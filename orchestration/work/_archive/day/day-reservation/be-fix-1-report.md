# day-reservation backend 고침 1: 코드 검수 W-2 · W-3 · W-5 (+ W-4 메모)

## 상태: done

커밋 · push · PR 없음. frontend 쪽 미커밋 변경은 건드리지 않았다.

## 수행

| 지적 | 고침 | 파일 |
|---|---|---|
| **W-2** 실제 kiq를 시험하지 않음 | 새 테스트 4개. ① 기록 broker(`InMemoryBroker`의 `kick`을 바꿔 메시지를 모음): `task_name = day.sync_reservation_date_hospital` · 메시지 본문 `args = [str(hospital), "2026-11-30"]` · `kwargs = {}` ② 메모리 broker에 같은 이름의 task를 등록해 실제로 `(hospital_id, date)`를 받는지 ③ kick 예외 → `False` + 경고 로그 `reservation refresh kick failed … SendTaskError`(taskiq가 감싼 이름) ④ kick이 멈추면 시간 상한에서 `False` + `timed out` 로그 | `backend/tests/day/test_reservation_refresh.py`(새) |
| **W-3** [fetch] 실패는 아무것도 증명하지 않음 · timeout 시험 없음 · A1 저장 증명이 비어 있음 | ① `[fetch]`를 빼고 **transaction 안 실패** 두 경우로 바꿨다. `apply_task_refs`(일정 · 처방 · 구매 · 시술권 · 카드 · 이력을 쓴 뒤)와 `apply_kos_keys`(마지막 단계)에서 예외를 내면 `error` / `ValueError`이고, 방문 · 고객 · 구매 · 선불카드가 **0행**이다(`_nothing_saved`) ② **timeout 되돌림**: 회차 상한을 1초로 두고, 키 보충까지 다 쓴 뒤 commit 전에 멈추게 했다. 결과는 `timeout`이고 0행이다. 그 뒤 잠금이 풀려 다시 돌리면 `done`이다 ③ **A1 저장 단언 추가**: 고객 > 0 · 선불카드(그 병원 고객 소유) > 0 · 작업 > 0 · 작업 참조 1건(고정본 첫 작업에 `ticketConfiguration.ticketId = tkt-1`을 넣었고, 그 작업의 `visit_task.ticket_id`가 채워짐). 쓰지 않게 된 가짜 어댑터의 `fail` 옵션은 지웠다 | `backend/tests/day/emr/test_date_sync.py` |
| **W-5** 범위 밖 날짜가 500 | `parse_day`에서 `date.min < d < date.max` 밖이면 같은 400 `invalid_request`(`detail="date out of range"`). 시험: `0001-01-01` · `9999-12-31` → 400 + `X-Day-Error: invalid_request` + 최신화 요청 0 · DB 읽기 0. 바로 안쪽 `0001-01-02` · `9999-12-30`은 200(판정까지 넘치지 않음) | `backend/day/services/reservations.py` · `backend/tests/day/web/test_reservation_page.py` |

## 검증

- `./scripts/test.sh -q backend/tests/day/emr backend/tests/day/test_reservation_refresh.py backend/tests/day/web/test_reservation_page.py backend/tests/day/test_reservation_rules.py backend/tests/day/test_reservation_queries.py backend/tests/day/board/test_reservation_permissions.py`(격리 PostgreSQL · Redis): **356 passed**
  - `test_date_sync.py` 10 passed(A1 강화 · transaction 안 실패 2 · timeout 1 포함)
  - `test_reservation_refresh.py` 4 passed
  - `test_reservation_page.py` 8 passed(W-5 1개 추가)
  - `tests/day/emr` 전체 = 오늘 회차 회귀 없음
- `ruff check` · `ruff format --check`: 만진 파일 통과
- `mypy`(루트 설정 · 전체): Success, 475 files
- `taut check`: diagnostics 0

## W-4 (고치지 않음 · 사용자 판단용)

**행 경합이 실제로 나는 조건**: 다른 날짜 최신화의 반영 transaction(일정 → 구매 → 시술권 → 카드 → 키 보충 · 한 번에 commit)이 열려 있는 동안, 오늘 10초 회차가 **같은 고객 행**을 써야 하는 경우다. 행은 `customer` · `ticket_bundle` / `ticket_set` / `ticket` · `prepaid_card` · `external_ref`, 그리고 키 보충의 고객 칸이다. 그 고객이 보는 날짜와 오늘에 모두 예약이 있고, 오늘 쪽이 그 사이에 일정 반영이나 키 보충(`apply_isolated` · 상한 8초)이나 오늘 구매 회차를 돌 때 생긴다. 이때 오늘 쪽은 날짜 transaction이 끝날 때까지 행 잠금을 기다린다. 날짜 transaction은 쓰기만 하므로 보통 1초 이내지만, 고객이 많은 날에는 길어진다. 기다림이 8초를 넘으면 오늘 키 보충이 한 회차 로그만 남기고 빠진다. 두 쪽이 서로 다른 순서로 행을 잡으면 교착이 나고, PostgreSQL이 한쪽 transaction을 되돌린다. 오늘 일정 회차가 되돌려진 쪽이면 `error` · `record_sync(error)`가 한 회차 남는다.

**대안 두 가지**:
- **① 날짜 transaction을 짧게 · 지는 쪽을 날짜로**: KOS 읽기는 지금처럼 밖에서 끝낸다. 반영 transaction에 `SET LOCAL lock_timeout`(예: 1 ~ 2초)을 걸고, 고객 행을 정렬된 순서로 써서 교착 가능성을 줄인다. 오늘 쪽이 행을 쥐고 있으면 날짜 쪽이 먼저 포기하고 `error`가 된다(중간 상태 없음 · 다시 열면 다시 돈다). 오늘 회차는 기다리는 시간이 짧아지고 되돌려지지 않는다. 대신 바쁜 시간에는 날짜 최신화 실패가 늘 수 있다.
- **② 같은 고객 행은 오늘 잠금 뒤로**: 반영 직전에 오늘 회차의 병원 잠금(`schedules` · `sales`)을 **짧게 기다려서**(예: 상한 수 초 · 잡힐 때까지 재시도) 잡고, 그 안에서 반영 transaction을 돈다. C2(조용히 건너뛰지 않음)는 「기다리다 상한이면 실패」로 지킨다. 오늘 쪽은 그동안 「앞 회차가 안 끝남」으로 한 회차(10초)를 건너뛸 수 있지만, 행 대기 · 교착은 없어진다.

## 이슈 · 코디가 확인할 것

- W-2 실패 로그의 예외 이름은 원래 예외가 아니라 taskiq가 감싼 `SendTaskError`다(코드는 그대로 `type(exc).__name__`). 로그만 보고 원인을 알기 어렵다면 `__cause__` 이름을 덧붙이는 방안이 있다. 그런 요청이 없어서 손대지 않았다.
- W-6(정원 null일 때 「/」까지 지움)은 frontend · 사용자 몫이라 손대지 않았다.
