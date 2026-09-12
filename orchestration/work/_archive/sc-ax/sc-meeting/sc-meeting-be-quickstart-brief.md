# [backend] 소수정 — 바로 시작(quick-start) 회의의 웜스타트 · 기본 안건(D32)

너는 **sc-ax `backend` 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = 2285277). `backend/` 만. 커밋 금지.

## 발견 (코디 브라우저 실물 e2e — [회의 시작] 버튼 = `POST /api/meetings/quick-start`)

1. `bootstrap/application.py:740 quick_start_meeting` 이 `launch_warm_start` 를 부르지 않는다(`start_meeting:770` 만 부른다) → `meeting_ai_sessions` 행 없음 → 전사 4블록(950자)·메모가 있어도 **배치가 한 번도 안 돈다**(`meeting_batch_runs` 0).
2. 바로 시작 회의는 안건이 0개라 메모 composer 의 안건 드롭다운이 비어 **메모를 던질 수 없다.**

## 할 것

1. `quick_start_meeting` 도 전이 커밋 뒤 `launch_warm_start(meeting_id)` — `start_meeting` 과 같은 자리. 테스트 1(quick-start 뒤 웜스타트가 제출됨).
2. **D32 (코디 결정)**: 바로 시작 회의는 **기본 안건 하나**(제목 「안건 1」, source manual, order 0)를 함께 만든다 — 메모가 붙을 자리. 합성의 「사람 안건 보존」 규칙 대상이다(AI 가 새 안건을 세우면 그 뒤에 선다). `POST /meetings`(예약)는 그대로(안건은 사람이 준다). 테스트 1(quick-start 응답 agendas 길이 1, 제목 「안건 1」).

## 검증

```
cd backend && uv run pytest -q tests/contract/test_meeting_core.py tests/contract/test_meeting_memo_batch.py tests/architecture -m 'not integration'. 검증 1회
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: quick-start 웜스타트·기본 안건" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — quick-start 소수정. 상세는 인박스." --enter
```
