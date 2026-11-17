# [backend] be-3 — N1 한 건만 (빠르게)

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-be-brief.md`(역할 · allowed_paths · 검증 · 완료 보고)를 따른다. 작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback`(미커밋 위에). 혼자 작업한다.

## 고칠 것
검수 `…/fix-feedback/review-code-2-report.md` **N1**(:59 · :67 · :76): 스냅샷 `systemDoctor` 가 줄 상태와 상관없이 참 → 「바로 시작」 → 「시작 취소」 줄이 「간호관리 준비중」, 다시 의사 호출하면 「간호관리 호출」로 호출 대상(「전체」 · 지정 원장)이 가려짐.
- `backend/day/services/board_rules.py:149` `system_doctor` 를 **진행중 · 완료 줄일 때만** 참으로(스펙 SPEC-002 U-3 :225 — 「간호관리」는 진행중 · 완료 자리 글자).
- 테스트 1개 이상: 시작 취소 뒤 준비중 → false · 그 줄 호출 → false · 진행중/완료 → true. 기존 systemDoctor 테스트 그대로 초록.

## 검증
- `cd backend && uv run pytest -q <고친 테스트 파일>` · ruff — 1회. infra 테스트를 고쳤으면 `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q <그 파일>`(컨테이너 건드리지 마라).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/be-3-report.md` (짧게). 완료 보고는 preamble 의 worker_done.
