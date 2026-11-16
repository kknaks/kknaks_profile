# [reviewer_code] Hub 선택 관계 4차 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

프로필 레포 `orchestration/work/phub-recommend/review-hub-selected-code-v3.md`와 `hub-selected-fix3-report.md`, SPEC-005 §5-5·§6-9, WORK-011을 읽고 Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`의 현재 diff를 기준 HEAD `2edc190`에 대조한다.

핵심은 R8-0180/R8-0244 interval 조건의 잘못된 key 차단, 일반 R8 claim의 source path ID 결속, 공유 claim·resolved·대안 회귀, 기존 186 section 첫 페이지 ID 순서와 peek/cut/safety 회귀 증거다. 다른 조건 표현에도 부당한 key를 추정하거나 인용하지 않는지 새 음성 사례를 본다. 항목별 PASS/WARN/FAIL과 파일:줄·근거·최소 수정안, **앱 WP-4 인계 가능 여부**를 적는다.

읽기 전용. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-hub-selected-code-v4.md`만 생성한다. 코드·서버·DB·평가 수정/실행 금지, 필요한 소수 단위 시험만 격리 실행 가능. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
