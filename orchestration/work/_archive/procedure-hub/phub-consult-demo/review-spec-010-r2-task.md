# [reviewer · 읽기만] SPEC-010 0.1.1 재검수 (11-20)

너는 SPEC-010 0.1.0 을 검수한 워커다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앞 검수 `$W/review-spec-010.md` · 고침 지시 `$W/spec-010-fix1-task.md`(코디 결정: P0-1 = reach 「케이스 직접」 만 · P1-1 = 허브 WP-H). `$W/SPEC-010-consult-myeongdong.md` 0.1.1 을 앞 지적 18 개 하나씩 닫혔나 대조하고(실측 필요한 것은 허브 18105 GET · JSON 다시 셈), 고치며 새로 생긴 구멍을 본다. 앞 검수와 같은 기준 · 같은 범위(리포트 1 개만 · 다른 파일 수정 0).

산출 `$W/review-spec-010-r2.md`: 판정(PASS / FAIL) · 지적별 닫힘 표 · 새 지적(P0 / P1 / P2).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_dbc58c9f-06a3-4337-9ad3-b1f7102f121a --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-010 r2" --body "판정 / 닫힘 / 새 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review r2 완료 — <한 줄>. 상세는 인박스." --enter
```
