# S05 — `M14` (크라이오리포라이시스) · extracted.json 1차 조사

> 구획 S05 · 소유 Pointer `/M14` 와 그 아래 52개 노드(말단 38). 문맥 참조: 루트 `""`, `/M14/name`, `/M14/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 2 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M14)` | `/M14` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M14/name` | string | 크라이오리포라이시스 | 분석 |
| 3 | `safety` | `/M14/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M14/safety/common` | array | (array · 5) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M14/safety/common/0` | string | 시술 부위 홍반 (빨개짐) | 분석 |
| 6 | `safety.common[1]` | `/M14/safety/common/1` | string | 붓기 | 분석 |
| 7 | `safety.common[2]` | `/M14/safety/common/2` | string | 멍 | 분석 |
| 8 | `safety.common[3]` | `/M14/safety/common/3` | string | 일시적 감각 저하 (저림, 무감각) | 분석 |
| 9 | `safety.common[4]` | `/M14/safety/common/4` | string | 시술 중 당기는 느낌과 냉감 | 분석 |
| 10 | `safety.serious` | `/M14/safety/serious` | array | (array · 1) | —(컨테이너) |
| 11 | `safety.serious[0]` | `/M14/safety/serious/0` | string | 역설적 지방 증식 (Paradoxical Adipose Hyperplasia, PAH) -- 극히 드물게 시술 부위 지방이 오히려 커지는 현상 | 분석 |
| 12 | `safety.uncommon` | `/M14/safety/uncommon` | array | (array · 2) | —(컨테이너) |
| 13 | `safety.uncommon[0]` | `/M14/safety/uncommon/0` | string | 시술 부위 통증 (수일~수주 지속) | 분석 |
| 14 | `safety.uncommon[1]` | `/M14/safety/uncommon/1` | string | 피부 경결 (딱딱해지는 느낌) | 분석 |
| 15 | `source` | `/M14/source` | string | 일반 의학 지식 | 분석 |
| 16 | `name_en` | `/M14/name_en` | string | Cryolipolysis | 분석 |
| 17 | `overview` | `/M14/overview` | string | 크라이오리포라이시스는 지방세포가 다른 세포보다 추위에 약한 성질을 이용해, 피부를 차갑게 냉각시켜 지방세포만 선택적으로 파괴하는 비수술적 지방 감소 시술이다. 한국에서는 '쿨스컬프팅(젤틱)', '크라이오' 등의 브랜드명으로 알려져 있다. | 분석 |
| 18 | `aftercare` | `/M14/aftercare` | array | (array · 3) | —(컨테이너) |
| 19 | `aftercare[0]` | `/M14/aftercare/0` | string | 특별한 다운타임 없이 일상생활 바로 가능 | 분석 |
| 20 | `aftercare[1]` | `/M14/aftercare/1` | string | 시술 부위를 가볍게 마사지하면 효과 촉진 | 분석 |
| 21 | `aftercare[2]` | `/M14/aftercare/2` | string | 건강한 식이와 운동 병행 권장 | 분석 |
| 22 | `mechanism` | `/M14/mechanism` | string | 어플리케이터(시술 기구)가 피부와 지방 조직을 흡입하면서 영하 10도 전후의 저온으로 냉각시킨다. 지방세포(adipocyte)는 다른 피부 세포보다 추위에 민감하여, 일정 온도 이하로 내려가면 지방세포 내부에 결정(크리스탈)이 형성되면서 세포가 손상된다. 손상된 지방세포는 수 주에 걸쳐 자연사(세포자멸사, apoptosis)하고, 몸의 면역 체계(대식세포)에 의해 자연스럽게 분해되어 체외로 배출된다. 주변의 피부, 근육, 신경 조직은 손상 없이 보존된다. | 분석 |
| 23 | `indications` | `/M14/indications` | object | (object · 2) | —(컨테이너) |
| 24 | `indications.primary` | `/M14/indications/primary` | array | (array · 2) | —(컨테이너) |
| 25 | `indications.primary[0]` | `/M14/indications/primary/0` | string | 운동/식이요법으로 빠지지 않는 국소 지방 감소 (복부, 옆구리, 허벅지 등) | 분석 |
| 26 | `indications.primary[1]` | `/M14/indications/primary/1` | string | 이중턱 지방 감소 | 분석 |
| 27 | `indications.extended` | `/M14/indications/extended` | array | (array · 4) | —(컨테이너) |
| 28 | `indications.extended[0]` | `/M14/indications/extended/0` | string | 팔뚝 지방 감소 | 분석 |
| 29 | `indications.extended[1]` | `/M14/indications/extended/1` | string | 브래지어 라인 지방 | 분석 |
| 30 | `indications.extended[2]` | `/M14/indications/extended/2` | string | 무릎 위 지방 | 분석 |
| 31 | `indications.extended[3]` | `/M14/indications/extended/3` | string | 등 지방 | 분석 |
| 32 | `source_type` | `/M14/source_type` | string | general | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 33 | `extracted_at` | `/M14/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 34 | `procedure_id` | `/M14/procedure_id` | string | M14-CRYO | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 35 | `onset_duration` | `/M14/onset_duration` | object | (object · 3) | —(컨테이너) |
| 36 | `onset_duration.peak` | `/M14/onset_duration/peak` | string | 시술 후 2~3개월 뒤 최종 결과 | 분석 |
| 37 | `onset_duration.onset` | `/M14/onset_duration/onset` | string | 시술 후 3~4주부터 지방 감소 체감 시작 | 분석 |
| 38 | `onset_duration.duration` | `/M14/onset_duration/duration` | string | 파괴된 지방세포는 영구적으로 제거 (체중 증가 시 남은 지방세포가 커질 수 있음) | 분석 |
| 39 | `contraindications` | `/M14/contraindications` | object | (object · 2) | —(컨테이너) |
| 40 | `contraindications.absolute` | `/M14/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 41 | `contraindications.absolute[0]` | `/M14/contraindications/absolute/0` | string | 냉글로불린혈증 (찬 온도에 의해 혈중 단백질이 굳는 질환) | 분석 |
| 42 | `contraindications.absolute[1]` | `/M14/contraindications/absolute/1` | string | 발작성 냉혈색소뇨증 (추위에 의해 혈색소가 파괴되는 질환) | 분석 |
| 43 | `contraindications.absolute[2]` | `/M14/contraindications/absolute/2` | string | 한랭두드러기 (추위에 의한 두드러기) | 분석 |
| 44 | `contraindications.relative` | `/M14/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 45 | `contraindications.relative[0]` | `/M14/contraindications/relative/0` | string | 레이노 현상 (추위에 의해 손끝/발끝이 하얗게 변하는 증상) | 분석 |
| 46 | `contraindications.relative[1]` | `/M14/contraindications/relative/1` | string | 시술 부위에 탈장이 있는 경우 | 분석 |
| 47 | `contraindications.relative[2]` | `/M14/contraindications/relative/2` | string | 시술 부위에 심한 피부 질환이 있는 경우 | 분석 |
| 48 | `guardrail_version` | `/M14/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 49 | `related_techniques` | `/M14/related_techniques` | array | (array · 3) | —(컨테이너) |
| 50 | `related_techniques[0]` | `/M14/related_techniques/0` | string | HIFES/EMS -- 근육 강화와 병합하여 바디 윤곽 개선 | 분석 |
| 51 | `related_techniques[1]` | `/M14/related_techniques/1` | string | 고주파(RF) 바디 -- 피부 타이트닝과 시너지 | 분석 |
| 52 | `related_techniques[2]` | `/M14/related_techniques/2` | string | 지방흡입 -- 더 적극적인 지방 제거가 필요한 경우 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S05-01** (P) serious 한 값 안에 사건명·영문명·약어·빈도(극히 드물게)·현상 설명이 「 -- 」로 이어져 있다. 「오히려 커지는」은 기대 효과(지방 감소)와 반대 방향이라는 표지다. → F4  
  근거: `/M14/safety/serious/0` 「역설적 지방 증식 (Paradoxical Adipose Hyperplasia, PAH) -- 극히 드물게」
- **OB-S05-02** (B) mechanism 의 「일정 온도 이하」는 임계 온도 값이 없다. 「영하 10도 전후」는 냉각 온도의 근사다. → B10  
  근거: `/M14/mechanism` 「일정 온도 이하로」; `/M14/mechanism` 「영하 10도 전후」
- **OB-S05-03** (P) duration 「영구적으로 제거」는 파괴된 지방세포의 제거에 걸리고, 괄호는 남은 지방세포가 커질 수 있다는 조건부 가능성이다. 효과 지속과 세포 제거가 한 값에 섞인다. → F5  
  근거: `/M14/onset_duration/duration` 「파괴된 지방세포는 영구적으로 제거」
- **OB-S05-04** (F) related_techniques 2·3번 값은 M10 의 2·3번 값과 글자가 같다. 같은 문자열이 다른 항목에서 반복된다. → F6  
  근거: `/M14/related_techniques/1` 「고주파(RF) 바디 -- 피부 타이트닝과 시너지」; `/M10/related_techniques/1` 「고주파(RF) 바디 -- 피부 타이트닝과 시너지」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX045 | frequency_degree_scoped | `/M14/safety/serious/0` | 극히 드물게 시술 부위 지방이 오히려 커지는 현상 |  |
| MX046 | time_range_word | `/M14/safety/uncommon/0` | (수일~수주 지속) |  |
| MX047 | quantity_approx | `/M14/mechanism` | 영하 10도 전후의 저온 |  |
| MX048 | threshold_unspecified | `/M14/mechanism` | 일정 온도 이하로 내려가면 |  |
| MX049 | negated_statement | `/M14/mechanism` | 주변의 피부, 근육, 신경 조직은 손상 없이 보존된다 |  |
| MX050 | negated_condition | `/M14/indications/primary/0` | 운동/식이요법으로 빠지지 않는 국소 지방 감소 |  |
| MX051 | possibility_condition | `/M14/onset_duration/duration` | (체중 증가 시 남은 지방세포가 커질 수 있음) |  |
| MX052 | condition_effect | `/M14/aftercare/1` | 가볍게 마사지하면 효과 촉진 |  |
| MX053 | combination_purpose | `/M14/related_techniques/0` | 근육 강화와 병합하여 바디 윤곽 개선 |  |
| MX180 | site_mention | `/M14/indications/extended/3` | 등 지방 | 부위 키워드 규칙에서 「등」(등의/등 = etc.) 오탐 때문에 제외한 부위어를 수동으로 기록 |
| MX188 | selectivity_negated_prefix | `/M14/overview` | 지방세포만 선택적으로 파괴하는 비수술적 지방 감소 시술 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R01-1 | `/M14/indications/primary/1` | [0,3) | 이중턱 | 이/MM + 중턱/NNG | 관형사 「이」 오분리 — 부위어가 MM+다른 명사로 쪼개짐 | 부위 표현 탐색 시 「이중턱」「이마」가 「중턱」「마」로 바뀜. 형태소 기반 부위 후보 추출에서 누락·오탐 |
| R11-1 | `/M14/safety/common/2` | [0,1) | 멍 | 멍/MAG | 단독 값 「멍」(타박 멍)을 부사(MAG)로 태깅 | 부작용 사건 명사가 부사로 분류 — 품사로 사건 명사를 고르면 누락. 값 자체는 원문 보존 |

규칙 기반 표현 후보 187건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S05"` 에 있다. 후보이며 전수 의미 해석이 아니다.
