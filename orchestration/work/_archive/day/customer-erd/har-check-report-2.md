# HAR 확인 리포트 2차 — 시술권 행 수 · 선불카드 충전/이력/취소

- 작성: day `researcher` · 2026-11-18 · task `task_dc92af7249f3`
- 앞 리포트: `har-check-report.md`(1차) 「확인 안 됨 — 필요한 HAR」 표의 줄마다 닫힘 여부를 적는다. 형식 · 근거 표기 · 금지 규칙은 1차와 같다.
- 입력: 새 HAR 4개(`고객정보.har` · `선불카드생성.har` · `선불카드결제.har` · `선불카드결제취소.har`). `python3 -I` 로 읽음. KOS 호출 0.
- 근거 표기: `파일.har#N` = `log.entries[N]`. 경로는 `/tenants/<id>/` 뒤만. id 값 · 이름 · 차트번호 · 메모 · 카드 제목은 옮기지 않았다.
- 구매 이름은 1차와 같다 — **구매 A**(쥬베룩 1cc ×2 · 백옥주사 · 승모근보톡스100 → 1000, 선불카드 결제) · **구매 B**(크라이오 진정관리 5회, 현금 → 취소 → 재결제). 새로 **구매 C**(선불카드 상품 「비공개 멤버십1」 현금 결제 → 취소).

## 0. 네 HAR 의 관계

| 시각(UTC) | HAR | 한 일 |
|---|---|---|
| ~05:00 | `고객정보.har` | 고객 상세 — 시술권 탭(`get-ticket-bundles` #26) · 선불카드(#23 · #24) · 일정 상세(#12) |
| 05:01:53 | `선불카드생성.har` | 선불카드 하나 더 생성(포인트 10,000 · 금액 0) + 카드 상세(충전 이벤트 · 카드 고객) |
| 05:03:21 | `선불카드결제.har` | 선불카드 **상품** 을 구매 C 로 담아 현금 결제 → 확정 |
| 05:03:49 | `선불카드결제취소.har` | **`#0~#56` 이 `선불카드결제.har` 57건과 요청 URL · body 가 모두 같다**(앞부분 포함) → `#76` 구매 C 현금 거래 취소 |

근거: 두 HAR 의 entries 앞 57건 요청 URL · postData 대조(57/57 같음).

---

## 1차 「확인 안 됨」 표 — 줄마다

| 1차 줄 | 판정 | 답(요약) | 근거 |
|---|---|---|---|
| Q1 티켓 행 수 · 가격 나누기 · 구매 직후 상태 | **닫힘** | 5회권 = 번들 1 → 세트 1 → **티켓 5행** · 티켓마다 65,780 · 합 328,900 = 번들 가격(나머지 0) · 전부 `AVAILABLE` | R1 |
| Q1 round 의 다회권 값 | **여전히 확인 안 됨** | 일정 상세의 `tasks` 가 0건이라 `ticketConfiguration` 이 없다 | R1 |
| Q2 취소된 구매의 시술권 | **닫힘(조건부)** | 구매 B 티켓 5장 그대로 `AVAILABLE` · 새 티켓 없음. 다만 HAR 시점엔 재결제까지 끝나 있어 「취소만 된 상태」의 티켓은 못 봤다 | R2 |
| Q2 `revokingItems` · `refundingItems` | **여전히 확인 안 됨** | 구매 C 취소 뒤에도 0 · 0 | R6 |
| Q2 일정 `purchaseIds[]` | **닫힘** | 일정 상세에 `purchaseIds` 있음 — [구매 B, 구매 A] 2건 | R8 |
| Q3 금액 충전 | **닫힘** | 선불카드 **상품** 을 구매 항목(`type = PREPAID_CARD_PRODUCT`)으로 사서 결제하면, 확정 때 카드가 만들어지고 금액 · 포인트가 같이 들어간다 | R5 |
| Q3 이력 | **닫힘** | `get-prepaid-card-charging-events` — 카드별 이벤트 목록(`CHARGE` · `PAYMENT`). 거래의 `chargingId` = `PAYMENT` 이벤트의 `chargingId` | R4 |
| Q3 선불카드 결제 취소 | **여전히 확인 안 됨** | 이번 취소는 「선불카드 상품을 현금으로 산 거래」의 취소다. **선불카드로 낸 결제(PREPAID_CARD 거래)의 취소는 표본 없음** | R6 |
| Q4 시술권 쪽 용량 | **닫힘** | 구매 A 의 항목 4개 = 번들 4개(쥬베룩 2행 → 번들 2개). 보톡스 세트 제목 「바디보톡스 하이톡스 1000unit」 · 세트 `unit = {UNIT, 1000}` · 4,400,000 | R3 |
| 거래 수단별 설정 안쪽 키 | **여전히 확인 안 됨** | 새 HAR 도 CASH · PREPAID_CARD 뿐 | 전 HAR 거래 |

---

## R1 다회권 티켓 — `고객정보.har#26`

경로 `ticket/v1/queries/get-ticket-bundles` · 요청 `{visitorId, sort{by: "ticket.createdDateTimeUtc", order: 2}}` · 응답 번들 10개.

번들 키: `purchaseId · purchaseItemId · optionConfiguration{optionId, optionTitle, productTitle, promotionConfiguration, translsMap} · ticketSets[] · title · price · visitorId · translsMap`
세트 키(1차와 같음): `procedure · unit · tickets[] · title · ticketGroupId · medicalService · translsMap` · 티켓 키: `id · status · price · createdDateTimeUtc`

| 번들(= 옵션 이름) | 구매 | 세트 제목 | 세트 `unit` | 티켓 수 | 티켓 가격 | 합 | 상태 |
|---|---|---|---|---|---|---|---|
| 크라이오 진정관리 5회 | B | 크라이오 진정관리 | `{}` | **5** | 65,780 ×5 | 328,900 | AVAILABLE ×5 |

- **10회권이면 10행인가 → KOS 도 회차마다 티켓 1행이다**(5회권 = 5행). 「1행 + 남은 횟수」 칸은 없다.
- **가격** = 번들 가격 ÷ 회차. 이번 표본은 나누어떨어져 나머지 0. **안 나누어떨어질 때의 나머지 처리는 확인 안 됨**(표본 없음).
- **구매 직후 상태 = `AVAILABLE`**. 티켓 `createdDateTimeUtc` ≈ 결제 · 확정 시각(구매 B 04:42:35 = 1차 `다회권구매.har#22` 승인 04:42:35 · 구매 A 04:44:20 ≈ 1차 `선불카드 결제.har#7` 승인 04:44:19.9 직후 확정). 확정(accept) 때 티켓이 생긴다고 **보인다**(명령 응답 `{}` 라 직접 증거는 시각뿐).
- 상태값: 이번 HAR 은 `AVAILABLE`(구매 A·B 의 9장) · `IN_USE`(이전 구매 5장). 1차 HAR 의 `USED` 와 합쳐 **`AVAILABLE · IN_USE · USED`** 3개.
- **`ticketConfiguration.round`** — 일정 상세(`고객정보.har#12`)의 `tasks` 가 **0건** → **여전히 확인 안 됨**. 필요한 HAR: 이 5회권으로 **작업을 하나 만든 뒤** 일정 상세(`get-schedule-detail`) 1회.

## R2 결제 취소된 구매의 시술권(구매 B) — `고객정보.har#26`

- 구매 B 번들 1개 · 티켓 **5장 그대로 · 전부 `AVAILABLE`** · 티켓 생성 시각은 첫 결제 승인 시각 그대로.
- 재결제(1차 `재결제.har#38`, 04:45:17) 때 **티켓이 새로 생기지 않았다**(구매 B 티켓 5장뿐 · 생성 시각 1개).
- 한계: 이 HAR 은 재결제 **뒤** 상태라, 「취소만 되고 재결제 전」 에 티켓이 잠시 바뀌었다가 돌아왔는지는 못 본다. 확인하려면 **현금 취소 직후 · 재결제 전** 시술권 탭 1회가 필요.

## R3 용량 변경 구매의 시술권(구매 A) — `고객정보.har#26`

| 번들(옵션 이름) | 세트 제목 | 세트 `unit` | 세트 `medicalService.configuration.unit` | 티켓 | 가격 | 상태 |
|---|---|---|---|---|---|---|
| 쥬베룩 1cc | 쥬베룩 | `{}` | 없음 | 1 | 11,000 | AVAILABLE |
| 쥬베룩 1cc | 쥬베룩 | `{}` | 없음 | 1 | 11,000 | AVAILABLE |
| 백옥주사 | 백옥주사 | `{}` | 없음 | 1 | 33,000 | AVAILABLE |
| 승모근보톡스100 | **바디보톡스 하이톡스 1000unit** | **`{UNIT, 1000}`** | `{UNIT, 100}` | 1 | **4,400,000** | AVAILABLE |

- **번들 = 구매 항목 1개.** 쥬베룩 2행 → 번들 2개(각 `purchaseItemId` 가 1차의 두 항목 id 와 같다).
- 번들 `title` · `optionConfiguration.optionTitle` = **원래 옵션 이름**(「승모근보톡스100」 그대로).
- **세트 쪽에 바뀐 용량이 남는다** — 세트 `unit = 1000`, 세트 `title` = 진료항목 이름 + 바뀐 용량(「…1000unit」). 진료항목 기본 단위(100)는 `medicalService.configuration.unit` 에 그대로.
- 비교: 같은 화면의 이전 구매 「승모근보톡스100」(용량 안 바꿈) 세트는 「바디보톡스 하이톡스 100unit」 · `unit = 100` · 440,000. → 1차 단서(「올리디아 120 1CC」 번들 · 「…4cc」 세트)와 같은 모양.
- 티켓 가격 = 바뀐 가격(4,400,000).

## R4 선불카드 충전 이력 — `선불카드생성.har`

### 경로

| # | 경로 | 요청 | 응답 |
|---|---|---|---|
| 4 | `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | visitorId | `data{remainingBalance{balance,total}, remainingPoint{balance,total}, lastPointChargedDateTimeUtc}` — 1차(`고객상세.har#39`)에 없던 `last…ChargedDateTimeUtc` 가 붙는다(값이 있을 때만으로 보임) |
| 5 · 14 | `get-prepaid-card-summaries` | visitorId | 1차와 같음 |
| 6 · 15 · 18 | **`get-prepaid-card-charging-events`** | **`id`(카드 id)** | 아래 |
| 7 · 16 · 19 | **`get-prepaid-card-visitors`** | `id`(카드 id) | R7 |
| 13 | `create-prepaid-card` | 1차와 같은 키(`chargingMemo` 는 이번엔 빠짐) | `{}` |

### `get-prepaid-card-charging-events` 응답 `data[]`

```text
type                     — 본 값: CHARGE · PAYMENT
createdDateTimeUtc
visitor{visitorId, name, chartNumber, owner(bool)}
amount{type, amount{value, currency}}   — amount.type 본 값: POINT (PAYMENT 은 음수)
chargingId(str)
memo(str)
```

- 카드 1(1차에서 만든 카드): 이벤트 2건 — `CHARGE` POINT +10,000,000 → `PAYMENT` POINT **-4,455,000**. 카드 2(이번 생성): `CHARGE` POINT +10,000 1건.
- **`chargingId` 는 이벤트 id 다** — 1차 `선불카드 결제.har#7` 거래의 `prepaidCardConfiguration.chargingId` = 카드 1의 `PAYMENT` 이벤트 `chargingId`(값 대조 일치). 카드 id(`prepaidCardId`)와는 다르다.
- **충전 · 사용은 각각 이벤트로 남는다**(CHARGE · PAYMENT). 1차의 현금 취소 · 재결제(구매 B)는 카드와 무관해서 이벤트가 없다.
- **취소 이벤트**: 표본 없음 — 확인 안 됨(R6).
- 금액(BALANCE) 충전 이벤트의 `amount.type` 값: 구매 C 카드의 이벤트를 조회한 HAR 이 없다(`선불카드결제.har#49` 는 카드 1 조회) → **확인 안 됨**. 필요한 HAR: 구매 C 로 생긴 카드의 상세(충전 이벤트) 1회.

## R5 선불카드 상품 결제 — `선불카드결제.har`

### 선불카드 상품 메뉴 — `#16 procedure-menu/prepaid-card-product/v1/queries/get-prepaid-card-product`

- 요청 `{closed: false}` · 응답 `data[]` 8개. 키: `id · title · price{value,currency} · balance{…} · point{…} · closed(bool) · expirationDurationInDays(int) · translsMap · order(int) · description`
- **메뉴에 선불카드 상품이 따로 있다**(시술 상품 `product-options` 와 다른 경로 `procedure-menu/prepaid-card-product`).

| order | 상품 이름 | 가격 | 금액(balance) | 포인트(point) | 유효(일) |
|---|---|---|---|---|---|
| 0 | 비공개 멤버십1 | 500,000 | 500,000 | 50,000 | 365 |
| 1 | 비공개 멤버십2 | 1,000,000 | 1,000,000 | 100,000 | 365 |
| 2 | 비공개 멤버십3 | 2,000,000 | 2,000,000 | 200,000 | 365 |
| 3 | 비공개 멤버십4 | 3,000,000 | 3,000,000 | 300,000 | 365 |
| 4 | 프리미엄 플랜 | 5,000,000 | 5,000,000 | 500,000 | 365 |
| 5 | VIP 플랜1 | 10,000,000 | 10,000,000 | 2,000,000 | 365 |
| 6 | VIP 플랜2 | 20,000,000 | 20,000,000 | 5,000,000 | 365 |
| 7 | VIP 플랜3 | 30,000,000 | 30,000,000 | 10,000,000 | 365 |

(전부 `closed = false` · 가격 = 금액 · 포인트는 덤.)

### 결제 흐름(명령)

| # | 명령 | 요점 |
|---|---|---|
| 20 | `initialize-purchase` | 새 구매 C |
| 21 | `add-pending-purchase-items` | 항목 1개 · **`type = PREPAID_CARD_PRODUCT`** · `optionConfiguration` 없음 · 대신 **`prepaidCardConfiguration{id(상품 id), title, price, balance, point, expirationDateTimeUtc, expirationDurationInDays, prepaidCardId(만들 카드 id — 화면이 미리 정함), description, translsMap}`** · `price` · `priceV2`(500,000 · 공급 454,546 · 부가세 45,454 · `TAXABLE`) · `basePrice` 같음 |
| 23 | `register-purchase` | 일정에 구매 C 연결 |
| 41 | `add-transaction` | CASH 500,000 APPROVED |
| 42 | `accept-purchase` | 확정 |

- **금액 충전은 구매 · 구매 항목을 만든다** — 항목 `type` 의 두 번째 값 `PREPAID_CARD_PRODUCT` 확인(1차는 `PRODUCT_OPTION` 뿐).
- **카드는 확정 때 생긴다** — `create-prepaid-card` 명령 없이, 확정 뒤 `get-prepaid-card-summaries`(#48)에 카드 3이 나타난다. 카드 id = 항목의 `prepaidCardConfiguration.prepaidCardId`(값 일치) · 생성 05:03:21.509(accept 직후).
- 결제 뒤 카드 3: **금액 500,000/500,000 · 포인트 50,000/50,000** · `description` 있음. 고객 합계(#47): 금액 0 → 500,000 · 포인트 5,605,000 · total 10,060,000(= 카드 1 · 2 의 5,545,000 + 10,000 에 50,000 더함) · `lastBalanceChargedDateTimeUtc` · `lastPointChargedDateTimeUtc` 둘 다 05:03:21.
- 구매 C 상태: `ACCEPTED/NOT_IN_PROCESS` · items 1 · 거래 1(#46).
- 구매 C 항목이 시술권 번들을 만드는지: 시술권 탭을 이 뒤에 연 HAR 없음 — **확인 안 됨**(`고객정보.har` 는 그 전).

## R6 선불카드 상품 결제 취소 — `선불카드결제취소.har`

- 명령 `#76 add-canceled-transaction` — 1차와 같은 모양: CASH **-500,000** · `CANCELED` · `canceledRefId` = 구매 C 의 현금 거래 · 공급 -454,546 · 부가세 -45,454 · `paymentDateTime{approved(원 승인), canceled, lastUpdated}`.
- 취소 뒤 구매 C(#77 · #84): `ACCEPTED/NOT_IN_PROCESS` 그대로 · 항목 1 그대로 · `revokingItems` 0 · `refundingItems` 0 · 거래 2(APPROVED +500,000 / CANCELED -500,000).
- **카드 잔액은 복구(회수)되지 않는다** — 취소 뒤 카드 3: 금액 500,000/500,000 · 포인트 50,000/50,000 · `updatedDateTimeUtc` 05:03:21 그대로(#69 · #70 · #79). 돈은 돌려줬는데 카드 금액은 남아 있는 상태.
- 충전 이벤트 변화: 취소 뒤 `get-prepaid-card-charging-events` 호출 0 → **확인 안 됨**.
- 「선불카드로 낸 결제」(PREPAID_CARD 거래) 취소 시 잔액 복구: 표본 없음 → **확인 안 됨**.

## R7 `get-prepaid-card-visitors` — `선불카드생성.har#7 · #16 · #19`

- 요청 `{id}`(카드 id) · 응답 `data[]{visitorId, name, chartNumber, owner(bool)}`.
- 표본 3회(카드 1 · 카드 2): **모두 1명 · `owner = true`**(소유자 본인). 이름으로 보아 **카드 하나에 고객 여럿이 붙을 수 있는 목록**(카드 공유 · 사용 고객)이고 `owner` 로 소유자를 가른다 — 2명 이상 · `owner = false` 표본이 없어 **뜻은 확인 안 됨**.
- 같은 `{visitorId, name, chartNumber, owner}` 꼴이 `create-prepaid-card` 의 `buyer` 와 충전 이벤트의 `visitor` 에도 있다 → 이벤트마다 「누가 충전 · 사용했나」 를 남기는 모양.
- 사용자 결정 6(선물 · 구매자 ≠ 소유자는 지금 없음)에 대해 판단하지 않는다 — 사실만.

## R8 일정 `purchaseIds[]` — `고객정보.har#12`

- 경로 `schedule/v1/queries/get-schedule-detail` · 요청 `{scheduleId}`.
- 응답 키: `consultation · consultations · createdDateTimeUtc · deleted · etceteraWorks · flowStep · flowStepUpdatedDateTimeUtc · id · occupiedResources · orderMemo · prescriptionIds · purchaseIds · purchases · reactions · receptionDateTimeUtc · reservation · reservationTagIds · taskTimers · tasks · updatedDateTimeUtc · visitor · visitorLocation · zone`
- **`purchaseIds` = 2건 [구매 B, 구매 A]**(등록 순서) · `purchases = []`(빈 배열 — 펼친 구매는 안 줌) · `prescriptionIds = []` · `tasks` 0건.
- 1차 「취소 · 재결제로 일정 연결이 바뀌나」: 재결제 뒤에도 구매 B 가 그대로 1건 → **새 구매 · 연결 변화 없음**.
- (일정 요약 `get-schedule-summaries` 에는 여전히 `purchaseIds` 키 없음 — 일정 **상세** 에만.)
- `#11 schedule/v1/queries/get-payment-required-tasks`(요청 visitorId) 응답 `data[]` 0건 — 이번 고객에 「수납 필요」 작업 없음.

---

## R9 초안 대조 — `erd-draft.md`

### 9-1. 담을 칸 없음(값 · 테이블 후보)

| # | KOS 값 | 본 곳 | 테이블 후보 | 비고 |
|---|---|---|---|---|
| 1 | 선불카드 **상품** 메뉴 `{title, price, balance, point, closed, expirationDurationInDays, order, description, translsMap}` | `선불카드결제.har#16` | 새 메뉴 테이블(예: `prepaid_card_product`) | 초안 메뉴(`product · product_option`)에 없는 별개 메뉴 |
| 2 | 구매 항목 `type = PREPAID_CARD_PRODUCT` + `prepaidCardConfiguration{상품 스냅샷 · prepaidCardId}` | `#21` | `purchase_item` | 초안 `purchase_item` 은 `product_option` 참조 + 스냅샷만. 「선불카드 상품 참조」 · 「만들어진 카드」 칸 없음 |
| 3 | 충전 이벤트 `type`(CHARGE · PAYMENT) · `amount.type`(POINT · 금액 쪽 값 미확인) · 부호 있는 금액 · `memo` · `createdDateTimeUtc` · `visitor` | `선불카드생성.har#6` | `prepaid_card_ledger` | 초안 결정 5(ledger 를 DAY 가 쌓는다)의 칸 정의 없음 |
| 4 | 이벤트 `chargingId` ↔ 거래 `prepaidCardConfiguration.chargingId` | 같은 곳 · 1차 `선불카드 결제.har#7` | `prepaid_card_ledger` ↔ `purchase_transaction` | 초안 그림엔 `purchase_transaction |o--o| prepaid_card_ledger` 관계가 이미 있음 — 칸 이름만 없음 |
| 5 | 카드 고객 목록 `get-prepaid-card-visitors{visitorId, owner}` | `#7` | (없음 · 결정 6 「소유자 하나」) | 표본은 1명 · owner true 만 |
| 6 | 세트 `unit`(바뀐 용량) · 세트 `title` | `고객정보.har#26` | `ticket_set` | 결정 8 은 구매 항목만 언급. 세트도 바뀐 용량을 가진다 |
| 7 | 티켓 가격(회차당 = 번들 ÷ 회차) | 같은 곳 | `ticket` | 초안 `ticket` 칸 미정의 |
| 8 | 일정 상세 `purchaseIds[]` 순서 | `고객정보.har#12` | `purchase.visit_id`(결정 1) | 순서는 칸 없음 — 기록만 |
| 9 | 고객 합계 `lastBalanceChargedDateTimeUtc` · `lastPointChargedDateTimeUtc` | `선불카드결제.har#47` | (파생 — 이벤트에서 계산 가능) | 기록만 |

### 9-2. 「정한 것」 1~9 와 어긋나는 것 · 새로 드러난 것

| # | 정한 것 | HAR 사실 | 근거 |
|---|---|---|---|
| A | 7. 충전 출처 — 2차 HAR 확인 뒤 | **두 길이 있다**: (a) 화면에서 카드 직접 생성(`create-prepaid-card` · 구매 없음 · 이번 표본은 포인트만) (b) 선불카드 상품을 **구매 항목으로 사고 확정** → 카드 자동 생성(금액 + 포인트) | `선불카드생성.har#13` · `선불카드결제.har#21 · #42 · #48` |
| B | 9. 다회권 = DAY 는 ticket N행 · KOS 모양은 2차 HAR 로 | **KOS 도 N행** — 어긋남 없음 | R1 |
| C | 2. 취소 = 음수 거래 · 재결제 = 같은 구매에 거래 추가 | 선불카드 상품 구매 취소도 같은 모양. 다만 **취소해도 카드 잔액이 남는다**(KOS 가 자동 회수 안 함) — 「결제 완료 = 상태 + 거래 합계」(결정 1)로 보면 구매 C 는 미결제인데 카드는 살아 있다 | R6 |
| D | 2. (티켓) | 현금 취소 · 재결제가 **티켓을 지우거나 새로 만들지 않는다**(티켓은 첫 확정 때 1번) | R2 |
| E | 8. 용량 변경 = 구매 항목은 바뀐 값만 | 시술권 **세트** 도 바뀐 단위(`unit`) · 바뀐 이름을 가진다. 번들 이름은 원래 옵션 이름 | R3 |
| F | 6. `prepaid_card.customer_id` = 소유자 하나 | KOS 엔 카드별 고객 **목록**(`get-prepaid-card-visitors` · `owner` 플래그)이 있다. 표본은 소유자 1명뿐 — 충돌 여부 미확인 | R7 |
| G | 4. 결제 수단 · 선불카드만 `prepaid_card_id` FK | 선불카드 결제 거래는 카드 id 외에 **이벤트 id(`chargingId`)** 도 가진다 | R4 |

### 9-3. 정할 것(결정하지 않음)

1. **선불카드 상품 메뉴** — 별도 테이블로 둘지, `product · product_option` 에 종류로 넣을지 (9-1 #1).
2. **구매 항목 종류** — `purchase_item` 에 종류(`PRODUCT_OPTION` · `PREPAID_CARD_PRODUCT`) 칸과 선불카드 상품 참조 · 만들어진 카드(`prepaid_card_id`) 칸을 둘지 (9-1 #2 · A).
3. **충전 출처 두 길** — 직접 생성(구매 없음)과 상품 구매를 둘 다 받을지 · 직접 생성 충전을 ledger 에 어떻게 남길지 (A).
4. **ledger 칸** — 이벤트 종류(충전 · 사용 · 취소 …) · 주머니(금액 · 포인트) · 부호 금액 · 메모 · 시각 · 거래 연결 (9-1 #3 · #4 · G).
5. **선불카드 상품 구매 취소 시 카드** — KOS 처럼 그대로 둘지, DAY 가 회수 이벤트를 남길지 (C).
6. **세트의 바뀐 용량** — `ticket_set` 에 단위 · 이름 스냅샷을 둘지 (E).
7. **티켓 가격 나머지** — 나누어떨어지지 않을 때 규칙(표본 없음) (R1).
8. **카드 고객 목록** — 결정 6 유지 시 KOS `get-prepaid-card-visitors` 의 2명 이상 경우를 어떻게 받을지(동기화 때) (F).

## 여전히 확인 안 됨 — 필요한 HAR

| 질문 | 필요한 HAR |
|---|---|
| 다회권 `round`(current/total) 값 | 크라이오 5회권으로 **작업 1개 만든 뒤** 일정 상세(`get-schedule-detail`) |
| 티켓 가격 나머지 처리 | 나누어떨어지지 않는 다회권(예: 3회권 100,000) 구매 뒤 시술권 탭 |
| 「취소만 된」 구매의 티켓 | 현금 취소 직후 · 재결제 전 시술권 탭 |
| `revokingItems` · `refundingItems` | 확정 구매에서 항목 하나만 취소/환불(화면에 있다면) |
| 선불카드로 낸 결제 취소 → 잔액 · 이벤트 | 구매 A 같은 PREPAID_CARD 거래 취소 1회 + 그 카드 상세(충전 이벤트) |
| 금액 충전 이벤트 `amount.type` · 상품 구매 취소 뒤 이벤트 | 구매 C 로 생긴 카드의 상세(충전 이벤트) 1회 |
| 구매 C 항목이 시술권을 만드나 | 구매 C 뒤 시술권 탭 1회 |
| 카드 고객 2명 이상 · `owner = false` | (결정 6 상 지금 필요 없음 — 기록만) |
| 거래 수단별 설정 안쪽 키 | 카드 · 이체 · 플랫폼 · 간편결제 · 의료대출 결제 각 1회(필요하면) |

※ 카드 3(구매 C) 상세 1회 + 시술권 탭 1회로 두 줄이 같이 닫힌다.

## 개인정보 점검

```text
grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9]{6}-?[1-4][0-9]{6}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|Bearer|[0-9a-f]{24}' har-check-report-2.md
```

점검 결과(2026-11-18): 일치 **1줄 — 위 grep 명령 줄 자신**(패턴 문자열의 `Bearer`). 그 밖 전화번호 · 주민번호 꼴 · 이메일 · `Bearer` · 24자리 hex **0건**. HAR 에서 본 직원 · 고객 이름 · 차트번호 · 카드 제목 · 메모 문자열 직접 grep → 0건.
