# HAR 확인 리포트 3차 — 환불 · 시술 사용 후 환불 · 선불카드 공유 · 시술권2

- 브리프: task_491ba532810d(3차) · 형식 · 금지 규칙은 1 · 2차와 같다(`har-check-report.md` · `har-check-report-2.md`).
- 근거 표기: `파일.har#n` = HAR `log.entries[n]`. id 는 「id(str)」. 같은 id 인지 대조할 때만 리포트 안 이름(구매 A~H · 카드 1~5)으로 부른다.
- 이름은 1 · 2차를 잇는다.
  - 구매 A · B · C = 2차와 같음(구매 C = 선불카드 상품 「비공개 멤버십1」 500,000 → 2차에서 현금 취소).
  - 카드 1 · 2 · 3 = 2차와 같음(카드 3 = 구매 C 로 생긴 카드).
  - **새로**:
    - 구매 D = 선불카드 상품 「VIP 플랜3」 30,000,000 → **카드 4**
    - 구매 E = 승모근보톡스100 440,000 · 카드 4 로 결제
    - 구매 F = 「비공개 멤버십1」 500,000 다시 구매 → **카드 5**
    - 구매 G = 승모근보톡스100 440,000 · 카드 5 로 결제
    - 구매 H = 다른 고객의 크라이오 진정관리 5회 328,900(`시술사용후환불`)

## 0. 다섯 HAR 의 관계(시각 UTC)

| 시각 | HAR | 고객 | 무엇 |
|---|---|---|---|
| 05:12:53–05:13:20 | `선불카드공유.har` | 고객 1(구매 A~G 의 고객) | 카드 4 에 다른 고객 1명 추가 → 카드 고객 목록 |
| 05:18:38–05:19:23 | `환불1.har` | 고객 1 | 구매 C 전액 환불 → `REFUNDED` |
| 05:18:38–05:21:07 | `환불2.har` | 고객 1 | **`#0~#46` 이 `환불1.har` 47건과 URL · 시작 시각까지 같다**(같은 녹화의 앞부분) → 이어서 구매 F 결제 → 카드 5 로 구매 G 결제 → 구매 F 환불 시작(완료 명령은 HAR 끝까지 없음 → `REFUNDING`) |
| 05:22:07–05:22:22 | `시술권2.har` | 고객 1 | 환불 1 · 2 **뒤** 시술권 탭 · 일정 상세 · 선불카드 · 구매 조회. 구매 F 는 여기서 이미 `PARTIALLY_REFUNDED`(완료 명령은 두 HAR 사이 05:21:07–05:22:07 에 있었다 — 구매 F `lastUpdatedDateTimeUtc` 05:21:12) |
| 07:17:08–07:18:05 | `시술사용후환불.har` | 고객 2(다른 고객) | 구매 H 티켓 1장으로 작업 추가 → 완료 → 구매 H 부분 환불 → `PARTIALLY_REFUNDED` |

- 사용자 「`환불2` 는 한 구매가 `REFUNDING` 으로 끝난다」 = 구매 F. **HAR 녹화가 완료 명령 전에 끝났을 뿐이다** — 1분 뒤 `시술권2.har#27 · #30` 에서 `PARTIALLY_REFUNDED` 다.
- `시술권2.har` 는 고객 1 이고, `시술사용후환불.har` 는 고객 2 다. 그래서 「환불된 시술권」(S4)은 이 HAR 들로 직접 볼 수 없다(아래 S4).

## S1 환불 흐름

### 명령 — 요청 body 전체 키 · 순서 · 응답

`시술사용후환불.har`(구매 H) 기준. 환불 1 · 2 도 키는 같다. 응답은 전부 `{}` 다.

| # | 명령 | 요청 body |
|---|---|---|
| 45 | `purchase/v1/commands/start-purchase-refund` | `{purchaseId}` |
| 46 | `purchase/v1/commands/mark-purchase-items-for-refund` | `{purchaseId, refundingItems[{targetItemId, adjustedPrice{amount{value,currency}, suppliedAmount, taxFreeAmount, vatAmount, taxation}}]}` |
| 55 | `purchase/v1/commands/add-canceled-transaction` | `{purchaseId, transaction{id, price, status:"CANCELED", paymentType, cashConfiguration{}, assigneeId, canceledRefId, createdDateTimeUtc, suppliedAmount, taxFreeAmount, vatAmount, paymentDateTime{lastUpdatedDateTimeUtc, approvedDateTimeUtc, canceledDateTimeUtc}}}` — 1차 취소 명령과 **같은 모양** |
| 68 | `purchase/v1/commands/add-transaction` | `{purchaseId, transaction{id, price, status:"APPROVED", paymentType, cashConfiguration{}, assigneeId, createdDateTimeUtc, suppliedAmount, taxFreeAmount, vatAmount, paymentDateTime{lastUpdatedDateTimeUtc, approvedDateTimeUtc}}}` — 1차 결제 명령과 같은 모양 |
| 73 | `purchase/v1/commands/complete-purchase-refund` | `{purchaseId}` |

- 순서: 화면 이벤트 「환불 버튼 클릭」(`#41` amplitude `purchase.click.refund_purchase_button`) → `start` 와 `mark` 가 **바로 붙어서** 나간다(#45 → #46 · 사이에 조회 없음). 그 뒤 원거래 전액 취소, 남길 금액 재결제, 완료 순이다.
- 거래 id(`transaction.id`)는 화면이 만든다. 1차 결제 · 취소와 같다.
- 세 HAR 의 명령 순서:

| HAR · 구매 | 명령 순서 |
|---|---|
| `시술사용후환불` · 구매 H(#45~#73) | start → mark(65,780) → 취소 −328,900 → 결제 +65,780 → complete |
| `환불1` · 구매 C(#17~#43) | start → mark(0) → 취소 −500,000 → complete. **재결제 없음** |
| `환불2` · 구매 F(#131~#175) | start → mark(440,000) → 결제 +440,000(#158) → 그 결제 취소 −440,000(#164) → 원거래 취소 −500,000(#170) → 결제 +440,000(#175) → (complete 는 HAR 밖) |

- 구매 F 의 #158 · #164 는 화면에서 잘못 누른 뒤 되돌린 것으로 **보인다**(같은 금액 결제 → 10초 뒤 취소). KOS 는 거래 순서를 막지 않는다.

### `refundingItems` 한 건 구조

```text
refundingItems[] = {
  targetItemId(str)                 — 구매 항목 id(items[].id)
  adjustedPrice {                   — 환불 뒤 「남는」 금액(고객이 최종 부담) · 환불액 아님
    amount{value,currency}          — 구매 H 65,780 · 구매 C 0 · 구매 F 440,000
    suppliedAmount{value,currency}  — 59,800 · 0 · 400,000
    taxFreeAmount{value,currency}   — 0 · 0 · 0
    vatAmount{value,currency}       — 5,980 · 0 · 40,000
    taxation                        — TAXABLE
  }
}
```

- 구매 H: 원 항목 328,900(공급 299,000 · 부가세 29,900)의 정확히 1/5 이다(59,800 = 299,000 ÷ 5 · 5,980 = 29,900 ÷ 5).
- 진행 중(`REFUNDING`)에는 구매의 `refundingItems` 에 위 한 건이 그대로 보인다(`시술사용후환불.har#50` · `환불2.har#23`).
- **완료(`complete-purchase-refund`) 뒤**:
  - `refundingItems` 는 다시 0건이 된다.
  - 대신 **구매 항목에 두 키가 새로 붙는다**(`시술사용후환불.har#75` · `시술권2.har#30`).
    - `adjustedPrice{value,currency}` — 금액만
    - `adjustPriceV2{amount, suppliedAmount, taxFreeAmount, vatAmount, taxation}` — 분해
  - 이름이 다르다: 명령의 `adjustedPrice` 는 분해 객체다. 항목에서는 `adjustedPrice` 가 금액만이고, 분해는 `adjustPriceV2` 에 있다.
- `revokingItems`: 이번 다섯 HAR 을 포함한 **모든 HAR 에서 0건**이다. 이름 · 명령도 HAR 에 없다(`revoke` grep: KOS API 0건). 그래서 **`refundingItems` 와 어떻게 다른지는 확인 안 됨**이다.

### 상태 · 진행 전이(구매 단위)

| 시점 | `status` | `process` | `refundingItems` | 근거 |
|---|---|---|---|---|
| 환불 전(확정 구매) | `ACCEPTED` | `NOT_IN_PROCESS` | 0 | `시술사용후환불.har#0` |
| start + mark 뒤 | `ACCEPTED` | **`REFUNDING`** | 1 | `#50` · `환불2.har#23` |
| 취소 거래 · 재결제 뒤 | `ACCEPTED` | `REFUNDING` | 1 | `#58` · `#72` |
| complete 뒤 · 남는 금액 > 0 | **`PARTIALLY_REFUNDED`** | `NOT_IN_PROCESS` | 0 | `#75`(구매 H) · `시술권2.har#30`(구매 F) |
| complete 뒤 · 남는 금액 = 0 | **`REFUNDED`** | `NOT_IN_PROCESS` | 0 | `환불2.har#44`(구매 C · 05:19:20) |

- start 와 mark 가 붙어 나가서 「start 만 한 상태」는 보지 못했다.
- 지금까지 본 구매 상태값은 다음과 같다.
  - `status`: `INITIALIZED` · `ACCEPTED` · `REFUNDED` · `PARTIALLY_REFUNDED`
  - `process`: `PENDING` · `NOT_IN_PROCESS` · `REFUNDING`
  - 전체 목록(다른 값이 있는지)은 확인 안 됨이다.
- **거래 합계 = 남는 금액**이다(세 구매 모두 맞음).

| 구매 | 거래(승인 − 취소) | 합계 | `adjustedPrice` |
|---|---|---|---|
| 구매 H | +328,900 −328,900 +65,780 | 65,780 | 65,780 |
| 구매 C | +500,000 −500,000 +500,000 −500,000 | 0 | 0 |
| 구매 F | +500,000 +440,000 −440,000 −500,000 +440,000 | 440,000 | 440,000 |

### 취소 vs 환불

| | 취소(1 · 2차) | 환불(3차) |
|---|---|---|
| 명령 | `add-canceled-transaction` **하나** | `start-purchase-refund` → `mark-purchase-items-for-refund` → `add-canceled-transaction` →(`add-transaction`)→ `complete-purchase-refund` |
| 거래 | 음수 `CANCELED` + `canceledRefId` | **같음**(같은 명령) + 남길 금액 재결제(`APPROVED`) |
| 구매 상태 | `ACCEPTED/NOT_IN_PROCESS` 그대로 | `ACCEPTED/REFUNDING` → `REFUNDED` 또는 `PARTIALLY_REFUNDED` / `NOT_IN_PROCESS` |
| 구매 항목 | 변화 없음 | 진행 중 `refundingItems` 1건 → 완료 뒤 항목에 `adjustedPrice` · `adjustPriceV2` |
| `price` · `priceV2` · `basePrice` | 그대로 | **그대로**(S2) |
| 선불카드 상품 구매의 카드 | **그대로 남음**(2차 R6 · 카드 3 금액 500,000 · 포인트 50,000) | **비워짐**(S5 · 카드 3 금액 0/0 · 포인트 0/0) |
| 티켓 | 그대로(2차 R2) | 확인 안 됨(S4) |
| 재결제 | 같은 구매에 거래 추가 · 상태 그대로 | 환불 안에서 남길 금액만 재결제 |

## S2 부분 환불 금액 — `시술사용후환불.har`

- **값이 맞는가**: `adjustedPrice` 65,780 = 번들 328,900 ÷ 회차 5 × 쓴 1회 = **KOS 티켓 1장 가격**(`#3 · #36` 티켓 `price` 65,780). 두 계산이 같은 값이라 KOS 가 어느 쪽으로 셈했는지는 구분 안 된다. 공급 · 부가세도 원 항목의 1/5 로 정확히 나뉜다.
- **화면이 계산해 준 흔적**: 환불 버튼(#41) → `start`(#45) → `mark`(#46) 사이에 **조회 요청 없음**. 그 전 마지막 조회는 시술권 번들(#36 · 티켓 상태 · 가격 포함)과 구매(#42 · #44)다. 계산은 **화면 안에서** 한 것으로 보인다. 계산 전용 경로 · 이벤트는 HAR 에 없다.
- **직원이 고친 흔적**:
  - 환불 클릭 뒤 amplitude 는 `[Amplitude] Form Started`(#69) 하나뿐이다. 입력값 · 수정 이벤트는 없다.
  - 금액이 공식값과 같으니 **고친 흔적은 없다.** 다만 고칠 수 있는 화면인지는 확인 안 됨이다.
  - 구매 F(`환불2.har#132`)의 440,000 = 카드 5 에서 쓴 금액(카드 5 금액 500,000 → 60,000 · `환불2.har#117`)이다. 선불카드 상품은 「쓴 금액」으로 셈한 것으로 보인다.
- **환불 뒤 구매 항목 `price` · `priceV2` · `basePrice`**: **바뀌지 않는다**. 구매 H 는 328,900 셋 다 그대로다(#0 · #50 · #75). 구매 C · F 도 500,000 그대로다(`시술권2.har#30`). 남는 금액은 새 키 `adjustedPrice` · `adjustPriceV2` 에만 있다.
- `priceAdjustments`: 환불 전후 모두 0건이다. 환불은 할인 조정과 별개 칸이다.

## S3 시술 사용 — `시술사용후환불.har#9~#36`

| # | 명령 | 요청 body |
|---|---|---|
| 9 | `schedule/v1/commands/add-flow-tasks` | `{scheduleId, tasks[{type:"PROCEDURE", title, procedureConfiguration{productOptionConfiguration{optionId, optionTitle, procedure{id,name,createDate}, unit{type:"UnitType_UNKNOWN", value:0}, translsMap}, **ticketConfiguration{ticketId, round{total, current}}**, medicalServiceConfiguration{id, code, title, translsMap, machines[{id,name}], caution}}, translsMap{title{translation{17개 언어}}}}]}` |
| 22 | `schedule/flow/v1/commands/change-tasks-assignees` | `{scheduleId, sequences[3], assigneeIds[1]}` |
| 25 | `schedule/flow/v1/commands/change-tasks-doctors` | `{scheduleId, sequences[3], doctorIds[1]}` |
| 29 | `schedule/flow/v1/commands/change-tasks-complete` | `{scheduleId, sequences[3], complete:true}` |

- **작업이 티켓을 가리키는 칸** = `procedureConfiguration.ticketConfiguration.ticketId`. 값은 구매 H 번들의 **첫 번째 티켓**이다(`#3` 목록 첫 행 · 생성 시각 정렬 · 5장 모두 같은 시각).
- **round 값**(1 · 2차 미확인 → **닫힘**): `round{total: 5, current: 1}`. 「5회 중 1회째」다. 화면이 작업을 만들 때 보낸다. 화면 이벤트 「시술권 목록에서 남은 시술 하나 추가」(#10 `clicked.remained_procedure_add_each+available_ticket_list`)가 있었다.
- 작업 이후 명령(담당 · 의사 · 완료)은 작업 순번 `sequences` 로만 가리킨다. 티켓 id 는 다시 나오지 않는다.
- **티켓이 `USED` 가 되는 지점**:
  - `#5`(작업 추가 전): 5장 모두 `AVAILABLE`.
  - `#36`(완료 #29 뒤): 그 티켓 1장만 **`USED`**, 4장 `AVAILABLE`.
  - 작업 추가(#9)와 완료(#29) 사이에는 시술권 조회가 없다. 그래서 작업 추가 때 `IN_USE` 가 되는지는 **확인 안 됨**이다.
  - 다른 고객 표본에서 `IN_USE` 티켓은 계속 있다(`#3` 승모근 1장 · `시술권2.har#19` 5장). 작업 연결 · 미완료 상태로 **보인다.** `USED` 로 바뀐 직접 원인은 `change-tasks-complete` 라고 보이지만, 응답이 `{}` 라 증거는 전후 조회뿐이다.
- 작업 완료로 구매는 바뀌지 않는다(#28 · #32 구매 H 그대로).

## S4 환불된 시술권

- **환불 뒤 티켓**: **확인 안 됨**.
  - `시술사용후환불.har` 의 마지막 시술권 조회는 `#36`(환불 시작 #45 전)이다.
  - `시술권2.har` 는 다른 고객(고객 1)이고, 그 고객이 환불한 구매(C · F)는 선불카드 상품이라 시술권이 없다(아래).
  - 필요한 HAR: 구매 H 고객의 환불 뒤 시술권 탭 1회.
- **`시술권2.har` 시점**: 05:22:07. **환불1 · 환불2 뒤**이고(환불2 끝 05:21:07), `시술사용후환불`(07:17)보다 **앞**이다. `#19 ticket/v1/queries/get-ticket-bundles{visitorId, sort}` 표는 아래와 같다.

| 번들(옵션) | 구매 | 세트 | 세트 unit | 티켓 | 상태 | 티켓 가격 |
|---|---|---|---|---|---|---|
| 승모근보톡스100 | 구매 G(카드 5 결제) | 바디보톡스 하이톡스 100unit | UNIT 100 | 1 | AVAILABLE | 440,000 |
| 승모근보톡스100 | 구매 E(카드 4 결제) | 바디보톡스 하이톡스 100unit | UNIT 100 | 1 | AVAILABLE | 440,000 |
| 쥬베룩 1cc | 구매 A | 쥬베룩 | — | 1 | AVAILABLE | 11,000 |
| 쥬베룩 1cc | 구매 A | 쥬베룩 | — | 1 | AVAILABLE | 11,000 |
| 백옥주사 | 구매 A | 백옥주사 | — | 1 | AVAILABLE | 33,000 |
| 승모근보톡스100 | 구매 A | 바디보톡스 하이톡스 1000unit | UNIT 1000 | 1 | AVAILABLE | 4,400,000 |
| 크라이오 진정관리 5회 | 구매 B | 크라이오 진정관리 | — | 5 | AVAILABLE ×5 | 65,780 ×5 |
| 쥬베룩 1cc ×3 · 승모근보톡스100 · [FACE] 셀레스텔라 1CC | 이전 구매 5건 | 각 1 세트 | 셀레스텔라 CC 1 · 보톡스 UNIT 100 | 각 1 | IN_USE ×5 | 11,000 · 440,000 · 165,000 |

- **선불카드 상품 구매(C · D · F)는 시술권 번들을 만들지 않는다**. 일정 상세 `purchaseIds` 7건 중 C · D · F 는 번들 목록에 0건이다. 2차 「구매 C 항목이 시술권을 만드나」는 **닫힘(안 만든다)**.
- **카드 5 가 환불됐어도 그 카드로 결제한 구매 G 는 그대로다**. `ACCEPTED/NOT_IN_PROCESS` · 거래 `PREPAID_CARD` 440,000 `APPROVED` 1건 · 티켓 `AVAILABLE`(`시술권2.har#19 · #30`).
- 같은 HAR 에서 본 것:
  - `#5 get-schedule-detail` 의 `purchaseIds` 는 7건이다[B, A, C, D, E, F, G](등록 순서). `tasks` 0건이다.
  - `#4 get-payment-required-tasks{visitorId}` 는 `data[]` 0건이다.

## S5 선불카드 상품 환불 — `환불1.har` · `환불2.har` · `시술권2.har`

### 카드 3(구매 C · 전액 환불 · `REFUNDED`)

| 시점 | 카드 3 금액(잔액/총) | 포인트(잔액/총) | `updatedDateTimeUtc` | 근거 |
|---|---|---|---|---|
| 환불 전 | 500,000 / 500,000 | 50,000 / 50,000 | 05:03:21(구매 C 확정) | `환불2.har#11` |
| 취소 거래 뒤 · complete 전 | 같음 | 같음 | 같음 | `#41`(변화 없음) |
| **complete 뒤** | **0 / 0** | **0 / 0** | 05:19:20.901(complete 05:19:20.703 직후) | `#71` |
| 1분 뒤 · `available:true` 조회 | **목록에 없음** | — | — | `시술권2.har#16` |

- **카드를 비운다.** 잔액뿐 아니라 **총액(`total`)도 0** 이 된다. 포인트(보너스)도 같이 0 이 된다.
- **카드 행은 남는다**:
  - `available` 없이 조회하면 0/0 으로 계속 나온다(`환불2.har#71~#177`).
  - `available:true` 로 조회하면 빠진다(`시술권2.har#16` — 요청 body 에 `available:true`. 2차까지의 조회엔 이 키가 없었다).
  - 카드 응답 키 10개(`id · title · remainingBalance · remainingPoint · expirationDateTimeUtc · createdDateTimeUtc · ownerId · description · translsMap · updatedDateTimeUtc`)에 **상태 · 삭제 칸은 없다**.
  - 삭제됐다는 신호는 없고, 「0 이 되어 사용 가능 목록에서 빠짐」이다.
- 취소(2차)와 다르다. 현금 취소만 했을 땐 카드가 그대로 남았다. **`complete-purchase-refund` 가 카드를 비운다**(시각으로 본 것 · 명령 응답 `{}`).

### 카드 5(구매 F · 부분 환불 · 440,000 남김)

| 시점 | 카드 5 금액 | 포인트 | 근거 |
|---|---|---|---|
| 구매 F 확정 직후 | 500,000 / 500,000 | (첫 조회엔 포인트 키 없음 → 다음 조회에 50,000 / 50,000) | `환불2.har#80` · `#106` |
| 구매 G 를 카드 5 로 결제 뒤 | **60,000** / 500,000 | 50,000 / 50,000 | `#117` |
| 환불 진행 중(`REFUNDING` · complete 전) | 60,000 / 500,000 그대로 | 50,000 / 50,000 그대로 | `#136 · #166 · #171 · #177` |
| complete 뒤(HAR 밖) · `available:true` | **목록에 없음** | — | `시술권2.har#16` |

- 고객 합계(`시술권2.har#17 get-visitor-prepaid-card-balance`)는 다음과 같다.
  - 금액: 29,560,000 / 30,000,000 = 카드 4 하나뿐
  - 포인트: 15,555,000 / 20,010,000 = 카드 1 · 2 · 4 합
  - 카드 3 · 5 는 합계에 들어가지 않는다. 카드 5 가 0 이 됐는지 목록에서만 빠졌는지는 **확인 안 됨**이다(`available` 없는 조회가 그 뒤 없음).
- **충전 · 사용 이벤트**: 환불 HAR 들에 `get-prepaid-card-charging-events` 호출이 **없다**. 환불이 이벤트를 남기는지(회수 · 차감 이벤트), 그 `type` 값이 무엇인지는 **확인 안 됨**이다.
- **`REFUNDING` 으로 끝난 구매** = **구매 F**(선불카드 상품 「비공개 멤버십1」 · 카드 5). HAR 녹화가 complete 전에 끝났다. `시술권2.har` 에서는 `PARTIALLY_REFUNDED` · 항목 `adjustedPrice` 440,000 이다.
- **사용자 의견 「취소하면 카드도 소프트 딜리트 · 취소 이력」에 대해 KOS 가 실제로 하는 것**:
  - 현금 **취소**(2차): 카드를 건드리지 않는다.
  - **환불 완료**: 카드 금액 · 포인트의 잔액과 총액을 **0 으로 만들고 행은 남긴다**. 사용 가능 목록(`available:true`)에서 빠진다.
  - 카드에 삭제 · 상태 칸은 없다.
  - 「이력」으로 남는 것은 구매 쪽뿐이다: 구매 상태 `REFUNDED`/`PARTIALLY_REFUNDED` · 음수 거래 · 항목 `adjustedPrice`. 카드 이벤트 쪽은 확인 안 됨이다.

### 구매 D(카드 4) — 기록만

- 구매 D(「VIP 플랜3」 30,000,000 · 05:12:25 생성)의 거래는 5건이다. +30,000,000 / −30,000,000(취소) / +30,000,000 / **+440,000** / +30,000,000 이고, 합계는 **60,440,000** 이다.
- 그런데 상태는 `ACCEPTED/NOT_IN_PROCESS` 이고 카드 4 총액은 30,000,000 이다(`환불2.har#0` · `시술권2.har#30`).
- 이 거래들은 이번 HAR 들보다 앞에 생겼고, 만든 명령은 HAR 에 없다. **KOS 는 거래 합계가 항목 금액을 넘어도 막지 않는다**는 표본으로만 적는다.

## S6 선불카드 공유 — `선불카드공유.har`

| # | 경로 | 요청 | 응답 |
|---|---|---|---|
| 2 | `visitor/v2/queries/get-visitors` | `{indexOfPage, countInPage:20, visitorName, phoneNumber, chartNumber, sort{by:"lastVisitedDateTimeUtc", order:"DESC"}}` | `{data[20], count}` — 고객 찾기(공유할 고객 선택) |
| 5 | **`purchase/prepaid-card/v1/commands/add-visitor-to-prepaid-card`** | **`{id(카드 id), visitorId}`** | `{}` |
| 6 | `purchase/prepaid-card/v1/queries/get-prepaid-card-visitors` | `{id}` | `data[2]` 아래 |

- 대상 카드 = 카드 4(「VIP 플랜3」 · 소유 고객 1)다. 카드 id 는 UUID 꼴이다(구매 · 고객 id 는 24자리 hex).
- **목록 응답**:
  - 추가 **뒤**(#6): 2건 `[{visitorId(고객 1), name, chartNumber, owner: true}, {visitorId(추가한 고객), name, chartNumber, owner: false}]`.
  - 추가 **전** 목록은 이 HAR 에 없다. 2차(`선불카드생성.har#7 · #16 · #19`, 카드 1 · 2)에서는 늘 1건 · `owner: true` 였다.
  - **`owner: false` = 공유 고객**이다(2차 「뜻 확인 안 됨」 → **닫힘**).
- `owner` 는 카드 목록(`get-prepaid-card-summaries`)의 `ownerId` 와 같은 고객이다. 공유 뒤에도 `ownerId` 는 고객 1 그대로다(`환불2.har#11`).
- **공유 고객이 카드를 쓸 때 이력**: HAR 에 **없다**.
  - 공유 뒤 카드 4 로 결제한 구매 E(05:14:43)는 **소유자(고객 1)** 의 구매다(`시술권2.har#27` 구매 E `visitorId` = 고객 1).
  - 이벤트 조회(`get-prepaid-card-charging-events`)도 이 HAR 엔 없다.
  - 2차에서 본 이벤트 `visitor{visitorId, name, chartNumber, owner}` 칸이 「누가 썼나」 자리로 보인다. 공유 고객 값이 실제로 들어가는지는 **확인 안 됨**이다.
- **제거 명령**: HAR 에 **없다**(`remove-visitor` grep 0건).
- 추가 뒤 화면은 고객 1 의 일정 · 구매 조회로 돌아간다(#12~#26). 공유 고객 쪽 카드 목록(그 고객의 `get-prepaid-card-summaries` 에 카드 4 가 보이는지)도 **확인 안 됨**이다.

## S7 초안 대조 — `erd-draft.md`

### 7-1. 담을 칸 없음

| # | 값 | 근거 | 담을 곳 후보 | 지금 초안 |
|---|---|---|---|---|
| 1 | 구매 상태 `REFUNDED` · `PARTIALLY_REFUNDED` · 진행 `REFUNDING` | S1 | `purchase.status` · `purchase.process` | 결정 2 는 「INITIALIZED · ACCEPTED …」만 적고 값 목록이 없음 |
| 2 | 진행 중 환불 대상 `refundingItems[{targetItemId, adjustedPrice(분해)}]` | S1 | `purchase_item` 또는 환불 테이블 | 칸 없음 · 결정 2 「항목 상태 칸 안 둔다 · 환불이 항목 단위면 그때 더한다」 |
| 3 | 완료 뒤 항목 `adjustedPrice` · `adjustPriceV2`(공급 · 면세 · 부가세 · 과세) | S1 · S2 | `purchase_item` 조정 금액 칸 | 결정 9 (b) 「`purchase_item` 조정 금액으로 남긴다」 — **칸 이름 · 분해 칸 미정의** |
| 4 | 환불 시작 · 완료 시각 | 구매 `lastUpdatedDateTimeUtc` 만 있음 | — | KOS 도 따로 안 줌 · 기록만 |
| 5 | 작업 `ticketConfiguration{ticketId, round{total, current}}` | S3 | `visit_task.ticket_id` · `ticket_round_current/total` | **결정 3 과 맞음**(칸 이미 있음) — 값 출처 확인만 |
| 6 | 카드 공유 `{카드, 고객, owner}` | S6 | `prepaid_card_customer` | 결정 6 추가분과 맞음. `owner` 는 `prepaid_card.customer_id` 로 갈음 |
| 7 | 카드 조회 필터 `available`(0 인 카드 숨김) | S5 | (파생 · 잔액 0) | 기록만 |
| 8 | 카드 「총액(total)」 이 환불로 0 이 됨 | S5 | `prepaid_card` 두 주머니(잔액 · 총액?) | 결정 5 「두 주머니 칸」 — 총액 칸을 둘지 미정 |

### 7-2. 「정한 것」과 어긋나거나 새로 드러난 것

| | 정한 것 | 실제 KOS | 근거 |
|---|---|---|---|
| A | 결정 1 「결제 완료 = 상태 + 거래 합계」 | 환불 뒤에는 거래 합계가 항목 `price` 가 아니라 **`adjustedPrice` 와 같다**(세 구매 모두). 비교 기준이 항목 금액 → 조정 금액으로 바뀐다. 구매 D 처럼 합계가 금액을 **넘는** 확정 구매도 있다 | S1 · S5 구매 D |
| B | 결정 2 「상태는 구매에 · 항목 상태 칸 없음」 | 환불은 **항목을 지정**한다(`targetItemId`). 다만 표본 3건 모두 항목 1개짜리 구매라, 여러 항목 중 일부만 환불되는 모양은 못 봤다. 결과 상태(`PARTIALLY_REFUNDED`)는 구매에 있다 | S1 |
| C | 결정 2 「취소 · 환불이 항목 단위면(`revokingItems` · `refundingItems`) 그때 더한다 — 환불 HAR 1건 필요」 | 환불 HAR 이 왔다. `refundingItems` 는 **진행 중에만** 있고 완료되면 항목의 `adjustedPrice` 로 옮겨진다. `revokingItems` 는 여전히 0 | S1 |
| D | 결정 9 (b) 「번들 가격 ÷ 회차 × 쓴 횟수」 | 1회권 · 단일 세트 다회권은 값이 KOS 티켓 가격 합과 같다(65,780). 단 초안 134줄의 **묶음 옵션**(울쎄라+써마지 165,000 → 세트별 73,333 / 91,667)은 「÷ 회차」가 세트마다 달라서 공식이 정해지지 않는다(표본 없음). **선불카드 상품**은 회차가 아니라 「쓴 금액」(440,000)이 남는 금액이다 | S2 · S5 |
| E | 결정 9 「직원이 금액을 고칠 수 있는지 미확인」 | HAR 에서도 미확인 — 수정 이벤트 없음 · 공식값 그대로 | S2 |
| F | 2차 C(선불카드 상품 취소해도 카드 남음) | **환불 완료는 카드를 0 으로 만든다**(금액 · 포인트 · 총액). 행은 남고 사용 가능 목록에서 빠진다. 취소 ≠ 환불 | S5 |
| G | 그림 `ticket |o--o| visit_task` · 결정 3 | KOS 도 작업이 티켓 1장을 가리킨다(`ticketId`). 완료 뒤 `USED`. 맞음 | S3 |
| H | 결정 6 추가(공유 고객 · 소유자는 `prepaid_card.customer_id`) | KOS 목록은 소유자를 **같은 목록 안 `owner:true`** 로 준다. 초안처럼 「소유자는 카드에 · 공유자만 연결 테이블」로 받으면 동기화 때 `owner:true` 행을 거르면 된다. 어긋남 없음 | S6 |
| I | 선불카드 상품 → 시술권 | 선불카드 상품 구매는 시술권을 안 만든다. 그림 `purchase_item ||--o| ticket_bundle` 의 `o`(0 개) 쪽 | S4 |

### 7-3. 정할 것(결정하지 않음)

1. **구매 상태값 목록**(7-1 #1): `REFUNDED` · `PARTIALLY_REFUNDED` · 진행 `REFUNDING` 을 `purchase.status` · `process` 값으로 받을지. DAY 가 원천일 때 환불 진행 상태(`REFUNDING`)를 둘지, 완료 상태만 둘지.
2. **조정 금액 칸**(7-1 #3 · 결정 9 (b)): `purchase_item` 에 둘 칸이 금액 하나인지, 공급 · 면세 · 부가세 분해까지인지. 이름(KOS 는 `adjustedPrice` · `adjustPriceV2` 두 키).
3. **환불 진행 중 표시**(7-1 #2): `refundingItems` 처럼 「환불 대상으로 표시된 항목」을 칸으로 둘지(항목 플래그 · 별도 테이블), 완료 결과만 둘지.
4. **결제 완료 계산 기준**(A): 환불된 구매에서 「거래 합계」를 무엇과 비교할지(조정 금액 있으면 조정 금액). 거래 합계 > 금액인 구매를 어떻게 볼지.
5. **부분 환불 공식의 적용 범위**(D): 묶음 옵션(세트 여럿) · 선불카드 상품(쓴 금액)에서 어떤 공식을 쓸지. 직원 수정을 허용할지.
6. **선불카드 상품 환불 시 카드**(F · 사용자 의견): KOS 는 0 으로 만들고 행을 남긴다(삭제 칸 없음). DAY 가 소프트 딜리트로 할지, 0 + 이력(ledger 회수 이벤트)으로 할지. 취소(카드 남음)와 환불(카드 비움)을 다르게 둘지.
7. **카드 총액 칸**(7-1 #8): 결정 5 「두 주머니」에 잔액만 둘지, 총액(충전 누계)도 둘지. 환불 때 총액도 0 이 되는 KOS 동작을 따를지.
8. **환불된 카드로 이미 결제한 구매**(S4 구매 G): 카드가 비워져도 그 카드로 낸 거래는 그대로다. DAY 에서 그 거래의 `prepaid_card_id` 참조를 어떻게 둘지(카드 소프트 딜리트를 고르면 참조 무결성 문제).

## 2차 「확인 안 됨」 표 — 줄마다

| 2차 줄 | 판정 | 근거 |
|---|---|---|
| 다회권 `round`(current/total) 값 | **닫힘** — `{total:5, current:1}` · 작업 추가 명령 요청에 있음 | S3 |
| 티켓 가격 나머지 처리 | 여전히 확인 안 됨(표본 모두 나누어떨어짐) | — |
| 「취소만 된」 구매의 티켓 | 여전히 확인 안 됨 | — |
| `revokingItems` · `refundingItems` | **반 닫힘** — `refundingItems` 모양 · 수명 확인 / `revokingItems` 여전히 0 | S1 |
| 선불카드로 낸 결제 취소 → 잔액 · 이벤트 | 여전히 확인 안 됨(이번엔 카드 **상품** 환불만) | — |
| 금액 충전 이벤트 `amount.type` · 상품 구매 취소 뒤 이벤트 | 여전히 확인 안 됨(이벤트 조회 없음) | — |
| 구매 C 항목이 시술권을 만드나 | **닫힘** — 안 만든다 | S4 |
| 카드 고객 2명 이상 · `owner = false` | **닫힘** — 공유 고객 = `owner:false` | S6 |
| 거래 수단별 설정 안쪽 키 | 여전히 확인 안 됨(이번 HAR 모두 CASH · PREPAID_CARD) | — |

## 여전히 확인 안 됨 — 필요한 HAR

| 질문 | 필요한 HAR |
|---|---|
| 환불 뒤 시술권(남은 4장 · 쓴 1장) 상태 | `시술사용후환불` 고객(구매 H)의 **환불 뒤 시술권 탭** 1회 |
| 작업 추가 때 티켓이 `IN_USE` 가 되는지 | 다회권 티켓으로 작업 추가 직후 · 완료 전 시술권 탭 1회 |
| 환불이 카드 이벤트를 남기나(회수 · 차감 `type`) · 금액 충전 이벤트 `amount.type` | 카드 3 또는 카드 5 상세(충전 이벤트) 1회 |
| 카드 5 가 0 이 됐나 · 목록에서만 빠졌나 | 고객 1 선불카드 목록(`available` 없이 · 「사용 완료」 포함 보기가 화면에 있다면) 1회 |
| 공유 고객이 카드를 쓸 때 이력 · 공유 고객 쪽 카드 목록 | 공유 고객으로 카드 4 결제 1회 + 카드 4 상세(충전 이벤트) + 그 고객 선불카드 목록 |
| 공유 고객 제거 명령 | 카드 상세에서 [제거] 1회 |
| `revokingItems` 의 뜻 | 확정 구매에서 항목 하나만 빼기(화면에 있다면) |
| 여러 항목 구매의 일부 항목 환불 · 묶음 옵션 부분 환불 금액 | 항목 2개 이상 구매에서 1개만 환불 · 울쎄라+써마지 같은 묶음 옵션 1회 사용 뒤 환불 |
| 환불 금액을 직원이 고칠 수 있나 | 환불 화면에서 금액을 고쳐 완료 1회 |
| 선불카드로 낸 결제 취소 → 잔액 · 이벤트 | 구매 G 같은 PREPAID_CARD 거래 취소 1회 + 그 카드 상세 |
| 「취소만 된」 구매의 티켓 · 티켓 가격 나머지 | 2차 표 그대로 |
| 구매 상태 · 진행 값 전체 목록 | (HAR 로는 어려움 — KOS 화면 필터 목록이 있다면 그 조회 1회) |

## 개인정보 점검

```text
grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9]{6}-?[1-4][0-9]{6}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|Bearer|[0-9a-f]{24}|[0-9a-f]{8}-[0-9a-f]{4}-' har-check-report-3.md
```

점검 결과(2026-11-18): 일치 **1줄 — 위 grep 명령 줄 자신**(패턴 문자열의 `Bearer`). 그 밖 전화번호 · 주민번호 꼴 · 이메일 · `Bearer` · 24자리 hex · UUID **0건**. HAR 에서 본 고객 이름 · 차트번호 · 직원 이름 · 화면 제목 문자열 직접 grep → 0건. 상품 이름은 메뉴 이름만(「비공개 멤버십1」 · 「VIP 플랜3」 · 옵션 이름).
