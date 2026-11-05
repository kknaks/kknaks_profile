# [reviewer_doc] 재검수 — DAY-SPEC-001 WARN 반영 + SPEC-000 token_hash

너는 day reviewer_doc 워커다(read-only · 리포트 1개 · 커밋 금지). 방법은 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-review-doc-brief.md` 와 같다.

읽을 것: 네 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-report.md`(W1 ~ W4) · **바뀐 원천** `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md`(login_session.token_hash · 「정할 것」 1 닫힘 · 새 절 「로그인 · 세션 계약 (2026-11-05 사용자 결정)」 — 사용자가 W1 ~ W4 를 전부 추천대로 정했다) ·
planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-fix2-report.md`.

대상: 워크트리 미커밋 변경 — `spec-001-login-session.md` · `spec-000-data-model.md`(§3 04 login_session · OQ-04-1 만) · `40-architecture/erd.md`(token_hash 키) · `log.md` · 인덱스.

볼 것: W1 ~ W4 가 원천 새 절대로 풀렸나 · 새로 생긴 발명 · 왜곡(특히 planner 가 해석으로 둔 둘 — 임시 토큰 5분 지난 병원 고르기 오류 코드(「아직 열린 것」에 남김) · KOS 조기 401 → `session_expired` 매핑 — 를 판정) · SPEC-000 다른 표가 바뀌지 않았나(diff) · lint `--strict` 1회.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-2-report.md` — PASS / WARN / FAIL. 완료는 preamble 의 worker_done 절차대로.
