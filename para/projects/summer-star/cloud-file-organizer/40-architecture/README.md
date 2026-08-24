# Architecture Index

규칙: `para/projects/project.md`

> 여러 spec/work가 공유하는 장기 구조를 관리한다. 단일 구현 메모가 아니라, 코드 스캐폴딩과 작업 분해의 기준이 되는 시스템/DB/배포 구조를 둔다.

최종 수정: 2026-07-08

## Scope

### In Scope

- FastAPI async backend 기본 구조
- Next.js + shadcn frontend 기본 구조
- PostgreSQL / SQLAlchemy / Alembic / Redis 구성
- Docker local/prod 실행 단위
- API layer dependency rule
- 비동기 worker와 open-kknaks 연동 경계

### Out Of Scope

- 실제 코드 구현
- migration 전문
- 운영 배포 절차 상세 runbook
- cloud vendor managed service 선택

## Architecture List

| ID | Title | Area | Status | File |
|---|---|---|---|---|
| ARCH-001 | System Architecture | system | draft | [system/system-001-system-architecture.md](system/system-001-system-architecture.md) |
| ARCH-002 | AI Queue State Tables | database | draft | [database/database-001-ai-queue-state.md](database/database-001-ai-queue-state.md) |
| ARCH-003 | Core Domain Tables | database | draft | [database/database-002-core-domain-tables.md](database/database-002-core-domain-tables.md) |

## Shared Constraints

| 항목 | 결정 |
|---|---|
| Backend | async FastAPI |
| Database | PostgreSQL |
| ORM / Migration | SQLAlchemy async, Alembic |
| Cache / Queue | Redis |
| Job state SoT | PostgreSQL `ai_queue_jobs` 계열 테이블 |
| Worker | backend worker process, open-kknaks task submit/consume boundary |
| Frontend | Next.js, shadcn/ui |
| Docker | `Dockerfile`, `Dockerfile.worker`, `docker-compose.local.yml`, `docker-compose.prod.yml` |
| Env | `.env.local`, `.env.prod` |
| API flow | `fe -> schema -> router -> dto -> service -> dto -> repo` |
| SQL rule | 상위 레이어 SQLAlchemy `stmt`/raw query 금지. query construction은 repo 전용 |

## Reading Order

| Area | Document |
|---|---|
| Product spec | [SPEC-001 User & RBAC](../20-spec/spec-001-user-rbac.md) |
| Product spec | [SPEC-003 Document Metadata Record](../20-spec/spec-003-document-metadata-record.md) |
| Product spec | [SPEC-004 Google Drive Connector & Sync](../20-spec/spec-004-google-drive-connector-sync.md) |
| Product spec | [SPEC-007 AI Classification Pipeline](../20-spec/spec-007-ai-classification-pipeline.md) |
| Architecture | [ARCH-001 System Architecture](system/system-001-system-architecture.md) |
| Architecture | [ARCH-003 Core Domain Tables](database/database-002-core-domain-tables.md) |
| Architecture | [ARCH-002 AI Queue State Tables](database/database-001-ai-queue-state.md) |

## Accepted Defaults

아래 항목은 권장값을 기본 아키텍처로 채택한다.

| 항목 | 기본값 | 상태 |
|---|---|---|
| Auth/session 방식 | backend JWT access token + refresh token cookie | accepted |
| API schema 소유권 | Pydantic v2 schema가 request/response 계약 소유 | accepted |
| Async job queue 방식 | Redis queue + worker process + PostgreSQL job state table | accepted |
| Observability | structured logging + request id + job id | accepted |
| Test baseline | backend unit/service/repo test + API contract test, frontend component/e2e smoke | accepted |
| Seed strategy | Alembic schema + 별도 seed command | accepted |
| Secret handling | `.env.local`은 로컬 전용, `.env.prod`는 git secret 대상 | accepted |
