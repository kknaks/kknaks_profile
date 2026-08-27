---
type: decision
id: STL-DEC-022
title: "subscription_status 신뢰원 — backend 캐시 + webhook sync + 강제 sync endpoint"
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
    - "[[decision-015-receipt-verification-dual-path|STL-DEC-015]]"
    - "[[decision-019-grace-period-handling|STL-DEC-019]]"
    - "[[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - caching
---

# subscription_status 신뢰원 — backend 캐시 + webhook sync (ADR-22)

앱의 구독 상태 조회는 `GET /users/me` → backend `subscription_status + pro_until` 캐시 기준(B). webhook 으로 backend 최신 유지, 구매 직후 client verify 로 즉시 sync. webhook 누락 대응용 강제 sync endpoint(`POST /subscription/sync`) 추가.

> 원본: `study_timelapse/medi_docs/current/adr/adr-22-status-source-cache-with-sync.md`. D-PLAN-2-11. Phase 2.

## Context

- Phase 1: `GET /users/me` 로 구독 상태 반환. Phase 2 에서 앱이 RevenueCat SDK 를 직접 조회하면 Phase 1 API 구조 변경 필요 + 오프라인 fallback 복잡.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[caching]] — 앱은 **backend 캐시**를 보고, webhook 이 그것을 최신으로 유지한다. 캐시가 낡을 수 있다는 것을 인정하고 **강제 sync 로 해소**하는 경로를 따로 둔 것이 이 결정이다

## Options

| Option | 신뢰원 | 장점 | 단점 |
|---|---|---|---|
| A | RevenueCat customer info 우선 | 항상 최신 | Phase 1 API 변경, 오프라인 fallback 복잡 |
| B (채택) | backend 캐시 + webhook sync | Phase 1 API 유지, 오프라인 자연 처리 | webhook 지연 시 일시 불일치 |
| C | 동시 조회, 불일치 시 RevenueCat 우선 | 정합 최대 | 구현·호출 2배 |

## Decision

**B 채택 + 강제 sync endpoint 추가.**

- `GET /users/me` 캐시 기준 응답, webhook 으로 최신 유지, 구매 직후 `POST /verify`([[decision-015-receipt-verification-dual-path|STL-DEC-015]])로 즉시 sync.
- 오프라인: 마지막 캐시 상태 표시, SDK 초기화 실패 시 backend fallback.
- **강제 sync(`POST /subscription/sync`)**: webhook 누락 시 결제 후 stale 해소("구독 상태 새로고침" UX). RevenueCat API 호출은 사용자 요청 시에만.

## 구현 현황

- 정합. `backend/app/api/v1/subscription.py:76` `sync_subscription` 엔드포인트(강제 sync 채택안 구현됨). 상태 조회는 `GET /users/me`(`users.py`) 유지.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | `is_pro` 캐시 컬럼 Phase 2 deprecated 표기 | — | P2.5 |
