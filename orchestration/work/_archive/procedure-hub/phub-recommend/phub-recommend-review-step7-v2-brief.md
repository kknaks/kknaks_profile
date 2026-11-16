# [reviewer] 실버 7단계 재검수 v2 — v1 지적 수정분 · 지금 원천 기준만

read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`. (맥락 없으면 `review-step7-report.md` 부터)
- 기준: `orchestration/work/phub-recommend/review-step7-report.md` F1 · F2 · W1~W4 · 지시 `phub-recommend-step7-fix-brief.md`
- 볼 것: F1 대응표 249 **전수** — 자동(human_check false) 행은 전부 원천 말 == 대상 이름(정규화)인지 · 사람 확인 88 · F2 엣지 523 **전수** — 단위 시술 부위 ∈ 앵커 부위(또는 하위) · 바디 CC 9 · 두피 CC 5 · apply 의 부위 검사 가드 · W1 표시 · source-fix 24 · W2 통일(계열 후보 전부 + no_unit_at_site) · W3 ambiguous · W4 기록 · open 0 · 결정론(5 · 7) · 고정 시험 · 스킬 점검 4종 · 회귀(v1 「확인한 것」)
- **가상 문장 · 미래 원천은 보지 않는다.** 지적은 지금 데이터에 실제로 있는 것만
- 산출 `orchestration/work/phub-recommend/review-step7-v2-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_3edd26c3-db5a-4f5d-b572-ea1855280c19 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 7단계 재검수 v2 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 7단계 재검수 v2 <판정>. 상세는 인박스." --enter
```
