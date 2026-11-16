# [planner] 앱 계약 r2 — SPEC-004 0.4.0 → 0.4.1 · DEC-007 · WORK-009 (리뷰 r1 처분)

너는 **cc-prototype `planner` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc`(공유).

앞 판(같은 문서를 쓴 planner)의 지시 · 보고: `orchestration/work/overall-board/app-spec-instructions.md` · `app-spec-report.md` — allowed_paths 는 거기 목록 + `20-spec/spec-005-reservation-board.md`(W4 낡은 줄만).

**할 일 = `orchestration/work/overall-board/app-spec-r2-instructions.md` 전부.** 버전 0.4.1 · 줄 끝 `(r2)`.

## 금지 · 검증
- 코드 수정 금지 · 실명 · KOS id · 키 · 토큰 금지(public) · 열린 것은 OQ
- 검증: FAIL 6 · WARN 14 · U 6 · Q-154 ~ 157 → 고친 곳 대조표 빠짐 0 · grep 0
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-spec-r2-report.md`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 커밋·push 금지.
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_4bd9bf94-fe21-42f3-8302-4cdd6a891426 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 완료: <한 줄>" --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
