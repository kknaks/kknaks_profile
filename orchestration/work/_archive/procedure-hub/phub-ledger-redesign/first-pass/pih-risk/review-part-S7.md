# S7 — procedures 21–22 · M13 플라즈마

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/22/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/21` | [21] | object | (object, 자식 9) | 6893–7156 |  |
| `/procedures/21/category` | category | string | "M13" | 6905–6910 |  |
| `/procedures/21/subcategory` | subcategory | string | "플라즈마" | 6925–6931 |  |
| `/procedures/21/name` | name | string | "플라즈마 (콜드플라즈마)" | 6939–6954 | E0260 |
| `/procedures/21/procedure_ref` | procedure_ref | string | "M13" | 6971–6976 |  |
| `/procedures/21/pih_risk` | pih_risk | string | "low" | 6988–6993 |  |
| `/procedures/21/pih_rate` | pih_rate | string | "2-5%" | 7005–7011 | E0261 |
| `/procedures/21/fitzpatrick_note` | fitzpatrick_note | string | "저온 플라즈마로 열손상 최소화. 표피 미세손상 부위에서 PIH 가능" | 7031–7070 | E0262, E0263 |
| `/procedures/21/risk_factors` | risk_factors | array | (array, 자식 3) | 7086–7117 |  |
| `/procedures/21/risk_factors/0` | [0] | string | "높은 에너지" | 7087–7095 | E0264 |
| `/procedures/21/risk_factors/1` | [1] | string | "과도한 조사 시간" | 7096–7107 | E0265 |
| `/procedures/21/risk_factors/2` | [2] | string | "어두운 피부" | 7108–7116 | E0266 |
| `/procedures/21/prevention` | prevention | string | "적정 에너지, SPF 50+ 자외선 차단" | 7131–7155 | E0267, E0268 |
| `/procedures/22` | [22] | object | (object, 자식 9) | 7157–7436 |  |
| `/procedures/22/category` | category | string | "M13" | 7169–7174 |  |
| `/procedures/22/subcategory` | subcategory | string | "플라즈마" | 7189–7195 |  |
| `/procedures/22/name` | name | string | "플라즈마 (열플라즈마/플렉서)" | 7203–7221 | E0269 |
| `/procedures/22/procedure_ref` | procedure_ref | string | "M13" | 7238–7243 |  |
| `/procedures/22/pih_risk` | pih_risk | string | "moderate" | 7255–7265 |  |
| `/procedures/22/pih_rate` | pih_rate | string | "5-15%" | 7277–7284 | E0270 |
| `/procedures/22/fitzpatrick_note` | fitzpatrick_note | string | "고온 플라즈마는 표피에 점상 열손상을 유발하여 PIH 위험 증가" | 7304–7341 | E0271 |
| `/procedures/22/risk_factors` | risk_factors | array | (array, 자식 3) | 7357–7388 |  |
| `/procedures/22/risk_factors/0` | [0] | string | "높은 에너지" | 7358–7366 | E0272 |
| `/procedures/22/risk_factors/1` | [1] | string | "조밀한 점상 조사" | 7367–7378 | E0273 |
| `/procedures/22/risk_factors/2` | [2] | string | "어두운 피부" | 7379–7387 | E0274 |
| `/procedures/22/prevention` | prevention | string | "적정 에너지·밀도, SPF 50+ 자외선 차단 4주 이상" | 7402–7435 | E0275, E0276 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | P | `/procedures/21/procedure_ref`, `/procedures/22/procedure_ref`, `/procedures/21/name`, `/procedures/22/name` | 21·22 번 모두 procedure_ref 'M13'(카테고리 수준)이고 name 은 '플라즈마 (콜드플라즈마)' / '플라즈마 (열플라즈마/플렉서)' 로 괄호에서만 갈린다. pih_risk 도 low/moderate 로 다르다(P1). |
| 2 | P | `/procedures/21/fitzpatrick_note` | '표피 미세손상 부위에서 PIH 가능' 의 '부위' 는 해부학적 시술 부위가 아니라 손상이 생긴 자리를 가리킨다. 부위 역할 구분 시 이 출현을 해부 부위로 합치지 않는다. |
| 3 | P | `/procedures/21/fitzpatrick_note`, `/procedures/22/fitzpatrick_note` | 21번 '저온 플라즈마로 열손상 최소화' ↔ 22번 '고온 플라즈마는 표피에 점상 열손상을 유발하여 PIH 위험 증가' — 같은 계열 두 행이 온도로 대조된다. |
| 4 | P | `/procedures/22/name` | '열플라즈마/플렉서' — '/' 로 방식명과 장비명(으로 보이는 것)이 묶임. 정체 확정은 후속. |
| 5 | B | `/procedures/22/prevention` | 'SPF 50+ 자외선 차단 4주 이상' 기준 시점 없음(B3). |
| 6 | P | `/procedures/21/risk_factors/1`, `/procedures/22/risk_factors/1` | '과도한 조사 시간'(시간 길이) · '조밀한 점상 조사'(밀도) — 조사(照射)의 서로 다른 속성이 위험요인. 수치 없음. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0260 | `/procedures/21/name` | 플라즈마 (콜드플라즈마) | 0–13 | name_candidate | P |  |
| E0261 | `/procedures/21/pih_rate` | 2-5% | 0–4 | range, rate | P |  |
| E0262 | `/procedures/21/fitzpatrick_note` | 저온 플라즈마로 열손상 최소화 | 0–16 | cause_reason, device_param, effect_change | P |  |
| E0263 | `/procedures/21/fitzpatrick_note` | 표피 미세손상 부위에서 PIH 가능 | 18–37 | condition, possibility, tissue_layer | P | '부위' = 손상 자리 |
| E0264 | `/procedures/21/risk_factors/0` | 높은 에너지 | 0–6 | risk_factor_phrase, degree | B |  |
| E0265 | `/procedures/21/risk_factors/1` | 과도한 조사 시간 | 0–9 | risk_factor_phrase, time, degree | B |  |
| E0266 | `/procedures/21/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0267 | `/procedures/21/prevention` | 적정 에너지 | 0–6 | recommendation | B |  |
| E0268 | `/procedures/21/prevention` | SPF 50+ 자외선 차단 | 8–22 | recommendation | P |  |
| E0269 | `/procedures/22/name` | 플라즈마 (열플라즈마/플렉서) | 0–16 | name_candidate, symbol_ambiguity | F |  |
| E0270 | `/procedures/22/pih_rate` | 5-15% | 0–5 | range, rate | P |  |
| E0271 | `/procedures/22/fitzpatrick_note` | 고온 플라즈마는 표피에 점상 열손상을 유발하여 PIH 위험 증가 | 0–35 | cause_reason, tissue_layer, effect_change, device_param | P |  |
| E0272 | `/procedures/22/risk_factors/0` | 높은 에너지 | 0–6 | risk_factor_phrase, degree | B |  |
| E0273 | `/procedures/22/risk_factors/1` | 조밀한 점상 조사 | 0–9 | risk_factor_phrase, device_param, degree | B |  |
| E0274 | `/procedures/22/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0275 | `/procedures/22/prevention` | 적정 에너지·밀도 | 0–9 | recommendation, device_param | B |  |
| E0276 | `/procedures/22/prevention` | SPF 50+ 자외선 차단 4주 이상 | 11–31 | recommendation, time, comparison | B | 기준 시점 없음 |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/21/risk_factors/1` | 조사 [4,6) | 조사/NNG | 동형이의어(照射) 구분 없음 | K |
| `/procedures/22/risk_factors/1` | 조사 [7,9) | 조사/NNG | 동형이의어(照射) | K |

## 5. 미결 (이 구획)

- B-S7-1 '4주 이상' 기준 시점 (issues.md B3)
- P-S7-1 procedure_ref 카테고리 수준 다중 행 (issues.md P1)
