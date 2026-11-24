# fe-feat-3 결과 보고 — 공지 「수정하기」 제자리 편집(R58 · R61 · R62 · 계약 v3 + 보충 1)

## 상태: done (실물 확인은 코디 재기동 뒤 · 스택 안 건드림 · 커밋 안 함)

## 수행
- `templates/partials/reservations_parts.html`
  - `notice_panel(date, weekday, notice)` 매크로 = `<section id="reservation-notice">`. 보기 모델 v3(`notice{id, content, editable, date}`) — 예전 `notice.items[]` 는 안 씀.
  - 날짜 머리 오른쪽 파란 글자 「수정하기」(editable 만 · 시안 `.btn-xs-text` L898 모양). 지난 날(editable false) = 버튼 · 폼 없음(R61).
  - 숨은 편집 폼: `ui.write_attrs("/reservations/notice", method="put", target="#reservation-notice", swap="outerHTML", disabled="find button")` + `hx-push-url="false"`. 칸: `date` · **`notice_id`(보충 1 · 없으면 빈 값)** · `content`(textarea · 지금 글). 글자 수 「n / 2,000」(앞뒤 공백 자른 길이 · R62 ④) · [취소](filled-gray s) · [저장](primary s · 시안 L2142) · 실패 줄 「저장하지 못했습니다」 + 「다시 시도」(숨김).
  - 패널에 성공 알림 틀 `<template data-day-res-notice-toast>`(ui.toast).
- `templates/partials/reservations_notice.html`(새) — backend `NOTICE_TEMPLATE` 이 그리는 저장 응답 조각 = 같은 매크로.
- `styles/app.css` → `static/day.css` — `.day-res-notice__head/edit/form/input/foot/count(.is-over 빨강)/error/retry` · 편집 중(`.is-editing`) 수정하기 · 글 숨김.
- `static/day.js`
  - 열기 = 폼 보임 · 포커스(글 끝) · 글자 수 · 취소 = 그린 글로 되돌리고 닫음(버림). 입력마다 글자 수 · 2,000 넘으면 빨강 · [저장] 막음 · 다른 길로 보내도 beforeRequest 가 막음.
  - 실패 판정 = 상태 0 · 4xx · 5xx · 연결/시간 초과 → 칸에 아무것도 끼우지 않고(X-Day-Error 공통 끼우기보다 뒤에서 막음) 글 · 편집 그대로 + 실패 줄. 다시 시도 = 같은 폼 다시 보냄.
  - 성공 = 응답 칸이 바뀌어 끼워짐 + `day:notice-saved`(HX-Trigger) 의 `message` 를 알림 틀에 넣어 #day-toasts(글자는 서버 값 — JS 에 한글 없음).
  - **편집 중 10초 폴링**: `resBeforeSwap` 에서 폴링 요청이면 편집 중 칸(노드 · 커서 · 떠 있는 저장 요청)을 잡아 두고, `resInit` 이 새 조각의 칸 자리에 되돌려 놓고 `htmx.process` 로 폼 연결을 다시. 표 · 나머지는 새로. 시계 · 요청 추가 없음.
  - **날짜 이동**(꺾쇠 · 오늘 · 달력 = `resPick`) = 편집 닫고 버림 → 새 날짜 칸.
  - htmx 리스너는 이름 있는 함수로(시험 추출기가 마지막 인라인 리스너를 잡는 규약 — 차트 시험과 겹치지 않게).
- 문구(`test_screen_copy.py`) — 결정 R58 문장만: 수정하기 · 저장 · 저장하지 못했습니다(취소 · 다시 시도 · 공지는 이미 표에 있음). 「공지를 저장했어요」는 서버 문구(JS · 템플릿에 없음).

## 시험
- `scripts/frontend/tests/res-notice.test.mjs`(새 · 7개 · 진짜 htmx · day.js + 서버 렌더 고정본 · 계약 모양 응답):
  1. 수정하기 → 지금 글 · 포커스 · 「8 / 2,000」 · 공백 자른 길이 · 취소 = 버림
  2. 저장 성공 — PUT `/reservations/notice`(date · notice_id · content) → 칸 교체 + 「공지를 저장했어요」 · 주소 줄 그대로
  3. 저장 실패(503 kos_unavailable · 보충 2 · X-Day-Error · HX-Reswap none) → 글 · 편집 그대로 + 실패 줄 · 다시 시도 → 같은 글 다시 → 성공
  4. 400(X-Day-Error · 본문 있음)도 칸을 덮지 않고 실패 줄
  5. 편집 중 폴링 2회 — 조각은 바뀌어도 칸 · 쓴 글 · 포커스 · 선택 범위 그대로 · 그 뒤 저장 동작 · 저장 뒤 폴링은 칸도 새로
  6. 2,000 초과 — 「2,001 / 2,000」 빨강 · 저장 막음 · 보내지 않음 · 앞뒤 공백은 안 셈
  7. 날짜 이동 = 바로 닫고 버림 · 새 날짜 칸(date 칸 = 새 날짜)
- `res-dom.mjs` — 가짜 서버에 `server(entry)`(상태 · 본문 · 머리) · method · form 기록 · `navs()` = GET 만 · jsdom `requestSubmit` 대역.
- `res-debounce.test.mjs` — 가짜 전역에 공지 함수 3개(resPick 이 부름).
- `backend/tests/day/web/test_reservations_screen.py` — 보기 모델 v3(+id) · 새 시험 2개(폼 속성 · 숨은 칸 · 글자 수 · 문구 · 알림 틀 / 빈 날 · 지난 날 버튼 없음) · 고정본 다시 씀.

## 검증
| 명령 | 결과 |
|---|---|
| `npm run check` | 통과 · node 116 pass |
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 500 passed(web 규칙 「쓰기는 ui.write_attrs」 포함) |
| 저장 조각 단독 렌더(backend 라우트가 넘기는 값) | 됨 |

## backend 에 알릴 것
- 지금 트리의 저장 라우트는 `NOTICE_FIELDS` 에 `notice_id` 가 없다(폼이 보내면 400 unknown field) · 저장 응답 `notice` 에 `id` 도 없다(그 뒤 폼의 notice_id = 빈 값). 보충 1 대로 backend 가 두 곳을 맞춰야 한다.

## 보충 2 반영 (KOS 장애 = 503 kos_unavailable)
- 화면 실패 판정은 상태 숫자를 가리지 않는다(`status === 0 || status >= 400` · day.js `resNoticeFailed`) — 코드 변경 없음. 시험의 KOS 장애 응답을 502 → 503 으로 바꿈 · res-notice 7 pass · npm run check 116 pass.
