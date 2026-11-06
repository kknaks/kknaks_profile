# -*- coding: utf-8 -*-
"""ERD v2 명세 (데이터). erd_spec_v11.py(v1.1) 를 읽어 구조 변경 2건만 덧씌운다.
  ① 시술 축: catalog_item(분류 항목 521 그대로) 과 procedure(what × site × technique 튜플) 분리
  ② 부작용: adverse_event_type(사건 사전) + course(경과 사전) + adverse_effect(event × site × course 튜플) + adverse_expression(원문 표현)
그 밖의 개체·관계·속성·사전·규칙·처분은 v1.1 그대로다. erd_build_v2.py 가 읽는다. v1·v1.1 명세는 손대지 않는다.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v11 as V11  # noqa

ERD_VERSION = "v2"
SNAPSHOT = V11.SNAPSHOT
LEDGER_DIR = V11.LEDGER_DIR
STEP1_FILE = V11.STEP1_FILE
STEP1_TIER2_SOURCE_RE = V11.STEP1_TIER2_SOURCE_RE
SOURCE_FILES = list(V11.SOURCE_FILES)
SOURCE_KIND = dict(V11.SOURCE_KIND)
TRUST_FLAGS = dict(V11.TRUST_FLAGS)
NORMALIZE_RULE = copy.deepcopy(V11.NORMALIZE_RULE)
ID_RULE = copy.deepcopy(V11.ID_RULE)
ID_RULE["procedure"] = "PRC-<sha256(what_id|site_id|technique_id)[:10]>. what_id = MOD-/SUB-/PRD- 개체 id, site_id = site 개체 id 또는 'none', technique_id = 기법 사전 id 또는 'none'. 같은 튜플 = 같은 시술"
ID_RULE["adverse_effect"] = "ADV-<sha256(event_id|site_id|course_id)[:10]>. event_id = 사건 사전 id, site_id = site 개체 id | 상대 부위 사전 id | 'none', course_id = 경과 사전 id('미상' 포함). 같은 튜플 = 같은 단위 부작용"
ID_RULE["catalog_item"] = "CAT-<sha256(계열 코드|norm(항목 이름))[:10]> — v1.1 procedure 의 식별자 규칙을 그대로 물려받는다"
ID_RULE["adverse_expression"] = "AEX-<sha256(출처 파일|잎 키 경로|레코드 위치|lang)[:10]> — 원문 레코드 하나가 표현 하나"
QUALITY_RULES = list(V11.QUALITY_RULES)
Q25 = list(V11.Q25)
DISPOSITIONS = dict(V11.DISPOSITIONS)
SITE_LABELS_KEEP = list(V11.SITE_LABELS_KEEP)
Q14_ORAL_DRUGS = list(V11.Q14_ORAL_DRUGS)
RESOLVE_RULES = copy.deepcopy(V11.RESOLVE_RULES)
RESOLVE_RULES["step2_decompose"]["dictionary_order_note"] = "v2: 사전 순서의 'procedure' 자리는 catalog_item_name(분류 항목 이름 색인)을 읽는다. 값·순서는 v1.1 그대로"

# ---------------------------------------------------------------------------
# 1. 개체 — v1.1 19 + catalog_item + adverse_expression = 21
# ---------------------------------------------------------------------------
ENTITIES = copy.deepcopy(V11.ENTITIES)


def _idx(key):
    return next(i for i, e in enumerate(ENTITIES) if e["key"] == key)


def _ent(key):
    return ENTITIES[_idx(key)]


# --- ① catalog_item: v1.1 procedure 를 통째로 옮긴다 (속성·alias·출처 전부)
_old_proc = _ent("procedure")
CATALOG_ITEM = copy.deepcopy(_old_proc)
CATALOG_ITEM.update({
    "key": "catalog_item", "prefix": "CAT", "label": "분류 항목(taxonomy 항목)", "beyond_minimum": True,
    "definition": ("taxonomy modality 항목 521 을 **있는 그대로** 담는 분류 항목. taxonomy 는 제품·마케팅명·부위 붙은 메뉴·기법이 섞인 분류 트리(10-27 결정)라 "
                   "단위 시술이 아니다. v1.1 `procedure` 의 속성·alias·출처를 전부 여기로 옮겼다. 계층(계열→하위분류→항목)도 그대로(R1·R2). "
                   "각 항목은 분해 규칙(§1.4)으로 튜플 하나(procedure)로 내려가고 R26 derived_from 으로 매단다."),
    "identity": "계열 코드 + 정규화 항목 이름 (v1.1 procedure 와 같음)",
    "aliases": "taxonomy items[].id (M1-2-1 · auto-M4-… · auto-63-… 전부) — 외부 참조 여부 무관하게 alias (질문 4). v1.1 PRC- id 는 CAT- 로 바뀐다(canonical_key 는 같음)",
})
CATALOG_ITEM["attrs"] = list(CATALOG_ITEM["attrs"]) + [
    ("tuple_status", "enum(complete|partial)", True, [], "분해 결과: complete = 미등록 조각 0, partial = 미등록 조각 ≥1 (procedure 는 둘 다 만든다, what 은 항상 확정)"),
    ("unregistered_fragments", "str[]", False, [], "이름 분해에서 어느 사전에도 닿지 않은 조각(공백 토큰 단위). 사전 추가는 이번 범위 아님 — 목록만"),
]
ENTITIES.insert(_idx("procedure"), CATALOG_ITEM)

# --- ① procedure: 튜플 (what, site, technique)
_SRC_REFS = [
    "taxonomy.json:modality[].subcategories[].items[].name",
    "market-pricing.json:categories[].items[].name",
    "synergy.json:links[].from", "synergy.json:links[].to",
    "problem-packages.json:problems[].complaints[].procedures[].name", "problem-packages.json:problems[].complaints[].combos[].combo[]", "problem-packages.json:problems[].complaints[].procedures[].products[]",
    "procedure-comparison.json:comparisons[].procedures[].name",
    "treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]", "treatment-optimization.json:by_age_group[].recommended_base[]", "treatment-optimization.json:by_age_group[].avoid[]", "treatment-optimization.json:by_age_group[].upgrade[]", "treatment-optimization.json:annual_plans[].schedule[].procedures[]",
    "treatment-sequence.json:sequence_order[].categories[]", "treatment-sequence.json:incompatible_same_day[].pair[]", "treatment-sequence.json:minimum_intervals[].from", "treatment-sequence.json:minimum_intervals[].to", "treatment-sequence.json:common_combos[].sequence[]",
    "post-procedure-timeline.json:timelines[].name",
]
_ent("procedure").update({
    "definition": ("**단위 시술 = 튜플 (what, site, technique)** — 무엇을 × 어디에 × 어떻게. what = modality | modality_subcategory | product 중 하나(필수): 분류 항목이 제품명이면 product, "
                   "아니면 가장 구체적인 계열 층. site = 부위 사전 값 | none(부위 미상 · 「전체얼굴」처럼 사전에 없는 조각은 미등록 조각 기록 + none). "
                   "technique = 기법 사전 값 | 계열 기본값 상속(R5 계열→기법, 기법이 하나인 계열만) | none. "
                   "원천: ① 분류 항목 521 의 분해(§1.4) ② 자유 텍스트 참조(§9.2 자리 전부)의 분해 ③ market-pricing 메뉴 122. 같은 튜플 = 같은 시술이며 여러 분류 항목이 같은 튜플이면 R26 derived_from(1:N) 으로 매단다. "
                   "조합 기호(+·/)로 같은 묶음 안에 멤버(primary 조각)가 둘 이상이면 시술이 아니라 package(kind=combo_ref) 로 보내고 멤버 각각을 튜플화한다."),
    "identity": "sha256(what_id|site_id|technique_id)[:10] — 튜플 자체가 식별자",
    "aliases": "없음 (분류 항목 id·이름은 catalog_item 의 alias. 참조 원문은 엣지 속성 target_label)",
    "beyond_minimum": False,
})
_ent("procedure")["attrs"] = [
    ("what_kind", "enum(modality|modality_subcategory|product)", True, [], "무엇을. §1.4 what 규칙(제품 > 하위분류 > 계열 · 분류 항목 조각은 그 항목의 what 종류로 비교)"),
    ("what_id", "str", True, _SRC_REFS, "MOD-/SUB-/PRD- 개체 id (R27). 출처 = 튜플을 만든 이름·참조 자리"),
    ("site_id", "str|none", True, [], "site 개체 id 또는 none (R28). 부위 사전 21(v1.1 그대로, 공유 사전)"),
    ("technique_id", "dict:technique|none", True, ["procedure-profiles.json:profiles[].mechanism[]"], "기법 사전 값 또는 none. 이름 조각이 기법 사전에 닿으면 그 값, 아니면 계열의 R5 기법이 하나일 때만 상속, 둘 이상이면 none(상속 불가 · §9.5)"),
    ("technique_origin", "enum(fragment|inherited|none)", True, [], "기법이 어디서 왔는지"),
    ("origins", "enum[](catalog_item|reference|market_pricing)", True, [], "① ② ③ 중 이 튜플을 만든 원천(합집합)"),
    ("status", "enum(complete|partial)", True, [], "complete = 이 튜플을 만든 모든 이름이 미등록 조각 0 · partial = 하나라도 미등록 조각 있음"),
    ("unregistered_fragments", "str[]", False, [], "이 튜플을 만든 이름들의 미등록 조각(합집합)"),
]

# --- ② adverse_effect: 튜플 (event, site, course)
_ADV_PHRASE_SRC = [
    "complications.json:categories[].complications[].name",
    "literature-evidence.json:categories.{code}.adverse_effects[].statement", "literature-evidence.json:categories.{code}.adverse_effects[].patient_ko",
    "consent-checklist.json:categories[].emergency_signs[]",
    "post-procedure-timeline.json:timelines[].phases[].normal[]", "post-procedure-timeline.json:timelines[].phases[].abnormal[]", "post-procedure-timeline.json:timelines[].phases[].caution[]", "post-procedure-timeline.json:timelines[].phases[].emergency[]",
    "extracted.json:{code}.safety.common[]", "extracted.json:{code}.safety.uncommon[]", "extracted.json:{code}.safety.serious[]", "extracted.json:{code}.safety.emergency[]",
    "taxonomy.json:modality[].extracted.safety.common[]", "taxonomy.json:modality[].extracted.safety.uncommon[]", "taxonomy.json:modality[].extracted.safety.serious[]",
    "taxonomy.json:modality[].subcategories[].items[].extracted.safety.common[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.long_term[]",
    "taxonomy.json:modality[].products[].extracted.safety.common[]", "taxonomy.json:modality[].products[].extracted.safety.serious[]", "taxonomy.json:modality[].products[].extracted.safety.common_side_effects[]",
]
_ent("adverse_effect").update({
    "definition": ("**단위 부작용 = 튜플 (event, site, course)**. event = 사건 사전(adverse_event_type) 값, site = 공유 부위 사전 21 | 상대 부위 사전(주사 부위·시술 부위) | none, course = 경과 사전(일시·지연·영구·재발·미상). "
                   "v1.1 은 정규화 문자열이 식별자라 「멍」 4표기가 4개체였다 — v2 는 같은 튜플 = 같은 단위 부작용. 원인 시술은 튜플에 넣지 않고 R15 may_cause 로만 연결하며 "
                   "등급·빈도·발생 시기·지속·대처·예방·위험 요인·예상/이상/주의/응급 표시는 전부 R15 엣지 속성(v1.1 과 같음). 원문 문장·문구·환자 설명은 adverse_expression 이 담고 R29 expresses 로 닿는다. "
                   "「혈관 폐색」→「피부 괴사」같은 인과는 R30 leads_to."),
    "identity": "sha256(event_id|site_id|course_id)[:10] — 튜플 자체가 식별자",
    "aliases": "없음 (표면형은 사건 사전 동의어 또는 adverse_expression.text)",
})
_ent("adverse_effect")["attrs"] = [
    ("event", "dict:adverse_event_type", True, ["complications.json:categories[].complications[].name"], "사건 사전 값. 뼈대 = complications.json 65 이름의 분해. 사전에 없는 조각은 미등록"),
    ("site_ref_kind", "enum(site|relative|none)", True, [], "site 개체(R31) | 상대 부위 사전(relative_site) | none"),
    ("site_ref_id", "str|none", True, [], "site 개체 id 또는 relative_site 사전 id 또는 none"),
    ("course", "dict:course", True, ["complications.json:categories[].complications[].name", "complications.json:categories[].complications[].duration"], "이름 수식어(일시적·지연성·가역적·영구·재발)에서. 없으면 「미상」"),
    ("status", "enum(complete|partial)", True, [], "이 튜플을 만든 문구가 전부 미등록 조각 0 이면 complete"),
    ("unregistered_fragments", "str[]", False, [], "이 튜플을 만든 문구들의 미등록 조각(합집합)"),
    ("origins", "str[]", True, _ADV_PHRASE_SRC, "이 튜플을 만든 문구의 출처 잎 키(합집합)"),
]

# --- ② adverse_expression: 원문 표현
ADVERSE_EXPRESSION = {
    "key": "adverse_expression", "prefix": "AEX", "label": "부작용 표현(원문)", "beyond_minimum": True,
    "definition": ("문헌 부작용 문장(32) · 시술 후 타임라인 문구 · consent/extracted 응급 징후 · 환자 설명(4개 언어) · extracted/taxonomy safety 문구를 담는 원문 레코드. "
                   "분해 규칙(§1.5)으로 튜플에 닿으면 R29 expresses 로 연결, 아니면 null + 미등록 조각 기록. v1.1 evidence_statement 중 adverse_effects 섹션 분(v1.1 adverse_effect kind=literature_claim)은 여기로 옮겼고 moa/effects 섹션은 evidence_statement 그대로. "
                   "타임라인 normal 문구는 사건 사전의 원천이 아니며 표현(kind=symptom_phrase)으로만 두고 R15 엣지 속성 reaction_level=normal 로 표시한다."),
    "identity": "출처 파일 + 잎 키 경로 + 레코드 위치 + lang",
    "aliases": "없음",
    "attrs": [
        ("kind", "enum(evidence_statement|symptom_phrase|emergency_sign|patient_text|safety_phrase)", True, [], "출처 키에서: literature adverse_effects statement → evidence_statement · timeline 문구 → symptom_phrase · consent emergency_signs → emergency_sign · literature patient_* → patient_text · extracted/taxonomy safety.* → safety_phrase"),
        ("text", "str", True, [
            "literature-evidence.json:categories.{code}.adverse_effects[].statement",
            "post-procedure-timeline.json:timelines[].phases[].normal[]", "post-procedure-timeline.json:timelines[].phases[].abnormal[]", "post-procedure-timeline.json:timelines[].phases[].caution[]", "post-procedure-timeline.json:timelines[].phases[].emergency[]",
            "consent-checklist.json:categories[].emergency_signs[]",
            "extracted.json:{code}.safety.common[]", "extracted.json:{code}.safety.uncommon[]", "extracted.json:{code}.safety.serious[]", "extracted.json:{code}.safety.emergency[]",
            "taxonomy.json:modality[].extracted.safety.common[]", "taxonomy.json:modality[].extracted.safety.uncommon[]", "taxonomy.json:modality[].extracted.safety.serious[]",
            "taxonomy.json:modality[].subcategories[].items[].extracted.safety.common[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.long_term[]",
            "taxonomy.json:modality[].products[].extracted.safety.common[]", "taxonomy.json:modality[].products[].extracted.safety.serious[]", "taxonomy.json:modality[].products[].extracted.safety.common_side_effects[]",
        ], "원문 그대로(브론즈 바이트). 각주 `[n]`·언어 섞임 정제는 실버 빌더(질문 19)"),
        ("patient_text", "str", False, ["literature-evidence.json:categories.{code}.adverse_effects[].patient_ko", "literature-evidence.json:categories.{code}.adverse_effects[].patient_en", "literature-evidence.json:categories.{code}.adverse_effects[].patient_zh", "literature-evidence.json:categories.{code}.adverse_effects[].patient_ja"], "kind=patient_text 는 언어별로 표현 레코드 하나(lang). 같은 문헌 레코드의 statement 표현과 같은 튜플에 닿는다(§1.5 문헌 규칙)"),
        ("lang", "enum(ko|en|zh|ja)|null", False, [], "patient_text 만. 그 밖은 null(원문 언어 판정 안 함)"),
        ("accuracy_score", "int", False, ["literature-evidence.json:categories.{code}.adverse_effects[].accuracy_score"], "v1.1 adverse_effect 에서 이동"),
        ("accuracy_note", "str", False, ["literature-evidence.json:categories.{code}.adverse_effects[].accuracy_note"], "v1.1 adverse_effect 에서 이동"),
        ("added_at", "date", False, ["literature-evidence.json:categories.{code}.adverse_effects[].added_at"], "v1.1 adverse_effect 에서 이동"),
        ("modality_code", "str|null", False, [], "문구가 놓인 자리의 계열(코드 키·categories[].id·timeline category). R15 엣지의 from 끝 힌트"),
        ("context", "obj(frequency_class|reaction_level|period|phase_label|item_name|product_name)", False, [], "문구가 놓인 자리의 분류 키(동의 키 정규화 ③). 튜플에 닿으면 R15 엣지 속성으로도 복사, 못 닿으면 여기만"),
        ("citation_present", "bool", False, [], "문헌 표현은 R19 cites"),
        ("match_status", "enum(linked|unlinked)", True, [], "R29 가 있으면 linked"),
        ("unregistered_fragments", "str[]", False, [], "분해에서 어느 사전에도 닿지 않은 조각"),
    ],
}
ENTITIES.insert(_idx("adverse_effect") + 1, ADVERSE_EXPRESSION)

# --- evidence_statement 정의 문구만 갱신
_ent("evidence_statement")["definition"] = "literature-evidence 의 moa·effects 문장(87). 인용 개체와 연결되고 환자용 4개 국어 문장을 가진다. adverse_effects 문장(32)은 v2 에서 adverse_expression(kind=evidence_statement)으로 간다."
# --- technique 정의: 계열 기본값 상속에 쓰인다
_ent("technique")["definition"] += " v2: procedure 튜플의 technique 축. 이름 조각이 닿지 않으면 R5 의 계열 기법을 상속하되 기법이 하나인 계열만(둘 이상이면 none)."
# --- site 정의: 공유 사전
_ent("site")["definition"] += " v2: procedure 튜플과 adverse_effect 튜플이 함께 쓰는 공유 사전(21 유지). 상대 부위(주사 부위·시술 부위)는 별도 사전 relative_site."
# --- package: combo_ref
_ent("package")["attrs"][0] = ("kind", "enum(consult_package|recipe|session_combo|cc_combo|optimization_plan|annual_plan|comparison|combo_ref)", True, [], "출처 파일별 고정. v2: combo_ref = 이름 분해에서 조합 기호(+·/)로 멤버가 둘 이상인 참조(멤버는 각각 procedure 튜플, R12)")
_ent("package")["definition"] += " v2: 분해에서 조합 기호로 멤버가 둘 이상인 참조는 kind=combo_ref 패키지로 보내고 멤버 각각을 procedure 튜플로 R12 에 매단다."

# ---------------------------------------------------------------------------
# 2. 관계 — v1.1 25 + 6 (R26~R31) · R2/R3/R15/R19/R20 끝점 갱신 · 시술 축 엣지에 catalog_item 추가 + 승격 규칙
# ---------------------------------------------------------------------------
RELATIONS = copy.deepcopy(V11.RELATIONS)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


PROMOTE_RULE = ("v2 승격 규칙: 참조가 분류 항목(catalog_item)에 닿으면 target_depth=catalog_item. 그 항목의 튜플이 확정(status=complete · what 확정 · 미등록 조각 0)이면 끝을 procedure 로 승격하고(target_depth=procedure) "
                "항목 id 는 엣지 속성 via_catalog_item 으로 보존. partial 이면 catalog_item 에 머문다. 규칙만 적고 값은 실버 빌드에서 만든다")
_rel("R2").update({"name": "has_catalog_item", "to": "catalog_item", "note": "taxonomy 트리. v2: 끝이 catalog_item(v1.1 procedure). 결정(reclassified_to)으로 재배치될 수 있음"})
_rel("R3").update({"from": "catalog_item", "note": "v2: 항목 이름 = 같은 계열 제품명(정규화 완전 일치)일 때만 자동. 그 항목의 튜플은 what=product. " + PROMOTE_RULE})
for rid in ("R9", "R12", "R15", "R16", "R17", "R18"):
    r = _rel(rid)
    r["note"] = (r["note"] + ". " if r["note"] else "") + PROMOTE_RULE
    attrs = list(r["attrs"])
    for i, a in enumerate(attrs):
        if a[0] == "target_depth":
            attrs[i] = ("target_depth", "enum(modality|subcategory|catalog_item|procedure|product)", "해결된 깊이. v2: catalog_item 추가, 튜플 확정 시 procedure 로 승격")
    if not any(a[0] == "via_catalog_item" for a in attrs):
        attrs.append(("via_catalog_item", "str|null", "승격 전 닿았던 분류 항목 id(CAT-)"))
    if rid in ("R16", "R17", "R18") and not any(a[0] == "target_depth" for a in attrs):
        attrs.append(("target_depth", "enum(modality|subcategory|catalog_item|procedure|product)", "v2: 시술 축 끝의 깊이"))
    r["attrs"] = attrs
_r15 = _rel("R15")
_r15["note"] = ("pih procedure_ref 는 가장 구체 수준 그대로 + target_depth (질문 5). extracted safety.serious null = 미입력. v2: 끝은 adverse_effect 튜플이며 문구 하나가 사건을 둘 이상 담으면 튜플마다 엣지 하나(같은 엣지 속성). "
                "타임라인 normal 문구는 reaction_level=normal 로 표시. 등급·빈도·시기·지속·대처·예방·위험 요인·예상/이상/주의/응급 표시는 전부 이 엣지 속성(튜플에 넣지 않는다). " + PROMOTE_RULE)
_r15["attrs"] = list(_r15["attrs"]) + [("expression_id", "str|null", "이 엣지를 만든 adverse_expression(원문) id. complications 레코드는 null(원문 = 사전 뼈대)")]
_rel("R19").update({"from": "evidence_statement|adverse_expression|clinical_rule", "note": "v2: 문헌 adverse_effects 인용은 adverse_expression(kind=evidence_statement)에서"})
_rel("R20").update({"to": "evidence_statement|adverse_expression(evidence_statement)", "note": "코드 키로 확정. v2: adverse_effects 섹션은 adverse_expression"})
RELATIONS += [
    {"id": "R26", "name": "derived_from", "from": "procedure", "to": "catalog_item", "card": "1:N",
     "attrs": [("decomposition", "obj(what_basis, site_fragment, technique_origin, qualifiers, unregistered_fragments)", "항목 이름을 어떻게 분해해 이 튜플이 됐는지(§1.4)")],
     "sources": ["taxonomy.json:modality[].subcategories[].items[].name"], "note": "분류 항목 하나 → 튜플 하나. 여러 항목이 같은 튜플이면 같은 procedure 에 N 엣지(접힘). §9.5 접힌 표"},
    {"id": "R27", "name": "procedure_what", "from": "procedure", "to": "modality|modality_subcategory|product", "card": "N:1", "attrs": [("what_kind", "enum(modality|modality_subcategory|product)", "")],
     "sources": [], "note": "튜플의 what 축. §1.4 what 규칙"},
    {"id": "R28", "name": "procedure_site", "from": "procedure", "to": "site", "card": "N:1 (없으면 none)", "attrs": [],
     "sources": [], "note": "튜플의 site 축. 부위 사전 21 공유. 사전에 없는 부위 조각은 미등록 기록 + none"},
    {"id": "R29", "name": "expresses", "from": "adverse_expression", "to": "adverse_effect", "card": "N:1 | null (문구 하나가 사건 둘 이상이면 N:M)",
     "attrs": [("matched_fragments", "obj(event, site, course)", "분해에서 닿은 조각"), ("basis", "enum(statement|patient_ko|both)", "문헌 표현: 어느 텍스트에서 닿았는지(§1.5 문헌 규칙)")],
     "sources": ["literature-evidence.json:categories.{code}.adverse_effects[].statement", "literature-evidence.json:categories.{code}.adverse_effects[].patient_ko", "consent-checklist.json:categories[].emergency_signs[]", "post-procedure-timeline.json:timelines[].phases[].normal[]", "post-procedure-timeline.json:timelines[].phases[].abnormal[]", "post-procedure-timeline.json:timelines[].phases[].caution[]", "post-procedure-timeline.json:timelines[].phases[].emergency[]", "extracted.json:{code}.safety.common[]", "extracted.json:{code}.safety.uncommon[]", "extracted.json:{code}.safety.serious[]", "extracted.json:{code}.safety.emergency[]"],
     "note": "튜플에 닿으면 연결, 아니면 null + 미등록 조각 기록. 사전 값·동의어 추가는 이번 범위 아님"},
    {"id": "R30", "name": "leads_to", "from": "adverse_effect", "to": "adverse_effect", "card": "N:M (방향 있음)", "attrs": [("basis", "str", "근거 문장(출처 잎 키)")],
     "sources": [], "note": "인과(혈관 폐색 → 피부 괴사). 원장은 인과를 구조화하지 않았다(incidence·mechanism 문장 안에만 있음) — 자동 생성 없음, 결정 개체(사람)로만 값이 생긴다"},
    {"id": "R31", "name": "adverse_site", "from": "adverse_effect", "to": "site", "card": "N:1 (상대 부위는 사전 relative_site · 없으면 none)", "attrs": [],
     "sources": ["complications.json:categories[].complications[].name"], "note": "튜플의 site 축. 공유 부위 사전 21 + relative_site(주사 부위·시술 부위) + none"},
]

ERD_ENUMS = copy.deepcopy(V11.ERD_ENUMS)
ERD_ENUMS["target_depth"] = ["modality", "subcategory", "catalog_item", "procedure", "product"]
ERD_ENUMS["package.kind"] = ERD_ENUMS["package.kind"] + ["combo_ref"]
ERD_ENUMS.pop("adverse_effect.kind", None)
ERD_ENUMS["adverse_expression.kind"] = ["evidence_statement", "symptom_phrase", "emergency_sign", "patient_text", "safety_phrase"]
ERD_ENUMS["adverse_expression.match_status"] = ["linked", "unlinked"]
ERD_ENUMS["procedure.what_kind"] = ["modality", "modality_subcategory", "product"]
ERD_ENUMS["procedure.technique_origin"] = ["fragment", "inherited", "none"]
ERD_ENUMS["procedure.origins"] = ["catalog_item", "reference", "market_pricing"]
ERD_ENUMS["tuple.status"] = ["complete", "partial"]
ERD_ENUMS["adverse_effect.site_ref_kind"] = ["site", "relative", "none"]
ERD_ENUMS["catalog_item.tuple_status"] = ["complete", "partial"]

# ---------------------------------------------------------------------------
# 3. 사건 사전(adverse_event_type) · 경과 사전(course) · 상대 부위(relative_site) — 값 하나하나 출처(파일·키)
#    뼈대 = complications.json categories[].complications[].name 65 를 분해한 조각. 표기 변형(한/영)은 동의어. kind=derived(원문의 부분 문자열).
#    category ∈ {국소 일시 반응, 염증/감염, 혈관, 신경, 색소, 구조/이물, 전신}
# ---------------------------------------------------------------------------
_CN = ("complications.json", "categories[].complications[].name")
_CD = ("complications.json", "categories[].complications[].duration")
_CI = ("complications.json", "categories[].complications[].incidence")
_TL = lambda k: ("post-procedure-timeline.json", f"timelines[].phases[].{k}[]")
_CS = ("consent-checklist.json", "categories[].emergency_signs[]")
_TI = ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.common[]")

# (canonical, category, [synonyms...]) — 전부 _CN 의 부분 문자열(정규화 후)
ADVERSE_EVENT_TYPES = [
    ("통증", "국소 일시 반응", ["압통", "Pain", "불편감", "Discomfort"]),
    ("멍", "국소 일시 반응", ["타박상", "반상출혈", "Bruising", "Ecchymosis"]),
    ("홍반", "국소 일시 반응", ["Erythema", "Redness", "발적", "빨개짐"]),
    ("부종", "국소 일시 반응", ["종창", "Swelling", "Edema", "붓기"]),
    ("혈종", "국소 일시 반응", ["Hematoma"]),
    ("열감", "국소 일시 반응", []),
    ("당김감", "국소 일시 반응", ["Tightness"]),
    ("자극감", "국소 일시 반응", ["Stinging"]),
    ("작열감", "국소 일시 반응", ["burning"]),
    ("건조", "국소 일시 반응", ["Dryness"]),
    ("낙설", "국소 일시 반응", ["각질 박리", "desquamation"]),
    ("소양감", "국소 일시 반응", ["Pruritus", "가려움"]),
    ("두통", "전신", []),
    ("독감 유사 증상", "전신", []),
    ("항체 내성", "전신", ["면역 저항"]),
    ("아나필락시스", "전신", ["즉시형 과민반응", "과민반응"]),
    ("실신", "전신", ["혈관미주신경성 반응", "vasovagal"]),
    ("전해질 과부하", "전신", []),
    ("감염", "염증/감염", ["Infection"]),
    ("바이오필름", "염증/감염", ["Biofilm"]),
    ("정맥염", "염증/감염", []),
    ("혈관 폐색", "혈관", ["혈관폐색", "Vascular Occlusion"]),
    ("색전", "혈관", ["Embolism", "공기색전"]),
    ("혈관외유출", "혈관", ["extravasation"]),
    ("감각 이상", "신경", ["감각이상", "저림", "감각둔화", "감각저하", "따끔거림", "Hypoesthesia", "Paresthesia"]),
    ("색소침착", "색소", ["PIH", "과색소침착", "염증후 색소침착", "Post-inflammatory Hyperpigmentation", "Hyperpigmentation"]),
    ("결절", "구조/이물", ["Nodule"]),
    ("육아종", "구조/이물", ["Granuloma"]),
    ("이물반응", "구조/이물", ["Foreign Body Reaction"]),
    ("경결", "구조/이물", ["딱딱함", "섬유화"]),
    ("구형구축", "구조/이물", ["Capsular Contracture"]),
    ("실 노출", "구조/이물", ["Thread Exposure"]),
    ("실 이동", "구조/이물", ["Thread Migration"]),
    ("딤플링", "구조/이물", ["피부 딤플링", "주름짐", "Dimpling", "Puckering"]),
    ("비대칭", "구조/이물", ["안면 비대칭", "Asymmetry"]),
    ("반흔", "구조/이물", ["Scarring"]),
    ("화상", "구조/이물", ["열손상", "Thermal Burn"]),
    ("수포", "구조/이물", []),
    ("괴사", "구조/이물", ["피부 괴사", "Skin Necrosis", "동상", "지방괴사", "Frostbite", "Fat Necrosis"]),
    ("PAH", "구조/이물", ["역설적 지방 증식", "Paradoxical Adipose Hyperplasia"]),
]
ADVERSE_EVENT_CATEGORIES = ["국소 일시 반응", "염증/감염", "혈관", "신경", "색소", "구조/이물", "전신"]
ADVERSE_EVENT_CATEGORY_REVIEW = ["화상", "수포", "경결", "비대칭", "두통"]  # 배정이 애매한 값 — 사용자 확인 대상(§12)

# 경과 사전 — (canonical, [(synonym, (file, path))...], canonical 출처)
COURSES = [
    ("일시", [("일시적", _CN), ("일과성", _CI), ("가역적", _CN), ("Transient", _CN)], _CN),
    ("지연", [("지연성", _CN), ("Delayed", _CN), ("Late-Onset", _CN), ("LOP", _CN)], _CN),
    ("영구", [("영구적", _CD), ("비가역적", _CD)], _CD),
    ("재발", [("재활성화", _TL("emergency"))], _TL("caution")),
    ("미상", [], None),  # 기본값 — 원장에 수식어가 없을 때. 출처 kind=default
]
# 상대 부위 사전 — (canonical, 출처, [(synonym, 출처)])
RELATIVE_SITES = [
    ("주사 부위", _CN, [("주사부위", _CN), ("주입 부위", _TI), ("주입부위", _TI)]),
    ("시술 부위", _CS, [("시술부위", ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.common[]"))]),
]

# ---------------------------------------------------------------------------
# 4. 분해 규칙 v2 (데이터) — erd-v2-tuples.py 가 그대로 실행
# ---------------------------------------------------------------------------
TUPLE_RULES = {
    "name": "tuples_v2",
    "procedure": {
        "input": {"catalog_items": "taxonomy.json modality[].subcategories[].items[].name 521 (family = 계열 코드, parent = 하위분류 id)",
                  "references": "v1.1 §9.2 의 자유 텍스트 자리 전부(erd-v1.1-resolve.py slot_items — pih id·고민·부위·canonical_category·step1 제외) + market-pricing items[].name 122(③)"},
        "fragments": "v1.1 §1.3 2단계 그대로: 괄호 안을 떼고(outer / inner 묶음), 묶음 안을 조합 기호 `+ / & ,` 로 멤버로 나누고, 멤버마다 사전 순서 product → modality_subcategory → catalog_item_name → site → spec → product_tier 로 완전 일치. 통째로 안 닿으면 공백 토큰을 왼쪽부터 가장 긴 구간으로. 남는 토큰 = 미등록 조각. 분류 항목 자신의 이름은 catalog_item_name 색인에서 제외(자기 참조 금지)",
        "combo": "같은 묶음(outer 또는 한 괄호) 안에서 조합 기호로 나뉜 멤버 중 primary(modality|modality_subcategory|product|catalog_item) 를 가진 멤버가 둘 이상 → package(kind=combo_ref). 멤버 각각을 튜플화. 괄호는 조합 기호가 아니다(괄호 안 멤버 하나는 수식 조각)",
        "what": ["product 조각(계열 안 우선, 없으면 전 계열) → what=product", "catalog_item 조각 → 그 항목의 튜플 what(분류 항목은 먼저 전부 튜플화)", "modality_subcategory 조각 → what=modality_subcategory", "modality 조각 또는 자리 힌트의 계열 → what=modality",
                 "분류 항목(①)의 what: 이름(또는 outer 조각)이 제품 색인에 닿으면 product, 아니면 부모 하위분류(가장 구체적인 계열 층). 하위분류 라벨 조각이 따로 닿으면 그 하위분류",
                 "primary 가 여럿이고 조합이 아니면 각 조각의 최종 what 종류로 product > modality_subcategory > modality 순(분류 항목 조각은 그 항목의 what 종류로 비교), 같은 종류면 텍스트 순서. 나머지는 extra_primaries 로 기록",
                 "조각이 계열 사전과 제품 색인 양쪽에 닿으면(보톡스·필러처럼 계열명이 제품명인 경우) what 은 product. 분류 항목(①)에서 타 계열·같은 계열의 계열 조각은 what 으로 쓰지 않는다(부모 하위분류가 더 구체적) — extra 로 기록",
                 "primary 도 힌트도 없으면 튜플 불가(what 미확정 · 집계 「튜플 불가」)"],
        "site": "site 사전(21) 에 닿은 조각. 둘 이상이면 텍스트 순서의 첫 조각(나머지 extra_sites). 없으면 none. 사전에 없는 부위 같은 조각(전체얼굴 등)은 미등록 조각으로만 기록(어느 축인지 판정하지 않는다 — 사전 추가는 범위 밖)",
        "technique": "조각이 기법 사전(12)에 닿으면 그 값(fragment). 아니면 R5 계열→기법(procedure-profiles mechanism[]) 이 하나인 계열은 상속(inherited), 둘 이상인 계열은 none(상속 불가 · 어느 기법인지 추측 금지)",
        "qualifiers": "spec(규격)·product_tier·extra 조각은 튜플에 넣지 않고 참조 레코드(R9/R12/R18 target_label 등) 쪽에 남긴다",
        "id": "PRC-sha256(what_id|site_id|technique_id)[:10]",
        "status": "complete = 미등록 조각 0 · partial = 미등록 조각 ≥1 (튜플은 둘 다 만든다, what 이 확정됐으므로)",
        "no_similarity": True,
    },
    "adverse": {
        "input": {"complications": "complications.json categories[].complications[].name 65 (사전 뼈대 + 튜플 ①)",
                  "phrases": "extracted/taxonomy safety.* 전 문구 · consent emergency_signs · literature adverse_effects statement(+patient_ko) 32 · post-procedure-timeline normal/abnormal/caution/emergency 전 문구"},
        "split": "정규화 전 원문을 괄호로 outer/inner 묶음으로 나누고, 묶음 안을 `· / , + 및 또는 — -- :` 로 멤버로 나눈다. 멤버마다 공백 토큰을 왼쪽부터 가장 긴 구간으로 사전 순서 relative_site → site → course → adverse_event_type 에 완전 일치(정규화 norm_v1). 남는 토큰 = 미등록 조각",
        "tuple": "멤버 안의 사건 조각 하나 = 튜플 하나(멤버에 사건이 둘이면 둘). site·course 는 멤버 → 같은 묶음 → outer 묶음 → (이름 전체에 그 축의 값이 하나뿐이면 그 값) 순으로 상속(멤버 자체 값이 우선). 없으면 site=none, course=미상",
        "normal_phrases": "타임라인 normal 문구는 사전 원천이 아니다. 같은 규칙으로 분해해 닿으면 R29 + R15(reaction_level=normal), 아니면 표현만",
        "literature": "문헌 레코드는 statement(영문)와 patient_ko(한글)를 각각 분해해 합집합 튜플에 닿는다(같은 레코드의 번역). patient_en/zh/ja 표현은 그 레코드의 튜플을 따라간다(basis 기록)",
        "id": "ADV-sha256(event_id|site_id|course_id)[:10]",
        "status": "complete = 문구에 미등록 조각 0 · partial = 미등록 조각 ≥1",
        "no_similarity": True,
    },
}
