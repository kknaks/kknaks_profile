# [reviewer · 읽기만] SPEC-010 WP-2 코드 검수 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(미커밋 — `git -C $A status` · `diff`). 정본 `$W/SPEC-010-consult-myeongdong.md`(§4 화면 · §12 slot · §13 WP-2 행) · 시안 `$W/design-consult-20261120.html` · 리포트 `$W/wp2-report.md` · 스크린숏 `$W/wp2-shots/`.

볼 것: 시안과 같은 마크업 · 클래스 · 문구(시안 밖 문구 0 · slot 빈 자리) · 스펙 계약(얼굴 점 · 몸 목록 · 접기 · 장바구니 드로어 옵션 줄 자리 · 모달 틀 · items 이벤트 · RT1) · 시험이 계약을 막는가 · 0.4 회귀 · 가격 숫자 장부 0. 시험은 `tests/test_v05_page.py` + 리포트의 0.4 관련만(전체 금지) · 화면 확인이 필요하면 빈 포트로 띄우고 끔. **수정 0 · 리포트 1 개** · 18222 손대지 마라.

산출 `$W/review-wp2.md`: 판정 · 지적(P0 / P1 / P2 · 파일:줄 · 고칠 방향).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e9e9922f-2211-43e5-bd97-3403b59f0b99 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: WP-2" --body "판정 / 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review WP-2 완료 — <한 줄>. 상세는 인박스." --enter
```
