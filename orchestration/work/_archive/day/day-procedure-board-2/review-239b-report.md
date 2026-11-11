# 재리뷰 리포트 — day-procedure-board-2 / code — CENTURION_DAY#239 리뷰 반영 (W1 · W2 · W3) (2026-11-11)

대상: 코드 워크트리 미커밋 전부(HEAD f1e67a2c 위 · 앞 리뷰 뒤 바뀐 것 중심 — 앞 diff 와 줄 비교 346줄). 지시 `fix-239-brief.md` · 앞 리포트 `review-239-report.md`.
파일 경로는 `backend/` 기준.

## 판정: PASS (WARN 2 · 낮음)

W1 · W2 · W3 이 사용자 결정(2026-11-11)대로 닫혔다.
- 카드가 원래 방으로 되돌아가는 경로는, 보통 흐름에서는 더 없다.
- 설정이 비면 「점유 이동」은 꺼진다.
- 「방 배정」 이름을 못 구하면 공용 토스트와 함께 거절한다.

남은 WARN 2 는 KOS 가 거절하거나 계획을 못 만드는 드문 실패 경로의 표시 문제다.

검증: `DAY_ENV_FILE=…/local.env scripts/test.sh -q` 결과는 아래 「테스트」 절(직접 1회).

## 앞 지적 닫힘

### W1 — 「방 배정」 없는 점유 이동 순서 · 카드 방 계산 (닫힘)
- **순서**: `services/board.py` `room_move` — 「방 배정」이 없으면 KOS 에는 `add-flow-tasks` **하나만** 쌓는다(`_room_assign_create` · 옮길 sequence · 새 방 외부 id 를 `expect` 에 실음). 확인된 조회에서 `follow_room_assign` 이 ① 새 「방 배정」 → 원래 방 ② 나머지(`moving`) → 새 방을 **차례로** 쌓는다(같은 조작 · 같은 보낼 직원). 결과적으로 KOS 배정 시각도 「방 배정(원래 방) → 나머지(새 방)」 순이다.
- **만드는 중 guard**: `emr/sync.py` `guard_of` — `room_assign_added` expect 의 `moving` sequence 에 `room` guard 를 건다. 그래서 확인 전 조회가 DAY 가 이미 옮긴 작업 방 · `visit.room_id`(hold_room)를 KOS 옛 값으로 덮지 않는다. 확인과 follow 가 같은 transaction 이라 guard 가 끊기는 틈도 없다(follow 의 ② op 이 같은 칸을 지킨다). `room_move_block` 은 「만드는 중」(`room_assign_creating`)을 `room_held` 로 막는다.
- **카드 방 계산**: `emr/sync.py` `card_room_of` · `with_card_room`(1330 ~ 1365) — 설정 id 가 있으면 「방 배정」을 뺀 방 붙은 작업 중 배정 시각이 가장 늦은 작업의 방. 「방 배정」 말고 방 붙은 작업이 없으면(접수만 된 고객) mapper 값(「방 배정」 방) 그대로. 설정이 없으면 지금 규칙 그대로. `apply_schedules` 가 모든 일정에 적용한다(834).
- 경로별 대조:
  | 경로 | 결과 |
  |---|---|
  | 「방 배정」 없는 점유 이동 | 확인 뒤 ①(방 배정 → A) ②(나머지 → F). 카드 = 「방 배정」을 뺀 가장 늦은 = F. 점유(방 배정 A ≠ 카드 F) 유지 — **앞 W1 의 되돌아감 없음** |
  | 「방 배정」 있는 점유 이동 | 나머지만 F · 카드 F(방 배정 제외 계산이라 「방 배정」 시각과 무관) |
  | 이동 | 전부 F · 카드 F |
  | 복귀 | 「방 배정」 취소 + 나머지 A · 카드 A |
  | KOS 웹에서 「방 배정」만 다시 배정 | 카드 계산에서 빠져 흔들리지 않음 |
  | 접수만 된 고객(「방 배정」만 방 있음) | `card_room_of` None → mapper 값 = 「방 배정」 방 — 카드 방이 생김 |
- 테스트:
  - `tests/day/emr/test_kos_board_contract.py:440-451`: `card_room_of` · `with_card_room` — 옮긴 뒤 · 「방 배정」만 · 설정 없음.
  - `tests/day/board/test_board_room_api.py::test_방배정이_없으면_만들고_다음_조회_뒤_원래_방에_둔다`(275 ~): add 하나 → 확인 → follow 두 op 순서.

### W2 — 설정이 비었을 때 (닫힘)
- `board_rules.can_hold_move`(602) — 이동 막힘이 없고 「남길 「방 배정」이 있거나 설정 id 가 있을 때」만 true. 스냅샷 `cards[].canHoldMove`(789). 템플릿 `partials/board_parts.html:315-316` 은 `canHoldMove` 가 아니면 「점유 이동」 버튼에 켜는 표시를 달지 않아 늘 꺼져 있다.
- `room_assign_unset` 코드는 코드 · 테스트 어디에도 없다(grep 0). 서버 거절은 기존 기본 코드 `conflict`(`errors.py:98` `BoardConflict` 기본값)이고, 토스트는 MESSAGES 폴백 「요청이 올바르지 않습니다」 — 새 글자 · 새 코드 없음.
- 테스트 `test_방배정이_없고_설정도_비면_점유_이동은_꺼지고_서버도_거절`.

### W3 — 「방 배정」 이름 · 외부 id 를 못 구할 때 (닫힘)
- `_room_assign_create` — 설정 id · 연결 · 일정 id · 원래 방 / 새 방 외부 id · 이름 중 하나라도 없으면 409 `conflict`. 이 검사가 DAY 값을 바꾸기 **전**에 있어(room_move 앞부분), 조용히 「이동」으로 끝나지 않는다.
- 테스트 `test_방배정_이름을_못_구하면_점유_이동은_거절`.

## WARN

### W1'. (낮음) 확인 뒤 follow 계획을 못 만들면 아무 표시 없이 되돌아간다
- `follow_room_assign` — `planner.plan` 이 `WriteNotSupportedError` 면 로그(info)만 남기고 끝난다. 이때 add op 은 이미 확인돼 guard 가 풀린다. 그래서 다음 조회가 DAY 가 옮겨 둔 작업 방을 KOS 값(원래 방)으로 되돌린다. 실패 토스트(`kos_failed`)도 없다.
- `_room_assign_create` 가 만들 때 외부 id 를 다 검사하므로, 실제로는 KOS 쪽 계획 규칙(열린 경로 · 값)이 바뀔 때만 생긴다 — 낮음. `outbox.failed` 처럼 event_log 를 남기거나 실패 토스트를 내면 「조용히」가 사라진다.

### W2'. (낮음) 방 이동 거절 글자는 여전히 비움 — 화면이 막는 경우만 남음
- `room_held` · `room_same` · `room_not_held` · `visit_not_on_board` 는 OQ-48 대로 토스트를 비운다(`test_웹_방_이동은_누른_카드와_OOB_거절_글자는_비움`). 화면은 각각 「점유 중이면 [복귀하기]만」 · 「지금 방 뺌」 · 「띠가 있을 때만 [복귀하기]」로 버튼을 막는다. 그래서 낡은 화면에서 누를 때만 아무 표시 없이 안 된다. 스펙 OQ-48 결정 대기라 그대로 둬도 된다.

## 회귀 · 조용히 통과
- 「방 배정」이 있는 점유 이동 · 이동 · 복귀의 op 순서와 테스트는 앞 판 그대로다(`test_점유_이동은_…` · `test_이동은_…` · 복귀).
- 차트 · 「방 배정」 판정 · 결정 (가)는 이번 diff 에서 바뀌지 않았다.
- 카드 방 규칙 변경이 설정 id 가 있는 병원의 모든 카드에 적용된다. 「방 배정」 말고 방 붙은 작업이 있으면 그 방이 카드 방이다. 보통 시술 작업은 호출 1단계(`change-tasks-room` = 카드 방)로 방이 붙으므로 결과는 같다. 앞 판과 다른 결과가 나는 것은 「방 배정」이 가장 늦게 배정된 경우뿐이다(= 고치려던 경우).
- 앞 리뷰 W4(완료 시술 집도의)는 사용자 확인으로 해소(KOS 상태 안 바뀜) — 코드 변경 없음, 맞음.

## 테스트
- `DAY_ENV_FILE=…/local.env scripts/test.sh -q` → **946 passed**(1 warning · 72초 · 실패 0).
- `uv run ruff check backend scripts` → All checks passed.
