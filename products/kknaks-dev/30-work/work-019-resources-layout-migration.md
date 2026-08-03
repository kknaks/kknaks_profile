---
type: work
id: KDEV-WORK-019
title: "지식층 디렉토리 이관 — resources/ 신설과 「양식 원천」 명칭 전환"
status: todo
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
progress: 0
created_at: 2026-08-03
updated_at: 2026-08-03
tags:
  - product/kknaks-dev
  - doc/work
  - status/todo
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
| Status | todo |
| Progress | 0% |
| Branch/PR | (미정) |
| Blocker | 없음 |
| Next | P1 — 절대경로 전수 검사(OQ-2) 후 atomic 이동 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | done — DEC-018 D1~D9, OQ 2 |
| Design | kknaks | 해당 없음 | — |
| FE | kknaks | 해당 없음 — 열람 화면은 미발주다 | — |
| BE | kknaks | 로더·발행부 경로 | todo |
| QA | kknaks | 부팅·그래프·발행 회귀 | todo |
| Ops | kknaks | 배포 후 부팅 확인 | todo |

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

- **Status**: TODO
- **설명**: 파일 이동과 코드 수정을 **한 커밋**에 넣는다. 여기까지가 이 발주의 위험 전부다.
- **작업**:
  - [ ] **선행: 절대경로 전수 검사**(DEC-018 OQ-2) — 노트 본문에 `reference/`·`permanent/` 를 적어 둔 곳이 있는지. 위키링크는 stem 이라 무관하지만 본문 문자열은 안 따라간다
  - [ ] `git mv` — 이동표대로. 각 디렉토리 `README.md` 포함
  - [ ] `reports/*.md` → `products/ax-knowledge-graph/30-work/reports/`
  - [ ] `persona_loader.py` — 로드 경로 2곳 · `_auto_enrich_note` 의 reference 경로 · `_load_permanent_notes` 의 훑는 디렉토리 목록
  - [ ] `apply/plan.py` — `ALLOWED_PREFIXES` · `LAYER_PREFIX` · **상위/하위 삼킴 방어 분기 제거**(형제가 되면 불필요)
  - [ ] `agent.md` — 경로표 4행 · 「지식층 읽기범위」의 `archive` 경로 · **`downloads/` 선언 추가**
  - [ ] 테스트 픽스처 경로
- **검증**:
  - [ ] `load_persona` 가 정상이고 **노드 수가 이동 전과 같다**
  - [ ] 그래프 ERROR 0 · WARN 0 — 이동 전과 동일
  - [ ] `layer` 판정이 안 바뀐다 — `type` 에서 나오므로 폴더 무관(DEC-010 D3)
  - [ ] 발행부가 새 경로를 허용하고 **옛 경로를 거부한다**
  - [ ] `resources/synthesis/` 로 가야 할 문서가 `resources/concept/` 아래면 위반으로 잡힌다
  - [ ] `git log --follow` 로 이동 전 이력이 따라온다
  - [ ] 전체 테스트 통과
- **완료 증거**: 미작성

### Phase 2 — 문서 정합 (경로)

- **Status**: TODO
- **설명**: 규칙과 템플릿이 새 경로를 가리키게 한다. 코드가 먼저 맞은 뒤라 문서만 따라가면 된다.
- **작업**:
  - [ ] `rules/knowledge-note-pipeline.md` — 4층 경로 · `archive` 위치
  - [ ] `templates/knowledge/` 4개(`idea`·`reference`·`concept`·`permanent`) — 저장 위치 문구
  - [ ] `agent.md` 의 지식노트 표 4행 (P1 에서 같이 했으면 확인만)
- **검증**:
  - [ ] 레포 전체에서 `reference/`·`permanent/` 를 **경로로** 가리키는 문서가 없다 (과거 기록·개정 노트는 제외)
  - [ ] `product_doc_pipeline --strict` 0 errors
- **완료 증거**: 미작성

### Phase 3 — 「양식 원천」 명칭 전환

- **Status**: TODO
- **설명**: `SoT` 를 **데이터가 어디 사나** 한 뜻으로 좁힌다. 양식을 정의하는 문서는 「양식 원천」으로 부른다(DEC-018 D8).
- **작업**:
  - [ ] `templates/knowledge/` 4개 · `templates/persona/` 3개 · `templates/product/showcase.md` 등 **양식을 정의하는 문서**의 문구
  - [ ] `rules/knowledge-note-pipeline.md:155` · `rules/product-doc-pipeline.md`
  - [ ] `agent.md` 의 *"이 문서들이 형식의 SoT다"*
  - [ ] **데이터 SoT 쪽은 안 건드린다** — `40-architecture/database`·DEC-009/012 는 그대로 `SoT`
- **검증**:
  - [ ] `templates/**` 에서 `SoT` 라는 말이 사라졌다
  - [ ] `40-architecture/database` 의 `SoT` 는 그대로다
  - [ ] 한 문서 안에서 두 뜻이 섞이지 않는다
- **완료 증거**: 미작성

### Phase 4 — 배포 + 부팅 확인 (Ops)

- **Status**: TODO
- **설명**: 서버가 `reset --hard` 로 새 구조를 받는다. **부팅이 되는지가 이 발주의 유일한 운영 관측**이다.
- **작업**:
  - [ ] 머지 → 배포
  - [ ] 서버 부팅 로그 확인
- **검증**:
  - [ ] 서버 `load_persona` 성공 — 실패하면 사이트가 옛 데이터를 서빙하며 조용히 멎는다
  - [ ] `/api/notes`·`/api/graph` 응답이 이동 전과 같다
  - [ ] `/download/*` 가 여전히 살아 있다 (`downloads/` 무변경 확인)
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 이동 전후 **노드 수·그래프 위반 수가 같다**
- [ ] `persona/`·`products/` 를 건드리지 않았다 — `git diff --stat` 으로 확인
- [ ] `downloads/` 가 그대로다 (지우면 DeskDeck 다운로드가 죽는다)
- [ ] 승인 대기 중인 큐 항목이 없다 — 발행 계획이 옛 경로를 담고 있으면 배포 후 `PATH_NOT_ALLOWED` 로 실패한다
- [ ] 로컬 Obsidian 볼트에서 링크가 살아 있는지 눈으로 확인

## Rollback

- **P1** — `git revert`. 이동과 코드가 한 커밋이라 되돌리면 원상태다. **이것이 atomic 으로 묶은 두 번째 이유다.**
- **P2·P3** — 문서만이라 개별 revert 가능.
- **P4** — 서버는 `reset --hard origin/main` 이라 revert 를 머지하면 따라온다.
- 부분 revert 시 영향: **P1 만 되돌리면 P2·P3 문서가 없는 경로를 가리킨다.** 되돌릴 땐 P1~P3 을 함께 본다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] SPEC-001 v0.0.6 · SPEC-005 v0.0.4 의 레이아웃이 실제와 일치한다.
- [ ] 레포에서 `permanent/` 가 **경로로** 쓰이는 곳이 없다.
- [ ] `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **`_meta.yaml` 의 `notes.clusters` 잔재.** `reference/` 가 flat 이 된 뒤로 아무도 안 읽는데 남아 있다. 이 발주 범위 밖이지만 같이 지울지는 P2 에서 판단한다.
- **`resources/synthesis/` 가 빈 채로 생긴다.** synthesis 층이 0건이라 디렉토리와 `README.md` 만 만들어진다. 빈 폴더를 미리 만들지 말자는 의견도 가능하나, **층이 있는데 자리가 없으면 첫 문서를 어디 둘지 또 물어야 한다.**
- **승인 큐에 저장된 발행 계획이 옛 경로를 담고 있을 수 있다.** `apply_plans.file_actions` 는 JSONB 로 박제된다 — 배포 전에 대기 항목이 없어야 한다. Pre-deploy Check 에 넣었다.

## Related

- SPEC: frontmatter `links.specs` 참조
- 선례: [[work-004-migrate-projects|KDEV-WORK-004]] — `projects → products/showcase` 를 atomic 하게 처리했다
