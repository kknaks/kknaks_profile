# #224 DAY v2 백엔드 뼈대 결과 보고

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` (브랜치 `kknaksss/day-data-architecture`, base `v2-dev` 8e4fb4b5). 커밋 · push · PR 안 함 — 변경은 워크트리에만.

## 수행 — 파일 · 모듈

| 단계 | 파일 |
|---|---|
| 1 프로젝트 · 설정 | `pyproject.toml` · `uv.lock` · `.python-version`(3.13) · `.gitignore` · `backend/common/config.py`(pydantic-settings: `APP_ENV` dev/prod · `DB_SCHEMA` 기본 `day_dev` · `DATABASE_URL` · `REDIS_URL` SecretStr) · `backend/common/errors.py`(`ServiceError` — centurion 모양) |
| 2 runtime · 헬스체크 | `backend/runtime/main.py`(`create_application` factory · lifespan 에서 엔진 · Redis 정리 · `ServiceError` 핸들러) · `backend/runtime/health.py` · `backend/common/redis.py` |
| 3 common/db · alembic | `backend/common/db/{__init__,model_base,session}.py`(`MetaData(schema=DB_SCHEMA, naming_convention)` · 접속 `search_path = "<DB_SCHEMA>, public"`) · `backend/migrations/{alembic.ini,env.py,script.py.mako}` · `backend/migrations/versions/20261105_0001_baseline.py`(빈 첫 리비전) |
| 4 로컬 compose | `deploy/compose.local.yaml`(postgres 16 · redis 7 + profile `app`: migrate · api · worker · scheduler) · `deploy/Dockerfile` · `deploy/local.env.example` · `scripts/test.sh` |
| 5 taskiq | `backend/common/tasks/broker.py`(`RedisStreamBroker` + `RedisAsyncResultBackend`) · `backend/runtime/tasks.py`(샘플 `day.ping`) · `backend/runtime/worker.py` · `backend/runtime/scheduler.py`(`LabelScheduleSource`) |
| 6 아키텍처 테스트 | `backend/tests/architecture/test_import_boundaries.py` |
| day 패키지 | `backend/day/__init__.py` · `backend/day/public.py`(빈 `__all__`) |
| 테스트 | `backend/tests/{conftest,infra}.py` · `tests/common/test_config.py` · `tests/runtime/test_health.py` · `tests/runtime/test_tasks.py` · `tests/migrations/test_alembic.py` |
| AGENTS.md | 두 곳만: `schema="day"` → `schema=`DB_SCHEMA`` · 「테이블은 `day` 스키마」→ env `DB_SCHEMA`(dev `day_dev` / prod `day_prod`) · 「테스트」절 실행 명령 |

## 정한 이름 (외부 계약 — 처음 생김)

| 항목 | 값 | 근거 |
|---|---|---|
| 헬스체크 | `GET /health/live` — 항상 200 `{"status":"ok","checks":{}}` · `GET /health/ready` — DB · Redis 를 2초 timeout 으로 동시 확인, 정상 200 `{"status":"ok","checks":{"database":"ok","redis":"ok"}}`, 하나라도 실패면 503 `status:"degraded"` + 실패 항목 `"failed"`(접속값 · 예외 문구는 안 나감) | centurion linky `health_router.py`(live/ready 분리 · degraded 503) + sso `health_service.py`(database · redis 확인 · 2초 timeout · "ok"/"failed"). DAY 는 앱이 하나라 서비스 접두어 없이 루트 `/health/*` |
| 태스크 이름 | `day.ping` — `schedule=[{"interval": 60}]`, 실행 시각(UTC ISO) 반환 · 로그 | 샘플 1개 |
| 큐 | Redis Stream `day:tasks` · consumer group `day` · maxlen ≈10000 · 결과 키 접두어 `day:task-result` · 결과 TTL 3600초(`TASK_RESULT_TTL_SECONDS`) | |
| 진입점 | api `uvicorn runtime.main:create_application --factory` · worker `taskiq worker runtime.worker:broker` · scheduler `taskiq scheduler runtime.scheduler:scheduler` · migrate `alembic -c backend/migrations/alembic.ini upgrade head` | centurion compose 모양 |
| 포트(127.0.0.1 만) | api **11040** · PostgreSQL **11042** · Redis **11043** — 띄우기 전 `lsof` 로 비어 있음 확인. 사용자 컨테이너(5433 · 5434 · 55434 · 57792 · 57823)와 안 겹침 | 기본 5432 · 6379 · 8000 회피 |
| 테스트 격리 | DB = 로컬 compose 같은 DB 안에서 테스트마다 새 스키마 `day_test_<hex>`(끝나면 DROP) · health infra 테스트는 `day_test` · Redis = db 15 | `DB_SCHEMA` 방식 그대로 — `day_dev` 안 건드림 |

## 검증 — 명령과 수치

| 완료 조건 | 증거 |
|---|---|
| **A1** compose 위 api 헬스체크 | `docker compose -f deploy/compose.local.yaml --env-file deploy/local.env --profile app up -d --build --wait` → postgres · redis · api Healthy, migrate Exited(0), worker · scheduler Up. `curl :11040/health/live` → `{"status":"ok","checks":{}} HTTP 200` · `curl :11040/health/ready` → `{"status":"ok","checks":{"database":"ok","redis":"ok"}} HTTP 200` |
| **A2** pytest | `scripts/test.sh -q`(로컬 compose PG · Redis) → **32 passed in 2.12s**. 인프라 없이 `uv run pytest -q` → 27 passed, 5 skipped(infra). 내역: config 11 · health 4 · tasks 5 · alembic 3 · architecture 9. `uv run ruff check backend` → All checks passed |
| **A3** alembic · DB_SCHEMA | 테스트: 새 스키마에 upgrade head → `<schema>.alembic_version = ['0001_baseline']`, `public.alembic_version` 없음 · downgrade base → `[]` → 다시 upgrade → `['0001_baseline']` · heads 하나. compose migrate: `Running upgrade -> 0001_baseline`, psql 로 `day_dev.alembic_version` 만 존재 · 값 `0001_baseline` |
| **A4** worker · scheduler | scheduler 로그 `Startup completed` → `Sending task day.ping` · worker 로그 `Listening started` → `Executing task day.ping with ID ca49…` → `runtime.tasks day.ping at=2026-11-05T07:00:28Z`. 수동 `ping.kiq()` → `wait_result` = `is_err=False value=2026-11-05T07:00:43Z`. infra 테스트도 실제 Redis 로 보내고 받아 결과를 읽음 |
| **A5** 비밀값 | 저장소 env 파일은 `deploy/local.env.example`(자리표시자 `<local-db-user>` 등)만. 실제 값은 `deploy/local.env`(gitignore `*.env`, `!*.env.example`) — 이 값이 커밋 대상 파일에 없음을 grep 확인. compose 의 비밀번호는 전부 `${…:?}` 보간. 코드에 접속 문자열 기본값 없음(`SecretStr("")`, 없으면 명시적 오류) |

추가 확인: alembic autogenerate 가 `search_path = DB_SCHEMA` + `MetaData(schema=…)` + `include_schemas` 조합에서 가짜 차이를 내지 않음(임시 모델로 create_all 뒤 `compare_metadata` → `[]`, 스크래치 — 저장소에 남기지 않음). #225 가 이 env 그대로 autogenerate 해도 된다.

## 계약 대조 (Issue #224)

| 항목 | 결과 |
|---|---|
| Python 3.13 · uv 프로젝트, api 헬스체크 응답 | 같음 |
| env 설정 APP_ENV(dev/prod) · DB_SCHEMA(dev day_dev / prod day_prod), MetaData schema · version_table_schema · search_path 가 DB_SCHEMA | 같음. 덧붙인 가드: `APP_ENV=prod` 는 `DB_SCHEMA=day_prod` 만, dev 는 `day_prod` 금지 · 스키마는 소문자 식별자만(SQL 에 그대로 들어가서) |
| runtime · common(config · errors · db) · day 빈 패키지 · alembic 빈 첫 revision · 로컬 compose(PG · Redis) | 같음 |
| taskiq worker · scheduler(Redis · taskiq-redis, RabbitMQ 없음), 실제 동기화 태스크 없음 | 같음 — 샘플 `day.ping` 만 |
| 아키텍처 테스트 day → common · day.public 단일 입구 | 같음 + common 은 day · runtime 금지 · day 는 runtime 금지 · day.public 이 ORM/Base 를 안 내보냄 · 상대/함수 안 import 도 검사 · 검사기 자체 테스트 |
| 하지 않는 것(업무 테이블 · KOS · 로그인 · 화면 · 알림 · prod 배포) | 안 함 |
| 버전 | taskiq 0.12.6(centurion 고정과 같음) · taskiq-redis 1.2.2 · fastapi 0.162 · SQLAlchemy 2.1.8 · alembic 1.20.1 · pydantic-settings 2.16 · redis 7.4 |

## 이슈 · 코디가 확인할 것

1. **migrations 는 `day.public` 창구 예외**로 뒀다 — AGENTS.md 「models/ … alembic 이 읽는다」 때문에 alembic env 가 #225 부터 `day.models` 를 import 해야 한다. 경계 테스트에 `DAY_INTERNAL_ALLOWED = {"day", "migrations"}` 로 명시(runtime 은 여전히 public 만).
2. **Base 위치**: 브리프대로 `common/db/model_base.py` 에 `Base`(schema=DB_SCHEMA)를 뒀다. AGENTS.md 트리는 `day/db.py` 에도 「Base/세션」을 적어 두었으니 #225 에서 `day/db.py` 가 이 Base 를 다시 내보낼지 · 옮길지 정하면 된다. 경계상 `Base` 는 `day.public` 으로 안 나간다.
3. **브로커 위치**: `common/tasks/broker.py` — `day/tasks/` 가 앞으로 여기에 등록해야 하고 day 는 runtime 을 import 못 하므로 common 에 뒀다. worker/scheduler 진입점은 runtime(태스크 모듈 import 로 등록). #226 이 `day/tasks/` 를 만들면 `runtime/worker.py` 에 import 한 줄 추가.
4. 브로커는 import 시점에 만들어져 `REDIS_URL` 이 없으면 import 가 실패한다(조용히 메모리 브로커로 바꾸지 않음 — centurion 의 `APP_ENV=test` 분기는 우리 APP_ENV 가 dev/prod 뿐이라 안 씀). api 는 broker 를 import 하지 않아 REDIS_URL 없이도 뜬다(ready 만 503).
5. 테스트 compose(`compose.test.yaml`)는 따로 두지 않았다 — `DB_SCHEMA` 로 스키마를 갈라 로컬 compose 하나로 테스트(테스트 스키마는 매번 DROP). 필요하면 별도 tmpfs compose 로 나눌 수 있다.
6. 로컬 Redis 비밀번호는 compose `command`(`--requirepass`)에 들어가 `docker inspect` 로 보인다 — 로컬 한정이라 그대로 둠.
7. 컨테이너는 내렸다(`down`). 볼륨 `day-local_day_postgres_data` · `day-local_day_redis_data` 와 이미지 `day-backend:local` 은 남김. `deploy/local.env`(무작위 로컬 값, gitignore)도 워크트리에 남김.
8. 로그 형식은 아직 기본 logging — 구조화 JSON 로그(system README 기본값)는 범위 밖이라 안 함.
