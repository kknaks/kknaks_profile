---
type: decision
id: STL-DEC-021
title: "취소 vs 환불 상태 전환 — 환불=즉시 cancelled, 취소=만료일까지 Pro 유지"
status: accepted
product: study-timelapse
created_at: 2026-05-09
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions:
    - "[[decision-010-subscription-state-model|STL-DEC-010]]"
    - "[[decision-017-refund-policy-store-delegation|STL-DEC-017]]"
    - "[[decision-019-grace-period-handling|STL-DEC-019]]"
    - "[[decision-022-status-source-cache-with-sync|STL-DEC-022]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 취소 vs 환불 상태 전환 (ADR-21)

RevenueCat 이벤트 유형에 따라 상태 전환을 분기한다. 환불(`REFUND`) = 즉시 `cancelled` + `pro_until=현재시각`. 자발적 취소(`CANCELLATION`) = `cancelled` 기록 + `pro_until` 만료까지 Pro 기능 유지.

> 원본: `study_timelapse/medi_docs/current/adr/adr-21-cancel-vs-refund-state-transition.md`. D-PLAN-2-10. Phase 2.

## Context

- 5상태 ENUM 의 `cancelled` 하나로 환불과 자발적 취소를 동일 처리하면 사용자 경험 차이 발생.
- 자발적 취소는 만료일까지 Pro 유지가 스토어 표준. 환불은 영수증 무효 → 즉시 전환 원칙.

## Options

| Option | 환불 | 취소 | 비고 |
|---|---|---|---|
| A | 즉시 전환 | 즉시 전환 | 취소 시 만료 전 Pro 박탈 → 반발 |
| B (채택) | 즉시 cancelled | 만료일까지 Pro 유지 | 구분 처리, 스토어 표준 |
| C | 만료일까지 유지 | 만료일까지 유지 | 환불 후 무임승차 |

## Decision

**B 채택.**

- `REFUND` → `cancelled` 즉시 + `pro_until=현재시각`(Pro 즉시 박탈).
- `CANCELLATION`(자발적) → `cancelled` 기록 + `pro_until` 유지 → 만료 시 lazy expiry → `expired`.
- Pro 판단: `is_active_pro` = pro / (cancelled and pro_until>now) / trial.
- 감사: `event_type='refund'` vs `'cancellation'` 으로 구분.

## 구현 현황

- 정합. `backend/app/services/subscription.py:36` — `if subscription_status == "cancelled" and pro_until is not None` 분기, `:92-94` `pro` + `pro_until<now` → `expired` lazy expiry.
- `subscription_event.py:19` event_type CHECK 에 refund/cancelled 포함.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | `GET /users/me` `is_pro` 의 cancelled+pro_until>now 분기 명세 | — | spec 단계 |
