# [reviewer_code] case3 분할 ID 완전성 7차 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v6.md`, `app-walk-phase-a-fix6-report.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5를 읽고 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff를 기준 HEAD `078ac99`에 대조한다.

6차 FAIL인 F1/F2 중 F1만 인용한 SDK·CLI part가 완료로 세어지는지 재현한다. 누락·추가·중복 ID, 잘못된 owner/target/원문, 실패 trace와 `delivery_groups`, 지원 부분 답·유보·안전 flags를 함께 확인한다. 새 결함은 구체적 재현 근거가 있을 때 보고한다. 실물 provider·Hub·QID는 코드 판정과 구분한다.

항목별 PASS/WARN/FAIL, 파일:줄·근거·최소 수정안, WP-4 발주 가능 여부와 활성화 전 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v7.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
