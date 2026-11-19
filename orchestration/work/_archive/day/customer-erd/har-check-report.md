# HAR 확인 리포트 — 고객 · 결제 · 시술권 · 선불카드 ERD 초안 v0 의 미확인 4건

- 작성: day `researcher` · 2026-11-18 · task `task_fb11ccb1df0b`
- 대상: `reference/2026-11-18-day-customer/erd-draft.md`(읽기만) 「받을 HAR」 1~4 · 「아직 응답 모양을 못 본 것」
- 입력: `reference/2026-11-18-day-customer/har/` 새 HAR 6개 + 비교 기준 4개. `python3 -I` 로 읽음. KOS 호출 0.
- 근거 표기: `파일.har#N` = HAR `log.entries[N]`(0부터). 경로는 `/tenants/<id>/` 뒤만.
- 개인정보 · 비밀값 · id 값은 옮기지 않았다(id 는 「id(str)」). 직원 이름 · 고객 이름 · 차트번호 · 메모 · 카드 이름도 뺐다.

## 0. 먼저 — 여섯 HAR 은 한 고객 · 한 흐름이다

같은 고객(visitorId 같음) 에서 시간 순서대로 떴다. 구매는 둘뿐이다.

| 순서 | HAR | 한 일 | 구매 A(4항목) | 구매 B(크라이오 5회) |
|---|---|---|---|---|
| 1 | `다회권구매.har` | 크라이오 진정관리 5회 담기 → 현금 결제 → 확정 | — | 생성 · ACCEPTED |
| 2 | `용량,수량변경.har` | 새 구매에 쥬베룩 1cc ×2 · 백옥주사 · 승모근보톡스100 담기 → 보톡스 용량 100→1000 | 생성 · INITIALIZED (pending 4) | 변화 없음 |
| 3 | `선불카드.har` | 선불카드 생성(포인트 충전) | 변화 없음 | 변화 없음 |
| 4 | `선불카드 결제.har` | 구매 A 를 선불카드로 결제 → 확정 | ACCEPTED · 거래 1 | 변화 없음 |
| 5 | `결제 취소.har` | 구매 B 의 현금 거래 취소 | 변화 없음 | 거래 2 |
| 6 | `재결제.har` | (5 의 기록을 앞부분에 그대로 포함 — `#0~#20` 의 취소 요청 body 가 5 와 같음) → 구매 B 를 다시 현금 결제 | 변화 없음 | 거래 3 |

근거: 구매 A·B 는 각 HAR 의 `get-purchase-summaries` 응답 `data[].id` 대조. `재결제.har#13` 요청 body = `결제 취소.har#13` 요청 body(바이트 동일).

⚠ **새 HAR 6개 어디에도 `ticket/v1/queries/get-ticket-bundles` 호출이 없다.** 시술권 탭을 연 기록이 없어서 Q1 의 핵심(티켓 행 수)과 Q2 · Q4 의 「시술권이 어떻게 되나」는 닫히지 않았다(아래 각 절 「확인 안 됨」).
근거: 여섯 HAR 의 요청 경로 전수 목록(아래 각 절) · 응답 본문에 `ticketSets` · `tickets` · `ticketGroupId` 키 0건(`고객상세.har` · `고객정보조회 .har` 에만 있음).

---

## Q1 다회권 — `다회권구매.har`

### 경로(요청 순서 · 텔레메트리 · 권한 조회 제외)

| # | 경로 | 요청 body 키 |
|---|---|---|
| 1 | `schedule/group/v1/queries/get-reservation-group` | id |
| 3 | `schedule/v1/queries/get-schedule-summaries` | visitorId · sort |
| 4 | `v1/visitor/queries/get-visitor` | |
| 6 | `purchase/v1/commands/initialize-purchase` | id · visitorId · assigneeId · assigneeIds[] |
| 8 | `purchase/v1/commands/add-pending-purchase-items` | purchaseId · items[] |
| 9 | `schedule/v1/commands/register-purchase` | scheduleId · purchaseId |
| 10 · 18 · 20 · 21 | `purchase/v1/queries/get-purchase-summaries` | purchaseIds[] · includeDeleted |
| 14 · 25 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | visitorId |
| 15 | `purchase/payment-settings/v1/queries/get-payment-settings` | |
| 22 | `purchase/v1/commands/add-transaction` | purchaseId · transaction{…} |
| 24 | `purchase/v1/commands/accept-purchase` | purchaseId |
| 26 | `visitor/files/v1/queries/get-visitor-files` | |
| 28 · 30 | `get-purchase-summaries` | |

### 답

| 질문 | 답 | 근거 |
|---|---|---|
| 옵션 `count` · 단위 | 「크라이오 진정관리 5회」 `optionConfiguration.count = 5` · `unit` 키 없음 · `optionType = SINGLE` · `compositions = []` · `medicalService.configuration.unit` 없음 | `#8` 요청 `items[0].optionConfiguration` · `#10` 응답 |
| 구매 항목 행 수 | **항목 1행**(count 5 를 한 행에 담음). 가격 = 한 행 전체 328,900(공급 299,000 · 부가세 29,900 · 면세 0). `price` · `priceV2.amount` · `basePrice.amount` 셋 다 328,900 | `#10` `pendingItems` 1건 → `#28` `items` 1건 |
| 티켓이 10행인지 1행+남은 횟수인지 | **확인 안 됨** — 이 HAR 에 `get-ticket-bundles` 호출 0 | 위 경로 목록 |
| 티켓마다 가격 나누기 · 나머지 처리 | **확인 안 됨**(같은 이유). 참고: 기존 HAR 의 1회권은 티켓 `price` = 번들 `price`(예: 「[오픈] 올리디아 120 1CC」 259,600 = 티켓 259,600) | `고객상세.har#37` |
| 티켓 상태값 · 구매 직후 상태 | 새 HAR 에 없음. **기존 HAR 에서 본 상태값: `AVAILABLE` · `IN_USE` · `USED`**(그 밖 값은 표본 없음). 구매 직후 상태는 확인 안 됨 | `고객상세.har` · `고객정보조회 .har` · `상품 수납.har` 의 `get-ticket-bundles` 응답 `ticketSets[].tickets[].status` |
| 기존 HAR 의 세트당 티켓 수 | 전부 1장(세트 28개 응답 · 반복 조회 포함) — 다회권 표본 없음 | 같은 곳 |
| `ticketConfiguration.round` 출처 | 일정 상세 `schedule/v1/queries/get-schedule-detail` 의 `data.tasks[].procedureConfiguration.ticketConfiguration{ticketId, round{total, current}}`(표본은 1/1). 예약 목록 `schedule/v2/queries/get-schedules-for-reservation` 에서는 같은 자리가 `{}` | `상품 수납.har#124` · `#115` |

**필요한 HAR**: 위 다회권(5회) 산 고객의 **고객 상세 → 시술권 탭**(`get-ticket-bundles`) 1회 + 그 시술권으로 **작업 1회 쓴 뒤** 일정 상세(`get-schedule-detail` → `ticketConfiguration.round`) 1회.

---

## Q2 취소 · 재결제 — `결제 취소.har` · `재결제.har`

### 경로(명령만 · 요청 순서)

| HAR # | 명령 | 요청 body |
|---|---|---|
| `결제 취소.har#13` (= `재결제.har#13`) | `purchase/v1/commands/add-canceled-transaction` | purchaseId · transaction{ id · price(**-328,900**) · status=`CANCELED` · paymentType=`CASH` · cashConfiguration{} · assigneeId · **canceledRefId**(원거래 id) · createdDateTimeUtc · suppliedAmount(-299,000) · taxFreeAmount(0) · vatAmount(-29,900) · paymentDateTime{ lastUpdatedDateTimeUtc · approvedDateTimeUtc(원거래 승인 시각) · **canceledDateTimeUtc** } } |
| `재결제.har#38` | `purchase/v1/commands/add-transaction` | purchaseId(**같은 구매 B**) · transaction{ id · price(328,900) · status=`APPROVED` · paymentType=`CASH` · cashConfiguration{} · assigneeId · createdDateTimeUtc · 공급 · 면세 · 부가세 · paymentDateTime{ lastUpdated · approved } } |

나머지는 조회뿐: `get-purchase-summaries`(#0 · 7 · 12 · 16~18 · 20 · 21 · 22 · 29 · 33 · 36 · 37 · 41 · 43) · `get-prepaid-card-summaries` · `get-payment-settings` · `get-reservation-group` · `get-schedule-summaries` · `get-visitor`.
**`initialize-purchase` · `register-purchase` · `accept-purchase` · 항목 명령은 두 HAR 에 0건.**

### 답

| 질문 | 답 | 근거 |
|---|---|---|
| 취소 단위 | **거래(transaction) 단위.** 원거래를 바꾸지 않고 **음수 금액의 `CANCELED` 거래 1건을 더한다**(`canceledRefId` → 원거래). 원거래는 그대로 `APPROVED` 로 남는다 | `결제 취소.har#13` 요청 · `#16` 응답 구매 B `transactions` 2건(APPROVED +328,900 / CANCELED -328,900, cancRef=원거래) |
| 항목 단위인가 | 이 흐름에서는 **아니다** — 취소 전후 구매 B `items` 1건 그대로(가격 · 키 변화 없음) | `#12` vs `#16` |
| `revokingItems` · `refundingItems` | 취소 뒤에도 **둘 다 0건**(구매 A·B 모두) — 언제 무엇이 들어가는지 **확인 안 됨** | `결제 취소.har#16~#20` · `재결제.har#41 · #43` |
| 취소 뒤 `status` · `process` | **변하지 않는다 — `ACCEPTED` / `NOT_IN_PROCESS` 그대로.** 새 값 0개. 여섯 HAR + 기존 HAR 전체에서 본 쌍은 `INITIALIZED/PENDING` · `ACCEPTED/NOT_IN_PROCESS` 둘뿐 | 각 HAR `get-purchase-summaries` 전수 |
| 재결제 = 같은 구매? 새 구매? | **같은 구매 B 에 거래를 하나 더 붙인다.** 새 구매 · 재확정(accept) 없음. 결과 구매 B 거래 3건: APPROVED +328,900 → CANCELED -328,900 → APPROVED +328,900 | `재결제.har#38` · `#41` 응답 |
| 일정 `purchaseIds[]` 변화 | **확인 안 됨** — 이번 HAR 의 `get-schedule-summaries` 응답 키는 `consultation · consultations · deleted · flowStep · id · reservation · reservationTagIds · tasks` 로 `purchaseIds` 키가 없다. 다만 재결제 흐름에 `register-purchase` 가 0건이고 조회 대상 구매 id 목록(2건)이 앞뒤로 같다 | `재결제.har#4 · #26` 응답 키 · 명령 목록 |
| 취소된 구매의 시술권 | **확인 안 됨** — `get-ticket-bundles` 호출 0 | 경로 목록 |

### `transactions[]` 한 건의 전체 키(응답 · `get-purchase-summaries`)

```text
id(str)
price{value, currency}                       — 취소 거래는 음수
status                                        — 본 값: APPROVED · CANCELED
paymentType                                   — 본 값: CASH · PREPAID_CARD · TRANSFER(기존 HAR)
cardConfiguration{}                           — 표본은 전부 빈 객체
cashConfiguration{}
transferConfiguration{}
platformConfiguration{}
prepaidCardConfiguration{prepaidCardId, chargingId, prepaidCardName}   — 선불카드 아니면 세 칸 모두 빈 문자열
easyPayConfiguration{}
medicalLoanConfiguration{}
assignee{id, name}                            — 거래마다 담당 직원
canceledRefId                                 — 취소 거래만 원거래 id, 나머지는 빈 문자열
createdDateTimeUtc
suppliedAmount{value, currency} · taxFreeAmount{…} · vatAmount{…}
paymentDateTime{lastUpdatedDateTimeUtc, approvedDateTimeUtc, canceledDateTimeUtc?}   — canceled 는 취소 거래에만
```

근거: `결제 취소.har#16` 응답 구매 B · `선불카드 결제.har#9` 응답 구매 A. 요청(`add-transaction`)에는 `assignee` 대신 `assigneeId`, 해당 수단의 `…Configuration` 하나만 실린다.
카드 · 플랫폼 · 간편결제 · 의료대출 거래의 `…Configuration` 안쪽 키는 **표본 0 — 확인 안 됨**.

---

## Q3 선불카드 — `선불카드.har` · `선불카드 결제.har`

### 경로

| HAR # | 경로 | 요청 body |
|---|---|---|
| `선불카드.har#13` | `purchase/prepaid-card/v1/commands/create-prepaid-card` | **streamId**(= 생성될 카드 id) · title · **chargingAmount**{value, currency}(이번 0) · **chargingPoint**{value, currency}(이번 10,000,000) · expiredDateTimeUtc(생성 +1년) · buyer{visitorId, name, chartNumber, **owner**(bool, true)} · chargingMemo |
| `선불카드.har#16` 등 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | visitorId |
| `선불카드 결제.har#7` | `purchase/v1/commands/add-transaction` | paymentType=`PREPAID_CARD` · price 4,455,000(공급 4,050,000 · 부가세 405,000) · prepaidCardConfiguration{prepaidCardId, chargingId, prepaidCardName} |
| `선불카드 결제.har#8` | `purchase/v1/commands/accept-purchase` | purchaseId |

### 답

| 질문 | 답 | 근거 |
|---|---|---|
| `get-prepaid-card-summaries` `data[]` 구조 | `{ id, title, remainingBalance{balance{value,currency}, total{value,currency}}, remainingPoint{balance{…}, total{…}}, expirationDateTimeUtc, createdDateTimeUtc, ownerId, description, translsMap{}, updatedDateTimeUtc }` — **잔액이 두 주머니(금액 balance · 포인트 point)**, 각각 남은 값 · 누적 total | `선불카드.har#16` 응답 |
| 생성 직후 값 | 카드 1장 · balance 0/0 · point 10,000,000/10,000,000 · `id` = 생성 요청의 `streamId` · `ownerId` = 고객 visitorId | `선불카드.har#13` 요청 · `#16` 응답 |
| 충전이 구매(항목)로 남나 | 이번 표본(**포인트 충전 · 금액 0**)에서는 **남지 않는다** — 생성 전후 `get-purchase-summaries` 의 구매는 구매 B 1건 그대로, 새 구매 · 항목 0 · `initialize-purchase` 0. **금액(chargingAmount>0) 충전이 구매를 만드는지는 확인 안 됨** | `선불카드.har#0~#18` 조회 결과 · 명령 목록(`create-prepaid-card` 1건뿐) |
| 충전 · 사용 · 포인트 이력 조회 경로 | **없다** — 10개 HAR 전체의 선불카드 경로는 `create-prepaid-card` · `get-prepaid-card-summaries` · `get-visitor-prepaid-card-balance` 셋뿐 | HAR 10개 경로 전수 |
| 선불카드 결제가 거래에 남는 모양 | 거래 1건 `paymentType=PREPAID_CARD` · `prepaidCardConfiguration{prepaidCardId(= 카드 id), chargingId, prepaidCardName(= 카드 title)}`. **`chargingId` 는 카드 id 와 다르고, 10개 HAR 의 다른 어느 응답에도 나오지 않는다**(충전 건 id 로 보이나 조회 경로 없음 — 확인 안 됨) | `선불카드 결제.har#7` 요청 · `#9` 응답 · chargingId 값 전수 검색 |
| 결제 뒤 잔액 변화 | point 10,000,000 → **5,545,000**(= 4,455,000 차감) · total 10,000,000 그대로 · balance 0/0 그대로 → 금액이 0 이라 포인트에서 빠졌다. 금액 · 포인트가 둘 다 있을 때 어느 쪽 먼저인지는 확인 안 됨 | `선불카드.har#16` vs `선불카드 결제.har#10` |
| `get-visitor-prepaid-card-balance` | **새 HAR 에는 호출 0.** 기존 HAR 의 응답 모양: `data{remainingBalance{balance,total}, remainingPoint{balance,total}}`(고객 합계, 카드 구분 없음) · 요청 visitorId | `고객상세.har#39` |
| 선불카드 결제를 취소하면 | 확인 안 됨 — 이번 취소는 현금 거래(구매 B). 취소 뒤 카드 잔액 5,545,000 그대로 | `결제 취소.har#15` |

**필요한 HAR**: (a) **금액**(chargingAmount>0) 충전 1회 — 구매가 생기는지, (b) 고객 상세 선불카드 탭에서 카드 **상세/이력** 열기(경로가 있으면 잡힌다), (c) 선불카드 결제 **취소** 1회 — 잔액 복구 · 취소 거래의 chargingId.

---

## Q4 용량 · 수량 변경 — `용량,수량변경.har`

### 경로(명령만 · 요청 순서)

| # | 명령 | 요청 body |
|---|---|---|
| 13 | `purchase/v1/commands/initialize-purchase` | id · visitorId · assigneeId · assigneeIds[] |
| 14 | `purchase/v1/commands/add-pending-purchase-items` | 쥬베룩 1cc (항목 id ①) |
| 15 | `schedule/v1/commands/register-purchase` | scheduleId · purchaseId |
| 25 | `purchase/v1/commands/add-pending-purchase-items` | **쥬베룩 1cc 같은 옵션 · 새 항목 id ②** |
| 29 | `purchase/v1/commands/add-pending-purchase-item`(단수) | `item` — 백옥주사 |
| 36 | `purchase/v1/commands/add-pending-purchase-item` | `item` — 승모근보톡스100 · `optionConfiguration.unit{type: UNIT, value: 100}` · 440,000 |
| 42 | `purchase/v1/commands/change-pending-purchase-items-option-unit` | purchaseId · **purchaseItemIds[]**(1건) · **changedBasePrice**{amount 4,400,000 · suppliedAmount 4,000,000 · taxFreeAmount 0 · vatAmount 400,000 · taxation TAXABLE} · **singleOptionUnitChangeConfiguration**{optionPrice{4,400,000}, singleOptionUnit{type: UNIT, value: 1000}} |

모든 명령 응답 본문은 `{}`. 화면 이벤트(amplitude 이벤트 이름 · 값만): `#27` `purchase.changed.purchase_item_count` previous 1 → next 2 · `#43` `purchase.clicked.change_unit_button` previousUnitValues ["100"] → nextUnitValues ["1000"].

### 답

| 질문 | 답 | 근거 |
|---|---|---|
| **수량** 변경 | 화면의 수량 1→2 는 **같은 옵션 항목을 한 행 더 추가**한 것(`add-pending-purchase-items`, 새 항목 id). 두 행 모두 `count = 1` · 11,000. 수량 칸은 없다 | `#25` 요청 · `#28` 응답 pendingItems 2건(같은 option id, 다른 item id) |
| **용량** 변경이 남는 곳 | **구매 항목의 옵션 스냅샷을 덮어쓴다**: `optionConfiguration.unit` 100 → **1000** · `optionConfiguration.price` 440,000 → 4,400,000 | `#41` vs `#45` 응답 보톡스 항목 |
| 원래 값이 남나 | 원래 옵션 단위 100 은 **항목 어디에도 원값 칸으로 남지 않는다.** 남은 흔적은 (a) `optionConfiguration.medicalService.configuration.unit = {UNIT, 100}`(진료항목 기본 단위라 안 바뀜) (b) 옵션 `title` 「승모근보톡스100」(안 바뀜) 뿐. 「변경 전 / 변경 후」 짝 칸 없음 | `#45` 응답 |
| 가격이 같이 바뀌나 | **바뀐다** — `price` · `priceV2`(amount 4,400,000 · 공급 4,000,000 · 부가세 400,000) · **`basePrice` 까지** 4,400,000 으로. `priceAdjustments` 0 — 조정 기록이 아니라 기준가 자체를 바꾼다(이번 표본은 단위 ×10 = 가격 ×10) | `#42` 요청 · `#45` 응답 |
| 시술권 세트 · 티켓 | **확인 안 됨** — 이 구매는 이 HAR 에서 확정되지 않았고(INITIALIZED/PENDING), 시술권 조회도 0. 이후 `선불카드 결제.har#8` 로 확정됐지만 그 뒤에도 `get-ticket-bundles` 0 | 경로 목록 |
| 단서(`고객상세.har`) | 「[오픈] 올리디아 120 1CC」 번들(번들 `optionConfiguration.optionTitle` 쪽) 아래 세트 `title` 「올리디아 120 4cc」 · 세트 `unit` 은 `{}` · 티켓 1장 259,600. 번들 제목 = 옵션 이름, 세트 제목 = 바뀐 용량이 들어간 이름으로 **보이나** 용량 변경 기록과 짝지은 표본이 없어 확인 안 됨 | `고객상세.har#37` |

**필요한 HAR**: 이번 구매 A(보톡스 1000 · 쥬베룩 ×2 포함, 이미 확정됨) 고객의 **고객 상세 → 시술권 탭**(`get-ticket-bundles`) 1회 — 세트 제목 · `unit` · 티켓 가격, 쥬베룩 2행이 번들 2개인지.

---

## Q5 초안 ERD 대조

`erd-draft.md` 의 결제 · 시술권 · 선불카드 테이블은 **테이블 이름과 관계만** 있고 칸 목록이 없다. 그래서 아래 「담을 칸 없음」은 칸이 정의된 메뉴 테이블(`04-1-menu.md`)은 칸 단위로, 나머지는 「이 값을 받을 테이블 후보」로 적는다.

### 5-1. 담을 칸 없음(값 · 테이블 후보)

| # | KOS 값 | 본 곳 | 테이블 후보 | 비고 |
|---|---|---|---|---|
| 1 | 옵션 단위 `optionConfiguration.unit{type, value}`(SINGLE 옵션) | `용량,수량변경.har#36` | `product_option` | 04-1 `product_option` 에 단위 칸 없음(단위는 `medical_service` · `composition` 에만). 옵션 단위(1000)와 진료항목 단위(100)가 다를 수 있다 |
| 2 | 구매 항목의 바뀐 단위 · 바뀐 가격 | `#45` | `purchase_item` | 항목 스냅샷 칸 미정의 |
| 3 | `changedBasePrice` · `singleOptionUnitChangeConfiguration.optionPrice` | `#42` 요청 | `purchase_item` | 변경 명령의 입력값. 원래 기준가는 응답에서 사라짐 |
| 4 | 거래 `status`(APPROVED · CANCELED) · `canceledRefId` · `paymentDateTime.approved/canceled/lastUpdated` | `결제 취소.har#13 · #16` | `purchase_transaction` | 취소 = 음수 거래 + 원거래 참조(자기 참조) |
| 5 | 거래 금액 분해 `suppliedAmount` · `taxFreeAmount` · `vatAmount` | 같은 곳 | `purchase_transaction` | |
| 6 | 거래 담당 `assignee`(거래마다) | 같은 곳 | `purchase_transaction` | 초안의 `purchase_assignee` 는 구매 단위 |
| 7 | 수단별 설정 7종 `card · cash · transfer · platform · prepaidCard · easyPay · medicalLoan Configuration` | 같은 곳 | `purchase_transaction` | 선불카드 외 안쪽 키는 표본 없음 |
| 8 | 선불카드 `remainingBalance{balance,total}` · `remainingPoint{balance,total}` | `선불카드.har#16` | `prepaid_card` | 금액 · 포인트 두 주머니 |
| 9 | 선불카드 `title` · `description` · `expirationDateTimeUtc` · `ownerId` | 같은 곳 | `prepaid_card` | 유효기간 있음(생성 +1년) |
| 10 | 생성 `chargingAmount` · `chargingPoint` · `chargingMemo` · `buyer.owner`(bool) | `선불카드.har#13` | `prepaid_card` / `prepaid_card_ledger` | 「구매자 ≠ 소유자」 가능성(owner 플래그) |
| 11 | 거래 `prepaidCardConfiguration.chargingId` | `선불카드 결제.har#7` | `prepaid_card_ledger`(충전 건) | 가리키는 대상 조회 경로 없음 |
| 12 | 시술권 세트 `unit{}` | `고객상세.har#37` | `ticket_set` | 표본은 빈 객체 |
| 13 | 일정 작업 `ticketConfiguration{ticketId, round{total,current}}` | `상품 수납.har#124` | `visit_task`(`ticket_id` · 회차 스냅샷) | 초안에 이미 「회차 스냅샷 남긴다」 있음 — 칸 이름만 미정 |
| 14 | 구매 항목 `type`(본 값 `PRODUCT_OPTION` 뿐 · 251건) | 전 HAR | `purchase_item` | 다른 타입 표본 없음 |

### 5-2. 초안과 어긋나는 사실

| # | 초안 | HAR 사실 | 근거 |
|---|---|---|---|
| A | 「수납 필요 = 열린 구매(INITIALIZED)」(정할 것 2) | 결제를 취소해 순결제액이 0 인 구매도 `ACCEPTED/NOT_IN_PROCESS` 그대로다. **`status` 만으로는 「돈이 들어왔나」를 알 수 없고 거래 합계가 필요하다** | `결제 취소.har#16` |
| B | 「취소 · 환불이 항목 단위면 그때 더한다 — 환불 HAR 1건 필요」 | 이번 「결제 취소」는 **항목이 아니라 거래 단위**(음수 거래). `revokingItems` · `refundingItems` 는 여전히 0 → 항목 단위 취소/환불은 다른 화면 동작일 가능성 — 표본 없음 | `결제 취소.har#13 · #16` |
| C | 재결제 모양 미정 | 같은 구매에 거래 추가 · 재확정 없음 → 구매 1 : 거래 N 이 「결제 · 취소 · 재결제」 이력을 다 담는다 | `재결제.har#38 · #41` |
| D | `purchase_item |o--o| prepaid_card : 충전 출처(확인 필요)` | 포인트 충전은 **구매를 만들지 않는다**(금액 충전은 미확인) | `선불카드.har` 명령 · 조회 |
| E | `prepaid_card_ledger : 충전 · 사용 · 포인트(확인 필요)` | KOS 에 **이력 조회 경로가 없다**(본 HAR 범위). 사용은 거래(`PREPAID_CARD`)로만, 충전은 `chargingId` 로만 흔적 | Q3 |
| F | 「유효기간 칸 두지 않는다 — KOS 에 값이 없고」(3-1, 시술권) | 시술권은 여전히 값 없음. 다만 **선불카드에는 유효기간이 있다**(`expiredDateTimeUtc` · `expirationDateTimeUtc`) — 3-1 은 시술권 결정이라 충돌은 아님, 선불카드 칸은 미정 | `선불카드.har#13 · #16` |
| G | 「참조 + 스냅샷」(옵션 → 구매 항목) | 용량 변경 시 KOS 는 **스냅샷을 덮어써** 원래 단위 · 기준가를 잃는다. 원래 값은 `product_option` 참조로만 되찾을 수 있다 | Q4 |
| H | (수량 개념 없음) | 수량 = 항목 행 반복. 초안과 충돌은 없음 — 기록만 | Q4 |

### 5-3. 정할 것(결정하지 않음)

1. **결제 완료 판단** — `purchase.status` 에 더해 거래 합계(승인 − 취소)를 볼지, 구매에 「결제액 · 미수액」 파생 칸을 둘지 (A).
2. **취소 모델** — 음수 `CANCELED` 거래 + `canceled_ref_transaction_id`(자기 참조)로 KOS 와 같게 갈지, 원거래에 상태를 둘지 (4 · B).
3. **거래 담당자** — 거래마다 담당(`assignee`)을 둘지, 구매 담당(`purchase_assignee`)으로 충분한지 (6).
4. **수단별 설정** — 7종 `…Configuration` 을 jsonb 한 칸으로 둘지 수단별 칸으로 둘지(선불카드 외 안쪽 키 표본 0) (7).
5. **선불카드 두 주머니** — 금액 · 포인트를 칸으로 나눌지, 잔액을 원장(ledger) 합으로 셀지 · 원장 없이 KOS 잔액만 받을지 (8 · E).
6. **선불카드 유효기간 · 소유자/구매자** (9 · 10 · F).
7. **충전 출처** — 금액 충전이 구매를 만드는지 HAR 로 먼저 확인 후 `purchase_item ↔ prepaid_card` 관계 유지 여부 (D).
8. **용량 변경** — 구매 항목에 「원 옵션 단위 · 원 기준가」와 「바뀐 단위 · 바뀐 가격」을 둘 다 둘지, 바뀐 값만 두고 원값은 `product_option` 참조로 볼지 · `product_option` 에 옵션 단위 칸을 더할지 (1 · 2 · 3 · G).
9. **다회권 티켓 행 수** — 정할 것 3(10회권 = ticket 10행)은 DAY 쪽 결정으로 이미 정해졌다. KOS 모양과 같은지는 아래 HAR 로 확인 뒤 동기화 매핑에서.

## 확인 안 됨 — 필요한 HAR

| 질문 | 필요한 HAR |
|---|---|
| Q1 티켓 행 수 · 가격 나누기 · 구매 직후 상태 | 다회권(크라이오 5회) 고객의 고객 상세 **시술권 탭**(`get-ticket-bundles`) |
| Q1 round 의 다회권 값 | 그 시술권으로 작업 1회 쓴 뒤 **일정 상세**(`get-schedule-detail`) |
| Q2 취소된 구매의 시술권 | 결제 취소한 구매 B 고객의 **시술권 탭** |
| Q2 `revokingItems` · `refundingItems` | 확정된 구매에서 **항목 하나만 취소/환불**하는 동작(화면에 있다면) |
| Q2 일정 `purchaseIds[]` | 일정 상세(`get-schedule-detail`) 1회 |
| Q3 금액 충전 · 이력 · 선불카드 결제 취소 | Q3 「필요한 HAR」(a)(b)(c) |
| Q4 시술권 쪽 용량 | 구매 A 고객의 **시술권 탭** |
| 거래 수단별 설정 안쪽 키 | 카드 · 플랫폼 · 간편결제 · 의료대출 결제 각 1회(필요하면) |

※ 시술권 탭 HAR 하나(같은 고객)로 Q1 · Q2(시술권) · Q4(시술권) 세 칸이 같이 닫힌다.

## 개인정보 점검

```text
grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9]{6}-?[1-4][0-9]{6}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|Bearer|[0-9a-f]{24}' har-check-report.md
```

점검 결과(2026-11-18): 일치 **1줄 — 위 grep 명령 줄 자신**(패턴 문자열 안의 `Bearer`). 그 밖 전화번호 · 주민번호 꼴 · 이메일 · `Bearer` · 24자리 hex **0건**.
추가로 HAR 에서 본 직원 · 고객 이름 · 차트번호 문자열을 직접 grep → 0건.
