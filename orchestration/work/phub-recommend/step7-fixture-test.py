"""step7-apply.py 고정 시험(6단계와 같은 틀) — 사례마다 결정 한 줄을 빼고 돌려 open[] 이 기대와 같은지 본다.
row_check(10-29 게이트 → 규칙) — 결정 그대로 돌려 대응표 행 · 추천 조합 앵커가 규칙(R12~R18)대로인지 본다.
edge_check(10-29 R21 부위 올라가기) — 엣지 단위 시술이 올라간 층 · 계열만 · 영역 넘음 0 인지 본다.

입력: step7-fixtures/cases.json · step7-decisions.json · step7-apply.py
출력: step7-fixtures/result.json (step7-apply.py 가 md 에 싣는다). 하나라도 FAIL 이면 종료 코드 1.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
CASES = json.load(open(W / 'step7-fixtures' / 'cases.json'))['cases']


def label(o):
    t = o['type']
    if 'where' in o:
        return f"{t}:{o['where']}|{o.get('unit') or o.get('concern') or o.get('purpose') or o.get('site') or o.get('text')}"
    if 'source_id' in o and 'units' in o:  # 검수 F2 — 엣지 앵커 부위 밖
        return f"{t}:{o['source_id']}|{'/'.join(o['units'])}"
    for k in ('id', 'name', 'text', 'site', 'cc', 'kind'):
        if k in o:
            return f"{t}:{o[k]}"
    if 'names' in o:
        return f"{t}:{'/'.join(o['names'])}"
    return f"{t}:{json.dumps(o, ensure_ascii=False)}"


def section(d, path):
    for p in path.split('.'):
        d = d[p]
    return d


def row_check(out, rows):
    """대응표 행(원천 · 표현) → 대상(+ severity) · 추천 조합(id) → 고민 앵커. 사람 질문 행은 「(사람 질문)」"""
    got = []
    for x in rows:
        if 'combo' in x:
            t = next(c for c in out['combos'] if c['id'] == x['combo'])['anchor']['concern']
            got.append(f"{x['combo']} → {' · '.join(t) or '앵커 없음'}")
            continue
        rr = [r for r in out['correspondence'] if r['source'] == x['source'] and r['text'] == x['text']]
        if not rr:
            got.append(f"{x['text']} → (행 없음)")
            continue
        r = rr[0]
        t = ['(사람 질문)'] if r['human_check'] else list(r['target']) + [f'severity {v}' for v in r.get('severity') or []] + [f'@{v}' for v in r.get('rule_sites') or [] if x.get('sites')]
        got.append(f"{x['text']} → {' · '.join(t) or '대상 없음'}")
    return got


def edge_check(out, rows):
    """R21 부위 올라가기 — 엣지(경로 · 원천 id · 계열) → 단위 시술 부위 · 층, 또는 계열만. region 행 = 영역 넘은 엣지 셈"""
    U = {u['id']: u for u in json.load(open(W / 'step5-units.json'))['units']}
    s3 = json.load(open(W / 'step3-sites.json'))
    P = {n['name']: n['parent'] for n in s3['nodes']}

    def reg(s):
        if s not in P:
            return None
        while P[s]:
            s = P[s]
        return s
    got = []
    for x in rows:
        if x.get('region'):
            n = 0
            for e in out['edges']:
                rs = {reg('얼굴 전체' if a == '얼굴' else a) for a in e['anchor_sites']} - {None}
                if x['region'] != 'all' and rs != {x['region']}:
                    continue
                n += sum(1 for u in e['to_units'] if reg(U[u]['key']['site']) and rs and reg(U[u]['key']['site']) not in rs)
            got.append(f"영역 {x['region']} 앵커 엣지의 다른 영역 단위 시술 {n}")
            continue
        if x.get('combo_family'):  # R26 — 조합 구성 전체에서 그 계열 단위 시술 셈
            cb = next(c for c in out['combos'] if c['id'] == x['combo_family'])
            n = sum(1 for p in cb.get('components') or [] for u in p['units'] if U[u]['key']['family'] == x['unit_family'])
            got.append(f"{x['combo_family']} 의 {x['unit_family']} 단위 시술 {n}")
            continue
        if x.get('combo'):  # R22 — 추천 조합 구성(계열)의 다른 영역 단위 시술 셈
            cb = next(c for c in out['combos'] if c['id'] == x['combo'])
            n = sum(1 for p in cb.get('components') or [] if p.get('family') == x['family'] for u in p['units'] if reg(U[u]['key']['site']) == x['unit_region'])
            got.append(f"{x['combo']} {x['family']} 의 {x['unit_region']} 단위 시술 {n}")
            continue
        if x.get('combo_status'):  # 판단 ② — 조합 구성 표시
            cb = next(c for c in out['combos'] if c['id'] == x['combo_status'])
            p = next(p for p in cb['components'] if p.get('family') == x['family'])
            got.append(f"{x['combo_status']} {x['family']} 단위 시술 {len(p['units'])} · {'표시 있음' if x['label'] in (p.get('status') or '') else '표시 없음'}")
            continue
        if x.get('combo_purposes'):  # R24 보강 — 레시피 이름 조각의 목적
            cb = next(c for c in out['combos'] if c['id'] == x['combo_purposes'])
            got.append(f"{x['combo_purposes']} 목적 " + (' · '.join(cb['anchor'].get('purposes') or []) or '없음'))
            continue
        if x.get('combo_units'):  # R24 — 조합 구성 단위 시술
            cb = next(c for c in out['combos'] if c['id'] == x['combo_units'])
            p = next(p for p in cb['components'] if p.get('family') == x['family'])
            got.append(f"{x['combo_units']} {x['family']} → {'/'.join(sorted(p['units'])) or '계열만'}")
            continue
        if x.get('edge_units'):  # R23 · R24 · R26 — 엣지(경로 · 앵커 · 계열 · 원천 id) 단위 시술
            ee = [e for e in out['edges'] if e['source'].startswith(x['source']) and e['from'] == x['edge_units'] and e['to_family'] == x['family'] and (not x.get('sid') or x['sid'] in (e.get('source_ids') or [e['source_id']]))]
            got.append(f"{x['label']} → " + (' | '.join('/'.join(sorted(e['to_units'])) or '계열만' for e in ee) or '(엣지 없음)'))
            continue
        if x.get('dup'):  # R27 — (갈래 × 원천 시술 · 계열) ③ 엣지 수
            ee = [e for e in out['edges'] if e['source'].startswith('③') and e['from'] == x['dup'] and (e['evidence'] or {}).get('name') == x['name'] and e['to_family'] == x['family']]
            got.append(f"{x['dup']} {x['name']}({x['family']}) ③ 엣지 {len(ee)} · CC {sum(len(e.get('source_ids') or [1]) for e in ee)}")
            continue
        if x.get('combo_fields'):  # 골드 빈틈 ②(10-30) — 조합 구성 칸 셋 셈(요약 = 다시 셈)
            cu = out['summary']['combos']['component_units']
            re_ = {f_: sum(len(p_.get('units') or []) for c_ in out['combos'] for p_ in c_.get(f_) or []) for f_ in ('components', 'members', 'upgrade')}
            got.append(' · '.join(f"{f_} {cu[f_]}{'' if cu[f_] == re_[f_] else '≠' + str(re_[f_])}" for f_ in ('components', 'members', 'upgrade')) + f" = {cu['total']}")
            continue
        if x.get('edge_layer'):  # R32(품질 B) — 엣지 층 표시
            ee = [e for e in out['edges'] if e['source'].startswith(x['source']) and e['from'] == x['edge_layer'] and e['to_family'] == x['family']]
            got.append(f"{x['label']} → layer " + (' | '.join(str(e.get('layer')) for e in ee) or '(엣지 없음)'))
            continue
        if x.get('cc'):  # R28(품질 · CC 슬롯) — 그 CC 가 든 엣지(경로 · 계열)
            ee = [e for e in out['edges'] if x['cc'] in (e.get('ccs') or []) and (not x.get('root') or str(e.get('source_id') or '').startswith(x['root'] + ':'))]
            got.append(f"CC {x['cc']} 엣지 " + ' · '.join(sorted(f"{e['source'][:1]}{e['to_family']}" for e in ee)))
            continue
        if x.get('concern'):  # R22 — 고민 앵커 엣지의 특정 단위 시술 셈
            n = sum(1 for e in out['edges'] if (e['from'] == x['concern'] or x['concern'] in (e.get('from_concerns') or [])) and x['unit'] in e['to_units'])
            got.append(f"{x['concern']} 엣지의 {x['unit']} {n}")
            continue
        ee = [e for e in out['edges'] if e['source'].startswith(x['source']) and e['from'] == x['from'] and e['to_family'] == x['family']]
        if not ee:
            got.append(f"{x['label']} → (엣지 없음)")
            continue
        for e in ee[:1]:
            sites = sorted({U[u]['key']['site'] for u in e['to_units']})
            got.append(f"{x['label']} → " + (f"{'/'.join(sites)} ({e['site_check']})" if sites else f"계열만 {e['to_family']} ({e['site_check']})"))
    return got


results = []
for c in CASES:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        dec_path = W / 'step7-decisions.json'
        inp = '원천 · 결정 그대로'
        if c['type'] == 'remove_decision':
            d = json.load(open(dec_path))
            lst = section(d, c['section'])
            n = len(lst)
            lst[:] = [x for x in lst if not all(x.get(k) == v for k, v in c['match'].items())]
            assert len(lst) == n - 1, (c['id'], n, len(lst))
            dec_path = td / 'dec.json'
            json.dump(d, open(dec_path, 'w'), ensure_ascii=False)
            inp = f"결정 {c['section']} 에서 {c['match']} 뺌"
        elif c['type'] == 'set_decision':  # 검수 F1 · F2 — 결정 값 하나를 바꿔 가드가 open 을 내는지
            d = json.load(open(dec_path))
            if 'match' in c:
                hit = [x for x in section(d, c['section']) if all(x.get(k) == v for k, v in c['match'].items())]
                assert len(hit) == 1, (c['id'], len(hit))
                hit[0].update(c['fields'])
                inp = f"결정 {c['section']} {c['match']} 를 " + ' · '.join(f'{k} = {v}' for k, v in c['fields'].items())
            else:
                *head, last = c['section'].split('.')
                section(d, '.'.join(head))[last] = c['value']
                inp = f"결정 {c['section']} = {c['value']}"
            dec_path = td / 'dec.json'
            json.dump(d, open(dec_path, 'w'), ensure_ascii=False)
        elif c['type'] == 'edge_check':
            inp = '엣지 판정 ' + ' / '.join(f"「{x.get('label') or x.get('region')}」" for x in c['rows'])
        elif c['type'] == 'row_check':
            inp = '규칙 판정 ' + ' / '.join(f"「{x.get('combo') or x['text']}」" for x in c['rows'])
        p = subprocess.run([sys.executable, str(W / 'step7-apply.py'), '--out', str(td), '--decisions', str(dec_path)], capture_output=True, text=True)
        if p.returncode != 0:
            actual = [f'실행 실패: {p.stderr.strip()[-300:]}']
        elif c['type'] == 'edge_check':
            actual = sorted(edge_check(json.load(open(td / 'step7-concerns.json')), c['rows']))
        elif c['type'] == 'row_check':
            actual = sorted(row_check(json.load(open(td / 'step7-concerns.json')), c['rows']))
        else:
            actual = sorted(label(o) for o in json.load(open(td / 'step7-concerns.json'))['open'])
    ok = actual == sorted(c['expect'])
    results.append(dict(id=c['id'], type=c['type'], input=inp, expect=sorted(c['expect']), actual=actual, pass_=ok, note=c.get('note', '')))
    print(('PASS' if ok else 'FAIL'), c['id'], actual)
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
json.dump(res, open(W / 'step7-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
