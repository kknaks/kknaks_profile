# [backend · 실물 확인 3] 리포트 — 시술권 오늘 시술 · 오더 메모 · 시술 대기 · 시술 중 귀가 · 귀가 대기 → 귀가

- 데모 지점 확인(`check_open_key_is_demo`) 통과 뒤에만 썼다(스크립트마다 매번).
- 호출은 전부 DAY `KosClient.internal()`. 레포 수정 · 커밋 없음. 값 · 토큰 · 개인정보 출력 없음.
- 시험 고객: `6b051a9e`(1판에서 만든 고객).
- 이번에 만든 것: 오늘 예약 X `25a4e104`(16:00) · Y `6e7105ad`(16:30), 시술권 수납 1건(purchase `id` 는 `state.json`).
- 둘 다 끝 상태는 `flowStep=COMPLETED` · `reservation.status=COMPLETED`.
- 스크립트: `/private/tmp/day-probe-3/`
  - `prep.py`(준비) · `testx.py`(X 1 ~ 7)
  - `testy.py`(Y 8a ~ 8g) · `testy2.py`(코디 답 뒤 8g1 ~ 9)
  - `p3lib.py` · `pcommon.py`
  - `log.md` · `state.json` · `run*.out`

## 표

| # | 경로(끝 이름) | 응답 | O / X | 비고 |
|---|---|---|---|---|
| 준비 · 예약 X | `reservation/v2/commands/reserve` | 200 | O | 16:00, 1판 본문 그대로 |
| 준비 · 수납 | `initialize-purchase` → `add-pending-purchase-items` → `register-purchase` → `add-transaction`(CASH) → `accept-purchase` | 다섯 번 모두 200 | O | 옵션 `6a8d94aa…` SINGLE `count=3` 80,000원. 품목 본문은 `Seeder._purchase_item`(HAR #24 모양). ⚠ 가격 나누기는 아래 ⓐ-1 |
| 준비 · 시술권 | `ticket/v1/queries/get-ticket-bundles` | 200 | O | 새 묶음 1(`purchaseId` 일치) · `ticketSets` 1 · `tickets` 3 개(`469735eb` · `9bf521e8` · `abc48d58`) 모두 `AVAILABLE`. ticket 키 = `id · status · price · createdDateTimeUtc`(회차 칸 없음) |
| 1 접수 | `schedule/v1/commands/recept` | 200 | O | `RECEPTION`. 상세 `purchaseIds` 1개(수납 연결 O) · `purchases` 는 빈 배열 |
| 2 시술권 작업 | `add-flow-tasks` `PROCEDURE` | 200 | O | 1.1초 뒤 보임. `tasks[seq1]` PROCEDURE · NOT_STARTED · `ticketConfiguration.ticketId` O · `round {total:3,current:1}` 그대로. 시술권 `469735eb` **AVAILABLE → IN_USE**(나머지 둘은 AVAILABLE) |
| 3 오더 메모 | `schedule/v1/commands/change-order-memo {scheduleId, orderMemo}` | 200 | O | 바로 보임. 상세 `orderMemo` 이 보낸 값과 같음 |
| 4 방 배정 | — | (안 함) | — | 5 가 방 배정 없이 200 이어서 하지 않았다 |
| 5 시술 대기 | 내부 `change-flow-step {id, step:PROCEDURE_WAITING}` | 200 | O | `RECEPTION → PROCEDURE_WAITING`, **방 배정 작업 없이** 됨. 시술 작업은 방 없음 · NOT_STARTED 그대로 |
| 6 시술 진행 | 내부 `change-flow-step {id, step:PROCEDURE}` | 200 | O | `PROCEDURE`. 시술 작업 NOT_STARTED 그대로 · 시술권 IN_USE 그대로 |
| 7ⓐ COMPLETED 만 | 내부 `change-flow-step COMPLETED` | **400** | X | `InvalidRequestException` `errorProperties [{key:"procedures", reason:"NotAvailable"}]`(2판과 같음) · `flowStep` PROCEDURE 그대로 |
| 7ⓑ 작업 취소 | `cancel-flow-tasks {scheduleId, sequences:[1], reason:"CANCEL"}` | 200 | O | seq1 → `CANCELED`. 시술권 `469735eb` **IN_USE → AVAILABLE**(되돌아감) |
| 7ⓒ 귀가 | 내부 `change-flow-step COMPLETED` | 200 | O | 1.1초 뒤 `COMPLETED` · `reservation.status=COMPLETED`. 시술권 AVAILABLE 그대로. `paymentRequired` 는 모든 작업에서 `false` 라 따로 처리할 것 없음 |
| 8 · 예약 Y | `reserve` | 400 → 200 | O | 첫 시도는 16:00(X 와 같은 시각 · 같은 고객) → 400 `startDateTime NotAvailable`. 빈 칸 조회로는 남아 있던 칸. 1회 재시도를 16:30 으로 → 200 |
| 8 · 접수 · 방 배정 · 방 | `recept` · `add-flow-tasks ETCETERA` · `change-tasks-room` | 모두 200 | O | 2판과 같음. seq1 「방 배정」 NOT_STARTED → READY |
| 8 · 상담 대기 | 내부 `change-flow-step CONSULTATION_WAITING` | 200 | O | |
| 8 · 시술권 작업 | `add-flow-tasks PROCEDURE` | 200 | O | seq2. 남은 첫 AVAILABLE = `469735eb`(X 에서 되돌아온 1회차) → IN_USE |
| 8 · 시술 진행 | 내부 `PROCEDURE` | 200 | O | |
| 8 · 작업 완료 1차 | `change-tasks-complete {scheduleId, sequences:[2], complete:true}` | **400** | X | `errorProperties [{key:"complete", reason:"NotAvailable"}]`. 작업 NOT_STARTED · 방 없음 |
| 8 · (코디 ①) 방 지정 | `change-tasks-room` seq2 | 200 | O | 시술 작업 NOT_STARTED → **READY** |
| 8 · (코디 ①) 작업 완료 2차 | `change-tasks-complete` seq2 `complete:true` | **400** | X | 같은 오류(`complete NotAvailable`). READY 에서도 안 됨. 시술권 IN_USE |
| 8 · (코디 ③) 작업 취소 | `cancel-flow-tasks {sequences:[1,2], reason:"CANCEL"}` | 200 | O | 둘 다 CANCELED. 시술권 `469735eb` IN_USE → **AVAILABLE** |
| 8 · 귀가 대기 | 내부 `change-flow-step PROCEDURE_DONE` | 200 | O | 1.1초 뒤 `PROCEDURE_DONE` |
| 9 귀가 | 내부 `change-flow-step COMPLETED` | 200 | O | `flowStep=COMPLETED` · `reservation.status=COMPLETED` |
| 10 정리 | — | — | O | X · Y 둘 다 COMPLETED. 산 시술권 3장은 모두 AVAILABLE 로 남아 있다(손대지 않음) |

`write_open`(현재 `writes.py`):
- 열림: `PROCEDURE_WAITING` · `PROCEDURE` · `PROCEDURE_DONE` · `cancel-flow-tasks` · `change-tasks-room` · `change-tasks-complete` · 「방 배정」 `add-flow-tasks`
- 닫힘(False): `recept` · 시술권 `add-flow-tasks`(PROCEDURE) · `change-order-memo` · `CONSULTATION_WAITING` · `COMPLETED`

## 핵심 결론

### ⓐ 시술권 작업 본문

HAR #50 모양 그대로 200(`Seeder._procedure_task` 와 같은 본문)이다.

```
{scheduleId, tasks:[{type:"PROCEDURE", title,
  procedureConfiguration:{
    productOptionConfiguration{optionId, optionTitle, procedure{id,name,createDate}, unit, translsMap},
    ticketConfiguration{ticketId, round{total,current}},
    medicalServiceConfiguration{id, code, title, translsMap, unit, medicines[{id,name}], caution}},
  translsMap}]}
```

- 값은 `get-ticket-bundles` 묶음에서 가져온다. 옵션 칸은 `optionConfiguration`, 나머지는 `ticketSets[0]` 의 `title · procedure · unit · medicalService · translsMap`.
- `ticketId` 는 `tickets[]` 에서 `AVAILABLE` 인 것을 쓴다.
- 상세 `tasks[].procedureConfiguration.ticketConfiguration.ticketId` 가 보낸 값으로 다시 읽힌다(O). `round` 도 보낸 값 그대로 다시 읽힌다.
- 시술권 상태는 작업을 만들면 `AVAILABLE → IN_USE`, 작업을 `CANCEL` 하면 `IN_USE → AVAILABLE` 로 바로 바뀐다(2초 안).

ⓐ-1 ⚠ 지어낸 값 두 가지:
- **`round` 값**: ticket 에 회차 칸이 없다. HAR 은 1회권(`1/1`)뿐이라, `total = tickets 수`, `current = createdDateTimeUtc 순 위치 + 1` 로 넣었다. KOS 는 받아들였지만, KOS 화면이 보내는 값과 같은지는 확인하지 못했다(다회권 HAR 필요).
- **다회권 가격 나누기**: 다회 옵션의 `price` 에는 `amount` · `additional` 만 있다. `item_prices` 에 필요한 `suppliedAmount` · `vatAmount` 가 없다. 그래서 HAR 의 1회권 비율(440,000 = 400,000 + 40,000, 과세 10%)대로 `supplied = round(amount/1.1)` · `vat = 나머지` 로 나눠 보냈고 다섯 단계 모두 200 이었다. 다회권 수납 HAR 로 KOS 화면 값과 맞춰 볼 필요가 있다.
- 지금 `option_usable` 은 이 다회 옵션들을 모두 쓸 수 없는 옵션으로 본다.

### ⓑ 시술만 진행에 방 배정이 필요한가

필요 없다.
- `RECEPTION` 에서 「방 배정」 작업 없이 `PROCEDURE_WAITING` → `PROCEDURE` 까지 200 이었다.
- 시술 작업은 방이 없어 NOT_STARTED 로 남는다. 시술 현황에서 [호출] 하려면 그 작업에 방을 지정해야 READY 가 된다(Y 에서 확인: 방을 지정하면 NOT_STARTED → READY).

### ⓒ 시술 중 귀가 순서 · 시술권 회차

1. 안 끝난 작업이 남아 있으면 내부 `COMPLETED` 는 400 `procedures NotAvailable` 이다.
2. 안 끝난 작업 전부를 `cancel-flow-tasks {sequences:[…], reason:"CANCEL"}` 로 취소하면 200 이다.
3. 그 뒤 내부 `COMPLETED` 가 200 이다.
4. 작업을 `CANCEL` 하면 그 작업이 쓰던 시술권 회차가 `AVAILABLE` 로 **되돌아간다**. 회차가 줄지 않는다.
5. 취소된 작업은 상세에 `CANCELED` 로 남는다(`ticketId` 칸도 남음).
6. `paymentRequired` 는 이번 작업 모두 `false` 였다(시술권으로 만든 작업). true 인 경우는 보지 못했다.

### ⓓ 귀가 대기 → 귀가

- 「방 배정」과 시술 작업을 `CANCEL` 한 뒤 내부 `PROCEDURE_DONE` → 내부 `COMPLETED` 가 모두 200 이다. 끝 상태는 `reservation.status=COMPLETED` 다.
- ⚠ 시술 작업을 「완료」(`DONE`)로 만들지 못했다:
  - `change-tasks-complete complete:true` 는 NOT_STARTED 에서도, 방을 지정한 READY 에서도 400 `complete NotAvailable` 이었다.
  - 코디 지시대로 호출 연쇄(`change-tasks-assignees` → `call-tasks-doctors` → `change-tasks-doctors`)는 하지 않았다. 「완료」에 이 연쇄(의사 수락, 또는 작업 진행 상태)가 먼저 필요한지는 **확인하지 못했다**.
  - 그래서 Y 는 작업 완료가 아니라 「전부 CANCEL → PROCEDURE_DONE → COMPLETED」(코디 ③)로 끝냈다. 시술권도 소모되지 않고 AVAILABLE 로 돌아왔다.
  - 「시술한 회차가 실제로 USED 등으로 바뀌는지」는 이번에 보지 못했다.

## DAY `writes.py` 에 열 때 필요한 것(후보 · 결정 아님)

| 동작 | 경로 · 본문 | 값 조건 후보 | 확인 조건 후보 |
|---|---|---|---|
| 접수 | `schedule/v1/commands/recept {scheduleId}` | — | `flowStep=RECEPTION` · `reservation.status=IN_PROGRESS` |
| 시술권 작업 | `add-flow-tasks` `type=PROCEDURE` + ⓐ 본문 | `ticketId` 가 그 고객 `get-ticket-bundles` 에서 `AVAILABLE` | 새 작업 `ticketConfiguration.ticketId == 보낸 값`(1초쯤 늦게 보임). 지금 `_is_room_assign_body` 만 열려 있어 따로 열어야 함 |
| 오더 메모 | `schedule/v1/commands/change-order-memo {scheduleId, orderMemo}` | 글 전체(덮어쓰기) | 상세 `orderMemo == 보낸 값`(바로 보임) |
| 시술 대기 | 내부 `change-flow-step PROCEDURE_WAITING` | 이미 열림. `RECEPTION` 에서 방 배정 없이도 됨 | `flowStep` |
| 시술 대기 · 시술 진행 [귀가] | ① `cancel-flow-tasks {sequences: 안 끝난 전부, reason:CANCEL}` → ② 내부 `change-flow-step COMPLETED` | ②는 ① 확인 뒤(먼저 보내면 400 `procedures`) | ① 작업 `canceled` · ② `flow_step=completed`. 시술권 회차는 `AVAILABLE` 로 되돌아감(DAY 가 따로 되돌릴 것 없음) |
| 귀가 대기 [귀가] | 내부 `change-flow-step COMPLETED` | `PROCEDURE_DONE` 에서(작업이 모두 끝났거나 취소된 상태) | `flow_step=completed` |
| 공통 | `COMPLETED` 를 `OPEN_STEPS` 에 넣는 것 | 안 끝난 작업이 남은 상태에서 단독으로 보내지 않게, 순서를 outbox 에서 묶어야 함 | — |

미결(코디 · 사용자 판단):
1. `change-tasks-complete true` 가 되는 작업 상태. 호출 연쇄가 필요한지는 이번에 시험하지 않음.
2. 다회권 `round` 값과 가격 나누기를 KOS 화면 HAR 로 확인하는 것.
3. 시술 중 귀가 때 시술권 회차를 되돌리는 것(KOS 의 CANCEL 동작)이 제품 의도와 맞는지.

## 규칙 위반 · 주의

- Y 첫 예약 16:00 → 400 뒤 **다른 시각(16:30)으로 1회 재시도**. 같은 요청 반복은 아님.
- 시술 작업 `complete` 는 코디 답에 따라 방 지정 뒤 1회만 더 보냈다. 그 밖에 자동 재전송은 없다.
- 7ⓐ · 8 첫 complete 의 「16초」는 확인 대기 시간(다시 읽기 반복)이다. KOS 응답 시간이 아니다.
- 1판 고객 `6b051a9e` 에는 사용자가 HAR 을 찍을 때 만든 기존 시술권 묶음 2개가 있다(`219d079f` IN_USE · `7cf0722c` AVAILABLE). 손대지 않았다.
