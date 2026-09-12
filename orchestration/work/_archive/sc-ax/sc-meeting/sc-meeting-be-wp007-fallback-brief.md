# [backend] WP-007 후속 — 회의실 자동 대체 · 최종 실패 시 회의 생성 거절 · 시간대별 가능 회의실 조회 (D36)

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = e740f32). `backend/` 만. 커밋 금지.

## 사용자 결정 D36 (2026-09-11) — 앞선 「실패해도 회의는 만든다」를 뒤집는다
1. **자동 대체**: 고른 방이 그 시간에 거절되면(RoomUnavailable) **조건에 맞는 다른 방으로 자동 예약**한다. 후보 기준 = 그 시간 가능한 공용 회의실 중 **정원 ≥ 인원(사내 참석자 + 사외 참석자 + 만든 사람)인 것 중 가장 작은 방**. 대체됐으면 응답에 `room_reservation.replaced: true` + 원래 방 이름(`requested_room_name`) — 화면이 「회의실 N 으로 예약됐습니다」 토스트.
2. **최종 실패 = 회의 생성 실패**: 대체할 방도 없으면(또는 인증·연결 실패) **회의를 만들지 않는다**. `POST /api/meetings` → **409** `{code:"room_unavailable"|"reservation_auth_failed"|"reservation_unavailable", message, available_rooms:[{room_id,name,capacity}]}` — `available_rooms` 는 그 시간대에 가능한 공용 회의실(인증·연결 실패면 빈 배열). 회의 원장에 아무것도 남기지 않는다(예약을 먼저 시도하고 성공한 뒤 회의를 만든다 — 회의 생성이 실패하면 예약을 되돌린다).
3. **시간대별 가능 회의실 조회**: `GET /api/meetings/rooms?starts_at=<ISO>&ends_at=<ISO>` → 그 시간에 가능한 방만 `[{room_id,name,capacity,available:true}]` (참고 코드 `availability`/`plan` 활용, 기존 파라미터 없는 호출은 전체 목록 그대로). 모달이 실패 뒤 이걸로 회의실 목록만 다시 그린다.
4. 「회의실 선택 안 함」·quick-start 는 그대로 호출 없음. 취소·일시 변경 동기화는 그대로.

## 검증
```
cd backend && uv run pytest -q tests/contract/test_meeting_rooms.py tests/contract/test_meeting_core.py tests/architecture -m 'not integration'. 대역. 실물은 코디. 검증 1회
```
테스트: 거절 → 정원 맞는 가장 작은 방으로 대체 + replaced · 후보 없음 → 409 + available_rooms + 회의 미생성 · 인증 실패 → 409 빈 후보 · 예약 성공 뒤 회의 생성 실패 → 예약 되돌림 · rooms?starts_at 필터 · 「선택 안 함」 호출 0.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WP-007 자동 대체·거절·가능 조회" \
  --body "변경 파일 / 계약(409 모양·replaced·rooms 필터) / 검증 수치 / FE 인계 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-007 후속. 상세는 인박스." --enter
```
