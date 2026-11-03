# [backend] case3 WP-4 자기 쌍·복수 조건·prior 수정

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 기존 미커밋 WP-4 코드를 이어간다. 기준 HEAD `078ac99`.

프로필 레포 `orchestration/work/phub-recommend/review-app-wp4-relation-code-v2.md` 전체, WORK-011 공개 계약 인계, WORK-012 WP-4, SPEC-006 0.3.10 §3-4-1-5를 읽는다.

- F-1: `다시 받`만으로 자기 쌍을 만들지 않는다. 질문이 확정 단위 시술 자체의 반복을 가리킬 때만 self pair를 조회한다. `이마 보톡스 후 다른 시술을 다시 받아도 되나요?`는 상대 미확정으로 남고 부재 완료를 선언하지 않는다. 유사 변형 음성 시험을 추가한다.
- F-3: 질문에서 `같은 날`과 `같은 부위` 등 여러 확정 조건을 모두 보존한다. 전역 row 조건은 그 집합과 대조한다. 맞는 row가 있는데 조건 추출이 하나로 압축돼 거짓 `unresolved_absence`가 되지 않게 한다. 미확정 조건 row는 인용하지 않고, 그 선별 실패를 원천 부재 완료로 바꾸지 않는다.
- F-5: 완료된 pair scope의 Hub `prior.ok/basis`를 source ID·방향·경과 기간과 결속해 Claude payload 및 facet 원장에 전달한다. 원문 fact가 입증하지 않는 정책값을 생성하지 않는다. 이전 시술이 두 번째 target인 역방향 요청/답 fixture를 추가한다.

기존 F-2/F-4 PASS, 페이지·출처·부분 답·안전·분할 ID 완전성 유지. 관련/전체 pytest, ruff, diff check. 실물 서버·DB·provider·50/239×3 평가는 실행하지 않는다. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-wp4-relation-fix2-report.md`. 완료 시 `worker_done` 한 번.
