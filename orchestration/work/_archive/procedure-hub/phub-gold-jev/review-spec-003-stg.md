# 검수 — SPEC-003 0.2.0 §11 · WORK-018 0.1.0 (stg 판)

- 검수자: reviewer(read-only) · 2026-11-18
- 대상: `SPEC-003-hub-gold-db.md` 0.2.0 §11(656–874) · 변경 기록 · `WORK-018-hub-stg.md` 0.1.0
- 기준: `_RESUME.md` §2 11-18 행(49 · 50 · 53) · `research-stg-seed.md` · 허브 `fdc155b`(읽기만)
- 대조한 코드: `app/core/app_factory.py` · `app/core/lifespan.py` · `app/core/db.py:26-46` · `app/gold_main.py` · `app/modules/gold/{config,db_inputs,medallion_load}.py` · `scripts/load_medallion.py` · `Dockerfile` · `.dockerignore` · `alembic/env.py` · `tests/test_public_api_contract.py:229-260` · `tests/test_gold_rest.py:74-87` · `.github/workflows/{backend-test,csp-azure-deploy,frontend-check}.yml` · `docs/guides/deployment.md:250-261`
- 수 확인: `$SM/silver/*.csv` 59 · `$SM/gold/g_*.csv` 15 + `questions.csv` · `notes/ledger-check-list.csv` 1 · 원장 폴더 24(JSON 21) · `assets/procedure-images/images/**/*.svg` 103 — §11-5 · WORK §3 와 같다. 로컬 LISTEN = 18105 · 18106 · 18108 · 18210 · 18220 · 18222 · 18432(18107 비어 있음).

## 판정: **WARN** — 구조는 맞고 구현해도 된다. 단 기존 허브 · 공개 표면을 지키려면 아래 「구현 전 꼭 고칠 것」 4줄을 SPEC/WORK 에 먼저 넣는다

결정(S-4 · 시드 · S-1~S-7 · O-S1~O-S3 코디 답)은 본문에 빠짐없이 풀렸고, OpenAPI · 공개 계약 · 라우트 겹침 · 데이터 폴더 · Dockerfile · CI 트리거 판단은 코드로 확인해 맞다. 걸리는 것은 「gold 가 무엇이 나든 `app.main` 은 산다」 는 약속이 **예외만** 덮고 **멈춤(hang) · 메모리** 를 안 덮는 것, 그리고 꺼짐 이유 글이 **공개 경로로 내부 DB 호스트를 낸다**는 것.

## 결함 표

| # | 심각 | 자리 | 무엇 | 근거 | 고칠 꼴 |
|---|---|---|---|---|---|
| R-1 | **High** | SPEC §11-2 715 · §11-3 724 | 꺼짐 이유 = `GoldLoadError` 문구 그대로 → **F1 문구에 접속 대상(호스트 · 포트 · DB 이름)이 든다.** 그 글이 gold REST · MCP 503 본문으로 나가고, Gateway `/procedure-hub/*` 는 인증 없이 공개(O-S5)라 stg 내부 DB 호스트가 인터넷에 나간다. 「F1 ~ F7 문구는 접속 값을 싣지 않는다」 는 사실과 다르다(비밀번호 · 사용자만 빠짐) | `db_inputs.py` `read_db_inputs` — `F"F1 DB 접속 실패(...) · {target}"` · `F"F1 DB 읽기 실패(...) · {target}"` · `medallion_load.py:271-279` `describe_target` = `host= port= db=` | 503 본문 · gold `health` 본문에는 **F 코드 + 짧은 사유만**(`· {target}` 앞에서 자름 또는 F 코드 + 예외 종류) · 대상은 서버 로그에만. ST7 에 「`detail` 에 `host=` 0」 단언 더함 |
| R-2 | **High** | SPEC §11-2 699 「무엇이 나든 시작 실패하지 않는다」 | gold DB 적재에 **시간 한도가 없다.** 적재는 lifespan 안이라 끝나야 요청을 받는다 → 원격 PG(TLS)에서 읽기가 멈추면 `app.main` 이 영영 요청을 안 받는다 = 기존 허브 다운. 허브 공용 엔진에는 connect · command timeout 이 있는데 gold 엔진에는 없다 | `db_inputs.py:5` 「15초 제한 없음」 · `make_engine` = `NullPool` 만 · `core/db.py:33-41`(공용은 `timeout` · `command_timeout`) | `app.main` 쪽에서만 적재를 시간 한도로 감싼다(예: `asyncio.wait_for`) → 넘으면 **꺼짐**(이유 `적재 시간 초과(<n>s)`). 한도 값은 설정(기본값 하나 — CD health 창보다 짧게, R-7). `gold_main` 동작은 그대로. ST 하나 더(느린 적재 → 꺼짐 · 기존 `health` 200) |
| R-3 | **High** | SPEC §11-7 ⑦ 829 · O-S4 867 | **메모리** — 켜진 gold 는 색인을 `app.main` 프로세스가 든다. VM · 컨테이너 여유를 모른 채 ⑦ 재시작 → OOM 이면 `--restart unless-stopped` 로 다시 뜰 때마다 같은 적재 → **재시작 고리 = 기존 허브 다운.** O-S4 는 「재어 둔다 · 기준값 안 정함」 이라 멈출 곳이 없다 | `deployment.md:255-258`(`--restart unless-stopped`) · §11-2 「적재가 끝나야 요청을 받는다」 | ① 에 VM `free -m` · `docker stats --no-stream <컨테이너>` 기록 더함 · **⑦ 앞 멈출 곳**: SE2 RSS 증가분(켜짐 − 꺼짐) × 2 가 ① 의 가용 메모리보다 크면 코디에게 · ⑦ 확인 지점에 `docker stats` 한 번 · 고리에 들면 §11-4 「끄기」 명령을 그대로 적는다(R-8) |
| R-4 | **Med** | WORK §6-2 ③ 169 | 「CD verify 꼴」 묶음이 **`app.main` 을 import 하는 기존 시험 셋을 빼먹었다** — `test_glossary_router.py` · `test_glossary_template.py` · `test_corpus_import_publication.py`(모두 `from app.main import app`). 실제 CD verify 는 `pytest -q --ignore=tests/integration` 전체라, 이 판이 그 파일들을 깨면 stg PR 머지 뒤 CD 에서야 드러난다(배포 막힘) | `grep -l "from app.main" tests/` = 5 파일 · `backend-test.yml:73-78` | ③ 묶음에 셋 더함(전수 = `grep -l "app.main\|app_factory" tests/` 결과 전부). WP-4 끝 한 번은 CD 와 같은 `--ignore=tests/integration` 전체여도 된다(「전체는 마지막 한 번」) — 코디 판단 |
| R-5 | Med | SPEC §11-6 「되돌리기」 815 | 「옛 이미지로 돌아가지 않는다」 가 **③ 에서 새 컨테이너가 안 뜨는 경우**(시작 명령의 `alembic upgrade head` 실패 — 권한 · 잠금 등)를 덮지 않는다. 이때 기존 허브는 내려가 있고, 마이그레이션은 트랜잭션 안이라 revision 은 `b202610300001` 그대로 → `:stg-rollback` 이 **안전한 유일한 빠른 길**이다 | `Dockerfile:27`(`alembic upgrade head && exec uvicorn`) · `alembic/env.py:36,43` `begin_transaction()` · `csp-azure-deploy.yml:86-95`(rollback 태그) | 되돌리기 표에 한 줄: 「③ 컨테이너가 안 뜸 → `alembic current` 가 ① 값 그대로면 `:stg-rollback` 으로 컨테이너를 다시 만든다(사용자 · deploy 꼴) · 다르면 멈추고 코디」. ③ 멈출 곳에도 같은 말 |
| R-6 | Low | SPEC §11-2 · WORK §4 #5 | 「무엇이 나든」 의 범위가 lifespan 뿐 — `GoldSettings()` 생성 · gold 조립(MCP 앱 만들기)은 `create_app()` = **import 때** 돈다. env 값이 잘못(예: 숫자 칸에 글자)이면 `app.main` import 실패 = 허브 다운. 지금 stg 가 더하는 키는 `GOLD_REPOSITORY`(글자) 하나라 실제 위험은 낮다 | `config.py:45-52`(int 칸) · `gold_main.py:95` 꼴 | SPEC 에 한 줄: 설정 생성 실패도 꺼짐(조립 함수가 `GoldSettings` 생성을 try 로 감쌈) — 또는 「import 때 실패는 CI 가 잡고 stg 는 글자 키 하나라 받아들임」 으로 범위를 적는다 |
| R-7 | Low | SPEC §11-7 ③ · ⑦ | CD 의 Gateway 확인은 `--retry 6 --retry-delay 5 --max-time 10`(약 90초 창) · ssh `command_timeout 3m`. ⑦ 이후의 **모든 다음 stg 배포**는 시작 때 원격 gold 적재를 한다 → 적재 시간이 창에 가까우면 CD 가 실패로 찍힌다(허브는 늦게라도 뜸) | `csp-azure-deploy.yml:143-159` | ⑦ 확인 지점에 「재시작 → `health` 200 시간 < 60초」 · 넘으면 코디(R-2 한도와 같이 정함) |
| R-8 | Low | SPEC §11-4 83-84 행 · §11-7 | 「컨테이너를 새로 만든다(`deploy.sh` — 사용자)」 에 명령이 없다 — 급할 때 사용자가 그대로 칠 수 있게 | `deployment.md:382` 꼴(`./deploy.sh procedure-hub stg` — Bastion 경유) | 「끄기」 · R-5 줄에 자리표시 명령 한 줄 |
| R-9 | Low | SPEC §11-7 ⑨ 831 | ⑥ 출력 · ⑦ 로그에는 `target … host=<stg DB 호스트> port= db=` 줄이 찍힌다. ⑨ 「출력 그대로 → `_RESUME`」 이면 내부 호스트가 프로필 레포(공개)에 들어간다 | `medallion_load.py:348` `out("target " + …)` · `gold_main.py:42` | ⑨ 에 「`target` 줄 · 호스트는 `<…>` 로 가리고 남김」 |
| R-10 | Low | SPEC §11-6 128 · §11-7 ⑤ | `<IMG>` = `:stg-<sha>` — VM 에는 deploy 가 `:stg` 를 당겨 둔다. `:stg-<sha>` 는 레지스트리에서 다시 받아야 한다(로그인 상태 의존) | `deployment.md:255-261` · `csp-azure-deploy.yml:107-109` | ⑤ 에서 ③ 뒤 `docker inspect --format '{{.Image}}' <컨테이너>` 의 이미지 id 를 `<IMG>` 로 쓰면 「서빙과 같은 이미지」 가 보장된다(대안으로 적기) |
| R-11 | Low | SPEC 부록 B ⑧ 905 | `aux_hash` `6435fe41…` 가 §11-0 `93ec89fd…` 와 다르다 — 0.1.0 재셈인데 표 머리에 판 표시가 없다 | — | 부록 B 머리에 「0.1.0 판 재셈 · 지금 값은 §11-0」 |
| R-12 | Low | WORK §6-1 ST1 · ST2 | `app.main.app`(모듈 전역)으로 lifespan 을 두 번 돌리면 MCP `session_manager.run()` 이 「한 인스턴스 한 번」 이라 두 번째가 `RuntimeError` → lifespan 실패. 지금 기존 시험은 lifespan 없이(ASGITransport) 써서 괜찮다 | `mcp/server/streamable_http_manager.py` `run()` 「only be called once per instance」 | ST 마다 조립 함수를 새로 불러 앱을 만든다(전역 `app` 재사용 금지) — WORK §4 「주의」 옆 한 줄 |

## 볼 것별 결과

### 1. 기존 stg 허브를 죽일 길

| 길 | 판정 | 근거 |
|---|---|---|
| 접속 실패 · 표 없음 · 행 0 · 해시 · 판 · F1~F7 | 꺼짐으로 받음 — OK | `db_inputs.py` 전부 `GoldLoadError` · §11-2 표 |
| 그 밖의 예외 | 종류 이름만 · 꺼짐 — OK | §11-2 711 |
| **멈춤(hang)** | **안 덮임** → R-2 | gold 엔진 시간 한도 0 |
| **메모리(OOM)** | **멈출 곳 없음** → R-3 | O-S4 |
| import 때 실패(설정 · 조립) | 범위 밖 → R-6(낮음) | `create_app()` 은 import 때 |
| lifespan 순서 | OK — 기존(로깅 → DB 확인) 뒤 gold · DB 확인 실패 = 시작 실패 그대로(E4). B-4(기존 `lifespan.py` 본문 안 고침)도 맞다 | `lifespan.py:19-24` |
| ③ 시작 마이그레이션 실패 | 되돌리기 빈칸 → R-5 | `Dockerfile:27` |
| OpenAPI · `test_public_api_contract` | OK — 하위 앱 `mount` 는 `app.openapi()` 의 `paths` 에 안 들어간다. 시험은 `paths` 만 세고 `app.docs_url` · 태그 6 을 본다 → 무수정 통과 기대가 맞다 | `test_public_api_contract.py:229-260` |
| 라우트 겹침 | OK — 기존 라우터 접두는 `/api/v1*` · `/internal/legacy-prod` · `/health` 뿐 · `/procedure-hub/{…}` 잡이 없다. `Mount("/procedure-hub/gold")` 는 `/procedure-hub/gold-mcp/…` 를 안 잡는다(다음 글자 `-`) | `grep APIRouter(prefix` |
| CD verify(SQLite · alembic check · pytest · ruff) | 스키마 변경 0 이라 `alembic check` 영향 0. pytest 는 R-4. 실물 데이터 시험(`test_gold_real` 등)은 **env** 로 skip 판정하고 적재기 기본 경로(I-7 = 적재기에만)는 거기에 닿지 않는다 — OK | 각 시험 머리 · `config.py` |
| DI wiring | 서버(한 진입점)는 OK. 시험은 WORK §4 주의 그대로 + R-12 | `container.py` `wiring_config` |
| `test_entrypoint_imports_no_db` | WORK §4 #1 의 자리 조건(공용 조립 모듈이 `app.core.tx` · `app.core.db` import 0)으로 지켜진다 — OK | `test_gold_rest.py:74-78` |
| CORS · 요청 로그 | 본문 불변 · 머리만 — O-S9 받아들임 OK | `app_factory.py:46-54` |

### 2. 절차서 ①~⑨

- 순서 OK: ② `GOLD_REPOSITORY=db` 를 ③ CD(컨테이너 새로 만듦) **앞에** 둔다 · §11-4 가 `docker restart` 는 env 파일을 다시 안 읽는다고 바로 적었다 · ③ 의 꺼짐 이유(F2 냐 「필수 env 없음」 이냐)로 ② 가 먹었는지 가른다 — 좋다. ⑦ 은 env 를 안 바꾸므로 `docker restart` 로 맞다.
- 적재기와 서빙 동시성 OK: 적재는 `DELETE` · 한 트랜잭션(`medallion_load.py:368`)이라 서빙의 `REPEATABLE READ` 읽기를 막지 않고, 서빙은 시작 때만 읽는다 · F7 이 겹침을 잡는다.
- downgrade 금지 · 옛 이미지 금지 명시 OK — 단 ③ 실패 예외는 R-5.
- 멈출 곳: ③ ⑤ ⑥ ⑦ 모두 있음 · 메모리(R-3) · 시간(R-7) 만 빔.
- 값 자리표시만: §11 본문에 호스트 · 계정 · 레지스트리 값 0(확인). 출력 옮겨 적기는 R-9.
- 사용자가 그대로 따라 하기: ① ② ⑤ ⑥ ⑦ 은 명령 꼴이 있다 · 「컨테이너 새로 만들기」 명령 빠짐(R-8) · `<IMG>` 고르는 법(R-10).

### 3. 데이터 폴더 · Dockerfile · `.dockerignore` · 기본 경로

- `data/medallion/` = build context 밖(`.dockerignore` `**` 뒤 `!backend/…`) · BE CI(`backend/**` 등) · CD(`backend/**` · `.dockerignore` · 워크플로) · FE check(`frontend/**` · `docs/**` · `backend/README.md` …) 트리거 밖 — **단 R-D7 로 `backend/README.md` 를 고치면 BE CI · CD 둘 다 돈다**(`backend/**`) · FE check 도 돈다. 이번 판은 코드도 바뀌니 영향 없음 — 다음 「데이터만 갱신」 판(§11-4 갱신)에서 README 를 안 건드리면 재배포 0 이 맞다. OK
- Dockerfile 한 줄 OK — `prepare_legacy_prod.py` 가 화이트리스트 밖인데 이미 COPY 되는 것으로 보아 `!backend/` 가 하위를 통째 살린다(I-2 판단 맞음 · SE3 로 확인). 이미지 안 경로 `/app/scripts/load_medallion.py` → `BACKEND_DIR=/app` → 부모 `/` → `/data/medallion` (I-5) 계산 맞음(`load_medallion.py:18`).
- `GOLD_IMAGE_DIR=/assets/procedure-images` 꼴 OK — V13 은 `<dir>/images/**/*.svg` 를 본다(`medallion_load.py:232`) · 레포 SVG 103.
- 크기 약 13.4MB(로컬 du silver 5.8M · gold 폴더 6.3M(.py · .md 포함) · 원장 1.3M) — LFS 불필요 판단 OK.

### 4. WP ↔ SPEC · 시험 범위 · 로컬 데이터

- WORK §10 대응표: §11-0 ~ §11-9 미대응 0 — 확인. E1~E7 · I-1~I-8 · R-D1~R-D7 · ST1~ST9 · SE1~SE4 모두 WP 에 자리가 있다.
- 시험 범위: WP 마다 「돌릴 파일」 만 · 전체 금지 — 규칙 맞음. 빠진 파일은 R-4.
- 로컬 데이터: 워커 포트 18107 하나(지금 비어 있음) · 18105 · 18108 · 18432 는 읽기만 · SE1 은 18432 인스턴스 **안의 임시 DB 이름**(만들기 전 이름 확인 · 끝나면 지움) · SE2 는 `app.main` 의 DB 확인(`SELECT 1`) + gold 읽기뿐 · alembic · 적재기 안 돌림 · downgrade 금지 — **적재된 데이터를 건드리는 길 0**. OK

## 구현 전 꼭 고칠 것

1. **R-1** 꺼짐 503 본문(REST · MCP · gold `health`)에 접속 대상(`host=` · `port=` · `db=`)을 싣지 않는다 — F 코드 + 짧은 사유만, 대상은 로그에만. ST7 에 `host=` 0 단언.
2. **R-2** `app.main` 의 gold 적재에 시간 한도 → 넘으면 꺼짐(`gold_main` 불변) · 시험 하나.
3. **R-3** 절차서 ① 메모리 기록 · ⑦ 앞 멈출 곳(SE2 RSS 증가분 기준) · 재시작 고리 때 「끄기」 명령.
4. **R-4** WORK §6-2 ③ 묶음에 `app.main` 을 import 하는 시험 전부(`test_glossary_router` · `test_glossary_template` · `test_corpus_import_publication`) — 또는 마지막 한 번 CD 와 같은 전체 꼴.

(R-5 ~ R-12 는 SPEC/WORK 문장 보탬 — 구현과 같이 고쳐도 된다.)
