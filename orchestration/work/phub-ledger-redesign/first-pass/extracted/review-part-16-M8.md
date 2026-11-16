# S16 — `M8` (레이저) · extracted.json 1차 조사

> 구획 S16 · 소유 Pointer `/M8` 와 그 아래 64개 노드(말단 49). 문맥 참조: 루트 `""`, `/M8/name`, `/M8/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 6 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M8)` | `/M8` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M8/name` | string | 레이저 | 분석 |
| 3 | `safety` | `/M8/safety` | object | (object · 4) | —(컨테이너) |
| 4 | `safety.common` | `/M8/safety/common` | array | (array · 4) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M8/safety/common/0` | string | 시술 부위 홍반 (빨개짐) | 분석 |
| 6 | `safety.common[1]` | `/M8/safety/common/1` | string | 부종 (붓기) | 분석 |
| 7 | `safety.common[2]` | `/M8/safety/common/2` | string | 일시적 통증이나 열감 | 분석 |
| 8 | `safety.common[3]` | `/M8/safety/common/3` | string | 가벼운 딱지 형성 | 분석 |
| 9 | `safety.serious` | `/M8/safety/serious` | array | (array · 3) | —(컨테이너) |
| 10 | `safety.serious[0]` | `/M8/safety/serious/0` | string | 흉터 (에너지가 과한 경우) | 분석 |
| 11 | `safety.serious[1]` | `/M8/safety/serious/1` | string | 감염 (특히 박피형 레이저 후) | 분석 |
| 12 | `safety.serious[2]` | `/M8/safety/serious/2` | string | 눈 손상 (보호안경 미착용 시) | 분석 |
| 13 | `safety.uncommon` | `/M8/safety/uncommon` | array | (array · 3) | —(컨테이너) |
| 14 | `safety.uncommon[0]` | `/M8/safety/uncommon/0` | string | 색소침착 (시술 후 피부가 일시적으로 어두워지는 현상 — 특히 아시안 피부에서 흔함) | 분석 |
| 15 | `safety.uncommon[1]` | `/M8/safety/uncommon/1` | string | 색소탈실 (피부색이 하얗게 빠지는 현상) | 분석 |
| 16 | `safety.uncommon[2]` | `/M8/safety/uncommon/2` | string | 물집 형성 | 분석 |
| 17 | `safety.emergency` | `/M8/safety/emergency` | array | (array · 1) | —(컨테이너) |
| 18 | `safety.emergency[0]` | `/M8/safety/emergency/0` | string | 레이저 시술 중 피부가 심하게 하얗게 변하거나 검게 탄다면 즉시 시술 중단 | 분석 |
| 19 | `source` | `/M8/source` | string | 임상적 피부관리 44장 | 분석 |
| 20 | `name_en` | `/M8/name_en` | string | Laser & Light Therapy | 분석 |
| 21 | `overview` | `/M8/overview` | string | 레이저(LASER)는 '유도방출에 의한 빛의 증폭'이라는 뜻으로, 특정 파장의 강력한 빛을 피부에 쏘아 원하는 피부 문제만 골라서 치료하는 시술이다. 1960년대 처음 개발된 후 꾸준히 발전해, 현재는 색소(기미·점), 혈관(홍조), 주름, 흉터, 제모, 문신 제거 등 거의 모든 피부 문제에 다양한 종류의 레이저가 사용되고 있다. | 분석 |
| 22 | `aftercare` | `/M8/aftercare` | array | (array · 4) | —(컨테이너) |
| 23 | `aftercare[0]` | `/M8/aftercare/0` | string | 자외선 차단제 꼼꼼히 바르기 (시술 후 색소침착 예방에 가장 중요) | 분석 |
| 24 | `aftercare[1]` | `/M8/aftercare/1` | string | 시술 부위 딱지를 억지로 떼지 않기 | 분석 |
| 25 | `aftercare[2]` | `/M8/aftercare/2` | string | 보습 관리 철저히 하기 | 분석 |
| 26 | `aftercare[3]` | `/M8/aftercare/3` | string | 박피형 레이저 후에는 의사가 처방한 연고 사용 | 분석 |
| 27 | `mechanism` | `/M8/mechanism` | string | 레이저는 '선택광선열용해(특정 색소만 골라서 열로 파괴하는 원리)' 개념을 기반으로 작동한다. 피부 속 특정 표적(멜라닌 색소, 혈관의 헤모글로빈, 물 등)이 특정 파장의 빛을 흡수하면 열이 발생해 그 표적만 선택적으로 파괴된다. 이때 레이저 조사 시간을 표적의 열이완시간(열이 식는 데 걸리는 시간)보다 짧게 유지하면, 주위 정상 조직에는 열손상 없이 표적만 치료할 수 있다. 분획 레이저(프랙셔널)는 빛을 미세하게 쪼개서 피부에 미세한 열손상 구역을 만들고, 사이사이 정상 피부가 빠르게 회복을 도와 다운타임을 줄인 최신 기술이다. | 분석 |
| 28 | `indications` | `/M8/indications` | object | (object · 2) | —(컨테이너) |
| 29 | `indications.primary` | `/M8/indications/primary` | array | (array · 5) | —(컨테이너) |
| 30 | `indications.primary[0]` | `/M8/indications/primary/0` | string | 색소 병변 — 기미, 주근깨, 검버섯, 오타모반 등 | 분석 |
| 31 | `indications.primary[1]` | `/M8/indications/primary/1` | string | 혈관 병변 — 혈관종, 모세혈관확장증, 홍조 | 분석 |
| 32 | `indications.primary[2]` | `/M8/indications/primary/2` | string | 문신 제거 | 분석 |
| 33 | `indications.primary[3]` | `/M8/indications/primary/3` | string | 피부 재생/주름 개선 — 프랙셔널 레이저, CO₂ 레이저 | 분석 |
| 34 | `indications.primary[4]` | `/M8/indications/primary/4` | string | 제모 — 알렉산드라이트, 다이오드, Nd:YAG 레이저 | 분석 |
| 35 | `indications.extended` | `/M8/indications/extended` | array | (array · 7) | —(컨테이너) |
| 36 | `indications.extended[0]` | `/M8/indications/extended/0` | string | 여드름흉터 치료 | 분석 |
| 37 | `indications.extended[1]` | `/M8/indications/extended/1` | string | 피부 리서페이싱 (피부 표면을 새롭게 재생) | 분석 |
| 38 | `indications.extended[2]` | `/M8/indications/extended/2` | string | 넓은 모공 개선 | 분석 |
| 39 | `indications.extended[3]` | `/M8/indications/extended/3` | string | 여드름 치료 (PDT — 광역학요법과 병합) | 분석 |
| 40 | `indications.extended[4]` | `/M8/indications/extended/4` | string | 백반증, 건선 치료 (엑시머 레이저) | 분석 |
| 41 | `indications.extended[5]` | `/M8/indications/extended/5` | string | 창상 치유 촉진 (저출력 레이저) | 분석 |
| 42 | `indications.extended[6]` | `/M8/indications/extended/6` | string | 피부암 전구 병변 치료 (광선각화증 등) | 분석 |
| 43 | `source_type` | `/M8/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 44 | `extracted_at` | `/M8/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 45 | `procedure_id` | `/M8/procedure_id` | string | M8-LASER | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 46 | `onset_duration` | `/M8/onset_duration` | object | (object · 3) | —(컨테이너) |
| 47 | `onset_duration.peak` | `/M8/onset_duration/peak` | string | 프랙셔널 레이저의 경우 3~6개월에 걸쳐 콜라겐 리모델링으로 효과 극대화 | 분석 |
| 48 | `onset_duration.onset` | `/M8/onset_duration/onset` | string | 시술 종류에 따라 다름 — 색소 레이저는 1~2주 후 딱지 탈락 시, 프랙셔널은 1~3개월에 걸쳐 서서히 | 분석 |
| 49 | `onset_duration.duration` | `/M8/onset_duration/duration` | string | 색소/혈관 레이저는 병변 제거 시 반영구적, 피부 재생 레이저는 수개월~수년 (노화는 계속 진행되므로) | 분석 |
| 50 | `contraindications` | `/M8/contraindications` | object | (object · 2) | —(컨테이너) |
| 51 | `contraindications.absolute` | `/M8/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 52 | `contraindications.absolute[0]` | `/M8/contraindications/absolute/0` | string | 치료 부위에 활동성 감염이 있는 경우 | 분석 |
| 53 | `contraindications.absolute[1]` | `/M8/contraindications/absolute/1` | string | 광과민성 질환이 있는 경우 (빛에 과민하게 반응하는 질환) | 분석 |
| 54 | `contraindications.absolute[2]` | `/M8/contraindications/absolute/2` | string | 켈로이드 체질 (박피형 레이저 시) | 분석 |
| 55 | `contraindications.relative` | `/M8/contraindications/relative` | array | (array · 4) | —(컨테이너) |
| 56 | `contraindications.relative[0]` | `/M8/contraindications/relative/0` | string | 최근 과도한 자외선 노출이나 인공 태닝을 한 경우 (색소침착 위험 증가) | 분석 |
| 57 | `contraindications.relative[1]` | `/M8/contraindications/relative/1` | string | 임신 중이거나 수유 중일 때 | 분석 |
| 58 | `contraindications.relative[2]` | `/M8/contraindications/relative/2` | string | 이소트레티노인(여드름 치료제) 복용 후 6개월 이내 | 분석 |
| 59 | `contraindications.relative[3]` | `/M8/contraindications/relative/3` | string | 피부색이 어두운 경우 (색소침착·탈색 위험이 높아 파장·설정 주의 필요) | 분석 |
| 60 | `guardrail_version` | `/M8/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 61 | `related_techniques` | `/M8/related_techniques` | array | (array · 3) | —(컨테이너) |
| 62 | `related_techniques[0]` | `/M8/related_techniques/0` | string | IPL (Intense Pulsed Light) — 레이저와 비슷하지만 여러 파장의 빛을 동시에 사용 | 분석 |
| 63 | `related_techniques[1]` | `/M8/related_techniques/1` | string | 프랙셔널 레이저 — 기존 박피 레이저의 다운타임을 줄인 최신 기술 | 분석 |
| 64 | `related_techniques[2]` | `/M8/related_techniques/2` | string | PDT (광역학요법) — 광감작제 약물 + 레이저를 병합한 여드름/피부암 치료 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S16-01** (I) uncommon 그룹 값의 괄호에 「특히 아시안 피부에서 흔함」이 있다. 그룹(uncommon)과 하위 집단 빈도(흔함)가 한 값에서 다르다. → I9  
  근거: `/M8/safety/uncommon/0` 「특히 아시안 피부에서 흔함」
- **OB-S16-02** (F) 레이저 종류(색소·혈관·프랙셔널·CO₂·알렉산드라이트·다이오드·Nd:YAG·엑시머·저출력·박피형)마다 onset·duration·peak·금기가 조건부다. name 은 「레이저」, name_en 은 「Laser & Light Therapy」이고 related 의 IPL 은 「레이저와 비슷하지만」으로 구분한다. → F3, F11  
  근거: `/M8/onset_duration/onset` 「시술 종류에 따라 다름」; `/M8/name_en` 「Laser & Light Therapy」; `/M8/related_techniques/0` 「레이저와 비슷하지만」
- **OB-S16-03** (B) relative 「최근 과도한 자외선 노출」의 「최근」 기간이 없다. 같은 그룹의 이소트레티노인은 「복용 후 6개월 이내」로 기간이 있다. → B4  
  근거: `/M8/contraindications/relative/0` 「최근 과도한 자외선 노출」; `/M8/contraindications/relative/2` 「복용 후 6개월 이내」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX159 | negated_condition | `/M8/safety/serious/2` | 눈 손상 (보호안경 미착용 시) |  |
| MX160 | population_frequency | `/M8/safety/uncommon/0` | 특히 아시안 피부에서 흔함 | uncommon 칸 안의 「흔함」(I9) |
| MX161 | sign_condition_urgent_action | `/M8/safety/emergency/0` | 피부가 심하게 하얗게 변하거나 검게 탄다면 즉시 시술 중단 |  |
| MX162 | comparison_condition | `/M8/mechanism` | 레이저 조사 시간을 표적의 열이완시간(열이 식는 데 걸리는 시간)보다 짧게 유지하면 |  |
| MX163 | negated_statement | `/M8/mechanism` | 주위 정상 조직에는 열손상 없이 |  |
| MX164 | subtype_time | `/M8/onset_duration/onset` | 색소 레이저는 1~2주 후 딱지 탈락 시, 프랙셔널은 1~3개월에 걸쳐 서서히 |  |
| MX165 | causal | `/M8/onset_duration/duration` | (노화는 계속 진행되므로) |  |
| MX166 | time_vague_condition_risk | `/M8/contraindications/relative/0` | 최근 과도한 자외선 노출이나 인공 태닝을 한 경우 (색소침착 위험 증가) |  |
| MX167 | medication_time_window | `/M8/contraindications/relative/2` | 이소트레티노인(여드름 치료제) 복용 후 6개월 이내 |  |
| MX168 | subtype_condition | `/M8/contraindications/absolute/2` | 켈로이드 체질 (박피형 레이저 시) |  |
| MX169 | degree_scope | `/M8/overview` | 거의 모든 피부 문제에 |  |
| MX185 | historical_claim | `/M8/overview` | 1960년대 처음 개발된 후 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R16-1 | `/M8/related_techniques/2` | [14,18) | 광감작제 | 광/NNG + 감/NNG + 작/NNG + 제/XSN | 「광감작제」가 광/감/작/제 로 잘게 분절 | 약물 부류 명칭 소실 |
| R17-1 | `/M8/safety/serious/2` | [11,14) | 미착용 | 미/NNG + 착용/NNG | 부정 접두 「미」(미착용)를 명사(NNG)로 태깅 | 부정(착용하지 않음) 표지가 품사로 드러나지 않음 — 조건 「보호안경 미착용 시」의 부정이 형태소 기반 탐색에서 빠질 수 있음. 표현 후보 negation 규칙은 원문 문자열로 잡음 |

규칙 기반 표현 후보 312건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S16"` 에 있다. 후보이며 전수 의미 해석이 아니다.
