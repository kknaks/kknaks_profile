---
type: spec
id: STL-SPEC-004
title: "구독 API 계약 (Phase 1)"
status: implemented
product: study-timelapse
created_at: 2026-05-06
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/spec
  - status/implemented
links:
  baselines: []
  decisions:
    - "[[decision-010-subscription-state-model|STL-DEC-010]]"
    - "[[decision-012-mock-purchase-api-and-events|STL-DEC-012]]"
    - "[[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]"
  specs:
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-005-subscription-data-model|STL-SPEC-005]]"
    - "[[spec-006-revenuecat-integration|STL-SPEC-006]]"
  works: []
  releases: []
  related: []
---

# 구독 API 계약 (Phase 1)

Phase 1 구독 REST API 의 Request·Response·에러 계약. mock-purchase 기반 구독 전환([[decision-012-mock-purchase-api-and-events|STL-DEC-012]]) + 약관 동의([[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]). Phase 2 에서 내부 구현만 RevenueCat 으로 교체([[spec-006-revenuecat-integration|STL-SPEC-006]]).

> 원본: `medi_docs/current/spec/spec-04-subscription-api.md`. 원본의 OpenAPI 스니펫·"409 vs 200" 구현 선택 deliberation 은 결정/구현 영역이라 제외. 확정 계약(엔드포인트·필드·에러코드)만 둔다.

## Context

- 관련 decision: mock-purchase API + 이벤트 소싱([[decision-012-mock-purchase-api-and-events|STL-DEC-012]]), anonymous paywall + 약관([[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]), 5상태 모델([[decision-010-subscription-state-model|STL-DEC-010]])
- 짝 spec: 상태 머신 [[spec-003-subscription-state-machine|STL-SPEC-003]], 데이터 모델 [[spec-005-subscription-data-model|STL-SPEC-005]]
- 공통: 인증 `Authorization: Bearer <JWT>`, 미인증 401. 타임스탬프 ISO 8601 UTC.

## BE Contract

| 엔드포인트 | 목적 | 인증 |
|---|---|---|
| `POST /api/subscription/mock-purchase` | paywall "구매" → Pro 전환 | JWT |
| `POST /admin/debug/subscription` | 상태 강제 전환 (QA) | JWT + ENV 가드 |
| `GET /api/users/me` (확장) | 구독 상태 + 일일 한도 + 배너 | JWT |
| `PUT /api/users/me/terms-agree` | 약관 동의 기록 | JWT |

### POST /api/subscription/mock-purchase

- Request: `{ "plan": "monthly" }` (`monthly` 만 허용, [[decision-011-monthly-only-no-yearly|STL-DEC-011]])
- 멱등: 이미 `pro` + `pro_until > now()` 이면 신규 이벤트 없이 현재 상태 반환 (`idempotent: true`). `trial`/`expired` → 정상 구매 (`idempotent: false`)
- Side-effect: `subscription_events` INSERT(`purchased`/`mock`/`monthly`/`amount_cents=199`) + `User` 상태 갱신(원자적)

| HTTP | code | 조건 |
|---|---|---|
| 400 | `INVALID_PLAN` | plan ≠ monthly |
| 402 | `TERMS_NOT_AGREED` | `terms_agreed_at IS NULL` |

### POST /admin/debug/subscription

- ENV 가드: `ALLOW_DEBUG_SUBSCRIPTION` 일 때만 라우터 등록 (미설정 → 라우트 부재). prod 설정 금지.
- Request: `{ user_id, target_status, note? }` (`target_status` ∈ 5상태)
- Side-effect: `subscription_events` INSERT(`source='admin'`) + 상태 강제 갱신

### GET /api/users/me (확장 필드)

| 필드 | 타입 | 설명 |
|---|---|---|
| `subscription_status` | enum | 5상태 |
| `trial_start_date` | date\|null | |
| `pro_until` | datetime\|null | |
| `is_pro` | bool | 상태 캐시 |
| `timezone` | string | IANA, 기본 `UTC` |
| `terms_agreed_at` / `privacy_agreed_at` | datetime\|null | |
| `daily_session_count` | int | 사용자 로컬 오늘 완료 세션 수 |
| `daily_quota` | int | trial/pro = -1(무제한), free/expired = 1 |
| `daily_quota_resets_at` | datetime | 사용자 로컬 자정(UTC 변환) |
| `banner_alert` | string\|null | `trial_expiring_24h`/`trial_expiring_1h`/`trial_expired`/`subscription_expired`/null |

- Lazy 만료: `trial`/`pro` 만료 조건이면 응답 전 갱신 후 갱신된 상태 반환 ([[spec-003-subscription-state-machine|STL-SPEC-003]])

### PUT /api/users/me/terms-agree

- Request: `{ terms_agreed: bool, privacy_agreed: bool }` (둘 다 true 여야 유효)
- Response: `UserResponseV2` (GET /me 동일 포맷). 재호출 시 시각 갱신 (멱등)
- 에러: `400 INVALID_AGREEMENT` (둘 중 하나라도 false)

## Case Matrix (에러 코드)

| Code | HTTP | 설명 |
|---|---|---|
| `INVALID_PLAN` | 400 | mock-purchase plan ≠ monthly |
| `TERMS_NOT_AGREED` | 402 | 약관 미동의 구매 시도 |
| `INVALID_AGREEMENT` | 400 | terms-agree false 포함 |
| `DAILY_QUOTA_EXCEEDED` | 403 | 세션 시작 한도 초과 ([[spec-010-session-domain|STL-SPEC-010]]) |
| `UNAUTHORIZED` | 401 | 토큰 없음/만료 |

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/backend/`. 전 엔드포인트·필드·에러 코드 코드 정합.

| 계약 | 코드 근거 |
|---|---|
| mock-purchase | `app/api/v1/subscription.py:31-45`, 멱등 `app/services/subscription.py:122-146`, 에러 `app/exceptions.py:45-57` |
| debug API (ENV 가드) | `app/api/v1/admin/debug.py:28-53`, `app/main.py:27-30` (`allow_debug_subscription`) |
| GET /me 확장 필드 | `app/api/v1/users.py:29-81`, `app/schemas/user.py:28-54`, banner_alert `app/services/subscription.py:52-66` |
| terms-agree | `app/api/v1/users.py:84-146` |

## Open Questions

- mock-purchase 의 prod ENV 가드(`ENABLE_MOCK_PURCHASE=false`)는 **Phase 2 요구**([[spec-006-revenuecat-integration|STL-SPEC-006]] §개요)이며 현재 코드에 미적용 — Phase 2 게이트 시 추가 필요. Phase 1 계약 자체는 ungated 가 정상.
