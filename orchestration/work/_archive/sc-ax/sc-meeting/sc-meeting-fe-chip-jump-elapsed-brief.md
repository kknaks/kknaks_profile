# [frontend] 칩 점프 겹침으로 · 시각 표기 회의 경과 mm:ss(D50, D31 철회)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD cf60d06). `frontend/` 만. 커밋 금지. dev 서버·5176 금지. **vitest 돌리지 마라 — `npx tsc --noEmit` 만.** **DS-17·18(task_e6d1b6a19896) 완료 보고 뒤 이어서.**

## 실물 3회차(09-11, 회의 8c63e19b) — 사용자 결정
1. **칩 점프 실패(버그)**: `MeetingDetailPage.inMarked` 가 「줄의 atMs 가 구간 안」만 잡아 구간이 줄 중간에서 시작하면 아무 줄도 안 켜진다(실측 8구간 중 5 실패). **고침**: 겹침 — `row.atMs <= marked.endMs && row.endMs >= marked.startMs`. `ScriptRow` 에 `endMs` 를 싣는다(transcript item 의 endMs, 스트림 final 의 endMs, 잠정 줄은 atMs). 첫 겹친 줄로 스크롤(지금 GutterList 규칙 그대로).
2. **시각 표기 = 회의 경과 mm:ss** (D31 벽시계 철회). 칩 · 스크립트 왼쪽 시각 · 메모 줄 시각 전부 회의 시작 기준 경과. 60분 넘으면 `h:mm:ss`. `meetingWallClock` 을 쓰는 자리를 새 `meetingElapsed(atMs)` 로 교체. 회의 정보 머리의 날짜·시간 범위(09-11 16:50~17:50)는 그대로 벽시계.

## 검증
`cd frontend && npx tsc --noEmit` 0. 테스트 파일은 새 표기에 맞게 고치되 실행하지 마라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 칩 점프 겹침·경과 mm:ss(D50)" \
  --body "변경 파일 / 점프 규칙 / 표기 교체 범위 / tsc / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — D50. 상세는 인박스." --enter
```
