# [reviewer_code] case3 WP-4 관계 어댑터 3차 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-app-wp4-relation-code-v2.md`와 `app-wp4-relation-fix2-report.md`, WORK-011 공개 계약 인계, WORK-012 WP-4, SPEC-006 0.3.10 §3-4-1-5를 읽는다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff(기준 HEAD `078ac99`)와 Hub selected 코어를 대조한다.

F-1 `다른 시술을 다시`의 자기 쌍 오판, F-3 복수 조건의 전역 행 누락·거짓 부재, F-5 역방향 `prior.ok/basis`의 source-bound Claude payload 전달을 작은 음성 시험과 실행 경로에서 확인한다. 이전 F-2/F-4 PASS, 페이지·build·출처·안전·분할 ID 완전성이 깨지지 않았는지 본다. 새 결함은 구체적인 재현 근거가 있을 때 보고한다.

항목별 PASS/WARN/FAIL, 파일:줄·재현·최소 수정안, WP-4 코드 수락 여부와 활성화 전 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-wp4-relation-code-v3.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
