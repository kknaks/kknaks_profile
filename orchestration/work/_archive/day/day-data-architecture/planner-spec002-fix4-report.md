# planner-spec002-fix4 결과 보고 — done (미커밋)

- **P1** — 웹 `kos_failed` = SSE 본문(`data`)에 토스트 HTML 조각 · 화면은 `sse-swap="kos_failed"` 로 끼움 · SSE `id:` 필드 안 씀(재연결 `Last-Event-ID` 와 안 섞임 · 재연결 때 다시 안 보냄) · `GET /board/toasts/{event_id}` 삭제(API 표는 「라우트 없음」) · 앱 짝 `{eventId, visitId, action}` 그대로. 고친 곳: 규칙 22 · SSE 표 「이벤트」 · 「웹이 받는 법」 · API 표 실패 토스트 행. `grep board/toasts` 0건.
- **P2** — U-4 의사 호출 창: 「추천」 = 「모든 의사」 한 줄(시안 L1064 주석 · 원천 순서) → 그 아래 원장 줄(비어 있는 원장 먼저 · 규칙 19) · 상태 글자 「대기」 대응은 디자인. OQ-20 닫음.
- **P3** — 판 버튼 = 「의사 호출 · N건」: U-3 · U-4(두 곳) · S-2(「의사 호출 · 2건」) · KOS 쓰기 표 행. 시안 [n개 호출]은 U-3 에 「따르지 않는다」로 한 번만. `grep "개 호출]"` → 그 한 곳뿐.
- 머리말 개정 ④ 한 줄 · `log.md` 한 줄 · lint `--strict` 0 error.
