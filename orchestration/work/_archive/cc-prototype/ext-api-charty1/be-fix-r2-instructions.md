# backend 3차 — 코드 검수 r2 시험 빈칸 (코드 변경 0)

원 브리프 제약 그대로. 리포트 `review-code-r2.md` N1 ~ N3 를 **시험만 더해** 닫는다(앱 코드는 고치지 않는다 — 시험이 실패하면 멈추고 보고).

- N1: T55 — 다른 날 예약 id 의 `reception` · `consultation_add` 여럿 넣고 board 결과 같음 + `events_for_reservations` 결과에 그날 예약 id 밖 줄 0
- N2: T54 — 줄의 `customer.customerId` = 사본 고객 id · `name` = 사본 이름 값 단언
- N3: T48 — `get-visitor` 가 NotFound 아닌 400 → 502 · T49 — `{customerId: 1, name: null, email: null}` → 200 · `{customerId: null}` → 400
- 각 시험이 실제로 계약을 잡는지 한 번 변이로 확인(예: `customers_in` 을 `{}` 로 바꾸면 실패) → 되돌림 · 보고에 적기

검증: `uv run pytest -q tests/test_ext_board.py tests/test_ext_lookup2.py` → 전체 1번 · ruff. 보고 두 채널.
