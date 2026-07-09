---
type: decision
id: CFO-DEC-011
title: "Drive sync 상태와 승인 대기 중 변경 처리"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - google-drive
  - sync
  - approval-conflict
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
  decisions:
    - "[[decision-003-google-drive-document-sot]]"
    - "[[decision-009-google-drive-intake-scope]]"
  specs: []
  works: []
  releases: []
  related: []
---

# Drive sync 상태와 승인 대기 중 변경 처리

Drive 파일이 삭제되면 DB row를 hard delete하지 않고 soft delete 상태로 반영한다. 문서의 기본 제목은 별도 승인 제목 없이 Google Drive의 `drive_name`을 사용한다. 승인 대기 중 Drive 파일이 변경되면 기존 AI 후보는 stale 처리하고 그대로 승인할 수 없게 한다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]]
- 관련 decision: [[decision-003-google-drive-document-sot]], [[decision-009-google-drive-intake-scope]]
- Google Drive가 파일 SoT이므로 삭제, 휴지통 이동, 파일명 변경, 본문 변경은 Drive 상태가 우선한다.
- AI 후보는 특정 Drive mirror 시점에서 생성된다.
- 승인 화면을 열어둔 동안 Drive 파일이 바뀔 수 있다.
- 승인된 metadata가 최신 Drive 파일과 다른 버전에서 만들어지면 신뢰할 수 없다.

## Decision

- 채택:
  - Drive에서 파일이 삭제되거나 휴지통으로 이동되면 DB document row는 삭제하지 않고 `removed` 또는 `trashed` 상태로 soft delete 처리한다.
  - 일반 사용자 UI의 트리/목록/검색/관련 문서에서는 soft deleted 문서를 숨긴다.
  - 관리자/동기화/감사 화면에서는 soft deleted 상태를 조회할 수 있게 한다.
  - 문서의 기본 제목은 `drive_name`이다.
  - v1에서는 별도 `approved_title`을 기본 필드로 두지 않는다.
  - Drive 파일명이 바뀌면 DB의 `drive_name` mirror와 UI 기본 제목도 Drive 기준으로 갱신한다.
  - AI 후보는 생성 당시 Drive mirror fingerprint를 함께 저장한다.
  - 승인 시 현재 Drive mirror fingerprint와 후보의 fingerprint를 비교한다.
  - fingerprint가 다르면 기존 후보는 `stale` 처리하고 승인할 수 없다.
  - stale 후보는 최신 Drive 상태 기준 재분석 또는 관리자 확인 후 새 후보로 다시 승인한다.
  - 승인 대기 중 파일이 삭제/휴지통 이동되면 승인을 막고 문서 상태를 `removed`/`trashed`로 보여준다.
  - Drive parent/folder는 수집 힌트로만 사용하고, 제품의 `physical_tree_path`를 자동 변경하지 않는다.
- 기각:
  - Drive에서 삭제된 문서를 DB에서 hard delete하는 방식.
  - 승인 대기 중 Drive 파일이 바뀌어도 과거 AI 후보를 그대로 승인하는 방식.
  - Drive 파일명을 승인 제목과 분리해 v1부터 별도 편집 필드로 관리하는 방식.
  - Drive folder 이동을 제품 트리 귀속 변경으로 자동 적용하는 방식.

## Document State

| State | 의미 | 일반 사용자 노출 |
|---|---|---|
| `active` | Drive에 존재하고 제품에서 탐색 가능한 문서 | 노출 |
| `trashed` | Drive 휴지통으로 이동된 문서 | 숨김 |
| `removed` | Drive changes에서 삭제/제외로 감지된 문서 | 숨김 |
| `out_of_scope` | 선택 감시 폴더 범위 밖으로 빠진 문서 | 숨김 |

## Candidate State

| State | 의미 | 승인 가능 여부 |
|---|---|---|
| `pending` | 최신 Drive mirror 기준으로 생성된 승인 대기 후보 | 가능 |
| `stale` | 후보 생성 이후 Drive mirror가 변경됨 | 불가 |
| `approved` | 사람이 승인해 확정된 후보 | 완료 |
| `rejected` | 사람이 반려한 후보 | 불가 |
| `blocked` | 문서 삭제/권한 부족/읽기 실패 등으로 승인 진행 불가 | 불가 |

## Fingerprint Rule

후보가 참조한 Drive 상태를 다음 값의 조합으로 저장한다.

| Field | 목적 |
|---|---|
| `drive_file_id` | 문서 identity |
| `drive_modified_time` | Drive 수정 시각 |
| `drive_version` 또는 `head_revision_id` | 가능할 때 버전 식별 |
| `drive_name` | 제목 mirror 변경 감지 |
| `mime_type` | reader/profile 변경 감지 |
| `content_fingerprint` | 본문을 읽은 경우 분석 대상 변경 감지 |

승인 시 현재 document mirror가 후보 fingerprint와 다르면 후보는 stale이다. stale 판정은 승인 action의 필수 precondition이다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Drive document state contract | `active`/`trashed`/`removed`/`out_of_scope` 상태와 UI 노출 규칙 |
| Approval candidate state contract | `pending`/`stale`/`approved`/`rejected`/`blocked` 전이 |
| Approval concurrency contract | 후보 fingerprint 비교와 stale 승인 차단 |
| Drive title contract | `drive_name`을 기본 제목으로 사용하는 UI/API 규칙 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-301 | Drive 삭제/휴지통 이동은 soft delete 상태로 DB에 남기고 일반 UI에서는 숨긴다. |
| OQ-302 | 기본 제목은 `drive_name`이다. v1에서 승인 제목을 분리하지 않는다. |
| OQ-303 | Drive parent/folder는 수집 힌트이며 제품 `physical_tree_path`를 자동 변경하지 않는다. |
| OQ-304 | 승인 후보는 Drive mirror fingerprint로 stale 여부를 검사한다. |
| OQ-901 | 선택 폴더 범위 밖 문서는 `out_of_scope`로 두고 일반 UI에서는 숨긴다. |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-1101 | stale 후보 발생 시 자동 재분석할지, 관리자 버튼으로 재분석할지 | DEC-022: 자동 재분석, 실패 시 수동 재분석 버튼 |
| OQ-1102 | Google Drive API에서 파일 타입별로 어떤 version/revision 필드를 안정적으로 쓸 수 있는지 | DEC-023: composite fingerprint 사용, 타입별 매핑은 spec 검증 |
