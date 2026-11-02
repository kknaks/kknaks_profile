# [frontend] 근거 시간 칩 전부 표시 · 「[시간]」 눌리는 칩 모양(D49)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD cee9bca). `frontend/` 만. 커밋 금지. dev 서버·5176 금지. **pytest·vitest 스위트 돌리지 마라(사용자 지시, e2e 로 본다) — `npx tsc --noEmit` 만.**

## 사용자 결정 (2026-09-11, D49 — D34 정정)
1. 줄의 근거 구간(`line.evidence`, 최대 3)을 **전부** 칩으로 낸다. 지금 `finalLinesOf/lineViews` 가 첫 구간 하나만 `at` 으로 내는 것을 배열로. 시작 시각이 같은 구간은 하나로 접는다. 시각 오름차순.
2. 칩은 **눌리는 칩 모양** — 테두리(또는 옅은 배경)+라운드의 chip 부품, 글자는 `mm:ss`(회의 벽시계 규칙 `meetingWallClock` 그대로). 지금의 맨글자 시각 대신. hover 시 배경 짙게. 포커스 링 규칙(전역 없음) 유지.
3. 각 칩 클릭 = 그 구간(`start_ms~end_ms`)으로 스크립트 점프(`setMarked` + 스크립트 탭). 회의 중·끝난 회의 모두(D3 그대로).
4. 부품: `frontend/src` 에 `TimeChip`(또는 기존 chip 류가 있으면 그것) 하나로. AgendaBlock 의 `AgendaLineView.at/onJump` 를 `chips:[{label, onJump}]` 로 넓혀라. Storybook 스토리 한 개.

## 검증
`cd frontend && npx tsc --noEmit` 0. 테스트 파일은 새 모양에 맞게 고치되 **실행은 하지 마라**.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 근거 칩 전부·칩 모양(D49)" \
  --body "변경 파일 / 부품 / tsc / DS 추가 후보 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — D49. 상세는 인박스." --enter
```
