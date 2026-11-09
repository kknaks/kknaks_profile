# [planner] SPEC-001 개정(CSRF · 빈 입력) + Delivery #227 contract v3

너는 day planner 다. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`(미커밋 SPEC-002 · SPEC-000 변경 있음). **이번엔 `spec-002-procedure-board.md` 를 건드리지 마라**(지금 다른 리뷰어가 검수 중 — 그 결과 뒤 따로 지시). 커밋 금지 · Delivery 승인 금지.

## 1. SPEC-001 개정 (사용자 결정 2026-11-06 — 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md` 「CSRF (웹)」 · 「빈 입력」 두 줄)
- 세션 전달 절 · 케이스 매트릭스에: CSRF = centurion admin 방식(세션마다 토큰 하나 · 웹 화면이 `hx-headers` 로 `X-CSRF-Token` · 없거나 틀리면 **403 `csrf_failed`** · 로그인 전 요청 `/api/auth/login` · `/api/auth/hospital` 은 CSRF 미적용 · SameSite=Lax · 앱 Bearer 는 CSRF 없음). 토큰을 둘 자리가 SPEC-000 `login_session` 에 필요하면 SPEC-000 표도 같이(원천에 「세션마다 CSRF 토큰 하나」).
- 매트릭스에: 이메일 · 비밀번호 빈 값 → KOS 안 부름 · **400 `invalid_request`**.
- 개정 머리말 한 줄 · log 한 줄.

## 2. Delivery #227 contract v3 (같은 Issue · 같은 key · contract_version 3 · 승인 안 함)
검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery227-v2-report.md` W1 ~ W7 을 「고칠 방향」대로 + A7 에 `csrf_failed` · A4 에 `invalid_request` 줄. 특히 **W1**: 재사용은 헤더 · 주소 · 시간 제한만, 직원 sign-in · get-user-account · 401(재-sign-in 없이 `expires_at` 당김)은 새 경로 · 401 재시도 금지 · 병원 고르기 전 sign-in 은 `tenant_id` 에 기대지 않음. W2 · W3 확인 방법(서비스 함수 단위 테스트 · 테스트 전용 권한 키). Issue 제목도 v2 이후 목표에 맞게 바꿀 수 있으면 바꾼다(스킬이 못 하면 리포트에).

## 3. SPEC-000
`staff.is_system_account` 설명을 「병원 연결의 sign-in 시스템 계정 하나 — 원장 목록에서 빠짐 · 마취용 · 공용은 1차에 빼지 않음(사용자 2026-11-06)」으로(SPEC-002 fix2 리포트가 남긴 것).

lint `--strict` 1회. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-csrf-delivery227-v3-report.md` — 바뀐 줄 · v3 전후 · plan_digest. 완료는 preamble 의 worker_done 절차대로(둘 다).
