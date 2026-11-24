# day-reservation backend 고침 3 — e2e 1회차 E2 · E3 (서버 쪽)

## 상태: done (커밋 · push · PR 없음 · 스택은 건드리지 않음 · 재기동은 코디)

## E2 — 다른 날짜 첫 화면은 최신화 끝을 짧게 기다린 뒤 그린다
- **표시 = 10초 캐시와 같은 자리**(`day:emr:reservation_date_recent:{병원}:{날짜}` · TTL `RESERVATION_DATE_CACHE_SECONDS`) — 값을 셋으로: worker 가 시작 때 `running` · 끝나면 `done` · `error` / `timeout` / 예외면 `failed`(전에는 실패면 지웠다)
  - `running` · `done` = 「최근」(결정 8 그대로 — 넣지도 잠그지도 않음) · `failed` = 최근 아님(다음 열기에 다시). 화면이 요청을 넣기 전 `failed` 를 보면 지우고 넣는다(기다림이 옛 실패를 보지 않게)
- **라우트 순서 바꿈**(`routers/reservations.py`): 오늘 아님 ∧ `poll` 아님 → `request_refresh`(10초 캐시면 안 넣음) → **넣었을 때만** `wait_refreshed` → DB 읽기 → 그림. 오늘 · 폴링 · 캐시에 걸린 날짜는 기다리지 않음
- `services/reservations.wait_refreshed` — 표시를 0.1초 간격으로 읽어 `done` · `failed` 면 바로, 상한이면 None(이전 사본 · R30). 상한 = 설정 하나 **`RESERVATION_DATE_WAIT_SECONDS`(기본 3.0 · 0 ~ 10 · 0 이면 안 기다림)** · Redis 를 못 읽으면 기다림을 끝내고 사본으로(경고 로그). 화면 요청은 KOS 를 부르지 않는다(R39 — Redis 표시만)
- 시험
  - 라우트(DB 없음): 다른 날짜 = `kick → wait → read` 순서 · 오늘 · 폴링 · 캐시에 걸림(넣지 않음) = wait 0
  - 표시(가짜 Redis): `done` / `failed` 면 즉시(읽기 1회) · `running` → 0.3초 뒤 `done` 이면 그때 · 상한이면 None(0.3초) · 0초면 안 기다림 · 못 읽으면 None + 경고 · `failed` 는 지우고 넣음 · `running` 이면 안 넣음 · 기본값 3.0
  - worker(실 Redis · PostgreSQL): 도는 중 `running` · 기다리는 화면은 끝나기 전엔 안 돌아오고 `done` 을 보고 돌아옴 → 그 뒤 DB 에 그 날짜 방문 있음 · 실패면 `failed`(최근 아님) · 끝나면 `done`(TTL ≤ 10)

## E3 — 「수납 필요」 = 귀가 대기 ∧ 시술 줄 수납필요
- 원천을 `purchase.status = initialized` → **`visit_task.payment_required`**(살아 있는 작업 중 하나라도 · 시술 현황 DAY-SPEC-002 규칙 4 와 같은 원천)로 — `queries/reservations.py` EXISTS · DTO 칸 `has_payment_required`. 단계 조건(귀가 대기 `procedure_done` 부터 · 취소 · 노쇼 먼저)은 그대로(`policies/reservations.py`)
- 시술 현황 판정(`policies/board_rules.BoardRules.payment_required`)은 판 세계(`BoardWorld`)에 묶인 메서드라 직접 재사용하지 않고, 같은 원천 · 같은 뜻(`any(t.payment_required …)`)을 묶음 조회 EXISTS 로 쓴다
- 시험
  - 값(DB 없음): 귀가 대기 + 수납필요 → 붙음 · **접수 + 수납필요 → 안 붙음** · 귀가 대기 + 없음 → 안 붙음 · 귀가 + 수납필요 → 안 붙음 · 취소 + 귀가 대기 + 수납필요 → 안 붙음
  - 실 PostgreSQL: **귀가 대기 + payment_required → 붙음** · **접수 + payment_required → 안 붙음** · **귀가 대기 + 열린 purchase 만 → 안 붙음** · 귀가 대기 + 지운 작업만 수납필요 → 안 붙음

## 검증
- `./scripts/test.sh -q backend/tests/day/emr backend/tests/day/test_reservation_refresh.py backend/tests/day/web/test_reservation_page.py backend/tests/day/web/test_reservations_screen.py backend/tests/day/test_reservation_rules.py backend/tests/day/test_reservation_queries.py backend/tests/day/board/test_reservation_permissions.py backend/tests/runtime backend/tests/migrations` → **444 passed**(`tests/day/emr` 전체 = 오늘 회차 회귀 없음)
- `./scripts/test.sh --pure -q backend/tests/architecture` → **317 passed**
- `ruff check` · `ruff format --check`(backend/day · common · tests/day · migrations) 통과 · `mypy` 전체 Success(476) · `taut check` diagnostics 0
- 실물 확인(스택 재기동 · 한유나 사례)은 코디 몫 — 하지 않음

## 바꾼 파일
- `backend/day/services/reservations.py`(표시 값 셋 · `refresh_state` · `wait_refreshed` · 실패 표시 지우고 넣기) · `backend/day/services/emr_date_sync.py`(끝 `done` · 실패 `failed`) · `backend/day/routers/reservations.py`(넣기 → 기다림 → 읽기) · `backend/common/config.py`(`reservation_date_wait_seconds`)
- `backend/day/queries/reservations.py` · `backend/day/dtos/reservation.py` · `backend/day/policies/reservations.py`(E3 원천)
- 테스트: `backend/tests/day/test_reservation_refresh.py` · `backend/tests/day/web/test_reservation_page.py` · `backend/tests/day/emr/test_date_sync.py` · `backend/tests/day/test_reservation_rules.py` · `backend/tests/day/test_reservation_queries.py`
- **frontend 파일 한 줄**: `backend/tests/day/web/test_reservations_screen.py:371` 이 내 시험 도우미 `_visit(open_purchase=…)` 를 부른다 — 칸 이름이 바뀌어 `payment_required=True` 로만 바꿨다(그 밖 변경 없음 · frontend 에 알릴 것)

## 이슈 · 코디가 확인할 것
- 날짜 바꾸기 응답이 최대 3초 늦어질 수 있다(최신화가 1 ~ 2초면 그만큼) — 화면은 그동안 이전 화면 유지(frontend 몫 · 로딩 문구 없음)
- 「수납 필요」가 이제 시술 현황과 같은 원천이라 SPEC-006 U-5 · §4 「다른 스펙과 다른 곳」 문장(열린 구매)은 SPEC 쪽 개정이 필요하다(코디 · planner 몫)
- `.run/` 스택은 새 코드로 다시 띄워야 반영된다(api · worker 둘 다)
