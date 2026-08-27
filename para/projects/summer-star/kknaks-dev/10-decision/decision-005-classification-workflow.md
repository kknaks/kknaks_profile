---
type: decision
id: KDEV-DEC-005
title: "분류 워크플로 — SSOT는 종착지 (승격/이동 아님)"
status: accepted
product: kknaks-dev
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
    - "[[decision-004-edge-model-and-schema|KDEV-DEC-004]]"
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
  specs:
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
  works: []
  releases: []
  related: []
up:
  - db-normalization
---

# 분류 워크플로 — SSOT는 종착지 (ADR-005)

아이디어가 성격에 따라 독립 SSOT(permanent / product / post)로 *분류*된다. permanent와 product/post는 평행한 독립 SSOT이며, 한쪽이 다른 쪽으로 흘러가지 않는다.

> **개정 (2026-07-27) — [[decision-011-approval-gate-chain|KDEV-DEC-011]] / [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]**
>
> 아래 두 조항을 개정한다. 나머지(평행 독립 SSOT, `up:`은 인용, idea 휘발, 분류=배치)는 **그대로 유효**하다.
>
> **① 정제 주체** — 종전 *"정제 주체 = 사람. 에이전트는 inbox 정리·연결 후보 제안까지만 보조"* 및 기각 항목 *"정제를 에이전트가 초안까지 하는 안(제텔 정신상 연결=본인 사고)"* → **AI가 초안을 만들고 사람이 승인 게이트에서 판단하는 모델로 전환**한다.
> 기각 당시의 우려("연결은 본인 사고여야 한다")는 **승인 게이트가 흡수**한다 — AI는 제안만 하고 파일·git을 직접 건드리지 못하며([[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D2), 어떤 개념을 만들지·기존 개념에 합칠지·어느 목적지에 둘지는 전부 사람이 게이트에서 결정한다. 연결 판단의 주체는 여전히 사람이고, 바뀐 것은 **초안 타이핑을 누가 하느냐**다.
> 반대로 게이트가 없으면 이 기각의 우려가 그대로 현실이 된다 — 현재 Slack 캡처가 AI 출력을 곧바로 커밋하는 상태가 정확히 그 사례다([[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]).
>
> **② 종착지 목록** — `permanent`/`product`/`post` 3종에 **원자 개념 `permanent/concept/`가 추가**된다([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D1). `inbox/`도 폐기 전용이 아니라 *"정제는 못 하지만 버리긴 아깝다"*로 승인된 idea가 머무는 **목적지**가 된다([[decision-011-approval-gate-chain|KDEV-DEC-011]] D1) — 종전 "분류 후 원본 idea 폐기"는 "분류 결과가 `inbox` 보류일 수 있다"로 완화된다.

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- "정제 안 된 아이디어 → 정제 → 영구/참고노트 → 프로덕트/페르소나" 흐름에서, 영구노트와 제품의 관계를 정의해야 함.
- 핵심 질문: permanent가 product로 "승격(이동)"하나? 아니면 별개인가?

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[db-normalization]] — **한 사실은 한 곳에** — permanent·product·post 를 평행 독립 SoT 로 두고 「이동이 아니라 분류」로 본 판단이 이 원리다. `up:` 인용은 중복이 아니라는 구별도 같은 자리에서 나온다

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 승격 = 이동 | permanent→product 파일 이동, SSOT 이동 | 단일 SSOT | permanent(고찰)와 product(명세)는 형태가 다른 별개 지식인데 강제 이동 | 기각 |
| **분류 = 독립 SSOT** | 아이디어가 성격별로 다른 종착지로 갈라짐 | 각자 SSOT, 자연스러움 | 종착지 판단 필요 | **채택** |

## Decision

- **분류 모델**: inbox(idea)가 성격 판단 후 종착지로 분류, 원본 idea는 폐기(휘발).
  - 제품 스펙감 → `products/{x}/00-baseline` (00→20 파이프라인 진입). SSOT = product.
  - 연구/고찰(제품화 전) → `permanent/`. SSOT = permanent.
  - 글감 → `persona/posts/`. SSOT = post.
- permanent와 product/post는 **평행 독립 SSOT** — 이동 관계 아님.
- `up:`(lineage)은 "이 노트는 저것을 기반으로 한다"는 계보 인용일 뿐, 두 노트 모두 각자 SSOT로 살아있음(중복 아님).
- idea는 휘발이라 `up:` 대상 아님 — 상류는 reference·permanent만.
- **분류 기준**: product=명백히 만들 것 / permanent=더 팔 탐구 / post=공유할 글. 명백하면 종착지 직행, 여물 게 더 필요하면 permanent 경유 정제 후 발전(두 경로 공존).
- **정제 메커니즘**: permanent 작성은 단순 이동이 아니라 "연결하며 내 언어로 재작성"하는 사고 행위. 정제의 핵심 순간은 기존 permanent와 `[[]]`로 잇는 때(관련/충돌/확장 발견).
- **정제 주체 = 사람(작성자)**. 에이전트는 inbox 정리·연결 후보 제안까지만 보조, 재작성·연결은 사람이 한다.
- 기각: 승격=이동 모델. 정제를 에이전트가 초안까지 하는 안(제텔 정신상 연결=본인 사고).

## Rationale

- 연구자료(permanent)와 제품 스펙(product)은 같은 내용의 단계가 아니라 다른 종류의 지식. 제품화 안 되는 고찰은 permanent가 최종 SSOT.
- 분류는 SSOT가 한 곳(종착지)이라 중복 없음. lineage는 별개 노트 간 인용이라 SSOT 중복 안 만듦.
- 원본 idea 폐기로 inbox는 항상 미분류만 남음(휘발 유지).

## Scope

- In: 노트 생명주기(수집→분류→연결→망각), SSOT 정의.
- Out: 검증 규칙(L1~L6) — [[decision-006-validation-gates|KDEV-DEC-006]].
- 영향을 받는 spec 후보: 워크플로 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 아카이브 내림 기준 | | 워크플로 spec |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 워크플로 spec | create | 분류·연결·망각 생명주기 |
