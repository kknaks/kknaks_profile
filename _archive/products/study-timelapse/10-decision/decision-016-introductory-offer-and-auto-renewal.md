---
type: decision
id: STL-DEC-016
title: "트라이얼 — RevenueCat introductory offer 7일 + 자동 갱신"
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
    - "[[decision-011-monthly-only-no-yearly|STL-DEC-011]]"
    - "[[decision-014-phase1-execution-strategy|STL-DEC-014]]"
    - "[[decision-018-app-user-id-mapping|STL-DEC-018]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - db-normalization
---

# 트라이얼 — RevenueCat introductory offer 7일 + 자동 갱신 (ADR-16)

Phase 2 트라이얼 = RevenueCat introductory offer 7일 무료 → 자동 결제 전환(B+A). 가입 시 backend trial 자동 시작은 제거하고 가입자는 `free` 로 기동한다. 한국 전자상거래법상 자동 갱신 14일 사전 고지 필수.

> 원본: `study_timelapse/medi_docs/current/adr/adr-16-introductory-offer-and-auto-renewal.md`. D-PLAN-2-2/2-3. Phase 2.

## Context

- Phase 1: 가입 즉시 backend 7일 trial 자동 시작(`subscription_status='trial'`, `trial_start_date`).
- Phase 2: 스토어 표준 introductory offer 로 전환. 트라이얼 재사용 방지·자동 결제 법적 고지 처리 필요.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[db-normalization]] — 트라이얼의 원장을 **RevenueCat 한 곳**으로 옮기고 backend 는 개입하지 않는다. 양쪽이 각자 trial 을 시작하면 어느 것이 맞는지 정할 수 없다

## Options

| 축 | 채택안 | 대안 |
|---|---|---|
| 트라이얼 정책 (D-PLAN-2-2) | B: RevenueCat introductory offer | A: Phase 1 backend trial 유지 / C: 하이브리드 / ~~D 폐기~~ |
| trial 만료 시 (D-PLAN-2-3) | A: 자동 결제 전환(스토어 표준) | B: 명시 동의 재노출 |

## Decision

**B + A 채택 — introductory offer 7일 무료 → 자동 결제.**

- **B 채택 = 가입 시 backend trial 자동 시작 제거.** 가입 시 `subscription_status='free'`, `trial_start_date=NULL`, `is_pro=False`. trial 진입은 paywall `purchasePackage()` 성공 시점(introductory offer).
- trial source of truth = RevenueCat(Apple/Google 계정 eligibility). backend 개입 없음.
- Phase 1 기존 사용자: 진행 중 trial 자연 종료(마이그레이션 없음).
- 한국법 자동 갱신 14일 사전 고지(trial 시작 = 결제 직후 기준). 푸시 알림은 Phase 3.

## 구현 현황

- 정합. `backend/app/services/auth_service.py:147` — 가입 시 `subscription_status="free"`, `:148` `trial_start_date=None`, `:149` `is_pro=False` (adr-16 의 변경 후 상태와 일치, trial 자동 시작 제거됨).
- `User.trial_start_date`(`user.py:35`)는 Phase 1 감사 이력 보존 용도로 유지.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 온보딩 trial 안내 페이지(`onboarding/trial-intro`) + paywall 진입 분기 | — | mobile 구현 |
| — | `TrialExpiringBanner` D-7 계산 기준(`pro_until`) | — | spec 단계 |
