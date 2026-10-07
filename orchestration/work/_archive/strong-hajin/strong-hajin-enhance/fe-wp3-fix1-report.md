# WP3 수정 1 결과 보고 (frontend)

## 상태: done

- 근거: `review-wp3-code-report.md`(F-1 · W-6) · `wp3-contract-fixed.md` **§5(갱신)** · 지시서 `fe-wp3-fix1-instructions.md`
- 워크트리 `strong-hajin-enhance` · 커밋 없음 · W-7(사외 참석자 입력 모양)은 손대지 않음(2루프)

## 1. 고친 것

| # | 검수 | 구현 위치(`frontend/src/` 기준) |
|---|---|---|
| F-1 | AX 가 제안한 회의실이 카드에 안 보이는데 확정은 그 방으로 옮겼다 — 카드가 `proposed_room_id` 를 읽지 않았다 | `features/action/ActionMeetingUpdateCard.tsx` — 제안 읽기 `proposedRoomOf` `:57`(칸 없음 = 제안 없음 · `null` = 「예약 없음」 제안 · 지금 방과 같은 번호 = 제안 아님) · 지금 방 `currentRoomOf` `:66` · **제안 방을 미리 고름** `draftOf` `:84` · **「AX 제안」 표지** — 회의실 라벨 옆 `Badge` `:294`(지금 골라진 것이 제안일 때만 · 「AX 제안 · {방 이름}」, 이름은 `proposed_room_name`, 「예약 없음」 제안이면 그 문구) · `meetingUpdateDraft` `:96~` — 비교 기준은 **지금 방**(제안이 아님): 제안을 고른 채 [등록] = `room: {room_id: 제안}` · 사람이 「기존 (변경 안 함)」 으로 되돌림 = **명시적 `room: {keep: true}`** `:108` · 「예약 없음」 = `room: {room_id: null}`(지금 방이 있거나 제안이 있었을 때) · 다른 방 = `room: {room_id: n}` · 제안이 없고 「기존」 그대로면 `room` 없음(서버: 없으면 「바꾸지 않음」). 문구 `lib/labels.ts:1410-1411` |
| W-6 | 수정 모달의 기존 방 대체 표시가 `status === "booked"` 만 봤다 — 앞 동기화 실패 + 조회 503 이면 기존 줄이 안 서고 「예약 없음」 으로 열렸다 | `features/meetings/MeetingEditModal.tsx` — `heldRoomName` `:42`(`booked` **또는 `failed`** 이면서 `room_name` 이 있으면 쥔 방) · 처음 고름 `:107`(그 방이 있으면 「기존」) · 셀렉트의 기존 줄 이름 `:122` |

## 2. 새 시험 (7개)

| 파일 | 시험 |
|---|---|
| `features/action/ActionMeetingUpdateCard.test.tsx` (+5) | 제안 방이 미리 골라지고 「AX 제안 · 회의실 1 (8인)」 표지 · 「기존」 은 안 골라짐 · 그대로 [등록] = `{room:{room_id:1}}` / 「기존」 으로 되돌리면 표지가 사라지고 `{room:{keep:true}}` / `proposed_room_id: null` = 「예약 없음」 미리 고름 + 표지 + `{room:{room_id:null}}` / 제안이 지금 방과 같으면 표지 없음 · `room` 없음 / 제안 칸이 없는 계약은 지금처럼(`room` 없음) |
| `features/meetings/MeetingEditModal.test.tsx` (+2) | `failed` + `room_name` + 조회 503 → 「기존 — 회의실 3 (확인 못 함)」 이 골라진 채 열림 · 안 바꾸면 저장 막힘(예약을 조용히 지우지 않음) / `failed` + `room_name: null` → 기존 줄 없음 |

## 3. 검증 — 돌린 시험 파일과 수치(직렬 · 관련 파일만)

| 시험 파일 | 결과 |
|---|---|
| `features/action/ActionMeetingUpdateCard.test.tsx` | 14/14 |
| `features/meetings/MeetingEditModal.test.tsx` | 20/20 |
| `features/meetings/RoomSelect.test.tsx` | 12/12 |
| `features/meetings/MeetingList.test.tsx` | 42/42 |
| `features/action/AxMeetingDraftCard.test.tsx` | 9/9 |
| `features/chat/MessageListMeetingCards.test.tsx` | 2/2 |
| `lib/labels.test.ts` | 10/10 |
| **합계** | **7 파일 · 109/109** |

- 빌드 `make frontend-build` 통과 · `tsc -b` 0 오류
- 전체 시험은 돌리지 않았다(코디 지시)

## 4. 미결 · 주의점

1. **BE 쪽 F-1 짝** — 계약 고정 §5: 편집 계약 `values` 에 `proposed_room_id`(·`proposed_room_name`)를 싣고, **draft 의 사람 선택이 언제나 제안을 이기며 draft 에 `room` 이 없으면 바꾸지 않는다**(지금 `merge_meeting_update_draft` 가 제안의 `changes.room` 을 남기는 갈래를 걷어야 한다). `room: {keep: true}` 를 받는 것도 BE 몫이다. 화면은 그 모양을 그대로 보낸다
2. `proposed_room_name` 이 오지 않으면 표지는 「AX 제안」 만 선다(방 이름은 셀렉트 줄에 이미 보인다)
3. 제안 방이 새 시간·인원에 못 쓰는 방이면(목록에 없음) 셀렉트가 「고른 회의실 「N」 은 … 다시 골라 주세요」 를 보이고 [등록]을 막는다(기존 `RoomSelect` 규칙) — 조용히 다른 방이나 「예약 없음」 으로 가지 않는다
4. AX **생성** 카드는 제안 방이 `values.room_id` 자체라(생성엔 «지금 방» 이 없다) 이번 수정 대상이 아니다 — 검수도 PASS
