# [backend] 분할 관계 part 검증·인용 trace 수정

너는 앱 코드 수정 워커다. Orca dispatch preamble 완료 보고를 따른다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 기존 미커밋 코드를 이어간다. 기준 HEAD `078ac99`.

프로필 레포 `orchestration/work/phub-recommend/review-app-provider-adaptive-code-v2.md` 전체, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-4/5를 읽는다.

이전 FAIL: 관계의 모든 `source_fact_ids`가 한 분할 part에 들어간 경우, 검증된 정본 관계 문장/원문+관계 문장을 잘못 거절하지 않는다. part 검증에 그 part의 `relation_resolved/prior` 구조를 전달하고, ID 완전성은 문장별 인용 허용과 기대 **집합**으로 대조한다. 정본 관계 문장에 동일 source ID가 원문 문장과 함께 다시 등장해도 증거 중복으로 실패시키지 않는다. 반대로 위조 값·ID·쌍·방향·조건은 차단한다. 한 part 완전 관계, relation-only, 원문+관계, 여러 part 성공/일부 실패 시험을 넣는다.

모든 최종 반환 경로(분할 성공·일부 실패·원문 fallback·단일 호출)의 `answer_citations`를 실제 최종 답의 인용 ID로 일관되게 기록한다. 기존 cap 미설정 호출, context 재시도, 비용 합산, 안전 flags/유보, WP-4 출처 검증 유지. CLI 실물 오류 문구·timing WARN은 아직 실물 관문으로 명시한다.

실물 서버·DB·provider·50/239×3 평가는 실행하지 않는다. 관련/전체 pytest, ruff, diff check. 코드·시험만 수정, 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-provider-adaptive-fix2-report.md`. 완료 시 `worker_done` 한 번.
