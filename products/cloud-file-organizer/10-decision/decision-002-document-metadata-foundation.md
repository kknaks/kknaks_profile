---
type: decision
id: CFO-DEC-002
title: "문서 메타데이터 기본 정의"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - metadata
  - access-control
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-001-google-drive-demo-intake]]"
    - "[[decision-003-google-drive-document-sot]]"
    - "[[decision-005-single-physical-tree-multiple-logical-links]]"
    - "[[decision-006-read-access-from-user-attributes]]"
    - "[[decision-008-sensitive-policy-context]]"
    - "[[decision-010-document-relation-and-related-metadata]]"
    - "[[decision-011-drive-sync-state-and-pending-approval-conflict]]"
    - "[[decision-016-read-access-policy-and-boolean-vector]]"
    - "[[decision-018-sensitive-document-preset-approval]]"
    - "[[decision-020-v1-document-relation-types]]"
    - "[[decision-021-unresolved-relation-candidates]]"
    - "[[decision-023-drive-composite-fingerprint]]"
  specs: []
  works: []
  releases: []
  related: []
---

# 문서 메타데이터 기본 정의

DB에 기록하는 문서 메타데이터는 Google Drive mirror, 제품 관리 정보, 접근 policy, AI 후보/승인값, 문서 relation을 기본 축으로 가진다. 파일 원본의 SoT는 [[decision-003-google-drive-document-sot]]를 따른다.

> 이 결정은 문서 metadata의 baseline 원장 구조를 확정한다. 세부 컬럼/enum은 spec에서 구체화한다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]], [[baseline-002-department-document-management-direction]]
- Google Drive는 파일 원본 SoT이고, 제품 내부 DB에는 메타데이터/인덱스/승인 상태가 필요하다.
- 문서 탐색은 두 축으로 갈 가능성이 높다.
  - 트리축: UI상 보이는 부서별 계층
  - 지식그래프축: 문서 메타데이터와 문서 간 연결
- 관련 decision들이 닫히면서 metadata의 기본 원장 구조는 spec으로 내릴 수 있는 상태가 되었다.

## Decision

- 채택:
  - 모든 문서는 제품 내부 DB에 **문서 record**를 가진다.
  - 문서 record는 원본 Drive 파일을 `drive_file_id`와 링크로 참조한다.
  - Google Drive에서 온 값은 Drive mirror 필드로 분리한다.
  - 문서의 기본 표시 제목은 `drive_name`이다.
  - 제품 트리 귀속은 `physical_tree_path`와 `owning_department`로 관리한다.
  - 논리 연결은 `related_departments`, `related_products`, DB `document_relations`로 관리한다.
  - 문서 간 연결의 SoT는 DB relation이고, UI/AI 표현에서 `[[...]]` 스타일 표기를 사용할 수 있다.
  - 접근권한은 named access policy로 저장한다.
  - boolean vector는 metadata 원장이 아니라 판정 결과/log로만 사용한다.
  - 생성부서와 귀속부서는 분리한다.
  - AI는 메타데이터 값을 제안할 수 있지만, 최종값은 사람 승인 후 확정된다.
- 기각:
  - `1/0/1` 같은 이진수 문자열을 문서 metadata 원장으로 저장하는 방식.
  - wikilink 문자열 자체를 relation SoT로 쓰는 방식.
  - Drive 원본 없는 placeholder document를 자동 생성하는 방식.

## Metadata Foundation

| Field | 의미 | 예시 | 성격 |
|---|---|---|---|
| `source_provider` | 원본 저장소 | `google_drive` | system |
| `drive_file_id` | Drive 파일 id | Drive file id | system / mirror |
| `drive_name` | Drive 파일명이며 기본 표시 제목 | `쓰레디 계약서 v1.docx` | system / mirror |
| `drive_web_url` | 원본 파일 열기 링크 | Drive webViewLink | system / mirror |
| `drive_mime_type` | Drive MIME type | Google Docs, PDF, XLSX | system / mirror |
| `drive_state` | Drive 기반 문서 상태 | `active`, `trashed`, `removed`, `out_of_scope` | system / mirror |
| `drive_fingerprint` | 승인 stale 판정 기준 | modifiedTime/name/mime/content hash 조합 | system / mirror |
| `document_type` | 문서 종류 | `계약서`, `회의록`, `기획서` | approved |
| `created_department` | 문서를 만든 부서 | `HR` | approved |
| `owning_department` | 문서를 관리/귀속하는 부서. DEC-005에 따라 단일값 | `HR` | approved |
| `physical_tree_path` | UI 트리상 물리 귀속 위치 | `메디솔브/개발팀/링키팀/개발문서/API 문서` | approved |
| `related_departments` | 관련 부서 | `개발팀`, `링키팀` | suggested -> approved |
| `related_products` | 관련 제품/팀 | `linky`, `thready` | suggested -> approved |
| `read_roles` | 읽기 가능한 role 목록 | `admin`, `manager` | approved / auth |
| `read_departments` | 읽기 가능한 부서 목록 | `HR`, `개발팀` | approved / auth |
| `read_positions` | 읽기 가능한 직급/책임 수준 | `leader`, `cto` | approved / auth |
| `access_logic` | 권한 판정 방식 | `ANY`, `ALL`, `PRESET` | approved / auth |
| `sensitivity` | 민감도 | `normal`, `sensitive` | suggested -> approved |
| `policy_preset` | 민감 문서 권한 preset | `HR_RESTRICTED` | suggested -> approved |
| `summary` | 문서 요약 | 한두 문장 요약 | suggested -> approved |
| `document_relations` | 문서 간 연결 | DB relation, UI/AI는 `[[문서명]]` 표현 가능 | suggested -> approved / graph |

## Document Link Principle

- 문서 간 연결의 SoT는 DB relation이다.
- 사람이 이해 가능한 `[[문서명]]` 스타일 링크는 UI/AI 입출력 표현으로 사용할 수 있다.
- 같은 링크가 여러 번 생성되어도 그래프 관계는 중복되지 않아야 한다.
- 링크는 트리 귀속을 대체하지 않는다. 트리는 UI 위치이고, 링크는 문서 간 의미 연결이다.
- AI는 링크 후보를 제안할 수 있지만, 승인 전에는 최종 그래프에 반영하지 않는다.

## Department Principle

- `created_department`는 문서를 만든 부서다.
- `owning_department`는 문서를 관리하고 책임지는 부서이며, [[decision-005-single-physical-tree-multiple-logical-links]]에 따라 단일값이다.
- 두 값은 같을 수 있지만 항상 같다고 가정하지 않는다.
- 예: HR이 만든 계약서가 쓰레디 프로젝트와 관련되어도, 관리 책임은 HR에 남을 수 있다.

## Access Role Principle

- 접근권한은 폴더 위치만으로 판단하지 않는다.
- 읽기 권한은 [[decision-006-read-access-from-user-attributes]]에 따라 사용자 DB의 부서/직급/권한과 문서 read policy를 비교해 판단한다.
- role 최종 enum은 spec에서 현재 회사 사용자 모델에 맞춰 구체화한다.
- 민감 문서(계약서, 인사, 재무)는 [[decision-008-sensitive-policy-context]]와 `context/policy.md`를 기준으로 추천한다.
- 권한 policy의 원장은 named policy이고, boolean vector는 판정 결과/log로만 사용한다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Metadata field contract | 기본 필드, 필수/선택, AI 제안 가능 여부 |
| Document relation contract | UI/AI 링크 표현과 DB relation의 변환/승인 규칙 |
| Access visibility contract | role 기반 목록 노출/상세 접근 규칙 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-211 | `access_roles` enum을 현재 회사 role과 맞출 것인가, 데모 전용 enum으로 둘 것인가? | DEC-006: 사용자 role 기반 읽기 권한. enum 세부값은 spec |
| OQ-212 | `owning_department`는 단일값인가, 복수값인가? | DEC-005: 단일값 |
| OQ-213 | UI/AI 링크 표현과 DB relation을 어떻게 변환할지 | DEC-010: wikilink 후보를 DB relation으로 승인 |
| OQ-214 | `related_department`, `related_product`는 승인 필드인가 후보 필드인가? | DEC-010: AI 후보 후 사람 승인 |
