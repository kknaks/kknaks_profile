# 리뷰 리포트 — prod-deploy-re1 / code 5 · Delivery #245 W3 방 옮기기 목록 상태 (2026-11-11)

범위(코디 지정): 방 옮기기 목록(E53) 「비어 있음」 / 「배정됨」 — `services/board_rules.py` 의 `ROOM_TAKEN_STEPS` · `room_takers` · `rooms_view`(+ 스냅샷 `rooms` 한 줄) ·
`templates/partials/board_parts.html` `room_pop` · `routers/kit_board.py` 견본 · 시험. **범위 밖**: 같은 파일의 W4 · W5(`home_room` · emr · `services/board.py`) · 차트 모달 미커밋.
근거: SPEC-002 개정 ⑱ :44 ① · U-15 :335 · E53 :164 · 스냅샷 :597 · OQ-51 :932 · fe-2-report.md.

## 판정: PASS

FAIL 0 · WARN 0 · 참고 3.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra" backend/tests/day/board/test_board_rules.py backend/tests/day/web/test_board_page.py backend/tests/architecture` | **145 passed** |
| `uv run ruff check` (`board_rules.py` · `kit_board.py` · 두 시험 파일) | All checks passed |
| `room_pop` diff 의 인라인 스크립트 · `style=` | 0건 |

infra 는 사용자 포트 · 프로세스 금지라 안 돌림(이 변경은 DB 를 새로 읽지 않는다 — 이미 읽은 world 값으로 계산).

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| 배정됨 = 판 카드 | PASS | `board_rules.py:27` `ROOM_TAKEN_STEPS = BOARD_STEPS(procedure_waiting · procedure) ∪ …` · `:592-597` `visit.room_id` |
| 점유로 잡은 방 | PASS | `:595` `hold_room(v)` = 살아 있는 「방 배정」의 방 ≠ 카드 방(`:567-578` · 취소 행 안 봄) — 스펙 :335 「점유로 잡은 방(살아 있는 「방 배정」의 방)」 그대로 |
| 접수 단계인데 방 있음 | PASS | `RECEPTION` 포함 · `room is not None` 일 때만 |
| 귀가 대기 | PASS | `PROCEDURE_DONE` 포함 |
| 같은 고객 다른 방문 | PASS | 고객으로 거르지 않음 — 방문 단위로 그대로 셈(시험 `same_customer`) |
| 넣지 않은 것 | PASS | 상담 · 귀가(`completed`) · 예약 단계는 안 셈 — OQ-51 미결 그대로(:932 「사용자 결정은 … 까지」). 지운 방문은 world 에 없음(`queries/board.py:105` `deleted_at is None`) · 오늘 방문만(`reserved_start_at` 범위) = 「오늘 다른 방문」 |
| 자기 자신 제외 | PASS | 템플릿 `board_parts.html:313-315` — `takenBy` 에서 `card.visitId` 를 뺀 뒤 판정(카드마다 다르므로 화면 몫 — 서버 값은 방문 id 목록). 카드 지금 방은 `here` 로 목록에서 뺌(기존) |
| 순서 | PASS | 서버 `rooms_view` = `w.rooms`(`room.order`) 순 → `sorted(key=bool(takenBy))`(안정 정렬) = 빈 방 먼저 · 묶음 안 `room.order`. 화면도 free → taken 으로 다시 묶고 각 묶음 안 서버 순서 |
| 배정됨도 고름 | PASS | 줄 마크업이 묶음과 상관없이 같은 `<input type="radio" name="roomId">`(disabled 없음) · `hx-params="mode,roomId"` 그대로 · 서버 이동 규칙(규칙 28 「점유 중인 방도 된다」)은 손대지 않음 |
| 글자 둘만 | PASS | 「비어 있음」(기존 원장 목록 글자) · 「배정됨」(`test_screen_copy.py` 근거 = SPEC-002 U-15 · E53 개정 ⑱). 침대 수 · (n/m) · 묶음 머리 줄 없음(머리 줄은 OQ-51 미결 — 안 둠) · 마크업 = 원장 목록 `day-opt__status[ is-free]` |
| 스냅샷 · API 번짐 | PASS | 스냅샷 `rooms[]` = `{id, title, takenBy}` — 스펙 :597 「+ 배정됨 여부 · 칸 이름은 구현 PR」 · 순서 「빈 방 먼저 → 배정됨」과 같다. 스냅샷은 앱 · SSE 에도 같은 dict 이지만 앱(`app/lib`)은 `rooms` 를 읽지 않음(grep — `chat_api` 의 rooms 는 채팅 방) · 웹에서 `snapshot.rooms` 를 읽는 곳은 `room_pop` 하나. `takenBy` 는 같은 스냅샷에 이미 있는 방문 id 뿐(새 정보 노출 없음) · 방문 id 를 `str(id)` 순으로 넣어 스냅샷이 매번 같은 모양(바뀜 비교에 흔들림 없음) |
| 견본(kit_board) | PASS | 빈 방 「시술실 E」 하나 추가 — 가짜 값 견본 화면 전용 |
| 시험 | PASS(+참고) | 규칙: 판 카드 · 점유 방 · 접수 · 귀가 대기 · 같은 방 다른 방문 = 셈 / 상담 · 귀가 · 예약 = 안 셈 / 순서(`test_board_rules.py` `test_방_옮기기_목록은_배정됨_방문을_싣고_빈_방_먼저`). 웹: 팝오버 줄 순서 · 글자 · `is-free` · 라디오 수 |

## 「조용히 통과하는 자리」 · 참고

- 참고 1(시험 공백): 「자기 자신 제외」 분기(`takenBy|reject("equalto", card.visitId)`)를 직접 걸어 보는 시험이 없다. 지금 규칙에서는 자기 방문이 `takenBy` 에 들 수 있는 방이 카드 지금 방(`here` 로 이미 빠짐)뿐이고, 점유 중인 카드는 [복귀하기]만 그려 목록이 없어서 실제로 이 분기가 결과를 바꾸는 경우가 없다 — 그래서 시험이 초록이어도 이 분기가 깨진 것을 모른다. OQ-51 로 단계가 늘거나 `here` 계산이 바뀌면 의미가 생긴다. 권고: 카드 방이 없는(room None) 카드 + 그 카드가 `takenBy` 에 든 방 하나로 「비어 있음」을 단언하는 웹 시험 한 개.
- 참고 2(순서 가장자리): 위 분기가 실제로 걸리면 「자기 자신만 있던 방」은 빈 방 묶음 **끝**에 붙는다(서버가 이미 배정됨 쪽에 정렬해 둔 것을 화면이 free 쪽으로 옮김) — 묶음 안 `room.order` 가 어긋날 수 있다. 지금은 위 이유로 생기지 않음. 고치려면 화면에서 free/taken 을 가른 뒤 `room.order`(서버 원래 순서 = `w.rooms`) 기준으로 다시 정렬하거나, 서버가 `order` 를 함께 싣는다.
- 참고 3(범위 밖 · 정보): SPEC-002 :320 은 차트 담당자 직군을 「이름 오른쪽」으로 적는데, 차트 모달 구현(fe-1 수정 1)은 「이름 앞」이다. 차트 모달은 리뷰 끝난 범위라 코디 판단에 맡긴다(스펙 문구 · 구현 중 하나).

## 범위 밖 관찰

- fe-2 리포트 이슈 1: fe 워커가 `ruff format backend/day` 를 한 번 돌려 backend 워커의 emr 파일이 바깥에서 포맷됐을 수 있다 — backend 워커에 알리는 것은 코디 몫. 이 리뷰는 emr 파일을 보지 않았다.
- 워크트리에 `app/store/` · `app/tool/store_capture/` 미추적 폴더가 있다(이 범위와 무관).
