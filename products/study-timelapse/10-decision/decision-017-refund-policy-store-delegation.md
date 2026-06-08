---
type: decision
id: STL-DEC-017
title: "환불 정책 — Apple/Google 스토어 위임, 회사 직접 환불 없음"
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
    - "[[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 환불 정책 — Apple/Google 스토어 위임 (ADR-17)

Phase 2 환불은 Apple/Google 스토어 정책에 전면 위임한다. 회사가 직접 일할 환불을 처리하지 않는다.

> 원본: `study_timelapse/medi_docs/current/adr/adr-17-refund-policy-store-delegation.md`. D-PLAN-2-4. Phase 2.

## Context

- in-app purchase(RevenueCat SDK → Apple/Google 결제 시트) 의 환불은 스토어가 처리하는 것이 표준. 스토어 외 결제 수단이 없으면 회사 직접 환불은 현실적으로 불가.
- Phase 1 `policy-05-subscription-refund` 초안의 일할 환불 조항은 미확정.

## Options

| Option | 방식 | 장점 | 단점 |
|---|---|---|---|
| A (채택) | Apple/Google 위임 | 운영 부담 0, in-app 기본 | 환불 조건 커스터마이징 불가 |
| B | 회사 직접 일할 환불 | 사용자 유연성 | 어드민 구현 필요, 스토어 외 수단 없으면 불가 |
| C | A 기본 + 특수 케이스만 B | 자동 + 예외 | 기준 불명확, 운영 부담 |

## Decision

**A 채택 — Apple/Google 스토어 환불 위임.**

- RevenueCat `REFUND`/`CANCELLATION`(영수증 무효) 수신 → backend 즉시 `cancelled` + `pro_until=현재시각`(상세 전환은 [[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]).
- `policy-05` 의 일할 환불 조항 → "환불은 해당 앱스토어 정책을 따릅니다" 로 교체. 환불 문의는 스토어 고객센터 안내.

## 구현 현황

- 정합(스키마 측면). 환불 전환 로직은 [[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]] 에서 grounding. Phase 1 `subscription_events` + `User` 컬럼 재사용(신규 스키마 없음).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | `policy-05-subscription-refund` 갱신(일할→스토어 위임) | — | P2.1 task |
| — | CS 환불 문의 안내 절차 | — | CS 가이드 |
