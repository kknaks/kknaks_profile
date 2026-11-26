# [reviewer_doc] review-doc-4 — planner-fix-3 재검수

너는 day `reviewer_doc` 워커다. 역할 · allowed_paths(read-only · 리포트 1개) · 검증 · 완료 보고는 같은 폴더 `day-app-re1-review-doc-brief.md` 를 따른다(먼저 읽어라). 대상 = 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` 커밋 **`22f7c30f..HEAD`** 의 `products/day/` 변경.

읽을 것(`/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/`): `review-doc-3-report.md`(W1 ~ W13 · U1 ~ U5) · `planner-fix-3-instructions.md` · `planner-fix-3-report.md` · `_RESUME.md` §2 review-doc-3 U1 · U2 ~ U4 행.

## 볼 것

1. W1 ~ W13 이 각각 닫혔나(파일:줄)
2. U1 ~ U4 가 결정 글자대로 들어갔나. **U1 을 [시술 대기] 신분확인 칸(D21)에도 같게 적은 것**이 결정 범위 안인지(결정은 [상담 대기]만 말함 — 같은 칸 하나를 두 버튼이 보는 구조면 범위 안 · 따로 보는 칸이면 범위 밖) 사실로 판정
3. 새로 생긴 문제(발명 · 모순 · 잔재) — 새 경로 `GET /api/reservations/visits/{id}/passport` 권한 · W3 `sending` 읽을 때 실패 규칙 · W4 IP 규칙 근거
4. U5(OQ-A79)는 열린 채인지(글자를 지었으면 FAIL)
5. lint day 범위

리포트 `review-doc-4-report.md`(같은 폴더) — PASS / WARN / FAIL · 지적마다 파일:줄 + 근거 + 고칠 방향. 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입.
