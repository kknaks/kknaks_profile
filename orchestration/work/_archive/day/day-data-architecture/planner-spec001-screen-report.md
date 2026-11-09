# planner-spec001-screen 결과 보고 — done (미커밋 · #232 안 건드림)

## 바뀐 곳 (`products/day/20-spec/spec-001-login-session.md`)

| 자리 | 바뀐 것 | 근거 |
|---|---|---|
| 머리말 | 개정 ④ 한 줄 | 원천 04 「웹 화면」 |
| §2 Placement | 웹 = 화면 라우트 · 앱 = JSON · 같은 service · 생김새 = centurion `sso/templates/login/login.html` · `login/choose.html` 모양 + #229 매크로(시안 나오면 맞춤) | 사용자 2026-11-06 |
| §2 UX Contract 머리 | 「문구 · 컴포넌트는 화면 SPEC 에서」 → 「웹 화면」 절 참조 | — |
| **§2 「웹 화면」 새 절** | ① 화면 라우트 표(GET/POST `/login` · POST `/login/hospital` · POST `/logout` — 같은 service · 이동 = 303 / HTMX 204 + HX-Redirect) ② CSRF — POST `/login` · `/login/hospital` 미적용 · `/logout` 적용 ③ 흐름 그림(미로그인 → 로그인 → (병원 고르기) → 로그인 뒤 갈 곳 · 로그아웃) ④ 로그인 뒤 갈 곳 = dev 견본(#229) / 빈 홈 → #231 뒤 시술 현황 ⑤ **임시 토큰 = 병원 고르기 조각의 숨은 폼 칸**(제안) ⑥ **매트릭스 13줄 + 로그아웃 성공 → 웹 처리 · 문구 대응표** | W1 ~ W5 · #227 `services/auth.py`(Redis 5분 · 한 번 쓰면 지움) · `routers/api/auth.py` · centurion kit README · admin `forbidden_page` · `?reason=` |
| §3 API 계약 머리 | 「웹 · 앱 같은 JSON」 → 「`/api/auth/*` 는 앱 전용 · 웹은 화면 라우트」 | 원천 04 |
| §3 「CSRF (웹)」 미적용 목록 | + 웹 화면 라우트 `POST /login` · `POST /login/hospital` | 검수 W5 |
| §5 OQ-1 | 정함 내용 → 앱 전용 + 웹 화면 라우트 (11-05 → 11-06 바뀜 표시) | 원천 04 |
| §5 아직 열린 것 | 「없음」 → 문구 추천안 · 숨은 폼 칸 제안 — 사용자 확인 대기 | — |

- 검수 W4 의 빠진 셋: `csrf_failed`(오류 토스트 · 화면 그대로) · `forbidden`(권한 없음 화면 · 로그아웃 버튼 · 로그인 직후도 가능) · 세션 사용 중 `session_expired`(`/login?reason=session_expired` + 안내) — 대응표에 들어감.
- `products/day/log.md` 2026-11-06 `spec-change` DAY-SPEC-001 한 줄 · lint `--strict` 0 error.

## 사용자 확인

### 1. 문구 (추천안 — 매트릭스의 뜻 그대로)

| 코드 | 화면 처리 | 추천 문구 |
|---|---|---|
| `invalid_request` 400 | 로그인 오류 칸 · KOS 안 부름 | 이메일과 비밀번호를 모두 입력해 주세요 |
| `invalid_credentials` 401 | 로그인 오류 칸 | 이메일 또는 비밀번호가 맞지 않습니다 (KOS 계정과 같습니다) |
| `kos_unavailable` 503 | 로그인 오류 칸 | KOS 연결에 문제가 있어 로그인할 수 없습니다. 잠시 뒤 다시 시도해 주세요 |
| `account_inactive` 403 | 로그인 오류 칸 | 로그인이 막힌 계정입니다. 관리자에게 문의해 주세요 |
| `no_connected_hospital` 403 | 로그인 오류 칸 | DAY 에 연결된 병원이 없는 계정입니다 |
| `no_staff_account` 403 | 로그인 오류 칸 | 이 병원의 직원 계정이 없습니다 |
| `mfa_not_supported` 403 | 로그인 오류 칸 | 2단계 인증 계정은 아직 DAY 로그인을 지원하지 않습니다 (SPEC-001 예시 그대로 — 이미 있던 문구) |
| `staff_inactive` 403 | 로그인 오류 칸 | 사용이 중지된 직원 계정입니다. 관리자에게 문의해 주세요 |
| `session_expired` 401 (세션 만료 · KOS 조기 401 · 임시 토큰 5분) | `/login?reason=session_expired` + 안내 | 로그인 시간이 끝났습니다. 다시 로그인해 주세요 |
| `unauthorized` 401 | `/login` · 안내 없음 | — |
| `forbidden` 403 | 권한 없음 화면 · 로그아웃 버튼 | 이 화면을 볼 권한이 없습니다. 관리자에게 문의해 주세요 |
| `csrf_failed` 403 | 오류 토스트 · 화면 그대로 | 페이지가 오래되었습니다. 새로고침한 뒤 다시 시도해 주세요 |
| 로그아웃 성공 | `/login?reason=logged_out` + 안내 | 로그아웃했습니다 |

### 2. 임시 토큰을 웹이 들고 가는 곳

| 안 | 내용 | |
|---|---|---|
| **① 숨은 폼 칸 (추천)** | 병원 고르기 조각에만 싣고 `POST /login/hospital` 본문으로 · URL · 쿠키 · 로그에 안 남김 | #227 이 이미 서버(Redis)에 5분 · 한 번 쓰고 지우는 방식으로 보관 — 새 쿠키 규칙 불필요 |
| ② 짧은 쿠키 | httpOnly · SameSite · 5분 쿠키 | 쿠키 규칙(이름 · 경로 · 지우기)을 새로 정해야 함 |

### 3. 그 밖 (기본값으로 둠 — 다르면 알려 주면 됨)

- 로그인 실패 때 입력한 이메일은 남기고 비밀번호는 비운다.
- 로그인 뒤 갈 곳 — dev = 견본(#229) · 그 밖 = 빈 홈.

## 다음

이 절이 사용자 확인으로 닫히면 #232 v2 — target 인용 · phase 1 · A6 · code_surface 의 mediness 줄 삭제(검수 W1) · TD6 은 이 절 인용(W2) · 임시 토큰(W3) · 13줄 렌더 테스트(W4) · A5 문장(W5).
