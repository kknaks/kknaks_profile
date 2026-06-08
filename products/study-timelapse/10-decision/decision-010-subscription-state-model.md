---
type: decision
id: STL-DEC-010
title: "구독 상태 모델 — 5상태 머신 + timezone 리셋 + 트라이얼 재사용 방지 deferred"
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
    - "[[decision-011-monthly-only-no-yearly|STL-DEC-011]]"
    - "[[decision-012-mock-purchase-api-and-events|STL-DEC-012]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 구독 상태 모델 — 5상태 머신 + timezone 리셋 + 트라이얼 재사용 방지 deferred (ADR-10)

`free / trial / pro / expired / cancelled` 5상태 머신을 Phase 1 스키마에 확정한다. 일일 한도 리셋은 사용자 로컬 자정(`User.timezone`) 기준, 트라이얼 재사용 방지는 Phase 1 deferred.

> 원본: `study_timelapse/medi_docs/current/adr/adr-10-subscription-state-model.md`. 결제 도메인 핵심 데이터 모델.

## Context

- 현행 `User.subscription_status` 는 3상태(free/trial/pro). Phase 2 RevenueCat 이벤트(active/expired/cancelled/in_grace_period)를 같은 머신으로 매핑해야 함.
- `daily_focus.session_count` 와 일일 한도 체크 연계 필요.

## Options

| Option | 상태 수 | Phase 2 호환 | 마이그레이션 |
|---|---|---|---|
| A | 3 (free/trial/pro) | ENUM 확장 마이그 필요 | O |
| B (채택) | 5 (free/trial/pro/expired/cancelled) | 완전 호환 | 없음 |
| C | 2 (free/pro) + trial 플래그 | 만료/취소 구분 모호 | O |

## Decision

**B 채택 — 5상태 머신 Phase 1 확정.**

- 상태별 Pro 기능·일일 한도: free/expired = 1회/일, trial/pro = 무제한, cancelled = 만료 전 무제한·후 1회/일.
- 일일 한도 리셋: `User.timezone` 기준 자정. 클라이언트 시계 신뢰 안 함.
- 트라이얼 재사용 방지: Phase 1 deferred → Phase 2 RevenueCat introductory offer eligibility 로 처리.

## 구현 현황

- 정합. `backend/app/models/user.py:19` — CHECK `subscription_status IN ('free','trial','pro','expired','cancelled')`.
- `user.py:40` — `timezone` 컬럼 존재. 일일 한도·전이 로직: `backend/app/services/subscription.py`.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 전이 조건·불변조건 정밀 명세 | — | subscription-state-machine spec |
| — | `User.timezone` 기본값 | — | spec 단계 |
