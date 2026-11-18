# research-db — silver · gold DB 화 설계 조사 (2026-11-17 · researcher · read-only)

> 발주: `db-research-brief.md` · 결정하지 않는다 — 추천만, 고를 것은 §0-2 「정할 것」.
> DB · 서버 · docker 를 띄우거나 접속하지 않았다. `.env` 를 열지 않았다. `$H` 는 읽기만(`git show` · `git log` · `git diff --stat`).
> 회사 데이터 본문 없음 — 표 이름 · 칸 이름 · id 꼴 · 셈만.
> 경로 접두어는 브리프와 같다: `$P`(프로필 워크트리) · `$W`(이번 작업 폴더) · `$SM`(silver-model · gitignore) · `$H`(허브 워크트리 · 브랜치 `kknaksss/phub-gold-jev` · HEAD `3750e4c` = `origin/release/v1.2.0`).
> 셈 스크립트는 세션 scratchpad 에만 있다(§7 에 명령 꼴과 결과).

## 0. 요약 · 정할 것

### 0-1. 요약(질문당)

| Q | 답 |
|---|---|
| Q1 기존 DB · stg 길 | PostgreSQL + async SQLAlchemy(asyncpg) · 스키마(네임스페이스)는 **쓰는 곳 0 — 전부 `public`** · alembic 한 줄 체인(헤드 `b202610300001`) · 테이블 167. **마이그레이션은 컨테이너가 뜰 때마다 `alembic upgrade head` 로 돈다**(`stg` push → Actions → 이미지 → VM 컨테이너 교체). 데이터 반입은 배포와 별개 gate — 운영자가 VM 에서 일회성 컨테이너로 CLI 를 돌리거나 `pg_restore` 로 넣는 것이 지금 길이다. silver 이름 둘(`modality` · `product`)이 기존 테이블과 **같은 이름**이다. gold 15(`g_*`)는 겹침 0 |
| Q2 표 → 테이블 | silver 57표 66,936행 387칸 · gold 15표 62,244행 278칸. **칸을 문자열 그대로 1:1 로 옮기면 「담을 칸 없는 값」 0.** 정규화하려 들 때만 걸리는 칸이 있다 — 여러 값 칸 13(gold) · 묶음 값 3 · 키 없는 표 3 · 다형 참조(표 이름 칸 + 코드 칸) gold 12짝 · silver 15칸 · 예약어 칸 `order` 2 · 소수 표기 1값. 허브가 지금 읽는 것 = gold 15 전부 + silver 5표(`source_ref` 전부 · `concern` · `adverse` · `condition` 은 2칸 · `concern_site` 3칸) + 원장 확인 목록(id · 코드만) |
| Q3 적재 · 빌드 추적 | `gold_hash` = gold 폴더 `*.csv` 16 파일(15표 + `questions.csv`)의 **파일 바이트** sha256 을 이름순으로 모아 다시 sha256 · `aux_hash` = 같은 식을 6 파일에. 이 워커가 다시 셈해 SPEC 값과 같음(`8accbb21…`). **DB 에는 파일 바이트가 없으므로 적재 때 셈한 값을 기록해 두는 자리(빌드 표)가 있어야 지금 응답 머리 · cursor 가 그대로 간다.** 원천 CSV 는 지금 로컬 gitignore 뿐 — stg 로 가는 길은 정해진 것이 없다(SPEC-001 O-8 그대로 열림) |
| Q4 repository 교체 | Protocol 메서드 29 · 앱에서 쓰는 것 27(`scope_by_holder` · `sites_of_concern` 은 앱 호출 0). **Protocol 은 동기(`def`)인데 허브 DB 엔진은 async(asyncpg) 하나뿐**이고, 한 요청이 repository 를 최대 수백 번 부른다(하위 닫힘 한 번에 `scope_by_subject` 최대 157회). 「시작 때 DB 에서 읽어 메모리 색인 그대로」 는 service · 도구 · 시험을 거의 안 건드리고, 「요청마다 쿼리」 는 코어 전체를 async 로 다시 써야 한다 |
| Q5 옛 판 대조 | 옛 스키마는 **허브가 gold 를 직접 짓고**(build.py 1,415줄) 값을 **JSON 칸**(`attrs` · `flags` · `evidence` · `source_refs` …)에 넣고 **빌드 번호로 쌓았다.** 새 gold 는 밖에서 지어 온 표라 그 셋이 다 필요 없다. 옛 브랜치 revision id `b202610300001` 이 지금 release 헤드와 **같은 글자**다(내용은 다름) — 옛 브랜치로 올린 로컬 DB 가 있으면 새 마이그레이션이 그 위에서 어긋난다 |

### 0-2. 정할 것(사용자가 고를 것만)

| # | 정할 것 | 선택지 | 추천 | 근거 | 위험 |
|---|---|---|---|---|---|
| D-1 | **DB 에 올릴 범위** | (a) gold 15 + 허브가 읽는 silver 만(`source_ref` · 계층 3표 · `concern_site`) + 원장 확인 (b) silver 57 전부 + gold 15 + 원장 확인 (c) gold 15 + gold 가 닿는 silver 39표 + `source_ref` · `concern_site` + 원장 확인 | **(b)** — 단 허브 코드가 읽는 범위는 (a) 그대로 두고 나머지 silver 는 「올려 두기만」 | (a) 111,357행 · (b) 129,505행 · (c) 128,275행 — 행 수 차이가 18,148(16%)뿐이다. (a) 는 `g_evidence.silver_table` + `silver_id` 가 가리키는 silver 행이 DB 에 없어 근거 길이 「문자열」 로만 이어진다(§2-3). (b) 는 gold 행 → silver 행 → `source_ref` 가 DB 안에서 닫히고 silver FK 80칸이 전부 걸린다(깨진 FK 0 · §2-2) | (b) 는 테이블 57 · 모델 57 이 늘고 silver 가 바뀔 때마다 마이그레이션이 따라간다(11-16 보강 때 표 1 · 칸 2 가 늘었다). 회사 데이터(설명 글 · 가격 표)가 stg DB 에 더 많이 올라간다. (c) 는 「닿는 표」 목록이 gold 빌드에 따라 바뀐다 |
| D-2 | **새 테이블 자리** | (a) `public` 에 접두어(gold 는 이미 `g_*` · silver 는 접두어 새로) (b) 별도 스키마(`gold` · `silver`) (c) 별도 DB | **(a)** | 허브에 스키마를 쓰는 곳이 0 이다(§1-4). 별도 스키마는 ① `alembic/env.py` 에 스키마 포함 설정이 없고 ② CI 의 `alembic check` 가 모델 ↔ DB 를 대조하며 ③ 기존 시험 20 파일이 SQLite 에 `Base.metadata.create_all` 을 한다 — 셋 다 공용 기반을 고쳐야 한다(§1-4). silver 접두어 없이는 `modality` · `product` 가 기존 테이블과 부딪힌다 | (a) 는 `public` 테이블이 167 → 182(gold) / 239(silver 포함)로 늘어 기존 팀 테이블과 섞여 보인다. 접두어를 `silver_` 로 하면 FK 이름 2개가 63자를 넘는다(`s_` 는 최대 63 — §2-4). (b) 가 실제로 되는지는 **확인 안 됨**(DB 를 띄우지 않았다 · stg 역할의 `CREATE SCHEMA` 권한도 확인 안 됨) |
| D-3 | **칸 타입** | (a) 전부 문자열(`TEXT NOT NULL DEFAULT ''`) — CSV 그대로 (b) 수 칸은 수 타입 · 빈칸은 NULL (c) (b) + 여러 값 칸을 자식 테이블로 | **(a)** — gold 는 반드시, silver 도 (a) | 계약이 「칸은 전부 문자열 · 값을 바꾸지 않는다」(`inputs.py:3` · SPEC-001 §2-1)이고 응답이 gold 행을 그대로 낸다(`core.py:116-121`). 수 타입으로 바꾸면 응답 때 문자열로 되돌려야 하고 소수 표기 1값이 float 왕복에서 달라진다(§2-5). 「담을 칸 없는 값 0」 은 (a) 에서만 셈 없이 성립한다 | (a) 는 DB 에서 수 비교 · 범위 조회를 못 한다(지금 허브 도구는 수 비교를 하지 않는다). `''` 와 NULL 을 섞지 않도록 적재기가 지켜야 한다 |
| D-4 | **빌드(판) 추적** | (a) 판 하나만 살아 있게 전체 교체 + 빌드 기록 표 1개(해시 · 파일별 sha256 · 행 수 · 적재 시각) (b) 빌드 표 + 모든 표에 판 칸(여러 판을 쌓고 발행 포인터로 고름) (c) 다음 판을 옆 테이블에 싣고 이름 바꿔치기 | **(a)** | gold 는 「불변 · 바뀌면 재시작」(SPEC-001 §2-3 1)이고 키가 판마다 다시 매겨질 수 있는 일련번호 꼴이다. (b) 는 옛 판이 한 방식이다 — 모든 PK · 인덱스 · 조회에 판 칸이 붙고 FK 가 복합이 된다(§5). 한 판이 12만 행 · 12MB 라 다시 싣는 비용이 작다 | (a) 는 DB 안에 옛 판이 없다 — 되돌리기 = 옛 CSV 묶음을 다시 싣는 것이라 **CSV 묶음을 판마다 보관하는 자리**가 있어야 한다(D-5). 적재 중 조회와 겹치지 않게 한 트랜잭션으로 바꿔야 한다 |
| D-5 | **원천 CSV 를 어디서 가져와 싣나** | (a) 운영자가 VM 디렉터리에 올리고 일회성 컨테이너의 적재 CLI 가 읽는다(지금 corpus 반입과 같은 길) (b) 허브 레포(비공개 회사 레포) `backend/import-data/` 에 CSV 를 커밋하고 이미지에 싣는다 (c) alembic 데이터 마이그레이션에 넣는다 (d) 로컬에서 실은 DB 를 `pg_dump --data-only` → stg 에 `pg_restore`(지금 baseline 반입과 같은 길) (e) 바깥 저장소(오브젝트 스토리지) | **(a)** | 허브 문서가 「seed/import corpus 는 이미지에 없다 · 저장소 밖」 을 기준으로 두고(`deployment.md:279-281` · `backend/README.md:44-45`) corpus 반입도 VM 디렉터리 + 읽기 전용 마운트다(`deployment.md:460-475`). SPEC-001 도 「레포에 CSV 를 커밋하지 않는다」 다(§2-1) | (a) 는 사람이 파일을 옮긴다 — 어느 판을 실었는지는 빌드 기록 표의 해시로만 확인된다. (b) 는 회사 데이터가 git 이력에 영구히 남고 `.dockerignore` · `Dockerfile` 을 고쳐야 한다. (c) 는 배포 때 컨테이너 시작이 적재를 기다리고 되돌리기가 마이그레이션 downgrade 가 된다. (e) 는 허브에 쓰는 곳이 있는지 **확인 안 됨** |
| D-6 | **repository 를 DB 로 바꾸는 방식** | (a) 시작 때 DB 에서 전부 읽어 지금 메모리 색인을 그대로 세운다 (b) 요청마다 SQL (c) (a) + 닫힘 · 계층 펼침을 빌드 때 테이블로 미리 | **(a)** | Protocol 이 동기이고 한 요청이 수백 번 부른다(§4-2). 허브에 동기 DB 드라이버가 없다(`pyproject.toml` — asyncpg · aiosqlite 뿐). (a) 는 service · 도구 9 · MCP · 시험 137개가 그대로 돈다(§4-4) | (a) 는 DB 를 「보관 · 배포 수단」 으로만 쓰는 셈이다 — SQL 로 조회하는 다른 소비자가 생기기 전에는 DB 의 이득이 「stg 에 데이터가 있다」 뿐이다. DB 를 다시 실어도 허브는 재시작해야 반영된다 |
| D-7 | **gold 가 stg 에서 뜨는 자리**(SPEC-001 O-7 — 그대로 열려 있음) | (a) `app.main` 에 gold 라우터 · MCP 를 붙인다 (b) 별도 진입점 `app.gold_main` 을 stg 에 따로 띄운다 | 이번 조사 범위(DB)가 아니다 — **사실만**: stg 이미지는 `app.main:app` 하나만 띄운다(`Dockerfile:27`). 테이블만 올리면 stg 에 gold API 는 없다 | `gold_main.py:4` 「DB 연결 없음 · `app.main` 과 별개」 | D-6 (a) 의 「시작 때 읽기」 가 어느 lifespan 에 들어가는지가 여기에 달려 있다 |
| D-8 | **원장 확인 목록을 DB 에 어떻게** | (a) id · 코드 쌍만(273쌍) 표 하나로 (b) 원본 16칸 전부 | **(a)** | 지금 허브가 「읽는 즉시 id 와 뽑은 코드만 남긴다 · 글 칸은 남기지 않는다」(`inputs.py:7` · SPEC-001 §2-1 X4 · X5) | (a) 는 코드 추출을 적재기가 한다 — 추출식(`inputs.py:37-38`)이 적재기로 옮겨 가고 `aux_hash` 에 들어가는 것은 원본 파일 바이트라 해시와 표 내용이 1:1 이 아니다 |

**사용자에게 물을 원천 질문(추천 없음)**: stg DB 역할이 새 테이블을 만들 수 있는 권한인지 · stg 에 회사 데이터(silver 설명 글 · 가격 표)를 올려도 되는 범위인지 — 이 조사로는 확인 못 했다.

---

## 1. Q1 — 허브 기존 DB 와 stg 반영 길

### 1-1. 엔진 · 접속 설정

| 항목 | 사실 | 근거 |
|---|---|---|
| 엔진 | PostgreSQL(CI · 리허설 `postgres:16`) · 드라이버 asyncpg · SQLAlchemy 2 async | `$H/backend/pyproject.toml:8,16` · `.github/workflows/backend-test.yml:37` · `backend/app/core/db.py:8-13` |
| 접속 설정 | env `DATABASE_URL` 하나(pydantic-settings · `backend/envs/.env` 또는 프로세스 env — 프로세스 env 가 앞섬). 없으면 **import 때 실패** | `backend/app/core/config.py:40-47` · `backend/app/core/db.py:17-22` |
| 풀 · 제한 | asyncpg 일 때만 `pool_pre_ping` · recycle 1800s · pool 대기 5s · 연결 5s · **쿼리 15s** | `core/db.py:33-42` · `core/config.py:49-53` |
| 세션 | `AsyncSessionLocal`(async_sessionmaker) · FastAPI 의존성 `get_db` | `core/db.py:48-58` |
| 시험 DB | pytest 는 SQLite 메모리(`sqlite+aiosqlite:///:memory:`) — Postgres 는 schema 검증에만 | `backend-test.yml:5,76-80` · `backend/README.md:62-66` |
| stg runtime env | VM 의 env-file 하나 · 필수 키는 `DATABASE_URL` 뿐 · Actions 는 앱 env 를 전달하지 않는다 | `docs/guides/deployment.md:214-216,231` |

- **gold 모듈은 지금 DB 를 전혀 모른다** — 설정도 따로(`GoldSettings` · `envs/.env.gold`)다(`modules/gold/config.py:24-29` · `gold_main.py:4`).
- 허브에 **동기 DB 드라이버가 없다**(psycopg 류 0 — `pyproject.toml` grep). Q4 에 걸린다.

### 1-2. alembic 체인 · 테이블

| 항목 | 사실 | 근거 |
|---|---|---|
| 체인 | `b202609030001`(initial · down None · 2,206줄 · create_table 166) → **`b202610300001`(헤드 · `legacy_prod_document` 1표)** — 가지 없음 | `backend/alembic/versions/*.py` 의 `revision` · `down_revision` |
| env | `settings.DATABASE_URL` 을 주입 · `target_metadata = Base.metadata` · async 엔진 · `NullPool` · **`include_schemas` · `version_table_schema` 없음** | `backend/alembic/env.py:18-24,41,47-52` |
| 모델 ↔ 마이그레이션 | 모델 `__tablename__` 167 = 마이그레이션 `create_table` 167(차집합 양쪽 0) | §7 셈 ① |
| 이름 규칙 | `Base.metadata` naming convention — `ix_%(column_0_label)s` · `fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s` · `pk_%(table_name)s` | `backend/app/model/base.py:8-14` |
| 모델 등록 | `app/model/__init__.py` 가 모델을 전부 import(「alembic autogenerate 감지용」) | `backend/app/model/__init__.py:1-60` |
| stg · prod 와 release | `origin/stg`(`a3cba75`) · `origin/prod`(`184e47e`) 의 `backend/` 는 `origin/release/v1.2.0`(`3750e4c`) 과 **같다**(차이 파일 = `docs/guides/prod-db-rename.md` 1개뿐). 세 브랜치 모두 versions 2 파일 | `git diff --quiet origin/stg origin/release/v1.2.0 -- backend` 등(§7 셈 ②) — fetch 하지 않았다(마지막 FETCH_HEAD 11-16) |

테이블 소유(모델 파일 = 묶음 · `app/model/*.py` 29 파일)

| 묶음 | 테이블 이름 머리 | 비고 |
|---|---|---|
| canonical(파일 이름 `canonical_*.py`) | `catalog_*` · `guidance_*` · `knowledge_*` · `publication_*` · `recommendation_*` · `safety_*` | 브리프의 「`canonical_*`」 는 **파일 이름**이고 테이블 이름에는 `canonical_` 이 없다 |
| 옛 정적 원장별 | `modality*` · `product*` · `procedure_profile*` · `procedure_comparison*` · `complication*` · `contraindication_rule` · `problem*` · `combo_recipe*` · `synergy_*` · `pricing_*` · `optimization_*` · `treatment_sequence_*` · `anatomy_*` … | silver 와 이름이 닮은 것이 여기 있다(§1-5) |
| 그 밖 | `glossary_version` · `translation_glossary` · `legacy_prod_document` | |

### 1-3. stg 에 새 테이블이 올라가는 길

```
feat/* → release/v1.2.0 → (PR) stg ─ push ─▶ Actions: backend-test(verify) → 이미지 빌드 → VM 컨테이너 교체
                                                                                   └ 컨테이너 CMD: alembic upgrade head && uvicorn app.main:app
```

| 단계 | 누가 · 언제 | 근거 |
|---|---|---|
| 트리거 | `stg` / `prod` push 중 `backend/**` · `.dockerignore` · 그 workflow 가 바뀌었을 때 · 또는 수동 dispatch(환경 선택) | `.github/workflows/csp-azure-deploy.yml:7-25` · `deployment.md:93-95` |
| 검증 | 배포 앞에 `backend-test.yml` 을 그대로 부른다 — **빈 PostgreSQL 에 `alembic upgrade head` + `alembic check`** · ruff · pytest(SQLite · `tests/integration` 제외) | `csp-azure-deploy.yml:54-55` · `backend-test.yml:66-80` |
| **마이그레이션 실행** | **컨테이너가 시작할 때마다** `alembic upgrade head` 뒤 uvicorn(사람이 따로 돌리지 않는다) | `backend/Dockerfile:26-27` |
| 배포 확인 | Gateway 로 `health` · `api/v1/products` 응답 꼴 확인 | `csp-azure-deploy.yml:152-160` |
| prod | 같은 workflow · 단 repository variable `PROD_CONTROLLED_CUTOVER == 'true'` 면 push 로는 배포 job 을 건너뛴다(수동 dispatch 만) | `csp-azure-deploy.yml:125-131` · `docs/guides/prod-migration.md:31-32` |
| 데이터 | **배포와 별개 gate** — 「FE 성공만으로 BE 배포 · DB migration · 데이터 반입 · publish 가 끝난 것으로 보지 않는다」 | `deployment.md:40-41` |

새 테이블을 더할 때 지켜야 할 것(사실만)

1. **모델이 있어야 한다.** CI 가 `alembic check` 로 `Base.metadata` 와 DB 를 대조한다(`backend-test.yml:68-70`). 마이그레이션에만 있고 모델에 없는 테이블은 「지울 테이블」 로 잡힌다(alembic 동작 — 이번에 돌려 보지 않음 · **확인 안 됨**).
2. **모델은 SQLite 에서도 만들어져야 한다.** 기존 시험 20 파일이 SQLite 에 `Base.metadata.create_all` 을 한다(§7 셈 ③ — `grep create_all backend/tests` 20줄). PostgreSQL 전용 타입은 지금 `JSON().with_variant(JSONB(), "postgresql")` 꼴로 쓴다(`app/model/legacy_prod.py:15-17`).
3. **revision id 는 옛 브랜치와 겹치지 않게.** 옛 브랜치(`origin/kknaksss/phub-recommend`)가 `b202610260001` · `b202610300001` · `b202610310001` 을 썼고 그중 `b202610300001` 은 지금 release 헤드와 **글자가 같다**(§5).
4. **헤드를 올린 뒤에는 옛 이미지로 그냥 못 돌아간다.** 옛 이미지도 시작 때 `alembic upgrade head` 를 도는데 DB 의 revision 을 모르면 실패한다 — 허브 문서가 baseline 전환에서 같은 실패를 적어 두었다(`deployment.md:288-290,367-371`). 새 헤드에서 runtime 만 되돌리려면 downgrade 가 먼저다.
5. **prod 에도 같은 마이그레이션이 간다.** `stg` → `prod` 승격 때 같은 이미지가 prod 에서 `upgrade head` 를 돈다 — 데이터를 안 실어도 빈 테이블은 생긴다.
6. **prod 전환 문서 · 도구에 박힌 revision.** `scripts/prepare_legacy_prod.py:161-162` 가 대상 revision `b202610300001` 을 고정으로 대조하고 `docs/guides/prod-db-rename.md:12-19` 가 「현재 운영 = `b202610300001` · 다르면 중지」 를 사전 점검에 둔다. 앞의 것은 문서가 「끝난 첫 이관의 역사적 검증 계약 · 다시 돌리지 않는다」 고 적었다(`prod-db-rename.md:36-44`). 뒤의 이름 전환이 **끝났는지는 확인 안 됨**(문서만 읽었다) — 안 끝났다면 새 헤드가 prod 에 가기 전에 그 절차와 순서가 걸린다.
7. **freeze guard** 는 새 테이블과 직접 닿지 않는다 — `scripts/cutover_legacy_prod.py:45-100` 의 `FreezeGuard` 는 첫 prod 이관 때 원본 DB 의 relation 119개 잠금을 확인하는 장치다(`prod-migration.md:294-309`).
8. `prod_readiness.py:674,684` · `prepare_legacy_prod.py:216` 은 `table_schema='public'` 만 본다 — 새 테이블을 `public` 에 두면 그 목록에 들어가고 다른 스키마에 두면 안 보인다.

### 1-4. 스키마(네임스페이스)

| 확인 | 결과 | 근거 |
|---|---|---|
| 모델 · 마이그레이션 · 스크립트에서 `schema=` · `search_path` · `CREATE SCHEMA` · `version_table` | **0건**(잡힌 것은 `include_in_schema=False`(OpenAPI) 1 · `information_schema … table_schema='public'` 3) | `grep -rn "schema=\|search_path\|CREATE SCHEMA\|version_table" app alembic scripts` |
| alembic env | `include_schemas` 없음 — 기본 스키마만 본다 | `alembic/env.py:27-44` |
| 시험 | SQLite `create_all` 20 파일 — SQLite 는 스키마 이름을 붙인 테이블을 그대로 못 만든다(ATTACH 가 있어야 함 · 일반 동작 · **이번에 돌려 보지 않음**) | §7 셈 ③ |
| stg 역할 권한 | `CREATE SCHEMA` 가능 여부 **확인 안 됨**. 허브 문서도 운영 역할의 「DB/schema CREATE 권한」 을 따로 확인할 것으로 둔다 | `prod-migration.md:123-125` |

→ 별도 스키마는 **지금 허브에 전례가 없고** `env.py` · 시험 기반을 함께 고쳐야 한다. 가능 여부 자체는 확인 안 됨(D-2).

### 1-5. 이름 · FK 충돌

| 대조 | 결과 | 셈 |
|---|---|---|
| gold 15 이름 ∩ 기존 167 | **0** | §7 셈 ① |
| silver 57 이름 ∩ 기존 167 | **2 — `modality` · `product`**(같은 이름 · 다른 칸 구성) | 같음 |
| 기존 테이블 중 `g_` · `gold_` · `silver_` 로 시작 | 0 | 같음 |
| silver 이름을 머리로 갖는 기존 테이블 | 39(`modality_*` 18 · `product_*` 3 · `procedure_profile*` 5 · `procedure_comparison*` 4 · `anatomy_*` 7 · `contraindication_rule` 1 + 위 2) — 같은 이름은 아니지만 접두어 없이 두면 `product_modality`(silver) 와 `modality_product`(기존)처럼 헷갈리는 짝이 생긴다 | 같음 |
| FK | 새 테이블에서 기존 테이블로 FK 를 걸 근거가 없다 — silver · gold 의 코드(`M1` · `PRC-…` · `PRD-…` 꼴)는 기존 테이블의 키와 다른 체계다(대응표는 `external_code` 가 자리만 있고 0행). 옛 판 모델도 「기존 테이블 · v1 graph 테이블과 FK 로 잇지 않는다」 로 두었다 | `$SM/notes/silver-erd.md:15`(「`external_code` … 설계만 — 행 0」) · `git show origin/kknaksss/phub-recommend:backend/app/model/gold.py:3` |
| 옛 브랜치 테이블 이름 | `gold_node` · `gold_edge` · `gold_build` · `gold_fact` · `gold_dictionary` · `gold_global` · `gold_publication` · `gold_source_snapshot` · `graph_*` — release 에는 없다(PR #31 draft). **옛 브랜치로 올린 로컬 DB 에는 남아 있을 수 있다** | `git show origin/kknaksss/phub-recommend:backend/alembic/versions/b202610300001_gold_schema.py:32-129` |

### 1-6. 지금 시드 · 적재 방식(`import-data` · `importing`)

| 무엇 | 사실 | 근거 |
|---|---|---|
| `backend/import-data/` | 파일 1개 — `canonical-mapping.v1.json`(매핑 등록부 · 20K). **데이터 본체는 없다** | `ls backend/import-data` |
| `backend/app/importing/` | 옛 정적 JSON 47 파일 corpus 를 읽고 검증하는 코드(3 파일 3,856줄) — DB 를 건드리지 않고 문제를 issue 로 낸다 | `app/importing/legacy_corpus.py:1-7` |
| 반입 CLI | `scripts/import_legacy_corpus.py` — `--dry-run`(쓰기 없음) · apply 는 **draft revision 만** 만들고 live 테이블 · publish 는 건드리지 않는다. exit 0 / 2 | `scripts/import_legacy_corpus.py:2-14` |
| 반입 기록 테이블 | `publication_source_artifact`(locator + checksum 유일) · `publication_import_job`(상태 5) · `publication_content_revision`(domain + content_hash 유일) · `publication_content_release`(**published 는 하나만** — 부분 유일 인덱스) | `app/model/canonical_publication.py:35-52,64-87,108-147,169-189` |
| stg 에서 CLI 돌리는 법 | 이미지에 CLI · 매핑 · corpus 가 없다 → VM 디렉터리에 두고 **일회성 컨테이너**(`--entrypoint .venv/bin/python` · env-file · 읽기 전용 마운트)로 | `deployment.md:460-475` |
| 초기 데이터 | 「seed/import corpus 와 data-init image 는 없다」 — 저장소 밖 snapshot 을 `pg_restore --data-only` 로 **수동** 복원 · 「서버 시작은 초기 데이터를 적재하지 않는다」 | `deployment.md:279-281,323-329` · `backend/README.md:44-45` |
| 이미지에 들어가는 것 | `app/` · `alembic/` · `alembic.ini` · `scripts/` 일부뿐(`.dockerignore` 가 그 밖 전부를 뺀다) | `backend/Dockerfile:13-22` · `.dockerignore:2-12` |

→ 허브에는 **「마이그레이션은 자동 · 데이터는 사람이 gate 를 열고 따로」** 가 굳어 있다. 새 데이터를 싣는 길도 여기에 맞추는 것이 전례와 같다(D-5 (a) · (d)).

---

## 2. Q2 — silver · gold → 테이블

### 2-1. gold 15표(62,244행 · 278칸 · 빈칸 177,469 / 714,598 = 25%)

| 표 | 행 | 칸 | 키 | 다른 표와 잇는 칸 | 수 칸 | 여러 값 칸 | 빈칸 비율 | 가장 긴 칸(B) |
|---|---:|---:|---|---|---|---|---:|---:|
| `g_adverse` | 2,923 | 35 | gid | target_table · target_code · adverse_code · silver_table · silver_id · freq_silver_id | onset_min · onset_max · duration_min · duration_max · freq_min · freq_max · n_factor · n_guidance | — | 59% | 203 |
| `g_adverse_detail` | 3,828 | 17 | gid | adverse_risk_id · target_table · target_code · silver_table · silver_id | — | — | 32% | 544 |
| `g_contraindication` | 350 | 19 | gid | target_table · target_code · condition_code · silver_table · silver_id | period_min · period_max | — | 39% | 213 |
| `g_edge` | 10,389 | 7 | edge_id | gold_table · gold_id · src · dst | — | — | 0% | 23 |
| `g_entry` | 2,642 | 10 | gid | entity_table · entity_code · silver_table · silver_id | — | silver_id(|) | 0% | 65 |
| `g_evidence` | 27,740 | 6 | (gold_table, gold_id, silver_table, silver_id) | gold_table · gold_id · silver_table · silver_id | — | fields(|) | 16% | 25 |
| `g_indication` | 4,866 | 23 | gid | asked_concern_code · concern_code · site_code · target_table · target_code · candidate_table · candidate_code · procedure_code · silver_table · silver_id | — | conditions | 21% | 128 |
| `g_node` | 1,545 | 7 | node_id | node_table · node_code · silver_table · silver_id | — | — | 0% | 58 |
| `g_offer` | 163 | 28 | gid | offer_id · modality_code · item_table · item_code · procedure_code · silver_table · silver_id | price_low · price_high · price_mid_raw | quantities · sites · concerns · effects · materials | 24% | 136 |
| `g_outcome` | 1,604 | 26 | gid | target_table · target_code · effect_code · silver_table · silver_id | onset_min · onset_max · peak_min · peak_max · duration_min · duration_max | — | 56% | 195 |
| `g_package` | 312 | 21 | gid | package_id · concern_code · item_table · item_code · item_procedure_code · silver_table · silver_id | step · n_schedule | conditions | 32% | 261 |
| `g_pair` | 904 | 27 | gid | from_table · from_code · to_table · to_code · conflict_id · silver_table · silver_id | interval_min · interval_max · order | goal_effects | 38% | 453 |
| `g_profile` | 739 | 27 | gid | subject_table · subject_code · modality_code · procedure_code · mechanism_code · silver_table · silver_id | n_cases · n_products | modality_code · modality_name · materials · methods · organizations | 41% | 832 |
| `g_recovery` | 37 | 12 | gid | target_table · target_code · silver_table · silver_id | min · max | — | 27% | 61 |
| `g_scope` | 4,202 | 13 | gid | subject_table · subject_code · holder_table · holder_code · silver_table · silver_id | — | — | 0% | 58 |

- **키**: 12표 `gid` · `g_node.node_id` · `g_edge.edge_id` — 전부 유일 · 빈칸 0 · 파일 순서 = 키 오름차순. `gid` · `edge_id` 는 `영문-숫자` 꼴 · 폭 고정(9B). `node_id` 는 `표:코드` 꼴(폭 다름 · 최대 23B).
- **`g_evidence` 는 키 칸이 없다**(`headers.py:45-46`) — (`gold_table`, `gold_id`, `silver_table`, `silver_id`) 넷이 유일(27,740 / 27,740). 같은 gold 행의 참조는 파일에서 이어져 있다(묶음 수 = 서로 다른 (`gold_table`, `gold_id`) 24,115).
- **값 종류**: 문자 249칸 · 정수 26칸 · 소수 2칸(`g_adverse.freq_min` · `freq_max`) · 전부 빈 칸 1(`g_adverse_detail.site_name`).
- **글자**: 줄바꿈 든 칸 0 · 앞뒤 공백 칸 0 · NUL 0 · 가장 긴 칸 832B(`g_profile.mechanism_text`).
- **되짚기 칸**: `g_evidence` 밖 14표 가운데 13표가 `silver_table` + `silver_id` 를 갖는다(`g_edge` 는 `gold_table` + `gold_id`) — silver 키로 못 찾는 행 0. 단 **`g_entry` 의 831행은 `silver_table = alias` · `silver_id = 「표|코드|이름」` 세 조각 묶음**이다(`alias` 에 키 칸이 없어서 — §2-2).
- **무결성(다시 셈)**: `g_evidence` 가 가리키는 gold 행 없음 0 · silver 행 없음 0 · `g_edge.src` / `dst` 가 `g_node` 에 없음 0 / 0 · `g_edge` 가 가리키는 gold 행 없음 0.

### 2-2. silver 57표(66,936행 · 387칸 · 빈칸 131,189 / 385,135 = 34%)

층: ① 사전 23 · ② 조합 6 · ③ 관계 20 · ④ 상품 8(`$SM/notes/silver-erd.md:8,228,304,587` · `drafts/silver-check/silver-schema.json`). 키 · FK 는 그 스키마 파일의 `key` · `fk` 를 그대로 읽었다.

| 층 | 표 | 행 | 칸 | 키 | FK 칸(→ 표) | 다형 칸 | 수 칸 | 빈칸 비율 | 가장 긴 칸(B) |
|---|---|---:|---:|---|---|---|---|---:|---:|
| ① | `adverse` | 188 | 7 | code | parent_code→adverse | — | — | 1% | 1324 |
| ① | `alias` | 980 | 4 | 없음 | — | target_table | — | 0% | 59 |
| ① | `anatomy` | 105 | 7 | code | tissue_code→tissue | — | — | 7% | 139 |
| ① | `anatomy_site` | 89 | 3 | id | anatomy_code→anatomy · site_code→site | — | — | 0% | 8 |
| ① | `concern` | 260 | 7 | code | parent_code→concern | — | — | 1% | 832 |
| ① | `concern_site` | 95 | 3 | id | concern_code→concern · site_code→site | — | — | 0% | 8 |
| ① | `condition` | 151 | 8 | code | parent_code→condition · material_code→material | — | — | 13% | 936 |
| ① | `effect` | 70 | 7 | code | parent_code→effect | — | — | 4% | 885 |
| ① | `external_code` | 0 | 8 | id | — | target_table | — | 0% | 0 |
| ① | `material` | 143 | 7 | code | parent_code→material | — | — | 9% | 357 |
| ① | `material_spec` | 33 | 5 | id | material_code→material | — | — | 0% | 16 |
| ① | `mechanism` | 54 | 6 | code | parent_code→mechanism | — | — | 13% | 501 |
| ① | `method` | 49 | 7 | code | parent_code→method | — | — | 13% | 414 |
| ① | `modality` | 18 | 5 | code | — | — | — | 2% | 585 |
| ① | `organization` | 202 | 7 | code | current_org_code→organization | — | — | 44% | 139 |
| ① | `product` | 315 | 10 | code | parent_code→product | — | — | 38% | 518 |
| ① | `product_material` | 390 | 5 | id | product_code→product · material_code→material | — | — | 0% | 16 |
| ① | `product_method` | 63 | 3 | id | product_code→product · method_code→method | — | — | 0% | 9 |
| ① | `product_modality` | 317 | 3 | id | product_code→product · modality_code→modality | — | — | 0% | 9 |
| ① | `product_organization` | 575 | 6 | id | product_code→product · org_code→organization | — | — | 0% | 262 |
| ① | `site` | 89 | 6 | code | parent_code→site | — | — | 26% | 354 |
| ① | `source_ref` | 48,094 | 4 | 없음 | — | target_table | — | 21% | 222 |
| ① | `tissue` | 25 | 7 | code | parent_code→tissue | — | — | 14% | 284 |
| ② | `case_method` | 107 | 3 | id | case_code→procedure_case · method_code→method | — | — | 0% | 8 |
| ② | `case_product` | 332 | 3 | id | case_code→procedure_case · product_code→product | — | — | 0% | 8 |
| ② | `procedure` | 138 | 8 | code | modality_code→modality · mechanism_code→mechanism | — | — | 17% | 832 |
| ② | `procedure_case` | 268 | 8 | code | procedure_code→procedure · tissue_code→tissue · anatomy_code→anatomy · site_code→site · material_code→material | — | — | 47% | 377 |
| ② | `procedure_material` | 175 | 3 | id | procedure_code→procedure · material_code→material | — | — | 0% | 8 |
| ② | `product_procedure` | 81 | 4 | id | product_code→product · procedure_code→procedure | — | — | 0% | 97 |
| ③ | `adverse_factor` | 732 | 7 | id | adverse_risk_id→adverse_risk · condition_code→condition · site_code→site · anatomy_code→anatomy | — | — | 40% | 502 |
| ③ | `adverse_frequency` | 344 | 9 | id | adverse_risk_id→adverse_risk | — | min(num) · max(num) | 44% | 85 |
| ③ | `adverse_guidance` | 3,061 | 9 | id | adverse_risk_id→adverse_risk | target_table | — | 42% | 544 |
| ③ | `adverse_rating` | 69 | 7 | id | adverse_risk_id→adverse_risk · scale_id→rating_scale | target_table | value(int) · text(int) | 21% | 14 |
| ③ | `adverse_risk` | 2,840 | 18 | id | adverse_code→adverse · site_code→site | target_table | onset_min(int) · onset_max(int) · duration_min(int) · duration_max(int) | 68% | 203 |
| ③ | `citation` | 63 | 9 | id | — | — | pmid(int) | 47% | 227 |
| ③ | `citation_link` | 241 | 5 | id | citation_id→citation | relation_table | — | 0% | 471 |
| ③ | `contraindication` | 350 | 14 | id | condition_code→condition · site_code→site | target_table | period_min(int) · period_max(int) | 52% | 213 |
| ③ | `indication` | 1,705 | 6 | id | concern_code→concern · site_code→site | target_table | — | 29% | 119 |
| ③ | `indication_condition` | 56 | 4 | id | indication_id→indication · condition_code→condition | — | — | 0% | 29 |
| ③ | `outcome` | 1,604 | 21 | id | effect_code→effect · site_code→site | target_table | onset_min(int) · onset_max(int) · peak_min(int) · peak_max(int) · duration_min(int) · duration_max(int) | 67% | 195 |
| ③ | `package` | 119 | 15 | id | concern_code→concern | — | duration_min(int) · duration_max(int) | 62% | 261 |
| ③ | `package_condition` | 3 | 4 | id | package_id→package · condition_code→condition | — | — | 0% | 8 |
| ③ | `package_item` | 312 | 7 | id | package_id→package | target_table | step(int) | 35% | 40 |
| ③ | `package_schedule` | 28 | 6 | id | package_id→package | — | week_text(int) · week_min(int) · week_max(int) | 0% | 94 |
| ③ | `procedure_relation` | 904 | 17 | id | — | from_table · to_table | interval_min(int) · interval_max(int) · order(int) | 42% | 453 |
| ③ | `procedure_relation_effect` | 127 | 4 | id | relation_id→procedure_relation · effect_code→effect | — | — | 8% | 25 |
| ③ | `rating_scale` | 4 | 6 | id | — | — | — | 50% | 26 |
| ③ | `recovery` | 37 | 8 | id | — | target_table | min(int) · max(int) | 40% | 61 |
| ③ | `statement_translation` | 384 | 4 | id | citation_link_id→citation_link | — | — | 0% | 194 |
| ④ | `offer` | 122 | 10 | id | price_list_id→price_list · modality_code→modality | — | price_low(int) · price_mid(int) · price_high(int) | 29% | 44 |
| ④ | `offer_concern` | 28 | 4 | id | offer_id→offer · concern_code→concern | — | — | 0% | 16 |
| ④ | `offer_effect` | 10 | 4 | id | offer_id→offer · effect_code→effect | — | — | 2% | 16 |
| ④ | `offer_item` | 163 | 6 | id | offer_id→offer | target_table | — | 4% | 136 |
| ④ | `offer_material` | 17 | 4 | id | offer_id→offer · material_code→material | — | — | 0% | 16 |
| ④ | `offer_quantity` | 129 | 6 | id | offer_id→offer | — | amount(num) | 17% | 14 |
| ④ | `offer_site` | 77 | 4 | id | offer_id→offer · site_code→site | — | — | 0% | 16 |
| ④ | `price_list` | 1 | 5 | id | — | — | version(num) | 0% | 106 |

- **키**: 55표가 `code`(사전 · 시술 · 케이스) 또는 `id` — 전부 유일. **키 없는 표 2**: `alias`(980행 — (`target_table`, `target_code`, `name`) 셋이 유일) · `source_ref`(48,094행 — 네 칸 전체가 유일 · 그보다 좁은 유일 묶음 없음 · `ref` 최대 222B).
- **FK**: 스키마에 FK 칸 80 — 실제 값으로 대조해 **깨진 FK 0**(§7 셈 ④). 자기 참조(`parent_code` 류)가 사전 표에 있다.
- **다형 참조(표 이름 칸 + 코드 칸)**: 14표 15칸 — `target_table`(11표) · `relation_table`(`citation_link`) · `from_table` / `to_table`(`procedure_relation`). 가리키는 표가 5~54가지라 **FK 한 줄로 못 건다.** `source_ref.target_table` 은 54표(= 57 − `alias` · `source_ref` · `external_code`) · silver 행을 못 찾는 `source_ref` 0.
- **값 종류**: 문자 340칸 · 정수 29 · 소수 4(`adverse_frequency.min` · `max` · `offer_quantity.amount` · `price_list.version` — 마지막은 판 번호 글자다) · 전부 빈 칸 14(`external_code` 8칸은 표가 0행 · 그 밖 6칸).
- **여러 값 칸**: **0** — ` · ` 가 든 칸은 전부 설명 · 메모 글(`description` · `note` · `text`)이다. silver 는 목록을 연결 표로 풀어 두었다.
- **고정 값 칸**: 스키마에 값 목록(`values`)이 있는 칸 34 · id 꼴(`id_pattern`)이 있는 표 55 · 값 뜻은 `$SM/notes/vocabulary.csv`.

### 2-3. 허브가 실제로 읽는 범위(메모리 판 기준)

| 입력 | 읽는 칸 | 행 | 쓰임 | 근거 |
|---|---|---:|---|---|
| gold 15표 | 헤더 전부(순서까지 계약 대조) | 62,244 | 도구 9 | `inputs.py:107-116` · `headers.py:6-41` |
| gold 폴더의 그 밖 CSV(`questions.csv`) | 읽지 않음 — **해시에만** | — | `gold_hash` | `inputs.py:117-121` |
| silver `source_ref` | 4칸 전부 | 48,094 | `evidence` 도구의 끝 | `inputs.py:123-129` · `memory.py:61-64,108-114` |
| silver `concern` · `adverse` · `condition` | **`code` · `parent_code` 2칸만**(7 · 7 · 8칸 중) | 260 · 188 · 151 | 계층 펼침 · 윗고민 물려받기 | `inputs.py:131-145` · `headers.py:57-58` |
| silver `concern_site` | `id` · `concern_code` · `site_code`(3칸 = 전부) | 95 | 부위로 고민 묶기 | `inputs.py:147-156` · `headers.py:60-61` |
| `notes/ledger-check-list.csv`(silver · gold 아님) | `id` + 코드 추출용 3칸(`silver_now` · `what` · `name`) — 읽는 즉시 id · 코드만 남김 | 325(코드 든 행 251 · 코드 218 · 쌍 273) | `ledger_check[]` | `inputs.py:158-175` · `headers.py:62-63` |

- 즉 허브가 읽는 silver 는 **57표 중 5표**이고 그중 3표는 2칸만이다. gold 의 이름 칸(`*_name`)이 silver 이름을 이미 복사해 갖고 있어서다(SPEC-001 §2-1 X2).
- `concern_site` 의 근거(`source_ref` 574행)는 **지금 도구로 닿지 않는다** — `evidence` 는 gold 행에서만 출발한다(`service.py:122-150`). 응답의 `csi_ids` 를 받아도 되짚을 도구가 없다(사실 기록 — 이번 범위 밖).

**범위 선택지(D-1)**

| | (a) gold 15 + 허브가 읽는 silver | (b) silver 57 + gold 15 | (c) gold 15 + gold 가 닿는 silver |
|---|---|---|---|
| 테이블 | 15 + 5 + 원장 확인 1 = **21** | 15 + 57 + 1 = **73** | 15 + 39 + `source_ref` · `concern_site` + 1 = **57** |
| 행 | 62,244 + 48,094 + 599 + 95 + 325 = **111,357** | 62,244 + 66,936 + 325 = **129,505** | 62,244 + 17,517 + 48,094 + 95 + 325 = **128,275** |
| 근거 길(gold 행 → 원장 포인터) | `g_evidence` → (`silver_table`, `silver_id`) **글자** → `source_ref.ref` — 지금과 같다. 가운데 silver 행은 DB 에 없다 | gold 행 → `g_evidence` → **silver 행(FK 가능)** → `source_ref` → `ref` — DB 안에서 닫힌다 | (b) 와 같되 gold 가 안 닿는 18표의 `source_ref` 3,287행은 대상 행이 없다 |
| 되짚기에서 끊기는 것 | silver 값을 DB 에서 볼 수 없다(「gold 값 ⊂ silver 값」 을 DB 로 다시 확인 못 함 — gold-check 가 CSV 에서만 한다) | 없음 | 문헌(`citation` · `citation_link`) · 번역(`statement_translation`) · 회사(`organization`) 등 18표 |
| 계층 3표 | 2칸만 싣면 silver 표와 이름은 같고 칸이 모자란 「반쪽 표」 가 된다 · 전부 싣면 (a) 의 뜻이 흐려진다 | 통째 | 통째(39표에 든다) |
| 위험 | 나중에 silver 를 올리면 `source_ref` 대상 FK 를 그때 건다 | 테이블 · 모델 · 마이그레이션 57 · 이름 충돌 2(접두어 필요) · silver 변경이 곧 스키마 변경 | 「닿는 표」 가 gold 판마다 달라질 수 있다(지금 38 + `alias`) |

gold 가 안 닿는 silver 18표(행): `source_ref` 48,094 · `statement_translation` 384 · `citation_link` 241 · `organization` 202 · `concern_site` 95 · `offer_site` 77 · `citation` 63 · `product_method` 63 · `mechanism` 54 · `material_spec` 33 · `offer_concern` 28 · `package_schedule` 28 · `tissue` 25 · `offer_material` 17 · `offer_effect` 10 · `rating_scale` 4 · `price_list` 1 · `external_code` 0(§7 셈 ⑤).

### 2-4. 표 → 테이블 대응 초안(표 1:1)

**공통 규칙(초안 — D-2 · D-3 에 따라 바뀐다)**

| 항목 | 초안 | 근거 |
|---|---|---|
| 표 ↔ 테이블 | CSV 1 = 테이블 1 · 칸 이름 그대로(순서도) | 계약이 헤더 순서까지 대조한다(`inputs.py:113-114`) |
| 테이블 이름 | gold = CSV 이름 그대로(`g_entry` …) · silver = 접두어 + CSV 이름 | gold 겹침 0 · silver 겹침 2(§1-5) |
| 칸 타입 | `TEXT NOT NULL DEFAULT ''` — 빈칸은 `''` | `inputs.py:3` 「칸은 전부 문자열」 · 서비스 코드가 빈칸을 `""` 로 비교한다(`concern.py:75` · `memory.py:74`) |
| PK | gold 12표 `gid` · `g_node.node_id` · `g_edge.edge_id` · silver 55표 `code` / `id` | §2-1 · §2-2 |
| 키 없는 표 3 | `g_evidence` — (`gold_table`, `gold_id`, `silver_table`, `silver_id`) 복합 PK 또는 순번 칸 · `alias` — (`target_table`, `target_code`, `name`) · `source_ref` — 순번 칸(네 칸 복합은 `ref` 가 길다) | 유일성 셈 §2-1 · §2-2 |
| **행 순서 칸** | 3표(`g_evidence` · `source_ref` · `alias`)에 **적재 순번 칸**이 있어야 한다 — 지금 응답의 `refs[]` · `source_refs[]` 순서가 **파일 순서**다(`repository.py:5` · `service.py:136-139`) · 키 있는 표는 키 오름차순 = 파일 순서라 순번이 필요 없다(§2-1) | 같은 입력 = 같은 응답 · cursor 가 순서에 기댄다(`core.py:100-106`) |
| FK(silver) | 스키마의 80칸 그대로 · 다형 15칸은 FK 없음(값 검사는 적재기) | §2-2 |
| FK(gold) | 걸 수 있는 것: `g_edge.src` / `dst` → `g_node.node_id` · `g_adverse_detail.adverse_risk_id` 는 **gold 가 아니라 silver** 키다 · 그 밖 `*_code` 칸은 전부 「표 이름 칸 + 코드 칸」 짝이거나 silver 코드 → gold 안에서는 FK 없음이 기본 | §2-5 C |
| 인덱스 | 지금 메모리 색인과 1:1(§4-1 표의 「칸」 열) | `memory.py:45-60` |
| 제약 · 인덱스 이름 | **직접 지어 준다** — 규칙이 첫 칸만으로 이름을 정해 (`subject_table`, `subject_code`) · (`subject_table`) 같은 복합 인덱스끼리 겹친다(옛 판이 같은 이유로 직접 지었다) | `model/base.py:9` · `git show origin/kknaksss/phub-recommend:backend/app/model/gold.py:3-5` |
| 이름 길이 | FK 이름 규칙 `fk_<표>_<칸>_<대상 표>` — 접두어 없이 최대 59 · `s_` 63 · **`silver_` 73(63 넘는 것 2)** | §7 셈 ⑥ |
| 예약어 칸 | `order` 2칸(`g_pair.order` · `procedure_relation.order`) — 따옴표가 붙어야 한다(SQLAlchemy 는 알아서 붙인다 · 손 SQL 은 주의) | §7 셈 ⑦ |

**gold 15표 초안**

| 테이블 | PK | 인덱스 후보(= 지금 색인) | 다른 표로 가는 칸 |
|---|---|---|---|
| `g_entry` | `gid` | (`norm`) · (`entity_table`, `entity_code`) · (`entity_table`) | `entity_table` + `entity_code`(14표) · `silver_table` + `silver_id`(831행은 세 조각 묶음) |
| `g_scope` | `gid` | (`subject_table`, `subject_code`) · (`holder_table`, `holder_code`) | `subject_*` · `holder_*`(각 5표) · `silver_*`(8표) |
| `g_profile` | `gid` | (`subject_table`, `subject_code`) **유일**(739 / 739) · 속성 맞춤 4칸(`materials` · `methods` 조각 · `anatomy_name` · `site_name`) | `subject_*`(4표) · `modality_code`(2행은 두 값) · `procedure_code` · `mechanism_code` |
| `g_indication` | `gid` | (`target_table`, `target_code`) · (`asked_concern_code`) · (`procedure_code`) · (`concern_code`) · 속성 맞춤 3칸 | `target_*` · `candidate_*`(각 5표) · `*_concern_code` · `site_code` · `procedure_code` |
| `g_outcome` | `gid` | (`target_table`, `target_code`) · (`effect_code`) · `site_name` | `target_*` · `effect_code` |
| `g_adverse` | `gid` | (`target_table`, `target_code`) · (`adverse_code`) · `site_name` | `target_*` · `adverse_code` · `silver_id` · `freq_silver_id`(silver `adverse_frequency`) |
| `g_adverse_detail` | `gid` | (`target_table`, `target_code`) · (`adverse_risk_id`) · `anatomy_name` · `site_name` | `adverse_risk_id`(silver `adverse_risk`) · `silver_*`(3표) |
| `g_recovery` | `gid` | (`target_table`, `target_code`) | `target_*`(4표) |
| `g_contraindication` | `gid` | (`target_table`, `target_code`) · (`condition_code`) · `site_name` | `target_*`(3표) · `condition_code` |
| `g_pair` | `gid` | (`from_table`, `from_code`) · (`to_table`, `to_code`) · (`question_class`) | `from_*` · `to_*`(5표 + **빈칸** 6 · 31행) |
| `g_package` | `gid` | (`item_table`, `item_code`) · (`package_id`) · (`concern_code`) | `package_id` · `item_*`(3표 + 빈칸 47) · `concern_code` · `item_procedure_code` |
| `g_offer` | `gid` | (`item_table`, `item_code`) · (`offer_id`) · (`procedure_code`) · 속성 맞춤 2칸(`materials` · `sites` 조각) | `offer_id` · `item_*`(3표 + 빈칸 20) · `modality_code` · `procedure_code` |
| `g_node` | `node_id` | — (`node_code` 도 유일 1,545) | `node_table` + `node_code`(10표) · `silver_*` |
| `g_edge` | `edge_id` | (`src`, `edge_type`) · (`dst`, `edge_type`) | `src` / `dst` → `g_node`(없는 것 0) · `gold_table` + `gold_id`(8표 · `gold_id` 도 유일) |
| `g_evidence` | 복합 4칸 또는 순번 | (`gold_table`, `gold_id`) · (`silver_table`, `silver_id`) | gold 13표 · silver 38표(둘 다 다형) |

**silver 57표 초안**: §2-2 표의 「키」 = PK · 「FK 칸」 = FK · 「다형 칸」 = FK 없음. 표별 칸 뜻은 `$SM/notes/silver-tables.md` · `silver-schema.json` 이 정본이라 여기에 다시 적지 않는다.

**빌드 · 보조 표(초안 — D-4 · D-8)**: 빌드 기록 1(§3-2) · 빌드 파일 1(파일 이름 · sha256 · 행 수 · 종류 — 지금 `health.files[]` 꼴) · 원장 확인 1(`lck_id`, `code` — 273쌍).

### 2-5. 「담을 칸 없는 값 0」 — 1:1 로 안 맞는 칸 전수

**결론: 칸을 문자열 그대로 옮기면(D-3 (a)) 담을 칸 없는 값은 0 이다** — 모든 값이 CSV 의 한 칸이고 줄바꿈 · NUL · 앞뒤 공백이 0 이라 그대로 들어간다. 아래는 **정규화(타입 · FK · 자식 표)로 가려 할 때** 걸리는 칸이다(§7 셈 ⑧).

**A. 한 칸에 여러 값(` · ` 로 이음) — gold 13칸**

| 표.칸 | 찬 행 | 여러 값 행 | 조각 | 한 칸 최대 | 조각 ↔ silver 사전 이름 | 허브가 쪼개 쓰나 |
|---|---:|---:|---:|---:|---|---|
| `g_profile.materials` | 486 | 94 | 608 | 4 | `material` 이름과 안 맞는 조각 0 | 쪼갬(`headers.py:77`) |
| `g_profile.methods` | 159 | 11 | 170 | 2 | `method` 와 안 맞는 조각 0 | 쪼갬 |
| `g_profile.organizations` | 263 | 203 | 575 | 6 | 조각이 전부 `이름(역할)` 꼴 — B | 안 쪼갬 |
| `g_profile.modality_code` | 739 | **2** | 741 | 2 | **코드 칸인데 두 값** — 2행 다 제품 | 안 쪼갬 |
| `g_profile.modality_name` | 739 | 2 | 741 | 2 | `modality` 와 안 맞는 조각 0 | 안 쪼갬 |
| `g_indication.conditions` | 54 | 12 | 72 | 4 | 대조 안 함(조건 글) · 칸 안 중복 조각 행 4 | 안 쪼갬 |
| `g_package.conditions` | 58 | 35 | 93 | 2 | 대조 안 함 · **칸 안 중복 조각 행 35** | 안 쪼갬 |
| `g_offer.quantities` | 163 | 11 | 174 | 2 | 조각 = `수+단위` 꼴 — B | 안 쪼갬 |
| `g_offer.sites` | 93 | 2 | 96 | 3 | `site` 이름과 안 맞는 조각 **59**(상품 이름 속 조각 원문) | 쪼갬 |
| `g_offer.concerns` | 31 | 1 | 32 | 2 | `concern` 과 안 맞는 조각 5 | 안 쪼갬 |
| `g_offer.effects` | 10 | 1 | 11 | 2 | `effect` 와 안 맞는 조각 5 | 안 쪼갬 |
| `g_offer.materials` | 16 | 1 | 17 | 2 | `material` 과 안 맞는 조각 10 | 쪼갬 |
| `g_pair.goal_effects` | 124 | 3 | 127 | 2 | `effect` 와 안 맞는 조각 **43**(목표 글 원문) | 안 쪼갬 |

- 사전 이름 자체에 ` · ` 가 든 것은 0 이라 지금은 쪼개기가 모호하지 않다. 다만 **사전과 안 맞는 조각이 4칸에 있다**(상품 조각 · 목표 글) — 자식 표 + 사전 FK 로 풀면 그 조각은 「담을 칸」 이 없다. 문자열 그대로면 문제없다.
- `g_package.conditions` 는 같은 조각이 한 칸에 두 번 든 행이 35 — 집합으로 바꾸면 값이 달라진다.

**B. 한 조각 안에 두 성질(묶음 값) — gold 3칸**

| 표.칸 | 꼴 | 수 |
|---|---|---:|
| `g_profile.organizations` | `이름(역할)` | 조각 575 전부 |
| `g_adverse.ratings` | `척도=값`(지금은 한 칸에 하나뿐 — 목록 자리) | 34행 |
| `g_offer.quantities` | `수+단위` · 단위만 · `수+단위 글` … 5꼴 | 조각 174 |

silver 에는 이 값들이 이미 풀려 있다(`product_organization` · `adverse_rating` + `rating_scale` · `offer_quantity`).

**C. 다형 참조(표 이름 칸 + 코드 칸) — FK 한 줄로 못 건다**

- gold 12짝: `g_entry.entity_*`(14표) · `g_scope.subject_*` · `holder_*`(5) · `g_profile.subject_*`(4) · `g_indication.target_*` · `candidate_*`(5) · `g_outcome` / `g_adverse` / `g_adverse_detail` / `g_recovery` / `g_contraindication` 의 `target_*` · `g_pair.from_*` · `to_*` · `g_package.item_*` · `g_offer.item_*` · `g_node.node_*` + 되짚기 `silver_table` + `silver_id`(13표) · `gold_table` + `gold_id`(2표).
- silver 15칸(14표): §2-2.
- **한 끝이 빈 행이 있다**: `g_pair.from_table` 빈칸 6 · `to_table` 31 · `g_package.item_table` 47 · `g_offer.item_table` 20(silver `procedure_relation` · `package_item` · `offer_item` 도 같은 수). 빈칸이 「끝 없음」 이라는 값이다.

**D. 묶음 식별자 · 목록 칸(구분자 `|` · ` + `)**

| 표.칸 | 꼴 | 수 |
|---|---|---:|
| `g_entry.silver_id` | `표|코드|이름` 세 조각(`alias` 행 지목) | 831행 |
| `g_evidence.fields` | `(행 전체)|name|name_ko` 1,756행 · `alias` 55행 · 빈칸 25,929행 — 값이 3가지뿐 | 27,740행 |
| `evidence_kind`(15표 전부) | `원장` 60,334 · `원장 + 외부 확인` 1,510 · `외부 확인` 400 — ` + ` 로 두 값 | 62,244행 |

**E. 수 칸**

- 정수 26칸(gold) · 29칸(silver) — `str(int(x)) == x` 가 **전부 성립**(앞 0 · 부호 꼴 없음).
- 소수: `g_adverse.freq_min`(= silver `adverse_frequency.min`) 114값 중 **1값이 float 왕복에서 표기가 달라진다**(끝자리 0 꼴) · `freq_max` 0 · `offer_quantity.amount` 0. `NUMERIC` 은 표기를 지키지만 `float` 는 못 지킨다.
- `price_list.version` 은 수처럼 보이는 판 번호 글자다(1행).

**F. 그 밖**

- 키 없는 표 3(`g_evidence` · `alias` · `source_ref`) — §2-4.
- 예약어 칸 `order` 2.
- 전부 빈 칸: gold 1(`g_adverse_detail.site_name`) · silver 6(`adverse_factor.site_code` · `package.duration_qualifier` · `package_item.role_text` · `rating_scale.min` · `max` · `meaning_text`) + 0행 표 1(`external_code`).
- 글 칸 안의 ` · `(조립 글): `g_profile.description` 166행(한 칸 최대 10조각) · `g_package.text` 32 · `g_offer.item_note` 23 · `g_indication.note` 2 · `g_outcome.note` 2 — 목록이 아니라 이어 붙인 글이다(`$SM/gold/README.md:3` 「이어 붙이기( · )」).

---

## 3. Q3 — 적재 · 빌드 추적

### 3-1. 지금 해시 셈 · 응답 머리

| 무엇 | 어떻게 | 근거 |
|---|---|---|
| 합치는 식 | 「파일 이름 + 공백 + sha256(파일 바이트)」 줄을 이름순으로 `\n` 으로 이어 다시 sha256 | `inputs.py:64-67` — `$SM/gold/gold-check.py:46-50` 과 같은 식 |
| `gold_hash` | gold 폴더의 `*.csv` **전부** — 15표 + 폴더의 다른 CSV(`questions.csv` · 읽지 않고 해시만) = 16 파일 | `inputs.py:107-121,177` |
| `aux_hash` | `source_ref.csv` · `concern.csv` · `adverse.csv` · `condition.csv` · `concern_site.csv` · `ledger-check-list.csv` 6 파일 | `inputs.py:129,144,155,175,178` |
| 기대 해시 | `GOLD_EXPECTED_HASH` 가 있으면 다를 때 시작 실패 · 없으면 경고만 | `inputs.py:179-183` |
| 응답 머리 | 모든 도구 응답에 `build{gold_hash, aux_hash, loaded_at}` | `core.py:108-113` |
| cursor | `gold_hash` · `aux_hash` 앞 32자 + 도구 + 요청 서명 + offset — build 가 다르면 `cursor_invalid` | `cursor.py:25-41` · `core.py:93-106` |
| health | 파일별 `{name, sha256, rows, kind}` · `expected_hash_checked` · `load_ms` · `integrity` 4셈 · 보조 입력 셈 | `service.py:152-166` · `repository.py:24-37` · `memory.py:116-131` |

이 워커가 같은 식으로 다시 셈(§7 셈 ⑨):

- `gold_hash` = `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c` — 시험 상수 `SPEC_GOLD_HASH_1116`(`$H/backend/tests/test_gold_load.py:18`)과 **같다.**
- `aux_hash` = `6435fe41f3851574729ef7aa7e108afb5cf7601c1764c160496a9e49aa1803a3`(6 파일).
- 참고 — silver 57 파일 전체에 같은 식 = `91237618f3886c02a33fc8d6a4ff1cc73173115e498a5693fb6cdd25cb9c9254`(지금 어디에도 기록되지 않는 값 · gold-final-notes 의 silver 해시는 56표 때 값이다).

**DB 로 갈 때 생기는 사실**

1. 해시가 **파일 바이트**에서 나온다 — DB 행에서는 같은 값을 다시 못 낸다(BOM · 따옴표 · 줄 끝이 바이트에 든다). 적재 때 셈한 값을 **기록해 두는 자리**가 있어야 응답 머리 · cursor · health 가 그대로 간다.
2. `gold_hash` 에 **허브가 읽지 않는 `questions.csv`** 가 들어 있다 — 적재기는 15표만 싣더라도 16 파일을 다 봐야 같은 값이 나온다.
3. `aux_hash` 의 6 파일 가운데 `ledger-check-list.csv` 는 silver · gold 가 아니다(`notes/`). 범위를 (b) 로 넓히면 「aux = 6 파일」 과 「DB 에 실린 silver = 57표」 가 어긋난다 — `aux_hash` 식을 그대로 둘지 silver 전체 해시를 더 둘지는 계약(SPEC-001 §2-3 4)이 정한다.

### 3-2. DB 판에서 옮기는 법(D-4)

| | (a) 판 하나 · 전체 교체 + 빌드 기록 표 | (b) 빌드 표 + 표마다 판 칸 | (c) 옆 테이블에 싣고 이름 바꿔치기 |
|---|---|---|---|
| 스키마 | 표 1:1 그대로 + 빌드 기록 1(+ 파일 목록 1) | 73표 전부에 판 칸 · PK = (판, 키) · 인덱스 전부 판 머리 · FK 복합 | 표 두 벌 |
| 재적재 | 한 트랜잭션에서 지우고 다시 넣기(12만 행 · 12MB) | 새 판 행을 더 쌓고 발행 포인터를 옮김 | 다음 판 싣고 rename |
| 되돌리기 | **옛 CSV 묶음을 다시 싣는다** — 묶음 보관 자리 필요 | 포인터를 옛 판으로 | 옛 벌이 남아 있으면 rename |
| stg ↔ 로컬 같은 판 확인 | 빌드 기록의 `gold_hash` · `aux_hash` + 표별 행 수 | 같음(발행된 판의 값) | 같음 |
| 조회 | 지금과 같음 | 모든 조회에 판 조건 | 지금과 같음 |
| 허브 전례 | `legacy_prod_document`(경로 PK + `sha256` 칸 — 통째 교체형) | `publication_content_release`(published 하나 · 부분 유일 인덱스) · 옛 PR #31 `gold_build` + `gold_publication` | 없음 |
| 위험 | DB 안에 옛 판 없음 · 적재 도중 실패는 트랜잭션으로 막아야 | 스키마가 2배로 복잡 · 옛 판이 한 방식(§5) | 실행 중 DDL · `alembic check` 와 어긋남 |

- **메모리 판과의 어긋남**: D-6 (a)(시작 때 읽기)이면 DB 를 다시 실어도 떠 있는 허브는 옛 판을 들고 있다. 지금 계약도 「gold 가 바뀌면 재시작」 이다(SPEC-001 §2-3 1). 재적재 = 적재 → 재시작 → `health.build` 확인이 한 절차가 된다.
- **같은 판 확인을 내용으로도 하려면**: 허브에 표 내용 해시 전례가 있다 — 행을 JSON 으로 정규화해 행별 sha256 을 정렬 · 이어 다시 sha256(`prod-migration.md:114-117`). 파일 해시와는 다른 값이지만 「DB 에 실제로 든 것」 을 stg ↔ 로컬로 견줄 수 있다(선택지로만).
- **빌드 기록에 둘 것(초안)**: `gold_hash` · `aux_hash` · 적재 시각 · 적재기 판 · 표별 행 수 · 파일별 sha256 · (D-1 (b) 면) silver 전체 해시. 지금 `LoadRecord`(`repository.py:24-37`)의 칸이 그대로 후보다.

### 3-3. 원천 CSV 를 어디서 가져와 싣나(D-5)

지금: `$SM`(프로필 레포 워크트리 안 · **gitignore · 로컬에만**). 크기 — gold 15표 6.4MB · silver 57표 5.9MB(그중 `source_ref` 4.2MB) · `ledger-check-list.csv` 포함 보조 6 파일 4.6MB(§7 셈 ⑨).

| 선택지 | 전례 | 걸리는 것 |
|---|---|---|
| (a) VM 디렉터리 + 일회성 컨테이너 적재 CLI | corpus 반입(`deployment.md:460-475`) | 사람이 파일을 VM 으로 옮긴다 · CLI 를 이미지에 넣을지는 문서가 「팀 결정」 으로 둠(`deployment.md:462-463`) |
| (b) 허브 레포에 커밋(`backend/import-data/`) | 매핑 등록부 1 파일(20K)만 있음 — **데이터 본체 전례 없음** | 회사 레포(비공개 여부는 이 조사로 **확인 안 됨** — 외부 호출 금지) · git 이력에 영구히 남음 · `.dockerignore:2-12` · `Dockerfile:13-22` 수정 · SPEC-001 §2-1 「레포에 CSV 를 커밋하지 않는다」 와 어긋남 |
| (c) alembic 데이터 마이그레이션 | 없음(지금 마이그레이션은 schema 만) | (b) 의 전부 + 컨테이너 시작이 적재를 기다림 · 판을 바꿀 때마다 마이그레이션 |
| (d) 로컬 DB → `pg_dump --data-only` → stg `pg_restore` | baseline 데이터 반입(`deployment.md:279-281,323-329`) | dump 파일도 회사 데이터 — 보관 자리는 (a) 와 같다 · 해시는 로컬 적재 때 기록된 값이 따라간다 |
| (e) 바깥 저장소(오브젝트 스토리지 등) | **확인 안 됨**(허브 코드 · 문서에서 쓰는 곳을 못 찾음) | 접근 키 · 네트워크가 새로 필요 |

- **금지 확인**: 공개 레포 `kknaks_profile` · `clinic_chat` 에는 못 둔다(브리프 §4 Q3). `$SM` 이 프로필 워크트리 안에 있지만 gitignore 라 지금은 로컬 파일일 뿐이다.
- 원장 확인 목록은 글 칸이 든 원본 대신 **id · 코드만 뽑은 것**을 보낼 수 있다(SPEC-001 §8 O-8 이 이미 적어 둔 선택지) — 단 `aux_hash` 는 원본 바이트로 셈한다(D-8 위험).

---

## 4. Q4 — repository 교체 자리

### 4-1. 인터페이스 · 쓰는 곳 전수

`GoldRepository` Protocol(`modules/gold/repository.py:40-77`) — 메서드 29 · **전부 동기(`def`)** · 돌려주는 행 = 읽기 전용 `Mapping[str, str]` · 순서 = CSV 파일 순서(`repository.py:5`). 쓰는 곳은 `grep -rn "repo\.<이름>(" app/modules/gold app/router/gold.py`(§7 셈 ⑩).

| 메서드 | 메모리 색인(`memory.py`) — 칸 | 앱에서 부르는 곳 |
|---|---|---|
| `entries_by_norm` | `g_entry` (`norm`) `:45` | `resolve.py:74` |
| `entry_norms` | `norm` 서로 다른 값 2,541 `:46` | `resolve.py:70` — **전부 훑어** 문장 안 부분 일치 |
| `entries_by_entity` | (`entity_table`, `entity_code`) `:47` | `facets.py:119,270` · `concern.py:39` · `coverage.py:53,65` |
| `entries_by_table` | (`entity_table`) `:48` | `resolve.py:109` · `concern.py:136` |
| `scope_by_subject` | `g_scope` (`subject_table`, `subject_code`) `:49` | `service.py:71` · `pairs.py:54` · `coverage.py:51,68` · `facets.py:117` · `closure.py:45,71` |
| `scope_by_holder` | (`holder_table`, `holder_code`) `:50` | **0**(시험에서도 0) |
| `profile_of` | `g_profile` (`subject_table`, `subject_code`) `:51` | `facets.py:205,215` |
| `rows_by_target` | 6표 (`target_table`, `target_code`) `:52` | `facets.py:208,221` |
| `rows_by_value` | (표, 칸) 12짝 `:20-27,53` | `pairs.py:115` · `concern.py:107` · `facets.py:213,217,252` |
| `rows_by_attr` | 속성 맞춤 칸 — 3칸은 ` · ` 로 쪼갠 조각 단위 `:67-77` | `facets.py:274` |
| `rows_all` | 표 전체 `:36` | `facets.py:177`(`g_offer` 163행에서 이름 부분 일치) |
| `distinct_values` | 처음 부를 때 셈해 둠(`repository.py:141-145`) | `pairs.py:43,46` · `service.py:65,83` · `facets.py:105` |
| `pair_by_from` · `pair_by_to` | `g_pair` (`from_*`) · (`to_*`) `:54-55` | `pairs.py:78` |
| `package_by_item` · `offer_by_item` | (`item_table`, `item_code`) `:56-57` | `pairs.py:110` · `facets.py:220` / `facets.py:211` |
| `node` | `g_node` 키 `:37` | `service.py:90,97` |
| `edges_out` · `edges_in` | `g_edge` (`src`, `edge_type`) · (`dst`, `edge_type`) `:58-59` | `service.py:94` |
| `row_by_gid` | 14표 키 `:37` | `service.py:133` |
| `evidence_of` | `g_evidence` (`gold_table`, `gold_id`) `:60` | `service.py:136` |
| `source_refs_of` | `source_ref` (`target_table`, `target_id`) + `fields` 거르기 `:61-64,108-114` | `service.py:137` |
| `parent_of` · `ancestors` · `descendants` | 계층 3표 `code → parent_code` · 자식 목록 `:80-88` · 걷기는 `repository.py:185-204` | `concern.py:119,127` · `facets.py:196` · `concern.py:140` |
| `ledger_ids` | 코드 → `lck id[]` `:104` | `ledger.py:21` |
| `concern_site_by_site` | `site_code → (concern_code, id)[]` `:91-99` | `concern.py:139` |
| `sites_of_concern` | `concern_code → site_code[]` `:100` | **0**(시험 `test_gold_holes.py` 만) |
| `load_record` | 적재 기록 | `service.py:153` · `core.py:97,105,109` |

구현체에 직접 기대는 곳: `service.py:22,34`(기본 factory 가 `CsvMemoryGoldRepository` — **`repository_factory` 인자로 갈아 끼울 수 있게 이미 열려 있다**) · 시험 `test_gold_load.py`(13곳) · `test_gold_holes.py`(5곳) · **`test_gold_load.py:121` 은 `repo._m`(내부 색인)을 직접 본다.**

메모리에서 미리 지어 두는 것

| 무엇 | 언제 | 자리 |
|---|---|---|
| 색인 dict 약 40개(위 표) | 적재 때 한 번 | `memory.py:36-65` |
| 속성 맞춤 색인(조각 단위) | 적재 때 | `memory.py:67-77` |
| 계층 자식 목록 | 적재 때 | `memory.py:80-88` |
| `integrity` 4셈 | 적재 때 | `memory.py:116-131` |
| **하위 닫힘(closure)** | **요청 때** — 너비 우선으로 `scope_by_subject` 를 되풀이 | `closure.py:49-84` |
| 계층 조상 · 자손 | 요청 때 걷기(깊이 최대 2) | `repository.py:185-204` |
| resolve 부분 일치 | 요청 때 `entry_norms` 2,541개를 전부 훑음 | `resolve.py:68-70` |

### 4-2. 한 요청이 repository 를 부르는 횟수(§7 셈 ⑪)

- `g_scope`: subject 858 · subject 당 행 최대 84(중앙 4).
- **하위 닫힘 한 번**: holder 최대 **156** · `scope_by_subject` 호출 최대 **157** · 깊이 최대 2 · holder 100 넘는 subject 2(계열). 시술은 최대 53.
- `pair` 는 그 holder 마다 `pair_by_from` + `pair_by_to` 를 한 번씩 더 부른다(`pairs.py:76-78`) — 계열 하나를 물으면 157 + 2 × 157 안팎. `facets` 도 holder 마다 `rows_by_target` 류를 부른다(`facets.py:201-221`).
- 지금은 전부 dict 조회라 셈이 무의미하지만 **「호출 하나 = SQL 하나」 로 옮기면 요청 하나가 수백 쿼리**가 된다.

### 4-3. 바꾸는 방식(D-6)

| | (a) 시작 때 DB → 메모리 색인 그대로 | (b) 요청마다 SQL | (c) (a) + 닫힘 · 계층을 빌드 때 테이블로 |
|---|---|---|---|
| 바뀌는 코드 | 새 repository 구현 1 + 적재부(`read_inputs` 자리에 DB 읽기) · Protocol · service · 도구 · MCP 그대로 | Protocol 이 async 가 되고 **service · closure · facets · pairs · concern · coverage · resolve · router · MCP 전부** async 로(지금 router 는 일부러 `def` — `router/gold.py:5`) · 또는 동기 드라이버를 새로 들임 | (a) + gold 에 없는 표가 생김 |
| DB 접근 | lifespan 에서 한 번(async 로 읽어 dict 로) | 요청마다 수백 번 → 묶음 조회(IN · 조인 · 재귀 CTE)로 다시 짜야 | 한 번 |
| 응답 속도 | 지금과 같음(요청은 메모리만) · 시작만 느려짐 | **확인 안 됨**(DB 를 띄우지 않았다) — 호출 수로는 쿼리 왕복 × 수백이 더해진다. `entry_norms` 훑기 · `rows_all` 은 SQL 로 바꾸면 꼴이 달라진다(부분 일치 방향이 「문장 안에 norm」 이다) | 지금과 같음 |
| 순서 보장 | 읽을 때 키(또는 순번)로 정렬하면 지금과 같음 | 쿼리마다 `ORDER BY` | 같음 |
| 메모리 | 지금과 같음(12만 행 · CSV 12MB) | 줄어듦 | 같음 |
| 위험 | DB 가 「조회 엔진」 이 아니라 「보관함」 이 된다 · 재적재 뒤 재시작 필요 | 재작성 범위가 코어 전체 · 「같은 입력 = 같은 응답」 을 다시 증명해야 함(시험 137) | 닫힘 표는 gold 15 밖 — 「gold 불변 · 허브가 관계를 만들지 않는다」(`closure.py:12`)와 부딪힌다 |

- 속도 기준선: 「gold + Jev 0.7s」 는 Jev 호출을 낀 값이다(`$W/_RESUME.md:21,142` · Jev 중앙 171ms `:53`). **허브 도구만의 응답 시간은 이 조사에서 재지 않았다**(서버를 띄우지 않음) — 응답에 `Server-Timing` 머리가 있어 잴 수는 있다(`gold_main.py:58-64`).
- 시작 시간: 이 워커의 순수 CSV 읽기(gold 15 + `source_ref`)는 146ms 였다(§7 셈 ⑨ · 색인 짓기 제외). DB 에서 11만 행을 읽는 시간은 **확인 안 됨** — 쿼리 제한 15s(`core/config.py:53`)가 표 하나 읽기에 걸리는지는 재 봐야 한다.
- (a) 에서 계층 3표를 통째 싣더라도 메모리에는 2칸만 둔다는 규칙(SPEC-001 §2-1 X2)은 「읽을 칸을 2칸만 고르는 쿼리」 로 그대로 지킬 수 있다.

### 4-4. 기존 시험이 DB 판에서 도는 법

`$H/backend/tests/test_gold_*.py` 8 파일 · 시험 함수 137(holes 38 · synthetic 36 · coverage 18 · real 17 · load 13 · contract 6 · rest 5 · mcp 4) + `gold_fixture.py`(319줄 — 가짜 코드 · 가짜 이름으로 15표 + 보조 파일을 `tmp_path` 에 CSV 로 씀) · `gold_support.py`(실물 env 없으면 skip).

| 시험 묶음 | 지금 기대는 것 | DB 판에서 |
|---|---|---|
| 도구 계약(synthetic · holes · coverage · contract · rest · mcp — 107) | `GoldState(write_fixture(tmp_path))` → CSV 메모리 | **선택지 ①** fixture 가 만든 같은 행을 SQLite 메모리 DB 에 넣고 DB repository 로 같은 시험을 한 번 더(factory 를 매개변수로 — `service.py:34`) · **선택지 ②** CSV 판을 시험 대역으로 남기고 DB 판은 「두 repository 가 같은 메서드에 같은 행을 내는지」 만 대조 |
| 적재(load 13 · holes 일부) | env 없음 · 파일 없음 · 헤더 다름 · 해시 다름 → 시작 실패 | 대부분 **적재기(CLI) 시험으로 옮겨 간다** — DB 판의 시작 실패 조건(빌드 기록 없음 · 해시 다름)은 새로 정해야 한다 |
| 실물(real 17 · load 일부) | 로컬 실물 CSV env · `questions.csv` | 실물을 실은 DB 가 있어야 — CI 에는 없다(지금도 skip) |
| `test_gold_load.py:121` | `repo._m` 내부 색인 | 구현에 묶여 있어 DB 판에서는 그대로 못 돈다 |

- CI 의 pytest 는 SQLite(`backend-test.yml:76-80`) — DB repository 가 **SQLite 에서도 돌아야** CI 에서 시험된다(PostgreSQL 전용 SQL · 타입을 쓰면 CI 에서 못 돈다).
- 시험은 동기 함수 + `asyncio_mode = "auto"`(`pyproject.toml:30`) · DB 는 async 엔진뿐이라 「DB 에서 읽어 메모리로」 한 번만 async 면 나머지 시험 본문은 그대로다.
- 빈 PostgreSQL 에서의 마이그레이션 검증은 CI 가 이미 한다(`backend-test.yml:66-70`) — 새 테이블도 자동으로 그 검증에 든다.

---

## 5. Q5 — 옛 판(PR #31)과 대조

**기록 확인**: `$P/orchestration/work/phub-recommend/_RESUME.md` 에 「11-08」 날짜가 붙은 결정 행은 **없다**(`grep -n "11-08"` 0건 — 같은 폴더에서는 `silver-proc-dryrun-brief.md:1` 한 줄뿐). 브리프가 가리킨 「11-08 중단 · ERD 바탕 틀림」 문장은 **확인 안 됨.** 아래는 실물로 확인한 것만이다.

| # | 옛 판에서 본 것 | 근거 | 새 안이 확인할 것 |
|---|---|---|---|
| 1 | **허브가 gold 를 직접 지었다** — 규칙 G1~G22 를 허브 코드로(`build.py` 1,415줄 · `pairs` · `facts` · `ids`) | `git show origin/kknaksss/phub-recommend:backend/app/modules/gold/build.py:1-8` · SPEC-001 §7 「빌드 — 버림 · 허브는 적재만」 | 적재기 · repository 에 **값을 만들거나 바꾸는 줄이 0** 인지 — 실은 행 수 = CSV 행 수 · 칸 값 = CSV 값(되읽어 대조) |
| 2 | **값을 JSON 칸에 넣었다** — `attrs` · `flags` · `evidence` · `source_refs` · `resolved` · `payload` · `variants` · `targets` … 표 8개 중 7개에 JSON 칸 17개(뒤 마이그레이션이 1개 더) | `…/alembic/versions/b202610300001_gold_schema.py:32-129`(`sa.Column(… _JSON` 17줄) · `b202610310001_gold_fact_attached.py:28` | 새 테이블에 **JSON 칸 0** — CSV 칸 하나 = 테이블 칸 하나. 여러 값 칸(§2-5 A)을 JSON 배열로 바꾸지 않았는지 |
| 3 | **노드 · 엣지 + 속성 덩어리가 저장 꼴이었다**(`gold_node` · `gold_edge` · `gold_fact`) — 관계형 표가 아니라 그래프가 원본 | 같은 파일 `:57-109` | 11-16 결정 「관계형 먼저 + 그래프 내보내기」(`$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/_RESUME.md:450` · `$SM/gold/semantic-map.md` §7-4) 그대로 — `g_node` · `g_edge` 는 내보내기 표일 뿐 속성은 12 속성 표에 있는지 |
| 4 | **빌드 번호로 쌓았다** — 표 5개(`gold_node` · `gold_edge` · `gold_global` · `gold_fact` · `gold_dictionary`)의 PK 가 (`build_id`, 키) · 그 인덱스가 전부 `build_id` 머리 · 발행 포인터 표 따로 | `…/b202610300001_gold_schema.py:68,88,99,111,124` · `…/app/model/gold.py:55-56,60-61,75-79,140` | D-4 를 (a) 로 정했다면 판 칸이 **어느 표에도 없는지** · (b) 로 정했다면 그 비용을 알고 고른 것인지 |
| 5 | **입력 원문을 DB 에 통째로 넣었다**(`gold_source_snapshot.body` JSON) | `…/b202610300001_gold_schema.py:32-39` | 원천 CSV · 원장 원문을 DB 칸에 통째로 넣지 않는지(해시 · 행 수만 기록) |
| 6 | **revision id 가 지금 release 헤드와 같은 글자** — 옛 `b202610300001` = `gold_schema`(down `b202610260001`) · 지금 release `b202610300001` = `legacy_prod_documents`(down `b202609030001`) | 옛: 같은 파일 `:18-19` · 지금: `$H/backend/alembic/versions/b202610300001_legacy_prod_documents.py:10-11` | 새 revision id 가 옛 브랜치 3개(`b202610260001` · `b202610300001` · `b202610310001`)와 다른지 · **옛 브랜치로 올린 로컬 DB**(`gold_*` · `graph_*` 테이블이 있고 `legacy_prod_document` 가 없는 DB)에 새 마이그레이션을 돌리지 않는지 — 빈 DB 에서 `upgrade head` 로 확인 |
| 7 | **인덱스 이름을 규칙에 맡기면 겹친다**(옛 모델 머리 주석 — 규칙이 첫 칸만으로 이름을 정함) | `…/app/model/gold.py:3-5` | 새 모델의 인덱스 · 제약 이름을 직접 지었는지 — `(subject_table, …)` 꼴 복합 인덱스가 많다(§2-4) |
| 8 | **ERD 를 값이 아니라 틀에서 지었다** — 프로필 쪽 기록: 「연결 관계부터 생각하다 꼬였다 — 개체 먼저, 관계는 나중」 · 그 뒤 새 판은 시범마다 「담을 칸 없는 값 0」 으로 닫았다 | `…/phub-ledger-redesign/_RESUME.md` §2 의 11-10 「계열 설계는 연결 관계 없이」 행 · `:419,421`(담을 칸 없음 227 → 0) | 테이블 정의를 **실제 값으로 실어 본 뒤** 동결하는지 — 이번 셈에서 1:1 문자열이면 0(§2-5) · 정규화하면 걸리는 칸 목록을 SPEC 에 그대로 싣는지 |
| 9 | **발행본이 없어도 경고만 하고 떴다** | SPEC-001 §2-3 5 「그 동작은 가져오지 않는다」 | DB 판에서 빌드 기록이 없거나 해시가 다를 때 **시작 실패**인지(지금 계약 유지) |

---

## 6. 확인 안 된 것(모음)

| # | 무엇 | 왜 |
|---|---|---|
| 1 | 별도 스키마가 `alembic check` · SQLite 시험에서 실제로 어떻게 되는지 | DB 를 띄우지 않았다(브리프 §7) — 코드 · 일반 동작으로만 적음 |
| 2 | stg DB 역할의 권한(`CREATE TABLE` · `CREATE SCHEMA`) | 접속 금지 |
| 3 | prod DB 이름 전환(`prod-db-rename.md`)이 끝났는지 · 지금 stg / prod 의 실제 revision | 문서만 읽음 · fetch 금지(마지막 FETCH_HEAD 11-16) |
| 4 | DB 판의 응답 시간 · 시작 시간 | 서버 · DB 를 띄우지 않음 |
| 5 | 허브 레포가 비공개인지 · 바깥 저장소를 쓰는 곳이 있는지 | 외부 호출 금지 · 코드 · 문서에서 못 찾음 |
| 6 | `phub-recommend/_RESUME.md` 의 「11-08 중단」 기록 | grep 0건 |
| 7 | 마이그레이션에만 있고 모델에 없는 테이블을 `alembic check` 가 잡는지 | 돌려 보지 않음(alembic 일반 동작으로 적음) |
| 8 | SPEC-001 §10 의 열린 것 가운데 O-7(진입점) · O-8(stg 데이터) · O-11(접근 제어) | 그대로 열려 있음 — 이번 조사는 DB 만 |

## 7. 셈 명령과 결과

전부 `python3`(표준 라이브러리 `csv` · `json` · `hashlib`) · `grep` · `git`(읽기 명령)이다. CSV 는 `encoding='utf-8-sig'` · `newline=''` 로 읽었다. 스크립트는 세션 scratchpad 에만 두었다.

| # | 무엇 | 명령 꼴 | 결과 |
|---|---|---|---|
| ① | 테이블 이름 대조 | `$H/backend` 에서 `re.findall('__tablename__ = "…"')`(app/model) · `re.findall("op.create_table('…'")`(alembic/versions) · `os.listdir($SM/silver)` · `$SM/gold/g_*.csv` 의 교집합 | 모델 167 · 마이그레이션 167 · 차집합 0 / 0 · silver ∩ 기존 = `modality` · `product` · gold ∩ 기존 = 0 · silver 이름을 머리로 갖는 기존 39 |
| ② | 브랜치 차이 | `git -C $H log --oneline origin/release/v1.2.0..origin/stg`(5줄) · `origin/stg..origin/release/v1.2.0`(2줄 — `3750e4c` · `6b986c4`) · `git diff --quiet origin/{stg,prod} origin/release/v1.2.0 -- backend` · `git ls-tree --name-only origin/{stg,prod} backend/alembic/versions/` | backend 같음(둘 다) · 차이 파일 = `docs/guides/prod-db-rename.md` · versions 2 파일씩 |
| ③ | SQLite `create_all` | `grep -rn "create_all" backend/tests backend/app` | 시험 20 파일 20줄 · app 0 |
| ④ | silver 키 · FK | `silver-schema.json` 의 `key` · `fk` 로 57표를 돌며 키 유일 · FK 값 ∈ 대상 키 | 키 중복 0 · FK 칸 80 · 깨진 FK 0 · 키 없는 표 2 · `source_ref` → silver 못 찾음 0 |
| ⑤ | 표별 행 · 칸 · 값 종류 | 57 + 15 파일을 `csv.reader` 로 읽어 칸마다 찬 값 · 빈칸 · 타입(정규식 정수 / 소수) · 최대 바이트 · 서로 다른 값 · 구분자(` · ` `;` `|`) | silver 57표 66,936행 387칸 · gold 15표 62,244행 278칸 · 헤더와 칸 수 다른 행 0 · §2-1 · §2-2 표 |
| ⑥ | 이름 길이 | `fk_<접두어><표>_<칸>_<접두어><대상>` 을 FK 80칸에 | 접두어 없음 최대 59 · `s_` 63 · `silver_` 73(63 넘는 것 2) · 표 이름 최대 25자 |
| ⑦ | 예약어 | 칸 · 표 이름을 PostgreSQL 예약어 목록과 대조 | 칸 2(`order`) · 표 0 |
| ⑧ | 여러 값 칸 쪼개기 | gold 칸을 ` · ` 로 나눠 조각 수 · 한 칸 최대 · 칸 안 중복 · silver 사전 `name_ko` / `name` 과 대조 · 조각 꼴은 글자를 가려(`X`) 셈 | §2-5 A · B · D |
| ⑨ | 해시 · 크기 | `sha256(파일 바이트)` → 「이름 + 공백 + sha256」 이름순 `\n` 이음 → sha256 · `os.path.getsize` · `time.perf_counter` | `gold_hash` `8accbb21…f6228c`(16 파일) · `aux_hash` `6435fe41…1803a3`(6 파일) · silver 57 `91237618…9c9254` · gold 15 = 6,396,917B · silver 57 = 5,872,513B(`source_ref` 4,153,182B) · 보조 6 = 4,628,394B · CSV 읽기 146ms |
| ⑩ | repository 쓰는 곳 | 메서드 29개마다 `grep -rn "repo\.<이름>(" app/modules/gold app/router/gold.py --include=*.py`(repository.py 제외) · 시험은 `grep -rl "\.<이름>(" tests` | §4-1 표 · 앱 호출 0 인 메서드 2 |
| ⑪ | 닫힘 호출 수 | `g_scope` 를 (`subject_table`, `subject_code`) 로 묶어 「하위 *」 role 3개만 따라 너비 우선(= `closure.py:49-84`) | subject 858 · subject 당 행 최대 84 · holder 최대 156 · 호출 최대 157 · 깊이 최대 2 |
| ⑫ | 원장 확인 · 계층 | 추출식 `\b(CON\|PRD\|PRC\|CAS\|OFR\|ADV\|CND\|EFF\|SITE)-\d+\b` 를 3칸 이음에 · 계층 3표 `parent_code` 걷기 | 325행 · 코드 든 행 251 · 코드 218 · 쌍 273(SPEC-001 §2-1 X6 과 같음) · 계층 깊이 최대 2(3표 모두) · 뿌리 17 / 15 / 15 |
| ⑬ | 근거 닿는 범위 | `g_evidence.silver_table` 서로 다른 값 · gold `silver_table` 칸 · `source_ref` 를 (`target_table`, `target_id`) 로 대조 | `g_evidence` 가 닿는 silver 표 38(+ `g_entry` 의 `alias` = 39) · 닿는 silver 행 16,157 · 그 `source_ref` 44,807 / 48,094 · 안 닿는 3,287 · gold 가 안 닿는 silver 18표 49,419행 |
