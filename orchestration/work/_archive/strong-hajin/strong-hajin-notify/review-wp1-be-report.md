# 코드 검수 — WP1-BE (사건 채널 SSE)

> reviewer(read-only) · 2026-10-08 · 대상 `strong-hajin-notify` 작업 트리의 backend 변경(수정 15 · 새 6) · base `d2a06fa`
> 계약: WORK-013 「Phase WP1-BE」 · Code Surface WP1 · SPEC-011 §4.1 · SPEC-008 §4.4 · 워커 리포트 `be-wp1-report.md`
> 약어: `B/` = `backend/src/ax_workspace/` · `BT/` = `backend/tests/`

## 0. 판정 — **WARN** (FAIL 0 · WARN 4)

체크박스 8개는 **코드로** 지켜졌다(리포트가 아니라 줄로 확인). 시험은 빈 단언이 아니라 계약 값을 직접 단언한다. 관련 파일만 돌려 **sqlite 121 passed · PostgreSQL 5 passed** 를 확인했다.
WARN 은 넷이다.
- 운영 인벤토리 drift 시험이 새 GET 라우트를 보지 못한다 — 초록인 채로 지나간다. 코디 판단에 동의한다
- 운영 SQL ①과 이미지 ② 사이에 생긴 행은 순번이 비어 영영 이어 받기 밖에 남는다
- 「회원 최대 순번보다 큰 커서」 가 SPEC Validation 과 다르게 처리된다
- 연결이 끊긴 뒤 허브 구독이 풀리는지 시험이 없다

### 실행한 것
- `git status` / `git diff`(backend) · 새 파일 전문 읽기
- `rg` 로 Code Surface WP1 패턴 다시 셈 · Starlette 1.6.0 의 `StreamingResponse` 끊김 처리 확인(uvicorn ASGI spec 2.3 → task group 이 끊김을 듣고 생성기를 취소한다)
- 시험(관련 파일만 · Makefile 타겟)
  - `make test-contract-serial FILES="tests/contract/test_events_stream.py tests/unit/test_user_event_hub.py tests/contract/test_production_route_registration.py tests/contract/test_notifications.py tests/contract/test_task_successors.py tests/architecture/test_operation_inventory.py tests/architecture/test_architecture.py tests/architecture/test_local_stack_targets.py tests/contract/test_external_inbox.py tests/contract/test_kakao_ingest_and_profile.py"` → **121 passed**
  - 워커의 격리 컨테이너 `ax-notify-pgtest`(127.0.0.1:55439 — 사용자 54329 아님)를 잠깐 켜서 `PYTEST_ADDOPTS='tests/integration/postgres/test_external_channels_postgres.py' POSTGRES_TEST_URL=… make test-postgres` → **5 passed**. 끝나고 다시 껐다(원래 상태 Exited)

---

## 1. 체크박스 8 — 코드로

| # | 계약 | 코드 | 판정 |
|---|---|---|---|
| 1 | 경로 · 머리 · `retry: 3000` · `ready` · 20초 ping | `B/entrypoints/http_events.py:37-44`(상수 · `Cache-Control: no-cache, no-transform` · `X-Accel-Buffering: no` · `Connection`) · `:86-90`(`text/event-stream; charset=utf-8`) · `:99-100`(retry → ready) · `:118-122`(`wait_for(queue.get, HEARTBEAT_SECONDS)` 시간 초과 → `: ping`. Python ≥3.12 라 `TimeoutError` 로 잡힌다) | PASS |
| 2 | 401 JSON · 403 · `/api/auth/me` 그대로 | `:79-84` — 출처 검사(`_same_origin` 공유 · Origin 없으면 통과 · 루프백 같은 포트 허용) → `current_principal` 의 `HTTPException` → 상태 그대로 JSON. 스트림을 열기 **전에** 돌아간다. `/api/auth/me` 무변경 | PASS |
| 3 | 사건 종류 · 메시지함 넷 이름/필드 그대로 | `events.py` `NOTIFICATION_UPSERTED` · `NOTIFICATION_READ` · `INBOX_EVENT_TYPES` · `to_payload` 는 빈 칸을 싣지 않는다 → 메시지함 사건 모양 불변(`test_user_event_hub` 왕복 단언) · `_live_frame`(`:133-154` — 넷은 페이로드 그대로 · read = `{v, **data}` · upserted = `{v, notification, created, replayed}` + `id:` · 모르는 것은 안 보냄) | PASS |
| 4 | 이어 받기 — 머리 > 쿼리 · 겹침 창 60초 · 기준 줄 대체 · 200 넘침 · **구독 먼저** · 같은 순번 한 번 | 머리 우선 `:56-67`(빈 머리면 쿼리 · 숫자 아님/음수면 「다시 붙었지만 기준 없음」 → `resync`) · 기준 줄 = `seq ≤ last` 가운데 최대(`B/platform/notifications.py:125-130` — 정확한 줄이 있으면 그 줄이 곧 최대이므로 SPEC 3-1 의 두 갈래를 쿼리 하나로) · 창 `floor = base.updated_at − 60s`(`:133`) · `seq > last OR (seq ≤ last AND updated_at ≥ floor)` 순번 순 `limit+1`(`:134-148`) · 넘침 → `overflow`(`B/modules/notifications.py:105`) · **`hub.subscribe` 가 DB 읽기보다 먼저**(`http_events.py:96` → `:105`) · `sent` 집합(`:97` · `:110` · `:139` · `:146`) | PASS(W-3 하나) |
| 5 | NOTIFY 짧은 페이로드 · API 가 DB 에서 읽음 | `publish_notification_upserted`(`B/platform/notifications.py:21-36` — `notification_id · seq · created` 만) · `emit` 이 flush 뒤 같은 세션에서 부름(`:93-96`) · SSE 가 `notification_event_item` 으로 읽고 인가(`B/bootstrap/application.py:2477-2480` → `modules/notifications.py:95-98`) | PASS |
| 6 | 큐 넘침 → `resync(dropped)` | `EventQueue.dropped`(`user_event_hub.py:44-49`) · `_offer` 가 버릴 때 표시(`:167-168`) · SSE 가 다음 사건 때 보고 내림(`http_events.py:123-125`). 넘침은 큐가 차 있을 때만 생기므로 「다음 사건」 은 반드시 온다 | PASS |
| 7 | 워커 게시 길 | `publish_user_event`(`B/platform/user_events.py:30-38`) — PG 면 그 트랜잭션의 `pg_notify` · 아니면 세션 `after_commit` 에서 같은 프로세스 허브로(`:41-53` · 롤백이면 버림) · 조립 `application.py:1098-1101`(PG 아닐 때만). meeting_worker 는 `create_workflow_application` 세션이라 같은 길. PG 시험이 「커밋 뒤에만 · 롤백은 없음」 을 고정 | PASS |
| 8 | 옛 WS 남김 · 회의 WS 무변경 | `http_inbox.py:340-` 라우트 그대로 + 넷만 거름(`:380-381`) · `http.py` diff 는 import 1 · 등록 1줄뿐(회의 WS `:1246` 무변경 — diff 에 meeting 0줄) | PASS |

## 2. 조용히 통과하는 자리

- **W-1 — 운영 인벤토리 drift 시험이 새 라우트를 못 본다(코디 판단에 동의).** `BT/architecture/test_operation_inventory.py:137` 은 라우트를 `('http.py', 'http_inbox.py')` 두 파일에서만 모은다. `GET /api/events/stream` 은 `http_events.py` 에 있어 `actual` 에 들지 않는다. 그래서 인벤토리에 행이 없어도 **초록**이다(직접 돌려 4 passed 확인)
  - **동의 근거**: 이 시험은 「선언된 HTTP 연산 전부가 인벤토리에 있다」 를 지키는 장치다(파일 머리 docstring · `http_count == len(actual)`). 라우트를 새 파일로 나누는 것은 지금 패턴(`http_inbox.py` 가 같은 이유로 목록에 들어간 선례 — `:133` 주석)과 같다. 목록에 더하지 않으면 다음 판들(WP2 알림 API)도 같은 구멍을 지난다
  - **고칠 것**:
    - 목록에 `http_events.py` 를 더한다(`:137` · 주석 `:133`)
    - 동시에 `docs/unified-operations-inventory.json` 에 `GET /api/events/stream` 행(`http_handler: events_stream` · `http_signature: (request: Request) -> StreamingResponse | JSONResponse`)과 `http_count` +1 을 더한다. 둘을 함께 해야 초록이다(행만 빼면 빨강)
    - 단, 이 시험은 `.workflow_application.` 속성 호출만 센다. `events_stream` 은 `workflow = request.app.state.workflow_application` 로 받아 부르므로 `http_application_calls` 는 비어 잡힌다 — 그대로 둬도 일관적이다
    - 시기: WP2 가 알림 API 행을 갱신할 때 함께 하는 것도 받아들일 수 있다. 그러면 WORK 체크에 「인벤토리 drift — `http_events.py`」 를 남기라
- 그 밖의 시험은 계약 값을 직접 단언한다. 시험 대역도 확인했다 — `BT/sse_stream_support.py` 는 ASGI 를 직접 부르고 `http.disconnect` 로 닫는다(TestClient 가 SSE 를 못 읽는 문제를 피했다)
  - 머리 셋의 글자(`BT/contract/test_events_stream.py:79-82`)
  - 401 JSON · 403 JSON(`:93-97`)
  - ping 두 번(`:116-117`)
  - 이어 받은 순번 목록 · 창 밖 옛 줄 제외(`:229-233`)
  - 머리 > 쿼리(`:253`)
  - 늦은 커밋(`:274-275`)
  - 기준 줄 대체(`:297`)
  - 넘침(`:329`)
  - `dropped` 뒤 최신 둘(`:369-370`)
  - 옛 WS 넷만(`:382-385`)
  - 빈 커서 = 첫 연결(`:389-395`)
- **W-4 — 끊긴 연결이 허브 구독을 풀었는지 시험이 없다.** `_stream` 의 `finally: hub.unsubscribe(...)`(`http_events.py:129-130`)는 코드로 맞다. Starlette 1.6 + uvicorn spec 2.3 에서 끊기면 task group 이 생성기를 취소하고, `await` 지점에서 `CancelledError` → `finally` 다. 그런데 이것이 깨지면 구독자가 쌓여도(회원마다 연결 수 증가 · 큐 200칸씩) 시험은 초록이다
  - **고칠 것**: `SseConnection` 을 닫은 뒤 `hub._subscribers[member]` 가 비었다는 단언 하나(`test_events_stream.py` 아무 시험 끝)

## 3. Code Surface WP1 — 다시 grep

| 패턴(`B/`) | WORK 표(d2a06fa) | 지금(다시 셈) | 처분 확인 |
|---|---|---|---|
| `user_events\.publish` | 9 / 6 | 9 / 6 | 메시지함 게시 9 자리는 손대지 않음 · `external_inbox.py:251`(깨우기) 그대로 |
| `UserEventType\.` | 12 / 6 | 17 / 9 | +5 = 알림 사건 생성(`platform/notifications.py`) · SSE 분기 · `INBOX_EVENT_TYPES` 정의. 기존 생성 11 자리 무변경 |
| `USER_EVENTS_CHANNEL` | 20 / 7 | 22 / 8 | 값 `ax_user_events` 그대로 · `user_events.py` 가 씀 |
| `UserEventHub\|user_event_hub` | 8 / 3 | 11 / 6 | |
| `@app\.websocket` | 2 / 2 | 2 / 2 | 메시지함 WS **남음**(넷만) · 회의 WS **무변경** |
| `StreamingResponse\|…\|text/event-stream` | 0 | 4 / 1 | `http_events.py` 만 |
| `publish_user_event` | — | 6 / 3 | 정의 · 알림 둘 |
| 라우트 등록 시험 | `test_production_route_registration.py` 갱신 | +14줄 — PRODUCTION 에 `/api/events/stream`(+ 옛 WS) · 세션 없이 401 | PASS |

워커 리포트 §2 의 수와 모두 같다. 표 밖 수정 넷(옛 WS 거름 · `schema_sync` 시퀀스 · Makefile 전제 검사 · `mark_read` 사건)도 계약에서 따라 나온 것이고 범위를 넘지 않는다. frontend diff 2파일은 WP1-FE 워커 몫이라 이번 판정에서 뺐다.

## 4. 마이그레이션 SQL 3파일 · 시퀀스 · schema_sync

| 항목 | 확인 | 판정 |
|---|---|---|
| 적용 순서 | ① `…-v2.sql`(트랜잭션 · `psql -1`) → ② 이미지 → ③ `….concurrent.sql`(트랜잭션 밖 · 사람이). 세 파일 머리에 같은 순서가 적혀 있고, 격리 · demo 는 `…-v2-index.sql` | PASS |
| 표가 없던 운영 | `CREATE TABLE IF NOT EXISTS notifications` 이 모델(`persistence.py` `NotificationRecord`)과 같다 — 칸 · `uq_notification_recipient_source` · FK 둘 · `ix_notifications_recipient_created` | PASS |
| 시퀀스 · 칸 | `CREATE SEQUENCE IF NOT EXISTS notification_seq` · `ADD COLUMN IF NOT EXISTS seq BIGINT` / `updated_at`(둘 다 nullable — 옛 이미지가 모른 채 돈다) | PASS |
| 옛 행 채우기 | `seq IS NULL` 행만 `created_at, id` 순으로 `nextval` · `updated_at = created_at` — 다시 돌려도 안전 | PASS(주석: 하위 쿼리 ORDER BY 뒤 `nextval` 평가 순서는 PG 가 보장하지 않는다 — 단순 스캔에선 실제로 지켜지고, 순서가 틀려도 「커지기만」 계약은 안 깨진다) |
| CONCURRENTLY | 트랜잭션 밖 · INVALID 인덱스 정리 · 되돌리기 `DROP INDEX CONCURRENTLY` 를 적었다. 격리판과 정의가 같다 | PASS |
| 되돌리기 | 이미지만 되돌린다 · 칸/시퀀스 additive | PASS |
| **W-2 — ①과 ② 사이의 행** | ①을 적용한 뒤 ②(새 이미지)가 뜨기 전, **옛 이미지가 쓰는 알림 행**(업무 요청 발송 · 수락)은 `seq` · `updated_at` 이 비어 남는다. 새 코드는 `seq IS NOT NULL` 만 이어 받고(`platform/notifications.py:127,139`), `_event_item` 은 `row.seq is None` 이면 버린다(`modules/notifications.py:112`) → 그 줄은 **영영 이어 받기 · SSE 밖**이다. WP2 의 목록 API 가 「순번 순」 이면 정렬도 흔들린다 | **고칠 것**: `…-v2.sql` 머리와 WORK 반영 순서에 「② 뒤 같은 파일을 한 번 더(채우기는 빈 행만 — 안전)」 를 적는다. 아니면 ②의 `emit` 외에 순번이 빈 행을 다루는 규칙을 WP2 에 넘긴다 |
| schema_sync | PG 면 모델 시퀀스를 칸보다 먼저 더한다(`schema_sync.py:27-32`) · 기존 표 인덱스는 지금 규칙대로 파일로 | PASS(주석: `Base.metadata._sequences` 는 SQLAlchemy 비공개 속성이다 — 판이 오르면 깨질 수 있다. 한 줄 주석이나 공개 경로로) |
| Makefile 전제 검사 | `notification_seq` 와 `notifications.seq` 가 없으면 local-stack 이 서지 않는다(`Makefile:334`) — `psql -tA` 출력 `notification_seq|seq` 와 `grep -qx` 가 맞다 · 시험 1줄 | PASS |

## 5. 그 밖에 본 것

- **W-3 — 커서가 그 회원의 최대 순번보다 클 때.** SPEC-011 Validation(:551)은 「회원의 가장 큰 순번보다 크면 이어 받기 없이 `resync`」 다. 그런데 구현은 기준 줄 = 「`seq ≤ last` 가운데 최대」 = 그 회원의 최신 줄이 되어, 그 줄 기준 60초 창 안의 줄을 **이어 받기로 다시 보낸다**(`platform/notifications.py:125-148`). 화면이 (id · 순번)으로 거르니 해는 작다. 하지만 계약 문장과 다르다
  - 고칠 것(택일): 코드에서 `last > max(seq)` 면 `no_base`(= `resync` 만)로 가르거나, SPEC Validation 문장을 「겹침 창 규칙 그대로」 로 고친다(코디 판단). 지금 시험은 이 경우를 고정하지 않는다
- 세션이 스트림 도중에 끝나도(로그아웃 · 만료) 연결은 열려 있는 동안 계속 민다 — 시작할 때 한 번만 인가한다. 옛 WS 와 같고 받는 사람은 그 회원 자신이며, 화면이 로그아웃 때 닫는다(§4.1-6). 참고만
- `workflow._settings.web_origin`(비공개 속성 접근)은 옛 WS(`http_inbox.py:350`)와 같은 패턴이다. 참고만
- 경계: `http_events.py` 는 `platform` 을 import 하지 않는다 — `test_architecture.py` 16 passed
- 연결마다 `sent` 집합이 커진다(알림 순번 수만큼 — 작다). 참고만

---

## 6. 목록

### FAIL
없음.

### WARN

| # | 파일:줄 | 고칠 것 |
|---|---|---|
| **W-1** | `backend/tests/architecture/test_operation_inventory.py:133,137` · `docs/unified-operations-inventory.json` | 파일 목록에 `http_events.py` + 인벤토리 `GET /api/events/stream` 행 · `http_count` +1(함께). 코디 판단에 **동의** — 늦어도 WP2 알림 API 행과 같이 |
| **W-2** | `backend/migrations/manual/2026-10-08-notifications-v2.sql`(머리 주석) · WORK-013 반영 순서 | ①과 ② 사이 옛 이미지가 쓴 행의 빈 `seq` — 「② 뒤 같은 파일 한 번 더」 를 절차로 |
| **W-3** | `backend/src/ax_workspace/platform/notifications.py:125-148` · SPEC-011 Validation :551 | 커서 > 회원 최대 순번이면 `resync` 만(코드) 또는 SPEC 문장 정정 + 시험 하나 |
| **W-4** | `backend/tests/contract/test_events_stream.py` | 연결을 닫은 뒤 허브 구독자가 비었다는 단언 하나 |

### 사용자에게 물을 것
없음.
