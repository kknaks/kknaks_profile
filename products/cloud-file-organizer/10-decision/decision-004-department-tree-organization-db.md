---
type: decision
id: CFO-DEC-004
title: "부서별 UI 트리와 조직도 DB 관리"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - department-tree
  - organization
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-002-document-metadata-foundation]]"
    - "[[decision-003-google-drive-document-sot]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 부서별 UI 트리와 조직도 DB 관리

문서 탐색용 트리축은 `회사 > 부서 > 팀/업무 > 문서종류`를 기본 구조로 둔다. 이 구조를 만들기 위한 조직도는 DB에서 관리한다.

> 이 결정은 UI상 보이는 트리축의 기본 골격을 정한다. 지식그래프축과 문서 관계 타입은 별도 결정/스펙에서 다룬다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 부서별로 흩어진 문서 관리를 통합하려면 UI에서 먼저 이해 가능한 부서 계층이 필요하다.
- 회사 전체 문서 체계를 처음부터 촘촘히 정의하기보다, 조직도를 기준으로 단순한 트리를 만든다.
- 조직은 변할 수 있으므로 문서 트리 기준을 하드코딩하면 유지보수가 어렵다.

## Decision

- 채택:
  - UI 트리 기본 구조는 **`회사 > 부서 > 팀/업무 > 문서종류`**로 간다.
  - 예시 경로는 `메디솔브 > HR > 계약 > 계약서`, `메디솔브 > 개발팀 > 링키팀 > 기획서`처럼 표현한다.
  - 제품/프로젝트 맥락(예: 쓰레디)은 트리 노드가 아니라 `related_products` 논리 연결로 표현한다.
  - 조직도는 DB에서 관리한다.
  - 부서/팀 노드는 조직도 DB를 source로 생성한다.
  - 문서종류 노드는 제품의 문서 분류 설정으로 관리한다.
  - 문서의 트리 귀속은 Drive 폴더 위치가 아니라 DB의 승인된 메타데이터/귀속값을 기준으로 한다.
- 기각:
  - Drive 폴더 구조를 그대로 제품 트리로 쓰는 방식.
  - 제품/부서/문서종류/프로젝트/관계를 모두 한 트리에 깊게 넣는 방식.
  - 조직도를 코드나 정적 문서에 하드코딩하는 방식.
- 보류:
  - 문서가 여러 부서와 관련될 때 트리 귀속을 복수 허용할지 여부.
  - 조직도 DB의 정확한 schema.
  - 조직도 변경 시 기존 문서 귀속을 자동 이동할지 여부.

## Tree Shape

```text
메디솔브
├── 개발팀
│   └── 링키팀
│       └── 기획서
└── HR
    └── 계약
        └── 계약서
```

## Data Ownership

| 데이터 | 관리 위치 | 용도 |
|---|---|---|
| 회사 | DB | 트리 root |
| 부서 | DB 조직도 | 1차 트리 노드 |
| 팀/업무 | DB 조직도 또는 조직 확장값 | 2차 트리 노드 |
| 문서종류 | DB 문서 분류 설정 | leaf 또는 하위 분류 |
| 문서 귀속 | DB 승인 메타데이터 | 문서가 UI 트리에 표시될 위치 |
| Drive 폴더 | Google Drive mirror | 참고 정보. 제품 트리 SoT 아님 |

## Organization DB Principle

- 조직도는 문서 트리의 기반 데이터다.
- 조직도에는 최소한 회사, 부서, 팀/업무 단위, 활성 여부가 필요하다.
- 조직 노드는 이름 변경/비활성화가 가능해야 한다.
- 비활성 조직 노드는 새 문서 귀속 후보에서 제외하되, 과거 문서 표시 정책은 후속 spec에서 정한다.
- 조직도 DB는 권한(role)과 동일 개념이 아니다. 예: HR 부서와 `hr` role은 연결될 수 있지만 같은 필드는 아니다.

## Idempotency Rules

- 같은 조직 노드는 중복 생성하지 않는다.
- 같은 문서가 같은 트리 경로에 여러 번 귀속되어도 UI에는 한 번만 표시된다.
- Drive 폴더 이동만으로 승인된 트리 귀속을 자동 변경하지 않는다.
- 조직도 이름 변경은 같은 조직 id를 유지한 채 UI 표시명만 바꾼다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Organization tree contract | 회사/부서/팀/업무 노드와 활성/비활성 lifecycle |
| Department document tree contract | 문서가 어떤 트리 경로에 표시되는지 |
| Document type catalog | 계약서, 기획서, 회의록 등 문서종류 관리 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-401 | 팀/업무 단위를 조직도에 둘지, 문서 트리 설정에 둘지 | DEC-012: 팀은 조직도 DB, 업무는 문서 트리 설정 |
| OQ-402 | 조직도 변경으로 비활성화된 부서의 기존 문서는 어디에 보일지 | DEC-013: 기존 path 유지, 일반 탐색 표시, 새 귀속 불가 |
| OQ-403 | 문서종류는 전사 공통 enum인지 부서별 enum인지 | DEC-007: 전사 공통 DB 카탈로그 |
