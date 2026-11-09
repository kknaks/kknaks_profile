# 리뷰 리포트 — day-data-architecture / doc · DAY-SPEC-002 fix4 재검수 (2026-11-06)

대상: mediness 워크트리 `day-data-architecture-spec`(미커밋). S2 = `products/day/20-spec/spec-002-procedure-board.md` · `log.md`. 줄 번호 = 지금 파일.
지시: `planner-spec002-fix4-instructions.md` · 작성 리포트 `planner-spec002-fix4-report.md` · 앞 리포트 `review-spec002-fix3-report.md`(P1 ~ P3).

lint `python3 scripts/lint-pipeline.py --strict` → **0 error** · `products/day/` 경고 0(263 warning 은 다른 제품).

## 판정: PASS — SPEC-002 를 닫을 수 있다

P1 ~ P3 은 닫혔고, 새 모순은 없다. 사용자 결정 OQ 는 0 이다.
열린 것은 이렇다.
- **HAR 요청 6개**(OQ-03 · 08 · 09 · 10 · 12 · 13)
- **기본값 확인 5개**(OQ-14 · 15 · 17 · 18 · 19) — 지금 값이 적혀 있어 구현을 막지 않는다.

## P1 ~ P3 — 닫혔나

| P | 지금 | 판정 |
|---|---|---|
| P1 웹 `kos_failed` | SSE 표 「이벤트」(L472): 웹 = 본문(`data`) **토스트 HTML 조각** · 앱 = `{eventId, visitId, action}` · SSE `id:` 필드 안 씀(재연결 `Last-Event-ID` 와 안 섞임 · 재연결 때 다시 안 보냄). 「웹이 받는 법」(L473): `sse-swap="kos_failed"` · 따로 GET 없음. 규칙 22(L507) 같은 뜻. API 표 L308 「라우트 없음」. `board/toasts` grep 0 | 닫힘 — 고정 URL 문제가 없어졌다. OQ-01(웹 = 화면 라우트 `/board/stream` 이 HTML 을 싣는다)과 맞는다. 「한 번만」 기준(판 조각에 실패 칸 없음)도 그대로 성립한다 |
| P2 「추천」 | U-4(L115): 「추천」 = 「모든 의사」 한 줄(시안 L1064 주석 · 원천 순서) → 그 아래 원장 줄(비어 있는 원장 먼저 · 규칙 19). OQ-20(L571) 닫음 | 닫힘 — 근거가 맞다. 수락 모드(U-6)에는 「모든 의사」가 없다. 시안 template `!acc` 와 같고 U-4 와 부딪히지 않는다 |
| P3 버튼 이름 | 「의사 호출 · N건」: U-3 L104 · U-4 L111 · L118 · S-2 L187(「의사 호출 · 2건」) · KOS 쓰기 표 L445. `개 호출]` grep = L104 「시안 [n개 호출]은 따르지 않는다」 한 곳뿐 | 닫힘(전수) |

## 새 모순 점검

- API 표 · SSE 표 · 규칙 22 · OQ-07 닫은 줄에서 토스트 경로가 모두 같다(SSE 본문 → `sse-swap`).
- 권한: `kos_failed` 는 `/board/stream`(`board` view) 위에 실린다. 판을 보는 사람 누구나 받고, 병원은 세션 병원 하나뿐이다(SSE 표 「병원」). SPEC-001 과 맞다.
- 머리말 개정 ④(L32) · log 줄(L16)이 바뀐 내용과 같다.

## 참고 (판정에 넣지 않음 — 구현 · 문구 몫)

1. 규칙 22 는 「worker 가 … 토스트 HTML 조각을 직접 보낸다」고 쓴다. 그런데 런타임은 worker → Redis pub/sub → api(L466)이고, SSE 연결과 Jinja 조각은 api 쪽에 있다. 그러니 「worker 가 event id 를 알리고, api 의 stream 이 그 `event_log` 로 조각을 그려 싣는다」로 읽고 구현하면 된다. WP 브리프에 한 줄로 넣기를 권한다.
2. 앞 판 참고들은 고치지 않아도 막히지 않는다.
   - 「웹이 받는 법」의 근거 「사용자 OQ-01」(L473)은 OQ-01 에 맞춘 기본값이다.
   - HTMX 는 기본값으로 4xx 응답을 화면에 끼우지 않는다. 오류 토스트를 띄우려면 구현에서 따로 처리해야 한다.
   - 두 번째 재호출의 기본 선택이 시안 코드와 다르다(SPEC 은 결정 문구대로).

## 닫을 때 남는 것

- **HAR 요청**: OQ-03(귀가 뒤 작업 방) · OQ-08([귀가 대기] KOS 요청) · OQ-09(재호출 `call-tasks-doctors` 재전송) · OQ-10(되돌리기 값) · OQ-12(시술 작업 응답 안쪽 키) · OQ-13(상담 응답 안쪽 키). 받으면 「확인됨」으로 바꾸는 개정이다.
- 기본값 확인 OQ-14 · 15 · 17 · 18 · 19 — 지금 값이 정해져 있다.
- 범위 밖으로 넘긴 것: U5 방 옮기기 · 연결, U11 차트 작성, 직원 앱(cc SPEC-004).
