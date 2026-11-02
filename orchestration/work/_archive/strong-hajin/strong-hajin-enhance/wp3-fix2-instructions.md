# [backend · frontend WP3 수정 2] 재검수 FAIL 1 · WARN 4

규칙 그대로(커밋 금지 · 관련 시험만). 근거 = `W/review-wp3-r2-report.md` · 계약 = `W/wp3-contract-fixed.md` **§6 · §7(갱신 2)**.

**backend**
- F-r2-1: 편집 계약 values 에 `room_proposed: bool` — AX 가 회의실을 바꾸자고 했을 때만 true(「예약 없음」 제안도 true) · 시험(시간만 바꾸는 제안 → false)
- W-r2-2: 결과 모르는 **취소**에서 Connect 가 「없음」 을 돌려주면 자리를 비운 것으로 확정(없는 예약에 PUT 되풀이 금지) · 시험
- W-r2-3: 실행 직전 예약 상태를 계획 때와 대조(달라졌으면 다시 계획 또는 거절) · 경미 — 시험 1
- 리포트 `W/be-wp3-fix2-report.md`

**frontend**
- F-r2-1: `room_proposed` 가 true 일 때만 제안 방을 미리 고르고 표지 · false 면 기존 방 그대로 · 시험(방 있는 회의 + 시간만 제안 → 그대로 등록해도 room 없음)
- W-r2-1: `409 ROOM_RESERVATION_UNCONFIRMED` 문구(§7) — 코드별 문구, 모르는 코드는 `detail.message` · 시험
- W-r2-4: 수정 모달 기존 줄 대체 표시에 `needs_verification` + 방 이름도 포함 · 시험
- 리포트 `W/fe-wp3-fix2-report.md`

완료 보고 두 명령(subject 「<역할> 완료: WP3 수정 2」) · **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
