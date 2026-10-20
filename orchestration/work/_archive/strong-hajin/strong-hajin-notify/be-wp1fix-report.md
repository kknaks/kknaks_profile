# WP1-BE 검수 WARN 4 손질 — 결과

- 출처: `review-wp1-be-report.md` §WARN
- `B/` = `backend/src/ax_workspace/` · `BT/` = `backend/tests/`

| # | 무엇 | 한 것 (파일:줄) | 시험 |
|---|---|---|---|
| **W-1** | 인벤토리 drift 시험이 새 라우트를 못 봤다 | `BT/architecture/test_operation_inventory.py:138` 파일 목록에 `http_events.py` 를 더했다<br>`docs/unified-operations-inventory.json` 에 `GET /api/events/stream` 행(E2 · 화면 전역 연결)을 넣었다<br>같은 방식으로 WP2 새 경로 다섯(summary · read-all · badges · 설정 GET/PUT)을 넣었고 `GET /api/notifications` 시그니처를 갱신했다<br>`http_count` 192 → **198** · 도구 셋(`list_notifications` · `notification_mark_read` · `meeting_share` 설명)의 스키마 갱신 — diff 난 항목만 바꿨다 | `make test-contract-serial FILES="tests/architecture/test_operation_inventory.py"` **4 passed** |
| **W-2** | ①과 ② 사이 옛 이미지가 쓴 빈 `seq` | `backend/migrations/manual/2026-10-08-notifications-v2.sql` 머리 주석에 「**② 이미지 반영 뒤 이 파일을 한 번 더** — 옛 이미지가 쓴 빈 `seq` · `updated_at` 을 채운다(빈 행만 · 다시 돌려도 안전)」를 적었다 | 재적용 동일은 PG 시험 `test_the_v2_sql_numbers_old_rows_and_sync_adds_a_missing_sequence` 가 지킨다 |
| **W-3** | 커서 > 회원 최대 순번이면 `resync` 만 (**코드를 SPEC 에**) | `B/platform/notifications.py:258-261` — 그 회원의 가장 큰 순번보다 크면 `None` → `resync(reconnected)` 만 | `test_a_cursor_above_the_members_newest_seq_sends_only_resync` |
| **W-4** | 닫힌 연결이 구독을 풀었다는 단언 | `BT/contract/test_events_stream.py` 첫 시험 — 연결 중에는 `_subscribers["mina"]` 가 있고, 닫은 뒤에는 비었다 | `test_the_stream_opens_with_retry_then_ready_and_the_proxy_safe_headers` |

**하나 더 — SPEC 대조 중 찾은 어긋남(코드를 SPEC 에 맞춤)**
- SPEC-011 Validation 은 「`Last-Event-ID` 가 정수가 아니면 없는 것으로 본다(첫 연결처럼)」다
- WP1 은 숫자가 아니면 `resync(reconnected)` 를 냈다 → `B/entrypoints/http_events.py:63` 에서 첫 연결로 바꿨다
- 음수는 정수라 「기준 없음 → `resync`」 그대로다
- 시험: `test_an_empty_or_non_integer_cursor_is_a_first_connection[not-a-number]`
- **WP1-FE 에 알릴 것**: 앞 보고의 「숫자가 아닌 `last_event_id` 는 `resync(reconnected)`」 는 **틀렸다** — 첫 연결이다

**검증** — WP1 시험 줄 `make test-contract-serial FILES="tests/unit/test_user_event_hub.py tests/contract/test_external_inbox.py tests/contract/test_kakao_ingest_and_profile.py tests/contract/test_production_route_registration.py tests/contract/test_events_stream.py"` → **78 passed** · 0 failed. PG 는 `be-wp2-report.md` §4.
