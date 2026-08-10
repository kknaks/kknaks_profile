---
type: decision
id: STL-DEC-020
title: "RevenueCat Webhook 인증 — Authorization Bearer"
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
    - "[[decision-015-receipt-verification-dual-path|STL-DEC-015]]"
    - "[[decision-022-status-source-cache-with-sync|STL-DEC-022]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - http-message
  - externalized-configuration
---

# RevenueCat Webhook 인증 — Authorization Bearer (ADR-20)

RevenueCat webhook 수신 시 `Authorization: Bearer <token>` 헤더를 검증한다. 토큰은 ENV `REVENUECAT_WEBHOOK_AUTH_TOKEN` 으로 관리, RevenueCat 대시보드에 동일 토큰 설정.

> 원본: `study_timelapse/medi_docs/current/adr/adr-20-webhook-auth-bearer.md`. D-PLAN-2-9. Phase 2.

## Context

- `POST /api/subscription/webhook`([[decision-015-receipt-verification-dual-path|STL-DEC-015]]) 무인증 시 외부 위변조 이벤트 수신 가능.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[http-message]] — `Authorization: Bearer <token>` 헤더로 발신자를 확인한다 — 본문이 아니라 **헤더가 신원을 나르는** 자리다
- [[externalized-configuration]] — 토큰을 코드가 아니라 ENV·`secret.env` 에 두고 로그에 남기지 않으며, 유출 시 대시보드와 함께 로테이션한다

## Options

| Option | 방식 | 장점 | 단점 |
|---|---|---|---|
| A (채택) | Authorization Bearer | RevenueCat 표준, 1줄 검증, HTTPS 하 충분 | 토큰 유출 시 위변조(HTTPS + ENV 저장으로 방어) |
| B | HMAC signature | 높은 보안 | RevenueCat 비표준, 커스텀 구현 |

## Decision

**A 채택 — Bearer 토큰 검증.**

- 토큰: 최소 32바이트 랜덤(`secrets.token_urlsafe(32)`), `secret.env`(gitignored) 저장, 로그 금지, 대시보드+ENV 동시 로테이션.
- HTTPS 강제. 401 시 RevenueCat 자동 재시도. 유출 시 즉시 로테이션 절차는 runbook.

## 구현 현황

- 정합. `backend/app/api/v1/subscription.py:91` `receive_webhook` 엔드포인트(Bearer 검증 포함). `REVENUECAT_WEBHOOK_AUTH_TOKEN` ENV 변수로 관리.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 토큰 로테이션 절차 runbook 화 | — | P2.4 runbook |
