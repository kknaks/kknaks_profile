# [reviewer_code] case3 적응형 입력·관계값 재검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/review-app-provider-adaptive-code.md`와 `app-provider-adaptive-fix-report.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-4/5를 읽고 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff(기준 HEAD `078ac99`)를 검수한다.

이전 FAIL: 단일 호출 또는 분할·원문 fallback에서 검증된 `resolved.value/field_status/by_direction`과 `prior.ok/basis`가 최종 답에 남는지 확인한다. 여러 source ID가 서로 다른 part에 있을 때 전부 성공해야만 관계값이 나오고 하나라도 실패하면 유보·incomplete가 되는지, 모델이 임의 relation 문장을 추가하거나 ID·방향·조건을 바꿔도 검증기가 막는지 음성 시험한다. 기본 cap 미설정 SDK/CLI 호출, context 재시도, ID/안전 flags/부분 답과 cost 합산의 앞 차수 PASS도 확인한다. 새 결함은 구체적 재현 근거가 있을 때 보고한다.

항목별 PASS/WARN/FAIL, 파일:줄·재현·최소 수정안, 활성화 전 실물 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-provider-adaptive-code-v2.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
