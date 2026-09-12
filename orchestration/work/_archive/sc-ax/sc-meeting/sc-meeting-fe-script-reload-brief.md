# [frontend] 종료 뒤 스크립트 원문 재조회 · 회의 중 시간 칩 점프

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD b440c6b). `frontend/` 만. 커밋 금지. dev 서버·5176 금지.

## 왜 (실물 1회차, 회의 d6e7b8e0 — 참여자 지호 창)
1. 스크립트 탭이 2줄만 남았다(서버는 64블록). `MeetingDetailPage` 가 원문(`readMeetingTranscript`)을 **페이지 열 때 한 번만** 읽고(`wantsTranscript` 는 상태가 in_progress→summarizing→done 으로 바뀌어도 그대로), 종료되면 `live=false` 라 `stream.finals` 가 빠져 처음 읽은 2줄만 남는다. 새로고침하면 64.
2. 회의록 줄의 시간 칩 점프(`onJump`)가 `settled`(끝난 회의)에서만 켜져서 **회의 중 AI 요약 탭 줄은 시각만 찍고 못 누른다.**

## 사용자 결정 (2026-09-11)
- **D2 종료 뒤 원문 재조회**: 회의 상태가 바뀔 때마다(특히 `in_progress→summarizing`, `summarizing→done|failed`) 원문을 다시 읽는다. 종료 시 BE 가 재전사로 원문을 **통째로 갈아 끼우므로**(화자·시각·줄 수 전부 바뀜) done 진입 때 재조회는 필수 — 스트림으로 쌓인 `finals` 를 done 에서 섞지 않는다(서버 원문만). 스트림 close(1000)·summarizing 폴링이 done 을 보는 순간이 트리거.
- **D3 회의 중 칩 점프**: 회의 중 AI 요약 탭의 줄도 시간 칩을 누르면 스크립트 탭으로 가서 그 구간(`marked`)이 표시된다. 진행 중 스크립트는 스트림 finals + 선로드분이므로 그 안에서 표시. `noteEditing` 제외 규칙은 그대로.

## 검증
`cd frontend && npx tsc --noEmit` + `npx vitest run src/meetings/`. 테스트로: 참여자 창이 in_progress 에서 열려 2블록 선로드 → done 전이 → 원문 재조회돼 서버분(64)만 선다 · 회의 중 AI 탭 줄의 칩 클릭 → 스크립트 탭 + 해당 구간 active.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 스크립트 재조회·회의 중 칩 점프" \
  --body "변경 파일 / 재조회 트리거 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 스크립트 재조회·칩 점프. 상세는 인박스." --enter
```
