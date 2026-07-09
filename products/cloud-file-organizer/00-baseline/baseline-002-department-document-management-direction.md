---
type: baseline
id: CFO-BASE-002
title: "부서별 문서 관리와 트리/지식그래프 이중 축"
status: accepted
product: cloud-file-organizer
source:
  type: conversation
  ref: "사용자 구두 정리 2026-07-08"
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
  decisions:
    - "[[decision-002-document-metadata-foundation]]"
    - "[[decision-004-department-tree-organization-db]]"
    - "[[decision-005-single-physical-tree-multiple-logical-links]]"
    - "[[decision-008-sensitive-policy-context]]"
  specs: []
  works: []
  releases: []
  related:
    - "/Users/kknaks/git/harness_works/mediness-mediness/context"
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/baseline
  - status/accepted
  - department-documents
  - knowledge-graph
---

# 부서별 문서 관리와 트리/지식그래프 이중 축

부서별로 흩어진 문서 관리 방식을 통합하고, UI상 트리와 메타데이터 기반 지식그래프를 분리해서 생각한다.

> 이 baseline의 핵심 방향은 decision으로 승격했다. 남은 세부 이슈는 `10-decision/README.md`와 후속 spec에서 닫는다.

## Raw

- 방향을 잘못 잡았다.
- 부서별로 문서를 관리하는 게 목표다.
- 지금 각 부서가 개별 방식(외장하드/네이버/공유드라이브 등)을 가지고 있다.
- 최종 파일은 부서별 계층화로 갈 것이다.
- 문서 간 메타데이터들이 연결되면 사실 트리구조는 크게 의미가 없다고 본다.
- 예시:

```text
메디솔브
├── 개발팀
│   └── 링키팀
└── HR
    └── 계약서
        └── 쓰레디
```

- 두 개의 축으로 생각해야 한다.
  - 지식그래프축: 메타데이터
  - 트리축: UI상 보이는 구조
- 서로 싱크는 항상 멱등해야 한다.

## Context

- 기존 SPEC 초안은 개발/API 관점이 강했고, 아직 회사 전체 문서 체계가 없는 현실과 맞지 않았다.
- 현재 필요한 것은 기능 계약이 아니라 제품 문제의 방향을 더 관찰하고 샘플 데이터로 가다듬는 것이다.
- Google Drive 데모는 입력 채널일 뿐, 핵심 문제는 부서별 문서 통합 관리다.

## Why It Matters

- 각 부서가 서로 다른 저장 방식으로 문서를 관리하면 검색, 인수인계, 권한 관리, 문서 간 관계 파악이 어렵다.
- 단순 트리만 고도화하면 폴더 정리를 강제하는 문제로 돌아갈 수 있다.
- 반대로 지식그래프만 있으면 사용자가 익숙하게 탐색할 UI 구조가 부족할 수 있다.
- 따라서 UI 트리와 메타데이터/관계 그래프를 분리해서 생각할 필요가 있다.

## Possible Direction

- 트리축은 부서/팀/업무 단위의 단순한 탐색 구조로 둔다.
- 부서별 UI 트리 기준은 [[decision-004-department-tree-organization-db]]에서 `회사 > 부서 > 팀/업무 > 문서종류`로 정리한다.
- 지식그래프축은 문서의 메타데이터, 관련 제품, 계약, 부서, 사람, 문서 간 관계를 표현한다.
- 같은 문서는 하나의 원장을 기준으로 트리 귀속과 그래프 관계를 연결한다.
- 문서 귀속은 [[decision-005-single-physical-tree-multiple-logical-links]]에서 단일 물리 트리 위치와 다중 논리 연결로 정리한다.
- 싱크는 멱등해야 한다. 같은 파일/관계/귀속을 여러 번 처리해도 중복이 생기지 않아야 한다.
- 샘플 데이터를 먼저 만들고, 그 샘플을 기준으로 decision/spec을 다시 만든다.
- 메타데이터 기본 축은 [[decision-002-document-metadata-foundation]]에서 먼저 정리한다.

## Resolution

| ID | Question | Next |
|---|---|---|
| OQ-201 | 샘플 데이터의 첫 부서/팀/문서 종류는 무엇으로 둘 것인가? | DEC-004: 기본 트리 `회사 > 부서 > 팀/업무 > 문서종류` |
| OQ-202 | 계약서 같은 민감 문서는 트리 노출과 그래프 연결을 어디까지 허용할 것인가? | DEC-006/DEC-008: 권한 없으면 숨김, 민감 정책은 `context/policy.md` |
| OQ-203 | 문서가 여러 부서와 관련될 때 트리 귀속은 하나만 둘 것인가, 보조 귀속을 허용할 것인가? | DEC-005: 물리 트리 위치 1개 + 논리 연결 N개 |
| OQ-204 | 외장하드/네이버/공유드라이브 등 기존 저장소는 데모에서 어떻게 표현할 것인가? | 현재 없음. v1 데모에서는 다루지 않음 |
