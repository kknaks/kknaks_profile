# #230 검수 FAIL 반영(fix1) — 백엔드 결과 보고

## #231 영향 (먼저 읽을 것)

조각 계약의 라우트 · 조각 이름 · 기존에 넘기던 값은 그대로다. **더한 것만** 있다. `templates/` · `static/` · `day.js` 는 건드리지 않았다.

| 무엇 | 바뀐 점 | #231 이 할 일 |
|---|---|---|
| SSE 새 이벤트 `session_expired` | `GET /board/stream` · `/api/board/stream` 이 신호마다 · 10초마다 세션 · 권한을 다시 본다. 죽었으면 `event: session_expired`(data = `unauthorized` · `session_expired` · `forbidden`)를 한 번 보내고 닫는다 | 받으면 `/login`(만료면 `?reason=session_expired`)으로 보낸다. 안 받아도 판은 더 안 오고, 다음 `GET /board` 가 #229 규칙으로 로그인 화면을 준다 |
| SSE 연결 수명 | 세션 만료와 1시간 중 이른 쪽에서 서버가 닫는다(살아 있는 세션이면 `session_expired` 없이) | 없음 — EventSource 가 `retry: 3000` 으로 다시 붙는다 |
| 셸 값 `is_admin` | `WebView.is_admin` · `MeView.is_admin` · `/api/auth/me` 의 `is_admin` | 권한으로 버튼을 숨길 때 `permissions` 와 함께 본다(true = 모든 키 · edit) |
| `snapshot.sync.lastError` | 이제 실제 값(`timeout` · 예외 이름 · 성공 뒤 null). `lastOkAt` 도 채워진다 | 「KOS 동기화 멈춤」 표시에 쓸 수 있다 |
| `card.need.overSec` | 기준을 넘긴 초(새 칸). `inbox.need` 정렬이 이것의 큰 순으로 바뀌었다 | 없음 — 순서는 서버가 정한다 |
| 웹 폼 모르는 칸 | 400 `invalid_request` + `X-Day-Error`(라우트마다 정한 칸과 `csrf_token` 만 허용) | 폼에 다른 칸을 싣지 않는다 |

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **268 passed** · 148 deselected(경고 1 = fastapi testclient 라이브러리 경고, 기존) |
| `scripts/test.sh -q` | **416 passed** (35s) — frontend 가 같은 워크트리에서 더한 테스트 포함 |
| `uv run ruff check backend scripts` · `ruff format --check backend` | All checks passed · 141 files already formatted |
| compose | down 안 함. `--profile app up -d --build --wait api worker scheduler` → `/health/ready` ok |
| 실물(조회만) | worker 10초 회차 `emr schedules … done`(이제 방문 잠금을 잡고 반영) · Redis `day:board:sync:<병원>` 에 `last_ok_at` 기록 · `last_error` 빔. KOS 쓰기 없음 |

## FAIL

### F1 — SSE 세션 다시 보기 · 수명
- `services/sessions.still_allowed(session, current, key, level, now)` — 세션 한 줄(PK) `check_alive` + `require_permission`.
- `routers/board.py`:
  - `stream_guard(current)` — 자기 DB 세션을 잠깐 열고 닫는다. 연결 내내 쥐지 않는다.
  - `board_stream_events(..., guard, expires_at, tick_seconds, max_seconds)` — 값(`board` · `kos_failed`)을 보내기 전과 10초마다 `guard` 를 부른다.
  - 실패면 `event: session_expired` + 오류 코드를 보내고 끝낸다.
  - 수명은 `min(expires_at, 1시간)` 이다(`STREAM_MAX_SECONDS`).
  - 웹 · 앱 스트림 둘 다 건다.
- 그래서 로그아웃 · 만료(KOS 401 로 당겨진 것 포함) · 권한 회수 뒤에는 스냅샷도 `kos_failed` 토스트(고객 이름)도 나가지 않는다.
- 테스트(infra · `test_board_sse.py` +5):
  - 앱 스트림을 연 뒤 로그아웃 → 다음 tick 에 `session_expired/unauthorized` 로 끝나고 board 없음;
  - 권한을 거두면 → `forbidden`;
  - KOS 401 로 만료되면 → `session_expired`;
  - 웹 스트림은 로그아웃 뒤 `kos_failed` 를 보내지 않음;
  - 수명이 지나면 그냥 닫음.

### F2 — query-count
- `tests/day/board/test_board_queries.py`(infra) — `load_world` 를 방문 2개 · 11개로 돌린다. 각 방문에 작업 2 · 집도의 · 호출(+ 호출 작업 · 수락) · 마취 · 흐름 이력 · 쓰기 큐 · 카드 순서를 채운다. `before_cursor_execute` 로 센 결과는 **둘 다 11개**이고 같다. 숫자를 고정해 쿼리가 늘면 깨진다.
- `queries/board.py` 독스트링이 이 파일을 가리키고, 이제 그 파일이 있다.

## WARN

| | 고친 것 | 테스트 |
|---|---|---|
| W1 전체 권한 | 판단은 `sessions.is_admin_email` 한 곳이다. `require_permission` · `MeView.is_admin` 이 부른다. `/` 는 `sessions.can_enter(permissions, is_admin)` 를 쓴다(권한 행 0인 관리자도 들어감). `WebView` · `/api/auth/me` 에 `is_admin` 을 실었다(JSON 칸 하나 추가 — 기존 칸 그대로) | `test_전체_권한_계정은_권한_행_없이_통과` — 전/후 `/` 403 → 200/303 · `me.is_admin` · `board.accept` 수락까지 · 로그 줄(`board.accept` 키) · 로그에 이메일 없음 |
| W2 확인 필요 정렬 | `need.overSec`(기준 넘긴 초) 큰 순. 마취/호출 중 하나 고르기는 그대로(넘긴 비율 — 결정 3) | `test_확인_필요_칸은_넘긴_시간_긴_순`(호출 9분 = 240초가 마취 21분 = 60초보다 위) |
| W3 sync | 일정 회차가 `done` 이면 시각을 쓰고 오류를 지운다. `error` · `timeout` 이면 오류 이름만 쓰고 시각은 그대로다(Redis 해시 `day:board:sync:<병원>`, TTL 1일). `RunResult.error_kind` 는 업체 응답 문구를 싣지 않는다. `services.board.board()` 가 읽어 스냅샷에 싣는다(`load_world` 는 DB 만 — 쿼리 수 그대로) | 실물 Redis 확인. 단위 — 스냅샷 모양 테스트는 기존 |
| W4 조용한 생략 | `Skipped(kind, reason="no_external_id")`. 세 경우를 `payload.kos = [{write, status: "skipped", reason}]` + 로그 한 줄로 남긴다: 방문 외부 id 없음(모든 동작), 호출의 방 외부 id 없음, 수락의 의사 외부 id 없음. `ActionResult.skipped`. 동기화 연결이 아예 없는 병원(`_vendor` None)은 KOS 쓰기 자체가 없는 병원이라 기록하지 않는다 — 계약상 의도된 생략 | `test_외부_id_가_없으면_skipped_로_남긴다`(호출 3쓰기) · `test_의사_외부_id_가_없으면_수락_쓰기는_skipped` |
| W5 a 토큰 대기 | `OUTBOX_TOKEN_WAIT_SECONDS`(기본 **1800초**). 마지막으로 pending 이 된 뒤 그만큼 토큰이 없으면 failed(`no staff token in time`)가 된다. 뒤 쓰기는 막히고, `kos_failed` 재료가 되며, 동기화 가드가 풀려 KOS 값을 따른다. 순수 함수 `decide_token_wait` | 단위 1 + infra `test_토큰을_너무_오래_기다리면_failed_뒤_쓰기도_막힘` |
| W5 사소 | `_block_later` 가 `deleted_at IS NULL` 만 막는다 | `test_지운_뒤_쓰기는_막힘_처리하지_않는다` |
| W5 b 보내는 중 재전송 | 코드 변경 없음(요청 상한 15초 < 확인 2번 20초라 드묾). **A8 첫 실제 쓰기 때 `call-tasks-doctors` 를 두 번 보냈을 때 KOS 동작을 같이 볼 것** — 남은 것에 둔다 | — |
| W6 조용히 통과 | 아래 표 | 아래 표 |
| W7 동기화 잠금 | 일정 반영은 반영 대기 쓰기를 읽기 전에 그 방문들의 `board:<visit_id>` advisory lock 을 정한 순서로 잡는다(`emr/sync.lock_visits` · 키 함수 `visit_lock_key` 를 조작과 같이 씀). 조작은 방문 하나만 잡으므로 교착이 없다. 조작이 commit 하기 전에는 동기화가 기다린다. 「진행 중 마취 하나」 · 「(호출, 시술)당 수락 하나」는 lock 으로 지킨다(DB 제약은 이번에 안 더함 — 낮음) | `test_board_locks.py`(조작이 잡은 방문은 기다림 · 다른 방문은 안 막음) |

### W6 「조용히 통과」 표 → 보강

| 자리 | 보강 |
|---|---|
| 시작 검사 순서 | 진행 중이면서 수락 안 된 호출에 묶인 시술을 더했다 → `task_not_waiting`. 두 검사 순서를 바꾸면 깨진다 |
| `nothing_to_accept` | 이미 시작한 시술 9를 판 작업 목록에 넣었다(`r3.tasks(v)` 에 있음을 단언) |
| 닫힌 쓰기 | 완료 취소 · 귀가 대기도 `payload.kos` 의 (write, `not_supported`)를 단언한다 |
| 웹 CSRF | HTMX 200 + `HX-Reswap: none` + 문구 · 일반 요청 403 · 같은 쿠키 JSON 경로는 403 `csrf_failed` |
| 웹 400 · 404 | `test_웹_400_404_도_오류_토스트_조각` — 404 `not_found` · 400 uuid 아님 · 400 모르는 칸(아무것도 안 바뀜) |
| 매트릭스 빈 줄 | 401 `session_expired`(읽기 · 쓰기) · 카드 0장 200 · 판 카드 아닌 방문/작업 404 · KOS 취소 작업 404 · `visit_home` 이 종료 · 시작 취소 · 완료 취소 · 마취 종료 · 재호출 · 수락에도 걸림 · 수락 `call_closed` · 재호출 `doctor_not_listed` |
| 웹 폼 모르는 칸 | 코드 고침(`routers/board._fields(request, *allowed)`) + 위 테스트 |
| `DAY_ADMIN_EMAILS` | 로그 줄 · `board.accept` 통과 테스트(W1) |

## 파일

- 고침:
  - backend: `common/config.py`(`outbox_token_wait_seconds`) · `day/dtos/auth.py` · `day/dtos/board.py` · `day/session.py` · `day/schemas/auth.py` · `day/routers/login.py` · `day/routers/api/auth.py` · `day/routers/board.py` · `day/routers/api/board.py`
  - services: `day/services/sessions.py` · `board.py` · `board_rules.py` · `board_events.py` · `emr_sync.py`
  - emr: `day/emr/outbox.py` · `day/emr/sync.py`
- 테스트:
  - 새로: `tests/day/board/test_board_queries.py` · `test_board_locks.py`
  - 고침: `test_board_sse.py` · `test_board_api.py` · `test_board_rules.py` · `conftest.py`(`email`) · `tests/day/emr/test_outbox.py` · `test_outbox_rules.py`
- migration: 새 것 없음(0004 그대로).

## 남은 것

- A8 실제 KOS 쓰기 1회 — 사용자 허락과 W8 원장 계정이 필요하다. 그때 W5 b(같은 호출을 두 번 보냈을 때 KOS 동작)도 같이 본다.
- `PROCEDURE_WAITING`(`방배정.har` 근거) 열지 여부 — 사용자 결정.
- SPEC 개정(코디): 오류 본문 `{detail, code, field}` · 완료된 시술 [종료] = `task_not_doing` · `doctorAssignedDateTimeUtc` · `need.overSec` · SSE `session_expired` · `me.is_admin`.
- 8번(KOS 401 세션 끝내기가 `sessions.end_session_on_kos_401` 과 outbox `_end_session` 으로 중복) — 낮음, 이번엔 안 모음.
- 「진행 중 마취 하나」 · 「수락 하나」 DB 제약 — lock 으로 충족, 낮음.
