# [planner] SPEC-001 재검수 W1 반영 — session_expired 범위 (사용자 결정 2026-11-05 — 추천대로)

너는 day planner 워커다. 계약 그대로. 같은 워크트리(PR #909 · 미커밋).
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-2-report.md` W1 · 바뀐 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md` 「로그인 · 세션 계약」 오류 · 재로그인 행.

결정: (1) KOS 조기 401 → **`session_expired`** (2) 병원 고르기 임시 토큰(5분) 만료 → **`session_expired`** (3) KOS 401 로 세션을 끝낼 때는 **`login_session.expires_at` 을 지금으로 당긴다**(`revoked_at` 은 로그아웃에만).

할 일: SPEC-001 의 오류 매트릭스 · 상태도 · Functional Rule · 「session_expired 범위」 문장 · 「아직 열린 것」을 원천대로 맞춘다(「아직 열린 것」이 비면 「없음」). 그 밖은 건드리지 마라. log 한 줄 · lint `--strict` 1회.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-fix3-report.md`. 완료는 preamble 의 worker_done 절차대로.
