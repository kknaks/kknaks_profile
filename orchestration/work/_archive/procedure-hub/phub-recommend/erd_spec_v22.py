# -*- coding: utf-8 -*-
"""ERD v2.2 명세 (데이터). erd_spec_v21.py(v2.1) 를 읽어 독립 검토(erd-v2.1-review.md) 반영 수정 6건만 덧씌운다 (발주서 erd-v2.2-brief.md).
  1. 미상은 식별자 값이 아니다 — 접힘 조건 「세 칸 전부 사전 값일 때만」 · 미상 칸이 있으면 식별자에 anchor(CAT-/REF-)
  2. 조각을 버리고 접지 않는다 — primary·site(·technique) 조각 둘 이상이면 combo_ref 또는 미해결 · v2.1 what 규칙 8 삭제 · extra_* 실값
  3. 기법 상속을 끈다 — technique 는 기법 사전에 닿은 이름 조각만 · R5 상속은 canonical_mapping 후보로만
  4. 규칙 ④ 유지 + 기록 — 신뢰 순위 자동 해결마다 conflict 레코드(status=auto_resolved_by_trust · chosen_value · values[].trust_tier · rule_ref=④) · decision kind conflict_override
  5. decision 개체를 빌드가 읽는 모양으로 — kind 7 추가/재정의 · 공통 필드 · 빌드는 status=approved 만 · 기존 22 이관
  6. course 출처 일원화 — 이름 수식어에서만 · duration·incidence 는 엣지 속성으로만 (§1.5·§2.14·§4 같은 문장)
구조(개체 21 · 관계 31 · 사전 46)는 v2.1 그대로. erd_build_v22.py 가 읽는다. v2.1 명세는 손대지 않는다.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v21 as V21  # noqa

ERD_VERSION = "v2.2"
SNAPSHOT = V21.SNAPSHOT
LEDGER_DIR = V21.LEDGER_DIR
STEP1_FILE = V21.STEP1_FILE
STEP1_TIER2_SOURCE_RE = V21.STEP1_TIER2_SOURCE_RE
SOURCE_FILES = list(V21.SOURCE_FILES)
SOURCE_KIND = dict(V21.SOURCE_KIND)
TRUST_FLAGS = dict(V21.TRUST_FLAGS)
NORMALIZE_RULE = copy.deepcopy(V21.NORMALIZE_RULE)
Q25 = list(V21.Q25)
DISPOSITIONS = dict(V21.DISPOSITIONS)
SITE_LABELS_KEEP = list(V21.SITE_LABELS_KEEP)
Q14_ORAL_DRUGS = list(V21.Q14_ORAL_DRUGS)
ADVERSE_EVENT_TYPES = list(V21.ADVERSE_EVENT_TYPES)
ADVERSE_EVENT_CATEGORIES = list(V21.ADVERSE_EVENT_CATEGORIES)
ADVERSE_EVENT_CATEGORY_REVIEW = list(V21.ADVERSE_EVENT_CATEGORY_REVIEW)
RELATIVE_SITES = list(V21.RELATIVE_SITES)

# ---------------------------------------------------------------------------
# 수정 1 — 접힘 조건 문장(문자 그대로) · 식별자
# ---------------------------------------------------------------------------
FOLD_CONDITION = "세 칸 전부 사전 값일 때만"
FOLD_RULE = ("접힘 조건: **" + FOLD_CONDITION + "** 다른 항목·참조와 접힌다 — what 이 사전 값(product | modality_subcategory | modality)이고 site 가 부위 사전 값이고 technique 가 기법 사전 값일 때. "
             "미상(site none · technique none)은 식별자 값이 아니다: 미상 칸이 하나라도 있거나 what 이 분류 항목 자신(CAT-)이면 식별자에 anchor 를 섞어 항목·참조마다 고유하다(접히지 않음). "
             "anchor = 분류 항목은 CAT- id, 참조(②③)는 REF-sha256(norm(label)|hint)[:10], 조합 멤버는 anchor#m<i>. "
             "참조(또는 조합 멤버)가 분류 항목 이름과 정규화 완전 일치(①)하면 그 항목 자체라 그 항목의 anchor 를 쓴다(같은 튜플 — 접힘 아님). 같은 라벨·같은 힌트의 참조도 ① 이라 자리가 달라도 같은 anchor. 규격·수식·계열명 조각이 붙은 라벨은 자기 anchor(미상 칸이 있으면 접히지 않는다)")
ID_RULE = copy.deepcopy(V21.ID_RULE)
ID_RULE["procedure"] = ("세 칸 전부 사전 값이면 PRC-<sha256(what_id|site_id|technique_id)[:10]>, 아니면(site none · technique none · what=CAT- 중 하나라도) PRC-<sha256(what_id|site_id|technique_id|anchor)[:10]>. "
                        "what_id = MOD-/SUB-/PRD-/CAT-, site_id = site 개체 id 또는 'none', technique_id = 기법 사전 id 또는 'none', anchor = CAT- id(분류 항목) · REF- id(참조, REF-sha256(norm(label)|hint)[:10]) · 조합 멤버는 anchor#m<i>. "
                        "v2.2: 미상은 식별자 값이 아니다 — " + FOLD_CONDITION + " 같은 튜플 = 같은 시술")
ID_RULE["reference"] = "REF-<sha256(norm(label)|hint)[:10]> — 참조 하나(정규화 라벨 · 계열 힌트 — 같은 라벨·힌트는 ① 정규화 완전 일치라 자리가 달라도 같다). v2.2 시술 튜플 anchor · decision tuple_assign 의 target.ref_id"

# ---------------------------------------------------------------------------
# 수정 6 — course 출처 문장 (§1.5 · §2.14 · §4 세 곳 같은 문장)
# ---------------------------------------------------------------------------
COURSE_RULE = ("경과(course)는 분해하는 문자열(complications 이름 · 표현 원문) 안의 경과 수식어(일시적 · 지연성 · 영구 · 가역적 등 경과 사전 값과 동의어)에서만 읽는다. "
               "duration · incidence 는 R15 엣지 속성으로만 쓰고 경과 칸을 정하는 데 읽지 않는다. 수식어가 없으면 「미상」.")
_CN = ("complications.json", "categories[].complications[].name")
_TL = lambda k: ("post-procedure-timeline.json", f"timelines[].phases[].{k}[]")  # noqa
_TIS = ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.serious[]")
# v2.2: 값·동의어 출처 = 수식어가 실제로 놓인 이름·표현 원문 잎 키만. v2.1 의 duration·incidence 출처 동의어 2(일과성 · 비가역적)는 어느 이름·표현 원문에도 없어 뺐다(경과 칸을 정하지 않는다)
COURSES = [
    ("일시", [("일시적", _CN), ("가역적", _CN), ("Transient", _CN)], _CN),
    ("지연", [("지연성", _CN), ("Delayed", _CN), ("Late-Onset", _CN), ("LOP", _CN)], _CN),
    ("영구", [("영구적", _TIS)], _TL("emergency")),
    ("재발", [("재활성화", _TL("emergency"))], _TL("caution")),
    ("미상", [], None),
]
COURSE_DROPPED = [("일과성", "일시", "complications.json:categories[].complications[].incidence"), ("비가역적", "영구", "complications.json:categories[].complications[].duration")]

# ---------------------------------------------------------------------------
# 수정 4 — 품질 규칙 ④
# ---------------------------------------------------------------------------
RULE4 = ("신뢰 순위로 풀리는 충돌: 순위가 다른 출처끼리 값이 다르면 높은 순위 값을 자동 채택하고, **채택마다 conflict 레코드를 남긴다** — kind=value_conflict · status=auto_resolved_by_trust · chosen_value=채택 값 · "
         "values[] 에 모든 값과 출처·trust_tier · rule_ref=④. 낮은 값은 실버에 보관. 사람이 뒤집을 때는 decision(kind=conflict_override, target.conflict_id, new_value.chosen_value, status=approved) — 빌드는 approved override 가 있으면 그 값을 쓴다")
QUALITY_RULES = [tuple(r) if r[0] != "④" else ("④", "자동 확정 + 기록", RULE4) for r in V21.QUALITY_RULES]
QUALITY_RULES = [r if r[0] != "⑥" else ("⑥", r[1], r[2] + ". conflict.status=open · rule_ref=⑥") for r in QUALITY_RULES]

# ---------------------------------------------------------------------------
# 수정 5 — decision kind (빌드가 읽는 모양)
# ---------------------------------------------------------------------------
# (kind, build_reads, target 구조체, new_value 구조체, 비고)
DECISION_KINDS = [
    ("dictionary_add", True, "obj(dictionary: 사전 이름)", "obj(canonical: str, synonyms: str[], category: str|null)", "사전에 값·동의어 추가(출처는 source_refs). 빌드는 분해를 다시 돌린다. 검토 §9.5.6·§12-3 의 미등록 조각·제품 사전 확장이 갈 자리"),
    ("tuple_assign", True, "obj(catalog_item_id: CAT-id | ref_id: REF-id — 둘 중 하나)", "obj(what_kind, what_id, site_id, technique_id)", "분해 결과 대신 그 항목·참조의 튜플 세 칸을 지정(「사각턱보톡스 = 보톡스×턱×injection」). 지정값이 세 칸 전부 사전 값이면 접힐 수 있고 아니면 anchor 그대로"),
    ("fold_approve", True, "obj(procedure_ids: str[] ≥2)", "obj(keep_id: str — procedure_ids 중 하나)", "튜플 둘 이상을 하나로. 나머지 id 의 출처·R26·엣지를 keep_id 로 옮기고 나머지 id 는 alias"),
    ("event_split", True, "obj(event: 사건 사전 id)", "obj(new_events: obj[](canonical, synonyms[], category))", "사건 사전 값 하나를 여럿으로(과민반응 ≠ 아나필락시스 등). 옮긴 동의어는 원 값에서 빠진다. 빌드는 부작용 분해를 다시 돌린다"),
    ("canonical_mapping", True, "obj(from_ref: str — 원천 참조(R5:<계열> · what id · 라벨 · 원장 canonical_category 의 항목), scope: str)", "obj(to_id: str)", "from_ref 를 to_id 로 읽는다(scope 안에서만). R5 기법 상속(§9.5.6) · 보톡스 product↔modality(검토 1-E) · 원장 canonical_category(질문 23)가 갈 자리"),
    ("conflict_override", True, "obj(conflict_id: CFL-id)", "obj(chosen_value: any)", "규칙 ④ 자동 해결(auto_resolved_by_trust) 또는 ⑥ open 충돌의 값을 사람이 정한다. conflict.status → resolved · decision_id"),
    ("exclude", True, "obj(id: 아무 개체·튜플·표현·사전 값 id)", "obj(excluded: true)", "실버·골드에서 뺀다(원장은 그대로). 사유는 reason"),
    ("reclassification", True, "obj(catalog_item_id: CAT-id)", "obj(modality_id: MOD-id)", "v1: 원장 reclassified_to → R2 재배치(질문 23)"),
    ("ledger_correction_note", False, "obj(catalog_item_id: CAT-id)", "obj(note: str)", "v1: 원장 교정 메모 보존(classification_issue · correction_note). 빌드가 값을 바꾸지 않는다"),
    ("verification_hold", False, "obj(catalog_item_id: CAT-id)", "obj(hold: true)", "v1: 원장 verification_needed — 확인 대기 표시만"),
    ("conflict_resolution", False, "obj(erd_ref: str — ERD 절·개체·속성 · review_item: str|null)", "obj(disposition: str)", "v1.1: ERD 개정 기록(처분). ERD 문서에 반영 — 빌드가 다시 적용하지 않는다"),
    ("scope_review", False, "obj(erd_ref: str — ERD 절·개체·관계 · review_item: str|null)", "obj(disposition: str)", "v1.1~: ERD 개정 기록(구조 변경·범위). ERD 문서에 반영 — 빌드가 다시 적용하지 않는다"),
]
DECISION_KINDS_NEW = ["dictionary_add", "tuple_assign", "fold_approve", "event_split", "canonical_mapping", "conflict_override", "exclude"]
DECISION_COMMON_FIELDS = ["id", "kind", "target", "new_value", "reason", "decided_by", "decided_at", "status", "source_refs"]
DECISION_STATUS = ["proposed", "approved", "rejected"]
DECISION_BUILD_RULE = "빌드는 status=approved 인 결정만 읽는다(proposed·rejected 는 목록만). build_reads=true 인 kind 만 실버 값을 바꾼다 — 나머지 kind 는 ERD 개정·원장 메모 기록"

# ---------------------------------------------------------------------------
# 분해 규칙 (참조 §1.3 — v2.1 그대로 + 수정 2 의 미해결 사유)
# ---------------------------------------------------------------------------
RESOLVE_RULES = copy.deepcopy(V21.RESOLVE_RULES)
RESOLVE_RULES["name"] = "decompose_v2_2"
RESOLVE_RULES["step3_assemble"]["unresolved"] += (". v2.2: 미등록 조각이 없어도 primary 조각 둘 이상(조합 아님) · site 조각 둘 이상 · technique 조각 둘 이상 · what 으로 못 쓰는 primary 조각이 있으면 "
                                                  "튜플 단계(§1.4)에서 미해결(⑨ · unresolved_reason=multi_primary|multi_site|multi_technique|unusable_primary|combo_outside_fragment) — 버리고 접지 않는다")

# ---------------------------------------------------------------------------
# 개체 — 구조 그대로(21). procedure · catalog_item · adverse_effect · conflict · decision 갱신
# ---------------------------------------------------------------------------
ENTITIES = copy.deepcopy(V21.ENTITIES)


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


_p = _ent("procedure")
_p["definition"] = ("**단위 시술 = 튜플 (what, site, technique)** — 무엇을 × 어디에 × 어떻게. what = modality | modality_subcategory | product (사전 값) 또는 catalog_item(분류 항목 자신). "
                    + FOLD_RULE + ". "
                    "**조각을 버리고 접지 않는다**(v2.2): 분류 항목 이름의 조각이 전부 사전에 닿았어도 primary(what 후보) 조각이 둘 이상(조합 아님) · site 조각이 둘 이상 · technique 조각이 둘 이상 · what 으로 못 쓰는 primary 조각이 있으면 사전 값으로 조립하지 않는다 — "
                    "분류 항목은 what = 항목 자신(status ambiguous · 조각 전부 extra_primaries/extra_sites 에 실값), 참조(②③)는 미해결(⑨). 같은 계열의 계열명 조각(what 의 계열과 같은 modality 조각)은 what 의 상위(R1·R4)로 이미 담기므로 버린 조각이 아니다. "
                    "조각 중 하나라도 미등록이면 v2.1 그대로 what = 항목 자신(partial · candidate_name). primary 조각이 없으면(부위만·계열명만) 항목 자신(complete). 부모 하위분류 fallback 없음. "
                    "site = 부위 사전 값 | none. technique = 이름 조각이 기법 사전에 닿을 때만 그 값 | none — **R5 계열 기법 상속은 하지 않는다**(v2.2 · 결정 kind canonical_mapping 후보로만 §9.5.6). "
                    "원천: ① 분류 항목 521 ② 자유 텍스트 참조(§9.2 자리 전부) ③ market-pricing 122. 조합 기호로 같은 묶음 안에 primary 멤버가 둘 이상이고 멤버 밖에 primary·site 조각이 없으면 package(kind=combo_ref)로 보내고 멤버 각각을 튜플화한다.")
_p["identity"] = ID_RULE["procedure"]
_attrs = []
for a in _p["attrs"]:
    n = a[0]
    if n == "what_kind":
        a = (n, a[1], True, [], "무엇을. §1.4 what 규칙(v2.2: primary 조각이 하나일 때만 사전 값 what · 미등록 있으면 partial · 둘 이상·못 쓰면 ambiguous · 없으면 complete — 셋 다 catalog_item = 항목 자신)")
    elif n == "technique_id":
        a = (n, a[1], False, a[3], "기법 사전 값 또는 none. **이름 조각이 기법 사전에 닿을 때만**(fragment). R5 계열 상속 없음(v2.2) — 상속은 decision kind canonical_mapping(target.from_ref=R5:<계열>)이 approved 일 때만")
    elif n == "technique_origin":
        a = (n, "enum(fragment|none)", True, [], "v2.2: inherited 삭제. canonical_mapping 결정으로 붙은 값은 실버 빌드에서 decision 출처(decision_id)로 남는다")
    elif n == "status":
        a = (n, "enum(complete|partial|ambiguous)", True, [], "complete = 미등록 조각 0 · partial = 미등록 조각 ≥1 · ambiguous(v2.2) = 조각은 전부 닿았지만 primary·site·technique 가 둘 이상이거나 what 으로 못 쓰는 primary 가 있어 사전 값으로 조립하지 않은 분류 항목 자신 튜플")
    _attrs.append(a)
    if n == "site_id":
        pass
_attrs.append(("anchor", "str|null", True, [], "v2.2 식별자 anchor. 세 칸 전부 사전 값이면 null(접힘 가능), 아니면 CAT- id(분류 항목) · REF- id(참조 자리) · …#m<i>(조합 멤버) — 식별자에 들어가 항목·참조마다 고유"))
_attrs.append(("all_dict_values", "bool", True, [], "v2.2: what·site·technique 세 칸이 전부 사전 값(미상 없음)이면 true — 그때만 접힘"))
_attrs.append(("extra_primaries", "str[]", True, [], "v2.2: 사전 값 what 튜플이면 [](버린 primary 없음). 항목 자신 튜플이면 이름에서 닿은 primary 조각 전부(실값 · null 아님)"))
_attrs.append(("extra_sites", "str[]", True, [], "v2.2: 칸에 들어가지 않은 부위 조각 전부(실값 · null 아님). 사전 값 what 튜플이면 []"))
_p["attrs"] = _attrs
_ent("catalog_item")["definition"] += (" v2.2: 이름 조각에 primary·site·technique 가 둘 이상이거나 what 으로 못 쓰는 primary 가 있어도 항목 자신이 what(tuple_status ambiguous) — 버리고 접지 않는다. "
                                       "항목 자신 튜플은 식별자에 CAT- anchor 가 들어가 항목마다 고유하다.")
_ent("catalog_item")["attrs"] = [a if a[0] != "tuple_status" else ("tuple_status", "enum(complete|partial|ambiguous)", False, [], "분해 결과: complete = 미등록 조각 0 · partial = 미등록 조각 ≥1 · ambiguous(v2.2) = primary/site/technique 둘 이상 또는 what 으로 못 쓰는 primary(항목 자신 what)")
                                 for a in _ent("catalog_item")["attrs"]]

_a = _ent("adverse_effect")
_a["attrs"] = [a if a[0] != "course" else ("course", "dict:course", True, ["complications.json:categories[].complications[].name"], COURSE_RULE) for a in _a["attrs"]]

_c = _ent("conflict")
_c["definition"] = ("같은 사실에 원장 값이 다르면 기계가 남기는 레코드 — 신뢰 순위로 자동 해결된 것(④ · status=auto_resolved_by_trust)도, 순위로 안 풀리는 것(⑥ · open)도 전부. 유사도만 높은 중복(⑦), 사전 밖 값(⑧), 참조 깨짐·미해결(⑨)도 같다. "
                    "실버에 값 전부 보관, 골드는 open 제외(auto_resolved_by_trust 는 chosen_value 로 골드에 간다). 사람 판정은 decision(kind=conflict_override)으로만.")
_cattrs = []
for a in _c["attrs"]:
    if a[0] == "values":
        a = ("values", "obj[](value, source_file, source_path, trust_tier)", True, a[3], a[4] + " · v2.2: trust_tier 는 필수(④ 판정 근거)")
    elif a[0] == "status":
        a = ("status", "enum(open|auto_resolved_by_trust|resolved|dismissed)", True, [], "v2.2: ④ 자동 채택 = auto_resolved_by_trust · ⑥~⑨ 사람 판정 전 = open · conflict_override 결정(approved) 적용 = resolved")
    _cattrs.append(a)
    if a[0] == "resolution_rule":
        _cattrs.append(("rule_ref", "enum(④|⑥|⑦|⑧|⑨)", True, [], "v2.2: 이 레코드를 만든 규칙 번호(§5)"))
        _cattrs.append(("chosen_value", "any|null", False, [], "v2.2: ④ 자동 채택 값(높은 순위 값) 또는 conflict_override 의 값. ⑥ open 은 null"))
_c["attrs"] = _cattrs

_d = _ent("decision")
_d["definition"] = ("사람이 판정한 레코드. 원장은 고치지 않고 결정만 쌓는다. **실버 빌드가 그대로 읽어 적용하는 모양**(v2.2): 공통 필드 id · kind · target(구조체) · new_value(구조체) · reason · decided_by · decided_at · status(proposed|approved|rejected) · source_refs[] — "
                    "target·new_value 의 모양은 kind 마다 정해져 있다(§5.2 표). " + DECISION_BUILD_RULE + ". taxonomy 안의 교정 메모 키는 원장 작성자 결정(status=approved · decided_by=원장 작성자)으로 적재한다(질문 23).")
_d["identity"] = "DEC-<적용일>-<일련 2자리> (적용일 = 레코드 적재일)"
_d["attrs"] = [
    ("id", "str", True, [], "DEC-YYYY-MM-DD-NN"),
    ("kind", "enum(" + "|".join(k[0] for k in DECISION_KINDS) + ")", True, [], "§5.2 표. 빌드 적용 kind(build_reads=true): " + " · ".join(k[0] for k in DECISION_KINDS if k[1])),
    ("target", "obj(kind별)", True, [], "무엇에 적용하나 — kind별 구조체(§5.2). v2.1 applies_to · resolves_conflict_id 를 대신한다"),
    ("new_value", "obj(kind별)", True, ["taxonomy.json:modality[].subcategories[].items[].reclassified_to", "taxonomy.json:modality[].subcategories[].items[].canonical_category"],
     "무엇으로 — kind별 구조체(§5.2). reclassified_to → reclassification.modality_id · canonical_category → canonical_mapping.to_id(하위분류 사전 일치만)"),
    ("reason", "str", True, ["taxonomy.json:modality[].subcategories[].items[].classification_issue", "taxonomy.json:modality[].subcategories[].items[].correction_note", "taxonomy.json:modality[].subcategories[].items[].verification_needed"],
     "왜(v2.1 what+why). 원장 메모는 원문 그대로"),
    ("decided_by", "str|null", True, [], "승인한 사람. status=proposed 면 null(제안 주체는 reason · source_refs) — 승인 시점에 채운다(검토 3-E). 원장 메모는 `원장 작성자(taxonomy.json)`"),
    ("decided_at", "date|null", True, [], "승인 일자. proposed 면 null. 원장 메모는 null(원장에 일자 없음)"),
    ("status", "enum(proposed|approved|rejected)", True, [], DECISION_BUILD_RULE),
    ("source_refs", "obj[](kind: ledger|brief|review|erd, ref: str)", True, [], "근거 — 원장 (파일:키 경로[레코드]) · 발주서 · 검토서 · ERD 절"),
]

# ---------------------------------------------------------------------------
# 관계 — 구조 그대로(31). R23·R24·R26·R27 비고, R15 비고(course)
# ---------------------------------------------------------------------------
RELATIONS = copy.deepcopy(V21.RELATIONS)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


_rel("R26")["note"] = "분류 항목 하나 → 튜플 하나. v2.2: 접힘은 " + FOLD_CONDITION + " — 미상 칸이 있거나 what 이 CAT- 인 튜플은 식별자에 CAT- anchor 가 들어가 1:1. §9.5 접힌 표"
_rel("R26")["attrs"] = [("decomposition", "obj(what_basis, fragments{primaries,sites,techniques}, family_fragments, extra_primaries, extra_sites, qualifiers, unregistered_fragments, self_reason)", "항목 이름을 어떻게 분해해 이 튜플이 됐는지(§1.4) · v2.2 extra_* 는 실값")]
_rel("R27")["note"] = "튜플의 what 축. §1.4 what 규칙. v2.2: primary 조각이 하나일 때만 사전 값 what — 미등록·둘 이상·못 쓰는 primary·primary 없음이면 what=catalog_item(항목 자신)"
_rel("R23")["note"] = "다형 참조 (target_type, target_id). v2.2: ④ 자동 해결(auto_resolved_by_trust)도 이 엣지를 가진다"
_rel("R24")["note"] = "decision.target 구조체(kind별)가 끝점 — 개체·튜플·참조(REF-)·사전 값·충돌(conflict_override.target.conflict_id). v2.2: 빌드는 status=approved 만 따라간다"
_r15 = _rel("R15")
_r15["note"] = (_r15.get("note") or "") + ". v2.2: duration · incidence 는 이 엣지의 속성으로만 — 경과 칸(adverse_effect.course)을 정하지 않는다"

ERD_ENUMS = copy.deepcopy(V21.ERD_ENUMS)
ERD_ENUMS["procedure.technique_origin"] = ["fragment", "none"]
ERD_ENUMS["procedure.status"] = ["complete", "partial", "ambiguous"]
ERD_ENUMS["catalog_item.tuple_status"] = ["complete", "partial", "ambiguous"]
ERD_ENUMS["reference.unresolved_reason"] = ["unregistered", "multi_primary", "multi_site", "multi_technique", "unusable_primary", "combo_outside_fragment"]
ERD_ENUMS["conflict.status"] = ["open", "auto_resolved_by_trust", "resolved", "dismissed"]
ERD_ENUMS["conflict.rule_ref"] = ["④", "⑥", "⑦", "⑧", "⑨"]
ERD_ENUMS["decision.kind"] = [k[0] for k in DECISION_KINDS]
ERD_ENUMS["decision.status"] = list(DECISION_STATUS)
ERD_ENUMS["decision.source_refs.kind"] = ["ledger", "brief", "review", "erd"]

# ---------------------------------------------------------------------------
# 튜플 규칙 v2.2 (데이터) — erd-v2.2-tuples.py 가 그대로 실행
# ---------------------------------------------------------------------------
TUPLE_RULES = copy.deepcopy(V21.TUPLE_RULES)
TUPLE_RULES["name"] = "tuples_v2_2"
_P = TUPLE_RULES["procedure"]
_P["fold_condition"] = FOLD_CONDITION
_P["fold_rule"] = FOLD_RULE
_P["technique_inheritance"] = False
_P["what"] = [
    "접힘 조건(v2.2): " + FOLD_CONDITION + " — what·site·technique 가 전부 사전 값일 때만 식별자에 anchor 가 없고 다른 항목·참조와 접힌다. 미상 칸이 하나라도 있으면 anchor(CAT-/REF-)로 항목·참조마다 고유",
    "product 조각(계열 안 우선, 없으면 전 계열) → what=product",
    "catalog_item 조각 → 그 항목의 튜플 what. 분류 항목(①)에서는 그 항목의 what 이 사전 값일 때만 — 항목 자신이 what 인 항목에 닿은 조각은 what 으로 못 쓰는 primary(unusable_primary → 항목 자신 · ambiguous)",
    "modality_subcategory 조각 → what=modality_subcategory (분류 항목에서 다른 계열 라벨은 못 쓰는 primary)",
    "modality 조각 → what=modality (참조 ②③). 분류 항목(①)에서 자기 계열명 조각은 R2 상위로 이미 담긴 family_fragments(버린 조각 아님), 다른 계열명 조각은 못 쓰는 primary. 참조에서도 what 의 계열과 같은 계열명 조각은 family_fragments",
    "조각이 계열 사전과 제품 색인 양쪽에 닿으면(보톡스·필러) what 은 product (v2.1 그대로 — 검토 1-E 는 결정 레코드 몫)",
    "**버리고 접지 않는다**(v2.2 · v2.1 규칙 8 삭제): 조합이 아닌데 primary 조각이 둘 이상이면(같은 what 을 가리키는 조각은 하나로 센다) 사전 값으로 조립하지 않는다 — 분류 항목은 항목 자신(ambiguous · reason multi_primary), 참조는 미해결(⑨ · multi_primary)",
    "what 으로 못 쓰는 primary 조각이 하나라도 있으면 같은 처리(reason unusable_primary)",
    "분류 항목(①): 조각 중 하나라도 미등록이면 what = 항목 자신(partial · candidate_name). primary 가 없으면 항목 자신(complete · reason no_primary). 부모 하위분류 fallback 없음",
    "참조 ②③: 미등록 조각이 있으면 미해결(⑨ · unregistered). primary 가 없으면 자리 힌트 계열(hint_family), 힌트도 없으면 튜플 불가",
]
_P["site"] = ("site 사전(21) 에 닿은 조각. 서로 다른 부위 조각이 **둘 이상이면 사전 값으로 조립하지 않는다**(v2.2) — 분류 항목은 항목 자신(ambiguous · multi_site · site=none · extra_sites 에 전부), 참조는 미해결(⑨ · multi_site). "
              "참조가 분류 항목에 닿았고 그 항목 튜플에 site 가 있으면 그 값도 센다. 없으면 none(미상 — 식별자 값 아님). 사전에 없는 부위 같은 조각은 미등록 조각")
_P["technique"] = ("조각이 기법 사전(12)에 닿으면 그 값(fragment). 아니면 **none**(v2.2: R5 계열 상속 삭제 — 미상은 미상). 서로 다른 기법 조각이 둘 이상이면 site 와 같은 처리(multi_technique). "
                   "R5 계열 → 기법 상속은 decision kind canonical_mapping(target.from_ref=R5:<계열>, target.scope) 후보로만 §9.5.6 에 목록")
_P["combo"] += ". v2.2: 멤버 밖(다른 묶음·멤버)에 primary·site·technique 조각이 있으면(멤버 what 의 계열명 조각 제외) 조합으로 보내지 않고 미해결(combo_outside_fragment). 멤버마다 같은 규칙 — 멤버가 모호하면 전체 미해결"
_P["qualifiers"] = "spec(규격)·product_tier 조각은 튜플 칸이 아니라 수식이다 — 참조 레코드(R9/R12/R18 target_label 등) 쪽에 남긴다. v2.2: primary·site·technique 조각은 수식이 아니다(둘 이상이면 위 규칙대로 미해결·항목 자신, 버리지 않는다)"
_P["extra"] = "extra_primaries · extra_sites 는 항상 실제 값 목록(null 아님). 사전 값 what 튜플이면 [] (버린 조각 없음), 항목 자신 튜플·미해결 참조면 닿은 조각 전부"
_P["status"] = "complete = 미등록 조각 0 · partial = 미등록 조각 ≥1 · ambiguous = 조각 전부 닿았지만 둘 이상·못 쓰는 primary (분류 항목은 셋 다 튜플을 만들되 partial·ambiguous 는 항목 자신이 what · 참조는 partial·ambiguous 면 미해결)"
_P["id"] = ID_RULE["procedure"]
_Q = TUPLE_RULES["adverse"]
_Q["course"] = COURSE_RULE
_Q["tuple"] = _Q["tuple"].replace("site·course 는", "site·course(§1.5 경과 규칙) 는")
