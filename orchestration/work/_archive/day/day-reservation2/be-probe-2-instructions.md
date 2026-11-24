# [backend · 실물 확인 2] KOS 데모 지점 — 접수 · 상담 대기 배정 · 상담사 / 관리실 바꾸기 · 상담 중 귀가

**앞 판 먼저 읽기**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-1-instructions.md`(규칙 · 금지 · 보고 방식 — 이번에도 전부 그대로) · `be-probe-1-report.md`(결과 · 연락처 꼴 · 취소 enum · 담당자 지연). 스크립트는 `/private/tmp/day-probe-2/`(1 의 `pcommon.py` 를 복사해 써도 됨).

**레포 파일을 고치거나 커밋하지 마라. 데모 지점 확인(`check_open_key_is_demo` 같은 것)을 통과한 뒤에만 쓴다.** `~/.config/day/` 금지 · 로컬 스택 · DB · docker 금지 · 값 · 토큰 · 개인정보 출력 금지(키 모양 · O / X · id 앞 8자).

## 1. 왜

예약 상세 모달의 접수 · 상담 단계 동작이 DAY `KosClient` 로 데모 지점에 실제로 들어가는지 본다. 결정(코디 `_RESUME.md` §2):
- [접수] = 오늘 예약만 · 명시적으로 버튼
- [상담 대기] = 시술 현황 방 배정과 같은 연쇄 — 「방 배정」 기타 작업 만들기 → 방 지정 → 단계 `CONSULTATION_WAITING`
- 상담 대기에서 상담사 · 관리실을 고르면 바로 KOS
- 상담 대기 · 상담 진행 중 [귀가 처리] = 바로 귀가 완료(`COMPLETED`)

## 2. 근거 경로 · 본문

- DAY: `backend/day/emr/kos/writes.py`(경로 상수 `ROOM` · `ADD_TASKS` · `FLOW_STEP` · 「방 배정」 `add-flow-tasks` 본문 · `ETCETERA`) · `services/board_rooms.py` · `services/emr_sync.py` `_chain_room_assign`(add-flow-tasks 뒤 상세 다시 읽어 새 sequence 찾기) · `emr/kos/demo/kos_board.py`(데모 도구가 `recept` · `add-flow-tasks` · `change-flow-step CONSULTATION_WAITING` 을 이미 부름 — 본문 모양 근거)
- 「방 배정」 기타 작업 id = `/Users/kknaks/git/CENTURION_DAY/deploy/local.env` `DAY_SEED_KOS_ROOM_ASSIGN_ETC_TASK_ID`(값 출력 금지) — 없으면 `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` 에서 「방 배정」
- cc(`git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/service/reception.py`): `run`(L116 ~ · recept → add-flow-tasks → change-tasks-room → change-flow-step) · `counselor_call`(L209 ~ · `update-reservation {scheduleId, counselor}`) · `discharge`(L230 ~ · 공개 `change-flow-step COMPLETED`)
- 방 목록 = `schedule/zone/room/v1/queries/get-rooms` · 상담 직원 = 1 에서 쓴 역할 「상담실장」

## 3. 시험 데이터

- 고객 = 1 에서 만든 시험 고객 `6b051a9e…`(「박하늘(시험)」) **만**. 새 고객 만들지 마라.
- 예약 = **오늘** 빈 칸에 시험 예약을 새로 만든다(접수가 오늘만 되므로). 기존 데모 예약 · 고객은 건드리지 마라.
- ⚠ 데모 지점 오늘 판은 DAY dev 서버 화면에도 보인다 — 시험이 끝나면 만든 예약은 전부 **귀가 완료 또는 취소**로 정리해 판에 걸린 채 남지 않게.

## 4. 시험 (각 단계 = 경로 · 본문 키 모양 · 응답 코드 · 다시 읽기(`schedule/v1/queries/get-schedule-detail`) 칸 O / X · 늦게 보이는 칸이 있으면 몇 초 뒤인지)

**예약 A (상담 대기까지 · 그 뒤 상담 대기에서 귀가)**
1. 오늘 예약 만들기(1 과 같은 본문) → `RESERVED`
2. **접수** 내부 `schedule/v1/commands/recept {scheduleId}` → 다시 읽어 `flowStep` 값(KOS 값 그대로) · `receptionDateTimeUtc`
3. **「방 배정」 기타 작업 만들기** `add-flow-tasks`(DAY `writes.py` `write_open` 이 허용하는 모양 그대로) → 상세에서 새 작업 sequence · 상태
4. **방 지정** `change-tasks-room {scheduleId, sequences:[3의 sequence], roomId}` → 작업 방 O / X
5. **단계 바꾸기** 내부 `schedule/v1/commands/change-flow-step {id, step:"CONSULTATION_WAITING"}`(DAY 본문 꼴 · `writes.py` 머리 주석) → `flowStep`
6. **상담사 바꾸기**(상담 대기에서) 내부 `update-reservation {scheduleId, counselor{id, name}}`(cc `counselor_call`) → 다시 읽어 `reservation.counselor` · `consultation` 쪽 어디에 들어갔나 · **1 에서 본 「바꾸지 않는 칸도 다시 실어야」가 여기서도 그런지**(담당자 · 그룹 · 시간 · 의사 · 메모가 지워지지 않았나 칸마다 O / X)
7. **관리실 바꾸기**(상담 대기에서) `change-tasks-room` 다른 방 → O / X
8. **상담 대기에서 귀가** — 먼저 DAY 내부 꼴 `change-flow-step {id, step:"COMPLETED"}` → 안 되면(4xx) 공개 `schedule/open/v1/commands/change-flow-step {scheduleId, step:"COMPLETED"}`(cc) → 다시 읽어 `flowStep` · 「방 배정」 작업 상태가 어떻게 됐나(남나 · 취소되나 · 완료되나)

**예약 B (상담 진행 중 귀가)**
9. 오늘 예약 만들기 → 접수 → 방 배정 → 방 지정 → `CONSULTATION_WAITING`(2 ~ 5 와 같음)
10. 상담 진행으로: `change-flow-step {id, step:"CONSULTATION"}`(KOS 값 이름이 다르면 openapi · `enums` · DAY `mapper` 에서 확인해 그 값) — 안 되면 「상담 진행으로 못 만듦」 기록하고 11 은 건너뜀
11. **상담 진행에서 귀가** — 8 과 같은 방식 → `flowStep` · 상담(`consultation`) 칸이 어떻게 남나(열린 채 · 닫힘)

**정리**
12. 남은 시험 예약이 있으면 공개 `cancel-reservation {reason:"CANCELED"}` — 귀가 완료된 건 취소하지 말고 그대로(취소가 400 이면 코드 · 메시지 기록).

## 5. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-2-report.md` — 맨 위 표: 시험 1 ~ 12 × (경로 · 응답 코드 · 들어갔나 O / X · 비고). 아래: 단계별 본문 · 응답 키 모양 · 다시 읽은 칸 · 「DAY `writes.py` 에 열 때 필요한 것」(경로 · 값 조건 · 확인 조건 후보 — 결정 아님). 특히 ⓐ `COMPLETED` 가 내부 / 공개 중 어디서 되나 ⓑ 귀가 뒤 「방 배정」 작업 · 상담 칸 상태 ⓒ `update-reservation` 이 칸을 덮어쓰나.

## 6. 완료 보고 — 1 과 같은 두 명령(subject 「backend 완료: KOS 데모 실물 확인 2」) · task-id · dispatch-id 는 이번 dispatch 값.
