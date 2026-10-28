# [researcher] 추가 지시 — 수납(KOS 화면 딥링크 · 수납 정보 읽기) · 귀가

앞 판 `reservation-consultation-report.md` 에 이어진다. **⚠ 코디 핸들이 다시 바뀌었다 — 보고 · 질문은 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**(옛 `term_0bdf5bdb…` 금지). 데모 테넌트 assert · 운영 키 금지 그대로.

## 1. 무엇을 하나

사용자 결정(2026-10-26):
- 상담 중 시술 · 수납 추가 · 오더 메모 · 수납 · 시술 대기 전환은 **상담사가 KOS 에서 직접**. ccc 는 사본으로 읽기만
- 예약 상세 「귀가 대기」 정산 상자의 **[수납하기 ›] = KOS 수납 화면을 연다**(그 고객 · 그 일정). 결제는 KOS 에서, **수납 정보는 KOS 에서 받아 온다**
- **[귀가 완료] = 데스크가 ccc 에서**

사용자가 데모에서 같은 고객으로 ① 수납 ② 귀가 를 HAR 로 떴다.

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/수납.har` (114항목). 코디가 본 쓰기: #19 `purchase/v1/commands/initialize-purchase` → #21 `add-pending-purchase-items` → #24 `schedule/v1/commands/register-purchase` → #101 `purchase/v1/commands/add-transaction` → #104 `accept-purchase`
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/귀가.har` (19항목). 쓰기: #17 `schedule/v1/commands/change-flow-step`
- **두 파일의 KOS 요청을 전부 세어** 인벤토리. HAR 에 `pages` 가 비어 있다 — 페이지 URL 은 요청의 `Referer` · `Origin` 헤더 · 문서(GET html) 항목에서 찾는다
- 앞 판: `reservation-read-report.md` §3.1 24 · 25행 · §3.4 · Q-15 / workflow-v2 「6. 귀가 대기」 · 「KOS 반영 표」([귀가 대기] = `cancel-flow-tasks` → `PROCEDURE_DONE`) · `changeFlowStep` 거절 조건(`COMPLETED` 로 갈 때 끝나지 않은 시술 → `procedures NotAvailable`)

## 3. 할 일

1. 인벤토리(파일별 · 순서 · 본문 키 · 응답 모양).
2. **딥링크**: KOS 웹 수납 화면 URL 형식 — 경로 · 쿼리에 고객 id · 일정 id · 탭이 들어가나(값은 `{visitorId}` 꼴로). 다른 HAR(`예약.har` · `고객정보 수정.har` · `방배정.har` 등)의 Referer 도 대조해 「고객 상세 › 수납 탭」을 바로 여는 주소가 있나. 로그인 필요 여부
3. **수납 쓰기 5건 해부**(모양만): 무엇이 만들어지고(구매 · 항목 · 거래) 일정과 어떻게 이어지나(`register-purchase` → 일정 `purchaseIds`?) · 작업 `paymentRequired` 가 언제 false 가 되나
4. **수납 정보 읽기 — 데모 조회로 확인**: 그 일정으로 공개 `getPurchaseSummaries` · `getScheduleDetail`(`purchaseIds` · tasks[].paymentRequired) · `getScheduleStatistics`(`optionItemTotalPriceV2` · `paymentTotalAmountV2`) 를 불러, 시안 정산 상자 「전체 금액 · 결제 금액」과 원내 현황 카드 금액 3칸 · 「수납 필요」 Badge 에 무엇을 쓸 수 있나. 「후납」에 해당하는 KOS 값이 정말 없나(미결제 잔액 · 상태)
5. **귀가 해부**: `change-flow-step` 이 어디서 어디로(`PROCEDURE_DONE` → `COMPLETED`?) · 그 전에 남은 작업 취소 같은 호출이 있나 · 처방전(`prescriptionIds`) 관련 호출이 있나. 공개 `changeFlowStep(COMPLETED)` 와 같은가
6. **데모 쓰기 시험(허가 · 1회)**: ccc [귀가 완료] 모양으로 **공개 `changeFlowStep{scheduleId, step: COMPLETED}`** 를 1회. 대상 = 오늘 데모 `PROCEDURE_DONE`(귀가 대기) 일정이 있으면 1건 · 없으면 하지 말고 「대상 없음」(다른 단계에서 억지로 올리지 마라). 전후 조회 비교
7. 「정할 것」 Q-102 부터 — 결정하지 마라

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-payment-discharge-report.md`

리포트에 id · 토큰 · 이름 · 카드 · 금액 실제 값 금지(모양 · 통화만).
