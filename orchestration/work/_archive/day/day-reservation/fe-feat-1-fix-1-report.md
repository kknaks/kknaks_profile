# fe-feat-1 고침 1 결과 보고 — 코드 검수 2(F2-1 · W2-1 · W2-2)

## 상태: done (실물 확인은 코디 재기동 뒤 · 스택 안 건드림 · 커밋 안 함)

## 수행
- **F2-1** `styles/app.css` → `static/day.css`(build): `.day-res-in-card:hover { border-color: var(--ms-gray-500) }` + 시안 transition(border-color · box-shadow 150ms ease-out) — SPEC U-8 · 시안 L475. 누르기 · `is-on` 은 그대로 없음.
- **W2-1** `static/day.js`: `resInY` — 원내 목록(`[data-day-res-in]`) 스크롤 때 적고, `resInit`(폴링 · 날짜 이동으로 조각을 끼울 때)에서 되살림. 탭을 실제로 바꾸면 맨 위(시안 L2808 `side.scrollTop = 0`). 새 조각에 고른 탭을 되살릴 때 오는 `day:tab` 으로는 지우지 않음(값이 바뀔 때만).
- **W2-2** `static/day.js`: `resCatsX`(시안 catsX L1793) — `resSyncCats` 가 적고, `resInit` · 탭 전환에서 되살림. 숨은 탭(`[hidden]` 조상)에선 적지 않음(숨은 줄은 0 이라 기억을 덮지 않게).
- 시계 · 요청 추가 없음(기존 day.js 시계 하나) · 인라인 · 손 CSS 없음.

## 시험 — `scripts/frontend/tests/res-inhouse.test.mjs` +2(진짜 htmx · day.js · jsdom)
1. 목록 세로 180 → 폴링으로 새 목록이 끼워져도 180 → 날짜 이동 뒤 180 → 탭 왕복이면 0
2. 칩 줄 가로 90 → 폴링 · 날짜 이동 뒤 90 → 공지 / 예약 탭에 있는 동안 폴링이 와도 돌아오면 90
- 변이: 목록 되살림 없앰 → 1 실패 · 칩 줄 되살림(두 곳) 없앰 → 2 실패 → 되돌림.

## 검증
| 명령 | 결과 |
|---|---|
| `npm run check` | 통과 · node 109 pass |
| `./scripts/test.sh --pure backend/tests/day/web/test_reservations_screen.py backend/tests/architecture` | 333 passed(고정본 그대로 — 템플릿 안 바꿈) |

## 바꾼 파일
`backend/day/static/day.js` · `backend/day/styles/app.css` · `backend/day/static/day.css` · `scripts/frontend/tests/res-inhouse.test.mjs`
