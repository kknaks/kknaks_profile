# #229 + 웹 로그인 fix1 — 검수(review-229-report.md) F1 ~ F3 · WARN 반영 결과 보고

- 작성: day frontend 워커 · 2026-11-06 · task_24692554d5d2
- 워크트리: 같은 워크트리 · 미커밋 그대로 · **커밋 안 함**
- compose: **내리지 않았다.** `--profile app up -d --build --wait api` 로 api 만 다시 올렸다. `/login` 은 재시작 전에도 뒤에도 200 이었다.

## 상태: done

## F1 — 견본에 실제 지점 이름

- 고친 곳:
  - `routers/kit.py` 에서 `hospital_name="세라미크의원 명동점"` 을 지웠다.
  - 머리의 병원 이름(E04)은 이제 **로그인한 세션의 병원 이름**(`sessions.me().hospital_name`)이다.
  - 아래 W1 때문에 견본은 로그인해야 열린다. 그래서 자리표시 이름은 필요 없다.
- 실데이터 전수 grep: `backend/day/**` · 템플릿 · 견본 · 테스트 · `scripts` · `deploy/*.example` 에서 `명동` · `세라미크` 는 0건이다. 남은 것은 `scripts/seed_demo_connection.py` docstring 의 「실제 병원(명동점 등) 키를 넣지 않는다」 한 줄뿐이고, 이것은 금지 문구다.
- 원장 · 고객 이름, 시술, 메모는 검수가 HAR 에서 0건으로 확인했다. 지어낸 값이다.
- 로컬 DB 의 데모 병원 이름은 「KOS 데모 지점」 이다. 스크린샷 머리에 이 이름이 보인다.
- 테스트:
  - `test_kit.py::test_견본에_실제_지점_이름이_없다` — 견본 페이지와 모달 4개 응답에 `명동` · `세라미크` 가 없다.
  - `test_web_login.py` — 실제 로그인 뒤 견본에 `명동` 이 없다.
- **스크린샷을 다시 찍었다**(`frontend-229-shots/`, 같은 이름으로 덮어씀). 데모 계정으로 로그인한 상태에서 찍었다.
  - 견본: `00` ~ `28` 29장
  - 상호작용: `i1` ~ `i5`
  - 로그인: `l1` ~ `l5` · `l2` 는 가짜 이메일로 다시 찍었다
  - 새로 1장: **`l6-forbidden-home`**(권한 없음 화면)
  - 합계 40장이다. 앞 리포트의 34장은 세는 법이 틀렸다(29 + 5 + 5 = 39 였다).

## F2 — JSON `/api/auth/*` 가 기본으로 쿠키를 심음

- `schemas/auth.py` 의 `LoginRequest.client` · `HospitalRequest.client` 기본값을 `"web"` 에서 **`"app"`** 으로 바꿨다(#232 A6 「기본값을 app 으로」).
- `client` 를 빼고 보낸 JSON 로그인은 이제 본문에 token 을 주고 쿠키를 심지 않는다.
- `client:"web"` 을 **명시할 때만** 예전대로 쿠키를 심는다. #227 의 쿠키 · CSRF 테스트(약 20개)가 이 경로를 쓴다.
- 칸을 아예 없애지 않은 까닭: 그 테스트들을 다 고쳐야 해서 범위가 커진다. 계약은 둘 중 하나를 허용한다. 웹 쿠키 단언은 이미 `test_web_login.py`(화면 라우트)에 있다.
- 테스트:
  - JSON 회귀 1개 `test_JSON_로그인은_client_없으면_앱_토큰이고_쿠키를_심지_않는다` — 본문 token 있음, 쿠키 없음, Bearer 로 `/me` 200.
  - 병원 고르기 JSON 테스트 1곳은 `client:"web"` 을 명시하게 고쳤다.

## F3 — 화면용 오류 처리

- 새 파일 `day/web_errors.py` 를 만들었다. 같은 오류를 경로로 가른다. `/api/` 로 시작하면 지금처럼 JSON `{detail, code, field}` 를 주고, 그 밖의 화면 경로는 아래처럼 처리한다.

| 오류 | 화면 경로 처리 |
|---|---|
| `unauthorized` | `/login` 으로 이동(일반 303 · HTMX 204 + HX-Redirect) |
| `session_expired` | `/login?reason=session_expired` |
| `forbidden` | **권한 없음 화면** `forbidden.html` 403 · 셸, 병원 이름, [로그아웃] 보임 · HTMX 는 조각 |
| `csrf_failed` | **토스트 조각** — HTMX 는 200 + `HX-Reswap: none`(화면 그대로), 일반 요청은 403 |

- `main.web_exception_handlers()` 가 이 처리들을 runtime 에 붙인다. 기존 `LoginRequired` 처리도 같이 붙인다.
- `/logout` 의 개별 try/except 를 없앴다. 이제 `Depends(writable_session)` 하나만 쓰고, 실패하면 위 처리를 탄다.
  - 바뀐 동작 하나: 세션이 만료된 상태로 로그아웃하면 `/login?reason=session_expired` 로 간다(예전에는 `/login`).
- **`/`(로그인 뒤 갈 곳)** 은 권한 행이 없는 직무면 `Forbidden` 을 내고 권한 없음 화면이 된다(SPEC-001 규칙 9 · 대응표).
  - **데모 계정은 권한 행이 0개다.** 그래서 브라우저에서 `/` 를 열면 권한 없음 화면이 나온다(`l6`).
  - 로그인 뒤 이동은 계약대로 dev 견본(`/dev/kit`)으로 바로 간다. 그래서 사용자 흐름(로그인 → 견본 → 로그아웃)은 그대로다.
- 테스트:
  - `tests/day/web/test_web_errors.py`(DB 없음 · 7개) — 화면 forbidden 페이지 · HX 조각, csrf 토스트(HX 200 · 일반 403), 세션 없음과 만료의 이동, `/api/` 는 JSON 그대로(오류 4가지).
  - infra: `test_권한_행이_없는_직무는_홈이_권한_없음_화면` — 403 화면에 로그아웃 버튼과 병원 이름이 보인다. 권한을 주면 견본으로 간다.
  - infra: 견본 echo 에서 CSRF 가 틀리면 토스트 조각이 온다(예전에는 JSON 403 을 단언했다).
- 하네스의 시험용 경로 `/test/write` · `/test/needs-*` 는 JSON 계약을 보는 테스트라서 `/api/test/...` 로 옮겼다(`tests/day/auth/conftest.py`).

## WARN

- **W1 `/dev/kit` 노출** → **로그인해야 열린다**(`required_web_view`). prod 는 여전히 404 이고, 로그인하지 않으면 `/login` 으로 간다(`test_kit.py`). DB 없는 견본 렌더 테스트는 세션 의존성만 견본 세션 값으로 바꿔 끼운다(`dependency_overrides`).
- **W2 요청마다 DB 세션 둘** → `session.py` 의 `optional_web_session` · `required_web_session` 을 `optional_web_view` · `required_web_view` 로 바꿨다.
  - 이 둘은 세션과 `me()`(병원 이름 · 권한)를 **DB 세션 하나**에서 읽고 `WebView` DTO(`dtos/auth.py`)를 돌려준다.
  - `/` 는 `Depends(db)` 를 더 이상 쓰지 않는다.
- **조용히 통과하던 자리 — 빌드 신선도** → `build.mjs` 가 `day.css` 첫 줄에 `source-sha256:<app.css 해시>` 를 적는다. `test_web_rules.py` 가 이 값을 지금의 `app.css` 와 비교한다. 이제 값만 바꾸고 빌드를 잊어도 실패한다.
- 이어 붙여 만드는 클래스(`'day-ic--' ~ tone` · `day-badge--` · `day-avatar--` · `day-tabs--`)는 직접 확인했다. 쓰는 값은 모두 `app.css` 에 정의돼 있다. `day-avatar--0` · `day-tabs--header` 는 기본 모양이라 클래스가 따로 없어도 된다.
- 「코디 확인」 1(로그인 카드 문구) · 7(Safari Secure 쿠키)은 사용자 확인 몫이라 바꾸지 않았다.

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **219 passed**(DB 없음 · 3.1s) |
| `scripts/test.sh -q`(compose postgres · redis 를 같이 씀, 내리지 않음) | **316 passed** |
| `uv run ruff check backend` · `ruff format --check` | 통과 |
| `scripts/build-css.sh` | `day.css 48.0KB` · source-sha256 기록 |
| api 재시작 | `/login` 전 200 → 후 200 · `/dev/kit`(로그인 안 함) → 303 `/login` |
| 브라우저(headless Chromium · 데모 계정) | 실패 문구, 이메일 유지 · 비밀번호 비움 → 로그인 → `/dev/kit`(머리 「KOS 데모 지점」) → CSRF POST 토스트 → `/` 권한 없음 403(로그아웃 버튼) → 로그아웃 → 「로그아웃했습니다」 · 쿠키 없음 |

## 바뀐 파일 (fix1)

- 새 파일: `day/web_errors.py` · `templates/forbidden.html` · `templates/partials/forbidden_page.html` · `tests/day/web/test_web_errors.py`
- 고친 파일:
  - `day/routers/kit.py` · `day/routers/login.py` · `day/session.py` · `day/dtos/auth.py` · `day/main.py` · `day/schemas/auth.py` · `day/styles/build.mjs` · `day/static/day.css`(다시 빌드) · `templates/partials/kit_page.html`
  - 테스트: `tests/day/web/test_kit.py` · `tests/day/auth/test_web_login.py` · `tests/day/auth/test_auth_api.py` · `tests/day/auth/conftest.py` · `tests/architecture/test_web_rules.py`

## 코디가 알 것

- 데모 계정(권한 0)으로 `/` 를 열면 권한 없음 화면이 나온다. 의도한 동작이다(SPEC 규칙 9).
- 앞 리포트 A4 표의 E04 「견본은 가짜 이름」 은 틀린 내용이었다. 지금은 「로그인 세션의 병원 이름」 이다.
