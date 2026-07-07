---
type: decision
id: AXKG-DEC-002
title: "Markdown 문서 SoT와 PostgreSQL 운영 저장소"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
    - "[[spec-009-prompt-dynamic-management|AXKG-SPEC-009]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
  works: []
  releases: []
  related: []
---

# Markdown 문서 SoT와 PostgreSQL 운영 저장소

최종 문서는 Markdown 파일을 SoT로 삼고, PostgreSQL은 운영 상태·승인 게이트·draft·문서 index·그래프 cache를 저장한다.

> 이 제품은 Obsidian 호환과 제품 페이지 그래프가 모두 중요하다. 따라서 최종 지식은 `.md` 파일로 남기고, DB는 작업 상태와 빠른 조회를 위한 운영 저장소로 둔다.

## Context

- 관련 baseline: AXKG-BL-001
- 문제/기회: 문서는 Obsidian에서 직접 열리고 git diff가 가능해야 하지만, 승인 게이트/상태/채팅/검색은 DB가 필요하다.
- 결정이 필요한 이유: Source Inbox, Reference 승인, Graph Chat, Auth 구현 전에 문서와 상태의 SoT 경계를 확정해야 한다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 모든 문서와 상태를 PostgreSQL에 저장 | 조회가 단순하다 | Obsidian/git 호환이 약하다 | 기각 |
| B | 모든 것을 Markdown 파일에 저장 | Obsidian 호환 최고 | 승인 상태/검색/동시성 관리가 어렵다 | 기각 |
| C | Markdown 파일 SoT + PostgreSQL 운영 저장소 | 문서 호환성과 앱 운영성을 모두 확보 | 파일/DB 동기화 규칙 필요 | 채택 |
| D | Markdown 파일 SoT + NoSQL 운영 저장소 | JSON payload에 유연 | 관계/상태/인덱스에는 PostgreSQL이 더 적합 | 기각 |

## Decision

- 채택:
  - 최종 문서 SoT는 Markdown 파일이다.
  - PostgreSQL을 운영 저장소로 사용한다.
  - 로컬 개발에서는 repo 내부 `data/documents`를 markdown root로 사용한다.
  - 배포 환경에서는 문서 root를 bind mount로 주입하고, 실제 mount path는 배포 설정에서 명시한다.
  - AI payload, gate payload, draft metadata는 PostgreSQL `jsonb`를 사용한다.
  - 모든 확정 문서는 `documents.path`를 가진다.
  - 그래프의 원천은 Markdown의 본문 wikilink와 frontmatter `up`이다.
  - PostgreSQL의 edge table은 빠른 조회와 Graph Chat을 위한 cache다.
- 기각:
  - 최종 문서를 DB에만 저장하는 방식.
  - MVP에서 NoSQL을 주 저장소로 쓰는 방식.
- 보류:
  - 배포 환경별 실제 host path. 배포 단계에서 확정한다.

## Rationale

- 판단 기준: Obsidian 호환, git 추적, 승인 상태 관리, 앱 조회 성능, 추후 확장성.
- 대안 대비 이유: Markdown만으로는 gate/draft/thread 상태 관리가 약하고, DB만으로는 Obsidian/파일 기반 그래프의 장점이 사라진다.
- 리스크: 파일과 DB가 불일치할 수 있다. 이를 줄이기 위해 확정 문서는 file write 성공 후 `documents` row를 갱신하고, graph cache는 markdown에서 재빌드 가능해야 한다.

## Scope

이번 decision에 반영할 범위.

- In:
  - Markdown 최종 문서 SoT
  - PostgreSQL 운영 저장소
  - `path` 기반 문서 index
  - JSONB 기반 AI/gate payload
  - graph edge cache
- Out:
  - 실제 migration SQL
  - pgvector 도입
  - 배포 환경별 실제 host path

## Deployment Deferred

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-001 | 배포 환경의 실제 bind mount host path | DevOps | 배포 단계에서 확정 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| AXKG-SPEC-005 | update | Markdown link graph가 source of truth |
| AXKG-SPEC-006 | update | Graph Chat은 Postgres edge cache를 사용할 수 있음 |
| Database architecture | create | PostgreSQL table 후보와 SoT 경계 |
