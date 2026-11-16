"""구획 원문 읽기용 출력. 사용: python3 reading_dump.py S01 [S02 ...]  (읽기 보조 · 파일을 쓰지 않는다)"""
import sys
from pe_common import read_source, Parser, segment_of
raw, text, sha = read_source()
nodes = Parser(text).parse()
for seg in sys.argv[1:]:
    print("=====", seg)
    for n in nodes:
        if segment_of(n["pointer"]) != seg:
            continue
        if n["type"] in ("object", "array"):
            print(f'{n["pointer"] or "/"}  <{n["type"]} {n["child_count"]}>')
        else:
            print(f'{n["pointer"]}  [{n["type"]}] {n["value"]!r}')
