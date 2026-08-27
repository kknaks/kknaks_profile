---
type: decision
id: AXKG-DEC-003
title: "Graph RAG 기반 AI 채팅과 기본 Claude provider"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-07
updated_at: 2026-07-14
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
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works:
    - "[[work-008-graph-rag-two-stage-retriever|AXKG-WORK-008]]"
  releases: []
  related:
    - "[[decision-001-provider-based-task-execution|OKK-DEC-001]]"
    - "[[spec-009-claude-codex-runner-adapter|OKK-SPEC-009]]"
up:
  - search-index
  - time-complexity
  - polling
  - performance-testing
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
- 채택: MVP Graph RAG retriever ranking은 `keyword score + edge distance` 추천안으로 시작한다. *(2026-07-14 PLAN-013-T-001 개정: 이 단일 경로는 폴백으로 강등되고 기본 경로는 qmd 2단 retriever다 — 아래 개정 참조)*
- 채택: embedding/pgvector는 MVP에서 제외하고, 검색 품질이 필요해지는 시점에 도입을 재검토한다. *(2026-07-14 PLAN-013-T-001 개정: embedding 검색은 qmd 사이드카가 담당하고 pgvector는 계속 파킹 — 아래 개정 참조)*

## Rationale

- Graph Chat의 제품 가치는 문서 목록 검색이 아니라 연결 구조를 근거로 답하는 데 있다.
- Markdown 링크와 PostgreSQL edge cache를 이미 SoT/cache 구조로 결정했으므로, 채팅도 같은 graph contract를 사용해야 한다.
- 기본 provider는 `claude`로 시작하되, open-kknaks provider 설정을 통해 `codex` 전환 가능성을 유지한다.

## Implementation Notes

> 참고: 아래의 `POST /graph/chat` 단발 API 표기는 AXKG-SPEC-006이 `POST /graph/chats` + run polling 모델로 정교화하며 대체됐다(superseded). retriever·context·응답 필드 계약은 그대로 유효하다.

- `POST /graph/chat`은 질문을 받으면 먼저 graph retriever를 호출한다.
- retriever는 selected node가 있으면 해당 node neighborhood를 우선 사용하고, 부족하면 전체 graph로 확장한다.
- MVP ranking은 keyword match 점수와 graph edge distance를 조합한다. *(2026-07-14 개정: 기본 경로는 qmd 2단 retriever, 이 조합은 qmd 장애 시 폴백 — 위 개정 참조)*
- ~~embedding vector search와 pgvector는 MVP 구현 범위에 넣지 않는다.~~ *(2026-07-14 개정: embedding 검색은 qmd 사이드카가 담당, pgvector는 계속 파킹 — 위 개정 참조)*
- AI task에는 question, selected node, retrieved documents, retrieved edges, edge paths를 context로 넘긴다.
- 응답에는 answer, evidence_documents, evidence_edges, used_paths, confidence, missing_context를 포함한다.
- 기본 설정 seed는 `provider=claude`로 생성한다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[search-index]] — qmd 사이드카가 BM25 + 벡터를 융합해 후보를 뽑는 1단. **검색을 위해 따로 만들어 두는 자료구조**가 있어야 한다는 것이 keyword 스캔에서 옮겨 온 이유다
- [[time-complexity]] — 폴백으로 남은 keyword 스캔이 **O(전체 문서)** 라 문서가 늘면 역전된다는 것이 전환의 근거로 명시돼 있다
- [[polling]] — 리랭크의 추가 지연을 **run polling UX 가 흡수한다**는 판단. 단발 API 대신 `POST /graph/chats` + run polling 으로 간 것도 같은 이유다
- [[performance-testing]] — 리랭크 기본값을 on 에서 off 로 뒤집은 것이 **CPU-only 실측 60초+** 였다. 결정이 추정이 아니라 측정으로 정정된 자리

## Open Questions

- (2026-07-14 PLAN-013-T-001) qmd 2단 retriever의 튜닝 숫자(edge 타입 가중치·hop 감쇠 함수·top-K)와 qmd 통합 형태(subprocess CLI vs MCP)는 결정하지 않는다 — "구현 기본값으로 시작, 관찰 후 조정"(상세 SSOT는 AXKG-SPEC-011 §7 OQ). pgvector는 계속 파킹(qmd 개정으로 그 자리를 대체). (2026-07-14 PLAN-013-T-007) 리랭크 기본값은 이 OQ에서 빠졌다 — 실측으로 off 확정(아래 §실측 수용 정정).

## 개정: embedding 검색 = pgvector 대신 qmd 사이드카 + 2단 retriever (2026-07-14 개정, PLAN-013-T-001)

채팅 고도화 라운드(PLAN-013 ① Graph RAG 고도화)에서 Graph RAG retriever를 재설계한다. 위 Decision의 "MVP ranking = `keyword score + edge distance`" / "embedding·pgvector MVP 제외"를 아래로 개정한다. **핵심 계약(Graph Chat = Graph RAG 기반 AI 채팅, 기본 provider = `claude`, 근거 부족 시 `INSUFFICIENT_GRAPH_CONTEXT`)은 불변**이며, 검색 메커니즘만 바뀌므로 신규 DEC로 쪼개지 않고 in-place 개정한다(DEC-005 amendment 선례 준수).

- **embedding 검색 = pgvector 대신 qmd 사이드카 채택**: qmd(github.com/tobi/qmd — 로컬 마크다운 검색엔진: BM25 + 로컬 embedding 벡터검색 RRF 융합 + LLM 리랭크, SQLite 자체 인덱스, CLI/MCP)를 후보 발굴 엔진으로 채택한다. **pgvector는 계속 파킹**(도입하지 않음). 종전 "embedding은 필요 시 pgvector 재검토"를 "embedding 검색은 qmd 사이드카가 담당"으로 대체한다.
- **retriever 2단 구조 채택**:
  - **1단 후보 발굴** = qmd 하이브리드 검색(BM25 + 벡터 RRF). **리랭크는 설정 토글, 기본 off**(2026-07-14 T-006 CPU 실측 수용 — 종전 on 기본값에서 정정, 아래 §실측 수용 정정). 리랭크 설정 표면의 owning spec은 AXKG-SPEC-007이다(경계 참조만 — 여기서 재서술하지 않는다).
  - **2단 그래프 확장(자체 구현)** = qmd top-K를 시드로 wikilink 그래프 탐색. edge 타입별 가중치 / hop 감쇠 / 다중 시드 점수 합산 / 선택 노드 neighborhood 우선(기존 계약 유지) / 근거 경로(`used_paths`·`evidence_edges`) 산출 강화.
- **인덱싱 = 사이드카 소유 주기적 증분 재인덱싱**: 채팅 요청 경로에 인덱싱 비용을 두지 않는다(2026-07-14 T-006 실측 수용 — 종전 'api가 문서 확정·쓰기 시점에 이벤트 구동'하던 방식에서 정정, 아래 §실측 수용 정정).
- **graceful fallback**: qmd 사이드카 장애 시 기존 `keyword + edge distance` 경로로 자동 폴백한다 — 현행 MVP 로직이 삭제되지 않고 폴백으로 강등되어 잔존한다.

**근거**: 같은 지연 시간대에서 리랭크 off 시에도 정확도가 순증하고, 리랭크 토글로 품질을 추가 구매하며(추가 지연은 run polling UX가 흡수), 현행 keyword 스캔은 O(전체 문서) 규모라 문서가 늘면 역전된다. retriever는 chat(④)과 문서화③가 공유하는 컴포넌트(AXKG-SPEC-011)라, 2단 전환은 문서화③의 연결 후보 발굴에도 동일하게 적용된다.

**결정하지 않는 것(구현 기본값/OQ로 위임)**: edge 타입 가중치·hop 감쇠 함수·top-K 등 튜닝 숫자는 "구현 기본값으로 시작, 관찰 후 조정"으로 두고 스펙에 박지 않는다. qmd 통합 형태(subprocess CLI vs MCP)·클래스/파일 경로 등 구현 세부는 미결(OQ)로 코드 소관이다. (리랭크 기본값은 실측으로 off 확정 — 아래 §실측 수용 정정.)

**정합 대상**: AXKG-SPEC-006(§1 Ranking 메타·§5 Implementation Rules 재설계), AXKG-SPEC-011(retriever 공유 컴포넌트·실패 매핑 폴백). 알고리즘 상세는 발명하지 않는다.

### 실측 수용 정정 (2026-07-14 개정, PLAN-013-T-007 — WORK-008/T-006 CPU-only 실측)

WORK-008 구현 실측으로 위 개정의 기본값·구동 방식 2건을 사용자 수용 정정한다. **계약 골격(qmd 사이드카·2단 구조·graceful fallback·"채팅 요청 경로 인덱싱 비용 0")은 불변**이며, 실측으로 확정된 기본값/방식만 정정한다.

- **리랭크 기본값 on → off**: CPU-only 환경에서 LLM 리랭크 1회 60초+ 실측(qmd 공식 권장도 CPU는 off). 기본 off로 두고 AXKG-SPEC-007 설정 표면으로 on 가능, GPU 배포 시 on 권장. → OQ였던 리랭크 기본값이 여기서 결정으로 승격된다.
- **인덱싱: api 문서 확정·쓰기 시점 이벤트 구동 → 사이드카 소유 주기적 증분 재인덱싱**: qmd MCP가 index/update 툴을 노출하지 않아 api 이벤트 구동이 불가하다. 사이드카가 주기적 증분 재인덱싱을 소유하고, 확정 직후 검색 반영까지 수분 staleness를 허용한다(사용자 수용). "채팅 요청 경로에 인덱싱 비용 0" 계약은 불변.

튜닝 확정값(top-K·edge 가중치·hop 감쇠 등)은 스펙에 박지 않는다 — 위 "결정하지 않는 것"의 OQ 패턴 유지(코드 소관).

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| AXKG-SPEC-006 | update | Graph Chat을 Graph RAG 기반 AI 채팅으로 명시. (2026-07-14) retriever 2단 재설계(qmd 1단 + 그래프 확장 2단·리랭크 토글·인덱싱 시점·폴백) |
| AXKG-SPEC-007 | update | MVP 기본 provider를 `claude`로 확정. 리랭크 토글 설정 표면 owning spec |
| AXKG-SPEC-011 | update | (2026-07-14) retriever 공유 컴포넌트 2단 전환 정합·qmd 장애→폴백 매핑 |
