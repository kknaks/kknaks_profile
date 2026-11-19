# KOS → DAY 동기화 조사 — API · 백필 · 변경 감지 (테스트 계정 실호출)

- 브리프: task_e71f3b5f7339(4차). 동기화 대상 SoT 는 `spec-000-data-model.md` §4(PR #951)의 새 테이블 28개와 §6 OQ-00-2 · 00-3 · 00-4 다.
- 출발점: HAR 리포트 1~3차(`har-check-report.md` · `-2` · `-3`). DAY prod 코드(`origin/prod`)의 `tasks/emr.py` · `emr/kos/__init__.py` · `client.py` 는 읽기만 했다.
- 공개 API 스펙: `https://developers.kos-solution.com/openapi.yaml`(받은 날 2026-11-19 · 1.0.1)을 읽기만 했다.
- 실호출(2026-11-19):
  - 내부 API: **테스트 계정**으로 sign-in 1회, 토큰은 재사용했다.
  - 공개 API: `KOS_API_tenent_dev`(데모 지점 open-api 키)만 썼다.
  - 시스템 계정 · 명동점 키는 쓰지 않았다.
  - 호출은 조회만 했다. 명령은 끝에 내 세션 해제 1회뿐이다.
  - 호출 사이 간격은 0.4초 이상이다. 페이지는 최대 2장까지만 넘겼다.
- 표기: 「내부」 = `api.kos-solution.com/tenants/{테넌트}/…`(사용자 토큰 · 웹 UA 필수) · 「공개」 = `open-api.kos-solution.com/…`(키 → 토큰 · 세션 없음). 건수는 데모 지점 값이다.

## 0. 테넌트 확인 — 데모 지점

| 확인 | 결과 |
|---|---|
| `common/v1/tenant/queries/get-user-tenants` | 200 · **테넌트 2개**. 그중 하나가 DAY 데모 시드 테넌트(`DAY_SEED_KOS_TENANT_ID`)와 같다. 데모 시드 open-api 키 = `KOS_API_tenent_dev` 다(값 대조 일치 · 값은 안 적음). 다른 하나는 **한 번도 부르지 않았다** |
| `v1/account/queries/get-user-account` | 200 · 키 `email · id · mfaMethods · name · role` |
| 같은 테넌트인가 | 공개 `get-zones`(데모 키) 구역 id 2개 = 내부 `schedule/zone/v1/queries/get-zones` 구역 id 2개 → **일치**. 그래서 내부 호출 전부 이 데모 테넌트로만 했다 |

- ⚠ 테스트 계정이 **다른 테넌트 하나에도 접근권**이 있다(`mode` 값이 데모 테넌트와 다르다). 그 테넌트가 실 데이터인지는 확인하지 않았다(부르지 않음). 코디 확인용 기록이다.

## 실호출 표 (경로 · 상태 · 건수)

| 분류 | API | 경로 | 요청 | 상태 | 건수 · 비고 |
|---|---|---|---|---|---|
| 인증 | 내부 | `common/v1/user/commands/sign-in` | `{email, password}` | 200 | 1회 · 토큰 재사용 |
| 인증 | 공개 | `open/authorization/commands/exchange-token` | `{key}` | 200 | 1회 |
| 구역 | 공개 | `schedule/open/zone/v1/queries/get-zones` | `{}` | 200 | 2 |
| 구역 | 내부 | `schedule/zone/v1/queries/get-zones` | `{}` | 200 | 2 |
| 메뉴 | 내부 | `procedure-menu/categories/queries/get-categories` | `{sort}` | 200 | 15 |
| 메뉴 | 공개 | `procedure-menu/open/categories/queries/get-categories` | `{}` | 200 | 15 |
| 메뉴 | 내부 | `procedure-menu/products/queries/get-products` | `{deleted:false, includePromotions:false}` | 200 | 상품 103 · 옵션 326(SINGLE 309 · GROUP 17) |
| 메뉴 | 내부 | 같은 경로 | `{deleted:true, …}` | 200 | 1(그 1건도 `deleted:false` — 필터 뜻 불명) |
| 메뉴 | 내부 | `procedure-menu/products/v3/queries/get-products` | `{closed, deleted, size:20}` | 200 | 20 · **`count` 103 · `nextCursor`** |
| 메뉴 | 공개 | `procedure-menu/open/products/queries/get-products` | `{}` | 200 | 상품 101 · 옵션 323(SINGLE 307 · GROUP 16) |
| 메뉴 | 내부 | `procedure-menu/product-options/v2/queries/search-product-option-summaries` | `{searchText:"", size:20, deleted, closed}` | 200 | 20 · `nextCursor` |
| 메뉴 | 내부 | `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product` | `{closed:false}` | 200 | 8 |
| 메뉴 | 내부 | `procedure-menu/etcetera-products/v1/queries/get-etcetera-products` | `{deleted:false}` | 200 | 11 |
| 메뉴 | 내부 | `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | `{}` | 200 | 10(경로 출처: cc-prototype `reservation_sync.py` `PATH_ETC`) |
| 메뉴 | 내부 | `procedure-menu/v2/queries/get-procedures` | `{deleted:false}` | 200 | 804 |
| 메뉴 | 내부 | `procedure-menu/procedure-categories/queries/get-procedure-categories` | `{includeDeleted:false}` | 200 | **0** |
| 메뉴 | 내부 | `common/medicine-and-machines/v2/queries/get-medicine-and-machines` | `{name:""}` | **404** | HAR(`상품 수납.har`, 11-11) 경로 · 지금 없음 |
| 메뉴 | 공개 | `procedure-menu/open/v1/machines/queries/get-machines` | `{}` | 200 | 302 |
| 메뉴 | 공개 | `procedure-menu/open/v1/medicines/queries/get-medicines` | `{}` | 200 | 349 |
| 메뉴 | 공개 | `procedure-menu/open/v1/procedures/queries/get-procedures` | `{}` | 200 | 804 |
| 메뉴 | 공개 | `procedure-menu/open/v1/medical-services/queries/get-medical-services` | `{}` | 200 | 226 |
| 일정 | 내부 | `schedule/v2/queries/get-schedules-grouped-by-zone` | `{zoneIds, startDateTimeUtc, endDateTimeUtc}` | 200 | 11-18 하루 13 · 8월 첫 주 94 · **8월 한 달 485(1.5MB · 0.9초)** · 9~11월 832(3.1MB) |
| 고객 | 내부 | `visitor/v2/queries/get-visitors` | `{indexOfPage, countInPage:20, …, sort}` | 200 | 20 · **`count` 558** |
| 구매 | 내부 | `purchase/v1/queries/get-purchase-summaries` | `{purchaseIds[46], includeDeleted:true}` | 200 | 46(삭제 5) |
| 구매 | 공개 | `purchase/open/v1/queries/get-purchase-summaries` | `{purchaseIds[46]}` | 200 | **41 — 삭제 5건이 빠진다** |
| 구매 | 공개 | 같은 경로 | `{purchaseIds[87]}` | 200 | 87 |
| 구매 | 내부 | `purchase/v1/queries/get-purchase-summaries` | `{purchaseIds[87], includeDeleted:true}` | 200 | 87 |
| 구매 | 공개 | `purchase/open/v1/queries/get-purchase-summaries-by-visitor-id` | `{visitorId}` | 200 | 12(그 고객 전체) |
| 시술권 | 내부 | `ticket/v1/queries/get-ticket-bundles` | `{visitorId, sort}` | 200 | 12 번들 |
| 시술권 | 공개 | `ticket/open/v1/queries/get-ticket-bundles` | `{visitorId}` | 200 | **5 — `AVAILABLE` 티켓 있는 번들만** |
| 선불카드 | 내부 · 공개 | `purchase[/open]/prepaid-card/v1/queries/get-prepaid-card-summaries` | `{visitorId}` | 200 · 200 | 5 · 5 |
| 선불카드 | 공개 | 같은 경로 | `{visitorId, available:true}` | 200 | 3(환불된 카드 2장 빠짐) |
| 선불카드 | 내부 · 공개 | `purchase[/open]/prepaid-card/v1/queries/get-prepaid-card-charging-events` | `{id}` × 카드 5 | 200 ×10 | 2 · 1 · 4 · 3 · 5 — 내부 = 공개 **글자까지 같음** |
| 선불카드 | 내부 | `purchase/prepaid-card/v1/queries/get-prepaid-card-visitors` | `{id}` × 카드 5 | 200 ×5 | 1 · 1 · 1 · 2 · 1 |
| 일정 | 내부 | `schedule/v1/queries/get-schedule-summaries` | `{visitorId, sort}` | 200 | 3 |
| 일정 | 공개 | `schedule/open/v1/queries/get-schedules-by-visitor` | `{visitorId}` · `{…, deleted:true}` | 200 · 200 | 3 · 3 |
| 일정 | 내부 · 공개 | `schedule[/open]/v1/queries/get-schedule-detail` | `{scheduleId}` | 200 · 200 | 1 — 최상위 키 23개 같음 · `purchaseIds` 같음 |
| 일정 | 공개 | `schedule/open/v1/queries/find-schedule-by-purchase-id` | `{purchaseId}` | 200 | 1(그 구매가 붙은 일정 — 대조 일치) |
| 일정 | 공개 | `schedule/open/v1/queries/get-schedules-summarized-by-tasks` | `{visitorId}` | 200 | 3 |
| 일정 | 내부 | `schedule/v1/queries/get-payment-required-tasks` | `{visitorId}` | 200 | 0 |
| 처방 | 내부 | `prescription/v1/queries/get-prescriptions` | `{visitorId}` | 200 | 0 |
| 통계 | 공개 | `statistics/open/v1/queries/get-purchase-item-statistics` | `{createdDateTimeUtcFrom/To, limit:50, cursor}` | 200 ×2 | 50+50 · **`totalCount` 444** · 겹침 0 |
| 통계 | 공개 | `…/get-transaction-statistics` | `{createdTimeUtcFrom/To, limit, cursor}` | 200 ×2 | 50+50 · `totalCount` 425 · 겹침 0 |
| 통계 | 공개 | `…/get-prepaid-card-charging-event-statistics` | `{chargedDateTimeUtcFrom/To, limit:50}` | 200 | 33 · `totalCount` 33(커서 없음) |
| 통계 | 공개 | `…/get-schedule-statistics` | `{reservationStartDateTimeUtcFrom/To, limit, cursor}` | 200 ×2 | 50+50 · `totalCount` 1317 |
| 통계 | 공개 | `…/get-visitor-statistics` | `{limit}` | **400** | `at least one date time range is required` |
| 통계 | 공개 | 같은 경로 | `{visitorCreatedDateTimeUtcFrom/To, limit:50}` | 200 | 50 · `totalCount` 558 |
| 통계 | 공개 | `…/get-procedure-task-statistics` | `{completedDateTimeUtcFrom/To, limit, cursor}` | 200 ×2 | 50+50 · `totalCount` 298 |
| 통계 | 공개 | `…/get-ticket-group-statistics` | `{limit}` · `{issuedDateTimeUtcFrom/To, limit}` | **404 ×2** | `No static resource …` — **스펙엔 있는데 운영 open-api 에 없음** |
| 통계 | 공개 | 구매 항목 · 거래 · 일정 통계(11-18 하루) | 같은 키 | 200 ×3 | 48 · 59 · 13 — 그날 요약(살아 있는 구매)의 항목 48 · 거래 59 · 일정 13 과 **정확히 같다** |
| 통계 | 공개 | 일정 통계 `totalCount` 만(8월 / 8월 이전 / 11-20 이후) | `limit:1` | 200 ×3 | 485 · **0** · 2 |
| 세션 | 내부 | `common/user/v1/queries/get-active-sign-ins` → `revoke-active-sign-in` → 다시 목록 | `{email, password(, signInId)}` | 200 · 200 · 200 | 1(내 `(research)` 1 · 남 0) → 해제 → **0** |

- 데모 지점 데이터는 2026-08 부터 있다(일정 통계 8월 이전 0).

## Q1 테이블별 원천 API 표

- 단위: **병원** = 병원 전체 한 번 · **고객** = `visitorId` 마다 · **구매** = `purchaseIds` 묶음 · **카드** = 카드 id 마다 · **일정** = 일정 id 마다.
- 「칸 표와 맞나」 = SPEC-000 §4 「외부(KOS)」 열의 키가 실제 응답에 있는지다.

### 메뉴 16

| 테이블 | 원천(권장 후보 먼저) | 공개/내부 | 요청 키 · 페이지 | 단위 | 칸 표와 맞나 |
|---|---|---|---|---|---|
| `product_category` | `procedure-menu/open/categories/queries/get-categories` | 공개(내부도 같음) | `{opened?, sort?}` · 페이지 없음 | 병원 | ✓ `id · name · order · opened · deleted · translsMap` |
| `product` | 내부 `procedure-menu/products/queries/get-products` / 공개 `…/open/products/queries/get-products` | 둘 다 | 내부 v1 페이지 없음 · v3 `size` + `nextCursor` + `count` · 공개 페이지 없음 | 병원 | ✓ 대부분. `displayPeriod · offeringPeriod` 는 **내부 응답에만**(103 중 1건). 내부에 `targetCountryCodes` 가 더 있다. **내부 103 · 공개 101** — 내부에만 있는 2건은 `closed · deleted` 모두 false(차이 이유 확인 안 됨) |
| `product_category_link` | 상품의 `categories[]` | 둘 다 | — | 병원 | ✓ |
| `product_option` | 상품의 `options[]`(또는 `search-product-option-summaries`) | 둘 다 | — | 병원 | 아래 2가지가 다르다 |
| `product_option_price` | 옵션 `price.additional[]{visitorType, amount, …}` | 둘 다 | — | 병원 | ✓ (데모 1건) |
| `product_option_composition` | GROUP 옵션 `compositions[]` | 둘 다 | — | 병원 | **어긋남** — 구성 키 = `title · count · unit · price · procedure · medicalService · medicineAndMachines`. 칸 표의 **`refSingleOptionId` 는 응답에 없다**(34 구성 모두). 구성 `id` 도 없다 |
| `treatment_item` | `procedure-menu/open/v1/medical-services/queries/get-medical-services` | **공개** | `{title?}` · 페이지 없음 | 병원 | ✓ `code · procedure · machines · medicines · unit(150/226) · healthcareReimbursement · taxation · status · draftedDateTimeUtc · updatedDateTimeUtc`. 칸 표 `priceAmount · durationTime · recommendedInterval` 은 **응답에 없다**(스펙엔 `contributionConstant` 만) |
| `treatment_item_machine` · `_medicine` | 시술 항목 `configuration.machines[] · medicines[]` | 공개 | — | 병원 | ✓ |
| `treatment` | 공개 `…/open/v1/procedures/queries/get-procedures` `{id,name}` / 내부 `procedure-menu/v2/queries/get-procedures` `{…, deleted, createDate, categoryIds}` | 둘 다 | 페이지 없음 · 804 | 병원 | ✓ `name`. `categoryIds` 는 내부에만 있고 804건 모두 빈 배열. 시술 카테고리 목록(`get-procedure-categories`)도 0건 |
| `machine` · `medicine` | `…/open/v1/machines/queries/get-machines` · `…/open/v1/medicines/queries/get-medicines` | **공개** | `{name?}` · 302 · 349 | 병원 | ✓ `{id, name}`(칸 표 `get-machines` · `get-medicines` 그대로). 내부 `get-medicine-and-machines` 는 지금 404 |
| `etc_task_type` | `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | **내부만** | `{}` · 10 | 병원 | ✓ `id · title · deleted · translsMap` |
| `prepaid_card_product` | `procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product` | **내부만**(openapi 에 없음) | `{closed}` · 8 | 병원 | ✓ `title · price · balance · point · closed · expirationDurationInDays · order · description` |
| `etcetera_product_category` | 품목의 `category{id, category, name, order, closed}` | **내부만** | — | 병원 | ✓ — **분류에 `id` 가 온다**(칸 표 「id 로 오는지 동기화 때 확인」 → 온다) |
| `etcetera_product` | `procedure-menu/etcetera-products/v1/queries/get-etcetera-products` | **내부만** | `{deleted}` · 11 | 병원 | ✓ `id · title · category · price` |

`product_option` 에서 다른 2가지:

- **`medicalService` 는 내부 응답에만 있다.** 내부 309/309 단품 옵션에 `medicalService{id, …, configuration}` 가 있고, 공개 응답에는 0이다. 공개만 쓰면 `treatment_item_id` 를 못 채운다. 이건 OQ-041-1 의 답이다.
- **옵션 자체에 `unit` 키가 없다**(내부 · 공개 모두 0/326). 칸 표 `optionConfiguration.unit` 은 **구매 항목 스냅샷의 키**다. 메뉴 응답에서는 `medicalService.configuration.unit`(188/309)뿐이다.

### 구매 5

| 테이블 | 원천 | 공개/내부 | 요청 키 | 단위 | 칸 표와 맞나 |
|---|---|---|---|---|---|
| `purchase` · `purchase_item` · `purchase_price_adjustment` · `purchase_transaction` · `purchase_assignee` | `purchase[/open]/v1/queries/get-purchase-summaries` | **둘 다 — 응답이 글자까지 같다**(41/41) | 내부 `{purchaseIds[], includeDeleted}` · 공개 `{purchaseIds[]}` · 87개 한 번에 됨 · 페이지 없음 | 구매 묶음 | ✓ HAR 1~3차 모양 그대로 |
| (같음) | `purchase/open/v1/queries/get-purchase-summaries-by-visitor-id` | 공개 | `{visitorId}` | 고객 | 같은 모양 · 그 고객 전체 |
| `purchase.visit_id` | 일정 목록 · 상세의 `purchaseIds[]` · 또는 공개 `find-schedule-by-purchase-id {purchaseId}` | 둘 다 | — | 일정 / 구매 | ✓ |

- 공개는 **삭제된 구매를 안 준다**(46 → 41). 내부 `includeDeleted:true` 는 `deleted:true` 로 준다(삭제 5 = `INITIALIZED/PENDING` 4 · `ACCEPTED` 1).
- 지운 구매도 일정의 `purchaseIds` 에는 남아 있었다(11-18 일정 목록의 46개에 삭제 5 포함).
- 데모 표본 값:
  - status · process: `ACCEPTED/NOT_IN_PROCESS` 39 · `INITIALIZED/PENDING` 4 · `PARTIALLY_REFUNDED` 2 · `REFUNDED` 1
  - 항목 종류: `PRODUCT_OPTION` 51 · `PREPAID_CARD_PRODUCT` 4 · `ETCETRA_PRODUCT` 1
  - 결제 수단: `CASH` 56 · `PREPAID_CARD` 3
  - `priceAdjustments` · `revokingItems` 는 0
- 공개 스펙의 enum은 HAR 보다 넓다. 표본에는 없지만 스펙 값이다.
  - `status` 에 `PAID` 가 더 있다.
  - `process` 에 `REVOKING` · `PREPAID_CARD_ITEM_SUBSTITUTING` 이 더 있다.
  - 구매에 `conversion{type: PREPAID_CARD_CONVERSION, refConversionId}` · `purchaseMemo` · `migratedDateTimeUtc` 키가 있다.
  - SPEC-000 `purchase.status/process` enum 에 없는 값이다(§정할 것 5).

### 시술권 3

| 테이블 | 원천 | 공개/내부 | 요청 키 | 단위 | 칸 표와 맞나 |
|---|---|---|---|---|---|
| `ticket_bundle` · `ticket_set` · `ticket` | 내부 `ticket/v1/queries/get-ticket-bundles` | **내부(전체)** | `{visitorId, sort?}` · 페이지 없음 | 고객 | ✓ 번들 `purchaseId · purchaseItemId · title · price · optionConfiguration` · 세트 `ticketGroupId · title · unit · medicalService · procedure` · 티켓 `id · status · price · createdDateTimeUtc` |
| (일부만) | 공개 `ticket/open/v1/queries/get-ticket-bundles` | 공개 | `{visitorId}` | 고객 | 키는 같음. **`AVAILABLE` 티켓이 있는 번들만**(12 → 5 · 스펙 제목 「사용 가능한 시술권 묶음」). `IN_USE` · `USED` 만 남은 번들은 안 온다 |
| `visit_task.ticket_id` | 일정 목록 · 상세 `tasks[].procedureConfiguration.ticketConfiguration{ticketId, round}` | 둘 다 | — | 일정 | ✓ — 11-18 일정 목록 작업 45 중 35 에 있음 |

### 선불카드 3

| 테이블 | 원천 | 공개/내부 | 요청 키 | 단위 | 칸 표와 맞나 |
|---|---|---|---|---|---|
| `prepaid_card` | `purchase[/open]/prepaid-card/v1/queries/get-prepaid-card-summaries` | 둘 다 | `{visitorId, available?}` | 고객(소유자) | ✓ `id · title · ownerId · remainingBalance · remainingPoint · expirationDateTimeUtc · createdDateTimeUtc · updatedDateTimeUtc`. `available:true` 면 환불된 카드가 빠진다(5 → 3). 칸 표 `streamId` 는 **응답에 없다** |
| `prepaid_card_customer` | `purchase/prepaid-card/v1/queries/get-prepaid-card-visitors` | **내부만**(openapi 에 없음) | `{id}` | 카드 | ✓ `{visitorId, name, chartNumber, owner}` — 카드 4 에 2명(owner true · false) |
| `prepaid_card_ledger` | `purchase[/open]/prepaid-card/v1/queries/get-prepaid-card-charging-events` | **둘 다 — 같은 응답** | `{id}` | 카드 | ✓ `type · amount{type, amount} · chargingId · createdDateTimeUtc · memo · visitor` |
| (병원 전체 이력) | 공개 `statistics/open/v1/queries/get-prepaid-card-charging-event-statistics` | 공개 | `{chargedDateTimeUtcFrom*, To*, limit*, cursor?, chargingEventTypes?, amountTypes?, visitorId?, ownerId?}` | **병원** | 행마다 `prepaidCardId · ownerId · visitorId(사용자) · chargingId · chargingType · chargingAmountType · chargingAmountV2 · chargedDateTimeUtc · memo · purchaseItems[] · assignees[]` |

- **이번 실호출로 새로 보인 이벤트 값**(HAR 2 · 3차 「확인 안 됨」을 닫는다):
  - `type` 에 **`REFUND`** 가 있다(OQ-10-2 · 환불 이벤트).
  - `amount.type` 에 **`BALANCE`** 가 있다.
  - 카드 3(전액 환불): `CHARGE BALANCE +500,000` · `CHARGE POINT +50,000` · `REFUND BALANCE −500,000` · `REFUND POINT −50,000`
  - 카드 5(부분 환불): `CHARGE` 2건 · `PAYMENT BALANCE −440,000` · `REFUND BALANCE −60,000` · `REFUND POINT −50,000` → 잔액 0 · **금액 총액 440,000**. 3차 리포트의 「총액도 0」은 전액 환불 때 얘기다. 부분 환불이면 총액이 쓴 금액으로 남는다.
  - 스펙 enum 은 `PAYMENT · PAYMENT_CANCEL · REFUND · CHARGE · EXPIRATION · SUBTRACT` 다(OQ-10-3 매핑 후보 · `PAYMENT_CANCEL` · `EXPIRATION` · `SUBTRACT` 는 표본 없음).
- 병원 전체 이벤트 통계 33행 중 `visitorId ≠ ownerId`(공유 고객이 쓴 것)는 **0** — 공유 사용 표본은 여전히 없다.

### 처방 1

| 테이블 | 원천 | 공개/내부 | 요청 키 | 단위 | 칸 표와 맞나 |
|---|---|---|---|---|---|
| `prescription` | 일정 목록 · 상세의 `prescriptionIds[]` | 둘 다 | — | 일정 | ✓ 칸이 `id · visit_id` 뿐이라 일정 응답으로 충분하다. 데모 9~11월 일정 832건에 `prescriptionIds` 가 있는 일정은 **0** — 표본 없음 |
| (내용) | 내부 `prescription/v1/queries/get-prescriptions` | 내부만 | `{visitorId}` | 고객 | 0건(데모) |

### 방문(일정) — 구매가 기대는 쪽

| 무엇 | 원천 | 공개/내부 | 요청 키 | 단위 |
|---|---|---|---|---|
| 기간 일정 목록(지금 10초 루프) | 내부 `schedule/v2/queries/get-schedules-grouped-by-zone` | 내부 | `{zoneIds, startDateTimeUtc, endDateTimeUtc}` · 페이지 없음 | 병원 · 기간 |
| 일정 목록 키 | `purchaseIds · prescriptionIds · tasks(ticketConfiguration 포함) · updatedDateTimeUtc · deleted …` 23개 — **상세와 최상위 키가 같다**. `purchases[]` 는 늘 빈 배열 | | | |
| 일정 id 나열 | 공개 `statistics/open/v1/queries/get-schedule-statistics` | 공개 | `{reservationStartDateTimeUtcFrom/To, limit*, cursor}` | 병원 |
| 고객별 일정 | 공개 `schedule/open/v1/queries/get-schedules-by-visitor` | 공개 | `{visitorId*, startDateTimeUtc?, endDateTimeUtc?, deleted?}` | 고객 |
| 상태별 일정 | 공개 `schedule/open/v1/queries/get-schedules-by-flow-step` | 공개 | `{flowStep*, reservationStartDateTimeUtcFrom*/To*}` — 단계 하나씩(9개) | 병원 · 단계 (스펙만 · 실호출 안 함) |
| 일정 상세 | 내부 · 공개 `…/get-schedule-detail` | 둘 다 | `{scheduleId}` | 일정 |

## Q2 백필 — 지난 이력 전체

### 병원 전체로 나열하는 API — **있다(공개 통계 6개 · 커서)**

| 통계 | 기간 필터(필수) | 행 단위 | 행에 있는 id | 표본 총수 |
|---|---|---|---|---|
| `get-purchase-item-statistics` | `createdDateTimeUtcFrom/To` | 구매 항목 | `purchaseId · visitorId`(항목 id 없음) | 444 |
| `get-transaction-statistics` | `createdTimeUtcFrom/To` | 거래 | `purchaseId · visitorId`(**거래 id 없음**) | 425 |
| `get-prepaid-card-charging-event-statistics` | `chargedDateTimeUtcFrom/To` | 카드 이벤트 | `prepaidCardId · ownerId · visitorId · chargingId` | 33 |
| `get-schedule-statistics` | `reservationStartDateTimeUtcFrom/To`(또는 `reservedDateTimeUtc…`) | 일정 | `scheduleId · visitorId` | 1,317 |
| `get-procedure-task-statistics` | `completedDateTimeUtcFrom/To` | 완료 작업 | `scheduleId · procedureTaskId · visitorId` | 298 |
| `get-visitor-statistics` | 날짜 범위 하나 이상(`visitorCreated…` 등) | 고객 | `visitorId` + `totalTicketCount · totalPrepaidCardBalanceV2 …` | 558 |
| ~~`get-ticket-group-statistics`~~ | — | — | — | **404(운영에 없음)** |

- 커서:
  - 응답 `nextCursor` 를 다음 요청 `cursor` 로 넣는다. 2장째 겹침 0(확인한 4개 모두)이다.
  - `totalCount` 는 첫 장에만 온다.
  - `limit` 는 필수다(50 으로 시험 · 상한은 확인 안 함).
- 통계는 **원장 행이 아니라 분석용 요약**이다.
  - 거래 · 항목 id 가 없고 이름 문자열이 들어 있다(고객 · 직원 이름 등).
  - 그래서 **id 나열용**으로만 쓰고, 칸은 원장 API(구매 요약 · 시술권 · 카드)로 다시 받는 모양이 된다.
- 통계는 **삭제된 구매를 빼고 센다.** 11-18 하루를 비교했다.
  - 구매 항목 48 · 거래 59 = 살아 있는 구매 41건의 항목 · 거래 수와 같다.
  - 삭제 구매 5건은 통계에 0건이다.
  - 열린(`INITIALIZED`) 구매가 들어가는지는 확인 안 됨이다(그날 열린 구매 4건은 모두 삭제된 것).

### 백필 순서 · 호출 수(데모 지점 실측 기준 추정)

| 순서 | 무엇 | 길 | 호출 수(데모) | 비고 |
|---|---|---|---|---|
| 1 | 방문(일정) | 내부 `get-schedules-grouped-by-zone` **한 달씩** | 4(8~11월) | 8월 485건 · 1.5MB · 0.9초 / 9~11월 832건 · 3.1MB. 작업 · `purchaseIds` · `prescriptionIds` 가 같이 온다. 공개 대안 = 일정 통계로 id 나열(1,317 ÷ limit) + `get-schedule-detail` 일정마다 1,317 |
| 2 | 구매 · 항목 · 거래 · 담당 | 1의 `purchaseIds` 를 모아 `get-purchase-summaries` 묶음 | 약 6(448 ÷ 87 시험값) | 공개는 삭제 구매가 빠진다 → 지운 것까지 받으려면 내부 `includeDeleted` |
| 3 | 시술권 | 내부 `get-ticket-bundles` 고객마다 | 최대 558 · 고객 통계로 `totalTicketCount > 0` 만 고르면 표본 50 중 7(14%) → 약 80 + 고객 통계 12장 | 병원 전체 시술권 목록 API 없음(통계는 404). 공개 시술권은 `AVAILABLE` 만 |
| 4 | 선불카드 · 이력 | 공개 이벤트 통계(병원 · 1장) → 카드 id · 소유자 → 소유자마다 `get-prepaid-card-summaries` · 카드마다 `get-prepaid-card-charging-events` · `get-prepaid-card-visitors`(내부) | 1 + 소유자 7 + 카드 15 × 2 = 약 38 | 이벤트가 하나도 없는 카드는 이 길로 못 찾는다(표본 카드 5장은 모두 `CHARGE` 가 있었다 · 확인 안 됨) |
| 5 | 처방 | 1의 `prescriptionIds` | 0 | 데모 표본 0 |
| 6 | 메뉴 | 병원 단위 목록 | 약 11 | 아래 Q4 |

- 데모 합계는 약 **150 호출**이고, 0.4초 간격으로 약 1분이다.
  - 고객 · 카드 수에 거의 비례한다. 실 병원의 고객 수는 이번에 보지 않았다(명동점 호출 금지).
  - 고객 N명이면 시술권 쪽이 `N × 시술권 보유율` 만큼 는다.
- 백필 순서는 **방문 → 구매**다(`purchase.visit_id` 필수). 1이 끝난 뒤 2를 한다.
- 지금 DAY 코드에 기간 백필 경로는 없다. `fetch_schedules` 는 오늘 창만 받고, 같은 경로에 기간만 넓히면 된다.

## Q3 변경 감지

| 무엇 | 바뀐 시각 칸 | 삭제 표시 | 「바뀐 것만」 받는 길 |
|---|---|---|---|
| 일정 | `updatedDateTimeUtc` · `flowStepUpdatedDateTimeUtc` | `deleted`(공개 고객별 조회는 `deleted` 필터) | 창(오늘) 전체를 다시 받고 비교(지금 방식). 바뀐 것만 받는 필터는 없음 |
| 구매 | `lastUpdatedDateTimeUtc` | `deleted` — **내부 `includeDeleted:true` 에서만 보임**(공개는 빠짐) | 구매 필터는 id 목록뿐이다. 대신 **공개 거래 통계 `createdTimeUtcFrom = 지난 회차`** 로 「새 거래(결제 · 취소 · 환불)가 생긴 구매」 id 를 받는 길이 있다. 새 구매는 구매 항목 통계 `createdDateTimeUtcFrom`. 거래 없이 바뀌는 것(열린 구매 삭제 · 항목 담기)은 이 길로 안 잡힌다 |
| 구매 항목 · 거래 | 칸 없음 · 거래 `paymentDateTime{…}`(승인 · 취소 시각) | 없음(구매 단위) | 구매를 통째로 다시 받는다 |
| 시술권 | **티켓 `createdDateTimeUtc` 뿐 — 바뀐 시각 없음** | 칸 없음 | 고객마다 다시 받아 상태 비교. 오늘 작업의 `ticketConfiguration.ticketId` 가 바뀐 티켓 후보다 |
| 선불카드 | 카드 `updatedDateTimeUtc` | 칸 없음(환불 = 0 + `available:false`) | 카드 이벤트는 쌓기만 하고 `createdDateTimeUtc` 가 있다 → **이벤트 통계 `chargedDateTimeUtcFrom = 지난 회차`** 로 병원 전체의 새 이벤트(카드 · 소유자 · 사용자)를 받는다 |
| 카드 공유 고객 | 없음 | 없음 | 카드마다 목록 비교만 |
| 메뉴 | 시술 항목만 `updatedDateTimeUtc`(+`draftedDateTimeUtc`) · 시술 `createDate`. 상품 · 옵션 · 카테고리 · 선불카드 상품 · 품목 · 기타 작업 · 기기 · 약물은 **시각 칸 없음** | `deleted`(카테고리 · 상품 · 옵션 · 시술 · 기타 작업) · `closed` · 기기 · 약물은 없음 | 전체를 받아 비교(지금 기준 정보와 같은 방식) |

- 지운 것을 알아채는 법:
  - **메뉴 · 일정**: 목록에서 사라짐 + `deleted`. 지금 DAY 규칙(「외부에서 사라진 행 → `deleted_at` + `is_present_in_source=false`」)을 그대로 쓸 수 있다.
  - **구매**: 공개는 사라짐으로만 보이고, 내부는 `deleted:true` 로 보인다.
  - **시술권 · 카드**: 「사라짐」 표본이 없다(환불 카드는 남아 있음).

## Q4 지금 루프에 붙이기

지금(`tasks/emr.py`):
- 10초 `sync_schedules_hospital` = 오늘 창 `get-schedules-grouped-by-zone` 1회(+ 처음 붙은 병원이면 기준 정보 회차).
- 1시간 `sync_master_hospital` = 구역 · 방 · 예약 그룹 · 직무 · 직원 · 코드.
- 일정 상세는 방 배정 연쇄 때만 부른다.

| 루프 | 더할 호출 | 입력 | 호출 수(오늘 일정 N · 오늘 고객 V) |
|---|---|---|---|
| 10초(오늘) | `get-purchase-summaries {purchaseIds}` | **이미 받는 일정 목록의 `purchaseIds`**(추가 호출 없이 손에 있다) | +1(묶음 · 11-18 데모 46개 한 번) |
| 10초 또는 덜 자주 | `get-ticket-bundles {visitorId}` | 오늘 고객 | +V(11-18 데모 V = 8) |
| 10초 또는 덜 자주 | `get-prepaid-card-summaries {visitorId}` | 오늘 고객 | +V |
| 카드가 바뀌었을 때 | `get-prepaid-card-charging-events {id}` · `get-prepaid-card-visitors {id}` | 카드 `updatedDateTimeUtc` 변화 · 또는 이벤트 통계 | +카드 수 × 2 |
| 처방 | 없음 | 일정 목록 `prescriptionIds` 가 이미 있다 | 0 |
| `visit_task.ticket_id` | 없음 | 일정 목록 `tasks[].ticketConfiguration` 가 이미 있다 | 0 |
| 1시간(기준 정보) | 메뉴 11개 | 카테고리 · 상품(옵션 · 가격 · 구성 · 카테고리 연결) · 시술 항목 · 시술 · 기기 · 약물(공개) + 선불카드 상품 · 품목 · 기타 작업(내부) | +약 11 |
| 1시간 또는 따로 | 이벤트 통계 `chargedDateTimeUtcFrom = 지난 회차` | 병원 | +1(페이지 수만큼) |

- 10초마다 전부 하면 오늘 회차당 `1 + 1 + 2V` 호출이다(데모 V = 8 → 18 · 분당 108).
  - 구매만 10초로 하고 시술권 · 카드는 「그 고객의 구매 `lastUpdatedDateTimeUtc` 나 작업 티켓이 바뀌었을 때」만 하면 회차당 2 + 바뀐 고객 수 × 2 다.
  - 고르는 건 §정할 것 1 이다.
- 일정의 `updatedDateTimeUtc` 가 구매 변경 때도 바뀌는지는 **확인 안 됨**이다(명령 호출 금지라 실험 못 함). 바뀐다면 「일정이 바뀐 고객만」으로 줄일 수 있다.
- 오늘 고객이 아닌 고객(지난 고객의 환불 · 카드 사용)은 10초 루프에 안 걸린다. 공개 거래 통계 · 이벤트 통계를 지난 회차 시각부터 받는 「병원 전체 변경」 회차로 잡을 수 있다(주기 §정할 것 2).

## Q5 공개 API 대체

| 대상 | 공개로 되나 | 근거 · 빈 곳 |
|---|---|---|
| 상품 카테고리 · 상품 · 옵션 · 가격 · 구성 · 시술 · 시술 항목 · 기기 · 약물 | **된다** | 단 옵션 → 시술 항목(`medicalService`) 연결이 공개 상품 응답에 없다. 공개 상품은 2건 적다 |
| 기타 작업 · 선불카드 상품 · 시술 외 품목 | **안 된다**(openapi 에 없음) | 내부만 |
| 구매 5 테이블 | **된다**(내부와 같은 응답) | 삭제 구매가 안 보인다 → 삭제 감지는 「사라짐」으로만 |
| 시술권 3 테이블 | **일부** | 공개는 `AVAILABLE` 번들만 → 쓴 · 쓰는 중 티켓 · 다 쓴 번들은 내부 필요. 시술권 통계는 운영에 404 |
| 선불카드 · 이력 | **된다**(내부와 같은 응답 · 병원 전체 이벤트 통계도 공개) | 공유 고객 목록(`get-prepaid-card-visitors`)은 내부만 |
| 처방 | 된다(일정 상세 `prescriptionIds` 공개) | — |
| 오늘 일정 목록 | 공개 대체는 단계별 조회 9번(`get-schedules-by-flow-step`) 또는 일정 통계 → 상세 일정마다 | 지금 내부 1회보다 호출이 많다(실호출 안 함) |
| 백필 나열 | **공개만 있다**(통계 6) | 내부엔 병원 전체 구매 · 거래 목록 경로를 HAR 에서 못 봤다 |

- 공개 API 로 내부 의존을 줄일 수 있는 범위는 **메뉴(대부분) · 구매 · 선불카드 · 백필 나열**이다.
- 남는 내부 의존은 다음 다섯이다.
  - 기타 작업 · 선불카드 상품 · 시술 외 품목
  - 옵션 → 시술 항목 연결
  - 시술권 전체
  - 카드 공유 고객
  - 오늘 일정 목록(이미 쓰는 중)

## 동기화 스펙에서 정할 것 (결정하지 않음)

1. **오늘 고객 시술권 · 카드 주기** — 10초마다(회차 `2 + 2V`)로 할지, 구매 · 작업 티켓 변화가 있을 때만 할지, 분 단위로 따로 둘지.
2. **오늘 밖 고객의 변경** — 공개 거래 통계 · 이벤트 통계를 「지난 회차 시각부터」 받는 병원 전체 회차를 둘지 · 주기(OQ-00-4).
3. **공개/내부 고르기** — 구매 · 카드 · 메뉴 대부분은 공개로 된다. 공개를 쓰면 삭제 구매가 안 보인다(사라짐으로만). 옵션 → 시술 항목 연결은 내부에만 있다. 어느 쪽을 기본으로 할지.
4. **시술권 원천** — 공개는 `AVAILABLE` 만이다. 내부(전체)를 쓸지, 공개 + 「사라진 번들 = 다 씀」으로 볼지(뜻이 다르다: 다 씀 · 환불 · 삭제가 구분 안 됨).
5. **SPEC enum 에 없는 KOS 값**:
   - 구매 `PAID` · `REVOKING` · `PREPAID_CARD_ITEM_SUBSTITUTING`
   - `conversion`(선불카드 전환)
   - 카드 이벤트 `REFUND` · `PAYMENT_CANCEL` · `EXPIRATION` · `SUBTRACT`
   - `ledger.kind` 매핑(OQ-10-3)을 어디에 둘지.
6. **옵션 단위의 원천** — 메뉴 응답의 옵션엔 `unit` 이 없다. `product_option.unit_type/unit_value`(1차 8)를 시술 항목 단위로 채울지, 비워 두고 구매 스냅샷만 쓸지.
7. **구성 `refSingleOptionId` · 시술 항목 가격 · 시간 · 간격 칸** — 응답에 없다. 칸을 유지할지(비어 있게 됨).
8. **백필 범위 · 순서**(OQ-00-3) — 기간(데모는 2026-08~), 지운 구매 포함 여부(내부 `includeDeleted`), 시술권 대상 고객을 고객 통계로 거를지, 이벤트 없는 카드를 어떻게 찾을지.
9. **통계 API 를 원장 동기화에 써도 되는지** — 분석용 요약(이름 문자열 · id 일부 없음)이다. 운영에 없는 통계(시술권 404)도 있어 계약 안정성을 어떻게 볼지.
10. **테스트 계정의 두 번째 테넌트** — 실 데이터인지 · 연구 호출에서 막을 장치가 필요한지(코디 확인).

## 확인 안 됨 — 필요한 HAR · 확인

| 질문 | 필요한 것 |
|---|---|
| 일정 `updatedDateTimeUtc` 가 구매 · 결제 · 시술권 변경 때도 바뀌나 | KOS 웹에서 결제 1회 전후의 일정 목록(HAR `수납` 화면 + 예약 현황 새로고침) |
| 열린(`INITIALIZED`) · 살아 있는 구매가 통계에 들어가나 | 항목만 담고 결제 안 한 구매가 있는 날의 통계 1회(조회만으로 가능 · 데모에 그런 구매가 생기면) |
| 카드 공유 고객이 카드로 결제했을 때 이벤트 `visitor` · 통계 `visitorId` | 공유 고객으로 결제 1회(HAR) |
| 이벤트 없는 카드가 있나(0 원 직접 생성) | 금액 0 · 포인트 0 으로 카드 만들기 1회(HAR) |
| 공개 · 내부 상품이 2건 다른 이유 | 그 2개 상품의 설정 화면(HAR) — 판매 채널 · 국가 등 |
| 통계 `limit` 상한 · 시술권 통계가 운영에 생기는지 | KOS 담당자 문의 또는 나중 재호출 |
| 내부 `get-medicine-and-machines`(404) 의 새 경로 | 시술 항목 설정 화면에서 약품 · 기기 고르기(HAR) — 지금은 공개 기기 · 약물로 대체됨 |
| 실 병원 규모(고객 · 카드 · 시술권 보유율) | 명동점은 호출 금지 — 사용자 · 코디가 정한 방법으로 |
| 처방이 있는 일정의 `prescriptionIds` · 처방 목록 모양 | 처방 1건 있는 고객(HAR 또는 데모에 처방 생성 뒤 조회) |

## 개인정보 점검

```text
grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}|Bearer|@medisolveai' kos-sync-research-report.md
```

점검 결과(2026-11-19): 일치 **1줄 — 위 grep 명령 줄 자신**(패턴 문자열의 `Bearer` · `@medisolveai`). 그 밖 전화번호 꼴 · 24자리 hex(테넌트 · 고객 · 구매 id · 커서) · `Bearer` · 계정 도메인 **0건**. UUID 꼴(카드 id) 0건. 고객 · 직원 이름 · 차트번호 · 메모 · 계정 값 · 토큰은 리포트에 옮기지 않았다(키 이름 · 건수 · 메뉴 수만).

## KOS 세션

- 테스트 계정으로 만든 세션은 1개(UA 끝 ` (research)`)였다. 끝에 `revoke-active-sign-in` 으로 **해제했다** — 해제 뒤 활성 세션 0(남의 세션은 처음부터 0 · 건드린 것 없음).
- 공개 토큰은 세션이 아니다(남기지 않음). 토큰 · 응답 원문 파일은 scratchpad 에서 지웠다.
