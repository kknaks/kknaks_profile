# WP3-BE 결과 보고 — AX 흐름(서버)

## 상태: done (커밋하지 않음 · WP1 `e51fe3b` · WP2 `e58fb25` 위 워크트리 변경)

- 근거: WORK-012 「Phase WP3-BE」 · SPEC-010 §2.2 · §2.4 · §4.1 · §4.3 · §4.4 · §4.5 · DEC-009 · **WP3 BE↔FE 계약 고정(`wp3-contract-fixed.md`) 1~4 그대로**
- 함께 처리: WP2 재검수 W-r2-2 · W-r2-3 · W-r2-4 · WP1 검수 W-2
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`
- **외부 서비스**: The Connect 는 모든 시험에서 대역이다(`T/contract/test_meeting_rooms.py` `FakeRoomGateway`). **실물 확인(방 변경 1회 · 예약 없던 회의에 방 추가 1회 · 「예약 없음」 1회 · Connect 끊고 목록 503)은 코디 E2E 몫**이다

## 0. 먼저 — WARN 넷

| # | 고친 것 | 위치 · 시험 |
|---|---|---|
| W-r2-2 | heartbeat 가 예외(DB 끊김)로 끝나도 루프를 빠져나가지 않는다. 로그만 남기고 다음 간격에 다시 연장하며, 합성이 끝날 때까지 기다린다(고아 합성 스레드 · 한 워커에서 합성 둘이 겹치는 일 없음) | `B/bootstrap/meeting_worker.py:99` · 시험 `T/unit/test_meeting_worker_heartbeat.py::test_a_failed_or_raising_heartbeat_neither_breaks_the_loop_nor_orphans_the_synthesis`(연장 `False` · 예외 두 갈래 → 다음 간격에도 연장 시도 · 잡 complete) |
| W-r2-3 | `TypeError` 글자 맞추기 되돌이를 없앴다. 러너 시그니처를 부르기 **전에** `inspect.signature` 로 한 번 보고 한 번만 부른다. 프롬프트를 넘겨야 하는데 `stdin_text` 를 못 받는 러너면 **부르지 않고 오류**다(이중 실행 · 빈 프롬프트 없음) | `B/platform/cli_process.py:107`(`_accepts`) · `invoke_runner` · `invoke_plain_runner`. 시험 `T/contract/test_cli_prompt_stdin.py::test_a_runner_that_cannot_take_stdin_is_refused_before_it_runs` · `::test_a_type_error_inside_the_runner_is_not_retried_as_another_call_shape`. **옛 시험 러너 21개**에 `stdin_text=None` 키워드를 더했다(제품 코드 아님 — `test_codex_cli.py` 11 · `test_claude_cli.py` 6 · `test_codex_stream_adapter.py` 2 · `test_claude_stream_adapter.py` 3 · `test_codex_stream_ingest.py` 1) |
| W-r2-4 | `Popen(text=True, encoding="utf-8", errors="replace")` | `B/platform/cli_process.py:177` · 시험 `::test_the_prompt_is_written_as_utf8_whatever_the_childs_locale`(자식 `LC_ALL=C` · 한국어 9바이트, serial) |
| WP1 W-2 | AX 회의 생성에서 `carried_from_meeting_id` 를 주면 그 회의의 **미결 최종 안건은 `source:"carried"`**, 새로 말한 안건은 `manual` · 이어온 회의 없이 `carried` 금지 | 정책 `B/platform/codex_cli.py:454-456`(`MEETING_CREATION_POLICY`) · 도구 설명 `B/modules/ax_execution/tool_catalog.py` `meeting_create` · 시험 `T/unit/test_ax_work_lookup_policy.py::test_a_continued_meeting_carries_the_unresolved_agendas_as_carried` |

## 1. 계약 체크박스 7/7

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **017** AX 대화 프롬프트에 맥락 목록 — **매 턴** · 업무 생성 탐색 지시 「목록에서 먼저, 상세는 도구로」 | 요청 칸 `AiConversationRequest.context_catalog` `B/modules/ax_execution/ai.py:64` · 대화 워커가 매 턴 **WP2 의 `WorkflowApplication.ai_context_catalog()` 를 그대로** 부른다 `B/bootstrap/conversation_worker.py:160`(새로 만들지 않음 · 대화 실행 경로는 이 하나뿐 — `converse` 호출 grep) · 프롬프트 자리 Codex `B/platform/codex_cli.py:560` · Claude `B/platform/claude_cli.py:327`(정책 뒤 · `User message:` 앞) · 정책 `codex_cli.py:497` 「프로젝트·업무·사람은 먼저 아래 「조직 맥락 목록」에서 찾는다 … (목록에서 먼저, 상세는 도구로)」 |
| 2 | **001** `meeting.reservation.create` 초안 저장 · 거절 · 편집 계약(회의 고유 필드 + 안건 `source` + `room_id`) · 회의 생성 정책에 자료 탐색 → 근거 자료가 카드에 | 초안 저장 종류 `B/modules/actions/policy.py:38` · 편집 계약 `B/platform/actions.py` `_meeting_edit_contract` — 장소 글자 칸·값 삭제(`:2122`) · `room_id` 필드 `type: "room"` · `save_command`(`:2130`) · 안건 `source` 는 `MeetingReservationAgendaInput`(WP1)이 값에 싣는다 · 거절은 기존 `reject` 그대로(시험으로 고정) · 정책 「업무 생성과 같은 기준으로 관련 회의·자료를 찾는다 … 카드의 **근거 자료**로 남는다」 `codex_cli.py:451-453`. 근거 자료는 기존 경로 그대로다 — 제안 턴의 `material_search` 근거를 `EvidenceRecord` 로 고정하고 미리보기 「근거 자료」 줄로 낸다(`platform/actions.py` `_evidence` — 모든 제안 공통). **복구 중**(회의실 예약 결과 확인 대기) 카드는 초안 저장도 닫는다(`allow_save` `policy.py:125,140` · `action_center.py:773`) |
| 3 | **003/016 목록** `GET /api/meetings/rooms` `people`·`meeting_id` · 정원 · 자기 예약 점유 제외 · `current`·`unavailable_reason` · Connect 실패 = 503 · 미설정 `[]` · MCP 같은 규칙 | 선택지 계산 `room_options` `B/modules/meetings/rooms.py:350`(정원 = `capacity ≥ people` · 정원 모르는 방은 빼지 않음 · `current` 는 못 써도 냄 · 이유는 시간 먼저) · 어댑터 `available(…, ignoring=외부번호)` `B/platform/the_connect.py:97` + 경계 Protocol `rooms.py:239` · 조립 `WorkflowApplication.meeting_rooms` `B/bootstrap/application.py:1128`(닿지 않으면 `RoomServiceUnavailable` — 빈 목록으로 삼키지 않음) · `meeting_id` 는 수정할 수 있는 회의만(`room_context` `mtg/application.py:1956` → 아니면 404) · HTTP `entrypoints/http.py:953`(`people` ge=0 · `meeting_id`) · 503 매핑 `:551`(`{code:"ROOM_SERVICE_UNAVAILABLE"}`) · MCP `meeting_room_list` `entrypoints/mcp.py:1725`(같은 인자) + 설명 |
| 4 | **003/016 수정** `PATCH room`(없음=유지·재확인 / `null`=예약 없음 / `n`=변경) · 새 예약 `Idempotency-Key` + 울타리 · 방 변경 = PUT `room_id` · 저장 직전 재확인 · 409 + `available_rooms` · 저장 때 장애 = 지금 동작 + 응답에 실패 | 입력 `MeetingRoomChoice` · `MeetingInfoPatch.room` · `room_choice()` `B/modules/meetings/commands.py:175,192,226` · 계획 `_plan_room_change` `bootstrap/application.py:1179`(재확인 — 바뀐 뒤 시각·인원으로 `available(ignoring=자기 예약)` + 정원 → 못 쓰면 `RoomBookingRefused(RoomChangeRefused)` = **409 `ROOM_BOOKING_REFUSED` + `available_rooms`** · 자동 대체 없음 · 목록 밖 방 `RoomNotFound` = **422 `ROOM_NOT_FOUND`**(`http.py:556`) · 닿지 않으면 막지 않음) · 실행 `_execute_room_plan` `:1238`/`_execute_room_plan_locked` `:1248` — **move**: 같은 방 시간 이동은 예전처럼 장소 글자를 건드리지 않는다(`return {}`) · 방 변경은 PUT `room_id` + `location = 새 방 이름` / **create**: 생성의 이중 예약 울타리 `_resolve_room_creation_attempt` 를 키 `meeting-update:{회의}:{Idempotency-Key}` 로, **대체 없이**(`allow_replacement=False` `:1302`) / **cancel**: DELETE + 장소 비움 / **clear**(쥔 자리 없음 + `null`): 예약 표지·장소 비움(`clear_reservation` `mtg/application.py:2007`). 장애 → `room_reservation = {status:"failed", reason:"reservation_unavailable"}`, 외부 번호는 지킨다(계약 고정 3). 「자리를 쥔」 판정 `_holds_seat` `:525` = 외부 번호 + `booked`·`failed` — 실패 뒤 다음 수정이 새 예약을 또 잡지 않는다. HTTP `PATCH` `http.py:988`(`Idempotency-Key` 헤더) · 입구 `update_meeting` `:2016` |
| 5 | **016 AX 회의 수정 카드 편집 계약** — `SUPPORTED_ACTION_TYPES` · `_edit_contract` 갈래 · 확정 실행이 위 규칙 | 종류 추가 `B/modules/actions/confirmation.py:36` · confirm 라벨 「이 내용으로 회의 수정」 `policy.py:26` · 계약 `B/platform/actions.py:2133` `_meeting_update_edit_contract` = **`editor="meeting_update"` · `values={meeting_id, title, purpose, starts_at, ends_at, attendee_ids, external_attendees, room_id, room_name}`**(지금 회의 위에 AX 제안을 겹침 · `room_id/room_name` = 지금 쥔 방 — 회의 모듈 `room_context` 로 읽음 · AX 가 방을 제안했으면 `proposed_room_id` 를 덧붙임) · 고칠 칸 `title·purpose·starts_at·ends_at·attendee_ids·external_attendees·room`(장소 글자 없음) · 대기 중일 때만 계약을 낸다. **확정 `draft` = 바뀐 칸만 + `room:{room_id}`**(계약 고정 1): 정규화 `normalize_meeting_update` `confirmation.py:186` · 겹치기 `merge_meeting_update_draft` `:206`(제안 위에 사람이 고친 칸이 이김 · `meeting_id/room_id/room_name` 이 섞여 와도 읽지 않음) → `action_center.py:604` · `decide_ax_confirmation` `:250`. 확정 실행 `bootstrap/application.py:4042` — PATCH 와 **같은** `_plan_room_change`(재확인 · 409) → `update_info` → 커밋 뒤 `_execute_room_plan`(영수증 갱신 훅). 새 예약 키는 `_prepare_action_effect` 가 `action:{id}:meeting-update` 로 싣는다 `:4288-4291` |
| 6 | **옛 `meeting.update`** 를 같은 수정 검증 경로로 | `bootstrap/application.py:4060` — 같은 `_plan_room_change`(방 유지 · 재확인 · 409)를 먼저 타고, 커밋 뒤 같은 `_execute_room_plan`. 참석자는 그 계약에 칸이 없다(합치기는 `MeetingInfoPatch` 쪽 WP1) |
| 7 | 생성의 Connect 실패는 지금 동작 그대로(OQ-1008) | 생성 경로(`create_meeting` · `_reserve_room` 의 자동 대체 · `room_unavailable` 거절)는 그대로 두었다. `allow_replacement` 기본값 `True` — 수정의 새 예약만 `False` |

**W-r2-6 (AX 사외 장소 글자)**: AX 제안은 생성·수정 모두 장소 글자를 저장하지 않는다. 생성은 `_freeze_meeting_proposal` `actions.py:330`, 수정은 `normalize_meeting_update` 가 `location` 을 뗀다(`actions.py:306`). 미리보기에도 남기지 않는다 — 생성은 「회의실 n」, 수정은 「회의실 예약 없음」 / 「회의실 n」(`actions.py:1372`). 사람이 HTTP 로 쓰는 장소 칸(API)은 그대로다(OQ-1005).

## 2. Code Surface WP3 대비 닿은 자리

| 행 | 닿은 자리 |
|---|---|
| 회의 생성 Action `meeting.reservation.create` | 초안 저장 종류 · 편집 계약(장소 삭제 · `room` 타입 · `save_command`) · 제안 고정(장소 None) · 미리보기 · 복구 중 저장 닫기. 확정·울타리·첨부 경로(`action_center.py:788,853` · `confirmation.py:39` · `bootstrap/application.py` 생성 실행)는 그대로 |
| 초안 저장·카드 판별 `DRAFT_SAVE_ACTION_TYPES · _meeting_edit_contract` | `policy.py:38,140` · `actions.py:2122-2130,2133`. 화면 쪽(`AxDraftCard`·`MessageList`)은 FE 몫 |
| 회의 생성 정책·도구 `MEETING_CREATION_POLICY` | 줄 넷 추가(자료 탐색 · `carried` · 회의실만 · 기존 회의는 `meeting_update`) — Claude 는 import 라 같은 문장 |
| 회의실 `meeting_room_list · RoomUnavailable · RoomBookingRefused · available_rooms …` | API(`http.py:953`) · 실패 삼킴 제거(`bootstrap/application.py:1128`) · 어댑터 `the_connect.py:97` · 경계 `rooms.py:239` · 새 예외 셋 `rooms.py:104,113,119` · 오류 매핑 `http.py:551,556` · AX 도구 `mcp.py:1725` + `tool_catalog` 설명 · 생성 예약 `_reserve_room(allow_replacement)` · `_resolve_room_creation_attempt(allow_replacement)` |
| 회의 수정·동기화 `meeting.info.update · MeetingInfoPatch · _sync_room_reservation · gateway.update(` | `commands.py:175-226` · `bootstrap/application.py` `update_meeting` · 수정 실행 두 갈래 · `_sync_room_reservation_locked` 의 「자리 쥔」 판정(`:1645`)과 실패 상태(`:1694` — 시각 동기화 실패 = `failed`, **취소 반납 실패는 지금처럼 `booked`**) · `http.py:988` · `mcp.py:840,1768` · `actions.py` 미리보기 |
| AX 수정 카드 편집 계약 자리 | `confirmation.py:36` · `actions.py` `_edit_contract` 갈래 + `_meeting_update_edit_contract` · 옛 `meeting.update` 실행 합침 |
| 017 대화 프롬프트 | `codex_cli.py:497,560` · `claude_cli.py:327` · `ai.py:64` · `conversation_worker.py:160` |
| **표 밖** | 재생 복구 `_sync_room_reservation`(`bootstrap/application.py` 영수증 복구 경로)도 `_holds_seat` 로 맞췄다 — 앞 동기화가 실패한 예약을 다시 맞춘다. `T/integration/postgres/test_postgres_integration.py:1673` 의 대역 `available` 시그니처도 맞췄다 |

**운영 인벤토리**: `docs/unified-operations-inventory.json` 에서 **diff 난 7항목만** 패치했다.
- 도구 셋: `meeting_room_list` · `meeting_create`(설명) · `meeting_update`(설명 · `room` · `idempotency_key`)
- HTTP 시그니처 둘: `PATCH /api/meetings/{meeting_id}` · `GET /api/meetings/rooms`
- 소유 호출 둘: 같은 두 라우트

## 3. 새 시험 · 고친 시험

**새 파일** `T/contract/test_meeting_room_change.py`(17)
- 목록: `people` 정원 · 자기 예약 점유 제외 + `current` · 못 쓰는 기존 방은 비활성 + 이유(시간 · 정원) · 503 · 남의 회의 `meeting_id` 404 · MCP 같은 규칙
- PATCH: 방 변경 = PUT `room_id` · 예약 없던 회의 + 방 = 키 없으면 422, 있으면 예약 1회(같은 키 재전송에 이중 예약 없음) · `null` = 취소 + 장소 비움 · 새 시간 만석 409 + `available_rooms` + 회의 불변 + 자동 대체 없음 · 인원 초과 409 · 없는 방 422 · 장애 = 회의는 바뀌고 `failed`/`reservation_unavailable` + 다음 수정이 같은 예약을 다시 맞춤(새 예약 없음)
- AX 수정 카드: 편집 계약 모양(계약 고정 1 · 장소 글자 미리보기 없음 · 명령 `confirm`·`reject`) · 「바뀐 칸만 + `room`」 확정이 PATCH 규칙으로 방 이동 · 만석 확정 409 · **옛 `meeting.update` 도 재확인 409**

**기존 파일에 더함**
- `T/contract/test_action_center.py` — 회의 초안 저장(회차 2 · 장소 칸 없음 · `save_command`) · 회의 초안 거절 · 회의 수정 카드는 저장 없음
- `T/contract/test_answer_resources.py` — **매 턴** 맥락 목록이 대화 요청에 실리고, 턴 사이 생긴 프로젝트가 다음 턴에 들어감(017)
- `T/unit/test_ax_work_lookup_policy.py` +5 — 목록에서 먼저 · 회의 생성 자료 탐색 · `carried`(W-2) · 회의실만/`meeting_update` · Codex·Claude 프롬프트에 맥락 목록 자리
- `T/unit/test_action_policy.py` — 회의 생성 = confirm·save·reject · 회의 수정 = confirm·reject
- WARN 시험 5(§0)

**계약이 바뀌어 고친 기존 시험**
- `test_meeting_rooms.py`
  - 목록 항목 모양 3건
  - AX 회의 수정 승인을 `approve` → `confirm`(빈 draft) 6곳
  - (복구 중 명령 `["confirm"]` 은 그대로 통과 — 저장도 닫음)
- `test_unified_commands.py::_approval_request` — 회의 수정 카드는 confirm
- `test_meeting_creation_input.py` — 회의 편집 계약 = 예약 필드 − `location`
- `test_action_center.py::test_save_is_offered_only_on_the_two_task_draft_kinds` → 회의 초안 저장 시험 셋으로 바꿈
- 대역 `FakeRoomGateway.available(ignoring)` + `occupant` · postgres 대역 시그니처

## 4. 검증 (바꾼 부분 관련 시험만 — 코디 지시)

| 명령 | 파일 | 결과 |
|---|---|---|
| `make test-contract-serial FILES="…"` | unit: `test_ax_work_lookup_policy.py` · `test_action_policy.py` · `test_meeting_worker_heartbeat.py` · `test_codex_stream_adapter.py` · `test_claude_stream_adapter.py` / `tests/architecture`(계층 · **인벤토리 drift**) / contract: `test_meeting_rooms.py` · `test_meeting_room_change.py`(새) · `test_action_center.py` · `test_meeting_creation_input.py` · `test_unified_commands.py` · `test_meeting_core.py` · `test_meeting_agenda_source.py` · `test_meeting_time_overlap.py` · `test_mcp.py` · `test_mcp_command_result.py` · `test_codex_cli.py` · `test_claude_cli.py` · `test_cli_prompt_stdin.py` · `test_codex_stream_ingest.py` · `test_answer_resources.py` · `test_conversation_lifecycle.py` | **439 passed** · 0 failed · 1 deselected |
| `AX_POSTGRES_TEST_URL=… uv run pytest -m integration -n0`(파일 지정 postgres 타깃이 없어 직접 지정) | `test_postgres_integration.py` · `test_meeting_time_overlap_postgres.py` | **51 passed** + 1건은 단독 실행 때 `tests/contract` 가 import 경로에 없어 실패 → 대역 파일(`test_meeting_rooms.py`)과 함께 지정해 **1 passed**(기준선 전체 실행에서는 같은 패스에 contract 가 모여 통과하던 시험 — 코드 결함 아님) |

- 전체 `make test` · `make verify` · 프론트 vitest 는 돌리지 않았다(코디 지시 — 마지막에 코디가 한다)

## 5. 미결 · 주의점

1. **실물 Connect 1회(코디 E2E)**
   - 방 변경 PUT `room_id` 가 실제로 방을 옮기는지(I-5 — 어댑터 인자는 있었지만 호출부가 처음 쓴다)
   - 예약 없던 회의에 방 추가(중복 예약 없음)
   - 「예약 없음」 취소
   - Connect 끊고 목록 503
2. **`available(ignoring)` 의 판정은 The Connect 예약 목록 행의 `id` 가 우리가 저장한 외부 번호와 같다는 가정**이다. 생성 POST 응답의 `id` 를 외부 번호로 저장하므로 같은 값일 것이다 — 실물에서 확인한다
3. **회의 상세의 `room_reservation` 은 방 번호를 내지 않는다**(기존 `view()`: 상태 · 방 이름 · 사유). 수정 카드는 `values.room_id/room_name` 으로 지금 방을 받고, 수정 모달은 목록의 `current` 줄로 받는다. 상세 응답에 `room_id` 를 더할지는 FE 와 맞출 일이다(지금은 계약 고정 1·4 로 충분)
4. 같은 방으로 시간만 옮긴 성공은 예전처럼 장소 글자를 다시 쓰지 않는다(그 사이 사람이 바꾼 장소를 덮지 않는다 — 기존 시험이 고정). 방을 바꾸거나 새로 잡으면 장소 = 방 이름이다
5. 직접 MCP `meeting_update`(위임 턴 아님)로 예약 없던 회의에 방을 고르면 `idempotency_key` 인자가 필요하다(PATCH 의 헤더와 같은 규칙). 위임 턴의 수정 카드는 승인 id 로 키를 만든다
6. W-r2-5(WP2 수정 1 리포트 §7-3 문구)는 이번 지시 목록에 없어 손대지 않았다
