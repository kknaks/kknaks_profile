# [frontend] 참여자 = 같은 회의 웹소켓에 읽기 전용으로 붙어 **모든 업데이트를 실시간 push 로** 받는다 (폴링 제거)

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD a462b6c). `frontend/` 만. 커밋 금지. 서버 재기동 금지(HMR).

## 사용자 결정(2026-09-11) — 앞선 「참여자 폴링」은 코디의 오독. 되돌린다
- 회의 웹소켓 하나에 **주최자(upstream, 마이크) + 참여자들(subscribe, 읽기 전용)** 이 같이 붙는다.
- 참여자는 보내는 것 없이 **회의에서 갱신되는 것 전부를 실시간으로 받는다**: 확정 스크립트(`transcript.final`) · 잠정 발화(`transcript.partial`, 서버가 보내면) · AI 요약(`ai.batch`) · **메모 줄**(새 프레임 `memo.line`, BE 가 붙임 — 올 때까지는 무시) · 종료(1000).
- 화면은 주최자와 같은 두 탭(메모 | AI 요약) + 자료 | 스크립트, 입력 칸·마이크·[회의 종료] 없음.
- a462b6c 의 **LIVE_POLL_MS 폴링 제거**, 참여자도 `useMeetingStream(role="subscribe")` 로. 주최자 두 번째 창(4409)도 subscribe 로 다시 붙음(bef1683 의 폴백 복원).
- **스크립트 세 칸 한 줄(시간 | 화자 | 내용)·촘촘한 간격은 그대로.**

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/ src/App.test.tsx. 테스트: 참여자 = subscribe 소켓 1·audio 없음·입력 없음·transcript.final/ai.batch/memo.line 수신 렌더 · 폴링 타이머 0.
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 참여자 웹소켓 구독(폴링 제거)" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 참여자 구독. 상세는 인박스." --enter
```
