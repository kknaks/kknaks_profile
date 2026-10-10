# WP1-BE 기준선 (고치기 전)

- 코드: 워크트리 `strong-hajin-notify` · `d2a06fa` · 변경 없음(`git status --short` 비어 있음) · 2026-10-08
- 격리 PostgreSQL: 사용자 54329 가 아닌 **별도 컨테이너 `ax-notify-pgtest` · `127.0.0.1:55439` · DB `ax_test_notify`**

| 명령 | 결과 |
|---|---|
| `make test-contract-serial FILES="tests/unit/test_user_event_hub.py tests/contract/test_external_inbox.py tests/contract/test_kakao_ingest_and_profile.py tests/contract/test_production_route_registration.py"` | **54 passed** · 1 warning · 36.7s |
| `PYTEST_ADDOPTS='tests/integration/postgres/test_external_channels_postgres.py' POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:55439/ax_test_notify make test-postgres` | **2 passed** · 1 warning · 10.3s |

**기존 실패: 0.**

참고 — 첫 시도의 DB 이름이 `axtest` 일 때 2 failed(`reset_demo requires a safe local demo database URL`)였다. 이건 시험 자체의 실패가 아니다. `reset_demo` 의 안전 이름 규칙(`^ax_(demo|test)…$` — `entrypoints/reset_demo.py:14`)에 걸린 것이고, DB 를 `ax_test_notify` 로 만들어 다시 돌리니 통과했다.
