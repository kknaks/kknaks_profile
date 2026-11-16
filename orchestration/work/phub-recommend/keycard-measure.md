# keycard 측정 — v6a case3 정확성 실패 진단(스펙 작성 안 함 · 코디 11-01)

> `keycard-measure.py` · `keycard-diagnose.py`(읽기만 · 결정론) · 골드 `567677edfe7123e9` · rerun-v6a `b202611011935-f9a211` case3 · 판정 = recheck2 `gold_match`(fact hit) ∩ 받은 fact(walk.fact_ids ∪ required ∪ full). 원장 인용 없음(fact id · 경로 · 셈만).

## 1. 분류

| 분류 | 행 |
|---|---|
| 걷기가 받음(답이 안 씀) | 4 |
| 골드 fact 없음 | 2 |
| 골드에 있는데 못 받음 | 61 |
| 합 | 67 |

- 코디 셈(65 · 받았는데 안 씀 0 · 못 받음 45)은 키워드 기준이었고 이 셈과 식이 다르다(코디 확인 11-01 — 이 셈이 맞음)

## 2. 핵심 수치 카드로 닿는가(스펙 멈춤의 근거)

- 카드 = 시술 노드마다 칸 8(onset · duration · downtime · interval · sessions · price_range · anesthesia · pain) · 칸당 fact 1(자기 → 계열 · 9단계 먼저) · 카드 노드 = 그 판의 필수 묶음 노드(rank 상위 3) ∪ 시작 노드
- 「골드에 있는데 못 받음」 61 중 **카드로 닿음 4**(칸: duration 3 · pain 1) · 상한(칸 후보 fact 전부 · 자기 + 계열) **8** · 핵심 수치 칸에 해당하는 fact 자체가 10행뿐
- 카드 크기(전 시술 노드 543 · 줄 80자): 중앙 1,200B · p95 1,555 · 최대 1,803 — ≤ 1KB 면 줄 40자로 줄여야 함

## 3. 못 받은 61행 — 무엇을 못 받았나

### section

| section | 행 |
|---|---|
| evidence | 18 |
| overview | 11 |
| recovery | 7 |
| safety.pih | 7 |
| disclosure | 4 |
| checks | 3 |
| safety.management | 2 |
| safety.side_effects | 2 |
| market | 2 |
| products | 1 |
| site_caution | 1 |
| aftercare | 1 |
| emergency | 1 |
| method | 1 |

### fact 를 가진 노드 종류(owner)

| 종류 | 행 |
|---|---|
| family | 21 |
| unit_procedure | 12 |
| combo | 10 |
| product | 5 |
| procedure_relation | 5 |
| check_condition | 3 |
| scope | 3 |
| site_caution | 1 |
| product_family | 1 |

## 4. 왜 못 받았나(걸음 기록 대조)

| 진단 | 행 |
|---|---|
| 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 29 |
| 안 방문 · 시작에서 1홉 | 13 |
| 안 방문 · 시작에서 2홉 | 11 |
| 방문 · section 받음 · 1쪽 밖(more) | 4 |
| 안 방문 · 6홉 밖 · 연결 없음 | 4 |

- 「방문」 = fact 를 내는 노드(owner · attached_to · 계열 fact 면 그 계열 단위 시술 · 엣지 · 조합이면 양끝 · 구성)가 걸음 노드 또는 필수 묶음 노드 · 「peek 엔 떴음」 = 그 노드에 그 section fact 가 있으므로 peek `sections[]` 에 나옴 · 「1쪽 밖」 = 그 section 을 받았는데 12줄 밖

### section × 진단

| section | 진단 | 행 |
|---|---|---|
| evidence | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 8 |
| evidence | 안 방문 | 7 |
| overview | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 6 |
| overview | 안 방문 | 5 |
| recovery | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 5 |
| safety.pih | 안 방문 | 5 |
| checks | 안 방문 | 3 |
| disclosure | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 3 |
| evidence | 방문 · section 받음 | 3 |
| market | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 2 |
| safety.management | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 2 |
| safety.pih | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 2 |
| aftercare | 안 방문 | 1 |
| disclosure | 안 방문 | 1 |
| emergency | 안 방문 | 1 |
| method | 안 방문 | 1 |
| products | 안 방문 | 1 |
| recovery | 방문 · section 받음 | 1 |
| recovery | 안 방문 | 1 |
| safety.side_effects | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | 1 |
| safety.side_effects | 안 방문 | 1 |
| site_caution | 안 방문 | 1 |

## 5. 행 목록

| 문항 | 원장 경로 | fact | section | 노드 | 진단 | 시작 노드 | 의도 | 멈춤 |
|---|---|---|---|---|---|---|---|---|
| Q001 | `patient-education.categories[0].duration_simple` | `family:M1#recovery#family_text[환자 설명 가이드(patient-education)][0].durati` | recovery | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | unit_procedure:U5-001 | I-01 | steps |
| Q002 | `extracted.M7.indications.primary` | `family:M7#overview#step9[taxonomy.modality[6].extracted.indications.pr` | overview | family | 안 방문 · 시작에서 2홉 | concern:auto-83-1774737181584 | I-01 | steps |
| Q003 | `extracted.M7.onset_duration.duration` | `family:M7#recovery#step9[taxonomy.modality[6].extracted.onset_duration` | recovery | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | site:site.jawline | I-01 | steps |
| Q005 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | `unit_procedure:U5-010#recovery#step9[taxonomy.modality[0].subcategorie` | recovery | unit_procedure | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | site:site.axilla | I-01 | steps |
| Q008 | `extracted.M8.indications.primary[0]` | `family:M8#overview#step9[taxonomy.modality[7].extracted.indications.pr` | overview | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-09 | steps |
| Q009 | `taxonomy.modality[8].subcategories[3].items[0].extracted.onset_duration.duration` | `product:auto-40-1774737181584#recovery#step9[taxonomy.modality[8].subc` | recovery | product | 방문 · section 받음 · 1쪽 밖(more) | product:auto-40-1774737181584 | I-02 | enough |
| Q017 | `taxonomy.modality[8].subcategories[3].items[0].name` | `product:auto-40-1774737181584#products#2_names.display_name` | products | product | 안 방문 · 시작에서 2홉 | family:M2 | I-07 | steps |
| Q018 | `contraindications.rules[0]` | `R8-0001#reason` | evidence | procedure_relation | 방문 · section 받음 · 1쪽 밖(more) | family:M1 | I-07 | steps |
| Q020 | `contraindications.rules[3].interval` | `R8-0004` | evidence | procedure_relation | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | product:auto-40-1774737181584 | I-08 | steps |
| Q025 | `problem-combos.combos[0].packages[2].expectedResult` | `combo:RC-PC-P1-3#evidence#effect.expectedResult` | evidence | combo | 안 방문 · 6홉 밖 · 연결 없음 | None | I-11 | None |
| Q026 | `problem-combos.combos[4].packages[1].expectedResult` | `combo:RC-PC-P5-2#evidence#effect.expectedResult` | evidence | combo | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | concern:P5 | I-11 | steps |
| Q028 | `problem-combos.combos[1].packages[0].clinicalRationale` | `combo:RC-PC-P2-1#evidence#effect.clinicalRationale` | evidence | combo | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | concern:P2-1 | I-01 | steps |
| Q031 | `combo-recipes.recipes[5].repeatCycle` | `combo:RC-RE-R2#evidence#effect.repeatCycle` | evidence | combo | 안 방문 · 시작에서 1홉 | product:M1-2-1 | I-05 | empty |
| Q035 | `complications.categories[0].complications[1].management` | `SE-M1-02#management` | safety.management | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | product:M1-2-1 | I-04 | enough |
| Q039 | `products.skin_booster.products[3].note` | `unit_procedure:U5-009#overview#step9[taxonomy.modality[3].products[3].` | overview | unit_procedure | 안 방문 · 시작에서 1홉 | product:M1-2-1 | I-06 | steps |
| Q043 | `anatomy-danger-zones.zones[5].botox_specific.key_warning` | `site_caution:SC-nasolabial-M1#site_caution#spec.key_warning` | site_caution | site_caution | 안 방문 · 시작에서 1홉 | family:M2 | I-01 | steps |
| Q046 | `complications.categories[1].complications[2].mechanism` | `SE-M2-03#mechanism` | safety.side_effects | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M2 | I-02 | empty |
| Q047 | `complications.categories[1].complications[0].management` | `SE-M2-01#management` | safety.management | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M2 | I-05 | enough |
| Q054 | `extracted.M2.onset_duration.duration` | `family:M2#recovery#step9[taxonomy.modality[1].extracted.onset_duration` | recovery | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M2 | I-06 | steps |
| Q058 | `patient-education.categories[3].pain_level` | `family:M4#overview#family_text[환자 설명 가이드(patient-education)][0].pain_l` | overview | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | product:M4-1-1 | I-04 | steps |
| Q064 | `synergy.links[31].timing` | `R8-0059` | evidence | procedure_relation | 방문 · section 받음 · 1쪽 밖(more) | family:M4 | I-07 | steps |
| Q067 | `market-pricing.categories[2].items[4].name` | `unit_procedure:U5-090#market#market[3]` | market | unit_procedure | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | product:M3-4-1 | I-06 | enough |
| Q072 | `pih-risk.procedures[15].name` | `unit_procedure:U5-103#safety.pih#pih[0].source` | safety.pih | unit_procedure | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | product:M9-1-1 | I-06 | steps |
| Q081 | `patient-education.categories[6].duration_simple` | `family:M7#recovery#family_text[환자 설명 가이드(patient-education)][0].durati` | recovery | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M7 | I-06 | steps |
| Q082 | `synergy.links[100].timing` | `R8-0028` | evidence | procedure_relation | 안 방문 · 6홉 밖 · 연결 없음 | None | I-07 | None |
| Q083 | `procedure-comparison.comparisons[0].procedures[1].limitations` | `combo:RC-CP-lifting#evidence#members[1].attrs_text.limitations` | evidence | combo | 방문 · section 받음 · 1쪽 밖(more) | family:M9 | I-10 | steps |
| Q084 | `synergy.links[100]` | `R8-0128#reason` | evidence | procedure_relation | 안 방문 · 6홉 밖 · 연결 없음 | None | I-07 | None |
| Q088 | `market-pricing.categories[10].items[5].name` | `unit_procedure:U5-110#market#market[5]` | market | unit_procedure | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | concern:P7 | I-05 | steps |
| Q094 | `consent-checklist.categories[10].mandatory_disclosures[5]` | `family:M11#disclosure#family_text[필수 고지(consent mandatory_disclosures)` | disclosure | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M11 | I-03 | enough |
| Q095 | `taxonomy.modality[10].subcategories[0].items[7].extracted.aftercare[2]` | `product:auto-M11-1775360637715#aftercare#extracted[auto-M11-1775360637` | aftercare | product | 안 방문 · 시작에서 1홉 | family:M11 | I-03 | steps |
| Q097 | `problem-combos.combos[6].packages[1].riskBenefit` | `combo:RC-PC-P9-2#evidence#effect.riskBenefit` | evidence | combo | 안 방문 · 시작에서 1홉 | family:M11 | I-07 | steps |
| Q099 | `extracted.M12.contraindications.absolute[3]` | `K8-0253` | checks | check_condition | 안 방문 · 시작에서 2홉 | concern:P9-2 | I-09 | steps |
| Q103 | `procedure-comparison.comparisons[4].procedures[1].limitations` | `combo:RC-CP-pigment#evidence#members[1].attrs_text.limitations` | evidence | combo | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-05 | steps |
| Q104 | `treatment-optimization.combination_rules[4].detail` | `scope:all#evidence#step8_notes[45]` | evidence | scope | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | technique:K04a | I-10 | steps |
| Q106 | `problem-packages.problems[13].complaints[0].cc_detail` | `unit_procedure:U5-131#overview#step9[problem-packages.problems[13].com` | overview | unit_procedure | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-06 | steps |
| Q108 | `pih-risk.procedures[3].prevention` | `pih[3]` | safety.pih | product | 안 방문 · 시작에서 1홉 | family:M8 | I-09 | steps |
| Q113 | `pih-risk.procedures[2].fitzpatrick_note` | `unit_procedure:U5-023#safety.pih#pih[2].fitzpatrick_note` | safety.pih | unit_procedure | 안 방문 · 시작에서 1홉 | family:M8 | I-06 | steps |
| Q115 | `consent-checklist.categories[7].mandatory_disclosures[4]` | `family:M8#disclosure#family_text[필수 고지(consent mandatory_disclosures)]` | disclosure | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-04 | steps |
| Q117 | `problem-packages.problems[5].complaints[0].alternatives[0]` | `unit_procedure:U5-009#overview#step9[problem-packages.problems[5].comp` | overview | unit_procedure | 안 방문 · 시작에서 2홉 | concern:P6 | I-11 | steps |
| Q121 | `literature-evidence.categories.M8.effects[0].patient_ko` | `ST-M8-effects-01#patient.ko` | overview | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-01 | steps |
| Q123 | `problem-packages.problems[8].complaints[6].cc_group` | `chemical-peel-mid#phases[3].emergency[0]` | emergency | family | 안 방문 · 시작에서 1홉 | concern:P8-1 | I-07 | steps |
| Q125 | `consent-checklist.categories[7].mandatory_disclosures[3]` | `family:M8#disclosure#family_text[필수 고지(consent mandatory_disclosures)]` | disclosure | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-04 | steps |
| Q127 | `problem-combos.combos[6].packages[0].expectedResult` | `combo:RC-PC-P9-1#evidence#effect.expectedResult` | evidence | combo | 안 방문 · 시작에서 1홉 | family:M8 | I-10 | steps |
| Q129 | `pih-risk.procedures[10].fitzpatrick_note` | `unit_procedure:U5-141#safety.pih#pih[0].fitzpatrick_note` | safety.pih | unit_procedure | 안 방문 · 시작에서 1홉 | family:M8 | I-03 | steps |
| Q130 | `extracted.M11.overview` | `family:M11#overview#step9[taxonomy.modality[10].extracted.overview]` | overview | family | 안 방문 · 시작에서 2홉 | concern:P8-1 | I-04 | steps |
| Q133 | `extracted.M2.indications.primary[2]` | `family:M2#overview#step9[taxonomy.modality[1].extracted.indications.pr` | overview | family | 안 방문 · 시작에서 2홉 | concern:P9 | I-06 | steps |
| Q134 | `consent-checklist.categories[7].contraindications[2]` | `K8-0182` | checks | check_condition | 안 방문 · 시작에서 2홉 | technique:K04b | I-06 | steps |
| Q137 | `problem-combos.combos[6].packages[0].expectedResult` | `combo:RC-PC-P9-1#evidence#effect.expectedResult` | evidence | combo | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-10 | steps |
| Q138 | `procedure-comparison.comparisons[3].evidence_notes[1]` | `combo:RC-CP-skin_texture#evidence#evidence_notes[1]` | evidence | combo | 안 방문 · 시작에서 1홉 | family:M8 | I-09 | steps |
| Q139 | `pih-risk.procedures[4].name` | `unit_procedure:U5-028#safety.pih#pih[0].source` | safety.pih | unit_procedure | 안 방문 · 6홉 밖 · 연결 없음 | None | I-07 | None |
| Q141 | `extracted.M8.contraindications.absolute[2]` | `K8-0291` | checks | check_condition | 안 방문 · 시작에서 2홉 | concern:P9 | I-09 | steps |
| Q147 | `procedure-comparison.comparisons[5].procedures[0].name` | `product_family:000137#overview#basis` | overview | product_family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-05 | enough |
| Q148 | `problem-packages.problems[9].complaints[0].combos[0].evidence` | `scope:all#evidence#step8_notes[191]` | evidence | scope | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M8 | I-05 | enough |
| Q150 | `pih-risk.procedures[12].fitzpatrick_note` | `unit_procedure:U5-023#safety.pih#pih[3].fitzpatrick_note` | safety.pih | unit_procedure | 안 방문 · 시작에서 2홉 | concern:P10 | I-09 | steps |
| Q155 | `consent-checklist.categories[7].mandatory_disclosures[2]` | `family:M8#disclosure#family_text[필수 고지(consent mandatory_disclosures)]` | disclosure | family | 안 방문 · 시작에서 1홉 | concern:P10 | I-03 | empty |
| Q159 | `problem-packages.problems[9].complaints[3].combos[0].evidence` | `scope:all#evidence#step8_notes[194]` | evidence | scope | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | concern:P10 | I-10 | steps |
| Q160 | `taxonomy.modality[7].subcategories[4].items[12].extracted.safety.common[1]` | `product:auto-M8-1775364775126#safety.side_effects#extracted[auto-M8-17` | safety.side_effects | product | 안 방문 · 시작에서 2홉 | concern:P10 | I-04 | steps |
| Q161 | `pre-procedure-checklist.category_specific[9]` | `family:M14#method#step9[taxonomy.modality[13].extracted.related_techni` | method | family | 안 방문 · 시작에서 1홉 | check_condition:C-PREG | I-09 | steps |
| Q164 | `patient-education.categories[14].downtime` | `family:M15#recovery#family_text[환자 설명 가이드(patient-education)][0].downt` | recovery | family | 안 방문 · 시작에서 2홉 | family:M2 | I-05 | steps |
| Q166 | `pih-risk.procedures[23].prevention` | `pih[23]` | safety.pih | unit_procedure | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | family:M15 | I-03 | steps |
| Q168 | `extracted.M15.overview` | `family:M15#overview#step9[taxonomy.modality[14].extracted.overview]` | overview | family | 방문 · Jev 가 그 section 안 고름(peek 엔 떴음) | concern:P6 | I-09 | steps |

