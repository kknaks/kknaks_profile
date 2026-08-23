---
type: baseline
id: KDEV-BL-001
title: "레포를 지식그래프로 — 상향식/하향식 메모 연결"
status: accepted
product: kknaks-dev
source:
  type: idea
  ref: "제텔카스텐(Zettelkasten) + PARA 조사, claude_pr/kknaks_profile/plans/PLAN-003"
links:
  baselines: []
  decisions:
    - "[[decision-001-products-single-root|KDEV-DEC-001]]"
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
    - "[[decision-003-node-type-and-identifier|KDEV-DEC-003]]"
    - "[[decision-004-edge-model-and-schema|KDEV-DEC-004]]"
    - "[[decision-005-classification-workflow|KDEV-DEC-005]]"
    - "[[decision-006-validation-gates|KDEV-DEC-006]]"
    - "[[decision-007-blog-graph-visualization|KDEV-DEC-007]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
    - "[[spec-005-graph-visualization|KDEV-SPEC-005]]"
  works: []
  releases: []
  related: []
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/accepted
---

# 레포를 지식그래프로 — 상향식/하향식 메모 연결

`kknaks_profile` 레포 전체를 상향식/하향식 메모로 연결된 하나의 지식그래프로 만들고, kknaks 블로그에서 그 관계를 시각화한다.

> 이 baseline은 이미 설계가 완료되어(PLAN-003) decision/spec으로 전개된 입력이다. 출발 아이디어와 당시 진단을 보존용으로 기록한다.

## Raw

평소 떠오른 생각·조사한 자료를 어딘가에 기록하고, 그 조각을 영구노트로 보관하고, 제품화할 수 있는 것은 제품으로 확장한다.

```
정제 안 된 아이디어 → 정제 → 영구/참고노트 → 프로덕트/페르소나 → (블로그 그래프 시각화)
```

이론적 배경 두 가지:
- **제텔카스텐(Zettelkasten)** — 작은 노트를 모아 연결하며 생각을 발전시키는 상향식 방식. fleeting(임시) → reference(참고) → permanent(영구) → 구조 노트.
- **PARA** — Project / Area / Resource / Archive. 주제가 아니라 *목적*으로 분류하고, 노트 위치는 유동적.

## Context

작업 착수 시점(2026-06-29) 진단 — 레포는 이미 *반쪽짜리* 지식그래프였다.

| 영역 | 노드(md) | 위키링크 포함 | frontmatter |
|---|---|---|---|
| `products/` | 243 | 138 | 135 |
| `persona/` | 299 | 15 | 298 |
| `context/` | 9 | 0 | 0 |

- `products/`는 이미 내부 연결된 그래프(하향식 개발 SSOT).
- `persona/`는 노드는 풍부하나 가로 연결이 거의 없음 — **상향식 연결망이 비어 있다.**
- 그래프 인프라(`app/back/core/wikilinks.py`: `build_graph`, `dead_links`)와 자동 인덱스(`_map.md`)가 이미 존재. DB 없음, 파일(frontmatter)이 SoT.
- 빠진 것: 아이디어 inbox(fleeting), 영구노트(permanent), 노트→제품으로 가는 관계 엣지.

## Why It Matters

- 흩어진 생각·자료가 연결되어 축적되면, 글쓰기·제품화의 재료가 된다 (백지에서 시작하지 않음).
- 관계를 블로그에서 시각화하면 "내 지식이 어떻게 이어지는지"가 포트폴리오가 된다.
- 단, 이건 **SoT 그 자체**라 정합성(깨진 링크·승격 추적)이 자동 검증되어야 한다.

## Possible Direction

(이후 decision으로 확정됨)

- 제품/프로젝트를 `products/` 단일 루트로 통합, showcase 카드 포함.
- 지식 파이프라인을 루트 레벨로: `inbox/`(휘발) · `reference/`(참고) · `permanent/`(영구, `archive/` 포함).
- 노드 식별자 = 파일명 stem(옵시디언 기준), 엣지 = 본문 `[[ ]]` + frontmatter `up:` 오버레이.
- 승격이 아니라 **분류** — 아이디어가 성격에 따라 독립 SSOT(permanent/product/post)로 갈라짐.
- 검증 게이트(L1~L6) + 블로그 그래프 시각화(전역 + 노트별 로컬).
