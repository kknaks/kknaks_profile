# 9단계 규칙 — 설명 사실

셈은 `step9-explanations.json summary`(2026-11-01 반영 판). 규칙이 바뀌면 셈이 바뀐다 — 여기 숫자는 그 판의 값이다.

## 종류(K)

| K | 이름 | 식(요약) | section |
|---|---|---|---|
| K1 | 효과 시작 · 지속 | `onset_duration.` | recovery |
| K2 | 작용 원리 | `extracted.mechanism` · `moa_summary` | method |
| K3 | 개요 · 설명 | `extracted.overview` · `items[].detail` · `subcategories[].description` | overview |
| K4 | 적응증 | `indications.`(contraindications 제외) | overview(D9-2) |
| K5 | 합병증 설명 | `complications…(management · prevention · …)` | safety.management(새 · D9-1) · safety.complications · safety.side_effects |
| K6 | 값 사전 | `reaction_levels` · `complications.severity_levels` | 시맨틱 value_dictionary · 골드 globals(D9-7) |
| K7 | 제품 메모 | `products[].(note · ingredient · material · legal_warning · type)` | overview · legal_warning = disclosure(D9-8) |
| K8 | 대안 | `alternatives[]` | overview(+ cc 조건) |
| K9 | 관련 기법 | `related_techniques[]` | method |
| K11 | 고민 상세 | `cc_detail` · 고민 항목 `detail` | overview |
| (K10) | 최적화 중증도 단계 | — | 대상 밖(7단계 조합에 이미 · 골드 24/24) |

## 붙이는 규칙

| 규칙 | 무엇 | 반영 판 레코드 |
|---|---|---|
| R9-1 | 원장 항목 extracted 설명 키 · detail → 5단계 `extracted[].attach` | 4,284 |
| R9-2 | taxonomy products · products.json(R9-2a 대조) → 5단계 `taxonomy_products` | 600 |
| R9-2b | products.json 이름이 taxonomy products 에 없음 → 원장 항목 이름이 전부 같은 제품일 때 그 제품(볼뉴머 → M9-2-3) | 1 |
| R9-3 | 계열 extracted = taxonomy 정본 · extracted.json 은 대조(D9-4) | 585 |
| R9-4 | procedure-profiles moa_summary → 계열 | 17 |
| R9-5 | 고민 쪽(alternatives · cc_detail · 고민 항목 detail) → 7단계 항목 · 시술 이름이면 단위 시술 + `cc:<CC>`(D9-5) | 357 |
| R9-5b | 시술 이름 항목인데 resolve 단위 시술 없음 · 계열만(R21) → 그 계열 | (R9-5 안 1) |
| R9-6 | 합병증 · 부작용 설명 → 8단계 실버 그대로 · section 표(`section_map` 435) | 레코드 없음 |
| R9-7 | 값 사전 → 시맨틱 · 골드 globals | 값 사전 8 |
| R9-8 | 하위 분류 description → 계열 overview + `sub_family:`(D9-9) | 3 |
| G9-1 | fact id = `{노드}#{section}#step9[{원천 경로}]` | — |

붙이지 않음(D9-6 · 고민 B09): 5단계 원문 보관(6단계 패키지 145 · 값 146 · 시술 아님 22 · 원장님 문의 7) · 고민 부위 · 시술 아님 항목 30.

## D9-3(같은 노드 · 같은 칸)

반영 판 node_slots 2,946 = 한 원천 2,317 · 같음 33 · **① 43 · ② 196 · ③ 357** · ② 처분 = 짧은 쪽 66 · 늦은 쪽 68 · 원천 우선순위 62 · alternatives 343.

- 군집: 같은 칸 레코드를 길이 내림 · 원천 순위 · 경로 순으로 놓고, 앞선 대표에 정규화 포함되면 그 대표에 접는다(same_as)
- ① 숫자 같음: 접은 뒤 대표가 여럿이어도 모든 대표의 숫자 집합이 같으면 가장 긴 대표 하나
- ②: 숫자 집합이 서로 다른 대표가 둘 이상 — 숫자 없는 대표는 함께 싣는다(multi_source)
- 기간 읽기: `N(-|~)M 단위`(분 · 시간 · 일 · 주 · 개월 · 달 · 년) → 일 [하한, 상한] · 한 문장에 여럿이면 전체 [최소, 최대] · 0일 낱말
- 원천 우선순위: 그 노드 자신의 원장 항목(0) → taxonomy products(1) → 후보(2) → 계열 · 프로파일(3) → 고민(4) → 경로 정렬
- 조사 판(606)과 반영 판(①+②+③ 596)의 차: 조사는 대조본(extracted.json 7칸 · products.json)도 원천으로 셌고, 반영은 대조본을 same_as · source_conflict 로 먼저 뺀다

## 대조본

| 규칙 | 원천 | 같음(same_as) | 다름(source_conflict · 싣지 않음) |
|---|---|---|---|
| D9-4 | extracted.json 계열 칸 | 286 | 7 |
| R9-2a | products.json 칸(taxonomy products 에 같은 칸 있음) | 38 | 5 |
