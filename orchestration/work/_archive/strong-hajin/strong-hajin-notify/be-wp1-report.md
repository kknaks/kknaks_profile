# WP1-BE 결과 보고 — 사건 채널(서버)

## 상태: done (커밋 없음 · 워크트리에 변경만)

- SSOT: WORK-013 「Phase WP1-BE」 · SPEC-011 v0.2.2 §4.1 · SPEC-008 v0.7.0 §4.4
- 워크트리: `strong-hajin-notify` · base `d2a06fa`
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `BT/` = `backend/tests/`

## 1. 계약 체크박스 — 8/8

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **`GET /api/events/stream`** — `text/event-stream` · `Cache-Control: no-cache, no-transform` · `X-Accel-Buffering: no` · 첫 `retry: 3000` + `event: ready` · 20초 `: ping` | `B/entrypoints/http_events.py` — 상수 `HEARTBEAT_SECONDS`(:37) · `RETRY_MILLISECONDS`(:39) · `STREAM_HEADERS`(:40, `Connection: keep-alive` 포함)<br>라우트 `register_event_routes` · `events_stream`(:75-90)<br>스트림 `_stream`(:93-): `retry` → `ready{v, server_time}` → 루프(`wait_for(queue.get, HEARTBEAT_SECONDS)` 시간 초과면 `: ping`)<br>등록 `B/entrypoints/http.py:2800` |
| 2 | **인증** — 세션이 없으면 `401` JSON(스트림 없음) · `Origin` 이 다르면 `403` · `/api/auth/me` 는 그대로 | `http_events.py:78-84`<br>옛 WS 의 `_same_origin`(`http_inbox.py`) 을 그대로 쓴다 → 403 JSON. 그다음 `current_principal`(세션 쿠키 / 개발 페르소나 — REST 와 같은 이음새)의 `HTTPException` → 그 상태 그대로 JSON<br>검사 순서는 옛 WS 와 같다(출처 → 사람). `/api/auth/me` 는 손대지 않았다 |
| 3 | **사건 종류** — 메시지함 넷은 이름·필드 그대로 · `notification.upserted`(id = 순번) · `notification.read` · `resync` | 정의: `B/modules/external_channels/events.py` — `NOTIFICATION_UPSERTED`(:44) · `NOTIFICATION_READ`(:46) · `INBOX_EVENT_TYPES`(:50). `UserEvent` 에 `notification_id` · `seq` · `created` 칸(빈 값은 페이로드에 싣지 않는다 → 메시지함 사건 모양 불변). 「메시지함 전용이 아님」을 docstring 에 적음<br>내보내기: `http_events.py` `_live_frame`(:133-)<br>• 메시지함 넷 = NOTIFY 페이로드 그대로 `{v, type, member_id, …}`<br>• `notification.read` = `{v, **data}`<br>• `notification.upserted` = `{v, notification, created, replayed}` + `id:`<br>• 모르는 종류는 내보내지 않는다<br>`notification` 항목은 지금 `NotificationView` + `seq` · `updated_at`(`B/modules/notifications.py` `NotificationEventItem` — §4.5-2 모양은 WP2)<br>`notification.read` 를 지금 단건 읽음에서 낸다: `B/platform/notifications.py:154`(`mark_read`) |
| 4 | **이어 받기** — `Last-Event-ID` 머리 > `?last_event_id=` · 겹침 창(−60초) · 기준 줄 없음 → 그 순번 이하 가장 큰 줄 / 그것도 없으면 `resync(reconnected)` · 200 넘으면 `replay_overflow` · 구독 먼저 · 같은 순번 한 번 | **머리 우선**: `_last_event_id`(`http_events.py:56-72`). 빈 값은 첫 연결이고, 숫자가 아니면 「다시 붙었는데 기준 없음」 → `resync(reconnected)`<br>**겹침 창**: `SqlAlchemyNotificationRepository.replay_after`(`B/platform/notifications.py:117-148`). 기준 = 순번 ≤ 마지막 가운데 가장 큰 순번 줄. 마지막 순번의 줄이 있으면 그 줄이고, 없으면 이하 최대 줄이다(쿼리 하나)<br>**상한·창**: `REPLAY_LIMIT = 200` · `REPLAY_OVERLAP = 60s`(`B/modules/notifications.py:56-58`)<br>**결과 갈래**: `NotificationApplication.replay`(:100-108) — `no_base` / `overflow` / `replayed`(인가된 줄만)<br>**구독 먼저**: `hub.subscribe` 가 DB 읽기보다 앞이다(`http_events.py:96`)<br>**한 번만**: `sent` 집합으로 이어 받기와 실시간의 같은 순번을 거른다(`:139` · `:146`) |
| 5 | **NOTIFY 페이로드** — 알림은 `{v, type, member_id, notification_id, seq, created}` 만 · SSE 를 내는 API 가 DB 에서 읽는다 | 내기: `publish_notification_upserted`(`B/platform/notifications.py:21-36`), `emit` 이 같은 트랜잭션에서 부른다(:96)<br>읽기: `WorkflowApplication.notification_event_item`(`B/bootstrap/application.py:2477`) → `NotificationApplication.event_item` — 받는 사람 확인 + 지금 인가 |
| 6 | **큐 넘침** → 그 연결에 `resync(dropped)` | `EventQueue`(`B/platform/user_event_hub.py:44-49`, `dropped` 표시). `_offer` 가 넘쳐 버릴 때 표시한다(:168)<br>SSE 가 다음 사건 때 표시를 보고 `resync(dropped)` 를 내고 표시를 지운다(`http_events.py:123-125`). 200칸 · 회원 거르기 · 1초 묶음은 그대로 |
| 7 | **워커 게시 길** — meeting_worker 가 같은 함수로(import 경로 · 세션) | `publish_user_event(session, UserEvent)`(`B/platform/user_events.py:30-38`) — PostgreSQL 이면 그 트랜잭션의 `pg_notify` 이고, 프로세스는 가리지 않는다<br>알림은 `SqlAlchemyNotificationRepository(session).emit` 이 순번을 받고 같은 세션에서 게시한다 → meeting_worker(`create_workflow_application` 세션)가 WP2 생성기로 부르면 그대로 닿는다<br>워커와 같은 `make_session_factory` 세션으로 커밋 뒤에만 나가고 롤백은 버린다는 것을 PG 시험으로 고정했다<br>sqlite(시험)는 NOTIFY 대신 세션 `after_commit` 에서 같은 프로세스 허브로 흘린다(`LOCAL_DISPATCH_KEY` — 조립 `B/bootstrap/application.py:1098-1101`, 롤백이면 버림) |
| 8 | WS `/api/inbox/stream` 라우트 **남김** · 회의 WS 손대지 않음 | `B/entrypoints/http_inbox.py` — 라우트는 그대로. **메시지함 넷만** 민다(:380 — 알림 사건은 옛 화면에 보내지 않는다). docstring 에 「화면은 더 쓰지 않음 · Rollback 여지」<br>회의 WS(`http.py:1245`)는 무변경 |

**스키마 — 이어 받기 틀에 필요한 만큼만**: 알림 표에 `seq` · `updated_at` 칸 + 전역 시퀀스 `notification_seq` + 인덱스 `ix_notifications_recipient_seq`. 나머지 칸(theme · item · relation · data · target …)은 WP2 몫이다.

- 모델: `B/platform/persistence.py` — `NOTIFICATION_SEQ`(:1303) · 인덱스(:1313) · `seq`(:1330) · `updated_at`(:1332)
- 순번 받기: `next_notification_seq`(`B/platform/notifications.py:14-18`) — PG 는 `nextval`, sqlite 는 최댓값 + 1
- 운영 SQL(새 파일 셋)
  - `backend/migrations/manual/2026-10-08-notifications-v2.sql` — 트랜잭션 판. 표 `IF NOT EXISTS`(지금까지 마이그레이션 파일이 없던 표) · 시퀀스 · 칸 · 옛 행 순번(`created_at, id` 순)/`updated_at` 채우기 · 재적용 가능
  - `…-v2-index.sql` — 격리 검증용 인덱스
  - `….concurrent.sql` — 운영 인덱스
- demo sync: `B/bootstrap/schema_sync.py:28-33` — PG 에 없는 **시퀀스도 더한다**(칸보다 먼저). 기존 표 인덱스는 지금 규칙대로 더하지 않는다 → 인덱스 SQL 파일로
- `make local-stack` 전제 검사: `Makefile:334` — `notification_seq` 시퀀스 + `notifications.seq` 칸이 없으면 시작을 거절하고 `sync-demo-schema` 를 안내한다. 시험 `BT/architecture/test_local_stack_targets.py` 에 단언 1줄

## 2. Code Surface 표 대비 — 닿은 자리

시작 시 `d2a06fa` 를 같은 패턴으로 다시 셌다(`git grep HEAD`). **표의 수와 모두 같았다.**

| 패턴(`B/`) | 표 | d2a06fa 다시 셈 | 지금 | 처분 |
|---|---|---|---|---|
| `user_events\.publish` | 9 / 6 | 9 / 6 | 9 / 6 | 메시지함 게시 자리 9 는 **바꿀 필요가 없다**. 이름·필드가 그대로이고 같은 NOTIFY → 허브 → SSE 로 닿는다(SSE 시험이 넷 모양을 고정). `external_inbox.py:251`(깨우기 채널)은 건드리지 않음. 새 게시는 `publish(...)` 를 감싼 `publish_user_event`(6 / 3 — 정의·알림 둘) |
| `pg_notify` | 1 / 1 | 1 / 1 | 1 / 1 | 그대로 |
| `UserEventType\.` | 12 / 6 | 12 / 6 | 17 / 9 | +5 = 알림 사건 생성 2(`platform/notifications.py`) · SSE 분기 2 + `INBOX_EVENT_TYPES` 정의 4줄 중 일부(events.py). 기존 11 생성 자리 무변경 |
| 사건 종류 정의 | 17 / 7 | 17 / 7 | 18 / 7 | `events.py` 에 두 종류 + `INBOX_EVENT_TYPES` |
| `USER_EVENTS_CHANNEL` | 20 / 7 | 20 / 7 | 22 / 8 | 값 그대로(`ax_user_events`) · `user_events.py` 가 import·사용 |
| `UserEventHub\|user_event_hub` | 8 / 3 | 8 / 3 | 11 / 6 | 허브(넘침 표시) · 조립(sqlite 배달) · SSE 라우트 |
| `@app\.websocket` | 2 / 2 | 2 / 2 | 2 / 2 | 둘 다 남김 · 메시지함 WS 는 넷만 거름 · 회의 WS 무변경 |
| `StreamingResponse\|EventSourceResponse\|text/event-stream` | 0 | 0 | 4 / 1 | 새 `http_events.py` |
| `_same_origin\|connection_principal\|CLOSE_*` | — | 15 / 4 | 17 / 5 | SSE 가 `_same_origin` 을 가져다 쓴다(옮긴 것이 아니라 공유 — WS 가 남으므로) |
| 듣는 쪽 `bootstrap/external_inbox.py:144-147` | — | — | — | 무변경. 시험 DB 메시지함 사건은 지금처럼 `_flush_local_events` 를 탄다 |
| 게시 프로세스 — meeting_worker | — | — | — | 길은 섰다(체크박스 7). 실제 호출은 WP2 생성기 |

**표 밖에서 더 찾은 것**
1. `B/entrypoints/http_inbox.py` 옛 WS 루프 — 이 판으로 채널에 알림 사건이 섞이므로 **메시지함 넷만 거르게** 했다. 옛 front 가 모르는 사건을 받지 않게 한 것이다(표에는 「남긴다」만 있었다)
2. `B/bootstrap/schema_sync.py` — 시퀀스를 모르던 sync 에 시퀀스 더하기
3. `Makefile` local-stack 전제 검사와 그 시험 — 옛 스키마로 스택이 서면 알림 쓰기가 500 이다(P-4)
4. `B/platform/notifications.py` `mark_read` — `notification.read` 게시(§4.5-1 의 「읽음 → 사건」을 지금 있는 단건 읽음에 먼저). staticmethod 에서 메서드로 바뀌었고, 부르는 곳은 `modules/notifications.py` 의 `self._repository.mark_read(row)` 하나라 모양이 그대로다
5. **운영 인벤토리 drift 시험**(`BT/architecture/test_operation_inventory.py`)은 라우트를 `http.py` · `http_inbox.py` 두 파일만 읽는다. 그래서 `http_events.py` 의 새 라우트는 **잡히지 않는다**
   - 인벤토리(`docs/unified-operations-inventory.json`)는 allowed_paths 밖이라 손대지 않았다
   - 그 시험의 파일 목록에 `http_events.py` 를 더하면 인벤토리 행이 필요하다 → **코디 판단**(아래 §5)

## 3. 새 시험

| 파일 | 시험 |
|---|---|
| `BT/contract/test_events_stream.py` (새 · 18) | 머리·`retry`·`ready`·첫 연결엔 `resync` 없음 / 401 JSON · 다른 출처 403 · 루프백 출처 허용 / 하트비트 / 메시지함 넷 이름·필드 그대로 + 회원 거르기 + id 없음 / 새 알림 = `id:` 순번 · `created` · 요청자 쪽엔 없음 / 읽음 → `notification.read` / 모르는 종류 안 보냄 / **비-200 뒤 `?last_event_id=` 회복(그 사이 알림 받음 · 창 밖 옛 줄 없음)** / 머리 > 쿼리 / **커밋 순서가 바뀐 작은 순번(겹침 창)** / **합쳐져 순번이 바뀐 줄의 옛 순번(기준 줄 대체)** / 기준 줄 없음·숫자 아님 → `resync` 만 / 넘침 → `replay_overflow` 만 / 이어 받은 순번이 실시간으로 다시 와도 한 번 / 큐 넘침 → `resync(dropped)` 뒤 최신 둘 / 옛 WS 는 넷만 / 빈 커서 = 첫 연결(×2) |
| `BT/sse_stream_support.py` (새 · 도구) | `SseConnection` — ASGI 를 직접 불러 끝나지 않는 스트림을 읽고 `http.disconnect` 로 닫는다. `TestClient` 는 본문을 끝까지 모아 SSE 를 못 읽는다 |
| `BT/unit/test_user_event_hub.py` (+2) | 넘침 = 최신 유지 + `dropped` 표시 / 알림 NOTIFY 짧은 페이로드 왕복 · 메시지함 사건 모양 불변 |
| `BT/contract/test_production_route_registration.py` (+1) | PRODUCTION 에 `/api/events/stream`(+ 옛 WS) 등록 · 세션 없이(페르소나 포함) 401 JSON |
| `BT/integration/postgres/test_external_channels_postgres.py` (+3) | **NOTIFY 경유**: 알림 짧은 페이로드가 커밋 뒤에만 · 워커와 같은 세션 공장에서 롤백은 없음 · 순번은 전역 시퀀스로 커짐 / 살아 있는 PG 의 허브 LISTEN → SSE 로 알림 · `Last-Event-ID` 로 다시 붙으면 이어 받기 → `resync` / 운영 SQL 이 옛 행에 순번을 주고(재적용 동일) · 인덱스 SQL · sync 가 없는 시퀀스를 더함 |

## 4. 검증 — 관련 시험만 (P-8 · Makefile 타겟)

격리 PostgreSQL 은 사용자 54329 가 아닌 **별도 컨테이너 `ax-notify-pgtest` · `127.0.0.1:55439` · DB `ax_test_notify`** 다(검증 뒤 정지 — 다음 판에 `docker start ax-notify-pgtest`).

| 명령 | 기준선(`be-baseline.md`) | 지금 |
|---|---|---|
| `make test-contract-serial FILES="tests/unit/test_user_event_hub.py tests/contract/test_external_inbox.py tests/contract/test_kakao_ingest_and_profile.py tests/contract/test_production_route_registration.py tests/contract/test_events_stream.py"` | 54 passed(새 파일 없이) | **75 passed** · 0 failed · 44.5s |
| `PYTEST_ADDOPTS='tests/integration/postgres/test_external_channels_postgres.py' POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:55439/ax_test_notify make test-postgres` | 2 passed | **5 passed** · 0 failed · 19.6s |

- 기존 실패: 기준선 0, 지금 0
- 첫 실행에서 새 SSE 시험 2건이 실패했다. 원인은 **내 시험의 기대값**이었다. 겹침 창이 기준 줄 자신과 기준과 같은 시각의 줄을 다시 주는 것은 SPEC 대로이고, 그 기대값을 고쳐 통과했다. 제품 코드는 그대로다
- **돌리지 않은 관련 파일**(P-8 — 시험 줄 밖). 바뀐 코드가 닿으니 코디의 전체 돌기에서 볼 것:
  - `BT/architecture/test_local_stack_targets.py` — 단언 1줄을 더했다. Makefile 에 그 두 글자가 있는 것은 grep 으로만 확인
  - `BT/architecture/test_architecture.py` — `http_events.py` 는 `platform` 을 import 하지 않는다. grep 0 으로만 확인
  - `BT/architecture/test_operation_inventory.py` — `NotificationView` 모양은 그대로다
  - `BT/architecture/test_test_pyramid.py`
  - `BT/contract/test_notifications.py` · `test_task_successors.py`(`emit` 0 기대) · `test_personal_command_tools.py` · `test_unified_queries.py` — `emit` · `mark_read` 를 지난다

## 5. 미결 · 주의점

1. **운영 인벤토리**(§2-5) — 새 라우트가 drift 시험 범위 밖이다. 행을 더할지, 시험 파일 목록에 `http_events.py` 를 더할지는 docs 소유라 코디가 정한다(WP2 가 알림 API 행을 갱신할 때 같이 하는 것이 자연스럽다)
2. **WP2 가 받는 자리**
   - `notification` 항목 모양 — 지금은 `NotificationView` + `seq` · `updated_at`. §4.5-2 로 바꾸는 것은 WP2
   - 읽기 인가 변경 — 지금은 못 읽으면 SSE·이어 받기에서도 빠진다. WP2 에서 `target: null` 로 바뀐다
   - 합친 줄 — `created: false` · 새 순번. `emit` 은 지금 새 줄만 순번을 받는다
   - 마이그레이션 — WP2 의 칸은 같은 `2026-10-08-notifications-v2.sql` 뒤에 덧붙이도록 파일 머리에 적었다
3. **WP1-FE 에 알릴 것(계약 고정값)**
   - `notification.upserted` 의 `data.notification.seq` 와 `id:` 는 같은 값이다
   - 이어 받은 줄의 `created` 는 `false` 다(이어 받기에는 「새로 섰나」가 없다 — `replayed: true` 로 가른다)
   - 메시지함 사건 `data` 는 WS 프레임과 달리 `v` · `member_id` 를 함께 싣는다(SPEC §4.1-2 모양)
   - 숫자가 아닌 `last_event_id` 는 `resync(reconnected)` 다
4. **옛 메시지함 사건 게시 9곳 중 sqlite 에서 허브로 흐르지 않는 것**(`external_channels.py:154` OAuth·연동 변경 등)은 지금과 같다. PG 에서는 모두 닿는다. 시험 DB 에서 그 사건을 SSE 로 보려면 그 자리도 `publish_user_event` 로 옮겨야 한다 — 이 판은 이름·필드 불변 원칙으로 두었다
5. **알림 표가 운영에 있는지** — 마이그레이션 파일이 없던 표다. SQL 은 `CREATE TABLE IF NOT EXISTS` 로 양쪽을 덮지만, 코디가 운영 확인 후 적용한다(BE 조사 §8-1)
6. **운영 실물**(완료 조건) — Cloudflare → ingress 1시간 유지 · ingress 버퍼링 끔 주석은 Pre-deploy(코디). 하트비트 20초는 `http_events.HEARTBEAT_SECONDS` 한 상수다
7. **연결 수** — SSE 한 연결이 그 회원의 사건마다 DB 읽기 1회(알림 사건만)를 스레드로 한다. 메시지함 사건은 DB 를 읽지 않는다
