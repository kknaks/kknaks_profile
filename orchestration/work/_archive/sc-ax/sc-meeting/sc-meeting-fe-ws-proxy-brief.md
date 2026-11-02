# [frontend] 소수정 — vite 프록시 WebSocket 통과(`ws: true`) · ready 전 닫힘을 「끊김」으로 표시

너는 **sc-ax `frontend` 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = 16d249c). `frontend/` 만. 커밋 금지.

## 발견 (코디 브라우저 실물 e2e, playwright 가짜 마이크)

- `make local-stack`(vite 5176 → API 8001) 에서 진행 중 화면이 **「연결하는 중」에서 멈춘다.** 서버 로그에 `WebSocket /api/meetings/{id}/stream` 접속 기록이 **0건** — `vite.config.ts` 의 `proxy: { "/api": "<target>" }` 문자열형은 HTTP 만 넘기고 **WS 업그레이드를 넘기지 않는다.**
- 그 상태에서 화면이 「연결하는 중」을 유지한다 — 소켓이 `ready` 전에 닫히면(1006 등) 끊김으로 드러나야 한다(브리프 P3 「끊기면 그대로 드러낸다」).

## 할 것

1. `vite.config.ts` 프록시를 객체형으로: `"/api": { target: environment.VITE_API_TARGET ?? "http://127.0.0.1:8000", ws: true }` (changeOrigin 은 필요할 때만). 다른 설정 불변.
2. `stream.ts`: `ready` 를 받기 전에 `close` 가 오면(코드 4401/4404/4409/1000 이 아닌 모든 닫힘 포함) 상태를 **끊김**(`streamDisconnected`, 사유는 close code) 으로 세운다. 테스트 1(ready 전 1006 닫힘 → 끊김 표시, 재연결 없음).

## 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/. 서버·5176 금지 — 실물은 코디가 붙인다.
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: vite WS 프록시·ready 전 닫힘" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — WS 프록시 소수정. 상세는 인박스." --enter
```
