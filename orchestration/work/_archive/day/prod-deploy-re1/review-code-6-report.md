# 리뷰 리포트 — prod-deploy-re1 / code 6 · Delivery #245 W4 · W5 (2026-11-11)

범위: `emr/base.py` · `emr/kos/__init__.py` · `emr/kos/mapper.py` · `emr/kos/writes.py` · `emr/normalized.py` · `emr/outbox.py` · `emr/sync.py` ·
`services/emr_sync.py` · `services/board.py`(room_move docstring · room_return) · `queries/board.py`(지운 「방 배정」 쿼리) · `dtos/board.py`(`removed_room_assigns`) ·
`services/board_rules.py` `home_room` · 새 시험 `tests/day/emr/test_room_move_chain*.py` · `test_board_room_api.py` · `test_board_queries.py`. **범위 밖**: W3(rooms) · 차트 모달.
근거: SPEC-002 개정 ⑱ — KOS 쓰기 표 :757 · :759-761 · :763-764 · 규칙 28(:835) · 29(:836) · 33(:840) · OQ-52(:933) · OQ-53(:934) · Issue #245 A2 · A3 · A4 · be-2-report.md.

## 판정: WARN

FAIL 0 · WARN 3(모두 낮음) · 참고 4. 연쇄 순서 · 경합 처리 · 실패 시 10초 조회로 넘김 · 복귀 DELETE 순서 · 귀가 대기 CANCEL · 사라짐 확인 · 규칙 33 · 쿼리 +1 · 로그는 스펙과 같다.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra" backend/tests/day/emr backend/tests/day/board backend/tests/architecture` | **195 passed**, 128 deselected |
| `uv run ruff check backend` | All checks passed |

infra(연쇄 5 · board_room_api · 쿼리 수)는 사용자 포트 · 프로세스 금지라 다시 돌리지 않았다 — be-2 격리 스택 수치(대상 21 passed · 전체 1199 passed + 2 failed: 쿼리 수 기대값은 고친 뒤 통과 · 차트 OOB 는 무관)를 근거로 둔다. 그 차트 시험(`test_board_chart_api.py:329`)은 지금 워크트리에서 「`chart-author-` 없음」으로 이미 고쳐져 있다(미커밋 2줄).

## W4 — 이벤트 연쇄 (`services/emr_sync.py:253-336`)

| 항목 | 판정 | 근거 |
|---|---|---|
| 순서 | PASS | `run_outbox` 가 보낸(2xx) `add-flow-tasks` 마다 `_chain_room_assign` → 상세 조회(`fetch_visit_tasks` · `get-schedule-detail {scheduleId}`) → `added_room_assign`(보내기 전에 없던 · 설정 기타 작업 id · 여럿이면 큰 것 — OQ-52 기본값) → 만들기 확인 → `follow_room_assign`(① 새 「방 배정」 → 원래 방 ② 나머지 → 새 방 · 기존 함수 그대로) → 그 방문만 `send_pending(visit_id=…)` → 상세 조회로 확인. 스펙 :759-761 · 규칙 28 과 같다 |
| 못 찾음 · 오류 · 미지원 → 10초 조회 | PASS | `not_found` · `detail_error`(EmrError) · 업체 미지원(`fetch_visit_tasks` 기본 None · `base.py`) 모두 만들기 쓰기를 `SENT` 그대로 두고 끝 → 기존 일정 조회의 `confirm` → `room_assign_added` → `follow_room_assign` 경로가 잇는다(`emr_sync.py:201`) |
| 동시성(일정 조회와 경합) | PASS | 확인은 조건부 UPDATE(`confirm_room_assign_added` → `_move` · status = SENT · attempts 같음 · `outbox.py:750-760`). 일정 조회가 같은 행을 먼저 옮기면(같은 transaction 안에서 `follow_room_assign` 까지) 연쇄 쪽 UPDATE 는 행 잠금 뒤 0행 → `taken_by_poll` · follow 를 두 번 쌓지 않는다. 연쇄 쪽도 확인 + follow 를 한 transaction 으로 commit. 일정 조회가 다시 보내기(resend)로 옮겨도 attempts 가 달라 연쇄는 물러선다 |
| outbox 잠금 · 상한 | PASS | 연쇄는 `run_outbox` 안(잠금 `day:lock:emr:outbox` · TTL 60 · 상한 55초 `asyncio.timeout`) — 다른 outbox 회차와 겹치지 않는다. 최악 추가 시간 ≈ 쉬기 0.5 × 4 + HTTP 6회. 상한에 걸려 취소돼도 commit 전이면 되돌아가고(SENT 그대로) commit 뒤면 follow 가 pending 으로 남아 다음 회차가 보낸다 |
| 다른 쓰기 순서 | PASS | follow 쓰기는 확인 때 쌓여 그 방문 큐 끝 seq — 그 사이 직원이 쌓은 쓰기가 먼저 나가는 것은 지금(조회 경로)과 같다. 연쇄의 보내기도 `send_pending` 의 방문별 seq 순 · 실패 시 그 방문 뒤 쓰기를 멈춤 규칙 그대로 |
| 주기 그대로 | PASS(코드) · WARN-2(시험) | `sync_schedule_interval_seconds` · `outbox_send_interval_seconds` = 10 그대로(`common/config.py:114-116` · 변경 없음). 단 A2 「주기 상수 그대로를 시험으로 고정」에 해당하는 시험이 없다 — W2 |
| 상세 조회 3회 재시도(be 가 더함) | PASS(정당) | 근거 = 데모 실물(쓰기 직후 상세가 옛 값 · be-2 리포트). 스펙 규칙 28 「바로 상세 조회로 확인」 · OQ-52 「못 찾으면 10초 조회로」 안의 구현 상수(`CHAIN_DETAIL_TRIES = 3` · `0.5초`)이며 주기를 바꾸지 않고, 못 찾으면 그대로 넘긴다. 상한 55초 안에서 작다. **권고**: OQ-52 가 「구현 PR 에서 확정」이므로 스펙 OQ-52 줄에 「상세 조회는 최대 3회 · 0.5초 간격」 한 마디 |
| 확인(뒤 상세) | PASS | `confirm_visit_tasks`(`outbox.py:763-793`) — 그 방문의 SENT 쓰기 중 `expect` 가 `tasks` 하나인 것만 · 맞을 때만 confirmed · 안 맞음은 세지 않음(재전송 판단은 10초 조회 `decide_on_poll` 몫). 조건부 UPDATE 라 일정 조회와 겹쳐도 안전 |
| 비밀값 로그 | PASS | 새 로그 = `room assign chain detail failed visit=<id>: <KosError>` · KosError 문자열은 `HTTP <코드> <className>` · `network <예외 이름>` 뿐(`kos/client.py:100-111` · `:177`) · 토큰 · 키 · 본문 없음. counts `chain` 은 숫자 |

## W5 — 복귀 = 「방 배정」 삭제

| 항목 | 판정 | 근거 |
|---|---|---|
| 순서 | PASS | `services/board.py:1489-1508` — `complete(complete=False)` → `delete_room_tasks` → `assign_room`(나머지 → 원래 방). 스펙 :763-764 · 규칙 29(KOS 웹 순서) 와 같다. 일정 없으면 셋 다 `Skipped`(기존 방식 · 조용히 건너뛰지 않음) |
| 귀가 대기 CANCEL 그대로 | PASS | `cancel_room_tasks` 계획(`writes.py:186-192`) 손대지 않음 · 기존 시험 `test_board_api.py:441` · `test_kos_board_contract.py:249` 그대로 통과 |
| 확인 = 사라짐 | PASS | 계획 `expect = {"tasks": {seq: {"absent": true}}}`(`writes.py:193-200`) · `tasks_met`(`outbox.py:647-664`) — 응답에 그 sequence 가 없으면 맞음 · 필수 칸이 빠져 뺀 작업(`skipped`)은 「있음」(조용히 맞음 처리 안 함 · 시험 `test_room_move_chain_rules.py:122`). 앞의 `complete=false`(status_not done)는 `TASK_KEY_FIELDS["absent"] = "status"` 로 뒤 삭제가 보내지면 `_superseded` 로 닫힘 → 작업이 사라져도 재전송 · failed 로 빠지지 않음(A3 · 시험 `:130`). 반영 중엔 조회가 DAY 의 `canceled` 를 덮지 않음(`sync.py` `EXPECT_TASK_FIELDS["absent"]` · 시험 `:145`). 데모 실물: 일정 조회에서 바로 빠짐 · 상세는 잠시 남음 → 확인을 일정 조회로 하는 지금 구현이 맞다(복귀는 연쇄를 쓰지 않음) |
| gate | PASS(+W1) | `write_open` 의 `cancel-flow-tasks` 는 `reason ∈ {CANCEL, DELETE}` 만(`writes.py:85-86` · 시험 `:114-119`) |
| 규칙 33 지운 행 포함 | PASS | `queries/board.py:189-200` — 그 날 방문의 `deleted_at` 있는 `is_room_assign` 행을 `removed_room_assigns` 로 · 판 작업(`w.tasks`)에는 안 넣음 → 점유 판정(`hold_room` = 살아 있는 행) · 판 카드에 안 보임. `home_room`(`board_rules.py:609-617`) = 살아 있는 · 취소된 · 지운 행 합쳐 `(sort_order, sequence)` 첫 행 · 없으면 `visit.room_id`. 지운 곳 무관(sync 의 기존 「사라짐 → deleted_at」 경로) · 시험 `test_room_move_chain_rules.py:160` |
| 쿼리 수 +1 | PASS | 방문 수와 무관한 쿼리 하나(`visit_id IN (…)`) — `test_board_queries.py` 기대 15 → 16 · 「방문 1개와 10개가 같다」 유지(N+1 아님) |
| 계약 | PASS | migration 0 · 공개 API · 스냅샷 변경 0. `WriteKind` 에 `delete_room_tasks` · `expect` 에 `absent`(내부 형식) 추가 |

## WARN

### W1. gate 가 DELETE 를 「복귀 경로에만」 열지는 않는다 — A3 문구보다 넓다
- Issue #245 A3 「KOS 쓰기 문(gate)은 DELETE 를 복귀 경로에만 연다」. 실제 gate(`writes.py:85-86`)는 (경로 + 값) 단위라 `cancel-flow-tasks` + `reason = DELETE` 면 어느 의도에서 와도 연다. 본문에는 「방 배정」인지 알 수 있는 칸이 없다(`scheduleId` · `sequences` 뿐) — 그래서 시술 작업 sequence 로 DELETE 를 쌓는 코드가 생겨도 gate 는 막지 못한다.
- 지금 DELETE 를 만드는 곳은 `room_return` 의 `delete_room_tasks` 하나(sequences = 원래 방의 살아 있는 「방 배정」)라 실해는 없다.
- 고칠 방향(택1): (a) A3 문구를 「DELETE 를 만드는 의도는 복귀(`delete_room_tasks`) 하나 · gate 는 CANCEL · DELETE 만」으로 맞춘다(코디) · (b) 아키텍처 시험 한 개 — `delete_room_tasks` 를 만드는 곳이 `services/board.py` `room_return` 하나뿐임을 고정.

### W2. A2 「주기 상수 그대로」를 고정하는 시험이 없다
- 코드는 바뀌지 않았다(`config.py:114-116` = 10). 그러나 A2 는 「세 경로(찾음 · 못 찾음 → 조회로 · **주기 상수 그대로**)를 시험으로 고정」. 찾음 · 못 찾음은 `test_room_move_chain.py:167` · `:204` 로 있다. 주기는 없음.
- 고칠 방향: `get_settings` 기본값 `sync_schedule_interval_seconds == 10` · `outbox_send_interval_seconds == 10` 단언 한 줄(DB 없이).

### W3. 연쇄의 보내기가 그 방문의 「다시 보낼(retry) 쓰기」를 같은 회차에 곧바로 다시 보낸다
- `_chain_room_assign` 의 `send_pending(visit_id=…)`(`emr_sync.py:309-316`)은 그 방문의 PENDING 을 seq 순으로 모두 보낸다. 첫 보내기에서 그 방문의 뒤 쓰기가 5xx 등으로 retry(PENDING · attempts+1) 됐다면, 연쇄가 1초 안에 다시 보내 attempts 를 또 올린다(`MAX_ATTEMPTS = 3` — 백오프 없음). 지금은 회차 간격(10초)이 사실상의 간격이었는데, 이 방문만 그 간격 없이 한 번 더 쓴다 → 일시 장애 때 failed 로 더 빨리 빠질 수 있다(→ 그 방문 뒤 쓰기 막힘).
- 드묾(「방 배정」 없는 점유 이동 + 같은 방문 다른 쓰기 실패가 같은 회차). 
- 고칠 방향: 연쇄 보내기는 follow 로 새로 쌓은 쓰기(그리고 그 앞 seq 의 attempts 0 쓰기)만 — 예: 이번 회차에 retry 가 난 방문이면 연쇄의 보내기를 건너뛰고 `follow_not_sent` 로 다음 회차에 맡김.

## 「조용히 통과하는 자리」 · 참고

- 참고 1: `_chain_room_assign` 은 `EmrError` 만 잡는다. 그 밖 예외(DB 오류 등)는 `run_outbox` 본문 밖으로 나가 `_run` 이 `error` 로 끝내고, **첫 보내기의 `_signal`(④ outbox 상태 · 실패 토스트 메시지)이 그 회차에 안 나간다**(`emr_sync.py:253-262` — 신호가 연쇄 뒤에 있음). 다음 회차에 다시 나가므로 실해는 작다. 연쇄를 `try/except Exception → "chain_error"` 로 감싸면 신호가 지켜진다.
- 참고 2: 결과 이름 — `confirmed >= sent["sent"]` 의 `sent` 는 그 방문에서 이번에 보낸 **모든** 쓰기 수다. 같은 방문의 다른(작업 칸이 아닌) 쓰기가 같이 나가면 follow 둘이 확인돼도 `follow_sent` 로 남는다(counts 이름만 · 동작 영향 없음).
- 참고 3(시험): 연쇄의 경합(`taken_by_poll`)은 「일정 조회가 먼저 확인한 뒤」 순서로만 시험한다(`:229`) — 진짜 동시(행 잠금 대기)는 시험하지 않는다. 조건부 UPDATE 라 코드상 안전.
- 참고 4: OQ-53 남은 것(KOS 가 지운 sequence 를 다시 쓰는지)은 be-2 실물로 확인 못함 — `added_room_assign` 의 「보내기 전에 없던 sequence」 판정은 다시 쓰여도 `known` 기준이라 영향은 「지운 번호가 새 방 배정으로 다시 나오면 새것으로 본다」 쪽(맞는 방향). Issue A6(코디 실물)에 그대로 남김.

## Acceptance (#245 · W4 · W5 부분)

| # | 판정 | 근거 |
|---|---|---|
| A2 | 충족(+W2) | 연쇄 · OQ-52 기본값 · 찾음/못 찾음 시험(infra 5). 주기 시험 없음(W2) |
| A3 | 충족(+W1) | 순서 · 사라짐 확인 · 재전송/failed 안 됨 · 귀가 대기 CANCEL 시험 그대로. gate 문구보다 넓음(W1) |
| A4 | 충족 | 지운 행 → 원래 방 · 판 · 점유에 안 보임(규칙 시험 + `test_board_room_api` infra) |
| A5 | 이 리뷰 범위 수치: not infra 195 passed · ruff 통과 · migration 0. 전체 `scripts/test.sh` 는 be-2 수치(쿼리 수 고친 뒤 · 차트 시험 고쳐짐)에 기댐 |
| A6 | 해당 없음(코디 실물) | be-2 데모 실물 1회: 연쇄 317ms · 복귀 DELETE 2xx · 일정 조회에서 빠짐 |
