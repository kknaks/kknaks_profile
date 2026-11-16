# problem-combos — 미결·한계

상태 문자: **A**=에이전트 추출/해석 오류 · **B**=원문 정보 부족 · **C**=현재 사용자 결정 필요 · 보조: **K**=알려진 분석 한계 · **P**=잠정 · **F**=후속 의미 조사 · **I**=원문 내 불일치.
원본 변경 제안은 현재 원본 보존 지시 아래 후속 확인 후보이며 선택 대기로 올리지 않는다.

## 요약

| 상태 | 건수 | 처리 상태 |
|---|---|---|
| A | 0 열림 | 작업 중 발견한 A 2건은 고침(아래 「고친 A」) |
| B | 5 | 열림 — 원문에 없음, 채우지 않음 |
| C | 0 | 아래 B·F·I 각각의 영향 검토 결과 지금 사용자 선택이 필요한 항목 없음(모두 후속 의미 조사·원장 간 비교 단계에서 다룸) |
| F | 6 | 열림 — 후속 의미 조사·원장 연결 |
| I | 5 | 열림 — 원문 내 불일치, 보존만 함(고치지 않음) |
| P | 1 | 잠정 관찰(구획 review 잠정 관찰 절에 다수 추가) |
| K | morphology.json `known_missegmentations` 81건 | 한계로 기록, 1차 종료를 막지 않음 |

## 열린 항목

| ID | 상태 | Pointer | 내용 | 영향 |
|---|---|---|---|---|
| I-PC-01 | B | `/combos/*/packages/*/priceRange` | 가격 범위 단위·기준(통화, 회당/패키지) 미기재. P5·P9만 `/회` 접미 | 가격 비교·정규화 불가. `만`을 원 단위로 바꾸지 않음 |
| I-PC-05 | B | `/combos/1/packages/3/riskBenefit` | 「시술 순서·간격 엄격 준수」 구체 간격 없음 | 간격 규칙 데이터화 불가 |
| I-PC-06 | B | `/combos/2/packages/1/products/0` | 「울쎄라 + 보톡스(엘러간) or 나보타」 or 적용 범위 괄호 없음 | 제품 조합 분해 시 두 해석 가능 |
| I-PC-08 | B | `/combos/3/packages/1/expectedResult` | 「1클」 약어 뜻 원문 없음 | 회차 단위 해석 불가 |
| I-PC-09 | B | `/combos/3/packages/2/riskBenefit` | 「SB」 약어 정의 없음(P5-3·P7-3 riskBenefit 에도 출현) | 스킨부스터 약어로 보이는 것은 잠정 |
| I-PC-02 | F | `/combos/*/packages/*/procedures/*` | M코드 정의가 이 원장에 없음 | 시술명 ↔ 코드 대응은 다른 원장과 연결 후 |
| I-PC-03 | F | `/combos/*/packages/*/products/*` | products 원소 안 `+`·`or`·`/`·`또는`·괄호 혼용, 결합 우선순위 원문 없음 | 제품 단위 분해는 후속 |
| I-PC-04 | F | `/combos/1/packages/2/procedures` | procedures 순서 ≠ name 순서, = rationale 화살표 순서. 배열 순서 의미 미정의 | 순서 의미 확정은 후속 |
| I-PC-12 | F | `/combos/4/packages/1/riskBenefit` | 「8개 소규모 연구」「2026 기준」「트라넥사민산(TXA)」 출처 없음 | 외부 보충 금지 — literature-evidence 등과 비교 단계 |
| I-PC-13 | F | `/combos/5/packages/1/riskBenefit` | 「문헌상 … 약 20~30% 감소」 출처 없음 | 같음 |
| I-PC-14 | P | `/combos/5/packages/0/procedures` | 스킨보톡스(희석)가 M1 로만 표현 | 시술 변형의 코드 구분 여부는 후속 |
| I-PC-07 | I | `/combos/2/packages/0` | products 「더블로골드」 vs clinicalRationale 「더블로」 | 동일 대상 여부 미확정 |
| I-PC-10 | I | `/combos/4/packages/*/priceRange` | `/회` 접미가 P5·P9 묶음에만 | I-PC-01 과 함께 |
| I-PC-11 | I | `/combos/*/packages/*/productTier` | 「국산+수입 혼합」「수입+국산」「국산/수입」「혼합」 표면형 불일치 | 등급 값 통합은 후속 |
| I-PC-15 | I | `/combos/7/packages/1/procedures` | 텍스트엔 HIFU 또는 RF(올리지오), procedures 엔 M9 만 | M9 범위 확인은 후속(F) |
| I-PC-16 | I | `/combos/*/packages/*/products/*` | 대안 표기 `or`·`/`·`또는` 혼용 | 기호만으로 의미 확정하지 않음 |

## 고친 A (에이전트 추출 오류)

1. 보조 정규식 「정도·빈도 부사」가 `더` 로 `더블로골드` 를, `약` 으로 `약하지만` 을 잡던 오탐 → 앞 경계·뒤 공백 조건을 넣어 재생성(build.py PATTERNS).
2. 알려진 오분절 기록이 품사 오분석(`리쥬란`→리쥬/NNP 이/VCP 란/ETM, `안내`→안/MAG 내/VV 등)과 명사 조각 분리를 구분하지 않던 것 → `issue` 칸을 「품사 오분석」/「복합 표현 분리」로 나누고 영향 문구 추가.

## 알려진 분석 한계 (K)

- kiwipiepy 0.24.1 `cong` 기본 사전, 사용자 사전 없음. 전문어 목록(build.py TERMS)에 든 표면형만 출현별로 K 기록 — 목록 밖 오분절은 빠졌을 수 있다.
- 품사 오분석 7종 20출현: `리쥬란`(12) · `니들RF`(니/NP 들/XSN 분해 2) · `안내`(부정 부사 오탐) · `하안면`(하/VV) · `심부`(심/XR) · `이중`(이/MM) · `PDRN이`(조사 이→MM).
- `안내` 의 `안/MAG` 는 부정 탐색 시 오탐이 됨(`/combos/7/packages/0/riskBenefit`). `modifier_tokens` 에 그대로 남아 있으므로 부정 집계에 쓰면 안 된다.
- 형태소 `form` 은 분석기 정규화형(예: 해요 → 하/어요)이라 `surface` 와 다를 수 있다. 기본형은 도구 반환값 그대로이며 도메인 표준명이 아니다.
- 보조 정규식 한계: 「부정」 패턴의 `안 ` 이 `동안 조합`(`/combos/0/packages/1/salesPitch` [17,26))·`세안 제한`(`/combos/3/packages/1/riskBenefit` [33,39))을 부정 후보로 잡음(오탐, expressions.json 에 regex 로 남김). 「순서 기호 연쇄」 패턴은 괄호 안 공백에서 끊겨 부분 구간을 냄 — 전체 연쇄는 수동 표현으로 보완. 정규식 결과는 전수 의미 해석이 아니다.
- 「드물게」「깊은」「얕게」「약간의」 등은 원문 그대로 보존했고 수치로 바꾸지 않았다.

## 후속 의미 조사로 남김 (1차에서 미검토)

- 필드 역할(상담 문구 salesPitch·upsellHook vs 의료진 참고 clinicalRationale·riskBenefit) 분류 — `/description` 자기서술 근거.
- `→` 의 쓰임 두 가지(시술 순서 vs 기전 인과), 괄호의 쓰임 여러 가지 — 구획 관찰에 위치별로 기록.
- problem 값 「쁘띠시술」(시술군)과 다른 problem(고민)의 성격 차이, problem 값 안 `/`.
- upsellHook 안 시술(HIFU·실리프팅·니들RF·스컬트라 등)은 패키지 구성원이 아님 — 관계 확정하지 않음.
