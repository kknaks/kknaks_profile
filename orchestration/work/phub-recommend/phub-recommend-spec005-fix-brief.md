# [planner] SPEC-005 · WORK-003 검수 FAIL 5 · WARN 9 수정

(맥락: `review-spec005-report.md` · 앞 지시 `phub-recommend-spec005-brief.md`)
- 리포트 「고칠 것」 그대로 — **F-1 ~ F-4 · W-1 ~ W-9 전부**(실물 칸 · 실물 셈으로 · 리포트가 적은 실물 근거를 다시 확인해서)
- **F-5 코디 판단 = ①**: 사전의 기존 고민 대상 mode(전부 · 하나 · 후보)는 바꾸지 않는다 · `menu:` 대상은 같은 match 안의 **별도 후보**로 낸다 · §6-1 I-01 경로에 「T1 결과 중 concern · site 만 쓴다(menu 는 I-11 T7 만)」 · I-11 경로에 「질의 말이 라벨이면 menu 후보로 T7」 — 10-30 결정 「고민 id 질의는 그대로」와 같음
- 결정표에 없는 새 결정을 「정해진 것」으로 넣지 말 것(필요하면 §7 열린 것)
- 끝나면 SPEC · WORK 머리에 「검수 반영 2026-10-30(F-1 ~ F-5 · W-1 ~ W-9)」 한 줄

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_d604db9d-e1da-4569-bef7-73441af2e8d8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC-005 검수 수정" --body "FAIL N/5 · WARN N/9 반영 / 열린 것 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] planner 완료 — SPEC-005 검수 수정. 상세는 인박스." --enter
```
