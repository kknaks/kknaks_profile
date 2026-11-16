#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""합성 입력으로 실버 산출물(out/entities · relations · conflicts · dictionaries · gate · manifest)만 쓴다 — 재실행 바이트 동일 시험용(별도 프로세스).
report.md·게이트 2B 는 실제 원장 전용 보고라 쓰지 않는다(실제 build.py 의 재실행 동일은 check.py ④).

python3 tests/_core_build.py <workspace root> <out>"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import synth  # noqa: E402
from lib import pipeline  # noqa: E402
from lib.report import write_all  # noqa: E402
from lib.reportmd import compare, manifest  # noqa: E402


def main():
    root, out = sys.argv[1], sys.argv[2]
    w = synth.Workspace.__new__(synth.Workspace)
    w.root = root
    w.bronze, w.step1 = os.path.join(root, "bronze"), os.path.join(root, "step1-products.json")
    w.erd, w.dict = os.path.join(root, "erd-v3.1.json"), os.path.join(root, "erd-v3.1-dictionaries.json")
    w.decisions, w.out = os.path.join(root, "decisions"), out
    a = w.args(out=out)
    S = pipeline.run(a)
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    gc = {}
    recs, edges = write_all(S, out, None, gc)
    cmp_rows = compare(S, a.tuples)
    manifest(S, a, recs, edges, cmp_rows, gc, out)  # out/manifest.json


if __name__ == "__main__":
    main()
