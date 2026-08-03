---
type: baseline
id: KDEV-BL-006
title: "PARA 정렬과 SoT 지도 — 지식층 디렉토리 재편"
status: raw
product: kknaks-dev
source:
  type: idea
  ref: "kknaks 요청 2026-08-03 — 디렉토리 정리, SoT 가 사방에 흩어져 있다"
links:
  baselines: []
  decisions:
    - "[[decision-018-resources-layout-and-sot-naming|KDEV-DEC-018]]"
  specs: []
  works: []
  releases: []
  related:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
    - "[[baseline-005-product-project-career-link|KDEV-BL-005]]"
created_at: 2026-08-03
updated_at: 2026-08-03
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/raw
---

# PARA 정렬과 SoT 지도 — 지식층 디렉토리 재편

**`permanent` 라는 이름이 두 뜻을 겸하고 있다** — 지식 자산의 그릇이면서 동시에 그 안의 한 층(synthesis)이다. R(Resources) 버킷을 이름이 뜻과 일치하는 자리로 옮기고, `archive` 를 그 밖으로 뺀다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

## Raw

> kknaks 요청 (2026-08-03)

- *"우리 `agent.md` 좀 수정해야 할 것 같아. 지금 디렉토리가 정리가 안 되는데?"*
- *"확실히 정하고 가자"* — PARA 로 축을 잡는다.

```text
P → product
A → 블로그 노출 영역
R → concept/reference
A → archive
```

- *"지금 SoT 가 사방에 흩어져 있는 것 같은데"*
- *"permanent 에 reference 를 이동하면 안 되나? 그리고 archive 를 permanent 밖으로 빼고"*

**대화 중 정정 — Area 는 미룬다.** *"일단 area 는 최종으로 가고"*. `persona/` 의 재분류는 이 baseline 범위 밖이고, 아래 「미결」에 남긴다.

**세 안 중 B 채택.** 실측을 보고 사용자가 골랐다.

| | 모양 | 판정 |
|---|---|---|
| A | `permanent/{reference,concept,*.md}` + `archive/` | `permanent` 겸직 심화 · 위계 역전 |
| **B** | **`resources/` 신설 + `archive/` 최상위** | **채택** — 이름이 뜻과 일치. 하위 폴더명은 미결 ② |
| C | 지금 유지, 문서에서만 R 을 "둘의 합" 으로 정의 | 폴더로는 안 보인다 |

## Context

작업 착수 시점(2026-08-03) 실측.

### 지식층 전체가 14 파일이고 둘은 비어 있다

```text
inbox                4
reference            2       ← flat (SPEC-001 은 아직 `{group}/` 이라고 적고 있다)
permanent/*.md       0       ← synthesis 층. 한 건도 없다
permanent/concept    8
permanent/archive    0       ← 비어 있다
```

**옮길 데이터가 사실상 없다.** `archive` 이동은 빈 디렉토리를 옮기는 일이고, `reference` 이동도 2 파일이다. 비용은 전부 코드와 문서에 있다.

`permanent/*.md` 가 0인 것은 [[work-017-grass-commit-pipeline|KDEV-WORK-017]] Open Issue(*"`permanent/concept/` 발행 경로가 어디서도 안 탔다"*)와 같은 자리다 — **4층 중 둘이 아직 안 채워졌다.**

### `layer` 는 디렉토리가 아니라 `type` 에서 나온다 — 이게 위험을 낮춘다

`core/graph.py:78 layer_of()` 가 `type` → `layer` 를 계산한다([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D3, *"같은 사실을 두 곳에 두면 언젠가 어긋난다"*).

**그래서 폴더를 옮겨도 그래프 층 판정·L1~L6 검증은 흔들리지 않는다.** 흔들리는 곳은 셋뿐이다.

| 곳 | 무엇 |
|---|---|
| `persona_loader._enrich_permanent` | 경로에서 `type` **기본값**을 정한다 — `"concept" in path.parts` |
| `persona_loader` 로드 경로 | `_load_reference_notes(… / "reference")` · `_load_permanent_notes(… / "permanent")` |
| `apply/plan.py` | `ALLOWED_PREFIXES` · `LAYER_PREFIX` · 층-경로 정합 검사 |

### `permanent` 가 두 뜻을 겸한다 — 이게 핵심 문제다

```text
permanent/          R 버킷의 루트 (concept·archive 를 담는 그릇)
permanent/*.md      synthesis 층 그 자체
```

`reference` 를 그 안에 넣으면(A안) 겸직이 심해진다. **4층에서 `reference` 는 `source`(미소화)이고 `permanent` 는 `synthesis`(판단)라, source 를 synthesis 아래에 두면 위계가 뒤집힌다.**

### SoT 를 선언하는 문서가 20개이고, 두 종류가 섞여 있다

| 뜻 | 어디서 | 예 |
|---|---|---|
| **형식 SoT** — 문서가 어떻게 생겼나 | `templates/**` 10개 | *"이 파일이 daily 형식의 SoT다"* |
| **데이터 SoT** — 진실이 어디 사나 | `40-architecture/database` · DEC-009/012 | *"발행 본문은 md, 운영 상태는 DB"* |

**같은 단어를 두 뜻으로 쓴다.** 어느 축 얘기인지 매번 다시 읽어야 하고, 그것이 *"사방에 흩어져 있다"* 는 감각의 가장 큰 원인이다. `permanent` 겸직과 **같은 병**이다.

### 주인 없는 디렉토리가 둘 있다

```text
downloads/   DeskDeckHelper-1.0.1.dmg      바이너리가 git 에 커밋돼 있고 .gitignore 에도 없다
reports/     PLAN-013-T-008 · T-009.md     폐기된 PLAN 체계의 잔재
```

`agent.md`·`SPEC-001`·`context/**` 어디도 이 둘을 가리키지 않는다. 흩어진 게 아니라 **떨어져 나온 것**이다.

### SPEC-001 에 낡은 줄이 하나 있다

레이아웃이 `reference/{group}/` 로 적혀 있는데 **실제는 flat 이다.** `_auto_enrich_note` docstring 이 그 이유를 남겨 뒀다 — *"cluster 가 `persona/_meta.yaml` 과 이중 SoT 를 이뤄 디렉토리를 바꿀 때마다 두 곳을 고쳐야 했다."* WORK-005/013 에서 flat 으로 바뀌었으나 spec 이 안 따라왔다.

## Why It Matters

- **이름이 뜻과 어긋나면 매번 해석 비용이 든다.** `permanent/concept/` 를 볼 때마다 *"영구노트 안의 개념인가, 개념이 영구노트의 한 종류인가"* 를 다시 판단하게 된다. 실제로는 둘 다 아니고 **형제**다.
- **지금이 가장 싸다.** 지식층이 14 파일이고 옮길 두 디렉토리 중 하나는 비어 있다. R 이 커진 뒤에 하면 파일 이동·링크 정합·아카이브 충돌이 전부 따라온다.
- **A(Area) 결정을 미룰 수 있게 된다.** R 과 Archive 를 먼저 세우면 남는 것이 `persona/` 하나뿐이라, 그때 A 를 정하는 판단이 단순해진다.
- **SoT 라는 말이 두 뜻인 것을 안 고치면 지도를 그려도 또 흩어진다.** 폴더를 옮기는 것과 같은 무게의 문제다.

## Possible Direction

아직 결정은 아니다. decision 에서 확정한다.

### 목표 레이아웃

```text
products/     P    제품 문서 + showcase          (변경 없음)
persona/      A    ← 최종 결정 보류 (미결 1)
resources/    R    reference · concept · notes   ← 신설
archive/      A    permanent/archive 에서 승격    ← 최상위로
inbox/        수집함 — PARA 밖, 유입구           (변경 없음)
```

`resources/` 하위는 4층을 그대로 쓴다 — **PARA 와 4층은 겹치는 게 아니라 직교한다.**

```text
resources/
├── reference/   층: source     type: reference
├── concept/     층: concept    type: concept
└── notes/       층: synthesis  type: permanent      ← 지금 `permanent/*.md`
```

`notes/` 이름은 후보다. `synthesis/` 도 가능하고, 그러면 폴더명이 층명과 1:1이 된다.

### `archive` 를 밖으로 빼는 이유

`archive` 는 **층이 아니라 상태**다(SPEC-001 이 이미 그렇게 적어 뒀다). 지금은 `permanent/` 아래 있어 *"영구노트의 아카이브"* 로 보이는데, 실제로는 `permanent`·`concept` 공용이고 앞으로 `reference` 도 내려간다. **상태를 층 아래 두면 그 층의 소유물처럼 읽힌다.**

### 코드 접점 — 셋뿐이다

`layer` 가 `type` 에서 나오므로 그래프·검증은 무영향이다.

| 파일 | 무엇을 고치나 |
|---|---|
| `persona_loader.py` | 로드 경로 2개 · `_enrich_permanent` 의 경로 기반 type 기본값 · `_auto_enrich_note` 의 reference 경로 |
| `apply/plan.py` | `ALLOWED_PREFIXES` · `LAYER_PREFIX` · `permanent` vs `concept` 접두 충돌 검사 |
| `agent.md` 경로표 | 4개 경로 |

**`LAYER_PREFIX` 에 접두 충돌이 하나 생긴다.** `resources/` 아래 셋이 모두 같은 접두를 공유하므로 `permanent → resources/notes/` 와 `concept → resources/concept/` 의 판정 순서가 중요해진다. 지금 코드에 이미 같은 형태의 방어가 있다(`permanent` 인데 `permanent/concept/` 아래면 위반).

### 문서 접점

`rules/knowledge-note-pipeline.md` · `templates/knowledge/` 4개 · SPEC-001·002·004·005 · `agent.md`.

**SPEC-001 의 낡은 줄(`reference/{group}/`)도 같은 개정에서 정정한다.**

### SoT 두 뜻을 이름으로 가른다

폴더 이동과 별개로, 문서에서 쓰는 말을 나눈다. 후보:

```text
형식 SoT  →  "양식 원천" (templates/**)
데이터 SoT →  "SoT"      (어디에 진실이 사나)
```

이름을 뭘로 하든, **한 문서 안에서 두 뜻을 같은 단어로 쓰지 않는다**가 결정의 내용이다.

## 미결 (decision 대상)

1. **`persona/` 를 A 로 볼 것인가** — 사용자가 *"area 는 최종으로"* 로 미뤘다. 후보 둘: **A-1 지속 책임**(career 만 A, 나머지는 P 산출물·표면) vs **A-2 공개 표면**(showcase·contents·algorithms·profile 이 A). A-2 로 가면 `products/*/showcase.md` 가 P 에서 A 로 넘어가고 `product_slug` 가 P↔A 다리가 된다.
2. **`resources/` 하위 synthesis 폴더 이름** — `notes/` vs `synthesis/`. 후자는 층명과 1:1 이지만 사람이 부르는 말과 멀다.
3. **`inbox/` 를 `resources/` 안에 넣을지** — 지금 안은 밖이다. 미소화라 R 이 아니라는 판단인데, PARA 원안에서도 Inbox 는 별도다.
4. **`downloads/` · `reports/` 처분** — 삭제 / `archive/` 로 / `.gitignore`. `downloads/` 는 **바이너리가 git 에 있는 상태**라 이력에서 빼는 것까지 볼지도 결정거리.
5. **SoT 두 뜻의 명칭** — 위 후보를 쓸지, 다른 말을 쓸지.
6. **이동 시점** — 지식층이 14 파일인 지금이 가장 싸다. 다만 `products/` 는 428 파일이라 P 는 이번에 안 건드린다는 것을 명시할지.
