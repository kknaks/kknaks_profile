# S5 — procedures 15–17 · M9 HIFU·RF·복합 에너지

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/17/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/15` | [15] | object | (object, 자식 9) | 5162–5441 |  |
| `/procedures/15/category` | category | string | "M9" | 5174–5178 |  |
| `/procedures/15/subcategory` | subcategory | string | "HIFU" | 5193–5199 |  |
| `/procedures/15/name` | name | string | "HIFU (울쎄라, 슈링크 등)" | 5207–5226 | E0199, E0200 |
| `/procedures/15/procedure_ref` | procedure_ref | string | "M9-1" | 5243–5249 |  |
| `/procedures/15/pih_risk` | pih_risk | string | "very_low" | 5261–5271 |  |
| `/procedures/15/pih_rate` | pih_rate | string | "< 1%" | 5283–5289 | E0201 |
| `/procedures/15/fitzpatrick_note` | fitzpatrick_note | string | "초음파 에너지는 표피를 통과하여 심부에 작용하므로 PIH 거의 없음" | 5309–5348 | E0202, E0203 |
| `/procedures/15/risk_factors` | risk_factors | array | (array, 자식 1) | 5364–5399 |  |
| `/procedures/15/risk_factors/0` | [0] | string | "표피에 가까운 카트리지(1.5mm) 사용 시 드물게 가능" | 5365–5398 | E0204, E0205, E0206 |
| `/procedures/15/prevention` | prevention | string | "적절한 카트리지 깊이 선택, 표피 접촉면 관리" | 5413–5440 | E0207, E0208 |
| `/procedures/16` | [16] | object | (object, 자식 9) | 5442–5699 |  |
| `/procedures/16/category` | category | string | "M9" | 5454–5458 |  |
| `/procedures/16/subcategory` | subcategory | string | "RF" | 5473–5477 |  |
| `/procedures/16/name` | name | string | "써마지/올리지오 (모노폴라 RF)" | 5485–5505 | E0209, E0210 |
| `/procedures/16/procedure_ref` | procedure_ref | string | "M9-2" | 5522–5528 |  |
| `/procedures/16/pih_risk` | pih_risk | string | "very_low" | 5540–5550 |  |
| `/procedures/16/pih_rate` | pih_rate | string | "< 1%" | 5562–5568 | E0211 |
| `/procedures/16/fitzpatrick_note` | fitzpatrick_note | string | "RF는 멜라닌 비의존적이라 피부색 무관하게 안전" | 5588–5616 | E0212, E0213 |
| `/procedures/16/risk_factors` | risk_factors | array | (array, 자식 1) | 5632–5663 |  |
| `/procedures/16/risk_factors/0` | [0] | string | "과도한 에너지로 인한 표피 화상 시 이차적 PIH" | 5633–5662 | E0214, E0215 |
| `/procedures/16/prevention` | prevention | string | "적정 에너지 사용, 표피 냉각 유지" | 5677–5698 | E0216, E0217 |
| `/procedures/17` | [17] | object | (object, 자식 9) | 5700–5998 |  |
| `/procedures/17/category` | category | string | "M9" | 5712–5716 |  |
| `/procedures/17/subcategory` | subcategory | string | "복합 에너지" | 5731–5739 | E0218 |
| `/procedures/17/name` | name | string | "인모드 (바이폴라 RF + IPL/다이오드)" | 5747–5773 | E0219, E0220 |
| `/procedures/17/procedure_ref` | procedure_ref | string | "M9-2-5" | 5790–5798 |  |
| `/procedures/17/pih_risk` | pih_risk | string | "low" | 5810–5815 |  |
| `/procedures/17/pih_rate` | pih_rate | string | "1-5%" | 5827–5833 | E0221 |
| `/procedures/17/fitzpatrick_note` | fitzpatrick_note | string | "RF 자체는 안전하나, IPL/다이오드 복합 사용 시 PIH 가능" | 5853–5891 | E0222, E0223 |
| `/procedures/17/risk_factors` | risk_factors | array | (array, 자식 2) | 5907–5939 |  |
| `/procedures/17/risk_factors/0` | [0] | string | "광에너지(IPL/다이오드) 병합 시" | 5908–5929 | E0224 |
| `/procedures/17/risk_factors/1` | [1] | string | "어두운 피부" | 5930–5938 | E0225 |
| `/procedures/17/prevention` | prevention | string | "Fitzpatrick III-IV에서 광에너지 비율 낮추기, RF 위주 사용" | 5953–5997 | E0226, E0227 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | P | `/procedures/15/name`, `/procedures/18/name` | 15번 'HIFU (울쎄라, 슈링크 등)' 의 괄호는 쉼표 나열 + '등' 으로 열린 예시 목록이다. 나열된 이름이 행의 전부가 아님을 원문이 '등' 으로 밝힌다. |
| 2 | P | `/procedures/15/risk_factors/0` | 15번 유일한 risk_factors 는 명사구가 아니라 절이다: '표피에 가까운 카트리지(1.5mm) 사용 시 드물게 가능'. 조건(사용 시)·빈도(드물게)·가능성(가능)이 한 값 안에 있고 무엇이 가능한지(PIH)는 생략돼 있다. 생략 대상을 채우지 않는다. |
| 3 | P | `/procedures/15/risk_factors/0`, `/procedures/20/risk_factors/0` | '1.5mm' 가 15번(카트리지) 과 20번(니들 깊이, '1.5mm+') 에 나온다. 같은 수치·단위지만 대상이 다르다 — 하나로 합치지 않는다. |
| 4 | P | `/procedures/15/fitzpatrick_note`, `/procedures/15/pih_rate` | 'PIH 거의 없음' 과 pih_rate '< 1%' 가 함께 있다. '거의' 는 0 이 아님을 남긴다. |
| 5 | P | `/procedures/16/risk_factors/0` | 16번 '과도한 에너지로 인한 표피 화상 시 이차적 PIH' — 원인 사슬(과도한 에너지 → 표피 화상 → 이차적 PIH)이 한 값 안에 있다. 사슬 분해는 후속. |
| 6 | P | `/procedures/16/fitzpatrick_note` | 'RF는 멜라닌 비의존적이라 피부색 무관하게 안전' — 피부형 조건을 부정하는 진술(무관하게). 같은 항목 risk_factors 는 조건부 PIH 를 남긴다. |
| 7 | P | `/procedures/17/name`, `/procedures/17/subcategory`, `/procedures/17/procedure_ref` | 17번 인모드: subcategory '복합 에너지', name '(바이폴라 RF + IPL/다이오드)' — '+' 는 모달리티 결합, '/' 는 IPL 과 다이오드의 나열. procedure_ref 'M9-2-5' 는 16번 RF 'M9-2' 아래 코드 형태지만 subcategory 는 'RF' 가 아니다. |
| 8 | B | `/procedures/17/pih_risk`, `/procedures/17/pih_rate`, `/procedures/17/fitzpatrick_note` | 17번 'low'/'1-5%' 가 RF 단독 사용인지 광에너지 병합 사용인지 원문에 없다. note 는 'RF 자체는 안전하나 … 복합 사용 시 PIH 가능' 으로 조건에 따라 다르다고만 한다. |
| 9 | P | `/procedures/17/risk_factors/0` | '광에너지(IPL/다이오드) 병합 시' 는 위험요인 칸인데 조건절('~시')만 있고 결과 명사가 없다. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0199 | `/procedures/15/name` | HIFU (울쎄라, 슈링크 등) | 0–17 | name_candidate, mixed_language | F | 열린 예시 목록 |
| E0200 | `/procedures/15/name` | 울쎄라, 슈링크 등 | 6–16 | name_candidate | F | '등' |
| E0201 | `/procedures/15/pih_rate` | < 1% | 0–4 | comparison, rate | P |  |
| E0202 | `/procedures/15/fitzpatrick_note` | 초음파 에너지는 표피를 통과하여 심부에 작용하므로 | 0–27 | cause_reason, tissue_layer | P |  |
| E0203 | `/procedures/15/fitzpatrick_note` | PIH 거의 없음 | 28–37 | negation, possibility, degree | P | '거의' |
| E0204 | `/procedures/15/risk_factors/0` | 표피에 가까운 카트리지(1.5mm) 사용 시 드물게 가능 | 0–31 | risk_factor_phrase, condition, possibility, tissue_layer | P | 생략 대상(PIH) 채우지 않음 |
| E0205 | `/procedures/15/risk_factors/0` | 카트리지(1.5mm) | 8–19 | device_param, quantity_unit | P | 1.5mm 대상 = 카트리지 |
| E0206 | `/procedures/15/risk_factors/0` | 드물게 가능 | 25–31 | possibility | P | 빈도 부사+가능. 백분율로 바꾸지 않음 |
| E0207 | `/procedures/15/prevention` | 적절한 카트리지 깊이 선택 | 0–14 | recommendation, device_param | B | 수치 없음 |
| E0208 | `/procedures/15/prevention` | 표피 접촉면 관리 | 16–25 | recommendation, tissue_layer | P |  |
| E0209 | `/procedures/16/name` | 써마지/올리지오 | 0–8 | name_candidate, symbol_ambiguity | F |  |
| E0210 | `/procedures/16/name` | 모노폴라 RF | 10–17 | device_param, mixed_language | P |  |
| E0211 | `/procedures/16/pih_rate` | < 1% | 0–4 | comparison, rate | P |  |
| E0212 | `/procedures/16/fitzpatrick_note` | RF는 멜라닌 비의존적이라 피부색 무관하게 안전 | 0–26 | cause_reason, negation, population | P |  |
| E0213 | `/procedures/16/fitzpatrick_note` | 피부색 무관하게 | 15–23 | negation, population | P |  |
| E0214 | `/procedures/16/risk_factors/0` | 과도한 에너지로 인한 표피 화상 시 이차적 PIH | 0–27 | risk_factor_phrase, cause_reason, condition, tissue_layer | F | 원인 사슬 |
| E0215 | `/procedures/16/risk_factors/0` | 이차적 PIH | 20–27 | cause_reason | P |  |
| E0216 | `/procedures/16/prevention` | 적정 에너지 사용 | 0–9 | recommendation | B |  |
| E0217 | `/procedures/16/prevention` | 표피 냉각 유지 | 11–19 | recommendation, tissue_layer | P |  |
| E0218 | `/procedures/17/subcategory` | 복합 에너지 | 0–6 | device_param | P |  |
| E0219 | `/procedures/17/name` | 인모드 | 0–3 | name_candidate | P |  |
| E0220 | `/procedures/17/name` | 바이폴라 RF + IPL/다이오드 | 5–23 | device_param, symbol_ambiguity, mixed_language | F | '+' 결합 · '/' 나열 |
| E0221 | `/procedures/17/pih_rate` | 1-5% | 0–4 | range, rate | B | 사용 방식 기준 불명 — B6 |
| E0222 | `/procedures/17/fitzpatrick_note` | RF 자체는 안전하나 | 0–11 | degree | P |  |
| E0223 | `/procedures/17/fitzpatrick_note` | IPL/다이오드 복합 사용 시 PIH 가능 | 13–36 | condition, possibility, symbol_ambiguity | P |  |
| E0224 | `/procedures/17/risk_factors/0` | 광에너지(IPL/다이오드) 병합 시 | 0–19 | risk_factor_phrase, condition, symbol_ambiguity | P | 조건만 있는 위험요인 |
| E0225 | `/procedures/17/risk_factors/1` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0226 | `/procedures/17/prevention` | Fitzpatrick III-IV에서 광에너지 비율 낮추기 | 0–32 | condition, population, recommendation, effect_change | P |  |
| E0227 | `/procedures/17/prevention` | RF 위주 사용 | 34–42 | recommendation | P |  |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/15/fitzpatrick_note` | 초음파 [0,3) | 초/XPN 음파/NNG | '초음파' 가 접두사+명사로 분해 | K |
| `/procedures/15/fitzpatrick_note` | 심부 [18,20) | 심/XR 부/NNG | 층위어 '심부' 오분절 — 작용 층위 정보 소실 | K |
| `/procedures/15/prevention` | 깊이 [9,11) | 깊이/MAG | 명사 '깊이'(depth)가 부사(깊게)로 태깅 — 세팅 대상 명사 소실 | K |
| `/procedures/16/fitzpatrick_note` | 비의존적 [8,12) | 비/NNG 의존/NNG 적/XSN | 부정 접두 '비-' 가 명사(비=雨)로 — 부정 의미 소실(심각) | K |
| `/procedures/16/risk_factors/0` | 이차적 [20,23) | 이/NR 차/NNB 적/XSN | '이차적'(secondary) 이 수사+의존명사로 | K |

## 5. 미결 (이 구획)

- B-S5-1 17번 위험도가 어떤 사용 방식 기준인지 없음 (issues.md B6)
- F-S5-1 16번 원인 사슬·15번 생략 대상 분해 후속 (issues.md F5)
