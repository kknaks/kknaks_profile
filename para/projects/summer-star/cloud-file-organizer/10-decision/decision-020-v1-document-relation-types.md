---
type: decision
id: CFO-DEC-020
title: "v1 문서 relation type 기본 목록"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - document-relation
  - knowledge-graph
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-010-document-relation-and-related-metadata]]"
    - "[[decision-014-physical-list-and-related-document-visibility]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - object-graph
---

# v1 문서 relation type 기본 목록

v1의 문서 relation type은 `related`, `references`, `supersedes`, `duplicate_candidate` 4개로 시작한다. `duplicate_candidate`는 중복/유사 후보 표시이며, v1에서 merge 동작은 제공하지 않는다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-010-document-relation-and-related-metadata]], [[decision-014-physical-list-and-related-document-visibility]]
- 문서 관계는 DB relation이 SoT다.
- relation type이 너무 많으면 승인 게이트가 복잡해진다.
- relation type이 너무 적으면 모든 관계가 `related`로 뭉개진다.
- 유사 문서종류 merge와 shortcut은 v1에서 제외하기로 이미 결정했다.

## Decision

- 채택:
  - v1 relation type은 `related`, `references`, `supersedes`, `duplicate_candidate` 4개로 시작한다.
  - `related`는 일반 관련 문서 연결이다.
  - `references`는 source 문서가 target 문서를 참조하는 관계다.
  - `supersedes`는 source 문서가 target 문서를 대체하는 관계다.
  - `duplicate_candidate`는 AI가 중복/유사 문서 후보로 판단한 관계다.
  - 모든 relation은 승인 전 후보이고, 사람 승인 후 graph에 반영한다.
  - `duplicate_candidate`는 merge action을 수행하지 않는다.
- 기각:
  - v1에서 relation type을 자유 입력으로 두는 방식.
  - 모든 관계를 `related` 하나로만 저장하는 방식.
  - `duplicate_candidate` 승인 시 문서를 자동 merge하는 방식.

## Relation Types

| Type | 의미 | 방향성 |
|---|---|---|
| `related` | 일반 관련 문서 | 약한 방향성 |
| `references` | source가 target을 참조 | source -> target |
| `supersedes` | source가 target을 대체 | source -> target |
| `duplicate_candidate` | 중복/유사 후보 | 약한 방향성 |

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[object-graph]] — 엣지에 **타입을 준다**(`related`·`references`·`supersedes`·`duplicate_candidate`). 연결의 종류가 곧 나중에 무엇을 물어볼 수 있는지를 정한다

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Relation type catalog contract | v1 relation type enum |
| Relation approval contract | AI 후보 relation의 승인/수정 |
| Duplicate candidate contract | 중복 후보 표시와 merge 제외 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-1001 | v1 relation type은 `related`, `references`, `supersedes`, `duplicate_candidate` 4개로 시작한다. |
