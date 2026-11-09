# S03 — `M12` (MTS (마이크로니들 치료)) · extracted.json 1차 조사

> 구획 S03 · 소유 Pointer `/M12` 와 그 아래 54개 노드(말단 40). 문맥 참조: 루트 `""`, `/M12/name`, `/M12/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 1 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M12)` | `/M12` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M12/name` | string | MTS (마이크로니들 치료) | 분석 |
| 3 | `safety` | `/M12/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M12/safety/common` | array | (array · 3) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M12/safety/common/0` | string | 시술 중 약간의 출혈과 진물 | 분석 |
| 6 | `safety.common[1]` | `/M12/safety/common/1` | string | 시술 후 피부가 빨개지고 약간 부을 수 있음 (1~2일 내 호전) | 분석 |
| 7 | `safety.common[2]` | `/M12/safety/common/2` | string | 출혈에 의해 일시적으로 멍이 들 수 있음 | 분석 |
| 8 | `safety.serious` | `/M12/safety/serious` | array | (array · 1) | —(컨테이너) |
| 9 | `safety.serious[0]` | `/M12/safety/serious/0` | string | 쾨브너현상 (건선 등 피부질환이 있는 환자에서 시술 부위에 병변이 새로 생기는 현상) | 분석 |
| 10 | `safety.uncommon` | `/M12/safety/uncommon` | array | (array · 3) | —(컨테이너) |
| 11 | `safety.uncommon[0]` | `/M12/safety/uncommon/0` | string | 감염 (무균 관리가 안 될 경우) | 분석 |
| 12 | `safety.uncommon[1]` | `/M12/safety/uncommon/1` | string | 색소침착 (특히 진피까지 깊이 치료한 경우) | 분석 |
| 13 | `safety.uncommon[2]` | `/M12/safety/uncommon/2` | string | 알레르기성 접촉피부염 (도포 약물에 의한 반응) | 분석 |
| 14 | `source` | `/M12/source` | string | 임상적 피부관리 22장 | 분석 |
| 15 | `name_en` | `/M12/name_en` | string | Microneedle Therapy System (Microneedling) | 분석 |
| 16 | `overview` | `/M12/overview` | string | MTS는 아주 가느다란 바늘이 많이 달린 롤러나 스탬프로 피부에 미세한 구멍을 내서, 피부가 스스로 상처를 치유하는 과정에서 콜라겐(피부 탄력 단백질)이 새로 만들어지게 유도하는 시술이다. 바늘 구멍을 통해 비타민, 히알루론산 등 유효 성분의 흡수를 높이는 효과도 있다. 고대부터 내려오는 자연적 상처치유 원리를 현대 과학으로 재정립한 시술이다. | 분석 |
| 17 | `aftercare` | `/M12/aftercare` | array | (array · 4) | —(컨테이너) |
| 18 | `aftercare[0]` | `/M12/aftercare/0` | string | 시술 후 보습제와 자외선차단제 꼭 사용하기 | 분석 |
| 19 | `aftercare[1]` | `/M12/aftercare/1` | string | 가벼운 세안과 샤워는 괜찮지만, 탕목욕이나 사우나는 피하기 | 분석 |
| 20 | `aftercare[2]` | `/M12/aftercare/2` | string | 출혈이 생긴 정도로 진피까지 치료한 경우 2~4일 화장 피하기 | 분석 |
| 21 | `aftercare[3]` | `/M12/aftercare/3` | string | 롤러는 반드시 멸균 상태에서 1회용으로 사용할 것 | 분석 |
| 22 | `mechanism` | `/M12/mechanism` | string | MTS 롤러의 미세한 바늘(0.2~2.0mm)이 피부 표피층과 진피층을 자극하면, 피부에 작은 상처가 생긴다. 이 상처를 회복하기 위해 PDGF, TGF-α/β 등 다양한 성장인자(세포 성장을 돕는 단백질)가 분비되고, 이들이 섬유모세포(콜라겐을 만드는 세포)를 활성화시킨다. 그 결과 새로운 콜라겐과 엘라스틴(피부 탄력 성분)이 만들어져 피부 탄력이 좋아지고, 각질층도 두꺼워진다. 흉터 부위에 시술하면 흉터의 콜라겐 밴드를 물리적으로 끊어줘서 흉터가 부드러워진다. 또한 피부에 미세한 물리적 구멍을 만들어 유효 성분의 경피흡수(피부를 통한 흡수)를 크게 높여준다. | 분석 |
| 23 | `indications` | `/M12/indications` | object | (object · 2) | —(컨테이너) |
| 24 | `indications.primary` | `/M12/indications/primary` | array | (array · 3) | —(컨테이너) |
| 25 | `indications.primary[0]` | `/M12/indications/primary/0` | string | 피부 노화 개선 (주름, 잔주름, 피부 탄력 저하) | 분석 |
| 26 | `indications.primary[1]` | `/M12/indications/primary/1` | string | 여드름흉터 | 분석 |
| 27 | `indications.primary[2]` | `/M12/indications/primary/2` | string | 피부결 개선 | 분석 |
| 28 | `indications.extended` | `/M12/indications/extended` | array | (array · 5) | —(컨테이너) |
| 29 | `indications.extended[0]` | `/M12/indications/extended/0` | string | 색소침착 개선 (약물 투입과 병행 시) | 분석 |
| 30 | `indications.extended[1]` | `/M12/indications/extended/1` | string | 탈모 치료 (두피 MTS + PRP 또는 성장인자) | 분석 |
| 31 | `indications.extended[2]` | `/M12/indications/extended/2` | string | 넓은 모공 개선 | 분석 |
| 32 | `indications.extended[3]` | `/M12/indications/extended/3` | string | 각종 유효 성분(비타민, 플라센타, 히알루론산 등) 흡수 촉진 | 분석 |
| 33 | `indications.extended[4]` | `/M12/indications/extended/4` | string | 수술 후 흉터 개선 | 분석 |
| 34 | `source_type` | `/M12/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 35 | `extracted_at` | `/M12/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 36 | `procedure_id` | `/M12/procedure_id` | string | M12-MTS | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 37 | `onset_duration` | `/M12/onset_duration` | object | (object · 3) | —(컨테이너) |
| 38 | `onset_duration.peak` | `/M12/onset_duration/peak` | string | 3~6회 반복시술 후 최대 효과 (콜라겐 리모델링에 수주~수개월 소요) | 분석 |
| 39 | `onset_duration.onset` | `/M12/onset_duration/onset` | string | 시술 후 1~2주부터 피부결 개선 느껴짐 | 분석 |
| 40 | `onset_duration.duration` | `/M12/onset_duration/duration` | string | 반복시술 시 피부가 점점 두꺼워지고 효과가 누적됨 | 분석 |
| 41 | `contraindications` | `/M12/contraindications` | object | (object · 2) | —(컨테이너) |
| 42 | `contraindications.absolute` | `/M12/contraindications/absolute` | array | (array · 4) | —(컨테이너) |
| 43 | `contraindications.absolute[0]` | `/M12/contraindications/absolute/0` | string | 피부에 감염성 질환이 있는 경우 | 분석 |
| 44 | `contraindications.absolute[1]` | `/M12/contraindications/absolute/1` | string | 심한 여드름이 진행 중인 경우 | 분석 |
| 45 | `contraindications.absolute[2]` | `/M12/contraindications/absolute/2` | string | 조절이 안 되는 당뇨병 | 분석 |
| 46 | `contraindications.absolute[3]` | `/M12/contraindications/absolute/3` | string | 켈로이드 체질 (흉터가 비정상적으로 부풀어오르는 체질) | 분석 |
| 47 | `contraindications.relative` | `/M12/contraindications/relative` | array | (array · 2) | —(컨테이너) |
| 48 | `contraindications.relative[0]` | `/M12/contraindications/relative/0` | string | 출혈성 질환이 있거나 아스피린 등 혈액 응고에 영향을 주는 약을 복용 중인 경우 주의 | 분석 |
| 49 | `contraindications.relative[1]` | `/M12/contraindications/relative/1` | string | 혈액으로 인한 감염성 질환이 있는 경우 주의 | 분석 |
| 50 | `guardrail_version` | `/M12/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 51 | `related_techniques` | `/M12/related_techniques` | array | (array · 3) | —(컨테이너) |
| 52 | `related_techniques[0]` | `/M12/related_techniques/0` | string | MTS + PRP — 미세 구멍 후 PRP 도포로 피부 재생 효과 극대화 | 분석 |
| 53 | `related_techniques[1]` | `/M12/related_techniques/1` | string | MTS + 약물 투입 — 비타민C, 히알루론산 등 유효 성분 경피 흡수 촉진 | 분석 |
| 54 | `related_techniques[2]` | `/M12/related_techniques/2` | string | 프랙셔널 레이저 — 비슷한 원리(미세 열손상 → 재생)이지만 레이저 에너지 사용 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S03-01** (B) onset_duration/duration 에 기간 값이 없고 누적 경향만 있다. peak 의 괄호 「수주~수개월」도 범위어다. → B3  
  근거: `/M12/onset_duration/duration` 「효과가 누적됨」; `/M12/onset_duration/peak` 「수주~수개월」
- **OB-S03-02** (P) mechanism 의 「(0.2~2.0mm)」는 「미세한 바늘」 뒤 괄호다. 바늘 길이로 읽히지만 원문은 길이·깊이라고 쓰지 않았다. safety 의 「진피까지 깊이 치료한 경우」, aftercare 의 「출혈이 생긴 정도로 진피까지 치료한 경우」는 치료 깊이를 층(진피)과 징후(출혈)로 표현한다. → F4  
  근거: `/M12/mechanism` 「미세한 바늘(0.2~2.0mm)」; `/M12/safety/uncommon/1` 「진피까지 깊이 치료한 경우」; `/M12/aftercare/2` 「출혈이 생긴 정도로 진피까지 치료한 경우」
- **OB-S03-03** (P) indications/extended 「탈모 치료 (두피 MTS + PRP 또는 성장인자)」는 부위(두피)·기법 조합(+)·대안(또는)이 한 괄호에 있다. 「+」와 「또는」의 결합 범위(MTS+PRP 또는 MTS+성장인자?)는 원문만으로 정해지지 않는다. → F2, F7  
  근거: `/M12/indications/extended/1` 「두피 MTS + PRP 또는 성장인자」
- **OB-S03-04** (구조) relative 금기 두 값이 「… 경우 주의」로 끝난다. relative 그룹 안에서 권고어(주의)가 값마다 붙기도 하고 안 붙기도 한다. → F7  
  근거: `/M12/contraindications/relative/0` 「경우 주의」; `/M12/contraindications/relative/1` 「경우 주의」
- **OB-S03-05** (F) overview 「고대부터 내려오는 자연적 상처치유 원리」는 역사 주장이다. 사실 검증하지 않았다. → F8  
  근거: `/M12/overview` 「고대부터 내려오는」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX023 | possibility_with_time | `/M12/safety/common/1` | 약간 부을 수 있음 (1~2일 내 호전) |  |
| MX024 | population_subgroup | `/M12/safety/serious/0` | 건선 등 피부질환이 있는 환자에서 |  |
| MX025 | negated_condition | `/M12/safety/uncommon/0` | (무균 관리가 안 될 경우) |  |
| MX026 | depth_condition | `/M12/safety/uncommon/1` | (특히 진피까지 깊이 치료한 경우) | 「깊이」 = 치료 깊이(진피까지). mm 없음 |
| MX027 | permission_vs_avoidance | `/M12/aftercare/1` | 가벼운 세안과 샤워는 괜찮지만, 탕목욕이나 사우나는 피하기 |  |
| MX028 | condition_threshold_time_window | `/M12/aftercare/2` | 출혈이 생긴 정도로 진피까지 치료한 경우 2~4일 화장 피하기 |  |
| MX029 | obligation | `/M12/aftercare/3` | 반드시 멸균 상태에서 1회용으로 사용할 것 |  |
| MX030 | quantity_with_target | `/M12/mechanism` | 미세한 바늘(0.2~2.0mm) | 바늘 길이로 읽히나 원문은 길이라고 적지 않음(잠정) |
| MX031 | site_condition | `/M12/mechanism` | 흉터 부위에 시술하면 |  |
| MX032 | condition_combination | `/M12/indications/extended/0` | (약물 투입과 병행 시) |  |
| MX033 | symbol_combination | `/M12/indications/extended/1` | 두피 MTS + PRP 또는 성장인자 | 「+」와 「또는」이 한 구절에 함께 |
| MX034 | count_anchor | `/M12/onset_duration/peak` | 3~6회 반복시술 후 최대 효과 |  |
| MX035 | time_range_word | `/M12/onset_duration/peak` | (콜라겐 리모델링에 수주~수개월 소요) |  |
| MX036 | field_content_without_time | `/M12/onset_duration/duration` | 반복시술 시 피부가 점점 두꺼워지고 효과가 누적됨 | duration 칸에 기간 값 없음(B3) |
| MX037 | negated_condition | `/M12/contraindications/absolute/2` | 조절이 안 되는 당뇨병 |  |
| MX038 | medication_condition | `/M12/contraindications/relative/0` | 아스피린 등 혈액 응고에 영향을 주는 약을 복용 중인 경우 주의 |  |
| MX039 | comparison_contrast | `/M12/related_techniques/2` | 비슷한 원리(미세 열손상 → 재생)이지만 레이저 에너지 사용 |  |
| MX182 | historical_claim | `/M12/overview` | 고대부터 내려오는 자연적 상처치유 원리를 현대 과학으로 재정립한 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|

규칙 기반 표현 후보 252건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S03"` 에 있다. 후보이며 전수 의미 해석이 아니다.
