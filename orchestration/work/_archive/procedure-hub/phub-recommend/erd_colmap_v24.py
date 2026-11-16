# -*- coding: utf-8 -*-
"""ERD v2.4 잎 키 행선지 규칙. v2.3(erd_colmap_v23.py) 위에 수정 1·2·3·6 이 닿는 행의 **비고만** 덧씌운다 — 행선지·표적은 v2.3 과 같다(이동 0).
  수정 1·2 (§1.5 부위 규칙 · raw_name 칸): complications name 비고.
  수정 3 (표현은 단위를 만들지 않는다): 표현 출처 잎 키 21(R29 출처 22 중 adverse_expression.text 출처) 비고에 「v2.4: R29 는 exact 만 · 새 단위 0」.
  수정 6 (site_id 출처): procedure.what_id 출처 이름·참조 키 19 비고에 「v2.4: procedure.site_id 출처(§2.5)」.
COLMAP · MOVES(v1.1 → v2) · MOVES_V22 · MOVES_V23 · MOVES_V24(= []) · NOTE_CHANGES_V24 · resolve 를 노출한다. erd_build_v24.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v23 as V23  # noqa
import erd_spec_v24 as S  # noqa

COLMAP = {f: list(rows) for f, rows in V23.COLMAP.items()}
MOVES = list(V23.MOVES)
MOVES_V22 = list(V23.MOVES_V22)
MOVES_V23 = list(V23.MOVES_V23)
MOVES_V24 = []
NOTE_CHANGES_V24 = []


def _note(file, path, suffix):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            rows[i] = (path, r[1], r[2], (r[3] + " · " if r[3] else "") + suffix)
            NOTE_CHANGES_V24.append((file, path, r[2], suffix))
            return
    raise KeyError(f"{file} {path}")


_note("complications.json", "categories[].complications[].name", "v2.4: 부위도 사건이 놓인 멤버 안의 조각만(원칙 C) · 후보 둘이면 튜플 둘(원칙 B) · raw_name(미등록 또는 붙지 않은 조각)은 site none · course 미상 · 사전 분해는 dict_tuples 보존(§1.5)")
_EXPR = "v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15)"
_x = next(e for e in S.ENTITIES if e["key"] == "adverse_expression")
EXPRESSION_TEXT_KEYS = list(next(a for a in _x["attrs"] if a[0] == "text")[3])
for k in EXPRESSION_TEXT_KEYS:
    f, p = k.split(":", 1)
    _note(f, p, _EXPR)
_SITE = "v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′)"
_p = next(e for e in S.ENTITIES if e["key"] == "procedure")
SITE_ID_KEYS = list(next(a for a in _p["attrs"] if a[0] == "site_id")[3])
for k in SITE_ID_KEYS:
    f, p = k.split(":", 1)
    _note(f, p, _SITE)


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
