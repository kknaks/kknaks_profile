# [frontend] 회의 승격 드로어 — 제목 「업무 요청」 · 유형 토글 숨김(D10)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD 469c91f). `frontend/` 만. 커밋 금지. dev 서버·5176 금지. **vitest 돌리지 마라 — `npx tsc --noEmit` 만.**

## 사용자 결정 (2026-09-11)
회의 회의록 「다음 할 일」→[업무 생성] 이 여는 `CreateWorkDrawer`(WorkModals.tsx) 가 제목 「새 업무 추가」 + 「업무/요청」 세그먼트 토글로 열리는데, 승격은 언제나 업무 요청(D19·D24)이라 「요청」 하나만 선택된 채 남아 검은 버튼처럼 보인다. 고침:
- 회의에서 열 때(승격 경로): 제목·label **「업무 요청」**, 세그먼트 토글 **렌더하지 않음**, 설명 한 줄(「동료가 수락해야 그 사람의 업무가 됩니다. 희망 기한을 함께 보낼 수 있습니다.」)만, 보내기 버튼 「업무 요청 보내기」 그대로.
- 업무 화면에서 여는 드로어(업무·요청 둘 다 가능할 때)는 지금 그대로. 유형이 하나뿐인 경우(canCreateTask xor canCreateRequest)는 어디서 열든 토글을 숨기고 제목을 그 유형(「업무 추가」/「업무 요청」)으로 — 한 개짜리 토글은 어디서도 안 보이게.
- 구현: `CreateWorkDrawer` 에 프롭 하나(예: `fixedKind: "request"`) 또는 「가능한 유형이 하나면 토글 없음 + 제목 유형별」 규칙 하나. 후자로 되면 프롭 없이.

## 검증
`cd frontend && npx tsc --noEmit` 0. 관련 테스트는 새 모양에 맞게 고치되 실행하지 마라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 승격 드로어 업무 요청(D10)" \
  --body "변경 파일 / 규칙 / tsc / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — D10. 상세는 인박스." --enter
```
