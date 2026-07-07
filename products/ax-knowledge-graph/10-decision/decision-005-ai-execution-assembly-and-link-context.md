---
type: decision
id: AXKG-DEC-005
title: "AI 실행 파이프라인 계약: 3자 조립·연결 후보 컨텍스트·MVP 문서화 범위 확정"
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
    - "[[decision-003-graph-rag-chat-and-default-claude|AXKG-DEC-003]]"
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
  specs:
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-009-prompt-dynamic-management|AXKG-SPEC-009]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works: []
  releases: []
  related: []
---

# AI 실행 파이프라인 계약: 3자 조립·연결 후보 컨텍스트·MVP 문서화 범위 확정

구현 착수 전 gap 리뷰(2026-07-07)에서 확인된 blocker를 닫는 결정이다.

## Decision

- **연결 후보 입력 컨텍스트(2단 하이브리드)**: 문서화 게이트(③) 초안 AI가 기존 그래프에서 연결 후보를 만들 때의 입력은 두 단으로 구성한다.
  1. Graph RAG retriever(AXKG-DEC-003의 keyword score + edge distance)를 재사용해 관련 기존 문서 top-N 후보를 추출한다.
  2. documents index 경량 스냅샷(`stem`·`aliases`·`title`·`document_type`)을 항상 함께 주입해, AI가 생성하는 wikilink가 유효한 stem/alias만 가리키게 한다.
  - 외부 그래프 도구(Graphify 등)는 제품 서빙 경로에 도입하지 않는다. Markdown→PostgreSQL 캐시(AXKG-DEC-002)가 유일한 그래프 원천이다. Graphify류 도구의 배치 enrichment 활용은 post-MVP 검토 항목으로 남긴다.
- **3자 조립(템플릿+프롬프트+output_schema)의 주체와 순서**: 백엔드 context builder가 조립하고, AI는 조립된 컨텍스트를 채우기만 한다. 순서는 `template(뼈대) → prompt(지시) → output_schema(출력 강제)`. `ai_task_definitions.template_key` 바인딩과 `ai_tasks.template_version_id` 스냅샷을 둔다.
- **output_schema 경계**: `output_schema`는 게이트 payload envelope(`classification.v1`/`documentation.v1`, AXKG-SPEC-002)의 form/구조 필드 내부만 관장한다. envelope 자체는 코드 고정 계약이다.
- **output_schema 표현 형식**: JSON Schema로 확정한다. 백엔드가 FastAPI/Python(Pydantic ↔ JSON Schema 상호변환)이고 AI provider structured output이 JSON Schema 기반이므로 대안이 없다.
- **AI 실행 파이프라인 spec 신설**: 4개 AI 스테이지(①요약 ②분류 ③문서초안 ④Graph RAG chat)의 공통 실행 계약 — 입력 컨텍스트 구성, 3자 조립, 구조화 출력 파싱·검증, 실패→`ai_tasks` 상태 매핑, 콘텐츠 수집 — 은 AXKG-SPEC-011이 SSOT다. 요약 AI(①)의 실행 계약(AXKG-SPEC-003과 AXKG-SPEC-001 사이에서 소관이 비어 있던 부분)은 SPEC-011 소관으로 확정한다.
- **project destination 문서화 MVP 포함**: project destination의 product 문서(baseline 후보) 초안 생성을 MVP에 포함한다. AXKG-SPEC-010의 템플릿 MVP scope를 `reference`·`permanent`·`project_baseline` 3종으로 확장한다.
- **SPEC-009·010 채택 근거 소급 부여**: 프롬프트·템플릿의 DB 동적 관리(AXKG-SPEC-009/010)는 이 결정으로 채택을 승인한다. AXKG-DEC-004의 "reference note 양식은 별도 template directory를 만들지 않고 문서 링크/frontmatter spec에 포함한다" 항목은 이 결정이 대체한다(supersede) — 파일 template directory를 만들지 않는다는 원칙은 유지하되, 문서 뼈대는 PostgreSQL 템플릿(AXKG-SPEC-010)에서 동적 관리하고 링크/frontmatter 계약의 SSOT는 여전히 AXKG-SPEC-005다.

## Rationale

- 연결 품질은 제품 핵심 가치(AXKG-BL-001)인데, 초안 AI가 그래프 컨텍스트 없이 wikilink를 생성하면 executor의 깨진 링크 거부(AXKG-SPEC-004)와 구조적으로 충돌한다. retriever 재사용은 새 기계 없이 관련성을, index 스냅샷은 링크 유효성을 보장한다.
- 조립을 AI에게 맡기면 출력 구조 보장이 약해지고 버전 스냅샷 추적이 애매해진다. BE 조립은 재현성과 감사 추적(`prompt_version_id`+`template_version_id`)을 확보한다.
- 실행 계약이 스펙 없이 아키텍처 문서에만 있으면 요약 스테이지처럼 소관이 비는 구멍이 생긴다. 관리(009/010)와 실행(011)을 분리해 각자 SSOT를 갖게 한다.
- project 문서화를 빼면 수집-분류-문서화 파이프라인이 PARA 4분류 중 하나에서 끊긴다. MVP에서 baseline 후보 한 종으로 좁혀 포함한다.

## Resulting Spec

| Spec | Action |
|---|---|
| AXKG-SPEC-011 | create — AI 실행 파이프라인(4스테이지 공통 실행 계약) |
| AXKG-SPEC-004 | update — 초안 생성 입력 컨텍스트를 SPEC-011 참조로 연결, 템플릿 소비 문구 정리 |
| AXKG-SPEC-005 | update — 연결 후보 컨텍스트(S-1)를 SPEC-011 계약으로 연결 |
| AXKG-SPEC-009 | update — output_schema 형식 JSON Schema 확정, 로드/조립 주체를 SPEC-011로 명시 |
| AXKG-SPEC-010 | update — 3자 조립 OQ 해소, MVP scope에 `project_baseline` 템플릿 추가 |

## Open Questions

- ~~콘텐츠 수집(URL 본문 fetch/유튜브 transcript)의 실행 위치~~ → **AXKG-SPEC-012로 확정**: BE 내 Source Collection Adapter(YouTube/정적 웹/동적 웹)가 수집하고 SourceMaterial로 정규화해 SPEC-011 context builder에 넘긴다. dynamic adapter의 브라우저 실행 분리 여부만 SPEC-012 OQ로 잔존.
- Graphify류 외부 그래프 도구의 배치 enrichment(후보 엣지 제안) 활용은 post-MVP 검토.
