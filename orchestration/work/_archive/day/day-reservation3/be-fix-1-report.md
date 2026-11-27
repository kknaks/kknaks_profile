# be-fix-1 결과 보고 — 코드 검수 1차 BE 몫

## 상태: done (커밋 없음)

## 고친 것
| # | 무엇 | 어디 |
|---|---|---|
| F1 | `pending_write_id` = 보내는 중(확인 대기 · 실패 아님)일 때만 · 실패면 None + `action="failed"` | `services/reservation_request_reads.py` `read_window` |
| F2 | 되살리기 UPDATE 범위 — 스레드 길 = 그 event 행만 · 공용 길 = 스레드 묶음(`payload.request_id`) event 행은 찾지도 되살리지도 않음 · 실패가 스레드 행뿐이면 409 `request_thread_write` | `services/reservation_writes.py` `retry` |
| F3 | 서비스 infra ①~④ + ext HTTP(E1 · E2 한 줄씩: `X-Day-Client` 400 · `Idempotency-Key` 빠짐 400 · 구분 값 없음 400 · 한도 키 `day:ext:key:{hospital}` · `customer_changed` 400) · ⑤ 알림은 `test_reservation_request_flow` 그대로 | 새 `tests/day/board/test_reservation_request_actions_flow.py`(4) |
| W1 | `customer_changed` = `booked(state)`(확인 대기 포함) · 대기 중 `thread.customer_id` 안 덮음 | `reservation_request_ext.add_version` · `policies` |
| W2 | E4 설명에 「5분 앞으로 겹쳐 읽고 requestId · version 으로 거름」 | `routers/api/ext_reservation_requests.py` |
| W6 | `grants()` 같은 `hospital_id` 둘 → 503 `ext_unavailable` + error 로그 · 테스트 | `routers/api/ext.py` · `test_ext_contract.py` |
| W7 | `NotificationTarget.requestId` · `date` = `None` 기본 · 받은 칸만(exclude_unset) — 앱 응답 모양 그대로 | `schemas/notification_responses.py` |
| W8 | `read_list` 묶음 조회(버전 1 · 「예약 있음」 1 — `threads.states`) + query-count 테스트(1개 = 4개 같은 수) | reads · threads · `test_reservation_request_flow.py` |
| W9 | 초진 W1 = 스레드 잠금 전에(`_look_first`, 읽고 rollback) · 잠금 안에서는 판정만 · 그 사이 버전이 바뀌면 다시 W1 | `services/reservation_request_actions.py` |
| W11 | 「요청됨」 ∧ 답할 버전 `cancel` ∧ 예약 없음 ∧ 확인 대기 아님 → 취소됨 + `reservation_applied`(취소 · 누른 직원 없음) · 버튼 없음 — 10초 회차(settle) · 테스트 | `settle._expire` · `policies.cancel_done` · `action` |
| W13 | E2 스레드 찾기(404)를 `_check` 앞으로 · `Idempotency-Key` 설명 = 「범위 = 병원 · 표마다(요청 · 버전 한 범위, 댓글 따로)」 | ext · 라우터 |
| 덧붙임 | `reservation_request_ext.py` 703줄 → 쓰기 498 + 새 `reservation_request_ext_reads.py`(E4 · E5 · E7 · E8) 231 · 동작 그대로 | |

W3 · W4 = 코디 e2e 실물(코드 그대로).

## 검증
- `scripts/test.sh` 전체 **3292 passed**(그 뒤 ext HTTP 테스트를 승인 클라이언트로 옮김 → 그 파일 4 passed)
- `scripts/check.sh --pure` **통과**(exit 0 · `.local/checks/20261126-223911-19372`)

## 주의
- W11 은 버튼을 누르지 않은 자동 반영이라 `reservation_applied.author` = 없음(시스템).
- `dismiss_failure`(접음)의 「예약 없음 ∧ cancel → 닫힘 folded」(N2 ③)는 그대로 — W11 은 확인 대기 아닌 경우만.
