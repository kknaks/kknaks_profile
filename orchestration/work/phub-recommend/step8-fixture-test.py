"""step8-apply.py 고정 시험(7단계와 같은 틀) — 하나라도 FAIL 이면 종료 코드 1.

갈래
- interval      : 간격 낱말 사전 각 갈래 — 원천 문장 → 숫자 칸(days · open_high · same_day · first 표시 · marks)
- none          : 원천 · 결정 그대로 → open 0
- remove_decision / remove_key : 결정 한 줄(사전 · 패턴 · 질문 · 칸 규칙 · 경과표)을 빼면 open 이 나는가(open 종류 집합)
- step7_mutate  : 7단계 정본에서 끝점(조합 · CC 엣지 · 고민 노드)을 빼면 open 이 나는가(끝점 어긋남)
- avoid_check   : 고민 조건 금기 → 「피함」 엣지(U8-2)
- scope_check   : 출력 · 깊이 한정어를 떼고 묶음으로 연 피함 · 금기 · 같은 날 불가 = 조건부(검수 F1)
- claim_check   : 문장 패턴(U8-1) — 그 원천 행에서 나온 주장(끝점 계열 · first · days · same_day)
- semantic_check: 시맨틱 반영(10-30 B1 · B3 · B8 · U1 · U2) — 합병증/부작용 나눔 · 예외 · gap 채움 · 조건 아님 · 끝점 candidates[]
- resolution_check: 충돌 하나로(10-30 · conflict_resolution R1~R6) — X8 처분 · 등급 · 대기 · 전수 가드(두 값 0)

입력: step8-fixtures/cases.json · step8-decisions.json · step8-apply.py
출력: step8-fixtures/result.json (step8-apply.py 가 md 에 싣는다)
"""
import importlib.util
import collections
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # 작업 폴더에 __pycache__ 를 남기지 않는다

W = Path(__file__).resolve().parent
CASES = json.load(open(W / 'step8-fixtures' / 'cases.json'))['cases']
DEC = json.load(open(W / 'step8-decisions.json'))
spec = importlib.util.spec_from_file_location('step8_apply', W / 'step8-apply.py')
APPLY = importlib.util.module_from_spec(spec)
spec.loader.exec_module(APPLY)


def section(d, path):
    for p in path.split('.'):
        d = d[p]
    return d


def run(td, dec_path=None, step7=None):
    cmd = [sys.executable, str(W / 'step8-apply.py'), '--out', str(td)]
    if dec_path:
        cmd += ['--decisions', str(dec_path)]
    if step7:
        cmd += ['--step7', str(step7)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return None, f'실행 실패: {p.stderr.strip()[-300:]}'
    return json.load(open(td / 'step8-relations.json')), None


def iv_view(iv, keys):
    return {k: iv.get(k) for k in keys}


def fams(e):
    if e['level'] == '복합(나눔)':
        return '+'.join(fams(p) for p in e['parts'])
    return e['level'] if e['level'] in ('시술 아님', '해석 안 됨', '모든 시술') else ','.join(e['families'])


results = []
for c in CASES:
    note = c.get('note', '')
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        if c['type'] == 'interval':
            iv = APPLY.parse_interval(c['text'], DEC['interval_lexicon'])
            actual = iv_view(iv, c['expect'].keys())
            expect = c['expect']
            inp = f"간격 원문 「{c['text']}」"
        else:
            dec_path, step7 = None, None
            inp = '원천 · 결정 그대로'
            if c['type'] in ('remove_decision', 'remove_key'):
                d = json.load(open(W / 'step8-decisions.json'))
                if c['type'] == 'remove_decision':
                    lst = section(d, c['section'])
                    n = len(lst)
                    lst[:] = [x for x in lst if not all(x.get(k) == v for k, v in c['match'].items())]
                    assert len(lst) == n - 1, (c['id'], n, len(lst))
                    inp = f"결정 {c['section']} 에서 {c['match']} 뺌"
                else:
                    del section(d, c['section'])[c['key']]
                    inp = f"결정 {c['section']} 에서 키 {c['key']} 뺌"
                dec_path = td / 'dec.json'
                json.dump(d, open(dec_path, 'w'), ensure_ascii=False)
            elif c['type'] == 'step7_mutate':
                s7 = json.load(open(W / DEC['canon']['step7']))
                lst = section(s7, c['section'])
                n = len(lst)
                lst[:] = [x for x in lst if not all(x.get(k) == v for k, v in c['match'].items())]
                assert len(lst) < n, (c['id'], n, len(lst))
                step7 = td / 'step7.json'
                json.dump(s7, open(step7, 'w'), ensure_ascii=False)
                inp = f"7단계 {c['section']} 에서 {c['match']} 뺌({n - len(lst)}줄)"
            out, err = run(td, dec_path, step7)
            expect = sorted(c['expect'])
            if err:
                actual = [err]
            elif c['type'] == 'avoid_check':
                actual = sorted({f"{'/'.join(a['from_concerns'])}→{fams(a['to'])}|{a['qualifier']}" for a in out['avoid_edges']})
                inp = '고민 조건 금기 → 피함 엣지'
            elif c['type'] == 'scope_check':
                actual = sorted({f"{a['id']}|{a['qualifier']}|{a.get('scope') or '기본 적용'}" for a in out['avoid_edges']} |
                                {f"{x['id']}|{x['kind']}" for x in out['claims'] if x.get('scope_conditional')} |
                                {f"{k['id']}|조건" for k in out['conditions']['claims'] if k.get('scope_conditional')})
                inp = '출력 · 깊이 한정어 → 조건부(scope_rule)'
            elif c['type'] == 'claim_check':
                actual = sorted(f"{fams(x['a'])}→{fams(x['b'])} first={(x['interval'] or {}).get('first')} days={(x['interval'] or {}).get('days')} same_day={(x['interval'] or {}).get('same_day')}"
                                + (' by_sub=' + ' / '.join(f"{o.get('sub_condition')}:first={o.get('first')},days={o['days']},same_day={o['same_day']}" for o in x['interval']['options']) if (x['interval'] or {}).get('by_sub_condition') else '')
                                for x in out['claims'] if x['source'] == c['source'] and str(x['source_index']) == str(c['source_index']))
                inp = f"문장 패턴 {c['source']}[{c['source_index']}]"
            elif c['type'] == 'semantic_check':
                sf = out['safety']
                v = c['view']
                if v == 'side_effect_exceptions':
                    actual = sorted(f"{x['id']}|{x['name']}" for x in sf['side_effects'] if x.get('staff_question'))
                elif v == 'severity_split':
                    actual = sorted({f"합병증:{x['severity'] or x['severity_site']}" for x in sf['complications']} | {f"부작용:{x['severity'] or x['severity_site']}" for x in sf['side_effects']})
                elif v == 'gap_fill':
                    actual = sorted([f"{f}:{k}={n}" for f, d in out['summary']['gap_filled_families'].items() for k, n in d.items()]
                                    + [f"gap:{f}" for f in sf['complication_gap_families']] + [f"mild_only:{f}" for f in sf['complication_mild_only_families']['families']])
                elif v == 'not_condition':
                    actual = sorted({f"빠짐:{k['kind']}" for k in out['conditions']['not_condition']} | {f"남음:{k['kind']}" for k in out['conditions']['claims']})
                elif v == 'endpoint_kinds':
                    actual = sorted({f"{ep['kind']}|후보 {'여럿' if len(ep['candidates']) > 1 else '없음' if not ep['candidates'] else '하나'}" for e in out['edges'] for ep in e['endpoints'].values()})
                inp = f"시맨틱 반영 확인 — {v}"
            elif c['type'] == 'resolution_check':
                v = c['view']
                if v == 'x8':
                    X = {x['id']: x for x in out['conflicts']}
                    actual = sorted(f"{i}|{X[i]['resolution']['status']}|{X[i]['resolution']['rule']}" for i in c['ids'])
                elif v == 'grade':
                    X = {x['id']: x for x in out['conditions']['grade_conflicts']}
                    actual = sorted(f"{i}|{X[i]['resolution']['grade3']}|{X[i]['resolution']['rule']}" for i in c['ids'])
                elif v == 'wait':
                    X = {x['id']: x for x in out['conditions']['wait_resolved']}
                    actual = sorted(f"{i}|{list(o['sub_condition'])[0] if list(o['sub_condition'])[0] == '조건' else list(o['sub_condition'].values())[0]}={o['months']}" for i in c['ids'] for o in X[i]['options'])
                elif v == 'guard':
                    cr = out['summary']['conflict_resolution']
                    owners = [e['resolved'] for e in out['edges']] + [p['resolved'] for p in out['resolved_pairs']]
                    both = sum(1 for r in owners for f in ('first', 'same_day', 'days') if r[f] is not None and any(o['field'] == f for o in r['options']))
                    staff_first = sum(1 for r in owners if r['field_status'].get('first') == '의료진 확인' and r['first'] is not None)
                    gtwo = sum(1 for o in out['open'] if o['type'].startswith('두 값 — 단위 시술 × 조건'))
                    actual = sorted([f"두 값 단위 시술 쌍 {cr['two_value_unit_pairs']}", f"두 값 엣지 {both}", f"순서 반대인데 순서 단정 {staff_first}", f"등급 두 값 {gtwo}"])
                inp = f"충돌 하나로 — {v} {','.join(c['ids'])}"
            elif c['type'] == 'quality_check':  # 품질 수정(10-30) — 원인마다 1건(E · I · K · O · J)
                v = c['view']
                if v == 'E':  # 끝점 부위 낱말 — 주장 끝점이 그 부위 단위 시술만
                    x = next(x for x in out['claims'] if x['id'] == c['claim'])
                    ep = x[c['side']]
                    actual = sorted(set(ep.get('units') or []) | {u for p_ in ep.get('parts') or [] for u in p_.get('units') or []})
                elif v == 'I':  # 원천 행 1:1 착지표 — 갈래별 셈 · 없음 0
                    actual = sorted([f"{h}={n}" for h, n in collections.Counter(x['how'] for x in out['row_landing']).items()] +
                                    [f"{c['source']}[{x['index']}]={x['how']}" for x in out['row_landing'] if x['source'] == c['source'] and x['how'] != '구조(주장 · 조건 · 피함)'])
                elif v == 'K':  # 안전 0 단위 시술 gap 명시
                    actual = sorted(f"{g['unit']}|{g['status']}" for g in out['safety']['unit_gaps'] if g['unit'] in c['units'])
                elif v == 'O':  # 방향별 same_day
                    e_ = next(e for e in out['edges'] if e['id'] == c['edge'])
                    actual = sorted(f"{k}={d_['same_day']}" for k, d_ in (e_['resolved'].get('by_direction') or {}).items())
                elif v == 'J':  # 원천 안전 원문 — 계열 원문 칸
                    actual = sorted(k for k in out['safety']['family_text'].get(c['family'], {}) if 'extracted.json' in k)
                inp = f"품질 수정 확인 — {v}"
            else:
                actual = sorted({o['type'] for o in out['open']})
    ok = actual == expect
    results.append(dict(id=c['id'], type=c['type'], input=inp, expect=expect, actual=actual, pass_=ok, note=note))
    print(('PASS' if ok else 'FAIL'), c['id'], actual)
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
json.dump(res, open(W / 'step8-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
