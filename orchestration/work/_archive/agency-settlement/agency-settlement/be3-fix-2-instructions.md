# backend 3판 수정 2 — 부분 취소 뒤 다른 금액 재승인 (코디 결정)

네가 올린 미결: 「itemsHere false 수납에 이 달 취소가 있으면 이 달 승인도 더한다」를 **채택**한다(settle() 한 줄). 근거: 원칙 = 「달을 모두 더하면 KOS 최종 금액」. 분할 결제 나머지(취소 없음)는 지금대로 더하지 않는다.
- 운영 9 · 10월 실물에서 이 갈래(itemsElsewhere)는 0 건이다 — 드문 꼴. 그래서 이 갈래를 탄 수납 수를 로그 숫자 하나로(이름 · 금액 · id 금지) 남겨라
- 시험: 9월 500,000 · 10월 −200,000 + 100,000 → 두 달 합 400,000 · 분할 결제(취소 없음) 꼴은 그대로 · 엑셀 · 에이전시 합 같음
- 못박아 둔 test_r3_f1_partial_cancel_then_reapprove_is_not_pinned 은 새 규칙으로 고친다
- 8800 · back/data 금지 · `uv run ruff check . && uv run pytest -q` · WP-BE3 §9 두 채널 · subject 「backend 3판 수정 2 완료」
