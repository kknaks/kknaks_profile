# [planner] 수정 2판 — 네 1판 리포트 미결 1 · 2 를 코디가 원천에서 고쳤다. SPEC-000 을 다시 맞춰라

너는 day planner 워커다. 계약은 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` 그대로(설계 변경 · products/day 밖 · 커밋 금지).
네 1판 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-fix-1-report.md` 의 미결 1 · 2 가 원천 쪽 문제였다 — 코디가 원천(`/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/`)을 고쳤다:

1. `02-customer.md` external_ref 의 묶은 행 `deleted_at · created_at · updated_at` → `created_at · updated_at | ✓` + `deleted_at | (필수 아님)` 두 행.
2. `06-room.md` zone · reservation_group, `07-misc.md` chat_message · chat_attachment · notice — created_at 행에 남아 있던 deleted_at 설명 · cc 칸을 `deleted_at` 행으로 옮겼다.

할 일: SPEC-000 의 해당 표를 바뀐 원천 그대로 다시 맞춘다(그 밖은 건드리지 마라). lint `--strict` 1회 · 개수 대조(원천 / SPEC).
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-fix-2-report.md`. 완료는 preamble 의 worker_done 절차대로.
