# [planner] SPEC-006 고침 2 — 2차 검수 FAIL 1 · WARN 5 + 새 결정 R26 · R27

맥락이 없으면 먼저 읽어라:
- 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-spec-brief.md` (§5 · §7 · §8 · §9 그대로 — 단 고침 1 지시서의 「코디 정정」 유지)
- 고침 1 지시서 `…/day-reservation/planner-fix-1-instructions.md`
- **결정 파일(갱신 — R26 · R27 추가)** `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`
- 2차 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-2-report.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (네 미커밋 변경 위에서)

## 고칠 것

1. **R26 반영 + F2-1 닫기**: 보는 날짜 최신화 = 오늘 동기화와 같은 범위 — 일정(`run_schedules` 경로) → KOS 키 보충(`tasks/emr.py` `_kos_keys` — `visit.reservation_group_id` 를 채움 · `mapper_kos_keys.py:286`) → 구매 · 시술권 · 카드(`sync_sales_hospital`). §3 조회 흐름 단계 · 코드 근거 줄 · 케이스를 이것으로. **OQ-R25 는 R26 으로 닫는다.** 화면을 그리기 전에 어느 단계까지 기다리는지(예: 일정 + 키 보충까지 기다리고 구매는 뒤따라 오는지)는 사실을 적고 OQ 로 — 단 그룹 칸이 비어 카드가 빠지는 순서는 두지 않는다(R20 전제)
2. **R27 반영**: OQ-R24 닫음 — 날짜를 넣은 잠금을 따로 · 이미 그 날짜를 받는 중이면 기다리지 않고 지금 DB 사본으로 그림
3. W2-1 ~ W2-5 — 리포트의 「고칠 것」 그대로(W2-1 · W2-2 는 사실 + OQ 로 · 결정 아님)
4. `20-spec.md` · `10-decision.md` · `log.md` 개정 표기
5. §8 검증 → §9 완료 보고(preamble 의 taskId · dispatchId)
