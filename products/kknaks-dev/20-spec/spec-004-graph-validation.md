---
type: spec
id: KDEV-SPEC-004
title: "그래프 검증 게이트 — L1~L6"
status: draft
product: kknaks-dev
version: 0.0.1
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-006-validation-gates|KDEV-DEC-006]]"
  specs:
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
  works: []
  releases: []
  related: []
---

# 그래프 검증 게이트 — L1~L6

지식그래프는 SoT라 정합성이 자동 검증되어야 한다. lint 규칙 6개와 3지점 실행, report-only→enforce 순서에 대한 계약.

## 1. Context

### Meta

- Decision reference: [[decision-006-validation-gates|KDEV-DEC-006]]
- Baseline reference: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Domain note: 레벨 = ERROR(차단) / WARN(리포트). 실행 = pre-commit · CI · 부팅.
- Open questions: §7

### Business Requirement

깨진 링크·잘못된 분류·SSOT 중복을 사람이 수동 추적하지 않고, 커밋/머지/부팅 시점에 자동 차단한다.

### Scope

In scope: 규칙 정의, 레벨, 실행 지점, enforcement 적용 순서.
Out of scope: 검증 함수 구현(work), 스키마 정의([[spec-002-graph-schema|KDEV-SPEC-002]]).

## 2. UX Contract

해당 없음 (lint 리포트는 콘솔/CI 출력).

## 3. User Scenario

### S-1. 작성자 — 커밋 시 검증

1. 노트를 커밋하면 pre-commit이 lint 실행.
2. ERROR(L1~L4)가 있으면 커밋 거부 + 위반 목록 출력.
3. WARN(L5/L6)은 리포트만, 커밋 통과.

### S-2. 시스템 — 부팅 시 검증

1. 백엔드 부팅 시 `persona_loader`가 그래프 검증.
2. ERROR면 fail-fast (오염된 SoT로 서버 안 뜸).

## 4. Interface Contract

### Data Contract — 규칙

| ID | 검사 | 레벨 |
|---|---|---|
| L1 dead link | 본문 `[[stem]]`·`up:` 타겟이 실존 | ERROR |
| L2 노드 스키마 | `id`/`type` 필수, type 허용값, 파일명 stem·alias 전역 유일(=SSOT 중복 금지) | ERROR |
| L3 오버레이 정합 | `up:`의 모든 stem이 본문 `[[]]`에도 존재 | ERROR |
| L4 방향 정합 | `up:` 타겟이 위계 상류(ref/permanent→product/post), idea up 금지 | ERROR |
| L5 orphan | 엣지 0개 노드 | WARN |
| L6 archive 참조 | 활성 노트가 `archived`를 `up`으로 의존 | WARN |

### Data Contract — 실행 지점

| 지점 | 차단 |
|---|---|
| pre-commit | ERROR → 커밋 거부 |
| CI | ERROR → 머지 거부 |
| 백엔드 부팅 | ERROR → fail-fast |

## 5. Implementation Rules

- L1~L4 = ERROR(차단), L5/L6 = WARN(리포트).
- **enforcement 적용 순서 (라이브 서버 brick 방지)**: 검증기는 먼저 **report-only**로 도입 → 레포 데이터 정리 후 → **맨 마지막에** ERROR/fail-fast 전환. report-only 출력이 마이그레이션 작업목록이 된다.
- 검증 함수 구현 위치·시그니처는 work (기존 `wikilinks.dead_links()` 확장).

## 6. Verification

### Acceptance Criteria

- [ ] dead link가 있으면 ERROR로 차단된다.
- [ ] 같은 stem이 두 곳에 있으면 L2 ERROR.
- [ ] `up:`이 본문에 없으면 L3 ERROR.
- [ ] idea를 up하면 L4 ERROR.
- [ ] enforcement는 데이터 green 이후에 켜진다(부팅 brick 없음).

## 7. Open Questions

- ~~(구현 OQ, work) 검증 함수 시그니처, 리포트 출력 포맷.~~ **해소(WORK-001, abcfbc4)** — `validate_graph(nodes, duplicate_stems=None) -> list[{rule,level,node,detail}]` + `summarize()`(rule/level별 카운트). 상세 [[spec-002-graph-schema|KDEV-SPEC-002]] §4.
- (OPEN, WORK-007) pre-commit/CI 훅 배선 + ERROR/fail-fast 전환 — enforcement ON 시점.
- (OPEN, WORK-002) L2 navigational 파일 처리 — WORK-002에서 정교화 (검증 false-positive: navigational L2=154, README/log/privacy/support + 중복 stem). 노드 제외 vs frontmatter type 부여 택일은 WORK-002 결정.
- (OPEN, WORK-002) L5 orphan 적용 범위 — WORK-002에서 정교화 (검증 false-positive: orphan L5=196). daily/학습노트 제외 여부 미확정.
