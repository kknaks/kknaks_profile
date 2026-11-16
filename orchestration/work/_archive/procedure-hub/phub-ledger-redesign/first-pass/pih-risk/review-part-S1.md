# S1 — procedures 0–3 · M8 색소/토닝

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/3/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/0` | [0] | object | (object, 자식 9) | 506–823 |  |
| `/procedures/0/category` | category | string | "M8" | 518–522 |  |
| `/procedures/0/subcategory` | subcategory | string | "색소/토닝" | 537–544 | E0028 |
| `/procedures/0/name` | name | string | "레이저 토닝 (QS Nd:YAG 1064nm 저에너지)" | 552–584 | E0029, E0030, E0031, E0032 |
| `/procedures/0/procedure_ref` | procedure_ref | string | "M8-1-1" | 601–609 |  |
| `/procedures/0/pih_risk` | pih_risk | string | "low" | 621–626 |  |
| `/procedures/0/pih_rate` | pih_rate | string | "~5%" | 638–643 | E0033 |
| `/procedures/0/fitzpatrick_note` | fitzpatrick_note | string | "III-IV에서도 비교적 안전. 저에너지 반복 조사로 멜라닌 점진적 제거" | 663–705 | E0034, E0035, E0036, E0037 |
| `/procedures/0/risk_factors` | risk_factors | array | (array, 자식 3) | 721–768 |  |
| `/procedures/0/risk_factors/0` | [0] | string | "과도한 fluence" | 722–735 | E0038 |
| `/procedures/0/risk_factors/1` | [1] | string | "짧은 시술 간격(2주 미만)" | 736–753 | E0039, E0040 |
| `/procedures/0/risk_factors/2` | [2] | string | "불충분한 자외선 차단" | 754–767 | E0041 |
| `/procedures/0/prevention` | prevention | string | "시술 간격 2-4주 유지, SPF 50+ 자외선 차단, 저에너지 유지" | 782–822 | E0042, E0043, E0044 |
| `/procedures/1` | [1] | object | (object, 자식 9) | 824–1144 |  |
| `/procedures/1/category` | category | string | "M8" | 836–840 |  |
| `/procedures/1/subcategory` | subcategory | string | "색소/토닝" | 855–862 | E0045 |
| `/procedures/1/name` | name | string | "QS Nd:YAG 1064nm (표준 에너지, 색소 치료)" | 870–904 | E0046, E0047 |
| `/procedures/1/procedure_ref` | procedure_ref | string | "M8-1-1" | 921–929 |  |
| `/procedures/1/pih_risk` | pih_risk | string | "moderate" | 941–951 |  |
| `/procedures/1/pih_rate` | pih_rate | string | "~10%" | 963–969 | E0048 |
| `/procedures/1/fitzpatrick_note` | fitzpatrick_note | string | "III-IV에서 표준 에너지 사용 시 PIH 위험 증가" | 989–1021 | E0049, E0050 |
| `/procedures/1/risk_factors` | risk_factors | array | (array, 자식 4) | 1037–1082 |  |
| `/procedures/1/risk_factors/0` | [0] | string | "높은 fluence" | 1038–1050 | E0051 |
| `/procedures/1/risk_factors/1` | [1] | string | "반복 조사" | 1051–1058 | E0052 |
| `/procedures/1/risk_factors/2` | [2] | string | "어두운 피부" | 1059–1067 | E0053 |
| `/procedures/1/risk_factors/3` | [3] | string | "불충분한 자외선 차단" | 1068–1081 | E0054 |
| `/procedures/1/prevention` | prevention | string | "테스트 샷 시행, 적정 fluence 설정, SPF 50+ 자외선 차단 4주 이상" | 1096–1143 | E0055, E0056, E0057, E0058 |
| `/procedures/2` | [2] | object | (object, 자식 9) | 1145–1404 |  |
| `/procedures/2/category` | category | string | "M8" | 1157–1161 |  |
| `/procedures/2/subcategory` | subcategory | string | "색소/토닝" | 1176–1183 | E0059 |
| `/procedures/2/name` | name | string | "피코토닝 (피코초 Nd:YAG 1064nm)" | 1191–1217 | E0060, E0061 |
| `/procedures/2/procedure_ref` | procedure_ref | string | "M8-1-2" | 1234–1242 |  |
| `/procedures/2/pih_risk` | pih_risk | string | "low" | 1254–1259 |  |
| `/procedures/2/pih_rate` | pih_rate | string | "1-3%" | 1271–1277 | E0062 |
| `/procedures/2/fitzpatrick_note` | fitzpatrick_note | string | "피코초 펄스로 열손상 최소화, QS 대비 PIH 낮음" | 1297–1328 | E0063, E0064 |
| `/procedures/2/risk_factors` | risk_factors | array | (array, 자식 2) | 1344–1366 |  |
| `/procedures/2/risk_factors/0` | [0] | string | "과도한 에너지" | 1345–1354 | E0065 |
| `/procedures/2/risk_factors/1` | [1] | string | "짧은 간격 반복" | 1355–1365 | E0066 |
| `/procedures/2/prevention` | prevention | string | "적정 에너지 유지, 시술 간격 2-4주" | 1380–1403 | E0067, E0068 |
| `/procedures/3` | [3] | object | (object, 자식 9) | 1405–1726 |  |
| `/procedures/3/category` | category | string | "M8" | 1417–1421 |  |
| `/procedures/3/subcategory` | subcategory | string | "색소/토닝" | 1436–1443 | E0069 |
| `/procedures/3/name` | name | string | "피코슈어 (755nm 피코초)" | 1451–1469 | E0070, E0071 |
| `/procedures/3/procedure_ref` | procedure_ref | string | "M8-1-3" | 1486–1494 |  |
| `/procedures/3/pih_risk` | pih_risk | string | "low" | 1506–1511 |  |
| `/procedures/3/pih_rate` | pih_rate | string | "2-5%" | 1523–1529 | E0072 |
| `/procedures/3/fitzpatrick_note` | fitzpatrick_note | string | "피코초 펄스로 열확산 최소화. 755nm은 멜라닌 흡수도가 높아 1064nm 대비 약간 높은 PIH" | 1549–1606 | E0073, E0074, E0075 |
| `/procedures/3/risk_factors` | risk_factors | array | (array, 자식 3) | 1622–1661 |  |
| `/procedures/3/risk_factors/0` | [0] | string | "과도한 에너지" | 1623–1632 | E0076 |
| `/procedures/3/risk_factors/1` | [1] | string | "755nm 파장의 멜라닌 흡수" | 1633–1651 | E0077 |
| `/procedures/3/risk_factors/2` | [2] | string | "어두운 피부" | 1652–1660 | E0078 |
| `/procedures/3/prevention` | prevention | string | "Fitzpatrick IV 이상에서는 1064nm 우선 고려, 적정 fluence 사용" | 1675–1725 | E0079, E0080 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | P | `/procedures/0/procedure_ref`, `/procedures/1/procedure_ref` | 0·1 두 행이 같은 procedure_ref 'M8-1-1' 을 갖고 name 의 에너지 세팅(괄호 '저에너지' vs '표준 에너지, 색소 치료')만 다르며 pih_risk 도 low/moderate 로 다르다. 이 원장의 행 단위는 '참조 코드' 가 아니라 '시술+세팅' 이다. |
| 2 | P | `/procedures/0/name`, `/procedures/1/name`, `/procedures/2/name`, `/procedures/3/name` | name 괄호 안에 장비 계열(QS·피코초)·매질(Nd:YAG)·파장(1064nm·755nm)·에너지 세팅·목적('색소 치료')이 섞여 있다. 괄호 안 쉼표는 1번에서 세팅과 목적을 나눈다. |
| 3 | P | `/procedures/0/fitzpatrick_note` | fitzpatrick_note 에 피부형 관련 진술('III-IV에서도 비교적 안전')과 기전 진술('저에너지 반복 조사로 멜라닌 점진적 제거')이 마침표로 이어져 한 칸에 있다. |
| 4 | B | `/procedures/1/prevention` | 'SPF 50+ 자외선 차단 4주 이상' 의 기준 시점(시술 후부터인지 등)이 없다. |
| 5 | B | `/procedures/0/risk_factors/0`, `/procedures/1/risk_factors/0`, `/procedures/1/prevention`, `/procedures/2/prevention`, `/procedures/3/prevention` | '과도한'·'높은' fluence/에너지와 '적정' fluence/에너지에 수치 기준이 없다. 원문만으로 경계를 정할 수 없다. |
| 6 | P | `/procedures/0/risk_factors/1`, `/procedures/0/prevention`, `/procedures/2/prevention` | 간격 진술: risk_factors '짧은 시술 간격(2주 미만)' 과 prevention '시술 간격 2-4주 유지' 가 같은 항목 안에서 짝을 이룬다. 2번은 '시술 간격 2-4주' 에 '유지' 동사 없이 끝난다. |
| 7 | F | `/procedures/2/fitzpatrick_note` | 'QS 대비 PIH 낮음' 의 비교 대상 QS 는 0번(저에너지)·1번(표준 에너지) 중 어느 행인지 원문에 없다. 비교 관계 연결은 후속. |
| 8 | F | `/procedures/3/fitzpatrick_note`, `/procedures/3/prevention` | 3번은 '1064nm 대비 약간 높은 PIH' 와 'Fitzpatrick IV 이상에서는 1064nm 우선 고려' 로 다른 파장(다른 행일 수 있음)을 대안으로 가리킨다. 어떤 행/시술을 지칭하는지 연결은 후속. |
| 9 | P | `/procedures/3/prevention` | 'Fitzpatrick IV 이상' 은 description 의 기준 집단 III-IV 를 넘어 V·VI 를 포함할 수 있는 조건이다. 원문 그대로 조건 범위를 보존. |
| 10 | P | `/procedures/1/risk_factors/2`, `/procedures/3/risk_factors/2` | '어두운 피부' 는 상대 표현이다. 기준 집단(III-IV) 안에서 무엇과 비교해 어두운지 원문에 없다(B1 계열과 함께 후속). |
| 11 | P | `/procedures/0/pih_rate`, `/procedures/1/pih_rate` | pih_rate '~5%'(low) · '~10%'(moderate) · '1-3%'(low) · '2-5%'(low). 0번 '~5%' 는 low 구간 '1-5%' 상한과 맞닿는다(경계 문제 B2). 구획 내 pih_risk↔risk_levels 범위 불일치는 없다. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0028 | `/procedures/0/subcategory` | 색소/토닝 | 0–5 | symbol_ambiguity | F | 하위분류명 안 '/' |
| E0029 | `/procedures/0/name` | 레이저 토닝 | 0–6 | name_candidate | P |  |
| E0030 | `/procedures/0/name` | QS Nd:YAG 1064nm 저에너지 | 8–29 | device_param, mixed_language | P | 괄호 안 장비·파장·세팅 |
| E0031 | `/procedures/0/name` | 1064nm | 18–24 | device_param, quantity_unit | P |  |
| E0032 | `/procedures/0/name` | 저에너지 | 25–29 | device_param, degree | B | 세팅 수식(수치 없음) |
| E0033 | `/procedures/0/pih_rate` | ~5% | 0–3 | approx, rate | P |  |
| E0034 | `/procedures/0/fitzpatrick_note` | III-IV에서도 비교적 안전 | 0–16 | population, condition, degree | P | '도' — 기준 집단에서도 |
| E0035 | `/procedures/0/fitzpatrick_note` | 비교적 안전 | 10–16 | degree | P | 비교 기준 불명 |
| E0036 | `/procedures/0/fitzpatrick_note` | 저에너지 반복 조사로 멜라닌 점진적 제거 | 18–40 | cause_reason, device_param | P | 기전 진술. '조사'=照射 |
| E0037 | `/procedures/0/fitzpatrick_note` | 점진적 | 34–37 | degree, time | P | 변화 속도 수식(멜라닌 제거) |
| E0038 | `/procedures/0/risk_factors/0` | 과도한 fluence | 0–11 | risk_factor_phrase, device_param, degree, mixed_language | B | 수치 기준 없음 |
| E0039 | `/procedures/0/risk_factors/1` | 짧은 시술 간격(2주 미만) | 0–15 | risk_factor_phrase, time, comparison | P | 괄호가 '짧은' 의 기준을 준다 |
| E0040 | `/procedures/0/risk_factors/1` | 2주 미만 | 9–14 | time, comparison, quantity_unit | P |  |
| E0041 | `/procedures/0/risk_factors/2` | 불충분한 자외선 차단 | 0–11 | risk_factor_phrase, negation, degree | P | 불- 접두 부정 |
| E0042 | `/procedures/0/prevention` | 시술 간격 2-4주 유지 | 0–13 | time, range, recommendation | P |  |
| E0043 | `/procedures/0/prevention` | SPF 50+ 자외선 차단 | 15–29 | recommendation, comparison, symbol_ambiguity | P | '+' = 이상(문맥상). 기간 없음 |
| E0044 | `/procedures/0/prevention` | 저에너지 유지 | 31–38 | recommendation, device_param | P |  |
| E0045 | `/procedures/1/subcategory` | 색소/토닝 | 0–5 | symbol_ambiguity | F |  |
| E0046 | `/procedures/1/name` | QS Nd:YAG 1064nm | 0–16 | name_candidate, device_param, mixed_language | P | 장비명이 곧 행 이름 |
| E0047 | `/procedures/1/name` | 표준 에너지, 색소 치료 | 18–31 | device_param, condition | P | 세팅+목적 병기 |
| E0048 | `/procedures/1/pih_rate` | ~10% | 0–4 | approx, rate | P |  |
| E0049 | `/procedures/1/fitzpatrick_note` | III-IV에서 표준 에너지 사용 시 PIH 위험 증가 | 0–30 | population, condition, effect_change | P | 증가의 기준(무엇 대비) 생략 |
| E0050 | `/procedures/1/fitzpatrick_note` | 표준 에너지 사용 시 | 9–20 | condition, device_param | P |  |
| E0051 | `/procedures/1/risk_factors/0` | 높은 fluence | 0–10 | risk_factor_phrase, device_param, degree | B |  |
| E0052 | `/procedures/1/risk_factors/1` | 반복 조사 | 0–5 | risk_factor_phrase | P | 반복 횟수 기준 없음 |
| E0053 | `/procedures/1/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population, degree | P | 상대 표현 |
| E0054 | `/procedures/1/risk_factors/3` | 불충분한 자외선 차단 | 0–11 | risk_factor_phrase, negation | P |  |
| E0055 | `/procedures/1/prevention` | 테스트 샷 시행 | 0–8 | recommendation | P |  |
| E0056 | `/procedures/1/prevention` | 적정 fluence 설정 | 10–23 | recommendation, device_param | B | 수치 없음 |
| E0057 | `/procedures/1/prevention` | SPF 50+ 자외선 차단 4주 이상 | 25–45 | recommendation, time, comparison, symbol_ambiguity | B | 기준 시점 없음 |
| E0058 | `/procedures/1/prevention` | 4주 이상 | 40–45 | time, comparison | B |  |
| E0059 | `/procedures/2/subcategory` | 색소/토닝 | 0–5 | symbol_ambiguity | F |  |
| E0060 | `/procedures/2/name` | 피코토닝 | 0–4 | name_candidate | P |  |
| E0061 | `/procedures/2/name` | 피코초 Nd:YAG 1064nm | 6–23 | device_param, mixed_language | P |  |
| E0062 | `/procedures/2/pih_rate` | 1-3% | 0–4 | range, rate | P |  |
| E0063 | `/procedures/2/fitzpatrick_note` | 피코초 펄스로 열손상 최소화 | 0–15 | cause_reason, device_param, effect_change | P |  |
| E0064 | `/procedures/2/fitzpatrick_note` | QS 대비 PIH 낮음 | 17–29 | comparison, reference | F | 비교 대상 행 불명 — F3 |
| E0065 | `/procedures/2/risk_factors/0` | 과도한 에너지 | 0–7 | risk_factor_phrase, degree | B |  |
| E0066 | `/procedures/2/risk_factors/1` | 짧은 간격 반복 | 0–8 | risk_factor_phrase, time, degree | B | '짧은' 의 기준이 이 항목엔 없음 |
| E0067 | `/procedures/2/prevention` | 적정 에너지 유지 | 0–9 | recommendation, device_param | B |  |
| E0068 | `/procedures/2/prevention` | 시술 간격 2-4주 | 11–21 | time, range, recommendation | P |  |
| E0069 | `/procedures/3/subcategory` | 색소/토닝 | 0–5 | symbol_ambiguity | F |  |
| E0070 | `/procedures/3/name` | 피코슈어 | 0–4 | name_candidate | P |  |
| E0071 | `/procedures/3/name` | 755nm 피코초 | 6–15 | device_param | P |  |
| E0072 | `/procedures/3/pih_rate` | 2-5% | 0–4 | range, rate | P |  |
| E0073 | `/procedures/3/fitzpatrick_note` | 피코초 펄스로 열확산 최소화 | 0–15 | cause_reason, effect_change, device_param | P |  |
| E0074 | `/procedures/3/fitzpatrick_note` | 755nm은 멜라닌 흡수도가 높아 1064nm 대비 약간 높은 PIH | 17–55 | cause_reason, comparison, degree | F |  |
| E0075 | `/procedures/3/fitzpatrick_note` | 약간 높은 PIH | 46–55 | degree, comparison | P | 수치 없음 |
| E0076 | `/procedures/3/risk_factors/0` | 과도한 에너지 | 0–7 | risk_factor_phrase, degree | B |  |
| E0077 | `/procedures/3/risk_factors/1` | 755nm 파장의 멜라닌 흡수 | 0–16 | risk_factor_phrase, device_param | P | 세팅이 아니라 파장 고유 성질을 위험요인으로 둠 |
| E0078 | `/procedures/3/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0079 | `/procedures/3/prevention` | Fitzpatrick IV 이상에서는 1064nm 우선 고려 | 0–33 | condition, population, recommendation, comparison, reference | F | 다른 파장(행)을 대안으로 지칭 — F3 |
| E0080 | `/procedures/3/prevention` | 적정 fluence 사용 | 35–48 | recommendation, device_param | B |  |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/2/fitzpatrick_note` | 피코초 [0,3) | 피코/NNP 초/XPN | '피코초'(시간 단위)가 고유명사+접두사로 쪼개짐. name 칸의 같은 말은 피코초/NNG 로 한 덩어리 — 칸마다 결과가 다름 | K |
| `/procedures/3/fitzpatrick_note` | 피코초 [0,3) | 피코/NNP 초/XPN | 위와 같음 | K |
| `/procedures/0/pih_rate` | ~ [0,1) | ~/SO | 근사 '~' 가 범위 붙임표와 같은 SO 태그 — 근사/범위 구분이 형태소 층에서 사라짐 | K |
| `/procedures/0/prevention` | 50+ [19,22) | 50/SN +/SW | '+' (이상) 가 기호 SW 로 분리 — 비교 의미는 형태소에 없음. name 의 결합 '+' 와 태그 동일 | K |
| `/procedures/1/risk_factors/1` | 조사 [3,5) | 조사/NNG | 동형이의어(照射/調査) 구분 없음. 문맥상 照射 | K |
| `/procedures/0/name` | 저에너지 [25,29) | 저에너지/NNP | 같은 말이 fitzpatrick_note 에선 저/XPN 에너지/NNG — 칸마다 분절 다름 | K |

## 5. 미결 (이 구획)

- B-S1-1 '4주 이상' 기준 시점 없음 (issues.md B3)
- B-S1-2 과도한/높은/적정 수치 기준 없음 (issues.md B4)
- F-S1-1 'QS 대비'·'1064nm 대비'·'1064nm 우선 고려' 의 지칭 행 연결 (issues.md F3)
- P-S1-1 같은 procedure_ref 다중 행(세팅 단위 행) (issues.md P1)
