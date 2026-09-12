# 회의 중 안건 추가(메모 칸에서) — task-management 와 같게

## 사용자 결정(2026-09-11, D45): 회의 중에도 주최자가 안건을 넣을 수 있다 — task-management 원형과 같게
- **FE**(`frontend/` 만): 메모 칸의 안건 드롭다운 맨 아래 **「+ 새 안건」** → 제목 한 줄 입력 → 안건 생성(출처 직접 입력) → 드롭다운이 그 안건으로 바뀌고 메모가 거기 붙는다. 주최자 창만. 참여자 창은 새 안건이 오면(스트림 `agenda.added` 또는 상세 재조회) 목록에 선다.
- **BE**(`backend/` 만): `POST /api/meetings/{id}/agendas` 를 **in_progress 에서 만든 사람에게 허용**(지금 409). 편집·삭제는 그대로 막음. 새 안건은 방의 모든 연결에 `agenda.added{agenda}` 프레임으로 broadcast(memo.line 과 같은 결). 배치·합성은 새 안건을 그대로 재료로.
- 원형: `/Users/kknaks/git/toy_pr2/task_management/app/back/`(회의 중 안건 추가 경로) — 읽기만.

## 검증
- FE: tsc + vitest src/meetings/ (새 안건 → 드롭다운 갱신·메모 붙음 · 참여자 창에 agenda.added 반영).
- BE: test_meeting_core.py + test_meeting_stream.py (진행 중 만든 사람 201 · 참여자 409 · 프레임 broadcast).

## 완료 보고 — **문구 변경 금지** (각자)
```bash
orca orchestration send --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from <네 handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "<frontend|backend> 완료: 회의 중 안건 추가" --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 --text "[worker_done] <frontend|backend> 완료 — 회의 중 안건 추가. 상세는 인박스." --enter
```
