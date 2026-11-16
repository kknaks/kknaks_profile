#!/usr/bin/env python3
"""읽기 보조: 구획별 형태소 결과에서 오분절 의심 어절을 모은다(build 후 실행). reading/S###.seg.txt 만 쓴다."""
import json, os, re
from collections import OrderedDict
HERE = os.path.dirname(os.path.abspath(__file__))
NOUNISH = {'NNG', 'NNP', 'NNB', 'NR', 'SL', 'SN', 'SH', 'XR'}
for fn in sorted(os.listdir(os.path.join(HERE, 'morphology'))):
    d = json.load(open(os.path.join(HERE, 'morphology', fn)))
    seen = OrderedDict()
    for rec in d['records']:
        v = rec['text']
        for m in re.finditer(r'\S+', v):
            s, e = m.start(), m.end()
            toks = [t for t in rec['tokens'] if t[2] >= s and t[3] <= e]
            if not re.search('[가-힣]', m.group()):
                continue
            tags = [t[1] for t in toks]
            run = 0; flag = False
            for i, t in enumerate(toks):
                if t[1] in NOUNISH:
                    run += 1
                    if run >= 2 and toks[i - 1][3] == t[2] and (t[1] in ('NNG','NNP') and toks[i-1][1] in ('NNG','NNP')) and (len(t[0]) == 1 or len(toks[i-1][0]) == 1):
                        flag = True
                else:
                    run = 0
            if any(x.startswith('W_') or x in ('UN', 'XR', 'NA', 'XPN') for x in tags):
                flag = True
            if flag:
                key = m.group()
                if key not in seen:
                    seen[key] = (rec['pointer'], ' '.join('%s/%s' % (t[0], t[1]) for t in toks))
    out = ['%s\t%s\t%s' % (k, p, a) for k, (p, a) in seen.items()]
    open(os.path.join(HERE, 'reading', fn.replace('.json', '.seg.txt')), 'w').write('\n'.join(out) + '\n')
    print(fn, len(out))
