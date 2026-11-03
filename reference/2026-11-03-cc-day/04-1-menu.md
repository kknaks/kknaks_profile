# 04-1 상품 · 시술 메뉴

2026-11-03 사용자와 정함 — **KOS 메뉴 구조를 그대로 따른다.**

> **1차에서는 만들지 않는다(사용자 2026-11-03).** 시술 현황은 메뉴를 몰라도 그려지므로 1차는 cc 방식 — 작업 · 희망 시술 · 상담 시술에
> KOS 가 같이 준 이름 · 단위 · 회차를 **스냅샷으로만** 적는다. 메뉴 테이블 · 메뉴 동기화 없음. 이 문서는 자체 운영(KOS 를 뗄 때) 단계의 설계로 남긴다. 공통 규칙은 [README.md](README.md).
검토표: https://claude.ai/artifact/JKu9WADr3Beokeih6BAqwG

## 정한 것

- ~~1차는 메뉴를 1시간마다 받아 둔다~~ (2026-11-03 바뀜) — 1차는 만들지 않는다. 자체 운영 단계에서 이 구조로 만든다.
- cc-prototype 에는 메뉴 테이블이 없었다(작업 이름 문자열 · 기타 작업 종류만). 기준은 cc 가 아니라 KOS.
- 희망 시술 · 상담 시술 · 작업 · (나중에) 구매는 이 메뉴를 **참조 + 스냅샷**으로 가리킨다(README 「참조 + 스냅샷」).
- 메뉴의 KOS id 는 전부 `external_ref`. 삭제는 소프트 딜리트.

```text
product_category ◀N:M▶ product ─1:N─▶ product_option (single · group(코스) · consultation)
                                         ├─ product_option_price         수가 유형별 가격 (→ customer_type)
                                         ├─ product_option_composition   코스 구성 (→ 단품 옵션 · 진료항목 · 시술)
                                         └─▶ medical_service ─▶ procedure(진료 행위) · machine · medicine
etc_task_type  기타 작업 종류 (방 배정 · 마취 · 시트팩 · 관리 마무리)
```

데모 지점 개수(2026-11-03 공개 API 조회): 카테고리 15 · 상품 101 · 옵션 323(단품 307 · 코스 16) · 진료항목 226 · 시술 804 · 기기 302 · 약물 349.

## product_category · 상품 카테고리 (데모 15)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | id | product_category |
| `hospital_id` | uuid FK → hospital | ✓ | 메뉴는 병원별 |  | product_category |
| `name` | varchar | ✓ | 예: 보톡스 · 필러 · 리프팅 · 이벤트 | name | product_category |
| `sort_order` | int | ✓ |  | order | product_category |
| `is_open` | bool | ✓ | 노출 여부 | opened | product_category |
| `name_translations` | jsonb |  | 다국어 이름 {ko, en, ja, zh-Hans, zh-Hant} | translsMap.name | product_category |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  | deleted | product_category |

## product · 상품 (데모 101)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | id | product |
| `hospital_id` | uuid FK → hospital | ✓ | 메뉴는 병원별 |  | product |
| `title` | varchar | ✓ | 상품 이름 | title | product |
| `description` | text |  |  | description | product |
| `caution` | text |  | 주의사항 | caution · cautions[] | product |
| `is_event` | bool | ✓ | 이벤트 상품 | isEvent | product |
| `is_closed` | bool | ✓ | 사용 안 함 | closed | product |
| `sort_order` | int | ✓ |  | order | product |
| `display_from · display_to` | timestamptz |  | 노출 기간 — KOS 문서에는 있고 이번 목록 응답에는 없었다 | displayPeriod | product |
| `offering_from · offering_to` | timestamptz |  | 예약 · 수납 가능 기간 — 같은 이유 | offeringPeriod | product |
| `badges` | varchar[] |  | 배지 | badges[] | product |
| `translations` | jsonb |  | 다국어 이름 · 설명 · 주의 · 이미지 주소 | translsMap | product |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  | deleted | product |

## product_category_link · 상품 ↔ 카테고리 (N:M)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `product_id · category_id` | uuid FK · PK | ✓ | 상품 하나가 카테고리 여럿에 | categories[] | product_category_link |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  | product_category_link |

## product_option · 상품 옵션 (데모 323 — SINGLE 307 · GROUP 16)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `id` | uuid PK | ✓ | 희망 시술 · 상담 시술 · 작업 · 구매가 가리키는 단위 | id | product_option |
| `product_id` | uuid FK → product | ✓ | 상품 1 : 옵션 N |  | product_option |
| `type` | enum single · group · consultation | ✓ | single = 진료항목 1개 · group = 코스(구성 여러 개) · consultation = 상담용(가격 없음) | type | product_option |
| `title` | varchar | ✓ | 옵션 이름 (예: 보톡스 50유닛 1회) | title | product_option |
| `description` | text |  |  | description | product_option |
| `count` | int |  | 횟수 (회차 — 10회권이면 10) | count | product_option |
| `procedure_id` | uuid FK → procedure |  | 시술(진료 행위) | procedure.id | product_option |
| `medical_service_id` | uuid FK → medical_service |  | single 의 진료항목 — KOS 문서상 single 은 진료항목 1개(이번 목록 응답에는 procedure 만 있었다 — 확인) | medicalService.id | product_option |
| `price_amount` | int |  | 정가 | price.amount | product_option |
| `supplied_amount · vat_amount · tax_free_amount` | int |  | 공급가 · 부가세 · 면세액 | price.* | product_option |
| `currency` | varchar |  | 통화 | price.amount.currency | product_option |
| `taxation` | enum |  | 과세 구분 (데모: TAXABLE 4 · 나머지 UNKNOWN) | price.taxation | product_option |
| `is_frequently_used` | bool |  | 자주 쓰는 옵션 | frequentlyUsedOption | product_option |
| `display_channels` | enum[] homepage · gangnamunni · kos_connect |  | 노출 채널 | displayChannels[] | product_option |
| `badges · promotions` | jsonb |  | 배지 · 프로모션 설정 | badges · promotionConfigurations | product_option |
| `translations` | jsonb |  | 다국어 제목 · 설명 | translsMap | product_option |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  | deleted | product_option |

## product_option_price · 수가 유형별 가격 (옵션 1 : N)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `option_id · customer_type_id` | uuid FK · PK | ✓ | 고객 수가 유형(02 고객의 customer_type)마다 다른 가격 | price.additional[].visitorType.id | product_option_price |
| `amount` | int | ✓ | 그 유형의 가격 | price.additional[].amount | product_option_price |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  | product_option_price |

## product_option_composition · 코스 구성 (group 옵션 1 : N)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `id` | uuid PK | ✓ |  |  | product_option_composition |
| `option_id` | uuid FK → product_option | ✓ | 코스(group) 옵션 |  | product_option_composition |
| `ref_single_option_id` | uuid FK → product_option |  | 구성이 가리키는 단품(single) 옵션 | refSingleOptionId | product_option_composition |
| `medical_service_id · procedure_id` | uuid FK |  | 구성의 진료항목 · 시술 | medicalService.id · procedure.id | product_option_composition |
| `title` | varchar | ✓ |  | title | product_option_composition |
| `count · unit_type · unit_value` | int · enum · numeric |  | 횟수 · 단위(cc · unit · shot …) · 용량 | count · unit | product_option_composition |
| `price_amount (+ 공급가 · 부가세 · 면세)` | int |  | 구성별 가격 | price | product_option_composition |
| `sort_order` | int | ✓ |  | 배열 순서 | product_option_composition |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  | product_option_composition |

## medical_service · 진료항목 (데모 226)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | id | medical_service |
| `hospital_id` | uuid FK → hospital | ✓ | 메뉴는 병원별 |  | medical_service |
| `code` | varchar |  | 진료항목 코드 | configuration.code | medical_service |
| `title` | varchar | ✓ | 예: 보톡스(이마) 50U | title | medical_service |
| `description · caution` | text |  |  | description · caution | medical_service |
| `status` | enum | ✓ | 데모는 전부 PUBLISHED | status | medical_service |
| `procedure_id` | uuid FK → procedure |  | 시술(진료 행위) | configuration.procedure.id | medical_service |
| `unit_type · unit_value` | enum · numeric |  | 단위 · 용량 (데모: CC 62 · UNIT 38 · SHOT 18 · KJ 16 …) | configuration.unit | medical_service |
| `healthcare_reimbursement` | enum |  | 급여 · 비급여 | configuration.healthcareReimbursement | medical_service |
| `taxation` | enum |  | 과세 구분 | configuration.taxation | medical_service |
| `price_amount` | int |  | 진료항목 가격 | priceAmount (문서) | medical_service |
| `duration_minutes · recommended_interval_days` | int |  | 시술 시간 · 권장 간격 — KOS 문서에 있음 | durationTime · recommendedInterval (문서) | medical_service |
| `translations` | jsonb |  |  | translsMap | medical_service |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  | drafted · updatedDateTimeUtc · deleted | medical_service |

## medical_service_machine · medical_service_medicine (N:M)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `medical_service_id · machine_id` | uuid FK · PK | ✓ | 진료항목에 쓰는 기기 | configuration.machines[] | medical_service_machine |
| `medical_service_id · medicine_id` | uuid FK · PK | ✓ | 진료항목에 쓰는 약물 | configuration.medicines[] | medical_service_medicine |

## procedure · 시술(진료 행위) (데모 804)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | id | procedure |
| `hospital_id` | uuid FK → hospital | ✓ | 메뉴는 병원별 |  | procedure |
| `name` | varchar | ✓ | 시술 이름 — 진료항목 · 옵션이 가리킨다. 이름 충돌: 5번 작업과 헷갈리지 않게 테이블 이름을 정할 것 | name | procedure |
| `category_ids` | — |  | 시술 카테고리 — 목록 응답엔 비어 있음 | categoryIds[] | 확인 필요 |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  | procedure |

## machine · medicine · 기기 (302) · 약물 (349)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `machine: id · hospital_id · name` | uuid · varchar | ✓ | 기기 | get-machines | machine |
| `medicine: id · hospital_id · name` | uuid · varchar | ✓ | 약물 — 마약류 보고 등에 쓰일 수 있음 | get-medicines | medicine |

## etc_task_type · 기타 작업 종류

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `id` | uuid PK | ✓ |  | id | etc_task_type |
| `hospital_id` | uuid FK → hospital | ✓ | 메뉴는 병원별 |  | etc_task_type |
| `title` | varchar | ✓ | 방 배정 · 마취 · 시트팩 · 관리 마무리 (명동점 4개) — 내부 API | get-etcetera-tasks (cc etc_task_def) | etc_task_type |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  | deleted | etc_task_type |

## 다른 곳으로

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) | 테이블 |
|---|---|---|---|---|---|
| `기타 상품 · 선불카드 상품` | — |  | KOS 메뉴에 있지만 수납(데스크) 전용 — 1차 범위 밖 | 데이터 모델 문서 | 두지 않음 (지금) |
| `타겟 국가 · 통화 · 부가세 설정` | — |  | 가격 표시 설정 — 수납 전용 | get-target-countries · currency · vat settings | 두지 않음 (지금) |
| `외부 id` | — |  | 모든 메뉴 테이블의 KOS id | id | external_ref |

## 정할 것 · 확인할 것

1. 단품 옵션의 진료항목 칸 — KOS 문서는 「단품 = 진료항목 1개」인데 목록 응답에는 `procedure` 만 있었다. 상품 1건 조회(`getProduct`)로 확인.
2. 노출 기간 · 판매 기간 — 문서에만 있음. 같은 방법으로 확인.
3. 시술 카테고리(`categoryIds`) — 목록 응답에 비어 있음.
4. 과세 구분 — 데모 옵션 323개 중 319개가 `UNKNOWN`.
5. 기타 작업 종류는 내부 API(`get-etcetera-tasks`)로만 받는다.
6. 테이블 이름 — KOS 「시술(진료 행위)」을 `procedure` 로 두면 5번 작업과 헷갈린다. 이름을 정할 것.

범위 밖(지금): 기타 상품 · 선불카드 상품 · 타겟 국가 · 통화 · 부가세 설정(수납 전용).
