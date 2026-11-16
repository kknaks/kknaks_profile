#!/usr/bin/env python3
"""literature-evidence 1차 결과 독립 검증. 파일을 쓰지 않는다. 실패 시 exit 1.

실행(레포 루트): python3 orchestration/work/phub-ledger-redesign/first-pass/literature-evidence/verify.py
           선택: --selftest  (메모리 안에서 결과를 변형해 검출되는지 확인)

build.py 의 스캐너를 쓰지 않는다: 원본은 json.loads(object_pairs_hook)로 다시 읽고,
위치는 원문 텍스트 슬라이스를 json.loads 로 되읽어 대조한다.
"""
import copy
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
SRC = os.path.join(REPO, 'orchestration/work/phub-recommend/bronze/phub-ledger/literature-evidence.json')
EXPECTED_SHA = '6e179872a9c234491ca62c20899757fca3aa5388833aa6bc4d1ac28a032aebfd'
KO_APPLY = re.compile(r'^(/accuracy_summary/rubric|/categories/M\d+/(moa|adverse_effects|effects)/\d+/(patient_ko|accuracy_note))$')


def load(name):
    return json.load(open(os.path.join(HERE, name), encoding='utf-8'))


def walk(x, p=''):
    yield p, x
    if isinstance(x, dict):
        for k, v in x.items():
            yield from walk(v, p + '/' + k.replace('~', '~0').replace('/', '~1'))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from walk(v, p + '/' + str(i))


def jtype(v):
    if isinstance(v, bool):
        return 'boolean'
    if v is None:
        return 'null'
    if isinstance(v, int):
        return 'number_int'
    if isinstance(v, float):
        return 'number_float'
    return {str: 'string', dict: 'object', list: 'array'}[type(v)]


def checks(D):
    try:
        return _checks(D)
    except Exception as ex:  # 결과 파일이 깨져 검사 자체가 실패하면 실패로 센다
        return ['검증 예외 %s: %s' % (type(ex).__name__, ex)]


def _checks(D):
    F = []
    raw, text, py, dups = D['raw'], D['text'], D['py'], D['dups']
    sm, cov, mo, ex, issues = D['source_map'], D['coverage'], D['morphology'], D['expressions'], D['issues']
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECTED_SHA:
        F.append('원본 해시 변경 %s' % sha)
    for name, obj in (('source-map', sm['source']), ('coverage', cov), ('morphology', mo), ('expressions', ex), ('issues-index', issues)):
        h = obj.get('sha256') or obj.get('source_sha256')
        if h != sha:
            F.append('%s 해시 불일치' % name)
    if dups:
        F.append('원본 중복 키 %d' % len(dups))
    if sm['parse']['duplicate_keys']:
        F.append('source-map 이 중복 키를 기록함(원본 재파싱과 대조 필요)')

    # ---------- 구조·값 양방향
    truth = dict(walk(py))
    nodes = {n['pointer']: n for n in sm['nodes']}
    if len(nodes) != len(sm['nodes']):
        F.append('source-map pointer 중복')
    missing = set(truth) - set(nodes)
    extra = set(nodes) - set(truth)
    if missing:
        F.append('source-map 누락 %d 예 %s' % (len(missing), sorted(missing)[:3]))
    if extra:
        F.append('source-map 불필요 %d 예 %s' % (len(extra), sorted(extra)[:3]))
    cp2b = None
    for p, n in nodes.items():
        if p not in truth:
            continue
        v = truth[p]
        if n['type'] != jtype(v):
            F.append('자료형 불일치 %s' % p)
        s, e = n['file_cp']
        seg = text[s:e]
        try:
            if json.loads(seg) != v:
                F.append('파일 cp 구간 값 불일치 %s' % p)
        except Exception:
            F.append('파일 cp 구간 파싱 실패 %s' % p)
        bs, be = n['file_byte']
        if raw[bs:be] != seg.encode('utf-8'):
            F.append('바이트 구간 불일치 %s' % p)
        if isinstance(v, (dict, list)):
            if n['child_count'] != len(v):
                F.append('자식 수 불일치 %s' % p)
            if n['is_leaf'] != (len(v) == 0):
                F.append('빈 컨테이너 말단 표시 오류 %s' % p)
        else:
            if n['literal'] != seg:
                F.append('리터럴 불일치 %s' % p)
            if n['value'] != v:
                F.append('값 불일치 %s' % p)
            if not n['is_leaf']:
                F.append('말단 표시 오류 %s' % p)
        if n['key'] is not None:
            ks, ke = n['key_file_cp']
            if json.loads(text[ks:ke]) != n['key'] or text[ks:ke] != n['key_literal']:
                F.append('키 구간 불일치 %s' % p)
        if n['type'] == 'string' and 'decoded_to_file_cp' in n:
            dec = ''.join(json.loads('"' + text[a:b] + '"') for a, b in n['decoded_to_file_cp'])
            if dec != v:
                F.append('이스케이프 대응표 불일치 %s' % p)
    # 순서
    for p, v in truth.items():
        if isinstance(v, dict):
            ks = list(v.keys())
            got = sorted([n for n in sm['nodes'] if n['parent'] == p], key=lambda n: n['order'])
            if [n['key'] for n in got] != ks:
                F.append('키 순서 불일치 %s' % p)
    leaves = {p for p, v in truth.items() if not isinstance(v, (dict, list)) or len(v) == 0}
    if set(cov['all_leaf_pointers']) != leaves:
        F.append('coverage all_leaf_pointers ≠ 원본 말단')
    if set(cov['all_node_pointers']) != set(truth):
        F.append('coverage all_node_pointers ≠ 원본 노드')

    # ---------- 구획 소유
    owned = {}
    for sg in cov['segments']:
        for p in sg['owned_pointers']:
            if p in owned:
                F.append('소유 중복 %s (%s, %s)' % (p, owned[p], sg['id']))
            owned[p] = sg['id']
        if set(sg['owned_leaf_pointers']) - set(sg['owned_pointers']):
            F.append('%s 말단 소유가 소유 노드 밖' % sg['id'])
        if set(sg['owned_leaf_pointers']) != (set(sg['owned_pointers']) & leaves):
            F.append('%s 소유 말단 집합 불일치' % sg['id'])
        for c in sg['context_refs']:
            if c not in truth:
                F.append('%s 공동참조 경로 없음 %s' % (sg['id'], c))
        if sg['reading_state'] != 'read_direct':
            F.append('%s 미독 상태 %s' % (sg['id'], sg['reading_state']))
        for f in (sg['manual_file'], sg['review_file']):
            if not f or not os.path.exists(os.path.join(HERE, f)):
                F.append('%s 결과 파일 없음 %s' % (sg['id'], f))
        mf = D['manual'].get(sg['id'])
        if mf is None or mf.get('reading_state') != 'read_direct' or mf.get('last_read_pointer') not in truth:
            F.append('%s manual 상태/마지막 Pointer 이상' % sg['id'])
        # 마지막 읽은 Pointer 가 그 구획 소유여야 함
        if mf and owned.get(mf.get('last_read_pointer')) not in (sg['id'], None):
            F.append('%s last_read_pointer 가 다른 구획 소유' % sg['id'])
    if set(owned) != set(truth):
        F.append('구획 소유 합집합 ≠ 원본 노드 (누락 %d, 불필요 %d)' % (len(set(truth) - set(owned)), len(set(owned) - set(truth))))
    for p, sgid in owned.items():
        m = re.match(r'^/categories/M(\d+)', p)
        want = 'S%02d' % int(m.group(1)) if m else 'S00'
        if sgid != want:
            F.append('구획 규칙 위반 %s → %s' % (p, sgid))

    # ---------- review 문서 대조
    idx = D['review_md']
    for sg in cov['segments']:
        if 'review-part-%s.md' % sg['id'] not in idx:
            F.append('review.md 목차에 %s 없음' % sg['id'])
        part = D['parts'].get(sg['id'], '')
        rows = {}
        for line in part.splitlines():
            m = re.match(r'^\| `([^`]*)` \| (.*?) \| (\w+) \| (.*) \| (\d+)–(\d+) \| (\w*) \| ([^|]*) \|$', line)
            if m:
                rows[m.group(1)] = m
        for p in sg['owned_pointers']:
            key = p or '(root)'
            m = rows.get(key)
            if not m:
                F.append('review-part-%s 에 행 없음 %s' % (sg['id'], key))
                continue
            n = nodes[p]
            col = n['key'] if n['key'] is not None else ('[%d]' % n['index'] if n['index'] is not None else '(root)')
            if m.group(2).replace('\\|', '|') != col:
                F.append('원본 컬럼명 불일치 %s' % p)
            if m.group(3) != n['type']:
                F.append('review 자료형 불일치 %s' % p)
            if n['type'] not in ('object', 'array'):
                if m.group(4).replace('\\|', '|') != n['literal']:
                    F.append('review 원문 값 불일치 %s' % p)
            if [int(m.group(5)), int(m.group(6))] != n['file_cp']:
                F.append('review 구간 불일치 %s' % p)
        if len(rows) != len(sg['owned_pointers']):
            F.append('review-part-%s 행 수 %d ≠ 소유 %d' % (sg['id'], len(rows), len(sg['owned_pointers'])))
        for sec in ('## 1. 원문 값', '## 2. 잠정 관찰', '## 3. 수동 표현', '## 4. 미결'):
            if sec not in part:
                F.append('review-part-%s 절 없음 %s' % (sg['id'], sec))

    # ---------- 형태소 적용/제외
    strings = {p for p, v in truth.items() if not isinstance(v, (dict, list))}
    ap = [v['pointer'] for v in mo['values']]
    exc = [x['pointer'] for x in mo['excluded']]
    if len(set(ap)) != len(ap) or len(set(exc)) != len(exc) or set(ap) & set(exc):
        F.append('형태소 적용/제외 중복')
    if set(ap) | set(exc) != strings:
        F.append('형태소 적용∪제외 ≠ 원본 비컨테이너 말단')
    if set(ap) != {p for p in strings if KO_APPLY.match(p)}:
        F.append('형태소 적용 집합이 정책(patient_ko·accuracy_note·rubric)과 다름')
    for x in mo['excluded']:
        if not x.get('reason') or not x.get('kind'):
            F.append('제외 사유 없음 %s' % x['pointer'])
    if mo['analyzer']['version'] != '0.24.1' or mo['analyzer']['model_type'] != 'cong' or mo['analyzer']['num_workers'] != 1:
        F.append('분석기 설정 기록 불일치')
    flagged = {}
    for v in mo['values']:
        val = truth[v['pointer']]
        if v['text'] != val:
            F.append('형태소 text 불일치 %s' % v['pointer'])
        n = nodes[v['pointer']]
        if not n['literal_equals_decoded']:
            F.append('적용 값에 이스케이프 있음(file_cp 계산 전제 위반) %s' % v['pointer'])
        if v['token_count'] != len(v['tokens']):
            F.append('토큰 수 불일치 %s' % v['pointer'])
        for t in v['tokens']:
            if val[t['start']:t['end']] != t['surface']:
                F.append('토큰 구간 불일치 %s #%d' % (v['pointer'], t['i']))
            if text[t['file_cp'][0]:t['file_cp'][1]] != t['surface']:
                F.append('토큰 파일 구간 불일치 %s #%d' % (v['pointer'], t['i']))
            if not t.get('lemma') and t['lemma'] != '':
                F.append('lemma 누락 %s #%d' % (v['pointer'], t['i']))
            for r in t.get('known_issue', []):
                flagged.setdefault((v['pointer'], t['i']), set()).add(r)
    occ_tok = {}
    rules = {r['id']: r for r in mo['segmentation_review']['rules']}
    for o in mo['segmentation_review']['occurrences']:
        r = rules.get(o['rule'])
        if not r:
            F.append('규칙 없는 출현 %s' % o['rule'])
            continue
        val = truth[o['pointer']]
        if val[o['span_in_value'][0]:o['span_in_value'][1]] != o['surface'] or text[o['file_cp'][0]:o['file_cp'][1]] != o['surface']:
            F.append('오분절 출현 구간 불일치 %s %s' % (o['rule'], o['pointer']))
        if [list(x) for x in o['raw_tokens']] != [list(x) for x in r['signature']]:
            F.append('오분절 출현 토큰 ≠ 서명 %s' % o['rule'])
        for i in range(*o['token_index']):
            occ_tok.setdefault((o['pointer'], i), set()).add(o['rule'])
    if occ_tok != flagged:
        F.append('오분절 출현 ↔ 토큰 표시 불일치')
    for rid in rules:
        if not any(o['rule'] == rid for o in mo['segmentation_review']['occurrences']):
            F.append('출현 0인 규칙 %s' % rid)
    # 서명 재검출(독립): 같은 서명이 표시 없이 남아 있지 않은지
    for v in mo['values']:
        tl = v['tokens']
        for rid, r in rules.items():
            sig = r['signature']
            for a in range(len(tl) - len(sig) + 1):
                if all(tl[a + j]['form'] == sig[j][0] and tl[a + j]['tag'] == sig[j][1] for j in range(len(sig))):
                    if not all(rid in tl[a + j].get('known_issue', []) for j in range(len(sig))):
                        F.append('표시 누락 서명 %s %s' % (rid, v['pointer']))
    keys_in_src = {n['key'] for n in sm['nodes'] if n['key'] is not None}
    if {f['key'] for f in mo['field_names']} != keys_in_src:
        F.append('필드명 처리 목록 ≠ 원본 키 집합')

    # ---------- 표현
    seen = set()
    ids = set()
    for e in ex['expressions']:
        if e['id'] in ids:
            F.append('표현 ID 중복 %s' % e['id'])
        ids.add(e['id'])
        if e['pointer'] not in truth or not isinstance(truth[e['pointer']], str):
            F.append('표현 Pointer 이상 %s' % e['id'])
            continue
        val = truth[e['pointer']]
        s, t = e['span_in_value']
        if not (0 <= s < t <= len(val)) or val[s:t] != e['text']:
            F.append('표현 구간 불일치 %s' % e['id'])
        a, b = e['file_cp']
        try:
            if json.loads('"' + text[a:b] + '"') != e['text']:
                F.append('표현 파일 구간 불일치 %s' % e['id'])
        except Exception:
            F.append('표현 파일 구간 파싱 실패 %s' % e['id'])
        if raw[e['file_byte'][0]:e['file_byte'][1]] != text[a:b].encode('utf-8'):
            F.append('표현 바이트 구간 불일치 %s' % e['id'])
        k = (e['pointer'], s, t, tuple(e['facets']), e['origin'])
        if k in seen:
            F.append('표현 중복 생성 %s' % e['id'])
        seen.add(k)
        if e['status'] not in ('P', 'F', 'B', 'I', 'K', 'A'):
            F.append('표현 상태 이상 %s' % e['id'])
        if e['segment'] != owned.get(e['pointer']):
            F.append('표현 구획 불일치 %s' % e['id'])
    n_manual = sum(len(m.get('expressions', [])) for m in D['manual'].values())
    if n_manual != sum(1 for e in ex['expressions'] if e['origin'] == 'manual'):
        F.append('수동 표현 수 ≠ manual 기록 수')
    # 수동 표현 ID 가 review-part 에 실렸는지
    for e in ex['expressions']:
        if e['origin'] == 'manual' and e['id'] not in D['parts'].get(e['segment'], ''):
            F.append('수동 표현 review 누락 %s' % e['id'])

    # ---------- 관찰·미결
    allids = set()
    for sgid, m in D['manual'].items():
        for kind in ('observations', 'issues'):
            for o in m.get(kind, []):
                if o['id'] in allids:
                    F.append('관찰/미결 ID 중복 %s' % o['id'])
                allids.add(o['id'])
                for p in o['pointers']:
                    if p not in truth:
                        F.append('%s 없는 Pointer %s' % (o['id'], p))
                if o['id'] not in D['parts'].get(sgid, ''):
                    F.append('review-part 에 %s 없음' % o['id'])
                if kind == 'issues' and o['class'] not in ('A', 'B', 'C', 'K', 'P', 'F', 'I'):
                    F.append('미결 문자 이상 %s' % o['id'])
                if kind == 'issues' and o['class'] in ('A', 'C'):
                    F.append('열린 %s 미결 %s (보고 상태와 대조 필요)' % (o['class'], o['id']))
    if len(issues['issues']) != sum(len(m.get('issues', [])) for m in D['manual'].values()):
        F.append('issues-index 수 ≠ manual 미결 수')
    for f in ('review.md', 'issues.md', 'validation.md', 'progress.md', 'build.py', 'segmentation-review.json'):
        if not os.path.exists(os.path.join(HERE, f)):
            F.append('산출물 없음 %s' % f)
    return F


def load_all():
    raw = open(SRC, 'rb').read()
    dups = []

    def hook(pairs):
        ks = [k for k, _ in pairs]
        if len(ks) != len(set(ks)):
            dups.append(ks)
        return dict(pairs)
    py = json.loads(raw, object_pairs_hook=hook)
    D = {'raw': raw, 'text': raw.decode('utf-8'), 'py': py, 'dups': dups,
         'source_map': load('source-map.json'), 'coverage': load('coverage.json'), 'morphology': load('morphology.json'),
         'expressions': load('expressions.json'), 'issues': load('issues-index.json'),
         'review_md': open(os.path.join(HERE, 'review.md'), encoding='utf-8').read(), 'parts': {}, 'manual': {}}
    for sg in D['coverage']['segments']:
        fp = os.path.join(HERE, 'review-part-%s.md' % sg['id'])
        D['parts'][sg['id']] = open(fp, encoding='utf-8').read() if os.path.exists(fp) else ''
        mp = os.path.join(HERE, 'manual', '%s.json' % sg['id'])
        if os.path.exists(mp):
            D['manual'][sg['id']] = json.load(open(mp, encoding='utf-8'))
    return D


def selftest(D):
    """원본·결과를 메모리에서 변형해 검출되는지 본다(파일 쓰기 없음)."""
    cases = []

    def mut(name, f):
        E = copy.deepcopy({k: v for k, v in D.items() if k not in ('raw', 'text')})
        E['raw'], E['text'] = D['raw'], D['text']
        f(E)
        cases.append((name, len(checks(E)) > 0))
    mut('source-map 말단 1개 삭제', lambda E: E['source_map']['nodes'].pop(-1))
    mut('구획 소유 1개 삭제', lambda E: E['coverage']['segments'][5]['owned_pointers'].pop(3))
    mut('구획 소유 중복', lambda E: E['coverage']['segments'][1]['owned_pointers'].append(E['coverage']['segments'][2]['owned_pointers'][0]))
    mut('구획 미독', lambda E: E['coverage']['segments'][7].__setitem__('reading_state', 'unread'))
    mut('표현 구간 1칸 이동', lambda E: E['expressions']['expressions'][10]['span_in_value'].__setitem__(0, E['expressions']['expressions'][10]['span_in_value'][0] + 1))
    mut('토큰 구간 변형', lambda E: E['morphology']['values'][3]['tokens'][2].__setitem__('end', E['morphology']['values'][3]['tokens'][2]['end'] + 1))
    mut('제외 1개 삭제', lambda E: E['morphology']['excluded'].pop(0))
    mut('오분절 표시 삭제', lambda E: [t.pop('known_issue', None) for v in E['morphology']['values'] for t in v['tokens']])
    mut('review 행 값 변형', lambda E: E['parts'].__setitem__('S04', E['parts']['S04'].replace('Skin Boosters', 'Skin Booster', 1)))
    mut('review 행 삭제', lambda E: E['parts'].__setitem__('S12', '\n'.join(l for l in E['parts']['S12'].splitlines() if '/categories/M12/effects/7/statement`' not in l)))
    mut('원본 바이트 변형', lambda E: E.__setitem__('raw', E['raw'].replace(b'2026-09-03', b'2026-09-04', 1)))
    return cases


def main():
    D = load_all()
    h0 = hashlib.sha256(D['raw']).hexdigest()
    F = checks(D)
    st = None
    if '--selftest' in sys.argv:
        st = selftest(D)
    h1 = hashlib.sha256(open(SRC, 'rb').read()).hexdigest()
    if h0 != h1:
        F.append('검증 중 원본 해시 변경')
    print(json.dumps({'source_sha256_start': h0, 'source_sha256_end': h1, 'failure_count': len(F), 'failures': F[:50],
                      'counts': {'nodes': len(D['source_map']['nodes']), 'leaves': len(D['coverage']['all_leaf_pointers']),
                                 'segments': len(D['coverage']['segments']),
                                 'segments_read_direct': sum(1 for s in D['coverage']['segments'] if s['reading_state'] == 'read_direct'),
                                 'morph_applied': len(D['morphology']['values']), 'morph_excluded': len(D['morphology']['excluded']),
                                 'tokens': sum(v['token_count'] for v in D['morphology']['values']),
                                 'seg_issue_occurrences': len(D['morphology']['segmentation_review']['occurrences']),
                                 'expressions': len(D['expressions']['expressions']),
                                 'manual_expressions': sum(1 for e in D['expressions']['expressions'] if e['origin'] == 'manual'),
                                 'issues': len(D['issues']['issues'])},
                      'selftest': [{'case': c, 'detected': d} for c, d in st] if st else None}, ensure_ascii=False, indent=1))
    if F or (st and not all(d for _, d in st)):
        sys.exit(1)


if __name__ == '__main__':
    main()
