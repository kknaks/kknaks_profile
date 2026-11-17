# [reviewer_doc] review-doc-2 — spec-2 재검수 (read-only)

너는 앞 맥락이 없다. 먼저 읽어라:
1. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-review-doc-brief.md` — 역할 · 결정 표 원천 · read-only · 검증 그대로.
2. 앞 검수 `…/fix-feedback/review-doc-1-report.md` (W1 ~ W12 · §6 착수 막는 OQ 표)
3. 지시 `…/fix-feedback/spec-2-instructions.md` (코디 기본값 표) · 결과 `…/fix-feedback/spec-2-report.md`

리뷰 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec` 미커밋 diff(spec-2 가 더한 부분).

## 볼 것 — 짧게
1. spec-2-instructions 의 기본값 표 18건이 스펙 본문 규칙 · 계약 · OQ 행에 빠짐 없이, 지시와 같은 값으로 들어갔나(파일:줄).
2. W3 · W6 · W10 · W11 · W12 가 고쳐졌나. W9 는 그대로여야 한다.
3. 새로 생긴 모순 · 넘침(화면 문구 발명) 0 인가. 정렬 쿼리 `sort=room` 이 코드 사실(`board_page` 의 `view` 인자)과 부딪히지 않나.
4. be · fe 가 이 스펙만으로 지을 수 있나 — 아직 착수 막는 것이 남았으면 표로.
5. `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-doc-2-report.md` — 판정 PASS/WARN/FAIL · 지적 파일:줄. 완료 보고는 preamble 의 worker_done.
