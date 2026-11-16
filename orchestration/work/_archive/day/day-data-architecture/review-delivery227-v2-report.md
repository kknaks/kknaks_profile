# 리뷰 리포트 — day-data-architecture / doc · Delivery #227 로그인 contract v2 (2026-11-06)

대상
- GitHub Issue MediSolveAIDev/CENTURION_DAY#227 본문(2026-11-06T01:27Z 갱신본)
- `delivery/v2-login.json`(contract v2) · `v2-login.v2.plan.json` · `v2-login.v2.apply.json`
- 작성 리포트 `planner-delivery227-v2-report.md`

기준
- **S1** = DAY-SPEC-001(`spec-001-login-session.md` — 줄 번호는 지금 파일)
- 원천 `erd/04-staff.md` 「로그인 · 세션 계약」
- **코드** = PR #228 브랜치(`CENTURION_DAY/day-data-architecture` HEAD `8c85233a`)

## 판정: WARN

- FAIL 은 없다. SPEC-001 에 없는 정책은 계약에 들어가지 않았다. API 4경로 · 오류 11줄 · 규칙 1 ~ 13 · 상태도 · 만료 규칙이 모두 Target Delta 에 대응된다.
- 원천 04 「로그인 · 세션 계약」 표와도 어긋나는 곳이 없다.
- Non-Goals 는 전부 S1 의 규칙 · OQ 에서 나왔다. 예외는 「prod · DB_SCHEMA=day_dev」 하나인데, 이것은 Delivery 운영 범위라 문제없다.
- 위험 L3 · 승인 대기 상태도 맞다.

WARN 은 7건이다.
- Acceptance 중 세 개(A5 후반 · A7 · A9 후반)가 이 Delivery 안에서 확인할 길이 없다.
- 「이미 있음 — 재사용」 중 「401 처리」는 실제 코드와 반대로 동작한다.
- S1 에 빈칸이 두 곳(CSRF 실패 · 빈 입력) 있어 구현자가 고르게 된다.

## WARN

### W1. 「재사용 — 401 처리」가 S1 규칙 8 과 반대로 동작한다
- 계약 Target Delta 마지막 줄 「KOS client(… 내부 sign-in · get-user-account · 브라우저 헤더 · **401 처리**)」 재사용.
- 코드: `backend/day/emr/kos/client.py`
  - `call()`(L253-271)은 401 을 받으면 `internal_token(force=True)` 로 **다시 sign-in 하고 같은 요청을 한 번 더 보낸다**.
  - `internal_token()`(L206-238)은 `credentials.system_email · system_password`(`crm_connection.config`)로 sign-in 한다.
  - `KosCredentials.from_config`(L84-89)는 시스템 계정 이메일 · 비밀번호가 **없으면 예외**를 낸다.
  - `kos-client-uri` 헤더(L156)는 `credentials.tenant_id` 로 만든다.
- 기준: S1 규칙 8(L230) 「KOS 가 만료 전에 401 을 주면 그 세션을 끝낸다 — `expires_at` 을 지금으로 당긴다」 · S-4 2(L107) 「비밀번호가 없으므로 토큰을 다시 받을 수 없다」.
- 직원 경로에서 그대로 재사용할 수 있는 것은 헤더 상수(`WEB_USER_AGENT`) · `KosEndpoints` · `_post` · 시간 제한 설정(`emr_http_timeout_seconds` 기본 15.0 — `common/config.py:87`)뿐이다. 직원 sign-in · get-user-account(직원 토큰) · 401 처리는 **새 경로**여야 한다. 특히 sign-in 은 병원(테넌트)을 고르기 전에 일어나므로 `credentials.tenant_id` 에 기대면 안 된다.
- 고칠 방향: Target Delta 의 재사용 줄을 「헤더 · 주소 · 시간 제한 재사용. 직원 sign-in · get-user-account · 401(재-sign-in 없이 `expires_at` 당김)은 새로 만든다」로 고친다. Review Surface 의 「시스템 계정 토큰과 섞이지 않게」에 「401 재시도 금지」를 더한다.

### W2. A5 후반(KOS 401 → `expires_at` 당김)을 부르는 곳이 이 Delivery 에 없다
- A5 「KOS 가 만료 전에 401 을 주면 그 세션의 expires_at 이 지금으로 당겨지고 …」.
- 이 Delivery 에서 직원 토큰으로 KOS 를 부르는 곳은 로그인 중의 ① ~ ③ 뿐이다. 세션이 쓰이는 동안 직원 토큰으로 KOS 를 부르는 것(outbox 발송)은 Non-Goal 이다(「직원 KOS 토큰으로 KOS 쓰기 — 첫 실제 쓰기 Delivery 몫」).
- 그래서 「세션 사용 중 KOS 401」(S1 L168)이 일어날 자리가 없다. 이대로면 A5 후반은 통과시킬 방법이 없거나, 구현자가 확인 장치를 지어내게 된다.
- 고칠 방향: A5 를 「세션을 KOS 401 로 끝내는 서비스 함수(`expires_at` = 지금 · `revoked_at` 그대로 · 다른 세션 그대로)를 이 Delivery 가 만들고 단위 테스트로 확인한다. 부르는 쪽은 쓰기 Delivery」로 고친다. 앞 절반(만료 시각이 지나면 `session_expired`)은 지금 문장으로 확인할 수 있다.

### W3. A9 후반(권한 행 없는 직무 → 403 `forbidden`)을 시험할 동작이 없다
- A9 「권한 행이 없는 직무의 세션은 **권한이 필요한 동작**에서 403 forbidden」.
- 이 Delivery 의 경로 4개는 권한이 필요 없다(S1 L130-133 — login · hospital = 세션 전 · me · logout = 세션만). `permission_key` 목록은 Non-Goal 이다.
- 고칠 방향: 「권한 검사 의존성(키 · level 을 받아 `job_role_permission` 을 보는 것)을 만들고, 테스트 전용 키로 행 있음 → 통과 · 행 없음 → 403 `forbidden` 을 단위 · API 테스트로 확인한다」처럼 확인 방법을 적는다.

### W4. A7 의 CSRF 「거절」이 어떤 응답인지 정해지지 않았고, 토큰을 받는 길도 없다
- A7 「X-CSRF-Token 이 없거나 틀리면 **거절**된다」.
- S1 에는 CSRF 실패를 다루는 줄이 없다(케이스 매트릭스 L159-171). 세션 전달(L141)도 「POST 계열은 CSRF — `X-CSRF-Token` 헤더」라는 말뿐이다. 그래서 다음 두 가지가 빈칸이다.
  - 웹이 CSRF 토큰을 **어디서 받는지**
  - **로그인 전 요청**(`POST /api/auth/login` · `/hospital`)에도 CSRF 를 거는지
- 코드에는 아직 CSRF 처리가 없다(`backend/day/` 에 `session.py` · `web.py` 없음 — 계약 code_surface 가 「수정 후보」로 새로 만든다고 적었다).
- 고칠 방향: 아래 「4. CSRF 판정」대로 S1 에 줄을 더한 뒤 A7 이 그 코드를 인용하게 한다. 토큰을 주는 방식과 로그인 전 요청의 처리는 S1 이 정한다. centurion 쪽에서 모양을 가져오는 것은 S1 이 정할 때의 근거로만 쓴다.

### W5. 빈 이메일 · 비밀번호의 응답이 정해지지 않았다
- S1 Validation(L152) 「둘 다 있어야 KOS sign-in 을 부른다」 — 그런데 없을 때 무엇을 돌려주는지는 매트릭스에 없다.
- 계약 Non-Goals 는 「형식 · 길이 검사 — KOS 에 맡김」뿐이다. 그래서 빈 값일 때 400 인지 `invalid_credentials` 인지 구현자가 고른다.
- 고칠 방향: S1 매트릭스에 한 줄을 더한다(CSRF 와 같은 개정 · 사용자 결정 몫 — 오류 코드는 2026-11-05 사용자 결정 범위라서). 그 전까지는 계약 Review Surface 의 「아직 결정이 필요한 것」에 올린다.

### W6. A4 의 「11경우」와 나열이 맞지 않는다
- A4 는 「11경우」라 하고 코드는 10개를 나열한다. 「kos_unavailable(KOS 403 · 15초 넘김 포함)」에는 S1 L162 의 「응답 없음」이 빠졌다.
- S1 매트릭스는 11줄이다. `session_expired` 가 두 줄(L168 만료 · KOS 조기 401 / L169 임시 토큰)이다. 임시 토큰 줄은 A2 가 확인한다.
- 고칠 방향: A4 를 「S1 매트릭스 11줄(L161-171) 각각 — 임시 토큰 만료는 A2」로 줄 단위로 적고, kos_unavailable 에 「응답 없음」을 더한다.

### W7. Target Delta · A1 에서 S1 의 세 가지가 빠졌다
- `account.last_login_at` 을 채운다(S1 S-1 6 · L88).
- 다시 로그인할 때 직무가 KOS 에서 바뀌었으면 `job_role` 도 KOS 값을 따른다(S-2 3 · L95 · 규칙 13 L235).
- `job_role` 에 분류 태그 · 기본 직무 여부를 채운다(S-1 5 · L87).
- 계약은 「account · staff · job_role … 이 자동으로 채워진다 · 다시 로그인하면 갱신」까지만 적었다. 그래서 A1 이 이 셋을 확인하지 않는다.
- 고칠 방향: Target Delta 흐름 줄과 A1 에 세 가지를 더한다.

## 볼 것별 판정

### 1. 계약 ↔ S1 — 빠짐 · 더함

| S1 | 계약 | 판정 |
|---|---|---|
| API 4경로(L128-133) | Target Delta 1 | 같음 |
| S-1 ~ S-3 흐름 · 규칙 2 · 5 · 6 | Target Delta 2 | 같음 — 단 W7(last_login_at · 직무 갱신 · 태그) |
| 세션 전달 · token_hash(L137-146 · 규칙 7) | Target Delta 3 · A3 · A7 | 같음 |
| 만료 · 상태도(L202-215 · 규칙 8) | Target Delta 4 · A5 · A6 | 같음 — 확인 방법은 W2 |
| 규칙 1 · 3 | Target Delta 5 · A3 | 같음 |
| 규칙 12 · 막는 경우 | Target Delta 6 | 같음 |
| 매트릭스 11줄(L159-171) | Target Delta 7 · A4 | 같음 — 표기 W6 |
| 규칙 9 | Target Delta 8 · A9 | 같음 — 확인 방법은 W3 |
| 규칙 10 · 11 | Target Delta 9 · A10 | 같음 |
| 규칙 4 · S-4 3 | Non-Goal(쓰기 쪽) | 맞다 — 토큰 저장만 하는 Delivery |
| Validation(L150-153) | Non-Goal 형식 검사 | 빈 값 응답은 S1 에도 없음 → W5 |
| S1 에 없는 것 | — | 없음 |

### 2. Acceptance 가 확인 가능한가 · 실물 1회 조건

- A1 · A2 · A3 · A4 · A6 · A8 · A10 은 확인할 수 있다.
  - A3 의 「로그에 남지 않는다」는 테스트에서 로그를 붙잡아 비밀번호 글자가 없는지 보는 식으로 적어 두면 더 분명하다.
- A5 후반(W2) · A7(W4) · A9 후반(W3)은 지금 문장으로는 통과 기준이 없다.
- 실물 1회 조건은 있다. A1 「dev 데모 지점 계정으로 POST /api/auth/login」, Verification 「dev 데모 지점 계정 로그인 1회 확인」.
  - 다만 그 1회에서 무엇을 보는지(세션 발급 · 6개 테이블 행 · 2회째 중복 없음)를 Verification 에 적어 두면 A1 과 짝이 맞는다.

### 3. 「이미 있음 — 재사용」 ↔ 코드

| 계약이 말한 것 | 코드 | 판정 |
|---|---|---|
| KOS 내부 sign-in | `client.py` `internal_token` L206-238 — **시스템 계정 자격** | 모양만 재사용 · 직원용은 새로(W1) |
| get-user-account | `_user_account_id` L240-250 — 시스템 계정 id 를 얻는 private 함수 | 모양만 재사용 · 직원용(mfaMethods · 직무)은 새로 |
| 브라우저 헤더 | `internal_headers` L150-160 · `WEB_USER_AGENT` | 재사용 가능 — `kos-client-uri` 의 tenant 만 직원 경로에 맞게 |
| 401 처리 | `call` L253-271 — 재-sign-in + 재시도 | **재사용하면 규칙 8 위반**(W1) |
| 15초 | `common/config.py:87` `emr_http_timeout_seconds = 15.0` · `factory.py:46` | 맞음 |
| login_session(token_hash) / external_session | `models/staff.py` L83-107 — `token_hash` · 살아 있는 행 유일(`live_unique`) · `expires_at` · `revoked_at` · `access_token` = `EncryptedText` · `token_expires_at` | 맞음 |
| account · staff `is_active` · `last_login_at` | `models/staff.py` L21-57 | 맞음 |
| 암호화 | `common/crypto.py` — Fernet · `ENCRYPTION_KEY` · 키가 없으면 평문 저장 안 함 | 맞음 |
| get-user-tenants 는 더한다 | `client.py` 에 없음 | 맞음 |

### 4. CSRF 판정 — 어디를 고쳐야 하나

- 지금 상태
  - S1 에는 CSRF 실패 줄이 없다.
  - SPEC-002 fix1 은 케이스 매트릭스(spec-002 L358)에 「웹 쓰기 요청에 CSRF 토큰 없음 · 틀림 → 403 · 이름은 §5 OQ-16(DAY-SPEC-001 몫)」, OQ-16(L555)에 「이름은 DAY-SPEC-001 에 없다 — DAY-SPEC-001 개정 몫」이라고 적었다.
  - #227 A7 은 「거절」, open_questions 는 「CSRF 실패 오류 코드」다.
- 판정: **고칠 곳은 SPEC-001 하나**다.
  - CSRF 는 S1 의 세션 전달 계약(L141)이고, 오류 코드 · HTTP 는 S1 매트릭스가 정본이다(SPEC-002 L285 「CSRF = DAY-SPEC-001」).
  - S1 매트릭스에 「웹 쓰기 요청에 CSRF 토큰 없음 · 틀림 → 403 · `<코드 이름>`」 한 줄을 더한다. 토큰을 주는 방식과 로그인 전 요청의 적용 여부(W4)도 S1 에 적는다.
  - 코드 이름은 사용자 몫이다. 매트릭스의 코드 이름 · HTTP 는 2026-11-05 사용자 결정 범위다(S1 L173).
- 고친 뒤 할 일
  - SPEC-002 는 L358 의 「이름은 OQ-16」을 S1 줄 참조로 바꾸고 OQ-16 을 닫는다. HTTP 403 은 이미 맞으니 그대로 둔다.
  - #227 은 A7 에 그 코드를 넣고 open_question 을 지운다.
  - S1 개정이 PR #909 에 들어가면 계약은 어차피 머지 뒤 v3(baseline ready)로 다시 묶인다. 그때 같이 반영하면 된다.
  - **v2 를 지금 승인하면 A7 은 확인할 수 없는 채로 남는다.** 이 점을 승인자에게 알린다.

### 5. Issue 제목이 v1 그대로

- 제목 「DAY v2 로그인 — KOS sign-in 으로 계정 · 직원 · 세션이 채워진다」. 계약 `title` · 본문 「목표」는 「DAY v2 로그인 · 세션 — … (DAY-SPEC-001)」이다.
- 계약 판정에는 영향이 없다. 본문 메타와 「목표」 줄이 v2 이고, idempotency 는 본문 마커(`day/v2-login`)로 잡힌다.
- 다만 Issue 목록에서 범위(세션 · SPEC-001)가 보이지 않는다. 코디가 `gh issue edit 227 --title` 로 계약 `title` 과 맞추면 된다. 승인 전에 해도 digest 와 무관한지는 스킬 동작에 따른다 — 이번엔 확인하지 않았다.

### 6. 위험 L3 · 승인 대기

- 본문 메타 `contract.risk_level=L3` · `contract_version=2` · `plan_digest=sha256:7656c2aa…eb3a`.
- 라벨은 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` — **승인 라벨 없음**.
- apply `status = scope-delta-recorded` · `next_action = review-delivery-plan(human_gate: true)`.
- 코멘트에 승인 receipt · 「승인」 글이 없다.
- 판정: **맞음**. L3 근거(인증 · 쿠키 · 오류 = AGENTS.md 상 외부 계약 · 외부 credential 저장 · 외부 sign-in)도 S1 L135 와 맞다.

## 고칠 방향 요약

1. **S1 개정**(PR #909): CSRF 실패 줄 + 토큰 주는 방식 · 로그인 전 적용 여부(W4), 빈 이메일 · 비밀번호 응답 줄(W5). 코드 이름 둘은 사용자에게 묻는다.
2. **계약 v3**(머지 뒤 · 같은 key):
   - W1 재사용 문구
   - W2 A5 확인 방법(서비스 함수 단위 테스트)
   - W3 A9 확인 방법(테스트 전용 키)
   - W6 A4 줄 단위 표기
   - W7 last_login_at · 직무 갱신 · 태그
   - A7 에 CSRF 코드 넣기
3. 지금 v2 를 승인할지는 사용자 몫이다. 승인하더라도 위 셋(A5 후반 · A7 · A9 후반)은 확인할 수 없다는 것을 같이 알린다.

## 직원이 실물에서 만날 자리

- W1 을 놓치고 client 의 401 재시도를 그대로 쓰면, 직원 토큰이 일찍 끝났을 때 DAY 가 **시스템 계정으로 다시 sign-in 해서 요청을 보낸다**. 그러면 KOS 기록에 그 직원 대신 시스템 계정이 남는다(S1 규칙 4 위반). 시스템 계정 설정이 없는 병원이면 이 경로에서 예외가 난다.
