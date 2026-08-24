---
type: baseline
id: CFO-BASE-001
title: "Google Drive 파일 메타데이터 승인형 구조화"
status: accepted
product: cloud-file-organizer
source:
  type: idea
  ref: "inbox/2026-07-08-gcs-realtime-hook-file-metadata-structuring.md"
links:
  baselines: []
  decisions:
    - "[[decision-001-google-drive-demo-intake]]"
    - "[[decision-002-document-metadata-foundation]]"
    - "[[decision-003-google-drive-document-sot]]"
    - "[[decision-004-department-tree-organization-db]]"
    - "[[decision-005-single-physical-tree-multiple-logical-links]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/baseline
  - status/accepted
  - google-drive
  - file-metadata
---

# Google Drive 파일 메타데이터 승인형 구조화

Google Drive에 새로 올라오는 파일을 감지해 AI가 메타데이터 후보를 만들고, 사람이 승인한 뒤 DB 링크와 프론트 설정 트리로 구조화한다.

> 이 baseline의 핵심 방향은 decision으로 승격했다. 남은 세부 이슈는 `10-decision/README.md`와 후속 spec에서 닫는다.

## Raw

구글클라우드에 올라간 파일을 실시간 후킹 해서 파일메타데이터를 만들고 구조화를 하는 프로젝트
왜냐하면 구글클라우드에 트리구조로 넣으라고 하면 아무도 안쓰니까 일단 데이터라도 넣어주거 우리쪽 서버에서 트리구조를 만드는 거야

## Context

- 사용자가 파일을 업로드하기 전에 정해진 트리 구조로 분류하도록 요구하면 사용률이 떨어진다.
- 초기 입력 장벽을 낮추기 위해, 사용자는 파일만 넣고 제품이 사후 구조화를 담당하는 방향이다.
- 데모 범위는 Google Drive만 대상으로 한다. Google Cloud Storage는 이번 범위에서 제외한다.
- 완전히 새로운 개념 검증이므로 기존 파일 소급 처리는 하지 않는다.
- 메타데이터는 AI가 생성/제안하고, 사람이 승인해야 제품 데이터로 반영된다.
- 트리 구조는 백엔드가 임의 생성하지 않고 프론트에서 설정 가능한 구조로 둔다.
- 메타데이터는 Google Drive 오브젝트 자체가 아니라 자체 DB에 저장하고, 원본 Drive 파일 링크를 연결한다.

## Why It Matters

- 데이터가 들어오지 않으면 이후 검색, 분류, 지식화, 자동화 기능을 만들 수 없다.
- 사전 분류 요구를 제거하면 실제 파일 축적률과 제품 채택률이 높아질 수 있다.
- 파일 메타데이터가 안정적으로 쌓이면 조직/프로젝트/업무 단위의 자동 트리 구성, 검색, 요약, 권한 검토 같은 후속 기능의 기반이 된다.

## Possible Direction

- Google Drive 변경 이벤트를 수신해 새 파일 후보를 DB에 등록한다.
- AI가 파일명, Drive 기본 속성, 가능한 경우 콘텐츠 텍스트를 바탕으로 메타데이터 후보를 생성한다.
- 승인 대기 상태의 후보를 사람이 검토하고 승인/수정/거절한다.
- 프론트에서 트리 구조와 분류 기준을 설정하고, 승인된 메타데이터가 그 구조에 매핑된다.
- 자체 DB에는 원본 Drive 파일 링크, Drive file id, AI 후보, 승인 결과, 트리 매핑을 저장한다.

## Resolution

| ID | Question | Next |
|---|---|---|
| OQ-001 | 입력원은 Google Cloud Storage, Google Drive, 또는 둘 다인가? | DEC-001: Google Drive only |
| OQ-002 | 실시간 후킹 방식은 Pub/Sub, Cloud Functions, Drive change API/webhook 중 무엇인가? | DEC-001: Drive changes.watch + changes.list |
| OQ-003 | 메타데이터 추출 범위는 어디까지인가? | DEC-002: DB 메타데이터 기본 축, DEC-006: read policy |
| OQ-004 | 트리 구조 생성 규칙은 규칙 기반, AI 기반, 사람 검수 기반 중 무엇인가? | DEC-004/DEC-005: DB 조직도 기반 트리 + 단일 물리 귀속/다중 논리 연결 |
| OQ-005 | 기존에 쌓인 파일의 소급 처리도 MVP에 포함하는가? | DEC-001: 제외 |
| OQ-006 | 메타데이터 저장소는 자체 DB인가, 클라우드 오브젝트 metadata인가? | DEC-003: Drive가 파일 SoT, DB는 메타데이터/인덱스/승인 상태 저장소 |
