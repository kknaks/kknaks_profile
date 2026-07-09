---
type: decision
id: CFO-DEC-013
title: "비활성 조직의 기존 문서 노출 기준"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - organization
  - document-tree
  - visibility
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-004-department-tree-organization-db]]"
    - "[[decision-012-organization-and-document-tree-boundary]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 비활성 조직의 기존 문서 노출 기준

조직도에서 부서나 팀이 비활성화되어도, 그 조직에 물리 귀속된 기존 문서는 기존 `physical_tree_path`를 유지한다. 일반 탐색에서는 숨기지 않고, 비활성 조직 표시와 기존 읽기 권한을 함께 적용한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-004-department-tree-organization-db]], [[decision-012-organization-and-document-tree-boundary]]
- 조직 개편으로 부서/팀이 사라지거나 비활성화될 수 있다.
- 기존 문서는 계약, 감사, 히스토리 관점에서 계속 찾을 수 있어야 한다.
- 조직도 변경이 문서 귀속을 자동 변경하면 관리 주체와 이력이 불명확해질 수 있다.

## Decision

- 채택:
  - 조직도 노드는 삭제하지 않고 `inactive` 상태로 비활성화한다.
  - 비활성 조직에 귀속된 기존 문서의 `physical_tree_path`는 유지한다.
  - 일반 탐색에서 비활성 조직과 기존 문서를 숨기지 않는다.
  - 비활성 조직/팀은 UI에서 `inactive` 상태로 표시한다.
  - 접근 권한은 기존 read policy를 그대로 적용한다.
  - 비활성 조직은 새 문서의 귀속 대상으로 선택할 수 없다.
  - 문서 관리자가 필요하면 별도 이관 action으로 `physical_tree_path`를 변경한다.
- 기각:
  - 비활성 조직의 기존 문서를 일반 탐색에서 숨기는 방식.
  - 조직도 변경 시 기존 문서의 물리 귀속을 자동으로 다른 부서로 옮기는 방식.
  - 비활성 조직 노드를 hard delete하는 방식.

## State Rules

| 대상 | 상태 | 처리 |
|---|---|---|
| 조직도 노드 | `active` | 새 문서 귀속 가능 |
| 조직도 노드 | `inactive` | 기존 문서 조회 가능, 새 귀속 불가 |
| 기존 문서 | active document | `physical_tree_path` 유지 |
| 신규 문서 | approval candidate | inactive 조직 선택 불가 |

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Organization lifecycle contract | 조직도 노드 active/inactive 처리 |
| Tree visibility contract | inactive 조직과 기존 문서 표시 규칙 |
| Reassignment contract | 문서 관리자가 명시적으로 이관하는 action |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-402 | 비활성 조직의 기존 문서는 기존 `physical_tree_path`에 유지하고 일반 탐색에서 표시한다. 단, 새 문서 귀속 대상으로는 선택할 수 없다. |
