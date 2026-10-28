# [researcher] 추가 지시 — 후납(시술 중 추가 시술 → 수납 필요) 

앞 판 `reservation-payment-discharge-report.md` 에 이어진다. 보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**. 데모 테넌트 assert · 운영 키 금지. **이번 판 KOS 쓰기 0건**(HAR 해석 + 조회).

## 1. 무엇을 하나

사용자(2026-10-26): 「**후납** = 결제를 다 하고 시술에 들어갔는데 **추가 시술**을 하는 경우」. KOS 화면에는 그때 **「수납 필요」**가 뜬다. 사용자가 데모에서 그 과정을 HAR 로 떴다.

시안: 예약 상세 정산 상자 「전체 · 결제 · 후납」(후납이 남으면 빨강 + [수납하기 ›] · [귀가 완료] 꺼짐) · 원내 현황 카드 Badge 「수납 필요」 · 금액 3칸. 앞 판 결론: 「후납」 KOS 필드 없음 · 「전체 − 결제」는 계산(Q-105) · `paymentRequired` 가 바뀌는 때를 못 봤음(Q-106).

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/수납필요 추가.har` (120항목). 코디가 본 쓰기: 수납 1회(#12 initialize → #13 add-pending-items → #15 register-purchase → #31 add-transaction → #33 accept) → 수납 2회(#57 · #58 · #59 · #78 · #80 같은 순서) → #85 `schedule/v1/commands/add-flow-tasks` → #108 `add-flow-tasks`
- **KOS 요청 전부 세어** 인벤토리(순서 · 본문 키 · 응답)
- 앞 판 리포트 · workflow-v2 「1. 시작 상태」(`paymentRequired` · 「수납 필요」)

## 3. 할 일

1. 장면 복원: 두 수납이 각각 무엇(첫 결제 · 추가 결제?) · 두 `add-flow-tasks` 가 어떤 작업(type · title · 수납 항목/시술권과 연결 · `paymentRequired` 값)을 더하나 · 순서상 「수납 필요」가 어느 시점에 켜지고 꺼지나
2. **「수납 필요」의 원천**: 작업 `paymentRequired` 인가 · 수납 `status` 인가 · 둘 다인가. 결제 전에 추가된 작업 ↔ 결제 뒤 추가된 작업의 차이. HAR 응답 + 지금 데모 같은 일정 **조회**로 확인
3. **후납 금액을 KOS 값으로 알 수 있나**: 수납이 여러 건(`purchaseIds[]`)일 때 「전체 · 결제」 합 · 미결제 수납(`PENDING` 등)이 있나 · 작업에 가격이 붙나. 계산 없이 KOS 가 주는 값이 있으면 그것, 없으면 「계산 필요」로
4. 시술 현황판(카드 「수납 필요」)과 같은 규칙인지 — `procedure/back` 이 지금 무엇으로 「수납 필요」를 판정하는지(코드 레포 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/back` read-only grep)와 비교
5. 「정할 것」 Q-111 부터 — 결정하지 마라

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-postpay-report.md`

리포트에 id · 토큰 · 이름 · 금액 실제 값 금지(모양 · 통화만).
