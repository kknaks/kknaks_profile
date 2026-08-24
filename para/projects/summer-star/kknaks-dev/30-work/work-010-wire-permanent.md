---
type: work
id: KDEV-WORK-010
title: "permanent 층 그래프 배선 — 영구노트를 _graph에 연결"
status: done
product: kknaks-dev
work_type: new-feature
owner: "profile-be"
roles:
  pm: ""
  design: ""
  fe: ""
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
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
  works:
    - "[[work-005-migrate-notes|KDEV-WORK-005]]"
  releases: []
  related: []
---

# permanent 층 그래프 배선 — 영구노트를 _graph에 연결

WORK-003에서 scaffold만 된 `permanent/`(영구노트 층)를 loader+graph에 배선한다. 그래야 영구노트를 쓰면 `/graph`에 `permanent` 노드로 뜨고, `reference→permanent` `up:` 계보가 **lineage 화살표**로 발현된다(현재 lineage 0건인 근본 이유 = permanent 미배선이라 `up:` 쓸 데가 없음). **BE-only** — WORK-005 reference 배선의 단순 미러(flat 구조, FE·라우트·dict키 트릭 불필요). `/api/graph`는 자동 노출(`_graph`가 permanent 포함).

> 비목표: inbox 배선(idea=휘발·비공개 scratch, 그래프 제외 유지), posts 배선(WORK-006 연기 — 첫 발행물 시 별도), FE 변경(불필요).

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-001-directory-structure|KDEV-SPEC-001]](permanent 실재화), [[spec-003-knowledge-workflow|KDEV-SPEC-003]](정제→permanent 종착 라이브화)
- Depends on work: [[work-005-migrate-notes|KDEV-WORK-005]](reference 배선 패턴 미러), enforcement(WORK-007)
- Follow-up work: (선택) posts 배선·inbox 정책
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature (BE-only) |
| Owner | profile-be |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph · `f7c34f7` |
| Blocker | - |
| Next | (지식 파이프라인 라이브 — permanent 노트 작성) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| BE | profile-be | permanent 로더 + 그래프 노드 + REQUIRED_FIELDS + map/test | done |
| QA | admin | boot(enforce ON) + pytest + 그래프 측정(빈 permanent 무영향) → 커밋 | done |

## 배경 — 현재 배선 상태 (정직)

`/api/graph`·`_graph`에 **현재 잡히는 것**: `reference/`(157, WORK-005) + `products/`(showcase+제품문서). **안 잡히는 것**: `inbox/`·`permanent/`·`persona/posts/`(전부 README scaffold만, loader 미스캔). 이 work는 그중 **permanent만** 배선한다(핵심 지식 허브 층).

## Code Surface (WORK-005 미러)

| 경로 | 동작 |
|---|---|
| `persona_loader.py:494 _load_reference_notes` 패턴 | 신규 `_load_permanent_notes(permanent_dir, persona_dir)`: `permanent/*.md`(flat) + `permanent/archive/*.md`(archived=true) 스캔. type=permanent·id=stem 주입(frontmatter 있으면 존중). **group 없음**(flat). |
| `persona_loader.py:67 REQUIRED_FIELDS` | `"permanent": {"type","id","title"}` 추가(flat=group 없음, reference 미러 minus group). |
| `persona_loader.py:216 _build_graph_nodes` | permanent 노트를 노드에 추가(현재 notes+products → +permanent). type=permanent, archived 반영. 본문 `[[]]`→assoc, `up:`→lineage. |
| `persona_loader.py` load_persona | permanent 로드 호출 + `_build_graph_nodes`에 전달. (선택) `data["permanent"]` 키. |
| `app/scripts/build_persona_map.py` | (선택) permanent 섹션 — _map.md 완전성. pre-commit 훅 정합. |
| `app/back/tests/test_loader.py`/`test_graph.py` | permanent 로드·그래프 노드·archived·REQUIRED 테스트(WORK-005 tmp 격리 패턴). |

- **무변경**: API 스키마(/api/graph는 _graph 그대로 → permanent 자동 포함), FE, /notes·/contents.
- **enforcement 상호작용**: permanent가 그래프 노드가 되므로 dead link·스키마·`up:` 방향(L1~L4)이 permanent 노트에도 강제됨(의도 — 오염 차단). 빈 permanent는 노드 0 → 무영향.

## ⚠ 구현 주의 (worker 확인)

- **L4 방향 정합**: `permanent up: [reference-stem]`에서 up 타겟 rank 비교(graph.py `_TYPE_RANK`: reference=4, permanent=4 동일). 동일 rank up이 L4 ERROR 안 나는지 **테스트로 확인**(나면 rank/규칙 조정은 별도 — 이 work는 배선만, 데이터 없어 latent). idea up 금지는 유지.
- **archived 판정**: `permanent/archive/` 경로 → archived=true (graph.py archived 노드는 id/alias 면제 = L2 해소 정합).
- report-only 아님 — enforcement ON 상태. 빈 permanent라 ERROR 0 유지돼야 부팅 정상.

## Execution

### Phase 1 — permanent 로더 + 그래프 노드 (profile-be)
- **Status**: DONE
- `_load_permanent_notes`+`_enrich_permanent`(flat 스캔, `archive/`→archived, type=permanent·id=stem·title=stem 주입, README 제외) + `REQUIRED_FIELDS["permanent"]={type,id,title}`(reference 미러 minus group/date) + `_build_graph_nodes` permanent 인자 + load_persona 배선(`data["permanent"]` 키) + `validate_persona` permanent 블록(id==stem 강제). (리포트 T-023)
- (선택) `build_persona_map` permanent 섹션은 **미수행**(정직) — `_map.md`는 persona/ 전용·permanent는 레포 루트·빈 층, pre-commit 정합 영향 없음(load_persona가 검증).

### Phase 2 — 검증 + 커밋 (admin)
- **Status**: DONE
- enforce-ON 부팅 성공(`GRAPH_ENFORCE=1`, raise 없음, ERROR-level 0·L5=156 WARN만), 빈 permanent → permanent loaded 0·노드 0·violations 불변(reference+products 그대로). 샘플 픽스처로 permanent 노드 발현·archived 판정·`up:`→lineage 엣지(dir=up)·L4 동일-rank 허용 실증. **286 passed**(=281+TestPermanent 5). `/api/graph` 스키마 무변경(permanent 자동 포함). 커밋 `f7c34f7`. (admin 게이트 독립 재현)

## Pre-deploy Check

- [x] enforce ON 부팅 성공(빈 permanent, ERROR 0 유지)
- [x] permanent 미작성 시 _graph 무변경(reference+products 그대로, permanent 노드 0)
- [x] API/FE 무변경(/api/graph 스키마 그대로)

## Rollback

- 로더/그래프 배선이라 revert로 원복.

## Done Criteria

- [x] `_load_permanent_notes` + REQUIRED_FIELDS["permanent"] + `_build_graph_nodes`에 permanent 포함
- [x] permanent/archive → archived (`test_archive_subdir_is_archived`)
- [x] 샘플 permanent 노트가 _graph에 permanent 노드 + `[[]]`/`up:` 엣지(lineage) 발현(테스트 실증 `test_up_emits_lineage_and_l4_same_rank_ok`; ※ live permanent 0건이라 라이브 /graph에는 아직 미발현 — 데이터 작성 시 발현)
- [x] boot(enforce ON) + pytest green(286 passed), 빈 permanent 무영향
- [x] 30-work/README·log 갱신

## Open Issues

- inbox(idea) 그래프 노출 정책 — 휘발·비공개라 제외 유지(별도 결정 시 변경).
- posts 배선 — WORK-006 연기 유지(첫 발행물 시).
- L4 동일-rank up(permanent↔reference) 규칙 — 데이터 생기면 재확인.

## Related

- Spec: [[spec-001-directory-structure|KDEV-SPEC-001]], [[spec-003-knowledge-workflow|KDEV-SPEC-003]]
- Work: [[work-005-migrate-notes|KDEV-WORK-005]]
