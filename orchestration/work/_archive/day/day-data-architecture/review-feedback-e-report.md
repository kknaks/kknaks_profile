# 리뷰 리포트 — day-data-architecture / code · 화면 피드백 F17 · F18 · F19 (2026-11-06)

대상: 커밋 `292d0996` 이후 미커밋 변경(8 파일 · +177/−33):
- `static/day.js` · `styles/app.css` + `static/day.css`
- `templates/ui.html` · `partials/board_main.html` · `partials/board_parts.html`
- `routers/kit_board.py`(dev 견본) · `tests/day/web/test_board_page.py`

근거: `board-feedback.md` F17 ~ F19 · 발주서 · `frontend-feedback-e-report.md` · 스크린샷 · `f19-drag.gif` · cc `OrderCard`(본).
읽기 전용으로 봤다. **compose 는 건드리지 않았다.** 테스트는 `-m "not infra"` 만 돌렸다.

## 판정: PASS — 커밋 가능

세 건이 결정대로 들어갔다.
- F18 은 원인(판을 다시 받은 뒤 같은 자리에 온 완료 줄 ⋮ · 줄에 이어 누른 클릭)을 짚고, 그 창을 막았다.
- F19 는 순서 저장(`PUT /board/order` 그대로 · 놓은 뒤 한 번) · SSE(끄는 동안 · 자리 잡는 동안 미룸) · 잠긴 카드(끌기 · 비켜나기 모두 제외)와 부딪히지 않는다.
- 손 CSS · 인라인 스크립트 0.

아래 「참고」 둘은 판정 밖이다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **305 passed · 157 deselected / 4.9s**(리포트 305 와 같음) |
| `uv run ruff check backend scripts` | All checks passed |
| grep(`templates/**` · `day.js`) | `style=` 0 · `<style>` 0 · `hx-on` 0 · `on*=` 0 · `<script>` 본문 0 · `innerHTML`/`eval`/`new Function` 0 |
| `day.css` 첫 줄 `source-sha256` | `ae4758af…` = 지금 `app.css` 해시 — 다시 빌드됨 |
| 새 CSS 값 | 모두 `styles/app.css` 안. 움직임 토큰 `--day-motion-flip 220ms` · `-settle 200ms` · `-guard 450ms` · `[data-day-sort-item].is-dragging{position:relative; z-index:5}` · `.is-day-settling … .day-proc__more{…}`. 위치 · 이동은 day.js 의 CSSOM(`el.style.transform`)과 WAAPI(`el.animate`)라 CSP `style-src 'self'` 와 손 CSS 규칙(템플릿 style 속성 금지) 모두에 맞다 |

## 항목별

| # | 판정 | 근거 |
|---|---|---|
| **F17** 호출(재호출) 뒤 그 카드 선택 해제 | 결정대로 | 원인 = 판을 다시 받을 때 체크를 되살리는 상태 지키기. 호출 · 재호출 창 form 에 `data-day-clear-checks="<방문>"`(`ui.html` `doctor_call_modal(clears)` · `board_main.html` `clears=card.visitId`). `htmx:beforeSwap`(`day.js:457-`)이 **그 form 의 2xx 응답일 때만** 그 방문 몫 체크 열쇠를 지운다. 체크 열쇠를 「방문 \| 칸=값」 으로 바꿔 다른 카드 체크는 그대로다. 오류(409 등)면 체크가 남는다. 바(`[의사 호출 · N건]`)는 체크 수에서 나오니 같이 사라진다. 테스트 `test_호출_재호출_창은_보낸_뒤_그_카드_체크를_푼다` · `f17-after-call.png` |
| **F18** [종료] 뒤 더보기가 저절로 열림 | 원인을 고침 | 재현 원인: [종료] → 판 다시 받기 → 그 줄이 완료 칸으로 내려가 포인터 밑에 완료 줄이 오고, hover 로 나타나는 ⋮ 가 [종료] 자리와 같은 자리에 미끄러져 나온다. 이어 누른 클릭이 ⋮ 메뉴나 줄(차트)을 연다(`f18-after-finish-before-fix.png`). 포커스 이어짐은 아니었다(body).<br>고침:<br>① 다시 받은 뒤 `--day-motion-guard`(450ms) 동안 `is-day-settling` — 그 동안 줄 ⋮ 숨김 · 누를 수 없음(CSS) · 줄 누름(차트) · 줄 팝오버 트리거 무시(`day.js` click 위임).<br>② 줄 · 카드 자리 변화를 FLIP(220ms · `--day-ease-out`)으로 짧게 미끄러뜨린다(`afterSwap` · 스냅샷은 `beforeSwap` 에서 — 순서 맞음 · 줄은 카드 기준 자리라 이중 이동 없음).<br>사용자 결정 「시간차를 두든지 부드럽게 하든지」 그대로다. 「같은 자리에 온 새 버튼이 이어 누른 입력을 받는」 원인 창을 닫았으므로 증상 가리기가 아니다 |
| **F19** 카드 D&D cc 처럼 | 결정대로 | `day.js:291-` 포인터 이벤트(HTML5 drag ghost 아님)로 다시 썼다.<br>- 끄는 카드가 손을 따라온다(`follow` — 잡은 간격 유지 · `setPointerCapture`).<br>- 다른 카드 위로 가면 그 자리로 들어가고 비켜나기는 FLIP · 비켜나는 동안(220ms)은 다시 바꾸지 않는다.<br>- 놓으면 200ms 로 제자리에 들어간 **뒤** `emitOrder` 한 번 → `day:sorted` → `PUT /board/order`(칸 `visitIds` 그대로).<br>- 화살표 키도 같은 FLIP.<br>`f19-drag-mid/end/dropped.png` · `f19-drag.gif` |

### F19 이 부딪히지 않는지

- **순서 저장**: 저장은 놓은 뒤 자리 잡기가 끝난 시점(`done`)에 한 번이다. `pointercancel` 도 `endDrag` → `done` 이고, 애니메이션이 실패해도 `.finished.then(done, done)` 으로 반드시 끝난다. 끌기 중 바뀐 미리보기 순서가 곧 저장 순서다.
- **SSE**: `busy()`(`day.js:398-399`)에 `drag` 가 들어 있다. `drag` 는 자리 잡기(`settling`)가 끝나는 `done` 에서야 null 이 되므로, 끄는 동안과 자리 잡는 동안 판 다시 받기가 미뤄지고 끝나면 `flushRefresh` 로 한 번 받는다.
- **잠긴 카드**: `sortable(item)` = `data-day-sort-locked` 없음(`:277`). 잠긴 카드는 잡을 수 없고(`pointerdown`), 다른 카드가 그 위로 와도 자리를 바꾸지 않는다(`pointermove` 의 `over` 후보에서 제외). edit 권한이 없으면 손잡이 자체가 없다(이전 그대로).

## 조용히 통과하는 자리

새 테스트 둘(`test_호출_재호출_창은_보낸_뒤_그_카드_체크를_푼다` · `test_줄_카드_자리_열쇠와_움직임_토큰`)은 마크업 속성 · 토큰이 있는지를 본다.
- F18 가드 · F19 끌기 · F17 체크 풀기의 **동작 자체**는 pytest 로 잠기지 않는다(브라우저를 돌리지 않음). 앞 리뷰들에서 받아들인 대로 브라우저 실물 · 스크린샷 · gif 로 대신했다.
- 동작 회귀를 자동으로 잡으려면 리포트의 Playwright 스크립트(`frontend-feedback-shots/w4-repro.mjs` 방식)를 F17 ~ F19 에도 남겨 두면 좋다(낮음).

## 참고 (판정 밖)

1. **F18 가드가 모든 판 다시 받기에 걸린다** — `afterSwap`(`day.js:478-490`)은 [종료] 응답뿐 아니라 **SSE 10초 주기 · 다른 직원의 조작 신호로 다시 받을 때도** 450ms 동안 줄 ⋮ · 줄 누름(차트)을 막는다. 10초마다 0.45초씩 클릭이 먹히지 않는 창이 생기는 셈이다(그 순간 누른 클릭은 조용히 무시). 실사용에서 드물게 「한 번 더 눌러야 했다」가 나올 수 있다. 다듬으려면 가드를 **자리가 바뀐 줄**(FLIP 대상)에만 걸거나, 직원 자신의 조작 응답 뒤에만 건다.
2. **실제 `/board` 실물은 아직이다** — 데모 지점 판 카드가 0장이라 F17 ~ F19 를 같은 템플릿 · 같은 day.js 인 견본(`/dev/kit/board`)과 Playwright 대체 응답으로 확인했다(실제 KOS 쓰기 0). 판 카드가 2장 이상 생기면 끌기 1회를 실물로 볼 것(리포트 「남은 것」과 같음).
- `routers/kit_board.py` 의 `?finish=<작업 id>` 는 dev 견본 전용 라우터(prod 404 · 로그인 필요) 안의 표시용 인자다. 업무 로직 변경이 아니다.
