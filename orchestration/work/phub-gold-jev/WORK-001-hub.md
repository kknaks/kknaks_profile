---
type: work
id: WORK-001
title: "허브 gold MCP 구현 계획 — 적재 · repository · 도구 8 · REST/MCP · 로컬 진입점 · 시험"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.2.0
created_at: 2026-11-16
updated_at: 2026-11-16
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.4.1 · 검수 PASS r5) ← 계약"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 「SPEC 0.4.1 승인 · WORK → 구현 → 코디 검증까지」 · 브랜치 = 허브 kknaksss/phub-gold-jev base release/v1.2.0)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-002-app.md"
    - "orchestration/work/phub-gold-jev/review-spec-001-002-r5.md"
    - "orchestration/work/phub-gold-jev/review-work-001-002.md (0.1.0 검수 — WORK-001 WARN 2 · NOTE 6 → 0.2.0 에서 반영)"
---

# WORK-001 — 허브 gold MCP 구현 계획

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터) · `HUB-WT` = 허브 새 워크트리 `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · base `origin/release/v1.2.0` = `3750e4c` · 11-16 확인 — 이미 만들어져 있고 변경 0) · `HUB-OLD` = 옛 PR #31 워크트리 `~/orca/workspaces/PROCEDURE-HUB/phub-recommend`(커밋 `2edc190` · **읽기만** — `git show HEAD:<경로>`).
> **계약은 SPEC-001 이다.** 이 문서는 「어느 파일에 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작을 만들지 않는다 — 구현 중 SPEC 과 어긋나는 것을 찾으면 코드를 맞춰 고치지 말고 보고한다.
> 공개 레포 규칙: 코드 · 시험 · 커밋 메시지에 시술 설명 · 원장 문장 · 질문 문장 · 가격 값을 넣지 않는다. 합성 fixture 는 가짜 코드 · 가짜 이름만.

## 0. 요약

- 허브 레포 `backend/` 에 **새 모듈 `app/modules/gold/`** + REST 라우터 + MCP 서버 + **로컬 진입점 `app/gold_main.py`** 를 짓는다. `release/v1.2.0` 의 `app.main` · 기존 라우터 · DB · alembic · Dockerfile 은 건드리지 않는다(SPEC-001 O-7 로컬 = 별도 ASGI).
- WP 넷: **WP-1** 적재 · 해시 · 색인 · repository → **WP-2** service(도구 8 코어) → **WP-3** REST · MCP · 진입점 · health → **WP-4** 시험 마감(T1 ~ T14 · 실물 37 문항 되짚기).
- 로컬 실행 포트 = **18105**(제안 — 옛 틀 18005 · README 의 8005 와 겹치지 않음 · 11-16 에 세 포트 모두 비어 있음을 `lsof` 로 확인).
- 머지 · push · PR · stg 는 이 계획에 없다(SPEC-001 §8 — 이번 판은 로컬 시험까지 · 커밋 · push 는 코디 몫).

## 1. 실제 레포 구조(확인 결과)

`git -C ~/git/PROCEDURE-HUB ls-tree -r --name-only origin/release/v1.2.0 backend/` 로 확인한 것(11-16).

| 확인한 것 | 결과 | 이 계획에서 |
|---|---|---|
| `backend/app/modules/` | `ai_usage` · `catalog` · `glossary` · `guidance` · `knowledge` · `publication` · `recommendation` · `reference_read` · `retrieval` · `safety` · `shared` — **`gold` 없음** | 새 폴더 `backend/app/modules/gold/` |
| `backend/app/router/` | `data` · `glossary` · `glossary_admin` · `health` · `knowledge` · `legacy_prod` · `terminology` — `gold.py` 없음 | 새 파일 `backend/app/router/gold.py` |
| `backend/app/swagger_docs/` | `common` · `data` · `glossary` · `health` · `knowledge` · `metadata` · `terminology` | 새 파일 `backend/app/swagger_docs/gold.py` |
| `backend/app/main.py` · `core/app_factory.py` | `create_app()` 하나 · lifespan 이 DB 연결을 검증(`core/lifespan.py:19-23`) | **안 고친다** — gold 진입점은 따로(`app/gold_main.py` · DB 연결 없음) |
| `backend/app/core/app_builder.py` | `FastAPIBuilder`(create_app → setup_container → add_exception_handlers → add_routers → build) | 그대로 쓴다(옛 틀 `HUB-OLD backend/app/graph_main.py:54-70` 과 같은 꼴) |
| `backend/app/core/exceptions.py` | `DomainError`(`http_status`) · `DomainValidationError` = **400** · `DomainNotFoundError` = 404 · 핸들러가 `{"detail": str(exc)}` | **안 고친다.** SPEC 의 `invalid_argument` 는 422 라 기존 `DomainValidationError` 를 못 쓴다 → gold 모듈 안에 `DomainError` 하위 셋을 둔다(§WP-2) |
| `backend/pyproject.toml` | 의존에 `mcp` 없음 · `httpx` 는 dev 의존 · `dependency-injector` · `pydantic-settings` 있음 | `mcp` 를 더한다(옛 틀 `HUB-OLD backend/pyproject.toml:12` 는 `mcp>=2.3,<3`) · `uv.lock` 갱신 |
| `backend/Dockerfile:27` | `alembic upgrade head && uvicorn app.main:app` | **안 고친다**(stg 진입점은 O-7 stg 쪽 — 배포 승인 때) |
| `backend/envs/` | `.env.example` 만 추적 · 루트 `.gitignore:46-47` 이 `.env*` 를 막고 `backend/envs/.env.example` 만 연다 | `backend/envs/.env.gold`(gitignore 됨)를 gold 설정 파일로 · `.env.example` 에 `GOLD_*` 이름만 더한다(값 빈칸) |
| `backend/tests/` | `conftest.py` 없음 · `tests/integration/` 은 CI 밖 · `tests/legacy_corpus_support.py` 같은 `*_support.py` 관례 | `tests/gold_support.py` · `tests/gold_fixture.py` · `tests/test_gold_*.py`(통합 폴더 밖 — README 「검증」 명령에 걸린다) |
| `backend/README.md` 「검증」(58-71) | `uv run ruff check app tests scripts` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration` | WP 검증 명령의 기준 |
| `AGENTS.md` | 프로젝트 스킬(`be-reviewer` · `task-checker`) 안내뿐 · 코드 규칙은 저장소 밖 문서를 가리킴 | 코드 꼴은 `release/v1.2.0` 의 기존 모듈과 옛 틀을 따른다 |

## 2. 공통 — 모든 WP 에 걸리는 것

### 2-1. 하지 말 것

- **사용자 포트 · 프로세스를 건드리지 않는다** — 8005 · 18005 · 18210 등 이미 떠 있는 것을 죽이거나 그 포트에 띄우지 않는다. 시험은 포트 없이(ASGI transport) 돌린다. 서버를 띄워 확인해야 하면 **18105** 만 쓰고 끝나면 내린다.
- **개발 · 운영 DB 금지.** `DATABASE_URL` 은 `sqlite+aiosqlite:///:memory:` 만 쓴다(README 「검증」). gold 모듈은 DB 를 읽지 않는다 — `app.core.tx` · `app.core.db` 를 import 하지 않는다.
- `backend/envs/.env` 를 열거나 고치지 않는다. docker 를 띄우지 않는다. 외부 API 호출 없음(허브는 LLM · Jev 를 부르지 않는다).
- `HUB-OLD` 워크트리의 파일을 **복사하지 않고** 고치지도 않는다(미커밋 8 · 미추적 2 가 있다 — `$W/_RESUME.md` §1). 틀만 보고 새로 쓴다(SPEC-001 §7).
- CSV · `questions.csv` 내용 · 원장 확인 목록의 글을 레포에 넣지 않는다.
- 커밋 · push · PR 은 코디 몫이다. 워크트리에 변경만 남긴다.

### 2-2. 코드 레포 allowed_paths

| 허용 | 무엇 |
|---|---|
| `backend/app/modules/gold/**` | 새 모듈 전부 |
| `backend/app/router/gold.py` · `backend/app/swagger_docs/gold.py` · `backend/app/gold_main.py` | 새 파일 |
| `backend/tests/gold_support.py` · `backend/tests/gold_fixture.py` · `backend/tests/test_gold_*.py` | 새 시험 |
| `backend/pyproject.toml` · `backend/uv.lock` | `mcp` 의존 추가 한 줄 + lock |
| `backend/envs/.env.example` | `GOLD_*` 이름(값 빈칸)만 덧붙임 |
| `backend/README.md` | 「gold 로컬 실행 · 검증」 한 절 덧붙임(기존 문단은 안 고침) |

이 밖(`app/main.py` · `core/**` · 기존 라우터 · `alembic/` · `Dockerfile` · `frontend/` · `docs/` · `.github/`)은 건드리지 않는다. 필요해 보이면 멈추고 묻는다.

### 2-3. 데이터 env(이름 = SPEC-001 §2-2 그대로 · 로컬 경로)

| env | 로컬 값 | 필수 |
|---|---|---|
| `GOLD_CSV_DIR` | `$SM/gold`(15표 + `questions.csv`) | 필수 |
| `GOLD_SOURCE_REF_PATH` | `$SM/silver/source_ref.csv` | 필수 |
| `GOLD_HIERARCHY_DIR` | `$SM/silver`(`concern.csv` · `adverse.csv` · `condition.csv`) | 필수 |
| `GOLD_LEDGER_CHECK_PATH` | `$SM/notes/ledger-check-list.csv` | 필수 |
| `GOLD_EXPECTED_HASH` | SPEC-001 §2-3 3 의 11-16 값 | 선택 |
| `GOLD_PAGE_LIMIT_DEFAULT` · `GOLD_PAGE_LIMIT_MAX` | 100 · 500(O-6 제안값) | 선택 |
| `GOLD_API_PREFIX` · `GOLD_MCP_MOUNT_PATH` · `GOLD_MCP_RESULT_MAX_CHARS` | `/procedure-hub/gold` · `/procedure-hub/gold-mcp` · 설정값 | 선택(기본값) |

다섯 파일이 11-16 에 그 자리에 있음을 `ls` 로 확인했다. 설정은 `backend/envs/.env.gold`(gitignore) 또는 프로세스 env 로 준다 — 프로세스 env 가 앞선다(옛 틀 `HUB-OLD backend/app/modules/gold/config.py:15-20`). 문서 · 코드에 절대 경로를 박지 않는다(옛 `tests/gold_support.py:17-21` 처럼 기본 경로를 코드에 넣지 않는다 — env 없으면 skip).

### 2-4. 검증 명령(전 WP 공통 틀 — `HUB-WT/backend` 에서)

```bash
uv sync
uv run ruff check app tests scripts
# 합성 시험(데이터 env 없음 — 실물 시험은 skip 된다)
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_<이 WP 것>.py
# 실물 시험(데이터 env 있음)
GOLD_CSV_DIR=$SM/gold GOLD_SOURCE_REF_PATH=$SM/silver/source_ref.csv \
GOLD_HIERARCHY_DIR=$SM/silver GOLD_LEDGER_CHECK_PATH=$SM/notes/ledger-check-list.csv \
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_<이 WP 것>.py
```

- **WP 마다는 그 WP 의 시험만** 돌린다. README 「검증」 의 전체 명령(`uv run pytest --ignore=tests/integration`)은 **WP-4 끝에 한 번** 돌려 기존 시험이 그대로 통과하는지 본다.
- 실물 시험은 `GOLD_CSV_DIR` 과 보조 입력 env 가 없으면 **skip** 이다(SPEC-001 §9 · 옛 틀 `HUB-OLD backend/tests/gold_support.py:25-27`). skip 수 · 통과 수를 둘 다 보고한다 — 「skip 이라 통과」 를 완료로 적지 않는다.

### 2-5. 로컬 실행(사용자 e2e 용)

```bash
cd ~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev/backend
uv sync
GOLD_CSV_DIR=$SM/gold GOLD_SOURCE_REF_PATH=$SM/silver/source_ref.csv \
GOLD_HIERARCHY_DIR=$SM/silver GOLD_LEDGER_CHECK_PATH=$SM/notes/ledger-check-list.csv \
uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18105
```

| 무엇 | 주소 |
|---|---|
| health | `http://127.0.0.1:18105/procedure-hub/gold/health` |
| REST 도구 | `http://127.0.0.1:18105/procedure-hub/gold/{resolve,scope,neighbors,facets,concern-candidates,pair,evidence}` |
| API 문서 | `http://127.0.0.1:18105/procedure-hub/gold/api-docs` |
| MCP(Streamable HTTP) | `http://127.0.0.1:18105/procedure-hub/gold-mcp/mcp` |

- gold 진입점은 DB 를 안 쓴다 — `DATABASE_URL` 없이 뜬다. 필수 env 가 하나라도 없으면 **시작 실패**다(SPEC-001 §2-3 5).
- 띄우기 전 `lsof -nP -iTCP:18105 -sTCP:LISTEN` 으로 비어 있는지 본다. 차 있으면 죽이지 말고 다른 포트를 골라 보고한다.

## 3. WP-1 — 적재 · 해시 · 색인 · repository

**목표**: 필수 env 의 21 파일(gold 15 + `questions.csv`(해시만) + `source_ref` + 보조 4)을 한 번 읽어 메모리 색인을 세우고, service 가 쓸 조회 메서드를 여는 repository 를 만든다.

**SPEC-001 대응**: §2-1(파일 · X1 ~ X6) · §2-2(env) · §2-3(적재 · 해시 · 실패 조건 · integrity 셈) · §3(계층 표의 repository 행) · §3-1(색인 전부) · 부록 A(헤더 계약) · §9 T1 · T2 · T3 · O-3(로컬 = (a)) · O-5(env 이름) · O-12 ① ② ③ ⑥.

**맨 먼저(코드를 한 줄도 쓰기 전)**: 워크트리가 깨끗한 지금 README 「검증」 전체 명령(§2-4 끝 줄 · WP-4 「검증」 의 마지막 두 줄)을 **한 번** 돌려 base(`3750e4c`)의 통과 수 · skip 수를 적어 둔다. WP-4 완료 조건 5 가 이 수와 견준다 — WP-4 때는 변경이 쌓여 그 자리에서 base 를 못 잰다.

**만들 파일**

| 파일 | 무엇 |
|---|---|
| `backend/app/modules/gold/__init__.py` | 모듈 설명 한 줄 |
| `backend/app/modules/gold/config.py` | `GoldSettings`(pydantic-settings · `envs/.env.gold` · `extra="ignore"`) — §2-3 표의 env. 필수 넷은 기본값 없이 빈 문자열 → 적재 때 「없음」 으로 판정 |
| `backend/app/modules/gold/headers.py` | **헤더 계약 상수** — 부록 A 를 그대로 옮긴 표(gold 15표의 전 칸 · `source_ref` 4 칸 · 보조 입력의 읽는 칸 · 속성 쪽 맞춤 칸 7 줄). T3 가 이 상수와 실제 CSV 헤더를 기계 대조한다 |
| `backend/app/modules/gold/inputs.py` | 파일 읽기(UTF-8 BOM · `,` · **전 칸 문자열**) · 파일별 `sha256` · 행 수 · gold 해시(`gold-check.py:46-50` 식 — 폴더의 `*.csv` 이름순 · 16 파일) · 보조 해시(같은 식 · 5 파일) · 실패 조건 → `GoldLoadError` |
| `backend/app/modules/gold/memory.py` | `GoldMemory` — §3-1 의 색인 전부(표별 키 → 행 · `gid` → 행 · 계층 `code ↔ parent_code` · 원장 확인 코드 → `id[]` · 속성 쪽 「칸 값(항목) → 행」) · integrity 셈 셋 |
| `backend/app/modules/gold/repository.py` | `GoldRepository`(Protocol — 조회 메서드만) + `CsvMemoryGoldRepository`(지금 구현). 메서드는 §3-1 색인 하나에 하나 + 「상위 · 하위 코드 묻기」 · 「코드의 원장 확인 id 묻기」 · 「적재 기록 읽기」 |

**옛 틀에서 가져올 것(틀만)**

| 옛 자리 | 가져오는 것 | 새로 쓰는 것 |
|---|---|---|
| `HUB-OLD backend/app/modules/gold/config.py:15-24` | pydantic-settings · 별도 env 파일 · prefix 설정 꼴 | env 이름 · 옛 손잡이(`:27-60`)는 전부 버림 |
| `…/gold/inputs.py:16-63` | 「입력 파일 목록 상수 → 읽기 → 파일 해시」 틀 | 목록 = CSV · 해시 식 = SPEC §2-3(옛 sha16 아님) |
| `…/gold/memory.py:13-60` | 「한 번 읽어 dict 색인」 틀 | 색인 키 = SPEC §3-1 |
| `…/gold/repository.py` | **가져오지 않는다**(옛 것은 DB 발행본 읽기) | Protocol + 메모리 구현 |

**지킬 것(구현 메모)**

- 원장 확인 목록은 읽는 즉시 `id` 와 뽑은 코드만 남기고 **글 칸을 버린다**(X4 · X5). 코드 추출식 = `$SM/gold/gold-build.py:648-651`(코드 접두어 9종 + `-` + 숫자 — 접두어 목록은 그 줄에서 읽어 상수로 옮긴다).
- 계층 3표는 `code` · `parent_code` 만 남긴다(X2).
- `questions.csv` 는 **바이트 해시만** — 행을 읽지 않는다(`rows = null` · `kind = hash_only`).
- service 가 CSV 행 dict · 색인 dict 를 직접 만지지 않게 repository 는 **행을 읽기 전용 매핑으로** 돌려준다(SPEC §3 「DB 구현으로 바꿀 때 service 가 그대로」). repository 메서드 이름은 여기서 정한다(SPEC §3-1 끝 줄 「이름은 WORK 에서」): `entries_by_norm` · `entries_by_entity` · `entries_by_table` · `scope_by_subject` · `scope_by_holder` · `profile_of` · `indication_by_asked` · `rows_by_target(table, …)` · `rows_by_value(table, column, code)` · `pair_by_from` · `pair_by_to` · `package_by_id` · `package_by_item` · `package_by_concern` · `offer_by_id` · `offer_by_item` · `offer_by_procedure` · `offers_all` · `node` · `edges_out` · `edges_in` · `evidence_of` · `source_refs_of` · `row_by_gid` · `rows_by_attr(table, column, value)` · `ancestors(table, code)` · `descendants(table, code)` · `ledger_ids(code)` · `load_record()`. (이름은 구현 때 다듬어도 된다 — 「색인 하나에 하나」 만 지킨다.)

**완료 조건**

1. 실물 env 로 `CsvMemoryGoldRepository` 를 세우면 21 파일의 행 수 = 파일 행 수이고 gold 해시 = SPEC §2-3 3 의 11-16 값이다. 보조 입력을 읽어도 gold 해시가 같다(T1).
2. `load_record()` 의 `gold` + `hash_only` 16 줄로 다시 센 값 = `gold_hash` · `source_ref` + `aux` 5 줄로 다시 센 값 = `aux_hash`(T1 · §4-8).
3. 합성 fixture 로: 필수 env 없음 · 파일 없음 · gold 헤더 다름 · 보조 입력의 쓸 칸 없음 · `GOLD_EXPECTED_HASH` 다름 → 전부 `GoldLoadError`(T2). `GOLD_EXPECTED_HASH` 없음 → 적재 성공 · `expected_hash_checked = false`.
4. `headers.py` 의 표가 실물 CSV 헤더와 **양방향**으로 맞는다 — 부록 A 의 칸이 헤더에 전부 있고 · gold 15표 헤더에서 이름에 `site` · `material` · `method` · `anatomy` 가 든 칸이 속성 쪽 맞춤 칸 7 줄에 전부 있다(T3).
5. 적재한 메모리에 원장 확인 목록의 글 칸 · 계층 3표의 `code` · `parent_code` 밖 칸이 없다(객체를 훑어 확인하는 시험 한 건).
6. integrity 셈: 실물에서 「근거 없는 gold 행」 0 · 「`source_ref` 짝 없는 참조」 0 · 「부모 없는 `parent_code`」 0(SPEC §2-3 6).

**검증**: `tests/test_gold_load.py`(T1 실물 · T2 합성 · 완료 조건 5 · 6) · `tests/test_gold_contract.py`(T3 — 헤더 대조는 실물 · 합성 fixture 가 `headers.py` 와 같은 헤더인지는 합성).

## 4. WP-2 — service(도구 8 코어)

**목표**: 도구 8 의 규칙을 HTTP · MCP 를 모르는 코어 하나로 짓는다. 입력 검증 · 쪽 넘김 · `layer` · `hier` · `attr` · `ledger_check[]` · 응답 머리가 전부 여기 있다.

**SPEC-001 대응**: §3(service 행) · §4-0(공통 전부 — 대상 표기 · 응답 머리 · `total` 단위 · 「있음」 경계 · 행 필드 · 원장 확인 · 쪽 넘김 · 오류) · §4-1 ~ §4-8 · §5-1 ~ §5-7 · §6(되짚기 키) · O-4(= (a)) · O-6 · O-9(= (a)) · O-12 ④ ⑤ ⑦ · O-16(= (a)) · O-18(= (a)).

**만들 파일**

| 파일 | 무엇 |
|---|---|
| `backend/app/modules/gold/errors.py` | `GoldLoadError` · `GoldInvalidArgument`(422) · `GoldNotFound`(404) · `GoldCursorInvalid`(400) — 뒤 셋은 `app.core.exceptions.DomainError` 하위(`http_status` 만 다름) · 메시지는 `<코드 이름>: <사유>` 꼴(`invalid_argument: …`). 기존 핸들러가 `{"detail": …}` 로 내고 MCP 는 같은 문구의 tool 오류가 된다 |
| `backend/app/modules/gold/cursor.py` | 불투명 cursor — (`gold_hash`, `aux_hash`, 도구, 응답을 바꾸는 입력의 해시, offset) 를 묶어 encode/decode. build 가 다르거나 입력이 다르면 `GoldCursorInvalid`(O-12 ⑤) |
| `backend/app/modules/gold/ranges.py` | §5-2 의 고정 표 — 범위 8 의 시작 표(`in_range`) · 속성 4표는 늘 참 · `resolve` 표 순서(`gold-build.py:633` 의 `order` 목록을 상수로) |
| `backend/app/modules/gold/resolve.py` | §5-1 R1 ~ R6 — `norm`(= `gold-build.py:126-127` 식) · 조사 16(옛 `resolve.py:19` 목록만) · 낱말 자르기 O-4 (a)(공백 낱말 + 이웃 낱말 이어 붙임) · 목록 꼴 |
| `backend/app/modules/gold/service.py` | `GoldState`(Singleton — repository + 적재 기록) · `GoldToolService`(요청마다) — 도구 8 메서드와 공통 머리(`build` · `request` · `total` · `next_cursor`) · 쪽 넘김 |
| `backend/app/modules/gold/facets.py` | `facets` 의 세 길(대상 쪽 · 값 쪽 · 속성 쪽) + `offer_name_contains` + 계층 펼침 세 자리 + `counts` |
| `backend/app/modules/gold/pairs.py` | `pair` 규칙 1 ~ 5 · `same_day_packages[]` · `a_side` · `a_layer` · `b_layer` |
| `backend/app/modules/gold/concern.py` | `concern_candidates` — `groups` · `modality_only[]` · `unreached[]` · `counts` |
| `backend/app/modules/gold/ledger.py` | `ledger_check[]` 조립 — 대조 코드 · `on` · 순서 · 겹침(§4-0 · §5-6 L1 ~ L4) |

(파일 나눔은 제안이다 — 한 파일이 커지지 않게 도구별로 가른 것. 합쳐도 계약은 같다.)

**옛 틀에서 가져올 것**

| 옛 자리 | 가져오는 것 |
|---|---|
| `HUB-OLD backend/app/modules/gold/service.py:1` | 「REST · MCP 공용 코어」 한 클래스 꼴 — **`:38-40` 의 「발행본 없어도 경고만 하고 뜸」 은 가져오지 않는다** |
| `…/gold/resolve.py:19` | 조사 16 개 목록**만**. `strip_particle`(`:22-31`)의 「뗀 뒤 완전 일치일 때만 · 원 낱말 먼저 · 긴 조사 먼저」 순서는 같은 뜻으로 새로 쓴다. 옛 4단계의 끝말 떼기 · 접두는 안 가져온다(R4) |
| `…/gold/tools.py` · `pairs.py` · `facts.py` · `ids.py` · `build.py` · `application.py` | **안 가져온다**(봉투 · intent · 빌드 — SPEC §7 「버림」) |

**도구별 확인 표(SPEC 절 → 꼭 시험으로 잡을 것)**

| 도구 | 절 | 꼭 잡을 것 |
|---|---|---|
| `resolve` | §4-1 · §5-1 | 겹침은 고르지 않고 전부 · 같은 (`entity_table`, `entity_code`) 한 번만 · 순서(표 순서 → 「이름」 먼저 → `gid`) · `range` 는 후보를 **버리지 않는다** · 후보 0 = `200` · 목록 꼴(`text` 없이 `range`/`tables` · 쪽 넘김 · `counts{by_table, entities}` · 둘 다 없으면 `invalid_argument`) · 비슷함 계산 없음 |
| `scope` | §4-2 · §5-3 | `subject` 방향만 · `roles` 거름 · `counts_by_role` · `g_scope` 에 없으면 `not_found` |
| `neighbors` | §4-3 | `edge_types` 필수(1 이상) · `out`/`in` · `node` 4 칸만 · 순서(`edge_type` → 이웃 `node_id` → `edge_id`) · `g_node` 에 없으면 `not_found` · 「닫히지 않는 것」 셋을 도구 설명 문구에 |
| `facets` | §4-4 · §5-3 ~ §5-7 | 맞춤 규칙 표 9 facet · `roles` 기본 `자기` · `물려받음` · 값 쪽 · 속성 쪽이면 `roles` 무시하고 `request` 에 되돌림 · `layer`(자기여도 붙임 · `scope_gid`) · `filters` 는 그 표 헤더 칸만 · `hier` 세 자리(자손 전부) · 속성 쪽(「—」 조합 = `invalid_argument` · 항목 단위 일치 · `attr.column` 전부 · `counts.by_column` · `subjects`) · `offer_name_contains`(`norm` 부분 일치 · `node` 와 함께 = `invalid_argument` · 다른 facet = `invalid_argument` · 빈 문자열 = `invalid_argument` · 0 행 = `200`) · `ledger_check[]` |
| `concern_candidates` | §4-5 | `total` = 묶음 수 · 쪽 밖 목록은 첫 쪽에만 · `site` 0 이면 0 그대로 + `counts.unfiltered_rows`(O-9 (a)) · 계층 입력 없음 |
| `pair` | §4-6 | 규칙 1 ~ 5 · `b` 없으면 한 끝이 빈 37 행도 나옴 · 고르지 않음(엇갈림 · 진 쪽 전부) · `same_day` 빈칸 그대로 · `package_kinds` 의 role 집합에 `하위 제품` · **`b` 없이 `package_kinds` 만 준 꼴은 SPEC 에 뜻이 없다 — 구현자가 고르지 않는다 · §9 N1-1 의 값으로** |
| `evidence` | §4-7 · §6 | `total` = `source_refs` 를 편 줄(0 인 참조는 1줄) · `fields` 로 잇기(`|` · `(행 전체)`) · `g_edge` = `invalid_argument` |
| `health` | §4-8 | `files[]` 21 줄 · `kind` 4종 · `questions.csv` 는 `rows = null` · `integrity` · `aux` · 글 칸 없음 |
| (공통) | §4-0 · §5-4 | 숫자 칸 문자열 그대로(V6) · `polarity` 로 안 거름(V4) · `price_mid_raw` 로 정렬 · 계산 안 함(V5) · `limit` 은 쪽 크기 — 끝까지 넘기면 `total` 전부 · 쪽 밖 목록에 한도 없음 · `counts*` 는 모든 쪽에 |

**완료 조건**

1. 합성 fixture 위에서 위 표의 「꼭 잡을 것」 이 전부 시험으로 선다(T6 결정론 · T9 계층 · T10 원장 확인 · T11 「있음」 경계 · T12 속성 쪽 · T13 입구 목록 · T14 상품 이름 — 합성 몫).
2. 모든 도구 응답의 행 필드 ⊂ `headers.py` 의 그 표 헤더 ∪ SPEC 부록 A 끝 단락의 계산 필드 목록(T3 의 응답 쪽 — 응답을 훑어 기계 대조).
3. 같은 입력 두 번 → 순서까지 같은 응답 · cursor 로 끝까지 넘긴 쪽 단위의 합 = `total`(도구별 단위 — §4-0 표) · 쪽 밖 목록은 첫 쪽에만(T6).
4. service 코드가 `GoldRepository` Protocol 메서드만 부른다 — `memory.py` · `inputs.py` 를 import 하지 않는다(`rg` 로 확인하는 시험 또는 검수 항목).
5. 허브에 「상위 N」 · 점수 · 순위 · 철자 거리로 빼거나 고르는 입력 · 코드가 없다 — `rg -n "score|rank|top_n|distance" app/modules/gold` 를 돌려 **걸린 줄을 전부 보고에 적고, 줄마다 입력 · 정렬 · 거름 코드가 아님을 밝힌다**(도구 설명 문구의 「순위를 매기지 않는다」 류는 걸릴 수 있다 — 입력 · 정렬 · 거름 코드로 걸린 줄이 0 이어야 한다).

**검증**: `tests/test_gold_tools_synthetic.py`(도구별) · `tests/test_gold_contract.py`(응답 필드 대조). 실물 몫은 WP-4.

## 5. WP-3 — REST · MCP · 진입점 · health

**목표**: 같은 코어를 REST 와 MCP 두 입구로 내고, 로컬에서 한 포트로 띄우는 ASGI 진입점을 만든다.

**SPEC-001 대응**: §1-4(코드 자리 · 이름) · §3(router · MCP 행 · Singleton + Factory) · §4-0(REST ↔ MCP 대응 표 · MCP 공통 · 오류 대응) · §4-8 · §7(틀 표의 서버 골격 · MCP 틀 · 라우터 · DI · 의존) · §9 T7 · O-5 · O-6(MCP 결과 크기) · O-7(로컬 = (a)).

**만들 파일**

| 파일 | 무엇 |
|---|---|
| `backend/app/modules/gold/container.py` | `GoldContainer` — `gold_state` Singleton · `gold_tools` Factory · wiring = `app.router.gold` |
| `backend/app/router/gold.py` | `GET` 8(`/resolve` · `/scope` · `/neighbors` · `/facets` · `/concern-candidates` · `/pair` · `/evidence` · `/health`) — 쿼리 → 코어 호출 → JSON 그대로. **쿼리 인자는 전부 선택으로 선언한다**(아래 「지킬 것」 1). 목록 입력(`roles` · `edge_types` · `classes` · `package_kinds` · `tables`)은 콤마 목록 · `filters` 는 `칸=값` 되풀이(쿼리 꼴은 여기서 정해 swagger 설명에 적는다) |
| `backend/app/swagger_docs/gold.py` | 태그 · 설명 · 오류 응답 예(422 · 404 · 400) |
| `backend/app/modules/gold/mcp_server.py` | 서버 이름 `procedure-hub-gold` · 도구 8(이름 · 입력 · 기본값 = REST 와 같음) · `readOnlyHint` · 결과 크기 meta(설정값) · `DomainError` → 같은 문구의 `ToolError` · 도구 설명 문구(§4-3 「닫히지 않는 것」 · §4-1 「고르지 않는다」 등 SPEC 이 「도구 설명에 적는다」 고 한 것) |
| `backend/app/gold_main.py` | ASGI 진입점 — **`create_gold_app(settings)` 팩토리**를 열고 모듈 전역 `app` 은 그것을 한 번 부른 값이다(아래 「지킬 것」 2). lifespan 에서 **적재만**(DB 연결 없음) → 실패면 예외로 시작 실패 · MCP `streamable_http_app(stateless_http=True, json_response=True)` 를 **한 번** 만들어 `GOLD_MCP_MOUNT_PATH` 에 마운트 · lifespan 에서 `mcp.session_manager.run()` · `Server-Timing` 미들웨어 |
| `backend/pyproject.toml` · `backend/uv.lock` | `mcp` 의존 추가(판은 옛 틀 `mcp>=2.3,<3` — 설치되는 실제 판의 import 경로를 소스로 확인하고 고정) |
| `backend/envs/.env.example` · `backend/README.md` | `GOLD_*` 이름 · 「gold 로컬 실행 · 검증」 절(§2-5 내용) |

**옛 틀에서 가져올 것(틀만)**

| 옛 자리 | 가져오는 것 | 다르게 하는 것 |
|---|---|---|
| `HUB-OLD backend/app/graph_main.py:27-30` | 컨테이너 → MCP 서버 → `streamable_http_app` 한 번 | 원장 MCP(`:23 · 32 · 46-47 · 81-82`)는 **없다**(SPEC §7 끝 행) |
| `…/graph_main.py:35-49` | lifespan 에서 `session_manager.run()` 에 들어가는 꼴 | `db_provider` 두 줄(`:39-40 · 49`)은 **없다** — CSV 적재만 |
| `…/graph_main.py:52-83` | `FastAPIBuilder` 조립 · `Server-Timing` 미들웨어 · mount | prefix · 이름은 SPEC §1-4 |
| `…/gold/mcp_server.py:22-23 · 30 · 55-59` | 서버 이름 · `ToolAnnotations(readOnlyHint=True …)` · 결과 크기 meta · `_call`(도메인 예외 → `ToolError`) | 도구 정의 · 설명 문구(`:24-51`)는 전부 새로 |
| `…/gold/container.py:14-18` | Singleton 상태 + Factory 서비스 | — |
| `…/router/gold.py:21-36` | `Depends(Provide[…])` · 콤마 목록 `split` · `JSONResponse` 그대로 내기 | 경로 · 입력은 SPEC §4 · health 의 DB 확인(`:40` 이후)은 없다 |

**지킬 것(구현 메모)**

1. **입력 검사는 코어 한 곳에서 한다.** 라우터의 쿼리 인자 · MCP 도구의 입력은 **전부 선택(기본값 없음 = 빠짐)** 으로 받아 그대로 코어에 넘기고, 필수 · enum · 한도 · `표:코드` 꼴 검사는 service 가 한다(SPEC-001 §3 service 행 「입력 검증」 · §4-0 `invalid_argument`). 라우터가 필수 쿼리를 FastAPI 필수 인자로 선언하면 코어에 닿기 전에 FastAPI 가 목록 꼴 본문의 422 를 내고, MCP 도 입력 스키마의 필수 검사가 먼저 걸리면 문구가 달라진다 — 그러면 「REST 문구 = MCP 문구」 가 깨진다. MCP 도구 스키마에도 `required` 를 두지 않는다(필수임은 도구 설명 문구로 알린다).
2. **진입점은 팩토리로 연다.** `create_gold_app(settings: GoldSettings) -> FastAPI` 가 컨테이너 · MCP 서버 · lifespan 을 그 설정으로 조립한다. 모듈 전역 `app = create_gold_app(GoldSettings())` 는 `uvicorn app.gold_main:app` 용 한 줄이다. 설정 · 컨테이너가 import 때 굳으면(옛 틀 `HUB-OLD backend/app/graph_main.py:27-30` 꼴) env 를 바꿔 가며 「시작 실패」 를 시험할 수 없다.
3. **시험은 lifespan 을 직접 연다.** `httpx` 의 ASGI transport 는 lifespan 을 돌리지 않는다 — `test_gold_rest.py` · `test_gold_mcp.py` 는 `create_gold_app(<합성 fixture 설정>)` 으로 만든 앱의 lifespan 컨텍스트(적재 · `session_manager.run()`)에 들어간 뒤 요청한다. 「필수 env 하나를 빼면 시작 실패」 는 그 설정으로 만든 앱의 lifespan 진입이 예외를 내는지로 본다.
4. `mcp` 는 설치되는 실제 판의 import 경로(`MCPServer` · `ToolError` 자리)를 소스로 한 번 확인하고 쓴다(§10 H-4).

**완료 조건**

1. `app.gold_main:app` 이 필수 env 로 뜨고 `GET <prefix>/health` 가 `200` · `build.gold_hash` = 11-16 값을 낸다. 필수 env 하나를 빼면 **프로세스가 시작에 실패한다**(lifespan 예외 — `create_gold_app(그 설정)` 의 lifespan 을 직접 열어 확인 · 「지킬 것」 2 · 3).
2. 같은 입력에 REST 응답 JSON 과 MCP 도구의 structured 출력이 **같다**(T7 — 합성 fixture · 도구 8 각각 한 건 이상 · `build.loaded_at` 까지 같은 상태를 보므로 같다).
3. 오류 대응: `invalid_argument` → 422 · `not_found` → 404 · `cursor_invalid` → 400 이고 MCP 는 같은 문구의 tool 오류다. **문구까지 대조한다** — 도구 8 중 필수 입력이 있는 것마다 「필수 인자 빠짐」 한 건에서 REST 본문의 `detail` 문자열 = MCP tool 오류 문구(글자 그대로 같음 · 「지킬 것」 1)이고, REST 본문이 FastAPI 기본 검증 꼴(목록)이 아니다. enum 밖 · 한도 밖도 한 건씩 같은 대조를 한다.
4. `app.gold_main` 을 import 해도 `app.core.tx` · `app.core.db` 가 import 되지 않는다(DB 없는 진입점 — `sys.modules` 를 보는 시험 한 건). `app.main` · `core/app_factory.py` 의 diff 는 0 이다.
5. MCP `list_tools` 가 8 개를 내고 전부 `readOnlyHint` 다.

**검증**: `tests/test_gold_rest.py`(ASGI transport — 포트 없음 · lifespan 은 시험이 직접 연다) · `tests/test_gold_mcp.py`(T7 — MCP 클라이언트를 ASGI transport 로 · lifespan 직접 · 옛 앱 틀 `APP-OLD clinic_chat/clients/hub_mcp.py:3-10` 의 import 경로 메모 참고). 서버를 실제로 띄우는 확인은 WP-4 의 실물 확인 한 번뿐이다.

## 6. WP-4 — 시험 마감 · 실물 되짚기

**목표**: SPEC-001 §9 T1 ~ T14 를 전부 세우고, 실물 gold 로 37 문항의 `gold_pointers` 를 되짚는다. 전체 검증을 한 번 돌리고 로컬 서버를 한 번 띄워 본다.

**SPEC-001 대응**: §9 전부(T1 ~ T14 · 문항별 기대 표 · fixture 규칙) · §6(T5 근거) · §5-3 · §5-4(T8).

**만들 파일**

| 파일 | 무엇 |
|---|---|
| `backend/tests/gold_fixture.py` | 합성 fixture **생성기** — 가짜 코드 · 가짜 이름으로 15표 + `questions.csv`(해시용 빈 껍데기) + `source_ref` + 계층 3표 + 원장 확인 목록을 `tmp_path` 에 쓴다. **레포에 CSV 파일을 두지 않는다.** 꼭 들어갈 모양: 3단 계층(손자 코드) · 한 끝이 빈 pair · 엇갈린 `same_day` · 충돌 짝 · 「계열 층만」 · 못 닿은 행 · 여러 값 칸(` · `) · 부분 문자열만 같은 항목 · `g_entry` 에만 있는 값 · 원장 확인에 걸린 코드(요청 쪽 · 상품 쪽 · 양쪽 겹침) |
| `backend/tests/gold_support.py` | `needs_gold` skip 표지(필수 env 넷이 다 있고 파일이 있을 때만) · 실물 repository 를 한 번만 세우는 캐시 · `questions.csv` 에서 `id` · `range` · `entry_text` · `gold_pointers` · `status` 만 읽는 로더(**시험 실행 때 로컬에서 읽을 뿐 값은 코드에 없다**) |
| `backend/tests/test_gold_real.py` | 실물 시험 — T1 · T4 · T5 · T6 · T8 · T9 · T10 · T11 · T12 · T13 · T14 |
| (WP-1 ~ 3 의 시험 파일) | 합성 몫 보강 |

**T4(37 문항 되짚기)를 세우는 법** — 문항별 호출 명세는 앱 쪽(WORK-002 WP-6)이 만든다. 허브 시험은 그것에 기대지 않고 `questions.csv` 만으로 선다:

1. 문항의 `entry_text`(안 풀리면 `question`)를 `resolve(text, range)` 에 넣어 `in_range` 후보를 **전부** 입구로 둔다.
2. 그 범위의 도구 길(SPEC §5-2 표 · §9 문항별 표)을 입구마다 **좁힘 입력 없이** 부른다 — `pair` 는 `a` 만 · `facets` 는 `filters` 없이 · role 은 §5-2 의 그 범위 값 · 쪽 넘김 끝까지 · 쪽 밖 목록 포함. Q33 은 `offer_name_contains` 길(입력 = `entry_text`).
   - **동시 가능 범위는 한 가지를 더 부른다**: `resolve` 가 낸 `in_range` 입구의 **쌍마다** `pair(a, b, package_kinds = 그 범위의 값)` — 순서 없는 쌍 전부 · 입구가 하나뿐이면 이 호출은 없다. 그 범위의 패키지 행은 `pair` 의 `same_day_packages[]` 로만 나오고 그 목록은 `package_kinds` 를 줘야 생긴다(SPEC §9 문항별 표 「`pair`(전 갈래 · 패키지)」 · §4-6 입력 표 · 규칙 3). `package_kinds` 는 범위 표가 고정한 입력이라 좁힘이 아니다(SPEC-002 BR1 (i) 와 같은 뜻). 37 표본 중 패키지 행을 가리키는 것은 10 이고 그중 Q19 · Q21 의 3 개씩이 이 길로만 되짚힌다(Q17 의 4 개는 `facets` package 길 — 검수 W1-1 셈). `b` 없이 `package_kinds` 만 주는 꼴은 쓰지 않는다(SPEC 에 뜻이 없다 — §9 N1-1).
3. 나온 `gid` 합집합 ⊇ 그 문항의 `gold_pointers` 를 본다. 좁힘 없이 부른 것이므로 답 키(WP-6)보다 넓다 — 이 시험은 「표본 ⊂ 도구 길」 만 본다(SPEC §9 T4 문구 그대로).
4. `gold_pointers` 가 빈 문항(Q10)은 `200` · `total` 0 과 `ledger_check[]` 를 본다.
5. **안 되짚히는 문항이 나오면 시험을 문항별 예외로 메우지 않는다** — 문항 id · 안 나온 `gid` · 그 `gid` 의 표(`gid` 접두) · 부른 호출을 보고에 적는다. 「SPEC 의 도구 길 구멍」 이라고 적기 전에 위 2 의 호출(동시 가능의 쌍 호출 포함)을 다 불렀는지 먼저 본다 — 시험 방법의 빠짐과 SPEC 의 구멍을 갈라 적는다.

**문항별 「따로 볼 것」**(SPEC §9 표 — 전부 실물 시험으로): Q04(상위 제품 진술이 하위 제품에 안 붙음 — S4) · Q10(`total` 0 · `not_found` 아님 · `LCK-010`) · Q12(행 있음 · `onset_text` · `duration_text` 빈칸 그대로) · Q35(회복과 부작용 지속이 다른 facet) · Q17(`hier` = `exact` 0 행 · `expand` 4 행) · Q19(충돌 행 둘 다) · Q21(`same_day` 채운 행 0 — 빈칸 유지) · Q24 · Q26(`self_pair`) · Q29(금기 행 전부 — 쪽 넘겨 끝까지) · Q33(`offer_name_contains` · 행 1 · `reach` 못 닿음 · `LCK-308` `on` = `rows`).

**완료 조건**

1. T1 ~ T14 가 전부 시험 함수로 있고(시험 이름에 `T<번호>` 를 넣어 대응이 보이게), **데이터 env 로 돌렸을 때 skip 0 · 실패 0** 이다. 데이터 env 없이 돌렸을 때는 실물 시험만 skip 이고 합성은 전부 통과한다.
2. T4: 37 문항 중 `gold_pointers` 가 있는 문항 전부에서 포인터 ⊂ 도구 길 결과(안 되는 문항 0 — 있으면 목록으로 보고하고 완료로 적지 않는다).
3. T5: T4 의 모든 `gid` 에 `evidence` → 참조 1 이상 · `source_ref` 1 이상.
4. T12 · T13 실물: 속성 4표 전 코드 × 맞춤 facet 의 `total` = 직접 센 수 · 입구 목록의 `counts.entities` = SPEC §5-2 아래 셈(표 14 개 값).
5. README 「검증」 전체 명령이 통과한다 — 기존 시험의 통과 수 · skip 수가 base(`3750e4c`)와 같다(**WP-1 맨 먼저 재 둔 수**와 견줘 함께 보고 — §3).
6. 로컬 서버를 18105 에 한 번 띄워 `health` 와 도구 한 건을 `curl` 로 받고 내린다(응답의 `gold_hash` · `total` 만 보고에 적는다 — 행 본문은 적지 않는다).
7. `git status --porcelain` 이 §2-2 allowed_paths 안의 파일뿐이다.

**검증**

```bash
# 합성만
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_*.py -q
# 실물 포함(§2-4 의 env 넷 + GOLD_EXPECTED_HASH)
… uv run pytest tests/test_gold_*.py -q -rs
# 마지막에 한 번 — README 「검증」
uv run ruff check app tests scripts
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q
```

## 7. 순서 · 의존

```
WP-1 ──▶ WP-2 ──▶ WP-3 ──▶ WP-4
              │        └─ 여기서부터 앱이 실물 허브(18105)에 붙을 수 있다(WORK-002 WP-3 · 4 · 6)
              └─ 응답 꼴이 코드로 선다 → 앱의 허브 클라이언트 · 걷기 단위 시험이 꼴을 맞춰 볼 수 있다
```

- 허브 WP 는 한 워크트리 안에서 **차례로** 간다(WP-2 가 WP-1 의 repository 를 · WP-3 이 WP-2 의 코어를 쓴다).
- **앱(WORK-002)과의 병행 — 제안**: 허브 WP-1 과 **동시에** 앱 WP-1(클라이언트 · CLI) · WP-2(A 열 원장 MCP) · WP-5(기록 틀)를 시작할 수 있다 — 이 셋은 허브 도구의 뜻에 기대지 않는다(계약은 SPEC-001 §4 로 이미 굳었다). 앱 WP-3(B 걷기) · WP-4(C 열) · WP-6(답 키)은 **허브 WP-3 이 끝난 뒤** 실물 허브로 한다. 근거와 「모의 허브」 의 한계는 WORK-002 §11 에 적었다 — 요약: 도구 8 의 결정론 규칙(층 펼침 · 계층 · 속성 맞춤)을 모의로 다시 지으면 허브를 두 번 짓는 셈이고 어긋난 모의가 걷기 결함을 가린다. 앱 단위 시험의 모의는 「쪽 넘김 · 오류 · 응답 꼴」 까지만 쓴다.

## 8. SPEC-001 절 ↔ WP 대응(안 걸린 구현 대상 = 0)

| SPEC-001 절 | 구현 대상 | WP |
|---|---|---|
| §1-2 하는 것 1 ~ 4 | ✓ | WP-1(1) · WP-2(2 · 4) · WP-3(3) |
| §1-3 범위 밖 | — (만들지 않는 것 — §2-1 「하지 말 것」 에 옮김) | — |
| §1-4 코드 자리 · 이름 | ✓ | WP-3(이름) · §1(자리 확인) |
| §2-1 파일 · X1 ~ X6 | ✓ | WP-1 |
| §2-2 env | ✓ | WP-1(`config.py`) · §2-3 |
| §2-3 적재 · 해시 1 ~ 6 | ✓ | WP-1 · WP-3(lifespan 시작 실패) |
| §3 계층 | ✓ | WP-1(repository) · WP-2(service) · WP-3(router · MCP) |
| §3-1 메모리 색인 | ✓ | WP-1 |
| §4-0 공통 | ✓ | WP-2(머리 · `total` · 「있음」 · 행 필드 · 원장 확인 · 쪽 넘김 · 오류) · WP-3(REST ↔ MCP 대응 · MCP 공통) |
| §4-1 `resolve` | ✓ | WP-2 |
| §4-2 `scope` | ✓ | WP-2 |
| §4-3 `neighbors` | ✓ | WP-2 · WP-3(도구 설명 문구) |
| §4-4 `facets`(대상 · 값 · 속성 쪽 · 상품 이름 · 계층 펼침) | ✓ | WP-2 |
| §4-5 `concern_candidates` | ✓ | WP-2 |
| §4-6 `pair` | ✓ | WP-2 |
| §4-7 `evidence` | ✓ | WP-2 |
| §4-8 `health` | ✓ | WP-2(코어) · WP-3(경로) |
| §5-1 R1 ~ R6 | ✓ | WP-2 |
| §5-2 범위별 표 · 속성 4표 · 입구 개념 수 | ✓ | WP-2(`ranges.py`) · WP-4(T13 셈) |
| §5-3 S1 ~ S4 | ✓ | WP-2 · WP-4(T8) |
| §5-4 V1 ~ V6 | ✓ | WP-2 · WP-4(T8) |
| §5-5 H1 ~ H5 | ✓ | WP-2 · WP-4(T9) |
| §5-6 L1 ~ L4 | ✓ | WP-2 · WP-4(T10) |
| §5-7 A1 ~ A6 | ✓ | WP-2 · WP-4(T12) |
| §6 근거 추적 | ✓ | WP-2(`evidence`) · WP-4(T5) |
| §7 가져갈 틀 / 버릴 것 | ✓(지침) | WP-1 ~ 4 의 「옛 틀」 표 |
| §8 stg | — **이번 판 구현 없음**(로컬 시험까지 · 머지 · 배포 · 데이터 반입은 별도 승인) | — |
| §9 T1 ~ T14 | ✓ | T1 · T2 = WP-1(+ WP-4 실물) · T3 = WP-1 · 2 · T6 · T9 ~ T14 = WP-2(합성) + WP-4(실물) · T7 = WP-3 · T4 · T5 · T8 = WP-4 |
| §10 열린 것 | 아래 §9 | — |
| 부록 A | ✓ | WP-1(`headers.py`) · T3 |

## 9. 열린 것 — SPEC-001 §10 이 「구현 때 정함」 으로 넘긴 것(번호 그대로 · 이번에 정할 제안값)

| # | 무엇 | 이번에 정할 제안값 | 어디서 |
|---|---|---|---|
| O-3 | gold 해시에 `questions.csv` | 로컬 = (a) 폴더 그대로 16 파일 · `health.files[]` 에 `hash_only` | WP-1 |
| O-4 | `resolve` 가 문장에서 낱말을 찾는 법 | (a) 공백 낱말 + 이웃 낱말 이어 붙임(이어 붙이는 길이 상한은 「문장의 낱말 수」 — 자르지 않는다) → R1 → R2. 놓친 입구 수는 앱 1회차 trace 로 | WP-2 |
| O-5 | 이름 | SPEC 제안 그대로 — 모듈 `app/modules/gold` · prefix `/procedure-hub/gold` · MCP 마운트 `/procedure-hub/gold-mcp` · 서버 `procedure-hub-gold` · env `GOLD_*` · 입력 `offer_name_contains` · `tables` · 필드 `attr` · `counts.subjects` · `counts.by_column` · `counts.entities`. 새로 정하는 이름: 진입점 **`app/gold_main.py`** · 설정 파일 **`envs/.env.gold`** · prefix 설정 `GOLD_API_PREFIX` · `GOLD_MCP_MOUNT_PATH` · REST 의 목록 쿼리 꼴(콤마) · `filters` 쿼리 꼴(`칸=값` 되풀이) | WP-1 · WP-3 |
| O-6 | 쪽 크기 · MCP 결과 크기 | 기본 100 · 최대 500 · MCP 결과 크기 meta 는 설정(`GOLD_MCP_RESULT_MAX_CHARS` — 값은 가장 큰 한 쪽이 잘리지 않는 값으로 WP-4 실물에서 재서 정하고 보고) · 쪽 밖 목록은 한도 없음 | WP-2 · WP-3 |
| O-7 | 진입점 | 로컬 = (a) 별도 ASGI `app.gold_main:app`. stg 쪽((b) `app.main` 마운트)은 **이번에 안 한다** | WP-3 |
| O-9 | `site` 로 0 행 | (a) 0 그대로 + `counts.unfiltered_rows` | WP-2 |
| O-12 | 제안 모음 ① ~ ⑦ | **승인됨** — SPEC 본문 그대로 구현 | WP-1 · WP-2 |
| O-16 | 속성 쪽 시작의 도구 꼴 | (a) `facets` 의 `node` | WP-2 |
| O-18 | 입구 목록의 도구 꼴 | (a) `resolve` 의 `text` 없는 꼴 | WP-2 |

**SPEC-001 에 빈 자리 · 되적을 것**(SPEC 은 이번에 안 고친다 — **SPEC 0.4.2 때 반영**)

| # | 자리 | 무엇 | 이번에 정할 제안값 | 상태 |
|---|---|---|---|---|
| N1-1 | SPEC-001 §4-6 입력 표 `package_kinds` · 규칙 3 | `pair` 에 **`b` 없이 `package_kinds`** 를 줬을 때의 뜻이 SPEC 에 없다(「두 끝이 함께 든 패키지」 만 적혀 있다). 선택지: (a) gold-build 시범과 같게 — `a` 쪽 집합과 항목이 겹치는 패키지를 낸다(`$SM/gold/gold-build.py:821` 의 `b` 없음 갈래) (b) `invalid_argument` | **(a)** — 시범 · gold 를 만든 식과 같은 뜻이고, 한 끝만 아는 질문에서 패키지가 폭에서 빠지지 않는다(원칙 「폭은 빠짐없이」). **구현자가 고르지 않는다 — 코디가 발주서에 이 값을 한 줄로 실어 준다.** T4 는 이 꼴에 기대지 않는다(§6 2 — 쌍 호출) | 제안 · **SPEC 0.4.2 때 §4-6 에 되적기** |
| H-2 | SPEC-001 §4-0 오류 | 오류 본문의 문구 접두 `<코드 이름>: <사유>`(§10 H-2) — 다른 서비스가 보는 표면이다 | 이 문서의 값으로 구현 · 앱 클라이언트는 문구가 아니라 **HTTP 상태**로 가른다(WORK-002 WP-1) | 구현 뒤 **SPEC 0.4.2 때 §4-0 에 되적기** |
| H-5 | SPEC-001 §4-0 REST · §4-4 `filters` | REST 쿼리 꼴 — 목록 = 콤마 · `filters` = `칸=값` 되풀이(§10 H-5) — 다른 서비스가 보는 표면이다 | 이 문서의 값으로 구현 · swagger 에 적음 | 구현 뒤 **SPEC 0.4.2 때 §4-0 에 되적기** |

이번 판에서 **정하지 않는 것**(상태가 「1회차 trace 뒤」 · 「뒤 단계에서 사용자 확인」): O-6 의 값 조정 · O-14 의 holder 확대 · O-15 효과 계층 · O-17 속성 쪽 한계 · O-3 · O-7 의 stg 쪽 · O-8 stg 데이터 반입 · O-11 접근 제어. 구현하지 않는다.

## 10. 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다 — 보고용)

| # | 자리 | 본 것 | 이 계획에서 한 것 |
|---|---|---|---|
| H-1 | SPEC-001 §4-0 오류 표 ↔ `release/v1.2.0` `app/core/exceptions.py:22-25` | SPEC 의 `invalid_argument` 는 422 인데 레포의 `DomainValidationError` 는 400 이다. 기존 클래스를 쓰면 계약과 어긋난다 | gold 모듈 안에 `DomainError` 하위 셋을 따로 둔다(WP-2 `errors.py`) — 공용 예외 파일은 안 고친다 |
| H-2 | SPEC-001 §4-0 오류 | 오류 **본문 꼴**이 SPEC 에 없다(코드 이름 · REST 상태까지만). 레포 핸들러는 `{"detail": <문구>}` 하나다 | 문구를 `<코드 이름>: <사유>` 로 시작하게 해 코드 이름이 REST · MCP 양쪽에서 같은 글로 나가게 한다(제안 — 본문에 `code` 칸을 따로 두려면 공용 핸들러를 고쳐야 한다) |
| H-3 | SPEC-001 §9 T4 | 허브 단위 시험이 문항의 「입구」 를 어디서 얻는지 적혀 있지 않다(호출 명세는 SPEC-002 §9-5 = 앱 쪽) | `questions.csv` 의 `entry_text` · `range` 로 `resolve` → 좁힘 없는 도구 길로 「표본 ⊂ 결과」 를 본다(§6). 정확한 명세 대조는 앱 WP-6 의 `sample_check` 가 한다 |
| H-4 | SPEC-001 §1-4 · §7 | 옛 틀 의존 표기 `mcp>=2.3,<3` — 설치되는 판의 import 경로(`mcp.server.mcpserver` 등)는 구현 때 소스로 확인해야 한다 | WP-3 에 확인 한 줄 |
| H-5 | SPEC-001 §4-4 `filters` · §4-0 REST | `filters`(칸=값 목록) · 목록 입력의 **REST 쿼리 꼴**이 SPEC 에 없다 | 콤마 목록 · `칸=값` 되풀이로 정하고 swagger 에 적는다(O-5 범위 — 이름 · 꼴) |

## 변경 기록

### 0.2.0 (2026-11-16) — 검수 `review-work-001-002.md` 반영(WARN 2 · NOTE 6)

계약(SPEC-001) · 결정(`_RESUME.md` §2)은 그대로다. 고친 것은 시험을 세우는 법 · 완료 조건 · 구현 메모뿐이다. 「고칠 방향」 은 리포트의 첫 선택지를 따랐다.

| 지적 | 고친 것 | 자리 |
|---|---|---|
| W1-1 | T4 단계 2 에 동시 가능 범위의 **쌍 호출** `pair(a, b, package_kinds)` 를 더함 · 단계 5 에 「시험 방법의 빠짐 ↔ SPEC 구멍」 을 갈라 적게 함 | §6 「T4 를 세우는 법」 2 · 5 |
| W1-2 | 「라우터 · MCP 입력은 전부 선택 · 검사는 코어」 메모 · 완료 조건 3 에 **문구 대조**(필수 빠짐 · enum 밖 · 한도 밖) | §5 「지킬 것」 1 · 만들 파일 `router/gold.py` 행 · 완료 조건 3 |
| N1-1 | `pair` 에 `b` 없이 `package_kinds` — SPEC 빈 자리. 제안 (a) 시범과 같게 · **SPEC 0.4.2 때 반영** | §9 「SPEC-001 에 빈 자리 · 되적을 것」 · §4 도구별 표 `pair` 행 |
| N1-2 | `create_gold_app(settings)` 팩토리 · 시험이 lifespan 을 직접 연다 | §5 「지킬 것」 2 · 3 · 만들 파일 `gold_main.py` 행 · 완료 조건 1 · 검증 |
| N1-3 | base 통과 · skip 수를 WP-1 맨 먼저 잰다 | §3 「맨 먼저」 · §6 완료 조건 5 |
| N1-4 | H-2 · H-5 를 「SPEC 0.4.2 때 되적기」 목록에 · 앱은 HTTP 상태로 가름(WORK-002 WP-1 에 같은 줄) | §9 같은 표 |
| N1-5 | `rg` 결과는 걸린 줄을 적고 입력 · 정렬 · 거름 코드가 아님을 밝힌다 | §4 완료 조건 5 |
| N1-6 | 고칠 것 없음(포트 18105 비어 있음 확인) | — |

### 0.1.0 (2026-11-16)

처음 씀 — WP 4 · SPEC-001 절 대응표 · 열린 것 9 · H-1 ~ H-5.
