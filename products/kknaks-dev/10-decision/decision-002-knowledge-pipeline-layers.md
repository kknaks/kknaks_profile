---
type: decision
id: KDEV-DEC-002
title: "지식 파이프라인 층을 루트 레벨로 (inbox/reference/permanent/archive/posts)"
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
    - "[[decision-001-products-single-root|KDEV-DEC-001]]"
    - "[[decision-005-classification-workflow|KDEV-DEC-005]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works: []
  releases: []
  related: []
---

# 지식 파이프라인 층을 루트 레벨로 (ADR-002)

아이디어→참고→영구 노트를 종착지(products·persona)와 같은 루트 레벨에 둔다. 장기기억은 `permanent/archive/`, 발행물은 `persona/posts/`.

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- persona는 노드는 많은데 가로 연결이 비어 있었다. 빠진 층: 아이디어 inbox(fleeting), 영구노트(permanent), 참고노트의 명확한 위치.
- `persona/daily/`는 `auto:true` 커밋 기반 활동 로그라 fleeting 역할을 못 함.
- `persona/contents/` 22개 중 21개가 외부 자료 정리(참고노트), `persona/notes/` 168개도 참고노트.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| persona 안에 형제 | persona/ideas, persona/permanent | persona 응집 | 파이프라인이 persona에 갇힘 | 부분 채택(아님) |
| **루트 레벨** | inbox/·reference/·permanent/ 를 루트로 | 파이프라인 한눈, 휘발/영구 생명주기 분리 | 루트 디렉토리 증가 | **채택** |

장기기억: (A) `permanent/archive/` 하위 / (B) 루트 `archive/` → **A**.

## Decision

- 채택:
  - `inbox/` — 정제 안 된 아이디어(fleeting, 휘발).
  - `reference/` — 참고노트(자료 정리, 출처 종속). ← `persona/notes`·`contents` 외부정리 종착.
  - `permanent/` — 영구노트. `permanent/archive/` = 장기기억(cold).
  - `persona/posts/` — 발행물(영구노트가 글이 된 것). 신설.
  - `persona/algorithms/` — 개인 배치 산출물, 그래프 무관, 잔류.
  - `persona/contents/C-001`(테스트용) 삭제.
- 기각: 파이프라인을 persona 하위에 두는 안.

## Rationale

- inbox는 빨리 던지는 곳이라 깊은 경로에 묻히면 즉시성이 죽음 → 루트.
- 참고노트는 출처가 외부(남의 자료)라 "나(persona)"보다 독립 지식층 → 루트 reference.
- 장기기억을 `permanent/archive/` 하위에 두면 LLM 워커가 평소 스캔에서 cold 노트를 안 읽음(agent.md 읽기범위). 부활 = 폴더 한 칸 이동.
- 링크는 파일명 stem 기반이라 폴더를 옮겨도 엣지가 안 끊김([[decision-003-node-type-and-identifier|KDEV-DEC-003]]).

## Scope

- In: 루트 디렉토리 층 + persona 재편(projects→products, notes/contents→reference, posts 신설).
- Out: 마이그레이션 실행, 아카이브 내림 기준(워크플로 spec).
- 영향을 받는 spec 후보: 디렉토리 구조 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 아카이브 내림 기준은 검증/워크플로 spec에서 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 디렉토리 구조 spec | create | 루트 층 + persona 재편 |
