# [frontend WP3 수정 1] 코드 검수 FAIL 1 · WARN 반영

규칙 그대로(커밋 금지 · 관련 시험만 · 직렬). 근거 = `W/review-wp3-code-report.md`.

1. **F-1** — 계약 고정 문서 `W/wp3-contract-fixed.md` **§5(갱신)** 대로: AX 수정 카드(`ActionMeetingUpdateCard.tsx` `draftOf`·`meetingUpdateDraft`)가 `proposed_room_id` 를 **미리 골라 두고 「AX 제안」 표지** · 사람이 「기존 — 변경 안 함」 으로 되돌리면 draft 에 명시적 `room: {keep: true}` · 시험
2. **W-6** — `MeetingEditModal.tsx:111` 기존 방 대체 표시: `status==="booked"` 만이 아니라 **`failed` + 방 이름**도 기존 줄로(앞 동기화 실패 + 조회 503 에서도 기존 줄이 선다) · 시험
- W-7(사외 참석자 입력 모양)은 2루프 — 손대지 마라
- 리포트 `W/fe-wp3-fix1-report.md` · 완료 보고 두 명령(subject 「frontend 완료: WP3 수정 1」) · **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
