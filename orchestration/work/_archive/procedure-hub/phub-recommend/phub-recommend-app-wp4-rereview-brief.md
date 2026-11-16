# [reviewer_code] case3 WP-4 관계 어댑터 재검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-app-wp4-relation-code.md`의 F-1~F-5와 `app-wp4-relation-fix-report.md`, WORK-011 공개 계약 인계, WORK-012 WP-4, SPEC-006 0.3.10 §3-4-1-5를 읽는다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff(기준 HEAD `078ac99`)와 Hub selected 코어/fixture를 대조한다.

F-1 단일 target의 자기 쌍 오판, F-2 Q139 global 오류/미완료가 pair 지원에 가려짐, F-3 global 조건 미검사, F-4 resolved 값과 source ID 전달, F-5 prior 역방향을 실제 코드·음성 시험에서 재검수한다. 관계 facet별 완료·지원·유보와 Claude payload를 추적하고, 다른 pair/조건/owner/비인용/빌드 불일치 시 지원·부재 오판이 없는지 확인한다. 새 결함은 구체적인 재현 근거가 있을 때 보고한다.

항목별 PASS/WARN/FAIL, 파일:줄·재현·최소 수정안, WP-4 코드 수락 여부와 활성화 전 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-wp4-relation-code-v2.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
