---
type: work
id: KDEV-WORK-001
title: "그래프 빌더 수술 + 검증기 (report-only)"
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
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions: []
  specs:
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works: []
  releases: []
  related: []
---

# 그래프 빌더 수술 + 검증기 (report-only)

기존 그래프 빌더가 실제 링크 형태(`[[stem|alias]]`·`[[folder/stem]]`)를 파싱하도록 고치고, products까지 그래프에 포함시키고, L1~L6 검증기를 **report-only(warn)** 로 추가한다. 이 work는 **enforcement를 켜지 않는다** (그건 WORK-007).

> 비목표: 디렉토리 이동·파일 정리(WORK-002~006), enforcement ON(WORK-007), 시각화(WORK-008/009).

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-002-graph-schema|KDEV-SPEC-002]], [[spec-004-graph-validation|KDEV-SPEC-004]]
- Depends on work: 없음 (첫 work)
- Parallel work: 없음
- Follow-up work: WORK-002(검증기 정교화 — 이 검증기의 report 출력을 정교화해 false-positive 제거)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | profile-be |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph (커밋 abcfbc4) |
| Blocker | - |
| Next | WORK-002 검증기 정교화 (false-positive 정교화) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| BE | profile-be | 빌더 regex·loader·검증기·_graph.json | done |
| QA | admin | probe 재현 + pytest 게이트 | done (255 passed) |

## Scope

포함:
- `wikilinks.py` regex가 `[[stem]]`·`[[stem|alias]]`·`[[folder/stem]]` 파싱
- alias 인덱스 (frontmatter `aliases` → `[[id]]` resolve)
- `persona_loader`가 products 포함 (현재 persona만)
- L1~L6 검증 함수 (report-only/warn — 부팅·커밋 차단 안 함)
- `_graph.json` 산출 (nodes/edges[type,dir]/backlinks)

제외:
- enforcement(ERROR/fail-fast/pre-commit/CI) → WORK-007
- 실제 데이터 정리(충돌·링크 정규화·평문 links: 정리) → WORK-004~006 (마이그레이션과 lockstep)

## Code Surface

- Repo / module: `app/back`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/back/core/wikilinks.py` | regex 확장, alias 처리, 엣지 type/dir, 검증 함수 추가 |
| `app/back/service/persona_loader.py` | products 디렉토리 로드 포함 |
| `app/back/main.py` | 부팅 시 검증 호출(report-only 로그), `_graph.json` 산출 |
| `app/back/core/` (신규?) | 검증 모듈 분리 여부는 구현 판단 |
| `app/back/tests/` | regex·검증·로더 테스트 |

- Domain/schema note: DB 안 건드림. 파일 frontmatter가 SoT.

## Internal Interface Contract

- `_graph.json` 형태는 [[spec-002-graph-schema|KDEV-SPEC-002]] §4 Data Contract 기준. 최종 필드명은 이 work에서 확정(SPEC OQ 해소) 후 spec에 환류.
- 검증 함수 반환: 위반 리스트 `[{rule, level, node, detail}]` (정확한 시그니처는 구현 판단).

## Execution

### Phase 1 — wikilinks regex 확장 + alias

- **Status**: DONE
- **설명**: 실제 링크(`[[stem|alias]]`·`[[folder/stem]]`)를 파싱하고, frontmatter `aliases`로 `[[id]]` resolve.
- **작업**:
  - [x] `WIKILINK_RE`를 alias(`|`)·경로형(`/`)·대문자 허용하도록 확장, target=stem 추출
  - [x] frontmatter `aliases` 인덱스 구축 → `[[id]]`를 stem으로 resolve
  - [x] 엣지에 `type`(assoc 기본) 부여
- **검증**:
  - [x] probe: 기존 products 링크가 엣지로 잡힌다 (probe edges 301)
  - [x] `[[id]]`가 aliases로 resolve된다 (단위테스트; 실데이터엔 `aliases` frontmatter 0개라 latent)
- **완료 증거**: `core/wikilinks.py` `WIKILINK_RE`+`_parse_target()`가 `[[stem]]`·`[[stem|alias]]`·`[[folder/stem]]`을 동일 stem으로 정규화(대문자·`_`·`.` 허용, 공백 차단). alias/`[[id]]` resolve는 전체 노드 집합이 필요해 `core/graph.py` `build_alias_index`(=`aliases`+frontmatter `id`+stem 자기참조→canonical stem)로 분리. `build_graph`/`dead_links` 출력 shape 불변(`/api/notes/graph` 계약 보존). `tests/test_wikilinks.py` green.

### Phase 2 — persona_loader products 포함

- **Status**: DONE
- **설명**: 현재 persona만 읽는 로더가 products도 그래프에 포함.
- **작업**:
  - [x] products `*.md` 로드 + 노드화 (type 부여)
  - [x] 기존 persona 로드 회귀 없음
- **검증**:
  - [x] probe: products 노드가 그래프에 등장 (product 노드 145개)
  - [x] 기존 persona 테스트 green
- **완료 증거**: `persona_loader._build_graph_nodes()`가 persona notes(stem==id) + `products/**/*.md`를 stem→node로 결합, `_load_product_node()`가 frontmatter(type/id/title/up/aliases)+body+`archived` 마킹. 중복 stem은 L2로 수집·첫 항목 유지(report-only). 신규 키 `_nodes`/`_graph`/`_graph_violations`만 추가, 기존 `_edges`/`_backlinks` 무변경 → notes 라우트 회귀 0. 그래프 빌드 전체를 try/except로 감싸 부팅 영향 0. probe: product 노드 145개 그래프 등장, 전체 255 passed.

### Phase 3 — `up:` lineage + L1~L6 검증기 (report-only)

- **Status**: DONE
- **설명**: `up:` 오버레이로 lineage 엣지 마킹, L1~L6 검증을 warn 모드로.
- **작업**:
  - [x] `up:`의 stem을 lineage+dir로 마킹 (본문 `[[]]` 부분집합 전제)
  - [x] L1(dead)·L2(스키마/유일)·L3(오버레이)·L4(방향)·L5(orphan)·L6(archive참조) 검증 함수
  - [x] **report-only**: 위반을 로그/리포트로 출력, 부팅·커밋 차단 안 함
- **검증**:
  - [x] probe: 현재 레포에서 검증 실행 → 위반 리포트 출력 (차단 없이)
  - [x] 리포트가 WORK-002 작업목록으로 쓸 수 있는 형태
- **완료 증거**: `core/graph.py` `build_knowledge_graph()`가 body `[[]]`→assoc, `up:` 마킹 타겟은 lineage+`dir="up"`로 승격(resolve 안 되는 타겟은 엣지 제외·L1 별도 보고). `validate_graph()`가 L1~L6 검증(절대 raise 안 함). probe 위반: `ERROR=165 (L1=11, L2=154), WARN=196 (L5=196)`, L3/L4/L6=0(up/archived 데이터 미존재 latent). L1=11은 전부 문법 설명용 prose 예시(실제 깨진 링크 아님), L2=154는 navigational/legal 파일(README/log/privacy/support+중복 stem) → WORK-002 worklist.

### Phase 4 — `_graph.json` 산출

- **Status**: DONE
- **설명**: nodes/edges/backlinks를 `_graph.json`으로 산출 (시각화·검증 소비).
- **작업**:
  - [x] `_graph.json` 산출 (부팅 시 + 빌드)
  - [x] 최종 필드명 확정 → SPEC-002에 환류
- **검증**:
  - [x] probe: `_graph.json`에 nodes/edges(type,dir)/backlinks 포함
- **완료 증거**: `main.py` `load_all()`→`_report_graph()`가 위반 요약 WARN 로그 + `_graph.json` best-effort write(읽기전용 FS 실패 무시). `config.graph_json_path()`(env `GRAPH_JSON_PATH`, 기본 repo 루트). `.gitignore`에 `_graph.json` 추가(부팅 derive 산출물). probe: nodes 309 / edges 301 / backlink-target 94, `_graph.json` 109KB(keys=nodes/edges/backlinks). 확정 필드 → SPEC-002 §4 환류.

## Pre-deploy Check

- [x] 검증기가 **report-only** 임을 확인 (부팅 fail-fast 미적용 — 기존 서버 영향 없음)
- [x] 기존 `/` 블로그 라우트·persona 로드 회귀 없음 (255 passed, `_edges`/`_backlinks` 무변경)

## Rollback

- 검증 함수·products 로드는 신규 추가라 호출부 미등록으로 비활성 가능.
- regex 변경은 기존 테스트로 회귀 확인.

## Done Criteria

- [x] 모든 Phase DONE
- [x] SPEC-002/004 계약(파싱·엣지·검증·_graph.json)이 검증 항목에 반영
- [x] pytest green + admin probe 재현 (255 passed, abcfbc4)
- [x] `30-work/README.md`·`log.md` 갱신 (PLAN-003-T-003)
- [x] `_graph.json` 필드 확정분을 SPEC-002에 환류 (PLAN-003-T-003)

## Open Issues

- **해소**: `_graph.json` 확정 필드 = `nodes[id,type,title,archived]` / `edges[source,target,type,dir]` / `backlinks{stem:[stem]}`. 검증 함수 시그니처 = `validate_graph(nodes, duplicate_stems=None) -> list[{rule,level,node,detail}]`. → SPEC-002 §4·§7 환류 완료.
- **해소**: 검증 모듈은 `core/graph.py`로 분리(alias 인덱스·`build_knowledge_graph`·`validate_graph`). `wikilinks.py`는 regex/파싱 한정.
- **이월(WORK-002)**: probe 검증 false-positive 정교화 — prose 예시 L1=11(code-fence 스킵 검토), navigational L2=154(README/log 노드 제외 검토), orphan L5=196(daily 제외 범위). SPEC-002/004 §7 OQ에 메모.

## Related

- SPEC: [[spec-002-graph-schema|KDEV-SPEC-002]], [[spec-004-graph-validation|KDEV-SPEC-004]]
