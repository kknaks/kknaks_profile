# 실버 9단계 조사 — 설명 사실 (read-only · 설계안)

> 조사 · 설계만 · 2026-11-01 · 결정 아님. 데이터 · 실버 · 골드 수정 없음. 기계용 정본 `step9-research.json`(`step9-research.py` · 결정론 — 두 번 돌려 바이트 같음). 결정 초안 `step9-decisions.json`. **원장 인용은 이 work/ 파일 안에만**(공개 레포 — 커밋 안 함).

## ① 한 줄

설명 사실 원장 필드 **76개 · 6,429행**(골드 fact 로 이미 있음 1,481 · 실버에만 1,425 · 둘 다 없음 3,523). 붙는 자리는 **새 대응표 없이** 5단계(`extracted[].attach` · `taxonomy_products`) · 7단계(고민 항목 resolve) · 8단계(complications · side_effects)가 이미 정한 길로 풀린다 → **사람 확인 0**. 효과: 2차 A 54 중 **이 단계(실버)로 42 · 골드 section 추가만으로 11 · 못 닫음 1** / rerun-v5a case3 A 30(이 조사 셈) 중 **실버로 20 · 골드 section 으로 6 · 못 닫음 4**(라벨 · 메타 칸).

## ② 셈

| 종류 | 이름 | 필드 | 행 | 골드 fact 있음 | 실버에만 | 둘 다 없음 | 붙는 노드 있음 | 골드 section(제안) |
|---|---|---|---|---|---|---|---|---|
| K1 | 효과 시작 · 지속 | 15 | 1,283 | 456 | 180 | 647 | 1,199 | recovery |
| K2 | 작용 원리 | 5 | 631 | 0 | 16 | 615 | 590 | method |
| K3 | 개요 · 설명 | 7 | 1,235 | 440 | 449 | 346 | 1,143 | overview |
| K4 | 적응증 | 9 | 2,267 | 161 | 345 | 1,761 | 2,115 | overview |
| K5 | 합병증 설명 | 7 | 435 | 242 | 193 | 0 | 435 | safety.management(새 · V-4) · 관리 외 칸은 safety.complications |
| K6 | 반응 · 중증도 단계(값 사전) | 8 | 8 | 0 | 0 | 8 | 8 | global(값 사전) |
| K7 | 제품 메모 | 14 | 89 | 10 | 44 | 35 | 80 | products(제품 노드 overview) |
| K8 | 대안 | 1 | 125 | 14 | 0 | 111 | 115 | overview(고민 노드) |
| K9 | 관련 기법 | 2 | 102 | 0 | 102 | 0 | 102 | method |
| K10 | 최적화 중증도 단계 | 7 | 139 | 132 | 7 | 0 | 0 | evidence(이미) |
| K11 | 고민 상세 | 1 | 115 | 26 | 89 | 0 | 105 | overview(고민 노드) |
| 합 | | 76 | 6,429 | 1,481 | 1,425 | 3,523 | 5,892 | |

- 셈 규칙: 원장 21파일 잎(문자열 · 숫자)을 전부 걷고 경로를 접은 꼴(`[n]` → `[]` · `M1` · `auto-…` 같은 코드 키 → `{code}`)이 아래 「종류 식」에 걸리면 대상. 「A 실패에 나온 필드」가 아니라 **같은 종류 필드 전부**(예: onset_duration 은 items · products · 계열 · extracted.json 네 자리 15필드)
- 종류 식(정규식 · `step9-research.py KINDS`): K1 `onset_duration.` · K2 `extracted.mechanism | moa_summary` · K3 `extracted.overview | items[].detail | subcategories[].description` · K4 `indications.`(contraindications 제외) · K5 `complications…(management|prevention|duration|onset|incidence|mechanism|risk_factors[])` · K6 `reaction_levels | complications.severity_levels` · K7 `products[].(note|ingredient|material|legal_warning|type)` · K8 `alternatives[]` · K9 `related_techniques[]` · K10 `treatment-optimization…severity_levels[].(rationale|sequence|…)` · K11 `cc_detail | problem 항목 detail`
- 「골드 fact 있음」 = 정규화(소문자 · 공백 · 기호 제거) 문자열이 b031371c 골드 fact 원문과 같거나 8자 이상 서로 포함 · 「실버에만」 = 골드 fact 엔 없고 실버 step1~8 정본 어딘가에 있음(노드 속성 · 원문 보관 · 레코드)
- **K10(최적화 중증도 단계) 은 이미 골드에 있다**(rationale · sequence · expected_sessions · evidence_level 24/24 · 7단계 조합) — SPEC-005 §4-3 V-4 의 「실버에 칸이 없다」는 틀림(스펙 정정 몫 · 9단계 대상 아님)
- **K5(합병증 설명) 은 실버 8단계에 이미 다 있다**(complications 35 + side_effects 72 레코드에 management · prevention · mechanism · onset · incidence · duration · risk_factors) — 골드가 관리 · 예방을 section 으로 안 내보냄(V-4) · 실버 변경 없음

### 대상 필드 전수(76)

| 종류 | 원장 필드 | 파일 | 행 | 골드 fact | 실버에만 | 없음 | 붙음 | 규칙 | 붙는 자리(행) |
|---|---|---|---|---|---|---|---|---|---|
| K1 | `taxonomy.modality[].subcategories[].items[].extracted.onset_duration.duration` | taxonomy | 521 | 203 | 68 | 250 | 484 | R9-1 | 단위 시술 147; 단위 시술 후보 19; 원문 보관(6단계 패키지) 16; 원문 보관(값) 17; 원문 보관(시술 아님(다른 단계)) 2; 원문 보관(시술 아님) 1; 원문 보관(원장님 문의) 1; 제품 × 계열 207; 제품 × 계열 × 키 하위 111 |
| K1 | `taxonomy.modality[].subcategories[].items[].extracted.onset_duration.onset` | taxonomy | 520 | 228 | 81 | 211 | 483 | R9-1 | 단위 시술 147; 단위 시술 후보 19; 원문 보관(6단계 패키지) 16; 원문 보관(값) 17; 원문 보관(시술 아님(다른 단계)) 2; 원문 보관(시술 아님) 1; 원문 보관(원장님 문의) 1; 제품 × 계열 206; 제품 × 계열 × 키 하위 111 |
| K1 | `taxonomy.modality[].products[].extracted.onset_duration.duration` | taxonomy | 59 | 11 | 11 | 37 | 55 | R9-2 | 단위 시술(taxonomy products · 5단계 S8) 1; 제품(taxonomy products) 58 |
| K1 | `taxonomy.modality[].products[].extracted.onset_duration.onset` | taxonomy | 59 | 14 | 15 | 30 | 55 | R9-2 | 단위 시술(taxonomy products · 5단계 S8) 1; 제품(taxonomy products) 58 |
| K1 | `extracted.{code}.onset_duration.duration` | extracted | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(extracted.json 대조본) 17 |
| K1 | `extracted.{code}.onset_duration.onset` | extracted | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(extracted.json 대조본) 17 |
| K1 | `extracted.{code}.onset_duration.peak` | extracted | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(extracted.json 대조본) 17 |
| K1 | `taxonomy.modality[].extracted.onset_duration.duration` | taxonomy | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(taxonomy 정본) 17 |
| K1 | `taxonomy.modality[].extracted.onset_duration.onset` | taxonomy | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(taxonomy 정본) 17 |
| K1 | `taxonomy.modality[].extracted.onset_duration.peak` | taxonomy | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(taxonomy 정본) 17 |
| K1 | `taxonomy.modality[].subcategories[].items[].extracted.onset_duration.peak_effect` | taxonomy | 8 | 0 | 1 | 7 | 7 | R9-1 | 단위 시술 4; 원문 보관(6단계 패키지) 1; 제품 × 계열 3 |
| K1 | `taxonomy.modality[].subcategories[].items[].extracted.onset_duration.peak` | taxonomy | 7 | 0 | 3 | 4 | 6 | R9-1 | 단위 시술 1; 원문 보관(6단계 패키지) 1; 제품 × 계열 5 |
| K1 | `taxonomy.modality[].products[].extracted.onset_duration.peak_effect` | taxonomy | 5 | 0 | 1 | 4 | 5 | R9-2 | 제품(taxonomy products) 5 |
| K1 | `taxonomy.modality[].products[].extracted.onset_duration.diffusion` | taxonomy | 1 | 0 | 0 | 1 | 1 | R9-2 | 제품(taxonomy products) 1 |
| K1 | `taxonomy.modality[].subcategories[].items[].extracted.onset_duration.maintenance` | taxonomy | 1 | 0 | 0 | 1 | 1 | R9-1 | 단위 시술 1 |
| K10 | `treatment-optimization.by_concern[].severity_levels[].evidence_level` | treatment-optimization | 24 | 24 | 0 | 0 | 0 | — | 7단계 조합에 이미 있음 24 |
| K10 | `treatment-optimization.by_concern[].severity_levels[].expected_sessions` | treatment-optimization | 24 | 24 | 0 | 0 | 0 | — | 7단계 조합에 이미 있음 24 |
| K10 | `treatment-optimization.by_concern[].severity_levels[].rationale` | treatment-optimization | 24 | 24 | 0 | 0 | 0 | — | 7단계 조합에 이미 있음 24 |
| K10 | `treatment-optimization.by_concern[].severity_levels[].sequence` | treatment-optimization | 24 | 24 | 0 | 0 | 0 | — | 7단계 조합에 이미 있음 24 |
| K10 | `treatment-optimization.by_concern[].severity_levels[].total_duration` | treatment-optimization | 24 | 17 | 7 | 0 | 0 | — | 7단계 조합에 이미 있음 24 |
| K10 | `treatment-optimization.by_concern[].severity_levels[].contraindicated_combos[]` | treatment-optimization | 17 | 17 | 0 | 0 | 0 | — | 7단계 조합에 이미 있음 17 |
| K10 | `treatment-optimization.by_concern[].severity_levels[].caveats[]` | treatment-optimization | 2 | 2 | 0 | 0 | 0 | — | 7단계 조합에 이미 있음 2 |
| K11 | `problem-packages.problems[].complaints[].cc_detail` | problem-packages | 115 | 26 | 89 | 0 | 105 | R9-5 | 고민 CC → 고민 노드 11; 고민 CC → 붙을 노드 없음(부위) 5; 고민 CC → 붙을 노드 없음(시술 아님) 5; 고민 CC → 시술 이름 항목 → 단위 시술 94 |
| K2 | `taxonomy.modality[].subcategories[].items[].extracted.mechanism` | taxonomy | 521 | 0 | 16 | 505 | 484 | R9-1 | 단위 시술 147; 단위 시술 후보 19; 원문 보관(6단계 패키지) 16; 원문 보관(값) 17; 원문 보관(시술 아님(다른 단계)) 2; 원문 보관(시술 아님) 1; 원문 보관(원장님 문의) 1; 제품 × 계열 207; 제품 × 계열 × 키 하위 111 |
| K2 | `taxonomy.modality[].products[].extracted.mechanism` | taxonomy | 59 | 0 | 0 | 59 | 55 | R9-2 | 단위 시술(taxonomy products · 5단계 S8) 1; 제품(taxonomy products) 58 |
| K2 | `extracted.{code}.mechanism` | extracted | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(extracted.json 대조본) 17 |
| K2 | `procedure-profiles.profiles[].moa_summary` | procedure-profiles | 17 | 0 | 0 | 17 | 17 | R9-4 | 계열(프로파일) 17 |
| K2 | `taxonomy.modality[].extracted.mechanism` | taxonomy | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(taxonomy 정본) 17 |
| K3 | `taxonomy.modality[].subcategories[].items[].extracted.overview` | taxonomy | 521 | 222 | 34 | 265 | 484 | R9-1 | 단위 시술 147; 단위 시술 후보 19; 원문 보관(6단계 패키지) 16; 원문 보관(값) 17; 원문 보관(시술 아님(다른 단계)) 2; 원문 보관(시술 아님) 1; 원문 보관(원장님 문의) 1; 제품 × 계열 207; 제품 × 계열 × 키 하위 111 |
| K3 | `taxonomy.modality[].subcategories[].items[].detail` | taxonomy | 501 | 179 | 322 | 0 | 464 | R9-1 | 단위 시술 146; 단위 시술 후보 14; 원문 보관(6단계 패키지) 16; 원문 보관(값) 17; 원문 보관(시술 아님(다른 단계)) 2; 원문 보관(시술 아님) 1; 원문 보관(원장님 문의) 1; 제품 × 계열 194; 제품 × 계열 × 키 하위 110 |
| K3 | `taxonomy.problem[].subcategories[].items[].detail` | taxonomy | 117 | 27 | 90 | 0 | 106 | R9-5 | 고민 항목 → 고민 노드 11; 고민 항목 → 붙을 노드 없음(부위) 5; 고민 항목 → 붙을 노드 없음(시술 아님) 5; 고민 항목 → 붙을 노드 없음(시술 이름) 1; 고민 항목 → 시술 이름 항목 → 단위 시술 95 |
| K3 | `taxonomy.modality[].products[].extracted.overview` | taxonomy | 59 | 12 | 3 | 44 | 55 | R9-2 | 단위 시술(taxonomy products · 5단계 S8) 1; 제품(taxonomy products) 58 |
| K3 | `extracted.{code}.overview` | extracted | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(extracted.json 대조본) 17 |
| K3 | `taxonomy.modality[].extracted.overview` | taxonomy | 17 | 0 | 0 | 17 | 17 | R9-3 | 계열(taxonomy 정본) 17 |
| K3 | `taxonomy.modality[].subcategories[].description` | taxonomy | 3 | 0 | 0 | 3 | 0 | — | 규칙 밖 3 |
| K4 | `taxonomy.modality[].subcategories[].items[].extracted.indications.primary[]` | taxonomy | 1656 | 132 | 262 | 1262 | 1527 | R9-1 | 단위 시술 448; 단위 시술 후보 65; 원문 보관(6단계 패키지) 59; 원문 보관(값) 61; 원문 보관(시술 아님(다른 단계)) 4; 원문 보관(시술 아님) 3; 원문 보관(원장님 문의) 2; 제품 × 계열 636; 제품 × 계열 × 키 하위 378 |
| K4 | `taxonomy.modality[].products[].extracted.indications.primary[]` | taxonomy | 256 | 18 | 58 | 180 | 237 | R9-2 | 단위 시술(taxonomy products · 5단계 S8) 3; 제품(taxonomy products) 253 |
| K4 | `extracted.{code}.indications.extended[]` | extracted | 101 | 2 | 6 | 93 | 101 | R9-3 | 계열(extracted.json 대조본) 101 |
| K4 | `taxonomy.modality[].extracted.indications.extended[]` | taxonomy | 100 | 2 | 6 | 92 | 100 | R9-3 | 계열(taxonomy 정본) 100 |
| K4 | `extracted.{code}.indications.primary[]` | extracted | 56 | 1 | 3 | 52 | 56 | R9-3 | 계열(extracted.json 대조본) 56 |
| K4 | `taxonomy.modality[].extracted.indications.primary[]` | taxonomy | 56 | 1 | 3 | 52 | 56 | R9-3 | 계열(taxonomy 정본) 56 |
| K4 | `taxonomy.modality[].subcategories[].items[].extracted.indications.secondary[]` | taxonomy | 18 | 3 | 2 | 13 | 16 | R9-1 | 단위 시술 3; 원문 보관(6단계 패키지) 2; 제품 × 계열 13 |
| K4 | `taxonomy.modality[].products[].extracted.indications.secondary[]` | taxonomy | 14 | 2 | 2 | 10 | 14 | R9-2 | 제품(taxonomy products) 14 |
| K4 | `taxonomy.modality[].subcategories[].items[].extracted.indications.extended[]` | taxonomy | 10 | 0 | 3 | 7 | 8 | R9-1 | 단위 시술 6; 원문 보관(6단계 패키지) 2; 제품 × 계열 2 |
| K5 | `complications.categories[].complications[].risk_factors[]` | complications | 92 | 79 | 13 | 0 | 92 | R9-6 | 부작용(8단계 실버 side_effects · 계열에 붙음) 13; 합병증(8단계 실버 complications · 노드) 79 |
| K5 | `complications.categories[].complications[].incidence` | complications | 65 | 30 | 35 | 0 | 65 | R9-6 | 부작용(8단계 실버 side_effects · 계열에 붙음) 38; 합병증(8단계 실버 complications · 노드) 27 |
| K5 | `complications.categories[].complications[].management` | complications | 65 | 27 | 38 | 0 | 65 | R9-6 | 부작용(8단계 실버 side_effects · 계열에 붙음) 38; 합병증(8단계 실버 complications · 노드) 27 |
| K5 | `complications.categories[].complications[].mechanism` | complications | 65 | 27 | 38 | 0 | 65 | R9-6 | 부작용(8단계 실버 side_effects · 계열에 붙음) 38; 합병증(8단계 실버 complications · 노드) 27 |
| K5 | `complications.categories[].complications[].onset` | complications | 65 | 36 | 29 | 0 | 65 | R9-6 | 부작용(8단계 실버 side_effects · 계열에 붙음) 38; 합병증(8단계 실버 complications · 노드) 27 |
| K5 | `complications.categories[].complications[].prevention` | complications | 64 | 27 | 37 | 0 | 64 | R9-6 | 부작용(8단계 실버 side_effects · 계열에 붙음) 37; 합병증(8단계 실버 complications · 노드) 27 |
| K5 | `complications.categories[].complications[].duration` | complications | 19 | 16 | 3 | 0 | 19 | R9-6 | 부작용(8단계 실버 side_effects · 계열에 붙음) 3; 합병증(8단계 실버 complications · 노드) 16 |
| K6 | `complications.severity_levels.critical` | complications | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K6 | `complications.severity_levels.mild` | complications | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K6 | `complications.severity_levels.moderate` | complications | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K6 | `complications.severity_levels.severe` | complications | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K6 | `post-procedure-timeline.reaction_levels.abnormal` | post-procedure-timeline | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K6 | `post-procedure-timeline.reaction_levels.caution` | post-procedure-timeline | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K6 | `post-procedure-timeline.reaction_levels.emergency` | post-procedure-timeline | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K6 | `post-procedure-timeline.reaction_levels.normal` | post-procedure-timeline | 1 | 0 | 0 | 1 | 1 | R9-7 | 값 사전(시맨틱 · B02) 1 |
| K7 | `taxonomy.modality[].products[].type` | taxonomy | 24 | 5 | 14 | 5 | 22 | R9-2 | 제품(taxonomy products) 24 |
| K7 | `products.energy_device.products[].type` | products | 18 | 5 | 11 | 2 | 15 | R9-2 | products.json → 이름이 taxonomy products 에 없음 1; products.json → 제품(taxonomy products) 17 |
| K7 | `taxonomy.modality[].products[].ingredient` | taxonomy | 9 | 0 | 5 | 4 | 8 | R9-2 | 제품(taxonomy products) 9 |
| K7 | `products.biostimulator.products[].ingredient` | products | 6 | 0 | 3 | 3 | 5 | R9-2 | products.json → 제품(taxonomy products) 6 |
| K7 | `products.prp_exosome.products[].type` | products | 5 | 0 | 2 | 3 | 5 | R9-2 | products.json → 제품(taxonomy products) 5 |
| K7 | `products.thread_lift.products[].material` | products | 5 | 0 | 4 | 1 | 5 | R9-2 | products.json → 제품(taxonomy products) 5 |
| K7 | `taxonomy.modality[].products[].material` | taxonomy | 5 | 0 | 4 | 1 | 5 | R9-2 | 제품(taxonomy products) 5 |
| K7 | `taxonomy.modality[].products[].note` | taxonomy | 5 | 0 | 0 | 5 | 4 | R9-2 | 단위 시술(taxonomy products · 5단계 S8) 1; 제품(taxonomy products) 4 |
| K7 | `products.skin_booster.products[].ingredient` | products | 3 | 0 | 0 | 3 | 3 | R9-2 | products.json → 제품(taxonomy products) 3 |
| K7 | `products.prp_exosome.products[].legal_warning` | products | 2 | 0 | 0 | 2 | 2 | R9-2 | products.json → 제품(taxonomy products) 2 |
| K7 | `products.prp_exosome.products[].note` | products | 2 | 0 | 0 | 2 | 2 | R9-2 | products.json → 제품(taxonomy products) 2 |
| K7 | `products.skin_booster.products[].note` | products | 2 | 0 | 0 | 2 | 2 | R9-2 | products.json → 단위 시술(taxonomy products · 5단계 S8) 1; products.json → 제품(taxonomy products) 1 |
| K7 | `products.stem_cell.products[].type` | products | 2 | 0 | 1 | 1 | 2 | R9-2 | products.json → 제품(taxonomy products) 2 |
| K7 | `products.botulinum_toxin.products[].note` | products | 1 | 0 | 0 | 1 | 0 | R9-2 | products.json → 제품(taxonomy products) 1 |
| K8 | `problem-packages.problems[].complaints[].alternatives[]` | problem-packages | 125 | 14 | 0 | 111 | 115 | R9-5 | 고민 CC → 고민 노드 11; 고민 CC → 붙을 노드 없음(부위) 5; 고민 CC → 붙을 노드 없음(시술 아님) 5; 고민 CC → 시술 이름 항목 → 단위 시술 104 |
| K9 | `extracted.{code}.related_techniques[]` | extracted | 51 | 0 | 51 | 0 | 51 | R9-3 | 계열(extracted.json 대조본) 51 |
| K9 | `taxonomy.modality[].extracted.related_techniques[]` | taxonomy | 51 | 0 | 51 | 0 | 51 | R9-3 | 계열(taxonomy 정본) 51 |

원문 예(필드마다 첫 행 · 원장 그대로)는 `step9-research.json fields[].example_path · example_text`.

## ③ 붙는 자리 · 중복 · 충돌

| 붙는 자리(행) | 행 |
|---|---|
| 제품 × 계열 | 1,680 |
| 단위 시술 | 1,197 |
| 제품 × 계열 × 키 하위 | 932 |
| 제품(taxonomy products) | 547 |
| 계열(extracted.json 대조본) | 293 |
| 계열(taxonomy 정본) | 292 |
| 합병증(8단계 실버 complications · 노드) | 230 |
| 부작용(8단계 실버 side_effects · 계열에 붙음) | 205 |
| 고민 CC → 시술 이름 항목 → 단위 시술 | 198 |
| 단위 시술 후보 | 155 |
| 원문 보관(값) | 146 |
| 원문 보관(6단계 패키지) | 145 |
| 7단계 조합에 이미 있음 | 139 |
| 고민 항목 → 시술 이름 항목 → 단위 시술 | 95 |
| products.json → 제품(taxonomy products) | 44 |
| 고민 CC → 고민 노드 | 22 |
| 계열(프로파일) | 17 |
| 원문 보관(시술 아님(다른 단계)) | 14 |
| 고민 항목 → 고민 노드 | 11 |
| 고민 CC → 붙을 노드 없음(부위) | 10 |
| 고민 CC → 붙을 노드 없음(시술 아님) | 10 |
| 값 사전(시맨틱 · B02) | 8 |
| 단위 시술(taxonomy products · 5단계 S8) | 8 |
| 원문 보관(시술 아님) | 8 |
| 원문 보관(원장님 문의) | 7 |
| 고민 항목 → 붙을 노드 없음(부위) | 5 |
| 고민 항목 → 붙을 노드 없음(시술 아님) | 5 |
| 규칙 밖 | 3 |
| products.json → 단위 시술(taxonomy products · 5단계 S8) | 1 |
| products.json → 이름이 taxonomy products 에 없음 | 1 |
| 고민 항목 → 붙을 노드 없음(시술 이름) | 1 |

- 원장 항목 521(items)의 설명 키는 **5단계가 이미 정한 `extracted[].attach`** 를 따른다 — 5단계 `extracted[].keys` 에 mechanism · overview · onset_duration.* · indications.* 가 적혀 있는데 `source_text` 는 aftercare · safety 만 끌어올렸다(`step5-units.json extracted[]` · 521/521). 9단계는 **같은 레코드의 나머지 키**를 끌어올리는 일
- taxonomy products 59 = 5단계 `taxonomy_products`(제품 58 · 스킨보톡스 M4-P-3 = 단위 시술 U5-009 · S8). products.json 은 B15 대조본 — 이름으로 taxonomy products 에 대고(45/46), 없는 1(볼뉴머)은 5단계 원장 항목 이름(auto-M4-1775362490962 → 제품 M9-2-3)으로(R9-2b)
- 고민 쪽(alternatives · cc_detail · 고민 항목 detail)은 7단계 `correspondence`(CC 115 → 항목) → 항목이 고민 노드면 그 노드 · 항목의 concern · 시술 이름 항목이면 resolve 단위 시술. **부위 · 시술 아님 항목(30행)은 붙일 노드가 없다**(B09 — 부위 + 목적으로 분해한 항목)
- 「원문 보관」 37항목(320행)은 5단계 행선지 결정(6단계 패키지 · 값 · 시술 아님 · 원장님 문의) 그대로 붙이지 않는다(D9-6)

**중복 · 충돌** — 같은 노드 · 같은 칸(slot)에 원천 레코드가 둘 이상인 자리 803(전 slot 2,918) 중 값이 같음 197 · **다름 606**(배열 칸은 레코드마다 값 집합으로 비교):

| 충돌 종류 | slot | 예(원장 그대로) |
|---|---|---|
| 계열 taxonomy ↔ extracted.json | 7 | `family:M12` mechanism: 「MTS 롤러의 미세한 바늘(0.2~2.0mm)이 피부 표피층과 진피층을 」 / 「MTS 롤러의 미세한 바늘(0.2~2.0mm)이 피부 표피층과 진피층을 」 (extracted.M12.mechanism · taxonomy.modality[11].extracted.mechanism) |
| 제품 원장 항목 ↔ taxonomy products | 186 | `product:M1-1-1` onset_duration.duration: 「3-4개월 지속」 / 「약 1개월에 완전한 효과 발현, 3-4개월 지속」 (duration · duration) |
| 제품 원장 항목 여럿 | 79 | `product:M10-1-1` onset_duration.duration: 「3-6개월 유지, 정기적 시술로 지속 효과」 / 「6-9개월」 (duration · duration) |
| 단위 시술 원장 항목 여럿 | 334 | `unit_procedure:U5-009` onset_duration.duration: 「1개월 후 완전한 효과 발현」 / 「3-4개월」 (duration · duration) |

- 계열 taxonomy ↔ extracted.json 7칸은 앞부분이 같고 뒤 문장만 다름(M12 mechanism · overview · M17 · M2 · M5 …) — B15 대로 taxonomy 정본 · 대조본은 source_conflict 리포트(D9-4)
- 단위 시술 · 제품 충돌은 **다른 원장 행이 같은 노드에 붙어서** 생긴다(예 U5-009 = 원장 항목 M1 스킨보톡스 + taxonomy products M4-P-3) — 숫자가 다른 것은 원천이 다르게 적은 것. 하나로 고르면 원천에 있는 말을 「없음」으로 만들어 A 를 다시 만든다 → C9-1 전부 싣기(D9-3)

## ④ 설계안 — 실버 9단계

### 레코드 꼴(record-schema 초안 · `step9-explanations.json`)

```json
{
 "id": "S9-<rule>-<원장 파일>:<원장 경로>",
 "rule": "R9-1",
 "kind": "K1",
 "slot": "onset_duration.duration",
 "text": "<원장 원문 그대로>",
 "source": {
  "file": "taxonomy",
  "path": "taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration",
  "record": "M1-3-6(원장 항목 id)"
 },
 "attach": {
  "nodes": [
   "unit_procedure:U5-010",
   "unit_procedure:U5-011"
  ],
  "level": "단위 시술",
  "via": "step5 extracted[].attach",
  "flags": [
   "candidates?",
   "cc:<CC>?",
   "sub_family?"
  ]
 },
 "status": "붙음 | 원문 보관(<5단계 행선지>) | 대조본 같음(same_as) | source_conflict",
 "same_as": "<같은 값 레코드 id?>",
 "multi_source": true,
 "order": 1,
 "section": "recovery"
}
```

- 필드 이름은 8단계 레코드(`attach` · `source` · `status`)와 같은 말을 쓴다 · `text` 는 원문 그대로(요약 · 다시 쓰기 · 번역 없음) · 숫자 정규화 없음
- 골드 fact id(G9-1) = `{노드}#{section}#step9[{원장 파일}:{원장 경로}]` — 결정론 · 노드가 여럿이면 노드마다 한 fact(같은 원장 경로)

### 붙이는 규칙

| 규칙 | 무엇 | 행 | 붙음 |
|---|---|---|---|
| R9-1 | 원장 항목 extracted 설명 키(mechanism · overview · onset_duration.* · indications.* · items[].detail)는 5단계 `extracted[].attach` 를 그대로 따른다 — 제품 → 제품 노드 · 단위 시술 → 그 단위 · 단위 시술 후보 → 후보 전부 + `candidates` 표시(8단계 aftercare 175 와 같은 선례) · 원문 보관 → 붙이지 않음(레코드에 status 만) | 4284 | 3964 |
| R9-2 | taxonomy products extracted 설명 키 · products[].note · ingredient · material · type 는 5단계 `taxonomy_products[].attach`(제품 · S8 단위 시술) · products.json(B15 대조본)은 이름이 같은 taxonomy products 행에 대어 — taxonomy 에 같은 칸이 있으면 same_as(같음) · source_conflict(다름 · 싣지 않음), taxonomy 에 없는 칸(legal_warning 2 · 일부 ingredient · type)만 싣는다 · 이름이 없으면 5단계 원장 항목 이름 일치(볼뉴머 1 → R9-2b) | 601 | 557 |
| R9-3 | 계열 extracted 설명 키 · related_techniques 는 taxonomy.modality[].extracted 를 정본으로 계열 노드에 · extracted.json 은 대조만(같으면 same_as · 다르면 source_conflict 리포트 7칸 — 싣지 않음 · D9-4) | 585 | 585 |
| R9-4 | procedure-profiles moa_summary 17 → 계열 method(B03 원문 보관 → fact) | 17 | 17 |
| R9-5 | problem-packages alternatives · cc_detail · taxonomy.problem 항목 detail → 7단계 항목 해석(고민 노드 · 항목의 concern · 시술 이름 항목이면 resolve 단위 시술 + `cc:<CC>` 조건 표시) · 부위 · 시술 아님 항목 30행은 붙이지 않음(B09) | 357 | 326 |
| R9-6 | complications.* 설명 칸은 8단계 실버(complications 35 · side_effects 72)에 이미 있다 — 실버 변경 없음 · 골드 빌드가 section 으로 내보냄(D9-1) | 435 | 435 |
| R9-7 | post-procedure-timeline.reaction_levels 4 · complications.severity_levels 4 = 값 사전(B02) → 시맨틱 값 사전 + 골드 globals(D9-7) | 8 | 8 |
| C9-1 | 같은 노드 · 같은 칸에 원천 레코드가 여럿이면 값이 같으면 한 행(same_as) · 다르면 **전부 싣고 고르지 않는다**(설명 문장은 resolved 대상 아님 · D-13e) + `multi_source` 표시 · 순서 = 좁은 원천 먼저(그 노드 자신의 원장 항목 → taxonomy products → 후보) — D9-3 | 2918 | 같음 197 · 다름 606 |
| G9-1 | fact id = `{노드}#{section}#step9[{원장 파일}:{원장 경로}]` · 결정론 · 원문 그대로(요약 · 다시 쓰기 없음) | — | — |

### 충돌 처리

- 「충돌은 보수적으로 하나」(_RESUME §2)는 **앱이 읽는 값**(시술 쌍 resolved · 확인 조건 등급 · 대기 기간)에 쓰는 규칙이다. 설명 문장은 근거(fact)라서 하나로 고르지 않고 원천마다 한 행(C9-1) — 같은 값은 same_as 로 접고, 다른 값은 `multi_source` 표시 + 순서(그 노드 자신의 원장 항목 → taxonomy products → 후보 · 계열은 taxonomy 정본만)
- 출처 우선순위(순서 · 대조본 처리에만): taxonomy items · products(정본) > procedure-profiles · problem-packages(큐레이션) > extracted.json · products.json(B15 대조본 · 같으면 same_as · 다르면 source_conflict 로 싣지 않음 · 정본에 없는 칸만 싣음)

### 사람 확인 자리 — 0

- 붙는 자리가 전부 이미 정해진 대응으로 풀린다(5단계 attach 3,964행 · taxonomy_products 557 · 7단계 항목 326 · 8단계 실버 435 · 계열 정본 302). 후보 여럿(5단계 「단위 시술 후보」 19항목 · 155행)은 8단계 aftercare 선례대로 **후보 전부 + candidates 표시**(고르지 않음 · SPEC §3.3.2)라 규칙. 충돌 606칸은 C9-1 로 규칙화
- 새로 세지 않은 원천 질문: 5단계에서 이미 열린 「원장님 문의」 알렉스필 1항목(7행) — 9단계도 붙이지 않음

### 골드 section(SPEC-005 §4-3 이름에 맞춤)

| 종류 | section | 새 section? |
|---|---|---|
| K1 효과 시작 · 지속 | recovery | 아니오 |
| K2 작용 원리 | method | 아니오 |
| K3 개요 · 설명 | overview | 아니오 |
| K4 적응증 | overview | 아니오(D9-2 대안 = indications) |
| K5 합병증 설명 | safety.management(새 · V-4) · 관리 외 칸은 safety.complications | **새 safety.management(D9-1)** |
| K6 반응 · 중증도 단계(값 사전) | global(값 사전) | 값 사전 · globals(D9-7) |
| K7 제품 메모 | products(제품 노드 overview) | 아니오 |
| K8 대안 | overview(고민 노드) | 아니오 |
| K9 관련 기법 | method | 아니오 |
| K10 최적화 중증도 단계 | evidence(이미) | 아니오 |
| K11 고민 상세 | overview(고민 노드) | 아니오 |

- legal_warning 2 는 disclosure(D9-8) · taxonomy 하위 분류 description 3 은 계열 overview + sub_family(D9-9) · 고민 쪽 alternatives 는 `cc:<CC>` 조건 표시(조건부 · D9-5)

## ⑤ 효과 — A 행 닫힘(행 단위 · 결정론)

판정: A 행의 원장 경로(evidence.path)가 위 대상 잎(또는 그 상위)이고 인용(정규화)이 그 잎 원문 안에 있으며 붙는 노드가 골드에 있으면 「예」 · R9-6(실버에 이미 있음)이면 「골드 빌드로」 · 그 밖 「아니오」.

### 2차 A(fail-triage2.json rows cls=A · rerun-v3 · 54행 · 문항 37) — 골드 빌드로(실버 변경 없음) 11 · 아니오 1 · 예 42

| 문항 | 케이스 | 항목 | 원장 경로 | 닫힘 | 규칙 · 자리 | 붙는 노드 |
|---|---|---|---|---|---|---|
| Q005 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q009 | case2 | accuracy | `taxonomy.modality[8].subcategories[3].items[0].extracted.mechanism` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:auto-40-1774737181584 |
| Q009 | case3 | accuracy | `taxonomy.modality[8].subcategories[3].items[0].extracted.onset_duration.duration` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:auto-40-1774737181584 |
| Q039 | case2 | accuracy | `products.skin_booster.products[3].note` | 예 | R9-2 · products.json → 단위 시술(taxonomy products · 5단계 S8) | unit_procedure:U5-009 |
| Q039 | case3 | accuracy | `products.skin_booster.products[3].note` | 예 | R9-2 · products.json → 단위 시술(taxonomy products · 5단계 S8) | unit_procedure:U5-009 |
| Q040 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q047 | case2 | accuracy | `complications.categories[1].complications[0].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M2 |
| Q047 | case3 | accuracy | `complications.categories[1].complications[0].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M2 |
| Q054 | case2 | accuracy | `extracted.M3.onset_duration.onset` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M3 |
| Q055 | case2 | on_topic | `extracted.M2.onset_duration.duration` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M2 |
| Q057 | case2 | accuracy | `extracted.M4.overview` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M4 |
| Q067 | case3 | on_topic | `extracted.M2.onset_duration.duration` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M2 |
| Q087 | case3 | accuracy | `extracted.M11.related_techniques[2]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M11 |
| Q087 | case3 | on_topic | `extracted.M12.mechanism` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 다름 · 인용은 정본 안에도 있음 | family:M12 |
| Q089 | case3 | accuracy | `extracted.M11.indications.primary[0]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M11 |
| Q089 | case3 | on_topic | `extracted.M11.indications.primary[0]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M11 |
| Q105 | case3 | accuracy | `pih-risk.procedures[6].name` | 아니오 | — · 대상 밖 |  |
| Q114 | case2 | accuracy | `extracted.M8.indications.primary[0]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M8 |
| Q117 | case2 | accuracy | `problem-packages.problems[5].complaints[1].alternatives[0]` | 예 | R9-5 · 고민 CC → 시술 이름 항목 → 단위 시술 | unit_procedure:U5-049 |
| Q118 | case2 | accuracy | `problem-packages.problems[5].complaints[6].cc_detail` | 예 | R9-5 · 고민 CC → 시술 이름 항목 → 단위 시술 | unit_procedure:U5-023 · unit_procedure:U5-024 · unit_procedure:U5-025 |
| Q118 | case2 | safety | `problem-packages.problems[5].complaints[7].cc_detail` | 예 | R9-5 · 고민 CC → 시술 이름 항목 → 단위 시술 | unit_procedure:U5-018 · unit_procedure:U5-019 · unit_procedure:U5-040 … |
| Q123 | case3 | accuracy | `extracted.M8.indications.primary[1]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M8 |
| Q133 | case3 | on_topic | `extracted.M2.indications.primary[2]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M2 |
| Q140 | case3 | on_topic | `complications.categories[4].complications[1].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M8 |
| Q162 | case2 | on_topic | `extracted.M15.mechanism` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q162 | case3 | accuracy | `extracted.M15.onset_duration.onset` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q167 | case2 | accuracy | `complications.categories[8].complications[2].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q167 | case3 | accuracy | `complications.categories[8].complications[2].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q168 | case2 | accuracy | `extracted.M15.indications.primary[1]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q168 | case2 | on_topic | `extracted.M15.overview` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q168 | case3 | accuracy | `extracted.M15.indications.primary[1]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q169 | case2 | accuracy | `complications.categories[8].complications[1].prevention` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q171 | case2 | accuracy | `complications.categories[8].complications[1].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q172 | case2 | accuracy | `complications.categories[8].complications[2].prevention` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q172 | case3 | accuracy | `complications.categories[8].complications[2].prevention` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q174 | case2 | on_topic | `complications.categories[8].complications[2].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q175 | case2 | accuracy | `taxonomy.modality[14].subcategories[0].items[45].extracted.mechanism` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-034 |
| Q175 | case3 | accuracy | `extracted.M15.indications.primary[1]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q178 | case3 | on_topic | `extracted.M7.overview` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M7 |
| Q179 | case2 | accuracy | `complications.categories[3].complications[7].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M7 |
| Q206 | case2 | accuracy | `post-procedure-timeline.reaction_levels.caution` | 예 | R9-7 · 값 사전(시맨틱 · B02) | scope:all |
| Q210 | case2 | accuracy | `taxonomy.modality[7].subcategories[3].items[3].extracted.indications.primary[0]` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:M8-4-3 |
| Q211 | case2 | accuracy | `taxonomy.modality[7].subcategories[0].items[7].extracted.indications.primary[0]` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-137 |
| Q214 | case2 | accuracy | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration` | 예 | R9-1 · 제품 × 계열 | product:M15-4-1 |
| Q214 | case2 | on_topic | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration.duration` | 예 | R9-1 · 제품 × 계열 | product:M15-4-1 |
| Q214 | case3 | accuracy | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration.onset` | 예 | R9-1 · 제품 × 계열 | product:M15-4-1 |
| Q218 | case2 | accuracy | `taxonomy.modality[8].subcategories[2].items[0].extracted.indications.primary` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:M9-3-1 |
| Q218 | case3 | on_topic | `taxonomy.modality[8].subcategories[2].items[0].extracted.indications.primary` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:M9-3-1 |
| Q221 | case3 | on_topic | `extracted.M7.onset_duration.duration` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M7 |
| Q230 | case2 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q230 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q231 | case2 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.onset` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q232 | case2 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q232 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |

### rerun-v5a case3 A(b202611011627-a76c8e · 판정 실패 200 중 gold_match 무히트 30 · 유효 29) — 골드 빌드로(실버 변경 없음) 6 · 아니오 4 · 예 20

| 문항 | 케이스 | 항목 | 원장 경로 | 닫힘 | 규칙 · 자리 | 붙는 노드 |
|---|---|---|---|---|---|---|
| Q003 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[7].extracted.indications.primary[0]` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-016 |
| Q009 | case3 | accuracy | `taxonomy.modality[8].subcategories[3].items[0].extracted.mechanism` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:auto-40-1774737181584 |
| Q015 | case3 | accuracy | `extracted.M9.onset_duration.duration` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M9 |
| Q035 | case3 | accuracy | `complications.categories[0].complications[1].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M1 |
| Q036 | case3 | accuracy | `post-procedure-timeline.timelines[0].phases[1].period` | 아니오 | — · 라벨 · 메타 칸(설명 사실 아님) |  |
| Q039 | case3 | accuracy | `products.skin_booster.products[3].note` | 예 | R9-2 · products.json → 단위 시술(taxonomy products · 5단계 S8) | unit_procedure:U5-009 |
| Q040 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q043 | case3 | accuracy | `extracted.M7.overview` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M7 |
| Q046 | case3 | accuracy | `complications.categories[1].complications[2].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M2 |
| Q047 | case3 | on_topic | `complications.categories[1].complications[0].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M2 |
| Q050 | case3 | accuracy | `complications.categories[1].complications[6].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M2 |
| Q054 | case3 | on_topic | `extracted.M3.onset_duration.onset` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M3 |
| Q075 | case3 | accuracy | `extracted.M9.onset_duration.onset` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M9 |
| Q087 | case3 | on_topic | `extracted.M11.related_techniques[2]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M11 |
| Q107 | case3 | accuracy | `pih-risk.description` | 아니오 | — · 라벨 · 메타 칸(설명 사실 아님) |  |
| Q133 | case3 | accuracy | `extracted.M2.indications.primary[2]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M2 |
| Q162 | case3 | on_topic | `extracted.M15.mechanism` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q165 | case3 | on_topic | `post-procedure-timeline.timelines[9].phases[3].label` | 아니오 | — · 라벨 · 메타 칸(설명 사실 아님) |  |
| Q168 | case3 | accuracy | `extracted.M15.indications.primary[1]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q171 | case3 | accuracy | `complications.categories[8].complications[1].management` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q172 | case3 | safety | `complications.categories[8].complications[2].prevention` | 골드 빌드로(실버 변경 없음) | R9-6 · 8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4) | family:M15 |
| Q175 | case3 | accuracy | `extracted.M15.indications.primary[1]` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M15 |
| Q178 | case3 | on_topic | `extracted.M2.indications` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M2 |
| Q214 | case3 | accuracy | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration.onset` | 예 | R9-1 · 제품 × 계열 | product:M15-4-1 |
| Q216 | case3 | accuracy | `extracted.M4.overview` | 예 | R9-3 · 계열(extracted.json 대조본) · taxonomy 정본과 같음 | family:M4 |
| Q218 | case3 | accuracy | `taxonomy.modality[8].subcategories[2].items[0].extracted.indications.primary` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:M9-3-1 |
| Q219 | case3 | accuracy | `procedure-profiles.profiles[2]` | 아니오 | — · 라벨 · 메타 칸(설명 사실 아님) |  |
| Q222 | case3 | accuracy | `taxonomy.modality[8].subcategories[1].items[2].extracted.mechanism` | 예 | R9-1 · 제품 × 계열 × 키 하위 | product:M9-2-5 |
| Q231 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |
| Q232 | case3 | accuracy | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 예 | R9-1 · 단위 시술 | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 |

- v5a 셈 차: 발주서는 「골드에 없음 27」 — 이 조사는 같은 배치의 판정 실패 200 을 recheck2 `gold_match`(정규화 · 포함 · 8자)로 다시 대 **30**(유효 29 · invalid 1 = Q219). 27 의 셈 식 출처가 없어 30 으로 적는다(아직 안 정한 것)
- 못 닫는 행: 2차 Q105(pih-risk procedures[].name — 시술 이름 라벨) · v5a Q036 · Q165(경과표 period · label) · Q107(pih-risk.description 파일 설명) · Q219(invalid · 운영 정보 needsAnesthesia) — 설명 사실이 아님(라벨 · 메타) · 골드 빌드 몫으로 남김
- 2차 A 를 칸별로: onset_duration 16 · indications 12 · management 8 · mechanism 4 · overview 3 · prevention 3 · note 2 · cc_detail 2 · alternatives · related_techniques · reaction_levels 각 1 · 기타 1 / v5a: onset_duration 7 · indications 6 · management 5 · mechanism 3 · overview 2 · note · prevention · related_techniques 각 1 · 기타 4

## ⑥ 아직 안 정한 것

- **D9-1** 합병증 · 부작용 관리 · 예방(management · prevention)을 골드 어느 section 으로 — 추천: 새 section `safety.management`
- **D9-2** 적응증(indications.primary · secondary · extended · 2,267행)을 어느 section 으로 — 추천: overview
- **D9-3** 같은 노드 · 같은 칸 다른 값 606칸(단위 시술 334 · 제품 원장↔taxonomy products 186 · 제품 원장 여럿 79 · 계열 7) — 예 U5-009 지속 「1개월 후 완전한 효과 발현」 vs 「3-4개월」 — 추천: 전부 싣기 + multi_source
- **D9-4** extracted.json 이 taxonomy 정본과 다른 7칸(계열 mechanism 4 · overview 2 · indications.extended 1) — 추천: 싣지 않음
- **D9-5** 쁘띠(P1) 시술 이름 CC 의 alternatives · cc_detail 을 단위 시술에 붙여도 되나(198 + 95행) — 추천: 단위 시술 + cc 조건
- **D9-6** 5단계 「원문 보관」 원장 항목 37개의 설명 키(320행) — 추천: 붙이지 않음
- **D9-7** 값 사전 8(반응 단계 4 · 중증도 4) — 추천: 시맨틱 값 사전 + 골드 globals(G16 과 같은 자리)
- **D9-8** 제품 legal_warning 2(ASCE+ · EXOSOME SKIN) section — 추천: disclosure
- **D9-9** taxonomy 하위 분류 description 3(M3 hADM · M16 DCA · 지방분해 혼합) — 추천: 계열 overview + sub_family 표시
- v5a A 수 — 이 조사 셈 30(유효 29 · gold_match 무히트) vs 발주서 27: 27 의 셈 식 출처 없음(코디 확인)
- 골드 빌드 쪽 칸(이 단계 밖): 경과표 phases[].period · label(Q036 · Q165) · pih-risk procedures[].name(Q105) · pih-risk.description(Q107) — 라벨 · 메타 칸이라 설명 사실 아님 · 닫지 않음으로 둠
- SPEC-005 §4-3 V-4 문구 「severity_levels 의 sequence · rationale · expected_sessions 는 실버에 칸이 없다」 — 이 조사에서 골드 fact 덮임 24/24(7단계 조합) · 스펙 정정 필요(9단계 몫 아님)

## 알려진 한계

- 「골드 fact 있음」 판정은 문자열 포함(8자) — 짧은 값(「3-5일」 등 8자 미만)은 같은 문자열일 때만 있음으로 셈 · 우연 포함이 있을 수 있어 「골드 있음」 1,481 은 상한 쪽
- 붙는 노드 셈은 골드 export(b031371c) 노드 기준 — 1단계 제품 행이 없는 taxonomy 제품(예 레티보 M1-P-10)은 붙음 0 으로 셈
- A 닫힘은 「골드에 fact 로 들어가 그 노드에 붙는다」까지 — 허브 응답 · 걸음이 그 section 을 가져오는지는 SPEC-005/006 몫
