# -*- coding: utf-8 -*-
"""드라이런 2차 — 7차 호출 잡기 · 2차 분해 한 번 돌리기(쓰기 없음)."""
import os
import sys

DRY2 = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(DRY2)
ERD_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, DRY2)

from lib import v32 as V32  # noqa: E402
from lib.util import norm  # noqa: E402
import dry2_au as D2  # noqa: E402
import kiwi_t0 as KT  # noqa: E402

# 1차 발주서 목록 그대로(dryrun/run_dryrun.py 와 같은 값) — 2차: R1 에서 「이상」을 뺀다
R1_LISTED_1 = ["장기간", "장기적", "임시", "일시", "일시적", "지속", "지속적", "영구", "영구적", "중등도", "중증", "심한", "경미", "경미한", "과도", "과도한", "이상", "불규칙",
               "미세", "미세한", "약간", "약간의", "광범위", "광범위한", "초기", "드문", "높음", "증가", "덜"]
R1_LISTED = [w for w in R1_LISTED_1 if w != "이상"]
R2_LISTED = ["신경", "하악변연신경", "안면신경", "감각신경", "눈", "안구", "결막", "눈썹", "눈꺼풀", "표정근", "근육", "두피", "피부", "진피", "혈관", "전신", "표면", "주사 부위", "시술 부위"]
S_RULES = {"suffix_감", "suffix_증", "suffix_형성"}


def capture_7th():
    """7차 파이프라인을 그대로 돌려(쓰기 없음) 마지막 분해 호출의 입력을 잡는다(1차 드라이런과 같은 방법)."""
    sys.path.insert(0, os.path.join(HERE, "dryrun"))
    import run_dryrun as R1M   # 1차 코드 — 읽기만(capture_7th · default_args)
    return R1M.capture_7th()


def surfaces(dj, name):
    for d in dj["dictionaries"]:
        if d["name"] == name:
            return {norm(v): e["canonical"] for e in d["entries"] for v in [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]}
    return {}


def run_stage2(call, kt, r1, r2):
    dj = call[0][0]
    sites = surfaces(dj, "site")
    dict_values = {norm(v) for v in kt.registered}
    D2.STATE = D2.Dry2State(kt, r1, r2, sites, dict_values)
    orig = V32.AdverseUnits32
    V32.AdverseUnits32 = D2.Dry2AdverseUnits
    try:
        a, k = call
        P, A, C, X = V32.run_v32(*a, **k)
    finally:
        V32.AdverseUnits32 = orig
    return A, D2.STATE, dict(V32.CUR)
