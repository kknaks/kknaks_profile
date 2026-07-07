---
type: spec
id: AXKG-SPEC-011
title: "AI 실행 파이프라인: 컨텍스트 조립·구조화 출력·실패 계약"
status: stable
product: ax-knowledge-graph
version: 0.0.1
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/spec
  - status/stable
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-003-graph-rag-chat-and-default-claude|AXKG-DEC-003]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
    - "[[spec-002-approval-gate-feedback-loop|AXKG-SPEC-002]]"
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-007-ai-provider-settings|AXKG-SPEC-007]]"
    - "[[spec-009-prompt-dynamic-management|AXKG-SPEC-009]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
  works:
    - "[[work-001-mvp-pipeline-scaffold|AXKG-WORK-001]]"
  releases: []
  related: []
---

# AI 실행 파이프라인: 컨텍스트 조립·구조화 출력·실패 계약

제품의 4개 AI 스테이지(①요약 ②분류 ③문서초안 ④Graph RAG chat)가 **무엇을 입력받아, 어떻게 조립되고, 어떤 구조로 출력하며, 실패하면 어디에 어떻게 남는지**의 공통 실행 계약을 보장한다. 프롬프트/템플릿의 **관리**(AXKG-SPEC-009/010)와 분리된, **실행**의 SSOT다.

> 근거: AXKG-DEC-005. 각 스테이지의 UX·게이트 동작은 각 소관 spec(AXKG-SPEC-001/003/004/006)이, provider 바인딩은 AXKG-SPEC-007이, 프롬프트·템플릿 버전 관리는 AXKG-SPEC-009/010이 정의한다. 이 spec은 그 사이의 실행 경로만 다룬다.

## 1. Context

### Meta

- Decision reference: AXKG-DEC-005(실행 계약·3자 조립·연결 컨텍스트), AXKG-DEC-001(파이프라인), AXKG-DEC-003(retriever)
- Baseline reference: AXKG-BL-001
- Domain note: `AI Stage`, `Context Builder`, `Assembly`, `Connection Candidate Context`, `Structured Output`, `Code Fallback`
- 실행 주체: 모든 AI 실행은 FastAPI가 `ai_tasks` row를 만들고 open-kknaks task로 위임한다. AI는 DB/Markdown을 직접 변경하지 않는다(AXKG-SPEC-004 executor 규칙).

### Business Requirement

요약 AI의 실행 계약이 AXKG-SPEC-003("SPEC-001 소관")과 AXKG-SPEC-001("summarized 이후만 다룸") 사이에서 비어 있었고, 문서초안 AI가 기존 그래프의 무엇을 보고 연결을 만드는지가 미정의였다. 실행 계약이 없으면 각 스테이지 구현이 서로 다른 방식으로 컨텍스트를 조립하고, 깨진 wikilink·파싱 실패가 사용자에게 일관되지 않게 표면화된다. 4스테이지가 같은 실행 규칙을 따라야 한다.

### Scope

In scope:

- 스테이지별 입력 컨텍스트 구성(context builder) 계약
- 문서초안 AI의 **연결 후보 검색 컨텍스트**(2단 하이브리드, AXKG-DEC-005)
- 템플릿+프롬프트+output_schema **3자 조립** 계약(주체·순서·버전 스냅샷)
- 구조화 출력(JSON Schema) 강제와 파싱·검증 실패 처리
- 실패의 `ai_tasks` 상태 매핑과 스테이지별 표면화
- 요약 스테이지의 `SourceMaterial` 입력 조립 계약(수집 adapter 자체는 AXKG-SPEC-012)
- 프롬프트/템플릿 로드 실패 시 코드 fallback 실행(AXKG-SPEC-009/010 S-3의 실행측 계약)

Out of scope:

- 프롬프트·템플릿 편집/버전 UI (AXKG-SPEC-009/010)
- provider·model·options 선택과 해석 (AXKG-SPEC-007)
- 게이트 승인/피드백 UX와 버전 규칙 (AXKG-SPEC-001/002/004)
- chat 세션/run polling UX (AXKG-SPEC-006)
- source type별 원문 수집 adapter 세부 (AXKG-SPEC-012)
- retriever 랭킹 알고리즘 세부 (AXKG-DEC-003, 구현 소관)
- Apply Executor의 검증·적용 규칙 (AXKG-SPEC-004)

## 2. UX Contract

이 spec은 새 화면을 추가하지 않는다. 실행 상태는 기존 소관 spec의 화면으로 표면화된다.

| 스테이지 | 표면 위치 | 소관 spec |
|---|---|---|
| ① 요약 | Source Inbox 요약 카드, `요약 재시도` CTA | AXKG-SPEC-003 |
| ② 분류 | 분류 게이트 카드, `재시도` CTA | AXKG-SPEC-001/002 |
| ③ 문서초안 | 문서화 게이트, `초안 생성 재시도` CTA | AXKG-SPEC-004 |
| ④ chat | run polling 상태, 실패 메시지 | AXKG-SPEC-006 |

## 3. User Scenario

### S-1. System — 요약 스테이지 실행

1. source가 등록되면(`received`) 시스템은 `ai_tasks(task_type=collect_source_summary)`를 만든다.
2. context builder가 AXKG-SPEC-012 Source Collection Adapter를 호출해 `SourceMaterial`을 얻고 입력 컨텍스트를 구성한다.
3. 활성 요약 프롬프트+output_schema(AXKG-SPEC-009)를 로드해 조립하고 open-kknaks로 실행한다.
4. 출력(`title`·`summary`·`keywords`·`source_type`)이 스키마 검증을 통과하면 `sources.summary_payload`에 저장되고 `summarized`가 된다.
5. 수집 또는 실행이 실패하면 `ai_tasks.status=failed`가 보존되고 source는 `collection_failed`로 표면화된다(AXKG-SPEC-003).

### S-2. System — 문서초안 스테이지의 연결 후보 컨텍스트 조립

1. 분류 게이트가 `project`/`area`/`resource`로 승인되면 문서화 게이트와 `ai_tasks(generate_documentation_gate)`가 생성된다.
2. context builder는 source 요약·분류 결과를 질의로 Graph RAG retriever(AXKG-DEC-003)를 호출해 관련 기존 문서 top-N 후보(발췌 포함)를 얻는다.
3. context builder는 documents index 경량 스냅샷(`stem`·`aliases`·`title`·`document_type`)을 함께 주입한다.
4. 활성 destination 템플릿(AXKG-SPEC-010) → 활성 프롬프트(AXKG-SPEC-009) → output_schema 순으로 조립해 실행한다.
5. AI는 후보와 스냅샷 안에서만 `up:`/`[[ ]]` 연결과 `derived_suggestions`를 만들고, 각 연결에 `link_reason`을 남긴다(AXKG-SPEC-005).

### S-3. System — 구조화 출력 파싱 실패

1. AI 출력이 JSON 파싱에 실패하거나 output_schema 검증에 실패한다.
2. 시스템은 부분 결과를 소비하지 않고 해당 실행을 실패로 처리한다: `ai_tasks.status=failed`, `error_code=OUTPUT_SCHEMA_MISMATCH`(파싱 실패는 `OUTPUT_PARSE_FAILED`).
3. 실패한 task row는 불변으로 보존되고, 재시도는 `retry_of_task_id`로 새 row를 만든다(AXKG-SPEC-002/003 공통 규칙).
4. 스테이지 소관 spec의 실패 UI(재시도 CTA)가 표면화한다.

### S-4. System — 활성 프롬프트/템플릿 로드 실패 fallback

1. 실행 시 활성 프롬프트 버전 또는 활성 템플릿 버전 로드가 실패한다.
2. context builder는 코드 내장 fallback 프롬프트/스키마/템플릿으로 조립을 계속한다(파이프라인을 중단하지 않는다).
3. fallback 사용 사실은 `ai_tasks.payload`에 기록되고 관찰 가능해야 한다. 이때 `prompt_version_id`/`template_version_id`는 null이다.

## 4. Interface Contract

### Stage Execution Contract

| 스테이지 | task_type | handler_kind | 입력 컨텍스트 | 출력 | 소비처 |
|---|---|---|---|---|---|
| ① 요약 | `collect_source_summary` | `source_summary` | source URL + `SourceMaterial`(AXKG-SPEC-012) | `title`, `summary`, `keywords`, `source_type` | `sources.summary_payload`, 요약 카드 |
| ② 분류 | `generate_classification_gate`, `regenerate_classification_gate` | `classification_gate` | 요약 payload + PARA 분류 기준. **그래프 컨텍스트 없음**(연결은 ③ 소관, AXKG-SPEC-001 §5) | `classification.v1` form 필드(AXKG-SPEC-002) | 분류 게이트 revision |
| ③ 문서초안 | `generate_documentation_gate`, `regenerate_documentation_gate` | `documentation_gate` | 요약+확정 destination + **활성 템플릿** + **연결 후보 컨텍스트**(아래) + (재생성 시) 피드백·이전 세션 | `documentation.v1` payload: draft(markdown_full) + derived_suggestions + apply_plan 제안 | 문서화 게이트 revision |
| ④ chat | `graph_rag_chat` | `graph_rag_chat` | 질문 + retriever 결과(evidence 문서) + 세션 이력 | 답변 + evidence | `graph_chat_runs`/messages |

이 표의 `task_type` 목록이 제품 전체 `ai_tasks.task_type` enum의 SSOT다. AXKG-SPEC-002는 게이트 4종만 참조하고, 새 task_type은 이 표에 먼저 등재한다.

### Connection Candidate Context (③ 전용, AXKG-DEC-005)

문서초안 AI의 입력 컨텍스트에는 아래 두 단이 **항상** 포함된다.

| 단 | 내용 | 목적 |
|---|---|---|
| 1. retriever 후보 | Graph RAG retriever(keyword score + edge distance) top-N 관련 문서 — 각 후보는 `stem`, `title`, `document_type`, 본문 발췌 | 연결 **관련성**: `up:`/`[[ ]]`·derived_suggestions의 실질 후보 |
| 2. index 스냅샷 | 전체 documents index의 경량 목록 — `stem`, `aliases`, `title`, `document_type` | 연결 **유효성**: 생성되는 wikilink target이 resolve 가능함을 보장 |

규칙:

- AI는 index 스냅샷에 없는 stem/alias를 wikilink target으로 생성하지 않는다. 스냅샷 밖 링크는 link-preview/executor의 `BROKEN_WIKILINK` 검증(AXKG-SPEC-005)에서 거부된다.
- 모든 연결 후보 채택에는 `link_reason`을 남긴다(AXKG-SPEC-004 DerivedSuggestion / AXKG-SPEC-005 Implementation Rules).
- top-N 기본값과 발췌 길이는 구현 기본값으로 두되, `ai_tasks.payload`에 실제 주입된 컨텍스트를 스냅샷한다.
- retriever는 chat(④)과 문서초안(③)이 **공유**하는 컴포넌트다(`domain.graph`).

### Assembly Contract (3자 조립, AXKG-DEC-005)

- 조립 주체는 **백엔드 context builder**다. AI는 조립된 컨텍스트를 채우기만 한다.
- 조립 순서: `template(뼈대, AXKG-SPEC-010)` → `prompt(지시, AXKG-SPEC-009)` → `output_schema(출력 강제)`.
- 템플릿은 `handler_kind=documentation_gate`에서만 조립된다. 바인딩은 `ai_task_definitions.template_key`, 사용 버전은 `ai_tasks.template_version_id`로 스냅샷한다.
- 프롬프트 사용 버전은 `ai_tasks.prompt_version_id`로 스냅샷한다.
- `output_schema`는 **JSON Schema**다. 게이트 payload envelope(`classification.v1`/`documentation.v1`)은 코드 고정이며, output_schema는 envelope 내부의 form/구조 필드만 관장한다.

### Validation

| 항목 | 규칙 |
|---|---|
| AI 출력 | JSON 파싱 가능해야 하고 활성(또는 fallback) output_schema 검증을 통과해야 함 |
| wikilink target | index 스냅샷의 stem/alias로 resolve 가능해야 함(AXKG-SPEC-005) |
| 조립 스냅샷 | 성공 실행의 `ai_tasks`는 사용한 `prompt_version_id`(+③은 `template_version_id`)를 가져야 함. fallback 실행은 null + payload 기록 |
| 부분 소비 금지 | 스키마 검증 실패 출력은 어떤 필드도 소비하지 않음 |

### Case Matrix

| 에러 코드 | 백엔드 출력 | 표면화 | 표시 위치 |
|---|---|---|---|
| `CONTENT_FETCH_FAILED` | Source Collection Adapter 수집 실패 | source `collection_failed` + `요약 재시도` | Source Inbox (AXKG-SPEC-003) |
| `OUTPUT_PARSE_FAILED` | AI 출력 JSON 파싱 실패 | task failed + 스테이지별 재시도 CTA | 각 스테이지 화면 |
| `OUTPUT_SCHEMA_MISMATCH` | output_schema 검증 실패 | task failed + 스테이지별 재시도 CTA | 각 스테이지 화면 |
| `PROMPT_FALLBACK_USED` | 활성 프롬프트 로드 실패(실행은 계속) | 관찰 로그/payload 기록 | 실패 아님 |
| `TEMPLATE_FALLBACK_USED` | 활성 템플릿 로드 실패(실행은 계속) | 관찰 로그/payload 기록 | 실패 아님 |

### Flow

```mermaid
sequenceDiagram
    participant Trigger as 스테이지 트리거
    participant BE as FastAPI (context builder)
    participant Store as PostgreSQL
    participant OK as open-kknaks

    Trigger->>BE: ai_tasks 생성(task_type)
    BE->>Store: ai_task_definitions 해석(handler_kind, prompt_key, template_key)
    BE->>Store: 활성 프롬프트+output_schema 로드 (실패 시 코드 fallback)
    alt handler_kind = documentation_gate
        BE->>Store: 활성 템플릿 로드 (실패 시 코드 fallback)
        BE->>Store: retriever top-N + documents index 스냅샷
    end
    BE->>BE: 조립: template -> prompt -> output_schema
    BE->>Store: ai_tasks 스냅샷(prompt_version_id, template_version_id, payload)
    BE->>OK: task 실행
    OK-->>BE: 출력
    alt 파싱·스키마 검증 통과
        BE->>Store: 스테이지별 결과 저장(summary_payload / revision / run)
    else 실패
        BE->>Store: ai_tasks.status=failed (error_code)
    end
```

### State / Lifecycle

이 spec은 새 상태를 만들지 않는다. 실행 결과는 기존 상태 모델로 매핑된다.

| 실행 결과 | 매핑 |
|---|---|
| ① 성공 / 실패 | `sources.summarized` / `sources.collection_failed` (AXKG-SPEC-003 SSOT) |
| ②③ 성공 / 실패 | 게이트 revision 생성 / 게이트 `failed` + 재시도 (AXKG-SPEC-002) |
| ④ 성공 / 실패 | `graph_chat_runs.succeeded` / `failed` (AXKG-SPEC-006) |
| 공통 | `ai_tasks.status` = `queued→running→succeeded|failed|cancelled`, 재시도는 `retry_of_task_id` 새 row |

## 5. Implementation Rules

- 모든 AI 실행은 등록된 `ai_task_definitions`를 거친다. handler 코드는 동적이지 않다(설정에서 임의 코드 실행 불가).
- 요약 스테이지는 AXKG-SPEC-012 Source Collection Adapter가 반환한 `SourceMaterial`을 입력 컨텍스트로 사용한다. 수집 실패는 `collection_failed`로 표면화한다.
- `SourceMaterial.content_text`가 최대 입력 길이를 초과하면 요약 스테이지가 chunk로 나눠 각각 요약한 뒤 하나의 summary로 병합한다(AXKG-SPEC-012 후처리 계약 연동). chunk 요약도 같은 output_schema를 따르고, 병합 결과만 `sources.summary_payload`에 저장한다.
- 분류 스테이지(②)에는 그래프 컨텍스트를 주입하지 않는다. 연결 생성은 문서초안 스테이지(③)의 전속 책임이다.
- 문서초안 스테이지(③)의 입력에는 연결 후보 컨텍스트 2단(retriever top-N + index 스냅샷)이 항상 포함된다.
- 3자 조립은 백엔드 context builder가 수행하고, 실행마다 사용 버전을 `ai_tasks`에 스냅샷한다.
- output_schema는 JSON Schema이며, 구조화 출력을 강제한다. 검증 실패 출력은 소비하지 않고 task를 실패 처리한다.
- 활성 프롬프트/템플릿 로드 실패는 실행을 중단시키지 않는다. 코드 fallback으로 계속하되 관찰 가능하게 기록한다.
- 실패한 `ai_tasks`는 불변 보존하고, 재시도는 `retry_of_task_id`로 연결된 새 row다.
- 재생성(피드백) 실행은 원 revision의 `open_kknaks_session_id`를 resume 컨텍스트로 사용한다(AXKG-SPEC-002).

## 6. Verification

### Acceptance Criteria

- [ ] 4개 task_type 전부가 `ai_task_definitions` 해석 → 조립 → 실행 → 스냅샷의 같은 경로를 탄다.
- [ ] 문서초안 실행의 `ai_tasks.payload`에 retriever 후보와 index 스냅샷이 기록된다.
- [ ] 문서초안 출력의 모든 wikilink target이 index 스냅샷의 stem/alias로 resolve된다(스냅샷 밖 링크는 `BROKEN_WIKILINK`로 거부).
- [ ] 성공한 ③ 실행의 `ai_tasks`에 `prompt_version_id`와 `template_version_id`가 스냅샷된다.
- [ ] output_schema(JSON Schema) 검증 실패 시 어떤 필드도 소비되지 않고 task가 실패 처리된다.
- [ ] 요약 수집 실패가 `collection_failed` + `요약 재시도`로 표면화된다.
- [ ] 활성 프롬프트/템플릿 로드 실패 시 코드 fallback으로 실행이 계속되고 그 사실이 기록된다.
- [ ] 분류 스테이지 입력에 그래프 컨텍스트가 없다.

## 7. Open Questions

- Source Collection Adapter의 실행 위치(FastAPI 내 fetcher vs worker 위임)는 구현 시 결정한다. 어느 쪽이든 AXKG-SPEC-012의 adapter 계약과 이 spec의 실패 매핑을 따른다.
- retriever top-N 기본값과 후보 발췌 길이는 구현 기본값으로 시작하고, 초안 품질 관찰 후 조정한다.
