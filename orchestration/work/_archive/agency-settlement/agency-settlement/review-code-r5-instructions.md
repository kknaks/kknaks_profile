# reviewer code r5 — WP-BE6 · WP-FE7 (SPEC-001 0.6.1)

지난 판 브리프 `agency-settlement-review4-brief.md` 의 규칙 그대로(read-only · 운영 PG 5434 · 8800 · 3800 · back/.env 건드리지 마라 · 운영 KOS 0).
대조: SPEC-001 **0.6.1** · WORK 5판 REVIEW5 행 · `r8-decisions.md` · DEC D-24 ~ D-28 · `review-doc-r8-report.md` 「구현 때 지킬 것」 · 앞 판 `review-code-r4-report.md`.
코디 실물: 0005 씨앗 「이번 달 열림 1 · 지난 달 고정 2」 · 9 · 10 · 11월 실결제 합 옮기기 전과 같음 · 확정 달 KOS 0 · 스케줄 꺼짐.
특히: ① 상품 일별 스냅샷 · 달 고정 뒤 키 · 수수료가 바뀌는 길(code r4 F-1 이 다시 열렸나) ② 21시 스케줄 · run_daily(겹침 · 놓친 실행 · `--due`) ③ 수동 연결(못 이은 품목에만 · 기록 · 풀기) ④ 지난 달 설정 열기 PUT 0 ⑤ 화면 b-11 ~ 18 · b-22 ⑥ schemas ↔ types.
리포트 `review-code-r5-report.md`. 원 브리프(review4) §9 두 채널(같은 task/dispatch) · subject 「reviewer code r5 완료」.
