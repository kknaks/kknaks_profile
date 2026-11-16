# [backend] case3 분할 part 완료 판정 수정

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 기존 미커밋 작업을 이어간다. 기준 HEAD `078ac99`.

프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v5.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5를 읽는다.

`case3.py:2020–2024`에서 분할 part의 `_supported_answer=False`를 trace에만 적고 무조건 성공으로 세는 FAIL을 고친다. 유효하지 않은 모델 답은 해당 part 실패/incomplete로 기록하거나, 서버 원문 재합성이 독립적인 무모델 성공 경로라면 모델 실패와 결정론 대체 성공을 명확히 분리해 완료 판정·trace·유보를 정합시킨다. 잘못된 ID/owner/target_key, 빈 답, 정상 stop이지만 근거 불일치인 SDK·CLI part 음성 시험을 추가한다. 다른 성공 part의 부분 답, 안전 flags, 미완료 facet 유보를 유지한다.

기본 gate False, WP-4 미구현 경계 유지. 실물 서버·DB·provider·50/239×3 평가는 실행하지 않는다. 관련/전체 pytest, ruff, diff check. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-walk-phase-a-fix5-report.md`. 완료 시 `worker_done` 한 번.
