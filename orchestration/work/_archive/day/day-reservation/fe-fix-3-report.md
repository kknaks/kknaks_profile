# fe-fix-3 결과 보고 — e2e 1회차 E1(폴링 멈춤) · E2(화면 쪽)

## 상태: done — 코디 재기동 뒤 실물 확인 필요(스택은 건드리지 않음)

## E1 조사
- `.run/api.log` 05:44 ~ 05:51: 오늘 10초 폴링은 정상 → 05:46:08 · 10 · 13 날짜 바꾸기(2 ~ 3초 간격 · 같은 연결) 뒤 폴링 0 · 05:46:31 날짜 바꾸기 뒤도 0. `/api/notifications/stream` 이 다시 열린 줄(45:22 · 47:31 · 49:49)은 **전체 페이지 다시 읽기**였다(새로고침). 그 사이 GET 간격이 20초 · 66초로 들쭉날쭉.
- jsdom 에 **진짜 htmx 2.0.4 + day.js + 서버 렌더 HTML** 을 올려 같은 순서(2 ~ 3초 간격 클릭 · 응답 0 / 0.2 / 1.5 / 3 / 9초)를 돌렸다. 폴링 멈춤 그 자체는 재현되지 않았다(htmx `every` 타이머는 요소가 문서에 있는 한 계속 돈다 — `ct()` 코드 확인). 대신 **같은 순서에서 진짜 결함 둘**이 나왔다:
  1. **클릭이 사라진다** — 날짜 요청 source 가 조각 안 `#reservation-nav` 였다. 앞 요청이 떠 있을 때 누르면 htmx 는 그 요소 줄에 넣는데, 앞 응답이 조각을 바꾸며 그 요소가 빠져 줄에 있던 요청이 버려졌다(LAT 9초: 3번 눌러 1번만 감). 화면은 앞 날짜에 남는다.
  2. **누른 만큼 안 간다** — 떠 있는 요청 뒤에 누르면 꺾쇠가 「화면 날짜」에서 다시 셌다(24 요청 중 또 누름 → 다시 24).
  - 폴링 쪽: 타이머가 조각마다 htmx 안에 있어, day.js 가드(팝오버 · 숨은 탭 · 늦춤 · 날짜 요청 대기)가 막힌 채 남으면 화면에서 알 수 없게 멈추는 구조였다. 실물에서 무엇이 막았는지는 로그만으로 못 가렸다(브라우저 연결 수 한도 6 · 숨은 탭 등 화면 밖 원인도 배제 못 함).

## E1 고침
- **폴링 시계 = day.js 하나**: `RES_POLL_MS = 10000` · `runtime.defer(document, "res-poll")`. **조각을 끼울 때마다 「지금부터 10초」로 다시 잡고**, 회차마다 **다음 회차를 먼저 잡은 뒤** `htmx.ajax(GET, data-day-res-poll URL, source = 폴링 요소)` — 어떤 회차가 막히거나 실패해도 다음 회차가 온다. 폴링 요청 상한 8초(걸린 요청이 다음 회차를 막지 않게).
- **날짜 요청 source = `#reservation-main`**(조각을 바꿔도 남는 요소 · `hx-push-url="true"` 를 여기로 옮김) — 떠 있을 때 누른 마지막 요청이 htmx 줄에 남아 앞 응답 뒤 나간다. 날짜 요청 상한 15초.
- 폴링 요소 = `<div hidden data-day-res-poll="/reservations?date=D&amp;poll=1" hx-push-url="false">`(push 를 끊음 · 계약 S 그대로 `poll=1`) · 조각 안 `hx-trigger` 없음.
- **기다리는 날짜**(`resNavDate`): 보낸 날짜가 화면에 들어올 때까지 꺾쇠 기준 · 머리 글자 = 그 날짜 · 그동안 폴링 쉼. 들어오면 풀림 · 요청이 실패/중단/시간 초과면 풀고 글자를 화면 날짜로.
- 고침 1 순서 판정 `createResOrder` 의 날짜 요청 대기에 **스스로 풀림(20초)** — 응답을 못 받아도 폴링이 영영 막히지 않게.
- 고침 1 · 2(순서 판정 · 300ms 늦춤)는 그대로 같이 돈다.

## E2(화면 쪽)
- 서버가 최대 3초 기다리는 동안: 표 · 패널은 이전 화면 그대로(htmx 는 응답 전까지 안 바꿈 · 로딩 글자 없음) · 머리 날짜 글자만 새 날짜 · 그 동안 폴링 0(기다리는 날짜 · 순서 판정) · 끝나면 새 날짜 조각 → 10초 뒤 그 날짜 폴링. 날짜 요청 상한 15초 > 3초.

## 시험 — 실제 브라우저 순서(브리프 요구)
- `scripts/frontend/tests/res-browser.test.mjs`(새 · 6개) — jsdom + 진짜 `htmx.min.js` · `day.js` + 서버 렌더 고정본, 가짜 시계 · 가짜 XHR(지연 조절):
  1. 오늘 — 10 · 20 · 30초 폴링(poll=1)
  2. **연타 5번 → 날짜 요청 1번(마지막 28일) → 끼움 → 10초 안에 첫 폴링 · 그 날짜로 3번 이상 계속** · 주소 줄은 날짜 바꾸기만
  3. 느린 서버(3초) · 2초 간격 3번 → 마지막(26일)이 남고 폴링 다시 돔
  4. 폴링 응답(4초)이 날짜 응답보다 늦게 와도 화면 · 폴링 모두 새 날짜
  5. 달력 열린 동안 폴링 쉼 · Esc 로 닫으면 다시
  6. E2 — 3초 기다리는 동안 표 HTML 그대로 · 머리 글자만 새 날짜 · 폴링 0 · 끝나면 새 날짜 → 다음 폴링
- 변이 확인: (a) 「끼울 때마다 · 회차마다 다시 잡기」를 없애면 5 실패/0 통과 (b) source 를 조각 안 nav 로 되돌리면 시험 3 실패 → 되돌림.
- 고정본 `scripts/frontend/tests/fixtures/reservations-page.html` · `reservations-fragment.html` — `test_reservations_screen.py::test_브라우저_시험_고정본은_지금_렌더와_같다` 가 지금 렌더와 같은지 지킨다(정적 파일 판만 0 으로) · 템플릿을 바꾸면 `DAY_UPDATE_FIXTURES=1 uv run pytest tests/day/web/test_reservations_screen.py`(backend 에서)로 다시 쓴다.
- devDependencies 추가(정확한 판 · lock 갱신): `jsdom 24.1.3` · `@sinonjs/fake-timers 13.0.5`.

## 검증
| 명령 | 결과 |
|---|---|
| `node --test tests/res-browser.test.mjs` | 6 pass |
| `npm run check`(build --check · ESLint 효과 경계 · Stylelint · Prettier · node test) | 통과 · node 77 pass |
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 493 passed |
| `uv run pytest tests/day/web/test_reservations_screen.py`(고정본 포함) | 13 passed |
| ruff check · format(내 테스트) | 통과 |
| 새 템플릿 `<script` · `<style` · ` style=` grep | 0 |

## 바꾼 파일
- `backend/day/static/day.js` · `backend/day/templates/reservations.html` · `backend/day/templates/partials/reservations_main.html`
- `backend/tests/day/web/test_reservations_screen.py`(폴링 단언 · 고정본 시험 — backend 의 `payment_required` 이름 변경은 그대로 둠)
- `scripts/frontend/tests/res-browser.test.mjs`(새) · `scripts/frontend/tests/fixtures/*.html`(새) · `res-order.test.mjs` · `res-debounce.test.mjs`(가짜 전역 · source 이름)
- `scripts/frontend/package.json` · `package-lock.json`(devDependencies 2)

## 코디가 볼 것
1. **SPEC R41 문구 「HTMX `hx-trigger="every …"`」과 방식이 다르다** — 요청은 여전히 HTMX 조각 GET · 10초 · DB 만이지만 시계는 day.js 하나다(위 이유). 문구를 「조각 폴링 10초(HTMX 조각 GET)」로 읽어도 되는지 확인 부탁.
2. 실물에서 멈춘 원인을 로그로 하나로 못 가렸다 — 재기동 뒤 같은 연타로 확인. 브라우저 개발자 도구 Network 에 `poll=1` 이 10초마다 찍히는지, 탭이 여러 개면(시술 현황 SSE 2 + 알림 SSE 1/탭) 연결 수 한도(HTTP/1.1 · 6)에 걸리는지도 같이 보면 좋다.
3. `.run/api.log` 로그에 쿼리가 안 찍혀 폴링/날짜 요청 구분이 「refresh requested」 줄로만 가능하다(backend 몫 · 참고).
