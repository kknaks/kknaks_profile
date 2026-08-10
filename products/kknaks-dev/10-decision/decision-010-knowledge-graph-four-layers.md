---
type: decision
id: KDEV-DEC-010
title: "지식 그래프 재설계 — 4층 모델과 원자 개념(concept) 층"
status: accepted
product: kknaks-dev
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-003-node-type-and-identifier|KDEV-DEC-003]]"
    - "[[decision-004-edge-model-and-schema|KDEV-DEC-004]]"
    - "[[decision-008-contents-retention|KDEV-DEC-008]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
    - "[[spec-005-graph-visualization|KDEV-SPEC-005]]"
  works:
    - "[[work-013-concept-layer|KDEV-WORK-013]]"
  releases: []
  related: []
up:
  - cohesion
  - object-graph
---

# 지식 그래프 재설계 — 4층 모델과 원자 개념(concept) 층 (ADR-010)

지식 노트를 **출처 → 원자 개념 → 종합 판단 → 실행** 4층으로 재편하고, 비어 있던 개념 층에 `permanent/concept/`를 신설한다. 노드 타입에 `layer` 축을 도입하고, 층별로 의미가 다른 검증(특히 orphan)을 재정의한다.

> [[decision-003-node-type-and-identifier|KDEV-DEC-003]]의 노드 타입 목록과 [[spec-004-graph-validation|KDEV-SPEC-004]]의 L5 정의를 개정한다. 두 결정의 **핵심 메커니즘(파일명 stem 식별자 + `aliases`, 본문 `[[]]` 단일 소스 + `up:` 오버레이)은 유지**한다 — 근거였던 옵시디언 순정 제약이 그대로이기 때문이다.

## Context

- 관련 baseline: [[baseline-003-inbox-approval-pipeline|KDEV-BL-003]], [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- 승인 게이트 파이프라인이 **어느 목적지에 무엇을 쓸지** 정하려면 목적지 taxonomy가 먼저 확정돼야 한다. 게이트 설계의 선행 결정이다.

### 실측 진단 (2026-07-27, `_graph.json`)

```text
nodes 406 / edges 427

157 reference        426 assoc
 79 decision           1 lineage
 76 work
 69 spec
 13 baseline
  6 release            idea 0 · post 0 · content 0(그래프 제외)
  4 runbook            concept 없음
  1 permanent
  1 bugfix
```

세 가지 문제가 확인된다.

1. **개념 층이 없다.** `reference`(자료)와 `permanent`(생각) 2층뿐이라, 같은 개념이 여러 자료에 걸쳐 나와도 합류할 자리가 없다. `permanent`는 실제로 1건이다.
2. **lineage 엣지가 1개다.** 방향성(계보)이 사실상 발현되지 않는다. 원인은 규칙 부재가 아니라 **생성기 부재**다 — `service/knowledge_capture/render.py:52-81`이 만드는 frontmatter에 `up:` 필드가 아예 없어서, Slack 캡처가 계보를 만들 방법이 구조적으로 없었다. 남은 1건은 사람이 손으로 쓴 `permanent` 1개다.
3. **L5 orphan 경보가 죽어 있다.** WORK-005에서 `persona/notes/` 157개를 `reference/`로 재타이핑한 뒤 orphan 156건이 WARN baseline으로 박제됐다([[spec-004-graph-validation|KDEV-SPEC-004]] §7). 모든 자료가 orphan인 상태에서 orphan 경보는 정보가 아니다.

### 코드 현실

- `core/graph.py:20` `ALLOWED_NODE_TYPES` 20종 — zettel 5 + persona 7 + products 8이 층 구분 없이 평평하다. [[decision-003-node-type-and-identifier|KDEV-DEC-003]]이 정한 건 5종이었다.
- `core/graph.py:33` `KNOWLEDGE_NODE_TYPES = {reference, permanent, post, product}` — L5 대상 집합.
- `core/graph.py:36` `_TYPE_RANK` — `reference/permanent/baseline/product = 4`로 동급. 실사용 0건인 `note`가 rank 1로 남아 있다.
- `core/graph.py:44` `build_alias_index` — frontmatter `aliases`를 stem으로 매핑한다. **개념 매칭에 쓸 재료가 이미 있다.**
- [[decision-008-contents-retention|KDEV-DEC-008]] — `persona/contents/`는 `_build_graph_nodes`에 전달되지 않는다. 그래프 노드가 아니므로 `[[C-012]]`는 L1 dead link ERROR가 된다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[cohesion]] — **층을 가르는 기준이 곧 응집도**다 — 「이 자료가 뭐라 했나」와 「이 개념은 뭔가」는 수명도 갱신 이유도 다르므로 한 노트에 두면 안 된다는 것이 4층의 근거다
- [[object-graph]] — 층이 생겨도 연결은 여전히 링크 그래프가 한다 — 폴더가 분류를 갖지 않는다는 전제가 유지된다

## Options

### 지식 층 구조

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 현행 2층 유지 | `reference` + `permanent` | 변경 0 | 개념 재사용 단위 없음, 제품 문서 쓸 때 개념을 긁어올 단일 지점 부재 | 기각 |
| **4층 + concept 신설** | 출처 → 개념 → 종합 → 실행 | 자료:개념 N:M 수용, 개념이 출처 합류로 성장, SoT 단일화 | 층 하나 추가, 검증·로더 개정 | **채택** |
| concept를 `permanent` 하위 태그로 | 디렉토리 대신 frontmatter 플래그 | 디렉토리 무변경 | 디렉토리가 1차 타입 결정이라는 SPEC-001 §5 원칙과 충돌 | 기각 |

### 유튜브 하나에서 나오는 산출물

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | `contents` + `concept` | 산출 2장 | contents가 그래프 노드가 아니라 **concept가 출처를 가리킬 수 없다**(L1 ERROR) | 기각 |
| **B** | `reference` + `concept` + `contents`(선택) | concept의 출처 추적이 그래프 안에서 성립, `reference/README.md`의 "인용되는 재료" 계약과 일치 | 산출 최대 3장 | **채택** |
| C | contents를 그래프 노드로 승격 | reference 불필요 | [[decision-008-contents-retention|KDEV-DEC-008]] 뒤집기, 8개 H2 교안은 그래프 재료로 무겁다 | 기각 |

### 제품 문서(248개)의 그래프 편입

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 제외 | 지식층만 그래프 | 노이즈 제거 | **"이 개념을 어느 프로덕트에 적용할지" 탐색이 끊긴다** | 기각 |
| **4층(실행층)으로 유지** | 제품 문서를 실행층 노드로 | concept → product 탐색 성립 | 내부 링크 248개가 지식 연결을 압도 | **채택** (층 필터로 뷰 분리) |

### 열람 표면

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| force-graph 유지 | 현행 `/graph` canvas | 구현됨 | lineage 1건이라 그릴 게 없고, 406노드에서 탐색이 안 됨 | 기각 |
| **트리 문서 렌더러** | 좌측 디렉토리 트리 + 우측 md 렌더 (AXKG-SPEC-013 형태) | 읽기·탐색이 실제로 됨 | 신규 구현 | **채택** |

> **부분 supersede (2026-08-10) — [[decision-019-drop-synthesis-layer|KDEV-DEC-019]]**
>
> 아래 D1 의 4층 중 **판단층(`resources/synthesis/`, `type: permanent`)은 폐기**됐다.
> 지식층은 `source → concept → execution` 3층이다. 층 축 도입·층별 orphan 판정·
> 파일명 stem 식별자·본문 `[[]]` 단일 소스 + `up:` 오버레이는 **그대로 유효**하다.

## Decision

### D1. 지식 4층 모델

노트는 아래 4층 중 하나에 속한다. 방향은 **출처 → 개념 → 종합 → 실행**이다.

| 층 | `layer` | 답하는 질문 | 경로 | 단위 | 수명 |
|---|---|---|---|---|---|
| 1. 출처 기록 | `source` | "이 자료가 뭐라고 했나" | `reference/{group}/` | 자료 하나 | 생성 후 고정 |

> **개정 (2026-07-28) — `reference` 는 flat 이다.** 위 표의 `reference/{group}/` 는 폐기한다.
>
> `{group}` 은 옛 `persona/notes/{cluster}/` 를 WORK-005 가 그대로 옮긴 것이고, 그 cluster 목록이
> `persona/_meta.yaml` 과 **이중 SoT** 를 이뤄 디렉토리를 바꿀 때마다 두 곳을 고쳐야 했다. 한쪽만
> 고치면 **부팅이 막혔다.**
>
> 이 문서가 `concept` 에 대해 정한 근거("개념은 분류 트리가 아니라 링크 그래프로 조직된다")가
> `reference` 에도 그대로 적용된다 — 출처 기록을 폴더로 나눌 이유가 없고, 분류는 `[[concept]]`
> 링크가 한다. cluster 의 유일한 소비자였던 `/graph` 는 D7 에서 이미 폐기했다.
>
> 결과: `reference/{YYYY-MM-DD}-{slug}.md`, `group` 필드 소멸, route 게이트의 group 선택 제거,
> `_meta.yaml` 은 표시용으로만 남는다.

| 2. 원자 개념 | `concept` | "이 개념은 뭔가" | `permanent/concept/` | 개념 하나 | 출처 합류로 **성장** |
| 3. 종합 판단 | `synthesis` | "내 판단·전략은 뭔가" | `permanent/` 루트 | 영역 하나 | 개념 유입마다 갱신 |
| 4. 실행 | `execution` | "그래서 뭘 만드나" | `products/{제품}/` | 프로젝트 문서 | 제품 파이프라인을 따름 |

층은 **디렉토리가 1차 결정**하고 frontmatter가 명시한다([[spec-001-directory-structure|KDEV-SPEC-001]] §5 원칙 계승).

### D2. `permanent/concept/` 신설과 동반 규율

- `permanent/concept/`를 신설하고 노드 타입 `concept`를 추가한다. 한 파일 = 한 개념.
- **SoT 위임**: 개념 상세의 SoT는 concept 노트 **한 곳**이다. `reference`는 개념을 재서술하지 않고 요지 + `[[concept]]`로 위임하고, `permanent` 종합 노트도 개념을 재서술하지 않고 **엮은 판단만** 소유한다.
- **개념 성장**: 같은 개념에 두 번째 출처가 오면 새 파일을 만들지 않고 **기존 concept를 보충**한다. 이것이 개념 성장 메커니즘이며, 승인 파이프라인의 concept 스테이지는 매번 "신규 생성 vs 기존 보충"을 판정한다.
- **`aliases` 필수**: concept는 frontmatter `aliases`를 반드시 갖는다(예: `stt` → `[Speech-to-Text, 음성인식, ASR]`). 개념 매칭의 1차 재료이며, `core/graph.py:44` `build_alias_index`가 이미 지원한다.
- "재서술 금지"의 범위는 **개념 상세 설명 섹션을 복사하지 않는다**는 뜻이다. 종합 노트의 판단 문장 안에 개념 요지가 인용되는 것은 허용하며 필연적이다.

### D3. 노드 타입 재편 — `layer` 축 도입

`type`은 유지하되 `layer` 축을 새로 둔다. 20종 평면 목록을 층으로 묶는다.

| 구분 | layer | type |
|---|---|---|
| 지식 층 | `source` | `reference` |
| | `concept` | `concept` (신설) |
| | `synthesis` | `permanent` |
| | `execution` | `baseline`, `decision`, `spec`, `work`, `release`, `runbook`, `bugfix` |
| **노드이되 층 없음** | — | `idea` |
| 그래프 밖 | — | `content`, `algorithm`, `daily`, `career`, `profile` |
| 보류 | — | `post` |

- `note`는 실사용 0건이므로 **제거**한다(WORK-005에서 `reference`로 전량 재타이핑됨).
- `product`는 `products/{제품}/showcase.md`를 가리키는데 그래프 빌더에서 제외돼 있다(WORK-004). 타입 목록에서 정리한다.
- **`idea`는 그래프 노드이지만 층에 속하지 않는다.** 본문 `[[]]`로 다른 노트를 참조할 수 있어 엣지는 생기지만, 휘발이라 상류가 될 수 없고 `up:`을 가질 수 없다(현행 `core/graph.py` L4 idea 가드 유지). 층이 없으므로 층별 orphan 판정(D5) 대상도 아니다.
- `content`·`algorithm`은 [[decision-008-contents-retention|KDEV-DEC-008]]대로 그래프 밖에 남는다. `daily`·`career`·`profile`은 정체성 문서로 그래프 주변에 둔다.
- `post`는 디렉토리 자체가 없고 실 발행물이 0건이라 층 배정을 **보류**한다(아래 보류 항목). 게시 판정 게이트 설계 시 함께 정한다.

`_TYPE_RANK`는 층 순서에서 도출한다: `source(1) → concept(2) → synthesis(3) → execution(4)`. `up:` 타겟은 **같거나 낮은 층**이어야 한다 — 즉 상류(출처 방향)만 가리킨다.

> **주의 — 현행 코드와 비교 방향이 반대다.** `core/graph.py:34`의 현행 규칙은 *"높을수록 상류, `up` 타겟 rank >= source rank"*이고 `reference = 4`(최상류), `idea = 0`이다. 새 모델은 층 번호를 **파이프라인 진행 순서**로 쓰므로 `reference = 1`이 되고 비교가 `<=`로 뒤집힌다. 구현 시 rank 테이블만 갈아끼우면 L4가 조용히 반대로 동작하므로, 비교 연산자까지 함께 바꿔야 한다.

| 관계 | 방향 | 예 |
|---|---|---|
| concept → reference | 개념이 출처를 가리킴 | `permanent/concept/stt.md` `up: [2026-07-27-whisper-architecture]` |
| synthesis → concept | 판단이 구성 개념을 가리킴 | `permanent/음성-인터페이스-전략.md` `up: [stt, vad]` |
| execution → concept/synthesis | 제품 결정이 근거를 가리킴 | `products/mac-remote/00-baseline/...` `up: [stt]` |

**층 rank는 층간 방향만 강제한다.** 실행층 내부의 순서(`baseline → decision → spec → work`)는 현행 `_TYPE_RANK`가 `baseline 4 / decision·spec 3 / work 2`로 인코딩하고 있는데, 이는 `rules/product-doc-pipeline.md`의 매핑 규칙이 이미 소유한 영역이다. 층 모델은 이를 흡수하지 않고 실행층을 하나로 묶으며, 제품 문서 내부 정합은 `product_doc_pipeline.py` 검증기가 계속 담당한다.

### D4. 엣지 모델 — 유지 + 생성 의무

- [[decision-004-edge-model-and-schema|KDEV-DEC-004]]의 **엣지 = 본문 `[[stem]]` 단일 소스(`assoc`) + frontmatter `up:` 오버레이(`lineage`)** 모델을 그대로 유지한다. 옵시디언 순정 제약이 변하지 않았고, 관계 종류를 엣지 타입으로 쪼개는 대신 **양 끝 노드의 `layer`로 관계를 읽는다**(concept→source = "출처", synthesis→concept = "구성").
- **신규**: 파이프라인이 생성하는 모든 지식 노트는 `up:`을 채워야 한다. `up:` 없이 발행되는 concept/synthesis는 Apply Executor가 거부한다. lineage 1건의 원인이 생성기 부재였으므로, 생성 계약에 의무를 박는다.
- L3(오버레이 정합 — `up:` stem이 본문 `[[]]`에도 존재)는 유지한다.

### D5. 검증 재정의 — 층별 orphan

현행 L5는 `KNOWLEDGE_NODE_TYPES` 전체에 같은 규칙을 적용해 156건 WARN을 만들었다. 층마다 orphan의 의미가 다르므로 분리한다.

| layer | orphan이면 | 판정 |
|---|---|---|
| `source` (reference) | 아직 개념으로 올라가지 않음 | **정상** — 위반이 아니라 **미소화 큐**로 집계 |
| `concept` | 출처도 없고 쓰이지도 않음 | **ERROR** — 개념으로 성립하지 않음 |
| `synthesis` (permanent) | 개념을 엮지 않음 | **WARN** |
| `execution` | 제품 파이프라인이 관리 | 검사 제외 (현행 유지) |
| 층 없음 (`idea`) | 휘발이라 연결 의무 없음 | 검사 제외 |

이 변경으로 156건 노이즈가 사라지고, 같은 데이터가 "소화 안 된 자료 157개"라는 **작업 큐**로 뒤집힌다. 이 큐가 승인 파이프라인의 입력 후보가 된다.

L1(dead link)·L2(스키마/유일성)·L3(오버레이)·L4(방향)·L6(archive 참조)는 층 개념 위에서 재서술하되 판정 강도는 유지한다.

### D6. 제품 문서는 그래프에 유지한다

`baseline`/`decision`/`spec`/`work` 등 제품 문서는 4층(실행)의 노드로 **유지**한다. "이 개념을 어느 프로덕트에 적용/업데이트할지"를 찾는 경로가 concept → execution 연결이기 때문이다. 다만 제품 문서 내부 링크 248개가 지식 연결을 압도하므로, 열람 표면에서 **`layer` 필터로 뷰를 분리**한다.

[[spec-005-graph-visualization|KDEV-SPEC-005]]와 WORK-009에 미해소로 남아 있던 "`/graph`가 products 문서를 포함할지" OQ를 이 결정으로 해소한다 — **포함한다.**

### D7. 열람 표면과 공개 경계

- **공개 프론트(블로그)는 게시 판정을 통과한 것만 노출한다.** `reference`·`concept`·`permanent`는 내부 지식이며 프론트에 노출하지 않는다.
- **내부 열람은 admin의 트리 문서 렌더러**로 한다 — 좌측 디렉토리 트리 + 우측 Markdown 렌더, 읽기 전용(AXKG-SPEC-013 형태).
- 현행 `/graph` force-directed 시각화는 **폐기**한다. lineage 1건이라 그릴 관계가 없고 406노드에서 탐색이 성립하지 않는다.

### 기각

- 현행 2층 유지, concept를 frontmatter 플래그로 두는 안.
- 유튜브 산출물 A안(`contents` + `concept`) — concept가 출처를 가리킬 수 없다.
- 유튜브 산출물 C안(contents를 그래프 노드로 승격) — [[decision-008-contents-retention|KDEV-DEC-008]] 뒤집기.
- 제품 문서 그래프 제외.
- 엣지 타입 세분화(`derives_from`/`composes`/`grounds`) — `layer`로 도출 가능하므로 불필요한 축.
- force-graph 유지.

### 보류

- `persona/posts/` 배선 — 디렉토리 자체가 없고 실 발행물 0건이다([[decision-008-contents-retention|KDEV-DEC-008]] Scope Out). 게시 판정 게이트 설계 시 함께 다룬다.
- concept 개정이 상류 `synthesis`를 낡게 만드는 stale 연쇄 — 개념 성장이 실제로 돌기 시작한 뒤 관찰해서 별도 결정으로 뺀다.

## Rationale

- **판단 기준**: 지식이 재사용 단위로 서는가, 검증이 실제 신호를 내는가, 승인 파이프라인이 쓸 목적지가 명확한가.
- **4층인 이유**: 자료와 개념은 1:1이 아니다. 영상 하나에서 개념이 여럿 나오고 개념 하나가 영상 여럿에 걸쳐 나온다. 층을 합치면 자료 기준으로는 개념이 흩어지고, 개념 기준으로는 "그 자료가 뭐라 했는지"가 사라진다. 수명도 다르다 — 자료는 박제, 개념은 성장.
- **DEC-003/004를 통째로 버리지 않는 이유**: 두 결정의 근거는 "옵시디언 순정을 못 바꾸니 빌더가 맞춘다"였고 이 제약은 그대로다. 깨진 건 타입 목록이 5종에서 20종으로 불어난 것과, `up:`을 만드는 생성기가 없었던 것이지 모델 자체가 아니다.
- **제품 문서를 남기는 이유**: 지식그래프의 목적이 "브레인을 쌓는 것"에서 끝나지 않고 "제품에 적용하는 것"까지다. concept → execution 연결을 끊으면 그 목적이 사라진다.
- **리스크**:
  - 노드 타입·검증 개정은 boot fail-fast 게이트(WORK-007)를 건드린다. `GRAPH_ENFORCE` kill-switch가 있으므로 단계적 전환이 가능하다.
  - concept ERROR 판정이 세다. 초기에 빈 concept가 생기면 부팅이 막힐 수 있으므로, work에서 report-only → enforce 순서를 지킨다(WORK-001~007의 검증된 전환 패턴 재사용).
  - reference 157개가 당분간 미소화 큐로 남는다. 소급 정제는 이번 범위가 아니다.

## Scope

- In: 4층 모델 정의, `permanent/concept/` 신설, `layer` 축과 노드 타입 재편, rank·`up:` 방향 규칙, 층별 orphan 재정의, 제품 문서 편입, 열람 표면 전환 방향.
- Out:
  - 승인 게이트 체인·큐·Apply Executor (후속 decision/spec)
  - `rules/knowledge-note-pipeline.md`·`templates/knowledge/` 실제 작성 (work 산출물)
  - `reference/` 157개 소급 정제
  - `persona/posts/` 배선
  - stale 연쇄
- 영향을 받는 spec 후보: [[spec-001-directory-structure|KDEV-SPEC-001]], [[spec-002-graph-schema|KDEV-SPEC-002]], [[spec-004-graph-validation|KDEV-SPEC-004]], [[spec-005-graph-visualization|KDEV-SPEC-005]].

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | `reference/`의 group 13종을 그대로 둘지, 4층 재편에 맞춰 정리할지 (현재 `BackendSchool`·`bitcamp` 등 과거 교육과정 잔재 포함) | kknaks | SPEC-001 개정 시 |
| OQ-2 | concept의 입도 — "STT" 하나인지 "STT / 스트리밍 ASR / VAD"로 쪼개는지. 너무 잘게 쪼개면 성장이 안 되고 너무 크면 SoT가 흐려진다 | kknaks | 유튜브 파이프라인 첫 실전에서 관찰 후 규칙화 |
| OQ-3 | 제품 문서 248개 중 `work`·`release`·`runbook`까지 그래프에 둘지, `baseline`/`decision`/`spec`까지만 둘지 | kknaks | SPEC-002 개정 시 |
| OQ-4 | `layer`를 frontmatter에 명시할지 디렉토리에서 도출만 할지 (명시하면 중복, 도출만 하면 이동 시 자동 추종) | kknaks | SPEC-002 개정 시 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-001-directory-structure|KDEV-SPEC-001]] | update | §4 레이아웃에 `permanent/concept/` 추가, 층-디렉토리 매핑 |
| [[spec-002-graph-schema|KDEV-SPEC-002]] | update | `layer` 축, `concept` 타입, rank 재정의, `aliases` 필수 규약, `note` 제거 |
| [[spec-004-graph-validation|KDEV-SPEC-004]] | update | L1~L6 층 기준 재서술, 층별 orphan, `up:` 생성 의무 |
| [[spec-005-graph-visualization|KDEV-SPEC-005]] | update | force-graph 폐기 → 트리 문서 렌더러, `layer` 필터, 공개/내부 경계 |
