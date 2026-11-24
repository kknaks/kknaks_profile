# planner-fix-13 결과 보고 — 검수 7 반영 (R54)

## 상태: done (커밋 안 함 · lint --strict 0 error · 263 warning 은 다른 제품)

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec`.

## 고친 것

| 검수 ID | 고친 곳 | 내용 |
|---|---|---|
| F7-2 | §3 「원내 현황 금액」 표 미수 ⓐ · ⓑ 세부 마지막 줄 · Rule 10 · 11 · 케이스 새 행 | ⓐ 의 거래 = 승인 · 취소 · `SPENT`(선불카드 포함) · `REQUESTED` · `FAILED` 는 안 셈(R54). 「WORK 가 확인 · 결정 문장 그대로가 기준」 문장은 취소선 → R54 규칙 |
| F7-1 (+ W7-1) | §3 표 ⓑ · 케이스 매트릭스 2행 바꿈 + 3행 더함 · 요약 5곳(개정 ⑧ 노트 ④ · §4 기획안과 다른 곳 · §4 다른 스펙과 다른 곳 · `20-spec.md` 범위 줄 · §3 ⓑ 세부) | ⓑ 덮임 = **이번 방문의 살아 있는 수납 건(상태 무관)에 같은 상품 옵션** (R54 문장 그대로). 새 케이스: 결제 끝난 건에 옵션이 있는데 플래그가 늦게 꺼짐 → 배지만 · ⓑ 0 / R54 대가(같은 옵션 또 넣음 → 수납 창에 넣기 전까지 미수에 안 잡힘) / ⓐ 의 REQUESTED · FAILED |
| W7-2 | §3 기준값 머리 · Rule 10 | R52 = 실측 당시 행 스냅샷을 fixture 로(지금 DB 로 맞추지 않음 · 고객 C 는 원래 사본에 없음) |
| W7-3 | §4 기획안과 다른 곳 「탭 이름 옆 수」 행 | 근거 ~~R4~~ → R46 |
| W7-4 | U-8 칩 줄 | 계약 값에 칩별 `count` 가 있어도 표시 안 함 |
| W7-5 | §4 DB | `purchase_transaction.status` = PG enum(approved · canceled) → 값 추가 migration 반드시 · `payment_type` 은 이미 7종이라 없음 · 방법은 WORK |
| W7-6 | §3 ⓑ 세부 마지막 줄 | R54 로 「결제 전」 판정이 없어져(상태 무관) 구매 상태 값 판정이 필요 없음 · 「같은 옵션」 = `purchase_item.product_option_id` = `visit_task.product_option_id` 로 적음 |
| — | 개정 ⑧ 보충 노트 · 결정 원천 R39 ~ R54 · 메타 · 10-decision 현재 결론 · log.md 한 줄 | 동기 |

## grep 확인

`아직 수납 건에 없` · `결제 전 수납 건` · `같게 읽음` — 남은 것은 모두 취소선 안(spec-006 L46 · L320 · L329). 살아 있는 문장 0.

## 남은 것

- 「한 폴링 동안 어긋날 수 있다」 문장에 R54 로 금액은 다시 세지 않는다는 한 줄을 보탰다(W7-1 확인 부탁 사항).
- DAY-SPEC-000 거래 status enum 맞추기 · 원내 현황 Delivery 는 여전히 코디 몫(planner-fix-12 미결 그대로).

## 바뀐 파일

`products/day/20-spec/spec-006-reservation-board.md` · `products/day/20-spec.md` · `products/day/10-decision.md` · `products/day/log.md`
