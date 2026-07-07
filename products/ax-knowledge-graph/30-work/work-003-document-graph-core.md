---
type: work
id: AXKG-WORK-003
title: "WP2: 문서·그래프 코어 — parser·index·retriever·그래프 뷰"
status: todo
product: ax-knowledge-graph
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-002-markdown-sot-postgres-storage|AXKG-DEC-002]]"
    - "[[decision-003-graph-rag-chat-and-default-claude|AXKG-DEC-003]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
  works:
    - "[[work-001-mvp-pipeline-scaffold|AXKG-WORK-001]]"
  releases: []
  related: []
---

# WP2: 문서·그래프 코어 — parser·index·retriever·그래프 뷰

Markdown SoT를 파싱해 `documents`/`document_edges` 캐시를 만들고, 그래프 조회·검색·retriever를 제공한다. **WP3(게이트)과 WP4(chat)의 전제**다 — 문서화 게이트의 연결 후보 컨텍스트(2단 하이브리드)와 chat의 evidence 검색이 여기서 나온다.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-005(링크·그래프 계약)
- Depends on work: AXKG-WORK-001(WP0)
- Parallel work: AXKG-WORK-002(WP1)와 병렬 가능
- Follow-up work: AXKG-WORK-004(WP3), AXKG-WORK-005(WP4)
- External dependency: 없음 (AI 호출 없는 순수 코어)

## Scope

포함:

- markdown parser (`storage/markdown_parser.py`): frontmatter(type/id/title/aliases/up/source/links) + 본문 `[[ ]]` 파싱, `[[stem|label]]`/`[[folder/stem]]` 정규화
- documents index: path/stem/aliases/title/document_type/content_hash, stem/alias resolve, duplicate stem 거부
- document_edges rebuild: `[[ ]]`→assoc, `up`(본문 동반 필수)→lineage, `links`는 엣지 아님, is_broken(외부 편집 사후 표시)
- rebuild 트리거 3종: startup scan(content_hash 비교) / 증분(문서 단위) / `POST /graph/rebuild`
- link validation: `BROKEN_WIKILINK`/`UP_WITHOUT_BODY_LINK`/`DUPLICATE_STEM`, `POST /documents/{id}/link-preview`
- retriever (`services/graph`): keyword score + edge distance, selected node neighborhood 우선 — **chat(④)과 문서화 게이트(③) 공유 컴포넌트** + documents index 경량 스냅샷 제공(연결 후보 컨텍스트 2단의 원천)
- graph/documents API: `GET /documents*`, `GET /documents/{id}/links`, `GET /graph/documents`, `neighborhood`, `POST /graph/search`, `POST /graph/rebuild`
- FE: 그래프 뷰(`/graph` 좌측) — react-force-graph-2d + d3-force (DEC-004: 기존 `/graph` 구현 참고), 노드 클릭 → 문서 상세/링크·백링크, `type=source` 기본 제외. **기준: `21-html/page-graph.html` — 레이아웃·한국어 카피 모두 시안을 따른다**

제외:

- Graph RAG chat 응답 생성 (WP4 — retriever만 여기)
- 문서 생성/수정 쓰기 경로 (WP3 apply executor)
- pgvector/embedding (post-MVP, DEC-003)

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/storage/markdown_parser.py` · `markdown_root.py` | 파싱·root 접근(경로 안전) |
| `apps/api/axkg/services/graph.py` · `documents.py` + `repositories/documents.py` · `document_edges.py` | index/rebuild/retriever/조회 |
| `apps/api/axkg/workers/graph_rebuild.py` | rebuild 트리거 |
| `apps/api/axkg/api/routes/documents.py` · `graph.py` | 조회·rebuild·link-preview 라우터 |
| `apps/web/app/graph/` | 그래프 뷰 |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `documents` / `document_edges` | 전체 구현 (index·rebuild·resolve) |

- 상태 / invariant: PG 캐시는 언제든 Markdown에서 재빌드 가능(DEC-002). 본문 `[[ ]]`가 엣지 단일 소스.
- Migration 필요 여부: 없음(WP0 완료).
- SPEC에 환류: retriever top-N 기본값 확정 시 SPEC-011 OQ 갱신.

## Execution

### Phase 1 — parser + index

- **Status**: TODO
- **작업**:
  - [ ] frontmatter/wikilink/up 파서 + 정규화
  - [ ] documents index upsert(content_hash), stem/alias resolve, duplicate 거부
- **검증**: [ ] SPEC-005 Link Syntax·Required Frontmatter 계약 단위 테스트

### Phase 2 — edges rebuild + 트리거

- **Status**: TODO
- **작업**:
  - [ ] assoc/lineage 엣지 생성, links 비엣지, is_broken 마킹
  - [ ] startup scan / 증분 / `POST /graph/rebuild`
- **검증**: [ ] 외부 편집 시나리오(파일 직접 수정 → rebuild → 엣지 갱신) 통과

### Phase 3 — retriever + 조회 API

- **Status**: TODO
- **작업**:
  - [ ] keyword+edge distance retriever, neighborhood 우선, index 스냅샷 제공
  - [ ] documents/graph 조회·검색·link-preview 라우터
- **검증**: [ ] `BROKEN_WIKILINK` 등 Case Matrix, 검색 순위 스모크

### Phase 4 — 그래프 뷰 (FE)

- **Status**: TODO
- **작업**:
  - [ ] force graph 렌더 + 노드 선택 → 문서 상세(링크/백링크/lineage)
- **검증**: [ ] SPEC-005 U-2 AC (page-graph.html 시안 참고)

## Pre-deploy Check

- [ ] document root 밖 경로 접근 거부
- [ ] rebuild가 Markdown을 쓰지 않음 (읽기 전용)

## Rollback

- 작업 레포 커밋 단위 revert. 캐시는 rebuild로 복구 가능.

## Done Criteria

- [ ] 모든 Phase DONE/SUPERSEDED
- [ ] SPEC-005 AC 전부 반영
- [ ] product `log.md`·`30-work/README.md` 갱신

## Open Issues

- retriever top-N 기본값·발췌 길이 (SPEC-011 OQ — 구현 기본값으로 시작).
