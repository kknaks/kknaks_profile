# S17 — `M9` (기기리프팅) · extracted.json 1차 조사

> 구획 S17 · 소유 Pointer `/M9` 와 그 아래 57개 노드(말단 43). 문맥 참조: 루트 `""`, `/M9/name`, `/M9/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 6 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M9)` | `/M9` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M9/name` | string | 기기리프팅 | 분석 |
| 3 | `safety` | `/M9/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M9/safety/common` | array | (array · 2) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M9/safety/common/0` | string | 시술 후 홍반 (빨개짐) -- 대부분 수 시간 내 사라짐 | 분석 |
| 6 | `safety.common[1]` | `/M9/safety/common/1` | string | 부종 (붓기) -- 경우에 따라 2~3일 지속 | 분석 |
| 7 | `safety.serious` | `/M9/safety/serious` | array | (array · 3) | —(컨테이너) |
| 8 | `safety.serious[0]` | `/M9/safety/serious/0` | string | 흉터 (과도한 에너지로 인한 진피 손상) | 분석 |
| 9 | `safety.serious[1]` | `/M9/safety/serious/1` | string | 피부위축 (수 주~수 개월 후, 특히 단극성 장비에서 지방층 경계면의 과도한 열 작용 시) | 분석 |
| 10 | `safety.serious[2]` | `/M9/safety/serious/2` | string | 심한 함몰이나 흉터는 진피하 절제술, 지방이식, 필러 등으로 교정 필요 | 분석 |
| 11 | `safety.uncommon` | `/M9/safety/uncommon` | array | (array · 3) | —(컨테이너) |
| 12 | `safety.uncommon[0]` | `/M9/safety/uncommon/0` | string | 수포 (너무 높은 에너지 사용 시 물집) | 분석 |
| 13 | `safety.uncommon[1]` | `/M9/safety/uncommon/1` | string | 화상 (부적절한 쿨링 시) | 분석 |
| 14 | `safety.uncommon[2]` | `/M9/safety/uncommon/2` | string | 색소침착 (시술 부위가 어두워지는 현상) | 분석 |
| 15 | `source` | `/M9/source` | string | 임상적 피부관리 27장 (고주파치료법) | 분석 |
| 16 | `name_en` | `/M9/name_en` | string | Device-based Lifting (RF / HIFU) | 분석 |
| 17 | `overview` | `/M9/overview` | string | 기기리프팅은 고주파(RF, Radiofrequency)나 고강도 집속 초음파(HIFU) 등의 에너지를 피부에 전달해서 콜라겐을 수축시키고 새로운 콜라겐 생성을 유도하는 비침습적(피부를 찌르지 않는) 리프팅 시술이다. 한국에서는 '써마지', '울쎄라', '슈링크', '올리지오' 등의 브랜드명으로 잘 알려져 있다. | 분석 |
| 18 | `aftercare` | `/M9/aftercare` | array | (array · 3) | —(컨테이너) |
| 19 | `aftercare[0]` | `/M9/aftercare/0` | string | 시술 후 세안, 샤워, 화장 등 일상생활에 지장 없음 | 분석 |
| 20 | `aftercare[1]` | `/M9/aftercare/1` | string | 시술이 끝나면 차가운 마스크나 팩으로 진정 | 분석 |
| 21 | `aftercare[2]` | `/M9/aftercare/2` | string | 진정 후 보습제와 썬크림으로 마무리 | 분석 |
| 22 | `mechanism` | `/M9/mechanism` | string | 고주파 전류를 인체 조직에 가하면 진동 폭이 매우 짧기 때문에 이온 운동이 거의 일어나지 않으며, 전류의 경로 안에서 열에너지로 변환되어 심부열을 발생시킨다. 다른 전류 형태와 달리 감각신경 및 운동신경을 자극하지 않아, 근육수축을 일으키지 않으면서 신체 조직 안의 특정 부위를 가열할 수 있다. 생체 열에너지로 변환된 고주파에너지는 조직의 온도를 상승시켜 세포의 기능을 증진시키고 혈류량을 증가시키며, 섬유모세포를 자극하여 새로운 콜라겐과 엘라스틴이 생성되어 피부의 탄력이 증가되고 주름이 개선된다. 초기에 콜라겐이 수축되는 현상이 나타나고, 시간이 지나면서 새로운 콜라겐들이 합성되어 치료효과가 나타난다. | 분석 |
| 23 | `indications` | `/M9/indications` | object | (object · 2) | —(컨테이너) |
| 24 | `indications.primary` | `/M9/indications/primary` | array | (array · 3) | —(컨테이너) |
| 25 | `indications.primary[0]` | `/M9/indications/primary/0` | string | 피부 탄력 저하 (늘어진 피부 타이트닝) | 분석 |
| 26 | `indications.primary[1]` | `/M9/indications/primary/1` | string | 리프팅 (처진 볼살, 턱선 리프팅) | 분석 |
| 27 | `indications.primary[2]` | `/M9/indications/primary/2` | string | 주름 개선 (잔주름뿐만 아니라 굵은 주름도) | 분석 |
| 28 | `indications.extended` | `/M9/indications/extended` | array | (array · 5) | —(컨테이너) |
| 29 | `indications.extended[0]` | `/M9/indications/extended/0` | string | 피부톤 개선 (고르게 밝아지는 효과) | 분석 |
| 30 | `indications.extended[1]` | `/M9/indications/extended/1` | string | 흉터 개선 (여드름 흉터 등 콜라겐 재구성) | 분석 |
| 31 | `indications.extended[2]` | `/M9/indications/extended/2` | string | 여드름 개선 (피지선에 작용) | 분석 |
| 32 | `indications.extended[3]` | `/M9/indications/extended/3` | string | 셀룰라이트 개선 | 분석 |
| 33 | `indications.extended[4]` | `/M9/indications/extended/4` | string | 모공 축소 | 분석 |
| 34 | `source_type` | `/M9/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 35 | `extracted_at` | `/M9/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 36 | `procedure_id` | `/M9/procedure_id` | string | M9-DEVICELIFT | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 37 | `onset_duration` | `/M9/onset_duration` | object | (object · 3) | —(컨테이너) |
| 38 | `onset_duration.peak` | `/M9/onset_duration/peak` | string | 1~3개월 후 새로운 콜라겐 합성으로 효과 극대화 | 분석 |
| 39 | `onset_duration.onset` | `/M9/onset_duration/onset` | string | 시술 직후 콜라겐 수축에 의한 즉각적 타이트닝 효과 | 분석 |
| 40 | `onset_duration.duration` | `/M9/onset_duration/duration` | string | 6~12개월 유지 (장비와 에너지 강도에 따라 다름) | 분석 |
| 41 | `contraindications` | `/M9/contraindications` | object | (object · 2) | —(컨테이너) |
| 42 | `contraindications.absolute` | `/M9/contraindications/absolute` | array | (array · 4) | —(컨테이너) |
| 43 | `contraindications.absolute[0]` | `/M9/contraindications/absolute/0` | string | 체내에 금속 악세사리나 임플란트가 있는 부위 | 분석 |
| 44 | `contraindications.absolute[1]` | `/M9/contraindications/absolute/1` | string | 심장박동기(페이스메이커) 사용자 | 분석 |
| 45 | `contraindications.absolute[2]` | `/M9/contraindications/absolute/2` | string | 방사선 치료 중인 사람 | 분석 |
| 46 | `contraindications.absolute[3]` | `/M9/contraindications/absolute/3` | string | 악성종양을 치료 중인 사람 | 분석 |
| 47 | `contraindications.relative` | `/M9/contraindications/relative` | array | (array · 4) | —(컨테이너) |
| 48 | `contraindications.relative[0]` | `/M9/contraindications/relative/0` | string | 고혈압 환자 | 분석 |
| 49 | `contraindications.relative[1]` | `/M9/contraindications/relative/1` | string | 임산부, 생리 중인 사람 | 분석 |
| 50 | `contraindications.relative[2]` | `/M9/contraindications/relative/2` | string | 금속 물질을 몸 안에 착용한 경우 (금속 제거 후 시술) | 분석 |
| 51 | `contraindications.relative[3]` | `/M9/contraindications/relative/3` | string | 피부가 얇은 부위 (이마, 관자놀이 등)는 조심해서 시술 | 분석 |
| 52 | `guardrail_version` | `/M9/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 53 | `related_techniques` | `/M9/related_techniques` | array | (array · 4) | —(컨테이너) |
| 54 | `related_techniques[0]` | `/M9/related_techniques/0` | string | 실리프팅 -- 물리적 리프팅과 기기 타이트닝 병합 | 분석 |
| 55 | `related_techniques[1]` | `/M9/related_techniques/1` | string | 보톡스 -- 근육성 주름에 병합 | 분석 |
| 56 | `related_techniques[2]` | `/M9/related_techniques/2` | string | 필러 -- 볼륨 부족 부위에 병합 | 분석 |
| 57 | `related_techniques[3]` | `/M9/related_techniques/3` | string | IPL/레이저 -- 색소, 혈관 치료와 병합 시 시너지 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S17-01** (I) absolute 「체내에 금속 악세사리나 임플란트가 있는 부위」와 relative 「금속 물질을 몸 안에 착용한 경우 (금속 제거 후 시술)」가 같은 조건을 두 등급에 둔다. → I5  
  근거: `/M9/contraindications/absolute/0` 「금속 악세사리나 임플란트가 있는 부위」; `/M9/contraindications/relative/2` 「금속 물질을 몸 안에 착용한 경우」
- **OB-S17-02** (B) name_en·overview 는 RF 와 HIFU 를 함께 들지만 mechanism 은 고주파(RF)만 설명한다. HIFU 기전은 이 항목에 없다. → B3  
  근거: `/M9/name_en` 「(RF / HIFU)」; `/M9/mechanism` 「고주파 전류를 인체 조직에 가하면」
- **OB-S17-03** (I) serious 셋째 값은 사건이 아니라 교정 방법(진피하 절제술·지방이식·필러)이다. → I6  
  근거: `/M9/safety/serious/2` 「교정 필요」
- **OB-S17-04** (P) relative 넷째 값의 「얇은」은 피부 두께(부위 성질)이고 「조심해서 시술」은 시술 방식 권고다. 금기 조건과 시술 주의가 한 값에 있다. serious 「피부위축」은 시점(수 주~수 개월 후)·장비(단극성)·조건(과도한 열 작용)을 함께 단다. → I8, F4  
  근거: `/M9/contraindications/relative/3` 「피부가 얇은 부위 (이마, 관자놀이 등)는 조심해서 시술」; `/M9/safety/serious/1` 「특히 단극성 장비에서」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX170 | course_frequency_time | `/M9/safety/common/0` | 대부분 수 시간 내 사라짐 |  |
| MX171 | condition_time | `/M9/safety/common/1` | 경우에 따라 2~3일 지속 |  |
| MX172 | time_subtype_condition | `/M9/safety/serious/1` | (수 주~수 개월 후, 특히 단극성 장비에서 지방층 경계면의 과도한 열 작용 시) |  |
| MX173 | management_in_safety | `/M9/safety/serious/2` | 심한 함몰이나 흉터는 진피하 절제술, 지방이식, 필러 등으로 교정 필요 | safety 칸이 교정 방법 진술(I6) |
| MX174 | degree_condition | `/M9/safety/uncommon/0` | (너무 높은 에너지 사용 시 물집) |  |
| MX175 | negated_statement | `/M9/mechanism` | 감각신경 및 운동신경을 자극하지 않아, 근육수축을 일으키지 않으면서 |  |
| MX176 | scope_inclusion | `/M9/indications/primary/2` | 잔주름뿐만 아니라 굵은 주름도 |  |
| MX177 | time_with_condition | `/M9/onset_duration/duration` | 6~12개월 유지 (장비와 에너지 강도에 따라 다름) |  |
| MX178 | condition_with_remedy | `/M9/contraindications/relative/2` | 금속 물질을 몸 안에 착용한 경우 (금속 제거 후 시술) | absolute/0 과 겹침(I5) |
| MX179 | thickness_site_caution | `/M9/contraindications/relative/3` | 피부가 얇은 부위 (이마, 관자놀이 등)는 조심해서 시술 | 「얇은」 = 피부 두께 |
| MX189 | negated_prefix_gloss | `/M9/overview` | 비침습적(피부를 찌르지 않는) |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R12-1 | `/M9/safety/serious/2` | [12,15) | 진피하 | 진/NNG + 피하/NNG | 「진피하」(진피 아래)를 진/NNG + 피하/NNG 로 분절 | 「진피하 절제술」이 「진」+「피하(피하조직)」로 바뀌어 층위(진피 vs 피하) 의미가 뒤바뀔 수 있음 |
| R18-2 | `/M9/safety/uncommon/1` | [9,11) | 쿨링 | 쿨/NNG + 링/NNG | 외래어 장비·현상 용어가 두 명사로 분절(딤플링·쿨링) | 용어 식별 실패(영향 작음) |

규칙 기반 표현 후보 236건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S17"` 에 있다. 후보이며 전수 의미 해석이 아니다.
