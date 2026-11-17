# 리뷰 리포트 — kos-signin-limit / code (2026-11-17)

대상: `CENTURION_DAY/kos-signin-limit` 미커밋 diff 전체(18 파일 수정 + 6 파일 새로) · base dev `0c401726`.
SSOT: SPEC-001 개정 ⑨ + 보충 ①~④ · §3 「KOS 동시 로그인 제한」 · §5 OQ-K* · `_RESUME.md` §2 · be-1 / fe-1 리포트.

## 판정: PASS (WARN 4 · FAIL 0)

직접 확인한 것:
- `uv run pytest -q -m "not infra"`(backend 전체 · `KOS_CLIENT_TAG` 뺀 셸) → **1015 passed, 343 deselected**
- 같은 실행을 `KOS_CLIENT_TAG=local` 셸로 한 번 더 → **1015 passed**(사용자 로컬 env 가 테스트를 깨지 않음)
- `uv run ruff check backend` → All checks passed
- infra 테스트(`test_device_choice_api.py` 4개)는 돌리지 않았다(Docker · 로컬 스택 금지) — be-1 리포트 467 passed 를 인용
- `app/` diff 0 · migration 0 · 화면 파일에 `<script` · `style="` 0

## FAIL

없음.

## WARN

### W-1. 웹 테스트의 가짜 service 가 `raising=False` — 이름이 바뀌면 조용히 통과
- `backend/tests/day/web/test_login_device.py:81` `monkeypatch.setattr(auth, name, fake, raising=False)`.
- be 쪽 `choose_device` 가 생기기 전에 넣은 것(fe-1 리포트). 지금은 `services/auth.py:417` 에 함수가 있으니
  `raising=True` 여야 한다. 지금 상태에서 service 이름이 `choose_device` 에서 바뀌어도 웹 테스트 15개는
  초록인데 실제 `/login/device` 는 `AttributeError` → 500.
- 근거: 계약 `auth.choose_device`(SPEC-001 §5 OQ-K4 · be-1 계약 표). 고칠 것 = `raising=False` 한 단어 삭제.

### W-2. 기기 목록의 DAY 로그인들이 모두 같은 줄로 보인다 (스펙대로지만 실물에서 막힐 자리)
- DAY 의 직원 로그인은 웹 · 앱 모두 **서버가** KOS 에 sign-in 한다. 그 UA 는 고정 상수
  `WEB_USER_AGENT`(macOS Chrome) + 표시이고 IP 는 서버 IP 다(`emr/kos/client.py:58` · `staff_client.py`
  `headers` · SPEC-001 §3 KOS 사실 「dev · prod 서버가 같은 IP」).
- 그래서 `device_label`(`services/auth.py` `_OS_MARKS` · `:485`)로 읽으면 DAY 로그인은 **전부
  「macOS Chrome · <서버 IP>」** — local · dev · prod 표시도 가려진다(OQ-K6 「환경 표시는 따로 안 보임」).
  직원이 가를 수 있는 건 2줄 상대 시각뿐이다.
- 코드는 스펙(U-4 · OQ-K6) 그대로라 FAIL 아님. 다만 사용자 로컬 확인 때 「어느 게 내 거냐」가 바로 나온다 —
  OQ-K6 에 「DAY 서버 로그인은 따로 표시」를 열어 두기를 권한다.

### W-3. 다른 직원이 쓰는 DAY 세션의 KOS 로그인을 끊을 수 있다 (OQ-K11 · 실물 확인 필요)
- 같은 KOS 계정을 여러 사람/기기가 DAY 로 쓰면, U-4 에서 고른 KOS 로그인이 **지금 살아 있는 DAY 웹 세션의 KOS
  토큰**일 수 있다(W-2 때문에 고르는 사람도 모른다). 해제 뒤 그 DAY 세션은 그대로 남지만, 직원 토큰을 쓰는
  KOS 쓰기가 `StaffTokenRejected`(401)로 실패한다(`staff_client.py` `KosStaffWriter.send`).
- 스펙 §3 직원 3 · OQ-K11 이 「확인 안 됨 · 실물 확인」으로 열어 둔 자리. 코드는 기존 S-4 의 2 경로 그대로라 범위 밖이지만,
  로컬 확인 시나리오에 「해제한 쪽 DAY 세션에서 KOS 쓰기」를 하나 넣어야 한다.

### W-4. 「못 읽는 UA = 원문」이면 환경 표시까지 화면에 그대로 나온다
- `services/auth.py:485` `return ua.strip()` — OS · 브라우저 둘 중 하나라도 못 읽으면 원문 전체를 라벨로 쓴다.
  원문에 ` (dev)` 같은 표시가 붙어 있으면 그대로 보인다. OQ-K6 기본값(「못 읽으면 원문」)과 「표시는 따로 안 보임」이
  부딪히는 자리 — 지금 서버 UA 는 늘 읽히므로 실제로는 사람이 쓰는 특이 브라우저에서만 생긴다. 빈 UA 면 1줄이
  「 · <IP>」로 시작한다(`login_card.html:26`). 글자를 짓지 않으려는 선택이라 기록만.

## 검토 항목별 결과

### 1. 보안 — PASS
| 확인 | 근거 |
|---|---|
| 비밀번호는 기기 선택 임시 값 안에만, 값 통째 `encrypt_value` · Redis 5분 · `take` 로 꺼내면 지움 · 되돌리지 않음 | `services/auth.py:379-` `_device_pending` · `:417-` `choose_device`(`put_back` 호출 없음). 테스트 `test_device_choice_rules.py` 「되돌리지 않음」 3개가 `put_backs == 0` 단언 |
| 이어지는 병원 고르기 임시 값에는 비밀번호 없음 | `_pending` 페이로드에 password 칸 없음 · infra 테스트가 `"password" not in payload` 단언 |
| 응답 · 화면 · 숨은 칸 · URL | 조각 숨은 칸은 `pending_token` 만(`login_card.html`) · 웹 테스트가 email/password 가 본문 · `location` · `hx-redirect` 에 없음을 단언 |
| 로그 | 앱 막힘 로그 `:231` 문구에 이메일 없음 · 기기 선택 로그는 `n=` · 해제 거절은 `status=` 만 · 시스템 계정 로그는 `hospital=` 만. caplog 단언 있음(시스템 · 웹 · 앱) |
| 예외 메시지 · repr | `post_kos` 는 `from None` + 예외 이름만 · `SignInLimitExceeded` 메시지는 고정 글자 · `_error_of` 는 `className` 만 · `PendingDeviceChoice.pending_token` `repr=False` · repr 단언 있음 |
| DB | infra 테스트가 account · login_session · external_session · staff · external_ref 전 행을 텍스트로 훑어 비밀번호 0 |
| 종류 구분 | 기기 토큰 → 병원 고르기 = `session_expired` · 되돌리지 않음(`:273`, 꺼내기 직후 검사라 `put_back` 전) · 병원 토큰(종류 칸 없는 옛 값 포함) → 기기 선택 = `session_expired` · 복호화 실패 = `session_expired`(`_load` `:318` — 전엔 500) |

### 2. 시스템 계정 자동 해제 — PASS
- 막혔을 때만: `client.py:324` — `is_sign_in_limit` 일 때만 `_revoke_oldest_own`. 테스트 「평소에는 목록을 보지 않는다」(force 재발급 포함).
- 같은 UA 글자까지: `:364` `r.user_agent == self.endpoints.user_agent` · 사람(표시 없음) · 다른 환경(`prod`) 행이 더 오래돼도 안 건드림 — 테스트가 섞인 목록으로 `revoked == ["own-old"]` 단언.
- 가장 오래된 1개 · 시각 없으면 가장 늦은 것으로: `_oldest` `:219`. 재시도 1회 · 또 막히면 401 실패(테스트).
- 태그 없으면 목록도 안 부르고 경고 + 실패(테스트). 해제 4xx = 로그 + 재시도 없음 + 실패(테스트). 목록 5xx = 실패(테스트).
- 동시성: 해제 · 재시도가 `_token_lock` 안(`internal_token`)이라 같은 클라이언트 안 중복은 없다. 병원별 어댑터 · 프로세스끼리는 잠금이 따로 — 같은 「가장 오래된 하나」를 둘이 고르면 두 번째가 4xx → 실패 · 다음 회차. 서로 끊는 왕복은 호출당 해제 1 · 재시도 1 로 묶여 무한 반복 없음(SPEC §3 시스템 7 · 8 그대로 · 남는 위험으로 기록됨).
- 해제 대상 목록은 **시스템 계정 자격**으로 받으므로 다른 직원 계정의 로그인은 원천적으로 대상이 아니다. 단 직원이 시스템 계정 이메일로 DAY 에 로그인한 세션은 같은 UA 라 대상이 될 수 있다(OQ-K2 대안 열에 기록됨).

### 3. 판정 — PASS
- `is_sign_in_limit` `client.py:152`: 401 + JSON dict + `message == "SignInLimitExceeded"` 일 때만. JSON 아님 · 다른 `message` · 다른 상태 → 아님.
- 직원 경로 `staff_client.py:122` 가 400/401 검사 **앞**에서 갈라 `SignInLimitExceeded`(→ `StaffCredentialsRejected` 하위라, 따로 안 다루는 곳은 지금처럼 자격 거절).
- 테스트: 틀린 비밀번호 본문(`InvalidPassword`) · 평문 401 본문 「SignInLimitExceeded」 둘 다 기기 제한 아님 단언.

### 4. 앱 — PASS
- `routers/api/auth.py:102` `device_choice=False` → service `:228-231` 가 `InvalidCredentials("email or password rejected")` — 틀린 비밀번호와 **같은 detail · 같은 code**. infra 테스트가 두 응답 JSON 이 같음을 단언 · 목록 · 임시 토큰 · 행 없음.
- `:103` `PendingDeviceChoice` 방어 가지는 도달 불가(`pragma: no cover`) — 와도 같은 401.
- 데모 넘김(`services/environments.py`) 변경 없음 — dev 가 401 `invalid_credentials` 를 주면 prod 가 그대로 넘김(`_LOGGED_CLIENT_CODES`). 앱 응답 모양 변화 0 · `app/` diff 0.
- `/api/auth/hospital` 에 기기 토큰이 오면 401 `session_expired`(전엔 `candidates` KeyError 500 가능) — 개선.

### 5. 웹 — PASS
- U-4 글자 6종 스펙 표와 한 글자씩 같음(제목 · 안내 2줄 · 「n분 전」 · 「방금 전」 · 「계속하기」) · `test_screen_copy.py` 근거 표에 추가 · 「처음으로」 없음(테스트 단언).
- 라디오 하나만 · 첫 항목 `checked` · KOS 순서 그대로(OQ-K9) · 60분 넘어도 「n분 전」(OQ-K5) · 시각 None 이면 2줄 생략(지어내지 않음).
- `/login/device` 갈래: `IssuedSession` → 쿠키 + 이동 · `PendingLogin` → 병원 고르기 조각 · 다시 막힘 → 새 토큰 조각 · `SessionExpired` → `/login?reason=session_expired`(HTMX 204 `HX-Redirect` / 303) · 그 밖 `ServiceError` → 오류 카드. 전부 테스트 있음.
- CSRF: 스펙 SPEC-001 「화면 라우트」 아래 줄 · §3 「CSRF (웹)」 미적용 목록에 `/login/device` 가 있다 — 로그인 전 요청이라 **걸지 않는 것이 스펙**. 라우트에 csrf 의존성 없음(`login.py:200`) = 스펙과 같음. Jinja2 autoescape 켜짐(Starlette 기본)이라 KOS 가 준 UA · IP · id 를 그려도 HTML 주입 없음.
- 손 CSS: `styles/app.css` 에 medikit 토큰 변수만 쓴 7줄 + `build-css.sh` 산출 `day.css`. 인라인 스크립트 0.

### 6. UA 표시 — PASS
- 공용 한 곳 `KosEndpoints.user_agent`(`client.py`) → 시스템 계정 `internal_headers` · 직원 로그인 `headers` · 직원 쓰기 `KosStaffWriter.send` · 목록/해제 `active_limit_headers` 모두 이것. 테스트 「세 곳 모두 표시 UA」가 전 요청 UA 를 단언.
- 비면 지금 UA 그대로(테스트) · 앞뒤 공백 제거.
- env 전달: `KosEndpoints`(pydantic BaseSettings)가 `KOS_CLIENT_TAG` 를 읽음 · `factory.py` 세 곳 모두 `KosEndpoints()` · `compose.local.yaml` 이 `${KOS_CLIENT_TAG:-}` 로 api · worker · scheduler 공통 앵커에 넘김 · 서버 `compose.yaml` 은 `env_file` 통째라 `deploy/config/<env>.env` 한 줄이면 됨 · `day_vm.py` 비밀 키 목록에 없어 배포 스크립트가 거부하지 않음.
- `local.env.example` 에 `KOS_CLIENT_TAG=local`. `deploy/config/{dev,prod}.env` 는 배포 PR 몫(OQ-K15) — 이번 diff 에 없음이 맞다.

### 7. 테스트 — PASS (W-1 제외)
- 위 1~6 의 규칙이 모두 **DB 없는** 단위 테스트(`test_kos_signin_limit.py` 16 · `test_device_choice_rules.py` 25 · `test_login_device.py` 15)로 단언되고, DB 가 보장하는 것(비밀번호가 DB 에 없음 · 세션 1행 · 진짜 Redis 한 번만)만 infra 4개 — AGENTS.md 「테스트」 2026-11-06 규칙과 맞다.
- 가짜는 KOS 경계(httpx MockTransport · `StaffAuthenticator` 하위)와 보관소뿐 — 도메인 규칙은 진짜 `services.auth`.
- 고정본 `kos_active_sign_ins.json` · `kos_sign_in_limit.json` 값은 가짜(IP 192.0.2.x · `example.invalid`).

## 조용히 통과하는 자리

1. **W-1** `raising=False` — 위.
2. `test_kos_client.py` · `test_kos_staff_client.py` 가 엔드포인트에 `kos_client_tag=""` 를 고정 — 셸 env 에 기대지 않게 한 것으로 맞다. 표시 UA 경로는 새 파일이 따로 단언하므로 빈 곳 아님.
3. 시스템 계정 자동 해제를 **`call()` 의 401 → force 재발급** 경로로 탄 테스트는 없다(직접 `internal_token()` 만). 같은 함수라 위험은 낮다 — 기록만.
4. infra 테스트는 이번 리뷰에서 돌리지 않았다(be-1 리포트 467 passed 인용).

## 직원이 실물에서 만날 자리 (사용자 로컬 확인)

1. **`KOS_CLIENT_TAG=local` 줄이 쓰는 env 파일에 있어야** 시스템 계정 자동 해제가 켜진다. 확인: `/Users/kknaks/git/CENTURION_DAY/deploy/local.env` 에는 이미 있음(키 이름만 grep) · 이 워크트리 `deploy/local.env` 는 파일 자체가 없음 — 워크트리에서 compose 를 띄우면 `--env-file` 을 메인 쪽으로 주거나 복사해야 한다. 없으면 worker 로그에 `KOS_CLIENT_TAG empty, no auto revoke` 경고 + 동기화 실패(지금과 같음) · 직원 UA 는 표시 없이 나간다.
2. 기기 목록의 DAY 로그인은 전부 「macOS Chrome · <서버 IP>」 — 고를 근거는 시각뿐(W-2).
3. 해제한 KOS 로그인이 다른 DAY 세션 것이면 그 세션의 KOS 쓰기가 401(W-3 · OQ-K11 실물 확인).
4. [계속하기] 뒤 최장 약 60초 — 버튼 `day-busy` 말고 진행 표시 없음(fe-1 리포트).
5. 5분 넘기고 [계속하기] → `/login` 안내 「로그인 시간이 끝났습니다…」로 처음부터.
6. 로컬 개발자 둘이 같은 `local` 표시 · 같은 시스템 계정이면 서로의 로그인을 끊는 왕복이 생길 수 있다(SPEC §3 시스템 8 — 로그로 확인).

## 참고(기존 부채 · 사소)

- `staff_client.py:4` 모듈 docstring 이 아직 「재사용하는 것은 `WEB_USER_AGENT`」 — 지금은 `KosEndpoints.user_agent`. 문서 한 줄.
- 계층 규칙: router 가 DB 를 안 만짐 · repository 층 없음 · 업체 차이는 `emr/kos/` 안(`StaffAuthenticator` 기본 구현은 미지원 = `EmrError`, 조용히 건너뛰지 않음) · `day.public` 변화 없음 · 같은 파일 이름 규칙 — 전부 지켜짐.
- `stg` 에서 복사한 코드 없음.
