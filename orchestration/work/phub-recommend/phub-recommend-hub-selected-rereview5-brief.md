# [reviewer_code] Hub K8·상태 6차 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-hub-selected-code-v5.md`, `hub-selected-fix5-report.md`, SPEC-005 §5-5·§6-9, WORK-011을 읽고 Hub worktree `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`의 현재 diff를 기준 HEAD `2edc190`에 대조한다.

5차 FAIL인 K8 section 변조가 완료로 통과하는지, Q139 원문 변조가 공개 열거 밖의 status를 반환하는지 음성 시험으로 검증한다. 다른 전역 text의 인용 불가가 실제로 유지되는지, 선택 쌍·550행 페이지·REST/MCP 응답의 앞 차수 PASS가 깨지지 않았는지 소수 시험으로 확인한다. 새 결함은 구체적인 재현 근거가 있을 때 보고한다. 항목별 PASS/WARN/FAIL, 파일:줄·근거·최소 수정안, **앱 WP-4 인계 가능 여부**를 적는다.

읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-hub-selected-code-v6.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
