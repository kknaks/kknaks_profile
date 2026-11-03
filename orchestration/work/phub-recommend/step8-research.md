# 실버 8단계 조사 — 관계 · 확인 조건 · 안전 · 근거 (read-only)

조사 워커 산출 · 2026-10-29 · 결정 아님(추천). 정본 `step8-research.json`. 원천 `phub-stg-2026-10-26` 은 읽기만 했다. 이름 해석은 5단계 정본(`step5-units` 162 키 · 장비 이름 동의어 · 1단계 제품 → product_links) · 2단계 계열 · 3단계 부위 · 4단계 기법 사전으로만, 고르지 않고 후보 전부 + 표시.

## ① 결정 묶음 (추천)

| # | 묶음 | 추천 | 근거 | 셈 |
|---|---|---|---|---|
| G1 | 시술↔시술 엣지 하나 + 주장 칸 | 끝점 쌍마다 엣지 하나(D-03) · 주장마다 원천 · 원문 · 종류(13) · 원문 등급 + 사이트 라벨 · 간격 원문(+비교용 범위) · 먼저 하는 쪽(원문 근거) · 이유 · 조건(CC · 고민×중증도 · 하위 조건) · 근거 id · gate_status · lowering(D-04). 주장 종류: 병행 · 간격 / 시너지(함께) / 순서 · 간격(다음에) / 대체(택 1) / 같은 날 불가 / 간격 / 간격 금기 / 재시술 간격(자기 쌍) / 시너지(CC 조합) / 순서(문장) / 원칙 문장 / 조합 규칙 | DEC-001 D-03 · D-04 · 10-26 「시너지 · 순서 · 간격 · 금기 = 엣지 하나의 속성」 · SPEC-004 §3.3.1 | 주장 389 |
| G2 | 끝점 단위 = 원천 이름이 가리키는 만큼 | 원천 시술군 코드(contraindications 27)는 계열 끝점 · 단위 시술은 조회 때 상속(C4) / 이름 원천은 5단계 정본으로 풀어 단위 시술 · 하나면 「이름 일치」 · 여럿이면 「후보 전부」(고르지 않음 · SPEC §3.3.2) / 하위 계열 · 기법 · 부위 낱말은 조건에 맞는 단위 시술 후보 + 원문 보관 / 「/ + or」 는 원소마다 끝점(복합) / 7단계 CC 엣지(③)는 그대로 재사용 | C4 · SPEC-004 §3.3.2 · 7단계 log §5-2 「부위 밖 0」 | 단위 시술 358; 계열 274; 복합(나눔) 38; 하위 계열 37; 기법 조건 25; 제품 → 단위 시술 19; 부위 조건 10; 조건 일치(낱말 교집합) 7; 용도 조건 4; 계열 묶음 3; 시술 아님 2; 모든 시술 1 |
| G3 | 대체(택 1) = 시너지 아님 | synergy type 「대신」 16 = 주장 종류 「대체(택 1)」 · 시너지로 세지 않음 | source-map C9 · B06 ④(승인) | 16 |
| G4 | 원칙 · 규칙 · 위험 문장의 쌍 = 수작업 대응표(게이트) | treatment-sequence principles 13 중 쌍 문장 8 → 주장 12 · combination_rules 6 → 11 · problem-combos riskBenefit 순서 문장 8 → 15 · 합 38 = gate_status unconfirmed + manual_map 표시 · 초기값 = 대응표. 원칙 5(클렌징 순서 · 채널 도포 가드 2 · 침습도 · 출혈) = 원문만(파생 계산 안 함 · B06 ⑥) | B06 ② · ⑥ · 10-27 승인 게이트 | 38 |
| G5 | 문장 화살표 · 「A 후 N 내 B 금지」 분해 | treatment-optimization sequence 24 → 42 · common_combos note 3 → 4 = 「문장 분해」 표시 · unconfirmed(기본 응답 제외 · include_unconfirmed 로) · contraindicated_combos 「A 후 N 내 B 금지」 꼴 10 = auto(꼴이 하나 · 금지 문장). 안전 주장(금지 · 같은 날 불가 · 간격)은 게이트 상태와 무관하게 기본 응답에서 거르지 않음(SPEC §4.1) | SPEC-004 §4.1 W-1 · D-06 | 분해 unconfirmed 48 · auto 10 |
| G6 | 충돌 = 전부 보존 + 「충돌」 표시 | 계열 쌍 기준 충돌 21(순서 · 같은 날 · 간격 수치) · 확인 조건 등급 충돌 76 · 이소트레티노인 기간 1 — 자동으로 고르지 않음 · 엣지 review_status=conflict · 의료진 질문(대표만) | DEC-001 D-13b · 10-29 6단계 결정(꿀광토닝 선례) | 21 + 76 + 1 |
| G7 | 시술 아닌 원소 · 묶음 낱말 | 트라넥삼산 경구 · 국소 · 미백약 · 비타민C 도포 · 왁싱 · 전기분해 = 「시술 아님」 끝점(엣지 안 세움 · 원문 보관 · 7단계 not_procedure 선례) 6주장 · 「열시술」 「에너지 기기」 「주입 시술」 「모든 시술」 = 묶음 끝점(후보 계열 전부 + 「묶음 낱말」 · 충돌 셈에서 뺌) 3주장 | 7단계 log §6 「시술 아님 6묶음」 · 추정 금지 | 6 · 3 |
| G8 | 6단계 메모 37 = 시너지의 「함께 판매」 근거 | 패키지 쌍은 새 엣지 아님 · 같은 synergy 링크 주장에 근거로 연결(링크 번호 그대로) · 「다름」 12 = 충돌 표시(꿀광토닝 선례) · 링크 없음 = 근거만 | _RESUME 10-29 6단계 결정 | 37(연결 23 · 다름 12) |
| G9 | procedure-profiles 플래그 = 계열 원문 속성 | hasProtein · hasHA · createsWound · createsChannel · thermalLoad 등 17계열 = 원문 속성 · 파생 엣지 계산 안 함(사이트 플래너 lib/synergy-algorithm.ts 가 쓰는 값이라 그대로 보존) | B06 ⑥ | 17 |
| G10 | 확인 조건 원장 | 조건 노드 53(결정론 사전 · 패턴 칸 공개) · 시술 → 조건 엣지 주장 330 — 원문 등급 + 3분류(금기 196 · 주의 55 · 확인만 79) · 끝점: 공통 12 = 「모든 시술」 1벌(조회 때 상속) · 계열별 = 계열 · 원장 항목 11 = 5단계 행선지(단위 시술 · 제품) · 이소트레티노인 쌍 5 = 조건 C-ISO ↔ 시술(C10) · 연령대 = 조건 C-AGE(20대~50대+) → avoid 6. 상담 22 · 시술 준비 5 · 고지(조건 없음) 6 = 계열 원문 속성(조건 엣지 아님) · 사람 조건 아닌 문장 4 = 계열 원문(부위 2 · 효과 · 근거 수준) | B04(승인) · 10-28 「확인 조건」 이름 · C10 | 노드 53 · 주장 378 |
| G11 | 합병증 노드 65 · has_complication | complications 정본 65 = 계열마다 따로 노드(같은 이름 「감염」 · 「PIH」 도 계열별) · 중증도 원문 + 사이트 라벨(경미 · 중등도 · 중증 · 위급) · 발생률 · 발현 · 지속 · 기전 · 위험 인자 · 처치 · 예방 원문 · 근거 URL → 웹 근거 노드 · 원천 없는 계열 17 = gap no_complication(추정 안 함) · taxonomy · extracted 부작용 문장 = 계열 · 단위 시술 근거 문장(합병증 노드와 글자 대응 안 함) | B13(승인) · SPEC-004 §3.3.3 D | 65 |
| G12 | 위험지대 = site_caution 엣지 속성 | zone 11 × (보톡스 M1 · 필러 M2) = 엣지 22 · 부위 = 3단계 danger_zone_mapping(묶음 넓은 쪽) · 속성: 위험도 · 혈관 · 신경 · 조직 계측 · 요령(clinical_pearls) · 보톡스/필러 핵심 경고 원문 · safe_layers = 4단계 참조(복사 안 함) · 그 부위에 계열 단위 시술이 없어도 엣지 둠(7) · critical_safety_facts = M2 안전 원문 | 10-28 해부학 결정 · B13 · C1 | 22 |
| G13 | 계열 안전 · 상담 원문 · 붙는 단위 | 필수 고지 109(원문 그대로 · 쪼개지 않음) · 즉시 내원 징후 55 · 환자 설명 17(+질문 51) · 사후관리(taxonomy 17 · profiles 17) · 부작용 문장 = 계열 속성 → 단위 시술 상속 · 경과표 10 = 계열 · 하위(hifu-rf = M9 HIFU · RF 단위 시술 · fractional-co2 = U5-028 · chemical-peel-mid = U5-034 + 깊이 원문 · dca-injection = N1) · PIH 위험 요인/예방 26 = 5단계 pih 붙은 단위 시술 그대로 · 원장 항목 aftercare/safety = 5단계 행선지 · N1 은 M16 원천 안 빌림(C5) | B05(승인) · C5 | 계열 17 · 경과 10 · PIH 26 |
| G14 | 근거 노드 | 문헌 25(PMID 키 · DOI · PMC · OA URL) · 근거 문장 119(기전 · 부작용 · 효과 · 정확도 원문 · 다국어 환자 문장 ko/en/zh/ja = 문장 노드 속성) · 웹 29(합병증 URL 38 중복 제거) · 가이드 · 표기 15(간격 source · 규칙 evidence — PMC 번호가 문헌과 맞으면 문헌 노드로) · 강도 = 원문 등급만(optimization evidence_level · 규칙 priority · consensus · contraindications level) — 숫자 만들지 않음 · evidence_kind = 파일 consensus_method 원문(4파일) · 나머지 「원천 표기 없음」 · 이유 문장 안 인용 표기는 자동 추출 안 함(원문 보관) | B11 · D-04 · OQ-111 | 188 |

## ② 사용자 최종 판단 — 한 표

| # | 판단 | 추천 | 다른 안 | 사용자 몫인 이유 |
|---|---|---|---|---|
| U8-1 | 사람이 문장을 쌍으로 옮긴 주장(38) · 화살표 분해 주장(48) — 사람 확인 게이트 페이지에 올릴지 | (가) 전부 unconfirmed 로 넣고 게이트 페이지(초기값 = 조사 대응표) — 승인된 것만 기본 응답 · 안전 주장은 상태와 무관하게 응답(SPEC §4.1) | (나) 화살표 분해는 결정론이라 auto · 수작업 대응 38 만 게이트 | 게이트 분량(86) vs 기본 응답에서 빠지는 순서 정보 — 운영 비용 판단 |
| U8-2 | 고민 조건 금기(「기미에 고에너지 레이저 · IPL 단독 금지」 6)를 어디에 두나 | (가) 7단계 고민 노드 「기미」 → 단위 시술(레이저 · IPL) 새 엣지 종류 「피함(금기 조합)」 — 고민 낱말은 고민 노드 하나만(7단계 W3 교훈) · SPEC-004 엣지 타입 +1 | (나) 확인 조건 노드 「기미」를 따로 세움 — 고민 노드와 같은 말을 둘이 나눠 가짐 | 엣지 타입 추가(SPEC 개정) 여부 |

나머지(G1~G14 · open 표 전부)는 승인된 결정(B04 · B05 · B06 · B11 · B13 · C4 · C9 · C10 · D-13b · 10-28 해부학 · 10-29 6단계)의 직접 귀결이라 추천대로면 된다.

## ③ 셈

| 항목 | 셈 | 내역 |
|---|---|---|
| 관계 주장 | **389** | 시너지(CC 조합) 137 · 시너지(함께) 50 · 순서 · 간격(다음에) 49 · 순서(문장 화살표) 46 · 병행 · 간격 27 · 대체(택 1) 16 · 순서(문장) 14 · 같은 날 불가 12 · 원칙 문장(쌍) 12 · 조합 규칙(쌍) 11 · 간격 9 · 간격 금기 5 · 재시술 간격(자기 쌍) 1 — gate auto 303 · unconfirmed 86(수작업 38 · 분해 48) |
| 관계 원천별 | 389 | problem-packages.complaints[].combos 137 · synergy.links 115 · treatment-optimization.by_concern.sequence 42 · contraindications.rules 27 · problem-combos.riskBenefit 15 · treatment-sequence.principles 12 · treatment-optimization.combination_rules 11 · treatment-optimization.by_concern.contraindicated_combos 10 · treatment-sequence.minimum_intervals 7 · treatment-sequence.incompatible_same_day 6 · treatment-sequence.common_combos.note 4 · problem-packages.complaints[].alternatives 2 · taxonomy.modality[].products[].extracted.safety.contraindications 1 |
| 충돌 | **21 + 76 + 1** | 계열 쌍 순서(먼저 하는 쪽) 13 · 같은 날 가능 ↔ 불가 4 · 간격 수치 4 / 확인 조건 등급 76 / 이소트레티노인 기간 1 |
| 확인 조건 | 노드 **53** · 주장 **378** | 사람 조건 325 · 상담 항목 22 · 고지 항목 6 · 연령대 조건 6 · 시술 준비 항목 5 · 사람 조건(시술 쌍에서 옮김 · C10) 5 · 고민 조건 금기(사람 조건 아님 — 7단계 고민 노드 기미) 5 · 부위 조건(사람 조건 아님 — 부위 × 제품) → site_caution 후보 1 · 효과 문장(조건 아님) → 계열 원문 속성 1 · 부위 조건(사람 조건 아님) → site_caution 후보 1 · 근거 수준 문장(조건 아님) → 계열 원문 속성 1 / 사람 조건 3분류 금기 196 · 확인만 74 · 주의 55 · 확인만(고지) 5 · 사전 밖 0 |
| 합병증 | **65** | 계열 10 · 원천 없는 계열 17(gap) |
| 주의 엣지(site_caution) | **22** | zone 11 × M1/M2 · 그 부위 단위 시술 없음 7 |
| 근거 | **188** | 문헌 25 · 문장 119 · 웹 29 · 가이드/표기 15 |
| 원천 쌍 아닌 것(속성) | 59 | combo-recipes.followUp 28 · problem-packages.combos 21 · problem-combos.riskBenefit 5 · problem-packages.complaints[].alternatives 4 · treatment-optimization.combination_rules 1 |
| open 후보 | **14 — 전부 해결 안 있음(빈 추천 0)** | 이름 안 풀림 1 · 코드 어긋남 9 · 충돌 · gap 등(⑤ 표) |
| 사용자 판단 · 원천 질문 | 2 · 11 | 의료진 8 · 병원 3 |

---

## A. 시술↔시술 관계

### A-1. 원천별 쌍 주장

| 원천 | 원천 행 | 주장 | 끝점 해석 | 비고 |
|---|---|---|---|---|
| `problem-packages.complaints[].combos` | 146 | 137 | 7단계 CC 엣지(③) 재사용 | 조건 = CC · 원소 1개 21 속성 |
| `synergy.links` | 115 | 115 | 이름 해석(코드는 source_code) | 함께 50 · 다음에 49(timing 「X N주 후 Y」 로 먼저 하는 쪽) · 대신 16 = 대체 · target = 조건 |
| `treatment-optimization.by_concern.sequence` | 24 | 42 | 화살표 분해 | 조건 = 고민 × 중증도 · evidence_level 원문 |
| `contraindications.rules` | 27 | 27 | 계열 코드 그대로(C4 상속) | level 원문 safe/caution/warning + 사이트 라벨 「병행 가능 · 간격 필요 · 주의 필요」(contraindications 화면 — caution=간격 필요 · warning=주의 필요) · 「X 먼저」 원문에서 먼저 하는 쪽 · 하위 조건(박리/비박리) 원문 |
| `problem-combos.riskBenefit` | 13 | 15 | 수작업 대응표 | 순서 문장 8 → 15 · 나머지 5 속성 |
| `treatment-sequence.principles` | 13 | 12 | 수작업 대응표 | 쌍 문장 8 → 12 · 원문만 5 |
| `treatment-optimization.combination_rules` | 8 | 11 | 수작업 대응표 | 쌍 6규칙 → 11 · priority/consensus 원문 = 강도 |
| `treatment-optimization.by_concern.contraindicated_combos` | 17(24칸 중) | 10 | 문장 분해 | 쌍 10 · 고민 · 사람 조건 7 → B |
| `treatment-sequence.minimum_intervals` | 9 | 7 | 이름 해석 | 이소트레티노인 2 → B · min_days/months 원문 · source → 근거 · 「필러 → 필러(동일 부위 재시술)」 = 자기 쌍(재시술 간격) |
| `treatment-sequence.incompatible_same_day` | 9 | 6 | 이름 해석 | 이소트레티노인 3 → B · 「HA 필러 주입 후 RF/HIFU」 1원소 = 방향 있는 쌍 · 「모든 시술」 = 와일드카드 |
| `treatment-sequence.common_combos.note` | 3 | 4 | 화살표 분해 |  |
| `problem-packages.complaints[].alternatives` | 6 | 2 | 문장 분해 | 간격 2 · 터치업 4 속성 |
| `taxonomy.modality[].products[].extracted.safety.contraindications` | 1 | 1 | 제품 → 단위 시술 | 미라클(M7-P-2) PDO + 비가교HA |

`treatment-sequence.sequence_order` 11 단계 = 쌍이 아니라 같은 날 순위 표(`A_relations.sequence_rank` — 범주마다 끝점 해석). 순위로 쌍을 만들지 않는다(파생 계산 안 함). `procedure-profiles` 플래그 17 = 계열 원문 속성(G9).

### A-2. 끝점 해석 결과

| 끝점 수준 | 셈 |
|---|---|
| 단위 시술 | 358 |
| 계열 | 274 |
| 복합(나눔) | 38 |
| 하위 계열 | 37 |
| 기법 조건 | 25 |
| 제품 → 단위 시술 | 19 |
| 부위 조건 | 10 |
| 조건 일치(낱말 교집합) | 7 |
| 용도 조건 | 4 |
| 계열 묶음 | 3 |
| 시술 아님 | 2 |
| 모든 시술 | 1 |

원천 코드 ↔ 정본 계열 어긋남 9: R8-0042 M17-엑소좀(원천 코드 M17 ↔ 해석 계열 M5) · R8-0076 M4-쥬베룩(원천 코드 M4 ↔ 해석 계열 M3) · R8-0078 M4-쥬베룩(원천 코드 M4 ↔ 해석 계열 M3) · R8-0079 M4-쥬베룩(원천 코드 M4 ↔ 해석 계열 M3) · R8-0080 M4-쥬베룩(원천 코드 M4 ↔ 해석 계열 M3) · R8-0100 M8-서브시전(원천 코드 M8 ↔ 해석 계열 N4) · R8-0101 M8-서브시전(원천 코드 M8 ↔ 해석 계열 N4) · R8-0102 M8-서브시전(원천 코드 M8 ↔ 해석 계열 N4) · R8-0109 M4-쥬베룩(원천 코드 M4 ↔ 해석 계열 M3)

### A-3. 6 · 7단계 메모 반영

| 7단계 메모 원천 | 메모 | 주장 | 속성 | 처리 |
|---|---|---|---|---|
| `problem-packages.complaints[].combos` | 146 | 137 | 21 | 조합 125 → 쌍 주장 137(3원소 조합은 쌍 3개) · 원소 1개 조합 21 = CC 속성(쌍 아님) |
| `combo-recipes.followUp` | 28 | 0 | 28 | 레시피 후속 일정 = 7단계 추천 조합 속성 원문(쌍 아님 — 같은 레시피 안 회차 · 재시술) |
| `treatment-optimization.sequence` | 24 | 42 | 0 | 화살표 분해 — 이웃한 두 원소 = 순서 주장(간격 원문 · 중증도 조건 · 근거 등급) · 반복 문구는 repeat_text |
| `treatment-optimization.contraindicated_combos` | 17 | 10 | 0 · B 7 | 「A 후 N 내 B 금지」 10 = 쌍 주장 · 고민(기미) · 사람 조건(활성 여드름 · 선탠) 7 = B 확인 조건 / 고민 조건 |
| `problem-combos.riskBenefit` | 13 | 15 | 5 | 순서 문장 8 → 쌍 15(수작업 대응표 · 게이트) · 순서 아닌 위험 문장 5 = 추천 조합 속성 |
| `treatment-optimization.combination_rules` | 8 | 11 | 1 · B 1 | 규칙 6 → 쌍 11(수작업 대응표 · 게이트 · B06 ②) · 결절 예방 1 = M3 안전 원문 · 기미 1 = 고민 조건 |
| `problem-packages.complaints[].alternatives` | 6 | 2 | 4 | 실 시술 후 HIFU/RF 2 = 간격 주장 · 반영구 터치업 4 = 단위 시술 재시술 간격 원문 |
| `treatment-sequence.common_combos.note` | 3 | 4 | 0 | 화살표 분해 — 3 문장 → 쌍 4 |
| 합 | 245 | | | |

6단계 메모 37 → 시너지 근거(함께 판매): synergy 링크와 연결 23 · 「다름」 12(충돌 표시) · 링크 없음 = 근거만.

### A-4. 충돌 (같은 계열 쌍 · 다른 말 — 전부 보존)

| id | 쌍 | 종류 | 쪽별 주장 |
|---|---|---|---|
| X8-001 | M1 ↔ M2 | 순서(먼저 하는 쪽) | M1: R8-0001, R8-0153, R8-0163, R8-0192, R8-0194, R8-0238, R8-0249 / M2: R8-0162, R8-0186 |
| X8-002 | M1 ↔ M2 | 같은 날 가능 ↔ 불가 | 가능: R8-0001, R8-0028, R8-0032, R8-0058, R8-0062, R8-0162, R8-0186 / 불가: R8-0153 |
| X8-003 | M1 ↔ M9 | 순서(먼저 하는 쪽) | M1: R8-0031 / M9: R8-0121, R8-0125, R8-0131, R8-0138, R8-0156, R8-0157, R8-0178, R8-0179, R8-0193, R8-0197, R8-0236, R8-0237, R8-0248 |
| X8-004 | M11 ↔ M15 | 순서(먼저 하는 쪽) | M11: R8-0039 / M15: R8-0050 |
| X8-005 | M11 ↔ M5 | 순서(먼저 하는 쪽) | M5: R8-0209 / M11: R8-0221, R8-0245 |
| X8-006 | M11 ↔ M8 | 순서(먼저 하는 쪽) | M8: R8-0244 / M11: R8-0246 |
| X8-007 | M15 ↔ M4 | 간격 수치 | R8-0052: 필링 1주 후 스킨부스터 / R8-0082: 필링 1주 후 스킨부스터 / R8-0206: 2주 |
| X8-008 | M15 ↔ M8 | 순서(먼저 하는 쪽) | M15: R8-0151, R8-0219 / M8: R8-0175, R8-0187, R8-0205, R8-0218 |
| X8-009 | M15 ↔ M8 | 같은 날 가능 ↔ 불가 | 가능: R8-0111, R8-0205 / 불가: R8-0144, R8-0151, R8-0175 |
| X8-010 | M2 ↔ M8 | 순서(먼저 하는 쪽) | M2: R8-0150, R8-0167 / M8: R8-0152, R8-0161, R8-0171, R8-0172, R8-0173, R8-0185 |
| X8-011 | M2 ↔ M8 | 같은 날 가능 ↔ 불가 | 가능: R8-0119 / 불가: R8-0143, R8-0147, R8-0150, R8-0152, R8-0171, R8-0172, R8-0173, R8-0185 |
| X8-012 | M2 ↔ M8 | 간격 수치 | R8-0152: 14일 / R8-0185: 당일 금지 · 최소 4주 |
| X8-013 | M2 ↔ M9 | 순서(먼저 하는 쪽) | M2: R8-0061, R8-0146, R8-0149, R8-0164, R8-0166, R8-0168, R8-0184 / M9: R8-0154, R8-0165, R8-0180 |
| X8-014 | M2 ↔ M9 | 같은 날 가능 ↔ 불가 | 가능: R8-0154, R8-0165 / 불가: R8-0146, R8-0149 |
| X8-015 | M3 ↔ M4 | 순서(먼저 하는 쪽) | M3: R8-0067, R8-0070, R8-0073 / M4: R8-0202 |
| X8-016 | M4 ↔ M8 | 순서(먼저 하는 쪽) | M4: R8-0077, R8-0084 / M8: R8-0105, R8-0108, R8-0110, R8-0112, R8-0116, R8-0120, R8-0189, R8-0207, R8-0214, R8-0234, R8-0247 |
| X8-017 | M4 ↔ M9 | 순서(먼저 하는 쪽) | M4: R8-0085 / M9: R8-0122, R8-0126, R8-0132, R8-0139, R8-0142, R8-0196 |
| X8-018 | M5 ↔ M8 | 순서(먼저 하는 쪽) | M5: R8-0090 / M8: R8-0208, R8-0221, R8-0223, R8-0247 |
| X8-019 | M7 ↔ M9 | 순서(먼저 하는 쪽) | M7: R8-0098, R8-0099, R8-0240, R8-0252, R8-0258 / M9: R8-0133, R8-0199 |
| X8-020 | M7 ↔ M9 | 간격 수치 | R8-0098: 실리프팅 1개월 후 써마지 / R8-0099: 실리프팅 후 2~3개월 뒤 울쎄라 / R8-0240: 2~3개월 간격 필요 (같은 날이면 다른 부위) / R8-0252: 2개월간 피할 것 / R8-0258: 2개월간 피할 것 |
| X8-021 | M7 ↔ M9 | 간격 수치 | R8-0133: 울쎄라 1개월 후 실리프팅 / R8-0199: 2-4주 |

셈 기준: 끝점의 계열 쌍(묶음 낱말 · 시술 아님 끝점 제외). 「먼저 하는 쪽」은 원문 근거(「X 먼저」 · 화살표 · 「N주 후」 · from→to)가 있는 주장만. 간격 수치는 같은 방향끼리 원문 범위가 겹치지 않을 때만. 같은 날 / 별도 세션 / 하위 조건 차이로 설명되는 것도 그대로 올렸다 — 설명 여부는 의료진 질문(Q8-2~6).

## B. 확인 조건 원장

| 조건 id | 이름 | 주장 | 원천 |
|---|---|---|---|
| C-PREG | 임신 | 37 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-BF | 수유 | 30 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-KEL | 켈로이드 체질 | 22 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-ANTICOAG | 항응고제 · 항혈소판제 | 21 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-NSAID | NSAIDs | 3 | consent-checklist · pre-procedure-checklist |
| C-ISO | 이소트레티노인 | 18 | consent-checklist · pre-procedure-checklist · taxonomy · treatment-sequence |
| C-RETIN | 레티노이드 처방 | 3 | consent-checklist · pre-procedure-checklist |
| C-HSV | 헤르페스 병력 | 4 | pre-procedure-checklist |
| C-AUTO | 자가면역질환 | 15 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-METAL | 체내 금속 · 금속 임플란트 | 15 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-PACE | 심장박동기 · 이식형 전자장치 | 12 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-ALLERGY | 알레르기 · 과민반응 병력 | 24 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-INFECT | 시술 부위 감염 · 염증 | 45 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-ACNE | 활동성 여드름 | 9 | consent-checklist · pre-procedure-checklist · taxonomy · treatment-optimization |
| C-DERM | 시술 부위 피부질환 · 피부 상태(피부염 · 습진 · 건선 · 로사세아) | 10 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-NMJ | 신경근 질환 | 6 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-EPI | 간질 · 경련성 질환 | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-NEURO | 신경계 질환 | 1 | pre-procedure-checklist |
| C-BLEED | 출혈 경향 · 응고장애 · 혈액질환 | 14 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-DM | 당뇨 · 면역저하 · 면역억제 | 13 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-CANCER | 악성종양 · 암 병력 | 6 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-CHF | 심부전 · 신장 질환 | 8 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-G6PD | G6PD 결핍증 | 3 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-COLD | 한냉 질환(한냉두드러기 · 한냉글로불린 · 한냉혈색소뇨 · 레이노) | 11 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-PHOTO | 광과민성 질환 · 약물 | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-SUN | 일광노출 · 태닝 · 자외선 차단 불가 | 5 | consent-checklist · pre-procedure-checklist · taxonomy · treatment-optimization |
| C-AMINO | 아미노글리코시드 항생제 | 3 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-DPEN | D-페니실라민 | 1 | pre-procedure-checklist |
| C-MUSCLE | 근이완제 등 특정 약물 | 1 | taxonomy |
| C-LIDO | 마취제 알레르기(리도카인) | 1 | pre-procedure-checklist |
| C-HYAL | 히알루로니다아제 알레르기 | 1 | pre-procedure-checklist |
| C-PRIOR | 최근 · 이전 시술 이력 | 17 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-RESID | 잔여 필러 · 실 · 영구필러 | 4 | pre-procedure-checklist |
| C-DENTAL | 최근 치과 시술 | 1 | pre-procedure-checklist |
| C-FLIGHT | 48시간 이내 비행 | 1 | pre-procedure-checklist |
| C-CHRONINF | 만성감염(피부결핵 · 매독) | 1 | pre-procedure-checklist |
| C-FITZ | Fitzpatrick 피부타입 · 어두운 피부 · PIH 위험 | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-SURG | 최근 수술 · 흉터(시술 부위) | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-HERNIA | 탈장 | 4 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-BMI | 체형 · 피하지방 두께 · 저체중 | 6 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-LIVER | 간기능 · 지질 수치(레티노이드 처방) | 3 | pre-procedure-checklist |
| C-SKINCARE | 사용 중 스킨케어 제품 | 1 | pre-procedure-checklist |
| C-PEELALG | 필링 제제 알레르기 | 1 | pre-procedure-checklist |
| C-VASC | 혈관 접근 상태 | 1 | pre-procedure-checklist |
| C-SUPPL | 복용 영양제 · 약물 상호작용 | 6 | pre-procedure-checklist · taxonomy |
| C-SMOKE | 흡연 | 2 | consent-checklist · taxonomy |
| C-GRAN | 이물반응 · 육아종 병력 | 1 | consent-checklist |
| C-CARDIO | 심혈관 질환(허혈성 심질환 · 고혈압) | 2 | taxonomy |
| C-RADIO | 방사선 치료 중 | 1 | taxonomy |
| C-HORMONE | 경구 피임약 · 에스트로겐 | 1 | taxonomy |
| C-INDIC | 적응 범위 밖(수술적 교정 필요) | 1 | consent-checklist |
| C-EXPECT | 비현실적 기대 | 6 | pre-procedure-checklist · taxonomy |
| C-AGE | 연령대 | 6 | treatment-optimization |

| 원천 | 주장 | 끝점 | 원문 등급 → 3분류 |
|---|---|---|---|
| `pre-procedure-checklist.universal_checks` | 12 | 모든 시술(공통 · 1벌) | absolute → 금기 · relative → 주의 · must_check → 확인만 · inform → 확인만(고지) · counseling/safety_protocol = 상담 · 시술 준비 항목(조건 엣지 아님) · 사이트 라벨 절대금기 · 상대금기 · 필수 확인 · 고지 · 상담 · 시술 준비 |
| `pre-procedure-checklist.category_specific` | 123 | 계열 | 위와 같음 |
| `consent-checklist.contraindications` | 105 | 계열 | 등급 칸 없음 → 금기(화면 「금기사항」) |
| `taxonomy.modality[].extracted.contraindications.absolute` | 53 | 계열 | 절대 → 금기 |
| `taxonomy.modality[].extracted.contraindications.relative` | 55 | 계열 | 상대 → 주의 |
| `taxonomy.items[].extracted.safety.contraindications` | 11 | 5단계 행선지(단위 시술 · 제품) | 등급 칸 없음 → 금기 |
| `treatment-sequence.incompatible_same_day` | 3 | 시술(이름 해석) | 같은 날 불가(복용 중) → 금기 |
| `treatment-sequence.minimum_intervals` | 2 | 시술(이름 해석) | 대기 기간 → 주의 |
| `treatment-optimization.by_age_group.avoid` | 6 | 시술(이름 해석 · 양 · 빈도 문장은 못 풂) | avoid → 주의 |
| `treatment-optimization.by_concern.contraindicated_combos` | 7 | 시술 | 금지 → 금기(고민 조건 5 는 U8-2) |
| `treatment-optimization.combination_rules` | 1 | 시술 | 금지 → 금기(고민 조건) |

extracted.json ↔ taxonomy modality extracted(C6): 금기 · 사후관리 17계열 전부 같음 — taxonomy 정본, extracted.json 은 검증만.

등급 충돌 76(같은 계열 × 같은 조건 · 원천마다 등급 다름) 조건별: C-PREG 12 · C-BF 9 · C-INFECT 9 · C-ANTICOAG 7 · C-KEL 5 · C-ALLERGY 5 · C-BLEED 3 · C-AUTO 3 · C-PRIOR 2 · C-DM 2 · C-METAL 2 · C-DERM 2 · C-ISO 2 · C-AMINO 1 · C-NMJ 1 · C-EPI 1 · C-SURG 1 · C-COLD 1 · C-HERNIA 1 · C-RETIN 1 · C-CHF 1 · C-NSAID 1 · C-BMI 1 · C-FITZ 1 · C-PHOTO 1 · C-SUN 1

이소트레티노인 기간 충돌 XK-ISO: pre-procedure-checklist.universal_checks isotretinoin: 프락셔널/얕은 필링 6개월 · 박리성 12개월 원칙 · 비박리 얕은 시술 의사 판단 조기 / pre-procedure-checklist M8 · M11 · M12 · M15: 프락셔널/얕은 필링 6개월 · 박리성 12개월 대기 원칙 / treatment-sequence.minimum_intervals: 프락셔널/얕은 필링 0개월(0~2개월 의사 판단) · 박리성/심부 필링 6개월 / treatment-sequence.incompatible_same_day: 비박리 0~2개월 · 박리성 6개월

## C. 안전

### C-1. 합병증 노드 65

| 계열 | 노드 | 중증도(원문 → 사이트) |
|---|---|---|
| M1 | 7 | 경미 6 · 중등도 1 |
| M2 | 7 | 경미 5 · 중등도 1 · 중증 1 |
| M3 | 6 | 중등도 2 · 중증 2 · 위급 1 · 경미 1 |
| M7 | 8 | 중등도 3 · 중증 1 · 경미 4 |
| M8 | 3 | 중등도 1 · 경미 2 |
| M9 | 6 | 중증 1 · 경미 4 · 중등도 1 |
| M11 | 5 | 중증 3 · 중등도 1 · 경미 1 |
| M14 | 7 | 중증 1 · 위급 1 · 경미 4 · 중등도 1 |
| M15 | 4 | 경미 4 |
| M16 | 12 | 경미 7 · 중등도 2 · 위급 1 · 중증 2 |
| 원천 없음(gap) | M4, M5, M6, M10, M12, M13, M17, N1, N2, N3, N4, N5, N6, N7, N8, N9, N10 | no_complication |

### C-2. site_caution 22

| 엣지 | zone → 부위(3단계 대응) | 위험도 | 혈관 · 신경 | 그 부위 단위 시술 |
|---|---|---|---|---|
| SC-forehead-M1 | forehead → 이마 (같음) | 4 | 2 · 2 | 1 |
| SC-forehead-M2 | forehead → 이마 (같음) | 4 | 2 · 2 | 1 |
| SC-glabella-M1 | glabella → 미간 (같음) | 5 | 2 · 1 | 1 |
| SC-glabella-M2 | glabella → 미간 (같음) | 5 | 2 · 1 | 0 |
| SC-temple-M1 | temple → 관자놀이 (같음) | 4 | 2 · 2 | 0 |
| SC-temple-M2 | temple → 관자놀이 (같음) | 4 | 2 · 2 | 1 |
| SC-periorbital-M1 | periorbital → 눈가(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 5 | 3 · 2 | 1 |
| SC-periorbital-M2 | periorbital → 눈가(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 5 | 3 · 2 | 1 |
| SC-nose-M1 | nose → 코(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 5 | 3 · 2 | 2 |
| SC-nose-M2 | nose → 코(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 5 | 3 · 2 | 1 |
| SC-nasolabial-M1 | nasolabial → 팔자 (같음) | 4 | 2 · 2 | 0 |
| SC-nasolabial-M2 | nasolabial → 팔자 (같음) | 4 | 2 · 2 | 1 |
| SC-cheek-M1 | cheek → 볼(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 3 | 2 · 3 | 0 |
| SC-cheek-M2 | cheek → 볼(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 3 | 2 · 3 | 1 |
| SC-lips-M1 | lips → 입술 (같음 + 입꼬리 · 입가 · 인중(새) | 3 | 2 · 2 | 0 |
| SC-lips-M2 | lips → 입술 (같음 + 입꼬리 · 입가 · 인중(새) | 3 | 2 · 2 | 1 |
| SC-chin-M1 | chin → 턱끝 (턱끝 추천(확인 필요 → 근거 있음)) | 3 | 2 · 1 | 1 |
| SC-chin-M2 | chin → 턱끝 (턱끝 추천(확인 필요 → 근거 있음)) | 3 | 2 · 1 | 1 |
| SC-jawline-M1 | jawline → 턱선 (같음 + 사각턱 관련) | 4 | 2 · 2 | 1 |
| SC-jawline-M2 | jawline → 턱선 (같음 + 사각턱 관련) | 4 | 2 · 2 | 0 |
| SC-neck-M1 | neck → 목(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 2 | 2 · 2 | 2 |
| SC-neck-M2 | neck → 목(묶음) (묶음 추천(확인 필요 → 근거 있음)) | 2 | 2 · 2 | 0 |

### C-3. 계열 안전 · 상담 원문 · 붙는 단위

| 경과표 | 원천 코드 | 붙는 곳 |
|---|---|---|
| botox | M1 | 계열 — family:M1 |
| ha-filler | M2 | 계열(하위 HA — M2 단위 시술 키에 하위 없음 → 계열 전부) — family:M2 |
| hifu-rf | M9 | 하위 계열 HIFU · RF — family:M9 U5-102,U5-103,U5-154,U5-091,U5-104,U5-152 |
| fractional-co2 | M8 | 단위 시술 — unit:U5-028 U5-028 |
| thread-lift | M7 | 계열 — family:M7 |
| dca-injection | M16-DCA | 계열 N1(C5 — M16 원천 빌리지 않음) — family:N1 |
| needle-rf | M11 | 계열 — family:M11 |
| skin-booster | M4 | 계열 — family:M4 |
| biostimulator | M3 | 계열 — family:M3 |
| chemical-peel-mid | M15 | 하위 계열 화학 박피 · 중간 깊이(단위 시술 U5-034 얼굴 전체 필링 · 깊이 원문) — family:M15 U5-034 |

원장 항목 단위 원문 셈: aftercare 521 · safety.common 521 · safety.serious 187 · safety.note 4 · safety.long_term 1 — 붙는 곳 제품(→ 5단계 「이 제품으로 했을 때」 extracted) 309 · 단위 시술 175 · 행선지 6단계 패키지 16 · 행선지 원장님 문의 1 · 행선지 값 17 · 행선지 시술 아님(다른 단계) 2 · 행선지 시술 아님 1

## D. 근거 노드

| 종류 | 노드 | 키 | 붙는 곳 |
|---|---|---|---|
| 문헌 | 25 | PMID(없으면 DOI) | 근거 문장 119 → 문헌 · 규칙 evidence 의 PMC 가 맞으면 같은 노드 |
| 근거 문장 | 119 | ST-계열-분야-번호 | 계열(기전 50 · 부작용 32 · 효과 37) · 다국어 환자 문장 4개 언어 · accuracy 원문 |
| 웹 | 29 | URL | 합병증 근거 칸 38 |
| 가이드 · 표기 | 15 | 원문 표기 | 간격 source · 규칙 evidence |

- EV-GD-001 「JCD 2023」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-002 「ASDS 2024」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-003 「임상 가이드」 — 가이드 · 표기 출처 · 주장 4
- EV-GD-004 「피부 회복」 — 출처 아님(이유 문장) · 주장 1
- EV-GD-005 「PRS 논문」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-006 「MFU-보툴리눔독소 진피내 주입 RCT (J Cosmet Dermatol, PMC11945533)」 — 가이드 · 표기 출처 · 주장 6
- EV-GD-007 「HIFU-HA 필러 열분해 연구(2024)」 — 가이드 · 표기 출처 · 주장 6
- EV-GD-008 「보툴리눔독소 당일 병용 안전성 리뷰(2014/2020)」 — 가이드 · 표기 출처 · 주장 6
- EV-GD-009 「JCD 2023 논문」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-010 「임상 가이드라인」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-011 「임상 컨센서스」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-012 「제조사 가이드 + 임상 경험」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-013 「in vitro 연구」 — 가이드 · 표기 출처 · 주장 1
- EV-GD-014 「ASDS 2017 consensus」 — 가이드 · 표기 출처 · 주장 2
- EV-GD-015 「AAD 2024」 — 가이드 · 표기 출처 · 주장 2

evidence_kind(파일 방법 표기): anatomy-danger-zones: 3-AI Expert Consensus (Perplexity research + Gemini analysis / literature-evidence: Curated successor of v1.0. Citation identity and metadata no / post-procedure-timeline: Perplexity(리서치) + Gemini(분석) + Claude(교과서 종합) 3-AI 컨센서스 / treatment-optimization: 3-AI Expert Panel Consensus (Perplexity+Gemini+Claude) / 그 밖(contraindications · synergy · treatment-sequence · pre-check · consent · complications · pih · patient-education · profiles · problem-packages): 파일에 방법 표기 없음 → evidence_kind 「원천 표기 없음」

## E. 못 정하는 것 (해결 안 붙음) · 원천 질문

### ⑤ open 표

| id | 무엇 | 셈 | 해결 안(추천) | 물을 곳 |
|---|---|---|---|---|
| O8-01 | 이름이 안 풀린 원소(TCA Cross · 왁싱/전기분해) | 1 | TCA Cross = 원소 「못 풂」 + 원문 보관(같은 주장 서브시전 원소는 끝점 유지) + 의료진 질문 · 왁싱/전기분해 = 시술 원장 밖 → 「시술 아님」 처리 | 의료진 |
| O8-02 | 「듀얼파장 레이저」 → M8 후보 31(넓음) | 1 | 후보 전부 + 「넓음」 표시 · 제모 문맥이라 레이저 제모 부위 단위 시술로 좁힐 근거 없음 → 병원 질문(어느 장비 · 파장) | 병원 |
| O8-03 | 「HA 볼류마이징 스킨부스터」 · 「혈관레이저」 용도 낱말 | 2 | 스킨부스터 후보 3 · 혈관 = 엑셀V(U5-099) · 브이빔(U5-141) 후보 + 원문 · 병원 질문 | 병원 |
| O8-04 | 원천 시술군 코드 ↔ 정본 계열 어긋남 | 9 | 끝점은 정본 계열(쥬베룩 = M3 · 서브시전 = N4 · 엑소좀 = M5) · source_code 칸 보존 · 원천 수정 후보 목록(7단계 source-fix 선례) | 병원(원천 관리) |
| O8-05 | 순서 · 같은 날 · 간격 충돌(계열 쌍) | 21 | 전부 보존 + review_status=conflict · 대표 5 의료진 질문(아래 Q8-2~6) · 나머지는 하위 조건 차이(박리/비박리 · 같은 날/별도 세션 · 같은 부위)로 원문에 적힌 것 | 의료진 |
| O8-06 | 확인 조건 등급 충돌(같은 계열 × 같은 조건, 원천마다 금기 · 주의 · 확인만 다름) | 76 | 원천별 등급 그대로 + 「등급 충돌」 · 대표(임신 · 수유: consent 「금기」 ↔ taxonomy 「미루는 게 좋음」) 의료진 질문 | 의료진 |
| O8-07 | 이소트레티노인 중단 후 대기(6/12개월 ↔ 0~2/6개월) | 1 | 둘 다 보존 · 충돌 표시 · 의료진 질문 | 의료진 |
| O8-08 | 합병증 원천 없는 계열 | 17 | gap no_complication 표시(「없음 = 안전」 아님) · 추정 안 함 | — |
| O8-09 | site_caution 부위에 그 계열 단위 시술 없음 | 7 | 엣지 둠(부위 안전 정보는 앞으로 생길 단위 시술에도 상속) · units_note 표시 | — |
| O8-10 | 간격 출처 칸이 출처가 아닌 것(「피부 회복」) | 1 | 근거 노드 「출처 아님(이유 문장)」 표시 · 원천 수정 후보 | 병원(원천 관리) |
| O8-11 | 경과표 ha-filler 의 하위 HA — M2 단위 시술 키에 하위 없음 | 1 | M2 계열 전부에 상속(M2 단위 시술 시장가가 전부 HA) + 원문 이름 보관 | — |
| O8-12 | 사람 조건 아닌 문장이 금기 목록에 섞임(얇은 피부 부위 2 · 효과 1 · 근거 수준 1) | 4 | 계열 원문 속성 · 부위 문장 2 는 부위 표시(site_caution 은 anatomy M1/M2 만 — 새로 안 만듦) | — |
| O8-13 | 같은 이름 합병증이 여러 계열(감염 · PIH) | 2 | 계열마다 따로 노드(B13) — 합치지 않음 | — |
| O8-14 | 원문 이유 칸 안 인용 표기(「ASPS 권고」 「Global Aesthetics Consensus 2016」 등) | — | 근거 노드로 자동 추출 안 함 · 원문 보관(정규식 추출은 추정 위험) | — |

### 원천 질문

| id | 받는 사람 | 질문 | 관련 |
|---|---|---|---|
| Q8-1 | 의료진 | 이소트레티노인 중단 후 대기 기간 — 사전 체크(얕은 시술 6개월 · 박리성 12개월) ↔ 시술 순서(얕은 시술 0~2개월 · 박리성 6개월) 중 어느 쪽을 상담 기준으로 쓰나 | XK-ISO |
| Q8-2 | 의료진 | 보톡스 ↔ 필러 순서 — 같은 부위 「보톡스 먼저」(contraindications) · 같은 날 「필러 먼저」(순서 · 원칙 · 규칙) · 별도 세션 「보톡스 먼저 2주」 — 같은 날 / 별도 세션 / 같은 부위 조건으로 나눠 맞나 | X8-001, X8-002 |
| Q8-3 | 의료진 | 필러 ↔ 레이저 — 「레이저/IPL 은 필러 전에」 · 「필러 → 레이저 최소 5일」 · 「필러 후 레이저 2~4주(IPL 4주)」 · 「프락셔널 후 당일 필러 금지 · 4주」 — 레이저 종류별로 어느 값 | X8-010, X8-011, X8-012 |
| Q8-4 | 의료진 | 실리프팅 → 에너지 리프팅 간격 — 써마지 1개월(synergy) ↔ 울쎄라 · HIFU 2~3개월(synergy · contraindications · riskBenefit) ↔ HIFU/RF 2개월(problem-packages) / 울쎄라 → 실리프팅 1개월 ↔ 2-4주 | X8-019, X8-020, X8-021 |
| Q8-5 | 의료진 | 레이저 ↔ 니들RF 순서 — P5-3 「레이저 → 니들RF」 ↔ P7-3 「니들RF → 레이저」 · 필링 ↔ 니들RF 「니들RF 2주 후 필링」 ↔ 「필링 2주 후 니들RF」 | X8-004, X8-006 |
| Q8-6 | 의료진 | 필링 ↔ 레이저 같은 날 — 「토닝 → 같은날 얕은 필링」 · 「레이저토닝 + 필링 같은 날」 ↔ 「심부 필링 + 레이저 같은 날 불가」 · 「제모 부위 필링 동시 금지」 — 깊이 · 부위 조건으로 설명되나 | X8-008, X8-009 |
| Q8-7 | 의료진 | 확인 조건 등급 — 임신 · 수유가 consent 에선 「금기」 · taxonomy 에선 「미루는 게 좋음(상대)」(M1 등 계열 다수) — 계열별 등급 확인 | XK-003, XK-006, XK-011, XK-014, XK-020, XK-024, XK-030, XK-033 … |
| Q8-8 | 의료진 | 「TCA Cross(아이스픽)」 · 「HA 볼류마이징 스킨부스터」 · 「듀얼파장 레이저」는 어느 단위 시술인가(지금 정본에 키 없음 · 후보 넓음) | R8-0222 |
| Q8-9 | 병원(원천 관리) | 원천 시술군 코드 어긋남 — synergy 「M4-쥬베룩」(정본 M3) · 「M8-서브시전」(정본 N4) · 「M17-엑소좀」(정본 M5) 원천 수정 | R8-0042, R8-0076, R8-0078, R8-0079, R8-0080, R8-0100, R8-0101, R8-0102 … |
| Q8-10 | 병원 | synergy 「M8-혈관레이저」 = 엑셀V · 브이빔 중 무엇(둘 다)인가 | R8-0112, R8-0326, R8-0327, R8-0328, R8-0329, R8-0330 |
| Q8-11 | 병원(원천 관리) | treatment-sequence minimum_intervals 「프락셔널 CO2 → 필러 14일」 의 source 칸 「피부 회복」 은 출처가 아님 — 출처 보충 | R8-0152 |

## 알려진 한계

- 이름 해석 사전 중 「조사 사전」(json `resolver_alias`) 항목은 5단계 사전에 없는 원천 낱말(「실」 「PDO실」 「비가교HA」 「리프팅기기」 「써마지」 등)에 근거 칸을 달아 붙인 것 — 반영 때 5단계 동의어로 올릴지 함께 승인 대상(G2).
- 화살표 분해는 「→」 와 「N주 후 · 간격」 머리말만 읽는다. 「또는」 「or」 는 복합 끝점, 반복 문구(「4주 간격 반복」)는 repeat_text 로 둬 간격으로 세지 않았다.
- 등급 3분류 · 조건 사전은 원문 낱말 정규식이다. 한 문장이 조건 둘에 걸리면 둘 다 단다(고르지 않음).
- 이 판은 지금 원천 기준이다. 가상 문장 시험은 하지 않았다.
