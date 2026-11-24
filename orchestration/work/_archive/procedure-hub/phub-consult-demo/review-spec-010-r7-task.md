# [reviewer · 읽기만] SPEC-010 0.2.6 재검수 r7 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앞 재검수 `$W/review-spec-010-r6.md` · 고침 지시 `$W/spec-010-fix9-task.md`(코디 판단: 조건 없는 되돌림 표지 규칙 지움 · 머리 누름 · LLM return 만 · TP14 예외 · 이번 턴 조건 = follow 로 채운 대상을 뺀 이해 결과). `$W/SPEC-010-consult-myeongdong.md` 0.2.6 에서 r6 의 P1 3 · P2 7 이 닫혔는지와 새 구멍만 본다(필요하면 실측). 리포트 1 개만 · 다른 파일 수정 0.

산출 `$W/review-spec-010-r7.md`: 판정 · 닫힘 표 · 새 지적.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_08fd3049-0cd7-4e48-9189-d68fbdbb9cef --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-010 r7" --body "판정 / 닫힘 / 새 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review r7 완료 — <한 줄>. 상세는 인박스." --enter
```
