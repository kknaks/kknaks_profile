---
type: decision
id: KDEV-DEC-009
title: "애플리케이션 DB화 토대 + 관리자 인증 방식"
status: accepted
product: kknaks-dev
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-002-app-db-and-admin|KDEV-BL-002]]"
  decisions: []
  specs:
    - "[[spec-006-admin-auth|KDEV-SPEC-006]]"
  works: []
  releases: []
  related:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
up:
  - jwt
  - cookie
  - async-io
  - database-migration
---

# 애플리케이션 DB화 토대 + 관리자 인증 방식 (ADR-009)

md-only 운영에서 관계형 DB 도입을 시작한다. 이 결정은 (1) DB 경계, (2) DB 스택, (3) 관리자 인증 방식 세 가지를 확정한다.

> **개정 (2026-07-27, v2)**: DB 접근을 **동기 → async(SQLAlchemy async 세션)로 전환**. 최초엔 기존 `def` 라우터와의 정합을 위해 동기로 결정·구현했고, 로그인 MVP가 동기로 동작하는 것을 확인한 뒤 owner 판단으로 async로 전환했다. 드라이버(psycopg3)·URL·Alembic(동기 CLI 유지)은 그대로다. D2·Options·Rationale에 반영. 상세는 [[work-011-admin-auth-mvp|KDEV-WORK-011]].

## Context

- 관련 baseline: [[baseline-002-app-db-and-admin|KDEV-BL-002]]
- 백엔드는 FastAPI in-memory persona 서버(동기 `def` 라우터). 관계형 DB·사용자 세션 없음.
- 지식그래프는 파일(frontmatter) SoT 전제 위에 검증 게이트가 서 있다([[baseline-001-repo-knowledge-graph|KDEV-BL-001]]).
- 운영 환경: 홈서버 docker + NPM(reverse proxy), 단일 워커 FastAPI. 프론트는 Vercel(`profile.kknaks.cloud`), 백은 `profile-api.kknaks.cloud`.

## Decision

### D1. DB 경계 — 무엇을 DB로, 무엇을 파일로

- **애플리케이션/운영 데이터**(사용자·세션 등 동적 상태)는 관계형 DB로 옮긴다. 첫 대상은 `users`.
- **지식그래프**(persona·reference·permanent md, frontmatter)는 **파일 SoT를 유지**한다. 검증 게이트(L1~L6)·옵시디언 그래프·enrich 잡은 변경 없음.
- 두 저장소는 공존한다. 콘텐츠의 DB 이관은 별도 baseline/decision에서 다룬다(이번 범위 밖).

### D2. DB 스택

| 항목 | 결정 |
|---|---|
| 엔진 | **PostgreSQL** (docker-compose 서비스로 추가, Redis처럼 컨테이너 관리) |
| ORM | **SQLAlchemy 2.0 async** (`create_async_engine` + `AsyncSession`; v2 개정 — 최초 동기에서 전환) |
| 마이그레이션 | **Alembic** (스키마 버전 관리, 첫 리비전 = `users`; 마이그레이션 CLI 는 동기 엔진 유지) |
| 드라이버 | psycopg 3 (`postgresql+psycopg://` — sync/async 공용, 전환에도 드라이버 교체 불필요) |

### D3. 관리자 인증 방식

- **단일 관리자**를 `.env`(`ADMIN_USERNAME`/`ADMIN_PASSWORD`)로 **시드**한다. 부팅 시 `users`에 멱등 upsert, 비밀번호는 bcrypt 해시로 저장(평문 저장 안 함).
- 세션은 **httpOnly 쿠키에 담은 JWT(HS256)**. FE는 토큰을 직접 만지지 않는다(XSS 노출 최소화).
- 쿠키 속성은 환경별: 로컬 dev는 host-only·`Secure=0`, 운영은 `Domain=.kknaks.cloud`·`Secure=1`·`SameSite=Lax`(프론트·백이 같은 site라 Lax로 전송됨).
- 회원가입·다중 유저·역할(role) 세분화·비밀번호 재설정은 범위 밖. `role` 컬럼은 두되 값은 `admin` 고정으로 시작.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[jwt]] — 세션을 **JWT(HS256)** 로 담되 프론트가 토큰을 직접 만지지 않게 했다 — 토큰이 신원을 나르는 방식과 그 노출 위험을 함께 다룬 결정이다
- [[cookie]] — 그 JWT 를 **httpOnly 쿠키**에 넣고 환경별로 `Domain`·`Secure`·`SameSite` 를 나눴다. 「스크립트가 못 읽게 한다」가 XSS 노출을 줄이는 근거다
- [[async-io]] — DB 접근을 **동기에서 async 세션으로 전환**한 개정. 기다리는 동안 워커를 놓아 주는 것이 요청 처리량을 정한다
- [[database-migration]] — Alembic 으로 스키마 변경을 버전으로 남긴다 — 손으로 DDL 을 치지 않고 되돌릴 수 있게 하는 장치다

## Options

### DB 엔진

| Option | Pros | Cons | Notes |
|---|---|---|---|
| **PostgreSQL** | 운영급, 콘텐츠 DB화까지 확장 유리, docker로 관리 | 컨테이너 1개 추가 운영 | **채택** |
| SQLite | 인프라 0, 파일 1개 | 동적 콘텐츠 확장 시 재이관 가능성 | 반려 |

### ORM / 마이그레이션

| Option | Pros | Cons | Notes |
|---|---|---|---|
| **async SQLAlchemy 2.0 + Alembic** | 비동기 I/O, 향후 콘텐츠 DB화까지 async 일관 | auth 외 기존 라우터는 여전히 동기(점진 전환) | **채택 (v2)** |
| SQLAlchemy 2.0 + Alembic (동기) | FastAPI 표준, 기존 동기 라우터와 정합 | 확장 시 async 재전환 | 최초 채택 → v2 에서 async 로 전환 |
| SQLModel + Alembic | Pydantic 통합, 모델=스키마 | SQLAlchemy 위 래퍼 층 | 반려 |

### 인증 방식

| Option | Pros | Cons | Notes |
|---|---|---|---|
| **쿠키 JWT + .env 시드** | httpOnly로 XSS 안전, stateless, 서브도메인 공유 | 즉시 무효화(로그아웃) 어려움 | **채택** |
| 서버 세션(Redis 저장) | 즉시 무효화 | 상태 저장·Redis 의존 | 후속 확장 여지 |
| Authorization 헤더 Bearer | 표준 API 인증 | FE가 토큰 저장(XSS 노출) | 반려 |

## Rationale

- Postgres는 이후 콘텐츠·노트까지 DB화할 때 재이관 없이 확장된다. 홈서버가 이미 docker라 Redis와 동형으로 운영.
- async SQLAlchemy(psycopg3 async)로 가면 향후 콘텐츠 DB화까지 비동기 I/O 로 일관된다. auth 만 DB 를 쓰는 지금이 전환 비용이 가장 작아, 동기 검증 직후 async 로 넘겼다. Alembic 은 마이그레이션 CLI 라 event loop 이득이 없어 동기 유지. 기존 콘텐츠 라우터(`def`)는 DB 무관(메모리 dict)이라 async 세션과 무충돌.
- httpOnly 쿠키 JWT는 FE가 토큰을 저장하지 않아 XSS에 강하고, 프론트/백이 같은 site(`kknaks.cloud`)라 `SameSite=Lax`로 자연히 전송된다.
- 지식그래프를 DB로 끌어오지 않는 이유: 검증 게이트·옵시디언 그래프·git 기반 SoT가 파일 전제 위에 서 있어, 이관은 이득 없이 리스크만 크다.

## Scope

- In: DB 경계 정의, DB 스택 선택, 관리자 인증 방식.
- Out: DB 스키마 전문·마이그레이션 순서·라우트/컴포넌트 파일(work), admin 실제 관리 기능(후속 spec), 콘텐츠 DB 이관.
- 영향을 받는 spec 후보: 관리자 인증 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | JWT 즉시 무효화(로그아웃/탈취 대응)가 필요해지면 서버 세션(Redis)로 승격할지 | kknaks | 필요 시 |
| OQ-2 | 다중 유저·역할 세분화 도입 시점 | kknaks | 후속 baseline |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 관리자 인증 spec | create | 톱니 진입 · 로그인/세션/로그아웃 · admin 목 화면 외부 계약 |
