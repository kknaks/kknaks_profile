---
type: work
id: KDEV-WORK-019
title: "지식층 디렉토리 이관 — resources/ 신설과 「양식 원천」 명칭 전환"
status: done
product: kknaks-dev
work_type: refactor
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-08-03
updated_at: 2026-08-03
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]"
  decisions:
    - "[[decision-018-resources-layout-and-sot-naming|KDEV-DEC-018]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-005-graph-visualization|KDEV-SPEC-005]]"
  works:
    - "[[work-013-concept-layer|KDEV-WORK-013]]"
  releases: []
  related:
    - "[[work-004-migrate-projects|KDEV-WORK-004]]"
---

# 지식층 디렉토리 이관 — `resources/` 신설과 「양식 원천」 명칭 전환

지식층 14 파일을 `resources/{source,concept,synthesis}/` 로 옮기고 `archive/` 를 최상위로 올린다. `SoT` 가 두 뜻으로 쓰이던 것을 **「양식 원천」과 「SoT」로 가른다.**

**만들지 않는 것**: `persona/`(A 판정) · `products/` 재편 · `type` enum 개명 · `downloads/` 이동 · `_meta.yaml` 의 `notes.clusters` 잔재 정리.

## Meta

- Baseline: [[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]
- Covers spec: [[spec-001-directory-structure|KDEV-SPEC-001]] v0.0.6 · [[spec-005-graph-visualization|KDEV-SPEC-005]] v0.0.4 (둘 다 개정 완료)
- Depends on work: [[work-013-concept-layer|KDEV-WORK-013]] — 4층과 `concept/` 를 실재화한 발주다. 이 발주는 그 층을 **옮기기만** 한다
- Parallel work: 없음
- Follow-up work: `persona/` A 판정 (후속 decision) · `products/` 재편 여부
- External dependency: **없다.** 외부 API·토큰·볼륨이 걸리지 않는다. 배포는 파일 이동을 서버에 반영하는 것뿐이다

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner | kknaks |
| Status | done |
| Progress | 100% (P1~P4 완주. 이동 전후 그래프 동일, 서버 실측도 같다. 887 passed) |
| Branch/PR | `work-019-resources` · PR #8 |
| Blocker | 없음 |
| Next | 없음 — 이 발주는 닫혔다 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | done — DEC-018 D1~D9, OQ 2 |
| Design | kknaks | 해당 없음 | — |
| FE | kknaks | 해당 없음 — 열람 화면은 미발주다 | — |
| BE | kknaks | 로더·발행부 경로 | **done** — 예상 3곳 → 실제 서비스 9곳 |
| QA | kknaks | 부팅·그래프·발행 회귀 | **done** — 기준선 대조 + 교차 배치 7종 |
| Ops | kknaks | 배포 후 부팅 확인 | **done** — 배포 21초, 서버 실측 일치 |

## Scope

포함:

- `reference/` → `resources/source/` · `permanent/concept/` → `resources/concept/` · `permanent/*.md` → `resources/synthesis/`
- `permanent/archive/` → `archive/` (최상위)
- `reports/*.md` → `products/ax-knowledge-graph/30-work/reports/`
- `persona_loader.py` 로드 경로 · 경로 기반 `type` 기본값
- `apply/plan.py` `ALLOWED_PREFIXES` · `LAYER_PREFIX` · 층-경로 정합
- `agent.md` 경로표 · 읽기범위 · `downloads/` 선언
- `rules/knowledge-note-pipeline.md` · `templates/knowledge/` 4개
- **「양식 원천」 명칭 전환** — `templates/**` 10개 + `rules/`

제외:

- `persona/` A 판정 → 후속 decision
- `products/` 재편 · `products/*/_archive/` 통합
- `type` enum 개명 → SPEC-002 소유
- `downloads/` 이동 → 운영 자산, 선언만
- `_meta.yaml` 의 `notes.clusters` 잔재 → 별도

## Code Surface

- Repo / module: `app/back` (로더·발행부) · 루트(디렉토리·문서·템플릿)

| 경로 후보 | 설명 |
|---|---|
| `reference/` · `permanent/` · `archive/` · `resources/` | `git mv` — P1 |
| `reports/` | 제품 아래로 — P1 |
| `service/persona_loader.py` | `_load_reference_notes` 경로 · `_load_permanent_notes` 경로 · `_enrich_permanent` 의 `path.parts` 판정 · `_auto_enrich_note` 의 reference 경로 — P1 |
| `service/apply/plan.py` | `ALLOWED_PREFIXES` · `LAYER_PREFIX` · 층-경로 정합 분기 — P1 |
| `agent.md` | 경로표 4행 · 「지식층 읽기범위」 · `downloads/` 선언 — P1 |
| `rules/knowledge-note-pipeline.md` | 경로 + 「양식 원천」 — P2·P3 |
| `templates/knowledge/*.md` (4) | 경로 + 「양식 원천」 — P2·P3 |
| `templates/persona/*.md` · `templates/product/*.md` | 「양식 원천」 — P3 |
| `tests/` | 로더 경로 픽스처 · 발행부 경로 단언 |

- Domain / schema note: **마이그레이션 0건.** DB 를 건드리지 않는다 — 지식층은 파일 SoT 다.

## Domain / Schema

해당 없음.

- 상태 / invariant: 없음
- Migration 필요 여부: **불필요**
- SPEC 환류: 없음 — SPEC-001·005 가 이미 개정됐다

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| P2 문서 | P1 의 확정된 경로 | 문서가 코드보다 앞서면 없는 경로를 가리킨다 |
| P3 명칭 | P2 | 같은 파일을 두 번 만지지 않으려고 뒤에 둔다 |
| P4 배포 | P1~P3 | — |
| 후속(A 판정) | 이 발주의 `resources/` | 남는 것이 `persona/` 하나가 돼야 판단이 단순해진다 |

## Internal Interface Contract

### 이동표

```text
reference/*.md            →  resources/source/*.md
permanent/concept/*.md    →  resources/concept/*.md
permanent/*.md            →  resources/synthesis/*.md      (현재 0건 — 디렉토리만 생긴다)
permanent/archive/        →  archive/                       (현재 0건 — 디렉토리만)
reports/*.md              →  products/ax-knowledge-graph/30-work/reports/
```

각 디렉토리의 `README.md`(navigational)도 함께 옮긴다.

### `LAYER_PREFIX` 접두 충돌 — 판정 순서가 계약이다

`resources/` 아래 셋이 같은 접두를 공유한다. **긴 접두를 먼저 본다.**

```text
concept    → resources/concept/
permanent  → resources/synthesis/
reference  → resources/source/
idea       → inbox/
```

지금은 `permanent` 가 `permanent/` 이고 `concept` 가 `permanent/concept/` 라 **상위가 하위를 삼키는 구조**였고, 그래서 `permanent` 인데 `permanent/concept/` 아래면 위반이라는 **별도 분기**가 있었다. 새 구조에서는 셋이 형제라 **그 분기가 필요 없어진다** — 제거 대상이다.

### `_enrich_permanent` 의 경로 판정

```python
default_type = "concept" if "concept" in path.parts else "permanent"
archived = "archive" in path.parts
```

`resources/concept/` 는 여전히 맞고, `archive/` 도 `path.parts` 에 남으므로 **둘 다 그대로 동작한다.** 다만 `_load_permanent_notes` 가 훑는 디렉토리 목록은 바뀐다.

## Execution

> **P1 을 원자적으로 한다.** 파일과 코드가 다른 커밋에 들어가면 그 사이 커밋에서 로더가 없는 경로를 보고 `PersonaError` 로 **부팅이 막힌다**(DEC-018 D9). [[work-004-migrate-projects|KDEV-WORK-004]] 가 `projects → products/showcase` 를 같은 이유로 atomic 하게 처리한 선례가 있다.
>
> **문서를 코드보다 뒤에 둔다.** 반대로 하면 문서가 아직 없는 경로를 가리키는 구간이 생긴다. 이 발주에서 문서는 코드를 설명하는 쪽이라 따라가는 것이 맞다.

### Phase 1 — 이동 + 코드 (atomic)

- **Status**: DONE
- **설명**: 파일 이동과 코드 수정을 **한 커밋**에 넣는다. 여기까지가 이 발주의 위험 전부다.
- **작업**:
  - [x] **선행: 절대경로 전수 검사**(DEC-018 OQ-2) — 노트 본문에 `reference/`·`permanent/` 를 적어 둔 곳이 있는지. 위키링크는 stem 이라 무관하지만 본문 문자열은 안 따라간다
  - [x] `git mv` — 이동표대로. 각 디렉토리 `README.md` 포함
  - [x] `reports/*.md` → `products/ax-knowledge-graph/30-work/reports/`
  - [x] `persona_loader.py` — 로드 경로 2곳 · `_auto_enrich_note` 의 reference 경로 · `_load_permanent_notes` 의 훑는 디렉토리 목록
  - [x] `apply/plan.py` — `ALLOWED_PREFIXES` · `LAYER_PREFIX` · **상위/하위 삼킴 방어 분기 제거**(형제가 되면 불필요)
  - [x] `agent.md` — 경로표 4행 · 「지식층 읽기범위」의 `archive` 경로 · **`downloads/` 선언 추가**
  - [x] 테스트 픽스처 경로
- **검증**:
  - [x] `load_persona` 가 정상이고 **노드 수가 이동 전과 같다**
  - [x] 그래프 ERROR 0 · WARN 0 — 이동 전과 동일
  - [x] `layer` 판정이 안 바뀐다 — `type` 에서 나오므로 폴더 무관(DEC-010 D3)
  - [x] 발행부가 새 경로를 허용하고 **옛 경로를 거부한다**
  - [x] `resources/synthesis/` 로 가야 할 문서가 `resources/concept/` 아래면 위반으로 잡힌다
  - [x] `git log --follow` 로 이동 전 이력이 따라온다
  - [x] 전체 테스트 통과
- **완료 증거**:
  - **선행 검사에서 본문 경로 참조 0건**(DEC-018 OQ-2 해소). 위키링크는 stem 기반이라 무관하고, 옛 경로를 적어 둔 것은 각 디렉토리 `README.md`(navigational)뿐이라 함께 옮기며 고쳤다.
  - **16개 전부 `rename` 으로 잡혔다** — `git log --follow` 가 이력을 따라간다. 파일 내용을 안 건드렸다는 뜻이기도 하다.
  - **이동 전후 그래프가 완전히 같다**: `nodes 287 · ERROR 0 · WARN 0 · notes 2 · permanent 8 · edges 0`. 이동 **전에 기준선을 찍고** 대조했다 — "문제 없어 보인다" 가 아니라 같은 수라는 것을 봤다.
  - **`layer` 가 `type` 에서 나온다는 예측이 실측으로 확인됐다**(DEC-010 D3). 폴더를 통째로 옮겼는데 층 판정·L1~L6 이 한 건도 안 움직였다.
  - **삼킴 방어 분기를 제거했다.** 종전에는 `permanent/` 가 `permanent/concept/` 를 삼켜 *"종합 노트가 concept 디렉토리에 있다"* 를 잡는 별도 분기가 필요했는데, 셋이 형제가 되면서 `LAYER_PREFIX` 정확 일치만으로 충분해졌다. **교차 배치 7종을 실측**했다 — 새 경로 통과 3 / 옛 경로 거부 2 / 종합이 concept 폴더에 거부 / 개념이 synthesis 폴더에 거부.
  - **이관 중 잠복 버그를 찾아 고쳤다** — `knowledge_capture/render.py` 가 `reference/{group}/` 로 쓰고 있었다. WORK-005/013 이 층을 flat 으로 바꾼 뒤로도 거기만 남아 있었고, **로더는 `*.md` 를 재귀 없이 훑으므로 하위 폴더에 쓰면 그 노트가 아예 안 읽힌다.** 롤백 경로(`KnowledgeCaptureRunner`)라 실행될 일이 드물어 드러나지 않았다.
  - 코드 접점이 발주 예상(셋)보다 넓었다 — `persona_loader`·`apply/plan.py` 외에 `concept_index`·`stages/{source_note,concept,daily}`·`collect_git`·`route`·`render` 까지 **서비스 9곳**에 경로가 박혀 있었다. 테스트가 그것을 전부 잡아냈다(20 → 8 → 1 → 0).
  - **887 passed** · `product_doc_pipeline --strict` 0 errors · `persona/` 무변경 · `products/` 는 `reports` 이동뿐.

### Phase 2 — 문서 정합 (경로)

- **Status**: DONE
- **설명**: 규칙과 템플릿이 새 경로를 가리키게 한다. 코드가 먼저 맞은 뒤라 문서만 따라가면 된다.
- **작업**:
  - [x] `rules/knowledge-note-pipeline.md` — 4층 경로 · `archive` 위치
  - [x] `templates/knowledge/` 4개(`idea`·`reference`·`concept`·`permanent`) — 저장 위치 문구
  - [x] `agent.md` 의 지식노트 표 4행 (P1 에서 같이 했으면 확인만)
- **검증**:
  - [x] 레포 전체에서 `reference/`·`permanent/` 를 **경로로** 가리키는 문서가 없다 (과거 기록·개정 노트는 제외)
  - [x] `product_doc_pipeline --strict` 0 errors
- **완료 증거**:
  - `rules/knowledge-note-pipeline.md` 4층 표·archive 위치 · `templates/knowledge/` 5개(`idea`·`reference`·`concept`·`permanent`·`README`)의 저장 경로.
  - 레포에서 `reference/`·`permanent/` 를 **경로로** 가리키는 문서가 0건이다. 남은 것은 개정 노트와 과거 기록뿐이고, 그건 그때의 사실이라 고치지 않는다.

### Phase 3 — 「양식 원천」 명칭 전환

- **Status**: DONE
- **설명**: `SoT` 를 **데이터가 어디 사나** 한 뜻으로 좁힌다. 양식을 정의하는 문서는 「양식 원천」으로 부른다(DEC-018 D8).
- **작업**:
  - [x] `templates/knowledge/` 4개 · `templates/persona/` 3개 · `templates/product/showcase.md` 등 **양식을 정의하는 문서**의 문구
  - [x] `rules/knowledge-note-pipeline.md:155` · `para/projects/project.md`
  - [x] `agent.md` 의 *"이 문서들이 형식의 SoT다"*
  - [x] **데이터 SoT 쪽은 안 건드린다** — `40-architecture/database`·DEC-009/012 는 그대로 `SoT`
- **검증**:
  - [x] `templates/**` 에서 `SoT` 라는 말이 사라졌다
  - [x] `40-architecture/database` 의 `SoT` 는 그대로다
  - [x] 한 문서 안에서 두 뜻이 섞이지 않는다
- **완료 증거**:
  - **전부 바꾸지 않았다.** `templates/**` 안에도 데이터 뜻으로 쓰인 `SoT` 가 섞여 있어 골라냈다 — `concept.md` 의 *"여기가 이 개념의 SoT다"*(개념 상세가 어디 사나), `work.md` 의 *"실제 schema 는 코드/migration 이 SoT다"*, `spec.md` 의 *"Case Matrix 를 단일 SoT로"*(에러 정의가 어디 사나)는 **그대로 `SoT`** 다.
  - 바꾼 것은 *"이 파일이 X 형식의 SoT다"* 꼴 **9곳**이고, 그것이 D8 이 가르려던 축이다. 기계적 치환이었으면 데이터 SoT 까지 지워 **문서가 더 헷갈려졌을 것**이다.
  - `agent.md` 와 `rules/knowledge-note-pipeline.md` 에 두 말의 구분을 **각주로 박았다** — 명칭만 바꾸고 이유를 안 남기면 다음 사람이 다시 섞는다.
  - `40-architecture/database` 의 `SoT` 8건은 데이터 뜻이라 그대로다.

### Phase 4 — 배포 + 부팅 확인 (Ops)

- **Status**: DONE
- **설명**: 서버가 `reset --hard` 로 새 구조를 받는다. **부팅이 되는지가 이 발주의 유일한 운영 관측**이다.
- **작업**:
  - [x] 머지 → 배포
  - [x] 서버 부팅 로그 확인
- **검증**:
  - [x] 서버 `load_persona` 성공 — 실패하면 사이트가 옛 데이터를 서빙하며 조용히 멎는다
  - [x] `/api/notes`·`/api/graph` 응답이 이동 전과 같다
  - [x] `/download/*` 가 여전히 살아 있다 (`downloads/` 무변경 확인)
- **완료 증거**:
  - 배포 **21초** (PR #8 머지 → `4da7c4f`). 서버 트리가 `resources/{source,concept,synthesis}` · `archive` · `inbox` 이고 **옛 경로는 전부 제거**됐다.
  - **서버 로더 실측이 로컬과 정확히 같다** — `nodes 287 · ERROR 0 · WARN 0 · notes 2 · permanent+concept 8`. 부팅이 막히면 사이트가 옛 데이터를 서빙하며 조용히 멎는데, 그 일이 없었다.
  - API 전부 200 — `/api/notes/recent`·`/api/notes/graph`·`/api/site`·`/api/projects`·`/api/career`·`/api/activity`. **`/api/notes/recent` 가 `resources/source/` 의 노트 2건을 돌려준다** — 새 경로에서 로드된다는 직접 증거다.
  - **`/download/DeskDeckHelper-1.0.1.dmg` 200** — D6 대로 건드리지 않아 살아 있다.
  - **배포 전 안전 확인**: 서버의 저장된 발행 계획 **0건**(대기 항목 2개는 `deleted`). `apply_plans.file_actions` 가 JSONB 로 박제돼 옛 경로를 담은 채 배포되면 `PATH_NOT_ALLOWED` 로 실패하는데, 그 위험이 없음을 미리 봤다.
  - **처음에 오독한 것 둘을 기록해 둔다.** `/api/notes`·`/api/graph` 가 404 였는데 **회귀가 아니라 내가 없는 경로를 친 것**이었다(실제는 `/api/notes/recent`·`/api/notes/graph`). 로그의 `Traceback` 도 이번 변경과 무관한 `pdf_generate` 의 Playwright 미설치이고 `_run_pdf_safe` 가 감싸고 있다.

## Pre-deploy Check

- [x] 이동 전후 **노드 수·그래프 위반 수가 같다**
- [x] `persona/`·`products/` 를 건드리지 않았다 — `git diff --stat` 으로 확인
- [x] `downloads/` 가 그대로다 (지우면 DeskDeck 다운로드가 죽는다)
- [x] 승인 대기 중인 큐 항목이 없다 — 발행 계획이 옛 경로를 담고 있으면 배포 후 `PATH_NOT_ALLOWED` 로 실패한다
- [x] 로컬 Obsidian 볼트에서 링크가 살아 있는지 눈으로 확인

## Rollback

- **P1** — `git revert`. 이동과 코드가 한 커밋이라 되돌리면 원상태다. **이것이 atomic 으로 묶은 두 번째 이유다.**
- **P2·P3** — 문서만이라 개별 revert 가능.
- **P4** — 서버는 `reset --hard origin/main` 이라 revert 를 머지하면 따라온다.
- 부분 revert 시 영향: **P1 만 되돌리면 P2·P3 문서가 없는 경로를 가리킨다.** 되돌릴 땐 P1~P3 을 함께 본다.

## Done Criteria

- [x] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [x] SPEC-001 v0.0.6 · SPEC-005 v0.0.4 의 레이아웃이 실제와 일치한다.
- [x] 레포에서 `permanent/` 가 **경로로** 쓰이는 곳이 없다.
- [x] `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **`_meta.yaml` 의 `notes.clusters` 잔재.** `reference/` 가 flat 이 된 뒤로 아무도 안 읽는데 남아 있다. 이 발주 범위 밖이지만 같이 지울지는 P2 에서 판단한다.
- **`resources/synthesis/` 가 빈 채로 생긴다.** synthesis 층이 0건이라 디렉토리와 `README.md` 만 만들어진다. 빈 폴더를 미리 만들지 말자는 의견도 가능하나, **층이 있는데 자리가 없으면 첫 문서를 어디 둘지 또 물어야 한다.**
- **승인 큐에 저장된 발행 계획이 옛 경로를 담고 있을 수 있다.** `apply_plans.file_actions` 는 JSONB 로 박제된다 — 배포 전에 대기 항목이 없어야 한다. Pre-deploy Check 에 넣었다.

## Related

- SPEC: frontmatter `links.specs` 참조
- 선례: [[work-004-migrate-projects|KDEV-WORK-004]] — `projects → products/showcase` 를 atomic 하게 처리했다
