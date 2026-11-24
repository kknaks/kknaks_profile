# [backend] fix-2 — 재검수 review-code-2 N1 · N2

읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/review-code-2-report.md` N1 · N2 · 결정 파일 C18(바뀜 — **동기화 이력 비교는 글만**).

- N1: `policies/board_chart_tabs.py` C18 판정 — `baseLogId` 뒤 `source=kos` 이력은 **마지막 글만** 요청 `baseBody` 와 비교(집도의 비교 안 함 · KOS 쪽 판정이 집도의를 본다). 테스트: 의사차트 · KOS 집도의 둘 → 409 → 동기화 이력 → 다시 저장 = 200 · 글 한 번.
- N2: `README.md:200` 파일 이름 → `backend/tests/day/board/test_board_chart_conflicts.py`.

검증: `scripts/test.sh -q backend/tests/day/board` · ruff. 커밋 금지. 보고 `be-fix-2-report.md` + preamble worker_done 두 채널. (SPEC 문구는 planner 가 따로 맞춘다.)
