---
type: decision
id: STL-DEC-014
title: "Phase 1 실행 전략 — 1a 완료 후 1b/1c 병렬 + DoD 단일 디바이스"
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
    - "[[decision-012-mock-purchase-api-and-events|STL-DEC-012]]"
    - "[[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]"
  specs: []
  works: []
  releases: []
  related: []
up: []
---

# Phase 1 실행 전략 — 1a 완료 후 1b/1c 병렬 + DoD 단일 디바이스 (ADR-14)

Phase 1a(backend DB + API) 완료 후 1b(paywall 연동) + 1c(약관 UI)를 병렬 시작. Phase 1 DoD = 단일 디바이스 검증.

> 원본: `study_timelapse/medi_docs/current/adr/adr-14-phase1-execution-strategy.md`. P-PLAN-1/2 통합. (이 결정은 산출물 계약이 아닌 실행 프로세스 결정 — 코드 grounding 대상 아님.)

## Context

- Phase 1 sub-phase: 1a(backend) / 1b(paywall) / 1c(약관). 직렬 vs 병렬, DoD 에 "다중 디바이스 동일 상태" 포함 여부 결정 필요.

## 근거 개념

없음 — 작업 순서와 완료 기준을 정한 일정 결정이다.

## Options

| 축 | 채택안 | 대안 |
|---|---|---|
| 진행 방식 (P-PLAN-1) | A: 1a API 계약 확정 즉시 1b/1c 병렬 | B: 1a 완전 완료 후 직렬 / C: 모두 병렬 |
| DoD 범위 (P-PLAN-2) | 단일 디바이스 | 다중 디바이스 동일 상태(제외) |

## Decision

**A + 단일 디바이스 DoD 채택.**

- 1a API spec 확정 시점 기준 1b/1c 병렬 → 재작업 위험 최소 + 납기 단축.
- DoD: 단일 디바이스 5개 시나리오(가입→trial, mock-purchase→Pro, Free 1회/일 초과 차단, trial 7일 만료→free, 약관 동의 이력) + debug API prod 404 + append-only 이력.
- 다중 디바이스 동기화는 서버 SSOT 구조상 자동 보장 → Phase 2 RevenueCat 연동 시 다룸.

## 구현 현황

- 프로세스 결정(코드 산출물 아님). Phase 1a 산출물은 [[decision-010-subscription-state-model|STL-DEC-010]]·[[decision-012-mock-purchase-api-and-events|STL-DEC-012]] 의 구현 현황으로 확인됨(5상태 모델, mock-purchase API, subscription_events append-only 모두 구현).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 다중 디바이스 동기화 검증 | — | Phase 2 RevenueCat 연동 |
