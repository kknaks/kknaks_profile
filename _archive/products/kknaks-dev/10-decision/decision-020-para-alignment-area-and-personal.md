---
type: decision
id: KDEV-DEC-020
title: "PARA 정렬 마무리 — 개인 영역 신설, A는 귀결, daily 는 개인 이력"
status: accepted
product: kknaks-dev
created_at: 2026-08-11
updated_at: 2026-08-11
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]"
  decisions:
    - "[[decision-018-resources-layout-and-sot-naming|KDEV-DEC-018]]"
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
    - "[[decision-019-drop-synthesis-layer|KDEV-DEC-019]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-012-grass-artifacts|KDEV-SPEC-012]]"
  works: []
  releases: []
  related: []
up: []
---

# PARA 정렬 마무리 — 개인 영역 신설, A는 귀결, daily 는 개인 이력

[[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]이 R·Archive만 정렬하고 **A를 명시적으로 미뤄 둔** 자리를 닫는다. 「일단 area는 최종으로 가고」로 유보했던 것이고, [[decision-018-resources-layout-and-sot-naming|KDEV-DEC-018]]도 「`persona/`(A 판정)는 후속 decision」이라 적어 두었다. R이 세워졌으니 지금이 그 후속이다.

## Context

- 관련 baseline: [[baseline-006-para-alignment-and-sot-map|KDEV-BL-006]]
- **문제 1 — 최상위가 없다.** 옵시디언에서 P(287)·R(509)·rules 세 덩어리가 각자 떠 있다. 문서는 있는데 `agent.md`·`context/index.md`·`context/kknaks.md`가 서로를 **경로 문자열로** 가리켜 그래프가 그리지 못한다(세 파일 모두 `[[]]` 0개).
- **문제 2 — R이 붙을 영역이 없다.** `context/kknaks.md`의 영역이 회사·여름별컴퍼니 둘뿐이라, 개념 363건이 어느 영역에도 속하지 못한다.
- **문제 3 — A의 성격이 안 정해졌다.** `persona/`가 영역인지 산출물인지 불명확해, daily를 career에 귀속시키려다 **하루에 두 영역이 섞인다**는 사실과 충돌했다(100건 중 67건이 회사+개인 혼재, 회사만인 날은 0건).

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | A = `context/{company,studio}` (영역 정의가 A) | 영역이 곧 A라 직관적 | `persona/`가 갈 곳이 없고, 정체성과 A가 같은 것이 된다 | 기각 |
| B | A = `persona/` 를 영역의 한 갈래로 | 트리가 단순 | daily가 여러 영역에 걸쳐 트리로 안 담긴다 | 기각 |
| **C** | **A = `persona/` 이되 「귀결」이다** | 정체성 → 영역 → 작업(P·R) → **귀결(A)** 의 흐름. daily 혼재 문제가 사라진다 | 트리가 아니라 파이프라인이라 한 번에 안 보인다 | **채택** |

## Decision

### D1. 정체성 아래 영역 셋 — 개인 영역을 신설한다

- `context/kknaks.md`가 **정체성**이고 그 아래 영역이 셋이다: **회사 · 여름별컴퍼니 · 개인**.
- **`context/personal/{current,projects}.md` 를 신설**한다. 회사·여름별컴퍼니가 **역할**이라면 개인은 **사람 이건학 본인**이다 — 회사 업무도 제품 개발도 아닌, 사람에게 속하는 것이 이 영역이다.
- 개인 영역이 갖는 것은 둘이다. **배움**(`resources/` 자료·개념)과 **이력**(`persona/daily/` 그날 한 일 전부).
- **R(`resources/`)은 개인 영역의 산출**이다. `idempotency`·`transaction` 은 회사 것도 사업체 것도 아니라 어디에도 못 붙어 있었다.
- 회사에서 배운 것이라도 **개념이면** 개인 영역이다. 회사 경험 기록(챌린지·성과)은 `context/company/` 다 — 축이 다르다.

### D2. PARA 배치

| 버킷 | 어디 | 소속 |
|---|---|---|
| **P** | `products/` | 여름별컴퍼니 영역 (`context/studio/projects.md` 의 Product SSOT 열이 이미 가리킨다) |
| **R** | `resources/{source,concept}` | 개인 영역 |
| **A** | `persona/` | **영역의 하위가 아니라 세 영역이 흘러드는 귀결** |
| **Archive** | `archive/` | 지금 비어 있다(README만) |

### D3. A는 트리의 가지가 아니라 귀결이다

**정체성 → 영역 → 작업(P·R·커밋) → 귀결(A)** 의 흐름이다. `persona/` 는 세 영역이 **공개로 나가는 출구**이지 한 영역의 하위가 아니다.

- `career/` ← 회사 영역 (잔디: 커밋 → `daily` → `career`)
- `showcase.md` ← P 제품
- `posts/` ← R 개념이 글이 된 것
- `profile.md` ← 정체성의 공개면

### D4. 계보 방향 — `up:` 은 귀결이 건다

**읽기 순서와 계보 방향이 반대다.**

| | 방향 |
|---|---|
| 읽기 | `context` → 영역 → P·R |
| 계보(`up:`) | **persona ──up──▶ P · R · `persona/daily`** |

「내가 무엇을 하는 사람인가」는 **실제로 한 일에서 나온다.** 그래서 귀결이 자기 근거를 가리킨다.

- `persona/career/{회사}` ──up──▶ `persona/daily/{그 회사 커밋이 있던 날들}`
- `persona/posts/{글}` ──up──▶ `resources/concept/{개념}`
- `products/*/showcase.md` ──up──▶ 그 제품의 decision·spec
- `persona/profile.md` ──up──▶ `career` 5건

**`context/` 는 계보에 들어가지 않는다** — 정의이지 산출물이 아니다.

**이 방향만 검증을 통과한다.** L4는 층이 있는 노드에서만 발화하는데(`if src_layer`), persona 는 층이 없어 자유롭게 `up:` 을 걸 수 있다. 반대로 P(execution)가 층 없는 노드를 `up:` 하면 ERROR다.

### D5. `persona/daily/` 는 그 자리에 둔다 — 개인 영역의 이력이다

daily 는 하루에 회사·제품·개인이 섞여(100건 중 67건 혼재, 회사만인 날 0건) 어느 **역할**에도 귀속되지 않는다. 그것이 애매함의 원인이 아니라 **daily 가 사람 단위 기록**이라는 뜻이다 — 사람은 하나이므로 역할별로 갈리지 않는다.

그래서 daily 는 **개인 영역의 이력**이고, `career` 와 축이 다른 짝이다.

| | 무엇 | 단위 | 공개 |
|---|---|---|---|
| `persona/daily/` | 그날 한 일 **전부** | 사람 | 본문 비공개 · `counts`·`summary` 가 잔디로 렌더 |
| `persona/career/` | 회사 것만 추린 정리본 | 역할 | 본문이 경력 페이지에 렌더 |

career 가 daily 에서 **회사 부분을 추려 간다**([[decision-015-grass-destinations-and-formats|KDEV-DEC-015]] D1 의 `type=company` 조건). 원장에서 역할별로 추려 가는 구조다.

> **한 번 `journal/` 로 뺐다가 되돌렸다.** 「A 는 귀결(공개 표면)이니 재료는 밖」이라는 근거였는데 둘이 안 맞았다 — ① 잔디(`counts`·`summary`)가 **사이트에 렌더되는 기능**이라 persona 안이 맞고, ② `career`(회사 이력)와 `daily`(개인 이력)가 같은 「이력」인데 하나만 밖으로 나가 대칭이 깨졌다.

### D6. 회사 제품은 P에 넣지 않는다

Charty·Linky 는 `context/company/projects.md` 의 표로 충분하다. 회사 코드 작업은 이 레포의 목적이 아니고(`context/company/projects.md` 「경계」), 제품 문서 파이프라인을 태울 이유가 없다.

### D7. 이번에 하지 않는 것

- **그래프 배선** — `persona_loader` 가 profile·career·daily 를 노드로 만드는 것. `up:` 을 걸어도 지금은 옵시디언에서만 보이고 `_graph.json` 에는 안 나타난다.
- **링크 작업** — `context` → PARA 의 경로 문자열을 `[[]]` 로 바꾸는 것.

둘을 **한 번에** 한다. D5 를 되돌린 덕에 경로 코드는 손댈 것이 없다 — `plan.py`·로더가 보던 `persona/daily/` 가 그대로다.

## 근거 개념

없음 — 디렉토리 배치와 영역 구획은 이 레포의 운영 판단이고 기댈 개념이 없다.

## Scope

- In: `context/kknaks.md` · `context/personal/**` · `rules/persona-artifacts.md` · `KDEV-SPEC-001`
- Out: 그래프 배선 · A 의 `up:` 작업 (D7)

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | `persona/{contents,posts,algorithms}` 가 귀결의 무엇인지 | kknaks | posts 는 R→글 경로인데 1건뿐이다. 경로가 도는지 먼저 본다 |
| OQ-2 | Archive 를 언제 쓰기 시작하나 | kknaks | 지금 비어 있다. 안 쓰게 된 개념이 생길 때 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| KDEV-SPEC-001 | update | `context/personal/` 추가 |
| KDEV-SPEC-012 | — | 착지 경로 변경 없음 |
