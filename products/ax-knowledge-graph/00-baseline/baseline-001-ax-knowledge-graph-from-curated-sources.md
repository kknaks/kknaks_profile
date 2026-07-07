---
type: baseline
id: AXKG-BL-001
title: "AX 관련 자료를 수집해 지식그래프로 구축하기"
status: accepted
product: ax-knowledge-graph
source:
  type: idea
  ref: "inbox/2026-07-07-ax-knowledge-graph-from-curated-sources.md"
links:
  baselines: []
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
    - "[[spec-002-approval-gate-feedback-loop|AXKG-SPEC-002]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-007-ai-provider-settings|AXKG-SPEC-007]]"
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
    - "[[spec-009-prompt-dynamic-management|AXKG-SPEC-009]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works: []
  releases: []
  related: []
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/baseline
  - status/accepted
---

# AX 관련 자료를 수집해 지식그래프로 구축하기

AX 관련 기사, 유튜브, 링크를 모아 개념·사례·도구를 노드로 만들고 관계를 엣지로 연결한 지식그래프를 구축한다.

> 이 baseline은 Slack에서 들어온 원본 아이디어를 제품화하기 위한 첫 입력이다. 아직 제품 결정은 확정하지 않고 문제, 기대효과, 열린 질문을 보존한다.

## Raw

간단한 아이디어인데 ax관련 기사, 유투브, 링크들을 모아서 지식그래프로 만들기

## Context

AX 관련 정보가 기사, 영상, 링크 형태로 분산되어 있다. 현재 상태에서는 자료를 저장해도 개념 간 연결, 사례 간 패턴, 도구의 포지션을 보기 어렵다.

## Why It Matters

- 자료 간 관계가 보이면 학습과 재탐색 비용이 줄어든다.
- 글쓰기, 의사결정, 새 자료 분류에 재사용 가능한 구조화 지식 베이스가 생긴다.
- 단순 북마크가 아니라 지식의 연결 구조를 제품 경험으로 만들 수 있다.

## Possible Direction

- AX의 의미를 먼저 좁힌다: Agent Experience, AI Transformation, 또는 별도 정의.
- 초기 수집은 수동 북마크와 링크 입력으로 시작하고, RSS·Slack·브라우저 확장은 이후 자동화로 분리한다.
- 노드 타입은 최소한 `source`, `concept`, `case`, `tool`, `person`, `organization`으로 시작한다.
- MVP는 "자료 입력 -> 요약/태깅 -> 관계 추천 -> 그래프 탐색" 흐름으로 잡는다.
