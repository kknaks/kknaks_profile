"""step6-apply.py 고정 시험 — 사례마다 결정 한 줄을 빼고 돌려 open[] 이 기대와 같은지 본다.

입력: step6-fixtures/cases.json · step6-decisions.json · step6-apply.py
출력: step6-fixtures/result.json (step6-apply.py 가 md 에 싣는다). 하나라도 FAIL 이면 종료 코드 1.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
CASES = json.load(open(W / 'step6-fixtures' / 'cases.json'))['cases']


def label(o):
    t = o['type']
    if 'where' in o:
        return f"{t}:{o['where']}|{o.get('unit') or o.get('question')}"
    for k in ('id', 'name', 'source'):
        if k in o:
            return f"{t}:{o[k]}"
    return f"{t}:{json.dumps(o, ensure_ascii=False)}"


def section(d, path):
    for p in path.split('.'):
        d = d[p]
    return d


results = []
for c in CASES:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        dec_path = W / 'step6-decisions.json'
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
        p = subprocess.run([sys.executable, str(W / 'step6-apply.py'), '--out', str(td), '--decisions', str(dec_path)], capture_output=True, text=True)
        actual = [f'실행 실패: {p.stderr.strip()[-300:]}'] if p.returncode != 0 else sorted(label(o) for o in json.load(open(td / 'step6-packages.json'))['open'])
    ok = actual == sorted(c['expect'])
    results.append(dict(id=c['id'], type=c['type'], input=inp, expect=sorted(c['expect']), actual=actual, pass_=ok, note=c.get('note', '')))
    print(('PASS' if ok else 'FAIL'), c['id'], actual)
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
json.dump(res, open(W / 'step6-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
