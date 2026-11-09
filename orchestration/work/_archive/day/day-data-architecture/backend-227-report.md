# Delivery #227 로그인 · 세션 (DAY-SPEC-001 · contract v3) 결과 보고

## 상태: done (커밋 안 함 · KOS 쓰기 0 · 화면 없음)

워크트리 `CENTURION_DAY/day-data-architecture` · #226 커밋(`8c85233a`) 위 미커밋.

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **175 passed · 90 deselected** (#226 뒤 155 → +20) |
| `scripts/test.sh -q`(compose postgres · redis, `DAY_REQUIRE_INFRA=1`) | **265 passed** (#226 뒤 222 → +43) |
| `uv run ruff check backend scripts` | All checks passed |
| 비밀값 대조(`deploy/local.env` 의 비밀번호 · 이메일 · 테넌트 id · 키 ↔ 추적 · 미추적 파일 전부) | 0건 |

새 테스트: DB 없이 20(`test_kos_staff_client.py` 10 · `tests/day/auth/test_auth_rules.py` 10) · infra 23(`tests/day/auth/test_auth_api.py`).
#225 테스트 2곳(`test_constraints` · `test_encryption`)은 `LoginSession` 을 만들 때 새 필수 칸 `csrf_token` 을 넣게 고쳤다.

### 실물 1회 (로컬 compose · `day_dev` · 데모 지점 시스템 계정 = 유일한 데모 로그인 계정)

migrate 가 `0003_login_session_csrf` 를 적용한 뒤 api(11040)에 curl. 값(토큰 · 쿠키 · 이메일)은 파일에만 두고 지웠다.

| # | 요청 | 결과 |
|---|---|---|
| 1 | `POST /api/auth/login`(web) | **200** `signed_in` — 본문에 token 없음, `Set-Cookie: day_session` 에 HttpOnly · Secure · SameSite=Lax · Max-Age · Path=/ |
| 2 | `GET /api/auth/me`(쿠키) | **200** — account · hospital · staff · job_role(태그 7개) · permissions(0) · expires_at |
| 3 | `POST /api/auth/login`(app, 같은 계정 두 번째) | **200** `signed_in` + 본문 token |
| 4 | `GET /me`(Bearer) | **200** |
| 5 | `GET /me`(첫 세션 쿠키) | **200** — 앞 세션 그대로 |
| 6 | `POST /logout`(쿠키 · CSRF 없음) | **403 `csrf_failed`** |
| 7 | `POST /logout`(쿠키 + `X-CSRF-Token`) | **200** |
| 8 | `GET /me`(로그아웃한 쿠키) | **401 `unauthorized`** |
| 9 | `GET /me`(Bearer — 다른 세션) | **200** |
| 10 | `POST /login`(빈 이메일) | **400 `invalid_request`** |

행 건수(`day_dev`, 전 → 후): account 0 → **1**(is_active · last_login_at 채움 1) · staff 80 → **80**(중복 없음 · 동기화가 만든 행에 account 연결 1) ·
job_role 15 → **15** · external_ref account 0 → **1** · staff 80 → 80 · job_role 15 → 15 · login_session 0 → **2**(csrf_token 2 · revoked 1) ·
external_session 0 → **2**(access_token `enc:` 2 · `login_session.expires_at = token_expires_at` 2).
api 로그: 비밀번호 · 이메일 · 테넌트 id · 쿠키 · Bearer 값 0건, error/traceback 0건. 끝나고 `down`.

## 완료 조건 대조

| | 증거 |
|---|---|
| A1 | 실물 위 표. 테스트 `test_데모_지점_로그인_한_병원이면_바로_세션과_행들`(쿠키 플래그 · 6개 테이블 · external_ref 3종) · `test_두_번째_로그인은_갱신만_직무는_KOS_값_앞_세션은_그대로`(행 수 그대로 · last_login_at 갱신 · KOS 에서 바뀐 직무 이름 · 태그 반영 · 앞 세션 200) · `test_앱은_Bearer_토큰_쿠키는_없다` |
| A2 | `test_연결_병원이_여럿이면_후보와_임시_토큰_고르면_세션`(후보 2 · 세션 0 · 후보 밖 403 `no_connected_hospital` · 고르면 세션 · 한 번 쓴 임시 토큰 다시 401) · `test_임시_토큰_5분이_지나면_session_expired` |
| A3 | `test_비밀번호는_DB_로그에_없고_KOS_토큰은_암호문` — 로그 붙잡기(DEBUG · 실패 로그인 포함)와 account · login_session · external_session · staff · external_ref 행 JSON 전체에 비밀번호 0, 직원 KOS 토큰 평문 0, `access_token` 은 `enc:`. `token_hash = sha256(token) ≠ token`(A1 테스트 · 규칙 테스트) |
| A4 | 줄마다: ① `test_빈_입력은_400_KOS_안_부름`(+ 서비스 단위 `test_빈_이메일_비밀번호는_KOS_를_부르지_않고_invalid_request`) ② `test_틀린_비밀번호_401_아무_행도_없음` ③ `test_KOS_장애는_503`(403 Unsupported · 응답 없음 · 시간 초과 × sign-in · get-user-account 단계) + client 단 `test_틀린_비밀번호는_거절_KOS_403_은_장애` · `test_응답_없음_시간_제한_넘김은_장애` ④ `test_막힌_DAY_계정은_account_inactive` ⑤⑥⑦ `test_연결된_병원_없음_직원_계정_없음_2단계_인증` ⑧ `test_동기화가_끈_직원은_staff_inactive` ⑨ `test_세션_만료가_지나면_session_expired` ⑩ `test_세션_없음_틀린_토큰은_unauthorized` · 로그아웃 뒤 ⑪ A9 ⑫ A7. 실패 케이스마다 `assert_no_session`(login_session 0 · 쿠키 없음). 코드 · HTTP 표는 `test_오류_코드는_매트릭스_그대로` |
| A5 | `login_session.expires_at = external_session.token_expires_at`(A1 테스트 · 실물 2/2). `sessions.end_session_on_kos_401` — `test_KOS_401_로_세션_끝내기는_그_세션만_expires_at_을_당긴다`(expires_at=지금 · revoked_at 비어 있음 · 두 번째 호출 False · 그 세션 401 `session_expired` · 같은 계정 다른 세션 200). 로그인 중 KOS 401: `test_로그인_중_KOS_401_은_재시도_없이_실패`(호출 = sign_in · user_tenants 한 번씩) + client 단 `test_직원_토큰_401_은_다시_sign_in_하지_않고_한_번에_실패`(요청 1건) |
| A6 | `test_로그아웃_뒤는_unauthorized_KOS_안_부름`(revoked_at 채움 · KOS 호출 수 그대로 · 뒤 401 `unauthorized`) · 실물 7 · 8 |
| A7 | `test_쿠키_쓰기_요청은_CSRF_필요_Bearer_와_로그인_전은_없음`(헤더 없음 · 틀림 403 `csrf_failed` · 맞음 200 · form `csrf_token` 200 · Bearer 200 · 세션 없으면 401 먼저) · 로그인 · 병원 고르기는 CSRF 의존성을 쓰지 않음 · 쿠키 플래그(A1) · 실물 6 |
| A8 | `test_dev_서버_후보는_데모_연결만`(데모 + 실제 연결 → 데모 하나로 바로 세션 · 실제만 → 403 `no_connected_hospital`) |
| A9 | `test_me_와_권한_검사` — /me 계정 · 병원 · 직원 · 직무 · 권한, 테스트 전용 키 `test.only_view`: 행 없음 403 `forbidden` · view 행 → view 200 · edit 요구 403 · /me 권한 목록에 나타남. 단위 `test_edit_은_view_를_포함한다` |
| A10 | `test_세_단계_모두_브라우저_헤더와_단계별_kos_client_uri`(UA · Origin · kos-client-uri · Bearer · 경로) · `test_직원_경로는_연결_설정_자격을_받지_않는다_시간_제한_15초`(생성자 인자 = endpoints · timeout · transport 뿐 · httpx timeout 15) |

## 새 경로 / 재사용 표

| 무엇 | 어디 | 새 · 재사용 |
|---|---|---|
| 직원 sign-in | `emr/kos/staff_client.py` `KosStaffAuthenticator.sign_in` | **새** — 직원 이메일 · 비밀번호, 400/401 → 거절 |
| get-user-tenants | `staff_client.user_tenants` | **새** — 직원 토큰 · 테넌트 없는 경로 |
| get-user-account(직원 토큰) | `staff_client.user_account` | **새** — 고른 테넌트 · mfaMethods · role |
| 401 처리 | 직원 경로는 `StaffTokenRejected` 로 바로 실패 · 세션 쪽은 `services/sessions.end_session_on_kos_401` | **새** — 재-sign-in · 재시도 없음 |
| 브라우저 헤더 값 | `client.WEB_USER_AGENT` | 재사용(값만 — 헤더 조립은 새 `headers(client_uri, token)`) |
| 주소 | `client.KosEndpoints`(`KOS_*_BASE` env) | 재사용 |
| 오류 모양 | `client.KosError` · `_error_of` | 재사용 |
| 요청 함수 | `KosClient._post` 는 그 객체의 httpx 에 묶여 있어 **같은 모양의 `_post` 를 새로** 뒀다(네트워크 오류 → `KosError("network …")`) | 모양만 재사용 |
| 시간 제한 | `common.config.emr_http_timeout_seconds`(15초) · `factory.build_staff_authenticator` | 재사용 |
| `KosClient.call()` 401 재시도 · `internal_token()` 시스템 계정 자격 · `credentials.tenant_id` | — | **쓰지 않음**(직원 경로 생성자가 받지도 않는다) |
| 암호화 | `common.crypto`(`external_session.access_token` = `EncryptedText` · 임시 토큰 Redis 값 = `encrypt_value`) | 재사용 |
| external_ref upsert | `emr.sync.Refs.link`(staff · job_role) · account 는 같은 ON CONFLICT 로 직접(계정 id 를 넘겨야 해서) | 재사용 |
| 동기화 후보 조건 | `services/crm_connections.syncable_conditions`(dev = is_demo · 연결 · 병원 살아 있음) | 재사용 |

## `kos-client-uri` — HAR 대조

로그인 HAR(`reference/2026-10-12-cc-prototype/로그인.har`)에서 경로 · 칸 이름 · 헤더 모양만 봤다(값 옮기지 않음).

| 요청 | HAR 의 `kos-client-uri` | 구현 | Origin |
|---|---|---|---|
| `common/v1/user/commands/sign-in` | `<web>/auth/sign-in` | 같음 | `<web>` 같음 |
| `common/v1/tenant/queries/get-user-tenants` | `<web>/hospital/select` | 같음 | 같음 |
| `tenants/<t>/v1/account/queries/get-user-account` | `<web>/<tenant>` | 같음(고른 테넌트) | 같음 |

- 브리프 · v3 검수 N1 · SPEC-001 규칙 10 과 일치한다.
- HAR 은 `Authorization` 헤더를 지워 둔 상태(크롬 내보내기)라 get-user-tenants · get-user-account 의 인증 방식은 HAR 로 못 본다.
  데모 지점 조회(토큰 받기 · 조회만)로 `Bearer <sign-in 토큰>` 이 두 요청 모두 200 인 것을 확인했다.
- 응답 칸(HAR · 데모 동일): sign-in `{data{id,email,name,tenantIds,token}, tokenExpiredDateTimeUtc}` · get-user-tenants
  `data[]{id,hospitalId,hospitalName,…}` · get-user-account `{data{id,name,email,role{id,name,roleTags[int]},mfaMethods[]}}`.
  `role.isDefault` 는 HAR 에만 있고 데모 응답에는 없다 → 없으면 None(있던 값을 덮지 않음).
- 데모에서 본 것: 틀린 비밀번호 sign-in = 401(`InvalidRequestException`) → `invalid_credentials`.
  **이상: 엉터리 Bearer 로 get-user-tenants 를 불러도 200** 이었다(본문은 보지 않음) — 로그인 경로는 방금 받은 토큰만 쓰므로 영향 없음.

## 계약에 없어 구현이 정한 것 (코디 확인)

1. **웹 · 앱 구분 = 요청 본문 `client`**(`web` 기본 — `day_session` 쿠키만, 본문에 token 없음 / `app` — 본문 `token` 을 Bearer 로, 쿠키 없음).
   SPEC 은 「웹 = 쿠키 · 앱 = Bearer」만 정했다. 두 응답 모두 `csrf_token` · `expires_at` 을 준다(웹 화면 `hx-headers` 용).
2. 응답 모양: login → `{"status":"signed_in", expires_at, csrf_token[, token]}` 또는 `{"status":"choose_hospital", pending_token, expires_in_seconds:300, hospitals[{id,name}]}` ·
   logout → `{"status":"signed_out"}` · 오류 → 공용 `{detail, code, field}`.
3. **후보 밖 병원 고르기 = 403 `no_connected_hospital`**(매트릭스에 줄 없음 — 「연결된 병원 아님」으로 읽음).
4. 임시 토큰 = Redis(`day:auth:pending:<토큰 해시>` · EX 300 · KOS 토큰은 암호문). 성공하면 지워 한 번만 쓴다. 실패(후보 밖 등)하면 5분 안에 다시 고를 수 있다.
5. **행을 쓰는 시점**: S-1 은 sign-in 직후 계정을 만든다고 적지만, 실패한 로그인에 행이 남지 않게(S-6 · A4) 모든 쓰기를
   get-user-account 뒤 한 transaction 으로 미뤘다. `account_inactive` 판단은 sign-in 직후(읽기) 그대로. 같은 KOS 사용자 동시 첫 로그인은
   advisory lock(`login:<사용자 id>`)으로 계정이 둘 생기지 않게.
6. 로그인 중 KOS 401(get-user-tenants · get-user-account)과 응답 모양 오류는 `kos_unavailable`(매트릭스 「KOS 장애」로 읽음). sign-in 400 도 `invalid_credentials`.
7. 처음 만드는 직원(동기화 전): `is_active = true`(KOS 가 그 테넌트 직원 계정을 돌려줌 — 동기화가 다음 회차에 덮음) ·
   `is_system_account` = 연결 설정 `system_email` 과 같은 이메일일 때만. 이미 있는 직원의 두 칸은 동기화 몫이라 로그인이 건드리지 않는다.
8. KOS 가 토큰 만료(`tokenExpiredDateTimeUtc`)를 안 주면 세션을 만들지 않고 `kos_unavailable`(만료를 지어내지 않음).
9. form 의 `csrf_token` 은 `application/x-www-form-urlencoded` 만 읽는다 — `python-multipart` 가 없고 `pyproject.toml` 이 allowed_paths 밖이다.
   multipart form 은 헤더 `X-CSRF-Token` 이 있어야 통과(HTMX 는 `hx-headers` 라 해당 없음).
10. 웹 라우터 위치: JSON `/api/auth/*` 는 `routers/api/auth.py`, 쿠키 · Bearer · CSRF 의존성은 `day/session.py`. runtime 은 `day.public.api_routers()` 만 부른다.
11. `login_session.last_used_at` 은 발급 때만 채운다(요청마다 갱신하지 않음).

## 파일

새: `backend/day/errors.py` · `dtos/auth.py` · `schemas/auth.py` · `session.py` · `routers/api/auth.py` · `services/auth.py` · `services/sessions.py` ·
`emr/kos/staff_client.py` · `migrations/versions/20261106_0003_login_session_csrf.py` · 테스트(`tests/day/auth/` · `tests/day/emr/test_kos_staff_client.py` · fixture 3).
고침: `emr/base.py`(StaffAuthenticator · 오류 3) · `emr/normalized.py`(로그인 형식 4) · `emr/kos/mapper.py`(로그인 응답 3) · `emr/factory.py` ·
`models/staff.py`(`csrf_token`) · `services/crm_connections.py`(`syncable_conditions`) · `public.py`(`api_routers`) · `runtime/main.py` · `AGENTS.md`(로그인 curl 한 줄) ·
테스트 4(컬럼 스냅샷 · alembic HEAD · LoginSession 두 곳). 시스템 계정 경로(`emr/kos/client.py`)는 고치지 않았다.

## 남은 것

- 화면(로그인 · 병원 고르기 · `base.html` `hx-headers`) — 화면 Delivery.
- 직원 토큰으로 KOS 쓰기 · `end_session_on_kos_401` 을 부르는 쪽 — 첫 실제 쓰기 Delivery.
- `permission_key` 목록 — SPEC-000 OQ-04-2.
- 실물은 연결 병원 1개(자동)만 — 여러 병원 후보 경로는 테스트로만 확인(데모 계정 테넌트 1개).
- SPEC-000 · 001 이 PR #909 미머지(spec-baseline pending) — 머지 뒤 계약 재결속.
