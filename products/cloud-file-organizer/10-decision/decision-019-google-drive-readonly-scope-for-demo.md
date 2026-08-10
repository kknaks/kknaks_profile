---
type: decision
id: CFO-DEC-019
title: "데모 v1 Google Drive readonly scope"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - google-drive
  - oauth
  - demo
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
  decisions:
    - "[[decision-009-google-drive-intake-scope]]"
    - "[[decision-018-sensitive-document-preset-approval]]"
  specs: []
  works: []
  releases: []
  related: []
up: []
---

# 데모 v1 Google Drive readonly scope

데모 v1에서는 AI 분류/메타데이터/문서 관계 추천 품질을 검증하기 위해 Google Drive OAuth scope를 `drive.readonly`로 시작한다. 감시 범위는 선택 폴더 1개로 제한하고, 원문은 DB에 저장하지 않는다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]]
- 관련 decision: [[decision-009-google-drive-intake-scope]], [[decision-018-sensitive-document-preset-approval]]
- 제품의 핵심 가치는 AI가 문서를 읽고 분류, 메타데이터, 관련 문서를 추천하는 흐름이다.
- `drive.metadata.readonly`만 사용하면 파일명/MIME/시간 중심 후보에 머물러 데모 품질이 낮아질 수 있다.
- 반대로 scope를 넓히면 원문 접근 정책과 저장 제한을 명확히 해야 한다.

## Decision

- 채택:
  - 데모 v1은 `drive.readonly`를 기본 scope로 사용한다.
  - 감시 대상은 DEC-009대로 선택 폴더 1개와 그 하위 항목으로 제한한다.
  - 기존 파일 소급 처리는 하지 않는다.
  - Drive 원문/본문은 DB에 저장하지 않는다.
  - DB에는 Drive mirror, AI 분석 결과, 요약, 메타데이터 후보, 승인 결과만 저장한다.
  - 민감 문서는 DEC-018대로 preset 후보를 표시하고 관리자 승인을 거친다.
  - 권한 없는 문서는 목록/트리/검색/관련 문서에서 숨긴다.
- 기각:
  - v1에서 `drive.metadata.readonly`만 기본으로 사용하고 본문 분석 없이 데모하는 방식.
  - whole My Drive 또는 Shared Drive 전체를 읽는 방식.
  - Drive 원문을 제품 DB에 복제 저장하는 방식.

## Safety Boundaries

| Boundary | 결정 |
|---|---|
| OAuth scope | `drive.readonly` |
| 감시 범위 | 선택 폴더 1개 |
| 소급 처리 | 없음 |
| 원문 저장 | DB 저장 안 함 |
| 저장 데이터 | mirror, summary, 후보 metadata, 승인 metadata |
| 민감 문서 | preset 후보 + 관리자 승인 |

## 근거 개념

없음 — 데모 v1 의 OAuth scope 값을 확정한 범위 결정이다.

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Google Drive OAuth contract | `drive.readonly` scope와 동의 화면 범위 |
| Content read contract | 본문 읽기, 분석, 원문 미저장 규칙 |
| Demo safety contract | 선택 폴더 제한과 민감 문서 승인 경계 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-902 | 데모 v1은 `drive.readonly`를 기본 scope로 사용한다. 단, 선택 폴더 제한과 원문 미저장을 safety boundary로 둔다. |
