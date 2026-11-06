# planner 수정 4판 — SPEC-001 0.2.1 (재검수 WARN)

리포트: `orchestration/work/agency-settlement/review-spec-001-r2-report.md` — W-1 · W-2 를 읽어라.

1. **W-1 ⑤ 「첫 승인 달」 판정 구멍 3개** — 리포트 권장대로 §6.2 를 고친다:
   (a) 전액 취소된 승인(⑤ 의 `canceledRefId` 로 짝지어진 승인 · 취소 쌍)은 「첫 승인」 후보에서 뺀다 → 재결제 달에 품목이 나온다
   (b) 귀속(① `createdTimeUtc`)과 첫 승인 시각(⑤ `approvedDateTimeUtc`)이 자정 경계로 다른 달이 되면 **① 귀속 달을 따른다**(품목이 어느 달에도 안 나오는 길 0). 규칙을 한 줄로: 「품목 줄은 그 수납의 *취소 안 된 첫 승인 결제 행*이 ① 로 귀속된 달에 나온다」
   (c) ⑤ 시각이 없을 때의 대체가 달마다 따로 돌지 않게 — 같은 규칙(① 귀속)으로 통일 · `firstApprovedUnknown` 카운트로 드러냄
   각각 §9.1 시험 하나씩 · WP-LIVE L11 에 (a) 건수
2. **W-2** — SPEC frontmatter `sources` 의 옛 cc-prototype 경로를 새 경로로(파일 실재 확인)
3. 판 0.2.1 · 인덱스 · public grep 다시. 끝나면 §9 두 채널(같은 task/dispatch · subject 「planner 수정 4판 완료」)
