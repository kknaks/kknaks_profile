---
type: decision
id: CFO-DEC-018
title: "민감 문서 preset 추천과 승인 기준"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - sensitive-document
  - access-control
  - approval
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-008-sensitive-policy-context]]"
    - "[[decision-016-read-access-policy-and-boolean-vector]]"
    - "[[decision-017-global-sensitive-policy-source]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 민감 문서 preset 추천과 승인 기준

v1에서는 민감 문서 권한 preset을 AI가 자동 확정하지 않는다. AI는 민감 문서 유형과 named preset을 추천하고, 관리자가 승인 게이트에서 최종 확정한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-008-sensitive-policy-context]], [[decision-016-read-access-policy-and-boolean-vector]], [[decision-017-global-sensitive-policy-source]]
- 민감 문서 권한은 회사 공통 정책을 따라야 한다.
- preset이 전혀 없으면 승인자가 매번 권한 정책을 놓칠 수 있다.
- AI가 권한을 자동 확정하면 민감 문서 노출 사고가 생길 수 있다.

## Decision

- 채택:
  - 민감 문서 preset은 named policy로 관리한다.
  - AI는 문서 유형과 민감도에 따라 preset을 추천한다.
  - 추천 preset은 승인 전 후보 상태다.
  - 관리자가 승인 게이트에서 preset을 확정하거나 수정한다.
  - HR, 계약, 재무, 보안, 법무 문서는 기본적으로 `제한 필요` 후보로 표시한다.
  - preset은 read policy 필드(`read_roles`, `read_departments`, `read_positions`, `access_logic`)로 풀어서 저장할 수 있어야 한다.
  - 권한 없는 문서는 preset 여부와 무관하게 목록/트리/검색/관련 문서에서 숨긴다.
- 기각:
  - AI가 민감 문서 preset을 승인 없이 자동 확정하는 방식.
  - 민감 문서에도 아무 preset 후보를 제안하지 않는 방식.
  - 승인 게이트에서 이진수 권한 표현만 보고 preset을 확정하는 방식.

## Initial Preset Candidates

| Preset | 대상 문서 예시 | 기본 동작 |
|---|---|---|
| `HR_RESTRICTED` | 인사, 급여, 평가, 계약직/정규직 정보 | 제한 필요 후보 |
| `CONTRACT_RESTRICTED` | 계약서, NDA, 거래 조건 | 제한 필요 후보 |
| `FINANCE_RESTRICTED` | 매출, 정산, 비용, 세금 | 제한 필요 후보 |
| `SECURITY_RESTRICTED` | 보안 정책, credential 절차, 접근 통제 | 제한 필요 후보 |
| `LEGAL_RESTRICTED` | 법무 검토, 분쟁, 컴플라이언스 | 제한 필요 후보 |

## Approval Gate Behavior

| 상태 | 처리 |
|---|---|
| AI가 민감 문서로 판단 | preset 후보와 이유를 표시 |
| 관리자가 preset 승인 | read policy로 확정 저장 |
| 관리자가 preset 수정 | 수정된 named policy/read policy 저장 |
| 관리자가 민감 아님으로 판단 | preset 후보 제거 후 일반 policy로 승인 |

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Sensitive preset catalog contract | named preset 목록과 policy mapping |
| AI sensitive candidate contract | AI가 제안하는 민감도/preset/reason |
| Approval gate preset contract | 관리자 승인/수정/제거 동작 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-802 | 민감 preset은 AI 추천 후보로 두고 관리자가 승인한다. HR/계약/재무/보안/법무는 기본 제한 필요 후보로 표시한다. |
