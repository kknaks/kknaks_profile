# [backend] case3 분할 경로 검수 FAIL 수정

너는 앱 코드 수정 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 앱 worktree `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 기존 미커밋 작업을 이어간다. 기준 HEAD `078ac99`.

프로필 레포 `orchestration/work/phub-recommend/review-app-walk-phase-a-code-v4.md`의 FAIL/WARN, SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5를 읽는다.

우선 수정: (1) 분할 성공 분기에서도 전체 지원 facet, 필수 안전 flags, 미완료 facet/관계 WP-4 유보를 보존하고 최종 합성을 검증한다. 같은 target의 다른 section fact가 앞 묶음에서 소비돼 출력에서 빠지지 않도록 한다. (2) 각 CLI/SDK part의 error/refusal/stop/빈 결과를 확인해 실패 facet은 incomplete로 남기고 성공 부분만 답한다. 실패를 원문 fallback으로 완료 위장하지 않는다. (3) 답 문장/인용의 target_key·facet·owner·scope를 원장의 지원 관계와 대조한다. 같은 section을 묻는 두 대상, 반복/전치/공통 facet의 회귀 시험을 추가한다. (4) CLI 합성 timing의 보강 필드를 유지한다.

기본 `walk_coverage_mode=False`, 관계 WP-4 미구현 경계 유지. 실물 서버·DB·provider·50/239×3 평가는 실행하지 않는다. 최소 회귀 시험, 관련/전체 pytest, ruff, diff check를 실행하고 미확인 운영 한도/TTFT를 보고한다. 코드·시험만 수정하며 커밋·push·PR 금지. 보고 파일은 프로필 레포 `orchestration/work/phub-recommend/app-walk-phase-a-fix4-report.md`. 완료 시 `worker_done` 한 번.
