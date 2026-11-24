# [reviewer_doc] 7차 검수 — SPEC-006 개정 ⑧ (원내 현황 탭 · R46 ~ R53)

앞 판 리포트 `review-doc-*-report.md` · `planner-fix-12-report.md` 가 이 폴더에 있다. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` 의 미커밋 변경(`git diff`)을 검수한다.
기준: 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` R46 ~ R53 · 계약 `contract-v2-inhouse.md`(이 폴더) · 시안 `stageCard`/`renderSide`.
특히: ① 금액 정의가 「병원에 그날 실제로 들어오는 돈」(수납 = 거래 − 선불카드 차감 · 미수 = 결제 전 잔액 + 수납 필요 옵션가 + VAT · 결제총액 = 합)과 한 글자도 어긋나지 않는지 ② R52 기준값 세 사례가 규칙으로 재현되는지 손계산 ③ 뒤집힌 R33 · R44 · R4 문장이 남아 있지 않은지 grep ④ planner 가 읽어 넣은 6건(리포트)이 결정과 충돌하는지 ⑤ lint --strict 0 error.
FAIL / WARN / PASS 로. 고치지 마라 · 커밋 금지. 리포트 `review-doc-7-report.md`(이 폴더) · preamble 의 worker_done.
