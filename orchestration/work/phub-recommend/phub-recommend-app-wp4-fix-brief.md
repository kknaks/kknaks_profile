# [backend] case3 WP-4 관계 어댑터 검수 FAIL 수정

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 기존 미커밋 WP-4 코드를 이어간다. 기준 HEAD `078ac99`.

프로필 레포 `orchestration/work/phub-recommend/review-app-wp4-relation-code.md`의 F-1~F-5 전부, `WORK-011-public-contract-handoff.md`, WORK-012 WP-4, SPEC-006 0.3.10 §3-4-1-5를 읽는다.

1. 확정 단위 시술 하나 + 상대 미확정 I-07을 `(unit,unit)`로 조회하지 않는다. 자기 쌍은 명시적 재시술 질문일 때만. 상대 후보/명시 대상 resolve frontier를 열거나 `unresolved_pair`로 남기고 부재 완료를 금지한다.
2. 관계 facet을 선택 pair별·Q139 global scope별로 분리한다. pair 근거가 있어도 global 404/error/truncated/build mismatch를 숨기지 않고 그 scope를 incomplete로 유지한다. Q139 전체 답에 필요한 R8 관계와 전역 fact 수신·전달을 각각 검증한다.
3. global `applies_to.condition`과 요청·질문에서 확정된 조건을 대조한다. 조건이 확인되지 않으면 원장에는 보존하되 인용·지원 fact로 쓰지 않는다. Hub `condition` 문자열 계약과 음성 시험을 맞춘다.
4. `resolved.value/field_status/by_direction/source_fact_ids`를 해당 source ID와 결속해 최종 근거 payload에 보존한다. 원문 없는 정책값을 의료 사실로 꾸미지 않는다. 대안과 방향을 구분한다.
5. I-08의 `prior.procedure`는 질문의 이전 시술 span이 가리키는 ID를 사용하고 불확실하면 prior 판정을 보류한다. 역순 질문 시험을 추가한다.

기존 페이지·출처·부분 답·안전·분할 ID 완전성은 유지한다. 모의 Hub 음성 시험과 관련/전체 pytest, ruff, diff check. 실물 서버·DB·provider·50/239×3 평가는 실행하지 않는다. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-wp4-relation-fix-report.md`. 완료 시 `worker_done` 한 번.
