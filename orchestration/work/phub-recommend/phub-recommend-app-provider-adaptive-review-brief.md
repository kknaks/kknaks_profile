# [reviewer_code] case3 provider 입력 적응형 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble 완료 보고를 따른다. 프로필 레포 `orchestration/work/phub-recommend/app-provider-adaptive-report.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-5와 공식 Claude Sonnet 5.5 context/token-counting 문서를 읽는다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 diff(기준 HEAD `078ac99`)를 검수한다.

핵심: cap 미설정 기본 SDK·CLI가 최종 선별 근거로 모델을 실제 호출하는지, API token preflight와 CLI 실제 context 오류 감지·이분 재시도가 과도한 입력을 `정보 없음`으로 바꾸지 않는지 확인한다. 한 fact 초과, 일부 part 실패, 명시 override, 비용/시간 중복·누락, ID/target/facet/source/안전 flags/미완료 유보 보존을 음성 시험한다. retrieval frontier가 생성 입력 cap 때문에 조기 종료되지 않는지 확인한다. WP-4 관계 근거와 resolved 값이 분할에서 유실되지 않는지도 본다. 새 결함은 구체적인 재현 근거가 있을 때 보고한다.

항목별 PASS/WARN/FAIL, 파일:줄·재현·최소 수정안, 활성화 전 실물 관문을 적는다. 읽기 전용, 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/review-app-provider-adaptive-code.md`만 생성. 코드·서버·DB·평가 수정/실행 금지, 소수 단위 시험만 허용. 커밋·push·PR 금지. 완료 시 `worker_done` 한 번.
