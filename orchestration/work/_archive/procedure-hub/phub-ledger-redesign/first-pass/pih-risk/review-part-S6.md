# S6 — procedures 18–20 · M11 니들RF·M12 MTS

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/20/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/18` | [18] | object | (object, 자식 9) | 5999–6304 |  |
| `/procedures/18/category` | category | string | "M11" | 6011–6016 |  |
| `/procedures/18/subcategory` | subcategory | string | "니들RF" | 6031–6037 | E0228 |
| `/procedures/18/name` | name | string | "니들RF - 절연침 (포텐자, 시크릿RF 등)" | 6045–6072 | E0229, E0230 |
| `/procedures/18/procedure_ref` | procedure_ref | string | "M11-1" | 6089–6096 |  |
| `/procedures/18/pih_risk` | pih_risk | string | "very_low" | 6108–6118 |  |
| `/procedures/18/pih_rate` | pih_rate | string | "< 1%" | 6130–6136 | E0231 |
| `/procedures/18/fitzpatrick_note` | fitzpatrick_note | string | "절연침이 표피를 우회하여 진피에 직접 RF 전달, PIH 거의 없음. 어두운 피부에도 안전" | 6156–6208 | E0232, E0233, E0234 |
| `/procedures/18/risk_factors` | risk_factors | array | (array, 자식 2) | 6224–6255 |  |
| `/procedures/18/risk_factors/0` | [0] | string | "비절연 니들 사용 시 표피 손상" | 6225–6244 | E0235 |
| `/procedures/18/risk_factors/1` | [1] | string | "과도한 에너지" | 6245–6254 | E0236 |
| `/procedures/18/prevention` | prevention | string | "절연침(insulated needle) 사용, 적정 에너지" | 6269–6303 | E0237, E0238 |
| `/procedures/19` | [19] | object | (object, 자식 9) | 6305–6579 |  |
| `/procedures/19/category` | category | string | "M11" | 6317–6322 |  |
| `/procedures/19/subcategory` | subcategory | string | "니들RF" | 6337–6343 | E0239 |
| `/procedures/19/name` | name | string | "니들RF - 비절연침" | 6351–6364 | E0240 |
| `/procedures/19/procedure_ref` | procedure_ref | string | "M11-1" | 6381–6388 |  |
| `/procedures/19/pih_risk` | pih_risk | string | "low" | 6400–6405 |  |
| `/procedures/19/pih_rate` | pih_rate | string | "2-5%" | 6417–6423 | E0241 |
| `/procedures/19/fitzpatrick_note` | fitzpatrick_note | string | "비절연침은 표피에도 RF 전달되어 절연침 대비 PIH 위험 약간 높음" | 6443–6483 | E0242, E0243 |
| `/procedures/19/risk_factors` | risk_factors | array | (array, 자식 3) | 6499–6527 |  |
| `/procedures/19/risk_factors/0` | [0] | string | "표피 열손상" | 6500–6508 | E0244 |
| `/procedures/19/risk_factors/1` | [1] | string | "어두운 피부" | 6509–6517 | E0245 |
| `/procedures/19/risk_factors/2` | [2] | string | "높은 에너지" | 6518–6526 | E0246 |
| `/procedures/19/prevention` | prevention | string | "Fitzpatrick III-IV에서 절연침 우선, 에너지 조절" | 6541–6578 | E0247, E0248 |
| `/procedures/20` | [20] | object | (object, 자식 9) | 6580–6892 |  |
| `/procedures/20/category` | category | string | "M12" | 6592–6597 |  |
| `/procedures/20/subcategory` | subcategory | string | "MTS" | 6612–6617 |  |
| `/procedures/20/name` | name | string | "마이크로니들링 (MTS, 더마롤러/더마펜)" | 6625–6650 | E0249, E0250 |
| `/procedures/20/procedure_ref` | procedure_ref | string | "M12" | 6667–6672 |  |
| `/procedures/20/pih_risk` | pih_risk | string | "low" | 6684–6689 |  |
| `/procedures/20/pih_rate` | pih_rate | string | "1-5%" | 6701–6707 | E0251 |
| `/procedures/20/fitzpatrick_note` | fitzpatrick_note | string | "열에너지 없이 물리적 미세손상만 유발하므로 PIH 낮음. 깊은 침 깊이 시 약간 증가" | 6727–6776 | E0252, E0253 |
| `/procedures/20/risk_factors` | risk_factors | array | (array, 자식 3) | 6792–6838 |  |
| `/procedures/20/risk_factors/0` | [0] | string | "깊은 니들 깊이(1.5mm+)" | 6793–6811 | E0254 |
| `/procedures/20/risk_factors/1` | [1] | string | "불충분한 자외선 차단" | 6812–6825 | E0255 |
| `/procedures/20/risk_factors/2` | [2] | string | "과도한 시술 빈도" | 6826–6837 | E0256 |
| `/procedures/20/prevention` | prevention | string | "적정 니들 깊이, SPF 50+ 자외선 차단, 시술 간격 4주 이상" | 6852–6891 | E0257, E0258, E0259 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | P | `/procedures/18/procedure_ref`, `/procedures/19/procedure_ref`, `/procedures/18/name`, `/procedures/19/name` | 18·19 번이 같은 procedure_ref 'M11-1' 을 갖고 name 은 '니들RF - 절연침 …' / '니들RF - 비절연침' 으로 바늘 종류만 다르다. ' - ' 는 상위명과 변형을 가르는 구분 기호로 쓰였다(이 원장에서 이 두 행만). |
| 2 | P | `/procedures/18/risk_factors/0`, `/procedures/19/name` | 18번(절연침) 의 risk_factors '비절연 니들 사용 시 표피 손상' 은 19번 행의 변형을 쓰는 상황을 위험요인으로 든다. 행 간 참조로 보이나 연결 확정은 후속(F3). |
| 3 | F | `/procedures/19/fitzpatrick_note`, `/procedures/19/prevention` | 19번 '절연침 대비 PIH 위험 약간 높음', 'Fitzpatrick III-IV에서 절연침 우선' 은 18번을 비교 대상·대안으로 지칭하는 것으로 보인다(F3). |
| 4 | P | `/procedures/18/fitzpatrick_note` | 18번 note 두 문장: '… 진피에 직접 RF 전달, PIH 거의 없음' + '어두운 피부에도 안전'. 층위(표피 우회 → 진피)가 이유. |
| 5 | P | `/procedures/20/category`, `/procedures/20/procedure_ref` | 20번 MTS 는 category 'M12' 와 procedure_ref 'M12' 가 같다 — 참조 코드가 카테고리 수준에 머문다(P1). |
| 6 | P | `/procedures/20/name` | 20번 name '마이크로니들링 (MTS, 더마롤러/더마펜)' — 괄호 안 쉼표 앞은 약어, 뒤는 '/' 로 묶인 도구 두 개. |
| 7 | P | `/procedures/20/fitzpatrick_note`, `/procedures/20/risk_factors/0` | note '깊은 침 깊이 시 약간 증가' 의 '깊은' 기준은 같은 항목 risk_factors '깊은 니들 깊이(1.5mm+)' 에만 수치로 있다. 같은 대상에 '침' 과 '니들' 두 표기. |
| 8 | P | `/procedures/20/risk_factors/2` | '과도한 시술 빈도' 의 '빈도' 는 시술 반복 빈도다 — PIH 발생 빈도가 아니다. 빈도 표현을 대상 없이 합치지 않는다. |
| 9 | P | `/procedures/20/fitzpatrick_note` | '열에너지 없이 물리적 미세손상만 유발하므로 PIH 낮음' — 부정(없이)·한정(만)·이유(므로)가 한 절에 있다. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0228 | `/procedures/18/subcategory` | 니들RF | 0–4 | name_candidate, mixed_language | P |  |
| E0229 | `/procedures/18/name` | 니들RF - 절연침 | 0–10 | name_candidate, symbol_ambiguity | P | ' - ' 구분 |
| E0230 | `/procedures/18/name` | 포텐자, 시크릿RF 등 | 12–24 | name_candidate | F | 열린 예시 목록 |
| E0231 | `/procedures/18/pih_rate` | < 1% | 0–4 | comparison, rate | P |  |
| E0232 | `/procedures/18/fitzpatrick_note` | 절연침이 표피를 우회하여 진피에 직접 RF 전달 | 0–26 | cause_reason, tissue_layer, device_param | P |  |
| E0233 | `/procedures/18/fitzpatrick_note` | PIH 거의 없음 | 28–37 | negation, possibility, degree | P |  |
| E0234 | `/procedures/18/fitzpatrick_note` | 어두운 피부에도 안전 | 39–50 | population, degree | P |  |
| E0235 | `/procedures/18/risk_factors/0` | 비절연 니들 사용 시 표피 손상 | 0–17 | risk_factor_phrase, condition, negation, reference, tissue_layer | F | 19번 변형 지칭으로 보임 |
| E0236 | `/procedures/18/risk_factors/1` | 과도한 에너지 | 0–7 | risk_factor_phrase, degree | B |  |
| E0237 | `/procedures/18/prevention` | 절연침(insulated needle) 사용 | 0–24 | recommendation, device_param, mixed_language | P |  |
| E0238 | `/procedures/18/prevention` | 적정 에너지 | 26–32 | recommendation | B |  |
| E0239 | `/procedures/19/subcategory` | 니들RF | 0–4 | name_candidate | P |  |
| E0240 | `/procedures/19/name` | 니들RF - 비절연침 | 0–11 | name_candidate, negation, symbol_ambiguity | P |  |
| E0241 | `/procedures/19/pih_rate` | 2-5% | 0–4 | range, rate | P |  |
| E0242 | `/procedures/19/fitzpatrick_note` | 비절연침은 표피에도 RF 전달되어 | 0–18 | cause_reason, tissue_layer, negation | P |  |
| E0243 | `/procedures/19/fitzpatrick_note` | 절연침 대비 PIH 위험 약간 높음 | 19–38 | comparison, degree, reference | F |  |
| E0244 | `/procedures/19/risk_factors/0` | 표피 열손상 | 0–6 | risk_factor_phrase, tissue_layer | P |  |
| E0245 | `/procedures/19/risk_factors/1` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0246 | `/procedures/19/risk_factors/2` | 높은 에너지 | 0–6 | risk_factor_phrase, degree | B |  |
| E0247 | `/procedures/19/prevention` | Fitzpatrick III-IV에서 절연침 우선 | 0–27 | condition, population, recommendation, reference | F |  |
| E0248 | `/procedures/19/prevention` | 에너지 조절 | 29–35 | recommendation | B | 방향·수치 없음 |
| E0249 | `/procedures/20/name` | 마이크로니들링 | 0–7 | name_candidate | P |  |
| E0250 | `/procedures/20/name` | MTS, 더마롤러/더마펜 | 9–22 | name_candidate, symbol_ambiguity, mixed_language | F |  |
| E0251 | `/procedures/20/pih_rate` | 1-5% | 0–4 | range, rate | P |  |
| E0252 | `/procedures/20/fitzpatrick_note` | 열에너지 없이 물리적 미세손상만 유발하므로 PIH 낮음 | 0–30 | negation, cause_reason, degree | P |  |
| E0253 | `/procedures/20/fitzpatrick_note` | 깊은 침 깊이 시 약간 증가 | 32–47 | condition, degree, effect_change, device_param | P |  |
| E0254 | `/procedures/20/risk_factors/0` | 깊은 니들 깊이(1.5mm+) | 0–16 | risk_factor_phrase, device_param, quantity_unit, comparison | P | 1.5mm 대상 = 니들 깊이 |
| E0255 | `/procedures/20/risk_factors/1` | 불충분한 자외선 차단 | 0–11 | risk_factor_phrase, negation | P |  |
| E0256 | `/procedures/20/risk_factors/2` | 과도한 시술 빈도 | 0–9 | risk_factor_phrase, degree, time | P | 빈도 대상 = 시술 반복 |
| E0257 | `/procedures/20/prevention` | 적정 니들 깊이 | 0–8 | recommendation, device_param | B |  |
| E0258 | `/procedures/20/prevention` | SPF 50+ 자외선 차단 | 10–24 | recommendation | P |  |
| E0259 | `/procedures/20/prevention` | 시술 간격 4주 이상 | 26–37 | time, comparison, recommendation | P |  |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/20/name` | 더마롤러 [14,18) | 더/MAG 마/MAG 롤러/NNG | 도구명이 부사 두 개+명사로 분해(심각) | K |
| `/procedures/20/prevention` | 니들 깊이 [3,8) | 니/NP 들/XSN 깊이/MAG | '니들'(needle) 이 대명사+접미사, '깊이' 가 부사로 — 세팅 대상 소실(심각) | K |
| `/procedures/18/name` | 절연침 [7,10) | 절연침/NNG | 같은 말이 note 에선 절연/NNG 침/NNG, prevention 에선 절연침/NNP — 칸마다 분절·품사 다름 | K |

## 5. 미결 (이 구획)

- F-S6-1 18↔19 행 간 비교·대안·위험요인 참조 연결 (issues.md F3)
- P-S6-1 procedure_ref 카테고리 수준(M12) (issues.md P1)
