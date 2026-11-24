# day-reservation backend rebase 1: origin/dev 최신 위로 · migration 0017

## 상태: done

- 새 HEAD: **`431c081b`**(브랜치 `kknaksss/day-reservation`). 부모는 `a03b83a4`(origin/dev · #270)이고 커밋은 하나다. 옛 `4b1d1662`을 옮긴 것이다.
- push 하지 않았다. 스택(11040 · docker · .run)과 deploy/*.env는 건드리지 않았다.

## 충돌 처리
- `backend/tests/migrations/test_alembic.py`: `HEAD` 한 줄만 충돌했다. → `HEAD = "0017_reservation_permission"`. dev 쪽 0015 · 0016 시험(차트 리비전 · 묶음 가격)은 그대로 살렸다.
- `scripts/frontend/package-lock.json`: `package.json`은 자동으로 합쳐졌다(dev 쪽 + 우리 `@sinonjs/fake-timers` · `jsdom`). lock은 dev 판에서 시작해 `npm install --package-lock-only`로 다시 만들었다(취약점 0).

## migration 번호 이어 붙이기
- `20261123_0015_reservation_permission.py`를 `20261123_0017_reservation_permission.py`로 옮겼다(git mv).
  - `revision = "0017_reservation_permission"`
  - `down_revision = "0016_ticket_bundle_unknown_price"`(dev의 문자열 그대로). docstring의 Revision ID · Revises도 맞췄다.
- grep으로 찾아 고친 곳:
  - `tests/migrations/test_reservation_permission_migration.py`: 파일 경로 · revision 문자열 · `PREV`(0016) · 시험 이름 · docstring
  - `tests/migrations/test_alembic.py`: `HEAD`
  - `day/services/default_permissions.py`: docstring 「0015」 → 「0017」
- 옛 이름(`0015_reservation_permission` · `20261123_0015`)은 이제 0건이다. `test_alembic.py:188`의 `0014_device_platform_android`는 dev 자신의 차트 시험이라 그대로 뒀다.
- `alembic heads`: **`0017_reservation_permission (head)` 하나**.

## rebase가 드러낸 통합 문제 하나 (고침)
- dev가 새로 들인 node 시험 도우미 `scripts/frontend/tests/production.mjs`는 `production("listener:htmx:afterRequest")`로 day.js에서 그 이벤트의 **마지막** `document.addEventListener`를 골라 평가한다.
- 그런데 우리 예약 현황이 세 번째 `htmx:afterRequest` 리스너를 이름(`resAfterRequest`)으로 등록한다. 그래서 차트 리스너 대신 이 이름만 잡혔고, `chart-recovery.test.mjs` 4개가 `ReferenceError: resAfterRequest is not defined`로 실패했다.
- 고침: 도우미가 **인라인 함수 리스너만** 잡게 조건 한 줄을 더했다(`arguments[1].type`이 `…FunctionExpression`인 것만). 이름으로 넘긴 리스너는 어차피 거기서 평가할 수 없다. day.js 실행 코드는 바꾸지 않았다.
- 이 파일은 dev(frontend 도구) 쪽 파일이다. frontend · 코디가 알아야 한다.

## 시험
- `./scripts/test.sh -q`(격리 PG · Redis): **136 passed**
  - 예약 관련 전부: rules · queries · refresh · page · screen · permissions · date_sync · date_sync_rules · default_permissions · board_default_view · emr_sync_service
  - `backend/tests/migrations` 전체(0017 왕복 · alembic head · dev 0015 · 0016 포함)
- `./scripts/test.sh --pure -q backend/tests/architecture`: **317 passed**
- node(`scripts/frontend` `npm test`):
  - 고치기 전: 102 중 98 pass · 4 fail
  - 고친 뒤: **102 pass · 0 fail**
- node 쪽 정적 검사: `npm run lint` · `format:check` · CSS 재현(`build.mjs --check`) 통과
- Python 정적 검사:
  - `ruff check backend scripts` 통과
  - `ruff format --check` 통과
  - `mypy` Success(526)
  - `taut check`: 0 errors
- 전체 `check.sh`는 브리프대로 돌리지 않았다.

## 코디가 확인할 것
- push · PR은 코디가 한다. migration 0017은 deploy의 migrate 단계로 적용된다.
- `production.mjs` 한 줄 변경을 frontend에 알릴 것.
- 스택은 새 HEAD로 다시 띄워야 dev 변경까지 반영된다(재기동은 코디).
