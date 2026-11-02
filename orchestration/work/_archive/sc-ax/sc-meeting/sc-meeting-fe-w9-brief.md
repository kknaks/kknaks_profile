# [frontend] W9 수정 — `MeetingLine.author` nullable (AI 줄 대비)

너는 **sc-ax `frontend` 워커**다. WP-006 P1~3 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (HEAD 806f52c). `frontend/` 만. `backend/` 는 다른 워커가 작업 중 — 읽기도 HEAD 로.

## 할 것 (검수 3 W9 — `review-code-03-report.md`)

- BE 는 `MeetingLine.author` 를 `member_id | null` 로 낸다(AI 줄·최종 줄은 작성자 없음). FE `viewModels.ts:750` 은 `author: string` 이고 `labels.ts:73` `personName` 이 null 에 `.replace` 를 걸어 TypeError 가 난다. WP-003 이 AI 트랙 줄을 같은 타입에 실으면 화면이 터진다.
- 고칠 것: `author: string | null` · 작성자 표시 자리(스크립트 탭 「메모 · 이름」, 메모 탭, 안건 블록)에서 null 이면 이름 자리를 비운다(시안에 AI 줄은 작성자 표기 없음). `personName` 에 null 이 들어가지 않게 호출부에서 가른다(함수 시그니처는 그대로).
- 테스트 1개: author null 인 줄이 있는 MeetingDetail 이 렌더되고 예외 없음.

## 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/. 검증 1회. 서버·5176 금지.
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: W9 author nullable" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — W9. 상세는 인박스." --enter
```
