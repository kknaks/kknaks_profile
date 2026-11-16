# [reviewer] 재리뷰 — seed_demo_board.py 반영 1차

너는 앞 리뷰(task_0b8b322c99d1)를 한 day reviewer 워커다. 같은 워크트리 · 같은 규칙(원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/day-procedure-board-2-review-brief.md` §5 · §7 — 읽기만 · KOS 호출 금지 · 커밋 금지).

앞 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-seed-demo-board-report.md`. 반영 지시: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/be-fix1-brief.md`.

## 볼 것
1. F1 · W1 · W2 · W3 · W5 · W6 · W7 · W8 이 지적대로 닫혔나 — 지적마다 닫힘 / 안 닫힘 / 새로 생긴 문제(파일:줄)
2. 고치면서 새로 생긴 「조용히 통과하는 자리」 — 특히 F1 확인이 **모든 쓰기 전** · 테넌트 가드가 **모든 KOS 호출 전**인지, 새 예외 처리(except Exception)가 쓰기 도중의 반쯤 만든 방문을 숨기지 않는지
3. W4(국적 alpha-2)는 사용자 승인 대기 — 판정에서 뺀다
4. pytest backend/tests/scripts · ruff 1회

## 산출물
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review2-seed-demo-board-report.md` 1개 · 판정 FAIL / WARN / PASS. 완료 보고는 원 브리프 §9 두 명령, 코디 핸들 `term_b915fb18-742f-4779-962c-79848020b8d5`.
