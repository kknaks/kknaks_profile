# 리뷰 리포트 — day-data-architecture / doc · SPEC-001 개정 ③ + Delivery #227 contract v3 (2026-11-06)

대상
- mediness 워크트리 `day-data-architecture-spec`(미커밋)의 `spec-001-login-session.md` · `spec-000-data-model.md` diff
- Issue MediSolveAIDev/CENTURION_DAY#227 본문(updatedAt 2026-11-06T01:35Z)
- `delivery/v2-login.json`(contract v3)
- 작성 리포트 `planner-spec001-csrf-delivery227-v3-report.md`
- 앞 검수 `review-delivery227-v2-report.md`(W1 ~ W7)

lint `python3 scripts/lint-pipeline.py --strict` → **0 error**, `products/day/` 경고 0(263 warning 은 다른 제품 — 무관).

## 판정: WARN (가벼움 1건)

- SPEC-001 개정 ③ 은 원천 04 「CSRF (웹)」 · 「빈 입력」 두 줄 그대로다. 발명은 없다.
- v3 는 v2 지적 W1 ~ W7 을 모두 닫았다. W1 은 고칠 방향대로 정확히 닫혔다.
- SPEC-000 `is_system_account` 설명은 사용자 결정과 맞다.
- 승인 라벨은 없다.

남은 지적은 하나(N1)다. 병원 고르기 전 KOS 요청에 실을 `kos-client-uri` 값이 비어 있어 구현자가 고르게 된다. 다만 답이 HAR 에 있어 한 줄이면 닫힌다. 그 밖은 후속 정리 2건이다(SPEC-002 OQ-16 · 원천 04 의 옛 설명).

## 1. SPEC-001 개정 ③ ↔ 원천 04

원천: `erd/04-staff.md` L130 「CSRF (웹)」 · L131 「빈 입력」.

| 원천이 정한 것 | SPEC-001 | 판정 |
|---|---|---|
| centurion admin 방식 · 세션마다 토큰 하나(`login_session` 과 같이) | 「CSRF (웹)」 첫 줄 · `login_session.csrf_token` | 같음 |
| `base.html` 이 `hx-headers` 로 `X-CSRF-Token` | 둘째 줄 | 같음. 「form 은 `csrf_token` 필드」는 CENTURION_DAY `AGENTS.md` 「웹 화면」에서 가져왔고 출처를 적었다 — 발명 아님 |
| 없거나 틀리면 403 `csrf_failed` | 셋째 줄 · 매트릭스 맨 아래 줄 | 같음 |
| 로그인 전 `/api/auth/login` · `/hospital` 미적용 · `SameSite=Lax` | 넷째 줄 · 매트릭스 「해당 없음」 | 같음 |
| 앱 Bearer 는 CSRF 없음 | 다섯째 줄 · 세션 전달 표 앱 행 | 같음 |
| 빈 이메일 · 비밀번호 → KOS 안 부름 · 400 `invalid_request` · 401 과 구분 | Validation · 매트릭스 맨 위 줄 | 같음 |
| 근거 · 머리말 | 매트릭스 아래 근거 줄 · 개정 ③ 머리말 | 맞음 |

SPEC-000 `login_session.csrf_token`(varchar ✓)은 원천의 「세션마다 CSRF 토큰 하나(`login_session` 과 같이)」를 칸으로 둔 것이라 맞다. 해시가 아닌 원문으로 둔 이유(작성 리포트 — 화면이 렌더할 때마다 실어야 함)도 맞다.

## 2. v2 지적 W1 ~ W7 — 닫혔나

| W | v3 | 판정 |
|---|---|---|
| W1 재사용 · 401 | Target Delta 마지막 줄을 보면 재사용은 「브라우저 헤더 · `KosEndpoints` · `_post` · `emr_http_timeout_seconds`」 넷뿐이다. 직원 sign-in · get-user-tenants · get-user-account · 401(재-sign-in 없이 `expires_at` 당김)은 **새 경로**다. `call()` 의 재-sign-in · 재시도와 `internal_token()` 의 시스템 계정 자격은 직원 경로에 쓰지 않는다. 병원 고르기 전에는 `credentials.tenant_id` 에 기대지 않는다. Review Surface 에 「401 재시도 금지」, A5 에 「로그인 중 KOS 401 은 재-sign-in · 재시도 없이 실패」, A10 · phase 1 에도 같은 내용이 있다 | **닫힘** — 코드(`client.py` L206-271 · L84-89 · L156)와 맞는다 |
| W2 A5 후반 | 「KOS 401 로 세션 끝내기」를 서비스 함수로 만들고 단위 테스트로 확인한다. 부르는 쪽은 쓰기 Delivery 다. verification 에도 줄이 있다 | 닫힘 |
| W3 A9 후반 | 권한 검사 의존성 + 테스트 전용 키 — 행 있음 통과 · 행 없음 403(단위 · API) | 닫힘 |
| W4 A7 | 403 `csrf_failed` · `login_session.csrf_token` 비교 · 로그인 전 · Bearer 는 통과. migration 을 phase · code_surface · Review Surface 에 넣었다 | 닫힘 |
| W5 빈 입력 | A4 ① 400 `invalid_request`(KOS 안 부름) · phase 3 | 닫힘 |
| W6 A4 표기 | SPEC-001 매트릭스 줄 단위 ① ~ ⑫ · kos_unavailable 「응답 없음」 · 임시 토큰은 A2 · forbidden 은 A9 · csrf 는 A7 로 넘김 | 닫힘. 매트릭스 13줄과 A4 의 12항목 + A2 가 빠짐 없이 맞는다 |
| W7 빠진 셋 | Target Delta 흐름 · A1 에 `is_active = true` · `last_login_at` · 직무 태그 · 기본 직무 · KOS 직무 변경 반영 | 닫힘 |

## 3. Acceptance — 확인 가능한가

- A1 ~ A10 모두 「무엇을 · 어떤 테스트로」가 적혀 있다.
  - 케이스 테스트: A2 · A4
  - 서비스 함수 단위 테스트: A5
  - 테스트 전용 키: A9
  - KOS client 테스트: A10
- 실물 1회 조건도 있다. A1 「dev 데모 지점 계정으로」, verification 「dev 데모 지점 계정 로그인 1회 확인」.
- 참고(지적 아님): v2 검수 때 「이러면 더 분명하다」로 남긴 두 가지 — A3 의 로그 붙잡기 확인 방법, 실물 1회 때 볼 것 목록 — 는 반영되지 않았다. A1 문장이 볼 것을 이미 담고 있어 통과 기준은 선다.

## 4. SPEC-000 `is_system_account`

- 바뀐 설명: 「병원 연결(`crm_connection.config` `system_email`)의 sign-in 시스템 계정 하나 — 원장 목록에서 빠진다. 「마취용」 · 공용 계정은 1차에 빼지 않는다(사용자 2026-11-06 · DAY-SPEC-002 규칙 19)」.
- 근거와 맞는다.
  - 결정 원천: `screen/procedure-board-decisions.md` L35 「1차는 빼지 않고 다 넣는다 … sign-in 시스템 계정만 지금처럼 자동으로 빠진다(#226)」
  - SPEC-002 규칙 19 · 25 · 닫은 OQ-06 · OQ-11
  - 코드: `KosCredentials.system_email`(`client.py` L75-89)
- 앞 fix1 검수 N2(「시스템 계정 하나」를 고를 길 없음)도 이 설명으로 닫힌다.

## 5. 승인 · 위험 · Issue

- 메타는 `contract_version=3` · `plan_digest=sha256:2351d615…e17a` · `risk_level=L3` · `spec_baseline_revision=d93b921`(pending)이다.
- 라벨은 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` — **승인 라벨 없음**.
- 코멘트 2개는 scope-delta v2 · v3 기록뿐이고 승인 receipt 는 없다.
- 본문 「아직 결정이 필요한 것」은 「없음」이다. v2 의 CSRF open question 이 닫혔다.
- Issue 제목은 여전히 v1(「DAY v2 로그인 — …」)이다. 계약에는 영향이 없다. 코디가 `gh issue edit` 로 맞추면 된다(작성 리포트에 명령이 있다).

## WARN

### N1. 병원 고르기 전 KOS 요청의 `kos-client-uri` 값이 비어 있다
- v3 A10 · Target Delta 는 「병원 고르기 전 요청은 연결 설정의 `tenant_id` 에 기대지 않는다」고 **하지 말 것**만 말하고, 대신 무엇을 실을지는 말하지 않는다.
- SPEC-001 규칙 10 은 sign-in · get-user-tenants · get-user-account 에 `kos-client-uri` 를 싣는다고만 한다.
- 지금 코드는 모든 내부 요청에 `{web}/{tenant}/reservation/schedule/` 를 싣는다(`client.py` L156).
- 그래서 구현자가 값을 고르게 된다. KOS 내부 API 차단(2026-11-03~)이 헤더를 보는 상황이라 잘못 고르면 로그인이 403 → `kos_unavailable` 로 멈출 수 있다.
- 답은 이미 HAR 에 있다. `reference/2026-10-12-cc-prototype/로그인.har` 의 KOS 웹 요청이 실은 값의 모양(값 자체는 옮기지 않음)은 이렇다.

| 요청 | `kos-client-uri` 모양 |
|---|---|
| sign-in | `<web>/auth/sign-in` |
| get-user-tenants | `<web>/hospital/select` |
| get-user-account | `<web>/<tenant>` |

- 고칠 방향: SPEC-001 규칙 10 에 위 모양을 한 줄로 적고(근거 HAR), 계약 A10 이 그것을 인용한다. 계약은 PR #909 머지 뒤 v4 로 다시 묶이므로 그때 같이 반영해도 된다. SPEC-001 만 먼저 고치고 구현 브리프에 넘겨도 된다.

## 후속 (이번 대상 밖 · 코디 정리용)

1. SPEC-002 는 아직 「이름은 §5 OQ-16(DAY-SPEC-001 몫)」(케이스 매트릭스 L360)과 OQ-16(L554)이 열려 있다. SPEC-001 에 `csrf_failed` 가 생겼으므로 L360 을 `csrf_failed` 로 바꾸고 OQ-16 을 닫는다. 이번 지시가 SPEC-002 를 막았으니 작성 리포트대로 다음 판에서 하면 된다.
2. 원천 `erd/04-staff.md` L64 의 `is_system_account` 설명이 옛 문구(「사람이 아닌 계정(시스템 · 공용) — 원장 목록 등에서 뺀다 (cc KOS_EXCLUDE_ACCOUNT_IDS)」)로 남아 있다. SPEC-000 은 새 결정(procedure-board-decisions L35)을 따르므로 원천 표와 SPEC 이 어긋난다. 원천 쪽 한 줄 정리 여부는 코디 판단이다.
