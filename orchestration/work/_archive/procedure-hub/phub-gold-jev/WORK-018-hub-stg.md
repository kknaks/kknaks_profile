---
type: work
id: WORK-018
title: "허브 stg 판 구현 계획 — 레포 데이터 폴더 반입 · gold 를 app.main 에 붙임(꺼진 채 기동) · Dockerfile 적재기 한 줄 · 적재기 기본 경로 · 시험 ST1 ~ ST9 · CI 꼴 · 로컬 실물 SE1 ~ SE4"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-18
updated_at: 2026-11-18
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md (0.2.0 — §11-0 ~ §11-9) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.8.1 — §4-0 오류 표 · §4-8 health · 도구 계약은 안 바뀐다)"
    - "orchestration/work/phub-gold-jev/SPEC-007-image-data.md (적재기 V13 · GOLD_IMAGE_DIR)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 — 「stg gold = app.main 에 붙임」 · 「stg 시드 = 일회성 적재」 · 「배포로 닫는다」 · 「승인 없이 이어서」)"
    - "orchestration/work/phub-gold-jev/spec-003-stg-brief.md (이 문서의 발주서)"
  related:
    - "orchestration/work/phub-gold-jev/research-stg-seed.md (조사)"
    - "orchestration/work/phub-gold-jev/WORK-010-hub-db.md · WORK-015-data-v07.md (앞 허브 DB WORK — 적재 · 실물 확인 꼴)"
---

# WORK-018 — 허브 stg 판 구현 계획

> 경로 접두어: `W` = 이 폴더 · `P` = 프로필 코디 워크트리 루트 · `H` = `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD `fdc155b` · **이 위에 이어서 짓는다**) · `B` = `$H/backend` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터 · 지금 판) · `LG` = `$P/orchestration/work/phub-recommend/bronze/phub-ledger`(원장).
> **계약은 SPEC-003 0.2.0 §11 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작을 만들지 않는다 — 어긋나는 것을 만나면 맞춰 고치지 말고 보고한다(§9).
> **안 바뀌는 것**: 도구 9 계약 · 오류 3 · gold 15표 · silver 59표 · 스키마(alembic revision 0 개 더함) · `gold_hash` · `aux_hash` · `app.main` 의 기존 라우터 · 공개 계약 · `/procedure-hub/health`. 적재 · 데이터 값을 고치지 않는다.
> 줄 번호는 `$B` `fdc155b` 에서 이 워커가 읽은 것이다(읽기만).

## 0. 요약

- 만드는 것 셋: ① 레포 루트 **`data/medallion/`**(silver 59 · gold 16 · 원장 확인 1 · 원장 24 · README) ② **gold 를 `app.main` 에 붙임** — 같은 조립 코드로 `gold_main` · `app.main` 두 진입점 · `app.main` 에서는 적재 실패 = **gold 만 꺼짐(503)** ③ **Dockerfile 적재기 한 줄 · 적재기 기본 경로**.
- WP 다섯 · 순서대로(한 워커 · 직렬): **WP-1** 데이터 폴더 반입 → **WP-2** 조립 나눔 · `app.main` 마운트 · 꺼짐 기동 → **WP-3** Dockerfile · 적재기 기본 경로 → **WP-4** 시험(ST1 ~ ST9 · CI 꼴 한 번) → **WP-5** 로컬 실물(SE1 ~ SE4) · 마감.
- **시험 규칙**: WP 마다 **그 WP 의 「돌릴 파일」 만** · 전체 pytest(`uv run pytest --ignore=tests/integration`) 금지. 단 WP-4 끝에 **CD verify 꼴을 한 번 흉내**(§6-2 — 임시 PostgreSQL DB 에 `alembic upgrade head` + `alembic check` · `ruff check .` · SQLite env 로 이번에 닿는 시험 파일 묶음).
- **포트 · 데이터**: 워커가 띄웠다 내리는 것은 **18107 하나**. 18105(허브 DB 판 0.8.1) · 18108(시험 앱용 0.7.2) · 18432(로컬 PostgreSQL — 적재된 DB) 의 **데이터 · 프로세스를 건드리지 마라.** 빈 DB 시험은 18432 인스턴스 안의 **임시 DB 이름**으로 만들고 끝나면 지운다. 18220 · 18222 · 18106 은 보지도 마라.
- **커밋 금지**(코디). 비밀값 · 접속 값 · 내부 호스트 주소를 레포 · 보고에 쓰지 마라.

## 1. 지금 코드(`$B` · `fdc155b` · 읽기만)

| 파일 | 지금 | 이번에 |
|---|---|---|
| `app/main.py`(9줄) | `app = create_app()` | 그대로(조립은 `app_factory`) |
| `app/core/app_factory.py`(66) | `create_app()` — `FastAPIBuilder` 로 라우터 7 · 미들웨어(요청 로그 · CORS) · `lifespan=lifespan`(`:38`) | WP-2 — gold 마운트 둘 · lifespan 을 「기존 + gold」 로 감쌈 |
| `app/core/lifespan.py`(24) | `configure_logging` → `db_provider.initialize` → `verify_connection(retries=3)` → yield → close | WP-2 — **기존 순서 · 동작 불변.** gold 단계는 그 뒤에 더한다(감싸는 자리는 `app_factory` 또는 새 함수 — 기존 함수 본문은 안 바꾼다 추천) |
| `app/gold_main.py`(95) | `load_state`(`:31-45` — 모르는 값 · 적재 실패 = 예외) · `create_gold_app`(`:48-92` — REST 라우터를 `prefix` 로 `add_routers` · `Server-Timing` 미들웨어 · MCP `streamable_http_app` 한 번 · `app.mount(GOLD_MCP_MOUNT_PATH, …)`(`:89`) · lifespan 안에서 `session_manager.run()`) | WP-2 — 조립을 공용 함수로 옮기고 `gold_main` 은 그것을 부름(동작 같음) |
| `app/modules/gold/service.py` | `GoldState.load()` · `load_from()` · `loaded`(`:31-54`) | 꺼짐 상태 · 이유를 들 자리 — `GoldState` 에 더할지 조립 쪽에 둘지는 구현 때(§9 B-2) |
| `app/modules/gold/errors.py` | `GoldLoadError` · 도메인 오류 3(422 · 404 · 400 — `{"detail": "<코드>: <사유>"}`) | WP-2 — `unavailable` · 503 꼴(SPEC-003 §11-3) |
| `app/modules/gold/db_inputs.py` | F1 ~ F7 = `GoldLoadError`(접속 값 · 값 본문 0) | **안 고친다** — 문구를 꺼짐 이유로 그대로 쓴다 |
| `app/modules/gold/config.py` | `GoldSettings` — 경로 기본값 없음(머리말) · `GOLD_REPOSITORY` 기본 `csv` | **안 고친다**(SPEC-003 §11-6 I-7) |
| `app/modules/gold/medallion_load.py`(420) | `read_bundle` 첫 줄 `_need(GOLD_CSV_DIR, GOLD_SILVER_DIR, GOLD_LEDGER_CHECK_PATH)`(`:106`) · `summary_lines`(`:260`) | WP-3 — 기본 경로를 채우는 자리(스크립트 또는 여기 — §9 B-3) · 요약 첫 줄에 경로 출처 |
| `scripts/load_medallion.py`(35) | `GoldSettings()` → `run` | WP-3 — 기본 경로 |
| `Dockerfile`(27) | runtime 단계 COPY 스크립트 3(`:21-22`) | WP-3 — 한 줄 |
| `.dockerignore`(루트 · 13) | `**` 뒤 `!backend/` …(`:2-12`) | 안 고침(빌드로 확인 — SE3) |
| `tests/test_gold_rest.py` | `test_entrypoint_imports_no_db`(`:74-78`) · `test_app_main_untouched`(`:81-87`) | WP-4 — 앞 것 그대로 · **뒤 것 지움**(SPEC-003 §11-1 E7) |
| `tests/test_public_api_contract.py` | `app.openapi()` 의 `/procedure-hub/` 경로 전부 대조 · 태그 6(`:229-260`) | **안 고친다** — 고치지 않은 채 통과해야 한다(ST5) |
| `backend/README.md` | gold 절 「데이터는 저장소에 넣지 않고 경로를 env 로」(`:91`) · 적재기 명령(`:135-137`) | WP-1 · WP-3 — 문장 고침 · `app.main` 에서의 gold · 기본 경로 |
| `assets/procedure-images/README.md` | 대조 표 · 끝줄 「Docker 이미지에 실리지 않는다」 | WP-1 — 대조 표에 데이터 폴더 한 줄 |

grep(이 워커): `app.main` 의 라우트 가운데 `/procedure-hub/gold` 로 시작하는 것 0 · `tests/` 에서 `app.main` 과 gold 를 같이 쓰는 파일 = `test_gold_rest.py` 하나 · `.github/scripts/*.mjs` 에 Dockerfile 을 보는 검사 0 · `$B/envs/` 에 `.env.gold` 없음(`.env.example` 뿐).

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| 순서 | WP-1 → WP-5 직렬 · 한 워커 |
| 보고 | WP 마다 바꾼 파일 · 돌린 시험 파일 · 통과 · skip · 지운 시험 수 · 확인 결과(수 · 해시) |
| 시험 env | 시험은 설정을 **주입**한다(`GoldSettings(...)` · DI override) — 프로세스 env · `envs/.env.gold` 에 기대지 않는다 |
| 금지 | 전체 pytest · `alembic downgrade`(어떤 DB 에서도) · 18105 · 18108 · 18432 데이터 · 프로세스 · 커밋 · push |
| 이름 | 새 모듈 · 함수 이름은 구현 때 정한다(§9 B-1) — 이 문서의 이름은 자리 설명용 |

## 3. WP-1 — 데이터 폴더 반입

**SPEC**: §11-5 R-D1 ~ R-D7.

| 복사 원천 | 복사 자리(`$H` 기준) | 개수 |
|---|---|---:|
| `$SM/silver/*.csv` | `data/medallion/silver/` | 59 |
| `$SM/gold/g_*.csv` + `$SM/gold/questions.csv` | `data/medallion/gold/` | 15 + 1 = 16 |
| `$SM/notes/ledger-check-list.csv` | `data/medallion/notes/ledger-check-list.csv` | 1 |
| `$LG/*`(JSON 21 + `README.md` · `CHANGELOG.md` · `HASHES.txt`) | `data/medallion/bronze/phub-ledger/` | 24 |
| (새로 씀) | `data/medallion/README.md` | 1 |

- **`$SM/gold/` 의 `.py` · `.md`(gold-build · gold-check · silver-image · silver-supplement · README · semantic-map · gold-final-notes)는 옮기지 않는다**(R-D2 · R-D4). `$SM/notes/` 의 다른 파일 · `drafts/` · `archive/` 도 안 옮긴다.
- 바이트 그대로 복사(`cp -p` 꼴) — 줄바꿈 · BOM 을 바꾸는 도구를 쓰지 마라.
- **sha 대조**: 원천 · 복사본 파일마다 sha256 같음(전 파일 · 100 줄 목록을 보고에 — 59 + 16 + 1 + 24) · 이 워커가 `$SM` 으로 다시 센 값 — 폴더 gold 16 의 결합 해시 = `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c` · 보조 6(`source_ref` · `concern` · `adverse` · `condition` · `concern_site` · `ledger-check-list`)의 결합 해시 = `93ec89fdd7d66781cdf18025c4698cc31a543fe252ebb1f16948fc0876ae0eeb` · silver 행 67,853 · gold 행 62,244. 원장은 `HASHES.txt` 와 대조(그 파일의 꼴대로).
- `.gitignore` 확인: `git check-ignore -v data/medallion/silver/source_ref.csv data/medallion/bronze/phub-ledger/taxonomy.json` → 걸리는 규칙 0 · `git status --short data/` 에 새 파일이 보인다.
- `README.md`(R-D5): 판 이름 · 두 해시 · 폴더별 파일 수 · 표 76 · 행 130,446 · 「만든 곳 = 레포 밖 메달리온 작업 공간(gold-build · silver-check 등)」 · 적재 명령 꼴(WP-3 의 기본 경로 · 자리표시) · 「손으로 고치지 않는다」 · 그림은 `assets/procedure-images/`. **개인 경로 · 개인 레포 주소 · 접속 값 금지.**
- 문서 두 줄(R-D7): `backend/README.md:91` 문장 · `assets/procedure-images/README.md` 대조 표 한 줄.

**확인**: 위 sha 대조 · 개수 · `git check-ignore` · 공개 금지 grep(§7 3).

## 4. WP-2 — 조립 나눔 · `app.main` 마운트 · 꺼짐 기동

**SPEC**: §11-1 E1 ~ E7 · §11-2 · §11-3.

추천 꼴(구현 워커가 다르게 할 수 있다 — 단 SPEC §11 의 관찰 가능한 동작은 그대로):

| # | 하는 것 |
|---|---|
| 1 | **gold 조립을 공용 함수 하나로** 옮긴다(자리 예: `app/modules/gold/` 아래 새 모듈 · `app.core.tx` · `app.core.db` 를 import 하지 않는 자리 — `test_entrypoint_imports_no_db` 를 지킨다). 돌려주는 것: ⓐ gold REST 하위 앱(라우트는 하위 앱 기준 상대 경로 · 도구 9 + `health` · `Server-Timing` 미들웨어 · `EXCEPTION_HANDLERS` · 문서 화면 `/api-docs` · `/redoc` · `/openapi.json`) ⓑ MCP 앱(`streamable_http_app(stateless_http=True, json_response=True)` 한 번) ⓒ 적재 함수(지금 `load_state`) ⓓ MCP 세션 관리자 ⓔ 꺼짐 가드 |
| 2 | **꺼짐 가드** — ⓐ ⓑ 앞에 서서 gold 가 꺼져 있으면 `503` · `{"detail": "unavailable: gold 꺼짐 — <이유>"}` 를 낸다(REST · MCP 같은 본문). 처음 상태 = 꺼짐(이유 `시작 적재 전`) · 적재가 성공하면 켜짐. 판정은 시작 때 한 번 |
| 3 | `gold_main`: 루트 앱에 ⓐ 를 `GOLD_API_PREFIX` 로 · ⓑ 를 `GOLD_MCP_MOUNT_PATH` 로 붙이고, lifespan 에서 ⓒ 를 부른다 — **실패는 지금처럼 예외(시작 실패)**. 경로 · 응답 · 문서 화면 자리가 지금과 같아야 한다(기존 gold 시험이 그대로 통과 — ST9) |
| 4 | `app.main`(`app_factory.create_app`): 기존 조립 뒤에 ⓐ · ⓑ 를 같은 경로로 **마운트**(OpenAPI 에 안 들어간다 — E3). lifespan = **기존 lifespan 그대로 들어간 뒤** ⓒ 를 `try` 로 부른다 → 성공이면 켜짐 · `GoldLoadError` 면 그 문구 · 그 밖의 예외면 **종류 이름만**을 이유로 꺼짐 + 경고 로그 한 줄 `gold off reason=<이유>` → ⓓ `session_manager.run()` 에 들어가 yield(꺼져도 세션 관리자는 돌린다 — 가드가 막으므로 해 없음) |
| 5 | `GoldSettings` 는 `app.main` 조립 때 한 번 만든다(지금 `gold_main.py:95` 와 같은 꼴) · 시험이 주입할 수 있게 조립 함수가 설정을 인자로 받는다 |
| 6 | 오류 꼴: `unavailable` 은 도메인 예외 클래스로 둘지 가드가 바로 응답할지 구현 때(§9 B-2) — 본문 · 상태는 SPEC §11-3 그대로 |

- **주의 — DI wiring 은 모듈 단위다**(`GoldContainer.wiring_config = ["app.router.gold"]` · `FastAPIBuilder.setup_container` 가 `wire()`). 한 프로세스에서 `gold_main` 조립과 `app.main` 조립이 둘 다 일어나면 `app.router.gold` 는 **마지막에 wire 한 컨테이너**를 본다. 서버(한 프로세스 · 한 진입점)는 문제없다. 시험에서 두 앱을 한 프로세스에 만들 때는 요청 전에 그 앱의 컨테이너로 다시 wire 하거나 시험을 나눈다 — 지금 `test_gold_rest.py` 도 앱을 여러 번 만든다(같은 꼴).
- `app.main` 의 `health_router`(`/procedure-hub/health`)와 gold `health`(`/procedure-hub/gold/health`)는 경로가 다르다 — 겹침 0. 마운트 뒤 `app.main` 라우트 표에 `/procedure-hub/gold*` 가 기존 라우트를 가리지 않는지 본다(라우트 순서 — 기존 라우터가 먼저).
- `app.main` 의 `health` · `health/config` 에 gold 를 넣지 않는다(E4).

**돌릴 파일(WP-2)**: `tests/test_gold_rest.py`(`test_app_main_untouched` 를 지운 뒤) · `tests/test_gold_mcp.py` · `tests/test_gold_contract.py` · `tests/test_gold_load.py` · `tests/test_gold_tools_synthetic.py` · `tests/test_medallion_repo.py` · `tests/test_public_api_contract.py`(합성 · SQLite 만 — `test_gold_real.py` · `test_gold_holes.py` · `test_gold_v07_*.py` 같은 실물 데이터 시험은 WP-2 에서 돌리지 않는다).

## 5. WP-3 — Dockerfile 적재기 한 줄 · 적재기 기본 경로

**SPEC**: §11-6 I-1 ~ I-8.

| # | 하는 것 |
|---|---|
| 1 | `backend/Dockerfile` runtime 단계(`:21-22` 옆)에 `COPY backend/scripts/load_medallion.py scripts/load_medallion.py` 한 줄. 다른 줄 · CMD 불변 · 데이터 COPY 0 |
| 2 | `.dockerignore` 는 고치지 않는다 — WP-5 SE3 빌드에서 이미지 안에 파일이 있는지 본다. 없으면 `!backend/scripts/load_medallion.py` 한 줄을 더하고 보고 |
| 3 | 적재기 기본 경로: 경로 env 셋(`GOLD_CSV_DIR` · `GOLD_SILVER_DIR` · `GOLD_LEDGER_CHECK_PATH`)이 **비었을 때만** `<backend 의 부모>/data/medallion/{gold, silver, notes/ledger-check-list.csv}`. env 가 앞선다. `GOLD_IMAGE_DIR` · `GOLD_EXPECTED_HASH` · `DATABASE_URL` 은 기본값 없음 |
| 4 | 기본값은 **적재기에만** — `GoldSettings` · 서버 CSV 판은 그대로(빈 값 = 시작 실패 / `app.main` 에서는 꺼짐) |
| 5 | 요약 첫 줄에 쓴 경로 셋 · 출처(`env` · `default`)를 찍는다(값 본문 · 접속 값 0) |
| 6 | 스크립트 머리말 · `backend/README.md` 적재기 절에 기본 경로 · 일회성 컨테이너 꼴(자리표시 · SPEC §11-6)을 적는다 |

**돌릴 파일(WP-3)**: `tests/test_medallion_load.py` · `tests/test_medallion_image.py` + WP-4 의 ST8 시험.

## 6. WP-4 — 시험

**SPEC**: §11-8 ST1 ~ ST9 · CI.

### 6-1. 더하거나 고칠 시험

| ST | 무엇 | 꼴 |
|---|---|---|
| ST1 | 빈 표 기동 | 임시 SQLite **파일** DB 에 새 표만 만든다(`Base.metadata` 의 medallion 표 또는 fixture 헬퍼) · 행 0 · `GOLD_REPOSITORY=db` · `DATABASE_URL` = 그 파일 → `app.main` 조립을 **lifespan 까지** 돌림(`LifespanManager` 꼴 또는 `TestClient` 컨텍스트) → `/procedure-hub/health` 200 · 열쇠 불변 · `/procedure-hub/gold/health` 503 · `detail` 이 `unavailable: ` 로 시작 · `F2` · 도구 하나 · MCP `POST <mount>/mcp` 도 503. ⚠ `app.main` 의 기존 lifespan 은 허브 공용 `DATABASE_URL` 로 DB 확인을 한다 — 시험에서는 그 값(공용 설정)과 gold 설정을 각각 주입한다(메모리 SQLite 는 엔진마다 다른 DB 라 gold 쪽은 **파일** DB) |
| ST2 | 적재 뒤 기동 | 같은 파일 DB 에 fixture 를 적재기로 싣고 → gold 켜짐 · `gold/health` 200 · `gold_hash` = fixture 값 · 도구 요청 몇 개의 JSON = 같은 설정의 `gold_main` 응답(`build.loaded_at` · `load_ms` 제외) · MCP 도구 호출 1 |
| ST3 | 해시 불일치 | `GOLD_EXPECTED_HASH` 다른 값 → `F6` · 빌드 기록 `sha256` 한 줄을 바꿈 → `F4` — 둘 다 꺼짐 · `app.main` `health` 200 |
| ST4 | 판 고르기 | `GOLD_REPOSITORY` 빈 값 · CSV env 없음 → 꺼짐(「필수 env 없음」) · `xyz` → 꺼짐 · `gold_main` 쪽 같은 두 경우는 지금처럼 시작 실패(기존 시험) |
| ST5 | 기존 계약 | `tests/test_public_api_contract.py` **무수정** 통과 · `/procedure-hub/health` · `/health/config` 열쇠 불변 · `test_app_main_untouched` 지움 |
| ST6 | lifespan 안 돈 꼴 | `ASGITransport(app=…)` 로 lifespan 없이 gold 경로 → 503 `시작 적재 전` |
| ST7 | 그 밖의 예외 | 적재 함수를 다른 예외로 바꿔 끼움 → 꺼짐 · `detail` = 종류 이름만 · `detail` · 로그에 `://` 0 |
| ST8 | 적재기 기본 경로 | 루트를 임시 폴더로 돌리고(monkeypatch) 그 밑 `data/medallion/` 에 fixture 를 놓음 → env 없이 `--dry-run` exit 0 · 요약 출처 `default` · env 를 주면 `env` 가 앞선다 |
| ST9 | `gold_main` 불변 | 기존 gold 시험 전부 · `test_entrypoint_imports_no_db` |

- 새 시험은 새 파일 하나(이름 예 `tests/test_gold_app_main.py`)에 모은다 · ST8 은 `test_medallion_load.py` 에 더해도 된다.
- fixture 는 지금 것(`tests/medallion_fixture.py` · `tests/gold_fixture.py`) — 회사 데이터 본문 0.

### 6-2. CD verify 꼴 한 번(전체 pytest 아님)

CI 는 PostgreSQL 에 `alembic upgrade head` + `alembic check` → `ruff check .` → SQLite env 로 pytest(`.github/workflows/backend-test.yml:66-80`). 로컬에서 같은 꼴로 **한 번**:

```bash
# backend/ 에서
# ① 임시 DB(18432 인스턴스 안 · 이름 예 phub_ci_tmp_<날짜>) — 만들기 전 같은 이름 없는지 보고, 끝나면 지운다
DATABASE_URL=postgresql+asyncpg://<USER>:<PASSWORD>@127.0.0.1:18432/<임시 DB> uv run alembic upgrade head
DATABASE_URL=postgresql+asyncpg://<USER>:<PASSWORD>@127.0.0.1:18432/<임시 DB> uv run alembic check
# ② ruff
uv run ruff check .
# ③ SQLite env · gold 데이터 env 없음 — 이번에 닿는 파일 묶음만
env -u GOLD_REPOSITORY -u GOLD_CSV_DIR -u GOLD_SOURCE_REF_PATH -u GOLD_HIERARCHY_DIR -u GOLD_LEDGER_CHECK_PATH -u GOLD_EXPECTED_HASH \
  DATABASE_URL="sqlite+aiosqlite:///:memory:" \
  uv run pytest -q tests/test_public_api_contract.py tests/test_gold_rest.py tests/<새 시험 파일> \
  tests/test_medallion_load.py tests/test_medallion_repo.py tests/test_medallion_model.py tests/test_medallion_image.py tests/test_gold_mcp.py tests/test_gold_contract.py tests/test_gold_load.py tests/test_gold_tools_synthetic.py
```

- ① 은 **새 revision 이 0 개**(이번 판은 스키마를 안 바꾼다)라 `fdc155b` 와 같은 결과여야 한다 — 다르면 멈추고 보고.
- 접속 값은 env 로만 주고 명령 · 보고에 찍지 않는다(코디가 준 방법 · 이미 쓰던 방법).
- 임시 DB 는 WP-5 SE1 에서 다시 쓸 수 있다(그대로 두었다가 SE1 뒤 지움).

## 7. WP-5 — 로컬 실물 · 마감

**SPEC**: §11-8 SE1 ~ SE4.

| SE | 무엇 | 꼴 · 기대 |
|---|---|---|
| SE1 | 빈 DB → gold 꺼짐 | 18432 인스턴스의 **임시 DB**(§6-2 ①) · `app.main` 을 **18107** 에(띄우기 전 `lsof -nP -iTCP:18107 -sTCP:LISTEN` 빔 확인) · `DATABASE_URL`(공용 · gold 같은 값) · `GOLD_REPOSITORY=db` → 로그 `gold off reason=F2…` · `GET /procedure-hub/health` 200 · `GET /procedure-hub/gold/health` 503 · 본문 F2 → 18107 내림(자기 PID 만) · **임시 DB 지움** |
| SE2 | 적재된 DB → gold 켜짐 | `app.main` 을 18107 에 · `DATABASE_URL` = 18432 의 적재된 DB · `GOLD_REPOSITORY=db` · `GOLD_EXPECTED_HASH`=§11-0 값 → 로그 `gold repository=db … gold_hash=8accbb21…` · `gold/health` 200 · 같은 요청 묶음을 **18105** 와 18107 에 보내 견줌(`build.loaded_at` · `load_ms` 제외 · 머리는 견주지 않음) · 묶음 = WORK-016 §6 요청 묶음 또는 `health` · `resolve`(목록 꼴 · 쪽 끝까지) · `concern-candidates` 셋 · `facets` 하나 · `evidence` 하나 · MCP `tools/list` 이름 9 · MCP `resolve` 하나 → 차이 0 · 18107 프로세스 RSS 를 재어 적음(O-S4) → 18107 내림. **`alembic` 을 이 DB 에 돌리지 않는다** · 적재기도 안 돌린다 |
| SE3 | 이미지 | `$H` 루트에서 `docker build -f backend/Dockerfile --target runtime -t phub-stg-check:local .` → `docker run --rm --entrypoint ls phub-stg-check:local scripts` 에 `load_medallion.py` · `docker run --rm --entrypoint ls phub-stg-check:local /` 에 `data` 없음 → §11-6 꼴로 `-v $H/data/medallion:/data/medallion:ro -v $H/assets/procedure-images:/assets/procedure-images:ro -e GOLD_IMAGE_DIR=/assets/procedure-images -e GOLD_EXPECTED_HASH=<값>` · `--dry-run`(DATABASE_URL 주지 않음 — DB 접속 0) → exit 0 · `tables 76 · rows 130,446` · 두 해시 · `image_files 103 checked` · 경로 출처 `default` → 이미지 지움(`docker rmi`) |
| SE4 | 데이터 폴더 | WP-1 의 sha 대조 결과 · 레포 경로(기본 경로)로 로컬 `uv run python scripts/load_medallion.py --dry-run` → exit 0 · 두 해시 = §11-0 |

- 18105 · 18108 · 18432 의 적재된 DB 를 바꾸는 명령(적재 · alembic · 재시작)을 하지 마라. SE2 는 **읽기만**이다.
- SE3 의 빌드는 uv 기반 이미지를 받는다(네트워크) — 실패하면 보고하고 SE3 만 「확인 안 됨」 으로 둔다(코디 판단).

### 7-1. 코디 몫

- 허브 브랜치 커밋 · push · PR(→ `release/v1.2.0`) · 머지 · `stg` PR — 코디(_RESUME §2 11-18 「승인 없이 이어서」).
- stg 반입(SPEC-003 §11-7 ① ~ ⑨)은 **사용자가 VM 에서** · 코디는 절차서 전달 · ⑧ 대조 · 기록.
- SPEC-001 다음 판 되적기(O-S1 `unavailable` 503 · §8 진입점 줄).

## 8. 완료 조건 · 검증 명령

1. WP-1 ~ WP-5 보고(바꾼 파일 · 돌린 파일 · 통과 · skip · 지운 시험 1 · 수 · 해시 · RSS · 걸린 시간).
2. ST1 ~ ST9 가 시험 이름 또는 주석으로 찾아진다 · §6-2 CD verify 꼴 통과(`alembic check` · ruff · 묶음 pytest).
3. 공개 금지 grep — `$H` 에서 `git diff fdc155b --name-only` 로 바뀐 파일 + `data/medallion/README.md` 에 접속 문자열 꼴(`postgresql+asyncpg://` 뒤 `@` 가 든 것) · 내부 호스트 이름(`docs/guides/deployment.md` 에 적힌 DB · 레지스트리 · Gateway 호스트를 그대로 grep 패턴으로) · 개인 경로(`/Users/`) 0.
4. `test_public_api_contract.py` · `app/core/lifespan.py` 의 기존 본문 · `app/router/health.py` · `alembic/versions/` 가 `git diff fdc155b` 에 **없다**(lifespan 을 고쳤다면 기존 단계가 그대로인지 diff 로 보고).
5. SE1 ~ SE4 결과 · 18107 내려감(`lsof` 빔) · 임시 DB 지움 · 로컬 이미지 지움.
6. 커밋 0 · 18105 · 18108 · 18432 데이터 그대로.

## 9. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

### 9-1. A — SPEC 되적기 후보(코디)

| # | 무엇 |
|---|---|
| A-1 | SPEC-001 §4-0 오류 표에 `unavailable` · 503 넷째 줄 · §8 「진입점(O-7)」 을 닫힘으로 · §1-4 코드 자리에 공용 조립 모듈 — SPEC-003 §11-9 O-S1 |
| A-2 | SPEC-003 §0 ~ §10 의 수 74 · 129,527 → 76 · 130,446 를 본문에 되적을지(지금은 머리 안내 · §11-0 으로만) |

### 9-2. B — 구현 워커가 추측으로 메우지 않게 이 문서가 정한 값(코디가 바꿀 수 있다)

| # | 값 |
|---|---|
| B-1 | 새 모듈 · 함수 · 시험 파일 이름은 구현 때 — 단 공용 조립 자리는 `app.core.tx` · `app.core.db` 를 import 하지 않는 곳 |
| B-2 | 꺼짐 상태 · 이유를 `GoldState` 에 둘지 조립 쪽에 둘지 · `unavailable` 을 예외 클래스로 둘지 가드가 바로 응답할지 — 구현 때(관찰 동작은 SPEC §11-3) |
| B-3 | 적재기 기본 경로를 `scripts/load_medallion.py` 에서 채울지 `medallion_load` 에서 채울지 — 구현 때(서버 설정에는 넣지 않는다) |
| B-4 | `app.main` lifespan 감싸기는 기존 `app/core/lifespan.py` 본문을 바꾸지 않는 꼴을 먼저 고른다(새 함수가 기존 lifespan 에 들어간 뒤 gold 를 더함) |

### 9-3. C — 확인 안 된 것

| # | 무엇 | 언제 |
|---|---|---|
| C-1 | stg 시작 시간 · 메모리(SPEC-003 O-S4) | SE2 RSS · stg ⑦ |
| C-2 | `deploy.sh` 가 env 파일의 더한 키를 넘기나(O-S7) | stg ③ 의 꺼짐 이유 |
| C-3 | `.dockerignore` 손 없이 적재기가 이미지에 드나(I-2) | SE3 |

## 10. SPEC-003 0.2.0 절 ↔ WP 대응(미대응 0)

| SPEC | WP |
|---|---|
| §11-0 정해진 것 · 수 | WP-1 대조 · SE3 · SE4 |
| §11-1 E1 ~ E7 진입점 | WP-2 · ST2 · ST5 · ST9 |
| §11-2 기동 규칙 | WP-2 · ST1 · ST3 · ST4 · ST6 · ST7 · SE1 · SE2 |
| §11-3 꺼진 응답 | WP-2 · ST1 · ST6 · SE1 |
| §11-4 켜기 · 끄기 · 갱신 | 코디 · 사용자(stg) — 코드 몫 = 「시작 때 한 번 판정」(WP-2) |
| §11-5 데이터 폴더 R-D1 ~ R-D7 | WP-1 · SE4 |
| §11-6 I-1 ~ I-8 · 일회성 꼴 · 되돌리기 | WP-3 · ST8 · SE3 |
| §11-7 stg 반입 절차서 | 코디 · 사용자(§7-1) |
| §11-8 ST1 ~ ST9 · CI · SE1 ~ SE4 | WP-4 · WP-5 |
| §11-9 열린 것 | §9 |

## 변경 기록

### 0.1.0 (2026-11-18) — 처음 씀

- SPEC-003 0.2.0 §11 을 WP 다섯으로 나눴다 — 데이터 반입 · `app.main` 마운트(꺼짐 기동) · Dockerfile · 기본 경로 · 시험 · 로컬 실물.
- 이 워커가 `$SM` 으로 다시 센 값: gold 16 결합 해시 `8accbb21…f6228c` · 보조 6 결합 해시 `93ec89fd…6ae0eeb` · silver 59 파일 67,853행 · gold 15표 62,244행 · 원장 폴더 24 파일(JSON 21).
- 지금 코드에서 본 걸림: `test_app_main_untouched`(지움) · 공개 계약 시험(하위 앱 마운트로 무수정 통과) · DI wiring 이 모듈 단위(§4 주의) · 빈 메모리 SQLite 는 엔진마다 다른 DB(ST1 은 파일 DB).
