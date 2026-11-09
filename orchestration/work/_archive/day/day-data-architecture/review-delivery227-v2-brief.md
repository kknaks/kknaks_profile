# [reviewer · WP] Delivery #227 로그인 contract v2 검수

너는 day reviewer(문서) 다. **읽기 전용** — Issue · 파일 수정 금지 · Delivery 승인 금지. 산출물은 리포트 1개.
대상: GitHub Issue #227 본문(`gh issue view 227 -R MediSolveAIDev/CENTURION_DAY`) · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/delivery/v2-login.json`(+ plan/apply) · 작성 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery227-v2-report.md` · 작성 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-delivery227-v2-instructions.md`.
기준: DAY-SPEC-001 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-001-login-session.md`(정본) · SPEC-000 04 · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md` 「로그인 · 세션 계약」 · PR #228 브랜치에 이미 있는 코드(`/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — `backend/day/emr/kos/` · `backend/common/crypto.py` · 모델 `login_session` · `external_session` · `account` · `staff`).

볼 것:
1. 계약(Target Delta · Acceptance A1 ~ A10 · Non-Goals)이 SPEC-001 의 경로 4 · 오류 매트릭스 · Functional Rule · 상태도 · 만료 규칙과 **빠짐 · 더함 없이** 맞나. SPEC-001 에 없는 것을 계약에 넣었나.
2. Acceptance 가 **검증 가능한 문장**인가(무엇을 어떻게 확인하면 통과인지) · 실물 1회(데모 지점 계정 로그인) 조건이 있나.
3. 「이미 있음 — 재사용」이 실제 코드와 맞나(파일 확인).
4. 작성 리포트가 남긴 것: CSRF 실패 오류 코드가 SPEC-001 에 없음 — SPEC-002 fix1 이 「CSRF 실패 403」으로 적었다(`/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-002-procedure-board.md` 에서 grep). 둘이 맞으려면 어디를 고쳐야 하나 판정.
5. Issue 제목이 v1 그대로인 것 — 문제인지.
6. 위험 L3 · 승인 대기 상태가 맞나(승인 라벨이 붙지 않았나).

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery227-v2-report.md` — 판정 · 지적(계약 항목 ↔ SPEC-001 줄) · 고칠 방향. 완료는 preamble 의 worker_done 절차대로(둘 다).
