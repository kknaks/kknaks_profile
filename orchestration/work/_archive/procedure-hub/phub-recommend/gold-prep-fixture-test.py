#!/usr/bin/env python3
"""골드 전 정리(10-30 · phub-recommend-gold-prep-brief.md) 고정 시험 — 항목마다 1건 이상. 실버 · 측정 파일을 읽기만 한다.

1 측정 계열 옮김 표 = 결정 파일에서(quality-eval.py MOVE_SRC) · 문항 · 슬롯 · 의도는 1차와 같음(정답 sub_families 만 2단계 결정으로 달라질 수 있음)
2 2단계 다파장 하위(step2-families multi_wavelength) · 사용자 판단 ③(엑셀 V 동의어 U5-138)과 맞물림 · 같은 성격 남은 것 0
3 부작용 덮어쓰기 값 — step5-fixture-test QG1a · QG1b
4 조합 구성 — step7-fixture-test QG2 + 여기서 시맨틱 combo_component 셈 = 7단계 셈
출력: gold-prep-fixtures/result.json · 하나라도 FAIL 이면 종료 코드 1.
"""
import json
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
J = lambda f: json.load(open(W / f, encoding='utf-8'))

ns = {'__file__': str(W / 'quality-eval.py'), '__name__': 'qe_fixture'}
_src = (W / 'quality-eval.py').read_text(encoding='utf-8')
exec(_src.split("\nif __name__ == '__main__':")[0], ns)
ns['_move_pairs']()
MS = ns['MOVE_SRC']

F2 = J('step2-families.json')
PF = {p['ledger_id']: p for p in F2['product_family']}
PF_BY_NAME = {p['display_name']: p for p in F2['product_family']}
MW = F2['multi_wavelength']
U5 = J('step5-units.json')
S7 = J('step7-concerns.json')
SEM = J('semantic.json')
Q1 = {q['id']: q for q in J('quality-v1/quality-eval-set.json')['questions']}
QN = {q['id']: q for q in J('quality-eval-set.json')['questions']}


def q_same_except_subs():
    bad = []
    for k in sorted(set(Q1) | set(QN)):
        a, b = dict(Q1.get(k) or {}), dict(QN.get(k) or {})
        for d in (a, b):
            if isinstance(d.get('answer'), dict):
                d['answer'] = {kk: vv for kk, vv in d['answer'].items() if kk != 'sub_families'}
        if a != b:
            bad.append(k)
    return bad


def multi_left():
    """같은 성격 남은 것 — 2단계 전수(seen) 중 「보조 더함」인데 rows 에 없는 것 · 하위 하나 · 보조 없음 · 손대지 않은 것"""
    added = {r['ledger_id'] for r in MW['rows']}
    return [x['display_name'] for x in MW['seen'] if (x['handled'] == '보조 더함') != (x['ledger_id'] in added)]


EXCEL = next(p for p in F2['product_family'] if p['display_name'] == '엑셀 V')
DEV = next(d for d in U5['device_name_synonyms'] if d['name'] == '엑셀 V')
UK = {u['id']: u['key'] for u in U5['units']}
cc = next(e for e in SEM['edge_kinds'] if e['kind'] == 'combo_component')

CASES = [
    ('G1a', '1', '옮김 표에 7단계 fam_kw 「서브시전」 (M8 → N4) — Q020', lambda: any('fam_kw 「서브시전」' in w for w in MS.get(('M8', 'N4'), ()))),
    ('G1b', '1', '옮김 표에 7단계 fam_kw 「지방분해」 (M14 → N1) — Q025', lambda: any('fam_kw 「지방분해」' in w for w in MS.get(('M14', 'N1'), ()))),
    ('G1c', '1', '옮김 표에 5단계 결정 원장 행선지 출처가 있음', lambda: any('5단계 결정 원장 행선지' in w for v in MS.values() for w in v)),
    ('G1d', '1', '문항 · 슬롯 · 의도 · 정답(하위 빼고)은 1차와 같음', lambda: q_same_except_subs() == []),
    ('G2a', '2', '엑셀 V 하위 = 엔디야그 레이저(주) + KTP(보조 · 원천 532nm)', lambda: EXCEL['sub_family'] == '엔디야그 레이저' and EXCEL['also_sub_families'] == [{'family': 'M8', 'sub_family': 'KTP'}]),
    ('G2b', '2', '사용자 판단 ③ — 5단계 「엑셀 V」 동의어 단위 시술 하위가 엑셀 V 주 · 보조 하위 안', lambda: {UK[u]['sub_family'] for u in DEV['units']} <= {EXCEL['sub_family']} | {a['sub_family'] for a in EXCEL['also_sub_families']}),
    ('G2c', '2', '파장 → 매질은 원천 근거 수가 가장 많은 것(532 → KTP · 755 → 알렉산드라이트)', lambda: MW['wavelength_medium']['532']['medium'] == 'KTP' and MW['wavelength_medium']['755']['medium'] == '알렉산드라이트 레이저'),
    ('G2d', '2', '추가된 보조마다 그 행 원천 파장이 매질에 대응', lambda: all(any((MW['wavelength_medium'].get(n) or {}).get('medium') == a for n in r['wavelengths']) for r in MW['rows'] for a in r['added'])),
    ('G2e', '2', '같은 성격(다파장 · 빠진 매질) 남은 것 0', lambda: multi_left() == []),
    ('G2f', '2', '10-30 ⑤ — 보조가 이미 있던 노블린 · 클라리티2 · 아포지 엘리트 플러스 · 디스커버리 피코에 KTP 보조(원천 532nm)', lambda: all('KTP' in {a['sub_family'] for a in PF_BY_NAME[n]['also_sub_families']} for n in ('노블린', '클라리티2', '아포지 엘리트 플러스', '디스커버리 피코'))),
    ('G4', '4', '시맨틱 combo_component 셈 = 7단계 구성 칸 셋 셈', lambda: cc['count'] == S7['summary']['combos']['component_units']['total'] and cc['path'] == 'combos[].components|members|upgrade[].units[]'),
]

results = []
for cid, item, what, fn in CASES:
    try:
        ok, err = bool(fn()), None
    except Exception as e:
        ok, err = False, repr(e)[:200]
    results.append(dict(id=cid, item=item, what=what, pass_=ok, error=err))
    print(('PASS' if ok else 'FAIL'), cid, what, err or '')
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
(W / 'gold-prep-fixtures').mkdir(exist_ok=True)
json.dump(res, open(W / 'gold-prep-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
