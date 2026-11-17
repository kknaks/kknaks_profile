# spec-2 결과 보고 — 사용자 결정 2건 · 검수 WARN 6건 반영 (DAY-SPEC-001 개정 ⑨ 보충 · DAY-SPEC-003 ⑱ 고침)

## 상태: done (미커밋 · push · Delivery 수정 없음 — 재결속은 코디)

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec` · `products/day/` 만 · 앞 판(spec-report) 미커밋 위에 이어서.

## 변경 파일 (줄 = 수정 뒤)

- `products/day/20-spec/spec-001-login-session.md` — 머리 「개정 ⑨ 보충」 노트 :44 + 본문 43곳 치환
- `products/day/20-spec/spec-003-mobile-app.md` — 개정 ⑱ 노트 다시 씀 :72 · U-1 「KOS 기기 제한」 :234 · 케이스 매트릭스 :748
- `products/day/20-spec.md` — In Scope 로그인 줄 · Out Of Scope 앱 기기 선택 줄(글자 맞춤)
- `products/day/log.md` — 2026-11-17 spec-change 행 1줄 추가(앞 ⑨ 행 위)

## 사용자 결정 반영

| 결정 | 반영 위치 (spec-001) |
|---|---|
| 1. 기기 선택 단계는 웹만 · 앱 로그인 API 는 오류 | 보충 노트 :44 ① · U-1 :84 · U-4 :99(「웹만」) · S-7 6 :241 · API 표 `/api/auth/device` 줄은 취소선(「없음」) · 응답 표 :293(403 `kos_signin_limit` 공용 오류 모양 · `choose_device` 는 웹 조각용 service 결과로만) · CSRF 목록 · 「앱 환경 연결」 규칙 9 :362(넘김 없음 → dev 4xx 를 그대로 넘김 · 지금 코드 그대로) · 직원 절 1 · 3 · 7 · 매트릭스 :449 · Flow opt · 규칙 15 · OQ-K4 · K7 닫음 · **새 OQ-K17** :616 · OQ-K14 :626 |
| 2. 시스템 계정 = 같은 UA 중 가장 오래된 하나만 해제 → 한 번 다시 | S-8 · 시스템 절 2 :397 · 로그 「1개 해제」 · OQ-K1 닫음 :607 · 매트릭스 시스템 줄 · 규칙 15 |

### 앱 오류 코드 — 기본값 = 403 `kos_signin_limit`(새 코드 · OQ-K17)

코드 사실(CENTURION_DAY dev `0c401726`): 앱은 비-2xx 본문의 `code` 를 그대로 `ApiError` 로 읽고(`app/lib/data/day_api.dart:186-188`) 로그인 실패로 끝낸다(`session_controller.dart:207-208` → `_fail`). 글자는 `copy.dart` `loginMessages` 에서 고르고, 없는 코드는 `codeOnly`(:51)라 코드 문자열만 보인다.

앱이 아는 코드는 모두 원인을 잘못 알린다. 그래서 기본값은 새 코드로 두었다.
- `invalid_credentials`: 지금 고치려는 오안내 그 글자다.
- `kos_unavailable`: 503 · 「KOS 연결에 문제」라고 나오는데 기다려도 안 풀린다. 게다가 데모 계정은 dev 의 5xx 를 prod 넘김이 `environment_unavailable` 로 바꾼다(`services/environments.py` `_relay` :258 — 4xx 만 그대로 넘김).
- `account_inactive`: DAY 계정이 막힌 것처럼 보인다.
- `invalid_request`: 빈 입력 글자가 나온다.

**깔린 앱에 보이는 것**: 오류 칸에 `kos_signin_limit` 코드만 보인다. 이메일은 남고 비밀번호는 비워진다. 자동 재시도와 KOS 해제는 없다. 오류 본문이라 `_targetFrom` 검사(W-6 의 앞선 조건)를 타지 않는다.

**대안**: 503 `kos_unavailable`(OQ-K17 대안 칸). 한글 글자는 나오지만 원인을 잘못 알린다. **사용자 확인 권장** — 지시서의 「지금 앱이 아는 코드 중」과 다른 선택이라서다.

## 검수 WARN 반영

| WARN | 반영 |
|---|---|
| W-1 토큰 종류 | 직원 절 2 하위 :409 — 임시 값에 `kind`를 둔다. 다른 단계 토큰이면 `session_expired` 로 끝내고 되돌리지 않는다. 두 방향 모두 같다. 근거 `auth.py:82` · `:234`(지금은 500). 종류 칸이 없는 값(배포 전 병원 고르기 값)은 병원 고르기 것으로 본다(기본값). 매트릭스에 새 줄 · 웹 대응표 :183 |
| W-2 근거 문장 | 직원 절 5 :412 — 잘못된 `device_id` 는 토큰을 **되돌리지 않고** `session_expired` 로 끝낸다(앱 JSON 이 없어져 400 + 되돌림은 필요 없음 · 비밀번호 암호문이 Redis 에 남는 문제도 같이 풀림). 병원 고르기와 다른 점은 코드 사실로 적었다: put_back `:225-228`, 후보 밖 = 403 `no_connected_hospital` `:238-239` 오류 카드, redirect 는 UUID 가 아닌 값 · 만료뿐 `routers/login.py:136-144`. 웹 대응표 · 매트릭스 · OQ-K8 ② 도 맞췄다 |
| W-3 해제 주체 | 시스템 절 6 :401 — worker 병원별 어댑터(`emr/factory.py` `adapter_for` · `client.py` `internal_token`)이고 api 는 아니다. 8 :403 — 서로 끊는 왕복 위험을 적었다(호출당 1회로 묶여 무한 반복 없음 · 로그로 봄 · 뿌리 OQ-K16). OQ-K1 근거도 고쳤다 |
| W-4 시스템 해제 4xx | 시스템 절 7 :402 — 로그만 남기고 다시 sign-in 하지 않으며 그 호출은 실패한다(**기본값** · OQ-K8 ③ · 대안 = sign-in 1회 더) |
| W-5 「처음으로」 | U-4 :106 · 화면 글자 :166 — 두지 않는다. OQ-K10 닫음(검수 W-5 · 코디). 처음부터는 `/login` 새로 열기 |
| W-6 | 결정 1 로 풀림. SPEC-003 ⑱ :72 · :234 · :748 을 403 `kos_signin_limit` 경로로 다시 썼다(코드 줄 근거 포함) |

## 착수 막는 OQ (갱신 뒤)

| OQ | 상태 · 기본값 |
|---|---|
| OQ-K1 | **닫음** — 가장 오래된 하나(사용자) |
| OQ-K2 | 직원 요청에도 표시 UA — 싣는다 |
| OQ-K3 | 임시 토큰 값 통째 암호문 · 5분 · 꺼내면 지움 · **되돌리지 않음** · `kind` · 웹만 |
| OQ-K4 | 웹 `POST /login/device` · service `choose_device` · `devices[...]` · `kind`(앱 경로 없음) |
| OQ-K5 · K6 | 그대로 |
| OQ-K7 | **닫음** — 앱 `choose_device` 없음 · dev 4xx 그대로 넘김 |
| OQ-K8 | ① 직원 해제 4xx → 그래도 sign-in ② 잘못된 기기 → `session_expired`(되돌림 없음) ③ 시스템 해제 4xx → 로그만 · 실패 |
| OQ-K12 | 빈 목록(웹) → 503 `kos_unavailable` |
| **OQ-K17(새)** | 앱 기기 제한 오류 = 403 `kos_signin_limit`(새 코드) · 대안 503 `kos_unavailable` |

그 밖: K9 · K11 · K13 · K15 · K16 은 그대로다. K10 은 닫았다. K14 는 다음 앱 버전 때 서버가 기기 선택을 아는 앱과 깔린 앱을 가르는 방법을 정해야 한다고 적었다.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → rc 0 · **0 error · 263 warning**. products/day 범위 ERROR 0 · WARN 0이다. 263 WARN 은 전부 타 제품 것이라 무관하다(앞 판과 같은 수).
- 개인정보: diff 추가 줄의 IPv4 · 이메일 패턴은 0건이고 비밀번호 값도 없다.

## 미결 · 주의점

- **OQ-K17**: 기본값이 새 코드라서 깔린 앱에는 영어 코드만 보인다. 사용자가 「한글 글자가 낫다」면 `kos_unavailable`(503)로 바꾸면 된다. 다만 그때 데모 계정에는 `environment_unavailable` 이 보인다.
- 다음 앱 버전에서 기기 선택을 하려면 서버가 앱을 가려야 한다(OQ-K14). 깔린 앱에는 계속 오류를 줘야 한다.
- Delivery #256 은 v1 baseline(개정 전)이다. 계약이 다시 바뀌었으니(앱 경로 제거 · 새 오류 코드) 스펙 PR 머지 → v2 재결속 → 승인 순서가 필요하다(코디).
