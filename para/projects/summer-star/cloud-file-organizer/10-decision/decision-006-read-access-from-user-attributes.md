---
type: decision
id: CFO-DEC-006
title: "사용자 속성 기반 문서 읽기 권한"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - access-control
  - user
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-002-document-metadata-foundation]]"
    - "[[decision-005-single-physical-tree-multiple-logical-links]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - role-based-entity
---

# 사용자 속성 기반 문서 읽기 권한

문서 접근 권한은 사용자 DB의 부서, 직급, 권한(role)을 기준으로 판정한다. 초기 범위는 읽기 권한만 다룬다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-005-single-physical-tree-multiple-logical-links]]
- 관련 부서로 논리 연결된 문서가 보일 수 있지만, 관련 부서라는 사실만으로 상세 접근권한을 자동 부여하면 안 된다.
- 사용자 정보에 부서/직급/권한을 관리하면 문서 접근권한을 일관되게 판정할 수 있다.

## Decision

- 채택:
  - 사용자 정보는 DB에서 관리한다.
  - 사용자 정보에는 최소한 **부서**, **직급**, **권한(role)** 이 필요하다.
  - 문서 접근 제어의 초기 범위는 **읽기 권한**만 다룬다.
  - 문서 읽기 권한은 문서 메타데이터와 사용자 속성을 비교해 판정한다.
  - 관련 부서(`related_departments`)는 탐색/추천 맥락이며, 읽기 권한을 자동 부여하지 않는다.
  - 물리 귀속 부서(`owning_department`)도 권한 판정의 입력이 될 수 있지만, 단독으로 전체 권한을 보장하지 않는다.
  - 최종 읽기 가능 여부는 사용자 속성과 문서의 read policy를 함께 본다.
  - 읽기 권한이 없는 문서는 목록/트리/검색/관련 문서 결과에서 보이지 않는다.
- 기각:
  - Drive 폴더 권한만으로 제품 문서 읽기 권한을 판단하는 방식.
  - related department에 포함되면 자동으로 상세 읽기를 허용하는 방식.
  - 쓰기/수정/삭제 권한까지 초기 decision에서 함께 다루는 방식.
- 보류:
  - 쓰기/수정/삭제 권한.
  - 직급별 세부 권한 matrix.

## User Attributes

| Field | 의미 | 예시 | 용도 |
|---|---|---|---|
| `department` | 사용자 소속 부서 | `HR`, `개발팀` | 부서 기반 읽기 판정 |
| `position` | 직급/책임 수준 | `staff`, `leader`, `cto` | 직급 기반 예외/상위 권한 |
| `role` | 시스템 권한 | `admin`, `member`, `hr`, `dev` | 기능 접근 및 문서 read policy |

## Document Read Policy

문서에는 읽기 권한 판정을 위한 policy가 필요하다.

| Field | 의미 | 예시 |
|---|---|---|
| `read_roles` | 읽을 수 있는 role 목록 | `admin`, `hr` |
| `read_departments` | 읽을 수 있는 부서 목록 | `HR`, `개발팀` |
| `read_positions` | 읽을 수 있는 직급/책임 수준 | `leader`, `cto` |
| `sensitivity` | 민감도 | `normal`, `sensitive` |

## Read Decision Rule

초기 규칙은 단순하게 둔다.

1. `admin` role은 모든 문서를 읽을 수 있다.
2. 사용자의 role이 문서 `read_roles`에 있으면 읽을 수 있다.
3. 사용자의 department가 문서 `read_departments`에 있으면 읽을 수 있다.
4. 사용자의 position이 문서 `read_positions`에 있으면 읽을 수 있다.
5. 위 조건에 모두 해당하지 않으면 읽을 수 없다.

## Visibility Principle

- 읽기 권한 판정은 상세 접근의 기준이다.
- 목록/트리/검색/관련 문서 노출도 읽기 권한 판정을 따른다.
- 읽기 권한이 없으면 잠금 표시가 아니라 숨김 처리한다.
- 민감 문서는 기본적으로 같은 규칙을 따르며, 별도 예외가 필요하면 후속 spec에서 더 좁게 제한한다.
- AI는 read policy 후보를 제안할 수 있지만, 최종 권한은 사람이 승인해야 한다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[role-based-entity]] — 부서·직급·role 을 **사용자 속성으로** 두고 그것으로 권한을 판정한다. 사람마다 권한을 따로 붙이지 않는다

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| User attribute contract | 사용자 부서/직급/권한 데이터 |
| Document read policy contract | 문서별 읽기 policy 필드와 판정 규칙 |
| Read visibility contract | 목록 노출/잠금/숨김 정책 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-601 | 목록 노출은 읽기 권한이 없을 때 숨김인가, 잠금 표시인가? | closed: 숨김 |
| OQ-602 | `role`, `department`, `position` 중 충돌 시 우선순위는 어떻게 둘 것인가? | DEC-016: 일반 문서는 ANY, 민감 문서는 PRESET/ALL 가능 |
| OQ-603 | 민감 문서의 기본 policy는 무엇인가? | DEC-008: `context/policy.md` |
