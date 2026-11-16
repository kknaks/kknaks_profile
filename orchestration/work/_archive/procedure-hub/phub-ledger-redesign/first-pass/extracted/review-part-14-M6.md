# S14 — `M6` (지방이식) · extracted.json 1차 조사

> 구획 S14 · 소유 Pointer `/M6` 와 그 아래 53개 노드(말단 39). 문맥 참조: 루트 `""`, `/M6/name`, `/M6/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 5 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M6)` | `/M6` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M6/name` | string | 지방이식 | 분석 |
| 3 | `safety` | `/M6/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M6/safety/common` | array | (array · 3) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M6/safety/common/0` | string | 채취 부위 및 주입 부위의 멍과 붓기 | 분석 |
| 6 | `safety.common[1]` | `/M6/safety/common/1` | string | 주입 부위 통증 및 불편감 | 분석 |
| 7 | `safety.common[2]` | `/M6/safety/common/2` | string | 초기 과교정 (붓기로 인해 볼륨이 과하게 보이는 것) | 분석 |
| 8 | `safety.serious` | `/M6/safety/serious` | array | (array · 3) | —(컨테이너) |
| 9 | `safety.serious[0]` | `/M6/safety/serious/0` | string | 감염 | 분석 |
| 10 | `safety.serious[1]` | `/M6/safety/serious/1` | string | 지방 색전증 (지방이 혈관에 들어가는 것 -- 극히 드묾) | 분석 |
| 11 | `safety.serious[2]` | `/M6/safety/serious/2` | string | 혈관 막힘으로 인한 피부 괴사 (극히 드묾) | 분석 |
| 12 | `safety.uncommon` | `/M6/safety/uncommon` | array | (array · 3) | —(컨테이너) |
| 13 | `safety.uncommon[0]` | `/M6/safety/uncommon/0` | string | 주입된 지방의 불균일한 생착 (울퉁불퉁해지는 것) | 분석 |
| 14 | `safety.uncommon[1]` | `/M6/safety/uncommon/1` | string | 석회화 (지방이 딱딱하게 굳는 것) | 분석 |
| 15 | `safety.uncommon[2]` | `/M6/safety/uncommon/2` | string | 지방 낭종 (기름 주머니 형성) | 분석 |
| 16 | `source` | `/M6/source` | string | 일반 의학 지식 | 분석 |
| 17 | `name_en` | `/M6/name_en` | string | Autologous Fat Grafting | 분석 |
| 18 | `overview` | `/M6/overview` | string | 지방이식은 본인의 몸에서 지방을 채취해서 볼륨이 필요한 부위에 주입하는 시술이다. 자기 자신의 지방을 사용하므로 알레르기 반응이 없고, 한 번 생착(살아붙으면)되면 반영구적으로 유지된다는 장점이 있다. | 분석 |
| 19 | `aftercare` | `/M6/aftercare` | array | (array · 3) | —(컨테이너) |
| 20 | `aftercare[0]` | `/M6/aftercare/0` | string | 채취 부위에 압박 붕대 착용 | 분석 |
| 21 | `aftercare[1]` | `/M6/aftercare/1` | string | 주입 부위를 강하게 누르거나 마사지하지 않기 | 분석 |
| 22 | `aftercare[2]` | `/M6/aftercare/2` | string | 시술 후 1~2주간 격렬한 운동 피하기 | 분석 |
| 23 | `mechanism` | `/M6/mechanism` | string | 복부, 허벅지 등 지방이 충분한 부위에서 소량의 지방을 리포석션(지방흡입) 방식으로 채취한 후, 원심분리기로 순수 지방세포만 분리한다. 분리된 지방세포를 미세 캐뉼라(가느다란 관)를 통해 볼륨이 필요한 부위(얼굴, 가슴, 엉덩이 등)에 소량씩 여러 층에 나누어 주입한다. 주입된 지방 중 일부는 주변 혈관과 연결되어 살아남고(생착), 나머지는 체내에서 자연 흡수된다. | 분석 |
| 24 | `indications` | `/M6/indications` | object | (object · 2) | —(컨테이너) |
| 25 | `indications.primary` | `/M6/indications/primary` | array | (array · 3) | —(컨테이너) |
| 26 | `indications.primary[0]` | `/M6/indications/primary/0` | string | 얼굴 볼륨 회복 (나이가 들면서 꺼진 볼, 관자놀이, 눈밑 등) | 분석 |
| 27 | `indications.primary[1]` | `/M6/indications/primary/1` | string | 이마 볼륨 확대 | 분석 |
| 28 | `indications.primary[2]` | `/M6/indications/primary/2` | string | 팔자주름 (깊은 주름) 개선 | 분석 |
| 29 | `indications.extended` | `/M6/indications/extended` | array | (array · 4) | —(컨테이너) |
| 30 | `indications.extended[0]` | `/M6/indications/extended/0` | string | 손등 회춘술 | 분석 |
| 31 | `indications.extended[1]` | `/M6/indications/extended/1` | string | 가슴 확대 (소량 확대) | 분석 |
| 32 | `indications.extended[2]` | `/M6/indications/extended/2` | string | 엉덩이 윤곽 개선 | 분석 |
| 33 | `indications.extended[3]` | `/M6/indications/extended/3` | string | 흉터 교정 (위축성 흉터) | 분석 |
| 34 | `source_type` | `/M6/source_type` | string | general | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 35 | `extracted_at` | `/M6/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 36 | `procedure_id` | `/M6/procedure_id` | string | M6-FATGRAFT | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 37 | `onset_duration` | `/M6/onset_duration` | object | (object · 3) | —(컨테이너) |
| 38 | `onset_duration.peak` | `/M6/onset_duration/peak` | string | 붓기가 빠진 후 3~6개월 뒤 최종 생착량 확인 | 분석 |
| 39 | `onset_duration.onset` | `/M6/onset_duration/onset` | string | 시술 직후 볼륨 효과 (초기에는 붓기 포함) | 분석 |
| 40 | `onset_duration.duration` | `/M6/onset_duration/duration` | string | 생착된 지방은 반영구적 유지 (생착률 30~70%, 개인차 큼) | 분석 |
| 41 | `contraindications` | `/M6/contraindications` | object | (object · 2) | —(컨테이너) |
| 42 | `contraindications.absolute` | `/M6/contraindications/absolute` | array | (array · 2) | —(컨테이너) |
| 43 | `contraindications.absolute[0]` | `/M6/contraindications/absolute/0` | string | 채취할 지방이 충분하지 않은 경우 (극심한 저체중) | 분석 |
| 44 | `contraindications.absolute[1]` | `/M6/contraindications/absolute/1` | string | 시술 부위에 활동성 감염이 있는 경우 | 분석 |
| 45 | `contraindications.relative` | `/M6/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 46 | `contraindications.relative[0]` | `/M6/contraindications/relative/0` | string | 혈액 응고 장애가 있는 경우 | 분석 |
| 47 | `contraindications.relative[1]` | `/M6/contraindications/relative/1` | string | 당뇨병 등 상처 회복이 느린 전신 질환 | 분석 |
| 48 | `contraindications.relative[2]` | `/M6/contraindications/relative/2` | string | 임신 중이거나 수유 중인 경우 | 분석 |
| 49 | `guardrail_version` | `/M6/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 50 | `related_techniques` | `/M6/related_techniques` | array | (array · 3) | —(컨테이너) |
| 51 | `related_techniques[0]` | `/M6/related_techniques/0` | string | 히알루론산 필러 -- 소량 볼륨 보정에 간편한 대안 | 분석 |
| 52 | `related_techniques[1]` | `/M6/related_techniques/1` | string | SVF(기질혈관분획) -- 지방에서 줄기세포를 분리하여 추가 재생 효과 | 분석 |
| 53 | `related_techniques[2]` | `/M6/related_techniques/2` | string | PRP(혈소판풍부혈장) -- 지방이식 시 병합하여 생착률 향상 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S14-01** (F) 부위 역할이 채취 부위와 주입 부위로 나뉜다(safety·aftercare·mechanism). mechanism 은 채취 부위 예(복부, 허벅지)와 주입 부위 예(얼굴, 가슴, 엉덩이)를 따로 든다. → F1  
  근거: `/M6/safety/common/0` 「채취 부위 및 주입 부위」; `/M6/mechanism` 「복부, 허벅지 등 지방이 충분한 부위」; `/M6/mechanism` 「(얼굴, 가슴, 엉덩이 등)」
- **OB-S14-02** (F) duration 의 「생착률 30~70%」는 생착 비율이며 개인차가 크다고 적었다. overview·duration 의 「반영구적」은 생착된 지방에 걸린다. → F10  
  근거: `/M6/onset_duration/duration` 「생착률 30~70%, 개인차 큼」; `/M6/overview` 「반영구적으로 유지된다」
- **OB-S14-03** (B) serious 「감염」은 조건·빈도 없이 단어 하나다. 다른 두 serious 값에는 「극히 드묾」이 붙었다. → B1  
  근거: `/M6/safety/serious/0` 「감염」; `/M6/safety/serious/2` 「(극히 드묾)」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX142 | site_role | `/M6/safety/common/0` | 채취 부위 및 주입 부위의 멍과 붓기 |  |
| MX143 | frequency_degree_scoped | `/M6/safety/serious/1` | 지방이 혈관에 들어가는 것 -- 극히 드묾 |  |
| MX144 | condition_duration | `/M6/overview` | 한 번 생착(살아붙으면)되면 반영구적으로 유지된다 |  |
| MX145 | time_window_avoidance | `/M6/aftercare/2` | 시술 후 1~2주간 격렬한 운동 피하기 |  |
| MX146 | time_window_with_anchor | `/M6/onset_duration/peak` | 붓기가 빠진 후 3~6개월 뒤 최종 생착량 확인 |  |
| MX147 | quantity_with_target | `/M6/onset_duration/duration` | (생착률 30~70%, 개인차 큼) |  |
| MX148 | negated_threshold_condition | `/M6/contraindications/absolute/0` | 채취할 지방이 충분하지 않은 경우 (극심한 저체중) |  |
| MX149 | alternative | `/M6/related_techniques/0` | 소량 볼륨 보정에 간편한 대안 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|

규칙 기반 표현 후보 204건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S14"` 에 있다. 후보이며 전수 의미 해석이 아니다.
