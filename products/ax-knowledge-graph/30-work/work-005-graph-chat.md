---
type: work
id: AXKG-WORK-005
title: "WP4: Graph RAG Chat"
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
updated_at: 2026-07-09
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-003-graph-rag-chat-and-default-claude|AXKG-DEC-003]]"
  specs:
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works:
    - "[[work-003-document-graph-core|AXKG-WORK-003]]"
  releases: []
  related: []
---

# WP4: Graph RAG Chat

지식그래프를 검색 컨텍스트로 쓰는 AI 채팅. WP2의 retriever를 재사용하고, WP0 실행 골격에 chat 스테이지(④)를 배선한다. WP5(설정)와 병렬 가능.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-006(Graph Chat), AXKG-SPEC-011④(chat 스테이지)
- Depends on work: AXKG-WORK-003(WP2 — retriever·graph)
- Parallel work: AXKG-WORK-006(WP5)
- Follow-up work: pgvector 검색 품질 개선 (post-MVP, DEC-003)
- External dependency: 없음 (open-kknaks 바인딩은 WP1에서 확정됨 전제)

## Scope

포함:

- chat 저장 모델 사용: `graph_chat_sessions`/`messages`/`runs` 서비스·레포 (user-scoped, soft delete)
- API: `GET/POST /graph/chats`, `GET /graph/chats/{chat_id}`, `POST /graph/chats/{chat_id}/messages`, `GET /graph/chats/{chat_id}/runs/{run_id}` — run polling 모델 (단발 `/graph/chat` 없음)
- chat 스테이지(④): `graph_rag_chat` context builder — retriever(keyword+edge distance, selected node neighborhood 우선) + evidence 문서 + 세션 이력을 조립한다. 실행 규칙은 seed된 `graph_rag_chat` DB 프롬프트(`axkg/seeds.py`)가 담는다(api가 디스크 `.md`를 런타임 로드하지 않음; 규칙 원천/SSOT 문서는 worker 프로젝트 컨텍스트 `context/graph-chat-rules.md`, AXKG-SPEC-011). 기존 세션은 `last_open_kknaks_session_id` resume
- 응답 계약: answer/evidence_documents/evidence_edges/used_paths/confidence/missing_context, 근거 부족 시 `INSUFFICIENT_GRAPH_CONTEXT`(추측 금지)
- 결과 저장: assistant message + evidence + run result_payload + retrieval_context 스냅샷
- FE: `/graph` 우측 chat 패널 — 세션 목록, 메시지, run polling 로딩 상태, evidence 문서 카드(클릭 → 그래프 노드/문서), 실패 표면. **기준: `21-html/page-graph.html` — 레이아웃·한국어 카피 모두 시안을 따른다**

제외:

- 그래프 뷰 자체 (WP2), pgvector/embedding, 팀 공유 세션

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/api/routes/graph.py` | chats/runs 라우터 |
| `apps/api/axkg/services/chat.py` + `repositories/chat.py` | 세션·메시지·run lifecycle |
| `apps/api/axkg/services/ai/` | ④ context builder 등록 + resume 배선 |
| `apps/web/app/graph/` | chat 패널 |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `graph_chat_sessions` / `graph_chat_messages` / `graph_chat_runs` | 전체 구현 |
| `ai_tasks` | `graph_rag_chat` 실사용 |

- 상태 / invariant: polling은 `graph_chat_runs.status`를 읽는다(원시 open-kknaks 상태 노출 금지). evidence는 실제 사용 문서만.
- Migration 필요 여부: 없음.
- SPEC에 환류: 없음 예상.

## Execution

### Phase 1 — 세션/run API

- **Status**: DONE (PLAN-007-T-001, profile-be T-011)
- **랜딩**: chat 세션/메시지/run lifecycle·폴링 API 5종(`GET/POST /graph/chats`, `GET /graph/chats/{id}`, `POST /graph/chats/{id}/messages`, `GET /graph/chats/{id}/runs/{run_id}`), 검증(EMPTY_QUESTION/NODE_NOT_FOUND), user 스코프 격리(타 유저 404), pytest 10 passed(회귀 233). AI 실행 배선은 Phase 2(완료).
- **작업**:
  - [x] sessions/messages/runs 서비스·레포 + 라우터(run polling)
- **검증**: [x] 새 chat/기존 chat 흐름 상태 전이 (queued→running→terminal)

### Phase 2 — chat 스테이지 배선

- **Status**: DONE (PLAN-007-T-002, profile-be)
- **랜딩**: queued chat run이 `graph_rag_chat`를 실제 실행해 답변/evidence를 생성·저장하고 폴링이 결과를 반환하도록 배선. ④ `GraphRagChatContextBuilder`(신규 `services/ai/graph_rag_chat.py`, `HANDLER_KIND=graph_rag_chat`) — retriever evidence + 세션 이력 조립, 응답 파싱·저장, 근거 부족 시 `INSUFFICIENT_GRAPH_CONTEXT`로 표면화(단정 answer 없이 missing_context), 기존 세션 resume 배선. 신규 테스트 6 passed, 전체 회귀 pytest 239 passed(무회귀).
- **작업**:
  - [x] ④ context builder(retriever evidence + 세션 resume) + 응답 파싱·저장
  - [x] INSUFFICIENT_GRAPH_CONTEXT·실패 매핑
- **검증**: [x] evidence 기반 응답/근거 부족 케이스 (테스트 커버 + 라이브 e2e 완료 2026-07-09 — 채팅 전송 → 프론트→백→redis→AI worker(claude 실행)→백→폴링 전 구간 실연동, 실제 답변 생성 확인)

### Phase 3 — FE chat 패널

- **Status**: DONE (PLAN-007-T-003, profile-fe + PLAN-007-T-005 정합)
- **랜딩**: `/graph` 우측 채팅 패널 — 좌측 그래프(WP2)에 `[graph] | [채팅]` split view, 세션 목록/메시지/run polling(`isTerminalStatus`로 종료)·Evidence Block, 실패 표면(`page-graph.html` 시안·한국어 카피 기준). T-005에서 evidence 키 정합(`snippet`→`excerpt`, `link_reason`→`reason`, BE 필드명 일치)과 SPEC-006 U-3 "관련 구절 요약/연결 이유" 렌더 보강.
- **작업**:
  - [x] 세션 목록/메시지/polling UI + evidence 카드 ↔ 그래프 연동
- **검증**: [x] SPEC-006 UX AC (page-graph.html 시안), tsc/build 통과

## Pre-deploy Check

- [ ] chat이 문서/DB를 변경하지 않음 (조회 전용)
- [ ] 세션이 user-scoped로 격리됨

## Rollback

- 작업 레포 커밋 단위 revert.

## Done Criteria

- [x] 모든 Phase DONE/SUPERSEDED
- [x] SPEC-006 AC + SPEC-011 ④ AC 반영
- [x] product `log.md`·`30-work/README.md` 갱신

**라이브 e2e 완료(2026-07-09)**: Phase 1~3 코드·게이트(pytest 239·tsc/build) done에 더해, docker api 재빌드 + dev DB 재시드(max_turns 전역3/chat6) 후 브라우저 라이브 e2e를 admin이 확인 완료 — 채팅 전송 → **프론트 → 백엔드 → redis → AI worker(claude 실행) → 백엔드 → 폴링** 전 구간 실연동, 실제 답변 생성·evidence 렌더 확인. (open-kknaks는 `AXKG_REDIS_URL` broker 방식, worker는 task_type 무관 범용 실행기.)

## Open Issues

- 없음 (라이브 e2e 완료 2026-07-09).
