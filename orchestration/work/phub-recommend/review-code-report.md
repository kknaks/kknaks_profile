---
type: review
id: REVIEW-CODE-001
title: "reviewer_code — Hub 데이터 그래프 + REST · MCP 구현 검수 (WORK-001 Phase 1~7)"
reviewer: reviewer_code 워커
created_at: 2026-10-26
target_worktree: /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend
base: origin/release/v1.2.0
contract: SPEC-001 v0.2.1 · WORK-001 · DEC-001 (D-05 · D-06 · D-12 · D-13c)
---

# 종합 판정: **PASS (조건부) — FAIL 0 · WARN 9**

- SPEC §3 노드 · 엣지 규칙, §3.3 세 규칙(제품 끝점 → `*_category` · 자기쌍 제외 · `sequence_order` 는 시술군끼리만), CC 동률, subgraph 방향 · 상한, safety 포함 규칙 R1, 응답 shape, 검증 코드, 발행 규칙이 코드에서 SPEC 그대로다.
- DEC 경계: 모델 · LLM 호출 0, 레거시 · canonical import 0, 큐레이션 3종 비병합, 이름 매칭은 정규화 완전 일치뿐이다. 검색 prefix · contains 와 「○○ 먼저」 패턴은 SPEC 이 허용한 곳에만 있다.
- 기존 앱 회귀: 수정한 기존 파일은 허용된 3개뿐이다. `app/main.py` 와 기존 테스트는 손대지 않았고, migration 은 `b202609030001` 위에 단일 head 로 올라간다.
- **FAIL 목록: 없음.**
- **머지 전 코디가 정할 것: WARN-1** — 이 브랜치가 stg 로 가면 컨테이너 기동 때 `alembic upgrade head` 가 graph 테이블 6개를 stg DB 에 만든다. 운영 이미지에도 `mcp` 의존성이 들어간다.
- 실행 검증은 하지 않았다(read-only 브리프 §7). 워커 실측(pytest 422 · E2E 76/76 · alembic diff 0)은 이 리뷰가 다시 확인하지 않았다.

## 0. 범위 산정

- `git log origin/release/v1.2.0..HEAD`: 커밋 0. 변경은 전부 미커밋이다.
- 수정(M) 3: `backend/app/model/__init__.py`(+8, import 1문) · `backend/pyproject.toml`(+2: `httpx>=0.28.1` · `mcp>=2.3,<3`) · `backend/uv.lock`(+473/-3)
  - lock 에서 제거 · 다운그레이드된 것: `idna` 3.11 → 3.20 하나뿐(전이). 나머지는 신규 추가(mcp 2.3.0 · mcp-types · httpx2 · httpcore2 · jsonschema · pyjwt · cryptography · sse-starlette · truststore 등)
- 신규(??): graph 코드 약 3,700줄(`app/modules/graph/*` 10 파일 · router · schema · swagger_docs · model · graph_main · migration · scripts 3), 테스트 약 1,250줄(+ fixture 10), 문서 · compose · env 예시
- `__pycache__` 는 untracked 이지만 `.gitignore:56` 으로 제외된다. `backend/envs/.env.graph` 가 워크트리에 있다(gitignore `.env*` — 커밋되지 않음)

## 1. SPEC 대조

| 항목 | 판정 | 근거(코드) | SPEC |
|---|---|---|---|
| 노드 10종 · 공통 필드 · 원천 키 | PASS | `sources.py:190-441` · `domain.py:68-129` | §3.2 |
| products ② 키 = 분류 키 · `category_id` 배열 펼침 | PASS | `sources.py:323-344` | §3.2 · F4 |
| 엣지 9종 · `edge_id` 원천 키(treats · has_product = 엔드포인트, 그 외 "") | PASS | `sources.py:482-545 · 503-519` · `domain.py:308-310` | §3.3 공통 · F3 |
| 무방향(`procedure_relation` · `synonym`) 사전순 | PASS | `sources.py:153-154` | §3.3 |
| synergy 끝점: 제품 · 못 풂 → `*_category`, 못 푼 것만 unresolved | PASS | `sources.py:725-740` | §3.3 시술↔시술 |
| 자기쌍 제외 → `self_relation_skipped` | PASS | `sources.py:705-716` | §3.3 · F1 |
| `sequence_order` 는 이미 생긴 쌍 · 양 끝 시술군 · order 다를 때만 | PASS | `sources.py:848-874` | §3.3 · F1 |
| contraindications `<from/to_name> 먼저` → first | PASS | `sources.py:765-770` | §3.3 |
| treatment-sequence 양 끝 다 풀린 것만 · 제품은 group 하나일 때 · 원소 1개 pair 1회 | PASS | `sources.py:785-845` | §3.3 · §3.4 |
| conflict = first 값 둘 이상 | PASS | `sources.py:949-956` | §3.3 |
| CC → 고민 항목 동률(cc_group = label) · ambiguous/unresolved 시 엣지 없음 | PASS | `sources.py:567-599` | §3.3 · F5 |
| synonym: 트리 concern→sub→item 순 · id 사전순 첫 일치 / 제품 ②↔① group 겹침 | PASS | `sources.py:907-946` | §3.3 · §3.2 |
| 이름 해석: 항목 → 시술군 → 제품, 시술군 우선 → ① 우선 → id 순 | PASS | `resolve.py:46-66` | §3.3.1 |
| 검증 코드 11종 · coverage_gap 7종 · unresolved_by_source 5키 · 등급 | PASS | `domain.py:265-296` · `validation.py:55-187` | §3.4 |
| error 만 발행 차단 · 같은 bronze_hashes → unchanged · `--force` 새 번호 | PASS | `application.py:200-219` | §3.4 |
| rejected 는 build + 이슈만 별도 트랜잭션, 이전 발행본 유지 | PASS | `application.py:267-293` | §3.4 · §5.3 |
| 조회 7종 응답 shape · `graph_version` "vN" · `published_at` | PASS | `application.py:739-992` · `schema/graph.py` | §4 |
| 검색 점수표 · names.en = synonym 열 · 정렬 | PASS | `application.py:750-776` · `domain.py:325-352` | §4-1 |
| 부분 그래프 방향(기본 out · 무방향 양쪽) · BFS 순서 · max_nodes · 엣지 양끝 포함 | PASS | `application.py:848-894` | §4-4 · F6 |
| Safety 포함 조건(contraindication · minimum_interval · incompatible_same_day) · gaps | PASS | `application.py:653-699` · `domain.py:253-259` | §4 Safety |
| R1: 시술 항목 자기 안전 엣지 → 맵 키 추가, 합치면 상세와 같음 | PASS | `application.py:710-736` · 테스트 `test_graph_api.py:169-184` | §4 응답 크기 · R1 |
| 에러: 503 문구 · 404 문구 · 422 | PASS | `domain.py:399-417` · `core/exceptions.py:40-42` | §4 Case Matrix |
| MCP: Streamable HTTP · `streamable_http_app(stateless_http=True, json_response=True)` 1회 · lifespan `session_manager.run()` · 마운트 경로 | PASS | `graph_main.py:26-39 · 61` | §5.1 |
| MCP tool 6 · 이름 · 입력 · 설명 문구 SPEC 그대로 · DomainError → ToolError | PASS | `mcp_server.py:39-145` | §5.1 |
| 로컬 실행 포트 55434 · 18005 · 컨테이너 · 볼륨 이름 | PASS | `graph-local.compose.yml` · `docs/graph-local.md:7-34` | §5.4 |

### 1-1. 워커가 SPEC 밖에서 고른 것 — 판정

| # | 선택 | 판정 | 근거 |
|---|---|---|---|
| ① | `procedure.attributes.group_id` = 노드 id(`procedure_group:M1`) | **PASS** | SPEC §4 「procedure 노드 자신은 `Node.attributes.group_id` 로 그 묶음을 가리킨다」. 그 묶음의 키가 노드 id 이므로 노드 id 여야 맞다(`sources.py:279`). 다만 같은 그래프에서 product `group_ids` 는 SPEC §3.2 대로 M 코드(`["M1"]`, `sources.py:311 · 343`)라 형식이 섞인다 → WARN-8 |
| ② | minimum_intervals 원천 `source` 문자열 → `cited_source` | **PASS** | Claim 공통 필드 `source`(엔드포인트)와 이름이 겹쳐 그대로 둘 수 없다(`sources.py:816`). SPEC §3.3 표 「`source` 문자열」을 `cited_source` 로 고쳐 적어야 한다(SPEC 환류) |
| ③ | procedure_relation 주장에 `kind` 추가 | **PASS** | 같은 엔드포인트 `treatment-sequence` 에서 minimum_intervals · incompatible_same_day · sequence_order 세 종류가 나오는데, Safety 포함 조건(§4)이 이 셋을 다르게 다룬다. 원천만으로는 구분할 수 없어 필요하다. Claim 「...타입별 값」에 더하는 것이라 shape 를 깨지 않는다. `schema.claim_fields` 에도 실렸다(`domain.py:186`). SPEC 환류 권장 |
| ④ | search `limit ≤ 100` · neighbors `limit ≤ 1000` | **WARN(SPEC 빈칸)** | SPEC §4-1 · §4-3 표에 상한이 없다. Validation 은 「위 표의 범위」라고만 적었다. REST · MCP · 서비스가 같은 상한을 쓴다(`application.py:537-538` · `router/graph.py:82 · 112` · `mcp_server.py:98 · 111`). 값 자체는 합리적이다. SPEC 표에 적어 두면 닫힌다 |
| ⑤ | validation `build=latest` | **PASS** | SPEC §4-7 그대로다(`application.py:964-992`): published · rejected 중 최신 빌드를 고르고 `unchanged` 기록은 뺀다. rejected 면 서빙 중 발행본의 version · published_at 을 싣고, 발행본이 없으면 503 이 아니라 그 빌드의 이슈를 준다. 테스트 `test_graph_api.py:290-306`. 발행본이 없을 때 `graph_version` · `published_at` 이 `null` 인 것은 SPEC 「모든 응답 최상위에 graph_version(문자열)」의 W3 예외로 읽었다 — SPEC 에 한 줄 적어 두면 좋다 |

## 2. DEC 경계

| 항목 | 판정 | 근거 |
|---|---|---|
| D-12 모델 · LLM 호출 0 | PASS | graph 코드 전체에서 `anthropic` · `openai` · `difflib` · `fuzz` · `levenshtein` 0건(grep). 경계 테스트 `test_graph_boundary.py:54-56 · 99-106`. 네트워크는 ingest 의 stg GET(`application.py:92-128`)뿐이다 |
| D-13c 레거시 · canonical import 0 | PASS | graph 코드의 `app.*` import 전수: `app.core.{app_builder,config,exceptions,logging,tx,tx.provider}` · `app.model.base` · `app.repository.base` · `app.schema.base` · graph 끼리. 이것이 전부이고 SPEC §5.2 허용 목록 안이다. retrieval import 는 테스트 `test_graph_domain.py:17` 하나뿐(SPEC 예외 허용) |
| 새 테이블 `graph_` 접두 · 외부 FK 0 | PASS | `model/graph.py` 6 테이블 · FK 는 전부 `graph_build.id`. 테스트 `test_graph_boundary.py:109-126` |
| D-13e 큐레이션 비병합 | PASS | treats 원천 키 = 엔드포인트라 원천마다 다른 엣지가 된다(`sources.py:487 · 544 · 625 · 701`) |
| D-13d 정규화 완전 일치만 | PASS | `resolve.py:48-66` · `sources.py:567 · 919 · 939` 모두 `normalize(a) == normalize(b)`. 부분 일치는 검색 점수(SPEC §4-1 허용)에만 있다 |
| D-05 REST · MCP 같은 서비스 | PASS | router · MCP 가 모두 `GraphQueryService` 메서드 하나를 부르고 같은 `graph_payload` 로 직렬화한다(`schema/graph.py:222-224`). 테스트 `test_graph_mcp.py:58` |
| D-06 safety 동반 · 버전 | PASS | 상세 · 이웃 · 부분 그래프가 safety 를 싣고, 모든 응답에 `graph_version` · `published_at` 이 있다(`test_graph_api.py:309-313`) |

## 3. 기존 앱 회귀

| 항목 | 판정 | 근거 |
|---|---|---|
| 기존 파일 수정이 허용 3개 안 | PASS | `git status`: M 은 `app/model/__init__.py` · `pyproject.toml` · `uv.lock` 뿐(SPEC §5.2 · WORK Code Surface) |
| `__init__.py` 는 추가만 | PASS | 기존 줄 변경 없이 import 블록 1개만 늘었다 |
| 기존 앱 · 공개 계약 42 불변 | PASS | `app/main.py` · `app/core/*` · `tests/test_public_api_contract.py` 무수정. 기존 앱에 `/graph` 경로가 없음을 테스트로 막는다(`test_graph_boundary.py:129-133`) |
| migration 단일 head | PASS | `alembic/versions` = `b202609030001` → `b202610260001`(down_revision 일치, `b202610260001_graph_schema.py:18-19`). downgrade 가 인덱스 · 테이블 6개를 역순으로 지운다 |
| 인덱스 이름 명시(W6) | PASS | `model/graph.py:41 · 58 · 74 · 95-96 · 118` |
| `tests/conftest.py` 신규 | **WARN-2** | 아래 |

## 4. 레포 규칙 (be-reviewer)

| 항목 | 판정 | 근거 |
|---|---|---|
| 계층 Router → Service → Repository | PASS | router 는 서비스 호출과 직렬화만 한다(`router/graph.py`). 저장소는 `graph_*` 만 다룬다(`repository.py`) |
| DI | PASS | graph 전용 `DeclarativeContainer` 를 쓰고 Factory 로 요청마다 새로 만든다. wiring 은 `app.router.graph` 다(`container.py`). MCP 는 provider 를 factory 로 받는다(`graph_main.py:26`) |
| 트랜잭션 | PASS | ingest 1 tx(`application.py:154`). 발행은 build · 노드 · 엣지 · 이슈 · 발행본을 1 tx 로 묶어 실패하면 하나도 남지 않는다(`:295-335`). rejected 는 별도 tx(`:267`). 조회는 `@transactional` 읽기다. CLI 의 `db_provider._engine` 교체는 기존 `manage_canonical_release.py:227-229 · 283` 선례를 따랐다 |
| 예외 | PASS | `DomainError` 파생(503 · 404 · 422)을 쓰고 graph 앱에 `EXCEPTION_HANDLERS` 를 등록했다(`graph_main.py:57`). core 는 고치지 않았다 |
| 배포 영향 | **WARN-1** | 아래 |

## 5. 테스트

| 항목 | 판정 | 근거 |
|---|---|---|
| stg 를 부르지 않음 | PASS | HTTP 모드는 `httpx.MockTransport` 로 시험한다(`test_graph_ingest.py:74-81`). API · MCP 는 `ASGITransport` 를 쓴다. stg 스냅샷 테스트는 `PHUB_GRAPH_SNAPSHOT_DIR` 가 있을 때만 돌고(`integration/test_graph_stg_snapshot.py:23`), 네트워크 없이 파일만 읽는다 |
| SPEC E2E 기대값 고정 | PASS | fixture 판은 S-1~S-5 를 `test_graph_api.py` 에서, 원천별 숫자 · conflict · 자기쌍 · CC 동률 · 배열 `category_id` · R1 을 `test_graph_sources.py` 에서 본다. stg 실측 숫자(S-6 전 항목 · 노드 941 · 엣지 타입별 · 주장 448/167)는 `test_graph_stg_snapshot.py:33-69` 가 고정한다 |
| 멱등 · 결정론 | PASS | `test_graph_build.py:31`(v1 → unchanged → force v2) · `test_graph_ingest.py`(키 순서만 다른 JSON 은 unchanged) |
| 발행본 없음 · 404 · 422 · MCP tool 오류 | PASS | `test_graph_api.py:47-81` · `test_graph_mcp.py:51 · 80` |
| 실행 결과 | 미확인 | 브리프 §7 에 따라 실행하지 않았다. 워커 보고는 pytest 422 passed |

## 6. WARN 목록 (FAIL 아님 — 수정 또는 기록)

| # | 위치 | 내용 | 근거 | 권장 |
|---|---|---|---|---|
| WARN-1 | `backend/Dockerfile:10 · 26` · `alembic/versions/b202610260001_graph_schema.py` · `pyproject.toml` | 이 브랜치가 `release/v1.2.0` 에 들어가고 stg 로 fast-forward 되면(`docs/guides/deployment.md:39`) 컨테이너 기동 `alembic upgrade head` 가 **graph 테이블 6개를 stg DB 에 만든다.** 운영 이미지에도 `mcp` · `httpx` 와 그 전이 의존성이 들어간다(`uv sync --frozen --no-dev`). 새 테이블만 생기니 파괴적이지는 않다. 하지만 SPEC §1 은 「배포 — 범위 밖(로컬 전용)」이다. `deployment.md:211` 의 head(`b202609030001`) 서술도 낡는다 | SPEC §1 Out of scope · be-reviewer 「배포 영향」 | 코디가 PR 머지 시점과 stg 반영 여부를 정한다. 머지 전에 결정을 PR 본문에 적는다 |
| WARN-2 | `backend/tests/conftest.py:1-3` | WORK Code Surface 목록에 없는 새 파일이다. `tests/` 루트 conftest 라서 **모든** pytest 세션(integration 포함)이 수집할 때 graph 모듈을 import 한다. fixture `graph_db` 는 autouse 가 아니고 이름도 겹치지 않아 기존 테스트 동작에는 영향이 없다. graph 모듈이 import 에서 깨지면 전체 테스트 수집이 깨진다 | WORK Code Surface · 「손대지 않는 것: 기존 테스트」 | 그대로 받아도 된다. 피하려면 graph 테스트 파일마다 `pytest_plugins` 나 직접 import 로 바꾼다. 코디가 허용 여부를 정한다 |
| WARN-3 | `domain.py:173-202` vs `sources.py:543 · 747` | `graph_schema.claim_fields` 가 실제로 내는 키를 다 적지 않았다 — `procedure_relation` 에 `timing`(synergy 주장), `treats` 에 `package_name`(problem-combos 주장)이 빠졌다. 외부 LLM 은 스키마만 읽고 tool 을 쓴다 | SPEC §4-6 「외부 LLM 이 이것만 읽고」 | 두 키를 `claim_fields` 에 더한다 |
| WARN-4 | (SPEC 빈칸) `application.py:537-538` | 선택 ④ 상한 100 · 1000 이 SPEC 에 없다 | SPEC §4 Validation | SPEC §4-1 · §4-3 표에 상한을 적는다(코드는 그대로) |
| WARN-5 | `scripts/graph_e2e_check.py:52` | `raise_for_status()` 때문에 앱이 503(빌드 전) · 404 를 주면 PASS/FAIL 표 대신 **traceback 으로 끝난다** | WORK Phase 7 「PASS/FAIL · 실제값 표」 | HTTP 오류를 FAIL 줄로 남기게 한다 |
| WARN-6 | `docs/graph-local.md:21` | 「처음 한 번」의 `cp envs/graph.env.example envs/.env.graph` 가 워크트리에 이미 있는 `.env.graph`(워커가 값을 넣은 것)를 **빈 URL 로 덮어쓴다.** stg 주소는 레포 문서에 없고 조사 리포트 머리(`research-report.md:4`)에만 있다 | 사용자 E2E | 문서에 「이미 있으면 건너뛴다」를 적거나 `cp -n` 을 쓴다. 코디가 사용자에게 stg 주소 출처를 알린다 |
| WARN-7 | `docs/graph-local.md:92-99` | 「알아 둘 것」에 SPEC §6.3 알려진 이상 일부가 빠졌다: M1↔M2 `conflict` 가 조건이 다른 주장끼리 잡힌 것(OQ-S05/S06), M2↔M7 「실 먼저」가 first 로 읽히지 않는 것, 이소트레티노인 노드에 간격 엣지가 없는 것. 사용자가 버그로 볼 수 있다 | SPEC §6.3 | §6.3 표를 문서에 옮기거나 링크한다 |
| WARN-8 | `sources.py:279` vs `:311 · 343` | `procedure.attributes.group_id` 는 노드 id(`procedure_group:M1`)인데 `product.attributes.group_ids` 는 M 코드(`["M1"]`)다. 둘 다 SPEC 문구대로지만 응답에서 형식이 섞인다 | SPEC §3.2 · §4 | SPEC 에서 한쪽으로 맞추는 것을 OQ 로 남긴다(이번엔 코드 그대로) |
| WARN-9 | SPEC 환류 | 선택 ② `cited_source` · ③ `kind` · ⑤ 발행본 없을 때 `graph_version: null` 이 SPEC 본문에 없다 | SPEC §3.3 · §4 | 다음 SPEC 버전에 적는다 |

## 7. 사용자가 실물에서 만날 자리

1. **`.env.graph` 덮어쓰기** (WARN-6): 문서 1단계 `cp` 를 그대로 치면 stg 주소가 지워진다. 그 상태로 `graph_ingest` 를 돌리면 「PHUB_GRAPH_SOURCE_BASE_URL 이 없습니다」로 종료 코드 2 가 난다(`scripts/graph_ingest.py:84-86`). 주소는 `https://api-stg-csp.medisolveai.com/procedure-hub/api/v1`(조사 리포트 머리)이다.
2. **`--env-file` 을 빼먹으면** 핵심 설정이 `envs/.env` 를 읽는다(`core/config.py` `env_file`). 이 워크트리에는 `envs/.env` 가 없어 `DATABASE_URL` 이 비고 alembic · CLI 가 실패한다. 다른 체크아웃에서 `envs/.env` 가 있는 채로 돌리면 graph 테이블이 그 DB 에 생긴다. 반드시 문서 명령 그대로 친다.
3. **빌드 전에 E2E 스크립트를 돌리면** 표 대신 traceback 이 나온다(WARN-5). `graph_build` 결과가 `published` 인지 먼저 본다.
4. **`/tmp/phub-stg`**: S-7 의 `--from-dir` 원본이다. macOS 는 재부팅하면 `/tmp` 를 비운다. 같은 세션 안에서 1~7 을 끝내거나 레포 밖 다른 경로를 쓴다.
5. **S-4 M1↔M2 `conflict`** 는 버그가 아니다 — 「동일 부위 보톡스 먼저」와 「같은 날 필러 먼저」가 조건 구분 없이 부딪히는 원천 그대로다(SPEC §6.3 · OQ-S05). 문서에는 이 설명이 없다(WARN-7).
6. **응답이 큰 곳**: `procedure_group:M8` 을 `edge_types` 없이 이웃 · 부분 그래프로 펼치면 수백 KB 가 넘는다. Swagger 가 느려질 수 있다. 문서 §5 에 적혀 있다.
7. **노드 id 형식이 섞여 보임**: 시술 항목 `attributes.group_id` 는 `procedure_group:M8`, 제품 `attributes.group_ids` 는 `["M8"]` 이다(WARN-8).
8. **검색 「보톡스」** 는 같은 점수 후보가 여럿이다(두 제품 원장 57쌍 · 시술군 · 고민 항목). 원장을 합치지 않은 의도된 결과다(SPEC §6.3, 문서 §5 에 있음).
9. **`/graph/validation?build=latest`** 는 발행본이 없을 때 `graph_version: null` 을 준다. 의도된 동작이다(⑤).
10. Swagger 경로 파라미터의 `:` · 한글(`opt_concern:처짐탄력`)은 Swagger 가 인코딩해 준다. curl 로 칠 때는 URL 인코딩이 필요할 수 있다.

## 8. 확인하지 못한 것

- pytest · ruff · alembic up/down · E2E 실행 결과(브리프 §7 read-only — 워커 보고 수치를 그대로 옮긴다)
- MCP SDK 2.3.0 의 `dict[str, Any]` 반환이 structured output 으로 그대로 나가는지 — 코드와 테스트(`test_graph_mcp.py:58 · 92`)로만 확인했다
- stg 실측 숫자(941 · 1,504 · conflict 7)를 다시 세지 않았다 — `test_graph_stg_snapshot.py` 가 고정한다
