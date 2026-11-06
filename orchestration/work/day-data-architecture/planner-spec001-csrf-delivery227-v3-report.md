# planner-spec001-csrf-delivery227-v3 결과 보고

## 상태: done (미커밋 · Delivery 승인 안 함 · spec-002 안 건드림)

## 1. SPEC-001 개정 ③ (`products/day/20-spec/spec-001-login-session.md`)

원천 = `erd/04-staff.md` 「CSRF (웹)」 · 「빈 입력」 줄(사용자 2026-11-06).

| 자리 | 바뀐 줄 |
|---|---|
| frontmatter | `last_updated` 11-05 → 11-06 |
| 머리말 | 「2026-11-06 개정 ③ — CSRF · 빈 입력 …」 한 줄 |
| §3 세션 전달 표 | 웹 행 규칙 「CSRF — 아래 「CSRF (웹)」」 · 앱 행 「CSRF 없음」 |
| §3 새 문단 「CSRF (웹)」 | centurion admin 방식 · 세션마다 토큰 하나 `login_session.csrf_token` · `base.html` `hx-headers` 로 `X-CSRF-Token`(form 은 `csrf_token`) · 없거나 틀리면 **403 `csrf_failed`** · 로그인 전 `/api/auth/login` · `/api/auth/hospital` 은 미적용(`SameSite=Lax`) · 앱 Bearer 미적용 |
| §3 Validation 이메일 · 비밀번호 | 「하나라도 비어 있으면 KOS 를 부르지 않고 400 `invalid_request`」 |
| §3 케이스 매트릭스 | 맨 위 **400 `invalid_request`**(빈 값 · ① 전 · KOS 안 부름) 줄 · 맨 아래 **403 `csrf_failed`**(웹 쿠키 세션 쓰기 요청) 줄 → 13줄 |
| 매트릭스 아래 근거 줄 | `invalid_request` · `csrf_failed` = 사용자 2026-11-06(원천 04) |

## 3. SPEC-000 (`products/day/20-spec/spec-000-data-model.md`)

- §3 04 `login_session` 에 **`csrf_token` varchar ✓**(세션마다 CSRF 토큰 하나 · 로그인 때 무작위 · 서버가 `X-CSRF-Token` 과 비교 · 원천 「세션마다 CSRF 토큰 하나(`login_session` 과 같이)」). 해시가 아니라 값으로 둔 이유: 웹 화면이 매 렌더마다 토큰을 `hx-headers` 에 실어야 해서 서버가 원문을 알아야 한다(token_hash 와 다름).
- §3 04 `staff.is_system_account` 설명 → 「병원 연결(`crm_connection.config` `system_email`)의 sign-in 시스템 계정 하나 — 원장 목록에서 빠진다. 「마취용」 · 공용 계정은 1차에 빼지 않는다(사용자 2026-11-06 · DAY-SPEC-002 규칙 19)」.
- `log.md` 2026-11-06 `spec-change` DAY-SPEC-001 · DAY-SPEC-000 한 줄.
- lint `--strict` → **0 error** · products/day 경고 0.

⚠ `login_session.csrf_token` 은 #225 모델(PR #228)에 없다 → #227 v3 가 migration 으로 더하도록 계약에 넣었다.
⚠ DAY-SPEC-002 L358 · OQ-16(「CSRF 코드 이름은 SPEC-001 몫」)은 이제 `csrf_failed` 로 닫을 수 있다 — 지시대로 spec-002 는 건드리지 않았다(검수 뒤 반영 필요).

## 2. Delivery #227 contract v3

- 요청 `delivery/v2-login.json`(v2 사본 `v2-login.v2.json`) → `start-delivery --plan`(`v2-login.v3.plan.json`) → `--apply`(`v2-login.v3.apply.json`). code repo = CENTURION_DAY v2-dev 로컬 clone. mediness origin/main = `d93b921013af517570b9c04bd14a0668650f4887`(이번 SPEC-001 개정은 미커밋이라 baseline 은 pending 그대로).
- [Issue #227](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/227) **같은 Issue 갱신**(apply `issue_number 227` · key `day/v2-login` 가진 Issue 는 #227 하나) · 본문 메타 `contract_version=3` · updatedAt 2026-11-06T01:35Z.
- 라벨 그대로 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` · `next_action = review-delivery-plan`(human_gate). **승인 안 함.**
- **plan_digest v3 = `sha256:2351d615ae52f25b839d28dff7ea69044a0406bbb5d5d0f8ef72b48f72e9e17a`** (v2 `sha256:7656c2aa…` 는 stale).
- **Issue 제목**: CLI 가 바꾸지 않는다(v1 제목 「DAY v2 로그인 — KOS sign-in 으로 계정 · 직원 · 세션이 채워진다」 그대로 · 본문 「목표」 줄은 「로그인 · 세션 — … (DAY-SPEC-001)」). 맞추려면 코디가 `gh issue edit 227 --title "DAY v2 로그인 · 세션 — KOS sign-in 으로 계정 · 직원 · 세션이 채워진다 (DAY-SPEC-001)"` — 나는 GitHub 에 따로 쓰지 않았다.

### v2 → v3

| 항목 | v2 | v3 |
|---|---|---|
| Target Delta 흐름 | account · staff · job_role … 채움 · 갱신 | + `account.is_active=true` · `last_login_at` · `job_role` 태그 · 기본 직무 · 재로그인 때 직무 KOS 값 따름(W7) |
| 세션 전달 | 쿠키에 「쓰기 요청은 X-CSRF-Token」 | CSRF 를 새 줄로: `login_session.csrf_token`(migration) · `hx-headers` · 403 `csrf_failed` · 로그인 전 · Bearer 미적용(W4) |
| 만료 | KOS 401 → expires_at 당김 | + 이 Delivery 는 그 서비스 함수를 만들고 부르는 쪽은 쓰기 Delivery(W2) |
| 오류 계약 | 11경우 | + 400 `invalid_request` · 403 `csrf_failed`(W5 · W4) |
| 권한 | 행 없으면 forbidden | + 권한 검사 의존성 · 테스트 전용 키로 확인(W3) |
| 재사용 | KOS client(sign-in · get-user-account · 헤더 · 401 처리) | **헤더 · 주소 · `_post` · 시간 제한만.** 직원 sign-in · get-user-tenants · get-user-account · 401(재-sign-in 없이 expires_at 당김)은 새 경로 · `call()` 401 재시도 · 시스템 계정 자격 안 씀 · 병원 고르기 전엔 `tenant_id` 비의존. 모델 · crypto 는 그대로(W1) |
| A1 | 행 생성 · 갱신 · 앞 세션 유지 | + is_active · last_login_at · 직무 태그 · 기본 · KOS 직무 변경 · csrf_token |
| A4 | 「11경우」(10 나열) | SPEC-001 매트릭스 줄 단위 ①~⑫ · kos_unavailable 에 응답 없음 · 임시 토큰은 A2 · forbidden A9 · csrf A7(W6) |
| A5 | 만료 + KOS 401 당김 | 만료 = API 테스트 · KOS 401 = 서비스 함수 단위 테스트 · 로그인 중 401 은 재시도 없이 실패(W2 · W1) |
| A7 | 「거절」 | **403 `csrf_failed`** · 로그인 전 · Bearer 통과 |
| A9 | 권한 필요 동작에서 forbidden | 테스트 전용 키 — 행 있음 통과 · 없음 403(W3) |
| A10 | 헤더 + 15초 | + 병원 고르기 전 요청은 tenant_id · 시스템 계정 자격 안 씀 |
| Review Surface | CSRF 코드 미정 줄 · v1→v2 stale | CSRF 줄 삭제 · v2→v3 stale · 재사용 줄에 「401 재시도 금지」 · `csrf_token` migration 줄 |
| Execution | 5 phase · open question CSRF | 6 phase(+ csrf_token migration) · 검증에 서비스 함수 · 테스트 전용 키 · open_questions 비움 · code_surface 에 migrations |
| 위험 · baseline | L3 · pending | L3 · pending(같음) |
