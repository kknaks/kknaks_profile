# WP3-BE 수정 1 결과 보고 — 검수 FAIL 1 · WARN 4

## 상태: done (커밋하지 않음 · WP3-BE 위 워크트리 변경)

- 근거: `be-wp3-fix1-instructions.md` · `review-wp3-code-report.md` · **계약 고정 문서 §5(갱신)**
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`
- Connect 는 시험에서 대역이다. W-5 는 어댑터를 최소 HTTP 대역(`_ConnectStub`)으로 본다

## 1. 지시 5/5

| # | 고친 것 | 위치 | 시험 |
|---|---|---|---|
| **F-1** | 편집 계약 `values` 에 **`proposed_room_id` · `proposed_room_name`** 을 더했다(제안 없으면 둘 다 null). 이름은 예약 시스템 목록에서 읽고, 없거나 닿지 않으면 null이다. **확정은 draft 의 사람 선택만 따른다**: `merge_meeting_update_draft` 가 제안의 `room` 을 버리고 draft 의 `room` 만 쓴다 → **draft 에 `room` 이 없으면 방을 바꾸지 않는다**. **`room: {keep: true}`** = 「기존 — 변경 안 함」(PATCH 에서도 같은 뜻). `keep` 과 `room_id` 를 함께 주면 422다. `room: {}` 도 422다(`room_id` 또는 `keep` 필수) | 계약 `B/platform/actions.py:2181` 근처(`_meeting_update_edit_contract`) · 이름 조회 `ActionServices.meeting_room_name` `actions.py:205` → `B/bootstrap/application.py:1712`(`_room_name_or_none`) · `:4817` · 겹치기 `B/modules/actions/confirmation.py:225` · `MeetingRoomChoice.keep` + 검증 · `room_choice()` `B/modules/meetings/commands.py:175,236` | `T/contract/test_meeting_room_change.py`: 제안 방이 values 에 실림 / **제안 있음 + `{keep:true}` → 안 바뀜**(다른 제안 칸은 섬) / **`room` 없음 → 안 바뀜** / **제안 그대로 `{room_id:5}` → 이동** / `keep`+`room_id` 422 · PATCH `keep` 은 유지 |
| **W-1** | 결과를 모르는 예약(`needs_verification`)을 두 갈래로 다룬다. ① **외부 번호가 있으면**(결과 모르는 이동·동기화) **쥔 자리**로 본다 — 다음 수정은 같은 외부 예약을 PUT·DELETE 로 다시 맞춘다(결과 확정 · 새 예약 없음). ② **외부 번호가 없으면**(결과 모르는 새 예약) 쥔 자리로도 빈 자리로도 다룰 수 없다 → **방에 닿는 수정**(회의실 선택 · 시각 · 인원 변경)은 **`409 ROOM_RESERVATION_UNCONFIRMED`**로 막는다(message 포함 · `available_rooms` 없음). 제목·목적만 고치는 수정은 막지 않는다. AX 확정·옛 `meeting.update` 도 같은 계획을 타서 똑같이 막힌다 | `_holds_seat` `B/bootstrap/application.py:528`(+`needs_verification`) · `_unconfirmed_seat` `:541` · 가드 `:1241` · 예외 `B/modules/meetings/rooms.py:119` · 409 매핑 `B/entrypoints/http.py:557` · 카드의 「지금 방」 판정도 같은 집합(`actions.py`) | 외부 번호 없는 확인 대기: 방 선택·시각·인원 = 409 + Connect 호출 0 · 제목만 = 200 / 외부 번호 있는 확인 대기: 방 변경 = 같은 예약 PUT(새 예약 없음) → `booked` |
| **W-2** | AX 확정·옛 `meeting.update` 의 **재확인(Connect `rooms`·`available`)을 액션 트랜잭션 밖으로** 뺐다. 계획을 둘로 나눴다 — `_room_plan_intent`(DB 만) · `_recheck_room_plan`(Connect). 트랜잭션 안의 실행(`_plan_room_change_in_action`)은 Connect 를 부르지 않는다. 밖에서 끝낸 재확인이 없으면 `_RoomRecheckNeeded` 를 올린다 → 입구(`run_action_command` · `decide_action`)의 `_run_with_room_recheck` 가 그 트랜잭션이 되돌려진 뒤 **밖에서 재확인**한다(거절이면 409 가 그대로 올라감). 그다음 결과(방 이름)를 열쇠로 들고 **짧은 트랜잭션으로 다시** 돈다. 열쇠는 회의·동작·대상 방·외부 번호·시각·인원이다. 그 사이 회의가 바뀌면 열쇠가 달라 한 번 더 재확인하고, 3회 넘으면 `MeetingStateConflict`. 반영(PUT·POST·DELETE)은 원래처럼 커밋 뒤 훅이다. PATCH 는 원래 밖에서 계획했다(같은 두 함수) | `B/bootstrap/application.py:575,585`(신호 · 열쇠 저장소 ContextVar) · `:1217,1258,1273,1296,1317` · 입구 `:3871` · `:4748` | AX 확정에서 Connect 목록 조회가 **언제나 트랜잭션 밖**(실행 함수 안팎 추적) · 옛 `meeting.update` 의 409 를 낸 가용 조회가 밖에서 정확히 1회 |
| **W-3** | AI 맥락 목록은 **새 provider 세션을 여는 턴에만** 싣는다 — 대화 첫 턴 · 세션을 이어 쓸 수 없어 새로 여는 턴(기존 `reset_provider_session` · 참조 없음). 이어 쓰는 턴은 `context_catalog=None` 이다. 정책 문구도 「아래 목록」 → 「이 대화의 목록(세션을 연 턴에 실린 것) · 목록에 없으면(그 뒤에 생겼을 수 있다) 도구로」 로 바꿨다 | `B/bootstrap/conversation_worker.py:163` · 정책 `B/platform/codex_cli.py`(`WORK_AND_REPORT_ROUTING_POLICY`) · 주석 `codex_cli.py`·`claude_cli.py:328`·`ai.py:63` | `T/contract/test_answer_resources.py::test_the_context_catalog_rides_only_the_turns_that_open_a_provider_session` — 4턴: 첫 턴 실림 · 이어 쓰는 2턴 None · 세션 참조를 잃은 뒤 새 세션 턴은 **그 순간 DB 로** 다시 실림(턴 사이에 생긴 프로젝트 포함) |
| **W-5** | 어댑터 `update` 가 **PUT 직전에 `available(ignoring=자기 예약)` 을 한 번** 본다(생성 `create` 와 같은 방식). 차면 PUT 하지 않고 `RoomUnavailable`(가능한 방 포함)를 낸다. 실행이 그것을 받으면 `failed` + `reason=ROOM_BOOKING_REFUSED` 로 남기고 **옛 예약의 외부 번호·방·장소를 지킨다**(옛 예약은 옛 자리에 그대로 있으므로 다음 수정이 같은 예약을 다시 맞춘다). 이전에는 외부 번호를 버려 다음 수정이 새 예약을 또 잡을 수 있었다 | `B/platform/the_connect.py:142-149` · 실행 `B/bootstrap/application.py:1422` | `T/contract/test_meeting_rooms.py::test_the_connect_put_checks_the_room_is_still_free_right_before_moving`: 남이 잡음 → PUT 0 + 가능한 방 · 자기 예약은 점유 아님 → PUT 1 · PUT 끊김 → 결과 모름. 기존 `test_the_connect_transport_failure_is_an_unknown_mutation_outcome` 은 방 없는 PUT 으로 바꿨다(방을 주면 이제 앞의 GET 이 먼저 끊긴다) |

## 2. 지시와 다르게 된 점 — W-5 의 「409」

- **PUT 직전 확인에서 찬 경우는 409 가 아니다.** 응답은 `200` 이고 회의는 바뀌며 `room_reservation = {status:"failed", reason:"ROOM_BOOKING_REFUSED"}` 를 싣는다.
- 이유: 반영(PUT)은 정보 커밋 **뒤**에 돈다(OQ-1008 · W-2 「반영은 짧게」 · 계약 고정 3). PUT 직전 시점에는 회의가 이미 바뀌어 있어서, 409(「아무것도 바꾸지 않았다」)를 낼 수 없다.
- **409 는 저장 직전 재확인(커밋 앞)이 낸다.** 그 재확인과 PUT 사이의 창(DB 커밋 한 번)에 남이 잡은 경우만 위 `failed` 로 떨어진다.
- 진짜 409 로 만들려면 「PUT 먼저 → 정보 커밋, 커밋 실패 시 PUT 되돌림」 으로 순서를 뒤집어야 한다. 그러면 외부 호출이 다시 커밋 앞으로 오고 보상 경로가 생긴다. 필요하면 지시 주면 그렇게 바꾸겠다.

## 3. 운영 인벤토리

- `docs/unified-operations-inventory.json` 에서 **diff 난 1항목만** 패치했다: 도구 `meeting_update`(입력 스키마의 `MeetingRoomChoice` 에 `keep` 추가 · `room_id` 기본값).
- PATCH HTTP 시그니처는 그대로다(모델 이름이 같다).

## 4. 검증 (관련 시험만)

| 명령 | 파일 | 결과 |
|---|---|---|
| `make test-contract-serial FILES="…"` | unit: `test_ax_work_lookup_policy.py` · `test_action_policy.py` · `test_worker_resilience.py` / `tests/architecture` / contract: `test_meeting_rooms.py` · `test_meeting_room_change.py` · `test_action_center.py` · `test_meeting_creation_input.py` · `test_unified_commands.py` · `test_meeting_core.py` · `test_meeting_time_overlap.py` · `test_mcp.py` · `test_mcp_command_result.py` · `test_codex_cli.py` · `test_claude_cli.py` · `test_answer_resources.py` · `test_conversation_lifecycle.py` · `test_conversation_pagination.py` | **417 passed** · 0 failed |
| `AX_POSTGRES_TEST_URL=… uv run pytest -m integration -n0` | `test_meeting_rooms.py`(대역 import 경로) + `test_postgres_integration.py` | **46 passed** · 0 failed |

- 새 시험 12개:
  - `test_meeting_room_change.py` 9개(F-1 5 · W-1 2 · W-2 2) — 이 파일은 26개가 됐다
  - `test_meeting_rooms.py` W-5 1개
  - `test_answer_resources.py` W-3 1개(매 턴 시험을 대체)
  - 편집 계약 모양 시험은 `proposed_*` 두 칸이 생겨 갱신
- 전체 `make test` · `make verify` 는 돌리지 않았다(코디 지시)

## 5. FE 와 맞출 점 · 미결

1. **FE 가 보내는 「기존 유지」 = `room: {keep: true}`**(또는 현재 `room_id`) — 둘 다 받는다. `room` 을 아예 빼도 「안 바꿈」 이다. 카드가 제안 방을 미리 골라 둔 채 그대로 확정하면 FE 는 `room: {room_id: 제안}` 을 실어야 한다(서버는 제안을 자동 적용하지 않는다).
2. AX 가 **「예약 없음」(room_id null)을 제안**한 경우는 `proposed_room_id = null` 이라 「제안 없음」 과 구별되지 않는다(계약 §5 는 두 칸만 정했다). 필요하면 칸 하나(예: `room_proposed: bool`)를 더하면 된다 — 코디 판정 거리.
3. 새 409 코드 **`ROOM_RESERVATION_UNCONFIRMED`**(`available_rooms` 없음) — FE 는 `message` 를 그대로 보이면 된다. 계약 고정 문서에 없는 코드라 FE 에 알릴 필요가 있다.
4. W-5 의 409 아님(§2).
5. 실물 Connect: PUT 직전 확인이 쓰는 예약 목록 행 `id` = 우리 외부 번호라는 가정(WP3 리포트 §5-2와 같음) — 코디 E2E.
