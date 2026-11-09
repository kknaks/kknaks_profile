# Delivery #231 시술 현황 1차 ② 화면 — 결과 보고 (DAY-SPEC-002)

- 작성: day frontend 워커 · 2026-11-06 · task_882a463a1e1e
- 워크트리: 같은 워크트리 · 미커밋 · **커밋 안 함**
- compose: **내리지 않았다.** `--profile app up -d --build --wait api` 로 api 만 새 코드로 다시 올렸다. `/login` 200 이다.
- 백엔드 로직(services · routers 로직 · emr · models · migrations)은 고치지 않았다. 고친 #230 파일 둘은 아래 「고친 것 — #230 쪽」에 적었다.

## 상태: done — 단, 실제 `/board` 는 브라우저로 못 봤다(권한)

- `deploy/local.env` 에 `DAY_ADMIN_EMAILS` 가 없다. 데모 계정의 직무에는 권한 행이 0개다. 그래서 **`/board` 를 열면 권한 없음 화면(403)이 나온다**(`00-real-board-forbidden.png`). 지시대로 그 값을 직접 넣지 않았다.
- 그 대신 다음 세 가지로 확인했다.
  1. **`/dev/kit/board` 견본**: 실제와 **같은 템플릿 · 같은 규칙(`BoardRules`)** 에 지어낸 하루(`routers/kit_board.py`)를 넣었다. 브라우저로 상태와 동작을 전부 확인하고 스크린샷을 찍었다.
  2. **실제 데모 지점의 오늘 데이터를 읽기 전용으로 렌더**: 판 카드 1장 · 작업 4개(호출 1 · 준비중 3) · 확인 필요 1 · 원장 5 · 창 4개. 템플릿 오류는 없었다. DB 에 쓰지 않았다.
  3. #230 의 infra 테스트가 실제 `/board` 와 조작 라우트를 새 템플릿으로 돌린다. 통과한다.

**사용자가 열 URL**
- 견본(상태 전부): **http://127.0.0.1:11040/dev/kit/board** — 데모 계정으로 로그인한 뒤
- 실제 화면: **http://127.0.0.1:11040/board** — `deploy/local.env` 에 `DAY_ADMIN_EMAILS=<로그인 이메일>` 을 넣고 `--profile app up -d api` 를 다시 하면 보인다. 넣기 전에는 권한 없음 화면이다.

## 수행

| 파일 | 내용 |
|---|---|
| `templates/board.html` | 셸 + `#board-root`(`hx-ext="sse"` · `sse-connect="/board/stream"`) + `#board-main`(`hx-get="/board" hx-trigger="sse:board"` · `data-day-refresh` · 안쪽 조작이 `hx-target` 을 물려받음) + `sse-swap="kos_failed"` → `#day-toasts` |
| `templates/partials/board_main.html` | 판 조각(조각 계약 #230 A9: `snapshot` · `inbox` · `today`). 페이지 머리 · 인박스 3탭 · 판(D&D form `hx-put="/board/order" hx-trigger="day:sorted"`) · 창(호출 · 재호출 · 수락 · 차트) · 더보기 메뉴 |
| `templates/partials/board_parts.html` | 조립 매크로(방문 카드 · 시술 줄 값 · 인박스 · 호출 탭 · 시술 완료 카드 · 마취 칩 · 원장 줄 · 창). **#229 ui.html 매크로에 스냅샷 값만 꽂는다 — 새 클래스 · 색 · 치수 0** |
| `templates/partials/board_toast_error.html` · `board_toast_kos_failed.html` | 오류 토스트(oob) · KOS 반영 실패 토스트(「방 · 고객 — 문구」) |
| `static/day.js` | 아래 「day.js」 |
| `templates/ui.html`(#229 매크로 손질 — 새 매크로 아님) | `check_item(form=, title=)` · `proc_row` 의 `action_attrs` · `field` · `locked` · `form` · `doctor_call_modal` 의 `form_id` · `target` · 숨은 칸 `target` / `doctorStaffId` · 동적 「호출할 시술」 · 라디오 이름 `pick` · `chart_modal` 섹션 `data-day-sec` · `memo(keep=)` |
| `web.py` | 표시 필터: `day_hm` · `day_date_label` · `day_age` · `day_plus_min` · `day_mmss` · `day_short` · `day_span_min`. 글자 모양만 만든다. 판정은 서버 값을 쓴다 |
| `routers/kit_board.py` · `main.py`(라우터 한 줄) | 견본 `/dev/kit/board`(dev · 로그인 필수) |
| 테스트 | `tests/day/web/test_board_page.py`(DB 없음 · 11개) · `test_web_rules.py`(Jinja 주석의 `#230` 같은 이슈 번호는 색 grep 에서 뺌) · `test_kit.py`(창 마크업 변경 반영) |

### day.js (이벤트 위임 + data-* · 인라인 스크립트 · `hx-on` 0)

- **조작 오류 토스트**: htmx 는 4xx 응답을 끼우지 않는다. 그래서 `X-Day-Error` 헤더가 있는 응답은 `htmx:beforeSwap` 에서 `shouldSwap = true` 로 끼운다. 본문은 oob 토스트이고 `HX-Reswap: none` 이라 판은 그대로다(#230 이 맡긴 일).
- **SSE 로 판 다시 받기**:
  - 창 · 메뉴 · 끌기 중에는 미룬다(`htmx:beforeRequest` 취소). 창이 닫히면 바로 다시 받는다.
  - 받을 때 화면 상태를 지킨다 — 체크 · 인박스 탭 · 접힘 · 메모 펼침 · 검색 글자 · 스크롤 · 고른 카드.
  - **확인 필요가 새로 생긴 카드만** 빨강으로 두 번 깜빡인다(처음 그릴 때는 안 깜빡임).
- **의사 호출 창**:
  - 카드의 준비중 체크는 HTML `form` 속성으로 그 카드의 창 form 에 딸려 있다. 창을 열면 「호출할 시술 · N개」를 체크로 채운다.
  - 줄을 고르면 숨은 `target`(all · one)과 `doctorStaffId` 를 채우고, 버튼을 「의사를 선택하세요」(꺼짐)에서 「호출」 · 「재호출」 · 「수락」으로 바꾼다.
- **인박스 카드 → 판 카드**: 고르면 스크롤하고, 같은 방문의 카드는 모두 선택, 나머지는 흐리게 한다(U-10).
- **시술 완료 탭 찾기**: 이름 · 발음으로 거른다. 찾은 글자는 `<mark>` 로 표시한다(DOM 으로 만들고 innerHTML 은 쓰지 않음). 0건이면 빈 상태와 [조건 지우기]를 보인다.
- **줄을 누르면 차트**: 그 시술 섹션만 깜빡인다(`data-day-flash-sec`).
- **SSE 토스트**: `sse-swap` 이 끼운 토스트도 보이게 `#day-toasts` 를 MutationObserver 로 본다.
- #229 의 1초 경과 · D&D(귀가 대기 카드는 잠김) · 체크 혼합 · 메모 · 팝오버는 그대로 쓴다.

## Acceptance

| # | 결과 | 근거 |
|---|---|---|
| A1 넣음 요소 전부 · 뺌 요소 없음 | 같음 | 아래 대응표 · `test_셸_머리_인박스_판이_다_있다` · `test_뺀_요소는_없다`(방 옮기기 · 연결 · 돌아가기 없음) |
| A2 손 CSS · 인라인 스크립트 · 새 컴포넌트 0 | 같음 | `test_web_rules.py` 전부 통과(style · 임의값 · 색/치수 · `<script>` 본문 · on* · `hx-on` · 클래스 전부 빌드 CSS 에 있음 · `app.css` 지문 그대로 = CSS 다시 빌드 불필요). 새 클래스 0 · 새 토큰 0 |
| A3 상태별 화면 | 같음(견본) | 스크린샷 01 ~ 14 · `test_시술_줄_5상태와_버튼` · `test_확인_필요_마취_3상태_수납_필요_귀가_대기` · `test_시술_완료_탭_찾기_빈_상태_차트`. 빈 판(「지금 판에 앉은 고객이 없어요」) · 인박스 빈 칸(개수 0)은 렌더 테스트로만 봤다 |
| A4 두 화면 SSE | **브라우저로 확인 못 함** | 권한(위). 판 다시 받기 경로(`sse:board` → `GET /board` 조각)와 #230 SSE 테스트(`test_board_sse.py` — 조작 직후 `board` 신호 · 첫 `board` · `kos_failed` 토스트 조각)는 통과한다. 권한이 열리면 두 창 실물을 할 수 있다 |
| A5 호출 · 재호출 · 수락 창 | 같음 | 브라우저: 호출은 기본 선택 없음 · 꺼진 「의사를 선택하세요」 → 고르면 「호출」 · target all/one. 재호출 기본 = 처음 대상(박지호 · 「처음 호출」 꼬리표). 수락은 「모든 의사」 줄 없음. `test_의사_호출_창_재호출_수락_기본_선택` · `test_보는_사람이_원장이면_수락_기본은_본인` |
| A6 오류 토스트 · kos_failed 토스트 | 조각 렌더 테스트 + #230 infra | `test_토스트_조각`(oob · 「방 · 고객 — 문구」) · #230 `test_board_api`(409 → 토스트 조각 + `X-Day-Error`) · `test_board_sse`(failed 순간 한 번). 브라우저 실물은 권한 때문에 못 했다(견본 조작은 403) |

## E 번호 ↔ 템플릿

| E | 요소 | 템플릿 · 매크로 |
|---|---|---|
| E01 ~ E05 | 셸 · 아이콘 줄(시술 현재) · 헤더 탭(시술 현황 → `/board`) | `base.html`(#229) |
| E04 | 병원 이름 | `view.hospital_name`(세션) |
| E06 | 고객 검색(자리만) | `base.html` |
| E07 | 「시술 현황 \| 2026-11-06 (금)」 | `board_main` `ui.page_head` + `day_date_label` |
| E08 | 날짜 이동 | 이 화면에선 쓰지 않음(날짜 글자만 · 시안 dateNav=false) |
| E09 · E10 | [필터] · 보기 바꾸기(자리만 · 꺼짐 · 「의사별 · 구역」 — SPEC 낱말) | `board_main` `ui.icon_button` · `ui.segment(disabled)` |
| E11 · E12 | 툴팁(마취 종료 · 재시작 · 필터) · 토스트 | `ui.sq_badge(tip=)` · `board_toast_*` |
| E15 · E16 | 인박스 · 탭 「현황 / 호출 n(수락 대기) / 시술 완료 n(귀가 대기)」 | `board_main` |
| E17 | 확인 필요 · 시작 가능 · 시술 대기 / 수락 대기 · 수락함(개수) | `ui.accordion` |
| E18 ~ E22 | 인박스 카드 · 고객 줄 · 원장 줄(수락 · 호출 +mm:ss · 재호출 +mm:ss) · 응답 없음 · [재호출] | `parts.inbox_card` · `parts.call_lines` |
| E23 | 호출 탭 카드 · [수락] | `parts.call_card` |
| E24 | 시간 배지(마취) | `parts.anesthesia_chip(button=false)` |
| E25 ~ E28 | 완료 탭 검색 · 찾은 글자 · 빈 상태 · 완료 카드(입실-귀가 · 귀가 대기 / 귀가 배지) | `board_main` · `parts.done_card` · day.js 찾기 |
| E29 · E30 | 시술 링크 줄 · 차트 아이콘 on/off | `parts.done_card` · `ui.chart_icons` |
| E31 | 보드(빈 방 없음 · 빈 판 빈 상태) | `board_main` |
| E32 · E33(머리 줄) | 방문 카드 · 머리 줄 | `parts.room_card` |
| E34 | 손잡이 · D&D → `PUT /board/order` | `ui.grip` · `data-day-sort` form |
| E35 | 경고 아이콘(확인 필요) | `icon("warn")` |
| E36 | 마취 칩 3상태 | `parts.anesthesia_chip` |
| E37 · E38 | 고객 줄(누르면 차트) · 바이탈(성별 미지정이면 비움 · 만 나이 · 입실) | `parts.customer` |
| E39 | 오더 메모(5줄 넘으면 크게 보기) | `ui.memo(keep=)` |
| E40 · E42 | 전체 선택(혼합 · 꺼짐) · 꺼진 체크 | `ui.check_all` · `ui.proc_row` |
| E41 · E43 · E44 · E45 | 시술 줄 5상태 · 시간 칸 · 줄 버튼(시작 · 종료 · 수락) · 더보기 | `parts.proc` → `ui.proc_row` |
| E46 | [의사 호출 · N건] / [귀가 대기] | `ui.actionbar` |
| E50 | 더보기 메뉴 「시작 취소」 · 「완료 취소」(확인 창 없음) | `parts.proc_menu` |
| E51 · E52 | 의사 호출 · 재호출 · 수락 창 · 아바타(이름 순 % 3 톤) | `parts.call_dialog` → `ui.doctor_call_modal` |
| E55 · E56 | 차트 모달(읽기 전용 · KOS 메모만) | `parts.chart` → `ui.chart_modal` |
| 수납 필요(U9) | 카드 고객 줄 · 인박스 카드 머리 | `ui.payment_required` |
| 뺌 | E33 방 이름 버튼 · E47 · E48 · E49 · E53 · E54 | 없음(테스트) |

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **268 passed** |
| `scripts/test.sh -q`(compose postgres · redis 를 같이 씀 · 내리지 않음) | **406 passed**(#230 테스트 포함) |
| `uv run ruff check` — 내가 고친 파일 | 통과. 저장소 전체에는 E501 5건이 남아 있는데 모두 #230 워커가 지금 고치는 파일이다(`services/sessions.py` · `dtos/auth.py:76` · `routers/board.py` · `tests/day/board/test_board_queries.py` · `test_board_sse.py`). 내가 손대지 않았다 |
| 브라우저(headless Chromium · 1600×1000 · 데모 계정 로그인) | 체크 2 → 바 「의사 호출 · 2건」 · 전체 선택 체크 → 창 「호출할 시술 · 2개」 · 꺼진 버튼 → 「모든 의사」 → target=all → 원장 → target=one. 인박스 → 판 고르기(같은 방문 카드 3장 선택). 재호출 기본 박지호. 수락 창 · 더보기 「시작 취소」 · 줄 → 차트 깜빡임. 메모 펼침. 찾기 「아름」 1건 + `<mark>` · 0건 빈 상태 · 지우기. D&D 미리 바뀜 → `PUT /board/order visitIds…`(견본이라 403) |
| 실제 데모 데이터 읽기 렌더 | 카드 1 · 작업 4 · 호출 1 · 원장 5 · 오류 없음 |

## 스크린샷 (`frontend-231-shots/` · 15장)

`00-real-board-forbidden`(실제 `/board` · 권한 없음) · `01-board`(견본 전체) · `02-checked-actionbar` · `03-call-modal` · `04-call-modal-picked` · `05-inbox-select` · `06-recall-modal` · `07-calls-tab` · `08-accept-modal` · `09-more-menu` · `10-chart-modal` · `11-memo-open` · `12-done-search` · `13-done-empty` · `14-dragging`

## 고친 것 — #230 쪽 (코디가 알 것)

- `tests/day/board/test_board_api.py` 한 줄: 자리 템플릿 글자 `need 0 · startable 0 · waiting 1` 을 단언하던 것을 인박스 아코디언 개수 정규식으로 바꿨다. `data-visit-id` 단언은 방문 카드에 그 속성을 남겨 그대로 통과한다.
- 그 밖의 #230 파일은 고치지 않았다.
- 작업하는 동안 #230 워커가 같은 워크트리를 고치고 있었다(`test_board_queries.py` 새 파일 · `WebView` 에 전체 권한 칸 · `routers/api/auth.py` · `routers/login.py` 변경). 내 변경과 겹치는 파일은 `test_board_api.py` 한 곳뿐이다.

## 정한 것 · 코디 확인

1. **문구를 내가 지었다**: 빈 판 「지금 판에 앉은 고객이 없어요」 · 완료 탭이 아예 비면 「시술 완료 고객이 없어요」.
2. **E10 세그먼트 낱말**: 시안의 「의사별 / 4층 / 미사용」 대신 SPEC 표 낱말 「의사별 · 구역」을 썼다. 꺼진 채 둔다(추정 금지).
3. **원장 상태 글자의 ○○ = 방 이름**이다(백엔드가 `room` 을 준다). 원천 스크린샷의 「대기」와 어떻게 맞출지는 디자인 몫으로 남는다(SPEC U-4).
4. **아바타 톤 = 원장 이름 순 % 3**: 의사 ↔ 색 규칙이 도메인에 없어(DS 조사 §6), 순서가 바뀌어도 색이 안 바뀌게 이름 순으로만 고정했다.
5. **고객 이름(E37)을 누르면 차트 모달**을 연다. 시안은 「차트 화면(아직 없음)」이다.
6. **권한이 없는 조작은 403 이고 화면에 아무것도 안 뜬다**(`web_errors` 의 권한 없음 조각은 htmx 가 끼우지 않는다). view 권한만 있는 사람이 버튼을 누르는 경우가 여기에 해당한다. 토스트로 알릴지는 결정이 필요하다.
7. **데모 지점 원장 목록의 이름 하나에 「명동」 이 들어 있다.** KOS 데모 테넌트의 계정 이름(데이터)이고, 코드 · 템플릿에 박은 것이 아니다. 실물 화면 스크린샷을 찍으면 보일 수 있다.
8. `PROCEDURE_WAITING` 열기(시작 취소 → KOS)는 #230 의 결정 거리다. 화면은 지금처럼 버튼을 보이고, KOS 쓰기는 백엔드가 막는다.

## 남은 것

- 실제 `/board` 브라우저 확인과 A4 두 화면 SSE 실물 — `DAY_ADMIN_EMAILS`(사용자) 또는 권한 표가 생긴 뒤.
- A6 KOS 반영 실패 토스트 실물 — 실제 KOS 쓰기(#230 A8) 뒤.
