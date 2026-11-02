# [researcher] 추가 지시 — 후납 수납 뒤 「수납 필요」가 꺼지나

앞 판 `reservation-postpay-report.md` 에 이어진다. **⚠ 코디 핸들 바뀜 — 보고 · 질문은 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**. 데모 assert · 운영 키 금지. **KOS 쓰기 0건**(HAR 해석 + 조회).

## 1. 무엇을 하나

앞 판에서 결제 뒤 옵션만으로 추가한 작업이 `paymentRequired: true`(「수납 필요」)였다. 사용자가 그 작업을 KOS 에서 **수납한 장면**을 떴다 — 사용자: 「(수납 필요가) 없어지는 것 같다」. 확인한다.

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/수납필요 확인.har` (249항목). 코디가 본 쓰기: #13 `schedule/socket/v1/commands/issue-schedule-socket-token` → #215 initialize-purchase → #216 add-pending-purchase-items → #217 register-purchase → #237 add-transaction → #238 accept-purchase
- **KOS 요청 전부 세어** 인벤토리(조회가 많다 — 같은 경로는 묶어 횟수로)

## 3. 할 일

1. 수납 5건이 그 추가 작업과 어떻게 이어지나(`add-pending-purchase-items` 의 항목이 작업의 옵션 · 시술권을 가리키나 · 작업에 시술권이 붙나)
2. **「수납 필요」가 언제 꺼지나** — HAR 응답의 작업 `paymentRequired` 를 순서대로(어느 호출 뒤 false) + 지금 데모 같은 일정 조회로 최종 확인. 작업 `ticketId` 등 같이 바뀐 필드
3. `issue-schedule-socket-token` — KOS 웹이 일정 변경을 **소켓**으로 받는 것으로 보인다. 소켓 주소 · 이벤트 모양(HAR 에 websocket 항목이 있으면). ccc 가 10초 조회 대신 쓸 수 있는 실시간 원천인지(결정 말고 사실만)
4. 이 결과로 정산 상자 「수납 필요 N건」 · [귀가 완료] 꺼짐 규칙이 KOS 값만으로 되나
5. 「정할 것」 Q-118 부터

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-postpay-check-report.md`

값 금지(모양만).
