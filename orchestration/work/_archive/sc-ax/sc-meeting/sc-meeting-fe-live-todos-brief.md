# [frontend] 회의 중 「AI 요약」 탭에 「다음 할 일」 후보(D46) — 읽기 전용

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD e7e0cfa). `frontend/` 만. 커밋 금지. dev 서버·5176 금지. BE 는 병렬로 만든다 — 계약대로 타입을 세우고 모킹으로 테스트.

## 계약 — 그대로
`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/sc-meeting-live-todos-contract.md`

## 할 것
1. `MeetingTodo` 에 `provisional: boolean`. `ai.batch` 프레임 agenda 에 `todos: MeetingTodo[]`(없으면 빈 배열로 취급).
2. `MeetingDetailPage` 「AI 요약」 탭(in_progress): 안건 블록 `todos` 에 배치의 todos(배치 전엔 상세의 provisional) — 제목 + 기한 후보만, `actions` 없음. 기존 AgendaBlock 의 todos 슬롯을 쓰되 버튼 자리는 비운다. 메모 탭엔 없음. done/failed 렌더는 손대지 마라.
3. 시안 어긋남 없음 — 시안 회의실.dc.html 진행 중 AI 요약 탭의 안건 블록 밑 「다음 할 일」 자리(SCR-106-E40 모양)를 그대로 쓴다. 시안에 그 자리가 없으면 완료 안건 블록의 「다음 할 일」 모양을 버튼 없이 재사용하고 리포트에 적어라.

## 검증
`cd frontend && npx tsc --noEmit` + `npx vitest run src/meetings/`. 테스트로: ai.batch 에 todos 가 오면 AI 탭 안건 밑에 제목·기한이 서고 [업무 생성]·[×] 가 없다 · 다음 배치가 오면 통째 교체 · 늦게 들어온 참여자(배치 전)는 상세의 provisional 로 선다 · 메모 탭엔 없다.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 회의 중 다음 할 일(D46)" \
  --body "변경 파일 / 렌더 자리 / 검증 수치 / 시안 대비 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — D46. 상세는 인박스." --enter
```
