# S12 — `M4` (스킨부스터) · extracted.json 1차 조사

> 구획 S12 · 소유 Pointer `/M4` 와 그 아래 58개 노드(말단 44). 문맥 참조: 루트 `""`, `/M4/name`, `/M4/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 4 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M4)` | `/M4` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M4/name` | string | 스킨부스터 | 분석 |
| 3 | `safety` | `/M4/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M4/safety/common` | array | (array · 4) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M4/safety/common/0` | string | 주사 부위 통증 | 분석 |
| 6 | `safety.common[1]` | `/M4/safety/common/1` | string | 일시적 홍반 (빨개짐) | 분석 |
| 7 | `safety.common[2]` | `/M4/safety/common/2` | string | 약간의 붓기 | 분석 |
| 8 | `safety.common[3]` | `/M4/safety/common/3` | string | 멍 | 분석 |
| 9 | `safety.serious` | `/M4/safety/serious` | array | (array · 2) | —(컨테이너) |
| 10 | `safety.serious[0]` | `/M4/safety/serious/0` | string | 농양 (고름이 차는 감염) | 분석 |
| 11 | `safety.serious[1]` | `/M4/safety/serious/1` | string | 드물게 심한 알레르기 반응 | 분석 |
| 12 | `safety.uncommon` | `/M4/safety/uncommon` | array | (array · 3) | —(컨테이너) |
| 13 | `safety.uncommon[0]` | `/M4/safety/uncommon/0` | string | 알레르기 반응 | 분석 |
| 14 | `safety.uncommon[1]` | `/M4/safety/uncommon/1` | string | 혈종 (피가 고이는 것) | 분석 |
| 15 | `safety.uncommon[2]` | `/M4/safety/uncommon/2` | string | 피부색소침착 (시술 부위가 어두워지는 현상) | 분석 |
| 16 | `source` | `/M4/source` | string | 임상적 피부관리 19장 (메조테라피) | 분석 |
| 17 | `name_en` | `/M4/name_en` | string | Skin Booster / Mesotherapy | 분석 |
| 18 | `overview` | `/M4/overview` | string | 스킨부스터는 피부의 진피층(피부 깊은 곳)에 히알루론산, 비타민, 아미노산 등 영양 성분을 소량씩 여러 포인트에 주입하는 시술이다. 한국에서는 '물광주사'로 널리 알려져 있으며, 메조테라피(mesotherapy) 기법을 기반으로 한다. 피부 자체의 수분과 탄력을 개선하는 것이 목적이다. | 분석 |
| 19 | `aftercare` | `/M4/aftercare` | array | (array · 3) | —(컨테이너) |
| 20 | `aftercare[0]` | `/M4/aftercare/0` | string | 시술 당일 세안이나 화장은 피하기 | 분석 |
| 21 | `aftercare[1]` | `/M4/aftercare/1` | string | 시술 후 자외선 차단제 꼼꼼히 바르기 | 분석 |
| 22 | `aftercare[2]` | `/M4/aftercare/2` | string | 시술 부위를 문지르거나 강하게 누르지 않기 | 분석 |
| 23 | `mechanism` | `/M4/mechanism` | string | 메조테라피는 중배엽(mesoderm) 유래 조직, 특히 피부의 진피층에 소량의 약물을 국소적으로 여러 포인트에 피내주사(피부 안에 주사)하는 치료법이다. 히알루론산을 진피 내에 주입하면 기존 필러와 같은 연조직 확대 기능보다는, 피부를 자극해 피부 자신의 구성성분을 스스로 형성하게 하여 피부 자체의 질을 향상시킨다. 전신 약물 투여로 발생할 수 있는 부담감과 위험성을 최소화하고, 원하는 국소부위에 제한적으로 약물을 직접 전달할 수 있다는 장점이 있다. | 분석 |
| 24 | `indications` | `/M4/indications` | object | (object · 2) | —(컨테이너) |
| 25 | `indications.primary` | `/M4/indications/primary` | array | (array · 4) | —(컨테이너) |
| 26 | `indications.primary[0]` | `/M4/indications/primary/0` | string | 피부 수분 부족 (건조하고 윤기 없는 피부) | 분석 |
| 27 | `indications.primary[1]` | `/M4/indications/primary/1` | string | 잔주름 (얕은 주름) | 분석 |
| 28 | `indications.primary[2]` | `/M4/indications/primary/2` | string | 피부 탄력 저하 | 분석 |
| 29 | `indications.primary[3]` | `/M4/indications/primary/3` | string | 모공 확대 | 분석 |
| 30 | `indications.extended` | `/M4/indications/extended` | array | (array · 6) | —(컨테이너) |
| 31 | `indications.extended[0]` | `/M4/indications/extended/0` | string | 피부 노화 방지 | 분석 |
| 32 | `indications.extended[1]` | `/M4/indications/extended/1` | string | 기미 (피부 색소 불균일) | 분석 |
| 33 | `indications.extended[2]` | `/M4/indications/extended/2` | string | 탈모증 (두피 메조테라피, 메조페시아) | 분석 |
| 34 | `indications.extended[3]` | `/M4/indications/extended/3` | string | 셀룰라이트 (피부 울퉁불퉁한 지방 침착) | 분석 |
| 35 | `indications.extended[4]` | `/M4/indications/extended/4` | string | 흉터 개선 | 분석 |
| 36 | `indications.extended[5]` | `/M4/indications/extended/5` | string | 튼살 (임신선, 성장선) | 분석 |
| 37 | `source_type` | `/M4/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 38 | `extracted_at` | `/M4/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 39 | `procedure_id` | `/M4/procedure_id` | string | M4-SKINBOOSTER | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 40 | `onset_duration` | `/M4/onset_duration` | object | (object · 3) | —(컨테이너) |
| 41 | `onset_duration.peak` | `/M4/onset_duration/peak` | string | 2~4주 후 피부결 개선 효과 최대 | 분석 |
| 42 | `onset_duration.onset` | `/M4/onset_duration/onset` | string | 시술 직후~2일 이내 피부 광채 효과 시작 | 분석 |
| 43 | `onset_duration.duration` | `/M4/onset_duration/duration` | string | 1~3개월 유지 (반복 시술 시 효과 누적) | 분석 |
| 44 | `contraindications` | `/M4/contraindications` | object | (object · 2) | —(컨테이너) |
| 45 | `contraindications.absolute` | `/M4/contraindications/absolute` | array | (array · 4) | —(컨테이너) |
| 46 | `contraindications.absolute[0]` | `/M4/contraindications/absolute/0` | string | 허혈성 심질환 (심장에 혈액 공급이 부족한 질환) | 분석 |
| 47 | `contraindications.absolute[1]` | `/M4/contraindications/absolute/1` | string | 당뇨병 환자 | 분석 |
| 48 | `contraindications.absolute[2]` | `/M4/contraindications/absolute/2` | string | 신장질환 환자 | 분석 |
| 49 | `contraindications.absolute[3]` | `/M4/contraindications/absolute/3` | string | 주입 약물에 과민반응을 보이는 경우 | 분석 |
| 50 | `contraindications.relative` | `/M4/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 51 | `contraindications.relative[0]` | `/M4/contraindications/relative/0` | string | 항응고제 복용 중인 경우 (멍이 잘 들 수 있음) | 분석 |
| 52 | `contraindications.relative[1]` | `/M4/contraindications/relative/1` | string | 임산부, 생리 중인 경우 주의 필요 | 분석 |
| 53 | `contraindications.relative[2]` | `/M4/contraindications/relative/2` | string | 시술 부위에 피부 질환이 있는 경우 | 분석 |
| 54 | `guardrail_version` | `/M4/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 55 | `related_techniques` | `/M4/related_techniques` | array | (array · 3) | —(컨테이너) |
| 56 | `related_techniques[0]` | `/M4/related_techniques/0` | string | 메조리프트 (Mesolift) -- 비타민과 히알루론산 주사로 리프팅 효과 | 분석 |
| 57 | `related_techniques[1]` | `/M4/related_techniques/1` | string | 메조보톡스 -- 보톡스를 진피층에 소량 주사해 모공/탄력 개선 | 분석 |
| 58 | `related_techniques[2]` | `/M4/related_techniques/2` | string | 메조페시아 (Mesopecia) -- 두피에 약물 주사해 탈모 치료 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S12-01** (P) serious 「드물게 심한 알레르기 반응」과 uncommon 「알레르기 반응」은 같은 사건이 빈도·정도 수식어로 다른 그룹에 있다. → F4  
  근거: `/M4/safety/serious/1` 「드물게 심한 알레르기 반응」; `/M4/safety/uncommon/0` 「알레르기 반응」
- **OB-S12-02** (F) name_en 「Skin Booster / Mesotherapy」, source 「19장 (메조테라피)」, mechanism 은 메조테라피 일반을 설명한다. related 의 메조리프트·메조보톡스·메조페시아도 메조테라피 계열이다. 항목 범위는 후속 판단이다. → F11  
  근거: `/M4/name_en` 「Skin Booster / Mesotherapy」; `/M4/mechanism` 「메조테라피는 중배엽(mesoderm) 유래 조직」
- **OB-S12-03** (P) overview 의 「진피층(피부 깊은 곳)」에서 「깊은」은 층의 위치 풀이다. 주입 깊이 수치가 아니다. → F4  
  근거: `/M4/overview` 「진피층(피부 깊은 곳)」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX127 | frequency_severity_scoped | `/M4/safety/serious/1` | 드물게 심한 알레르기 반응 | uncommon/0 「알레르기 반응」과 수식어로 구분 |
| MX128 | quantity_word_scoped | `/M4/overview` | 소량씩 여러 포인트에 주입 |  |
| MX129 | comparison_contrast | `/M4/mechanism` | 기존 필러와 같은 연조직 확대 기능보다는 |  |
| MX130 | time_range | `/M4/onset_duration/onset` | 시술 직후~2일 이내 |  |
| MX131 | medication_possibility | `/M4/contraindications/relative/0` | 항응고제 복용 중인 경우 (멍이 잘 들 수 있음) |  |
| MX132 | population_recommendation | `/M4/contraindications/relative/1` | 임산부, 생리 중인 경우 주의 필요 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R05-1 | `/M4/contraindications/absolute/0` | [4,7) | 심질환 | 심/NNP + 질환/NNG | 「심질환」의 「심」을 고유명사(NNP)로 태깅 | 심장 질환 의미의 한자어 요소가 고유명사로 오인. 질환명 탐색 시 오분류 |
| R06-1 | `/M4/mechanism` | [21,23) | 유래 | 유/NNP + 래/NNG | 「유래」가 유/NNP + 래/NNG 로 분절 | 「중배엽 유래」의 기원 관계 표현 소실 |
| R08-3 | `/M4/mechanism` | [107,110) | 필러와 | 필러와/NNG | 「필러」+조사가 한 명사(NNG)로 묶임(필러가·필러와) | 조사 정보 소실 및 명사 형태가 「필러가」로 남아 시술명 집계·대조에서 누락 |
| R11-5 | `/M4/safety/common/3` | [0,1) | 멍 | 멍/MAG | 단독 값 「멍」(타박 멍)을 부사(MAG)로 태깅 | 부작용 사건 명사가 부사로 분류 — 품사로 사건 명사를 고르면 누락. 값 자체는 원문 보존 |
| R20-3 | `/M4/indications/extended/5` | [0,2) | 튼살 | 트/VV + ᆫ/ETM + 살/NNG | 「튼살」을 트/VV + ᆫ/ETM + 살/NNG 로 분해 | 문법적으로 가능한 분해이나 질환/고민 명칭 단위가 사라짐(동사 「트다」 + 「살」) |

규칙 기반 표현 후보 189건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S12"` 에 있다. 후보이며 전수 의미 해석이 아니다.
