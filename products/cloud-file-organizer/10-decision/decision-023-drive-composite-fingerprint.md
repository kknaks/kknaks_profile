---
type: decision
id: CFO-DEC-023
title: "Drive composite fingerprint 기준"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - google-drive
  - fingerprint
  - approval-conflict
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
  decisions:
    - "[[decision-011-drive-sync-state-and-pending-approval-conflict]]"
    - "[[decision-022-stale-candidate-auto-reanalysis]]"
  specs: []
  works: []
  releases: []
  related: []
---

# Drive composite fingerprint 기준

승인 후보의 stale 판정은 Google Drive의 단일 revision/version 필드에만 의존하지 않는다. 파일 타입별 필드 차이를 고려해 필수 mirror 값과 선택 revision 값, 본문 fingerprint를 조합한 composite fingerprint를 사용한다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]]
- 관련 decision: [[decision-011-drive-sync-state-and-pending-approval-conflict]], [[decision-022-stale-candidate-auto-reanalysis]]
- Google Docs/Sheets/Slides와 binary 파일은 Drive API에서 revision/version 신뢰도가 다를 수 있다.
- 승인 후보는 생성 당시 Drive 상태와 승인 시점 Drive 상태가 같을 때만 승인 가능해야 한다.
- 단일 revision 필드가 없거나 안정적이지 않은 파일도 stale 판정이 가능해야 한다.

## Decision

- 채택:
  - 승인 후보는 생성 당시 composite fingerprint를 저장한다.
  - composite fingerprint의 필수값은 `drive_file_id`, `drive_modified_time`, `drive_name`, `mime_type`이다.
  - Drive API에서 안정적으로 얻을 수 있으면 `head_revision_id`, `drive_version`을 추가한다.
  - 본문을 읽어 AI 분석을 수행한 경우 `content_fingerprint`를 추가한다.
  - 승인 시 현재 Drive mirror와 후보 fingerprint를 비교한다.
  - 분석 결과에 영향을 줄 수 있는 fingerprint 값이 바뀌면 후보는 stale이다.
  - 파일 타입별 revision/version 필드 매핑은 구현 spec에서 검증한다.
- 기각:
  - 모든 파일 타입에서 단일 `revision_id`만 stale 기준으로 사용하는 방식.
  - `modifiedTime`만으로 본문 변경 여부를 완전히 판단하는 방식.
  - Drive 파일명이 바뀌어도 후보 제목/분류 검토 없이 승인하는 방식.

## Fingerprint Fields

| Field | 필수 여부 | 목적 |
|---|---|---|
| `drive_file_id` | 필수 | 문서 identity |
| `drive_modified_time` | 필수 | Drive 수정 시점 변화 감지 |
| `drive_name` | 필수 | 기본 제목 변화 감지 |
| `mime_type` | 필수 | reader/profile 변화 감지 |
| `head_revision_id` | 가능 시 | Drive revision 변화 감지 |
| `drive_version` | 가능 시 | Drive version 변화 감지 |
| `content_fingerprint` | 본문 읽은 경우 | AI 분석 대상 본문 변화 감지 |

## Stale Rule

```text
candidate.fingerprint != current_drive_mirror.fingerprint
  -> candidate stale
  -> approval blocked
  -> auto reanalysis enqueue
```

비교는 spec에서 필드별로 구체화한다. 예를 들어 `drive_name` 변경은 제목 후보에 영향을 줄 수 있으므로 stale로 본다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Drive fingerprint contract | 필수/선택 fingerprint 필드 정의 |
| File type mapping contract | Google Docs/Sheets/Slides/binary별 revision/version 매핑 |
| Approval stale precondition contract | 승인 저장 전 fingerprint 비교 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-1102 | Drive stale 판정은 단일 revision 필드가 아니라 composite fingerprint로 수행한다. 타입별 필드 매핑은 구현 spec에서 검증한다. |
