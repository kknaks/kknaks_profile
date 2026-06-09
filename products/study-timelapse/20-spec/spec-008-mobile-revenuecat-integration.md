---
type: spec
id: STL-SPEC-008
title: "Mobile RevenueCat SDK 통합 (Phase 2)"
status: implemented
product: study-timelapse
created_at: 2026-05-09
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/spec
  - status/implemented
links:
  baselines: []
  decisions:
    - "[[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]"
    - "[[decision-016-introductory-offer-and-auto-renewal|STL-DEC-016]]"
    - "[[decision-018-app-user-id-mapping|STL-DEC-018]]"
    - "[[decision-022-status-source-cache-with-sync|STL-DEC-022]]"
  specs:
    - "[[spec-006-revenuecat-integration|STL-SPEC-006]]"
    - "[[spec-004-subscription-api|STL-SPEC-004]]"
  works: []
  releases: []
  related: []
---

# Mobile RevenueCat SDK 통합 (Phase 2)

`react-native-purchases` SDK 기반 mobile 통합 계약: SDK 초기화, logIn 시점([[decision-018-app-user-id-mapping|STL-DEC-018]]), 온보딩 trial 안내, paywall 구매 흐름, introductory offer([[decision-016-introductory-offer-and-auto-renewal|STL-DEC-016]]), grace 배너, 강제 sync([[decision-022-status-source-cache-with-sync|STL-DEC-022]]).

> 원본: `medi_docs/current/spec/spec-08-mobile-revenuecat-integration.md`. 원본의 TS 컴포넌트/훅 구현 본문은 30-work 영역이라 제외. 화면 흐름·SDK 호출 시점·상태 계약만 둔다.

## Context

- 관련 decision: anonymous paywall + 로그인 유도([[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]), introductory offer 7일 + 자동 갱신([[decision-016-introductory-offer-and-auto-renewal|STL-DEC-016]]), app_user_id 매핑([[decision-018-app-user-id-mapping|STL-DEC-018]]), 캐시+sync([[decision-022-status-source-cache-with-sync|STL-DEC-022]])
- 짝 spec: backend API [[spec-006-revenuecat-integration|STL-SPEC-006]], Phase 1 API [[spec-004-subscription-api|STL-SPEC-004]]
- product: `com.kknaks.studytimelapse.monthly`

## FE Contract

### SDK 초기화 / logIn
- `Purchases.configure({ apiKey })` (`EXPO_PUBLIC_REVENUECAT_*_API_KEY`), app 최상위 layout
- `Purchases.logIn(user.id)` — 인증 성공 직후 + 토큰 복원 재진입 시 ([[decision-018-app-user-id-mapping|STL-DEC-018]]). web/미설정 시 no-op
- Anonymous 사용자: 로그인 전 logIn 호출 없음. paywall 도달 시 로그인 유도 ([[decision-013-anonymous-paywall-and-terms|STL-DEC-013]])

### 온보딩 trial 안내 흐름 ([[decision-016-introductory-offer-and-auto-renewal|STL-DEC-016]])
```
가입(free) → onboarding/terms → onboarding/trial-intro
  ├─ [7일 무료 체험 시작] → /paywall?source=onboarding → purchasePackage
  └─ [나중에] → / (Free 1회/일)
```
- 가입 시 trial 자동 시작 없음(`free`). trial 진입은 store introductory offer 로만 ([[spec-003-subscription-state-machine|STL-SPEC-003]])

### paywall 구매 흐름
| 단계 | 계약 |
|---|---|
| Offerings | `Purchases.getOfferings()` → current |
| intro 자격 | `checkTrialOrIntroductoryPriceEligibility` → 배지 표시 |
| 구매 | `Purchases.purchasePackage(monthly)` |
| verify | `POST /verify` 1회 재시도, 실패 시 "잠시 후 자동 갱신" 안내 ([[spec-006-revenuecat-integration|STL-SPEC-006]]) |
| 갱신 | `invalidateQueries(['me'])` → Pro UI |
| staging fallback | RC 미설정/web → `mockPurchase('monthly')` |

### useSubscription 훅 / 강제 sync
- 필드: `graceUntil`, `isGracePeriod`, `graceUntilApproaching`(또는 isGraceApproaching), `showWatermark`(Free), `showProgressBar`(Pro/Trial)
- grace 배너: `isGracePeriod` 시 결제수단 관리 링크
- 강제 sync: 설정/stats 에서 `POST /sync` + invalidate, 429 시 쿨다운 안내 ([[decision-022-status-source-cache-with-sync|STL-DEC-022]])

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/frontend/mobile/` (`react-native-purchases ^10.1.0`, `package.json:33`). 전 계약 코드 정합 — gap 없음.

| 계약 | 코드 근거 |
|---|---|
| SDK init | `src/lib/purchases.ts:10-27`, `app/_layout.tsx:56-58` |
| logIn | `src/lib/purchases.ts:29-36`, `app/_layout.tsx:36-41` |
| trial-intro 흐름 | `app/onboarding/trial-intro.tsx` 존재, `app/onboarding/terms.tsx:31` → trial-intro 라우팅 |
| paywall (purchasePackage + verify 1재시도 + mock fallback) | `app/paywall.tsx:43-60,96-140` |
| api 함수 | `src/api/subscription.ts:23-30` (mock/verify/sync) |
| useSubscription | `src/hooks/useSubscription.ts:31-67` (grace/watermark/progress) |
| 강제 sync UI | `app/stats.tsx:83-101,462` (30초 쿨다운) |

## Open Questions

- 없음 (mobile 경로 end-to-end 구현·배포). 단, backend 의 `INITIAL_PURCHASE` period_type trial 분기 미구현이라([[spec-006-revenuecat-integration|STL-SPEC-006]] OQ) store introductory offer 구매가 backend 에서 trial 로 기록되지 않는 점은 backend 측 gap.
