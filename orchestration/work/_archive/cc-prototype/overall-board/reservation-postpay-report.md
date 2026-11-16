# 후납 — 시술 중 추가 시술 → 「수납 필요」 (HAR 해석 · 조회)

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-payment-discharge-report.md`(`PD§`)에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/수납필요 추가.har`(120항목 · 07:51:06Z ~ 07:52:07Z, gitignore)
  - 공개 스펙 openapi.yaml 1.0.1
  - 시술 현황 코드 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/back`(read-only, HEAD `d05cd88` 2026-10-26)
- 대상 일정: 앞 판들의 시험 일정이 아닌 **다른 데모 일정 1건**(오늘 19:00 KST · HAR 처음 `RECEPTION` · 작업 0)
- **KOS 쓰기 0건.** 데모 조회만 했다(테넌트 · 키 `assert`, 쓰기 허가 목록 비움). 운영 키 0
- 표기
  - **확인**: HAR · 데모로 본 것
  - **스펙** · **코드**: 문서 · 코드에 적힌 것
  - **추정**: 해석
- 리포트에 id · 이름 · 금액 실제 값은 적지 않았다(모양 · 통화 KRW 만)

---

## 0. 결론

- **장면**: 수납 2건을 **모두 결제 · 확정한 뒤**(각 `ACCEPTED`) 시술 작업 2개를 동선에 넣었다
  - 작업 ①은 **결제한 수납에서 나온 시술권(`ticketConfiguration.ticketId`)으로** 넣었다 → `paymentRequired: false`
  - 작업 ②는 **수납하지 않은 상품 옵션(`productOptionConfiguration` 만, 시술권 없음)으로** 넣었다 → **`paymentRequired: true`**
  - 이것이 「후납」 = 결제 뒤의 추가 시술이다(지금 데모 조회 확인)
- **「수납 필요」의 원천 = 작업 `tasks[].paymentRequired`**(작업마다 붙는 bool)
  - 이번 일정의 수납 2건은 모두 `ACCEPTED · NOT_IN_PROCESS` 인데 작업 ②는 `paymentRequired: true` 였다 → **수납 `status` 로는 알 수 없다**
  - KOS 는 작업을 넣을 때 시술권이 붙어 있으면 결제된 것, 옵션만 있으면 결제가 필요한 것으로 판정하는 것으로 보인다(추정 — 본문에 `paymentRequired` 칸을 보내지 않았는데 값이 갈렸다)
- **후납 「금액」을 KOS 가 주는 값은 없다**
  - 작업에 가격 필드가 없다
  - 수납 2건은 「항목 합 = 결제 합」으로 잔액이 0 이다(추가 시술은 수납에 아예 들어 있지 않다)
  - `pendingItems` 도 비어 있다
  - 금액을 보이려면 작업의 상품 옵션 id → 공개 `getProductOptions.price`(정가)로 **계산 · 추정**해야 한다. 정가이고 실제 받을 값이 아니다 → Q-111
- **시술 현황판과 같은 규칙이다**
  - `procedure/back` 은 카드 「수납 필요」 = 작업 중 **「방 배정」을 뺀** 작업 하나라도 `paymentRequired` 이면 참(`app/domain/rules.py:111-112`)
  - 원천은 KOS `tasks[].paymentRequired`(`app/kos/sync.py:131`)
  - 취소(`CANCELED`) 작업은 뺀다(`rules.py` `items`)
- 정할 것은 **7개**다(Q-111 ~ Q-117)

---

## 1. HAR 인벤토리

항목 120 = KOS POST 80 + OPTIONS 2 + Datadog 28 + Amplitude 10.

`kos-client-uri` 의 탭은 순서대로 이렇게 바뀌었다(고객 상세 `…/reservation/schedule/?visitorId&scheduleId&tab=`)
- `reservation` — #0 ~ #33, 수납 ①
- `consultation` — #36 ~ #83, 수납 ②
- `purchase` — #84 ~ #94, 작업 ①
- `procedure` — #95 · #96
- `consultation` — #99
- `purchase` — #100 ~ #119, 작업 ②

KOS POST 80건(경로별 · # 순서)

| 경로 | 횟수 | # | 본문 키 | 응답 · 용도 |
|---|---|---|---|---|
| `role/v2/queries/get-roles` | 1 | 0 | — | |
| `schedule/v1/queries/get-schedule-summaries` | 1 | 1 | `visitorId · sort` | 대상: **`RECEPTION` · `IN_PROGRESS` · 작업 0** |
| `schedule/group/v1/queries/get-reservation-group` | 9 | 2 · 17 · 22 · 61 · 67 · 87 · 90 · 109 · 113 | `id` | |
| `procedure-menu/visitors/queries/get-visitors` | 4 | 3 · 5 · 50 · 103 | `sort` | (0) |
| `v1/visitor/queries/get-visitor` | 3 | 4 · 19 · 64 | `id` | |
| `procedure-menu/product-options/v2/queries/search-product-option-summaries` | 6 | 6 · 8 · 51 · 52 · 104 · 105 | `searchText · size · deleted · optionTypes[2] · (targetCountryCode) · baseDateTimeUtc · closed` | 상품 옵션 고르기(국가 코드 2자 · 3자로 두 번씩 부른다) |
| `account/v2/queries/get-accounts` | 2 | 7 · 27 | `{}` | |
| **`purchase/v1/commands/initialize-purchase`** | 2 | **12 · 57** | `id · visitorId · assigneeId · assigneeIds` | 수납 ① · ② 생성 |
| **`purchase/v1/commands/add-pending-purchase-items`** | 2 | **13 · 58** | `purchaseId · items[1]{…PRODUCT_OPTION…}` | 항목 추가 |
| **`schedule/v1/commands/register-purchase`** | 2 | **15 · 59** | `scheduleId · purchaseId` | 일정 `purchaseIds` 1 → 2 |
| `purchase/v1/queries/get-purchase-summaries` | 26 | 16 · 21 · 29 · 30 · 37 · 39 · 42 · 46 · 49 · 54 · 60 · 66 · 73 · 74 · 76 · 77 · 83 · 89 · 94 · 95 · 99 · 107 · 112 · 116 · 118 · 119 | `purchaseIds[1→2] · includeDeleted` | 약 3초마다 다시 읽는다(PD§1.1 과 같다) |
| `account/v2/queries/get-accounts-last-update…` | 4 | 18 · 62 · 88 · 110 | — | |
| `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | 4 | 25 · 34 · 70 · 81 | `visitorId` | (0) |
| `purchase/payment-settings/v1/queries/get-payment-settings` | 2 | 26 · 71 | — | |
| **`purchase/v1/commands/add-transaction`** | 2 | **31 · 78** | `purchaseId · transaction{price, status:APPROVED, paymentType(①CASH · ②TRANSFER), …}` | 결제 |
| **`purchase/v1/commands/accept-purchase`** | 2 | **33 · 80** | `purchaseId` | 수납 확정 |
| `ticket/v1/queries/get-ticket-bundles` | 5 | 36 · 41 · 45 · 84 · 100 | `visitorId · sort` | **결제한 수납마다 시술권 묶음이 생긴다**(#84: 묶음 6, 이 중 2개가 이번 수납 ① · ②의 것) |
| **`schedule/v1/commands/add-flow-tasks`** | 2 | **85 · 108** | §2 | 작업 ① · ② |
| `image/visitor-image/v1/queries/get-visitor-images` | 1 | 96 | `visitorId · scheduleId · deleted` | (0) — 시술 탭 |

합계 80. 쓰기 12건 = 수납 5단계 × 2 + 작업 추가 2.

---

## 2. 장면 복원

| 순서 | 시각(Z) | 쓰기 | 무엇 | 「수납 필요」 |
|---|---|---|---|---|
| 1 | 51:08 ~ 51:12 | 수납 ①: initialize → add-pending-items → register → add-transaction(현금) → accept | 상품 옵션 1개 수납 · 결제 · 확정. 결제 합 = 항목 합 | 작업 없음 |
| 2 | 51:14 ~ | (조회) 시술권 묶음 | 수납 ①의 시술권이 생겼다 | |
| 3 | 51:31 ~ 51:41 | 수납 ②: 같은 5단계(계좌이체) | 다른 상품 옵션 1개 수납 · 결제 · 확정 | 작업 없음 |
| 4 | 51:44 | **작업 ①** `add-flow-tasks` | `PROCEDURE` · `productOptionConfiguration`(수납 ② 항목의 옵션) + **`ticketConfiguration{ticketId(수납 ②의 시술권), round{total:1, current:1}}`** + `medicalServiceConfiguration` | **꺼짐** — `paymentRequired: false` |
| 5 | 51:57 | **작업 ②** `add-flow-tasks` | `PROCEDURE` · `productOptionConfiguration`(**수납 ①·② 어디에도 없는 옵션**) + `medicalServiceConfiguration`. **`ticketConfiguration` 없음** | **켜짐** — `paymentRequired: true` |

- 작업 ①의 시술권 id 는 #84 시술권 묶음 목록에 있다(확인). 작업 ②의 옵션 id 는 두 수납의 항목에 없다(확인)
- `add-flow-tasks` 본문에는 두 번 모두 `paymentRequired` 칸이 **없다**. 값은 KOS 가 정했다(확인: 지금 조회에서 ① false · ② true)
- **수납 ①의 시술권은 아직 동선에 들어가지 않았다.** 사용자가 고른 것은 수납 ②의 시술권과 수납하지 않은 옵션이다(이 장면에서 시술권 하나가 남아 있다)

**작업이 추가된 뒤 결제하면 꺼지는지**는 이 HAR 에 없다. 작업 ②를 위한 세 번째 수납은 하지 않았다 → Q-113

---

## 3. 지금 데모 상태 (조회)

| 조회 | 결과 |
|---|---|
| 공개 `getScheduleDetail` | `RECEPTION` · `IN_PROGRESS` · 「4층」 · `purchaseIds` 2(HAR 의 두 수납) · 작업 2 |
| ↳ 작업 seq 1(HAR 작업 ①) | `PROCEDURE · NOT_STARTED · paymentRequired false · 시술권 있음 · 방 없음` |
| ↳ 작업 seq 2(HAR 작업 ②) | `PROCEDURE · NOT_STARTED · **paymentRequired true** · 시술권 없음 · 방 없음` |
| 공개 `getPurchaseSummaries`(두 id) | 둘 다 `ACCEPTED · NOT_IN_PROCESS` · 항목 1 · 거래 1 · `pendingItems` 0. 수납마다 항목 합 = 결제 합(확인) |
| 내부 `schedule/v1/queries/get-payment-required-tasks{visitorId}` | **200 · 0건.** 작업 ②가 `paymentRequired: true` 인데도 비어 있다. 이 조회가 무엇을 기준으로 「수납 필요 작업」을 모으는지는 모른다 → Q-114 |
| 공개 `getScheduleStatistics`(오늘) | 이 일정 행이 없었다(앞 판처럼 금액은 볼 수 없었다) |
| 공개 `getProductOptions{optionIds:[작업 ②의 옵션]}` | 200 · 옵션 1 · `price{amount, additional}`(정가) — 작업 ②에 가격을 붙인다면 쓸 수 있는 유일한 KOS 값이다 |

---

## 4. 「수납 필요」 · 후납 금액 — 원천 정리

| 무엇 | KOS 값 | 메모 |
|---|---|---|
| 「수납 필요」 켜짐 | **`tasks[].paymentRequired == true` 인 작업이 있다** | 수납 status 와 상관없다(두 수납 모두 확정인데 켜졌다) |
| 결제 전에 넣은 작업 ↔ 결제 뒤 넣은 작업 | 결제 뒤라도 **시술권으로 넣으면 false, 옵션만으로 넣으면 true** | 앞 판(KDA§4) 데모에서 결제 전 작업이 true · 시술권 없음이었던 것과 맞는다(추정: 시술권 유무가 판정 근거) |
| 「전체 금액」 | 수납 항목 합(이미 수납한 것) — **추가 시술 ②는 들어 있지 않다** | 추가 시술까지 넣으려면 작업 ②의 옵션 정가를 더해야 한다(계산 · 정가 추정) |
| 「결제 금액」 | 수납 거래 합(`APPROVED`) | 계산 |
| **「후납 금액」** | **KOS 에 없음** | 「전체 − 결제」를 해도 0 이다(수납이 다 끝났으므로). 후납은 「`paymentRequired` 작업들의 정가 합」으로만 추정할 수 있다 → Q-111 |
| 미결제 수납 | 이번 장면에는 없다(`PENDING` · `INITIALIZED` 수납 0) | 상담사가 수납을 만들어 두고 결제를 미루면 `INITIALIZED/PENDING` 수납이 생길 수 있다(PD§3 의 중간 상태) → Q-112 |

---

## 5. 시술 현황판 규칙과 비교 (`procedure/back`, read-only)

| 위치 | 내용 |
|---|---|
| `app/kos/sync.py:131` | KOS 작업마다 `payment_required = bool(t.get("paymentRequired"))` 로 저장 |
| `app/domain/rules.py:87-93` `items` | 카드 작업 = KOS 목록에 있고 `CANCELED` 가 아닌 작업 전부(type 무관) |
| `app/domain/rules.py:95-97` `procedures` | `items` 에서 「방 배정」(방 붙은 ETCETERA · ccc 가 호출한 적 없음)을 뺀 것 |
| `app/domain/rules.py:111-112` `payment_required` | `any(p.payment_required for p in self.procedures(v))` |
| `app/schemas/board.py:127` | 카드 계약 `paymentRequired: bool` |

→ **같은 규칙이다**: 작업 `paymentRequired` 하나라도 참이면 「수납 필요」.
- 예약 현황(원내 현황 카드 · 정산 상자)도 같은 판정을 쓰면 두 화면이 맞는다
- 차이가 생길 수 있는 곳
  - 시술 현황은 「방 배정」 · 취소 작업을 뺀다(예약 쪽도 뺄지)
  - 시술 현황 카드는 **시술 대기부터**만 생긴다. 이번 일정처럼 `RECEPTION` 에서 작업이 생긴 경우는 예약 쪽에서만 보인다

---

## 6. 호출 기록 (조회만)

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| 공개 | `getScheduleDetail` 1 · `getPurchaseSummaries` 1 · `getScheduleStatistics` 1 · `getProductOptions` 1 | 4 | 200 |
| 내부 | `schedule/v1/queries/get-payment-required-tasks` 1 | 1 | 200 |
| 인증 | 공개 `exchange-token` 2 · 내부 sign-in 1 | 3 | 200 |

**쓰기 0건** · 운영 키 0건. 코드 레포는 grep · 읽기만 했다.

---

## 7. 정할 것 (결정하지 않음) — 7개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-111 | 「후납 금액」을 보일지 · 무엇으로 | KOS 에 값이 없다. `paymentRequired` 작업의 옵션 정가(`getProductOptions.price`) 합으로 추정할지(할인 · 프로모션이 반영되지 않는다), 금액 없이 「수납 필요」만 보일지 | PD Q-105 |
| Q-112 | 「전체 · 결제」 계산 범위 | 수납이 여러 건(`purchaseIds[]`)이다. 모든 수납의 항목 합 · 승인 거래 합을 더할지, 미확정(`INITIALIZED/PENDING`) 수납을 넣을지 | PD Q-105 |
| Q-113 | 「수납 필요」가 꺼지는 때 | 결제 뒤 추가된 작업을 그 뒤에 수납하면 KOS 가 그 작업을 false 로 바꾸는지(시술권이 붙는지 · 작업이 바뀌는지) 이 HAR 에 없다. 데모에서 한 번 더 HAR 을 뜰지 · 시험할지 | PD Q-106 |
| Q-114 | 내부 `get-payment-required-tasks` | `paymentRequired` 작업이 있는데 0건이 왔다. 이 조회를 쓰지 않고 일정 작업으로 판정할지 | — |
| Q-115 | 예약 쪽 「수납 필요」 판정 규칙 | 시술 현황과 같게(「방 배정」 · 취소 작업 제외) 할지 | `_RESUME` 10-25 |
| Q-116 | [귀가 완료] 꺼짐 조건 | 시안은 「후납이 남으면 꺼짐」이다. KOS 값으로는 「`paymentRequired` 작업이 있으면 꺼짐」이 된다. 그 작업을 KOS 에서 취소한 경우 · 끝난 경우를 어떻게 셀지 | PD Q-110 |
| Q-117 | 남은 시술권 | 결제했지만 동선에 넣지 않은 시술권이 남을 수 있다(이번 장면: 수납 ①의 시술권). 예약 상세에 「미사용 시술권」을 보일지 | — |
