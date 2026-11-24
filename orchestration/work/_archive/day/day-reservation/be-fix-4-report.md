# day-reservation backend 고침 4: 수납 필요 단계 조건 제거 (R42 · 사용자 정정)

## 상태: done

커밋 · push · PR 없음. 스택은 건드리지 않았고, 재기동은 코디가 한다.

## 수행
- 판정(`backend/day/policies/reservations.py`): `payment_due`를 바꿨다.
  - 전: `state == "procedure_done" ∧ has_payment_required`
  - 후: **`state ∉ {canceled, no_show} ∧ has_payment_required`**
  - 내원 단계(예약 · 접수 · 상담 · 시술 · 귀가 대기 · 귀가)와 상관없이, 살아 있는 시술 줄 중 `visit_task.payment_required`가 하나라도 있으면 붙인다.
- **취소 · 노쇼는 안 붙인다.** 지금 규칙 그대로다. 이유: 예약 상태를 먼저 보는 닫힌 카드라 수납할 방문이 아니다. 띠 · 툴팁 · 필터와 같은 판정 순서다.
- 원천은 고침 3과 같다. `queries/reservations.py`의 EXISTS로 `visit_task.payment_required`(삭제되지 않은 작업)를 본다. 주석만 R42로 바꿨다(`queries` · `dtos`).

## 시험
- 값(DB 없음) `test_reservation_rules.py`의 `test_수납_필요는_단계와_상관없이_시술_줄_수납필요`:
  - 붙음: 예약 · **접수** · **시술 진행** · 귀가 대기 · 귀가 각각에 수납필요가 있을 때
  - 안 붙음: **수납필요 없음** · 취소(+ 수납필요) · 노쇼(+ 수납필요)
- 실 PostgreSQL `test_reservation_queries.py`:
  - 붙음: **접수 + 수납필요** · **시술 진행 + 수납필요**(줄 둘 중 하나) · 귀가 대기 + 수납필요
  - 안 붙음: **수납필요 없음**(귀가 대기 + 열린 purchase만) · **지운 작업**(시술 진행 + 지운 줄만 수납필요)
  - 카드 수 7 → 8 · 「전체」 5 → 6
- 화면 시험(`test_reservations_screen.py` · `test_reservation_page.py`)은 그대로 통과했고 고치지 않았다.

## 검증
- `./scripts/test.sh -q backend/tests/day/test_reservation_rules.py backend/tests/day/test_reservation_queries.py backend/tests/day/web/test_reservations_screen.py backend/tests/day/web/test_reservation_page.py`: **38 passed**
- `ruff check` · `ruff format --check`(backend/day · tests/day) 통과
- `mypy` 전체: Success
- `taut check`: diagnostics 0

## 바꾼 파일
- `backend/day/policies/reservations.py`
- `backend/day/queries/reservations.py`(주석)
- `backend/day/dtos/reservation.py`(주석)
- `backend/tests/day/test_reservation_rules.py`
- `backend/tests/day/test_reservation_queries.py`

## 코디가 확인할 것
- SPEC-006 U-5 「수납 필요」 문장(귀가 대기 ∧ 열린 구매)과 케이스 매트릭스 「열린 구매가 있는데 귀가 대기 아님」은 R42에 맞춰 SPEC 쪽 개정이 필요하다.
- 실물(한유나 사례 · 접수 상태 + KOS 수납필요 2줄 → 배지)은 스택을 재기동한 뒤 확인해야 한다.
