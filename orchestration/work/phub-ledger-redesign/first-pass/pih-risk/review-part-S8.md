# S8 — procedures 23–25 · M15 케미컬필링

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/procedures/25/prevention`
- 공동 참조 문맥(소유 아님): `/description`, `/risk_levels`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `/procedures/23` | [23] | object | (object, 자식 9) | 7437–7715 |  |
| `/procedures/23/category` | category | string | "M15" | 7449–7454 |  |
| `/procedures/23/subcategory` | subcategory | string | "케미컬필링" | 7469–7476 | E0277 |
| `/procedures/23/name` | name | string | "AHA/BHA 필링 (표재성)" | 7484–7502 | E0278, E0279 |
| `/procedures/23/procedure_ref` | procedure_ref | string | "M15-1-1" | 7519–7528 |  |
| `/procedures/23/pih_risk` | pih_risk | string | "low" | 7540–7545 |  |
| `/procedures/23/pih_rate` | pih_rate | string | "1-5%" | 7557–7563 | E0280 |
| `/procedures/23/fitzpatrick_note` | fitzpatrick_note | string | "표재성 필링으로 PIH 위험 낮음. 글리콜산 30-50% 기준" | 7583–7619 | E0281, E0282 |
| `/procedures/23/risk_factors` | risk_factors | array | (array, 자식 3) | 7635–7663 |  |
| `/procedures/23/risk_factors/0` | [0] | string | "높은 농도" | 7636–7643 | E0283 |
| `/procedures/23/risk_factors/1` | [1] | string | "긴 도포 시간" | 7644–7653 | E0284 |
| `/procedures/23/risk_factors/2` | [2] | string | "어두운 피부" | 7654–7662 | E0285 |
| `/procedures/23/prevention` | prevention | string | "적정 농도·시간, SPF 50+ 자외선 차단, 점진적 농도 상향" | 7677–7714 | E0286, E0287, E0288 |
| `/procedures/24` | [24] | object | (object, 자식 9) | 7716–8073 |  |
| `/procedures/24/category` | category | string | "M15" | 7728–7733 |  |
| `/procedures/24/subcategory` | subcategory | string | "케미컬필링" | 7748–7755 | E0289 |
| `/procedures/24/name` | name | string | "TCA 필링 (중간-심층)" | 7763–7779 | E0290, E0291 |
| `/procedures/24/procedure_ref` | procedure_ref | string | "M15-1-2" | 7796–7805 |  |
| `/procedures/24/pih_risk` | pih_risk | string | "high" | 7817–7823 |  |
| `/procedures/24/pih_rate` | pih_rate | string | "15-30%" | 7835–7843 | E0292 |
| `/procedures/24/fitzpatrick_note` | fitzpatrick_note | string | "III-IV에서 높은 PIH 위험. TCA 농도 35% 이상 시 더욱 증가" | 7863–7906 | E0293, E0294 |
| `/procedures/24/risk_factors` | risk_factors | array | (array, 자식 4) | 7922–7972 |  |
| `/procedures/24/risk_factors/0` | [0] | string | "높은 TCA 농도(35%+)" | 7923–7940 | E0295 |
| `/procedures/24/risk_factors/1` | [1] | string | "깊은 침투" | 7941–7948 | E0296 |
| `/procedures/24/risk_factors/2` | [2] | string | "어두운 피부" | 7949–7957 | E0297 |
| `/procedures/24/risk_factors/3` | [3] | string | "불충분한 자외선 차단" | 7958–7971 | E0298 |
| `/procedures/24/prevention` | prevention | string | "Fitzpatrick III-IV에서 저농도(15-25%) 사용, 필요 시 hydroquinone 전처치 4주, SPF 50+ 자외선 차단 2개월 이상" | 7986–8072 | E0299, E0300, E0301 |
| `/procedures/25` | [25] | object | (object, 자식 9) | 8074–8316 |  |
| `/procedures/25/category` | category | string | "M15" | 8086–8091 |  |
| `/procedures/25/subcategory` | subcategory | string | "케미컬필링" | 8106–8113 | E0302 |
| `/procedures/25/name` | name | string | "제스너 필링" | 8121–8129 | E0303 |
| `/procedures/25/procedure_ref` | procedure_ref | string | "M15-1" | 8146–8153 |  |
| `/procedures/25/pih_risk` | pih_risk | string | "moderate" | 8165–8175 |  |
| `/procedures/25/pih_rate` | pih_rate | string | "5-10%" | 8187–8194 | E0304 |
| `/procedures/25/fitzpatrick_note` | fitzpatrick_note | string | "중간 깊이 필링으로 III-IV에서 주의 필요" | 8214–8241 | E0305 |
| `/procedures/25/risk_factors` | risk_factors | array | (array, 자식 2) | 8257–8275 |  |
| `/procedures/25/risk_factors/0` | [0] | string | "다층 도포" | 8258–8265 | E0306 |
| `/procedures/25/risk_factors/1` | [1] | string | "어두운 피부" | 8266–8274 | E0307 |
| `/procedures/25/prevention` | prevention | string | "최소 레이어 수, SPF 50+ 자외선 차단" | 8289–8315 | E0308, E0309 |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | P | `/procedures/23/fitzpatrick_note`, `/procedures/24/fitzpatrick_note`, `/procedures/24/risk_factors/0`, `/procedures/24/prevention` | 이 구획의 '%' 는 둘로 갈린다: pih_rate 의 % (위험 비율) 와 '글리콜산 30-50%', 'TCA 농도 35% 이상', '35%+', '저농도(15-25%)' 의 % (약제 농도). 같은 기호를 대상 없이 합치지 않는다. |
| 2 | B | `/procedures/23/name`, `/procedures/23/fitzpatrick_note` | 23번 name 은 'AHA/BHA 필링' 인데 note 의 기준은 '글리콜산 30-50% 기준' 하나뿐이다. BHA 쪽 기준 농도는 원문에 없다. |
| 3 | P | `/procedures/23/fitzpatrick_note` | '글리콜산 30-50% 기준' 은 이 행의 위험도가 전제하는 조건으로 읽히지만, pih_rate 전체에 걸리는지 문장 단위 진술인지 원문만으로 확정 못 함. |
| 4 | P | `/procedures/24/fitzpatrick_note`, `/procedures/24/risk_factors/0`, `/procedures/24/prevention` | 24번 TCA: 위험 증가 조건 '35% 이상' 과 권고 '저농도(15-25%)' 사이 25~35% 구간은 원문에 진술이 없다. 채우지 않는다. |
| 5 | P | `/procedures/24/prevention`, `/procedures/4/prevention` | 24번 'hydroquinone 전처치 4주' 는 전처치 기간을 준 유일한 출현이다. 4번 'hydroquinone 전처치'·5번 '전처치' 에는 기간이 없다 — 옮겨 적용하지 않는다. |
| 6 | P | `/procedures/24/name`, `/procedures/25/fitzpatrick_note`, `/procedures/23/name` | 깊이 표현: 23 '(표재성)', 24 '(중간-심층)' ('-' = 범위), 25 '중간 깊이 필링'. 필링 깊이가 name 괄호 또는 note 에 흩어져 있다. |
| 7 | P | `/procedures/25/procedure_ref`, `/procedures/23/procedure_ref`, `/procedures/24/procedure_ref` | procedure_ref: 23 'M15-1-1', 24 'M15-1-2', 25 'M15-1' — 25번만 상위 코드(P1). |
| 8 | B | `/procedures/25/risk_factors/0`, `/procedures/25/prevention` | '다층 도포' ↔ '최소 레이어 수' — 몇 층부터 다층인지·최소가 몇인지 수치 없음. |
| 9 | P | `/procedures/25/fitzpatrick_note` | 'III-IV에서 주의 필요' — 일반 주의(무엇을 어떻게 주의하는지 없음). |
| 10 | P | `/procedures/23/prevention` | '점진적 농도 상향' — 회차에 걸친 변화로 읽히나 회차·폭 없음. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0277 | `/procedures/23/subcategory` | 케미컬필링 | 0–5 | name_candidate | P |  |
| E0278 | `/procedures/23/name` | AHA/BHA 필링 | 0–10 | name_candidate, symbol_ambiguity, mixed_language | F |  |
| E0279 | `/procedures/23/name` | 표재성 | 12–15 | degree, tissue_layer | P | 필링 깊이 |
| E0280 | `/procedures/23/pih_rate` | 1-5% | 0–4 | range, rate | P |  |
| E0281 | `/procedures/23/fitzpatrick_note` | 표재성 필링으로 PIH 위험 낮음 | 0–18 | cause_reason, degree, tissue_layer | P |  |
| E0282 | `/procedures/23/fitzpatrick_note` | 글리콜산 30-50% 기준 | 20–34 | quantity_unit, range, condition, claim_scope | P | % = 농도 |
| E0283 | `/procedures/23/risk_factors/0` | 높은 농도 | 0–5 | risk_factor_phrase, degree | B |  |
| E0284 | `/procedures/23/risk_factors/1` | 긴 도포 시간 | 0–7 | risk_factor_phrase, time, degree | B |  |
| E0285 | `/procedures/23/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0286 | `/procedures/23/prevention` | 적정 농도·시간 | 0–8 | recommendation | B |  |
| E0287 | `/procedures/23/prevention` | SPF 50+ 자외선 차단 | 10–24 | recommendation | P |  |
| E0288 | `/procedures/23/prevention` | 점진적 농도 상향 | 26–35 | recommendation, time, effect_change, degree | P |  |
| E0289 | `/procedures/24/subcategory` | 케미컬필링 | 0–5 | name_candidate | P |  |
| E0290 | `/procedures/24/name` | TCA 필링 | 0–6 | name_candidate, mixed_language | P |  |
| E0291 | `/procedures/24/name` | 중간-심층 | 8–13 | range, tissue_layer, symbol_ambiguity | P | '-' = 범위 |
| E0292 | `/procedures/24/pih_rate` | 15-30% | 0–6 | range, rate | P |  |
| E0293 | `/procedures/24/fitzpatrick_note` | III-IV에서 높은 PIH 위험 | 0–18 | population, condition, degree | P |  |
| E0294 | `/procedures/24/fitzpatrick_note` | TCA 농도 35% 이상 시 더욱 증가 | 20–41 | condition, comparison, quantity_unit, degree, effect_change | P | % = 농도 |
| E0295 | `/procedures/24/risk_factors/0` | 높은 TCA 농도(35%+) | 0–15 | risk_factor_phrase, quantity_unit, comparison, symbol_ambiguity | P |  |
| E0296 | `/procedures/24/risk_factors/1` | 깊은 침투 | 0–5 | risk_factor_phrase, degree | B |  |
| E0297 | `/procedures/24/risk_factors/2` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0298 | `/procedures/24/risk_factors/3` | 불충분한 자외선 차단 | 0–11 | risk_factor_phrase, negation | P |  |
| E0299 | `/procedures/24/prevention` | Fitzpatrick III-IV에서 저농도(15-25%) 사용 | 0–35 | condition, population, recommendation, range, quantity_unit | P |  |
| E0300 | `/procedures/24/prevention` | 필요 시 hydroquinone 전처치 4주 | 37–61 | condition, time, recommendation, mixed_language | B | '필요 시' 기준 없음 |
| E0301 | `/procedures/24/prevention` | SPF 50+ 자외선 차단 2개월 이상 | 63–84 | recommendation, time, comparison | B | 기준 시점 없음 |
| E0302 | `/procedures/25/subcategory` | 케미컬필링 | 0–5 | name_candidate | P |  |
| E0303 | `/procedures/25/name` | 제스너 필링 | 0–6 | name_candidate | P |  |
| E0304 | `/procedures/25/pih_rate` | 5-10% | 0–5 | range, rate | P |  |
| E0305 | `/procedures/25/fitzpatrick_note` | 중간 깊이 필링으로 III-IV에서 주의 필요 | 0–25 | cause_reason, population, recommendation, tissue_layer | P |  |
| E0306 | `/procedures/25/risk_factors/0` | 다층 도포 | 0–5 | risk_factor_phrase, quantity_unit | B | 수치 없음 |
| E0307 | `/procedures/25/risk_factors/1` | 어두운 피부 | 0–6 | risk_factor_phrase, population | P |  |
| E0308 | `/procedures/25/prevention` | 최소 레이어 수 | 0–8 | recommendation, degree | B | 수치 없음 |
| E0309 | `/procedures/25/prevention` | SPF 50+ 자외선 차단 | 10–24 | recommendation | P |  |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/procedures/23/name` | 필링 [8,10) | 필/NNG 링/NNG | 시술명 '필링' 오분절(note 칸에선 필링/NNG 한 덩어리) | K |
| `/procedures/24/name` | 필링 [4,6) | 필/NNP 링/NNG | 시술명 오분절 | K |
| `/procedures/25/name` | 제스너 [0,3) | 제스/NNP 너/NP | 고유명 '제스너' 가 고유명사+대명사로 | K |
| `/procedures/24/risk_factors/0` | 35%+ [10,14) | 35/SN %+/SW | '%' 와 '+'(이상) 가 한 기호 토큰으로 묶임 | K |
| `/procedures/25/fitzpatrick_note` | 깊이 [3,5) | 깊이/MAG | 명사 '깊이' 가 부사로 | K |
| `/procedures/24/prevention` | 전처치 [55,58) | 전처치/NNG | 4·5번에선 전/MM 처치/NNG — 같은 말이 칸마다 다르게 분절 | K |

## 5. 미결 (이 구획)

- B-S8-1 BHA 기준 농도 없음 (issues.md B7)
- B-S8-2 다층/최소 레이어 수치 없음 (issues.md B4)
- F-S8-1 % 의 대상(위험 비율 vs 농도) 구분은 후속 모델에서 (issues.md F6)
