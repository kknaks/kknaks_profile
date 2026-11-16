# S04 — `M13` (플라즈마) · extracted.json 1차 조사

> 구획 S04 · 소유 Pointer `/M13` 와 그 아래 44개 노드(말단 31). 문맥 참조: 루트 `""`, `/M13/name`, `/M13/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 2 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M13)` | `/M13` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M13/name` | string | 플라즈마 | 분석 |
| 3 | `safety` | `/M13/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M13/safety/common` | array | (array · 2) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M13/safety/common/0` | string | 시술 중 약간의 따끔거림 | 분석 |
| 6 | `safety.common[1]` | `/M13/safety/common/1` | string | 일시적 홍반 (빨개짐) | 분석 |
| 7 | `safety.serious` | `/M13/safety/serious` | null | null | 제외: 문자열 아님 |
| 8 | `safety.uncommon` | `/M13/safety/uncommon` | array | (array · 1) | —(컨테이너) |
| 9 | `safety.uncommon[0]` | `/M13/safety/uncommon/0` | string | 피부 건조감 | 분석 |
| 10 | `source` | `/M13/source` | string | 일반 의학 지식 | 분석 |
| 11 | `name_en` | `/M13/name_en` | string | Plasma Treatment | 분석 |
| 12 | `overview` | `/M13/overview` | string | 플라즈마 시술은 기체에 에너지를 가해 만든 플라즈마(제4의 물질 상태)를 피부에 적용하여 피부 재생, 살균, 약물 흡수 촉진 등의 효과를 얻는 시술이다. 한국에서는 '플라즈마 샤워', '플라즈젯', '플렉스마' 등의 이름으로 알려져 있다. | 분석 |
| 13 | `aftercare` | `/M13/aftercare` | array | (array · 2) | —(컨테이너) |
| 14 | `aftercare[0]` | `/M13/aftercare/0` | string | 특별한 다운타임 없이 일상생활 바로 가능 | 분석 |
| 15 | `aftercare[1]` | `/M13/aftercare/1` | string | 시술 직후 보습제 및 자외선 차단제 도포 | 분석 |
| 16 | `mechanism` | `/M13/mechanism` | string | 플라즈마는 기체(주로 질소 또는 헬륨)에 고에너지를 가해 이온화시킨 상태로, 활성 산소종(ROS)과 활성 질소종(RNS) 등 반응성이 높은 입자들을 포함한다. 이러한 활성 입자들이 피부 표면에 작용하면 살균 효과(세균, 바이러스, 진균 제거)를 나타내고, 피부 세포의 재생을 촉진한다. 또한 피부 장벽을 일시적으로 열어주어 이후 도포하는 약물이나 화장품 성분의 피부 흡수율을 크게 높여준다. | 분석 |
| 17 | `indications` | `/M13/indications` | object | (object · 2) | —(컨테이너) |
| 18 | `indications.primary` | `/M13/indications/primary` | array | (array · 3) | —(컨테이너) |
| 19 | `indications.primary[0]` | `/M13/indications/primary/0` | string | 피부 살균 및 진정 (여드름, 염증성 피부) | 분석 |
| 20 | `indications.primary[1]` | `/M13/indications/primary/1` | string | 약물/화장품 성분 피부 흡수 촉진 | 분석 |
| 21 | `indications.primary[2]` | `/M13/indications/primary/2` | string | 피부 재생 및 탄력 개선 | 분석 |
| 22 | `indications.extended` | `/M13/indications/extended` | array | (array · 3) | —(컨테이너) |
| 23 | `indications.extended[0]` | `/M13/indications/extended/0` | string | 아토피 피부염 보조 치료 | 분석 |
| 24 | `indications.extended[1]` | `/M13/indications/extended/1` | string | 상처 치유 촉진 | 분석 |
| 25 | `indications.extended[2]` | `/M13/indications/extended/2` | string | 색소 개선 보조 | 분석 |
| 26 | `source_type` | `/M13/source_type` | string | general | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 27 | `extracted_at` | `/M13/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 28 | `procedure_id` | `/M13/procedure_id` | string | M13-PLASMA | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 29 | `onset_duration` | `/M13/onset_duration` | object | (object · 3) | —(컨테이너) |
| 30 | `onset_duration.peak` | `/M13/onset_duration/peak` | string | 반복 시술 후 2~4주 뒤 피부 개선 체감 | 분석 |
| 31 | `onset_duration.onset` | `/M13/onset_duration/onset` | string | 시술 직후 피부 진정/살균 효과 | 분석 |
| 32 | `onset_duration.duration` | `/M13/onset_duration/duration` | string | 단독 시술보다 다른 시술과 병합 시 시너지 효과 | 분석 |
| 33 | `contraindications` | `/M13/contraindications` | object | (object · 2) | —(컨테이너) |
| 34 | `contraindications.absolute` | `/M13/contraindications/absolute` | array | (array · 2) | —(컨테이너) |
| 35 | `contraindications.absolute[0]` | `/M13/contraindications/absolute/0` | string | 심장박동기(페이스메이커) 사용자 | 분석 |
| 36 | `contraindications.absolute[1]` | `/M13/contraindications/absolute/1` | string | 시술 부위에 금속 임플란트가 있는 경우 | 분석 |
| 37 | `contraindications.relative` | `/M13/contraindications/relative` | array | (array · 2) | —(컨테이너) |
| 38 | `contraindications.relative[0]` | `/M13/contraindications/relative/0` | string | 임신 중이거나 수유 중인 경우 | 분석 |
| 39 | `contraindications.relative[1]` | `/M13/contraindications/relative/1` | string | 심한 피부 손상이 있는 부위 | 분석 |
| 40 | `guardrail_version` | `/M13/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 41 | `related_techniques` | `/M13/related_techniques` | array | (array · 3) | —(컨테이너) |
| 42 | `related_techniques[0]` | `/M13/related_techniques/0` | string | 메디컬스킨케어(필링) -- 병합 시 약물 흡수율 향상 | 분석 |
| 43 | `related_techniques[1]` | `/M13/related_techniques/1` | string | 레이저 토닝 -- 색소 치료와 병합 | 분석 |
| 44 | `related_techniques[2]` | `/M13/related_techniques/2` | string | MTS(마이크로니들링) -- 피부 재생 시너지 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S04-01** (I) onset_duration/duration 값이 지속 기간이 아니라 병합 효과 진술이다. → I7, B3  
  근거: `/M13/onset_duration/duration` 「단독 시술보다 다른 시술과 병합 시 시너지 효과」
- **OB-S04-02** (구조) safety/serious 가 null, uncommon 은 1개, common 2개로 이 원장에서 가장 짧은 safety 다. → B1  
  근거: `/M13/safety/serious`; `/M13/safety/uncommon/0` 「피부 건조감」
- **OB-S04-03** (P) overview 의 따옴표 이름(플라즈마 샤워·플라즈젯·플렉스마)은 원문이 「이름」이라고만 적었다(브랜드명이라 하지 않음). → F11  
  근거: `/M13/overview` 「등의 이름으로 알려져 있다」
- **OB-S04-04** (F) related 「메디컬스킨케어(필링)」은 M15 name 「메디컬스킨케어」를, 「MTS(마이크로니들링)」은 M12 를 가리키는 듯한 문자열이다. 연결 확정은 후속이다. → F6  
  근거: `/M13/related_techniques/0` 「메디컬스킨케어(필링)」; `/M13/related_techniques/2` 「MTS(마이크로니들링)」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX040 | alternative_with_frequency | `/M13/mechanism` | (주로 질소 또는 헬륨) |  |
| MX041 | duration_modifier_scoped | `/M13/mechanism` | 피부 장벽을 일시적으로 열어주어 |  |
| MX042 | time_window_with_anchor | `/M13/onset_duration/peak` | 반복 시술 후 2~4주 뒤 피부 개선 체감 |  |
| MX043 | field_content_without_time | `/M13/onset_duration/duration` | 단독 시술보다 다른 시술과 병합 시 시너지 효과 | duration 칸이 병합 효과 진술(I7) |
| MX044 | degree_site_condition | `/M13/contraindications/relative/1` | 심한 피부 손상이 있는 부위 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|

규칙 기반 표현 후보 120건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S04"` 에 있다. 후보이며 전수 의미 해석이 아니다.
