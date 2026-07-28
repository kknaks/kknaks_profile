---
type: work
id: KDEV-WORK-013
title: "concept 층 도입 — 4층 재편 · 검증 재정의 · 규칙/템플릿"
status: todo
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: —
  fe: —
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-003-knowledge-workflow|KDEV-SPEC-003]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works: []
  releases: []
  related: []
---

# concept 층 도입 — 4층 재편 · 검증 재정의 · 규칙/템플릿

`permanent/concept/`를 신설하고 그래프를 4층(`source`/`concept`/`synthesis`/`execution`)으로 재편한다. 층별 orphan 판정과 `up:` 방향 반전을 **report-only로 먼저 측정한 뒤** enforce로 넘긴다.

> 만들지 않는 것: 승인 파이프라인. 이 work가 끝나면 concept 노트를 **손으로라도** 쓸 수 있고, WORK-014/015가 그 위에 자동 유입을 얹는다.

## Meta

- Baseline: KDEV-BL-003
- Covers spec: KDEV-SPEC-001·002·003·004
- Depends on work: 없음
- Parallel work: WORK-012 (bridge 흡수 — 서로 독립)
- Follow-up work: WORK-014
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | — |
| Blocker | 없음 |
| Next | Phase 1 report-only 측정 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 층 정의·enforce 시점 판단 | todo |
| Design | — | UI 변경 없음 | — |
| FE | — | 변경 없음 (열람 표면은 후속) | — |
| BE | kknaks | 빌더·검증기·로더 | todo |
| QA | kknaks | report-only 측정·회귀 | todo |
| Ops | kknaks | enforce 전환·kill-switch | todo |

## Scope

포함:

- `permanent/concept/` 디렉토리 신설
- `layer` 축 도입 — `type`에서 도출해 `_graph.json` `nodes[].layer`에 담기
- type enum 재편: `concept` 추가, `note` 제거, `product` 정리
- rank 재정의 + **비교 연산자 반전**
- L2 type별 필수 필드(`concept`=`aliases`+`up`, `permanent`=`up`, `idea`=`up` 금지)
- L5 층별 orphan 판정 + `source` orphan을 **미소화 큐 지표**로 분리
- `rules/knowledge-note-pipeline.md` 신규
- `templates/knowledge/` 4종 (idea·reference·concept·permanent)
- 루트 디렉토리 README 개정 (`inbox/`는 "미정제만 보유")

제외:

- 승인 큐·게이트 (WORK-014·015)
- 트리 문서 렌더러 (후속 — SPEC-005)
- 발행 전 검증 훅 (WORK-015 Executor에서 이 검증기를 호출)
- `reference/` 157개 소급 정제 (범위 밖)
- `reference/` group 13종 정리 (범위 밖)

## Code Surface

- Repo / module: `app/back/core`, `app/back/service`, 레포 루트

| 경로 후보 | 설명 |
|---|---|
| `app/back/core/graph.py` | `ALLOWED_NODE_TYPES`·`KNOWLEDGE_NODE_TYPES`·`_TYPE_RANK` + L2/L4/L5 로직 |
| `app/back/service/persona_loader.py` | `permanent/concept/` 순회, `layer` 주입 |
| `app/back/tests/test_graph.py` · `test_graph_enforcement.py` | 층별 판정·rank 반전 테스트 |
| `app/scripts/install_hooks.sh` | pre-commit 트리거에 `permanent`·`inbox` 추가 (기존 구멍) |
| `permanent/concept/` | 신설 (README 포함) |
| `rules/knowledge-note-pipeline.md` | 신규 — `product-doc-pipeline.md`의 대칭 |
| `templates/knowledge/*.md` | 신규 4종 |
| `inbox/README.md` · `reference/README.md` · `permanent/README.md` | 개정 |

- Domain / schema note: **DB 변경 없음.** 파일·빌더·검증기만 다룬다.

## Domain / Schema

해당 없음 (파일 SoT).

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-015 | `validate_graph` | Apply Executor가 발행 전 검증에서 이 함수를 호출한다 |
| 후속 열람 표면 | `_graph.json` `nodes[].layer` | 층 필터가 이 필드를 소비한다 |

## Internal Interface Contract

`_graph.json` `nodes[]`에 `layer` 필드가 추가된다. 값은 `source` · `concept` · `synthesis` · `execution` · `null`(층 없음).

`validate_graph`의 반환에 **미소화 큐 집계**가 더해진다 — `source` orphan은 위반 목록에 넣지 않고 별도로 낸다. 기존 호출부(`_enforce_graph`)가 위반 목록만 보고 차단하므로, 이 분리로 부팅이 막히지 않는다.

## Execution

### Phase 1 — report-only 측정

- **Status**: TODO
- **설명**: 새 규칙을 **차단 없이** 넣고 기존 406노드가 얼마나 위반하는지 잰다. WORK-001~007에서 검증된 순서(report-only → 데이터 정리 → enforce)를 그대로 따른다.
- **작업**:
  - [ ] `layer` 도출 매핑 추가 (`type` → `layer`)
  - [ ] rank 테이블을 층 순서로 교체하고 **비교 연산자를 `<=`로 반전**
  - [ ] L2 type별 필수 필드 규칙 추가
  - [ ] L5를 층별 판정으로 교체 + `source` orphan 별도 집계
  - [ ] 새 규칙 위반을 **WARN/리포트로만** 내보내도록 임시 처리
- **검증**:
  - [ ] 기존 406노드에 대한 신규 위반 수를 측정해 기록 (L2 필수 필드 / L4 반전 각각)
  - [ ] L5 WARN이 156건 → 0건이 되고 미소화 큐 지표에 156이 잡힌다
  - [ ] 부팅이 막히지 않는다 (`_enforce_graph`가 신규 위반으로 raise하지 않음)
  - [ ] 기존 테스트 전부 통과
- **완료 증거**: 미작성

> **rank 반전 주의**: 테이블만 교체하고 비교를 그대로 두면 L4가 조용히 반대로 동작한다. 현행은 `reference=4` + `up 타겟 rank >= 자기 rank`, 신규는 `reference=1` + `<=`다. Phase 1에서 `concept → reference`가 통과하고 `reference → concept`가 걸리는지 반드시 확인한다.

### Phase 2 — 데이터 정리

- **Status**: TODO
- **설명**: Phase 1이 찾아낸 위반을 해소한다. 위반 수에 따라 범위가 정해지므로 Phase 1 결과를 보고 시작한다.
- **작업**:
  - [ ] `note` 타입 잔존 데이터 확인 및 제거 (실사용 0건 예상 — 확인 필요)
  - [ ] `permanent` 1건의 `up:` 필수 충족 여부 확인·보정
  - [ ] 기존 lineage 1건이 새 방향 규칙을 통과하는지 확인·보정
  - [ ] `product` 타입 정리 (showcase는 이미 빌더에서 제외됨 — enum만 정리)
- **검증**:
  - [ ] 신규 규칙 위반이 0이 된다
  - [ ] 기존 노드 수·엣지 수가 의도치 않게 변하지 않는다
- **완료 증거**: 미작성

### Phase 3 — concept 층 실재화

- **Status**: TODO
- **설명**: 디렉토리와 로더 배선. WORK-010의 permanent 배선을 미러한다.
- **작업**:
  - [ ] `permanent/concept/` 디렉토리 + README 생성
  - [ ] `persona_loader`가 `permanent/concept/`를 순회하고 `type: concept`를 주입
  - [ ] `_build_graph_nodes`에 concept 포함
  - [ ] `_graph.json` `nodes[]`에 `layer` 필드 추가
  - [ ] 샘플 concept 1건을 손으로 작성해 계보 발현 확인
- **검증**:
  - [ ] concept 노트가 노드로 잡히고 `layer: concept`이 나온다
  - [ ] `concept → reference` `up:`이 lineage 엣지로 발현된다 (**lineage 엣지가 1건에서 늘어나는 첫 지점**)
  - [ ] `aliases`로 링크한 `[[음성인식]]`이 canonical stem으로 resolve된다
  - [ ] 빈 `permanent/concept/`에서도 부팅에 영향이 없다
- **완료 증거**: 미작성

### Phase 4 — 규칙·템플릿 문서

- **Status**: TODO
- **설명**: 사람과 AI가 따를 작성 규칙을 파일로 만든다. AI가 concept 초안을 생성하려면 따를 형식이 파일로 있어야 한다.
- **작업**:
  - [ ] `rules/knowledge-note-pipeline.md` 작성 — 4층 모델·SoT 위임·개념 성장·경로/frontmatter·`up:`/`[[]]` 규칙
  - [ ] `templates/knowledge/` 4종 작성 (idea·reference·concept·permanent)
  - [ ] `inbox/README.md`의 "미분류만 보유" → **"미정제만 보유"** 개정
  - [ ] `reference/README.md`·`permanent/README.md`에 층·SoT 위임 반영
  - [ ] 각 README가 SPEC이 아니라 `rules/knowledge-note-pipeline.md`를 가리키도록 정리
  - [ ] **템플릿을 기계가 읽을 수 있는 형태로 둔다** — WORK-015의 AI 스테이지가 프롬프트에 주입할 수 있어야 한다(경로 고정 + frontmatter 예시 포함)
- **검증**:
  - [ ] 템플릿으로 만든 concept가 검증을 통과한다 (**템플릿과 lint가 어긋나지 않음을 실제로 확인**)
  - [ ] 템플릿으로 만든 reference·permanent도 검증을 통과한다
  - [ ] 규칙 문서와 SPEC-001/002/004 사이에 중복 서술이 없다 (규칙=쓸 때 / SPEC=검증 계약)
- **완료 증거**: 미작성

> 템플릿은 사람용 참고자료가 아니라 **AI 초안 생성의 입력**이다. WORK-015의 concept·source_note 스테이지가 이 파일을 프롬프트에 넣는다. 따라서 템플릿이 검증을 통과하지 못하면 AI 산출물도 통과하지 못한다 — 위 검증 항목이 그 정합을 보장한다.

### Phase 5 — enforce 전환

- **Status**: TODO
- **설명**: 데이터가 green이 된 뒤에 차단을 켠다. 순서를 지키지 않으면 라이브 서버가 부팅에 실패한다.
- **작업**:
  - [ ] 신규 L2/L4 위반을 ERROR로 승격
  - [ ] `GRAPH_ENFORCE` kill-switch가 신규 규칙에도 적용되는지 확인
  - [ ] **pre-commit 훅 트리거 경로 구멍 수정** — `app/scripts/install_hooks.sh:34`의 `^(persona|reference|products)/`에 `permanent`·`inbox` 추가
- **검증**:
  - [ ] enforce ON 상태에서 실데이터 부팅 성공
  - [ ] `up:` 없는 concept를 주입하면 부팅이 막힌다
  - [ ] `reference → concept` `up:`을 주입하면 L4 ERROR가 난다
  - [ ] `GRAPH_ENFORCE=0`이면 로드된다
  - [ ] 런타임 reload 실패 시 구 데이터가 유지된다
  - [ ] **`permanent/concept/` 파일만 고친 커밋이 pre-commit 검증을 탄다**
  - [ ] **`permanent/` 루트 파일만 고친 커밋도 검증을 탄다** (기존 구멍 해소 확인)
- **완료 증거**: 미작성

> **기존 구멍**: `install_hooks.sh:34`의 트리거가 `^(persona|reference|products)/`인데 **`permanent/`가 빠져 있다.** WORK-010이 permanent를 그래프 노드로 배선했으나 훅 트리거는 따라가지 않았다. 지금은 permanent 노트만 고쳐 커밋하면 그래프 검증이 돌지 않고 부팅 시점에야 걸린다. `inbox/`(idea 노드)도 같다. concept 추가가 이 구멍을 확대하므로 여기서 함께 막는다.

## Pre-deploy Check

- [ ] Phase 2가 끝나 신규 위반이 0인 상태에서만 Phase 5를 켠다
- [ ] `GRAPH_ENFORCE` kill-switch 동작 확인 (부팅 brick 대비)
- [ ] `_graph.json` 계약 변경(`layer` 추가)이 기존 FE `/graph`를 깨지 않는지 확인 — 추가 필드라 무시되면 정상
- [ ] 기존 156건 L5 WARN이 사라져도 운영 경보 파이프라인에 영향이 없는지 확인

## Rollback

- Phase 5 → `GRAPH_ENFORCE=0`으로 즉시 차단 해제. 부팅이 살아난다.
- Phase 3 → `permanent/concept/`가 비어 있으면 노드 0이라 무영향. 로더 배선만 revert.
- Phase 1 → rank 테이블·연산자를 원복. `layer`는 추가 필드라 소비자가 없으면 무해.
- DB 변경이 없어 migration revert 절차가 없다.

## Done Criteria

- [ ] 모든 Phase가 `DONE`이다.
- [ ] `permanent/concept/`에 concept를 쓰면 검증을 통과하고 그래프에 계보로 잡힌다.
- [ ] L5 orphan 156건이 위반이 아니라 미소화 큐 지표로 나온다.
- [ ] `rules/knowledge-note-pipeline.md`와 `templates/knowledge/`가 존재한다.
- [ ] enforce ON 상태에서 실데이터 부팅이 성공한다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- **Phase 1의 측정 결과가 이 work의 실제 범위를 정한다.** L4 반전으로 기존 데이터가 크게 깨지면 Phase 2가 별도 work로 분리될 수 있다.
- concept 입도 규칙은 아직 없다(KDEV-DEC-010 OQ-2). 손으로 쓰는 단계에서는 판단에 맡기고, WORK-015 첫 실전에서 관찰해 규칙화한다.
- `rules/knowledge-note-pipeline.md`와 SPEC-001/002/004의 경계가 흐려질 위험이 있다. 규칙은 **쓸 때 따르는 것**, SPEC은 **검증기가 검사하는 계약**으로 나눈다.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: WORK-010(permanent 배선 — 이 work가 미러하는 선례), 후속 WORK-014
