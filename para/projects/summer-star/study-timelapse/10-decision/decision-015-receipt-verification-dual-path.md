---
type: decision
id: STL-DEC-015
title: "영수증 검증 이중 경로 — client verify + RevenueCat webhook"
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
    - "[[decision-012-mock-purchase-api-and-events|STL-DEC-012]]"
    - "[[decision-020-webhook-auth-bearer|STL-DEC-020]]"
    - "[[decision-022-status-source-cache-with-sync|STL-DEC-022]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - unique-key
---

# 영수증 검증 이중 경로 — client verify + RevenueCat webhook (ADR-15)

RevenueCat 결제 후 backend 상태 갱신 경로를 client `POST /api/subscription/verify` + RevenueCat webhook 이중 경로로 결정한다. webhook 이 source of truth(충돌 시 우선), 멱등 키는 `transaction_id`.

> 원본: `study_timelapse/medi_docs/current/adr/adr-15-receipt-verification-dual-path.md`. Phase 2.

## Context

- Phase 1 mock-purchase → Phase 2 RevenueCat SDK 영수증 검증 흐름 전환.
- 결제 직후 즉시 Pro unlock UX 와 환불·취소·갱신·grace-period 라이프사이클 모두 충족 필요.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[unique-key]] — **같은 `transaction_id` 는 두 번 들어오지 않는다** — 경로가 둘(client verify · webhook)이라 중복이 필연이므로, 멱등을 유일 제약으로 보장한다

## Options

| Option | trigger | 장점 | 단점 |
|---|---|---|---|
| A | client → `POST /verify` | 즉시 갱신, UX 지연 없음 | 재시도·위조 방어 필요 |
| B | webhook 단독 | 위조 불가, 라이프사이클 완결 | 수신 지연 → unlock UX 지연 |
| C (채택) | A + B 이중 (webhook = SoT) | 즉시 unlock + 라이프사이클 처리 | 멱등 처리 복잡 |

## Decision

**C 채택 — client verify + webhook 이중 경로.**

- A: 구매 직후 `POST /verify` → backend 가 RevenueCat API 재확인 후 `subscription_status='pro'` + events INSERT(`source='revenuecat'`, `transaction_id`).
- B: webhook = source of truth. 환불·취소·갱신·grace 처리. 충돌 시 webhook 우선.
- 멱등성: 동일 `transaction_id` 중복 INSERT 차단.

## 구현 현황

- 정합. `backend/app/api/v1/subscription.py:53` `verify_receipt`, `:91` `receive_webhook` 엔드포인트.
- `backend/app/models/subscription_event.py:54` `transaction_id` 컬럼 + 마이그 `004_phase2_revenuecat_columns.py` 의 부분 유니크 인덱스(`idx_sub_events_transaction_id`).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | client verify 실패 시 재시도 정책(권장: 1회 후 webhook 대기) | — | spec 단계 |
