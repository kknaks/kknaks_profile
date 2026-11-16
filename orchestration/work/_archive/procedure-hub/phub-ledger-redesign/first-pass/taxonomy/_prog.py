#!/usr/bin/env python3
"""progress.md 읽기 로그 갱신(manual/*.json 기준). python3 _prog.py <다음구획>"""
import json, os, sys, re
H = os.path.dirname(os.path.abspath(__file__))
cov = json.load(open(os.path.join(H, 'coverage.json')))
ids = [s['id'] for s in cov['sections']]
rows = []
done = []
for sid in ids:
    f = os.path.join(H, 'manual', sid + '.json')
    if os.path.exists(f):
        m = json.load(open(f))
        done.append(sid)
        rows.append('| %s | %s | `%s` | 관찰 %d · 표현 %d · 오분절 %d · 미결 %d |' % (sid, m['state'], m.get('last_pointer'), len(m.get('observations', [])), len(m.get('expressions', [])), len(m.get('seg_errors', [])), len(m.get('issues', []))))
p = open(os.path.join(H, 'progress.md')).read()
p = p.split('## 읽기 로그')[0]
nxt = sys.argv[1] if len(sys.argv) > 1 else '-'
p = re.sub(r'- 현재 구획: .*', '- 현재 구획: %s 까지 직접 읽기 완료 (%d/%d)' % (done[-1] if done else '-', len(done), len(ids)), p)
p = re.sub(r'- 다음 구획: .*', '- 다음 구획: %s (남은 구획: %s)' % (nxt, ', '.join(i for i in ids if i not in done) or '없음'), p)
p += '## 읽기 로그\n\n| 구획 | 상태 | 마지막 읽은 Pointer | 기록 |\n|---|---|---|---|\n' + '\n'.join(rows) + '\n'
open(os.path.join(H, 'progress.md'), 'w').write(p)
print(len(done), 'done; next', nxt)
