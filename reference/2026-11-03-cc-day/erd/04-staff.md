# 04 직원 · 계정 · 로그인 · 역할

2026-11-03 사용자와 정함. 공통 규칙은 [README.md](README.md). 검토표: https://claude.ai/artifact/2GdAR4BNwe9BykTpb66K3S

## 정한 것

- **로그인 = 우리 로그인 화면 → KOS sign-in → 반환값 저장**(사용자 2026-11-03). DAY 는 비밀번호를 저장하지 않는다.
- **로그인하면 우리 값이 자동으로 채워진다** — 관리자가 계정을 미리 만들지 않는다.
- **역할 = KOS 직무(`job_role`) 그대로**(사용자 2026-11-03). DAY 가 역할을 따로 만들지 않는다. DAY 에서 할 수 있는 일은
  직무별 `job_role_permission` 으로 정한다. KOS 화면 권한(`featureList`)은 쓰지 않는다. KOS 를 떼도 `job_role` 은 DAY 테이블로 남는다.
- KOS 직무가 없는 두 종류: **본사**(브랜드 조회 — `account_brand_access`) · **시스템 관리자**(`account.is_system_admin`).
- 직무 분류 태그(`job_role.tags` — 고정 7개)로 업무를 판단한다(의사 목록 · 상담사 목록).
- KOS 사용자 id · 직원 계정 id · 직무 id 는 `external_ref`. KOS 토큰은 `external_session`(KOS 를 떼면 테이블째 지움).
- DAY 가 직원의 KOS 토큰으로 KOS 에 쓴다 — KOS 기록에 실제 직원이 남는다(cc 는 시스템 계정 하나로 썼다).

## 로그인 흐름 — KOS 그대로 (`reference/2026-10-12-cc-prototype/로그인.har`)

| 순서 | KOS 호출 | 응답 | DAY 에 채워지는 것 |
|---|---|---|---|
| ① | `common/v1/user/commands/sign-in` `{email, password}` | 사용자 id · email · name · tenantIds · token · 토큰 만료 | `account`(없으면 만들고 있으면 갱신) · `external_ref`(account ↔ KOS 사용자 id) |
| ② | `common/v1/tenant/queries/get-user-tenants` | 소속 병원(테넌트) 목록 | DAY 에 연결된 병원(`crm_connection.config.tenant_id`)만 고른다 — 하나면 자동 |
| ③ | `tenants/{id}/v1/account/queries/get-user-account` | 그 병원의 직원 계정 id · 이름 · 직무(role · roleTags) | `staff`(있으면 `account_id` 연결, 없으면 만듦) · `job_role` |
| — | — | — | `login_session` + `external_session`(KOS 토큰 · 만료 · 테넌트 id) |

KOS 명동점: 직원 90 · 의사 10 · 상담 31 · 직무 21 · 분류 태그 7(`admin` · `doctor` · `counselor` · `nurse` · `skincare` ·
`call_counselor` · `coordinator`). 직무 하나에 태그가 여럿(예: 코디 = call_counselor · counselor · coordinator).

## `account` — DAY 로그인 계정 (= KOS 사용자 1명)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | DAY 로그인 계정 = KOS 사용자 1명(여러 병원 테넌트에 속할 수 있다). 로그인은 우리 화면 → KOS sign-in. KOS 사용자 id 는 external_ref(entity_type = account) | sign-in data.id |
| `email` | varchar | ✓ | 로그인 이메일 — KOS sign-in 응답 | sign-in data.email |
| `name` | varchar | ✓ | 표시 이름 | sign-in data.name |
| `is_system_admin` | bool | ✓ | 시스템 관리자 — 병원 직원이 아니라 KOS 직무가 없다. 전체를 본다 |  |
| `is_active` | bool | ✓ | 로그인 허용 | cc account.active |
| `last_login_at` | timestamptz |  | 마지막 로그인 |  |
| `created_at · updated_at` | timestamptz | ✓ |  |  |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 | |

## `account_brand_access` — 본사 조회 (계정 ↔ 브랜드)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `account_id` | uuid FK → account · PK | ✓ | 본사(브랜드 조회) 계정 — KOS 직무가 없다 |  |
| `brand_id` | uuid FK → brand · PK | ✓ | 볼 수 있는 브랜드 — 소속 지점 데이터 조회만 |  |
| `created_at · updated_at` | timestamptz | ✓ |  |  |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 | |

## `staff` — 병원 직원 (KOS 직원 계정 미러 · 계정 1 : 직원 N)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 병원 직원 1명 — 외부 CRM 직원 계정 1개 = 1행 | account.id |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `account_id` | uuid FK → account |  | 이 직원으로 로그인하는 DAY 계정 — 로그인 때 KOS get-user-account 로 잇는다. 한 계정이 병원마다 직원 행을 가진다(계정 1 : 직원 N) | get-user-account data.id ↔ sign-in data.id |
| `name` | varchar | ✓ | 표시 이름 (KOS name — 닉네임일 수 있음) | name |
| `real_name` | varchar |  | 실명 | realName |
| `email` | varchar |  | KOS 계정 이메일 | email |
| `license_number` | varchar |  | 면허번호 — 의사 · 간호사 | licenseNumber |
| `job_role_id` | uuid FK → job_role |  | 직무 (병원별 이름 — 원장 · 간호 · 코디 …) | roleId · roleName |
| `default_zone_id` | uuid FK |  | 기본 근무 구역(층) | defaultWorkingZoneId |
| `is_active` | bool | ✓ | 재직(활성) — 퇴사자는 끈다 | activate |
| `is_system_account` | bool | ✓ | 병원 연결의 sign-in 시스템 계정 하나 — 원장 목록에서 빠지고 KOS 담당자(`assigneeIds`)로 쓴다. 마취용 · 공용 계정은 1차에 빼지 않는다(사용자 2026-11-06 · `screen/procedure-board-decisions.md`) |  |
| `created_at · updated_at` | timestamptz | ✓ |  |  |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 | |

## `job_role` — 직무 = DAY 역할 (KOS role 그대로)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 병원별 직무 = DAY 역할. KOS role 을 그대로 쓴다(로그인 때 get-user-account 로 받음). KOS 를 떼도 DAY 테이블로 남는다. 명동점 21개 | id |
| `hospital_id` | uuid FK → hospital | ✓ |  |  |
| `name` | varchar | ✓ | 직무 이름 | name |
| `tags` | enum[] admin · doctor · counselor · nurse · skincare · call_counselor · coordinator | ✓ | 직무 분류 — 고정 7개. 한 직무가 여럿 (예: 코디 = call_counselor · counselor · coordinator). 업무 판단(의사 목록 · 상담사 목록)은 이걸로 | roleTags[] (1~7) |
| `is_default` | bool |  | KOS 기본 직무인지 | isDefault |
| `created_at · updated_at` | timestamptz | ✓ |  |  |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 | |

## `job_role_permission` — 직무별 DAY 권한

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `job_role_id` | uuid FK → job_role · PK | ✓ | 직무 1 : 권한 N — DAY 관리자가 정한다 |  |
| `permission_key` | varchar · PK | ✓ | DAY 에서 할 수 있는 일 — 코드가 정한 목록(예: board.view · board.call_doctor · visit.edit · settings.crm) | centurion sso.menu_catalog |
| `level` | enum view · edit | ✓ | 보기만 / 고치기까지 |  |
| `created_at · updated_at` | timestamptz | ✓ |  |  |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 | |

## `login_session` — DAY 로그인 세션

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | DAY 로그인 세션 |  |
| `token_hash` | varchar UNIQUE | ✓ | 세션 토큰의 해시 — 쿠키 · Bearer 에는 따로 만든 무작위 토큰을 주고 DB 에는 해시만 둔다(세션 id 를 그대로 쓰지 않는다 · 사용자 2026-11-05) |  |
| `account_id` | uuid FK → account | ✓ |  |  |
| `hospital_id` | uuid FK → hospital | ✓ | 지금 고른 병원 — KOS 사용자가 여러 테넌트에 속하면 로그인 뒤 고른다 | get-user-tenants |
| `staff_id` | uuid FK → staff | ✓ | 그 병원에서의 직원 | get-user-account |
| `expires_at · last_used_at · revoked_at` | timestamptz |  | 만료 · 마지막 사용 · 로그아웃 |  |
| `created_at · updated_at` | timestamptz | ✓ |  |  |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 | |

## `external_session` — KOS 토큰 (KOS 를 떼면 지움)

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `session_id` | uuid FK → login_session · PK | ✓ | 세션 1 : KOS 토큰 1 — KOS 를 뗄 때 이 테이블째 지운다(핵심 테이블에 KOS 칸을 두지 않는다) |  |
| `vendor` | enum kos · vegas | ✓ |  |  |
| `access_token` | 암호화 text | ✓ | KOS sign-in 이 준 토큰 — DAY 가 이 직원 이름으로 KOS 에 쓴다(KOS 기록에 실제 직원이 남는다) | sign-in data.token |
| `token_expires_at` | timestamptz | ✓ | 토큰 만료 — 지나면 다시 로그인 | tokenExpiredDateTimeUtc |
| `external_tenant_id` | varchar | ✓ | 고른 병원의 KOS 테넌트 id | get-user-tenants data[].id |
| `created_at · updated_at` | timestamptz | ✓ |  |  |
| `deleted_at` | timestamptz | | 소프트 딜리트 — null = 살아 있음 | |

## 정할 것

1. ~~KOS 계정에 2단계 인증(`mfaMethods`)이 켜진 경우의 로그인 흐름~~ → 정함(2026-11-05): 1차는 다루지 않고 막고 안내 — cc 처리 없음 · 명동점 직원 계정 90개 중 0개. DAY-SPEC-001 OQ-6.
2. `permission_key` 목록 — 화면이 정해질 때 코드에서 정한다.

## 로그인 · 세션 계약 (2026-11-05 사용자 결정 — DAY-SPEC-001)

| 주제 | 정한 것 |
|---|---|
| API 경로 | 웹 · 앱 공용 JSON — `POST /api/auth/login` · `GET /api/auth/me` · `POST /api/auth/hospital`(병원 고르기) · `POST /api/auth/logout` |
| 세션 전달 | 웹 쿠키 `day_session`(httpOnly · SameSite=Lax · Secure · CSRF `X-CSRF-Token`) · 앱 `Authorization: Bearer` — 같은 `login_session` 한 행. 토큰은 무작위 값, DB 에는 `token_hash` |
| 세션 길이 | DAY 세션 만료 = KOS 토큰 만료. 여러 기기 동시 로그인 허용 |
| 병원 고르기 | 연결된 병원이 하나면 바로 세션. 여럿이면 짧은 임시 토큰(5분) → 병원을 고르면 진짜 세션 |
| 오류 | 401 `invalid_credentials` · 503 `kos_unavailable`(KOS 장애 · KOS 403 `Unsupported client.` 포함) · 403 `no_connected_hospital` · 403 `no_staff_account` · 403 `mfa_not_supported` · 403 `account_inactive` · 403 `staff_inactive` · 401 `session_expired`(만료 — KOS 토큰이 일찍 끝난 경우(KOS 조기 401) · 병원 고르기 임시 토큰(5분) 만료 포함) · 401 `unauthorized`(세션 없음 · 로그아웃된 세션) · 403 `forbidden`(권한 없음) |
| 재로그인 | KOS 401 → 세션 끝(`login_session.expires_at` 을 지금으로 당긴다 — `revoked_at` 은 로그아웃에만) · 다시 로그인. 토큰 만료 직원의 쓰기 큐는 다시 로그인까지 「반영 중」. 로그아웃은 KOS 에 알리지 않는다 |
| CSRF (웹) | **centurion admin 방식** — 세션마다 CSRF 토큰 하나(`login_session` 과 같이) · 웹 화면(`base.html`)이 `hx-headers` 로 `X-CSRF-Token` 을 싣는다 · 없거나 틀리면 **403 `csrf_failed`**. 로그인 전 요청(`/api/auth/login` · `/api/auth/hospital`)은 세션이 없어 CSRF 를 걸지 않고 `SameSite=Lax` 쿠키로 막는다. 앱(Bearer)은 CSRF 없음 (사용자 2026-11-06) |
| 빈 입력 | 이메일 · 비밀번호 중 하나라도 비어 있으면 KOS 를 부르지 않고 **400 `invalid_request`**(틀린 비밀번호 401 `invalid_credentials` 와 구분) (사용자 2026-11-06) |
| 웹 화면 | **웹 로그인은 화면 라우트**(`/login` · `/login/hospital` · 로그아웃) — 폼을 받아 오류는 HTML 조각 · 성공은 이동. **`/api/auth/*` JSON 은 앱 전용**. 로직은 같은 service(#227). 시술 현황(SPEC-002 OQ-01)과 같은 규칙 — 11-05 「웹 · 앱 같은 JSON」을 바꿈 (사용자 2026-11-06) |
| 1차 범위 | 병원 직원만. 본사 · 시스템 관리자 로그인은 1차 밖(`login_session` 개정과 함께). 2단계 인증 계정은 막고 안내 |
| 그 밖 | 로그인 후 병원 바꾸기 = 다시 로그인 · 비활성 직원 = 로그인 막기(판정 = 기준 정보 동기화 `get-accounts.activate` 로 채운 `staff.is_active`) · dev 서버 = 데모 연결 병원만 · 권한 행 없는 직무 = 아무것도 못 함 · 처음 만든 `account.is_active` = true · KOS 호출 시간 제한 15초(cc 값) · 이메일 · 비밀번호 형식 검사는 KOS 에 맡긴다 · 안내 문구는 화면 SPEC(예시만) |
