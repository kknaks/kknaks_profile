# 리뷰 리포트 — day-data-architecture / code · Delivery #229 웹 기반 + #232 웹 로그인 (2026-11-06)

대상: 워크트리 `CENTURION_DAY/day-data-architecture` — #224 ~ #227 커밋(`fb2508e4`) 위 미커밋(#229 + 웹 로그인).
읽기 전용으로 봤다. KOS 호출은 하지 않았다. **compose 는 건드리지 않았다**(사용자 브라우저 확인 중 · 11040). 테스트는 `-m "not infra"` 만 돌렸고, infra 수치는 구현 리포트(305 passed)를 따른다.
기준: Issue #229(v2) · #232(v3) · 발주서 + 코디 우선순위 변경 · 구현 리포트 · 스크린샷 34장 · SPEC-001 「웹 화면」 절 · 레포 AGENTS.md 「웹 화면」.

## 판정: FAIL

웹 기반(#229) 쪽은 깨끗하다. 손 CSS · 인라인 스크립트 · `hx-on` · CDN 은 0이고, 키트 · htmx 는 원본과 바이트까지 같고, CSP 와 대응표도 맞다. FAIL 은 세 가지다.
- **견본에 실제 병원 이름이 박혀 있다**(F1).
- **#232 계약 두 줄이 빠졌다** — A6 JSON `client` 기본값(F2), A3 권한 없음 화면 · 화면용 오류 처리(F3).

셋 다 고치는 범위는 작다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **210 passed · 95 deselected / 3.0s**(구현 리포트 210 과 같음) |
| `uv run ruff check backend scripts` | All checks passed |
| `scripts/test.sh` | 돌리지 않음(지시) — 구현 리포트 305 passed |
| 벤더링 대조 | `medikit.css` · `medikit.js` = centurion `origin/main:docs/development/medikit-htmx-kit/` 와 **동일**. `htmx.min.js` = centurion `backend/admin/static` 과 **동일** |

### grep 전수 (`backend/day/templates/**`)

| 항목 | 결과 |
|---|---|
| `style=` 속성 · `<style>` | 0 · 0 |
| `hx-on` (템플릿 + day.js) | 0 |
| `on*=` 속성 · `javascript:` | 0 · 0 |
| `<script>` | `base.html:13-16` 의 `src` 4개뿐(htmx · sse 확장 · medikit.js · day.js) · 본문 0 · CDN 0 |
| tailwind 임의값 `x-[…]` | 0 |
| day.js `eval` · `new Function` · `innerHTML` | 0 |
| 토큰 정의(`--…:`) | `styles/app.css` 에만(110줄). 템플릿 · JS 에 0. day.js 의 `el.style.left/top/width` 는 툴팁 · 팝오버 위치 계산(CSSOM)이다. CSP `style-src 'self'` 가 막는 인라인 style 속성이 아니라 규칙 밖이다 |
| CSP | `web.py:30-34` — `script-src 'self'; style-src 'self'; frame-ancestors 'none'; form-action 'self'` 를 모든 화면 응답에 |

## FAIL

### F1. 견본에 실제 병원(고객사) 지점 이름이 박혀 있다 — `backend/day/routers/kit.py:178`
- 근거: `hospital_name="세라미크의원 명동점"`. 스크린샷 머리(`l3-after-login-kit.png` 등 견본 34장 전부)에 보이는 지점 이름이 여기서 온다. DB 에서 오는 값이 아니다. 출처는 시안 `reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` 과 실제 HAR(`har/고객상세.har`)에도 있는 **실제 운영 지점 이름**이다. 이 Delivery 들 내내 「명동점 금지」였던 바로 그 지점이다. 구현 리포트 A4 표 E04 는 「견본은 가짜 이름」이라고 적었는데 **사실과 다르다.** AGENTS.md 「가짜 계정 · 가짜 도메인을 하드코딩하지 않는다」 · reviewer 「비밀값 · 가짜 계정 · 하드코딩」 위반이다.
- 그 밖 실데이터 점검: 견본의 원장 · 고객 이름(김도윤 · 이서연 · 박지호 · 김하나 · 이두리 · 이저실 등)은 실제 HAR 에서 0건이다. 시안 목업에 있던 이름이거나 지어낸 이름이다. 시술명 · 메모도 일반 문구다. **실데이터는 병원 이름 한 곳이다.**
- 고칠 방향:
  - 로그인했으면 그 세션의 병원 이름(`sessions.me` 의 `hospital_name` — 데모 지점 이름)을, 아니면 「견본 병원」 같은 분명한 자리표시 이름을 쓴다.
  - 테스트에 「견본 응답에 `명동` 이 없다」 같은 한 줄을 둔다.
  - **오케스트레이션 폴더의 스크린샷 34장도 다시 찍는다**(저장소 밖이지만 공유되는 산출물이다).

### F2. #232 A6 미충족 — JSON `/api/auth/login` · `/hospital` 이 기본으로 웹 쿠키를 심는다 — `backend/day/schemas/auth.py:23 · 29`
- 근거: `client: Client = "web"` 이 그대로다(`schemas/` · `routers/api/` diff 0줄). 그래서 `client` 를 안 보낸 JSON 로그인은 여전히 `day_session` 쿠키를 심는다(`routers/api/auth.py:42-48`). #232 「바뀌는 것」은 「JSON `/api/auth/*` 는 앱 전용이므로 client 기본값을 app 으로 바꾸거나 칸을 없애 JSON 이 기본으로 웹 쿠키를 심지 않게 한다(#227 코드 변경)」고 했고, A6 은 「앱 경로 회귀 테스트(#227 테스트 갱신)」를 요구한다. SPEC-001 개정 ④(JSON = 앱 전용)와도 어긋난다. 구현 리포트는 이 줄을 언급하지 않는다.
- 고칠 방향: 기본값을 `"app"` 으로 바꾸거나 `client` 칸과 쿠키 분기를 없앤다(웹은 이제 화면 라우트가 쿠키를 심는다). `test_auth_api.py` 의 쿠키 단언(웹 경로)은 `test_web_login.py` 쪽으로 옮기고, JSON 은 「`client` 없이 → 본문 token · 쿠키 없음」 회귀 1개.

### F3. #232 A3 일부 미충족 — 권한 없음 화면과 화면용 `forbidden` · `csrf_failed` 처리가 없다 — `backend/day/main.py:23-27` · `routers/login.py:54`
- 근거: #232 는 「forbidden 은 권한 없음 화면, csrf_failed 는 오류 토스트 조각 — JSON 핸들러와 HTML 응답을 HX-Request · 경로로 가르는 의존성 · 핸들러를 둔다」고 했다. A3 는 「forbidden → 권한 없음 화면 · csrf_failed → 오류 토스트」를 요구한다. 구현은 다음과 같다.
  - `web_exception_handlers()` 는 `LoginRequired` 하나뿐이다.
  - `MESSAGES["forbidden"]` 문구는 정의만 있고 쓰는 화면 · 템플릿이 없다(grep 0).
  - `csrf_failed` 토스트는 `/logout` 라우트 안의 `try/except`(`login.py:160-168`)에만 있다. 같은 의존성을 쓰는 `POST /dev/kit/echo` 는 CSRF 가 틀리면 공용 `ServiceError` 핸들러의 **JSON 403** 을 돌려준다. htmx 는 4xx 를 바꿔 넣지 않으니 화면에는 **아무것도 안 보인다**(조용한 실패).
  - SPEC 대응표는 「권한 행이 없는 직무는 로그인 직후에도 이 화면」이다. 지금 `/`(빈 홈)는 권한을 보지 않는다.
- 고칠 방향: `web_exception_handlers` 에 화면 라우트용 처리를 더한다.
  - `Forbidden` → 권한 없음 페이지(로그아웃 버튼 보임 · centurion `forbidden_page` 방식).
  - `CsrfFailed` → `toast_only` 조각(HTMX 200 + `HX-Reswap: none` / 일반 403).
  - JSON(`/api/`)과 화면은 경로나 `Accept` 로 가른다.
  - `/logout` 의 개별 `try/except` 는 이 핸들러로 합친다.
  - 테스트: 권한 행이 없는 직무로 로그인 → `/` 가 권한 없음 화면 · `/dev/kit/echo` CSRF 틀림 → 토스트 조각.

## WARN

### W1. `/dev/kit` 가 로그인 없이 열린다 — `routers/kit.py:22-27`
- 판정: **지금은 받아들인다.** `APP_ENV != dev` 면 404(`dev_only` 의존성 · `test_kit.py` 가 prod 404 확인)다. 내용은 정적 견본뿐이고 DB · KOS 를 읽지 않는다. `POST /dev/kit/echo` 는 `writable_session` 이라 로그인 · CSRF 가 필요하다.
- 다만 `APP_ENV=dev` 는 로컬만이 아니라 **공유 dev 서버**(#226 · #227 의 dev = `day_dev`)도 뜻한다. dev 서버를 밖에 열기 전에는 `required_web_session` 을 걸거나 별도 env 스위치(`DAY_DEV_KIT=1`)로 끄기를 권한다. F1 을 고치면 노출되는 실데이터는 없다.

### W2. 업무 화면 의존성이 요청마다 DB 연결을 하나 더 연다 — `session.py`(`optional_web_session` · `required_web_session`)
- 근거: 두 의존성이 `get_async_session()` 을 직접 연다. `/`(`login.py:175-190`)는 `Depends(db)` 도 같이 쓰므로 요청 하나에 DB 세션이 둘이다. 지금은 화면이 적어 실해가 없다. 업무 화면이 늘면 풀 사용이 두 배가 된다.
- 고칠 방향: `Depends(db)` 를 받아 같은 세션을 쓴다(`current_session` 과 같은 모양).

## 조용히 통과하는 자리

| 자리 | 왜 |
|---|---|
| `test_web_rules.py:54` 「템플릿이 쓰는 클래스는 빌드된 CSS 에 있다」 | 클래스 **이름**이 있는지만 본다. `styles/app.css` 의 값을 바꾸고 `scripts/build-css.sh` 를 안 돌려도(이름은 그대로) 초록이다. 빌드 결과에 원본 해시를 머리 주석으로 박고 테스트가 `app.css` 해시와 비교하거나, CI 에서 빌드 후 `git diff --exit-code day.css` |
| 같은 테스트의 클래스 추출 | 매크로 안에서 문자열을 이어 만드는 클래스(`'day-btn--' ~ size` 같은 꼴)는 정규식이 못 잡을 수 있다. 실제로 이어 붙이는 곳이 있는지 한 번 확인할 것(낮음) |
| `/dev/kit/echo` CSRF 실패 | 테스트는 403 `csrf_failed` 상태만 본다. 실제 화면에는 아무것도 안 뜬다(F3) |
| 구현 리포트 E04 「견본은 가짜 이름」 | 문서와 코드가 다르다(F1) |

## 맞게 된 것 (확인)

- **CSRF**: `base.html:19` `<body hx-headers='{{ {...}|tojson }}'>` 한 곳. 로그인했을 때만 붙는다. `tojson` 이 `'` 를 `'` 로 바꿔 속성이 깨지지 않는다. 로그아웃 폼에 `csrf_token` 숨은 칸이 있다(JS 없을 때). `POST /login` · `/login/hospital` 은 CSRF 의존성을 쓰지 않는다(SPEC 미적용 목록). `/logout` 은 쓴다.
- **로그인 화면(SPEC-001 「웹 화면」)**:
  - 문구 `routers/login.py:44-60` 이 대응표 13줄 + 「로그아웃했습니다」와 **글자까지 같다**(대조함).
  - 처음 보는 코드는 문구를 지어내지 않고 KOS 장애 문구로 보인다.
  - 임시 토큰은 숨은 폼 칸(`login_card.html:10`)에만 있다. URL · 쿠키 · 로그에는 없다.
  - 실패하면 이메일은 남고 비밀번호는 빈다(`login_card.html:24 · 28`).
  - 만료 · 이미 쓴 토큰 → `/login?reason=session_expired`.
  - 이동은 일반 303 · HTMX 204 + `HX-Redirect`(`web.py:119-126`).
- **쿠키 심기 = 웹 라우트**: `login.py:96-99` `set_session_cookie`. 로그아웃은 `clear_session_cookie`. service 는 #227 그대로 부른다.
- **대응표(A4)**: SPEC-002 1차 요소 E01 ~ E57 + 「수납 필요」 → 매크로 · 견본 섹션 표가 빠짐없다. 「안 만듦」(E47 ~ E49 · E53 · E54)은 이유와 함께 적혔다.
- htmx-config `allowEval:false` · `allowScriptTags:false`. 라이선스 3개를 같이 두었다. Jinja autoescape(`.html`) 켜짐. `day_mark` 는 escape 뒤 `<mark>` 를 붙인다(`web.py:47-65` · 테스트 있음).

## 「코디가 확인할 것」 1 ~ 8 판정

| # | 항목 | 판정 |
|---|---|---|
| 1 | 로그인 카드 문구 셋 · 빈 홈 문구를 구현이 정함 | **확인 필요(사용자)** — #232 는 「문구는 표 그대로 — 새로 짓지 않는다」다. 표에 없는 카드 제목 · 설명은 짓지 말아야 할 문구에 해당하는지 애매하다. 짧고 뜻은 SPEC U-2 를 옮긴 것이라 문제 소지는 작다. 사용자 한 번 확인 |
| 2 | 「수납 필요」 모양 · 위치 | 받아들임 — SPEC 이 「위치는 디자인」. 토큰(`--ms-yellow`)만 썼다. 시안이 나오면 맞춘다 |
| 3 | `/dev/kit` 로그인 없이 열림 | W1 — 지금은 받아들임 · 공유 dev 서버 열기 전 잠글 것 |
| 4 | 귀가 대기 흐림 0.7(시안 값 재사용) | 받아들임 — `--day-dim-room` 토큰 하나로 둔다 |
| 5 | 스크롤바 시안 값 | 받아들임 — `app.css` 토큰에만 |
| 6 | 아이콘 줄 시안 path · 현재 메뉴 = 시술 | 받아들임 |
| 7 | `Secure` 쿠키를 Chromium 으로만 확인 | 받아들임(계약 · #227 쿠키 규칙). 참고: Safari 는 `http://127.0.0.1` 에서 `Secure` 쿠키를 거절할 수 있다. 로컬 확인은 Chromium 기준이라고 AGENTS 실행 줄에 한 줄 적어 두면 헷갈림이 없다 |
| 8 | 키트 teal(`--ms-primary-600/700`) 남음 | 받아들임 — 쓰는 곳 0. 시안 값이 나오면 덮는다 |

## 직원이 실물에서 만날 자리

- (F3) 권한 행이 없는 직무로 로그인해도 지금은 빈 홈이 열린다. SPEC 은 권한 없음 화면이다. 업무 화면이 붙으면 그 화면 POST 의 CSRF 실패가 아무 표시 없이 무시된다(토스트 없음).
- (F2) 앱이 `client` 를 빠뜨리면 토큰 대신 쿠키를 받아 로그인이 안 된 것처럼 보인다.
