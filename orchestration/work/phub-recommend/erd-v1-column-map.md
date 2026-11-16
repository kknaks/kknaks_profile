# ERD v1 — 원장 잎 키 573 행선지 표

작성 2026-11-04 · 입력 `bronze-ledger-column-scan.json`(잎 키 573) · 행선지 범주 5: 개체(개체.속성) / 사전 / 엣지(엣지 속성) / 브론즈(브론즈 원문만) / 버림

표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v1.md §3) · `bronze` · `drop`. 비고의 ①~⑤ 는 품질 규칙 번호, 「질문 N」은 §7 답.

## 요약

| 행선지 | 잎 키 수 |
|---|---|
| 개체 | 378 |
| 엣지 | 107 |
| 사전 | 75 |
| 브론즈 | 12 |
| 버림 | 1 |
| 합계 | 573 |

## `anatomy-danger-zones.json` — 잎 키 67

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `consensus_method` | str | 1 | 개체 | `source_file.method` | 신뢰 순위 4 근거 |
| 4 | `critical_safety_facts.minimum_filler_for_blindness` | str | 1 | 개체 | `clinical_rule.text` | kind=critical_safety_fact, topic=키 이름 |
| 5 | `critical_safety_facts.blindness_highest_risk_zones` | str | 1 | 개체 | `clinical_rule.text` | kind=critical_safety_fact |
| 6 | `critical_safety_facts.mechanism` | str | 1 | 개체 | `clinical_rule.text` | kind=critical_safety_fact |
| 7 | `critical_safety_facts.caveat` | str | 1 | 개체 | `clinical_rule.text` | kind=critical_safety_fact |
| 8 | `zones[].id` | str | 11 | 개체 | `site.aliases` | 뼈대 zone id = site canonical_key |
| 9 | `zones[].name_ko` | str | 11 | 개체 | `site.name_ko` | 사전 site 정준 한글명 |
| 10 | `zones[].name_en` | str | 11 | 개체 | `site.name_en` | 사전 site 동의어(en) |
| 11 | `zones[].danger_level` | int | 11 | 개체 | `site.danger_level` | 사전 danger_level 검증 |
| 12 | `zones[].danger_color` | str | 11 | 사전 | `dict:danger_level` | level 의 색 라벨 (zone 마다 level 과 1:1) |
| 13 | `zones[].vessels[].name` | str | 24 | 개체 | `anatomical_structure.name_raw` | kind=vessel. `한글 (영문)` 분해 ③ |
| 14 | `zones[].vessels[].depth_mm` | float | 22 | 엣지 | `R21.depth_mm` |  |
| 15 | `zones[].vessels[].diameter_mm` | float | 24 | 엣지 | `R21.diameter_mm` |  |
| 16 | `zones[].vessels[].course` | str | 24 | 엣지 | `R21.course` |  |
| 17 | `zones[].vessels[].danger` | str | 24 | 엣지 | `R21.danger` |  |
| 18 | `zones[].vessels[].note` | str | 2 | 엣지 | `R21.note` |  |
| 19 | `zones[].vessels[].depth_range_mm[]` | float | 10 | 엣지 | `R21.depth_range_mm` | 단일값/범위 두 형태 원문 보존 |
| 20 | `zones[].nerves[].name` | str | 21 | 개체 | `anatomical_structure.name_raw` | kind=nerve |
| 21 | `zones[].nerves[].type` | str | 21 | 개체 | `anatomical_structure.nerve_type` | 사전 nerve_type |
| 22 | `zones[].nerves[].significance` | str | 21 | 엣지 | `R21.significance` |  |
| 23 | `zones[].safe_injection_depth` | str | 11 | 개체 | `site.safe_injection_depth` |  |
| 24 | `zones[].tissue_data.frontalis_thickness.midpupil_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 25 | `zones[].tissue_data.frontalis_thickness.lateral_canthus_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 26 | `zones[].tissue_data.frontalis_thickness.lateral_orbital_rim_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 27 | `zones[].tissue_data.skin_to_periosteum_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 28 | `zones[].tissue_data.notes` | str | 11 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 29 | `zones[].clinical_pearls[]` | str | 61 | 개체 | `site.clinical_pearls` |  |
| 30 | `zones[].botox_specific.target_muscle` | str | 11 | 엣지 | `R22.target_muscle` | site→M1 |
| 31 | `zones[].botox_specific.risk` | str | 11 | 엣지 | `R22.risk_text` | site→M1 |
| 32 | `zones[].botox_specific.safe_zone` | str | 11 | 엣지 | `R22.safe_zone` | site→M1 |
| 33 | `zones[].botox_specific.diffusion_range_cm` | str | 1 | 엣지 | `R22.diffusion_range_cm` | site→M1 |
| 34 | `zones[].botox_specific.key_warning` | str | 11 | 엣지 | `R22.key_warning` | site→M1 |
| 35 | `zones[].botox_specific.dose_range` | str | 11 | 엣지 | `R22.dose_range` | site→M1 |
| 36 | `zones[].filler_specific.risk_level` | int | 11 | 엣지 | `R22.risk_level` | site→M2. 사전 danger_level |
| 37 | `zones[].filler_specific.primary_risk` | str | 11 | 엣지 | `R22.primary_risk` | site→M2 |
| 38 | `zones[].filler_specific.safe_technique` | str | 11 | 엣지 | `R22.safe_technique` | site→M2 |
| 39 | `zones[].filler_specific.max_per_point_ml` | float | 11 | 엣지 | `R22.max_per_point_ml` | site→M2 |
| 40 | `zones[].filler_specific.preferred_product` | str | 11 | 엣지 | `R22.preferred_product` | site→M2 |
| 41 | `zones[].tissue_data.csm_mean_thickness_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 42 | `zones[].tissue_data.csm_thickness_variation_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 43 | `zones[].filler_specific.emergency_protocol` | str | 3 | 엣지 | `R22.emergency_protocol` | site→M2 |
| 44 | `zones[].tissue_data.stl_entry_point` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 45 | `zones[].tissue_data.pitanguy_line` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 46 | `zones[].tissue_data.tear_trough_anatomy` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 47 | `zones[].tissue_data.muscle_fiber_data` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 48 | `zones[].tissue_data.orbital_septum` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 49 | `zones[].tissue_data.rhinion_subcutaneous_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 50 | `zones[].tissue_data.rhinion_data_source` | str | 1 | 개체 | `citation.text` | kind=guideline_text. site.tissue_data 에도 원문 키 보존 |
| 51 | `zones[].tissue_data.nasal_tip_skin_thickness_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 52 | `zones[].tissue_data.facial_artery_distance_to_nlf_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 53 | `zones[].tissue_data.asian_adjacent_distribution_percent` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 54 | `zones[].tissue_data.within_5mm_percent` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 55 | `zones[].tissue_data.facial_artery_diameter_mandible_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 56 | `zones[].tissue_data.facial_artery_diameter_nasal_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 57 | `zones[].tissue_data.buccal_fat_pad` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 58 | `zones[].tissue_data.smas_depth_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 59 | `zones[].tissue_data.sub_smas_vs_subcutaneous` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 60 | `zones[].tissue_data.labial_artery_depth_range_mm[]` | float | 2 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 61 | `zones[].tissue_data.superior_labial_artery_submucosal_percent` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 62 | `zones[].tissue_data.mental_foramen_location` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 63 | `zones[].tissue_data.dao_coverage` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 64 | `zones[].tissue_data.marginal_mandibular_depth` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 65 | `zones[].tissue_data.facial_artery_crossing` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 66 | `zones[].tissue_data.platysma_thickness_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 67 | `zones[].tissue_data.platysma_coverage` | str | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |

## `combo-recipes.json` — 잎 키 15

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `recipes[].id` | str | 7 | 개체 | `package.aliases` | kind=recipe (질문 6) |
| 5 | `recipes[].name` | str | 7 | 개체 | `package.name` |  |
| 6 | `recipes[].subtitle` | str | 7 | 개체 | `package.subtitle` |  |
| 7 | `recipes[].goal` | str | 7 | 사전 | `dict:purpose_label` | package.purpose |
| 8 | `recipes[].intensity` | str | 7 | 사전 | `dict:package_tier` | package.tier |
| 9 | `recipes[].procedures[]` | str | 19 | 엣지 | `R12.member(modality)` | M 코드 → 계열 깊이 |
| 10 | `recipes[].expectedResults` | str | 7 | 개체 | `package.expected_result` |  |
| 11 | `recipes[].patientExplanation` | str | 7 | 개체 | `package.patient_explanation` |  |
| 12 | `recipes[].analogy` | str | 7 | 개체 | `package.analogy` |  |
| 13 | `recipes[].repeatCycle` | str | 7 | 개체 | `package.repeat_cycle` |  |
| 14 | `recipes[].followUp[].week` | int | 28 | 개체 | `package.follow_up.week` |  |
| 15 | `recipes[].followUp[].action` | str | 28 | 개체 | `package.follow_up.action` |  |

## `complications.json` — 잎 키 17

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `severity_levels.mild` | str | 1 | 사전 | `dict:severity` | 정의문 |
| 2 | `severity_levels.moderate` | str | 1 | 사전 | `dict:severity` | 정의문 |
| 3 | `severity_levels.severe` | str | 1 | 사전 | `dict:severity` | 정의문 |
| 4 | `severity_levels.critical` | str | 1 | 사전 | `dict:severity` | 정의문 |
| 5 | `categories[].id` | str | 10 | 엣지 | `R15.from(modality)` | 계열 끝 |
| 6 | `categories[].name` | str | 10 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 7 | `categories[].complications[].name` | str | 65 | 개체 | `adverse_effect.name` | kind=named |
| 8 | `categories[].complications[].severity` | str | 65 | 엣지 | `R15.severity` | 사전 severity |
| 9 | `categories[].complications[].incidence` | str | 65 | 엣지 | `R15.incidence` |  |
| 10 | `categories[].complications[].onset` | str | 65 | 엣지 | `R15.onset` |  |
| 11 | `categories[].complications[].mechanism` | str | 65 | 엣지 | `R15.mechanism` |  |
| 12 | `categories[].complications[].risk_factors` | list(empty) | 46 | 엣지 | `R15.risk_factors` | 빈 배열 46 = null ⑤ |
| 13 | `categories[].complications[].management` | str | 65 | 엣지 | `R15.management` |  |
| 14 | `categories[].complications[].prevention` | str | 65 | 엣지 | `R15.prevention` |  |
| 15 | `categories[].complications[].evidence` | str | 38 | 개체 | `citation.url` | kind=url, `;` 분리 ③ → R15.evidence_ref |
| 16 | `categories[].complications[].duration` | str | 19 | 엣지 | `R15.duration` |  |
| 17 | `categories[].complications[].risk_factors[]` | str | 92 | 엣지 | `R15.risk_factors` |  |

## `consent-checklist.json` — 잎 키 8

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `categories[].id` | str | 17 | 엣지 | `R16.from(modality)` | 계열 끝 (R15 emergency_signs 도) |
| 5 | `categories[].name` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 6 | `categories[].mandatory_disclosures[]` | str | 109 | 개체 | `modality.mandatory_disclosures` | 고지문 = 속성 |
| 7 | `categories[].contraindications[]` | str | 105 | 개체 | `person_condition.name` | kind=condition, R16.level=consent |
| 8 | `categories[].emergency_signs[]` | str | 55 | 개체 | `adverse_effect.name` | kind=emergency_sign, R15.frequency_class=emergency |

## `contraindications.json` — 잎 키 10

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `rules[].from` | str | 27 | 엣지 | `R18.from(modality)` | kind=pair_rule |
| 5 | `rules[].from_name` | str | 27 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 6 | `rules[].to` | str | 27 | 엣지 | `R18.to(modality)` |  |
| 7 | `rules[].to_name` | str | 27 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 8 | `rules[].level` | str | 27 | 엣지 | `R18.level` | 사전 interaction_level |
| 9 | `rules[].interval` | str | 27 | 엣지 | `R18.interval_text` |  |
| 10 | `rules[].note` | str | 27 | 엣지 | `R18.note` |  |

## `extracted.json` — 잎 키 24

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `{code}.name` | str | 17 | 사전 | `dict:modality` | 코드 키 연결 동의어 |
| 2 | `{code}.safety.common[]` | str | 59 | 개체 | `adverse_effect.name` | R15.frequency_class=common |
| 3 | `{code}.safety.serious` | null | 2 | 엣지 | `R15(serious)` | null 2 = 미입력 ⑤ (질문 17) |
| 4 | `{code}.safety.uncommon[]` | str | 45 | 개체 | `adverse_effect.name` | R15.frequency_class=uncommon |
| 5 | `{code}.source` | str | 17 | 개체 | `citation.text` | kind=textbook → R19 (modality.extracted_meta 출처) |
| 6 | `{code}.name_en` | str | 17 | 사전 | `dict:modality` | 코드 키 연결 동의어(en) |
| 7 | `{code}.overview` | str | 17 | 개체 | `modality.overview` | 출처=extracted.json, taxonomy 와 충돌 검사 (질문 2) |
| 8 | `{code}.aftercare[]` | str | 53 | 개체 | `modality.aftercare` |  |
| 9 | `{code}.mechanism` | str | 17 | 개체 | `modality.mechanism` | 질문 2 |
| 10 | `{code}.indications.primary[]` | str | 56 | 개체 | `modality.indications_primary` |  |
| 11 | `{code}.indications.extended[]` | str | 101 | 개체 | `modality.indications_extended` |  |
| 12 | `{code}.source_type` | str | 17 | 개체 | `modality.extracted_meta.source_type` | 사전 source_type |
| 13 | `{code}.extracted_at` | str | 17 | 개체 | `modality.extracted_meta.extracted_at` |  |
| 14 | `{code}.procedure_id` | str | 17 | 개체 | `modality.aliases` | M1-BOTOX 형 |
| 15 | `{code}.onset_duration.peak` | str | 17 | 개체 | `modality.peak` |  |
| 16 | `{code}.onset_duration.onset` | str | 17 | 개체 | `modality.onset` |  |
| 17 | `{code}.onset_duration.duration` | str | 17 | 개체 | `modality.duration` |  |
| 18 | `{code}.contraindications.absolute[]` | str | 53 | 개체 | `person_condition.name` | R16.level=absolute |
| 19 | `{code}.contraindications.relative[]` | str | 55 | 개체 | `person_condition.name` | R16.level=relative |
| 20 | `{code}.guardrail_version` | str | 17 | 개체 | `modality.extracted_meta.guardrail_version` |  |
| 21 | `{code}.related_techniques[]` | str | 51 | 개체 | `modality.related_techniques` |  |
| 22 | `{code}.safety.serious[]` | str | 37 | 개체 | `adverse_effect.name` | R15.frequency_class=serious |
| 23 | `{code}.safety.emergency[]` | str | 2 | 개체 | `adverse_effect.name` | R15.frequency_class=emergency |
| 24 | `{code}.updated` | str | 1 | 개체 | `modality.extracted_meta.updated` | M3 만 |

## `literature-evidence.json` — 잎 키 68

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` |  |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` |  |
| 3 | `source_method` | str | 1 | 개체 | `source_file.method` | 신뢰 순위 1 근거 |
| 4 | `accuracy_summary.scored_by` | str | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 5 | `accuracy_summary.rubric` | str | 1 | 사전 | `dict:accuracy_rubric` | accuracy_score 값 구간 정의 |
| 6 | `accuracy_summary.overall_average` | float | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 7 | `accuracy_summary.n_scored` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 8 | `accuracy_summary.by_field_average.moa` | float | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 9 | `accuracy_summary.by_field_average.adverse_effects` | float | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 10 | `accuracy_summary.by_field_average.effects` | float | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 11 | `accuracy_summary.by_category_average.{code}` | float | 7 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 12 | `accuracy_summary.patient_ko_coverage` | str | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 13 | `accuracy_summary.patient_translations_coverage.ko` | str | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 14 | `accuracy_summary.patient_translations_coverage.en` | str | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 15 | `accuracy_summary.patient_translations_coverage.zh` | str | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 16 | `accuracy_summary.patient_translations_coverage.ja` | str | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 문장 단위에서 재계산 |
| 17 | `categories.{code}.name` | str | 17 | 사전 | `dict:modality` | 코드 키 연결 동의어(en 학술명) |
| 18 | `categories.{code}.moa[].statement` | str | 50 | 개체 | `evidence_statement.statement` | kind=moa |
| 19 | `categories.{code}.moa[].citations[].authors` | str | 50 | 개체 | `citation.authors` | kind=pubmed, pmid 동일성 → R19 |
| 20 | `categories.{code}.moa[].citations[].title` | str | 50 | 개체 | `citation.title` | kind=pubmed, pmid 동일성 → R19 |
| 21 | `categories.{code}.moa[].citations[].journal` | str | 50 | 개체 | `citation.journal` | kind=pubmed, pmid 동일성 → R19 |
| 22 | `categories.{code}.moa[].citations[].year` | int | 50 | 개체 | `citation.year` | kind=pubmed, pmid 동일성 → R19 |
| 23 | `categories.{code}.moa[].citations[].pmid` | str | 50 | 개체 | `citation.pmid` | kind=pubmed, pmid 동일성 → R19 |
| 24 | `categories.{code}.moa[].citations[].doi` | str | 48 | 개체 | `citation.doi` | kind=pubmed, pmid 동일성 → R19 |
| 25 | `categories.{code}.moa[].citations[].pmc` | str | 49 | 개체 | `citation.pmc` | kind=pubmed, pmid 동일성 → R19 |
| 26 | `categories.{code}.moa[].citations[].oa_url` | str | 49 | 개체 | `citation.oa_url` | kind=pubmed, pmid 동일성 → R19 |
| 27 | `categories.{code}.moa[].accuracy_score` | int | 6 | 개체 | `evidence_statement.accuracy_score` |  |
| 28 | `categories.{code}.moa[].accuracy_note` | str | 6 | 개체 | `evidence_statement.accuracy_note` |  |
| 29 | `categories.{code}.moa[].patient_ko` | str | 50 | 개체 | `evidence_statement.patient_text.ko` | 질문 19 정제 |
| 30 | `categories.{code}.moa[].patient_en` | str | 50 | 개체 | `evidence_statement.patient_text.en` | 질문 19 정제 |
| 31 | `categories.{code}.moa[].patient_zh` | str | 50 | 개체 | `evidence_statement.patient_text.zh` | 질문 19 정제 |
| 32 | `categories.{code}.moa[].patient_ja` | str | 50 | 개체 | `evidence_statement.patient_text.ja` | 질문 19 정제 |
| 33 | `categories.{code}.moa[].added_at` | str | 44 | 개체 | `evidence_statement.added_at` |  |
| 34 | `categories.{code}.adverse_effects[].statement` | str | 32 | 개체 | `adverse_effect.name` | kind=literature_claim |
| 35 | `categories.{code}.adverse_effects[].citations[].authors` | str | 32 | 개체 | `citation.authors` | kind=pubmed, pmid 동일성 → R19 |
| 36 | `categories.{code}.adverse_effects[].citations[].title` | str | 32 | 개체 | `citation.title` | kind=pubmed, pmid 동일성 → R19 |
| 37 | `categories.{code}.adverse_effects[].citations[].journal` | str | 32 | 개체 | `citation.journal` | kind=pubmed, pmid 동일성 → R19 |
| 38 | `categories.{code}.adverse_effects[].citations[].year` | int | 32 | 개체 | `citation.year` | kind=pubmed, pmid 동일성 → R19 |
| 39 | `categories.{code}.adverse_effects[].citations[].pmid` | str | 32 | 개체 | `citation.pmid` | kind=pubmed, pmid 동일성 → R19 |
| 40 | `categories.{code}.adverse_effects[].citations[].doi` | str | 30 | 개체 | `citation.doi` | kind=pubmed, pmid 동일성 → R19 |
| 41 | `categories.{code}.adverse_effects[].citations[].pmc` | str | 29 | 개체 | `citation.pmc` | kind=pubmed, pmid 동일성 → R19 |
| 42 | `categories.{code}.adverse_effects[].citations[].oa_url` | str | 29 | 개체 | `citation.oa_url` | kind=pubmed, pmid 동일성 → R19 |
| 43 | `categories.{code}.adverse_effects[].accuracy_score` | int | 8 | 개체 | `adverse_effect.accuracy_score` |  |
| 44 | `categories.{code}.adverse_effects[].accuracy_note` | str | 8 | 개체 | `adverse_effect.accuracy_note` |  |
| 45 | `categories.{code}.adverse_effects[].patient_ko` | str | 32 | 개체 | `adverse_effect.patient_text.ko` | 질문 19 정제 |
| 46 | `categories.{code}.adverse_effects[].patient_en` | str | 32 | 개체 | `adverse_effect.patient_text.en` | 질문 19 정제 |
| 47 | `categories.{code}.adverse_effects[].patient_zh` | str | 32 | 개체 | `adverse_effect.patient_text.zh` | 질문 19 정제 |
| 48 | `categories.{code}.adverse_effects[].patient_ja` | str | 32 | 개체 | `adverse_effect.patient_text.ja` | 질문 19 정제 |
| 49 | `categories.{code}.adverse_effects[].added_at` | str | 24 | 개체 | `adverse_effect.added_at` |  |
| 50 | `categories.{code}.effects[].statement` | str | 37 | 개체 | `evidence_statement.statement` | kind=effect |
| 51 | `categories.{code}.effects[].citations[].authors` | str | 37 | 개체 | `citation.authors` | kind=pubmed, pmid 동일성 → R19 |
| 52 | `categories.{code}.effects[].citations[].title` | str | 37 | 개체 | `citation.title` | kind=pubmed, pmid 동일성 → R19 |
| 53 | `categories.{code}.effects[].citations[].journal` | str | 37 | 개체 | `citation.journal` | kind=pubmed, pmid 동일성 → R19 |
| 54 | `categories.{code}.effects[].citations[].year` | int | 37 | 개체 | `citation.year` | kind=pubmed, pmid 동일성 → R19 |
| 55 | `categories.{code}.effects[].citations[].pmid` | str | 37 | 개체 | `citation.pmid` | kind=pubmed, pmid 동일성 → R19 |
| 56 | `categories.{code}.effects[].citations[].doi` | str | 35 | 개체 | `citation.doi` | kind=pubmed, pmid 동일성 → R19 |
| 57 | `categories.{code}.effects[].citations[].pmc` | str | 36 | 개체 | `citation.pmc` | kind=pubmed, pmid 동일성 → R19 |
| 58 | `categories.{code}.effects[].citations[].oa_url` | str | 36 | 개체 | `citation.oa_url` | kind=pubmed, pmid 동일성 → R19 |
| 59 | `categories.{code}.effects[].patient_ko` | str | 37 | 개체 | `evidence_statement.patient_text.ko` | 질문 19 정제 |
| 60 | `categories.{code}.effects[].patient_en` | str | 37 | 개체 | `evidence_statement.patient_text.en` | 질문 19 정제 |
| 61 | `categories.{code}.effects[].patient_zh` | str | 37 | 개체 | `evidence_statement.patient_text.zh` | 질문 19 정제 |
| 62 | `categories.{code}.effects[].patient_ja` | str | 37 | 개체 | `evidence_statement.patient_text.ja` | 질문 19 정제 |
| 63 | `categories.{code}.effects[].added_at` | str | 34 | 개체 | `evidence_statement.added_at` |  |
| 64 | `categories.{code}.effects` | list(empty) | 8 | 개체 | `modality.evidence_statement_count` | 빈 배열 8 = null |
| 65 | `categories.{code}.effects[].accuracy_score` | int | 3 | 개체 | `evidence_statement.accuracy_score` |  |
| 66 | `categories.{code}.effects[].accuracy_note` | str | 3 | 개체 | `evidence_statement.accuracy_note` |  |
| 67 | `categories.{code}.moa` | list(empty) | 6 | 개체 | `modality.evidence_statement_count` | 빈 배열 6 = null ⑤ (질문 13) |
| 68 | `categories.{code}.adverse_effects` | list(empty) | 6 | 개체 | `modality.evidence_statement_count` | 빈 배열 6 = null |

## `market-pricing.json` — 잎 키 11

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` |  |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` |  |
| 3 | `currency` | str | 1 | 사전 | `dict:unit` | 통화 단위 (source_file.currency 에도) |
| 4 | `note` | str | 1 | 개체 | `source_file.note` |  |
| 5 | `categories[].id` | str | 17 | 개체 | `modality.price_items(소속)` | 계열 끝 |
| 6 | `categories[].name` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 7 | `categories[].items[].name` | str | 122 | 개체 | `modality.price_items.label` | 시술/제품 연결은 사전 일치만 (질문 11) |
| 8 | `categories[].items[].unit` | str | 122 | 사전 | `dict:unit` | modality.price_items.unit |
| 9 | `categories[].items[].low` | int | 122 | 개체 | `modality.price_items.low` | KRW |
| 10 | `categories[].items[].mid` | int | 122 | 개체 | `modality.price_items.mid` |  |
| 11 | `categories[].items[].high` | int | 122 | 개체 | `modality.price_items.high` |  |

## `patient-education.json` — 잎 키 12

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` |  |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` |  |
| 3 | `categories[].id` | str | 17 | 개체 | `modality(소속)` | 계열 끝 |
| 4 | `categories[].name` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 5 | `categories[].patient_name` | str | 17 | 사전 | `dict:modality` | 환자용 별칭 동의어 (modality.patient_name 에도) |
| 6 | `categories[].simple_explanation` | str | 17 | 개체 | `modality.patient_simple_explanation` |  |
| 7 | `categories[].how_it_works` | str | 17 | 개체 | `modality.patient_how_it_works` |  |
| 8 | `categories[].duration_simple` | str | 17 | 개체 | `modality.patient_duration_simple` |  |
| 9 | `categories[].pain_level` | str | 17 | 개체 | `modality.patient_pain_level` |  |
| 10 | `categories[].downtime` | str | 17 | 개체 | `modality.patient_downtime` |  |
| 11 | `categories[].common_concerns[].q` | str | 51 | 개체 | `modality.faq.q` | FAQ = 속성 |
| 12 | `categories[].common_concerns[].a` | str | 51 | 개체 | `modality.faq.a` |  |

## `pih-risk.json` — 잎 키 18

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `risk_levels.very_low` | str | 1 | 사전 | `dict:pih_risk_level` | 정의(% 범위) |
| 5 | `risk_levels.low` | str | 1 | 사전 | `dict:pih_risk_level` |  |
| 6 | `risk_levels.moderate` | str | 1 | 사전 | `dict:pih_risk_level` |  |
| 7 | `risk_levels.high` | str | 1 | 사전 | `dict:pih_risk_level` |  |
| 8 | `risk_levels.very_high` | str | 1 | 사전 | `dict:pih_risk_level` |  |
| 9 | `notes.{code}` | str | 4 | 개체 | `modality.pih_note` | M1_to_M7 범위 키 전개 ③ |
| 10 | `procedures[].category` | str | 26 | 엣지 | `R15.from.modality_code` | 계열 코드 (procedure_ref 와 함께) |
| 11 | `procedures[].subcategory` | str | 26 | 엣지 | `R15.technique_label` | 사전 technique |
| 12 | `procedures[].name` | str | 26 | 엣지 | `R15.source_label` | 원문 라벨 |
| 13 | `procedures[].procedure_ref` | str | 26 | 엣지 | `R15.from(proc_axis)+target_depth` | 가장 구체 수준 그대로 (질문 5). to=adverse_effect `PIH` |
| 14 | `procedures[].pih_risk` | str | 26 | 엣지 | `R15.pih_risk` | 사전 pih_risk_level |
| 15 | `procedures[].pih_rate` | str | 26 | 엣지 | `R15.pih_rate` |  |
| 16 | `procedures[].fitzpatrick_note` | str | 26 | 엣지 | `R15.fitzpatrick_note` |  |
| 17 | `procedures[].risk_factors[]` | str | 68 | 엣지 | `R15.risk_factors` |  |
| 18 | `procedures[].prevention` | str | 26 | 엣지 | `R15.prevention` |  |

## `post-procedure-timeline.json` — 잎 키 16

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `consensus_method` | str | 1 | 개체 | `source_file.method` | 신뢰 순위 4 근거 |
| 4 | `reaction_levels.normal` | str | 1 | 사전 | `dict:reaction_level` | 정의 |
| 5 | `reaction_levels.abnormal` | str | 1 | 사전 | `dict:reaction_level` |  |
| 6 | `reaction_levels.caution` | str | 1 | 사전 | `dict:reaction_level` |  |
| 7 | `reaction_levels.emergency` | str | 1 | 사전 | `dict:reaction_level` |  |
| 8 | `timelines[].id` | str | 10 | 개체 | `modality.aliases` | timeline name 이 계열명과 정규화 일치할 때만 alias, 아니면 R15.source_label 보조 |
| 9 | `timelines[].category` | str | 10 | 엣지 | `R15.from(proc_axis)+target_depth` | M 코드 → 계열, M16-DCA → 하위분류 (질문 7) |
| 10 | `timelines[].name` | str | 10 | 엣지 | `R15.source_label` | 시술명 원문. 더 구체 대상은 사전 일치만 |
| 11 | `timelines[].phases[].period` | str | 43 | 엣지 | `R15.period` | 사전 period |
| 12 | `timelines[].phases[].label` | str | 43 | 엣지 | `R15.phase_label` | 사전 phase_label |
| 13 | `timelines[].phases[].normal[]` | str | 162 | 개체 | `adverse_effect.name` | kind=symptom, R15.reaction_level=normal |
| 14 | `timelines[].phases[].abnormal[]` | str | 86 | 개체 | `adverse_effect.name` | kind=symptom, reaction_level=abnormal |
| 15 | `timelines[].phases[].caution[]` | str | 93 | 개체 | `adverse_effect.name` | kind=symptom, reaction_level=caution |
| 16 | `timelines[].phases[].emergency[]` | str | 94 | 개체 | `adverse_effect.name` | kind=symptom, reaction_level=emergency |

## `pre-procedure-checklist.json` — 잎 키 11

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `universal_checks[].id` | str | 12 | 개체 | `person_condition.aliases` | kind=check, universal=true |
| 5 | `universal_checks[].label` | str | 12 | 개체 | `person_condition.name` | kind=check, universal=true |
| 6 | `universal_checks[].type` | str | 12 | 개체 | `person_condition.universal_level` | 사전 condition_level |
| 7 | `universal_checks[].description` | str | 12 | 개체 | `person_condition.description` |  |
| 8 | `category_specific[].id` | str | 17 | 엣지 | `R16.from(modality)` |  |
| 9 | `category_specific[].name` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 10 | `category_specific[].checks[].label` | str | 123 | 개체 | `person_condition.name` | kind=check → R16 |
| 11 | `category_specific[].checks[].type` | str | 123 | 엣지 | `R16.level` | 사전 condition_level |

## `problem-combos.json` — 잎 키 18

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `combos[].problem_id` | str | 8 | 엣지 | `R13.to(problem)` | 확정 |
| 5 | `combos[].problem` | str | 8 | 사전 | `dict:problem` | 코드 연결 동의어(처짐/탄력·피부결/톤/항노화) |
| 6 | `combos[].packages[].id` | str | 24 | 개체 | `package.aliases` | kind=consult_package (질문 6) |
| 7 | `combos[].packages[].tier` | str | 24 | 사전 | `dict:package_tier` | package.tier |
| 8 | `combos[].packages[].tierLabel` | str | 24 | 사전 | `dict:package_tier` | tier 와 쌍 → 동의어 |
| 9 | `combos[].packages[].name` | str | 24 | 개체 | `package.name` |  |
| 10 | `combos[].packages[].procedures[]` | str | 63 | 엣지 | `R12.member(modality)` | M 코드 |
| 11 | `combos[].packages[].productTier` | str | 24 | 사전 | `dict:product_tier` | package.product_tier |
| 12 | `combos[].packages[].products[]` | str | 24 | 개체 | `package.products_text` | 조합 문장 — 제품 사전 일치 자동 아님 |
| 13 | `combos[].packages[].priceRange` | str | 24 | 개체 | `package.price_range` | 질문 22 |
| 14 | `combos[].packages[].expectedResult` | str | 24 | 개체 | `package.expected_result` |  |
| 15 | `combos[].packages[].salesPitch` | str | 24 | 개체 | `package.sales_pitch` |  |
| 16 | `combos[].packages[].upsellHook` | str | 24 | 개체 | `package.upsell_hook` |  |
| 17 | `combos[].packages[].clinicalRationale` | str | 24 | 개체 | `package.clinical_rationale` |  |
| 18 | `combos[].packages[].riskBenefit` | str | 24 | 개체 | `package.risk_benefit` |  |

## `problem-packages.json` — 잎 키 19

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `problems[].problem_id` | str | 14 | 개체 | `problem(소속)` | 확정 |
| 5 | `problems[].problem` | str | 14 | 사전 | `dict:problem` | 코드 연결 동의어(= taxonomy 와 동일) |
| 6 | `problems[].complaints[].cc` | str | 115 | 개체 | `complaint.name` | (problem_id, 이름) 유일 일치 결합 (질문 9) |
| 7 | `problems[].complaints[].cc_detail` | str | 115 | 개체 | `complaint.detail` |  |
| 8 | `problems[].complaints[].cc_group` | str | 115 | 사전 | `dict:site` | R10 (질문 24) |
| 9 | `problems[].complaints[].procedures[].name` | str | 254 | 엣지 | `R9.target_label` | 「시술 종류」층 (질문 10) |
| 10 | `problems[].complaints[].procedures[].category` | str | 254 | 엣지 | `R9.modality_code` |  |
| 11 | `problems[].complaints[].procedures[].role` | str | 254 | 엣지 | `R9.role` |  |
| 12 | `problems[].complaints[].procedures[].products[]` | str | 388 | 엣지 | `R9.products` | 제품 사전 일치 → product id, 미일치 4종 ⑨ |
| 13 | `problems[].complaints[].combos[].name` | str | 146 | 개체 | `package.name` | kind=cc_combo |
| 14 | `problems[].complaints[].combos[].combo[]` | str | 277 | 엣지 | `R12.target_label` | 사전 일치만 |
| 15 | `problems[].complaints[].combos[].reason` | str | 146 | 엣지 | `R14.reason` |  |
| 16 | `problems[].complaints[].combos[].evidence` | str | 146 | 엣지 | `R14.evidence` |  |
| 17 | `problems[].complaints[].alternatives[]` | str | 125 | 개체 | `complaint.alternatives` |  |
| 18 | `problems[].complaints[].procedures[].products` | list(empty) | 47 | 엣지 | `R9.products` | 빈 배열 47 = null ⑤ |
| 19 | `problems[].complaints[].combos` | list(empty) | 1 | 개체 | `complaint.combos_present` | 빈 배열 1 = null |

## `procedure-comparison.json` — 잎 키 18

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` |  |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` |  |
| 3 | `comparisons[].id` | str | 9 | 개체 | `package.aliases` | kind=comparison. R13 고민 사전 일치만 |
| 4 | `comparisons[].title` | str | 9 | 개체 | `package.name` |  |
| 5 | `comparisons[].subtitle` | str | 9 | 개체 | `package.subtitle` |  |
| 6 | `comparisons[].evidence_notes[]` | str | 11 | 개체 | `package.evidence_notes` |  |
| 7 | `comparisons[].procedures[].name` | str | 39 | 엣지 | `R12.target_label` | 사전 일치만 (질문 11) |
| 8 | `comparisons[].procedures[].category` | str | 39 | 엣지 | `R12.modality_code` |  |
| 9 | `comparisons[].procedures[].mechanism_simple` | str | 39 | 엣지 | `R12.mechanism_simple` |  |
| 10 | `comparisons[].procedures[].pain` | str | 39 | 엣지 | `R12.pain` | 사전 pain_scale |
| 11 | `comparisons[].procedures[].downtime` | str | 39 | 엣지 | `R12.downtime` |  |
| 12 | `comparisons[].procedures[].onset` | str | 39 | 엣지 | `R12.onset` |  |
| 13 | `comparisons[].procedures[].duration` | str | 39 | 엣지 | `R12.duration` |  |
| 14 | `comparisons[].procedures[].cost_range` | str | 39 | 엣지 | `R12.cost_range` |  |
| 15 | `comparisons[].procedures[].best_for` | str | 39 | 엣지 | `R12.best_for` |  |
| 16 | `comparisons[].procedures[].limitations` | str | 39 | 엣지 | `R12.limitations` |  |
| 17 | `comparisons[].procedures[].pih_risk` | str | 39 | 엣지 | `R12.pih_risk` | 사전 pih_risk_level (`none` 포함) |
| 18 | `comparisons[].procedures[].asian_skin_note` | str | 2 | 엣지 | `R12.asian_skin_note` |  |

## `procedure-profiles.json` — 잎 키 27

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `profiles[].id` | str | 17 | 개체 | `modality(소속)` |  |
| 5 | `profiles[].name` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 6 | `profiles[].name_en` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어(en) |
| 7 | `profiles[].phase` | str | 17 | 개체 | `modality.floor_phase` | 사전 floor_phase |
| 8 | `profiles[].phaseOrder` | int | 17 | 개체 | `modality.floor_phase_order` | 중복 원문 보존 (질문 21) |
| 9 | `profiles[].mechanism[]` | str | 25 | 사전 | `dict:technique` | R5 |
| 10 | `profiles[].hasProtein` | bool | 17 | 개체 | `modality.flags.hasProtein` |  |
| 11 | `profiles[].hasHA` | bool | 17 | 개체 | `modality.flags.hasHA` |  |
| 12 | `profiles[].usesGel` | bool | 17 | 개체 | `modality.flags.usesGel` |  |
| 13 | `profiles[].createsWound` | bool | 17 | 개체 | `modality.flags.createsWound` |  |
| 14 | `profiles[].createsChannel` | bool | 17 | 개체 | `modality.flags.createsChannel` |  |
| 15 | `profiles[].thermalLoad` | int | 17 | 개체 | `modality.risk_scores.thermalLoad` |  |
| 16 | `profiles[].bleedingRisk` | int | 17 | 개체 | `modality.risk_scores.bleedingRisk` |  |
| 17 | `profiles[].swellingRisk` | int | 17 | 개체 | `modality.risk_scores.swellingRisk` |  |
| 18 | `profiles[].needsAnesthesia` | str | 17 | 개체 | `modality.anesthesia` | 사전 anesthesia |
| 19 | `profiles[].position` | str | 17 | 개체 | `modality.position` | 사전 position |
| 20 | `profiles[].needsCleansing` | bool | 17 | 개체 | `modality.flags.needsCleansing` |  |
| 21 | `profiles[].prepTime` | int | 17 | 개체 | `modality.prep_time_min` |  |
| 22 | `profiles[].prepNotes` | str | 17 | 개체 | `modality.prep_notes` |  |
| 23 | `profiles[].durationMin` | int | 17 | 개체 | `modality.duration_min` |  |
| 24 | `profiles[].durationMax` | int | 17 | 개체 | `modality.duration_max` |  |
| 25 | `profiles[].moa_summary` | str | 17 | 개체 | `modality.moa_summary` |  |
| 26 | `profiles[].practicalNotes[]` | str | 64 | 개체 | `modality.practical_notes` |  |
| 27 | `profiles[].aftercare[]` | str | 64 | 개체 | `modality.aftercare` | 출처=procedure-profiles |

## `products.json` — 잎 키 61

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `botulinum_toxin.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `botulinum_toxin` 는 계열 alias |
| 5 | `botulinum_toxin.products[].name` | str | 11 | 개체 | `product.name` |  |
| 6 | `botulinum_toxin.products[].name_en` | str | 11 | 개체 | `product.name_en` |  |
| 7 | `botulinum_toxin.products[].manufacturer` | str | 11 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 8 | `botulinum_toxin.products[].country` | str | 11 | 사전 | `dict:country` | product.country. `-` = null |
| 9 | `botulinum_toxin.products[].mfds` | bool | 11 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 10 | `botulinum_toxin.products[].note` | str | 1 | 개체 | `product.note` |  |
| 11 | `filler_ha.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `filler_ha` 는 계열 alias |
| 12 | `filler_ha.products[].name` | str | 7 | 개체 | `product.name` |  |
| 13 | `filler_ha.products[].name_en` | str | 7 | 개체 | `product.name_en` |  |
| 14 | `filler_ha.products[].manufacturer` | str | 7 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 15 | `filler_ha.products[].country` | str | 7 | 사전 | `dict:country` | product.country. `-` = null |
| 16 | `filler_ha.products[].mfds` | bool | 7 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 17 | `biostimulator.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `biostimulator` 는 계열 alias |
| 18 | `biostimulator.products[].name` | str | 6 | 개체 | `product.name` |  |
| 19 | `biostimulator.products[].name_en` | str | 6 | 개체 | `product.name_en` |  |
| 20 | `biostimulator.products[].manufacturer` | str | 6 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 21 | `biostimulator.products[].country` | str | 6 | 사전 | `dict:country` | product.country. `-` = null |
| 22 | `biostimulator.products[].mfds` | bool | 6 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 23 | `biostimulator.products[].ingredient` | str | 6 | 사전 | `dict:ingredient_material` | product.ingredient_material |
| 24 | `skin_booster.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `skin_booster` 는 계열 alias |
| 25 | `skin_booster.products[].name` | str | 5 | 개체 | `product.name` |  |
| 26 | `skin_booster.products[].name_en` | str | 5 | 개체 | `product.name_en` |  |
| 27 | `skin_booster.products[].manufacturer` | str | 5 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 28 | `skin_booster.products[].country` | str | 5 | 사전 | `dict:country` | product.country. `-` = null |
| 29 | `skin_booster.products[].mfds` | bool | 5 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 30 | `skin_booster.products[].ingredient` | str | 3 | 사전 | `dict:ingredient_material` |  |
| 31 | `skin_booster.products[].note` | str | 2 | 개체 | `product.note` | 스킨보톡스 → not_separate_product (질문 18) |
| 32 | `thread_lift.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `thread_lift` 는 계열 alias |
| 33 | `thread_lift.products[].name` | str | 5 | 개체 | `product.name` |  |
| 34 | `thread_lift.products[].name_en` | str | 5 | 개체 | `product.name_en` |  |
| 35 | `thread_lift.products[].manufacturer` | str | 5 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 36 | `thread_lift.products[].country` | str | 5 | 사전 | `dict:country` | product.country. `-` = null |
| 37 | `thread_lift.products[].mfds` | bool | 5 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 38 | `thread_lift.products[].material` | str | 5 | 사전 | `dict:ingredient_material` |  |
| 39 | `energy_device.category_id[]` | str | 3 | 엣지 | `R4.from(modality)` | [M8,M9,M11] 집합 — 제품별 계열은 taxonomy 소속으로 |
| 40 | `energy_device.products[].name` | str | 18 | 개체 | `product.name` |  |
| 41 | `energy_device.products[].name_en` | str | 18 | 개체 | `product.name_en` |  |
| 42 | `energy_device.products[].manufacturer` | str | 18 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 43 | `energy_device.products[].country` | str | 18 | 사전 | `dict:country` | product.country. `-` = null |
| 44 | `energy_device.products[].type` | str | 18 | 사전 | `dict:product_type` | 기법 사전 후보이기도 함 → R5 |
| 45 | `prp_exosome.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `prp_exosome` 는 계열 alias |
| 46 | `prp_exosome.products[].name` | str | 5 | 개체 | `product.name` |  |
| 47 | `prp_exosome.products[].name_en` | str | 5 | 개체 | `product.name_en` |  |
| 48 | `prp_exosome.products[].manufacturer` | str | 5 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 49 | `prp_exosome.products[].country` | str | 5 | 사전 | `dict:country` | product.country. `-` = null |
| 50 | `prp_exosome.products[].mfds` | bool | 5 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 51 | `prp_exosome.products[].type` | str | 5 | 사전 | `dict:product_type` |  |
| 52 | `prp_exosome.products[].note` | str | 2 | 개체 | `product.note` |  |
| 53 | `prp_exosome.products[].legal_warning` | str | 2 | 개체 | `product.legal_warning` |  |
| 54 | `prp_exosome.products[].regulatory_status` | str | 2 | 개체 | `product.regulatory_status` |  |
| 55 | `stem_cell.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `stem_cell` 는 계열 alias |
| 56 | `stem_cell.products[].name` | str | 2 | 개체 | `product.name` |  |
| 57 | `stem_cell.products[].name_en` | str | 2 | 개체 | `product.name_en` |  |
| 58 | `stem_cell.products[].manufacturer` | str | 2 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 59 | `stem_cell.products[].country` | str | 2 | 사전 | `dict:country` | product.country. `-` = null |
| 60 | `stem_cell.products[].mfds` | bool | 2 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 61 | `stem_cell.products[].type` | str | 2 | 사전 | `dict:product_type` |  |

## `synergy.json` — 잎 키 10

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` |  |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` |  |
| 3 | `links[].from` | str | 115 | 엣지 | `R18.from_label` | `M코드-이름` 분해 ③ → 계열 확정, 이름은 사전 일치만 (질문 8) |
| 4 | `links[].from_category` | str | 115 | 엣지 | `R18.from_modality` |  |
| 5 | `links[].to` | str | 115 | 엣지 | `R18.to_label` |  |
| 6 | `links[].to_category` | str | 115 | 엣지 | `R18.to_modality` |  |
| 7 | `links[].type` | str | 115 | 사전 | `dict:synergy_type` | R18.kind 매핑(함께→synergy_together …) |
| 8 | `links[].reason` | str | 115 | 엣지 | `R18.reason` |  |
| 9 | `links[].timing` | str | 115 | 엣지 | `R18.timing` |  |
| 10 | `links[].target` | str | 115 | 사전 | `dict:purpose_label` | R18.target |

## `taxonomy.json` — 잎 키 87

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `modality[].id` | str | 17 | 개체 | `modality.code` | 정본 (질문 1) |
| 2 | `modality[].category` | str | 17 | 개체 | `modality.name` | 정본 한글명 = 사전 modality 정준값 |
| 3 | `modality[].category_en` | str | 17 | 개체 | `modality.name_en` | 사전 동의어(en) |
| 4 | `modality[].group` | str | 17 | 사전 | `dict:modality_group` | modality.group |
| 5 | `modality[].subcategories[].id` | str | 74 | 개체 | `modality_subcategory.code` | + aliases |
| 6 | `modality[].subcategories[].label` | str | 74 | 개체 | `modality_subcategory.label` | 기법 사전 후보 → R5 |
| 7 | `modality[].subcategories[].items[].id` | str | 521 | 개체 | `procedure.aliases` | 질문 4 |
| 8 | `modality[].subcategories[].items[].name` | str | 521 | 개체 | `procedure.name` | R3 제품 일치 |
| 9 | `modality[].subcategories[].items[].detail` | str | 521 | 개체 | `procedure.detail` | 빈 문자열 20 = null |
| 10 | `modality[].subcategories[].items[].extracted.overview` | str | 521 | 개체 | `procedure.overview` |  |
| 11 | `modality[].subcategories[].items[].extracted.mechanism` | str | 521 | 개체 | `procedure.mechanism` |  |
| 12 | `modality[].subcategories[].items[].extracted.indications.primary[]` | str | 1656 | 개체 | `procedure.indications_primary` |  |
| 13 | `modality[].subcategories[].items[].extracted.indications.extended[]` | str | 10 | 개체 | `procedure.indications_extended` |  |
| 14 | `modality[].subcategories[].items[].extracted.safety.common[]` | str | 1278 | 개체 | `adverse_effect.name` | R15.frequency_class=common |
| 15 | `modality[].subcategories[].items[].extracted.safety.serious[]` | str | 422 | 개체 | `adverse_effect.name` | R15.frequency_class=serious |
| 16 | `modality[].subcategories[].items[].extracted.onset_duration.onset` | str | 520 | 개체 | `procedure.onset` |  |
| 17 | `modality[].subcategories[].items[].extracted.onset_duration.duration` | str | 521 | 개체 | `procedure.duration` |  |
| 18 | `modality[].subcategories[].items[].extracted.aftercare[]` | str | 1914 | 개체 | `procedure.aftercare` |  |
| 19 | `modality[].subcategories[].items[].extracted.safety.note` | str | 4 | 개체 | `procedure.safety_note` |  |
| 20 | `modality[].subcategories[].items[].extracted.onset_duration.peak` | str | 7 | 개체 | `procedure.peak` |  |
| 21 | `modality[].subcategories[].items[].extracted.onset_duration.peak_effect` | str | 8 | 개체 | `procedure.peak` | 동의 키 ③ |
| 22 | `modality[].subcategories[].items[].extracted.indications.secondary[]` | str | 18 | 개체 | `procedure.indications_extended` | 동의 키 ③ (질문 20) |
| 23 | `modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]` | str | 6 | 개체 | `adverse_effect.name` | 동의 키 → common |
| 24 | `modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]` | str | 6 | 개체 | `adverse_effect.name` | 동의 키 → serious |
| 25 | `modality[].subcategories[].items[].extracted.safety.contraindications[]` | str | 11 | 개체 | `person_condition.name` | R16 (level=unspecified) |
| 26 | `modality[].subcategories[].items[].verification_needed` | str | 1 | 개체 | `decision.what` | kind=verification_hold (질문 23) |
| 27 | `modality[].subcategories[].items[].extracted.safety.long_term[]` | str | 1 | 개체 | `adverse_effect.name` | R15.frequency_class=long_term |
| 28 | `modality[].subcategories[].items[].extracted.onset_duration.maintenance` | str | 1 | 개체 | `procedure.maintenance` |  |
| 29 | `modality[].extracted.overview` | str | 17 | 개체 | `modality.overview` | 출처=taxonomy (질문 2) |
| 30 | `modality[].extracted.mechanism` | str | 17 | 개체 | `modality.mechanism` |  |
| 31 | `modality[].extracted.indications.primary[]` | str | 56 | 개체 | `modality.indications_primary` |  |
| 32 | `modality[].extracted.indications.extended[]` | str | 100 | 개체 | `modality.indications_extended` |  |
| 33 | `modality[].extracted.contraindications.absolute[]` | str | 53 | 개체 | `person_condition.name` | R16.level=absolute |
| 34 | `modality[].extracted.contraindications.relative[]` | str | 55 | 개체 | `person_condition.name` | R16.level=relative |
| 35 | `modality[].extracted.safety.common[]` | str | 59 | 개체 | `adverse_effect.name` | R15 common |
| 36 | `modality[].extracted.safety.uncommon[]` | str | 45 | 개체 | `adverse_effect.name` | R15 uncommon |
| 37 | `modality[].extracted.safety.serious[]` | str | 37 | 개체 | `adverse_effect.name` | R15 serious |
| 38 | `modality[].extracted.onset_duration.onset` | str | 17 | 개체 | `modality.onset` |  |
| 39 | `modality[].extracted.onset_duration.peak` | str | 17 | 개체 | `modality.peak` |  |
| 40 | `modality[].extracted.onset_duration.duration` | str | 17 | 개체 | `modality.duration` |  |
| 41 | `modality[].extracted.aftercare[]` | str | 53 | 개체 | `modality.aftercare` |  |
| 42 | `modality[].extracted.related_techniques[]` | str | 51 | 개체 | `modality.related_techniques` |  |
| 43 | `modality[].products[].id` | str | 59 | 개체 | `product.aliases` | M1-P-0 형 → R4 소속 |
| 44 | `modality[].products[].name` | str | 59 | 개체 | `product.name` | products.json 과 병합 (질문 3) |
| 45 | `modality[].products[].name_en` | str | 59 | 개체 | `product.name_en` |  |
| 46 | `modality[].products[].manufacturer` | str | 59 | 사전 | `dict:manufacturer` |  |
| 47 | `modality[].products[].country` | str | 59 | 사전 | `dict:country` |  |
| 48 | `modality[].products[].mfds` | bool/null | 59 | 개체 | `product.mfds` | null 17 = 미입력 (질문 16) |
| 49 | `modality[].products[].extracted.overview` | str | 59 | 개체 | `product.overview` |  |
| 50 | `modality[].products[].extracted.mechanism` | str | 59 | 개체 | `product.mechanism` |  |
| 51 | `modality[].products[].extracted.indications.primary[]` | str | 256 | 개체 | `product.indications_primary` |  |
| 52 | `modality[].products[].extracted.safety.common[]` | str | 222 | 개체 | `adverse_effect.name` | R15 (product) common |
| 53 | `modality[].products[].extracted.safety.note` | str | 1 | 개체 | `product.safety_note` |  |
| 54 | `modality[].products[].extracted.onset_duration.onset` | str | 59 | 개체 | `product.onset` |  |
| 55 | `modality[].products[].extracted.onset_duration.duration` | str | 59 | 개체 | `product.duration` |  |
| 56 | `modality[].products[].extracted.aftercare[]` | str | 238 | 개체 | `product.aftercare` |  |
| 57 | `modality[].products[].extracted.onset_duration.peak_effect` | str | 5 | 개체 | `product.peak` | 동의 키 ③ |
| 58 | `modality[].products[].extracted.onset_duration.diffusion` | str | 1 | 개체 | `product.diffusion` |  |
| 59 | `modality[].products[].note` | str | 5 | 개체 | `product.note` |  |
| 60 | `modality[].name` | str | 17 | 버림 | `drop` | 17/17 `category` 와 같은 값 — 중복 키 |
| 61 | `modality[].products[].extracted.indications.secondary[]` | str | 14 | 개체 | `product.indications_extended` | 동의 키 ③ |
| 62 | `modality[].products[].extracted.safety.serious[]` | str | 62 | 개체 | `adverse_effect.name` | R15 (product) serious |
| 63 | `modality[].subcategories[].description` | str | 3 | 개체 | `modality_subcategory.description` |  |
| 64 | `modality[].products[].ingredient` | str | 9 | 사전 | `dict:ingredient_material` |  |
| 65 | `modality[].subcategories[].items[].classification_issue` | str | 2 | 개체 | `decision.what` | kind=ledger_correction_note |
| 66 | `modality[].subcategories[].items[].is_marketing_name` | bool | 6 | 개체 | `procedure.is_marketing_name` |  |
| 67 | `modality[].subcategories[].items[].ingredient_basis` | str | 6 | 개체 | `procedure.ingredient_basis` |  |
| 68 | `modality[].subcategories[].items[].canonical_category` | str | 6 | 개체 | `decision.new_value` | kind=canonical_mapping (하위분류 사전 일치만) |
| 69 | `modality[].subcategories[].items[].naming_caveat` | str | 6 | 개체 | `procedure.naming_caveat` |  |
| 70 | `modality[].products[].type` | str | 24 | 사전 | `dict:product_type` |  |
| 71 | `modality[].products` | list(empty) | 7 | 개체 | `modality.products_present` | 빈 배열 7 = null (질문 15) |
| 72 | `modality[].products[].material` | str | 5 | 사전 | `dict:ingredient_material` |  |
| 73 | `modality[].products[].extracted.safety.common_side_effects[]` | str | 4 | 개체 | `adverse_effect.name` | 동의 키 → common |
| 74 | `modality[].products[].extracted.safety.contraindications[]` | str | 1 | 개체 | `product.contraindication_notes` | 병합 금기 문장 |
| 75 | `modality[].subcategories[].items[].correction_note` | str | 1 | 개체 | `decision.what` | kind=ledger_correction_note |
| 76 | `modality[].subcategories[].items[].reclassified_to` | str | 1 | 개체 | `decision.new_value` | kind=reclassification → R2 재배치 |
| 77 | `modality[].subcategories[].items` | list(empty) | 2 | 개체 | `modality_subcategory.items_present` | 빈 배열 2 = null |
| 78 | `problem[].id` | str | 14 | 개체 | `problem.code` | 정본 (질문 12) |
| 79 | `problem[].category` | str | 14 | 개체 | `problem.name` | = 사전 problem 정준값 |
| 80 | `problem[].category_en` | str | 14 | 개체 | `problem.name_en` |  |
| 81 | `problem[].subcategories[].id` | str | 53 | 개체 | `problem_subcategory.code` |  |
| 82 | `problem[].subcategories[].label` | str | 53 | 개체 | `problem_subcategory.label` | 부위 사전 동의어 원천 (질문 24) → R11 |
| 83 | `problem[].subcategories[].items[].id` | str | 117 | 개체 | `complaint.aliases` |  |
| 84 | `problem[].subcategories[].items[].name` | str | 117 | 개체 | `complaint.name` |  |
| 85 | `problem[].subcategories[].items[].detail` | str | 117 | 개체 | `complaint.detail` |  |
| 86 | `problem[].subcategories[].items[].modality_ref[]` | str | 105 | 엣지 | `R8.to(modality)` |  |
| 87 | `problem[].subcategories[].items[].modality_ref` | list(empty) | 26 | 엣지 | `R8(none)` | 빈 배열 26 = null → 질문 14 두 묶음 |

## `treatment-optimization.json` — 잎 키 36

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` |  |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` |  |
| 3 | `consensus_method` | str | 1 | 개체 | `source_file.method` | 신뢰 4 근거 |
| 4 | `optimization_principles[]` | str | 4 | 개체 | `clinical_rule.text` | kind=principle |
| 5 | `by_concern[].concern` | str | 8 | 엣지 | `R13.problem_label` | 고민 사전 일치만 (질문 12) |
| 6 | `by_concern[].concern_en` | str | 8 | 사전 | `dict:problem` | 후보(en) — 자동 동의어 아님 |
| 7 | `by_concern[].icon` | str | 8 | 사전 | `dict:purpose_label` |  |
| 8 | `by_concern[].severity_levels[].level` | str | 24 | 엣지 | `R13.severity` | `경미 (설명)` 분해 ③ → 사전 concern_severity + severity_detail |
| 9 | `by_concern[].severity_levels[].optimal_combo[]` | str | 74 | 엣지 | `R12.target_label` | kind=optimization_plan. 사전 일치만 |
| 10 | `by_concern[].severity_levels[].sequence` | str | 24 | 개체 | `package.sequence_text` |  |
| 11 | `by_concern[].severity_levels[].rationale` | str | 24 | 개체 | `package.clinical_rationale` |  |
| 12 | `by_concern[].severity_levels[].expected_sessions` | str | 24 | 개체 | `package.expected_sessions` |  |
| 13 | `by_concern[].severity_levels[].total_duration` | str | 24 | 개체 | `package.total_duration` |  |
| 14 | `by_concern[].severity_levels[].evidence_level` | str | 24 | 개체 | `package.evidence_level` | 사전 evidence_level |
| 15 | `by_concern[].severity_levels[].contraindicated_combos` | list(empty) | 11 | 개체 | `package.contraindicated_combos` | 빈 배열 11 = null |
| 16 | `by_concern[].severity_levels[].contraindicated_combos[]` | str | 17 | 개체 | `package.contraindicated_combos` | R18 변환은 사전 일치만 |
| 17 | `by_concern[].severity_levels[].caveats[]` | str | 2 | 개체 | `package.caveats` |  |
| 18 | `by_age_group[].age` | str | 4 | 개체 | `person_condition.name` | kind=age_group, 사전 age_group |
| 19 | `by_age_group[].primary_concerns[]` | str | 17 | 엣지 | `R17.target_label` | relation_kind=primary_concern → 고민 사전 일치만 |
| 20 | `by_age_group[].recommended_base[]` | str | 17 | 엣지 | `R17.target_label` | recommended_base |
| 21 | `by_age_group[].avoid[]` | str | 6 | 엣지 | `R17.target_label` | avoid |
| 22 | `by_age_group[].maintenance` | str | 4 | 개체 | `person_condition.maintenance` |  |
| 23 | `by_age_group[].annual_focus` | str | 4 | 개체 | `person_condition.annual_focus` |  |
| 24 | `by_age_group[].upgrade[]` | str | 5 | 엣지 | `R17.target_label` | upgrade |
| 25 | `by_age_group[].note` | str | 1 | 개체 | `person_condition.note` |  |
| 26 | `combination_rules[].rule` | str | 8 | 개체 | `clinical_rule.text` | kind=combination_rule |
| 27 | `combination_rules[].detail` | str | 8 | 개체 | `clinical_rule.detail` |  |
| 28 | `combination_rules[].evidence` | str | 8 | 개체 | `citation.text` | kind=guideline_text → R19 |
| 29 | `combination_rules[].consensus` | str | 8 | 사전 | `dict:consensus` | clinical_rule.consensus |
| 30 | `combination_rules[].priority` | str | 8 | 사전 | `dict:rule_priority` | clinical_rule.priority |
| 31 | `annual_plans[].plan_name` | str | 3 | 개체 | `package.name` | kind=annual_plan |
| 32 | `annual_plans[].age_group` | str | 3 | 사전 | `dict:age_group` | package.age_group |
| 33 | `annual_plans[].annual_budget_range` | str | 3 | 개체 | `package.price_range` |  |
| 34 | `annual_plans[].focus` | str | 3 | 개체 | `package.focus` |  |
| 35 | `annual_plans[].schedule[].month` | int | 36 | 엣지 | `R12.month` |  |
| 36 | `annual_plans[].schedule[].procedures[]` | str | 77 | 엣지 | `R12.target_label` | `토닝 4회` 횟수 섞임 — 사전 일치만 |

## `treatment-sequence.json` — 잎 키 20

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `principles[]` | str | 13 | 개체 | `clinical_rule.text` | kind=principle |
| 5 | `sequence_order[].order` | int | 11 | 개체 | `modality.same_session_order.order` | categories[] 끝에 |
| 6 | `sequence_order[].phase` | str | 11 | 사전 | `dict:session_phase` | modality.same_session_order.phase |
| 7 | `sequence_order[].categories[]` | str | 19 | 개체 | `modality.same_session_order(소속)` | 코드/코드+라벨/라벨 세 형식 (질문 7) — 미해결은 ⑨ |
| 8 | `sequence_order[].reason` | str | 11 | 개체 | `modality.same_session_order.reason` |  |
| 9 | `incompatible_same_day[].pair[]` | str | 17 | 엣지 | `R18.from_label/to_label` | kind=incompatible_same_day. 사전 일치만 |
| 10 | `incompatible_same_day[].reason` | str | 9 | 엣지 | `R18.reason` |  |
| 11 | `common_combos[].name` | str | 8 | 개체 | `package.name` | kind=session_combo |
| 12 | `common_combos[].sequence[]` | str | 26 | 엣지 | `R12.target_label` | order = 배열 순서 |
| 13 | `common_combos[].total_time` | str | 8 | 개체 | `package.total_duration` |  |
| 14 | `common_combos[].note` | str | 3 | 개체 | `package.note` |  |
| 15 | `minimum_intervals[].from` | str | 9 | 엣지 | `R18.from_label` | kind=minimum_interval. 사람 조건(이소트레티노인)도 from 가능 |
| 16 | `minimum_intervals[].to` | str | 9 | 엣지 | `R18.to_label` |  |
| 17 | `minimum_intervals[].min_days` | int | 7 | 엣지 | `R18.min_interval_value` | unit=day (질문 22) |
| 18 | `minimum_intervals[].source` | str | 9 | 개체 | `citation.text` | kind=guideline_text → R18.source_ref |
| 19 | `minimum_intervals[].reason` | str | 9 | 엣지 | `R18.reason` |  |
| 20 | `minimum_intervals[].min_months` | int | 2 | 엣지 | `R18.min_interval_value` | unit=month |
## 검산 결과

### A. 잎 키 행선지

- PASS — 행선지 행 573 = 스캔 잎 키 573 = 573
- PASS — 중복 행 0
- PASS — 스캔에만 0 · 표에만 0
- PASS — 행선지 범주 밖/표적 없음(미정) 0
- 행선지 분포: 개체 378 · 엣지 107 · 사전 75 · 브론즈 12 · 버림 1 (합 573)
- PASS — 표적이 ERD 에 정의되지 않은 행 0

### B. 사전 값 출처

- PASS — 출처 없는 사전 값 0 / 정준값 465 + 동의어 200
- PASS — 원장에서 확인 안 되는 출처 0
- 사전 36개 · 정준값 465 · 동의어 200 · 후보 37 · 출처 100% 확인

### C. ERD 출처 키·표적

- PASS — ERD 출처 키 426개 중 스캔 잎 키에 없는 것 0
- PASS — 행선지 표의 사전 23개 전부 사전 파일에 있음
- 개체 19 · 관계 25 · 사전 36 · 재검토 19

### D. 브론즈 바이트

- PASS — 원장 21 sha256 일치 (불일치 0)

**종합: PASS** — 잎 키 573/573 행선지 확정(미정 0) · 사전 값 출처 100% · ERD 출처 키 100% · 브론즈 sha256 일치
