---
type: decision
id: CFO-DEC-010
title: "문서 relation과 related metadata 승인 기준"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - document-relation
  - knowledge-graph
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
---

# 문서 relation과 related metadata 승인 기준

UI/AI에서는 `[[문서명]]` 스타일 링크 표현을 허용하지만, 문서 연결의 Source of Truth는 DB relation이다. 관련 부서/제품은 AI 후보로 생성되며, 최종값은 사람 승인 후 확정된다.

## Context

- 관련 baseline: [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-002-document-metadata-foundation]], [[decision-005-single-physical-tree-multiple-logical-links]]
- 트리축은 문서의 물리 위치를 1개만 갖고, 관련 맥락은 지식그래프축에서 표현한다.
- 사람이 이해하기 쉬운 링크 표현과 DB의 안정적인 relation 저장 방식을 분리해야 한다.

## Decision

- 채택:
  - UI/AI 입출력에서는 `[[문서명]]` 스타일 링크 표현을 허용한다.
  - DB의 확정 연결 SoT는 `document_relations` 같은 relation/edge 구조다.
  - AI가 만든 wikilink 표현은 backend가 후보 relation으로 정규화한다.
  - 사람 승인 전에는 후보 relation을 확정 graph에 반영하지 않는다.
  - 승인 후 relation은 문서 id 기준으로 저장한다.
  - 문서명이 바뀌어도 relation은 문서 id 기준으로 유지한다.
  - `related_department`, `related_product`는 AI 후보로 생성될 수 있지만 최종값은 승인 필드다.
  - 같은 relation은 `(source_document_id, target_document_id, relation_type)` 기준으로 중복 저장하지 않는다.
- 기각:
  - wikilink 문자열 자체를 최종 graph SoT로 쓰는 방식.
  - AI가 추천한 관련 부서/제품/relation을 승인 없이 바로 확정하는 방식.
  - 문서명 문자열 매칭만으로 영구 relation을 유지하는 방식.

## Relation Model

| Field | 의미 |
|---|---|
| `source_document_id` | 연결을 시작하는 문서 id |
| `target_document_id` | 연결 대상 문서 id |
| `relation_type` | 연결 타입 |
| `source_label` | UI/AI에서 쓰인 원문 링크 라벨 |
| `approved_by` | 승인자 |
| `approved_at` | 승인 시각 |

## Related Metadata Model

| Field | 후보 생성 | 최종 반영 |
|---|---|---|
| `related_departments` | AI 가능 | 사람 승인 필요 |
| `related_products` | AI 가능 | 사람 승인 필요 |
| `document_relations` | AI 가능 | 사람 승인 필요 |

## Normalization Rules

- `[[문서명]]`은 후보 target 문서 검색 키로 사용한다.
- 같은 이름의 문서가 여러 개면 승인 게이트에서 사람이 대상 문서를 선택해야 한다.
- 대상 문서가 아직 없으면 unresolved relation 후보로 둔다.
- unresolved relation은 확정 graph가 아니라 승인 대기 후보로만 남긴다.
- 승인된 relation은 문서 id 기준으로 저장한다.

## Idempotency Rules

- 같은 `(source_document_id, target_document_id, relation_type)`은 한 번만 저장한다.
- 같은 wikilink 후보가 여러 번 생성되어도 후보 fingerprint가 같으면 중복 생성하지 않는다.
- 문서 title이 바뀌어도 승인된 relation은 유지한다.
- target 문서가 삭제/removed 상태가 되면 relation은 삭제하지 않고 broken/removed 상태로 표시할 수 있다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Relation candidate contract | AI wikilink 후보와 unresolved relation 처리 |
| Relation approval contract | 승인 게이트에서 target 문서 선택/승인 |
| Graph relation contract | 승인 relation 저장과 중복 방지 |
| Related metadata contract | related department/product 후보와 승인 필드 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-1001 | v1 relation_type 기본 목록은 무엇으로 둘 것인가? | DEC-020: related/references/supersedes/duplicate_candidate |
| OQ-1002 | target 문서가 없는 wikilink 후보를 새 문서 생성 후보로 연결할지 | DEC-021: unresolved relation candidate로 보관, 자동 생성 없음 |
