# -*- coding: utf-8 -*-
"""ERD v2.1 명세 (데이터). erd_spec_v2.py(v2) 를 읽어 **시술 튜플 접힘 규칙 하나**만 덧씌운다 (발주서 erd-v2.1-brief.md).
  - 이름 조각이 전부 사전에 닿았을 때만 what/site/technique 를 사전 값으로 조립 → 그때만 접힘
  - 하나라도 미등록이면 what = 그 분류 항목 자신(what_kind=catalog_item · candidate_name 보존) · 접지 않음
  - 부모 하위분류 fallback 삭제(fallback_to_parent=false) · 참조(②③)는 미등록 조각 있으면 미해결(⑨)
구조(개체 21 · 관계 31 · 사전 46 · 행선지)는 v2 그대로. erd_build_v21.py 가 읽는다. v2 명세는 손대지 않는다.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v2 as V2  # noqa

ERD_VERSION = "v2.1"
SNAPSHOT = V2.SNAPSHOT
LEDGER_DIR = V2.LEDGER_DIR
STEP1_FILE = V2.STEP1_FILE
STEP1_TIER2_SOURCE_RE = V2.STEP1_TIER2_SOURCE_RE
SOURCE_FILES = list(V2.SOURCE_FILES)
SOURCE_KIND = dict(V2.SOURCE_KIND)
TRUST_FLAGS = dict(V2.TRUST_FLAGS)
NORMALIZE_RULE = copy.deepcopy(V2.NORMALIZE_RULE)
ID_RULE = copy.deepcopy(V2.ID_RULE)
ID_RULE["procedure"] = ("PRC-<sha256(what_id|site_id|technique_id)[:10]>. what_id = MOD-/SUB-/PRD- 개체 id 또는 (v2.1) CAT- 분류 항목 id(what_kind=catalog_item · 이름 조각에 미등록이 있거나 primary 조각이 없는 항목은 항목 자신이 what), "
                        "site_id = site 개체 id 또는 'none', technique_id = 기법 사전 id 또는 'none'. 같은 튜플 = 같은 시술. CAT- 기반 튜플은 항목마다 고유하므로 다른 항목과 접히지 않는다")
QUALITY_RULES = list(V2.QUALITY_RULES)
Q25 = list(V2.Q25)
DISPOSITIONS = dict(V2.DISPOSITIONS)
SITE_LABELS_KEEP = list(V2.SITE_LABELS_KEEP)
Q14_ORAL_DRUGS = list(V2.Q14_ORAL_DRUGS)

# ---------------------------------------------------------------------------
# 분해 규칙 — v2 그대로 + 규칙 5: fallback_to_parent 명시 + what 결정(분류 항목) 교체
# ---------------------------------------------------------------------------
RESOLVE_RULES = copy.deepcopy(V2.RESOLVE_RULES)
RESOLVE_RULES["name"] = "decompose_v2_1"
RESOLVE_RULES["step3_assemble"]["fallback_to_parent"] = False
RESOLVE_RULES["step3_assemble"]["fallback_to_parent_note"] = ("v2.1: 분류 항목 이름의 조각이 하나라도 사전에 없으면 부모 하위분류로 떨어뜨리지 않는다(접힘 금지). what = 그 분류 항목 자신(what_kind=catalog_item). "
                                                             "참조 자리(②)·market-pricing(③)도 같다 — 미등록 조각이 있으면 그 참조는 unresolved(⑨)이며 부모 층 튜플로 접지 않는다")
RESOLVE_RULES["step3_assemble"]["unresolved"] += ". v2.1: 미해결 참조는 procedure 튜플을 만들지 않는다(힌트 계열·부모 층으로 접지 않음)"

# ---------------------------------------------------------------------------
# 개체 — 구조 그대로(21). procedure 의 what 정의·속성만 갱신
# ---------------------------------------------------------------------------
ENTITIES = copy.deepcopy(V2.ENTITIES)


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


_p = _ent("procedure")
_p["definition"] = ("**단위 시술 = 튜플 (what, site, technique)** — 무엇을 × 어디에 × 어떻게. what = modality | modality_subcategory | product (사전 값) 또는 (v2.1) catalog_item(분류 항목 자신). "
                    "**분류 항목의 이름 조각이 전부 사전에 닿았을 때만** what/site/technique 를 사전 값으로 조립하고 그때만 다른 항목과 접힌다. 조각 중 하나라도 미등록이면 접지 않는다 — what = 그 분류 항목 자신(what_kind=catalog_item, 미등록 조각은 candidate_name 으로 보존), "
                    "site/technique 는 닿은 조각만(technique 는 §1.4 그대로 R5 계열 상속 허용), 상태 partial. 조각이 전부 닿았어도 primary(제품·하위분류·사전 값 what 의 분류 항목) 조각이 없으면(부위만·계열명만) 역시 항목 자신. 부모 하위분류로 떨어뜨리는 fallback 은 없다(fallback_to_parent=false) — 하위분류는 R2 상위 관계로만. "
                    "site = 부위 사전 값 | none(부위 미상 · 사전에 없는 조각은 미등록 조각 기록 + none). technique = 기법 사전 값 | 계열 기본값 상속(R5, 기법이 하나인 계열만) | none. "
                    "원천: ① 분류 항목 521 의 분해(§1.4) ② 자유 텍스트 참조(§9.2 자리 전부)의 분해 ③ market-pricing 메뉴 122 — ②③은 미등록 조각이 있으면 미해결(⑨)로 두고 튜플을 만들지 않는다. "
                    "같은 튜플 = 같은 시술이며 여러 분류 항목이 같은 튜플이면 R26 derived_from(1:N) 으로 매단다. 조합 기호(+·/)로 같은 묶음 안에 멤버(primary 조각)가 둘 이상이면 시술이 아니라 package(kind=combo_ref) 로 보내고 멤버 각각을 튜플화한다.")
_p["identity"] = "sha256(what_id|site_id|technique_id)[:10] — 튜플 자체가 식별자 (what_id 가 CAT- 이면 항목마다 고유)"
_attrs = []
for a in _p["attrs"]:
    if a[0] == "what_kind":
        a = ("what_kind", "enum(modality|modality_subcategory|product|catalog_item)", True, [], "무엇을. §1.4 what 규칙(조각 전부 사전 값일 때 제품 > 하위분류 > 계열 · 미등록 조각 있거나 primary 없으면 catalog_item = 항목 자신)")
    elif a[0] == "what_id":
        a = ("what_id", "str", True, a[3], "MOD-/SUB-/PRD-/CAT- 개체 id (R27). 출처 = 튜플을 만든 이름·참조 자리")
    elif a[0] == "status":
        a = ("status", "enum(complete|partial)", True, [], "complete = 이 튜플을 만든 모든 이름이 미등록 조각 0 · partial = 하나라도 미등록 조각 있음. v2.1: partial 은 what_kind=catalog_item 뿐(사전 값 what 튜플은 전부 complete)")
    _attrs.append(a)
    if a[0] == "what_id":
        _attrs.append(("candidate_name", "str[]", False, ["taxonomy.json:modality[].subcategories[].items[].name"], "v2.1: what_kind=catalog_item 일 때 이름 분해에서 어느 사전에도 닿지 않은 조각(제품명·기법·부위 후보). 사전 추가는 실버 빌드의 결정 묶음 — 보존만"))
_p["attrs"] = _attrs
_ent("catalog_item")["definition"] += " v2.1: 이름 조각에 미등록이 있거나 primary 조각이 없는 항목은 그 항목 자신이 튜플의 what(what_kind=catalog_item)이며 다른 항목과 접히지 않는다(부모 하위분류 fallback 삭제)."

# ---------------------------------------------------------------------------
# 관계 — 구조 그대로(31). R26·R27 비고만 갱신
# ---------------------------------------------------------------------------
RELATIONS = copy.deepcopy(V2.RELATIONS)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


_rel("R26")["note"] = "분류 항목 하나 → 튜플 하나. 여러 항목이 같은 튜플이면 같은 procedure 에 N 엣지(접힘). v2.1: 접힘은 세 칸 전부 사전 값일 때만 — what 이 CAT-(항목 자신)인 튜플은 1:1. §9.5 접힌 표"
_rel("R27").update({"to": "modality|modality_subcategory|product|catalog_item", "note": "튜플의 what 축. §1.4 what 규칙. v2.1: 미등록 조각이 있거나 primary 조각이 없는 분류 항목은 what=catalog_item(항목 자신)"})
_rel("R27")["attrs"] = [("what_kind", "enum(modality|modality_subcategory|product|catalog_item)", "")]

ERD_ENUMS = copy.deepcopy(V2.ERD_ENUMS)
ERD_ENUMS["procedure.what_kind"] = ["modality", "modality_subcategory", "product", "catalog_item"]

ADVERSE_EVENT_TYPES = list(V2.ADVERSE_EVENT_TYPES)
ADVERSE_EVENT_CATEGORIES = list(V2.ADVERSE_EVENT_CATEGORIES)
ADVERSE_EVENT_CATEGORY_REVIEW = list(V2.ADVERSE_EVENT_CATEGORY_REVIEW)
COURSES = list(V2.COURSES)
RELATIVE_SITES = list(V2.RELATIVE_SITES)

# ---------------------------------------------------------------------------
# 튜플 규칙 v2.1 (데이터) — erd-v2.1-tuples.py 가 그대로 실행. what 결정 부분만 교체
# ---------------------------------------------------------------------------
TUPLE_RULES = copy.deepcopy(V2.TUPLE_RULES)
TUPLE_RULES["name"] = "tuples_v2_1"
_P = TUPLE_RULES["procedure"]
_P["fallback_to_parent"] = False
_P["what"] = [
    "접힘 조건(v2.1): 이름 조각이 **전부** 사전(제품 · 하위분류 라벨 · 사전 값 what 을 가진 분류 항목 · 부위 · 기법 · 규격 · product_tier · 계열)에 닿았을 때만 what/site/technique 를 사전 값으로 조립하고, 그때만 다른 항목과 접힐 수 있다",
    "product 조각(계열 안 우선, 없으면 전 계열) → what=product",
    "catalog_item 조각 → 그 항목의 튜플 what(분류 항목은 먼저 전부 튜플화). 분류 항목(①)에서는 그 항목의 what 이 사전 값(product|modality_subcategory|modality)일 때만 — 항목 자신(catalog_item)이 what 인 항목에 닿은 조각은 what 으로 쓰지 않는다",
    "modality_subcategory 조각 → what=modality_subcategory",
    "modality 조각 또는 자리 힌트의 계열 → what=modality (참조 ②③). 분류 항목(①)에서 계열 조각은 what 이 아니다(extra 로 기록)",
    "분류 항목(①)의 what: 조각 중 하나라도 미등록이면 **접지 않는다** — what = 그 분류 항목 자신(what_kind=catalog_item · what_id=CAT- · 미등록 조각은 candidate_name), site/technique 는 닿은 조각만(technique 는 아래 technique 규칙대로 R5 상속 허용), 상태 partial. 조각이 전부 닿았어도 primary 가 없으면(부위만·계열명만·항목 자신이 what 인 항목만) 역시 항목 자신(status complete)",
    "부모 하위분류로 떨어뜨리는 fallback 은 없다(fallback_to_parent=false). 하위분류는 항목의 상위 관계(R2)로만 남는다",
    "primary 가 여럿이고 조합이 아니면 각 조각의 최종 what 종류로 product > modality_subcategory > modality 순(분류 항목 조각은 그 항목의 what 종류로 비교), 같은 종류면 텍스트 순서. 나머지는 extra_primaries 로 기록",
    "조각이 계열 사전과 제품 색인 양쪽에 닿으면(보톡스·필러처럼 계열명이 제품명인 경우) what 은 product",
    "참조 ②③: 미등록 조각이 하나라도 있으면 그 참조는 미해결(v1.1 ⑨)이며 튜플을 만들지 않는다(힌트 계열·부모 층 튜플로 접지 않음). primary 도 힌트도 없으면 튜플 불가",
]
_P["fragments"] = ("v2.1: 먼저 v1.1 3단계 (a) **통째 일치**를 본다 — 라벨(또는 분류 항목 이름, 자기 이름 제외) 전체가 하나의 사전 값(계열·제품·하위분류 라벨·분류 항목 이름)이면 조각 하나(괄호·조합 기호가 값 안에 있어도 쪼개지 않는다 · 「PRP/자가혈」「마이크로니들링(MTS)」「리쥬란 HB+」). "
                   "아니면 " + _P["fragments"])
_P["status"] = "complete = 미등록 조각 0 · partial = 미등록 조각 ≥1 (분류 항목은 둘 다 튜플을 만들되 partial 은 항목 자신이 what · 참조는 partial 이면 미해결)"
_P["id"] = "PRC-sha256(what_id|site_id|technique_id)[:10] · what_id ∈ {MOD-, SUB-, PRD-, CAT-}"
