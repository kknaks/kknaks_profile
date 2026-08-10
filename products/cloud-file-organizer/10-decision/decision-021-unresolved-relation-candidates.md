---
type: decision
id: CFO-DEC-021
title: "target 없는 relation 후보 처리"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - document-relation
  - approval
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-003-google-drive-document-sot]]"
    - "[[decision-010-document-relation-and-related-metadata]]"
    - "[[decision-020-v1-document-relation-types]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - foreign-key
  - object-graph
---

# target 없는 relation 후보 처리

AI가 `[[문서명]]` 같은 링크를 만들었지만 대상 문서가 DB에 없으면 새 문서를 자동 생성하지 않는다. 해당 링크는 `unresolved relation candidate`로 저장하고, 승인 게이트에서 관리자가 처리한다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-003-google-drive-document-sot]], [[decision-010-document-relation-and-related-metadata]], [[decision-020-v1-document-relation-types]]
- Google Drive가 파일 SoT다.
- DB document row는 Drive 파일을 대표해야 한다.
- target 없는 링크를 자동 문서로 생성하면 Drive 원본이 없는 문서가 생긴다.
- AI가 만든 wikilink는 후보 표현이며, DB relation은 승인 후 확정된다.

## Decision

- 채택:
  - target 문서가 없는 wikilink/relation 후보는 `unresolved relation candidate`로 저장한다.
  - unresolved 후보는 확정 graph에 반영하지 않는다.
  - target 없는 후보 때문에 새 document row를 자동 생성하지 않는다.
  - 승인 게이트에서 관리자는 기존 문서를 검색해 target을 지정할 수 있다.
  - 관리자는 unresolved 상태로 보류하거나 후보를 제거할 수 있다.
  - Drive에 실제 파일이 새로 들어오면 unresolved 후보를 다시 매칭할 수 있다.
- 기각:
  - target 없는 wikilink를 기준으로 DB 문서를 자동 생성하는 방식.
  - unresolved 후보를 승인 graph에 확정 relation으로 저장하는 방식.
  - Drive 원본 없는 placeholder document를 v1에서 만드는 방식.

## Approval Gate Actions

| Action | 처리 |
|---|---|
| target 지정 | 기존 document id와 연결해 relation 후보를 승인 가능 상태로 전환 |
| 보류 | unresolved 후보로 유지 |
| 제거 | 후보를 rejected/removed 처리 |
| 재매칭 | 새 Drive 문서 수집 후 title/drive_name 기반으로 후보 target 재검색 |

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[foreign-key]] — **대상 없는 참조를 확정 그래프에 넣지 않는다** — 없는 문서를 자동 생성하지도 않고, 보류 상태로 두었다가 사람이 대상을 지정한다
- [[object-graph]] — 해소되지 않은 후보를 그래프 밖에 두어, 확정 그래프에는 **실존하는 노드끼리의 엣지만** 남긴다

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Unresolved relation candidate contract | target 없는 후보 저장 구조 |
| Relation approval target selection contract | 관리자 target 지정/보류/제거 |
| Relation rematch contract | 신규 Drive 문서 수집 후 unresolved 후보 재검색 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-1002 | target 없는 wikilink는 새 문서 자동 생성 없이 unresolved relation candidate로 보관하고, 승인 게이트에서 관리자가 처리한다. |
