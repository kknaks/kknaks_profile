# [reviewer_code] case3 분할 수정 5차 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v4.md`와 `app-walk-phase-a-fix4-report.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5를 읽고 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 현재 diff를 기준 HEAD `078ac99`에 대조한다.

이전 FAIL인 분할 후 미완료 유보/필수 안전 flags/지원 fact 완전성, 각 SDK·CLI part error/refusal/stop 처리와 완료 판정이 실제 경로와 음성 시험에서 닫혔는지 본다. 같은 section의 두 대상, 반복·전치·공통 facet, claim별 target_key/owner/scope 검증, CLI timing 보존도 확인한다. 새 결함도 지적하되 실물 provider 한도·QID 재생 미수행은 코드 결함과 구분한다.

각 항목 PASS/WARN/FAIL, 파일:줄·근거·최소 수정안, WP-4 발주 가능 여부와 활성화 전 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v5.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
