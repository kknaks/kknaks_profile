# [planner] DAY-SPEC-001 — 사용자 결정 반영(OQ 11개 전부 권장대로)

너는 day planner 워커다. 계약은 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` 그대로. 워크트리 같은 곳(PR #909 · 미커밋 SPEC-001 위에서).
네 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-report.md` 의 「사용자에게 받을 OQ」 11개를 **사용자가 2026-11-05 전부 권장대로 정했다.**

할 일:
1. `spec-001-login-session.md` §5 OQ-1 ~ OQ-11 을 닫는다 — 각 권장안을 본문 계약(§3 · §4)으로 옮기고 OQ 표에는 「정함(사용자 2026-11-05)」으로 남긴다.
   - OQ-6(2단계 인증): 근거 한 줄 추가 — **cc-prototype 은 2단계 인증 처리가 없다(시스템 계정 하나) · KOS 명동점 직원 계정 90개 중 2단계 인증이 켜진 계정 0개(2026-11-05 코디 확인)**. 1차는 다루지 않고, 켜진 계정은 막고 안내.
   - OQ-7(a): 1차 로그인 = 병원 직원만. 본사 · 시스템 관리자 로그인은 「1차 밖 — SPEC-000 login_session 개정과 함께」로 표시.
2. status 는 draft 유지. version 만 템플릿 규칙대로 올린다(필요하면).
3. `log.md` 한 줄 · lint `--strict` 1회.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-fix-report.md`. 완료는 preamble 의 worker_done 절차대로.
