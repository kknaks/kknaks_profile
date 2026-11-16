# -*- coding: utf-8 -*-
"""ERD v2.3 잎 키 행선지 규칙. v2.2(erd_colmap_v22.py) 위에 수정 1·7 이 닿는 행의 **비고만** 덧씌운다 — 행선지·표적은 v2.2 와 같다(이동 0).
  수정 1: 시술 축 엣지의 끝 = 시술 튜플 — 참조 자리(R9/R12/R15/R16/R17/R18 target_label · from) 비고에 「끝 = procedure 튜플(§3 엣지 끝 규칙)」. pih procedure_ref 항목 id → 그 항목의 튜플.
  수정 7: taxonomy.json safety 잎 키 11 비고에 「R29 출처(v2.3)」.
COLMAP · MOVES(v1.1 → v2) · MOVES_V22(v2.1 → v2.2) · MOVES_V23(v2.2 → v2.3 = []) · NOTE_CHANGES_V23 · resolve 를 노출한다. erd_build_v23.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v22 as V22  # noqa

COLMAP = {f: list(rows) for f, rows in V22.COLMAP.items()}
MOVES = list(V22.MOVES)
MOVES_V22 = list(V22.MOVES_V22)
MOVES_V23 = []
NOTE_CHANGES_V23 = []


def _note(file, path, suffix):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            rows[i] = (path, r[1], r[2], (r[3] + " · " if r[3] else "") + suffix)
            NOTE_CHANGES_V23.append((file, path, r[2], suffix))
            return
    raise KeyError(f"{file} {path}")


_END = "v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드)"
_note("synergy.json", "links[].from", _END)
_note("synergy.json", "links[].to", _END)
_note("problem-packages.json", "problems[].complaints[].procedures[].name", _END)
_note("problem-packages.json", "problems[].complaints[].combos[].combo[]", _END)
_note("procedure-comparison.json", "comparisons[].procedures[].name", _END)
_note("treatment-optimization.json", "by_concern[].severity_levels[].optimal_combo[]", _END)
_note("treatment-optimization.json", "by_age_group[].recommended_base[]", _END)
_note("treatment-optimization.json", "by_age_group[].avoid[]", _END)
_note("treatment-optimization.json", "by_age_group[].upgrade[]", _END)
_note("treatment-optimization.json", "annual_plans[].schedule[].procedures[]", _END)
_note("treatment-sequence.json", "sequence_order[].categories[]", _END)
_note("treatment-sequence.json", "incompatible_same_day[].pair[]", _END)
_note("treatment-sequence.json", "minimum_intervals[].from", _END)
_note("treatment-sequence.json", "minimum_intervals[].to", _END)
_note("treatment-sequence.json", "common_combos[].sequence[]", _END)
_note("post-procedure-timeline.json", "timelines[].name", _END)
_note("pih-risk.json", "procedures[].procedure_ref", "v2.3: 항목 id(M8-1-1)는 그 항목의 procedure 튜플이 끝, 하위분류 id 는 subcategory, M 코드는 modality(§9.5.8)")
_note("post-procedure-timeline.json", "timelines[].category", "v2.3: 끝 깊이 그대로(M 코드 → modality · M16-DCA → subcategory) · timelines[].name 이 튜플로 해결되면 그 튜플")
_T = "taxonomy.json"
for p in ["modality[].extracted.safety.common[]", "modality[].extracted.safety.uncommon[]", "modality[].extracted.safety.serious[]",
          "modality[].subcategories[].items[].extracted.safety.common[]", "modality[].subcategories[].items[].extracted.safety.serious[]",
          "modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]", "modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]",
          "modality[].subcategories[].items[].extracted.safety.long_term[]",
          "modality[].products[].extracted.safety.common[]", "modality[].products[].extracted.safety.serious[]", "modality[].products[].extracted.safety.common_side_effects[]"]:
    _note(_T, p, "v2.3: R29 출처에 등재(수정 7)" + (" · R15 from = 항목의 procedure 튜플" if "items[]" in p else " · R15 from = product" if "products[]" in p else " · R15 from = modality"))
_note("complications.json", "categories[].complications[].name", "v2.3: 미등록 조각이 있는 이름은 raw_name 튜플(anchor = 원장 locator · 접히지 않음) · 경과는 사건에 바로 붙은 수식어만(§1.5)")


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
