# [reviewer_doc] SPEC-008 마감 검수 (review-doc-5)

너는 day `reviewer_doc` 워커다. 맥락이 없으면 `day-reservation3-review-doc-brief.md`(규칙 · 완료 보고 §9) · `review-doc-4-report.md` 를 먼저 읽어라.

대상: 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec` 커밋 `HEAD`(origin/main 위로 다시 올린 한 커밋 · `git diff origin/main..HEAD`). 읽기만 · 고치지 않는다.

근거: `planner-close-1-instructions.md`(무엇을 반영해야 하나) · `planner-close-1-report.md` · `be-swagger-1-report.md` ③④ · `be-swagger-2-report.md` · `fe-nav-1-report.md` ⑤ · 코드 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3`(dev 머지본 · 읽기만).

## 볼 것

1. **main 쪽 내용이 빠지지 않았나** — `git diff ae8cec61..origin/main -- products/day`(#964 · #969 · #967)에서 생긴 줄이 HEAD 에 다 있나. 개정 번호 충돌(006 ⑭/⑮ · 007 고침 6/7 · 001 ⑭/⑮)이 바르게 갈렸나 · 우리가 「고침 6」「⑭」로 남긴 곳 없나(grep).
2. **SPEC 이 코드와 같은가** — 판정 규칙 · 식별값 필수 · W3 counselor · W18 · cancel 202 · customer_changed · 재시도 accepted_status · 오류 코드 표 · 로그인 뒤 갈 곳 · 셸 메뉴. 코드 실제 분기와 대조.
3. stable 근거 · lint `--strict` products/day ERROR 0.

판정 FAIL / WARN / PASS · 지적마다 파일:줄 · 고칠 방향. 리포트 `review-doc-5-report.md`(이 폴더). 완료 보고 §9 두 명령 · subject `reviewer_doc 완료: SPEC-008 마감 검수`.
