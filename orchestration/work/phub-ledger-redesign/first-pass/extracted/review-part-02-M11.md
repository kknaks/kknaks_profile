# S02 — `M11` (니들RF) · extracted.json 1차 조사

> 구획 S02 · 소유 Pointer `/M11` 와 그 아래 53개 노드(말단 39). 문맥 참조: 루트 `""`, `/M11/name`, `/M11/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 1 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M11)` | `/M11` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M11/name` | string | 니들RF | 분석 |
| 3 | `safety` | `/M11/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M11/safety/common` | array | (array · 3) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M11/safety/common/0` | string | 시술 부위 홍반 (빨개짐) | 분석 |
| 6 | `safety.common[1]` | `/M11/safety/common/1` | string | 약간의 붓기 | 분석 |
| 7 | `safety.common[2]` | `/M11/safety/common/2` | string | 시술 부위 따끔거림 | 분석 |
| 8 | `safety.serious` | `/M11/safety/serious` | array | (array · 2) | —(컨테이너) |
| 9 | `safety.serious[0]` | `/M11/safety/serious/0` | string | 감염 (1회용 팁 사용으로 위생 관리) | 분석 |
| 10 | `safety.serious[1]` | `/M11/safety/serious/1` | string | 드물게 화상 (부적절한 에너지 설정 시) | 분석 |
| 11 | `safety.uncommon` | `/M11/safety/uncommon` | array | (array · 2) | —(컨테이너) |
| 12 | `safety.uncommon[0]` | `/M11/safety/uncommon/0` | string | 색소침착 (박피나 레이저 시술에 비해 위험이 매우 작음) | 분석 |
| 13 | `safety.uncommon[1]` | `/M11/safety/uncommon/1` | string | 일시적 건조함 | 분석 |
| 14 | `source` | `/M11/source` | string | 임상적 피부관리 28장 (인트라셀 Fractional RF Microneedle) | 분석 |
| 15 | `name_en` | `/M11/name_en` | string | Microneedle Radiofrequency (MNRF) | 분석 |
| 16 | `overview` | `/M11/overview` | string | 니들RF는 미세침(마이크로니들)을 피부에 삽입하면서 동시에 고주파(RF) 에너지를 전달하는 시술이다. 한국에서는 '인트라셀', '포텐자', '시크릿', '스카렛' 등의 브랜드명으로 알려져 있다. 비박피성 피부재생 장비와 프랙셔널 레이저의 장점을 합쳐, 진피층에 직접 에너지를 전달하면서도 표피 손상은 최소화하는 것이 특징이다. | 분석 |
| 17 | `aftercare` | `/M11/aftercare` | array | (array · 3) | —(컨테이너) |
| 18 | `aftercare[0]` | `/M11/aftercare/0` | string | 시술 후에 보이는 딱지가 없으므로 일상생활에 지장 없음 | 분석 |
| 19 | `aftercare[1]` | `/M11/aftercare/1` | string | 시술 후 자외선 차단제 꼼꼼히 바르기 | 분석 |
| 20 | `aftercare[2]` | `/M11/aftercare/2` | string | 보습제를 충분히 발라주기 | 분석 |
| 21 | `mechanism` | `/M11/mechanism` | string | 니들RF는 특수 제작된 절연 마이크로니들을 순간적으로 피부에 삽입하여 치료 기둥을 만들며, 동시에 고압 펄스의 고주파를 이용한 국소적인 열손상을 통해 시술 범위 중 원하는 목표 부위에만 약 20%의 면적에 피부재생을 촉진하는 미세한 상처들을 만들어 세포의 성장인자를 유도하여 피부의 자연치유를 극대화한다. 레이저와 같이 표피를 에너지 전달통로로 사용하는 방식이 아니므로, 박피성 시술 시 발생하는 색소침착 등의 부작용이 없고, 바늘 끝을 통해 물리적으로 진피 내에 직접 미세상처를 줄 뿐만 아니라 고주파를 이용한 진피 내의 전반적인 열손상을 통해 콜라겐 리모델링을 유도하여 피부재생에 효과를 가져온다. | 분석 |
| 22 | `indications` | `/M11/indications` | object | (object · 2) | —(컨테이너) |
| 23 | `indications.primary` | `/M11/indications/primary` | array | (array · 3) | —(컨테이너) |
| 24 | `indications.primary[0]` | `/M11/indications/primary/0` | string | 흉터 및 피부재생 (여드름 흉터, 수술 흉터 등) | 분석 |
| 25 | `indications.primary[1]` | `/M11/indications/primary/1` | string | 리프팅/타이트닝 (피부 처짐 개선) | 분석 |
| 26 | `indications.primary[2]` | `/M11/indications/primary/2` | string | 미백 및 피부결 개선 | 분석 |
| 27 | `indications.extended` | `/M11/indications/extended` | array | (array · 5) | —(컨테이너) |
| 28 | `indications.extended[0]` | `/M11/indications/extended/0` | string | 여드름 치료 (활동성 여드름) | 분석 |
| 29 | `indications.extended[1]` | `/M11/indications/extended/1` | string | 기미, 색소침착 개선 | 분석 |
| 30 | `indications.extended[2]` | `/M11/indications/extended/2` | string | 잡티 개선 | 분석 |
| 31 | `indications.extended[3]` | `/M11/indications/extended/3` | string | 모공 축소 | 분석 |
| 32 | `indications.extended[4]` | `/M11/indications/extended/4` | string | 튼살 (배, 허벅지 등) | 분석 |
| 33 | `source_type` | `/M11/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 34 | `extracted_at` | `/M11/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 35 | `procedure_id` | `/M11/procedure_id` | string | M11-NEEDLERF | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 36 | `onset_duration` | `/M11/onset_duration` | object | (object · 3) | —(컨테이너) |
| 37 | `onset_duration.peak` | `/M11/onset_duration/peak` | string | 1~3개월 후 콜라겐 리모델링 효과 최대 | 분석 |
| 38 | `onset_duration.onset` | `/M11/onset_duration/onset` | string | 시술 후 1~2주부터 피부결 개선 체감 | 분석 |
| 39 | `onset_duration.duration` | `/M11/onset_duration/duration` | string | 6~12개월 유지 (반복 시술 시 효과 누적) | 분석 |
| 40 | `contraindications` | `/M11/contraindications` | object | (object · 2) | —(컨테이너) |
| 41 | `contraindications.absolute` | `/M11/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 42 | `contraindications.absolute[0]` | `/M11/contraindications/absolute/0` | string | 시술 부위에 활동성 감염이 있는 경우 | 분석 |
| 43 | `contraindications.absolute[1]` | `/M11/contraindications/absolute/1` | string | 심장박동기(페이스메이커) 사용자 | 분석 |
| 44 | `contraindications.absolute[2]` | `/M11/contraindications/absolute/2` | string | 체내 금속 임플란트가 있는 부위 | 분석 |
| 45 | `contraindications.relative` | `/M11/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 46 | `contraindications.relative[0]` | `/M11/contraindications/relative/0` | string | 켈로이드 체질 (단, 일반적인 니들RF는 켈로이드 위험이 낮음) | 분석 |
| 47 | `contraindications.relative[1]` | `/M11/contraindications/relative/1` | string | 임신 중이거나 수유 중인 경우 | 분석 |
| 48 | `contraindications.relative[2]` | `/M11/contraindications/relative/2` | string | 혈액 응고 장애가 있는 경우 | 분석 |
| 49 | `guardrail_version` | `/M11/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 50 | `related_techniques` | `/M11/related_techniques` | array | (array · 3) | —(컨테이너) |
| 51 | `related_techniques[0]` | `/M11/related_techniques/0` | string | 프랙셔널 레이저 -- 비슷한 피부 재생 원리이나 표피 손상이 더 큼 | 분석 |
| 52 | `related_techniques[1]` | `/M11/related_techniques/1` | string | 일반 고주파(RF) -- 비침습적 타이트닝 | 분석 |
| 53 | `related_techniques[2]` | `/M11/related_techniques/2` | string | MTS(마이크로니들링) -- RF 없이 물리적 자극만으로 콜라겐 유도 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S02-01** (I) mechanism 은 「박피성 시술 시 발생하는 색소침착 등의 부작용이 없고」라 했지만 safety/uncommon 에 「색소침착」이 있다(괄호로 위험이 매우 작다고 단서). 「없음」과 「드묾」이 한 항목 안에서 다르다. → I3  
  근거: `/M11/mechanism` 「색소침착 등의 부작용이 없고」; `/M11/safety/uncommon/0` 「색소침착 (박피나 레이저 시술에 비해 위험이 매우 작음)」
- **OB-S02-02** (P) serious 「드물게 화상」에는 빈도어(드물게)와 조건(부적절한 에너지 설정 시)이 함께 있다. 「감염」의 괄호는 사건 설명이 아니라 예방 방법이다. → F4  
  근거: `/M11/safety/serious/1` 「드물게 화상」; `/M11/safety/serious/0` 「1회용 팁 사용으로 위생 관리」
- **OB-S02-03** (F) mechanism 의 「약 20%의 면적」은 「시술 범위 중 원하는 목표 부위」를 분모로 한 면적 비율로 적혀 있다. 환자 비율이 아니다. → F10  
  근거: `/M11/mechanism` 「목표 부위에만 약 20%의 면적에」
- **OB-S02-04** (B) source 는 「임상적 피부관리 28장 (인트라셀 Fractional RF Microneedle)」으로 장 번호와 장 주제만 있다. 판·저자·쪽은 없다. overview 의 브랜드명(인트라셀·포텐자·시크릿·스카렛)은 원문이 「브랜드명」이라 적었다. → B7  
  근거: `/M11/source` 「임상적 피부관리 28장」; `/M11/overview` 「'인트라셀', '포텐자', '시크릿', '스카렛' 등의 브랜드명」
- **OB-S02-05** (P) relative 「켈로이드 체질 (단, 일반적인 니들RF는 켈로이드 위험이 낮음)」은 금기 조건 + 예외 단서다. 단서의 「일반적인」이 어떤 장비·설정을 가리키는지 없다. → B10  
  근거: `/M11/contraindications/relative/0` 「단, 일반적인 니들RF는」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX014 | prevention_in_safety_paren | `/M11/safety/serious/0` | (1회용 팁 사용으로 위생 관리) |  |
| MX015 | frequency_degree_scoped_condition | `/M11/safety/serious/1` | 드물게 화상 (부적절한 에너지 설정 시) | 빈도어「드물게」가 serious 그룹 안에 있음 |
| MX016 | comparison_degree | `/M11/safety/uncommon/0` | 박피나 레이저 시술에 비해 위험이 매우 작음 |  |
| MX017 | quantity_with_target | `/M11/mechanism` | 약 20%의 면적 | 분모 = 시술 범위 중 목표 부위(원문 구절) |
| MX018 | negated_statement | `/M11/mechanism` | 색소침착 등의 부작용이 없고 | safety/uncommon/0 과 대조(I3) |
| MX019 | negated_causal | `/M11/aftercare/0` | 딱지가 없으므로 일상생활에 지장 없음 |  |
| MX020 | exception_qualifier | `/M11/contraindications/relative/0` | (단, 일반적인 니들RF는 켈로이드 위험이 낮음) |  |
| MX021 | condition_effect | `/M11/onset_duration/duration` | (반복 시술 시 효과 누적) |  |
| MX022 | comparison_contrast | `/M11/related_techniques/0` | 비슷한 피부 재생 원리이나 표피 손상이 더 큼 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R04-1 | `/M11/safety/uncommon/0` | [6,8) | 박피 | 박/NNP + 피/NNG | 「박피」가 박+피로 분절 | 시술 기법어(박피·비박피) 식별 실패. 「비박피성」의 부정 접두 「비」는 XPN 으로 남지만 대상어가 깨짐 |
| R04-2 | `/M11/overview` | [109,112) | 비박피 | 비/XPN + 박/NNG + 피/NNG | 「박피」가 박+피로 분절 | 시술 기법어(박피·비박피) 식별 실패. 「비박피성」의 부정 접두 「비」는 XPN 으로 남지만 대상어가 깨짐 |
| R20-1 | `/M11/indications/extended/4` | [0,2) | 튼살 | 트/VV + ᆫ/ETM + 살/NNG | 「튼살」을 트/VV + ᆫ/ETM + 살/NNG 로 분해 | 문법적으로 가능한 분해이나 질환/고민 명칭 단위가 사라짐(동사 「트다」 + 「살」) |

규칙 기반 표현 후보 205건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S02"` 에 있다. 후보이며 전수 의미 해석이 아니다.
