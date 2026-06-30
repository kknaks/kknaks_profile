---
type: work
id: KDEV-WORK-008
title: "전역 그래프 /graph — _graph API + force-directed 시각화"
status: done
product: kknaks-dev
work_type: new-feature
owner: "profile-fe"
roles:
  pm: ""
  design: ""
  fe: "profile-fe"
  be: "profile-be"
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
    - "[[work-007-enforce-validation|KDEV-WORK-007]]"
  releases: []
  related: []
---

# 전역 그래프 /graph — _graph API + force-directed 시각화

전체 지식맵(`_graph`, 309노드/327엣지)을 HTTP로 노출하고 블로그 `/graph`에서 force-directed로 렌더한다(SPEC-005 U-1). 노드색=type, lineage=화살표/assoc=선, archived=흐리게, type 필터. BE 엔드포인트 + FE 페이지를 **계약 기반 병렬**로.

> 비목표: 노트별 로컬 그래프(WORK-009), 개별 노트 라우트(WORK-009), _graph.json 산출 변경(이미 있음).

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-005-graph-visualization|KDEV-SPEC-005]] (U-1 전역)
- Depends on work: [[work-007-enforce-validation|KDEV-WORK-007]] (그래프 데이터 정합·enforced)
- Follow-up work: WORK-009(로컬 그래프 — 이 컴포넌트 서브셋 재사용)
- External dependency: 없음 (force-graph lib 설치됨)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | profile-be(API) + profile-fe(뷰) |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph · `211f502` |
| Blocker | - |
| Next | WORK-009 로컬 그래프 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| BE | profile-be | `GET /api/graph` (get_data()["_graph"] 서빙) + 라우터 등록 | done |
| FE | profile-fe | `/graph` 페이지 + `knowledge-graph-view` 컴포넌트 + api/types/topnav | done |
| QA | admin | API 응답 + build + 엔드포인트 계약 + 게이트 | done |

> **병렬**: API 계약(아래)이 확정이라 BE/FE 동시 진행. FE는 계약에 맞춰 빌드.

## API 계약 (확정 — BE/FE 병렬 기준)

`GET /api/graph` → 메모리 `get_data()["_graph"]` 그대로:
```json
{
  "nodes": [{"id": "<stem>", "type": "reference|permanent|post|product|idea", "title": "...", "archived": false}],
  "edges": [{"source": "<stem>", "target": "<stem>", "type": "lineage|assoc", "dir": "up|null"}],
  "backlinks": {"<stem>": ["<stem>", ...]}
}
```
- 빈 그래프면 `{nodes:[],edges:[],backlinks:{}}`. `_graph_error` 시에도 200 + 빈 그래프(부팅은 enforce가 별도 차단).

## Code Surface

| 구분 | 경로 | 동작 |
|---|---|---|
| 신설 | `app/back/api/routers/graph.py` | `@router.get("/api/graph")` → `get_data().get("_graph") or {빈}` |
| 수정 | `app/back/main.py` (~166-188) | `from api.routers import graph` + `include_router(graph.router)` |
| 신설 | `app/front/app/graph/page.tsx` | `/graph` 페이지(api.graph() fetch → 뷰) |
| 신설 | `app/front/components/graph/knowledge-graph-view.tsx` | force-graph 전역 뷰(type 색·lineage/assoc·archived·필터) |
| 수정 | `app/front/lib/api.ts` | `graph: (lang) => get<GraphResponse>("/api/graph", lang)` |
| 수정 | `app/front/lib/types.ts` | `GraphResponse`(nodes/edges/backlinks) — 기존 NotesGraphResponse와 별개 |
| 수정 | `app/front/components/shell/topnav.tsx` (~8-15) | NAV_ITEMS에 graph 추가 + 번호 갱신 |

- **재사용**: `notes-graph-view.tsx`의 ForceGraph2D 래핑부(SSR lazy-import·ResizeObserver·d3Force 튜닝·zoomToFit) 패턴 복제. `NoteDetailPanel`(backlinks 렌더)은 노드 클릭 패널에 재사용 가능.
- **무변경**: 기존 /notes·/api/notes/graph(notes 전용, 별개).

## Implementation Rules (SPEC-005 §5)

- 노드 색 = `type` (idea/reference/permanent/post/product 5색 — reference·permanent·post·product가 실제 등장. 범례 표기).
- 엣지: `type=="lineage"` → 화살표(react-force-graph `linkDirectionalArrowLength`), `assoc` → 무방향 선.
- `archived==true` → 흐리게(투명도↓).
- type 필터 토글(범례 클릭 등). 노드 포커스 → 이웃 강조(선택).
- 노드 클릭: notes(reference)는 `/api/notes/{id}` 패널(NoteDetailPanel 재사용). product 등 타입별 이동은 WORK-009/후속(이 work는 최소 클릭→패널/하이라이트).

## Execution

### Phase 1 — BE: /api/graph (profile-be)
- **Status**: DONE
- 라우터 신설 + 등록. `GET /api/graph` → `get_data()["_graph"]` 서빙, 200 + 계약(nodes/edges/backlinks). 실데이터 nodes 309/edges 327. 테스트 `TestGraph` 3 추가. (리포트 T-018)

### Phase 2 — FE: /graph 페이지 + 뷰 (profile-fe, Phase 1과 병렬)
- **Status**: DONE
- `/graph` 페이지 + `knowledge-graph-view`(노드색=type 5색·lineage 화살표/assoc 선·archived 흐리게·type 필터·이웃 강조·클릭 패널 `NoteDetailPanel` 재사용). topnav 07/Graph. `npm build` green. (리포트 T-019)

### Phase 3 — 검증 + 커밋 (admin)
- **Status**: DONE
- pytest **281 passed**(+TestGraph 3), `npm build` green, 시각 규칙 코드 검증(5색·alpha 0.3·lineage 화살표 함수). 데이터 경로·계약·컴파일 검증 완료. ⚠ 실 canvas 픽셀 렌더는 미검증(force-dynamic, lineage 데이터 0건) — Open Issue 표기. 커밋 `211f502`.

## Pre-deploy Check

- [x] `/api/graph` 200 + 계약(nodes/edges/backlinks) — nodes 309/edges 327
- [x] `npm build` green (FE 타입·빌드)
- [x] enforce/그래프 데이터 무변경(읽기 전용 노출)
- [x] 기존 /notes·/api/notes/graph 무영향

## Rollback

- 라우터·페이지 신설이라 revert로 원복. 기존 기능 무영향.

## Done Criteria (SPEC-005 §6)

- [x] `/api/graph`가 전역 _graph(nodes/edges/backlinks) 서빙, 계약 일치 (nodes 309/edges 327)
- [x] `/graph`에서 전체 노드/엣지가 type 색·엣지 스타일(lineage 화살표/assoc 선)로 렌더 (코드 검증; ⚠ 실 픽셀 렌더 미검증 — Open Issue)
- [x] 노드 클릭(패널/이동), type 필터 동작 (NoteDetailPanel 재사용·필터 토글)
- [x] archived 노드 시각 구분(흐리게, alpha 0.3)
- [x] pytest(281 passed) + `npm build` green
- [x] 30-work/README·log 갱신

## Open Issues

- **실 canvas 픽셀 렌더 미검증**: 검증은 데이터 경로·계약·컴파일·시각 규칙 코드(5색·alpha 0.3·lineage 화살표 함수)까지. force-dynamic + lineage 데이터 0건이라 실제 캔버스 픽셀 렌더는 자동 게이트에서 미확인. 실데이터 렌더 시 육안 확인 후속.
- 노드 클릭 시 타입별 정식 이동(notes/[id]·products showcase)은 WORK-009 + 후속. 이 work는 패널/하이라이트까지.
- 309노드 성능/클러스터링(SPEC-005 §7) — 현재 규모는 force-graph 무난, 필요 시 후속.

## Related

- Spec: [[spec-005-graph-visualization|KDEV-SPEC-005]]
- Work: [[work-007-enforce-validation|KDEV-WORK-007]]
