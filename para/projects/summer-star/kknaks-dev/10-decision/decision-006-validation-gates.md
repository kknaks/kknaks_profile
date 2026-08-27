---
type: decision
id: KDEV-DEC-006
title: "검증 게이트 L1~L6 — 정합성 자동 차단"
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
    - "[[decision-004-edge-model-and-schema|KDEV-DEC-004]]"
    - "[[decision-005-classification-workflow|KDEV-DEC-005]]"
  specs:
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works: []
  releases: []
  related: []
up:
  - foreign-key
  - unique-key
  - ci-cd
---

# 검증 게이트 L1~L6 (ADR-006)

지식그래프는 SoT 그 자체라 정합성이 최우선. lint 규칙 6개를 3지점(pre-commit/CI/부팅)에서 자동 차단한다. 수동 체크 0.

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- 기존 인프라: `wikilinks.dead_links()`(깨진 링크 검출), `persona_loader` 부팅 fail-fast, `_map.md` pre-commit+부팅 빌드, `product_doc_pipeline.py`.
- "깨진 링크를 수동으로 어떻게 추적하나", "분류/계보를 어떻게 검증하나"가 핵심 요구.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[foreign-key]] — L1 dead link 는 **참조 무결성 검사** 그 자체다 — 가리키는 대상이 없으면 막는다
- [[unique-key]] — L2 의 「파일명 stem·alias 전역 유일」이 유일 제약이고, 그것이 곧 SoT 중복 금지다
- [[ci-cd]] — 여섯 규칙을 **pre-commit·CI·부팅 세 지점에서 자동 차단**한다. 사람이 기억해서 지키는 것이 아니라 통과 못 하면 못 들어가게 만든 것이 이 결정의 핵심이다

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 수동 점검 | 사람이 링크 확인 | 단순 | 누락, 안 됨 | 기각 |
| **자동 lint 게이트** | 규칙 + 3지점 차단 | 정합성 보장 | 구현 필요 | **채택** |

## Decision

lint 규칙:

| ID | 검사 | 레벨 |
|---|---|---|
| L1 dead link | 본문 `[[stem]]`·`up:` 타겟 실존 | ERROR |
| L2 노드 스키마 | id/type 필수, type 허용값, 파일명 stem·alias 전역 유일(=SSOT 중복 금지) | ERROR |
| L3 오버레이 정합 | `up:`의 모든 stem이 본문 `[[]]`에도 존재 | ERROR |
| L4 방향 정합 | `up:` 타겟이 위계 상류(ref/permanent→product/post), idea up 금지 | ERROR |
| L5 orphan | 엣지 0개 | WARN |
| L6 archive 참조 | 활성→archived `up` 의존 | WARN |

- 실행 3지점 모두 ERROR 차단: pre-commit(커밋 거부) · CI(머지 거부) · 백엔드 부팅(fail-fast, 오염 SoT면 서버 안 뜸).
- 구현: `core/wikilinks.py` 옆 검증 함수. 산출물 = `_graph.json` + lint 리포트.
- "깨진 링크 추적"=L1, "분류/계보 검증"=L1+L3+L4.

## Rationale

- SoT라 정합성 우선 → L1~L4는 차단(ERROR), L5/L6은 리포트(WARN).
- 부팅 fail-fast로 오염된 SoT로는 서버가 안 뜨게(가용성보다 정합성).
- L2 stem 전역 유일 = SSOT 중복 금지가 자동 검증됨([[decision-005-classification-workflow|KDEV-DEC-005]]).
- ⚠ 적용 순서: 검증기는 report-only로 먼저 만들고, ERROR/fail-fast는 데이터 정리 후 **맨 마지막에** 켠다(안 그러면 라이브 서버 brick).

## Scope

- In: lint 규칙·레벨·실행 지점.
- Out: 구현(work), enforcement 켜는 시점(work 순서).
- 영향을 받는 spec 후보: 검증 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 검증 spec | create | L1~L6 + 3지점 + report-only→enforce 순서 |
