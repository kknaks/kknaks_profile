# [backend] WP-005 소수정 — `MeetingMaterial.can_detach` · `DELETE /shares` 응답 목록

너는 **sc-ax `backend` 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = eda908e). `backend/` 만. reviewer 가 격리본으로 병렬 검수 중 — 커밋 금지.

## 할 것 (FE P5 인계 2건)

1. `MeetingMaterial` 응답에 **`can_detach: bool`**(올린 사람 && 상태 in_progress 아님) 추가 — 권한은 서버가 말한다(FE 가 `uploaded_by === personaId` 로 맞춰 보는 우회 제거). 테스트 1(올린 사람 true · 다른 참석자 false · 진행 중 false).
2. `DELETE /api/meetings/{id}/shares/{member_id}` 응답을 **`GET /shares` 와 같은 목록**으로(지금은 회의 한 줄). 테스트 1.

## 검증

```
cd backend && uv run pytest -q tests/contract/test_meeting_materials.py tests/contract/test_meeting_core.py tests/architecture -m 'not integration'. 검증 1회
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WP-005 소수정(can_detach·shares 응답)" \
  --body "변경 파일 / 검증 수치 / FE 인계"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — WP-005 소수정. 상세는 인박스." --enter
```
