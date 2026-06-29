---
type: decision
id: KDEV-DEC-004
title: "엣지 모델(본문 [[]] + up 오버레이) + 스키마 SSOT 문서"
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
    - "[[decision-003-node-type-and-identifier|KDEV-DEC-003]]"
    - "[[decision-006-validation-gates|KDEV-DEC-006]]"
  specs:
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
  works: []
  releases: []
  related: []
---

# 엣지 모델 + 스키마 SSOT (ADR-004)

모든 엣지는 본문 `[[ ]]`가 단일 소스(옵시디언 그래프에 항상 표시). 계보(lineage)는 frontmatter `up: [stem]` 평문 오버레이로 마킹(블로그만 읽음). 스키마는 분산 저장하되 정의 문서는 한 곳.

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- DB 없음, 파일(frontmatter)이 SoT. `build_graph()`가 본문 `[[]]` + frontmatter `links:`를 엣지로 조립.
- 파이프라인에 성격이 다른 두 관계: 정제 계보(방향 O) vs 연상 연결(방향 X).
- 순정 옵시디언 그래프는 본문 `[[]]`만 엣지로 그림(frontmatter property-link는 버전 의존, `showArrow:false`라 방향/타입 구분 안 됨).

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| frontmatter 전용 lineage | `up: ["[[…]]"]` | 구조적 | 옵시디언 버전 의존, 그래프서 assoc과 구분 안 됨 | 기각 |
| **본문 [[]] + up 오버레이** | 본문이 단일 엣지 소스, up은 평문 마킹 | 버전 리스크 0, 중복 없음 | 빌더가 두 신호 읽음 | **채택** |

스키마 저장: 데이터는 분산(각 노트), 정의(스키마) 문서는 한 곳. 중앙 데이터 문서는 금지(drift).

## Decision

- 엣지 = 본문 `[[stem]]` 단일 소스. 기본 타입 `assoc`.
- `lineage`(계보) = frontmatter `up: [stem, …]` 평문 리스트 오버레이 — 본문 링크 중 계보인 것 + 방향(상류→이 노트) 마킹. 블로그만 읽음, 옵시디언 무시(안 깨짐). 하류는 backlink로 자동 도출.
- 전제: 영구노트는 참고노트를 본문에 `[[]]`로 인용한다([[decision-005-classification-workflow|KDEV-DEC-005]]).
- 출처(URL)는 노드 아님 → `source:` 속성.
- 기존 평문 `links: [id]`는 폐기 → 본문 `[[]]` 또는 `up:`으로 흡수.
- 스키마 정의 SSOT = `products/kknaks-dev/20-spec/spec-knowledge-graph.md` (구 medi_docs spec 계승). 데이터는 분산.
- 기각: frontmatter 위키링크 lineage, 중앙 관계 데이터 문서.

## Rationale

- 본문 `[[]]`는 옵시디언 그래프에 항상 나오고 버전 리스크 0.
- `up`은 본문에 이미 있는 링크를 가리키는 오버레이라 중복 아님(L3로 강제).
- 스키마는 한 곳이어야 새 관계 추가·검증의 기준이 됨. 데이터는 분산해야 SSOT·drift 방지.

## Scope

- In: 엣지 타입(assoc/lineage), up 오버레이, source 속성, 스키마 문서 위치.
- Out: 빌더 regex/검증 구현(work), 구 spec 이관.
- 영향을 받는 spec 후보: 스키마 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | (해결) medi_docs 전체 폐기 완료 (2026-06-29). spec-02/04는 KDEV-SPEC-002로 계승 | kknaks | done |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 스키마 spec | create | 엣지 타입 + up 오버레이 + 빌더 동작 |
