# [reviewer] SPEC-005 · WORK-003 재검수 v2 — v1 지적 수정분 (read-only · 짧게)
(맥락: 내가 쓴 `review-spec005-report.md` · 수정 지시 `phub-recommend-spec005-fix-brief.md`)
- F-1 ~ F-5 · W-1 ~ W-9 가 실물 기준으로 고쳐졌나(실물 칸 · 셈 · 가드 식을 다시 스크립트로) · F-5 는 코디 판단 ①(기존 고민 mode 그대로 · menu 별도 후보 · I-01 은 concern · site 만)대로인가
- 고치면서 새로 생긴 어긋남 · 결정표에 없는 새 결정이 있나 · 새 열린 것 O-4 가 정말 결정표 밖인가
- v1 PASS 항목 회귀 없나
- 산출 `review-spec005-v2-report.md` · 맨 위 PASS/FAIL + 「open = N」 · 가상 문장 금지
## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_985b2783-a884-4f3f-8c78-49992113369e --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer 완료: SPEC-005 재검수 v2" --body "PASS|FAIL · FAIL N · WARN N · open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] reviewer 완료 — SPEC-005 재검수 v2. 상세는 인박스." --enter
```
