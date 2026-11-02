# 접수 묶음 — 데모 실호출 시험 (데모 쓰기 허가 판)

- 시험일: 2026-10-26 (KST) · 05:30:11Z ~ 05:31:51Z · 시험자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-room-report.md`(아래 `RM§`)에서 이어진다. 허가: 지시서 §0(사용자 「데모 지점은 테스트 해봐도 돼」) · §2 목록만
- **테넌트 확인**: 호출 전에 다음을 확인했다
  - procedure `.env` 의 테넌트 id 가 앞 판 HAR 의 데모 테넌트 id 와 **같다**(스크립트 `assert`)
  - 공개 키 = `KOS_API_tenent_dev` 이고, 운영 키 `KOS_API_tenent` 와 **다르다**(`assert`). 운영 키 사용 0건
- 쓰기 가드: 스크립트가 허가 목록 6개 경로(`recept` · `add-flow-tasks` · `change-tasks-room` · 내부/공개 `change-flow-step` · `reserve`) 밖의 command 를 막았다
- 표기
  - **확인**: 이번에 데모에서 실제로 보낸 것 · 본 것
  - **추정**: 해석
- 리포트에 id · 토큰 · 이름 값은 적지 않았다(방 이름만 적는다)

---

## 0. 결론

- **A. ccc 묶음(접수 → 「방 배정」 작업 → 방 지정 → 상담 대기)은 시술 대기를 거치지 않고 4번 모두 200 이다**
  - **`change-tasks-room` 은 일정 단계가 `RECEPTION` 이어도 받는다**(확인)
  - 끝 상태(`CONSULTATION_WAITING` · `IN_PROGRESS` · 「방 배정」 `READY` + 방 + 배정 시각)는 KOS 화면 우회(RM§3)의 끝 상태와 **필드 모양이 같다**. 공개 `getScheduleDetail` 과 내부 `get-schedules-grouped-by-zone` · `get-schedule-detail` 셋 다 같았다
- **B. 공개 `changeFlowStep{scheduleId, step: RECEPTION}` 은 내부 `recept` 와 같은 결과를 냈다**: `flowStep RECEPTION` · `receptionDateTimeUtc` 기록 · `reservation.status RESERVED → IN_PROGRESS`
  - 차이는 반영 순서뿐이다. 공개는 응답 직후 단계 · 접수 시각이 먼저 보이고 예약 상태는 몇 초 뒤에 바뀌었다. 내부 `recept` 는 응답 직후에는 셋 다 이전 값이었고 몇 초 뒤 한꺼번에 바뀌었다
- **쓰기는 모두 응답 `{}`(200) 이고, 결과가 조회에 보이기까지 0 ~ 3초가 걸렸다.** 바로 다시 읽으면 이전 상태가 오는 경우가 있다(recept · add-flow-tasks · change-flow-step)
  - `change-tasks-room` 은 바로 보였다
- 대상 일정 · 끝 상태
  - A = 오늘 4층의 `RESERVED` · 작업 없음 일정 1건. 앞 판 `예약.har` #87 에서 사용자가 만든 기존 고객 예약이고, 그때 유일한 후보였다
  - B = 후보가 없어서 **시험용으로 만든 일정**(데모 기존 고객 · 내부 `reserve`)
  - 끝 상태: A `CONSULTATION_WAITING`, B `RECEPTION`. 둘 다 시술 대기가 아니다. 되돌리지 않았다
- 정할 것은 **6개**다(Q-73 ~ Q-78)

---

## 1. 시험 A — 내부 묶음 (대상: 오늘 4층 `RESERVED` · 작업 없음 일정)

시험 전 상태(공개 `getScheduleDetail`): `flowStep RESERVED` · `reservation.status RESERVED` · `receptionDateTimeUtc` 없음 · `tasks[]` 0 · `zone` 「4층」.

| 순서 | 호출(내부, 시스템 계정 Bearer) | 본문(모양) | 결과 코드 · 응답 | 바로 뒤 조회 | 몇 초 뒤 조회 |
|---|---|---|---|---|---|
| A1 | `POST /schedule/v1/commands/recept` | `{scheduleId}` | **200** `{}` | 0.1초: **안 바뀜**(`RESERVED` · `RESERVED` · 접수 시각 없음) | 수 초 뒤: `flowStep RECEPTION` · `reservation.status IN_PROGRESS` · `receptionDateTimeUtc` = 호출 시각 · `flowStepUpdatedDateTimeUtc` = 같은 시각 · `tasks[]` 0. 공개 상세 · 내부 상세 · 내부 grouped 셋이 같았다 |
| A2 | `POST /schedule/v1/commands/add-flow-tasks` | `{scheduleId, tasks:[{type:"ETCETERA", title:"방 배정", etceteraConfiguration{etceteraTaskId, name:"방 배정", translsMap}, translsMap}]}` — `etceteraTaskId` 는 `get-etcetera-tasks` 의 「방 배정」. 키 구성은 `방배정.har` #60 과 같다(스크립트로 비교) | **200** `{}` | 0.1초: 작업 0개 | 3.2초: 작업 1개 — `ETCETERA · sequence 1 · 「방 배정」 · NOT_STARTED · 방 없음`. 단계는 `RECEPTION` 그대로 |
| (조회) | 공개 `getScheduleDetail` | — | 200 | 「방 배정」의 sequence = **1** 을 확인 | — |
| A3 | `POST /schedule/flow/v1/commands/change-tasks-room` | `{scheduleId, sequences:[1], roomId}` — 방은 **A-룸7**(아래 메모) | **200** `{}` | 0.1초: **바로 보임** — 「방 배정」 `READY` · 방 A-룸7 · `roomAssignedDateTimeUtc` = `readyDateTimeUtc` = 호출 시각. **단계 `RECEPTION` 에서 받았다** | — |
| A4 | `POST /schedule/v1/commands/change-flow-step` | `{id, step:"CONSULTATION_WAITING"}` | **200** `{}` | 0.1초: 아직 `RECEPTION` | 3.2초: `CONSULTATION_WAITING` · `flowStepUpdatedDateTimeUtc` 갱신 · 작업 · 방 그대로 · `receptionDateTimeUtc` 그대로 |

방 고르기
- 직전에 내부 `get-schedules-grouped-by-zone`(4층 · 오늘)의 모든 작업 `room` 을 모았다. 쓰이던 방은 A-룸1 · A-룸2 · A-룸5 였다
- `get-rooms`(28개)에서 그 셋을 뺀 방 중 A-룸7 을 골랐다

A 끝 상태(공개 · 내부 3가지 조회 일치)

| 필드 | 값(모양) |
|---|---|
| `flowStep` | `CONSULTATION_WAITING` |
| `reservation.status` | `IN_PROGRESS` |
| `receptionDateTimeUtc` | 있음(A1 시각) |
| `tasks[]` | 1개 — `ETCETERA · seq 1 · 「방 배정」 · READY · room A-룸7 · roomAssignedDateTimeUtc · readyDateTimeUtc` |
| `zone` · `visitorLocation` | 「4층」 그대로 |

**KOS 화면 결과와 비교**(RM§3 끝 상태 = `방배정.har` 일정의 지금 상태)
- 같은 필드가 같은 모양이다: `CONSULTATION_WAITING` · `IN_PROGRESS` · 접수 시각 · 작업 1개 「방 배정」 `READY` + 방 + 배정 시각
- 다른 점은 시각 값과 방, 그리고 **KOS 우회는 중간에 `PROCEDURE_WAITING` 을 한 번 거쳤다는 것**뿐이다
- 일정 응답에 「지난 단계 이력」 필드는 없어서, 조회로는 두 경로를 구분할 수 없다
- 참고: 앞 판 HAR 일정의 방은 HAR 당시 A-룸9 였는데 지금은 A-룸5 다. 그 사이 누군가 방을 바꾼 것으로 보인다(이 시험과는 상관없다)
- KOS 웹 화면을 직접 열어 보지는 않았다(조회 API 로만 비교) → Q-78

---

## 2. 시험 B — 공개 `changeFlowStep(RECEPTION)` (대상: 시험용으로 만든 일정)

### 2.1 시험용 일정 만들기 (지시서 §2 의 「대상이 없으면」)

오늘 4층의 `RESERVED` 일정은 A 하나뿐이었다(공개 `getSchedulesByFlowStep(RESERVED)` = 1건). 그래서 하나를 만들었다.

| 순서 | 호출 | 본문(모양) | 결과 |
|---|---|---|---|
| B0 | 내부 `POST /schedule/reservation/v2/commands/reserve` | `{visitorId(데모 기존 고객 — 앞 판 설문 HAR 의 고객), zoneId(4층), occupiedResources:[{id(새 uuid), type:RESERVATION_GROUP, reservationTime{08:30Z ~ 09:00Z = 17:30 ~ 18:00 KST}, reservationGroup{「국내」 id, zoneId}}], reservationAssignee{id, name}}` — 키 구성은 `예약.har` #87 과 같다(스크립트로 비교) | **200** `{scheduleId}` · 3초 뒤 `RESERVED` · `RESERVED` · 작업 0 · 「4층」 |

- 그 칸은 미리 공개 `getReservationSlotsByGroupsV2` 로 봤다: 정원 3 · 예약 0
- **「시험용으로 만듦」**: 오늘 17:30 KST · 「국내」 · 데모 기존 고객 1명
- ⚠ `reservationAssignee` 에는 sign-in 응답의 `data.id · name` 을 넣었다. 그런데 이 id 는 공개 `getAccounts` 의 계정 id 목록에 **없다**(sign-in 의 id 는 계정 id 가 아니라 사용자 id 로 보인다, 추정). 내부 `reserve` 는 그대로 받았다. 일정에는 담당자 id · 이름이 보인다 → Q-75

### 2.2 B1 공개 단계 변경

| 순서 | 호출(공개, 데모 키 토큰) | 본문 | 결과 | 바로 뒤 | 몇 초 뒤 |
|---|---|---|---|---|---|
| B1 | `POST /schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"RECEPTION"}` | **200** `{}` | 0.1초: `flowStep RECEPTION` · `receptionDateTimeUtc` = 호출 시각 · `flowStepUpdatedDateTimeUtc` = 같은 시각 · **`reservation.status` 는 아직 `RESERVED`** | 다음 조회: **`reservation.status IN_PROGRESS`**. 공개 상세 · 내부 상세 · 내부 grouped 셋이 같았다 |

B 끝 상태: `RECEPTION` · `IN_PROGRESS` · 접수 시각 있음 · 작업 0. 되돌리지 않았다.

### 2.3 내부 `recept` ↔ 공개 `changeFlowStep(RECEPTION)`

| | 내부 `recept{scheduleId}` (A1) | 공개 `changeFlowStep{scheduleId, step:RECEPTION}` (B1) |
|---|---|---|
| `flowStep` | → `RECEPTION` | → `RECEPTION` |
| `receptionDateTimeUtc` | 기록 | **기록** |
| `reservation.status` | → `IN_PROGRESS` | **→ `IN_PROGRESS`**(조금 늦게) |
| 구역 · 작업 | 그대로 | 그대로 |
| 반영 | 응답 직후는 셋 다 이전 값 → 수 초 뒤 함께 | 단계 · 접수 시각은 바로, 예약 상태는 수 초 뒤 |
| 접수 직원 | 일정에 필드 없음 | 같음 |

→ 이번 데모 한 건씩 비교한 결과, **조회로 보이는 필드의 결과는 같다.** 둘이 KOS 안에서 같은 처리인지(알림 · 이력 · 통계)는 조회로 알 수 없다 → Q-73

---

## 3. 호출 기록

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| **쓰기 · 내부** | `schedule/v1/commands/recept` | 1 | 200 |
| | `schedule/v1/commands/add-flow-tasks` | 1 | 200 |
| | `schedule/flow/v1/commands/change-tasks-room` | 1 | 200 |
| | `schedule/v1/commands/change-flow-step` | 1 | 200 |
| | `schedule/reservation/v2/commands/reserve`(B 시험용 일정) | 1 | 200 |
| **쓰기 · 공개** | `schedule/open/v1/commands/change-flow-step` | 1 | 200 |
| 조회 · 공개 | `get-schedule-detail` 17 · `get-schedules-by-flow-step` 2 · `get-accounts` 2 · `get-reservation-slots-by-groups` 1 | 22 | 모두 200 |
| 조회 · 내부 | `get-schedules-grouped-by-zone` 8 · `schedule/v1/queries/get-schedule-detail` 5 · `get-rooms` 2 · `get-etcetera-tasks` 2 | 17 | 모두 200 |
| 인증 | 공개 `exchange-token` 11 · 내부 sign-in 10 | 21 | 모두 200 |

- **쓰기는 6건이고, 각각 1회씩 보냈다.** 실패나 재시도는 없었다
- 허가 목록 밖 쓰기 0건 · 운영 키 0건
- 합계 66회(스크립트 호출 로그로 셌다)
- 일정 2개 모두 시술 대기(`PROCEDURE_WAITING`)로 둔 적이 없다. A 는 `RECEPTION` → `CONSULTATION_WAITING` 으로 바로 갔다
- 남긴 것
  - A: 오늘 4층 · `CONSULTATION_WAITING` · 「방 배정」 A-룸7
  - B: 오늘 4층 · 17:30 KST · `RECEPTION` · 작업 없음(시험용으로 만듦)

---

## 4. 정할 것 (결정하지 않음) — 6개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-73 | 접수를 공개 `changeFlowStep(RECEPTION)` 으로 할지 내부 `recept` 로 할지 | 이번 시험에서는 보이는 결과(단계 · 접수 시각 · `IN_PROGRESS`)가 같았다. KOS 안의 다른 효과(알림 · 이력 · 통계)는 조회로 비교할 수 없다 | RM Q-63 |
| Q-74 | 쓰기 뒤 반영 지연(0 ~ 3초) | 바로 다시 읽으면 이전 상태가 온다. 묶음 중간에 sequence 를 확인하려면 다시 읽는 간격 · 횟수가 필요하다(이번에는 3초 간격으로 읽어 두 번째에 보였다). 시술 현황의 「KOS 반영 중」 처리와 같은 규칙을 쓸지 | RM Q-64 · Q-65 |
| Q-75 | 예약 담당자 id | sign-in 의 `data.id` 는 계정 목록(`getAccounts`)에 없는 id 인데 내부 `reserve` 가 받았다. 시스템 계정의 계정 id 를 따로 찾아 넣을지, 담당자를 비울지 | C Q-60 |
| Q-76 | 접수 묶음의 끝 단계 | 이번에는 상담 대기로 끝냈다(지시). 「바로 시술」 경로라면 시술 대기로 올려야 하는데, 그러면 시술 현황 카드가 바로 생긴다 | RM Q-68 |
| Q-77 | 방 「사용 중」 판정 | 이번에는 오늘 4층 일정의 모든 작업 `room` 을 모아 뺐다. 끝난 일정 · 취소된 작업의 방도 「사용 중」으로 칠지 정의가 필요하다 | RM Q-70 · R Q-16 |
| Q-78 | KOS 웹 화면 눈 확인 | 조회 API 로는 KOS 우회와 같은 모양이었다. KOS 웹 화면(시술 진행판 · 고객 상세)에서 A 일정이 우회 결과와 똑같이 보이는지는 사람이 열어 확인해야 한다(사용자 표면 확인) | — |
