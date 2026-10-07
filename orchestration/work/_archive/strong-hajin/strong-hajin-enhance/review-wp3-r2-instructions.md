# [reviewer 재검수] WP3 수정 1 — 고친 자리만

규칙 그대로(읽기 전용 · 실행 금지 · 리포트 한 장). 대상 = `W/be-wp3-fix1-report.md` · `W/fe-wp3-fix1-report.md` 가 적은 변경(WP2 커밋 `e58fb25` 뒤 미커밋 diff 중 수정분). 계약 = `W/wp3-contract-fixed.md` §1~5.

- 네 리포트 `review-wp3-code-report.md` 의 F-1 · W-1 · W-2 · W-3 · W-5 · W-6 이 각각 고쳐졌나(PASS/FAIL · 파일:줄) · BE↔FE 가 §5(제안 방 · `room:{keep:true}` · room 없음=안 바꿈)에서 맞물리나
- 코디 판정(판정 대상 아님): **W-5 PUT 직전 찬 경우 = 200 + `room_reservation.failed`**(409 아님 — 반영이 커밋 뒤라서. 409 는 커밋 앞 재확인이 낸다) · W-3 = 맥락 목록은 새 provider 세션 턴에만 · W-7 은 2루프
- **새로 생긴 위험**: W-2 의 「되돌림 → 밖 재확인 → 짧은 재실행」 에서 두 번 실행·부분 적용 · 새 오류 `409 ROOM_RESERVATION_UNCONFIRMED` 가 FE 에서 어떻게 보이나(FE 는 409 + available_rooms 만 거절로 본다 — 이 코드는 available_rooms 가 있나)
- 리포트 `W/review-wp3-r2-report.md` · 완료 보고 두 명령(subject 「reviewer 완료: WP3 재검수 <판정>」) · **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
