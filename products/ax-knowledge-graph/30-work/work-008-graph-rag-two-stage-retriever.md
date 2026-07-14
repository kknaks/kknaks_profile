---
type: work
id: AXKG-WORK-008
title: "WP7: Graph RAG 2단 retriever (qmd 사이드카)"
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
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/todo
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
    - "[[work-005-graph-chat|AXKG-WORK-005]]"
  releases: []
  related: []
---

# WP7: Graph RAG 2단 retriever (qmd 사이드카)

Graph RAG retriever를 `keyword score + edge distance` 단일 스캔에서 **2단 구조**로 전환한다 — 1단 후보 발굴은 qmd 사이드카 하이브리드 검색, 2단 그래프 확장은 자체 wikilink 탐색. retriever는 채팅④과 문서화③가 공유하는 컴포넌트이므로(AXKG-SPEC-011) 두 스테이지 모두에 동일하게 적용된다. 기존 keyword+edge 경로는 삭제하지 않고 qmd 장애 시 graceful fallback으로 강등해 유지한다. BE 단독.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-006(retriever 2단 재설계 절 §1·§5), AXKG-SPEC-011(retriever 공유 컴포넌트·`RETRIEVER_FALLBACK_USED` 폴백 매핑)
- Covers decision: AXKG-DEC-003(2026-07-14 개정 — qmd 사이드카·2단 retriever·리랭크 토글·인덱싱 시점·graceful fallback)
- Depends on work: AXKG-WORK-003(WP2 — 그래프 코어·현행 keyword+edge retriever), AXKG-WORK-005(WP4 — chat④ 실행 경로)
- Parallel work: AXKG-WORK-009(WP8), AXKG-WORK-010(WP9)
- Follow-up work: 없음 (튜닝 숫자·qmd 통합 형태는 구현 기본값으로 시작, 관찰 후 조정 — AXKG-SPEC-011 §7 OQ)
- External dependency: qmd 사이드카(github.com/tobi/qmd — 로컬 마크다운 검색엔진, BM25+로컬 embedding 벡터검색 RRF 융합+LLM 리랭크, SQLite 인덱스, CLI/MCP)

## Scope

포함:

- qmd 사이드카 통합(docker 배선 포함)과 장애 감지
- 1단 후보 발굴: qmd 하이브리드 검색(BM25 + 벡터 RRF), 리랭크 설정 토글(기본 on — 설정 표면 소유는 AXKG-SPEC-007)
- 2단 그래프 확장: qmd top-K 시드로 wikilink 그래프 탐색(edge 타입별 가중치·hop 감쇠·다중 시드 점수 합산·선택 노드 neighborhood 우선), 근거 경로(`used_paths`·`evidence_edges`) 산출 강화
- keyword+edge graceful fallback(qmd 장애 시 자동 강등, `RETRIEVER_FALLBACK_USED` 관찰 기록)
- 문서 쓰기/확정 시점 증분 인덱싱(채팅 요청 경로에 인덱싱 비용 0)
- 채팅④·문서화③ 공유 컴포넌트(`domain.graph`)에 동일 적용

제외:

- pgvector/embedding 자체 구현 (embedding은 qmd 사이드카가 담당, pgvector 계속 파킹 — AXKG-DEC-003)
- retriever 튜닝 숫자·qmd 통합 형태(subprocess CLI vs MCP)·클래스/파일 경로 (구현 기본값·OQ, AXKG-SPEC-011 §7)
- chat/문서화 게이트의 UX·응답 표면 (AXKG-SPEC-006/004 소관, 이 WP는 검색 계약만)

## Progress Checklist

코드 발주 단위(C-item). 계약·스펙 참조 수준까지만 — 클래스/파일 경로·튜닝 숫자는 발주 시 구현 기본값으로 확정한다.

- [x] **C-1 qmd 사이드카 통합** — qmd 사이드카 docker 배선(서비스 기동)과 장애 감지 경로. (AXKG-DEC-003 개정) — `apps/qmd/Dockerfile`+`entrypoint.sh`(공식 이미지 없어 node:22 위 빌드, embed 모델 pre-bake), dev·prod compose에 `qmd` 서비스+`qmd-index` 볼륨(인덱스 영속). 장애 감지=`QmdUnavailable`→폴백. **통합 형태=HTTP MCP 사이드카**(subprocess CLI는 재로드로 186s/쿼리, 실측). ::1 바인딩은 socat 브리지로 우회.
- [x] **C-2 증분 인덱싱** — 문서 쓰기/확정 시점에 qmd 인덱스를 증분 갱신하고, 채팅 요청 경로에서는 인덱싱하지 않는다. (AXKG-SPEC-006 §5, AXKG-DEC-003) — 사이드카 entrypoint가 주기적 `qmd update`(변경분만)+`qmd embed`를 백그라운드로 수행(요청 경로 인덱싱 비용 0). qmd MCP가 index 툴을 노출하지 않아 api-트리거 대신 사이드카 소유 증분 재인덱싱 채택.
- [x] **C-3 1단 후보 발굴** — qmd 하이브리드 검색(BM25+벡터 RRF)으로 질문 관련 top-K 후보, 리랭크 토글(기본 on). 리랭크 설정 표면은 AXKG-SPEC-007 소관(참조만). (AXKG-SPEC-006 §5, AXKG-SPEC-011) — MCP `query`(명시적 lex+vec searches, top_k=12). **리랭크 기본 off로 확정**(OQ): CPU-only에서 LLM 리랭크 60s+(실측), qmd 문서도 CPU는 off 권장. `AXKG_QMD_RERANK_DEFAULT` 설정(SPEC-007 표면)으로 GPU 배포 시 on.
- [x] **C-4 2단 그래프 확장** — top-K 시드 wikilink 탐색: edge 타입 가중치·hop 감쇠·다중 시드 점수 합산·선택 노드 우선, `used_paths`·`evidence_edges` 근거 경로 산출 강화. (AXKG-SPEC-006 §5) — `GraphService._retrieve_two_stage`. 기본값(OQ): edge weight lineage=1.5/assoc=1.0, hop_decay=0.5^hop, max_hop=2, seed_base=10.
- [x] **C-5 graceful fallback** — qmd 사이드카 장애 시 1단을 `keyword score + edge distance`로 자동 폴백(2단 그래프 확장은 유지), `RETRIEVER_FALLBACK_USED`를 `ai_tasks.payload`에 관찰 기록(품질 강등·사용자 실패 아님). (AXKG-SPEC-011 Case Matrix) — 기존 keyword+edge 경로 보존(폴백 강등), pipeline이 빌더 플래그를 `payload["fallbacks"]`로 수집.
- [x] **C-6 공유 컴포넌트 적용** — 2단 retriever를 채팅④과 문서화③(연결 후보 발굴, `domain.graph`)에 동일하게 적용. (AXKG-SPEC-011 Connection Candidate Context) — 두 소비처 모두 `GraphService.retrieve()`를 호출하므로 retrieve() 2단 전환이 자동 적용. 두 execution 서비스가 settings로 qmd 클라이언트를 주입.

## Verification

- [x] AXKG-SPEC-006 §5 retriever 2단 재설계 계약 반영(1단 qmd 하이브리드·2단 그래프 확장·리랭크 토글·인덱싱 시점·폴백)
- [x] AXKG-SPEC-011 `RETRIEVER_FALLBACK_USED` 매핑과 공유 컴포넌트(③④) 동일 적용 반영
- [x] qmd 장애를 주입해도 keyword+edge 폴백으로 답변이 성립하고 폴백 사실이 관찰 기록된다 — `test_graph_two_stage_retriever`(폴백 케이스)+`test_ai_pipeline`(payload 기록) pytest 통과
- [x] 채팅 요청 경로에 인덱싱 비용이 없다(인덱싱은 문서 쓰기/확정 시점) — 인덱싱은 사이드카 소유(주기적 `qmd update`), api retrieve()는 검색만 호출

## Rollback

- 작업 레포 커밋 단위 revert. qmd 사이드카 미기동/제거 시 keyword+edge 폴백 경로로 계속 동작.

## Change Log

| Date | Change |
|---|---|
| 2026-07-14 | work-add. PLAN-013-T-005 WP 분해로 신규 작성(todo). AXKG-DEC-003 개정·AXKG-SPEC-006/011 T-001 산출분 기준. |
| 2026-07-14 | PLAN-013-T-006(profile-be) C-1~C-6 구현. C-1 스모크 실측(rerank off 하이브리드 0.3s vs CLI 186s)로 통합 형태=HTTP MCP 사이드카·리랭크 기본 off 확정. 2단 retriever(`GraphService`)+qmd 클라이언트(`services/qmd.py`)+graceful fallback+`RETRIEVER_FALLBACK_USED` 배선, dev·prod compose에 qmd 사이드카. ax-graph pytest 403 통과(신규 20). |
