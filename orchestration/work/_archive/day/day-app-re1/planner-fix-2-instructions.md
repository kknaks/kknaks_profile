# [planner] fix-2 — review-doc-2 표기 N1 · N2

너는 day `planner` 워커다. 역할 · 범위 · allowed_paths · 검증 · 완료 보고는 같은 폴더 `day-app-re1-spec-brief.md` 를 그대로 따른다. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` 의 미커밋 변경 위에 이어서 고친다.

읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/review-doc-2-report.md` §N1 · §N2.

할 것 — 리포트의 고칠 방향대로 **이 두 건만**:
1. N1 — `spec-003-mobile-app.md` A-55 의 「미저장 없으면 iOS 밀기 = 닫힘」에 닫기 표의 조건(밀 수 있는 화면일 때 · 아이패드 창엔 없음)을 맞춘다
2. N2 — `spec-003-mobile-app.md` 의 「카메라 · 앨범」 잔재(리포트가 짚은 두 곳 · 그 밖에 grep 으로 더 있으면 전부)를 OQ-A73 기본값 표시와 맞춘다

그 밖은 고치지 않는다. 개정 번호 새로 따지 않음 · log.md 손대지 않아도 됨. lint(브리프 §8) 후 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/planner-fix-2-report.md`(N1 · N2 → 파일:줄 전 / 후). 커밋 · push 금지.

완료 보고: dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입.
