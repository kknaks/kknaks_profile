# [frontend] 회의록 목록 — 페이지가 늘어나지 않고 목록 패널 안에서만 스크롤 (항목 1 재발주)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. `frontend/` 만. 커밋 금지.

## 사용자 실물(브라우저 창 약 2000×1130, 회의 19건)
회의가 많으면 **페이지 전체에 스크롤이 생긴다** — 왼쪽 패널이 내용 높이만큼 자라 오른쪽 패널까지 같이 늘어난다. 요구: **페이지는 뷰포트에 고정, 목록은 왼쪽 패널 안에서만 스크롤**(투명 스크롤바 그대로). 오른쪽 패널도 같은 높이로 고정(머리·푸터 고정, 본문 스크롤).

## 원인 후보(네가 P3 후속에서 경고한 것)
`thesc-shell → canvas.full-height → page-surface → meeting-surface → meeting-columns → meeting-panel → meeting-scroll` 기둥 중 어느 칸이 `min-height:0` 이 빠졌거나 `height` 가 auto 라 flex 자식이 내용만큼 자란다. 목록 `ul` 을 감싸는 `.meeting-scroll` 이 `flex:1 1 0; min-height:0; overflow-y:auto` 이고 그 조상 전부가 높이를 뷰포트에서 받아야 한다(`.canvas.full-height` 가 `height:100vh - 상단` 또는 shell 이 `100dvh` grid). 목록 헤더(제목·버튼 줄)는 고정.

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/. 서버·5176 금지 — 실물은 코디(회의 19건 상태로 문서 높이 == 뷰포트 높이인지 잰다).
```
jsdom 으로는 높이를 못 재니 CSS 규칙 검사(각 칸의 min-height:0·overflow 규칙 존재)로 고정.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 목록 패널 내부 스크롤" \
  --body "원인 / 변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 목록 스크롤. 상세는 인박스." --enter
```
