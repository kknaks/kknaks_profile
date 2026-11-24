# [backend · 실물 확인 3] KOS 데모 지점 — 시술권으로 오늘 시술 · 오더 메모 · 시술 대기 · 시술 중 귀가 · 귀가 대기 → 귀가

**앞 판 먼저 읽기**: 같은 폴더 `be-probe-1-instructions.md`(규칙 · 금지 · 보고 방식 — 이번에도 전부 그대로) · `be-probe-1-report.md` · `be-probe-2-instructions.md` · `be-probe-2-report.md`. 스크립트는 `/private/tmp/day-probe-3/`(앞 판 `pcommon.py` 재사용 가능).

**레포 파일 수정 · 커밋 금지. 데모 지점 확인 통과 뒤에만 쓴다.** `~/.config/day/` 금지 · 로컬 스택 · DB · docker 금지 · 값 · 토큰 · 개인정보 출력 금지(키 모양 · O / X · id 앞 8자). 기존 데모 고객 · 예약은 건드리지 마라.

## 1. 왜 (코디 `_RESUME.md` §2 결정)

- 재진 접수: 「시술만 진행」을 켜고 시술 목록에서 「오늘」 체크한 시술권으로 **오늘 시술 작업**을 만들고 **오더 메모**를 저장한 뒤 **[시술 대기]**(`PROCEDURE_WAITING`)
- 시술 대기 · 시술 진행 [귀가 처리] = 안 끝난 시술 작업 취소(`cancel-flow-tasks` CANCEL) → 내부 `change-flow-step {id, COMPLETED}`
- 귀가 대기 [귀가 처리] = 바로 내부 `COMPLETED`

## 2. 근거

- HAR(사용자 · 데모 지점): `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/수납시술추가.har` — 수납(`initialize-purchase` → `add-pending-purchase-items` → `register-purchase` → `add-transaction` → `accept-purchase`) → `get-ticket-bundles` → 시술 작업 `add-flow-tasks`(`type` · `title` · `procedureConfiguration{productOptionConfiguration, ticketConfiguration{ticketId, round{total, current}}, medicalServiceConfiguration}` · `translsMap`). **본문 모양은 이 HAR 을 그대로 따라라**(값만 이번 것으로). HAR 은 파이썬 `-I` 로 JSON 만 읽어라.
- DAY: `backend/day/emr/kos/writes.py`(`CANCEL` · `FLOW_STEP` · `ADD_TASKS` 상수) · `services/board_home.py`(시술 현황 [귀가 대기] = 작업 취소 → `PROCEDURE_DONE`) · `emr/kos/demo/kos_board.py`(구매 · 시술권 경로 · 본문) · 오더 메모 `emr/kos/ext_reads.py:261` 본문 모양(`{scheduleId, orderMemo}`)
- 2 리포트: 접수 · 방 배정 · 방 지정 연쇄 본문 그대로

## 3. 준비 — 시험 고객에게 시술권 만들기

1. 시험 고객 `6b051a9e…`(「박하늘(시험)」)로 **오늘** 예약 X 를 만든다.
2. HAR 순서대로 예약 X 에 **회차 2회 이상**인 시술권 상품 옵션 하나를 수납까지 끝낸다(금액은 데모 상품 그대로 · 결제 수단은 HAR 과 같은 것). → `get-ticket-bundles {visitorId}` 로 새 시술권 묶음 · 시술권 id · 회차 상태 기록.
   - 이 시술권이 「지난 시술권」 역할을 한다. 만들 수 없으면(4xx) 멈추고 보고.

## 4. 시험 (각 단계 = 경로 · 본문 키 모양 · 응답 · 다시 읽기 칸 O / X · 늦게 보이는 칸 몇 초)

**예약 X (시술만 진행 → 시술 대기 → 시술 진행 중 귀가)**
1. 접수 `recept`
2. **시술권으로 오늘 시술 작업 만들기** `add-flow-tasks`(HAR #50 모양 · 3 의 시술권 id · 회차) → 상세 `tasks[]` 에 시술 작업 · `procedureConfiguration.ticketConfiguration.ticketId` O / X · 시술권 회차 상태 변화(`get-ticket-bundles` — `AVAILABLE → IN_USE` 등 KOS 값 그대로)
3. **오더 메모** `schedule/v1/commands/change-order-memo {scheduleId, orderMemo}` → 상세 `orderMemo` O / X
4. 「방 배정」 작업 + 방 지정(2 와 같음) — **시술만 진행에서도 방 배정 작업이 필요한지**: 먼저 방 배정 없이 5 를 해 보고, 400 이면 방 배정 뒤 다시
5. **시술 대기** 내부 `change-flow-step {id, step:"PROCEDURE_WAITING"}` → `flowStep`
6. 시술 진행으로: 내부 `change-flow-step {id, step:"PROCEDURE"}`(DAY 시술 현황 첫 [시작]과 같음)
7. **시술 진행 중 귀가**: ⓐ 먼저 `COMPLETED` 만 보내 보기(400 이면 오류 칸 기록) → ⓑ 안 끝난 작업 전부 `cancel-flow-tasks {reason:"CANCEL"}` → 내부 `COMPLETED` → `flowStep` · 작업 상태 · **시술권 회차 상태가 되돌아가나**(`get-ticket-bundles`) · 수납 필요(`paymentRequired`)가 남은 작업이 있었으면 그것도

**예약 Y (귀가 대기 → 귀가)**
8. 같은 고객 · 오늘 예약 Y → 접수 → 「방 배정」 + 방 지정 → `CONSULTATION_WAITING` → 시술권 남은 회차로 오늘 시술 작업 하나(2 와 같음) → `PROCEDURE` → 작업 완료 `change-tasks-complete {complete:true}` → 남은 「방 배정」 작업 처리(시술 현황 [귀가 대기]와 같게 `cancel-flow-tasks` CANCEL) → `PROCEDURE_DONE`
9. **귀가 대기에서 귀가** 내부 `COMPLETED` → `flowStep` · `reservation.status`

**정리**
10. 남은 시험 예약은 귀가 완료 상태로 끝낸다(접수 뒤 취소는 KOS 가 막음 — 2 리포트). 산 시술권은 그대로 둔다(환불 · 회수 API 를 찾지 마라).

## 5. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-3-report.md` — 맨 위 표(준비 · 시험 1 ~ 10 × 경로 · 응답 · O / X · 비고) → 핵심 결론(ⓐ 시술권 작업 본문 · ⓑ 시술만 진행에 방 배정 필요 여부 · ⓒ 시술 중 귀가 순서와 시술권 회차 · ⓓ 귀가 대기 → 귀가) → 「DAY `writes.py` 에 열 때 필요한 것」(후보 · 결정 아님).

## 6. 완료 보고 — 1 과 같은 두 명령(subject 「backend 완료: KOS 데모 실물 확인 3」) · task-id · dispatch-id 는 이번 dispatch 값. 막히면 `[질문] backend:` 로 코디 터미널에.
