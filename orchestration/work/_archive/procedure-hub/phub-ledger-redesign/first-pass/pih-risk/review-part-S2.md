# S2 — procedures 4–8 · M8 프락셔널

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/8/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/4` | [4] | object | (object, 자식 9) | 1727–2139 |  |
| `/procedures/4/category` | category | string | "M8" | 1739–1743 |  |
| `/procedures/4/subcategory` | subcategory | string | "프락셔널" | 1758–1764 |  |
| `/procedures/4/name` | name | string | "CO2 프락셔널 (10600nm, 박리성)" | 1772–1797 | E0081, E0082 |
| `/procedures/4/procedure_ref` | procedure_ref | string | "M8-2-1" | 1814–1822 |  |
| `/procedures/4/pih_risk` | pih_risk | string | "very_high" | 1834–1845 |  |
| `/procedures/4/pih_rate` | pih_rate | string | "~50%" | 1857–1863 | E0083 |
| `/procedures/4/fitzpatrick_note` | fitzpatrick_note | string | "III-IV에서 매우 높은 PIH 위험. 박리성 레이저 중 가장 높은 PIH 발생률" | 1883–1931 | E0084, E0085 |
| `/procedures/4/risk_factors` | risk_factors | array | (array, 자식 5) | 1947–2031 |  |
| `/procedures/4/risk_factors/0` | [0] | string | "깊은 ablation depth" | 1948–1967 | E0086 |
| `/procedures/4/risk_factors/1` | [1] | string | "높은 density/coverage" | 1968–1989 | E0087 |
| `/procedures/4/risk_factors/2` | [2] | string | "불충분한 자외선 차단" | 1990–2003 | E0088 |
| `/procedures/4/risk_factors/3` | [3] | string | "어두운 피부" | 2004–2012 | E0089 |
| `/procedures/4/risk_factors/4` | [4] | string | "시술 후 부적절한 상처 관리" | 2013–2030 | E0090 |
| `/procedures/4/prevention` | prevention | string | "Fitzpatrick III-IV에서는 가급적 비박리성 대안 고려. 사용 시 낮은 에너지·밀도, SPF 50+ 3개월 이상, 필요 시 hydroquinone 전처치" | 2045–2138 | E0091, E0092, E0093, E0094, E0095, E0096 |
| `/procedures/5` | [5] | object | (object, 자식 9) | 2140–2450 |  |
| `/procedures/5/category` | category | string | "M8" | 2152–2156 |  |
| `/procedures/5/subcategory` | subcategory | string | "프락셔널" | 2171–2177 |  |
| `/procedures/5/name` | name | string | "어븀야그(Er:YAG) 프락셔널 (2940nm, 박리성)" | 2185–2218 | E0097, E0098 |
| `/procedures/5/procedure_ref` | procedure_ref | string | "M8-2-3" | 2235–2243 |  |
| `/procedures/5/pih_risk` | pih_risk | string | "high" | 2255–2261 |  |
| `/procedures/5/pih_rate` | pih_rate | string | "10-20%" | 2273–2281 | E0099 |
| `/procedures/5/fitzpatrick_note` | fitzpatrick_note | string | "CO2 대비 열손상 적으나 박리성이라 PIH 위험 여전히 높음" | 2301–2337 | E0100, E0101 |
| `/procedures/5/risk_factors` | risk_factors | array | (array, 자식 3) | 2353–2391 |  |
| `/procedures/5/risk_factors/0` | [0] | string | "높은 에너지" | 2354–2362 | E0102 |
| `/procedures/5/risk_factors/1` | [1] | string | "깊은 ablation" | 2363–2376 | E0103 |
| `/procedures/5/risk_factors/2` | [2] | string | "불충분한 자외선 차단" | 2377–2390 | E0104 |
| `/procedures/5/prevention` | prevention | string | "적정 에너지 사용, SPF 50+ 자외선 차단 2개월 이상, 필요 시 전처치" | 2405–2449 | E0105, E0106, E0107 |
| `/procedures/6` | [6] | object | (object, 자식 9) | 2451–2792 |  |
| `/procedures/6/category` | category | string | "M8" | 2463–2467 |  |
| `/procedures/6/subcategory` | subcategory | string | "프락셔널" | 2482–2488 |  |
| `/procedures/6/name` | name | string | "프락셀듀얼 (1550+1927nm, 비박리~얕은 박리)" | 2496–2528 | E0108, E0109, E0110 |
| `/procedures/6/procedure_ref` | procedure_ref | string | "M8-2-4" | 2545–2553 |  |
| `/procedures/6/pih_risk` | pih_risk | string | "moderate" | 2565–2575 |  |
| `/procedures/6/pih_rate` | pih_rate | string | "5-15%" | 2587–2594 | E0111 |
| `/procedures/6/fitzpatrick_note` | fitzpatrick_note | string | "1550nm 비박리 + 1927nm 얕은 박리 복합. 1927nm 사용 비율에 따라 PIH 변동" | 2614–2669 | E0112, E0113 |
| `/procedures/6/risk_factors` | risk_factors | array | (array, 자식 3) | 2685–2725 |  |
| `/procedures/6/risk_factors/0` | [0] | string | "1927nm 고에너지 사용" | 2686–2702 | E0114 |
| `/procedures/6/risk_factors/1` | [1] | string | "높은 density" | 2703–2715 | E0115 |
| `/procedures/6/risk_factors/2` | [2] | string | "어두운 피부" | 2716–2724 | E0116 |
| `/procedures/6/prevention` | prevention | string | "Fitzpatrick III-IV에서 1927nm 비율 낮추기, SPF 50+ 자외선 차단" | 2739–2791 | E0117, E0118 |
| `/procedures/7` | [7] | object | (object, 자식 9) | 2793–3039 |  |
| `/procedures/7/category` | category | string | "M8" | 2805–2809 |  |
| `/procedures/7/subcategory` | subcategory | string | "프락셔널" | 2824–2830 |  |
| `/procedures/7/name` | name | string | "피코프락셀 (비박리성 피코초)" | 2838–2856 | E0119, E0120 |
| `/procedures/7/procedure_ref` | procedure_ref | string | "M8-2-5" | 2873–2881 |  |
| `/procedures/7/pih_risk` | pih_risk | string | "low" | 2893–2898 |  |
| `/procedures/7/pih_rate` | pih_rate | string | "1-3%" | 2910–2916 | E0121 |
| `/procedures/7/fitzpatrick_note` | fitzpatrick_note | string | "비박리성 + 피코초 펄스로 PIH 위험 낮음" | 2936–2962 | E0122 |
| `/procedures/7/risk_factors` | risk_factors | array | (array, 자식 2) | 2978–3000 |  |
| `/procedures/7/risk_factors/0` | [0] | string | "과도한 에너지" | 2979–2988 | E0123 |
| `/procedures/7/risk_factors/1` | [1] | string | "짧은 간격 반복" | 2989–2999 | E0124 |
| `/procedures/7/prevention` | prevention | string | "적정 에너지 유지, 시술 간격 4주 이상" | 3014–3038 | E0125, E0126 |
| `/procedures/8` | [8] | object | (object, 자식 9) | 3040–3288 |  |
| `/procedures/8/category` | category | string | "M8" | 3052–3056 |  |
| `/procedures/8/subcategory` | subcategory | string | "프락셔널" | 3071–3077 |  |
| `/procedures/8/name` | name | string | "피코슈어 프락셀 (755nm 비박리성)" | 3085–3108 | E0127, E0128 |
| `/procedures/8/procedure_ref` | procedure_ref | string | "M8-2-6" | 3125–3133 |  |
| `/procedures/8/pih_risk` | pih_risk | string | "low" | 3145–3150 |  |
| `/procedures/8/pih_rate` | pih_rate | string | "1-3%" | 3162–3168 | E0129 |
| `/procedures/8/fitzpatrick_note` | fitzpatrick_note | string | "FOCUS 렌즈 어레이로 비박리성 치료, PIH 낮음" | 3188–3219 | E0130, E0131 |
| `/procedures/8/risk_factors` | risk_factors | array | (array, 자식 1) | 3235–3246 |  |
| `/procedures/8/risk_factors/0` | [0] | string | "과도한 에너지" | 3236–3245 | E0132 |
| `/procedures/8/prevention` | prevention | string | "적정 에너지 유지, SPF 50+ 자외선 차단" | 3260–3287 | E0133, E0134 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | I | `/procedures/5/pih_risk`, `/procedures/5/pih_rate`, `/risk_levels/high`, `/risk_levels/moderate` | 5번 어븀야그: pih_risk 'high'(risk_levels '15-30%') 인데 pih_rate 는 '10-20%' — 하한 10 이 high 구간 밖이고 moderate '5-15%' 와 겹친다. 원문 내 불일치로 기록(어느 쪽이 맞는지 판단 안 함). |
| 2 | P | `/procedures/4/pih_risk`, `/procedures/4/pih_rate` | 4번 CO2: 'very_high' / '~50%' 는 '> 30%' 와 맞는다. 이 원장 최고값. |
| 3 | P | `/procedures/4/fitzpatrick_note` | '박리성 레이저 중 가장 높은 PIH 발생률' — 비교 범위가 '박리성 레이저' 로 제한된 최상급 진술. 이 원장 안 박리성 행은 4·5번(6번은 '얕은 박리' 일부). |
| 4 | F | `/procedures/4/prevention` | 'Fitzpatrick III-IV에서는 가급적 비박리성 대안 고려' — 대안 행(6·7·8번 등 '비박리' 표기 행)을 이름으로 지칭하지 않는다. 연결은 후속(F3). |
| 5 | P | `/procedures/4/prevention` | 4번 prevention 은 두 문장. 둘째 문장 '사용 시' 가 뒤 세 조치(낮은 에너지·밀도 / SPF 50+ 3개월 이상 / 필요 시 hydroquinone 전처치) 전부에 걸리는지, 첫 조치에만 걸리는지 원문 구두점만으로 단정 못 함 — 조건 범위 후속. |
| 6 | P | `/procedures/4/prevention` | 'SPF 50+ 3개월 이상' 은 '자외선 차단' 이 생략된 형태(다른 행은 'SPF 50+ 자외선 차단 …'). 생략된 행위어를 채우지 않고 원문 그대로 둔다. |
| 7 | B | `/procedures/4/prevention`, `/procedures/5/prevention` | '필요 시' 의 판단 기준이 없다. 5번 '필요 시 전처치' 는 전처치 약제·기간도 없다(4번은 hydroquinone 명시, 기간 없음). |
| 8 | P | `/procedures/6/name`, `/procedures/6/fitzpatrick_note` | 6번 '1550+1927nm' 의 '+' 는 한 장비의 두 파장 결합, '비박리~얕은 박리' 의 '~' 는 박리 정도의 범위로 읽힌다. 같은 원장에서 '+' 가 'SPF 50+'(이상)로도 쓰인다 — 기호 뜻이 문맥마다 다름(K/F). |
| 9 | P | `/procedures/6/fitzpatrick_note`, `/procedures/6/risk_factors/0`, `/procedures/6/prevention` | '1927nm 사용 비율에 따라 PIH 변동' 은 방향 없는 의존 진술이다. 방향은 같은 항목 prevention '1927nm 비율 낮추기' 와 risk_factors '1927nm 고에너지 사용' 으로만 간접적으로 드러난다. |
| 10 | P | `/procedures/4/risk_factors/1` | '높은 density/coverage' — '/' 로 두 영문 용어를 묶음. 동의어 병기인지 대안인지 불명. |
| 11 | P | `/procedures/4/risk_factors/4` | '시술 후 부적절한 상처 관리' 는 시술 뒤 시점의 관리 행위를 위험요인으로 둔 유일한 형태(이 구획). |
| 12 | P | `/procedures/4/procedure_ref`, `/procedures/5/procedure_ref` | procedure_ref 가 M8-2-1 다음 M8-2-3 — M8-2-2 는 이 원장에 없다(원장 안 사실만). |
| 13 | P | `/procedures/8/fitzpatrick_note` | 'FOCUS 렌즈 어레이' 는 장비 고유 기술명으로 보이는 대문자 영문. 이름 정체는 후속. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0081 | `/procedures/4/name` | CO2 프락셔널 | 0–8 | name_candidate | P |  |
| E0082 | `/procedures/4/name` | 10600nm, 박리성 | 10–22 | device_param, quantity_unit | P |  |
| E0083 | `/procedures/4/pih_rate` | ~50% | 0–4 | approx, rate | P |  |
| E0084 | `/procedures/4/fitzpatrick_note` | III-IV에서 매우 높은 PIH 위험 | 0–21 | population, condition, degree | P |  |
| E0085 | `/procedures/4/fitzpatrick_note` | 박리성 레이저 중 가장 높은 PIH 발생률 | 23–46 | comparison, degree, rate, claim_scope | P | 비교 범위 한정 최상급 |
| E0086 | `/procedures/4/risk_factors/0` | 깊은 ablation depth | 0–17 | risk_factor_phrase, device_param, degree, mixed_language | B | 깊이 수치 없음 |
| E0087 | `/procedures/4/risk_factors/1` | 높은 density/coverage | 0–19 | risk_factor_phrase, device_param, symbol_ambiguity, mixed_language | B |  |
| E0088 | `/procedures/4/risk_factors/2` | 불충분한 자외선 차단 | 0–11 | risk_factor_phrase, negation | P |  |
| E0089 | `/procedures/4/risk_factors/3` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0090 | `/procedures/4/risk_factors/4` | 시술 후 부적절한 상처 관리 | 0–15 | risk_factor_phrase, time, negation | P |  |
| E0091 | `/procedures/4/prevention` | Fitzpatrick III-IV에서는 가급적 비박리성 대안 고려 | 0–36 | condition, population, recommendation, negation, reference, degree | F | 대안 행 지칭 없음 |
| E0092 | `/procedures/4/prevention` | 가급적 | 22–25 | degree, recommendation | P | 권고 강도 |
| E0093 | `/procedures/4/prevention` | 사용 시 낮은 에너지·밀도, SPF 50+ 3개월 이상, 필요 시 hydroquinone 전처치 | 38–91 | condition, recommendation | F | '사용 시' 적용 범위 불명 — F4 |
| E0094 | `/procedures/4/prevention` | 낮은 에너지·밀도 | 43–52 | device_param, degree, recommendation | P | '·' 로 두 대상이 '낮은' 을 공유 |
| E0095 | `/procedures/4/prevention` | SPF 50+ 3개월 이상 | 54–68 | time, comparison, recommendation, symbol_ambiguity | B | '자외선 차단' 생략형 · 기준 시점 없음 |
| E0096 | `/procedures/4/prevention` | 필요 시 hydroquinone 전처치 | 70–91 | condition, time, recommendation, mixed_language | B | '필요 시' 기준·기간 없음 |
| E0097 | `/procedures/5/name` | 어븀야그(Er:YAG) 프락셔널 | 0–17 | name_candidate, mixed_language | P |  |
| E0098 | `/procedures/5/name` | 2940nm, 박리성 | 19–30 | device_param, quantity_unit | P |  |
| E0099 | `/procedures/5/pih_rate` | 10-20% | 0–6 | range, rate | I | pih_risk high 와 불일치 — I1 |
| E0100 | `/procedures/5/fitzpatrick_note` | CO2 대비 열손상 적으나 | 0–14 | comparison, reference | F | 4번 지칭으로 보임 — 연결 후속 |
| E0101 | `/procedures/5/fitzpatrick_note` | 박리성이라 PIH 위험 여전히 높음 | 15–34 | cause_reason, degree | P |  |
| E0102 | `/procedures/5/risk_factors/0` | 높은 에너지 | 0–6 | risk_factor_phrase, degree | B |  |
| E0103 | `/procedures/5/risk_factors/1` | 깊은 ablation | 0–11 | risk_factor_phrase, degree, mixed_language | B |  |
| E0104 | `/procedures/5/risk_factors/2` | 불충분한 자외선 차단 | 0–11 | risk_factor_phrase, negation | P |  |
| E0105 | `/procedures/5/prevention` | 적정 에너지 사용 | 0–9 | recommendation, device_param | B |  |
| E0106 | `/procedures/5/prevention` | SPF 50+ 자외선 차단 2개월 이상 | 11–32 | recommendation, time, comparison | B | 기준 시점 없음 |
| E0107 | `/procedures/5/prevention` | 필요 시 전처치 | 34–42 | condition, time, recommendation | B | 약제·기간·기준 없음 |
| E0108 | `/procedures/6/name` | 프락셀듀얼 | 0–5 | name_candidate | P |  |
| E0109 | `/procedures/6/name` | 1550+1927nm | 7–18 | device_param, symbol_ambiguity | P | '+' = 두 파장 결합 |
| E0110 | `/procedures/6/name` | 비박리~얕은 박리 | 20–29 | range, negation, degree, symbol_ambiguity | P | '~' = 범위 |
| E0111 | `/procedures/6/pih_rate` | 5-15% | 0–5 | range, rate | P |  |
| E0112 | `/procedures/6/fitzpatrick_note` | 1550nm 비박리 + 1927nm 얕은 박리 복합 | 0–28 | device_param, negation, degree, symbol_ambiguity | P |  |
| E0113 | `/procedures/6/fitzpatrick_note` | 1927nm 사용 비율에 따라 PIH 변동 | 30–53 | condition, effect_change | P | 방향 없음 |
| E0114 | `/procedures/6/risk_factors/0` | 1927nm 고에너지 사용 | 0–14 | risk_factor_phrase, device_param, degree | B |  |
| E0115 | `/procedures/6/risk_factors/1` | 높은 density | 0–10 | risk_factor_phrase, device_param, mixed_language | B |  |
| E0116 | `/procedures/6/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0117 | `/procedures/6/prevention` | Fitzpatrick III-IV에서 1927nm 비율 낮추기 | 0–34 | condition, population, recommendation, effect_change | P | 얼마나 낮출지 없음 |
| E0118 | `/procedures/6/prevention` | SPF 50+ 자외선 차단 | 36–50 | recommendation | P | 기간 없음 |
| E0119 | `/procedures/7/name` | 피코프락셀 | 0–5 | name_candidate | P |  |
| E0120 | `/procedures/7/name` | 비박리성 피코초 | 7–15 | device_param, negation | P |  |
| E0121 | `/procedures/7/pih_rate` | 1-3% | 0–4 | range, rate | P |  |
| E0122 | `/procedures/7/fitzpatrick_note` | 비박리성 + 피코초 펄스로 PIH 위험 낮음 | 0–24 | cause_reason, negation, symbol_ambiguity | P | '+' = 두 성질 결합(이유 나열) |
| E0123 | `/procedures/7/risk_factors/0` | 과도한 에너지 | 0–7 | risk_factor_phrase, degree | B |  |
| E0124 | `/procedures/7/risk_factors/1` | 짧은 간격 반복 | 0–8 | risk_factor_phrase, time | B |  |
| E0125 | `/procedures/7/prevention` | 적정 에너지 유지 | 0–9 | recommendation | B |  |
| E0126 | `/procedures/7/prevention` | 시술 간격 4주 이상 | 11–22 | time, comparison, recommendation | P |  |
| E0127 | `/procedures/8/name` | 피코슈어 프락셀 | 0–8 | name_candidate | P |  |
| E0128 | `/procedures/8/name` | 755nm 비박리성 | 10–20 | device_param, negation | P |  |
| E0129 | `/procedures/8/pih_rate` | 1-3% | 0–4 | range, rate | P |  |
| E0130 | `/procedures/8/fitzpatrick_note` | FOCUS 렌즈 어레이로 비박리성 치료 | 0–21 | cause_reason, name_candidate, mixed_language, negation | F |  |
| E0131 | `/procedures/8/fitzpatrick_note` | PIH 낮음 | 23–29 | degree | P |  |
| E0132 | `/procedures/8/risk_factors/0` | 과도한 에너지 | 0–7 | risk_factor_phrase, degree | B |  |
| E0133 | `/procedures/8/prevention` | 적정 에너지 유지 | 0–9 | recommendation | B |  |
| E0134 | `/procedures/8/prevention` | SPF 50+ 자외선 차단 | 11–25 | recommendation | P |  |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/4/name` | CO2 [0,3) | CO/SL 2/SN | 장비명 CO2 가 문자+숫자로 분리 | K |
| `/procedures/4/fitzpatrick_note` | 박리성 [23,26) | 박/NNP 리/NNG 성/XSN | 전문어 '박리(성)' 오분절 — 박리 정도 정보가 형태소 층에서 사라짐 | K |
| `/procedures/4/prevention` | 비박리성 [26,30) | 비/XPN 박/NNG 리/XSN 성/XSN | '비-' 부정 접두는 남지만 '박리' 가 쪼개짐 | K |
| `/procedures/5/fitzpatrick_note` | CO2 [0,3) | CO/SL 2/SN |  | K |
| `/procedures/5/fitzpatrick_note` | 박리성 [15,18) | 박/NNG 리/XSN 성/XSN | 박리 오분절 | K |
| `/procedures/6/name` | 비박리 [20,23) | 비/XPN 박/NNG 리/XSN | 박리 오분절 | K |
| `/procedures/6/name` | 박리 [27,29) | 박/NNG 리/XSN | '얕은 박리' 의 박리 오분절 | K |
| `/procedures/6/fitzpatrick_note` | 비박리 [7,10) | 비/XPN 박/NNG 리/XSN |  | K |
| `/procedures/6/fitzpatrick_note` | 박리 [23,25) | 박/NNG 리/XSN | '얕은 박리' | K |
| `/procedures/6/risk_factors/0` | 고에너지 [7,11) | (빈 구간)/이/VCP 고/EC 에너지/NNG | '고-'(높은) 가 서술격조사+연결어미로 분석되고 길이 0 토큰이 생김 — '높은 에너지' 의미 소실(심각) | K |
| `/procedures/7/fitzpatrick_note` | 비박리성 [0,4) | 비/XPN 박/NNG 리/XSN 성/XSN |  | K |
| `/procedures/8/name` | 비박리성 [16,20) | 비/XPN 박/NNG 리/XSN 성/XSN |  | K |
| `/procedures/8/fitzpatrick_note` | 비박리성 [14,18) | 비/XPN 박/NNG 리/XSN 성/NNG |  | K |
| `/procedures/4/prevention` | 전처치 [88,91) | 전/MM 처치/NNG | '전처치'(사전 처치)의 '전' 이 관형사(MM)로 — 시간적 '전' 의미가 형태소 품사와 어긋남 | K |
| `/procedures/5/prevention` | 전처치 [39,42) | 전/MM 처치/NNG | 위와 같음 | K |
| `/procedures/6/name` | ~ [23,24) | ~/SO | 범위 '~' — 근사 '~'(pih_rate)와 같은 태그 | K |

## 5. 미결 (이 구획)

- I-S2-1 5번 high ↔ 10-20% 불일치 (issues.md I1)
- B-S2-1 '필요 시' 기준·5번 전처치 약제/기간 없음 (issues.md B5)
- B-S2-2 '3개월 이상'·'2개월 이상' 기준 시점 없음 (issues.md B3)
- F-S2-1 '비박리성 대안'·'CO2 대비' 지칭 행 연결 (issues.md F3)
- F-S2-2 4번 '사용 시' 조건의 적용 범위 (issues.md F4)
