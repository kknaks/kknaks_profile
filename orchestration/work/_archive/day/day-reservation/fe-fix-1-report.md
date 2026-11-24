# fe-fix-1 결과 보고 — 코드 검수 review-code-1 F-1 · W-1 고침

## 상태: done (브라우저 실물 확인은 A4 e2e 때)

## 수행

### F-1 시안에 없는 aria-label 「예약 표」
- `backend/day/templates/partials/reservations_parts.html:85` — `<main class="day-res-board" aria-label="예약 표">` → `<main class="day-res-board">`. 시안 `.sched-wrap` · `#board` 에 이름이 없어(grep 0) **비움**.
- `backend/tests/architecture/test_screen_copy.py` HIDDEN 의 `"예약 표"` 행 삭제.
- 화면 테스트에 `<main class="day-res-board">`(이름 없음) 단언 1줄.
- 덤: 같은 표의 내 주석 한 줄이 E501(110 > 100) — 두 줄로 나눔(지난번 놓침).

### W-1 폴링 응답 × 날짜 바꾸기 응답 경쟁
- 방법 = `day.js` 에 순서 판정 `createResOrder()` + htmx 리스너 3개(`resBeforeRequest` · `resBeforeSwap` · `resAfterRequest`) — **「마지막 날짜 바꾸기가 이긴다」**:
  - 날짜 바꾸기(source `#reservation-nav`)마다 세대 +1. 그보다 앞 세대 응답(옛 폴링 · 앞선 날짜 바꾸기)은 `beforeSwap` 에서 `shouldSwap = false`.
  - 날짜 바꾸기가 떠 있는 동안 폴링은 보내지 않는다(옛 날짜 조각의 폴링 요소가 보내는 것). 끝나면(끼움 · 오류 · 중단 — `afterRequest`, 그리고 안전하게 `beforeSwap` 에서도) 대기를 푼다.
  - 기존 「팝오버 열림 · 숨은 탭이면 폴링 회차 건너뜀」은 같은 리스너로 합침.
- 이유 한 줄: `hx-sync` 는 요소마다 전략이 달라(폴링 drop · 날짜 바꾸기 replace) 두 요소 · htmx.ajax 에 나눠 달아야 하고 브라우저 없이는 순서를 시험할 수 없다. 판정을 한 함수로 두면 응답 순서와 무관하게 같은 규칙이고 DOM 없이 시험된다.
- 시험 `scripts/frontend/tests/res-order.test.mjs`(새 · 6개) — day.js 의 **실제** 리스너를 꺼내(`production()`) htmx 이벤트 순서(beforeRequest → beforeSwap → afterRequest)를 흉내 낸다:
  1. 폴링 A 가 떠 있을 때 B 로 바꿈 → B 먼저 · A 나중 도착 = A 버림
  2. A 먼저 · B 나중 도착 = A 버림 · B 끼움
  3. 날짜 바꾸기가 떠 있는 동안 폴링은 안 보냄 → 끝난 뒤 폴링은 보내고 끼움
  4. 날짜를 빠르게 두 번 → 마지막 것만(응답 순서 무관)
  5. 날짜 바꾸기 실패(afterRequest 만) → 폴링이 막히지 않음
  6. 팝오버 열림 · 숨은 탭 → 폴링 회차 건너뜀
- 변이 확인: 판정을 `accept: () => true` 로 바꾸면 3개가 실패(3 pass / 3 fail) → 되돌림.

## 바꾼 파일
- `backend/day/static/day.js`(W-1 — 순서 판정 · 리스너)
- `backend/day/templates/partials/reservations_parts.html`(F-1)
- `backend/tests/architecture/test_screen_copy.py`(F-1 행 삭제 · 주석 줄 나눔)
- `backend/tests/day/web/test_reservations_screen.py`(F-1 단언)
- `scripts/frontend/tests/res-order.test.mjs`(새 — W-1 순서 시험)

## 검증
| 명령 | 결과 |
|---|---|
| `node --test tests/res-order.test.mjs` | 6 pass |
| `npm run check`(build --check · ESLint · Stylelint · Prettier · node test) | 통과 · node test 66 pass(60 → 66) |
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 490 passed(화면 테스트 12 포함) |
| ruff check · format(내 테스트 · 문구 표) | 통과 |
| 새 템플릿 `<script` · `<style` · ` style=` grep | 0 |
| CSS 빌드 | 안 함(CSS 안 바꿈) |

## 못 한 것 · 코디가 볼 것
- 실제 htmx 2.0.4 에서 이벤트 detail(`xhr` · `elt` = htmx.ajax source)이 가정대로인지는 브라우저로 A4 e2e 때 확인(코드는 htmx 문서의 이벤트 순서 · detail 이름을 따름).
- 폴링 요소가 아직 떠 있는 옛 요청을 **취소**하지는 않는다(응답을 버릴 뿐) — 서버는 그 요청을 끝까지 처리한다(`poll=1` 이라 최신화 요청 없음 · DB 읽기 1회).
