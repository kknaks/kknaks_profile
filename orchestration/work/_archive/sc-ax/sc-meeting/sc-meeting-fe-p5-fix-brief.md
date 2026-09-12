# [frontend] P5 소수정 — `can_detach` 소비 · 공유 삭제 응답 목록 소비 · 흔들리는 테스트(검수 6 W-2)

너는 **sc-ax `frontend` 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = **cbb4799** BE 소수정 커밋). `frontend/` 만. 커밋 금지.

## 할 것

1. `MeetingMaterial.can_detach`(BE 가 냄) 로 × 노출을 정한다 — `uploaded_by === personaId` 판별과 그 때문에 들어온 `personaId` 프롭을 걷는다(다른 이유로 필요하면 남겨도 된다, 리포트에 적어라).
2. `DELETE /shares/{member_id}` 가 이제 `GET /shares` 와 같은 목록을 돌려준다 — 재조회 우회를 걷고 응답으로 갱신.
3. **검수 6 W-2**: `MeetingLive.test.tsx:101` `socket()` 헬퍼가 `FakeSocket.instances` 를 기다리지 않아 간헐 실패(7회 중 2회). `connect()` 에 `waitFor(() => instances.length > 0)` 한 줄. 같은 결의 헬퍼가 다른 테스트에 있으면 같이.

## 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/ 를 **3회 연속**(흔들림 0 확인). 서버·5176 금지.
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: P5 소수정(can_detach·shares·W-2)" \
  --body "변경 파일 / 검증 수치(3회) / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — P5 소수정. 상세는 인박스." --enter
```
