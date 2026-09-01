
# [frontend] WP-130 검수 FAIL 정정 — 다중 파일 첨부 유실

너는 **mediness `frontend` 워커**다. 검수 리포트의 FE 몫 FAIL 을 정정한다 — 좁은 라운드.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/frontend/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (**back/·mcp/ 금지 — BE 워커 병렬**)

## SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-code130-report.md` — 위반 ②·WARN 좌표

## 해야 할 일
1. **위반 ② — 다중 파일 첨부 유실**: `front/components/landing-chat/LandingChatClient.tsx` pickFiles 가 N개를 같은 null draft_id 로 동시 업로드해 마지막 1건만 남는다. 정정: **첫 업로드를 await 해 draft_id 를 받고, 나머지는 그 draft_id 로 순차(또는 draft_id 확보 후 병렬)** 업로드. 실패 파일은 칩에 에러 표시. 회귀 테스트 1건(2개 파일 → 둘 다 같은 draft_id 로 업로드됨)
2. **WARN — fallback 규칙 두 벌**: `front/components/tasks/detail/CanonicalTaskDetail.tsx:395` 의 background/goal↔description fallback 이 BE 와 중복 판정이다 — 서버 값 소비 한 벌로 정리(재유도 금지 규율)
3. 참고: 헤더 배지 한 줄 정정은 코디가 이미 반영(TaskDetailShell.tsx) — 건드리지 마라
4. 재검증: tsc·만진 파일 prettier·관련 테스트 — 수치 보고

## 완료 보고 — 문구 변경 금지
> ⚠ 핸들은 dispatch preamble 값을 믿어라.
```bash
orca orchestration send --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "frontend fix 완료: <한 줄>" --body "정정 목록/검증 수치"
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[worker_done] frontend(130 fix) — <한 줄>. 상세는 인박스." --enter
```
