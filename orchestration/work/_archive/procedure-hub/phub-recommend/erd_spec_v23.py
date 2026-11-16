# -*- coding: utf-8 -*-
"""ERD v2.3 명세 (데이터). erd_spec_v22.py(v2.2) 를 읽어 2차 독립 검토(erd-v2.2-review.md ⑥) 반영 수정 7건만 덧씌운다 (발주서 erd-v2.3-brief.md).
  1. 시술 축 엣지의 끝 = 시술 튜플 — R3·R9·R12·R15·R16·R17·R18: 참조가 튜플로 해결됐으면 procedure 튜플 id 가 끝. 계열·하위분류·제품 노드는 참조가 그 층까지만 적혀 있을 때뿐(target_depth)
  2. 경과(course)는 사건에 바로 붙은 수식어만 — 이름 안에 사건이 둘 이상이면 수식어가 붙은 사건에만 경과, 나머지는 미상 (§1.5 문자 그대로)
  3. 부작용도 미등록 조각이 있으면 접지 않는다 — 미등록 조각이 있는 이름은 항목별 고유 튜플(event_kind=raw_name · candidate_name) · 접힘은 세 칸 전부 사전 값일 때만
  4. 결정 kind 4종 추가 — edge_create · tuple_assign_multi · adverse_tuple_assign · conflict_close (12 + 4 = 16)
  5. 결정은 안 바뀌는 키만 가리키고(파생 id PRC-/ADV-/CFL- 금지) 적용 순서를 고정한다(① dictionary_add … ⑦ exclude)
  6. 기법 잔재 제거 — §2.7 정의 문장 · technique_id 출처(이름 키 → 기법 사전)
  7. R29 출처 보완 — taxonomy.json safety 잎 키 11
구조(개체 21 · 관계 31 · 사전 46)는 v2.2 그대로. erd_build_v23.py 가 읽는다. v2.2 명세는 손대지 않는다.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v22 as V22  # noqa

ERD_VERSION = "v2.3"
SNAPSHOT = V22.SNAPSHOT
LEDGER_DIR = V22.LEDGER_DIR
STEP1_FILE = V22.STEP1_FILE
STEP1_TIER2_SOURCE_RE = V22.STEP1_TIER2_SOURCE_RE
SOURCE_FILES = list(V22.SOURCE_FILES)
SOURCE_KIND = dict(V22.SOURCE_KIND)
TRUST_FLAGS = dict(V22.TRUST_FLAGS)
NORMALIZE_RULE = copy.deepcopy(V22.NORMALIZE_RULE)
Q25 = list(V22.Q25)
DISPOSITIONS = dict(V22.DISPOSITIONS)
SITE_LABELS_KEEP = list(V22.SITE_LABELS_KEEP)
Q14_ORAL_DRUGS = list(V22.Q14_ORAL_DRUGS)
ADVERSE_EVENT_TYPES = list(V22.ADVERSE_EVENT_TYPES)
ADVERSE_EVENT_CATEGORIES = list(V22.ADVERSE_EVENT_CATEGORIES)
ADVERSE_EVENT_CATEGORY_REVIEW = list(V22.ADVERSE_EVENT_CATEGORY_REVIEW)
RELATIVE_SITES = list(V22.RELATIVE_SITES)
COURSES = list(V22.COURSES)
COURSE_DROPPED = list(V22.COURSE_DROPPED)
FOLD_CONDITION = V22.FOLD_CONDITION
FOLD_RULE = V22.FOLD_RULE
RULE4 = V22.RULE4.replace("target.conflict_id", "target.conflict_key")
DECISION_COMMON_FIELDS = list(V22.DECISION_COMMON_FIELDS)
DECISION_STATUS = list(V22.DECISION_STATUS)
DECISION_BUILD_RULE = V22.DECISION_BUILD_RULE

# ---------------------------------------------------------------------------
# 수정 1 — 시술 축 엣지의 끝 = 시술 튜플
# ---------------------------------------------------------------------------
EDGE_END_RULE = ("v2.3 엣지 끝 규칙(검토 1-A): 시술 축(proc_axis)을 끝으로 쓰는 엣지는, 그 자리의 참조가 §1.4 로 **procedure 튜플**(또는 combo_ref 의 멤버 튜플)로 해결됐으면 그 **튜플 id 를 끝**으로 쓴다(target_depth=procedure · 미상 칸이 있는 anchor 튜플도 같다 · 참조가 분류 항목 이름과 일치하면 그 항목의 튜플이며 via_catalog_item=CAT- id). "
                 "계열(modality)·하위분류(modality_subcategory)·제품(product) 노드에 직접 붙는 것은 **참조가 그 층까지만 적혀 있을 때뿐**이다 — M 코드만(M1) → modality · 실존 하위분류 id(M1-2 · M16-DCA) → subcategory · 제품 사전 전용 자리(products[]) 와 제품 레코드(taxonomy products[]) → product — 그 깊이를 target_depth 로 표시한다. "
                 "분류 항목 id(M8-1-1 · auto-…) 나 taxonomy 항목 레코드에 붙은 자리는 그 항목의 튜플(procedure)이다 — 항목 521 전부 튜플이 있으므로 catalog_item 은 끝이 아니다. 미해결(⑨)은 끝이 없다(unresolved_reference 레코드). 실측: §9.5.8 엣지 자리별 끝 분포(erd-v2.3-tuples.py)")
EDGE_END_KINDS = ["procedure", "modality", "subcategory", "product", "unresolved"]
TARGET_DEPTH = ["modality", "subcategory", "procedure", "product"]

# ---------------------------------------------------------------------------
# 수정 2 — 경과 규칙 (§1.5 · §2.14 · §4 세 곳 같은 문장)
# ---------------------------------------------------------------------------
COURSE_RULE = ("경과(course)는 분해하는 문자열(complications 이름 · 표현 원문) 안의 경과 수식어(일시적 · 지연성 · 영구 · 가역적 등 경과 사전 값과 동의어)에서만 읽되, **사건에 바로 붙은 수식어만** 읽는다 — 같은 멤버(조합 기호 `· / , + 및 또는` 로 나뉜 조각) 안의 수식어만 그 사건의 경과다. "
               "이름 안에 사건이 둘 이상이면 수식어가 붙은 사건에만 경과를 주고 나머지는 미상: 「통증·불편감 및 지연성 통증(LOP)」→ (통증, 미상) + (통증, 지연) 둘. 멤버 밖(같은 묶음 · 바깥 묶음 · 이름 전체)의 수식어는 가져오지 않는다. "
               "duration · incidence 는 R15 엣지 속성으로만 쓰고 경과 칸을 정하는 데 읽지 않는다. 수식어가 없으면 「미상」.")

# ---------------------------------------------------------------------------
# 수정 3 — 부작용 접힘 조건 · raw_name 튜플 · 원장 locator
# ---------------------------------------------------------------------------
LOCATOR_RULE = ("원장 locator = `<파일>:<잎 키 경로>@<레코드 키>` — 레코드 키는 상위 레코드 id 와 배열 위치(예 `complications.json:categories[].complications[].name@M16/12` = M16 묶음의 13번째 이름 · "
                "`extracted.json:{code}.safety.common[]@M1/3`). 브론즈는 바이트 보존(sha256)이라 위치가 안정 키다. 결정 레코드의 target 과 conflict 안정 키가 이 locator 를 쓴다")
ADVERSE_FOLD_RULE = ("부작용 접힘 조건(v2.3 · 검토 2-B · 시술과 같은 원칙): **세 칸 전부 사전 값일 때만** 다른 이름과 접힌다 — 이름의 조각이 전부 사전(사건 · 부위 · 상대 부위 · 경과)에 닿아 미등록 조각이 0 이고 event 가 사건 사전 값일 때. "
                     "부작용 축의 site none · course 미상은 v2 그대로 축의 정의값이라 사전 값으로 센다(검토 2-D 「none·미상을 식별자 값으로 둘지」는 동결 후 scope_review — §12). "
                     "complications 이름에 **미등록 조각이 하나라도 있으면 접지 않는다**: 그 이름은 항목별 고유 튜플(event_kind=raw_name · event=이름 원문 · anchor=그 이름의 원장 locator · candidate_name=미등록 조각 · 닿은 사건·부위·경과 조각은 event_fragments·extra_* 에 실값 보존)이며 식별자에 anchor 가 들어가 다른 이름과 접히지 않는다. "
                     "표현(adverse_expression)은 정체성을 만들지 않으므로 raw_name 튜플을 만들지 않는다 — 조각이 닿은 사전 튜플에 R29 로 연결하되 미등록 조각이 있으면 match_status=partial 로 구분한다(linked = 미등록 0 · partial = 미등록 ≥1 · unlinked = 닿은 사건 없음)")
ID_RULE = copy.deepcopy(V22.ID_RULE)
ID_RULE["adverse_effect"] = ("세 칸 전부 사전 값이면(미등록 조각 0 · event_kind=dict) ADV-<sha256(event_id|site_id|course_id)[:10]>, 미등록 조각이 있는 complications 이름(event_kind=raw_name)은 ADV-<sha256(RAW:<anchor>|site_id|course_id|<anchor>)[:10]> — "
                             "event_id = 사건 사전 id, site_id = site 개체 id | 상대 부위 사전 id | 'none', course_id = 경과 사전 id('미상' 포함), anchor = 그 이름의 원장 locator. v2.3: 미등록 조각이 있으면 접히지 않는다(§1.5 접힘 조건)")
ID_RULE["locator"] = LOCATOR_RULE
ID_RULE["conflict_decision_ids"] = ("CFL- 레코드 id 는 (대상 id + 속성 + 출처 집합) 해시 — **파생 id 라 결정의 target 이 아니다**. 결정이 가리키는 conflict 의 안정 키 = conflict.stable_key = {kind, locators[]}(값 출처 원장 locator 의 정렬 쌍 + 충돌 종류). DEC- 는 (적용일 + 일련)")
ID_RULE["decision_target"] = ("결정 target 이 가리켜도 되는 키(v2.3 · 검토 3-B): 분류 항목 id(CAT-) · 참조 자리 id(REF- · 조합 멤버 REF-…#m<i>) · 원장 locator(file:key path@record) · 원장에서 직접 나온 고정 id(MOD-/SUB-/PRD-/SIT-/TEC-) · 사전 값(사전 이름 + 정준값) · conflict 안정 키(kind + locator 쌍). "
                              "**금지**: 다른 결정을 적용하면 바뀌는 파생 id — PRC-(튜플) · ADV-(부작용 튜플) · CFL-(충돌 레코드) · 부작용 튜플은 (event, site, course) 사전 값 세 쌍으로, 시술 튜플은 anchor(CAT-/REF-) 또는 (what_id, site_id, technique_id) 로 가리킨다. 검산 K-2 가 전수 확인")

# ---------------------------------------------------------------------------
# 수정 4·5 — 결정 kind 16 · 안정 키 · 적용 순서
# ---------------------------------------------------------------------------
_REF_STRUCT = "ref 구조체 = obj(kind: anchor|locator|procedure_tuple|adverse_tuple|dict_value, anchor: CAT-/REF- | locator: str | tuple: obj(what_id, site_id, technique_id) | tuple: obj(event, site, course — 사전 정준값) | dict: obj(dictionary, canonical))"
DECISION_KINDS = [
    ("dictionary_add", True, "obj(dictionary: 사전 이름)", "obj(canonical: str, synonyms: str[], category: str|null)", "사전에 값·동의어 추가(출처는 source_refs). 빌드는 분해를 다시 돌린다. §9.5.6·§12-3 의 미등록 조각·제품 사전 확장이 갈 자리. 적용 ①"),
    ("canonical_mapping", True, "obj(from_ref: str — 원천 참조(R5:<계열> · MOD-/SUB-/PRD- id · 라벨 · 원장 canonical_category 의 CAT- id), scope: str[] — 적용 범위의 anchor 목록(CAT-/REF-) 또는 [\"*\"])", "obj(to_id: str — MOD-/SUB-/PRD-/TEC- 고정 id)",
     "from_ref 를 to_id 로 읽는다(scope 의 anchor 안에서만 · v2.3: scope 는 자유 문자열이 아니라 id 목록 — §9.5.6 의 분류 항목 목록이 그 scope). R5 계열 기법 후보(§9.5.6) · 보톡스 product↔modality(검토 1-E) · 원장 canonical_category(질문 23). 적용 ②"),
    ("tuple_assign", True, "obj(catalog_item_id: CAT-id | ref_id: REF-id — 둘 중 하나)", "obj(what_kind, what_id, site_id, technique_id)", "분해 결과 대신 그 항목·참조의 튜플 세 칸을 지정(「사각턱보톡스 = 보톡스×턱×injection」). 지정값이 세 칸 전부 사전 값이면 접힐 수 있고 아니면 anchor 그대로. 적용 ③"),
    ("tuple_assign_multi", True, "obj(catalog_item_id: CAT-id | ref_id: REF-id — 둘 중 하나)", "obj(tuples: obj[](what_kind, what_id, site_id, technique_id) — 둘 이상)",
     "v2.3: 항목·참조 하나를 튜플 **여럿**으로 지정(「보톡스 이마/미간」= 보톡스×이마 + 보톡스×미간 · 「필러 볼/턱」). 참조 자리면 package(kind=combo_ref)로 멤버 각각 R12, 분류 항목이면 튜플마다 R26. §9.5.4 multi_site·multi_primary 미해결의 자리. 적용 ③"),
    ("adverse_tuple_assign", True, "obj(locator: 원장 locator — complications 이름(raw_name 튜플의 anchor) 또는 표현(adverse_expression) 레코드, kind: raw_name|expression)", "obj(tuples: obj[](event_id, site_id, course_id) — 하나 이상)",
     "v2.3: 부작용 원천(미등록 조각이 있어 raw_name 으로 남은 complications 이름 · partial/unlinked 표현)에 (사건, 부위, 경과) 튜플을 사람이 지정한다(「카테터 관련 감염」→ 감염×카테터 · 「구형구축 (…섬유성 결절)」→ 구형구축만). raw_name 튜플은 지정 튜플로 대체되고 locator 가 출처로 남는다 · 표현은 R29 를 지정 튜플로. 적용 ③"),
    ("fold_approve", True, "obj(anchors: str[] ≥2 — CAT-/REF- id 또는 조합 멤버 anchor(…#m<i>))", "obj(keep_anchor: str — anchors 중 하나)",
     "anchor 가 가리키는 튜플 둘 이상을 하나로(v2.3: PRC- 가 아니라 anchor 를 받는다 — 검토 3-B). 나머지 anchor 의 튜플 출처·R26·엣지를 keep_anchor 의 튜플로 옮기고 나머지 튜플 id 는 alias. 적용 ④"),
    ("event_split", True, "obj(event: 사건 사전 정준값)", "obj(new_events: obj[](canonical, synonyms[], category))", "사건 사전 값 하나를 여럿으로(과민반응 ≠ 아나필락시스 등). 옮긴 동의어는 원 값에서 빠진다. 빌드는 부작용 분해를 다시 돌린다. 적용 ④"),
    ("edge_create", True, "obj(relation: R# — R30 등 결정으로만 값이 생기는 관계, from_ref: ref 구조체, to_ref: ref 구조체)", "obj(attrs: obj — 그 관계의 엣지 속성)",
     "v2.3: 원장이 구조화하지 않은 엣지를 사람이 만든다 — R30 leads_to(혈관 폐색 → 피부 괴사) 등. " + _REF_STRUCT + ". 적용 ⑤"),
    ("conflict_override", True, "obj(conflict_key: obj(kind, locators[]) — conflict.stable_key)", "obj(chosen_value: any)", "규칙 ④ 자동 해결(auto_resolved_by_trust) 또는 ⑥ open 충돌의 값을 사람이 정한다(v2.3: CFL- 가 아니라 안정 키). conflict.status → resolved · decision_id. 적용 ⑥"),
    ("conflict_close", True, "obj(conflict_key: obj(kind, locators[]) — conflict.stable_key)", "obj(verdict: enum(not_same|both_valid|needs_source), note: str)",
     "v2.3: 값을 고르지 않고 충돌을 닫는다 — not_same(⑦ 후보는 같은 것이 아니다 · 각자 유지) · both_valid(둘 다 맞다 · 실버에 둘 다, 골드도 둘 다) · needs_source(원장 밖 근거가 필요 · 골드 제외 유지). 셋 다 conflict.status → dismissed · verdict·note 는 conflict.close_verdict 에 보존. 「단계 끝 = open 0」에 닿는 길. 적용 ⑥"),
    ("exclude", True, "obj(kind: enum(catalog_item|reference|ledger_record|dictionary_value), key: CAT-id | REF-id | 원장 locator | obj(dictionary, canonical))", "obj(excluded: true)", "실버·골드에서 뺀다(원장은 그대로 · v2.3: 아무 id 가 아니라 고정 키만). 사유는 reason. 적용 ⑦"),
    ("reclassification", True, "obj(catalog_item_id: CAT-id)", "obj(modality_id: MOD-id)", "v1: 원장 reclassified_to → R2 재배치(질문 23). 원장 메모 결정 — 적용 ⓪(원장 적재 때)"),
    ("ledger_correction_note", False, "obj(catalog_item_id: CAT-id)", "obj(note: str)", "v1: 원장 교정 메모 보존(classification_issue · correction_note). 빌드가 값을 바꾸지 않는다"),
    ("verification_hold", False, "obj(catalog_item_id: CAT-id)", "obj(hold: true)", "v1: 원장 verification_needed — 확인 대기 표시만"),
    ("conflict_resolution", False, "obj(erd_ref: str — ERD 절·개체·속성 · review_item: str|null)", "obj(disposition: str)", "v1.1: ERD 개정 기록(처분). ERD 문서에 반영 — 빌드가 다시 적용하지 않는다"),
    ("scope_review", False, "obj(erd_ref: str — ERD 절·개체·관계 · review_item: str|null)", "obj(disposition: str)", "v1.1~: ERD 개정 기록(구조 변경·범위). ERD 문서에 반영 — 빌드가 다시 적용하지 않는다"),
]
DECISION_KINDS_NEW = list(V22.DECISION_KINDS_NEW)
DECISION_KINDS_NEW_V23 = ["edge_create", "tuple_assign_multi", "adverse_tuple_assign", "conflict_close"]
DECISION_KINDS_RESHAPED_V23 = {"fold_approve": "target.procedure_ids(PRC-) → target.anchors(CAT-/REF-) · keep_id → keep_anchor", "conflict_override": "target.conflict_id(CFL-) → target.conflict_key(안정 키)",
                               "exclude": "target.id(아무 id) → target.(kind, key) 고정 키", "canonical_mapping": "target.scope str → str[](anchor 목록)"}
DECISION_APPLY_ORDER = [
    ("①", ["dictionary_add"], "사전 값·동의어가 먼저 — 이후 단계의 분해·지정이 이 사전을 읽는다"),
    ("②", ["canonical_mapping"], "참조·계열 기법·canonical_category 를 읽는 방식"),
    ("③", ["tuple_assign", "tuple_assign_multi", "adverse_tuple_assign"], "항목·참조·부작용 원천의 튜플 지정(분해 결과를 덮는다)"),
    ("④", ["fold_approve", "event_split"], "튜플 접기 · 사건 사전 분리(③ 이 끝난 튜플 위에서)"),
    ("⑤", ["edge_create"], "결정으로만 생기는 엣지(R30 등) — 양끝 튜플이 ③④ 로 확정된 뒤"),
    ("⑥", ["conflict_override", "conflict_close"], "충돌 판정 — 값·튜플이 전부 확정된 뒤"),
    ("⑦", ["exclude"], "제외는 마지막"),
]
DECISION_APPLY_ORDER_RULE = ("빌드는 approved 결정을 **① dictionary_add → ② canonical_mapping → ③ tuple_assign / tuple_assign_multi / adverse_tuple_assign → ④ fold_approve / event_split → ⑤ edge_create → ⑥ conflict_override / conflict_close → ⑦ exclude** 순으로 적용한다. "
                             "같은 단계 안은 decided_at 순(같으면 id 순). 원장 메모 결정(reclassification · 원장 작성자)은 ⓪ 원장 적재 때. 결정 사이의 결과는 이 순서로만 정해지고 사전 상태에 따라 달라지지 않는다(검토 3-B)")
DECISION_TARGET_RULE = ID_RULE["decision_target"]

# ---------------------------------------------------------------------------
# 분해 규칙 (참조 §1.3 — v2.2 그대로)
# ---------------------------------------------------------------------------
RESOLVE_RULES = copy.deepcopy(V22.RESOLVE_RULES)
RESOLVE_RULES["name"] = "decompose_v2_3"

# ---------------------------------------------------------------------------
# 개체 — 구조 그대로(21)
# ---------------------------------------------------------------------------
ENTITIES = copy.deepcopy(V22.ENTITIES)


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


# 수정 6 — technique 정의 · technique_id 출처
_t = _ent("technique")
_t["definition"] = (_t["definition"].split(" v2: ")[0]
                    + " v2.3: procedure 튜플의 technique 축은 **이름 조각이 기법 사전에 완전 일치할 때만** 그 값이고, 아니면 none(미상)이다. 계열 기본값을 튜플에 붙이지 않는다 — R5(계열↔기법)는 관계로만 남고, "
                      "결정 kind canonical_mapping(target.from_ref=R5:<계열> · scope=anchor 목록)이 approved 일 때만 그 scope 의 technique=none 튜플에 적용된다(§9.5.6 후보 목록).")
_p = _ent("procedure")
_p["definition"] = (_p["definition"].replace("technique = 이름 조각이 기법 사전에 닿을 때만 그 값 | none — **R5 계열 기법 상속은 하지 않는다**(v2.2 · 결정 kind canonical_mapping 후보로만 §9.5.6). ",
                                             "technique = 이름 조각이 기법 사전에 닿을 때만 그 값 | none — **계열 기본값(R5)을 튜플에 붙이지 않는다**(v2.2 · 결정 kind canonical_mapping 후보로만 §9.5.6). ")
                    + " v2.3: 시술 축 엣지(R3·R9·R12·R15·R16·R17·R18)의 끝은 이 튜플이다(§3 엣지 끝 규칙).")
_SRC_REFS = next(a for a in _p["attrs"] if a[0] == "what_id")[3]
_attrs = []
for a in _p["attrs"]:
    n = a[0]
    if n == "technique_id":
        a = (n, a[1], False, list(_SRC_REFS), "기법 사전 값 또는 none. **이름 조각이 기법 사전에 완전 일치할 때만**(fragment) — 출처는 이름·참조 자리의 키(what_id 와 같다)이고 사전은 §4 technique(정준값 출처 procedure-profiles mechanism[]). v2.3: 출처를 이름 키로(검토 1-B). 계열 기본값은 붙이지 않는다 — canonical_mapping(target.from_ref=R5:<계열>) approved 일 때만")
    elif n == "technique_origin":
        a = (n, "enum(fragment|none)", True, [], "v2.2: inherited 삭제 · v2.3: fragment = 이름 조각이 기법 사전에 닿음 · none = 미상. canonical_mapping 결정으로 붙은 값은 실버 빌드에서 decision 출처(decision_id)로 남는다")
    _attrs.append(a)
_p["attrs"] = _attrs

# 수정 2·3 — adverse_effect
_a = _ent("adverse_effect")
_a["definition"] = (_a["definition"] + " v2.3: " + ADVERSE_FOLD_RULE + ". 경과 규칙은 §1.5(사건에 바로 붙은 수식어만).")
_a["identity"] = "sha256(event_id|site_id|course_id)[:10] — 세 칸 전부 사전 값일 때. 미등록 조각이 있는 이름(event_kind=raw_name)은 sha256(RAW:anchor|site_id|course_id|anchor) — 이름마다 고유(접히지 않음)"
_aattrs = []
for a in _a["attrs"]:
    if a[0] == "event":
        _aattrs.append(("event_kind", "enum(dict|raw_name)", True, [], "v2.3: dict = 사건 사전 값(세 칸 전부 사전 값 — 접힘 가능) · raw_name = complications 이름에 미등록 조각이 있어 이름 자신이 사건 자리(접히지 않음 · adverse_tuple_assign 결정의 대상)"))
        _aattrs.append(("event", "dict:adverse_event_type | str(raw_name)", True, a[3], a[4] + " · v2.3: event_kind=raw_name 이면 이름 원문"))
        continue
    if a[0] == "course":
        a = ("course", "dict:course", True, a[3], COURSE_RULE)
    if a[0] == "status":
        a = ("status", "enum(complete|partial)", True, [], "complete = 이 튜플을 만든 문구가 전부 미등록 조각 0 · partial = 미등록 조각 ≥1. v2.3: complications 이름은 partial 이면 raw_name 튜플(접히지 않음) — 사전 튜플(event_kind=dict)이 partial 인 것은 표현(R29 match_status=partial)에서만")
    _aattrs.append(a)
_aattrs += [
    ("anchor", "str|null", True, [], "v2.3 식별자 anchor. 세 칸 전부 사전 값이면 null(접힘 가능), raw_name 이면 그 이름의 원장 locator — 식별자에 들어가 이름마다 고유"),
    ("all_dict_values", "bool", True, [], "v2.3: event 가 사전 값이고 미등록 조각 0 이면 true — 그때만 접힘(site none · course 미상은 축의 정의값으로 센다 · 검토 2-D 는 §12)"),
    ("candidate_name", "str[]", True, ["complications.json:categories[].complications[].name"], "v2.3: raw_name 튜플의 미등록 조각(사전 추가·adverse_tuple_assign 의 재료). dict 튜플은 []"),
    ("event_fragments", "str[]", True, [], "v2.3: raw_name 튜플에서 사건 사전에 닿은 조각 전부(실값 · 버리지 않는다). dict 튜플은 [event]"),
    ("extra_sites", "str[]", True, [], "v2.3: raw_name 튜플에서 site 칸에 들어가지 않은 부위 조각(둘 이상일 때 전부). dict 튜플은 []"),
    ("extra_courses", "str[]", True, [], "v2.3: raw_name 튜플에서 course 칸에 들어가지 않은 경과 조각(둘 이상일 때 전부). dict 튜플은 []"),
]
_a["attrs"] = _aattrs
_x = _ent("adverse_expression")
_x["attrs"] = [a if a[0] != "match_status" else ("match_status", "enum(linked|partial|unlinked)", True, [], "R29 가 있으면 linked. v2.3: 미등록 조각이 있는데 닿은 사전 튜플이 있으면 partial(표현은 정체성을 만들지 않는다 — raw_name 튜플 없음 · adverse_tuple_assign 의 대상) · 닿은 사건 없음 unlinked") for a in _x["attrs"]]
_x["identity"] = "출처 파일 + 잎 키 경로 + 레코드 위치 + lang (= 원장 locator · §1.1)"

# 수정 4·5 — conflict · decision
_c = _ent("conflict")
_c["identity"] = "레코드 id = 대상 id + 속성/엣지 + 출처 집합 해시(CFL- · 파생). **안정 키 stable_key = {kind, locators[]}**(값 출처 원장 locator 정렬 쌍 + 종류) — 결정은 이것만 가리킨다(v2.3 · 검토 3-B)"
_c["definition"] += " v2.3: 사람 판정은 decision(kind=conflict_override — 값을 고름 · conflict_close — 고르지 않고 닫음: not_same | both_valid | needs_source)으로만, 둘 다 conflict.stable_key 를 가리킨다."
_cattrs = []
for a in _c["attrs"]:
    _cattrs.append(a)
    if a[0] == "target_id":
        _cattrs.append(("stable_key", "obj(kind, locators: str[] — 정렬)", True, [], "v2.3: 결정이 가리키는 안정 키. locators = values[] 의 (source_file:source_path@record) 전부(정렬). target_id 가 파생 id(PRC-/ADV-)여도 이 키는 바뀌지 않는다"))
    if a[0] == "chosen_value":
        _cattrs.append(("close_verdict", "enum(not_same|both_valid|needs_source)|null", False, [], "v2.3: conflict_close 결정(approved)의 verdict. status=dismissed 와 함께"))
    if a[0] == "status":
        _cattrs[-1] = ("status", "enum(open|auto_resolved_by_trust|resolved|dismissed)", True, [], "v2.2: ④ 자동 채택 = auto_resolved_by_trust · ⑥~⑨ 사람 판정 전 = open · conflict_override(approved) = resolved · v2.3: conflict_close(approved) = dismissed")
_c["attrs"] = _cattrs
_d = _ent("decision")
_d["definition"] = (_d["definition"] + " v2.3: target 은 안정 키만(" + "CAT-/REF-/원장 locator/고정 id/사전 값/conflict.stable_key — PRC-/ADV-/CFL- 금지) · 적용 순서 ①~⑦ 고정(§5 표) · kind 16(12 + edge_create · tuple_assign_multi · adverse_tuple_assign · conflict_close).")
_dattrs = []
for a in _d["attrs"]:
    if a[0] == "kind":
        a = ("kind", "enum(" + "|".join(k[0] for k in DECISION_KINDS) + ")", True, [], "§5.2 표(16). 빌드 적용 kind(build_reads=true): " + " · ".join(k[0] for k in DECISION_KINDS if k[1]) + " · 적용 순서 §5 표")
    elif a[0] == "target":
        a = ("target", "obj(kind별)", True, [], "무엇에 적용하나 — kind별 구조체(§5.2). v2.3: 안정 키만(" + "검산 K-2: PRC-/ADV-/CFL- 0)")
    _dattrs.append(a)
_d["attrs"] = _dattrs

# ---------------------------------------------------------------------------
# 관계 — 구조 그대로(31). 수정 1(R3·R9·R12·R15·R16·R17·R18) · 수정 7(R29) · R30 비고
# ---------------------------------------------------------------------------
RELATIONS = copy.deepcopy(V22.RELATIONS)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


PROMOTE_RULE_V2 = V22.V21.V2.PROMOTE_RULE
PROC_AXIS_EDGES = ["R3", "R9", "R12", "R15", "R16", "R17", "R18"]
for rid in PROC_AXIS_EDGES:
    r = _rel(rid)
    r["note"] = (r["note"] or "").replace(PROMOTE_RULE_V2, EDGE_END_RULE)
    if EDGE_END_RULE not in r["note"]:
        r["note"] = (r["note"] + ". " if r["note"] else "") + EDGE_END_RULE
    attrs = []
    for a in r["attrs"]:
        if a[0] == "target_depth":
            a = ("target_depth", "enum(" + "|".join(TARGET_DEPTH) + ")", "v2.3: 끝의 깊이 — procedure(참조가 튜플로 해결됨 · 기본) · modality/subcategory/product(참조가 그 층까지만 적힘). catalog_item 은 끝이 아니다(항목 전부 튜플이 있다)")
        elif a[0] == "via_catalog_item":
            a = ("via_catalog_item", "str|null", "참조가 분류 항목 이름과 일치해 그 항목의 튜플을 끝으로 썼을 때 그 항목 id(CAT-)")
        attrs.append(a)
    if not any(a[0] == "target_depth" for a in attrs):
        attrs.append(("target_depth", "enum(" + "|".join(TARGET_DEPTH) + ")", "v2.3: 끝의 깊이(procedure 기본)"))
    if not any(a[0] == "via_catalog_item" for a in attrs):
        attrs.append(("via_catalog_item", "str|null", "참조가 분류 항목 이름과 일치해 그 항목의 튜플을 끝으로 썼을 때 그 항목 id(CAT-)"))
    r["attrs"] = attrs
_rel("R3").update({"from": "procedure", "note": "v2.3: 항목 이름 = 같은 계열 제품명(정규화 완전 일치)일 때만 자동. 끝(from)은 그 항목의 튜플(what=product · via_catalog_item=CAT-). " + EDGE_END_RULE})
_r29 = _rel("R29")
R29_TAXONOMY_SAFETY_KEYS = [
    "taxonomy.json:modality[].extracted.safety.common[]", "taxonomy.json:modality[].extracted.safety.uncommon[]", "taxonomy.json:modality[].extracted.safety.serious[]",
    "taxonomy.json:modality[].subcategories[].items[].extracted.safety.common[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]",
    "taxonomy.json:modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]",
    "taxonomy.json:modality[].subcategories[].items[].extracted.safety.long_term[]",
    "taxonomy.json:modality[].products[].extracted.safety.common[]", "taxonomy.json:modality[].products[].extracted.safety.serious[]", "taxonomy.json:modality[].products[].extracted.safety.common_side_effects[]",
]
_r29["sources"] = list(_r29["sources"]) + [k for k in R29_TAXONOMY_SAFETY_KEYS if k not in _r29["sources"]]
_r29["attrs"] = list(_r29["attrs"]) + [("match_status", "enum(linked|partial)", "v2.3: 표현에 미등록 조각이 있으면 partial(연결은 두되 구분)")]
_r29["note"] = "튜플에 닿으면 연결, 아니면 null + 미등록 조각 기록. v2.3: 출처에 taxonomy.json safety 잎 키 11(계열 3 · 항목 5 · 제품 3)을 더했다(§9.6.3 연결 대부분의 출처 · 검토 3-C) · 미등록 조각이 있는 표현은 match_status=partial. 사전 값·동의어 추가는 이번 범위 아님"
_r30 = _rel("R30")
_r30["note"] = "인과(혈관 폐색 → 피부 괴사). 원장은 인과를 구조화하지 않았다(incidence·mechanism 문장 안에만 있음) — 자동 생성 없음. v2.3: 결정 kind edge_create(target.relation=R30 · from_ref/to_ref = (event, site, course) 사전 값 세 쌍 · new_value.attrs.basis) 가 approved 일 때만 값이 생긴다(적용 ⑤)"
_rel("R24")["note"] = "decision.target 구조체(kind별)가 끝점 — v2.3: 안정 키만(CAT-/REF-/원장 locator/고정 id/사전 값/conflict.stable_key). 빌드는 status=approved 만 §5 적용 순서로 따라간다"
_rel("R23")["note"] = (_rel("R23")["note"] or "") + ". v2.3: conflict.stable_key(kind + 출처 locator 쌍)가 결정의 대상"

ERD_ENUMS = copy.deepcopy(V22.ERD_ENUMS)
ERD_ENUMS["target_depth"] = list(TARGET_DEPTH)
ERD_ENUMS["edge_end_kind"] = list(EDGE_END_KINDS)
ERD_ENUMS["adverse_effect.event_kind"] = ["dict", "raw_name"]
ERD_ENUMS["adverse_expression.match_status"] = ["linked", "partial", "unlinked"]
ERD_ENUMS["conflict.close_verdict"] = ["not_same", "both_valid", "needs_source"]
ERD_ENUMS["decision.kind"] = [k[0] for k in DECISION_KINDS]
ERD_ENUMS["decision.apply_order"] = [" / ".join(ks) for _, ks, _ in DECISION_APPLY_ORDER]

QUALITY_RULES = []
for no, cls, rule in V22.QUALITY_RULES:
    if no == "④":
        rule = RULE4
    elif no == "⑦":
        rule = rule + ". v2.3: 판정은 decision conflict_close(verdict=not_same) 또는 fold_approve"
    elif no == "⑨":
        rule = rule + ". v2.3: 범위 밖·판정은 conflict_close(needs_source) · 지정은 tuple_assign(_multi)"
    QUALITY_RULES.append((no, cls, rule))

# ---------------------------------------------------------------------------
# 튜플 규칙 v2.3 (데이터) — erd-v2.3-tuples.py 가 그대로 실행
# ---------------------------------------------------------------------------
TUPLE_RULES = copy.deepcopy(V22.TUPLE_RULES)
TUPLE_RULES["name"] = "tuples_v2_3"
_P = TUPLE_RULES["procedure"]
_P["technique"] = ("조각이 기법 사전(12)에 닿으면 그 값(fragment). 아니면 **none**(미상은 미상 — 계열 기본값 R5 를 튜플에 붙이지 않는다 · v2.2). 서로 다른 기법 조각이 둘 이상이면 site 와 같은 처리(multi_technique). "
                   "R5 계열 → 기법은 decision kind canonical_mapping(target.from_ref=R5:<계열>, target.scope=anchor 목록) 후보로만 §9.5.6 에 목록")
_P["edge_end"] = EDGE_END_RULE
_P["edge_end_kinds"] = list(EDGE_END_KINDS)
_P["code_references"] = "M 코드만(M1)·실존 하위분류 id(M1-2 · M16-DCA)인 참조는 분해하지 않고 그 노드가 끝(modality/subcategory · 튜플 없음). 분류 항목 id(M8-1-1 · auto-…)는 그 항목의 튜플이 끝(procedure)"
_Q = TUPLE_RULES["adverse"]
_Q["course"] = COURSE_RULE
_Q["tuple"] = ("멤버 안의 사건 조각 하나 = 튜플 하나(멤버에 사건이 둘이면 둘). **course 는 같은 멤버 안의 수식어만**(§1.5 경과 규칙 · v2.3) — 멤버 밖에서 가져오지 않는다. "
               "site 는 v2 그대로 멤버 → 같은 묶음 → outer 묶음 → (이름 전체에 그 축의 값이 하나뿐이면 그 값) 순(멤버 자체 값이 우선 · 「주사 부위 반응 (부종·압통)」의 바깥 부위). 없으면 site=none, course=미상")
_Q["fold_condition"] = FOLD_CONDITION
_Q["fold_rule"] = ADVERSE_FOLD_RULE
_Q["raw_name"] = ("complications 이름에 미등록 조각이 있으면: 튜플 하나(event_kind=raw_name · event=이름 원문 · anchor=원장 locator · candidate_name=미등록 조각 · event_fragments=닿은 사건 조각 전부 · site/course 는 닿은 조각이 하나씩일 때만 그 칸, 둘 이상이면 none/미상 + extra_* 에 전부). "
                  "같은 이름이 여러 사건 조각을 가져도 튜플은 하나다(지정은 adverse_tuple_assign)")
_Q["expressions"] = "표현(AEX)은 raw_name 튜플을 만들지 않는다. 미등록 조각이 있어도 닿은 사전 튜플에 R29 로 연결하되 match_status=partial · 닿은 사건이 없으면 unlinked. 표현이 만든 사전 튜플은 v2 그대로(65 에 없던 새 튜플 §9.6.4)"
_Q["id"] = ID_RULE["adverse_effect"]
_Q["status"] = "complete = 문구에 미등록 조각 0 · partial = 미등록 조각 ≥1 (complications 이름은 partial 이면 raw_name 튜플 · 표현은 partial 이면 R29 match_status=partial)"
_Q["locator"] = LOCATOR_RULE
