# 40-architecture

AX Knowledge Graph의 구현 아키텍처는 **Next.js + FastAPI + PostgreSQL + Markdown document root + open-kknaks**를 기본 스택으로 잡는다. Redis는 durable state가 아니라 필요 시 비동기 작업 큐/락/캐시 용도로 붙인다.

모노레포는 현재 `kknaks_profile` 루트 구조를 따른다. 즉 `agent.md`, `.agent/`, `templates/`, `rules/`, `context/`, `inbox/`, `permanent/`, `reference/`, `products/` 같은 지식/에이전트 운영 디렉터리를 루트에 유지하고, 런타임 앱만 `apps/`와 `packages/` 아래에 둔다.

| Area | Path |
|---|---|
| System | `system/README.md` — monorepo layout, service boundaries, runtime flows |
| Database | `database/README.md` — PostgreSQL schema, indexes, payload boundaries |
| Deploy | `deploy/README.md` — local/deploy runtime topology and document mount |

## Stack Summary

| Layer | Choice |
|---|---|
| Frontend | Next.js / React / TypeScript |
| Backend | FastAPI / Pydantic / SQLAlchemy / Alembic |
| Operational DB | PostgreSQL |
| Optional queue/cache | Redis |
| AI execution | open-kknaks provider task API (`claude` default, `codex` supported) |
| Final document SoT | Markdown files under configured document root |
