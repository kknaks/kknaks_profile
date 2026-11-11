# 리뷰 리포트 — day-app / code · backend D1 로그인 환경 연결 (2026-11-09)

- 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app` 워크트리 미커밋 변경(HEAD 91728737 = origin/dev 기준). `app/**` 는 검수 대상 아님(읽지 않음).
  - 수정: `AGENTS.md` · `backend/common/config.py` · `backend/day/routers/api/auth.py` · `backend/day/schemas/auth.py` · `backend/tests/day/auth/conftest.py` · `deploy/local.env.example`
  - 신규: `backend/day/dtos/environments.py` · `backend/day/services/environments.py` · `backend/tests/day/auth/test_environments.py`(단위) · `backend/tests/day/auth/test_environments_api.py`(infra)
- SSOT: mediness `day-app-spec` 78f3ee59(HEAD 일치 확인) — DAY-SPEC-001 §3 「앱 환경 연결 (데모 계정)」 규칙 1~8 · 케이스 매트릭스 끝 3줄 · §4 규칙 14 · Validation, DAY-SPEC-003 §3 「세션 보관」 · 「연결 대상 검증」 · U-1, Delivery #235 `execution`(code_surface · verification · rollback · predeploy), 사용자 지시(미머지 SPEC 기준 구현 — 승인부재로 보지 않음).
- 직접 실행(이 검수에서 1회): `uv run pytest -q -m "not infra" backend/tests/day/auth backend/tests/architecture` → **115 passed, 36 deselected** · `uv run ruff check backend` → All checks passed · `ruff format --check backend` → 158 files already formatted. infra · DB · 서버 기동 · 실 env 읽기는 하지 않음(코디 몫).
- 추가 확인: scratchpad 의 일회성 probe(네트워크 없음 · `httpx.MockTransport`)로 `relay_login` 경계를 직접 찔러 봄(아래 W-1 · 참고).

## 판정: FAIL (backend 로직 자체는 FAIL 없음 — 로컬 compose 전달 누락 1건이 FAIL)

핵심 계약(판별 위치 · 행 0 · 대상 하나 · 리다이렉트 0 · 재시도 0 · 전체 60초 · 4xx 보존 · 그 밖 503 · 대상/환경 불일치 거절 · 로그 비밀값 0 · 요청 칸/헤더 무시 · 웹 무변경 · 롤백 경로)은 코드와 SPEC 이 같다. 로컬 manifest 가 새 env 를 컨테이너로 넘기지 않는 것이 유일한 FAIL 이고, 이것은 워커 allowed_paths 밖이었으므로 코디가 범위를 열어 줘야 고칠 수 있다.

## FAIL

### F-1. `deploy/compose.local.yaml` 이 새 env 셋을 컨테이너로 넘기지 않는다
- 위치: `deploy/compose.local.yaml:14-25` (`x-backend.environment: &backend-environment` — **명시 목록**. `DAY_ADMIN_EMAILS` 는 25행에 있으나 `DAY_PUBLIC_API_BASE` · `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` 없음. `env_file` 없음).
- 근거: Delivery #235 `execution.predeploy`/verification 의 로컬 day-local 통합 검증, `deploy/local.env.example:43-50` 이 이 셋을 「직접 넣는다」고 안내함, AGENTS.md 실행 명령(`--env-file deploy/local.env` 로 compose 기동). 브리프 §3 「compose/배포 코드가 그 값을 실제 앱으로 전달하는 구조는 코드구현 몫」.
- 재현: `deploy/local.env` 에 `DAY_PUBLIC_API_BASE=https://…` 를 넣고 `--profile app up` → api 컨테이너 env 에 값이 없음(`--env-file` 은 compose 보간용일 뿐, 목록에 없는 이름은 전달 안 됨) → 로컬 앱 로그인 응답에 `api_base_url` 가 영영 실리지 않는다.
- 영향: 사용자가 local.env 에 값을 넣어도 조용히 무시된다(예제 파일이 거짓 안내가 됨). DAY-SPEC-003 「환경 칸 필수」를 켠 빌드로 day-local 에 붙는 A3/A4 통합 검증이 로컬에서 불가능. 로컬에서 `APP_ENV=prod` 흉내로 데모 넘김을 보는 것도 불가능.
- 고칠 것(원 워커): 25행 아래에 `DAY_PUBLIC_API_BASE: ${DAY_PUBLIC_API_BASE:-}` · `DAY_DEMO_LOGIN_EMAILS: ${DAY_DEMO_LOGIN_EMAILS:-}` · `DAY_DEMO_API_BASE: ${DAY_DEMO_API_BASE:-}` 세 줄. (`migrate` 서비스는 `<<: *backend-environment` 로 같이 받는데, `DAY_PUBLIC_API_BASE` 가 틀리면 `get_database_settings()` 도 같은 `Settings` 라 migrate 도 실패한다 — 참고 R-3.) **이 파일은 워커 브리프 allowed_paths 밖이었다 — 코디가 범위를 열어야 한다.**
- 서버 쪽은 PASS: `deploy/compose.yaml:23-25` 는 `env_file: ./config/${DAY_DEPLOY_ENV}.env` + Key Vault 로 만든 `app.env` 전체를 받는다. `scripts/deploy/day_vm.py:45-46` 의 금지 키 · 접두어(`DAY_LOCAL_` · `DAY_SEED_` · `DAY_TEST_` · 비밀 이름)에 세 이름이 걸리지 않아 `deploy/config/<env>.env` 에 넣으면 그대로 전달된다.

## WARN

### W-1. dev 응답이 깊게 중첩된 JSON 이면 503 이 아니라 처리 안 된 500
- 위치: `backend/day/services/environments.py:207-210` — `json.loads(raw)` 는 `ValueError` 만 잡는다. 64KiB 안에서 `[` 3만 겹은 `RecursionError` 를 내고 `except _Unusable / TimeoutError / httpx.HTTPError` 어디에도 안 걸린다.
- 근거: DAY-SPEC-001 규칙 3 · 케이스 매트릭스 「모르는 응답 → 503 `environment_unavailable`」.
- 재현(probe 결과): 200 본문 `b"["*30000 + b"]"*30000` → `RecursionError` 그대로 전파. 401 본문 안에 깊은 중첩을 넣어도 같음. 라우터에는 `ServiceError` 핸들러만 있어 결과는 500 Internal Server Error(오류 계약 `{detail, code, field}` 아님).
- 영향: dev 가 깨졌거나 중간 장비가 이상한 본문을 줄 때만이라 가능성은 낮음. 그래도 「조용히 다른 실패」 자리 — 앱은 `environment_unavailable` 대신 모르는 500 을 받는다. `except (ValueError, RecursionError)` 로 `not_json` 처리 + 단위 테스트 1건이면 된다.
- 나머지 경계는 PASS(probe): 깨진 UTF-8 · gzip 헤더인데 gzip 아님(`DecodingError`) · `RemoteProtocolError` · 599 · `environment: "DEV"`(대문자) → 전부 503. 429 `{detail, code}` → 429 그대로(4xx 보존, SPEC 그대로).

### W-2. 넘김에 동시성 상한이 없다
- 위치: `backend/day/services/environments.py:171-186` (`_post` — 요청마다 새 `AsyncClient`, 상한 없음).
- 근거: AGENTS.md 「백엔드 안전 기준」 — 「timeout · 취소 · 동시성 상한을 명시한다」. timeout(60초 전체)과 취소는 있고 동시성 상한만 없다.
- 영향: 데모 이메일을 아는 쪽이 prod 로그인을 연타하면 prod 가 dev 로 요청마다 최대 60초짜리 연결을 연다(dev 는 다시 KOS 3번). prod api 는 `--workers 1` 이라 event loop 는 막히지 않지만 소켓 · dev KOS 부하가 상한 없이 늘어난다. 데모 계정은 몇 개뿐이고 일반 로그인 경로에도 상한이 없는 것으로 보여(기존 부채 여부는 이번 범위 밖) WARN 으로 둔다. 상한(예: 모듈 `asyncio.Semaphore`, 넘치면 503 `environment_unavailable`)을 둘지는 코디 판단 — SPEC 에 새 정책을 더하는 것이 아니라 AGENTS 규칙 준수 문제.

### W-3. `DAY_PUBLIC_API_BASE` 가 틀리면 기동 오류 로그에 원값(userinfo 포함)이 찍힌다
- 위치: `backend/common/config.py:161-168` (`field_validator` 안에서 `SettingsError` → pydantic 이 `ValidationError` 로 감쌈).
- 근거: 같은 파일 `SettingsError` docstring 「메시지에 URL · credential 을 넣지 않는다」(`config.py:42`).
- 재현: `Settings(day_public_api_base='https://user:s3cret@day.example.test')` → 메시지 `… [type=value_error, input_value='https://user:s3cret@day.example.test', …]`.
- 영향: 공개 주소라 보통 비밀은 아니지만, 정확히 「userinfo 거절」을 하는 칸이 거절 사유인 userinfo 를 로그에 남긴다. `model_validator(mode="after")` 에서 직접 `SettingsError` 를 던지거나 `hide_input_in_errors=True` 로 막을 수 있다.

### W-4. 서버 일반 설정에 env 이름이 없다 — prod 에서 `DAY_PUBLIC_API_BASE` 를 빠뜨리면 조용히 칸 생략
- 위치: `deploy/config/dev.env` · `deploy/config/prod.env`(세 이름 없음) · `backend/day/services/environments.py:72-74` · `backend/day/schemas/auth.py`(`exclude_none`).
- 근거: Delivery #235 `execution.code_surface` 에 「`deploy/config/*.env` · `deploy/local.env.example` (env 이름만 · 값 없음)」이 들어 있다. 워커 브리프 §3 「실제env수정금지」와 겹쳐 워커는 example 만 고쳤다. DAY-SPEC-001 「응답 칸」은 일반 로그인 `api_base_url = DAY_PUBLIC_API_BASE` 라고만 하고 비었을 때는 정하지 않았다.
- 영향: prod 에 값이 없으면 서버는 정상 기동하고 앱 로그인 응답에서 `api_base_url` 만 빠진다 → 정식 앱은 「환경 칸 필수」로 모든 일반 로그인을 거절(fail-closed라 데이터 사고는 아님, 다만 원인이 서버 로그에 안 남음). 코디 선택지: (a) `deploy/config/<env>.env` 에 빈 이름 줄을 넣어 배포 확인 항목으로 드러내기(Delivery code_surface 대로) (b) 그대로 두고 배포 체크리스트(predeploy 「dev `DAY_PUBLIC_API_BASE` = prod `DAY_DEMO_API_BASE`」)로만 관리. 서버가 prod 에서 비면 기동 실패하게 바꾸는 것은 SPEC 에 없는 정책이라 요구하지 않는다.

### W-5. 일반 앱 로그인 · `/hospital` · `/me` 의 새 칸 성공 경로는 infra 테스트로만 확인된다 (코디 실행으로 PASS — 경미)
- 위치: `backend/tests/day/auth/test_environments.py`(단위)에는 일반 계정이 **성공**하는 경우가 없다(가짜 KOS 가 늘 거절 — `RejectingKos`). `environment` · `api_base_url` 이 일반 `signed_in` · `choose_hospital` · `/hospital` · `/me` 에 실리는지, 웹 응답 칸이 그대로인지는 `test_environments_api.py` ①②③⑥ 에만 있다.
- 근거: AGENTS.md 「테스트」 — DB 가 필요 없는 것은 단위로. 다만 이 칸은 `auth.login` 이 DB 를 써야 나오므로 infra 로 두는 것 자체는 맞다.
- 영향: 검수 중 코디 통보(msg_6e5adbb3899d) — `scripts/test.sh -q` 전체 **647 passed, 1 warning**(신규 infra 6 포함, 증거 `backend-evidence/coordinator-full-pytest.txt` 끝줄 확인. 다만 그 파일은 `-q` 출력이라 테스트 이름별 결과는 없음). 그래서 현재는 확인됨. 남는 것은 「단위만 돌리는 개발 루프(`-m "not infra"`)에서 이 칸이 깨져도 모른다」는 점 하나 — 일반 계정 성공 응답 칸을 단위로 하나 두면(가짜 KOS 성공 + DB 없이 쓰기 어려우면 생략 가능) 좋다.

## PASS (SPEC 항목별 대조)

| SPEC/WP 항목 | 코드 | 판정 |
|---|---|---|
| 판별 = prod · `client=app` · 목록 이메일, 공백 · 소문자 (규칙 1) | `services/environments.py:77-81` · `common/config.py:225-228` | 같음 |
| KOS · DB 쓰기 **전에** 분기 (규칙 2) | `routers/api/auth.py:95-97` — `auth.login` 앞에서 return. `Depends(db)` 세션은 열리지만 lazy 라 쿼리 · 행 0. 단위 테스트는 DB 를 `ForbiddenDb`(만지면 AssertionError), KOS 를 호출 기록 가짜로 끼워 실제 라우터로 확인 | 같음 |
| dev 서버 · 웹 `/login` · `client=web` 비넘김 | `is_demo_login` 이 `app_env != prod` · `client != app` 이면 False. 웹 `routers/login.py` 무변경. 단위 + infra ⑥ | 같음 |
| 대상 = `DAY_DEMO_API_BASE` 정규화 origin 하나 · 받은 email/password 그대로 · `client:"app"` | `environments.py:195-202`. Authorization · Cookie 안 실음, 요청마다 새 클라이언트라 쿠키 저장 0 · dev `Set-Cookie` 앱에 전달 0 · prod 쿠키 생성 0(`response` 안 씀 — 테스트 `set-cookie` 없음 확인) | 같음 |
| 정규화: https · userinfo · non-443 · path · query · fragment(빈 `?` `#` 포함) 거절, host 소문자, 끝 `/` 동일 | `common/config.py:49-70`. 24 케이스 단위 테스트 | 같음 |
| 전체 60초 · redirect 0 · retry 0 | `asyncio.timeout(60)` 이 연결~본문 끝 전체 · `follow_redirects=False` · 1회 · `trust_env=False`. 느린 머리 · 늦게 흐르는 본문 둘 다 테스트. 3xx 5종 → 요청 1건 · 503 | 같음 |
| dev 4xx 보존 / 그 밖 503 | 4xx 이고 `{detail, code(str)}` 면 HTTP · 본문 그대로(`RelayedError.to_body`), 아니면 503. 200 이외 2xx · 5xx · 비JSON · 모르는 status · 칸 누락 · 비uuid · 64KiB 초과 → 503(예외 W-1) | 같음 |
| dev 가 실은 `environment`/`api_base_url` 불일치 → 503 | `_matches_target`(`environments.py:121-127`) — 정규화 비교라 끝 `/` · 대문자 · `:443` 은 같음 | 같음 |
| 요청 환경 헤더 · 모르는 칸으로 라우팅 변경 0 | `LoginRequest` 무변경(pydantic 기본 extra=ignore) · 판별은 설정만. 테스트(`environment`/`api_base_url` 칸 + `X-Day-Environment` 헤더) | 같음 |
| `APP_ENV` · `DB_SCHEMA` 요청마다 변경 0 | 프로세스 설정 읽기만 | 같음 |
| 비밀번호 · 토큰 · 이메일 · 주소 로그 0 (규칙 8) | 로그는 `demo login relay result=<code>` 만. `httpx`/`httpcore` 로거는 `common/logs.py:22` 에서 WARNING 이라 요청 URL 도 안 남음. DTO repr 에서 토큰 칸 제외 | 같음 |
| 롤백: 목록 유지 + `DAY_DEMO_API_BASE` 비움 → 503, prod 인증으로 안 샘 | `environments.py:195-198` — 목록만 보고 판별, 대상 None 이면 KOS · dev 호출 전 503. 단위(빈 값 · http · path) + infra ⑤ | 같음 (Delivery rollback 2번째 항목) |
| 빈 비밀번호 데모 계정 → 400 `invalid_request`, 넘김 0 | `environments.py:193-194` | 같음 (Validation) |
| 일반 앱 `signed_in`/`choose_hospital`/`/hospital` = 자기 `APP_ENV` + 자기 공개 origin, `/me` `environment` | `routers/api/auth.py:50-58 · 96-101 · 113-115 · 138` | 같음 (infra — 코디 실행 PASS) |
| 웹 응답 칸 무변경 | `client=web` 은 `target=None` + `exclude_none` → 칸 없음 | 같음 (infra ①③⑥ — 코디 실행 PASS) |
| `own_target` 이 KOS 부작용 뒤에 오류를 낼 수 있나 | `_signed_in` 은 `auth.login` 커밋 뒤에 불리지만 `normalize_origin` 은 예외를 내지 않고(None), 틀린 `DAY_PUBLIC_API_BASE` 는 기동 때 이미 거절 → 성공 후 실패 경로 없음 | 문제 없음 |
| 공통 설정 추가가 기존 웹을 깨나 | 기본값 모두 빈 문자열 · `extra="ignore"` · 다른 `Settings` 클래스 없음. 웹 라우트 · 템플릿은 `/api/auth/me` 를 쓰지 않음 · `MeOut` 생성처는 1곳 | 깨지 않음 |
| 계층 · 경계 | 라우터는 HTTP + 응답 매핑만, 외부 호출 · 검사는 service. architecture 27 통과 | 같음 |
| 테스트 더블 결속 | 단위: 실제 `auth_router` + 실제 `RelayDeps` → 실제 `httpx.AsyncClient`(redirect · timeout · stream 동작 그대로)에 `MockTransport` 만 바꿔 끼움. infra: 실제 PostgreSQL 행 수 전후 비교(`account` · `staff` · `login_session` · `external_session` · `external_ref`) — 단위 spy 로 대체하지 않음 | 의미 있음 |
| 스코프 | D2 · D3 서버 · migration · seed · 웹 화면 변경 없음. AGENTS.md 앱 문장은 #235 승인 범위 · SPEC-003 481행 뜻과 같음. 넘김을 `services/auth.py` 가 아니라 새 `services/environments.py` 에 둔 것은 브리프 「D1 전용 서비스 파일」 허용 안 | 준수 |
| 비밀 · 가짜 계정 · 하드코딩 주소 | 테스트의 `*.example.test` 만. `local.env.example` 은 빈 값 | 없음 |

## 직원이 실물에서 만날 자리

- 로컬(day-local): F-1 이 고쳐지기 전엔 local.env 에 값을 넣어도 앱 로그인에 `api_base_url` 가 안 실려, 「환경 칸 필수」 빌드는 로그인할 수 없다.
- prod 배포 때 `DAY_PUBLIC_API_BASE` 를 빠뜨리면 서버는 멀쩡히 뜨고 직원 앱 로그인만 전부 실패한다(W-4). 서버 로그에는 원인이 안 남는다.
- dev 의 `DAY_PUBLIC_API_BASE` 와 prod 의 `DAY_DEMO_API_BASE` 가 다르면(예: 다른 host) 심사관 로그인이 늘 `environment_unavailable`. 끝 `/` · 대문자 · `:443` 차이는 괜찮다.
- `environment_unavailable` 화면 문구는 아직 없음(DAY-SPEC-003 OQ-A16 — 열린 것, 결함 아님).

## 실연동 pending (구현 결함 아님 — 구분해서 기록)

- infra 6건(`test_environments_api.py`) — 코디가 day-local 로 실행, 전체 647 passed(이 리뷰어는 실행하지 않음 · 코디 증거 인용). 이것은 테스트 DB 기준의 「prod 행 0」이고 실제 prod 확인이 아니다.
- dev 서버 · prod 배포 뒤 실제 데모 넘김 · prod DB 행 0 사용자 조회 — Delivery 범위 밖(pending).
- code · integration 전체 완료를 이 리포트로 선언하지 않는다. mobile(`app/`)은 검수하지 않았다.

## 참고(기존 부채 · 판단 거리)

- R-1. `EnvironmentUnavailable` · `RelayedError` 가 `day/errors.py` 가 아니라 `services/environments.py` 에 있다(워커 보고 이슈 2). 동작 문제는 없고 정리 여부는 코디 판단.
- R-2. 넘김 로그의 `result=` 에 dev 4xx `code` 문자열이 그대로 들어간다(probe: `<script>` 도 그대로). 비밀은 아니고 dev 는 우리 서버라 낮음.
- R-3. `get_database_settings()` 도 같은 `Settings` 라 틀린 `DAY_PUBLIC_API_BASE` 는 migrate 까지 멈춘다. 「틀리면 뜨지 않는다」의 의도된 연장으로 보이며 기능 결함 아님.
- R-4. 단위 테스트 `Settings()` 호출은 프로세스 env 를 읽는다 — 셸에 `DAY_DEMO_*` 가 있으면 `test_데모_계정_목록은_공백_무시_소문자` 의 `Settings().demo_login_emails == frozenset()` 이 흔들릴 수 있다(현재 셸에선 통과).
