# [reviewer_doc] SPEC-006 3차 검수 — 고침 2 확인

맥락이 없으면 먼저 읽어라:
- 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-review-doc-brief.md` · 2차 지시서 `…/day-reservation/review-doc-2-instructions.md`(코디 정정 — 조회 때 KOS 호출은 FAIL 아님)
- 네 리포트 `…/day-reservation/review-doc-1-report.md` · `review-doc-2-report.md`
- **결정 파일(갱신 — R26 · R27)** `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`
- planner 고침 2 지시서 `…/day-reservation/planner-fix-2-instructions.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (고치지 마라)

## 볼 것
1. F2-1 · W2-1 ~ W2-5 가 닫혔는지(행별)
2. R26(일정 → KOS 키 보충 → 구매 · 시술권 · 카드) · R27(날짜 잠금 · 받는 중이면 사본) 반영 — 본문 전체 일관 · 코드 줄(tasks/emr.py:71-112 · mapper_kos_keys.py:281-286 · sync_schedules.py:506 등) 직접 확인
3. 새 OQ-R28 — 기본안이 본문에 결정처럼 섞였는지 · 그룹 빈 카드가 빠지는 순서가 남아 있지 않은지(R20 전제)
4. 이번 고침으로 새로 생긴 모순만 FAIL. 1 · 2차에서 이미 PASS 한 곳을 새로 뒤지지 마라
5. 판정 FAIL / WARN / PASS

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-3-report.md` 1개만. 완료 보고는 preamble 의 taskId · dispatchId 로.
