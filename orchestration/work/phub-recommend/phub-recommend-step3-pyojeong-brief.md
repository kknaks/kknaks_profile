# [researcher] 3단계 정본 한 줄 — 「표정근」 행선지

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`. 먼저 `step3-sites.md` · `step3-decisions.json` 구조와 `step4-source-fix.md` 를 읽어라.

`step4-source-fix.md` 「3단계 정본 1」 그대로: `step3-decisions.json` strings 「표정근」을 얼굴 노드 해부학 이름(속성)에서 빼고 deferred 「4단계 대상 근육」(step4 H15 받음)으로. `step3-apply.py` 재실행 → open 0 · 결정론 · 얼굴 노드 anatomical/compound 칸에 표정근 0. 그다음 `step4-apply.py` 재실행(넘김 받음 대조가 그대로 맞는지 · open 0). `step4-source-fix.md` 해당 줄에 「반영됨」 표시. 다른 것은 바꾸지 마라.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_101ef0a8-99f8-49b1-8b3f-6b8bc8c23004 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 3단계 표정근 한 줄" \
  --body "step3 셈 / step4 open / 결정론"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 3단계 표정근 한 줄. 상세는 인박스." --enter
```
