# [reviewer_doc] 검수 — DAY-SPEC-001 로그인 · 세션

너는 day reviewer_doc 워커다(read-only · 리포트 1개 · 커밋 금지). 방법은 1판 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-review-doc-brief.md` 와 같다 — 원천 대비 누락 · 발명 · 왜곡.

대상: 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` 의 미커밋 변경(`git diff` + untracked) — 새 `products/day/20-spec/spec-001-login-session.md` · `20-spec.md` · `30-work.md` · `log.md`. SPEC-000 · architecture 는 이미 PASS — 다시 보지 마라(SPEC-001 이 SPEC-000 과 어긋나는지만 본다).

원천(정답지):
1. `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md`(정한 것 · 로그인 흐름 · 테이블) · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md`(api 예외 · KOS 헤더 위험) · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/01-hospital.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/README.md` 공통 규칙
2. **사용자 결정(2026-11-05)** = `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-report.md` 「사용자에게 받을 OQ」 표의 **권장안 11개 전부** + OQ-6 근거(cc 처리 없음 · 명동점 90계정 중 0개)
3. planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-fix-report.md` — planner 가 「권장안 밖에서 붙인 이름」을 스스로 적었다: 경로 `/api/auth/logout` · `/api/auth/hospital`, 오류 코드 `staff_inactive` · `unauthorized` · `forbidden`. **이것들을 발명으로 볼지 판정하고, 결정 · 원천에 근거가 없으면 WARN 이상으로 따로 모아라**(사용자가 고르게).

볼 것: 결정 11개가 빠짐없이 · 바뀌지 않고 들어갔나 · 원천에 없는 정책 · 값 · 경로 · 코드 · SPEC-000(login_session 필수 칸 · external_session 등)과 모순 · 「아직 열린 것」이 정말 열린 것인가 · 보안 grep · lint `--strict` 1회.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-report.md` — PASS / WARN / FAIL. 완료는 preamble 의 worker_done 절차대로.
