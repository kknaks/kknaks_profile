# 재검수 r2 — WORK-012 WP3 수정 1

- 검수자: reviewer(read-only) · 2026-10-07
- 대상: `be-wp3-fix1-report.md` · `fe-wp3-fix1-report.md` 가 적은 변경(`e58fb25` 뒤 미커밋 diff 중 수정분)
- 계약: `wp3-contract-fixed.md` §1~5
- 코디 판정(판정 대상 아님)
  - W-5 = 200 + `room_reservation.failed`
  - W-3 = 맥락 목록은 새 provider 세션 턴에만
  - W-7 = 2루프
- 한 일: 코드 읽기 · `rg`. **시험·빌드·실물은 돌리지 않았다** — 워커 수치: BE 417 + postgres 46 · FE 7파일 109/109
- 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/`

---

## 0. 판정 — **FAIL**(BE↔FE §5 의 `null` 해석이 갈린다 · 새로 생김)

1차의 F-1 · W-1 · W-2 · W-3 · W-5 · W-6 는 각자로는 모두 고쳐졌다. 그런데 F-1 을 고치면서 **양쪽이 `proposed_room_id: null` 을 다르게 읽게 됐다.**

- **BE**: 제안이 없을 때도 이 칸을 **언제나 `null` 로 싣는다.**
- **FE**: 칸이 있고 `null` 이면 **「회의실 예약 없음」 제안**으로 읽는다.

결과: **방이 잡힌 회의에 AX 가 시간·참석자만 바꾸자고 한 모든 수정 카드**(가장 흔한 「1시간 미뤄 줘」)가 이렇게 된다.
1. 「회의실 예약 없음」 이 「AX 제안」 표지와 함께 미리 골라진다
2. 사람이 그대로 [등록]한다
3. FE 가 `room: {room_id: null}` 을 보낸다
4. 서버가 **예약을 취소하고 장소를 비운다**

1차 F-1 보다 넓은 결함이다(그때는 제안이 있는 카드만이었다). **FAIL 1 · WARN 4.**

---

## 1. 1차 지적 — 항목별

| # | 1차 지적 | 지금 | 판정 |
|---|---|---|---|
| F-1 BE 쪽 | 확정이 제안의 `room` 을 적용 | `merge_meeting_update_draft` 가 제안의 `room` 을 버리고 **draft 의 `room` 만** 쓴다(`B/modules/actions/confirmation.py:206-230`) — `room` 없음 = 안 바꿈 · `room:{keep:true}` = 유지 · `keep`+`room_id` 422 · `{}` 422(`B/modules/meetings/commands.py:175-236`)<br>계약 `values.proposed_room_id`·`proposed_room_name`(`B/platform/actions.py:2178-2186`) | PASS(단 §2 F-r2-1) |
| F-1 FE 쪽 | 카드가 제안을 안 봄 | `proposedRoomOf`(`F/features/action/ActionMeetingUpdateCard.tsx:57-63`) · 미리 고름 `draftOf` `:84` · 「AX 제안」 표지 `:294` · 되돌리면 `room:{keep:true}` `:108` | PASS(단 §2 F-r2-1) |
| W-1 | `needs_verification` 을 빈 자리로 봄 | 외부 번호가 **있으면** 쥔 자리(`_holds_seat` `B/bootstrap/application.py:528-539` — 같은 예약을 PUT·DELETE 로 다시 맞춤). **없으면** `_unconfirmed_seat`(`:542-549`) → 방에 닿는 수정(방 선택·시각·인원)을 `409 ROOM_RESERVATION_UNCONFIRMED` 로 막는다(`:1238-1243`). 제목·목적만이면 통과 · AX 확정·옛 `meeting.update` 도 같은 계획 | PASS(W-r2-1) |
| W-2 | 액션 트랜잭션 안에서 Connect 호출 | 계획을 둘로 나눴다 — `_room_plan_intent`(DB) · `_recheck_room_plan`(Connect)<br>트랜잭션 안의 `_plan_room_change_in_action`(`:1273-1294`)은 밖에서 끝낸 재확인이 없으면 `_RoomRecheckNeeded` 를 던진다<br>입구 `run_action_command` `:3871` · `decide_action` `:4754` 의 `_run_with_room_recheck`(`:1296-1315`)가 되돌린 뒤 밖에서 재확인 → 열쇠(회의·동작·방·외부 번호·시각·인원)로 짧게 재실행 · 3회 넘으면 `MeetingStateConflict` | PASS(§3) |
| W-3 | 매 턴 맥락 목록이 세션에 쌓임 | `context_catalog = … if session_ref is None else None`(`B/bootstrap/conversation_worker.py:163`) — 첫 턴·세션을 새로 여는 턴(`reset_provider_session` 포함)만 · 정책 문구 「세션을 연 턴의 목록 · 없으면 도구로」 | PASS |
| W-5 | PUT 전 가용 확인 없음 | 어댑터 `update` 가 `room_id` 가 있으면 PUT 직전 `available(ignoring=자기 외부 번호)` → 차면 PUT 없이 `RoomUnavailable`(`B/platform/the_connect.py:142-149`) → 실행이 `failed` + `reason=ROOM_BOOKING_REFUSED` · **옛 외부 번호·방·장소 보존**(`application.py:1486~`) → 응답 200 + `room_reservation.failed`(코디 판정과 같음) | PASS |
| W-6 | 수정 모달 기존 방 대체 표시가 `booked` 만 | `heldRoomName`(`F/features/meetings/MeetingEditModal.tsx:42`) = `booked`·`failed` + 이름 · 처음 고름 `:107` · 기존 줄 이름 `:122` | PASS(참고: 서버는 이제 `needs_verification`+외부 번호도 쥔 자리로 본다 — FE 대체 표시는 그 상태를 안 본다. 503 과 겹칠 때만 드러나는 경미한 차이) |

---

## 2. 새 FAIL

### F-r2-1 (FAIL · BE+FE · 코디 판정 필요) — `proposed_room_id: null` 의 뜻이 양쪽에서 다르다

- **BE**(`B/platform/actions.py:2180-2186`):
  - `proposed = changes.get("room") …`
  - `values["proposed_room_id"] = None if proposed is None else proposed.get("room_id")` → **제안이 없어도 키가 있고 값은 `null`**
  - BE 리포트 §5-2 도 「「예약 없음」 제안과 「제안 없음」 이 구별되지 않는다」 고 적었다
- **FE**(`ActionMeetingUpdateCard.tsx:57-63`):
  - `"proposed_room_id" in values` 가 거짓일 때만 「제안 없음」
  - 키가 있고 값이 비면, 지금 방이 있을 때 **`"none"` = 「예약 없음」 제안**으로 읽는다
  - FE 리포트 §1 「칸 없음 = 제안 없음 · `null` = 「예약 없음」 제안」
- **맞물림 결과**: 방이 잡힌 회의 + AX 가 방을 언급하지 않은 수정 제안이면 아래가 된다. 서버는 「draft 의 사람 선택이 이긴다」 규칙대로 그 `null` 을 사람 선택으로 실행한다.
  - `draftOf.room = "none"` + 「AX 제안 · 회의실 예약 없음」 표지
  - 그대로 [등록] → `meetingUpdateDraft` 가 `room: {room_id: null}`(`:109-110`) → `cancel`(DELETE · 장소 비움)
- **시험이 못 잡은 이유**:
  - FE 시험의 「제안 칸이 없는 계약은 지금처럼」 은 **키를 빼고** 만들었다
  - BE 시험은 FE 를 거치지 않는다
  - 실제 BE 가 내는 모양(키 있음 · `null`)으로 FE 를 돌린 시험이 없다
- **고칠 것**(코디가 하나를 고른다 → 계약 §5 문구 고정):
  - (가) **BE**: 제안이 없으면 `proposed_room_id`·`proposed_room_name` 키를 **싣지 않는다**. 「예약 없음」 제안만 키 + `null`. FE 는 그대로.
  - (나) **양쪽**: `room_proposed: bool` 을 더하고 FE 는 그것으로만 제안 여부를 판정한다.
  - 시험: **BE 의 실제 편집 계약 응답 모양**(제안 없음 · 방 제안 · 예약 없음 제안 셋)을 FE 카드에 넣어 「그대로 등록 = 무엇이 나가나」 를 단언한다. BE 에도 「제안 없음이면 키 없음(또는 `room_proposed=false`)」 시험.

---

## 3. 새로 생긴 위험

### 3-1 W-2 「되돌림 → 밖 재확인 → 짧은 재실행」

| 물음 | 본 것 | 판정 |
|---|---|---|
| 두 번 실행 | 첫 실행은 `_RoomRecheckNeeded` 로 **커밋 전에** 끝나고, `_rollback_action_session`(`application.py:3934-3942`)이 세션을 되돌리며 커밋 뒤 훅(`scax_after_commit`)도 버린다. 확정의 외부 반영(PUT·POST·DELETE)은 커밋 뒤 훅이라 첫 실행에서는 나가지 않는다 | PASS |
| 부분 적용 | `meeting.info.update` 갈래는 계획을 **가장 먼저** 부른다(`:4174` · 옛 `meeting.update` `:4194`). 회의 정보 변경·감사 기록은 그 뒤라 되돌릴 것이 없다 | PASS |
| 되돌림 보상 훅 | `_rollback_action_session` 은 `scax_after_rollback` 보상 훅을 돈다. 회의 수정 갈래는 계획 전에 외부 효과를 내지 않으므로 보상할 것이 없다(회의 생성 울타리는 다른 종류 · 이 경로 안 탐) | PASS |
| 그 사이 회의 변경 | 열쇠에 시각·인원·외부 번호가 들어 있어 달라지면 다시 재확인 · 3회 제한 | PASS |
| 고리 밖 호출 | `_ROOM_RECHECKS` 가 없으면(입구 둘을 거치지 않은 직접 실행) 예전처럼 안에서 재확인한다 — 시험·내부 경로용 안전망. 제품 입구는 HTTP·MCP 모두 `run_action_command`/`decide_action` 을 지난다(`http.py:1464,2502` · `mcp.py:442,1607` · `demo_work.py:71`) | PASS |

### 3-2 새 오류 `409 ROOM_RESERVATION_UNCONFIRMED` 가 FE 에서

- **BE 응답**: `detail = {code: "ROOM_RESERVATION_UNCONFIRMED", message}` — `available_rooms` 없음(`http.py:557`)
- **FE `roomRejectionOf`**(`F/features/meetings/BookingModal.tsx:39-46`):
  - `meetingScreen.roomRejected` 에 이 코드가 **없고**(`F/lib/labels.ts:911-917`) `available_rooms` 도 없어 `null` 을 돌려준다
  - 그래서 거절로 보지 않고 일반 오류로 간다
- **일반 오류 문구**: `request()`(`F/lib/api.ts:165-168`)는 `detail` 이 문자열일 때만 메시지로 쓰고, 아니면 `response.statusText` 다.
  - HTTP/1.1 이면 영어 「Conflict」
  - HTTP/2(ingress)면 **빈 글자**
  - BE 가 실어 보낸 한국어 `message` 는 화면에 안 나온다
  - 수정 모달·AX 수정 카드 모두 같은 길이다
- **판정 → W-r2-1(FE)**: `roomRejected` 에 `ROOM_RESERVATION_UNCONFIRMED` 문구를 더하거나, `detail.message` 가 있으면 그것을 쓴다. 셀렉트는 그대로 둔다(가능 방 목록이 아니므로 `refused` 로 바꾸지 않는다). 계약 고정 문서에도 이 코드를 올린다(코디).

### 3-3 그 밖

| 자리 | 본 것 | 판정 |
|---|---|---|
| `needs_verification` + 외부 번호 = 쥔 자리 | 결과 모름이 **DELETE(취소)** 에서 났으면, 그 외부 예약은 이미 지워졌을 수 있다. 다음 수정의 PUT 은 404 류 → `failed`(외부 번호 보존) → 다시 수정해도 같은 실패가 되풀이된다. 사람에겐 「예약 시스템에 닿지 못했습니다」 가 계속 뜬다 | WARN(W-r2-2 · BE · 드묾) — PUT/DELETE 가 「없음」 이면 자리를 비운 것으로 확정 |
| 영수증 복구와 사람 수정 | 확인 대기를 푸는 복구 경로(`_sync_room_reservation` · 영수증)와 사람의 PATCH 가 같은 회의에 겹치면, `_room_sync_lock` 으로 반영은 줄 서지만 **계획(재확인)은 락 밖**이라 옛 상태로 세운 계획이 실행될 수 있다 | WARN(W-r2-3 · BE · 드묾) — 실행 직전 예약 상태가 계획 때와 같은지 한 번 대조 |
| W-3 정책 문구 | 이어 쓰는 턴에는 목록이 없다 — 세션 기억에 기댄다. provider 가 세션을 요약·압축하면 목록이 흐려질 수 있다(정책이 「없으면 도구로」 로 받친다) | 참고 |
| W-5 시간만 이동 | `room_id` 가 없으면 확인을 건너뛴다 — 부르는 쪽(`_execute_room_plan_locked` 의 `move`)은 언제나 `room_id` 를 준다(`target_room_id`) | PASS |

---

## 4. FAIL / WARN 목록(재발주용)

### FAIL (1)

| # | 팀 | 자리 | 무엇 | 고칠 것 |
|---|---|---|---|---|
| F-r2-1 | BE+FE(+코디 판정) | BE `B/platform/actions.py:2180-2186` · FE `F/features/action/ActionMeetingUpdateCard.tsx:57-63,103-111` · 계약 §5 | 제안이 없어도 BE 는 `proposed_room_id: null` 을 싣는데, FE 는 그것을 「예약 없음」 제안으로 읽어 미리 고른다 → 방 있는 회의의 AX 시간 수정을 그대로 등록하면 **예약 취소** | (가) BE 가 제안 없을 때 키를 빼거나 (나) `room_proposed: bool` — 코디가 정해 계약 §5 에 적는다 · BE 실제 응답 모양으로 FE 시험 |

### WARN (4)

| # | 팀 | 자리 | 무엇 | 권장 |
|---|---|---|---|---|
| W-r2-1 | FE(+코디) | `F/features/meetings/BookingModal.tsx:39-46` · `F/lib/labels.ts:911-917` · `F/lib/api.ts:165-168` | `409 ROOM_RESERVATION_UNCONFIRMED` 가 「Conflict」/빈 글자로 보인다 | 코드별 문구 추가 또는 `detail.message` 사용 · 계약 문서에 코드 추가 |
| W-r2-2 | BE | `B/bootstrap/application.py:528-539` | 결과 모르는 **취소**의 외부 번호를 쥔 자리로 다시 맞추면 없는 예약에 PUT 이 되풀이된다 | 「없음」 응답이면 자리를 비운 것으로 확정 |
| W-r2-3 | BE | 계획(락 밖) ↔ 영수증 복구 | 계획과 실행 사이 예약 상태 변경 미대조 | 실행 직전 상태 대조(경미) |
| W-r2-4 | FE | `F/features/meetings/MeetingEditModal.tsx:42` | 대체 표시가 `needs_verification`+이름을 안 본다(서버는 쥔 자리로 본다) — 503 과 겹칠 때만 | `needs_verification` 도 포함(경미) |

### 확인한 것 / 확인 안 한 것

- **확인한 것**
  - 수정분 코드 전부
  - §5 의 BE 방출 모양과 FE 해석을 줄 단위로 대조
  - W-2 되돌림·훅·보상·열쇠·입구 전수
  - 새 409 의 FE 경로(거절 판정 → 일반 오류 → `statusText`)
- **확인 안 한 것**
  - 시험·빌드 실행 · 실물 Connect
  - 운영 ingress 가 HTTP/2 인지(빈 `statusText` 여부)
