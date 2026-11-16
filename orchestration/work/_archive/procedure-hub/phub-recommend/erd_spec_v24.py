# -*- coding: utf-8 -*-
"""ERD v2.4 명세 (데이터). erd_spec_v23.py(v2.3) 를 읽어 3차 독립 검토(erd-v2.3-review.md ⑥) 반영 수정 6건만 덧씌운다 (발주서 erd-v2.4-brief.md).
  1. (2-A′) 부작용 site 는 원칙 C — 사건이 놓인 멤버 안의 부위 조각만 · 부위 후보 둘이면 원칙 B 로 튜플 둘 · 붙지 않은 부위 조각은 extra_sites 에 보존하고 접지 않는다 (§1.5)
  2. (2-B′) raw_name 튜플에는 course·site 를 주지 않는다 — 둘 다 none/미상 · 사전 분해는 dict_tuples 에 보존 (§1.5)
  3. (2-C′) 표현은 단위를 만들지 않는다(원칙 D) — 기존 단위(complications 65 이름 유래 사전 튜플)와 세 칸 완전 일치할 때만 R29(match_status=exact) · 아니면 unlinked + candidates (§1.5 · §2.14 · §2.15 · R29)
  4. (3-A′) adverse_tuple_assign 대상 = raw_name 튜플 전부 · 표현 레코드 전부(exact 포함) (§5.2)
  5. (3-B′) CAT- 의 「계열 코드」 = taxonomy 트리 위치(원장 modality[].id · reclassification 적용 전) — reclassification 은 R2 만 바꾼다 (§1.4 · §2.3 · §2.4 · §5.2)
  6. (3-C′) procedure.site_id 출처 = what_id 와 같은 이름·참조 키 19 · adverse_effect.site_ref_* 출처 = complications 이름 키 (§2.5 · §2.14)
구조(개체 21 · 관계 31 · 사전 46 · 값)는 v2.3 그대로. erd_build_v24.py 가 읽는다. v2.3 명세는 손대지 않는다.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v23 as V23  # noqa

ERD_VERSION = "v2.4"
SNAPSHOT = V23.SNAPSHOT
LEDGER_DIR = V23.LEDGER_DIR
STEP1_FILE = V23.STEP1_FILE
STEP1_TIER2_SOURCE_RE = V23.STEP1_TIER2_SOURCE_RE
SOURCE_FILES = list(V23.SOURCE_FILES)
SOURCE_KIND = dict(V23.SOURCE_KIND)
TRUST_FLAGS = dict(V23.TRUST_FLAGS)
NORMALIZE_RULE = copy.deepcopy(V23.NORMALIZE_RULE)
Q25 = list(V23.Q25)
DISPOSITIONS = dict(V23.DISPOSITIONS)
SITE_LABELS_KEEP = list(V23.SITE_LABELS_KEEP)
Q14_ORAL_DRUGS = list(V23.Q14_ORAL_DRUGS)
ADVERSE_EVENT_TYPES = list(V23.ADVERSE_EVENT_TYPES)
ADVERSE_EVENT_CATEGORIES = list(V23.ADVERSE_EVENT_CATEGORIES)
ADVERSE_EVENT_CATEGORY_REVIEW = list(V23.ADVERSE_EVENT_CATEGORY_REVIEW)
RELATIVE_SITES = list(V23.RELATIVE_SITES)
COURSES = list(V23.COURSES)
COURSE_DROPPED = list(V23.COURSE_DROPPED)
FOLD_CONDITION = V23.FOLD_CONDITION
FOLD_RULE = V23.FOLD_RULE
RULE4 = V23.RULE4
DECISION_COMMON_FIELDS = list(V23.DECISION_COMMON_FIELDS)
DECISION_STATUS = list(V23.DECISION_STATUS)
DECISION_BUILD_RULE = V23.DECISION_BUILD_RULE
EDGE_END_RULE = V23.EDGE_END_RULE
EDGE_END_KINDS = list(V23.EDGE_END_KINDS)
TARGET_DEPTH = list(V23.TARGET_DEPTH)
COURSE_RULE = V23.COURSE_RULE
LOCATOR_RULE = V23.LOCATOR_RULE
DECISION_APPLY_ORDER = list(V23.DECISION_APPLY_ORDER)
DECISION_APPLY_ORDER_RULE = V23.DECISION_APPLY_ORDER_RULE
DECISION_KINDS_NEW = list(V23.DECISION_KINDS_NEW)
DECISION_KINDS_NEW_V23 = list(V23.DECISION_KINDS_NEW_V23)
DECISION_KINDS_RESHAPED_V23 = dict(V23.DECISION_KINDS_RESHAPED_V23)
PROC_AXIS_EDGES = list(V23.PROC_AXIS_EDGES)
R29_TAXONOMY_SAFETY_KEYS = list(V23.R29_TAXONOMY_SAFETY_KEYS)

# ---------------------------------------------------------------------------
# 원칙 A~D (발주서 문장 그대로 · 시술 쪽 v2.1~v2.3 과 동일하게 부작용 쪽에 적용)
# ---------------------------------------------------------------------------
PRINCIPLES = [
    ("A", "미상 칸이 하나라도 있으면 다른 이름과 접지 않는다."),
    ("B", "조각을 버리지 않는다. 한 칸에 후보가 둘이면 단위를 둘로 나누거나(부위 「이마/눈가」→ 둘) 미해결로 둔다."),
    ("C", "수식어(경과·부위)는 **같은 멤버 안에서 바로 붙은 사건**에만 준다. 이름 전체에서 끌어오지 않는다."),
    ("D", "표현(adverse_expression)은 단위를 **가리키기만** 한다. 표현에서 새 단위를 만들지 않는다."),
]
PRINCIPLES_TEXT = " · ".join(f"{k}. {v}" for k, v in PRINCIPLES)

# ---------------------------------------------------------------------------
# 수정 1 — 부위 규칙 (§1.5 · 2-A′)
# ---------------------------------------------------------------------------
SITE_RULE = ("부위(site)는 원칙 C — **사건이 놓인 멤버(조합 기호 `· / , + 및 또는 — -- :` 로 나뉜 조각) 안의 부위 조각(부위 사전 21 · 상대 부위 사전)만** 그 사건의 부위다. 멤버 밖(같은 묶음 · 바깥 묶음 · 이름 전체)에서 가져오지 않는다 — v2.3 의 「멤버 → 같은 묶음 → outer 묶음 → 이름 전체 유일값」 순서는 없앴다(「주사 부위 반응 (부종·압통)」의 바깥 부위는 괄호 안 사건에 붙지 않는다). "
             "부위 조각만으로 된 멤버(사건·경과·미등록 조각 0)가 같은 묶음 안에서 사건 멤버 **바로 앞**에 있으면 그 멤버와 한 멤버로 읽는다(부위 나열 — 「이마/눈가 당김감」= 부위 후보 {이마, 눈가} × 당김감). "
             "한 멤버에 부위 후보가 둘 이상이면 원칙 B — 버리지 않고 **부위마다 튜플**(당김감×이마 + 당김감×눈가). 경과 후보가 둘 이상이어도 같은 방식(경과마다). "
             "사건에 붙지 않은 부위·경과 조각(사건 없는 멤버 · 괄호 안 부위 나열 「혈관 폐색(미간·코)」)은 버리지 않고 **extra_sites · extra_courses 에 보존**하며, 그 문자열은 접지 않는다 — complications 이름이면 raw_name 튜플(anchor=locator), 표현이면 match_status=unlinked(adverse_tuple_assign 의 대상). 없으면 site=none, course=미상(축의 정의값 · 검토 2-D 는 §12). "
             "실측 §9.6.2b: 멤버 밖에서 온 site 0 · 「두통 × 주사 부위」 0 · 부위 나열 합치기 전부 · 나눈 단위 전부 · 보존한 조각 전부.")

# ---------------------------------------------------------------------------
# 수정 2 — raw_name 튜플의 칸 (§1.5 · 2-B′)
# ---------------------------------------------------------------------------
RAW_NAME_RULE = ("complications 이름에 미등록 조각이 하나라도 있거나(partial) 사건에 붙지 않은 부위·경과 조각이 남으면(unresolved): 이름마다 고유한 튜플 하나(event_kind=raw_name · event=이름 원문 · anchor=원장 locator · candidate_name=미등록 조각). "
                 "**raw_name 튜플에는 course·site 를 주지 않는다 — site=none · course=미상(둘 다 미상 · 식별자 RAW:anchor 만으로 고유).** 이름 전체에서 조각이 하나라고 그 칸에 넣지 않는다(v2.3 의 「닿은 조각이 하나씩일 때만 그 칸」 삭제 — 「통증·불편감 및 지연성 통증(LOP)」의 raw 칸은 지연이 아니라 미상). "
                 "§1.5 경과·부위 규칙으로 분해한 결과는 dict_tuples(사건, 부위, 경과)·event_fragments·extra_sites·extra_courses 에 **보존만** 한다(adverse_tuple_assign 의 재료 · 튜플 칸이 아니다). 같은 이름이 여러 사건 조각을 가져도 튜플은 하나다. 실측 §9.6.2c: raw 튜플 site none 100% · course 미상 100%.")

# ---------------------------------------------------------------------------
# 수정 3 — 표현은 단위를 만들지 않는다 (§1.5 · §2.14 · §2.15 · R29 · 2-C′)
# ---------------------------------------------------------------------------
EXPRESSION_RULE = ("표현(adverse_expression)은 원칙 D — 단위를 **가리키기만** 한다. 기존 단위 = complications 65 이름에서 §1.5 로 생긴 사전 튜플(event_kind=dict)뿐이다. "
                   "표현을 §1.5 와 같은 규칙으로 분해한 결과(candidates — (event, site, course) 후보 전부)가 **미등록 조각 0 · 사건에 붙지 않은 조각 0 · 후보 전부가 기존 단위와 세 칸 완전 일치**할 때만 R29 로 연결한다(match_status=exact · 후보마다 엣지 하나). "
                   "하나라도 아니면 연결하지 않는다(match_status=unlinked · 사유 unregistered | unattached_fragments | no_unit | no_event) — 표현 레코드에 candidates(후보 세 칸 · 기존 단위 존재 여부 · would_be_id)를 보존해 adverse_tuple_assign(kind=expression)의 재료로 둔다. "
                   "**표현에서 새 단위를 만들지 않는다 — raw_name 튜플도 사전 튜플도**(v2.3 「표현이 만든 사전 튜플은 v2 그대로」 삭제 — 65 에 없던 새 튜플 57 → 0 · partial 인데 연결 0). 문헌 레코드는 statement 와 patient_ko 두 쪽 전부 exact 일 때만 exact. 실측 §9.6.3·§9.6.4.")

ADVERSE_FOLD_RULE = ("부작용 접힘 조건(v2.3 · 검토 2-B · 시술과 같은 원칙): **세 칸 전부 사전 값일 때만** 다른 이름과 접힌다 — 이름의 조각이 전부 사전(사건 · 부위 · 상대 부위 · 경과)에 닿아 미등록 조각이 0 이고 event 가 사건 사전 값일 때. "
                     "부작용 축의 site none · course 미상은 v2 그대로 축의 정의값이라 사전 값으로 센다(검토 2-D 「none·미상을 식별자 값으로 둘지」는 동결 후 scope_review — §12). "
                     "complications 이름에 **미등록 조각이 하나라도 있으면 접지 않는다**(v2.4: 사건에 붙지 않은 부위·경과 조각이 남아도 접지 않는다 — 원칙 A·B): 그 이름은 항목별 고유 튜플(event_kind=raw_name · event=이름 원문 · anchor=그 이름의 원장 locator · candidate_name=미등록 조각 · site=none · course=미상 · 사전 분해 결과는 dict_tuples·event_fragments·extra_* 에 실값 보존)이며 식별자에 anchor 가 들어가 다른 이름과 접히지 않는다. "
                     "표현(adverse_expression)은 정체성을 만들지 않는다 — 단위를 가리키기만 한다(원칙 D · v2.4): 기존 단위와 세 칸 완전 일치할 때만 R29(match_status=exact), 아니면 unlinked + candidates. 표현이 raw_name 튜플도 사전 튜플도 만들지 않는다")
ID_RULE = copy.deepcopy(V23.ID_RULE)
ID_RULE["adverse_effect"] = ("세 칸 전부 사전 값이면(미등록 조각 0 · 붙지 않은 조각 0 · event_kind=dict) ADV-<sha256(event_id|site_id|course_id)[:10]>, raw_name 튜플(event_kind=raw_name)은 ADV-<sha256(RAW:<anchor>|none|<course_id(미상)>|<anchor>)[:10]> — "
                             "event_id = 사건 사전 id, site_id = site 개체 id | 상대 부위 사전 id | 'none', course_id = 경과 사전 id('미상' 포함), anchor = 그 이름의 원장 locator. v2.4: raw_name 의 site·course 칸은 항상 none·미상(2-B′). 튜플은 complications 65 이름에서만 생긴다(표현은 가리키기만 · 2-C′)")
CAT_FAMILY_RULE = ("CAT- 식별자의 「계열 코드」 = **taxonomy 트리 위치**(원장 `taxonomy.json:modality[].id` — 그 항목이 적힌 계열 · reclassification 메모 적용 전). reclassification(reclassified_to · 적용 ⓪)은 R2(하위분류 → 항목) 재배치만 바꾸고 CAT- id 는 바꾸지 않는다 — "
                   "소프라노 티타늄 = sha256(`M9|소프라노티타늄`) 그대로(M9 → M8 재배치 뒤에도) · 볼뉴머 M4/M9 는 각각의 트리 위치로 서로 다른 CAT-. 결정·R26·anchor 튜플 id 가 가리키는 CAT- 는 다른 결정 뒤에도 바뀌지 않는다(검토 3-B′)")
ID_RULE["catalog_item"] = V23.ID_RULE["catalog_item"] + ". v2.4: " + CAT_FAMILY_RULE
ID_RULE["adverse_expression_candidates"] = "표현 레코드의 candidates[] = (event, site, course) 후보 + would_be_id(ADV-sha256(event_id|site_id|course_id) — 단위가 있으면 그 id, 없으면 「있었다면」 id) + exists. 튜플이 아니다(원칙 D)"

# ---------------------------------------------------------------------------
# 수정 4 — adverse_tuple_assign 대상 범위 (§5.2 · 3-A′) · 수정 5 — reclassification 비고 (§5.2 · 3-B′)
# ---------------------------------------------------------------------------
DECISION_KINDS = []
for k, br, t, nv, n in V23.DECISION_KINDS:
    if k == "adverse_tuple_assign":
        t = "obj(locator: 원장 locator — complications 이름(raw_name 튜플의 anchor) 또는 표현(adverse_expression) 레코드의 locator, kind: raw_name|expression)"
        n = ("부작용 원천에 (사건, 부위, 경과) 튜플을 사람이 지정한다. **대상 = raw_name 튜플 전부(미등록 조각 · 붙지 않은 조각) · 표현 레코드 전부(exact 포함 — linked 인데 틀리거나 조각을 잃은 표현도 · v2.4 3-A′)** · partial/unlinked 만이 아니다. "
             "예 「카테터 관련 감염」→ 감염×카테터 · 「구형구축 (…섬유성 결절)」→ 구형구축만 · 「이마/눈가 당김감」의 후보 둘 확인. raw_name 튜플은 지정 튜플로 대체되고 locator 가 출처로 남는다 · 표현은 R29 를 지정 튜플로(candidates 가 재료 · 지정 튜플이 기존 단위에 없으면 지정이 단위를 세운다 — 결정으로만). 적용 ③")
    elif k == "reclassification":
        n = n + ". v2.4: CAT- 의 계열 코드는 taxonomy 트리 위치(원장)로 고정 — 이 결정은 R2 만 바꾸고 CAT- id 를 바꾸지 않는다(3-B′ · §2.4)"
    DECISION_KINDS.append((k, br, t, nv, n))
DECISION_TARGET_RULE = ID_RULE["decision_target"] + ". v2.4: CAT- 는 taxonomy 트리 위치의 계열 코드로 고정(reclassification 뒤에도 같다 · §2.4)"

# ---------------------------------------------------------------------------
# 분해 규칙 (참조 §1.3 — v2.3 그대로)
# ---------------------------------------------------------------------------
RESOLVE_RULES = copy.deepcopy(V23.RESOLVE_RULES)
RESOLVE_RULES["name"] = "decompose_v2_4"

# ---------------------------------------------------------------------------
# 개체 — 구조 그대로(21)
# ---------------------------------------------------------------------------
ENTITIES = copy.deepcopy(V23.ENTITIES)


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


# 수정 5 — §2.3 · §2.4 계열 코드 고정
_sub = _ent("modality_subcategory")
_sub["definition"] += " v2.4: 분류 항목(CAT-)의 「계열 코드」는 이 하위분류가 놓인 taxonomy 트리 위치의 계열(modality[].id)이며, reclassification(reclassified_to)은 R2 재배치만 바꾸고 CAT- id 를 바꾸지 않는다(§2.4 · 3-B′)."
_cat = _ent("catalog_item")
_cat["identity"] = "계열 코드 + 정규화 항목 이름 (v1.1 procedure 와 같음) — v2.4: " + CAT_FAMILY_RULE
_cat["definition"] += " v2.4: 식별자의 계열 코드 = taxonomy 트리 위치(원장 · reclassification 적용 전) 고정(3-B′)."

# 수정 6 — §2.5 procedure.site_id 출처 = what_id 와 같은 이름·참조 키 19
_p = _ent("procedure")
_SRC_REFS = next(a for a in _p["attrs"] if a[0] == "what_id")[3]
_attrs = []
for a in _p["attrs"]:
    if a[0] == "site_id":
        a = ("site_id", a[1], a[2], list(_SRC_REFS), "site 개체 id 또는 none (R28). 부위 사전 21(v1.1 그대로, 공유 사전). v2.4: 출처는 이름·참조 자리의 키(what_id 와 같은 19 — 부위 조각은 그 문자열에서 읽는다 · 3-C′) · 사전은 §4 site")
    _attrs.append(a)
_p["attrs"] = _attrs

# 수정 1·2·3 — adverse_effect
_a = _ent("adverse_effect")
_a["definition"] = (_a["definition"].split(" v2.3: ")[0] + " v2.4(원칙 A~D · §1.5): " + ADVERSE_FOLD_RULE + ". 경과·부위는 사건이 놓인 멤버 안의 수식어만(원칙 C) · 한 칸에 후보가 둘이면 튜플 둘(원칙 B) · raw_name 의 칸은 none/미상(2-B′) · 표현은 단위를 만들지 않는다(원칙 D · 2-C′).")
_a["identity"] = "sha256(event_id|site_id|course_id)[:10] — 세 칸 전부 사전 값일 때. raw_name 튜플(미등록 조각 또는 붙지 않은 조각)은 sha256(RAW:anchor|none|미상 id|anchor) — 이름마다 고유(접히지 않음 · 칸은 none/미상)"
_COMP_NAME = ["complications.json:categories[].complications[].name"]
_aattrs = []
for a in _a["attrs"]:
    n = a[0]
    if n == "event_kind":
        a = (n, a[1], True, [], "dict = 사건 사전 값(세 칸 전부 사전 값 — 접힘 가능 · complications 65 이름 유래만) · raw_name = complications 이름에 미등록 조각이 있거나(partial) 사건에 붙지 않은 부위·경과 조각이 남아(unresolved · v2.4) 이름 자신이 사건 자리(접히지 않음 · 칸 none/미상 · adverse_tuple_assign 결정의 대상)")
    elif n == "event":
        a = (n, a[1], True, _COMP_NAME, "사건 사전 값. 뼈대 = complications.json 65 이름의 분해. 사전에 없는 조각은 미등록 · event_kind=raw_name 이면 이름 원문. v2.4: 튜플은 complications 65 이름에서만 생긴다(표현은 가리키기만)")
    elif n == "site_ref_kind":
        a = (n, a[1], True, _COMP_NAME, "site 개체(R31) | 상대 부위 사전(relative_site) | none. v2.4: 출처 = complications 이름 키(부위 조각은 그 문자열에서 · 3-C′) · 규칙은 §1.5 부위 규칙(사건이 놓인 멤버 안의 부위만 · 원칙 C)")
    elif n == "site_ref_id":
        a = (n, a[1], True, _COMP_NAME, "site 개체 id 또는 relative_site 사전 id 또는 none. v2.4: " + SITE_RULE)
    elif n == "status":
        a = ("status", "enum(complete|partial|unresolved)", True, [], "complete = 미등록 조각 0 · 붙지 않은 조각 0(사전 튜플) · partial = 미등록 조각 ≥1(raw_name) · unresolved(v2.4) = 미등록 0 이지만 사건에 붙지 않은 부위·경과 조각이 남음(raw_name · 원칙 B). 표현은 튜플 status 를 바꾸지 않는다(가리키기만)")
    elif n == "unregistered_fragments":
        a = (n, a[1], a[2], [], "이 튜플을 만든 이름의 미등록 조각(raw_name 만 · dict 튜플은 [] — v2.4: 표현의 미등록 조각은 표현 레코드에만)")
    elif n == "origins":
        a = (n, a[1], True, a[3], "이 튜플을 만든 원천 = complications 뿐(v2.4). 표현 origin 은 exact 로 **가리킨** 출처로만 더해진다(튜플을 만들지 않는다)")
    elif n == "candidate_name":
        a = (n, a[1], True, _COMP_NAME, "raw_name 튜플의 미등록 조각(사전 추가·adverse_tuple_assign 의 재료 · unresolved 면 []). dict 튜플은 []")
    elif n == "event_fragments":
        a = (n, a[1], True, [], "raw_name 튜플에서 사건 사전에 닿은 조각 전부(실값 · 버리지 않는다). dict 튜플은 [event]")
    elif n == "extra_sites":
        a = (n, a[1], True, [], "v2.4: 사건에 붙지 않은 부위 조각 전부(raw_name — 사건 없는 멤버·괄호 안 부위 나열 + 사전 분해가 붙였던 부위도 칸이 none 이므로 여기에) · 원칙 B 보존. dict 튜플은 [](붙지 않은 조각이 있으면 그 이름은 raw_name 이다)")
    elif n == "extra_courses":
        a = (n, a[1], True, [], "v2.4: 사건에 붙지 않은 경과 조각 + raw_name 의 사전 분해가 붙였던 경과(칸이 미상이므로 여기에) · 원칙 B 보존. dict 튜플은 []")
    _aattrs.append(a)
_aattrs += [
    ("dict_tuples", "obj[](event, site, course)|null", False, [], "v2.4: raw_name 튜플에 §1.5 사전 분해 결과를 보존만(튜플 칸이 아니다 · adverse_tuple_assign 의 재료). dict 튜플은 null"),
    ("raw_reason", "enum(unregistered|unattached_fragments|unregistered+unattached_fragments)|null", False, [], "v2.4: raw_name 이 된 사유. dict 튜플은 null"),
    ("site_basis", "enum(member|site_list)|null", False, [], "v2.4: dict 튜플의 site 가 어디서 왔나 — member(사건 멤버 안) · site_list(바로 앞 부위 나열 멤버) · null(none). 멤버 밖은 없다(검산)"),
    ("course_basis", "enum(member)|null", False, [], "course 가 어디서 왔나 — member(사건 멤버 안) · null(미상). 멤버 밖은 없다(검산)"),
]
_a["attrs"] = _aattrs
_x = _ent("adverse_expression")
_x["definition"] += " v2.4(원칙 D): 표현은 단위를 가리키기만 한다 — 분해 결과(candidates)가 기존 단위와 세 칸 완전 일치할 때만 R29(exact), 아니면 unlinked + candidates 보존. 표현에서 새 단위를 만들지 않는다."
_xattrs = []
for a in _x["attrs"]:
    if a[0] == "match_status":
        a = ("match_status", "enum(exact|unlinked)", True, [], "v2.4: exact = 미등록 조각 0 · 사건에 붙지 않은 조각 0 · 후보 전부가 기존 단위(complications 65 유래 사전 튜플)와 세 칸 완전 일치 → R29(후보마다). unlinked = 그 밖 전부(사유 unlinked_reasons) — R29 없음 · candidates 보존 · adverse_tuple_assign 의 대상(exact 포함 — 표현 레코드 전부가 대상 · §5.2). v2.3 의 linked/partial 삭제")
    elif a[0] == "unregistered_fragments":
        a = (a[0], a[1], a[2], [], "분해에서 어느 사전에도 닿지 않은 조각(하나라도 있으면 unlinked · 원칙 A)")
    _xattrs.append(a)
_xattrs += [
    ("candidates", "obj[](event, site, site_kind, course, would_be_id, exists, unit_id|null, site_basis, course_basis, member)", True, [], "v2.4: §1.5 로 분해한 (사건, 부위, 경과) 후보 전부(원칙 B · 버리지 않는다). exists = 기존 단위에 있음. 튜플이 아니다 — 표현은 단위를 만들지 않는다(원칙 D)"),
    ("unlinked_reasons", "enum[](unregistered|unattached_fragments|no_unit|no_event)", True, [], "v2.4: unlinked 사유(중복 가능). exact 면 []"),
    ("extra_sites", "str[]", True, [], "v2.4: 사건에 붙지 않은 부위 조각(보존 · 있으면 unlinked)"),
    ("extra_courses", "str[]", True, [], "v2.4: 사건에 붙지 않은 경과 조각(보존 · 있으면 unlinked)"),
]
_x["attrs"] = _xattrs

# 결정 kind 16 — 개체 decision 의 kind 열거는 같다
_d = _ent("decision")
_d["definition"] += " v2.4: adverse_tuple_assign 대상 = raw_name 전부 · 표현 레코드 전부(3-A′) · CAT- 는 트리 위치 계열 코드로 고정(3-B′)."

# ---------------------------------------------------------------------------
# 관계 — 구조 그대로(31). R29 · R15 · R31 비고
# ---------------------------------------------------------------------------
RELATIONS = copy.deepcopy(V23.RELATIONS)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


_r29 = _rel("R29")
_r29["attrs"] = [a if a[0] != "match_status" else ("match_status", "enum(exact)", "v2.4: R29 엣지는 match_status=exact 일 때만 있다(표현은 단위를 가리키기만 · 원칙 D). partial 연결 없음") for a in _r29["attrs"]]
_r29["attrs"] = [a if a[0] != "basis" else ("basis", "enum(both)", "문헌 표현: v2.4 는 statement·patient_ko 두 쪽 전부 exact 일 때만 연결(both)") for a in _r29["attrs"]]
_r29["note"] = ("v2.4(원칙 D): 표현의 분해 결과(candidates)가 미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위(complications 65 유래 사전 튜플)와 세 칸 완전 일치할 때만 연결(exact · 후보마다 엣지). 아니면 null(unlinked) + 표현 레코드에 candidates·unlinked_reasons 보존. "
                "표현은 raw_name 튜플도 사전 튜플도 만들지 않는다(v2.3 §9.6.4 의 새 튜플 57 → 0). 출처는 v2.3 그대로(22 = 11 + taxonomy safety 11). 사전 값·동의어 추가는 이번 범위 아님")
_r15 = _rel("R15")
_r15["note"] = (_r15["note"] or "") + " v2.4: 표현 유래 엣지(expression_id)는 그 표현이 R29 exact 일 때만 생긴다 — 끝은 기존 단위(complications 65 유래 튜플) · 표현이 세운 튜플은 없다."
_r31 = _rel("R31")
_r31["note"] = (_r31["note"] or "") + " v2.4: site 축 값은 §1.5 부위 규칙(사건이 놓인 멤버 안의 부위만 · 원칙 C) · raw_name 은 none"

ERD_ENUMS = copy.deepcopy(V23.ERD_ENUMS)
ERD_ENUMS["adverse_expression.match_status"] = ["exact", "unlinked"]
ERD_ENUMS["adverse_expression.unlinked_reason"] = ["unregistered", "unattached_fragments", "no_unit", "no_event"]
ERD_ENUMS["adverse_effect.status"] = ["complete", "partial", "unresolved"]
ERD_ENUMS["adverse_effect.raw_reason"] = ["unregistered", "unattached_fragments", "unregistered+unattached_fragments"]
ERD_ENUMS["adverse_effect.site_basis"] = ["member", "site_list"]
ERD_ENUMS["decision.kind"] = [k[0] for k in DECISION_KINDS]

QUALITY_RULES = list(V23.QUALITY_RULES)

# ---------------------------------------------------------------------------
# 튜플 규칙 v2.4 (데이터) — erd-v2.4-tuples.py 가 그대로 실행
# ---------------------------------------------------------------------------
TUPLE_RULES = copy.deepcopy(V23.TUPLE_RULES)
TUPLE_RULES["name"] = "tuples_v2_4"
TUPLE_RULES["principles"] = [{"key": k, "text": v} for k, v in PRINCIPLES]
_P = TUPLE_RULES["procedure"]
_P["input"]["catalog_items"] = _P["input"]["catalog_items"] + " — v2.4: family = taxonomy 트리 위치의 계열 코드(modality[].id · reclassification 적용 전) · CAT- id 의 계열 코드와 같다(§2.4)"
_P["cat_family"] = CAT_FAMILY_RULE
_Q = TUPLE_RULES["adverse"]
_Q["principles"] = PRINCIPLES_TEXT
_Q["course"] = COURSE_RULE
_Q["site"] = SITE_RULE
_Q["tuple"] = ("멤버 안의 사건 조각 하나 = 튜플 하나(멤버에 사건이 둘이면 둘). **course 는 같은 멤버 안의 수식어만**(§1.5 경과 규칙 · v2.3) · **site 도 같은 멤버 안의 부위 조각만**(§1.5 부위 규칙 · v2.4 · 원칙 C) — 둘 다 멤버 밖에서 가져오지 않는다. "
               "한 칸에 후보가 둘 이상이면 후보마다 튜플(원칙 B). 사건에 붙지 않은 부위·경과 조각은 extra_* 에 보존하고 그 문자열은 접지 않는다. 없으면 site=none, course=미상")
_Q["fold_condition"] = FOLD_CONDITION
_Q["fold_rule"] = ADVERSE_FOLD_RULE
_Q["raw_name"] = RAW_NAME_RULE
_Q["expressions"] = EXPRESSION_RULE
_Q["id"] = ID_RULE["adverse_effect"]
_Q["status"] = "complete = 미등록 조각 0 · 붙지 않은 조각 0 · partial = 미등록 조각 ≥1(raw_name) · unresolved = 붙지 않은 부위·경과 조각만 남음(raw_name · v2.4). 표현은 튜플 status 를 바꾸지 않는다(match_status=exact|unlinked 는 표현 레코드의 것)"
_Q["locator"] = LOCATOR_RULE
_Q["site_member_only"] = True
_Q["expressions_create_units"] = False
_Q["raw_name_cells"] = "none/미상"
