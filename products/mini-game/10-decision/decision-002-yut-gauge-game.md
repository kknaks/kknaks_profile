---
type: decision
id: MG-DEC-002
title: "Yut gauge first game"
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
  decisions:
    - MG-DEC-001
  specs:
    - MG-SPEC-002
  works:
    - MG-WORK-001
  releases: []
  related: []
up: []
---

# Yut gauge first game

첫 daily game은 윷놀이 결과를 게이지 타이밍으로 보정하는 모바일 버튼 게임으로 만든다.

## Context

- 관련 baseline: BL-001
- 문제/기회: 누구나 이해하는 `도/개/걸/윷/모` 결과를 짧은 조작으로 만든다.
- 결정이 필요한 이유: 윷놀이 결과 확률과 플랫폼 공통 ranking 값이 필요하다.

## 근거 개념

없음 — 게임 규칙과 확률 분포를 정한 제품 결정이다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 게이지 정확도에 따라 높은 결과 확률이 증가 | 조작감 있음, 좋은 입력이 유리함 | 확률 테이블 필요 | 채택 |
| B | 완전 랜덤 윷 결과 | 구현 단순 | 게임성이 약함 | 기각 |
| C | 여러 번 던져 합산 점수 | 더 풍부함 | MVP가 길어짐 | 보류 |

## Decision

- 채택: 사용자는 한 번의 버튼 입력으로 게이지를 멈춘다.
- 채택: 게이지 중앙에 가까울수록 높은 결과(`걸`, `윷`, `모`) 확률이 증가한다.
- 채택: 중앙을 정확히 맞춰도 `모`가 보장되지는 않는다. 좋은 입력은 확률을 유리하게 만들 뿐이다.
- 채택: 결과 label은 `도`, `개`, `걸`, `윷`, `모`다.
- 채택: 플랫폼 공통 `rankValue`는 `도=1`, `개=2`, `걸=3`, `윷=4`, `모=5`로 둔다.
- 채택: 점수 `score`도 MVP에서는 `rankValue`와 동일하게 둔다.
- 채택: 꼴찌 탐색에서는 낮은 `rankValue`가 불리하다.
- 채택: MVP는 1인 1회 던지기다. 재시도와 여러 판 합산은 후속으로 미룬다.
- 채택: 정확도 구간별 확률 테이블은 아래와 같이 시작한다.

| Accuracy band | 기준 | 도 | 개 | 걸 | 윷 | 모 |
|---|---|---:|---:|---:|---:|---:|
| Perfect | 중앙 오차 0-5% | 5% | 8% | 18% | 31% | 38% |
| Great | 중앙 오차 5-15% | 8% | 12% | 24% | 30% | 26% |
| Good | 중앙 오차 15-30% | 14% | 18% | 30% | 24% | 14% |
| Normal | 중앙 오차 30-50% | 24% | 24% | 28% | 16% | 8% |
| Bad | 중앙 오차 50-100% | 38% | 28% | 21% | 9% | 4% |

## Rationale

- 판단 기준: 모바일에서 짧게 끝나는가, 결과를 바로 비교할 수 있는가, 첫 게임 구현이 단순한가.
- 대안 대비 이유: 완전 랜덤보다 버튼 타이밍이 있어 “내가 했다”는 감각이 생긴다.
- 리스크: 좋은 입력이 결과를 보장한다고 느껴지면 불만이 생길 수 있으므로 UI 문구와 spec에 "확률 상승, 보장 아님"을 명시한다.

## Scope

이번 spec에 반영할 범위.

- In:
  - 윷 화면.
  - 게이지.
  - 버튼 입력.
  - `도/개/걸/윷/모` 결과.
  - 결과별 `rankValue`.
  - 게이지 정확도 기반 확률 보정.
  - 정확도 구간별 확률 테이블.
- Out:
  - 실제 윷판 이동.
  - 팀전.
  - 여러 번 던지기.
  - 애니메이션/사운드 고도화.
- 영향을 받는 spec 후보:
  - SPEC-002: yut gauge game.

## Open Questions

없음. 확률 테이블은 SPEC-002에서 QA 가능한 계약으로 옮긴다.

## Resolved Baseline Questions

| Baseline Question | Resolution |
|---|---|
| Q-005 윷놀이 결과 확률 | 게이지 중앙 정확도 기반 확률 보정. 중앙을 맞춰도 모는 보장하지 않는다. 결과 rank는 도1/개2/걸3/윷4/모5 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| SPEC-002 | create | 윷놀이 게이지 게임 룰/UX/결과 계약 |
