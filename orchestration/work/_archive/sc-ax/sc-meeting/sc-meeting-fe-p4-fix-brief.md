# [frontend] P4 소수정 — 시각 눈금 벽시계(D31) · 근거 칩 NaN 가드 · 임시 스크립트 정리

너는 **sc-ax `frontend` 워커**다. WP-006 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = 96d5312). `frontend/` 만. backend 워커 병렬 — 커밋 금지.

## 할 것

1. **D31 (코디 결정, 시안 정본)**: 근거 칩과 스크립트 탭 줄의 시각 눈금은 **벽시계 HH:MM** 이다(시안 `근거 [15:32] [15:34]`, 스크립트 줄 시각). 값 = `meeting.started_at + at_ms`(진행 중·완료 모두). `started_at` 이 없으면(예정) 눈금을 비운다. 진행 표시 띠의 **경과 시간**은 그대로 경과다. 칩→줄 점프는 at_ms 로 맞추므로 눈금과 무관.
2. **근거 칩 NaN 가드**: BE 가 evidence 키를 `start_ms/end_ms` 로 고친다(계약대로). FE 는 계약 키만 읽되, 값이 숫자가 아니면 칩을 그리지 않는다(NaN:NaN 금지). 테스트 1.
3. `frontend/shot_*.mjs`(코디 스크린샷 스크립트, untracked)는 손대지 말고 무시.

## 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/. 검증 1회. 서버·5176 금지.
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: P4 소수정(벽시계·NaN 가드)" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — P4 소수정. 상세는 인박스." --enter
```
