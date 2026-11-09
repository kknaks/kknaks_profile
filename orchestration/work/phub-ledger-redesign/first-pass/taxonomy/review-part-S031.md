# S031 — M9 기기 리프팅

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/8/name`
- 단위: M9-P-6, name
- 상위 문맥(공동 참조·소유 아님): `/modality/8` M9 / 기기 리프팅 / 기기 리프팅
- 기계 기록: `source-map.json`(section=S031) · `morphology/S031.json` · `expressions.json`(section=S031) · 읽기 렌더 `reading/S031.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/8/products/6` | products[6] | object | {object, 키 8: id, name, name_en, manufacturer, country, mfds, type, extracted} |
| `/modality/8/products/6/id` | id | string | M9-P-6 |
| `/modality/8/products/6/name` | name | string | LDM |
| `/modality/8/products/6/name_en` | name_en | string | LDM-MED |
| `/modality/8/products/6/manufacturer` | manufacturer | string | 제이시스메디칼 |
| `/modality/8/products/6/country` | country | string | KR |
| `/modality/8/products/6/mfds` | mfds | null | null |
| `/modality/8/products/6/type` | type | string | 초음파 |
| `/modality/8/products/6/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/products/6/extracted/overview` | overview | string | RF 기술 기반의 피부 리프팅 기기로 심부 콜라겐 수축과 신생 콜라겐 생성을 유도한다. |
| `/modality/8/products/6/extracted/mechanism` | mechanism | string | 이온진동을 통해 조직 내 이온의 운동으로 심부 열을 발생시킨다. 이를 통해 기존 콜라겐의 즉각적 수축과 장기적 신생 콜라겐 생성으로 피부 탄력을 회복시킨다. |
| `/modality/8/products/6/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/products/6/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/8/products/6/extracted/indications/primary/0` | primary[0] | string | 얼굴 처짐 |
| `/modality/8/products/6/extracted/indications/primary/1` | primary[1] | string | 목 주름 |
| `/modality/8/products/6/extracted/indications/primary/2` | primary[2] | string | 팔뚝 처짐 |
| `/modality/8/products/6/extracted/indications/primary/3` | primary[3] | string | 복부 탄력 저하 |
| `/modality/8/products/6/extracted/indications/primary/4` | primary[4] | string | 전반적 피부 탄력 개선 |
| `/modality/8/products/6/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/8/products/6/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/8/products/6/extracted/safety/common/0` | common[0] | string | 시술 직후 홍반 |
| `/modality/8/products/6/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/8/products/6/extracted/safety/common/2` | common[2] | string | 일시적 감각 이상 |
| `/modality/8/products/6/extracted/safety/common/3` | common[3] | string | 화상(부적절한 사용 시) |
| `/modality/8/products/6/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/products/6/extracted/onset_duration/onset` | onset | string | 즉시 효과 + 점진적 개선(2-3개월) |
| `/modality/8/products/6/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/8/products/6/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/8/products/6/extracted/aftercare/0` | aftercare[0] | string | 24시간 고온 노출 피하기(사우나, 찜질방) |
| `/modality/8/products/6/extracted/aftercare/1` | aftercare[1] | string | 자극적 화장품 최소 1주일 사용 금지 |
| `/modality/8/products/6/extracted/aftercare/2` | aftercare[2] | string | 냉찜질로 부종 관리 |
| `/modality/8/products/6/extracted/aftercare/3` | aftercare[3] | string | 자외선 차단 필수 |
| `/modality/8/products/6/extracted/aftercare/4` | aftercare[4] | string | 충분한 수분 섭취 |
| `/modality/8/name` | name | string | 기기 리프팅 |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| I | `/modality/8/products/6/type`, `/modality/8/products/6/extracted/overview`, `/modality/8/products/6/extracted/mechanism` | LDM 제품 type '초음파' 인데 overview 'RF 기술 기반', mechanism '이온진동 … 심부 열'(RF 서술). type 과 서술의 에너지원이 다르다. |
| P | `/modality/8/products/6/name`, `/modality/8/products/6/name_en` | name 'LDM', name_en 'LDM-MED' — 영문명이 더 길다. M9 subcategories items 에 LDM 항목은 없다(제품만). |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/8/products/6/extracted/safety/common/3` | [0, 13] | 화상(부적절한 사용 시) | 조건 | common 칸의 조건부 화상 |
| `/modality/8/products/6/extracted/onset_duration/onset` | [0, 21] | 즉시 효과 + 점진적 개선(2-3개월) | 기호, 수량·단위·시간, 범위 | '+' = 그리고 |
| `/modality/8/products/6/extracted/aftercare/1` | [0, 20] | 자극적 화장품 최소 1주일 사용 금지 | 범위, 수량·단위·시간, 부정 |  |

## 형태소 분석 확인 (알려진 오분절 K)

(없음)

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S031-I01 | I | `/modality/8/products/6/type`, `/modality/8/products/6/extracted/overview` | LDM type(초음파) vs RF 서술. | 에너지원 속성 채택 시 확인 |

