---
type: spec
id: STL-SPEC-007
title: "영수증 검증 흐름 (Phase 2)"
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
    - "[[decision-015-receipt-verification-dual-path|STL-DEC-015]]"
    - "[[decision-017-refund-policy-store-delegation|STL-DEC-017]]"
    - "[[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]"
    - "[[decision-022-status-source-cache-with-sync|STL-DEC-022]]"
  specs:
    - "[[spec-006-revenuecat-integration|STL-SPEC-006]]"
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-005-subscription-data-model|STL-SPEC-005]]"
  works: []
  releases: []
  related: []
---

# 영수증 검증 흐름 (Phase 2)

RevenueCat customer info 를 신뢰원으로 사용하는 backend 영수증 검증 계약. backend 는 Apple/Google 영수증을 직접 검증하지 않고 RevenueCat 이 server-side 검증 완료한 customer info 를 신뢰([[decision-015-receipt-verification-dual-path|STL-DEC-015]]). webhook 이벤트 처리·보안·멱등 규칙.

> 원본: `medi_docs/current/spec/spec-07-receipt-verification.md`. 원본의 Python handler/helper 본문(의사코드)은 30-work 영역이라 제외. 검증 전략·보안·멱등 계약만 둔다. [[spec-006-revenuecat-integration|STL-SPEC-006]]의 backend 상세 짝.

## Context

- 관련 decision: 이중 경로 검증([[decision-015-receipt-verification-dual-path|STL-DEC-015]]), 스토어 환불 위임([[decision-017-refund-policy-store-delegation|STL-DEC-017]]), 취소 vs 환불([[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]), 캐시+sync([[decision-022-status-source-cache-with-sync|STL-DEC-022]])
- 짝 spec: API 계약 [[spec-006-revenuecat-integration|STL-SPEC-006]] (이 spec 은 backend 전용; mobile 은 [[spec-008-mobile-revenuecat-integration|STL-SPEC-008]])

## BE Contract (검증 전략)

| 항목 | 규칙 |
|---|---|
| 신뢰원 | RevenueCat customer info. backend 가 Apple/Google 직접 검증 안 함 |
| 위조 방어 | verify 시 backend 가 `GET /subscribers/{app_user_id}` 재조회 → `entitlements.active` 없으면 422. client 값 그대로 신뢰 안 함 |
| Pro 판정 | `is_active_pro(user)`: status∈(trial,pro) OR (cancelled AND pro_until>now) |
| grace 판정 | `is_grace_period(user)`: `grace_until > now()` (status='pro' 유지, 6번째 상태 없음, [[decision-019-grace-period-handling|STL-DEC-019]]) |

## webhook 처리 계약

| 단계 | 규칙 |
|---|---|
| 멱등 | `event.id` 존재 시 200 `idempotent:true` |
| unknown user | `app_user_id` 매핑 실패 → 경고 로그 + 200 (재시도 방지) |
| 이벤트 분기 | 6종 ([[spec-006-revenuecat-integration|STL-SPEC-006]] 이벤트 매핑 표) |
| 환불 | REFUND → cancelled 즉시, `pro_until = now()` ([[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]) |
| grace | BILLING_ISSUE → `grace_until` 설정, status pro 유지 |
| 시각 파싱 | ms epoch → UTC datetime |
| 금액 추출 | `price` 필드 → cents (×100) |

## Validation (보안)

| 항목 | 규칙 |
|---|---|
| webhook 인증 | `Bearer <REVENUECAT_WEBHOOK_AUTH_TOKEN>`, 불일치 401, HTTPS 강제 ([[decision-020-webhook-auth-bearer|STL-DEC-020]]) |
| 멱등 인덱스 | `event_id`/`transaction_id` UNIQUE partial — 중복 INSERT 불가 |
| rate limit | verify 5회/분, sync 30초 쿨다운 |

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/backend/`.

| 계약 | 코드 근거 | 정합 |
|---|---|---|
| RevenueCat 신뢰(직접검증 없음) | `app/services/subscription_handler.py:83-129` (Apple/Google 직접 호출 없음, `get_customer_info`만) | ✅ |
| webhook 멱등/unknown 200/6분기/_parse_ms/_extract_amount_cents | `subscription_handler.py:132-206`, `:60-70` | ✅ |
| is_active_pro / is_grace_period / grace_until | `app/services/subscription.py:123-127`, `app/models/user.py:43`, set `subscription_handler.py:178` | ✅ |
| Bearer 인증 / UNIQUE 인덱스 | `app/api/v1/subscription.py:97-99`, 마이그 `004_*.py:37-50` | ✅ |
| sync 30초 쿨다운 | `subscription_handler.py:220-224` | ✅ |
| **verify 5회/분 rate-limit** | (검증 범위 내 미발견) | ❌ 미구현 |

## Open Questions

- **[gap] verify 엔드포인트 rate-limit(5회/분) 미구현** — sync 만 30초 쿨다운 존재(`subscription_handler.py:220-224`), verify(`:83-129`)에는 rate-limit 없음. 핵심 검증 계약은 구현됐으나 남용 방어 하드닝 미완 → 추가 권장. (sync 쿨다운은 in-memory 라 서버 재시작 시 리셋 — 분산 환경 시 외부 store 필요.)
