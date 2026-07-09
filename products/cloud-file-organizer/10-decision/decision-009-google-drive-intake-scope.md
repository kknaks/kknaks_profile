---
type: decision
id: CFO-DEC-009
title: "Google Drive intake scope"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - google-drive
  - intake
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
  decisions:
    - "[[decision-001-google-drive-demo-intake]]"
    - "[[decision-003-google-drive-document-sot]]"
    - "[[decision-019-google-drive-readonly-scope-for-demo]]"
  specs: []
  works: []
  releases: []
  related: []
---

# Google Drive intake scope

v1 데모의 Google Drive 수집 범위는 선택 폴더 1개로 제한한다. 파일 본문을 읽을 수 없으면 Drive metadata만으로 AI 후보를 만들고, 승인자가 수동 보완한다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]]
- 관련 decision: [[decision-001-google-drive-demo-intake]], [[decision-003-google-drive-document-sot]]
- DEC-001에서 Google Drive only와 `changes.watch + changes.list`를 채택했다.
- 아직 OAuth scope, 감시 대상, 읽을 수 없는 파일 처리 기준이 열려 있었다.

## Decision

- 채택:
  - v1 감시 대상은 **사용자가 선택한 Google Drive 폴더 1개**다.
  - 선택 폴더 하위의 새 파일/변경만 수집 대상으로 삼는다.
  - OAuth scope는 최소 권한을 우선한다.
  - Drive 파일/폴더 metadata 수집에는 `drive.metadata.readonly`를 기본 후보로 둔다. *(이후 DEC-019에서 데모 v1 기본 scope가 `drive.readonly`로 확정되어 이 항목은 대체되었다.)*
  - 파일 본문/내보내기/export가 필요한 경우에만 `drive.readonly`를 요구한다. *(DEC-019로 대체)*
  - 본문을 읽을 수 없는 파일은 수집 실패가 아니라 `metadata_only` 후보로 등록한다.
  - `metadata_only` 후보는 Drive 파일명, MIME type, 수정시각, 원본 링크만으로 AI 후보를 만든다.
  - 승인자는 본문 분석이 없는 후보의 메타데이터를 수동 보완할 수 있다.
- 기각:
  - v1에서 전체 My Drive를 감시하는 방식.
  - v1에서 모든 파일 타입을 반드시 본문 분석해야 하는 방식.
  - 본문을 못 읽는 파일을 수집 실패로 처리하는 방식.
- 보류:
  - 여러 폴더 감시.
  - Shared Drive 전체 감시.
  - 파일 타입별 정교한 parser/OCR 정책.

## Scope Policy

| 항목 | v1 결정 |
|---|---|
| 감시 단위 | 선택 폴더 1개 |
| 하위 폴더 | 포함 |
| 전체 My Drive | 제외 |
| Shared Drive | 보류 |
| 기존 파일 backfill | 제외 |
| 새 파일/변경 | 포함 |

## OAuth Policy

> 이 절의 scope 기본값은 DEC-019로 대체되었다. 데모 v1 기본 scope는 `drive.readonly`다.

| 필요 기능 | Scope 후보 | Notes |
|---|---|---|
| 파일 id, 이름, MIME type, 링크, parent, 수정시각 조회 | `drive.metadata.readonly` | 최초 기본 후보였으나 DEC-019로 대체 |
| Google Docs/Sheets 등 export 또는 파일 본문 읽기 | `drive.readonly` | DEC-019에서 v1 기본 scope로 확정 |

최소 권한 우선 방향은 유지한다. metadata-only 단계 도입 같은 scope 축소는 v2 이후 재검토한다.

## Unsupported / Unreadable File Policy

- 읽을 수 없는 파일도 DB document record를 만든다.
- `read_capability=metadata_only`로 표시한다.
- AI는 파일명과 Drive metadata만으로 제한된 후보를 만든다.
- 승인 게이트는 "본문 분석 없음" 상태를 표시한다.
- 승인자는 문서종류, 부서, 권한, 관련 문서 등을 수동 입력/수정할 수 있다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Drive folder selection | 감시 폴더 선택/저장/변경 |
| Drive scope and auth | OAuth scope와 권한 안내 |
| Drive metadata-only intake | 본문 미지원 파일 처리 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-901 | 선택 폴더를 바꾸면 기존 DB 문서는 유지할지 제외 표시할지 | DEC-011: `out_of_scope`로 유지하고 일반 UI 숨김 |
| OQ-902 | `drive.readonly`를 v1 기본으로 받을지, metadata-only에서 단계적으로 요청할지 | DEC-019: 데모 v1은 `drive.readonly`, 선택 폴더 제한과 원문 미저장 |
