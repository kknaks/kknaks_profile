---
type: decision
id: CFO-DEC-024
title: "open-kknaks 기반 AI 문서 분류 파이프라인"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - open-kknaks
  - ai-classification
  - pipeline
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-001-google-drive-demo-intake]]"
    - "[[decision-002-document-metadata-foundation]]"
    - "[[decision-019-google-drive-readonly-scope-for-demo]]"
    - "[[decision-022-stale-candidate-auto-reanalysis]]"
  specs:
    - "[[spec-004-google-drive-connector-sync]]"
    - "[[spec-005-approval-gate]]"
    - "[[spec-007-ai-classification-pipeline]]"
  works: []
  releases: []
  related:
    - "[[spec-001-task-model-and-lifecycle]]"
    - "[[spec-002-redis-broker-queue-contract]]"
    - "[[spec-003-python-client-and-streaming-api]]"
    - "[[spec-009-claude-codex-runner-adapter]]"
---

# open-kknaks 기반 AI 문서 분류 파이프라인

AI 문서 분류/메타데이터 후보 생성은 제품 내부 ad-hoc worker가 아니라 `open-kknaks` task 실행 모델을 사용한다. Drive sync는 분석 job을 enqueue하고, `open-kknaks`가 provider runner를 실행해 구조화된 후보 JSON을 반환한다. 제품 DB에는 검증된 후보만 저장한다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]], [[baseline-002-department-document-management-direction]]
- 관련 decision: [[decision-001-google-drive-demo-intake]], [[decision-002-document-metadata-foundation]], [[decision-019-google-drive-readonly-scope-for-demo]], [[decision-022-stale-candidate-auto-reanalysis]]
- `open-kknaks`는 provider 기반 task 실행, Redis broker queue, Python client, Claude/Codex runner adapter 계약을 가진다.
- 기존 spec에는 AI Worker enqueue만 있고, 실제 분류 실행 주체와 task/result 계약이 빠져 있었다.
- 문서 원문은 제품 DB에 저장하지 않기로 결정되어 있으므로, AI task payload와 retention 경계도 명확해야 한다.

## Decision

- 채택:
  - AI 문서 분류/메타데이터 후보 생성은 `open-kknaks` task로 실행한다.
  - 제품 backend는 Drive sync 후 classification job을 생성하고 `open_kknaks.AgentClient.submit()` 계열 client로 task를 제출한다.
  - provider/model/queue/timeout은 제품 env로 설정한다.
  - task 입력에는 document id, Drive fingerprint, Drive mirror, 추출된 분석 입력, 조직/문서종류/정책 context, 출력 schema를 포함한다.
  - task 결과는 구조화된 candidate JSON이어야 한다.
  - 제품 backend는 결과 schema와 fingerprint를 검증한 뒤 metadata candidate로 저장한다.
  - `open-kknaks` task는 승인 metadata를 직접 쓰지 않는다.
  - `open-kknaks` task는 Google Drive나 제품 DB에 직접 쓰지 않는다.
  - stale 후보 재분석도 같은 classification pipeline으로 재실행한다.
- 기각:
  - 제품 backend 안에서 임시 AI 호출 로직을 직접 구현하는 방식.
  - AI runner가 approval metadata를 직접 확정 저장하는 방식.
  - AI runner가 Drive connector 권한을 직접 보유하는 방식.

## Pipeline Boundary

| 단계 | 책임 |
|---|---|
| Drive sync | Drive mirror/fingerprint 갱신, 분석 job 생성 |
| Product backend | open-kknaks task submit, result 검증, candidate 저장 |
| open-kknaks | provider runner 실행, stream/result 반환 |
| Approval gate | admin 승인/수정/거절 |

## Safety Boundary

- Drive OAuth secret과 connector env는 open-kknaks task payload에 넣지 않는다.
- 제품 DB credential은 open-kknaks task payload에 넣지 않는다.
- AI 결과는 후보일 뿐 승인값이 아니다.
- task payload/result retention은 구현 spec에서 원문 저장 정책과 충돌하지 않게 제한한다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| AI classification pipeline contract | Drive sync -> open-kknaks task -> candidate 저장 |
| open-kknaks task payload contract | 입력 context와 출력 schema |
| classification result validation contract | schema/fingerprint/idempotency 검증 |
