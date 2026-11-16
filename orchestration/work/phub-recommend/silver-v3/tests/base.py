# -*- coding: utf-8 -*-
"""시험 공통 — 분해 엔진(합성 사전·합성 원장) · 합성 빌드 캐시."""
import atexit
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
os.environ.setdefault("SILVER_TEST_TMP", "/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/f4798840-05cc-4695-94d0-decfad37f126/scratchpad")
os.makedirs(os.environ["SILVER_TEST_TMP"], exist_ok=True)

import synth  # noqa: E402
from lib.adverse31 import AdverseUnits31, ConditionTuples  # noqa: E402
from lib.decompose import Ids, Lexicon, ProcedureTuples, with_alias  # noqa: E402
from lib.util import mkid, norm  # noqa: E402

ERD = synth._erd()
RULES = ERD["resolve_rules"]
TRULES = ERD["tuple_rules"]
R12_SLOT = "treatment-optimization.optimal_combo[] (57)"
R9_SLOT = "problem-packages.procedures[].name (시술 종류 29)"


class Engines:
    """§1.3~§1.6 분해기 — 합성 사전 · 합성 원장으로(결정 없음) · v3.1 부작용 단위(AdverseUnits31) · 조건 단위(ConditionTuples)."""

    def __init__(self, dic=None, L=None, stopwords=True):
        self.L = L or synth.ledger()
        self.dic = dic or synth.dictionaries()
        self.lex = Lexicon(with_alias(self.dic))
        self.ids = Ids(self.dic, self.L, RULES)
        self.ids.stopwords_enabled = stopwords
        self.PT = ProcedureTuples(self.lex, RULES, self.ids, self.L)
        self.PT.run_catalog()
        self.AT = AdverseUnits31(self.ids, TRULES["adverse"])
        self.CT = ConditionTuples(self.dic, TRULES["condition"])

    def ref(self, label, hint=None, slot="시험"):
        return self.PT.run_reference(label, hint, "reference", slot)

    def item(self, fam, name):
        return self.PT.catalog[(fam, name)]

    def tuple_of(self, row):
        return self.PT.tuples[row["procedure_id"]]

    def name(self, text, locator="complications.json:categories[].complications[].name@T/0"):
        return self.AT.run_name(text, {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "locator": locator, "rec": (0, 0)})

    def phrase(self, text, locator="extracted.json:{code}.safety.common[]@T/0"):
        """문구 하나 판정(문구 사전 항목이 될 정규화형 · status auto|unlinked · 후보 · parsed · shape)."""
        return self.AT.evaluate(text, {"origin": "extracted.safety", "file": "extracted.json", "path": "{code}.safety.common[]", "locator": locator, "rec": ("M1", 0), "kind": "safety_phrase"})

    def cond(self, text, path="categories[].contraindications[]", file="consent-checklist.json", rec="M1/0"):
        return self.CT.run(file, path, rec, text, "M1", "contraindication")


_E = None


def engines():
    global _E
    if _E is None:
        _E = Engines()
    return _E


_BUILDS = {}


def build(key, decisions=(), L=None, dic=None, erd_path=None, erd_patch=None):
    """합성 빌드(pipeline.run) — key 별로 한 번. 반환 (Workspace, Silver). erd_path=synth.ERD32_PATH 면 v3.2 빌드."""
    if key in _BUILDS:
        return _BUILDS[key]
    w = synth.Workspace(L=L, dic=dic, erd_path=erd_path, erd_patch=erd_patch)
    if decisions:
        w.add_decisions(list(decisions))
    S = w.build()
    _BUILDS[key] = (w, S)
    return w, S


@atexit.register
def _cleanup():
    for w, _ in _BUILDS.values():
        w.cleanup()


def log(S, did):
    xs = [x for x in S.apply_log if x["id"] == did]
    return xs[0] if len(xs) == 1 else (xs or None)


def edges(S, rel, **kw):
    out = []
    for e in S.R.get(rel, []):
        if all((e["from"] if k.startswith("from") else e["to"]).get(k.split("_", 1)[1]) == v for k, v in kw.items()):
            out.append(e)
    return out


class T(unittest.TestCase):
    maxDiff = None
