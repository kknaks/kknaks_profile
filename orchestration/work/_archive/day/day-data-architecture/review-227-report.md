# 리뷰 리포트 — day-data-architecture / code · Delivery #227 로그인 · 세션 (2026-11-06)

대상: 워크트리 `CENTURION_DAY/day-data-architecture` — #224 ~ #226 커밋(`8c85233a`) 위 미커밋 #227.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. compose 는 11042 · 11043 만 쓰고 끝나고 `down` 했다.
기준: Issue #227 contract v3 · DAY-SPEC-001(PR #909) · 발주서 · 구현 리포트 · v2/v3 계약 검수.

## 판정: WARN (FAIL 0)

A1 ~ A10 은 코드 · 테스트로 확인된다. 시스템 계정 경로와도 섞이지 않는다(`emr/kos/client.py` diff 0줄 · 직원 경로는 401 재시도 0 · 연결 설정 자격을 받지 않는다). 비밀값 누출도 없다.
머지 전에 고치기를 권하는 것은 **W1(임시 토큰 「한 번만」이 동시 요청에서 깨짐)** 하나다. 나머지는 작은 것이다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q`(DAY_REQUIRE_INFRA=1) | **265 passed / 19.7s** (구현 리포트와 같음) |
| `uv run pytest -q -m "not infra"` | **175 passed · 90 deselected / 2.7s** |
| `uv run ruff check backend scripts` | All checks passed |
| 이번 테스트 파일(전체 / DB 없이) | `test_auth_rules` 10/10 · `test_kos_staff_client` 10/10 · `test_auth_api` 23/0 |
| 비밀값 대조(`deploy/local.env` 의 키 · 테넌트 id · 시스템 이메일 · 비밀번호 ↔ 추적 · 미추적 파일 + 구현 리포트) | 0건 |
| 시스템 계정 경로 `emr/kos/client.py` diff | 0줄 |

## 계약 대조

| | 판정 | 근거 |
|---|---|---|
| A1 | 같음 | `services/auth.py:288-361` `_finish` — 한 transaction 에서 account(처음이면 `is_active=True` · `last_login_at`) · external_ref(account · staff · job_role) · job_role(이름 · 태그 · `is_default` 는 응답에 있을 때만) · staff · login_session(`csrf_token`) · external_session. 두 번째 로그인은 `_account_by_user`(`:131`) + ON CONFLICT 로 갱신만 한다. 앞 세션은 건드리지 않는다. 웹은 쿠키, 앱은 본문 `token`(`routers/api/auth.py:42-48`). 실물은 구현 리포트 표(행 수 그대로) |
| A2 | 같음(W1) | `auth.py:198-234` — 후보 안에서만, 5분 안에서만, 성공하면 지운다. 테스트 `test_auth_api.py:259-307` |
| A3 | 같음 | 비밀번호는 `staff_client.sign_in` 본문에만 실린다. 로그 · 예외 · 행에는 없다. `external_session.access_token` 은 `EncryptedText`, Redis 임시 값의 KOS 토큰은 `encrypt_value`(`auth.py:259`). 세션 토큰은 `secrets.token_urlsafe(32)`, DB 에는 `sha256` 만(`sessions.py:28-33`) · `live_unique(login_session.token_hash)` |
| A4 | 같음 | 매트릭스 줄마다 API 테스트가 있다(`test_auth_api.py:340-433` 등). 빈 입력은 `auth.py:174-176`(KOS 부르기 전). 실패한 로그인은 ⑤ 전에 끝나 행이 없다(`assert_no_session`) |
| A5 | 같음 | `expires_at = signed.token_expires_at`(`auth.py:345`). 만료가 없으면 세션을 만들지 않는다(`:244-246`). `sessions.end_session_on_kos_401`(`:90-108`) — 그 세션만 · `revoked_at` 그대로 · 조건부 UPDATE. 직원 경로 401 은 `StaffTokenRejected` 로 한 번에 실패한다(`staff_client.py:104-105 · 120-121`) |
| A6 | 같음 | `sessions.logout`(`:75-87`) — `revoked_at` 만 채우고 KOS 호출은 없다 |
| A7 | 같음 | `session.py:57-69` `writable_session` — 쿠키일 때만 CSRF 를 보고, 헤더 → urlencoded form `csrf_token` 순으로 찾는다. 비교는 `hmac.compare_digest`(`sessions.py:71`), 순서는 401 → 403. login · hospital 은 이 의존성을 쓰지 않는다. 쿠키는 HttpOnly · Secure · SameSite=Lax · Path=/ · Max-Age = expires_at(`session.py:86-97`). CORS 미들웨어가 없어 다른 출처에서 `Authorization` 을 실을 길이 없다. FastAPI JSON 본문은 `application/json` 이 아니면 거절되므로 form 으로 로그인 CSRF 를 걸 수도 없다 |
| A8 | 같음 | `connected_candidates`(`auth.py:147-165`)가 #226 `syncable_conditions` 를 재사용한다(dev = is_demo) |
| A9 | 같음 | `sessions.require_permission` · `level_allows`(edit ⊇ view) · `session.require_permission` 의존성. 테스트 전용 키로 행 없음 403 / 있음 200 |
| A10 | 같음 | `staff_client.py:59-64 · 86 · 102 · 118` — 단계마다 `kos-client-uri` 가 `<web>/auth/sign-in` · `<web>/hospital/select` · `<web>/<고른 테넌트>`(HAR · v3 N1 과 같음). 생성자는 endpoints · timeout · transport 만 받는다(`test_kos_staff_client.py:112-123` 이 시그니처까지 단언). 시간 제한 15초 |

「하지 않는 것」 침범 없음: 화면 0 · KOS 쓰기 0 · 로그아웃의 KOS 통지 0 · 본사/시스템 관리자 로그인 0 · prod 0.

### 시스템 계정 경로와 섞이지 않음

- 직원 경로는 `KosClient` 를 쓰지 않는다. 가져다 쓰는 것은 `WEB_USER_AGENT` · `KosEndpoints` · `KosError` · `_error_of` 뿐이다(`staff_client.py:30`). 토큰을 객체에 두지 않는다.
- 401 → `StaffTokenRejected` 로 바로 실패한다. 테스트가 요청 1건을 단언한다(`test_kos_staff_client.py:149-158`).
- 병원 고르기 전 sign-in · get-user-tenants 는 테넌트 없는 경로다. 테넌트는 사용자가 고른 후보의 `tenant_id` 에서만 온다.
- 단 하나 닿는 자리: `_finish` 가 연결 설정에서 `system_email` 을 읽는다(`auth.py:302-303`). KOS 로 보내지 않고 `is_system_account` 비교에만 쓴다. 다만 이 때문에 api 프로세스가 로그인마다 연결 설정 전체(시스템 비밀번호 포함)를 복호화해 메모리에 올린다 → W3.

### 누출 점검

| 자리 | 결과 |
|---|---|
| 로그 | `auth.py:360` 병원 id · 계정 id 뿐이다. 직원 경로에는 로그가 없다. httpx INFO URL 은 #226 W5 의 WARNING 상향이 같은 프로세스에 걸린다(`staff_client` 가 `client` 를 import) |
| 예외 → 응답 `detail` | `KosUnavailable(detail=f"... {exc}")`(`auth.py:186 · 243 · 282`) — `exc` 는 `HTTP <code> <className>` · `network <예외 이름>` 뿐이다. 이메일 · 토큰 · 테넌트 id 는 없다(KOS 오류 클래스 이름이 응답에 나가는 정도 — 참고) |
| 응답 | login 은 웹이면 token 이 없고(쿠키), 앱이면 token. `/me` 는 자기 이메일 |
| repr | **W2** — `NStaffSignIn.token` · `IssuedSession.token/csrf_token` · `CurrentSession.csrf_token` 이 기본 dataclass repr 에 그대로 나온다 |
| Redis | 임시 값 안의 KOS 토큰은 암호문이다. **이메일 · 이름은 평문**(5분) → 참고 |
| DB | 비밀번호 0 · KOS 토큰 평문 0(`test_비밀번호는_DB_로그에_없고_KOS_토큰은_암호문` 이 행 JSON 전체를 훑는다) |

### 기타 판정

- **동시 로그인**: `pg_advisory_xact_lock(login:<KOS 사용자 id>)`(`auth.py:306-310`)을 잡은 **뒤에** 계정을 다시 찾는다. READ COMMITTED 에서 앞 보유자의 commit 이 보이므로 계정이 둘 생기지 않는다. staff · job_role · external_ref 는 ON CONFLICT 다. 이것도 W4 와 같은 「동시성 테스트 없음」 자리다(낮음).
- **병원 경계**: staff · job_role 은 `Refs(candidate.hospital_id)` 범위다. account 는 병원에 속하지 않는 설계(SPEC-000)라 병원을 넘어 하나다. account external_ref 는 병원마다 한 줄. 세션은 병원 하나(`login_session.hospital_id`)다. 이상 없음.
- **migration 0003**: `login_session.csrf_token String NOT NULL`, 기본값 없음. 행이 있으면 실패하지만, 로그인 경로가 이번에 처음 생겨 dev · prod 모두 빈 테이블이다(docstring 에 적음). downgrade 는 drop. HEAD 테스트도 고쳤다. 이상 없음.
- 「계약에 없어 구현이 정한 것」 1 ~ 11: 받아들일 만하다. 5(행 쓰기를 ⑤ 로 미룸)는 S-6 「실패하면 행 없음」을 지키기 위한 것이고 `account_inactive` 판단 시점(① 뒤)은 그대로라 SPEC 과 충돌하지 않는다. 3(후보 밖 = 403 `no_connected_hospital`) · 6(로그인 중 KOS 401 = `kos_unavailable`)은 SPEC 개정 때 매트릭스에 한 줄씩 적어 두기를 권한다. 9(multipart form 은 헤더 필요)는 HTMX `hx-headers` 기준으로 문제 없다.

## WARN

### W1. 임시 토큰 「한 번만」이 동시 요청에서 깨진다 — `services/auth.py:207-233`
- 근거: `store.get` → KOS get-user-account(수백 ms) + ⑤ transaction → `store.delete` 순서다. 같은 `pending_token` 으로 두 요청이 거의 동시에 오면(더블 클릭 · 앱 재시도) 둘 다 `get` 을 통과해 **세션 두 개**(또는 서로 다른 병원 세션 두 개)를 만든다. 테스트는 차례로 다시 쓰는 것만 본다(`test_auth_api.py:300-303`).
- 고칠 방향: 처음에 원자적으로 꺼낸다. Redis `GETDEL`(6.2+, 로컬 compose 이미지 버전 확인)이나 Lua `get+del` 을 쓴다. 「후보 밖이면 5분 안에 다시 고를 수 있다」(구현 결정 4)를 지키려면, 검증에 실패했을 때 남은 TTL 로 되돌려 넣는다(`SET … KEEPTTL` 또는 `PEXPIRE`). 또는 같은 키에 `SET NX` 「사용 중」 표시를 둔다. 테스트: 같은 토큰으로 동시 2요청 → 세션 1개(infra · Redis).

### W2. 토큰이 dataclass repr 에 그대로 나온다 — `emr/normalized.py` `NStaffSignIn.token` · `dtos/auth.py:14-20 · 41-51`
- 근거: 브리프가 「repr 누출」을 따로 짚었다. 지금 코드에는 이 객체들을 로그로 찍는 줄이 없다. 그래도 예외 traceback(locals 를 싣는 오류 수집기 · `pytest` 실패 출력 · 디버그 로그)이나 앞으로 들어올 `logger.info("%s", issued)` 한 줄이면 KOS 토큰 · DAY 세션 토큰 · CSRF 토큰이 평문으로 나간다. #226 의 `ConnectionConfig.__repr__` 과 같은 수준으로 맞춰 두는 것이 일관된다.
- 고칠 방향: `token: str = field(repr=False)`(`NStaffSignIn` · `IssuedSession`) · `csrf_token` 도 `repr=False`(`IssuedSession` · `CurrentSession`) · `PendingLogin.pending_token` 도 같이. DB 없는 테스트 1개: `repr()` 에 토큰 값이 없는지.

### W3. 로그인 경로가 연결 설정 전체를 복호화한다(시스템 비밀번호 포함) — `services/auth.py:302-303 · 456-457`
- 근거: `session.get(CrmConnection)` 은 `EncryptedJSONB` 라 `open_api_key` · `system_email` · `system_password` 를 모두 복호화한다. 쓰는 것은 처음 만드는 직원의 `is_system_account` 비교 한 칸뿐이다. 그런데 그 칸은 #226 기준 정보 동기화가 다음 회차에 `get-user-account` id 기준으로 다시 덮는다(`sync.py` staff upsert 칸에 `is_system_account`). 계약(v3 W1)은 「연결 설정 자격을 직원 경로에 쓰지 않는다」고 했다. KOS 로 보내지 않으니 위반은 아니다. 다만 api 프로세스가 로그인마다 시스템 비밀번호를 메모리에 올릴 이유는 없다.
- 고칠 방향: 처음 만드는 직원은 `is_system_account=False` 로 두고 동기화에 맡긴다(동기화 전 몇 분의 공백). 또는 `select(CrmConnection.config["system_email"])` 처럼 그 칸만 읽고 그 칸만 복호화한다. 앞의 것이 단순하다. `test_처음_만든_직원의_시스템_계정_표시는_…` 은 그에 맞춰 바꾼다. 그 테스트의 `assert CrmVendor.KOS`(`test_auth_api.py:533`)는 늘 참이라 지운다.

### W4. 테스트 규칙(2026-11-06) — DB 가 필요 없는 매트릭스 줄이 infra API 테스트에만 있다 — `tests/day/auth/test_auth_api.py`
- 근거: `test_auth_api.py` 23개가 모두 infra 다. 그중 ② 틀린 비밀번호(`:348`) · ③ KOS 장애 중 sign-in 단계(`:361` 일부) · 로그인 중 KOS 401 의 「재시도 없음」(`:244`)은 DB 에 닿기 전에 끝나는 서비스 규칙이다. `test_auth_rules.py` 에는 ①(빈 입력)만 서비스 단위로 있다. 쓰기 순서(실패하면 행 없음) · advisory lock · ON CONFLICT · 쿠키 · CSRF 끝에서 끝까지는 infra 가 맞다.
- 고칠 방향: ② · ③(sign-in 단계) · 「sign-in 만료 없음 → kos_unavailable」(`auth.py:244-246`)을 `test_auth_rules.py` 에 가짜 `StaffAuthenticator` 로 옮긴다. `_sign_in` 은 세션을 안 쓰니 함수 단위로 바로 된다. API 쪽에는 매트릭스 대표 몇 줄만 남긴다. 급하지 않다 — 다음 손볼 때.

## 조용히 통과하는 자리

| 자리 | 왜 |
|---|---|
| `RedisPendingStore`(`auth.py:92-101`) | API 테스트는 모두 `MemoryStore`(`tests/day/auth/conftest.py:116-128`)를 쓴다. 진짜 보관소의 `ex=300` 을 지워도(영원히 남는 임시 토큰) 테스트는 초록이다. infra(Redis db 15) 1개: put → TTL ≤ 300 · delete 뒤 None |
| 임시 토큰 동시 사용 | W1 — 차례로 다시 쓰는 것만 본다 |
| 동시 첫 로그인 | advisory lock 을 지워도 지금 테스트는 통과한다(동시 요청 테스트 없음). 낮음 — 같은 사람의 동시 첫 로그인은 드물다 |
| `test_응답_없음_시간_제한_넘김은_장애`(`test_kos_staff_client.py:146`) | `"p" not in str(...).split()` — 비밀번호를 한 글자 `"p"` 로 두고 단어 단위로 비교한다. 거의 늘 참이다. 비밀번호를 긴 고유값(`pw-fake-…`)으로 바꾸고 부분 문자열로 검사한다 |
| `test_처음_만든_직원의_…`(`test_auth_api.py:533`) | `assert CrmVendor.KOS` — 늘 참인 단언(W3 와 같이 지운다) |
| A3 로그 검사 | 가짜 `StaffAuthenticator` 경로라 진짜 `KosStaffAuthenticator` + httpx 로그는 지나지 않는다. 비밀번호는 요청 본문에만 있고 httpx 는 본문을 찍지 않으므로 실해는 없다. 참고만 |

## 직원이 실물에서 만날 자리

- 병원 고르기 화면에서 두 번 누르면 세션이 두 개 생길 수 있다(W1). 쿠키는 마지막 것으로 덮인다. 앞 세션은 만료까지 남는다.
- KOS 가 내부 API 를 막으면 로그인 자체가 503 `kos_unavailable` 이다. 응답 `detail` 에 KOS 오류 이름(예: `HTTP 403 …`)이 보인다 — 화면은 `code` 로 문구를 고를 것.
- 처음 로그인한 직원은 기준 정보 동기화 전까지 `staff.is_active=true` 다(구현 결정 7). 그 사이 KOS 에서 퇴사 처리된 직원이 막 로그인하면 다음 동기화(최대 1시간) 전까지 통과한다. SPEC 의 `staff_inactive` 출처가 동기화이므로 계약 범위 안이다.
- 세션 중간에 계정 · 직원이 비활성이 되어도 이미 발급한 세션은 KOS 토큰 만료까지 유효하다(SPEC 은 로그인만 막는다). 화면 Delivery 에서 필요하면 요청마다 보는 검사를 정한다.

## 참고

- Redis 임시 값에 이메일 · 이름이 평문으로 5분 남는다. 토큰은 암호문이다. 같은 Redis 에 접근할 수 있는 쪽이면 DB 도 볼 수 있으니 실해는 낮다. 맞추려면 그 값 전체를 `encrypt_value` 한다.
- 로그인 시도 횟수 제한(무차별 대입)은 계약에 없다(KOS 가 계정 잠금을 하는지 확인 안 됨). 운영 전 정할 일.
- 쿠키 `Secure` 는 HTTPS 전제다(계약 「배포 전 확인」). 로컬 http://localhost 는 브라우저가 허용한다.
