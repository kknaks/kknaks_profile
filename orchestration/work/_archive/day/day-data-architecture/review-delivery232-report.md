# 리뷰 리포트 — day-data-architecture / doc · Delivery #232 로그인 화면(웹) (2026-11-06)

대상
- Issue MediSolveAIDev/CENTURION_DAY#232(contract v1 · 코멘트 0)
- `delivery/v2-login-page.json` · plan · apply
- 지시 `planner-delivery-loginpage-instructions.md` · 작성 리포트 `planner-delivery-loginpage-report.md`
- SPEC-001 은 이번에 고치지 않았다(mediness 워크트리 clean · HEAD `3c14633b`)

기준
- DAY-SPEC-001(§3 API 계약 · 케이스 매트릭스 13줄 · 「CSRF (웹)」 · Validation 빈 입력)
- #227 구현 `fb2508e4` — `backend/day/routers/api/auth.py` · `session.py` · `schemas/auth.py`
- #229 계약(v2 진행 중)
- centurion `backend/sso/templates/login/{login,choose}.html` · `admin/routers/session.py` · `medikit-htmx-kit/README.md`
- 지시서 「사용자 결정」

## 판정: WARN

FAIL 은 없다. 다음은 맞다.
- 사용자 결정 둘 — #229 다음 · 매크로로만 · 시안이 없으니 centurion 로그인 모양
- 병원 고르기 · 로그아웃 · 미로그인 리다이렉트
- 하지 않는 것(시술 현황 · 앱 · 새 디자인 · 규칙 변경)
- 손 CSS · 인라인 스크립트 grep
- 브라우저 실물 · 스크린샷 · 데모 지점 계정
- 위험 L2 · **승인 라벨 없음**

다만 다음 넷이 남는다.
- **SPEC 이 닫히기 전에 계약을 승인하는 순서**(W1)
- **SPEC-001 에서 닫힌 결정(웹도 JSON)을 기본값으로 뒤집은 것**(W2)
- 임시 토큰을 웹에서 어디에 들고 가는지 빈칸(W3)
- 매트릭스 중 화면 처리가 빠진 줄 셋(W4)

## 볼 것별

| 볼 것 | 계약 | 판정 |
|---|---|---|
| 매트릭스 줄마다 화면 문구(발명 없이) | TD2: 9개 코드 · 「매트릭스의 뜻 그대로 — 새로 지어내지 않는다」 · 모르는 문구는 SPEC-001 화면 절 OQ · A2(두 개 스크린샷 + 나머지 렌더 테스트) | 원칙은 맞다. SPEC-001 에 있는 문구는 `mfa_not_supported` 예시 하나뿐(L166 「확정 문구는 화면 SPEC」)이라 나머지는 OQ 가 맞다. 순서는 W1, 빠진 줄은 W4 |
| 병원 고르기 | TD3 · choose.html 모양 · 임시 토큰 5분 → `session_expired` 로 처음부터(S1 U-2 · S-3) | 맞다 — 토큰을 들고 가는 방식은 W3 |
| 로그아웃 | TD4 POST(CSRF) → 로그인 화면 · A5 | 맞다(#227 `logout` 은 `writable_session` = CSRF 검사 · `auth.py:103-110`) |
| 미로그인 리다이렉트 | TD4 · A3 「일반 303 · HTMX 204 + HX-Redirect」 | 맞다 — 키트 README L38 「세션 만료: HTMX 요청에는 `204 + HX-Redirect`, 일반 요청에는 303」 그대로 |
| 웹 = 화면 라우트 | TD6 · Review Surface · open_question | **W2** |
| #229 매크로만 | TD1 · A4 · Non-Goal 「새 매크로는 #229 로」 · Review Surface 「centurion 템플릿의 tailwind 임의값은 모양만」 | 맞다 |
| 의존 순서 | #229(매크로 · base · CSRF hx-headers) · #227(`fb2508e4`) | 맞다 — #227 은 PR #228 에 들어와 있고(`git log`), #229 는 진행 중(워크트리에 `static/` · `styles/` 미추적) |
| Acceptance 확인 가능 | A1 실물 흐름 · A2 스크린샷 + 렌더 테스트 · A3 라우트 테스트 · A4 grep · A5 · A6 | 대체로 가능 — A5 문장이 서로 부딪힌다(W5) |
| 승인 라벨 | `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` · 코멘트 0 | 승인 없음 |
| centurion 모양 근거 | admin `routers/session.py:26` 「콘솔 로그인 = auth 로그인 화면(`/auth/login?app=console`)」 → `sso/templates/login/login.html` | 근거가 맞다(admin 에는 로그인 템플릿이 없다) |

## WARN

### W1. SPEC-001 화면 절을 이 Delivery 의 첫 phase 로 쓴다 — 문서가 닫히기 전에 계약을 승인하게 된다
- 계약: phase 1 「SPEC-001 화면 절(화면 · 흐름 · 오류 문구 — 모르는 것은 OQ)」 · code_surface 첫 줄 `products/day/20-spec/spec-001-login-session.md(mediness)` · A6 「SPEC-001 화면 절이 PR 로 들어가 있다 · 정하지 못한 문구는 OQ 로」 · open_question 「오류 문구 — 사용자 확인」.
- 이대로면 승인 시점에는 화면 문구 · 흐름의 정본이 없다. 구현 Delivery 가 자기 SPEC 을 쓰고, 열린 OQ 를 남긴 채로 A6 을 통과할 수 있다. 문서 파이프라인(SPEC → 계약 → 구현) 순서와 반대다. 지금까지 #227 · #230 은 SPEC 이 닫힌 뒤 계약했다.
- 고칠 방향: SPEC-001 화면 절(문구 · 흐름 · 매트릭스 대응표)을 planner 가 먼저 쓰고, 문구는 사용자 확인으로 닫는다. 그 뒤 계약 v2 는 그 절을 target 으로 인용하고 phase 1 · A6 · code_surface 의 mediness 줄을 뺀다.

### W2. 「웹 = 화면 라우트」 기본값이 SPEC-001 에서 닫힌 결정과 반대다
- SPEC-001 §3(L126) 「웹(HTMX)과 앱이 같은 JSON 경로를 쓴다(cc-prototype 선례 · 사용자 2026-11-05)」 · §5 OQ-1 「정함 — JSON `/api/auth/*` 하나를 웹(HTMX) · 앱이 같이」.
- 계약 TD6 은 SPEC-002 OQ-01(시술 현황 버튼 결정)을 로그인에도 넓혀 기본값으로 삼았다. SPEC-002 OQ-01 은 시술 현황 API 에 대한 결정이고, SPEC-001 을 바꾸지 않았다.
- 계약 스스로도 Review Surface · open_question 에 「로그인 화면도 화면 라우트로 갈지」를 올렸다. 그러니 이것은 아직 사용자 결정이 아니다. 열린 질문을 기본값으로 Target Delta 에 박은 꼴이다.
- 참고 사실: #227 `/api/auth/login` 은 웹(`client=web`)이면 이미 `day_session` 쿠키를 심고 JSON 을 돌려준다(`auth.py:42-48`). 그래서 어느 쪽이든 화면 라우트(페이지 GET)는 필요하다. 차이는 **폼 제출이 HTML 조각을 받느냐, JSON 을 받고 HX-Redirect 하느냐**다.
- 고칠 방향: 이 질문을 W1 의 SPEC-001 화면 절 작업에서 사용자에게 닫게 하고, 계약은 그 답을 따른다. 화면 라우트로 가면 SPEC-001 §3 · OQ-1 문구도 같이 개정한다.

### W3. 병원 고르기의 임시 토큰을 웹이 어디에 들고 가는지 없다
- #227: 연결 병원이 여럿이면 login 응답이 `pending_token` · `expires_in_seconds` · `hospitals` 를 준다. `/api/auth/hospital` 은 본문의 `pending_token` 을 받는다(`auth.py:58-77`).
- 웹 화면은 이 토큰을 다음 요청까지 들고 가야 한다. 숨은 폼 칸인지, 짧은 쿠키인지, 서버 쪽 보관인지 계약 · SPEC-001 어디에도 없어서 구현자가 고르게 된다.
- 이 토큰은 「5분 안 세션 발급권」이라 보관 방식이 보안 결정이다. 쿠키로 들고 가면 SameSite · httpOnly 규칙도 같이 정해야 한다.
- 고칠 방향: W1 의 SPEC-001 화면 절에서 정한다(예: 숨은 폼 칸 · 응답 조각에만 · 로그에 남기지 않음). 계약은 그것을 인용한다.

### W4. 매트릭스 줄 중 화면 처리가 빠진 셋
- SPEC-001 매트릭스는 13줄이다. 계약은 로그인 화면 문구 9개와 리다이렉트(`unauthorized` · 만료)를 다룬다. 다음 셋은 화면에서 무엇이 보이는지가 없다.
  - **`csrf_failed`(403)** — 로그아웃 POST 에서 토큰이 틀리면(오래 열린 탭 · 다른 탭에서 다시 로그인)
  - **`forbidden`(403)** — 로그인 뒤 갈 곳(견본 · 빈 홈)을 권한 없는 직무가 열 때. 「권한 행이 없는 직무는 아무것도 못 한다」(규칙 9)라 로그인 직후 화면이 403 일 수 있다
  - **`session_expired` 가 세션 사용 중에 나는 경우**(L168) — TD2 는 로그인 페이지 문구 목록에 넣었고 A3 는 리다이렉트만 말한다. 「리다이렉트 + 로그인 화면에 만료 문구」인지 그냥 로그인 화면인지가 없다
- 고칠 방향: 세 줄을 W1 의 화면 절 대응표에 넣는다(문구가 없으면 OQ). A2 렌더 테스트 목록도 13줄 기준으로 적는다.

### W5. A5 문장이 서로 부딪힌다
- A5 「로그아웃 · **병원 고르기 등 쓰기 요청은 CSRF 를 지킨다** — 로그인 전 요청(로그인 · **병원 고르기**)은 CSRF 미적용」.
- SPEC-001 「CSRF (웹)」은 `/api/auth/login` · `/api/auth/hospital` 을 미적용으로 정했다. #227 도 그렇다(`session.py:9-10` 주석).
- 고칠 방향: 「쿠키 세션의 쓰기(로그아웃)는 CSRF · 로그인 전 요청(로그인 · 병원 고르기)은 미적용 · SameSite=Lax」로 고친다. W2 에서 화면 라우트로 가면 그 화면 라우트의 로그인 · 병원 고르기 POST 도 미적용 목록에 이름을 적는다.

## 참고 (이 Delivery 밖)

- #227 오류 본문은 공용 핸들러의 `{detail, code, field}`(`auth.py:3-4` 주석)다. SPEC-002 API 계약은 JSON 오류 본문을 `{error: {code, message}}`(cc 형식)로 적었다. 이번 로그인 화면은 HTML 이라 영향이 없다. 다만 #230 앱 JSON 과 SPEC-002 사이에 어긋남이 남아 있으니 코디가 한 번 정리할 것.

## 고칠 방향 요약

1. SPEC-001 화면 절을 먼저 쓴다(planner). 다음을 사용자 확인으로 닫고 계약 v2 에서 인용한다(W1 · W2 · W3 · W4).
   - 문구 · 흐름 · 13줄 대응표
   - 웹 폼이 화면 라우트로 가는지 JSON 으로 가는지
   - 임시 토큰을 들고 가는 방식
2. 계약 v2: phase 1 · A6 · mediness code_surface 를 빼고, A2 를 13줄 기준으로 고치고, A5 문장을 고친다(W5).
