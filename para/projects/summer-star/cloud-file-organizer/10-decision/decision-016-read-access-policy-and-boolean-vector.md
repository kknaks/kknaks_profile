---
type: decision
id: CFO-DEC-016
title: "읽기 권한 policy와 boolean vector 사용 범위"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - access-control
  - metadata
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-006-read-access-from-user-attributes]]"
    - "[[decision-008-sensitive-policy-context]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - modifier-flags
---

# 읽기 권한 policy와 boolean vector 사용 범위

문서 metadata 원장은 사람이 이해할 수 있는 named policy로 저장한다. `1/0/1` 같은 boolean vector는 문서 metadata 원장에 저장하지 않고, 권한 판정 결과와 감사/debug 로그에서만 사용한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-006-read-access-from-user-attributes]], [[decision-008-sensitive-policy-context]]
- 사용자 정보는 부서, 직급, 권한 role을 가진다.
- 문서 접근 권한은 초기에는 읽기 기준만 다룬다.
- `role/department/position` 조건을 `1/0/1` 같은 이진 표현으로 관리하는 방안이 검토되었다.
- 그러나 boolean vector는 문서 자체의 속성이 아니라 특정 사용자와 문서의 판정 결과다.

## Decision

- 채택:
  - 문서 metadata DB에는 named access policy를 저장한다.
  - 기본 권한 필드는 `read_roles`, `read_departments`, `read_positions`, `sensitivity`, `access_logic`로 둔다.
  - 일반 문서의 기본 `access_logic`은 `ANY`다.
  - `ANY`는 role, department, position 조건 중 하나라도 만족하면 읽기 가능하다는 뜻이다.
  - 민감 문서는 `PRESET` 또는 `ALL` 같은 stricter policy를 사용할 수 있다.
  - boolean vector는 권한 판정 엔진 내부 결과로만 생성한다.
  - 필요하면 감사/debug 로그에 `role_match`, `department_match`, `position_match`, `final_readable`을 남긴다.
  - 권한 없는 문서는 기존 결정대로 목록/트리/검색/관련 문서에서 숨긴다.
- 기각:
  - 문서 metadata 원장에 `1/0/1` 같은 이진수 문자열을 저장하는 방식.
  - 관리자 승인 게이트에서 이진수만 보고 접근 정책을 승인하는 방식.
  - 모든 문서를 role/department/position의 AND 조건으로만 판정하는 방식.

## Access Policy Fields

| Field | 의미 |
|---|---|
| `read_roles` | 읽기 가능한 role 목록 |
| `read_departments` | 읽기 가능한 부서 목록 |
| `read_positions` | 읽기 가능한 직급 목록 |
| `sensitivity` | 문서 민감도 |
| `access_logic` | `ANY`, `ALL`, `PRESET` 같은 판정 방식 |

## Boolean Vector

| Field | 의미 | 저장 위치 |
|---|---|---|
| `role_match` | 사용자 role이 문서 policy와 일치하는지 | 판정 결과/log |
| `department_match` | 사용자 부서가 문서 policy와 일치하는지 | 판정 결과/log |
| `position_match` | 사용자 직급이 문서 policy와 일치하는지 | 판정 결과/log |
| `final_readable` | 최종 읽기 가능 여부 | 판정 결과/log |

예시:

```text
role_match / department_match / position_match
1 / 0 / 1
```

이 값은 문서별 고정 metadata가 아니라 특정 사용자 요청에 대한 계산 결과다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[modifier-flags]] — `1/0/1` 같은 **비트 압축 표현**을 원장에 두지 않는다는 결정. 압축된 플래그는 기계가 읽기엔 싸지만 사람이 읽을 수 없어, 판정 결과와 로그에서만 쓴다

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Access policy contract | named policy 필드와 `ANY`/`ALL`/`PRESET` 의미 |
| Access evaluation contract | 사용자 속성 기반 read 판정 |
| Access audit log contract | boolean vector와 final decision 로그 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-602 | 문서 metadata 원장은 named policy로 저장하고, boolean vector는 권한 판정 결과/log 용도로만 사용한다. |
