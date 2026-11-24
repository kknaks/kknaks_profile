# [spec] SPEC-011 0.1.2 — 재검수 지적 고침 (자동 · 11-23)

앞 발주 `fetch-plan-spec-task.md` 규칙 그대로. 재검수 `$W/review-spec-011-r2.md`(FAIL · 새 P1 1 · P2 4). `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`

## 코디 결정(다시 묻지 마라)
- **P1-5 = (가) G2b 를 뺀다.** 44b2 T2 빠짐은 Jev 시대(`kinds_by=jev`) 장부 줄이라 지금 앱에서 생기지 않는 시대 차이로 적는다. FR1 의 F20 은 「Jev 시대 장부라 대상 칸 없음 — 지금 시대에서는 FR1 고민」 으로.
- 모든 셈을 **시대로 나눈다**(Jev 시대 · understand 시대 · default) — 지금 시대 수가 머리 수.

## 할 일
- P1-5 · P2-10 ~ P2-13 을 리포트 「고칠 방향」 대로 `SPEC-011-fetch-plan.md` 0.1.2 · `fetch-plan-report.md` 에 반영. 수치는 다시 돌린 스크립트 출력에서.
- P2-11: WP-1 · WP-2 완료 조건에 「11-23 이후 새 장부 턴(맞추는 데 안 쓴 것) 빠짐 0」 — 새 턴은 코드 워커가 실물 3 대화(03b8 · ecc6 · 73bd) 재생으로 만든다고 적기.
- 「바뀐 것」 표 갱신.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d43f5cc1-116b-4ab6-8810-a4c6f8f31f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-011 0.1.2" --body "지적 처리 / 지금 시대 표본 · 밖 감소 · 빠짐"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-011 0.1.2 완료 — <한 줄>. 상세는 인박스." --enter
```
