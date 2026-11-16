# [reviewer_code] case3 적응형 분할 관계 검증 재검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-app-provider-adaptive-code-v2.md`, `app-provider-adaptive-fix2-report.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-4/5를 읽고 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff(기준 HEAD `078ac99`)를 검수한다.

이전 FAIL인 한 분할 part에 모든 relation source ID가 있는데도 정상 관계 문장을 거절하는지 재현한다. relation-only, 원문+relation, 단일 호출, 서로 다른 part에 분산, 일부 source 실패를 확인한다. 위조 값·ID·쌍·방향·조건은 막고, 실제 최종 답의 인용 ID 집합이 성공·일부 실패·fallback의 `answer_citations`와 일치하는지 본다. 기본 cap 미설정 SDK/CLI 호출, context 재시도, 비용 합산, 안전 flags·유보의 앞 차수 PASS도 확인한다. 새 결함은 구체적인 재현 근거가 있을 때 보고한다.

항목별 PASS/WARN/FAIL, 파일:줄·재현·최소 수정안, 활성화 전 실물 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-provider-adaptive-code-v3.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
