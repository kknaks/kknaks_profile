# day-reservation backend 고침 2: 사용자 결정 4 · 8 · 9 (서버 쪽)

## 상태: done

커밋 · push · PR 없음. frontend의 미커밋 변경은 건드리지 않았다.

작업 중에 코디 정정이 두 번 왔고 둘 다 반영했다:
- 브리프 3번(병원당 동시 1개)은 결정 8(Redis 10초 캐시)로 바뀌었다. 한때 만들었던 병원 잠금 · 차례 대기는 **뺐다**.
- 브리프 2번(서버 시작 때 시드)은 결정 9(데이터 migration)로 바뀌었다. 한때 넣었던 worker 기동 시드(`seed_all` · WORKER_STARTUP 핸들러 · 그 테스트)는 **뺐다**.

## 결정 4: 행 경합은 날짜 쪽이 양보
- `services/emr_date_sync.py` 반영 transaction의 첫 문장이 `select(set_config('lock_timeout', '<ms>ms', true))`다. 이는 `SET LOCAL`과 같다. raw `text()`를 쓰지 않은 것은 taut 규칙 때문이다.
- 상한 값은 설정 `RESERVATION_DATE_LOCK_TIMEOUT_MS`(기본 1500 · 100 ~ 10000 · `common/config.py`)에서 온다.
- 일정의 방문을 고객 외부 id 순으로 정렬한 뒤 반영한다. 고객 행을 정렬된 순서로 쓰게 되어 교착이 줄어든다. 시술권 · 카드는 이미 고객 정렬 순이다.
- `lock_timeout`(55P03)이나 교착(40P01)이 나면 `DateRowBusy`(ValueError) → 회차 `error`(`error_kind = "DateRowBusy"`)다. 되돌리므로 중간 상태가 없고 캐시도 지운다.
- 오늘 회차의 transaction에는 상한을 걸지 않았다. 오늘 회차 코드는 그대로다.
- 시험 `test_결정4_오늘_쪽이_행을_쥐면_날짜_쪽이_양보한다`(실 PostgreSQL):
  - 다른 transaction이 그 고객 행을 `FOR UPDATE`로 쥔다.
  - 날짜 쪽은 5초 안에 `error` / `DateRowBusy`로 끝난다(상한 1.5초).
  - 쥔 쪽의 UPDATE + commit은 1초 안에 끝난다(기다리지 않음).
  - 날짜 쪽 방문은 0행이고 캐시 표시가 지워진다.
  - 쥔 쪽 값이 남고, 풀린 뒤 다시 돌리면 `done`이다.

## 결정 8: 잠금 전에 Redis 10초 캐시 (병원당 상한 없음)
- 표시 키는 `day:emr:reservation_date_recent:{병원}:{날짜}`이고 값은 한 곳이다. TTL은 설정 `RESERVATION_DATE_CACHE_SECONDS`(기본 10)다. 키 · 읽기 · 세우기 · 지우기 함수는 `services/reservations.py`의 `recent_key` · `recently_refreshed` · `mark_refreshed` · `forget_refreshed`.
- **화면 쪽**(`request_refresh`): 표시가 있으면 kiq를 하지 않고 `False`를 돌려준다(info 로그). 캐시를 못 읽으면 경고 로그만 남기고 그래도 넣는다. 같은 날짜 잠금이 중복을 막는다.
- **worker 쪽**(`run_reservation_date`):
  - 표시가 있으면 새 상태 `skipped_recent`로 끝난다. 이때 잠금도 잡지 않는다.
  - 없으면 그대로 (병원, 날짜) 잠금(`try_lock`)을 잡는다.
  - 표시는 **최신화가 시작될 때**(잠금 안 body 첫 줄) 세운다. 그래서 진행 중에 들어온 요청도 막힌다.
  - `error` · `timeout` · 예외면 표시를 지운다. 다음 열기에 다시 돈다.
- 「병원당 날짜 최신화 동시 1개」는 없다. 다른 날짜는 동시에 돈다(시험 있음).
- `emr_sync.Status`에 `skipped_recent`를 더했다(리터럴 하나).
- 시험:
  - 실 Redis · PostgreSQL:
    - 끝난 뒤 TTL은 0초 초과 · 10초 이하이고 다시 요청하면 `skipped_recent`다(일정 조회 1회).
    - 진행 중 요청은 `skipped_recent`다.
    - 캐시가 만료된 순간 겹친 요청은 잠금이 막아 `skipped_locked`다.
    - 실패하면 표시가 지워진다.
    - 다른 날짜는 동시에 `done`이다.
  - 화면 쪽(가짜 Redis):
    - 표시가 있으면 kick이 0이다.
    - 다른 날짜는 넣는다.
    - 캐시 읽기에 실패해도 넣는다(경고 로그).

## 결정 9: 권한 행 = 데이터 migration
- 새 파일 `migrations/versions/20261123_0015_reservation_permission.py`(`0014_device_platform_android` 다음).
  - upgrade = `INSERT … SELECT id, 'reservation', 'view' FROM job_role WHERE deleted_at IS NULL ON CONFLICT (job_role_id, permission_key) DO NOTHING`
  - downgrade = `DELETE FROM job_role_permission WHERE permission_key = 'reservation'`
  - 칸 · 표 · 인덱스 · enum 변경은 없다.
- 기존 시드(`default_permissions.seed` · 기준 정보 회차 · 로그인 준비)는 그대로다. 이후 새로 들어오는 직무가 그쪽 몫이다. docstring에 「언제」를 적었다.
- `tests/migrations/test_alembic.py`의 `HEAD`를 `0015_reservation_permission`으로 바꿨다.
- 새 시험 `tests/migrations/test_reservation_permission_migration.py`:
  - 본문 검사: 0014를 잇는지, 데이터만 바꾸는지.
  - **왕복**: 0014 상태에 직무 넷(그냥 · `reservation` edit로 고친 직무 · 그 키를 지운 직무 · 지운 직무)과 다른 키 행을 넣는다.
    - upgrade: 「그냥」 직무에만 view가 들어간다. 고친 행 · 지운 행 · 지운 직무는 그대로다.
    - downgrade: 그 키 행만 빠지고 다른 행은 이전과 같다.
    - 다시 upgrade: 살아 있는 직무 셋에 view가 들어간다.

## 검증
- `./scripts/test.sh -q backend/tests/day/emr backend/tests/day/test_reservation_refresh.py backend/tests/day/web/test_reservation_page.py backend/tests/day/test_reservation_rules.py backend/tests/day/test_reservation_queries.py backend/tests/day/board/test_reservation_permissions.py backend/tests/day/test_default_permissions.py backend/tests/day/board/test_board_default_view.py backend/tests/runtime backend/tests/migrations`(격리 PostgreSQL · Redis): **428 passed**
  - `tests/day/emr` 전체 통과 = 오늘 회차 회귀 없음
  - `tests/migrations` 전체 통과(0015 왕복 · alembic head · check · offline SQL 포함)
- `./scripts/test.sh --pure -q backend/tests/architecture`: **317 passed**
- `ruff check` · `ruff format --check`(backend/day · common · migrations · tests): 통과
- `mypy`(전체): Success, 476 files
- `taut check`: diagnostics 0. 첫 구현의 `text("SET LOCAL …")`이 TAUT raw SQL 진단에 걸려 `set_config`로 바꿨다.

## 바꾼 파일 (이번 고침)
- `backend/day/services/emr_date_sync.py`: 결정 4 · 8
- `backend/day/services/reservations.py`: 캐시 키 · 읽기 · 세우기 · 지우기 · `request_refresh` 앞 확인
- `backend/day/services/emr_sync.py`: `Status`에 `skipped_recent`
- `backend/common/config.py`: `reservation_date_lock_timeout_ms` · `reservation_date_cache_seconds`
- `backend/day/services/default_permissions.py`: docstring만(「언제」 · migration 0015)
- `backend/day/tasks/emr.py`: 이번 고침의 순변경 없음(넣었다 뺀 기동 시드)
- `backend/migrations/versions/20261123_0015_reservation_permission.py`(새)
- 테스트:
  - `backend/tests/day/emr/test_date_sync.py`: A5를 캐시에 맞춤 · 결정 8 두 개 · 결정 4 하나
  - `backend/tests/day/test_reservation_refresh.py`: 캐시 셋
  - `backend/tests/migrations/test_reservation_permission_migration.py`(새)
  - `backend/tests/migrations/test_alembic.py`: HEAD

## 이슈 · 코디가 확인할 것
- **migration 배포**: 이 PR이 0015를 더한다. deploy-dev · prod의 migrate 단계(`.github/workflows/migrate-prod`)로 적용된다. 실제 DB에는 적용하지 않았다(브리프).
- **설정 두 개**(`RESERVATION_DATE_LOCK_TIMEOUT_MS` · `RESERVATION_DATE_CACHE_SECONDS`)는 기본값이 있어서 `deploy/config/*.env`에 넣지 않아도 된다.
- **캐시의 대가**: 표시를 세운 10초 안에 KOS가 바뀌면 그 10초 동안 다시 열어도 최신화하지 않는다(결정 8이 받아들인 것).
- **양보의 대가**: 오늘 쪽이 같은 고객 행을 쥐는 바쁜 시간에는 날짜 최신화가 `DateRowBusy`로 실패할 수 있다. 다시 열면 다시 돈다. 실패 표시는 2루프(R19)다.
