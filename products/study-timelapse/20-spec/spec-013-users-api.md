---
type: spec
id: STL-SPEC-013
title: "Users API (프로필·구독·약관)"
status: implemented
product: study-timelapse
created_at: 2026-05-18
updated_at: 2026-06-08
tags:
  - product/study-timelapse
  - doc/spec
  - status/implemented
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-003-subscription-state-machine|STL-SPEC-003]]"
    - "[[spec-004-subscription-api|STL-SPEC-004]]"
  works: []
  releases: []
  related: []
---

# Users API (프로필·구독·약관)

인증 사용자의 프로필·구독 상태·일일 한도·배너 알림 조회 + 프로필 수정·약관 동의·streak 갱신 계약.

> 원본: `medi_docs/current/spec/spec-13-users-api.md`. frontmatter 에 ADR depends 없음 → `links.decisions` 비움. 구독 상태/한도/약관은 [[spec-003-subscription-state-machine|STL-SPEC-003]]·[[spec-004-subscription-api|STL-SPEC-004]] 와 공유(`GET /me` 확장 필드는 spec-004 와 동일 계약).

## Context

- 짝 spec: 구독 상태([[spec-003-subscription-state-machine|STL-SPEC-003]]), 구독 API([[spec-004-subscription-api|STL-SPEC-004]] — GET /me·terms-agree 공유)
- 범위: `/api/users/me` 계열 4개 엔드포인트

## BE Contract (Users Endpoints)

### GET /api/users/me
- 응답 전 `apply_lazy_expiry(user)` (trial/pro 만료 자동 전이)
- Response: `UserResponseV2` (확장 필드는 [[spec-004-subscription-api|STL-SPEC-004]] 참조)
  - `daily_quota`: trial/pro = -1, free/expired/cancelled = 1
  - `daily_quota_resets_at`: 사용자 timezone 다음 자정(UTC)
  - `banner_alert`: trial 만료 1h/24h 이내 또는 null

### PUT /api/users/me/terms-agree
- Request: `{terms_agreed, privacy_agreed}` (둘 다 true). 400 `INVALID_AGREEMENT`. 멱등(재호출 시각 갱신)

### PUT /api/users/me/profile
- Request: `{name}`. 빈 문자열 → 422

### PUT /api/users/me/streak
- Request: `{streak, longest_streak?}`. `longest_streak` 미제공 시 `max(기존, streak)` 유지

## Data Contract (User 주요 필드)

`subscription_status`(VARCHAR(20) CHECK), `trial_start_date`, `is_pro`, `pro_until`, `grace_until`, `timezone`, `terms_agreed_at`, `privacy_agreed_at`, `streak`, `longest_streak`, `total_focus_time` — 상세는 [[spec-005-subscription-data-model|STL-SPEC-005]].

## Case Matrix (에러)

| 엔드포인트 | 상황 | 응답 |
|---|---|---|
| GET /me | JWT 미제공 | 401 `UNAUTHORIZED` |
| terms-agree | false 포함 | 400 `INVALID_AGREEMENT` |
| profile | name 빈 문자열 | 422 |

## 구현 현황 (코드 grounding)

ground truth: `study_timelapse/backend/`. 전 엔드포인트 정합 — gap 없음.

| 계약 | 코드 근거 |
|---|---|
| GET /me (lazy expiry/quota/resets/banner) | `app/api/v1/users.py:29-81`, `app/schemas/user.py:28-54`, resets `app/services/subscription.py:42-49` |
| terms-agree (400 INVALID_AGREEMENT) | `app/api/v1/users.py:84-146` |
| profile (422 empty) | `app/api/v1/users.py:149-168` |
| streak (max 로직) | `app/api/v1/users.py:171-199` |

## Open Questions

- 없음 (구현·배포 완료).
