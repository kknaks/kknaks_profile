# 리뷰 리포트 — prod-deploy-re1 / code 재리뷰 7 · #245 W4 · W5 수정 1 (2026-11-11)

범위(코디 지정 · 전체 재리뷰 아님): review-code-6 W1 · W2 · W3 · 참고 1 이 닫혔나 · 새 어긋남. 근거: be-2-report.md 「수정 1」 · review-code-6.

## 판정: PASS

FAIL 0 · WARN 0 · 참고 2.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra" backend/tests/architecture backend/tests/day/emr` | **137 passed**, 43 deselected |
| `uv run ruff check backend` | All checks passed |

infra(W3 · 참고 1 시험 — 실제 PostgreSQL · Redis)는 사용자 포트 · 프로세스 금지라 안 돌림 — be-2 수정 1 격리 스택 76 passed 를 근거로 두고, 시험 본문을 읽어 단언을 확인했다.

## W1 — 닫힘 (PASS)

`backend/tests/architecture/test_room_delete_write.py`(새) — AST 로 `day/` 의 문자열 상수를 모두 보고, `delete_room_tasks` 가 정의(`emr/base.py`) · 계획(`emr/kos/writes.py`) 밖에서는 `services/board.py` `room_return` 함수 안에서만 나오는지 · 실제로 만드는 줄이 있는지(`assert makers` — 빈 통과 막음) · 값 `"DELETE"` 가 `emr/kos/writes.py` 밖에 없는지 단언. 리뷰 6 W1 의 (b) 방향 그대로 — gate 가 경로+값 단위인 한계를 「만드는 곳 하나」로 묶었다. 모듈 docstring 이 그 이유를 적었다.

## W2 — 닫힘 (PASS)

`test_room_move_chain_rules.py:180-189` — `Settings` 기본값 `sync_schedule_interval_seconds == 10` · `outbox_send_interval_seconds == 10` + `deploy/` 의 `.env` · `.yaml` · `.example` 어디에도 두 이름이 없음(덮지 않음). `Settings` 는 env 접두가 없어(`common/config.py:75`) 대문자 이름이 곧 env 이름 — 검사 대상 이름이 맞다. `scripts/` · `.github/` 에도 두 이름 없음(grep).

## W3 — 닫힘 (PASS)

- `outbox.py:136-137` `Report.retried_visits` — `_send_one` 의 보내기 결과가 retry · failed 면 그 방문을 담음(`:573-574`).
- `emr_sync.py` `run_outbox` 가 `send=op.visit_id not in report.retried_visits` 로 연쇄를 부르고, `_chain_room_assign` 은 `send=False` 면 확인 · follow 쌓기(한 transaction · commit)까지만 하고 `follow_not_sent` 로 끝 → 다음 발송 회차가 seq 순(retry 난 쓰기 먼저 → follow ① → ②)으로 보낸다. 같은 회차 즉시 재전송이 없어 attempts 가 한 회차에 두 번 오르지 않는다.
- 시험 `test_room_move_chain.py` `test_같은_회차에_그_방문_쓰기가_retry_됐으면_연쇄는_보내지_않고_다음_회차에` — KOS 호출 = add · room(503) · detail 셋뿐 · 503 쓰기 pending · follow 둘 pending · counts `follow_not_sent`.

## 참고 1 — 닫힘 (PASS)

- `run_outbox` 가 연쇄 하나를 `try/except Exception` 으로 감싸 `chain_error` 를 세고, 로그엔 예외 **클래스 이름만**(`type(exc).__name__`) — 값 누출 없음. 그 뒤 `_signal`(④ outbox 상태 · 실패 토스트)이 그대로 나간다.
- `except Exception` 은 `asyncio.CancelledError`(BaseException)를 잡지 않으므로 회차 상한(`asyncio.timeout`) 취소는 그대로 동작한다. 연쇄 안 세션은 예외 때 rollback(`get_async_session` 방식) → 확인 UPDATE 도 되돌아가 만들기 쓰기는 `sent` 그대로 → 10초 조회가 잇는다.
- 시험 `test_연쇄가_깨져도_첫_보내기_신호는_나간다` — `follow_room_assign` 이 값이 든 `RuntimeError` 를 던짐 → 회차 `done` · `chain_error: 1` · 신호 1회 · 만들기 쓰기 `sent` 그대로.

## 새 어긋남

없음. 참고만:

- 참고 1(시험 거짓 양성 가능성): W1 시험은 `day/` 안 **모든** 문자열 `"DELETE"` 를 막는다. 나중에 HTTP 메서드 이름(`methods=["DELETE"]` 등)이 `day/` 에 생기면 이 시험이 걸린다 — 그때 `cancel-flow-tasks` 본문 맥락으로 좁히면 된다. 지금은 해당 없음.
- 참고 2: W3 의 `retried_visits` 는 보내기 오류(retry · failed)만 본다. 토큰 기다림(`no_token`)은 attempts 를 올리지 않으므로 대상이 아닌 것이 맞다.
