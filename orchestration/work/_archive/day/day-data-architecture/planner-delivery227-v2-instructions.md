# [planner] Delivery #227 로그인 재계약(contract v2) — DAY-SPEC-001 을 target 으로

너는 day planner 다. 앞서 #224 ~ #227 Delivery 를 만든 방식(`/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/delivery/v2-login*.json` · mediness `start-delivery` 스킬)을 그대로 쓴다. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`(mediness · PR #909 · 미커밋 SPEC-002 변경이 있다 — **건드리지 마라**).

## 왜

#227 은 DAY-SPEC-001(로그인 · 세션 · 2026-11-05 사용자 결정)이 있기 전에 만들어져 target 이 SPEC-000 뿐이고 계약 문구가 SPEC-001 과 어긋난다(예: 「2단계 인증 — 하지 않음」 → SPEC-001 은 「막고 안내」 · 오류 코드 · 웹 쿠키 + 앱 Bearer · CSRF · 만료 = KOS 토큰 만료 · 임시 토큰 5분 · KOS 401 → `expires_at` 당김).

## 할 일

1. `delivery/v2-login.json` 을 contract v2 로: target_specs 에 **DAY-SPEC-001** 추가 · `target_delta` · `acceptance` · `non_goals` · `review_surface` 를 SPEC-001 본문(경로 4 · 오류 매트릭스 · Functional Rule · 상태도)에 맞게 · `scope_delta` 에 무엇이 바뀌었는지 · 위험 L3 유지 · `spec_baseline` 은 아직 pending(PR #909 미머지).
2. 스킬 절차대로 plan → apply 로 **Issue #227 본문을 갱신**(같은 idempotency key · contract_version 2). 새 Issue 를 만들지 마라. Delivery 계획 **승인은 하지 마라** — 승인은 사용자 몫(`delivery-plan:review` 그대로).
3. 이미 PR #228 브랜치에 있는 것과 겹치는 자리(#226 의 KOS client sign-in · 브라우저 헤더 · `external_session` 모델 · 암호화)는 「이미 있음 — 재사용」으로 계약에 적는다.
4. SPEC-001 에 없는 것을 계약에 넣지 마라.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery227-v2-report.md` — 바뀐 계약 항목(전 → 후) · plan_digest · Issue 갱신 확인(링크). 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` 둘 다).
