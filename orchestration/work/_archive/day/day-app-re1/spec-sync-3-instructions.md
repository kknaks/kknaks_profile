# [planner] spec-sync-3 — review-doc-5 WARN 7 고침

너는 day `planner` 워커다. 역할 · 규칙 · 검증 · 보고는 `spec-sync-2-instructions.md`(같은 폴더)를 그대로 잇는다(먼저 읽어라 · 구현이 정본 · 새 규칙 금지). 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` — spec-sync-2 의 미커밋 변경 위에 이어서(커밋 · push 금지). 코드 정본 = CENTURION_DAY `a76496c4`(`git show a76496c4:<path>` 로만 · checkout 금지).

읽을 것: `review-doc-5-report.md`(같은 폴더) W1 ~ W7 전부.

## 고칠 것

W1 ~ W7 을 리포트 「고칠 방향」대로 전부(W1 OQ-A90 행 상태 · W2 근거 줄 `day.js:5643-5653` · W3 U-26 `canResend` · W4 SPEC-003 baseBody null→"" · W5 :1624 열린 OQ 요약 줄 · W6 SPEC-007 alpha-2 문장 → OQ-A9 잇기 · W7 503 `photo_disabled` = 사진이 있을 때만 조건). 행마다 처분(고침 파일:줄 / 그대로 + 이유).

## 검증 · 보고

lint `--strict` day 범위 0/0 · 번호 참조 끊김 0. 리포트 `spec-sync-3-report.md`(같은 폴더 · W1 ~ W7 처분표). 완료 = dispatch preamble 의 `worker_done`(`--report-path`) + 직접 주입 `[worker_done] planner 완료: spec-sync-3 — <한 줄>. 상세는 인박스.`
