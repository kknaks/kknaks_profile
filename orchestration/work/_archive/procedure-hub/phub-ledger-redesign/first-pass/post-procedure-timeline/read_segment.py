"""구획 하나를 Pointer 와 함께 출력한다(읽기 보조, 쓰기 없음). usage: python3 read_segment.py S01"""
import json, sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
SRC = os.path.join(ROOT, 'orchestration/work/phub-recommend/bronze/phub-ledger/post-procedure-timeline.json')
d = json.load(open(SRC, encoding='utf-8'))
seg = sys.argv[1]
def walk(o, p):
    if isinstance(o, dict):
        if not o: print(p, '{}')
        for k, v in o.items(): walk(v, p + '/' + k)
    elif isinstance(o, list):
        if not o: print(p, '[]')
        for i, v in enumerate(o): walk(v, f'{p}/{i}')
    else:
        print(p, '=', json.dumps(o, ensure_ascii=False))
if seg == 'S00':
    for k in ['version', 'updated', 'consensus_method', 'reaction_levels']: walk(d[k], '/' + k)
else:
    i = int(seg[1:]) - 1
    walk(d['timelines'][i], f'/timelines/{i}')
