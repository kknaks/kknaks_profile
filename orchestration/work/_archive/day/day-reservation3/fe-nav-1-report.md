# [frontend] fe-nav-1 리포트 — 셸 메뉴 「현황」 · 로그인 뒤 예약 현황

워크트리 `day-reservation3`(미커밋 · 커밋 · push 안 함). backend 의 ext 파일(`schemas/ext_*` · `routers/api/ext*` · `deployment.md`)은 건드리지 않았다.

## ① 고친 파일:줄

| 파일:줄 | 고친 것 |
| --- | --- |
| `backend/day/menu.py:5` | 머리 설명 — 헤더 탭 셋은 「현황」 아래(사용자 11-27 · 옛 「홈」) |
| `backend/day/menu.py:22` | RAIL `("home", "홈", "house")` → `("status", "현황", "house")` |
| `backend/day/menu.py:36-42` | HREFS — `"status": "/reservations"` 더함 · `"reservation"` · `"procedure"` 뺌(화면 없음 = 링크 없는 글자). 탭 `reservation_board` · `procedure_board` 경로는 그대로 |
| `backend/day/routers/login.py:72-77` | `after_login()` = `"/reservations"` · docstring(사용자 2026-11-27, 11-06 결정을 바꿈) |
| `backend/day/routers/board.py:162` · `kit.py:180` · `kit_board.py:366` | `active_menu="procedure"` → `"status"` |
| `backend/day/routers/reservations.py:77` | `active_menu="reservation"` → `"status"` |
| `backend/day/templates/base.html:30` | 아이콘 줄 hx-boost 대상 `("customer", "procedure")` → `"customer"`만. 「현황」은 예약 현황으로 가는 전체 페이지 링크(예약 현황 링크가 boost 를 안 쓰던 규칙 그대로) |
| `backend/tests/day/auth/test_web_login.py:44 · 53 · 73 · 115 · 174` | 로그인 뒤 `location` = `/reservations` · 테스트 이름 「예약_현황으로」 |
| `backend/tests/day/web/test_login_device.py:148 · 155` | `hx-redirect` · `location` = `/reservations` |
| `backend/tests/day/web/test_reservation_page.py:139` | `active_menu` = `"status"` |
| `backend/tests/day/board/test_customer_chart.py:541` | `/board` 의 아이콘 줄 켜짐 = `"status"` |
| `backend/tests/day/web/test_reservations_screen.py:282-287` | 「현황」 링크 = `/reservations` · 켜짐 · boost 없음 · 「홈」 없음 · 링크 있는 메뉴 = 2개(고객 · 현황) |
| `scripts/frontend/tests/fixtures/reservations-page.html` | 고정본을 다시 만듦(`DAY_UPDATE_FIXTURES=1`) |

**키 이름**: `home` → **`status`**. 글자는 「현황」, 아이콘은 그대로 `house`다. `data-day-rail-menu` · `data-day-menu` 값도 `status`로 바뀌었다. `day.js` 의 rail aria-current 맞추기는 이 값을 그대로 비교하므로 코드를 고치지 않았다.

## ② grep 으로 센 자리

| 자리 | 고침/그대로 | 이유 |
| --- | --- | --- |
| `menu.py` RAIL `home`/「홈」 | 고침 | 사용자 결정 |
| `menu.py` HREFS `reservation` · `procedure` | 고침(뺌) | 「예약」 · 「시술」 = 화면 없음 |
| `login.py` `after_login` · `/` · `login_page`(로그인돼 있으면) · `_signed_in` | 고침(한 함수) | 모두 `after_login()` 하나를 부른다 |
| `active_menu=` board · kit · kit_board · reservations | 고침 | 탭 셋 = 「현황」 |
| `active_menu="customer"` customers ×2 | 그대로 | 고객 메뉴 |
| `base.html:30` boost 목록 | 고침 | `procedure` 키가 사라짐 |
| `app.css` `[data-day-menu="customer"]` | 그대로 | 고객만 쓰는 규칙 |
| `day.js:5799` 알림 누르기 → `/board` | 그대로 | 원장 호출 알림을 누르면 가는 곳(SPEC-005)이지 로그인 뒤 기본값이 아니다. 테스트 `test_board_feedback.py:317`도 그대로 |
| `day.js:5864` rail aria-current | 그대로 | 키 값을 비교만 한다 |
| `board.html:24` `hx-get="/board"`(세션 끝남) · `board.py`/`board_photos.py` 의 `redirect("/board")` | 그대로 | 시술 현황 자체 동작 |
| `test_web_login.py`(4) · `test_login_device.py`(2) | 고침 | 로그인 뒤 갈 곳 |
| `test_reservation_page.py` · `test_customer_chart.py` · `test_reservations_screen.py` | 고침 | 메뉴 키 |
| `test_screen_copy.py` 「홈」 | 없음 | 표에 「홈」이 없다(「현황」은 기존 탭 글자에 있다). 전체 통과 |
| `test_login_page.py:46` 「세션_없이_홈을_열면」 · `test_web_login.py:150` 「홈이_권한_없음」 | 그대로 | `/` 경로를 가리키는 테스트 이름이고 메뉴 글자가 아니다 |
| 그 밖의 `"home"` (`board` 의 귀가 대기 `why` · 앱 `format.dart` 등) | 그대로 | 다른 뜻(귀가) |

## ③ 권한 없음 · 앱 진입

- **권한 없음**: `/reservations` 는 `require_permission(RESERVATION_KEY="reservation", VIEW)`로 막고, `/board` 는 `BOARD_KEY="board"` VIEW로 막는다. 둘 다 `Forbidden` → `web_errors.forbidden_handler` → 같은 권한 없음 화면(로그아웃 버튼 보임)이다. **규칙은 같고, 보는 권한 키만 `board` → `reservation`으로 바뀐다.** 권한 행이 아예 없는 직무는 `/` 가 그 전에 403을 준다(`sessions.can_enter`, 그대로).
  - **[질문 후보]**: `board` 보기 권한만 있고 `reservation` 보기 권한이 없는 직무(시술실 직원 등)는 이제 로그인하자마자 권한 없음 화면을 보게 된다. 예전에는 바로 시술 현황이 떴다. 「현황」 링크도 `/reservations` 라서 그 직무는 헤더 「시술 현황」 탭으로 직접 가야 한다. 로그인 뒤 갈 곳을 권한 따라 고를지는 고치지 않았다(코디 · 사용자 판단).
- **앱(Flutter) · 태블릿**: `app/lib` 에 웹 `/` · `/board` 진입이 없다. 앱은 webview 패키지가 없고 `/api/...` JSON(`/api/board/stream` · `/api/reservations` 등)만 쓴다. `url_launcher` 는 개인정보 링크 · 채팅 링크에만 쓴다. Caddy 에 `/board` 리다이렉트는 없다(사진 올리기 본문 상한 경로만 있음). 태블릿 웹도 기본 진입을 따로 두지 않는다.

## ④ 검증

- `ruff check backend` 통과 · `ruff format --check` 통과(718 files).
- `scripts/test.sh --pure backend/tests/day/web backend/tests/architecture` — **679 passed**.
- `scripts/check.sh --pure` — 모두 통과(evidence `.local/checks/20261127-102759-92088`).
- `scripts/test.sh` 전체 1회 — **3297 passed**(실패 0)

## ⑤ 스펙에 고칠 줄(코디 spec 마감 때)

- **SPEC-001** 「로그인 뒤 갈 곳」: 시술 현황 `/board`(2026-11-06) → **예약 현황 `/reservations`**(사용자 2026-11-27). 권한 없음 규칙(규칙 9 · 대응표 forbidden)은 그대로이고, 보는 권한이 `reservation` 보기로 바뀐다.
- **셸 메뉴(E02 아이콘 줄 · E05 헤더 탭)를 적은 스펙/시안 메모**: 「홈」 → **「현황」**. 헤더 탭 예약 현황 · 원내 현황 · 시술 현황은 모두 「현황」 아래다. 화면이 있는 메뉴는 고객 · 현황뿐이고, 「예약」 · 「시술」 · 「매출」 · 「설정」은 링크 없는 글자다. 「현황」 링크 = `/reservations`.
- **SPEC-006**(예약 현황)이나 SPEC-002(시술 현황)에 「아이콘 줄 「예약」/「시술」이 켜진다」는 줄이 있으면 → 「현황」이 켜진다.
