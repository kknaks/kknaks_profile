# planner 0.4.3 — 구현 뒤 동기(코드가 정본)

코드 PR kknaksss/agency-settlement#1 이 올라갔다. 그 사이 코드에서 정해진 것을 SPEC · WORK 에 맞춘다(새 정책 만들지 마라):
- code r3 F-1 · W-1 · W-2(`review-code-r3-report.md`) · backend 수정 1 · 2(_RESUME §2 마지막 줄 「달을 모두 더하면 KOS 최종」 · 이 달 취소가 있으면 이 달 살아 있는 승인도 더함 · pinned_elsewhere 갈래 · 반영 기준 = ② 받은 직후 · repaidAfterCancel 로그)
- front: 묶음 차례 = back 응답 차례 · 「앞 달 결제 취소」 머리 결제일 칸 글자 · itemsNowhere 안 숨김 · 폭 1600
- r2 W-1 · r4 W-3 · r5 등 남은 SPEC 문구 정리 · OQ 상태 갱신(OQ-132 = 코디 추천안 · 사용자 답 대기 · OQ-136 = 시안 v3 안 만듦)
- WORK-001 3판 WP 상태 = 완료(LIVE3 실물 숫자: 10월 ⚠ 0 · 9월 ⚠ 1 = 8월 승인의 9월 취소 꼴 · 확정 달 KOS 0) · 코드 PR 링크
- 실제 금액 · 이름 · 수납 id 금지(public). 판 0.4.3 · 원 브리프 §9 두 채널(같은 task/dispatch) · subject 「planner 0.4.3 완료」
