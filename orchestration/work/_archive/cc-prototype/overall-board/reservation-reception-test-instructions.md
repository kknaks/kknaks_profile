# [researcher] 추가 지시 — 접수 묶음 데모 실호출 시험 (**데모 쓰기 허가됨**)

앞 판 `reservation-room-report.md` 에 이어지는 판이다. 완료 보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**.

## 0. 허가 범위 — 이번 판만 예외

사용자(2026-10-26): **「데모 지점은 테스트 해봐도 돼」.** 이번 판은 **데모 테넌트(`KOS_API_tenent_dev` · procedure `.env` 의 시스템 계정)에 한해** 아래 §2 의 쓰기를 허가한다.
- 운영 명동점 키(`KOS_API_tenent`) 절대 금지 — 호출 전에 테넌트가 앞 판들의 데모 값과 같은지 확인
- §2 에 없는 쓰기(고객 수정 · 결제 · 시술 추가 · 완료 · 취소 등)는 여전히 금지. 필요하면 먼저 질문
- ⚠ 같은 데모 4층을 시술 현황판 E2E 가 보고 있을 수 있다. **시험 일정을 시술 대기(`PROCEDURE_WAITING`)로 두지 마라**(시술 현황 카드가 생긴다). 끝 상태는 상담 대기 또는 접수

## 1. 무엇을 확인하나

사용자 확인(2026-10-26): 코디 목표 = 「고객이 오면 방 배정」. KOS 화면은 방 지정 화면이 시술 대기만 보여서 **접수 → 방 배정 작업 추가 → 시술 대기로 올림 → 방 지정 → 상담 대기로 되돌림**으로 우회한다. ccc 는 그 우회 없이 **[접수 완료] 한 번**으로 묶으려 한다:

```text
A. recept → add-flow-tasks(「방 배정」 ETCETERA) → (일정 다시 조회로 sequence 확인) → change-tasks-room(그 작업 · 방) → change-flow-step(CONSULTATION_WAITING)
```

확인할 것 (Q-63 · Q-64 · Q-67 · Q-72)
1. **A 가 시술 대기를 거치지 않고 끝까지 200 인가** — 특히 `change-tasks-room` 이 일정 단계 `RECEPTION` 에서도 받나
2. 각 단계 뒤 일정 상태(조회): flowStep · `reservation.status` · `receptionDateTimeUtc` · tasks[](type · title · status · room · roomAssignedDateTimeUtc)
3. **KOS 웹 화면에 같은 결과로 보이나** — 공개 · 내부 조회로 HAR 의 KOS 우회 결과(앞 판 §3 끝 상태)와 같은 모양인지 비교
4. **B. 공개 `changeFlowStep(RECEPTION)`** 을 다른 예약 일정 하나에: 접수 시각 · `reservation.status`(`IN_PROGRESS`?)까지 바뀌나 → 내부 `recept` 와 차이

## 2. 허가된 쓰기 (이 목록만)

| 시험 | 대상 | 호출 |
|---|---|---|
| A | 오늘(KST) 데모 4층의 **`RESERVED` · 작업 없음** 일정 1건 | 내부 `recept` · `add-flow-tasks` · `change-tasks-room` · `change-flow-step`(CONSULTATION_WAITING) — 본문은 `방배정.har` 와 같은 모양 |
| B | 다른 `RESERVED` 일정 1건 | 공개 `changeFlowStep{scheduleId, step: RECEPTION}` |

- 대상 일정이 없으면: 데모 **기존 고객**으로 내부 `reserve`(본문은 `예약.har` 기존 고객 건과 같은 모양) 로 오늘 일정을 만들어도 된다. 만든 것은 리포트에 「시험용으로 만듦」으로 적는다
- 방은 데모 방 중 **오늘 다른 일정이 쓰지 않는 방**으로
- 각 쓰기는 **1회만**. 실패하면 재시도하지 말고 응답 그대로(값 가려서) 적고 다음으로 넘어가지 말지 판단해 기록
- 시험이 끝난 일정은 **그대로 둔다**(되돌리지 마라). 끝 상태를 적는다

## 3. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-reception-test-report.md` — 리포트 1개

## 4. 리포트

- 호출마다: 순서 · 경로 · 결과 코드 · 바뀐 필드(모양만 · id 값 금지)
- A · B 의 결론 한 줄씩 + KOS 화면 결과와 같은지
- 「정할 것」은 Q-73 부터(결정하지 마라)
- 리포트에 id · 토큰 · 이름 · 방 이름 외 개인 값 금지
