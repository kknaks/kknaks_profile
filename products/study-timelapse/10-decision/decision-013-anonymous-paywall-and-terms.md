---
type: decision
id: STL-DEC-013
title: "Anonymous paywall 로그인 유도 + 약관 가입·결제 양쪽 노출"
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
    - "[[decision-014-phase1-execution-strategy|STL-DEC-014]]"
  specs: []
  works: []
  releases: []
  related: []
---

# Anonymous paywall 로그인 유도 + 약관 양쪽 노출 (ADR-13)

Anonymous 사용자가 paywall 도달 시 로그인 화면으로 redirect. 약관·개인정보처리방침은 가입 화면 + paywall 양쪽에 노출. 약관 초안은 planner 작성 → 사용자 검토 → Phase 2 진입 전 법무 완료.

> 원본: `study_timelapse/medi_docs/current/adr/adr-13-anonymous-paywall-and-terms.md`. D-PLAN-9/10 + P-PLAN-3 통합.

## Context

- Phase 1 결제는 인증 사용자만. Anonymous 의 paywall 도달은 Free 한도 초과 시 이론상 가능.
- 한국 전자상거래법: 결제 전 약관 동의·개인정보처리방침 표시 필수.

## Options

| 축 | 채택안 | 대안 |
|---|---|---|
| Anonymous paywall (D-PLAN-9) | A: 로그인 유도 후 paywall | B: paywall 먼저 / C: 접근 차단 |
| 약관 위치 (D-PLAN-10) | A: 가입 + paywall 양쪽 | B: 가입만 / C: Phase 2 보류 |
| 약관 작성 (P-PLAN-3) | A: planner 초안 → 검토 → Phase 2 전 법무 | B: 외부 법무 선의뢰 / C: Phase 2 전에만 |

## Decision

**세 축 모두 A 채택.**

- Anonymous → 로그인 화면 redirect, 구매 의도 보존(로그인 후 paywall 복귀).
- 약관: 가입 화면 동의 체크박스 + paywall 결제 직전 문구.
- 동의 이력: `User.terms_agreed_at`, `User.privacy_agreed_at`.
- 약관 텍스트: planner 초안 → 사용자 검토 → Phase 2(실제 결제) 진입 전 법무 검토 완료.

## 구현 현황

- 정합. `backend/app/models/user.py:44` `terms_agreed_at`, `:45` `privacy_agreed_at` 컬럼.
- 약관 화면: `frontend/mobile/app/legal/`, onboarding 흐름.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 약관/개인정보/환불정책 planner 초안 작성 | — | 별도 task |
| — | Phase 2 진입 전 법무 검토 완료 체크포인트 | — | Phase 2 게이트 |
