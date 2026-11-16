# [reviewer] 1단계 재검수 — FAIL 반영 확인

너는 1단계를 검수한 reviewer 다(read-only). 1차 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-report.md` 의 지적이 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `step1-decisions.json`(+ .md)에서 닫혔는지 확인하라.
- 지적별 PASS/FAIL · 고치면서 새로 생긴 문제(회귀) · 새로 추가된 15행(taxonomy products[])의 근거와 연결을 1차와 같은 기준으로
- 산출: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-v2-report.md` 1개, 맨 위 PASS/FAIL

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 1단계 재검수 <판정>" \
  --body "지적별 판정 / 회귀 / 남은 것"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] reviewer 완료 — 1단계 재검수 <판정>. 상세는 인박스." --enter
```
