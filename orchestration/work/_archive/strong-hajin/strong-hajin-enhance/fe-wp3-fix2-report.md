# WP3 수정 2 결과 보고 (frontend)

## 상태: done

- 근거: `review-wp3-r2-report.md` · 계약 `wp3-contract-fixed.md` **§6 · §7** · 지시서 `wp3-fix2-instructions.md`(frontend 몫 셋)
- 워크트리 `strong-hajin-enhance` · 커밋 없음

## 1. 고친 것 (`frontend/src/` 기준)

| # | 검수 | 구현 위치 |
|---|---|---|
| F-r2-1 | `proposed_room_id: null` 만으로는 「예약 없음 제안」 과 「제안 없음」 을 못 가른다 — 시간만 바꾸자는 제안에서도 카드가 「예약 없음」 을 미리 골라 그대로 등록하면 예약이 취소될 수 있었다 | `features/action/ActionMeetingUpdateCard.tsx` `proposedRoomOf` `:59-60` — **`values.room_proposed === true` 일 때만 제안**(§6). 그때만 `proposed_room_id` 를 미리 고르고(`null` = 「회의실 예약 없음」) 「AX 제안」 표지. `false`·칸 없음 = 기존 방 그대로 · 표지 없음 · 그대로 [등록]하면 `room` 없음(수정 1 의 「`proposed_room_id` 칸이 있으면 제안」 판정을 걷었다) |
| W-r2-1 | `409 ROOM_RESERVATION_UNCONFIRMED` 문구(§7) — 코드별 문구, 모르는 코드는 `detail.message` | 문구 `lib/labels.ts:910`(`meetingScreen.saveErrors.ROOM_RESERVATION_UNCONFIRMED` 「회의실 예약을 아직 확인 중입니다 — 잠시 뒤 다시 시도해 주세요」) · 판정 `features/meetings/BookingModal.tsx:43` `meetingErrorText`(코드별 문구 → `detail.message` → 오류 글자 → 기본 문구. 겹침 409 처럼 `detail` 이 문자열이면 그대로 — K22) · 쓰는 곳 둘: 수정 모달 `MeetingEditModal.tsx:190` · AX 수정 카드 `ActionMeetingUpdateCard.tsx:161`. 거절(`available_rooms`)이 아니므로 셀렉트는 건드리지 않는다 — 고른 방 그대로 다시 저장할 수 있다 |
| W-r2-4 | 수정 모달 기존 줄 대체 표시에 `needs_verification` + 방 이름도 | `MeetingEditModal.tsx:46` `heldRoomName` — `booked` · `failed` · **`needs_verification`** 이면서 `room_name` 이 있으면 쥔 방 |

## 2. 새 시험 (6개) · 고친 시험

| 파일 | 시험 |
|---|---|
| `features/action/ActionMeetingUpdateCard.test.tsx` (+4) | **방 있는 회의 + 시간만 제안**(`room_proposed:false` · `proposed_room_id:null`) → 「기존」 그대로 · 표지 없음 · 그대로 등록 = `room` 없음 / `room_proposed` 칸 없음 + `proposed_room_id: 1` → 제안 아님 / 확정 409 `ROOM_RESERVATION_UNCONFIRMED` → §7 문구 · 고른 방 그대로 · [등록] 다시 가능 / 모르는 코드 409 → `detail.message` |
| `features/meetings/MeetingEditModal.test.tsx` (+2) | `needs_verification` + 방 이름 + 조회 503 → 「기존 — 회의실 3 (확인 못 함)」 에서 열림 / 저장 409 `ROOM_RESERVATION_UNCONFIRMED` → §7 문구 · 모달 그대로 |
| 고친 것 | `ActionMeetingUpdateCard.test.tsx` 의 수정 1 시험 다섯(제안 방 · 「기존」 으로 되돌림 · 예약 없음 제안 · 지금 방과 같은 제안 · 제안 칸 없음)의 대역에 `room_proposed: true` 를 더함(§6) — 단언은 그대로 |

## 3. 검증 — 돌린 시험 파일과 수치(직렬 · 관련 파일만)

| 시험 파일 | 결과 |
|---|---|
| `features/action/ActionMeetingUpdateCard.test.tsx` | 18/18 |
| `features/meetings/MeetingEditModal.test.tsx` | 22/22 |
| `features/meetings/MeetingList.test.tsx` | 42/42 |
| `features/meetings/RoomSelect.test.tsx` | 12/12 |
| `features/action/AxMeetingDraftCard.test.tsx` | 9/9 |
| `features/chat/MessageListMeetingCards.test.tsx` | 2/2 |
| `lib/labels.test.ts` | 10/10 |
| **합계** | **7 파일 · 115/115** |

- 빌드 `make frontend-build` 통과 · `tsc -b` 0 오류 · 전체 시험은 돌리지 않았다(코디 지시)

## 4. 미결

1. BE 짝(같은 지시서의 backend 몫): 편집 계약 `values.room_proposed`(회의실을 바꾸자고 했을 때만 true · 「예약 없음」 제안도 true) — 화면은 이 칸이 true 일 때만 제안으로 본다. BE 가 아직 싣지 않으면 카드는 언제나 기존 방에서 연다(안전한 쪽)
2. `ROOM_RESERVATION_UNCONFIRMED` 는 수정 모달·AX 수정 카드 두 자리에서만 문구를 가린다. 생성(`bookMeeting`)은 이 오류를 내지 않는다(§7 — 회의실 수정 경로 오류)
