---
type: decision
id: CFO-DEC-012
title: "조직도와 문서 트리 설정의 경계"
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
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-004-department-tree-organization-db]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 조직도와 문서 트리 설정의 경계

조직도 DB는 사람의 소속과 권한 판단에 필요한 `회사 > 부서 > 팀`까지만 관리한다. 문서 탐색을 위한 `업무 > 문서종류` 계층은 별도의 문서 트리 설정에서 관리한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-004-department-tree-organization-db]]
- 부서별 문서 관리는 조직 구조와 문서 탐색 구조를 모두 필요로 한다.
- 조직도는 사용자 소속, 권한, 관리 책임의 기준이다.
- 업무 분류와 문서종류는 실제 문서 탐색 UX를 위한 분류이며 조직 개편보다 자주 바뀔 수 있다.

## Decision

- 채택:
  - 조직도 DB는 `회사 > 부서 > 팀`까지만 관리한다.
  - 사용자 정보의 `department`, `team`은 조직도 DB를 기준으로 한다.
  - 문서 트리 설정은 조직도 노드 아래에 붙는 `업무 > 문서종류` 계층을 관리한다.
  - 문서의 `physical_tree_path`는 조직도 노드와 문서 트리 설정 노드를 조합해 만든다.
  - 업무 분류 변경은 조직도 변경으로 보지 않는다.
- 기각:
  - `업무`를 조직도 DB의 정식 조직 단위로 넣는 방식.
  - 조직도와 문서 트리를 하나의 테이블/계층으로 합치는 방식.
  - 문서종류를 조직도 하위 단위처럼 관리하는 방식.

## Boundary

| 영역 | 포함 | 목적 |
|---|---|---|
| 조직도 DB | 회사, 부서, 팀 | 소속, 권한, 관리 주체 |
| 문서 트리 설정 | 업무, 문서종류 | 탐색, 분류, 승인 게이트 선택 |
| 문서 record | physical tree path | 특정 문서의 실제 UI 귀속 위치 |

## Example

```text
조직도 DB
메디솔브
|- 개발팀
|  |- 링키팀
|- HR

문서 트리 설정
메디솔브
|- 개발팀
|  |- 링키팀
|     |- 제품기획
|     |  |- PRD
|     |- 개발문서
|        |- API 문서
```

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Organization contract | 회사/부서/팀 모델과 사용자 소속 연결 |
| Document tree config contract | 업무/문서종류 노드 관리 |
| Physical tree path contract | 조직도 노드 + 문서 트리 노드 조합 방식 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-401 | 팀은 조직도 DB에 두고, 업무는 문서 트리 설정에 둔다. |
