---
type: decision
id: AXKG-DEC-001
title: "PARA 기반 수집-분류-연결-문서화 파이프라인과 승인 게이트"
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
  decisions: []
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
    - "[[spec-002-approval-gate-feedback-loop|AXKG-SPEC-002]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-007-ai-provider-settings|AXKG-SPEC-007]]"
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# PARA 기반 수집-분류-연결-문서화 파이프라인과 승인 게이트

AX 관련 자료를 AI가 탐색·정리하되, 분류와 연결은 사용자가 승인하는 게이트를 통과한 뒤 영구 문서로 편입한다.

> 이 제품은 자동 수집기가 아니라 "AI가 제안하고 사람이 승인하는 지식 운영 시스템"이다. 레포의 PARA 흐름처럼 날것 입력을 프로젝트/영역/리소스/아카이브 성격에 맞게 분류하고, 승인된 결과만 영구 문서화한다.

## Context

- 관련 baseline: AXKG-BL-001
- 문제/기회: 링크, 문서, 영상이 쌓여도 분류와 연결 근거가 없으면 재사용 가능한 지식그래프가 되지 않는다.
- 결정이 필요한 이유: AI 자동화 범위와 사람 승인 지점을 먼저 고정해야 MVP spec이 흔들리지 않는다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | AI가 수집부터 문서화까지 자동 처리 | 처리량이 높다 | 잘못된 분류와 연결이 누적된다 | 초기 제품에는 부적합 |
| B | AI가 제안하고 사용자가 승인한 결과만 반영 | 신뢰성과 편집 가능성이 높다 | 승인 UI와 재생성 로직이 필요하다 | 채택 |
| C | 사용자가 직접 작성하고 AI는 보조만 담당 | 통제력이 높다 | 제품 가치가 약하다 | 기각 |

## Decision

- 채택: `자동 요약 -> 분류 게이트 -> 문서화 승인 게이트 -> 영구 문서화` 파이프라인(2-게이트).
- 채택: AI는 2-stage로 나눈다. **① 요약 AI** — source가 `received`가 되면 사람이 "수집 시작"을 누르지 않아도 **자동으로** 실행되어 제목·요약·키워드·자료 유형을 만든다(`received → summarizing → summarized`, 실패 시 `collection_failed` 재시도). **② 분류기 AI** — `summarized` 항목을 분류 게이트로 보내는 행위가 트리거이며, **PARA 분류만** 생성한다.
- 채택: **2-게이트 구조**. **① 분류 게이트**(②, AXKG-SPEC-001) = PARA 분류만. **② 문서화 승인 게이트**(③, AXKG-SPEC-004) = destination별 AI 초안(frontmatter + 본문 + `up:`/`[[ ]]` 연결) + 파생지식 후보. 요약·분류 카드는 한 카드로 병합하고, 문서화 게이트는 분류 게이트 바로 아래 인라인으로 연다(우측 사이드바 없음).
- 채택: **연결(connection)은 별도 게이트가 아니다.** 문서화 게이트 AI 초안의 `up:`/`[[ ]]`와 파생지식 후보로 흡수한다. 초안 승인 시 그래프 연결로 반영한다.
- 채택: **`resource ≡ reference`.** `resource`는 PARA 분류 라벨, `reference note`는 그 산출 노트 타입으로 같은 대상의 두 이름이다. 문서화 게이트는 destination-agnostic이며 매핑은 `resource→reference note`, `area→permanent note`, `project→product 문서`, `archive→문서화 중단`.
- 채택: 게이트 대상은 `summarized` source뿐이다. inbox에 쌓인 미요약 항목은 분류 게이트로 보낼 수 없다.
- 채택: 두 게이트 모두 버전 관리한다. 피드백 시 새 버전(v2)을 생성하고 직전 버전(v1)은 read-only(버튼 비활성, archive 보존)로 둔다.
- 채택: PARA 노트법을 적용한다. 입력 자료는 우선 source로 보존하고, 승인 후 Project, Area, Resource, Archive 성격에 맞는 영구 문서로 편입한다.
- 기각: 요약을 사람이 수동으로 "수집 시작"해서 트리거하는 방식.
- 기각: 분류와 연결을 하나로 합친 단일 병합 게이트(연결 후보 토글). 연결은 게이트가 아니라 문서화 초안에서 발현한다.
- 기각: 연결을 별도 승인 게이트로 두는 방식.
- 기각: reference를 전용 사이드바 개념으로 두는 방식. reference는 resource destination의 한 경우이고 문서화 게이트는 인라인이다.
- 기각: AI가 임의로 영구 문서를 바로 수정하는 방식.
- 채택: Graph Chat은 MVP에 포함하고, Graph RAG 검색은 PostgreSQL graph cache와 Markdown link graph를 사용한다.
- 채택: 그래프 시각화는 기존 `kknaks_profile`의 `/graph` 구현을 참고해 AX 제품에 맞게 새로 구현한다.

## Rationale

- 판단 기준: 지식 베이스의 정합성, 사용자의 편집 통제권, 이후 문서 재사용 가능성, 입력 처리 마찰 최소화.
- 대안 대비 이유: AX 자료는 개념·도구·사례의 해석이 중요해서 AI의 첫 판단을 바로 SoT로 삼으면 위험하다. 따라서 요약은 자동화해 마찰을 줄이되, 지식그래프 편입(분류·연결)에는 사람 승인을 유지한다.
- 2-게이트 이유: 분류 판단과 문서화(초안·연결) 판단은 성격이 다른 결정이다. 분류 게이트는 "이 자료가 무엇인가"(PARA), 문서화 게이트는 "어떤 문서로 어떻게 연결해 남길 것인가"를 다룬다. 연결을 별도 게이트로 두는 대신 문서화 초안의 `up:`/`[[ ]]`로 흡수하면, 사람은 완성된 문서 초안을 보며 연결까지 한 번에 검토·승인할 수 있다. 두 게이트 모두 인라인 세로 스택으로 두어 사이드바 왕복을 없앤다.
- 리스크: 요약 자동화로 품질 낮은 요약이 게이트 대상에 섞일 수 있다. `collection_failed` 재시도와 게이트에서의 피드백·재생성으로 보정한다. bulk approve는 후속으로 둔다.

## Scope

이번 spec에 반영할 범위.

- In:
  - 링크, 문서, 영상 URL 입력
  - `received` 시 자동 요약(① 요약 AI)과 요약 결과 생성
  - 분류 게이트(② 분류기 AI: PARA 분류만)
  - 문서화 승인 게이트(③: destination별 AI 초안 + `up:`/`[[ ]]` 연결 + 파생지식, 연결은 초안에 흡수)
  - 두 게이트 공통 피드백 기반 재생성(v2, v1 read-only)
  - 승인 결과의 영구 문서화와 그래프 연결 반영
- Out:
  - 브라우저 확장, RSS, Slack bot 자동 수집
  - 복수 사용자 권한 모델
  - 자동 publish
  - 별도 그래프 DB 제품 선택
  - 기존 `/graph` 구현을 참고한 AX 제품 그래프 UI 구현
- 영향을 받는 spec 후보:
  - AXKG-SPEC-003 source inbox
  - AXKG-SPEC-001 curation pipeline
  - AXKG-SPEC-002 approval gate feedback loop
  - AXKG-SPEC-004 documentation approval gate
  - AXKG-SPEC-005 document link graph contract
  - AXKG-SPEC-006 graph chat
  - AXKG-SPEC-007 AI provider settings
  - AXKG-SPEC-008 simple token auth

## Resolved Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-001 | AX를 Agent Experience로 정의할지 AI Transformation까지 포함할지 | PM | AXKG-DEC-004에서 AI Transformation 중심으로 확정 |
| OQ-002 | 영구 문서 저장소를 파일 기반으로 시작할지 DB 기반으로 시작할지 | BE | AXKG-DEC-002에서 Markdown SoT + PostgreSQL로 확정 |
| OQ-003 | 그래프 탐색 UI를 MVP에 포함할지 | Product | AXKG-DEC-003에서 Graph RAG Chat MVP 포함으로 확정 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| AXKG-SPEC-003 | create | Slack URL이 처음 들어오는 raw source queue |
| AXKG-SPEC-001 | create | 수집-분류-연결-문서화 end-to-end 흐름 |
| AXKG-SPEC-002 | create | 승인 게이트, 피드백, 재생성 정책 |
| AXKG-SPEC-004 | create | 문서화 승인 게이트: destination별 AI 초안과 파생지식 |
| AXKG-SPEC-005 | create | Obsidian과 제품 페이지가 공유하는 문서 링크/그래프 계약 |
| AXKG-SPEC-006 | create | 그래프 탐색 화면과 그래프 기반 질의응답 |
| AXKG-SPEC-007 | create | open-kknaks 내부 AI 실행 설정과 Claude/Codex provider 선택 |
| AXKG-SPEC-008 | create | MVP seed user와 브라우저 저장 token 기반 로그인 |
