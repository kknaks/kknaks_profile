# WP3 BE↔FE 계약 고정 (코디 판정 2026-10-07 — FE 질문, SPEC-010 대조)

1. **AX 회의 수정 카드 편집 계약** (SPEC 에 세부 없음 → FE 안 확정): `editor="meeting_update"` · `values = {meeting_id, title, purpose, starts_at, ends_at, attendee_ids, external_attendees, room_id(지금 방 id | null), room_name(지금 방 이름 | null)}` · confirm 의 `draft` = **바뀐 칸만** + 방은 PATCH 와 같은 `room: {room_id}`(안 바꾸면 `room` 없음)
2. **수정 거절**(SPEC-010 :283 · :385 · AC-08): PATCH 와 AX 수정 확정 모두 `409` · `detail = {code: "ROOM_BOOKING_REFUSED", message, available_rooms: []}` — FE 는 409 + `available_rooms` 배열이면 거절로 본다(생성의 `room_unavailable` 도 그대로)
3. **저장 때 Connect 장애**(SPEC-010 :283): 회의는 바뀌고 응답 `meeting.room_reservation = {status: "failed", reason: "reservation_unavailable"}` → 화면 「회의실 예약 시스템에 닿지 못했습니다」
4. **회의실 목록**(SPEC-010 :258-259 · :388): 인자 `starts_at, ends_at, people, meeting_id` · 항목 `{room_id, name, capacity, available, current, unavailable_reason}` · Connect 에 닿지 않으면 `503 detail={code: "ROOM_SERVICE_UNAVAILABLE"}` · 계정 env 없음은 `200 []`

## 갱신 (WP3 검수 F-1 · 코디 판정 2026-10-07)

5. **AX 가 제안한 방** — 편집 계약 values 에 `proposed_room_id`(·`proposed_room_name`)를 더한다. 카드는 **제안 방을 미리 골라 두고 「AX 제안」 표지**를 단다. 사람이 「기존 — 변경 안 함」 으로 되돌리면 draft 에 **명시적 `room: {keep: true}`**(또는 현재 `room_id`)를 싣는다. 서버는 **draft 의 사람 선택이 언제나 AX 제안을 이긴다** — draft 에 `room` 이 없으면 「바꾸지 않음」 이다(제안을 적용하지 않는다)

## 갱신 2 (WP3 재검수 F-r2-1 · 코디 판정 2026-10-07)

6. **「AX 가 방을 제안했는가」 는 `room_proposed: bool` 로 따로 싣는다** — `proposed_room_id: null` 만으로는 「예약 없음 제안」 과 「제안 없음」 을 가를 수 없다. `room_proposed=false` 면 카드는 **기존 방을 그대로** 고른 채 연다(제안 표지 없음). `room_proposed=true` 일 때만 `proposed_room_id`(null = 「예약 없음」 제안)를 미리 고르고 「AX 제안」 표지
7. **`409 ROOM_RESERVATION_UNCONFIRMED`** — `detail = {code, message}`(available_rooms 없음). 화면 문구 = 「회의실 예약을 아직 확인 중입니다 — 잠시 뒤 다시 시도해 주세요」 · 회의실을 건드리지 않는 수정은 이 오류를 내지 않는다
