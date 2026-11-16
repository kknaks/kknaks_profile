"""market-pricing.json 1차 조사 결과 독립 검증. 파일을 쓰지 않는다. 실패 시 exit 1.

레포 루트에서: python3 orchestration/work/phub-ledger-redesign/first-pass/market-pricing/verify.py
"""
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC = REPO / 'orchestration/work/phub-recommend/bronze/phub-ledger/market-pricing.json'
EXPECTED_SHA = '601d7e7b4db29731bf15304ff3ec9489ba38838e9f5ba2144c2c181cfd15e477'

fails = []
checks = 0


def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def esc(k):
    return k.replace('~', '~0').replace('/', '~1')


def independent_walk(obj, ptr=''):
    """json 표준 파서 결과에서 Pointer → (type, value) 를 독립적으로 만든다."""
    out = {}
    if isinstance(obj, dict):
        out[ptr] = ('object', len(obj))
        for k, v in obj.items():
            out.update(independent_walk(v, f'{ptr}/{esc(k)}'))
    elif isinstance(obj, list):
        out[ptr] = ('array', len(obj))
        for i, v in enumerate(obj):
            out.update(independent_walk(v, f'{ptr}/{i}'))
    else:
        t = ('null' if obj is None else 'boolean' if isinstance(obj, bool) else 'integer' if isinstance(obj, int)
             else 'number' if isinstance(obj, float) else 'string')
        out[ptr] = (t, obj)
    return out


def coverage_checks(cov, leaf_set, cont_set, label=''):
    errs = []
    owned = []
    for s in cov['segments']:
        owned += s['owned_leaf_pointers']
    if set(cov['all_leaf_pointers']) != leaf_set:
        errs.append(f'{label}coverage all_leaf_pointers != 원문 말단 집합 (누락 {len(leaf_set - set(cov["all_leaf_pointers"]))} · 불필요 {len(set(cov["all_leaf_pointers"]) - leaf_set)})')
    if set(owned) != leaf_set:
        errs.append(f'{label}구획 소유 합집합 != 원문 말단 (누락 {sorted(leaf_set - set(owned))[:5]} · 불필요 {sorted(set(owned) - leaf_set)[:5]})')
    if len(owned) != len(set(owned)):
        errs.append(f'{label}구획 간 소유 중복 {len(owned) - len(set(owned))}')
    oc = []
    for s in cov['segments']:
        oc += s['owned_container_pointers']
    if set(oc) != cont_set or len(oc) != len(set(oc)):
        errs.append(f'{label}컨테이너 소유 불일치')
    for s in cov['segments']:
        if not s.get('direct_read'):
            errs.append(f'{label}{s["id"]} direct_read 아님')
        if not s.get('machine_extracted'):
            errs.append(f'{label}{s["id"]} machine_extracted 아님')
    return errs


def main():
    raw0 = SRC.read_bytes()
    sha0 = hashlib.sha256(raw0).hexdigest()
    check(sha0 == EXPECTED_SHA, f'원본 해시 시작 불일치 {sha0}')
    text = raw0.decode('utf-8')

    dups = []

    def hook(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                dups.append(k)
            seen.add(k)
        return dict(pairs)
    data = json.loads(text, object_pairs_hook=hook)
    check(not dups, f'원문 중복 키 {dups}')
    ind = independent_walk(data)
    leaf_set = {p for p, (t, v) in ind.items() if t not in ('object', 'array')} | \
               {p for p, (t, v) in ind.items() if t in ('object', 'array') and v == 0}
    cont_set = {p for p, (t, v) in ind.items() if t in ('object', 'array')}

    sm = load('source-map.json')
    morph = load('morphology.json')
    expr = load('expressions.json')
    cov = load('coverage.json')
    segs = load('segments.json')
    for name, o in (('source-map', sm), ('morphology', morph), ('expressions', expr), ('coverage', cov), ('segments', segs)):
        check(o['source_sha256'] == EXPECTED_SHA, f'{name} 기록 해시 불일치')
    check(sm['source_bytes'] == len(raw0), 'source_bytes 불일치')

    # ---- 1. 구조·값 양방향
    nodes = {n['pointer']: n for n in sm['nodes']}
    check(len(nodes) == len(sm['nodes']), 'source-map Pointer 중복')
    check(set(nodes) == set(ind), f'source-map 노드 ↔ 원문 Pointer 불일치 (누락 {set(ind) - set(nodes)} · 불필요 {set(nodes) - set(ind)})')
    for p, (t, v) in ind.items():
        n = nodes.get(p)
        if not n:
            continue
        check(n['type'] == t, f'자료형 불일치 {p}')
        if t in ('object', 'array'):
            check(n['length'] == v, f'길이 불일치 {p}')
        else:
            check(n['value'] == v and type(n['value']) == type(v), f'값 불일치 {p}')
    # 배열 순서: 인덱스 Pointer 가 원문 순서와 같은지 (리터럴 시작 위치 단조 증가)
    order = [n['literal_char_span'][0] for n in sm['nodes']]
    check(order == sorted(order), 'source-map 노드 순서가 원문 순서와 다름')

    # ---- 2. 구간 재현
    for n in sm['nodes']:
        cs, ce = n['literal_char_span']
        bs, be = n['literal_byte_span']
        seg_c = text[cs:ce]
        seg_b = raw0[bs:be].decode('utf-8')
        check(seg_c == seg_b, f'코드포인트/바이트 구간 불일치 {n["pointer"]}')
        check(json.loads(seg_c) == ind[n['pointer']][1] if n['type'] not in ('object', 'array') else
              len(json.loads(seg_c)) == n['length'], f'리터럴 구간 원문 재현 실패 {n["pointer"]}')
        if n['type'] not in ('object', 'array'):
            check(n['literal'] == seg_c, f'literal 문자열 불일치 {n["pointer"]}')
    keyocc = sm['key_occurrences']
    check(len(keyocc) == sum(1 for p in ind if p != '' and not re.search(r'/\d+$', p)), '키 출현 수 불일치')
    for k in keyocc:
        cs, ce = k['literal_char_span']
        check(json.loads(text[cs:ce]) == k['key'], f'키 구간 재현 실패 {k["pointer"]}')
        check(k['pointer'] in ind, f'키 Pointer 무효 {k["pointer"]}')

    # ---- 3. coverage
    for e in coverage_checks(cov, leaf_set, cont_set):
        check(False, e)
    seg_ids = [s['id'] for s in segs['segments']]
    check([s['id'] for s in cov['segments']] == seg_ids, 'coverage 구획 목록 ≠ segments.json')
    for s in cov['segments']:
        check((HERE / s['manual_record']).exists(), f'{s["id"]} manual 기록 없음')
        rp = HERE / s['review_file']
        check(rp.exists(), f'{s["id"]} review 파일 없음')
        if rp.exists():
            check(s['review_section'] in rp.read_text(encoding='utf-8'), f'{s["id"]} review 절 없음')
        mo = json.loads((HERE / s['manual_record']).read_text(encoding='utf-8'))
        check(mo.get('direct_read') is True and mo['segment'] == s['id'], f'{s["id"]} manual direct_read 아님')
        check(mo['last_pointer'] in s['owned_leaf_pointers'], f'{s["id"]} 마지막 읽은 Pointer 가 구획 밖')
        # 마지막 읽은 Pointer 가 구획의 마지막 말단인지 (끝까지 읽음)
        check(mo['last_pointer'] == s['owned_leaf_pointers'][-1], f'{s["id"]} 마지막 읽은 Pointer ≠ 구획 끝')
        for ptr, *_ in mo['observations']:
            check(ptr in ind, f'{s["id"]} 관찰 Pointer 무효 {ptr}')
        for iid, st, ptrs, _ in mo['issues']:
            check(st in 'ABCIPFK' and len(st) == 1, f'{iid} 상태 문자 무효')
            for p in ptrs:
                check(p in ind, f'{iid} Pointer 무효 {p}')
    # 변이 시험: 소유 하나를 빼거나 중복시키면 검출되는가
    m1 = copy.deepcopy(cov); m1['segments'][3]['owned_leaf_pointers'].pop()
    check(coverage_checks(m1, leaf_set, cont_set) != [], '변이 시험(소유 누락) 미검출')
    m2 = copy.deepcopy(cov); m2['segments'][4]['owned_leaf_pointers'].append(m2['segments'][5]['owned_leaf_pointers'][0])
    check(coverage_checks(m2, leaf_set, cont_set) != [], '변이 시험(소유 중복) 미검출')

    # ---- 4. 형태소 적용/제외 대응
    str_ptrs = {p for p, (t, v) in ind.items() if t == 'string'}
    applied = morph['applied']
    ap = [a['pointer'] for a in applied]
    ex = [e['pointer'] for e in morph['excluded_strings']]
    check(len(ap) == len(set(ap)) and len(ex) == len(set(ex)) and not (set(ap) & set(ex)), '형태소 적용/제외 중복')
    check(set(ap) | set(ex) == str_ptrs, f'문자열 말단 ↔ 적용/제외 불일치 {str_ptrs ^ (set(ap) | set(ex))}')
    ns = {n['pointer'] for n in morph['non_string_leaves']}
    check(ns == {p for p in leaf_set if ind[p][0] not in ('string', 'object', 'array')}, '숫자 말단 목록 불일치')
    for e in morph['excluded_strings']:
        check(bool(e['reason']) and e['value'] == ind[e['pointer']][1], f'제외 기록 불량 {e["pointer"]}')
    ntok = 0
    for a in applied:
        v = ind[a['pointer']][1]
        check(a['text'] == v, f'형태소 원문 불일치 {a["pointer"]}')
        prev = -1
        for t in a['tokens']:
            ntok += 1
            check(0 <= t['start'] <= t['end'] <= len(v), f'토큰 구간 범위 밖 {a["pointer"]}')
            check(t['slice'] == v[t['start']:t['end']], f'토큰 slice 불일치 {a["pointer"]}')
            check(t['form_equals_slice'] == (t['form'] == t['slice']), f'form_equals_slice 불일치 {a["pointer"]}')
            check(t['start'] >= prev, f'토큰 순서 역전 {a["pointer"]}')
            prev = t['start']
        # 공백·문장부호 외 모든 문자가 어떤 토큰 구간에 덮이는지
        covered = set()
        for t in a['tokens']:
            covered.update(range(t['start'], max(t['end'], t['start'])))
        miss = [i for i, ch in enumerate(v) if not ch.isspace() and i not in covered]
        check(not miss, f'토큰이 덮지 않은 문자 {a["pointer"]} {[v[i] for i in miss]}')
    check(ntok == morph['counts']['tokens'], '토큰 수 집계 불일치')
    tokmap = {a['pointer']: a for a in applied}
    for x in morph['known_missegmentation_occurrences']:
        a = tokmap.get(x['pointer'])
        check(a is not None, f'오분절 Pointer 무효 {x["pointer"]}')
        if a:
            s, e = x['span']
            check(a['text'][s:e] == x['surface'], f'오분절 구간 재현 실패 {x["pointer"]}')
            got = [[t['form'], t['tag']] for t in a['tokens'] if s <= t['start'] < e]
            check(got == x['raw_tokens'], f'오분절 원시 토큰 불일치 {x["pointer"]}')
    check(morph['analyzer']['version'] == '0.24.1' and morph['analyzer']['model_type'] == 'cong'
          and morph['analyzer']['num_workers'] == 1, '분석기 설정 기록 불일치')
    fn = {k['key'] for k in keyocc}
    check({f['field_name'] for f in morph['field_names']} == fn, '필드명 분석 목록 불일치')

    # ---- 5. 표현
    for x in expr['auto_candidates'] + expr['manual_expressions']:
        v = ind.get(x['pointer'], (None, None))[1]
        check(isinstance(v, str) and v[x['start']:x['end']] == x['text'] and x['full_value'] == v,
              f'표현 구간 재현 실패 {x["id"]}')
    regen = set()
    for pdef in expr['method']['patterns']:
        for p in ap:
            for m in re.finditer(pdef['pattern'], ind[p][1]):
                regen.add((p, m.start(), m.end(), pdef['id']))
    got = {(x['pointer'], x['start'], x['end'], x['pattern_id']) for x in expr['auto_candidates']}
    check(regen == got, f'자동 후보 재현 불일치 (누락 {len(regen - got)} · 불필요 {len(got - regen)})')
    check(len(expr['auto_candidates']) == len(got), '자동 후보 중복')
    check(all(x['review'] for x in expr['auto_candidates']), '검토 표시 없는 자동 후보')
    mexp = 0
    for sid in seg_ids:
        mo = json.loads((HERE / 'manual' / f'{sid}.json').read_text(encoding='utf-8'))
        mexp += len(mo['expressions'])
        mine = [x for x in expr['manual_expressions'] if x['segment'] == sid]
        check(len(mine) == len(mo['expressions']), f'{sid} 수동 표현 수 불일치')
        for (ptr, sub, persp, note), x in zip(mo['expressions'], mine):
            check(x['pointer'] == ptr and x['text'] == sub, f'{sid} 수동 표현 대응 불일치 {ptr} {sub}')
            check(ptr in leaf_set and seg_ids[[s['id'] for s in cov['segments']].index(sid)] == sid, '')
    check(mexp == len(expr['manual_expressions']), '수동 표현 총수 불일치')

    # ---- 6. 읽기용 문서 대조 (분할 문서 포함)
    parts = {sid: (HERE / f'review-part-{sid}.md').read_text(encoding='utf-8') for sid in seg_ids}
    head = (HERE / 'review.md').read_text(encoding='utf-8')
    for sid in seg_ids:
        check(f'review-part-{sid}.md' in head, f'review.md 목차에 {sid} 없음')
    def mdv(v):
        return str(v).replace('|', '\\|')
    for k in ('version', 'updated', 'currency', 'note'):
        check(f"| `/{k}` | `{k}` | string | `{mdv(data[k])}` |" in parts['S00'], f'S00 원문 값 행 없음 /{k}')
    for ci, cat in enumerate(data['categories']):
        sid = f'S{ci + 1:02d}'; b = f'/categories/{ci}'; P = parts[sid]
        check(f"| `{b}/id` | `id` | string | `{cat['id']}` |" in P, f'{sid} id 행 없음')
        check(f"| `{b}/name` | `name` | string | `{mdv(cat['name'])}` |" in P, f'{sid} name 행 없음')
        rows = [l for l in P.splitlines() if re.match(rf'^\| `{b}/items/\d+` \| ', l)]
        check(len(rows) == len(cat['items']), f'{sid} 항목 행 수 {len(rows)} ≠ {len(cat["items"])}')
        for j, it in enumerate(cat['items']):
            row = f"| `{b}/items/{j}` | {mdv(it['name'])} | {mdv(it['unit'])} | {it['low']} | {it['mid']} | {it['high']} |"
            check(row in P, f'{sid} 항목 값 행 누락/변형 {b}/items/{j}')
        for n in [x for x in sm['nodes'] if x['segment'] == sid and x['type'] == 'string']:
            check(f"| `{n['pointer']}` | {mdv(n['value'])} |" in P, f'{sid} 형태소 행 없음 {n["pointer"]}')
    issues_md = (HERE / 'issues.md').read_text(encoding='utf-8')
    allids = []
    for sid in seg_ids:
        mo = json.loads((HERE / 'manual' / f'{sid}.json').read_text(encoding='utf-8'))
        for iid, *_ in mo['issues']:
            allids.append(iid)
            check(f'| {iid} |' in parts[sid], f'{iid} 구획 문서에 없음')
        for ptr, ob, st in mo['observations']:
            check(mdv(ob) in parts[sid], f'{sid} 관찰 누락 {ptr}')
    for iid, *_ in json.loads((HERE / 'manual' / 'cross-issues.json').read_text(encoding='utf-8'))['issues']:
        allids.append(iid)
    check(len(allids) == len(set(allids)), '미결 ID 중복')
    for iid in allids:
        check(f'| {iid} |' in issues_md, f'issues.md 에 {iid} 없음')
    check(not re.search(r'\| C — 현재 사용자 결정 필요 \| [1-9]', issues_md), 'C 건수 0 아님(보고와 불일치)')
    for x in morph['known_missegmentation_occurrences']:
        check(f"`{x['pointer']}` [{x['span'][0]},{x['span'][1]})" in issues_md, f'issues.md 오분절 출현 없음 {x["pointer"]}')

    # ---- 7. 원본 해시 끝
    sha1 = hashlib.sha256(SRC.read_bytes()).hexdigest()
    check(sha1 == EXPECTED_SHA, '원본 해시 끝 불일치')

    print(json.dumps({'checks': checks, 'failures': len(fails), 'source_sha256_start': sha0, 'source_sha256_end': sha1,
                      'nodes': len(ind), 'leaves_and_empty_containers': len(leaf_set), 'containers': len(cont_set),
                      'segments': len(seg_ids), 'string_values': len(str_ptrs), 'morph_applied': len(ap),
                      'morph_excluded': len(ex), 'tokens': ntok, 'auto_candidates': len(got),
                      'manual_expressions': mexp, 'issues': len(allids)}, ensure_ascii=False))
    for f in fails[:50]:
        print('FAIL', f)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
