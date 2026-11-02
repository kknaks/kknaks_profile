# [frontend] 소수정 — 「정리 중」 동안 상태 다시 묻기 (폴링) · 스크립트 탭 기본 확인

너는 **sc-ax `frontend` 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = 2285277). `frontend/` 만. 커밋 금지.

## 발견 (코디 브라우저 실물 e2e)

- `/end` 뒤 서버는 25초 만에 `done` 이 됐는데 화면은 **150초 넘게 「정리 중」 스켈레톤**에 머물렀다. `MeetingDetailPage` 가 WS 종료(1000) 때 한 번만 `reload()` 하고, `summarizing` 동안 상태를 다시 묻지 않는다(`grep setInterval` → 경과 시계 하나뿐).

## 할 것

1. `status === "summarizing"` 인 동안 **5초마다 상세를 다시 읽고**(`reload()`), `done`/`failed`/`cancelled` 가 되면 멈춘다. 페이지를 떠나면 정리(effect cleanup). 상수 한 곳. 테스트 1(가짜 타이머: summarizing → 두 번째 응답 done → 폴링 멈춤·회의록 렌더).
2. 확인만: 진행 중 오른쪽 탭 기본이 「자료」이고 「스크립트」는 눌러야 보인다 — 시안(E63 「자료」기본)대로면 그대로 두고 리포트에 한 줄.

## 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run src/meetings/. 서버·5176 금지.
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 정리 중 폴링" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 정리 중 폴링. 상세는 인박스." --enter
```
