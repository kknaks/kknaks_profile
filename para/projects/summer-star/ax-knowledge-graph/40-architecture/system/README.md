# System Architecture

AX Knowledge Graph는 **Next.js UI + FastAPI API + PostgreSQL 운영 저장소 + Markdown document root + open-kknaks AI 실행**으로 구성한다. Redis는 MVP 필수 저장소가 아니라, 비동기 작업 큐/락/캐시가 필요해질 때 붙이는 보조 런타임으로 둔다.

```text
+-------------------+        HTTP/JSON        +-------------------+
| Next.js Web App   | <---------------------> | FastAPI API       |
| apps/web          |                         | apps/api          |
+-------------------+                         +---------+---------+
                                                        |
                                                        | SQLAlchemy/Alembic
                                                        v
                                                +-------+--------+
                                                | PostgreSQL     |
                                                | operational DB |
                                                +-------+--------+
                                                        |
                       validated file actions           | graph/index cache
                                                        v
                                                +-------+--------+
                                                | Markdown Root  |
                                                | data/documents |
                                                +----------------+

FastAPI -- open-kknaks task API --> open-kknaks provider runner (claude/codex)
FastAPI -- optional queue/cache --> Redis
```

## Runtime Stack

| Layer          | Choice                          | Responsibility                                                                          |
| -------------- | ------------------------------- | --------------------------------------------------------------------------------------- |
| Web            | Next.js + React + TypeScript    | Source Inbox, approval gates, graph/chat, settings                                      |
| API            | FastAPI + Pydantic v2 + SQLAlchemy 2.0 async (`postgresql+psycopg`, psycopg3 async) | auth, source workflow, gate workflow, graph API, settings API |
| DB             | PostgreSQL                      | operational state, approval revisions, drafts, apply plans, document index, graph cache |
| Migration      | Alembic (async 설정)            | schema changes and seed data                                                            |
| AI runner      | open-kknaks                     | summary, classification, documentation draft, Graph RAG answer generation               |
| Markdown SoT   | local/bind-mounted file root    | finalized`.md` documents only                                                         |
| Optional infra | Redis                           | background queue, idempotency locks, short-lived cache, pub/sub progress                |

## Monorepo Layout

구현 레포는 모노레포다. 아래는 WP0 Phase 2에서 scaffold를 깔며 확정한 구조의 역반영이다(AXKG-WORK-001).

```text
ax-graph/
  CLAUDE.md                      # 얇게 — agent.md를 읽으라고만 둔다
  agent.md                       # 에이전트 진입점
  context/                       # AI 스테이지 배경지식·방법 지침 문서 (worker 프로젝트 컨텍스트, claude가 읽음 — api 주입 아님, AXKG-SPEC-011)
    source-summary-guide.md      #   → 요약 지침은 apps/worker/workspace/context/로 이동(AXKG-WORK-002 Phase 3, profile-be); 나머지 스테이지 지침도 배선 시 동일 이동
    para-classification.md
    approval-gate-flow.md
    document-link-rules.md
    graph-chat-rules.md
  apps/
    worker/                      # open-kknaks ClaudeWorker (Redis consumer)
      workspace/                 # worker 이미지 내장 프로젝트 컨텍스트 (WORK_DIR, claude 진입점)
        CLAUDE.md                #   얇게 — agent.md를 읽으라고만
        agent.md                 #   worker 실행 에이전트 진입점
        context/
          source-summary-guide.md  # 요약 방법 지침 (api 미로드)
    web/                         # Next.js app
      app/
        login/
        approval/
        graph/
        settings/
      components/
      lib/api-client/
    api/
      axkg/                      # FastAPI app
        main.py
        config.py
        core/                    # database(async engine/session), security, redis
        models/                  # SQLAlchemy 2.0 ORM 모델
        repositories/            # DB 접근 계층 — DB session은 여기서만
        services/                # 비즈니스 로직 계층
        dto/                     # 내부 전달 객체 (서비스 계층 입출력, pydantic v2)
        schemas/                 # API 요청/응답 객체 (라우터 전용, pydantic v2)
        api/
          routes/                # 얇은 라우터 (auth, sources, gates, documents, graph, settings, prompts, templates)
        workers/
          ai_tasks.py
          apply_executor.py
          graph_rebuild.py
        integrations/
          open_kknaks.py           # OpenKknaksClient ABC + HTTP 스텁(참고용)
          redis_open_kknaks.py     # 실 바인딩 — AgentClient(RedisBroker namespace=axkg) producer (AXKG-WORK-002)
          slack.py
          source_collection/     # youtube, static_web, dynamic_web (AXKG-SPEC-012)
        storage/
          markdown_root.py
          markdown_parser.py
      alembic/                   # async 설정 migration + seed
      tests/
  packages/
    contracts/                   # OpenAPI-derived TS types or shared JSON schema
  data/
    documents/                   # 실험용 로컬 Markdown root
```

| Path                | Role                                                                                      |
| ------------------- | ----------------------------------------------------------------------------------------- |
| `agent.md`          | 에이전트 진입점. `CLAUDE.md`는 agent.md를 가리키는 얇은 포인터만 둔다                     |
| `context/`          | AI 스테이지 방법·배경 지침 문서. **worker 프로젝트 컨텍스트로 claude가 직접 읽는다**(api 조립·주입 아님). 요약 지침은 `apps/worker/workspace/context/`에 내장(AXKG-SPEC-011)      |
| `apps/`, `packages/` | runtime implementation and shared code                                                   |
| `data/documents/`   | 실험용 로컬 Markdown root                                                                  |

별도 template/prompt 파일 디렉토리는 두지 않는다. 템플릿·프롬프트의 런타임 SSOT는 DB이고(AXKG-SPEC-009/010), 초기 seed와 코드 fallback은 코드(마이그레이션/상수)가 소유한다.

## Service Boundaries

### Next.js Web App

- Holds no provider credentials.
- Calls FastAPI only; never calls open-kknaks or PostgreSQL directly.
- Renders optimistic progress from API state: `sources`, `approval_gates`, `approval_gate_revisions`, `ai_tasks`.
- Displays Markdown preview/diff returned by the API. The browser does not write Markdown files.

### FastAPI API

- Owns all state transitions.
- Creates `ai_tasks` rows and dispatches open-kknaks tasks.
- Persists AI outputs as `approval_gate_revisions.payload`, `drafts.payload`, and `apply_plans.payload`.
- Persists open-kknaks task/session ids on `ai_tasks` and gate/chat result rows for retry and feedback continuation.
- Runs Apply Executor after human approval.
- Exposes graph/search/chat APIs from PostgreSQL cache and Markdown-derived indexes.

### PostgreSQL

- Source of truth for operational state.
- Not the source of truth for finalized Markdown body.
- Stores document index/path, graph edge cache, approvals, settings, prompts, templates, auth tokens, AI task history.

### Markdown Document Root

- Source of truth for finalized document content.
- API writes here only through Apply Executor.
- `documents.path` stores document-root-relative paths, never absolute host paths.

### open-kknaks

- Runs AI provider tasks using configured provider/options/provider_options.
- **Binding = Redis 직결 `AgentClient`, HTTP 아님** (AXKG-WORK-002 Phase 3 확정). FastAPI api가 producer다: `RedisOpenKknaksClient`가 `AgentClient(RedisBroker(url=AXKG_REDIS_URL, namespace="axkg"))`를 감싸 `submit(prompt, context, provider, model, options, provider_options, metadata, queue="default", max_retries=0) -> task_id`로 태스크를 넣고 `result(task_id, timeout)`(XREAD BLOCK)로 결과를 받는다. open-kknaks `ClaudeWorker`가 같은 Redis + `namespace=axkg` + `queue=default`의 consumer다.
- `max_retries=0` 고정 — 재시도는 AXKG가 `retry_of_task_id` 새 row로 소유(AXKG-SPEC-002/011), broker 자동재시도와 이중 방지한다.
- Provider credential(`CLAUDE_CODE_OAUTH_TOKEN`)은 worker(consumer) 측에만 둔다(AXKG-SPEC-007: provider credential은 서버까지, 실제 실행은 worker). api/web에는 두지 않는다.
- Returns output to FastAPI. It never writes AXKG DB rows or Markdown files directly.
- **worker 실행 모델(AXKG-SPEC-011 Assembly Contract)**: worker(`ClaudeWorker`)는 스테이지 방법·배경 지침을 담은 프로젝트 컨텍스트를 **이미지에 내장**하고(배포 시 마운트/git pull 런타임 의존 회피, 빌드 시점 고정), 실행 작업 디렉토리(`WORK_DIR`)를 그 경로로 둔다. claude가 진입 `CLAUDE.md → agent.md → context/`를 스스로 읽는다. 요약 방법 지침(`source-summary-guide.md` 등)은 이 프로젝트 컨텍스트에 있고 api는 로드하지 않는다. 요약 작업용 프로젝트 컨텍스트는 코드레포 `apps/worker/workspace/`(profile-be 소관).
- Receives resolved prompt/context from FastAPI. api submit 표면 = **DB 프롬프트(작업 지시) + output_schema (+③ 활성 템플릿) + 런타임 원문/후보**뿐이다. 방법 지침은 프로젝트 컨텍스트가 담당한다. Prompt selection is controlled by `ai_task_definitions.prompt_key` and the active prompt version.
- Tool/workflow 정의는 코드레포(`.agent.md`/`decision-pipe.md` 등)가 관리하고 runner가 읽는다. 제품 설정 UI가 편집하는 것은 prompt/template뿐이다(AXKG-SPEC-009/010). VoltAgent(레거시 my-agent-app)는 참고용 레거시일 뿐 바인딩하지 않는다 — tool/workflow introspection이 필요해지면 자체 구현한다.
- Default settings:
  - `provider=claude`
  - `options.timeout_sec=300`
  - `provider_options.max_turns=3`
  - `provider_options.effort=medium`

### Redis

Redis is optional for MVP. Add it when the process model needs out-of-process background workers or real-time progress.

Use Redis for:

- AI task queue if FastAPI request lifecycle should not run tasks inline.
- Apply Executor lock: prevent duplicate apply for the same `apply_plan_id`.
- Graph rebuild debounce/cache.
- Progress pub/sub for long-running AI tasks.

Do not use Redis as durable workflow state. PostgreSQL remains the durable source for task/gate/apply status.

## API Layering

백엔드는 라우터 → 서비스 → 레포지토리 3계층으로 나눈다. 의존은 단방향이다 — 역방향 import를 금지한다.

```text
api.routes (라우터)  -->  services (비즈니스)  -->  repositories (DB 접근)  -->  models (ORM)
    schemas <-> dto              dto                      dto <-> ORM
```

- **라우터(`api/routes/`)**: 얇게 유지한다. 요청/응답 검증과 schemas↔dto 변환, 서비스 호출만 한다. 비즈니스 로직을 두지 않는다.
- **서비스(`services/`)**: 비즈니스 로직 계층. 입출력은 dto다. DB session에 직접 접근하지 않고 레포지토리를 통해서만 데이터에 닿는다.
- **레포지토리(`repositories/`)**: DB 접근 계층. **DB session은 레포지토리만 접근한다.** dto↔ORM 변환을 담당한다.
- **객체 분리**: `schemas/`는 API 요청/응답 객체(라우터 전용), `dto/`는 내부 전달 객체(서비스 계층 입출력). 둘 다 pydantic v2다.
- **DB 접속**: SQLAlchemy 2.0 async + `postgresql+psycopg`(psycopg3 async). Alembic도 async 설정으로 구성한다.

## FastAPI Modules

| Module                     | Key responsibilities                                                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `api.routes`             | 얇은 라우터 — 요청/응답 검증, schemas↔dto 변환, 서비스 호출. 비즈니스 로직 없음                                                        |
| `services.sources`       | URL validation, source lifecycle, summary retry                                                                                        |
| `services.gates`         | classification/documentation gate lifecycle, feedback, revision approval                                                               |
| `services.ai`            | AI task creation, retry chaining, open-kknaks request mapping                                                                          |
| `services.documents`     | draft storage, apply plan validation, Markdown path safety                                                                             |
| `services.graph`         | Markdown link parsing, graph cache rebuild, Graph RAG retriever (shared by chat and documentation-gate context builder, AXKG-SPEC-011) |
| `services.settings`      | AI provider settings, prompt versions, template versions                                                                               |
| `repositories.*`         | 도메인별 DB 접근 — 유일한 DB session 접근 계층, dto↔ORM 변환                                                                            |
| `models`                 | SQLAlchemy 2.0 ORM 모델 정의                                                                                                            |
| `dto` / `schemas`        | 서비스 계층 입출력 내부 전달 객체 / API 요청·응답 객체(라우터 전용) — 둘 다 pydantic v2                                                 |
| `core.database`          | SQLAlchemy 2.0 async engine/session (`postgresql+psycopg`)                                                                              |
| `workers.apply_executor` | validates and applies approved DB/file actions                                                                                         |
| `workers.ai_tasks`       | runs or polls open-kknaks tasks, stores outputs/failures                                                                               |
| `workers.graph_rebuild`  | rebuilds `documents`/`document_edges` cache from Markdown (see Graph Rebuild triggers)                                                 |
| `integrations.source_collection` | URL adapter selection + YouTube/static/dynamic web fetchers -> SourceMaterial (AXKG-SPEC-012, SSRF guard). api 프로세스 내 BackgroundTask에서 실행               |
| `integrations.redis_open_kknaks` | open-kknaks 실 바인딩 — `AgentClient(RedisBroker namespace=axkg, queue=default)` producer. worker(`ClaudeWorker`)가 consumer (AXKG-WORK-002 Phase 3)          |

## Request Flows

### AI Task Resolution

Every AI execution goes through a registered task definition before open-kknaks is called.

```text
task_type
  -> ai_task_definitions.key
  -> handler_kind decides context builder/result handler
  -> prompt_key loads active prompt version(prompt_text + output_schema[JSON Schema])
  -> template_key loads active template version (documentation_gate only)
  -> context builder assembles submit payload: prompt(작업 지시) + output_schema (+ documentation_gate: active template) + runtime data (AXKG-SPEC-011)
     documentation_gate runtime data adds connection candidate context:
       graph retriever top-N + documents index snapshot(stem/aliases/title/type)
     방법·배경 지침은 조립하지 않음 — worker 이미지 내장 프로젝트 컨텍스트(CLAUDE.md->agent.md->context/)를 claude가 실행 디렉토리에서 읽음
  -> global provider settings
  -> task definition defaults
  -> task_overrides[task_type]
  -> ai_tasks snapshot(provider/options/provider_options/prompt_version_id/template_version_id)
  -> open-kknaks Task
```

Active prompt/template load failure does not stop the pipeline: the context builder falls back to code-embedded defaults, records the fallback observably, and leaves `prompt_version_id`/`template_version_id` null (AXKG-SPEC-009/010 S-3, AXKG-SPEC-011).

`task_overrides` is dynamic for registered tasks. Adding an entirely new task from Settings is not arbitrary code execution; it requires a known `handler_kind` and a prompt key. Once a definition exists, provider/options/provider_options and prompt versions are dynamically manageable.

### Source Intake and Summary

```text
Next.js -> FastAPI POST /sources/manual
FastAPI -> PostgreSQL insert sources(status=received)
FastAPI -> commit, then schedule BackgroundTask  (Starlette가 BackgroundTask를 세션 teardown보다 먼저 실행 → 스케줄 직전 명시 commit)
[api BackgroundTask] -> received -> summarizing + ai_tasks create(task_type=collect_source_summary)
[api BackgroundTask] -> Source Collection Adapter (AXKG-SPEC-012, api 프로세스 내 실행)
           youtube | static_web | dynamic_web -> SourceMaterial
           canonical_url로 normalized_url 갱신 + 중복 재검사
[api BackgroundTask] -> AgentClient.submit (Redis namespace=axkg, queue=default)
           SourceMaterial 기반 context, 초과 길이는 chunk 요약 병합
open-kknaks ClaudeWorker (consumer) -> claude 실행 -> Redis result
[api BackgroundTask] -> AgentClient.result(timeout) -> sources.status=summarized, sources.summary_payload=...
```

수집(collect_source)은 api 프로세스 내 BackgroundTask에서 실행한다(별도 browser worker로 분리하지 않는다, AXKG-WORK-002 Phase 3). open-kknaks worker로 넘어가는 것은 요약 AI 실행뿐이다.

If summary fails:

- Store `ai_tasks.status=failed`.
- Keep source row.
- UI shows `요약 재시도`.
- Retry creates a new `ai_tasks` row with `retry_of_task_id=<failed_task_id>`.

### Classification Gate

```text
POST /sources/{source_id}/classification-gates
  -> create approval_gates(gate_kind=classification)
  -> create ai_tasks(generate_classification_gate)
  -> store ai_tasks.open_kknaks_session_id
  -> store approval_gate_revisions(v1, payload=classification proposal, open_kknaks_session_id)

POST /gates/{gate_id}/feedback
  -> gate_feedback row
  -> load target revision open_kknaks_session_id as resume session
  -> ai_tasks(regenerate_classification_gate, options.resume=true)
  -> store ai_tasks.open_kknaks_session_id
  -> approval_gate_revisions(v2, parent_revision_id=v1, open_kknaks_session_id)

POST /gates/{gate_id}/approve
  -> approve active revision
  -> source.destination_type confirmed
  -> if project/area/resource, create documentation gate
```

Classification gate output is PARA destination only. It does not create connection candidates.

### Documentation Gate and Apply

```text
classification approved
  -> approval_gates(gate_kind=documentation)
  -> context builder (AXKG-SPEC-011):
       graph retriever top-N candidates (shared with Graph RAG chat)
       + documents index snapshot(stem/aliases/title/document_type)
       + active template(template_key) + active prompt + output_schema
  -> ai_tasks(generate_documentation_gate)
  -> approval_gate_revisions(v1 payload includes draft + derived_suggestions + apply_plan)
  -> apply_plan pre-validation at revision creation (validation_status: pending -> valid/invalid,
     shown in U-5 preview before approve; full validation runs again at approve time)

POST /gates/{documentation_gate_id}/approve   (common gate action API, AXKG-SPEC-002)
  -> validate active revision and apply_plan
  -> Apply Executor validates db_actions/file_actions
  -> write Markdown files or patches
  -> update DB rows
  -> rebuild document_edges cache (incremental)
  -> source.status=documented, visible_in_inbox=false

Reclassification ("이 destination이 아님", AXKG-SPEC-004 S-3):
POST /gates/{documentation_gate_id}/feedback (not_this_destination_reason)
  -> documentation gate -> cancelled
  -> classification gate reopen: approved -> regenerating
     approved revision marked superseded, approved_revision_id cleared
  -> sources.destination_type / approved_classification_gate_id reset
  -> ai_tasks(regenerate_classification_gate) with reclassification reason
```

AI does not apply the plan. It proposes `draft + apply_plan`; Apply Executor is the only writer.

### Graph RAG Chat

```text
New chat:
  Next.js -> POST /graph/chats (question, selected_node_id?, filters?)
  FastAPI -> create graph_chat_sessions(chat_id)
  FastAPI -> create graph_chat_messages(role=user)
  FastAPI -> create graph_chat_runs(run_id, status=queued)
  FastAPI -> create ai_tasks(task_type=graph_rag_chat)
  Next.js -> poll GET /graph/chats/{chat_id}/runs/{run_id}
  Worker/FastAPI -> graph retriever(keyword score + edge distance)
  Worker/FastAPI -> open-kknaks with question + graph context + evidence docs
  Worker/FastAPI -> store assistant message + evidence + open_kknaks_session_id
  Next.js -> render completed assistant message

Existing chat:
  Next.js -> POST /graph/chats/{chat_id}/messages (question)
  FastAPI -> load graph_chat_sessions.last_open_kknaks_session_id
  FastAPI -> create user message + run + linked ai_task
  Worker/FastAPI -> pass previous open-kknaks session id when available
  Next.js -> poll run until succeeded/failed/cancelled
```

MVP retriever does not require pgvector. Add embeddings later only if keyword + graph distance is insufficient.
Chat history is user-scoped and persisted in PostgreSQL. `ai_tasks` tracks provider execution; `graph_chat_runs` tracks product-level response status and polling state.

### Graph Rebuild

`documents`/`document_edges`는 Markdown에서 재빌드 가능한 cache다(AXKG-SPEC-005). MVP 재인덱스 트리거는 세 가지다:

```text
1. startup scan     — API 기동 시 content_hash 비교로 변경 파일만 재인덱스
2. apply executor   — 문서화 게이트 approve 적용 직후 해당 문서 증분 rebuild
3. manual API       — POST /graph/rebuild (Obsidian 등 외부 편집 후 사용자가 호출)
```

파일 watcher 기반 자동 감지는 post-MVP다. 외부(Obsidian/git) 편집 직후 그래프가 stale할 수 있으며, 수동 rebuild 또는 재기동으로 동기화한다.

## API Surface

| Area          | Routes                                                                                                                                                                                                                                                            |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Auth          | `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`                                                                                                                                                                                                     |
| Sources       | `POST /sources/manual`, `GET /sources`, `GET /sources/{id}`, `POST /sources/{id}/queue-collection`, `GET /sources/{id}/ai-tasks`                                                                                                                                                        |
| Integrations  | `POST /api/v1/slack/commands` — Slack 슬래시 커맨드 intake. 등록 Request URL과 문자 그대로 일치(무prefix 관례 예외) (AXKG-SPEC-003)                                                                                                                                                                                            |
| Gates         | `GET /sources/{id}/gates`, `POST /sources/{id}/classification-gates`, `POST /gates/{id}/feedback`, `POST /gates/{id}/regenerate`, `POST /gates/{id}/retry`, `POST /gates/{id}/approve` — 분류·문서화 공통 액션 API (AXKG-SPEC-002)                                                                |
| Documentation | `GET /documentation-gates`, `GET /documentation-gates/{source_id}/drafts/{version}/markdown` — 조회 전용 뷰. 액션은 Gates 공통 API 사용 (AXKG-SPEC-004)          |
| Documents     | `GET /documents`, `GET /documents/{id}`, `GET /documents/{id}/markdown`, `GET /documents/{id}/links`, `POST /documents/{id}/link-preview`                                                                                                                                                      |
| Graph         | `GET /graph/documents`, `GET /graph/documents/{id}/neighborhood`, `POST /graph/search`, `POST /graph/rebuild`, `GET /graph/chats`, `POST /graph/chats`, `GET /graph/chats/{chat_id}`, `POST /graph/chats/{chat_id}/messages`, `GET /graph/chats/{chat_id}/runs/{run_id}` |
| Settings      | `GET/PUT /settings/ai-provider`, `GET /settings/ai-provider/health`, `PUT/DELETE /settings/ai-provider/task-overrides/{task_key}`                                                                                                                                                                                           |
| Prompts       | `GET /prompts`, `GET /prompts/{key}`, `GET /prompts/{key}/versions`, `POST /prompts/{key}/versions`, `POST /prompts/{key}/rollback`                                                                                                                     |
| Templates     | `GET /templates`, `GET /templates/{key}`, `GET /templates/{key}/versions`, `POST /templates/{key}/versions`, `POST /templates/{key}/rollback`                                                                                                           |

## Configuration

| Env                           | Default            | Notes                    |
| ----------------------------- | ------------------ | ------------------------ |
| `AXKG_DATABASE_URL`         | required           | PostgreSQL DSN           |
| `AXKG_REDIS_URL`            | empty              | open-kknaks 실행 broker(`namespace=axkg`, `queue=default`) 겸 optional queue/cache. producer(api)·worker(`ClaudeWorker`) 공유. 미설정 시 요약 자동 트리거 조용히 생략 |
| `AXKG_MARKDOWN_ROOT`        | `data/documents` | local dev document root  |
| `AXKG_OPEN_KKNAKS_BASE_URL` | required           | HTTP 스텁(`open_kknaks.py`, 참고용)용 endpoint. **실 바인딩은 `AXKG_REDIS_URL` Redis broker** — required 여부는 배포 시 admin 재확인 |
| `AXKG_AUTH_TOKEN_TTL_DAYS`  | `30`             | MVP token expiry         |
| `AXKG_DEFAULT_PROVIDER`     | `claude`         | seed setting only        |
| `AXKG_SLACK_SIGNING_SECRET` | required for Slack intake | `POST /api/v1/slack/commands` 슬래시 커맨드 서명 검증 |
| `AXKG_SLACK_BOT_TOKEN`      | required for Slack intake | 앵커 메시지 post·스레드 요약 회신용 |

## Invariants

- No finalized Markdown write without approved documentation gate revision.
- No DB/file action execution by AI provider output alone.
- Retry never overwrites failed `ai_tasks`; it creates a new row linked by `retry_of_task_id`.
- `documented` sources are hidden from the default Source Inbox, not deleted.
- `deleted` sources are soft-deleted.
- Graph edges in PostgreSQL are cache; Markdown wikilinks and `up` are canonical.
- `frontmatter.links` alone does not create graph edges.
- Graph Chat sessions/messages/runs are user-scoped and persisted; polling reads `graph_chat_runs.status`, not raw open-kknaks state directly.

## Open Items

- ~~Choose initial background execution mode: inline FastAPI task vs Redis-backed worker.~~ → Source Intake 경로 확정(AXKG-WORK-002 Phase 3): 수집은 **api 프로세스 내 BackgroundTask**, AI 실행은 **Redis-backed open-kknaks worker**(`AgentClient(RedisBroker)`). 후속 스테이지(분류/문서화 게이트)의 트리거 모델은 해당 WP에서 확정.
- Decide whether local `data/documents` should be committed examples or runtime-only gitignored content.
- Write Alembic migrations from `../database/README.md`.

