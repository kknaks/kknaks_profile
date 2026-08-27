---
type: work
id: AXKG-WORK-003
title: "WP2: 문서·그래프 코어 — parser·index·retriever·그래프 뷰"
status: done
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
progress: 100
created_at: 2026-07-07
updated_at: 2026-07-08
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/done
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

> Phase 1~3 실제 반영(PLAN-006-T-002). Phase 4(그래프 뷰 FE)는 미착수 후보.

| 경로 | 설명 | 상태 |
|---|---|---|
| `apps/api/axkg/storage/markdown_parser.py` · `markdown_root.py` | 파싱·root 접근(경로 안전) | 스텁→구현 |
| `apps/api/axkg/services/graph.py` · `documents.py` | index/rebuild/retriever/조회 서비스 | 스텁→구현 |
| `apps/api/axkg/repositories/documents.py` | documents/document_edges CRUD (session 접근 유일) | 신규 |
| `apps/api/axkg/dto/document.py` | DocumentDTO / DocumentEdgeDTO | 신규 |
| `apps/api/axkg/workers/graph_rebuild.py` | rebuild 트리거 3종(full·증분·startup scan) | 스텁→구현 |
| `apps/api/axkg/api/routes/documents.py` · `graph.py` | 조회·rebuild·link-preview 라우터 | 스텁→구현 |
| `apps/api/axkg/schemas/documents.py` · `graph.py` | 조회·그래프 응답 스키마 | 신규 |
| `apps/api/axkg/main.py` | startup scan 배선(best-effort) | 수정 |
| `apps/api/pyproject.toml` · `uv.lock` | pyyaml 명시 선언 | 수정 |
| `apps/web/app/graph/` | 그래프 뷰 (Phase 4) | 미착수 |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `documents` / `document_edges` | 전체 구현 (index·rebuild·resolve) |

- 상태 / invariant: PG 캐시는 언제든 Markdown에서 재빌드 가능(DEC-002). 본문 `[[ ]]`가 엣지 단일 소스.
- Migration 필요 여부: 없음(WP0 완료).
- SPEC에 환류: retriever top-N 기본값 확정 시 SPEC-011 OQ 갱신.

## Execution

### Phase 1 — parser + index

- **Status**: DONE (PLAN-006-T-002)
- **작업**:
  - [x] frontmatter/wikilink/up 파서 + 정규화
  - [x] documents index upsert(content_hash), stem/alias resolve, duplicate 거부
- **검증**: [x] SPEC-005 Link Syntax·Required Frontmatter 계약 단위 테스트 (`test_markdown_parser.py` 11 · `test_markdown_root.py` 5)

### Phase 2 — edges rebuild + 트리거

- **Status**: DONE (PLAN-006-T-002)
- **작업**:
  - [x] assoc/lineage 엣지 생성, links 비엣지, is_broken 마킹
  - [x] startup scan / 증분 / `POST /graph/rebuild`
- **검증**: [x] 외부 편집 시나리오(파일 직접 수정 → rebuild → 엣지 갱신) 통과 (`test_external_edit_incremental_rebuild` · `test_incremental_rebuild_updates_edges_on_body_change`)

### Phase 3 — retriever + 조회 API

- **Status**: DONE (PLAN-006-T-002)
- **작업**:
  - [x] keyword+edge distance retriever, neighborhood 우선, index 스냅샷 제공
  - [x] documents/graph 조회·검색·link-preview 라우터
- **검증**: [x] `BROKEN_WIKILINK` 등 Case Matrix, 검색 순위 스모크 (`test_graph_core.py` 11 · `test_graph_api.py` 12, admin 게이트 194 passed)

### Phase 4 — 그래프 뷰 (FE)

- **Status**: DONE (PLAN-006-T-008, tsc+build 통과)
- **작업**:
  - [x] force graph 렌더(react-force-graph-2d+d3-force, ssr:false dynamic) + 노드 선택 → 문서 상세(상류 up/하류/backlink/참조 wikilink). `type=source` 제외, assoc 실선/lineage 점선+화살표. 채팅 패널(SPEC-006)은 WP4 제외.
- **검증**: [x] SPEC-005 U-2 AC (page-graph.html 좌측 그래프 섹션 시안), `/graph` 라이브 200 컴파일 (노드=데이터id, 상세 links/backlink)

## Pre-deploy Check

- [x] document root 밖 경로 접근 거부 (`test_reject_absolute_path` · `test_reject_parent_escape`)
- [x] rebuild가 Markdown을 쓰지 않음 (읽기 전용) (`test_rebuild_is_read_only`)

## Rollback

- 작업 레포 커밋 단위 revert. 캐시는 rebuild로 복구 가능.

## Done Criteria

- [x] 모든 Phase DONE/SUPERSEDED (Phase 1~4 done)
- [x] SPEC-005 AC 전부 반영 (BE 계약 AC + U-2 그래프 뷰 AC done)
- [x] product `log.md`·`30-work/README.md` 갱신 (PLAN-006-T-005)

## Open Issues

- retriever 기본값 확정(구현): `top_n=8`, `snippet_len=240`, neighborhood boost `{거리1:+4, 거리2:+2}`, keyword 가중치(title/alias +3 / tag +2 / body 출현 최대 +3). WP3 Apply Executor로 확정 문서 유입 시작 — 라이브 데이터 축적 후 SPEC-011 OQ로 값 튜닝(스펙 환류는 admin 판단). PLAN-006-T-002.
- 그래프 뷰 후속 개선(비차단, PLAN-006-T-008): 자동 fit/zoom 미적용(노드 소수라 무해), document_type 색 팔레트 FE 하드코딩(globals.css tier 토큰 통일 여지), "문서 열기"=source_url(단일 문서 뷰어 라우트 생기면 path 딥링크로 교체).
