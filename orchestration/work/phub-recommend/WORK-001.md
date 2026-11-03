---
type: work
id: WORK-001
title: "Hub 데이터 그래프 + 조회 tool — 로컬 E2E 1차 구현"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: new-feature
owner: "backend 워커"
roles:
  pm: "코디네이터"
  design: ""
  fe: ""
  be: "backend 워커"
  qa: "reviewer_code 워커 · 사용자(E2E)"
  ops: ""
progress: 0
created_at: 2026-10-26
updated_at: 2026-10-26
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  baselines: []
  decisions:
    - "orchestration/work/phub-recommend/DEC-001.md"
  specs:
    - "orchestration/work/phub-recommend/SPEC-001.md"
  works: []
  releases: []
  related:
    - "orchestration/work/phub-recommend/research-report.md"
---

# Hub 데이터 그래프 + 조회 tool — 로컬 E2E 1차 구현

SPEC-001 을 PROCEDURE-HUB 새 브랜치에 구현한다 — 브론즈 적재 CLI · 노드/엣지 빌드 · 검증 게이트 · 발행 · REST 7 + MCP 6 tool · 로컬 실행 문서 · E2E 확인 스크립트.
**비목표**: 상담 에이전트 · LLM · 프론트 화면 · 레거시/canonical 테이블과 코드 변경 · 배포(DEC-001 D-12 · D-13c · D-13g).

> 계약(필드 · 규칙 · 기대값)은 SPEC-001 이 갖는다. 이 문서는 순서 · 파일 · 검증 명령만 갖는다. 둘이 다르면 SPEC-001 이 맞다.

> **변경 이력**
> - 2026-10-26 재검수 반영 — R1 · WARN-n(`review-spec-001-v2-report.md`): 시술 항목 자기 안전 엣지 fixture · 테스트 기대(R1) · 엣지 9종 · Mount 예시 옵션
> - 2026-10-26 검수 반영 — F1~F7(`review-spec-001-report.md`): import 허용 목록을 SPEC §5.2 표와 일치(F7) · `has_procedure` 분리와 fixture 경우 추가(F1 · F3 · F4 · F5 · F6) · ruff 범위 CI 와 같게(W5) · 인덱스 이름 명시(W6) · 재적재 `--from-dir` 로 stg 1회(W8) · MCP 옵션 위치 확정(검수 §4)
> - 2026-10-26 초안

## Meta

- Baseline: 없음
- Covers spec: SPEC-001
- Depends on work: 없음
- Parallel work: 없음(상담 에이전트는 다른 레포 · 다른 work)
- Follow-up work: 상담 에이전트(DEC-001 D-08 · D-09 ②) · SPEC-001 §7 OQ 결정 후 보정
- External dependency: stg 공개 GET 21개(Phase 7 에서 1회만) · PyPI `mcp` 2.x

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | backend 워커 1명 |
| Status | todo |
| Progress | 0% |
| Branch/PR | PROCEDURE-HUB `release/v1.2.0` 에서 새 브랜치(DEC-001 D-09 ①). 이름은 코디네이터가 발주 때 정한다. PR · push 는 코디네이터 |
| Blocker | 없음 |
| Next | Phase 1 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | 코디네이터 | 범위 · 브랜치 · 발주 · PR | todo |
| BE | backend 워커 | Phase 1~7 | todo |
| QA | reviewer_code 워커 → 사용자 | 코드 리뷰(`.agents/skills/be-reviewer/SKILL.md` 기준) → 다음 날 사용자 로컬 E2E(SPEC-001 §6) | todo |

## Scope

포함:

- SPEC-001 §3 ~ §6 전부

제외:

- SPEC-001 §1 Out of scope 전부
- 기존 앱(`app.main:app`)에 graph 라우터 등록 — SPEC-001 §5.2 「왜 별도 앱인가」 · OQ-S07

## Code Surface

- Repo / module: `PROCEDURE-HUB/backend`
- 새 파일:

| 경로 | 설명 |
|---|---|
| `app/graph_main.py` | graph 앱 진입점 — `FastAPIBuilder`(`app/core/app_builder.py:21-33`)로 REST 라우터 + MCP 마운트 + lifespan(db_provider + `mcp.session_manager.run()`) |
| `app/modules/graph/__init__.py` | 모듈 |
| `app/modules/graph/domain.py` | 노드 · 엣지 타입(이름 · 설명 — `graph_schema` 가 그대로 낸다) · `normalize`(SPEC §3.3.1, `retrieval/domain.py:55-59` 복사) · 안정 id · 검색 점수표 |
| `app/modules/graph/sources.py` | 원천 10개별 노드/엣지 추출기(엔드포인트 하나 = 함수 하나). 순수 함수 — 입력 JSON + 브론즈 참조 → 노드 · 엣지 · 이슈 |
| `app/modules/graph/resolve.py` | 이름 해석 사전(SPEC §3.3.1) |
| `app/modules/graph/validation.py` | 검사(SPEC §3.4 코드표) |
| `app/modules/graph/application.py` | `GraphIngestApplication` · `GraphBuildApplication`(빌드 · 검증 · 발행) · `GraphQueryService`(조회 7종 — REST 와 MCP 가 같이 부른다) |
| `app/modules/graph/repository.py` | 저장소(`app/repository/base.py` `BaseRepository` 상속 — `publication/repository.py:36-38` 모양. `app.repository.base` 는 SPEC §5.2 허용 목록에 있다) |
| `app/modules/graph/container.py` | graph 전용 `DeclarativeContainer`(`app/core/container.py:57-68` 모양). wiring = `app.router.graph` · `app.modules.graph.mcp_server` |
| `app/modules/graph/mcp_server.py` | `MCPServer("procedure-hub-graph")` · tool 6개(SPEC §5.1 표) — 각 tool 은 `GraphQueryService` 를 부르기만 한다 |
| `app/modules/graph/config.py` | `PHUB_GRAPH_SOURCE_BASE_URL` 등 graph 전용 설정(`pydantic-settings`, `app/core/config.py:39-44` 와 같은 env 파일 규칙). `core/config.py` 는 고치지 않는다 |
| `app/router/graph.py` | REST 7개(`router/knowledge.py:22-39` 모양, prefix `/api/v1/graph`, 태그 「그래프」) |
| `app/schema/graph.py` | 응답 Pydantic(`app/schema/base.py` 의 `ItemBase` · `ResponseBase` — 허용 목록에 있다) |
| `app/swagger_docs/graph.py` | summary · description(`docs/guides/api.md:21-25`) |
| `app/model/graph.py` | ORM(아래 Domain / Schema) |
| `alembic/versions/b202610260001_graph_schema.py` | down_revision `b202609030001` |
| `scripts/graph_ingest.py` · `scripts/graph_build.py` | CLI(`scripts/manage_canonical_release.py:19-44` 모양: sys.path · argparse · `--database-url`). ingest 는 `--source http` · `--from-dir` · `--save-dir`(SPEC §3.1) |
| `scripts/graph_e2e_check.py` | SPEC §6 S-1~S-7 자동 확인(REST + MCP 클라이언트), PASS/FAIL 표 |
| `graph-local.compose.yml` | `phub-graph-postgres` · 볼륨 `phub-graph-pgdata` · `55434:5432` · `postgres:16` |
| `envs/graph.env.example` | `DATABASE_URL`(55434) · `PHUB_GRAPH_SOURCE_BASE_URL`(빈 값 + 주석) — 비밀값 없음 |
| `docs/graph-local.md` | 로컬 실행 안내(SPEC §5.4 순서 · 주소 · 시나리오 실행법 · 정리 명령) |
| `tests/fixtures/graph/*.json` | 손으로 줄인 원천 10개(아래 Phase 3) |
| `tests/test_graph_*.py` | 단위 · 저장소 · API · MCP · 경계 테스트 |
| `tests/integration/test_graph_stg_snapshot.py` | 실측 스냅샷 디렉토리(env `PHUB_GRAPH_SNAPSHOT_DIR`)로 SPEC §6 S-6 숫자 확인. CI 제외 경로(`backend/README.md:49-53`) |

- 손대는 기존 파일(추가만): `app/model/__init__.py`(import 한 줄) · `pyproject.toml`(`mcp>=2.3,<3` · `httpx` 를 runtime 의존성으로 — 지금은 dev 에만 있음 `pyproject.toml` `[tool.uv] dev-dependencies`) · `uv.lock`
- **손대지 않는 것**: `app/main.py` · `app/core/*` · `app/core/container.py` · `app/core/app_factory.py` · 다른 `app/modules/*` · `app/repository/*` · `app/service/*` · `app/router/*`(graph 외) · 기존 모델 · 기존 migration · 기존 테스트
- Domain / schema note: migration 필요(새 테이블만). 실제 스키마의 SoT 는 `app/model/graph.py` + migration

## Domain / Schema

| Entity | 역할 | 레이어 |
|---|---|---|
| `graph_bronze_snapshot` | 엔드포인트 · 수집 시각 · 내용 해시 · HTTP 상태 · 입력 모드 · 원천 위치 · 원본 JSON. (endpoint, content_hash) 유일 | 브론즈 |
| `graph_build` | 빌드 1회 — 시작/끝 시각 · 읽은 브론즈 해시 집합 · 결과(`published`/`rejected`/`unchanged`) | 빌드 |
| `graph_node` | (build, node_id) 유일. type · name · names · synonyms · attributes · source_refs(JSON) | 실버 |
| `graph_edge` | (build, edge_id) 유일. type · from · to · review_status · claims(JSON). (build, from) · (build, to) 조회 인덱스 | 시맨틱 |
| `graph_validation_issue` | build · code · severity · subject_kind · subject · detail(JSON) · bronze_ref(JSON) | 검증 |
| `graph_publication` | graph_version(정수, 유일) · build · published_at · bronze_hashes · check_summary · counts | 발행 |

- **인덱스 · 제약에 이름을 명시한다**(`Index("ix_graph_edge_build_from", …)` 처럼). `Base` naming convention 은 `ix_%(column_0_label)s` · `uq_%(table_name)s_%(column_0_name)s`(`app/model/base.py:8-14`)라 첫 컬럼만으로 이름이 정해진다 — (build, from) · (build, to) 처럼 같은 컬럼으로 시작하는 인덱스 둘이 `ix_graph_edge_build_id` 로 겹쳐 migration 이 실패한다(검수 W6)
- JSON 컬럼은 `JSON().with_variant(JSONB(), "postgresql")`(`app/model/canonical_publication.py:32`) — 테스트가 SQLite 메모리에서 `Base.metadata.create_all` 로 돌기 때문(`tests/test_publication_application.py:29-41`)
- 노드 · 엣지는 빌드 번호로 나눠 쌓는다(지난 발행본 보존 — SPEC §3.4). 레거시 · canonical 테이블로 가는 FK 없음
- migration 은 모델과 diff 0 이어야 한다 — CI 가 `alembic upgrade head` + `alembic check` 를 돈다(`.github/workflows/backend-test.yml:64-68`)
- SPEC 환류: 응답 필드는 SPEC §4 가 SoT. 구현 중 바꿔야 하면 코디네이터에게 묻는다

## Internal Interface Contract

- `GraphQueryService` 메서드 = SPEC §4 의 7개(검색 · 상세 · 이웃 · 부분 그래프 · 목록 · 스키마 · 검증). REST 라우터와 MCP tool 은 **이 메서드만** 부르고, 반환 dataclass → 같은 Pydantic 스키마로 직렬화한다. 그래서 같은 입력이면 REST JSON 과 MCP structured output 이 같다(SPEC §6 S-5 4번)
- 발행본 없음 · 노드 없음은 `app/core/exceptions.py` 의 `DomainError` 파생(503 · 404)으로 던지고, graph 앱에 `EXCEPTION_HANDLERS`(`exceptions.py:45-46`)를 등록한다. MCP 쪽은 같은 예외를 tool 오류로 바꾼다
- 503 용 `DomainError` 파생(예: `GraphNotPublished`, `http_status=503`)은 `app/modules/graph/` 안에 둔다(core 를 고치지 않는다)

## Execution

### Phase 1 — 모델 · migration · 뼈대 · 경계 테스트

- **Status**: TODO
- **설명**: 테이블과 빈 모듈 · 빈 graph 앱을 세우고, 경계(D-13c)와 기존 계약이 깨지지 않음을 먼저 테스트로 고정한다
- **작업**:
  - [ ] `app/model/graph.py` · `app/model/__init__.py` import · migration `b202610260001`
  - [ ] `pyproject.toml` 에 `mcp>=2.3,<3` · `httpx` 추가 → `uv lock`
  - [ ] `app/modules/graph/` 뼈대(domain 의 타입 표 · normalize · 안정 id 함수) · `container.py` · `config.py`
  - [ ] `app/graph_main.py` — health 정도만 응답하는 빈 앱(라우터는 Phase 5)
  - [ ] `tests/test_graph_boundary.py`: graph 코드(SPEC §5.2 「import 허용 목록」 머리의 파일 전부 — `app/modules/graph/**` · `app/router/graph.py` · `app/schema/graph.py` · `app/swagger_docs/graph.py` · `app/model/graph.py` · `app/graph_main.py` · `scripts/graph_*.py`)의 `app.*` import 를 AST 로 읽어 **SPEC §5.2 허용 목록 밖이 0** 인지. 허용 목록은 SPEC 표를 그대로 상수로 옮긴다(`app.core.config` · `app.core.tx*` · `app.core.exceptions` · `app.core.app_builder` · `app.core.logging` · `app.core.db` · `app.model.base` · `app.repository.base` · `app.schema.base` · graph 코드끼리). 새 테이블이 전부 `graph_` 접두인지(검수 F7)
  - [ ] `tests/test_graph_domain.py`: normalize 가 `retrieval.domain.normalize_term` 과 같은 결과(테스트에서만 비교 import 허용) · 안정 id 결정론
- **검증**:
  - [ ] `uv run ruff check .`
  - [ ] `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_boundary.py tests/test_graph_domain.py tests/test_public_api_contract.py`
  - [ ] 빈 PostgreSQL(55434)에서 `alembic upgrade head` → `alembic check` → `alembic downgrade b202609030001` → `upgrade head`
- **완료 증거**: 미작성

### Phase 2 — 브론즈 적재 CLI

- **Status**: TODO
- **설명**: SPEC §3.1 — 원본 그대로 · 해시 멱등 · 두 입력 모드
- **작업**:
  - [ ] `GraphIngestApplication` + `scripts/graph_ingest.py`(`--source http|--from-dir <경로>` · `--endpoints` 부분 실행 · `--database-url`)
  - [ ] 해시: 정규화 JSON SHA-256(SPEC §3.1)
  - [ ] 결과 표 stdout · 실패 있으면 종료 코드 1
- **검증**:
  - [ ] `tests/test_graph_ingest.py`(SQLite): fixture 디렉토리 적재 → 행 수 · 두 번째 실행 전부 `unchanged` · 키 순서만 바꾼 JSON 도 `unchanged` · 파일 없음/깨진 JSON → `failed` · 종료 코드. HTTP 모드는 `httpx.MockTransport` 로(네트워크 0)
  - [ ] `uv run ruff check .` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_ingest.py`
- **완료 증거**: 미작성

### Phase 3 — 실버 · 시맨틱 빌드

- **Status**: TODO
- **설명**: SPEC §3.2 노드 10종 · §3.3 엣지 9종 · §3.3.1 이름 해석. 원천별 추출기는 순수 함수로 두고 단위 테스트한다
- **작업**:
  - [ ] fixture 10개(`tests/fixtures/graph/<endpoint>.json`)를 **손으로 줄여** 만든다 — 실제 응답과 같은 키 구조(SPEC §3.2 · §3.3 의 위치)를 지키고, 아래 경우가 반드시 들어가게:
    - M1 · M2 · M8 · M13 시술군 / 「쳐짐」 대분류 + 「처짐/탄력」 최적화 고민 / `modality_ref` 빈 고민 항목 1개
    - contraindications M1–M2(`note` 에 「보톡스 먼저 → 필러」) + treatment-sequence `sequence_order` 에 M2 가 M1 보다 앞 → `conflict`
    - synergy 이름이 시술 항목과 안 맞는 끝점 1개(시술군으로 붙고 `unresolved_name_ref`) · optimization 못 푸는 이름 1개 · 원소 1개짜리 `incompatible_same_day.pair` 1개
    - 같은 정규화 이름 제품이 두 원장에 1쌍(→ `synonym`)
    - synergy 끝점이 **제품**으로 풀리는 경우 1개(→ `*_category` 시술군) · 양 끝이 같은 시술군이 되는 링크 1개(→ `self_relation_skipped`) · 시술 항목 끝점이 낀 쌍 1개(→ `sequence_order` 주장이 붙지 않음)
    - `products` 분류 하나는 `category_id` 가 배열(`["M8", "M9"]` 등 — stg `energy_device` 와 같은 모양)
    - problem-packages CC 가 같은 P 안 두 고민 항목과 이름이 같고 `cc_group` 으로만 갈리는 경우 1개 · 어떤 규칙으로도 안 갈리는 경우 1개(→ `ambiguous_cc_match`)
    - 같은 (from, to) 로 두 tier 가 같은 시술군을 가리키는 problem-combos 행(→ 엣지 1 · 주장 2)
    - **시술 항목이 끝점인 안전 엣지** 1개 — treatment-sequence `incompatible_same_day` 에서 한쪽이 시술 항목(stg 의 「CO2 프락셔널」 ↔ 「필러」 모양)으로 풀리는 쌍(R1)
  - [ ] `sources.py` 추출기 10개 · `resolve.py` · 빌드 조립(노드 → 사전 → 엣지). 엣지 타입 9종(`has_child` 와 `has_procedure` 는 다른 타입) · `edge_id` 원천 키는 SPEC §3.3 표 「원천 키」 열
  - [ ] `procedure_group.session_phase_order` · `procedure_relation` 쌍 키(사전순) · `first` 판정 · `conflict` 판정(SPEC §3.3 「시술↔시술 주장」)
- **검증**:
  - [ ] `tests/test_graph_sources.py`: 원천별 노드/엣지/주장/이슈 기대값(fixture 기준 숫자를 테스트에 박는다) · M1–M2 엣지 claims 원천 · `review_status=conflict` · 「처짐」 synonym 0 · 제품 끝점 → 시술군 · 자기쌍 제외 · 시술 항목 쌍에 `sequence_order` 없음 · 배열 `category_id` → `has_product` 원소마다 · CC 동률 규칙 · 같은 입력 두 번 → 같은 id 집합
  - [ ] 모델 호출 0 — 빌드 경로에 네트워크 · LLM 클라이언트 import 없음(boundary 테스트에 `anthropic` · `openai` 등 금지 추가)
  - [ ] `uv run ruff check .` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_sources.py tests/test_graph_boundary.py`
- **완료 증거**: 미작성

### Phase 4 — 검증 게이트 · 발행

- **Status**: TODO
- **설명**: SPEC §3.4 — 이슈 코드 · error 만 차단 · 발행본 · 같은 브론즈면 `unchanged`
- **작업**:
  - [ ] `validation.py`(코드표 전부 · `coverage_gap` 하위 종류 · `unresolved_by_source` 집계)
  - [ ] `GraphBuildApplication` + `scripts/graph_build.py`(`--force` · `--database-url`). 빌드 한 번 = 트랜잭션 하나(`app/core/tx/transaction.py:41-47`), rejected 이슈는 별도 트랜잭션
  - [ ] stdout: 발행 결과 · 버전 · `check_summary` 표
- **검증**:
  - [ ] `tests/test_graph_build.py`(SQLite): fixture → `published` v1 · 재실행 `unchanged` · `--force` → v2 · 필수 엔드포인트 하나 지운 브론즈 → `rejected` · 이전 발행본 유지 · 이슈 코드별 수가 fixture 기대값
  - [ ] `uv run ruff check .` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_build.py`
- **완료 증거**: 미작성

### Phase 5 — 조회 서비스 · REST · graph 앱

- **Status**: TODO
- **설명**: SPEC §4 — 7개 엔드포인트 · 최신 발행본만 · `safety` 동반 · 에러 형태
- **작업**:
  - [ ] `GraphQueryService` 7 메서드 · 검색 점수표 · 정렬 · 부분 그래프 너비 우선 · 상한 · `truncated`
  - [ ] `Safety` 조립(시술 항목은 시술군 상속 · `gaps`)
  - [ ] `app/router/graph.py` · `app/schema/graph.py` · `app/swagger_docs/graph.py` · `graph_main.py` 에 등록 · 예외 핸들러
- **검증**:
  - [ ] `tests/test_graph_api.py`(SQLite + `httpx.ASGITransport`, `tests/test_public_api_contract.py:15-17` 방식): fixture 빌드 후 SPEC §6 S-1 ~ S-5 를 fixture 판으로 — 검색 점수 · 「처짐」 0 동의어 · M1–M2 conflict · 모든 응답 `graph_version` · 시술 노드 `safety`(시술군당 한 묶음 · **시술 항목 자기 안전 엣지가 있으면 그 항목 키도 맵에 있고, 두 키를 합친 내용 == 그 항목 상세의 `safety`**(R1) · 포함 조건에 시너지만 있는 엣지 없음) · 부분 그래프 방향(`out` 기본 · 무방향 엣지 양쪽 · `max_nodes` 에서 `truncated`) · 검증 `limit=0` · `build=latest` · 발행본 없음 503 · 없는 노드 404 · 잘못된 타입 422
  - [ ] 기존 계약 불변: `tests/test_public_api_contract.py` 통과(기존 앱 operation 42개 그대로)
  - [ ] `uv run ruff check .` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_api.py tests/test_public_api_contract.py`
- **완료 증거**: 미작성

### Phase 6 — MCP

- **Status**: TODO
- **설명**: SPEC §5.1 — Streamable HTTP · stateless · JSON 응답 · graph 앱에 마운트 · tool 6개가 같은 서비스를 부른다
- **작업**:
  - [ ] `mcp_server.py` — tool 이름 · 입력 스키마 · 설명 문구는 SPEC §5.1 표 그대로. `stateless_http=True` · `json_response=True` 는 `MCPServer(...)` 가 아니라 `mcp.streamable_http_app(stateless_http=True, json_response=True)` 키워드로 준다(SPEC §5.1 · https://py.sdk.modelcontextprotocol.io/run/asgi/)
  - [ ] `graph_main.py`: `Mount("/procedure-hub/graph-mcp", app=mcp.streamable_http_app(stateless_http=True, json_response=True))` — `streamable_http_app()` 은 한 번만 부른다 · lifespan 에 `mcp.session_manager.run()`(https://py.sdk.modelcontextprotocol.io/run/asgi/ 경고)
- **검증**:
  - [ ] `tests/test_graph_mcp.py`: SDK 의 클라이언트(또는 in-memory 연결 — https://py.sdk.modelcontextprotocol.io/get-started/testing/)로 `list_tools` = 6개 이름 · 각 입력 스키마 필수 필드 · `graph_get_node` 결과 == 같은 id 의 REST JSON · 발행본 없음 → tool 오류
  - [ ] `uv run ruff check .` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_mcp.py`
- **완료 증거**: 미작성

### Phase 7 — 로컬 실행 문서 · E2E 스크립트 · 실측 1회

- **Status**: TODO
- **설명**: 사용자가 다음 날 그대로 따라 할 수 있게(SPEC §5.4 · §6). 워커가 지정 포트(55434 · 18005)로 **한 번 끝까지** 돌려 보고, 실측 숫자를 완료 증거로 남긴 뒤 정리한다
- **작업**:
  - [ ] `graph-local.compose.yml` · `envs/graph.env.example` · `docs/graph-local.md`(SPEC §5.4 순서 · Swagger/MCP 주소 · `claude mcp add` 예 · 시나리오 실행 `scripts/graph_e2e_check.py` · 정리 `docker compose -f graph-local.compose.yml down -v`)
  - [ ] `scripts/graph_e2e_check.py --base-url http://127.0.0.1:18005` — SPEC §6 S-1 ~ S-6 기대값을 확인하고 PASS/FAIL · 실제값 표를 낸다. S-1 · S-3 · S-4 · S-5 는 MCP 로도. **S-7 은 CLI 재실행이라 스크립트가 부르지 않는다** — `docs/graph-local.md` 에 손으로 하는 순서(SPEC §6 S-7)를 적는다(검수 W8)
  - [ ] `tests/integration/test_graph_stg_snapshot.py` — `PHUB_GRAPH_SNAPSHOT_DIR` 가 있을 때만 실행
  - [ ] 실측: 빈 DB → migration → `graph_ingest --save-dir <레포 밖 임시 폴더>`(**stg GET 21개를 각 1회 — 이것이 유일한 stg 호출**) → `graph_build` → 앱 기동 → `graph_e2e_check.py` → S-7: `graph_ingest --from-dir <그 폴더>`(21개 `unchanged`) · `graph_build`(`unchanged`). 원본은 레포에 넣지 않는다
  - [ ] 정리: 앱 종료 · `docker compose … down -v`(사용자가 빈 DB 부터 시작하도록). 지정 포트 외 사용자 포트 · 프로세스는 건드리지 않는다
- **검증**:
  - [ ] `graph_e2e_check.py` 전부 PASS. SPEC §6 S-6 숫자와 다르면 FAIL 로 두고 차이(실제값 · 원인 추정 · stg 변경 여부)를 완료 증거에 적는다 — 숫자를 맞추려고 규칙을 바꾸지 않는다
  - [ ] **전체 검증 한 번**: `uv run ruff check .` · `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration`(`backend/README.md:44-47`) · 빈 Postgres `alembic upgrade head && alembic check`
- **완료 증거**: 미작성

## Pre-deploy Check

배포 없음(로컬 전용). 브랜치를 PR 로 올리기 전에만:

- [ ] 기존 앱 공개 operation 42개 불변(`tests/test_public_api_contract.py`)
- [ ] `envs/graph.env.example` 에 비밀값 없음 · `.env.graph` 는 git 에 없음(`.gitignore` `.env*`)
- [ ] stg 원본 스냅샷이 레포에 없음

## Rollback

- 브랜치를 버리면 끝(운영 반영 없음)
- DB: `alembic downgrade b202609030001` 로 graph 테이블만 제거(기존 166 테이블 무관) · 로컬 컨테이너는 `docker compose -f graph-local.compose.yml down -v`

## Done Criteria

- [ ] Phase 1 ~ 7 이 `DONE`
- [ ] SPEC-001 §6.2 Acceptance Criteria 전부 · `graph_e2e_check.py` 실측 PASS(또는 차이가 완료 증거에 설명됨)
- [ ] 전체 검증 통과(기존 테스트 포함) — 깨진 것이 이 work 와 무관하면 「무관」으로 분리해 보고
- [ ] reviewer_code 리뷰 반영

## Open Issues

- ~~`stateless_http` · `json_response` 를 켜는 API 위치~~ — 닫힘(검수 §4): `streamable_http_app()` 키워드. 설치된 버전에서 다르면 완료 증거에 적는다
- MCP in-memory 테스트 예시(https://py.sdk.modelcontextprotocol.io/get-started/testing/)는 `pytest.mark.anyio` 를 쓰고 레포는 `asyncio_mode = "auto"`(`pyproject.toml`)다 — 섞어 쓸 때 이벤트 루프 플러그인이 겹치지 않게 한다(검수 §4)
- `uv run --env-file` 이 설치된 uv 버전에서 동작하는지 Phase 7 에서 확인. 안 되면 `docs/graph-local.md` 에 대체 명령(`set -a; . envs/.env.graph; set +a`)
- 계약 차원의 열린 것은 SPEC-001 §7 · DEC-001 OQ 가 갖는다 — 구현 중 판단이 필요하면 임의로 정하지 말고 코디네이터에게 묻는다

## Related

- SPEC: SPEC-001
- Decision: DEC-001
- 조사: research-report.md
