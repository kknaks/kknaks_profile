"""step4-apply.py 고정 시험 — 「결정 한 줄 빼면 open」만. 사례마다 step4-decisions.json 의 한 줄을 빼고 돌려 open[] 이 기대와 같은지 본다.

입력: step4-fixtures/cases.json · step4-decisions.json · step4-apply.py
출력: step4-fixtures/result.json (step4-apply.py 가 md 에 싣는다). 하나라도 FAIL 이면 종료 코드 1.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
CASES = json.load(open(W / 'step4-fixtures' / 'cases.json'))['cases']


def label(o):
    t = o['type']
    if t in ('결정 없는 표현', '행선지 오류'):
        return f"{t}:{o['key']}"
    if t == '넘겨받은 것 행선지 없음':
        return f"{t}:{'|'.join(o['item']) if isinstance(o['item'], list) else o['item']}"
    if t == '근거 없는 대상 근육':
        return f"{t}:{o['muscle']}"
    if t in ('결정 없는 technique_hint',):
        return f"{t}:{o['ledger_id']}"
    if t in ('결정 없는 계열 기본 기법',):
        return f"{t}:{o['family']}"
    if t in ('결정 없는 초안 기법', '근거 없는 노드'):
        return f"{t}:{o['id']}"
    return f"{t}:{json.dumps(o, ensure_ascii=False)}"


results = []
for c in CASES:
    d = json.load(open(W / 'step4-decisions.json'))
    before = len(d[c['section']])
    d[c['section']] = [x for x in d[c['section']] if not all(x.get(k) == v for k, v in c['match'].items())]
    removed = before - len(d[c['section']])
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        json.dump(d, open(td / 'dec.json', 'w'), ensure_ascii=False)
        p = subprocess.run([sys.executable, str(W / 'step4-apply.py'), '--out', str(td), '--decisions', str(td / 'dec.json')],
                           capture_output=True, text=True)
        actual = ([f'실행 실패: {p.stderr.strip()[-200:]}'] if p.returncode != 0
                  else sorted(label(o) for o in json.load(open(td / 'step4-techniques.json'))['open']))
    ok = removed == 1 and actual == sorted(c['expect'])
    results.append(dict(id=c['id'], input=f"{c['section']} {json.dumps(c['match'], ensure_ascii=False)} 뺌({removed}줄)",
                        expect=sorted(c['expect']), actual=actual, pass_=ok))
    print(('PASS' if ok else 'FAIL'), c['id'], actual)
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
json.dump(res, open(W / 'step4-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
