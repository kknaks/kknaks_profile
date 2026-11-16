# S09 — `M1` (보톡스) · extracted.json 1차 조사

> 구획 S09 · 소유 Pointer `/M1` 와 그 아래 72개 노드(말단 58). 문맥 참조: 루트 `""`, `/M1/name`, `/M1/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 3 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M1)` | `/M1` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M1/name` | string | 보톡스 | 분석 |
| 3 | `safety` | `/M1/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M1/safety/common` | array | (array · 7) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M1/safety/common/0` | string | 주사 부위 통증 | 분석 |
| 6 | `safety.common[1]` | `/M1/safety/common/1` | string | 약간의 붓기 | 분석 |
| 7 | `safety.common[2]` | `/M1/safety/common/2` | string | 피부 빨개짐 | 분석 |
| 8 | `safety.common[3]` | `/M1/safety/common/3` | string | 멍 | 분석 |
| 9 | `safety.common[4]` | `/M1/safety/common/4` | string | 두통 | 분석 |
| 10 | `safety.common[5]` | `/M1/safety/common/5` | string | 이마나 눈썹이 무거운 느낌 | 분석 |
| 11 | `safety.common[6]` | `/M1/safety/common/6` | string | 얼굴이 약간 부은 느낌 | 분석 |
| 12 | `safety.serious` | `/M1/safety/serious` | array | (array · 2) | —(컨테이너) |
| 13 | `safety.serious[0]` | `/M1/safety/serious/0` | string | 드물게 메스꺼움, 피로감, 감기 비슷한 증상 (20년간 치명적 부작용 보고 없음) | 분석 |
| 14 | `safety.serious[1]` | `/M1/safety/serious/1` | string | 반복 시술 시 몸에서 항체가 생겨 효과가 줄어들 수 있음 | 분석 |
| 15 | `safety.uncommon` | `/M1/safety/uncommon` | array | (array · 4) | —(컨테이너) |
| 16 | `safety.uncommon[0]` | `/M1/safety/uncommon/0` | string | 표정이 어색해지는 느낌 (마스크 쓴 것 같은 얼굴) | 분석 |
| 17 | `safety.uncommon[1]` | `/M1/safety/uncommon/1` | string | 주름이 덜 펴지는 경우 | 분석 |
| 18 | `safety.uncommon[2]` | `/M1/safety/uncommon/2` | string | 윗눈꺼풀이나 눈썹이 처지는 현상 | 분석 |
| 19 | `safety.uncommon[3]` | `/M1/safety/uncommon/3` | string | 눈이 건조해지는 증상 (눈물 분비 감소) | 분석 |
| 20 | `source` | `/M1/source` | string | 임상적 피부관리 36장 | 분석 |
| 21 | `name_en` | `/M1/name_en` | string | Botulinum Toxin Type A | 분석 |
| 22 | `overview` | `/M1/overview` | string | 보톡스는 근육을 일시적으로 쉬게 만드는 주사제다. 원래 눈 떨림이나 근육 경련 치료에 쓰였지만, 주름을 펴는 효과가 알려지면서 1990년대부터 미용 시술로 널리 퍼졌다. 2002년 미국 FDA, 2008년 한국 식약처에서 미간주름 치료용으로 정식 승인받았다. | 분석 |
| 23 | `aftercare` | `/M1/aftercare` | array | (array · 2) | —(컨테이너) |
| 24 | `aftercare[0]` | `/M1/aftercare/0` | string | 주사 직후 시술 부위를 강하게 누르거나 문지르지 않기 (확산 방지 목적, 자세 제한의 독립 효과는 RCT에서 확인되지 않음) | 분석 |
| 25 | `aftercare[1]` | `/M1/aftercare/1` | string | 시술 부위를 만지거나 문지르지 않기 | 분석 |
| 26 | `mechanism` | `/M1/mechanism` | string | 보톡스는 근육에 명령을 전달하는 신경 끝부분에 작용한다. 신경이 근육에 '움직여라'는 신호(아세틸콜린)를 보내는 걸 차단해서, 근육이 힘을 못 쓰고 이완된다. 뇌나 척수 같은 중추신경에는 영향을 주지 않고, 주사 맞은 부위의 근육과 땀샘에만 작용한다. | 분석 |
| 27 | `indications` | `/M1/indications` | object | (object · 2) | —(컨테이너) |
| 28 | `indications.primary` | `/M1/indications/primary` | array | (array · 4) | —(컨테이너) |
| 29 | `indications.primary[0]` | `/M1/indications/primary/0` | string | 미간주름 (눈썹 사이 찡그리면 생기는 세로 주름) | 분석 |
| 30 | `indications.primary[1]` | `/M1/indications/primary/1` | string | 눈가 주름 (웃을 때 생기는 까치발 주름) | 분석 |
| 31 | `indications.primary[2]` | `/M1/indications/primary/2` | string | 이마 주름 (가로로 생기는 이마 줄) | 분석 |
| 32 | `indications.primary[3]` | `/M1/indications/primary/3` | string | 사각턱 (턱 근육이 발달해서 얼굴이 넓어 보이는 것) | 분석 |
| 33 | `indications.extended` | `/M1/indications/extended` | array | (array · 19) | —(컨테이너) |
| 34 | `indications.extended[0]` | `/M1/indications/extended/0` | string | 눈썹 올리기 | 분석 |
| 35 | `indications.extended[1]` | `/M1/indications/extended/1` | string | 눈밑주름 | 분석 |
| 36 | `indications.extended[2]` | `/M1/indications/extended/2` | string | 목주름 | 분석 |
| 37 | `indications.extended[3]` | `/M1/indications/extended/3` | string | 윗입술 세로주름 | 분석 |
| 38 | `indications.extended[4]` | `/M1/indications/extended/4` | string | 콧등 잔주름 (토끼주름) | 분석 |
| 39 | `indications.extended[5]` | `/M1/indications/extended/5` | string | 콧구멍 벌렁거림 완화 | 분석 |
| 40 | `indications.extended[6]` | `/M1/indications/extended/6` | string | 콧구멍 줄이기 | 분석 |
| 41 | `indications.extended[7]` | `/M1/indications/extended/7` | string | 매부리코 교정 | 분석 |
| 42 | `indications.extended[8]` | `/M1/indications/extended/8` | string | 짧은 인중 늘리기 | 분석 |
| 43 | `indications.extended[9]` | `/M1/indications/extended/9` | string | 팔자주름 | 분석 |
| 44 | `indications.extended[10]` | `/M1/indications/extended/10` | string | 눈썹 높이 맞추기 | 분석 |
| 45 | `indications.extended[11]` | `/M1/indications/extended/11` | string | 얼굴 좌우 비대칭 교정 | 분석 |
| 46 | `indications.extended[12]` | `/M1/indications/extended/12` | string | 입꼬리 처짐 교정 | 분석 |
| 47 | `indications.extended[13]` | `/M1/indications/extended/13` | string | 뾰족턱 교정 | 분석 |
| 48 | `indications.extended[14]` | `/M1/indications/extended/14` | string | 턱 울퉁불퉁한 피부 개선 | 분석 |
| 49 | `indications.extended[15]` | `/M1/indications/extended/15` | string | 상처/피부결 개선 | 분석 |
| 50 | `indications.extended[16]` | `/M1/indications/extended/16` | string | 피부 부드럽게/흉터 교정 | 분석 |
| 51 | `indications.extended[17]` | `/M1/indications/extended/17` | string | 켈로이드 (흉터가 부풀어오르는 증상) | 분석 |
| 52 | `indications.extended[18]` | `/M1/indications/extended/18` | string | 다한증 (땀이 과하게 나는 증상) | 분석 |
| 53 | `source_type` | `/M1/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 54 | `extracted_at` | `/M1/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 55 | `procedure_id` | `/M1/procedure_id` | string | M1-BOTOX | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 56 | `onset_duration` | `/M1/onset_duration` | object | (object · 3) | —(컨테이너) |
| 57 | `onset_duration.peak` | `/M1/onset_duration/peak` | string | 약 1주일 후 원하는 만큼 효과 도달 | 분석 |
| 58 | `onset_duration.onset` | `/M1/onset_duration/onset` | string | 시술 후 12시간~4일 사이에 효과가 나타나기 시작 | 분석 |
| 59 | `onset_duration.duration` | `/M1/onset_duration/duration` | string | 3~6개월 유지 (사람마다 다름) | 분석 |
| 60 | `contraindications` | `/M1/contraindications` | object | (object · 2) | —(컨테이너) |
| 61 | `contraindications.absolute` | `/M1/contraindications/absolute` | array | (array · 4) | —(컨테이너) |
| 62 | `contraindications.absolute[0]` | `/M1/contraindications/absolute/0` | string | 보톡스 성분(알부민)에 알레르기가 있는 경우 | 분석 |
| 63 | `contraindications.absolute[1]` | `/M1/contraindications/absolute/1` | string | 중증근무력증 / 루게릭병 (근육이 점점 약해지는 질환) 환자 | 분석 |
| 64 | `contraindications.absolute[2]` | `/M1/contraindications/absolute/2` | string | 주사 맞을 부위에 염증이나 감염이 있는 경우 | 분석 |
| 65 | `contraindications.absolute[3]` | `/M1/contraindications/absolute/3` | string | 시술 결과에 비현실적인 기대를 가진 경우 | 분석 |
| 66 | `contraindications.relative` | `/M1/contraindications/relative` | array | (array · 2) | —(컨테이너) |
| 67 | `contraindications.relative[0]` | `/M1/contraindications/relative/0` | string | 임신 중이거나 수유 중일 때는 미루는 게 좋음 | 분석 |
| 68 | `contraindications.relative[1]` | `/M1/contraindications/relative/1` | string | 특정 약물(항생제 일부, 근이완제 등) 복용 중이면 효과가 과하게 나타날 수 있으니 의사에게 알릴 것 | 분석 |
| 69 | `guardrail_version` | `/M1/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 70 | `related_techniques` | `/M1/related_techniques` | array | (array · 2) | —(컨테이너) |
| 71 | `related_techniques[0]` | `/M1/related_techniques/0` | string | 메조보톡스 (더모톡신) — 피부 탄력 개선, 리프팅 효과 | 분석 |
| 72 | `related_techniques[1]` | `/M1/related_techniques/1` | string | 에어보톡스 — 여드름 흉터 치료에 활용 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S09-01** (I) safety/serious 첫 값에 「드물게」와 경미해 보이는 증상(메스꺼움·피로감·감기 비슷한 증상)이 있고 괄호는 치명적 부작용 보고가 없다는 진술이다. serious 둘째 값과 uncommon 둘째 값은 사건이 아니라 효과 감소·부족이다. → I6, F8  
  근거: `/M1/safety/serious/0` 「20년간 치명적 부작용 보고 없음」; `/M1/safety/serious/1` 「효과가 줄어들 수 있음」; `/M1/safety/uncommon/1` 「주름이 덜 펴지는 경우」
- **OB-S09-02** (I) aftercare 두 값의 내용이 거의 겹친다(누르거나 문지르지 않기 / 만지거나 문지르지 않기). 첫 값에는 근거 진술(RCT 미확인)이 붙었다. → I12  
  근거: `/M1/aftercare/0` 「문지르지 않기」; `/M1/aftercare/1` 「시술 부위를 만지거나 문지르지 않기」
- **OB-S09-03** (F) overview 의 승인 정보(2002 FDA·2008 식약처)는 「미간주름 치료용」에 한정돼 있고 indications 에는 미간주름을 포함해 값 23개(primary 4 · extended 19)가 있다. 승인 범위와 적응증 목록의 관계는 원문에 없다. 사실 검증하지 않았다. → F8  
  근거: `/M1/overview` 「미간주름 치료용으로 정식 승인받았다」; `/M1/indications/extended/18` 「다한증」
- **OB-S09-04** (F) indications/extended 19개에 부위(눈밑·목·인중), 목적(눈썹 올리기·콧구멍 줄이기), 질환(켈로이드·다한증), 결(상처/피부결)이 한 목록에 섞여 있다. 부위와 고민을 분리하지 않았다. → F2  
  근거: `/M1/indications/extended/0` 「눈썹 올리기」; `/M1/indications/extended/17` 「켈로이드」; `/M1/indications/extended/15` 「상처/피부결 개선」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX097 | frequency_degree_scoped | `/M1/safety/serious/0` | 드물게 메스꺼움, 피로감, 감기 비슷한 증상 | 「드물게」가 쉼표 나열 셋 모두에 걸리는지 원문만으로 불명 |
| MX098 | negated_evidence_statement | `/M1/safety/serious/0` | (20년간 치명적 부작용 보고 없음) |  |
| MX099 | condition_possibility_causal | `/M1/safety/serious/1` | 반복 시술 시 몸에서 항체가 생겨 효과가 줄어들 수 있음 |  |
| MX100 | degree_effect_shortfall | `/M1/safety/uncommon/1` | 주름이 덜 펴지는 경우 |  |
| MX101 | time_degree_negated_instruction | `/M1/aftercare/0` | 주사 직후 시술 부위를 강하게 누르거나 문지르지 않기 |  |
| MX102 | negated_evidence_statement | `/M1/aftercare/0` | 자세 제한의 독립 효과는 RCT에서 확인되지 않음 |  |
| MX103 | negated_statement | `/M1/mechanism` | 뇌나 척수 같은 중추신경에는 영향을 주지 않고 |  |
| MX104 | site_restriction | `/M1/mechanism` | 주사 맞은 부위의 근육과 땀샘에만 작용한다 |  |
| MX105 | regulatory_claim_scoped | `/M1/overview` | 2002년 미국 FDA, 2008년 한국 식약처에서 미간주름 치료용으로 정식 승인받았다 |  |
| MX106 | time_window_with_anchor | `/M1/onset_duration/onset` | 시술 후 12시간~4일 사이에 |  |
| MX107 | time_with_variability | `/M1/onset_duration/duration` | 3~6개월 유지 (사람마다 다름) |  |
| MX108 | population_recommendation | `/M1/contraindications/relative/0` | 임신 중이거나 수유 중일 때는 미루는 게 좋음 |  |
| MX109 | medication_possibility_obligation | `/M1/contraindications/relative/1` | 복용 중이면 효과가 과하게 나타날 수 있으니 의사에게 알릴 것 |  |
| MX187 | historical_claim | `/M1/overview` | 1990년대부터 미용 시술로 널리 퍼졌다 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R11-2 | `/M1/safety/common/3` | [0,1) | 멍 | 멍/MAG | 단독 값 「멍」(타박 멍)을 부사(MAG)로 태깅 | 부작용 사건 명사가 부사로 분류 — 품사로 사건 명사를 고르면 누락. 값 자체는 원문 보존 |

규칙 기반 표현 후보 245건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S09"` 에 있다. 후보이며 전수 의미 해석이 아니다.
