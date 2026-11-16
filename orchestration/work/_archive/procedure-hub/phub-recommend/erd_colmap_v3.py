# -*- coding: utf-8 -*-
"""ERD v3 잎 키 행선지 규칙. v2.4(erd_colmap_v24.py) 위에 V3-1~10 이 닿는 행의 **비고만** 덧씌운다 — 행선지·표적은 v2.4 와 같다(이동 0 · 잎 키 1,072 그대로 · 브론즈 2판은 이름 6곳만 바뀌어 잎 키 집합이 같다 — 검산 A).
  V3-1: complications name(수식 칸 qualifier · 사전 adverse_qualifier 출처) · 수식 출처 잎 키(consent emergency_signs · extracted/taxonomy safety.serious · anatomy vessels[].danger · filler_specific.primary_risk · critical_safety_facts.mechanism).
  V3-3·V3-4: 시술 축 참조 자리 잎 키 19(stopwords → qualifier_text · `+`/`/` 규칙 · 부위 여럿 → 튜플 여럿 · member_mode).
  V3-5: anatomy 층 정보 잎 키(safe_injection_depth · tissue_data.notes · clinical_pearls · vessels[].danger) · complications prevention · consent mandatory_disclosures → 사전 site(kind=layer) 출처.
  V3-2: taxonomy 항목 이름 · problem-combos products[] · extracted/taxonomy related_techniques[](회사 괄호 후보 자리).
  V3-8: procedure-profiles mechanism[] (R5 from 에 하위분류).
COLMAP · MOVES(v1.1 → v2) · MOVES_V22 · MOVES_V23 · MOVES_V24 · MOVES_V3(= []) · NOTE_CHANGES_V3 · resolve 를 노출한다. erd_build_v3.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v24 as V24  # noqa
import erd_spec_v3 as S  # noqa

COLMAP = {f: list(rows) for f, rows in V24.COLMAP.items()}
MOVES = list(V24.MOVES)
MOVES_V22 = list(V24.MOVES_V22)
MOVES_V23 = list(V24.MOVES_V23)
MOVES_V24 = list(V24.MOVES_V24)
MOVES_V3 = []
NOTE_CHANGES_V3 = []


def _note(file, path, suffix):
    rows = COLMAP[file]
    for i, r in enumerate(rows):
        if isinstance(r[0], str) and r[0] == path:
            rows[i] = (path, r[1], r[2], (r[3] + " · " if r[3] else "") + suffix)
            NOTE_CHANGES_V3.append((file, path, r[2], suffix))
            return
    for r in rows:
        if not isinstance(r[0], str) and r[0].match(path):
            # 정규식 행이 받던 잎 키 — 그 행선지·표적 그대로 명시 행을 앞에 둔다(다른 잎 키의 비고는 그대로)
            rows.insert(0, (path, r[1], r[2], (r[3] + " · " if r[3] else "") + suffix))
            NOTE_CHANGES_V3.append((file, path, r[2], suffix))
            return
    raise KeyError(f"{file} {path}")


# V3-1 — 수식 칸 · 수식 사전 출처
_note("complications.json", "categories[].complications[].name", "v3(V3-1): 튜플 (event, site, course, qualifier?) — 수식 조각은 같은 멤버 안에서만 · 「공기색전」→ (색전, none, 미상, 공기) · (V3-5) site 에 layer 값 가능")
QUALIFIER_SOURCE_KEYS = []
for canon, kind, src, syns, note in S.ADVERSE_QUALIFIERS:
    for f, p in [src] + [ss for _, ss in syns] + S.ADVERSE_QUALIFIER_EXTRA_SOURCES.get(canon, []):
        k = f"{f}:{p}"
        if k not in QUALIFIER_SOURCE_KEYS:
            QUALIFIER_SOURCE_KEYS.append(k)
for k in QUALIFIER_SOURCE_KEYS:
    f, p = k.split(":", 1)
    if (f, p) == ("complications.json", "categories[].complications[].name"):
        continue
    _note(f, p, "v3(V3-1): 사전 adverse_qualifier 값 출처(derived)")

# V3-5 — 조직층 값 출처
LAYER_SOURCE_KEYS = []
for canon, src, syns, note in S.SITE_LAYERS:
    for f, p in [src] + [ss for _, ss in syns] + S.SITE_LAYER_EXTRA_SOURCES.get(canon, []):
        k = f"{f}:{p}"
        if k not in LAYER_SOURCE_KEYS:
            LAYER_SOURCE_KEYS.append(k)
for k in LAYER_SOURCE_KEYS:
    f, p = k.split(":", 1)
    if (f, p) == ("complications.json", "categories[].complications[].name"):
        continue
    _note(f, p, "v3(V3-5): 사전 site 조직층(kind=layer) 값 출처(derived)")

# V3-3 · V3-4 — 시술 축 참조 자리 19
_p = next(e for e in S.ENTITIES if e["key"] == "procedure")
REF_KEYS = list(next(a for a in _p["attrs"] if a[0] == "what_id")[3])
_REF = "v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and)"
for k in REF_KEYS:
    f, p = k.split(":", 1)
    _note(f, p, _REF + (" · (V3-2) 괄호 안 회사·제품 규칙 후보 자리(「보톡스(엘러간)」)" if k == "taxonomy.json:modality[].subcategories[].items[].name" else ""))

# V3-2 — 회사 괄호 후보 자리(참조 자리 밖 · 속성)
_note("problem-combos.json", "combos[].packages[].products[]", "v3(V3-2): 「보톡스(엘러간)」 7곳 — 합성 문장(속성 · 분해 대상 아님)이지만 회사 괄호 규칙의 후보 자리로 §9.5.9 에 실측")
_note("extracted.json", "{code}.related_techniques[]", "v3(V3-2): 「메조보톡스 (더모톡신)」 — 설명 문장(속성) · 회사 괄호 후보 자리 실측 §9.5.9")
_note("taxonomy.json", "modality[].extracted.related_techniques[]", "v3(V3-2): 「메조보톡스 (더모톡신)」 — 설명 문장(속성) · 회사 괄호 후보 자리 실측 §9.5.9")
_note("products.json", "botulinum_toxin.products[].manufacturer", "v3(V3-2): 회사 괄호 규칙의 제품→회사 지도(제조사)")
_note("taxonomy.json", "modality[].products[].manufacturer", "v3(V3-2): 회사 괄호 규칙의 제품→회사 지도(제조사)")

# V3-8 — R5 from 하위분류
_note("procedure-profiles.json", "profiles[].mechanism[]", "v3(V3-8): R5 from = modality|modality_subcategory — 하위분류 단위 기본 기법은 canonical_mapping 결정으로만(basis)")


def resolve(file, path):
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
