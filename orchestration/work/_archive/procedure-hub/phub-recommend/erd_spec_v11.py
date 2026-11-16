# -*- coding: utf-8 -*-
"""ERD v1.1 명세 (데이터). erd_spec.py(v1) 를 읽어 세 묶음(A 재검토 처분 · B 분해 규칙 · C step1 브론즈 편입)만 덧씌운다.
erd_build_v11.py 가 읽는다. v1 명세는 손대지 않는다.
"""
import copy
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
import sys  # noqa
sys.path.insert(0, HERE)
import erd_spec as V1  # noqa

ERD_VERSION = "v1.1"
SNAPSHOT = V1.SNAPSHOT
LEDGER_DIR = V1.LEDGER_DIR
WORK_DIR = HERE
STEP1_FILE = "step1-products.json"          # 22번째 브론즈 원천 (조사 산출물) — 같은 폴더
STEP1_TIER2_SOURCE_RE = r"식약처.*API"      # licenses[].source 가 이 정규식에 맞을 때만 허가 필드 신뢰 2

NORMALIZE_RULE = copy.deepcopy(V1.NORMALIZE_RULE)
NORMALIZE_RULE["note"] = ("정규화 결과가 완전히 같을 때만 「같은 것」. 괄호·조합 기호가 섞인 참조는 v1.1 분해 규칙(§1.3)으로 조각을 내어 "
                          "조각 단위로 완전 일치만 본다. 유사도·추측 매칭은 하지 않는다.")
ID_RULE = copy.deepcopy(V1.ID_RULE)
ID_RULE["survey_products"] = "step1 제품(origin=survey)은 PRD-<sha256(계열코드|norm(display_name))[:10]>, 계열 코드가 없으면 'survey' 를 계열 자리에. step1 ledger_id 는 alias"

# ---------------------------------------------------------------------------
# 1. 원장 파일 21 + 조사 산출물 1 · 신뢰 순위
# ---------------------------------------------------------------------------
SOURCE_FILES = []
for f, t, basis, note in V1.SOURCE_FILES:
    if f == "complications.json":
        note = "발주서 §5 목록은 4 이나 원장에 source_method·consensus_method 키가 없다. 8-1 처분(사용자): 3 유지 + 「AI 컨센서스 추정」 표시"
    SOURCE_FILES.append((f, t, basis, note))
SOURCE_FILES.append((STEP1_FILE, 3, "items[].4_license.licenses[].source",
                     "조사 산출물(research artifact, 10-29 · 395 항목 · 식약처 허가 조사). 허가·회사·공식명 필드는 licenses[].source 가 "
                     f"`{STEP1_TIER2_SOURCE_RE}` 에 맞을 때만 2, 그 밖(판정·메모·search_names 등)은 3. 설계·식별자(ledger_id·1_identity 등)는 ERD 에 들이지 않고 출처 키로만 쓴다"))
SOURCE_KIND = {f: "ledger" for f, *_ in V1.SOURCE_FILES}
SOURCE_KIND[STEP1_FILE] = "research_artifact"
TRUST_FLAGS = {"complications.json": "AI 컨센서스 추정(8-1)", STEP1_FILE: "허가 필드만 조건부 2(C)"}

# ---------------------------------------------------------------------------
# 2. 개체 — v1 그대로 + product 속성 추가 · technique/site 정의 갱신
# ---------------------------------------------------------------------------
ENTITIES = copy.deepcopy(V1.ENTITIES)


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


# source_file: 종류 속성
_ent("source_file")["definition"] = "브론즈 스냅샷(2026-10-26)의 원장 JSON 21 + 조사 산출물 step1-products.json(10-29). 실버의 모든 값이 가리키는 출처의 뿌리."
_ent("source_file")["attrs"].insert(5, ("kind", "enum(ledger|research_artifact)", True, [], "원장 21 = ledger, step1 = research_artifact"))
_ent("source_file")["attrs"].insert(7, ("trust_flag", "str|null", False, [], "8-1 「AI 컨센서스 추정」 · step1 「허가 필드만 조건부 2」"))

# technique: 8-4 처분
_ent("technique")["definition"] = ("에너지원·작용 방식 단위. 8-4 처분(사용자): 원장에서 기법 키(technique·mechanism·method 류)로 명시된 값만 — "
                                   "procedure-profiles `mechanism[]` 하나뿐이다. taxonomy 하위분류 label 은 `modality_subcategory` 개체로만, "
                                   "products energy_device `type` 은 product_type 사전으로만, pih-risk `subcategory` 는 하위분류 라벨 일치(R15.subcategory_label)로만. "
                                   "extracted `related_techniques[]` 는 키 이름에 technique 가 있으나 값이 설명 문장이라 기법 값이 아니다(v1 §2.2 유지).")
_ent("technique")["attrs"] = [("name", "str", True, ["procedure-profiles.json:profiles[].mechanism[]"], "사전 technique 정준값(12)")]

# site: 8-2 처분
_ent("site")["definition"] = ("해부학적 부위. 8-2 처분(사용자): anatomy-danger-zones 11 zone(뼈대) + taxonomy problem 하위분류 라벨 중 실제 부위만(10). "
                              "「(확장)」 51개 정준값은 없앴고, 부위가 아닌 41개는 고민 하위분류 라벨 사전(problem_subcategory_label)으로 재배치(§8-2 표). "
                              "복합 라벨(이마/관자놀이 등)은 `/` 분해로 뼈대 멤버를 기록한다.")
_ent("site")["attrs"] = [a for a in _ent("site")["attrs"] if a[0] != "is_backbone"]
_ent("site")["attrs"].insert(2, ("site_kind", "enum(backbone|taxonomy_site_label)", True, [], "anatomy 11 = backbone, taxonomy 부위 라벨 10 = taxonomy_site_label"))
_ent("site")["attrs"].insert(3, ("members", "site[]|null", False, [], "복합 라벨을 `/` 로 분해해 모든 조각이 부위 사전에 닿을 때만 멤버(이마/관자놀이 → 이마, 관자놀이)"))
_ent("site")["aliases"] = "zone id(영문 슬러그) · 사전 동의어 · cc_group 원문(부위 라벨 10 에 한함)"

# modality_subcategory: 하위분류 라벨이 기법 사전에서 빠져 여기로만
_ent("modality_subcategory")["definition"] = ("taxonomy modality[].subcategories 74. 계열 아래, 단위 시술 위의 분류 층. 참조 깊이 「하위분류」의 대상. "
                                              "8-4 처분: 하위분류 label 64(distinct)는 기법이 아니라 이 개체의 label 로만 둔다. pih-risk subcategory 는 이 label 과 일치할 때만 연결.")

# complaint / problem_subcategory: cc_group 재배치
_ent("problem_subcategory")["definition"] = ("taxonomy problem[].subcategories 53. 8-2 처분: 라벨 53 은 사전 problem_subcategory_label 의 정준값이고, "
                                             "problem-packages cc_group 은 (problem_id, label) 로 이 개체에 결합한다(R7 그룹). 부위인 라벨 10 은 부위 사전에도 있다(R11).")
_ent("complaint")["attrs"].append(("cc_group_raw", "str", False, ["problem-packages.json:problems[].complaints[].cc_group"], "원문 보존. 하위분류 결합은 사전 problem_subcategory_label (problem_id, label) 일치"))

# product: C step1 편입
_p = _ent("product")
_p["definition"] = ("제조사 기준 제품(약제·기기·실). products.json 59 와 taxonomy modality[].products 59 를 합치되 어긋난 3건은 충돌 (질문 3). "
                    "v1.1: step1-products.json 395 항목을 제품 속성(허가·공식명·허가권자·제조원·허가 상태·KPIC·출처 질의)의 **출처 키**로 편입한다. "
                    "원장 59 와의 대응은 B 분해 규칙(이름 분해·동의어)으로만 하고, 원장에 없는 제품은 origin=survey 로 올린다. step1 의 ledger_id·1_identity 같은 설계·식별자는 들이지 않는다(브론즈).")
_p["identity"] = "계열 코드 + 정규화 제품명 (survey 제품은 계열 코드 없으면 'survey' + 정규화 display_name; 원장 대응이 되면 원장 제품 id 를 쓰고 step1 쪽은 alias)"
_p["attrs"] += [
    ("origin", "enum(ledger|survey)", True, [], "원장 59 = ledger, step1 에만 있는 제품 = survey(원장 밖 · 현장/웹 조사)"),
    ("survey_ledger_id", "str|null", False, [f"{STEP1_FILE}:items[].ledger_id"], "step1 ledger_id 는 alias 로만 보존 (설계 식별자 아님)"),
    ("survey_names", "obj[](name,lang,role)", False, [f"{STEP1_FILE}:items[].2_names.display_name", f"{STEP1_FILE}:items[].2_names.ledger_name", f"{STEP1_FILE}:items[].2_names.search_names[].name", f"{STEP1_FILE}:items[].2_names.search_names[].lang"], "aliases. 원장 대응은 이 이름들을 B 규칙으로 분해해 제품 사전 일치만"),
    ("survey_family_code", "str|null", False, [f"{STEP1_FILE}:items[].family.code"], "B 규칙 1단계 계열 힌트. `현장 기기`·`원천 항목 없음` = null(계열 없음 → 이름의 계열 동의어로)"),
    ("license_status", "dict:license_status", False, [f"{STEP1_FILE}:items[].4_license.status"], "정상·확인 불가·허가 대상 아님·허가 취소(이력)·미허가·허가번호 미확인 — 「확인 불가」는 null 이 아니라 그 값 그대로. 신뢰 3(판정)"),
    ("license_kind", "dict:license_kind", False, [f"{STEP1_FILE}:items[].4_license.kind"], "의약품/의료기기. null = 미입력"),
    ("licenses", "obj[](license_no, kind, state, item, official_name, official_name_en, holder, holder_biz, manufacturer, date, pack_unit, models, model, company, kpic.*, source, …)", False,
     [f"{STEP1_FILE}:items[].4_license.licenses[].license_no", f"{STEP1_FILE}:items[].4_license.licenses[].kind", f"{STEP1_FILE}:items[].4_license.licenses[].state", f"{STEP1_FILE}:items[].4_license.licenses[].item",
      f"{STEP1_FILE}:items[].4_license.licenses[].official_name", f"{STEP1_FILE}:items[].4_license.licenses[].official_name_en", f"{STEP1_FILE}:items[].4_license.licenses[].holder", f"{STEP1_FILE}:items[].4_license.licenses[].holder_biz",
      f"{STEP1_FILE}:items[].4_license.licenses[].manufacturer", f"{STEP1_FILE}:items[].4_license.licenses[].date", f"{STEP1_FILE}:items[].4_license.licenses[].pack_unit", f"{STEP1_FILE}:items[].4_license.licenses[].models[]",
      f"{STEP1_FILE}:items[].4_license.licenses[].model", f"{STEP1_FILE}:items[].4_license.licenses[].company", f"{STEP1_FILE}:items[].4_license.licenses[].key", f"{STEP1_FILE}:items[].4_license.licenses[].source",
      f"{STEP1_FILE}:items[].4_license.licenses[].kpic.drug_code", f"{STEP1_FILE}:items[].4_license.licenses[].kpic.drug_name", f"{STEP1_FILE}:items[].4_license.licenses[].kpic.ingredient", f"{STEP1_FILE}:items[].4_license.licenses[].kpic.atc"],
     f"허가 건(연결 허가). 잎 키 이름 그대로 보존. `source` 가 `{STEP1_TIER2_SOURCE_RE}` 에 맞는 건만 신뢰 2(식약처 공식), 아니면 3. kpic.drug_code = KPIC 코드"),
    ("license_history", "obj[](같은 모양)", False, [f"{STEP1_FILE}:items[].4_license.history[].license_no", f"{STEP1_FILE}:items[].4_license.history[].state", f"{STEP1_FILE}:items[].4_license.history[].official_name", f"{STEP1_FILE}:items[].4_license.history[].holder", f"{STEP1_FILE}:items[].4_license.history[].date"], "취소·취하 이력 허가 건. 신뢰 규칙은 licenses 와 같다"),
    ("spec", "obj[](license_no, pack_unit, content, models_with_volume, basis)", False, [f"{STEP1_FILE}:items[].5_spec.license[].license_no", f"{STEP1_FILE}:items[].5_spec.license[].pack_unit", f"{STEP1_FILE}:items[].5_spec.license[].content", f"{STEP1_FILE}:items[].5_spec.license[].models_with_volume[]", f"{STEP1_FILE}:items[].5_spec.license[].basis", f"{STEP1_FILE}:items[].5_spec.license_spec[].license_key", f"{STEP1_FILE}:items[].5_spec.license_spec[].pack_unit", f"{STEP1_FILE}:items[].5_spec.license_spec[].content"], "허가 기준 포장단위·함량. 시장가 복사본(5_spec.market*)은 market-pricing.json 파생이라 브론즈"),
    ("companies", "obj(manufacturer[], importer[], seller[], license_holder[], other[])(name, basis, original, role, period)", False,
     [f"{STEP1_FILE}:items[].6_companies.manufacturer[].name", f"{STEP1_FILE}:items[].6_companies.manufacturer[].basis", f"{STEP1_FILE}:items[].6_companies.importer[].name", f"{STEP1_FILE}:items[].6_companies.importer[].basis", f"{STEP1_FILE}:items[].6_companies.seller[].name", f"{STEP1_FILE}:items[].6_companies.seller[].basis", f"{STEP1_FILE}:items[].6_companies.license_holder[].name", f"{STEP1_FILE}:items[].6_companies.other[].name"],
     "회사 역할별 이름 + 근거 문장. `근거 없음`·`해당 없음` 은 값 그대로(판정값, 신뢰 3). 제조사 사전(manufacturer)과는 정규화 일치만"),
    ("survey_note", "str|null", False, [f"{STEP1_FILE}:items[].note"], "조사 메모. 신뢰 3"),
]
_p["aliases"] = "taxonomy products[].id (M1-P-0 형) · products.json 의 섹션 키(소속) · step1 ledger_id · step1 display_name/ledger_name/search_names"

# conflict: step1 회사 충돌 레코드도 출처
_c = _ent("conflict")
_c["attrs"][4] = ("values", "obj[](value, source_file, source_path, trust_tier)", True,
                  [f"{STEP1_FILE}:items[].6_companies.conflicts[].field", f"{STEP1_FILE}:items[].6_companies.conflicts[].license", f"{STEP1_FILE}:items[].6_companies.conflicts[].other", f"{STEP1_FILE}:items[].6_companies.conflicts[].source", f"{STEP1_FILE}:items[].6_companies.conflicts[].note"],
                  "step1 6_companies.conflicts(12) 는 허가 값 vs 다른 출처 값의 value_conflict 로 그대로 적재(「덮어쓰지 않음」 유지)")

# citation: step1 URL 근거
_ci = _ent("citation")
_ci["attrs"][9] = ("url", "str", False, ["complications.json:categories[].complications[].evidence", f"{STEP1_FILE}:items[].evidence[].urls[]", f"{STEP1_FILE}:items[].4_license.distribution_sources[].url"], "`;` 로 이어진 복수 URL 은 분리(③) — 원문은 브론즈. step1 evidence/유통 근거 URL 도 kind=url")
_ci["attrs"][10] = ("text", "str", False, ["extracted.json:{code}.source", "treatment-optimization.json:combination_rules[].evidence", "treatment-sequence.json:minimum_intervals[].source", "anatomy-danger-zones.json:zones[].tissue_data.rhinion_data_source", f"{STEP1_FILE}:items[].4_license.distribution_sources[].text"], "교과서 장·가이드라인 문자열. `일반 의학 지식`·`임상 가이드` 도 값 그대로")

# ---------------------------------------------------------------------------
# 3. 관계 — R5 · R10 · R11 · R15 갱신, R4 에 step1 계열 힌트
# ---------------------------------------------------------------------------
RELATIONS = copy.deepcopy(V1.RELATIONS)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


_rel("R4")["sources"].append(f"{STEP1_FILE}:items[].family.code")
_rel("R4")["note"] += ". step1 family.code 는 survey 제품의 계열 힌트(M 코드일 때만), `현장 기기`·`원천 항목 없음` 은 계열 없음"
_rel("R5")["from"] = "modality"
_rel("R5")["sources"] = ["procedure-profiles.json:profiles[].mechanism[]"]
_rel("R5")["note"] = "8-4 처분: 기법 사전 = mechanism[] 12 값만. 하위분류 label·energy_device type·pih subcategory 는 기법이 아니다"
_rel("R10")["note"] = "8-2 처분: cc_group 이 부위 사전(뼈대 11 + taxonomy 부위 라벨 10)에 있을 때만. 나머지 cc_group 은 R7 그룹(사전 problem_subcategory_label)"
_rel("R11")["note"] = "라벨이 부위 사전(taxonomy 부위 라벨 10)에 있을 때만"
_r15 = _rel("R15")
_r15["attrs"] = [a if a[0] != "technique_label" else ("subcategory_label", "str", "pih-risk subcategory 원문 — modality_subcategory.label 정규화 일치 시 하위분류 연결, 아니면 라벨만") for a in _r15["attrs"]]
_rel("R9")["note"] = "name 을 B 분해 규칙으로 해결: 사전 일치면 그 깊이, 분해 성공·항목 없음이면 조합 보존, 조각이 사전에 없으면 ⑨"
_rel("R12")["note"] = "M 코드 멤버는 계열 깊이로 확정. 자유 텍스트 멤버는 B 분해 규칙(§1.3) — 사전 일치 · 분해 성공·항목 없음 · ⑨"
_rel("R18")["note"] = "synergy 노드 `M코드-이름` 은 코드로 계열 확정(B 1단계), 이름은 분해 규칙. 자유 텍스트 쌍도 같은 규칙"
_rel("R17")["note"] = "자유 텍스트 → B 분해 규칙, 고민 라벨은 고민 사전 일치만"

ERD_ENUMS = copy.deepcopy(V1.ERD_ENUMS)
ERD_ENUMS["product.origin"] = ["ledger", "survey"]
ERD_ENUMS["site.site_kind"] = ["backbone", "taxonomy_site_label"]
ERD_ENUMS["source_file.kind"] = ["ledger", "research_artifact"]
ERD_ENUMS["reference.status"] = ["resolved", "decomposed", "unresolved"]
ERD_ENUMS["reference.decomposed_shape"] = ["single_primary_qualified", "combo", "qualifier_only"]

QUALITY_RULES = [list(r) for r in V1.QUALITY_RULES]
QUALITY_RULES[8] = ["⑨", "자동 탐지·표시", ("참조 해결은 결정론 분해 규칙(§1.3): ① 계열 확정(자리의 상위 코드, 없으면 이름의 계열 동의어) ② 이름 분해(괄호 밖/안 · 조합 기호 `+ / & ,` · 공백) 후 조각마다 "
                                         "제품 → 하위분류 → 단위 시술 → 부위 → 규격(정규식) → product_tier 순으로 완전 일치만 ③ 조립: 통째 일치면 그 깊이로 연결, "
                                         "조각이 전부 사전에 닿으면 「분해 성공·항목 없음」으로 조합 보존, 사전에 없는 조각이 하나라도 있으면 그때만 unresolved_reference(닿은 조각은 부분 결과로 기록). 유사도·추측 금지")]
QUALITY_RULES = [tuple(r) for r in QUALITY_RULES]

# ---------------------------------------------------------------------------
# 4. B. 참조 해결 — 결정론 분해 규칙 (데이터. erd-v1.1-resolve.py 가 그대로 실행)
# ---------------------------------------------------------------------------
RESOLVE_RULES = {
    "name": "decompose_v1_1",
    "normalize": NORMALIZE_RULE["name"],
    "step1_family": {
        "what": "참조가 놓인 자리의 상위 계열 코드를 힌트로 쓴다. 없으면 조각 중 계열 사전(modality) 동의어에 닿는 첫 조각의 계열",
        "slot_hints": {
            "market-pricing.items[].name": "categories[].id",
            "synergy.links[].from/to": "노드 접두 M코드 (`M9-울쎄라` → M9)",
            "problem-packages.procedures[].name": "procedures[].category",
            "procedure-comparison.procedures[].name": "procedures[].category",
            "post-procedure-timeline.timelines[].name": "timelines[].category 의 M코드 부분",
            "treatment-sequence.sequence_order[].categories[]": "`M코드-라벨` 의 M코드",
            "pih-risk": "procedure_ref 가 id 이므로 분해 대상 아님(id 깊이 판정)",
            "step1-products.items[]": "family.code (M코드일 때만)",
            "그 밖": "힌트 없음",
        },
        "code_regex": r"^(M\d+)(?:[-_ ](.+))?$",
    },
    "step2_decompose": {
        "paren_regex": r"\(([^()]*)\)",
        "paren_rule": "괄호 안 내용을 떼어 따로 조각으로(괄호 밖 = outer, 안 = inner). 중첩 없음 가정(원장에 중첩 괄호 없음)",
        "combo_symbols": ["+", "/", "&", ","],
        "secondary_split": " ",
        "secondary_rule": "조각이 통째로 어느 사전에도 안 닿으면 공백으로 토큰을 나누고, 왼쪽부터 가장 긴 연속 토큰 구간을 사전 순서로 시도한다(정확 일치만). 남는 토큰 = 사전에 없는 조각",
        "dictionary_order": ["product", "modality_subcategory", "procedure", "site", "spec", "product_tier"],
        "modality_lookup": "조각이 계열 사전(modality)에 닿으면 kind=modality (1단계 계열 확정용 · 조합 멤버로도 보존)",
        "spec_regex": r"^(\d+(?:\.\d+)?)\s*(cc|ml|mL|바이알|줄|회|샷|개|부위|cm2|cm²|차|단위|U)(?:\s*(기준|이상|패키지|당|동시))?$",
        "spec_dictionary": "unit 사전 정준값과의 완전 일치도 규격으로 본다",
        "scope_rule": "계열이 확정되면 제품·하위분류·단위 시술은 그 계열 안에서 먼저 찾고, 없으면 전 계열에서 찾는다(다른 계열의 조합 멤버). 전 계열에서 둘 이상 계열에 닿으면 모호 → 사전에 없는 조각으로 센다",
        "overlap_rule": "한 조각이 단위 시술과 제품 양쪽에 닿으면 단위 시술(8-11 처분), 하위분류와 제품 양쪽이면 하위분류",
    },
    "step3_assemble": {
        "tuple": ["family", "primaries(product|modality_subcategory|procedure|modality)", "sites", "specs", "tiers"],
        "resolved": "참조 전체가 하나의 사전 값과 통째로 일치(괄호·조합 없이) → 그 깊이(modality|subcategory|procedure|product)로 연결",
        "decomposed": "통째 일치는 아니지만 조각이 전부 사전에 닿음 → 「분해 성공·항목 없음」. 조합(튜플) 자체를 보존하고 가격·시너지는 그 조합에 단다. shape = single_primary_qualified(primary 1 + 부위/규격/등급) | combo(primary ≥2) | qualifier_only(primary 0)",
        "unresolved": "사전에 없는 조각이 하나라도 있음 → unresolved_reference. 닿은 조각은 partial 로 기록",
        "no_similarity": True,
    },
}

# ---------------------------------------------------------------------------
# 5. 질문 25 답 — v1.1 에서 바뀐 답만 덧씌움
# ---------------------------------------------------------------------------
Q25 = list(V1.Q25)
_q = dict(Q25)
_q[7] = "코드+라벨 합성값(M16-DCA·M15-도포·M15-팩)은 실존 하위분류 id 이면 그 하위분류로 연결. 나머지는 라벨을 B 분해 규칙으로 계열 안에서 해결(§9.2 v1.1 열)."
_q[8] = "synergy 노드는 코드로 계열 확정(B 1단계), 이름은 B 분해 규칙. 분해 성공·항목 없음은 조합 보존, 사전에 없는 조각만 미해결. from_category/to_category 는 엣지 속성으로 보존."
_q[10] = "problem-packages procedures[].name 29종은 B 분해 규칙으로 해결(통째 일치 → 깊이, 분해 성공 → 조합 보존, 사전 밖 조각 → 미해결)."
_q[11] = "자유 텍스트 시술명(treatment-optimization·treatment-sequence·procedure-comparison·market-pricing)은 B 분해 규칙(§1.3). 결과는 §9.2 v1 vs v1.1. problem-combos products 문장은 여전히 속성(문장 합성, 분해 대상 아님)."
_q[14] = "modality_ref 빈 26 항목은 두 묶음 — ① 기존 계열 매핑 후보(서브시전·에어서브시전·윤곽주사·지방분해주사·HPL·BNLS·브이올렛·컷슬린·두피메조) ② 계열 없음 격리(반영구 4·경구약 4(약물치료·미녹시딜·피나스테리드·두타스테리드 — 8-5 처분)·FUE·FUT·미라드라이·실리콘시트·스테로이드주사·경화요법·엔더몰로지), 격리 묶음은 「피부과 허브 범위 밖」 범위 검토 표시. 미배정 0."
_q[24] = "부위 사전 v1.1 = anatomy 11 zone 뼈대 + taxonomy 부위 라벨 10(코·이마/관자놀이·턱/턱선·입술·눈가·볼/광대·얼굴·사각턱·이중턱/턱밑·승모근·광대·볼/관자놀이 중 뼈대와 겹치지 않는 10). cc_group 52 중 부위 라벨만 부위 동의어, 나머지 41 은 사전 problem_subcategory_label(고민 하위분류 라벨)로 — 8-2 처분."
_q[16] = "기기 mfds null / 키 없음 = null(미입력). v1.1: step1 허가 상태(license_status)는 별도 속성이며 「확인 불가」도 값 그대로. mfds 와 license_status 는 합치지 않는다."
Q25 = [(n, _q[n]) for n, _ in Q25]

# ---------------------------------------------------------------------------
# 6. A. 재검토 19 처분 — 사용자 판단 4 + 워커 처리 확정 15
# ---------------------------------------------------------------------------
# (no, 처분 주체, 처분 내용, v1.1 반영 위치)
DISPOSITIONS = {
    1: ("사용자", "3 유지 + 「AI 컨센서스 추정」 표시(trust_flag)", "§5.1 · source_file.trust_flag"),
    2: ("사용자", "부위 사전에서 「(확장)」 51 제거. 부위 = anatomy 11 + taxonomy 부위 라벨 10. 뺀 41 은 고민 하위분류 라벨 사전(problem_subcategory_label)으로 재배치(§8-2 표)", "§4 site · problem_subcategory_label · R10/R11 · §9.1"),
    3: ("워커 처리 확정", "secondary → extended 동의 키 정규화 유지", "§2 procedure.indications_extended"),
    4: ("사용자", "하위분류 label 64 를 기법 사전에서 제거, modality_subcategory 개체로만. 기법 사전 = mechanism[] 12 값만(energy_device type → product_type 사전, pih subcategory → 하위분류 라벨 일치)", "§4 technique · R5 · R15.subcategory_label"),
    5: ("사용자", "경구약 4(약물치료·미녹시딜·피나스테리드·두타스테리드) = ② 「피부과 허브 범위 밖」 격리 묶음, 범위 검토 표시. 미배정 0", "§9.2 질문 14 표 · q14_bundles"),
    6: ("워커 처리 확정", "product_tier 7 표면형 전부 정준값, 병합 안 함", "§4 product_tier"),
    7: ("워커 처리 확정", "pih_risk_level 합집합 6값, `none` 정의 null", "§4 pih_risk_level"),
    8: ("워커 처리 확정", "literature adverse_effects 32 는 부작용 개체 kind=literature_claim, 이름형과의 연결은 ⑦/사람", "§2 adverse_effect"),
    9: ("워커 처리 확정", "timeline name 은 R15.source_label, 더 좁은 이름은 참조 해결(v1.1 은 B 규칙)", "R15 · §9.2"),
    10: ("워커 처리 확정", "concern·comparison id 는 고민 사전 일치만, 나머지 후보", "§4 problem · R13"),
    11: ("워커 처리 확정", "항목+제품 겹침은 procedure 우선(B overlap_rule 로 데이터화)", "§1.3 overlap_rule · R18"),
    12: ("워커 처리 확정", "age_group 5값 전부 정준값, 병합 안 함", "§4 age_group"),
    13: ("워커 처리 확정", "botox_specific → M1, filler_specific → M2", "R22"),
    14: ("워커 처리 확정", "M1_to_M7 → M1..M7 전개", "③ · modality.pih_note"),
    15: ("워커 처리 확정", "market-pricing 122·problem-combos products 24 는 속성 보존. v1.1: market-pricing 이름은 B 규칙으로 다시 센다(§9.2), products 문장은 분해 대상 아님", "modality.price_items · §9.2"),
    16: ("워커 처리 확정", "정제 규칙은 실버 빌더 명세, 원문 브론즈", "질문 19"),
    17: ("워커 처리 확정", "universal_checks 는 person_condition.universal=true, 엣지 없음", "R16"),
    18: ("워커 처리 확정", "주호소 중복은 6 으로 충돌 예상, 결합 키 (problem_id, 이름)", "§9.3 · complaint"),
    19: ("워커 처리 확정", "comparison 비교값은 R12 엣지 속성", "R12"),
}

# 8-2 부위/비부위 판정 — taxonomy 부위 라벨(실제 부위)만 부위 사전에 남긴다 (사용자 판단의 예시: 코·이마/관자놀이·턱/턱선)
SITE_LABELS_KEEP = ["코", "입술", "이마/관자놀이", "턱/턱선", "눈가", "볼/광대", "얼굴", "사각턱", "이중턱/턱밑", "승모근", "광대", "볼/관자놀이"]
# 8-5 경구약 4 — ② 격리 묶음
Q14_ORAL_DRUGS = ["약물치료", "미녹시딜", "피나스테리드", "두타스테리드"]
