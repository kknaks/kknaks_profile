#!/usr/bin/env python3
"""직접 읽기용 출력 도우미(파일 쓰기 없음): 구획 하나의 모든 노드를 원문 순서로 Pointer·리터럴과 함께 출력.
citations/N 객체는 자식 값 전부를 한 줄로 묶어 출력한다(값 생략 없음).
사용: python3 read_segment.py S01"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
sm = json.load(open(os.path.join(H, 'source-map.json'), encoding='utf-8'))
seg = sys.argv[1]
cit = re.compile(r'^(.*/citations/\d+)/([a-z_]+)$')
buf = None
def flush():
    global buf
    if buf:
        print('%s {%s}' % (buf[0], ' | '.join('%s=%s' % kv for kv in buf[1])))
    buf = None
for n in sm['nodes']:
    if n['segment'] != seg:
        continue
    m = cit.match(n['pointer'])
    if m and n['type'] not in ('object', 'array'):
        if not buf or buf[0] != m.group(1):
            flush(); buf = [m.group(1), []]
        buf[1].append((m.group(2), n['literal']))
        continue
    flush()
    if re.search(r'/citations/\d+$', n['pointer']):
        continue  # 객체 자체는 다음 줄 묶음에 포함
    if n['type'] in ('object', 'array'):
        print('%s  <%s %d>' % (n['pointer'] or '(root)', n['type'], n['child_count']))
    else:
        print('%s = %s' % (n['pointer'], n['literal']))
flush()
