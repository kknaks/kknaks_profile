#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD 적합성 시험 러너 — (1) enumerate_cases.py 로 경우 목록을 뽑고 (2) unittest 를 전부 돌린 뒤
(3) 목록의 모든 경우에 대응하는 시험이 있는지(covers · mark) 검사한다. 시험 FAIL · 빠진 경우 · ERD 에 없는 경우를 가리키는 시험 → exit 1.

python3 tests/run_tests.py [-v] [-k 패턴] [--cases-out 파일]
"""
import argparse
import json
import os
import sys
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import enumerate_cases as EC  # noqa: E402
from registry import COVERED  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", action="store_true")
    ap.add_argument("-k", default=None, help="시험 이름 부분 일치(이때 커버리지 검사는 건너뛴다)")
    ap.add_argument("--cases-out")
    a = ap.parse_args()
    t0 = time.time()
    erd, dic = EC.load(os.path.join(EC.ERD_DIR, "erd-v3.3.json")), EC.load(os.path.join(EC.ERD_DIR, "erd-v3.3-dictionaries.json"))
    cases = EC.enumerate_all(erd, dic)
    if a.cases_out:
        with open(a.cases_out, "w", encoding="utf-8") as f:
            json.dump({"summary": EC.summary(cases), "cases": cases}, f, ensure_ascii=False, indent=1)
    loader = unittest.TestLoader()
    if a.k:
        loader.testNamePatterns = [f"*{a.k}*"]
    suite = loader.discover(HERE, pattern="test_*.py", top_level_dir=os.path.dirname(HERE))
    res = unittest.TextTestRunner(verbosity=2 if a.v else 1).run(suite)
    ids = {c["id"] for c in cases}
    missing = [c for c in cases if c["id"] not in COVERED]
    unknown = sorted(set(COVERED) - ids)
    s = EC.summary(cases)
    print(f"\n경우의 수 {s['total']} · {json.dumps(s['by_category'], ensure_ascii=False)} · ref {json.dumps(s['ref_accept_reject'])}")
    print(f"시험 {res.testsRun} · 실패 {len(res.failures)} · 오류 {len(res.errors)} · 대응 경우 {len(ids & set(COVERED))}/{len(ids)}")
    ok = res.wasSuccessful()
    if not a.k:
        if missing:
            ok = False
            print(f"FAIL 시험 없는 경우 {len(missing)}:")
            for c in missing[:200]:
                print("  -", c["id"], f"({c['source']})")
        if unknown:
            ok = False
            print(f"FAIL ERD 에 없는 경우를 가리키는 시험 {len(unknown)}: {unknown[:50]}")
    print(f"{'PASS' if ok else 'FAIL'} ({time.time() - t0:.1f}s)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
