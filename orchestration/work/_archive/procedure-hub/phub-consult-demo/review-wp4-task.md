# [reviewer · 읽기만] WP-3 고침 재검수 + WP-4 코드 검수 (11-20)

너는 WP-3 을 검수한 워커다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(미커밋). 정본 `$W/SPEC-010-consult-myeongdong.md` 0.2.7.
1. **WP-3 고침:** `$W/review-wp3.md` P1 1 · P2 5 가 닫혔나(`$W/wp3-fix-task.md` 코디 판단 — 허브 오류 턴은 목록 · 조건 · 주제 그대로 · 주제 한도는 화면 · LLM · 되돌림 모두 · test_t17) · `$W/wp3-fix-report.md`.
2. **WP-4:** §4-5 모달 · §8 그림 · §13 WP-4 행 · `$W/wp4-report.md` · 스크린숏 `$W/wp4-shots/` · 그림 자리 = 허브 레포 `assets/procedure-images/images/`(코디 G1 판단). 계약 · 시험 · 실물 허브(18105 GET) 대조 · 그림 빠짐 0 · 0.4 회귀.
시험은 WP-3 · WP-4 관련만(전체 금지). **수정 0 · 리포트 1 개** · 18222 손대지 마라.

산출 `$W/review-wp4.md`: 판정(WP-3 고침 · WP-4 각각) · 지적.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e9e9922f-2211-43e5-bd97-3403b59f0b99 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: WP-3 고침 · WP-4" --body "판정 / 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review WP-4 완료 — <한 줄>. 상세는 인박스." --enter
```
