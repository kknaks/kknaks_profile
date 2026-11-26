# [reviewer_doc] review-doc-5 — spec-sync-2 검수(SPEC ↔ 머지된 구현)

너는 day `reviewer_doc` 워커다. 역할 · allowed_paths(read-only · 리포트 1개) · 검증 · 완료 보고는 같은 폴더 `day-app-re1-review-doc-brief.md` 를 따른다(먼저 읽어라). 대상 = 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` 의 **미커밋 변경**(`git diff HEAD` · HEAD `538befe4`) 중 `products/day/`.

정본 = 머지된 코드 CENTURION_DAY `origin/dev` `a76496c4`(코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` — `git show a76496c4:<path>` 로만 읽어라 · checkout 금지 · 다른 워커가 브랜치를 쓰는 중).

읽을 것(`/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/`): `spec-sync-2-instructions.md` · `spec-sync-2-report.md` · `be-2-report.md` §0 · `be-fix-2-report.md` · `app-fix-2-report.md` · `merge-dev-2-report.md` §4 · `_RESUME.md` §2.

## 볼 것

1. 처분표 항목 1 ~ 8 이 SPEC 에 들어갔나(파일:줄) — 특히 D1 ~ D17 이름 · 코드 · 응답 칸이 **코드와 글자까지 같은지**(코드 파일:줄 대조)
2. 구현이 정본이라며 바꾼 문장이 실제 코드와 맞나(표본 아닌 전수 — 바꾼 hunk 마다)
3. 새로 지은 규칙 · 글자가 없나(발명이면 FAIL) · main 쪽(#965 · #966 · #967) 문장을 건드리지 않았나
4. 닫은 OQ(119 · 120 · A83 · N25 · D29 · D30 · D31 · D39 · D42 · D06 등)가 근거(사용자 결정 · 구현)와 함께 닫혔나 · 사용자 확인 3가지(BW6 · 국적 alpha-2 · OQ-A95/A93)는 열린 채인가
5. 번호 참조 끊김 0 · lint `--strict` day 범위

리포트 `review-doc-5-report.md`(같은 폴더) — PASS / WARN / FAIL · 지적마다 파일:줄 + 근거 + 고칠 방향. 완료 = dispatch preamble 의 `worker_done`(`--report-path`) + 직접 주입 `[worker_done] reviewer_doc 완료: review-doc-5 — <판정>. 상세는 인박스.`
