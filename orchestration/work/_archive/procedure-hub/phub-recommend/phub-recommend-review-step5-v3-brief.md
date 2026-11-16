# [reviewer] 실버 5단계 재검수 v3 — v2 F1 수정분 · 지금 원천 기준만

read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`. (맥락 없으면 `review-step5-report.md` · `-v2-report.md` 부터)
- 기준: `review-step5-v2-report.md` F1 「닫는 결정」 · 지시 `phub-recommend-step5-fix4-brief.md` + 코디 추가 지시(1단계 출처가 목적 · 기법을 채우면 단위 시술 0 이 아니어도 그 키에 잇기 — 제모 U5-100 · 101 · 병변 U5-131)
- 볼 것: 상속 1227쌍 전수에서 **기법 근거 없는 쌍 0** · **출처로 더한 44쌍이 출처 문구(technique_compat.product_evidence)로 실제 받쳐지는지 전수**(리팟 · 슬렌더엑스 제외 이유 포함) · M5 확인 불가 출처 처리 · 추천 가능 제품 중 단위 시술 0 = 진단 장비 2 + 예외 3(미라셀 · 셀엑소좀 · 스마트자이드 — 원천 질문)뿐인지 · open 0 · 결정론 · 회귀(v2 PASS 항목)
- **가상 문장 · 미래 원천은 보지 않는다.** 지적은 지금 데이터에 실제로 있는 것만
- 산출 `orchestration/work/phub-recommend/review-step5-v3-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_c2ab8181-2cce-47df-98ec-3002575b6ff0 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 5단계 재검수 v3 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 5단계 재검수 v3 <판정>. 상세는 인박스." --enter
```
