# 골드 설계 조사 — 규칙 적용 그래프 · 허브 도구 · 의도별 탐색 · 패널 응답

정본 데이터 `gold-research.json` · 읽기 전용 조사(실버 · 시맨틱 · 브론즈 수정 없음) · 계산은 지금 실버 json 으로 직접(추정 · 가상 문장 없음) · 2026-10-30

## 0. 요약

골드 규칙 **17** · 의도 **12** · 도구 **9** · 탐색 경로 **11** · 펼친 뒤 엣지 **24,392**(저장 3,044 → 단위 시술 수준) · 결정 묶음 **6**(결정 18) · 사용자 판단 **3**

- 규모: 정본 노드 1,071 · 저장 엣지 3,044(브리프의 1,145 · 5천은 연결 구조 페이지 기준 1,112 · 4,391). 펼치면 관계가 대부분 — 주장 395 → 단위 시술 쌍 14,942행(서로 다른 쌍 4,794). 그래도 메모리 dict 조회로 추천 4 질의 0.54ms
- 큰 발견 5: ① semantic I1 이 「추천 계열만」도 펼치라고 적었는데 10-29 W2 와 충돌(펼치면 970행) → 안 펼침 ② 부작용 덮어쓰기 값이 실버에 없음(키만) — 브론즈에 있음 ③ combo_component 셈이 비교 members · upgrade 119 를 빠뜨림 ④ 사전 완전 일치로 「턱선 처짐」 · 「Sofwave」 · 「볼루마」 · 미라쥬 「눈물고랑 · 밝기 · 피지」가 안 잡힘 ⑤ 샘플의 턱선 처짐 → 소프웨이브는 「얼굴 전체」 층을 같이 낼 때만 나옴(U-1)
- 샘플 대조: 8단계 「시술 후 2주 사우나」는 지금 원천에 없음 — 원천은 M9 「당일 사우나 · 격한 운동 피하기」. 카드는 「당일」로 나가고 Claude 는 카드 밖 말을 못 한다(D-16)

## 1. 샘플 11단계 → 허브 호출

| 단계 | 장면 | 허브 |
|---|---|---|
| 1 | 상담 시작 · 빈 화면 | 없음 |
| 2 | 미라쥬 결과 도착(7 영역) | 영역 → site · concern id(연결 층 대응 · D-17) |
| 3 | 첫 고민 · 이마 주름 | resolve → I-01 recommend(P2 × 이마) |
| 4 | 두 번째 고민 · 팔자 | I-01(P2 × 팔자) |
| 5 | 세 번째 고민 · 턱선 처짐 | resolve 낱말 나눔 → I-01(P3 × 턱선) |
| 6 | 추천 · 소프웨이브 | I-01 카드(U-1 에 따라) + 연결 층 가격 |
| 7 | 시술 방법 안내 | I-02 procedure_card(method) |
| 8 | 주의 안내 · 사우나 | I-03 aftercare — 원천 「당일」 |
| 9 | 팔자 추천 · 필러 2cc | I-10 dose · products — 볼루마 품목 없음 |
| 10 | 결제 조합 A·B·C | I-07 pair_check(조합 A 쌍 3) · I-06 비교(A ↔ B) · 가격 연결 층 |
| 11 | 조합 A 확정 | 없음(앱 기록) |
| 공통 | 이전 방문 · 문진(통증 민감 · 6주 전 보톡스 · 같은 날 가능) | I-08 · I-09 |

화면 3칸(피부 분석 얼굴 지도 · 상담 내역 고민 카드 · 추천 · 결제 조합)과 아래 줄 「공통 · 이전 방문 · 문진」. 패널이 바뀌는 때 = 고민이 생김(3~5) · 추천(6) · 설명 · 주의 추가(7 · 8) · 용량(9) · 조합(10)

## 2. 골드 그래프 규칙

| id | 이름 | 규칙 | 셈(지금 데이터) | 근거 | 메모 |
|---|---|---|---|---|---|
| G1 | 정본 id 로 바꿔 싣기 | 실버 id → 정본 id(B6 · semantic ids.map 1,071). 단위 시술 · 제품 id 는 안정 키 — 연결 층이 여기에 붙는다 | 노드 1,071(13종) | semantic §5 |  |
| G2 | 계열 → 단위 시술 펼치기(I1) | 관계 · 확인 조건 · 합병증 · 근거 문장 · 부작용 · 위험지대 · 피함의 계열 끝을 key.family 가 그 계열인 단위 시술 전부로 펼쳐 단위 시술 수준 행으로 싣는다(행마다 how = 계열에서 상속) | 관계 단위 쌍 행 15,103(서로 다른 쌍 4,794) · 확인 조건 3,373(단위 × 조건 서로 다름 1,600) · 합병증 285(실버 units_inherit 285 와 같음) · 근거 문장 1,215 · 부작용 612 | semantic I1 |  |
| G3 | 추천(treats) 「계열만」은 펼치지 않는다 | 고민 → 계열만 81 은 계열 엣지 그대로 + 표시(이 부위 단위 시술 없음 · 앵커 부위 없음 등). 펼치면 970행 — 10-29 W2(「그 부위 단위 시술 없음 → 계열 후보 전부」 폐기)와 정면 충돌 | 계열만 81(앵커 부위 없음 49 · no_unit_at_site 13 · ambiguous 11 · unresolved 5 · concern_without_site 2 · not_procedure 1) · 펼쳤다면 970 | _RESUME 10-29 W2 · semantic I5 「없으면 계열만 · 단위 시술 후보 붙이지 않음」 | semantic I1 문구 「추천 계열만」이 W2 와 어긋남 → SPEC-005 에서 I1 대상에서 뺀다 |
| G4 | 하위 계열 · 기법 조건 끝(I2 · I3) | 8단계가 이미 units 칸에 풀어 둔 값을 그대로 쓴다(재계산 안 함). 키에 그 하위 없는 계열은 「후보」 표시 | 하위 끝 42 · 기법 끝 25 — 전부 units 칸 있음(1행 예외: 「조건에 맞는 단위 시술 없음 — 계열에서 멈춤」) | semantic I2 · I3 |  |
| G5 | 제품 → 단위 시술(I4) | 5단계 product_link 규칙(같은 계열 주 · 보조 · 하위 일치 · 기법 호환 F1 · 도포 가드)을 골드 빌드에서 다시 계산하고 5단계 기록(inherited_candidates)과 같은지 assert | 상속 후보 1,364(추천 가능 제품 1,016) + 저장 44 · 기법 호환을 빼면 2,666 → 기법 호환이 1,302행을 거른다 | semantic I4 · step5 rules.product_link |  |
| G6 | 부위 — 저장은 7단계 값 · 질의 때 층 거르기 | treats 엣지의 부위 판정(R21 · R22 · R23 · R25)은 7단계가 이미 엣지에 적용했으므로 다시 안 한다. 질의에 부위가 오면 같은 R21 층 규칙으로 거른다(U-1 판단 대상) | site_check 부위 안 109 · 상위 얼굴 전체 35 · 상위 바디 2 · 앵커 부위 없음 268 · 계열만 13 | semantic I5 |  |
| G7 | 끝점 묶음(I6) | candidates[] 는 OR — 펼친 행마다 「후보」 표시. 고르지 않는다(10-27 W-1) | 끝점 단위 시술 후보 112 · 계열 묶음 2 | semantic I6 |  |
| G8 | 조건부 제외(I7) | default_apply false 는 펼치되 conditional 표시 → 기본 응답 · 기본 탐색에서 뺀다(조회 옵션 include_conditional 로만) | 관계 192행 · 피함 3(AV8-001 · 002 · 004 — 기미 × 고출력 레이저 · 각 31 단위) · 확인 조건 1 | semantic I7 |  |
| G9 | 부작용 덮어쓰기(I8) | 계열 부작용(safety.side_effects 72)을 단위 시술로 펼치고, 아래 수준 safety.common 값이 있으면 그 값으로 바꾼다 — 우선순위: 제품 × 계열(× 키 하위) > 단위 시술 > 계열. 합병증 노드는 덮지 않는다. 계열 값은 근거(override_of)로 남긴다 | 계열 → 단위 612행 · 덮을 값: 제품 × 계열 207 + 제품 × 계열 × 하위 111 · 단위 시술 147 + 후보 19 · taxonomy products 59 | semantic I8 · U2 · B1 | 실버 step5 extracted[] 에는 keys 만 있고 문장 값이 없다 — 값은 브론즈 extracted.json · taxonomy 에 있음(실물 확인). 적재가 실버 attach 표대로 브론즈 원문을 싣는다(10-27 「extracted 를 노드 속성으로」 결정과 같은 꼴) |
| G10 | 해당 없음 ≠ gap(I9) | 안전 칸마다 상태 3값 = 값 있음 · 해당 없음(원천) · 정보 없음(gap). 「없음 = 안전」으로 말하지 않게 상태를 응답에 그대로 | PIH 해당 없음 77 · PIH gap 63 · 합병증 gap 계열 12(단위 36) · 부작용 gap 계열 10(단위 26) · 중대 반응 없음(원천) 1 | semantic I9 |  |
| G11 | 경과 타임라인 · PIH · 운영 · 계열 원문 붙는 수준 | 원천이 가리킨 수준에 붙여 아래로 상속(엣지 아님 · 속성). 하위 계열에 붙은 것은 그 하위 단위 시술만 | 타임라인 10 → 단위 52행(hifu-rf 는 HIFU · RF 6 단위만 — SUPERB · 마이크로웨이브 단위에는 안 붙음) · PIH 26 · 계열 원문 27 | semantic I8 |  |
| G12 | 기본 응답 거르기 | 뺀다: 제품 recommendable false · 패키지 recommendable false · 병원 시그니처 · 영업 문구 · conditional · 시술 아님 · 못 풂. gate 3값(자동(완전 일치) · 자동(규칙) · 결정)은 전부 통과 — 「미확인」은 상태가 아니라 표시(question · weak · gap)라 값은 내고 표시를 붙인다 | 제품 추천 제외 118(활성 354 중) · 패키지 제외 2 · 영업 문구 24 · gate 로 빠지는 것 0(지금 gate 값 3종 전부 승인 · 자동) | 10-27 W-1 · semantic §6 · 6-3 |  |
| G13 | 안전 정보는 늘 낸다 | 시술이 응답에 나오면 거르기와 무관하게 같이 낸다: 합병증 · 부작용 · 확인 조건(전 등급) · 위험지대 · 금기류 관계(간격 금기 13 · 조합 금기 3 · 같은 날 불가 7 · 대체) · 피함(조건부 아닌 것) · 응급 징후 · 필수 고지 · gap 상태 | 단위 시술당 확인 조건 중앙 12 · 최대 20 · 전역 조건 16 | 10-26 경계 「안전 엣지는 시술 노드와 항상 같이」 |  |
| G14 | 충돌 — 고르지 않고 쌍 요약 | 단위 쌍 하나에 걸린 주장들의 same_day · days · first 값 집합을 결정론으로 모아 「값이 하나면 그 값 · 여럿이면 충돌 + 양쪽 주장 id」. 자동으로 고르지 않는다(D-13b) | 예: 이마 보톡스 ↔ 팔자 필러 주장 13(conflict 11) — same_day {true · false · null} · first {a · b} | semantic 표시 conflict 104 · 10-29 6단계 |  |
| G15 | 하위 조건별 값(by_sub_condition) | 겉 칸이 비면 options[] 를 그대로 전달 — 쌍 요약도 option 별로. 한 값으로 접지 않는다 | 주장 2 | reading_contract |  |
| G16 | 와일드카드 · 전역 조건은 펼치지 않는다 | 「모든 시술」 관계 1(R8-0148)과 공통 확인 조건 13주장(조건 16 · 22행)은 전역 행 하나로 두고 모든 시술 응답에 붙인다(162 배 행 안 만듦) | 전역 관계 1 · 전역 조건 22행 — 펼쳤다면 관계 161 · 조건 3,564 | semantic I6 · 끝점 「모든 시술」 |  |
| G17 | 추천 조합 구성 — members · upgrade 도 엣지로 | combo_component 를 components 만이 아니라 비교 members · 연령 플랜 upgrade 까지 세운다(R22 가 이미 이 칸들을 거름) | components 462 + 비교 members 107 + upgrade 12 = 581 | step7 combos · R22 | semantic edge_kinds combo_component 셈 462 는 components 만 — 119행 빠짐(SPEC-005 에서 정본 보강 · 실버 수정 아님) |

### 2-1. 펼친 뒤 셈

| 엣지 | 행 |
|---|---|
| product_family | 370 |
| key_family | 162 |
| key_site | 131 |
| key_technique | 162 |
| child_of | 104 |
| concern_related | 4 |
| family_technique | 34 |
| line_item | 5 |
| contains | 71 |
| concern_site | 23 |
| anchors_combo | 94 |
| combo_component | 462 |
| treats(단위 시술 행 · 계열만은 계열 엣지 그대로) | 769 |
| uses_product(저장 + I4 상속 후보) | 1,408 |
| procedure_relation(단위 시술 쌍 행 · 와일드카드 제외) | 14,942 |
| procedure_relation 와일드카드(전역 1행 유지) | 1 |
| requires_check(단위 시술 × 조건 행) | 3,373 |
| requires_check 전역(모든 시술 · 응답마다 붙임) | 22 |
| has_complication(단위 시술) | 285 |
| has_statement(단위 시술) | 1,215 |
| side_effect(단위 시술 · 속성 엣지) | 612 |
| site_caution(단위 시술) | 17 |
| concern_avoid(단위 시술 · 조건부 포함 안 함) | 2 |
| cites | 124 |
| **합** | **24,392** |

- 계열 1홉 안(합병증 · 근거 문장 · 부작용을 계열에): 22,506
- 관계 펼침 큰 주장: R8-0239 2,184행 「열 시술 후 주입 시술 순서 준수 필수. 울쎄라의 SM…」 · R8-0311 775행 「레이저 + 미백주사…」 · R8-0313 775행 「레이저 + 미백주사…」 · R8-0003 527행 「M1↔M8 비박리·비박리 프락셔널: 같은 날 가능(레이…」
- 단위 시술 관계 이웃 중앙 70 · 최대 161 · 확인 조건 단위당 중앙 12 · 최대 20
- 일관성: 합병증 펼친 행 285 = 실버 units_inherit 285 (같음)

## 3. 의도

| id | 의도 | 슬롯 | 샘플 근거 | 예시 질문 | 경로 | 도구 |
|---|---|---|---|---|---|---|
| I-01 | 고민 → 추천 | concern[] · site? · region? | 3·4·5단계 「이마 주름」 「팔자」 「턱선 처짐」 · 6단계 소프웨이브 추천 | 이마 주름이 신경 쓰여요 / 턱선이 처졌어요 | P-01 | recommend |
| I-02 | 시술 설명 | procedure(unit\|product\|family) | 7단계 「초음파로 피부 속 깊은 층을 데워 … 하안면 약 30분」 | 소프웨이브는 어떻게 하는 거예요? | P-02 | procedure_card |
| I-03 | 주의 · 사후관리 | procedure · topic?(aftercare\|timeline\|emergency) | 8단계 「시술 후 2주 사우나 피하기」 | 끝나고 사우나 가도 돼요? | P-03 | procedure_card(sections=aftercare,timeline,emergency) |
| I-04 | 부작용 · 합병증 | procedure | (샘플 카드 「주의」 칸) | 멍 들어요? / 부작용 있어요? | P-04 | procedure_card(sections=safety) |
| I-05 | 회복 · 효과 기간 | procedure | 6단계 카드 「當日恢復 · 持續 12 個月」 | 바로 출근해도 돼요? / 얼마나 가요? | P-05 | procedure_card(sections=recovery) |
| I-06 | 비교 | procedures[2+] \| purpose | 10단계 조합 B 「Ulthera」 ↔ A 「Sofwave」 | 울쎄라랑 소프웨이브 뭐가 달라요? | P-06 | compare |
| I-07 | 같이 · 순서 · 간격 | procedures[2+] · same_day? | 10단계 조합 A 「Sofwave + Voluma 2cc + 이마 보톡스」 — 같은 날 · 순서 | 오늘 셋 다 같이 해도 돼요? / 뭐부터 해요? | P-07 | pair_check |
| I-08 | 이전 시술 뒤 가능? | procedure · prior_procedure · elapsed_days | 공통 칸 「六週前施打過肉毒，可同日進行」(6주 전 보톡스) | 6주 전에 보톡스 맞았는데 괜찮아요? | P-08 | pair_check(prior=…) |
| I-09 | 나한테 해도 되나(확인 조건) | procedure · person_conditions[] | 공통 칸 「문진 · 통증에 민감」 | 임신 준비 중인데요 / 켈로이드 체질이에요 | P-09 | check_conditions |
| I-10 | 용량 · 회차 · 제품 | procedure · product? · amount? | 9단계 「필러 2cc 추천 · 고객 1cc 희망」 | 필러 몇 cc 맞아요? / 볼루마로 해 주세요 | P-10 | procedure_card(sections=dose,products) |
| I-11 | 추천 조합 · 패키지 구성 | concern\|purpose\|procedure | 10단계 결제 조합 A·B·C(구성 = 허브 · 가격 = 연결 층) | 같이 하면 좋은 거 있어요? | P-11 | combos |
| I-12 | 가격 | procedure\|product | 6단계 「NT$28,000 · 活動價」 · 10단계 조합 가격 | 얼마예요? | — (연결 층) | 연결 층(KOS 어댑터) — 허브는 단위 시술 · 제품 id 만 |

## 4. 허브 도구(REST · MCP 같은 코어 · LLM 없음 · 결정론)

| id | 이름 | 꼴 | 입력 | 출력 | 규칙 | 실측 |
|---|---|---|---|---|---|---|
| T1 | resolve | REST GET /gold/resolve · MCP resolve | {"text": "str", "tokens?": "[str]", "kinds?": "[node kind]"} | {"matches": [{"span": "str", "mode": "하나\|전부\|후보", "candidates": [{"id": "unit_procedure:U5-140", "kind": "str", "name": "str", "reasons": ["str"], "match": "완전\|낱말\|접두", "flags": ["candidates", "weak", "…"]}]}], "unmatched": ["str"]} | norm 완전 일치(사전 1,962) → 띄어쓰기로 나눠 낱말마다 → 접두 일치(「부분 일치」 표시). 후보 여럿이면 전부(10-27). LLM 없음 | 「턱선 처짐」 사전 없음 → 「턱선」 site.jawline + 「처짐」 P3 · P3-1~3(전부) · 「Sofwave」 완전 일치 없음 → 접두 「Sofwave System」 · 「주름」 = 고민 P2 + 단위 5(후보) |
| T2 | recommend | REST GET /gold/recommend · MCP | {"concerns": "[id]", "site?": "id", "region?": "id", "include_conditional?": "bool=false", "include_not_recommended?": "bool=false"} | panel 응답(§5) — areas[] · cards[] · family_only[] · flags · facts[] | P-01 | 턱선 처짐 0.5ms 안팎(4 질의 0.54ms) |
| T3 | procedure_card | REST GET /gold/procedures/{id} · MCP | {"id": "unit\|product\|family", "product?": "id", "sections?": "[overview,method,recovery,aftercare,timeline,emergency,safety,checks,dose,products,evidence]"} | card(§5) — 칸마다 facts[id, text, flags, state] | P-02~P-05 · P-10 | slim 중앙 2.6KB · 최대 5.0KB / 원문 포함 full 중앙 12.8KB · 최대 18.4KB |
| T4 | pair_check | REST POST /gold/pairs · MCP | {"procedures": "[id 2+]", "same_day?": "bool", "prior?": {"procedure": "id", "elapsed_days": "int"}} | {"pairs": [{"a": "id", "b": "id", "summary": {"same_day": "[값]", "days": "[[하한,상한]]", "first": "[a\|b]", "state": "일치\|충돌\|정보 없음"}, "prior_ok?": "bool\|null", "claims": [{"id": "R8-…", "kind": "str", "interval": "{}", "flags": []}]}]} | P-07 · P-08 — 쌍 C(n,2) 마다 · 충돌은 값 집합으로 | 보톡스↔소프웨이브 주장 6(days [14,14] · [0,14] · same_day true 1 · conflict 1) · 필러↔소프웨이브 6 · 보톡스↔필러 13(conflict 11) |
| T5 | check_conditions | REST GET /gold/procedures/{id}/checks · MCP | {"id": "unit\|product", "conditions?": "[C-…]"} | {"checks": [{"condition": "C-…", "name": "str", "grade3": "금기\|주의\|확인만\|확인만(고지)", "claims": ["K8-…"], "scope": "unit\|family\|global"}], "global": "[…]"} | P-09 | M9 계열 확인 조건 16(주장 19 — 금기 13 · 확인만 3 · 주의 3) + 전역 16 |
| T6 | compare | REST POST /gold/compare · MCP | {"procedures": "[id 2+]"} | {"rows": "[칸 × 시술 — 키 차이(계열 · 하위 · 부위 · 기법) · ops · 회복 · 지속 · 안전 셈]", "source_comparisons": "[비교 combo members attrs_text]", "alternatives": "[대체(택 1) 주장]"} | P-06 | 울쎄라(U5-102)↔소프웨이브(U5-140) 관계 주장 0 · 「리프팅 비교」 members 에 소프웨이브 없음 → 키 차이(HIFU ↔ SUPERB 초음파)만 |
| T7 | combos | REST GET /gold/combos · MCP | {"concern?": "id", "purpose?": "id", "procedure?": "id", "include_sales_copy?": "bool=false"} | {"combos": "[추천 조합 · 패키지 — 구성 단위 시술 · tier · 출처 · 표시]"} | P-11 | 조합 79 · 패키지 24(추천 22) |
| T8 | neighbors | REST GET /gold/nodes/{id}/neighbors · MCP | {"id": "id", "edge_kinds?": "[kind]", "depth?": "int ≤ 2", "limit?": "int=50", "include_conditional?": "bool"} | {"nodes": [], "edges": [], "truncated": "bool", "counts_by_kind": {}} | 여러 홉 범용 — 정해 둔 경로 밖 질문 | 단위 시술 관계 이웃 중앙 70 · 최대 161 → limit 필수 |
| T9 | vocab | REST GET /gold/vocab · MCP | {"kinds?": "[concern\|site\|purpose\|check_condition\|intent]"} | {"trees": "고민 트리 · 부위 트리 · 목적 · 확인 조건 · 의도 · 슬롯 enum"} | Jev 슬롯 선택지(10-26 「Jev 선택지는 Hub 가 노드 목록 · 스키마로」) | 고민 57 · 부위 53 · 목적 13 · 확인 조건 53 |

## 5. 의도별 탐색 경로(지금 데이터로 따라간 값)

| id | 의도 | 경로 | 지금 데이터 |
|---|---|---|---|
| P-01 | I-01 | resolve(고민 · 부위) → 고민 + 하위 고민(트리) · 부위가 있으면 부위 아래 항목 고민도 → treats(단위 시술 행 + 계열만) → 부위 층 거르기(R21: 부위 · 하위 → 상위(묶음 통과) → 영역 「전체」 노드) → 단위 시술마다 G13 안전 묶음 · 쓰는 제품(I4) · 추천 조합 앵커 | 이마 주름(P2 × 이마) → U5-001 이마 보톡스(원천 5행) · U5-086 이마 필러 / 팔자 → U5-082 팔자 필러 / 턱선 처짐(P3 × 턱선) → U5-103 턱선 HIFU(6) · U5-122 턱선 실리프팅(5) · U5-016 턱선 보톡스(1). 얼굴 전체 층(U-1)까지 넣으면 턱선 처짐 +8(U5-140 소프웨이브 포함). 부위 없는 「처짐」 → 27 단위(바디 5 포함) → D-12 |
| P-02 | I-02 | resolve(시술) → 후보 여럿이면 후보 전부 반환(되묻기) → 단위 시술 → 키(계열 · 하위 · 부위 · 기법) · ops(마취 · 소요) · 계열 근거 문장(moa · effects, 환자용 ko) · 계열 원문 「환자 설명 가이드」 · 쓰는 제품 extracted(overview · mechanism) | 소프웨이브 → product:auto-40 · U5-140(후보 2) · ops 30~60분 · 연고마취 또는 없음 · M9 근거 문장 moa 3 · effects 1 · 환자 설명 「초음파나 고주파 에너지로 피부 깊은 층을 자극」 |
| P-03 | I-03 | 단위 시술 → 계열(+하위) 원문 사후관리 · 경과 타임라인(G11 붙는 수준) · 응급 징후 · 필수 고지 | U5-140 → M9 사후관리 「당일 사우나 · 격한 운동 피하기」(procedure-profiles) · 타임라인 hifu-rf 는 HIFU · RF 단위에만 → U5-140 타임라인 없음(정보 없음). 샘플 8단계 「2주 사우나」는 지금 원천에 없음 → 카드는 「당일」 |
| P-04 | I-04 | 단위 시술 → 부작용(G9 덮어쓰기) · 합병증(계열) · PIH(붙는 수준) · gap 상태(G10) | U5-140 → 부작용 4(홍반 · 부종 · 통증·열감 · 일시적 감각이상) · 합병증 2(화상 severe · PIH moderate) · PIH gap |
| P-05 | I-05 | 단위 시술 → 계열 원문 환자 설명(downtime · duration_simple) · extracted onset_duration · 비교 members attrs_text(downtime · duration) | M9 「거의 없음 - 약간의 붉은기와 붓기 수시간~1일」 · 「약 6-12개월 지속」 |
| P-06 | I-06 | 시술 2+ → 키 칸 나란히 · ops · 회복 · 안전 셈 → 비교 combo members(같은 단위 시술이 든 것) attrs_text → 대체(택 1) 주장 | 울쎄라 U5-102 ↔ 소프웨이브 U5-140: 하위 HIFU ↔ SUPERB 초음파 · 같은 K05 · 관계 주장 0 · 「리프팅 비교」(RC-CP-lifting) 엔 울쎄라만 |
| P-07 | I-07 | 시술 n → 쌍 C(n,2) → 쌍마다 관계 주장(I1 펼친 행) → G14 쌍 요약(same_day · days · first) · G15 options · 금기류 먼저 | 조합 A(U5-140 · U5-082 · U5-001) 쌍 3: 보톡스↔소프웨이브 6 · 필러↔소프웨이브 6(M2↔M9 「4주 이상」 · 「필러 2주 후 리프팅」 conflict) · 보톡스↔필러 13(conflict 11) |
| P-08 | I-08 | 쌍(prior, 지금) → 간격 주장 days 하한 ≤ 경과일 → 충족 · same_day 는 경과 0 일 때만 · 순서(first)가 거꾸로면 표시 · C-PRIOR 확인 조건도 | 6주(42일) 전 보톡스 → 소프웨이브: days [14,14] · [0,14] 하한 14 ≤ 42 → 충족 · M9 확인 조건에 C-PRIOR(최근 · 이전 시술 이력) 있음 |
| P-09 | I-09 | 단위 시술 → requires_check(단위 + 계열 상속 + 제품) + 전역 → 사람 조건 낱말 → resolve(check_condition) → 등급 | U5-140 → 조건 16 + 전역 16 · 통증 민감은 확인 조건 노드 없음 → ops 마취(연고마취 또는 없음)로 |
| P-10 | I-10 | 단위 시술 → dose_range · step4 attrs · 쓰는 제품(I4) → 제품 5_spec(규격) · 라인 품목 | U5-082 팔자 필러 · 쥬비덤(M2-2-1) 라인 있음 · 「볼루마/Voluma」 품목 없음 → 허브 보강 후보 |
| P-11 | I-11 | 고민 · 목적 · 시술 → anchors_combo · combo_component(G17) · 패키지 contains → 영업 문구 빼고 | 조합 79 · 패키지 22(추천) |

## 6. 패널 응답 모양

### 6-1. 왼쪽 얼굴 지도

왼쪽 얼굴 지도 영역 = 3단계 부위 노드(얼굴 영역 33 = 묶음 5 + 가리킬 수 있는 28). 지도에는 단위 시술이 있는 부위 25 를 칠할 수 있다(얼굴 전체 44 단위는 영역 전체 표시)

| 미라쥬 영역(샘플) | 허브 id |
|---|---|
| 턱선 | site:site.jawline |
| 팔자 | site:site.nasolabial |
| 이마 | site:site.forehead |
| 눈물고랑 | 사전 없음(연결 층 대응) |
| 밝기 | 사전 없음(연결 층 대응) |
| 모공 | concern:P7 |
| 피지 | 사전 없음(연결 층 대응) |

### 6-2. 카드 칸

- 이름 · 키(무엇을 · 어디에 · 어떻게)
- 왜 추천(treats 원천 · 표시)
- 시술 방법(근거 문장 · 환자 설명)
- 회복 · 지속
- 주의(사후관리 · 타임라인 · 응급 징후)
- 부작용 · 합병증 · gap 상태
- 확인 조건(등급)
- 쓰는 제품(허가 상태)
- 연결 키(병원 상품은 연결 층이 붙임)

### 6-3. 응답 뼈대(앱 · Claude 공통)

```json
{
 "request": {
  "intent": "I-01",
  "slots": {},
  "resolved": "[resolve 결과 그대로]"
 },
 "areas": [
  {
   "site": "site:site.jawline",
   "name": "턱선",
   "layer": "부위 안|상위|영역 전체",
   "concerns": [
    "concern:auto-88-…"
   ],
   "card_ids": [
    "unit_procedure:U5-103"
   ]
  }
 ],
 "cards": [
  {
   "id": "unit_procedure:U5-103",
   "name": "턱선 HIFU 리프팅",
   "key": {
    "family": "family:M9",
    "sub_family": "HIFU",
    "site": "site:site.jawline",
    "technique": "technique:K05"
   },
   "why": [
    {
     "edge": "treats",
     "from": "concern:auto-88-…",
     "source": "① taxonomy modality_ref",
     "flags": []
    }
   ],
   "products": [
    {
     "id": "product:M9-1-1",
     "name": "울쎄라",
     "license": "정상"
    }
   ],
   "sections": {
    "method": "[facts]",
    "recovery": "[facts]",
    "safety": {
     "side_effects": "[facts]",
     "complications": "[facts]",
     "state": "값|해당 없음|정보 없음"
    },
    "checks": "[{condition, grade3}]",
    "aftercare": "[facts]"
   },
   "flags": [
    "default_value(부위 기본값)",
    "candidates",
    "…"
   ],
   "link_key": "unit_procedure:U5-103"
  }
 ],
 "family_only": [
  {
   "family": "family:M2",
   "reason": "앵커 부위 없음|이 부위 단위 시술 없음",
   "flags": [
    "gap"
   ]
  }
 ],
 "pairs?": "[pair_check 결과 — 조합 질문일 때]",
 "facts": [
  {
   "id": "ST-M9-moa-01|SE-M9-01|CX-M9-01|K8-…|R8-…|U5-140.ops",
   "text": "원문 그대로",
   "flags": [],
   "source": "evidence_source id?"
  }
 ],
 "claude_contract": {
  "allowed_fact_ids": "[facts[].id]",
  "must_show_flags": [
   "conflict",
   "candidates",
   "gap",
   "weak",
   "question",
   "default_value",
   "license_unconfirmed"
  ],
  "rule": "카드 밖 말 금지 — 문장마다 facts id 하나 이상 · 숫자 · 기간 · 금기는 facts 원문 값만 · 충돌은 양쪽 · gap 은 「정보 없음」 · 후보 여럿이면 되묻기"
 }
}
```

## 7. 속도 · 정확성 장치

| id | 장치 | 규칙 | 근거 |
|---|---|---|---|
| S1 | 응답 크기 | 카드 기본 slim(id · 이름 · 요약 facts) — 중앙 2.6KB · 최대 5.0KB. 원문(계열 원문 · 합병증 상세)은 sections 요청 때만 — full 중앙 12.8KB · 최대 18.4KB(162 단위 합 1.78MB) | 계산 |
| S2 | 관계는 쌍 질문에서만 | 단위 시술 하나의 관계 이웃 중앙 70 · 최대 161 → 카드에 관계 목록을 싣지 않고 pair_check 로만 | 계산 |
| S3 | 홉 제한 | 정해 둔 경로(P-01~P-11)는 고정 홉. neighbors 는 depth ≤ 2 · limit 50 · truncated 표시 | 관계 주장 1개가 2,184 단위 쌍으로 펼쳐짐(R8-0239 「열 시술 후 주입」) |
| S4 | 메모리 그래프 · 빌드 때 펼침 | 골드 24,392 행을 빌드 때 계산해 적재 — 요청 때는 dict 조회만(32만 조회 0.086초 · 추천 4 질의 0.54ms, 파이썬) | 계산 |
| S5 | 근거 인용 | facts 마다 정본 id + 원천(evidence_source) — Claude 는 그 id 만 인용 | 근거 문장 119 · 출처 69 |
| S6 | 표시 전달 | 표시 12 를 행마다 그대로(conflict · conditional · candidates · weak · question · not_recommended · gap · default_value · unresolved · not_procedure · by_sub_condition · license_unconfirmed) — Claude 계약에 must_show | semantic §6-2 |
| S7 | 빌드 일관성 assert | 합병증 펼친 행 = 실버 units_inherit 285 · I4 = 5단계 기록 1,364 · 저장 엣지 = semantic 셈 — 다르면 빌드 실패 | 계산에서 285 = 285 확인 |

## 8. 결정 묶음(추천대로 진행 가능 — 코디 확인)

### A 골드 펼치기

| id | 결정 | 추천 | 왜 |
|---|---|---|---|
| D-01 | 골드 = 단위 시술 수준으로 빌드 때 전부 펼쳐 적재(24,392행) · 와일드카드 · 전역 조건만 전역 행 | 추천 | 사용자 10-30 「규칙을 다 적용한 그래프」 · 규모상 ms |
| D-02 | treats 계열만 81 은 펼치지 않음 · semantic I1 문구 「추천 계열만」을 SPEC-005 에서 뺌 | 추천 | 10-29 W2 사용자 결정과 충돌(펼치면 970행) |
| D-03 | I4 는 5단계 규칙 재구현 + 기록 1,364 와 같음 assert | 추천 | 기법 호환이 1,302행을 거름 — 단순 계열 상속은 틀림 |
| D-04 | combo_component 에 비교 members 107 · upgrade 12 포함(581) | 추천 | semantic 셈 462 가 components 만 셈 |

### B 기본 응답 · 안전

| id | 결정 | 추천 | 왜 |
|---|---|---|---|
| D-05 | 기본 응답 거르기 G12 · gate 3값 전부 통과 · 미확인은 표시로 | 추천 | 10-27 W-1 · semantic 6-3(「미확인」은 상태 아님) |
| D-06 | 안전 묶음 G13 은 늘 동봉 · gap 3상태 | 추천 | 10-26 경계 |
| D-07 | 부작용 덮어쓰기 값 = 적재가 브론즈 extracted 원문을 실버 attach 표대로 · 우선 제품×계열(×하위) > 단위 > 계열 · 계열 값은 override_of 로 보존 · 합병증 안 덮음 | 추천 | 실버엔 키만 있음(확인) · 10-27 extracted 노드 속성 결정 |

### C 충돌 · 조건부 · 간격 읽기

| id | 결정 | 추천 | 왜 |
|---|---|---|---|
| D-08 | 쌍 요약 결정론(값 집합) · 충돌이면 양쪽 id · 고르지 않음 | 추천 | D-13b |
| D-09 | by_sub_condition 은 options 그대로 · 쌍 요약도 option 별 | 추천 | reading_contract |
| D-10 | 이전 시술 경과 판정 = 경과일 ≥ days 하한이면 충족 · 상한은 원문 표시만 · same_day 는 경과 0 일 때 | 추천 | reading_contract days = [하한, 상한] · 샘플 「6주 전 보톡스」 |

### D 사전 · 부위

| id | 결정 | 추천 | 왜 |
|---|---|---|---|
| D-11 | resolve = 완전 일치 → 낱말 나눔 → 접두 일치(「부분 일치」 표시) · 못 찾은 낱말 unmatched 반환 + 허브 보강 후보 기록 | 추천 | 「턱선 처짐」 · 「Sofwave」 가 완전 일치로 안 잡힘(실측) |
| D-12 | 부위 없이 고민만 → 기본 영역 얼굴 + 「다른 영역 시술 있음」 표시 | 추천 | 10-30 「피부 고민 기본 영역 = 얼굴」 · 「처짐」 단독 27 단위 중 바디 5 |
| D-13 | 질의 부위 거르기 = R21 층 규칙(층 범위는 U-1) | 추천 | 저장 엣지와 같은 규칙 |

### E 응답 · 속도 · 인용

| id | 결정 | 추천 | 왜 |
|---|---|---|---|
| D-14 | 카드 slim 기본 · 원문은 sections 요청 · 관계는 pair_check 로만 | 추천 | S1 · S2 셈 |
| D-15 | neighbors depth ≤ 2 · limit 50 · truncated | 추천 | R8-0239 2,184 쌍 |
| D-16 | Claude 계약 = facts id 인용 · must_show 표시 · 숫자 · 기간 · 금기는 원문 값만 | 추천 | 「카드 밖 말 금지」 · 샘플 「2주 사우나」 ↔ 원천 「당일」 |

### F 경계 · 보강 후보

| id | 결정 | 추천 | 왜 |
|---|---|---|---|
| D-17 | 미라쥬 영역 → 허브 id 대응은 연결 층(장비 어댑터) · 허브는 site · concern id 만 | 추천 | 10-30 「표준 꼴 + 소스별 어댑터」 · 눈물고랑 · 밝기 · 피지 사전 없음 |
| D-18 | 샘플 대조 빈칸 → 허브 보강 후보 목록: 쥬비덤 볼루마 품목 · 「Sofwave」 단독 표기 · 소프웨이브 2주 사우나(원천 없음) | 추천 | 10-30 「허브에 없는 건 보강 후보 목록만」 |

## 9. 사용자 최종 판단

| id | 질문 | 보기 | 추천 | 왜 |
|---|---|---|---|---|
| U-1 | 고민 × 부위 추천에 「얼굴 전체」 시술을 같이 낼까 | 가까운 층만(R21 그대로) — 턱선 처짐 = 턱선 HIFU · 턱선 실리프팅 · 턱선 보톡스 3 / 가까운 층 + 얼굴 전체(층 표시 다르게) — 턱선 처짐 = 3 + 8(소프웨이브 · 얼굴 전체 HIFU · 고주파 · 실리프팅 · 스킨부스터 2 · 콜라겐부스터 · 마이크로웨이브) | 가까운 층 + 얼굴 전체(층 표시) | 샘플은 턱선 처짐에 소프웨이브(U5-140 · 부위 원천 없음 → 얼굴 전체 기본값)를 추천 — 가까운 층만이면 안 나옴. 이마 주름 · 팔자도 얼굴 전체 10 이 더해짐 |
| U-2 | 허브 도구를 누가 부르나 | 앱 서버(Jev 슬롯 → 앱 서버가 허브 호출 → 결과 + 계약을 Claude 에) / Claude 가 MCP 도구로 직접 | 앱 서버 | 결정론 경로 · 응답 크기 · 패널 갱신을 앱이 쥠 · Claude 는 facts 로만 문장 — 여러 홉 예외 질문만 Claude 에 neighbors 를 열지 따로 |
| U-3 | 병원 가격이 없을 때 허브 시장가(원천 범위)를 보여 줄까 | 안 보임(가격 = 연결 층만) / 「시장가 참고」 표시로 보임 | 안 보임 | 화면 가격은 병원 상품(연결 층) · 허브 시장가 122 는 원천 범위값이라 상담 화면 가격과 섞이면 오해 |

## open

없음 — 결정 묶음 · 사용자 판단 표에 다 올림
