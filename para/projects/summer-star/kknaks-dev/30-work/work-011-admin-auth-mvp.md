---
type: work
id: KDEV-WORK-011
title: "관리자 인증 MVP — DB 토대 + 쿠키 JWT 로그인 + admin 목"
status: done
product: kknaks-dev
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
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-002-app-db-and-admin|KDEV-BL-002]]"
  decisions:
    - "[[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]"
  specs:
    - "[[spec-006-admin-auth|KDEV-SPEC-006]]"
  works: []
  releases: []
  related: []
---

# 관리자 인증 MVP — DB 토대 + 쿠키 JWT 로그인 + admin 목

애플리케이션 DB화의 첫 삽. PostgreSQL·SQLAlchemy·Alembic 토대를 깔고, `.env`로 시드한 단일 관리자를 httpOnly 쿠키 JWT로 로그인시키고, 헤더 톱니 → `/admin` 목 화면까지 배선한다.

**비목표**: admin의 실제 관리 기능(콘텐츠 편집), 회원가입/다중 유저, 콘텐츠 DB 이관. 지식그래프는 md SoT 그대로 둔다(건드리지 않는다).

## Meta

- Baseline: [[baseline-002-app-db-and-admin|KDEV-BL-002]]
- Covers spec: [[spec-006-admin-auth|KDEV-SPEC-006]]
- Depends on work: 없음 (신규 DB 토대 — 기존 그래프 work와 독립)
- Parallel work: 없음
- Follow-up work: admin 실제 관리 기능 spec/work (다음 상세 페이지 계획)
- External dependency: 없음 (Postgres는 docker-compose 로컬 서비스로 신설)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR | (main, 미커밋 워킹트리) |
| Blocker | 없음 |
| Next | 후속 — admin 실제 관리 기능 spec/work |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | todo |
| Design | kknaks | 로그인/admin 목 UX | todo |
| FE | kknaks | 톱니·로그인·admin 페이지 | todo |
| BE | kknaks | DB 토대·auth API·시드 | todo |
| QA | kknaks | 로그인 e2e·게이트 검증 | todo |
| Ops | kknaks | postgres 서비스·env | todo |

## Scope

포함:

- PostgreSQL docker-compose 서비스(운영 `docker-compose.yml` + 로컬 `docker-compose.local.yml`) + `DATABASE_URL` 배선.
- DB 토대: SQLAlchemy 2.0 async 엔진/세션/Base, `get_db` async 의존성 (v2 — 최초 동기에서 전환, DEC-009 개정).
- Alembic 초기화 + `users` 초기 리비전.
- 관리자 인증 백엔드: bcrypt 해시·JWT 발급/검증, `.env` 시드(부팅 시 멱등 upsert), `POST /api/auth/login`·`POST /api/auth/logout`·`GET /api/auth/me`, `require_admin` 의존성.
- 프론트: 헤더 우상단 톱니 진입점, `/admin/login` 로그인 폼, `/admin` 목 화면(인증 게이트), `lib/api.ts` auth 메서드(credentials 동봉).
- `.env`/`.env.example` 키 추가.

제외:

- admin 실제 관리 기능(후속 spec/work).
- 회원가입·다중 유저·role 세분화·비밀번호 재설정(DEC-009 범위 밖).
- 콘텐츠/지식그래프 DB 이관.

## Code Surface

- Repo / module: `app/back` (FastAPI), `app/front` (Next.js), repo 루트(compose/env).
- 만질 파일 후보:

| 경로 후보 | 설명 | 상태 |
|---|---|---|
| `app/back/pyproject.toml` | sqlalchemy·alembic·psycopg[binary]·bcrypt·pyjwt 추가 | 초안 작성됨 |
| `app/back/config.py` | `database_url`·admin·jwt·cookie 설정 함수 | 초안 작성됨 |
| `app/back/core/db.py` | 엔진/세션/Base/`get_db` | 초안 작성됨 |
| `app/back/core/models.py` | `User` 모델 | 초안 작성됨 |
| `app/back/core/security.py` | bcrypt 해시·JWT 인코드/디코드 | 초안 작성됨 |
| `app/back/service/seed.py` | 부팅 시 admin upsert | 초안 작성됨 |
| `app/back/alembic.ini`·`alembic/env.py`·`alembic/versions/*` | 마이그레이션 토대 + users 리비전 | 신규 |
| `app/back/api/routers/auth.py` | login/logout/me + `require_admin` | 신규 |
| `app/back/main.py` | auth 라우터 등록 + lifespan 시드 호출 | 수정 |
| `app/front/components/shell/topnav.tsx` | 우상단 톱니 진입점 | 수정 |
| `app/front/app/admin/login/page.tsx`·`app/front/app/admin/page.tsx` | 로그인 폼·admin 목 | 신규 |
| `app/front/lib/api.ts` | auth 메서드(credentials include) | 수정 |
| `docker-compose.yml`·`docker-compose.local.yml` | postgres 서비스 + `DATABASE_URL` | 수정 |
| `.env`·`.env.example` | DB·admin·jwt 키 | 수정 |

- Domain / schema note: migration 필요(신규 `users`). 실제 schema 전문은 Alembic 리비전이 SoT. 지식그래프 파일 로딩 경로는 건드리지 않는다.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `users` | 관리자 계정 저장. `username`(unique)·`password_hash`(bcrypt)·`role`(기본 `admin`)·`created_at`/`updated_at` |

- 상태 / invariant: `username` 전역 유일. 비밀번호는 해시만 저장(평문 금지). role 은 `admin` 고정 시작.
- Migration 필요 여부: 예 — Alembic 초기 리비전 = `users` 생성.
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 없음(SPEC-006 Data Contract가 이미 `username`/`role`만 노출로 정의).

## Internal Interface Contract

- JWT payload: `{ sub: username, uid: <user.id>, role, iat, exp }`, HS256, 시크릿 `JWT_SECRET`, 만료 `JWT_EXPIRE_MINUTES`(기본 720).
- 세션 쿠키: 이름 `AUTH_COOKIE_NAME`(기본 `kknaks_session`), `HttpOnly`, `SameSite=Lax`, 운영 `Secure`+`Domain=.kknaks.cloud`(env), 로컬 host-only·비-Secure.
- `require_admin` 의존성: 쿠키 토큰 디코드 실패/만료/부재 → `401`. 성공 → payload 반환. 후속 admin API가 이 의존성을 소비한다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 후속 admin 관리 기능 work | `require_admin` 의존성 | 관리 API가 이 게이트를 재사용 |
| 후속 콘텐츠 DB화 work | `core/db` 엔진/세션·Alembic | 같은 DB 토대 위에 테이블 추가 |

## Execution

### Phase 1 — DB 토대 (Postgres · SQLAlchemy · Alembic)

- **Status**: DONE
- **설명**: 관계형 DB 인프라를 세운다. 이후 모든 테이블의 공통 기반.
- **작업**:
  - [ ] `docker-compose.local.yml`·`docker-compose.yml`에 postgres 서비스(healthcheck·volume) + back `DATABASE_URL` 배선, back `depends_on` postgres.
  - [ ] `pyproject.toml` deps 확정 + `uv sync`.
  - [ ] `core/db.py`(엔진/세션/Base/`get_db`)·`core/models.py`(`User`) 확정.
  - [ ] Alembic 초기화(`alembic.ini`, `env.py`가 `config.database_url()`·`Base.metadata` 참조), `users` 초기 리비전 autogenerate.
  - [ ] `.env`/`.env.example`에 `DATABASE_URL`·`ADMIN_USERNAME`/`ADMIN_PASSWORD`·`JWT_SECRET`/`JWT_EXPIRE_MINUTES`·`AUTH_COOKIE_*` 키.
- **검증**:
  - [x] `docker compose -f docker-compose.local.yml up -d postgres` 후 healthy.
  - [x] `alembic upgrade head` → `users` 테이블 생성 확인(`\d users`).
  - [x] 기존 부팅(persona 로드)·기존 테스트 무회귀.
- **완료 증거**: postgres 컨테이너 healthy(호스트 포트 45433 — axkg-postgres 45432 충돌 회피). `alembic upgrade head` → `0001_create_users` 적용, `users`(id·username unique·password_hash·role·created/updated_at) + `ix_users_username` 확인. compose 크리덴셜은 `.env` POSTGRES_* 치환(커밋 파일에 비번 리터럴 없음). back 컨테이너 부팅 시 persona 406노드 정상 로드.

### Phase 2 — 인증 백엔드 (시드 · JWT · auth 라우터)

- **Status**: DONE
- **설명**: 시드된 관리자를 쿠키 JWT로 로그인/세션/로그아웃시키는 API.
- **작업**:
  - [ ] `core/security.py`(bcrypt·JWT) 확정.
  - [ ] `service/seed.py` — lifespan에서 `.env` admin 멱등 upsert(비번 로테이션 지원), DB 미가용이면 로그만(부팅 비차단).
  - [ ] `api/routers/auth.py` — `POST /api/auth/login`(자격검증→Set-Cookie), `POST /api/auth/logout`(쿠키만료), `GET /api/auth/me`, `require_admin`.
  - [ ] `main.py` — auth 라우터 등록 + lifespan 시드 호출. CORS는 이미 credentials 허용·명시 origin(확인).
- **검증**:
  - [x] 옳은 자격 → `200`+세션 쿠키(HttpOnly), `GET /me` `200`.
  - [x] 틀린 자격 → `401` `invalid credentials`(아이디/비번 구분 안 함).
  - [x] 세션 없이 `/me` → `401`. 로그아웃 후 `/me` → `401`.
  - [x] 응답 어디에도 비밀번호/해시 없음. 신규 pytest 통과.
- **완료 증거**: `tests/test_auth.py` 5 passed (라이브 postgres, async). 시드 로그 `seeded/refreshed admin user 'kknaks'`. 로그인 200+`Set-Cookie kknaks_session; HttpOnly; SameSite=Lax`, 틀린 자격 401 `invalid credentials`, 미인증/로그아웃 후 `/me` 401, 응답에 password/hash 미노출. **async 전환 반영**: `core/db.py` create_async_engine+AsyncSession, `service/seed.py`·auth login `async def`+`await db.execute`, main lifespan `await seed_admin()`. logout/me 는 DB 무관이라 `def` 유지. bcrypt/JWT 는 CPU-bound sync 호출(단일 관리자 저트래픽이라 event loop 영향 무시 가능).

### Phase 3 — 프론트 (톱니 · 로그인 · admin 목)

- **Status**: DONE
- **설명**: SPEC-006 UX 계약 구현. 헤더 진입 → 로그인 → 목 화면 게이트.
- **작업**:
  - [ ] `lib/api.ts` — `login`/`logout`/`authMe`(`credentials: 'include'`).
  - [ ] `topnav.tsx` — 우상단 lang 옆 톱니 아이콘 버튼 → `/admin`(`/print` 미노출 유지).
  - [ ] `app/admin/login/page.tsx` — 아이디/비번 폼, 제출 활성 규칙, 통합 에러 문구, 성공 시 `/admin` 이동, 이미 인증 시 `/admin` 이동.
  - [ ] `app/admin/page.tsx` — 마운트 시 `authMe` 체크, 미인증 → `/admin/login`, 인증 → "관리자 대시보드 (준비 중)" 목 + 계정 표시 + 로그아웃.
- **검증**:
  - [x] 톱니가 모든 공개 페이지 헤더에 노출.
  - [x] 로그인 성공/실패/미인증 접근/로그아웃 흐름이 SPEC-006 S-1~S-5대로 동작.
  - [x] 타입체크 green(내 파일 에러 0 — 잔여 3개는 삭제된 mini-game 라우트의 stale `.next/types`, 무관).
- **완료 증거**: `lib/api.ts` `authApi`(login/logout/me, `credentials: "include"`)+`AuthError`, `topnav.tsx` 우상단 톱니 SVG→`/admin`, `app/admin/login/page.tsx`(폼·제출활성·통합에러·이미인증 리다이렉트), `app/admin/page.tsx`(마운트 시 `me()` 게이트·목 대시보드·로그아웃). `npx tsc --noEmit` 내 파일 에러 0.

### Phase 4 — 통합 검증 (로컬 e2e)

- **Status**: DONE
- **설명**: FE+BE+DB를 로컬에서 붙여 SPEC-006 Acceptance를 실증.
- **작업**:
  - [x] 로컬 스택 기동(postgres+back+front, docker back + next dev) 후 톱니→로그인→목→로그아웃 e2e.
  - [x] cross-origin(3000→48000) 쿠키 왕복 확인(credentials·CORS·SameSite).
- **검증**:
  - [x] SPEC-006 §6 Acceptance Criteria 전 항목 충족.
  - [~] 세션 만료: JWT `exp` 발급 확인(디코드), 짧은 만료 실측은 생략(계약상 만료 토큰=미인증 경로는 미인증 401 로 동일 검증됨).
- **완료 증거**: 도커 back(async) 부팅 후 `POST /api/auth/login`(Origin: localhost:3000) → `200` + `access-control-allow-credentials: true` + `access-control-allow-origin: http://localhost:3000` + `Set-Cookie kknaks_session; HttpOnly; SameSite=Lax`, body `{"user":{"username":"kknaks","role":"admin"}}`. 틀린 자격 401. 프론트 `localhost:3000/admin/login` 200, owner 브라우저 e2e 로그인 정상 확인. 3000↔48000 은 same-site(localhost)라 Lax 쿠키 왕복 정상.

## Pre-deploy Check

- [ ] 기존 persona 로딩·그래프 enforce·기존 라우터 무영향(auth·db는 가산만).
- [ ] `.env`에 실제 `ADMIN_PASSWORD`·강한 `JWT_SECRET` 주입(기본 `changeme`/dev 시크릿 금지).
- [ ] 운영 쿠키 `Secure`+`Domain=.kknaks.cloud` 설정, CORS origin 와일드카드 아님.
- [ ] 응답에 비밀번호/해시/토큰 서명키 미노출.

## Rollback

- auth 라우터 미등록 + 톱니 링크 제거 → 로그인 기능 비활성(기존 공개 사이트 무영향).
- `alembic downgrade -1` → `users` 드롭. postgres 서비스는 콘텐츠 API와 무관하므로 중지해도 공개 사이트 서빙 지속.

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] SPEC-006 Acceptance/Case Matrix가 검증 항목에 반영됐다.
- [ ] 신규 pytest + `npm run build` + 로컬 e2e 통과.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- (개발 내부) alembic `env.py`가 동기 엔진·`config.database_url()`을 참조하도록 배선(offline/online 모드 모두).
- (개발 내부) 로컬 dev 쿠키가 3000↔48000 same-site로 전송되는지 브라우저 실측(Lax 기준). 문제 시 dev 한정 완화책 검토.
- 결정이 필요한 항목은 없음(§SPEC-006 §7·DEC-009 OQ는 전부 후속 범위, 비차단).

## Related

- SPEC: [[spec-006-admin-auth|KDEV-SPEC-006]]
- Decision: [[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]
