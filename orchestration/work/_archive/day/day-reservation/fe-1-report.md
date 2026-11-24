# fe-1 결과 보고 — Delivery #269 예약 현황 화면(Jinja2 + HTMX · day.js)

## 상태: done (실물 e2e A4 는 pending — 순서 조건: ① ② ③ 머지 뒤 마지막 Issue 에서 1회)

## 수행 — 템플릿 · 조각 · 정적 파일

| 파일 | 내용 |
|---|---|
| `backend/day/templates/reservations.html`(새) | 전체 페이지 — base 셸 + `#reservation-main`(V0) 안에 조각 include |
| `backend/day/templates/partials/reservations_main.html`(새) | HX 조각 — 페이지 머리(「예약 현황 \| 날짜(요)」 · 꺾쇠 · [오늘] · 달력 · [필터]) + 표 + 오른쪽 패널 + 10초 폴링 요소 |
| `backend/day/templates/partials/reservations_parts.html`(새) | 부품 매크로 — 달력 · 필터 팝오버 · 카드 · 표 · 오른쪽 패널 · state 키 → (띠 색 · 툴팁 · 필터 줄 · 모양) 표 |
| `backend/day/templates/ui.html` | 버튼 변형 `filled-black`(medikit Filled Black — 시안 L169) 하나 추가 |
| `backend/day/templates/icons.html` | `notice` 아이콘(시안 `ib-notice-20.svg` path · 옅은 면은 `day-ic__soft` 클래스) |
| `backend/day/static/day.js` | 예약 현황 절 — 날짜 바꾸기(htmx.ajax · source=`#reservation-nav` hx-push-url) · 달력(달 이동 · 칸 그리기) · 필터(화면 안 흐리게 · 다시 받아도 · 날짜를 옮겨도 남음) · 자리(카드 · 회색 면 · 열 폭 · 처음 세로 위치) · 현재 시각 선 1분마다 · 좌우 넘김 · 스크롤 지킴 · 폴링 회차 건너뛰기(팝오버 열림 · 숨은 탭). 툴팁에 `data-tip-delay`(0.3초) · 누름/키 입력에 닫힘 |
| `backend/day/styles/app.css` → `static/day.css`(빌드) | `--day-res-*` 토큰(시안 치수) + `day-res-*` 클래스 |
| `backend/tests/day/web/test_reservations_screen.py`(새) | 화면 테스트 12개 |
| `backend/tests/architecture/test_screen_copy.py` | 새 문구 근거(시안 줄 번호) — 코디 허락(contract-v1-addendum §3) |

- 렌더는 #267 실제 라우트 `GET /reservations` 를 쓰고 서비스(board_view · 권한 · 최신화)만 가짜로 — 마지막 테스트는 #267 `presentation.view(rules.board(...))` 실제 판정값을 그대로 넘겨 그린다(실제 값에 붙음 확인).
- 로컬 도구: `scripts/frontend` 에 `npm ci`(lock 그대로 · node_modules 는 gitignore).

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q backend/tests/day/web/test_reservations_screen.py` | 12 passed |
| `./scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` | 489 passed(시술 현황 화면 · 문구 · web 규칙 · 구조 포함) |
| `./scripts/build-css.sh` · `npm run check`(build --check · ESLint · Stylelint · Prettier · node test 60) | 통과 |
| ruff check · ruff format --check(내 테스트 · 문구 표) | 통과 |
| mypy --strict(내 테스트) | 내 파일 오류 0 — `day/policies/interpret/chinese.py:14` opencc stub 없음 1건은 **무관**(기존) |
| grep `<script` · `<style` · ` style=` (새 템플릿 3개) | 0 |

## Acceptance

- [x] A1 화면 구성 넣음 요소 = 시안 모양 · 문구 · 뺌 요소 안 그림(테스트 `test_뺀_요소는_그리지_않는다`)
- [x] A2 인라인 스크립트 0 · 손 CSS 0 — 자리는 day.js 가 data-* → CSSOM(style 속성 아님 · CSP) · 값은 app.css 토큰
- [x] A3 날짜 바꾸기(poll 없음 · push) · 10초 폴링(`poll=1` · push 안 함 · nav 밖이라 hx-push-url 안 물려받음) · 필터(V4 수 그대로) · 툴팁(state → 시안 글자) · 좌우 넘김 — V0 ~ V4 가짜 값 렌더 테스트
- [ ] A4 실물 e2e(로컬 · KOS 데모) — **pending**: 순서 조건(① ② ③ 다 들어간 뒤 마지막 Issue 에서 1회) · 사용자 포트/프로세스를 건드리지 않음. 브라우저 동작(JS 자리 · 달력 · 필터 · 넘김 · 폴링 실제 요청)도 그때 눈으로 확인 필요

## 계약 대조

| 항목 | 같음/다름 |
|---|---|
| 계약 S — 폴링 `GET /reservations?date=D&poll=1` + HX-Request · push 없음 / 날짜 바꾸기는 poll 없이 | 같음(테스트) |
| V0 — `#reservation-main` = 머리 날짜 줄 + 표 + 오른쪽 패널 · 셸은 전체 페이지만 | 같음(테스트) |
| V1 + 보충 — date · weekday · is_today · today · now_min · open_min · axis{start_min, end_min, time_gray_spans} | 같음 — 시간 칸 회색 = time_gray_spans 그대로 · 처음 세로 = open_min |
| V2 — columns · 「n명 / m분」 · capacity null = 「n명」 비움 | 같음 — null 이면 「m분」만(「/」도 뺌 — 아래 확인) |
| V3 — cards · state 키 → 띠 · 툴팁 · 모양 / stack_index → 가로 자리 | 같음 |
| V4 — filter.total · counts 그대로 · notice.items[].content · 「예약 요청」 제목은 템플릿 | 같음 |

## 시안 대조(시안 `20261113_예약현황_시연 (1).html`)

| 요소 | 시안 | 이 구현 |
|---|---|---|
| RV-06 ~ 08 머리 | L1446 ~ 1455 · L1635 · calHtml L2415 ~ 2420 · CSS L767 ~ 780 | 같음 — [오늘] 오늘이면 꺼짐 · 달력 일 ~ 토 · 「YYYY년 M월」 · 이전/다음 달 · 오늘 · 고른 날 |
| RV-09 · 10 필터 | L1626 ~ 1633 · L339 ~ 347 | 같음 — 깔때기 + 「필터」 · 고르면 상태 이름 + 파란 버튼 · 「전체 n」 · 선 · 7줄 · 다른 카드 25% |
| RV-11 ~ 17 표 | L305 ~ 335 · L1671 ~ 1712 · L2759 | 같음 — 52 시간 칸 · 50 머리 · 70 줄 · sticky · 지금 시각 선/표 · 넘김 (보이는 폭 − 52) × 0.8 · 끝이면 숨김 |
| RV-20 ~ 27 카드 | L350 ~ 385 · L1657 ~ 1669 · S5 L2010 · 툴팁 L2842 ~ 2847 | 같음 — 띠 3 · 이름 14/500 · 국가 12 · 「수납 필요」 테두리 · 「초진」 · 취소 가운데 줄 · 귀가 50% · 0.3초 툴팁 |
| RV-32 ~ 38 패널 | L388 · L1806 · L1813 · L1831 · L450 | 탭 「공지 / 예약」 하나 · 공지 머리 아이콘 + `YYYY.MM.DD (요)` · 글 그대로 · 「예약 요청」 제목만 · 위/아래 1:1(R14 — 시안 360 고정과 다름 · SPEC §4) |
| 카드 높이 | 늘 열 간격 한 칸(L1659) | start ~ end(SPEC §4 「시안과 다른 곳」 · R9) |

## 이슈 · 코디가 확인할 것

1. **정원 null 열 머리**: 계약 「n명 부분 비움」을 「m분」만 보이게 했다(「/ m분」의 「/」도 뺌). 「/ 30분」을 원하면 한 줄 바꾸면 된다 — 사용자 확인.
2. **카드 · 회색 면 · 선 자리는 JS 가 놓는다**(CSP 로 style 속성 금지라 data-* → CSSOM). JS 가 없으면 카드가 열 맨 위에 겹친다 — 기존 시술 현황의 툴팁 · 팝오버와 같은 방식.
3. **[오늘] · [필터] 버튼 = medikit Filled Black(gray-200 · 검정 글자)** — 시안 `btn-filled-black`. 시술 현황의 [오늘](Outlined Black · 꺼짐)과 모양이 다르다(시안 대로).
4. 날짜 앞/뒤 계산은 day.js 달력 산수(로컬 날짜 · 업무 판정 아님) · 「오늘」은 `GET /reservations`(date 없음 = 서버 오늘).
5. 폴링은 팝오버(필터 · 달력)가 열려 있거나 탭이 숨으면 그 회차만 건너뛴다(열린 팝오버가 닫히지 않게) — 다음 10초에 다시.
6. 시안 L1636 주석 「꺾쇠 없음」과 달리 SPEC RV-07 대로 꺾쇠를 그렸다(SPEC 우선).
7. 아직 못 본 것: 실제 브라우저 확인(A4 와 함께).
