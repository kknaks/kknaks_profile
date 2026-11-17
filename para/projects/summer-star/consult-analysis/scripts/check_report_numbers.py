#!/usr/bin/env python3
"""보고서의 수가 전부 집계 JSON 에 있는지 대조한다(SPEC-002 §7 「보고서에만 있는 수는 없다」).

- 보고서 본문(앞머리 YAML 뒤)의 수를 모두 뽑는다. 문서 번호(SPEC-002 · D-11 · E-1) · 판 번호(0.2.1) · 날짜 · 절 번호 · 표 정렬 줄은 뺀다.
- JSON 안의 모든 수(정수 · 소수 · 사전 키로 쓴 수)와 비교한다. 천 단위 쉼표는 지우고 본다.
- 없는 수가 하나라도 있으면 종료 1. 출력은 수와 줄 번호만.
"""

import argparse
import json
import re
import sys

SKIP = [
    re.compile(r"\b[A-Z][A-Za-z]*-\d+(?:\.\d+)*\b"),  # SPEC-002 · D-11 · E-1 · WP-3 · ISO-8601 같은 이름
    re.compile(r"\b[A-Za-z]+\d+\b"),  # l2 · q1 · q3 · U+1F300 의 일부 같은 낱말
    re.compile(r"\b\d+\.\d+\.\d+\b"),  # 판 번호
    re.compile(r"\b\d{4}-\d{2}-\d{2}(?:T[\d:.]+Z)?\b"),  # 날짜 · 시각
    re.compile(r"U\+[0-9A-Fa-f]+"),
    re.compile(r"`[^`]*`"),  # 코드 표기(칸 · 값 이름)
    re.compile(r"\[[^\]]*\]\([^)]*\)"),  # 링크
    re.compile(r"^#+\s*\d+\.\s*"),  # 절 번호
]
NUM = re.compile(r"(?<![\dA-Za-z.])\d[\d,]*(?:\.\d+)?(?![\dA-Za-z])")  # 한글이 붙어도 수로 본다(278.2분)


def json_numbers(obj, out):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        out.add(round(float(obj), 1))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if re.fullmatch(r"\d+", k):
                out.add(float(k))
            json_numbers(v, out)
    elif isinstance(obj, list):
        for v in obj:
            json_numbers(v, out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--json", required=True)
    args = ap.parse_args(argv)
    nums = set()
    with open(args.json, encoding="utf-8") as fh:
        json_numbers(json.load(fh), nums)
    with open(args.report, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    start = 0
    if lines and lines[0] == "---":
        start = lines.index("---", 1) + 1
    seen = missing = 0
    for i, line in enumerate(lines[start:], start=start + 1):
        if re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", line):
            continue
        s = line
        for p in SKIP:
            s = p.sub(" ", s)
        for tok in NUM.findall(s):
            v = float(tok.replace(",", ""))
            seen += 1
            if round(v, 1) not in nums:
                missing += 1
                print("JSON 에 없음: 줄 %d · %s" % (i, tok))
    print("보고서의 수 %d개 · JSON 에 없음 %d" % (seen, missing))
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
