# [backend] 회의 중 AI 배치에 「다음 할 일」 후보(D46) — 스키마·provisional 적재·ai.batch push

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. `backend/` 만. 커밋·재기동 금지. 실물 Codex 호출 금지(대역). **지금 하는 재전사 폴백 폐기(task_51fc8000be06) 완료 보고 뒤에 이어서.**

## 계약 — 그대로
`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/sc-meeting-live-todos-contract.md`

## 할 것
1. `ai_batch_output.json` 에 `todos` 추가(required, strict). 회의 중 배치 프롬프트에 「안건별 후속 업무 후보를 함께 낸다, 담당자 없음」 한 줄.
2. `meeting_todos.provisional` 열(reset_demo 스키마 + `--sync` 가 ALTER 로 붙이게). 배치 적재에서 provisional 전량 교체. 최종 합성 시작 시 provisional 삭제.
3. `Todo` 직렬화에 `provisional`. `push_ai_batch` payload 의 각 agenda 에 `todos`.
4. promote/delete 의 provisional 409 `todo_provisional`.

## 검증
`cd backend && uv run pytest -q tests/contract/test_meeting_batch*.py tests/contract/test_meeting_finalize.py tests/architecture -m 'not integration'`. 테스트로: 배치가 todos 를 내면 provisional 로 적재·다음 배치가 통째 교체·push payload 에 실림 · todos 없는(빈) 배치도 통과 · 최종 합성이 provisional 을 지우고 final todos 만 남김 · provisional promote/delete 409.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 회의 중 다음 할 일(D46)" \
  --body "변경 파일 / 스키마·적재·push / 검증 수치 / sync-demo-schema 필요 여부 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — D46. 상세는 인박스." --enter
```
