# be-4 — #245 W6 후속 (b) · 반영 대기 쓰기가 있으면 [복귀하기] 끔

워크트리 `prod-deploy-re1` · 커밋 안 함(변경만 남김). 근거: review-code-8-report.md 「판정 — 엇갈림」.

## 고친 것

`backend/day/services/board_rules.py` `room_return_block` 한 곳만 바꿨다. 검사 순서:

1. 판에 없음 → `visit_not_on_board`(그대로)
2. 점유 아님 → `room_not_held`(그대로)
3. **그 방문에 반영 대기(`pending` · `sent`) 쓰기 있음 → `conflict`(새로 추가)**

- 반영 대기 방문은 `BoardWorld.reflecting` 을 쓴다. `load_world` 가 이미 outbox `pending`·`sent`·지우지 않은 행으로
  만들고 있고, 스냅샷 `reflecting` 도 같은 값이다. 그래서 판 GET · 조작 응답 · 신호 뒤 스냅샷 어디서
  계산해도 같은 판정이다. `canReturnRoom` = `room_return_block is None` 이고 서버 `room_return` 도 같은 함수로
  거절한다(409).
- 연쇄 길(follow `sent`)과 일정 조회 길(follow `pending`)을 둘 다 닫는다. 확인 · failed · 취소로 반영
  대기가 끝나면 다시 켜진다.
- 새 코드 · 새 문구는 없다. 기존 `conflict` 는 기존 공용 토스트를 쓴다. 화면은 지금처럼 버튼을 그리지 않는다.
- 범위 밖은 건드리지 않았다: (a) absent 확인 · 다른 버튼(`canMoveRoom` · `canHoldMove`) · 웹 템플릿 · 문구 · 주기.
  board_rules.py 의 rooms 쪽도 그대로다.

주의(코디 판단용): 조건은 브리프대로 「그 방문의 반영 대기 쓰기 전부」다. 그래서 점유 이동과 상관없는 쓰기(예:
차트 글 · 단계)가 반영 대기여도 그동안(보통 다음 발송 · 조회까지 몇 초) [복귀하기]가 꺼진다.

## 시험

- 새 시험 `test_board_room_chain.py::test_연쇄_도중_반영_대기면_복귀는_꺼지고_확인_뒤_켜진다`:
  - 가짜 KOS 가 follow(`change-tasks-room`)를 보내는 순간 판 카드를 읽는다.
  - 그때 띠는 보이고(W6), `reflecting = true`, `canReturnRoom = false` 이다. 서버 `room-return` 도 409 `conflict` 다.
  - 연쇄 확인 뒤에는 `reflecting = false`, `canReturnRoom = true` 다.
- `test_board_room_api.py` 기존 시험 두 개를 늘렸다. 복귀 단언(쓰기 · 방 · 확인 · 지운 행 판정)은 그대로다.
  - `test_방배정이_없으면_만들고_다음_조회_뒤_원래_방에_둔다`(일정 조회 길): follow 가 pending 이면
    `canReturnRoom = false` 다. 확인으로 바꾸면 true 가 된다. 원래 끝 단언은 「true」였다. 바로 이 엇갈림 경우라 false 로 바꾸고,
    확인 뒤 true 를 덧붙였다.
  - `test_점유_이동은_방배정만_남기고_완료까지_새_방_복귀는_취소와_원래_방`:
    - 이 시험은 점유 이동 쓰기가 pending 인 채로 복귀를 눌렀다. 지금은 그때 `canReturnRoom = false` 이고 복귀는
      409 `conflict` 다. 그다음 점유 이동 쓰기를 확인으로 바꾸면 true 가 되고, 이후 복귀 흐름은 원래 단언 그대로 통과한다.
- 음성 확인: 새 조건을 끈 채로 돌리면 위 3개가 실패한다. 확인한 뒤 원래대로 돌렸다.

검증: 격리 스택(`day-be245` · 11142/11143)에서 관련 파일만 1회 돌렸다(test_board_room_api · test_board_room_chain ·
test_board_rules · test_room_move_chain_rules · test_room_move_chain · test_board_api · tests/architecture).
결과는 **168 passed**. `uv run ruff check backend` 통과, 바꾼 파일 format 통과. 스택은 `down -v` 했다.
11040 · `day-local` 은 건드리지 않았다. 데모 실물은 하지 않았다(코디 지시).

## 워크트리 변경(커밋 안 함 · be-3 포함)

- `backend/day/emr/sync.py` · `backend/day/services/emr_sync.py` — be-3(W6)
- `backend/day/services/board_rules.py` — 이번(be-4)
- `backend/tests/day/board/test_board_room_chain.py`(새 파일 · be-3 + 이번 시험 1개)
- `backend/tests/day/board/test_board_room_api.py` — 이번
