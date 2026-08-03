---
type: decision
id: KDEV-DEC-018
title: "지식층 디렉토리 재편 — resources/ 신설과 SoT 명칭 분리"
status: proposed
product: kknaks-dev
created_at: 2026-08-03
updated_at: 2026-08-03
tags:
  - product/kknaks-dev
  - doc/decision
  - status/proposed
links:
  baselines:
    - "[[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]"
  decisions:
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
  specs: []
  works: []
  releases: []
  related:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
    - "[[decision-017-product-registry-and-admin-scaffold|KDEV-DEC-017]]"
---

# 지식층 디렉토리 재편 — `resources/` 신설과 SoT 명칭 분리 (ADR-018)

R(Resources) 버킷을 `resources/` 로 신설하고 **하위 폴더 이름을 층 이름으로 통일한다.** `archive` 를 최상위로 올리고, `SoT` 라는 말이 두 뜻으로 쓰이던 것을 **「양식 원천」과 「SoT」로 가른다.**

> [[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]] 의 B안. `persona/`(A 판정)와 `products/`(P)는 이번 범위 밖이다.

## Context

- 관련 baseline: [[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]
- **`permanent` 가 두 뜻을 겸한다** — R 버킷의 그릇(concept·archive 를 담는다)이면서 동시에 synthesis 층 그 자체(`permanent/*.md`)다.
- **`SoT` 도 두 뜻이다** — 선언 문서 20개가 *형식 SoT*(`templates/**` 10개)와 *데이터 SoT*(`40-architecture/database`·DEC-009/012)를 같은 단어로 쓴다. 어느 축인지 매번 다시 읽어야 한다.
- **지식층 전체가 14 파일**이고, 옮길 둘 중 `permanent/archive/` 는 **비어 있고** `permanent/*.md`(synthesis)도 **0건**이다. 데이터 이동 위험이 사실상 없다.
- **`layer` 는 디렉토리가 아니라 `type` 에서 도출한다**([[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] D3 · `core/graph.py:78 layer_of()`). 폴더를 옮겨도 **그래프 층 판정과 L1~L6 검증은 흔들리지 않는다.**
- 코드 접점은 셋뿐이다 — `persona_loader` 로드 경로와 경로 기반 `type` 기본값 · `apply/plan.py` 의 `ALLOWED_PREFIXES`/`LAYER_PREFIX`/층-경로 정합 · `agent.md` 경로표.
- **`downloads/` 와 `reports/` 는 잔재가 아니었다.** `main.py:180` 이 `downloads/` 를 `/download/*` 로 정적 서빙하고 DeskDeck 랜딩이 그걸 링크한다(MRT-RB-001). `reports/PLAN-013-T-008·009.md` 는 `products/ax-knowledge-graph/` 의 `log.md`·`30-work/` 가 참조한다. **선언이 없을 뿐 소유자가 있다.**
- `SPEC-001` 레이아웃이 `reference/{group}/` 로 적혀 있으나 **실제는 flat** 이다(WORK-005/013 에서 바뀌었고 spec 이 안 따라왔다).

## Options

### R 버킷의 모양

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | `permanent/{reference,concept,*.md}` + `archive/` | 이동 최소 | **`permanent` 겸직 심화.** source 를 synthesis 아래 두어 4층 위계가 뒤집힌다 |
| **B** | **`resources/` 신설 + `archive/` 최상위** | 이름이 뜻과 일치. PARA 와 4층이 직교 | 문서·코드 수정이 A 보다 넓다 |
| C | 현행 유지, 문서에서만 R 을 "둘의 합" 으로 정의 | 코드 0 | 폴더로는 안 보인다. 새로 오는 사람이 못 읽는다 |

### `resources/` 하위 폴더의 이름 축

| Option | Description | Pros | Cons |
|---|---|---|---|
| **층 이름** | `source/` · `concept/` · `synthesis/` | **폴더명 = 층명 1:1.** `permanent` 겸직 이름이 사라진다 | 사람이 부르는 말("레퍼런스")과 한 겹 멀다 |
| type 이름 | `reference/` · `concept/` · `permanent/` | 기존 용어 유지, 수정 최소 | `permanent` 이름이 남는다 |
| 혼합 | `reference/` · `concept/` · `notes/` | — | **축이 섞인다** — 고치려는 병을 새 폴더에 옮기는 것 |
| flat | 하위 없이 전부 `resources/*.md` | 축이 하나 | 14개일 땐 되지만 늘면 섞인다 |

### `SoT` 명칭

| Option | Description | Pros | Cons |
|---|---|---|---|
| **양식 원천 / SoT** | templates 는 "양식 원천", 데이터 위치만 "SoT" | **강한 말을 한 뜻으로 좁힌다** | templates 10개 문구 수정 |
| 형식 SoT / 저장 SoT | 수식어로 가른다 | 수정 최소 | 같은 단어를 공유해 읽을 때 한 번 더 판단해야 한다 |

## Decision

### D1. `resources/` 를 신설하고 하위를 **층 이름**으로 둔다

```text
resources/
├── source/      type: reference    "이 자료가 뭐라고 했나"
├── concept/     type: concept      "이 개념은 뭔가"
└── synthesis/   type: permanent    "내 판단·전략은 뭔가"
```

폴더명과 층명이 1:1이 되고 **`permanent` 라는 겸직 이름이 디렉토리에서 사라진다.**

`source/` 와 `synthesis/` 는 flat 이다 — `concept/` 이 이미 flat 인 것과 같은 이유다(*"개념은 분류 트리가 아니라 링크 그래프로 조직된다"*, SPEC-001). **`SPEC-001` 의 `reference/{group}/` 는 낡은 줄이라 같은 개정에서 정정한다.**

### D2. `archive/` 를 최상위로 올린다

```text
permanent/archive/  →  archive/
```

`archive` 는 **층이 아니라 상태**다 — SPEC-001 이 이미 그렇게 적어 뒀고, `permanent`·`concept` 공용이며 앞으로 `reference` 도 내려간다. **상태를 층 아래 두면 그 층의 소유물처럼 읽힌다.**

`agent.md` 의 「지식층 읽기범위」가 `permanent/archive/` 를 cold 로 제외하고 있다(D-005) — 경로만 바뀌고 규칙은 그대로다.

### D3. `type` enum 은 바꾸지 않는다 — 폴더명만 층으로 간다

`type: permanent` 는 그대로 둔다. 폴더가 `synthesis/` 가 되는 순간 **`permanent` 는 더 이상 두 뜻이 아니다** — 그릇 노릇이 사라지고 type 이름 하나로 남는다.

`type` enum 은 [[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]] 이 정하고 `SPEC-002` 가 소유하는 **그래프 계약**이다. 같이 바꾸면 `_graph.json`·프론트·검증기까지 번지는데, **이 결정이 풀려는 문제는 거기 없다.**

### D4. `inbox/` 는 `resources/` 밖에 둔다

미소화 입력은 R 이 아니다. PARA 원안에서도 Inbox 는 별도 버킷이고, `inbox/` 는 그래프에서 **층에 속하지 않는다**(SPEC-001 — *"노드이되 층에 속하지 않고 `up:` 대상이 될 수 없다"*).

### D5. `products/` 와 `persona/` 는 이번에 건드리지 않는다

- **`products/` 는 428 파일**이다. R 재편과 섞으면 회귀면이 폭발하고, P 는 지금 이름과 뜻이 어긋나 있지 않다.
- **`persona/`(A 판정)는 후속 decision 이다.** 사용자가 *"일단 area 는 최종으로"* 로 미뤘고, R·Archive 를 먼저 세우면 남는 것이 하나뿐이라 그때 판단이 단순해진다.
- `products/*/_archive/`(버전 컷오프 동결본)는 **D2 의 `archive/` 와 다른 것**이다. 제품 버전 스냅샷이라 제품 폴더 안에 있는 것이 맞고, 옮기지 않는다.

### D6. `downloads/` 는 그대로 두고 **선언만 추가한다**

지우면 **DeskDeck 다운로드가 죽는다** — `main.py:180` 이 `PERSONA_DIR.parent / "downloads"` 를 `/download/*` 로 서빙한다. 서빙 경로가 코드에 박혀 있어 옮기면 코드·랜딩·runbook 이 같이 바뀌는데, **얻는 것이 "폴더가 정돈돼 보인다" 뿐이다.**

`SPEC-001` 레이아웃과 `agent.md` 에 **"운영 자산 · mac-remote RB-001 소유"** 로 적는다. 문제는 위치가 아니라 **주인이 문서에 없던 것**이었다.

### D7. `reports/` 는 해당 제품 아래로 옮긴다

```text
reports/PLAN-013-T-008-profile-be.md  →  products/ax-knowledge-graph/30-work/reports/
reports/PLAN-013-T-009-profile-be.md  →  (같은 곳)
```

`products/ax-knowledge-graph/log.md` 와 `30-work/` 가 이미 참조한다 — **주인이 명확한데 루트에 놓여 있었다.** 지우지 않는 이유는 WORK-009/010 의 완료 근거이기 때문이다.

두 파일은 frontmatter `type` 이 없어 **그래프 노드가 아니다**(navigational). 제품 폴더로 들어가도 노드가 늘지 않는다 — `_build_graph_nodes` 가 `type` 없는 파일을 건너뛴다.

### D8. `SoT` 를 한 뜻으로 좁힌다 — 양식은 **「양식 원천」**

| 말 | 뜻 | 어디 |
|---|---|---|
| **양식 원천** | 문서가 **어떻게 생겼나** | `templates/**` |
| **SoT** | 데이터가 **어디 사나** | `40-architecture/database` · DEC-009/012 |

`SoT` 는 강한 말이라 한 뜻으로 남긴다. **한 문서 안에서 두 뜻을 같은 단어로 쓰지 않는다**가 이 결정의 알맹이고, 명칭은 그 수단이다.

`rules/knowledge-note-pipeline.md:155`(*"템플릿은 형식의 SoT다"*)와 `templates/**` 10개가 대상이다.

### D9. 이동은 `git mv` 한 커밋이고, 위키링크는 안 깨진다

노드 식별자가 **파일명 stem** 이라([[decision-003-node-type-and-identifier|KDEV-DEC-003]]) `[[async-await]]` 같은 링크는 경로와 무관하다. Obsidian 도 stem 으로 푼다.

한 커밋으로 묶는 이유는 [[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D3 과 같다 — 나눠 커밋하면 중간 커밋에서 로더가 없는 경로를 보고 부팅이 막힌다.

### 기각

- **`permanent/` 안에 `reference/` 넣기(A안)** — 겸직이 심해지고 4층 위계가 뒤집힌다(source 가 synthesis 아래).
- **폴더명을 type 축으로(`reference`·`concept`·`permanent`)** — 수정은 적지만 `permanent` 이름이 남아 이 결정의 목적이 반만 달성된다.
- **혼합 축(`reference`·`concept`·`notes`)** — 고치려는 병(한 단어 두 뜻)을 새 폴더에 그대로 옮긴다.
- **`resources/` flat** — 14개일 땐 되지만 늘면 층이 섞이고, 그때 다시 나누는 비용이 지금보다 크다.
- **`type` enum 까지 `synthesis` 로 개명** — 그래프 계약(SPEC-002)까지 번지는데 이 결정이 푸는 문제는 거기 없다.
- **`downloads/` 삭제·이동** — 운영 자산이고 서빙 경로가 코드에 박혀 있다. 문제는 위치가 아니라 선언 부재였다.
- **`reports/` 삭제** — WORK-009/010 의 완료 근거다.
- **`products/*/_archive/` 를 `archive/` 로 합치기** — 제품 버전 스냅샷이라 성격이 다르다.

## Rationale

- **판단 기준** — 이름이 뜻과 어긋나면 매번 해석 비용이 든다. `permanent/concept/` 를 볼 때마다 *"영구노트 안의 개념인가, 개념이 영구노트의 한 종류인가"* 를 다시 판단하게 되는데 **실제로는 둘 다 아니고 형제**다.
- **지금이 가장 싸다** — 지식층 14 파일, 옮길 둘 중 하나는 비어 있다. R 이 커진 뒤엔 파일 이동·링크 정합·아카이브 충돌이 전부 따라온다.
- **위험이 낮다는 근거가 코드에 있다** — `layer` 를 `type` 에서 도출한 DEC-010 D3 덕에 폴더 이동이 그래프를 안 건드린다. *"같은 사실을 두 곳에 두면 언젠가 어긋난다"* 던 그 결정이 지금 이 이동을 싸게 만든다.
- **대안 대비** — C(문서로만 정의)는 코드가 0이지만 **폴더를 여는 사람에겐 안 보인다.** 이 결정이 푸는 것은 코드 동작이 아니라 **읽는 사람의 해석 비용**이라, 폴더에 안 드러나면 푼 게 아니다.
- **리스크**
  - `LAYER_PREFIX` 접두 충돌 — `resources/` 아래 셋이 같은 접두를 공유한다. 판정 순서를 잘못 짜면 `synthesis` 문서가 `concept/` 로 가도 통과할 수 있다. 지금 코드에 같은 형태의 방어가 이미 있다(`permanent` 인데 `permanent/concept/` 아래면 위반).
  - `_enrich_permanent` 의 경로 기반 `type` 기본값 — `"concept" in path.parts` 가 새 경로에서도 맞는지 확인이 필요하다. `resources/concept/` 는 여전히 맞다.
  - **중간 커밋 부팅 실패** — 로더가 없는 경로를 보면 `PersonaError` 다. D9 의 한 커밋 규율이 유일한 방어다.
  - 외부 참조 — 노트에 절대 경로를 적어 둔 곳이 있으면 깨진다. 링크는 stem 이라 안전하지만 **본문의 경로 문자열**은 검사해야 한다.

## Scope

- **In** — `resources/{source,concept,synthesis}/` 신설 · `archive/` 최상위 승격 · `reports/` → `products/ax-knowledge-graph/30-work/reports/` · `downloads/` 선언 추가 · `persona_loader` 3곳 · `apply/plan.py` 3곳 · `agent.md` 경로표 · `rules/knowledge-note-pipeline.md` · `templates/knowledge/` 4개 · SPEC-001·004·005 개정 · **「양식 원천」 명칭 전환**(templates 10개).
- **Out** — `persona/` A 판정(후속 decision) · `products/` 재편 · `type` enum 개명 · `products/*/_archive/` 통합 · `inbox/` 이동 · `downloads/` 이동.
- **영향을 받는 spec 후보** — `SPEC-001`(레이아웃·층 매핑·`{group}` 낡은 줄), `SPEC-004`(검증 경로), `SPEC-005`(열람 표면 경로), `SPEC-010`(`ALLOWED_PREFIXES`).

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | `persona/` 를 A 로 볼 때 **A-1 지속 책임** vs **A-2 공개 표면** | kknaks | 후속 decision. A-2 면 `showcase.md` 가 P→A 로 넘어가 [[decision-017-product-registry-and-admin-scaffold\|KDEV-DEC-017]] D2(통합)를 재검토해야 한다 |
| OQ-2 | 본문에 절대 경로를 적어 둔 노트가 있는지 | kknaks | work 착수 시 `reference/`·`permanent/` 문자열 전수 검사 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-001-directory-structure\|KDEV-SPEC-001]] | **update (완료 v0.0.6)** | 층 매핑 · 레이아웃 트리 · 시나리오 · 자동 갱신 경로 · 체크리스트 · `downloads`·`reports` 소유 명시 · `{group}` 낡은 OQ 무효 처리 |
| [[spec-005-graph-visualization\|KDEV-SPEC-005]] | **update (완료 v0.0.4)** | 트리 렌더 경로. **렌더 규칙은 무변경** — 트리가 디렉토리를 그대로 비추므로 폴더가 바뀌면 따라간다 |
| [[spec-004-graph-validation\|KDEV-SPEC-004]] | **불필요** | 경로 언급 2건이 전부 **과거 기록**이다(WORK-005 서술 · 해소된 OPEN). 검증 규칙은 `type`·`layer` 로 쓰여 있고 디렉토리를 안 본다 |
| [[spec-010-apply-executor\|KDEV-SPEC-010]] | **불필요** | 경로 계약을 **SPEC-001 에 위임**한다(§검증 표: *"층-경로 정합 · `type`이 디렉토리와 일치 · KDEV-SPEC-001"*). 허용목록의 구체 경로를 이 spec 이 갖고 있지 않다 |

**계약을 위임해 둔 값이 여기서 나왔다.** 넷을 고칠 줄 알았는데 둘로 끝났다 — SPEC-010 이 경로를 자기 문서에 복사하지 않고 SPEC-001 을 가리켜 뒀고, SPEC-004 는 규칙을 `type`/`layer` 로 썼기 때문이다. **디렉토리를 아는 문서가 하나뿐이라 디렉토리를 바꾸는 비용이 하나다.**
