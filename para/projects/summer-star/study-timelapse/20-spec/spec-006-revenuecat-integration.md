---
type: spec
id: STL-SPEC-006
title: "RevenueCat 통합 API (Phase 2)"
status: in_dev
product: study-timelapse
created_at: 2026-05-09
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/spec
  - status/in_dev
links:
  baselines: []
  decisions:
    - "[[decision-015-receipt-verification-dual-path|STL-DEC-015]]"
    - "[[decision-017-refund-policy-store-delegation|STL-DEC-017]]"
    - "[[decision-019-grace-period-handling|STL-DEC-019]]"
    - "[[decision-020-webhook-auth-bearer|STL-DEC-020]]"
    - "[[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]"
    - "[[decision-022-status-source-cache-with-sync|STL-DEC-022]]"
  specs:
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-004-subscription-api|STL-SPEC-004]]"
    - "[[spec-005-subscription-data-model|STL-SPEC-005]]"
    - "[[spec-007-receipt-verification|STL-SPEC-007]]"
    - "[[spec-008-mobile-revenuecat-integration|STL-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# RevenueCat 통합 API (Phase 2)

Phase 2 RevenueCat 연동 REST 계약: verify / webhook / sync 3개 엔드포인트와 이벤트→상태 매핑. 이중 경로(verify + webhook=SoT, [[decision-015-receipt-verification-dual-path|STL-DEC-015]]), Bearer webhook 인증([[decision-020-webhook-auth-bearer|STL-DEC-020]]), grace period([[decision-019-grace-period-handling|STL-DEC-019]]), 취소/환불 전이([[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]), 강제 sync([[decision-022-status-source-cache-with-sync|STL-DEC-022]]).

> 원본: `medi_docs/current/spec/spec-06-revenuecat-integration.md`. 원본의 Python handler 본문·SQL DDL·sequence 의사코드는 30-work/구현 영역이라 제외. 엔드포인트·이벤트 매핑·인증 계약만 둔다.
>
> **status: in_dev** — verify/webhook/sync 엔드포인트와 5개 이벤트 분기는 구현됐으나, `INITIAL_PURCHASE` 의 `period_type` TRIAL/NORMAL 분기(아래 §이벤트 매핑)가 코드에 미구현이다(아래 Open Questions).

## Context

- 관련 decision: 이중 경로 검증([[decision-015-receipt-verification-dual-path|STL-DEC-015]]), 스토어 환불 위임([[decision-017-refund-policy-store-delegation|STL-DEC-017]]), grace period([[decision-019-grace-period-handling|STL-DEC-019]]), Bearer 인증([[decision-020-webhook-auth-bearer|STL-DEC-020]]), 취소 vs 환불([[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]), 캐시+sync([[decision-022-status-source-cache-with-sync|STL-DEC-022]])
- 짝 spec: 검증 흐름 [[spec-007-receipt-verification|STL-SPEC-007]] (handler 상세), mobile SDK [[spec-008-mobile-revenuecat-integration|STL-SPEC-008]]
- 공통: 응답 `{success, data|error}`, 타임스탬프 ISO 8601 UTC. product = `com.kknaks.studytimelapse.monthly`

## BE Contract

| 엔드포인트 | 인증 | 목적 |
|---|---|---|
| `POST /api/subscription/verify` | User JWT | 구매 직후 client → backend 즉시 갱신 (경로 A) |
| `POST /api/subscription/webhook` | Bearer (`REVENUECAT_WEBHOOK_AUTH_TOKEN`) | RevenueCat push 이벤트 (경로 B, SoT) |
| `POST /api/subscription/sync` | User JWT | 사용자 강제 sync (RevenueCat 직접 조회) |

### POST /verify
- Request: `{ app_user_id, transaction_id, product_identifier }`
- 멱등: `transaction_id` 이미 처리 → `idempotent:true`. 위조 방어: backend 가 RevenueCat `GET /subscribers/{id}` 재확인 → entitlement 없으면 422
- 에러: 403 `USER_MISMATCH`(JWT≠app_user_id), 422 `REVENUECAT_VERIFICATION_FAILED`, 429 `RATE_LIMITED`
- 재시도: network/5xx 시 client 1회 재시도 후 webhook 대기 안내

### POST /webhook
- 인증: `Authorization: Bearer` 불일치 → 401. ENV 미설정 시 라우터 미등록
- 멱등: `event.id` 중복 → 200 `idempotent:true`. unknown `app_user_id` → 경고 로그 + 200 (재시도 방지)
- 응답: 모든 정상 처리 200 OK

### POST /sync
- Request: body 없음(JWT에서 user_id). RevenueCat 직접 조회 → 갱신
- 쿨다운 30초, 초과 시 429 `RATE_LIMITED`

## 이벤트 매핑 (RevenueCat event.type → 상태)

| event.type | event_type | 상태 전이 | grace_until |
|---|---|---|---|
| `INITIAL_PURCHASE` | `purchased` (또는 `trial_started`) | → pro (period_type=TRIAL이면 → trial) | NULL |
| `RENEWAL` | `renewed` | pro 유지 | NULL |
| `CANCELLATION` | `cancel_scheduled` | → cancelled (pro_until 까지 Pro) | — |
| `EXPIRATION` | `expired` | → expired | NULL |
| `BILLING_ISSUE` | `billing_issue` | pro 유지 | `grace_period_expiration_at` ([[decision-019-grace-period-handling|STL-DEC-019]]) |
| `REFUND` | `refunded` | → cancelled (즉시), `pro_until = now()` ([[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]) | NULL |

> `INITIAL_PURCHASE` 의 `event.period_type` 분기 (TRIAL→trial / NORMAL→pro, [[decision-016-introductory-offer-and-auto-renewal|STL-DEC-016]]): 명세에 있으나 **코드 미구현** — Open Questions.

## 인증·멱등 (보안)

- webhook: `event_id` UNIQUE partial 인덱스 → 중복 INSERT 불가 ([[spec-005-subscription-data-model|STL-SPEC-005]])
- verify: `transaction_id` UNIQUE partial 인덱스
- Bearer 토큰 유출 시 RevenueCat 대시보드에서 교체. HTTPS 강제

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/backend/`.

| 계약 | 코드 근거 | 정합 |
|---|---|---|
| verify (멱등/USER_MISMATCH/422) | `app/api/v1/subscription.py:48-68`, `app/services/subscription_handler.py:83-129` | ✅ |
| webhook (Bearer/멱등/unknown 200/ENV 게이트) | `app/api/v1/subscription.py:86-103`, `app/main.py:32-35`, handler `:132-206` | ✅ |
| sync (JWT/30초 쿨다운) | `app/api/v1/subscription.py:71-83`, handler `:209-249` | ✅ |
| 이벤트 분기 5종(RENEWAL/CANCELLATION/EXPIRATION/BILLING_ISSUE/REFUND) | `app/services/subscription_handler.py:160-190` | ✅ |
| RevenueCat client (GET /subscribers) | `app/integrations/revenuecat.py:35-53` | ✅ |
| **INITIAL_PURCHASE period_type 분기** | `app/schemas/subscription.py:14-23` (필드 없음), handler `:160-165` (항상 pro) | ❌ 미구현 |

## Open Questions

- **[gap] `INITIAL_PURCHASE` period_type 분기 미구현** — `RevenueCatWebhookEvent` 스키마에 `period_type` 필드 부재(`subscription.py:14-23`), 핸들러는 INITIAL_PURCHASE 를 항상 `pro`/`purchased` 로 처리(`subscription_handler.py:160-165`). RevenueCat introductory offer(trial) 구매가 backend 에서 `pro` 로 기록됨 → Phase 2 store-trial 경로가 명세대로 동작하지 않음. period_type 분기 구현 필요 ([[decision-016-introductory-offer-and-auto-renewal|STL-DEC-016]]).
- verify rate-limit(5회/분)은 명세에 있으나 미구현 ([[spec-007-receipt-verification|STL-SPEC-007]] OQ와 동일).
