# ERD v3.1 — 잎 키 행선지 표 (원장 21 · 브론즈 2판 + step1-products.json)

**v3 와 행선지·표적이 다른 행은 29 개다** — V3.1-7 consent mandatory_disclosures 1(modality 속성 → clinical_rule.text) + V3.1-10 표현 관련 28(개체 adverse_expression.* → 사전 dict:phrase_dictionary). 비고만 바뀐 행 36(아래 「비고 변경 v3 → v3.1」 — V3.1-4 조건 사전 출처·단위 식별 · V3.1-2 제품 note 후보 · V3.1-5 회·차 자리 · V3.1-9 단위 세 칸·경과 엣지 · V3.1-6 겹침). 그 밖 행선지·표적·비고는 v3 과 같다(검산 A 행 단위 대조). 규칙 `erd_colmap_v31.py`.

브론즈 2판 잎 키 재스캔: 원장 21 잎 키 573 = 1판 573 · 파일별 집합 차이 0.

작성 2026-11-05 · 입력 `bronze-ledger-column-scan.json`(원장 잎 키 573) + `step1-products.json` 잎 키 499 = 1072 · 행선지 범주 5: 개체 / 사전 / 엣지 / 브론즈 / 버림 · **미정 0**

표적 표기: `entity.attr` · `dict:<사전>` · `R#.attr`(관계 번호는 erd-v3.1.md §3) · `bronze` · `drop`. v1.1 과 달라진 행 47 + v2.2 3 + v2.3 0 + v2.4 0 + v3 0 + v3.1 29.

## 이동 표 (v3 → v3.1)

| # | 파일 | 경로 | v3 | v3.1 |
|---|---|---|---|---|
| 1 | `consent-checklist.json` | `categories[].mandatory_disclosures[]` | `개체:modality.mandatory_disclosures` | `개체:clinical_rule.text` |
| 2 | `consent-checklist.json` | `categories[].emergency_signs[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 3 | `extracted.json` | `{code}.safety.common[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 4 | `extracted.json` | `{code}.safety.uncommon[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 5 | `extracted.json` | `{code}.safety.serious[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 6 | `extracted.json` | `{code}.safety.emergency[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 7 | `literature-evidence.json` | `categories.{code}.adverse_effects[].statement` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 8 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_ko` | `개체:adverse_expression.patient_text` | `사전:dict:phrase_dictionary` |
| 9 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_en` | `개체:adverse_expression.patient_text` | `사전:dict:phrase_dictionary` |
| 10 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_zh` | `개체:adverse_expression.patient_text` | `사전:dict:phrase_dictionary` |
| 11 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_ja` | `개체:adverse_expression.patient_text` | `사전:dict:phrase_dictionary` |
| 12 | `literature-evidence.json` | `categories.{code}.adverse_effects[].accuracy_score` | `개체:adverse_expression.accuracy_score` | `사전:dict:phrase_dictionary` |
| 13 | `literature-evidence.json` | `categories.{code}.adverse_effects[].accuracy_note` | `개체:adverse_expression.accuracy_note` | `사전:dict:phrase_dictionary` |
| 14 | `literature-evidence.json` | `categories.{code}.adverse_effects[].added_at` | `개체:adverse_expression.added_at` | `사전:dict:phrase_dictionary` |
| 15 | `post-procedure-timeline.json` | `timelines[].phases[].normal[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 16 | `post-procedure-timeline.json` | `timelines[].phases[].abnormal[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 17 | `post-procedure-timeline.json` | `timelines[].phases[].caution[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 18 | `post-procedure-timeline.json` | `timelines[].phases[].emergency[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 19 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.common[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 20 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.serious[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 21 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 22 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 23 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.long_term[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 24 | `taxonomy.json` | `modality[].extracted.safety.common[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 25 | `taxonomy.json` | `modality[].extracted.safety.uncommon[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 26 | `taxonomy.json` | `modality[].extracted.safety.serious[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 27 | `taxonomy.json` | `modality[].products[].extracted.safety.common[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 28 | `taxonomy.json` | `modality[].products[].extracted.safety.serious[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |
| 29 | `taxonomy.json` | `modality[].products[].extracted.safety.common_side_effects[]` | `개체:adverse_expression.text` | `사전:dict:phrase_dictionary` |

## 비고 변경 (v3 → v3.1 · 표적 동일)

| # | 파일 | 경로 | 표적 | 추가된 비고 |
|---|---|---|---|---|
| 1 | `consent-checklist.json` | `categories[].contraindications[]` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 2 | `extracted.json` | `{code}.contraindications.absolute[]` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 3 | `extracted.json` | `{code}.contraindications.relative[]` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 4 | `taxonomy.json` | `modality[].extracted.contraindications.absolute[]` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 5 | `taxonomy.json` | `modality[].extracted.contraindications.relative[]` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 6 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.contraindications[]` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 7 | `pre-procedure-checklist.json` | `universal_checks[].label` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=check) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 8 | `pre-procedure-checklist.json` | `category_specific[].checks[].label` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=check) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 9 | `treatment-optimization.json` | `by_age_group[].age` | `person_condition.name` | v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=age_group) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 10 | `consent-checklist.json` | `categories[].id` | `R16.from(modality)` | v3.1(V3.1-4): R16 끝은 조건 단위(CND- · 사전 정준값+kind) · v3.1(V3.1-7): R32(basis=ledger) from 계열 |
| 11 | `pre-procedure-checklist.json` | `category_specific[].id` | `R16.from(modality)` | v3.1(V3.1-4): R16 끝은 조건 단위(CND-) |
| 12 | `products.json` | `prp_exosome.products[].legal_warning` | `product.legal_warning` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보 — 규칙 문장이면 edge_create(R32 rule_applies_to · from_ref locator)가 레코드와 엣지를 세운다(값 자동 생성 없음 · 실측 §9.7.2) |
| 13 | `products.json` | `prp_exosome.products[].regulatory_status` | `product.regulatory_status` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보 — 규칙 문장이면 edge_create(R32 rule_applies_to · from_ref locator)가 레코드와 엣지를 세운다(값 자동 생성 없음 · 실측 §9.7.2) |
| 14 | `taxonomy.json` | `modality[].products[].note` | `product.note` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보 — 규칙 문장이면 edge_create(R32 rule_applies_to · from_ref locator)가 레코드와 엣지를 세운다(값 자동 생성 없음 · 실측 §9.7.2) |
| 15 | `products.json` | `botulinum_toxin.products[].note` | `product.note` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보(「화장품 허가. 주사/주입 사용 금지」 류) — R32 는 edge_create 로만 · 실측 §9.7.2 |
| 16 | `products.json` | `skin_booster.products[].note` | `product.note` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보(「화장품 허가. 주사/주입 사용 금지」 류) — R32 는 edge_create 로만 · 실측 §9.7.2 |
| 17 | `products.json` | `prp_exosome.products[].note` | `product.note` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보(「화장품 허가. 주사/주입 사용 금지」 류) — R32 는 edge_create 로만 · 실측 §9.7.2 |
| 18 | `treatment-optimization.json` | `annual_plans[].schedule[].procedures[]` | `R12.target_label` | v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
| 19 | `treatment-optimization.json` | `by_concern[].severity_levels[].optimal_combo[]` | `R12.target_label` | v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
| 20 | `treatment-sequence.json` | `common_combos[].sequence[]` | `R12.target_label` | v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
| 21 | `procedure-comparison.json` | `comparisons[].procedures[].name` | `R12.target_label` | v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
| 22 | `problem-packages.json` | `problems[].complaints[].combos[].combo[]` | `R12.target_label` | v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
| 23 | `problem-packages.json` | `problems[].complaints[].procedures[].name` | `R9.target_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 24 | `treatment-optimization.json` | `by_age_group[].recommended_base[]` | `R17.target_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 25 | `treatment-optimization.json` | `by_age_group[].avoid[]` | `R17.target_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 26 | `treatment-optimization.json` | `by_age_group[].upgrade[]` | `R17.target_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 27 | `synergy.json` | `links[].from` | `R18.from_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 28 | `synergy.json` | `links[].to` | `R18.to_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 29 | `treatment-sequence.json` | `incompatible_same_day[].pair[]` | `R18.from_label/to_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 30 | `treatment-sequence.json` | `minimum_intervals[].from` | `R18.from_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 31 | `treatment-sequence.json` | `minimum_intervals[].to` | `R18.to_label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 32 | `market-pricing.json` | `categories[].items[].name` | `modality.price_items.label` | v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 33 | `complications.json` | `categories[].complications[].name` | `dict:adverse_event_type` | v3.1(V3.1-9): 단위 = (사건, 부위, 물질) 세 칸 · 상대 부위는 none(relative_site_text 보존) · 이름의 경과 조각은 category → 단위 R15.course · raw_name 은 그대로 |
| 34 | `complications.json` | `categories[].id` | `R15.from(modality)` | v3.1(V3.1-9): R15.course 는 이 category → 단위 엣지의 속성(이름의 경과 조각) · v3.1(V3.1-10): 문구 유래 엣지는 source_phrases 부록 |
| 35 | `literature-evidence.json` | `categories.{code}.adverse_effects[].citations[].pmid` | `citation.pmid` | v3.1(V3.1-10): 문헌 문구의 인용은 문구 사전 항목 citations[](개체 아님) · R19 from 에서 adverse_expression 삭제 |
| 36 | `taxonomy.json` | `modality[].group` | `dict:modality_group` | v3.1(V3.1-6): modality_group 값 「관리」가 stopword 와 겹친다 — 통째 일치가 먼저 · 분해 사전이 아니라 충돌 없음(overlap 목록) |

## 이동 표 (v2.1 → v2.2)

| # | 파일 | 경로 | v2.1 | v2.2 |
|---|---|---|---|---|
| 1 | `taxonomy.json` | `modality[].subcategories[].items[].verification_needed` | `개체:decision.what` | `개체:decision.reason` |
| 2 | `taxonomy.json` | `modality[].subcategories[].items[].classification_issue` | `개체:decision.what` | `개체:decision.reason` |
| 3 | `taxonomy.json` | `modality[].subcategories[].items[].correction_note` | `개체:decision.what` | `개체:decision.reason` |

## 이동 표 (v1.1 → v2)

| # | 파일 | 경로 | v1.1 | v2 |
|---|---|---|---|---|
| 1 | `taxonomy.json` | `modality[].subcategories[].items[].id` | `개체:procedure.aliases` | `개체:catalog_item.aliases` |
| 2 | `taxonomy.json` | `modality[].subcategories[].items[].name` | `개체:procedure.name` | `개체:catalog_item.name` |
| 3 | `taxonomy.json` | `modality[].subcategories[].items[].detail` | `개체:procedure.detail` | `개체:catalog_item.detail` |
| 4 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.overview` | `개체:procedure.overview` | `개체:catalog_item.overview` |
| 5 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.mechanism` | `개체:procedure.mechanism` | `개체:catalog_item.mechanism` |
| 6 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.indications.primary[]` | `개체:procedure.indications_primary` | `개체:catalog_item.indications_primary` |
| 7 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.indications.extended[]` | `개체:procedure.indications_extended` | `개체:catalog_item.indications_extended` |
| 8 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.indications.secondary[]` | `개체:procedure.indications_extended` | `개체:catalog_item.indications_extended` |
| 9 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.note` | `개체:procedure.safety_note` | `개체:catalog_item.safety_note` |
| 10 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.onset_duration.onset` | `개체:procedure.onset` | `개체:catalog_item.onset` |
| 11 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.onset_duration.duration` | `개체:procedure.duration` | `개체:catalog_item.duration` |
| 12 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.onset_duration.peak` | `개체:procedure.peak` | `개체:catalog_item.peak` |
| 13 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.onset_duration.peak_effect` | `개체:procedure.peak` | `개체:catalog_item.peak` |
| 14 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.onset_duration.maintenance` | `개체:procedure.maintenance` | `개체:catalog_item.maintenance` |
| 15 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.aftercare[]` | `개체:procedure.aftercare` | `개체:catalog_item.aftercare` |
| 16 | `taxonomy.json` | `modality[].subcategories[].items[].is_marketing_name` | `개체:procedure.is_marketing_name` | `개체:catalog_item.is_marketing_name` |
| 17 | `taxonomy.json` | `modality[].subcategories[].items[].ingredient_basis` | `개체:procedure.ingredient_basis` | `개체:catalog_item.ingredient_basis` |
| 18 | `taxonomy.json` | `modality[].subcategories[].items[].naming_caveat` | `개체:procedure.naming_caveat` | `개체:catalog_item.naming_caveat` |
| 19 | `complications.json` | `categories[].complications[].name` | `개체:adverse_effect.name` | `사전:dict:adverse_event_type` |
| 20 | `literature-evidence.json` | `categories.{code}.adverse_effects[].statement` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 21 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_ko` | `개체:adverse_effect.patient_text.ko` | `개체:adverse_expression.patient_text` |
| 22 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_en` | `개체:adverse_effect.patient_text.en` | `개체:adverse_expression.patient_text` |
| 23 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_zh` | `개체:adverse_effect.patient_text.zh` | `개체:adverse_expression.patient_text` |
| 24 | `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_ja` | `개체:adverse_effect.patient_text.ja` | `개체:adverse_expression.patient_text` |
| 25 | `literature-evidence.json` | `categories.{code}.adverse_effects[].accuracy_score` | `개체:adverse_effect.accuracy_score` | `개체:adverse_expression.accuracy_score` |
| 26 | `literature-evidence.json` | `categories.{code}.adverse_effects[].accuracy_note` | `개체:adverse_effect.accuracy_note` | `개체:adverse_expression.accuracy_note` |
| 27 | `literature-evidence.json` | `categories.{code}.adverse_effects[].added_at` | `개체:adverse_effect.added_at` | `개체:adverse_expression.added_at` |
| 28 | `consent-checklist.json` | `categories[].emergency_signs[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 29 | `post-procedure-timeline.json` | `timelines[].phases[].normal[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 30 | `post-procedure-timeline.json` | `timelines[].phases[].abnormal[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 31 | `post-procedure-timeline.json` | `timelines[].phases[].caution[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 32 | `post-procedure-timeline.json` | `timelines[].phases[].emergency[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 33 | `extracted.json` | `{code}.safety.common[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 34 | `extracted.json` | `{code}.safety.uncommon[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 35 | `extracted.json` | `{code}.safety.serious[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 36 | `extracted.json` | `{code}.safety.emergency[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 37 | `taxonomy.json` | `modality[].extracted.safety.common[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 38 | `taxonomy.json` | `modality[].extracted.safety.uncommon[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 39 | `taxonomy.json` | `modality[].extracted.safety.serious[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 40 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.common[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 41 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.serious[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 42 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 43 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 44 | `taxonomy.json` | `modality[].subcategories[].items[].extracted.safety.long_term[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 45 | `taxonomy.json` | `modality[].products[].extracted.safety.common[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 46 | `taxonomy.json` | `modality[].products[].extracted.safety.serious[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |
| 47 | `taxonomy.json` | `modality[].products[].extracted.safety.common_side_effects[]` | `개체:adverse_effect.name` | `개체:adverse_expression.text` |

## 요약

| 행선지 | 원장 21 | step1 | 합계 |
|---|---|---|---|
| 개체 | 349 | 139 | 488 |
| 브론즈 | 12 | 353 | 365 |
| 사전 | 104 | 6 | 110 |
| 엣지 | 107 | 1 | 108 |
| 버림 | 1 | 0 | 1 |
| 합계 | 573 | 499 | 1072 |

## `anatomy-danger-zones.json` — 잎 키 67

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `consensus_method` | str | 1 | 개체 | `source_file.method` | 신뢰 순위 4 근거 |
| 4 | `critical_safety_facts.minimum_filler_for_blindness` | str | 1 | 개체 | `clinical_rule.text` | kind=critical_safety_fact, topic=키 이름 |
| 5 | `critical_safety_facts.blindness_highest_risk_zones` | str | 1 | 개체 | `clinical_rule.text` | kind=critical_safety_fact |
| 6 | `critical_safety_facts.mechanism` | str | 1 | 개체 | `clinical_rule.text` | kind=critical_safety_fact · v3(V3-1): 사전 adverse_qualifier 값 출처(derived) |
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
| 17 | `zones[].vessels[].danger` | str | 24 | 엣지 | `R21.danger` | v3(V3-1): 사전 adverse_qualifier 값 출처(derived) · v3(V3-5): 사전 site 조직층(kind=layer) 값 출처(derived) |
| 18 | `zones[].vessels[].note` | str | 2 | 엣지 | `R21.note` |  |
| 19 | `zones[].vessels[].depth_range_mm[]` | float | 10 | 엣지 | `R21.depth_range_mm` | 단일값/범위 두 형태 원문 보존 |
| 20 | `zones[].nerves[].name` | str | 21 | 개체 | `anatomical_structure.name_raw` | kind=nerve |
| 21 | `zones[].nerves[].type` | str | 21 | 개체 | `anatomical_structure.nerve_type` | 사전 nerve_type |
| 22 | `zones[].nerves[].significance` | str | 21 | 엣지 | `R21.significance` |  |
| 23 | `zones[].safe_injection_depth` | str | 11 | 개체 | `site.safe_injection_depth` | v3(V3-5): 사전 site 조직층(kind=layer) 값 출처(derived) |
| 24 | `zones[].tissue_data.frontalis_thickness.midpupil_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 25 | `zones[].tissue_data.frontalis_thickness.lateral_canthus_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 26 | `zones[].tissue_data.frontalis_thickness.lateral_orbital_rim_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 27 | `zones[].tissue_data.skin_to_periosteum_mm` | float | 1 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 |
| 28 | `zones[].tissue_data.notes` | str | 11 | 개체 | `site.tissue_data.*` | 부위별 자유 구조 — 키 이름 보존 · v3(V3-5): 사전 site 조직층(kind=layer) 값 출처(derived) |
| 29 | `zones[].clinical_pearls[]` | str | 61 | 개체 | `site.clinical_pearls` | v3(V3-5): 사전 site 조직층(kind=layer) 값 출처(derived) |
| 30 | `zones[].botox_specific.target_muscle` | str | 11 | 엣지 | `R22.target_muscle` | site→M1 |
| 31 | `zones[].botox_specific.risk` | str | 11 | 엣지 | `R22.risk_text` | site→M1 |
| 32 | `zones[].botox_specific.safe_zone` | str | 11 | 엣지 | `R22.safe_zone` | site→M1 |
| 33 | `zones[].botox_specific.diffusion_range_cm` | str | 1 | 엣지 | `R22.diffusion_range_cm` | site→M1 |
| 34 | `zones[].botox_specific.key_warning` | str | 11 | 엣지 | `R22.key_warning` | site→M1 |
| 35 | `zones[].botox_specific.dose_range` | str | 11 | 엣지 | `R22.dose_range` | site→M1 |
| 36 | `zones[].filler_specific.risk_level` | int | 11 | 엣지 | `R22.risk_level` | site→M2. 사전 danger_level |
| 37 | `zones[].filler_specific.primary_risk` | str | 11 | 엣지 | `R22.primary_risk` | site→M2 · v3(V3-1): 사전 adverse_qualifier 값 출처(derived) |
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
| 5 | `categories[].id` | str | 10 | 엣지 | `R15.from(modality)` | 계열 끝 · v3.1(V3.1-9): R15.course 는 이 category → 단위 엣지의 속성(이름의 경과 조각) · v3.1(V3.1-10): 문구 유래 엣지는 source_phrases 부록 |
| 6 | `categories[].name` | str | 10 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 7 | `categories[].complications[].name` | str | 65 | 사전 | `dict:adverse_event_type` | v2: 65 이름을 분해한 사건 조각이 사전 뼈대(표기 변형 = 동의어). 이름 하나 → 튜플(event×site×course) 하나 이상 → R15(계열 → 튜플) · v2.3: 미등록 조각이 있는 이름은 raw_name 튜플(anchor = 원장 locator · 접히지 않음) · 경과는 사건에 바로 붙은 수식어만(§1.5) · v2.4: 부위도 사건이 놓인 멤버 안의 조각만(원칙 C) · 후보 둘이면 튜플 둘(원칙 B) · raw_name(미등록 또는 붙지 않은 조각)은 site none · course 미상 · 사전 분해는 dict_tuples 보존(§1.5) · v3(V3-1): 튜플 (event, site, course, qualifier?) — 수식 조각은 같은 멤버 안에서만 · 「공기색전」→ (색전, none, 미상, 공기) · (V3-5) site 에 layer 값 가능 · v3.1(V3.1-9): 단위 = (사건, 부위, 물질) 세 칸 · 상대 부위는 none(relative_site_text 보존) · 이름의 경과 조각은 category → 단위 R15.course · raw_name 은 그대로 |
| 8 | `categories[].complications[].severity` | str | 65 | 엣지 | `R15.severity` | 사전 severity |
| 9 | `categories[].complications[].incidence` | str | 65 | 엣지 | `R15.incidence` | v2.2: 엣지 속성으로만 — 경과(course) 칸을 정하지 않는다(§1.5 경과 규칙) |
| 10 | `categories[].complications[].onset` | str | 65 | 엣지 | `R15.onset` |  |
| 11 | `categories[].complications[].mechanism` | str | 65 | 엣지 | `R15.mechanism` |  |
| 12 | `categories[].complications[].risk_factors` | list(empty) | 46 | 엣지 | `R15.risk_factors` | 빈 배열 46 = null ⑤ |
| 13 | `categories[].complications[].management` | str | 65 | 엣지 | `R15.management` |  |
| 14 | `categories[].complications[].prevention` | str | 65 | 엣지 | `R15.prevention` | v3(V3-5): 사전 site 조직층(kind=layer) 값 출처(derived) |
| 15 | `categories[].complications[].evidence` | str | 38 | 개체 | `citation.url` | kind=url, `;` 분리 ③ → R15.evidence_ref |
| 16 | `categories[].complications[].duration` | str | 19 | 엣지 | `R15.duration` | v2.2: 엣지 속성으로만 — 경과(course) 칸을 정하지 않는다(§1.5 경과 규칙) |
| 17 | `categories[].complications[].risk_factors[]` | str | 92 | 엣지 | `R15.risk_factors` |  |

## `consent-checklist.json` — 잎 키 8

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `categories[].id` | str | 17 | 엣지 | `R16.from(modality)` | 계열 끝 (R15 emergency_signs 도) · v3.1(V3.1-4): R16 끝은 조건 단위(CND- · 사전 정준값+kind) · v3.1(V3.1-7): R32(basis=ledger) from 계열 |
| 5 | `categories[].name` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 6 | `categories[].mandatory_disclosures[]` | str | 109 | 개체 | `clinical_rule.text` | 고지문 = 속성 · v3(V3-5): 사전 site 조직층(kind=layer) 값 출처(derived) · v3.1(V3.1-7): 문장마다 clinical_rule(kind=disclosure · 원문 · locator) · R32 rule_applies_to(basis=ledger · scope=modality · severity=info) 로 categories[].id 계열에 · 같은 문장은 문구 사전(phrase_dictionary · kind=disclosure) 항목으로 부작용 단위에 닿는다(R15 source_phrases · disclosure=true) · modality.mandatory_disclosures 속성 삭제 |
| 7 | `categories[].contraindications[]` | str | 105 | 개체 | `person_condition.name` | kind=condition, R16.level=consent · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 8 | `categories[].emergency_signs[]` | str | 55 | 사전 | `dict:phrase_dictionary` | kind=emergency_sign · R29 → R15(frequency_class=emergency) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3(V3-1): 사전 adverse_qualifier 값 출처(derived) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |

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
| 2 | `{code}.safety.common[]` | str | 59 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(frequency_class=common) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 3 | `{code}.safety.serious` | null | 2 | 엣지 | `R15(serious)` | null 2 = 미입력 ⑤ (질문 17) |
| 4 | `{code}.safety.uncommon[]` | str | 45 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(frequency_class=uncommon) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
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
| 18 | `{code}.contraindications.absolute[]` | str | 53 | 개체 | `person_condition.name` | R16.level=absolute · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 19 | `{code}.contraindications.relative[]` | str | 55 | 개체 | `person_condition.name` | R16.level=relative · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 20 | `{code}.guardrail_version` | str | 17 | 개체 | `modality.extracted_meta.guardrail_version` |  |
| 21 | `{code}.related_techniques[]` | str | 51 | 개체 | `modality.related_techniques` | v3(V3-2): 「메조보톡스 (더모톡신)」 — 설명 문장(속성) · 회사 괄호 후보 자리 실측 §9.5.9 |
| 22 | `{code}.safety.serious[]` | str | 37 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(frequency_class=serious) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3(V3-1): 사전 adverse_qualifier 값 출처(derived) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 23 | `{code}.safety.emergency[]` | str | 2 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(frequency_class=emergency) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
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
| 34 | `categories.{code}.adverse_effects[].statement` | str | 32 | 사전 | `dict:phrase_dictionary` | kind=evidence_statement · v2: v1.1 adverse_effect(literature_claim) 에서 이동. R19 cites · R20 · R29 · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 35 | `categories.{code}.adverse_effects[].citations[].authors` | str | 32 | 개체 | `citation.authors` | kind=pubmed, pmid 동일성 → R19 |
| 36 | `categories.{code}.adverse_effects[].citations[].title` | str | 32 | 개체 | `citation.title` | kind=pubmed, pmid 동일성 → R19 |
| 37 | `categories.{code}.adverse_effects[].citations[].journal` | str | 32 | 개체 | `citation.journal` | kind=pubmed, pmid 동일성 → R19 |
| 38 | `categories.{code}.adverse_effects[].citations[].year` | int | 32 | 개체 | `citation.year` | kind=pubmed, pmid 동일성 → R19 |
| 39 | `categories.{code}.adverse_effects[].citations[].pmid` | str | 32 | 개체 | `citation.pmid` | kind=pubmed, pmid 동일성 → R19 · v3.1(V3.1-10): 문헌 문구의 인용은 문구 사전 항목 citations[](개체 아님) · R19 from 에서 adverse_expression 삭제 |
| 40 | `categories.{code}.adverse_effects[].citations[].doi` | str | 30 | 개체 | `citation.doi` | kind=pubmed, pmid 동일성 → R19 |
| 41 | `categories.{code}.adverse_effects[].citations[].pmc` | str | 29 | 개체 | `citation.pmc` | kind=pubmed, pmid 동일성 → R19 |
| 42 | `categories.{code}.adverse_effects[].citations[].oa_url` | str | 29 | 개체 | `citation.oa_url` | kind=pubmed, pmid 동일성 → R19 |
| 43 | `categories.{code}.adverse_effects[].accuracy_score` | int | 8 | 사전 | `dict:phrase_dictionary` | v2: adverse_effect 에서 이동 · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문헌 정확도·등록일 → 항목 accuracy[] |
| 44 | `categories.{code}.adverse_effects[].accuracy_note` | str | 8 | 사전 | `dict:phrase_dictionary` | v2: adverse_effect 에서 이동 · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문헌 정확도·등록일 → 항목 accuracy[] |
| 45 | `categories.{code}.adverse_effects[].patient_ko` | str | 32 | 사전 | `dict:phrase_dictionary` | kind=patient_text, lang=ko · 같은 문헌 레코드의 statement 표현과 같은 튜플(§1.5) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 환자 설명 → 항목 translations[](en/zh/ja · 자리 ko 는 자기 항목) · 단위 explanations[] 부록 |
| 46 | `categories.{code}.adverse_effects[].patient_en` | str | 32 | 사전 | `dict:phrase_dictionary` | kind=patient_text, lang=en · 같은 문헌 레코드의 statement 표현과 같은 튜플(§1.5) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 환자 설명 → 항목 translations[](en/zh/ja · 자리 ko 는 자기 항목) · 단위 explanations[] 부록 |
| 47 | `categories.{code}.adverse_effects[].patient_zh` | str | 32 | 사전 | `dict:phrase_dictionary` | kind=patient_text, lang=zh · 같은 문헌 레코드의 statement 표현과 같은 튜플(§1.5) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 환자 설명 → 항목 translations[](en/zh/ja · 자리 ko 는 자기 항목) · 단위 explanations[] 부록 |
| 48 | `categories.{code}.adverse_effects[].patient_ja` | str | 32 | 사전 | `dict:phrase_dictionary` | kind=patient_text, lang=ja · 같은 문헌 레코드의 statement 표현과 같은 튜플(§1.5) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 환자 설명 → 항목 translations[](en/zh/ja · 자리 ko 는 자기 항목) · 단위 explanations[] 부록 |
| 49 | `categories.{code}.adverse_effects[].added_at` | str | 24 | 사전 | `dict:phrase_dictionary` | v2: adverse_effect 에서 이동 · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문헌 정확도·등록일 → 항목 accuracy[] |
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
| 7 | `categories[].items[].name` | str | 122 | 개체 | `modality.price_items.label` | 시술/제품 연결은 사전 일치만 (질문 11) · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
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
| 11 | `procedures[].subcategory` | str | 26 | 엣지 | `R15.subcategory_label` | 8-4 처분: 하위분류 label 정규화 일치 시 하위분류 연결, 아니면 라벨만 |
| 12 | `procedures[].name` | str | 26 | 엣지 | `R15.source_label` | 원문 라벨 |
| 13 | `procedures[].procedure_ref` | str | 26 | 엣지 | `R15.from(proc_axis)+target_depth` | 가장 구체 수준 그대로 (질문 5). to=adverse_effect `PIH` · v2.3: 항목 id(M8-1-1)는 그 항목의 procedure 튜플이 끝, 하위분류 id 는 subcategory, M 코드는 modality(§9.5.8) |
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
| 9 | `timelines[].category` | str | 10 | 엣지 | `R15.from(proc_axis)+target_depth` | M 코드 → 계열, M16-DCA → 하위분류 (질문 7) · v2.3: 끝 깊이 그대로(M 코드 → modality · M16-DCA → subcategory) · timelines[].name 이 튜플로 해결되면 그 튜플 |
| 10 | `timelines[].name` | str | 10 | 엣지 | `R15.source_label` | 시술명 원문. 더 구체 대상은 사전 일치만 · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) |
| 11 | `timelines[].phases[].period` | str | 43 | 엣지 | `R15.period` | 사전 period |
| 12 | `timelines[].phases[].label` | str | 43 | 엣지 | `R15.phase_label` | 사전 phase_label |
| 13 | `timelines[].phases[].normal[]` | str | 162 | 사전 | `dict:phrase_dictionary` | kind=symptom_phrase · R29 → R15(reaction_level=normal) · normal 문구는 사전 원천 아님(표현만, 닿으면 엣지 표시) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 14 | `timelines[].phases[].abnormal[]` | str | 86 | 사전 | `dict:phrase_dictionary` | kind=symptom_phrase · R29 → R15(reaction_level=abnormal) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 15 | `timelines[].phases[].caution[]` | str | 93 | 사전 | `dict:phrase_dictionary` | kind=symptom_phrase · R29 → R15(reaction_level=caution) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 16 | `timelines[].phases[].emergency[]` | str | 94 | 사전 | `dict:phrase_dictionary` | kind=symptom_phrase · R29 → R15(reaction_level=emergency) · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |

## `pre-procedure-checklist.json` — 잎 키 11

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `universal_checks[].id` | str | 12 | 개체 | `person_condition.aliases` | kind=check, universal=true |
| 5 | `universal_checks[].label` | str | 12 | 개체 | `person_condition.name` | kind=check, universal=true · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=check) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 6 | `universal_checks[].type` | str | 12 | 개체 | `person_condition.universal_level` | 사전 condition_level |
| 7 | `universal_checks[].description` | str | 12 | 개체 | `person_condition.description` |  |
| 8 | `category_specific[].id` | str | 17 | 엣지 | `R16.from(modality)` | v3.1(V3.1-4): R16 끝은 조건 단위(CND-) |
| 9 | `category_specific[].name` | str | 17 | 사전 | `dict:modality` | 코드 연결 동의어 |
| 10 | `category_specific[].checks[].label` | str | 123 | 개체 | `person_condition.name` | kind=check → R16 · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=check) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
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
| 12 | `combos[].packages[].products[]` | str | 24 | 개체 | `package.products_text` | 조합 문장 — 제품 사전 일치 자동 아님 · v3(V3-2): 「보톡스(엘러간)」 7곳 — 합성 문장(속성 · 분해 대상 아님)이지만 회사 괄호 규칙의 후보 자리로 §9.5.9 에 실측 |
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
| 8 | `problems[].complaints[].cc_group` | str | 115 | 사전 | `dict:problem_subcategory_label` | 8-2 처분: (problem_id, label) 로 고민 하위분류 결합(R7). 부위 라벨 10 은 dict:site 동의어에도 · complaint.cc_group_raw 원문 |
| 9 | `problems[].complaints[].procedures[].name` | str | 254 | 엣지 | `R9.target_label` | 「시술 종류」층 (질문 10) · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 10 | `problems[].complaints[].procedures[].category` | str | 254 | 엣지 | `R9.modality_code` |  |
| 11 | `problems[].complaints[].procedures[].role` | str | 254 | 엣지 | `R9.role` |  |
| 12 | `problems[].complaints[].procedures[].products[]` | str | 388 | 엣지 | `R9.products` | 제품 사전 일치 → product id, 미일치 4종 ⑨ · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) |
| 13 | `problems[].complaints[].combos[].name` | str | 146 | 개체 | `package.name` | kind=cc_combo |
| 14 | `problems[].complaints[].combos[].combo[]` | str | 277 | 엣지 | `R12.target_label` | 사전 일치만 · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
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
| 7 | `comparisons[].procedures[].name` | str | 39 | 엣지 | `R12.target_label` | 사전 일치만 (질문 11) · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
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
| 9 | `profiles[].mechanism[]` | str | 25 | 사전 | `dict:technique` | R5 — 기법 사전의 유일한 출처(8-4) · v3(V3-8): R5 from = modality\|modality_subcategory — 하위분류 단위 기본 기법은 canonical_mapping 결정으로만(basis) |
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
| 7 | `botulinum_toxin.products[].manufacturer` | str | 11 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null · v3(V3-2): 회사 괄호 규칙의 제품→회사 지도(제조사) |
| 8 | `botulinum_toxin.products[].country` | str | 11 | 사전 | `dict:country` | product.country. `-` = null |
| 9 | `botulinum_toxin.products[].mfds` | bool | 11 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 10 | `botulinum_toxin.products[].note` | str | 1 | 개체 | `product.note` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보(「화장품 허가. 주사/주입 사용 금지」 류) — R32 는 edge_create 로만 · 실측 §9.7.2 |
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
| 31 | `skin_booster.products[].note` | str | 2 | 개체 | `product.note` | 스킨보톡스 → not_separate_product (질문 18) · v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보(「화장품 허가. 주사/주입 사용 금지」 류) — R32 는 edge_create 로만 · 실측 §9.7.2 |
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
| 44 | `energy_device.products[].type` | str | 18 | 사전 | `dict:product_type` | 8-4 처분: 기법 사전 아님 — 제품 유형 사전만 |
| 45 | `prp_exosome.category_id` | str | 1 | 엣지 | `R4.from(modality)` | 섹션 키 `prp_exosome` 는 계열 alias |
| 46 | `prp_exosome.products[].name` | str | 5 | 개체 | `product.name` |  |
| 47 | `prp_exosome.products[].name_en` | str | 5 | 개체 | `product.name_en` |  |
| 48 | `prp_exosome.products[].manufacturer` | str | 5 | 사전 | `dict:manufacturer` | product.manufacturer. `-` = null |
| 49 | `prp_exosome.products[].country` | str | 5 | 사전 | `dict:country` | product.country. `-` = null |
| 50 | `prp_exosome.products[].mfds` | bool | 5 | 개체 | `product.mfds` | 신뢰 2 식약처 (질문 16) |
| 51 | `prp_exosome.products[].type` | str | 5 | 사전 | `dict:product_type` |  |
| 52 | `prp_exosome.products[].note` | str | 2 | 개체 | `product.note` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보(「화장품 허가. 주사/주입 사용 금지」 류) — R32 는 edge_create 로만 · 실측 §9.7.2 |
| 53 | `prp_exosome.products[].legal_warning` | str | 2 | 개체 | `product.legal_warning` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보 — 규칙 문장이면 edge_create(R32 rule_applies_to · from_ref locator)가 레코드와 엣지를 세운다(값 자동 생성 없음 · 실측 §9.7.2) |
| 54 | `prp_exosome.products[].regulatory_status` | str | 2 | 개체 | `product.regulatory_status` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보 — 규칙 문장이면 edge_create(R32 rule_applies_to · from_ref locator)가 레코드와 엣지를 세운다(값 자동 생성 없음 · 실측 §9.7.2) |
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
| 3 | `links[].from` | str | 115 | 엣지 | `R18.from_label` | `M코드-이름` 분해 ③ → 계열 확정, 이름은 사전 일치만 (질문 8) · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 4 | `links[].from_category` | str | 115 | 엣지 | `R18.from_modality` |  |
| 5 | `links[].to` | str | 115 | 엣지 | `R18.to_label` |  · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
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
| 4 | `modality[].group` | str | 17 | 사전 | `dict:modality_group` | modality.group · v3.1(V3.1-6): modality_group 값 「관리」가 stopword 와 겹친다 — 통째 일치가 먼저 · 분해 사전이 아니라 충돌 없음(overlap 목록) |
| 5 | `modality[].subcategories[].id` | str | 74 | 개체 | `modality_subcategory.code` | + aliases |
| 6 | `modality[].subcategories[].label` | str | 74 | 개체 | `modality_subcategory.label` | 8-4 처분: 기법 사전 아님 — 하위분류 개체로만 |
| 7 | `modality[].subcategories[].items[].id` | str | 521 | 개체 | `catalog_item.aliases` | 질문 4 · v2: CAT- 개체의 alias |
| 8 | `modality[].subcategories[].items[].name` | str | 521 | 개체 | `catalog_item.name` | 분류 항목 이름 그대로. R3 제품 일치(같은 계열 제품명) · v2: 분해 규칙 §1.4 로 procedure 튜플 원천 ① · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · (V3-2) 괄호 안 회사·제품 규칙 후보 자리(「보톡스(엘러간)」) |
| 9 | `modality[].subcategories[].items[].detail` | str | 521 | 개체 | `catalog_item.detail` | 빈 문자열 20 = null · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 10 | `modality[].subcategories[].items[].extracted.overview` | str | 521 | 개체 | `catalog_item.overview` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 11 | `modality[].subcategories[].items[].extracted.mechanism` | str | 521 | 개체 | `catalog_item.mechanism` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 12 | `modality[].subcategories[].items[].extracted.indications.primary[]` | str | 1656 | 개체 | `catalog_item.indications_primary` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 13 | `modality[].subcategories[].items[].extracted.indications.extended[]` | str | 10 | 개체 | `catalog_item.indications_extended` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 14 | `modality[].subcategories[].items[].extracted.safety.common[]` | str | 1278 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(catalog_item→승격 규칙, frequency_class=common) · v2.3: R29 출처에 등재(수정 7) · R15 from = 항목의 procedure 튜플 · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 15 | `modality[].subcategories[].items[].extracted.safety.serious[]` | str | 422 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(catalog_item→승격 규칙, frequency_class=serious) · v2.3: R29 출처에 등재(수정 7) · R15 from = 항목의 procedure 튜플 · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3(V3-1): 사전 adverse_qualifier 값 출처(derived) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 16 | `modality[].subcategories[].items[].extracted.onset_duration.onset` | str | 520 | 개체 | `catalog_item.onset` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 17 | `modality[].subcategories[].items[].extracted.onset_duration.duration` | str | 521 | 개체 | `catalog_item.duration` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 18 | `modality[].subcategories[].items[].extracted.aftercare[]` | str | 1914 | 개체 | `catalog_item.aftercare` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 19 | `modality[].subcategories[].items[].extracted.safety.note` | str | 4 | 개체 | `catalog_item.safety_note` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 20 | `modality[].subcategories[].items[].extracted.onset_duration.peak` | str | 7 | 개체 | `catalog_item.peak` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 21 | `modality[].subcategories[].items[].extracted.onset_duration.peak_effect` | str | 8 | 개체 | `catalog_item.peak` | 동의 키 ③ · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 22 | `modality[].subcategories[].items[].extracted.indications.secondary[]` | str | 18 | 개체 | `catalog_item.indications_extended` | 동의 키 ③ (질문 20) · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 23 | `modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]` | str | 6 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(catalog_item→승격 규칙, frequency_class=common(동의 키)) · v2.3: R29 출처에 등재(수정 7) · R15 from = 항목의 procedure 튜플 · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 24 | `modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]` | str | 6 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(catalog_item→승격 규칙, frequency_class=serious(동의 키)) · v2.3: R29 출처에 등재(수정 7) · R15 from = 항목의 procedure 튜플 · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 25 | `modality[].subcategories[].items[].extracted.safety.contraindications[]` | str | 11 | 개체 | `person_condition.name` | R16 (level=unspecified) · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 26 | `modality[].subcategories[].items[].verification_needed` | str | 1 | 개체 | `decision.reason` | kind=verification_hold (질문 23) · v2.2: target={catalog_item_id} · new_value={hold:true} · 원문 = reason · decided_by=원장 작성자 · status=approved |
| 27 | `modality[].subcategories[].items[].extracted.safety.long_term[]` | str | 1 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(catalog_item→승격 규칙, frequency_class=long_term) · v2.3: R29 출처에 등재(수정 7) · R15 from = 항목의 procedure 튜플 · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 28 | `modality[].subcategories[].items[].extracted.onset_duration.maintenance` | str | 1 | 개체 | `catalog_item.maintenance` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 29 | `modality[].extracted.overview` | str | 17 | 개체 | `modality.overview` | 출처=taxonomy (질문 2) |
| 30 | `modality[].extracted.mechanism` | str | 17 | 개체 | `modality.mechanism` |  |
| 31 | `modality[].extracted.indications.primary[]` | str | 56 | 개체 | `modality.indications_primary` |  |
| 32 | `modality[].extracted.indications.extended[]` | str | 100 | 개체 | `modality.indications_extended` |  |
| 33 | `modality[].extracted.contraindications.absolute[]` | str | 53 | 개체 | `person_condition.name` | R16.level=absolute · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 34 | `modality[].extracted.contraindications.relative[]` | str | 55 | 개체 | `person_condition.name` | R16.level=relative · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=condition) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 35 | `modality[].extracted.safety.common[]` | str | 59 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(계열, frequency_class=common) · v2.3: R29 출처에 등재(수정 7) · R15 from = modality · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 36 | `modality[].extracted.safety.uncommon[]` | str | 45 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(계열, frequency_class=uncommon) · v2.3: R29 출처에 등재(수정 7) · R15 from = modality · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 37 | `modality[].extracted.safety.serious[]` | str | 37 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(계열, frequency_class=serious) · v2.3: R29 출처에 등재(수정 7) · R15 from = modality · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3(V3-1): 사전 adverse_qualifier 값 출처(derived) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 38 | `modality[].extracted.onset_duration.onset` | str | 17 | 개체 | `modality.onset` |  |
| 39 | `modality[].extracted.onset_duration.peak` | str | 17 | 개체 | `modality.peak` |  |
| 40 | `modality[].extracted.onset_duration.duration` | str | 17 | 개체 | `modality.duration` |  |
| 41 | `modality[].extracted.aftercare[]` | str | 53 | 개체 | `modality.aftercare` |  |
| 42 | `modality[].extracted.related_techniques[]` | str | 51 | 개체 | `modality.related_techniques` | v3(V3-2): 「메조보톡스 (더모톡신)」 — 설명 문장(속성) · 회사 괄호 후보 자리 실측 §9.5.9 |
| 43 | `modality[].products[].id` | str | 59 | 개체 | `product.aliases` | M1-P-0 형 → R4 소속 |
| 44 | `modality[].products[].name` | str | 59 | 개체 | `product.name` | products.json 과 병합 (질문 3) |
| 45 | `modality[].products[].name_en` | str | 59 | 개체 | `product.name_en` |  |
| 46 | `modality[].products[].manufacturer` | str | 59 | 사전 | `dict:manufacturer` | v3(V3-2): 회사 괄호 규칙의 제품→회사 지도(제조사) |
| 47 | `modality[].products[].country` | str | 59 | 사전 | `dict:country` |  |
| 48 | `modality[].products[].mfds` | bool/null | 59 | 개체 | `product.mfds` | null 17 = 미입력 (질문 16) |
| 49 | `modality[].products[].extracted.overview` | str | 59 | 개체 | `product.overview` |  |
| 50 | `modality[].products[].extracted.mechanism` | str | 59 | 개체 | `product.mechanism` |  |
| 51 | `modality[].products[].extracted.indications.primary[]` | str | 256 | 개체 | `product.indications_primary` |  |
| 52 | `modality[].products[].extracted.safety.common[]` | str | 222 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(product, frequency_class=common) · v2.3: R29 출처에 등재(수정 7) · R15 from = product · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 53 | `modality[].products[].extracted.safety.note` | str | 1 | 개체 | `product.safety_note` |  |
| 54 | `modality[].products[].extracted.onset_duration.onset` | str | 59 | 개체 | `product.onset` |  |
| 55 | `modality[].products[].extracted.onset_duration.duration` | str | 59 | 개체 | `product.duration` |  |
| 56 | `modality[].products[].extracted.aftercare[]` | str | 238 | 개체 | `product.aftercare` |  |
| 57 | `modality[].products[].extracted.onset_duration.peak_effect` | str | 5 | 개체 | `product.peak` | 동의 키 ③ |
| 58 | `modality[].products[].extracted.onset_duration.diffusion` | str | 1 | 개체 | `product.diffusion` |  |
| 59 | `modality[].products[].note` | str | 5 | 개체 | `product.note` | v3.1(V3.1-2): clinical_rule(kind=product_note) 출처 후보 — 규칙 문장이면 edge_create(R32 rule_applies_to · from_ref locator)가 레코드와 엣지를 세운다(값 자동 생성 없음 · 실측 §9.7.2) |
| 60 | `modality[].name` | str | 17 | 버림 | `drop` | 17/17 `category` 와 같은 값 — 중복 키 |
| 61 | `modality[].products[].extracted.indications.secondary[]` | str | 14 | 개체 | `product.indications_extended` | 동의 키 ③ |
| 62 | `modality[].products[].extracted.safety.serious[]` | str | 62 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(product, frequency_class=serious) · v2.3: R29 출처에 등재(수정 7) · R15 from = product · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3(V3-1): 사전 adverse_qualifier 값 출처(derived) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 63 | `modality[].subcategories[].description` | str | 3 | 개체 | `modality_subcategory.description` |  |
| 64 | `modality[].products[].ingredient` | str | 9 | 사전 | `dict:ingredient_material` |  |
| 65 | `modality[].subcategories[].items[].classification_issue` | str | 2 | 개체 | `decision.reason` | kind=ledger_correction_note · v2.2: target={catalog_item_id} · new_value={note} · 원문 = reason |
| 66 | `modality[].subcategories[].items[].is_marketing_name` | bool | 6 | 개체 | `catalog_item.is_marketing_name` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 67 | `modality[].subcategories[].items[].ingredient_basis` | str | 6 | 개체 | `catalog_item.ingredient_basis` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 68 | `modality[].subcategories[].items[].canonical_category` | str | 6 | 개체 | `decision.new_value` | kind=canonical_mapping (하위분류 사전 일치만) · v2.2: target={from_ref: CAT-id, scope: 항목} · new_value={to_id: SUB-id} |
| 69 | `modality[].subcategories[].items[].naming_caveat` | str | 6 | 개체 | `catalog_item.naming_caveat` |  · v2: catalog_item(분류 항목 그대로). 튜플은 이름 분해 → procedure(R26) |
| 70 | `modality[].products[].type` | str | 24 | 사전 | `dict:product_type` |  |
| 71 | `modality[].products` | list(empty) | 7 | 개체 | `modality.products_present` | 빈 배열 7 = null (질문 15) |
| 72 | `modality[].products[].material` | str | 5 | 사전 | `dict:ingredient_material` |  |
| 73 | `modality[].products[].extracted.safety.common_side_effects[]` | str | 4 | 사전 | `dict:phrase_dictionary` | kind=safety_phrase · R29 → R15(product, frequency_class=common(동의 키)) · v2.3: R29 출처에 등재(수정 7) · R15 from = product · v2.4: 표현은 단위를 가리키기만(원칙 D) — R29 는 match_status=exact(미등록 0 · 붙지 않은 조각 0 · 후보 전부 기존 단위와 세 칸 일치)일 때만 · 새 튜플 0 · 아니면 unlinked + candidates(§1.5 · §2.15) · v3.1(V3.1-10): adverse_expression 개체·R29 삭제 — 문구 → 정규화형 항목(status auto\|approved\|unlinked) · auto 면 (사건, 부위, 물질) 단위(없으면 생성) + R15 source_phrases 부록 · unlinked 면 게이트 unlinked_phrases |
| 74 | `modality[].products[].extracted.safety.contraindications[]` | str | 1 | 개체 | `product.contraindication_notes` | 병합 금기 문장 |
| 75 | `modality[].subcategories[].items[].correction_note` | str | 1 | 개체 | `decision.reason` | kind=ledger_correction_note · v2.2: target={catalog_item_id} · new_value={note} · 원문 = reason |
| 76 | `modality[].subcategories[].items[].reclassified_to` | str | 1 | 개체 | `decision.new_value` | kind=reclassification → R2 재배치 · v2.2: target={catalog_item_id} · new_value={modality_id} |
| 77 | `modality[].subcategories[].items` | list(empty) | 2 | 개체 | `modality_subcategory.items_present` | 빈 배열 2 = null |
| 78 | `problem[].id` | str | 14 | 개체 | `problem.code` | 정본 (질문 12) |
| 79 | `problem[].category` | str | 14 | 개체 | `problem.name` | = 사전 problem 정준값 |
| 80 | `problem[].category_en` | str | 14 | 개체 | `problem.name_en` |  |
| 81 | `problem[].subcategories[].id` | str | 53 | 개체 | `problem_subcategory.code` |  |
| 82 | `problem[].subcategories[].label` | str | 53 | 개체 | `problem_subcategory.label` | = 사전 problem_subcategory_label 정준값. 부위 라벨 10 만 부위 사전(R11) |
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
| 9 | `by_concern[].severity_levels[].optimal_combo[]` | str | 74 | 엣지 | `R12.target_label` | kind=optimization_plan. 사전 일치만 · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
| 10 | `by_concern[].severity_levels[].sequence` | str | 24 | 개체 | `package.sequence_text` |  |
| 11 | `by_concern[].severity_levels[].rationale` | str | 24 | 개체 | `package.clinical_rationale` |  |
| 12 | `by_concern[].severity_levels[].expected_sessions` | str | 24 | 개체 | `package.expected_sessions` |  |
| 13 | `by_concern[].severity_levels[].total_duration` | str | 24 | 개체 | `package.total_duration` |  |
| 14 | `by_concern[].severity_levels[].evidence_level` | str | 24 | 개체 | `package.evidence_level` | 사전 evidence_level |
| 15 | `by_concern[].severity_levels[].contraindicated_combos` | list(empty) | 11 | 개체 | `package.contraindicated_combos` | 빈 배열 11 = null |
| 16 | `by_concern[].severity_levels[].contraindicated_combos[]` | str | 17 | 개체 | `package.contraindicated_combos` | R18 변환은 사전 일치만 |
| 17 | `by_concern[].severity_levels[].caveats[]` | str | 2 | 개체 | `package.caveats` |  |
| 18 | `by_age_group[].age` | str | 4 | 개체 | `person_condition.name` | kind=age_group, 사전 age_group · v3.1(V3.1-4): 조건 사전 person_condition 값 출처(derived) · 이름은 사전 값(+표지어)으로 완전 일치만 접고 아니면 raw_name 단위(kind=age_group) · 문장은 단위의 phrases[] 부록 + R16/R17/R18.source_phrases |
| 19 | `by_age_group[].primary_concerns[]` | str | 17 | 엣지 | `R17.target_label` | relation_kind=primary_concern → 고민 사전 일치만 |
| 20 | `by_age_group[].recommended_base[]` | str | 17 | 엣지 | `R17.target_label` | recommended_base · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 21 | `by_age_group[].avoid[]` | str | 6 | 엣지 | `R17.target_label` | avoid · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 22 | `by_age_group[].maintenance` | str | 4 | 개체 | `person_condition.maintenance` |  |
| 23 | `by_age_group[].annual_focus` | str | 4 | 개체 | `person_condition.annual_focus` |  |
| 24 | `by_age_group[].upgrade[]` | str | 5 | 엣지 | `R17.target_label` | upgrade · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
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
| 36 | `annual_plans[].schedule[].procedures[]` | str | 77 | 엣지 | `R12.target_label` | `토닝 4회` 횟수 섞임 — 사전 일치만 · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |

## `treatment-sequence.json` — 잎 키 20

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | str | 1 | 개체 | `source_file.version` | 파일 메타 (질문 25) |
| 2 | `updated` | str | 1 | 개체 | `source_file.updated` | 파일 메타 (질문 25) |
| 3 | `description` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `principles[]` | str | 13 | 개체 | `clinical_rule.text` | kind=principle |
| 5 | `sequence_order[].order` | int | 11 | 개체 | `modality.same_session_order.order` | categories[] 끝에 |
| 6 | `sequence_order[].phase` | str | 11 | 사전 | `dict:session_phase` | modality.same_session_order.phase |
| 7 | `sequence_order[].categories[]` | str | 19 | 개체 | `modality.same_session_order(소속)` | 코드/코드+라벨/라벨 세 형식 (질문 7) — 미해결은 ⑨ · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) |
| 8 | `sequence_order[].reason` | str | 11 | 개체 | `modality.same_session_order.reason` |  |
| 9 | `incompatible_same_day[].pair[]` | str | 17 | 엣지 | `R18.from_label/to_label` | kind=incompatible_same_day. 사전 일치만 · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 10 | `incompatible_same_day[].reason` | str | 9 | 엣지 | `R18.reason` |  |
| 11 | `common_combos[].name` | str | 8 | 개체 | `package.name` | kind=session_combo |
| 12 | `common_combos[].sequence[]` | str | 26 | 엣지 | `R12.target_label` | order = 배열 순서 · v2: 분해 → procedure 튜플(§1.4) 원천 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): `\d+회` → R12.session_count · `\d+차` → R12.session_index(R12 자리) |
| 13 | `common_combos[].total_time` | str | 8 | 개체 | `package.total_duration` |  |
| 14 | `common_combos[].note` | str | 3 | 개체 | `package.note` |  |
| 15 | `minimum_intervals[].from` | str | 9 | 엣지 | `R18.from_label` | kind=minimum_interval. 사람 조건(이소트레티노인)도 from 가능 · v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 16 | `minimum_intervals[].to` | str | 9 | 엣지 | `R18.to_label` | v2.3: 끝 = procedure 튜플(§3 엣지 끝 규칙 · 튜플로 해결된 참조는 그 튜플 id, M 코드·하위분류 id 만이면 그 노드) · v2.4: procedure.site_id 출처(what_id 와 같은 이름·참조 키 · 부위 조각은 이 문자열에서 · §2.5 · 3-C′) · v3(V3-3·V3-4): stopwords 토큰은 조각이 아니라 qualifier_text(`\d+차` 는 session_index) · `+` 함께 · `/` 부위면 함께·대안이면 또는 · 괄호 안 대안은 바깥 하나 · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿(R12 member_mode and) · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R9/R17/R18/③ 자리 · 엣지 속성 자리 없음) |
| 17 | `minimum_intervals[].min_days` | int | 7 | 엣지 | `R18.min_interval_value` | unit=day (질문 22) |
| 18 | `minimum_intervals[].source` | str | 9 | 개체 | `citation.text` | kind=guideline_text → R18.source_ref |
| 19 | `minimum_intervals[].reason` | str | 9 | 엣지 | `R18.reason` |  |
| 20 | `minimum_intervals[].min_months` | int | 2 | 엣지 | `R18.min_interval_value` | unit=month |

## `step1-products.json` — 잎 키 499 (조사 산출물 · 22번째 브론즈 원천)

| # | 경로 | 타입 | 횟수 | 행선지 | 표적 | 비고 |
|---|---|---|---|---|---|---|
| 1 | `version` | int | 1 | 개체 | `source_file.version` | 파일 메타 |
| 2 | `generated_at` | str | 1 | 개체 | `source_file.updated` | 파일 메타(생성일 2026-10-28, 조사 10-29 판) |
| 3 | `scope` | str | 1 | 개체 | `source_file.description` | 파일 메타 |
| 4 | `basis.frozen_input` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 5 | `basis.decisions[]` | str | 3 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 6 | `basis.research[]` | str | 10 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 7 | `basis.export_check` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 8 | `basis.kpic` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 9 | `basis.script` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 10 | `basis.fields.2_names` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 11 | `basis.fields.4_license` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 12 | `basis.fields.6_companies` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 13 | `basis.fields.line` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 14 | `basis.fields.merged_into · merged_from` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 15 | `basis.fields.moved_to` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 16 | `basis.fields.active` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 17 | `basis.fields.open[]` | str | 1 | 브론즈 | `bronze` | step1 작업 근거 메타(결정·조사 파일 목록) — 설계 |
| 18 | `summary.rows_total` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 19 | `summary.rows_v1` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 20 | `summary.rows_new` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 21 | `summary.active_products` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 22 | `summary.merged` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 23 | `summary.moved_to_procedure_name` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 24 | `summary.status.정상` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 25 | `summary.status.확인 불가` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 26 | `summary.status.허가 대상 아님` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 27 | `summary.status.허가 취소(이력)` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 28 | `summary.status.미허가` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 29 | `summary.status.허가번호 미확인` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 30 | `summary.recommendable.true` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 31 | `summary.recommendable.false` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 32 | `summary.lines.count` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 33 | `summary.lines.names[]` | str | 20 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 34 | `summary.lines.item_undetermined[]` | str | 4 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 35 | `summary.companies_filled.manufacturer` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 36 | `summary.companies_filled.importer` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 37 | `summary.companies_filled.seller` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 38 | `summary.seller_filled` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 39 | `summary.export_only_unlinked` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 40 | `summary.kpic_enriched_licenses` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 41 | `summary.kpic_enriched_note` | str | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 42 | `summary.kpic_linked` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 43 | `summary.review_v3.R1_3line_removed` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 44 | `summary.review_v3.R1_line_items_dropped` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 45 | `summary.review_v3.R2_typo_search_removed` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 46 | `summary.review_v3.R3_drug_importer_na` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 47 | `summary.review_v3.F4_ref_dupes_rows` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 48 | `summary.final_10_28.domestic7` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 49 | `summary.final_10_28.n45_rows` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 50 | `summary.final_10_28.n45_distribution_confirmed` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 51 | `summary.final_10_28.n45_confirmed_by_source` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 52 | `summary.final_10_28.n45_unconfirmed` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 53 | `summary.source_fix` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 54 | `summary.open_rows` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 55 | `summary.open_items` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 56 | `summary.origin_questions` | int | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 57 | `summary.export_only_rows_need_recheck` | list(empty) | 1 | 브론즈 | `bronze` | 파일 수준 집계값 — 실버는 항목 단위에서 재계산 |
| 58 | `shared_license[].ledger_ids[]` | str | 61 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 59 | `shared_license[].names[]` | str | 61 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 60 | `shared_license[].segments[]` | str | 30 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 61 | `shared_license[].licenses[]` | str | 38 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 62 | `shared_license[].relation` | str | 28 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 63 | `shared_license[].licenses_history[]` | str | 6 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 64 | `shared_license[].rule_note` | str | 4 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 65 | `shared_license[].licenses` | list(empty) | 3 | 브론즈 | `bronze` | 라인+품목 설계(같은 허가 묶음) — 식별자 설계라 들이지 않음. 허가 번호 자체는 items[].4_license 에서 |
| 66 | `lines.온다.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 67 | `lines.온다.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 68 | `lines.온다.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 69 | `lines.온다.items[].license_no` | str | 3 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 70 | `lines.온다.items[].name` | str | 3 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 71 | `lines.온다.item_undetermined_rows` | list(empty) | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 72 | `lines.온다.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 73 | `lines.온다.basis` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 74 | `lines.온다.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 75 | `lines.더채움.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 76 | `lines.더채움.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 77 | `lines.더채움.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 78 | `lines.더채움.items[].license_no` | str | 4 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 79 | `lines.더채움.items[].name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 80 | `lines.더채움.items[].ledger_id` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 81 | `lines.더채움.item_undetermined_rows` | list(empty) | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 82 | `lines.더채움.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 83 | `lines.더채움.basis` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 84 | `lines.더채움.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 85 | `lines.엘라비에 프리미어.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 86 | `lines.엘라비에 프리미어.parent_line` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 87 | `lines.엘라비에 프리미어.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 88 | `lines.엘라비에 프리미어.items[].license_no` | str | 4 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 89 | `lines.엘라비에 프리미어.item_undetermined_rows[]` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 90 | `lines.엘라비에 프리미어.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 91 | `lines.엘라비에 프리미어.basis` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 92 | `lines.엘라비에 프리미어.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 93 | `lines.더블로.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 94 | `lines.더블로.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 95 | `lines.더블로.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 96 | `lines.더블로.items[].license_no` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 97 | `lines.더블로.items[].name` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 98 | `lines.더블로.item_undetermined_rows[]` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 99 | `lines.더블로.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 100 | `lines.더블로.basis` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 101 | `lines.더블로.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 102 | `lines.더블로.note` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 103 | `lines.밸피엔.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 104 | `lines.밸피엔.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 105 | `lines.밸피엔.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 106 | `lines.밸피엔.items[].license_no` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 107 | `lines.밸피엔.item_undetermined_rows[]` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 108 | `lines.밸피엔.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 109 | `lines.밸피엔.basis` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 110 | `lines.밸피엔.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 111 | `lines.오메가브이.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 112 | `lines.오메가브이.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 113 | `lines.오메가브이.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 114 | `lines.오메가브이.items[].license_no` | str | 3 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 115 | `lines.오메가브이.items[].name` | str | 3 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 116 | `lines.오메가브이.item_undetermined_rows[]` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 117 | `lines.오메가브이.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 118 | `lines.오메가브이.basis` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 119 | `lines.오메가브이.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 120 | `lines.라라.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 121 | `lines.라라.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 122 | `lines.라라.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 123 | `lines.라라.items[].name` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 124 | `lines.라라.items[].ledger_id` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 125 | `lines.라라.item_undetermined_rows` | list(empty) | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 126 | `lines.라라.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 127 | `lines.라라.basis` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 128 | `lines.라라.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 129 | `lines.DB FNS.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 130 | `lines.DB FNS.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 131 | `lines.DB FNS.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 132 | `lines.DB FNS.items[].license_no` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 133 | `lines.DB FNS.items[].name` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 134 | `lines.DB FNS.item_undetermined_rows` | list(empty) | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 135 | `lines.DB FNS.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 136 | `lines.DB FNS.basis` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 137 | `lines.DB FNS.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 138 | `lines.BBL(Sciton).line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 139 | `lines.BBL(Sciton).parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 140 | `lines.BBL(Sciton).line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 141 | `lines.BBL(Sciton).items[].name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 142 | `lines.BBL(Sciton).items[].ledger_id` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 143 | `lines.BBL(Sciton).items[].license_no` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 144 | `lines.BBL(Sciton).item_undetermined_rows` | list(empty) | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 145 | `lines.BBL(Sciton).company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 146 | `lines.BBL(Sciton).basis` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 147 | `lines.BBL(Sciton).decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 148 | `lines.브이빔.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 149 | `lines.브이빔.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 150 | `lines.브이빔.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 151 | `lines.브이빔.items[].name` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 152 | `lines.브이빔.items[].license_no` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 153 | `lines.브이빔.items[].ledger_id` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 154 | `lines.브이빔.item_undetermined_rows` | list(empty) | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 155 | `lines.브이빔.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 156 | `lines.브이빔.basis` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 157 | `lines.브이빔.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 158 | `lines.바이리즌.line_name` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 159 | `lines.바이리즌.parent_line` | null | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 160 | `lines.바이리즌.line_row` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 161 | `lines.바이리즌.items[].name` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 162 | `lines.바이리즌.items[].license_no` | str | 2 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 163 | `lines.바이리즌.item_undetermined_rows` | list(empty) | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 164 | `lines.바이리즌.company` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 165 | `lines.바이리즌.basis` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 166 | `lines.바이리즌.decision` | str | 1 | 브론즈 | `bronze` | 제품 라인 설계(라인명 키) — 설계라 들이지 않음 |
| 167 | `open[].ledger_id` | str | 31 | 브론즈 | `bronze` | step1 열린 질문 — 작업 상태 |
| 168 | `open[].name` | str | 31 | 브론즈 | `bronze` | step1 열린 질문 — 작업 상태 |
| 169 | `open[].open` | str | 31 | 브론즈 | `bronze` | step1 열린 질문 — 작업 상태 |
| 170 | `open[].decision` | str | 31 | 브론즈 | `bronze` | step1 열린 질문 — 작업 상태 |
| 171 | `items[].ledger_id` | str | 395 | 개체 | `product.aliases` | step1 ledger_id 는 alias 로만(product.survey_ledger_id) |
| 172 | `items[].segment` | str | 395 | 브론즈 | `bronze` | step1 작업 구간 — 설계 |
| 173 | `items[].source` | str | 395 | 브론즈 | `bronze` | step1 행 출처 구분(ledger/site_device/…) — 설계 |
| 174 | `items[].family.code` | str | 395 | 엣지 | `R4.from(modality)` | 계열 힌트(M코드일 때만). `현장 기기`·`원천 항목 없음` = 계열 없음 |
| 175 | `items[].family.name` | str | 395 | 브론즈 | `bronze` | `M코드 계열명 · 하위분류` 합성 — 계열은 code 로 확정 |
| 176 | `items[].1_identity.kind` | str | 395 | 브론즈 | `bronze` | step1 1_identity(종류·근거) — 설계. ERD 에 들이지 않음(C) |
| 177 | `items[].1_identity.basis` | str | 395 | 브론즈 | `bronze` | step1 1_identity(종류·근거) — 설계. ERD 에 들이지 않음(C) |
| 178 | `items[].1_identity.basis_type` | str | 395 | 브론즈 | `bronze` | step1 1_identity(종류·근거) — 설계. ERD 에 들이지 않음(C) |
| 179 | `items[].2_names.display_name` | str | 395 | 개체 | `product.survey_names` | 대표 이름(alias). 원장 대응은 B 분해 규칙으로만 |
| 180 | `items[].2_names.ledger_name` | str/null | 395 | 개체 | `product.survey_names` | 원장 표기 이름(alias). null 2 = 미입력 |
| 181 | `items[].2_names.search_names[].name` | str | 615 | 개체 | `product.survey_names` | 검색 이름(alias, 신뢰 3) |
| 182 | `items[].2_names.search_names[].lang` | str | 615 | 개체 | `product.survey_names` | 이름 언어(한/영) |
| 183 | `items[].2_names.name_basis[]` | str | 1010 | 브론즈 | `bronze` | 이름별 근거 문장 — 조사 메모 |
| 184 | `items[].4_license.status` | str | 395 | 사전 | `dict:license_status` | product.license_status. 「확인 불가」도 값 그대로 |
| 185 | `items[].4_license.kind` | str/null | 395 | 사전 | `dict:license_kind` | product.license_kind. null 140 = 미입력 |
| 186 | `items[].4_license.reason` | str | 395 | 브론즈 | `bronze` | 판정 사유 문장 — 판정 |
| 187 | `items[].4_license.licenses[].key` | str | 342 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 188 | `items[].4_license.licenses[].license_no` | str | 342 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 189 | `items[].4_license.licenses[].kind` | str | 238 | 사전 | `dict:license_kind` | product.licenses.kind |
| 190 | `items[].4_license.licenses[].state` | str | 342 | 사전 | `dict:license_state` | product.licenses.state (허가 건 상태) |
| 191 | `items[].4_license.licenses[].item` | str/null | 301 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 192 | `items[].4_license.licenses[].official_name` | str | 185 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 193 | `items[].4_license.licenses[].official_name_en` | str | 66 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 194 | `items[].4_license.licenses[].models` | list(empty) | 41 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 195 | `items[].4_license.licenses[].holder` | str | 238 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 196 | `items[].4_license.licenses[].holder_biz` | str | 115 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 197 | `items[].4_license.licenses[].manufacturer` | str/null | 124 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 198 | `items[].4_license.licenses[].date` | str/null | 303 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 199 | `items[].4_license.licenses[].pack_unit` | str | 39 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 200 | `items[].4_license.licenses[].source` | str | 199 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 201 | `items[].4_license.licenses[].kpic.drug_code` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 202 | `items[].4_license.licenses[].kpic.drug_name` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 203 | `items[].4_license.licenses[].kpic.ingredient` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 204 | `items[].4_license.licenses[].kpic.company` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 205 | `items[].4_license.licenses[].kpic.class` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 206 | `items[].4_license.licenses[].kpic.atc` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 207 | `items[].4_license.licenses[].kpic.kpic_class` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 208 | `items[].4_license.licenses[].kpic.insurance` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 209 | `items[].4_license.licenses[].kpic.hira_code` | null/str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 210 | `items[].4_license.licenses[].kpic.insurance_code_search` | null/str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 211 | `items[].4_license.licenses[].kpic.source` | str | 46 | 개체 | `product.licenses.kpic.*` | KPIC 코드(drug_code)·분류·급여 — 키 이름 보존. 출처 KPIC(신뢰 3) |
| 212 | `items[].4_license.history` | list(empty) | 335 | 개체 | `product.license_history` | 빈 배열 335 = null ⑤ |
| 213 | `items[].4_license.reference` | list(empty) | 300 | 브론즈 | `bronze` | 빈 배열 300 |
| 214 | `items[].4_license.recommendable` | bool | 395 | 브론즈 | `bronze` | step1 추천 가능 판정 — 다음 실버 빌드 결정 후보, ERD 속성 아님 |
| 215 | `items[].5_spec.license[].license_no` | str | 185 | 개체 | `product.spec.*` | 허가 기준 포장단위·함량 — 키 이름 보존 |
| 216 | `items[].5_spec.license[].pack_unit` | str/null | 185 | 개체 | `product.spec.*` | 허가 기준 포장단위·함량 — 키 이름 보존 |
| 217 | `items[].5_spec.license[].content` | str/null | 185 | 개체 | `product.spec.*` | 허가 기준 포장단위·함량 — 키 이름 보존 |
| 218 | `items[].5_spec.license[].basis` | str | 185 | 개체 | `product.spec.*` | 허가 기준 포장단위·함량 — 키 이름 보존 |
| 219 | `items[].5_spec.market` | null/str | 241 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 220 | `items[].5_spec.note` | str/null | 141 | 브론즈 | `bronze` | 규격 메모 |
| 221 | `items[].6_companies.manufacturer[].name` | str | 407 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 222 | `items[].6_companies.manufacturer[].original` | null/str | 261 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 223 | `items[].6_companies.manufacturer[].basis` | str | 407 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 224 | `items[].6_companies.importer[].name` | str | 403 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 225 | `items[].6_companies.importer[].original` | str/null | 265 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 226 | `items[].6_companies.importer[].basis` | str | 403 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 227 | `items[].6_companies.seller[].name` | str | 403 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 228 | `items[].6_companies.seller[].original` | null | 247 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 229 | `items[].6_companies.seller[].basis` | str | 403 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 230 | `items[].6_companies.license_holder` | list(empty) | 393 | 개체 | `product.companies` | 빈 배열 393 = null |
| 231 | `items[].6_companies.other` | list(empty) | 391 | 개체 | `product.companies` | 빈 배열 391 = null |
| 232 | `items[].6_companies.conflicts` | list(empty) | 384 | 개체 | `conflict` | 빈 배열 384 = 충돌 없음(명시적 빈 목록) |
| 233 | `items[].7_site_use.photo_ids` | list(empty) | 311 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 234 | `items[].7_site_use.note` | str | 141 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 235 | `items[].gate` | null/str | 395 | 브론즈 | `bronze` | step1 게이트 메모 — 작업 상태 |
| 236 | `items[].change_vs_draft` | null/str | 395 | 브론즈 | `bronze` | step1 초안 대비 변경 메모 — 작업 상태 |
| 237 | `items[].note` | null/str | 395 | 개체 | `product.survey_note` | 조사 메모(신뢰 3) |
| 238 | `items[].evidence[]` | str | 591 | 브론즈 | `bronze` | 문자열형 근거(질의 로그) |
| 239 | `items[].taxonomy_product_ids[]` | str | 65 | 브론즈 | `bronze` | step1 이 적어 둔 taxonomy 제품 대응 — 원장 대응은 B 분해 규칙으로만 하므로 쓰지 않는다(C) |
| 240 | `items[].open` | list(empty) | 365 | 브론즈 | `bronze` | 빈 배열 365 |
| 241 | `items[].active` | bool | 395 | 브론즈 | `bronze` | step1 활성 플래그 — 작업 상태 |
| 242 | `items[].merged_from[]` | str | 18 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 243 | `items[].2_names.search_names` | list(empty) | 120 | 개체 | `product.survey_names` | 빈 배열 120 = null ⑤ |
| 244 | `items[].4_license.licenses` | list(empty) | 189 | 개체 | `product.licenses` | 빈 배열 189 = null ⑤ |
| 245 | `items[].5_spec.license` | null/list(empty) | 71 | 개체 | `product.spec` | null 51 = 미입력 |
| 246 | `items[].dedup.role` | str | 28 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 247 | `items[].dedup.duplicates[]` | str | 14 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 248 | `items[].4_license.reference[].key` | str | 130 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 249 | `items[].4_license.reference[].license_no` | str/null | 165 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 250 | `items[].4_license.reference[].kind` | str | 86 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 251 | `items[].4_license.reference[].state` | str | 152 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 252 | `items[].4_license.reference[].item` | str/null | 113 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 253 | `items[].4_license.reference[].official_name` | str/null | 74 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 254 | `items[].4_license.reference[].official_name_en` | str | 18 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 255 | `items[].4_license.reference[].models` | list(empty) | 8 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 256 | `items[].4_license.reference[].holder` | str | 104 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 257 | `items[].4_license.reference[].holder_biz` | str | 28 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 258 | `items[].4_license.reference[].date` | str/null | 109 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 259 | `items[].4_license.reference[].pack_unit` | str | 1 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 260 | `items[].4_license.reference[].source` | str | 100 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 261 | `items[].4_license.reference[].why` | str | 165 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 262 | `items[].4_license.reference[].kpic.drug_code` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 263 | `items[].4_license.reference[].kpic.drug_name` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 264 | `items[].4_license.reference[].kpic.ingredient` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 265 | `items[].4_license.reference[].kpic.company` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 266 | `items[].4_license.reference[].kpic.class` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 267 | `items[].4_license.reference[].kpic.atc` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 268 | `items[].4_license.reference[].kpic.kpic_class` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 269 | `items[].4_license.reference[].kpic.insurance` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 270 | `items[].4_license.reference[].kpic.hira_code` | null | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 271 | `items[].4_license.reference[].kpic.insurance_code_search` | null | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 272 | `items[].4_license.reference[].kpic.source` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 273 | `items[].6_companies.importer[].role` | null/str | 26 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 274 | `items[].6_companies.seller[].role` | null/str | 44 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 275 | `items[].6_companies.license_holder[].name` | str | 2 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 276 | `items[].6_companies.license_holder[].role` | str | 2 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 277 | `items[].6_companies.license_holder[].basis` | str | 2 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 278 | `items[].merged_into` | str | 18 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 279 | `items[].open[]` | str | 31 | 브론즈 | `bronze` | step1 열린 질문 — 작업 상태 |
| 280 | `items[].4_license.licenses[].models[]` | str | 327 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 281 | `items[].4_license.history[].key` | str | 97 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 282 | `items[].4_license.history[].license_no` | str | 109 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 283 | `items[].4_license.history[].kind` | str | 75 | 사전 | `dict:license_kind` | product.license_history.kind |
| 284 | `items[].4_license.history[].state` | str | 109 | 사전 | `dict:license_state` | product.license_history.state (취소·취하·만료) |
| 285 | `items[].4_license.history[].item` | str/null | 77 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 286 | `items[].4_license.history[].official_name` | str/null | 51 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 287 | `items[].4_license.history[].models[]` | str | 52 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 288 | `items[].4_license.history[].holder` | str/null | 75 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 289 | `items[].4_license.history[].date` | str | 87 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 290 | `items[].4_license.history[].source` | str | 53 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 291 | `items[].4_license.history[].manufacturer` | str/null | 32 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 292 | `items[].4_license.reference[].models[]` | str | 106 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 293 | `items[].5_spec.license[].models_with_volume` | null | 123 | 개체 | `product.spec.*` | 허가 기준 포장단위·함량 — 키 이름 보존 |
| 294 | `items[].5_spec.history_license[].license_no` | str | 33 | 브론즈 | `bronze` | 취소 이력 허가의 규격 — 이력 허가는 product.license_history 로 충분 |
| 295 | `items[].5_spec.history_license[].pack_unit` | null | 33 | 브론즈 | `bronze` | 취소 이력 허가의 규격 — 이력 허가는 product.license_history 로 충분 |
| 296 | `items[].5_spec.history_license[].content` | null | 33 | 브론즈 | `bronze` | 취소 이력 허가의 규격 — 이력 허가는 product.license_history 로 충분 |
| 297 | `items[].5_spec.history_license[].models_with_volume` | null | 22 | 브론즈 | `bronze` | 취소 이력 허가의 규격 — 이력 허가는 product.license_history 로 충분 |
| 298 | `items[].5_spec.history_license[].basis` | str | 33 | 브론즈 | `bronze` | 취소 이력 허가의 규격 — 이력 허가는 product.license_history 로 충분 |
| 299 | `items[].5_spec.rule_note` | str | 34 | 브론즈 | `bronze` | 규격 규칙 메모 |
| 300 | `items[].4_license.licenses[].product_names` | str/null | 67 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 301 | `items[].5_spec.license[].models_with_volume[]` | str | 46 | 개체 | `product.spec.*` | 허가 기준 포장단위·함량 — 키 이름 보존 |
| 302 | `items[].line.line_name` | str | 35 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 303 | `items[].line.role` | str | 35 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 304 | `items[].line.members[]` | str | 41 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 305 | `items[].line.decision` | str | 35 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 306 | `items[].shared_license_with[]` | str | 77 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 307 | `items[].line.parent_line` | null/str | 11 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 308 | `items[].line.items[].license_no` | str | 24 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 309 | `items[].line.items[].name` | str | 19 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 310 | `items[].line.items[].ledger_id` | str | 6 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 311 | `items[].line.company` | str | 11 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 312 | `items[].line.item_undetermined` | bool | 11 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 313 | `items[].line.basis` | null/str | 11 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 314 | `items[].4_license.approval.by` | str | 6 | 브론즈 | `bronze` | 코디 검수 승인 기록 — 작업 상태 |
| 315 | `items[].4_license.approval.date` | str | 6 | 브론즈 | `bronze` | 코디 검수 승인 기록 — 작업 상태 |
| 316 | `items[].4_license.approval.basis` | str | 6 | 브론즈 | `bronze` | 코디 검수 승인 기록 — 작업 상태 |
| 317 | `items[].4_license.reference[].manufacturer` | str/null | 19 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 318 | `items[].4_license.reference[].product_names` | str | 23 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 319 | `items[].6_companies.seller[].period` | str | 19 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 320 | `items[].6_companies.manufacturer[].role` | str/null | 39 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 321 | `items[].line.item` | str | 4 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 322 | `items[].line.line_row` | str | 6 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 323 | `items[].5_spec.history_license[].models_with_volume[]` | str | 19 | 브론즈 | `bronze` | 취소 이력 허가의 규격 — 이력 허가는 product.license_history 로 충분 |
| 324 | `items[].4_license.history[].holder_biz` | str | 10 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 325 | `items[].4_license.history[].date_note` | str | 3 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 326 | `items[].6_companies.conflicts[].field` | str | 12 | 개체 | `conflict.values` | kind=value_conflict(허가 값 vs 다른 출처) — 「덮어쓰지 않음」 그대로 |
| 327 | `items[].6_companies.conflicts[].license` | str | 12 | 개체 | `conflict.values` | kind=value_conflict(허가 값 vs 다른 출처) — 「덮어쓰지 않음」 그대로 |
| 328 | `items[].6_companies.conflicts[].other` | str | 12 | 개체 | `conflict.values` | kind=value_conflict(허가 값 vs 다른 출처) — 「덮어쓰지 않음」 그대로 |
| 329 | `items[].6_companies.conflicts[].source` | str | 12 | 개체 | `conflict.values` | kind=value_conflict(허가 값 vs 다른 출처) — 「덮어쓰지 않음」 그대로 |
| 330 | `items[].6_companies.conflicts[].note` | str | 12 | 개체 | `conflict.values` | kind=value_conflict(허가 값 vs 다른 출처) — 「덮어쓰지 않음」 그대로 |
| 331 | `items[].6_companies.company_search_names[].name` | str | 13 | 브론즈 | `bronze` | 회사 검색 이름(오기 포함) — 조사 과정 |
| 332 | `items[].6_companies.company_search_names[].basis` | str | 13 | 브론즈 | `bronze` | 회사 검색 이름(오기 포함) — 조사 과정 |
| 333 | `items[].4_license.licenses[].use_purpose` | str | 6 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 334 | `items[].4_license.licenses[].use_purpose_source` | str | 6 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 335 | `items[].4_license.licenses[].type_name_api` | str | 6 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 336 | `items[].5_spec.market[].source_item` | str | 35 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 337 | `items[].5_spec.market[].unit_raw` | str | 14 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 338 | `items[].5_spec.market[].amount` | float/null | 14 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 339 | `items[].5_spec.market[].unit` | str/null | 35 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 340 | `items[].5_spec.market[].price_krw.low` | int | 14 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 341 | `items[].5_spec.market[].price_krw.mid` | int | 14 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 342 | `items[].5_spec.market[].price_krw.high` | int | 14 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 343 | `items[].5_spec.market[].basis` | str | 14 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 344 | `items[].dedup.same_as` | str | 14 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 345 | `items[].dedup.basis` | str | 14 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 346 | `items[].dedup.state` | str | 14 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 347 | `items[].4_license.unlinked_use_mismatch[].key` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 348 | `items[].4_license.unlinked_use_mismatch[].license_no` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 349 | `items[].4_license.unlinked_use_mismatch[].kind` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 350 | `items[].4_license.unlinked_use_mismatch[].state` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 351 | `items[].4_license.unlinked_use_mismatch[].item` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 352 | `items[].4_license.unlinked_use_mismatch[].official_name` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 353 | `items[].4_license.unlinked_use_mismatch[].official_name_en` | str | 4 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 354 | `items[].4_license.unlinked_use_mismatch[].product_names` | str | 4 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 355 | `items[].4_license.unlinked_use_mismatch[].models[]` | str | 21 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 356 | `items[].4_license.unlinked_use_mismatch[].holder` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 357 | `items[].4_license.unlinked_use_mismatch[].holder_biz` | str | 4 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 358 | `items[].4_license.unlinked_use_mismatch[].manufacturer` | str | 1 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 359 | `items[].4_license.unlinked_use_mismatch[].date` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 360 | `items[].4_license.unlinked_use_mismatch[].source` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 361 | `items[].4_license.unlinked_use_mismatch[].use_purpose` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 362 | `items[].4_license.unlinked_use_mismatch[].use_purpose_source` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 363 | `items[].4_license.unlinked_use_mismatch[].type_name_api` | str | 5 | 브론즈 | `bronze` | 용도 불일치로 연결 안 한 허가 — 후보 |
| 364 | `items[].5_spec.license_unlinked_note` | str | 4 | 브론즈 | `bronze` | 메모 |
| 365 | `items[].use_mismatch` | str | 4 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 366 | `items[].4_license.licenses[].valid` | str | 3 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 367 | `items[].6_companies.other[].name` | str | 5 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 368 | `items[].6_companies.other[].role` | str | 5 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 369 | `items[].6_companies.other[].basis` | str | 5 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 370 | `items[].6_companies.other[].period` | str | 2 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 371 | `items[].6_companies.importer[].period` | str | 1 | 개체 | `product.companies.*` | 역할별 회사(name·basis·original·role·period). `근거 없음`·`해당 없음` 은 값 그대로 |
| 372 | `items[].7_site_use.photo_ids[]` | str | 79 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 373 | `items[].moved_to` | str | 23 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 374 | `items[].moved_note` | str | 23 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 375 | `items[].4_license.history[].official_name_en` | str | 6 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 376 | `items[].weak_link` | str | 2 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 377 | `items[].4_license.history[].product_names` | str | 3 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 378 | `items[].1_identity.detail` | str | 136 | 브론즈 | `bronze` | step1 1_identity(종류·근거) — 설계. ERD 에 들이지 않음(C) |
| 379 | `items[].2_names.ledger_maker_texts[]` | str | 84 | 브론즈 | `bronze` | 원장 업체 표기 원문(오기 포함) — 제조사 사전 일치 자동 아님 |
| 380 | `items[].4_license.licenses[].model` | str | 157 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 381 | `items[].4_license.licenses[].company` | str | 104 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 382 | `items[].5_spec.license_pack` | str | 123 | 브론즈 | `bronze` | `해당 없음(의료기기 장비 …)` 설명 문장 |
| 383 | `items[].5_spec.content` | str | 123 | 브론즈 | `bronze` | `해당 없음(장비)` 설명 문장 |
| 384 | `items[].7_site_use.sample_photo_ids` | list(empty) | 111 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 385 | `items[].7_site_use.photo_reads[].photo_id` | str | 47 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 386 | `items[].7_site_use.photo_reads[].read_model` | null/str | 47 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 387 | `items[].7_site_use.photo_reads[].matches` | str | 47 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 388 | `items[].evidence[].type` | str | 594 | 브론즈 | `bronze` | 조사 근거 메모(유형·설명·출처 문장) |
| 389 | `items[].evidence[].detail` | str | 580 | 브론즈 | `bronze` | 조사 근거 메모(유형·설명·출처 문장) |
| 390 | `items[].evidence[].source` | str | 182 | 브론즈 | `bronze` | 조사 근거 메모(유형·설명·출처 문장) |
| 391 | `items[].4_license.history[].model` | str | 57 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 392 | `items[].4_license.history[].company` | str | 34 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 393 | `items[].7_site_use.sample_photo_ids[]` | str | 12 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 394 | `items[].evidence[].urls[]` | str | 190 | 개체 | `citation.url` | kind=url → 제품 R19 |
| 395 | `items[].4_license.reference[].model` | str | 72 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 396 | `items[].4_license.reference[].company` | str | 44 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 397 | `items[].7_site_use.photo_reads` | list(empty) | 79 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 398 | `items[].4_license.reference[].candidate` | str | 9 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 399 | `items[].recheck.before` | str | 69 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 400 | `items[].recheck.method` | str | 69 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 401 | `items[].recheck.queries[].query` | str | 224 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 402 | `items[].recheck.queries[].total` | int | 224 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 403 | `items[].recheck.queries[].fetched` | int | 224 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 404 | `items[].recheck.queries[].name_hits` | list(empty) | 130 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 405 | `items[].recheck.queries[].name_hits_count` | int | 224 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 406 | `items[].recheck.result` | str | 69 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 407 | `items[].recheck.note` | str | 50 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 408 | `items[].4_license.reference[].state_raw` | str | 7 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 409 | `items[].4_license.reference[].serial` | str | 7 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 410 | `items[].recheck.queries[].name_hits[]` | str | 420 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 411 | `items[].recheck.found[]` | str | 29 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 412 | `items[].recheck.auto_rule_a` | bool | 19 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 413 | `items[].5_spec.market[].low` | int | 21 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 414 | `items[].5_spec.market[].mid` | int | 21 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 415 | `items[].5_spec.market[].high` | int | 21 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 416 | `items[].5_spec.market[].currency` | str | 21 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 417 | `items[].5_spec.market[].expr` | str | 21 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 418 | `items[].4_license.history[].models` | list(empty) | 4 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 419 | `items[].4_license.licenses[].state_raw` | str | 23 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 420 | `items[].4_license.licenses[].serial` | str | 23 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 421 | `items[].recheck.queries` | list(empty) | 4 | 브론즈 | `bronze` | 중복·라인·재탐색 설계/과정 — 들이지 않음 |
| 422 | `items[].4_license.license_basis` | str | 23 | 브론즈 | `bronze` | 허가 연결 근거 메모 |
| 423 | `items[].4_license.distribution_sources[].url` | str | 44 | 개체 | `citation.url` | kind=url(유통 근거 가격표) → 제품 R19 |
| 424 | `items[].4_license.distribution_sources[].text` | str | 44 | 개체 | `citation.text` | 유통 근거 설명 |
| 425 | `items[].5_spec.license_spec` | list(empty) | 117 | 개체 | `product.spec` | 빈 배열 117 = null |
| 426 | `items[].5_spec.market_pricing` | list(empty) | 123 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 427 | `items[].7_site_use.photos` | list(empty) | 82 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 428 | `items[].merged_ledger_ids` | null | 122 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 429 | `items[].line_children` | null | 124 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 430 | `items[].evidence` | list(empty) | 87 | 브론즈 | `bronze` | 빈 배열 87 |
| 431 | `items[].4_license.licenses[].item_class` | str | 30 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 432 | `items[].4_license.licenses[].manuf_nm` | null/str | 30 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 433 | `items[].4_license.licenses[].consign` | null | 30 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 434 | `items[].4_license.licenses[].permit_date` | str | 39 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 435 | `items[].4_license.licenses[].cancel` | null | 30 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 436 | `items[].4_license.licenses[].basis` | str | 39 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 437 | `items[].5_spec.market_pricing[].source_item` | str | 3 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 438 | `items[].5_spec.market_pricing[].unit` | str | 3 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 439 | `items[].5_spec.market_pricing[].low` | int | 3 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 440 | `items[].5_spec.market_pricing[].mid` | int | 3 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 441 | `items[].5_spec.market_pricing[].high` | int | 3 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 442 | `items[].5_spec.market_pricing[].currency` | str | 3 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 443 | `items[].5_spec.market_pricing[].basis` | str | 3 | 브론즈 | `bronze` | market-pricing.json 파생 복사본 — 가격 정본은 원장(modality.price_items) |
| 444 | `items[].7_site_use.photos[].photo_id` | str | 44 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 445 | `items[].7_site_use.photos[].in_use` | bool | 44 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 446 | `items[].7_site_use.photos[].read_model` | str/null | 44 | 브론즈 | `bronze` | 현장 사진 연결 — ERD 범위 밖(사진 자산은 별도) |
| 447 | `items[].4_license.history[].item_class` | str | 22 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 448 | `items[].4_license.history[].manuf_nm` | str/null | 22 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 449 | `items[].4_license.history[].consign` | null/str | 22 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 450 | `items[].4_license.history[].permit_date` | str | 22 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 451 | `items[].4_license.history[].cancel.code` | str | 22 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 452 | `items[].4_license.history[].cancel.date` | str | 22 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 453 | `items[].4_license.history[].basis` | str | 22 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 454 | `items[].merged_ledger_ids[]` | str | 4 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 455 | `items[].4_license.reference[].item_class` | str | 21 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 456 | `items[].4_license.reference[].manuf_nm` | null/str | 21 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 457 | `items[].4_license.reference[].consign` | null/str | 21 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 458 | `items[].4_license.reference[].permit_date` | str | 21 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 459 | `items[].4_license.reference[].cancel` | null | 18 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 460 | `items[].4_license.reference[].basis` | str | 21 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 461 | `items[].4_license.queries_emedi[].query` | str | 57 | 브론즈 | `bronze` | emedi 질의 로그 — 조사 과정 |
| 462 | `items[].4_license.queries_emedi[].total` | int | 57 | 브론즈 | `bronze` | emedi 질의 로그 — 조사 과정 |
| 463 | `items[].4_license.queries_emedi[].name_hits` | list(empty) | 43 | 브론즈 | `bronze` | 빈 배열 |
| 464 | `items[].4_license.reference[].cancel.code` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 465 | `items[].4_license.reference[].cancel.date` | str | 3 | 브론즈 | `bronze` | 참고 허가(연결되지 않은 후보 + why) — 판정 전 후보라 들이지 않음 |
| 466 | `items[].4_license.licenses[].name_en` | str | 9 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 467 | `items[].4_license.licenses[].holder_en` | str | 9 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 468 | `items[].4_license.licenses[].consign_manuf` | null/str | 9 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 469 | `items[].4_license.licenses[].induty_type` | str | 9 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 470 | `items[].4_license.licenses[].etc_otc` | str | 9 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 471 | `items[].4_license.licenses[].material` | str | 9 | 개체 | `product.licenses.*` | 허가 건 필드 — 키 이름 보존. source 가 `식약처.*API` 면 신뢰 2, 아니면 3 |
| 472 | `items[].5_spec.license_spec[].license_key` | str | 9 | 개체 | `product.spec.*` | 허가 키 기준 규격 — 키 이름 보존 |
| 473 | `items[].5_spec.license_spec[].pack_unit` | str | 9 | 개체 | `product.spec.*` | 허가 키 기준 규격 — 키 이름 보존 |
| 474 | `items[].5_spec.license_spec[].content` | str | 9 | 개체 | `product.spec.*` | 허가 키 기준 규격 — 키 이름 보존 |
| 475 | `items[].5_spec.license_spec[].basis` | str | 9 | 개체 | `product.spec.*` | 허가 키 기준 규격 — 키 이름 보존 |
| 476 | `items[].line_children[]` | str | 2 | 브론즈 | `bronze` | step1 식별자 설계(병합·이동·라인) — 들이지 않음 |
| 477 | `items[].4_license.queries_emedi[].name_hits[]` | str | 32 | 브론즈 | `bronze` | emedi 질의 로그 — 조사 과정 |
| 478 | `items[].4_license.history[].note` | str | 2 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 479 | `items[].4_license.history[].kpic.drug_code` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 480 | `items[].4_license.history[].kpic.drug_name` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 481 | `items[].4_license.history[].kpic.ingredient` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 482 | `items[].4_license.history[].kpic.company` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 483 | `items[].4_license.history[].kpic.class` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 484 | `items[].4_license.history[].kpic.atc` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 485 | `items[].4_license.history[].kpic.kpic_class` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 486 | `items[].4_license.history[].kpic.insurance` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 487 | `items[].4_license.history[].kpic.hira_code` | null | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 488 | `items[].4_license.history[].kpic.insurance_code_search` | null | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 489 | `items[].4_license.history[].kpic.source` | str | 2 | 개체 | `product.license_history.kpic.*` | 키 이름 보존 |
| 490 | `items[].taxonomy_product.id` | str | 15 | 브론즈 | `bronze` | step1 이 적어 둔 taxonomy 제품 대응 — 원장 대응은 B 분해 규칙으로만 하므로 쓰지 않는다(C) |
| 491 | `items[].taxonomy_product.name_en` | str | 15 | 브론즈 | `bronze` | step1 이 적어 둔 taxonomy 제품 대응 — 원장 대응은 B 분해 규칙으로만 하므로 쓰지 않는다(C) |
| 492 | `items[].taxonomy_product.manufacturer` | str | 15 | 브론즈 | `bronze` | step1 이 적어 둔 taxonomy 제품 대응 — 원장 대응은 B 분해 규칙으로만 하므로 쓰지 않는다(C) |
| 493 | `items[].taxonomy_product.country` | str | 15 | 브론즈 | `bronze` | step1 이 적어 둔 taxonomy 제품 대응 — 원장 대응은 B 분해 규칙으로만 하므로 쓰지 않는다(C) |
| 494 | `items[].taxonomy_product.mfds` | bool/null | 15 | 브론즈 | `bronze` | step1 이 적어 둔 taxonomy 제품 대응 — 원장 대응은 B 분해 규칙으로만 하므로 쓰지 않는다(C) |
| 495 | `items[].5_spec.license[]` | str | 2 | 개체 | `product.spec` | 문자열형 2 — 규격 문장 원문(③ 분해는 실버 빌더) |
| 496 | `items[].4_license.history[].state_raw` | str | 1 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 497 | `items[].4_license.history[].serial` | str | 1 | 개체 | `product.license_history.*` | 취소·취하 이력 허가 건 — 키 이름 보존. 신뢰 규칙은 licenses 와 같다 |
| 498 | `items[].5_spec` | null | 5 | 브론즈 | `bronze` | null 5 = 미입력 |
| 499 | `items[].7_site_use` | null | 5 | 브론즈 | `bronze` | null 5 |
## 검산 결과

### A. 잎 키 행선지 (원장 21 + step1 · 이동 표)

- PASS — 행선지 행 1072 = 원장 잎 키 573(=573) + step1 잎 키 499 = 1072 (=1,072)
- PASS — 중복 행 0
- PASS — 스캔에만 0 · 표에만 0
- PASS — 행선지 범주 밖/표적 없음(미정) 0
- 행선지 분포(전체): 개체 488 · 브론즈 365 · 사전 110 · 엣지 108 · 버림 1 (합 1072) · step1 만: 브론즈 353 · 개체 139 · 사전 6 · 엣지 1 (합 499)
- PASS — 표적이 ERD 에 정의되지 않은 행 0
- PASS — 이동 표 v1.1→v2 47 + v2.1→v2.2 3 + v2.2→v2.3 0 + v2.3→v2.4 0 + v2.4→v3 0 + v3→v3.1 29 = v1.1 표와 표적이 다른 행 51 (같은 집합)
- PASS — v3 표와 표적이 다른 행 29 = 이동 표 v3→v3.1 29 (고지 1 → clinical_rule.text · 표현 28 → dict:phrase_dictionary(사전) · 비고만 바뀐 행 36 전부 실제 잎 키)
- PASS — v2.4 표와 표적이 다른 행 29 = v3→v3.1 이동 29(v2.4→v3 이동 0 · v3 비고 변경 40)
- PASS — 브론즈 2판 잎 키 재스캔 573 = 1판 573 · 파일별 집합 차이 0 (전부 같다 — 2판은 이름 6곳만 바뀜)
- PASS — v2.3 표와 표적이 다른 행 29 = 이동 표 v2.3→v2.4 0 (이동 0 · v2.4 비고 변경 41)
- PASS — v2.2 표와 표적이 다른 행 29 = 이동 표 v2.2→v2.3 0 (이동 0 · 비고만 바뀐 행 30: 시술 축 참조 자리 16 + pih procedure_ref + timeline category + taxonomy safety 11 + complications name)
- PASS — v2.1 표와 표적이 다른 행 32 = 이동 표 v2.1→v2.2 3 (같은 집합 · verification_needed: decision.what→decision.reason, classification_issue: decision.what→decision.reason, correction_note: decision.what→decision.reason)
- PASS — procedure.* 행선지 0 (v1.1 procedure 행은 전부 catalog_item.* 로) · catalog_item 행 18 · adverse_expression 행 0 · adverse_effect.name 행 0

### B. 사전 값 출처

- PASS — 출처 없는 사전 값 0 / 정준값 2435 + 동의어 482
- PASS — 원장/step1 에서 확인 안 되는 출처 0
- PASS — 출처 kind=default 는 ['course:미상'] 하나뿐 (ERD 정의값)
- 사전 49개(값 사전 45 + 이름 색인 3 + 문구 색인 1) · 정준값 2435 · 동의어 482 · 후보 37 · 출처 100% 확인(문구 사전은 raw_variants 가 그 경로 값과 정규화 일치)

### C. ERD 출처 키·표적

- PASS — ERD 출처 키 595개 중 잎 키에 없는 것 0
- PASS — 행선지 표의 사전 28개 전부 사전 파일에 있음
- 개체 20 · 관계 31 · 사전 49 · 처분 19 · 결정 레코드 27

### D. 브론즈 바이트 (원장 21 + step1)

- PASS — 원장 21(브론즈 2판 bronze/phub-ledger) + step1 sha256 일치 (파일 22, 불일치 0) · HASHES.txt 21 과 접두 일치(불일치 0) · 판 2 기록
- PASS — 1판 대조: 바뀐 파일 ['treatment-optimization.json', 'treatment-sequence.json'] (CHANGELOG 6곳 = treatment-optimization 2 + treatment-sequence 4 · distinct 새 이름 5) · 1판 sha256 기록 일치 True
- PASS — step1 = research_artifact · 기본 3 · 허가 필드 조건부 2 (115/342 건)

### E. 분해 규칙 재현 (erd-v1.1-resolve.py 를 v2 사전으로 재실행)

- PASS — 자리 19개 (n·해결·분해 성공·미해결) 재현 불일치 0
- PASS — v1.1·v2 수치와 같음 — 2판에서 이름이 바뀐 treatment-optimization·treatment-sequence 자리와 부위 사전(v3 조직층 5)만 다를 수 있다(그 자리 차이 1 · 그 밖 불일치 0); 허용된 차이: 부위 사전 (뼈대 11 + 확장).n: v1.1 21 vs v2 26
- PASS — 합계 재현: 미해결 332 · 분해 성공·항목 없음 45 · 해결 178
- PASS — 규칙 데이터: 유사도 금지 · 사전 순서 제품→하위분류→분류 항목(procedure 자리 = catalog_item_name)→부위→규격→product_tier

### F. 처분 반영 (v1.1 그대로)

- PASS — 부위 사전 26 = 뼈대 11 + taxonomy 부위 라벨 10 + v3 조직층 5 · 확장 0 (공유 사전 유지)
- PASS — 기법 사전 12 = profiles[].mechanism[] distinct 12
- PASS — 처분 19 (사용자 4 · 워커 확정 15)
- PASS — complications.json 3 유지 + 「AI 컨센서스 추정」
- PASS — 질문 14 묶음 26: ① 11 · ② 15(범위 검토) · 미배정 0
- PASS — 8-2 처분 표 51 행 (v1 확장 51)

### G. 튜플·단위·문구·조건 실측 재현 (erd-v3.1-tuples.py 재실행)

- PASS — 요약 수치 재현 불일치 0 (erd-v3.1.json tuple_report · erd-v3.1-tuples.json 과 비교 · 세 축 · 목록형 키는 M/N 에서 따로)
- PASS — 튜플·단위·문구 항목 id 집합 재현 일치 (시술 598 · 부작용 단위 61 · 조건 단위 312 · 문구 항목 1218)
- PASS — 식별자 규칙 재계산 불일치 0 (v2.2: 세 칸 전부 사전 값이면 PRC-sha256(what_id|site_id|technique_id), 아니면 …|anchor · v3.1: ADV-sha256(event_id|site_id|qualifier_id · 없으면 none · 경과 없음) / raw_name 은 ADV-sha256(RAW:anchor|none|none|anchor) · anchor ⇔ raw_name · qualifier_id ⇔ qualifier)
- PASS — 분류 항목 521 (= taxonomy 항목 521) 전부 튜플 있음 (없는 것 0)
- PASS — 접힌 표 항목 합 521 = 521 + 부위 여럿 항목의 추가 튜플 0 · 튜플 521 = distinct 521 (521 → 521)
- PASS — complications 이름 65 전부 단위 있음 (없는 것 0) · 접힌 표에 등장하는 이름 65
- PASS — 튜플마다 원천(출처 이름·문구) ≥1
- PASS — technique_origin ∈ {fragment, none} · none ⇔ technique_id none (위반 0) — v2.1 항목 「상속 기법 = R5 단일 기법」은 v2.2 에서 「상속 0」(J-3)으로 바뀜 · 상속 불가 계열 ['M11', 'M15', 'M17', 'M3', 'M4', 'M5', 'M6', 'M8']
- PASS — what ∈ {modality, modality_subcategory, product, catalog_item(v2.1)} 위반 0 · site ∈ 부위 사전(anatomical·region) | none — layer 는 시술 site 칸에 없다(v3)
- PASS — 부작용 단위 site ∈ {site, none}(v3.1 상대 부위 없음) · qualifier ∈ 수식 사전 | none · event_kind ∈ {dict, raw_name} · status ∈ {complete, partial, unresolved} · dict 단위 event ∈ 사건 사전 · 경과 칸 없음
- 시술: 분류 항목 521 → 튜플 521 · 참조 ② 367 → 튜플 155 + combo_ref 0 + 미해결 199 + 불가 0 · ③ 122 → 튜플 16 + combo_ref 0 + 불가 0 · 전체 튜플 598 · site none 비율 0.973 · technique none 비율 1.0 · 미등록 조각 distinct 714
- 부작용: complications 65 → 단위 49(사전 35 + raw_name 14) · 사건 사전 40 · 문구 자리 3044 → 항목 1218 ({'unlinked': 1033, 'auto': 185}) · 전체 단위 61(문구가 세운 12) · 미등록 조각 distinct 1776 · 조건: 298 → 312 (kind 포함 299 → 312 · 사전 단위 96 + raw 216)

### H. 구조 변경 반영

- PASS — 개체 20 = v1.1 19 + catalog_item + adverse_expression − adverse_expression(v3.1 V3.1-10 · 문구는 부록)
- PASS — 관계 31 = v1.1 25 + R26~R31 − R29 + R32 (v3.1)
- PASS — 사전 49 = v3 47 + person_condition + phrase_dictionary
- PASS — v1.1 procedure 속성 15·출처 전부 catalog_item 에 있음 (빠진 속성 0 · 빠진 출처 0) · 식별자 규칙 동일
- PASS — procedure = 튜플(what_kind·what_id·site_id·technique_id)
- PASS — adverse_effect = 단위(event·site_ref·qualifier) · 문자열 name 식별자 없음 · 경과 칸 없음(v3.1)
- PASS — v1.1 adverse_effect.name 의 문구 출처 21개 전부 문구 사전 항목 출처에 있음 (빠진 것 0: [])
- PASS — target_depth = ['modality', 'subcategory', 'procedure', 'product'] (v2.3: catalog_item 은 끝이 아니다 — v2 항목 「catalog_item 추가」는 K-1 로 대체)
- PASS — package.kind 에 combo_ref
- PASS — 사건 사전 40 값마다 category ∈ 7 분류 · 출처 전부 complications.json 이름(derived) · 동의어 71
- PASS — 경과 사전 = ['미상', '영구', '일시', '재발', '지연']
- PASS — 상대 부위 사전 = ['시술 부위', '주사 부위']
- PASS — 시술 축 엣지 7(R3·R9·R12·R15·R16·R17·R18)에 v2.3 엣지 끝 규칙 기록(승격 규칙 0): ['R3', 'R9', 'R12', 'R15', 'R16', 'R17', 'R18'] — v2 항목 「승격 규칙」은 K-1 로 대체
- PASS — 결정 레코드 27 = 처분 19 + 구조 변경 2 + v2.1~v2.4 개정 4 + v3 개정 1 (이관 26 · J-6) + v3.1 개정 1

### I. v2.1 접힘 규칙 (v2.1 항목 유지 · v2.2 에서 바뀐 기대값은 항목 안에)

- PASS — 규칙 데이터: resolve_rules.step3_assemble.fallback_to_parent=False · tuple_rules.procedure.fallback_to_parent=False · tuple_rules.name=tuples_v3_1
- PASS — 부모 하위분류 fallback 항목 0 (v2: 464)
- PASS — 접힌 튜플(항목 ≥2) 0 전부 세 칸 사전 값(v2.2: site·technique none 도 불가) — 위반 0 · 접힌 항목 수 0 (v2.1: 튜플 3 · 항목 6)
- PASS — partial·ambiguous 항목이 섞인 접힌 튜플 0
- PASS — 미등록 조각 있는 항목 472 전부 what=항목 자신(CAT- id · partial · candidate_name = 미등록 조각 · anchor = CAT-) — 위반 0 · 항목 자신 what 477 (사유 {'unregistered': 472, 'no_primary': 2, 'multi_primary': 2, 'unusable_primary': 1})
- PASS — 항목 자신(CAT-) what 튜플 478 은 전부 항목 1개(접힘 0) — 위반 0
- PASS — 참조 ②③ 489: 미등록 조각 있음 ⇔ 미해결(unregistered) · 미해결은 튜플 없음 · 위반 0 · partial 튜플 0 · 미해결 ② 199 + ③ 106 = 305 (사유 ② {'unregistered': 196, 'multi_primary': 3} · ③ {'multi_primary': 9, 'unregistered': 97})
- PASS — 참조가 닿은 튜플 115 중 partial·ambiguous 인 것은 항목 자신(CAT-) 튜플뿐 (사전 값 what 인데 아닌 것 0)
- PASS — 미해결(사유 unregistered) 수 = v1.1 분해 규칙(§9.2 · stopwords 없음) 미해결 수 − stopwords 로 풀린 참조 4 — 자리별 불일치 0 (v2.2 는 그 위에 multi_*/unusable 미해결이 더해진다)
- PASS — 사전 49: v3 가 바꾼 셋(site · adverse_event_type · adverse_qualifier) 밖 46 개는 값·동의어·순서 = v2.4 · course 정준값 5·동의어 동일 · 뺀 동의어 []
- PASS — 구조 = v2.1 − adverse_expression − R29 + R32 (개체 20 · 관계 31 · 같은 키·순서)
- PASS — procedure.what_kind = ['modality', 'modality_subcategory', 'product', 'catalog_item'] · candidate_name 속성 · R27 → modality|modality_subcategory|product|catalog_item
- PASS — 521 → 521 (v2.1 518 · v2 110) · 접힌 표 항목 합 521
- PASS — 부작용 단위 ≠ v2.1·v2.2 (v2.3 수정 2·3 · v2.4 1·2·3 · v3.1 세 칸): 미등록 조각 있는 complications 이름 14 전부 raw_name 단위 하나씩 · 미등록 0 인 이름 51 은 사전 단위(붙지 않은 조각이 남으면 raw) — v2.3 65 → 58 / v3.1 65 → 49

### J. v2.2 수정 6건 (발주서 erd-v2.2-brief.md)

- PASS — J-1 미상 포함 튜플 접힘 0 — 미상 칸(site/technique none)이 있거나 what=CAT- 인 튜플 598 전부 anchor 하나 · 정규화 라벨 하나(같은 라벨 = ① 만 같은 튜플) · 위반 0 · 미상 포함 분류 항목 접힘 0 · 세 칸 전부 사전 값 튜플 0
- PASS — J-1 접힘 조건 문자 그대로 「세 칸 전부 사전 값일 때만」 — json fold_condition · tuple_rules.procedure.fold_condition/fold_rule · id_rule.procedure · md 16 곳
- PASS — J-1 v2.1 의 미상 칸 있는데 라벨이 합쳐진 튜플 18 (§9.5.2 분류 항목 3 + 참조) → v2.2 전부 갈라짐 18/18 · 분류 항목 접힘 3 → 0
- PASS — J-2 버린 조각 0 — 분류 항목 521 · 참조 489 의 extra_primaries/extra_sites 전부 실값(null 0) · 사전 값 what 인데 primary/site/technique 둘 이상 0 · 항목 자신 튜플은 조각 전부 extra 에 · 위반 0 · v2.1 규칙 8 삭제 True · 검토 사례 {'IPL 제모': 'unresolved:multi_primary', '사각턱 (수입)': 'unresolved:multi_primary', '사각턱 (국산)': 'unresolved:multi_primary'}
- PASS — J-3 상속 기법 0 (v2.1 inherited 247) · enum procedure.technique_origin=['fragment', 'none'] · tuple_rules.technique_inheritance=false · canonical_mapping 후보 9 계열 = R5 단일 기법 계열 ['M1', 'M10', 'M12', 'M13', 'M14', 'M16', 'M2', 'M7', 'M9']
- PASS — J-4 ④ 유지 + 기록 — 품질 규칙 ④ 에 「채택마다 conflict 레코드」(status=auto_resolved_by_trust · chosen_value · values[].trust_tier · rule_ref=④ · 뒤집기 conflict_override) · conflict.status=['open', 'auto_resolved_by_trust', 'resolved', 'dismissed'] · conflict 속성 rule_ref·chosen_value · §9.3 rule_ref 열 True
- PASS — J-5 decision kind 7 ['dictionary_add', 'tuple_assign', 'fold_approve', 'event_split', 'canonical_mapping', 'conflict_override', 'exclude'] 전부 enum·표(target/new_value 구조체 필드)·build_reads · kind 총 20 · 개체 속성 = 공통 필드 9 · 「빌드는 status=approved 인 결정만 읽는다(proposed·r…」 · 레코드 모양 위반 0 · 형태 위반 []
- PASS — J-6 기존 결정 26(v3) 전부 이관(id·kind·target·status 유지 · 누락/변경 0) · 이관 표 26 · approved 19(처분 19) · proposed ['20', '21', '22', '23', '24', '25', '26'](decided_by·decided_at null) · 신규 ['DEC-2026-11-05-27']
- PASS — J-7 course 문장 — tuple_rules.adverse.course(§1.5) = json course_rule(v2.3 문장 + v3.1 엣지 덧말) · 경과 사전 비고(§4) = v2.3 문장 · v3.1: adverse_effect 에 course 속성 없음 · R15.course 가 엣지 속성 · md 절별 {'§1.5': True, '§4': True, 'R15': True} · 사전 출처에 duration/incidence 0 (위반 0)

### K. v2.3 수정 7건 (발주서 erd-v2.3-brief.md)

- PASS — K-1 엣지 끝 분포 실측 존재 — 자리 30(텍스트 13 + 코드·레코드 16 · ③ 참고 1) · 관계 ['R3', 'R9', 'R12', 'R15', 'R16', 'R17', 'R18'] · 건 3423: {'procedure': 1891, 'modality': 953, 'subcategory': 62, 'product': 318, 'unresolved': 199} · 끝 종류 전부 ['procedure', 'modality', 'subcategory', 'product', 'unresolved'] 안 · 참조 결과 ⇔ 끝 종류 위반 0 · 코드 참조 node 9(튜플 0) · md §9.5.8 True
- PASS — K-2 파생 id(PRC-/ADV-/CFL-)를 target 으로 쓰는 결정 0 / 27 · kind 표 target 에 파생 id 0 / 20 · target 규칙(json decision_target_rule · §1.1) 금지 명시 · conflict.stable_key 속성
- PASS — K-3 적용 순서 표 존재 — ① dictionary_add/canonical_rename/dictionary_remove/phrase_map → ② canonical_mapping → ③ tuple_assign/tuple_assign_multi/adverse_tuple_assign → ④ fold_approve/event_split → ⑤ edge_create → ⑥ conflict_override/conflict_close → ⑦ exclude · 빌드 적용 kind 14 전부 한 번씩(reclassification·product_reclassify 는 ⓪) · 같은 단계 decided_at 순 · md §5.4 True
- PASS — K-4 결정 kind 20 = 12 + 4(edge_create, tuple_assign_multi, adverse_tuple_assign, conflict_close) + v3 1(canonical_rename) + v3.1 3(product_reclassify · dictionary_remove · phrase_map) · 구조체 필드 위반 [] · conflict.close_verdict enum · R30 은 edge_create 로만
- PASS — K-5 부작용 미등록 포함 접힘 0 — 접힌 단위 10 전부 사전 값·미등록 0(위반 0) · raw_name 단위 14 = 미등록·붙지 않은 조각 있는 이름(이름마다 하나 · anchor=locator · 위반 0) · 65 → 49(사전 35 + raw 14) · 문구 사전 항목 status 판정 위반 0(auto 185 · unlinked 1033) · md §9.6.6 True
- PASS — K-6 course 규칙 문장(사건에 바로 붙은 수식어만 · 사건 둘 이상이면 수식어 붙은 사건에만 · LOP 둘) — §1.5·§4·R15 · v3.1 경과는 엣지 속성(course_is_edge_attribute) · LOP 사전 분해 [[('통증', None, '미상', None), ('통증', None, '지연', None)]] · 미상 아닌 경과가 멤버 밖에서 온 단위·항목 0
- PASS — K-7 기법 잔재 표현 0 — json(technique.definition · procedure.technique_id/technique_origin 규칙 · procedure 정의 · tuple_rules.technique) 「상속」 0 · md §1~§9(§5.3 결정 레코드 원문 제외 · v3: 「상속」이 결정 문맥(V3-8 · canonical_mapping)에 쓰인 문장은 자동 상속 표현이 아니다) 「상속」 0 · technique_id 출처 = what_id 출처(이름 키 19) · mechanism[] 은 기법 사전(§4) 출처로만
- PASS — K-8 taxonomy safety 11 키 — R15 출처 47 에 포함 · 문구 사전 항목 출처에 전부 등장 · 11 키 전부 잎 키 존재 · R29 없음(v3.1)

### L. v2.4 수정 6건 (발주서 erd-v2.4-brief.md · 원칙 A~D)

- PASS — L-1 부위 상속 0(2-A′ · 원칙 B·C · v3.1 상대 부위 none) — 이름·문구 항목 1283 의 단위·후보 전수: 멤버 밖에서 온 site 0 · 부위 나열 합치기 1(구조 위반 0) · 후보 둘 이상 분할 3(위반 0) · 붙지 않은 조각 보존 203 문자열(이름→raw_name · 문구→unlinked 위반 0) · 상대 부위가 칸에 든 단위 0 · dict 단위 site_basis ∈ {member, site_list} · json site_rule=tuple_rules.adverse.site · md §1.5 부위 규칙 True · §9.6.2b True
- PASS — L-2 raw_name 칸 none/none 100%(2-B′ · v3.1 세 칸) — raw 단위 14: site none 14 · qualifier none 14 · 위반 0 · dict_tuples 보존 14 · LOP raw · 사전 분해 (통증, 미상)+(통증, 지연) 보존 True · 사유 {'unregistered': 10, 'unregistered+unattached_fragments': 4} · id_rule RAW:anchor|none|none · md §1.5·§9.6.2c True
- PASS — L-3 문구 유래 단위(v3.1 V3.1-9/10) — 문구가 세운 조합 12 = 단위 49 → 61 · 전부 세 칸 사전 값 · 미등록 조각 섞인 단위 0 · 후보 would_be_id/exists/auto⇔후보 위반 0 · raw 단위를 문구가 만든 것 0 · json expression_rule=tuple_rules.adverse.expressions(문구 사전 규칙) · md §1.5·§9.6.10 True
- PASS — L-4 §5.2 adverse_tuple_assign 대상 문구(v3.1) — 「raw_name 단위 전부」 · 문구는 phrase_map(target PHR-|normalized · new_value units·courses·status) · md §5.2 True
- PASS — L-5 CAT- 계열 코드 = taxonomy 트리 위치(3-B′) — json cat_family_rule · id_rule.catalog_item · catalog_item.identity · modality_subcategory 정의 · reclassification 비고 · tuple_rules.procedure.cat_family · md {'§1.4': True, '§2.3': True, '§2.4': True, '§5.2': True} · 실측: 분류 항목 521 전부 CAT- = sha256(트리 계열|이름) (위반 0) · reclassified_to 항목 1 도 트리 위치 True · 소프라노 티타늄 M9 · 볼뉴머 M4/M9 True
- PASS — L-6 site_id 출처(3-C′) — procedure.site_id 출처 19 = what_id 출처(v2.3 은 0) · 전부 잎 키 존재 · adverse_effect.site_ref_kind/site_ref_id 출처 = complications 이름 키 · md §2.5·§2.14 행에 「(파생/ERD 정의)」 없음
- PASS — L-7(v3.1) 개체·관계 구조 = v3 − adverse_expression − R29 + R32(개체 20 · 관계 31) · 사전 49 = 47 + person_condition + phrase_dictionary · 값 변경은 json values_changed_from_v3(N-11 이 전수 대조)
- PASS — L-8 원칙 A~C 문장 = 발주서 그대로 True · D = v3.1 문장(「미등록 조각이 섞인 단위를 만들지 않는다」) True · md §0·§1.5
- PASS — L-9 v2.3 규칙 유지 — 미등록 포함 접힘 0 · course_member_only True · site_member_only True · expressions_create_units all_dict_cells_only · raw 생성 False · 경과는 엣지 True
### M. v3 변경 10건 (발주서 erd-v3-brief.md · 각각 반영 여부 + 실측) + 브론즈 2판 + 사용자 정의 3·명시 예외

- PASS — M-1 V3-1 수식 칸(v3.1 세 칸 중 하나) — 사전 adverse_qualifier 5 · 사건 동의어 「공기색전」 v2.4 있음 → v3 제거(이력 removed_synonyms) · adverse_effect qualifier/qualifier_id/qualifier_basis/extra_qualifiers · id_rule 세 칸 · json qualifier_rule=tuple_rules.adverse.qualifier · 실측: 멤버 밖 수식 0 · raw qualifier none · 「공기색전」→ 공기+색전 True · qualifier≠none 단위 2 · md §9.6.7 True
- PASS — M-1′ v3 대조(정보) — 이름 유래 단위 v3 57 → v3.1 49(경과·상대 부위가 칸에서 나가 접힘이 늘었다) · 표현 2807 자리의 전이 {'unlinked→unlinked': 1509, 'unlinked→auto': 647, 'exact→auto': 651} · 단위 57 → 61
- PASS — M-2 V3-2 괄호 안 회사·제품 — 규칙 데이터 resolve_rules.company_paren=tuple_rules.procedure.company_paren · 후보 전수 241(회사 닿음 0 · 제품 닿음 2 · 안 닿음 239) · 「보톡스(엘러간)」·「더모톡신」 자리 9 전부 사전에 안 닿음(엘≠앨) · 적용 2 = what_basis company_paren 인 항목·참조 2 · md §9.5.9
- PASS — M-3 V3-3 stopwords — 규칙 데이터 단어 19(발주서 12 전부 + 원장 실측 7) · locator 없는 단어 0 · 사전 값과 겹침 0 · 미등록 조각에 새어 나온 stopword 0 · 전후 distinct 731→714 · 총 1016→984 · R12 session_index/qualifier_text · R9/R17/R18 qualifier_text · md §9.5.10
- PASS — M-4 V3-4 조합 기호 — 규칙 데이터 resolve_rules.step3_assemble.combo=tuple_rules.procedure.combo · R12 member_mode(enum and|or) · 실측 `+`/`/` 라벨 전수 66(treatment-optimization·sequence 의 `/` 23 ≥ 12 · 2판 `+` 4곳 전부 1판 이름 대조) · 「무엇을 하나 × 부위 여럿」 4(구조 위반 0 · 엣지 끝 multi_tuple 4) · 괄호 안 대안 3(위반 0) · combo_ref member_mode 없음 0 · 기호가 있는데 multi_site 로 남은 참조 0 · md §9.5.11
- PASS — M-5 V3-5 부위 kind — site 26 = v2.4 21(값·순서 그대로 True) + layer 5(피부, 피하 지방층, 근육, 혈관, 점막 · 출처 derived True) · 값마다 kind ∈ 4 True(분포 {'anatomical': 20, 'region': 1, 'layer': 5}) · site.kind 속성 · enum · relative_site 2 불변 · 시술 site 칸의 layer 0 · 부작용 layer 튜플 3 · 문구 후보 15 · md §9.6.8
- PASS — M-6 V3-6 canonical_rename — kind 20(v3 신설 1) · build_reads · target(dictionary·code·canonical) · new_value(canonical·old_as_synonym·is_marketing_name) · 적용 ① ['dictionary_add', 'canonical_rename', 'dictionary_remove', 'phrase_map'] · md §5.2
- PASS — M-7 V3-7 description·media_refs — product·technique 속성(출처 locator 필수 · path·sha256·captured_at·source·kind) · enum media_refs.kind · md §2.6(product)·§2.7(technique)
- PASS — M-8 V3-8 기법 상속 하위분류 단위 — R5 from modality|modality_subcategory · basis · 후보 9 계열 전부 하위분류별 scope(항목 수 합 일치) · M16 수액(R5 기법 intravenous 하나 · 하위분류 7 — 하위분류별 지정 자리) · R5 기법 둘 이상·없음 계열 ['M11', 'M15', 'M17', 'M3', 'M4', 'M5', 'M6', 'M8'] · md §9.5.6
- PASS — M-9 V3-9 결정 적용 대상 확장 — tuple_assign·tuple_assign_multi·adverse_tuple_assign 비고 · target 규칙(미해결·조합 REF-) · 빌더 규칙 문장(anchor 부재로 거부하지 않는다) · md §5
- PASS — M-10 V3-10 fold_approve 가 ⑦ 을 닫는다 — 규칙 ⑦ 문장 · fold_approve 비고 · conflict.status 비고 · fold_close_rule · md §5
- PASS — M-11 사전 값 변경은 셋뿐(v2.4 → v3) — v2.4 46 사전 중 site·adverse_event_type 밖 44 개 값·동의어·후보 동일 True · site 앞 21 동일 True(+layer 5) · 사건 사전 동일 True(색전 동의어 차이 ['공기색전']) · 새 사전 ['adverse_qualifier', 'person_condition', 'phrase_dictionary'](v3 adverse_qualifier + v3.1 person_condition·phrase_dictionary)
- PASS — M-12 사용자 정의 3 과 명시 예외 유지 — 정의 3 문장 = ERD-FROZEN 동결 조건 문장 True · 명시 예외 문장 = ERD-FROZEN(v3 덧말 제외) · json user_definitions·explicit_exception·tuple_rules 에 같은 문장 · 부작용 none·미상·qualifier none 은 값(tuples.json qualifier_none_is_value) · md §0
- PASS — M-13 브론즈 2판 — HASHES.txt 불일치 0 · 2판 잎 키 573 = 1판 573 · 파일별 차이 0 · 바뀐 파일 ['treatment-optimization.json', 'treatment-sequence.json']

### N. v3.1 변경 10건 (발주서 erd-v3.1-brief.md 6건 + 코디·사용자 추가 4건 · 각각 반영 여부 + 실측) + 열거기 호환 + 사전 불변 + 사용자 정의

- PASS — N-1 V3.1-1 product_reclassify — kind(build_reads · 적용 ⓪ · target product_id|product · new_value to_modality_code) · product.reclassified_from · id_rule.product 재계산+alias · R4 이동·제품 끝 엣지 규칙 문장 · 실측 §9.7.1 대상 예 2(id 재계산 일치 True) · md §5
- PASS — N-2 V3.1-2 R32 rule_applies_to — from clinical_rule · to product|technique|proc_axis · 속성 scope·severity·source_locator·decision_id·basis · enum · clinical_rule kind +product_note · edge_create 비고 · 출처 후보 전수 §9.7.2 14(제품 note·legal_warning·regulatory_status · 「주사 금지」 문장 포함 True)
- PASS — N-3 V3.1-3 dictionary_remove — kind(target dictionary·canonical·synonym? · new_value removed) · ① 순서 ['dictionary_add', 'canonical_rename', 'dictionary_remove', 'phrase_map'] · 사전 49 전부 removed_synonyms/removed_entries 필드 · 「공기색전」 이력 1(정준값 색전 · by ERD v3(V3-1)) · 값 제거 거부 규칙(in_use)
- PASS — N-4 V3.1-4 조건 사전 — 사전 person_condition 98(출처 derived 100% True) · 표지어 14(locator 전부) · 실측 원장 자리 471 · 이름 298(kind 포함 299) → **단위 312**(사전 96 + raw 216) · 완전 일치 이름 83 · raw 이름 216 · 단위 id 규칙(kind|정준값 · RAW:kind|원문) 위반 0 · 문장 부록 471(위반 0 · 단위 phrases 합 529) · 접힌 표 = 단위 전부 True · R16/R17/R18 source_phrases · 문장이 세운 단위 0 · md §9.7.0 True
- PASS — N-5 V3.1-5 회·차 자리 — R12 session_count·session_index · R9/R17/R18 qualifier_text 비고 · resolve_rules 「회 → count」 문장 교체 · 실측 규격 토큰 14(회 6 · 차 8) → R12.session_index 8 · R12.session_count 3 · qualifier_text 3 · 자리 규칙 위반 0 · md §9.5.12
- PASS — N-6 V3.1-6 stopwords 겹침 — 규칙 문장(통째 일치 먼저 · 조각에만) · 겹침 목록(사전 49 전수 재계산 = 규칙 데이터) ['관리'] · 분해 사전 7 겹침 0 · v3 「겹치는 단어 없다」 문장 삭제 · md §9.5.13
- PASS — N-7 V3.1-7 필수 고지 — modality.mandatory_disclosures 삭제 · clinical_rule(disclosure · text 출처 · phrase_ids) · R32 basis=ledger(출처) · R15 disclosure · column-map 이동 · 실측 §9.8 고지 109(계열 17) → clinical_rule 109 · 문구 항목 109(auto 0 · unlinked 109 · 세운 단위 0) · 동의서 뷰 = 골드 한 줄
- PASS — N-8 V3.1-8 안전 문구 수식어 — 단어 138(class 별 {'degree': 25, 'timing': 29, 'incidence': 9, 'condition': 18, 'connector': 7, 'misc': 50}) 전부 v3 미등록 조각 빈도 ≥4(위반 []) · locator 없는 단어 0 · 패턴 5(locator 없음 0) · class 유효 True · 조각 분류 전수 6222 토큰 = class 합 · 분류 밖 0 · 미등록 조각에 새어 나온 수식어 0 · 미등록 총 v3 5596 → 4189 · 수식어는 속성에 보존(버리지 않음) · md §9.6.9
- PASS — N-9 V3.1-9 단위 (사건, 부위, 물질) — 사전 단위 47 전부 세 칸 사전 값(부위 anatomical·layer·region|none · 물질|none · 경과 칸 없음 · 위반 0) · id 고유 True · 문구가 세운 단위 위반 0 · R15 엣지 1342 의 경과 247 전부 경과 사전 값이고 **그 단위의 사건 멤버에 붙은 경과(후보 courses · 원칙 C · S-1)** 에서만 온다(멤버 수준 위반 0 · 밖 0 · 「주사 부위 일시적 부종 및 멍」의 멍 엣지 경과 null True) · 상대 부위 none 단위 10 · 조합 하나뿐인 사건 31/38(부종 2) · §0 정의 2 개정 문장·명시 예외 개정 문장 · R15.course · adverse_effect 경과 속성 없음
- PASS — N-10 V3.1-10 문구 사전 — 항목 1218(id = PHR-sha256(정규화형) · status 위반 0 · auto 185 · unlinked 1033) · 결정 kind phrase_map(① · target PHR-|normalized · new_value units) · **부록 합 1298 + 0 + 1637 = 2935 = 문구 자리 2935(= v3 표현 2,807 + 환자 설명 128(ko 항목 32 + 번역 96) = 2,935) True** · auto 단위 전부 실재 True · adverse_expression 개체 없음 · R29 없음 · 열거기 호환 enum 키 유지 True · evidence_statement 유지 · md §9.6.3·§9.6.12
- PASS — N-11 사전 값 불변(v3 → v3.1) — v3 47 사전 값·동의어·후보 동일 True · 새 사전 ['person_condition', 'phrase_dictionary'](값은 분해 결과·조건 핵심 · 기존 값 변경 0)
- PASS — N-12 사용자 정의 — 동결 원문 3 = ERD-FROZEN True · v3.1 문장(정의 1 그대로 · 정의 2 개정 · 정의 3 kind 20·⓪①) · 명시 예외 개정(부위 none · 물질 none 은 값) · 개정 사유 문장 · md §0
- PASS — N-13 적합성 열거기(silver-v3/tests/enumerate_cases.py · 읽기만)가 erd-v3.1.json·사전을 읽는다 — 경우 2514 · 새 kind·단계 경우 전부 있음(빠짐 []) · ref:R32 60(accept 12) · ref:R29 0 · R16 끝 dict_value:person_condition accept True

**종합: PASS** (NOTE 0) — 잎 키 1072/1072 행선지 확정(미정 0 · v3 대비 이동 29 · 비고 변경 36) · 사전 값 출처 100% · ERD 출처 키 100% · 브론즈 2판 sha256 21 + HASHES.txt + step1 일치 · 분해 규칙 재현 일치 · 튜플·단위·문구·조건 실측 재현 일치 · 구조 = v3 − adverse_expression − R29 + R32 · v2.1~v3 항목 유지(기대값 갱신) · v3.1 10건 각각 반영·실측(product_reclassify · R32 · dictionary_remove · 조건 사전 298 → 312 · 회·차 · 겹침 · 고지 · 수식어 · 단위 세 칸 · 문구 사전 부록 합) · 사전 값 불변 · 사용자 정의 1·3·명시 예외 논리 유지 · 정의 2 개정 문장
