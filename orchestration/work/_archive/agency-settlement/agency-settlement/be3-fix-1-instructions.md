# backend 3판 수정 1 — code r3 F-1 · W-2

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r3-report.md` F-1 · W-2 · NOTE 를 읽어라.
1. **F-1** — 리포트 고침안대로: 품목이 다른(확정) 달에 고정된 수납(pinned_elsewhere)이 이 달에 취소 + 다른 금액 재승인되면 **이 달 실결제 = 이 달 paymentsNet**(settle() 한 갈래 · 응답 · 엑셀 · 에이전시 합 같은 값). 리포트의 탐침 꼴 그대로 시험(9월 X + 10월 = KOS 최종)
2. **W-2** — 반영 판정 기준 시각 = ② 를 받은 직후 시각(받기 시작 시각 아님). 시험 1
3. 묶음 정렬은 back 이 정한다(지금 그대로). 응답 계약은 바꾸지 마라
- 8800 · back/data · back/.env 건드리지 마라 · 운영 KOS 0 · `uv run ruff check . && uv run pytest -q` · 원 브리프(WP-BE3) §9 두 채널 · subject 「backend 3판 수정 1 완료」
