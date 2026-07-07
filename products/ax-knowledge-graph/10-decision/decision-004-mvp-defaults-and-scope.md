---
type: decision
id: AXKG-DEC-004
title: "MVP 기본값과 남은 범위 결정"
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
  specs:
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
    - "[[spec-002-approval-gate-feedback-loop|AXKG-SPEC-002]]"
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-007-ai-provider-settings|AXKG-SPEC-007]]"
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
    - "[[spec-009-prompt-dynamic-management|AXKG-SPEC-009]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
  works: []
  releases: []
  related: []
---

# MVP 기본값과 남은 범위 결정

남은 open question은 추천안으로 닫고 MVP 구현 기본값으로 사용한다.

## Decision

- AX 범위는 MVP에서 `AI Transformation` 중심으로 정의한다.
- 수집 방식은 Slack URL 수신과 제품 페이지 직접 URL 입력으로 시작한다.
- RSS, 브라우저 확장, 자동 크롤링은 MVP 이후로 둔다.
- Slack event는 원문 전체를 장기 보존하지 않고 URL, channel, user, timestamp, text snippet, metadata만 저장한다.
- 피드백 UI는 빠른 선택지와 자유 입력을 함께 제공한다.
- reference note 양식은 별도 template directory를 만들지 않고 문서 링크/frontmatter spec에 포함한다.
- provider별 기본 model preset은 MVP에서 두지 않는다. `provider=claude`만 기본값으로 두고 model은 비워둔다.
- auth token은 MVP에서 `localStorage`에 저장한다.
- 그래프 시각화는 기존 `kknaks_profile`의 `/graph` 구현을 참고해 AX 제품에 맞게 새로 구현한다.
- 참고 구현의 기반은 `app/front/app/graph`, `app/front/components/graph/*`, `react-force-graph-2d`, `d3-force`다.

## Rationale

- MVP는 수집-승인-문서화-Graph RAG 흐름을 먼저 검증해야 한다.
- 자동 수집 채널과 보안 강화는 제품 흐름이 검증된 뒤 확장하는 편이 비용 대비 효율적이다.
- 문서 양식은 파일 기반 SoT와 Obsidian 호환을 우선하므로, 별도 template directory보다 spec contract로 관리한다.

## Open Questions

없음. 배포 환경별 bind mount host path는 배포 단계 결정으로 남긴다.
