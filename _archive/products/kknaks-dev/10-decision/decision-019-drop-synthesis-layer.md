---
type: decision
id: KDEV-DEC-019
title: "판단층(synthesis) 폐기 — 지식을 3층으로 줄인다"
status: accepted
product: kknaks-dev
created_at: 2026-08-10
updated_at: 2026-08-10
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]"
  decisions:
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
    - "[[decision-018-resources-layout-and-sot-naming|KDEV-DEC-018]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works: []
  releases: []
  related: []
up: []
---

# 판단층(synthesis) 폐기 — 지식을 3층으로 줄인다

지식층을 **출처 → 개념 → 실행** 3층으로 줄인다. [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]이 세운 4층 중 **판단층(`resources/synthesis/`, `type: permanent`)만 걷어낸다.** 나머지(층 축 도입, 층별 orphan 판정, 파일명 stem 식별자, 본문 `[[]]` 단일 소스 + `up:` 오버레이)는 그대로 유지한다.

> DEC-010 D1의 4층 표와 그에 딸린 `permanent` 계약을 이 결정이 **대체(supersede)**한다.

## Context

- 관련 baseline: [[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]
- **문제**: 판단층은 도입 이후 **한 건도 쓰이지 않았다.** 그런데 층이 있다는 사실만으로 템플릿·필수 필드·orphan 규칙·`up:` 대상 표가 따라붙었고, 「언제 만드나」를 정하려 하자 후보 탐지 스크립트와 판정 장부까지 필요해졌다.
- **결정이 필요한 이유**: 쓰이지 않는 층이 **사람이 주기적으로 판정해야 하는 큐**를 만들고 있었다. 그것은 자동으로 검증되는 나머지 파이프라인과 성격이 다르다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 4층 유지, 판단층은 비워 둔다 | 스펙 변경 없음 | 빈 층을 채우라는 압력이 규칙·템플릿으로 계속 남는다 | 지금까지의 상태 |
| B | 4층 유지 + 승격 규칙·탐지기·장부를 붙인다 | 파편화를 기계가 감지 | **사람이 판정해야 하는 큐**가 생긴다. 실제로 만들어 봤고 걷어냈다 | 기각 |
| C | **판단층을 없애고 3층으로 간다** | 남는 것이 전부 자동 검증된다 | 여러 제품에 걸친 공통 판단의 자리가 없어진다 | **채택** |

## Decision

- 채택: 지식층은 **출처(`resources/source/`) → 개념(`resources/concept/`) → 실행(`products/`)** 3층이다.
- 채택: `resources/synthesis/` 디렉토리와 `templates/knowledge/permanent.md`를 제거한다.
- 채택: `type: permanent`를 허용 타입에서 뺀다. 층 rank는 `source 1 · concept 2 · execution 3`(값은 상대 순서만 의미).
- 채택: **여러 제품에 걸친 공통 판단은 별도 노트를 두지 않고 각 제품의 `decision`이 갖는다.** 같은 판단이 반복되면 `links.related`로 서로를 가리킨다.
- 채택: 제품 문서의 `up:` 대상은 **`concept`뿐**이다.
- 기각: 승격 트리거·후보 탐지기·판정 장부(Option B). 사람이 돌려야 하는 절차는 두지 않는다.
- 보류: 없음.

## Rationale

- **판단 기준**: 이 레포의 파이프라인은 **어긋나면 커밋이 막히는 것**으로 유지된다(L1~L6, `product_doc_pipeline.py`). 판단층만은 그렇게 만들 수 없었다 — 「같은 판단의 반복인가」는 본문을 읽어야 알 수 있어 기계가 판정하지 못한다.
- **대안 대비 이유**: A는 빈 층이 규칙에 남아 계속 압력이 되고, B는 그 압력을 절차로 바꿔 **관리 대상을 하나 더** 만든다. 실제로 B를 만들어 본 뒤 걷어냈다.
- **리스크**: 같은 판단이 제품마다 반복될 때 한 곳에서 볼 수 없다. 감수한다 — 반복이 실제로 아플 만큼 쌓이면 그때 다시 결정한다. **없어서 아픈 것이 있어서 복잡한 것보다 고치기 쉽다.**

## 근거 개념

없음 — 층을 몇 개 둘지는 이 레포의 운영 판단이고 기댈 개념이 없다.

## Scope

- In: `resources/synthesis/`, `templates/knowledge/permanent.md`, `rules/knowledge-note-pipeline.md`, `agent.md`, `app/back/core/graph.py`, `app/back/service/persona_loader.py`
- Out: `archive/`(층이 아니라 상태라 그대로), `persona/`(A 영역), 제품 문서 파이프라인
- 영향을 받는 spec: KDEV-SPEC-001 · 002 · 003 · 004

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 같은 판단이 제품마다 반복되는 것이 실제로 문제가 되는 시점은 언제인가 | kknaks | 아플 때 다시 결정한다 — 미리 장치를 만들지 않는다 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| KDEV-SPEC-001 | update | 디렉토리에서 `resources/synthesis/` 제거 |
| KDEV-SPEC-002 | update | 층·타입 표에서 `synthesis`·`permanent` 제거 |
| KDEV-SPEC-003 | update | 생명주기에서 판단층 경유 제거 |
| KDEV-SPEC-004 | update | L2 필수필드·L5 orphan 판정에서 `permanent` 제거 |
