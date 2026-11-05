# #224 검수 WARN 반영(fix1) 결과 보고

## 상태: done

같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture`, 미커밋 이어서. 커밋 · push · PR 안 함. W5 · W6 · W8 · W9(worker 의 migrate 의존 · APP_ENV 필수화)는 손대지 않음.

## W 별 고친 곳

| W | 고친 곳 | 내용 |
|---|---|---|
| **W1** 테스트 기본 스키마 | `backend/tests/conftest.py:13-16` | 어떤 `common` · `day` import 보다 먼저 `APP_ENV` · `DATABASE_URL` · `REDIS_URL` 을 지우고 `os.environ["DB_SCHEMA"] = "day_test"`. 머리말에 이유(Base 스키마가 import 순간 굳음) |
| | `backend/tests/common/test_config.py:7-14` | 「기본값 dev · day_dev」 단언을 `Settings(_env_file=None)` 직접 생성(+ `DB_SCHEMA` delenv)으로 옮김 |
| | `backend/tests/common/test_config.py:69-76` | 새 시험 `test_테스트_프로세스는_day_dev_를_쓰지_않는다` — `get_settings().db_schema == "day_test"` · search_path `day_test, public` · `day.db.Base.metadata.schema == "day_test"` |
| | `backend/tests/infra.py:5` | `TEST_SCHEMA = "day_test"` · health infra 테스트의 개별 `DB_SCHEMA` 덮어쓰기 제거(conftest 값 사용) |
| **W2** Base → day | `backend/common/db/model_base.py:6-17` | 스키마 없는 도구만 — `NAMING_CONVENTION` · `make_metadata(schema)`. `common.db` 는 `Base` 를 공개하지 않음(`backend/common/db/__init__.py`) |
| | `backend/day/db.py:16-22` (새 파일) | centurion `crm/db.py` 모양 — `SCHEMA = get_settings().db_schema` · `class Base(DeclarativeBase): metadata = make_metadata(SCHEMA)` |
| | `backend/migrations/env.py:22` | `from day.db import Base` |
| **W3** 태스크 등록 | `backend/day/tasks/__init__.py` (새, 빈 패키지 + docstring) | 등록 방식 = taskiq CLI 모듈 인자(a) |
| | `deploy/compose.local.yaml:101-106` | worker `taskiq worker runtime.worker:broker day.tasks --workers 1` · scheduler `taskiq scheduler runtime.scheduler:scheduler day.tasks` |
| | `backend/runtime/worker.py:1-6` · `backend/runtime/scheduler.py:1-3` | 진입점 docstring 에 모듈 인자 명시. runtime 은 `day.tasks` 를 Python import 하지 않음(경계 테스트가 `import day.tasks` 를 위반으로 잡는 것을 자기 테스트로 확인) |
| | `backend/tests/architecture/test_import_boundaries.py:11-14` | 머리말에 등록 방식 기록 |
| **W4** infra skip | `backend/tests/infra.py:9` · `backend/tests/conftest.py:34-44` | `DAY_REQUIRE_INFRA=1` 이고 접속값이 없는데 infra 테스트가 있으면 `pytest.UsageError`(실패). 아니면 기존대로 skip |
| | `scripts/test.sh:22` | `export DAY_REQUIRE_INFRA=1` |
| | `backend/tests/test_infra_guard.py` (새) | subprocess pytest 로 확인 — 켜면 returncode≠0 + 메시지, 끄면 `1 skipped` exit 0 |
| **W7** 경계 좁히기 | `backend/tests/architecture/test_import_boundaries.py:38-40` | 예외를 `migrations/env.py` 파일 하나 → `day.db` · `day.models`(하위 포함)만. `migrations/versions/*` 는 day 내부 금지 |
| | 같은 파일 `:31-36` | `common` → `migrations` 금지, `day` → `migrations` 금지, `runtime` → `migrations` 금지 추가 |
| | 같은 파일 `:54-64, 82-85` | `importlib.import_module("…")` · `import_module("…")` · `__import__("…")` 문자열 상수 검사 |
| | 같은 파일 `:192-203` | leak 테스트에 `isinstance(value, ModuleType)` 금지 추가 |
| | 같은 파일 자기 테스트 | `test_문자열_import_도_잡는다` · `test_migrations_는_env_py_만_day_db_와_models_를_읽는다` 추가, 기존 자기 테스트에 `import day.tasks` · `import migrations` 위반 추가. 위반 출력은 줄 순서로 정렬 |
| **조용히 통과 5** | `backend/runtime/health.py:41-48` | probe 실패 시 `logger.warning("readiness %s failed: %s", name, type(exc).__name__)` — 예외 타입만 |
| | `backend/tests/runtime/test_health.py` (degraded 테스트) | caplog 로 `readiness database failed` · `readiness redis failed` 두 줄, 로그에 접속값(`unused` · `127.0.0.1`) 없음 단언 |
| | `backend/tests/common/test_db_session.py` (새, infra) | 실제 PG 에서 `SHOW search_path == get_settings().search_path == "day_test, public"` |
| **ignore** | `.dockerignore` (새) | `.git` · `.venv` · `**/.env` · `**/.env.*` · `**/*.env` · `!**/*.env.example` · 캐시들 |
| | `.gitignore:10` | `.env.*` 추가(`!*.env.example` 유지). 확인: `.env.prod` · `deploy/local.env` ignore, `deploy/local.env.example` 은 안 막힘 |
| **AGENTS.md** | 「저장소 구조」 트리 | `runtime/` 아래 `main.py · health.py` · `worker.py · scheduler.py · tasks.py`, `common/` 아래 `redis.py` · `tasks/`, `day/` 의 `db.py` 줄을 `Base(db.py, schema=DB_SCHEMA)/세션` 으로 |
| | 「계층 규칙」 | 한 줄 추가: 태스크 등록 = taskiq CLI 모듈 인자(`… day.tasks`) |
| | 「테스트」 실행 명령 | `scripts/test.sh` 줄에 `DAY_REQUIRE_INFRA=1`(infra 없으면 skip 아닌 실패) · CI 는 이것만 |

## 검증 — 수치

| 명령 | 결과 |
|---|---|
| `lsof` 11040 · 11042 · 11043 | 비어 있음 → 띄움 |
| `scripts/test.sh -q` (로컬 compose PG · Redis, `DAY_REQUIRE_INFRA=1`) | **37 passed** in 2.65s (전: 32. +config 1 · architecture 2 · search_path 1 · infra guard 2, −0) |
| `uv run pytest -q` (인프라 없이) | 31 passed, 6 skipped |
| `uv run ruff check backend` | All checks passed! |
| `compose --profile app up -d --build --wait` | migrate Exited(0) · api Healthy · `/health/ready` 200 `{"database":"ok","redis":"ok"}` |
| `docker inspect` Cmd | worker `["taskiq","worker","runtime.worker:broker","day.tasks","--workers","1"]` · scheduler `["taskiq","scheduler","runtime.scheduler:scheduler","day.tasks"]` |
| scheduler · worker 로그 | `Startup completed` → `Sending task day.ping` → worker `Listening started` → `Executing task day.ping` → `runtime.tasks day.ping at=2026-11-05T07:12:59Z` |
| psql | 스키마 `day_dev` 하나(테스트 스키마 잔여 없음) · `day_dev.alembic_version = 0001_baseline` |
| `compose … down` | 컨테이너 · 네트워크 내림. 볼륨 남김 |

## 이슈 · 코디가 확인할 것

1. `day/tasks/__init__.py` 는 지금 태스크가 없다 — #226 이 태스크 모듈을 만들면 이 `__init__.py` 에서 import 해야 CLI 모듈 인자로 등록된다(docstring 에 적음). #226 단위 테스트가 `day.tasks` 를 import 하려면 `REDIS_URL` 을 넣은 fixture 가 필요(`tests/runtime/test_tasks.py` 의 `entrypoints` 모양).
2. in-process DB 테스트(#225)는 이제 `day_test` 스키마로 굳는다 — 테스트 시작 시 `day_test` 를 만들고 끝날 때 지우는 fixture(또는 `schema_translate_map`)는 #225 몫. 지금 테스트는 `day_test` 를 만들지 않는다(search_path 확인만).
3. W5 · W6 · W8 · W9 미반영(지시대로).
