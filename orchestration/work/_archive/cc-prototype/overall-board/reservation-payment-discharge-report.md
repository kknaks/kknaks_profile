# 수납(KOS 화면 딥링크 · 수납 정보 읽기) · 귀가

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-consultation-report.md`(`CS§`)에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/수납.har`(114 · 07:36:32Z ~ 07:37:18Z) · `귀가.har`(19 · 07:37:36Z ~ 07:37:43Z) — gitignore
  - 다른 HAR 9개의 `kos-client-uri`
  - 공개 스펙 openapi.yaml 1.0.1
- 대상 일정: 앞 판 상담 HAR 의 그 일정(신규 고객 · 오늘 18:30 KST). 수납 · 귀가 HAR 의 쓰기가 모두 이 일정과 수납 1건에 대한 것이다(확인)
- 데모 조회만 했다(테넌트 · 키 `assert`). **귀가 쓰기 시험은 하지 않았다** — 오늘 데모에 `PROCEDURE_DONE` 일정이 **0건**이었다(§6 「대상 없음」)
- 표기
  - **확인**: HAR · 데모로 본 것
  - **스펙**: openapi.yaml
  - **추정**: 해석
- 리포트에 id · 이름 · 카드 정보 · 금액 실제 값은 적지 않았다(모양 · 통화만)

---

## 0. 결론

- **딥링크**: KOS 웹 고객 상세의 탭은 주소로 바로 열린다(다른 HAR 에서 본 꼴)

  ```text
  https://app.kos-solution.com/{tenantId}/reservation/schedule/?visitorId={visitorId}&scheduleId={scheduleId}&tab=purchase
  ```

  - `tab` 값은 `reservation · consultation · procedure · purchase` 4개를 봤다. `tab=purchase` 는 `방배정.har` 에서 봤다
  - 이번 수납은 **`tab=consultation`(상담 탭)** 화면에서 했다(`&historyMenu=reservationHistory` 가 붙어 있었다)
  - 로그인은 KOS 웹 세션이 있어야 한다. 주소만으로 로그인을 건너뛰는지는 미확인이다 → Q-102
- **수납 = 쓰기 5번**: `initialize-purchase`(수납 1건 생성) → `add-pending-purchase-items`(상품 옵션 추가) → `schedule/v1/commands/register-purchase`(**일정 ↔ 수납 연결 → 일정 `purchaseIds`**) → `add-transaction`(결제 1건, 이번에는 계좌이체) → `accept-purchase`(수납 확정)
  - 수납 상태: `INITIALIZED · PENDING` → **`ACCEPTED · NOT_IN_PROCESS`**
  - **이번 수납으로 일정에 작업(`tasks`)은 생기지 않았다**(0개 그대로). 「수납 → 시술 목록」은 자동이 아니다(이 경우)
- **수납 정보 읽기**: 공개 `getScheduleDetail.purchaseIds` → 공개 **`getPurchaseSummaries`** 로 모두 읽힌다(데모 확인)
  - 「전체 금액」 = 항목 `items[].priceV2.amount` 합(계산)
  - 「결제 금액」 = 거래 `transactions[].price` 합(계산)
  - 이번 건은 둘이 같았다
  - **「후납」이라는 KOS 값은 없다.** 미결제 잔액은 「전체 − 결제」를 계산해야 한다
  - 통계(`getScheduleStatistics`)에는 이 일정의 금액 필드가 아직 없었다
- **귀가 = 쓰기 1번**: 내부 `schedule/v1/commands/change-flow-step{id, step:"COMPLETED"}`(`PROCEDURE_DONE` → `COMPLETED`) · KOS 「내원 흐름」 화면(`/reservation/flow?id=`)에서 보냈다
  - 그 전에 작업 취소 · 처방전 호출은 없다(이 일정은 작업 0개 · 처방전 0개)
  - 끝 상태: `COMPLETED` · 예약 상태 **`COMPLETED`**
  - 공개 짝 = `changeFlowStep{scheduleId, step:COMPLETED}`
- 정할 것은 **9개**다(Q-102 ~ Q-110)

---

## 1. HAR 인벤토리

### 1.1 `수납.har` — 항목 114

구성: KOS POST 57 + KOS 정적 js 6 + KOS OPTIONS 17 + **`localhost:25001`** 8(POST 4 · OPTIONS 4) + Datadog 23 + Amplitude 3.

- `kos-client-uri` 는 57건 모두 `/{tenantId}/reservation/schedule/?visitorId={visitorId}&scheduleId={scheduleId}&tab=consultation&historyMenu=reservationHistory` 다. `Referer` · `Origin` 은 `https://app.kos-solution.com/`
- **`localhost:25001/health`**(4회 · 응답 0 = 연결 안 됨): 결제할 때 KOS 웹이 이 PC 의 결제 단말 연동 프로그램을 찾는 것으로 보인다(추정). 데모 PC 에는 없었다

KOS POST 57건(경로별 · # 순서)

| 경로 | 횟수 | # | 본문 키 | 응답 · 용도 |
|---|---|---|---|---|
| `role/v2/queries/get-roles` | 3 | 0 · 60 · 71 | — | 역할 |
| `schedule/group/v1/queries/get-reservation-group` | 5 | 1 · 28 · 37 · 61 · 72 | `id` | |
| `procedure-menu/visitors/queries/get-visitors` | 4 | 2 · 12 · 62 · 73 | `sort` | (0) |
| `schedule/v1/queries/get-schedule-summaries` | 3 | 3 · 63 · 74 | `visitorId · sort` | 대상: **`CONSULTATION` · 작업 0** — 수납 전후로 같다 |
| `v1/visitor/queries/get-visitor` | 4 | 4 · 32 · 64 · 75 | `id` | |
| `procedure-menu/product-options/v2/queries/search-product-option-summaries` | 1 | 5 | `searchText · size · deleted · optionTypes[SINGLE, GROUP] · targetCountryCode · baseDateTimeUtc · closed` | 상품 옵션 고르기 창 |
| `account/v2/queries/get-accounts` | 2 | 7 · 46 | `{}` | 담당자 선택지 |
| `procedure-menu/currency-settings/queries/get-currency-settings` | 1 | 17 | — | `KRW` |
| **`purchase/v1/commands/initialize-purchase`** | 1 | **19** | §2 | `{}` |
| **`purchase/v1/commands/add-pending-purchase-items`** | 1 | **21** | §2 | `{}` |
| **`schedule/v1/commands/register-purchase`** | 1 | **24** | §2 | `{}` |
| `purchase/v1/queries/get-purchase-summaries` | **25** | 26 · 35 · 50 · 51 · 53 · 56 · 57 · 68 · 70 · 77 · 79 · 82 · 84 · 85 · 89 · 90 · 94 · 96 · 97 · 99 · 100 · 107 · 109 · 111 · 113 | `purchaseIds[1] · includeDeleted` | **수납 화면이 약 3초마다 다시 읽는다.** #100 까지 `INITIALIZED · PENDING` · #107 부터 `ACCEPTED` |
| `account/v2/queries/get-accounts-last-update…` | 1 | 30 | — | |
| `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | 2 | 41 · 106 | `visitorId` | (0) |
| `purchase/payment-settings/v1/queries/get-payment-settings` | 1 | 43 | — | 결제 수단 설정(카드 · 현금 · 이체 · 플랫폼 · 간편결제 · 선불카드 · 의료대출) |
| **`purchase/v1/commands/add-transaction`** | 1 | **101** | §2 | `{}` |
| **`purchase/v1/commands/accept-purchase`** | 1 | **104** | §2 | `{}` |

합계 57. 쓰기 5건.

### 1.2 `귀가.har` — 항목 19

구성: KOS POST 10 + OPTIONS 2 + Datadog 5 + Amplitude 2.

| # | 경로 | 본문 키 | 응답 | 화면(`kos-client-uri`) |
|---|---|---|---|---|
| 0 | `purchase/v1/queries/get-purchase-summaries` | `purchaseIds · includeDeleted` | `ACCEPTED · NOT_IN_PROCESS` | 고객 상세(상담 탭) |
| 1 | `get-roles` | — | | 〃 |
| 2 | `get-reservation-group` | `id` | | 〃 |
| 3 | `procedure-menu/visitors/…/get-visitors` | `sort` | | 〃 |
| 4 | `get-schedule-summaries` | `visitorId · sort` | 대상: **`PROCEDURE_DONE` · `IN_PROGRESS` · 작업 0** | 〃 |
| 5 | `v1/visitor/queries/get-visitor` | `id` | | 〃 |
| 8 | `get-accounts-last-update…` | — | | **`/reservation/flow`**(내원 흐름 화면) |
| 9 | `schedule/v2/queries/get-schedules-grouped-by-zone` | `zoneIds[2] · 날짜 범위` | 대상: `PROCEDURE_DONE` · 작업 0 · `purchaseIds` 1 · `prescriptionIds` 0 | 〃 |
| 13 | `meta/notice/v1/queries/get-notices` | 날짜 범위 · `deleted` | (0) | 〃 |
| **17** | **`schedule/v1/commands/change-flow-step`** | `id · step:"COMPLETED"` | `{}` | **`/reservation/flow?id={scheduleId}`** |

합계 10. 쓰기 1건.

**두 HAR 사이**: 수납 HAR 끝에서 대상은 `CONSULTATION` 이었고, 귀가 HAR 처음에는 `PROCEDURE_DONE` 이었다. 그 사이의 단계 변경(상담 → 귀가 대기)은 HAR 에 없다. **시술 대기 · 시술을 거쳤는지도 알 수 없다**(작업이 0개라서 시술을 하지 않고 바로 귀가 대기로 보낸 것으로 보인다, 추정) → Q-107

---

## 2. 딥링크

다른 HAR 의 `kos-client-uri` 를 모두 모아 본 KOS 웹 주소 꼴(`{…}` 는 id)

| 주소 | 화면 |
|---|---|
| `/{tenantId}/reservation` | 예약 현황 판 |
| `/{tenantId}/reservation/schedule/?visitorId={visitorId}` (+ `&tab=reservation` · `&reservationWorkspaceMode=…`) | 고객 상세(일정 없이) |
| `/{tenantId}/reservation/schedule/?visitorId={visitorId}&scheduleId={scheduleId}&tab={reservation\|consultation\|procedure\|purchase}` (+ `&historyMenu=reservationHistory`) | **고객 상세 · 그 일정 · 탭** |
| `/{tenantId}/reservation/procedure` · `?id={scheduleId}` | 시술 진행판 |
| `/{tenantId}/reservation/flow` · `?id={scheduleId}` | 내원 흐름(귀가를 보낸 곳) |
| `/{tenantId}/visitor-information` | 고객 정보 |

- 호스트: `https://app.kos-solution.com`
- [수납하기 ›] 후보: `…/reservation/schedule/?visitorId={visitorId}&scheduleId={scheduleId}&tab=purchase`
  - 이번 수납 HAR 은 상담 탭(`tab=consultation`)에서 했다. 수납 탭과 상담 탭 중 어디서 결제 창이 열리는지는 HAR 만으로 알 수 없다 → Q-103
- 로그인: KOS 웹은 직원 로그인 세션이 있어야 한다(앱의 모든 요청이 테넌트 경로 아래 내부 API 이다). 세션이 없을 때 이 주소가 로그인 뒤 그 화면으로 돌아오는지는 확인하지 않았다(브라우저 시험 필요) → Q-102
- KOS 화면은 같은 브라우저(데스크 PC)에서 열린다. 결제 단말은 그 PC 의 `localhost:25001` 프로그램이 받는 것으로 보인다(추정) → Q-104

---

## 3. 수납 쓰기 5건 해부

| 순서 | 호출 | 본문(모양) | 결과 |
|---|---|---|---|
| P1 | `purchase/v1/commands/initialize-purchase` | `{id(새 uuid — 화면이 만든다), visitorId, assigneeId, assigneeIds[1]}` | 수납 1건. `status INITIALIZED` |
| P2 | `purchase/v1/commands/add-pending-purchase-items` | `{purchaseId, items:[{id(새 uuid), type:"PRODUCT_OPTION", optionConfiguration{id, title, productTitle, optionType:SINGLE, procedure{id,name}, count, unit{type,value}, price{value,currency}, medicalService{…}}, price{value, currency:KRW}, priceV2{amount, suppliedAmount, taxFreeAmount, vatAmount, taxation}, basePrice{…}}]}` | `pendingItems[1]` · `process PENDING` |
| P3 | `schedule/v1/commands/register-purchase` | `{scheduleId, purchaseId}` | **일정 `purchaseIds` 에 이 수납이 들어간다**(지금 조회 확인) |
| P4 | `purchase/v1/commands/add-transaction` | `{purchaseId, transaction:{id(새 uuid), price{value, currency}, status:"APPROVED", paymentType:"TRANSFER", transferConfiguration{}, assigneeId, createdDateTimeUtc, suppliedAmount, taxFreeAmount, vatAmount, paymentDateTime{lastUpdatedDateTimeUtc, approvedDateTimeUtc}}}` | 거래 1건 |
| P5 | `purchase/v1/commands/accept-purchase` | `{purchaseId}` | `status ACCEPTED` · `process NOT_IN_PROCESS` · `pendingItems` → **`items`** |

- 결제 수단은 화면에서 고른다(`paymentType`). 수단별 설정 칸은 `card · cash · transfer · platform · prepaidCard · easyPay · medicalLoan` 이 있다
- **작업 `paymentRequired`**: 이 일정은 수납 전후로 작업이 0개였다. 그래서 `paymentRequired` 가 언제 false 가 되는지는 이번 HAR 로 확인하지 못했다 → Q-106
  - 앞 판들(KDA§4 · workflow-v2)에서는 결제 전 작업이 `paymentRequired: true` 였다
  - 내부에는 `schedule/v1/queries/get-payment-required-tasks{visitorId}` 조회가 있다
- **공개 짝: 없음.** 공개 수납 작업은 조회(`getPurchaseSummaries` · `getPurchaseSummariesByVisitor`)뿐이다(스펙 grep)

---

## 4. 수납 정보 읽기 — 데모 조회

| 조회(공개) | 결과 |
|---|---|
| `getScheduleDetail` | `purchaseIds` 1(이번 수납) · `prescriptionIds` 0 · `tasks` 0 · `taskTimers` 0 · 지금 `COMPLETED` · `COMPLETED` |
| `getPurchaseSummaries{purchaseIds}` | 200 · 키 `id · visitorId · status ACCEPTED · process NOT_IN_PROCESS · items[1] · transactions[1] · pendingItems[] · revokingItems[] · refundingItems[] · priceAdjustments[] · assignee · assignees · createdDateTimeUtc · lastUpdatedDateTimeUtc · deleted` |
| ↳ `items[]` | `id · type(PRODUCT_OPTION) · optionConfiguration{title, productTitle, procedure, count, unit, …} · price{value, currency} · priceV2{amount, suppliedAmount, taxFreeAmount, vatAmount, taxation} · basePrice · priceAdjustments` |
| ↳ `transactions[]` | `id · price{value, currency} · status(APPROVED) · paymentType(TRANSFER) · 수단별 configuration · suppliedAmount · taxFreeAmount · vatAmount · paymentDateTime{approvedDateTimeUtc, …} · canceledRefId · assignee` |
| `getPurchaseSummariesByVisitor{visitorId}` | 200 · 1건 |
| `getScheduleStatistics`(오늘) | 이 일정 행은 있다. 그러나 **`optionItemTotalPriceV2` · `paymentTotalAmountV2` 키가 없었다**(금액 미반영 · 갱신 지연인지는 모른다) |

스펙 enum(`protos.purchase.PurchaseSummary`)
- `status`: `INITIALIZED`(초기화) · `PAID`(결제 완료) · `ACCEPTED`(수납 확정) · `PARTIALLY_REFUNDED` · `REFUNDED`
- `process`: `NOT_IN_PROCESS` · `PENDING`(수납 추가 진행 중) · `REVOKING` · `REFUNDING` · `PREPAID_CARD_ITEM_SUBSTITUTING`

**시안 칸에 쓸 수 있는 것**

| 시안 | KOS 원천 | 메모 |
|---|---|---|
| 정산 상자 「전체 금액」 · 원내 현황 카드 「전체」 | `items[].priceV2.amount.value` 합(+ `pendingItems`?) | 계산이다. 이번 건은 항목 1개 |
| 「결제 금액」 · 카드 「결제」 | `transactions[]`(status `APPROVED`) `price.value` 합 | 계산이다. 이번 건은 전체와 같았다. 취소 거래(`canceledRefId`)를 빼야 하는지 → Q-105 |
| **「후납 금액」** | **KOS 에 없음.** 「전체 − 결제」로 계산할 수밖에 없다 | `ACCEPTED`(수납 확정)와 `PAID`(결제 완료)가 따로 있다. 전액을 결제하지 않고도 확정할 수 있는지는 미확인 → Q-105 |
| 「수납 필요」 Badge | 작업 `paymentRequired`(R§3.4) 또는 수납 `status` ≠ `ACCEPTED` | 이번 일정은 작업이 없어서 비교하지 못했다 → Q-106 |
| [수납하기 ›] 뒤 반영 | KOS 수납 화면은 3초마다 다시 읽는다. ccc 는 일정의 `purchaseIds` → `getPurchaseSummaries` 를 읽으면 된다 | 조회 주기 → Q-108 |

---

## 5. 귀가 해부

- 내부 `schedule/v1/commands/change-flow-step{id, step:"COMPLETED"}` → `{}` · 「내원 흐름」 화면
- 전: `PROCEDURE_DONE` · `IN_PROGRESS` · 작업 0 · 수납 1(`ACCEPTED`) · 처방전 0
- 뒤(지금 조회): `COMPLETED` · **`reservation.status COMPLETED`**(예약 상태도 함께 바뀐다) · `flowStepUpdatedDateTimeUtc` = 귀가 시각
- **그 전에 다른 호출이 없었다**: 작업 취소(`cancel-flow-tasks`) · 처방전 · 수납 확인 호출이 HAR 에 없다. 작업이 0개라서 취소할 것도 없었다
  - workflow-v2 의 [귀가 대기] 묶음(`cancel-flow-tasks` → `PROCEDURE_DONE`)은 시술 현황 쪽 규칙이다
  - 「귀가 대기 → 귀가」 사이에는 KOS 가 다른 호출을 요구하지 않는다(이 경우)
- 공개 스펙 `changeFlowStep` 400: 「귀가 단계로 바꿀 때 **완료되지 않은 시술이 있으면** `procedures NotAvailable`」. 작업이 있는 고객은 남은 작업을 끝내거나 취소해야 귀가가 될 것이다(스펙). 이번 HAR 은 작업이 없어서 그 경우는 보지 못했다
- **공개 짝**: `changeFlowStep{scheduleId, step:"COMPLETED"}` — 같은 단계 변경이다(앞 판 RT§2.3 처럼 결과가 같은지는 시험하지 못했다, §6)

---

## 6. 데모 쓰기 시험 — 대상 없음

- 오늘(KST) 데모에서 공개 `getSchedulesByFlowStep(PROCEDURE_DONE)` = **0건**(확인)
- 지시대로 다른 단계에서 억지로 올리지 않았다. **귀가 쓰기는 보내지 않았다**
- 귀가 대기 일정이 생기면 같은 모양(`changeFlowStep{scheduleId, step:COMPLETED}`)으로 시험할 수 있다 → Q-110

---

## 7. 호출 기록 (조회만)

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| 공개 | `getScheduleDetail` 1 · `getPurchaseSummaries` 1 · `getPurchaseSummariesByVisitor` 1 · `getScheduleStatistics` 1 · `getSchedulesByFlowStep(PROCEDURE_DONE)` 1 | 5 | 200 |
| 인증 | 공개 `exchange-token` 1 · 내부 sign-in 1 | 2 | 200 |

**쓰기 0건** · 운영 키 0건.

---

## 8. 정할 것 (결정하지 않음) — 9개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-102 | [수납하기 ›] 딥링크의 로그인 | KOS 웹 세션이 없는 PC · 브라우저에서 주소를 열면 어떻게 되는지 브라우저에서 확인해야 한다. 데스크 PC 에 KOS 가 늘 로그인되어 있다고 가정할지 | — |
| Q-103 | 어느 탭으로 열지 | `tab=purchase`(수납 탭) · `tab=consultation`(이번 HAR 이 결제한 곳) 중 어디서 결제 창이 바로 뜨는지 | — |
| Q-104 | 결제 단말 | KOS 웹이 `localhost:25001` 단말 프로그램을 찾는다. 데스크 PC 에 설치가 필요한지 · ccc 와 상관없는지 | — |
| Q-105 | 「결제 금액」 · 「후납」 계산 | KOS 에 잔액 필드가 없다. 항목 합 − 승인 거래 합으로 계산할지 · 취소 거래 · 가격 조정(`priceAdjustments`) · `pendingItems` 를 어떻게 셀지. `ACCEPTED` 와 `PAID` 의 차이도 정해야 한다 | R Q-15 |
| Q-106 | 「수납 필요」 판정 | 작업 `paymentRequired` · 수납 `status` 중 무엇으로 할지. 이번 수납은 작업을 만들지 않아서 `paymentRequired` 가 바뀌는 때를 보지 못했다 | R Q-15 |
| Q-107 | 수납 → 시술 목록 | 이번 수납은 일정 작업을 만들지 않았다. 시술 작업은 상담 시술 · 동선 추가로 따로 생기는 것으로 보인다. 시술 현황의 「수납 뒤 시술 목록이 올라온다」(workflow-v2 1)와 맞는지 확인할지 | — |
| Q-108 | 수납 정보 조회 주기 | KOS 화면은 3초마다 다시 읽는다. ccc 정산 상자 · 원내 현황 카드는 언제 다시 읽을지(시술 현황 10초 규칙 · 화면 열 때) | — |
| Q-109 | 처방전 | 일정 `prescriptionIds` 만 있고 내용을 읽는 공개 · 내부 호출은 이번에도 보지 못했다. 정산 상자 「처방전」을 어떻게 할지 | R Q-19 |
| Q-110 | [귀가 완료] 시험 | 오늘 데모에 귀가 대기 일정이 없어서 공개 `changeFlowStep(COMPLETED)` 를 보내지 못했다. 귀가 대기 일정이 생기면 다시 허가할지. 남은 작업이 있으면 KOS 가 거절한다(스펙) — ccc 가 귀가 전에 작업을 취소할지(`cancel-flow-tasks`, 시술 현황 규칙) | — |
