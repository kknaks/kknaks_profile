# [backend] 회의실 v3 — 자료 떼기 「예정」에서만(A4) · 미커밋 내보내기 분 유지

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD b61ba47 + **네가 방금 만든 내보내기 이식분이 미커밋으로 있다 — 건드리지 말고 그 위에 쌓아라**). `backend/` 만. 커밋 금지.

## 할 것
1. **A4(D34)**: `MeetingMaterial.can_detach` = 올린 사람 && **status == scheduled**(예정에서만). `DELETE …/materials/{mid}` 게이트도 같은 규칙(그 밖 409). 테스트 갱신(진행 중·종료 false·409).
2. **C3**: 변경 없음 — `GET /transcript` 의 `memos` 는 그대로 두고(다른 소비자 가능) FE 가 무시한다. 확인만.
3. 상태 어휘는 서버 enum 여섯 그대로(D34 서버 유지).

## 검증
```
cd backend && uv run pytest -q tests/contract/test_meeting_materials.py tests/contract/test_meeting_finalize.py tests/architecture -m 'not integration'. 검증 1회
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 회의실 v3(자료 떼기 예정만)" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — 회의실 v3. 상세는 인박스." --enter
```
