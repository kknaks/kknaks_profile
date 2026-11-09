# Delivery #230 시술 현황 1차 ① 백엔드 결과 보고 (DAY-SPEC-002)

## 상태: done — 실제 KOS 쓰기 0 · 커밋 안 함 · compose 는 내리지 않고 api · worker · scheduler 만 새 코드로 다시 올림

워크트리 `CENTURION_DAY/day-data-architecture` · #224 ~ #229 커밋(`9c7376ca`) 위 미커밋.

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **255 passed** · 130 deselected |
| `scripts/test.sh -q`(compose postgres · redis · `DAY_REQUIRE_INFRA=1`) | **385 passed** (29s) |
| `uv run ruff check backend scripts` · `ruff format --check backend` | All checks passed · 포맷 맞음 |

이번에 더한 테스트: DB 없이 — `tests/day/board/test_board_rules.py` 20 · `tests/day/emr/test_kos_board_contract.py` 10 ·
`test_outbox_rules.py` +1 · infra — `tests/day/board/test_board_api.py` 19 · `test_board_sse.py` 4 · `test_outbox.py` +6 ·
`test_sync.py` +2 · `test_constraints.py` +1(`external_outbox(visit_id, seq)`). #226 테스트는 새 보내기 규칙(직원 토큰 · `send(command, token)`)에 맞춰 고쳤다.

### 실물 (데모 지점 · 조회 + DAY 동작 + 쓰기 큐 적재까지 · KOS 쓰기 없음)

1. `--profile app up -d --build --wait api worker scheduler` — migrate 가 `0004_board` 적용(`doctor_call.closed_at` 칸 1 · `uq_external_outbox_visit_id_seq` 1).
2. worker 10초 조회: 오늘 데모 방문 1건(시술 대기 · 방 있음 = 판 카드) · `visit_task` 5(방 배정 1 · 시술 4) · `external_ref(visit_task)` 5 ·
   회차마다 `done` · 오류 0. 오늘 작업의 직원 배열은 비어 있어 `visit_task_staff` 0 · 상담 0.
3. 같은 코드를 호스트 프로세스로 `day_dev` 에 붙여(전체 권한은 그 프로세스 env 의 `DAY_ADMIN_EMAILS` 에만 · `deploy/local.env` 는 손대지 않음)
   **KOS 토큰이 없는 데모 직원**의 세션으로 조작 — 그래서 worker 는 보낼 토큰이 없어 기다린다(규칙 24):

| # | 요청 | 결과 |
|---|---|---|
| 1 | `GET /api/board` | 200 · 카드 1 · 카드 시술 4(방 배정 빠짐) · 전부 준비중 · `canCall` · 원장 5 |
| 2 | `GET /board`(HX · 쿠키) | 200 · 판 조각에 그 카드 |
| 3 · 4 · 5 | 마취 시작 · 다시 시작 · 종료 | 200 · **409 `anesthesia_running`** · 200 |
| 6 | 호출(시술 1 · 모든 의사) | 200 `{callId}` |
| 7 | 호출된 시술 [시작] | **409 `call_not_accepted`** |
| 8 | 다시 `GET /api/board` | 그 줄 `called` · 호출 탭 1 · `reflecting` true |
| 9 | Redis 채널 `day:board:<병원>` | `board` 신호 3(조작마다) |
| 10 | worker 한 회차 뒤 쓰기 큐 | `change-tasks-room` · `change-tasks-assignees` · `call-tasks-doctors` 셋 다 `pending` · attempts 0 — worker 로그 `{'no_token': 1}` |
| 11 | event_log | `anesthesia.start` 1 · `anesthesia.end` 1 · `call.create` 1 |
| 12 | 정리 | 적재한 op 3 `deleted_at`(보내지 않게) · 임시 세션 revoked · 임시 계정 삭제 |

- **남은 흔적**: 오늘 데모 카드의 DAY 호출 1건(그 시술이 「호출」)과 마취 1회차는 `day_dev` 에 남는다(되돌리기 없는 기록 · 규칙 20). KOS 에는 아무것도 가지 않았다.
- SSE `kos_failed` 실물은 실패가 필요해 테스트로만(아래 A7).

## 완료 조건 대조

| | 증거 |
|---|---|
| A1 | `emr/kos/mapper.py` `task` · `consultation` · `NVisit.tasks/consultations` · `emr/sync.py` `_apply_tasks` · `_apply_consultations`. contract `test_kos_board_contract.py`(procedureConfiguration · 직원 배열 · 빈 칸 · 필수 빠짐 → 빼고 sequence 기록 · 상담 둘이면 비움) · infra `test_작업_작업직원_상담이_들어온다` · 실물 2. **직원 배열 모양(OQ-12 직원 부분)은 데모 지점 조회(지난 30일 · 작업 241 · 비어 있지 않은 assignees 151 · doctors 141 · calledDoctors 13)로 `[{id, name}]` 확인 — 고정본을 그 모양으로 했다.** `procedureConfiguration` 안쪽 키도 같은 조회로 확인해 매핑(옵션 · 진료항목 · 단위 · 회차 · 약물). `visit.room_id` 규칙은 #226 구현이 이미 cc `_card_room_task` 와 같다 |
| A2 | `services/board_rules.py`(DB 모름) · `test_board_rules.py` 20 — 카드 조건 · 방 배정 · 5상태 · 유효 호출(닫힌 호출 제외) · [시작] 409 순서 · 종료 · 되돌리기 · 귀가 대기 · 마취 · 확인 필요(20분 초과 · 5분 · 지금 열린 호출부터) · urgency · 인박스 칸 · 원장 상태 · 카드 순서(저장 → 생긴 순 → 귀가 대기) · 재호출 기본 = 처음 대상 · 스냅샷 모양 |
| A3 | `test_board_api.py` — 401 · 403 forbidden(권한 없음 · view 만으로 조작) · 400(빈 · 중복 · 모르는 target · 모르는 칸 · one 인데 의사 없음) · 404(없는 · 다른 병원 · 방 배정 작업) · 409 전부(`visit_home` · `anesthesia_*` · `task_not_pickable` · `doctor_not_listed` · `call_closed` · `nothing_to_accept` · `task_not_waiting` · `call_not_accepted` · `no_doctor` · `task_not_started` · `task_not_doing` · `task_not_done` · `tasks_not_done`). 웹: 판 조각 계약 · 웹 409 = 토스트 조각 + `X-Day-Error` · CSRF 없음 → `csrf_failed` 토스트(#229 처리) · 조작 → 판 조각 |
| A4 | `services/board.py` — 조작마다 advisory lock · event_log 1 · outbox 0 ~ 3 · 한 transaction · KOS 를 기다리지 않음. `test_호출_한_번은_event_1행과_KOS_쓰기_3행` · `test_수락_event_의_actor_는_수락한_의사` · 실물 10 · 11 |
| A5 | `emr/kos/writes.py` `KosWritePlanner` · `write_open` — 아래 「열린 쓰기」 표. `test_열린_쓰기는_HAR_확인_6가지` · `test_닫힌_쓰기는_op_을_만들지_않고_드러낸다`(6) · `test_보내기_직전에도_값으로_막는다` · `test_열지_않은_쓰기는_요청이_나가지_않는다` · API `test_닫힌_쓰기는_DAY_만_바뀌고_op_0개`(시작 취소 · 완료 취소 · 귀가 대기 — DAY 상태 · event_log 바뀜 · op 0 · `payload.kos = not_supported`) · `test_재호출은_방_담당자만_보내고_호출은_닫힘` · 「다음 조회가 KOS 값을 따름」 `test_반영_대기_칸은_덮지_않고_failed_뒤엔_KOS_값`(귀가 대기 → 다음 조회 `procedure` · 반영 대기 칸은 지킴 · failed 뒤 KOS 값) |
| A6 | `emr/outbox.py` — 보내기 전 잡기(pending → sent 조건부 UPDATE) `test_같은_행을_동시에_두_번_보내지_않는다` · 오래된 sent → failed(`OUTBOX_SENT_STALE_SECONDS` 기본 **180초**) `test_오래_확인_안_된_sent_는_failed` + 단위 · 빈 expect 거부 `test_빈_expect_는_넣지_않는다` · `(visit_id, seq)` 유일 — migration `0004` + `test_constraints` + 동시 적재 · 실패 뒤 뒤 op failed + `blockedOpIds` `test_failed_면_뒤_쓰기도_막히고_event_log` · 토큰 없음 = pending · attempts 그대로 · 뒤 op 도 기다림 `test_토큰이_없으면_pending_그대로_attempts_안_올림` · 그 직원 토큰으로 보냄 · KOS 401 → 그 세션 `expires_at` 당기고 op 은 기다림 |
| A7 | `services/board_events.py`(Redis pub/sub) · `routers/board.py` `board_stream_events` — `test_조작_직후_board_신호` · `test_failed_로_바뀐_순간_kos_failed_한_번`(두 번째 회차엔 다시 안 보냄 · 막힌 뒤 op 은 따로 안 알림 · action = `call.create`) · `test_스트림_첫_board_와_kos_failed_토스트`(연결 즉시 board · `kos_failed` 본문 = 토스트 조각 HTML · `id:` 없음) · `test_앱_스트림은_스냅샷_JSON` · 실물 9. 10초 신호는 스트림이 직접 · 일정 조회 변경은 값 지문(Redis) 비교 |
| A8 | **이번엔 하지 않음(브리프)** — 실제 KOS 쓰기 실물은 사용자 허락 뒤 · 데모 원장 계정(W8) 대기. 직원 배열 모양은 쓰기 없이 조회로 확인해 A1 에 반영 |
| A9 | 아래 「조각 계약」 표 — 코드 문서 `backend/day/routers/board.py` 첫 docstring 이 정본 |

## 조각 계약 (A9 — #231 이 인용)

| 라우트 | 성공 응답 | 조각 이름 | 넘기는 값 |
|---|---|---|---|
| `GET /board` | 전체 페이지 / `HX-Request` 면 조각 | `board.html` / `partials/board_main.html` | `snapshot` · `inbox` · `today` (+ 셸: `session` · `hospital_name` · `rail_menus` · `header_tabs` · `htmx`) |
| `POST /board/visits/{id}/anesthesia/start` · `/end` | 판 조각 | `partials/board_main.html` | 같음 |
| `POST /board/visits/{id}/calls` | 〃 | 〃 | 폼 칸 `taskIds`(여럿) · `target`(`all`/`one`) · `doctorStaffId` |
| `POST /board/calls/{id}/recall` | 〃 | 〃 | `target` · `doctorStaffId` |
| `POST /board/calls/{id}/accept` | 〃 | 〃 | `doctorStaffId` |
| `POST /board/tasks/{id}/start` · `/finish` · `/undo-start` · `/undo-finish` | 〃 | 〃 | — |
| `POST /board/visits/{id}/home` | 〃 | 〃 | — |
| `PUT /board/order` | 〃 | 〃 | 폼 칸 `visitIds`(여럿 · 순서대로) |
| 조작 실패 400 · 404 · 409 | 그 HTTP + `X-Day-Error: <code>` + `HX-Reswap: none` | `partials/board_toast_error.html` | `code` · `message` |
| 401 · 403 · CSRF | #229 화면 규칙 | `/login` 이동 · `forbidden_page` · `partials/toast_only.html` | — |
| `GET /board/stream` | `text/event-stream` | — | SSE 아래 |

- `snapshot` = SPEC-002 「스냅샷 모양」 그대로(`now` · `version` · `limits` · `sync` · `doctors[]` · `cards[]` · `calls[]` · `doneTab[]`) — 카드 순서 = 배열 순서, 규칙 값(`pickable` · `canStart` · `canFinish` · `canUndoStart` · `canUndoFinish` · `canCall` · `canHome` · `need` · `inbox{section, urgency}` · `reflecting`)은 서버가 실었다. 시술 줄 `call` 에 `firstCalledAt` · `lastCalledAt` · `firstTargetStaffId` · `firstKind`(재호출 창 기본값 · 「응답 없음」 계산용)를 더했다.
- `inbox` = `{need, startable, waiting}` — 각 칸은 `snapshot.cards` 의 카드, 정렬 끝남(넘긴 시간 긴 순 · urgency 큰 순 · 입실 오래된 순).
- **#231 이 할 것**: htmx 는 기본으로 4xx 를 끼우지 않는다 → `day.js` 에서 `X-Day-Error` 헤더가 있는 응답을 끼우게(`htmx:beforeSwap` → `shouldSwap = true`). 본문은 `hx-swap-oob` 토스트 하나 · `HX-Reswap: none` 이라 판은 그대로.
- SSE: `event: board` + 빈 `data:` — 연결 즉시 · Redis 신호(조작 · 일정 변경 · 기준 정보 · outbox 상태) · 10초마다 → `hx-trigger="sse:board"` 로 `GET /board`. `event: kos_failed` + `data:` = `partials/board_toast_kos_failed.html` 렌더 HTML(넘기는 값 `room_title` · `customer_name` · `action` · `message`) → `sse-swap="kos_failed"` 로 `#day-toasts`. `id:` 없음 · `retry: 3000` · 15초 `: ping`. 앱(`/api/board/stream`)은 `board` = 스냅샷 JSON · `kos_failed` = `{eventId, visitId, action}`.
- 자리 템플릿 4개(`board.html` · `partials/board_main.html` · `partials/board_toast_error.html` · `partials/board_toast_kos_failed.html`)는 이 값만 쓰는 최소 마크업 — #231 이 바꾼다. 문구(`routers/board.py` `MESSAGES` · `KOS_FAILED_MESSAGE`)도 자리 값.
- 메뉴: 아이콘 줄 「시술」 · 헤더 탭 「시술 현황」 → `/board`(`menu.py` `HREFS`).

## 열린 쓰기 (경로 + 값)

| 동작 | 경로 | 값 조건 | HAR 근거 | 열림 |
|---|---|---|---|---|
| 호출 · 재호출 1 | `schedule/flow/v1/commands/change-tasks-room` | 고른 작업이 이미 다 카드 방이면 안 보냄 | `시술현황_방배정.har` · `방배정.har` | 열림 |
| 호출 · 재호출 2 | `schedule/flow/v1/commands/change-tasks-assignees` | `assigneeIds` = 시스템 계정 KOS id | `의사호출_2.har` | 열림 |
| 호출 3 | `schedule/flow/v1/commands/call-tasks-doctors` | 아직 호출 안 된 작업(새 호출) | `의사호출*.har` | 열림 |
| 수락 | `schedule/flow/v1/commands/change-tasks-doctors` | 수락한 의사 · 그 의사 토큰 | `의사호출_2.har` | 열림 |
| 첫 [시작] | `schedule/v1/commands/change-flow-step` | `step = PROCEDURE` 만 | `의사호출_2.har` · `시술완료_상태 copy.har` | 열림 |
| [종료] | `schedule/flow/v1/commands/change-tasks-complete` | `complete = true` 만 | `시술완료*.har` | 열림 |
| 재호출 3 | `call-tasks-doctors`(이미 WAITING) | — | 없음(OQ-09) | **닫힘** |
| 시작 취소 | `change-flow-step` `PROCEDURE_WAITING` | — | **있음 — 아래** | **닫힘(W6)** |
| 완료 취소 | `change-tasks-complete` `complete = false` | — | 없음(OQ-10) | **닫힘** |
| 귀가 대기 | `cancel-flow-tasks` · `change-flow-step` `PROCEDURE_DONE` | — | 없음(OQ-08) | **닫힘** |

- 닫힌 쓰기는 op 을 만들지 않고 `event_log.payload.kos = [{write, status: not_supported, reason}]` 로 남는다(로그에도 한 줄). 보내기 직전에도 `KosAdapter.supports_write` 가 같은 (경로 + 값)으로 다시 막는다.
- **`방배정.har`(`reference/2026-10-23-cc-overall-board/har/`)에 `change-flow-step` `step = PROCEDURE_WAITING`(200)이 있다 — 확인된 HAR 근거 있음 · 사용자 결정 대상.** SPEC-002 OQ-10 은 「HAR 없음」이라 적고 있어 근거가 생긴 셈이다. W6 결정대로 1차는 닫아 두었다. 열면 `writes.py` `OPEN_STEPS` 에 한 값을 더하는 한 줄이다(시작 취소에서 고객이 시술 대기로 돌아갈 때만 나감). 같은 HAR 들에 `PROCEDURE_DONE` · `complete=false` · `cancel-flow-tasks` 는 없다.
- 보내는 방식: **그 조작 직원 본인의 KOS 토큰**(`external_session` · 만료가 가장 늦은 것) · 브라우저 헤더 · `kos-client-uri = <web>/<tenant>/reservation/procedure`(HAR 의 쓰기 요청 모양) · 401 재-sign-in · 재시도 없음(`staff_client.KosStaffWriter`). 시스템 계정 경로는 고치지 않았다.
- dev 서버는 `is_demo` 연결 병원만 쓰기를 만든다(`services/board.py` `_vendor` = 동기화 조건과 같음).

## 계약에 없어 구현이 정한 것 (코디 확인)

1. **오류 본문** — 앱 JSON 은 #227 과 같은 `{detail, code, field}`. SPEC-002 는 cc 형식 `{error: {code, message}}` 를 적었지만 한 서버에 두 모양을 두지 않았다.
2. **[종료]를 이미 완료된 시술에** — 매트릭스에 줄이 없어 `task_not_doing`.
3. **확인 필요에 마취 · 호출이 둘 다면** 넘긴 비율이 큰 쪽 하나(카드당 `need` 하나).
4. **outbox 「sending」** — 새 상태값(enum · migration) 없이 「잡기 = pending → sent 조건부 UPDATE」로 했다. 보내다 실패하면 sent → pending(attempts+1). worker 가 잡은 뒤 죽으면 그 행은 sent 로 남아 확인 2번 · 오래된 sent(180초) 규칙이 다시 보내거나 failed 로 만든다.
5. **오래된 sent 기준 = 180초**(`OUTBOX_SENT_STALE_SECONDS`) — 조회 2번(20초)이면 다시 보내므로 넉넉히.
6. **확인 조건(`expect`) 모양** — 우리 형식 `{flow_step}` · `{tasks: {seq: {status | room_external_id | assignees_contain | doctors_contain}}}`. 조회가 덮지 않을 칸(`Guard`)도 여기서 나온다(업체를 모름).
7. **`doctorAssignedDateTimeUtc`** — SPEC 표는 「내부 응답에 키 없음 → 비워 둔다」인데 데모 응답에는 있어(작업 241 중 148) 받는다. `doctorCallDateTime` 은 소수 자리가 1 ~ 3 자리로 섞여 와 그대로 파싱.
8. **KOS 401 로 세션 끝내기**는 #227 서비스 함수와 같은 일을 outbox 안에서 한다(같은 transaction 에서 op 을 pending 으로 되돌리려고).
9. **SSE 「일정 조회가 값을 바꿨을 때」** — 받은 일정(우리 형식) 지문을 Redis(`day:board:digest:<병원>`)에 두고 다를 때만 보낸다. 쓰기 큐 확인이 상태를 바꿨을 때도 보낸다.
10. **전체 권한 계정** — `DAY_ADMIN_EMAILS`(쉼표 · 대소문자 무시)는 `services/sessions.require_permission` 한 곳에서만 보고, 그 길로 통과하면 `permission granted by DAY_ADMIN_EMAILS` 로그. `deploy/local.env.example` · compose env 에 이름만 · `deploy/local.env` 값은 넣지 않았다. 권한 표 시드 없음.

## 파일

새: `migrations/versions/20261106_0004_board.py` · `day/dtos/board.py` · `day/queries/board.py` · `day/services/board.py` · `board_rules.py` · `board_events.py` ·
`day/emr/kos/writes.py` · `day/routers/board.py` · `day/routers/api/board.py` · 자리 템플릿 4 · 테스트(`tests/day/board/` · `test_kos_board_contract.py`).
고침: `models/task.py`(closed_at · 유일) · `emr/{base,normalized,sync,outbox,factory}.py` · `emr/kos/{__init__,mapper,staff_client}.py` · `errors.py` ·
`services/{sessions,emr_sync}.py` · `main.py` · `menu.py` · `public.py` · `web_errors.py` · `common/config.py` · `deploy/{compose.local.yaml,local.env.example}` · 테스트 · 고정본.

## 남은 것

- **A8 실제 KOS 쓰기 1회**(호출 → 수락 → 첫 시작 → 종료 → confirmed) — 사용자 허락 · 데모 원장 계정(W8) 뒤. 수락 단계는 그 원장이 DAY 에 로그인해 있어야 나간다(규칙 24).
- **`PROCEDURE_WAITING` 열기 여부** — 위 HAR 근거 · 사용자 결정.
- #231 화면 — 위 조각 계약 · `day.js` 의 4xx 끼우기.
- 시술 완료 탭 방 묶음(OQ-03) · 상담 시술(OQ-13 — 데모에도 `consultationProcedures` 값 없음) · HAR 미확인 쓰기(OQ-08 · 09 · 10 complete false).
- 오늘 데모 카드에 남은 DAY 호출 1건 · 마취 1회차(실물 흔적 · KOS 무관).
- SPEC-002 반영(코디): `doctorAssignedDateTimeUtc` 받음 · 직원 배열 모양 확인 · `PROCEDURE_WAITING` HAR 근거.
