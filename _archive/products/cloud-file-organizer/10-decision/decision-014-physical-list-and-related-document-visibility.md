---
type: decision
id: CFO-DEC-014
title: "물리 귀속 목록과 관련 문서 노출 분리"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - document-tree
  - knowledge-graph
  - visibility
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-005-single-physical-tree-multiple-logical-links]]"
    - "[[decision-010-document-relation-and-related-metadata]]"
  specs: []
  works: []
  releases: []
  related: []
up: []
---

# 물리 귀속 목록과 관련 문서 노출 분리

부서 기본 트리/목록에는 물리 귀속 문서만 노출한다. 논리 연결된 문서는 해당 부서의 관련 문서 영역에서 노출하고, 검색에서는 물리 귀속과 논리 연결 문서를 모두 찾을 수 있게 한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-005-single-physical-tree-multiple-logical-links]], [[decision-010-document-relation-and-related-metadata]]
- 문서는 물리 트리 위치 1개를 갖고, 여러 부서/제품과 논리적으로 연결될 수 있다.
- 부서 기본 목록은 문서 관리 주체를 나타내야 한다.
- 관련 문서는 지식그래프축 탐색에 가깝고, 실제 관리 주체와 섞이면 혼란이 생긴다.

## Decision

- 채택:
  - 부서 기본 트리/목록에는 해당 부서에 물리 귀속된 문서만 노출한다.
  - 논리 연결 문서는 기본 목록에 섞지 않는다.
  - 논리 연결 문서는 부서 상세의 `관련 문서` 탭/영역에 노출한다.
  - 검색 결과에는 물리 귀속 문서와 논리 연결 문서를 모두 포함할 수 있다.
  - 검색 결과에서는 `물리 귀속`과 `관련 문서` 출처를 구분해 표시한다.
  - 권한 없는 문서는 기본 목록, 관련 문서, 검색 결과 어디에서도 숨긴다.
- 기각:
  - 논리 연결 문서를 부서 기본 목록에 함께 노출하는 방식.
  - 관련 문서를 검색에서 제외하는 방식.
  - 권한 없는 관련 문서를 잠금 표시로 노출하는 방식.

## Visibility Rules

| 화면 | 물리 귀속 문서 | 논리 연결 문서 | 권한 없는 문서 |
|---|---|---|---|
| 부서 기본 트리/목록 | 노출 | 숨김 | 숨김 |
| 부서 관련 문서 영역 | 필요 시 제외 | 노출 | 숨김 |
| 검색 | 노출 | 노출 | 숨김 |
| 문서 상세 relation | 노출 | 노출 | 숨김 |

## 근거 개념

없음 — 목록·검색에서 무엇을 어디에 보일지 정한 노출 규칙이다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Department document list contract | 기본 목록은 physical ownership 기준 |
| Related document view contract | related department/product/relation 기반 관련 문서 노출 |
| Search result contract | physical/related 출처 표시와 권한 필터 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-501 | 논리 연결 문서는 부서 기본 목록에 섞지 않고 관련 문서 영역에 노출한다. 검색에서는 물리 귀속과 논리 연결 문서를 모두 찾을 수 있다. |
