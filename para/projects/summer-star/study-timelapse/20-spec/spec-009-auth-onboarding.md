---
type: spec
id: STL-SPEC-009
title: "Auth & 온보딩 도메인"
status: in_dev
product: study-timelapse
created_at: 2026-05-18
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/spec
  - status/in_dev
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-008-mobile-revenuecat-integration|STL-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# Auth & 온보딩 도메인

Google/Apple OAuth id_token 을 검증해 JWT 를 발급하고, 신규 사용자는 약관 동의 → 트라이얼 소개 → paywall 온보딩으로 안내한다. 기존 사용자는 로그인 직후 홈 진입.

> 원본: `medi_docs/current/spec/spec-09-auth-onboarding.md`. 원본 frontmatter 에 ADR depends 없음 → `links.decisions` 비움(추론 금지). 구독/온보딩 연계는 [[spec-003-subscription-state-machine|STL-SPEC-003]]·[[spec-008-mobile-revenuecat-integration|STL-SPEC-008]] 로 연결.
>
> **status: in_dev** — backend auth(Google·Apple·refresh)는 전부 구현됐으나, **모바일 Apple Sign-In 이 end-to-end 미연동**이다(아래 Open Questions). 태스크 brief 는 "POST /api/auth/apple 코드 미구현"으로 적었으나 **코드 대조 결과 backend 는 구현됨** — 실제 gap 은 mobile 측이다(코드를 따름).

## Context

- 짝 spec: 구독 상태([[spec-003-subscription-state-machine|STL-SPEC-003]], 가입 초기 `free`), mobile RevenueCat([[spec-008-mobile-revenuecat-integration|STL-SPEC-008]], 온보딩 trial-intro)
- 범위: OAuth 검증·JWT 발급·신규/기존 분기·온보딩 라우팅

## BE Contract (Auth Endpoints)

| 엔드포인트 | 인증 | Request | 비고 |
|---|---|---|---|
| `POST /api/auth/google` | 불필요 | `{id_token, terms_agreed, privacy_agreed, timezone}` | id_token 검증 → JWT |
| `POST /api/auth/apple` | 불필요 | `{identity_token, name, terms_agreed, privacy_agreed, timezone}` | identity_token(JWKS/kid) 검증 → JWT |
| `POST /api/auth/refresh` | 불필요 | `{refresh_token}` | 새 JWT 쌍 |

- Response(google/apple): `{tokens:{access_token, refresh_token, token_type, expires_in}, user:{id, provider, email, name, is_new}}`
- 검증 실패(만료/조작/kid 불일치) → 401
- 토큰: access 60분, refresh 30일
- Apple 공개키 인메모리 캐시(kid). 미매칭 시 캐시 무효화 후 1회 재시도

### 신규 User 초기값
| 필드 | 값 |
|---|---|
| `subscription_status` | `free` |
| `trial_start_date` | NULL |
| `is_pro` | false |
| `timezone` | 요청값 or `UTC` |
| `terms_agreed_at`/`privacy_agreed_at` | `*_agreed=true` 시 now(), else NULL |

- `provider_id` 조회 — 있으면 로그인, 없으면 신규
- 기존 로그인 시 `apply_lazy_expiry` 호출. 신규 가입은 호출 안 함(trial_start_date=NULL)
- Apple: 첫 로그인 시만 이름 제공 → 이후 `name=null` 이면 기존값 유지

## FE Contract (모바일 온보딩)

| 화면 | 경로 | 설명 |
|---|---|---|
| 로그인 | `app/login.tsx` | Google Sign-In 버튼 (현재 단일 provider) |
| 온보딩 약관 | `app/onboarding/terms.tsx` | 약관·개인정보 동의 |
| 트라이얼 소개 | `app/onboarding/trial-intro.tsx` | 혜택 안내 + paywall 진입/건너뛰기 |
| Paywall | `app/paywall.tsx` | [[spec-008-mobile-revenuecat-integration|STL-SPEC-008]] |

### 전환 흐름
```
앱 시작 → RouteGuard
  ├─ 미로그인 → /login
  └─ 로그인 + terms_agreed_at=null → /onboarding/terms
/login: Google 성공 → is_new ? /onboarding/terms : /
/onboarding/terms: 동의 → /onboarding/trial-intro
/onboarding/trial-intro: 시작 → /paywall?source=onboarding / 나중에 → /
```

## Case Matrix (에지)

| 케이스 | 처리 |
|---|---|
| 기존 사용자(is_new=false) | 온보딩 건너뛰고 / |
| terms_agreed_at=null 상태 타 라우트 | RouteGuard → /onboarding/terms (login/legal 제외) |
| 약관 화면 하드웨어 백 | BackHandler 차단 |
| paywall 미로그인 | 로그인 유도 (redirect 없음) |
| paywall RC 미설정(staging) | mockPurchase 폴백 |
| token 만료/kid 불일치/refresh 변조 | 401 |

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/`.

| 계약 | 코드 근거 | 정합 |
|---|---|---|
| POST /auth/google | `backend/app/api/v1/auth.py:18-45`, `services/auth_service.py:46-62,160-192` | ✅ |
| POST /auth/apple (BE) | `backend/app/api/v1/auth.py:47-74`, `services/auth_service.py:65-114` (JWKS/kid/RS256/iss/aud, 캐시 무효화 재시도) | ✅ |
| POST /auth/refresh, 60분/30일 | `backend/app/api/v1/auth.py:77-92`, `services/jwt_service.py:12,24` | ✅ |
| 신규 초기값 free/NULL/false, lazy expiry 분기 | `services/auth_service.py:147-149,179-181,215-217` | ✅ |
| 모바일 Google 로그인 + 온보딩 라우팅 | `frontend/mobile/app/login.tsx:35-66`, `onboarding/terms.tsx`, `trial-intro.tsx`, RouteGuard `app/_layout.tsx:47-49` | ✅ |
| **모바일 Apple Sign-In** | `frontend/mobile/app/login.tsx` Google 단독, Apple 버튼/SDK/의존성·`/auth/apple` 호출 부재 | ❌ 미연동 |

## Open Questions

- **[gap, D3] 모바일 Apple Sign-In end-to-end 미연동** — backend `POST /api/auth/apple` 는 실제 Apple JWKS 검증까지 완전 구현(`auth_service.py:65-114`)이나, 모바일 `login.tsx` 는 Google 단독이며 Apple 버튼/`expo-apple-authentication` 의존성/`/auth/apple` 호출이 전혀 없음(grep 확인). 따라서 사용자는 Apple 로그인을 수행할 수 없음. iOS 심사상 Apple Sign-In 요구 가능성 있어 출시 전 모바일 연동 필요. (태스크 brief 의 "BE 미구현" 전제는 코드와 불일치 — 정정.)
