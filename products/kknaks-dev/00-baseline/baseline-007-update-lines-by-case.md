---
type: baseline
id: KDEV-BL-007
title: "업데이트 라인 케이스 정리 — 서버 승인 게이트 · 로컬 작업"
status: raw
product: kknaks-dev
source:
  type: idea
  ref: "PARA 연결(KDEV-DEC-020) 뒤 「이걸 규칙에 맞게 업데이트하는 라인」을 케이스별로 정리하려는 작업"
links:
  baselines:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
    - "[[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]"
  decisions:
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
    - "[[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]]"
  specs:
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
    - "[[spec-012-grass-artifacts|KDEV-SPEC-012]]"
  works: []
  releases: []
  related: []
created_at: 2026-08-11
updated_at: 2026-08-11
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/raw
---

# 업데이트 라인 케이스 정리 — 서버 승인 게이트 · 로컬 작업

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

무엇이 어디로 들어와 어디에 앉는지를 **케이스별로** 늘어놓는다. [[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]]이 자리(PARA)를 정했으니, 다음은 **그 자리로 가는 라인**이다.

## Raw

축이 둘이다.

```
서버(승인 게이트)   스케줄·외부 입력 → DB 큐 → 게이트 → 승인분만 발행
로컬(사람·에이전트) 직접 작성 → pre-commit 검사 → 커밋
```

### 확인된 사실

**입구는 `inbox/` 가 아니다.** [[decision-011-approval-gate-chain|KDEV-DEC-011]] D1 이 뒤집었다 —

> **승인 큐는 DB에 둔다.** 승인 전에는 레포에 파일이 생기지 않는다. …
> **`inbox/` 는 "보류함"으로 역할을 바꾼다** … 즉 `inbox/` 도 **하나의 목적지**이지 대기열이 아니다.

다만 `app/back/service/knowledge_capture/render.py:38` 이 아직 `inbox/` 로 직접 쓴다(게이트 이전 구현 잔존). **어느 쪽이 현행인지 확인이 필요하다.**

## 케이스

### 서버 — 승인 게이트

| # | 케이스 | 입구 | 종착지 | 상태 |
|---|---|---|---|---|
| 1 | 잔디잡 | **09:05 KST** 스케줄 → 접수 → DB 큐 | `persona/daily/` · `persona/career/{회사}` · `resources/concept/` | 돈다 |
| 2 | 유튜브 콘텐츠 | Slack URL·업로드 → DB 큐 | `resources/source/` · `resources/concept/` · `persona/contents/` · `inbox/`(보류) · 폐기 | 돈다 |
| 3 | 블로그 글 | — | `persona/posts/` | **미구현** |

- 1은 **route 게이트가 없다** — 목적지가 고정이라 고를 것이 없다([[decision-015-grass-destinations-and-formats|KDEV-DEC-015]] D1).
- 2는 route 게이트가 **목적지 조합**을 고른다([[spec-008-gate-chain|KDEV-SPEC-008]]).

#### 1. 잔디잡 워크플로우

```mermaid
flowchart TD
    S(["09:05 KST 스케줄<br/>daily-activity"]) --> I["intake<br/>어제 날짜 item 접수"]
    I --> Q[("DB 큐<br/>item + stage")]

    Q --> C["collect · auto<br/>LLM 없음 — git 을 읽고 센다"]
    C --> C1["tracked_repos 조회<br/>slug · type · detail · product_slug · enabled"]
    C1 --> C2["레포별 커밋 수집"]
    C2 --> C3["career 귀속 판정<br/>type=company → detail = career stem"]
    C3 --> C4["counts 집계<br/>commit · note · study"]

    C4 --> V["investigate · auto<br/>레포마다 1건 — 유일한 N 제출 스테이지"]
    V --> V1["레포별 diff 조사<br/>무엇을 왜 했나"]

    V1 --> G{{"daily · gate<br/>사람 승인"}}
    G -->|"작성도 여기서 한다"| G1["daily 본문 · summary<br/>career 갱신안 · concept 후보"]
    G1 --> G2{"승인?"}
    G2 -->|"재생성"| G1
    G2 -->|"거절"| X(["종료 — 발행 없음"])
    G2 -->|"승인"| A["Apply Executor<br/>원자적 발행"]

    A --> D1["persona/daily/{YYYY-MM-DD}.md<br/>upsert · 활동 &gt; 0 · auto:false 아님"]
    A --> D2["persona/career/{stem}.md<br/>replace · type=company 커밋 있음 · is_current · changed"]
    A --> D3["resources/concept/{slug}.md<br/>upsert · 개념 후보 + 승인"]
    A --> D4["git commit + push"]
```

**세 가지가 통념과 다르다.**

1. **스케줄 잡은 접수만 한다.** 조사·작성·발행은 드라이버와 게이트가 이어받는다 — 종전에는 잡 안에서 다 해서 **사람 승인 없이 레포에 쓰였다**(`scheduler.py` 주석, KDEV-WORK-017 P5).
2. **`compose` auto 스테이지가 없다. 작성은 게이트가 한다.** 재생성이 「서술만 다시 만든다」라 게이트도 작성 능력이 필요했고, auto 쪽 작성은 첫 회에만 쓰여 중복이 되기 때문이다(`definitions.py` 주석).
3. **게이트가 하나뿐이라 승인이 곧 체인 종료이자 발행 트리거**다.

#### 2. 유튜브 콘텐츠 워크플로우

```mermaid
flowchart TD
    IN1(["Slack URL 수신"]) --> N["normalize_url<br/>detect_source_kind"]
    IN2(["제품 화면 URL 입력"]) --> N
    IN3(["inbox md 업로드"]) --> N
    N --> Q[("DB 큐<br/>source_kind=youtube")]

    Q --> C["collect · auto<br/>원문·자막 수집"]
    C --> S["summarize · auto<br/>판단 재료만 만든다 — 노트 작성 아님"]

    S --> R{{"route · gate<br/>★ 목적지 조합을 고른다"}}
    R --> R1{"exclusive?"}
    R1 -->|"보류"| H["inbox/{날짜}-{slug}.md<br/>idea 1장 발행하고 종료"]
    R1 -->|"폐기"| X(["종료 — 이후 스테이지 없음"])
    R1 -->|"아니오"| E["enabled_stages()<br/>켠 목적지만 게이트를 연다"]

    E -.->|"reference on"| G1{{"source_note · gate"}}
    E -.->|"concept on"| G2{{"concept · gate"}}
    E -.->|"derived on"| G3{{"derived · gate"}}

    G1 --> A["Apply Executor<br/>원자적 발행"]
    G2 --> A
    G3 --> A

    A --> D1["resources/source/{날짜}-{slug}.md"]
    A --> D2["resources/concept/{slug}.md<br/>concept_index 로 기존 개념 매칭"]
    A --> D3["persona/contents/**"]
    A --> D4["git commit + push"]

    G2 -.->|"이 목적지가 아님"| R
```

**잔디와 다른 점 넷.**

1. **입구가 사람이다.** Slack·화면 입력·업로드 셋 다 사람이 시작한다. 잔디만 스케줄이 시작한다.
2. **`route` 게이트가 체인 길이를 정한다.** `enabled_stages()` 가 켠 목적지만 뒤 게이트를 연다 — 아무것도 안 켜면 게이트가 없다.
3. **배타 옵션이 있다.** 보류(`inbox/` 1장 발행 후 종료)와 폐기(즉시 종료)는 뒤 게이트를 만들지 않는다.
4. **유일한 역방향 전이가 있다.** 뒤 게이트에서 「이 목적지가 아님」을 내면 `route` 가 재오픈된다. 자동 스테이지(수집·요약) 결과는 재사용한다 — 목적지 오판 때문에 자막을 다시 받지 않는다.

`summarize` 는 **판단 재료만** 만들고 **노트 작성은 게이트가 한다** — 잔디의 `daily` 게이트가 작성하는 것과 같은 대칭이다.

### 로컬 — 사람·에이전트

| # | 케이스 | 입구 | 종착지 | 상태 |
|---|---|---|---|---|
| 4 | product 작업 | 직접 | `products/{제품}/{00-baseline…70-runbook}` + 근거 개념이 없으면 `resources/{source,concept}` | 돈다 |
| 5 | 공부 노트 | 직접 | `resources/source/` → `resources/concept/` | **미구현** |

- 4는 pre-commit 이 강제한다 — decision 의 `up:`·「근거 개념」 절, 그래프 L1~L6.

## Context

[[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]] 이 자리를 정했다.

```
정체성  context/kknaks.md      회사 · 여름별컴퍼니 · 개인
작업    P products/  ·  R resources/  ·  이력 persona/daily/
귀결    A persona/   career · posts · showcase · profile
```

각 케이스의 종착지가 이 배치의 어디에 앉는지가 정리의 기준이다.

## Why It Matters

**같은 자리에 두 축이 쓴다.** `resources/concept/` 는 케이스 1·2·4·5 넷이 모두 쓰고, `persona/` 는 1·3이 쓴다. 축마다 다른 규칙으로 쓰면 같은 디렉토리가 두 모양이 된다.

그리고 **비어 있는 칸이 드러난다** — 3·5가 미구현이고, 그 둘이 각각 「R → 글」과 「배움 → 개념」이라 **개인 영역의 산출 경로 둘이 다 비어 있다.**

## Possible Direction

아직 결정은 아니지만 가능한 방향.

- (비워 둠 — 케이스별로 채운다)

## 미결

| ID | 질문 |
|---|---|
| OQ-1 | `knowledge_capture/render.py` 의 `inbox/` 직접 쓰기가 현행인가, 게이트 이전 잔재인가 |
| OQ-2 | 게이트 목적지에 `products/` 가 없다 — P 는 로컬만 만드는 것이 맞나 |
| OQ-3 | `persona/posts/` 를 누가 만드나 — 게이트(3)인가 로컬인가 |
| OQ-4 | 케이스 5(공부 노트)가 게이트를 타야 하나, 로컬로 끝내야 하나 |
