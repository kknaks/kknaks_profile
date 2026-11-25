# day-menu-hide 결과 보고 — 예약 현황 · 고객 메뉴 막기

## 상태: done (브랜치 `kknaksss/day-menu-hide` · origin/dev 1b5bba22 위 · 커밋 · push 없음)

## 바꾼 것

| 파일 | 내용 |
|---|---|
| `backend/day/menu.py:35-39` | `HREFS` 에서 `customer` · `reservation` · `reservation_board` 를 뺌. 그 자리에 주석 「2026-11-25 사용자 — 예약 현황 · 고객 메뉴 막음(화면 · 라우트는 그대로 · 다시 열 때 이 줄 복구)」 + 복구할 원래 값 한 줄(주석). `base.html` 의 기존 `href` None 분기를 탄다 → 아이콘 줄 「예약」 · 「고객」 = `<span class="day-rail__item">`, 헤더 탭 「예약 현황」 = `<span class="day-tab">`(지금 화면이면 `aria-current`, 아니면 `aria-disabled`) |
| `backend/tests/day/web/test_reservations_screen.py:277` | `test_reservation_rail_link_opens_full_page` → `test_reservation_customer_menus_are_text_only`(두 href · `data-day-rail-menu` 없음 · 아이콘 줄 · 헤더 탭이 글자) |
| `backend/tests/day/board/test_customer_chart.py:617` · `:640` | 고객 화면의 아이콘 줄 단언을 글자(`<span … aria-current="page">`)로. `/customers` GET · HX-Boosted 요청 자체는 그대로 200 · `#workspace` 단언 그대로 |
| `scripts/frontend/tests/fixtures/reservations-page.html:17-18 · 26` | 브라우저 시험 고정본(`test_브라우저_시험_고정본은_지금_렌더와_같다` 가 렌더와 같은지 검사). `DAY_UPDATE_FIXTURES=1` 이 `scripts/test.sh` 에서 전달되지 않아 같은 세 줄(`<a>` → `<span>`)만 손으로 고쳤고, 시험이 렌더와 같음을 확인했다. 프론트 브라우저 시험 코드에 rail · 탭 링크를 쓰는 곳은 없다 |

라우트 · 템플릿 · 서버 API · 설정값 · `base.html` 은 건드리지 않았다. 주소 직접 입력(`/reservations` · `/customers`)은 그대로 열린다.

## 다른 화면에서 이 화면으로 가는 링크 · 버튼 (목록만 — 고치지 않음)

모두 **예약 · 고객 화면 자신 안**에 있다. 판(`/board`) · 인박스 · 셸 등 다른 화면에서 `/reservations` · `/customers` 로 보내는 링크 · 버튼 · `location` 이동은 grep 결과 없다.

| 위치 | 무엇 |
|---|---|
| `templates/customer_chart.html:4` | 고객 차트 → 「고객 목록」 `<a href="/customers">` |
| `templates/partials/customers_list.html:9 · 17 · 35 · 49` | 고객 목록 쪽번호 · 거름 form · 「지우기」 · 줄 → `/customers/{id}/chart` |
| `templates/reservations.html:15 · 25` | 예약 현황 SSE(`/reservations/stream`) · 세션 끝 `hx-get="/reservations"` |
| `templates/partials/reservations_main.html:36` | 폴링 `/reservations?date=…&poll=1` |
| `templates/partials/reservations_*.html`(book · detail · dialogs · parts) | 예약 등록 · 상세 · 공지 · 취소 등 `/reservations/...` 쓰기 · 조회 |
| `static/day.js:1888-1889` | 예약 현황 날짜 바꾸기 `/reservations?date=` |
| `static/day.js:2416` · `:3045` | 예약 상세 `/reservations/visits/{id}` · 등록 창 `/reservations/book?` |

참고: `routers/api/ext.py` 의 `/reservations` · `/customers/...` 는 외부 API(다른 경로 접두어)라 메뉴와 무관하다.

## 검증

- `./scripts/test.sh -q backend/tests/day/web backend/tests/day/board/test_customer_chart.py backend/tests/day/board/test_reservation_permissions.py backend/tests/day/board/test_board_default_view.py backend/tests/architecture/test_screen_copy.py`(격리 PG · Redis) → **280 passed**. 이 중 `/reservations` · `/customers` GET 시험(권한 · 화면 · 고객 목록 · 동행)이 모두 통과한다.
  - 처음 실행에서 고정본 시험 1개가 낡음으로 실패했다 → 위 fixture 세 줄을 고친 뒤 통과.
- `uv run ruff check` · `ruff format --check`(바뀐 파이썬 3파일) → 통과.
- 브리프의 `uv run pytest` 대신 리포 정본 러너 `scripts/test.sh` 를 썼다(격리 인프라 · 사용자 스택 무접촉).
- 로컬 스택 11140: 재시작하지 않음 · 리로드 뒤 `curl http://127.0.0.1:11140/login` → **200**.

## 이슈

- 없음. 고정본은 `DAY_UPDATE_FIXTURES` 대신 손으로 고쳤다 — 코디가 원하면 직접 pytest(`DAY_UPDATE_FIXTURES=1`)로 다시 써도 같은 결과여야 한다.
