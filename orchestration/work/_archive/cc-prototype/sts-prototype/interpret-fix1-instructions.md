# [frontend] 통역 fix1 — 번역 음성 되먹임 막기(반이중)

배포본에서 폰으로 시험: 번역 음성이 스피커로 나오면 마이크가 그걸 다시 듣고 또 번역한다(`e2e-feedback-batch-3.md` #1). `echoCancellation: true` 는 폰 · Web Audio 재생에선 믿을 수 없다.

- `cc/front/lib/interpret.ts`(+ 모달): **번역 음성 재생 중엔 마이크 PCM 을 보내지 않는다** — `audio_start` 받는 순간부터 **실제 재생이 끝나고 약 400ms 뒤**까지 송신 중지(재생 큐가 비는 시점 기준, 조각이 이어지면 계속 막힘). 그 사이 화면 상태는 「듣는 중」 그대로 두되 마이크 아이콘만 「재생 중」 표시(시안 상태 4종 안에서 — 새 문구는 「재생 중」 하나만)
- [멈춤]/[다시] · 닫기 동작은 그대로. 사용자가 재생 중 [멈춤] 을 누르면 재생도 멈춘다(큐 비우기)
- WS 계약 변경 없음
- `npx tsc --noEmit` · `npm run lint` · `npm run build` 1회 · 목업 WS 로 「audio_start 중 PCM 송신 0바이트 · 재생 끝 +400ms 뒤 재개」 확인
- 리포트 `interpret-fix1-report.md`(이 폴더) · 완료 보고는 WP11 브리프 두 명령(subject 「frontend 완료: 통역 fix1 …」, taskId/dispatchId 는 WP11 것 task_8aa50a4a2768 / ctx_20975f3db451)
- `cc/front/` 만 · 커밋 금지 · 사용자 포트 금지
