---
type: work
id: KDEV-WORK-004
title: "projects → products/{제품}/showcase.md 재편 + loader 재배선"
status: done
product: kknaks-dev
work_type: migration
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
  works:
    - "[[work-003-knowledge-layer-scaffold|KDEV-WORK-003]]"
  releases: []
  related: []
---

# projects → products/{제품}/showcase.md 재편 + loader 재배선

`persona/projects/*.md` 13개(블로그 showcase 카드)를 `products/{제품}/showcase.md`로 이동하고(D-002), loader가 `products/*/showcase.md`를 읽도록 재배선한다. **dict 키 `"projects"`는 유지** → /api/projects·print·inputs·FE 무변경. report-only 불변. 이동·코드는 **하나의 atomic 커밋**(반쪽 = 블로그/pre-commit 훅 깨짐).

> 비목표: notes/contents 이동(WORK-005/006), enforcement(WORK-007), 시각화(WORK-008/009), product-as-graph-node 정식화(아래 §Open Issue, SPEC-002 후속).

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-001-directory-structure|KDEV-SPEC-001]] (projects→products 재편)
- Depends on work: [[work-003-knowledge-layer-scaffold|KDEV-WORK-003]] (층 scaffold 완료)
- Follow-up work: WORK-005(notes→reference), WORK-006(contents→reference/posts)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | migration |
| Owner | profile-be (코드) + product-curator (배치) |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph · 커밋 `7548a67` (atomic) |
| Blocker | - |
| Next | WORK-005 notes→reference |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| curator | product-curator | 13개 showcase 배치(git mv + org 주입 + 디렉토리 생성) | done |
| BE | profile-be | loader glob 재배선 + 그래프 showcase 제외 + map builder + inputs/main_job 주석 + test fixture | done |
| QA | admin | pytest 재현 + /api/projects·블로그 렌더 + _map.md 빌드 + 그래프 baseline 확인 → atomic 커밋 | done |

> **순서**: curator 배치 먼저(파일 이동) → 검수 → BE 코드(이동된 파일 대상 테스트) → admin atomic 커밋. 워커는 커밋 안 함(pre-commit 훅이 마이그레이션 중간에 _map.md를 깨뜨리지 않게 admin이 단일 커밋).

## Scope

포함:
- `persona/projects/*.md` 13개 → `products/{제품}/showcase.md` 이동(파일명 = `showcase.md`, 디렉토리명 = 기존 stem).
- showcase frontmatter에 `org: company|studio` 주입(아래 표). `type:project`·`id:P-NN`·`category`·`status`·`visible`·`stack`·`thumbnail`·`links.repo`·케이스스터디 본문 **그대로 보존**.
- loader: `products/*/showcase.md` glob 로드(dict 키 `"projects"` 유지). 카테고리 검증은 `persona/_meta.yaml`의 `projects.categories` 그대로.
- 그래프 빌더가 `showcase.md`를 노드 스캔에서 제외(stem 충돌 방지).
- lockstep: `build_persona_map.py`·`inputs.py`/`main_job.py` 주석·test fixture.

제외:
- product 파이프라인 디렉토리(00-baseline 등) 신설 — 회사/일부 개인 제품은 `showcase.md`만(S1). 파이프라인은 각 제품 작업 시.
- P-NN id·`/assets/projects/P-NN/` 경로 변경 — **유지**(D-013: rename은 선택적 폴리시, 자산 보존 우선).
- product-as-graph-node(type=product, dir-identity) → §Open Issue.

## org 매핑 (admin 확정 2026-06-30)

| project | org |
|---|---|
| centurion-charty | company |
| centurion-mso | company |
| linky | company |
| mediness | company |
| nexus | company |
| kknaks-profile | studio |
| language-diary | studio |
| mykakao | studio |
| open-kknaks | studio |
| persona-counselor | studio |
| study-timelapse | studio |
| summer-star-company | studio |
| wine-log | studio |

- 기존 product 디렉토리 있음(showcase만 추가): language-diary, mykakao, open-kknaks, persona-counselor, study-timelapse, wine-log.
- 신규 디렉토리 생성(showcase만): centurion-charty, centurion-mso, linky, mediness, nexus, kknaks-profile, summer-star-company.

## Code Surface

| 경로:라인 | 동작 |
|---|---|
| `persona/projects/*.md` (13) | git mv → `products/{stem}/showcase.md` |
| `app/back/service/persona_loader.py:110` | `_load_dir(persona/projects)` → `products/*/showcase.md` glob 로드(키 "projects" 유지) |
| `app/back/service/persona_loader.py:201` | `_build_graph_nodes` glob에서 `name == "showcase.md"` 제외(stem 충돌 회피) |
| `app/scripts/build_persona_map.py:262` | `_load_dir("projects")` → `products/*/showcase.md` 로드(pre-commit 훅 _map.md 빌드) |
| `app/back/service/jobs/inputs.py:146` | docstring `persona/projects/*.md` → `products/*/showcase.md` (로직 무변경) |
| `app/back/service/jobs/main_job.py:79,84` | 주석 경로 갱신(로직 무변경, `get_data().get("projects")` 유지) |
| `app/back/tests/test_loader.py` (~249) | `_scaffold_min_persona`가 `products/{x}/showcase.md` 생성하도록 fixture 수정 |
| `app/back/tests/test_routers.py` | /api/projects 응답 검증 — 키 동일, fixture만 정합 |

- 무변경(키 "projects" 보존): `main.py`, `api/routers/projects.py`, `api/routers/print.py`, `app/front/**`.
- `persona/_meta.yaml`의 `projects.categories`는 **유지**(loader가 계속 카테고리 검증). persona/projects/ 디렉토리는 비워져 제거.

## Execution

### Phase 1 — showcase 배치 (curator)

- **Status**: DONE
- 13개 `git mv` → `products/{stem}/showcase.md` + `org` 주입(type/id/category/status/visible/stack/thumbnail/links.repo·본문 보존) + 신규 디렉토리 7개 생성. persona/projects/ 제거. **커밋 안 함**(admin atomic).

### Phase 2 — loader/map/jobs 재배선 (BE)

- **Status**: DONE
- loader가 `products/*/showcase.md` glob 로드(dict 키 `"projects"` 유지) + 그래프 빌더 `showcase.md` 제외 + `build_persona_map` + inputs/main_job 주석 + test fixture. pytest green. **커밋 안 함.**

### Phase 3 — 검증 + atomic 커밋 (admin)

- **Status**: DONE (커밋 `7548a67`)
- admin pytest 게이트 **262 passed**. `/api/projects` totalCount 6(visible)·필드 동일. `_map.md` 재빌드(projects 13, products/{slug}/showcase 링크). 그래프 빌더 showcase 제외 → **violations 34(전부 L2)=baseline, false-positive 0 유지**(노드 304, projects 13). product_doc_pipeline showcase-only 면제 → **28err→0**. → 단일 atomic 커밋.

## Pre-deploy Check

- [x] report-only 유지(enforcement = WORK-007)
- [x] dict 키 "projects" 보존 → API/FE/print 무변경 확인
- [x] persona/projects/ 완전 제거, products/{x}/showcase.md 13개 존재
- [x] pre-commit 훅(_map.md 빌드) 통과 — 마이그레이션이 atomic이라 중간 깨짐 없음

## Rollback

- 단일 커밋이므로 revert 1회로 원복. report-only라 서비스 로직 영향은 loader 경로뿐.

## Done Criteria

- [x] 13개 showcase가 `products/{x}/showcase.md`로 이동 + org 주입(type/id/thumbnail/repo 보존)
- [x] loader가 `products/*/showcase.md` 로드, 키 "projects" 유지, 카테고리 검증 정상
- [x] 그래프 빌더 showcase 제외 → L2 false-positive 0 유지(잔존 34 불변)
- [x] build_persona_map·inputs·main_job·test fixture 정합, pytest green(262 passed)
- [x] `/api/projects`·블로그 `/projects` 동작, _map.md 재빌드 정상
- [x] 30-work/README·log 갱신(이 task)

## Open Issues

- **product-as-graph-node 정식화(deferred)**: showcase를 블로그 그래프 노드로 띄우려면(D-017) stem이 아닌 **디렉토리명 기반 식별자**가 필요(모든 showcase.md는 stem 동일). 현재는 그래프 스캔에서 제외해 baseline만 보존. type=product 부여 + dir-identity 빌더 변경은 **SPEC-002 후속**으로 WORK-007(enforcement) 전에 게이트. → SPEC-002 §OQ 추가 제안.
- nexus org=company는 확신 낮음(admin 2026-06-30 확정). 추후 정정 시 frontmatter 1줄.

## Related

- Spec: [[spec-001-directory-structure|KDEV-SPEC-001]]
- Work: [[work-003-knowledge-layer-scaffold|KDEV-WORK-003]]
