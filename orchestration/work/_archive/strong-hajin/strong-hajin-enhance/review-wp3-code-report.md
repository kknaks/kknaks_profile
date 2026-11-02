# 코드 검수 — WORK-012 WP3 (BE + FE)

- 검수자: reviewer(read-only) · 2026-10-07
- 대상: 코드 워크트리 `strong-hajin-enhance` 의 **WP2 커밋 `e58fb25` 뒤 미커밋 변경 전부**
  - 수정 46파일(+1823/−306) · 새 파일 7
  - 리포트 경로: 지시서 본문은 `review-wp1-code-report.md` 로 적혀 있으나 코디 메시지대로 `review-wp3-code-report.md` 에 쓴다 — WP1 리포트는 덮지 않았다
- 계약
  - WORK-012 「Phase WP3-BE」·「Phase WP3-FE」 · Code Surface WP3 표
  - SPEC-010 §2.2 · §2.4 · §4.1 · §4.3 · §4.4 · §4.5
  - **`wp3-contract-fixed.md` 1~4**
- 워커 리포트: `be-wp3-report.md` · `fe-wp3-report.md`(코디 정정대로)
- 한 일: `git diff` 핵심 경로 읽기 · `rg` 재확인. **시험·빌드·실물 Connect 는 돌리지 않았다** — 수치는 워커 값(BE 439 + postgres 51+1 · FE 28파일 560/564, 실패 4 = 기준선)
- 지시서 물음 3·4 는 WP1 문구가 그대로 와 있다. WP3 의 같은 축(계약 고정 넷 · 수정 경로 회귀)으로 답한다.
- 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/` · `T/` = `backend/tests/`

---

## 0. 판정 — **FAIL**(BE↔FE 계약 1건)

체크박스는 BE 7/7 · FE 5/5 모두 구현됐다. 넘겨받은 WARN(WP2 W-r2-2·3·4 · WP1 W-2·W-3)도 모두 고쳐졌다.
계약 고정 2~4 는 양쪽이 같다. 옛 `meeting.update` 도 새 재확인·409 를 탄다(AC-21).

**FAIL 1건**(계약 고정 1)
- AX 가 **회의실 변경을 제안한** 수정 카드에서, BE 는 그 방을 `values.proposed_room_id` 로 따로 싣는다. FE 는 이 칸을 **읽지 않는다.**
- 그래서 카드 셀렉트는 「기존 — 회의실 N (변경 안 함)」 을 보인다. 그런데 사람이 그대로 [등록]하면 `draft` 에 `room` 이 없고, 서버는 **제안의 방 변경을 그대로 실행한다.**
- 화면이 말한 것과 다른 일이 일어난다 — 예약 이동이 사람 눈에 보이지 않는다.

그 밖은 **WARN 8건**이다.

---

## 1. 계약 체크박스 — 구현 위치

### WP3-BE (7/7)

| 계약 | 구현 | 판정 |
|---|---|---|
| 017 대화 매 턴 맥락 목록 · 「목록에서 먼저」 | `AiConversationRequest.context_catalog` `B/modules/ax_execution/ai.py:64` · 대화 워커가 매 턴 WP2 의 `ai_context_catalog()` `B/bootstrap/conversation_worker.py:160` · 프롬프트 자리 `codex_cli.py:560` · `claude_cli.py:327` · 정책 `codex_cli.py:497`. 프롬프트는 WP2 의 **stdin 경로**로 간다(argv 아님) | PASS(W-3) |
| 001 회의 생성 초안 저장 · 거절 · 편집 계약 · 자료 탐색 | 초안 저장 종류 `B/modules/actions/policy.py:38` · 편집 계약 장소 삭제·`room` 타입·`save_command` `B/platform/actions.py:2122-2130` · 정책 `codex_cli.py:451-453` · 근거 자료는 기존 `_evidence` 경로 · 복구 중 저장 닫기 `policy.py:125,140` | PASS |
| 003/016 목록 | `room_options` `B/modules/meetings/rooms.py:350-376` · `available(…, ignoring)` `B/platform/the_connect.py:97-109` · `meeting_rooms` `B/bootstrap/application.py:1128-1175`(삼킴 제거 → `RoomServiceUnavailable`) · `meeting_id` 권한 `room_context` → 404 · HTTP `http.py:953` · 503 `:551-555` · MCP `mcp.py:1725` | PASS(W-4) |
| 003/016 수정 | `MeetingRoomChoice`·`MeetingInfoPatch.room`·`room_choice()` `B/modules/meetings/commands.py:175-226`<br>계획 `_plan_room_change` `bootstrap/application.py:1179-1236`<br>실행 `_execute_room_plan(_locked)` `:1238-1338`<br>`_holds_seat` `:525-534`<br>PATCH `update_meeting` `:2016-2037` | PASS(W-1 · W-5) |
| 016 AX 수정 카드 편집 계약 | 종류 `B/modules/actions/confirmation.py:36` · 계약 `B/platform/actions.py:2133-2200` · 정규화·겹치기 `confirmation.py:186-220` · 확정 실행 `bootstrap/application.py:4042-4059` · 새 예약 키 `:4288-4291` | **FAIL — §3 F-1** |
| 옛 `meeting.update` 같은 경로 | `bootstrap/application.py:4060-4074` — `_plan_room_change(…, None)` 먼저(시각이 바뀌고 자리를 쥐었으면 재확인 → 409) → 커밋 뒤 `_execute_room_plan` | PASS(AC-21 · W-2) |
| 생성의 Connect 실패는 그대로 | `_reserve_room(allow_replacement=True)` 기본값 · 수정의 새 예약만 `False` | PASS |

### WP3-FE (5/5 + W-3)

| 계약 | 구현 | 판정 |
|---|---|---|
| 회의실 셀렉트 부품 하나 · 네 자리 | `F/features/meetings/RoomSelect.tsx`(조회 `:78-109` · 300ms · 503 = 「조회 실패」 · 기존 줄 · 비활성+이유 · 막힘 `:144`)<br>쓰는 자리 넷: `BookingModal.tsx:551` · `MeetingEditModal.tsx:253` · `AxDraftCard.tsx` `MeetingPageBody` `:214~` · `ActionMeetingUpdateCard.tsx:257`<br>`readMeetingRooms` 호출은 `RoomSelect.tsx:85` 한 곳 | PASS |
| 수정 모달 장소 칸 → 셀렉트 · 바뀐 값만 · H-2 · H-1 | `MeetingEditModal.tsx` `changedPatch` `:129-146` · 멱등 키 · [저장] 옆 이유 `:303` · 장애 문구 `:166` · 409 → `"unset"` | PASS(W-6) |
| AX 회의 생성 카드 = `AxDraftCard` 틀 | kind 셋 `AxDraftCard.tsx:40` · 편집기 맞춤 `:44-46` · 회의 쪽 `MeetingPageBody` `:214-271`(기본 정보·참석자·회의실+안건·자료) · [수정] = `BookingModal` 편집 창(`save_draft`) `:592~` · 접힌 한 줄 「회의 열기」<br>**OQ-901 확인**: 회의 쪽에 프로젝트·연관 업무 칸이 없다(`project_id`·`reference_task_ids` 를 읽는 줄 `:307-315` 은 업무 쪽 전용) · 편집 창의 `TaskAttachmentGroup` 에 넘기는 `draft={{} as {reference_task_ids?}}`(`:612`)는 타입 맞추기용 빈 값이라 새는 칸 없음 | PASS |
| AX 회의 수정 카드 새로 | `F/features/action/ActionMeetingUpdateCard.tsx` · 갈래 `MessageList.tsx:318-325` · `meetingUpdateDraft` `:69-83` | **FAIL — §3 F-1** |
| 「회의실 예약 없음」 | `labels.ts:864` | PASS |
| (WP1 W-3) 불러온 방이 새 시간에 없으면 이유 | `BookingModal.tsx` `applySuggestion` → `requestedRoom` · `RoomSelect.tsx:141` | PASS |

### 넘겨받은 WARN

| WARN | 지금 | 판정 |
|---|---|---|
| WP2 W-r2-2 heartbeat 예외 | `B/bootstrap/meeting_worker.py:92-106` — `try/except Exception` → 로그 + `continue`(합성 끝까지 기다림) · 시험 두 갈래 | PASS |
| WP2 W-r2-3 `TypeError` 되돌이 | `B/platform/cli_process.py:107-140` `_accepts`(`inspect.signature`) — 부르기 전에 한 번 정하고 `stdin_text` 를 못 받는 러너면 부르지 않고 오류 | PASS |
| WP2 W-r2-4 인코딩 | `cli_process.py:177` `encoding="utf-8", errors="replace"` · 시험 `LC_ALL=C` 자식 | PASS |
| WP1 W-2 AX `carried` | 정책 `codex_cli.py:454-456`(이어온 회의의 `concluded=false` 최종 안건 = `carried`) · 도구 설명 · 시험 | PASS |
| WP1 W-3 | 위 FE 표 | PASS |

---

## 2. Code Surface WP3 — 다시 센 것

| 표의 행 | 다시 센 것 | 판정 |
|---|---|---|
| 회의 생성 Action | 초안 저장 · 편집 계약 · 미리보기 · 제안 고정(장소 None `actions.py:330`) — 확정·울타리·첨부는 그대로 | PASS |
| 초안 저장·카드 판별 | 서버 `policy.py:38,140` · `actions.py:2122-2133` / 화면 `AxDraftCard.tsx:40-53` · `MessageList.tsx:314,318` · `MyWorkPage.tsx`(`isAxTaskDraftKind` — 회의 초안이 내 업무 칩에 섞이지 않게, 표 밖에서 찾음) · `ActionMeetingCard` 는 안전망으로 남김(회의 생성은 앞 갈래가 잡는다 — 시험 잠금) | PASS |
| 회의 생성 정책·도구 | `MEETING_CREATION_POLICY` 줄 넷 · Claude 는 import | PASS |
| 회의실 | API·실패 삼킴 제거·어댑터·경계·예외 셋(`rooms.py:104-125`)·오류 매핑·MCP·`tool_catalog` · 화면 `api.ts:1483` · `RoomSelect` | PASS |
| 회의 수정·동기화 | `commands.py` · `update_meeting` · 수정 실행 둘 · `_sync_room_reservation_locked` 의 `_holds_seat` · HTTP `:988` · MCP `:840,1768` / 화면 `MeetingEditModal` · `api.ts:1258-1268` | PASS |
| AX 수정 카드 편집 계약 자리 | `confirmation.py:36` · `actions.py` `_edit_contract` 갈래 · `MessageList.tsx:318` · `ActionResultCard` 정의는 다른 종류용으로 남음 | PASS(내용은 F-1) |
| 017 대화 프롬프트 | `codex_cli.py:497,560` · `claude_cli.py:327` · `ai.py:64` · `conversation_worker.py:160` — 대화 실행 경로는 이 하나(`converse` 호출 재확인) | PASS |
| 운영 인벤토리 | 7항목만 패치(워커 셈) — 아키텍처 drift 시험 통과(워커) | PASS |

---

## 3. 계약 고정 넷 · BE↔FE

| 고정 | BE | FE | 판정 |
|---|---|---|---|
| 1 수정 카드 `editor="meeting_update"` · `values` 아홉 · `draft` = 바뀐 칸만 + `room` | `values` 아홉 + **AX 가 방을 제안했으면 `proposed_room_id` 를 덧붙인다**(`actions.py:2175-2176` · 계약 고정 문서에 없는 열째 칸) | `draftOf` 가 `values.room_id` 만 보고 「keep」/「none」 을 정한다(`ActionMeetingUpdateCard.tsx:56-66`). **`proposed_room_id` 를 읽는 코드 0**(`rg proposed_room_id frontend/src` = 0) | **FAIL — F-1** |
| 2 수정 거절 409 `{code:"ROOM_BOOKING_REFUSED", message, available_rooms}` | `RoomChangeRefused.reason` `rooms.py:110` → `RoomBookingRefused` → `http.py:563-571` | `roomRejectionOf`(`BookingModal.tsx:39`)를 수정 모달·수정 카드가 같이 씀 | PASS |
| 3 저장 때 장애 `room_reservation={status:"failed", reason:"reservation_unavailable"}` | `_execute_room_plan_locked` `RoomReservationError` 갈래 · 외부 번호 보존 | `MeetingEditModal.tsx:166` 문구 | PASS |
| 4 목록 인자·항목·503·`[]` | `meeting_rooms` · `room_options` · 503 매핑 | `RoomSelect` · `viewModels` `MeetingRoom` | PASS |

### F-1 (FAIL · BE+FE) — AX 가 제안한 회의실이 카드에 안 보이는데 확정은 그 방으로 옮긴다

- **흐름**:
  1. AX 가 `meeting_update` 로 `request.room = {room_id: 7}` 을 제안한다(정책 `codex_cli.py` 「회의실은 `request.room = {room_id}`」)
  2. 편집 계약 `values.room_id/room_name` = **지금 방 3**, `values.proposed_room_id = 7`
  3. FE 셀렉트는 「기존 — 회의실 3 (변경 안 함)」 을 고른 채로 선다
  4. 사람은 그대로 [등록]한다
  5. `meetingUpdateDraft` 가 `room` 을 싣지 않는다(`:80`)
  6. 서버 `merge_meeting_update_draft`(`confirmation.py:206-220`)가 **제안의 `changes.room={room_id:7}` 을 그대로 남긴다**
  7. 확정 실행이 방 7 로 PUT 한다
- **결과**: 「변경 안 함」 을 보고 누른 사람의 회의가 다른 방으로 옮겨진다. 제안이 `{room_id: null}`(예약 없음)이면 **예약이 취소된다.**
- SPEC-010 §2.4 「AX 가 제안한 방이 있으면 미리 골라져 있다」 · D-09 와 어긋난다. 계약 고정 1 문서에도 이 칸이 없다 — BE 가 계약 밖 칸을 더했고 FE 는 몰랐다.
- **시험이 못 잡은 이유**: FE 시험(`ActionMeetingUpdateCard.test.tsx`)의 계약 대역에 `proposed_room_id` 가 없다. BE 시험은 「바뀐 칸만 + `room`」 확정만 본다.
- **고칠 것**(둘 다 필요하다)
  - **FE**: `values.proposed_room_id` 가 있으면(값 `null` = 「예약 없음」 제안 포함 — 키 존재로 판정) 셀렉트를 그 선택으로 미리 고르고, 그 줄에 「AX 제안」 표지를 단다. 사람이 「기존」 으로 되돌리면 `room` 을 보내야 한다 — 기존 방이면 `{room_id: 지금 방}`, 쥔 방이 없던 회의면 `{room_id: null}`.
  - **BE**: 사람이 「기존 유지」 를 보냈을 때 제안의 방이 이기지 않게 한다. 예를 들어 `draft.room` 이 지금 방과 같으면 `changes.room` 을 지운다.
  - **계약 고정 1 문서에 `proposed_room_id` 를 올린다**(코디).
  - **시험**: 양쪽에 「방을 제안한 카드를 그대로 등록 = 제안 방」 · 「기존으로 되돌려 등록 = 방 유지」.

---

## 4. 회귀 · Connect 경로

| 갈래 | 본 것 | 판정 |
|---|---|---|
| 방 유지 + 시각/인원 변경 | `room` 없음 · 자리를 쥠 → 재확인(`available(ignoring=자기 외부 번호)` + 정원) → 못 쓰면 409(회의 불변) · 쓰면 시각 변경은 `move`(같은 방 PUT · 장소 글자 안 건드림) · 인원만 변경은 `keep`(외부 호출 없음) | PASS |
| `null` 취소 | 쥔 자리 → `cancel` = DELETE + 장소 비움 · 안 쥠 → `clear` = 표지·장소 비움 · DELETE 실패 = `failed` + 외부 번호 보존(다음 수정이 다시 맞춤) | PASS |
| 방 이동 | 쥔 자리 → PUT `room_id`(같은 외부 번호) · 안 쥠 → `create` = 생성 울타리를 키 `meeting-update:{회의}:{Idempotency-Key}` 로 · 대체 없음 · 같은 키 재전송 = 예약 1회(시험) · AX = `action:{id}:meeting-update` | PASS |
| **확인 대기 예약** | `_holds_seat` 은 `booked`·`failed` 만 자리를 쥔 것으로 본다(`application.py:525-534`) — `needs_verification` 은 빠진다. 앞 예약/이동의 결과가 「모름」 인 회의를 사람이 PATCH 하면 두 갈래로 샌다:<br>— 방을 고르면 `create` → **이중 예약 가능**(모르는 예약이 실제로 잡혔으면)<br>— 시각만 바꾸면 `none` → **Connect 쪽 예약이 옛 시각에 남을 수 있음**<br>PATCH 쪽에는 「확인 대기 중이면 막는다」 가드가 없다(AX 카드는 복구 중 저장을 닫지만 확정·PATCH 는 열려 있다) | **WARN(W-1 · BE)** — 확인 대기면 수정의 방 변경을 409/423 으로 막거나, 자리를 쥔 것으로 보고 확인 뒤에만 반영 |
| 재확인 ↔ PUT 사이 | 어댑터 `update`(`the_connect.py:133-141`)는 PUT 전에 비어 있는지 보지 않는다(생성 `create` 는 본다). 재확인 뒤 그 짧은 창에 남이 잡으면 Connect 가 겹침을 허용하는지에 달렸다 | WARN(W-5 · BE · 실물 확인) |
| Connect 예약행 `id` = 외부 번호 가정(BE 미결 2) | `available(ignoring)` 이 `row["id"] == 우리 external_id` 로 자기 예약을 뺀다. 생성 POST 응답 `id` 를 저장하므로 같을 것이다. **틀리면** 수정할 때마다 기존 방이 「새 시간에 예약 불가」 로 막히고(시간이 옛 시각과 겹치는 경우), 재확인도 409 다 | WARN(W-4) — 실물 1회(코디 E2E 항목에 「시간을 30분만 미뤄도 기존 방이 선다」 추가) |
| 상세 `room_reservation` 에 `room_id` 없음(BE 미결 3) | FE 는 기존 줄을 **서버 목록의 `current`** 로 안다(`meeting_id` 를 주면 서버가 쥔 방에 `current: true`). 이름(`room_reservation.room_name`, `status==="booked"` 일 때)은 조회 실패 때의 대체 표시뿐 | **계약대로 — 결함 아님**. 단 대체 표시가 `booked` 만 본다(W-6) |
| AX 확정·옛 `meeting.update` 의 트랜잭션 | 두 갈래 모두 `_plan_room_change`(Connect `rooms()`·`available()` HTTP · 상한 `TDL_HTTP_TIMEOUT_SECONDS` 20초)를 **액션 확정 트랜잭션 안에서** 부른다(`application.py:4046-4049,4067`). PATCH 는 트랜잭션 밖에서 부른다. 액션 행 잠금을 쥔 채 외부 호출 최대 수십 초 — 저장소 원칙(「provider 호출 중 트랜잭션을 열어 두지 않는다」)과 어긋난다 | WARN(W-2 · BE) — 계획을 확정 트랜잭션 앞으로 빼거나 `_prepare_action_effect` 자리에서 |
| WP1·WP2 영역 | `cli_process`·`meeting_worker` 는 넘겨받은 WARN 수정만. 안건 출처·기한·받기·SVG·「빠른 회의」·보정 표 경로는 diff 에 없다 | PASS |

---

## 5. 시험이 계약을 잡나

| 시험 | 판정 | 비고 |
|---|---|---|
| `T/contract/test_meeting_room_change.py`(17) | 강함 | 목록 정원·자기 예약 제외·`current`·이유·503·404·MCP / PATCH 이동·새 예약 키·재전송·취소·409·인원 409·422·장애 후 재맞춤 / 수정 카드 계약 모양·확정·409 / 옛 `meeting.update` 409 |
| | **빈틈** | **AX 가 방을 제안한 카드**(F-1) · `needs_verification` 회의의 수정(W-1) |
| `T/contract/test_action_center.py` · `test_action_policy.py` · `test_ax_work_lookup_policy.py` | 강함 | 초안 저장·거절·명령 · 정책 문장 |
| `T/contract/test_answer_resources.py`(017) | 강함 | 매 턴 실림 · 턴 사이 새 프로젝트 |
| `F/features/meetings/RoomSelect.test.tsx`(12) | 강함 | 상태 넷 · 수정 모양 · 300ms · 빠짐 · W-3 · 409 |
| `F/features/action/ActionMeetingUpdateCard.test.tsx`(9) | 보통 | 바뀐 칸만·409·거절은 강함. **계약 대역에 `proposed_room_id` 가 없어 F-1 을 못 잡는다** |
| `F/features/action/AxMeetingDraftCard.test.tsx`(9) · `MessageListMeetingCards.test.tsx`(2) | 강함 | 업무 연결 쪽 없음 · 갈래 |

---

## 6. 사람 눈에 이상해 보일 자리

| # | 자리 | 무엇이 걸리나 |
|---|---|---|
| H-1 | **AX 수정 카드의 「변경 안 함」** | F-1 — 「변경 안 함」 을 보고 등록했는데 회의실이 바뀌거나 예약이 사라진다 |
| H-2 | **긴 AX 대화가 느려진다** | 맥락 목록(WP2 셈 소규모 68KB · 1시간 가정 113KB)을 **매 턴** 싣는데, 대화는 같은 provider 세션을 이어 쓴다 → 세션 기록에 목록이 턴마다 한 벌씩 쌓인다. 몇 턴 뒤 입력 토큰·지연·비용이 크게 늘고, 문맥 한도에 닿으면 provider 오류나 자동 요약이 날 수 있다(W-3) |
| H-3 | **수정 모달에서 시간을 조금 미뤘을 뿐인데 기존 방이 「예약 불가」** | W-4 가정이 틀리면 생긴다(자기 예약과 겹침) |
| H-4 | **방 목록이 라디오 목록** | SPEC 은 「셀렉트」 — FE 는 생성 모달의 기존 라디오 모양을 그대로 넷에 썼다(DS 안). AX 생성 카드 셋째 쪽은 높이 고정이라 방이 많으면 안에서 굴린다 |
| H-5 | **AX 수정 카드의 사외 참석자 = 쉼표 글자 한 칸** | 생성 모달은 사람 단위 칩인데 카드만 쉼표 입력 — 「홍길동, 김철수」 를 띄어 쓰는 실수에 약하다(FE 미결 6) |
| H-6 | **「회의실 예약 시스템에 닿지 못했습니다」 뒤** | 회의는 바뀌고 예약은 옛 상태 — 다시 맞추는 단추 없이 「다음 수정 저장」 에서만 맞춰진다(SPEC H-1 그대로) |
| H-7 | **확인 대기 회의 수정** | W-1 — 아무 경고 없이 저장되고, 나중에 Connect 에 두 예약이 보일 수 있다 |
| H-8 | **Today 판단 대기에서 회의 생성 봉투** | 이제 쪽 나눔 카드로 연다(FE 미결 5) — 채팅과 같아 좋지만, 처음 보는 사람에겐 바뀐 모양 |

---

## 7. FAIL / WARN 목록(재발주용)

### FAIL (1) — BE + FE

| # | 자리 | 무엇 | 고칠 것 |
|---|---|---|---|
| F-1 | FE `F/features/action/ActionMeetingUpdateCard.tsx:56-83`(`draftOf` · `meetingUpdateDraft`) · BE `B/platform/actions.py:2175-2176` · `B/modules/actions/confirmation.py:206-220` · 계약 고정 1 | AX 가 제안한 방(`proposed_room_id`)을 카드가 안 보이고, 「변경 안 함」 그대로 등록하면 서버가 제안 방으로 옮긴다/취소한다 | FE: 제안 방을 미리 고르고 「AX 제안」 표지 · 「기존」 으로 되돌리면 명시적 `room` · BE: 사람의 「기존 유지」 가 제안을 이기게 · 계약 문서 갱신 · 양쪽 시험 |

### WARN (8)

| # | 팀 | 자리 | 무엇 | 권장 |
|---|---|---|---|---|
| W-1 | BE | `B/bootstrap/application.py:525-534` `_holds_seat` · `_plan_room_change` | `needs_verification` 예약을 자리 없음으로 봐서 수정이 새 예약(이중) 또는 이동 누락 | 확인 대기면 방 관련 수정을 막거나 쥔 자리로 다룬다 · 시험 |
| W-2 | BE | `B/bootstrap/application.py:4046-4049,4067` | AX 확정·옛 `meeting.update` 가 액션 트랜잭션 안에서 Connect 를 부른다(최대 20초+) | 계획을 트랜잭션 밖으로 |
| W-3 | BE(+코디 판정) | `B/bootstrap/conversation_worker.py:160` · 대화 프롬프트 | 맥락 목록을 매 턴 싣고 세션을 이어 써서 세션 기록에 목록이 쌓인다(H-2) | 실측(10턴 대화의 입력 토큰) · 필요하면 「세션의 첫 턴·새 세션에만 싣고 이어 쓰는 턴은 생략」 을 코디가 판정(OQ-1002 ② 재검토) |
| W-4 | 코디(실물) | `B/platform/the_connect.py:105` `ignoring` | 예약행 `id` = 외부 번호 가정(BE 미결 2) | 실물 1회 — 30분 미루기에 기존 방이 서는지 |
| W-5 | BE(실물) | `B/platform/the_connect.py:133-141` `update` | PUT 전 가용 확인 없음 — 재확인↔PUT 창의 겹침은 Connect 동작에 달림 | 실물 확인 · 필요하면 PUT 직전 `available(ignoring)` 한 번 |
| W-6 | FE | `F/features/meetings/MeetingEditModal.tsx:111` | 기존 방 대체 표시가 `status==="booked"` 만 — 앞 동기화가 실패해 자리를 쥔(`failed`) 회의 + 조회 실패(503)면 기존 줄이 안 선다 | `failed` + 방 이름도 기존 줄로 |
| W-7 | FE | `F/features/action/ActionMeetingUpdateCard.tsx` 사외 참석자 | 쉼표 글자 한 칸(H-5) | 2루프 시안 |
| W-8 | 문서(planner) | SPEC-010 §2.2 「셀렉트」 · 계약 고정 1 | 화면은 라디오 목록 · 계약 문서에 `proposed_room_id` 없음 | SPEC·계약 문서 정리 |

### 확인한 것 / 확인 안 한 것

- **확인한 것**
  - 계약 고정 넷을 BE·FE 코드로 대조
  - 수정 계획·실행의 갈래 전부(none·keep·move·create·cancel·clear · 실패·모름·거절)
  - 옛 `meeting.update` 경로 · AX 생성 카드의 회의 쪽 필드 · `proposed_room_id` 쓰는 곳 전수(`rg`)
  - 넘겨받은 WARN 다섯의 코드
- **확인 안 한 것**
  - 시험·빌드 실행 · 실물 Connect
  - 액션 확정 409 가 HTTP 에서 계약 고정 2 모양으로 나가는지는 BE 시험(「만석 확정 409」)을 믿었다 — 액션 라우트의 오류 매핑을 별도로 따라가지 않았다
