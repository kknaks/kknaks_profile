# WP3-FE 결과 보고 (frontend)

## 상태: done

- 워크트리 `strong-hajin-enhance` · WP1 `e51fe3b` · WP2 `e58fb25` 위 · 커밋·push 없음(변경은 워크트리에만). `git status` 의 `backend/` 변경은 병렬 BE 워커 것이다(이 판은 `frontend/src/` 만)
- 계약: WORK-012 「Phase WP3-FE」 + SPEC-010 §2.2 · §2.4 · §4.1 · §4.3 · §4.4 + **WP3 계약 고정**(`wp3-contract-fixed.md` — FE 가 물은 넷: 수정 카드 편집 계약 · 409 · 저장 때 Connect 장애 · 목록 503/항목)
- 검증 범위 = **바꾼 부분 관련 시험 파일만**(코디 지시 — 전체 시험은 마지막에 코디)

## 1. 계약 체크박스별 구현 위치 — 5/5 (+ W-3)

| # | 계약 | 구현 위치(파일:줄 — `frontend/src/` 기준) |
|---|---|---|
| 1 | **회의실 셀렉트 부품 하나** — 생성 모달 · 수정 모달 · AX 생성 카드 · AX 수정 카드. 수정만 맨 위 기존 줄 · 구분선 · 「회의실 예약 없음」 · 가용 목록 · 비활성+이유 · 「가용 없음」/「조회 실패 — 다시 시도」 · 조건 바뀌면 다시 받기(300ms) | 새 부품 `features/meetings/RoomSelect.tsx` — 조회 `:78-109`(첫 조회는 바로, 그 뒤 `setTimeout(load, 300)` `:105` · 503 포함 모든 실패 = 「조회 실패」) · 기존 줄(수정만 — `meetingId` 가 있을 때, 목록의 `current` 또는 `currentName`) · 비활성+이유(`time_conflict` 「새 시간에 예약 불가」 · `capacity` 「새 인원보다 작은 방」) · 조회 실패면 「(확인 못 함)」 으로 고를 수 있음 · 구분선 `:184` · 거절 목록(`refused`) · 고른 방이 목록에서 빠짐 · 불러온 방 요청(`requestedName`) · 막힘 판정 `:144` → `onStatus({state, blocked, reason})`. API `lib/api.ts:1483`(`starts_at,ends_at,people,meeting_id`) · 타입 `lib/viewModels.ts`(`MeetingRoom` 에 `available·current·unavailable_reason`) · 문구 `lib/labels.ts:864-883`(OQ-1017 기본값) · CSS `styles/meetings.css`(`.meeting-room-select` · `.meeting-room.disabled` · `__reason` · `-sep` · `-note`). **쓰는 자리 넷**: `BookingModal.tsx:551` · `MeetingEditModal.tsx:253` · `AxDraftCard.tsx`(셋째 쪽 — `MeetingPageBody` `:214` 의 `roomSlot`) · `ActionMeetingUpdateCard.tsx:257` |
| 2 | 수정 모달 장소 글자 칸 → 셀렉트(OQ-1005) · 바뀐 값만 보내기(OQ-1010) · 기존 방 비활성일 때 [저장] 옆 이유 한 줄(H-2 · OQ-1016) · 조회 실패 중 저장 결과 줄(H-1) | `features/meetings/MeetingEditModal.tsx` — 기존 방 `:111`(`room_reservation.status === "booked"` 의 방 이름) · `#meeting-head-place` 삭제 → 셀렉트 `:253` · 바뀐 값만 `changedPatch` `:129-146`(제목 · 시각 둘 · 참석자 · 방은 「기존」 이면 `room` 없음 / 「예약 없음」 = `{room_id:null}` / 다른 방 = `{room_id:n}`) · 새 예약이 날 수 있는 저장은 `Idempotency-Key`(같은 내용이면 같은 키) `:148~` · [저장] 옆 이유 `:303`(셀렉트가 막으면 [저장] 비활성) · H-1 / 저장 때 Connect 장애(계약 고정 3) 문구 `:166` · 409 거절 → 셀렉트를 가능한 방으로 · 값은 `"unset"`(조용히 「예약 없음」 으로 옮기지 않음) · 판정은 생성과 같은 `roomRejectionOf`(`BookingModal.tsx:39` — 409 + 아는 코드 또는 `available_rooms` 배열 · 계약 고정 2). `updateMeetingInfo` 에 `room` · 멱등 키 인자 `lib/api.ts:1258-1268` |
| 3 | **AX 회의 생성 카드를 `AxDraftCard` 틀로** — 쪽 나눔(기본 정보 · 참석자 · 회의실·안건 · 자료) · AX 배지·회차 · 거절 · 수정(편집 창 → 초안 저장) · 등록 · 접힌 한 줄 「회의 열기」 | `features/action/AxDraftCard.tsx` — kind 셋 `:40`(+ `ax.meeting.reservation.create`) · kind↔편집기 맞춤 `:44-46`(회의 = `meeting` 편집기) · `isAxTaskDraftKind` `:53`(내 업무 「AX 제안」 칩은 업무 초안만 — `MyWorkPage.tsx` 가 이것을 쓴다) · 회의 쪽 `MeetingPageBody` `:214-271`(기본 정보: 회의명·날짜·시간(KST)·주최자(미리보기 `host`)·목적 / 참석자: 사내·사외 / 회의실·안건: 셀렉트 + 안건(넘어온 것 표시) / 자료) · 회의실 조회 조건 `:273` · 제안 방 미리 고름 `:367` · 카드에서 방만 바꾸면 그 값을 초안으로 `:372`·`:407` · 등록 뒤 접힌 한 줄 + 「회의 열기」 `:438~` · [수정] = `BookingModal` 편집 창 `:592~`(「저장」 = `save_draft` 회차+1 · 첨부 초안은 `TaskAttachmentGroup` 을 편집 창에 꽂아 업무 카드와 같은 길 — D-05). `BookingModal` 편집 창 모드 `features/meetings/BookingModal.tsx`(`BookingDraft` — 계약 값으로 채움 · 지난 회의 제안 숨김 · 주 단추 「저장」 · 회의를 만들지 않고 `draft.onSubmit`). 거절은 업무 카드와 같은 단추·사유 규칙(기존 코드 그대로 회의에도 선다). 문구 `lib/labels.ts:1396~`(`meetingPages` 등) · CSS `styles/ax.css`(셋째 쪽만 안에서 굴림) |
| 4 | **AX 회의 수정 카드를 새로 그린다** — 결과 카드 대신 편집 카드(필드 + 셀렉트 수정 모양 · 장소 글자 칸 없음 · 초안 저장·회차 없음) | 새 부품 `features/action/ActionMeetingUpdateCard.tsx` — 편집 계약 `editor="meeting_update"`(계약 고정 1 · 타입 `lib/viewModels.ts:894-895`) · 칸 = 회의명 · 목적 · 날짜 · 시간 · 참석자(사내 `MultiSelect` · 사외 글자 — 쉼표) · 회의실 셀렉트(수정 모양 — `values.meeting_id`·`room_name`) · 장소 글자 칸 없음 · 회차·[수정] 없음 · [거절](사유 규칙 같음) · [등록]의 `draft` = **바뀐 칸만** + `room:{room_id}`(`meetingUpdateDraft` `:69`) · 409 거절 → 셀렉트 다시 · 다시 고를 때까지 막힘 `:118` · 등록 뒤 한 줄 + 「회의 열기」. 갈래 `features/chat/MessageList.tsx:318-325`(AX 초안 카드 다음 · 결과 카드보다 앞) · 회의 생성 카드에도 「회의 열기」 를 넘김 `:314` |
| 5 | 생성 모달 「회의실 선택 안 함」 → 「회의실 예약 없음」 | `lib/labels.ts:864`(`noRoom`) · 주석 `lib/api.ts`(생성 `room_id` 설명) |
| W-3 | WP1 검수: 불러오기 뒤 지난 회의 방이 새 시간에 없으면 조용히 「예약 없음」 이 되지 않게 이유를 보인다 | `BookingModal.tsx` `applySuggestion` — 방을 이름으로 **요청**만(`setRequestedRoom`) → 셀렉트가 그 시간·인원의 가용 목록에서 찾으면 고르고, 못 쓰면 「지난 회의의 회의실 「X」 은 이 시간·인원에 예약할 수 없습니다」 한 줄(`RoomSelect.tsx` `requestedGone` `:141`). 같은 결로 **고른 방이 조건 변경 뒤 목록에서 빠지면** 「고른 회의실 「X」 은 … 다시 골라 주세요」 + 만들기·저장이 막힌다(`BookingModal.tsx:217` `ready` 에 `!roomStatus.blocked`) |

## 2. Code Surface WP3 표 대비 닿은 자리

| 무엇(표) | 다시 셈 / 닿은 자리 |
|---|---|
| 회의실 `readMeetingRooms…` — 화면 `api.ts:1468-1471` · `BookingModal.tsx:36-39,124-160,506-525` · 문구 `labels.ts:860,872~` | `api.ts`(인자 넷) · `BookingModal` 의 자체 조회 effect·라디오 목록을 **지우고** `RoomSelect` 하나로 · `roomRejectionOf` 를 내보내 수정 모달·수정 카드가 같이 씀 · 문구 `noRoom` 바꿈 + 셀렉트 문구. 지금 prod 의 `readMeetingRooms` 호출은 `RoomSelect.tsx:85` 한 곳(정의 `api.ts:1483`) · 시험 12 파일이 모킹 |
| 초안 저장·카드 판별 `AX_DRAFT_KINDS · axDraftFromAction · ActionMeetingCard` — 화면 `AxDraftCard.tsx:35-64` · `MessageList.tsx:6-7,295-333` · `ActionMeetingCard.tsx:101~` | `AxDraftCard.tsx`(kind·편집기·쪽·명령) · `MessageList.tsx`(회의 수정 갈래 + 회의 생성 카드에 `onOpenMeeting`). `ActionMeetingCard` 는 **고치지 않았다** — 회의 생성은 이제 `axDraftFromAction` 갈래가 먼저 잡아 `ActionMeetingCard`(편집기 `meeting` 갈래)에 닿지 않는다. 남은 갈래는 AX 접두사가 아닌 `meeting` 편집기용 안전망이다(§5-4) |
| 회의 수정·동기화 — 화면 `MeetingEditModal.tsx:119-125,200-212` · `api.ts:1244-1256` | 둘 다 바꿈(§1-2). ⚠ 표의 말처럼 `ActionMeetingCard.tsx:417-427` 은 생성 카드의 장소 칸이라 수정 카드와 무관 — 손대지 않음 |
| AX 수정 카드 편집 계약 — 화면 `MessageList.tsx:295-333`(갈래 더함) · `:641`(`ActionResultCard` — 이 종류는 더는 여기로 안 감) | 갈래 `:318`. `ActionResultCard` 정의는 그대로(다른 종류가 씀) |

**표 밖에서 더 찾은 것**
- `isAxDraftKind` 를 쓰는 `features/work/MyWorkPage.tsx`(내 업무 「AX 제안」 칩) — kind 셋으로 넓히면 회의 생성 초안이 내 업무 칩에 섞인다 → 업무 초안만 보는 `isAxTaskDraftKind` 로 바꿔 지금 동작 유지
- `axDraftFromEnvelope` 를 쓰는 `features/today/TodayPage.tsx`(판단 대기 → `AxDraftModal`) — 이제 회의 생성 봉투도 같은 쪽 나눔 카드로 연다(「어디서 답해도 같은 카드」 원칙 · 코드 변경 없음 — §5-5)
- `editor` 유니온(`viewModels.ts`)에 `meeting_update` 를 더함
- `BookingModal` 의 첫 조회가 예전엔 «시간 없이 전부» 였다 — 정원 조건이 생겨 처음부터 시간·인원으로 묻는다(기존 시험 둘을 새 모양으로 고침)

## 3. 새 시험 (42개) · 고친 시험

| 파일 | 시험 수 | 무엇 |
|---|---|---|
| `features/meetings/RoomSelect.test.tsx`(새) | 12 | **상태 넷**(가용 있음 · 가용 없음 · 조회 실패 503 + [다시 시도] · 기존 방 못 씀 — 비활성+이유·선택 안 옮김·막힘) · 수정 모양(기존 줄·구분선·`meeting_id` · 시간 겹침 이유 · 조회 실패면 「(확인 못 함)」 · 방 없던 회의는 기존 줄 없음) · 300ms 다시 받기 · 고른 방 빠짐 · W-3 · 409 거절 목록 |
| `features/meetings/MeetingEditModal.test.tsx` | +8 | 기존 줄에서 열림·조회 인자 · 다른 방 = `room:{room_id}` + 멱등 키 · 예약 없음 = `{room_id:null}` · 시각만 = 시작·종료만 · H-2(막힘 + [저장] 옆 이유) · 409 ROOM_BOOKING_REFUSED · H-1 · 저장 때 Connect 장애 문구 |
| `features/meetings/MeetingList.test.tsx` | +2 | W-3 — 불러온 방을 쓸 수 있으면 미리 고름 · 못 쓰면 이유 한 줄 + 「예약 없음」 그대로 |
| `features/action/AxMeetingDraftCard.test.tsx`(새) | 9 | 판별(편집기 맞춤 · 내 업무 칩 제외) · 머리(AX·회차·「회의 생성」·쪽 넷·업무 연결 없음) · 쪽 내용 셋 · [등록](초안 없음 / 카드에서 방 바꾸면 초안) · [거절] · [수정] = 생성 모달 → `save_draft`(회의를 만들지 않음 · 안건 출처 유지) · 접힌 한 줄 「회의 열기」 |
| `features/action/ActionMeetingUpdateCard.test.tsx`(새) | 9 | 계약 값으로 채움·장소 글자 칸 없음·회차/수정 없음·기존 줄 · 변경 없음 = 초안 없음 · 바뀐 칸만 + `room` · 예약 없음 + 시각 · 방 없던 회의 · H-2 · 409 ROOM_BOOKING_REFUSED · [거절] · 「회의 열기」 |
| `features/chat/MessageListMeetingCards.test.tsx`(새) | 2 | 채팅 갈래 — 회의 생성 = 쪽 나눔 카드 · 회의 수정 = 수정 카드(결과 카드 아님) |

고친 기존 시험(계약이 바뀐 자리만): `MeetingEditModal.test.tsx`(장소 글자 칸 → 셀렉트 · 저장 patch = 바뀐 값만 · 방 목록 모킹 기본값) · `MeetingList.test.tsx`(「회의실 선택 안 함」 → 「회의실 예약 없음」 + 「가용 없음」 문구 · 첫 조회가 시간·인원을 싣는다 — 둘)

## 4. 검증 — 돌린 시험 파일과 수치

명령: `cd frontend && npx vitest run --no-file-parallelism <아래 파일>` (직렬)

| 시험 파일 | 결과 |
|---|---|
| `features/meetings/RoomSelect.test.tsx` | 12/12 |
| `features/meetings/MeetingEditModal.test.tsx` | 18/18 |
| `features/meetings/MeetingList.test.tsx` | 42/42 |
| `features/meetings/MeetingAfter.test.tsx` | 34/34 |
| `features/meetings/MeetingDetail.test.tsx` | 18/18 |
| `features/meetings/MeetingLive.test.tsx` | 85/85 |
| `features/meetings/MeetingMaterials.test.tsx` | 15/15 |
| `features/meetings/MeetingTitle.test.tsx` | 15/15 |
| `features/meetings/MeetingWorkspace.test.tsx` | 6/6 |
| `features/action/AxMeetingDraftCard.test.tsx` | 9/9 |
| `features/action/ActionMeetingUpdateCard.test.tsx` | 9/9 |
| `features/action/AxDraftCard.test.tsx` | 29/29 |
| `features/action/AxDraftSave.test.tsx` | 17/17 |
| `features/action/ActionMeetingCard.test.tsx` | 7/7 |
| `features/action/ActionTaskCard.test.tsx` | 22/22 |
| `features/action/ActionCenter.test.tsx` | 14/14 |
| `features/action/CommandConfirmationForm.test.tsx` | 8/8 |
| `features/chat/MessageListMeetingCards.test.tsx` | 2/2 |
| `features/chat/ChatDrawer.test.tsx` | 65/65 |
| `features/chat/ChatButtonStates.test.tsx` | 8/8 |
| `features/today/TodayPage.test.tsx` | 3/3 |
| `features/work/MyWorkPage.test.tsx` | 43/43 |
| `features/work/WorkRequestModalFlow.test.tsx` | 11/11 |
| `features/work/WorkTabsAndTables.test.tsx` | 7/7 |
| `features/work/InboxRead.test.tsx` | 6/6 |
| `features/work/WorkRowCompletion.test.tsx` | 6/6 |
| `features/work/CreateWork.test.tsx` | 39/43 — **실패 4 = 기준선(`fe-baseline.md`)의 기존 실패 그대로**(업무 시작일·마감일 4건 — 이 판과 무관) |
| `lib/labels.test.ts` | 10/10 |
| **합계** | **28 파일 · 564 중 560 통과 · 실패 4(전부 기준선)** — 이번 판 실패 0 |

- 빌드 `make frontend-build`(`tsc -b && vite build`) **통과**(청크 500kB 경고만)
- 전체 시험(`make frontend-test` · 프론트 전체 vitest)은 **돌리지 않았다**(코디 지시)

## 5. 미결 · 주의점

1. **WP3-BE 와 같이 나가야 한다** — 화면은 계약 고정 넷을 그대로 쓴다: 목록 인자 `people`·`meeting_id` · 항목 `available·current·unavailable_reason` · 503 · PATCH `room` + 멱등 키 · 409 `ROOM_BOOKING_REFUSED` + `available_rooms` · 저장 때 장애 `room_reservation {status:"failed", reason:"reservation_unavailable"}` · `meeting.info.update` 의 `editor="meeting_update"` 와 `values` 아홉 · `meeting.reservation.create` 의 `save_draft`. 옛 서버면: 목록에 `current` 가 없어 기존 줄이 이름으로만(가용 판정 없이) 서고, 수정 카드는 편집 계약이 없어 지금처럼 결과 카드로 간다
2. **옛 서버 + 새 화면의 PATCH** — 수정 모달이 `location` 을 더는 보내지 않고 `room` 을 보낸다. 옛 서버의 `MeetingInfoPatch` 가 `extra=forbid` 면 방을 바꾸는 저장이 422 다 — BE 와 같은 판에 나가야 한다(WP1 의 005 와 같은 결)
3. **AX 회의 생성 카드의 셋째 쪽은 카드 안에서 방을 고른다** — SPEC §2.4 「회의실 쪽은 셀렉트 그대로 · AX 가 제안한 방이 미리 골라져 있다」 를 그 쪽에서 바로 고르는 것으로 읽었다. 방만 바꾸고 [등록]하면 초안(`draft`)에 그 방을 싣는다(회차는 안 오른다 — 저장이 아니라 확정이므로). 쪽 높이가 고정이라 방이 많으면 그 쪽만 안에서 굴린다
4. **`ActionMeetingCard` 는 남겨 두었다** — 회의 생성은 이제 쪽 나눔 카드가 잡아 이 카드에 닿지 않는다(시험 `MessageListMeetingCards` 가 잠금). 지우지 않은 것은 `meeting` 편집기를 쓰는 다른 종류가 생길 때의 안전망이자, 그 시험 파일(7개)이 여전히 그 부품 자체를 잠그고 있어서다 — 걷어낼지는 2루프에서 정할 일
5. **판단 대기(Today)의 회의 생성 봉투도 쪽 나눔 카드로 연다** — `axDraftFromEnvelope` 가 회의 kind 를 받게 돼 생긴 변화다(원칙: 채팅·판단 대기가 같은 카드). 내 업무의 「AX 제안」 칩에는 넣지 않았다(업무 자리)
6. **AX 수정 카드의 사외 참석자**는 글자 한 칸(쉼표로 구분)이다 — DS 에 사람 이름 목록 입력 부품이 없어 생성 모달의 「사외 참석자로 추가」 흐름을 카드에 옮기지 않았다(2루프 시안 몫)
7. 완료 조건(실물 · 앱 — S-2 · S-3 · S-6 · S-7)은 코디 E2E 몫

## 다른 팀 영향

- BE: §5-1·2 — 계약 고정 넷 + PATCH `room`(그리고 `location` 을 안 보내도 되는지)
- SPEC: 「회의실 셀렉트」 는 지금 화면처럼 **라디오 목록 모양**으로 그렸다(생성 모달의 기존 목록 모양 · DS 안) — 「셀렉트」 를 드롭다운으로 바꿀지는 시안 몫
