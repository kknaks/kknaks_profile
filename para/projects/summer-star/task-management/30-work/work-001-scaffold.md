---
type: work
id: WORK-001
title: "스캐폴딩 — 레포·FastAPI·Postgres·Next 정적·Tauri 셸"
status: todo
product: "task-management"
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 0
created_at: 2026-09-05
updated_at: 2026-09-05
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-001]
  decisions: [DEC-001]
  specs: [SPEC-000]
  works: []
  releases: []
  related: []
---

# 스캐폴딩 — 레포·FastAPI·Postgres·Next 정적·Tauri 셸

**앱 창 하나와 백엔드 한 벌을 세우고, 창이 실제로 서버에 붙는 것까지** 만든다. 화면 기능은 만들지 않는다 — 로그인은 WORK-002, 유형·프로젝트는 WORK-003 이다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-001
- Covers spec: **SPEC-000**(스캐폴딩 — 앱 셸·백엔드·DB·시드)
- Depends on work: 없음 — **v1 의 첫 work**다
- Parallel work: 없음. WORK-002·003 이 이 위에 순서대로 얹힌다
- Follow-up work: WORK-002(로그인·세션) · WORK-003(업무 설정)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`. **이 문서가 있는 `kknaks_profile` 워크트리에 코드를 만들지 않는다.** 이 레포의 `app/back`·`app/front` 는 다른 제품(kknaks_profile)이다
  - `orchestration/config/projects/task-management.json` 의 **`repos.code` 등록이 이 work 착수 전에 필요**하다(현재 notes 에 「첫 코드 work 발주 때 추가」로 남아 있다) → Open Issues
  - Docker(Compose v2) · Node 20+ · Python 3.12+ · uv · Rust 툴체인(Tauri 빌드용). **codex·Redis·Soniox 는 이 work 범위 밖**이다(회의록 그룹에서 compose 에 합류)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | `repos.code` 미등록 |
| Next | Phase 1 — 레포 초기화 · 백엔드 기동 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-000 대조 | todo |
| Design |  | 연결 확인 화면·최소 폭 안내 화면 토큰 적용(SPEC-000 U-1·U-2) | todo |
| FE |  | Next 정적 골격 · shadcn·토큰 · Tauri 셸 결합 | todo |
| BE |  | FastAPI·설정·헬스 · Alembic·시드 · compose | todo |
| QA |  | Phase 검증(앱 창 E2E) | todo |
| Ops |  | compose·env 예시 · 로컬 기동 문서 | todo |

## Scope

포함:

- 코드 레포 초기화(모노 구조 — `app/back` · `app/front`) · 공통 개발 스크립트
- FastAPI + uv 골격(계층 디렉토리·`Settings`·도메인 예외 → HTTP 핸들러) + **헬스 엔드포인트**
- docker compose(Postgres + API) · `.env.example`
- **Alembic** 도구 세팅 + **account 도메인 초판 마이그레이션** + **시드**(계정 1 · 기본 유형 3, 멱등)
- Next.js 정적 골격(`output: 'export'`) + Tailwind + shadcn + **토큰 CSS 변수** + QueryClientProvider · Toaster · OverlayProvider 뼈대
- **연결 확인 화면**(SPEC-000 U-1) · **최소 폭 안내 화면**(SPEC-000 U-2)
- **Tauri 셸 결합** — `tauri dev` 로 앱 창이 뜨고 CORS origin 이 통한다

제외:

- 로그인·토큰·세션 가드 → **WORK-002**
- 유형·프로젝트 CRUD 화면 → **WORK-003**(스키마·시드만 여기서 만든다)
- Redis · open-kknaks worker · 파일 저장소 · Soniox → 회의록 그룹
- 코드 서명·설치 패키지·자동 업데이트 → v1 배포 시점

## Code Surface

- Repo / module: **`github.com/kknaks/task_management`**(신규 clone). 루트에 `app/back`·`app/front` 두 모듈을 둔다 — 아키텍처 문서의 트리(`backend/README.md` §4 · `frontend/README.md` §2)를 그대로 옮긴 구조다
- 만질 파일 후보

| 경로 후보 | 설명 |
|---|---|
| `README.md` · `Makefile`(또는 `justfile`) | 로컬 기동 절차 한 곳. `make up` · `make migrate` · `make seed` · `make app` |
| `docker-compose.local.yml` | Postgres + API. 회의록 그룹에서 Redis·worker 가 여기에 붙는다 |
| `.env.example` (back) · `app/front/.env.example` | SPEC-000 §5 환경변수 표 그대로. **비밀값 기본값 없음** |
| `app/back/pyproject.toml` · `uv.lock` | uv 의존성 |
| `app/back/main.py` | 앱 팩토리 — 라우터·CORS·예외 핸들러 **조립만** |
| `app/back/config.py` | `Settings`(pydantic-settings). env 를 읽는 유일한 곳 |
| `app/back/core/db.py` | async engine · `async_sessionmaker(expire_on_commit=False)` · `get_db` |
| `app/back/core/exceptions.py` | `AppError` 계층 + HTTP 매핑 핸들러 |
| `app/back/api/health_router.py` | `GET /api/health` — **인증 게이트 밖 두 표면 중 하나** |
| `app/back/api/deps.py` | `get_db`(+`require_account` 자리 — 구현은 WORK-002) |
| `app/back/models/base.py` · `models/account.py` | 공통 믹스인 + account 도메인 5 테이블 |
| `app/back/alembic.ini` · `alembic/versions/*` | 마이그레이션 |
| `app/back/seed/seed.py` | 계정 1 + 기본 유형 3, **멱등** |
| `app/back/tests/conftest.py` · `tests/test_health.py` | 실제 Postgres 테스트 DB |
| `app/front/package.json` · `next.config.ts` | `output:'export'` · `trailingSlash:true` · `images.unoptimized:true` |
| `app/front/tailwind.config.ts` · `components.json` | Tailwind + shadcn CLI 설정, `screens` 재정의(`desk`/`wide`/`ultra`) |
| `app/front/src/styles/tokens.css` · `globals.css` | `09-design-tokens` → CSS 변수 2층(토큰 → shadcn 시맨틱) |
| `app/front/src/app/layout.tsx` | 폰트(번들 포함) · 토큰 변수 · QueryClientProvider · OverlayProvider · Toaster |
| `app/front/src/app/page.tsx` | **연결 확인 화면**(SPEC-000 U-1). WORK-002 에서 로그인 리다이렉트로 대체 |
| `app/front/src/components/shared/MinWidthGuard.tsx` | **최소 폭 안내 화면**(SPEC-000 U-2) |
| `app/front/src/lib/api/client.ts` · `lib/env.ts` | fetch 래퍼 최소판(Bearer·401 재시도는 WORK-002) · `NEXT_PUBLIC_*` 읽는 유일한 곳 |
| `app/front/src-tauri/tauri.conf.json` · `src-tauri/src/main.rs` | 셸 설정(창 크기·CSP·dev URL). **위치는 Tauri CLI 기본 관례를 따른다**(프론트 루트의 형제) |

- Domain / schema note: **마이그레이션이 필요하다** — account 도메인 초판(§Domain / Schema). 스키마 전문은 코드·migration 이 SoT 이고 이 문서는 범위만 적는다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `account` | 계정·프로필. **앱에서 만들 수 없고 시드로만 생긴다**(DEC-001 §2) |
| `career` | 경력 행(하드 삭제). 이번엔 **테이블만** 만들고 화면은 개인 설정 그룹 |
| `auth_session` | refresh 토큰 회전 기록. 이번엔 테이블만, 쓰기는 WORK-002 |
| `work_type` | 동적 유형. **기본 3종 시드**가 여기 들어간다 |
| `project` | 프로젝트. 테이블만, 화면은 WORK-003 |

- 상태 / invariant: `database/domains/account.md` A-1~A-11 을 따른다. 특히 **A-4**(기본 3종 잠금) · **A-5**(색은 팔레트 토큰명) · **G-1**(bigint identity, slug 없음) · **G-3**(enum 은 varchar + CHECK) · **§0-1**(소프트 딜리트는 `deleted_at`)
- Migration 필요 여부: **필요**. 리비전 1건(account 도메인 5 테이블 + 인덱스). `autogenerate` 초안을 **사람이 읽고 고친다**(CHECK·부분 인덱스는 자동 생성이 놓친다 — `database/README.md` §0-2)
- SPEC 에 환류해야 하는 변경: 없음(SPEC-000 §4 Data Contract 범위 안)

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-002 | `account` · `auth_session` 테이블 · 시드 계정 · `Settings`(JWT_*) · `core/security.py` 자리 | 로그인은 시드 계정이 있어야 검증된다 |
| WORK-003 | `work_type` · `project` 테이블 · 기본 유형 3종 시드 · 토큰 CSS 변수 | 팔레트 변수는 이 work 의 `tokens.css` 에 자리를 만든다(값 8종 등록은 WORK-003) |
| 이후 전 work | compose · Alembic · 예외 핸들러 · 정적 빌드 파이프라인 · Tauri 셸 | 모든 기능이 이 골격 위에 얹힌다 |

## Internal Interface Contract

외부 계약(헬스 응답·시드 결과)은 **SPEC-000 §4** 가 정본이다. 여기서는 **후속 work 가 의존하는 내부 접점**만 고정한다.

| 접점 | 계약 |
|---|---|
| `Settings` | env 를 읽는 유일한 곳. **비밀값에 기본값을 두지 않는다**(없으면 기동 실패). 키 이름은 SPEC-000 §5 표 그대로 |
| 도메인 예외 → HTTP | `AppError(status, code)` 하위 5종(Validation 422 · Unauthorized 401 · Forbidden 403 · NotFound 404 · Conflict 409). 응답은 **`{"detail","code"}` 고정**. **핸들러는 `main.py` 한 곳에만 등록**한다 |
| 세션 의존성 자리 | `api/deps.py` 에 `require_account` 를 **선언만** 해 두고 WORK-002 가 채운다. 라우터 단위로 걸 수 있게 시그니처를 고정한다(`account_id: int` 반환) |
| 시드 실행 | `make seed` 한 줄. **멱등**이고 마이그레이션 이후에만 돈다. 값은 `SEED_*` env 에서 읽는다 |
| 프론트 API 베이스 | `lib/env.ts` 가 `NEXT_PUBLIC_API_BASE` 를 읽는 유일한 곳. 다른 파일에서 `process.env` 를 직접 읽지 않는다 |
| CSS 변수 2층 | `tokens.css` 가 `--tm-*` 원시 토큰, `globals.css` 가 shadcn 시맨틱 변수로 매핑(`frontend/README.md` §5-1). 컴포넌트는 hex 를 직접 쓰지 않는다 |

## Execution

### Phase 1 — 레포 초기화 · 백엔드 기동 · 헬스체크

- **Status**: TODO
- **설명**: 코드 레포를 만들고 **API 와 Postgres 가 compose 로 함께 뜨는 상태**까지 간다. 이 Phase 가 끝나면 화면이 없어도 백엔드가 그 자체로 돈다.
- **작업**:
  - [ ] `task_management` 레포 clone · 루트 `README.md`·`Makefile`·`.gitignore`
  - [ ] `app/back` uv 프로젝트 생성(FastAPI · SQLAlchemy 2.0 async · psycopg3 · pydantic-settings · uvicorn)
  - [ ] 계층 디렉토리 생성 — `api/` `service/` `repository/` `models/` `dto/` `schemas/` `core/` `seed/` `tests/`(빈 패키지라도 만들어 경계를 먼저 세운다)
  - [ ] `config.py` `Settings` — SPEC-000 §5 환경변수. **비밀값 기본값 금지**
  - [ ] `core/db.py`(async engine · `expire_on_commit=False` · `pool_pre_ping`) · `core/exceptions.py`(AppError 5종 + 핸들러)
  - [ ] `api/health_router.py` — `GET /api/health`(DB 왕복 포함). 인증 없음
  - [ ] `main.py` 앱 팩토리 — 라우터·CORS(**명시 목록, `allow_credentials=False`**)·예외 핸들러 조립
  - [ ] `docker-compose.local.yml`(Postgres + API) · `.env.example`
  - [ ] `tests/` 세팅(pytest · asyncio_mode=auto · httpx AsyncClient · **실제 Postgres**) + `test_health.py`
- **검증**:
  - [ ] `make up` 으로 Postgres·API 가 뜨고 로그에 오류가 없다
  - [ ] `curl :8000/api/health` 가 **200** 과 `status`·`version`·`database` 를 준다
  - [ ] **DB 컨테이너만 내리면** 같은 호출이 **503 `db_unavailable`** 이다(200 「정상」이 아니다)
  - [ ] `.env` 에서 `JWT_SECRET` 을 지우면 **API 가 기동하지 않고** 누락 변수명이 로그에 남는다
  - [ ] `pytest` 가 통과한다
- **완료 증거**: 미작성

### Phase 2 — Alembic · account 도메인 마이그레이션 · 시드

- **Status**: TODO
- **설명**: 스키마와 시드를 세운다. **계정은 앱에서 만들 수 없으므로**(DEC-001 §2) 이 Phase 가 끝나야 이후 work 의 로그인·설정을 검증할 수 있다.
- **작업**:
  - [ ] Alembic 초기화(async 엔진과 **같은 드라이버**로 물린다) · `alembic.ini`
  - [ ] `models/base.py` 공통 믹스인(`created_at`·`updated_at`) · `models/account.py`(account · career · auth_session · work_type · project)
  - [ ] 리비전 1건 생성 — `autogenerate` 초안을 **사람이 읽고 고친다**(CHECK 제약·부분 유니크·인덱스)
  - [ ] `downgrade` 작성(개발 중 되감기용)
  - [ ] `seed/seed.py` — 계정 1(`SEED_*` env, **비밀번호 해시만 저장**) + 기본 유형 3종(미팅·회의/개인 업무/문서·보고, `is_default`). **멱등**
  - [ ] `make migrate` · `make seed` 를 Makefile 에 등록
- **검증**:
  - [ ] `make migrate` 가 빈 DB 에서 오류 없이 끝난다
  - [ ] `make seed` 후 `account` 1행, `work_type` 3행이고 **셋 다 기본 유형 표시**가 켜져 있다
  - [ ] **`make seed` 를 한 번 더 실행해도 오류가 없고 행 수가 그대로다**
  - [ ] 시드 비밀번호를 규칙(8자 이상 + 문자·숫자·특수문자) 위반 값으로 두면 **시드가 실패한다**
  - [ ] `alembic downgrade -1` → `upgrade head` 왕복이 된다
- **완료 증거**: 미작성

### Phase 3 — Next 정적 골격 · 토큰 · 연결 확인 화면

- **Status**: TODO
- **설명**: 프론트를 **브라우저에서 먼저 돌린다.** 앱 창을 붙이기 전에 정적 빌드 제약(`output:'export'`)과 토큰 체계를 확정해 둔다.
- **작업**:
  - [ ] `app/front` Next 프로젝트 · `next.config.ts`(`output:'export'` · `trailingSlash` · `images.unoptimized`)
  - [ ] Tailwind + shadcn 초기화 · `screens` 재정의(`desk:1280` · `wide:1440` · `ultra:1920`)
  - [ ] `styles/tokens.css` — `09-design-tokens` 색·타입·radius·그림자를 `--tm-*` 로. **팔레트 변수 자리도 만든다**(값 8종은 WORK-003)
  - [ ] `globals.css` — shadcn 시맨틱 변수 매핑 · Pretendard **번들 포함**(CDN 금지)
  - [ ] `app/layout.tsx` — QueryClientProvider(`retry:false` · `refetchOnWindowFocus:false`) · Toaster · OverlayProvider 뼈대
  - [ ] `lib/env.ts` · `lib/api/client.ts` 최소판(에러를 `ApiError{status,code,detail}` 로 변환)
  - [ ] `app/page.tsx` — **연결 확인 화면**(SPEC-000 U-1: 확인 중 / 연결됨 / 실패 + 「다시 확인」)
  - [ ] `components/shared/MinWidthGuard.tsx` — **최소 폭 안내 화면**(SPEC-000 U-2), 루트 레이아웃에 적용
- **검증**:
  - [ ] `npm run dev` → 브라우저에서 「**서버에 연결되었습니다**」와 대상 주소·버전이 보인다
  - [ ] API 를 내리면 「**서버에 연결하지 못했습니다**」 + 사유 + 「다시 확인」이 보이고, **화면이 비지 않는다**. 「다시 확인」은 **요청을 한 번만** 보낸다
  - [ ] 창을 1280 미만으로 줄이면 「**창이 너무 좁습니다**」가 덮고, 넓히면 즉시 원래 화면으로 돌아온다
  - [ ] `npm run build` 가 `out/` 을 만들고, 산출물에 **`app/api/**`·`middleware.ts`·동적 세그먼트 디렉토리가 없다**
  - [ ] 번들에 **외부 origin 스크립트·폰트 요청이 없다**(네트워크 탭에서 자기 origin 만)
- **완료 증거**: 미작성

### Phase 4 — Tauri 셸 결합

- **Status**: TODO
- **설명**: **처음부터 앱 창에서 개발한다**(§C-4 번복). 이 Phase 가 끝나면 이후 모든 기능을 실제 셸에서 E2E 로 검증할 수 있다.
- **작업**:
  - [ ] `app/front/src-tauri` 초기화 · dev 는 프론트 개발 서버를, 빌드는 `out/` 정적 산출물을 싣게 설정
  - [ ] 창 기본 크기 **1440×900**(≥1280). **`minWidth` 를 걸지 않는다**(FE §7-2 — 안내 화면으로 막는다)
  - [ ] 앱 창 origin 을 백엔드 `CORS_ORIGINS` **명시 목록에 추가**(`*` 금지)
  - [ ] CSP 로 외부 origin 차단(SYS-3 XSS 완화)
  - [ ] 키체인 플러그인 **의존성만 추가**(사용은 WORK-002)
  - [ ] `make app` = `tauri dev` 등록 · README 에 기동 절차 4줄
- **검증**:
  - [ ] `make app` 으로 **앱 창이 뜬다**(macOS 주 개발기)
  - [ ] 앱 창에 「**서버에 연결되었습니다**」가 보인다
  - [ ] `CORS_ORIGINS` 에서 앱 창 origin 을 빼면 창이 **CORS 실패**로 뜨고, 되돌리면 다시 연결된다
  - [ ] 앱 창을 1280 미만으로 줄이면 최소 폭 안내가 덮는다
  - [ ] 새 clone + `.env.example` 복사만으로 **Phase 1~4 절차가 처음부터 재현**된다(README 대로)
- **완료 증거**: 미작성

## Pre-deploy Check

이 work 는 로컬 개발 환경만 세운다. 배포 대상이 없으므로 운영 리스크 체크는 아래 셋뿐이다.

- [ ] `.env` 실제 값이 레포에 커밋되지 않았다(`.env.example` 만 추적)
- [ ] 시드 계정 비밀번호가 **소스·로그 어디에도 평문으로 남지 않는다**
- [ ] 헬스 응답에 **버전 문자열 외 내부 정보가 없다**(env·경로·계정 정보 금지 — SPEC-000 §5)

## Rollback

- **Phase 2 스키마**: `alembic downgrade -1`. 데이터가 시드뿐이라 손실이 없다. 컨테이너째 되돌리려면 `docker compose -f docker-compose.local.yml down -v` 후 `make up && make migrate && make seed`
- **Phase 3·4**: 프론트·셸은 상태를 갖지 않는다 — 브랜치 폐기로 끝난다
- **전체**: 레포가 신규라 되돌릴 기존 서비스가 없다. `main` 에 머지 전이면 브랜치 삭제로 원복

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-000 §6 Acceptance 10개 항목이 전부 확인**됐다(Phase 검증에 1:1 로 옮겨져 있다).
- [ ] `make up → migrate → seed → app` 절차가 **새 clone 에서 재현**된다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **`repos.code` 등록이 선행돼야 한다** — `orchestration/config/projects/task-management.json` 의 notes 가 「첫 코드 work 발주 때 추가」로 남아 있다. 코드 워커 워크트리·allowed_paths 도 그때 정해진다(코디)
- **Tauri 디렉토리 위치를 `app/front/src-tauri` 로 잡았다** — Tauri CLI 기본 관례(프론트 루트의 형제)를 따랐다. 아키텍처 문서에 셸 디렉토리 규약이 없어 이 work 가 정했다
- **Next·Node·Python 버전 핀을 아직 고르지 않았다** — 아키텍처는 「Python 3.12+」만 못박았다(`backend/README.md` §1). Phase 1 착수 시 `.tool-versions`(또는 `engines`)로 고정하고 README 에 적는다
- **SPEC-000 S000-OQ-2 미해소** — `system/README.md` Overview·SYS-9 와 `frontend/README.md` FE-C2 가 아직 「웹 우선, Tauri 는 마지막 포장」이다. 이 work 는 **번복 이후(처음부터 Tauri)** 를 따랐다. 문서 정정은 코디 소관
- **SPEC-000 S000-OQ-3 미해소(Windows 확인 시점)** — 이 work 의 검증은 macOS 기준이다. Windows 에서 같은 절차가 도는지 확인하는 시점을 잡아야 한다
- **SPEC-000 S000-OQ-4 미해소(연결 확인 화면 수명)** — WORK-002 가 로그인 화면으로 대체할 때 이 화면을 남길지 정해야 한다. 지금 계획은 **대체(삭제)** 다

## Related

- SPEC: SPEC-000 (frontmatter `links.specs`)
- Work: 없음(첫 work). 후속은 WORK-002 · WORK-003
