---
type: decision
id: CFO-DEC-015
title: "physical_tree_path 변경 이력 보존"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - document-tree
  - audit
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-005-single-physical-tree-multiple-logical-links]]"
    - "[[decision-014-physical-list-and-related-document-visibility]]"
  specs: []
  works: []
  releases: []
  related: []
---

# physical_tree_path 변경 이력 보존

문서의 현재 `physical_tree_path`는 document row에 저장하고, 변경 이력은 별도 history/audit 구조에 append-only로 보존한다. Drive folder 이동은 제품 트리 이관으로 보지 않으며, 제품 내 명시적 이관 action만 path 변경 이력에 기록한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-005-single-physical-tree-multiple-logical-links]], [[decision-014-physical-list-and-related-document-visibility]]
- `physical_tree_path`는 문서의 물리 귀속과 관리 주체를 나타낸다.
- 문서 관리 주체가 바뀌면 나중에 감사, 책임 추적, 운영 이관 확인이 필요하다.
- 현재 탐색 경로와 변경 이력을 같은 필드에 섞으면 조회와 감사 목적이 섞인다.

## Decision

- 채택:
  - 현재 `physical_tree_path`는 document row에 저장한다.
  - `physical_tree_path` 변경 이력은 별도 history/audit 구조에 append-only로 저장한다.
  - path 변경은 제품 내 명시적 이관 action으로만 발생한다.
  - 이력에는 이전 path, 새 path, 변경자, 변경 사유, 변경 시각을 저장한다.
  - Drive parent/folder 이동은 제품 `physical_tree_path` 변경으로 자동 반영하지 않는다.
  - Drive folder 이동은 Drive mirror 필드에만 반영한다.
- 기각:
  - 현재 path만 저장하고 변경 이력을 버리는 방식.
  - Drive folder 이동을 제품 트리 이관으로 자동 처리하는 방식.
  - history row를 수정 가능한 상태로 두는 방식.

## History Fields

| Field | 의미 |
|---|---|
| `document_id` | 이관 대상 문서 |
| `from_physical_tree_path` | 이전 path |
| `to_physical_tree_path` | 새 path |
| `changed_by` | 변경자 |
| `changed_reason` | 변경 사유 |
| `changed_at` | 변경 시각 |

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Physical tree path contract | document row의 현재 path 저장 방식 |
| Document reassignment contract | 명시적 이관 action과 validation |
| Path history contract | append-only 변경 이력과 감사 조회 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-503 | `physical_tree_path` 변경 이력은 append-only history/audit 구조로 보존한다. |
