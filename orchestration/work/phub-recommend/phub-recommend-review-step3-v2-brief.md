# [reviewer] 실버 3단계 재검수 v2 — v1 지적 수정 · 끝 조건 open 0

너는 v1 을 검수한 reviewer 다(read-only · 산출 리포트 1개). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
- 기준: `orchestration/work/phub-recommend/review-step3-report.md`(F1~F5 · W1~W7 · 다시 돌릴 때 순서) · 지시 `phub-recommend-step3-fix-brief.md`(코디 기본값)
- 대상: `step3-lexicon.json`(새) · `step3-decisions.json` v2 · `step3-apply.py` · `step3-sites.json` · `.md` · `step3-source-fix.md`
- 볼 것: F1 표 50회가 행으로 잡혔는지 + **v1 과 같은 독립 재추출을 다시**(새 사전 밖 잔여 0 인지 — 워커가 잔여 검사로 6문자열 더 찾았다고 보고: dorsum · 측두의 · 입을 크게 벌리 · 입냄새 · hair · 손으로 · 머리 높여 — 행선지 맞는지) · F2 근거 약(워커는 하관 키를 [하관, 하관] 으로 넣음 — 맞는지) · F3 16행 · F4 · F5 · W1~W7 · **구조**: 새 원천 문자열이 결정 파일 한 줄로 닫히는지 사본에서 시험(결정 1 빼면 open 1 · 원천 사본에 부위 문장 하나 넣으면 open 으로 나오는지) · open 0 · 결정론 · 회귀(v1 PASS 항목)
- 산출 `orchestration/work/phub-recommend/review-step3-v2-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_a7ff6cee-c0d1-4402-b300-3e7f44fcb55c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 3단계 재검수 v2 <판정>" \
  --body "open N / FAIL N / WARN N / v1 지적 닫힘 N/12"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 3단계 재검수 v2 <판정>. 상세는 인박스." --enter
```
