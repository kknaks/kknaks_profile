# [reviewer_doc] 검수 — 40-architecture 추가(시스템 런타임 · 코드 구조)

너는 day reviewer_doc 워커다(read-only · 리포트 1개만 · 커밋 금지). 방법은 1판 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-review-doc-brief.md` 와 같다 — 원천 대비 누락 · 발명 · 왜곡.

대상: 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` 의 미커밋 변경 — `git diff` + untracked
(`products/day/40-architecture/system.md` · 새 `code-structure.md` · `README.md` · `log.md`). SPEC-000 등 나머지는 이미 PASS 다 — 다시 보지 마라.

원천(정답지):
1. 시스템 런타임 — `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md`
2. 코드 구조 — `git -C /Users/kknaks/git/CENTURION_DAY show origin/v2-dev:AGENTS.md` (mediness 에는 요약 + 링크만이어야 한다 — 복제 · 발명 여부)
3. 지시서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-arch-instructions.md` · planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-arch-report.md`(주장을 실물로 확인)

볼 것: 원천에 없는 기술 · 버전 · 수치 · 구성요소가 들어갔나(planner 가 「caddy 위치는 원천에 없어 일반 앞단으로 그림」이라고 했다 — 표시가 됐는지) · 원천의 결정이 빠지거나 바뀌었나 ·
`rules/document-pipeline.md` 40-architecture 규칙(함수 목록 · API 본문 금지) · 기존 절과 새 절이 서로 어긋나지 않나 · 링크 · lint `--strict` 1회.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-arch-report.md` — PASS / WARN / FAIL. 완료는 preamble 의 worker_done 절차대로.
