---
type: decision
id: DEC-001
title: ""
status: proposed
product: ""
created_at: 2026-05-28
updated_at: 2026-05-28
tags:
  - product/
  - doc/decision
  - status/proposed
links:
  baselines: []
  decisions: []
  specs: []
  works: []
  releases: []
  related: []
# 이 결정의 근거가 된 concept stem (resources/concept/). 아래 「근거 개념」에도 [[]] 로 적는다.
# `links:` 버킷과 달리 `up:` 만 그래프 엣지가 된다 — rules/knowledge-note-pipeline.md
up: []
---

# Title

<1-2줄 요약: baseline의 어떤 입력을 제품에 어떻게 반영할지 결정한다.>

> baseline의 날것 입력을 spec으로 내리기 전에 적용 방향을 정하는 문서.
> 기능 계약 상세는 `20-spec/`, 실제 작업 순서는 `30-work/`에 둔다.

## Context

어떤 baseline을 보고 판단하는지 적는다.

- 관련 baseline:
- 문제/기회:
- 결정이 필요한 이유:

## Options

검토한 선택지를 적는다.

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A |  |  |  |  |
| B |  |  |  |  |

## Decision

채택한 방향을 적는다.

- 채택:
- 기각:
- 보류:

## Rationale

왜 이 결정을 했는지 적는다.

- 판단 기준:
- 대안 대비 이유:
- 리스크:

## 근거 개념

이 결정이 기대는 개념(`resources/concept/`). 개념 상세는 여기 쓰지 않고 링크로 위임한다 — 상세의 SoT는 concept 노트다.

- [[concept-stem]] — 이 결정에서 그 개념이 한 역할 한 줄

> `up:`에 넣은 stem은 이 절에도 `[[]]`로 있어야 한다(그래프 L3 오버레이).
> 근거가 아니라 단순 참조면 `up:`에 넣지 말고 본문 링크로만 둔다.

**쓰다가 새 개념이 나오면** 먼저 있는지 찾고(`ls resources/concept/` + `aliases` grep),
없으면 둘로 가른다 — **세상에 있는 개념**이면 `resources/source/`에 출처 노트를 만들고 그것을
`up:`으로 `resources/concept/`를 만든다. **이 결정에서 처음 세운 판단**이거나 **여기서만 쓰는
말**이면 개념이 아니라 이 문서가 그대로 갖는다(`up: []` + 「없음 — 사유」).
판단 기준은 `rules/knowledge-note-pipeline.md`의 「결정을 쓰다 새 개념이 나오면」.
개념은 결정 문서를 `up:`으로 가리킬 수 없다(층 방향).
**개념을 만드는 것은 이 결정을 쓰는 쪽의 일이다** — 같은 턴에 `resources/source/` 와
`resources/concept/` 를 만들어 잇는다. 미루면 그 개념은 만들어지지 않는다.

## Scope

이번 spec에 반영할 범위.

- In:
- Out:
- 영향을 받는 spec 후보:

## Open Questions

아직 결정하지 못했지만 spec으로 내려가기 전에 풀어야 하는 질문.

| ID | Question | Owner | Next |
|---|---|---|---|
|  |  |  |  |

## Resulting Spec

이 결정으로 생성하거나 업데이트할 spec.

| Spec | Action | Notes |
|---|---|---|
|  | create/update |  |
