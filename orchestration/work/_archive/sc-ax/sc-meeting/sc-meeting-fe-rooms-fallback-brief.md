# [frontend] WP-007 후속 — 대체 예약 토스트 · 생성 실패 토스트 + 회의실 목록만 재렌더 (D36)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = e740f32). `frontend/` 만(회의록 페이지 예약 모달). 커밋 금지. **BE 가 같은 트리에서 병렬로 계약을 만든다 — 아래 모양대로 모킹해 만들고 실물은 코디가 붙인다.**

## 계약(코디 확정, BE 구현 중)
- `POST /api/meetings` 성공 201: `meeting.room_reservation: {status:"booked", room_name, replaced: boolean, requested_room_name?: string}`. **replaced 면 토스트 「{room_name}(으)로 예약됐습니다」** (고른 방이 안 돼 대체됐다는 뜻, 문구는 labels.ts 임시).
- **409** `{detail:{code:"room_unavailable"|"reservation_auth_failed"|"reservation_unavailable", message, available_rooms:[{room_id,name,capacity}]}}` = **회의가 만들어지지 않았다.** 토스트 「회의실이 이미 예약되어 있습니다」(code 별 3문구) 뒤 **모달은 닫지 않고**, 입력값(회의명·일시·목적·안건·참석자)은 전부 유지한 채 **회의실 목록만** `available_rooms` 로 다시 그린다(맨 위 「회의실 선택 안 함」은 그대로, 선택은 해제). 빈 배열이면 「선택 안 함」만.
- `GET /api/meetings/rooms?starts_at&ends_at` → 그 시간대 가능 방만. 모달에서 **일시를 바꾸면** 이걸로 목록을 다시 받는다(디바운스 300ms). 처음 열 때는 파라미터 없이(전체).
- 「예약 중」 버튼 상태는 그대로.

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/. 서버·5176 금지.
```
테스트: replaced 토스트 · 409 → 토스트 + 모달 유지 + 입력값 유지 + 회의실만 재렌더 · 일시 변경 → rooms 재조회 파라미터.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 회의실 대체·거절 처리" \
  --body "변경 파일 / 검증 수치 / 임시 문구 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 회의실 대체·거절. 상세는 인박스." --enter
```
