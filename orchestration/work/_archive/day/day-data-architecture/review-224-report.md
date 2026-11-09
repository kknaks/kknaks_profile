# 리뷰 리포트 — day-data-architecture / code · Delivery #224 백엔드 뼈대 (2026-11-05)

대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture`(브랜치 `kknaksss/day-data-architecture`, HEAD = `origin/v2-dev` = `8e4fb4b5`) 의 미커밋 변경 — `AGENTS.md` 수정 + 신규 41 파일(`git status --short -uall`). 읽기 전용, 파일 수정 0.

근거 표기: **I#224** = GitHub Delivery Issue #224(「바뀌는 것」 B1~B5 · 「하지 않는 것」 · A1~A5) · **AG** = 워크트리 `AGENTS.md` 절 · **SYS D-n** = `reference/2026-11-03-cc-day/system/README.md` 결정 번호 · **CT** = centurion `origin/main` · **TS** = centurion `docs/development/testing-strategy.md`.

## 판정: WARN

완료 조건 A1 ~ A5 는 내가 직접 돌려 전부 확인했다(아래 「직접 돌린 명령」). 「하지 않는 것」을 넘은 곳은 없다. FAIL 은 없다.
다만 **#225 · #226 이 그대로 물려받으면 깨지는 자리가 3개**(W1 · W2 · W3)다 — 머지 전 또는 #225 착수 전에 정해야 한다.

## 계약 대조 (I#224)

| 항목 | 결과 | 근거(코드) |
|---|---|---|
| B1 Python 3.13 · uv · api 헬스체크 | 같음 | `.python-version:1` 3.13(CT 와 같음) · `pyproject.toml:5` · `runtime/health.py:54-69` |
| B2 env 설정 APP_ENV · DB_SCHEMA → MetaData · version_table_schema · search_path | 같음 (값의 출처 하나 = `get_settings().db_schema`) | `common/config.py:34-35,65-67` · `common/db/model_base.py:24` · `migrations/env.py:29,43` · `common/db/session.py:39-41` |
| B3 runtime · common(config · errors · db) · day 빈 패키지 · alembic 빈 첫 revision · 로컬 compose | 같음 (+ `common/redis.py` · `common/tasks/` 추가 — Redis 가 B4 에 필요해 정당) | `versions/20261105_0001_baseline.py` · `deploy/compose.local.yaml` |
| B4 taskiq worker · scheduler(Redis · taskiq-redis, RabbitMQ 없음), 동기화 태스크 없음 | 같음 — 샘플 `day.ping` 만 | `common/tasks/broker.py:24-39` · `runtime/tasks.py:18-22` · `runtime/scheduler.py:12` |
| B5 import 경계 테스트(day → common · day.public 단일 입구) | 같음 + 추가 규칙(common↛runtime · day↛runtime) | `tests/architecture/test_import_boundaries.py` |
| 하지 않는 것(화면 · 시술 현황 · 알림 · prod 배포 · 업무 테이블 · KOS · 로그인) | 안 넘음 — `backend/day/` 는 `__init__.py` · 빈 `public.py` 뿐, emr · models · templates 없음 | `backend/day/public.py:7` |
| 「검토할 부분」 AGENTS.md schema 표기 갱신 | 이 PR 에 포함 — SYS D-7(사용자 2026-11-05)과 맞고 be-brief §5 허용 범위(두 표기 + 실행 명령) 안 | `git diff AGENTS.md` 3 hunk |

## FAIL

없음.

## WARN

### W1 (높음 · #225 착수 전) 테스트의 기본 스키마가 `day_dev` 다 — 그리고 `Base` 의 스키마는 import 순간 굳는다
- `backend/tests/conftest.py:16-18` 은 「day_dev 에 닿지 않게」 env 를 지운다고 적었지만, 지우면 `common/config.py:35` 기본값으로 떨어져 테스트 프로세스의 `DB_SCHEMA` 는 **`day_dev`** 다(`tests/common/test_config.py:7-12` 가 그것을 단언한다).
- `common/db/model_base.py:24` `MetaData(schema=get_settings().db_schema)` 는 import 시점 값으로 고정된다. 직접 확인: `DB_SCHEMA=day_probe` 로 import → env 를 `day_other` 로 바꾸고 `cache_clear()` 해도 `Base.metadata.schema == "day_probe"` 그대로.
- MetaData 에 스키마가 박히면 SQL 이 `day_dev.<table>` 로 **명시 한정**돼 `search_path` 로 격리가 안 된다. 지금은 모델이 0개라 무해하지만, #225 가 in-process 로 `create_all` · 서비스 테스트를 쓰는 순간 로컬 개발 데이터(`day_dev`)에 테이블을 만들고 지운다. 현재의 「테스트마다 `day_test_<hex>`」 방식은 **subprocess(alembic) 에서만** 통한다(`tests/migrations/test_alembic.py:25-41`).
- 근거: AG 「작업 규칙 — 공유 DB 를 테스트에 쓰지 않는다」의 취지 · TS §9 「테스트에서 운영·STG DB 나 Redis 를 사용하지 않는다」 · 브리프 §6-6 「테스트가 `day_dev` 를 건드리지 않는지」.
- 고칠 방향: conftest 가 env 를 지우는 대신 **`DB_SCHEMA=day_test` 를 먼저 넣는다**(어떤 `common`/`day` import 보다 앞). #225 의 DB 테스트는 테스트 스키마를 `execution_options(schema_translate_map={settings.db_schema: test_schema})` 로 바꾸거나 고정 `day_test` 를 세션 시작/끝에 만들고 지우는 fixture 로. 「기본값은 day_dev」 단언은 `Settings(_env_file=None)` 생성 테스트로 옮긴다.

### W2 (높음 · #225 착수 전) DAY 의 `Base` 가 `common` 에 있다 — AG 「모델 감추기」·트리 · CT 모양과 어긋남
- `backend/common/db/model_base.py:21-24` 에 DAY 스키마가 박힌 `Base`, `common/db/__init__.py:3,14` 이 그것을 공개한다.
- AG 트리는 `day/db.py — 설정 · Base/세션(schema=DB_SCHEMA)`, AG 계층 규칙은 「ORM 모델 · `Base` 는 `day` 밖으로 내보내지 않는다」. `common` 에 있으면 `runtime` 이 `from common.db import Base` 로 `Base.metadata.tables`(= #225 의 모든 테이블)에 닿고, 경계 테스트는 이것을 막지 못한다(`test_import_boundaries.py:24-29` 에서 runtime → common 은 허용).
- CT 의 본: `common/db/model_base.py` 는 **스키마 없는 공통 Base + NAMING_CONVENTION**, 도메인 Base 는 `crm/db.py`(`MetaData(schema="crm")` · `SEARCH_PATH` · `CONNECT_ARGS`).
- 경위: be-brief §6-3 이 「common/db · `model_base`(`MetaData(schema=DB_SCHEMA)`)」로 지시했고 I#224 B3 도 「common(… db session/model_base)」라 워커 잘못은 아니다 — **브리프와 AG 의 충돌**이다.
- 고칠 방향: `common/db/model_base.py` 는 `NAMING_CONVENTION` 만(또는 `make_metadata(schema)` 같은 도구), `backend/day/db.py` 에 `class Base(DeclarativeBase): metadata = MetaData(schema=get_settings().db_schema, naming_convention=…)`. alembic `env.py:21` 은 `from day.db import Base`(migrations 예외로 허용됨). 모델이 0개인 지금 옮기는 게 가장 싸다.

### W3 (높음 · #226 착수 전) 워커 리포트의 태스크 등록 계획이 경계 테스트에 막힌다
- 리포트 「코디가 확인할 것」 3 은 「#226 이 `day/tasks/` 를 만들면 `runtime/worker.py` 에 import 한 줄 추가」라고 한다. 그런데 `test_import_boundaries.py:65-67` 은 runtime 이 `day.public` 밖을 import 하면 실패시킨다 → `import day.tasks` 는 **빨간불**. 계획대로 하면 #226 이 경계를 넓히거나 우회하게 된다.
- 브로커를 `common/tasks/broker.py` 에 둔 것 자체는 받아들일 만하다 — 스키마 · 도메인 지식이 없는 Redis 인프라라 `common` 성격이고, day 태스크가 runtime 을 import 할 수 없으니. (CT 는 `linky/tasks/broker.py` 지만 linky 는 진입점도 자기 패키지에 있다.)
- 고칠 방향(하나 정할 것): (a) taskiq CLI 의 모듈 인자로 등록 — `taskiq worker runtime.worker:broker day.tasks` · `taskiq scheduler runtime.scheduler:scheduler day.tasks`(Python import 가 아니라 경계 무관) — compose `command` 와 AG 실행 명령에 반영. 또는 (b) `day.public` 에 `register_tasks()` 같은 입구를 두고 runtime 이 그것만 부른다. 어느 쪽이든 경계 테스트 파일 머리말에 적는다.
- 덧: 샘플 `day.ping` 이 `runtime/tasks.py` 에 있다(AG 트리상 태스크는 `day/tasks/`). 인프라 핑이라 runtime 에 두는 것은 받아들이되, `runtime/tasks.py:4` 처럼 「업무 태스크는 day/tasks」 문구가 이미 있으니 그대로 둔다.

### W4 (중간) infra 테스트가 env 없으면 조용히 skip → CI 에서 「27 passed」가 초록으로 보인다
- `backend/tests/conftest.py:28-36` — `DAY_TEST_DATABASE_URL` · `DAY_TEST_REDIS_URL` 둘 중 하나라도 없으면 infra 5개(A3 alembic 3 · ready 200 · 태스크 왕복)가 전부 skip. `uv run pytest -q` → `27 passed, 5 skipped` 종료 코드 0. A3 · A4 의 유일한 자동 증거가 사라져도 초록이다.
- 근거: TS §10 「새 skip … 으로 실패를 숨기지 않는다」 · AG 「테스트 — migration 은 실제 PostgreSQL 로 검증」.
- 고칠 방향: `DAY_REQUIRE_INFRA=1`(또는 `CI=true`)이면 skip 대신 `pytest.fail`/`UsageError`. `scripts/test.sh` 가 이 값을 켠다. CI 를 붙일 때 `scripts/test.sh` 만 쓰도록 AG 실행 명령에 한 줄. 지금 CI 가 없으니 머지 차단은 아님.

### W5 (중간 · #226) 프로세스 공용 Redis 클라이언트의 `socket_timeout` 이 헬스체크 timeout(2초)에 묶였다
- `backend/common/redis.py:24-27` — `get_redis()` 는 앞으로 잠금(SYS D-6) · pub/sub(SSE 신호, SYS 기본값)도 쓸 클라이언트인데 `socket_timeout=health_check_timeout_seconds`. pub/sub `listen()` · 블로킹 명령은 2초마다 `TimeoutError` 로 끊긴다. 설정 이름도 의미와 다르다.
- 근거: AG 백엔드 안전 「timeout … 을 명시한다」(명시하되 용도별로).
- 고칠 방향: `REDIS_SOCKET_TIMEOUT_SECONDS` 같은 별도 설정을 두고, 헬스 probe 는 이미 `asyncio.timeout`(`runtime/health.py:40`)이 상한을 걸고 있으니 클라이언트 timeout 에 기대지 않는다.

### W6 (낮음) DB 쿼리 timeout 이 없다
- `backend/common/db/session.py:48-55` — `pool_timeout` 만 있고 asyncpg `command_timeout` · 서버 `statement_timeout` 이 없다. 헬스는 `asyncio.timeout` 으로 막혀 있으나 #225 이후 서비스 쿼리는 상한이 없다.
- 근거: AG 백엔드 안전 「timeout · 취소 · 동시성 상한을 명시한다」.
- 고칠 방향: `connect_args` 에 `command_timeout` 또는 `server_settings={"statement_timeout": …}` 를 설정값으로. 다음 Delivery 몫이어도 된다.

### W7 (낮음) 경계 검사기의 구멍과 넓은 예외
- `test_import_boundaries.py:32` `DAY_INTERNAL_ALLOWED = {"day", "migrations"}` — 필요한 것은 `migrations/env.py` 가 `day.models`(W2 를 고치면 `day.db`)를 읽는 것뿐인데 `migrations/versions/*` 까지 day 내부 전부를 import 할 수 있다(리비전이 현재 모델을 import 하면 과거 리비전이 나중에 깨진다).
  → 예외를 `migrations/env.py` 와 `day.models` · `day.db` 로 좁힌다.
- 못 잡는 형태: `importlib.import_module("day.models")` · `__import__` 문자열 import. `common → migrations` 금지 없음(`:25`). leak 테스트(`:130-141`)는 클래스만 보고 `from day import models` 처럼 **모듈째** 다시 내보내는 것은 못 잡는다.
  → 문자열 import 는 `ast.Call` 로 `import_module`/`__import__` 첫 인자 상수를 검사, leak 테스트에 `isinstance(value, ModuleType)` 금지 추가.
- 검사기 자체는 진짜로 깨진다: 자기 테스트(`:85-127`)가 절대 · 함수 안 · 상대 import 위반을 잡는 것을 확인했고, `test_검사_대상_패키지가_전부_있다`(`:79-82`)가 새 최상위 패키지가 생기면 규칙 추가를 강제한다 — 좋음.

### W8 (낮음) alembic offline(`--sql`) 은 스키마를 만들지 않는다
- `backend/migrations/env.py:82-85` — 직접 확인: `alembic upgrade head --sql` 출력이 `CREATE TABLE day_dev.alembic_version` 로 시작하고 `CREATE SCHEMA` · `SET search_path` 가 없다. DBA 에게 SQL 을 넘기는 방식(관리형 DB 에서 흔함)으로 첫 적용하면 실패한다.
- 고칠 방향: offline 분기에서 `context.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")` · `SET search_path` 를 먼저 낸다. prod 배포는 범위 밖이라 다음 Delivery 몫이어도 된다.

### W9 (낮음) 그 밖의 자리
- `deploy/compose.local.yaml:19-23,99-105` — worker · scheduler 가 `migrate` 완료를 기다리지 않는다(api 만 `:83-85`). 지금은 DB 를 안 쓰니 무해, #226 의 동기화 태스크는 테이블이 필요 → 그때 `migrate: service_completed_successfully` 추가.
- `.dockerignore` 없음 — `compose.local.yaml:66-68` build context 가 레포 루트라 `deploy/local.env` · `.venv` 가 docker 데몬으로 전송된다. 이미지에는 안 들어간다(`deploy/Dockerfile:13,16` 은 `pyproject.toml · uv.lock · .python-version` · `backend` 만 COPY). `.dockerignore` 에 `**/*.env` · `.venv` 를.
- `common/config.py:34-35` — `APP_ENV` 가 없으면 조용히 dev · `day_dev`. SYS D-7 의 「스키마별 DB 계정」이 막아 주지만 prod 서버가 env 를 빠뜨리면 dev 로 뜬다. prod 배포 Delivery 에서 「배포 env 는 APP_ENV 필수」를 넣을 것.
- search_path 가 실제로 걸리는지를 단언하는 테스트가 없다 — `test_config.py:12,23` 은 문자열만 본다. 직접 확인한 결과 걸린다(`SHOW search_path` → `day_probe, public`). infra 테스트에 `SHOW search_path == settings.search_path` 한 줄을 권한다(B2 의 증거).
- AG 저장소 구조 트리에 새 자리(`common/redis.py` · `common/tasks/` · `runtime/health.py · tasks.py · worker.py · scheduler.py`)가 없다. be-brief §5 가 AGENTS.md 수정을 두 곳으로 막았으므로 워커 몫이 아니다 → 코디가 W2 · W3 결정과 함께 트리를 갱신.
- `.gitignore:9-11` — `*.env` 는 `deploy/local.env` 를 막는다(확인: `git check-ignore -v deploy/local.env` → `.gitignore:10:*.env`). `.env.prod` 같은 `.env.*` 형태는 안 막힌다 — 필요하면 `.env.*` + `!*.env.example`.

## 「조용히 통과하는 자리」 (따로 모음)

1. **infra skip** — W4. env 가 하나라도 없으면 A3 · A4 증거 5개가 skip, exit 0.
2. **테스트 기본 스키마 = `day_dev`** — W1. 주석은 반대로 말한다(`conftest.py:16`). 모델이 생기는 순간 테스트가 로컬 `day_dev` 를 만진다.
3. **`Base` 스키마 동결** — W1. 테스트에서 `DB_SCHEMA` 를 바꾸고 `cache_clear()` 해도 ORM 은 안 따라간다. 설정 테스트는 초록.
4. **스키마 없을 때 search_path 폴백** — `search_path = "<DB_SCHEMA>, public"`(`config.py:67`). 스키마가 아직 없으면 `current_schema()` 가 `public` 이 된다(직접 확인). ORM 은 MetaData 로 한정돼 있어 안전하나, 리비전 · raw SQL 의 한정 안 된 이름은 migrate 전이면 `public` 으로 간다. migrate 가 api 앞에 있어(`compose.local.yaml:83-85`) 지금은 막혀 있다.
5. **헬스 probe 의 넓은 `except Exception`**(`health.py:42`) — 의도된 것(응답에 예외 문구를 안 냄)이고 failed 로 드러나므로 조용한 통과는 아니다. 다만 원인 로그가 한 줄도 안 남는다 → `logger.warning("readiness %s failed: %s", name, type(exc).__name__)`(접속값 없이 예외 타입만) 권장.

## 직원이 실물에서 만날 자리

해당 없음 — 화면 · 업무 기능이 없는 뼈대. 운영자가 만날 자리는 `/health/ready` 503(`{"checks":{"redis":"failed"}}` 처럼 어느 쪽인지 보임)뿐이고 확인했다.

## 워커 리포트 「이슈 · 코디가 확인할 것」 1 ~ 8 판정

| # | 내용 | 판정 |
|---|---|---|
| 1 | migrations 를 `day.public` 창구 예외로 | **받아들임(좁힐 것)** — 예외 자체는 AG 「models/ … alembic 이 읽는다」로 정당. 범위를 `migrations/env.py` → `day.models` · `day.db` 로 좁힌다(W7). |
| 2 | `Base` 를 `common/db/model_base.py` 에 | **고칠 것** — W2. 브리프 지시였지만 AG 「모델 감추기」 · 트리 · CT `crm/db.py` 모양과 어긋남. 모델 0개인 지금 `day/db.py` 로. |
| 3 | 브로커를 `common/tasks/broker.py` 에, #226 이 `runtime/worker.py` 에 import 추가 | **위치는 받아들임 · 등록 계획은 고칠 것** — W3. 계획대로면 경계 테스트가 실패한다. CLI 모듈 인자 또는 `day.public` 입구로 지금 정한다. |
| 4 | REDIS_URL 없으면 브로커 import 실패(메모리 브로커 폴백 없음) | **받아들임** — 조용한 폴백 없는 것이 맞다. api 는 broker 를 import 안 함 확인(`runtime/main.py` import 목록). 단 #226 단위 테스트가 `day.tasks` 를 import 하려면 `tests/runtime/test_tasks.py:27-32` 같은 fixture 가 필요하다는 점을 #226 브리프에 적을 것. |
| 5 | `compose.test.yaml` 없이 스키마로 테스트 격리 | **조건부 받아들임** — DB 1개 · 스키마 분리(SYS D-7)와 맞다. 조건: W1(테스트 기본 스키마를 `day_test` 로, in-process ORM 격리 방법)을 먼저 고칠 것. |
| 6 | 로컬 Redis 비밀번호가 compose `command` 에 노출 | **받아들임** — 로컬 한정 · 127.0.0.1 바인딩(`compose.local.yaml:51`) · 값은 gitignore 된 `local.env`. |
| 7 | 컨테이너 내림 · 볼륨 · 이미지 · `deploy/local.env` 남김 | **받아들임** — 확인: `local.env` 는 ignore 되고 그 비밀값 3개는 커밋 대상 파일 어디에도 없다(grep 0건). |
| 8 | 구조화 JSON 로그 안 함 | **받아들임** — I#224 범위 밖. SYS 「기본값 — 로그」 이므로 다음 Delivery 몫. |

## DB_SCHEMA 점검 (브리프 §6-2)

- **같은 한 값**: MetaData(`model_base.py:24`) · version_table_schema(`env.py:29,43`) · search_path(`config.py:65-67` → `session.py:39-41`, `env.py:72`) · `include_name`(`env.py:33-37`) 모두 `get_settings().db_schema` 하나. PASS. 테스트 스키마는 subprocess alembic 에선 같은 경로(env)로 들어가 PASS, in-process 는 W1.
- **SQL 에 그대로 들어가는 자리**: `env.py:58` `CREATE SCHEMA {SCHEMA}` · search_path. `config.py:24,49-54` 가 `^[a-z_][a-z0-9_]{0,62}$` 로 막는다 — 인젝션 · 따옴표 문제 없음. 테스트 `test_config.py:47-54`. PASS. (`public` · `pg_*` 같은 이름도 통과하지만 dev 가드상 실제 해 없음 — 참고.)
- **APP_ENV ↔ DB_SCHEMA 가드**: prod ⇒ `day_prod` 만, dev ⇒ `day_prod` 금지(`config.py:56-63`), 테스트 `test_config.py:33-44`. PASS.
- **첫 migrate 의 스키마 생성**: `env.py:52-58` 이 `pg_namespace` 로 있는지 보고 없을 때만 `CREATE SCHEMA`. 관리형 DB(CREATE DATABASE 없음 · CREATE SCHEMA 는 DB 의 CREATE 권한 필요)와 맞다 — 스키마별 계정에 DB CREATE 가 없으면 DBA 가 미리 만들고 env 는 지나간다. PASS. offline 모드는 W8.

## 직접 돌린 명령과 수치

| 명령 | 결과 |
|---|---|
| `lsof -nP -iTCP:11040 -iTCP:11042 -iTCP:11043 -sTCP:LISTEN` | 비어 있음 (사용자 컨테이너 5433 · 5434 · 55434 · 57792 · 57823 와 안 겹침, 손대지 않음) |
| `uv run ruff check backend` | All checks passed! |
| `uv run pytest -q` (인프라 없이) | **27 passed, 5 skipped** in 0.41s |
| `docker compose -f deploy/compose.local.yaml --env-file deploy/local.env up -d --wait postgres redis` → `scripts/test.sh -q` | **32 passed** in 1.83s (2회째 1.70s, 같음) |
| `… --profile app up -d --build --wait` | api healthy · migrate Exited(0) · worker · scheduler Up |
| `curl :11040/health/live` · `/health/ready` | `{"status":"ok","checks":{}}` 200 · `{"status":"ok","checks":{"database":"ok","redis":"ok"}}` 200 — **A1** |
| psql `information_schema.tables where table_name='alembic_version'` | `day_dev.alembic_version` 만 (public 없음) · 스키마 `day_dev` 하나 — **A3** (upgrade/downgrade 왕복은 infra 테스트 3개 통과) |
| scheduler · worker 로그 | `Startup completed` → `Sending task day.ping` → `Listening started` → `Executing task day.ping` → `runtime.tasks day.ping at=2026-11-05T07:06:46Z` — **A4** |
| `compose stop redis` 후 `/health/ready` | `{"status":"degraded","checks":{"database":"ok","redis":"failed"}}` **503**, 0.06s — 접속값 · 예외 문구 없음 |
| `git check-ignore -v deploy/local.env` · local.env 비밀값 3개를 커밋 대상(tracked + untracked-not-ignored) 파일에서 grep | `.gitignore:10:*.env` · **0건** — **A5** (env 파일은 `deploy/local.env.example` 자리표시자만) |
| 스크래치 probe: `DB_SCHEMA=day_probe` 엔진 `SHOW search_path` · Base 스키마 동결 | `day_probe, public` (current_schema=public — 스키마 없음) · env 바꾼 뒤에도 `Base.metadata.schema == day_probe` (W1 근거) |
| `alembic upgrade head --sql` | `CREATE TABLE day_dev.alembic_version` 부터 — `CREATE SCHEMA` 없음 (W8 근거) |
| `… --profile app down` | 컨테이너 · 네트워크 내림. 볼륨 `day-local_day_postgres_data` · `day-local_day_redis_data` 남김 |

버전(uv.lock 설치): taskiq 0.12.6(SYS D-5 · CT 고정과 같음) · taskiq-redis 1.2.2 · fastapi 0.162.0 · sqlalchemy 2.1.8 · alembic 1.20.1 · redis 7.4.1.

## 참고(기존 부채 · 무관)

- 무관한 실패 없음 — `v2-dev` 는 빈 브랜치라 기존 테스트가 없다.
- `reference/2026-11-03-cc-day/system/README.md` 「이미 정한 것」 3번째 줄은 아직 「PostgreSQL(`day` 스키마)」 — D-7 과 어긋나는 문서 잔재(레포 밖, 코디 몫).
- 역할 문서 `tools.md` 는 「테스트 실행 금지」지만 이번 브리프 §6 이 실행을 명시 허용해 브리프를 따랐다. 레포 파일 수정 0.

## 권장 처리 순서

1. 이 PR 안에서(싸다): **W1**(conftest `DB_SCHEMA=day_test`) · **W2**(`Base` → `day/db.py`) · **W3**(태스크 등록 방식 결정 + compose command) · **W4**(`DAY_REQUIRE_INFRA`).
2. #225 브리프에: W1 의 in-process 스키마 격리 방법 · W6 쿼리 timeout · W7 migrations 예외 좁히기 · search_path 단언 테스트.
3. #226 브리프에: W3 결정 · W5 Redis timeout 분리 · W9 worker 의 migrate 의존.
4. prod 배포 Delivery 에: W8 offline SQL · APP_ENV 필수화 · `.dockerignore`.
