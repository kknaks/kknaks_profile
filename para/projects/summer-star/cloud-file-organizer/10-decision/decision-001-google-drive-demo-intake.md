---
type: decision
id: CFO-DEC-001
title: "Google Drive 데모 수집/메타데이터 승인 구조"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - google-drive
  - file-metadata
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
  decisions: []
  specs: []
  works: []
  releases: []
  related:
    - "https://developers.google.com/workspace/drive/api/guides/push"
    - "https://developers.google.com/workspace/drive/api/guides/manage-changes"
    - "https://developers.google.com/workspace/events/guides/events-drive"
    - "https://developers.google.com/workspace/events/guides/create-subscription"
up:
  - human-in-the-loop
  - polling
---

# Google Drive 데모 수집/메타데이터 승인 구조

데모 범위는 Google Drive만 대상으로 하고, 새 변경 이벤트를 받아 AI 메타데이터 후보를 생성한 뒤 사람이 승인해서 DB 링크와 프론트 설정 트리에 반영한다.

> baseline의 날것 입력을 spec으로 내리기 전에 적용 방향을 정하는 문서.
> 기능 계약 상세는 `20-spec/`, 실제 작업 순서는 `30-work/`에 둔다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]]
- 문제/기회: 사용자에게 사전 폴더/트리 정리를 요구하면 업로드 자체가 막힌다. 데모는 Google Drive에 파일을 넣기만 해도 제품이 후보 구조화를 시작하는 경험을 보여줘야 한다.
- 결정이 필요한 이유: 입력원, 실시간 후킹 방식, AI/사람 승인 경계, 트리 설정 책임, 저장 위치를 정해야 후속 spec으로 내릴 수 있다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[human-in-the-loop]] — **AI 는 제안만 하고 승인된 값만 제품 메타데이터가 된다** — 자동화의 상한을 처음부터 그은 것이 이 제품의 뼈대다
- [[polling]] — `changes.watch` 로 알림을 받고 `changes.list` 로 **바뀐 것만** 조회한다. 전체를 다시 훑지 않는 증분 조회가 수집 비용을 정한다

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | Drive API `changes.watch` webhook으로 변경 알림을 받고 `changes.list`로 실제 변경분 조회 | Drive API 표준 기능, 데모 구현 범위가 작음, `files`/`changes` 리소스 변경 알림 지원 | HTTPS webhook 필요, 채널 만료 갱신 필요, 알림만으로 전체 payload가 오지 않아 변경 조회가 필요 | 채택 |
| B | Google Workspace Events API + Pub/Sub subscription | Pub/Sub 기반 운영형 이벤트 파이프라인, Workspace 이벤트 구독 모델과 ordering key 지원 | Cloud project/billing/Pub/Sub 설정이 필요하고 데모에는 무겁다. Drive event target은 파일 단위 구독 중심이라 폴더/전체 변경 감시 UX는 별도 설계 필요 | 후속 확장 후보 |
| C | 주기 polling으로 `changes.list`만 호출 | webhook/공개 HTTPS 없이 가능, 로컬 데모 쉬움 | 실시간성이 약하고 불필요한 호출이 생김. "실시간 후킹" 데모 설득력이 낮음 | 로컬 개발 fallback |

## Decision

- 채택:
  - 데모 입력원은 **Google Drive only**.
  - 실시간 후킹은 **Drive API `changes.watch` + `changes.list`**를 1차 방식으로 채택한다.
  - AI는 파일 메타데이터를 **생성/제안**만 한다.
  - 사람은 AI 후보를 **승인/수정/거절**하고, 승인된 값만 제품 메타데이터가 된다.
  - 트리 구조와 분류 기준은 **프론트에서 설정**한다.
  - 기존 Drive 파일 소급 처리는 하지 않는다. 구독 시작 이후 새 변경만 다룬다.
  - 메타데이터는 자체 DB에 저장하고, Drive 원본은 `drive_file_id`, `web_view_link` 같은 링크 필드로 연결한다.
- 기각:
  - Google Cloud Storage 데모.
  - Drive 파일/폴더 자체를 제품의 최종 메타데이터 저장소로 쓰는 방식.
  - 백엔드가 임의 트리를 자동 확정하는 방식.
  - 초기 MVP에서 기존 파일 전체 backfill/import.
- 보류:
  - Workspace Events API + Pub/Sub는 운영형/엔터프라이즈 확장 시 재검토한다.

## Rationale

- 판단 기준:
  - 사용자가 말한 데모 범위는 Google Drive only다.
  - 공식 Drive API는 리소스 변경 알림을 webhook으로 받을 수 있고, `files`와 `changes` 메서드의 알림을 지원한다.
  - Drive API 알림은 변경 사실을 알려주는 트리거로 쓰고, 실제 변경 목록과 파일 속성은 `changes.list`/`files.get`으로 조회하는 편이 상태 복구와 재시도에 맞다.
  - Google Workspace Events API는 Pub/Sub topic/subscription 준비가 필요해 데모 시작점으로는 무겁다.
- 대안 대비 이유:
  - polling만으로도 가능하지만 "실시간 후킹" 제품 메시지를 약화시킨다.
  - Workspace Events API는 운영 이벤트 파이프라인에는 맞지만, 데모에서 검증할 핵심은 AI 후보/사람 승인/트리 설정 UX다.
- 리스크:
  - Drive API watch channel은 만료가 있으므로 갱신 job이 필요하다.
  - webhook endpoint는 HTTPS와 유효 인증서가 필요하다.
  - Drive 변경 알림은 중복/순서/누락 가능성을 고려해 `startPageToken`/`nextPageToken` 저장과 idempotent 처리가 필요하다.
  - OAuth scope 선택에 따라 파일 콘텐츠 분석 가능 범위가 달라진다.

## Source Notes

- Drive API push notification 문서는 Drive가 리소스 변경 시 앱에 알림을 보내며, webhook callback URL과 notification channel 설정이 필요하다고 설명한다. 또한 `files`와 `changes` 메서드 알림을 지원한다.
- 같은 문서 기준으로 Drive notification channel은 `files` 리소스 최대 1일, `changes` 리소스 최대 1주 만료이므로 갱신이 필요하다.
- Drive changes 문서는 현재 상태 기준 시작 토큰을 `changes.getStartPageToken`으로 가져오고 이후 변경 조회에 사용하는 흐름을 제공한다.
- Workspace Events API subscription 문서는 Pub/Sub topic을 이벤트 수신 endpoint로 설정하고 subscription을 만드는 흐름을 제시한다. Drive events 문서는 Drive의 target resource로 File을 지원한다.

## Scope

이번 spec에 반영할 범위.

- In:
  - Google Drive OAuth 연결
  - Drive `changes.watch` webhook channel 생성/갱신
  - `startPageToken` 저장 및 `changes.list` 기반 변경 조회
  - 새 파일 후보 DB 등록
  - Drive 원본 링크 저장
  - AI 메타데이터 후보 생성
  - 사람 승인/수정/거절 workflow
  - 프론트 트리 구조 설정과 승인 메타데이터 매핑
- Out:
  - Google Cloud Storage
  - Workspace Events API + Pub/Sub 운영 파이프라인
  - 기존 Drive 파일 backfill/import
  - 승인 전 AI 후보를 최종 데이터로 노출
  - Drive 오브젝트 custom property를 제품 SoT로 사용
- 영향을 받는 spec 후보:
  - SPEC-003 Document Metadata Record
  - SPEC-004 Google Drive Connector & Sync
  - SPEC-005 Approval Gate
  - SPEC-006 Document Relations & Explorer

## Closed Questions

후속 decision에서 닫힌 질문.

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-101 | Google Drive OAuth scope는 최소 read-only로 충분한가, 파일 export/content read까지 필요한가? | closed | DEC-019: 데모 v1은 `drive.readonly` |
| OQ-102 | 데모에서 감시 대상은 사용자의 전체 My Drive인가, 선택 폴더 1개인가? | closed | DEC-009: 선택 폴더 1개 |
| OQ-103 | AI가 읽을 수 없는 파일 타입은 어떤 최소 메타데이터만 제안하는가? | closed | DEC-009: metadata-only 후보 |

## Resulting Spec

이 결정으로 생성하거나 업데이트할 spec.

| Spec | Action | Notes |
|---|---|---|
| SPEC-003 Document Metadata Record | create | Drive mirror, metadata field, candidate/approved 상태, fingerprint 계약 |
| SPEC-004 Google Drive Connector & Sync | create | Drive OAuth env 설정, changes.watch/changes.list, 선택 폴더, no backfill 계약 |
| SPEC-005 Approval Gate | create | AI 후보 승인/수정/거절, 문서종류 추가, 민감 preset, stale 처리 |
| SPEC-006 Document Relations & Explorer | create | 트리 탐색, 문서 상세, 연결 문서/지식그래프 탐색 |
