# [reviewer] 실버 2단계 재검수 v3 — v2 WARN 3 수정분만

너는 v1 · v2 를 검수한 reviewer 다(read-only · 산출 리포트 1개). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
- 기준: `orchestration/work/phub-recommend/review-step2-v2-report.md` W-1~W-3 · `_RESUME.md` §2 10-28 「2단계 재검수 v2 PASS 뒤 WARN 3 처리」 행 · 지시 `phub-recommend-step2-fix2-brief.md`
- 볼 것(수정분만): M8 하위가 매질 한 축인지(방식 칸 0) · 재배치 20행 · null 18행 각각 근거가 원천 · 허가 · 모델명에 실제로 있는지(추정 0) · 광원 2종 14행 기준 일관 · technique_hint 25 = 적힌 말 그대로 · M7 synonyms 에 품목명 0 · open 40 · 결정론 · 회귀(v2 PASS 항목 · 352 셈 · 다른 계열 행이 바뀌지 않았는지 v2 시점과 비교 — v2 시점 사본이 없으면 step2-apply.py 의 git 이전 상태 대신 리포트 기록값과 대조)
- 산출 `orchestration/work/phub-recommend/review-step2-v3-report.md` · 맨 위 PASS/FAIL

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_e935d4d1-c970-4194-b5ff-68be7a928cc5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 2단계 재검수 v3 <판정>" \
  --body "v2 WARN 닫힘 N/3 / 새 지적 N / 회귀 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 2단계 재검수 v3 <판정>. 상세는 인박스." --enter
```
