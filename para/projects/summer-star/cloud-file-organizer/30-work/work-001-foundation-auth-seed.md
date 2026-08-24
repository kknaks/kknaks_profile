---
type: work
id: CFO-WORK-001
title: "기반: DB 마이그레이션 + Auth + User Seed"
status: done
product: cloud-file-organizer
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/work
  - status/done
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-001-user-rbac]]"
  works: []
  releases: []
  related: []
---

# 기반: DB 마이그레이션 + Auth + User Seed

ARCH-002/003 전체 테이블 마이그레이션, JWT 인증, Mediness user seed, RBAC 판정 core까지 — 이후 모든 WP가 딛고 서는 기반을 만든다. 조직도/문서 트리 CRUD·관리 화면은 만들지 않는다(WORK-002).

> 1 파일 = 1 work = **빌드 계획**. SPEC 본문은 복제하지 않고 ID/링크로 참조한다. Status Board / Spec Coverage는 `30-work/README.md`가 담당한다.

## Meta

- Baseline: BASE-001, BASE-002 (spec 경유)
- Covers spec: SPEC-001 (User & RBAC)
- Depends on work: 없음 (첫 착수 WP)
- Parallel work: 없음 — 이 WP가 끝나야 WORK-002/003이 뜬다
- Follow-up work: WORK-002 (조직도/문서 트리), WORK-003 (문서 record + Drive sync)
- External dependency: Mediness dev DB 접근(`ssh medi-me` → Lima `master` VM → k8s PostgreSQL, `mediness-dev`/`public.users` 26 rows). seed는 dump/export 파일 경유 가능 — 연동 방식은 착수 시 결정

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR | main `a6ac641` |
| Blocker | - |
| Next | WORK-002 착수 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | SPEC-001 범위 고정 | done |
| Design | kknaks | 로그인 화면(21-html/login-rbac.html 기준 — password 방식으로 시안 정정) | done |
| FE | kknaks | 로그인 화면 + auth client | done |
| BE | kknaks | migration, auth, seed CLI, RBAC core | done |
| QA | kknaks | AC 검증, seed 멱등 검증 | done |
| Ops | kknaks | env/secret, compose 기동 확인 | todo |

## Scope

포함:

- Alembic migration: ARCH-002 `ai_queue_jobs` + ARCH-003 전체 테이블(`users`, `organization_nodes`, `document_tree_nodes`, `document_types`, `documents`, `document_related_departments`, `document_path_histories`, `metadata_candidates`, `document_relations`, `relation_candidates`, `drive_sync_state`, `drive_sync_events`) — 제약/unique/index 포함
- 인증: JWT access token + refresh token httpOnly cookie (ARCH-001 Accepted Defaults). login/refresh/logout endpoint + FE 로그인 화면 배선
- Mediness users seed CLI: `source_user_id` 기준 멱등 upsert (SPEC-001 Source Seed 필드 매핑)
- 기본 조직도 노드 seed: 회사(`메디솔브`) + department 노드 — user `department_node_id` 매핑을 위해 이 WP에 포함 (DEC-004 기본 트리, seed `department` 분포 `ax/be/design/fe/hr/plan/qa/rnd` 기반)
- seed 시 이름 규칙으로 조직도 노드 매핑 시도, 실패분은 admin 보정 tool 범위(SPEC-001 Admin Behavior — v1 admin tool: 매핑 없는 user 목록 + node 지정 API)
- RBAC 판정 core service: read policy 평가(`ANY`/`ALL`/`PRESET`), Visibility Contract(`active=false`/`resigned_at`/`department_node_id is null` 제한), boolean vector는 판정 결과/log 전용
- admin role 판정 dependency (승인 게이트/관리 API 공용 guard)

제외:

- 조직도/문서 트리 CRUD·관리 화면 → WORK-002
- 문서 목록/탐색에 RBAC 적용 → WORK-006 (core 판정 함수만 여기서 제공)
- Drive OAuth connector → WORK-003 (login과 분리, env 주입 계약만 준수)
- Google social login (SPEC-001 Out of scope)

## Code Surface

- Repo / module: `gcs_demo` (backend 중심 + FE 로그인)
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `backend/app/models/` | SQLAlchemy model 전체 (ARCH-002/003) |
| `backend/app/db/migrations/versions/` | Alembic migration (autogenerate 후 제약/index 보정) |
| `backend/app/core/security.py` · `core/config.py` | JWT 발급/검증, env typed settings |
| `backend/app/api/deps.py` | current_user / admin guard dependency |
| `backend/app/api/routers/auth.py` | login / refresh / logout |
| `backend/app/schemas/` · `dtos/` | auth·user request/response 계약 |
| `backend/app/services/auth.py` · `services/rbac.py` | 인증, read policy 판정 core |
| `backend/app/repos/users.py` · `repos/organization.py` | user/org 노드 DB access |
| `backend/app/seeds/` | users seed CLI + 기본 조직도 seed (멱등) |
| `frontend/app/login/page.tsx` · `lib/auth/` · `lib/api/client.ts` | 로그인 화면 + 토큰/쿠키 처리 |

- Domain / schema note: **이 WP가 전체 schema migration의 SoT 착수점**이다. 실제 schema 전문은 코드/migration이 SoT (ARCH-002/003은 구조 기준). SQLAlchemy `stmt`/query construction은 `app/repos/` 전용 — router/service/worker에서 금지 (ARCH-001 §4).

## Domain / Schema

| Entity | 역할 |
|---|---|
| `users` | Mediness seed 기반 제품 user 원장. `source_user_id` unique 멱등 upsert |
| `organization_nodes` | 기본 seed(회사+부서)까지만 이 WP. CRUD는 WORK-002 |
| 나머지 ARCH-002/003 테이블 | migration으로 생성만. 데이터 흐름은 후속 WP |

- 상태 / invariant: SPEC-001 Visibility Contract가 판정 SSOT. boolean vector 컬럼 저장 금지 (DEC-016)
- Migration 필요 여부: **있음** — 이 WP의 본체
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 인증 endpoint 경로/쿠키 이름 확정 시 spec 구현 노트 환류

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-002~006 전체 | migration된 테이블 + `deps.py` auth/admin guard | 모든 WP가 이 위에서 작업 |
| WORK-006 | `services/rbac.py` read policy 판정 함수 | 문서 목록/검색/관련 문서 숨김 필터 |
| WORK-005 | admin guard + `users` 승인자 FK | 승인 게이트 접근 제어·`approved_by` |

## Internal Interface Contract

- `services/rbac.evaluate_read(user, doc_policy) -> ReadDecision(role_match, department_match, position_match, final_readable)` — 원장 저장 없이 판정/log 전용
- `api/deps.get_current_user()` / `require_admin()` — 후속 라우터 공용

## Execution

### Phase 1 — ARCH-002/003 전체 테이블 Alembic migration

- **Status**: DONE
- **설명**: 이후 WP가 테이블 부재로 막히지 않도록 도메인 전체 schema를 한 번에 내린다.
- **작업**:
  - [x] ARCH-003 도메인 테이블 + ARCH-002 `ai_queue_jobs` SQLAlchemy model 작성 (`backend/app/models/` 13개 테이블)
  - [x] Alembic migration 생성 — unique(`source_user_id`, `(source_provider, drive_file_id)`, `(source,target,type)` relation, ai job idempotency 등)·check(enum 축)·GIN index(path/read_departments) 포함
  - [x] `alembic upgrade head` / `downgrade -1` 왕복 확인
- **검증**:
  - [x] 빈 DB에서 upgrade head 성공, 13 테이블/제약 존재 (ARCH-003 §8 AC)
  - [x] `metadata_candidates` 부분 unique(문서당 pending 1개), `document_path_histories` append-only 전제 구조 확인
- **완료 증거**: migration `58b8efe84ede_arch_002_003_core_domain_tables.py`. `upgrade head`→13 테이블·GIN 3종·partial unique 1종 생성, `downgrade`→0 테이블, 재`upgrade` 성공(왕복 검증). pytest `test_migration.py`(5)에서 provider/file unique·pending 1개·enum check·GIN/partial index 존재를 검증. enum 축은 v1에서 text+CHECK로 저장(enum table 분리는 후속).

### Phase 2 — JWT 인증 (access + refresh cookie) + 로그인 화면

- **Status**: DONE
- **설명**: FE↔BE 인증 경계를 고정한다. refresh token은 httpOnly secure cookie (ARCH-001 Accepted Defaults).
- **작업**:
  - [x] `POST /auth/login`·`POST /auth/refresh`·`POST /auth/logout`·`GET /auth/me` + JWT 발급/검증 (`JWT_SECRET`, TTL env). access는 body, refresh는 httpOnly cookie(`refresh_token`, path=/auth)
  - [x] `get_current_user`/`require_admin` dependency (`api/deps.py`), 비활성(`active=false`)/퇴사(`resigned_at`) 사용자 로그인·세션 차단
  - [x] FE 로그인 화면(`app/login`) — email+password 단일 로그인으로 재작업(tsc 통과), `lib/auth/session.ts` 계약 확정, 시안(login-rbac.html)도 password 방식으로 정정
- **검증**:
  - [x] seed 계정 로그인 → access 발급 + refresh cookie 세팅, refresh로 회전 동작
  - [x] `active=false` 계정 로그인 거부(403 ACCOUNT_DISABLED)
- **완료 증거**: `core/security.py`(bcrypt+PyJWT), `services/auth.py`, `api/routers/auth.py`, `api/deps.py`. pytest `test_auth.py`(8): 로그인 성공/오류 401/비활성 403/`/auth/me` bearer/refresh 회전/logout. **FE 계약**: 쿠키 `refresh_token`(httpOnly, path=/auth), 로그인 응답 `{access_token, token_type:"bearer", expires_in, user{...}}`, 데모 credential=env `DEMO_USER_PASSWORD`(기본 `cfo-demo-2026`).

### Phase 3 — Mediness user seed CLI + 조직도 매핑 보정

- **Status**: DONE
- **설명**: `mediness.public.users` 26 rows를 제품 user로 멱등 반영하고, 권한 판정 기준인 조직도 노드 매핑을 만든다.
- **작업**:
  - [x] 기본 조직도 seed: 회사 root(`메디솔브`) + department 노드 8종 (seed `department` 분포 ax/be/design/fe/hr/plan/qa/rnd)
  - [x] users seed CLI (`python -m app.seeds`): SPEC-001 필드 매핑, `source_user_id` 기준 멱등 upsert, 재실행 안전, prod 가드(`--force`)
  - [x] 이름 규칙으로 `department_node_id` 매핑 시도(18/26 매핑), 실패분 조회 + admin 보정 API(`GET /admin/users/unmapped`, `POST /admin/users/{id}/department`)
- **검증**:
  - [x] seed 2회 실행 → row 수 불변(26)·값 갱신 (SPEC-001 AC 멱등). run1 created=26, run2 created=0/updated=26
  - [x] 매핑 실패 user 8명이 보정 목록에 나오고 보정 후 `department_node_id` 반영(목록 8→7)
- **완료 증거**: `app/seeds/`(organization.py/users.py/__main__.py) + `app/seeds/data/mediness_users.json`(dump에서 **안전 필드만** 추출, password/전화/생일 등 credential 제외). `repos/users.py`·`repos/organization.py`·`services/users.py`·`api/routers/admin_users.py`. pytest `test_seed.py`(5)+`test_admin_users.py`(4). 데모 password는 env 공통값만 부여(원본 Mediness credential 미반영·미로그).

### Phase 4 — RBAC 판정 core

- **Status**: DONE
- **설명**: SPEC-001 RBAC Rules/Visibility Contract를 서비스 함수로 고정한다. 화면 적용은 후속 WP.
- **작업**:
  - [x] `evaluate_read(user, policy) -> ReadDecision`: `ANY`/`ALL` 평가, `PRESET`은 풀어 저장된 read policy 필드를 ANY(v1 기본)로 평가, admin 전체 허용
  - [x] `read_departments` 노드 id 매칭 — department 노드면 하위 팀 포함(하위 팀 user도 department_node_id 보유), team 노드면 해당 팀
  - [x] Visibility 판정: `active=false`/`resigned_at`/`department_node_id null` 제한
- **검증**:
  - [x] SPEC-001 AC 항목별 unit test (admin 전체 읽기·민감 문서 포함, PRESET/ANY/ALL 판정, 비활성·퇴사·미매핑 숨김)
  - [x] boolean vector는 `ReadDecision`(판정 결과/log)로만 반환, 어떤 원장 컬럼에도 저장 안 함(DEC-016)
- **완료 증거**: `services/rbac.py`·`dtos/rbac.py`(ReadPolicy/ReadDecision). pytest `test_rbac.py`(10, DB-free). 원장 테이블에 `role_match` 등 컬럼 없음(모델 검토).

## Pre-deploy Check

- [x] `.env.local`/`.env.prod`에 `JWT_SECRET` 등 신규 env 반영, 평문 commit 없음 (.env.example만 commit 대상, .env.local은 gitignore)
- [x] Mediness 원본 DB credential이 코드/문서/log에 남지 않음 (dump 안전 필드만 추출, seed log에 password 미출력)
- [x] seed CLI가 prod에서 임의 실행되지 않도록 실행 조건 명시 (APP_ENV=prod면 `--force` 필요)

## Rollback

- migration: `alembic downgrade` 절차 (base까지 왕복 검증된 revision 단위)
- auth: 라우터 미등록으로 비활성화 가능 — 기존 화면 없음이라 영향 범위 없음
- seed: 멱등 upsert이므로 재실행으로 복원. 삭제 rollback은 하지 않음(원장 보존)

## Done Criteria

- [x] 모든 Phase가 `DONE`이다 (FE 로그인 화면 포함 — password 방식 재작업 완료).
- [x] SPEC-001 Acceptance Criteria가 Phase 검증(pytest 33)에 반영됐다.
- [x] 필요한 테스트/검증이 끝났다 — pytest 33 passed, alembic base 왕복, seed 2회 멱등(26/26, 매핑 18), 라이브 스모크(login→me→refresh→logout 204, 오답 401) 독립 재검증.
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- ~~데모 로그인 credential 정책 미정~~ → **확정안(BE)**: env `DEMO_USER_PASSWORD` 공통 데모 password를 seed user 전원에 부여(원본 Mediness credential 미반영). **spec-001 환류는 admin 확인 대기** — 확인 후 SPEC-001 Login Boundary에 구현 노트 반영 필요.
- ~~Mediness DB 접근 방식~~ → **확정**: dump 파일(`mediness_2026-07-03.dump`)에서 **안전 필드만** repo 내 seed JSON으로 추출. credential 컬럼(password/전화/생일/카드/slack)은 추출 제외. 임시 복원 DB는 추출 후 삭제.

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Architecture: ARCH-001 §4 layer rule, ARCH-002/003 (테이블 구조 기준)
