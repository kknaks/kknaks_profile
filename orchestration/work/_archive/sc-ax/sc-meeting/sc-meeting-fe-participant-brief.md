# [frontend] 회의실 진행 중 — 참여자 폴링 화면(두 탭 읽기 전용) · 스크립트 세 칸 한 줄

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD 504e1d8). `frontend/` 만. 커밋 금지. 서버 재기동 금지(사용자 사용 중, HMR 만).

## 사용자 결정(2026-09-11) — 웹소켓은 주최자 창 하나뿐, 참여자는 폴링
1. **참여자(만든 사람이 아닌 참석자) 의 진행 중 화면**: 주최자와 같은 **「메모 | AI 요약」 두 탭 + 오른쪽 「자료 | 스크립트」 탭**을 그대로 보이되 **읽기 전용**(메모 입력 칸·마이크·[회의 종료] 없음). 웹소켓을 **열지 않고** 3~5초마다(상수 한 곳) 회의 상세(메모·AI 요약 줄)와 `GET /transcript`(확정 스크립트)를 다시 읽어 갱신. 정리 중 폴링과 같은 결. 지금 참여자 화면은 안건 제목만 있는 「AI 회의록」 한 벌 — 이걸 걷는다.
2. **주최자의 두 번째 창**(4409 meeting_stream_active)도 같은 폴링 화면으로 — 방금 넣은 「구독 폴백」(bef1683)은 걷는다. 상태 줄 문구 「다른 창에서 진행 중입니다」는 유지.
3. **스크립트 탭 줄 배치**: 지금 「화자 / 시각」 세로 두 줄 + 본문, 간격 넓음 → **`시간 | 화자 | 내용` 세 칸 한 줄**, 줄 간격은 본문 한 줄 높이 기준으로 촘촘하게. 진행 중·끝난 뒤·참여자 화면 전부. GutterList 를 세 칸으로 넓히거나 새 행 부품(D25 표에).
4. 웹소켓(주최자 창)은 지금 그대로.

## 검증
```
cd frontend && npx tsc --noEmit + npx vitest run src/meetings/ src/App.test.tsx. 테스트: 참여자 진행 중 → WS 0·두 탭·입력 없음·폴링으로 메모/AI/스크립트 갱신 · 스크립트 세 칸.
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 참여자 폴링·스크립트 세 칸" \
  --body "항목 1~4 처리 / 변경 파일 / 검증 수치 / DS 후보 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — 참여자 폴링. 상세는 인박스." --enter
```
