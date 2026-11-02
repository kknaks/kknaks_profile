# [frontend] WP-007 Phase 3 — 회의실 실제 목록 · room_id · 예약 결과 안내 (회의록 페이지 예약 모달·패널)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = d0d5e32 WP-007 BE). `frontend/` 만. 커밋 금지. 범위 = 회의록 페이지(BookingModal · 목록 패널 · 상세 머리의 장소 표시).

## BE 실물(코디 e2e 로 확인)
- `GET /api/meetings/rooms` → `[{room_id:number, name, capacity}]` (실제 THE CONNECT 공용 회의실 7개; 계정 없거나 못 닿으면 **빈 배열**).
- `POST /api/meetings` body 에 **`room_id: number|null`** (지금 보내는 `location` 문자열 대신). null 이면 예약 호출 없음. 응답 `meeting.room_reservation: {status:"booked"|"failed"|"cancelled", room_name, reason}|null` — booked 면 `location` 이 회의실 이름으로 채워져 온다.
- 실패 reason 4종: `room_unavailable`(그 시간 이미 예약) · `reservation_auth_failed` · `reservation_unavailable`(연결 안 됨) · `room_reservation_failed`.
- 회의 취소(삭제) 시 예약도 cancelled 로 동기(BE). 일시 변경 시 update 동기.

## 할 것
1. BookingModal 장소: 정적 `MEETING_ROOMS` 4개 → `GET /api/meetings/rooms` 로 교체(api.ts 함수). 목록 맨 위 「회의실 선택 안 함」(기본, room_id null) 그대로. 빈 배열이면 「회의실 선택 안 함」만. 표시는 `name`(정원 포함돼 옴).
2. 생성 요청에 `room_id` 실음(location 문자열 제거). 응답의 `room_reservation` 이 failed 면 모달을 닫은 뒤 **안내 한 줄**(문구는 labels.ts 임시, reason 별: 「그 시간엔 이미 예약된 회의실입니다 — 회의는 만들었고 장소는 비어 있습니다.」 등 4종, OQ 로 리포트) — 회의는 이미 생성됐으므로 목록 갱신.
3. 패널·상세 머리의 장소 표시는 지금대로(`location`). booked 면 회의실 이름이 그 자리에 선다. failed/cancelled 상태 표시는 두지 않는다(안내 한 줄로 끝).
4. 예약 실패로 [회의 생성] 이 최대 20초 붙잡힐 수 있다 — 버튼 로딩 상태(비활성+「예약 중」)만 두고 재시도 없음.

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/. 서버·5176 금지. rooms/POST 모킹.
```
테스트: rooms 빈 배열 → 선택 안 함만 · room 고르면 room_id 실림 · 선택 안 함이면 null · failed 응답 시 안내 한 줄 + 목록 갱신 · 로딩 상태.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: WP-007 P3 회의실 배선" \
  --body "변경 파일 / 검증 수치 / 임시 문구 4 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — WP-007 P3. 상세는 인박스." --enter
```
