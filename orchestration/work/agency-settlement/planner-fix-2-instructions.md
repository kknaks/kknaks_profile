# planner 수정 2판 — SPEC-007 0.1.2 (작은 것 하나)

- ⑤ `getPurchaseSummaries` 추가는 코디 승인(_RESUME §2 새 줄).
- **OQ-904 닫음**: 결제일 칸 = ⑤ `transactions[].paymentDateTime.approvedDateTimeUtc`, 취소 줄 = `canceledDateTimeUtc`(① 행과 ⑤ transaction 을 잇는 키 · 매칭이 안 되면 어떻게 보일지를 §5 · §6 에 적는다 — 근거는 공식 스펙 스키마). `lastUpdatedPaymentDateTimeUtc` 는 쓰지 않는다. 정렬도 이 값. 달 귀속(D-06) 필터는 ① `createdTimeUtc` 그대로인지, 결제일과 다를 때를 OQ 로 남긴다
- §9.1 에 시험 하나 · 판 0.1.2 · public grep 다시. 끝나면 §9 두 채널 보고(subject 「planner 수정 2판 완료」)
