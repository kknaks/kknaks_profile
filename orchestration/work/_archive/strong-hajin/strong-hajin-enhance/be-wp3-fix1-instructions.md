# [backend WP3 수정 1] 코드 검수 FAIL 1 · WARN 반영

규칙 그대로(커밋 금지 · 관련 시험만). 근거 = `W/review-wp3-code-report.md`.

1. **F-1** — 계약 고정 문서 `W/wp3-contract-fixed.md` **§5(갱신)** 대로: values 에 `proposed_room_id`·`proposed_room_name` · draft 의 사람 선택이 제안을 이긴다 · draft 에 `room` 이 없으면 방을 바꾸지 않는다(`actions.py:2175-2176` · `confirmation.py:206-220`) · 시험(제안 있음 + 기존 유지 → 안 바뀜 / 제안 그대로 → 이동 / room 없음 → 안 바뀜)
2. **W-1** — `needs_verification`(확인 대기) 예약을 「자리 없음」 으로 보지 않는다 — 쥔 자리로 다루거나, 확인 대기 중이면 방 관련 수정을 거절(어느 쪽이든 이중 예약·이동 누락이 없게) · 시험
3. **W-2** — AX 확정·옛 `meeting.update` 에서 Connect 호출을 **액션 트랜잭션 밖으로**(계획은 밖에서, 반영은 짧게)
4. **W-3(코디 판정 — OQ-1002 ② 고침)** — AI 맥락 목록은 **세션의 첫 턴과 새 세션을 열 때만** 싣는다. 이어 쓰는 턴에는 싣지 않는다(세션이 이미 갖고 있다 — 매 턴 실으면 세션 기록에 쌓인다). 시험
5. **W-5** — Connect PUT(방 이동·시간 변경) **직전에 `available(ignoring=자기 예약)` 한 번** 확인 · 차면 409 `ROOM_BOOKING_REFUSED`
- 리포트 `W/be-wp3-fix1-report.md` · 완료 보고 두 명령(subject 「backend 완료: WP3 수정 1」) · **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
