# 리뷰 리포트 — day-data-architecture / code · #230 fix1 재검수 (2026-11-06)

대상: 같은 워크트리의 미커밋 #230 fix1(백엔드). 근거 문서는 `backend-230-fix1-instructions.md` · `backend-230-fix1-report.md`, 앞 리포트는 `review-230-report.md` 다.
#231 fix1 파일(`templates/` · `static/day.js` · `tests/day/web/`)은 같은 시각에 frontend 가 고치는 중이라 판정에서 뺐다.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. **compose 는 건드리지 않았다.** 테스트는 `-m "not infra"` 만 돌렸고, 전체 416 은 수정 리포트 · 코디 확인 수치를 따른다.

## 판정: PASS (FAIL 0 · 이번 범위 WARN 0)

F1 · F2 와 W1 ~ W7(W5 b 는 의도대로 A8 로 넘김)이 닫혔다. 「#231 영향」 표도 코드와 맞는다. 아래 「참고」 둘은 판정 밖이다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **270 passed · 1 failed · 148 deselected / 3.3s** |
| 실패 1건 | `tests/day/web/test_board_page.py::test_확인_필요_마취_3상태_수납_필요_귀가_대기`(`:102` 귀가 대기 잠금 정규식) — **#231 fix1 파일**이다. `board_parts.html` 이 이 검수 도중(13:53)에도 바뀌고 있었다. #230 백엔드 결과가 아니라 판정에서 뺐다. #231 fix1 재검수에서 다시 볼 것 |
| `uv run ruff check backend scripts` | All checks passed |

## F · W 별 확인

| | 판정 | 근거 |
|---|---|---|
| F1 SSE 세션 · 권한 재확인 · 수명 | **닫힘** | 아래 따로 |
| F2 query-count | **닫힘** | `tests/day/board/test_board_queries.py`(infra) — 방문 2개 · 11개(작업 · 집도의 · 호출 · 수락 · 마취 · 이력 · 쓰기 큐 · 순서)로 `before_cursor_execute` 를 센다. 둘 다 **11** 로 같고, 숫자를 고정해 쿼리가 늘면 깨진다. `queries/board.py:4` 독스트링이 이제 사실이다 |
| W1 전체 권한 | **닫힘** | 판단은 `sessions.is_admin_email`(`:130`) 한 곳이다. `require_permission`(`:166`) · `MeView.is_admin` 이 부른다. `/` 는 `can_enter(permissions, is_admin)`(`login.py:169`). `WebView.is_admin`(`dtos/auth.py:78`) · `MeView`(`:88`) · `/api/auth/me`(`schemas/auth.py:84`)에 실었다. 테스트: 전/후 `/` 403 → 통과 · `board.accept` · 로그 줄 · 로그에 이메일 없음 |
| W2 확인 필요 정렬 | **닫힘** | `need.overSec`(`board_rules.py:306-308`) 내림차순(`:521`). 「호출 9분(240초) > 마취 21분(60초)」 테스트 |
| W3 sync 값 | **닫힘** | 일정 회차 `done` → `record_sync(ok_at=now, error=None)`(`emr_sync.py:213`), `error` · `timeout` → 오류 이름만(`:216` · `error_kind = type(exc).__name__` · 업체 문구 없음). `board()` 가 Redis 에서 읽어 스냅샷에 싣는다(`load_world` 쿼리 수 그대로) |
| W4 조용한 생략 | **닫힘** | 외부 id 없음 세 경우 → `payload.kos = [{write, status: "skipped", reason: "no_external_id"}]` + 로그. 연결 없는 병원(`_vendor` None)은 KOS 쓰기 자체가 없는 병원이라 기록하지 않는다 — 받아들임. 테스트 2 |
| W5 a 토큰 대기 상한 | **닫힘** | `OUTBOX_TOKEN_WAIT_SECONDS`(1800초) · 순수 함수 `decide_token_wait` → `failed`(`no staff token in time`) → 뒤 쓰기 막힘 · `kos_failed` · 가드 풀림. 단위 + infra |
| W5 b 보내는 중 재전송 | **넘김(받아들임)** | 요청 상한 15초 < 확인 2번 20초라 드물다. A8 첫 실제 쓰기 때 `call-tasks-doctors` 를 두 번 보냈을 때 KOS 가 어떻게 하는지 확인 — 남은 것에 적혀 있다 |
| W5 사소 | **닫힘** | `_block_later` 가 `deleted_at IS NULL` 만. 테스트 1 |
| W6 조용히 통과 | **닫힘** | 시작 409 순서(진행 중 + 미수락 호출 시술을 더함 → 순서를 바꾸면 깨짐) · `nothing_to_accept`(시술 9 를 판 목록에 넣고 단언) · 닫힌 쓰기 셋 다 `payload.kos` 단언 · 웹 CSRF 상태 · 웹 400/404 토스트 조각 · 매트릭스 빈 줄 전부 · 웹 폼 모르는 칸(`routers/board._fields` · 코드도 고침) · `DAY_ADMIN_EMAILS` 로그 |
| W7 동기화 잠금 | **닫힘** | `emr/sync.lock_visits`(`:1244-1254`) — 반영 대기 쓰기(`pending_guards`)를 읽기 **전에** 그 방문들의 `board:<visit_id>` 잠금을 잡는다(`:886-889`). 키 함수 `visit_lock_key` 를 조작(`services/board.py:104`)과 같이 쓴다. 조작은 방문 하나만 잡으므로 교착이 없다. 테스트 `test_board_locks.py` |

### F1 — SSE

- `routers/board.py:235-287` `board_stream_events`: 값(`board` · `kos_failed`)을 보내기 전과 10초마다 `guard` 를 부른다. 죽었으면 `event: session_expired` + 코드(`unauthorized` · `session_expired` · `forbidden`)를 보내고 `return`. 수명은 `min(세션 expires_at, 1시간)`이다.
- 루프가 메시지에만 매달리지 않는다: `board_events.subscribe`(`:142-161`)는 1초마다 메시지가 없으면 `{"type": "tick"}` 을 내서 10초 검사 · 수명 마감이 신호 없이도 돈다(확인함).
- `stream_guard`(`:214-221`)는 검사마다 DB 세션을 잠깐 열고 닫는다. 연결 내내 쥐지 않는다. `still_allowed`(`sessions.py:177-195`) = 세션 PK 한 줄 `check_alive` + `require_permission`(전체 권한 포함).
- 웹(`routers/board.py:305-310`) · 앱(`routers/api/board.py:116-118`) 둘 다 `guard` · `expires_at` 을 건다.
- 테스트(`test_board_sse.py` +5): 로그아웃 → `unauthorized` · 권한 회수 → `forbidden` · KOS 401 로 만료 → `session_expired` · 웹 스트림은 로그아웃 뒤 `kos_failed` 없음 · 수명이 지나면 닫힘. 마지막 청크를 정확한 문자열로 단언한다(`:206 · 221 · 233 · 260`).
- 첫 `board` 는 검사 없이 나간다. 연결 때 의존성(`required_web_view` · `current_session` + `_allowed`)이 방금 확인했으니 맞다.

## 「#231 영향」 표 — 정확한가

**정확하다.** 표의 여섯 줄을 코드와 대조했다.

| 표의 줄 | 코드 |
|---|---|
| SSE `session_expired`(data = 코드) | `routers/board.py:269` · 테스트 문자열 일치 |
| 연결 수명 `min(만료, 1시간)` · 살아 있으면 이벤트 없이 닫음 | `:254-256 · 271-272` |
| `is_admin`(WebView · MeView · `/api/auth/me`) | `dtos/auth.py:78 · 88` · `schemas/auth.py:84` · `session.py:116` |
| `sync.lastError` · `lastOkAt` 실제 값 | `emr_sync.py:213-216` → `board_events.record_sync` |
| `card.need.overSec` · `inbox.need` 정렬 | `board_rules.py:306-308 · 521` |
| 웹 폼 모르는 칸 400 + `X-Day-Error` | `routers/board.py:145-157` |

#231 쪽 할 일(`session_expired` 받으면 `/login` 이동 · `is_admin` 으로 버튼 판단)은 #231 fix1 몫이다.

## 조용히 통과하는 자리

새로 찾은 것 없음. 보강된 테스트는 고친 줄을 되돌리면 깨지는 구조다(시작 순서 · `nothing_to_accept` · query-count 고정 숫자 · SSE 마지막 청크 문자열 · 잠금 대기).

## 참고 (판정 밖)

1. **웹 폼의 모르는 칸 검사는 urlencoded 만 본다** — `_fields`(`routers/board.py:151-152`)는 `Content-Type` 이 urlencoded 가 아니면 `{}` 를 돌려준다. multipart · JSON 본문을 웹 조작 라우트에 보내면 칸이 없는 요청이 된다. 대개 `taskIds` 없음 → 400 이라 실해는 없다. htmx 는 늘 urlencoded 다. 낮음.
2. **`lock_visits` 의 잠금 순서** — `select(pg_advisory_xact_lock(k)) FROM (… ORDER BY k)` 는 PostgreSQL 이 바깥 함수 호출 순서까지 보장하지 않는다. 다만 지금은 순서가 중요하지 않다: 같은 병원의 일정 반영은 Redis 잠금으로 하나만 돌고, 조작은 방문 하나만 잡는다. 그래서 교착이 생길 조합이 없다. 나중에 조작이 방문 둘 이상을 잡게 되면 그때 정렬을 보장하는 방식(키마다 따로 `execute`)으로 바꿀 것.
3. 남은 것(수정 리포트와 같음): A8 실제 KOS 쓰기 1회(W5 b 같이) · `PROCEDURE_WAITING` 사용자 결정 · SPEC-002 개정 목록(오류 본문 · `task_not_doing` · `doctorAssignedDateTimeUtc` · `overSec` · SSE `session_expired` · `me.is_admin`) · KOS 401 세션 끝내기 중복 구현(낮음).
