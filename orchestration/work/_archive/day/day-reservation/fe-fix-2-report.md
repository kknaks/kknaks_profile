# fe-fix-2 결과 보고 — 사용자 결정 6(화면 쪽) · 날짜 연타 늦춤

## 상태: done (브라우저 실물 확인은 A4 e2e 때)

## 수행
- `backend/day/static/day.js`
  - `RES_GO_DELAY_MS = 300` — 연타 늦춤 값 **한 곳**.
  - `resPick(date)` — 꺾쇠 · [오늘] · 달력이 모두 이 길로: 늦추는 날짜(`resGoDate`)를 바꾸고 팝오버를 닫고 머리 날짜 글자를 **바로** 바꾼 뒤(시안 동작), `runtime.defer(document, "res-go", …, RES_GO_DELAY_MS)` — 같은 키라 누를 때마다 마감이 뒤로 밀리고 **멈춘 뒤 마지막 날짜만** `resGo` 한 번(GET · poll 없음 · push). 중간 날짜 요청 0 → 서버 최신화 0.
  - 꺾쇠 기준 = 지금 보이는(늦추는 중인) 날짜(`resShownDate`) — 연타하면 누른 만큼 이동. [오늘] = `""`(date 없음 = 서버 오늘).
  - 머리 글자 `YYYY-MM-DD (요)` — 요일 글자는 서버가 그린 달력 머리(일 ~ 토)에서 읽는다(JS 에 한글 없음 · 문구 표 그대로). [오늘]은 보이는 날짜가 오늘이면 꺼짐.
  - 늦추는 동안 폴링은 보내지 않는다(`resBeforeRequest` — 옛 날짜 폴링이 글자를 되돌리지 않게). 날짜 요청이 나간 뒤엔 고침 1 순서 판정(`createResOrder`)이 그대로 막는다.
- `backend/day/templates/partials/reservations_main.html` — 날짜 버튼에 `data-day-res-date-label`.

## 시험
- `scripts/frontend/tests/res-debounce.test.mjs`(새 · 5개) — day.js 실제 함수(`resPick` · `resShift` · `resShownDate` · `resBeforeRequest` · `createResOrder`) + 가짜 시계(`fixture()`):
  1. 늦춤 값 한 곳 · 짧음(0 < 값 ≤ 500ms)
  2. 다음 날 5번 연타(사이 250ms) → 그동안 요청 0 · 글자 5번(24 ~ 28일) → 멈춘 뒤 요청 1번 = `2026-11-28` · 그 뒤로 더 없음
  3. 앞 · 뒤 · 달력 · [오늘] 섞어 → 마지막(`""` = 오늘) 하나만
  4. 달력에서 고른 뒤 꺾쇠 = 고른 날 기준 → `2026-12-26` 한 번
  5. 늦추는 동안 폴링 안 보냄 → 날짜 요청이 나간 뒤에도 순서 판정이 폴링을 막음(고침 1 과 같이 동작)
- 변이 확인: 늦춤을 없애면(값 0 · 바로 resGo) 3개 실패(2 pass / 3 fail) → 되돌림.
- `res-order.test.mjs`(고침 1) — 가짜 전역에 `resGoDate: null` 한 줄(새 조건 반영).

## 검증
| 명령 | 결과 |
|---|---|
| `node --test tests/res-debounce.test.mjs tests/res-order.test.mjs` | 11 pass |
| `npm run check`(build --check · ESLint(효과 경계 포함) · Stylelint · Prettier · node test) | 통과 · node 71 pass |
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 490 passed(화면 테스트 · 문구 표 · web 규칙) |
| 새 템플릿 `<script` · `<style` · ` style=` grep | 0 |
| CSS 빌드 | 안 함(CSS 안 바꿈) |

## 바꾼 파일
- `backend/day/static/day.js`
- `backend/day/templates/partials/reservations_main.html`
- `scripts/frontend/tests/res-debounce.test.mjs`(새)
- `scripts/frontend/tests/res-order.test.mjs`

## 볼 것
- 늦춤 300ms 동안 표 · 패널은 옛 날짜 그대로이고 머리 글자만 새 날짜다(시안 동작 기준 · 브리프 허용). 실물에서 어색하면 값 한 곳만 바꾸면 된다.
- 서버 쪽 「병원당 날짜 최신화 한 번에 하나」(결정 6 후반)는 backend 몫.
