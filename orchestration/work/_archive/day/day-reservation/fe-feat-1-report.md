# fe-feat-1 결과 보고 — 원내 현황 탭 화면(R46 ~ R48 · 계약 v2 inhouse)

## 상태: done — 실물 확인은 backend inhouse 가 붙은 뒤 코디 재기동 때(스택은 건드리지 않음)

## 수행
- `templates/partials/reservations_parts.html`
  - `side(date, weekday, notice, inhouse)` — 탭 `ui.tabs("res-side", [공지 / 예약, 원내 현황], 기본 "req")` + `ui.tab_panel` 두 개(R46 · 숫자 없음). 공지 / 예약 패널 내용은 그대로.
  - `inhouse_panel` — 칩 줄(시안 catsHtml L1790: 앞 · 뒤 꺾쇠 「앞 칩 보기」·「뒤 칩 보기」 · `role=group aria-label="보기"` L1481) · 칩 글자 = `chips[].label`(시안 L1820 처럼 숫자 없음 — `count` 는 그리지 않음) · 카드 목록 · 빈 상태 「해당하는 고객이 없어요」(L1823).
  - `inhouse_card` — 시안 stageCard L1777: 이름 · 「수납 필요」(payment_due · 빨강 테두리 배지) · 「수납 완료」(payment_done · 파랑 배지) · 단계 배지(stage.label · 색 = 표 띠와 같은 `day-res-c--*` 단계 색 토큰). 접수 = `reserved_label / nationality`(null 은 뺌) · 그 밖 = 선 아래 「상담 ○○ 실장」(counselor_name 있을 때만) + amounts 있으면 「총 합계」·「수납 필요」(unpaid > 0 = 빨강)·「수납 완료」, 금액 = 시안 n0w 「1,234 원」. 카드 = div(누르기 동작 없음 · R47 — 시안의 hover 테두리도 뺌).
- `templates/partials/reservations_main.html` — `parts.side(..., inhouse|default({'chips': [], 'items': []}))`(키가 없으면 빈 패널 — backend 가 붙으면 계약 값).
- `styles/app.css` → `static/day.css`(build) — 시안 L393 ~ 406 · L453 ~ 481 값으로 `.day-res-cats*` · `.day-res-chip` · `.day-res-in*` · `.day-res-in-card*` + `--day-res-cats-*` · `--day-res-chip-*` · `--day-res-in-shadow` 토큰. 탭 패널 = `.day-res-side > .day-tab-panel:not([hidden])` 세로 채움.
- `static/day.js`
  - `resSide`(기본 "req") · `resInCat`(기본 "all") — 화면 상태. `resApplyInhouse` = 고른 칩의 `cat` 이 아닌 카드 hidden + 순번 정렬(「전체」 = order_all · 다른 칩 = order_cat · DOM 순서 = 보이는 순서) · 다 숨으면 빈 상태 글자. 판정 · 비교 규칙은 만들지 않음(서버 순번만).
  - `resApplySide` — 새 조각(늘 기본 탭)에 고른 탭을 되살림(기존 G2 `selectTab`). `day:tab` 으로 고른 탭 기억.
  - `resInit` — 폴링 시계(기존 하나)를 **먼저** 잡은 뒤 탭 · 칩 · 칩 줄을 되살림(패널 쪽에서 무엇이 나도 폴링은 안 멈춤). 새 시계 · 새 요청 없음.
  - 칩 줄: 넘칠 때만 꺾쇠 · 끝 흐림(`--day-res-fl/fr` CSSOM), 꺾쇠 = 한 화면 2/3(L2804), 세로 휠 → 가로(L1802), 고른 칩이 잘렸으면 보이게(L1794).
- 인라인 스크립트 · style 0 · 시안에 없는 문구 0.

## 시험
- `scripts/frontend/tests/res-inhouse.test.mjs`(새 · 5개) — 진짜 htmx · day.js + 서버 렌더 고정본(계약 모양 inhouse 픽스처):
  1. 기본 탭 = 공지 / 예약 · 「전체」 = order_all 순
  2. 칩 = cat 거르기 + order_cat 순 · 「전체」로 돌아오면 order_all · DOM 순서 = 보이는 순서
  3. 고른 탭 · 칩이 10초 폴링 · 날짜 이동 · 그 뒤 폴링에도 남음 · 공지 / 예약으로 돌아간 것도 기억
  4. 폴링으로 고른 칩의 고객이 빠지면 빈 상태 · 다시 들어오면 목록
  5. 칩 줄 꺾쇠 · 흐림(넘침 흉내)
- 변이 확인: 정렬 없앰 → 2 실패 · 탭 기억 없앰 → 3 실패 → 되돌림.
- `scripts/frontend/tests/res-dom.mjs`(새) — res-browser 의 jsdom 받침을 빼서 같이 씀(+ `respond` 훅 · jsdom 에 없는 `CSS.escape` 대역). res-browser 6개 그대로 통과.
- `backend/tests/day/web/test_reservations_screen.py` — 계약 모양 `INHOUSE`(TODAY_VIEW · OTHER_VIEW 도 같은 값 = 오늘) · 새 시험 3개(칩 · 카드 글자 · 배지 · 색 클래스 · 빨강 · 빈 상태 · 다른 날짜 · 폴링에도 같이) · R33 「탭 하나」 단언 2곳을 R46 으로 바꿈 · 고정본 다시 씀.
- `backend/tests/architecture/test_screen_copy.py` — 시안 문구만: 원내 현황 · 상담 · 시술 · 실장 · 총 합계 · 수납 완료 · 원 · 해당하는 고객이 없어요 / aria: 앞 칩 보기 · 뒤 칩 보기 · 보기(근거 = 시안 줄).

## 검증
| 명령 | 결과 |
|---|---|
| `npm run check`(CSS build --check · ESLint · Stylelint · Prettier · node test) | 통과 · node 107 pass |
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 496 passed |
| ruff check · format(내 테스트 2개) | 통과 |
| 템플릿 `<script` · `<style` · ` style=` grep | 0 |

## backend 와 맞춤
- 지금 트리의 backend `presentation/reservation_inhouse.py` 출력 키 · `policies/reservation_inhouse.py` 단계 키(reception ~ procedure_done) · cat(reception · consult · procedure · going_wait)가 템플릿이 읽는 것과 같음을 확인(backend 파일은 안 건드림).

## 코디가 볼 것
1. 칩 `count` 는 계약에 있으나 시안 칩(L1820)에 숫자가 없어 그리지 않았다.
2. 시안 카드 hover 테두리(L475)는 누르기 동작이 없어(R47) 뺐다 — 필요하면 CSS 한 줄.
3. 「수납 필요」 · 「수납 완료」 배지 = 기존 `ui.sq_badge`(red outline · primary solid) — 시안 `.ib-pay` 와 높이 · 글자 1px 정도 차이.
