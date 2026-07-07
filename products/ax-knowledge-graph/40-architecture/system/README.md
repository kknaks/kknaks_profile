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
| API            | FastAPI + Pydantic + SQLAlchemy | auth, source workflow, gate workflow, graph API, settings API                           |
| DB             | PostgreSQL                      | operational state, approval revisions, drafts, apply plans, document index, graph cache |
| Migration      | Alembic                         | schema changes and seed data                                                            |
| AI runner      | open-kknaks                     | summary, classification, documentation draft, Graph RAG answer generation               |
| Markdown SoT   | local/bind-mounted file root    | finalized`.md` documents only                                                         |
| Optional infra | Redis                           | background queue, idempotency locks, short-lived cache, pub/sub progress                |

## Monorepo Layout

Target implementation repo is a monorepo. Keep the same workspace shape as `kknaks_profile`: product docs and knowledge roots stay at the repository root, while runtime code lives under `apps` and shared contracts under `packages`.

```text
/
  agent.md                      # workspace-level agent operating guide
  .agent/                       # local agent tools used by this repo
    hooks/
    scripts/
    skills/
  rules/                        # product/document pipeline rules
  templates/                    # reusable markdown/template seeds
    context/
    product/
  context/                      # company/studio context notes
  inbox/                        # raw captured sources before curation
  permanent/                    # durable knowledge notes
  reference/                    # external/reference materials
  workspace/                    # local scratch/runtime workspace, gitignored as needed
    ax-knowledge-graph/

  apps/
    web/                         # Next.js app
      app/
        approval/
        graph/
        settings/
      components/
      lib/api-client/
    api/                         # FastAPI app
      axkg/
        main.py
        config.py
        api/
          routes/
            auth.py
            sources.py
            approval_gates.py
            documentation_gates.py
            documents.py
            graph.py
            settings.py
            prompts.py
            templates.py
        core/
          security.py
          database.py
          redis.py
        domain/
          sources/
          gates/
          documents/
          graph/
          ai/
          settings/
        workers/
          ai_tasks.py
          apply_executor.py
          graph_rebuild.py
        integrations/
          open_kknaks.py
          slack.py
        storage/
          markdown_root.py
          markdown_parser.py
      alembic/
      tests/
  packages/
    contracts/                   # OpenAPI-derived TS types or shared JSON schema
    ui/                          # optional shared UI primitives
  data/
    documents/                   # local dev Markdown root, gitignored if runtime generated
  products/
    ax-knowledge-graph/
      00-baseline/
      20-spec/
      21-html/
      30-work/
      40-architecture/
```

Root knowledge directories are not incidental. AXKG reads from and writes around this repository shape:

| Path                                         | Role                                                                         |
| -------------------------------------------- | ---------------------------------------------------------------------------- |
| `agent.md`                                 | human/agent operating instructions for the repository                        |
| `.agent/`                                  | local skills, hooks, scripts, and automation helpers                         |
| `templates/`                               | source templates for context/product documents and generated markdown shapes |
| `rules/`                                   | curation and product-document pipeline rules                                 |
| `context/`, `reference/`, `permanent/` | existing knowledge roots that can become graph inputs                        |
| `inbox/`                                   | raw source intake before classification/documentation gates                  |
| `products/ax-knowledge-graph/`             | AXKG product specs, HTML mocks, work items, architecture docs                |
| `apps/`, `packages/`                     | runtime implementation and shared code                                       |

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
- Returns output to FastAPI. It never writes AXKG DB rows or Markdown files directly.
- Receives resolved prompt/context from FastAPI. Prompt selection is controlled by `ai_task_definitions.prompt_key` and the active prompt version.
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

## FastAPI Modules

| Module                     | Key responsibilities                                                                                                                   |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `domain.sources`         | URL validation, source lifecycle, summary retry                                                                                        |
| `domain.gates`           | classification/documentation gate lifecycle, feedback, revision approval                                                               |
| `domain.ai`              | AI task creation, retry chaining, open-kknaks request mapping                                                                          |
| `domain.documents`       | draft storage, apply plan validation, Markdown path safety                                                                             |
| `domain.graph`           | Markdown link parsing, graph cache rebuild, Graph RAG retriever (shared by chat and documentation-gate context builder, AXKG-SPEC-011) |
| `domain.settings`        | AI provider settings, prompt versions, template versions                                                                               |
| `workers.apply_executor` | validates and applies approved DB/file actions                                                                                         |
| `workers.ai_tasks`       | runs or polls open-kknaks tasks, stores outputs/failures                                                                               |
| `workers.graph_rebuild`  | rebuilds `documents`/`document_edges` cache from Markdown (see Graph Rebuild triggers)                                                 |
| `integrations.source_collection` | URL adapter selection + YouTube/static/dynamic web fetchers -> SourceMaterial (AXKG-SPEC-012, SSRF guard)                       |

## Request Flows

### AI Task Resolution

Every AI execution goes through a registered task definition before open-kknaks is called.

```text
task_type
  -> ai_task_definitions.key
  -> handler_kind decides context builder/result handler
  -> prompt_key loads active prompt version(prompt_text + output_schema[JSON Schema])
  -> template_key loads active template version (documentation_gate only)
  -> context builder assembles: template -> prompt -> output_schema (AXKG-SPEC-011)
     documentation_gate adds connection candidate context:
       graph retriever top-N + documents index snapshot(stem/aliases/title/type)
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
FastAPI -> ai_tasks create(task_type=collect_source_summary)
FastAPI -> Source Collection Adapter (AXKG-SPEC-012)
           youtube | static_web | dynamic_web -> SourceMaterial
           canonical_url로 normalized_url 갱신 + 중복 재검사
Worker/FastAPI -> open-kknaks (SourceMaterial 기반 context, 초과 길이는 chunk 요약 병합)
open-kknaks -> summary result
FastAPI -> sources.status=summarized, sources.summary_payload=...
```

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
| Integrations  | `POST /integrations/slack/sources` — Slack intake (AXKG-SPEC-003)                                                                                                                                                                                            |
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
| `AXKG_REDIS_URL`            | empty              | optional                 |
| `AXKG_MARKDOWN_ROOT`        | `data/documents` | local dev document root  |
| `AXKG_OPEN_KKNAKS_BASE_URL` | required           | open-kknaks API endpoint |
| `AXKG_AUTH_TOKEN_TTL_DAYS`  | `30`             | MVP token expiry         |
| `AXKG_DEFAULT_PROVIDER`     | `claude`         | seed setting only        |
| `AXKG_SLACK_SIGNING_SECRET` | required for Slack intake | `POST /integrations/slack/sources` 요청 서명 검증 |
| `AXKG_SLACK_BOT_TOKEN`      | empty            | optional — 수신 완료 reaction/응답용 |

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

- Choose initial background execution mode: inline FastAPI task vs Redis-backed worker.
- Decide whether local `data/documents` should be committed examples or runtime-only gitignored content.
- Write Alembic migrations from `../database/README.md`.

