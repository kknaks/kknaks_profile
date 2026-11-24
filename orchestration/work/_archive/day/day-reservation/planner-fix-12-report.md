# planner-fix-12 결과 보고 — SPEC-006 개정 ⑧ (원내 현황 탭 · R46 ~ R53)

## 상태: done (커밋 안 함 · lint --strict 0 error)

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (HEAD `8a0f54e9` 위 미커밋 변경).

## 바뀐 파일

| 파일 | 바뀐 것 |
|---|---|
| `products/day/20-spec/spec-006-reservation-board.md` | 개정 ⑧ 노트 · 결정 원천 R39 ~ R53 · frontmatter sources(조사 리포트 · 기획 §1-5) · 메타 Domain note(08 구매 · 상담 · 직원 · 메뉴 다시 읽음) · Business Req 한 줄 · 1차 범위(넣음 행 · R4/R44 줄 취소선) · RV-32 · RV-40(뺌 → 넣음) · **새 U-8**(탭 · 대상 · 칩 · 정렬 · 빈 목록 · 누르기 없음 · 갱신 · 카드 표) · U-7 제목 · S-6 · 용어 4개 · 칸 표 3줄 · **새 §3 「원내 현황 금액」**(수납 · 미수 ⓐ ⓑ · 결제총액 · VAT · 횟수 · R52 기준값 · R53 매핑) · API 표 한 줄 · 케이스 20줄 · Rule 9 ~ 11 · 기획안과 다른 곳 4줄 · 시안과 다른 곳 7줄 · 다른 스펙과 다른 곳 2줄 · DB · OQ-R03 → R46 |
| `products/day/20-spec.md` | 범위 줄에 원내 현황 탭 요약 · 개정 ① ~ ⑧ · Out 줄의 「원내 현황 탭」 · 「R44 원내 현황 카드」 취소선 · 영역 읽는 순서에 「원내 현황 금액」 |
| `products/day/10-decision.md` | 현재 결론 줄 R39 ~ R53 · R44 일부 취소선 · 개정 ⑧ 요약. 새 ESC 없음 |
| `products/day/log.md` | spec-change 한 줄(개정 ⑧) |
| `products/day/30-work.md` | **바꾸지 않음** — Spec Coverage 행(#267 ~ #269 · proposed)은 그대로 맞다. 원내 현황 탭을 덮을 Delivery 가 아직 없어 넣을 링크가 없다(아래 미결 1) |

## 뒤집힌 문장 정리 (grep `탭 하나만` · `원내 현황` · `다음 피처` · `R44`)

- R33 「탭 하나만 켜진 채」: RV-32 · OQ-R03 닫힌 행(→ R46) · 머리 요약 — 취소선 + 개정 ⑧.
- R44 「원내 현황 = 다음 피처」: 개정 ⑦ 노트 ③ · 1차 범위 다음 피처 줄 · 20-spec.md Out 줄 · 10-decision — 「원내 현황 탭 카드」만 취소선(공지 「수정하기」는 다음 피처 그대로).
- R4 「원내 현황 탭 뺌」: 머리말 범위 밖 목록 · 1차 범위 · RV-40 · 시안과 다른 곳 · 기획안과 다른 곳 우측 사이드 줄 · 20-spec.md.
- 남긴 것: RV-03 헤더 탭 「원내 현황」(링크 없는 글자)은 **헤더 메뉴**라 패널 탭과 다른 것 — 그대로 둠.

## planner 가 읽어 넣은 곳 (결정 문장에 없는 것 — 코디 확인 바람)

1. **R52 기준값 이름** — 결정 파일의 고객 이름은 SPEC 에 옮기지 않고 「고객 A · B · C」로 적었다(브리프 규칙).
2. **접수 카드 국적이 없을 때** — 시안은 「대한민국」을 채우지만 U-5 국가 글자 규칙(값 그대로 · 없으면 글자 없음)을 따라 「{예약 일시}」만 보이게 했다. 시안과 다른 곳 표에 「planner 적용」으로 표시.
3. **「수납 완료」 · 「수납 필요」 배지 동시** — 시안 L1781 대로 둘 중 하나(「수납 필요」가 붙으면 「수납 완료」 없음).
4. **미수 ⓐ 에서 세는 거래 상태** — R53 의 「수납」 셈(승인 · 취소 · SPENT)과 같게 읽음. **「아직 결제 전 수납 건」 · 「같은 상품 옵션」 판정 칸**(구매 상태 값 · `purchase_item.product_option_id`)은 WORK 가 코드로 확인하라고 적음.
5. **탭 · 칩 바꾸기 = 화면 안 · 폴링 뒤에도 유지** · 원내 목록은 날짜 조각 오른쪽 패널에 함께 실림 — 이름 제안 · 구현으로 표시.
6. 구매 회차가 일정보다 늦을 때 배지와 금액이 한 폴링 동안 어긋날 수 있다는 사실 한 줄(오늘 화면 C1 밖 · R41).

## 미결 · 주의

1. **Delivery** — 원내 현황 탭은 #267 ~ #269 범위 밖(새 화면 블록 · 금액 계산 · R53 매핑 = 동기화 변경). 새 Delivery 발행이나 기존 Issue scope_delta 는 코디 몫 — 그 뒤 30-work Spec Coverage 를 갱신한다.
2. **DAY-SPEC-000 와 어긋남** — `purchase_transaction.status` enum 이 SPEC-000 에서는 `approved` · `canceled` 둘. R53 은 `SPENT` · `REQUESTED` · `FAILED` 를 받는다. SPEC-000 본문은 고치지 않았다(다른 SPEC 금지) — 「다른 스펙과 다른 곳」에 사실로 적음. 맞추기는 코디 몫.
3. R53 값 넓힘에 enum 값 추가 migration 이 드는지는 WORK(§4 DB 에 적음).

## lint

`python3 scripts/lint-pipeline.py --strict` → 0 error · 263 warning(다른 제품 기존 · products/day 0).
