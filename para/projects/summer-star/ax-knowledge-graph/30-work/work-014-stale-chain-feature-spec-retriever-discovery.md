---
type: work
id: AXKG-WORK-014
title: "WP14: stale 연쇄 확장 — feature_spec 대상 + 신규 개념 retriever 발굴 축"
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
created_at: 2026-07-25
updated_at: 2026-07-25
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-002-enterprise-requirement-project-destination|AXKG-BL-002]]"
  decisions:
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
  specs:
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
  works:
    - "[[work-012-plan-then-fanout|AXKG-WORK-012]]"
    - "[[work-013-company-root-and-context|AXKG-WORK-013]]"
  releases: []
  related: []
---

# WP14: stale 연쇄 확장 — feature_spec 대상 + 신규 개념 retriever 발굴 축

concept stale 연쇄(AXKG-SPEC-004 §E, AXKG-DEC-005 E)를 두 축으로 확장한다.

1. **대상 확장(E-9)**: stale 마킹·재생성 대상을 종합 노트(permanent)에서 **회사 기능정의서(feature_spec)** 까지 넓힌다.
2. **감지 축 확장(E-8)**: 기존 backlink 감지(이미 링크한 문서만)가 못 잡는 **신규 개념 인입**을, 그 개념을 쿼리로 한 **retriever 발굴**(qmd 하이브리드)로 관련 문서를 찾아 배지를 붙인다.

## 배경 (왜)

- 기능정의서의 `## 8. 연결`은 현재 회사 원본요약 1 + 기술 개념 0~1개로 **연결이 빈약**하다. 기술 개념(permanent/concepts)이 후보에는 다 주어지는데도, 생성 시점 템플릿·프롬프트가 "역량 차용 1개(해당 시)"로 몰고 후보에 본문 스니펫이 없어 제목이 안 겹치면 스킵되기 때문이다.
- 더 근본적으로, **스펙이 생성된 뒤 새 기술 개념(예: `음성-인식-stt`)이 들어와도 기존 스펙(예: 회의록 검색)에 소급 연결되지 않는다**. permanent 종합 노트는 구성 개념이 자랄 때 stale→재생성으로 갱신되지만(§E 구현 완료), 그 파이프라인은 세 겹으로 feature_spec을 배제한다:
  - 트리거가 `supplement_existing_concept`(기존 개념 성장)뿐 — 신규 create는 트리거 없음.
  - 감지가 backlink 기반 — 아직 링크 안 한 스펙은 원천적으로 미감지.
  - 대상·재생성 게이트가 `permanent`로 하드 한정(`document_type != "permanent"` → `not_permanent` 리젝트).

## 설계 (SSOT: AXKG-SPEC-004 §E, E-8/E-9)

- **재생성 프리미티브 재사용**: feature_spec은 producing 문서화 게이트가 없으므로(plan-then-fanout 산출), 기능 dedup의 `supplement_existing_feature`(기존 기능정의서 전문 주입 + 병합·업그레이드 overwrite)를 재생성 경로로 재사용한다.
- **발굴 범위**: corp 경계 + relevance score 임계 + top-N 상한(임계·N은 구현 상수)로 과잉 포함 억제. LLM triage(E-7) 아님.
- **반영 방식**: 배지 → 수동 승인(E-1/E-3~E-6 상속). 자동 연쇄 재작성 없음.
- **백필**: E-8 배포 이전 인입된 기존 concept 전수에 발굴 트리거를 1회 소급 실행(멱등).

## 작업 항목 (코드 레포 ax-graph)

- **T-014-1** 사전 검증 — `document_stale_marks` 테이블/`list_stale`/배지 라우트의 permanent 가정 여부(마이그레이션 필요성 판정).
- **T-014-2** 트리거 — `apply_executor`에 신규 개념 발굴 마킹(`_mark_stale_from_new_concepts`) 추가 + 기존 supplement 마킹 대상 필터 `permanent`→`{permanent, feature_spec}` 확장.
- **T-014-3** 재생성 진입점 — `gates.open_stale_regeneration` 타입 분기(permanent=기존 경로 / feature_spec=`supplement_existing_feature` 큐잉). `feature_spec` context builder `_supplement_block` stale 변형 + `documentation_gate` stale 블록 대응.
- **T-014-4** 백필 스크립트 — 기존 concept 소급 발굴(`backfill_company_root` 앱-컨텍스트 CLI 패턴). `음성-인식-stt`로 회의록 스펙 stale 라이브 검증.
- **T-014-5** 테스트 — create 발굴 마킹(corp 경계·임계) + feature_spec 재생성이 `## 8. 연결`에 개념 링크 추가.

## Meta

- 생성 시점 연결 빈약(템플릿·프롬프트·후보 스니펫)은 **별개 축**으로, feature_spec 템플릿(`project_feature_spec`)·`generate_feature_spec` 프롬프트·`feature_spec` context builder 개선으로 병행 가능(본 WP 범위 밖, 후속 정리).
