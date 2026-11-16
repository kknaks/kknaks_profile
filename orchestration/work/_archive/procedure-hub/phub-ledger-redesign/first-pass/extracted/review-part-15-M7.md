# S15 — `M7` (실리프팅) · extracted.json 1차 조사

> 구획 S15 · 소유 Pointer `/M7` 와 그 아래 65개 노드(말단 51). 문맥 참조: 루트 `""`, `/M7/name`, `/M7/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 5 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M7)` | `/M7` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M7/name` | string | 실리프팅 | 분석 |
| 3 | `safety` | `/M7/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M7/safety/common` | array | (array · 4) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M7/safety/common/0` | string | 시술 부위 통증 및 뻣뻣한 느낌 | 분석 |
| 6 | `safety.common[1]` | `/M7/safety/common/1` | string | 붓기 | 분석 |
| 7 | `safety.common[2]` | `/M7/safety/common/2` | string | 멍 | 분석 |
| 8 | `safety.common[3]` | `/M7/safety/common/3` | string | 딤플링 (피부 표면이 울퉁불퉁해지는 현상) | 분석 |
| 9 | `safety.serious` | `/M7/safety/serious` | array | (array · 5) | —(컨테이너) |
| 10 | `safety.serious[0]` | `/M7/safety/serious/0` | string | 안면신경 일시적 마비 (드물게 발생, 대부분 회복됨) | 분석 |
| 11 | `safety.serious[1]` | `/M7/safety/serious/1` | string | 안면신경 영구 손상 (극히 드묾) | 분석 |
| 12 | `safety.serious[2]` | `/M7/safety/serious/2` | string | 감각신경 손상 (대이개신경 손상) | 분석 |
| 13 | `safety.serious[3]` | `/M7/safety/serious/3` | string | 감염 | 분석 |
| 14 | `safety.serious[4]` | `/M7/safety/serious/4` | string | 침샘 관통 (이하선 손상) | 분석 |
| 15 | `safety.uncommon` | `/M7/safety/uncommon` | array | (array · 5) | —(컨테이너) |
| 16 | `safety.uncommon[0]` | `/M7/safety/uncommon/0` | string | 피부 주름 (skin fold) 형성 | 분석 |
| 17 | `safety.uncommon[1]` | `/M7/safety/uncommon/1` | string | 삽입 지점 볼록함 | 분석 |
| 18 | `safety.uncommon[2]` | `/M7/safety/uncommon/2` | string | 실이 피부 밖으로 튀어나오는 현상 | 분석 |
| 19 | `safety.uncommon[3]` | `/M7/safety/uncommon/3` | string | 실의 이동 (원래 위치에서 움직이는 것) | 분석 |
| 20 | `safety.uncommon[4]` | `/M7/safety/uncommon/4` | string | 불만족스러운 결과 | 분석 |
| 21 | `source` | `/M7/source` | string | The Art and Science of Thread Lifting (2nd Ed., Oh/Hong/Song, Springer 2024) | 분석 |
| 22 | `name_en` | `/M7/name_en` | string | Thread Lifting | 분석 |
| 23 | `overview` | `/M7/overview` | string | 실리프팅은 체내에서 녹는 특수한 실(thread)을 피부 아래에 삽입해서 처진 피부를 물리적으로 당겨 올리는 비수술적 리프팅 시술이다. 2000년대 초반부터 인기를 얻기 시작했으며, 필러나 보톡스만으로는 한계가 있는 얼굴 하부(볼, 턱선, 팔자주름) 처짐 교정에 주로 사용된다. 코그실(톱니 모양 실)과 모노실(매끈한 실) 등 다양한 종류가 있다. | 분석 |
| 24 | `aftercare` | `/M7/aftercare` | array | (array · 3) | —(컨테이너) |
| 25 | `aftercare[0]` | `/M7/aftercare/0` | string | 시술 후 2~4주간 입을 크게 벌리거나 과도한 표정 짓기 피하기 | 분석 |
| 26 | `aftercare[1]` | `/M7/aftercare/1` | string | 시술 부위를 강하게 누르거나 마사지하지 않기 | 분석 |
| 27 | `aftercare[2]` | `/M7/aftercare/2` | string | 시술 후 1주일간 격렬한 운동, 사우나 피하기 | 분석 |
| 28 | `mechanism` | `/M7/mechanism` | string | 실리프팅은 크게 네 가지 기전으로 작용한다. 첫째, 보강 효과(reinforcement effect)로 실이 약해진 피부 조직을 물리적으로 지지해준다. 둘째, 스캐폴드 효과(scaffold effect)로 실 주변에 새로운 콜라겐이 형성되어 피부 구조를 강화한다. 셋째, 코그실(톱니실)의 경우 직접적인 리프팅 효과로 처진 조직을 위로 당겨 올린다. 넷째, 조직학적 효과로 실이 삽입된 후 시간이 지나면서 주변에 콜라겐 재생과 조직 리모델링이 일어난다. PDO(폴리디옥사논), PLLA, PCL 등 흡수성 실 소재는 체내에서 서서히 녹으면서 콜라겐 생성을 촉진한다. | 분석 |
| 29 | `indications` | `/M7/indications` | object | (object · 2) | —(컨테이너) |
| 30 | `indications.primary` | `/M7/indications/primary` | array | (array · 4) | —(컨테이너) |
| 31 | `indications.primary[0]` | `/M7/indications/primary/0` | string | 얼굴 하부 처짐 (볼, 턱선이 내려앉은 것) | 분석 |
| 32 | `indications.primary[1]` | `/M7/indications/primary/1` | string | 팔자주름 (코입술주름) 개선 | 분석 |
| 33 | `indications.primary[2]` | `/M7/indications/primary/2` | string | 마리오네트 라인 (입꼬리에서 턱으로 내려가는 주름) 개선 | 분석 |
| 34 | `indications.primary[3]` | `/M7/indications/primary/3` | string | 턱선 리프팅 (이중턱, 불분명한 턱선) | 분석 |
| 35 | `indications.extended` | `/M7/indications/extended` | array | (array · 7) | —(컨테이너) |
| 36 | `indications.extended[0]` | `/M7/indications/extended/0` | string | 눈썹 리프팅 (처진 눈썹 올리기) | 분석 |
| 37 | `indications.extended[1]` | `/M7/indications/extended/1` | string | 관자놀이 리프팅 | 분석 |
| 38 | `indications.extended[2]` | `/M7/indications/extended/2` | string | 볼 리프팅 (광대뼈 아래 처짐 교정) | 분석 |
| 39 | `indications.extended[3]` | `/M7/indications/extended/3` | string | 목 리프팅 | 분석 |
| 40 | `indications.extended[4]` | `/M7/indications/extended/4` | string | 이마/미간 주름 개선 (모노실) | 분석 |
| 41 | `indications.extended[5]` | `/M7/indications/extended/5` | string | 눈가 주름 개선 (모노실) | 분석 |
| 42 | `indications.extended[6]` | `/M7/indications/extended/6` | string | 코 리프팅 (코끝 올리기) | 분석 |
| 43 | `source_type` | `/M7/source_type` | string | us | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 44 | `extracted_at` | `/M7/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 45 | `procedure_id` | `/M7/procedure_id` | string | M7-THREADLIFT | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 46 | `onset_duration` | `/M7/onset_duration` | object | (object · 3) | —(컨테이너) |
| 47 | `onset_duration.peak` | `/M7/onset_duration/peak` | string | 1~3개월 후 콜라겐 재생으로 효과 극대화 | 분석 |
| 48 | `onset_duration.onset` | `/M7/onset_duration/onset` | string | 시술 직후 리프팅 효과 확인 가능 | 분석 |
| 49 | `onset_duration.duration` | `/M7/onset_duration/duration` | string | 코그실 6~18개월, 모노실 6~12개월 (실 소재와 종류에 따라 다름) | 분석 |
| 50 | `contraindications` | `/M7/contraindications` | object | (object · 2) | —(컨테이너) |
| 51 | `contraindications.absolute` | `/M7/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 52 | `contraindications.absolute[0]` | `/M7/contraindications/absolute/0` | string | 시술 부위에 활동성 감염이나 염증이 있는 경우 | 분석 |
| 53 | `contraindications.absolute[1]` | `/M7/contraindications/absolute/1` | string | 실 소재(PDO, PLLA 등)에 알레르기가 있는 경우 | 분석 |
| 54 | `contraindications.absolute[2]` | `/M7/contraindications/absolute/2` | string | 켈로이드 체질 | 분석 |
| 55 | `contraindications.relative` | `/M7/contraindications/relative` | array | (array · 5) | —(컨테이너) |
| 56 | `contraindications.relative[0]` | `/M7/contraindications/relative/0` | string | 임신 중이거나 수유 중일 때 | 분석 |
| 57 | `contraindications.relative[1]` | `/M7/contraindications/relative/1` | string | 혈액 응고 장애가 있거나 항응고제 복용 중인 경우 | 분석 |
| 58 | `contraindications.relative[2]` | `/M7/contraindications/relative/2` | string | 이전 골 수술이나 안면 수술 이력이 있는 경우 의사와 상의 | 분석 |
| 59 | `contraindications.relative[3]` | `/M7/contraindications/relative/3` | string | 심한 여드름 흉터가 있는 부위 | 분석 |
| 60 | `contraindications.relative[4]` | `/M7/contraindications/relative/4` | string | 이전 리프팅 시술 이력이 있는 경우 | 분석 |
| 61 | `guardrail_version` | `/M7/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 62 | `related_techniques` | `/M7/related_techniques` | array | (array · 3) | —(컨테이너) |
| 63 | `related_techniques[0]` | `/M7/related_techniques/0` | string | 필러 -- 볼륨 부족한 부위에 병합 시술 | 분석 |
| 64 | `related_techniques[1]` | `/M7/related_techniques/1` | string | 보톡스 -- 근육성 주름에 병합 가능 | 분석 |
| 65 | `related_techniques[2]` | `/M7/related_techniques/2` | string | 고주파(RF)/HIFU -- 피부 타이트닝과 시너지 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S15-01** (구조) source 가 외부 단행본 서지(저자·판·출판사·연도)이고 source_type 이 이 원장에서 유일하게 us 다. → B9  
  근거: `/M7/source` 「The Art and Science of Thread Lifting (2nd Ed., Oh/Hong/Song, Springer 2024)」; `/M7/source_type` 「us」
- **OB-S15-02** (F) 실 하위 유형(코그실·모노실)과 소재(PDO·PLLA·PCL)가 overview·mechanism·indications·duration 에 나온다. indications 일부는 「(모노실)」 조건부, duration 은 유형별 기간이다. 코그실 풀이도 「톱니 모양 실」(overview)과 「톱니실」(mechanism)로 다르다. → F3, F7  
  근거: `/M7/onset_duration/duration` 「코그실 6~18개월, 모노실 6~12개월」; `/M7/indications/extended/4` 「(모노실)」; `/M7/overview` 「코그실(톱니 모양 실)」; `/M7/mechanism` 「코그실(톱니실)」
- **OB-S15-03** (P) serious 의 신경 손상이 두 값으로 나뉜다 — 일시적 마비(드물게, 대부분 회복)와 영구 손상(극히 드묾). 지속성(일시적·영구)과 빈도·경과가 함께 붙는다. uncommon 「불만족스러운 결과」는 사건이 아니라 결과 평가다. → F4, I6  
  근거: `/M7/safety/serious/0` 「드물게 발생, 대부분 회복됨」; `/M7/safety/serious/1` 「영구 손상 (극히 드묾)」; `/M7/safety/uncommon/4` 「불만족스러운 결과」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX150 | frequency_course_scoped | `/M7/safety/serious/0` | 안면신경 일시적 마비 (드물게 발생, 대부분 회복됨) |  |
| MX151 | frequency_duration_scoped | `/M7/safety/serious/1` | 안면신경 영구 손상 (극히 드묾) |  |
| MX152 | comparison_limit_site | `/M7/overview` | 필러나 보톡스만으로는 한계가 있는 얼굴 하부(볼, 턱선, 팔자주름) 처짐 교정 |  |
| MX153 | subtype_condition | `/M7/mechanism` | 코그실(톱니실)의 경우 직접적인 리프팅 효과 |  |
| MX154 | time_window_avoidance | `/M7/aftercare/0` | 시술 후 2~4주간 입을 크게 벌리거나 과도한 표정 짓기 피하기 |  |
| MX155 | time_window_avoidance | `/M7/aftercare/2` | 시술 후 1주일간 격렬한 운동, 사우나 피하기 |  |
| MX156 | subtype_time | `/M7/onset_duration/duration` | 코그실 6~18개월, 모노실 6~12개월 (실 소재와 종류에 따라 다름) |  |
| MX157 | subtype_condition | `/M7/indications/extended/4` | 이마/미간 주름 개선 (모노실) |  |
| MX158 | history_condition_obligation | `/M7/contraindications/relative/2` | 이전 골 수술이나 안면 수술 이력이 있는 경우 의사와 상의 |  |
| MX186 | historical_claim | `/M7/overview` | 2000년대 초반부터 인기를 얻기 시작했으며 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R01-2 | `/M7/indications/primary/3` | [8,11) | 이중턱 | 이/MM + 중턱/NNG | 관형사 「이」 오분리 — 부위어가 MM+다른 명사로 쪼개짐 | 부위 표현 탐색 시 「이중턱」「이마」가 「중턱」「마」로 바뀜. 형태소 기반 부위 후보 추출에서 누락·오탐 |
| R03-1 | `/M7/safety/serious/2` | [9,14) | 대이개신경 | 대/XPN + 이/NR + 개/NNB + 신경/NNG | 전문 해부 용어 「대이개신경」 분절 오류(대/XPN+이/NR+개/NNB) | 수사·단위명사로 오인 — 신경 명칭 소실, 수량 후보 오탐 가능 |
| R11-6 | `/M7/safety/common/2` | [0,1) | 멍 | 멍/MAG | 단독 값 「멍」(타박 멍)을 부사(MAG)로 태깅 | 부작용 사건 명사가 부사로 분류 — 품사로 사건 명사를 고르면 누락. 값 자체는 원문 보존 |
| R18-1 | `/M7/safety/common/3` | [0,3) | 딤플링 | 딤플/NNG + 링/NNG | 외래어 장비·현상 용어가 두 명사로 분절(딤플링·쿨링) | 용어 식별 실패(영향 작음) |

규칙 기반 표현 후보 263건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S15"` 에 있다. 후보이며 전수 의미 해석이 아니다.
