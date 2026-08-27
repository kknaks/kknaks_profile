---
type: decision
id: STL-DEC-019
title: "Grace Period 처리 — pro 유지 + grace_until 컬럼 (옵션 B)"
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
    - "[[decision-021-cancel-vs-refund-state-transition|STL-DEC-021]]"
    - "[[decision-022-status-source-cache-with-sync|STL-DEC-022]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - sql-null
  - database-migration
---

# Grace Period 처리 — pro 유지 + grace_until 컬럼 (ADR-19)

결제 수단 만료로 갱신 실패 시 Apple(최대 16일)/Google(최대 30일) grace period 동안 Pro 기능을 유지한다. `subscription_status='pro'` 유지 + `grace_until TIMESTAMP NULL` 신규 컬럼(옵션 B).

> 원본: `study_timelapse/medi_docs/current/adr/adr-19-grace-period-handling.md`. D-PLAN-2-8. Phase 2.

## Context

- RevenueCat `BILLING_ISSUE_DETECTED_EVENT`/`in_grace_period` 발생 시 grace period 시작. 가이드라인상 grace 동안 Pro 유지 권장.
- Phase 1 마이그레이션 0 원칙 — Phase 2 스키마 변경 최소화.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[sql-null]] — `grace_until TIMESTAMP NULL` 을 더해 **「해당 없음」을 NULL 로** 표현한다. `ADD COLUMN DEFAULT NULL` 이라 기존 행을 건드리지 않는 것이 이 선택의 값이다
- [[database-migration]] — ENUM 을 늘리는 대신 컬럼을 더한 판단 — **기존 데이터와 코드 분기에 미치는 영향**으로 두 방식을 비교했다

## Options

| Option | 방식 | 마이그 | 비고 |
|---|---|---|---|
| A | 6번째 ENUM `in_grace_period` | ENUM 마이그 1 + Phase 1 코드 전반 분기 | 상태 명확하나 회귀 위험 |
| B (채택) | `pro` 유지 + `grace_until` 컬럼 | 컬럼 add 1(영향 작음) | 5-state 머신 유지 |
| C | `pro` 유지 + events 메타데이터 | 0 | grace 조회 aggregation 복잡 |

## Decision

**B 채택 — `pro` 유지 + `grace_until TIMESTAMP NULL`.**

- ENUM 변경(A)은 Phase 1 전체 코드 분기 추가로 회귀 위험 큼. `grace_until` 컬럼 추가는 `ADD COLUMN DEFAULT NULL` 로 기존 데이터 영향 없음.
- webhook `BILLING_ISSUE` 수신 → `grace_until = now + grace_period_days` + `pro` 유지. 갱신 성공 시 `grace_until=NULL`. 만료 후 미갱신 시 `expired`.
- 설정 화면에 "결제 수단을 업데이트해주세요" 배너 권장.

## 구현 현황

- 정합. `backend/app/models/user.py:43` `grace_until` 컬럼. 마이그 `004_phase2_revenuecat_columns.py:24` — `op.add_column("users", grace_until …)` 주석에 "adr-19 B" 명시.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | `GET /users/me` 에 `grace_until` 필드 노출·배너 임계값 | — | spec 단계 |
