# [frontend] 2a-1 fix1 에 한 줄 추가 (add1)
- `frontend/src/features/calendar/calendarWrites.ts:225` 근처 주석 「`schedule_release` 를 싣는 표면은 셋뿐」 → 넷(완료·완료 보고 제출의 마감일 채움이 더해짐 — BE Phase 1). 주석만, 동작 변경 없음
- 저장·등록이 붙인 자료 ID(`attachment_draft_ids`)를 **같은 목록으로** 싣는지 확인(서버가 저장 스냅샷에 자료 ID 를 남겨, 등록 때 목록이 같아야 회차가 안 오른다). 다르면 맞추고 테스트 1건
