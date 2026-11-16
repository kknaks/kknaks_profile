# [reviewer_code] case3 분할 part 6차 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v5.md`, `app-walk-phase-a-fix5-report.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5를 읽고 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 현재 diff를 기준 HEAD `078ac99`에 대조한다.

5차 FAIL인 정상 stop이지만 잘못된 ID/owner/target_key/원문을 가진 SDK·CLI part가 완료로 세어지는지 다시 시험한다. 실패 part의 incomplete/blocked, 성공 part의 부분 답·안전 flags·유보, 최종 trace/answer_validation을 함께 확인한다. 앞 차수 PASS가 깨지지 않았는지도 소수 시험으로 본다. 새 결함은 구체적인 재현 근거가 있을 때 보고한다. 실물 provider 한도/Hub/QID 재생은 코드 판정과 분리한다.

항목별 PASS/WARN/FAIL, 파일:줄·근거·최소 수정안, WP-4 발주 가능 여부와 활성화 전 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v6.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
