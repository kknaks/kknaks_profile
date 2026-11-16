# [reviewer] 실버 3단계 재검수 v3 — v2 지적 수정 · 끝 조건 open 0

너는 v1 · v2 를 검수한 reviewer 다(read-only · 산출 리포트 1개). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
- 기준: `orchestration/work/phub-recommend/review-step3-v2-report.md` N1 · N2 · W-a · W-b · 지시 `phub-recommend-step3-fix2-brief.md`
- 대상: `step3-lexicon.json` · `step3-decisions.json` · `step3-apply.py` · `step3-fixture-test.py` · `step3-fixtures/cases.json` · `step3-sites.json` · `.md`
- 볼 것: N1(입술 24) · N2 ①~④(새 형태소 · 귓볼 · 등/배 패턴형 허용 · fixture 38 케이스가 v2 T1~T4 를 다 덮는지 + **네가 새 문장 몇 개를 더 만들어 사본에서 시험** — fixture 밖에서도 open 으로 나오는지) · 등 8→11 로 늘어난 3회(등 지방 · 등 마사지)가 맞는 행선지인지 · W-a · W-b 가드 · open 0 · 결정론 · 회귀(v2 PASS 항목 · 셈 519)
- 산출 `orchestration/work/phub-recommend/review-step3-v3-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_a7ff6cee-c0d1-4402-b300-3e7f44fcb55c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 3단계 재검수 v3 <판정>" \
  --body "open N / FAIL N / WARN N / v2 지적 닫힘 N/4"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 3단계 재검수 v3 <판정>. 상세는 인박스." --enter
```
