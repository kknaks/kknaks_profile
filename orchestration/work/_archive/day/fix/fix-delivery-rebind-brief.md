# [planner] Delivery #241 baseline 재결속 (v6) — SPEC-000 stable 머지 뒤

너는 day planner 워커(같은 터미널)다.

사실(코디 2026-11-11): 스펙 PR **mediness#930(DAY-SPEC-000 `stable`) → main 스쿼시 머지** `caf7f3ebb3eafc525c08ee056fe047f4a4051eb1`. 스펙 워크트리는 `git fetch origin` 뒤 `origin/main` 으로 읽는다(파일 수정 금지).

## 할 것

1. 네 계획(`spec-stable-report.md` #241 단계 1)대로 **재결속 v6** — 같은 key `day/fix-device-feedback-interpret` · `contract_version 6` · `spec_baseline_revision = caf7f3eb…` · 결과 계약 v5 그대로(보관 request `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/delivery/fix.v6.request.json` 의 revision 만 새 SHA 로) → `--plan` 으로 `missing_target_specs = []` · `plan_digest` 가 v5 승인(`sha256:3fb28dfc…7288`)과 같은지 확인 → 같으면 `--apply`. **digest 가 다르거나 baseline 이 ready 가 안 되면 적용하지 말고 보고**한다.
2. 적용 뒤 라벨 · baseline 상태 · next_action 을 재조회한다.
3. **review-delivery 는 하지 않는다**(수용 항목 A7 · A11 · A14 = 사용자 실기기 몫이 미확인 — 어떻게 닫을지 사용자가 정하는 중). 2차 Delivery(#234 · #235 · #236 · #239)는 건드리지 않는다.

파일 수정 · 커밋 · push · MCP Task 카드 금지. 쓴 request · 결과 파일은 `…/work/fix/delivery/` 에도 복사해 둔다(네 scratchpad 는 곧 사라진다).

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/delivery-rebind-report.md` — 라벨 · baseline · contract_version · plan_digest · next_action.

끝나면 두 명령 모두(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: <한 줄>" --body "baseline / 라벨 / digest / next_action"
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
