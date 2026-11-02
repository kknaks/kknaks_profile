# 단계별 이동 — KOS 그대로 (E2E batch 5 #1) 결과 보고

## 상태: done

지시 `reservation-move-stage-instructions.md` · 브랜치 `kknaksss/overall-board-2` · 커밋 안 함 · front 안 고침 · 포트 안 띄움(앱 안에서 실행 · 임시 DB).

## 1. 데모 실호출 (2026-10-27)

- 시작 전 assert(값 출력 없음): `KOS_TENANT_ID` == 데모 HAR 경로 테넌트 → OK · `.env` · 환경에 `KOS_API_tenent`(운영) 없음 → OK · `PROC_FAKE_BOARD` 꺼짐 · DB = 스크래치 임시 파일
- 이동 = **ccc 이동 코드 그대로**(`ReservationService.move` → 내부 `schedule/reservation/v2/commands/update-reservation{scheduleId, occupiedResources{items}}`). 시험 스크립트 안에서만 `draggable` 막기를 풀었다(KOS 가 무엇을 받는지 보려고)
- 일정: 데모에 그 단계 일정이 없어 **새로 만들었다** — 2026-11-12 KST · 그룹 「국내」 · 10:00 부터 30분 간격 10개 · 시험 고객 10명(가상 이름 `[ccc 시험] 이동 NN` · 생년월일만) · 예약 메모 `[ccc 시험] 단계별 이동 …`. 단계 올리기 = 공개 `change-flow-step` · 취소 · 부도 = 공개 `cancel-reservation`
- 같은 그룹 이동 = 원래 시각 **+4시간**(빈 칸) → 원래 시각으로 되돌림. 되돌림은 끝난 뒤 KOS 를 다시 읽어 **모든 일정이 원래 시각 · 원래 그룹인 것을 확인했다**(아래 「확인」 칸)

| 단계 | flowStep · status(이동 때) | 이동 응답 | 바뀐 필드(이동 직후 상세 비교) | 되돌림 |
|---|---|---|---|---|
| 예약 | `RESERVED` · `RESERVED` | **200** | `occupiedResources`(시각) · `reservation.startDateTime` · `endDateTime` 만 | 200 · 확인 |
| 접수 | `RECEPTION` · `IN_PROGRESS` | **200** | 시각 · 묶음만 · flowStep 그대로 · 작업 수 그대로 | 200 · 확인 |
| 상담 대기 | `CONSULTATION_WAITING` · `IN_PROGRESS` | **200** | 시각 · 묶음만 | 200 · 확인 |
| 상담 중 | `CONSULTATION` · `IN_PROGRESS` | **200** | `occupiedResources` 만 | 200 · 확인 |
| 시술 대기 | — | **미확인** | 만들 수 없음: `change-flow-step PROCEDURE_WAITING` → 400 `procedures:NotFound`(공개 · 내부 둘 다 — 시술 작업이 있어야 한다 · 수납 쓰기는 허가 밖). 데모의 우리 표식 일정(앞뒤 14일 · 191건) 중에도 시술 대기 0건 | — |
| 시술 중 | `PROCEDURE` · `IN_PROGRESS`(**지난 날짜** 일정 — 아래) | **200** | — | 200 · 확인 |
| 귀가 대기 | `PROCEDURE_DONE` · `IN_PROGRESS` | **200** | 시각 · 묶음만 | 200 · 확인 |
| 귀가 완료 | `COMPLETED` · `COMPLETED` | **200** | 시각 · 묶음만 | 200 · 확인 |
| 취소 | `RESERVED` · `CANCELED` | **200** | 시각 · 묶음만 · status 그대로 | 200 · 확인 |
| 부도 | `RESERVED` · `NO_SHOW` | **200** | 시각 · 묶음만 · status 그대로 | 200 · 확인 |
| **다른 칸(그룹)** — 예약 단계 일정 · 「국내」 → 「중화권」 같은 시각 | `RESERVED` | **200** | `occupiedResources[0].reservationGroup.reservationGroupId` · `reservation.reservationGroupId` 만 | 200 · 확인 |
| **지난 날짜** — 5일 전 · 우리 표식(`[ccc 데모`) 일정 · +1시간 | `PROCEDURE` · `IN_PROGRESS` | **200**(지난 날도 받는다) | — | 200 · 확인 |

- **KOS 가 단계 때문에 이동을 거절한 경우는 없었다.** 9 단계 · 그룹 이동 · 지난 날짜 모두 200. 바뀐 것은 시각 · 그룹(묶음 · `reservation.start/endDateTime` · `reservationGroupId`)뿐 — **flowStep · status · 작업 · 방 · 상담은 그대로**(상세 전후 비교에서 그 키는 안 나옴)
- 반영 지연: 되돌림 직후 읽기에 이전 시각 · 그룹이 보인 경우가 있었다(7건) → 3초 뒤 다시 읽어 모두 원래 값 확인(KOS 쓰기 뒤 0 ~ 3초 · SPEC §4.3 와 같음)
- 곁에서 본 것(이동 아님): 미래 날짜 일정에 내부 `recept` = 400(접수는 당일만으로 보임) · 공개 `change-flow-step` 은 `RESERVED → RECEPTION` · `→ CONSULTATION_WAITING` · `CONSULTATION → PROCEDURE_DONE` 를 받았다 · 내부 `change-flow-step RECEPTION` = 400 `step:NotAvailable`
- 접수 단계는 앞 조사(`reservation-move-cancel-report.md` — HAR)에서도 200 이었다

## 2. 코드

| 파일 | 바뀜 |
|---|---|
| `procedure/back/app/domain/reservation_rules.py` | `draggable(main)` = `DRAG_MAINS`(예약 · 접수 · 상담 · 시술 · 귀가 · 취소 · 부도 — **KOS 가 받은 단계 전부**). 근거 주석. 주 상태(main)만으로 충분해서 sub · flowStep 은 받지 않는다(KOS 가 단계로 가르지 않았다) |
| `procedure/back/app/service/fake_reservations.py` | 가짜 board 도 같은 `draggable()` |
| `procedure/back/app/service/reservations.py` | 안 바뀜 — 이동 API 의 같은 검사(`if not draggable(main): 409 not_movable`)가 같은 함수를 써서 규칙이 따라온다(검사 자리는 남김) |
| `procedure/back/tests/test_resv_write.py` | `test_move_not_movable_and_reception_movable` → `test_move_every_stage_kos_accepts`(9 단계 parametrize · 카드 `draggable` · 같은 `update-reservation` 본문) + `test_move_unknown_main_not_movable`(막는 규칙이면 KOS 안 부르고 409 — 검사 자리) |
| `procedure/back/tests/test_resv_board.py` | 카드 `draggable` 기대값 — 취소 · 부도 · 상담도 true |

- **front 확인(안 고침)**: 스케줄 표는 `card.draggable` 만 본다(`ScheduleTable.tsx` `canDrag = card.draggable && !preview`). 하나 — `app/(main)/reservations/live/page.tsx` `withMoves` 가 화면이 미리 바꾼 상태(`states` · 조작 직후 낙관 표시)가 있는 카드는 `draggable: false` 로 덮는다(다음 board 까지 잠깐). 의도된 동작으로 보이며 이번 지시와 부딪히지 않는다

## 검증

- `cd procedure/back && uv run ruff check . && uv run pytest -q` → **All checks passed · 361 passed**(경고 1 · 기존)

## 남긴 데모 흔적 (데모 테넌트 — 값 · id · 이름 없음)

1. **시험 고객 10명**(새 내원객 · 가상 이름 `[ccc 시험] 이동 01 ~ 10` · 생년월일 · 국적 KR · 연락처 없음)
2. **2026-11-12 KST 「국내」 일정 10개**(10:00 ~ 15:00 · 30분 · 메모 `[ccc 시험] 단계별 이동 2026-11-12 · <단계>`) — 지금 상태: `RESERVED` 3 · `RECEPTION` 1 · `CONSULTATION_WAITING` 1 · `CONSULTATION` 1 · `PROCEDURE_DONE` 1 · `COMPLETED` 1 · `CANCELED` 1 · `NO_SHOW` 1. **모두 원래 시각 · 원래 그룹**(이동 → 되돌림 확인)
3. 지난 날짜(5일 전) 우리 표식 데모 일정 1개 — +1시간 이동 → 되돌림(원래 시각 확인) · 수정 시각만 바뀜
4. 실패한 쓰기(상태 안 바뀜): `recept` 400 × 5 · `change-flow-step PROCEDURE_WAITING/PROCEDURE` 400 · 내부 `change-flow-step RECEPTION` 400
- 지우기 · 정리는 하지 않았다(허가 = 이동만). 진행 단계 일정은 공개 취소로 지울 수 없다(접수 이후 — kos-demo-patients 규칙 4). 정리 여부는 코디 판단. scheduleId 목록은 워커 스크래치(`move_probe_ids.json`)에만 있다

## 이슈 · 코디가 확인할 것

1. **시술 대기 = 미확인인데 연다** — 데모에서 만들 수 없었다(`procedures:NotFound`). 앞뒤 단계(상담 중 · 시술 중 · 귀가 대기)가 모두 받고 KOS 가 단계로 막은 곳이 하나도 없어 연다. 막아야 하면 `DRAG_MAINS` 는 main 단위라 sub 를 받도록 한 줄 더하면 된다
2. **취소 · 부도 · 귀가 완료 카드도 끌린다**(KOS 가 받음 · 지시 「KOS 가 받은 단계 = 끌 수 있음」). SPEC-005 §5.4 「드래그할 수 있는 카드 = reserved · reception(OQ-714)」 줄은 planner 가 고쳐야 한다
3. 지난 날짜 이동도 KOS 가 받는다 — ccc 는 같은 날 안에서만 옮기므로(§5.4) 지난 날 표에서도 끌 수 있다. 막을지는 SPEC 몫
4. `not_movable` 은 지금 규칙으로는 나올 일이 없다(코드 · 오류 코드는 남김)
