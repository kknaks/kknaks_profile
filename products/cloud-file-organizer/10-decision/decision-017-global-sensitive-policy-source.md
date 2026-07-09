---
type: decision
id: CFO-DEC-017
title: "민감 문서 정책의 전역 단일 원장"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - policy
  - sensitive-document
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-008-sensitive-policy-context]]"
    - "[[decision-016-read-access-policy-and-boolean-vector]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 민감 문서 정책의 전역 단일 원장

민감 문서 정책은 제품별로 분리하지 않고 전역 `context/policy.md`를 단일 원장으로 유지한다. 나중에 운영 복잡도가 커지면 같은 정책 원장을 DB 테이블 형태로 승격할 수 있다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-008-sensitive-policy-context]], [[decision-016-read-access-policy-and-boolean-vector]]
- 민감 문서 판단과 접근권한 기본 정책은 회사 공통 정책 성격이 강하다.
- 제품별 정책 파일을 바로 분리하면 중복과 불일치가 생길 수 있다.
- 현재는 demo/baseline 단계이므로 정책이 한 곳에서 관리되는 것이 더 안전하다.

## Decision

- 채택:
  - 민감 문서 정책의 현재 SoT는 전역 `context/policy.md`다.
  - Claude/agent는 민감도, 권한, 승인 게이트 판단 시 전역 정책을 먼저 읽는다.
  - 제품별 정책 파일은 v1에서 만들지 않는다.
  - 나중에 정책을 DB 테이블로 관리할 수 있도록 policy 항목은 구조화 가능한 형태로 유지한다.
  - DB 테이블로 승격해도 정책 원장은 하나만 둔다.
- 기각:
  - 제품별로 민감 문서 정책 파일을 즉시 분리하는 방식.
  - 제품마다 서로 다른 민감도 기준을 독립 관리하는 방식.
  - `context/policy.md`와 DB 정책 테이블을 동시에 원장으로 두는 방식.

## Future Direction

정책이 운영 데이터가 되면 다음처럼 DB 테이블로 승격할 수 있다.

| Candidate Table | 목적 |
|---|---|
| `policy_rules` | 민감 문서 판단 rule |
| `policy_presets` | HR/계약/재무/보안 같은 기본 접근 preset |
| `policy_versions` | 정책 변경 이력 |

이 경우에도 `context/policy.md`는 원장이 아니라 agent가 참조할 정책 설명/프롬프트 가이드로 전환한다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Global policy contract | `context/policy.md`의 적용 범위 |
| Policy-to-access preset contract | 민감도 policy와 read access preset 연결 |
| Policy evolution contract | 파일 기반 정책에서 DB 정책으로 승격하는 조건 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-801 | 민감 문서 정책은 전역 `context/policy.md`를 단일 원장으로 유지한다. 나중에 DB 테이블로 승격할 수 있다. |
