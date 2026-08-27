---
type: work
id: KDEV-WORK-002
title: "검증기 정교화 (code-fence 스킵 · navigational 제외 · orphan 범위)"
status: done
product: kknaks-dev
work_type: refinement
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
  works:
    - "[[work-001-graph-builder-validator|KDEV-WORK-001]]"
  releases: []
  related: []
---

# 검증기 정교화 (code-fence 스킵 · navigational 제외 · orphan 범위)

WORK-001 검증이 뱉은 위반 165개가 전부 false positive였다. 검증기를 정교화해 **진짜 위반만 남긴다**(목표: 노이즈 0). 여전히 **report-only** — enforcement는 WORK-007.

> 비목표: enforcement ON(WORK-007), 디렉토리 이동(WORK-004~006). 데이터 파일 자체는 안 고친다 — 검증기 로직만 정교화.

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-002-graph-schema|KDEV-SPEC-002]], [[spec-004-graph-validation|KDEV-SPEC-004]]
- Depends on work: [[work-001-graph-builder-validator|KDEV-WORK-001]] (검증기·`_graph.json` 기반)
- Follow-up work: WORK-003(지식층 scaffold)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | refinement |
| Owner | profile-be |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph (커밋 0014790) |
| Blocker | - |
| Next | WORK-003 지식층 scaffold (L5 실제 orphan은 지식 노드 채운 뒤 재-probe) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| BE | profile-be | 빌더/검증기 로직 정교화 + 테스트 | done |
| QA | admin | probe 재현(위반 감소) + pytest 게이트 | done (260 passed) |

## Scope

포함 (admin 승인된 3개 규칙):
- **① code-fence/inline-code 내 `[[]]` 스킵** — ` ```...``` `·`` `...` `` 안의 `[[stem]]`은 엣지로 잡지 않는다 (문법 설명 prose 오탐 L1=11 해소).
- **② navigational 노드 제외** — 그래프 노드 자격 = frontmatter `type` 보유. `type` 없는 `README`/`log`/`privacy`/`support`는 노드에서 제외 (L2=154 해소).
- **③ orphan(L5) 범위 한정** — orphan 검사를 지식 노드(`reference`/`permanent`/`post`/`product`)만 대상. `idea`/그 외(daily·algorithms·career 등)는 제외 (L5=196 노이즈 제거).

제외:
- enforcement(ERROR/fail-fast/CI) → WORK-007
- 데이터 파일 수정(디렉토리 이동·링크 정규화) → WORK-004~006
- code-fence 대신 "문서 예시 escape"로 가는 안 (택일: **빌더 스킵 채택**)

## Code Surface

| 경로 후보 | 설명 |
|---|---|
| `app/back/core/wikilinks.py` | code-fence/inline 영역 검출 후 그 안의 `[[]]` 스킵 |
| `app/back/core/graph.py` | navigational 노드 제외(node 자격=type 보유), L5 orphan 대상 type 한정 |
| `app/back/service/persona_loader.py` | 노드 수집 시 navigational 제외 반영 (필요 시) |
| `app/back/tests/test_wikilinks.py`·`test_graph.py` | code-fence 스킵·navigational 제외·orphan 범위 테스트 |

- Domain/schema note: DB 안 건드림. 검증기 로직만.

## Execution

### Phase 1 — code-fence/inline `[[]]` 스킵

- **Status**: DONE
- **설명**: 문서가 문법 설명용으로 적은 코드블록/인라인 내 `[[stem]]`을 엣지에서 제외.
- **작업**:
  - [x] 본문 파싱 시 ` ``` ` fenced block + `` ` `` inline span 영역 제외 후 `[[]]` 추출
- **검증**:
  - [x] probe: L1 dead link 12건(prose 예시) → 0
  - [x] 실제 본문 링크(코드블록 밖)는 그대로 잡힘
- **완료 증거**: `app/back/core/wikilinks.py`에 `FENCED_CODE_RE`/`INLINE_CODE_RE`+`_strip_code()` 추가, `extract_wikilinks()` 단일 추출 지점에 적용(build/knowledge/validate 자동 반영). `test_wikilinks` inline/fenced skip + 코드 밖 회귀 green. probe L1 12→0, 본문 링크 회귀 0. (리포트 PLAN-003-T-004 P1)

### Phase 2 — navigational 노드 제외

- **Status**: DONE
- **설명**: frontmatter `type` 없는 README/log/privacy/support를 그래프 노드에서 제외.
- **작업**:
  - [x] 노드 자격 = frontmatter `type` 보유로 한정 (없으면 노드 아님)
- **검증**:
  - [x] probe: L2 154건 → 34건 (잔존 34 = `v1_0_1-` 아카이브 사본 ↔ live 가 같은 frontmatter `id` 공유 — false-positive 아님, 아카이브 설계 이슈로 이월)
  - [x] 기존 지식 노드 수 회귀 없음 (노드 310→302, navigational 8개만 제외)
- **완료 증거**: `app/back/service/persona_loader.py` `_build_graph_nodes()`에서 `node.get("type")` 없으면 `continue`. persona notes는 항상 type 보유 → 무영향. `test_loader::TestGraphNodeQualification` green. probe L2 154→34, 노드 310→302. (리포트 PLAN-003-T-004 P2)

### Phase 3 — orphan(L5) 범위 한정

- **Status**: DONE
- **설명**: orphan WARN을 지식 노드(reference/permanent/post/product)만 대상.
- **작업**:
  - [x] L5 검사 대상 type을 지식 노드로 한정 (idea·daily·algorithms·career 제외)
- **검증**:
  - [x] probe: L5 196건 → 0 (노이즈 제거). 주의: L5=0 은 "orphan 없음"이 아니라 지식 노드(reference/permanent/post/product)가 레포에 아직 0개(WORK-003 대기)라 검사 대상이 없는 상태 — 지식층 채운 뒤 재-probe 시 실제 orphan 노출 예상.
- **완료 증거**: `app/back/core/graph.py`에 `KNOWLEDGE_NODE_TYPES = {reference, permanent, post, product}` 신설(`idea` 제외), `validate_graph` L5 루프가 비지식 노드 skip. `test_graph` green. probe L5 196→0. (리포트 PLAN-003-T-004 P3)

### Phase 4 — SPEC 환류

- **Status**: DONE
- **설명**: SPEC-002/004 §7 OPEN 메모를 rule로 확정 (환류 제안 → product-curator 반영).
- **작업**:
  - [x] SPEC-002 §5: code-fence 스킵 rule 확정. SPEC-004 §4: navigational 제외 + orphan 범위 rule 확정. (반영 = @product-curator, PLAN-003-T-005)
- **검증**:
  - [x] 검증 재실행: 남은 위반이 전부 "진짜"인지 admin과 확인 — false-positive(L1 prose/L2 navigational/L5 비지식) 0 달성, 잔존 L2=34 는 아카이브 id 충돌(설계 이슈)로 분류·이월.
- **완료 증거**: SPEC-002 §5/§7, SPEC-004 §4/§7 rule 확정 + OPEN 메모 해소, L2=34 신규 OPEN 추가 — @product-curator PLAN-003-T-005 반영.

## Pre-deploy Check

- [x] 여전히 **report-only** (enforcement 미적용 — ERROR/fail-fast/CI 는 WORK-007)
- [x] 실제 본문 링크·지식 노드 회귀 없음 (260 passed, persona notes _edges 289→289 무변경)

## Rollback

- 검증기 로직 변경이라 이전 커밋으로 revert 가능. report-only라 서비스 영향 0.

## Done Criteria

- [x] 모든 Phase DONE (1~4)
- [x] probe: false-positive(L1 prose / L2 navigational / L5 비지식 orphan) 0
- [x] pytest green (260 passed) + admin probe 재현
- [x] SPEC-002/004 환류 제안 → product-curator 반영 (PLAN-003-T-005)
- [x] 30-work/README·log 갱신 (PLAN-003-T-005)

## Open Issues

- **L2=34 잔존 — 아카이브 사본 id 충돌**: `v1_0_1-X`(아카이브 사본)가 live `X`와 같은 frontmatter `id`(`MRT-*`)를 공유해 alias/id 전역유일 위반. 그래프 자체는 정상(정렬상 live로 resolve), 깨진 링크 아님 — 유일성 경고일 뿐. 근본 원인 = `version-cutoff` skill 이 파일명·wikilink 에만 버전 prefix 를 붙이고 `id` 는 원본 그대로 둠. 후속 결정(택일): (1) version-cutoff 가 frontmatter `id` 에도 버전 prefix / (2) 검증기가 `archived` 노드를 id/alias 유일성 검사에서 면제. → SPEC-004 §7 신규 OPEN, WORK-004~006 또는 별도.

## Related

- SPEC: [[spec-002-graph-schema|KDEV-SPEC-002]], [[spec-004-graph-validation|KDEV-SPEC-004]]
- Work: [[work-001-graph-builder-validator|KDEV-WORK-001]]
