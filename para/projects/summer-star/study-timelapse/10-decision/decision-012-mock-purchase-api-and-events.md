---
type: decision
id: STL-DEC-012
title: "mock-purchase API + 이벤트 소싱 (전용 API / append-only / source 컬럼)"
status: accepted
product: study-timelapse
created_at: 2026-05-06
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions:
    - "[[decision-010-subscription-state-model|STL-DEC-010]]"
    - "[[decision-011-monthly-only-no-yearly|STL-DEC-011]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - application-event
  - immutability
  - externalized-configuration
---

# mock-purchase API + 이벤트 소싱 (ADR-12)

Phase 1 결제 트리거는 전용 `POST /api/subscription/mock-purchase`. 결제 이력은 `subscription_events` 에 append-only 이벤트 소싱. Phase 2 RevenueCat 이력은 `source="revenuecat"` 컬럼으로 동일 테이블에 혼재.

> 원본: `study_timelapse/medi_docs/current/adr/adr-12-mock-purchase-api-and-events.md`. D-PLAN-1/5/6 통합.

## Context

- Phase 1: 스토어 SDK 없이 backend 가 직접 구독 상태 mock. Phase 2: RevenueCat webhook → 동일 테이블.
- 결제 이력 보존(감사·환불 분쟁), debug 강제 전환 API 의 prod 노출 위험 방지.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[application-event]] — 결제 이력을 상태가 아니라 **일어난 사건의 나열**로 쌓는다(`event_type`·`occurred_at`·`raw_payload`). 현재 상태만 두면 어떻게 그렇게 됐는지 알 수 없다
- [[immutability]] — `subscription_events` 는 **append-only** — UPDATE·DELETE 를 금지해 이력이 사후에 바뀌지 않게 한다
- [[externalized-configuration]] — 디버그 엔드포인트를 `ENABLE_DEBUG_SUBSCRIPTION` 로 끄고 운영에서 404 로 만든다 — 코드가 아니라 환경이 노출 여부를 정한다

## Options

| 축 | 채택안 | 대안 |
|---|---|---|
| 결제 트리거 (D-PLAN-1) | A: 전용 mock-purchase API | B: debug API 재사용 / C: 어드민 API 재사용 |
| 이력 범위 (D-PLAN-5) | A: 모든 이벤트 append-only | B: 성공 거래만 / C: 1행 upsert |
| mock→real (D-PLAN-6) | A: 이력 보존 + source 컬럼 | B: 폐기 / C: 별도 테이블 |

## Decision

**세 축 모두 A 채택.**

- `POST /api/subscription/mock-purchase`(JWT 필수, 멱등). Phase 2 전환 시 내부 구현만 교체.
- `POST /admin/debug/subscription`(스테이지 전용, `ENABLE_DEBUG_SUBSCRIPTION=false` 시 prod 404).
- `subscription_events`: append-only(UPDATE/DELETE 금지), `event_type / source / plan / amount_cents / occurred_at / raw_payload`.

## 구현 현황

- 정합. `backend/app/models/subscription_event.py:16` 테이블, `:19` event_type CHECK, `:25` `source IN ('mock','revenuecat','admin','system')`, `:45` amount_cents.
- `backend/app/api/v1/subscription.py:36` `mock_purchase` 엔드포인트. debug API: `backend/app/api/v1/admin/`.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | `User.is_pro / pro_until` 캐시 vs events reduce read 전략 | — | subscription-data-model spec |
