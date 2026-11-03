"""step3-apply.py 고정 시험 — 사례마다 원천 사본에 문장 파일 하나를 붙이거나 결정 한 줄을 빼고 돌려 open[] 이 기대와 같은지 본다.

입력: step3-fixtures/cases.json · step3-decisions.json(source 키) · step3-apply.py
출력: step3-fixtures/result.json (step3-apply.py 가 md 에 싣는다). 하나라도 FAIL 이면 종료 코드 1.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
CASES = json.load(open(W / 'step3-fixtures' / 'cases.json'))['cases']
DEC = json.load(open(W / 'step3-decisions.json'))
SRC = Path(DEC['source']['path'])


def label(o):
    if o['type'] == '사전 밖 부위 형태소':
        return o['token']
    if o['type'] == '결정 없는 문자열':
        return f"결정없음:{o['key'][0]}|{o['key'][1]}"
    if o['type'] == '트리 밖 결정 문자열에 행선지 없음':
        return f"트리밖행선지없음:{o['key'][0]}"
    return f"{o['type']}:{o.get('string')}"


results = []
for c in CASES:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        src, out = td / 'src', td / 'out'
        src.mkdir(); out.mkdir()
        for f in sorted(SRC.glob(DEC['source']['glob'])):
            os.symlink(f, src / f.name)
        dec_path = W / 'step3-decisions.json'
        inp = '원천 그대로'
        if c['type'] == 'add_text':
            json.dump({'fixture': c['text']}, open(src / 'zz-fixture.json', 'w'), ensure_ascii=False)
            inp = f"「{c['text']}」"
        elif c['type'] == 'remove_decision':
            d = json.load(open(dec_path))
            d['strings'] = [s for s in d['strings'] if s['key'] != c['key']]
            dec_path = td / 'dec.json'
            json.dump(d, open(dec_path, 'w'), ensure_ascii=False)
            inp = f"결정에서 {c['key']} 뺌"
        p = subprocess.run([sys.executable, str(W / 'step3-apply.py'), '--source', str(src), '--out', str(out), '--decisions', str(dec_path)],
                           capture_output=True, text=True)
        if p.returncode != 0:
            actual = [f'실행 실패: {p.stderr.strip()[-200:]}']
        else:
            actual = sorted(label(o) for o in json.load(open(out / 'step3-sites.json'))['open'])
    ok = actual == sorted(c['expect'])
    results.append(dict(id=c['id'], type=c['type'], input=inp, expect=sorted(c['expect']), actual=actual, pass_=ok, note=c.get('note', '')))
    print(('PASS' if ok else 'FAIL'), c['id'], actual)
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
json.dump(res, open(W / 'step3-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
