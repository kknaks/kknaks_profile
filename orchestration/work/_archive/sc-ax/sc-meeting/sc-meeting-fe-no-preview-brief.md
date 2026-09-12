# [frontend] D37 — 자료 미리보기(드로어) 데모 제외

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. `frontend/` 만. 커밋 금지.

## 할 것 (사용자 결정 D37, 2026-09-11)
- 자료 행 클릭이 **드로어 미리보기를 열지 않는다**. 대신 `GET …/materials/{mid}/content` 를 **새 탭으로 연다**(a href target=_blank, download 아님 — 브라우저가 PDF/MD 를 알아서 보임).
- `MaterialDrawer.tsx`·관련 테스트·`.material-frame` 스타일 제거. `FileList` 의 `onOpen` 은 새 탭 열기로.
- 자료 첨부·목록·떼기(can_detach)는 그대로.

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/. 서버·5176 금지.
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 자료 미리보기 제외(D37)" \
  --body "변경/삭제 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 미리보기 제외. 상세는 인박스." --enter
```
