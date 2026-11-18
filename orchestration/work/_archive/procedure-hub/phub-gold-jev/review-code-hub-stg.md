# 검수 — 허브 stg 판 코드(WORK-018 · SPEC-003 0.2.0 §11)

- 검수자: reviewer_code(read-only) · 2026-11-18
- 대상: `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD `fdc155b` 위 미커밋) — 바뀐 파일 10(`app/core/app_factory.py` · `app/gold_main.py` · `modules/gold/{config,errors}.py` · `scripts/load_medallion.py` · `Dockerfile` · `README.md` 2 · 시험 2) + 새 파일 `modules/gold/assembly.py` · `tests/test_gold_app_main.py` · `data/medallion/`(101)
- 기준: SPEC-003 §11 · WORK-018 · `impl-hub-stg-instructions.md`(R-1 ~ R-4 코디 답) · `review-spec-003-stg.md` · `_RESUME.md` §2 11-18 행(49 MCP 421)
- 안 건드린 것: 파일 수정 0 · stash · checkout 0 · 서버 기동 0 · 로컬 PG 접속 0. Docker 이미지는 검수용으로 지어 보고 지웠다(`docker rmi` 확인).

## 판정: **PASS** — stg 배포를 막을 것 0. WARN 급 지적 2(시간 한도 60초와 CD 확인 창 · 늦게 끝난 적재가 남기는 「켜짐」 로그)는 절차서 · 설정으로 받을 수 있다

「gold 에서 무엇이 나든 `app.main` 은 뜬다」 를 코드 경로로 따라가 확인했다 — 설정 생성 · 조립 실패(`build_gold_parts_soft` 의 `except Exception`), 판 · F1 ~ F7 · 그 밖의 예외(`load_soft` 세 갈래), 멈춤(데몬 스레드 + `wait_for`) 모두 gold 만 꺼진다. 기존 표면은 바이트 단위로 그대로다: `app.main` OpenAPI 문서 sha256 이 `fdc155b` 와 같고(`eecab968…`), `lifespan.py` · `router/` · `alembic/` · `test_public_api_contract.py` diff 0, CD 와 같은 SQLite 판 전체 pytest 855 passed / 53 skipped.

## 직접 돌린 것(수치)

| # | 무엇 | 결과 |
|---|---|---|
| 1 | WORK-018 §6-2 ③ 묶음 + R-4 셋(`glossary_router` · `glossary_template` · `corpus_import_publication`) — gold env 없음 · `DATABASE_URL=sqlite+aiosqlite:///:memory:` | **336 passed · 7 skipped**(39s) |
| 2 | CD 꼴 전체 `pytest -q --ignore=tests/integration`(SQLite · gold env 없음 · `envs/.env.gold` 없음) | **855 passed · 53 skipped**(77s) — 실패 0 |
| 3 | `uv run ruff check .` | All checks passed |
| 4 | `app.main` import 시간(같은 venv · 3회) — `fdc155b`(git archive 사본) vs 지금 | 0.51 ~ 0.80s → 0.74 ~ 0.82s(약 +0.2s) · 라우트 47 → 49(Mount 2) · OpenAPI paths 38 → 38 · **OpenAPI JSON sha256 동일** |
| 5 | Docker `--target runtime` 빌드(`.dockerignore` 무수정) | `/app/scripts/load_medallion.py` 있음 · `/` 에 `data` 없음 · 이미지 지움 |
| 6 | 이미지 안 `--dry-run`(데이터 · 그림 `:ro` 마운트 · DB env 0) | 요약 첫 줄 경로 셋 `(default)` · `aux_hash 93ec89fd…` · `tables 76 · rows 130446` |
| 7 | 레포 기본 경로 로컬 `--dry-run`(SE4 · `GOLD_EXPECTED_HASH`=§11-0 · `GOLD_IMAGE_DIR`) | exit 0 · `gold_hash 8accbb21…f6228c` · `aux_hash 93ec89fd…6ae0eeb` · `tables 76 · rows 130446` · `image_files 103 checked` |
| 8 | `data/medallion/` ↔ 원천 바이트 대조(`cmp`) | 100 / 100 같음(silver 59 · gold 16 · notes 1 · 원장 24) + README 1 · 13MB · `git check-ignore` 걸림 0 |
| 9 | gold_main 의 문서 화면(합성 fixture · ASGI) | `/procedure-hub/gold/openapi.json` 200 · `/api-docs` 200 · Swagger 가 `/procedure-hub/gold/openapi.json` 을 가리킴 |

`alembic check` 는 돌리지 않았다(로컬 PG 에 임시 DB 를 만드는 쓰기라 read-only 범위 밖). 대신 `git diff fdc155b -- backend/alembic backend/app/model` = 0 · `alembic/env.py` 가 import 하는 모델 불변으로 `fdc155b` 와 같은 결과라고 판단 — 구현 워커의 §6-2 ① 결과로 닫으면 된다.

## 지적 표

| # | 심각 | 파일:줄 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| C-1 | **Med (WARN)** | `app/modules/gold/config.py:66` · `assembly.py:179` · `app_factory.py:45` | 시간 한도 60초 동안 **`app.main` 전체가 요청을 안 받는다**(적재가 lifespan 안 · yield 앞). 원격 DB 가 멈추면 stg 허브는 「죽지는 않지만」 시작 뒤 60초 + import · `verify_connection` · `alembic upgrade` 동안 응답 0. CD 의 Gateway 확인은 `--retry 6 --retry-delay 5 --max-time 10`(최악 약 100초 · `csp-azure-deploy.yml:151-159`)이라 멈춤 + 느린 시작이 겹치면 **CD 가 실패로 찍힐 수 있다**(허브는 늦게 뜸). 정상 켜짐 때도 적재 시간 T 만큼 시작이 늦어진다 | 검수 R-2 · R-7 · `assembly.py:283-286`(`await parts.load_soft()` 뒤 yield) | 코드 고침 필수 아님. 절차서 ⑦ 에 「재시작 → `health` 200 까지 시간」 을 재고, stg env 에 `GOLD_LOAD_TIMEOUT_SECONDS` 를 SE2 적재 시간 × 2~3(예 20 ~ 30초)로 두는 것을 추천. 근본 대안(다음 판) = 적재를 yield 뒤 백그라운드로(가드가 이미 「시작 적재 전」 503 을 내므로 관찰 동작 같음) |
| C-2 | **Low-Med** | `assembly.py:80` · `:179-181` · `:193-218` | 한도를 넘긴 뒤에도 데몬 스레드의 적재는 계속 돌고, 끝나면 `GoldState` 에 색인을 세우고 **`gold repository=db target=… gold_hash=…` 로그를 찍는다** — 가드는 닫힌 채(503). 절차서 ⑦ · SE2 가 이 로그 줄을 켜짐 신호로 쓰므로 `gold off reason=적재 시간 초과` 뒤에 「켜진 것 같은」 줄이 따라 나와 사람이 잘못 읽을 수 있다. 그 사이 색인 메모리 · CPU(GIL)를 쓰고, 끝내 안 끝나면 DB 연결 하나를 프로세스 수명 동안 쥔다 | 코드 경로(`load_state` 는 스레드 안 · `settle` 은 `fut.done()` 이면 버림 — 결과만 버리고 부수효과는 남음) | 절차서에 「켜짐 판정 = `gold/health` 200 · 로그는 `gold off` 줄이 없을 때만」 한 줄. 코드로 고치면: 한도 넘김 때 플래그를 세워 스레드 쪽 `load_state` 성공 로그를 `gold late load discarded` 로 바꾸거나 `state._repo` 를 비움 |
| C-3 | Low | `assembly.py:180` | 적재 안에서 난 `TimeoutError`(예: 드라이버 접속 시간 초과 · 스레드에서 `fut` 로 넘어옴)도 `except TimeoutError` 에 걸려 이유가 「적재 시간 초과(60s)」 로 찍힌다 — 실제는 F1 접속 실패. 꺼지는 결과는 같다 | `_in_daemon_thread` 가 예외를 그대로 `set_exception` | 한도 초과는 `wait_for` 자신의 초과만 — 스레드 예외를 `RuntimeError` 꼴로 감싸 넘기거나 경과 시간으로 가름 |
| C-4 | Low | `assembly.py:207-211` · `:186` | 스레드에서 `BaseException`(예: `asyncio.CancelledError` · `SystemExit`)이 나면 그대로 `fut` 에 실려 `except Exception` 을 빠져나가 **lifespan 시작 실패**(= app.main 안 뜸)가 된다. 지금 적재 코드에서 날 길은 보이지 않아 실제 위험은 낮다 | 「무엇이 나든」(§11-2) | `target()` 에서 `Exception` 이 아닌 `BaseException` 은 `RuntimeError(type name)` 로 바꿔 넘김 |
| C-5 | Low (정보) | `assembly.py:228-243` · `gold_main.py` | gold REST 가 하위 앱이 되면서 **gold 의 `openapi.json` 꼴이 바뀌었다** — `paths` 가 상대(`/resolve`)이고 `servers: [{"url": "/procedure-hub/gold"}]` 가 붙음(전에는 절대 경로 · servers 없음). URL 은 같고 Swagger 는 동작(확인). gold openapi.json 의 `paths` 를 직접 읽는 소비자가 있으면 어긋남 | 실행 확인(위 9) | SPEC-001 되적기 때 한 줄(「gold openapi = 하위 앱 · servers 접두」) · 앱 쪽이 openapi 를 안 읽으면 처분 없음 |
| C-6 | Low (정보) | `app_factory.py:21` | `app.main` import 가 이제 gold 조립 모듈(`mcp` SDK · gold 라우터)을 끌어온다 — import 자체가 실패하면(패키지 누락) 꺼짐이 아니라 app.main 다운. `mcp` 는 `pyproject` · `uv.lock` 의존이고 이미지 빌드 · 전체 시험이 통과해 실제 위험 없음. import 시간 +0.2s | 실행 확인(위 4) | 처분 없음(CI 가 잡는다) |

## 볼 것별 결과

### 1. `app.main` 기동 — gold 실패가 허브를 못 죽이나

| 길 | 결과 | 근거 |
|---|---|---|
| 설정 생성 실패(숫자 칸에 글자 등) | 꺼짐 · 이유 = 종류 이름(`ValidationError`) · 기본 경로에 503 앱 | `assembly.py:258-266` · `test_R6_settings_error_gold_off` |
| 조립 실패(MCP · FastAPI 하위 앱 · wire) | 같은 `except Exception` — 꺼짐 | `assembly.py:260-266` |
| 판 모름 · CSV env 없음 | `GoldLoadError` → 꺼짐(문구) | `test_ST4_*` |
| F1 ~ F7 | `GoldLoadError` → 꺼짐 · 503 본문은 `public_reason`(대상 꼬리 자름) · 로그는 전문(비밀번호 · 사용자 0) | `assembly.py:183-185` · `test_ST1` · `test_ST3_*` · `test_ST7_F1_target_not_in_response` |
| 그 밖의 예외 | 종류 이름만 · 로그에도 종류 이름만 | `assembly.py:186-188` · `test_ST7_other_exception_type_name_only` |
| 멈춤(비동기 · 동기 둘 다) | 데몬 스레드 + `wait_for` → 한도 뒤 꺼짐 · 프로세스 종료를 붙잡지 않음 · 닫힌 루프에 `call_soon_threadsafe` 는 `RuntimeError` 를 삼킴 | `assembly.py:193-218` · `test_R2_*`(async · sync-block) — 단 C-1 · C-2 |
| `BaseException` | 빠져나감 → C-4(Low) | — |
| MCP 세션 관리자 | 조립 실패 때 `mcp=None` → `nullcontext` · 서버는 한 번만 `run()` | `assembly.py:162-164` |
| 기존 lifespan 실패(DB 확인) | 그대로 시작 실패 — 기존 동작 불변(gold 는 `async with base(app)` 안) | `assembly.py:283` |
| 자원 | 성공 · 실패 때 엔진은 `read_db_inputs` 의 `finally: dispose`(스레드 루프 안). 멈춘 채 남는 경우만 연결 하나(C-2) | `db_inputs.py:100-120` |
| 늦게 끝난 적재와 가드의 경합 | 가드는 `wait_for` 가 한도 안에 끝났을 때만 `open()`(메인 루프) — 늦은 결과는 `fut.done()` 이라 버림. 요청이 닫힌 가드를 넘는 길 0 · 판정은 시작 때 한 번 | `assembly.py:189-190` · `:201-203` |

### 2. 기존 동작 불변

- `test_public_api_contract.py` 무수정 통과 · `app.main` OpenAPI JSON sha256 = `fdc155b` 와 동일 · `/procedure-hub/health` · `/health/config` 열쇠 불변(`test_ST5_hub_health_keys_unchanged`).
- `app/core/lifespan.py` · `app/router/*` · `alembic/` diff 0. `app_factory.py` 는 gold 세 줄 + `create_app(*, gold_settings=None)` 키워드 인자(호출자는 `app/main.py:8` 하나 · 인자 없이 부름).
- 라우트 순서: 기존 47 라우트 뒤에 Mount 2(`/procedure-hub/gold` · `/procedure-hub/gold-mcp`) — 기존 라우트를 가리지 않음(`test_ST5_gold_outside_openapi_and_after_existing_routes` + 직접 확인).
- 기존 라우터 wiring: 운영 코드는 `create_app()` 한 번 = 기존과 같다. 시험의 재wire 는 `tests/test_gold_app_main.py:39-46` autouse fixture 안(시험 전용) — 운영 영향 0. 전체 pytest(855)에서 glossary 등 전역 앱 override 시험이 순서 상관없이 통과.
- `gold_main` 동작: `load_strict` = 예외 그대로 시작 실패(`test_ST4_gold_main_still_fails_to_start`) · 경로 · 문서 화면 같음 · 기존 gold 시험 전부 통과 · `test_entrypoint_imports_no_db` 통과. 바뀐 것은 문서 JSON 꼴(C-5)과 `Server-Timing` 이 미들웨어 → 순수 ASGI 래퍼(응답 시작까지 · 본문 불변).
- `test_app_main_untouched` 지움(SPEC-003 §11-1 E7 · `tests/test_gold_rest.py`) — 남은 import 사용은 ruff 통과로 확인.

### 3. CD verify 를 깨는 길

- SQLite 판 전체 pytest: 855 passed · 53 skipped · 실패 0. 새 시험(`test_gold_app_main.py` 20 + ST8 3)은 데이터 env 없이 합성 fixture · 임시 SQLite 파일로만 돈다. `test_ST7_F1_target_not_in_response` 는 `127.0.0.1:1` 접속 거절을 쓰므로 CI 러너에서도 같은 F1(포트 1 LISTEN 없음).
- `test_ST8_*` 는 `GoldSettings.model_config["env_file"]` 을 monkeypatch 로 끄고 되돌림 — 로컬 `.env.gold` 유무와 무관.
- ruff 통과 · `alembic` 변경 0(위). Docker 빌드: `.dockerignore` 무수정으로 적재기 들어감 · 데이터 안 들어감(확인).

### 4. 503 본문 · MCP 허용 호스트

- R-1: 503 본문 = `unavailable: gold 꺼짐 — <F 코드 + 짧은 사유>` · `public_reason` 이 `· <방언> host=…` 꼬리를 자르고, 꼴이 바뀌어 `://` · `host=` 가 남으면 첫 낱말만(`assembly.py:86-91`). 다른 `GoldLoadError` 문구(파일 이름 · 칸 이름 · 해시 · 판 값)에 접속 값 0(grep 확인). REST · MCP · gold `health` 같은 본문(`_assert_off`).
- MCP: `enable_dns_rebinding_protection=True` 고정 · 기본 = 로컬 셋 · 설정값은 **더하기만**(`assembly.py:60-66`) · 목록 밖 Host 421 · 목록 밖 Origin 403(`test_mcp_allowed_hosts` 두 진입점). 가드(503)가 Host 검사보다 앞이라 꺼짐 때는 Host 무관 503.

### 5. `data/medallion/`

- 원천과 바이트 같음 100/100(위 8) · 결합 해시 · 행 수 = §11-0(위 6 · 7) · 크기 13MB.
- 비밀 0: 접속 문자열 · 내부 호스트(`docs/guides/deployment.md` 의 DB · 레지스트리 · Gateway 호스트) · 개인 경로 grep — 걸린 2 건은 공개 기사 URL(`medicaltimes.com/Users/News/…` · `source_ref.csv`) · 1 건은 `secretion`(문헌 본문) — 둘 다 오탐. README 에 개인 경로 · 레포 주소 · 접속 값 0.
- CD 트리거(`backend/**` · `.dockerignore` · 워크플로) 밖 · build context 밖. 이번 PR 은 `backend/` 도 바꾸므로 CD 는 돈다(정상).

## stg 배포를 막을 것

**없음.**

배포 전 · 절차서에 넣기를 권하는 것(막지는 않음):

1. (C-1) stg env 의 `GOLD_LOAD_TIMEOUT_SECONDS` 를 SE2 실측 적재 시간 기준으로 정함(기본 60초면 멈춤 + 느린 시작에서 CD Gateway 확인 창 약 100초에 가까움) · ⑦ 에서 재시작 → `health` 200 시간 기록.
2. (C-2) 켜짐 판정은 `GET …/gold/health` 200 · `gold off reason=` 줄이 있으면 뒤따르는 `gold repository=db … gold_hash=` 줄은 켜짐이 아니다.
3. (_RESUME 11-18 행 49) stg env 에 `GOLD_MCP_ALLOWED_HOSTS=<Gateway 공개 호스트>` — 없으면 stg MCP 421(REST 는 됨).
