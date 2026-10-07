# WP3-BE 수정 2 결과 보고 — 재검수 FAIL 1 · WARN 2

## 상태: done (커밋하지 않음 · 수정 1 위 워크트리 변경)

- 근거: `wp3-fix2-instructions.md`(backend 몫 셋) · `review-wp3-r2-report.md` · 계약 고정 문서 **§6 · §7**
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`

## 1. 지시 3/3

| # | 고친 것 | 위치 | 시험 |
|---|---|---|---|
| **F-r2-1** | 편집 계약 `values.room_proposed: bool` 을 더했다. **AX 가 회의실을 바꾸자고 했을 때만 true**다 — 제안 `changes` 에 `room` 이 있을 때(「예약 없음」 = `room:{room_id:null}` 제안도 true). 시간·제목만 바꾸는 제안은 false다. 확정 draft 에 섞여 와도 읽지 않는다(값 모양 키 허용 목록에 추가) | `B/platform/actions.py:2183` · 허용 목록 `B/modules/actions/confirmation.py`(`merge_meeting_update_draft`) | `T/contract/test_meeting_room_change.py`: **방 있는 회의 + 시간만 제안 → `room_proposed=false`** · `proposed_room_id=null` · 지금 방(3) 그대로 / **「예약 없음」 제안 → `room_proposed=true` + `proposed_room_id=null`** / 방 제안 → true(기존 시험에 단언 추가) / 계약 모양 시험에 열한째 칸 반영 |
| **W-r2-2** | 예약 시스템이 **「없음」(404)** 이라고 답하면 새 예외 `RoomReservationGone`(`reservation_gone`)을 낸다(닿지 못함 `RoomGatewayUnavailable` 과 가른다 · PUT·DELETE 만 · 로그인 재시도 뒤 판정). 받는 쪽: **취소**는 거둔 것으로 확정(`cancelled` · 장소 비움) · **이동**은 **자리를 비운 것으로 확정**(`failed` + `reason=reservation_gone` + **외부 번호 버림**) → 다음 수정이 없는 예약에 PUT 을 되풀이하지 않는다. 방을 다시 고르면 생성 울타리로 새로 잡는다(키 필요). 같은 처리를 수정 실행 · 동기화/복구(`_sync_room_reservation_locked`) · 주인 없는 예약 반납에 넣었다 | 예외 `B/modules/meetings/rooms.py:119` · 어댑터 `B/platform/the_connect.py:150,154,202` · 실행 `B/bootstrap/application.py:1407,1453` · 동기화 `:1825,1853` · 반납 `:2091` | 어댑터: 404 → `RoomReservationGone`(PUT · DELETE) · 결과 모르는 예약(외부 번호 있음)이 사라짐 → 첫 수정 `failed/reservation_gone` · **두 번째 수정은 PUT 0** · 방을 다시 고르면 새 예약 1 / 이미 없는 예약 취소 → `cancelled` + 장소 null |
| **W-r2-3** | **실행 직전 대조** `_reconcile_room_plan` — 회의실 락 안에서 지금 예약을 다시 읽어 계획 때의 「쥔 자리」(외부 번호)와 비교한다. 같으면 그대로 실행한다. 달라졌으면 지금 상태로 계획을 고친다:<br>— 그 사이 자리가 생겼다(복구 확정): `create` → `move`(새로 잡지 않고 그 예약을 옮김) · `clear` → `cancel`<br>— 자리가 사라졌다: `move` 는 하지 않고 `cancel` 은 `clear`<br>— 결과 모르는 새 예약이 됐다: 아무것도 하지 않는다(이중 예약 방지 · W-1 과 같은 이유)<br>정보는 이미 커밋된 뒤라 「거절」 대신 「다시 계획」 을 골랐다 | `B/bootstrap/application.py:1356` · 호출 `:1391` | 계획(새 예약) 뒤 · 실행 전에 복구가 자리를 확정 → **생성 0 · 그 예약을 PUT 으로 옮김** · 장소 = 새 방 |

## 2. 운영 인벤토리

- `docs/unified-operations-inventory.json` 에서 **diff 난 1항목만** 패치했다: `PATCH /api/meetings/{meeting_id}` 의 `owning_calls`(수정 경로가 지금 예약을 읽는 `reservation_input` 호출이 늘었다).
- 도구 스키마 · HTTP 시그니처는 바뀌지 않았다.

## 3. 검증 (관련 시험만)

| 명령 | 파일 | 결과 |
|---|---|---|
| `make test-contract-serial FILES="…"` | `tests/architecture` · `tests/unit/test_action_policy.py` · contract: `test_meeting_rooms.py` · `test_meeting_room_change.py` · `test_action_center.py` · `test_meeting_creation_input.py` · `test_unified_commands.py` · `test_meeting_core.py` · `test_meeting_time_overlap.py` · `test_mcp.py` · `test_mcp_command_result.py` | 첫 회차 336 passed · 1 failed(인벤토리 `owning_calls` drift) → 패치 뒤 `tests/architecture` **45 passed** · 바뀐 contract 파일 둘(`test_meeting_room_change.py` 31 · `test_meeting_rooms.py` 39) 따로 돌려 **70 passed** |
| `AX_POSTGRES_TEST_URL=… uv run pytest -m integration -n0` | `test_meeting_rooms.py`(대역 import 경로) + `test_postgres_integration.py` | **46 passed** |

- 새 시험 6개:
  - `test_meeting_room_change.py` 5개(F-r2-1 2 · W-r2-2 2 · W-r2-3 1)
  - `test_meeting_rooms.py` 어댑터 404 1개
- 대역 `FakeRoomGateway.gone` 을 더했다
- 전체 `make test` · `make verify` 는 돌리지 않았다

## 4. 미결 · 주의점

1. 「없음」 판정은 **The Connect 가 지워진 예약에 404 를 준다**는 가정이다. 다른 코드(예: 400 · 410)를 주면 지금처럼 `failed`(닿지 못함)로 남는다 — 실물 확인은 코디 E2E.
2. 동기화 경로에서 사라진 예약을 옮기려다 비운 경우, 장소 글자는 방 이름을 그대로 둔다(기존 동기화 규칙 — 취소만 장소를 비운다). 수정 실행 경로는 장소를 비운다.
3. 생성 보상(`_compensate_room_creation_attempt`)의 DELETE 가 404 면 지금처럼 확인 대기로 남는다(이번 지시 밖 · 드묾).
