---
type: decision
id: CFO-DEC-003
title: "Google Drive 문서 SoT와 DB 동기화 기준"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - google-drive
  - source-of-truth
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-001-google-drive-demo-intake]]"
    - "[[decision-002-document-metadata-foundation]]"
  specs: []
  works: []
  releases: []
  related: []
---

# Google Drive 문서 SoT와 DB 동기화 기준

문서 파일의 Source of Truth는 항상 Google Drive다. DB는 Drive의 최신 변경 내역을 반영한 메타데이터/인덱스/승인 상태 저장소이며, Drive 원본을 대체하지 않는다.

> 이 결정은 "문서 원장 기준"에 대한 결정이다. 파일 자체와 Drive 기본 속성의 원천은 Drive이고, DB는 제품 기능을 위한 동기화된 표현이다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]], [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-001-google-drive-demo-intake]], [[decision-002-document-metadata-foundation]]
- 사용자는 Google Drive에 파일을 올린다.
- 파일명, 위치, 삭제, 이동, 권한, 갱신 시각 같은 원본 변경은 Drive에서 발생한다.
- 제품 DB는 AI 메타데이터 후보, 승인값, 트리 귀속, 관계 탐색을 위해 필요하지만 파일 원본을 소유하지 않는다.
- Drive 변경 반영, AI 분석, 사람 승인, 재분석이 동시에 일어날 수 있으므로 동시성 기준이 필요하다.

## Decision

- 채택:
  - **Google Drive가 문서 파일 SoT다.**
  - DB는 Drive 문서의 최신 상태를 반영하는 동기화 저장소다.
  - 문서 identity의 외부 기준은 `drive_file_id`다.
  - DB row는 `drive_file_id`를 unique key로 삼아 멱등 upsert한다.
  - Drive 변경 내역은 `changes.watch` 알림 후 `changes.list`로 조회해 DB에 반영한다.
  - DB의 Drive-derived 필드는 Drive 변경이 우선한다.
  - 사람이 승인한 제품 메타데이터는 DB에 저장하되, 원본 Drive 파일을 덮어쓰지 않는다.
  - 동시성 충돌은 **Drive-derived 필드**와 **사람 승인 필드**를 분리해서 처리한다.
  - 같은 문서에 대한 DB 갱신은 `drive_file_id` 단위로 직렬화되거나 낙관적 버전 검사를 통과해야 한다.
- 기각:
  - DB를 파일 원본 SoT로 보는 방식.
  - Drive에서 파일이 바뀌었는데 DB가 별도 원본처럼 과거 값을 유지하는 방식.
  - Drive 파일을 복사해 제품 내부 저장소를 원본으로 삼는 방식.

## Data Ownership

| 데이터 | SoT | DB 역할 |
|---|---|---|
| 파일 바이너리/본문 원본 | Google Drive | 필요 시 읽고 분석 결과만 저장 |
| Drive file id | Google Drive | 문서 식별 key로 저장 |
| 파일명 | Google Drive | 최신값 mirror |
| Drive 위치/부모 | Google Drive | 최신값 mirror 또는 참고값 |
| MIME type | Google Drive | 최신값 mirror |
| Drive 수정 시각 | Google Drive | 최신값 mirror |
| Drive 삭제/휴지통 상태 | Google Drive | 최신 상태 mirror |
| AI 메타데이터 후보 | DB | 제품 내부 생성값 |
| 사람 승인 메타데이터 | DB | 제품 내부 승인값 |
| 트리 귀속 | DB | 제품 UI 구조 |
| 문서 관계/그래프 | DB | 제품 내부 관계 |

## Sync Rules

- Drive 변경 이벤트는 중복 수신될 수 있으므로 DB 반영은 항상 idempotent해야 한다.
- 같은 `drive_file_id`에 대한 변경은 새 문서를 만들지 않고 기존 DB row를 갱신한다.
- 파일명이 바뀌면 DB의 Drive-derived title/name mirror는 갱신한다.
- Drive에서 파일이 삭제되거나 휴지통으로 이동되면 DB row는 삭제하지 않고 상태를 `removed` 또는 `trashed`로 반영한다.
- DB의 승인 메타데이터는 Drive mirror 필드와 분리한다.
- Drive-derived 필드가 바뀌어도 승인 메타데이터를 자동 삭제하지 않는다. 다만 재분석 필요 상태를 표시할 수 있다.
- 마지막으로 반영한 Drive change token/page token을 저장해 재시작 후에도 이어서 동기화한다.

## Concurrency Rules

- 동시성 제어의 기준 key는 `drive_file_id`다.
- Drive sync worker, AI analysis worker, approval action이 같은 문서를 동시에 갱신할 수 있다.
- Drive sync는 Drive-derived 필드만 갱신한다.
- 사람 승인 action은 승인 메타데이터와 승인 상태만 갱신한다.
- AI analysis는 승인 전 후보값만 갱신한다. 이미 승인된 값을 자동 덮어쓰지 않는다.
- 승인 action은 저장 시점에 문서 record의 version 또는 `updated_at`을 검사한다.
- 승인 화면을 연 뒤 Drive 변경이 반영되었다면, 저장 시 충돌을 표시하고 최신 Drive mirror를 확인하게 한다.
- 같은 Drive change event가 여러 번 처리되어도 최종 DB 상태는 같아야 한다.
- 같은 AI 후보가 여러 번 생성되어도 동일한 후보 fingerprint면 중복 생성하지 않는다.
- 같은 승인 요청이 재시도되어도 이미 승인된 결과와 동일하면 성공으로 처리한다.

## Conflict Policy

| 충돌 상황 | 처리 |
|---|---|
| Drive 파일명이 바뀌는 동안 사용자가 메타데이터를 승인 | Drive name mirror는 갱신하고, 승인 title과 충돌하면 사용자에게 최신 Drive name 확인 필요 표시 |
| Drive 파일이 삭제/휴지통 이동된 동안 사용자가 승인 | 승인 저장을 막고 `removed`/`trashed` 상태를 보여준다 |
| AI 재분석 중 사용자가 기존 후보를 승인 | 승인 시 version 검사. 후보가 바뀌었으면 최신 후보 확인 후 다시 승인 |
| 같은 Drive 변경 이벤트가 중복 수신 | `drive_file_id` + change token 기준 idempotent 처리 |
| 두 사용자가 같은 후보를 동시에 승인/거절 | 먼저 성공한 action이 상태를 닫고, 뒤 action은 이미 처리된 상태를 반환 |

## Terminology

| 용어 | 의미 |
|---|---|
| Drive SoT | 파일 원본과 Drive 기본 속성의 최종 기준 |
| DB mirror | Drive의 현재 상태를 제품 DB에 반영한 값 |
| 승인 메타데이터 | AI 후보를 사람이 승인/수정해 확정한 제품 내부 데이터 |
| 문서 record | `drive_file_id`에 대응되는 DB row. 파일 원본은 아님 |

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Drive sync contract | `changes.watch`/`changes.list`, token 저장, upsert, 삭제/이동 반영 |
| Document record contract | Drive-derived 필드와 product-owned 필드 분리 |
| Metadata approval contract | Drive 변경과 승인 메타데이터의 충돌/재분석 표시 |
| Concurrency contract | `drive_file_id` 단위 idempotency, version 검사, 중복 이벤트/중복 승인 처리 |

## Closed Questions

| ID | Question | Next |
|---|---|---|
| OQ-301 | Drive에서 파일이 삭제됐을 때 UI에서 숨김 처리만 할지, archive 상태로 노출할지 | DEC-011: soft delete 후 일반 UI 숨김 |
| OQ-302 | Drive 파일명이 바뀌면 승인된 `title`도 자동 갱신할지, Drive name과 approved title을 분리할지 | DEC-011: 기본 제목은 `drive_name` |
| OQ-303 | Drive parent/folder를 제품 트리축에 얼마나 반영할지 | DEC-011: 수집 힌트로만 사용 |
| OQ-304 | version 검사를 숫자 version으로 할지, `updated_at`/etag 기반으로 할지 | DEC-011: Drive mirror fingerprint 기반 stale 검사 |
