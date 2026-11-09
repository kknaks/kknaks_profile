# [planner] DAY-SPEC-001 로그인 · 세션 — PR #909 에 같이

너는 day planner 워커다. 계약은 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` 그대로(원천에 없는 정책 발명 금지 · products/day 밖 금지 · 커밋 금지).
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` (PR #909 브랜치 — 같은 PR 에 들어간다, 사용자 2026-11-05).

**왜**: Delivery #227(로그인)이 대상 SPEC 없이 열렸다(코디 실수 — 사용자 지적). 로그인 · 세션의 외부 계약(API · 쿠키 · 오류 · 만료)을 SPEC 으로 먼저 닫는다.

## 원천 (정한 것)

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md` — 「정한 것」 · 「로그인 흐름 — KOS 그대로」 표(① sign-in → ② get-user-tenants → ③ get-user-account → 세션) · account · staff · job_role · job_role_permission · login_session · external_session · account_brand_access
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` — api / worker 분리(로그인은 api 의 바로 조회 예외) · 「위험 — KOS 내부 API 차단」(브라우저 헤더 필수)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/README.md` 공통 규칙 · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/01-hospital.md`(crm_connection.config.tenant_id · is_demo · APP_ENV=dev)
- DAY-SPEC-000 §3 04(이미 이 워크트리에 있음) — 데이터 칸은 여기를 **참조만**(복제 금지)
- 참고(권한 아님): cc-prototype `procedure/back/app/kos/client.py`(sign-in · get-user-account · 토큰 갱신 · 401 재시도 · 브라우저 헤더) ·
  KOS HAR `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/로그인.har`(필드 이름만 — 값 옮기지 마라) ·
  CENTURION_DAY `AGENTS.md`(v2-dev — 「작업 규칙」: API 경로 · 인증 · 쿠키 · 오류 계약 = 외부 계약 · 「웹 화면」: CSRF) · centurion admin 세션 방식(`git -C /Users/kknaks/git/centurion show origin/main:backend/admin/session.py`)

## 할 일

1. `products/day/20-spec/spec-001-login-session.md`(DAY-SPEC-001 · draft) — 사용자 동작과 계약:
   - 로그인 흐름(우리 화면 → KOS sign-in → 병원 고르기 → 직원 · 직무 채움 → 세션) · 자동 채움 규칙 · 비밀번호 저장 안 함 · KOS 토큰 보관(external_session)
   - 병원 고르기(연결된 병원만 · 하나면 자동) · 본사(브랜드 조회) · 시스템 관리자
   - 세션 만료 · KOS 토큰 만료 · 로그아웃 · 권한(직무 → job_role_permission) · `APP_ENV=dev` 는 데모 연결만
   - 실패 경우(KOS 비밀번호 틀림 · KOS 403 · 연결된 병원 없음 · 직원 계정 없음 · 2단계 인증 계정)
   - **원천에 없는 계약 값(API 경로 · 쿠키 이름 · 세션 길이 · 오류 코드 · 재로그인 정책 · 2단계 인증 처리)은 정하지 마라** — 각각 OQ 로 옵션 + 권장(근거: centurion · cc 선례)을 적는다. 사용자가 고른다.
2. `20-spec.md` 인덱스 · `30-work.md` Spec Coverage(인덱스 미러 규칙대로) · `log.md` 한 줄(PR `#909`).
3. lint `--strict` 1회.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-report.md` — 작성 내용 · 원천 근거 표 · **사용자에게 받을 OQ 목록(옵션 + 권장)**. 완료는 preamble 의 worker_done 절차대로.
