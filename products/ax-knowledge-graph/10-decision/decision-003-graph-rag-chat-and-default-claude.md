---
type: decision
id: AXKG-DEC-003
title: "Graph RAG 기반 AI 채팅과 기본 Claude provider"
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
    - "[[decision-002-markdown-sot-postgres-storage|AXKG-DEC-002]]"
  specs:
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-007-ai-provider-settings|AXKG-SPEC-007]]"
  works: []
  releases: []
  related:
    - "[[decision-001-provider-based-task-execution|OKK-DEC-001]]"
    - "[[spec-009-claude-codex-runner-adapter|OKK-SPEC-009]]"
---

# Graph RAG 기반 AI 채팅과 기본 Claude provider

Graph Chat은 단순 LLM 채팅이 아니라, 제품의 문서 그래프를 검색 context로 사용하는 Graph RAG 기반 AI 채팅으로 구현한다. 내부 AI 실행 provider의 MVP 기본값은 `claude`로 둔다.

## Context

- 관련 baseline: AXKG-BL-001
- 관련 spec: AXKG-SPEC-006, AXKG-SPEC-007
- 관련 architecture decision: AXKG-DEC-002
- 결정이 필요한 이유: Graph Chat의 구현 성격과 AI task 기본 provider를 고정해야 MVP 구현이 흔들리지 않는다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 일반 LLM 채팅 | 구현이 단순하다 | 제품 문서 그래프와 분리된다 | 기각 |
| B | Markdown 문서 검색 기반 RAG | 구현 난이도가 낮다 | 문서 간 연결 경로를 충분히 활용하지 못한다 | 부분 참고 |
| C | Graph RAG 기반 AI 채팅 | 문서, 엣지, neighborhood를 답변 근거로 쓸 수 있다 | retriever 설계가 필요하다 | 채택 |

## Decision

- 채택: Graph Chat은 Graph RAG 기반 AI 채팅이다.
- 채택: 답변 생성 전 질문과 관련된 문서 노드, 연결 엣지, 선택 노드의 neighborhood를 검색한다.
- 채택: AI 답변은 검색된 graph context와 evidence document를 근거로 생성한다.
- 채택: 근거가 부족하면 추측하지 않고 `INSUFFICIENT_GRAPH_CONTEXT`로 처리한다.
- 채택: MVP 기본 provider는 `claude`다.
- 채택: Settings 페이지에서는 `claude`와 `codex`를 모두 선택 가능하게 유지한다.
- 채택: MVP Graph RAG retriever ranking은 `keyword score + edge distance` 추천안으로 시작한다.
- 채택: embedding/pgvector는 MVP에서 제외하고, 검색 품질이 필요해지는 시점에 도입을 재검토한다.

## Rationale

- Graph Chat의 제품 가치는 문서 목록 검색이 아니라 연결 구조를 근거로 답하는 데 있다.
- Markdown 링크와 PostgreSQL edge cache를 이미 SoT/cache 구조로 결정했으므로, 채팅도 같은 graph contract를 사용해야 한다.
- 기본 provider는 `claude`로 시작하되, open-kknaks provider 설정을 통해 `codex` 전환 가능성을 유지한다.

## Implementation Notes

> 참고: 아래의 `POST /graph/chat` 단발 API 표기는 AXKG-SPEC-006이 `POST /graph/chats` + run polling 모델로 정교화하며 대체됐다(superseded). retriever·context·응답 필드 계약은 그대로 유효하다.

- `POST /graph/chat`은 질문을 받으면 먼저 graph retriever를 호출한다.
- retriever는 selected node가 있으면 해당 node neighborhood를 우선 사용하고, 부족하면 전체 graph로 확장한다.
- MVP ranking은 keyword match 점수와 graph edge distance를 조합한다.
- embedding vector search와 pgvector는 MVP 구현 범위에 넣지 않는다.
- AI task에는 question, selected node, retrieved documents, retrieved edges, edge paths를 context로 넘긴다.
- 응답에는 answer, evidence_documents, evidence_edges, used_paths, confidence, missing_context를 포함한다.
- 기본 설정 seed는 `provider=claude`로 생성한다.

## Open Questions

없음. 검색 품질 개선과 pgvector 도입은 MVP 이후 개선 항목으로 둔다.

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| AXKG-SPEC-006 | update | Graph Chat을 Graph RAG 기반 AI 채팅으로 명시 |
| AXKG-SPEC-007 | update | MVP 기본 provider를 `claude`로 확정 |
