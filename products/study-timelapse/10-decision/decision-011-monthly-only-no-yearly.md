---
type: decision
id: STL-DEC-011
title: "월 only $1.99 — 연 플랜 폐기"
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
    - "[[decision-012-mock-purchase-api-and-events|STL-DEC-012]]"
    - "[[decision-014-phase1-execution-strategy|STL-DEC-014]]"
  specs: []
  works: []
  releases: []
  related: []
up: []
---

# 월 only $1.99 — 연 플랜 폐기 (ADR-11)

월+연 2-tier 권장을 폐기하고 월 $1.99 단일 플랜으로 확정한다. 연 플랜 미운영.

> 원본: `study_timelapse/medi_docs/current/adr/adr-11-monthly-only-no-yearly.md`. 원본 planning-02 §D-PLAN-8(월+연 2-tier) 권장을 supersede 한다.

## Context

- 기존 권장: 월+연 2-tier(월 $2.99/연 $19.99 잠정). `paywall.tsx` 도 동일 하드코딩.
- 연 가격 미확정 → Phase 2 App Store Connect 등록 차단 요소.
- 사용자 비즈니스 결정: 연 플랜 미운영 확정.

## 근거 개념

없음 — 플랜과 가격을 정한 제품 결정이다.

## Options

| Option | 구성 | 장점 | 단점 |
|---|---|---|---|
| A | 월+연 2-tier ($2.99/$19.99) | 연 업셀 | 연 가격 미확정 → App Store 차단 |
| B (채택) | 월 only ($1.99/월) | paywall 단순, 단일 상품, 결정 부담 없음 | 장기 가입 인센티브 없음 |
| C | 평생 license (one-time) | 단건 수익 | 구독 전환 복잡, Phase 1 초과 |

## Decision

**B 채택 — 월 $1.99 단일 플랜.**

- paywall 단일 CTA, `subscription_events.plan` ENUM = `monthly` 만.
- App Store Connect 차단 요소(연 가격) 제거로 Phase 2 진입 가속.
- 연 플랜 추가는 Phase 3+ 별도 결정.

## 구현 현황

- 정합. `backend/app/models/subscription_event.py:29` — CHECK `plan IN ('monthly')`.
- `frontend/mobile/app/paywall.tsx:21` `MONTHLY_PRODUCT_ID`, `:97` `mockPurchase('monthly')` — 연 플랜 UI/로직 없음.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |
