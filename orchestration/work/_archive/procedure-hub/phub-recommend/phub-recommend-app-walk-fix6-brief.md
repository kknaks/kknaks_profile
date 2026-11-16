# [backend] case3 분할 part 인용 ID 완전성 수정

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 기존 미커밋 작업을 이어간다. 기준 HEAD `078ac99`.

프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v6.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5를 읽는다.

분할 part의 제공된 `rows/support_ids` 전체와 모델 답의 인용 ID 집합을 비교한다. 누락·추가·중복이 생긴 경우 해당 part를 완료로 기록하거나 `delivery_groups`에 미확인 ID를 넣지 않는다. 필요한 경우 누락 ID를 별도 재처리하되 완료 판정은 확인된 ID만 반영한다. SDK·CLI에서 F1/F2 중 F1만 답하는 음성 시험과 ID 추가/중복 시험을 넣는다. 실패 사유와 `unread`/blocked/stop trace도 일치시킨다. 성공 part의 부분 답·미완료 유보·안전 flags를 유지한다.

기본 gate False와 WP-4 미구현 경계 유지. 실물 서버·DB·provider·50/239×3 평가는 실행하지 않는다. 관련/전체 pytest, ruff, diff check. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-walk-phase-a-fix6-report.md`. 완료 시 `worker_done` 한 번.
