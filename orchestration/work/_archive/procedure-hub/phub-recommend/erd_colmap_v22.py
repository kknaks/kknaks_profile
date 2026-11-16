# -*- coding: utf-8 -*-
"""ERD v2.2 잎 키 행선지 규칙. v2.1(= v2 · erd_colmap_v21.py) 위에 수정 5·6 이 닿는 행만 덧씌운다.
  수정 5: decision 공통 필드 개편 — decision.what 이 없어지고 원장 메모 원문은 decision.reason 으로(3 행 이동). reclassified_to · canonical_category 는 decision.new_value 그대로(비고만: kind별 구조체 필드).
  수정 6: complications duration · incidence 는 R15 엣지 속성으로만(비고만 — 행선지 그대로).
COLMAP · MOVES(v1.1 → v2 이동 표 · v2 그대로) · MOVES_V22(v2.1 → v2.2 이동 표) · resolve 를 노출한다. erd_build_v22.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v21 as V21  # noqa

COLMAP = {f: list(rows) for f, rows in V21.COLMAP.items()}
MOVES = list(V21.MOVES)
MOVES_V22 = []


def _replace(file, path, dest, target, note):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            if r[2] != target or r[1] != dest:
                MOVES_V22.append((file, path, f"{r[1]}:{r[2]}", f"{dest}:{target}"))
            rows[i] = (path, dest, target, note)
            return
    raise KeyError(f"{file} {path}")


_T = "taxonomy.json"
_I = "modality[].subcategories[].items[]."
_replace(_T, _I + "verification_needed", "개체", "decision.reason", "kind=verification_hold (질문 23) · v2.2: target={catalog_item_id} · new_value={hold:true} · 원문 = reason · decided_by=원장 작성자 · status=approved")
_replace(_T, _I + "classification_issue", "개체", "decision.reason", "kind=ledger_correction_note · v2.2: target={catalog_item_id} · new_value={note} · 원문 = reason")
_replace(_T, _I + "correction_note", "개체", "decision.reason", "kind=ledger_correction_note · v2.2: target={catalog_item_id} · new_value={note} · 원문 = reason")
_replace(_T, _I + "canonical_category", "개체", "decision.new_value", "kind=canonical_mapping (하위분류 사전 일치만) · v2.2: target={from_ref: CAT-id, scope: 항목} · new_value={to_id: SUB-id}")
_replace(_T, _I + "reclassified_to", "개체", "decision.new_value", "kind=reclassification → R2 재배치 · v2.2: target={catalog_item_id} · new_value={modality_id}")
_C = "complications.json"
_replace(_C, "categories[].complications[].duration", "엣지", "R15.duration", "v2.2: 엣지 속성으로만 — 경과(course) 칸을 정하지 않는다(§1.5 경과 규칙)")
_replace(_C, "categories[].complications[].incidence", "엣지", "R15.incidence", "v2.2: 엣지 속성으로만 — 경과(course) 칸을 정하지 않는다(§1.5 경과 규칙)")


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
