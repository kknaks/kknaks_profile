---
type: decision
id: AXKG-DEC-009
title: "회사 루트 문서 + 회사 context 층: 요구사항을 회사 하나로 묶는 앵커"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-21
updated_at: 2026-07-21
tags:
  - product/ax-knowledge-graph
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-002-enterprise-requirement-project-destination|AXKG-BL-002]]"
  decisions:
    - "[[decision-007-enterprise-project-destination-fanout|AXKG-DEC-007]]"
    - "[[decision-008-plan-then-fanout|AXKG-DEC-008]]"
  specs:
    - "[[spec-014-enterprise-project-fanout|AXKG-SPEC-014]]"
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
  works: []
  releases: []
  related: []
up:
  - identifying-relationship
  - data-modeling
---

# 회사 루트 문서 + 회사 context 층: 요구사항을 회사 하나로 묶는 앵커

회사 프로젝트에 **회사 루트 문서 `{corp}.md`(상위 개념/앵커)** 와 **회사 context 층 `context/`(조직·업무플로우 등 회사 배경지식)** 를 도입한다. 지금까지 회사 프로젝트는 `origin`·`baseline`(원본요약)·`spec`(기능정의서)만 있어 **요구사항을 회사 하나로 묶는 상위 개념이 없었다** — docx를 올릴 때마다 baseline이 따로 생겨 서로 안 묶였다. 회사 루트 문서를 앵커로 두고 모든 산출을 `up:` 체인으로 수렴시키며, project 분류를 **요구사항 vs 회사 context 2종으로 하위 분기**해 배경지식을 요구사항 팬아웃과 분리 저장한다. **AXKG-DEC-007의 팬아웃 결과 계약은 유지**하되 그 위에 회사 앵커 층을 얹는 확장이다.

## Context — 배경 (사용자 설계 2026-07-21)

현재 회사 프로젝트 팬아웃(AXKG-DEC-007 / AXKG-SPEC-014)은 `projects/{corp}/`에 `origin`(첨부 원본)·`baseline`(원본요약)·`spec`(기능정의서)만 둔다. 두 가지 공백이 있다:

1. **회사 앵커 부재**: 요구사항 docx를 여러 번 올리면 baseline(원본요약)이 매번 따로 생겨 **서로 묶이지 않는다.** "이 회사가 무엇인가"를 대표하는 안정적 상위 문서가 없어, 회사 단위 축적·탐색·상위개념 연결이 안 된다.
2. **회사 배경지식 저장처 부재**: 회사의 조직도(org)·휴가/업무 플로우(vacation_flow) 같은 **요구사항이 아닌 회사 배경(context)** 을 올리면, 지금은 요구사항 팬아웃(baseline+spec)으로 잘못 흘러간다. 배경지식과 요구사항은 성격이 달라 분리 저장·분리 표현이 필요하다.

이를 **회사 루트 문서 + 회사 context 층 + up: 회사 루트 체인**으로 해결한다.

> 이 결정은 AXKG-SPEC-014 외부 계약을 **확장**한다(pointer가 아니라 본문 정합) — 회사 프로젝트 구조에 `{corp}.md`와 `context/`가 추가되고, project 분류가 요구/context로 하위 분기된다. 팬아웃 결과 계약(원본요약 + 기능정의서 N, main+derived, origin·경로) 자체는 유지된다.

## Decision

### 1. 회사 루트 문서 `{corp}.md` = 회사의 상위 개념/앵커

- **결정**: "프로젝트 추가" 시 사용자가 회사 **간략 정보**(회사명·도메인·한 줄 소개 등)를 입력하면 `projects/{corp}/{corp}.md`(예: `projects/sc/sc.md`)로 **회사 루트 문서**를 생성한다. **회사당 1개, 안정적**(요구 docx가 늘어도 변하지 않는 앵커). document_type은 회사 루트를 나타내는 **신규 `company` 타입**으로 두는 것을 기본으로 하며(그래프 앵커 노드로서 up-target 허브 역할이 일반 `permanent`(전역 `permanent/` 종합 노트)와 경로·의미가 다르기 때문), 정확한 타입 확정(신규 enum vs `permanent` 재사용·마이그레이션)은 구현 OQ로 둔다.
- **근거(왜)**: 요구사항에 회사 앵커가 없어 docx마다 baseline이 고립됐다. 회사당 1개의 안정적 루트를 두면 모든 산출(baseline·spec·context)이 그 루트로 수렴해 **회사 단위 축적·탐색·상위개념 연결**이 가능해진다. "프로젝트 추가"는 이미 회사 경계를 사람이 명시적으로 만드는 지점이라(AXKG-DEC-007 D2), 그 시점에 간략정보를 받아 루트를 만드는 게 자연스럽다.
- **영향**: "프로젝트 추가" 폼이 빈 스캐폴드 생성에서 **회사 간략정보 입력 + `{corp}.md` 생성**으로 확장된다(AXKG-SPEC-014 UX). 회사 루트는 origin과 달리 **그래프 노드**다(up-target 허브). 이 루트가 아래 Decision 3의 `up:` 수렴 대상이 된다.

### 2. project destination 하위 분기 — 요구사항 vs 회사 context

- **결정**: inbox 업로드(intake 메모에 **회사명 + 성격 힌트**, 예: "SC 회사 정보야") → 요약①/분류가 **메모 + 내용으로 "요구사항이냐 회사 배경(context)이냐"를 판단**한다. PARA `project` destination 안에서:
  - **요구사항** → 기존 v2 팬아웃(baseline 원본요약 + spec 기능정의서 N, AXKG-DEC-007 / AXKG-DEC-008 plan-then-fanout).
  - **회사 context** → `projects/{corp}/context/{문서}.md`(조직 org·업무플로우 vacation_flow 등 회사 배경지식) 단일 문서(팬아웃하지 않음).
- **근거(왜)**: 분류 AI는 이미 PARA 4종(project/area/resource/archive)을 가르므로, **project 내부의 요구/context 2종 구분은 실현 가능**하다(요약 단계 판단으로 충분). 배경지식(org·flow)과 요구사항(기능)은 성격이 달라 — 배경은 기능으로 쪼갤 대상이 아니라 회사를 이해하는 참고자료다 — 팬아웃 대상에서 빼고 `context/`에 별도 저장해야 표현·탐색이 맞는다. **메모의 성격 힌트를 우선 신호**로 쓰고, 힌트가 없으면 내용으로 판단한다.
- **영향**: 분류/요약 단계에 **project 하위 sub-type 판정(requirement | context)** 이 추가된다. 경로에 `projects/{corp}/context/` 층이 생긴다. context 산출은 요약① 수준의 단일 문서 생성(요구사항처럼 기능 팬아웃하지 않음)이며, 판단 모호 시 폴백은 OQ로 둔다.

### 3. up: 회사 루트 체인 — 모든 산출이 회사 루트로 수렴

- **결정**: 회사 프로젝트 내 모든 산출이 회사 루트로 수렴하도록 `up:`을 배선한다:
  - `baseline`(원본요약)·`context` 문서 → `up: [{corp}]`(회사 루트 stem).
  - `spec`(기능정의서) → `up: [원본요약]`(자신을 낳은 baseline) — baseline이 다시 `up: [{corp}]`이므로 **spec→원본요약→{corp}** 2단 체인으로 회사 루트에 수렴한다.
  문서 생성 시 시스템은 corp을 이미 알고 있으므로(corp 바인딩, AXKG-SPEC-014), **회사 루트 stem을 주입해 `up:` frontmatter + 본문 `[[{corp}]]` 링크를 자동 생성**한다(그래프 엣지의 단일 소스는 본문 `[[ ]]`, AXKG-SPEC-005).
- **근거(왜)**: `up:` 체인이 회사 루트로 수렴하면 그래프에서 **회사 단위로 묶여** 탐색·상위개념 연결이 된다. spec→원본요약→{corp} 2단 체인은 기존 baseline↔spec 관계(spec은 자기 baseline 소속, AXKG-SPEC-014 §4 `## 기능 목록` 링크)를 유지하면서 전이적으로 회사 루트까지 도달한다 — 기존 링크 계약을 깨지 않고 앵커만 추가한다.
- **영향**: 문서 생성(요약/팬아웃/context) 시 corp stem 주입 배선이 필요하다. 회사 루트 문서 자체는 프로젝트 최상위 앵커라 `up:`이 없거나 전역 앵커만 가진다. 링크 계약 세부는 AXKG-SPEC-005, 주입 위치는 후속 work(AXKG-WORK-013).

### 4. origin 양쪽 보관 — 요구든 context든 원본 raw 유지

- **결정**: 업로드된 docx가 요구사항이든 회사 context든 **첨부 원본은 `projects/{corp}/origin/`에 손대지 않은 raw로 보관**한다(AXKG-DEC-007 D8 유지). 분기(requirement/context)와 무관하게 원본 보관은 동일하다.
- **근거(왜)**: origin은 감사·역참조·재요약용 원본이며(그래프 노드 아님, AXKG-DEC-007 D8), 요구/context 어느 쪽이든 "회사가 준 원본"이라는 성격은 같다. 분기와 무관하게 일관 보관하는 것이 단순하고 안전하다.
- **영향**: origin 보관 로직은 sub-type 분기 이전(intake/staging)에서 공통으로 동작한다 — 변경 없음, 재확인.

## Consequences

- **AXKG-SPEC-014 확장(본문 정합)**: 회사 프로젝트 구조에 `{corp}.md`(회사 루트) + `context/` 층이 추가되고, project 분류가 요구/context로 하위 분기되며, 모든 산출이 `up: {corp}` 체인으로 수렴한다. 구조 트리·UX("프로젝트 추가" 간략정보 입력)·Data Contract·Flow·Scope를 이 결정에 맞춰 갱신한다(pointer가 아니라 외부 계약 본문 확장). 단, 팬아웃 결과 계약(원본요약 + 기능정의서 N, main+derived, origin·경로 컨벤션)은 불변이다.
- **코드 영향(코드레포 소관)**:
  - **분류/요약**: project 하위 sub-type 판정(requirement | context) — 분류 프롬프트/라우팅에 메모 성격 힌트 + 내용 판단 추가.
  - **경로**: `projects/{corp}/context/` 디렉토리 매핑, context document_type 산출.
  - **"프로젝트 추가"**: 회사 간략정보 입력 폼 + `{corp}.md` 생성(BE 스캐폴드 + FE 폼).
  - **up: 배선**: 문서 생성 시 corp 루트 stem 주입 → `up:` frontmatter + 본문 `[[{corp}]]` 자동 생성(요약/팬아웃/context 생성 경로 공통).
  - **기존 baseline/spec**: `up:`을 회사 루트 체인으로 정합(spec→원본요약→{corp}).
- **후속 구현은 AXKG-WORK-013**(회사 루트 + context)으로 발주한다. 생성 메커니즘은 AXKG-DEC-008(plan-then-fanout)과 정합한다(요구사항 팬아웃 경로는 그대로).

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[identifying-relationship]] — 회사 루트 `{corp}.md` 를 앵커로 두고 **모든 산출이 `up:` 으로 수렴**한다. 부모 없이는 고립되던 baseline 들에 식별 부모를 준 것이다
- [[data-modeling]] — 요구사항과 회사 context 를 **다른 것으로 가른** 분기. 같은 destination 안에서 성격이 다른 둘을 나눠 저장한다

## Open Questions

- **회사 루트/context document_type 확정**: 회사 루트를 신규 `company` 타입으로 둘지 `permanent` 재사용할지, context 문서를 신규 `context` 타입으로 둘지 `reference`/`permanent` 재사용할지 — 그래프 노드 처리·enum/마이그레이션·경로 컨벤션 정합을 보고 구현 시 확정한다(이 결정은 신규 `company`/`context` 방향을 기본으로 둔다).
- **요구/context 판단 모호 시 폴백**: 메모 힌트가 없고 내용으로도 애매할 때 — 기본을 요구사항(팬아웃)으로 둘지 context로 둘지, 혹은 사용자 확인을 물을지. 오분류 비용(context를 기능으로 쪼개면 노이즈 / 요구를 context로 두면 팬아웃 누락)을 보고 후속에서 확정.
- **context 문서의 dedup(누적) 여부**: 같은 성격 context(예: org)가 다른 docx로 또 들어올 때 — 기존 context 문서에 통합·보강할지, 별개 문서로 둘지. 요구사항 dedup(AXKG-DEC-007 D4)과 같은 정책을 적용할지 후속에서 확정.
