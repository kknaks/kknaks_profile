# 후납 수납 뒤 「수납 필요」가 꺼지나

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-postpay-report.md`(`PP§`)에서 이어진다
- 원천: `reference/2026-10-23-cc-overall-board/har/수납필요 확인.har`(249항목 · 08:20:09.9Z ~ 08:20:37.8Z, gitignore)
- 대상 일정: 앞 판과 **같은 일정**(오늘 19:00 KST · `RECEPTION`). 작업 ②(결제 뒤 옵션만으로 넣은 작업)를 수납한 장면이다
- **KOS 쓰기 0건.** 데모 조회만 했다(테넌트 · 키 `assert`, 쓰기 허가 목록 비움). 운영 키 0
- 표기
  - **확인**: HAR · 데모로 본 것
  - **추정**: 해석
- 리포트에 id · 토큰 · 이름 · 금액 값은 적지 않았다

---

## 0. 결론

- **「수납 필요」는 꺼진다.** 꺼지는 때는 **`accept-purchase`(수납 확정) 직후**다
  - `register-purchase`(일정에 수납 연결) 뒤에는 아직 `paymentRequired: true` 였다
  - 확정하자 KOS 가 **새 수납에서 나온 시술권을 작업 ②에 자동으로 붙이고**(`ticketConfiguration.ticketId` · `round{1/1}`) `paymentRequired` 를 **false** 로 바꿨다(소켓 이벤트 · 지금 조회 둘 다 확인)
  - 작업 ②를 고치는 별도 호출은 없었다
- 판정 규칙(앞 판 추정의 확인): **작업에 시술권이 붙으면 결제됨, 없으면 수납 필요**. 시술권은 「수납 확정」 때 그 항목 옵션과 같은 옵션의 작업에 붙는다
- **KOS 웹은 일정 변경을 소켓으로 받는다**
  - 연결: `wss://schedule-socket.kos-solution.com/socket.io/?room={tenantId}&EIO=4&transport=websocket`(Socket.IO v4)
  - 인증: 내부 `schedule/socket/v1/commands/issue-schedule-socket-token` 이 준 토큰을 연결 직후 보낸다
  - 이벤트 `updated{schedule: 일정 전체, version}` · `ticketUpdated{visitorId, ticketBundles}`
  - 일정 전체의 키는 `get-schedule-detail` 과 같다(확인)
- 정산 상자 「수납 필요 N건」 · [귀가 완료] 꺼짐은 **KOS 값만으로 판정할 수 있다**(`tasks[].paymentRequired` 개수). 금액(후납 얼마)은 여전히 KOS 값이 없다(PP Q-111)
- 정할 것은 **5개**다(Q-118 ~ Q-122)

---

## 1. HAR 인벤토리

항목 249 구성

| 출처 | 항목 수 |
|---|---|
| KOS `api.kos-solution.com` POST | 96 |
| KOS OPTIONS | 9 |
| KOS 정적 `core-cf.kos-solution.com` | js 74 · css 1 · svg 1 |
| KOS `app.kos-solution.com` mp3 | 1(알림음으로 보인다, 추정) |
| **KOS 웹소켓 `schedule-socket.kos-solution.com`** | 1(메시지 9) |
| Datadog | 55 |
| Amplitude | 3 |
| `api.channel.io`(상담 채팅 위젯) | 8 |

HAR 맨 앞이 예약 현황 판 → 고객 상세(상담 탭)를 다시 연 장면이라 조회가 많다.

KOS POST 96건(경로별, 처음 나온 순서)

| 경로 | 횟수 | 대표 # | 용도 |
|---|---|---|---|
| `schedule/default-operation-time/v1/queries/get-default-days-off` | 3 | 0 · 4 · 26 | |
| **`schedule/socket/v1/commands/issue-schedule-socket-token`** | 1 | **13** | 소켓 토큰 발급(§3). 이름은 command 지만 KOS 데이터를 바꾸지 않는다 |
| `schedule/zone/v1/queries/get-zones` | 2 | 27 · 33 | |
| `role/v2/queries/get-roles` | 2 | 28 · 183 | |
| `schedule/default-operation-time/v1/queries/get-default-operation-timetable` | 1 | 29 | |
| `schedule/occupied-time/v2/queries/get-occupied-times` | 1 | 31 | |
| `account/v2/queries/get-accounts-last-update…` | 3 | 32 · 221 · 244 | |
| `meta/notice/v1/queries/get-notices` | 2 | 35 · 113 | |
| `schedule/group/v1/queries/get-reservation-groups` | 2 | 36 · 111 | |
| `account/v2/queries/get-accounts` | 7 | 37 … 230 | |
| `meta/codes/v1/queries/get-codes` | 13 | 38 … 155 | |
| `visitor/v2/queries/get-visitor` | 1 | 39 | |
| `schedule/v1/queries/get-payment-required-tasks` | 1 | 40 | `{visitorId}` → **0건**(작업 ②가 `paymentRequired: true` 인 때인데도, PP Q-114 와 같다) |
| `schedule/v1/queries/get-schedule-detail` | 1 | 41 | **수납 전**: 작업 ① false · 시술권 있음 / 작업 ② **true** · 시술권 없음 · `purchaseIds` 2 |
| `account/v2/queries/get-accounts-status` | 1 | 43 | |
| `schedule/group/v1/queries/get-reservation-group` | 5 | 69 … 243 | |
| `procedure-menu/visitors/queries/get-visitors` | 3 | 74 · 185 · 205 | |
| `procedure-menu/currency-settings/queries/get-currency-settings` | 3 | 75 · 134 · 148 | |
| `consultation/v1/queries/get-consultations-by-visitor-id` | 2 | 82 · 107 | |
| `schedule/v1/queries/get-schedule-summaries` | 2 | 83 · 186 | |
| `ticket/v1/queries/get-ticket-bundles` | 1 | 84 | |
| `purchase/tax-refund-settings/v1/queries/get-tax-refund-settings` | 1 | 121 | |
| `v1/visitor/queries/get-visitor` | 4 | 125 · 164 · 187 · 222 | |
| `purchase/payment-settings/v1/queries/get-payment-settings` | 2 | 126 · 229 | |
| `procedure-menu/vat-settings/queries/get-vat-settings` | 1 | 133 | |
| `meta/template/v1/queries/get-hospital-text-snippets` | 1 | 136 | 병원 상용구 |
| `schedule/group/v1/queries/get-reservation-group-days-offs` | 1 | 139 | |
| `schedule/v2/queries/get-schedules-for-reservation` | 1 | 140 | |
| `purchase/v1/queries/get-purchase-summaries` | 13 | 152 … 248 | 약 3초마다 다시 읽는다 |
| `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | 1 | 153 | |
| `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | 3 | 156 · 228 · 240 | |
| `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | 1 | 157 | |
| `security/v2/queries/check-message-permission` | 1 | 158 | |
| `procedure-menu/product-options/v2/queries/search-product-option-summaries` | 3 | 190 · 208 · 212 | |
| `procedure-menu/target-countries/v1/queries/get-target-countries` | 1 | 203 | |
| **`purchase/v1/commands/initialize-purchase`** | 1 | **215** | 수납 ③ 생성 |
| **`purchase/v1/commands/add-pending-purchase-items`** | 1 | **216** | 항목 1 |
| **`schedule/v1/commands/register-purchase`** | 1 | **217** | 일정 연결 |
| **`purchase/v1/commands/add-transaction`** | 1 | **237** | 결제 1 |
| **`purchase/v1/commands/accept-purchase`** | 1 | **238** | 확정 |

합계 96. KOS 데이터를 바꾼 쓰기는 수납 5건이다(+ 소켓 토큰 발급 1).

---

## 2. 수납 ③ ↔ 작업 ② 연결 · 「수납 필요」가 꺼지는 때

| 시각(Z) | 사건 | 작업 ②(`paymentRequired` · 시술권) | 근거 |
|---|---|---|---|
| 08:20:09 ~ | 수납 전 | **true** · 없음 | #41 일정 상세 |
| 08:20:24.09 ~ 24.73 | `initialize-purchase` → `add-pending-purchase-items` → `register-purchase` | — | |
| 08:20:25.02 | 소켓 `updated` | **true** · 없음. `purchaseIds` 2 → **3** | 소켓 |
| 08:20:30.97 ~ 31.04 | `add-transaction` → **`accept-purchase`** | — | |
| 08:20:31.27 | 소켓 `ticketUpdated` | 새 시술권 묶음 1개 — `purchaseId` = 수납 ③, `purchaseItemId` = 수납 ③의 그 항목, 시술권 1장(`AVAILABLE`) | 소켓 |
| **08:20:31.47** | 소켓 `updated` | **false** · **수납 ③의 시술권**(`round{total:1, current:1}`) | 소켓 |
| 지금 | 공개 `getScheduleDetail` | 작업 ① · ② 모두 **false** · 둘 다 시술권 있음 · `purchaseIds` 3 | 데모 조회 |

- **연결 근거**: 수납 ③의 항목(`add-pending-purchase-items`)의 상품 옵션 id 가 작업 ②의 `productOptionConfiguration.optionId` 와 같다(확인). 항목에 작업 sequence 를 가리키는 필드는 없다. KOS 가 옵션으로 짝을 맞춘 것으로 보인다(추정)
- **작업 ②에서 함께 바뀐 필드**(소켓 전 ↔ 후)
  - `paymentRequired`
  - `procedureConfiguration.ticketConfiguration.ticketId` · `round.total` · `round.current`
  - `procedureConfiguration.productOptionConfiguration.productTitle`
  - `procedureConfiguration.medicalServiceConfiguration.medicines` · `unit.type` · `unit.value`
  - → 작업 설정이 시술권(수납 항목) 쪽 값으로 다시 채워졌다
- 작업 상태(`NOT_STARTED`) · 순서 · 방은 그대로다
- 지금 수납 3건 모두 `ACCEPTED · NOT_IN_PROCESS` · 수납마다 항목 합 = 결제 합(확인)
- 내부 `get-payment-required-tasks` 는 지금도 0건이다. 이 조회는 판정에 쓸 수 없다(PP Q-114 그대로)

---

## 3. 소켓 (`issue-schedule-socket-token` · `schedule-socket`)

| 항목 | 내용(확인) |
|---|---|
| 토큰 발급 | 내부 `POST api.kos-solution.com/tenants/{tenantId}/schedule/socket/v1/commands/issue-schedule-socket-token` · 본문 `{}` → `{token: "<문자열>"}`. JWT 꼴은 아니다. 유효 기간 · 재발급 규칙은 응답에 없다 |
| 연결 | `wss://schedule-socket.kos-solution.com/socket.io/?room={tenantId}&EIO=4&transport=websocket`. **room = 테넌트 id**(확인) — 지점 전체 방이다 |
| 프로토콜 | Socket.IO v4(Engine.IO 4). 서버가 `0{sid, pingInterval:25000, pingTimeout:20000, maxPayload}` → 클라이언트가 `40{"token": …}` → 서버 `40{sid}` → 이벤트 `42[…]` · ping/pong `2`/`3` |
| 이벤트 `updated` | `42["updated", {schedule: {…}, version}]` — `schedule` 은 **일정 한 건 전체**(키 22개, `get-schedule-detail.data` 와 키가 같다). `version` 은 정수(이번 2회 모두 0) |
| 이벤트 `ticketUpdated` | `42["ticketUpdated", {visitorId, ticketBundles:[{purchaseId, purchaseItemId, optionConfiguration, price, ticketSets[{tickets[{status …}]}], title, translsMap, visitorId}]}]` |
| 이번에 받은 것 | 28초 동안 `updated` 2 · `ticketUpdated` 2 · ping 1. 모두 이 일정 · 이 고객 것이었다. 같은 시간에 다른 일정이 바뀌지 않았으므로, 다른 일정 변경도 오는지는 확인하지 못했다 |
| 인증 주체 | 토큰 발급이 내부 API(직원 세션)다. **공개 API 에는 소켓 · 웹훅이 없다**(스펙 grep) |

ccc 가 쓸 수 있는 것(사실만)
- 시스템 계정(내부 Bearer)으로 토큰을 받아 같은 주소에 붙으면, 일정이 바뀔 때 일정 전체가 즉시 온다. 10초 조회가 아니라 이벤트로 받는 길이다
- 공식 계약이 아니다. 끊김 · 재연결 · 놓친 이벤트를 따라잡는 방법(`version`?)은 문서가 없다 → Q-119 · Q-120

---

## 4. 정산 상자 · [귀가 완료] 규칙을 KOS 값만으로 할 수 있나

| 시안 | KOS 값 | 판정 |
|---|---|---|
| 「수납 필요 N건」 | 일정 `tasks[]` 중 `paymentRequired == true` 인 개수(「방 배정」 · 취소 제외는 시술 현황 규칙, PP§5) | **KOS 값만으로 된다** |
| 수납 필요가 풀리는 때 | 그 작업 옵션의 수납이 **확정(`accept-purchase`)** 된 때 → 작업에 시술권이 붙고 false | **KOS 값만으로 된다**(확인) |
| [귀가 완료] 꺼짐(후납이 남으면) | `paymentRequired == true` 작업이 하나라도 있으면 꺼짐 | **KOS 값만으로 된다.** 단 KOS `changeFlowStep(COMPLETED)` 자체는 「끝나지 않은 시술」로 거절한다(스펙). 수납 필요는 서버가 막는 조건이 아니다 → Q-121 |
| 「후납 금액」 | 없음 | 정가로 추정만 된다(PP Q-111) |
| 「수납 중」(수납을 만들었지만 확정 전) | 수납 `status INITIALIZED` · `process PENDING`(확인: 이번 HAR 의 등록 ~ 확정 사이) | 이 사이에는 아직 「수납 필요」가 켜져 있다 → Q-122 |

---

## 5. 호출 기록 (조회만)

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| 공개 | `getScheduleDetail` 1 · `getPurchaseSummaries` 1 · `getTicketBundlesQuery` 1 | 3 | 200 |
| 내부 | `schedule/v1/queries/get-payment-required-tasks` 1 | 1 | 200 |
| 인증 | 공개 `exchange-token` 1 · 내부 sign-in 1 | 2 | 200 |

- **쓰기 0건** · 운영 키 0건
- 소켓 토큰 발급 · 소켓 연결은 하지 않았다(HAR 해석만)

---

## 6. 정할 것 (결정하지 않음) — 5개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-118 | 「수납 필요」 판정을 `tasks[].paymentRequired` 로 확정할지 | 이번에 켜짐(옵션만으로 추가) · 꺼짐(수납 확정 → 시술권 자동 연결)을 모두 확인했다. 시술 현황 규칙과 같다. 남은 확인: 같은 옵션 작업이 둘일 때 시술권이 어느 작업에 붙는지 | PP Q-113 · Q-115 |
| Q-119 | KOS 소켓을 원천으로 쓸지 | 일정 전체가 즉시 온다. 내부 토큰 · 비공식 · 지점 전체 room 이다. 10초 조회와 같이 쓸지 · 대신 쓸지 · 쓰지 않을지 | workflow-v2 D-08 |
| Q-120 | 소켓 이벤트를 놓쳤을 때 | 재연결 사이의 변경을 따라잡는 방법이 문서에 없다(`version` 의 뜻 미확인). 다시 연결할 때 전체 조회를 할지 | — |
| Q-121 | [귀가 완료]를 「수납 필요」로 막을지 | KOS 서버는 수납 필요로 귀가를 막지 않는다(스펙 거절 조건은 끝나지 않은 시술뿐). 막는 것은 ccc 규칙이 된다 | PP Q-116 |
| Q-122 | 「수납 중」 상태 표시 | 수납을 만들고 확정하기 전(`INITIALIZED/PENDING`)에는 수납 필요가 그대로 켜져 있다. 「수납 중」을 따로 보일지 | PP Q-112 |
