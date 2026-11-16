# S07 — `M16` (수액치료) · extracted.json 1차 조사

> 구획 S07 · 소유 Pointer `/M16` 와 그 아래 53개 노드(말단 39). 문맥 참조: 루트 `""`, `/M16/name`, `/M16/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 3 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M16)` | `/M16` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M16/name` | string | 수액치료 | 분석 |
| 3 | `safety` | `/M16/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M16/safety/common` | array | (array · 3) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M16/safety/common/0` | string | 주사 부위 통증 및 멍 | 분석 |
| 6 | `safety.common[1]` | `/M16/safety/common/1` | string | 주입 중 혈관 따라 약간의 화끈거림 | 분석 |
| 7 | `safety.common[2]` | `/M16/safety/common/2` | string | 일시적 어지러움 | 분석 |
| 8 | `safety.serious` | `/M16/safety/serious` | array | (array · 3) | —(컨테이너) |
| 9 | `safety.serious[0]` | `/M16/safety/serious/0` | string | 아나필락시스 (심각한 전신 알레르기 반응 -- 극히 드묾) | 분석 |
| 10 | `safety.serious[1]` | `/M16/safety/serious/1` | string | 전해질 불균형 (부적절한 성분 투여 시) | 분석 |
| 11 | `safety.serious[2]` | `/M16/safety/serious/2` | string | 감염 (무균 관리가 안 될 경우) | 분석 |
| 12 | `safety.uncommon` | `/M16/safety/uncommon` | array | (array · 2) | —(컨테이너) |
| 13 | `safety.uncommon[0]` | `/M16/safety/uncommon/0` | string | 정맥염 (혈관 벽 자극으로 인한 염증) | 분석 |
| 14 | `safety.uncommon[1]` | `/M16/safety/uncommon/1` | string | 알레르기 반응 (피부 발진, 가려움) | 분석 |
| 15 | `source` | `/M16/source` | string | 일반 의학 지식 | 분석 |
| 16 | `name_en` | `/M16/name_en` | string | IV Therapy / Intravenous Nutrient Therapy | 분석 |
| 17 | `overview` | `/M16/overview` | string | 수액치료는 비타민, 미네랄, 아미노산, 항산화제 등의 영양 성분을 정맥주사(IV)를 통해 혈관에 직접 투여하는 시술이다. 한국 피부과와 미용 클리닉에서 '백옥주사(글루타치온)', '신데렐라주사(알파리포산)', '마늘주사(비타민B1)' 등의 이름으로 널리 시행되고 있다. 경구 복용보다 높은 혈중 농도를 빠르게 달성할 수 있다는 것이 장점이다. | 분석 |
| 18 | `aftercare` | `/M16/aftercare` | array | (array · 3) | —(컨테이너) |
| 19 | `aftercare[0]` | `/M16/aftercare/0` | string | 주사 부위를 5분 이상 눌러서 지혈 | 분석 |
| 20 | `aftercare[1]` | `/M16/aftercare/1` | string | 시술 당일 과도한 음주 피하기 | 분석 |
| 21 | `aftercare[2]` | `/M16/aftercare/2` | string | 충분한 수분 섭취 | 분석 |
| 22 | `mechanism` | `/M16/mechanism` | string | 영양 성분을 정맥을 통해 직접 혈류에 투여하면, 소화기관을 거치지 않으므로(위장관 초회통과효과 회피) 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다. 경구 복용 시 흡수율이 10~30%에 불과한 비타민C 같은 성분도, 정맥주사로는 훨씬 높은 혈중 농도를 달성할 수 있다. 고농도로 투여된 항산화 성분(글루타치온, 비타민C 등)은 활성산소를 중화하고, 멜라닌(피부 색소) 생성을 억제하며, 세포 대사를 촉진하는 효과를 나타낸다. | 분석 |
| 23 | `indications` | `/M16/indications` | object | (object · 2) | —(컨테이너) |
| 24 | `indications.primary` | `/M16/indications/primary` | array | (array · 3) | —(컨테이너) |
| 25 | `indications.primary[0]` | `/M16/indications/primary/0` | string | 피부 미백 및 톤 개선 (글루타치온, 비타민C) | 분석 |
| 26 | `indications.primary[1]` | `/M16/indications/primary/1` | string | 피로 회복 및 활력 증진 (비타민B군, 아미노산) | 분석 |
| 27 | `indications.primary[2]` | `/M16/indications/primary/2` | string | 항산화/노화 방지 (비타민C, 알파리포산) | 분석 |
| 28 | `indications.extended` | `/M16/indications/extended` | array | (array · 4) | —(컨테이너) |
| 29 | `indications.extended[0]` | `/M16/indications/extended/0` | string | 숙취 해소 | 분석 |
| 30 | `indications.extended[1]` | `/M16/indications/extended/1` | string | 면역력 강화 | 분석 |
| 31 | `indications.extended[2]` | `/M16/indications/extended/2` | string | 체중 감량 보조 (지방 대사 촉진 성분) | 분석 |
| 32 | `indications.extended[3]` | `/M16/indications/extended/3` | string | 모발 건강 개선 | 분석 |
| 33 | `source_type` | `/M16/source_type` | string | general | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 34 | `extracted_at` | `/M16/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 35 | `procedure_id` | `/M16/procedure_id` | string | M16-IVTHERAPY | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 36 | `onset_duration` | `/M16/onset_duration` | object | (object · 3) | —(컨테이너) |
| 37 | `onset_duration.peak` | `/M16/onset_duration/peak` | string | 시술 후 1~3일 뒤 피부 톤 개선 체감 | 분석 |
| 38 | `onset_duration.onset` | `/M16/onset_duration/onset` | string | 주입 중~직후 피로 회복 효과 체감 | 분석 |
| 39 | `onset_duration.duration` | `/M16/onset_duration/duration` | string | 1~2주 유지 (정기적 시술로 효과 누적) | 분석 |
| 40 | `contraindications` | `/M16/contraindications` | object | (object · 2) | —(컨테이너) |
| 41 | `contraindications.absolute` | `/M16/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 42 | `contraindications.absolute[0]` | `/M16/contraindications/absolute/0` | string | 주입 성분에 알레르기가 있는 경우 | 분석 |
| 43 | `contraindications.absolute[1]` | `/M16/contraindications/absolute/1` | string | G6PD 결핍증 환자 (고용량 비타민C 투여 시 용혈 위험) | 분석 |
| 44 | `contraindications.absolute[2]` | `/M16/contraindications/absolute/2` | string | 심한 신부전 환자 (전해질 불균형 위험) | 분석 |
| 45 | `contraindications.relative` | `/M16/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 46 | `contraindications.relative[0]` | `/M16/contraindications/relative/0` | string | 심부전 환자 (과다한 수액으로 심장 부담) | 분석 |
| 47 | `contraindications.relative[1]` | `/M16/contraindications/relative/1` | string | 당뇨병 환자 (포도당 포함 수액 주의) | 분석 |
| 48 | `contraindications.relative[2]` | `/M16/contraindications/relative/2` | string | 임신 중이거나 수유 중인 경우 | 분석 |
| 49 | `guardrail_version` | `/M16/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 50 | `related_techniques` | `/M16/related_techniques` | array | (array · 3) | —(컨테이너) |
| 51 | `related_techniques[0]` | `/M16/related_techniques/0` | string | 메조테라피 -- 피부에 직접 영양 성분 주입 | 분석 |
| 52 | `related_techniques[1]` | `/M16/related_techniques/1` | string | PRP(혈소판풍부혈장) -- 자가 혈액 활용 재생 치료 | 분석 |
| 53 | `related_techniques[2]` | `/M16/related_techniques/2` | string | 경구 영양제 -- 유지 요법으로 병행 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S07-01** (F) overview 의 이름 셋은 이름 + 괄호 성분(글루타치온·알파리포산·비타민B1)이고 indications/primary 도 효과마다 괄호로 성분을 단다. 효과·금기(G6PD: 고용량 비타민C, 당뇨: 포도당 포함 수액)가 성분 조건부다. → F3  
  근거: `/M16/overview` 「'백옥주사(글루타치온)'」; `/M16/indications/primary/0` 「(글루타치온, 비타민C)」; `/M16/contraindications/absolute/1` 「고용량 비타민C 투여 시」
- **OB-S07-02** (F) mechanism 의 수치 「거의 100%」(생체이용률), 「10~30%」(경구 흡수율, 비타민C)는 대상·분모가 문장 안에 있다. 출처 근거는 source 「일반 의학 지식」뿐이다. → F10, B7  
  근거: `/M16/mechanism` 「거의 100%에 가깝다」; `/M16/mechanism` 「10~30%에 불과한」; `/M16/source` 「일반 의학 지식」
- **OB-S07-03** (P) serious 「아나필락시스」의 괄호 안에 설명과 빈도가 「 -- 」로 이어진다. 빈도어가 괄호 안에 들어간 꼴이다. → F4  
  근거: `/M16/safety/serious/0` 「심각한 전신 알레르기 반응 -- 극히 드묾」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX073 | time_site_degree | `/M16/safety/common/1` | 주입 중 혈관 따라 약간의 화끈거림 |  |
| MX074 | frequency_degree_scoped | `/M16/safety/serious/0` | 극히 드묾 |  |
| MX075 | condition | `/M16/safety/serious/1` | (부적절한 성분 투여 시) |  |
| MX076 | comparison_possibility | `/M16/overview` | 경구 복용보다 높은 혈중 농도를 빠르게 달성할 수 있다 |  |
| MX077 | quantity_threshold | `/M16/aftercare/0` | 5분 이상 눌러서 지혈 |  |
| MX078 | time_degree_avoidance | `/M16/aftercare/1` | 시술 당일 과도한 음주 피하기 |  |
| MX079 | quantity_with_target | `/M16/mechanism` | 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다 |  |
| MX080 | quantity_with_target | `/M16/mechanism` | 경구 복용 시 흡수율이 10~30%에 불과한 비타민C |  |
| MX081 | ingredient_condition_risk | `/M16/contraindications/absolute/1` | (고용량 비타민C 투여 시 용혈 위험) |  |
| MX082 | ingredient_condition | `/M16/contraindications/relative/1` | (포도당 포함 수액 주의) |  |
| MX083 | time_range | `/M16/onset_duration/onset` | 주입 중~직후 |  |
| MX084 | time_with_condition | `/M16/onset_duration/duration` | 1~2주 유지 (정기적 시술로 효과 누적) |  |
| MX190 | named_variant_with_ingredient | `/M16/overview` | '백옥주사(글루타치온)', '신데렐라주사(알파리포산)', '마늘주사(비타민B1)' |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R14-1 | `/M16/mechanism` | [46,50) | 초회통과 | 초/NNB + 회/NNB + 통과/NNG | 「초회통과」를 초/NNB + 회/NNB(의존명사 단위) + 통과로 분절 | 약동학 용어가 시간·횟수 단위(초·회)로 오인 — 수량·시간 후보 오탐 위험 |
| R15-1 | `/M16/contraindications/absolute/1` | [27,29) | 용혈 | 용/NNG + 혈/NNG | 「용혈」이 용/NNG + 혈/NNG 로 분절 | 위험 사건(용혈) 명칭 소실 |
| R19-1 | `/M16/contraindications/absolute/1` | [0,4) | G6PD | G/SL + 6/SN + PD/SL | 효소 코드 「G6PD」가 G/SL + 6/SN + PD/SL 로 분절 | 숫자 6 이 수사(SN)로 분리 — 수량 후보로 오인될 수 있음 |

규칙 기반 표현 후보 216건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S07"` 에 있다. 후보이며 전수 의미 해석이 아니다.
