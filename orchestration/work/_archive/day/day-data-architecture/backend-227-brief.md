# [backend] Delivery #227 — 로그인 · 세션 (DAY-SPEC-001 · contract v3)

너는 day backend 워커다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/backend/`(rules.md 2026-11-06 테스트 규칙 — DB 쓰는 테스트와 안 쓰는 테스트 나누기). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — #224 · #225 · #226 커밋 위에 이어서(PR #228 하나). 다른 워커 없음.

## SSOT

- **계약 = Issue #227 contract v3** `gh issue view 227 -R MediSolveAIDev/CENTURION_DAY` — Target Delta · Acceptance A1 ~ A10 · Non-Goals · Review Surface. (Delivery 승인은 사용자 몫 — 사용자가 구현을 지시했다.)
- **정본 = DAY-SPEC-001** `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-001-login-session.md`(경로 4 · 오류 매트릭스 · Functional Rule · 상태도 · CSRF · 빈 입력) · SPEC-000 04(`account` · `staff` · `job_role` · `job_role_permission` · `login_session` · `external_session`).
- 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md` 「로그인 · 세션 계약」.
- 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery227-v2-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-csrf-delivery227-v3-report.md`(특히 N1 — 아래).
- 본: centurion admin CSRF(`git -C /Users/kknaks/git/centurion show origin/main:backend/admin/web.py` · `session.py` · `templates/base.html` — `hx-headers`) · cc 로그인(`git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/...` 로그인 · 계정 경로) · 로그인 HAR(main 체크아웃 · gitignore) `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/로그인.har`(경로 · 칸 이름만).

## 정해 둔 것 (검수에서 나온 것)

- **#226 KOS client 의 401 재시도 · 시스템 계정 sign-in 을 직원 경로에 쓰지 마라**(v3 W1). 재사용 = 헤더 상수 · 주소 · 시간 제한만. 직원 sign-in · get-user-tenants · get-user-account(직원 토큰) · 401 처리(재-sign-in 없이 `expires_at` 당김 · 다른 세션 그대로)는 새 경로.
- **`kos-client-uri` (v3 검수 N1 · HAR 근거)**: sign-in = `<web>/auth/sign-in` · get-user-tenants = `<web>/hospital/select` · get-user-account = `<web>/<tenant>`. 병원 고르기 전에는 연결 설정 `tenant_id` 에 기대지 않는다. 너의 HAR 확인으로 맞는지 한 번 더 보고 리포트에 적는다.
- CSRF = centurion admin 방식(세션마다 토큰 · `hx-headers` · 403 `csrf_failed` · 로그인 전 요청 미적용 · 앱 Bearer 없음). 빈 입력 = 400 `invalid_request`(KOS 안 부름).

## allowed_paths

`backend/day/`(routers/api · services · schemas · dtos · session.py · web.py 등 계약 code_surface) · `backend/day/emr/kos/`(직원 경로 추가 — 시스템 경로는 고치지 마라) · `backend/common/` · `backend/runtime/`(라우터 등록) · `backend/tests/` · `deploy/local.env.example` · `AGENTS.md`(실행 · 로그인 한 줄). 모델 · migration 은 계약이 요구하면(`login_session.csrf_token` 등 SPEC-000 개정분) — 그 경우 새 리비전 `0003`.

## 하지 말 것

화면(Jinja2 로그인 페이지 디자인) · KOS 쓰기 · 명동점 키 · 비밀번호 저장/로그 · 커밋. 포트 11040 · 11042 · 11043 만, 끝나면 `down`.

## 검증 · 보고

- `uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff — 두 수치 모두.
- **실물 1회(필수)**: 로컬 compose + 데모 지점 연결 시드 상태에서 **데모 지점 계정**(`deploy/local.env` 의 `DAY_SEED_KOS_SYSTEM_*` — 데모 지점 시스템 계정이 유일한 데모 로그인 계정이다)으로 `POST /api/auth/login` → (병원 하나면 바로 세션) → `GET /api/auth/me` → `POST /api/auth/logout` → `/me` 401 까지 curl 로. 행 건수 · 응답 코드만 보고(토큰 · 쿠키 값 · 이메일 금지). 같은 계정 두 번 로그인 → 중복 행 없음.
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-227-report.md` — A1 ~ A10 증거 · 새/재사용 경로 표 · `kos-client-uri` HAR 대조 · 남은 것. 완료는 preamble 의 worker_done 절차대로(둘 다).
