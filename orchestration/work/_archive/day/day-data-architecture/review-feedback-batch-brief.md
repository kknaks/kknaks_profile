# [reviewer] 화면 피드백 수정 묶음 — 코드 검수 (커밋 전)

너는 #230 · #231 을 검수한 day reviewer 다. **읽기 전용** · KOS 호출 금지 · **compose 는 사용자가 보는 중 — down · 재시작 금지** · 테스트는 `uv run pytest -m "not infra"` 만(전체는 코디 확인).
대상: 마지막 커밋 `3cbb2e08` 이후 미커밋 변경 전부(`git diff` · `git status`).
읽을 것: 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md`(F1 · F3 ~ F16) · SPEC-002 ⑥⑦⑧(PR #909 `19e5e461`) · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` · 작업 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-landing-fix-report.md` · `frontend-feedback-a-report.md` · `-b-` · `-c-` · `-d-` · `backend-feedback-a-report.md` · `-b-` · `-c-` · Issue #230 v7 · #231 v4.
볼 것: 피드백 항목마다 구현이 결정대로인가 · F3 다시 호출(유효 호출 · 앞 수락 무효 · 닫기 규칙 · KOS 재전송) · F10 누른 사람 토큰 · `sender_staff_id` migration 0005 · 데모 연결만 열림(`KOS_TRIAL_WRITES_ON_LIVE`) · F16 바로 보내기(중복 · 잠금 · 실패 시 응답) · F11 day.js 판 맞추기 장치 · 손 CSS · 인라인 스크립트 0 · 테스트 규칙 · 누출 · 「조용히 통과」.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-feedback-batch-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
