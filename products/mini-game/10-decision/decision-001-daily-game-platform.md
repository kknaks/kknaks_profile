---
type: decision
id: MG-DEC-001
title: "Daily game platform MVP"
status: accepted
product: mini-game
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - product/mini-game
  - doc/decision
  - status/accepted
links:
  baselines:
    - MG-BL-001
  decisions: []
  specs:
    - MG-SPEC-001
    - MG-SPEC-002
  works:
    - MG-WORK-001
  releases: []
  related: []
---

# Daily game platform MVP

매일 다른 모바일 미니게임을 열되, 로그인/참여/결과 기록/꼴찌 탐색/일일 종료는 공통 플랫폼 계약으로 둔다.

## Context

- 관련 baseline: BL-001
- 문제/기회: 회사 커피 내기용으로 매일 짧게 참여할 수 있는 모바일 웹 게임이 필요하다.
- 결정이 필요한 이유: 게임이 매일 바뀌어도 결과 기록과 꼴찌 탐색은 공통으로 유지되어야 한다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | Next.js + Supabase 기반 모바일 웹 | 구현 빠름, Auth/DB 활용 가능, 모바일 배포 단순 | Supabase 정책 설계 필요 | 채택 |
| B | 별도 백엔드 + Next.js | 장기 확장 유리 | MVP 작업량 증가 | 보류 |
| C | 노로그인 링크 게임 | 진입장벽 낮음 | 중복 참여/사용자 식별 취약 | 기각 |

## Decision

- 채택: 프론트는 Next.js, Auth/DB는 Supabase를 MVP 기본 스택으로 둔다.
- 채택: 로그인한 사용자만 당일 게임에 참여할 수 있다.
- 채택: 사용자는 하루 active game에 1회만 제출할 수 있다.
- 채택: 매일 참여 마감 시각은 Asia/Seoul 기준 12:30이다.
- 채택: daily game registry는 DB로 관리한다. 날짜별 active game, game type, cutoff, config를 DB record로 둔다.
- 채택: 게임별 결과는 공통 `score`, `rankValue`, `resultLabel`, `metadata` 형태로 기록한다.
- 채택: 꼴찌는 참여 완료자에게 즉시 공개되는 전체 결과에서 `rankValue`가 가장 낮은 참여자로 판정한다. 동률이면 공동 꼴찌로 표시하고, 실제 커피 내기 처리는 꼴찌끼리 알아서 정한다.
- 기각: MVP에서 익명 참여, 무제한 재시도, PC 최적화, 멀티게임 동시 운영은 하지 않는다.

## Rationale

- 판단 기준: 회사 내 반복 사용, 중복 참여 방지, 매일 게임 교체, 빠른 MVP 구현.
- 대안 대비 이유: Supabase Auth/DB 조합은 로그인과 결과 저장을 빠르게 닫을 수 있고, game registry를 DB로 두면 게임을 매일 바꾸는 구조가 코드 배포에 묶이지 않는다.
- 리스크: Supabase RLS와 daily cutoff 처리가 제품 핵심 경계가 된다.

## Scope

이번 spec에 반영할 범위.

- In:
  - 모바일 웹 로그인.
  - 당일 active game 조회.
  - 1일 1회 참여 제출.
  - 결과 저장.
  - 12:30 이후 참여 차단.
  - 꼴찌 탐색.
  - DB 기반 날짜별 game registry.
- Out:
  - 게임 생성 admin UI.
  - 여러 게임 동시 참여.
  - 결제/정산/커피 주문 연동.
  - PC 전용 레이아웃.
- 영향을 받는 spec 후보:
  - SPEC-001: daily game platform.
  - SPEC-002: yut gauge game.

## Open Questions

없음. 세부 schema와 RLS 정책은 SPEC/architecture에서 확정한다.

## Follow-up Decisions

| ID | Topic | Trigger |
|---|---|---|
| FD-001 | Admin UI 제공 여부 | DB registry를 사람이 자주 수정해야 할 때 |

## Resolved Baseline Questions

| Baseline Question | Resolution |
|---|---|
| Q-001 로그인 방식 | Supabase Auth 기반 로그인. MVP 세부 provider는 spec에서 확정 |
| Q-002 하루 한 번만 참여 가능한가 | 당일 active game 기준 1회 제출 |
| Q-003 12:30 종료 timezone | Asia/Seoul. 결과 공개 시간이 아니라 참여 마감 시간 |
| Q-004 꼴찌 판정 기준 | game result의 `rankValue` 최저값. 동률은 공동 꼴찌 표시, 실제 처리는 당사자 간 결정 |
| Q-006 매일 바뀌는 게임 등록 | DB 기반 daily game registry 사용 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| SPEC-001 | create | 로그인/참여/결과/꼴찌/daily cutoff 계약 |
| SPEC-002 | create | 첫 게임인 윷놀이 게이지 룰 계약 |
