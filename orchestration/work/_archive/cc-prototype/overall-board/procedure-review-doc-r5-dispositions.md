# review-doc r5 처분 (코디 · 2026-10-27) — 리뷰 제안 기본값 그대로

| # | 처분 | 누가 |
|---|---|---|
| W1 | 판 = **흰 판(스크롤 컨테이너) 전체** — 가장자리 12px 에 놓아도 판 안 | planner(§5.12 한 줄) · frontend(지금 구현 확인) |
| W2 | `procedure/back/app/service/fake_board.py` **예시 값만** 고쳐도 된다(예외) · **카드 수 5 유지 · 있는 카드 값만** · 검증에 `cd procedure/back && uv run pytest -q` | planner(WORK-008 Meta · WP-FE3) · frontend |
| W3 | WP-E2E · §9 #32 에 「SPEC-005 §9 #42 부상태 색 그대로」 한 줄 | planner · 코디 E2E |
| W4 | 발음 근거 문구만 바로잡음 | planner |
| W5 | #28 = 「오른쪽 칸(호출함 · 칩 · 아이콘 · 버튼)이 한 줄로 남는다 · 시술 이름 줄바꿈은 허용」 | planner · 사용자 E2E |
