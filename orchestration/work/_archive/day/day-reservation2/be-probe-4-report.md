# [backend · 실물 확인 4] 리포트 — 상담사 지정(상담 기록) · 시술만 진행 관리실 배정 연쇄

- 데모 지점 확인(`check_open_key_is_demo`) 통과 뒤에만 썼다.
- 호출은 전부 DAY `KosClient.internal()`. 레포 수정 · 커밋 없음. 값 · 토큰 · 개인정보 출력 없음.
- 고객: 시험 고객 `6b051a9e`.
- 이번에 만든 것(코디 추가 P′ `5e5948bd` 18:00 포함 — 아래 「접수 뒤 의사 지정」):
  - 오늘 예약 P `40ee69dc`(17:00) · Q `254d49b2`(17:30). 둘 다 끝 상태 `flowStep=COMPLETED` · `reservation.status=COMPLETED`.
  - 상담 기록 2건(P 에 붙음 · `02669787` · `ede6a26f`).
- 상담 직원: 활성 「상담총괄실장」 두 명. c1 = `6a793faa`, c2 = `6a8ce6a4`.
- 스크립트: `/private/tmp/day-probe-4/`
  - `probe4.py` · `extra.py`(코디 추가)
  - `p3lib.py` · `pcommon.py`(3판 것)
  - `run.out` · `log.md` · `state.json`

## 표

| # | 경로(끝 이름) | 응답 | O / X | 비고 |
|---|---|---|---|---|
| P1 예약 · 접수 · 방 배정 · 방 · 상담 대기 | `reserve` · `recept` · `add-flow-tasks ETCETERA` · `change-tasks-room` · 내부 `change-flow-step CONSULTATION_WAITING` | 모두 200 | O | 2판과 같음. 이때 상세 `consultations[]` 는 빈 배열, `consultation{consultationMemo, counselor, doctor}` 의 `counselor` 는 비어 있음 |
| P2 상담사 지정 | `consultation/v1/commands/create-consultation` `{consultationId(새 uuid), visitorId, consultationStartedDateTimeUtc(=일정 시작), scheduleId, content{text:""}, counselorIds:[c1]}` | 200(`{}`) | O | 아래 「P2 다시 읽기」 |
| P3ⓐ 상담사 바꾸기 | `consultation/v1/commands/change-consultation-counselors {consultationId, counselorIds:[c2]}` | 200 | O | 같은 기록 `02669787` 의 상담사가 c1 → **c2**. 기록 수는 1 그대로. 상세 `consultation.counselor` 도 c2 |
| P3ⓑ 같은 id 로 다시 만들기 | — | (안 함) | — | ⓐ 길이 있어서 브리프대로 건너뜀 |
| P3ⓒ 새 id 로 하나 더 만들기 | `create-consultation`(새 `consultationId` · c1) | 200 | O | 기록이 **둘**이 된다(`02669787` c2 · `ede6a26f` c1). 상세 `consultation.counselor` 는 c2(첫 기록 것)로 남음 |
| P4 귀가 | `cancel-flow-tasks [1] CANCEL` → 내부 `COMPLETED` | 200 · 200 | O | `COMPLETED`. 상담 기록 2건 그대로 남음(상담사 · scheduleId 그대로) |
| **접수 뒤 의사 지정**(코디 추가) | `schedule/reservation/v2/commands/update-reservation {scheduleId, occupiedResources:{items:[{id: 기존 자원 id, type, reservationTime: 기존 시작 · 끝, reservationGroup{reservationGroupId: 기존, zoneId, doctors:[{id,name}]}}]}}`(1판 5-3 모양) | 200 | **O** | 아래 「접수 뒤 의사 지정 다시 읽기」 |
| Q5a 예약 · 접수 | `reserve` · `recept` | 200 · 200 | O | `RECEPTION` |
| Q5b 「방 배정」 작업 | `add-flow-tasks ETCETERA` | 200 | O | seq1 NOT_STARTED |
| Q5c 방 지정 | `change-tasks-room` seq1 | 200 | O | seq1 → READY |
| Q5d 시술권 작업 | `add-flow-tasks PROCEDURE`(3판 본문) | 200 | O | seq2 NOT_STARTED · `ticketId` `abc48d58` · `round {total:3, current:3}`(D48. 아래 주의 1) |
| Q5e 시술 작업에 같은 방 | `change-tasks-room` seq2(seq1 과 같은 방) | 200 | O | seq2 **NOT_STARTED → READY** |
| Q5f 오더 메모 | `change-order-memo` | 200 | O | 상세 `orderMemo` 이 보낸 값과 같음 |
| Q5g 시술 대기 | 내부 `change-flow-step PROCEDURE_WAITING` | 200 | O | `RECEPTION → PROCEDURE_WAITING` |
| Q5 최종 읽기 | `get-schedule-detail` | — | O | `flowStep=PROCEDURE_WAITING`. 작업 둘 다 `READY` · 같은 방 · `roomAssignedDateTimeUtc` · `readyDateTimeUtc` 있음. 시술권 `abc48d58` AVAILABLE → IN_USE |
| Q6 정리 | `cancel-flow-tasks [1,2] CANCEL` → 내부 `COMPLETED` | 200 · 200 | O | 둘 다 CANCELED → `COMPLETED`. `abc48d58` IN_USE → **AVAILABLE** |

### P2 다시 읽기(1초 뒤와 4초 뒤가 같음)

| 읽는 자리 | 결과 |
|---|---|
| `flowStep` | **`CONSULTATION_WAITING` 그대로**(`CONSULTATION` 으로 안 감) · `reservation.status=IN_PROGRESS` |
| 상세 `consultations[]` | 1건 `02669787` · `counselors=[c1]`(바로 보임) |
| 상세 `consultation.counselor` | c1(`consultations[0]` 을 비춘 칸으로 보임) |
| 상세 `reservation.counselor` | 비어 있음(2판 `update-reservation counselor` 자리와 다름) |
| `get-consultations-by-visitor-id {visitorId}` | 이 일정의 기록 1건 · c1. 행 키 = `id · visitor · scheduleId · consultationStartedDateTimeUtc · counselors · consultationDoctors · consultationProcedures · content · createdDateTimeUtc · updatedDateTimeUtc`. 고객 전체 기록 수 1 → 2(1건은 사용자가 HAR 을 찍을 때 만든 기존 기록) |
| DAY `mapper.consultation(row)` | 상세 `consultations[]` 를 그대로 넣으면 `counselor_external_id = c1`. `single()` 은 상담사가 한 명일 때만 채운다 |

### 접수 뒤 의사 지정 다시 읽기(코디 추가)

P 는 이미 `COMPLETED` 였다. 그래서 같은 고객으로 새 오늘 예약 **P′ `5e5948bd`**(18:00)를 만들었다. 본문의 지정 의사는 D1 = `6a955c10`(원장)이다.

1. 접수 `recept` → 200. `flowStep=RECEPTION` · `reservation.status=IN_PROGRESS`(상담 대기 전).
2. `update-reservation` 으로 지정 의사를 D1 → D2(다른 활성 「원장」)로 바꿨다.
3. 정리: 작업이 없는 `RECEPTION` 에서 내부 `COMPLETED` → 200. 끝 상태 `COMPLETED` · `COMPLETED`.

| 칸 | 접수 뒤(전) | update 뒤 | 
|---|---|---|
| `occupiedResources[0].reservationGroup.doctors` | D1 | **D2**(바로 보임 · 다시 읽기 1회째) |
| `occupiedResources` 수 · 자원 id | 1 · `137e4b10` | 1 · `137e4b10`(같음) |
| 시작 시각 · 예약 그룹 | 18:00 · 기존 | 그대로 |
| `flowStep` · `reservation.status` | RECEPTION · IN_PROGRESS | **그대로**(접수가 풀리지 않음) |
| 담당자 · 예약 메모 · 유입 상세 | O | O(지워지지 않음) |
| `reservation.doctor` | 비어 있음 | 비어 있음(1판과 같음 · 의사는 ⓑ 자리에만) |

→ 접수 뒤에도 1판 5-3 모양 그대로 지정 의사를 바꿀 수 있다. 접수 상태와 다른 칸은 바뀌지 않는다.

덤으로 본 것: 작업이 없는 접수 상태에서는 내부 `COMPLETED` 가 바로 200 이다. 400 `procedures` 는 안 끝난 작업이 있을 때만 난다.

## 결론

### ⓐ 상담사 지정이 단계를 바꾸나

바꾸지 않는다.
- `create-consultation` 뒤에도 `flowStep` 은 `CONSULTATION_WAITING` 그대로다.
- 상담 기록만 생긴다. 상세 `consultations[]` 에 바로 보이고, `consultation.counselor` 에도 보인다.
- [상담 시작](`CONSULTATION`)은 따로 `change-flow-step` 으로 보내야 한다. 2판에서 `CONSULTATION` 단계 이동은 상담 기록을 만들지 않았다.

### ⓑ 상담사 바꾸기 길

`consultation/v1/commands/change-consultation-counselors {consultationId, counselorIds:[…]}` 로 200 이고, 같은 기록에서 덮어쓴다.

출처: KOS 웹 클라이언트 JS(`reservation-client_v0.0.541.js`). HAR `kknaks_profile/reference/2026-10-23-cc-overall-board/har/예약그룹.har` #35 응답 본문에 들어 있다.
- 화면 쪽 사용처 코드는 `schedule.consultations.at(0)` 의 `id` 에 `counselorIds: counselor ? [counselor.id] : []` 를 보낸다. 곧 **일정의 첫 상담 기록**을 고친다.
- 오류 매핑은 `consultationId NotFound` · `counselorIds[n] NotAvailable` · `counselorIds Required(atLeastOneAssignee)` 다. 빈 배열은 「최소 한 명」 오류일 수 있다(시험 안 함).
- 같은 JS 에 `change-consultation-information {consultationId, consultationStartedDateTimeUtc, content, counselorIds, doctorIds, result}` · `remove-consultation {consultationId}` · `change-consultation-doctors` 도 있다(시험 안 함).
- KOS openapi(`2026-09-18`) · DAY 코드 · cc 코드에는 이 명령들이 없다. DAY 는 공개 `update-schedule-consultation-info`(상담 메모)만 쓴다.

### ⓒ 차티 [상담 시작]과 겹칠 위험(관찰한 만큼)

- `create-consultation` 을 새 `consultationId` 로 또 보내면 **같은 일정에 기록이 둘** 생긴다. KOS 는 막지 않았다(200).
- 그 뒤 상세 `consultation.counselor` 는 첫 기록의 상담사를 보여 준다.
- 그래서 차티(또는 KOS 화면)가 [상담 시작] 때 따로 기록을 만들면, DAY 가 지정한 기록과 두 건이 될 수 있다. 차티가 실제로 기록을 만드는지는 이번에 보지 않았다.
- DAY 가 겹침을 피하려면:
  - 지정 전에 그 일정 `consultations[]` 가 비었는지 본다.
  - 있으면 `change-consultation-counselors` 로 첫 기록을 고친다(KOS 화면과 같은 규칙).
- DAY 쪽 읽기: `mapper.consultation` 이 기록마다 매핑하므로 둘이면 둘 다 들어온다. 어느 기록의 상담사를 「예약 상담사」로 보일지는 정해야 한다. KOS 화면은 `consultations[0]` 를 쓴다.
- 귀가(`COMPLETED`) 뒤에도 상담 기록은 지워지거나 닫히지 않고 그대로 남는다. 「상담 종료」 칸은 보지 못했다(행 키에 없음).

### ⓓ 시술만 진행 연쇄

브리프 순서 한 번으로 전부 200 이었다.

1. 「방 배정」 작업
2. 방 지정
3. 시술권 작업
4. 그 시술 작업에 같은 방 지정
5. 오더 메모
6. `PROCEDURE_WAITING`

- 시술 작업도 방을 지정하면 **NOT_STARTED → READY** 가 된다(`roomAssignedDateTimeUtc` · `readyDateTimeUtc` 채워짐).
- 최종 상태: 작업 둘 다 READY · 같은 방 · `flowStep=PROCEDURE_WAITING`.
- 정리에서 작업 둘을 `CANCEL` 하면 시술권이 AVAILABLE 로 돌아온다(3판과 같음).

## DAY `writes.py` 에 열 때 필요한 것(후보 · 결정 아님)

| 동작 | 경로 · 본문 | 값 조건 후보 | 확인 조건 후보 |
|---|---|---|---|
| 상담사 지정(기록 없을 때) | `consultation/v1/commands/create-consultation {consultationId: 새 uuid, visitorId, consultationStartedDateTimeUtc: 일정 시작, scheduleId, content{text:""}, counselorIds:[id]}` | 그 일정 `consultations[]` 가 비어 있을 때만. `consultationId` 는 DAY 가 만든 uuid(멱등 키로 쓸 수 있음). 같은 id 로 다시 보내면 어떻게 되는지는 시험 안 함 | 상세 `consultations[]` 에 그 `id` · `counselors == [id]`(바로 보임) |
| 상담사 바꾸기(기록 있을 때) | `consultation/v1/commands/change-consultation-counselors {consultationId: consultations[0].id, counselorIds:[id]}` | 상담사 1명(덮어쓰기). 빈 배열(지정 해제)은 시험 안 함 | 그 기록 `counselors == [id]` |
| 시술 작업 방 지정 | `change-tasks-room {scheduleId, sequences:[시술 seq…], roomId}` | 이미 열림. 「방 배정」과 같은 방 · 여러 seq 를 한 번에 보낼 수 있는지는 시험 안 함(이번엔 seq 마다 따로) | 작업 `room_external_id` · status READY |
| 시술만 진행 [시술 대기] | 「방 배정」 add → 방 → 시술권 add(들) → 시술 작업 방 → `change-order-memo` → `change-flow-step PROCEDURE_WAITING` | outbox 에서 순서를 묶는다. `PROCEDURE_WAITING` 은 이미 열림. 시술권 `add-flow-tasks` · `change-order-memo` · `recept` 는 아직 닫혀 있음 | 마지막 `flow_step=procedure_waiting` + 작업마다 READY |
| 접수 뒤 지정 의사 바꾸기 | `update-reservation {scheduleId, occupiedResources:{items:[기존 자원 id · 시간 · 그룹 + doctors]}}` | 기존 자원 id · 시간 · 그룹을 그대로 다시 실어야 함(1판 모양) | `occupiedResources[0].reservationGroup.doctors == [새 의사]` · `flowStep` 그대로 |
| 동기화 | `mapper.consultation` 은 이미 `counselors` 를 읽는다 | 기록이 둘 이상일 때 화면에 어느 것을 보일지 정해야 함(KOS 화면 = 첫 기록) | — |

## 주의

1. **시술권 상태가 이번 실행 밖에서 바뀌어 있었다**:
   - Q 를 만들기 전 `get-ticket-bundles` 에서 3판 시술권 3장 중 `469735eb` · `9bf521e8` 이 **IN_USE** 였다. 3판이 끝날 때는 셋 다 AVAILABLE 이었다. D48 HAR(`시술권사용.har`) 을 찍으면서 생긴 것으로 보인다.
   - D48 규칙(목록 순 첫 AVAILABLE · `current = 쓰는 중 / 쓴 수 + 1`)대로 `abc48d58` · `current 3` 을 썼다.
   - 정리 뒤 `abc48d58` 만 AVAILABLE 로 돌아왔다. 나머지 두 장(IN_USE)은 손대지 않았다.
2. 고객의 상담 기록은 3건이 남는다. 이번 것 2건 · 기존(HAR) 1건. 지우는 명령(`remove-consultation`)은 브리프 밖이라 쓰지 않았다.
3. 같은 요청 재시도 · 자동 재전송 없음. 모든 단계가 첫 시도에 200 이었다.
