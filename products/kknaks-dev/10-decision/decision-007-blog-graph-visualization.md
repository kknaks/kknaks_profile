---
type: decision
id: KDEV-DEC-007
title: "블로그 그래프 시각화 — 전역 + 노트별 로컬"
status: accepted
product: kknaks-dev
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-004-edge-model-and-schema|KDEV-DEC-004]]"
    - "[[decision-006-validation-gates|KDEV-DEC-006]]"
  specs:
    - "[[spec-005-graph-visualization|KDEV-SPEC-005]]"
  works: []
  releases: []
  related: []
---

# 블로그 그래프 시각화 (ADR-007)

`build_graph` 산출물(`_graph.json`)을 블로그에서 force-directed로 렌더한다. 전역 `/graph` + 각 노트 페이지 하단 로컬 그래프(옵시디언 경험과 동형).

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- 목표는 관계를 블로그에서 시각화하는 것. 데이터는 빌더가 노드+엣지+타입+방향을 산출.
- backlink는 `build_graph`가 이미 산출 → 로컬 그래프 추가 비용 작음.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 전역만 | /graph 한 개 | 단순 | 노트 맥락 약함 | 시작점 가능 |
| **전역 + 로컬** | /graph + 노트별 미니 그래프 | 옵시디언 경험 동형 | 작업 약간 더 | **채택** |

## Decision

- 데이터: `build_graph` 확장 → `_graph.json` (노드 + 엣지 + `type` + `dir`).
- 전역 `/graph` 라우트(force-directed 전체 지식맵) + 각 노트 페이지 하단 로컬 그래프(이웃 + 백링크).
- 노드 색 = `type`, 엣지 = lineage(화살표)/assoc(선), archive 흐리게. type 필터·포커스.
- 처음엔 전역만(C)으로 시작해 로컬로 확장해도 됨.

## Rationale

- 옵시디언 경험이 전역+로컬 그래프라 사용자 멘탈 모델과 일치.
- 백링크 데이터가 이미 있어 로컬 그래프 추가 비용 작음.

## Scope

- In: _graph.json 산출, /graph 라우트, 노트별 로컬 그래프.
- Out: 빌더/프론트 구현(work).
- 영향을 받는 spec 후보: 시각화 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | force graph 라이브러리 선택 | | 시각화 spec/work |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 시각화 spec | create | _graph.json 스키마 + 렌더 규칙 |
