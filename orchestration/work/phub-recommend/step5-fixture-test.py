"""step5-apply.py 고정 시험 — 사례마다 결정 한 줄을 빼거나 원천 사본에 행 하나를 더해 돌리고 open[] 이 기대와 같은지 본다.

입력: step5-fixtures/cases.json · step5-decisions.json(source 키) · step5-apply.py
출력: step5-fixtures/result.json (step5-apply.py 가 md 에 싣는다). 하나라도 FAIL 이면 종료 코드 1.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
CASES = json.load(open(W / 'step5-fixtures' / 'cases.json'))['cases']
DEC = json.load(open(W / 'step5-decisions.json'))
SRC = Path(DEC['source']['path'])
KEYS = ('id', 'unit', 'index', 'zone', 'product', 'name')


def label(o):
    t = o['type']
    if t == '결정이 가리키는 키 없음':
        return f"{t}:{o['where']}|{o['unit']}"
    if t == '넘겨받은 것 행선지 없음':
        return f"{t}:{o['source']}|{o.get('family') or o.get('id') or o.get('text') or o.get('key') or o.get('path')}"
    if t == '결정 없는 4단계 속성':
        return f"{t}:{o['attr']}|{o['key']}"
    for k in KEYS:
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
        src, out = td / 'src', td / 'out'
        src.mkdir(); out.mkdir()
        for f in sorted(SRC.glob('*.json')):
            os.symlink(f, src / f.name)
        dec_path = W / 'step5-decisions.json'
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
        elif c['type'] == 'add_market_row':
            os.unlink(src / 'market-pricing.json')
            m = json.load(open(SRC / 'market-pricing.json'))
            next(x for x in m['categories'] if x['id'] == c['category'])['items'].append(c['row'])
            json.dump(m, open(src / 'market-pricing.json', 'w'), ensure_ascii=False)
            inp = f"원천 market-pricing {c['category']} 에 「{c['row']['name']}」 더함"
        p = subprocess.run([sys.executable, str(W / 'step5-apply.py'), '--source', str(src), '--out', str(out), '--decisions', str(dec_path)],
                           capture_output=True, text=True)
        if p.returncode != 0:
            actual = [f'실행 실패: {p.stderr.strip()[-300:]}']
        elif c['type'] == 'override_check':  # 골드 빈틈 ①(10-30) — 부작용 덮어쓰기 값 = 원천 safety 원문 그대로 · 붙는 수준
            o_ = json.load(open(out / 'step5-units.json'))
            src_it = next(it_ for m_ in json.load(open(SRC / 'taxonomy.json'))['modality'] for s_ in m_['subcategories'] for it_ in s_['items'] if it_['id'] == c['item'])
            want = src_it['extracted'].get('safety') or {}
            host = next(x for x in o_['product_links'] if x['product'] == c['host']) if c['host_kind'] == 'product' else next(u for u in o_['units'] if u['id'] == c['host'])
            ov = next(x for x in host.get('side_effect_override') or [] if x['id'] == c['item'])
            actual = sorted([f"{k}={'원문 같음' if ov['values'].get(k) == v else '다름'}" for k, v in want.items() if v] + [f"level={ov['level']}", f"override_of={ov['override_of']}"] +
                            [f"행 {sum(n for k, n in o_['summary']['side_effect_override']['rows'].items() if not k.startswith('안 실음'))}"])
            inp = f"{c['host_kind']} {c['host']} ← extracted[{c['item']}]"
        elif c['type'] == 'source_text_check':  # 품질 J(10-30) — 안전 · 사후관리 원문이 붙는 수준(extracted 행)에 그대로
            o_ = json.load(open(out / 'step5-units.json'))
            row = next(x for x in o_['extracted'] if x['id'] == c['item'])
            src_it = next(it_ for m_ in json.load(open(SRC / 'taxonomy.json'))['modality'] for s_ in m_['subcategories'] for it_ in s_['items'] if it_['id'] == c['item'])
            want = {k: v for k, v in (src_it['extracted'].get('safety') or {}).items()}
            actual = sorted([f"{k}={'원문 같음' if (row.get('source_text') or {}).get('safety.' + k) == v else '다름'}" for k, v in want.items()] +
                            [f"extracted 행 {sum(1 for x in o_['extracted'] if x.get('source_text'))}/{len(o_['extracted'])} 원문 있음"])
            inp = f"extracted[{c['item']}] 안전 원문"
        else:
            actual = sorted(label(o) for o in json.load(open(out / 'step5-units.json'))['open'])
    ok = actual == sorted(c['expect'])
    results.append(dict(id=c['id'], type=c['type'], input=inp, expect=sorted(c['expect']), actual=actual, pass_=ok, note=c.get('note', '')))
    print(('PASS' if ok else 'FAIL'), c['id'], actual)
res = dict(total=len(results), passed=sum(r['pass_'] for r in results),
           cases=[dict({k: v for k, v in r.items() if k != 'pass_'}, **{'pass': r['pass_']}) for r in results])
json.dump(res, open(W / 'step5-fixtures' / 'result.json', 'w'), ensure_ascii=False, indent=1)
print(f"{res['passed']}/{res['total']}")
sys.exit(0 if res['passed'] == res['total'] else 1)
