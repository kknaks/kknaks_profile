---
type: decision
id: STL-DEC-018
title: "RevenueCat app_user_id ↔ backend user_id 매핑 — 가입 즉시 logIn"
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
    - "[[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]"
    - "[[decision-016-introductory-offer-and-auto-renewal|STL-DEC-016]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - surrogate-key
---

# RevenueCat app_user_id ↔ backend user_id 매핑 — 가입 즉시 logIn (ADR-18)

RevenueCat `app_user_id` 를 backend `user_id` 와 1:1 매핑한다. 가입 직후 `Purchases.logIn(user_id)` 호출. 디바이스 변경/재설치 시 customer info 자동 복원.

> 원본: `study_timelapse/medi_docs/current/adr/adr-18-app-user-id-mapping.md`. D-PLAN-2-7. Phase 2.

## Context

- RevenueCat SDK 는 `app_user_id` 로 구독 이력 추적. 미설정 시 anonymous ID 자동 생성 → backend user_id 와 불일치, 디바이스 변경 시 복원 불가.
- Phase 1 인증 필수 paywall([[decision-013-anonymous-paywall-and-terms|STL-DEC-013]]).

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[surrogate-key]] — 외부 시스템과의 연결을 **바뀌지 않는 내부 식별자(`User.id`)** 로 잡는다. 이메일이나 계정처럼 바뀔 수 있는 값으로 이으면 디바이스 변경에서 끊긴다

## Options

| Option | 매핑 시점 | 장점 | 단점 |
|---|---|---|---|
| A (채택) | 가입 즉시 `logIn(user_id)` | 구현 단순, 1:1 일치, 복원 자동 | 가입 시 SDK 초기화 필요 |
| B | 결제 시점 logIn | SDK 초기화 지연 가능 | anonymous merge 필요 |
| C | 익명 결제 후 가입 시 merge | 로그인 전 결제 지원 | Phase 1 인증 필수와 상충 |

## Decision

**A 채택 — 가입 즉시 `Purchases.logIn(backend_user_id)`.**

- `app_user_id` = backend `User.id`(stable identifier).
- 디바이스 변경/재설치: 동일 Apple/Google 계정 로그인 후 `logIn(user_id)` → customer info 복원 → backend sync.
- anonymous 사용자: [[decision-013-anonymous-paywall-and-terms|STL-DEC-013]] 정책 그대로(로그인 유도). 게스트 결제 후 복원은 Phase 2 비목표.

## 구현 현황

- 정합(backend 무영향). 추가 엔드포인트 불필요 — `user_id` 는 기존 인증 토큰에서 추출. RevenueCat `logIn` 호출은 mobile 측(`frontend/mobile/`).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 탈퇴 후 재가입 시 동일 user_id 재사용 여부 | — | spec 단계 |
