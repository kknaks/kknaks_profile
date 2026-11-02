
# [frontend] Task 생성 모달에 참고자료(링크·파일) 섹션 추가

너는 **mediness `frontend` 워커**다. 사용자 확정: 생성 모달에서 태스크의 연관 원장 전부(첨부 포함)가 들어가야 한다.
역할: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/frontend/role.md`
워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (**back/·mcp/ 금지.** ⚠ 다른 FE 워커가 ApprovalCard·TaskDraftBody·wbs 카드 쪽 작업 중 — 그 파일들 금지. 네 범위는 ManualTaskCreateModal 계열만)

## 해야 할 일

1. `front/components/tasks/ManualTaskCreateModal.tsx` 에 **참고자료 섹션** 추가(체크리스트 아래): 링크/파일을 모아 칩 목록으로 들고 있다가 — 기존 TaskReferenceAdder 폼 본체(presentation="inline")·칩 조각 재사용, 두 벌 금지 — **생성 성공 후** `POST /api/ax/tasks/{id}/references` 로 순차 업로드(링크 JSON·파일 multipart, role=reference)
2. **업로드 실패해도 태스크 생성은 유지** — 실패 파일만 사유 안내(채팅 컴포저와 같은 규율). 25MB 선차단·denylist 는 기존 lib 재사용
3. 생성 후 상세로 이동하는 흐름이면 업로드 완료 후 이동(또는 이동 후 반영 — 기존 UX 따라 판단, 뒤집기 가능 표기)
4. 검증: tsc·만진 파일 prettier·회귀 테스트(링크+파일 2건 업로드·실패 시 태스크 생존·25MB 차단) — 전체 스위트 금지

## 완료 보고 — 문구 변경 금지
> ⚠ preamble 핸들 우선. 커밋·push 금지.
```bash
orca orchestration send --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "frontend 모달 첨부 완료: <한 줄>" --body "변경/검증 수치"
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[worker_done] frontend(모달 첨부) — <한 줄>. 상세는 인박스." --enter
```
