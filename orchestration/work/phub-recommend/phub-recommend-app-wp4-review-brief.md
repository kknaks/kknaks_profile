# [reviewer_code] case3 WP-4 관계 어댑터 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/WORK-011-public-contract-handoff.md`, `WORK-012.md` WP-4, `SPEC-006.md` 0.3.10 §3-4-1-5, `SPEC-005.md` §5-5·§6-9와 `app-wp4-relation-report.md`를 읽는다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff(기준 HEAD `078ac99`)와 Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`의 선택 관계 코어/fixture를 대조한다.

확정 단위 pair·전역 Q139을 별도 frontier로 수집하고 cursor/more/complete/status를 끝까지 처리하는지, 64/32 KiB 호출 상한이 전체 탐색 종료로 전파되지 않는지 본다. claim/resolved/대안·전역 각 fact의 ID/text/source/applies_to/quotable/방향/조건을 실제 지원 판정과 Claude payload까지 추적한다. 다른 pair·조건·owner의 근거를 인용하지 않고 `quotable=false`, truncated/error/build mismatch에서 부재나 지원 완료를 선언하지 않는지 음성 시험한다. 기존 WP-1~3/5의 부분 답·안전·분할 ID 완전성이 깨지지 않았는지도 본다. 대표 R8 5개와 Q139 별도 scope 접근을 검사한다.

항목별 PASS/WARN/FAIL, 파일:줄·재현·최소 수정안, 활성화 전 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-wp4-relation-code.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
