# S06 — `M15` (메디컬스킨케어) · extracted.json 1차 조사

> 구획 S06 · 소유 Pointer `/M15` 와 그 아래 64개 노드(말단 50). 문맥 참조: 루트 `""`, `/M15/name`, `/M15/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 2 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M15)` | `/M15` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M15/name` | string | 메디컬스킨케어 | 분석 |
| 3 | `safety` | `/M15/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M15/safety/common` | array | (array · 3) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M15/safety/common/0` | string | 시술 후 2~3일간 피부 건조 및 각질 발생 | 분석 |
| 6 | `safety.common[1]` | `/M15/safety/common/1` | string | 일시적 홍반 (빨개짐) -- 시간 지나면 대부분 호전 | 분석 |
| 7 | `safety.common[2]` | `/M15/safety/common/2` | string | 약간의 따가움 | 분석 |
| 8 | `safety.serious` | `/M15/safety/serious` | array | (array · 3) | —(컨테이너) |
| 9 | `safety.serious[0]` | `/M15/safety/serious/0` | string | 반흔 (중층박피 후 비후성 반흔 발생빈도 1% 이내) | 분석 |
| 10 | `safety.serious[1]` | `/M15/safety/serious/1` | string | 비후성 반흔 (깊은 필링에서 드물게) | 분석 |
| 11 | `safety.serious[2]` | `/M15/safety/serious/2` | string | 색소탈실 (피부가 하얗게 변하는 것, 특히 페놀 필링) | 분석 |
| 12 | `safety.uncommon` | `/M15/safety/uncommon` | array | (array · 3) | —(컨테이너) |
| 13 | `safety.uncommon[0]` | `/M15/safety/uncommon/0` | string | 염증후색소침착(PIH, 시술 부위가 어두워지는 것) | 분석 |
| 14 | `safety.uncommon[1]` | `/M15/safety/uncommon/1` | string | 감염 (바이러스 감염 포함) | 분석 |
| 15 | `safety.uncommon[2]` | `/M15/safety/uncommon/2` | string | 알레르기 반응 | 분석 |
| 16 | `source` | `/M15/source` | string | 임상적 피부관리 14장 (필링) | 분석 |
| 17 | `name_en` | `/M15/name_en` | string | Medical Skincare / Chemical Peeling | 분석 |
| 18 | `overview` | `/M15/overview` | string | 메디컬스킨케어는 피부과에서 시행하는 전문적인 피부 관리 시술을 총칭하며, 대표적으로 화학박피술(케미칼필링)이 있다. 필링은 화학물질, 기계적 방법, 레이저 등을 이용하여 노화되고 손상된 피부를 벗겨내고 새로운 피부 재생을 유도하는 시술이다. 일상적 피부 관리의 기본이자 핵심으로, 여드름, 기미, 잔주름, 모공 등 다양한 피부 고민에 활용된다. | 분석 |
| 19 | `aftercare` | `/M15/aftercare` | array | (array · 5) | —(컨테이너) |
| 20 | `aftercare[0]` | `/M15/aftercare/0` | string | 자외선 차단이 가장 중요 -- SPF 30 이상 자외선차단제를 2~3시간 간격으로 재도포 | 분석 |
| 21 | `aftercare[1]` | `/M15/aftercare/1` | string | 최소 시술 후 3개월간은 강박적으로 자외선 차단제 사용 | 분석 |
| 22 | `aftercare[2]` | `/M15/aftercare/2` | string | 보습제를 자주 도포해 피부 수분 유지 | 분석 |
| 23 | `aftercare[3]` | `/M15/aftercare/3` | string | 필링 후 통증이 3~4일 지속되면 바이러스 감염 의심하고 대응 | 분석 |
| 24 | `aftercare[4]` | `/M15/aftercare/4` | string | 필링 후 관리: 클렌징-pH 밸런싱-앰플관리-마스크-보습-메이크업 순서 | 분석 |
| 25 | `mechanism` | `/M15/mechanism` | string | 케미칼필링은 화학물질을 피부에 도포하여 해당 조직의 구조를 시각적으로 개선시키고자 하는 피부 개선 치료의 하나로, 각질이 벗겨지는 자연적 과정을 단순히 가속화시키는 것이지만 단백질의 응고 혹은 용해로 인해서 표피와 진피 일부를 완전히 파괴할 수도 있다. 필링에 사용된 성분과 적용 방법에 따라 재생 정도에 차이가 생기며, 진피에서 피부의 재생이 일어난다. 얕은필링(AHA, 저농도 TCA)은 각질층~표피층만 벗겨내고, 중간필링(고농도 TCA)은 유두진피까지, 깊은필링(페놀)은 망상진피 하부까지 영향을 미친다. | 분석 |
| 26 | `indications` | `/M15/indications` | object | (object · 2) | —(컨테이너) |
| 27 | `indications.primary` | `/M15/indications/primary` | array | (array · 4) | —(컨테이너) |
| 28 | `indications.primary[0]` | `/M15/indications/primary/0` | string | 칙칙한 피부 (거무칙칙함) 개선 -- 가장 흔한 적응증 | 분석 |
| 29 | `indications.primary[1]` | `/M15/indications/primary/1` | string | 여드름 치료 및 여드름 흉터 | 분석 |
| 30 | `indications.primary[2]` | `/M15/indications/primary/2` | string | 모공각화증 (피부 표면의 까칠한 돌기) | 분석 |
| 31 | `indications.primary[3]` | `/M15/indications/primary/3` | string | 잔주름 개선 | 분석 |
| 32 | `indications.extended` | `/M15/indications/extended` | array | (array · 8) | —(컨테이너) |
| 33 | `indications.extended[0]` | `/M15/indications/extended/0` | string | 기미 (피부 색소 불균일) | 분석 |
| 34 | `indications.extended[1]` | `/M15/indications/extended/1` | string | 주근깨 | 분석 |
| 35 | `indications.extended[2]` | `/M15/indications/extended/2` | string | 흑자 (검은 점) | 분석 |
| 36 | `indications.extended[3]` | `/M15/indications/extended/3` | string | PIH(염증후색소침착, 피부 트러블 후 자국) | 분석 |
| 37 | `indications.extended[4]` | `/M15/indications/extended/4` | string | 지루각화증 (노인성 사마귀) | 분석 |
| 38 | `indications.extended[5]` | `/M15/indications/extended/5` | string | 광선각화증 (자외선에 의한 피부 변화) | 분석 |
| 39 | `indications.extended[6]` | `/M15/indications/extended/6` | string | 튼살 | 분석 |
| 40 | `indications.extended[7]` | `/M15/indications/extended/7` | string | 닭살 (모공각화증) | 분석 |
| 41 | `source_type` | `/M15/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 42 | `extracted_at` | `/M15/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 43 | `procedure_id` | `/M15/procedure_id` | string | M15-SKINCARE | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 44 | `onset_duration` | `/M15/onset_duration` | object | (object · 3) | —(컨테이너) |
| 45 | `onset_duration.peak` | `/M15/onset_duration/peak` | string | 필링 후 1~4회 진정/재생 관리 후 최종 결과 | 분석 |
| 46 | `onset_duration.onset` | `/M15/onset_duration/onset` | string | 얕은 필링은 시술 직후부터, 중간/깊은 필링은 1~2주 후 회복되면서 효과 시작 | 분석 |
| 47 | `onset_duration.duration` | `/M15/onset_duration/duration` | string | 1회 시술 효과 2~4주, 주기적 시술로 장기 개선 유지 | 분석 |
| 48 | `contraindications` | `/M15/contraindications` | object | (object · 2) | —(컨테이너) |
| 49 | `contraindications.absolute` | `/M15/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 50 | `contraindications.absolute[0]` | `/M15/contraindications/absolute/0` | string | 피부 유형 IV~VI형 (어두운 피부)에서 깊은 필링은 색소장애 위험 | 분석 |
| 51 | `contraindications.absolute[1]` | `/M15/contraindications/absolute/1` | string | 활동성 바이러스 감염 (단순포진 등) | 분석 |
| 52 | `contraindications.absolute[2]` | `/M15/contraindications/absolute/2` | string | 시술 부위 피부 상태가 나쁜 경우나 면역결핍 상태 | 분석 |
| 53 | `contraindications.relative` | `/M15/contraindications/relative` | array | (array · 6) | —(컨테이너) |
| 54 | `contraindications.relative[0]` | `/M15/contraindications/relative/0` | string | 비타민유도체(이소트레티노인) 복용 중인 경우 박피 후 반흔 우려 | 분석 |
| 55 | `contraindications.relative[1]` | `/M15/contraindications/relative/1` | string | 자외선 차단이 불가능한 사람 | 분석 |
| 56 | `contraindications.relative[2]` | `/M15/contraindications/relative/2` | string | 켈로이드 체질 | 분석 |
| 57 | `contraindications.relative[3]` | `/M15/contraindications/relative/3` | string | 과도한 기대를 하는 경우 | 분석 |
| 58 | `contraindications.relative[4]` | `/M15/contraindications/relative/4` | string | 임산부 | 분석 |
| 59 | `contraindications.relative[5]` | `/M15/contraindications/relative/5` | string | 흡연 및 경구 피임약, 갱년기 에스트로겐 복용 중 | 분석 |
| 60 | `guardrail_version` | `/M15/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 61 | `related_techniques` | `/M15/related_techniques` | array | (array · 3) | —(컨테이너) |
| 62 | `related_techniques[0]` | `/M15/related_techniques/0` | string | MTS(마이크로니들링) -- 물리적 자극으로 피부 재생 유도 | 분석 |
| 63 | `related_techniques[1]` | `/M15/related_techniques/1` | string | 레이저토닝 -- 기미/색소 치료에 병합 | 분석 |
| 64 | `related_techniques[2]` | `/M15/related_techniques/2` | string | LDM(초음파) -- 피부 진정 및 재생 시너지 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S06-01** (I) serious 에 「반흔」과 「비후성 반흔」이 따로 있고 첫 값의 괄호도 비후성 반흔 빈도를 말한다. 같은 사건이 두 값에 겹친다. indications 에서도 「모공각화증」(primary)과 「닭살 (모공각화증)」(extended)이 겹친다. → I10  
  근거: `/M15/safety/serious/0` 「중층박피 후 비후성 반흔 발생빈도 1% 이내」; `/M15/safety/serious/1` 「비후성 반흔」; `/M15/indications/primary/2` 「모공각화증」; `/M15/indications/extended/7` 「닭살 (모공각화증)」
- **OB-S06-02** (F) 필링 깊이 하위 유형(얕은·중간·깊은)과 각 층(각질층~표피층 · 유두진피 · 망상진피 하부), 약제(AHA·저농도 TCA·고농도 TCA·페놀)가 mechanism 에 있고 onset 은 유형별 시간이 다르다. 「얕은필링」/「얕은 필링」 띄어쓰기도 다르다. 「얕은·깊은」은 필링 깊이 등급이며 mm 가 아니다. → F3, F7  
  근거: `/M15/mechanism` 「얕은필링(AHA, 저농도 TCA)」; `/M15/onset_duration/onset` 「얕은 필링은 시술 직후부터」
- **OB-S06-03** (I) absolute 금기 첫 값은 환자 조건이 아니라 「피부 유형 IV~VI형에서 깊은 필링은 색소장애 위험」이라는 하위 유형 조건 위험 진술이다. absolute 셋째 값은 두 조건(피부 상태 불량·면역결핍)을 「나」로 묶었다. → I8  
  근거: `/M15/contraindications/absolute/0` 「깊은 필링은 색소장애 위험」; `/M15/contraindications/absolute/2` 「나쁜 경우나 면역결핍 상태」
- **OB-S06-04** (F) name 「메디컬스킨케어」는 overview 에서 전문 피부 관리 시술의 「총칭」이고 대표가 화학박피술이다. name_en 은 「Medical Skincare / Chemical Peeling」. 항목 범위가 총칭인지 필링인지 값마다 다르다. → F11  
  근거: `/M15/overview` 「총칭하며, 대표적으로 화학박피술(케미칼필링)이 있다」; `/M15/name_en` 「Medical Skincare / Chemical Peeling」
- **OB-S06-05** (P) aftercare 다섯째 값의 「-」는 관리 단계의 순서 구분자다(README 에 없는 기호 용법). aftercare 넷째 값은 「3~4일 지속되면 → 의심하고 대응」의 조건-행동이다. → F5, F7  
  근거: `/M15/aftercare/4` 「클렌징-pH 밸런싱-앰플관리-마스크-보습-메이크업 순서」; `/M15/aftercare/3` 「3~4일 지속되면」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX054 | time_window_with_anchor | `/M15/safety/common/0` | 시술 후 2~3일간 |  |
| MX055 | course_frequency | `/M15/safety/common/1` | 시간 지나면 대부분 호전 |  |
| MX056 | quantity_with_target | `/M15/safety/serious/0` | 중층박피 후 비후성 반흔 발생빈도 1% 이내 | 조건(중층박피 후) + 사건 + 수치 상한. 분모 미기재 |
| MX057 | frequency_degree_scoped_condition | `/M15/safety/serious/1` | (깊은 필링에서 드물게) |  |
| MX058 | subtype_condition | `/M15/safety/serious/2` | 특히 페놀 필링 |  |
| MX059 | quantity_threshold_interval | `/M15/aftercare/0` | SPF 30 이상 자외선차단제를 2~3시간 간격으로 재도포 |  |
| MX060 | time_window_with_anchor | `/M15/aftercare/1` | 최소 시술 후 3개월간은 강박적으로 |  |
| MX061 | condition_threshold_time_window | `/M15/aftercare/3` | 필링 후 통증이 3~4일 지속되면 바이러스 감염 의심하고 대응 |  |
| MX062 | sequence_hyphen | `/M15/aftercare/4` | 클렌징-pH 밸런싱-앰플관리-마스크-보습-메이크업 순서 | 「-」가 순서 구분자로 쓰임 |
| MX063 | possibility_statement | `/M15/mechanism` | 표피와 진피 일부를 완전히 파괴할 수도 있다 |  |
| MX064 | subtype_depth_range | `/M15/mechanism` | 얕은필링(AHA, 저농도 TCA)은 각질층~표피층만 벗겨내고 |  |
| MX065 | subtype_depth_range | `/M15/mechanism` | 중간필링(고농도 TCA)은 유두진피까지 |  |
| MX066 | subtype_depth_range | `/M15/mechanism` | 깊은필링(페놀)은 망상진피 하부까지 |  |
| MX067 | subtype_time | `/M15/onset_duration/onset` | 얕은 필링은 시술 직후부터, 중간/깊은 필링은 1~2주 후 회복되면서 효과 시작 |  |
| MX068 | count_time | `/M15/onset_duration/duration` | 1회 시술 효과 2~4주 |  |
| MX069 | population_subtype_risk | `/M15/contraindications/absolute/0` | 피부 유형 IV~VI형 (어두운 피부)에서 깊은 필링은 색소장애 위험 | 금기 칸이 위험 진술 형태(I8) |
| MX070 | medication_condition_risk | `/M15/contraindications/relative/0` | 복용 중인 경우 박피 후 반흔 우려 |  |
| MX071 | negated_condition | `/M15/contraindications/relative/1` | 자외선 차단이 불가능한 사람 |  |
| MX072 | frequency_degree_scoped | `/M15/indications/primary/0` | 가장 흔한 적응증 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R09-1 | `/M15/indications/primary/0` | [8,13) | 거무칙칙함 | 거/NP + 무/XPN + 칙칙/XR + 하/XSA + ᆷ/ETN | 「거무칙칙함」의 「거」를 대명사(NP)로 분석 | 색조 형용 표현이 대명사 + 접두사로 깨짐. 수식(색조) 표현 탐색 누락 |
| R13-1 | `/M15/contraindications/relative/0` | [30,32) | 반흔 | 반/NNG + 흔/NNG | 「반흔」이 반/NNG + 흔/NNG 로 분절(같은 원장 다른 출현은 한 단어) | 흉터(반흔) 사건 명사 소실 — 금기 문맥의 위험 대상 탐색 누락 |
| R20-2 | `/M15/indications/extended/6` | [0,2) | 튼살 | 트/VV + ᆫ/ETM + 살/NNG | 「튼살」을 트/VV + ᆫ/ETM + 살/NNG 로 분해 | 문법적으로 가능한 분해이나 질환/고민 명칭 단위가 사라짐(동사 「트다」 + 「살」) |

규칙 기반 표현 후보 291건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S06"` 에 있다. 후보이며 전수 의미 해석이 아니다.
