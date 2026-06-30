---
type: work
id: KDEV-WORK-009
title: "노트별 로컬 그래프 — 이웃(1-hop) + 백링크 미니 그래프"
status: done
product: kknaks-dev
work_type: new-feature
owner: "profile-fe"
roles:
  pm: ""
  design: ""
  fe: "profile-fe"
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-06-30
updated_at: 2026-06-30
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions: []
  specs:
    - "[[spec-005-graph-visualization|KDEV-SPEC-005]]"
  works:
    - "[[work-008-global-graph|KDEV-WORK-008]]"
  releases: []
  related: []
---

# 노트별 로컬 그래프 — 이웃(1-hop) + 백링크 미니 그래프

선택한 노트 중심의 1-hop 이웃 + 백링크 미니 그래프(SPEC-005 U-2). **FE-only** — `/graph`가 이미 로드한 그래프 데이터에서 ego-network를 클라이언트 추출, WORK-008의 force-graph 컴포넌트를 서브셋 모드로 재사용. BE 무변경.

> 비목표: 개별 노트 라우트(notes/[id]) 신설, BE 신규 엔드포인트, 데이터 산출 변경.

## 스코핑 결정 (admin 2026-06-30)

현재 UX는 개별 노트 라우트가 없고 **노드 클릭 → 상세 패널**(NoteDetailPanel) 방식이다. SPEC-005 U-2의 "노트 페이지 하단 로컬 그래프"를 **클릭 패널 안에 임베드**하는 게 기존 UX와 정합(새 라우트 sprawl 회피). "노트 페이지" = 현 패널.

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-005-graph-visualization|KDEV-SPEC-005]] (U-2 로컬)
- Depends on work: [[work-008-global-graph|KDEV-WORK-008]] (force-graph 뷰·graph 데이터·패널 재사용)
- Follow-up work: 없음 (PLAN-003 적용 단계 종료)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature (FE-only) |
| Owner | profile-fe |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph · `7436119` |
| Blocker | - |
| Next | (PLAN-003 적용 완료) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| FE | profile-fe | ego-network 추출 + 패널 내 미니 그래프 렌더 | done |
| QA | admin | npm build + 렌더 게이트 | done |

## Code Surface

| 구분 | 경로 | 동작 |
|---|---|---|
| 수정 | `app/front/components/graph/knowledge-graph-view.tsx` | 노드 클릭 패널에 로컬 미니 그래프 섹션 추가 |
| 신설(선택) | `app/front/components/graph/local-graph.tsx` | ego-network 미니 force-graph(서브셋) |
| 유틸 | (동일 파일 내) | ego 추출: 선택 노드 + edges에서 1-hop 이웃 + `backlinks[id]` |

- **데이터**: 이미 로드된 `GraphResponse`(nodes/edges/backlinks)에서 클라이언트 추출. BE/API 무변경.
- **재사용**: WORK-008 force-graph 래핑부 + 시각 규칙(type색·lineage 화살표/assoc 선·archived). 미니 모드(작은 캔버스, 중심 노드 강조).

## Implementation Rules (SPEC-005 §5/U-2)

- 로컬 그래프 = 선택 노드 + **1-hop 이웃**(edges에서 source/target 인접) + **backlinks**(역참조).
- 중심 노드 시각 강조. 이웃 노드 클릭 → 해당 노드로 패널 전환(또는 포커스 이동).
- "연결된 노트" 헤더(SPEC-005 U-2 문구). 이웃 0이면 단독 노드 상태 표시.
- 시각 규칙은 WORK-008 전역과 동일(type색·lineage 화살표·archived 흐리게).

## Execution

### Phase 1 — ego 추출 + 미니 그래프 (profile-fe)
- **Status**: DONE
- `local-graph.tsx` `egoNetwork(g, centerId)`: edges 1-hop 이웃 + `backlinks[id]` 역참조 추출(pristine 노드 복사로 전역 시뮬레이션 무충돌, 백링크 엣지 중복 방지). `LocalGraph` 미니 force-graph(240px·중심 노드 강조·"연결된 노트 N" 헤더·이웃 0이면 단독 상태), 이웃 클릭 → 패널 재중심. 공유 시각규칙 모듈 `lib/graph.ts`(전역·로컬이 import → 색 규칙 drift 방지). (리포트 T-021)

### Phase 2 — 검증 + 커밋 (admin)
- **Status**: DONE
- `npm build` green(`/graph` 3.85kB, `/notes` 무영향), 라이브 SSR 검증(310노드/330엣지, 범례 실 8종 전부·stale 4종 0건 → 데이터 기반 팔레트 동작 확인). ⚠ canvas 픽셀 렌더(노드색·archived 흐림·로컬 미니그래프 레이아웃·이웃 클릭 전환)는 헤드리스라 육안 미확인. 커밋 `7436119`.

## Pre-deploy Check

- [x] `npm run build` green
- [x] BE/API 무변경(FE-only) — git status상 백엔드 무변경
- [x] 기존 /graph 전역 뷰·패널 무회귀(`/notes` 무영향 확인)

## Rollback

- FE 컴포넌트 변경이라 revert로 원복.

## Done Criteria (SPEC-005 §6)

- [x] 노트(노드) 선택 시 로컬 그래프(이웃 1-hop + 백링크) 표시 (egoNetwork 추출·LocalGraph 임베드; ⚠ 픽셀 레이아웃 육안 미확인 — Open Issue)
- [x] 이웃 노드 클릭으로 전환/이동 (onSelectNode 재중심; ⚠ 클릭 동작 육안 미확인)
- [x] 이웃 없으면 단독 노드 상태 (구현됨)
- [x] 시각 규칙(type색·archived) 전역과 일관 (공유 `lib/graph.ts`; ⚠ lineage 화살표는 데이터 0건이라 발현 불가·검증 불가 — Open Issue)
- [x] npm build green
- [x] 30-work/README·log 갱신

## Open Issues

- 개별 노트 라우트(notes/[id]) + 페이지 하단 배치는 미채택(패널 임베드로 대체). 향후 노트 상세 페이지 도입 시 재배치 가능.
- **canvas 픽셀 렌더 육안 미종결**: T-021 게이트는 헤드리스(SSR 범례·데이터 기반 팔레트·build까지 검증). WORK-008+009 실 캔버스 픽셀(노드색·archived 흐림·로컬 미니그래프 레이아웃·이웃 클릭 전환)은 브라우저 필요 — 육안 후속.
- **lineage 엣지 0건**: 라이브 330엣지 전부 `assoc`/`dir:null`. lineage 화살표 규칙은 계약대로 구현됐으나 데이터에 미발현 → 시각 검증 불가. 빌더가 lineage(up: 오버레이)를 안 내는지는 SPEC-005 §7 / SPEC-002 §7 Open Question으로 박제(이 work 범위 아님).

## Related

- Spec: [[spec-005-graph-visualization|KDEV-SPEC-005]]
- Work: [[work-008-global-graph|KDEV-WORK-008]]
