# 02 고객

2026-11-03 사용자와 정함. 공통 규칙은 [README.md](README.md) 「모든 테이블에 공통」.

## 정한 것

- **고객은 병원별로 1명이다.** 같은 사람이 두 지점에 다니면 고객 행이 둘이다 — **브랜드 안에서 묶지 않는다**(사용자 2026-11-03).
  각 병원이 독립 운영 주체이고, 본사(브랜드)는 소속 지점 데이터를 조회만 한다. KOS 내원객도 테넌트(지점)마다 따로 있다.
- 테이블: `customer` · 코드 `customer_type` · `customer_category`(+ `customer_category_link`) · `funnel_category` · `funnel`.
- **최종 목표는 DAY 자체만 쓰는 것**이고 KOS · Vegas 는 뗀다(사용자 2026-11-03). 그래서 `customer` 에 업체 칸을 두지 않고,
  외부 id 는 공통 `external_ref` 한 테이블에만 둔다(아래).
- **연동 기간에는 외부 CRM 이 원장이다**(사용자 2026-11-03). 고객 생성 · 수정의 기준은 외부 CRM 이고 DAY 는 받아 적는다.
- **차트번호는 하나(`customer.chart_number`, 병원 안 유일)** — 연동 기간에는 외부 CRM 차트번호를 그대로 받아 적고
  DAY 가 발급하지 않는다. 자체 운영으로 넘어가면 그 번호를 이어서 DAY 가 발급한다. 직원이 쓰던 번호가 바뀌지 않는다.

## 다른 주제로 보낸 것

| cc 테이블 / KOS 값 | 어디로 | 이유 |
|---|---|---|
| `isNew`(신환 여부) | 3번 예약 / 방문 | KOS 에서도 고객이 아니라 일정(스케줄)에 달린 값 |
| `visitorType`(고객 수가 유형) | 3번 예약 / 방문 · 또는 범위 밖 | 일정 안에서 읽히는 값 |
| `identity_check` · `id_photo` · `questionnaire_history` | 7번 접수 | 고객을 가리키는 접수 기록 |
| 선불카드 · 시술권 | 범위 밖(지금) | 고객 상세 화면에는 나오지만 cc 기능이 쓰지 않았다 |

## 검토

2026-11-03 사용자 검토(https://claude.ai/artifact/YSBxTAMpNmBSL7jxKfHFXi) — 57칸 중 승인 53 · 반려 4.

- 1:1 은 전부 `customer` 한 테이블에 둔다 — 나누면 조인 비용이 더 크다(사용자). 나누는 것은 1:N · N:M · 코드 목록뿐.
- 반려: `legacy_notes`(KOS `migratedMemo` — `customer_notes` 와 같은 노트) · `unni_information`(필요할 때 따로 이관) ·
  `custom_attributes`(KOS 고객 정의 항목 — 명동점 정의 0개) · `line_information`(뺌 — 아래).
- SNS 계정은 고객당 하나만 입력한다(사용자) — `customer.sns_type` · `sns_account_id`. LINE ID 도 여기(`sns_type = line`).
- KOS `lineInformation[]` 은 사람이 입력하는 LINE ID 가 아니다(KOS OpenAPI `VisitorConnectedInformation.Line`): 고객이
  KOS Connect 예약 화면을 LINE 안(LIFF)에서 열 때 KOS 가 자동으로 붙이는 연동 정보 — `channelId`(병원 LINE 공식 계정) ·
  `id`(LINE 사용자 id — 내부용, LINE ID 와 다름) · `displayName` · `liffId`. 용도는 KOS 의 중복 고객 찾기 · LINE 메시지 발송.
  LINE 메시지는 Linky 가 보내므로 DAY 에 두지 않는다(사용자 2026-11-03). 강남언니 연동 정보(`unniInformation`)도 같은 종류.
- LINE 은 메시지를 보내려고 연동하는 것이고 메시지는 Linky 에서 보낸다 — **DAY 는 계정 id 만 알면 된다**(사용자).
- 코드 테이블(`customer_type` · `customer_category` · `funnel` · `funnel_category`)은 외부 CRM 코드를 받아 맞춘다(미러링).

## `customer` — 고객 (병원별)

외부 CRM 고객 정보를 전부 담는다(README 「DAY 테이블이 더 크다」). 연동 기간엔 외부가 원장, DAY 는 동기화.

| 묶음 | 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|---|
| 식별 | `id` | uuid PK | ✓ | | — |
| | `hospital_id` | uuid FK → `hospital` | ✓ | 고객은 병원별 1명 | — |
| | `chart_number` | varchar | ✓ | 병원 안 유일. 연동 기간엔 외부 값을 받아 적는다 | `chartNumber` |
| | `registered_at` | timestamptz | | 병원에 처음 등록된 시각 | `createdDateTimeUtc` |
| | `deleted_at` | timestamptz | | 소프트 딜리트(README 「삭제」) — 외부에서 지워지면 그 시각을 채운다 | `deleted` |
| 이름 | `name` | varchar | ✓ | | `name` |
| | `name_pronunciation` | varchar | | 이름의 한글 발음 — 외국인 고객용 | `phoneticName` |
| | `passport_surname` · `passport_given_names` | varchar | | 여권 영문 성 · 이름 | 같은 이름 |
| 인적 | `gender` | enum | | | `gender` |
| | `birth_date` | date | | | `dateOfBirth`(문자열) |
| | `nationality` · `language` | varchar | | | 같은 이름 |
| 신원 | `registration_number` | 암호화 text | | 주민등록번호 | 같은 이름 |
| | `foreign_registration_number` | 암호화 text | | 외국인 등록번호 | 같은 이름 |
| | `passport_number` | 암호화 text | | 여권번호 | 같은 이름 |
| | `passport_expiry_date` | date | | | 같은 이름 |
| 연락 | `phone_country_code` · `phone_number` | varchar | | | `phoneNumber`(공개 API) |
| | `additional_phone_country_code` · `additional_phone_number` | varchar | | | `additionalPhoneNumber` |
| | `email` | varchar | | | `email` |
| | `address` · `address_detail` · `zip_code` | varchar | | | `address{…}` |
| | `sns_type` | enum `etc` · `kakaotalk` · `line` · `instagram` · `whatsapp` · `wechat` | | SNS 종류 — 고객이 알려 준 계정 하나 | `snsInfo.snsType` |
| | `sns_account_id` | varchar | | SNS 계정 id(예: 고객이 알려 준 LINE ID). 메시지는 Linky 가 보낸다 | `snsInfo.accountId` |
| 관리 | `customer_notes` | text | | 고객 특이사항 · 주의사항. 시술실에 보인다 | `memo` |
| | `customer_type_id` | uuid FK → `customer_type` | | 고객 수가 유형(가격 등급) | `visitorType.id` |
| | `assigned_doctor_id` · `assigned_counselor_id` | uuid FK → 직원(4번) | | 지정 의사 · 상담사 | `doctor` · `counselor` |
| 유입 | `funnel_id` | uuid FK → `funnel` | | 최초 유입 채널 | `visitorFunnel.funnelId` |
| | `funnel_detail` | varchar | | 상세 유입 채널(자유 입력) | `visitorFunnel.funnelDetail` |
| | `referrer_customer_id` · `referrer_staff_id` | uuid FK | | 추천한 고객 · 직원 | 관리 정보 `visitor` · `account` |
| | `referrer_name` | varchar | | 추천인 이름만 있을 때 | `recommenderName` |
| 동의 | `agreed_personal_info` · `agreed_marketing` · `agreed_informational` | bool | | 개인정보 · 광고 · 정보성 수신 | 동의 3개 |
| 시각 | `created_at` · `updated_at` | timestamptz | ✓ | DAY 행 생성 · 수정 (동기화 칸은 `external_ref`) | — |

제약: (`hospital_id`, `chart_number`) 유일. 인덱스: 이름 · 전화번호 검색.

다른 곳으로: `is_new` → 3번 방문(방문마다 달라짐) · `last_visited_at` → 방문 기록에서 계산.

## `external_ref` — 외부 CRM 연결 (모든 테이블 공통 · 한 테이블)

외부 id 를 담는 테이블은 이것 하나다(사용자 2026-11-03). KOS · Vegas 를 뗄 때 이 테이블째 지운다.
고객 · 코드 · 이후 예약 · 직원 · 방 · 시술도 전부 여기에 넣는다.

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | uuid PK | ✓ | |
| `hospital_id` | uuid FK → `hospital` | ✓ | |
| `entity_type` | enum | ✓ | 어느 DAY 테이블인지 — `customer` · `customer_type` · `customer_category` · `funnel` · `funnel_category` · … |
| `entity_id` | uuid | ✓ | 그 테이블의 행 id (테이블이 여럿이라 FK 는 걸지 않는다 — 핵심 행은 소프트 딜리트라 지워지지 않는다) |
| `vendor` | enum `kos` · `vegas` | ✓ | |
| `external_id` | varchar | ✓ | 외부 id |
| `external_number` | varchar | | 사람이 보는 외부 번호 — 고객이면 외부 차트번호 |
| `external_updated_at` | timestamptz | | 외부 수정 시각 — 바뀐 것만 받기 |
| `synced_at` | timestamptz | | 마지막으로 외부에서 받은 시각 |
| `is_present_in_source` | bool | ✓ | 마지막 조회에 외부에 있었나 — 외부에서 사라지면 false |
| `linked_at` | timestamptz | ✓ | 처음 연결(= DAY 가 처음 받은 시각, 또는 DAY 에서 만들어 외부에 등록된 시각) |
| `unlinked_at` | timestamptz | | 업체를 바꾸거나 뗄 때 닫는다. 행은 남긴다 |
| `created_at` · `updated_at` | timestamptz | ✓ | 생성 · 수정 |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 |

제약: (`hospital_id`, `vendor`, `entity_type`, `external_id`) 유일. 인덱스: (`entity_type`, `entity_id`).

## 코드 테이블 (병원별 · 외부 CRM 코드를 미러링)

| 테이블 | 필드 | 외부(KOS) |
|---|---|---|
| `customer_type` | `id` · `hospital_id` · `name` · `deleted_at` · 생성/수정 시각 | 고객 수가 유형 |
| `customer_category` | `id` · `hospital_id` · `name` · `color` · `sort_order` · `is_closed` · `deleted_at` · 생성/수정 시각 | `get-codes VISITOR_CATEGORY` |
| `funnel_category` | `id` · `hospital_id` · `name` · `sort_order` · `is_closed` · `deleted_at` · 생성/수정 시각 | `get-codes FUNNEL_CATEGORY` |
| `funnel` | `id` · `hospital_id` · `category_id` → `funnel_category` · `name` · `sort_order` · `is_closed` · `is_default` · `deleted_at` · 생성/수정 시각 | `get-codes FUNNEL` |
| `customer_category_link` | `customer_id` + `category_id` (PK) · `deleted_at` · 생성/수정 시각 | `visitorCategories[]` |

코드의 외부 id 도 `external_ref` 에 둔다.
화면에서는 코드 목록을 메모리에 올려 이름을 붙인다 — 목록 조회에 조인을 늘리지 않는다.

## 외부(KOS) 원본 참고

### 내부 API `visitor/v2/queries/get-visitor` — KOS 웹 고객 상세 화면이 부르는 것

출처: `har/고객상세.har`(사용자 2026-11-03 · **운영 명동점 테넌트** — gitignore, 값은 옮기지 않는다). 필드 이름 · 타입만.

| 묶음 | KOS 칸 |
|---|---|
| 식별 | `id` · `chartNumber` · `deleted` · `createdDateTimeUtc` · `updatedDateTimeUtc` |
| 이름 | `name` · `phoneticName` · `passportSurname` · `passportGivenNames` |
| 인적 | `gender` · `dateOfBirth` · `nationality` · `language` · `registrationNumber` · `foreignRegistrationNumber` · `passportNumber` |
| 연락 | `address{address, detailedAddress, zipCode}` · `snsInfo{snsType, accountId}` · `lineInformation[]` · `unniInformation[]`(강남언니) — **전화번호는 이 응답에 없다** |
| 관리 | `memo`(특이사항) · `migratedMemo`(이관 메모) · `visitorType{id,name}`(수가 유형) · `visitorCategories[]` · `visitorCategoryId` · `doctor{id,name}`(지정 의사) · `counselor{id,name}`(지정 상담사) · `customAttributes[]` |
| 유입 | `visitorFunnel{funnelCategoryId, funnelId, funnelDetail}` · 옛 칸 `funnel` · `detailedFunnel` · `recommenderName`(추천인 이름) |
| 동의 | `aggrementPersonalInformation` · `aggrementAdvertisements` · `agreementInformationalNotification` |
| 방문 | `isNew` · `lastVisitedDateTimeUtc` |

같은 화면이 부르는 코드 목록(`meta/codes/v1/queries/get-codes`, 응답 `{id, category, name, order, closed, default|color}`):
`FUNNEL`(유입 채널) · `FUNNEL_CATEGORY`(유입 채널 카테고리 — 명동점은 비어 있음) · `VISITOR_CATEGORY`(고객분류 — `color` 있음).
`get-custom-attribute-definitions`(병원별 추가 항목 정의)는 명동점에서 비어 있다.

**내부 API 고객에는 `updatedDateTimeUtc` 가 있다** — 바뀐 고객만 골라 받을 수 있는지 확인할 것(공개 API `getVisitor` 에는 없다).

### 공개 API (2026-11-03 데모 지점 조회)

- `getVisitor` → `id` · `chartNumber` · `name` · `phoneNumber{countryCode, phoneNumber}` · `dateOfBirth` · `gender` · `nationality`
- 일정 안 `visitor` → 위에 더해 `memo` · `visitorType{id,name}` · `isNew` · `categories[]` · `snsInfo{snsType, accountId}` · `phoneticName`

## 정할 것

1. `gender` 값 목록 · `nationality` · `language` 형식(코드인지 이름인지) — KOS 값 확인 뒤.
