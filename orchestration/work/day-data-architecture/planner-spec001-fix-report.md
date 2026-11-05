# DAY-SPEC-001 — 사용자 결정 반영 결과 보고

## 상태: done

## 수행 내용

워크트리 `mediness-mediness/day-data-architecture-spec`(PR #909 브랜치) · `products/day/` 만. 커밋 안 함.

`products/day/20-spec/spec-001-login-session.md` — OQ-1 ~ OQ-11(2026-11-05 사용자 · 전부 권장안)을 본문 계약으로 옮기고 §5 는 「정함」 표로 남김. status `draft` 유지 · **version `0.0.1` 유지**(템플릿 규칙: version 은 제품 버전 — 문서 개정으로 올리지 않는다. 개정은 머리의 「2026-11-05 개정 ①」 노트 + log 가 소유).

| 자리(줄) | 바뀐 것 | OQ |
|---|---|---|
| :43 §1 「1차 범위」 새 절 | 1차 로그인 = 병원 직원만 · 본사 · 시스템 관리자는 「1차 밖 — DAY-SPEC-000 `login_session` 개정과 함께」 · 2단계 인증 계정은 1차에서 다루지 않음 | 7 · 6 |
| §2 U-2 · U-3 · S-1 ~ S-6 | dev 후보 = 데모 연결만 · 병원 바꾸기 = 다시 로그인 · 로그아웃은 다른 기기 세션 유지 · 실패 지점마다 오류 코드 · 만료 = KOS 토큰 만료 · 조기 401 → 세션 끝 · 토큰 끝난 직원의 쓰기 「반영 중」 유지 · KOS 로그아웃 안 알림 · 권한 행 없으면 아무것도 못 함 | 10 · 8 · 3 · 4 · 5 · 11 |
| :122 §3 API 계약 | `POST /api/auth/login` · `POST /api/auth/hospital` · `GET /api/auth/me` · `POST /api/auth/logout` — 웹 · 앱 공용 JSON | 1 |
| :135 「세션 전달」 표 | 웹 쿠키 `day_session`(httpOnly · SameSite=Lax · Secure · CSRF `X-CSRF-Token`) · 앱 `Authorization: Bearer` · 같은 `login_session` · 쿠키 수명 = `expires_at` | 2 · 3 |
| :151 케이스 매트릭스 | HTTP · 오류 코드 칸 추가 — `invalid_credentials` 401 · `kos_unavailable` 503 · `account_inactive` · `no_connected_hospital` · `no_staff_account` · `mfa_not_supported` · `staff_inactive` 403 · `session_expired` · `unauthorized` 401 · `forbidden` 403 | 4 · 6 · 9 · 11 |
| Flow · 상태 | 경로 · 쿠키 / Bearer · 만료 = KOS 토큰 만료 · 세션 여러 개 동시 사용중 | 1 · 2 · 3 |
| :216 Functional Rule 12개 | 위 결정을 규칙으로(4 · 5 · 6 · 7 · 8 · 11 새로 / 보강) | 전부 |
| :237 §5 | OQ 표 11행 「정함(사용자 2026-11-05)」 + 근거. **OQ-6 근거에 「cc-prototype 은 2단계 인증 처리가 없다(시스템 계정 하나) · KOS 명동점 직원 계정 90개 중 2단계 인증 켜진 계정 0개(2026-11-05 코디 확인)」** | 전부 |
| :255 「아직 열린 것」 | 결정에 값이 없던 것만 — 아래 미결 1 ~ 3 + permission_key 목록(SPEC-000 OQ-04-2) | — |

`products/day/log.md:17` — 2026-11-05 `spec-change` · DAY-SPEC-001 · #909 한 줄.

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 은 타 제품 기존 — 무관)
```

본문에 남은 「→ OQ-n」 0개.

## 미결 · 주의점 (권장안 밖에서 내가 붙인 이름 — 확인 바람)

1. **경로 이름 두 개**: 권장안은 `POST /api/auth/login` · `GET /api/auth/me` 만 이름이 있고 「로그아웃 · 병원 고르기는 같은 접두어」였다. `POST /api/auth/logout` · `POST /api/auth/hospital` 은 그 접두어 안에서 내가 붙인 이름이다.
2. **오류 코드 세 개**: 권장 후보 7개(`invalid_credentials` · `kos_unavailable` · `no_connected_hospital` · `no_staff_account` · `mfa_not_supported` · `account_inactive` · `session_expired`)에 더해, 결정은 됐지만 코드가 없던 자리에 `staff_inactive`(OQ-9 비활성 직원) · `unauthorized`(세션 없음 — cc 선례 이름) · `forbidden`(권한 없음 · OQ-11)을 같은 형식으로 붙였다. SPEC 에도 그렇게 적었다.
3. **SPEC 「아직 열린 것」으로 둔 것** — 결정에 값이 없어 정하지 않았다: KOS 호출 시간 제한 값 · 비활성 직원을 아는 방법(③ 응답에 활성 칸이 안 보임 — 동기화 전 첫 로그인을 어떻게 볼지) · 로그인 1단계 → 병원 고르기를 잇는 방법(1단계의 KOS 토큰을 클라이언트에 주지 않는 방식 — 구현 때 정해 SPEC 에 돌려 적기).
4. 이전 리포트대로 — Delivery #227 target 에 SPEC-001 을 넣으려면 `day/v2-login` 을 contract_version 2 + scope_delta 로 재실행하고 L3 재승인이 필요하다(코디 처리).
