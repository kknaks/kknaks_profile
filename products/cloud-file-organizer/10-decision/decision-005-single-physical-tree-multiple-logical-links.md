---
type: decision
id: CFO-DEC-005
title: "문서 귀속: 단일 물리 트리와 다중 논리 연결"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - document-ownership
  - knowledge-graph
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-002-document-metadata-foundation]]"
    - "[[decision-004-department-tree-organization-db]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - db-normalization
  - object-graph
---

# 문서 귀속: 단일 물리 트리와 다중 논리 연결

문서는 UI 트리상 하나의 물리적 위치에만 귀속된다. 여러 부서와 관련된 맥락은 문서 메타데이터/지식그래프의 논리적 연결로 표현한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-004-department-tree-organization-db]]
- 트리축은 사용자가 문서를 찾는 물리적 위치다.
- 지식그래프축은 문서가 여러 부서/제품/업무와 연결되는 논리적 관계다.
- 한 문서를 트리에 여러 번 배치하면 관리 주체와 중복 표시가 흐려질 수 있다.

## Decision

- 채택:
  - 문서는 물리적 트리 위치를 **정확히 1개** 가진다.
  - 물리적 트리 위치가 문서의 **관리 주체**를 의미한다.
  - 여러 부서가 관련된 경우, 해당 부서들은 논리적 연결로 표현한다.
  - 논리적 연결된 부서의 화면에서도 해당 문서를 볼 수 있다.
  - 논리적 연결은 문서 원본 위치를 바꾸지 않는다.
  - 문서 수정/관리 책임은 물리적 귀속 부서가 가진다.
- 기각:
  - 한 문서를 여러 트리 위치에 물리적으로 중복 배치하는 방식.
  - Drive 폴더 위치를 그대로 물리적 귀속으로 자동 확정하는 방식.
  - 관련 부서를 모두 관리 주체로 보는 방식.

## Model

| 개념 | Cardinality | 의미 |
|---|---:|---|
| physical_tree_path | 1 | 문서가 실제 UI 트리에서 놓이는 대표 위치 |
| owning_department | 1 | 문서 관리 주체. physical_tree_path의 부서 축과 정합해야 한다 |
| related_departments | 0..N | 문서와 관련된 부서. 해당 부서 탐색에서 문서가 노출될 수 있다 |
| related_products | 0..N | 문서와 관련된 제품/팀/프로젝트 |
| document_relations | 0..N | 다른 문서와의 논리 연결 |

## Example

```text
physical_tree_path:
  메디솔브 > HR > 계약 > 계약서

owning_department:
  HR

related_departments:
  개발팀
  링키팀

related_products:
  thready
```

이 경우 문서의 관리 주체는 HR이다. 다만 개발팀/링키팀 화면에서도 관련 문서로 탐색될 수 있다.

## Visibility Rules

- 사용자가 물리 트리에서 HR 계약서를 보면 이 문서는 원래 위치에 나타난다.
- 사용자가 개발팀 또는 링키팀 관련 문서를 보면 이 문서는 논리 연결 결과로 나타날 수 있다.
- 논리 연결로 노출된 문서는 원래 물리 경로를 함께 표시한다.
- 접근권한은 별도로 판단한다. 관련 부서라는 사실만으로 상세 접근권한을 자동 부여하지 않는다.

## Idempotency Rules

- 같은 문서는 하나의 `physical_tree_path`만 가진다.
- 같은 부서가 `related_departments`에 여러 번 들어와도 한 번만 저장/노출한다.
- 같은 물리 경로와 논리 연결을 여러 번 추천받아도 결과는 중복되지 않는다.
- 물리 위치 변경은 명시적 승인 action이어야 한다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[db-normalization]] — 문서의 관리 주체를 **정확히 하나**로 두고 나머지 관련성은 연결로 뺀다. 물리 위치를 여럿 두면 어느 것이 맞는지 정할 수 없다
- [[object-graph]] — 여러 부서와의 관련은 **트리가 아니라 그래프**로 표현한다 — 계층 하나로 담기지 않는 관계가 링크로 간다

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Document placement contract | physical tree path, owning department, related departments |
| Related department visibility | 논리 연결된 부서 화면에서 문서가 보이는 방식 |
| Ownership change workflow | 물리 위치/관리 주체 변경 승인 흐름 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-501 | 논리 연결 문서는 부서 목록에서 기본 노출할지, "관련 문서" 탭에만 노출할지 | DEC-014: 기본 목록은 물리 귀속, 논리 연결은 관련 문서 영역 |
| OQ-502 | related department가 있어도 접근권한이 없으면 목록에서 숨길지, 잠금 표시할지 | DEC-006: 숨김 |
| OQ-503 | physical_tree_path 변경 이력을 보존할지 | DEC-015: append-only history/audit 구조로 보존 |
