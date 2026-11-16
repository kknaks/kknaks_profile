# [reviewer] 재리뷰 — #239 리뷰 반영(W1 · W2 · W3)

같은 규칙(`review-239-brief.md` — 읽기만 · KOS · 공유 DB 금지 · test.sh 돌려도 됨). 대상: 코드 워크트리 `git diff`(미커밋 전부 — 앞 리뷰 뒤 바뀐 것 중심). 지시 `fix-239-brief.md` · 앞 리포트 `review-239-report.md`.

## 볼 것
1. W1: 「방 배정」 없는 점유 이동 = add-flow-tasks → 확인 → ①방 배정 → 원래 방 ②나머지 → 새 방 순서 · 만드는 중 guard · 카드 방 계산에서 방 배정 뺌(설정 id 있을 때 · 다른 방 붙은 작업 없으면 그대로) — 카드가 원래 방으로 되돌아가는 경로가 남았나 · 기존 방 배정 있는 점유 이동 · 이동 · 복귀 · KOS 웹 재배정 · 접수만 된 고객 카드
2. W2 canHoldMove(설정 비면 꺼짐) · room_assign_unset 삭제 · W3 이름 못 구하면 409 거절(조용히 이동 아님)
3. 회귀 · 조용히 통과하는 자리 · test.sh 946 passed 직접 1회

산출물 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-239b-report.md` · FAIL / WARN / PASS. 완료 보고 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`).
