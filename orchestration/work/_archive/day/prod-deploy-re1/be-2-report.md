# prod-deploy-re1 backend 2 — #245 W4 · W5 서버 결과 보고

## 상태: done (커밋 · push 안 함 — 워크트리 변경만)

정본: SPEC-002 개정 ⑱(mediness#934) — KOS 쓰기 표 · 규칙 28 · 29 · 33 · OQ-52 · OQ-53. 근거: research-1 W4 · W5.

## 수행 — 파일 · 모듈

### W4 — 「방 배정」 없는 점유 이동: 이벤트 연쇄

- **예약 상세 조회**
  - `backend/day/emr/kos/__init__.py:52` `PATH_SCHEDULE_DETAIL = schedule/v1/queries/get-schedule-detail`(`{scheduleId}` · HAR `방선택.har`)
  - `:181` `KosAdapter.fetch_visit_tasks` — 시스템 계정 토큰으로 읽기만 한다. 응답 모양이 틀리면 `KosError`.
- `backend/day/emr/kos/mapper.py:541` `visit_tasks(resp)` — `data.tasks` 를 일정 조회와 같은 `task()` 로 읽는다. 필수 칸이 빠진 작업은 `skipped_sequences` 로 따로 둔다.
- `backend/day/emr/normalized.py` `NVisitTasks(tasks, skipped_sequences)` 를 새로 두었다.
- `backend/day/emr/base.py` `EmrAdapter.fetch_visit_tasks` 는 기본값이 None 이다(지원 안 하는 업체 → 10초 조회로 넘김).
- `backend/day/emr/outbox.py`
  - `Report.room_assign_sent`(`:135`) — `_send_one` 이 `add-flow-tasks` 2xx 를 받으면 여기에 담는다(`:574`).
  - `send_pending(visit_id=…)` — 방문 하나만 보낼 수 있게 했다.
  - `added_room_assign` 이 `NVisitTasks` 도 받는다.
  - `tasks_met`(`:647`) — 작업 확인 공통 함수. `expect_met` 도 이것을 쓴다.
  - `confirm_room_assign_added`(`:750`) — sent 그대로일 때만 confirmed 로 옮긴다. 같은 때 일정 조회가 먼저 확인했으면 False 를 돌려주고, follow 쓰기를 두 번 쌓지 않는다.
  - `confirm_visit_tasks`(`:763`) — 상세 조회로 보낸 작업 쓰기를 확인한다. 안 맞음은 세지 않는다(재전송 판단은 10초 조회 몫).
- `backend/day/services/emr_sync.py`
  - `run_outbox` 가 보낸 「방 배정」 만들기마다 `_chain_room_assign`(`:268`)을 부른다.
  - 연쇄 순서:
    1. 상세 조회로 새 「방 배정」 sequence 를 찾는다(보내기 전에 없던 것 · 설정 기타 작업 id).
    2. 만들기 쓰기를 확인한다.
    3. `board.follow_room_assign` 으로 ① 새 「방 배정」 → 원래 방, ② 나머지 → 새 방을 쌓는다.
    4. 그 방문만 바로 보낸다.
    5. 바로 상세 조회로 확인한다.
  - 상세 조회는 최대 `CHAIN_DETAIL_TRIES = 3` 번, `0.5` 초 간격으로 읽는다(데모 실물에서 쓰기 직후 옛 값이 보였다 — 아래).
  - 못 찾음 · 상세 오류 · 지원 안 함이면 거기서 멈추고 지금처럼 10초 일정 조회가 잇는다(주기 조정 없음 · 10초 조회 그대로).
  - 결과는 counts `chain` 에 남긴다: `confirmed` · `follow_sent` · `not_found` · `detail_error` · `taken_by_poll` · `follow_not_sent`.
- `backend/day/services/board.py` — `room_move` docstring 만 바꿨다.

### W5 — [복귀하기] = 「방 배정」 삭제

- `backend/day/emr/base.py` — `WriteKind` 에 `delete_room_tasks` 를 더했다(새 intent · 귀가 대기 `cancel_room_tasks` 와 나눔).
- `backend/day/emr/kos/writes.py`
  - `DELETE_REASON = "DELETE"`(`:67`)
  - `write_open` 의 `cancel-flow-tasks` 는 `CANCEL` · `DELETE` 만 연다.
  - 계획(`:193`): body `reason = DELETE`, 확인 = `{"tasks": {seq: {"absent": true}}}`. 표에도 두 행을 더했다.
- `backend/day/emr/outbox.py`
  - `absent` 확인: 일정 조회 응답에 그 sequence 가 없으면 맞음. 필수 칸이 없어 뺀 작업(`skipped_task_sequences`)은 「있음」으로 본다.
  - `TASK_KEY_FIELDS["absent"] = "status"` — 앞의 `complete=false`(status_not done)는 뒤 삭제가 보내지면 `_superseded` 로 닫힌다. 작업이 사라지면 그 확인은 영영 안 맞기 때문이다.
- `backend/day/emr/sync.py` — `EXPECT_TASK_FIELDS["absent"] = "status"`. 삭제 반영 중에는 조회가 DAY 의 `canceled`(반영 중 값)를 덮지 않는다.
- `backend/day/services/board.py:1496` `room_return` — `complete(false)` → `delete_room_tasks` → `change-tasks-room`(나머지 → 원래 방) 순서다(KOS 웹 순서). [귀가 대기]는 `CANCEL` 그대로다(`:980` 손대지 않음).
- **규칙 33 — 지운 「방 배정」 행도 원래 방 판정에 넣는다**
  - `backend/day/dtos/board.py` — `BoardWorld.removed_room_assigns`(방문 → (sort_order, sequence, 방))를 끝에 더했다.
  - `backend/day/queries/board.py:~190` — `deleted_at` 이 있는 `is_room_assign` 행을 쿼리 하나로 읽는다. 판 작업(`w.tasks`)에는 넣지 않는다.
  - `backend/day/services/board_rules.py:610` `home_room` — 살아 있는 · 취소된 「방 배정」과 지운 행을 합쳐 `sort_order` 첫 행으로 정한다.
  - **board_rules 는 `home_room` 만 고쳤다.** rooms 쪽(frontend 워커)과 차트 쪽 미커밋 변경은 그대로다.

### 시험

- 새 파일 `backend/tests/day/emr/test_room_move_chain_rules.py` — DB 없이 9개.
  - 상세 응답 매핑 · 모양 틀림 → None
  - 새 「방 배정」 찾기
  - DELETE 계획 · 보내기 문
  - 사라짐 확인(필수 칸 빠짐 = 있음)
  - `complete=false` 를 삭제가 덮음
  - guard
  - home_room(지운 행)
- 새 fixture `backend/tests/day/emr/fixtures/kos_schedule_detail.json`(값은 기존 가짜 고정본 그대로) · README 한 줄
- 새 파일 `backend/tests/day/emr/test_room_move_chain.py` — infra 5개. 가짜 KOS 가 보낸 쓰기를 작업 사본에 반영한다.
  - 연쇄 순서 = add → detail → room → room → detail · 세 쓰기 모두 confirmed
  - 늦게 보이면 한 번 더 읽어 확인
  - 못 찾으면 detail 3회 뒤 sent 그대로(10초 조회로)
  - 상세 오류
  - 조회가 먼저 확인했으면 연쇄는 쌓지 않음
- 고친 `backend/tests/day/board/test_board_room_api.py`
  - 복귀 경로 = `change-tasks-complete` · `cancel-flow-tasks(DELETE)` · `change-tasks-room`
  - 사라짐 조회 → 앞 두 쓰기 confirmed
  - 지운 행이 `removed_room_assigns` 에 들어감
- 고친 `backend/tests/day/board/test_board_queries.py:177` — world 쿼리 수 15 → 16(지운 「방 배정」 쿼리 하나 · 방문 1개와 10개가 같음은 그대로)

## 검증 — 명령과 수치

- `uv run pytest -q -m "not infra" backend/tests` → 880 passed(중간). 새 DB 없는 시험 9 passed.
- 격리 스택(`docker compose -p day-be245` · 포트 11142/11143 · scratchpad env · `day-local` 은 건드리지 않음 · 끝나고 `down -v`)으로 돌렸다.
  - `scripts/test.sh -q` 고친 · 새 시험(chain · chain_rules · board_room_api) → **21 passed**
  - `scripts/test.sh -q` 전체 → **1199 passed · 2 failed**
    - `test_board_queries.py::test_방문_1개와_10개의_쿼리_수가_같다` — 내 변경(쿼리 +1)이다. 기대값을 고친 뒤 3 passed.
    - `test_board_chart_api.py::test_웹_차트_저장은_OOB_충돌이면_그_줄과_토스트_담당자_없음은_토스트_없음` — **무관**이다. 작성자 OOB(`chart-author-…`)를 찾는데, frontend 워커의 미커밋 차트 모달 변경(개정 ⑱ ④ 작성자 안 보임 · `board_chart_parts.html`)이 그 자리를 뺐다. 내 파일과 관계없다.
- `uv run ruff check backend` → All checks passed. `ruff format --check backend/day` → 통과.

## 데모 KOS 실물 1회 (데모 테넌트 · 가드 `6a793c…` = `seed_demo_board.py` 와 같음)

- 스크립트는 scratchpad 에만 두었다(`demo_chain_check.py` · `demo_read.py`) — 레포 밖이다.
- 값(id · 이름 · 키)은 찍지 않았다. 시스템 계정 토큰으로 보냈다(`seed_demo_board.py` 와 같은 방식). 오늘 판 카드 방문 1건에서 했다.
- **W4 연쇄**
  - `add-flow-tasks` 2xx **84ms** → 상세 조회 **첫 번째에서** 새 「방 배정」을 찾음(51ms)
  - → `change-tasks-room` 2건 151ms → 바로 상세 조회(32ms)로 확인한 결과: ① 새 「방 배정」 → 원래 방은 **맞음**, ② 나머지 → 새 방은 **아직 옛 값**
  - 연쇄 전체 **317ms**(지금 dev 실측 19.8 ~ 27.1초와 비교)
  - 새 「방 배정」 상태 = `ready` · 방 = 원래 방
  - → KOS 가 쓰기를 수십 ms 안에 다 반영하지 않을 때가 있다. 그래서 상세 조회를 짧게 다시 읽게 했다(3회 · 0.5초). 그래도 안 맞으면 10초 조회가 확인한다.
- **W5 삭제(OQ-53)**
  - 「방 배정」(완료 아닌 기타 작업)에 `complete=false` → **KOS 가 받음(2xx)**
  - `cancel-flow-tasks reason=DELETE` → 2xx
  - 바로 다음 **일정 조회(`get-schedules-grouped-by-zone`)에서 그 작업이 빠짐**(absent=True)
  - 같은 순간 **상세 조회에는 아직 남아 있었다**. 잠시 뒤 다시 읽었을 때는(`demo_read.py`) 상세 · 일정 조회 둘 다에서 빠졌다.
  - 그래서 확인은 일정 조회(10초)의 「사라짐」으로 한다. 지금 구현이 그렇다 — 복귀는 연쇄를 쓰지 않는다.
- **sequence 재사용**: 이번 1회로는 확인하지 못했다. 지운 sequence 가 그때 가장 큰 번호였지만, 다시 만들어 보지 않았다 → OQ-53 의 이 항목은 **pending** 이다.
- **되돌림**: 옮긴 작업은 원래 방으로 되돌렸다. 바로 읽었을 때는 안 맞았고, 다음 읽기(`demo_read.py`)에서 모든 작업이 원래 방이었다. 테스트로 만든 「방 배정」은 삭제돼 조회에서 빠졌다.
  - 데모 방문에 남은 흔적: 작업 `roomAssignedDateTimeUtc` 갱신 가능성.

## 계약 대조

- KOS 쓰기 표 「점유 이동 · 방 배정 없음」 1 · 2 · 3: **같음**. 응답 → 상세 → ① · ② → 상세 확인 · 못 찾으면 10초 조회 · 주기 조정 없음.
- 「복귀」 1 · 2: **같음**. `complete=false` → `DELETE` · 확인 = 사라짐 · DAY 사본 `deleted_at` 은 sync 의 기존 「사라짐」 처리.
- 귀가 대기 `CANCEL`: **그대로**.
- 규칙 33: **같음**. 지운 행 포함 · 지운 곳 무관(DAY 복귀 · KOS 웹 모두 `deleted_at` 으로 들어온다). 이미 `CANCEL` 로 쌓인 행은 그대로다.
- OQ-52 기본값(상세 조회 경로 · 가려내는 법 · 못 찾을 때): **그대로 구현**. 다른 점 하나: 상세 조회를 3회까지 다시 읽는다(데모 실물 근거). 이것을 구현 PR 에서 확정할지 코디가 판단한다.
- migration · 공개 API · 스냅샷 변경은 없다. `external_outbox.expect` 에 새 키 `absent` 를 더했다(내부 형식).

## 이슈 · 코디가 확인할 것

1. 상세 조회 재읽기(3 × 0.5초)는 스펙에 없는 상수다. 연쇄는 worker 의 outbox 회차 안에서 돈다(잠금 TTL 안 · 최악 몇 초). 이대로 둘지, 스펙 OQ-52 에 한 줄 더할지 정한다.
2. 연쇄로 확인된 뒤에도 DAY 판의 새 「방 배정」 작업 행은 다음 10초 일정 조회 때 들어온다. KOS 반영은 ~0.3초이지만 DAY 점유 띠는 조회 회차를 기다린다. 연쇄에서 DAY 행까지 바로 만들지는 범위 밖이라 하지 않았다.
3. OQ-53 남은 것: KOS 가 지운 sequence 를 다시 쓰는지 — 확인 안 됨(pending).
4. 무관 실패 1건(`test_board_chart_api` 작성자 OOB)은 frontend 워커의 차트 모달 변경과 함께 시험을 맞춰야 한다.

## 수정 1 (review-code-6 W1 · W2 · W3 · 참고 1 · 2026-11-11)

- **W1 (b) 아키텍처 시험** — `backend/tests/architecture/test_room_delete_write.py`(새)
  - AST 로 `day/` 전체의 문자열 상수를 본다.
  - `delete_room_tasks` 는 정의(`emr/base.py`) · 계획(`emr/kos/writes.py`) 말고는 `services/board.py` 의 `room_return` 함수 안에서만 나온다. 실제로 만드는 줄이 있는지도 확인한다.
  - 값 `"DELETE"` 는 `emr/kos/writes.py` 밖에서 나오지 않는다.
- **W2 주기 상수** — `test_room_move_chain_rules.py::test_일정_조회_발송_주기는_10초_그대로다`(DB 없이)
  - `Settings` 기본값 `sync_schedule_interval_seconds == 10` · `outbox_send_interval_seconds == 10`
  - `deploy/` 의 env · yaml · 예시 파일 어디에도 두 이름이 없다(덮지 않음).
- **W3 연쇄 보내기 건너뛰기**
  - `backend/day/emr/outbox.py:137` `Report.retried_visits` — `_send_one` 의 보내기 오류 결과가 retry · failed 이면 그 방문을 담는다(`:574`).
  - `backend/day/services/emr_sync.py` `_chain_room_assign(..., send=…)` — 그 방문이 이번 회차에 retry 됐으면 확인 · follow 쌓기까지만 하고 보내지 않는다. 결과는 `follow_not_sent` 이고, 다음 발송 회차가 보낸다.
  - 시험 `test_room_move_chain.py::test_같은_회차에_그_방문_쓰기가_retry_됐으면_연쇄는_보내지_않고_다음_회차에`
    - KOS 호출 = add · room(503) · detail
    - 503 난 쓰기는 attempts 1 그대로
    - follow 둘은 pending
- **참고 1**
  - `run_outbox` 가 연쇄를 `try/except Exception` 으로 감싼다. 실패하면 `chain_error` 를 남기고 로그에는 예외 클래스 이름만 찍는다(값 없음). 첫 보내기의 `_signal` 은 그대로 나간다.
  - 시험 `test_연쇄가_깨져도_첫_보내기_신호는_나간다` — 회차 done · chain_error · 신호 1회 · 만들기 쓰기는 sent 그대로(10초 조회가 잇는다).
- **검증**
  - 격리 스택(`day-be245` · 끝나고 `down -v`)에서 `scripts/test.sh -q` 를 연쇄 · 연쇄 규칙 · architecture 전체 · board_room_api · outbox · emr_sync_service 로 돌렸다 → **76 passed**
  - `uv run ruff check backend` → 통과 · 만진 파일 `ruff format` 통과(시험 파일 1개는 서식만 다시 맞춤)
