# be-swagger-2 결과 보고 — `Idempotency-Key` 재시도 응답 = 처음 응답 그대로

## 상태: done (커밋 없음 · 새 migration 파일 없음 · 로컬 스택 안 건드림)

## 고친 파일:줄

| 파일:줄 | 무엇 |
|---|---|
| `backend/migrations/versions/20261126_0031_reservation_request.py:169` | `reservation_request_version.accepted_status`(enum `reservation_request_status` · null 허용) — 이번 0031 안에서(지시서의 `20261125_…` 는 실제 파일 이름 `20261126_0031_reservation_request.py`) |
| `backend/day/models/reservation_request.py:134-135` | `accepted_status: RequestStatus \| None` |
| `backend/day/services/reservation_request_ext.py:319` | `_replay` — `status` = 저장한 `accepted_status`(null 이면 `requested`) · 그 전엔 늘 `"requested"` |
| 같은 파일 `:354` | E1 — v1 에 `requested` 저장 |
| 같은 파일 `:414` · `:444` | E2 — 받은 뒤 스레드 상태(`requested` · `canceled`)를 버전에 저장 · 응답도 같은 값(`thread.status`)에서 |
| `backend/day/routers/api/ext_reservation_request_docs.py:49` · `:133-134` | 흐름 6 · E2 설명 「`status` 는 `requested` 로 온다」 → 「처음 응답 그대로(`requestId` · `version` · `kind` · `status`)」 |
| `backend/day/routers/api/ext_reservation_requests.py:31` | `Idempotency-Key` 헤더 설명 「처음 응답 그대로」 |
| `backend/tests/day/test_column_snapshot.py:85` | 칸 목록에 `accepted_status` |
| `backend/tests/day/board/test_reservation_request_actions_flow.py:396-404` | **새 시험** — 예약 현황에서 먼저 취소된 스레드에 E2 `cancel` = `canceled` → 같은 키 재시도 응답 == 처음 응답(`canceled`) |
| `backend/tests/day/test_reservation_request_flow.py:98` | E1 재시도 확인을 `requestId` 만 → 응답 전체 같음으로 |

## 고른 방법 · 이유

**처음 상태 저장**(`accepted_status`). 버전 행에서 다시 계산하는 길은 결정적이지 않다: 「취소됨으로 닫은 E2」 표지가 될 만한 `reservation_applied` `cancel`(글쓴이 없음 · 그 버전)은 병원 동기화(`settle._expire` · W11)도 **같은 버전에** 뒤늦게 붙인다 — 처음 응답이 `requested` 였던 `cancel` 재시도가 `canceled` 로 바뀌어 버린다. 응답을 만든 그 자리에서 값을 저장하면 그런 갈래가 없다. 재생 조회는 이미 그 행을 읽으므로 쿼리도 늘지 않는다. null(칸이 생기기 전 행 — 배포 전이라 실제로는 없음) = 예전과 같이 `requested`.

## 검증

- 관련 시험(`test_ext_contract` · `architecture/test_api_contracts` · `test_ext_reads` · 예약 요청 rules · flow · actions_flow · writes_plan · `test_column_snapshot` · `test_models` · `tests/migrations`) = **440 passed**.
- `scripts/check.sh --pure` = **통과**(ruff · format · mypy · taut audit/check · frontend · 시험 2420 passed · `.local/checks/20261127-103436-99297`).
