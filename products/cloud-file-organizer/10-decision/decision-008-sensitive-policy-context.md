---
type: decision
id: CFO-DEC-008
title: "민감 문서 정책 컨텍스트와 Claude 진입 흐름"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - sensitive-documents
  - policy
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-006-read-access-from-user-attributes]]"
  specs: []
  works: []
  releases: []
  related:
    - "../../../context/policy.md"
---

# 민감 문서 정책 컨텍스트와 Claude 진입 흐름

민감 문서 판단은 제품 코드에 하드코딩하지 않고 `context/policy.md`에 정책 컨텍스트로 둔다. 로컬 Claude/agent는 문서 민감도나 권한 후보를 판단할 때 이 정책과 사용자 프롬프트를 함께 읽는다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-006-read-access-from-user-attributes]]
- 권한 없는 문서는 숨김으로 결정했다.
- 다음으로 필요한 것은 계약서/인사/재무 같은 민감 문서의 기본 policy 추천 기준이다.
- 로컬 Claude는 작업 시작 시 `CLAUDE.md`를 먼저 읽고, 이 레포는 `CLAUDE.md -> agent.md -> context/index.md` 흐름을 가진다.

## Decision

- 채택:
  - 민감 문서 정책은 `context/policy.md`에 둔다.
  - 로컬 Claude/agent는 문서 민감도, read policy, 승인 게이트 관련 판단을 할 때 `context/policy.md`를 읽는다.
  - 민감 문서 정책은 AI 추천 기준이며 최종 권한은 사람이 승인한다.
  - 계약, 인사, 재무, 보안, 법무 문서는 민감 문서 후보로 본다.
  - 민감 문서 후보는 `needs_human_review=true`로 추천한다.
  - 문서 본문에 secret이 있으면 값을 복사하지 않고 위험만 표시한다.
- 기각:
  - 민감 문서 정책을 제품 코드에만 하드코딩하는 방식.
  - 민감 문서를 AI가 자동 승인하는 방식.
  - 관련 부서 연결만으로 민감 문서 읽기 권한을 자동 부여하는 방식.

## Claude Read Flow

```text
CLAUDE.md
-> agent.md
-> context/index.md
-> context/policy.md (문서 민감도/권한/승인 게이트 판단 시)
-> 사용자 프롬프트
```

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Sensitive document classification | 민감 문서 후보 판정과 이유 표시 |
| Read policy suggestion | `read_roles`, `read_departments`, `read_positions` 추천 |
| Approval gate risk panel | 민감 문서 후보와 human review 표시 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-801 | `context/policy.md`를 제품별로 분리할지, 전역 정책으로 유지할지 | DEC-017: 전역 `context/policy.md` 단일 원장 |
| OQ-802 | 민감 문서 후보별 기본 role/department preset을 어디까지 고정할지 | DEC-018: AI 추천 후보 + 관리자 승인 |
