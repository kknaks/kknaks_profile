# S3 — procedures 9–11 · M8 IPL·혈관

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/11/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/9` | [9] | object | (object, 자식 9) | 3289–3637 |  |
| `/procedures/9/category` | category | string | "M8" | 3301–3305 |  |
| `/procedures/9/subcategory` | subcategory | string | "IPL" | 3320–3325 |  |
| `/procedures/9/name` | name | string | "IPL (560-950nm 광대역)" | 3333–3354 | E0135, E0136 |
| `/procedures/9/procedure_ref` | procedure_ref | string | "M8-3-1" | 3371–3379 |  |
| `/procedures/9/pih_risk` | pih_risk | string | "moderate" | 3391–3401 |  |
| `/procedures/9/pih_rate` | pih_rate | string | "5-10%" | 3413–3420 | E0137 |
| `/procedures/9/fitzpatrick_note` | fitzpatrick_note | string | "광대역 파장이 멜라닌에 비선택적 흡수. III-IV에서 표피 멜라닌 경쟁 흡수로 PIH 위험" | 3440–3493 | E0138, E0139 |
| `/procedures/9/risk_factors` | risk_factors | array | (array, 자식 4) | 3509–3557 |  |
| `/procedures/9/risk_factors/0` | [0] | string | "높은 fluence" | 3510–3522 | E0140 |
| `/procedures/9/risk_factors/1` | [1] | string | "짧은 펄스폭" | 3523–3531 | E0141 |
| `/procedures/9/risk_factors/2` | [2] | string | "어두운 피부" | 3532–3540 | E0142 |
| `/procedures/9/risk_factors/3` | [3] | string | "적합하지 않은 필터 선택" | 3541–3556 | E0143 |
| `/procedures/9/prevention` | prevention | string | "Fitzpatrick IV에서 긴 파장 필터(590nm+) 사용, 적정 fluence, SPF 50+ 자외선 차단" | 3571–3636 | E0144, E0145, E0146, E0147 |
| `/procedures/10` | [10] | object | (object, 자식 9) | 3638–3930 |  |
| `/procedures/10/category` | category | string | "M8" | 3650–3654 |  |
| `/procedures/10/subcategory` | subcategory | string | "혈관" | 3669–3673 | E0148 |
| `/procedures/10/name` | name | string | "브이빔 (PDL 595nm)" | 3681–3698 | E0149, E0150 |
| `/procedures/10/procedure_ref` | procedure_ref | string | "M8-4-1" | 3715–3723 |  |
| `/procedures/10/pih_risk` | pih_risk | string | "low" | 3735–3740 |  |
| `/procedures/10/pih_rate` | pih_rate | string | "1-5%" | 3752–3758 | E0151 |
| `/procedures/10/fitzpatrick_note` | fitzpatrick_note | string | "혈관 타겟이라 멜라닌 경쟁 흡수 적음. 자반(purpura) 후 PIH 가능" | 3778–3822 | E0152, E0153 |
| `/procedures/10/risk_factors` | risk_factors | array | (array, 자식 2) | 3838–3874 |  |
| `/procedures/10/risk_factors/0` | [0] | string | "자반 유발 세팅(높은 에너지, 짧은 펄스)" | 3839–3864 | E0154 |
| `/procedures/10/risk_factors/1` | [1] | string | "어두운 피부" | 3865–3873 | E0155 |
| `/procedures/10/prevention` | prevention | string | "비자반성(subpurpuric) 세팅 우선, SPF 50+ 자외선 차단" | 3888–3929 | E0156, E0157 |
| `/procedures/11` | [11] | object | (object, 자식 9) | 3931–4237 |  |
| `/procedures/11/category` | category | string | "M8" | 3943–3947 |  |
| `/procedures/11/subcategory` | subcategory | string | "혈관" | 3962–3966 |  |
| `/procedures/11/name` | name | string | "엑셀브이/더마브이 (LP 532+1064nm)" | 3974–4001 | E0158, E0159 |
| `/procedures/11/procedure_ref` | procedure_ref | string | "M8-4-2" | 4018–4026 |  |
| `/procedures/11/pih_risk` | pih_risk | string | "low" | 4038–4043 |  |
| `/procedures/11/pih_rate` | pih_rate | string | "1-3%" | 4055–4061 | E0160 |
| `/procedures/11/fitzpatrick_note` | fitzpatrick_note | string | "1064nm은 멜라닌 흡수 낮아 안전. 532nm은 표재 혈관용이나 멜라닌 흡수 주의" | 4081–4130 | E0161, E0162 |
| `/procedures/11/risk_factors` | risk_factors | array | (array, 자식 2) | 4146–4180 |  |
| `/procedures/11/risk_factors/0` | [0] | string | "532nm 사용 시 어두운 피부" | 4147–4166 | E0163 |
| `/procedures/11/risk_factors/1` | [1] | string | "높은 fluence" | 4167–4179 | E0164 |
| `/procedures/11/prevention` | prevention | string | "Fitzpatrick IV에서 1064nm 위주 사용, 532nm 최소화" | 4194–4236 | E0165, E0166 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | P | `/procedures/9/subcategory`, `/procedures/9/name` | 9번은 subcategory 'IPL' 과 name 'IPL (560-950nm 광대역)' 이 같은 말로 시작한다. 하위분류명과 행 이름이 겹친다(원장 안 사실). |
| 2 | P | `/procedures/9/fitzpatrick_note` | 두 문장 중 둘째 'III-IV에서 표피 멜라닌 경쟁 흡수로 PIH 위험' 은 서술어·정도 수식 없이 '위험' 으로 끝난다. 정도(높음/낮음)를 채우지 않는다. |
| 3 | P | `/procedures/9/prevention` | 'Fitzpatrick IV에서 긴 파장 필터(590nm+) 사용' 의 조건은 IV 만 — III 은 이 조치의 조건에 없다. 괄호 '590nm+' 가 '긴' 의 기준을 준다('+'=이상으로 읽힘). |
| 4 | P | `/procedures/9/risk_factors/3` | '적합하지 않은 필터 선택' — 부정 서술(않은)이 위험요인 명사구 안에 있다. 무엇이 적합한지는 prevention 의 590nm+ 와 간접 연결. |
| 5 | P | `/procedures/10/fitzpatrick_note`, `/procedures/10/risk_factors/0`, `/procedures/10/prevention` | 10번 브이빔: '자반(purpura) 후 PIH 가능' 은 사건 선후(자반 → PIH)와 가능성 진술. risk_factors '자반 유발 세팅(높은 에너지, 짧은 펄스)' 는 괄호로 세팅을 풀고, prevention '비자반성(subpurpuric) 세팅 우선' 이 그 반대 세팅을 권한다. 세 칸이 한 사슬로 읽히지만 관계 확정은 후속. |
| 6 | P | `/procedures/10/fitzpatrick_note` | '혈관 타겟이라 멜라닌 경쟁 흡수 적음' — 이유(타겟) → 결과. '적음' 은 정도 수식(수치 없음). |
| 7 | P | `/procedures/11/name` | 11번 name '엑셀브이/더마브이 (LP 532+1064nm)' — '/' 로 두 장비명, '+' 로 두 파장. README 상 '/'=대안이나 기호만으로 확정 안 함. |
| 8 | P | `/procedures/11/risk_factors/0` | '532nm 사용 시 어두운 피부' — 조건(파장 사용)과 집단(어두운 피부)이 한 위험요인 안에 결합. 둘 중 하나만 떼면 뜻이 바뀐다. |
| 9 | P | `/procedures/11/fitzpatrick_note`, `/procedures/11/prevention` | 11번은 같은 장비 안 두 파장의 비교·선택(1064nm 위주, 532nm 최소화)이다. 3·13·14번의 '1064nm' 언급처럼 다른 행을 지칭하는 것과 구분해야 할 수 있음(후속). |
| 10 | P | `/procedures/11/fitzpatrick_note` | '532nm은 표재 혈관용이나 멜라닌 흡수 주의' — 용도 진술과 주의가 '-이나' 로 대조. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0135 | `/procedures/9/name` | IPL | 0–3 | name_candidate, mixed_language | P |  |
| E0136 | `/procedures/9/name` | 560-950nm 광대역 | 5–18 | device_param, range | P |  |
| E0137 | `/procedures/9/pih_rate` | 5-10% | 0–5 | range, rate | P |  |
| E0138 | `/procedures/9/fitzpatrick_note` | 광대역 파장이 멜라닌에 비선택적 흡수 | 0–20 | device_param, negation | P |  |
| E0139 | `/procedures/9/fitzpatrick_note` | III-IV에서 표피 멜라닌 경쟁 흡수로 PIH 위험 | 22–51 | population, condition, cause_reason, tissue_layer | P | 정도 서술 없음 |
| E0140 | `/procedures/9/risk_factors/0` | 높은 fluence | 0–10 | risk_factor_phrase, device_param | B |  |
| E0141 | `/procedures/9/risk_factors/1` | 짧은 펄스폭 | 0–6 | risk_factor_phrase, device_param, degree | B |  |
| E0142 | `/procedures/9/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0143 | `/procedures/9/risk_factors/3` | 적합하지 않은 필터 선택 | 0–13 | risk_factor_phrase, negation, device_param | P |  |
| E0144 | `/procedures/9/prevention` | Fitzpatrick IV에서 긴 파장 필터(590nm+) 사용 | 0–35 | condition, population, recommendation, device_param, comparison | P | IV 만 조건 |
| E0145 | `/procedures/9/prevention` | 590nm+ | 25–31 | quantity_unit, comparison, symbol_ambiguity | P | '+' = 이상 |
| E0146 | `/procedures/9/prevention` | 적정 fluence | 37–47 | recommendation, device_param | B |  |
| E0147 | `/procedures/9/prevention` | SPF 50+ 자외선 차단 | 49–63 | recommendation | P |  |
| E0148 | `/procedures/10/subcategory` | 혈관 | 0–2 | tissue_layer | P | 하위분류명이 타겟 조직 |
| E0149 | `/procedures/10/name` | 브이빔 | 0–3 | name_candidate | P |  |
| E0150 | `/procedures/10/name` | PDL 595nm | 5–14 | device_param, mixed_language | P |  |
| E0151 | `/procedures/10/pih_rate` | 1-5% | 0–4 | range, rate | P |  |
| E0152 | `/procedures/10/fitzpatrick_note` | 혈관 타겟이라 멜라닌 경쟁 흡수 적음 | 0–20 | cause_reason, degree | P |  |
| E0153 | `/procedures/10/fitzpatrick_note` | 자반(purpura) 후 PIH 가능 | 22–42 | time, possibility, mixed_language | F | 선후·가능성 |
| E0154 | `/procedures/10/risk_factors/0` | 자반 유발 세팅(높은 에너지, 짧은 펄스) | 0–23 | risk_factor_phrase, device_param, cause_reason | F |  |
| E0155 | `/procedures/10/risk_factors/1` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0156 | `/procedures/10/prevention` | 비자반성(subpurpuric) 세팅 우선 | 0–23 | recommendation, negation, device_param, mixed_language | P |  |
| E0157 | `/procedures/10/prevention` | SPF 50+ 자외선 차단 | 25–39 | recommendation | P |  |
| E0158 | `/procedures/11/name` | 엑셀브이/더마브이 | 0–9 | name_candidate, symbol_ambiguity | F |  |
| E0159 | `/procedures/11/name` | LP 532+1064nm | 11–24 | device_param, symbol_ambiguity, mixed_language | P | '+' = 두 파장 |
| E0160 | `/procedures/11/pih_rate` | 1-3% | 0–4 | range, rate | P |  |
| E0161 | `/procedures/11/fitzpatrick_note` | 1064nm은 멜라닌 흡수 낮아 안전 | 0–20 | cause_reason, device_param, degree | P |  |
| E0162 | `/procedures/11/fitzpatrick_note` | 532nm은 표재 혈관용이나 멜라닌 흡수 주의 | 22–47 | device_param, recommendation, tissue_layer | P |  |
| E0163 | `/procedures/11/risk_factors/0` | 532nm 사용 시 어두운 피부 | 0–17 | risk_factor_phrase, condition, population | P | 조건+집단 결합 |
| E0164 | `/procedures/11/risk_factors/1` | 높은 fluence | 0–10 | risk_factor_phrase, device_param | B |  |
| E0165 | `/procedures/11/prevention` | Fitzpatrick IV에서 1064nm 위주 사용 | 0–29 | condition, population, recommendation, device_param | P |  |
| E0166 | `/procedures/11/prevention` | 532nm 최소화 | 31–40 | recommendation, effect_change, device_param | P |  |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/10/risk_factors/0` | 자반 유발 [0,5) | 자/IC 반/NNG 유/NNG 발/NNG | '자반'(purpura)·'유발' 이 감탄사+명사 조각으로 분해 — 사건명·인과 동사 소실(심각) | K |
| `/procedures/10/prevention` | 비자반성 [0,4) | 비자반성/NNP | 부정 접두 '비-' 가 고유명사 한 덩어리에 묻힘 — 다른 칸의 비/XPN 분리와 다름 | K |
| `/procedures/11/fitzpatrick_note` | 표재 [29,31) | 표/NNG 재/XPN | '표재'(얕은 층) 오분절 — 층위 정보 소실 | K |
| `/procedures/9/name` | 560-950 [5,12) | 560-950/W_SERIAL | 파장 범위가 일련번호 한 토큰 | K |

## 5. 미결 (이 구획)

- F-S3-1 '/'·'+' 기호 뜻(장비명 대안/병기·파장 결합) 후속 (issues.md F2)
- F-S3-2 10번 자반→PIH 사슬·세팅 관계는 후속 의미 조사 (issues.md F5)
