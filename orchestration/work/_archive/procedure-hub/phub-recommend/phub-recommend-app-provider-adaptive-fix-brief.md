# [backend] 관계 resolved/prior 최종 답 보존

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 기존 미커밋 코드를 이어간다. 기준 HEAD `078ac99`.

프로필 레포 `orchestration/work/phub-recommend/review-app-provider-adaptive-code.md`의 FAIL/WARN, `app-provider-adaptive-report.md`, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-4/5와 WORK-011 공개 계약 인계를 읽는다.

관계 `resolved.value/field_status/by_direction`와 `prior.ok/basis`를 최종 답에 근거 ID·방향·조건과 함께 보존한다. 단일 모델 답에서 지원되는 관계값을 단순 원문 완전 일치 검증기가 버리지 않도록, 원천 fact ID에 결속된 구조화 relation 문장을 별도로 검증한다. 원문 fallback도 검증된 relation 값은 표현한다. `source_fact_ids`가 여럿이면 모두 수집·인용된 경우에만 그 값이 지원되며, 분할에서 서로 다른 part로 갈라져도 완료로 위장하지 않는다. 필요하면 해당 source들을 같은 part에 묶거나 최종 병합에서 ID 전체를 검증해 결합한다. 출처가 부족한 값은 유보하고 의료 사실을 추정하지 않는다.

단일 호출 resolved 간격/순서, 역방향 prior, 두 source가 다른 part로 갈라짐, 일부 source 실패, Q139 전역과 R8 관계, 기존 부분 답·안전 flags·ID 완전성 음성 시험을 추가한다. CLI 오류 문구와 timing WARN은 실물 검증 전 한계로 정확히 기록하고, 확실하게 고칠 수 있는 코드 결함만 수정한다. 기본 cap 미설정의 적응형 호출·retrieval 분리 유지.

실물 서버·DB·provider·50/239×3 평가는 실행하지 않는다. 관련/전체 pytest, ruff, diff check. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-provider-adaptive-fix-report.md`. 완료 시 `worker_done` 한 번.
