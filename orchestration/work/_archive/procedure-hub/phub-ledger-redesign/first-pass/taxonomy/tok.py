#!/usr/bin/env python3
"""읽기 보조: 단어(부분 문자열)가 든 값의 형태소 분할을 보여준다. python3 tok.py S001 단어 [단어...]"""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sec = sys.argv[1]
words = sys.argv[2:]
files = [sec] if sec != 'ALL' else [f[:-5] for f in sorted(os.listdir(os.path.join(HERE, 'morphology')))]
for w in words:
    shown = set()
    for f in files:
        for rec in json.load(open(os.path.join(HERE, 'morphology', f + '.json')))['records']:
            i = rec['text'].find(w)
            if i < 0: continue
            m = re.search(r'\S*' + re.escape(w) + r'\S*', rec['text'])
            s, e = m.start(), m.end()
            an = ' '.join('%s/%s' % (t[0], t[1]) for t in rec['tokens'] if t[2] < e and t[3] > s)
            if an in shown: continue
            shown.add(an)
            print('%s\t%s\t%s\t%s' % (w, m.group(), an, rec['pointer']))
