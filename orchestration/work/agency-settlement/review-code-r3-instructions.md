# reviewer code r3 — WP-REVIEW3 (BE3 · FE3 · SPEC 0.4.2)

읽을 것: SPEC-001 0.4.2 · WORK 3판 WP-REVIEW3 행 · DEC-001 D-18 · `review-doc-r6-report.md` §3 「구현 때 지킬 것」 1~10 · 보고 `wp-fe3-report.md` · backend 보고의 「판단 · 주의」(1)~(5)(아래).
backend 판단: (1) itemsNowhere 는 실결제 0 · 줄 0 이어도 안 숨김 (2) 반영 판정은 시계 순서 기댐 (3) 묶음 정렬 = 저장 paid_at · 없으면 이 달 첫 취소 시각 — front 정렬과 다를 수 있음 (4) 엑셀 「정보」 시트에 실결제 합 한 줄 (5) schema 1→2.

**코디 실물(운영 · 숫자만)**: 새 back 재시작 뒤 10월 KOS 0 · ⚠ 결제≠품목 0 · 앞의 두 꼴 수납 실결제 = 품목 합 · 숨김 14 · 반영된 취소 3 · refresh=new kosCalls 2 · 9월 closed KOS 0. **9월에 ⚠ 1 수납**(끝 4자리 Ⓐ): 품목 1개 PARTIALLY_REFUNDED 남은 금액 〈금액5〉 · 9월 paymentsNet −〈금액6〉 · 결제 수단 카드. 이 꼴이 SPEC 상 정상(분할 · 앞 달 결제 등)인지 · 버그인지 코드로 판정하라(운영 KOS 호출 금지 · `back/data` 는 읽기만 — 개인정보 리포트 금지 · 숫자만).

리포트 `review-code-r3-report.md` · 판정 PASS/WARN/FAIL · `파일:줄`. 원 브리프 §9 두 채널(같은 task/dispatch) · subject 「reviewer code r3 완료」.
