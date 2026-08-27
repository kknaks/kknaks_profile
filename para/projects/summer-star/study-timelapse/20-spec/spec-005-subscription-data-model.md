---
type: spec
id: STL-SPEC-005
title: "구독 데이터 모델"
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
    - "[[decision-011-monthly-only-no-yearly|STL-DEC-011]]"
    - "[[decision-012-mock-purchase-api-and-events|STL-DEC-012]]"
    - "[[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]"
  specs:
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-004-subscription-api|STL-SPEC-004]]"
    - "[[spec-006-revenuecat-integration|STL-SPEC-006]]"
  works: []
  releases: []
  related: []
---

# 구독 데이터 모델

구독 DB 계약: User 컬럼 확장 + `subscription_events` append-only 테이블 + `daily_focus` 정합성([[decision-010-subscription-state-model|STL-DEC-010]], [[decision-012-mock-purchase-api-and-events|STL-DEC-012]]).

> 원본: `medi_docs/current/spec/spec-05-subscription-data-model.md`. 원본의 Alembic 마이그레이션 스켈레톤·시드 코드·ENUM vs VARCHAR deliberation 은 구현/결정 영역이라 제외. 테이블·컬럼·제약·인덱스 계약만 둔다.

## Context

- 관련 decision: 5상태 모델([[decision-010-subscription-state-model|STL-DEC-010]]), 월 only([[decision-011-monthly-only-no-yearly|STL-DEC-011]]), 이벤트 소싱([[decision-012-mock-purchase-api-and-events|STL-DEC-012]]), 약관 컬럼([[decision-013-anonymous-paywall-and-terms|STL-DEC-013]])
- 짝 spec: 상태 머신 [[spec-003-subscription-state-machine|STL-SPEC-003]], API [[spec-004-subscription-api|STL-SPEC-004]]

## Data Contract

### User 컬럼

| 컬럼 | 타입 | NULL | 기본 | 비고 |
|---|---|:---:|---|---|
| `subscription_status` | VARCHAR(20) + CHECK | NOT NULL | `free` | `free/trial/pro/expired/cancelled` |
| `trial_start_date` | DATE | NULL | NULL | Phase 2 신규=NULL |
| `is_pro` | BOOLEAN | NOT NULL | false | 상태 캐시 |
| `pro_until` | TIMESTAMP | NULL | NULL | |
| `grace_until` | TIMESTAMP | NULL | NULL | RevenueCat billing issue ([[spec-006-revenuecat-integration|STL-SPEC-006]]) |
| `timezone` | VARCHAR(50) | NOT NULL | `UTC` | IANA, daily_focus 날짜 기준 |
| `terms_agreed_at` | TIMESTAMP | NULL | NULL | |
| `privacy_agreed_at` | TIMESTAMP | NULL | NULL | |

> `is_pro` 는 `subscription_status` 캐시. 항상 동기: trial/pro→true, free/expired→false, cancelled→`pro_until>now()`면 true.

### subscription_events 테이블 (append-only)

| 컬럼 | 타입 | 비고 |
|---|---|---|
| `id` | UUID PK | gen_random_uuid() |
| `user_id` | UUID FK | ON DELETE CASCADE |
| `event_type` | VARCHAR(30) CHECK | `trial_started/trial_expired/purchased/renewed/expired/cancelled/refunded` (+ Phase 2 `cancel_scheduled/billing_issue`) |
| `source` | VARCHAR(20) CHECK | `mock/revenuecat/admin/system` |
| `plan` | VARCHAR(20) CHECK | `monthly` |
| `amount_cents` | INTEGER NULL | mock purchased/renewed=199, system/admin=NULL |
| `currency` | VARCHAR(3) NULL | 기본 USD |
| `occurred_at` | TIMESTAMP | 기본 now() |
| `raw_payload` | JSONB NULL | webhook 원본 |
| `event_id` | VARCHAR(100) NULL | Phase 2 webhook 멱등 (UNIQUE partial) |
| `transaction_id` | VARCHAR(100) NULL | Phase 2 verify 멱등 (UNIQUE partial) |
| `created_at` | TIMESTAMP | 기본 now() |

- append-only: repository 는 `create()`/`list()` 만. UPDATE/DELETE 없음 (I5, [[spec-003-subscription-state-machine|STL-SPEC-003]])
- 인덱스: `(user_id, occurred_at DESC)`, `(event_type, occurred_at)`, `(source)`, UNIQUE `(event_id)`/`(transaction_id)` partial

## Validation (daily_focus 정합성)

- 일일 한도 진실 원천 = `daily_focus (user_id, 사용자_로컬_오늘)` 의 `session_count`
- `daily_focus.date` = **사용자 timezone 로컬 날짜** (서버 UTC `date.today()` 아님)
- 기존 UTC 레코드: `timezone='UTC'` 기본값 사용자는 기존과 동일 동작. 신규는 로컬 날짜 기준

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/backend/`. 전 컬럼·테이블·제약·인덱스 코드 정합 — gap 없음.

| 계약 | 코드 근거 |
|---|---|
| User 컬럼 | `app/models/user.py:18-45`; 마이그 001(status,trial), 002(is_pro,pro_until), 003(timezone,terms,privacy,CHECK), 004(grace_until) |
| subscription_events | `app/models/subscription_event.py:13-60`, 마이그 `003_*.py:47-108` + `004_*.py:22-64` (event_id/transaction_id) |
| append-only | `app/repositories/subscription_event.py:18-46` (create/list 만) |
| 인덱스 | `003_*.py:96-107`, UNIQUE partial `004_*.py:37-50` |
| amount_cents | `app/services/subscription.py:160` (199), admin=None |
| daily_focus 로컬 날짜 | `app/api/v1/sessions.py:55-58,242` (ZoneInfo) |

## Open Questions

- 없음 (구현·배포 완료).
