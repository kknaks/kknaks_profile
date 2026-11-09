# 리뷰 리포트 — day-data-architecture / doc · SPEC-001 개정 ④ 웹 화면 절 · 화면 라우트 (2026-11-06)

**대상**
- mediness 워크트리 `spec-001-login-session.md` diff(미커밋) · `log.md` 한 줄
- 지시 `planner-spec001-screen-instructions.md` · 작성 리포트 `planner-spec001-screen-report.md`

**기준**
- 원천 `erd/04-staff.md` L132 「웹 화면」(사용자 2026-11-06)
- 앞 검수 `review-delivery232-report.md` W1 ~ W5
- #227 코드 `fb2508e4`(`routers/api/auth.py` · `services/auth.py` · `session.py` · `schemas/auth.py` · `runtime/main.py`)
- centurion `admin/routers/session.py`(`reason` · `forbidden_page`)

**lint**: `python3 scripts/lint-pipeline.py --strict` → **0 error** · `products/day/` 경고 0.

지시대로 **문구 확정 여부는 판정하지 않았다**(사용자 몫). 문구는 「매트릭스의 뜻을 넘는지」만 봤다.

## 판정: WARN (가벼움 2)

- §3 · OQ-1 은 원천 새 줄대로 바뀌었다. 앱 JSON 경로 표는 그대로다.
- 화면 절 대응표는 매트릭스 13줄을 빠짐없이 덮는다(앞 검수 W4 의 셋 포함).
- 임시 토큰 안은 #227 구현과 맞다.

남은 것은 가벼운 둘이다. SPEC 이 기본값을 「제안」 표시 없이 정한 곳 하나(N1), 원천 CSRF 줄과의 동기화 하나(N2). 그리고 #227 코드가 바뀌어야 할 자리를 아래에 모았다.

## 1. §3 · OQ-1 ↔ 원천 L132

| 원천 「웹 화면」 | SPEC-001 | 판정 |
|---|---|---|
| 웹 로그인은 화면 라우트(`/login` · `/login/hospital` · 로그아웃) | §2 Placement · 「웹 화면」 화면 라우트 표(`GET/POST /login` · `POST /login/hospital` · `POST /logout`) | 같음. 로그아웃 경로 이름 `/logout` 은 원천에 없지만 원천이 「로그아웃」으로만 적어 정한 것이다 — 발명 아님 |
| 폼을 받아 오류는 HTML 조각 · 성공은 이동 | 화면 라우트 표 응답 칸 · 「이동 = 303 / HTMX 204 + HX-Redirect」(키트 README L38) | 같음 |
| `/api/auth/*` JSON 은 앱 전용 | §3 API 계약 머리 · OQ-1 「앱 전용 · 11-05 → 11-06 바뀜」 | 같음 — 경로 4개 표는 그대로 |
| 로직은 같은 service(#227) | 표 「`/api/auth/login` 과 같은 service」 등 | 같음 |
| 11-05 결정을 바꿈 | 머리말 개정 ④ · OQ-1 에 이력 | 맞다 |

## 2. 매트릭스 13줄 ↔ 화면 절 대응표

§3 매트릭스는 `invalid_request` · `invalid_credentials` · `kos_unavailable` · `account_inactive` · `no_connected_hospital` · `no_staff_account` · `mfa_not_supported` · `staff_inactive` · `session_expired`(사용 중) · `session_expired`(임시 토큰) · `unauthorized` · `forbidden` · `csrf_failed` 13줄이다. 대응표에 **13줄이 모두** 있고, 「로그아웃 성공」 한 줄이 더 있다.

| 앞 검수 W4 의 셋 | 화면 절 | 판정 |
|---|---|---|
| `csrf_failed` | 오류 토스트 · 화면 그대로 | 덮음 |
| `forbidden`(로그인 직후 포함) | 권한 없음 화면 · 로그아웃 버튼 · 「권한 행이 없는 직무는 로그인 직후에도」(규칙 9) | 덮음 — centurion admin `forbidden_page` 방식이 근거로 확인된다(`admin/main.py:37 · 58`) |
| 사용 중 `session_expired` | `/login?reason=session_expired` + 안내 | 덮음 — `?reason=` · `logged_out` 은 centurion `admin/routers/session.py:24-40` 과 같은 방식이다 |

### 문구 — 매트릭스의 뜻을 넘나 (확정 여부는 판정 안 함)

- 대부분 매트릭스 「결과」 칸의 뜻 그대로다. `mfa_not_supported` 는 §3 예시 문구 그대로다. `invalid_credentials` 의 「(KOS 계정과 같습니다)」는 U-1 「KOS 계정 그대로」에서 왔다.
- **사용자 확인 때 같이 볼 한 곳**: `kos_unavailable` 은 매트릭스 「결과」가 「DAY 쪽 문제로 안내(직원 잘못 아님)」(L162)다. 추천 문구는 「**KOS 연결**에 문제가 있어…」로 원인을 KOS 로 말한다. 뜻을 넘는 발명은 아니다(매트릭스 「경우」 칸이 KOS 장애다). 다만 매트릭스가 고른 안내 방향(DAY 쪽)과 어긋나니, 사용자가 문구를 고를 때 이 차이를 함께 보여 주면 된다.

## 3. 임시 토큰 안 ↔ #227 구현

| SPEC 「웹 화면」 | #227 코드 | 판정 |
|---|---|---|
| 서버 쪽(Redis · 5분 · 한 번 쓰면 지움) · 토큰 값만 돌려줌 | `services/auth.py:81-82` `PENDING_TTL_SECONDS = 300` · `day:auth:pending` · L97-112 GET + PTTL + DEL 한 번에(take-once) · L302 내용은 `encrypt_value` 로 암호화 | 맞음 |
| 5분이 지나거나 이미 쓰였으면 `session_expired` | L226-229 키가 없으면 `SessionExpired("hospital selection expired")` | 맞음 |
| 숨은 폼 칸 → `POST /login/hospital` 본문 | `HospitalRequest.pending_token`(`schemas/auth.py:27`) · 비면 `InvalidRequest`(L224-225) | 맞음. 숨은 칸이 비어 오면 `session_expired` 가 아니라 400 `invalid_request` 이 된다. 대응표의 `invalid_request` 줄은 「이메일 · 비밀번호 빈 값」만 적었다 — 정상 화면에선 생기지 않는 경우라 지적까지는 아니다 |

## 4. #227 코드가 바뀌어야 하는 자리 (구현 Delivery #232 v2 가 계약에 담을 것)

1. **웹 화면 라우트가 없다** — `backend/day/routers/` 에는 `api/auth.py` 만 있다. `GET/POST /login` · `POST /login/hospital` · `POST /logout` 화면 라우터(`routers/login.py` 등)와 템플릿을 새로 둔다. service(`services/auth.py` · `services/sessions.py`)는 그대로 쓴다.
2. **쿠키를 심는 자리** — 지금은 JSON 라우트가 `client=web` 이면 쿠키를 심는다(`routers/api/auth.py:42-48` `_signed_in` → `set_session_cookie`). 게다가 `LoginRequest.client` · `HospitalRequest.client` 기본값이 `"web"` 이다(`schemas/auth.py:23 · 29`).
   - 「`/api/auth/*` = 앱 전용」이 되면 쿠키 심기(`session.set_session_cookie`)는 **웹 화면 라우트로 옮긴다**.
   - JSON 쪽 `client` 는 기본값을 `app` 으로 하거나 칸을 없앤다. 그대로 두면 앱 전용 경로가 기본으로 웹 쿠키를 심는다.
3. **로그아웃** — `POST /api/auth/logout` 은 `writable_session`(CSRF) + `clear_session_cookie`(L103-110)다. 앱 전용이 되면 쿠키 지우기는 웹 `/logout` 몫이다. 웹 `/logout` 은 form `csrf_token` 칸으로 CSRF 를 넘긴다 — `session.py:57-68` 이 이미 urlencoded 폼 칸을 읽는다.
4. **CSRF 미적용 목록 주석** — `session.py:9-10` 주석은 `/api/auth/login` · `/api/auth/hospital` 만 적었다. 웹 `POST /login` · `/login/hospital` 을 더한다. 실제로는 이 라우트들이 `writable_session` 을 안 쓰면 된다.
5. **미로그인 · 만료 → 이동** — 지금 `current_session` 은 401 `ServiceError` 를 던지고, 공용 핸들러가 JSON(`{detail, code, field}`)으로 낸다(`runtime/main.py:30 · 45`). 웹 화면 라우트에는 「303 / HTMX 204 + HX-Redirect + `?reason=`」 의존성 또는 핸들러가 따로 필요하다. `forbidden` 은 권한 없음 화면, `csrf_failed` 는 오류 토스트 조각이다. JSON 핸들러와 HTML 응답을 HX-Request · 경로로 가르는 자리를 정해야 한다.

## WARN

### N1. 「입력한 이메일 유지 · 비밀번호 비움」을 제안 표시 없이 정했다
- SPEC 흐름 그림 「실패 ──▶ 오류 조각(로그인 화면 그대로 · **입력한 이메일 유지 · 비밀번호 비움**)」. 원천 · 매트릭스 · centurion 근거가 없는 화면 동작이다.
- 작성 리포트는 이것을 「사용자 확인 §3 그 밖 — 기본값」으로 올렸다. 그런데 SPEC 「아직 열린 것」에는 문구 · 숨은 폼 칸만 있고 이 항목이 없다.
- 고칠 방향: 「아직 열린 것」에 「실패 때 이메일 유지(기본값)」를 더하거나 흐름 그림에 「(기본값 · 확인 대상)」을 단다. 「로그인 뒤 갈 곳」은 지시서 · 앞 계약에 이미 있던 값이라 괜찮다.

### N2. 원천 04 「CSRF (웹)」 줄은 아직 `/api/auth/*` 만 미적용으로 적었다
- 원천 L130 「로그인 전 요청(`/api/auth/login` · `/api/auth/hospital`)은 … CSRF 를 걸지 않고」. SPEC 은 웹 화면 라우트 `POST /login` · `/login/hospital` 을 미적용 목록에 더했다.
- 「로그인 전 요청은 미적용」이라는 원천의 뜻에서 나온 확장이라 발명은 아니다. 다만 원천 표와 SPEC 이 글자 그대로는 어긋난다.
- 고칠 방향: 원천 L130 을 「로그인 전 요청(웹 `/login` · `/login/hospital` · 앱 `/api/auth/login` · `/hospital`)」으로 맞출지는 코디 판단이다(원천은 사용자 결정 기록이라 코디가 직접 다루는 파일).

## 다음

- 사용자 확인 3가지(문구 · 숨은 폼 칸 · 이메일 유지)가 닫히면 #232 v2 로 넘어간다.
  - 위 4절 ① ~ ⑤ 를 v2 의 Target Delta · phase 에 넣는다(앞 검수 W1 ~ W5 와 함께).
  - 특히 ② 쿠키 심는 자리와 `client` 기본값은 #227 코드 변경이다. 「백엔드는 라우트 · 리다이렉트만」이라는 #232 v1 문장을 고쳐야 한다.
