# 원장 → 골드 커버리지 · 빈 노드 · 고립 · 입구 점검(조사 · 설계만)

- 골드 `567677edfe7123e9` · 원장 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26`(21 파일) · 실버 정본 11 파일 · fullrun-v2 `b202611020020-edc407`(문항 239 · 같은 문항 두 번은 늦은 쪽)
- 재생성: `python3 node-audit-report.py`(→ `node-audit-coverage.py` · `node-audit.py` 를 돌림) · 두 번 돌려 바이트 같음 확인 · 데이터 수정 없음 · 허브는 GET resolve 만
- **결론 · 적용 없음 — 숫자 · 근거만.** 적용은 사용자 결정 뒤 별도 발주

## 0. 원장 → 골드 커버리지 전수(보충 · 1번)

판정(앞이 이김): **①** 골드 fact 원문에 있음 · **②** fact 는 아니고 골드 노드 · 엣지 · globals 속성(또는 fact 부가칸 meta)에만 · **③** 실버 정본 11 파일에는 있는데 골드에 안 나감 · **④** 실버에도 없음.  
정규화 = triage 식(소문자 · 공백 · 기호 제거). 8자 이상 = 원장 값이 골드 문자열 안에 포함 → 조각 합(골드 문자열들이 원장 값의 80% 이상 덮음) → 3-gram ≥ 0.8. 8자 미만(짧은 값) = 같음 또는 「길이 ≤ 2×+4 인 골드 문자열 안 포함」(triage 짧은 인용 규칙). 경로 = 배열 인덱스 → [] · 코드 키 → {code} · products 분류 키 → {category} — source-map 517 칸과 전부 일치.  
**한계**: 값 기준(문맥 없음) — 같은 문장이 **다른 노드**에 fact 로 붙어 있어도 ①. 「이 노드에 붙었나」는 §1 · §4 에서 따로 봄. 짧은 값(숫자 · 코드 · 한 낱말)은 우연 일치가 있어 따로 셈.

### 0-1. 전체

| 묶음 | 잎 | 판정 대상 | ① fact | ② 속성만 | ③ 실버만 | ④ 실버에도 없음 | 구조값(불리언 · null) | 빈 값 |
|---|---|---|---|---|---|---|---|---|
| 전체 | 23783 | 23509 | 18338 (78.0%) | 4451 (18.9%) | 556 (2.4%) | 164 (0.7%) | 210 | 64 |
| 내용 칸 | 21452 | 21281 | 17251 (81.1%) | 3444 (16.2%) | 536 (2.5%) | 50 (0.2%) | 108 | 63 |
| 메타 · 보관 칸 | 2331 | 2228 | 1087 (48.8%) | 1007 (45.2%) | 20 (0.9%) | 114 (5.1%) | 102 | 1 |
| 긴 값(≥8자) | – | 11275 | 8989 (79.7%) | 1916 (17.0%) | 257 (2.3%) | 113 (1.0%) | – | – |
| 짧은 값(<8자) | – | 12234 | 9349 (76.4%) | 2535 (20.7%) | 299 (2.4%) | 51 (0.4%) | – | – |

「내용 칸」 = source-map 행선지에 속성 · 노드 · 엣지가 하나라도 있는 칸 · 「메타 · 보관」 = 행선지가 리니지 · 버림 · 원문 보관뿐. ② 중 fact 부가칸(meta)만 = 200(도구가 `with_meta` 일 때만 보임).

### 0-2. 파일별

| 파일 | 판정 대상 | ① | ② | ③ | ④ | ① 비율 |
|---|---|---|---|---|---|---|
| taxonomy.json | 11801 | 10071 | 1347 | 342 | 41 | 85.3% |
| problem-packages.json | 2366 | 2018 | 307 | 28 | 13 | 85.3% |
| literature-evidence.json | 1706 | 871 | 825 | 1 | 9 | 51.1% |
| synergy.json | 922 | 511 | 262 | 148 | 1 | 55.4% |
| extracted.json | 717 | 630 | 24 | 6 | 57 | 87.9% |
| market-pricing.json | 648 | 188 | 456 | 1 | 3 | 29.0% |
| complications.json | 627 | 569 | 58 | 0 | 0 | 90.7% |
| post-procedure-timeline.json | 558 | 474 | 81 | 2 | 1 | 84.9% |
| treatment-optimization.json | 491 | 368 | 111 | 11 | 1 | 74.9% |
| anatomy-danger-zones.json | 483 | 313 | 168 | 1 | 1 | 64.8% |
| procedure-comparison.json | 432 | 369 | 62 | 0 | 1 | 85.4% |
| procedure-profiles.json | 411 | 375 | 32 | 1 | 3 | 91.2% |
| problem-combos.json | 370 | 169 | 199 | 0 | 2 | 45.7% |
| pre-procedure-checklist.json | 331 | 158 | 171 | 0 | 2 | 47.7% |
| consent-checklist.json | 306 | 291 | 13 | 0 | 2 | 95.1% |
| products.json | 295 | 150 | 128 | 3 | 14 | 50.8% |
| pih-risk.json | 288 | 210 | 72 | 0 | 6 | 72.9% |
| patient-education.json | 240 | 226 | 13 | 0 | 1 | 94.2% |
| contraindications.json | 192 | 146 | 39 | 5 | 2 | 76.0% |
| treatment-sequence.json | 184 | 132 | 43 | 7 | 2 | 71.7% |
| combo-recipes.json | 141 | 99 | 40 | 0 | 2 | 70.2% |

### 0-3. 파일 × 필드 경로 — ①이 아닌 잎이 많은 순(② + ③ + ④ ≥ 1 · 전부는 json `coverage.rows`)

| 파일 | 경로 | 칸 | 대상 | ① | ② | ③ | ④ | ① 비율 | 예(① 아닌 것) | ②③ 가 있는 곳(첫째) |
|---|---|---|---|---|---|---|---|---|---|---|
| taxonomy.json | `modality[].subcategories[].items[].id` | 메타 · 보관 | 521 | 26 | 495 | 0 | 0 | 5.0% | M1-2-1 | ② node_attr:productattrs.gold.overrides[].source_id |
| taxonomy.json | `modality[].subcategories[].items[].name` | 내용 | 521 | 317 | 191 | 13 | 0 | 60.8% | 피나스테리드도포 | ② node_attr:unit_procedureattrs.silver.side_effect_override[].name |
| pre-procedure-checklist.json | `category_specific[].checks[].type` | 내용 | 123 | 0 | 123 | 0 | 0 | 0.0% | absolute_contraindication | ② edge_attr:requires_checkattrs.grade_original |
| market-pricing.json | `categories[].items[].high` | 내용 | 122 | 0 | 122 | 0 | 0 | 0.0% | 200000 | ② node_attr:packageattrs.silver.price[].high |
| market-pricing.json | `categories[].items[].low` | 내용 | 122 | 0 | 122 | 0 | 0 | 0.0% | 50000 | ② node_attr:packageattrs.silver.price[].low |
| market-pricing.json | `categories[].items[].mid` | 내용 | 122 | 0 | 122 | 0 | 0 | 0.0% | 100000 | ② node_attr:packageattrs.silver.price[].low |
| taxonomy.json | `problem[].subcategories[].items[].id` | 내용 | 117 | 0 | 117 | 0 | 0 | 0.0% | auto-63-1774737181584 | ② edge_attr:treatsattrs.row.source_id |
| synergy.json | `links[].to` | 내용 | 115 | 6 | 61 | 48 | 0 | 5.2% | M9-리프팅기기 | ② node_attr:productattrs.silver.family.name |
| synergy.json | `links[].from` | 내용 | 115 | 9 | 40 | 66 | 0 | 7.8% | M11-포텐자 | ③ step6-packages.json.step6-to-step8-notes[].links[].from |
| problem-packages.json | `problems[].complaints[].procedures[].category` | 내용 | 254 | 157 | 97 | 0 | 0 | 61.8% | M7 | ② node_attr:comboattrs.silver.members[].source_family |
| taxonomy.json | `problem[].subcategories[].items[].name` | 내용 | 117 | 44 | 73 | 0 | 0 | 37.6% | 코필러 | ② node_attr:siteattrs.silver.compound_strings[].key[] |
| problem-packages.json | `problems[].complaints[].cc` | 내용 | 115 | 44 | 71 | 0 | 0 | 38.3% | 코필러 | ② node_attr:siteattrs.silver.compound_strings[].key[] |
| taxonomy.json | `modality[].subcategories[].items[].extracted.mechanism` | 내용 | 521 | 453 | 16 | 52 | 0 | 86.9% | SNARE 복합체(SNAP-25)를 절단하여 신경 말단에서 아세틸콜린 분비를 차단함으로써 근육 수축을 억제한다. 900kDa 복합체 형태의 순수독소(150kDa) | ③ step9-explanations.json.records[].text |
| synergy.json | `links[].type` | 내용 | 115 | 50 | 49 | 16 | 0 | 43.5% | 대신 | ③ step6-packages.json.step6-to-step8-notes[].links[].type |
| taxonomy.json | `modality[].subcategories[].id` | 메타 · 보관 | 74 | 13 | 52 | 9 | 0 | 17.6% | M3-new-1774324512965 | ② edge_attr:requires_checkattrs.row.source_index |
| taxonomy.json | `modality[].products[].id` | 메타 · 보관 | 59 | 0 | 59 | 0 | 0 | 0.0% | M1-P-0 | ② node_attr:productattrs.gold.overrides[].source_id |
| taxonomy.json | `modality[].subcategories[].items[].extracted.indications.primary` | 내용 | 1656 | 1598 | 3 | 55 | 0 | 96.5% | 눈썹 사이 주름(글래벨라) |  |
| taxonomy.json | `modality[].products[].name_en` | 내용 | 59 | 2 | 54 | 0 | 3 | 3.4% | Skin Botox | ② node_attr:productattrs.silver.2_names.search_names[].name |
| products.json | `{category}.products[].name_en` | 메타 · 보관 | 59 | 3 | 53 | 0 | 3 | 5.1% | Skin Botox | ② node_attr:productattrs.silver.2_names.search_names[].name |
| taxonomy.json | `problem[].subcategories[].id` | 내용 | 53 | 0 | 40 | 13 | 0 | 0.0% | P1-5 | ② node_attr:comboattrs.silver.source_id |
| complications.json | `categories[].complications[].severity` | 내용 | 65 | 13 | 52 | 0 | 0 | 20.0% | mild | ② global:value_dictionary |
| problem-packages.json | `problems[].complaints[].cc_group` | 내용 | 115 | 64 | 45 | 6 | 0 | 55.7% | 주사치료 | ② node_name:concern |
| literature-evidence.json | `categories.{code}.moa[].citations[].authors` | 내용 | 50 | 0 | 50 | 0 | 0 | 0.0% | Park MY, Ahn KY | ② node_attr:evidence_sourceattrs.silver.authors |
| literature-evidence.json | `categories.{code}.moa[].citations[].journal` | 내용 | 50 | 1 | 49 | 0 | 0 | 2.0% | Archives of craniofacial surgery | ② node_attr:evidence_sourceattrs.silver.journal |
| literature-evidence.json | `categories.{code}.moa[].citations[].pmc` | 내용 | 49 | 0 | 49 | 0 | 0 | 0.0% | PMC7968983 | ② node_attr:evidence_sourceattrs.silver.pmc |
| literature-evidence.json | `categories.{code}.moa[].citations[].doi` | 내용 | 48 | 0 | 48 | 0 | 0 | 0.0% | 10.7181/acfs.2021.00003 | ② node_attr:evidence_sourceattrs.silver.doi |
| literature-evidence.json | `categories.{code}.moa[].citations[].pmid` | 내용 | 50 | 2 | 48 | 0 | 0 | 4.0% | 33714246 | ② node_attr:evidence_sourceattrs.silver.pmid |
| market-pricing.json | `categories[].items[].name` | 내용 | 122 | 74 | 47 | 1 | 0 | 60.7% | 줄기세포 관절치료 | ② node_attr:unit_procedureattrs.silver.market[].name |
| synergy.json | `links[].from_category` | 내용 | 115 | 68 | 47 | 0 | 0 | 59.1% | M10 | ② node_attr:comboattrs.silver.members[].source_family |
| synergy.json | `links[].to_category` | 내용 | 115 | 68 | 47 | 0 | 0 | 59.1% | M4 | ② node_attr:comboattrs.silver.members[].source_family |
| taxonomy.json | `modality[].subcategories[].items[].extracted.overview` | 내용 | 521 | 474 | 15 | 32 | 0 | 91.0% | 2세대 자가혈 제품, 서방형 성장인자 방출 | ③ step9-explanations.json.records[].text |
| literature-evidence.json | `categories.{code}.moa[].added_at` | 메타 · 보관 | 44 | 0 | 44 | 0 | 0 | 0.0% | 2026-04-19 | ② node_attr:evidence_statementattrs.silver.added_at |
| taxonomy.json | `modality[].subcategories[].label` | 내용 | 74 | 30 | 28 | 5 | 11 | 40.5% | 용도별 | ② node_attr:unit_procedureattrs.silver.side_effect_override[].name |
| products.json | `{category}.products[].country` | 내용 | 58 | 15 | 43 | 0 | 0 | 25.9% | FR | ② node_attr:productattrs.silver.taxonomy_product.country |
| taxonomy.json | `modality[].products[].country` | 내용 | 58 | 15 | 43 | 0 | 0 | 25.9% | FR | ② node_attr:productattrs.silver.taxonomy_product.country |
| pih-risk.json | `procedures[].risk_factors` | 내용 | 68 | 26 | 42 | 0 | 0 | 38.2% | 과도한 fluence | ② fact_meta:safety.pihmeta.risk_factors[] |
| post-procedure-timeline.json | `timelines[].phases[].period` | 내용 | 43 | 1 | 42 | 0 | 0 | 2.3% | Day 0 | ② fact_meta:timelinemeta.period |
| problem-packages.json | `problems[].complaints[].procedures[].products` | 내용 | 388 | 347 | 41 | 0 | 0 | 89.4% | 리쥬란 힐러 | ② node_attr:comboattrs.silver.products_text[] |
| literature-evidence.json | `categories.{code}.effects[].citations[].authors` | 내용 | 37 | 0 | 37 | 0 | 0 | 0.0% | Park MY, Ahn KY | ② node_attr:evidence_sourceattrs.silver.authors |
| taxonomy.json | `modality[].subcategories[].items[].detail` | 내용 | 501 | 464 | 18 | 19 | 0 | 92.6% | 필로르가 · 프랑스 · 53가지 활성성분+HA | ③ step5-units.json.ledger[].detail |
| literature-evidence.json | `categories.{code}.effects[].citations[].journal` | 내용 | 37 | 1 | 36 | 0 | 0 | 2.7% | Archives of craniofacial surgery | ② node_attr:evidence_sourceattrs.silver.journal |
| literature-evidence.json | `categories.{code}.effects[].citations[].pmc` | 내용 | 36 | 0 | 36 | 0 | 0 | 0.0% | PMC7968983 | ② node_attr:evidence_sourceattrs.silver.pmc |
| literature-evidence.json | `categories.{code}.effects[].citations[].doi` | 내용 | 35 | 0 | 35 | 0 | 0 | 0.0% | 10.7181/acfs.2021.00003 | ② node_attr:evidence_sourceattrs.silver.doi |
| literature-evidence.json | `categories.{code}.effects[].added_at` | 메타 · 보관 | 34 | 0 | 34 | 0 | 0 | 0.0% | 2026-04-19 | ② node_attr:evidence_statementattrs.silver.added_at |
| procedure-comparison.json | `comparisons[].procedures[].name` | 내용 | 39 | 5 | 34 | 0 | 0 | 12.8% | 울쎄라 (HIFU) | ② node_attr:comboattrs.silver.members[].text |
| taxonomy.json | `modality[].subcategories[].items[].extracted.onset_duration.duration` | 내용 | 521 | 487 | 3 | 31 | 0 | 93.5% | 24-30개월 | ③ step9-explanations.json.records[].text |
| treatment-optimization.json | `by_concern[].severity_levels[].optimal_combo` | 내용 | 74 | 40 | 34 | 0 | 0 | 54.1% | 스킨부스터(리쥬란) | ② node_attr:comboattrs.silver.components[].text |
| literature-evidence.json | `categories.{code}.effects[].citations[].pmid` | 내용 | 37 | 4 | 33 | 0 | 0 | 10.8% | 33714246 | ② node_attr:evidence_sourceattrs.silver.pmid |
| literature-evidence.json | `categories.{code}.adverse_effects[].citations[].authors` | 내용 | 32 | 0 | 32 | 0 | 0 | 0.0% | Witmanowski H, Błochowiak K | ② node_attr:evidence_sourceattrs.silver.authors |
| literature-evidence.json | `categories.{code}.moa[].citations[].year` | 내용 | 50 | 18 | 32 | 0 | 0 | 36.0% | 2021 | ② node_attr:evidence_sourceattrs.silver.year |
| post-procedure-timeline.json | `timelines[].phases[].label` | 내용 | 43 | 11 | 32 | 0 | 0 | 25.6% | 초기 경과 | ② fact_meta:timelinemeta.label |
| literature-evidence.json | `categories.{code}.adverse_effects[].citations[].journal` | 내용 | 32 | 1 | 31 | 0 | 0 | 3.1% | Postepy dermatologii i alergologii | ② node_attr:evidence_sourceattrs.silver.journal |
| taxonomy.json | `modality[].subcategories[].items[].extracted.onset_duration.onset` | 내용 | 520 | 489 | 2 | 29 | 0 | 94.0% | 2-3일부터 시작 |  |
| taxonomy.json | `problem[].subcategories[].items[].modality_ref` | 내용 | 105 | 74 | 31 | 0 | 0 | 70.5% | M7 | ② node_attr:comboattrs.silver.members[].source_family |
| literature-evidence.json | `categories.{code}.adverse_effects[].citations[].doi` | 내용 | 30 | 0 | 30 | 0 | 0 | 0.0% | 10.5114/ada.2019.82795 | ② node_attr:evidence_sourceattrs.silver.doi |
| literature-evidence.json | `categories.{code}.adverse_effects[].citations[].pmid` | 내용 | 32 | 2 | 30 | 0 | 0 | 6.2% | 33603602 | ② node_attr:evidence_sourceattrs.silver.pmid |
| market-pricing.json | `categories[].items[].unit` | 내용 | 122 | 92 | 30 | 0 | 0 | 75.4% | 1cc | ② node_attr:productattrs.silver.5_spec.market[].unit_raw |
| literature-evidence.json | `categories.{code}.adverse_effects[].citations[].pmc` | 내용 | 29 | 0 | 29 | 0 | 0 | 0.0% | PMC7874868 | ② node_attr:evidence_sourceattrs.silver.pmc |
| products.json | `{category}.products[].manufacturer` | 메타 · 보관 | 58 | 30 | 21 | 0 | 7 | 51.7% | 뉴메코(Newmeco, 메디톡스 계열) | ② node_attr:productattrs.silver.taxonomy_product.manufacturer |
| contraindications.json | `rules[].level` | 내용 | 27 | 0 | 22 | 5 | 0 | 0.0% | warning | ② global:value_dictionary |
| literature-evidence.json | `categories.{code}.effects[].citations[].year` | 내용 | 37 | 10 | 27 | 0 | 0 | 27.0% | 2021 | ② node_attr:evidence_sourceattrs.silver.year |
| problem-packages.json | `problems[].complaints[].procedures[].name` | 내용 | 254 | 228 | 26 | 0 | 0 | 89.8% | PRP/자가혈 |  |
| taxonomy.json | `modality[].products[].extracted.mechanism` | 내용 | 59 | 33 | 0 | 26 | 0 | 55.9% | SNARE 복합체(SNAP-25)를 절단하여 신경근접합부에서 아세틸콜린의 분비를 차단합니다. 900kDa 복합체 형태로 공급되며, 활성 성분인 150kDa 순수독 | ③ step9-explanations.json.records[].text |
| taxonomy.json | `modality[].products[].manufacturer` | 내용 | 58 | 33 | 21 | 0 | 4 | 56.9% | 솔타메디컬 | ② node_attr:productattrs.silver.taxonomy_product.manufacturer |
| literature-evidence.json | `categories.{code}.adverse_effects[].added_at` | 메타 · 보관 | 24 | 0 | 24 | 0 | 0 | 0.0% | 2026-04-19 | ② node_attr:evidence_statementattrs.silver.added_at |
| problem-combos.json | `combos[].packages[].id` | 내용 | 24 | 0 | 24 | 0 | 0 | 0.0% | P1-1 | ② node_attr:comboattrs.silver.source_id |
| problem-combos.json | `combos[].packages[].products` | 내용 | 24 | 0 | 24 | 0 | 0 | 0.0% | 나보타 or 보툴렉스 | ② node_attr:comboattrs.silver.products_text[] |
| problem-combos.json | `combos[].packages[].salesPitch` | 메타 · 보관 | 24 | 0 | 24 | 0 | 0 | 0.0% | 처음이시면 가볍게 보톡스부터 시작해보세요. 10분이면 끝나고 점심시간에도 가능해요. | ② node_attr:comboattrs.silver.sales_copy.salesPitch |
| problem-combos.json | `combos[].packages[].tier` | 내용 | 24 | 0 | 24 | 0 | 0 | 0.0% | entry | ② node_attr:comboattrs.silver.tier |
| problem-combos.json | `combos[].packages[].upsellHook` | 메타 · 보관 | 24 | 0 | 24 | 0 | 0 | 0.0% | 보톡스로 주름 펴시고, 필러로 꺼진 부분 채우시면 확 달라지세요! | ② node_attr:comboattrs.silver.sales_copy.upsellHook |
| taxonomy.json | `problem[].subcategories[].label` | 내용 | 53 | 29 | 22 | 2 | 0 | 54.7% | 주사치료 | ② node_attr:concernattrs.silver.source_label |
| treatment-optimization.json | `by_concern[].severity_levels[].level` | 내용 | 24 | 0 | 24 | 0 | 0 | 0.0% | 경미 (fine lines) | ② node_attr:comboattrs.silver.anchor.severity |
| anatomy-danger-zones.json | `zones[].vessels[].course` | 내용 | 24 | 1 | 23 | 0 | 0 | 4.2% | 안와상연에서 상방으로 주행, 이마 중앙선 근처 | ② edge_attr:site_cautionattrs.row.vessels[].course |
| anatomy-danger-zones.json | `zones[].vessels[].name` | 내용 | 24 | 1 | 23 | 0 | 0 | 4.2% | 활차상동맥 (Supratrochlear artery) | ② edge_attr:site_cautionattrs.row.vessels[].name |
| literature-evidence.json | `categories.{code}.adverse_effects[].citations[].year` | 내용 | 32 | 9 | 23 | 0 | 0 | 28.1% | 2021 | ② node_attr:evidence_sourceattrs.silver.year |
| anatomy-danger-zones.json | `zones[].nerves[].name` | 내용 | 21 | 0 | 21 | 0 | 0 | 0.0% | 활차상신경 (Supratrochlear nerve) | ② edge_attr:site_cautionattrs.nerves[].name |
| anatomy-danger-zones.json | `zones[].nerves[].significance` | 내용 | 21 | 0 | 21 | 0 | 0 | 0.0% | 이마 내측 감각 | ② edge_attr:site_cautionattrs.nerves[].significance |
| anatomy-danger-zones.json | `zones[].nerves[].type` | 내용 | 21 | 0 | 21 | 0 | 0 | 0.0% | sensory | ② edge_attr:site_cautionattrs.nerves[].type |
| problem-combos.json | `combos[].packages[].procedures` | 내용 | 63 | 43 | 20 | 0 | 0 | 68.3% | M4 | ② node_attr:comboattrs.silver.members[].source_family |
| synergy.json | `links[].target` | 내용 | 115 | 95 | 2 | 18 | 0 | 82.6% | 안티에이징 패키지 | ③ step7-concerns.json.correspondence[].text |

(① 아닌 잎이 있는 경로 274 / 전체 경로 517 — 80 줄까지만 표시)

### 0-4. ④ 실버에도 없음 — 큰 필드부터 · 왜 빠졌나

| 파일 | 경로 | ④ / 대상 | 예 | source-map 행선지(단계 · 종류 · 상태) | 왜 빠졌나(기록 인용) | 결정 있음? |
|---|---|---|---|---|---|---|
| extracted.json | `{code}.extracted_at` | 17 / 17 | 2026-03-28 | 브론즈/리니지/미정 | source-map B01: extracted 원천 메타 = 「브론즈 리니지 · 미정」 — 실버 어느 단계도 안 받음(결정 없음) | **없음** |
| extracted.json | `{code}.source` | 17 / 17 | 일반 의학 지식 | 브론즈/리니지/미정 | 같음(「일반 의학 지식」 같은 출처 문자열) — 8단계 evidence_source 는 literature/guides/web 만 받음 · 결정 없음 | **없음** |
| taxonomy.json | `modality[].subcategories[].label` | 11 / 74 | 용도별 | 2/속성/끝 · 3/속성/끝 | 2 · 3단계 「속성 · 끝」 판정 근거로만 씀 — 「용도별」 같은 묶음 라벨 11 은 노드 · 속성 어디에도 안 옮김(결정은 「판정」까지 · 실음 여부 결정 없음) | **없음** |
| extracted.json | `{code}.procedure_id` | 9 / 17 | M11-NEEDLERF | 2/리니지/끝 | 2단계 「리니지 · 끝(계열 동의어 대조 · 정본 step2)」 — 코드 값이라 대조에만 쓰고 안 실음(결정대로) | 있음(결정대로 안 실음) |
| problem-packages.json | `problems[].complaints[].combos[].reason` | 9 / 146 | 단독 시술 | 8/엣지 속성/미정 | 8단계 「엣지 속성 · 미정」(시너지 주장 evidence) — 146 중 137 은 붙고 짧은 이유 9(「단독 시술」 등)만 빠짐 · 결정 없음 | **없음** |
| products.json | `{category}.products[].manufacturer` | 7 / 58 | 뉴메코(Newmeco, 메디톡스 계열) | 1/원문 보관/끝 | 1단계 「원문 보관 · 끝」 — 업체 표기는 허가 기준 6_companies 로 바꿈(원천 표기 7 은 원문 보관 · 결정대로) | 있음(결정대로 안 실음) |
| extracted.json | `{code}.name_en` | 6 / 17 | High-Intensity Focused Electromagnetic Stimulation / EMS | 2/리니지/끝 | 2단계 리니지 · 끝 — 계열 영문명은 step2 정본 이름을 씀(원천 표기 6 은 안 옮김 · 결정대로) | 있음(결정대로 안 실음) |
| taxonomy.json | `modality[].subcategories[].items[].ingredient_basis` | 6 / 6 | 히알루론산(비가교 또는 저분자 HA) + 비타민(C/B 계열) 혼합. 제품·클리닉별 배합 상이 | 5/속성/결정됨 | **5단계 「단위 시술 ingredient 속성 · 결정됨」인데 step5-units.json 에 글이 없음** — step5-units.md:438~440 은 이 칸을 동의어 판정 근거로만 인용(마케팅명 = 동의어). 결정과 실물이 다름 | **결정 있음 · 실물 없음** |
| taxonomy.json | `modality[].subcategories[].items[].naming_caveat` | 6 / 6 | '꿀광'은 효과 묘사용 마케팅명으로 표준화된 단일 제제가 아님. 실제 사용 성분·농도는 클리닉별로 상이하므로 상담 시 실제 성분과 허가 제품명 확인 필요 | 5/속성/결정됨 | **5단계 「name_status · 주의 문구 원문 — S14」 결정(step5-units.md:1436)인데 주의 문구 원문이 실버에 없음** — 결정과 실물이 다름 | **결정 있음 · 실물 없음** |
| extracted.json | `{code}.source_type` | 5 / 17 | general | 브론즈/리니지/미정 | 같음 · 결정 없음 | **없음** |
| taxonomy.json | `modality[].subcategories[].items[].canonical_category` | 5 / 6 | M4 스킨부스터 > 재생형 메조테라피 | 2/리니지/끝 | 2단계 리니지 · 끝(계열 판정 근거) — 결정대로 | 있음(결정대로 안 실음) |
| pih-risk.json | `procedures[].fitzpatrick_note` | 4 / 26 | 피코초 펄스로 열확산 최소화. 755nm은 멜라닌 흡수도가 높아 1064nm 대비 약간 높은 PIH | 5/속성/표시 | 5단계 「표시」(step5-units.md:1391 S10 — 26행 3층에 붙임) — 22 는 붙고 4 빠짐 · 빠진 4 에 대한 결정 없음 | **없음** |
| taxonomy.json | `modality[].products[].manufacturer` | 4 / 58 | 솔타메디컬 | 1/속성/끝 | 1단계 6_companies(허가 기준) — 원천 표기 4 는 버림(결정대로) | 있음(결정대로 안 실음) |
| products.json | `{category}.products[].name_en` | 3 / 59 | Skin Botox | 1/원문 보관/끝 | 1단계 원문 보관 · 끝(search_names 로 대체) — 3 은 표기 차이로 안 붙음 | 있음(결정대로 안 실음) |
| taxonomy.json | `modality[].products[].name_en` | 3 / 59 | Skin Botox | 1/속성/끝 | 1단계 search_names — 3 은 표기 차이 | 있음(결정대로 안 실음) |
| extracted.json | `{code}.name` | 2 / 17 | MTS (마이크로니들 치료) | 2/리니지/끝 | 2단계 리니지 · 끝(같음) | 있음(결정대로 안 실음) |
| problem-packages.json | `problems[].complaints[].combos[].evidence` | 2 / 146 | 4~6회 시리즈 | 8/엣지 속성/미정 | source-map: 시너지 주장 evidence | **없음** |
| products.json | `{category}.products[].regulatory_status` | 2 / 2 | 화장품 허가만 받은 제품 — 식약처의 주사·주입 용도 허가 없음 | 1/속성/끝 · 5/속성/미정 | 5단계 「allowed_routes [도포] 가드」(step5-units.md:1401) 로 바꿈 — 원문 문장은 안 실음 · 원문 보관 결정 없음 | **없음** |
| taxonomy.json | `modality[].products[].extracted.safety.common_side_effects` | 2 / 4 | 일시적 울퉁불퉁함 | 5/속성/미정 | 5단계 키 정규화(safety.common · step5-units.md:1437) — 2 는 값 표기 차이로 안 붙음 · 결정 없음 | **없음** |
| taxonomy.json | `modality[].subcategories[].items[].classification_issue` | 2 / 2 | 이 엔트리는 M4(스킨부스터) 섹션에 잘못 등재됨 — 볼뉴머는 클래시스(Classys)의 6.78MHz 모노폴라 RF 리프팅 장비이며, 주사제가 아님. 카테고리를 | 2/리니지/끝 | 2단계 리니지 · 끝(조사 정정 근거) — 결정대로 | 있음(결정대로 안 실음) |
| anatomy-danger-zones.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| combo-recipes.json | `description` | 1 / 1 | 대표원장급 검증 조합 레시피 — 목적별 프리셋 + 기대 효과 + 후속 프로토콜 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| combo-recipes.json | `updated` | 1 / 1 | 2026-04-04 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| consent-checklist.json | `description` | 1 / 1 | 시술별 필수 고지 항목. 법적 동의서 기반 mandatory disclosure, 금기사항, 응급 징후 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| consent-checklist.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| contraindications.json | `description` | 1 / 1 | 시술 간 금기/주의사항/간격 매트릭스 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| contraindications.json | `updated` | 1 / 1 | 2026-07-11 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| extracted.json | `{code}.updated` | 1 / 1 | 2026-07-11 | 브론즈/리니지/미정 | 같음 · 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.by_category_average.{code}` | 1 / 7 | 98.0 | 버림/버림/미정 | 브론즈 메타 칸(원문에서 다시 셀 수 있는 집계) — 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.patient_ko_coverage` | 1 / 1 | 119/119 | 버림/버림/미정 | 브론즈 메타 칸(원문에서 다시 셀 수 있는 집계) — 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.patient_translations_coverage.en` | 1 / 1 | 119/119 | 버림/버림/미정 | 브론즈 메타 칸(원문에서 다시 셀 수 있는 집계) — 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.patient_translations_coverage.ja` | 1 / 1 | 119/119 | 버림/버림/미정 | 브론즈 메타 칸(원문에서 다시 셀 수 있는 집계) — 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.patient_translations_coverage.ko` | 1 / 1 | 119/119 | 버림/버림/미정 | 브론즈 메타 칸(원문에서 다시 셀 수 있는 집계) — 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.patient_translations_coverage.zh` | 1 / 1 | 119/119 | 버림/버림/미정 | 브론즈 메타 칸(원문에서 다시 셀 수 있는 집계) — 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.rubric` | 1 / 1 | 95-100=교과서 consensus, 85-94=주류 표준, 70-84=뉘앙스 보정, 50-69=근거 약함, 0-49=부정확 | 브론즈/리니지/미정 | 브론즈 메타 칸(근거 품질 점수의 뜻(시맨틱 설명)) — 결정 없음 | **없음** |
| literature-evidence.json | `accuracy_summary.scored_by` | 1 / 1 | Legacy content-quality scores retained for surviving statements; not a clinical claim appr | 브론즈/리니지/미정 | 브론즈 메타 칸(근거 품질 점수의 뜻(시맨틱 설명)) — 결정 없음 | **없음** |
| literature-evidence.json | `updated` | 1 / 1 | 2026-09-03 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| market-pricing.json | `categories[].name` | 1 / 17 | 에너지기기(HIFU/RF) | 2/리니지/끝 | 브론즈 메타 칸(시장가 행의 계열) — step2-families.json(2단계 정본) · procedure-master-v3.json(5단계 초안 — 재료) market_rows | 있음(결정대로 안 실음) |
| market-pricing.json | `note` | 1 / 1 | 한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위. | 5/속성/결정됨 | source-map: 시술 1회 가격의 통화 · 단서(가격 칸 메타) — 행선지가 속성인데 실버에 글 없음 | **결정 있음 · 실물 없음** |
| market-pricing.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| patient-education.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| pih-risk.json | `description` | 1 / 1 | 시술별 PIH(Post-Inflammatory Hyperpigmentation) 위험도. Fitzpatrick skin type III-IV (한국인 대다수)를  | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| pih-risk.json | `updated` | 1 / 1 | 2026-04-05 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| post-procedure-timeline.json | `updated` | 1 / 1 | 2026-07-11 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| pre-procedure-checklist.json | `description` | 1 / 1 | 시술 전 체크리스트. 카테고리별 universal + category-specific 확인 항목 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| pre-procedure-checklist.json | `updated` | 1 / 1 | 2026-04-05 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| problem-combos.json | `description` | 1 / 1 | Problem별 추천 조합 — 상담 안내와 의료진 참고 정보 통합 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| problem-combos.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| problem-packages.json | `description` | 1 / 1 | taxonomy P1~P14 하위구조 기반 CC 자동 생성 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| problem-packages.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| procedure-comparison.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| procedure-profiles.json | `description` | 1 / 1 | 시술 프로파일 v3 — 플로어 매니저 관점: 제품 준비, 소요 시간, 마취, 시술 후 관리 포함 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| procedure-profiles.json | `profiles[].name` | 1 / 17 | 에너지기기(HIFU/RF) | 2/리니지/끝 | 브론즈 메타 칸(계열 키(정본 = step2)) — step2-families.json(2단계 정본) | 있음(결정대로 안 실음) |
| procedure-profiles.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| products.json | `description` | 1 / 1 | 미용시술 제품-제조사 매핑 (유통사 아닌 제조사 기준) | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| products.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| synergy.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| taxonomy.json | `modality[].subcategories[].items[].correction_note` | 1 / 1 | 이전 데이터에 '808nm 다이오드 제모 레이저'로 잘못 기재돼 있었음. 실제 사양은 클래시스 공식 제품 페이지(https://classys.co.kr/produ | 2/리니지/끝 | 2단계 리니지 · 끝 — 결정대로 | 있음(결정대로 안 실음) |
| taxonomy.json | `modality[].subcategories[].items[].verification_needed` | 1 / 1 | 식약처 허가 번호 및 임상시험 근거 확인 전까지 '신규 허가' 표현 사용 금지. 확인 전에는 임상·광고에 사용 지양 | 1/리니지/끝 | 1단계 4_license 가 대체 — 결정대로 | 있음(결정대로 안 실음) |
| treatment-optimization.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| treatment-sequence.json | `description` | 1 / 1 | 동일 세션 시술 조합 순서 가이드. 안전성과 효과 최적화 기준. | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |
| treatment-sequence.json | `updated` | 1 / 1 | 2026-07-26 | 브론즈/리니지/결정됨 | 브론즈 메타 칸(브론즈 스냅샷 메타(엣지 · 속성의 원천 버전)) — DEC-001 D-02 브론즈 원본 보존 · D-10 · DEC-001 D-04 엣지 메타(근거 · 강도 · 조건 · 원천) | 있음(결정대로 안 실음) |

**결정 없이(또는 결정과 다르게) 빠진 것** — 21 경로 · 잎 91:

- extracted.json `{code}.extracted_at` 17 — **없음**
- extracted.json `{code}.source` 17 — **없음**
- taxonomy.json `modality[].subcategories[].label` 11 — **없음**
- problem-packages.json `problems[].complaints[].combos[].reason` 9 — **없음**
- taxonomy.json `modality[].subcategories[].items[].ingredient_basis` 6 — **결정 있음 · 실물 없음**
- taxonomy.json `modality[].subcategories[].items[].naming_caveat` 6 — **결정 있음 · 실물 없음**
- extracted.json `{code}.source_type` 5 — **없음**
- pih-risk.json `procedures[].fitzpatrick_note` 4 — **없음**
- problem-packages.json `problems[].complaints[].combos[].evidence` 2 — **없음**
- products.json `{category}.products[].regulatory_status` 2 — **없음**
- taxonomy.json `modality[].products[].extracted.safety.common_side_effects` 2 — **없음**
- extracted.json `{code}.updated` 1 — **없음**
- literature-evidence.json `accuracy_summary.by_category_average.{code}` 1 — **없음**
- literature-evidence.json `accuracy_summary.patient_ko_coverage` 1 — **없음**
- literature-evidence.json `accuracy_summary.patient_translations_coverage.en` 1 — **없음**
- literature-evidence.json `accuracy_summary.patient_translations_coverage.ja` 1 — **없음**
- literature-evidence.json `accuracy_summary.patient_translations_coverage.ko` 1 — **없음**
- literature-evidence.json `accuracy_summary.patient_translations_coverage.zh` 1 — **없음**
- literature-evidence.json `accuracy_summary.rubric` 1 — **없음**
- literature-evidence.json `accuracy_summary.scored_by` 1 — **없음**
- market-pricing.json `note` 1 — **결정 있음 · 실물 없음**

### 0-5. ② · ③ — 어디에 있고 어느 도구 · 섹션으로 내보내면 되나(추천 · 내용 칸 상위)

| 내보낼 자리(추천) | ② | ③ | 경로(많은 순 앞 5) |
|---|---|---|---|
| 그 밖 — 소유 노드의 가장 가까운 section(overview · method · aftercare) fact 로 | 961 | 354 | problem-packages.problems[].complaints[].procedures[].category(97) · problem-packages.prob |
| evidence_source 노드 속성 — 출처 표기는 지금처럼 속성(인용 목록) · fact 화 불필요(추천) | 683 | 0 | literature-evidence.categories.{code}.moa[].citations[].authors(50) · literature-evidence. |
| 이름 · 동의어 — resolve 사전(fact 불필요) | 524 | 20 | taxonomy.modality[].subcategories[].items[].name(204) · taxonomy.problem[].subcategories[] |
| 시장가 — 단위 시술/제품 `market` fact(가격 · 규격) — T3 card · expand | 444 | 1 | market-pricing.categories[].items[].high(122) · market-pricing.categories[].items[].low(12 |
| 시너지 엣지 끝점 · 종류 — 엣지로 이미 표현(③ 는 6단계 notes 원문만) | 246 | 148 | synergy.links[].to(109) · synergy.links[].from(106) · synergy.links[].type(65) · synergy.l |
| 식별자 — 내보낼 필요 없음 | 263 | 13 | taxonomy.problem[].subcategories[].items[].id(117) · taxonomy.problem[].subcategories[].id |
| site_caution 엣지 속성 → 부위 노드 `site_caution` fact(위치 · 혈관 · 깊이) — T10 peek · T11 expand(부위 시작 걸음) | 142 | 0 | anatomy-danger-zones.zones[].vessels[].course(23) · anatomy-danger-zones.zones[].vessels[] |
| 확인 조건 등급 — requires_check 엣지 resolved · T5 checks 가 이미 냄(fact 불필요) | 139 | 0 | pre-procedure-checklist.category_specific[].checks[].type(123) · pre-procedure-checklist.u |
| `safety.pih` fact(위험 요인 문장) — 지금 meta 에만 | 42 | 0 | pih-risk.procedures[].risk_factors(42) |

## 1. 빈 노드(사실 0) — 원천 재료 전수

셈: 사실 0 = gold-export fact 의 owner_id ∪ attached_to 에 한 번도 없음(코디 셈과 같음). 재료 = 원장 레코드 중 **이름 칸**(name · label · problem · concern · cc · category · zone · condition 등)이 노드 이름 · 실버 동의어 · 사전 표현(조건 붙은 CC 행 제외)과 같은 「자기 레코드」의 잎(id 류 뺌). 재료 종류는 잎 키로 나눔. 「정의 · 설명」 = 자기 레코드 **바로 아래**(taxonomy 는 extracted. 아래 포함)의 description · overview · definition · explanation · simple_ · analogy · summary · subtitle 칸 — 하위 항목(시술 · 제품) 설명은 「하위 항목」으로 따로. 괄호 별칭 = 원장 문자열 「X(Y)」 에서 X 나 Y 가 노드 말일 때 반대쪽(잡음 있음 → 사람 확인). 언급 = 다른 레코드 문장 안에 노드 말이 나옴(3자 이상 · 2자는 짧은 칸만).

| 종류 | 노드 | 사실 0 | 재료 있음(자기 레코드) | 재료 없음 | 정의 · 설명 있음 | 괄호 별칭 후보 있음 | 언급만 있음 |
|---|---|---|---|---|---|---|---|
| concern | 57 | 45 | 43 | 2 | 2 | 30 | 2 |
| site | 53 | 42 | 13 | 29 | 3 | 26 | 23 |
| technique | 26 | 26 | 4 | 22 | 1 | 10 | 11 |
| purpose | 13 | 13 | 9 | 4 | 0 | 7 | 2 |
| check_condition | 53 | 12 | 0 | 12 | 0 | 1 | 12 |
| package | 24 | 8 | 8 | 0 | 5 | 2 | 0 |
| combo | 79 | 5 | 5 | 0 | 0 | 0 | 0 |
| 합 | – | 151 | **82** | 69 | 11 | – | – |

재료 종류별 셈(빈 노드 전체 · 잎 수 / 그 재료가 있는 노드 수): 기타 214/80 · 하위 항목 4698/74 · 상위 분류 114/68 · 대표 시술 120/39 · 영문명 32/23 · 세부 · 메모 61/22 · 위험 등급 145/20 · 가격 68/16 · 기법 설명 13/11 · 정의 · 설명 12/11 · 별칭 5/5 · 위치 43/5

빈 노드 재료 중 골드에 fact 로도 없는 것(②③④) = 1080 잎 — 나머지는 골드에 fact 로 있지만 **다른 노드(시술 · 제품 · 조합)** 에 붙어 있음(이 노드에서 걸으면 안 보임).

### 1-1. 노드별(빈 노드 전부)

| 노드 | 이름 | 엣지 | 자기 레코드(수 · 첫째) | 재료 종류별 수 | 정의 | 괄호 별칭 후보(앞 3) | 언급 수 |
|---|---|---|---|---|---|---|---|
| `check_condition:C-CHRONINF` | 만성감염(피부결핵 · 매독) | 9 | 0 ·  | {} | ✗ |  | 2 |
| `check_condition:C-DENTAL` | 최근 치과 시술 | 9 | 0 ·  | {} | ✗ |  | 1 |
| `check_condition:C-DPEN` | D-페니실라민 | 18 | 0 ·  | {} | ✗ |  | 1 |
| `check_condition:C-HORMONE` | 경구 피임약 · 에스트로겐 | 6 | 0 ·  | {} | ✗ |  | 2 |
| `check_condition:C-HYAL` | 히알루로니다아제 알레르기 | 9 | 0 ·  | {} | ✗ |  | 1 |
| `check_condition:C-LIDO` | 마취제 알레르기(리도카인) | 7 | 0 ·  | {} | ✗ |  | 10 |
| `check_condition:C-LIVER` | 간기능 · 지질 수치(레티노이드 처방) | 8 | 0 ·  | {} | ✗ |  | 7 |
| `check_condition:C-MUSCLE` | 근이완제 등 특정 약물 | 18 | 0 ·  | {} | ✗ |  | 2 |
| `check_condition:C-NEURO` | 신경계 질환 | 10 | 0 ·  | {} | ✗ |  | 1 |
| `check_condition:C-PEELALG` | 필링 제제 알레르기 | 6 | 0 ·  | {} | ✗ |  | 1 |
| `check_condition:C-PHOTO` | 광과민성 질환 · 약물 | 46 | 0 ·  | {} | ✗ |  | 10 |
| `check_condition:C-RETIN` | 레티노이드 처방 | 8 | 0 ·  | {} | ✗ | 외용제 · 확인 | 10 |
| `combo:RC-SQ-01` | 동안 기본 | 3 | 1 · treatment-sequence.common_combos[0] | {"기타": 4, "대표 시술": 1} | ✗ |  | 0 |
| `combo:RC-SQ-02` | 피부결 개선 | 5 | 1 · treatment-sequence.common_combos[1] | {"기타": 4, "대표 시술": 1} | ✗ |  | 55 |
| `combo:RC-SQ-03` | 리프팅 풀코스 | 10 | 1 · treatment-sequence.common_combos[2] | {"기타": 5, "대표 시술": 1} | ✗ |  | 0 |
| `combo:RC-SQ-04` | 여드름 집중 | 3 | 1 · treatment-sequence.common_combos[3] | {"기타": 5, "대표 시술": 1} | ✗ |  | 0 |
| `combo:RC-SQ-05` | 색소 집중 | 4 | 1 · treatment-sequence.common_combos[4] | {"기타": 4, "대표 시술": 1} | ✗ |  | 0 |
| `concern:J10` | 피부결 | 18 | 2 · problem-combos.combos[3] | {"가격": 3, "기타": 3, "영문명": 1, "위험 등급": 9, "하위 항목": 61} | ✗ | CO2 · M4 · 문제 | 155 |
| `concern:J14` | 잇몸미소 | 3 | 0 ·  | {} | ✗ | gummy smile | 2 |
| `concern:J8` | 자갈턱 | 2 | 0 ·  | {} | ✗ |  | 2 |
| `concern:P10` | 제모 | 70 | 4 · problem-packages.problems[9] | {"기타": 4, "대표 시술": 1, "상위 분류": 1, "영문명": 2, "위험 등급": 6, "하위 항목": 318} | ✗ | 겨드랑이 · 레이저 · 영구적 | 34 |
| `concern:P11` | 얼굴윤곽 | 42 | 3 · problem-combos.combos[7] | {"가격": 2, "기타": 2, "대표 시술": 1, "영문명": 1, "위험 등급": 2, "하위 항목": 191} | ✗ | 실 | 43 |
| `concern:P11-2` | 이중턱 | 13 | 3 · problem-packages.problems[2].complaints[2] | {"기타": 3, "대표 시술": 1, "상위 분류": 3, "세부 · 메모": 3, "하위 항목": 38} | ✗ | 리프팅 · 턱 아래 부위 · 턱밑 지방 | 60 |
| `concern:P12` | 바디 | 5 | 4 · problem-packages.problems[11] | {"기타": 4, "대표 시술": 1, "상위 분류": 1, "영문명": 2, "위험 등급": 6, "하위 항목": 217} | ✗ | HIFES · 여성 · 인모드 | 60 |
| `concern:P12-3` | 탄력 | 8 | 1 · taxonomy.problem[11].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ | 개선 | 15 |
| `concern:P12-4` | 셀룰라이트 | 14 | 1 · taxonomy.problem[11].subcategories[3] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ | 중등도 · 피부 울퉁불퉁한 지방 침착 | 17 |
| `concern:P13` | 두피/탈모 | 28 | 3 · problem-packages.problems[12] | {"기타": 2, "대표 시술": 1, "상위 분류": 1, "영문명": 1, "하위 항목": 329} | ✗ | AGA · MTS · 두피치료 | 36 |
| `concern:P14-1` | 점/사마귀 | 9 | 1 · taxonomy.problem[13].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 2 |
| `concern:P14-3` | 다한증 | 19 | 2 · taxonomy.modality[0].subcategories[2].items[5] | {"기법 설명": 1, "기타": 7, "대표 시술": 1, "상위 분류": 2, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목": 16} | ○ | 땀이 과하게 나는 증상 | 12 |
| `concern:P14-4` | 피부질환(백반증 · 건선) | 6 | 1 · taxonomy.problem[13].subcategories[3] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 19 |
| `concern:P2` | 주름 | 30 | 5 · problem-combos.combos[1] | {"가격": 4, "기법 설명": 1, "기타": 8, "대표 시술": 2, "상위 분류": 1, "세부 · 메모": 1, "영문명": 2, "위험 등급": 10 | ○ | crow's feet · glabellar lines · platysmal bands | 186 |
| `concern:P2-1` | 표정주름 | 4 | 1 · taxonomy.problem[1].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ | 눈가 · 미간 · 이마 | 16 |
| `concern:P2-2` | 깊은주름 | 6 | 1 · taxonomy.problem[1].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ | 팔자주름 | 41 |
| `concern:P2-3` | 잔주름 | 3 | 3 · problem-packages.problems[1].complaints[6] | {"기타": 3, "대표 시술": 1, "상위 분류": 3, "세부 · 메모": 3, "하위 항목": 29} | ✗ | 개선 · 얕은 주름 · 토끼주름 | 74 |
| `concern:P3` | 처짐 | 20 | 4 · problem-combos.combos[2] | {"가격": 4, "기타": 4, "대표 시술": 1, "영문명": 2, "위험 등급": 10, "하위 항목": 240} | ✗ | HIFU · HIFU 또는 고주파 · Mephisto sign | 593 |
| `concern:P3-1` | 처짐 | 5 | 1 · taxonomy.problem[2].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ | Mephisto sign · depressor septi nasi · drooping | 9 |
| `concern:P3-2` | 처짐 | 3 | 1 · taxonomy.problem[2].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ | Mephisto sign · depressor septi nasi · drooping | 7 |
| `concern:P3-3` | 처짐 | 12 | 1 · taxonomy.problem[2].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ | Mephisto sign · depressor septi nasi · drooping | 7 |
| `concern:P4` | 항노화 | 11 | 3 · problem-combos.combos[3] | {"가격": 3, "기타": 2, "대표 시술": 1, "영문명": 1, "위험 등급": 3, "하위 항목": 196} | ✗ | 원인 | 116 |
| `concern:P4-1` | 탄력 | 31 | 3 · problem-combos.combos[2] | {"가격": 4, "기타": 4, "상위 분류": 1, "영문명": 1, "위험 등급": 10, "하위 항목": 75} | ✗ | HIFU · HIFU 또는 고주파 · RF | 962 |
| `concern:P4-3` | 전신항노화 | 10 | 1 · taxonomy.problem[3].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ |  | 2 |
| `concern:P5` | 색소/미백 | 38 | 5 · problem-combos.combos[3] | {"가격": 6, "기타": 5, "대표 시술": 1, "영문명": 2, "위험 등급": 12, "하위 항목": 287} | ✗ | 기미 · 기미 보조 · 기미 초기 | 113 |
| `concern:P5-2` | 주근깨/잡티 | 21 | 1 · taxonomy.problem[4].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 10 |
| `concern:P5-3` | 오타모반/ABNOM | 9 | 1 · taxonomy.problem[4].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ |  | 1 |
| `concern:P5-4` | 전체미백 | 9 | 1 · taxonomy.problem[4].subcategories[3] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 2 |
| `concern:P6` | 여드름 | 15 | 4 · problem-packages.problems[5] | {"기타": 4, "대표 시술": 1, "상위 분류": 1, "영문명": 2, "위험 등급": 6, "하위 항목": 221} | ✗ | comedonal · comedonal acne · inflammatory | 223 |
| `concern:P6-1` | 급성(활성) 여드름 | 9 | 1 · taxonomy.problem[5].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ |  | 3 |
| `concern:P6-2` | 피지/모공 | 18 | 1 · taxonomy.problem[5].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ |  | 9 |
| `concern:P6-3` | 여드름자국(PIH/PIE) | 10 | 1 · taxonomy.problem[5].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ | PIE · PIH | 3 |
| `concern:P7` | 모공 | 16 | 4 · problem-combos.combos[5] | {"가격": 3, "기타": 4, "대표 시술": 1, "영문명": 2, "위험 등급": 9, "하위 항목": 221} | ✗ | 결과 | 93 |
| `concern:P7-1` | 피지과다형 모공 | 14 | 1 · taxonomy.problem[6].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 2 |
| `concern:P7-2` | 탄력저하형 모공 | 14 | 1 · taxonomy.problem[6].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 2 |
| `concern:P7-3` | 흉터형(열린모공) | 10 | 1 · taxonomy.problem[6].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ | 열린모공 | 19 |
| `concern:P8` | 홍조/혈관 | 7 | 2 · problem-packages.problems[7] | {"기타": 1, "대표 시술": 1, "영문명": 1, "하위 항목": 105} | ✗ |  | 4 |
| `concern:P8-1` | 홍조 | 15 | 1 · taxonomy.problem[7].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ | 엑셀V · 혈관 · 혈관병변 | 30 |
| `concern:P8-2` | 모세혈관확장 | 13 | 1 · taxonomy.problem[7].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ | 병변 | 18 |
| `concern:P8-3` | 정맥류 | 4 | 1 · taxonomy.problem[7].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ |  | 0 |
| `concern:P9` | 흉터 | 20 | 5 · problem-combos.combos[6] | {"가격": 2, "기타": 5, "대표 시술": 1, "상위 분류": 1, "영문명": 2, "위험 등급": 8, "하위 항목": 400} | ✗ | 개선 · 결손부위 · 과도한 에너지로 인한 진피 손상 | 139 |
| `concern:P9-1` | 여드름흉터 | 27 | 2 · taxonomy.problem[8].subcategories[0] | {"기타": 3, "상위 분류": 1, "영문명": 1, "위험 등급": 6, "하위 항목": 39} | ✗ | 개선 · 니들RF · 진피절제주입법과 병행 | 68 |
| `concern:P9-2` | 켈로이드/비후성 | 14 | 1 · taxonomy.problem[8].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 4 |
| `concern:P9-3` | 수술흉터/화상흉터 | 9 | 1 · taxonomy.problem[8].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ |  | 2 |
| `concern:P9-4` | 튼살 | 3 | 1 · taxonomy.problem[8].subcategories[3] | {"기타": 1, "상위 분류": 1, "하위 항목": 4} | ✗ | 배 · 성장선 · 임신선 | 4 |
| `package:P6-01` | 풀페이스큐레이션 | 4 | 1 · taxonomy.modality[0].subcategories[2].items[9] | {"기법 설명": 1, "기타": 5, "대표 시술": 1, "상위 분류": 1, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목": 13} | ○ |  | 0 |
| `package:P6-02` | 바디큐레이션 | 2 | 1 · taxonomy.modality[0].subcategories[2].items[10] | {"기법 설명": 1, "기타": 5, "대표 시술": 1, "상위 분류": 1, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목": 16} | ○ |  | 0 |
| `package:P6-03` | 넥큐레이션 | 8 | 1 · taxonomy.modality[0].subcategories[2].items[11] | {"기법 설명": 1, "기타": 5, "대표 시술": 1, "상위 분류": 1, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목": 12} | ○ |  | 1 |
| `package:P6-04` | 페이스앤넥큐레이션 | 4 | 1 · taxonomy.modality[0].subcategories[2].items[12] | {"기법 설명": 1, "기타": 5, "대표 시술": 1, "상위 분류": 1, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목": 14} | ○ |  | 0 |
| `package:P6-20` | 프리미엄 스킨케어 (풀코스) | 0 | 1 · market-pricing.categories[14].items[6] | {"가격": 3, "기타": 1, "대표 시술": 1, "상위 분류": 1} | ✗ |  | 0 |
| `package:P6-22` | 스컬트라 (3회 패키지) | 1 | 6 · market-pricing.categories[2].items[0] | {"가격": 7, "기법 설명": 3, "기타": 20, "대표 시술": 7, "상위 분류": 5, "세부 · 메모": 1, "영문명": 2, "위험 등급": 1 | ○ | 1바이알 · 3회 패키지 · PLLA | 37 |
| `package:P6-23` | 이모드 (4회 패키지) | 2 | 4 · market-pricing.categories[9].items[0] | {"가격": 12, "기타": 4, "대표 시술": 4, "상위 분류": 4} | ✗ | 4회 패키지 · 복부 · 복부+힙 동시 | 0 |
| `package:P6-24` | 줄기세포 3회 패키지 (전체얼굴) | 1 | 1 · market-pricing.categories[16].items[5] | {"가격": 3, "기타": 1, "대표 시술": 1, "상위 분류": 1} | ✗ |  | 0 |
| `purpose:PU-01` | 리프팅 | 7 | 0 ·  | {} | ✗ | HIFU · HIFU 또는 고주파 · RF | 587 |
| `purpose:PU-02` | 타이트닝(탄력) | 9 | 0 ·  | {} | ✗ | HIFU · 개선 · 콜라겐 자극 | 146 |
| `purpose:PU-03` | 재생 | 9 | 1 · taxonomy.modality[15].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 117} | ✗ | PRP · SB · 샤워 | 45 |
| `purpose:PU-04` | 볼륨 회복(충전) | 49 | 2 · taxonomy.problem[3].subcategories[1] | {"기타": 3, "상위 분류": 1, "영문명": 1, "위험 등급": 6, "하위 항목": 25} | ✗ | 2cc · 4cc · HA 1cc | 60 |
| `purpose:PU-05` | 연장 | 2 | 0 ·  | {} | ✗ |  | 0 |
| `purpose:PU-06` | 축소 | 1 | 0 ·  | {} | ✗ |  | 0 |
| `purpose:PU-07` | 지방분해(지방감소) | 45 | 4 · problem-packages.problems[10].complaints[1].procedures[0] | {"기타": 1, "대표 시술": 9, "상위 분류": 4, "하위 항목": 14} | ✗ | 물리적 · 화학적 | 146 |
| `purpose:PU-08` | 근육강화 | 10 | 1 · taxonomy.problem[11].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ | HIFES | 37 |
| `purpose:PU-09` | 항산화 | 0 | 1 · taxonomy.modality[15].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 101} | ✗ | 글루타치온 | 78 |
| `purpose:PU-10` | 피로회복 | 9 | 1 · taxonomy.modality[15].subcategories[1] | {"기타": 1, "상위 분류": 1, "하위 항목": 116} | ✗ |  | 19 |
| `purpose:PU-11` | 면역 | 0 | 1 · taxonomy.modality[15].subcategories[2] | {"기타": 1, "상위 분류": 1, "하위 항목": 117} | ✗ |  | 15 |
| `purpose:PU-12` | 영양보충 | 6 | 1 · taxonomy.modality[15].subcategories[3] | {"기타": 1, "상위 분류": 1, "하위 항목": 71} | ✗ |  | 3 |
| `purpose:PU-13` | 문신 제거 | 6 | 4 · market-pricing.categories[7].items[9] | {"가격": 3, "기타": 4, "대표 시술": 2, "상위 분류": 4, "세부 · 메모": 3, "하위 항목": 11} | ✗ |  | 36 |
| `site:site.abdomen` | 복부 | 4 | 0 ·  | {} | ✗ | 감소 · 부위 · 이모드 | 10 |
| `site:site.arm` | 팔 | 2 | 0 ·  | {} | ✗ |  | 0 |
| `site:site.axilla` | 겨드랑이 | 4 | 0 ·  | {} | ✗ | 제모 | 9 |
| `site:site.back` | 등 | 3 | 0 ·  | {} | ✗ |  | 5 |
| `site:site.beard` | 수염 | 2 | 0 ·  | {} | ✗ |  | 2 |
| `site:site.bikini` | 비키니 | 2 | 2 · problem-packages.problems[9].complaints[2] | {"기타": 2, "대표 시술": 1, "상위 분류": 2, "세부 · 메모": 3, "하위 항목": 8} | ✗ |  | 0 |
| `site:site.body` | 바디 | 24 | 3 · problem-packages.problems[11] | {"기타": 2, "대표 시술": 1, "상위 분류": 1, "영문명": 1, "하위 항목": 193} | ✗ | HIFES · 여성 · 인모드 | 49 |
| `site:site.buttock` | 힙 | 2 | 0 ·  | {} | ✗ | 이모드 | 0 |
| `site:site.calf` | 종아리 | 2 | 1 · taxonomy.modality[0].subcategories[2].items[3] | {"기법 설명": 1, "기타": 3, "대표 시술": 1, "상위 분류": 1, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목": 10} | ○ |  | 11 |
| `site:site.cheek` | 볼 | 5 | 1 · anatomy-danger-zones.zones[6] | {"별칭": 1, "세부 · 메모": 5, "영문명": 1, "위치": 8, "위험 등급": 8, "하위 항목": 20} | ✗ | 부위 · 처짐 · 필러 | 0 |
| `site:site.chest` | 가슴 | 2 | 0 ·  | {} | ✗ | 부위 | 2 |
| `site:site.chin-group` | 턱(묶음) | 5 | 2 · anatomy-danger-zones.zones[8] | {"기타": 1, "별칭": 1, "상위 분류": 1, "세부 · 메모": 5, "영문명": 1, "위치": 8, "위험 등급": 8, "하위 항목": 19} | ✗ | 이브아르 | 3 |
| `site:site.eyebrow` | 눈썹 | 2 | 0 ·  | {} | ✗ | 처짐 | 8 |
| `site:site.eyelid` | 눈꺼풀 | 4 | 0 ·  | {} | ✗ | 부위 | 28 |
| `site:site.face` | 얼굴 | 12 | 1 · taxonomy.problem[9].subcategories[0] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ | 부위 | 112 |
| `site:site.flank` | 옆구리 | 3 | 0 ·  | {} | ✗ | 감소 · 지방 | 13 |
| `site:site.foot` | 발 | 2 | 0 ·  | {} | ✗ |  | 0 |
| `site:site.forehead-group` | 이마(묶음) | 3 | 2 · anatomy-danger-zones.zones[0] | {"기타": 1, "별칭": 1, "상위 분류": 1, "세부 · 메모": 4, "영문명": 1, "위치": 11, "위험 등급": 8, "하위 항목": 26} | ✗ | 돌출부 · 부위 · 표정근 | 49 |
| `site:site.full-face` | 얼굴 전체 | 45 | 0 ·  | {} | ✗ | IPL · MTS · PRP | 55 |
| `site:site.gingiva` | 잇몸 | 3 | 0 ·  | {} | ✗ |  | 0 |
| `site:site.hand` | 손 | 2 | 0 ·  | {} | ✗ |  | 0 |
| `site:site.infraorbital` | 눈밑 | 3 | 0 ·  | {} | ✗ |  | 9 |
| `site:site.lateral-canthus` | 눈가 | 5 | 1 · taxonomy.problem[0].subcategories[4] | {"기타": 1, "상위 분류": 1, "하위 항목": 6} | ✗ | 부위 · 표정근 · 표정주름 | 26 |
| `site:site.leg` | 다리 | 4 | 0 ·  | {} | ✗ |  | 0 |
| `site:site.marionette` | 마리오네트 | 2 | 0 ·  | {} | ✗ |  | 9 |
| `site:site.masseter` | 사각턱 | 2 | 4 · market-pricing.categories[0].items[6] | {"가격": 6, "기법 설명": 1, "기타": 7, "대표 시술": 3, "상위 분류": 4, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목" | ○ | 교근 · 교근 비대 · 교근 축소 | 31 |
| `site:site.mouth-corner` | 입꼬리 | 2 | 0 ·  | {} | ✗ | 손상 · 운동마비 | 14 |
| `site:site.nasal-ala` | 콧망울 | 2 | 0 ·  | {} | ✗ |  | 4 |
| `site:site.nasal-dorsum` | 콧등 | 2 | 0 ·  | {} | ✗ |  | 6 |
| `site:site.nasal-tip` | 코끝 | 2 | 0 ·  | {} | ✗ | 보톡스 | 4 |
| `site:site.neck` | 목 | 5 | 1 · anatomy-danger-zones.zones[10] | {"별칭": 1, "세부 · 메모": 5, "영문명": 1, "위치": 7, "위험 등급": 8, "하위 항목": 17} | ✗ | 부위 · 합병증 | 0 |
| `site:site.nose` | 코 | 3 | 2 · anatomy-danger-zones.zones[4] | {"기타": 1, "별칭": 1, "상위 분류": 1, "세부 · 메모": 7, "영문명": 1, "위치": 9, "위험 등급": 9, "하위 항목": 25} | ✗ | 분포 · 폐색 | 0 |
| `site:site.perioral` | 입가 | 7 | 0 ·  | {} | ✗ |  | 151 |
| `site:site.philtrum` | 인중 | 2 | 0 ·  | {} | ✗ |  | 2 |
| `site:site.scalp` | 두피 | 11 | 0 ·  | {} | ✗ | MTS · PRP · 엑소좀 | 32 |
| `site:site.sideburn` | 구레나룻 | 2 | 0 ·  | {} | ✗ |  | 2 |
| `site:site.submental` | 턱밑 | 5 | 0 ·  | {} | ✗ | 이중턱 | 25 |
| `site:site.thigh` | 허벅지 | 4 | 0 ·  | {} | ✗ | 감소 · 바디 · 채취부 | 28 |
| `site:site.trapezius` | 승모근 | 2 | 3 · market-pricing.categories[0].items[8] | {"가격": 3, "기법 설명": 1, "기타": 6, "대표 시술": 2, "상위 분류": 3, "세부 · 메모": 1, "정의 · 설명": 1, "하위 항목" | ○ | 사다리꼴근 | 19 |
| `site:site.upper-arm` | 팔뚝 | 3 | 0 ·  | {} | ✗ | 바디 | 12 |
| `site:site.whole-body` | 전신 | 3 | 0 ·  | {} | ✗ | 제모 | 6 |
| `site:site.zygoma` | 광대 | 2 | 1 · taxonomy.problem[10].subcategories[3] | {"기타": 1, "상위 분류": 1, "하위 항목": 2} | ✗ | 보톡스 · 처짐 | 20 |
| `technique:K01` | 주입 | 62 | 0 ·  | {} | ✗ | 개인차 있으며 | 96 |
| `technique:K01a` | 메조테라피 | 8 | 0 ·  | {} | ✗ | mesotherapy · 물광주사 | 29 |
| `technique:K01b` | 정맥 주사 | 27 | 0 ·  | {} | ✗ | IV | 34 |
| `technique:K01c` | 무바늘 제트 주입 | 3 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K02` | 삽입 | 8 | 0 ·  | {} | ✗ |  | 2 |
| `technique:K02a` | 코그실 삽입 | 1 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K02b` | 모노실 삽입 | 1 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K02c` | 볼륨실 삽입 | 1 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K03` | 미세침 천공 | 6 | 0 ·  | {} | ✗ |  | 1 |
| `technique:K04` | 조사 | 27 | 0 ·  | {} | ✗ | test spot | 0 |
| `technique:K04a` | 토닝 | 4 | 2 · problem-packages.problems[5].complaints[6] | {"기타": 2, "대표 시술": 1, "상위 분류": 2, "세부 · 메모": 3, "하위 항목": 15} | ✗ | 논어블레이티브 | 32 |
| `technique:K04b` | 프락셔널 | 5 | 11 · problem-packages.problems[8].complaints[0].procedures[0] | {"기타": 1, "대표 시술": 40, "상위 분류": 11, "하위 항목": 201} | ✗ | 박리성 · 오픈 · 전체얼굴 | 151 |
| `technique:K04c` | 광역학 | 2 | 0 ·  | {} | ✗ |  | 6 |
| `technique:K05` | 에너지 가열 | 10 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K06` | 전자기 자극 | 8 | 0 ·  | {} | ✗ |  | 2 |
| `technique:K07` | 플라즈마 전달 | 6 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K08` | 냉각 | 9 | 0 ·  | {} | ✗ | DCD · contact cooling · 아이스팩 | 4 |
| `technique:K09` | 도포 | 6 | 0 ·  | {} | ✗ | LAED · MTS · 니들RF 후 경피 전달 | 3 |
| `technique:K10` | 침투 | 2 | 0 ·  | {} | ✗ | 영양 공급 | 0 |
| `technique:K11` | 박리·흡인 | 3 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K12` | 소수술 | 8 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K12a` | 서브시전 | 2 | 11 · problem-packages.problems[6].complaints[5] | {"기법 설명": 1, "기타": 8, "대표 시술": 21, "상위 분류": 11, "세부 · 메모": 7, "정의 · 설명": 1, "하위 항목": 50} | ○ | 깊은 흉터 박리 | 41 |
| `technique:K12b` | 펀치 | 2 | 0 ·  | {} | ✗ |  | 2 |
| `technique:K12c` | 압출 | 2 | 2 · problem-packages.problems[5].complaints[0] | {"기타": 2, "대표 시술": 1, "상위 분류": 2, "세부 · 메모": 3, "하위 항목": 13} | ✗ |  | 0 |
| `technique:K13` | 미세색소주입 | 5 | 0 ·  | {} | ✗ |  | 0 |
| `technique:K14` | 흡입 마사지 | 2 | 0 ·  | {} | ✗ |  | 2 |

### 1-2. 원장에 정의 · 설명 자체가 없는 노드(7 종류 전체 — 사실 있는 노드 포함)

「정의 없음」 = 자기 레코드가 없거나, 있어도 바로 아래에 정의 · 설명 칸이 없음. 예 `팔자주름`(concern:auto-83 · 사실 3) — 자기 레코드 4(anatomy-danger-zones nasolabial · market-pricing 「팔자주름 (HA 1cc)」 · problem-packages cc · taxonomy 항목) = 위치 7 · 위험 8 · 가격 3 · 영문 1 · 별칭 후보(코입술주름 등)만 있고 정의 문장 없음.

| 종류 | 노드 | 정의 없음 | 그중 재료(위치 · 위험 · 가격 · 시술)는 있음 | 정의 없음 이름(앞 30) |
|---|---|---|---|---|
| concern | 57 | 55 | 53 | 피부결 · 잇몸미소 · 자갈턱 · 제모 · 얼굴윤곽 · 이중턱 · 바디 · 탄력 · 셀룰라이트 · 두피/탈모 · 점/사마귀 · 피부질환(백반증 · 건선) · 표정 |
| site | 53 | 50 | 19 | 복부 · 팔 · 겨드랑이 · 등 · 수염 · 비키니 · 바디 · 힙 · 볼 · 볼(묶음) · 가슴 · 턱끝 · 턱(묶음) · 눈썹 · 눈꺼풀 · 얼굴 · 옆구리  |
| technique | 26 | 25 | 3 | 주입 · 메조테라피 · 정맥 주사 · 무바늘 제트 주입 · 삽입 · 코그실 삽입 · 모노실 삽입 · 볼륨실 삽입 · 미세침 천공 · 조사 · 토닝 · 프락셔널 · |
| purpose | 13 | 13 | 9 | 리프팅 · 타이트닝(탄력) · 재생 · 볼륨 회복(충전) · 연장 · 축소 · 지방분해(지방감소) · 근육강화 · 항산화 · 피로회복 · 면역 · 영양보충 · 문 |
| check_condition | 53 | 49 | 4 | 활동성 여드름 · 연령대 · 알레르기 · 과민반응 병력 · 아미노글리코시드 항생제 · 수유 · 출혈 경향 · 응고장애 · 혈액질환 · 체형 · 피하지방 두께 ·  |
| package | 24 | 7 | 7 | MTS + PRP (전체얼굴) · 이모드 (복부+힙 동시) · MTS + 스킨부스터 · 프리미엄 스킨케어 (풀코스) · 줄기세포 + MTS (전체얼굴) · 이모드 |
| combo | 79 | 62 | 31 | 20대 연령 플랜 · 30대 연령 플랜 · 40대 연령 플랜 · 50대+ 연령 플랜 · 20대 피부관리 베이직 플랜 · 30대 동안 유지 플랜 · 40대+ 안티에 |
| 합 | 305 | **261** | – | – |

정의 있는 노드: 항응고제 · 항혈소판제(check_condition) · 자가면역질환(check_condition) · 헤르페스 병력(check_condition) · 이소트레티노인(check_condition) · 여드름 치료 비교(combo) · 바디 컨투어링 비교(combo) · 제모 비교(combo) · 리프팅 비교(combo) · 색소 치료 비교(combo) · 피부 재생 비교(combo) · 피부결 개선 비교(combo) · 볼륨 회복 비교(combo) · 주름 개선 비교(combo) · 레이저 토닝(combo) · 리프팅 기본(combo) · 리프팅 풀패키지(combo) · 피부 재생 골든루틴(combo) · 탄력 + 주름 집중(combo) · 모공/흉터 집중(combo) · 동안 쁘띠 패키지(combo) · 레이저 토닝 + 재생(combo) · 다한증(concern) · 주름(concern) · 풀페이스큐레이션(package) · 바디큐레이션(package) · 넥큐레이션(package) · 페이스앤넥큐레이션(package) · 꿀광토닝(package) · 브라이트닝레이저(package) · 여신토닝(package) · 셀리부트프로그램(package) · DNA리셋프로그램(package) · 텍스쳐스무딩(package) · 쿨핏프로그램(package) · 유리피부관리(package) · 도자기피부관리(package) · 인형피부관리(package) · 허니스킨관리(package) · 스킨부스터오마카세(package) · 스컬트라 (3회 패키지)(package) · 종아리(site) · 사각턱(site) · 승모근(site) · 서브시전(technique)

→ concern · site · technique · purpose 는 원장에 「X 란 무엇」 문장이 거의 없다(정의 있음 concern 2 · site 3 · technique 1 · purpose 0). 「팔자주름이 뭔가요」 는 **원장 재료로는 정의 문장을 만들 수 없음** — 위치(해부 · 혈관) · 위험 등급 · 대표 시술 · 가격으로 「설명」은 조립 가능, 정의 문장 자체는 원천 보강(의료진 · 새 원천) 몫.

## 2. 고립 노드(엣지 0) — 왜 · 이을 후보

| 종류 | 고립 | 사실 있음 |
|---|---|---|
| combo | 4 | 4 |
| evidence_source | 39 | 39 |
| package | 1 | 0 |
| product | 3 | 3 |
| purpose | 2 | 0 |

| 노드 | 이름 | 사실 | 왜 고립(실버 기록) | 원천으로 이을 후보(종류 · 근거) |
|---|---|---|---|---|
| `combo:RC-AN-20대` | 20대 피부관리 베이직 플랜 | 45 | 실버 앵커 = 연령대(age_group) — 고민 · 목적 노드 아님 · components 칸 없음(7단계가 연간 플랜 schedule 을 구성으로 안 풂) | combo_component 후보 7/7 말(원장 annual_plans.schedule[].procedures — 허브 resolve 로 닿음: IPL(가을 색소 관리), IPL(색소 관리), LED 집중(여름철), 스킨부스터, 연말 집중 케어(필링+LED), 토닝, 필링) · 안 닿음  · anchors_combo 후보 = focus 「피부 기초 관리, 여드름/흉터 개선, 모공/피부결 관리」 resolve → concern:J10, concern:P6, concern:P7, concern:P9, menu:모공, menu:흉터 |
| `combo:RC-AN-30대` | 30대 동안 유지 플랜 | 33 | 실버 앵커 = 연령대(age_group) — 고민 · 목적 노드 아님 · components 칸 없음(7단계가 연간 플랜 schedule 을 구성으로 안 풂) | combo_component 후보 8/8 말(원장 annual_plans.schedule[].procedures — 허브 resolve 로 닿음: IPL, 바이오스티뮬레이터, 보톡스, 보톡스 이마/미간, 보톡스 터치업, 스킨부스터, 연말 특별 관리(필링+LED), 토닝) · 안 닿음  · anchors_combo 후보 = focus 「노화 예방, 동적주름 관리, 콜라겐 투자 시작」 resolve →  |
| `combo:RC-AN-40대+` | 40대+ 안티에이징 집중 플랜 | 46 | 실버 앵커 = 연령대(age_group) — 고민 · 목적 노드 아님 · components 칸 없음(7단계가 연간 플랜 schedule 을 구성으로 안 풂) | combo_component 후보 15/15 말(원장 annual_plans.schedule[].procedures — 허브 resolve 로 닿음: HIFU(울쎄라/슈링크), HIFU/RF(하반기), IPL, IPL(가을 색소), 바이오스티뮬레이터, 바이오스티뮬레이터(유지 1차), 보톡스, 보톡스 터치업, 보) · 안 닿음  · anchors_combo 후보 = focus 「처짐/주름 적극 관리, 볼륨 복원, 복합 시술 조합」 resolve → concern:P2, concern:P3, concern:P3-1, concern:P3-2, concern:P3-3, menu:주름, purpose:PU-04,  |
| `combo:RC-PC-P1-1` | 보톡스 단독 | 4 | 앵커 = P1 쁘띠시술(고민 노드 아님 · J5 메뉴 이름 속성만) · 구성 「보톡스 단독」 = 고민(대분류)에 부위 없음 · 이름 · 제품으로 못 좁힘(R23) → units 0 · 계열 엣지도 안 만듦 | ① 메뉴 「쁘띠시술」 → 이 조합(menu_labels 에는 이미 RC-PC-P1-1 이 있음 — 그래프 엣지만 없음) ② combo_component → family:M1(계열만 · 원장 problem-combos.combos[0].packages[0].procedures) — 근거 = 같은 P1 의 P1-2 · P1-3 는 엣지 있음 |
| `package:P6-20` | 프리미엄 스킨케어 (풀코스) | 0 | 6단계 일반 패키지 · components 0 — 원장에 시장가 이름(market-pricing 「프리미엄 스킨케어 (풀코스)」)만 · 구성 시술 원문 없음 | contains 후보 없음(원장에 구성 없음) — 원천 보강 몫 |
| `product:auto-M15-1775401780659` | 알렉스필 | 2 | 1단계 허가 「확인 불가」 · recommendable false — 2단계 원장님 문의 3(알렉스필 · 더마큐어 · 벨르업 · _RESUME 10-28 「사용자가 따로 문의」) | product_family 후보 = 2단계 문의 답 뒤(지금 이으면 열린 것을 추측으로 메움) — 대기 |
| `product:new-DEV-034` | 벨르업 | 2 | 1단계 허가 「확인 불가」 · recommendable false — 2단계 원장님 문의 3(알렉스필 · 더마큐어 · 벨르업 · _RESUME 10-28 「사용자가 따로 문의」) | product_family 후보 = 2단계 문의 답 뒤(지금 이으면 열린 것을 추측으로 메움) — 대기 |
| `product:new-DEV-042` | 더마큐어 | 2 | 1단계 허가 「확인 불가」 · recommendable false — 2단계 원장님 문의 3(알렉스필 · 더마큐어 · 벨르업 · _RESUME 10-28 「사용자가 따로 문의」) | product_family 후보 = 2단계 문의 답 뒤(지금 이으면 열린 것을 추측으로 메움) — 대기 |
| `purpose:PU-09` | 항산화 | 0 | 7단계 「목적 · 고민 대응 없음」 — 메뉴(M16-1 미백/항산화 · M16-3 재생/면역 · P4-3 항산화수액)에서만 나온 목적 · 고민 앵커 없음 | treats(목적 → 단위 시술) 후보 = 메뉴 M16 하위 단위 시술(원장 taxonomy modality M16 subcategories) — 이름 근거만 · 효과 근거 문장 없음 → 사람 확인 |
| `purpose:PU-11` | 면역 | 0 | 7단계 「목적 · 고민 대응 없음」 — 메뉴(M16-1 미백/항산화 · M16-3 재생/면역 · P4-3 항산화수액)에서만 나온 목적 · 고민 앵커 없음 | treats(목적 → 단위 시술) 후보 = 메뉴 M16 하위 단위 시술(원장 taxonomy modality M16 subcategories) — 이름 근거만 · 효과 근거 문장 없음 → 사람 확인 |

evidence_source 고립 39: 종류 {'가이드 · 표기 출처': 14, '원문 출처 문자열(내부 · 통설)': 10, '웹': 14, '출처 아님(이유 문장)': 1} · 39 전부 `used_by`(8단계 주장 R8-…)가 있음 — 골드는 cites 엣지를 문헌 진술(evidence_statement → 문헌)에서만 만들고, 8단계 주장(엣지 속성 claim)이 가리키는 가이드 · 웹 · 내부 출처에는 엣지가 없음. 후보 = 주장이 붙은 엣지(procedure_relation · requires_check)의 evidence 에 출처 id 를 싣거나 `cites_claim` 엣지 — 39 전부 근거 있음(used_by). 「출처 아님(이유 문장)」 1 은 이을 대상 아님.

**원천으로 이을 수 있는 고립 = 44** / 49(combo 4 · purpose 2(사람 확인) · evidence_source 38) · 못 이음 = product 3(문의 대기) · package 1(원천에 구성 없음) · evidence_source 1(출처 아님).

## 3. 입구 — fullrun-v2 case3 되돌아감 15(no_start 12 · no_facts 3)

말마다: 조사를 뗀 꼴(은 · 는 · 이 · 가 · 을 · 를 · 와 · 과 · 랑 · 에 · 만 · 도 · 부터 · 만으로 …, 남는 말 2자 이상)로 허브 resolve(GET) 다시 · semantic 사전 정확 일치 · 원장 잎에 그 말이 든 경로 수.

| 문항 | 되돌아감 | 질문 | 그때 resolve 후보 | 조사 떼면 닿는 말 → 노드 | 사전에 없고 원천에 있는 말(→ 닿을 노드) | 원인 |
|---|---|---|---|---|---|---|
| Q025 | no_start | 쁘띠시술 추천 패키지 뭐 있어요? | none:고민 노드 아님(트리 항목) |  |  | 후보가 트리 항목(none) — 메뉴 후보는 있었으나 시작 선택지 아님 |
| Q042 | no_start | 필러와 보톡스는 무엇이 달라요? | family:M2, concern:P14-3, family:M1, product:M1-2-1 |  |  | 후보 있음 · Jev 「해당 없음」(두 시술 · 비교 의도 시작 문제 — 사전 아님) |
| Q059 | no_start | 손주사와 기계주사 중 무엇이 더 좋아요? |  |  |  | resolve 0 · 원천에 노드 말 없음(일반 질문) |
| Q066 | no_start | PN·PDRN 제품은 생선 알레르기가 있어도 맞나요? |  | 알레르기가→알레르기: check_condition:C-ALLERGY |  | resolve 0 → 조사 · 사전 보강으로 시작 가능 |
| Q082 | no_start | 고주파와 초음파를 같은 날 받아도 되나요? | unit_procedure:U5-091, unit_procedure:U5-104 |  | 초음파 → family:M9(원장 「고강도 집속 초음파(HIFU)」 · 괄호 별칭) — 사전엔 없음 | 후보 있음 · Jev 「해당 없음」(두 시술 · 비교 의도 시작 문제 — 사전 아님) |
| Q084 | no_start | 써마지와 덴서티를 함께 받아도 되나요? | unit_procedure:U5-091, unit_procedure:U5-104, product:new-DEV-024 |  |  | 후보 있음 · Jev 「해당 없음」(두 시술 · 비교 의도 시작 문제 — 사전 아님) |
| Q117 | no_facts | 여드름 레이저만 받으면 약 없이 낫나요? | concern:P6 | 레이저만→레이저: family:M8 |  | 시작 노드 concern:P6 사실 0(§1 빈 노드) |
| Q119 | no_start | 압출과 레이저를 같은 날 해도 되나요? | concern:P6-1, technique:K12c, unit_procedure:U5-048, family:M8 |  |  | 후보 있음 · Jev 「해당 없음」(두 시술 · 비교 의도 시작 문제 — 사전 아님) |
| Q144 | no_facts | 여드름 자국이 남아 있는데 흉터 레이저부터 받나요? | concern:P6, concern:P9 | 레이저부터→레이저: family:M8 |  | 시작 노드 concern:P6 사실 0(§1 빈 노드) |
| Q187 | no_facts | 처짐이 심해도 실리프팅만으로 충분한가요? | concern:P3, concern:P3-1, concern:P3-2, concern:P3-3 | 실리프팅만으로→실리프팅: family:M7 |  | 시작 노드 concern:P3-1 사실 0(§1 빈 노드) |
| Q203 | no_start | 항응고제를 먹는데 주사 시술 받을 수 있나요? |  | 항응고제를→항응고제: check_condition:C-ANTICOAG |  | resolve 0 → 조사 · 사전 보강으로 시작 가능 |
| Q204 | no_start | 피부에 감염이 있으면 미용 시술을 미뤄야 하나요? |  |  | 감염 → check_condition:C-INFECT(확인 조건 match_pattern · 사전엔 없음) | resolve 0 → 조사 · 사전 보강으로 시작 가능 |
| Q205 | no_start | 여러 시술을 묶어 받으면 항상 효과가 더 좋나요? |  |  |  | resolve 0 · 원천에 노드 말 없음(일반 질문) |
| Q206 | no_start | 시술 후 평소와 다른 극심한 통증은 언제 연락하나요? |  |  |  | resolve 0 · 원천에 노드 말 없음(일반 질문) |
| Q238 | no_start | 처음 받는 쁘띠 시술은 무엇부터 시작하면 좋아요? |  |  | 쁘띠 → menu 쁘띠시술(RC-PC-P1-1~3 · 원장 combo-recipes 「동안 쁘띠 패키지」 · problem-combos P1) | resolve 0 → 조사 · 사전 보강으로 시작 가능 |

원인 셈: resolve 0 4 · resolve 0 · 원천에 노드 말 없음 3 · 시작 노드 사실 0 3 · 후보 있음 · Jev 「해당 없음」 4 · 후보가 트리 항목 1

참고: 「PN·PDRN 제품은 …」 질문 통째 resolve 는 0 인데 「PN」 · 「PDRN」 낱말 하나씩은 U5-018 에 닿음(접두 단계 · 낱말 하나일 때만) — 질의 쪽 낱말 나눔 · 조사 떼기 문제.

### 3-1. 239 문항 resolve 「unmatched」 말 빈도(서로 다른 말 485 · 합 979)

상위 25(대부분 기능어):  후 53 · 되나요? 34 · 있나요? 26 · 수 22 · 하나요? 18 · 같은 17 · 받아도 14 · 얼마나 11 · 날 10 · 더 10 · 받을 10 · 어떻게 10 · 피부가 10 · 달라요? 9 · 시술 9 · 맞나요? 8 · 바로 8 · 받으면 8 · 어떤 8 · 언제 8 · 중 8 · 가능해요? 7 · 돼요? 7 · 없어지나요? 7 · 맞아도 6

**낱말 하나로 resolve 하면 닿는 말 34개(문항 등장 37)** — 그중 **조사를 떼야 닿는 말 25** · 나머지 9 은 조사 없이도 낱말 하나면 닿는데 질문 통째로는 안 닿은 말(질의 낱말 나눔 · 접두 단계 문제). 「주사 · 장비 → concern:P13」 · 「볼살 → PU-07」 같은 접두 일치는 맞는지 사람 확인:

| 말 | 등장 | 뗀 꼴 | 닿는 노드 | 문항 |
|---|---|---|---|---|
| 마취까지 | 2 | 마취 | check_condition:C-LIDO | Q215, Q219 |
| 주사 | 2 | 주사 | concern:P13 | Q126, Q203 |
| 주사는 | 2 | 주사 | concern:P13 | Q054, Q207 |
| PDRN | 1 | PDRN | unit_procedure:U5-018 | Q066 |
| PN | 1 | PN | unit_procedure:U5-018 | Q066 |
| 기기 | 1 | 기기 | family:M9 | Q198 |
| 깊은 | 1 | 깊은 | concern:P2-2 | Q175 |
| 레이저만 | 1 | 레이저 | family:M8 | Q117 |
| 레이저만으로 | 1 | 레이저 | family:M8 | Q132 |
| 레이저부터 | 1 | 레이저 | family:M8 | Q144 |
| 레티노이드 | 1 | 레티노이드 | check_condition:C-RETIN | Q172 |
| 리프팅만으로 | 1 | 리프팅 | concern:P3, concern:P4-1, family:M9 | Q086 |
| 마취가 | 1 | 마취 | check_condition:C-LIDO | Q046 |
| 보톡스만으로 | 1 | 보톡스 | concern:P14-3, family:M1, product:M1-2-1 | Q237 |
| 복부나 | 1 | 복부 | site:site.abdomen | Q218 |
| 볼살이 | 1 | 볼살 | purpose:PU-07 | Q074 |
| 수술 | 1 | 수술 | concern:P9-3 | Q197 |
| 스킨부스터의 | 1 | 스킨부스터 | family:M4 | Q071 |
| 실리프팅만으로 | 1 | 실리프팅 | family:M7 | Q187 |
| 알레르기가 | 1 | 알레르기 | check_condition:C-ALLERGY | Q066 |
| 울쎄라의 | 1 | 울쎄라 | product:M9-1-1, product:M9-1-2, unit_procedure:U5-102 | Q212 |
| 장비 | 1 | 장비 | concern:P13 | Q075 |
| 주름에도 | 1 | 주름에 | concern:P2, unit_procedure:U5-001, unit_procedure:U5-002 | Q028 |
| 주사도 | 1 | 주사 | concern:P13 | Q236 |
| 주사를 | 1 | 주사 | concern:P13 | Q233 |
| 주사와 | 1 | 주사 | concern:P13 | Q215 |
| 팔뚝에도 | 1 | 팔뚝에 | site:site.upper-arm | Q218 |
| 팔자주름에는 | 1 | 팔자주름에 | concern:auto-83-1774737181584 | Q043 |
| 표정을 | 1 | 표정 | concern:P2-1 | Q028 |
| 표정이 | 1 | 표정 | concern:P2-1 | Q030 |
| 항응고제를 | 1 | 항응고제 | check_condition:C-ANTICOAG | Q203 |
| 활동성 | 1 | 활동성 | check_condition:C-ACNE | Q096 |
| 흉터나 | 1 | 흉터 | concern:P9 | Q197 |
| 흉터에도 | 1 | 흉터에 | concern:P9 | Q138 |

**조사 떼도 안 닿고 원장에는 있는 내용 말 167개** — 그중 확인 조건 match_pattern 에만 있는 말 4(염증, 감염, 켈로이드, 피부염) · 나머지 앞 40: 받아(14 · 원장 2) · 얼마(11 · 원장 2) · 어떤(8 · 원장 2) · 맞아(6 · 원장 1) · 어느(4 · 원장 8) · 때문(3 · 원장 6) · 멍과(3 · 원장 2) · 있어(3 · 원장 33) · 전에(3 · 원장 11) · 지방(3 · 원장 518) · 햇빛(3 · 원장 5) · 흑자(3 · 원장 15) · 계속(2 · 원장 3) · 다시(2 · 원장 22) · 동시(2 · 원장 204) · 번만(2 · 원장 1) · 부위(2 · 원장 879) · 붓기(2 · 원장 56) · 사우나(2 · 원장 123) · 생길(2 · 원장 12) · 시간(2 · 원장 406) · 여드름약(2 · 원장 1) · 염증(2 · 원장 162) · 자국(2 · 원장 20) · 자극(2 · 원장 414) · 자주(2 · 원장 73) · 줄여(2 · 원장 14) · 초음파(2 · 원장 88) · 추천(2 · 원장 30) · 콜라겐(2 · 원장 698) · 통증(2 · 원장 205) · 패인(2 · 원장 1) · 피해야(2 · 원장 4) · 함께(2 · 원장 73) · 화상(2 · 원장 69) · 화장(2 · 원장 126) · 0개(1 · 원장 12) · 6주(1 · 원장 96) · HA(1 · 원장 448) · 가벼운(1 · 원장 88)

**입구 사전 후보 = 31**(조사 떼기로 닿는 말 25 · 확인 조건 match_pattern → 사전 4 · 원장 근거 새 표현 2: 「쁘띠」 → 메뉴 쁘띠시술 · 「초음파」 → M9). 「손주사 · 기계주사」 는 원장 0 → 사전 후보 아님(사람 확인).

## 4. 효과 추정 — fullrun-v2 case3 실패 행 중 닫힐 가능성(행 단위)

case3 실패 행(5 항목 중 하나라도 실패) = 101 · 항목별 실패 {'accuracy': 77, 'candidates': 5, 'on_topic': 13, 'safety': 28, 'uncertainty': 1} · 답에 「정보 없음」류 문구 86 행 · 판사 실패 주장 중 「정보 없음이라 했다」 류 71.

판사 인용(원장 quote)의 커버리지 판정: {'①': 111, '②': 8, '③': 3, '④': 1} → **실패 인용의 대부분(①)은 골드 fact 에 이미 있음** — 「원장 → 골드 미적재」 보다 「걸음이 그 노드 · 섹션에 못 감」 이 큼(rerun-v8a 「못 받음」 과 같은 방향).

| 문항 | 질문 | 실패 항목 | 닫힐 근거 |
|---|---|---|---|
| Q007 | 피부결이 거칠어요 | candidates | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:J10) · E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q025 | 쁘띠시술 추천 패키지 뭐 있어요? | accuracy, safety | B' 메뉴 후보를 시작으로(쁘띠시술 → 조합) |
| Q043 | 팔자주름에는 무조건 필러가 맞나요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P2, concern:auto-83-1774737181584, concern:auto-84-1774737181584) |
| Q066 | PN·PDRN 제품은 생선 알레르기가 있어도 맞나요? | accuracy, safety | B 입구(조사 · 사전) → 시작 노드 생김 |
| Q067 | 쥬베룩과 일반 HA 필러는 뭐가 달라요? | accuracy, candidates | E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q071 | 스킨부스터의 정확한 주입 용량은 얼마가 맞나요? | accuracy, candidates | E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q086 | 피부 처짐과 지방 때문에 턱선이 흐린데 리프팅만으로 되나요? | accuracy, safety | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P11, concern:P3) |
| Q106 | 점 빼는 레이저와 기미 토닝은 같은가요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(combo:RC-CP-pigment) |
| Q112 | 색소 레이저 후 리쥬란을 바로 맞아도 되나요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P5) |
| Q117 | 여드름 레이저만 받으면 약 없이 낫나요? | accuracy | A 빈 시작 노드(concern:P6) 채움 → 걷기 시작 · C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(combo:RC-CP-acne) |
| Q122 | 갈색 여드름 자국과 흉터는 같은 건가요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P6) · E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q127 | 여드름 레이저를 몇 번 받아야 하나요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P6) |
| Q132 | 여드름 흉터는 레이저만으로 없어지나요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P6, concern:P9) |
| Q139 | 서브시전과 프락셔널 레이저는 뭘 먼저 하나요? | accuracy, on_topic | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P9-1) |
| Q144 | 여드름 자국이 남아 있는데 흉터 레이저부터 받나요? | accuracy | A 빈 시작 노드(concern:P6) 채움 → 걷기 시작 |
| Q147 | 레이저 제모는 한 번이면 끝나나요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P10) |
| Q159 | 수염 제모와 팔 제모는 횟수가 같나요? | accuracy | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:P10) · E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q162 | 화학적 필링과 프락셔널 레이저는 뭐가 달라요? | accuracy | E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q187 | 처짐이 심해도 실리프팅만으로 충분한가요? | safety | A 빈 시작 노드(concern:P3-1) 채움 → 걷기 시작 |
| Q192 | 바디 고주파가 체중을 크게 줄여 주나요? | accuracy, safety, candidates | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(combo:RC-CP-body_contouring) · E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q202 | 이소트레티노인 먹는 중 프락셔널 레이저 가능해요? | accuracy, uncertainty | E 실패 인용이 골드 fact 아님(②) → 커버리지 보강 |
| Q203 | 항응고제를 먹는데 주사 시술 받을 수 있나요? | safety | B 입구(조사 · 사전) → 시작 노드 생김 |
| Q204 | 피부에 감염이 있으면 미용 시술을 미뤄야 하나요? | accuracy, on_topic | B 입구(조사 · 사전) → 시작 노드 생김 |
| Q212 | 슈링크와 울쎄라의 효과와 유지 기간은 어떻게 달라요? | accuracy | E 실패 인용이 골드 fact 아님(③) → 커버리지 보강 |
| Q214 | LDM은 한 번만 받아도 체감할 수 있나요? | accuracy | E 실패 인용이 골드 fact 아님(③) → 커버리지 보강 |
| Q216 | 물광주사 시술에는 시간이 얼마나 걸려요? | on_topic | E 실패 인용이 골드 fact 아님(④) → 커버리지 보강 |
| Q221 | 어떤 종류의 리프팅 실이 저에게 맞나요? | accuracy | E 실패 인용이 골드 fact 아님(③) → 커버리지 보강 |
| Q237 | 팔자주름을 보톡스만으로 펼 수 있나요? | accuracy, safety | C 실패 인용이 걸은 빈 노드의 원천 재료에 있음(concern:auto-83-1774737181584) |
| Q238 | 처음 받는 쁘띠 시술은 무엇부터 시작하면 좋아요? | on_topic | B 입구(조사 · 사전) → 시작 노드 생김 · D 고립 노드 연결(combo:RC-PC-P1-1) |

**닫힐 가능성 행 = 29** / 실패 101(on_topic 실패 4 / 13 · 「정보 없음」류 답 26 / 86). 근거별: A 3 · B 5 · C 14 · D 1 · E 12. 「가능성」 = 그 근거가 고쳐지면 걸음이 원천 근거에 닿을 수 있는 행(답 생성 · 채점 흔들림 15~20% 는 안 셈) — 상한에 가까운 추정.

on_topic 실패 중 위 근거로 안 닫히는 행: Q016, Q018, Q046, Q047, Q069, Q102, Q133, Q164, Q206 — A~E 근거에 안 걸림(원인 미분류 · Q206 은 시작 노드 없는 일반 질문).

## 5. 설계 초안 — 실버 10단계(가칭 · 노드 설명 사실) · 사전 보강 · 고립 연결 (적용 금지)

### 5-1. 레코드 꼴(9단계 records 와 같은 꼴 · 새 owner 종류만)

```json
{"id": "S10:<원장 파일>.<구체 경로>", "owner": "concern:P6", "section": "overview|site_caution|market|evidence|method",
 "kind": "이름 · 별칭 | 영문 | 위치 | 위험 등급 | 대표 시술 | 가격 | 하위 항목 요약 | 정의(원천에 있을 때만)",
 "text": "<원문 그대로>", "origin": {"file": "anatomy-danger-zones", "path": "zones[5].danger_level"},
 "rule": "N10-1 자기 레코드", "class": "한 원천|여러 원천", "same_as": [], "status": "자동|사람 확인"}
```
### 5-2. 붙이는 규칙(추천)

- **N10-1 자기 레코드**: 이름 칸 = 노드 이름 · 실버 동의어 · 사전 표현(조건 없는 행)인 원장 레코드의 바로 아래 잎 → 그 노드 fact. 섹션 = 재료 종류(위치 · 위험 → site_caution · 가격 → market · 정의 · 설명 → overview · 대표 시술 → overview(목록 한 줄)). id 류 · 리니지 칸은 안 붙임
- **N10-2 하위 항목 요약**: 자기 레코드 아래 하위 항목(시술 · 제품 · 패키지)은 원문을 복사하지 않고 「하위 N개 — 이름 목록」 한 fact + 이미 있는 하위 노드 id 참조(DB 는 가리키기만 원칙)
- **N10-3 같은 글 합침**: 같은 원문이 여러 레코드 → 하나(class 여러 원천 · same_as) — 9단계 D9-3 ① 그대로
- **N10-4 정의 없음은 만들지 않음**: 정의 문장이 원장에 없으면 fact 를 만들지 않고 `state: 정보 없음(gap)` 한 줄(현 골드 gap 규칙) — 답은 「원장에 정의 없음 + 위치 · 시술은 이렇다」 로
- **N10-5 괄호 별칭**: 자동으로 안 붙임 — 후보 목록 → 사람 확인(잡음 큼: 「볼 (처짐)」 같은 꼴)
### 5-3. 사전 보강 규칙(추천)

- **D-a 질의 조사 떼기**: resolve 질의 쪽에서 낱말 끝 조사(5-3 목록) 떼고 다시 완전 일치 — 사전 행 추가 없음 · 10-30 「허브 resolve 조사 떼기(질의 쪽)」 결정의 실행
- **D-b 확인 조건 match_pattern → 사전**: check_condition 의 match_pattern 낱말(감염 · 염증 · 결핵 …)을 사전 표현으로(mode 후보)
- **D-c 메뉴 접두**: 「쁘띠」 → 메뉴 쁘띠시술(J5 메뉴 경로 · 원장 combo-recipes 「동안 쁘띠 패키지」)
- **D-d 괄호 별칭 중 원장 근거 있는 것**: 「초음파」 → M9(「고강도 집속 초음파 (HIFU)」) — 후보 목록은 사람 확인
### 5-4. 고립 연결 규칙(추천)

- **L-a 연간 플랜**: annual_plans.schedule[].procedures 를 7단계 R21~R24(이름 · 부위 · 제품으로 내림)로 combo_component · focus 낱말을 고민 앵커로(R12~R22)
- **L-b 메뉴 조합**: 앵커 없는 메뉴 조합은 계열 엣지(combo_component → family)라도 냄 — RC-PC-P1-1 → M1
- **L-c 8단계 출처**: 주장 used_by 가 있는 evidence_source 는 주장이 붙은 엣지 evidence 에 출처 id(또는 cites_claim 엣지)
- **L-d 목적 PU-09 · PU-11**: 메뉴 M16 하위 단위 시술로 treats — 효과 문장 없음 → 사람 확인
### 5-5. 「사람 확인」 자리

- 괄호 별칭 후보 637(빈 노드 · 잡음 큼) · 사전 밖 말 「손주사 · 기계주사」(원장 0) · 목적 PU-09 · PU-11 treats · 정의 없는 노드 261 중 정의 문장을 원천 보강할지(의료진 · 새 원천) · 결정과 실물이 다른 5단계 2칸(ingredient_basis 6 · naming_caveat 6)
### 5-6. decisions 초안(추천값)

| id | 질문 | 추천 | 근거 |
|---|---|---|---|
| D10-1 | 빈 노드에 원장 자기 레코드 잎을 fact 로 붙일까 | 붙임(N10-1 · 섹션은 재료 종류) — 하위 항목은 요약 한 줄(N10-2) | 빈 노드 151 중 재료 있음 82 |
| D10-2 | 정의 문장이 원장에 없는 노드 | 만들지 않음 · gap 표시(N10-4) — 정의 원천 보강은 별도 결정 | 7 종류 261 노드 정의 없음 |
| D10-3 | resolve 질의 조사 떼기 | 넣음(D-a · 질의 쪽만) | 조사를 떼야 닿는 말 25 · 낱말 하나면 닿는 말 34 · 되돌아감 Q066 · Q203 |
| D10-4 | 확인 조건 match_pattern 을 사전으로 | 넣음(D-b · mode 후보) | Q204 「감염」 → C-INFECT |
| D10-5 | 「쁘띠」 메뉴 접두 · 「초음파」 → M9 | 넣음(D-c · D-d) | Q238 · Q082 |
| D10-6 | 고립 조합 4 · evidence_source 38 연결 | L-a · L-b · L-c 대로 | Q238 정답 인용이 고립 RC-PC-P1-1 에 있음 |
| D10-7 | 커버리지 ② 속성만(내용 칸) 을 fact 로 | 판매 문구 · 시장가 · site_caution 위치는 fact 화 · 식별자 · 출처 표기 · 동의어는 그대로 | §0-5 |
| D10-8 | 결정 없이 · 결정과 다르게 빠진 ④ | 5단계 ingredient_basis · naming_caveat 는 결정대로 실음(원문) · extracted 리니지 4칸은 브론즈 메타로 두고 안 실음 · 나머지는 원문 보관 | §0-4 |
### 5-7. 아직 안 정한 것

- 10단계를 실버 단계로 둘지 · 골드 빌드 규칙(gold-prep)으로 둘지(실버 정본에 owner 를 노드 id 로 쓰는 첫 단계)
- case3 걸음이 빈 노드의 새 fact 를 실제로 받는지 — 의도 묶음(I-02 overview+method 등)에 site_caution · market 이 없어 시작 노드에서 안 펼칠 수 있음(SPEC-006 몫)
- 효과 추정은 상한 — 실제는 재빌드 뒤 같은 50/239 재측정으로만 확인

## 요약 숫자

```json
{
 "coverage": {
  "leaves": 23783,
  "judged": 23509,
  "①": 18338,
  "②": 4451,
  "③": 556,
  "④": 164
 },
 "coverage_rate": {
  "①": 0.78,
  "②": 0.1893,
  "③": 0.0237,
  "④": 0.007
 },
 "undecided_missing_paths": 21,
 "undecided_missing_leaves": 91,
 "empty_nodes": 151,
 "empty_with_material": 82,
 "empty_with_definition": 11,
 "no_definition_nodes_all7": 261,
 "isolated": 49,
 "isolated_linkable": 44,
 "entry_dict_candidates": 31,
 "strip_josa_hits": 25,
 "single_word_hits": 34,
 "fail_rows": 101,
 "closable_rows": 29
}
```
