# [reviewer · 읽기만] SPEC-010 WP-3 · D1 · WP-3b 코드 검수 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(미커밋 — `git -C $A status` · `diff`). 정본 `$W/SPEC-010-consult-myeongdong.md` 0.2.7(§5-0 CD · TP1 ~ TP14 · §5-1 ~ §5-4 · §13 WP-3 · WP-3b 행) · 리포트 `$W/wp3-report.md` · `$W/wp3b-report.md` · 코디 판단 D1 (가) = LS 로 막은 칸 값은 주제 칸에서 빼고 장부 `blocked` 에만(스펙 LS3 문구는 곧 고침).

볼 것: 스펙 계약과 코드가 같은가(조건 누적 · 주제 판단 규칙 + 이해 호출 topic 합치기 · 되돌림 · 저장 · 재기동 복원 · reach 케이스 직접만 · 효과 길 · NM · SF · LS · 축 고르기) · 시험이 계약을 막는가 · 실물 표본(허브 18105 GET · 실제 이해 호출은 필요할 때 빈 포트로 한두 번만) · 0.4 회귀 · 장부 가격 0. 시험은 WP-3 · 3b 시험 + 리포트의 회귀 목록만(전체 금지). **수정 0 · 리포트 1 개** · 18222 손대지 마라.

산출 `$W/review-wp3.md`: 판정 · 지적(P0 / P1 / P2 · 파일:줄 · 고칠 방향).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e9e9922f-2211-43e5-bd97-3403b59f0b99 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: WP-3 · 3b" --body "판정 / 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review WP-3 완료 — <한 줄>. 상세는 인박스." --enter
```
