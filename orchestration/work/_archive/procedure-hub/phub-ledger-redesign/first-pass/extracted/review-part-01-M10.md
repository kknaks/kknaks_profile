# S01 — `M10` (HIFES/EMS) · extracted.json 1차 조사

> 구획 S01 · 소유 Pointer `/M10` 와 그 아래 50개 노드(말단 37). 문맥 참조: 루트 `""`, `/M10/name`, `/M10/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 1 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M10)` | `/M10` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M10/name` | string | HIFES/EMS | 분석 |
| 3 | `safety` | `/M10/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M10/safety/common` | array | (array · 3) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M10/safety/common/0` | string | 시술 부위 근육통 (운동 후와 비슷한 느낌) | 분석 |
| 6 | `safety.common[1]` | `/M10/safety/common/1` | string | 일시적 근육 경련 | 분석 |
| 7 | `safety.common[2]` | `/M10/safety/common/2` | string | 시술 중 약간의 불편감 | 분석 |
| 8 | `safety.serious` | `/M10/safety/serious` | null | null | 제외: 문자열 아님 |
| 9 | `safety.uncommon` | `/M10/safety/uncommon` | array | (array · 2) | —(컨테이너) |
| 10 | `safety.uncommon[0]` | `/M10/safety/uncommon/0` | string | 시술 부위 피부 발적 (빨개짐) | 분석 |
| 11 | `safety.uncommon[1]` | `/M10/safety/uncommon/1` | string | 일시적 관절/건 불편감 | 분석 |
| 12 | `source` | `/M10/source` | string | 일반 의학 지식 | 분석 |
| 13 | `name_en` | `/M10/name_en` | string | High-Intensity Focused Electromagnetic Stimulation / EMS | 분석 |
| 14 | `overview` | `/M10/overview` | string | HIFES(고강도 집속 전자기 자극)와 EMS(전기근육자극)는 전자기 에너지를 이용해 근육을 강제로 수축시키는 시술이다. 한국에서는 '엠스컬프', '테슬라포머' 등의 브랜드명으로 알려져 있으며, 복부, 엉덩이, 팔, 다리 등의 근육 강화와 지방 감소를 목적으로 사용된다. | 분석 |
| 15 | `aftercare` | `/M10/aftercare` | array | (array · 3) | —(컨테이너) |
| 16 | `aftercare[0]` | `/M10/aftercare/0` | string | 특별한 다운타임 없이 일상생활 바로 가능 | 분석 |
| 17 | `aftercare[1]` | `/M10/aftercare/1` | string | 충분한 수분 섭취 | 분석 |
| 18 | `aftercare[2]` | `/M10/aftercare/2` | string | 운동 병행 시 효과 극대화 | 분석 |
| 19 | `mechanism` | `/M10/mechanism` | string | 고강도 집속 전자기장(HIFEM)이 운동신경을 자극하여 단시간에 수만 회의 근육 초극대 수축(supramaximal contraction)을 유발한다. 이는 일반적인 운동으로는 달성할 수 없는 강도의 근육 수축으로, 근육 섬유의 재구성(근비대)과 새로운 근섬유 생성(근섬유 증가)을 유도한다. 동시에 근육 수축으로 인해 주변 지방세포에 대사 스트레스가 가해져, 지방세포의 자연사(세포자멸사, apoptosis)가 유도되어 지방 감소 효과도 나타난다. | 분석 |
| 20 | `indications` | `/M10/indications` | object | (object · 2) | —(컨테이너) |
| 21 | `indications.primary` | `/M10/indications/primary` | array | (array · 3) | —(컨테이너) |
| 22 | `indications.primary[0]` | `/M10/indications/primary/0` | string | 복부 근육 강화 및 지방 감소 | 분석 |
| 23 | `indications.primary[1]` | `/M10/indications/primary/1` | string | 엉덩이 리프팅 (힙업) | 분석 |
| 24 | `indications.primary[2]` | `/M10/indications/primary/2` | string | 허벅지 근육 강화 | 분석 |
| 25 | `indications.extended` | `/M10/indications/extended` | array | (array · 4) | —(컨테이너) |
| 26 | `indications.extended[0]` | `/M10/indications/extended/0` | string | 팔뚝 근육 토닝 | 분석 |
| 27 | `indications.extended[1]` | `/M10/indications/extended/1` | string | 종아리 근육 강화 | 분석 |
| 28 | `indications.extended[2]` | `/M10/indications/extended/2` | string | 산후 복직근이개 (배 근육 벌어짐) 개선 | 분석 |
| 29 | `indications.extended[3]` | `/M10/indications/extended/3` | string | 골반저근 강화 (요실금 개선) | 분석 |
| 30 | `source_type` | `/M10/source_type` | string | general | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 31 | `extracted_at` | `/M10/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 32 | `procedure_id` | `/M10/procedure_id` | string | M10-HIFES | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 33 | `onset_duration` | `/M10/onset_duration` | object | (object · 3) | —(컨테이너) |
| 34 | `onset_duration.peak` | `/M10/onset_duration/peak` | string | 마지막 시술 후 2~4주 뒤 | 분석 |
| 35 | `onset_duration.onset` | `/M10/onset_duration/onset` | string | 시술 직후 근육 피로감, 2~4주 후 근육 강화 체감 | 분석 |
| 36 | `onset_duration.duration` | `/M10/onset_duration/duration` | string | 6~12개월 유지 (운동 병행 시 더 오래 유지) | 분석 |
| 37 | `contraindications` | `/M10/contraindications` | object | (object · 2) | —(컨테이너) |
| 38 | `contraindications.absolute` | `/M10/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 39 | `contraindications.absolute[0]` | `/M10/contraindications/absolute/0` | string | 체내 금속 임플란트가 시술 부위에 있는 경우 | 분석 |
| 40 | `contraindications.absolute[1]` | `/M10/contraindications/absolute/1` | string | 심장박동기(페이스메이커) 또는 이식형 제세동기 사용자 | 분석 |
| 41 | `contraindications.absolute[2]` | `/M10/contraindications/absolute/2` | string | 임신 중인 경우 | 분석 |
| 42 | `contraindications.relative` | `/M10/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 43 | `contraindications.relative[0]` | `/M10/contraindications/relative/0` | string | 간질(뇌전증) 환자 | 분석 |
| 44 | `contraindications.relative[1]` | `/M10/contraindications/relative/1` | string | 심각한 심폐질환 환자 | 분석 |
| 45 | `contraindications.relative[2]` | `/M10/contraindications/relative/2` | string | 최근 수술 이력이 있는 부위 | 분석 |
| 46 | `guardrail_version` | `/M10/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 47 | `related_techniques` | `/M10/related_techniques` | array | (array · 3) | —(컨테이너) |
| 48 | `related_techniques[0]` | `/M10/related_techniques/0` | string | 크라이오리포라이시스 (냉동지방분해) -- 지방 감소에 병합 | 분석 |
| 49 | `related_techniques[1]` | `/M10/related_techniques/1` | string | 고주파(RF) 바디 -- 피부 타이트닝과 시너지 | 분석 |
| 50 | `related_techniques[2]` | `/M10/related_techniques/2` | string | 지방흡입 -- 더 적극적인 지방 제거가 필요한 경우 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S01-01** (I) name 은 HIFES, mechanism 은 HIFEM(고강도 집속 전자기장)으로 적었다. name_en 은 Stimulation 으로 풀었다. 같은 대상의 약칭 표기가 값마다 다르다. → I1  
  근거: `/M10/name` 「HIFES/EMS」; `/M10/mechanism` 「고강도 집속 전자기장(HIFEM)」; `/M10/name_en` 「High-Intensity Focused Electromagnetic Stimulation / EMS」
- **OB-S01-02** (P) name 「HIFES/EMS」의 「/」는 overview 가 둘을 「HIFES(…)와 EMS(…)」로 함께 설명하므로 대안인지 병기인지 원문만으로 정해지지 않는다. → F11  
  근거: `/M10/overview` 「HIFES(고강도 집속 전자기 자극)와 EMS(전기근육자극)는」
- **OB-S01-03** (구조) safety/serious 가 null 이다(빈 배열이 아님). 중대한 부작용이 없다는 뜻인지 미기재인지 원문에 없다. → B1  
  근거: `/M10/safety/serious`
- **OB-S01-04** (B) relative 금기 「최근 수술 이력이 있는 부위」의 「최근」 기간이 없다. 「심각한 심폐질환」의 정도 기준도 없다. → B4, B10  
  근거: `/M10/contraindications/relative/2` 「최근 수술 이력」; `/M10/contraindications/relative/1` 「심각한 심폐질환」
- **OB-S01-05** (F) overview 의 부위 나열(복부, 엉덩이, 팔, 다리)과 indications 의 부위(복부·엉덩이·허벅지·팔뚝·종아리·골반저근)가 표현 단위가 다르다(팔/팔뚝, 다리/허벅지·종아리). 부위 체계는 정하지 않았다. → F1, F2  
  근거: `/M10/overview` 「복부, 엉덩이, 팔, 다리」; `/M10/indications/extended/0` 「팔뚝」
- **OB-S01-06** (F) related_techniques 의 「크라이오리포라이시스 (냉동지방분해)」는 이 원장 M14 name 과 같은 문자열을 포함한다. 「고주파(RF) 바디」「지방흡입」은 이 원장의 name 에 없다. 연결은 후속 과제다. → F6  
  근거: `/M10/related_techniques/0` 「크라이오리포라이시스」; `/M10/related_techniques/1` 「고주파(RF) 바디」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX001 | event_with_gloss_comparison | `/M10/safety/common/0` | 시술 부위 근육통 (운동 후와 비슷한 느낌) | 사건 + 비교 설명 괄호 |
| MX002 | duration_modifier_scoped | `/M10/safety/common/1` | 일시적 근육 경련 | 「일시적」→ 경련 |
| MX003 | time_and_degree_scoped | `/M10/safety/common/2` | 시술 중 약간의 불편감 | 시점(시술 중) + 정도(약간의) → 불편감 |
| MX004 | negated_statement | `/M10/aftercare/0` | 특별한 다운타임 없이 |  |
| MX005 | condition_effect | `/M10/aftercare/2` | 운동 병행 시 효과 극대화 | 무엇의 효과인지 생략(항목 시술로 읽힘 — 잠정) |
| MX006 | quantity_word_scoped | `/M10/mechanism` | 단시간에 수만 회의 근육 초극대 수축 |  |
| MX007 | negated_comparison | `/M10/mechanism` | 일반적인 운동으로는 달성할 수 없는 강도 |  |
| MX008 | time_window_with_anchor | `/M10/onset_duration/peak` | 마지막 시술 후 2~4주 뒤 | 기준 시점 = 마지막 시술 |
| MX009 | time_window_with_anchor | `/M10/onset_duration/onset` | 2~4주 후 근육 강화 체감 |  |
| MX010 | condition_effect | `/M10/onset_duration/duration` | (운동 병행 시 더 오래 유지) |  |
| MX011 | site_role_condition | `/M10/contraindications/absolute/0` | 시술 부위에 있는 경우 | 금기 조건이 부위에 한정 |
| MX012 | time_vague_site_condition | `/M10/contraindications/relative/2` | 최근 수술 이력이 있는 부위 | 「최근」 기간 미기재 |
| MX013 | condition_alternative | `/M10/related_techniques/2` | 더 적극적인 지방 제거가 필요한 경우 |  |
| MX181 | site_list_purpose | `/M10/overview` | 복부, 엉덩이, 팔, 다리 등의 근육 강화와 지방 감소를 목적으로 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R10-1 | `/M10/indications/extended/2` | [3,8) | 복직근이개 | 복직근/NNP + 이/JKS + 개/NNG | 「복직근이개」의 「이개」를 주격조사 「이」 + 「개」로 분절 | 질환명(복직근 이개 = 배 근육 벌어짐)이 「복직근」+조사+「개」로 바뀌어 질환 의미 소실 |

규칙 기반 표현 후보 185건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S01"` 에 있다. 후보이며 전수 의미 해석이 아니다.
