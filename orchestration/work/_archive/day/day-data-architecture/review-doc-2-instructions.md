# [reviewer_doc] 재검수 — DAY SPEC-000 수정 1 · 2판

너는 day reviewer_doc 워커다(read-only · 리포트 1개만). 계약 · 방법은 1판 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-review-doc-brief.md` 그대로다.

읽을 것:
1. 네 1판 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-doc-report.md` — FAIL F1 · F2, WARN W1 ~ W4
2. 원천이 바뀌었다 — `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/`: 묶은 행 deleted_at 분리(NULL 허용) · `consultation_procedure`(03) · `visit_occupied_resource_doctor`(06) 칸 표 추가 · 03 머리말 「정함」
3. planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-fix-1-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-fix-2-report.md` — 주장을 믿지 말고 실물로

확인할 것:
- F1 · F2 · W1 · W4 가 풀렸는가(1판 지적 줄을 다시 본다).
- **바뀐 원천 전체**를 1판과 같은 방법(줄 순서 diff · 직접 셈)으로 다시 대조 — 수정하면서 새로 생긴 누락 · 발명 · 왜곡이 없는가.
- W2(ESC-001 값)는 **사용자가 그대로 두기로 했다** — 지적하지 마라. W3(log PR 칸)은 코디가 PR 때 채운다.
- lint `--strict` 1회.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-doc-2-report.md` — 판정 PASS / WARN / FAIL. 완료는 preamble 의 worker_done 절차대로.
