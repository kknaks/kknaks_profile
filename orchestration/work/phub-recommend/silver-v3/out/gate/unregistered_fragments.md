# 미등록 조각(⑧ unregistered_value)

총 480 행(축별 distinct 조각 하나 = 행 하나 · 사전 밖 값 포함). 축 후보 = 사전 46 정규화 완전 일치만(근거 포인터) — 추정 없음.

## dict:accuracy_rubric (1 · 총 1)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | 95-100=교과서 consensus, 85-94=주류 표준, 70-84=뉘앙스 보정, 50-69=근거 약함, 0-49=부정확 | 1 | literature-evidence.json:accuracy_summary.rubric×1 | — | — |

## dict:country (2 · 총 2)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | - | 1 | products.json:skin_booster.products[].country×1 | — | — |
| 2 | - | 1 | taxonomy.json:modality[].products[].country×1 | — | — |

## dict:manufacturer (2 · 총 2)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | - | 1 | products.json:skin_booster.products[].manufacturer×1 | — | — |
| 2 | - | 1 | taxonomy.json:modality[].products[].manufacturer×1 | — | — |

## dict:modality (2 · 총 2)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | PRP/엑소좀 | 1 | market-pricing.json:categories[].name×1 | — | — |
| 2 | PRP/엑소좀 | 1 | procedure-profiles.json:profiles[].name×1 | — | — |

## dict:pih_risk_level (5 · 총 5)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | 1-5% | 1 | pih-risk.json:risk_levels.low×1 | — | — |
| 2 | 15-30% | 1 | pih-risk.json:risk_levels.high×1 | — | — |
| 3 | 5-15% | 1 | pih-risk.json:risk_levels.moderate×1 | — | — |
| 4 | < 1% | 1 | pih-risk.json:risk_levels.very_low×1 | — | — |
| 5 | > 30% | 1 | pih-risk.json:risk_levels.very_high×1 | — | — |

## dict:problem (7 · 총 7)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | Acne / Acne Scars | 1 | treatment-optimization.json:by_concern[].concern_en×1 | — | — |
| 2 | Body Contouring | 1 | treatment-optimization.json:by_concern[].concern_en×1 | — | — |
| 3 | Pigmentation / Melasma | 1 | treatment-optimization.json:by_concern[].concern_en×1 | — | — |
| 4 | Sagging / Elasticity | 1 | treatment-optimization.json:by_concern[].concern_en×1 | — | — |
| 5 | Skin Texture / Pores | 1 | treatment-optimization.json:by_concern[].concern_en×1 | — | — |
| 6 | Volume Loss | 1 | treatment-optimization.json:by_concern[].concern_en×1 | — | — |
| 7 | Wrinkle Reduction | 1 | treatment-optimization.json:by_concern[].concern_en×1 | — | — |

## dict:reaction_level (4 · 총 4)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | 응급 반응 -- 즉시 응급실/클리닉 | 1 | post-procedure-timeline.json:reaction_levels.emergency×1 | — | — |
| 2 | 이상 반응 -- 모니터링 필요, 경과 관찰 | 1 | post-procedure-timeline.json:reaction_levels.abnormal×1 | — | — |
| 3 | 정상 반응 -- 예상 범위, 조치 불필요 | 1 | post-procedure-timeline.json:reaction_levels.normal×1 | — | — |
| 4 | 주의 반응 -- 24-48시간 내 클리닉 연락 | 1 | post-procedure-timeline.json:reaction_levels.caution×1 | — | — |

## dict:severity (4 · 총 4)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | 경미 — 자연 소실, 경과 관찰 | 1 | complications.json:severity_levels.mild×1 | — | — |
| 2 | 위급 — 응급 대응, 비가역적 손상 가능 | 1 | complications.json:severity_levels.critical×1 | — | — |
| 3 | 중등도 — 치료 필요, 클리닉 방문 | 1 | complications.json:severity_levels.moderate×1 | — | — |
| 4 | 중증 — 즉시 치료, 후유증 가능 | 1 | complications.json:severity_levels.severe×1 | — | — |

## procedure (453 · 총 544)

| # | 조각 | 횟수 | 등장 자리(횟수) | 축 후보(사전 일치) | 결정 묶음 1 |
|---|---|---|---|---|---|
| 1 | 바디 | 7 | treatment-optimization.optimal_combo[] (57)×3 · synergy.links[].from/to (노드 52)×2 · procedure-comparison.procedures[].name (39)×1 · market-pricing.items[].name (122)×1 | problem:바디, purpose_label:바디 | — |
| 2 | 주사 | 7 | taxonomy.json:modality[].subcategories[].items[].name×4 · treatment-optimization.optimal_combo[] (57)×1 · post-procedure-timeline.timelines[].name (10)×1 · market-pricing.items[].name (122)×1 | — | — |
| 3 | 비타민C | 5 | market-pricing.items[].name (122)×2 · taxonomy.json:modality[].subcategories[].items[].name×1 · treatment-optimization.optimal_combo[] (57)×1 · treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 4 | 리쥬란 | 4 | procedure-comparison.procedures[].name (39)×2 · treatment-optimization.optimal_combo[] (57)×1 · treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 5 | 리프팅 | 4 | market-pricing.items[].name (122)×2 · treatment-optimization.annual_plans.schedule[].procedures[] (29)×1 · post-procedure-timeline.timelines[].name (10)×1 | purpose_label:리프팅 | — |
| 6 | 볼륨 | 4 | market-pricing.items[].name (122)×4 | — | — |
| 7 | 시술 | 4 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×2 · treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 · market-pricing.items[].name (122)×1 | — | — |
| 8 | 심부 | 4 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×2 · treatment-sequence.minimum_intervals from/to (14 distinct)×2 | — | — |
| 9 | 이모드 | 4 | market-pricing.items[].name (122)×4 | — | — |
| 10 | 저출력 | 4 | treatment-optimization.optimal_combo[] (57)×2 · taxonomy.json:modality[].subcategories[].items[].name×1 · procedure-comparison.procedures[].name (39)×1 | — | — |
| 11 | 지방분해 | 4 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 · procedure-comparison.procedures[].name (39)×1 · post-procedure-timeline.timelines[].name (10)×1 | — | — |
| 12 | 810nm | 3 | treatment-optimization.optimal_combo[] (57)×2 · procedure-comparison.procedures[].name (39)×1 | — | — |
| 13 | EMS | 3 | market-pricing.items[].name (122)×2 · synergy.links[].from/to (노드 52)×1 | — | — |
| 14 | LLLT | 3 | taxonomy.json:modality[].subcategories[].items[].name×1 · synergy.links[].from/to (노드 52)×1 · problem-packages.procedures[].products[] (제품 34)×1 | — | — |
| 15 | 고주파 | 3 | procedure-comparison.procedures[].name (39)×1 · treatment-optimization.optimal_combo[] (57)×1 · post-procedure-timeline.timelines[].name (10)×1 | — | — |
| 16 | 병변내 | 3 | taxonomy.json:modality[].subcategories[].items[].name×1 · problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | — | — |
| 17 | 색소 | 3 | treatment-optimization.annual_plans.schedule[].procedures[] (29)×3 | purpose_label:색소 | — |
| 18 | 여드름 | 3 | market-pricing.items[].name (122)×3 | problem:여드름, purpose_label:여드름, person_condition:여드름 | — |
| 19 | 프랙셔널 | 3 | procedure-comparison.procedures[].name (39)×3 | — | — |
| 20 | 755nm | 2 | procedure-comparison.procedures[].name (39)×1 · treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 21 | NAD | 2 | taxonomy.json:modality[].subcategories[].items[].name×2 | — | — |
| 22 | PDT | 2 | procedure-comparison.procedures[].name (39)×1 · treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 23 | 감초주사 | 2 | taxonomy.json:modality[].subcategories[].items[].name×1 · market-pricing.items[].name (122)×1 | — | — |
| 24 | 경구 | 2 | treatment-optimization.optimal_combo[] (57)×2 | — | — |
| 25 | 광선치료 | 2 | procedure-comparison.procedures[].name (39)×1 · market-pricing.items[].name (122)×1 | — | — |
| 26 | 끝 | 2 | market-pricing.items[].name (122)×2 | — | — |
| 27 | 냉동지방분해 | 2 | procedure-comparison.procedures[].name (39)×1 · treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 28 | 리포셀 | 2 | procedure-comparison.procedures[].name (39)×1 · treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 29 | 리프팅기기 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | — | — |
| 30 | 마이크로니들링 | 2 | synergy.links[].from/to (노드 52)×1 · treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 31 | 모발이식 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | problem_subcategory_label:모발이식 | — |
| 32 | 물광주사 | 2 | procedure-comparison.procedures[].name (39)×1 · market-pricing.items[].name (122)×1 | — | — |
| 33 | 미라드라 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | — | — |
| 34 | 미백주사 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | — | — |
| 35 | 반영구화장 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | problem_subcategory_label:반영구화장 | — |
| 36 | 스테로이드주사 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | — | — |
| 37 | 실 | 2 | market-pricing.items[].name (122)×2 | adverse_event_type:실 | — |
| 38 | 약물치료 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | problem_subcategory_label:약물치료 | — |
| 39 | 재생 | 2 | procedure-comparison.procedures[].name (39)×1 · market-pricing.items[].name (122)×1 | — | — |
| 40 | 제거 | 2 | market-pricing.items[].name (122)×2 | — | — |
| 41 | 제네시스 | 2 | procedure-comparison.procedures[].name (39)×1 · market-pricing.items[].name (122)×1 | — | — |
| 42 | 제모레이저 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | — | — |
| 43 | 주입 | 2 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 · market-pricing.items[].name (122)×1 | — | — |
| 44 | 지방분해주사 | 2 | taxonomy.json:modality[].subcategories[].items[].name×1 · treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 45 | 코그 | 2 | taxonomy.json:modality[].subcategories[].items[].name×1 · market-pricing.items[].name (122)×1 | — | — |
| 46 | 클렌징 | 2 | taxonomy.json:modality[].subcategories[].items[].name×1 · treatment-sequence.sequence_order[].categories[] (19)×1 | — | — |
| 47 | 탈모 | 2 | market-pricing.items[].name (122)×2 | purpose_label:탈모 | — |
| 48 | 태반주사 | 2 | taxonomy.json:modality[].subcategories[].items[].name×1 · market-pricing.items[].name (122)×1 | — | — |
| 49 | 턱라인 | 2 | market-pricing.items[].name (122)×2 | — | — |
| 50 | 피부결 | 2 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 · treatment-optimization.annual_plans.schedule[].procedures[] (29)×1 | purpose_label:피부결 | — |
| 51 | 피코레이저 | 2 | problem-packages.procedures[].name (시술 종류 29)×1 · problem-packages.combos[].combo[] (멤버 29)×1 | product_type:피코레이저 | — |
| 52 | 회복력 | 2 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×2 | — | — |
| 53 | 후 | 2 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 · market-pricing.items[].name (122)×1 | — | — |
| 54 | 흉터 | 2 | market-pricing.items[].name (122)×2 | problem:흉터, purpose_label:흉터, adverse_event_type:흉터 | — |
| 55 | 1064nm | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 56 | 50% | 1 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 | — | — |
| 57 | 808nm | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 58 | AAPE | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:AAPE | — |
| 59 | ACR | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:ACR | — |
| 60 | AHA | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 61 | ALA | 1 | treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 62 | ALA-PDT | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:ALA-PDT | — |
| 63 | ASA필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:ASA필 | — |
| 64 | BHA | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 65 | CGF | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:CGF | — |
| 66 | CO2레이저 | 1 | problem-packages.procedures[].products[] (제품 34)×1 | — | — |
| 67 | CO2필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:CO2필 | — |
| 68 | CPR | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:CPR | — |
| 69 | Cog | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 70 | Cross | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 71 | DCA | 1 | post-procedure-timeline.timelines[].name (10)×1 | — | — |
| 72 | DNA리셋프로그램 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:DNA리셋프로그램 | — |
| 73 | EGF크림 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:EGF크림 | — |
| 74 | FCR필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:FCR필 | — |
| 75 | GA필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:GA필 | — |
| 76 | GPC주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:GPC주사 | — |
| 77 | HArmonyCa | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:HArmonyCa | — |
| 78 | HP주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 79 | LHA필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:LHA필링 | — |
| 80 | M | 1 | market-pricing.items[].name (122)×1 | — | — |
| 81 | MPE | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:MPE | — |
| 82 | PCA실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:PCA실 | — |
| 83 | PCL복합실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 84 | PDL | 1 | problem-packages.procedures[].products[] (제품 34)×1 | — | — |
| 85 | PDO실 | 1 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 | — | — |
| 86 | PDO코그 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 87 | PDRN | 1 | market-pricing.items[].name (122)×1 | — | — |
| 88 | PDT블루라이트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:PDT블루라이트 | — |
| 89 | PHA필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:PHA필 | — |
| 90 | PLCL | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:PLCL | — |
| 91 | PLLA-SCA | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:PLLA-SCA | — |
| 92 | PN주사 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 93 | PPC | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 94 | PRF | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:PRF | — |
| 95 | PRP | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:PRP | — |
| 96 | Q-스위치 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 97 | RF마이크로니들 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 98 | S | 1 | market-pricing.items[].name (122)×1 | — | — |
| 99 | SNP솔루션 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:SNP솔루션 | — |
| 100 | SVF | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:SVF | — |
| 101 | TU | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 102 | V라인 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 103 | V라인주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:V라인주사 | — |
| 104 | V리프트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:V리프트 | — |
| 105 | V빔 | 1 | problem-packages.procedures[].products[] (제품 34)×1 | — | — |
| 106 | or | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 107 | ±5-FU | 1 | problem-packages.procedures[].products[] (제품 34)×1 | — | — |
| 108 | 간해독 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 109 | 강화 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 110 | 경락 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 111 | 고농도 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 112 | 고농도C | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:고농도C | — |
| 113 | 고려 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 114 | 고용량 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 115 | 골드필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:골드필 | — |
| 116 | 과잉 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 117 | 관절치료 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 118 | 광역동치료 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 119 | 광조사 | 1 | treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 120 | 국소 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 121 | 국소마취 | 1 | treatment-sequence.sequence_order[].categories[] (19)×1 | — | — |
| 122 | 그린필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:그린필 | — |
| 123 | 글루타치온 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 124 | 글리세롤 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 125 | 글리콜산크림 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:글리콜산크림 | — |
| 126 | 금지 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 127 | 기타 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | problem:기타, modality_subcategory_label:기타 | — |
| 128 | 깊이 | 1 | post-procedure-timeline.timelines[].name (10)×1 | — | — |
| 129 | 꺼짐 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 130 | 꿀광주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:꿀광주사 | — |
| 131 | 꿀광토닝 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:꿀광토닝 | — |
| 132 | 나드주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:나드주사 | — |
| 133 | 나이아신아마이드 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:나이아신아마이드 | — |
| 134 | 네페르티티 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 135 | 넥큐레이션 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:넥큐레이션 | — |
| 136 | 노바스템 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:노바스템 | — |
| 137 | 노화 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 138 | 니들 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 139 | 다복스 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:다복스 | — |
| 140 | 다빼주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:다빼주사 | — |
| 141 | 다이어트 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 142 | 다한증 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | problem_subcategory_label:다한증, catalog_item_name:다한증 | — |
| 143 | 닥토필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:닥토필 | — |
| 144 | 데옥시콜산 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 145 | 도자기피부관리 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:도자기피부관리 | — |
| 146 | 도트필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:도트필 | — |
| 147 | 도포 | 1 | treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 148 | 도포·배양 | 1 | treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 149 | 도프ECM | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:도프ECM | — |
| 150 | 동일 | 1 | treatment-sequence.minimum_intervals from/to (14 distinct)×1 | — | — |
| 151 | 두피LED | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:두피LED | — |
| 152 | 두피스케일링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:두피스케일링 | — |
| 153 | 두피주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 154 | 두피치료 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 155 | 듀얼파장 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 156 | 드원셀 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:드원셀 | — |
| 157 | 등살주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:등살주사 | — |
| 158 | 디멜라필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:디멜라필 | — |
| 159 | 딥 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 160 | 라라닥터 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:라라닥터 | — |
| 161 | 라라필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:라라필 | — |
| 162 | 락틱산 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 163 | 래디에스 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 164 | 러브핸들 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 165 | 러브핸들주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:러브핸들주사 | — |
| 166 | 런치필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:런치필 | — |
| 167 | 레나토S | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:레나토S | — |
| 168 | 레드라이트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:레드라이트 | — |
| 169 | 레디에스 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 170 | 레보실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:레보실 | — |
| 171 | 레이저토닝 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:레이저토닝 | — |
| 172 | 레이저토닝pro | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:레이저토닝pro | — |
| 173 | 레이저토닝듀얼 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:레이저토닝듀얼 | — |
| 174 | 레티놀 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:레티놀 | — |
| 175 | 로즈실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:로즈실 | — |
| 176 | 롱펄스 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 177 | 리듐 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:리듐 | — |
| 178 | 리드파인 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:리드파인 | — |
| 179 | 리쥬하 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 180 | 리즈톡신 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:리즈톡신 | — |
| 181 | 리투오 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:리투오 | — |
| 182 | 리투오파인 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:리투오파인 | — |
| 183 | 리포 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 184 | 리포린 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:리포린 | — |
| 185 | 린피니 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:린피니 | — |
| 186 | 마꾸필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:마꾸필 | — |
| 187 | 마늘주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:마늘주사 | — |
| 188 | 마이어스칵테일 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:마이어스칵테일 | — |
| 189 | 마이크로니들RF | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 190 | 만델릭산 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 191 | 매끈V주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:매끈V주사 | — |
| 192 | 멀티미네랄 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:멀티미네랄 | — |
| 193 | 멀티비타민수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:멀티비타민수액 | — |
| 194 | 메디컬 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 195 | 메소테라피 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 196 | 메조 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 197 | 메조테라피 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 198 | 메테로 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:메테로 | — |
| 199 | 면사리프트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:면사리프트 | — |
| 200 | 면역 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 201 | 면포압출 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:면포압출 | — |
| 202 | 모공축소 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 203 | 모노 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:모노 | — |
| 204 | 모든 | 1 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 | — | — |
| 205 | 모피어스8 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 206 | 목적 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 207 | 목전용 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 208 | 몰드리프트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:몰드리프트 | — |
| 209 | 몰딩 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 210 | 문신 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 211 | 물톡스 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:물톡스 | — |
| 212 | 미녹시딜 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 213 | 미라셀 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:미라셀 | — |
| 214 | 미라콜 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:미라콜 | — |
| 215 | 미라클필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:미라클필링 | — |
| 216 | 미라필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:미라필링 | — |
| 217 | 미백성분 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 218 | 미백약물 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 219 | 미세채널 | 1 | treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 220 | 미세침 | 1 | post-procedure-timeline.timelines[].name (10)×1 | — | — |
| 221 | 미스코 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:미스코 | — |
| 222 | 밀리핏주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:밀리핏주사 | — |
| 223 | 밀크필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:밀크필 | — |
| 224 | 바넬라 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 225 | 바디큐레이션 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:바디큐레이션 | — |
| 226 | 바이리즌 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:바이리즌 | — |
| 227 | 바이블주 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:바이블주 | — |
| 228 | 박리성 | 1 | treatment-sequence.minimum_intervals from/to (14 distinct)×1 | — | — |
| 229 | 박피 | 1 | market-pricing.items[].name (122)×1 | adverse_event_type:박피 | — |
| 230 | 백옥주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:백옥주사 | — |
| 231 | 베이비필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:베이비필 | — |
| 232 | 벤조일퍼옥사이드 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:벤조일퍼옥사이드 | — |
| 233 | 벨벳주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:벨벳주사 | — |
| 234 | 별도 | 1 | treatment-sequence.minimum_intervals from/to (14 distinct)×1 | — | — |
| 235 | 보리톡스 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:보리톡스 | — |
| 236 | 보조·근거 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 237 | 복부슬림주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:복부슬림주사 | — |
| 238 | 복용 | 1 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 | — | — |
| 239 | 볼류마이징 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 240 | 볼륨실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:볼륨실 | — |
| 241 | 부위 | 1 | treatment-sequence.minimum_intervals from/to (14 distinct)×1 | — | — |
| 242 | 부위당 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 243 | 부자연스러운 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 244 | 불필요한 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 245 | 블랙필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:블랙필 | — |
| 246 | 블랙필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:블랙필링 | — |
| 247 | 블루라이트 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 248 | 비가교HA | 1 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 | — | — |
| 249 | 비수술 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 250 | 비오틴주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:비오틴주사 | — |
| 251 | 비타민 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 252 | 비타민B1 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 253 | 비타민D | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:비타민D | — |
| 254 | 비타민D주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:비타민D주사 | — |
| 255 | 빼당주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:빼당주사 | — |
| 256 | 사마귀 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 257 | 산 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 258 | 산소필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:산소필 | — |
| 259 | 살리실릭 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 260 | 살몬필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:살몬필 | — |
| 261 | 생크림필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:생크림필 | — |
| 262 | 샤워 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 263 | 서브시전 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:서브시전 | — |
| 264 | 선크림SPF50 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:선크림SPF50 | — |
| 265 | 성장호르몬주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:성장호르몬주사 | — |
| 266 | 세라마이드 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:세라마이드 | — |
| 267 | 세션 | 1 | treatment-sequence.minimum_intervals from/to (14 distinct)×1 | — | — |
| 268 | 센독스 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:센독스 | — |
| 269 | 셀디톡스수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:셀디톡스수액 | — |
| 270 | 셀레늄 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:셀레늄 | — |
| 271 | 셀룰라이트주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:셀룰라이트주사 | — |
| 272 | 셀르디엠 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:셀르디엠 | — |
| 273 | 셀리부트프로그램 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:셀리부트프로그램 | — |
| 274 | 소노PDRN | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:소노PDRN | — |
| 275 | 소부위 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 276 | 소프트필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:소프트필 | — |
| 277 | 솔코세릴필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:솔코세릴필링 | — |
| 278 | 수소필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:수소필링 | — |
| 279 | 슈퍼투턱주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:슈퍼투턱주사 | — |
| 280 | 스네일샷 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:스네일샷 | — |
| 281 | 스노우주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:스노우주사 | — |
| 282 | 스컬프슈어 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 283 | 스킨부스터오마카세 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:스킨부스터오마카세 | — |
| 284 | 스킨스케일링 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 285 | 스킨케어 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 286 | 스테로이드 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 287 | 스피로노락톤 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:스피로노락톤 | — |
| 288 | 신데렐라주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:신데렐라주사 | — |
| 289 | 실리콘겔 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:실리콘겔 | — |
| 290 | 실리콘시트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:실리콘시트 | — |
| 291 | 실리콘피부관리 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 292 | 실크필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:실크필 | — |
| 293 | 써마지 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 294 | 아기주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아기주사 | — |
| 295 | 아다팔렌 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아다팔렌 | — |
| 296 | 아디떼 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아디떼 | — |
| 297 | 아르기닌주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아르기닌주사 | — |
| 298 | 아미노필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아미노필 | — |
| 299 | 아젤라산 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아젤라산 | — |
| 300 | 아쿠아미드 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아쿠아미드 | — |
| 301 | 아큐주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아큐주사 | — |
| 302 | 아큐탄 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아큐탄 | — |
| 303 | 아크네필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:아크네필 | — |
| 304 | 안면 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 305 | 안쪽 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 306 | 알라딘필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:알라딘필링 | — |
| 307 | 알렉스토닝 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:알렉스토닝 | — |
| 308 | 알렉스필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:알렉스필 | — |
| 309 | 알부틴 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:알부틴 | — |
| 310 | 알파리포산 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 311 | 알파리포산주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:알파리포산주사 | — |
| 312 | 압출 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 313 | 앨리필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:앨리필 | — |
| 314 | 앵커리프트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:앵커리프트 | — |
| 315 | 약한 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 316 | 양파추출물연고 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:양파추출물연고 | — |
| 317 | 얕은 | 1 | treatment-sequence.minimum_intervals from/to (14 distinct)×1 | — | — |
| 318 | 에너지부스트수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:에너지부스트수액 | — |
| 319 | 에이비오톡신 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:에이비오톡신 | — |
| 320 | 에피로크 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:에피로크 | — |
| 321 | 엑소좀필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:엑소좀필 | — |
| 322 | 엑소힐러 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:엑소힐러 | — |
| 323 | 엔자이매틱필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:엔자이매틱필링 | — |
| 324 | 엘리실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:엘리실 | — |
| 325 | 여신토닝 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:여신토닝 | — |
| 326 | 여우필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:여우필 | — |
| 327 | 연고마취 | 1 | treatment-sequence.sequence_order[].categories[] (19)×1 | — | — |
| 328 | 예방 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 329 | 예방적 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 330 | 예스필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:예스필 | — |
| 331 | 옐로우필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:옐로우필링 | — |
| 332 | 오메가3수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:오메가3수액 | — |
| 333 | 오픈 | 1 | treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 334 | 옥시덤 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:옥시덤 | — |
| 335 | 올리핏주 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:올리핏주 | — |
| 336 | 외관 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 337 | 우유필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:우유필 | — |
| 338 | 울쎄라급 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 339 | 울트라 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 340 | 유래 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 341 | 유리피부관리 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:유리피부관리 | — |
| 342 | 이뮨코어수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:이뮨코어수액 | — |
| 343 | 이소트레티노인 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:이소트레티노인 | — |
| 344 | 이중턱 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 345 | 이지피틱필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:이지피틱필 | — |
| 346 | 인에이블 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:인에이블 | — |
| 347 | 인형피부관리 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:인형피부관리 | — |
| 348 | 입꼬리 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 349 | 잇몸미소 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 350 | 자가지방이식 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 351 | 자가혈 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 352 | 자연스러운 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 353 | 자연스러움 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 354 | 재생팩 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 355 | 재시술 | 1 | treatment-sequence.minimum_intervals from/to (14 distinct)×1 | — | — |
| 356 | 저출력레이저 | 1 | synergy.links[].from/to (노드 52)×1 | — | — |
| 357 | 저하 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 358 | 전신 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 359 | 점 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 360 | 제네시스토닝 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:제네시스토닝 | — |
| 361 | 제네오X | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:제네오X | — |
| 362 | 제스너필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:제스너필링 | — |
| 363 | 제트필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:제트필 | — |
| 364 | 제한적 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 365 | 종합 | 1 | market-pricing.items[].name (122)×1 | package_tier:vip | — |
| 366 | 종합비타민수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:종합비타민수액 | — |
| 367 | 종합아미노산수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:종합아미노산수액 | — |
| 368 | 주근깨토닝 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:주근깨토닝 | — |
| 369 | 주름 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | problem:주름, catalog_item_name:주름, adverse_event_type:주름 | — |
| 370 | 줄기세포유래 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 371 | 줄기세포필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:줄기세포필 | — |
| 372 | 중 | 1 | treatment-sequence.incompatible_same_day[].pair[] (14 distinct)×1 | — | — |
| 373 | 중간 | 1 | post-procedure-timeline.timelines[].name (10)×1 | — | — |
| 374 | 중요 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 375 | 쥐젖 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 376 | 쥬브아셀 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:쥬브아셀 | — |
| 377 | 지방 | 1 | procedure-comparison.procedures[].name (39)×1 | adverse_qualifier:지방 | — |
| 378 | 지방흡입 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 379 | 진정 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 380 | 진정관리 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 381 | 진정팩 | 1 | treatment-sequence.common_combos[].sequence[] (22 distinct)×1 | — | — |
| 382 | 진주필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:진주필 | — |
| 383 | 징크주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:징크주사 | — |
| 384 | 처짐 | 1 | market-pricing.items[].name (122)×1 | adverse_event_type:처짐 | — |
| 385 | 철분주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:철분주사 | — |
| 386 | 체리필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:체리필 | — |
| 387 | 초과 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 388 | 치료 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 389 | 카복시테라피 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:카복시테라피 | — |
| 390 | 카이벨라 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:카이벨라 | — |
| 391 | 카탈리스트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:카탈리스트 | — |
| 392 | 칼슘주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:칼슘주사 | — |
| 393 | 캐번실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:캐번실 | — |
| 394 | 코그실루프 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:코그실루프 | — |
| 395 | 코조각주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:코조각주사 | — |
| 396 | 코직산 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:코직산 | — |
| 397 | 콘드로이틴주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:콘드로이틴주사 | — |
| 398 | 콜라겐수액 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:콜라겐수액 | — |
| 399 | 콜라겐핀 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:콜라겐핀 | — |
| 400 | 콜라겐필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:콜라겐필 | — |
| 401 | 쿨핏프로그램 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:쿨핏프로그램 | — |
| 402 | 쿰스필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:쿰스필 | — |
| 403 | 퀸즈필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:퀸즈필 | — |
| 404 | 큐젤MAX | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:큐젤MAX | — |
| 405 | 크라이오셀 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:크라이오셀 | — |
| 406 | 크랜베리필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:크랜베리필 | — |
| 407 | 크리스탈필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:크리스탈필 | — |
| 408 | 타이트닝 | 1 | treatment-optimization.optimal_combo[] (57)×1 | — | — |
| 409 | 탄앤막필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:탄앤막필링 | — |
| 410 | 태반주사멜스몬 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:태반주사멜스몬 | — |
| 411 | 턱밑 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 412 | 턱선보톡스 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:턱선보톡스 | — |
| 413 | 테오시알레디세스 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:테오시알레디세스 | — |
| 414 | 텐선실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:텐선실 | — |
| 415 | 투 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 416 | 투와이실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:투와이실 | — |
| 417 | 투자 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 418 | 트라넥삼산 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:트라넥삼산 | — |
| 419 | 트레티노인 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:트레티노인 | — |
| 420 | 트리암시놀론 | 1 | problem-packages.procedures[].products[] (제품 34)×1 | — | — |
| 421 | 파셀라 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 422 | 파인 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 423 | 팻킬주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:팻킬주사 | — |
| 424 | 펀치시술 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:펀치시술 | — |
| 425 | 페놀필링 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:페놀필링 | — |
| 426 | 페이스앤넥큐레이션 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:페이스앤넥큐레이션 | — |
| 427 | 펜카이라주 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:펜카이라주 | — |
| 428 | 표정근 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 429 | 풀코스 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 430 | 풀페이스큐레이션 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:풀페이스큐레이션 | — |
| 431 | 퓨어녹스 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:퓨어녹스 | — |
| 432 | 프로 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | — | — |
| 433 | 프로락틴주사 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:프로락틴주사 | — |
| 434 | 프리미엄 | 1 | market-pricing.items[].name (122)×1 | — | — |
| 435 | 프린스리프트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:프린스리프트 | — |
| 436 | 플라필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:플라필 | — |
| 437 | 피나스테리드도포 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:피나스테리드도포 | — |
| 438 | 피지선 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 439 | 피코 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 440 | 피코토닝 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:피코토닝 | — |
| 441 | 필러량 | 1 | treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)×1 | — | — |
| 442 | 필로르가135HA | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:필로르가135HA | — |
| 443 | 핑크필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:핑크필 | — |
| 444 | 하이드라 | 1 | procedure-comparison.procedures[].name (39)×1 | — | — |
| 445 | 하이드로퀴논 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:하이드로퀴논 | — |
| 446 | 해초필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:해초필 | — |
| 447 | 해피리프트 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:해피리프트 | — |
| 448 | 허니스킨관리 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:허니스킨관리 | — |
| 449 | 허니콤실 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:허니콤실 | — |
| 450 | 헤어맥스 | 1 | problem-packages.procedures[].products[] (제품 34)×1 | — | — |
| 451 | 호박필 | 1 | taxonomy.json:modality[].subcategories[].items[].name×1 | catalog_item_name:호박필 | — |
| 452 | 홍조 | 1 | market-pricing.items[].name (122)×1 | adverse_event_type:홍조 | — |
| 453 | 화학 | 1 | market-pricing.items[].name (122)×1 | — | — |
