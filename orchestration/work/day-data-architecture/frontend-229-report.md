# Delivery #229 (DAY 웹 기반 · medikit HTMX 컴포넌트) + 웹 로그인 화면: 결과 보고

- 작성: day frontend 워커 · 2026-11-06 · task_5725534585b1
- 워크트리 `CENTURION_DAY/day-data-architecture`(브랜치 `kknaksss/day-data-architecture`, #224 ~ #227 위) · **커밋 안 함**
- 스크린샷: `frontend-229-shots/`(34장, 아래 「스크린샷」)

## 상태: done

- #229 phase 1 ~ 7을 모두 했다. A1 ~ A9를 모두 확인했다.
- 코디가 중간에 순서를 바꿨다(로그인 화면 먼저). 그래서 로그인 화면(`/login` · `/login/hospital` · `/logout` · `/`)도 같이 만들었다.
- **compose `--profile app`을 띄운 채로 두었다.** api · worker · scheduler · postgres · redis가 떠 있다. 사용자는 **http://127.0.0.1:11040/login** 을 열면 된다.

## 수행: 파일

| 위치 | 파일 | 내용 |
|---|---|---|
| static/(벤더링) | `medikit.css` · `medikit.js` | centurion `origin/main:docs/development/medikit-htmx-kit/`를 그대로 복사했다(고치지 않음) |
| | `htmx.min.js`(2.0.4) · `HTMX-LICENSE.txt` | centurion `backend/admin/static`에서 복사 |
| | `htmx-ext-sse.js`(2.2.4) · `HTMX-EXT-SSE-LICENSE.txt` | npm `htmx-ext-sse@2.2.4`(0BSD). 벤더링만 하고, SSE 연결은 Non-Goal |
| | `PretendardVariable.woff2` · `PRETENDARD-LICENSE.txt` | centurion `backend/sso/static/admin`에서 복사. 키트 README의 「글꼴은 DAY가 둔다」 |
| | `day.js` | DAY 부품 동작 전부. 이벤트 위임 + `data-*`만 쓴다 |
| | `day.css` | **빌드 결과**(커밋 대상 · 손으로 고치지 않음) |
| styles/ | `app.css` | DAY 토큰(`html[data-product="crm"]`, `--ms-*` 덮기 + `--day-*`) + `day-*` 컴포넌트 클래스. **새 값은 여기에만 있다** |
| | `medikit-preset.json` | centurion `backend/admin/styles/medikit-preset.json` 사본(medikit 1.4.0) |
| | `tailwind.config.mjs` · `build.mjs` | centurion admin과 같은 구성이다. 도구는 저장소 밖(`DAY_CSS_TOOLS`)에 둔다 |
| scripts/ | `build-css.sh` | tailwindcss 4.3.4 · postcss 8.5.32를 `~/.cache/day-css-tools`에 고정 설치한 뒤 빌드한다. AGENTS.md 실행 명령에 한 줄 추가 |
| templates/ | `base.html` | CRM 셸(G1), htmx-config, `#modal-root` · `#day-toasts` 자리, **`<body hx-headers='{"X-CSRF-Token": …}'>` 한 곳**, 로그인했을 때만 [로그아웃] |
| | `ui.html` | 매크로 전부(아래 대응표) |
| | `icons.html` | 시안 assets의 path를 그대로 옮기고 currentColor로 바꿨다. 아이콘 30종 |
| | `kit.html` · `partials/kit_page.html` · `kit_modal.html` · `kit_echo.html` | 견본 페이지(dev 전용) |
| | `login.html` · `partials/login_card.html` · `home.html` · `partials/toast_only.html` | 로그인 · 병원 고르기 · 빈 홈 · CSRF 실패 토스트 |
| day/ | `web.py` | Jinja2 · `render`(HX 분기 · `Vary` · **CSP 헤더**) · `redirect`(303 / 204 + HX-Redirect) · `day_mark` 필터 · `LoginRequired` |
| | `main.py` · `menu.py` | 화면 라우터 · 정적 마운트 · 예외 처리 묶음 · 아이콘 줄과 헤더 탭 목록 |
| | `routers/kit.py` | `/dev/kit` · `/dev/kit/modal/{call,recall,accept,chart}` · `POST /dev/kit/echo`(CSRF 견본). prod에서는 404 |
| | `routers/login.py` | `/login` · `POST /login` · `POST /login/hospital` · `POST /logout` · `/` |
| | `session.py` | `optional_web_session` · `required_web_session` 추가. 기존 함수는 고치지 않았다 |
| | `public.py` · `runtime/main.py` | `web_routers` · `static_mount` · `web_exception_handlers`를 연결 |
| 의존성 | `pyproject.toml` · `uv.lock` | `jinja2>=3.1,<4` 추가(Jinja2Templates에 필요) |

## 웹 로그인 화면 (코디 우선순위 변경분)

- **로직은 #227 service를 그대로 부른다.** `auth.login` · `auth.choose_hospital` · `sessions.logout` · `sessions.current_session`이다. 앱 JSON과 같은 `auth_deps` 의존성을 써서 테스트 override도 같이 먹는다. 쿠키는 웹 라우트에서 `set_session_cookie` · `clear_session_cookie`로 심고 지운다.
- **문구**: SPEC-001 대응표의 13줄과 「로그아웃했습니다」를 그대로 옮겼다(`routers/login.py` `MESSAGES` · `NOTICES`). 처음 보는 오류 코드가 오면 문구를 지어내지 않고 KOS 장애 문구로 보인다.
- **실패하면** 입력한 이메일은 그대로 두고 비밀번호 칸은 비운다. `invalid_request` · `invalid_credentials`이면 입력칸도 빨갛게 표시한다.
  - HTMX 요청에는 200 조각을 준다(htmx는 4xx 응답을 바꿔 넣지 않는다).
  - 일반 요청에는 오류 HTTP 코드와 전체 페이지를 준다.
- **병원이 여럿이면** 같은 카드 자리에 고르기 목록을 그린다(centurion `choose.html` 모양).
  - 임시 토큰은 **숨은 폼 칸에만** 싣는다.
  - 만료됐거나 이미 쓴 토큰이면 `/login?reason=session_expired`로 보낸다.
- **로그아웃**: 버튼에 `hx-post`(hx-headers 토큰)를 달고, JS가 없을 때를 위해 폼에 `csrf_token` 칸도 둔다.
  - CSRF가 틀리면 「페이지가 오래되었습니다…」 토스트를 띄우고 `HX-Reswap: none`으로 화면을 그대로 둔다.
  - 성공하면 `/login?reason=logged_out`으로 보낸다.
- **세션 없이 `/`를 열면 `/login`으로 보낸다.** 만료된 세션이면 `?reason=session_expired`를 붙인다. HTMX 요청이면 204 + `HX-Redirect`로 보낸다.
- **로그인 뒤 갈 곳**: dev 서버면 `/dev/kit`, 그 밖은 빈 홈(`home.html`)이다. `/`를 열면 dev에서는 견본으로 보낸다.
- 모양은 centurion 로그인 카드(400 · 모서리 16)를 따랐다. 입력은 `ui.input_box('l')`, 버튼은 `ui.btn('primary','l')`, 안내는 `ui.banner`다.
- **카드 문구 셋은 근거 문서에 없어서 내가 정했다.** 「KOS 계정으로 로그인합니다.」 · 「병원 선택」 · 「로그인할 병원을 고르세요. 다른 병원으로 바꾸려면 다시 로그인합니다.」(뒤 문장은 SPEC U-2의 뜻을 옮긴 것). 아래 「코디가 확인할 것」 1.

### 브라우저 실물 (compose app · 11040 · headless Chromium · 데모 계정 = 시드의 KOS 시스템 계정)

| # | 동작 | 결과 |
|---|---|---|
| 1 | `/` 열기(쿠키 없음) | `/login`으로 이동 |
| 2 | 틀린 비밀번호 | 「이메일 또는 비밀번호가 맞지 않습니다 (KOS 계정과 같습니다)」 · 이메일 남음 · 비밀번호 빔 |
| 3 | 이메일을 비우고 제출 | 「이메일과 비밀번호를 모두 입력해 주세요」 |
| 4 | 데모 계정 로그인 | `/dev/kit`로 이동(연결 병원 1개라 자동) · `body[hx-headers]`에 X-CSRF-Token 있음 |
| 5 | 견본의 [HTMX POST 보내기] | 토스트 「CSRF 확인 — 요청이 통과했어요」(**A9**) |
| 6 | [로그아웃] | `/login?reason=logged_out` 「로그아웃했습니다」 · `day_session` 쿠키 없어짐 |

`Secure` 쿠키는 Chromium에서 http://127.0.0.1 로도 받았다. 다른 브라우저(Safari 등)는 확인하지 않았다.

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **210 passed** |
| `scripts/test.sh -q`(로컬 compose PostgreSQL · Redis, `DAY_REQUIRE_INFRA=1`) | **305 passed** |
| `uv run ruff check backend` · `ruff format --check` | 통과 |
| `scripts/build-css.sh` | `day.css 48.0KB (tailwindcss 4.3.4 · medikit 1.4.0)` |

새 테스트:
- `tests/architecture/test_web_rules.py`: grep 13개
  - style 속성 · `<style>`
  - tailwind 임의값 `x-[…]`
  - 템플릿 안 hex · rgb · px 등 값
  - 템플릿이 쓰는 `ms-*` · `day-*` 클래스가 빌드된 CSS에 다 있는지(**빌드를 잊으면 실패한다**)
  - 인라인 `<script>` · 허용 목록 밖 src
  - `on*=` · `hx-on` · `javascript:`
  - JS의 eval · `new Function` · 문자열 타이머 · `day.js`의 innerHTML
  - 라이선스 3개 · htmx-config `allowEval:false` · `allowScriptTags:false` · CDN 없음
- `tests/day/web/test_kit.py`: dev 200 · prod 404 · HX 조각 · 뒤로가기 복원은 전체 페이지 · 28개 섹션 · CSP · 의사 호출 창 원천 모양 · 재호출 기본 선택 · 수락 모드
- `tests/day/web/test_login_page.py`: DB 없이 로그인 화면 · reason 안내 · 모르는 reason 무시 · `/` → `/login`(303 · HX 204)
- `tests/day/web/test_mark.py`: 찾은 글자 escape
- `tests/day/auth/test_web_login.py`(infra · 가짜 KOS 경계):
  - 로그인 → 쿠키 속성 → 견본 `hx-headers` → **A9 echo 200 / 토큰 없으면 403 `csrf_failed`**
  - 실패 문구 · 이메일 유지 · 빈 입력이면 KOS를 안 부름 · 연결 병원 없음
  - 병원 여럿 → 숨은 칸 → 고르기 → 같은 토큰을 다시 쓰면 `session_expired`
  - 로그아웃 CSRF 토스트 → 성공 → 쿠키 지움 → `/`가 `/login`으로

## Acceptance 대조

| # | 결과 | 근거 |
|---|---|---|
| A1 견본(dev 전용 · prod 404) · 상태별 | 같음 | `/dev/kit` 섹션 28개(아래 대응표 「그린 상태」) · `test_kit.py` |
| A2 손 CSS 0 | 같음 | 템플릿에 style · 임의값 · 색과 치수 값이 0개다. 새 값은 `styles/app.css` 토큰에만 있다. `test_web_rules.py` · 응답 CSP `style-src 'self'` |
| A3 인라인 스크립트 0 | 같음 | `<script>` 본문 · on* · hx-on · eval 0개. JS는 day.js · medikit.js · htmx · sse 확장뿐이다. CSP `script-src 'self'` |
| A4 대응표 | 같음 | 아래 표 |
| A5 키트 올릴 후보 | 같음 | 아래 목록 |
| A6 벤더링 · 라이선스 · htmx-config | 같음 | static/ · base.html meta · 테스트 |
| A7 브라우저 스크린샷(1280×720 이상) | 같음 | 1440×900 · 섹션 28장 + 상호작용 5장 + 로그인 5장 |
| A8 의사 호출 모달 | 같음 | 아래 「의사 호출 창」 · `23-call.png` · `i3` · `i4` |
| A9 CSRF hx-headers | 같음 | base.html 한 곳 · infra 테스트 · 브라우저 #5 |

## A4 대응표: SPEC-002 화면 구성 1차 요소 → 매크로

검수의 「참고 1」대로 **「넣음 · 자리만 · 수납 필요」를 모두 포함했다.** 그린 상태는 견본(`/dev/kit#kit-…`)에서 보이는 상태다.

| E | 요소 | 매크로 · 조합 | G | 그린 상태(견본 섹션) |
|---|---|---|---|---|
| E01 | 앱 틀 | `base.html` `.day-app` · `.day-main` | G1 | 셸 그 자체(모든 페이지) |
| E02 | 아이콘 줄 | `base.html` `.day-rail` + `menu.py` | G1 | 기본(42%) · 현재(100%) — `00-viewport` |
| E03 | 헤더 | `base.html` `.day-header` | G1 | 〃 |
| E04 | 병원 이름 | `base.html` `.day-hospital`(값 = `hospital_name`) | ― | 견본은 가짜 이름 · 홈은 `me().hospital_name` |
| E05 | 헤더 탭 | `base.html` `.day-tab` · `ui.tabs(variant=header)` | G2 | 현재 · 꺼짐(화면 없음) — `12-tabs` |
| E06 | 고객 검색 28 (자리만) | `ui.search(size="ss", header=true)` | ― | 빈 칸 — `04-inputs` |
| E07 | 페이지 머리 | `ui.page_head` | ― | 날짜 글자 — `02-shell` |
| E08 | 날짜 이동 (자리만) | `ui.page_head(date_nav=true)` | ― | 꺼짐(이 화면) · 켜짐 — `02-shell` |
| E09 | [필터] (자리만) | `ui.icon_button(tip=)` | G3 | 기본 · 꺼짐 · 툴팁 — `03-buttons` · `i1` |
| E10 | 보기 바꾸기 (자리만) | `ui.segment` | G2 | 선택 · 꺼짐 — `12-tabs` |
| E11 | 툴팁 | `ui.tip` · `data-tip` + day.js · `ui.tip_static` | G3 | 보이는 상태 · hover — `06-tooltip` · `i1` |
| E12 · E57 | 토스트 | `ui.toast` · `ui.toast_oob` · `#day-toasts` | ― | 성공 · 오류(KOS 실패) · 실제 oob — `10-toast` · `l4` |
| E15 | 인박스 칸 | `.day-inbox`(조합) | ― | `27-inbox` |
| E16 | 인박스 탭 | `ui.tabs(variant=inbox)` + `ui.tab_panel` | G2 | 현황 · 호출 · 시술 완료 — `12-tabs` · `27-inbox` |
| E17 | 접는 칸 머리 | `ui.accordion` | G4 | 펼침 · 접힘 · 아이콘(경고 · 체크 · 빼기) · 개수 — `09-accordion` |
| E18 | 인박스 카드 | `ui.dense_card("inbox")` + `ui.card_head` | G5 | 기본 · 선택 · 선택+늦음 · 새로 늦음(깜빡임) · 흐림 — `13-cards` |
| E19 | 카드 줄 | `.day-line`(조합) | ― | `13-cards` · `27-inbox` |
| E20 | 원장 줄 | `.day-line` + `ui.elapsed` | G13 | 수락 · 호출 +mm:ss(늦음 빨강) · 재호출 — `20-elapsed` |
| E21 | 응답 없음 | `.day-line--prev` | ― | `20-elapsed` · `27-inbox` |
| E22 | [재호출] | `ui.btn('gray','ss')` | ― | `03-buttons` · `27-inbox` |
| E23 | 호출 탭 카드 | `dense_card` + `.day-dots` + `ui.btn('primary','ss')` | ― | `27-inbox`(호출 탭) |
| E24 | 시간 배지 | `ui.sq_badge` | G6 | solid primary · red · gray · going-wait · yellow / outline — `14-badges` |
| E25 | 완료 탭 검색 + X | `ui.search(clearable=true)` | ― | 빈 칸(X 숨김) · 글자 있음(X) — `04-inputs` |
| E26 | 찾은 글자 | `day_mark` 필터 | G7 | `15-mark` · `27-inbox` |
| E27 | 빈 상태 | `ui.empty_state` | ― | `25-empty` · `27-inbox` |
| E28 | 시술 완료 카드 | `dense_card` + `.day-card__time` + `sq_badge(going-wait)` | G5 · G6 | 선택(차트 열림) — `27-inbox` |
| E29 | 시술 링크 줄 | `.day-linkrow` | ― | hover · 말줄임 — `16-icons` |
| E30 | 차트 아이콘 | `ui.chart_icons` | G8 | on · off — `16-icons` |
| E31 | 보드 | `.day-board` · `.day-board__grid` | ― | `28-board` |
| E32 | 방 카드(방문 카드) | `ui.dense_card("room")` | G5 | 기본 · 선택 · 선택+늦음 · 흐림 · 드래그 중 · 귀가 대기(흐림) — `13-cards` |
| E33 머리 줄 | 방 머리 줄 | `.day-card__head` · `.day-card__title-wrap` | G5 | `13-cards` · `28-board` |
| E34 | 손잡이 · 순서 | `ui.grip` + `data-day-sort*` | G9 | 끌기 · 화살표 키 · 잠긴 카드(귀가 대기) — `17-sort` |
| E35 | 경고 아이콘 | `icon('warn', tone='red')` | G8 | `13-cards` · `28-board` |
| E36 | 마취 칩 | `ui.sq_badge(button=true, tip=)` + `ui.elapsed` | G6 · G13 | ① 시작 · ② 진행 · ② 20분 넘음(빨강) · ③ 완료 — `14-badges` |
| E37 | 고객 줄 | `ui.customer_line` | ― | hover — `13-cards` |
| E38 | 바이탈 줄 | `ui.vital` | ― | 성별 비움(KOS 미지정) 포함 — `28-board` |
| E39 | 오더 메모 | `ui.memo` | G10 | 5줄 이하 · 넘음(잘림 + 버튼) · 펼침 — `18-memo` |
| E40 | 전체 선택 | `ui.check_all` | G11 | 없음 · 혼합 · 전체 · 꺼짐 · 동작 — `11-checkbox` |
| E41 | 시술 줄 | `ui.proc_row` | G12 | 준비중(체크 · 체크됨) · 호출(늦음) · 수락 · 진행중 · 완료 · 메뉴 열림 — `19-procs` |
| E42 | 꺼진 체크박스 | `ui.check_item(disabled=true)` | G11 | `11-checkbox` · `19-procs` |
| E43 | 시간 칸 | `ui.time_cell` | G13 | 진행 · 5분 넘음(빨강) · 완료(title) — `20-elapsed` |
| E44 | 줄 버튼 24 | `ui.btn(…, 'xs')` | ― | 시작(solid) · 종료 · 수락(Outlined Black) — `03-buttons` · `19-procs` |
| E45 | 더보기 | `.day-proc__more` + `ui.pop_trigger` | G12 | hover · 포커스 · 메뉴 열림 — `19-procs` |
| E46 | 호출 바 / [귀가 대기] | `ui.actionbar` | G14 | 숨김 · 고름([의사 호출 · N건]) · 귀가 대기 — `21-actionbar` |
| E50 | 더보기 메뉴 | `ui.popover("menu")` + `ui.menu_row` · `ui.menu_sep` | G16 | 닫힘 · 열림 · 꺼진 줄 · Esc — `07-popover` · `i2` |
| E51 | 의사 호출 창 | `ui.doctor_call_modal` | G16 · G17 | 아래 |
| E52 | 의사 아바타 | `ui.avatar` | G17 | tone 0 · 1 · 2 · 전체 호출 · ALL — `22-avatar` |
| E55 | 차트 모달(읽기) | `ui.chart_modal` | G2 | 열린 견본 · 화면 안 열기 · 서버 조각 · 줄을 누르면 깜빡임 — `24-chart` · `i5` |
| E56 | 글 칸 | `ui.textarea`(`.day-textarea`) | ― | 쓰기 · 읽기 전용 — `04-inputs` · `24-chart` |
| 수납 필요 | U9 | `ui.payment_required()` | ― | `26-payment` · `27-inbox` · `28-board` |
| (기타) | 콤보박스 목록 | `ui.combobox` | G16 | 고르기 전 · 고른 값 · 꺼짐 · 펼친 목록(선택 · 꺼진 줄) — `08-combo` |
| (기타) | E13 포커스 · E14 스크롤바 | `app.css` `:focus-visible` · `::-webkit-scrollbar` | ― | 전역 |

**안 만듦**(A4): E33 방 이름 버튼(방 옮기기) · E47 · E48 · E49 · E53 · E54가 쓰이는 곳(방 옮기기 · 연결 풀기). 확인 창 E54도 1차에는 쓰는 곳이 없어 만들지 않았다.

### 의사 호출 창 (A8 · 원천 「화면 참고」)

- 모달이다. 머리는 「의사 호출」 + 「A-룸2 · 김하나」 + X다.
- 왼쪽은 검색 → 「추천」 → **「모든 의사」**(ALL 아바타 · 「콜 잡은 원장이 집도」) → 「원장」 줄(아바타 · 이름 · 오른쪽 상태)이다.
- 오른쪽은 「선택됨」과 「호출할 시술 · N개」 + 목록이다.
- 아래 버튼은 고르기 전에는 **꺼진 「의사를 선택하세요」**, 고르면 「호출」이다(day.js).
- 모드:
  - recall: 제목 「재호출」, 기본 선택 = 처음 호출 대상.
  - accept: 제목 「수락할 원장」(시안 L1084), 「모든 의사」 줄 없음.
- 검색은 키트 medikit.js의 `data-filter-list`를 썼다.
- 원장 순서(비어 있는 원장 먼저)와 상태 글자(규칙 19)는 화면(#231)이 값을 넘겨서 정한다. 매크로는 받은 순서대로 그린다.

## A5 「키트로 올릴 후보」 (centurion medikit HTMX 키트에 없음 · DAY에 새로 만듦)

| 후보 | 매크로 · 클래스 | JS(day.js) | 메모 |
|---|---|---|---|
| 툴팁(꼬리 · 떠 있는 하나) | `tip` · `.day-tip` | `[data-tip]` | 키트 README의 「Radix 없음」 빈칸을 메운다 |
| 팝오버 + 메뉴 | `popover` · `menu_row` · `menu_sep` | `[data-day-pop]` 위치 · 바깥 클릭 · Esc · 포커스 복귀 · ↑↓ | |
| 콤보박스 목록 | `combobox` | 옵션 고르기 → hidden input | |
| 아코디언(높이 전환) | `accordion` | `[data-day-acc]` | `<details>` 대신 grid 0fr↔1fr |
| 토스트 | `toast` · `toast_oob` · `#day-toasts` | 자동 사라짐 | Notify sm |
| 체크박스 혼합 | `check_all` · `check_item` · `.ms-checkbox:indeterminate` | 그룹 동기화 | 키트 `data-check-all`은 form 이름 단위라 카드 단위를 따로 만들었다 |
| 밑줄 탭(3 크기) · 세그먼트 | `tabs` · `tab_panel` · `segment` | 고르기 · ←→ | |
| 실시간 경과 | `elapsed` · `time_cell` | `[data-day-since]` · `[data-day-late-at]` | 서버가 기준 시각을 내려준다 |
| 끌어서 순서 | `grip` · `data-day-sort*` | `day:sorted` 이벤트 | |
| 입력 지우기 X · 28 크기 | `search(clearable, size="ss")` | `[data-day-clear]` | |
| 글 칸(Textarea) | `.day-textarea` | ― | 키트에 textarea가 없다 |
| 버튼 Outlined Black · Filled Gray · 24 · 정사각 아이콘 | `btn('black'│'filled-gray', 'xs'│'icon'│'m36')` | ― | |
| 빈 상태(테두리 없음 + 버튼) | `empty_state` | ― | 키트 `ms-empty`는 표 전용 |
| 화면 안 dialog 열기 · 줄을 누르면 dialog | ― | `[data-day-open-dialog]` · `[data-day-row-open]` | |
| 응답 CSP 헤더 · `redirect`(204 + HX-Redirect) | `web.py` | ― | |
| **DAY 전용으로 둘 것(올리지 않음)** | CRM 셸 · 밀집 카드 · 사각 배지 · 시술 줄 · 액션 바 · 메모 · 의사 아바타 · 의사 호출 창 · 차트 모달 · CRM 토큰 · 고객 상태 팔레트 | | 시술 현황 도메인 모양 |

## 코디가 확인할 것

1. **로그인 카드 문구 셋은 내가 정했다**(근거 없음): 「KOS 계정으로 로그인합니다.」 · 「병원 선택」 · 「로그인할 병원을 고르세요. 다른 병원으로 바꾸려면 다시 로그인합니다.」. 빈 홈 문구 「아직 열린 화면이 없어요」도 마찬가지다.
2. **「수납 필요」 모양 · 위치는 내가 정했다**(시안에 없음 · SPEC 「위치는 디자인」).
   - 모양: 사각 배지 yellow solid(medikit `--ms-yellow` 토큰).
   - 위치: 방 카드 고객 이름 오른쪽 · 인박스 카드 머리.
3. **`/dev/kit`는 로그인 없이도 열린다**(dev 전용 개발 도구 · DB 없는 테스트를 위해). 로그인하면 hx-headers와 [로그아웃]이 붙는다. 업무 화면 규칙(「세션 없으면 /login」)은 `/`와 이후 업무 화면에 적용한다.
4. **귀가 대기 카드를 「흐리게」 그리는 투명도는 시안 값을 다시 썼다.** SPEC U-9에는 수치가 없어서, 시안이 「다른 방 선택 시」에 쓰는 0.7(`--day-dim-room`)을 가져왔다.
5. **E14 스크롤바는 시안 값을 따랐다**(thumb rgba 0.1 / 0.2 — DS 조사에 따르면 medikit base.css와 다르다).
6. **아이콘 줄 아이콘**: 시안 rail SVG의 path를 그대로 썼다. 시안의 rail 현재 메뉴 「예약」은 시안을 만들며 남은 흔적이라 따르지 않았다. 견본은 현재 = 시술로 그렸다.
7. **`Secure` 쿠키는 http 로컬에서 Chromium으로만 확인했다.** Safari로 http://127.0.0.1 을 열면 쿠키가 안 심길 수 있다(#227의 쿠키 규칙 그대로라 고치지 않았다).
8. **키트 CSS의 teal 값이 남아 있다.** `--ms-primary-600/700`은 덮지 않았다(시안 값이 없음). 지금 쓰는 곳도 없다.

## 스크린샷 (`frontend-229-shots/`)

| 묶음 | 파일 |
|---|---|
| 견본 전체 | `00-viewport` · 섹션 `01-tokens` ~ `28-board`(28장, 섹션 번호 = 목차) |
| 상호작용 | `i1-tooltip-hover` · `i2-popover-open` · `i3-call-modal-open`(서버 조각 · data-open-on-load) · `i4-call-modal-picked-filtered` · `i5-chart-modal-row-click` |
| 로그인 | `l1-login` · `l2-login-error`(가짜 이메일로 다시 찍음) · `l3-after-login-kit` · `l4-csrf-toast` · `l5-logged-out` |

## 띄워 둔 것

- `docker compose -f deploy/compose.local.yaml --env-file deploy/local.env --profile app`: api(11040) · worker · scheduler · postgres(11042) · redis(11043). **내리지 않았다**(코디 지시 · 사용자 확인용).
- worker가 데모 지점과 KOS 동기화를 돈다(평소 app 프로필과 같다).
- 내 로컬 uvicorn과 headless 브라우저는 모두 끝냈다.
