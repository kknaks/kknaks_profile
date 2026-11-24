# [reviewer · 읽기만] WP-6 코드 검수 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(미커밋). 정본 `$W/SPEC-010-consult-myeongdong.md` 0.2.7(§7 · R1 ~ R11 · §4-4 · §13 WP-6 행) · `$W/wp6-report.md` · `$W/wp6-shots/`. 볼 것: 블록 계약 · 가격은 JSON 값만 · 허브 근거만 · 답 규칙 시험 · 채팅 그림 · 실물 시나리오 6 턴(리포트 · 장부)에서 규칙 어긴 곳 · 0.4 회귀. 특히 6 턴 「보톡스 시술 원리가 뭐야?」 가 LLM return(t1) 을 규칙 new 가 이겨 **새 주제 t3** 이 된 것 · 5 턴 「같이 받아도 돼요?」 가 장바구니 쌍을 못 잡은 것 — 원인(코드 · 스펙)과 고칠 방향. 시험은 WP-6 관련만. **수정 0 · 리포트 1 개** · 18222 손대지 마라.
산출 `$W/review-wp6.md`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e9e9922f-2211-43e5-bd97-3403b59f0b99 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: WP-6" --body "판정 / 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review WP-6 완료 — <한 줄>. 상세는 인박스." --enter
```
