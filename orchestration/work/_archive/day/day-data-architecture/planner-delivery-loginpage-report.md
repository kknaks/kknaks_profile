# planner-delivery-loginpage 결과 보고 — done (human gate · 승인 안 함)

- **[CENTURION_DAY#232](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/232)** 「DAY v2 로그인 화면(웹) — 로그인 · 병원 고르기 · 로그아웃 (#229 매크로 · DAY-SPEC-001)」 · key `day/v2-login-page` · **L2** · target DAY-SPEC-001(pending — PR #909 미머지).
- **plan_digest = `sha256:8c8fadd9f2c8612ea3370155e857602be4a48dcb3dec7be7a60ee3bd74872ba6`** · 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`.
- 파일 `delivery/v2-login-page.json` · `.plan.json` · `.apply.json`. mediness 워크트리 파일은 이번에 고치지 않았다(SPEC-001 화면 절은 계약의 첫 phase 로 넣음).

## 계약 요약

- **모양 근거**: centurion 은 admin 이 auth(sso) 로그인으로 넘긴다(`admin/routers/session.py` → `/auth/login`). 그래서 실제 따를 템플릿은 `backend/sso/templates/login/login.html`(가운데 카드 · 제목 · 안내 · 오류 칸 · 버튼) · `login/choose.html`(고르기 목록 + 로그아웃) — 병원 고르기에 그대로 대응. Google 로그인 대신 이메일 · 비밀번호.
- **Target Delta 7**: #229 매크로로만 · 로그인 페이지(오류 문구 = SPEC-001 매트릭스 줄마다 뜻 그대로) · 병원 고르기(임시 토큰 5분) · 로그아웃 + 로그인 안 한 요청 리다이렉트(303 · HTMX 204 + HX-Redirect — 키트 README) · 로그인 뒤 = 견본(dev) 또는 빈 홈 · 웹 = 화면 라우트(#227 service · 쿠키 · CSRF 재사용 · 백엔드는 라우트 · 리다이렉트만) · **첫 phase = SPEC-001 화면 절**(모르는 문구는 OQ).
- **Acceptance A1 ~ A6**: 데모 지점 계정 실물 흐름 스크린샷 · 오류 화면(틀린 비밀번호 · 빈 입력) 스크린샷 + 나머지 문구 렌더 테스트 · 리다이렉트 · 손 CSS 0 · 인라인 스크립트 0 · CSRF(로그인 전 미적용) · SPEC-001 화면 절 PR.
- **Non-Goals**: 시술 현황 · 앱 로그인 · 디자인 새로 · 로그인 규칙 변경 · 본사/관리자 · 2단계 · prod.
- **Review Surface**: baseline pending · L2 근거 · **SPEC-001 §3 「웹 · 앱 같은 JSON /api/auth」와 웹 = 화면 라우트 원칙(SPEC-002 OQ-01)의 관계** · centurion 템플릿은 tailwind 임의값을 쓰므로 모양만 따르고 매크로 · 토큰으로 근사 · 오류 문구 사용자 확인 · 로그인 뒤 갈 곳(prod 는 빈 홈).
- **의존**: #229(매크로 · base · CSRF hx-headers) · #227(PR #228 `fb2508e4`). **담당: frontend**(라우트 · 템플릿) — 스키마에 칸이 없어 리포트에만.

## 사용자에게

1. #232 승인 receipt.
2. 로그인 화면도 웹 = 화면 라우트로 갈지(계약 기본값) — SPEC-001 §3 JSON 공용 문구 개정 여부.
3. 오류 문구 확인(SPEC-001 화면 절 phase 에서 OQ 로 올라옴).
