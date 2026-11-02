# planner 추가 지시 4 (코디 · 2026-10-27) — 예약 카드 이동 단계 = KOS 그대로

원천: `reservation-move-stage-report.md`(데모 실호출) · `_RESUME` §2 10-27 「예약 카드 이동 단계 = KOS 그대로」 · E2E batch 5 #1 · 코드 `domain/reservation_rules.py` `DRAG_MAINS`.
- SPEC-005 §5.4 「드래그할 수 있는 카드 = 예약 · 접수」 → **KOS 가 받은 단계 전부**(예약 · 접수 · 상담 · 시술 · 귀가 · 취소 · 부도 — 시술 대기는 데모에서 못 만들어 미확인 · 앞뒤 단계가 받아 연다) · 바뀌는 필드 = 시각 · 그룹뿐(데모 확인)
- OQ-714 닫음(옮길 수 있는 단계 부분) · DEC-006 줄 · E2E 시나리오 #11 에 「상담 대기 카드 이동」 한 단계 · 0.4.0 변경 표 · 부록 G batch 5 #1 ~ #3 줄(#2 · #3 = frontend 처리 `a7e793c`)
- 보고서 `reservation-spec-r4-report.md` 「추가 지시 4」 절 + 같은 두 명령
