# S4 — procedures 12–14 · M8 제모

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/14/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/12` | [12] | object | (object, 자식 9) | 4238–4546 |  |
| `/procedures/12/category` | category | string | "M8" | 4250–4254 |  |
| `/procedures/12/subcategory` | subcategory | string | "제모" | 4269–4273 | E0167 |
| `/procedures/12/name` | name | string | "장파장 제모 (Nd:YAG 1064nm LP)" | 4281–4308 | E0168, E0169 |
| `/procedures/12/procedure_ref` | procedure_ref | string | "M8-5" | 4325–4331 |  |
| `/procedures/12/pih_risk` | pih_risk | string | "very_low" | 4343–4353 |  |
| `/procedures/12/pih_rate` | pih_rate | string | "~1%" | 4365–4370 | E0170 |
| `/procedures/12/fitzpatrick_note` | fitzpatrick_note | string | "긴 파장(1064nm) + 긴 펄스폭으로 표피 멜라닌 보호, 어두운 피부에도 가장 안전한 제모 레이저" | 4390–4448 | E0171, E0172 |
| `/procedures/12/risk_factors` | risk_factors | array | (array, 자식 2) | 4464–4488 |  |
| `/procedures/12/risk_factors/0` | [0] | string | "과도한 fluence" | 4465–4478 | E0173 |
| `/procedures/12/risk_factors/1` | [1] | string | "짧은 펄스폭" | 4479–4487 | E0174 |
| `/procedures/12/prevention` | prevention | string | "적정 fluence, 표피 냉각(DCD/contact cooling) 사용" | 4502–4545 | E0175, E0176 |
| `/procedures/13` | [13] | object | (object, 자식 9) | 4547–4872 |  |
| `/procedures/13/category` | category | string | "M8" | 4559–4563 |  |
| `/procedures/13/subcategory` | subcategory | string | "제모" | 4578–4582 | E0177 |
| `/procedures/13/name` | name | string | "알렉산드라이트 제모 (755nm LP)" | 4590–4613 | E0178, E0179 |
| `/procedures/13/procedure_ref` | procedure_ref | string | "M8-5-3" | 4630–4638 |  |
| `/procedures/13/pih_risk` | pih_risk | string | "low" | 4650–4655 |  |
| `/procedures/13/pih_rate` | pih_rate | string | "2-5%" | 4667–4673 | E0180 |
| `/procedures/13/fitzpatrick_note` | fitzpatrick_note | string | "755nm은 멜라닌 흡수가 높아 Fitzpatrick I-III에 최적. IV에서는 1064nm 권장" | 4693–4751 | E0181, E0182 |
| `/procedures/13/risk_factors` | risk_factors | array | (array, 자식 3) | 4767–4805 |  |
| `/procedures/13/risk_factors/0` | [0] | string | "어두운 피부(IV+)" | 4768–4781 | E0183 |
| `/procedures/13/risk_factors/1` | [1] | string | "높은 fluence" | 4782–4794 | E0184 |
| `/procedures/13/risk_factors/2` | [2] | string | "불충분한 냉각" | 4795–4804 | E0185 |
| `/procedures/13/prevention` | prevention | string | "Fitzpatrick IV 이상은 1064nm Nd:YAG 우선, 적절한 냉각 시스템 사용" | 4819–4871 | E0186, E0187 |
| `/procedures/14` | [14] | object | (object, 자식 9) | 4873–5161 |  |
| `/procedures/14/category` | category | string | "M8" | 4885–4889 |  |
| `/procedures/14/subcategory` | subcategory | string | "제모" | 4904–4908 | E0188 |
| `/procedures/14/name` | name | string | "다이오드 제모 (800-810nm LP)" | 4916–4940 | E0189, E0190 |
| `/procedures/14/procedure_ref` | procedure_ref | string | "M8-5" | 4957–4963 |  |
| `/procedures/14/pih_risk` | pih_risk | string | "low" | 4975–4980 |  |
| `/procedures/14/pih_rate` | pih_rate | string | "1-3%" | 4992–4998 | E0191 |
| `/procedures/14/fitzpatrick_note` | fitzpatrick_note | string | "중간 파장으로 III-IV에서 비교적 안전. 1064nm 대비 약간 높은 PIH" | 5018–5064 | E0192, E0193 |
| `/procedures/14/risk_factors` | risk_factors | array | (array, 자식 2) | 5080–5103 |  |
| `/procedures/14/risk_factors/0` | [0] | string | "높은 fluence" | 5081–5093 | E0194 |
| `/procedures/14/risk_factors/1` | [1] | string | "어두운 피부" | 5094–5102 | E0195 |
| `/procedures/14/prevention` | prevention | string | "적정 fluence, 표피 냉각 사용, Fitzpatrick IV에서 주의" | 5117–5160 | E0196, E0197, E0198 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | I | `/procedures/12/pih_risk`, `/procedures/12/pih_rate`, `/risk_levels/very_low`, `/risk_levels/low` | 12번 장파장 제모: pih_risk 'very_low'(risk_levels '< 1%') 인데 pih_rate '~1%' — 근사 1% 는 '< 1%' 경계에 걸치고 low '1-5%' 의 하한과 같다. 원문 내 경계 불일치로 기록. |
| 2 | P | `/procedures/12/procedure_ref`, `/procedures/13/procedure_ref`, `/procedures/14/procedure_ref` | 제모 세 행의 procedure_ref 가 'M8-5', 'M8-5-3', 'M8-5' — 12·14 번은 하위 번호 없는 상위 코드를 공유하고 13번만 3단 코드. 참조 깊이가 행마다 다르다(P1·F1). |
| 3 | P | `/procedures/12/fitzpatrick_note` | '긴 파장(1064nm) + 긴 펄스폭으로 표피 멜라닌 보호' — '+' 는 두 이유의 결합. '어두운 피부에도 가장 안전한 제모 레이저' 는 제모 레이저 범위 최상급 진술. |
| 4 | P | `/procedures/13/fitzpatrick_note` | 13번 '755nm은 멜라닌 흡수가 높아 Fitzpatrick I-III에 최적. IV에서는 1064nm 권장' — 원장 기준 집단(III-IV, description)과 다른 범위 I-III 를 최적 대상으로 든다. 13번 pih_rate '2-5%' 가 어느 피부형 기준인지 원문만으로 불명(B1 과 같은 원인). |
| 5 | P | `/procedures/13/risk_factors/0` | '어두운 피부(IV+)' — 이 원장에서 '어두운 피부' 에 피부형 기준을 괄호로 준 유일한 출현. 다른 행의 '어두운 피부' 에 이 기준을 옮겨 적용하지 않는다. |
| 6 | F | `/procedures/13/prevention`, `/procedures/14/fitzpatrick_note` | 13번 '1064nm Nd:YAG 우선', 14번 '1064nm 대비 약간 높은 PIH' 는 다른 행(12번 장파장 제모 Nd:YAG 1064nm LP 로 보임)을 파장으로 지칭한다. 연결은 후속(F3). |
| 7 | P | `/procedures/14/prevention` | 'Fitzpatrick IV에서 주의' — 무엇을 어떻게 주의하는지 없는 일반 주의. |
| 8 | P | `/procedures/12/prevention` | '표피 냉각(DCD/contact cooling)' — 괄호 안 '/' 로 두 냉각 방식. 13번 '적절한 냉각 시스템', 14번 '표피 냉각 사용' 과 표현이 다르다. |
| 9 | P | `/procedures/14/fitzpatrick_note` | '중간 파장으로 III-IV에서 비교적 안전' — '중간' 은 상대 표현(무엇들 사이인지 원문에 없음). |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0167 | `/procedures/12/subcategory` | 제모 | 0–2 | claim_scope | P | 하위분류명이 목적 |
| E0168 | `/procedures/12/name` | 장파장 제모 | 0–6 | name_candidate, degree | P | '장파장' 상대 표현 |
| E0169 | `/procedures/12/name` | Nd:YAG 1064nm LP | 8–24 | device_param, mixed_language | P |  |
| E0170 | `/procedures/12/pih_rate` | ~1% | 0–3 | approx, rate | I | very_low 와 경계 — I2 |
| E0171 | `/procedures/12/fitzpatrick_note` | 긴 파장(1064nm) + 긴 펄스폭으로 표피 멜라닌 보호 | 0–32 | cause_reason, device_param, symbol_ambiguity, tissue_layer | P | '+' = 이유 결합 |
| E0172 | `/procedures/12/fitzpatrick_note` | 어두운 피부에도 가장 안전한 제모 레이저 | 34–56 | population, degree, comparison, claim_scope | P | 최상급 |
| E0173 | `/procedures/12/risk_factors/0` | 과도한 fluence | 0–11 | risk_factor_phrase, device_param | B |  |
| E0174 | `/procedures/12/risk_factors/1` | 짧은 펄스폭 | 0–6 | risk_factor_phrase, device_param | B |  |
| E0175 | `/procedures/12/prevention` | 적정 fluence | 0–10 | recommendation, device_param | B |  |
| E0176 | `/procedures/12/prevention` | 표피 냉각(DCD/contact cooling) 사용 | 12–41 | recommendation, tissue_layer, symbol_ambiguity, mixed_language | P |  |
| E0177 | `/procedures/13/subcategory` | 제모 | 0–2 | claim_scope | P |  |
| E0178 | `/procedures/13/name` | 알렉산드라이트 제모 | 0–10 | name_candidate | P |  |
| E0179 | `/procedures/13/name` | 755nm LP | 12–20 | device_param | P |  |
| E0180 | `/procedures/13/pih_rate` | 2-5% | 0–4 | range, rate | P |  |
| E0181 | `/procedures/13/fitzpatrick_note` | 755nm은 멜라닌 흡수가 높아 Fitzpatrick I-III에 최적 | 0–39 | cause_reason, population, range, degree | P | 기준 집단과 다른 범위 |
| E0182 | `/procedures/13/fitzpatrick_note` | IV에서는 1064nm 권장 | 41–56 | condition, population, recommendation, reference | F |  |
| E0183 | `/procedures/13/risk_factors/0` | 어두운 피부(IV+) | 0–11 | risk_factor_phrase, population, comparison, symbol_ambiguity | P | '어두운' 의 유일한 기준 표기 |
| E0184 | `/procedures/13/risk_factors/1` | 높은 fluence | 0–10 | risk_factor_phrase, device_param | B |  |
| E0185 | `/procedures/13/risk_factors/2` | 불충분한 냉각 | 0–7 | risk_factor_phrase, negation | P |  |
| E0186 | `/procedures/13/prevention` | Fitzpatrick IV 이상은 1064nm Nd:YAG 우선 | 0–35 | condition, population, comparison, recommendation, reference | F |  |
| E0187 | `/procedures/13/prevention` | 적절한 냉각 시스템 사용 | 37–50 | recommendation | P |  |
| E0188 | `/procedures/14/subcategory` | 제모 | 0–2 | claim_scope | P |  |
| E0189 | `/procedures/14/name` | 다이오드 제모 | 0–7 | name_candidate | P |  |
| E0190 | `/procedures/14/name` | 800-810nm LP | 9–21 | device_param, range | P |  |
| E0191 | `/procedures/14/pih_rate` | 1-3% | 0–4 | range, rate | P |  |
| E0192 | `/procedures/14/fitzpatrick_note` | 중간 파장으로 III-IV에서 비교적 안전 | 0–23 | cause_reason, population, degree | P |  |
| E0193 | `/procedures/14/fitzpatrick_note` | 1064nm 대비 약간 높은 PIH | 25–44 | comparison, degree, reference | F |  |
| E0194 | `/procedures/14/risk_factors/0` | 높은 fluence | 0–10 | risk_factor_phrase, device_param | B |  |
| E0195 | `/procedures/14/risk_factors/1` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0196 | `/procedures/14/prevention` | 적정 fluence | 0–10 | recommendation | B |  |
| E0197 | `/procedures/14/prevention` | 표피 냉각 사용 | 12–20 | recommendation, tissue_layer | P |  |
| E0198 | `/procedures/14/prevention` | Fitzpatrick IV에서 주의 | 22–41 | condition, population, recommendation | B | 주의 내용 없음 |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/14/fitzpatrick_note` | 비교적 [17,20) | 비교/NNG 적/XSN | 다른 칸(0번)에선 비교적/MAG — 정도 부사가 명사+접미사로 | K |
| `/procedures/13/risk_factors/0` | IV+ [7,10) | IV/SL +/SW | '+'(이상) 기호 분리 — 비교 의미 형태소에 없음 | K |
| `/procedures/12/pih_rate` | ~ [0,1) | ~/SO | 근사 '~' | K |
| `/procedures/14/name` | 800-810 [9,16) | 800-810/W_SERIAL | 범위가 일련번호 한 토큰 | K |

## 5. 미결 (이 구획)

- I-S4-1 12번 very_low ↔ ~1% 경계 (issues.md I2)
- F-S4-1 1064nm 지칭 행 연결 (issues.md F3)
- P-S4-1 procedure_ref 깊이 혼재 M8-5 / M8-5-3 (issues.md P1)
