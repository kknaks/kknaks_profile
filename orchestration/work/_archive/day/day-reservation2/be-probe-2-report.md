# be-probe-2 결과 보고 — KOS 데모 지점 실물 확인 2 (접수 · 상담 대기 · 상담사 / 관리실 · 귀가)

## 상태: done

- 실행일: 2026-11-24 오후(KST) · DAY `KosClient` 그대로 · 데모 지점 확인(`check_open_key_is_demo`) **통과 뒤에만** 썼다
- 고객 = 1 의 시험 고객 `6b051a9e…` 만 · 예약 = 오늘 빈 칸에 새로 2건: **A `374dc0e2…`(15:00)** · **B `0bb85202…`(15:30)** · 다른 예약이 쓰지 않는 방만 골랐다
- 레포 수정 · 커밋 없음(`git status` 깨끗). 값 · 토큰 · 개인정보 출력 없음
- **최종: A · B 모두 `flowStep = COMPLETED` · `reservation.status = COMPLETED`**(판에 걸려 있지 않음). 정리는 코디 답(② · ① · ③)대로 했다(§정리)

## 요약 표

| 시험 | 경로 | 응답 | 들어갔나 | 비고 |
|---|---|---|---|---|
| 1 오늘 예약(A) | 내부 `schedule/reservation/v2/commands/reserve` | 200 | O | 1 과 같은 본문 + 지정 의사를 ⓑ 자리에(6 의 덮어쓰기 확인용). 담당자 · 유입은 약 1초 뒤에 보임 |
| 2 접수 | 내부 `schedule/v1/commands/recept {scheduleId}` | 200 | O | `flowStep RESERVED → RECEPTION`(≤0.1s) · `reservation.status RESERVED → IN_PROGRESS` · `receptionDateTimeUtc` 채워짐 |
| 3 「방 배정」 작업 | 내부 `schedule/v1/commands/add-flow-tasks` | 200 | O | `write_open` 통과 모양 · 새 작업 seq 1 · `ETCETERA` · `NOT_STARTED` · 방 없음(≈1s 뒤 보임) |
| 4 방 지정 | 내부 `schedule/flow/v1/commands/change-tasks-room` | 200 | O | 작업 방 = 고른 방 · 상태 **`NOT_STARTED → READY`**(≤0.1s) |
| 5 상담 대기 | 내부 `schedule/v1/commands/change-flow-step {id, step:"CONSULTATION_WAITING"}` | 200 | O | ≈1s · **지금 `write_open` 은 이 값을 막는다(False)** |
| 6 상담사 바꾸기 | 내부 `schedule/reservation/v2/commands/update-reservation {scheduleId, counselor}` | 200 | O | `reservation.counselor` 에 들어감 · `consultation.counselor` 는 빈 값. **다른 칸은 지워지지 않음**(전부 O) |
| 7 관리실 바꾸기 | 내부 `change-tasks-room`(다른 방) | 200 | O | ≈1s · 작업 `READY` 유지 · `flowStep` 그대로 |
| 8 상담 대기에서 귀가 | 내부 `change-flow-step {id, COMPLETED}` → 공개 `schedule/open/v1/commands/change-flow-step {scheduleId, COMPLETED}` | **400 / 400** | X | 둘 다 `InvalidRequestException` · `errorProperties [{key:"procedures", reason:"NotAvailable"}]` — 열린 「방 배정」 작업(READY) 때문 |
| 9 예약 B 연쇄 | 1 ~ 5 와 같음 | 200 ×5 | O | A 와 같은 결과 · 같은 지연 |
| 10 상담 진행 | 내부 `change-flow-step {id, step:"CONSULTATION"}` | 200 | O | ≈1s · `flowStep = CONSULTATION` · 작업 `READY` 그대로 · `consultations` 는 빈 목록 그대로 |
| 11 상담 진행에서 귀가 | 8 과 같음 | **400 / 400** | X | 8 과 같은 오류(`procedures NotAvailable`) |
| 12 정리 · 취소 | 공개 `schedule/open/v1/commands/cancel-reservation {reason:"CANCELED"}` | **400** | X | 접수 뒤에는 취소 안 됨 · `errorProperties [{key:"status", reason:"NotAvailable"}]` → 코디 답대로 작업을 먼저 닫음(아래) |
| 정리 A ② | 내부 `schedule/v1/commands/cancel-flow-tasks {reason:"CANCEL"}` → 내부 `COMPLETED` | 200 → 200 | O | 작업 `CANCELED`(방은 그대로) → `flowStep COMPLETED` · `status COMPLETED` |
| 정리 B ① | 내부 `schedule/flow/v1/commands/change-tasks-complete {complete:true}` | **400** | X | `[{key:"complete", reason:"NotAvailable"}]`(상담 단계의 「방 배정」 READY 작업은 완료 처리가 안 됨) |
| 정리 B ③ | 내부 `cancel-flow-tasks {reason:"DELETE"}` → 내부 `COMPLETED` | 200 → 200 | O | 작업이 상세에서 사라짐 → `flowStep COMPLETED` · `status COMPLETED` |

## 핵심 결론

- **ⓐ `COMPLETED` 는 내부 경로(`{id, step}`)에서 된다.** 단 **열린 작업이 없을 때만**이다. 「방 배정」 작업이 READY 면 내부 · 공개 둘 다 400 `procedures NotAvailable`. 작업을 닫자 내부 `COMPLETED` 가 바로 200 · ≈1s 뒤 반영(A · B 모두). 공개 경로는 작업이 열렸을 때만 시험됐고(400), 닫은 뒤에는 시험하지 않았다(내부가 먼저 통과)
- **ⓑ 귀가는 「방 배정」 작업을 알아서 닫아 주지 않는다.** [귀가 처리] = 작업 닫기 → `COMPLETED` 두 단계가 필요하다
  - `cancel-flow-tasks CANCEL` → 작업이 `CANCELED` 로 남음(방 id 남음 · `completedDateTimeUtc` 없음)
  - `cancel-flow-tasks DELETE` → 작업이 상세 `tasks` 에서 사라짐
  - `change-tasks-complete true` → 상담 단계에서는 400(`complete NotAvailable`)
  - 상담 칸: 귀가 뒤에도 `consultation` 은 `{consultationMemo, counselor, doctor}` 모양 그대로(counselor · doctor 빈 값). `consultations` 는 처음부터 끝까지 빈 목록이었다. **API 로 `CONSULTATION` 단계에 넣어도 상담 기록은 생기지 않는다**(cc 주석 「상담 기록은 KOS [상담 시작]이 만든다」와 맞음). 그래서 「열린 채 / 닫힘」을 가를 상담 기록 자체가 없다
- **ⓒ `update-reservation {scheduleId, counselor}` 는 다른 칸을 덮어쓰지 않는다.** `occupiedResources` 없이 보냈는데 담당자 · 예약 그룹 · 시작 시각 · 지정 의사(ⓑ 자리) · 메모 · 유입 · 유입 상세가 모두 그대로였다(칸마다 O). 1 의 「바꾸지 않는 칸도 다시 실어야」는 **`occupiedResources` 안**(items 통째)에 한정된 이야기로 보인다. 최상위 칸은 보낸 것만 바뀐다
- 접수(`recept`)는 `reservation.status` 도 `IN_PROGRESS` 로 바꾼다. 귀가 뒤 `status = COMPLETED`. 1 의 취소(`CANCELED`)와 같은 자리다
- 접수 뒤 예약은 `cancel-reservation` 이 막힌다(`status NotAvailable`). 정리는 귀가 쪽으로만 할 수 있다

## 단계별 본문 · 응답 키 모양

| 단계 | 요청 키 | 응답 키 |
|---|---|---|
| reserve | `{visitorId, zoneId, occupiedResources[{id, type, reservationTime{start,end}, reservationGroup{reservationGroupId, zoneId, doctors[{id,name}]}}], reservationAssignee{id,name}, reservationMemo, funnel{funnel{id,category,name,order,closed,default}, funnelDetail}}` | `{scheduleId}` |
| recept | `{scheduleId}` | `{}` |
| add-flow-tasks | `{scheduleId, tasks[{type:"ETCETERA", title, etceteraConfiguration{etceteraTaskId, name, translsMap{name{}}}, translsMap{title{}}}]}`(1개) | `{}` |
| change-tasks-room | `{scheduleId, sequences[int], roomId}` | `{}` |
| change-flow-step(내부) | `{id, step}` | `{}` |
| change-flow-step(공개) | `{scheduleId, step}` | (400 만 받음) |
| update-reservation | `{scheduleId, counselor{id, name}}` | `{}` |
| cancel-flow-tasks | `{scheduleId, sequences[int], reason}` | `{}` |
| change-tasks-complete | `{scheduleId, sequences[int], complete}` | (400 만 받음) |
| cancel-reservation | `{scheduleId, reason:"CANCELED"}` | (400 만 받음) |
| 400 공통 | — | `{className, errorProperties[{key, reason}], message, properties, status}` · `className = InvalidRequestException` |

상세 작업 행 키: `anesthesiaType, assigneeMemo, assignees, calledDoctors, completedDateTimeUtc, doctorCallDateTime, doctorMemo, doctors, etceteraConfiguration, memo, order, paymentRequired, procedureConfiguration, readyDateTimeUtc, room, roomAssignedDateTimeUtc, sequence, status, title, translsMap, type, urgencyLevel`

다시 읽기 지연: recept · change-tasks-room 은 ≤0.1s. add-flow-tasks · change-flow-step · update-reservation · cancel-flow-tasks 는 ≈1s(첫 읽기에 없고 1초 뒤 읽기에 있음). reserve 뒤 담당자 · 유입은 ≈1s.

## DAY `writes.py` 에 열 때 필요한 것 (후보 — 결정 아님)

| 동작 | api · 경로 | 값 조건 후보 | 확인 조건 후보 |
|---|---|---|---|
| [접수] | internal `schedule/v1/commands/recept` | `{scheduleId}` · 오늘 · 지금 `RESERVED` | `flowStep == RECEPTION` · `reservation.status == IN_PROGRESS` |
| [상담 대기] 1 | internal `add-flow-tasks`(이미 열림 · 「방 배정」 하나) | 그대로 | 새 seq 의 `ETCETERA` 작업(≈1s 지연) |
| [상담 대기] 2 | internal `change-tasks-room`(이미 열림) | 그대로 | 작업 방 = 고른 방 · 상태 `READY` |
| [상담 대기] 3 | internal `change-flow-step` | **`step = CONSULTATION_WAITING` 을 `OPEN_STEPS` 에 더해야 함**(지금 막힘) | `flow_step == consultation_waiting` |
| (상담 진행) | internal `change-flow-step` | `step = CONSULTATION`(쓸 경우 · 지금 막힘) | `flowStep == CONSULTATION` · 상담 기록은 생기지 않음 |
| 상담사 바꾸기 | internal `schedule/reservation/v2/commands/update-reservation` | 본문이 **`{scheduleId, counselor{id,name}}` 둘만**일 때만 열기(`occupiedResources` 가 섞이면 덮어쓰기 위험) | `reservation.counselor.id == 고른 직원`(`consultation.counselor` 아님) |
| 관리실 바꾸기 | internal `change-tasks-room`(이미 열림) | 상담 대기 「방 배정」 작업 seq | 작업 방 = 새 방 |
| [귀가 처리] 1 | internal `cancel-flow-tasks`(이미 열림) | 「방 배정」 seq · `reason = CANCEL`(작업이 `CANCELED` 로 남음) 또는 `DELETE`(사라짐) | 작업 `canceled` / `absent` |
| [귀가 처리] 2 | internal `change-flow-step` | **`step = COMPLETED` 를 더해야 함**(지금 막힘) · 열린 작업(READY · NOT_STARTED 등)이 없을 때만 보냄 | `flowStep == COMPLETED` · `reservation.status == COMPLETED` |

- 「귀가」 순서가 틀리면(작업이 열린 채 `COMPLETED`) KOS 가 400 `procedures NotAvailable` 를 준다. outbox 순서(작업 닫기 → 단계)와 확인 조건이 필요하다
- `change-tasks-complete true` 는 상담 단계의 「방 배정」 작업에 쓸 수 없다(400). 귀가 쪽 작업 닫기는 `cancel-flow-tasks` 로 해야 한다
- 귀가 뒤 작업을 `CANCELED` 로 남길지(방 기록 남음) `DELETE` 로 지울지는 제품 결정이다. 시술 현황판의 방 「사용 중」 계산에 어떤 영향이 있는지는 확인하지 않았다

## 이슈 · 코디가 확인할 것

1. 브리프 8 · 11 의 「바로 귀가」는 KOS 가 한 번에 받지 않는다. 작업 닫기 한 단계가 더 필요하다(위 표)
2. 정리 때 KOS 로 보낸 칸: A 는 ②(`cancel-flow-tasks CANCEL` → 내부 `COMPLETED`), B 는 ① 400 → ③(`DELETE` → 내부 `COMPLETED`). 둘 다 귀가 완료
3. 본 시험의 정리 단계(12)에서 취소 400 뒤 **대체로 `COMPLETED`(내부 · 공개)를 한 번 더 보냈다**. 8 · 11 과 같은 요청을 다시 보낸 셈이다(둘 다 같은 400). 코디에 묻기 전에 스크립트가 자동으로 한 것이다 — 규칙 「같은 요청 반복 금지」에 어긋남
4. 상담 진행(`CONSULTATION`)으로 넣어도 KOS 상담 기록이 생기지 않았다. DAY 가 상담 기록을 기대한다면 KOS [상담 시작] 화면 동작(HAR)이 따로 필요하다
5. 시험 고객 `6b051a9e…` 는 그대로 둠 · 오늘 예약 A · B 는 귀가 완료로 남아 있다(판에서 내려감)

## 시험 스크립트 (`/private/tmp/day-probe-2/`)

- `pcommon.py`(1 에서 복사 · 경로만 바꿈) · `probe2.py`(1 ~ 12) · `cleanup.py`(코디 답 정리 ② · ① · ③)
- `run.out` · `cleanup.out` · `log.md`(키 모양 · O/X · id 앞 8자) · `state.json`(단계별 결과 · 이름 · 개인정보 없음)
