---
type: work
id: WORK-010
title: "허브 로컬 DB 화 구현 계획 — 확인(지연 FK · load_seq · 시간) · 계약 상수 · 모델 74 · alembic 1 · 적재 CLI · DB 판 repository · 시험 DT1 ~ DT15 · DE1 ~ DE8"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md (0.1.0 · 검수 PASS — FAIL 0 · WARN 4 · NOTE 8 · review-spec-003.md) ← 계약"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 — 「SPEC-003 U-1 (a)」 빈칸 NULL + FK 82 · 「SPEC-003 U-2 (a)」 Docker postgres:16 · 127.0.0.1:18432 · 「SPEC-003 검수 뒤 코디」 W-1 ~ W-4 · 「DB 화 이번 목표 = 로컬 허브 DB 까지」 · 「Procedure Hub 데이터는 공개 정보」)"
  related:
    - "orchestration/work/phub-gold-jev/review-spec-003.md (WARN 4 · NOTE 8 — 이 문서 §10)"
    - "orchestration/work/phub-gold-jev/research-db.md (사실 · 셈)"
    - "orchestration/work/phub-gold-jev/WORK-007-hub-v052.md (앞 허브 WORK — 공통 규칙의 꼴)"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.6.0 — 도구 계약 · 이번에 안 바뀐다)"
---

# WORK-010 — 허브 로컬 DB 화 구현 계획

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터) · `H` = `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · HEAD `85c28af` · **이 위에 이어서 짓는다**) · `B` = `$H/backend`.
> **계약은 SPEC-003 0.1.0 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작을 만들지 않는다 — 어긋나는 것을 찾으면 코드를 맞춰 고치지 말고 보고한다(§11).
> **사용자 결정은 닫혔다**(_RESUME §2 11-17): **U-1 = (a)** CSV 그대로 · 빈칸만 NULL · FK 82 / **U-2 = (a)** Docker `postgres:16` · `127.0.0.1:18432`(코디가 이미 띄웠다 · 새 빈 DB). 검수 WARN 4 는 코디가 정했다(같은 표 「검수 뒤 코디」 행) — §10 에 한 줄씩 받았다.
> 11-17 결정으로 Procedure Hub 데이터(원장 · silver · gold)는 공개 정보다 — 이 문서 · 시험 · fixture 에 「데이터 본문 0」 제약을 걸지 않는다. **비밀값 · 접속 문자열 · 내부 URL 금지는 그대로다.**

## 0. 요약

- 만드는 것 넷: ① **계약 상수(silver) + 모델 74 + alembic 1** ② **적재 CLI**(로컬 CSV → 로컬 DB · V1 ~ V10 + 검수로 더한 검사 둘 · L1 ~ L6 · dry-run · exit 0 / 2 / 3) ③ **DB 판 repository**(시작 때 한 번 읽어 **같은 `LoadedInputs` → 같은 `GoldMemory`** · `GOLD_REPOSITORY` 기본 `csv`) ④ **시험** DT1 ~ DT15(합성 · SQLite · CI) · DE1 ~ DE8(로컬 실물).
- **도구 계약 · 응답은 안 바뀐다.** `health` 에 새 필드를 넣지 않는다(W-1 (a)). `service.py` 의 도구 9 · `router/gold.py` · `mcp_server.py` · `swagger_docs/gold.py` 는 **한 줄도 안 고친다**.
- WP 다섯: **WP-0 확인**(지연 FK · `load_seq` · 기준선 시간 — 코드 레포에 남기는 것 0) → **WP-1** 계약 상수 · 모델 · 마이그레이션 → **WP-2** 적재 CLI · 합성 fixture(silver 57) → **WP-3** DB 판 repository · 설정 · lifespan → **WP-4** 로컬 실물 확인(DE1 ~ DE6 · DE8) · 문서 · 마감.
- **완료 조건의 마지막 줄(DE7 — 18105 를 DB 판으로 바꿔 앱 37 키 대조)은 코디 몫이다.** 워커는 18107 에 DB 판을 띄워 18105(CSV 판 · 코디 것)와 **나란히** 대조(DE6)까지 한다. 워커는 18105 · 18220 · 18210 · 18005 를 내리거나 띄우지 않는다(§8).

## 1. 지금 코드(11-17 확인 — `$B` · HEAD `85c28af` · 읽기만)

| 파일 | 지금 | 이번에 |
|---|---|---|
| `app/modules/gold/inputs.py`(197줄) | `FileRecord`(`:41-46`) · `LoadedInputs`(`:49-61`) · `combined_hash`(`:64-67` — 파이썬 `sorted`) · `_read_bytes`(`:70-73`) · `_parse`(`:76-91`) · `read_inputs`(`:100-197`) = 읽기 + 헤더 대조 + 해시 + 기대 해시를 한 함수에서 · 원장 코드 추출식(`:37-38` · `:169`) | WP-2 — 적재기가 `_parse` · `combined_hash` · `LEDGER_CODE_RE` · `FileRecord` 를 **가져다 쓴다**(식 두 벌 금지 — SPEC §2-4). 이름에서 `_` 를 떼어 공개하는 것 말고 동작은 안 바꾼다 |
| `app/modules/gold/headers.py`(124줄) | `GOLD_HEADERS`(`:6-41` — 15표 헤더) · `KEY_COLUMN`(`:46`) · `SOURCE_REF_HEADER`(`:48`) · `HIERARCHY_*`(`:57-58`) · `CONCERN_SITE_*`(`:60-61`) | WP-1 — 그대로 읽는다(gold 계약의 원천) |
| `app/modules/gold/config.py`(54줄) | `GoldSettings` — `envs/.env.gold` 또는 프로세스 env(`:24-29`) · 필수 넷 `REQUIRED_ENV`(`:19`) · 빈 선택 값 = 미설정(`:20-21` · `:48-54`) | WP-2 · WP-3 — 새 칸 셋(`GOLD_REPOSITORY` · `GOLD_SILVER_DIR` · `DATABASE_URL`) |
| `app/modules/gold/repository.py`(219줄) | `LoadRecord`(`:24-37`) · Protocol 29 메서드(`:40-77`) · `CsvMemoryGoldRepository.__init__` 이 `read_inputs` 를 **생성자 안에서** 부르고 `GoldMemory` · `LoadRecord` 를 세운다(`:83-102`) | WP-3 — 「입력 읽기」 와 「색인 세우기」 를 가른다(SPEC P2). Protocol 은 그대로 |
| `app/modules/gold/service.py`(170줄) | `RepositoryFactory`(`:28`) · `GoldState.__init__(settings, repository_factory=CsvMemoryGoldRepository)`(`:34`) · `load()` 동기(`:39-40`) · `health`(`:152-166`) | WP-3 — `GoldState` 만(읽은 입력을 받아 세우는 길 하나). **`GoldToolService` · `health` 는 안 고친다** |
| `app/modules/gold/container.py`(16줄) | `gold_state = Singleton(GoldState, settings=settings)`(`:15`) | 안 고친다(예상) |
| `app/modules/gold/memory.py`(131줄) | `GoldMemory(inputs)` — 색인 · `integrity` | **안 고친다**(P2 — DB 판용으로 다시 쓰지 않는다) |
| `app/gold_main.py`(72줄) | lifespan 에서 `container.gold_state().load()`(`:32-37`) · 모듈 끝에서 `create_gold_app(GoldSettings())`(`:72`) | WP-3 — lifespan 이 `db` 판이면 DB 에서 읽는다(async) |
| `app/model/`(파일 60) | `Base` · 이름 규칙(`base.py:8-14`) · `__init__.py` 가 전 모델을 import(마지막 줄 `:205` `legacy_prod`) · `__tablename__` 167 | WP-1 — 새 `medallion.py` + import 한 줄 |
| `alembic/` | `env.py` 가 `app.core.config.settings.DATABASE_URL` 을 읽는다(`:10` · `:18-20`) — 그 설정은 `envs/.env` + 프로세스 env(`app/core/config.py:40-47`) · `alembic.ini:89` 는 자리 표시 URL · versions 2 파일 · 헤드 `b202610300001`(`…legacy_prod_documents.py:10-11`) | WP-1 — 새 revision 파일 1. **`env.py` · `alembic.ini` 는 안 고친다** |
| `scripts/` | 운영 CLI 전례 `import_legacy_corpus.py`(exit 0 / 2 — `:13` · 접속 대상을 비밀번호 가려 찍는다 `:114`) · `scripts/__init__.py` 있음(시험이 `from scripts.… import` 한다) | WP-2 — 새 `load_medallion.py` |
| `tests/` | gold 시험 8 파일(2,563줄) · `gold_fixture.py` `write_fixture`(`:288-305`) 가 silver 폴더에 **5 파일만** · 계층 3표를 **5칸 헤더**로 쓴다(`:298-300` — 실제 silver 는 7 ~ 8칸) · `settings_for`(`:308-319`) · `gold_support.py` 실물 판정(`:22-30`) · `real_settings`(`:36-40`) · `real_state`(`:43-47`) · `create_all` 28 파일 | WP-2 — 새 fixture(silver 57 · 계약 헤더) / WP-3 — 두 판 매개변수화 |
| `.github/workflows/backend-test.yml` | 제한 15분(`:33`) · `postgres:16`(`:37`) · `alembic upgrade head` → `alembic check`(`:66-70`) · `ruff check .`(`:72-74`) · pytest 는 SQLite(`:76-80`) | **안 고친다** — 이 순서를 그대로 통과해야 한다(C1 ~ C7) |

**구현을 묶는 기존 시험 둘**(고치지 않는다 — 이 문서의 설계 제약이다):

| 시험 | 무엇을 막나 | 이번에 뜻하는 것 |
|---|---|---|
| `tests/test_gold_rest.py:72-76` `test_entrypoint_imports_no_db` | `import app.gold_main` 만으로 `app.core.db` · `app.core.tx` 가 올라오면 실패 | DB 판은 **`app.core.db` 를 쓰지 않는다** — 자기 엔진을 `sqlalchemy` 로 직접 만든다(SPEC P4 와 같은 방향). `app.core.config` 도 import 하지 않는다(§10 W-2) |
| `tests/test_gold_rest.py:79-85` `test_app_main_untouched` | `backend/app/main.py` · `backend/app/core/**` 가 `origin/release/v1.2.0` 과 한 글자라도 다르면 실패 | **`app/core/` 는 allowed_paths 밖이다**(§2) |

참고로 `app/model/*` · `app/modules/gold/*` 가운데 `app.core.db` · `app.core.tx` · `app.core.config` 를 import 하는 파일은 0 이다(`grep` — 11-17). `app.model.medallion` 을 import 하면 `app/model/__init__.py` 가 먼저 돌아 167 모델이 함께 올라온다 — `db` 판일 때만 그 import 가 일어나게 **늦게 import** 한다(WP-3).

기준선: 11-17 코디 검증 = 데이터 env 로 README 「검증」 전체 **638 passed · 2 skipped**(_RESUME §5 「허브 0.5.2 완료」). WP-0 이 같은 명령으로 **통과 · skip 수와 걸린 시간**을 다시 적는다.

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| allowed_paths(허브 레포) | **새 파일**: `backend/app/model/medallion.py` · `backend/app/modules/gold/silver_contract.py` · `backend/app/modules/gold/medallion_load.py`(적재 논리) · `backend/app/modules/gold/db_inputs.py`(DB → `LoadedInputs`) · `backend/alembic/versions/b202611170001_medallion_tables.py` · `backend/scripts/load_medallion.py` · `backend/tests/medallion_fixture.py` · `backend/tests/test_medallion_*.py`(이름은 전부 제안 — O-7) / **고치는 파일**: `backend/app/model/__init__.py`(import 한 줄) · `backend/app/modules/gold/{config,inputs,repository,service}.py`(`service.py` 는 `GoldState` 만) · `backend/app/gold_main.py`(lifespan) · `backend/tests/gold_support.py` · `backend/tests/test_gold_*.py`(두 판 매개변수화에 드는 줄만) · `backend/envs/.env.example` · `backend/README.md`(gold 절) |
| 손대지 않는 것 | `backend/app/main.py` · `backend/app/core/**`(§1 시험) · `backend/alembic/env.py` · `alembic.ini` · 기존 versions 2 파일 · 기존 모델 파일 · `pyproject.toml` · `uv.lock`(새 의존 0 — asyncpg · aiosqlite 가 이미 있다) · `.github/**` · `Dockerfile` · gold 도구 코드(`core` · `resolve` · `facets` · `pairs` · `concern` · `coverage` · `closure` · `cursor` · `kinds` · `ledger` · `ranges` · `memory` · `mcp_server`) · `router/gold.py` · `swagger_docs/gold.py` |
| 데이터 | 로컬 `$SM/gold`(15표 + `questions.csv`) · `$SM/silver`(57표) · `$SM/notes/ledger-check-list.csv`. **CSV · dump 를 허브 레포에 넣지 않는다**(루트 `.gitignore:46-47 · 59` 가 `.env*` · `*.dump` 를 막지만 CSV 는 막지 않는다 — `git status --porcelain` 으로 확인한다) |
| 접속 값 | 로컬 PostgreSQL 의 접속 값은 **레포 밖 파일**에 있다(_RESUME §2 11-17 「U-2 (a)」 행). 워커는 코디가 발주서에 적은 방법으로 **프로세스 env 에 올리기만** 한다 — 내용을 화면 · 로그 · 보고 · 문서에 찍지 않는다(`cat` · `echo` 금지). 이 문서를 쓴 워커는 그 파일을 열지 않았다 — 파일이 어떤 변수 이름을 내는지는 §11 B-1 |
| 포트 | 시험은 포트 없이(ASGI transport · SQLite 파일). 서버 확인은 **18107** 만(11-17 `lsof` — 비어 있음 · 듣는 중: 18105 · 18106 · 18210 · 18220 · 18432). 띄우기 전 `lsof -nP -iTCP:18107 -sTCP:LISTEN` 으로 다시 본다. 18105 · 18106 · 18220 · 18210 · 18005 는 건드리지 않는다. PostgreSQL 컨테이너(18432)를 내리거나 다시 만들지 않는다 |
| 검증 명령 | README 「검증」(`README.md:58-64`) 그대로 — `uv run ruff check app tests scripts`(CI 는 `ruff check .`) · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration`. **단계마다 그 WP 의 시험만 · 전체는 WP-4 에 한 번.** 실물 시험은 데이터 env 가 없으면 skip — 통과 · skip 수를 둘 다 보고한다 |
| **PostgreSQL URL 로 돌리는 pytest** | `tests/test_gold_*.py` · `tests/test_medallion_*.py` **만**. 전체 pytest 를 PostgreSQL `DATABASE_URL` 로 돌리지 않는다(다른 시험이 `app.core.db` 엔진을 그 URL 로 세운다) |
| 커밋 | 안 한다 — 워크트리에 변경만 남긴다(코디 몫). push · PR · 머지는 별도 승인(SPEC §7-3 끝 줄) |
| 「시험이 깨진다」 의 뜻 | 기존 시험은 **한 줄도 안 바뀌고 통과**가 기본이다(C6). 고치는 것은 두 판 매개변수화에 드는 fixture 줄뿐 — 고친 시험 이름과 까닭을 보고에 목록으로 낸다 |

## 3. WP-0 — 확인(W-4 · O-6) · 기준선

**목표**: 본문을 짓기 전에 SPEC 이 「확인 안 됨」 으로 넘긴 것을 로컬 PostgreSQL 에서 닫는다. **허브 레포에 남기는 파일 0**(스크립트는 세션 임시 폴더).
**SPEC**: §2-1 R4 · R5 · §2-6(지연 FK) · §3-3 C1 · C2 · 끝 문단 · §10-2 O-6 · §7-2 DE1 · 검수 W-4 · N-6.

| # | 확인 | 어떻게 | 통과 | 안 되면 |
|---|---|---|---|---|
| Z-1 | **접속 대상** | §8-1 의 「접속 대상 찍기」 명령 | 호스트 `127.0.0.1` · 포트 `18432` · 코디가 알려 준 DB 이름 · `public` 테이블 0(코디가 띄운 그대로 — _RESUME §5 11-17) | 다르면 **멈추고 보고**한다(다른 DB 에 아무것도 돌리지 않는다) |
| Z-2 | **지연 FK 가 `alembic check` 에서 어긋나지 않는가**(W-4 ①) | 표본 `MetaData`(허브와 같은 이름 규칙 `base.py:8-14`) — 자기 참조 FK 표 하나 · FK 둘인 표 하나 · 그 대상 표 · `load_seq` PK 표 하나. FK 전부 `deferrable=True, initially="DEFERRED"`. ① 빈 `public` 에 `create_all` ② `alembic.autogenerate.compare_metadata(MigrationContext.configure(conn), 표본)` ③ **역검증** — 같은 표본에서 FK 옵션만 뺀 `MetaData` 로 다시 비교 ④ `drop_all` → `public` 0 테이블로 되돌린다 | ② 가 `[]` · ③ 이 `[]` 이 아니다(비교기가 옵션을 본다는 증거 — alembic 1.18.4 · SQLAlchemy 2.0.50) | ② 가 차이를 내면 **대안**(아래) |
| Z-3 | **`load_seq` PK 가 시퀀스를 만들지 않는가**(W-4 ②) | Z-2 표본의 `load_seq` 칸에 `autoincrement=False` · `create_all` 뒤 `pg_sequences` 를 센다 | 시퀀스 0 · 칸 기본값(`column_default`) 없음. 역검증: `autoincrement=False` 를 빼면 시퀀스 1(또는 identity) | — (옵션은 모델 · 마이그레이션 **양쪽에** 준다 — WP-1) |
| Z-4 | **SQLite `create_all`** | 같은 표본을 `sqlite+aiosqlite` 메모리에 `create_all` → 지연 FK DDL · `autoincrement=False` 정수 PK 가 만들어진다 | 오류 0 | 대안 |
| Z-5 | **silver FK 에 표 사이 순환이 있는가** | `$SM/drafts/silver-check/silver-schema.json` 의 `columns[].fk` 80 으로 의존 그래프를 그려 자기 참조 11 을 뺀 뒤 순환을 찾는다(셈만) | 순환 0 이면 「의존 순서」 가 서고 `metadata.sorted_tables` 가 경고 없이 정렬된다 | 순환이 있으면 수와 표를 보고(대안의 「의존 순서 싣기」 가 그대로는 안 선다) |
| Z-6 | **기준선**(W-4 ③ 의 「앞」) | `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q --durations=15` 를 데이터 env 없이 한 번 · 있이 한 번 | 통과 · skip 수 · **걸린 시간**(초)을 적는다 — WP-1 끝에 같은 명령으로 「뒤」 를 잰다 | — |

**대안(O-6 · N-6)** — Z-2 또는 Z-4 가 안 되면 **지연 없이** 간다: FK 82 를 보통 FK 로 걸고, 적재기는 ① **지우기 = 의존 역순**(자식 먼저 — L2) ② **싣기 = 의존 순서**(부모 먼저 — L3) ③ 자기 참조 11칸은 표 하나를 **한 문장(여러 행 INSERT)** 으로 싣거나 부모 행이 앞에 오게 실은 뒤 `load_seq` 는 파일 행 번호 그대로 둔다. 어느 쪽으로 갔는지를 WP-0 보고에 한 줄로 적고 WP-1 · WP-2 가 그 결정을 따른다. **대안으로 가면 SPEC §2-6 의 「전부 지연」 문장이 바뀐다 — SPEC 되적기 후보로 보고한다**(§11 A-9).

**완료 조건**: Z-1 ~ Z-6 의 결과 표(통과 / 대안) · 역검증 둘의 결과 · `public` 이 다시 0 테이블 · `git status --porcelain` 변화 0.

## 4. WP-1 — 계약 상수 · 모델 74 · alembic 1

**목표**: 74 테이블을 `Base.metadata` 에 올리고 같은 것을 마이그레이션 하나로 만든다. 데이터는 넣지 않는다.
**SPEC**: §2-1 R1 ~ R10 · §2-2 · §2-3 · §2-4 · §2-5 · §2-6 · §2-7 · §2-8 · §2-9 · §3-1 · §3-2 · §3-3 C1 ~ C5 · §7-1 DT1 ~ DT3 · §7-2 DE1 · O-1 · O-3 · O-4 · O-5 · O-7.

| 만들 것 | 어디 | 내용 |
|---|---|---|
| silver 계약 상수 | 새 `app/modules/gold/silver_contract.py`(import 0 인 상수 파일 — `headers.py` 와 같은 꼴) | `SILVER_HEADERS`(표 → 칸 튜플 · 57표 · 순서 = 실제 헤더) · `SILVER_KEY`(표 → `code` \| `id` \| `None` — 키 없는 표 2: `alias` · `source_ref`) · `SILVER_FK`(표 → {칸: 대상 표} · 합 **80** · 자기 참조 11) · `SILVER_POLY`(다형 칸 15 — 14표 · V10 이 센다). **`silver-schema.json` 에서 이름만 기계로 옮긴다**(`tables[<표>].key` · `columns[].name` · `columns[].fk`) — 손으로 치지 않는다. 뜻 · 설명 칸은 옮기지 않는다 |
| 계약 묶음 | 같은 파일 또는 `medallion.py` 머리 | 72표의 (테이블 이름, CSV 이름, 칸, PK, FK, 인덱스, 유일 제약)을 내는 **함수 하나** — gold 는 `GOLD_HEADERS` · `KEY_COLUMN`(`headers.py:6-46`), silver 는 위 상수. 모델 · 적재기 · DB 판 · 시험이 이 함수만 읽는다(SPEC §3-1 「계약의 원천 하나」) |
| 모델 | 새 `app/model/medallion.py` | 72표를 위 계약에서 **기계로** `Table(..., Base.metadata)` 로 올린다 + `medallion_ledger_check`(§2-4 — PK (`lck_id`, `code`) · 인덱스 (`code`)) + `medallion_build`(§2-5 — 10칸). 타입은 `Text` · `Integer` · `DateTime(timezone=True)` 뿐 · `schema=` 0 · PostgreSQL 전용 타입 0(C3) |
| 칸 규칙 | 같은 파일 | `load_seq` `Integer` · NOT NULL · **`autoincrement=False`**(72표 전부에 — PK 인 3표뿐 아니라. 규칙을 하나로) · CSV 칸은 전부 `Text` · NULL 허용. NOT NULL 은 PK 칸 · 유일 제약 칸 · `load_seq` · `g_edge.src` / `dst` 에만(R6) |
| PK | 같은 파일 | gold 12표 `gid` · `g_node.node_id` · `g_edge.edge_id` · silver 55표 `code` / `id` · **키 없는 3표(`g_evidence` · `s_alias` · `s_source_ref`)는 `load_seq`**(R5) |
| FK 82 | 같은 파일 | silver 80(대상 = `s_<대상>` 의 PK) + `g_edge.src` · `dst` → `g_node.node_id`. **WP-0 이 통과면 82 전부 `deferrable=True, initially="DEFERRED"`** · 대안이면 옵션 없이. 이름은 규칙 그대로(`fk_<표>_<칸>_<대상 표>` — 최대 63자 한 개 · R8) |
| 인덱스 30 · 유일 3 | 같은 파일 | **이름을 직접 준다**(`ix_<표>__<칸>_<칸>` · `uq_<표>__<칸>_<칸>` — R8). 목록은 SPEC §2-2 표의 「인덱스」 칸 · §2-8(gold 28 + `s_source_ref` (`target_table`, `target_id`) + `medallion_ledger_check` (`code`)) · 유일 = `g_profile` (`subject_table`, `subject_code`) · `g_evidence` 네 칸 · `s_alias` (`target_table`, `target_code`, `name`) |
| 예약어 칸 | — | `order` 2(`g_pair` · `s_procedure_relation`) — 칸 이름 그대로. 손 SQL 을 쓰지 않는다(R9) |
| 등록 | `app/model/__init__.py` | 끝에 import 한 줄(`:205` 의 `legacy_prod` 줄 꼴 — `# noqa: F401`) |
| 마이그레이션 | 새 `alembic/versions/b202611170001_medallion_tables.py` | `revision = 'b202611170001'` · `down_revision = 'b202610300001'`. **`op.create_table` 을 풀어 쓴 고정본** — 앱의 계약 상수를 import 하지 않는다(SPEC §3-2 「꼴」). 만드는 법(제안): 빈 로컬 DB 를 `b202610300001` 까지 올린 뒤 `alembic revision --autogenerate` 로 뽑아 id · 파일 이름 · FK 옵션 · `autoincrement=False` · 인덱스 이름을 눈으로 대조해 굳힌다. `downgrade` = 74 테이블을 의존 역순으로 `drop_table`. 데이터 0 |

**W-4 를 받는 줄**
- **지연 FK · `autoincrement=False` 는 모델과 마이그레이션 양쪽에 같은 값으로** 준다 — 한쪽만 주면 `alembic check` 가 깨진다(검수 W-4 ① · WP-0 Z-2 역검증이 그것을 보였다).
- **`public` 테이블 셈**(W-4 ④): 세는 식 = `SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'`. `upgrade head` 뒤 **242**(기존 167 + 새 74 + `alembic_version` 1) · `alembic_version` 을 빼면 **241**(SPEC DE1 · §2-9 의 수). 보고에 두 수를 다 적는다.
- **pytest 시간**(W-4 ③ 의 「뒤」): WP-0 Z-6 과 같은 명령으로 다시 잰다 — `create_all` 을 도는 28 파일의 합이 얼마나 늘었나. CI 제한은 15분이다(`backend-test.yml:33`). 눈에 띄게 늘면(제안 기준: 전체 시간 1.5배 넘게) 고치지 말고 수와 함께 보고한다(§11 A-10).

**완료 조건**
1. **DT1** — `Base.metadata` 에 새 테이블 74(이름 = SPEC §2) · 72표의 칸 = `load_seq` + 계약 헤더(순서까지) · 전부 `Text` · PK · FK **82** · 직접 지은 인덱스 **30** · 유일 제약 **3** · 이름 길이 ≤ 63 · 이름 중복 0 · JSON 칸 0 · 판 칸 0 · 테이블 칸 합 **749** · 새 테이블 → 기존 167 FK 0 · gold → silver FK 0(R10). 시험이 계약 상수와 메타데이터를 기계로 대조한다.
2. **DT2** — SQLite 메모리에 `Base.metadata.create_all` 이 새 74 를 품고 성공(C2) · 기존 시험이 그대로 통과(C6 — 이 WP 에서는 `create_all` 을 쓰는 28 파일을 돌린다).
3. **DT3** — revision id `b202611170001` 이 옛 브랜치의 셋(`b202610260001` · `b202610300001` · `b202610310001`)과 다르다 · `down_revision` = `b202610300001` · 헤드 하나(`alembic heads`).
4. **DE1**(로컬 PostgreSQL · §8-1 순서) — `alembic upgrade head` → `alembic check` 가 「차이 없음」 · `public` 242(= 241 + `alembic_version`) · `downgrade -1` → 167 + 1 · 다시 `upgrade head` → 242 · 시퀀스 0(`pg_sequences` 에서 새 테이블 것) · 지연 FK 82 가 `pg_constraint.condeferrable` · `condeferred` 로 보인다(대안이면 0).
5. **계약 ↔ 실물**(데이터 env 가 있으면): `SILVER_HEADERS` 57 = `$SM/silver` 의 실제 헤더 57(이름 · 순서) · `SILVER_FK` 합 80 · 스키마 JSON 과 어긋남 0. 없으면 skip.
6. 옛 브랜치 이름과 겹침 0 — 새 74 이름이 `gold_*` · `graph_*` 로 시작하지 않는다(D-9).

**검증**: `uv run ruff check app tests scripts` → `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_medallion_model.py -q` + `create_all` 28 파일 → §8-1 의 alembic 명령(프로세스 env 붙인 꼴만).

## 5. WP-2 — 적재 CLI · 합성 fixture

**목표**: 로컬 CSV 묶음을 검사하고 한 트랜잭션으로 74 테이블에 싣는다. 검사가 실패하면 DB 를 건드리지 않는다.
**SPEC**: §4-1 · §4-2 · §4-3 V1 ~ V10 · §4-4 L1 ~ L6 · §4-5 · §2-1 R3 · R4 · R9 · §2-4(추출식 하나) · §2-5(빌드 기록 74행 · 해시 식) · §2-7(NUL · 다형 셈) · §3-3 C7 · §7-1 DT4 ~ DT8 · DT13 · O-2 · O-9.

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| CLI 껍데기 | 새 `scripts/load_medallion.py` | `argparse`(`--dry-run`) · exit code · 요약 출력. `uv run python scripts/load_medallion.py`(전례 `import_legacy_corpus.py` 의 `BACKEND_DIR` 를 `sys.path` 에 넣는 꼴). 논리는 아래 모듈에 둔다(시험이 함수로 부른다) |
| 적재 논리 | 새 `app/modules/gold/medallion_load.py` | ① env → ② 읽기 · 검사 → ③ 해시 → ④ 요약 / ⑤ DB 확인 → ⑥ 한 트랜잭션(SPEC §4-2). `app.model.medallion` 의 테이블 객체로만 SQL 을 짓는다(손 SQL 0) |
| 설정 | `config.py` | `GOLD_SILVER_DIR: str = ""`(새) · `DATABASE_URL: str = ""`(새 — §10 W-2). 기존 `REQUIRED_ENV` 넷은 **CSV 판 허브의 필수**로 그대로 둔다 — 적재기의 필수는 아래 표 |
| 읽기 · 파싱 재사용 | `inputs.py` | `_parse` · `_read_bytes` 를 적재기가 가져다 쓴다(이름 공개만 · 판정 그대로 — V4 = 「지금 `_parse` 와 같은 판정」). `combined_hash` · `LEDGER_CODE_RE` · `LEDGER_CODE_SOURCE_COLUMNS` · `FileRecord.kind` 의 네 값도 그대로 |
| 합성 fixture | 새 `tests/medallion_fixture.py` | `gold_fixture.write_fixture` 의 gold · notes 를 그대로 쓰고 **silver 폴더를 계약 헤더 57표로** 쓴다 — 허브가 읽는 5표(`source_ref` · `concern` · `adverse` · `condition` · `concern_site`)는 **기존 fixture 와 같은 값**을 계약 칸에(나머지 칸은 빈칸 또는 가짜 값) · 그 밖의 52표는 FK 가 닫히는 최소 행. DT13 의 꼴(여러 값 칸 ` · ` · 칸 안 중복 조각 · 묶음 값 · 끝자리 0 소수 · 한 끝이 빈 다형 짝 · `order` 칸 값 · 전부 빈 칸 · 0행 표)을 넣는다. **기존 `gold_fixture.py` 의 5칸 계층 헤더는 그대로 둔다**(CSV 판 기존 시험용 — 적재기에 주면 V5 로 떨어지는 것이 맞다) |

**필수 env — dry-run / 적재를 나눈다**(W-3 ②)

| env | `--dry-run` | 적재 |
|---|---|---|
| `GOLD_CSV_DIR`(gold 폴더 — 15표 + `questions.csv`) | 필수 | 필수 |
| `GOLD_SILVER_DIR`(silver 폴더 — 57표) | 필수 | 필수 |
| `GOLD_LEDGER_CHECK_PATH` | 필수 | 필수 |
| `DATABASE_URL` | **필요 없다**(있어도 접속하지 않는다 — DT7) | **필수** — 없으면 V1 · exit 2 |
| `GOLD_EXPECTED_HASH` | 선택(있으면 V9) | 선택(있으면 V9) |
| `GOLD_SOURCE_REF_PATH` · `GOLD_HIERARCHY_DIR` | 읽지 않는다 | 읽지 않는다(N-3 — §10) |

**검사 — SPEC V1 ~ V10 + 검수로 더한 둘**(번호 V11 · V12 는 이 문서가 붙였다 — SPEC 되적기 후보)

| # | 검사 | 실패 |
|---|---|---|
| V1 ~ V9 | SPEC §4-3 그대로(env · 폴더 · 파일 / 72표 전부 있음 / silver 폴더의 계약 밖 CSV / UTF-8 · 칸 수 / 헤더 = 계약 / PK 빈칸 0 · 중복 0 · 유일 제약 3 묶음 중복 0 / FK 82칸의 빈칸 아닌 값이 대상 키에 있음 / NUL 0 / 기대 해시) | exit 2 |
| V10 | (세기만) 다형 참조가 못 찾은 행 수 · 표별 행 수 · 빈칸 수 | 막지 않는다 — 요약 |
| **V11**(N-4) | 세 원천(gold 폴더 16 · silver 57 · 원장 확인 목록 1) 사이에 **같은 파일 이름 0** — `medallion_build.file_name` 이 PK 다 | exit 2(입력 문제를 L4 의 exit 3 으로 흘리지 않는다) |
| **V12**(N-5) | 원장 확인 목록의 `id` 가 **유일 · 빈칸 0** — 그래야 DB 판의 `ledger_rows_with_code`(서로 다른 `lck_id` 수)가 CSV 판(행 수로 센다 — `inputs.py:166-171`)과 같다 | exit 2 |

gold 폴더의 계약 밖 CSV 는 지금처럼 `hash_only`(읽지 않고 sha256 만 — `inputs.py:117-120`) · silver 폴더는 exit 2 — 폴더마다 다른 것은 SPEC 그대로다(N-8).

**한 번 읽기**(W-3 ③) — **파일마다 바이트를 한 번만 읽는다.** 그 한 벌의 바이트에서 sha256 · 파싱 · 검사 · 실을 행이 전부 나온다(`read_inputs` 의 `data` 쓰임과 같다 — `inputs.py:111-116`). 검사 뒤 싣기 직전에 파일을 다시 열지 않는다. `hash_only` 파일은 sha256 을 낼 때 한 번.

**트랜잭션 — L1 ~ L6**

| # | 하는 것 | 구현 줄 |
|---|---|---|
| ⑤ 앞 | **접속 대상을 찍는다**(W-2 ③) — `호스트 · 포트 · DB 이름` 만(`sqlalchemy.engine.make_url` 의 `host` · `port` · `database` — 비밀번호 · 사용자 이름은 찍지 않는다) | dry-run 은 `DATABASE_URL` 이 있어도 「접속 안 함」 이라고만 찍는다 |
| ⑤ | **접속 실패 = exit 2**(W-3 ① — 쓴 것 0 이다) · 메시지에 접속 문자열을 넣지 않는다(예외 글을 그대로 찍지 않는다 — 드라이버 예외에 호스트 밖의 값이 섞일 수 있다) | 적재기 자신의 엔진(`create_async_engine` · `NullPool` · 요청용 pool · 15초 제한을 물려받지 않는다 — SPEC §4-1) |
| L1 | 새 테이블 74 가 없으면 쓰지 않고 exit 2 · 「`alembic upgrade head` 먼저」 | `inspect` 로 테이블 이름 74 를 본다 |
| L2 | 트랜잭션 하나 · 새 74 의 행을 전부 지운다 | `DELETE`(O-2 — SQLite 에서도 같다). 지연 FK 면 순서 무관 · **대안이면 의존 역순**(WP-0) |
| L3 | 72표를 싣는다 — `load_seq` = 파일 행 번호(1 부터) · 빈칸(`''`) → NULL · 그 밖의 값은 그대로 | 묶음 크기 = 드라이버 매개변수 한도 ÷ 칸 수(가장 넓은 표 36칸 — asyncpg 한도 32,767 이면 한 문장 900행 안쪽) **또는** 행 목록을 넘기는 `executemany` 꼴(한도와 무관). 어느 쪽인지와 가장 큰 표(48,094행)의 걸린 시간을 보고한다 |
| L4 | `medallion_ledger_check`(뽑은 쌍) · `medallion_build`(74행) | `built_at` 은 한 번 정한 값을 74행에 · `loader_version` 은 상수 하나 |
| L5 | **커밋 전 되읽기 대조** — 표마다 `count(*)` = 파일 행 수 · `ORDER BY load_seq` 로 읽은 행(NULL → `''`) = CSV 행(값 · 순서) · `''` 이 든 칸 0 | 하나라도 다르면 롤백 · exit 3 |
| L6 | 커밋(지연 FK 는 이때 검사) | 실패 = 롤백 · exit 3 |

**exit code**: `0` 성공(dry-run 은 검사 통과) · `2` 입력 · 검사 · **접속** · L1 실패 — DB 에 쓴 것 0 · `3` L2 ~ L6 실패 — 롤백 · 옛 판 그대로(SPEC §4-5 + W-3 ①).
**요약 출력**(dry-run · 적재 공통): 표별 행 수 · 빈칸 수 · `gold_hash` · `aux_hash` · 파일별 sha256 · V10 의 셈 · 실을 테이블 수 · 실을 행 수. **값 본문은 찍지 않는다**(SPEC §4-1 끝 줄 — 표 이름 · 행 수 · 해시 · 파일 이름만).

**완료 조건**
1. **DT4** — 합성 fixture 를 SQLite 에 싣는다 → 표별 행 수 = 파일 행 수 · 빈칸 = NULL · `''` 0 · `load_seq` = 1…n · `medallion_build` **74행**(`kind` 별 15 · 1 · 1 · 5 · 52) · `medallion_ledger_check` = 뽑은 쌍.
2. **DT5** — V1 ~ V9 · **V11 · V12** 를 하나씩 깨뜨린 묶음 → exit 2 · DB 에 쓴 것 0(앞서 실어 둔 판의 빌드 기록이 그대로) · **접속 실패(없는 SQLite 폴더 경로 등) → exit 2** · L1(테이블 없는 DB) → exit 2.
3. **DT6** — 싣는 도중 실패를 넣는다(예: 되읽기 대조를 어긋나게) → exit 3 · 롤백 · 옛 판 그대로.
4. **DT7** — `--dry-run` 은 `DATABASE_URL` **없이** exit 0 · 엔진을 만들지 않는다(엔진 만드는 함수를 막아 두고 확인) · 요약에 해시 · 표별 행 수.
5. **DT8** — 72표를 `load_seq` 순으로 읽어 NULL → `''` 한 행 = CSV 행(값 · 순서).
6. **DT13** — 위 fixture 의 꼴들이 왕복 뒤 글자 그대로.
7. 한 번 읽기 — 시험이 파일 읽기 횟수를 센다(파일마다 1) 또는 검사 뒤 파일을 바꿔도 실린 행 · 해시가 처음 읽은 바이트의 것임을 본다.
8. 멱등 — 같은 묶음을 두 번 실으면 `built_at` 만 다르고 같은 상태.
9. 로그 · 요약 · 오류 글에 접속 문자열 · 값 본문 0(시험이 출력에서 fixture 의 글 값과 URL 의 비밀번호 자리를 찾아 0 임을 본다).

**검증**: `uv run pytest tests/test_medallion_load.py -q`(SQLite 는 **`tmp_path` 의 파일 DB** 를 쓴다 — 메모리 SQLite 는 엔진을 따로 만들면 서로 다른 DB 다).

## 6. WP-3 — DB 판 repository · 설정 · lifespan

**목표**: `GOLD_REPOSITORY=db` 면 시작 때 DB 에서 한 번 읽어 **CSV 판과 같은 `LoadedInputs`** 를 만들고 **지금 `GoldMemory`** 에 넘긴다. 요청은 DB 를 부르지 않는다.
**SPEC**: §5-1 · §5-2 P1 ~ P10 · §5-3 F1 ~ F7 · §5-4 · §2-1 R3 · R4 · §3-3 C6 · C7 · §7-1 DT9 ~ DT12 · DT14 · DT15 · 검수 W-1 · W-2 · N-1 · N-2 · N-7.

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 고르는 설정 | `config.py` | `GOLD_REPOSITORY: str = "csv"`(새 · `OPTIONAL_DEFAULTED_ENV` 에 넣어 빈 값 = 미설정 → `csv`) · 값은 `csv` \| `db` · 그 밖 = 시작 실패(`GoldLoadError`). **기본 `csv` 는 이 WORK 가 구현 선에서 닫는다**(N-7 — 지금 동작 · 기존 시험 · README 명령이 안 바뀌고 CSV 판이 대조 기준으로 남는다 · 뒤집기는 SPEC §9 N-6) |
| **`DATABASE_URL` 을 읽는 자리 = 하나**(W-2 ①) | `config.py` `GoldSettings.DATABASE_URL` | **적재기와 `db` 판은 이 값만 읽는다** — 프로세스 env 가 먼저 · 다음이 `envs/.env.gold`. **`app.core.config` 를 import 하지 않으므로 `envs/.env` 의 값은 적재기 · `db` 판에 닿지 않는다.** alembic 만 다른 길(`envs/.env` + 프로세스 env — `alembic/env.py:10,18`)이라 alembic 명령은 **전부 프로세스 env 를 붙인 꼴**로만 쓴다(§8-1). 값 꼴은 허브 공용 그대로 `postgresql+asyncpg://…` · 시험은 `sqlite+aiosqlite:///<파일>` |
| DB → 입력 | 새 `app/modules/gold/db_inputs.py` | `async def read_db_inputs(settings) -> LoadedInputs`. 자기 엔진(`create_async_engine` · `NullPool`) · **연결 하나 · 트랜잭션 하나**로 전부 읽고 **엔진을 닫는다**(P3 · P4). `app.model.medallion` 은 이 함수 안에서 늦게 import |
| 읽는 범위(P5) | 같은 파일 | gold 15표 전 칸 · `s_source_ref` 4칸 · `s_concern` / `s_adverse` / `s_condition` 의 **`code` · `parent_code` 두 칸만**(칸을 고른 `select`) · `s_concern_site` 3칸 · `medallion_ledger_check` · `medallion_build`. 나머지 silver 52표는 읽지 않는다 |
| 순서(P6) · NULL(P7) | 같은 파일 | gold 15 · `s_source_ref` 는 `ORDER BY load_seq` · NULL → `''`. **`s_concern_site` · 계층 3표도 `load_seq` 순으로 읽는다**(제안 — `LoadedInputs.concern_site` 가 리스트라 DT9 의 「같다」 가 순서까지 서게 · §11 A-4) |
| 한 판만(P8) | 같은 파일 | PostgreSQL 이면 그 연결에 `REPEATABLE READ`(방언 이름을 보고 건다 — SQLite 에는 그 이름이 없다) · **방언과 무관하게** 처음 읽은 `medallion_build` 74행 = 끝에 다시 읽은 74행(다르면 F7) |
| `LoadedInputs` 채우기(P9) | 같은 파일 | `gold_hash` · `aux_hash` = 빌드 기록 값 · `files` = `kind` ∈ {`gold`, `hash_only`} 16줄 + {`source_ref`, `aux`} 6줄 · `rows` = `file_rows`(`hash_only` 는 `None`) · `ledger_rows` = 원장 확인 목록 줄의 `file_rows` · `ledger_rows_with_code` = 서로 다른 `lck_id` 수 · `ledger_ids_by_code` = 코드 → `lck_id` 목록 |
| **정렬은 파이썬에서**(N-1) | 같은 파일 | `files` 의 gold 16줄 순서 · 해시 재셈 · `ledger_ids_by_code` 의 id 순을 **DB `ORDER BY` 글자 정렬에 맡기지 않는다** — 읽어 온 뒤 파이썬 `sorted` 로(`inputs.py:66,121,190` 과 같은 식) · 해시 재셈은 `combined_hash` 를 **그대로 부른다**. aux 6줄 순서는 CSV 판의 고정 순서(`source_ref` → `concern` → `adverse` → `condition` → `concern_site` → 원장 확인 목록 — `inputs.py:129-175`)를 코드 상수로 맞춘다 |
| **`expected_hash_checked`**(N-2) | 같은 파일 | DB 판도 **env 유무로** 정한다 — `bool(settings.GOLD_EXPECTED_HASH.strip())`(CSV 판 `inputs.py:196` 과 같은 식). `health.expected_hash_checked` 로 나가는 값이다 — DT9 의 대조 목록에 넣는다 |
| 시작 실패 F1 ~ F7 | 같은 파일 | 전부 `GoldLoadError` — `DATABASE_URL` 없음 · 접속 실패 · 테이블 없음 / 빌드 기록 0행 / 판 값이 행마다 다름 / 기록의 `file_name` · `sha256` 줄로 다시 센 해시 ≠ 기록 값 / 읽은 표 행 수 ≠ `table_rows` / 기대 해시 ≠ `gold_hash` / 처음 · 끝 빌드 기록이 다름. 오류 글에 접속 문자열을 넣지 않는다. 기대 해시가 없으면 CSV 판처럼 경고만(`inputs.py:182-183`) |
| 색인 세우기 가르기(P2) | `repository.py` | `CsvMemoryGoldRepository.__init__`(`:83-102`)을 「입력을 받아 `GoldMemory` · `LoadRecord` 를 세우는 몸통」 과 「`read_inputs` 를 부르는 CSV 생성자」 로 가른다. DB 판은 같은 몸통에 `read_db_inputs` 의 결과를 준다. **`_m`(내부 색인) 이름은 두 판에서 같다**(`test_gold_load.py:114-125` 가 `repo._m` 을 본다 — SPEC §7-1 끝 불릿). 이름 · 클래스 가름은 §11 A-3 |
| `load_ms` · `loaded_at`(P10) | `repository.py` | 지금 뜻 그대로 — DB 판의 `load_ms` 는 DB 읽기 시작부터 색인이 설 때까지 · `loaded_at` 은 이 프로세스가 올린 시각(`built_at` 이 아니다) |
| 상태 | `service.py` `GoldState`(`:31-50`) | 동기 `load()` 는 **그대로**(CSV 판 · 기존 시험이 부른다). `db` 판용으로 「이미 읽은 입력으로 세우는」 길 하나를 더한다(이름 제안 `load_from(inputs)`). `GoldToolService` · `health`(`:152-166`)는 안 고친다 |
| lifespan | `gold_main.py:32-37` | `GOLD_REPOSITORY` 가 `db` 면 `inputs = await read_db_inputs(settings)` → `state.load_from(inputs)` · `csv` 면 지금 한 줄 그대로. **`asyncio.run` 을 돌고 있는 루프 안에서 부르지 않는다.** 모르는 값 = 시작 실패 |
| **`health` 새 필드 — 안 넣는다**(W-1 (a)) | — | SPEC §8 표의 `§4-8 health` 줄(`repository` · `db_build{…}`)은 **이번에 구현하지 않는다.** 두 판의 `health` JSON 은 `build.loaded_at` · `load_ms` 만 다르다(DT10 · DE5). 어느 판으로 떴는지는 **시작 로그 한 줄**(판 · 접속 대상의 호스트 · 포트 · DB 이름 · `gold_hash`)로만 남긴다 |
| 시험 헬퍼 | `tests/gold_support.py`(`:36-47`) | `real_settings` 가 프로세스 env 의 `GOLD_REPOSITORY` · `DATABASE_URL` 을 함께 받고 `real_state` 가 `db` 면 DB 에서 읽어 세운다(동기 시험 · 비동기 시험 어느 쪽에서 처음 불려도 되게 — 별 스레드의 새 루프에서 읽는 헬퍼 하나). **기본은 지금과 같다**(env 없으면 `csv`) |
| 두 판 매개변수화 | `tests/test_gold_tools_synthetic.py:20-24` 의 `svc` · `tests/test_gold_mcp.py:19-25` · `tests/test_gold_rest.py:21-30` 의 `running` | fixture 를 `csv` · `db` 두 판으로 돌린다 — `db` 판 = `medallion_fixture` 폴더를 `tmp_path` 의 SQLite 파일에 실은 뒤 그 URL 로. **시험 본문은 안 고친다** |

**완료 조건**
1. **DT9** — 같은 fixture 폴더로 CSV 판 `LoadedInputs` = DB 판 `LoadedInputs`: `gold`(표 · 행 · 칸 · 값 · 순서) · `source_ref` · `hierarchy` · `concern_site` · `ledger_ids_by_code` · `ledger_rows` · `ledger_rows_with_code` · `files`(22줄 · 순서까지) · `gold_hash` · `aux_hash` · **`expected_hash_checked`**(N-2 — env 를 준 때 · 안 준 때 둘 다). **전제(N-3)**: CSV 판의 `GOLD_SOURCE_REF_PATH` · `GOLD_HIERARCHY_DIR` 이 적재기의 `GOLD_SILVER_DIR` 과 **같은 폴더의 같은 파일**을 가리킨다 — `aux_hash` 가 파일 이름을 넣어 세기 때문이다. 시험은 그렇게 세운다.
2. **DT10** — 기존 합성 도구 시험(도구 9 · REST · MCP)이 두 판으로 통과 · 같은 요청의 응답 JSON 이 두 판에서 같다(`build.loaded_at` 제외 · `health` 는 `load_ms` 도). **`health` 의 열쇠 집합이 두 판에서 같다**(새 필드 0 — W-1).
3. **DT11** — F1 ~ F7 을 하나씩 → lifespan 이 `GoldLoadError` 로 시작 실패.
4. **DT12** — `GOLD_REPOSITORY` 기본 = `csv` · 빈 값 = `csv` · 모르는 값 → 시작 실패 · `db` 면 CSV 경로 env 넷 없이 뜬다.
5. **DT14** — `db` 판 허브가 시작 뒤 엔진을 닫았다 · 도구 9 를 한 번씩 부르는 동안 쿼리 0(엔진 이벤트로 센다 — 0 인지와 「엔진이 이미 dispose 됐다」 둘 다).
6. **DT15** — `db` 판이 읽은 표 = P5 의 것뿐(쿼리를 잡아 표 이름을 모은다 — silver 52표 0) · 계층 3표에서 고른 칸이 `code` · `parent_code` 둘뿐.
7. `tests/test_gold_rest.py:72-85` 의 두 시험이 **손대지 않고** 통과 — `import app.gold_main` 만으로 `app.core.db` · `app.core.tx` 가 올라오지 않는다 · `app/core` 차이 0.
8. `test_service_layer_uses_repository_only`(`test_gold_tools_synthetic.py:393-398`) 가 손대지 않고 통과 — `service.py` 가 `modules.gold.inputs` · `modules.gold.memory` 를 import 하지 않는다(`load_from` 의 인자 타입 때문에 import 가 필요해지면 `repository.py` 쪽에 둔다).
9. `memory.py` · 도구 코드의 `git diff` 가 비어 있다.

**검증**: `uv run pytest tests/test_medallion_repo.py tests/test_gold_tools_synthetic.py tests/test_gold_mcp.py tests/test_gold_rest.py tests/test_gold_load.py tests/test_gold_contract.py -q`.

## 7. WP-4 — 로컬 실물 확인 · 문서 · 마감

**SPEC**: §6-1 ~ §6-3 · §7-2 DE1 ~ DE6 · DE8 · §7-3 1 · 2 · 4 · §3-3 C5 · C6.

순서 · 명령은 §8. 여기는 무엇을 보나.

| # | 확인 | 기대 |
|---|---|---|
| DE1 | WP-1 완료 조건 4 를 **빈 DB 에서 처음부터** 다시(WP-1 에서 이미 올렸으면 그 결과를 쓰되, `downgrade -1` → `upgrade head` 왕복은 **적재 앞에** 한 번) | `alembic check` 통과 · 242 / 241 |
| DE2 | `--dry-run` | 72표 통과 · 행 수 = SPEC §2-2 · §2-3 · `gold_hash` = `8accbb21…f6228c` · `aux_hash` = `6435fe41…1803a3`(전체 값은 SPEC §2-5) · 못 찾은 다형 참조 수(세기만) · 실을 행 **129,527** |
| DE3 | 적재 | exit 0 · 74 테이블 행 수 = SPEC §2-9(gold 62,244 · silver 66,936 · 원장 확인 273 · 빌드 기록 74) · 되읽기 차이 0 · `''` 0 · FK 위반 0 · 걸린 시간 |
| DE4 | 같은 묶음 다시 → 같은 상태(`built_at` 만) · 헤더 한 칸을 바꾼 사본(**레포 밖 세션 임시 폴더**) → exit 2 · 빌드 기록 불변 | — |
| DE5 | 18107 에 `db` 판 → `health` | `build.gold_hash` · `build.aux_hash` · `files[]` 22줄(`name` · `sha256` · `rows` · `kind` · **순서**) · `integrity` · `aux` · `expected_hash_checked` 가 18105(CSV 판)의 `health` 와 같다 · 열쇠 집합이 같다 |
| DE6 | 18105(CSV 판 · 코디 것 — **읽기 요청만 보낸다**)와 18107(DB 판)에 같은 요청 묶음 → JSON 이 같다(`build.loaded_at` 제외) | 요청 묶음 = ① 기존 gold 실물 시험이 보내는 요청(아래 pytest 가 덮는다) ② 37 문항 답 키의 `calls[]` — 앱 워크트리의 명세 파일을 **읽기만** 해 그대로 보낸다(자리는 코디가 발주서에 준다 — §11 B-2) · 쪽을 끝까지 넘긴다. + 실물 pytest 를 DB 판으로: CSV env 넷 + `GOLD_REPOSITORY=db` + PostgreSQL `DATABASE_URL` 로 `tests/test_gold_*.py` 가 CSV 판과 **같은 통과 · skip 수** |
| DE8 | 재기만 | DB 판 `load_ms` · 표별 읽기 시간(가장 큰 표 48,094행) · CSV 판 `load_ms` 를 나란히 — 기준값 없음 |

**마감 할 일**
1. `README.md` gold 절(`:82-114`): `GOLD_REPOSITORY`(기본 `csv`) · 적재 순서(`alembic upgrade head` → dry-run → 적재 → 허브 재시작 → `health` 해시 확인) · `db` 판 실행 명령 · **「alembic · 적재 전에 접속 대상을 찍어 본다」** 한 줄 · 「PostgreSQL URL 로는 gold · medallion 시험만」 한 줄. 명령의 접속 값은 전부 `<…>` 자리 표시.
2. `envs/.env.example`(`:11-25`): `GOLD_REPOSITORY=` · `GOLD_SILVER_DIR=` 와 설명 주석 한 줄씩. **`DATABASE_URL` 줄은 건드리지 않는다**(`:1` — 허브 공용).
3. 전체 검증 **한 번**: `uv run ruff check .`(CI 와 같은 범위) · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q --durations=15` 를 데이터 env 없이 · 있이 — 통과 · skip 수 · 시간을 WP-0 기준선과 나란히(W-4 ③).
4. `alembic check` 를 적재 **뒤**의 DB 에서도 한 번(데이터가 있어도 스키마 대조는 같아야 한다).
5. 공개 grep(§9) · `git status --porcelain` 이 §2 allowed_paths 안의 파일뿐 · `git status --ignored` 로 새로 생긴 무시 파일(임시 SQLite · 사본 폴더가 레포 안에 생기지 않았는지).
6. 18107 의 `db` 판은 **띄워 둔 채** 코디에게 알린다(코디가 DE7 앞에 한 번 더 본다 · 내리는 것은 그 뒤 워커 또는 코디 — 발주서가 정한다).
7. 보고: WP 별 결과 · 고친 기존 시험 목록(이름 · 까닭) · WP-0 의 결정(지연 / 대안) · 다시 센 수(242 / 241 · 129,527 · 74 · 82 · 30 · 3) · 시간 표 · §11 의 A · B 항목마다 정한 값.

**완료 조건**: DT1 ~ DT15 가 시험 이름 또는 주석으로 찾아진다 · DE1 ~ DE6 · DE8 결과가 보고에 있다 · 위 1 ~ 7.

## 8. 실물 확인 — 순서 · 누가

### 8-1. 워커 몫(로컬 PostgreSQL 18432 · 허브 18107)

접속 값은 프로세스 env 로만 준다. 아래 `<…>` 는 자리 표시다.

```bash
# backend/ 에서. 접속 값은 코디가 준 방법으로 프로세스 env 에 올린 뒤(내용을 찍지 않는다)

# ⓪ 접속 대상 찍기 — alembic 이 실제로 읽을 값을 같은 길(app.core.config)로 읽어 호스트 · 포트 · DB 이름만
uv run python -c "from sqlalchemy.engine import make_url; from app.core.config import settings; u = make_url(settings.DATABASE_URL); print(u.host, u.port, u.database)"
#   → 127.0.0.1 18432 <DB>  가 아니면 멈춘다. 프로세스 env 를 빼먹으면 envs/.env 의 값(또는 빈 값)이 찍힌다 — 그때 alembic 을 돌리지 않는다

# ① 스키마 — 전부 프로세스 env 를 붙인 꼴로만(W-2 ②)
DATABASE_URL="$DATABASE_URL" uv run alembic upgrade head
DATABASE_URL="$DATABASE_URL" uv run alembic check
DATABASE_URL="$DATABASE_URL" uv run alembic downgrade -1     # DE1 — 새 74 만 지운다 · 적재 앞에만
DATABASE_URL="$DATABASE_URL" uv run alembic upgrade head

# ② 적재 — 경로는 로컬 $SM
export GOLD_CSV_DIR=<gold 폴더> GOLD_SILVER_DIR=<silver 폴더> GOLD_LEDGER_CHECK_PATH=<ledger-check-list.csv>
export GOLD_EXPECTED_HASH=<SPEC §2-5 의 gold_hash>
uv run python scripts/load_medallion.py --dry-run     # DE2 — DB 접속 0
uv run python scripts/load_medallion.py               # DE3 — 시작 때 접속 대상을 찍는다
uv run python scripts/load_medallion.py               # DE4 — 다시 싣기

# ③ DB 판 허브 — 18107 만(띄우기 전 lsof 로 비었는지)
lsof -nP -iTCP:18107 -sTCP:LISTEN
GOLD_REPOSITORY=db GOLD_EXPECTED_HASH=<같은 값> \
  uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18107

# ④ 대조 — 18105(CSV 판 · 코디 것)에는 GET · POST 조회만 보낸다
#    DE5 health · DE6 요청 묶음 · DE8 시간
# ⑤ 실물 pytest 를 DB 판으로 — gold · medallion 시험만
GOLD_REPOSITORY=db GOLD_SOURCE_REF_PATH=<silver 폴더>/source_ref.csv GOLD_HIERARCHY_DIR=<silver 폴더> \
  uv run pytest tests/test_gold_*.py tests/test_medallion_*.py -q -rs
```

- ⓪ 의 한 줄은 **alembic 을 돌리기 전마다** 본다(W-2 ③). 지금 이 워크트리에는 `envs/.env` 파일이 없다(11-17 — `envs/` 에 `.env.example` 뿐 · 내용은 열지 않았다) — 그래서 프로세스 env 를 빼먹으면 빈 값이 되어 alembic 이 자리 표시 URL(`alembic.ini:89`)로 떨어져 접속 자체가 안 된다. **이것은 지금 상태일 뿐이다 — 파일이 생기면 달라지므로 ⓪ 을 건너뛰지 않는다.**
- `downgrade -1` 은 **적재 앞에만** 돈다(뒤에 돌리면 실은 판이 지워진다 — 다시 실으면 되지만 DE3 의 수를 다시 봐야 한다).
- 워커는 PostgreSQL 컨테이너를 내리거나 다시 만들지 않고, **18105 · 18220 · 18210 · 18005 를 내리거나 띄우지 않는다.** 18106 도 건드리지 않는다.
- 옛 브랜치(`phub-recommend`)로 올린 DB 에는 돌리지 않는다(SPEC §3-2 — 지금 18432 는 새 빈 DB 다).

### 8-2. 코디 몫

| 순서 | 무엇 | 왜 코디인가 |
|---|---|---|
| 앞 | 로컬 PostgreSQL 띄우기(**끝남** — 11-17) · 접속 값을 워커에게 주는 방법 정하기(§11 B-1) · 37 답 키 명세의 자리 알려 주기(§11 B-2) | 사용자 기계의 프로세스 · 레포 밖 값 |
| WP-4 뒤 | 워커 보고 검증(ruff · pytest · `alembic check` · grep · 18107 `health`) | — |
| **DE7 · 완료 조건** | **18105 의 CSV 판을 내리고 같은 포트에 `db` 판을 띄운다** → 앱에서 답 키 대조 (나) → **37 / 37 같음**(CSV 판에서 확인된 키와). 앱 쪽 명령은 WORK-009 의 키 다시 뽑기 · 대조 걸음(`answer_key --all` → `--diff`)을 따른다 — **지금 확인된 키를 덮지 않게 백업 폴더를 먼저 둔다** | 18105 는 앱(18220) · 사용자 e2e 가 보는 포트다 · 워커는 건드리지 않는다 |
| 뒤 | 18105 를 어느 판으로 둘지 · 18107 내리기 · 커밋 · SPEC 되적기(§11 A 항목) | 사용자 결정 · 코디 몫 |

## 9. 완료 조건 · 검증 명령(모음)

| # | 완료 조건(SPEC §7-3) | 누가 | 무엇으로 |
|---|---|---|---|
| 1 | DT1 ~ DT15 통과 · `ruff` · 기존 시험 전부 통과(CSV 판 그대로) | 워커 | `uv run ruff check .` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q` |
| 2 | DE1 ~ DE6 통과(+ DE8 기록) | 워커 | §8-1 |
| 3 | **DE7 — 18105 를 `db` 판으로 · 앱 37 키 대조 (나) 가 CSV 판과 같다** | **코디** | §8-2 |
| 4 | 레포에 CSV · dump · 접속 값이 들어가지 않았다 | 워커 → 코디 | 아래 grep |

```bash
# backend/ 에서
uv run ruff check .
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q --durations=15
DATABASE_URL="$DATABASE_URL" uv run alembic check          # ⓪ 뒤에 · 프로세스 env 붙인 꼴만
uv run alembic heads                                       # 헤드 하나 — b202611170001

# 허브 워크트리 루트에서 — 커밋 후보 전체
git status --porcelain                                     # allowed_paths 안뿐 · *.csv · *.dump · *.db · *.sqlite 0
git diff --stat origin/release/v1.2.0 -- backend/app/main.py backend/app/core   # 비어 있다
git diff HEAD --stat -- backend/app/modules/gold/memory.py backend/app/router/gold.py backend/app/modules/gold/mcp_server.py   # 비어 있다
git diff HEAD -U0 | grep -n -i -E "postgresql(\+asyncpg)?://[^<]|:[0-9]{4,5}/[a-z_]+|passw|secret|token|api[_-]?key"   # 자리 표시 · 127.0.0.1 포트 설명 밖 0
git diff HEAD -U0 | grep -n -E "/(Users|home)/[a-z]"       # 홈 경로 0
grep -rn "app.core.db\|app.core.tx\|app.core.config" backend/app/modules/gold backend/app/model/medallion.py backend/scripts/load_medallion.py   # 0
```

`backend-test.yml:51` 과 `envs/.env.example:1` 에 이미 있는 CI · 예시용 로컬 URL 은 이번 변경이 아니다 — grep 은 **이번 차이**에만 건다.

## 10. 검수 지적 반영 — WARN 4 · NOTE 8(`review-spec-003.md` §1)

| # | 지적(한 줄) | 이 문서에서 | 어디 |
|---|---|---|---|
| **W-1** | `health` 새 필드가 「같은 응답」 계약과 부딪힌다 | **(a) 새 필드를 안 넣는다**(코디 결정). `service.py` `health` 를 안 고친다 · 두 판의 열쇠 집합이 같음을 DT10 · DE5 가 본다 · 어느 판인지는 시작 로그로만 | §6 표 「`health` 새 필드」 · 완료 조건 2 |
| **W-2** | `DATABASE_URL` 을 어느 설정이 읽는지 안 닫혔다 | ① **읽는 자리 하나 = `GoldSettings.DATABASE_URL`**(프로세스 env → `envs/.env.gold` · `envs/.env` 는 닿지 않는다) ② alembic 명령은 **프로세스 env 붙인 꼴만** ③ alembic 앞에는 「접속 대상 찍기」 한 줄 · 적재기 · `db` 판은 스스로 **호스트 · 포트 · DB 이름**을 찍는다(비밀번호 · 사용자 이름 없음) | §6 표 「읽는 자리」 · §5 표 「⑤ 앞」 · §8-1 ⓪ ① |
| **W-3** | 적재 CLI 구멍 셋 | ① **접속 실패 = exit 2**(쓴 것 0) ② 필수 env 를 dry-run / 적재로 나눈 표(`DATABASE_URL` 은 적재만) ③ **파일은 한 번 읽는다** | §5 「필수 env」 표 · 「한 번 읽기」 · 「트랜잭션」 표 ⑤ · 완료 조건 2 · 4 · 7 |
| **W-4** | 첫 WP 확인 목록 | ① 지연 FK 를 모델 · 마이그레이션 **양쪽에 같게** → `alembic check` + 역검증 ② `load_seq` `autoincrement=False`(PK 3표 — 규칙을 하나로 72표 전부) ③ `create_all` 28 파일 pytest 시간 앞 · 뒤 ④ `public` 셈 식 — `alembic_version` 을 넣어 **242** · 빼면 241 | §3 WP-0 Z-2 ~ Z-6 · §4 「W-4 를 받는 줄」 · 완료 조건 4 · §7 마감 3 |
| N-1 | 「이름순」 은 파이썬 글자 순 — DB `ORDER BY` 에 맡기면 정렬 규칙을 탄다 | **정렬은 파이썬에서** · `combined_hash` 를 그대로 부른다 | §6 표 「정렬은 파이썬에서」 |
| N-2 | `expected_hash_checked` 가 P9 · 대조 목록에 없다 | DB 판도 env 유무로 정한다 · DT9 목록에 더함 | §6 표 · 완료 조건 1 |
| N-3 | 적재기는 `GOLD_SILVER_DIR` 하나로 읽는다 — CSV 판의 두 env 가 같은 폴더의 같은 파일일 때만 `aux_hash` 가 같다 | 대조 전제로 적음 — DT9 · DE5 · DE6 은 같은 폴더로 세운다 | §5 「필수 env」 표 · §6 완료 조건 1 · §8-1 ⑤ |
| N-4 | 세 원천 사이 파일 이름 겹침 검사가 없다 | **V11** — exit 2 | §5 「검사」 표 |
| N-5 | 원장 확인 목록 `id` 유일 · 빈칸 0 이어야 두 판의 셈이 같다 | **V12** — exit 2 | §5 「검사」 표 |
| N-6 | 지연 FK 대안에 「지우기도 역순」 이 빠졌다 | 대안 = 지우기 의존 역순 + 싣기 의존 순서 + 자기 참조 11칸 | §3 「대안」 |
| N-7 | 기본값 `csv` 가 변경 기록의 제안 목록에 없다 | 이 WORK 가 구현 선에서 닫는다(뒤집기는 SPEC §9 N-6) — SPEC 변경 기록 되적기 후보 | §6 표 「고르는 설정」 · §11 A-8 |
| N-8 | 계약 밖 CSV 처리가 폴더마다 다르다 | SPEC 그대로 둔다(gold = `hash_only` · silver = exit 2) | §5 「검사」 표 아래 줄 |

## 11. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

**A — 구현 때 정한다(제안값 · 정한 값을 보고에 적는다)**

| # | 무엇 | 제안 | 상태 |
|---|---|---|---|
| A-1 | `DATABASE_URL` 을 읽는 자리(W-2 ①) — SPEC §4-1 은 「alembic 이 읽는 그 값」 과 「`.env.gold`」 를 함께 적었다 | **`GoldSettings.DATABASE_URL`**(프로세스 env → `.env.gold`). `app.core.config` 를 읽으면 `envs/.env` 의 다른 DB 가 조용히 잡힐 수 있고 `app.core` 는 고칠 수 없다(§1 시험). 다른 길 — 프로세스 env 만(`os.environ`) 읽는 더 좁은 꼴 — 도 된다 | 구현 때 정함 — SPEC §4-1 되적기 후보 |
| A-2 | 파일 · 모듈 · 함수 이름(§2 의 새 파일 · `load_from` · `read_db_inputs` · `SILVER_*`) | 본문 제안(O-7 의 이름은 SPEC 그대로 — `medallion_build` · `medallion_ledger_check` · `load_seq` · `GOLD_REPOSITORY` · `GOLD_SILVER_DIR` · `load_medallion.py` · `medallion.py` · `b202611170001` · exit 3) | 구현 때 정함 |
| A-3 | `repository.py` 를 어떻게 가르나(P2) | 몸통 클래스 하나(입력을 받는다) + CSV 생성자 · DB 생성자. `CsvMemoryGoldRepository(settings)` 의 부르는 꼴은 그대로 둔다(기존 시험 · `service.py:34` 기본값) | 구현 때 정함 |
| A-4 | `s_concern_site` · 계층 3표의 읽는 순서 — SPEC P6 은 gold 15 · `s_source_ref` 만 적었고 §5-4 는 `concern_site` 가 같아야 한다고 적었다 | `load_seq` 순으로 읽는다(리스트 비교가 선다 · 결과에는 영향 없음 — `memory.py:88,93` 이 정렬한다) | 구현 때 정함 — SPEC P6 되적기 후보 |
| A-5 | 합성 fixture 의 silver 52표를 얼마나 채우나 | 표마다 0 ~ 2행 · FK 82 가 한 번씩은 값으로 걸리게 · 0행 표 하나(`s_external_code`) | 구현 때 정함 |
| A-6 | L3 의 묶음 꼴 | `executemany` 꼴(한도와 무관)로 시작 — 가장 큰 표의 시간을 재고 느리면 여러 행 INSERT 묶음으로 | 구현 때 정함(O-2 는 `DELETE`) |
| A-7 | V11 · V12 라는 번호 | 이 문서가 붙였다 — SPEC §4-3 표 되적기 후보 | 보고 |
| A-8 | 기본값 `csv`(N-7) · exit 2 = 접속 실패(W-3 ①) · `health` 새 필드 없음(W-1) | 본문 그대로 — SPEC §4-5 · §5-1 · §8 표 · 변경 기록 되적기 후보 | 보고 |
| A-9 | WP-0 이 대안으로 가면 SPEC §2-6 「전부 지연」 문장이 바뀐다 | 결정과 근거(Z-2 · Z-4 결과)를 보고 | WP-0 뒤 |
| A-10 | pytest 시간이 눈에 띄게 늘면 | 고치지 않고 수를 보고(예: `create_all` 을 쓰는 시험이 필요한 테이블만 만들게 하는 것은 **기존 시험 28 파일을 고치는 일**이라 이 WORK 밖이다) | WP-1 뒤 |
| A-11 | `db` 판일 때 `app/model/__init__.py` 가 167 모델을 함께 올리는 시간 | `load_ms` 에 들어간다 — DE8 에서 따로 적는다 | 재기만 |

**B — 코디에게 받을 것(발주서에)**

| # | 무엇 | 왜 |
|---|---|---|
| B-1 | 로컬 PostgreSQL 접속 값을 워커 프로세스 env 에 올리는 방법 — 그 파일이 `DATABASE_URL`(`postgresql+asyncpg://…` 꼴)을 그대로 내는지 · DB 이름(Z-1 이 견줄 값) | 이 문서를 쓴 워커는 그 파일을 열지 않았다 — **확인 안 됨** |
| B-2 | 37 문항 답 키 명세(`calls[]`)의 자리(앱 워크트리 · gitignore 로컬) — DE6 이 읽기만 한다 | 앱 레포는 이 WORK 의 allowed_paths 밖이다. 못 받으면 DE6 은 「기존 실물 시험의 요청 + DB 판 실물 pytest」 까지만 하고 그 사실을 보고한다(답 키 요청 대조는 코디의 DE7 이 덮는다) |
| B-3 | WP-4 뒤 18107 을 누가 언제 내리나 | §7 마감 6 |

**이번 판에 구현 대상이 아닌 절**: SPEC §8(SPEC-001 되적기 목록 — 문서 일 · 그 가운데 `§4-8 health` 줄은 W-1 로 뺀다) · §9 N-1 ~ N-11(다음 범위 — stg · 요청마다 SQL · 정규화 · 접근 제어) · O-5(gold → silver 홑 칸 FK — 1회차 뒤) · O-8(표 내용 해시 — 뒤 단계) · O-9(잠금 — 막지 않음).

## 12. SPEC-003 절 ↔ WP 대응(미대응 0)

| SPEC-003 절 | 무엇 | WP | 시험 · 확인 |
|---|---|---|---|
| §1-2 D-0 ~ D-10 | 정해진 것 | 전부(범위 · 금지) | §2 · §9 grep · DT1(R10) · DT3(D-9) |
| §2-1 R1 · R2 · R5 ~ R8 · R10 | 이름 · 칸 · PK · NOT NULL · JSON 0 · 이름 규칙 · 기존 167 FK 0 | WP-1 | DT1 |
| §2-1 R3 | 빈칸 = NULL · 읽을 때 `''` | WP-2(싣기) · WP-3(읽기) | DT4 · DT8 · DT13 · DE3 |
| §2-1 R4 | `load_seq` | WP-0(Z-3) · WP-1 · WP-2 · WP-3 | DT1 · DT4 · DT8 |
| §2-1 R9 | 예약어 칸 `order` | WP-1 · WP-2 | DT13 |
| §2-2 gold 15표 | 표 · PK · 유일 · FK · 인덱스 | WP-1 | DT1 · DE1 · DE3(행 수) |
| §2-3 silver 57표 | 표 · PK · FK 80 · 다형 칸 | WP-1(계약 상수 · 모델) · WP-2(V10) | DT1 · WP-1 완료 조건 5 · DE2 |
| §2-4 `medallion_ledger_check` | 273쌍 · 추출식 하나 | WP-1(표) · WP-2(L4 · V12) · WP-3(읽기) | DT4 · DT9 · DE3 |
| §2-5 `medallion_build` | 74행 · 해시 식 | WP-1(표) · WP-2(L4) · WP-3(P9 · F2 ~ F5) | DT4 · DT9 · DT11 · DE2 · DE5 |
| §2-6 FK 82 · 지연 | 걸기 · 지연 옵션 | WP-0(Z-2 · Z-4 · Z-5) · WP-1 | DT1 · DE1 · DE3 |
| §2-7 다형 · 1:1 로 안 맞는 칸 | 그대로 한 칸 · NUL | WP-2(V8 · V10 · fixture) | DT13 · DE2 |
| §2-8 인덱스 30 · 유일 3 | 직접 지은 이름 | WP-1 | DT1 |
| §2-9 셈 | 74 · 129,527 · 749 | WP-1 · WP-4 | DT1 · DE1 · DE3 |
| §3-1 모델 자리 | `medallion.py` · import 한 줄 · 기계로 짓기 · 계약의 원천 하나 | WP-1 | DT1 |
| §3-2 마이그레이션 | 1개 · id · 고정본 · downgrade | WP-1 | DT3 · DE1 |
| §3-3 C1 | 마이그레이션 = 모델 | WP-0 · WP-1 | DE1(`alembic check`) |
| §3-3 C2 · C3 · C4 | SQLite `create_all` · 전용 타입 0 · 이름 ≤ 63 | WP-0(Z-4) · WP-1 | DT1 · DT2 |
| §3-3 C5 · C6 | ruff · 기존 시험 그대로 | WP-4 | §9 |
| §3-3 C7 | DB 판 · 적재기가 SQLite 에서도 돈다 | WP-2 · WP-3 | DT4 ~ DT15 |
| §4-1 자리 · 입력 env | 스크립트 · env · 자기 엔진 · 로그에 값 0 | WP-2 | DT4 · 완료 조건 9 |
| §4-2 순서 ① ~ ⑥ | — | WP-2 | DT4 · DT7 |
| §4-3 V1 ~ V10 | 검사(+ V11 · V12) | WP-2 | DT5 · DE2 · DE4 |
| §4-4 L1 ~ L6 | 한 트랜잭션 교체 · 멱등 | WP-2 | DT4 · DT6 · DE3 · DE4 |
| §4-5 dry-run · exit | 0 / 2 / 3 | WP-2 | DT5 ~ DT7 |
| §5-1 고르는 설정 | `GOLD_REPOSITORY` 기본 `csv` | WP-3 | DT12 |
| §5-2 P1 ~ P10 | 시작 때 읽기 | WP-3 | DT9 · DT10 · DT14 · DT15 |
| §5-3 F1 ~ F7 | 시작 실패 | WP-3 | DT11 |
| §5-4 두 판 대조 | 입력 · 도구 응답 · 앱 | WP-3 · WP-4 · **코디** | DT9 · DT10 · DE5 · DE6 · **DE7** |
| §6-1 로컬 PostgreSQL | 띄우기 | **코디(끝남)** | Z-1 |
| §6-2 적재 · §6-3 허브를 DB 판으로 | 명령 | WP-4 | §8-1 |
| §7-1 DT1 ~ DT15 | 허브 단위 | WP-1(1 ~ 3) · WP-2(4 ~ 8 · 13) · WP-3(9 ~ 12 · 14 · 15) | — |
| §7-2 DE1 ~ DE8 | 로컬 실물 | WP-1 · WP-4(1 ~ 6 · 8) · **코디(7)** | — |
| §7-3 완료 조건 | — | §9 | — |
| §8 SPEC-001 되적기 | 문서 일 | **구현 대상 아님**(§11 끝 줄 · `health` 줄은 W-1 로 뺌) | — |
| §9 다음 범위 | — | **범위 밖** | — |
| §10-1 U-1 · U-2 | 사용자 결정 | 닫힘 — (a) · (a) | 머리말 |
| §10-2 O-1 ~ O-4 · O-7 | `load_seq` 72표 전부 · `DELETE` · 빌드 기록 표 1 · silver 해시 칸 없음 · 이름 | WP-1 · WP-2 — 본문 그대로 | §11 A-2 · A-6 |
| §10-2 O-6 | 지연 FK 확인 | WP-0 | Z-2 ~ Z-5 |
| §10-2 O-5 · O-8 · O-9 | — | 이번에 안 함 | §11 끝 줄 |

## 변경 기록

### 0.1.0 (2026-11-17)

- 새로 씀 — SPEC-003 0.1.0 을 WP 다섯(WP-0 확인 · WP-1 계약 상수 · 모델 · 마이그레이션 · WP-2 적재 CLI · WP-3 DB 판 repository · WP-4 실물 확인 · 마감)으로. 사용자 결정 U-1 · U-2 는 (a) 로 닫힌 값으로 적었다(_RESUME §2 11-17).
- `review-spec-003.md` 의 WARN 4 · NOTE 8 을 §10 에 한 줄씩 넣었다 — 코디 결정 W-1 (a) `health` 새 필드 없음 · W-2 읽는 자리 하나 + 프로세스 env 꼴 + 접속 대상 찍기 · W-3 접속 실패 exit 2 · 필수 env 나눔 · 한 번 읽기 · W-4 첫 WP 네 줄.
- 이 문서가 더한 것(SPEC 되적기 후보 — §11 A): 검사 번호 V11 · V12 · `DATABASE_URL` 을 읽는 자리 = `GoldSettings` · `s_concern_site` · 계층 3표도 `load_seq` 순 · 허브 레포의 두 시험(`test_entrypoint_imports_no_db` · `test_app_main_untouched`)이 묶는 설계 제약.
- 돌려 보지 않은 것: DB · alembic · pytest · 서버(읽기와 `lsof` · `grep` 만). 접속 값 파일 · `.env` 는 열지 않았다.
