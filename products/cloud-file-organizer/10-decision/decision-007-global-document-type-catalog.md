---
type: decision
id: CFO-DEC-007
title: "전사 공통 문서종류 카탈로그와 승인 게이트 추가"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - document-type
  - approval-gate
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

# 전사 공통 문서종류 카탈로그와 승인 게이트 추가

문서종류는 전사 공통 DB 카탈로그로 관리한다. 승인 게이트에서 적절한 문서종류가 드롭다운에 없으면 관리자만 새 문서종류를 추가할 수 있다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-004-department-tree-organization-db]]
- DEC-004에서 UI 트리 기본 구조를 `회사 > 부서 > 팀/업무 > 문서종류`로 정했다.
- 따라서 문서종류는 트리축의 leaf이자 AI 분류 후보가 된다.
- 부서마다 다른 문서종류를 무제한 만들면 트리가 다시 파편화될 수 있다.

## Decision

- 채택:
  - 문서종류는 **전사 공통 카탈로그**로 관리한다.
  - 문서종류 카탈로그는 DB에 저장한다.
  - 승인 게이트에는 문서종류 드롭다운을 제공한다.
  - 드롭다운에 적절한 값이 없으면 관리자가 새 문서종류를 추가할 수 있다.
  - 추가된 문서종류는 전사 공통 카탈로그에 반영된다.
  - AI는 전사 공통 카탈로그를 기준으로 문서종류를 추천한다.
  - 새 문서종류 추가는 중복/유사어 검사를 거쳐야 한다.
  - v1에서는 유사 문서종류 merge를 하지 않는다.
  - v1에서는 부서별 자주 쓰는 문서종류 shortcut을 제공하지 않는다.
- 기각:
  - 부서별로 완전히 분리된 문서종류 enum을 운영하는 방식.
  - 코드에 문서종류를 하드코딩하는 방식.
  - AI가 추천한 새 문서종류를 사람 승인 없이 자동 추가하는 방식.
- 보류:
  - v1 이후 문서종류 merge/rename/deprecate 정책.

## Initial Catalog Candidates

초기 샘플은 아래 정도로 시작한다. 최종값은 샘플 데이터와 승인 게이트 사용 중 조정한다.

| Document Type | 예시 |
|---|---|
| 계약서 | 병원/외부업체/제품 계약 |
| 회의록 | 회의 정리, 의사결정 기록 |
| 기획서 | 제품/기능 기획 |
| 요구사항 | 고객 요청, 내부 요구 |
| 정책 | 권한, 운영, 보안, 인사 정책 |
| 레퍼런스 | 외부 자료, 조사 자료 |
| 보고서 | 주간/월간/성과 보고 |
| 산출물 | 디자인, 개발, QA 결과물 |

## Approval Gate Rule

- 승인자는 AI 추천 문서종류를 그대로 승인할 수 있다.
- 추천값이 틀리면 기존 드롭다운에서 다른 문서종류를 선택할 수 있다.
- 드롭다운에 없으면 관리자만 새 문서종류를 추가할 수 있다.
- 새 문서종류 추가 시 이름은 전사 공통 카탈로그에서 unique해야 한다.
- 기존 문서종류와 유사해도 v1에서는 merge flow를 제공하지 않는다. 중복으로 판단되면 새로 만들 수 없다.
- 새 문서종류가 추가되어도 기존 문서들의 문서종류는 자동 변경하지 않는다.
- 일반 승인자는 드롭다운에 없는 문서종류가 필요하면 관리자에게 추가를 요청한다.

## Idempotency Rules

- 같은 이름의 문서종류는 중복 생성하지 않는다.
- 대소문자/공백/간단한 표기 차이는 정규화 후 중복 검사한다.
- 같은 승인 요청이 재시도되어도 문서종류는 하나만 생성된다.
- 문서종류가 rename되어도 문서 record는 stable type id를 참조해야 한다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Document type catalog contract | 전사 공통 문서종류 CRUD, 중복 검사, 활성/비활성 |
| Approval gate type selection | 승인 화면의 드롭다운/추가 UX |
| AI type suggestion | AI가 카탈로그 기반으로 문서종류를 추천하는 규칙 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-701 | 새 문서종류 추가 권한은 모든 승인자에게 줄지 관리자에게만 줄지 | closed: 관리자만 |
| OQ-702 | 유사 문서종류 merge는 누가 승인할지 | closed: v1 제외 |
| OQ-703 | 부서별 자주 쓰는 문서종류 shortcut을 둘지 | closed: v1 제외 |
