# Database Architecture

AX Knowledge Graph의 저장소 원칙:

```text
Markdown file = finalized document body SoT
PostgreSQL = operational state / approval workflow / draft payload / document index / graph cache
Redis = optional volatile queue/cache/lock, never durable workflow SoT
```

관련 decision: `../../10-decision/decision-002-markdown-sot-postgres-storage.md`

## Design Rules

- Use UUID primary keys for application entities.
- Use `created_at`, `updated_at` on mutable operational tables.
- Use explicit enum-like text columns plus `CHECK` constraints in first migration.
- Use JSONB for AI payloads and flexible settings, not for core query keys.
- Store workspace-root-relative paths only. No absolute host paths in DB.
- Keep failed AI task history immutable; retries create new rows linked by `retry_of_task_id`.
- `approval_gates` is the gate container; `approval_gate_revisions` is the actual AI proposal version.

## SoT Boundary

| Data | SoT | Notes |
|---|---|---|
| Final Markdown body | Markdown file | Obsidian, git, product UI read the same `.md` |
| Document path/index | PostgreSQL `documents.path` | relative to configured workspace root |
| Source Inbox state | PostgreSQL `sources` | raw input lifecycle, visibility, soft delete |
| Approval gates | PostgreSQL `approval_gates` | source + gate kind container |
| Gate proposals | PostgreSQL `approval_gate_revisions` | v1/v2 actual AI outputs |
| Feedback | PostgreSQL `gate_feedback` | user instruction for regeneration |
| Drafts/apply plans | PostgreSQL `drafts`, `apply_plans` | pre-approval payloads and executor plan |
| Graph edges | Markdown wikilink/up | PostgreSQL `document_edges` is rebuildable cache |
| Graph Chat history | PostgreSQL `graph_chat_sessions`, `graph_chat_messages`, `graph_chat_runs` | user-scoped chat list, message history, response polling state |
| AI execution | PostgreSQL `ai_tasks` + open-kknaks task id | durable trace and retry chain |
| Settings/prompts/templates | PostgreSQL | operational configuration, not Markdown SoT |

## Extensions

MVP needs only standard PostgreSQL plus UUID support:

```sql
create extension if not exists pgcrypto;
```

Do not add pgvector for MVP. Graph RAG starts with keyword score + edge distance.

## Core Enums

Implement as `TEXT CHECK (...)` first. Native Postgres enums can come later if needed.

| Name | Values |
|---|---|
| `source_status` | `received`, `summarizing`, `summarized`, `collection_failed`, `ignored`, `documented`, `archived`, `deleted` |
| `source_channel` | `slack`, `manual` |
| `destination_type` | `project`, `area`, `resource`, `archive` |
| `gate_kind` | `classification`, `documentation` |
| `approval_gate_status` | `not_started`, `generating`, `review_pending`, `feedback_pending`, `regenerating`, `approved`, `failed`, `cancelled` |
| `approval_revision_status` | `drafting`, `reviewable`, `approved`, `superseded`, `rejected`, `failed` |
| `ai_task_status` | `queued`, `running`, `succeeded`, `failed`, `cancelled` |
| `apply_plan_status` | `pending`, `valid`, `invalid`, `applying`, `applied`, `failed` |
| `file_action_type` | `create_markdown`, `patch_markdown`, `update_frontmatter` |
| `document_type` | `reference`, `permanent`, `concept`, `baseline`, `decision`, `spec`, `work`, `source` |
| `edge_type` | `assoc`, `lineage` |
| `provider` | `claude`, `codex` |
| `chat_session_status` | `active`, `archived`, `deleted` |
| `chat_message_role` | `user`, `assistant`, `system` |
| `chat_run_status` | `queued`, `running`, `succeeded`, `failed`, `cancelled` |
| `ai_handler_kind` | `source_summary`, `classification_gate`, `documentation_gate`, `graph_rag_chat` |

## Table Groups

### Auth

#### `users`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | default `gen_random_uuid()` |
| `email` | text unique not null | seed: `kknaks@medisolveai.com` |
| `password_hash` | text not null | never store plain password |
| `display_name` | text | |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

#### `auth_tokens`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `user_id` | uuid fk users | |
| `token_hash` | text unique not null | store hash only |
| `expires_at` | timestamptz not null | |
| `revoked_at` | timestamptz | logout |
| `created_at` | timestamptz not null | |

Indexes:

- `auth_tokens(token_hash)`
- `auth_tokens(user_id, revoked_at, expires_at)`

### Source Inbox

#### `sources`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `source_url` | text not null | http/https only |
| `normalized_url` | text not null | duplicate detection |
| `source_channel` | text not null | `slack` or `manual` |
| `submitted_by` | uuid fk users nullable | Slack user can live in metadata for MVP |
| `submitted_at` | timestamptz not null | |
| `raw_text` | text | Slack message or manual note |
| `status` | text not null | source lifecycle |
| `visible_in_inbox` | boolean not null default true | false for `documented`, `archived`, `deleted` |
| `summary_payload` | jsonb not null default `{}` | title/summary/tags/type seed |
| `destination_type` | text | set after classification approval |
| `approved_classification_gate_id` | uuid fk approval_gates nullable | |
| `approved_documentation_gate_id` | uuid fk approval_gates nullable | |
| `metadata` | jsonb not null default `{}` | Slack/manual metadata |
| `documented_at` | timestamptz | |
| `deleted_at` | timestamptz | soft delete |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes:

- unique `sources(normalized_url)` where `deleted_at is null`
- `sources(status, visible_in_inbox, submitted_at desc)`
- `sources(destination_type)`

Rules:

- `documented` does not delete the source; set `visible_in_inbox=false`.
- `deleted` is soft delete; set `deleted_at`, keep row.
- `collection_failed` should have a failed summary `ai_tasks` row.
- `metadata` jsonb 규약: Slack 수신은 `metadata.slack_events[]`(ts/channel/user/text snippet)로 누적한다. 중복 URL 재수신 시 새 row를 만들지 않고 이 배열에 이벤트를 추가하고, 이미 `documented`면 `metadata.duplicate_candidate=true`를 표시한다(AXKG-SPEC-003 S-2).

### Approval Gates

#### `approval_gates`

Gate container. One source can have one classification gate and one documentation gate.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `source_id` | uuid fk sources not null | |
| `gate_kind` | text not null | `classification` or `documentation` |
| `status` | text not null | container lifecycle |
| `active_revision_id` | uuid nullable | latest review target |
| `approved_revision_id` | uuid nullable | final approved revision |
| `last_ai_task_id` | uuid nullable | last generation/regeneration task |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes/constraints:

- unique `approval_gates(source_id, gate_kind)`
- `approval_gates(status, gate_kind)`
- `approval_gates(active_revision_id)`
- `approval_gates(approved_revision_id)`

Rules:

- 문서화 게이트는 별도 테이블이 아니라 `gate_kind=documentation` row다. UI 표시 상태(draft_generating 등)는 파생이며 저장 SSOT는 `approval_gates.status`다(AXKG-SPEC-004 매핑표).
- Reclassification("이 destination이 아님", AXKG-SPEC-004 S-3): 분류 게이트를 재오픈한다 — status `approved → regenerating`, 기존 approved revision은 `superseded`로 마킹(내용 불변), `approved_revision_id` 해제, `sources.destination_type`·`approved_classification_gate_id` 리셋. 해당 documentation gate는 `cancelled`. unique(source_id, gate_kind) 제약은 유지된다(새 게이트를 만들지 않고 재오픈).

#### `approval_gate_revisions`

Actual AI proposals. User approves or gives feedback on a revision, not on the abstract container.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `gate_id` | uuid fk approval_gates not null | |
| `version` | integer not null | v1/v2/v3 per gate |
| `status` | text not null | revision lifecycle |
| `payload` | jsonb not null | `classification.v1` or `documentation.v1` |
| `form_schema_version` | text not null | payload UI schema |
| `parent_revision_id` | uuid fk approval_gate_revisions nullable | regenerated from |
| `feedback_id` | uuid fk gate_feedback nullable | feedback that caused this revision |
| `ai_task_id` | uuid fk ai_tasks nullable | task that created it |
| `open_kknaks_session_id` | text | session/thread id returned by the AI run that created this revision |
| `created_at` | timestamptz not null | |
| `approved_at` | timestamptz | |

Indexes/constraints:

- unique `approval_gate_revisions(gate_id, version)`
- `approval_gate_revisions(gate_id, status, version desc)`
- `approval_gate_revisions(ai_task_id)`
- `approval_gate_revisions(open_kknaks_session_id)` where not null

Payload conventions:

- Classification payload includes `destination_type`, `destination_reason`, `suggested_title`, `suggested_tags`, `source_summary`, `confidence`.
- Documentation payload includes `document_draft`, `derived_suggestions`, `apply_plan_id` or embedded apply plan snapshot.

#### `gate_feedback`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `gate_id` | uuid fk approval_gates not null | |
| `target_revision_id` | uuid fk approval_gate_revisions not null | |
| `body` | text not null | user feedback |
| `quick_options` | jsonb not null default `[]` | e.g. destination change |
| `payload` | jsonb not null default `{}` | `not_this_destination_reason`, etc. |
| `status` | text not null default `submitted` | `submitted`, `consumed`, `cancelled` |
| `created_at` | timestamptz not null | |
| `consumed_at` | timestamptz | |

Indexes:

- `gate_feedback(gate_id, created_at desc)`
- `gate_feedback(target_revision_id)`

### AI Tasks

#### `ai_task_definitions`

Registered AI task definitions connect execution settings with prompt management. Settings can create or edit overrides only for registered definitions. Prompts are selected through `prompt_key`.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `key` | text unique not null | task type key, e.g. `graph_rag_chat` |
| `display_name` | text not null | settings UI label |
| `description` | text | |
| `handler_kind` | text not null | code-known handler. Not arbitrary executable code |
| `prompt_key` | text not null | links to `prompts.key` |
| `template_key` | text nullable | links to `document_templates.key`. Set for `documentation_gate` handler only (AXKG-DEC-005) |
| `default_provider` | text | optional task default, otherwise global provider |
| `default_model` | text | optional task model override |
| `default_options` | jsonb not null default `{}` | task defaults, e.g. timeout |
| `default_provider_options` | jsonb not null default `{}` | task defaults, e.g. max_turns/effort |
| `enabled` | boolean not null default true | disabled tasks cannot be run |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes:

- unique `ai_task_definitions(key)`
- `ai_task_definitions(enabled, handler_kind)`
- `ai_task_definitions(prompt_key)`

Rules:

- `settings.ai_provider.task_overrides` keys must exist in `ai_task_definitions.key`.
- Creating a definition dynamically is allowed only for known `handler_kind` values; handler code is not dynamic.
- A new feature becomes settings-manageable when it has an `ai_task_definitions` row and a matching `prompts` row.

#### `ai_tasks`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `task_type` | text not null | `collect_source_summary`, `generate_classification_gate`, `regenerate_classification_gate`, `generate_documentation_gate`, `regenerate_documentation_gate`, `graph_rag_chat` |
| `task_definition_id` | uuid fk ai_task_definitions nullable | definition used to resolve prompt/settings |
| `status` | text not null | |
| `source_id` | uuid fk sources nullable | |
| `gate_id` | uuid fk approval_gates nullable | |
| `revision_id` | uuid fk approval_gate_revisions nullable | set after revision creation if applicable |
| `retry_of_task_id` | uuid fk ai_tasks nullable | never overwrite failed task |
| `retry_count` | integer not null default 0 | derived or denormalized |
| `provider` | text not null | `claude` or `codex` |
| `model` | text | optional override |
| `options` | jsonb not null default `{}` | includes `timeout_sec`, `resume` |
| `provider_options` | jsonb not null default `{}` | includes `max_turns`, `effort` |
| `open_kknaks_task_id` | text | external task id |
| `open_kknaks_session_id` | text | external session/thread id returned by open-kknaks |
| `prompt_version_id` | uuid fk prompt_versions nullable | active prompt version snapshot used. null when code fallback ran |
| `template_version_id` | uuid fk document_template_versions nullable | active template version snapshot used (documentation gate tasks). null when code fallback ran |
| `payload` | jsonb not null default `{}` | request/response snapshot, resolved prompt/context (documentation gate: retriever candidates + documents index snapshot, AXKG-SPEC-011) |
| `error_code` | text | |
| `error_message` | text | |
| `queued_at` | timestamptz not null | |
| `started_at` | timestamptz | |
| `finished_at` | timestamptz | |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes:

- `ai_tasks(status, queued_at)`
- `ai_tasks(task_type, status)`
- `ai_tasks(task_definition_id, created_at desc)`
- `ai_tasks(prompt_version_id)`
- `ai_tasks(template_version_id)`
- `ai_tasks(source_id, created_at desc)`
- `ai_tasks(gate_id, created_at desc)`
- `ai_tasks(retry_of_task_id)`
- unique `ai_tasks(open_kknaks_task_id)` where `open_kknaks_task_id is not null`
- `ai_tasks(open_kknaks_session_id)` where `open_kknaks_session_id is not null`

### Drafts and Apply Plans

#### `drafts`

Drafts are pre-approval artifacts. Final Markdown body still lives in the file system.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `source_id` | uuid fk sources nullable | |
| `gate_revision_id` | uuid fk approval_gate_revisions not null | |
| `draft_type` | text not null | `main_document`, `derived_suggestion` |
| `version` | integer not null | tied to revision version |
| `filename_candidate` | text | |
| `target_path` | text | document-root-relative target |
| `change_kind` | text not null | `create` or `modify` |
| `payload` | jsonb not null | frontmatter preview, body preview, full markdown, diff |
| `created_at` | timestamptz not null | |

Indexes:

- `drafts(gate_revision_id, draft_type)`
- `drafts(target_path)`

#### `apply_plans`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `gate_revision_id` | uuid fk approval_gate_revisions not null | |
| `status` | text not null | validation/apply lifecycle |
| `validation_status` | text not null | `pending`, `valid`, `invalid` |
| `db_actions` | jsonb not null default `[]` | typed DB actions |
| `file_actions` | jsonb not null default `[]` | `create_markdown`, `patch_markdown`, `update_frontmatter` |
| `validation_errors` | jsonb not null default `[]` | |
| `applied_at` | timestamptz | |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes/constraints:

- unique `apply_plans(gate_revision_id)`
- `apply_plans(status, validation_status)`

File action rules:

| Action | Required fields | Rendering |
|---|---|---|
| `create_markdown` | `target_path`, `markdown` | full `.md` preview |
| `patch_markdown` | `target_path`, `patch` or `diff_preview` | diff preview |
| `update_frontmatter` | `target_path`, `frontmatter_patch` | diff preview |

Derived suggestion mapping:

| suggestion_type | target | file action |
|---|---|---|
| `supplement_existing_concept` | existing concept/permanent doc | `patch_markdown` or `update_frontmatter` |
| `create_new_concept` | new concept/permanent doc | `create_markdown` |
| `create_project_baseline` | `products/ax-knowledge-graph/00-baseline/*.md` | `create_markdown` |

### Documents and Graph Cache

#### `documents`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `path` | text unique not null | workspace root relative path |
| `stem` | text unique not null | filename stem or canonical id |
| `document_type` | text not null | |
| `title` | text not null | parsed from frontmatter |
| `aliases` | text[] not null default `{}` | resolve wikilinks |
| `tags` | text[] not null default `{}` | |
| `source_url` | text | external URL property |
| `frontmatter` | jsonb not null default `{}` | parsed metadata snapshot |
| `content_hash` | text not null | detect file changes |
| `indexed_at` | timestamptz not null | |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes:

- unique `documents(path)`
- unique `documents(stem)`
- GIN `documents(aliases)`
- GIN `documents(tags)`
- `documents(document_type)`

#### `document_edges`

Rebuildable cache from Markdown body wikilinks and frontmatter `up`.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `from_document_id` | uuid fk documents not null | |
| `to_document_id` | uuid fk documents nullable | null if broken |
| `to_target` | text not null | raw target stem/path from wikilink/up |
| `edge_type` | text not null | `assoc` or `lineage` |
| `source_syntax` | text not null | `wikilink`, `up` |
| `label` | text | label part of `[[target|label]]` |
| `is_broken` | boolean not null default false | unresolved target |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes/constraints:

- unique `document_edges(from_document_id, to_target, edge_type, source_syntax)`
- `document_edges(from_document_id)`
- `document_edges(to_document_id)`
- `document_edges(edge_type)`
- `document_edges(is_broken)`

Rules:

- Body `[[ ]]` creates `assoc`.
- `up` creates `lineage` and must also exist as body wikilink.
- `frontmatter.links` does not create edges.

### Graph Chat

Graph Chat is user-scoped and persistent. A chat session stores the conversation container, messages store durable history, and runs track one assistant response generation attempt. The frontend should poll `graph_chat_runs.status` through the API until the run reaches a terminal state.

#### `graph_chat_sessions`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | `chat_id` exposed to client |
| `user_id` | uuid fk users not null | owner |
| `title` | text not null | first question summary or user edited title |
| `status` | text not null default `active` | `active`, `archived`, `deleted` |
| `selected_document_id` | uuid fk documents nullable | default context from graph node |
| `last_open_kknaks_session_id` | text | provider session/thread id to resume existing chat |
| `metadata` | jsonb not null default `{}` | filters, graph view state, UI hints |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |
| `last_message_at` | timestamptz | list ordering |
| `deleted_at` | timestamptz | soft delete |

Indexes:

- `graph_chat_sessions(user_id, status, last_message_at desc)`
- `graph_chat_sessions(selected_document_id)`
- `graph_chat_sessions(last_open_kknaks_session_id)` where not null

#### `graph_chat_messages`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `session_id` | uuid fk graph_chat_sessions not null | |
| `role` | text not null | `user`, `assistant`, `system` |
| `content` | text not null | rendered message body |
| `sequence_no` | integer not null | stable ordering within session |
| `run_id` | uuid fk graph_chat_runs nullable | assistant message generated by this run |
| `selected_document_id` | uuid fk documents nullable | user context at send time |
| `evidence` | jsonb not null default `{}` | assistant evidence documents/edges/paths |
| `metadata` | jsonb not null default `{}` | token count, confidence, missing context |
| `created_at` | timestamptz not null | |

Indexes/constraints:

- unique `graph_chat_messages(session_id, sequence_no)`
- `graph_chat_messages(session_id, created_at)`
- `graph_chat_messages(run_id)`

#### `graph_chat_runs`

One run means one assistant response generation attempt for a user message.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | exposed as `run_id` for polling |
| `session_id` | uuid fk graph_chat_sessions not null | |
| `user_message_id` | uuid fk graph_chat_messages not null | |
| `assistant_message_id` | uuid fk graph_chat_messages nullable | set on success |
| `ai_task_id` | uuid fk ai_tasks nullable | open-kknaks execution trace |
| `status` | text not null | `queued`, `running`, `succeeded`, `failed`, `cancelled` |
| `open_kknaks_session_id` | text | session/thread id used for this run |
| `selected_document_id` | uuid fk documents nullable | context snapshot |
| `filters` | jsonb not null default `{}` | request filters |
| `retrieval_context` | jsonb not null default `{}` | selected docs, edges, paths, ranking |
| `result_payload` | jsonb not null default `{}` | answer, evidence, missing_context, suggested_actions |
| `error_code` | text | |
| `error_message` | text | |
| `queued_at` | timestamptz not null | |
| `started_at` | timestamptz | |
| `finished_at` | timestamptz | |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

Indexes:

- `graph_chat_runs(session_id, created_at desc)`
- `graph_chat_runs(status, queued_at)`
- `graph_chat_runs(ai_task_id)`
- `graph_chat_runs(open_kknaks_session_id)` where not null

Chat flow rules:

- New chat:
  - create `graph_chat_sessions`
  - insert user `graph_chat_messages`
  - create `graph_chat_runs`
  - create linked `ai_tasks(task_type=graph_rag_chat)`
  - poll run status until terminal
- Existing chat:
  - use existing `chat_id`
  - pass `last_open_kknaks_session_id` as resume/session context when available
  - insert new user message and new run
  - update `last_open_kknaks_session_id` from run result
- Result storage:
  - assistant answer is stored as `graph_chat_messages(role=assistant)`
  - evidence/result snapshot is stored on both `graph_chat_runs.result_payload` and assistant message `evidence`
  - `ai_tasks` stores provider/options/open-kknaks request-response snapshot

### Settings, Prompts, Templates

#### `settings`

Generic settings table for keyed configuration.

| Column | Type | Notes |
|---|---|---|
| `key` | text pk | e.g. `ai_provider` |
| `value` | jsonb not null | |
| `updated_by` | uuid fk users nullable | |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

`ai_provider` default value:

```json
{
  "provider": "claude",
  "model": null,
  "options": { "timeout_sec": 300, "resume": false },
  "provider_options": { "max_turns": 3, "effort": "medium" },
  "task_overrides": {}
}
```

`task_overrides` example:

```json
{
  "graph_rag_chat": {
    "options": { "timeout_sec": 600 },
    "provider_options": { "max_turns": 6, "effort": "high" }
  }
}
```

The keys are validated against `ai_task_definitions.key`.

#### `prompts`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `key` | text unique not null | e.g. `classification_gate` |
| `name` | text not null | |
| `description` | text | |
| `active_version_id` | uuid nullable | fk added after versions table |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

#### `prompt_versions`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `prompt_id` | uuid fk prompts not null | |
| `version` | integer not null | |
| `prompt_text` | text not null | |
| `output_schema` | jsonb not null | JSON schema |
| `created_by` | uuid fk users nullable | |
| `created_at` | timestamptz not null | |

Constraints:

- unique `prompt_versions(prompt_id, version)`

#### `document_templates`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `key` | text unique not null | `reference`, `permanent`, `project_baseline` |
| `name` | text not null | |
| `active_version_id` | uuid nullable | |
| `created_at` | timestamptz not null | |
| `updated_at` | timestamptz not null | |

#### `document_template_versions`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | |
| `template_id` | uuid fk document_templates not null | |
| `version` | integer not null | |
| `body` | text not null | Markdown skeleton |
| `created_by` | uuid fk users nullable | |
| `created_at` | timestamptz not null | |

Constraints:

- unique `document_template_versions(template_id, version)`

## Recommended Migration Order

1. `users`, `auth_tokens`
2. `settings`
3. `sources`
4. `prompts`, `prompt_versions`
5. `ai_task_definitions`
6. `ai_tasks`
7. `approval_gates`
8. `gate_feedback`
9. `approval_gate_revisions`
10. add FK columns on `approval_gates` to revisions/tasks
11. `drafts`, `apply_plans`
12. `documents`, `document_edges`
13. `graph_chat_sessions`, `graph_chat_messages`, `graph_chat_runs`
14. `document_templates`, `document_template_versions`
15. seed user, AI provider settings, default prompts/templates/task definitions

The split around gates/revisions avoids circular FK friction in the first migration. Graph chat has a similar nullable cycle between assistant messages and runs; create `graph_chat_messages` before `graph_chat_runs`, then add nullable `graph_chat_messages.run_id` and `graph_chat_runs.assistant_message_id` FKs after both tables exist.

## Initial Seeds

| Seed | Value |
|---|---|
| User | `kknaks@medisolveai.com` |
| AI provider | `claude` |
| timeout | `300` |
| max turns | `3` |
| effort | `medium` |
| prompts | source summary, classification gate, documentation gate, graph chat |
| task definitions | `collect_source_summary`, `generate_classification_gate`, `regenerate_classification_gate`, `generate_documentation_gate`, `regenerate_documentation_gate`, `graph_rag_chat` |
| templates | `reference`, `permanent`, `project_baseline` (AXKG-SPEC-010 MVP scope, AXKG-DEC-005) |

## Open Items

- `documents.path` is workspace-root-relative. Product docs and permanent/concept docs can be indexed together, but Apply Executor writes only to configured allowlist paths.
- Write actual Alembic migration files.
- Decide whether Redis-backed task queue is needed before first implementation, or whether FastAPI background tasks are enough for MVP.
