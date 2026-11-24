# [reviewer_doc] SPEC-006 4차 검수 — 고침 3 확인

맥락이 없으면 먼저 읽어라: 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-review-doc-brief.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-2-instructions.md`(코디 정정) · 네 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-3-report.md` · planner 고침 3 지시서 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/planner-fix-3-instructions.md`(코디 방향 — **SPEC 은 조건 C1 ~ C4 만 계약으로 적고 함수 · 잠금 · transaction 설계는 WORK 몫**) · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (고치지 마라)

## 볼 것
1. F3-1 · F3-2 · W3-1 ~ W3-3 이 C1 ~ C4 로 닫혔는지(행별)
2. C1 ~ C4 가 본문 전체(흐름 · 케이스 · Rule 7 · OQ-R23 · OQ-R28)에서 일관한지 · 「못 지키는 곳」 사실 줄(emr_kos_keys.py:50-57 · :81-128 · emr_sync.py:243 · emr_sale_sync.py:74-77 · :187-194 · :355-367)을 코드로 확인
3. **설계를 SPEC 에서 요구하지 마라** — 「어떻게 지킬지 SPEC 에 없다」는 FAIL 이 아니다(WORK 몫). 조건이 서로 모순이거나 지킬 수 없는 조건만 FAIL
4. 이번 고침이 새로 만든 모순만 FAIL. 앞 판에서 PASS 한 곳을 새로 뒤지지 마라
5. 판정 FAIL / WARN / PASS

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-4-report.md` 1개만. 완료 보고는 preamble 의 taskId · dispatchId 로.
