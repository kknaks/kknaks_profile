# [planner] SPEC-001 화면 절 먼저 — 로그인 화면(웹) · #232 v2 앞

너는 day planner 다. mediness 워크트리 · 미커밋 · 커밋 금지. Issue #232 는 이번에 고치지 마라(이 절이 닫힌 뒤 v2).
읽을 것: 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery232-report.md` W1 ~ W5 · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md` 「웹 화면」 새 줄(사용자 2026-11-06) · #227 코드(`/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture/backend/day/` routers · services/auth.py · session.py) · centurion admin 로그인 본.

1. **SPEC-001 개정**: §3 · OQ-1 을 원천 새 줄대로 — 웹 = 화면 라우트(`/login` · `/login/hospital` · 로그아웃) HTML 조각 · `/api/auth/*` = 앱 전용 · 같은 service.
2. **SPEC-001 화면 절 새로**: 화면 · 흐름(미로그인 → 로그인 → (병원 고르기) → 로그인 뒤 갈 곳 · 로그아웃) · **매트릭스 줄마다 화면 처리 · 문구**(W4 의 빠진 셋 포함) · 병원 고르기 임시 토큰을 웹이 들고 가는 곳(W3 — 원천 · #227 코드 근거로 제안, 근거 없으면 OQ) · 로그인 뒤 갈 곳(1차 = 견본 또는 빈 홈 — #231 뒤 시술 현황).
3. 문구는 매트릭스의 뜻 그대로 쓰고 **사용자 확인이 필요한 문구는 표로 모아** 리포트 「사용자 확인」 절에(추천 문구 같이). 발명 금지.
4. log 한 줄 · lint `--strict`.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-screen-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
