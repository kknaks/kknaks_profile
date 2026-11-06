# -*- coding: utf-8 -*-
"""잎 키 573 → 행선지 규칙. 각 항목: (path 또는 regex, dest, target, note)
dest ∈ 개체 / 사전 / 엣지 / 브론즈 / 버림
"""
import re

META = [
    ("version", "개체", "source_file.version", "파일 메타 (질문 25)"),
    ("updated", "개체", "source_file.updated", "파일 메타 (질문 25)"),
    ("description", "개체", "source_file.description", "파일 메타"),
    ("consensus_method", "개체", "source_file.method", "신뢰 순위 4 근거"),
]

COLMAP = {}

COLMAP["anatomy-danger-zones.json"] = META + [
    ("critical_safety_facts.minimum_filler_for_blindness", "개체", "clinical_rule.text", "kind=critical_safety_fact, topic=키 이름"),
    ("critical_safety_facts.blindness_highest_risk_zones", "개체", "clinical_rule.text", "kind=critical_safety_fact"),
    ("critical_safety_facts.mechanism", "개체", "clinical_rule.text", "kind=critical_safety_fact"),
    ("critical_safety_facts.caveat", "개체", "clinical_rule.text", "kind=critical_safety_fact"),
    ("zones[].id", "개체", "site.aliases", "뼈대 zone id = site canonical_key"),
    ("zones[].name_ko", "개체", "site.name_ko", "사전 site 정준 한글명"),
    ("zones[].name_en", "개체", "site.name_en", "사전 site 동의어(en)"),
    ("zones[].danger_level", "개체", "site.danger_level", "사전 danger_level 검증"),
    ("zones[].danger_color", "사전", "dict:danger_level", "level 의 색 라벨 (zone 마다 level 과 1:1)"),
    ("zones[].vessels[].name", "개체", "anatomical_structure.name_raw", "kind=vessel. `한글 (영문)` 분해 ③"),
    ("zones[].vessels[].depth_mm", "엣지", "R21.depth_mm", ""),
    ("zones[].vessels[].diameter_mm", "엣지", "R21.diameter_mm", ""),
    ("zones[].vessels[].course", "엣지", "R21.course", ""),
    ("zones[].vessels[].danger", "엣지", "R21.danger", ""),
    ("zones[].vessels[].note", "엣지", "R21.note", ""),
    ("zones[].vessels[].depth_range_mm[]", "엣지", "R21.depth_range_mm", "단일값/범위 두 형태 원문 보존"),
    ("zones[].nerves[].name", "개체", "anatomical_structure.name_raw", "kind=nerve"),
    ("zones[].nerves[].type", "개체", "anatomical_structure.nerve_type", "사전 nerve_type"),
    ("zones[].nerves[].significance", "엣지", "R21.significance", ""),
    ("zones[].safe_injection_depth", "개체", "site.safe_injection_depth", ""),
    (re.compile(r"^zones\[\]\.tissue_data\.rhinion_data_source$"), "개체", "citation.text", "kind=guideline_text. site.tissue_data 에도 원문 키 보존"),
    (re.compile(r"^zones\[\]\.tissue_data\..+"), "개체", "site.tissue_data.*", "부위별 자유 구조 — 키 이름 보존"),
    ("zones[].clinical_pearls[]", "개체", "site.clinical_pearls", ""),
    ("zones[].botox_specific.target_muscle", "엣지", "R22.target_muscle", "site→M1"),
    ("zones[].botox_specific.risk", "엣지", "R22.risk_text", "site→M1"),
    ("zones[].botox_specific.safe_zone", "엣지", "R22.safe_zone", "site→M1"),
    ("zones[].botox_specific.diffusion_range_cm", "엣지", "R22.diffusion_range_cm", "site→M1"),
    ("zones[].botox_specific.key_warning", "엣지", "R22.key_warning", "site→M1"),
    ("zones[].botox_specific.dose_range", "엣지", "R22.dose_range", "site→M1"),
    ("zones[].filler_specific.risk_level", "엣지", "R22.risk_level", "site→M2. 사전 danger_level"),
    ("zones[].filler_specific.primary_risk", "엣지", "R22.primary_risk", "site→M2"),
    ("zones[].filler_specific.safe_technique", "엣지", "R22.safe_technique", "site→M2"),
    ("zones[].filler_specific.max_per_point_ml", "엣지", "R22.max_per_point_ml", "site→M2"),
    ("zones[].filler_specific.preferred_product", "엣지", "R22.preferred_product", "site→M2"),
    ("zones[].filler_specific.emergency_protocol", "엣지", "R22.emergency_protocol", "site→M2"),
]

COLMAP["combo-recipes.json"] = META + [
    ("recipes[].id", "개체", "package.aliases", "kind=recipe (질문 6)"),
    ("recipes[].name", "개체", "package.name", ""),
    ("recipes[].subtitle", "개체", "package.subtitle", ""),
    ("recipes[].goal", "사전", "dict:purpose_label", "package.purpose"),
    ("recipes[].intensity", "사전", "dict:package_tier", "package.tier"),
    ("recipes[].procedures[]", "엣지", "R12.member(modality)", "M 코드 → 계열 깊이"),
    ("recipes[].expectedResults", "개체", "package.expected_result", ""),
    ("recipes[].patientExplanation", "개체", "package.patient_explanation", ""),
    ("recipes[].analogy", "개체", "package.analogy", ""),
    ("recipes[].repeatCycle", "개체", "package.repeat_cycle", ""),
    ("recipes[].followUp[].week", "개체", "package.follow_up.week", ""),
    ("recipes[].followUp[].action", "개체", "package.follow_up.action", ""),
]

COLMAP["complications.json"] = [
    ("severity_levels.mild", "사전", "dict:severity", "정의문"),
    ("severity_levels.moderate", "사전", "dict:severity", "정의문"),
    ("severity_levels.severe", "사전", "dict:severity", "정의문"),
    ("severity_levels.critical", "사전", "dict:severity", "정의문"),
    ("categories[].id", "엣지", "R15.from(modality)", "계열 끝"),
    ("categories[].name", "사전", "dict:modality", "코드 연결 동의어"),
    ("categories[].complications[].name", "개체", "adverse_effect.name", "kind=named"),
    ("categories[].complications[].severity", "엣지", "R15.severity", "사전 severity"),
    ("categories[].complications[].incidence", "엣지", "R15.incidence", ""),
    ("categories[].complications[].onset", "엣지", "R15.onset", ""),
    ("categories[].complications[].mechanism", "엣지", "R15.mechanism", ""),
    ("categories[].complications[].risk_factors", "엣지", "R15.risk_factors", "빈 배열 46 = null ⑤"),
    ("categories[].complications[].management", "엣지", "R15.management", ""),
    ("categories[].complications[].prevention", "엣지", "R15.prevention", ""),
    ("categories[].complications[].evidence", "개체", "citation.url", "kind=url, `;` 분리 ③ → R15.evidence_ref"),
    ("categories[].complications[].duration", "엣지", "R15.duration", ""),
    ("categories[].complications[].risk_factors[]", "엣지", "R15.risk_factors", ""),
]

COLMAP["consent-checklist.json"] = META + [
    ("categories[].id", "엣지", "R16.from(modality)", "계열 끝 (R15 emergency_signs 도)"),
    ("categories[].name", "사전", "dict:modality", "코드 연결 동의어"),
    ("categories[].mandatory_disclosures[]", "개체", "modality.mandatory_disclosures", "고지문 = 속성"),
    ("categories[].contraindications[]", "개체", "person_condition.name", "kind=condition, R16.level=consent"),
    ("categories[].emergency_signs[]", "개체", "adverse_effect.name", "kind=emergency_sign, R15.frequency_class=emergency"),
]

COLMAP["contraindications.json"] = META + [
    ("rules[].from", "엣지", "R18.from(modality)", "kind=pair_rule"),
    ("rules[].from_name", "사전", "dict:modality", "코드 연결 동의어"),
    ("rules[].to", "엣지", "R18.to(modality)", ""),
    ("rules[].to_name", "사전", "dict:modality", "코드 연결 동의어"),
    ("rules[].level", "엣지", "R18.level", "사전 interaction_level"),
    ("rules[].interval", "엣지", "R18.interval_text", ""),
    ("rules[].note", "엣지", "R18.note", ""),
]

COLMAP["extracted.json"] = [
    ("{code}.name", "사전", "dict:modality", "코드 키 연결 동의어"),
    ("{code}.name_en", "사전", "dict:modality", "코드 키 연결 동의어(en)"),
    ("{code}.procedure_id", "개체", "modality.aliases", "M1-BOTOX 형"),
    ("{code}.source", "개체", "citation.text", "kind=textbook → R19 (modality.extracted_meta 출처)"),
    ("{code}.source_type", "개체", "modality.extracted_meta.source_type", "사전 source_type"),
    ("{code}.extracted_at", "개체", "modality.extracted_meta.extracted_at", ""),
    ("{code}.guardrail_version", "개체", "modality.extracted_meta.guardrail_version", ""),
    ("{code}.updated", "개체", "modality.extracted_meta.updated", "M3 만"),
    ("{code}.overview", "개체", "modality.overview", "출처=extracted.json, taxonomy 와 충돌 검사 (질문 2)"),
    ("{code}.mechanism", "개체", "modality.mechanism", "질문 2"),
    ("{code}.indications.primary[]", "개체", "modality.indications_primary", ""),
    ("{code}.indications.extended[]", "개체", "modality.indications_extended", ""),
    ("{code}.onset_duration.onset", "개체", "modality.onset", ""),
    ("{code}.onset_duration.peak", "개체", "modality.peak", ""),
    ("{code}.onset_duration.duration", "개체", "modality.duration", ""),
    ("{code}.aftercare[]", "개체", "modality.aftercare", ""),
    ("{code}.related_techniques[]", "개체", "modality.related_techniques", ""),
    ("{code}.contraindications.absolute[]", "개체", "person_condition.name", "R16.level=absolute"),
    ("{code}.contraindications.relative[]", "개체", "person_condition.name", "R16.level=relative"),
    ("{code}.safety.common[]", "개체", "adverse_effect.name", "R15.frequency_class=common"),
    ("{code}.safety.uncommon[]", "개체", "adverse_effect.name", "R15.frequency_class=uncommon"),
    ("{code}.safety.serious[]", "개체", "adverse_effect.name", "R15.frequency_class=serious"),
    ("{code}.safety.serious", "엣지", "R15(serious)", "null 2 = 미입력 ⑤ (질문 17)"),
    ("{code}.safety.emergency[]", "개체", "adverse_effect.name", "R15.frequency_class=emergency"),
]

_LIT_CIT = [
    ("authors", "citation.authors"), ("title", "citation.title"), ("journal", "citation.journal"), ("year", "citation.year"),
    ("pmid", "citation.pmid"), ("doi", "citation.doi"), ("pmc", "citation.pmc"), ("oa_url", "citation.oa_url"),
]
_lit = [
    ("version", "개체", "source_file.version", ""),
    ("updated", "개체", "source_file.updated", ""),
    ("source_method", "개체", "source_file.method", "신뢰 순위 1 근거"),
    ("accuracy_summary.rubric", "사전", "dict:accuracy_rubric", "accuracy_score 값 구간 정의"),
    ("categories.{code}.name", "사전", "dict:modality", "코드 키 연결 동의어(en 학술명)"),
    ("categories.{code}.moa", "개체", "modality.evidence_statement_count", "빈 배열 6 = null ⑤ (질문 13)"),
    ("categories.{code}.adverse_effects", "개체", "modality.evidence_statement_count", "빈 배열 6 = null"),
    ("categories.{code}.effects", "개체", "modality.evidence_statement_count", "빈 배열 8 = null"),
]
for k in ["scored_by", "overall_average", "n_scored", "by_field_average.moa", "by_field_average.adverse_effects", "by_field_average.effects",
          "by_category_average.{code}", "patient_ko_coverage", "patient_translations_coverage.ko", "patient_translations_coverage.en",
          "patient_translations_coverage.zh", "patient_translations_coverage.ja"]:
    _lit.append((f"accuracy_summary.{k}", "브론즈", "bronze", "파일 수준 집계값 — 실버는 문장 단위에서 재계산"))
for sec, ent, kindnote in [("moa", "evidence_statement", "kind=moa"), ("effects", "evidence_statement", "kind=effect"), ("adverse_effects", "adverse_effect", "kind=literature_claim")]:
    p = f"categories.{{code}}.{sec}[]"
    _lit.append((f"{p}.statement", "개체", f"{ent}.{'statement' if ent=='evidence_statement' else 'name'}", kindnote))
    for ck, tgt in _LIT_CIT:
        _lit.append((f"{p}.citations[].{ck}", "개체", tgt, "kind=pubmed, pmid 동일성 → R19"))
    for lang in ["ko", "en", "zh", "ja"]:
        _lit.append((f"{p}.patient_{lang}", "개체", f"{ent}.patient_text.{lang}", "질문 19 정제"))
    _lit.append((f"{p}.accuracy_score", "개체", f"{ent}.accuracy_score", ""))
    _lit.append((f"{p}.accuracy_note", "개체", f"{ent}.accuracy_note", ""))
    _lit.append((f"{p}.added_at", "개체", f"{ent}.added_at", ""))
COLMAP["literature-evidence.json"] = _lit

COLMAP["market-pricing.json"] = [
    ("version", "개체", "source_file.version", ""),
    ("updated", "개체", "source_file.updated", ""),
    ("currency", "사전", "dict:unit", "통화 단위 (source_file.currency 에도)"),
    ("note", "개체", "source_file.note", ""),
    ("categories[].id", "개체", "modality.price_items(소속)", "계열 끝"),
    ("categories[].name", "사전", "dict:modality", "코드 연결 동의어"),
    ("categories[].items[].name", "개체", "modality.price_items.label", "시술/제품 연결은 사전 일치만 (질문 11)"),
    ("categories[].items[].unit", "사전", "dict:unit", "modality.price_items.unit"),
    ("categories[].items[].low", "개체", "modality.price_items.low", "KRW"),
    ("categories[].items[].mid", "개체", "modality.price_items.mid", ""),
    ("categories[].items[].high", "개체", "modality.price_items.high", ""),
]

COLMAP["patient-education.json"] = [
    ("version", "개체", "source_file.version", ""),
    ("updated", "개체", "source_file.updated", ""),
    ("categories[].id", "개체", "modality(소속)", "계열 끝"),
    ("categories[].name", "사전", "dict:modality", "코드 연결 동의어"),
    ("categories[].patient_name", "사전", "dict:modality", "환자용 별칭 동의어 (modality.patient_name 에도)"),
    ("categories[].simple_explanation", "개체", "modality.patient_simple_explanation", ""),
    ("categories[].how_it_works", "개체", "modality.patient_how_it_works", ""),
    ("categories[].duration_simple", "개체", "modality.patient_duration_simple", ""),
    ("categories[].pain_level", "개체", "modality.patient_pain_level", ""),
    ("categories[].downtime", "개체", "modality.patient_downtime", ""),
    ("categories[].common_concerns[].q", "개체", "modality.faq.q", "FAQ = 속성"),
    ("categories[].common_concerns[].a", "개체", "modality.faq.a", ""),
]

COLMAP["pih-risk.json"] = META + [
    ("risk_levels.very_low", "사전", "dict:pih_risk_level", "정의(% 범위)"),
    ("risk_levels.low", "사전", "dict:pih_risk_level", ""),
    ("risk_levels.moderate", "사전", "dict:pih_risk_level", ""),
    ("risk_levels.high", "사전", "dict:pih_risk_level", ""),
    ("risk_levels.very_high", "사전", "dict:pih_risk_level", ""),
    ("notes.{code}", "개체", "modality.pih_note", "M1_to_M7 범위 키 전개 ③"),
    ("procedures[].category", "엣지", "R15.from.modality_code", "계열 코드 (procedure_ref 와 함께)"),
    ("procedures[].subcategory", "엣지", "R15.technique_label", "사전 technique"),
    ("procedures[].name", "엣지", "R15.source_label", "원문 라벨"),
    ("procedures[].procedure_ref", "엣지", "R15.from(proc_axis)+target_depth", "가장 구체 수준 그대로 (질문 5). to=adverse_effect `PIH`"),
    ("procedures[].pih_risk", "엣지", "R15.pih_risk", "사전 pih_risk_level"),
    ("procedures[].pih_rate", "엣지", "R15.pih_rate", ""),
    ("procedures[].fitzpatrick_note", "엣지", "R15.fitzpatrick_note", ""),
    ("procedures[].risk_factors[]", "엣지", "R15.risk_factors", ""),
    ("procedures[].prevention", "엣지", "R15.prevention", ""),
]

COLMAP["post-procedure-timeline.json"] = META + [
    ("reaction_levels.normal", "사전", "dict:reaction_level", "정의"),
    ("reaction_levels.abnormal", "사전", "dict:reaction_level", ""),
    ("reaction_levels.caution", "사전", "dict:reaction_level", ""),
    ("reaction_levels.emergency", "사전", "dict:reaction_level", ""),
    ("timelines[].id", "개체", "modality.aliases", "timeline name 이 계열명과 정규화 일치할 때만 alias, 아니면 R15.source_label 보조"),
    ("timelines[].category", "엣지", "R15.from(proc_axis)+target_depth", "M 코드 → 계열, M16-DCA → 하위분류 (질문 7)"),
    ("timelines[].name", "엣지", "R15.source_label", "시술명 원문. 더 구체 대상은 사전 일치만"),
    ("timelines[].phases[].period", "엣지", "R15.period", "사전 period"),
    ("timelines[].phases[].label", "엣지", "R15.phase_label", "사전 phase_label"),
    ("timelines[].phases[].normal[]", "개체", "adverse_effect.name", "kind=symptom, R15.reaction_level=normal"),
    ("timelines[].phases[].abnormal[]", "개체", "adverse_effect.name", "kind=symptom, reaction_level=abnormal"),
    ("timelines[].phases[].caution[]", "개체", "adverse_effect.name", "kind=symptom, reaction_level=caution"),
    ("timelines[].phases[].emergency[]", "개체", "adverse_effect.name", "kind=symptom, reaction_level=emergency"),
]

COLMAP["pre-procedure-checklist.json"] = META + [
    ("universal_checks[].id", "개체", "person_condition.aliases", "kind=check, universal=true"),
    ("universal_checks[].label", "개체", "person_condition.name", "kind=check, universal=true"),
    ("universal_checks[].type", "개체", "person_condition.universal_level", "사전 condition_level"),
    ("universal_checks[].description", "개체", "person_condition.description", ""),
    ("category_specific[].id", "엣지", "R16.from(modality)", ""),
    ("category_specific[].name", "사전", "dict:modality", "코드 연결 동의어"),
    ("category_specific[].checks[].label", "개체", "person_condition.name", "kind=check → R16"),
    ("category_specific[].checks[].type", "엣지", "R16.level", "사전 condition_level"),
]

COLMAP["problem-combos.json"] = META + [
    ("combos[].problem_id", "엣지", "R13.to(problem)", "확정"),
    ("combos[].problem", "사전", "dict:problem", "코드 연결 동의어(처짐/탄력·피부결/톤/항노화)"),
    ("combos[].packages[].id", "개체", "package.aliases", "kind=consult_package (질문 6)"),
    ("combos[].packages[].tier", "사전", "dict:package_tier", "package.tier"),
    ("combos[].packages[].tierLabel", "사전", "dict:package_tier", "tier 와 쌍 → 동의어"),
    ("combos[].packages[].name", "개체", "package.name", ""),
    ("combos[].packages[].procedures[]", "엣지", "R12.member(modality)", "M 코드"),
    ("combos[].packages[].productTier", "사전", "dict:product_tier", "package.product_tier"),
    ("combos[].packages[].products[]", "개체", "package.products_text", "조합 문장 — 제품 사전 일치 자동 아님"),
    ("combos[].packages[].priceRange", "개체", "package.price_range", "질문 22"),
    ("combos[].packages[].expectedResult", "개체", "package.expected_result", ""),
    ("combos[].packages[].salesPitch", "개체", "package.sales_pitch", ""),
    ("combos[].packages[].upsellHook", "개체", "package.upsell_hook", ""),
    ("combos[].packages[].clinicalRationale", "개체", "package.clinical_rationale", ""),
    ("combos[].packages[].riskBenefit", "개체", "package.risk_benefit", ""),
]

COLMAP["problem-packages.json"] = META + [
    ("problems[].problem_id", "개체", "problem(소속)", "확정"),
    ("problems[].problem", "사전", "dict:problem", "코드 연결 동의어(= taxonomy 와 동일)"),
    ("problems[].complaints[].cc", "개체", "complaint.name", "(problem_id, 이름) 유일 일치 결합 (질문 9)"),
    ("problems[].complaints[].cc_detail", "개체", "complaint.detail", ""),
    ("problems[].complaints[].cc_group", "사전", "dict:site", "R10 (질문 24)"),
    ("problems[].complaints[].procedures[].name", "엣지", "R9.target_label", "「시술 종류」층 (질문 10)"),
    ("problems[].complaints[].procedures[].category", "엣지", "R9.modality_code", ""),
    ("problems[].complaints[].procedures[].role", "엣지", "R9.role", ""),
    ("problems[].complaints[].procedures[].products[]", "엣지", "R9.products", "제품 사전 일치 → product id, 미일치 4종 ⑨"),
    ("problems[].complaints[].procedures[].products", "엣지", "R9.products", "빈 배열 47 = null ⑤"),
    ("problems[].complaints[].combos[].name", "개체", "package.name", "kind=cc_combo"),
    ("problems[].complaints[].combos[].combo[]", "엣지", "R12.target_label", "사전 일치만"),
    ("problems[].complaints[].combos[].reason", "엣지", "R14.reason", ""),
    ("problems[].complaints[].combos[].evidence", "엣지", "R14.evidence", ""),
    ("problems[].complaints[].combos", "개체", "complaint.combos_present", "빈 배열 1 = null"),
    ("problems[].complaints[].alternatives[]", "개체", "complaint.alternatives", ""),
]

COLMAP["procedure-comparison.json"] = [
    ("version", "개체", "source_file.version", ""),
    ("updated", "개체", "source_file.updated", ""),
    ("comparisons[].id", "개체", "package.aliases", "kind=comparison. R13 고민 사전 일치만"),
    ("comparisons[].title", "개체", "package.name", ""),
    ("comparisons[].subtitle", "개체", "package.subtitle", ""),
    ("comparisons[].evidence_notes[]", "개체", "package.evidence_notes", ""),
    ("comparisons[].procedures[].name", "엣지", "R12.target_label", "사전 일치만 (질문 11)"),
    ("comparisons[].procedures[].category", "엣지", "R12.modality_code", ""),
    ("comparisons[].procedures[].mechanism_simple", "엣지", "R12.mechanism_simple", ""),
    ("comparisons[].procedures[].pain", "엣지", "R12.pain", "사전 pain_scale"),
    ("comparisons[].procedures[].downtime", "엣지", "R12.downtime", ""),
    ("comparisons[].procedures[].onset", "엣지", "R12.onset", ""),
    ("comparisons[].procedures[].duration", "엣지", "R12.duration", ""),
    ("comparisons[].procedures[].cost_range", "엣지", "R12.cost_range", ""),
    ("comparisons[].procedures[].best_for", "엣지", "R12.best_for", ""),
    ("comparisons[].procedures[].limitations", "엣지", "R12.limitations", ""),
    ("comparisons[].procedures[].pih_risk", "엣지", "R12.pih_risk", "사전 pih_risk_level (`none` 포함)"),
    ("comparisons[].procedures[].asian_skin_note", "엣지", "R12.asian_skin_note", ""),
]

COLMAP["procedure-profiles.json"] = META + [
    ("profiles[].id", "개체", "modality(소속)", ""),
    ("profiles[].name", "사전", "dict:modality", "코드 연결 동의어"),
    ("profiles[].name_en", "사전", "dict:modality", "코드 연결 동의어(en)"),
    ("profiles[].phase", "개체", "modality.floor_phase", "사전 floor_phase"),
    ("profiles[].phaseOrder", "개체", "modality.floor_phase_order", "중복 원문 보존 (질문 21)"),
    ("profiles[].mechanism[]", "사전", "dict:technique", "R5"),
    ("profiles[].hasProtein", "개체", "modality.flags.hasProtein", ""),
    ("profiles[].hasHA", "개체", "modality.flags.hasHA", ""),
    ("profiles[].usesGel", "개체", "modality.flags.usesGel", ""),
    ("profiles[].createsWound", "개체", "modality.flags.createsWound", ""),
    ("profiles[].createsChannel", "개체", "modality.flags.createsChannel", ""),
    ("profiles[].thermalLoad", "개체", "modality.risk_scores.thermalLoad", ""),
    ("profiles[].bleedingRisk", "개체", "modality.risk_scores.bleedingRisk", ""),
    ("profiles[].swellingRisk", "개체", "modality.risk_scores.swellingRisk", ""),
    ("profiles[].needsAnesthesia", "개체", "modality.anesthesia", "사전 anesthesia"),
    ("profiles[].position", "개체", "modality.position", "사전 position"),
    ("profiles[].needsCleansing", "개체", "modality.flags.needsCleansing", ""),
    ("profiles[].prepTime", "개체", "modality.prep_time_min", ""),
    ("profiles[].prepNotes", "개체", "modality.prep_notes", ""),
    ("profiles[].durationMin", "개체", "modality.duration_min", ""),
    ("profiles[].durationMax", "개체", "modality.duration_max", ""),
    ("profiles[].moa_summary", "개체", "modality.moa_summary", ""),
    ("profiles[].practicalNotes[]", "개체", "modality.practical_notes", ""),
    ("profiles[].aftercare[]", "개체", "modality.aftercare", "출처=procedure-profiles"),
]

_prod = META[:]
for sec in ["botulinum_toxin", "filler_ha", "biostimulator", "skin_booster", "thread_lift", "prp_exosome", "stem_cell"]:
    _prod.append((f"{sec}.category_id", "엣지", "R4.from(modality)", f"섹션 키 `{sec}` 는 계열 alias"))
_prod.append(("energy_device.category_id[]", "엣지", "R4.from(modality)", "[M8,M9,M11] 집합 — 제품별 계열은 taxonomy 소속으로"))
for sec in ["botulinum_toxin", "filler_ha", "biostimulator", "skin_booster", "thread_lift", "energy_device", "prp_exosome", "stem_cell"]:
    _prod += [
        (f"{sec}.products[].name", "개체", "product.name", ""),
        (f"{sec}.products[].name_en", "개체", "product.name_en", ""),
        (f"{sec}.products[].manufacturer", "사전", "dict:manufacturer", "product.manufacturer. `-` = null"),
        (f"{sec}.products[].country", "사전", "dict:country", "product.country. `-` = null"),
    ]
for sec in ["botulinum_toxin", "filler_ha", "biostimulator", "skin_booster", "thread_lift", "prp_exosome", "stem_cell"]:
    _prod.append((f"{sec}.products[].mfds", "개체", "product.mfds", "신뢰 2 식약처 (질문 16)"))
_prod += [
    ("botulinum_toxin.products[].note", "개체", "product.note", ""),
    ("biostimulator.products[].ingredient", "사전", "dict:ingredient_material", "product.ingredient_material"),
    ("skin_booster.products[].ingredient", "사전", "dict:ingredient_material", ""),
    ("skin_booster.products[].note", "개체", "product.note", "스킨보톡스 → not_separate_product (질문 18)"),
    ("thread_lift.products[].material", "사전", "dict:ingredient_material", ""),
    ("energy_device.products[].type", "사전", "dict:product_type", "기법 사전 후보이기도 함 → R5"),
    ("prp_exosome.products[].type", "사전", "dict:product_type", ""),
    ("prp_exosome.products[].note", "개체", "product.note", ""),
    ("prp_exosome.products[].legal_warning", "개체", "product.legal_warning", ""),
    ("prp_exosome.products[].regulatory_status", "개체", "product.regulatory_status", ""),
    ("stem_cell.products[].type", "사전", "dict:product_type", ""),
]
COLMAP["products.json"] = _prod

COLMAP["synergy.json"] = [
    ("version", "개체", "source_file.version", ""),
    ("updated", "개체", "source_file.updated", ""),
    ("links[].from", "엣지", "R18.from_label", "`M코드-이름` 분해 ③ → 계열 확정, 이름은 사전 일치만 (질문 8)"),
    ("links[].from_category", "엣지", "R18.from_modality", ""),
    ("links[].to", "엣지", "R18.to_label", ""),
    ("links[].to_category", "엣지", "R18.to_modality", ""),
    ("links[].type", "사전", "dict:synergy_type", "R18.kind 매핑(함께→synergy_together …)"),
    ("links[].reason", "엣지", "R18.reason", ""),
    ("links[].timing", "엣지", "R18.timing", ""),
    ("links[].target", "사전", "dict:purpose_label", "R18.target"),
]

_tx = [
    ("modality[].id", "개체", "modality.code", "정본 (질문 1)"),
    ("modality[].category", "개체", "modality.name", "정본 한글명 = 사전 modality 정준값"),
    ("modality[].category_en", "개체", "modality.name_en", "사전 동의어(en)"),
    ("modality[].group", "사전", "dict:modality_group", "modality.group"),
    ("modality[].name", "버림", "drop", "17/17 `category` 와 같은 값 — 중복 키"),
    ("modality[].subcategories[].id", "개체", "modality_subcategory.code", "+ aliases"),
    ("modality[].subcategories[].label", "개체", "modality_subcategory.label", "기법 사전 후보 → R5"),
    ("modality[].subcategories[].description", "개체", "modality_subcategory.description", ""),
    ("modality[].subcategories[].items", "개체", "modality_subcategory.items_present", "빈 배열 2 = null"),
    ("modality[].subcategories[].items[].id", "개체", "procedure.aliases", "질문 4"),
    ("modality[].subcategories[].items[].name", "개체", "procedure.name", "R3 제품 일치"),
    ("modality[].subcategories[].items[].detail", "개체", "procedure.detail", "빈 문자열 20 = null"),
    ("modality[].subcategories[].items[].extracted.overview", "개체", "procedure.overview", ""),
    ("modality[].subcategories[].items[].extracted.mechanism", "개체", "procedure.mechanism", ""),
    ("modality[].subcategories[].items[].extracted.indications.primary[]", "개체", "procedure.indications_primary", ""),
    ("modality[].subcategories[].items[].extracted.indications.extended[]", "개체", "procedure.indications_extended", ""),
    ("modality[].subcategories[].items[].extracted.indications.secondary[]", "개체", "procedure.indications_extended", "동의 키 ③ (질문 20)"),
    ("modality[].subcategories[].items[].extracted.safety.common[]", "개체", "adverse_effect.name", "R15.frequency_class=common"),
    ("modality[].subcategories[].items[].extracted.safety.serious[]", "개체", "adverse_effect.name", "R15.frequency_class=serious"),
    ("modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]", "개체", "adverse_effect.name", "동의 키 → common"),
    ("modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]", "개체", "adverse_effect.name", "동의 키 → serious"),
    ("modality[].subcategories[].items[].extracted.safety.long_term[]", "개체", "adverse_effect.name", "R15.frequency_class=long_term"),
    ("modality[].subcategories[].items[].extracted.safety.contraindications[]", "개체", "person_condition.name", "R16 (level=unspecified)"),
    ("modality[].subcategories[].items[].extracted.safety.note", "개체", "procedure.safety_note", ""),
    ("modality[].subcategories[].items[].extracted.onset_duration.onset", "개체", "procedure.onset", ""),
    ("modality[].subcategories[].items[].extracted.onset_duration.duration", "개체", "procedure.duration", ""),
    ("modality[].subcategories[].items[].extracted.onset_duration.peak", "개체", "procedure.peak", ""),
    ("modality[].subcategories[].items[].extracted.onset_duration.peak_effect", "개체", "procedure.peak", "동의 키 ③"),
    ("modality[].subcategories[].items[].extracted.onset_duration.maintenance", "개체", "procedure.maintenance", ""),
    ("modality[].subcategories[].items[].extracted.aftercare[]", "개체", "procedure.aftercare", ""),
    ("modality[].subcategories[].items[].verification_needed", "개체", "decision.what", "kind=verification_hold (질문 23)"),
    ("modality[].subcategories[].items[].classification_issue", "개체", "decision.what", "kind=ledger_correction_note"),
    ("modality[].subcategories[].items[].correction_note", "개체", "decision.what", "kind=ledger_correction_note"),
    ("modality[].subcategories[].items[].reclassified_to", "개체", "decision.new_value", "kind=reclassification → R2 재배치"),
    ("modality[].subcategories[].items[].canonical_category", "개체", "decision.new_value", "kind=canonical_mapping (하위분류 사전 일치만)"),
    ("modality[].subcategories[].items[].is_marketing_name", "개체", "procedure.is_marketing_name", ""),
    ("modality[].subcategories[].items[].ingredient_basis", "개체", "procedure.ingredient_basis", ""),
    ("modality[].subcategories[].items[].naming_caveat", "개체", "procedure.naming_caveat", ""),
    ("modality[].extracted.overview", "개체", "modality.overview", "출처=taxonomy (질문 2)"),
    ("modality[].extracted.mechanism", "개체", "modality.mechanism", ""),
    ("modality[].extracted.indications.primary[]", "개체", "modality.indications_primary", ""),
    ("modality[].extracted.indications.extended[]", "개체", "modality.indications_extended", ""),
    ("modality[].extracted.contraindications.absolute[]", "개체", "person_condition.name", "R16.level=absolute"),
    ("modality[].extracted.contraindications.relative[]", "개체", "person_condition.name", "R16.level=relative"),
    ("modality[].extracted.safety.common[]", "개체", "adverse_effect.name", "R15 common"),
    ("modality[].extracted.safety.uncommon[]", "개체", "adverse_effect.name", "R15 uncommon"),
    ("modality[].extracted.safety.serious[]", "개체", "adverse_effect.name", "R15 serious"),
    ("modality[].extracted.onset_duration.onset", "개체", "modality.onset", ""),
    ("modality[].extracted.onset_duration.peak", "개체", "modality.peak", ""),
    ("modality[].extracted.onset_duration.duration", "개체", "modality.duration", ""),
    ("modality[].extracted.aftercare[]", "개체", "modality.aftercare", ""),
    ("modality[].extracted.related_techniques[]", "개체", "modality.related_techniques", ""),
    ("modality[].products", "개체", "modality.products_present", "빈 배열 7 = null (질문 15)"),
    ("modality[].products[].id", "개체", "product.aliases", "M1-P-0 형 → R4 소속"),
    ("modality[].products[].name", "개체", "product.name", "products.json 과 병합 (질문 3)"),
    ("modality[].products[].name_en", "개체", "product.name_en", ""),
    ("modality[].products[].manufacturer", "사전", "dict:manufacturer", ""),
    ("modality[].products[].country", "사전", "dict:country", ""),
    ("modality[].products[].mfds", "개체", "product.mfds", "null 17 = 미입력 (질문 16)"),
    ("modality[].products[].ingredient", "사전", "dict:ingredient_material", ""),
    ("modality[].products[].material", "사전", "dict:ingredient_material", ""),
    ("modality[].products[].type", "사전", "dict:product_type", ""),
    ("modality[].products[].note", "개체", "product.note", ""),
    ("modality[].products[].extracted.overview", "개체", "product.overview", ""),
    ("modality[].products[].extracted.mechanism", "개체", "product.mechanism", ""),
    ("modality[].products[].extracted.indications.primary[]", "개체", "product.indications_primary", ""),
    ("modality[].products[].extracted.indications.secondary[]", "개체", "product.indications_extended", "동의 키 ③"),
    ("modality[].products[].extracted.safety.common[]", "개체", "adverse_effect.name", "R15 (product) common"),
    ("modality[].products[].extracted.safety.serious[]", "개체", "adverse_effect.name", "R15 (product) serious"),
    ("modality[].products[].extracted.safety.common_side_effects[]", "개체", "adverse_effect.name", "동의 키 → common"),
    ("modality[].products[].extracted.safety.contraindications[]", "개체", "product.contraindication_notes", "병합 금기 문장"),
    ("modality[].products[].extracted.safety.note", "개체", "product.safety_note", ""),
    ("modality[].products[].extracted.onset_duration.onset", "개체", "product.onset", ""),
    ("modality[].products[].extracted.onset_duration.duration", "개체", "product.duration", ""),
    ("modality[].products[].extracted.onset_duration.peak_effect", "개체", "product.peak", "동의 키 ③"),
    ("modality[].products[].extracted.onset_duration.diffusion", "개체", "product.diffusion", ""),
    ("modality[].products[].extracted.aftercare[]", "개체", "product.aftercare", ""),
    ("problem[].id", "개체", "problem.code", "정본 (질문 12)"),
    ("problem[].category", "개체", "problem.name", "= 사전 problem 정준값"),
    ("problem[].category_en", "개체", "problem.name_en", ""),
    ("problem[].subcategories[].id", "개체", "problem_subcategory.code", ""),
    ("problem[].subcategories[].label", "개체", "problem_subcategory.label", "부위 사전 동의어 원천 (질문 24) → R11"),
    ("problem[].subcategories[].items[].id", "개체", "complaint.aliases", ""),
    ("problem[].subcategories[].items[].name", "개체", "complaint.name", ""),
    ("problem[].subcategories[].items[].detail", "개체", "complaint.detail", ""),
    ("problem[].subcategories[].items[].modality_ref[]", "엣지", "R8.to(modality)", ""),
    ("problem[].subcategories[].items[].modality_ref", "엣지", "R8(none)", "빈 배열 26 = null → 질문 14 두 묶음"),
]
COLMAP["taxonomy.json"] = _tx

COLMAP["treatment-optimization.json"] = [
    ("version", "개체", "source_file.version", ""),
    ("updated", "개체", "source_file.updated", ""),
    ("consensus_method", "개체", "source_file.method", "신뢰 4 근거"),
    ("optimization_principles[]", "개체", "clinical_rule.text", "kind=principle"),
    ("by_concern[].concern", "엣지", "R13.problem_label", "고민 사전 일치만 (질문 12)"),
    ("by_concern[].concern_en", "사전", "dict:problem", "후보(en) — 자동 동의어 아님"),
    ("by_concern[].icon", "사전", "dict:purpose_label", ""),
    ("by_concern[].severity_levels[].level", "엣지", "R13.severity", "`경미 (설명)` 분해 ③ → 사전 concern_severity + severity_detail"),
    ("by_concern[].severity_levels[].optimal_combo[]", "엣지", "R12.target_label", "kind=optimization_plan. 사전 일치만"),
    ("by_concern[].severity_levels[].sequence", "개체", "package.sequence_text", ""),
    ("by_concern[].severity_levels[].rationale", "개체", "package.clinical_rationale", ""),
    ("by_concern[].severity_levels[].expected_sessions", "개체", "package.expected_sessions", ""),
    ("by_concern[].severity_levels[].total_duration", "개체", "package.total_duration", ""),
    ("by_concern[].severity_levels[].evidence_level", "개체", "package.evidence_level", "사전 evidence_level"),
    ("by_concern[].severity_levels[].contraindicated_combos", "개체", "package.contraindicated_combos", "빈 배열 11 = null"),
    ("by_concern[].severity_levels[].contraindicated_combos[]", "개체", "package.contraindicated_combos", "R18 변환은 사전 일치만"),
    ("by_concern[].severity_levels[].caveats[]", "개체", "package.caveats", ""),
    ("by_age_group[].age", "개체", "person_condition.name", "kind=age_group, 사전 age_group"),
    ("by_age_group[].primary_concerns[]", "엣지", "R17.target_label", "relation_kind=primary_concern → 고민 사전 일치만"),
    ("by_age_group[].recommended_base[]", "엣지", "R17.target_label", "recommended_base"),
    ("by_age_group[].avoid[]", "엣지", "R17.target_label", "avoid"),
    ("by_age_group[].maintenance", "개체", "person_condition.maintenance", ""),
    ("by_age_group[].annual_focus", "개체", "person_condition.annual_focus", ""),
    ("by_age_group[].upgrade[]", "엣지", "R17.target_label", "upgrade"),
    ("by_age_group[].note", "개체", "person_condition.note", ""),
    ("combination_rules[].rule", "개체", "clinical_rule.text", "kind=combination_rule"),
    ("combination_rules[].detail", "개체", "clinical_rule.detail", ""),
    ("combination_rules[].evidence", "개체", "citation.text", "kind=guideline_text → R19"),
    ("combination_rules[].consensus", "사전", "dict:consensus", "clinical_rule.consensus"),
    ("combination_rules[].priority", "사전", "dict:rule_priority", "clinical_rule.priority"),
    ("annual_plans[].plan_name", "개체", "package.name", "kind=annual_plan"),
    ("annual_plans[].age_group", "사전", "dict:age_group", "package.age_group"),
    ("annual_plans[].annual_budget_range", "개체", "package.price_range", ""),
    ("annual_plans[].focus", "개체", "package.focus", ""),
    ("annual_plans[].schedule[].month", "엣지", "R12.month", ""),
    ("annual_plans[].schedule[].procedures[]", "엣지", "R12.target_label", "`토닝 4회` 횟수 섞임 — 사전 일치만"),
]

COLMAP["treatment-sequence.json"] = META + [
    ("principles[]", "개체", "clinical_rule.text", "kind=principle"),
    ("sequence_order[].order", "개체", "modality.same_session_order.order", "categories[] 끝에"),
    ("sequence_order[].phase", "사전", "dict:session_phase", "modality.same_session_order.phase"),
    ("sequence_order[].categories[]", "개체", "modality.same_session_order(소속)", "코드/코드+라벨/라벨 세 형식 (질문 7) — 미해결은 ⑨"),
    ("sequence_order[].reason", "개체", "modality.same_session_order.reason", ""),
    ("incompatible_same_day[].pair[]", "엣지", "R18.from_label/to_label", "kind=incompatible_same_day. 사전 일치만"),
    ("incompatible_same_day[].reason", "엣지", "R18.reason", ""),
    ("common_combos[].name", "개체", "package.name", "kind=session_combo"),
    ("common_combos[].sequence[]", "엣지", "R12.target_label", "order = 배열 순서"),
    ("common_combos[].total_time", "개체", "package.total_duration", ""),
    ("common_combos[].note", "개체", "package.note", ""),
    ("minimum_intervals[].from", "엣지", "R18.from_label", "kind=minimum_interval. 사람 조건(이소트레티노인)도 from 가능"),
    ("minimum_intervals[].to", "엣지", "R18.to_label", ""),
    ("minimum_intervals[].min_days", "엣지", "R18.min_interval_value", "unit=day (질문 22)"),
    ("minimum_intervals[].min_months", "엣지", "R18.min_interval_value", "unit=month"),
    ("minimum_intervals[].source", "개체", "citation.text", "kind=guideline_text → R18.source_ref"),
    ("minimum_intervals[].reason", "엣지", "R18.reason", ""),
]


def resolve(file, path):
    """path 에 맞는 규칙 하나를 돌려준다. 정확 일치 우선, 그다음 regex."""
    rules = COLMAP[file]
    for r in rules:
        if isinstance(r[0], str) and r[0] == path:
            return r
    for r in rules:
        if not isinstance(r[0], str) and r[0].match(path):
            return r
    return None
