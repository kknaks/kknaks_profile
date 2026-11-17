# spec-3 결과 — OQ-K17 닫음 (앱 = 지금과 같은 401 `invalid_credentials`)

상태: done · 미커밋 · `products/day/` 만 · 워크트리 `mediness-mediness/kos-signin-limit-spec`

## 반영 (사용자 2026-11-17 「심사 중 앱 화면은 지금과 같음 · 앱은 다음 버전에서 같이 고침」)
- 앱 JSON 로그인(`POST /api/auth/login`) 기기 제한 = **401 `invalid_credentials`(지금과 같음)** · 새 코드 `kos_signin_limit` 안 씀 · 원인 오안내 알고 감수 · 다음 앱 버전 때 앱 전용 처리 · 서버 로그에만 기기 제한 표시(이메일 · 비밀번호 없이). 기기 선택 단계는 웹 `/login` 만.

## 변경 (줄 = 수정 뒤)
- `spec-001-login-session.md` — 새 머리 노트 「개정 ⑨ 보충 ④」 :46 · 보충 ① 의 403 취소선 :44 · U-1 기대 결과 :86 · U-4 :101 · S-7 6 :243 · API 표 :261 · 응답 모양 :295 · 앱 환경 연결 규칙 9 :364 · 직원 절 1 :409 · 케이스 매트릭스 앱 줄 :451 · Flow opt · 규칙 15 · OQ-K7 :615 · **OQ-K17 닫음** :618 · OQ-K14 :628
- `spec-003-mobile-app.md` — 개정 ⑱ 노트 :72 다시 씀(깔린 앱 화면 = 틀린 비밀번호와 같은 글자) · U-1 「KOS 기기 제한」 :234 · 케이스 매트릭스 :748
- `20-spec.md` — In Scope · Out Of Scope 로그인 줄 글자 맞춤
- `log.md` — 2026-11-17 spec-change 행 1줄 추가(보충 ④)

## 검증
`python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error · products/day WARN 0 (WARN 263 은 타 제품 · 무관).
`kos_signin_limit` 남은 곳 = 「쓰지 않음」 · 취소선 기록뿐(spec-001 :44 · :46 · :618 · spec-003 :72 · log).

## 남은 것
- 앞 판 log 행(보충 ① ~ ③)의 「403 `kos_signin_limit`」 글은 이력이라 그대로 둠(새 행이 뒤집음).
- Delivery Issue 재결속은 코디 몫.
