---
type: work
id: AXKG-WORK-001
title: "WP0: 모노레포 scaffold와 실행 골격"
status: in-progress
product: ax-knowledge-graph
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 10
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/in-progress
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-002-markdown-sot-postgres-storage|AXKG-DEC-002]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works: []
  releases: []
  related: []
---

# WP0: 모노레포 scaffold와 실행 골격

작업 레포에 실행 가능한 기반을 만든다: 디렉토리 구조 확정, DB 마이그레이션/seed, 로그인, AI 실행 골격. 도메인 기능(intake/그래프/게이트/chat/설정)은 이 WP가 깐 골격 위에 WP1~5(work-002~006, 후속 생성)로 나눠 붙인다.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-008(로그인), AXKG-SPEC-011(실행 골격 — task definition 해석→조립→fallback 프레임까지. 스테이지별 구현은 각 도메인 WP)
- Depends on work: 없음
- Parallel work: 없음
- Follow-up work: WP1 Source Intake(SPEC-003/012/011①), WP2 문서·그래프 코어(SPEC-005), WP3 승인 게이트(SPEC-001/002/004/011②③), WP4 Graph Chat(SPEC-006/011④), WP5 설정(SPEC-007/009/010)
- External dependency: open-kknaks API endpoint

## WP Plan (전체 지도)

| WP | Work | 범위 | Covers | 선행 |
|---|---|---|---|---|
| WP0 | AXKG-WORK-001 (이 문서) | scaffold + migration + auth + 실행 골격 | SPEC-008, 011(골격) | — |
| WP1 | work-002 (예정) | Source Inbox + 수집 adapter + 요약 | SPEC-003, 012, 011① | WP0 |
| WP2 | work-003 (예정) | markdown parser + documents/edges 캐시 + rebuild + retriever + 그래프 뷰 | SPEC-005 | WP0 |
| WP3 | work-004 (예정) | 분류②·문서화③ 게이트 + Apply Executor + 재분류 재오픈 | SPEC-001, 002, 004, 011②③ | WP1+WP2 |
| WP4 | work-005 (예정) | Graph RAG chat 세션/run polling | SPEC-006, 011④ | WP2 |
| WP5 | work-006 (예정) | AI Provider·Prompts·Templates 설정 | SPEC-007, 009, 010 | WP0 |

WP2(그래프 코어)가 WP3(게이트)보다 선행이다 — 문서화 게이트의 연결 후보 컨텍스트(retriever + documents index)와 승인 apply의 엣지 rebuild가 WP2 산출물을 전제한다. WP4/WP5는 병렬 가능.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | in-progress |
| Progress | 10% |
| Branch/PR |  |
| Blocker | 없음 (Redis는 FastAPI background task로 시작, 필요 시 도입 — Open Issues) |
| Next | Phase 2 디렉토리 구조 scaffold → 구조 확정 후 40-architecture 역반영 + 도메인 WP(work-002~006) 생성 |

## Scope

포함:

- 모노레포 디렉토리 구조 scaffold (`apps/web` Next.js, `apps/api` FastAPI, `packages/contracts`)
- 구조 확정 결과를 `40-architecture/system/README.md` monorepo layout에 역반영
- Alembic migration (database README 권장 순서 15단계) + 초기 seed (user, ai_provider 설정, prompts, templates, task definitions)
- 간단한 토큰 로그인 (SPEC-008): seed user, 토큰 발급/검증, 보호 라우트 미들웨어, 로그인 페이지
- AI 실행 골격 (SPEC-011): `ai_task_definitions` 해석 → context builder 조립(template→prompt→output_schema) → open-kknaks 위임 → 출력 파싱/검증 → 실패 매핑 → 코드 fallback — **프레임과 인터페이스까지만**, 스테이지별 context builder 내용은 각 도메인 WP
- 로컬 실행 환경 (docker compose 또는 dev server 조합, workspace bind mount)

제외:

- 도메인 기능 전부 (WP1~5): intake/수집/요약, parser/그래프, 게이트/executor, chat, 설정 UI
- 배포 자동화 (deploy README의 docker compose 초안은 로컬 실행 수준까지만)
- 협업 권한

## Code Surface

- Repo / module: `/Users/kknaks/git/toy_pr2/ax-graph`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `apps/web/` | Next.js app (로그인 페이지 + 앱 셸) |
| `apps/api/axkg/` | FastAPI app (core/security, domain 골격, workers 골격) |
| `apps/api/alembic/` | PostgreSQL migration + seed |
| `packages/contracts/` | OpenAPI/JSON schema 공유 계약 |
| `40-architecture/system/README.md` | 구조 확정 후 layout 역반영 (문서) |

- Domain / schema note: PostgreSQL 운영 저장소 + Markdown SoT(workspace bind mount) + open-kknaks AI task 실행. Redis는 필요 시 도입.

## Domain / Schema

| Entity | 역할 | 이 WP에서 |
|---|---|---|
| `users` / `auth_tokens` | 로그인 (SPEC-008) | 전체 구현 |
| `settings` / `prompts` / `prompt_versions` / `document_templates` / `document_template_versions` | 실행 골격의 조립 원천 | 테이블 + seed까지 (편집 UI는 WP5) |
| `ai_task_definitions` / `ai_tasks` | 실행 골격 (SPEC-011) | 전체 구현 (해석·스냅샷·fallback) |
| `sources`, `approval_gates`+revisions, `gate_feedback`, `drafts`, `apply_plans`, `documents`, `document_edges`, `graph_chat_*` | 도메인 테이블 | migration까지만 (로직은 WP1~4) |

- 상태 / invariant: 마이그레이션은 database README의 권장 순서를 따른다. 실패한 `ai_tasks`는 불변, 재시도는 `retry_of_task_id` 새 row.
- Migration 필요 여부: 필요. `40-architecture/database/README.md` 전체를 Alembic으로 전환.
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 구조 확정 시 monorepo layout 차이를 40-architecture에 역반영.

## Execution

### Phase 1 — 구현 stack 결정

- **Status**: DONE
- **설명**: MVP를 어떤 프레임워크와 저장소로 만들지 결정한다.
- **작업**:
  - [x] UI/BE 통합 방식 후보 정리
  - [x] 파일 기반/SQLite/그래프 DB 후보 비교
  - [x] architecture 문서 작성
- **검증**:
  - [x] 선택된 stack으로 AXKG-SPEC-001~012를 구현할 수 있다.
- **완료 증거**: `40-architecture/system/README.md`, `40-architecture/database/README.md`

### Phase 2 — 디렉토리 구조 scaffold

- **Status**: TODO
- **설명**: 모노레포 구조를 실제로 깔고, 확정된 구조를 아키텍처 문서에 역반영한다.
- **작업**:
  - [ ] `apps/web`(Next.js), `apps/api`(FastAPI), `packages/contracts` 생성
  - [ ] FastAPI 모듈 골격 생성 (api/routes, core, domain, workers, integrations, storage)
  - [ ] 로컬 실행 환경 구성 (dev server + PostgreSQL + workspace bind mount)
  - [ ] 확정 구조를 `40-architecture/system/README.md` monorepo layout에 역반영
- **검증**:
  - [ ] 로컬에서 web/api가 뜨고 health check가 응답한다.
  - [ ] 문서의 layout과 실제 트리가 일치한다.
- **완료 증거**: 미작성

### Phase 3 — DB 마이그레이션과 seed

- **Status**: TODO
- **설명**: database README를 Alembic migration으로 전환하고 초기 seed를 넣는다.
- **작업**:
  - [ ] 권장 순서 15단계 migration 작성
  - [ ] seed: user(`kknaks@medisolveai.com`), ai_provider 설정, prompts 4종, templates 3종(`reference`/`permanent`/`project_baseline`), task definitions 6종
- **검증**:
  - [ ] 빈 DB에서 migration + seed가 한 번에 통과한다.
  - [ ] enum/제약이 database README와 일치한다.
- **완료 증거**: 미작성

### Phase 4 — 로그인 (SPEC-008)

- **Status**: TODO
- **설명**: seed user 기반 토큰 로그인과 보호 라우트를 구현한다.
- **작업**:
  - [ ] `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`
  - [ ] token hash 저장 + TTL + Bearer 검증 미들웨어
  - [ ] 로그인 페이지 + localStorage 저장 + 보호 라우트 리다이렉트
- **검증**:
  - [ ] SPEC-008 Acceptance Criteria 통과.
- **완료 증거**: 미작성

### Phase 5 — AI 실행 골격 (SPEC-011)

- **Status**: TODO
- **설명**: 4스테이지 공통 실행 경로의 프레임을 만든다. 스테이지별 context builder 내용은 도메인 WP가 채운다.
- **작업**:
  - [ ] `ai_task_definitions` 해석 → provider/options 해석(SPEC-007 규칙) → `ai_tasks` 생성·스냅샷
  - [ ] context builder 인터페이스 + 3자 조립(template→prompt→output_schema[JSON Schema])
  - [ ] open-kknaks client (task 생성/폴링, session id 저장)
  - [ ] 출력 JSON 파싱 + output_schema 검증 + 실패 매핑(`OUTPUT_PARSE_FAILED`/`OUTPUT_SCHEMA_MISMATCH`)
  - [ ] 활성 프롬프트/템플릿 로드 실패 시 코드 fallback + 관찰 기록
  - [ ] 재시도 체인(`retry_of_task_id`)
- **검증**:
  - [ ] 더미 handler로 해석→조립→실행→스냅샷 경로가 end-to-end로 돈다.
  - [ ] SPEC-011 Acceptance Criteria 중 골격 항목(스냅샷, 검증 실패 미소비, fallback) 통과.
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] AI provider credential이 클라이언트에 노출되지 않음
- [ ] auth token은 hash로만 저장됨
- [ ] Apply Executor 도입 전이므로 이 WP에서 workspace 쓰기 경로 없음

## Rollback

- 앱 scaffold 변경은 작업 레포 커밋 단위로 revert한다.
- 부모 제품 문서 변경은 별도 커밋으로 분리해 revert 가능하게 유지한다.

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] 확정 디렉토리 구조가 40-architecture에 역반영됐다.
- [ ] 도메인 WP(work-002~006)가 확정 구조 기준으로 생성됐다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- Redis 도입 시점: FastAPI background task로 시작하고, out-of-process worker가 필요해지는 시점(WP1 요약 큐 or WP3 apply lock)에 재검토.
