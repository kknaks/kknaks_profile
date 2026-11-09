"""구획 직접 읽기용 출력 보조. 원문 값을 Pointer 와 함께 그대로 출력한다(해석 없음)."""
import json, sys
SRC = __file__.rsplit('/first-pass/', 1)[0] + '/../phub-recommend/bronze/phub-ledger/market-pricing.json'
d = json.load(open(SRC, encoding='utf-8'))
for seg in sys.argv[1:]:
    n = int(seg[1:])
    if n == 0:
        for k in ['version', 'updated', 'currency', 'note']:
            print(f'/{k}\t{json.dumps(d[k], ensure_ascii=False)}')
        continue
    c = d['categories'][n - 1]; b = f'/categories/{n-1}'
    print(f'== {seg} {b}/id={c["id"]!r} {b}/name={c["name"]!r} items={len(c["items"])}')
    for i, it in enumerate(c['items']):
        print(f'{b}/items/{i}\t' + '\t'.join(f'{k}={json.dumps(v, ensure_ascii=False)}' for k, v in it.items()))
