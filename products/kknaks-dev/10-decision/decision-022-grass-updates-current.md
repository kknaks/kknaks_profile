---
type: decision
id: KDEV-DEC-022
title: "잔디가 current.md 의 「진행 중」만 갱신한다"
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
    - "[[baseline-007-update-lines-by-case|KDEV-BL-007]]"
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
  decisions:
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
    - "[[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]]"
  specs:
    - "[[spec-012-grass-artifacts|KDEV-SPEC-012]]"
  works: []
  releases: []
  related: []
up: []
---

# 잔디가 current.md 의 「진행 중」만 갱신한다

잔디 착지에 **`context/{company,studio}/current.md`** 를 더한다. 다만 파일 전체가 아니라 **「진행 중」 표 하나만** 갈아 끼운다.

## Context

- 관련 baseline: [[baseline-007-update-lines-by-case|KDEV-BL-007]]
- **`current.md` 가 죽어 있다.** `context/company/current.md` 는 71일, `context/studio/current.md` 는 59일 방치다(2026-08-11 기준). 「이번 주 목표: context 라우팅 구조를 정리한다」가 두 달 전에 끝난 일로 남아 있고, `studio` 는 제품 13개 중 6개만 적혀 있다.
- **아무도 갱신하지 않는다.** 잔디는 `career` 를 갱신하지만 `current.md` 는 건드리지 않는다. 사람의 규율에만 기대는 문서는 갱신되지 않는다 — [[spec-003-knowledge-workflow|KDEV-SPEC-003]] 가 「그 리뷰 단계가 구현된 적이 없다」로 이미 겪은 실패다.
- **커밋이 그 정보를 갖고 있다.** 어느 레포에 무엇을 했는지는 잔디가 이미 조사한다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 파일 전체를 갱신안으로 교체 | 단순 | **사람이 정한 우선순위·목표·blocker 가 매일 덮인다** | 기각 |
| B | 갱신하지 않는다(현행) | 사람 소유가 확실 | 두 달째 죽어 있다 | 기각 |
| **C** | **「진행 중」 표만 갈아 끼운다** | 커밋에서 나오는 것만 쓴다. 사람 몫은 건드릴 방법 자체가 없다 | 섹션 경계를 지켜야 한다 | **채택** |

## Decision

### D1. 착지에 `context/{company,studio}/current.md` 를 더한다

[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]] D1 의 착지 셋(daily·career·concept)에 하나를 더한다.

| 경로 | 액션 | 조건 | 갱신 범위 |
|---|---|---|---|
| `context/company/current.md` | 섹션 replace | `type=company` 커밋 있음 | **`## 진행 중` 표만** |
| `context/studio/current.md` | 섹션 replace | `type=studio` 커밋 있음 | **`## 진행 중` 표만** |

귀속은 `tracked_repos.type` 이 정한다 — career 귀속과 같은 값이다([[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]] D1).

### D2. 커밋에서 나오는 것만 쓴다

| 섹션 | 소유 | 왜 |
|---|---|---|
| `## 진행 중` | **시스템** | 어느 레포에 무엇을 했는지는 커밋이 말한다 |
| `## 현재 우선순위` | 사람 | P0/P1 과 Goal 은 판단이다 |
| `## 이번 주 목표` | 사람 | 〃 |
| `## Blockers` | 사람 | 〃 |
| `## 목적` · `## 운영 원칙` · `## 현재 상황` | 사람 | 잘 안 바뀌는 정의 |

**갱신안은 「진행 중」 표만 담는다.** 다른 섹션이 담기면 발행을 거부한다 — `career` 의 `PROTECTED_CAREER_FIELDS` 와 같은 규율이다. 무시하는 것이 아니라 **애초에 담기지 않아야** 한다.

### D3. 섹션 밖은 텍스트 그대로 이어 붙인다

`render_career` 가 겪은 것을 반복하지 않는다 — 종전에 frontmatter 를 파싱해 왕복했더니 **값은 보존되지만 주석이 사라지고 키가 재정렬**돼, 본문만 바뀌어야 할 발행이 42 insertions / 38 deletions 를 냈다.

`current.md` 도 같다. **`## 진행 중` 헤더부터 다음 `## ` 직전까지만** 교체하고 나머지는 문자 그대로 남긴다. 사람이 적어 둔 주석·빈 칸·순서도 그 사람의 것이다.

### D4. `context/` 를 발행 허용 경로에 넣는다

`ALLOWED_PREFIXES` 에 `context/` 가 없어 지금은 발행이 거부된다. 더한다.

**다만 `context/` 는 여전히 계보 밖이다**([[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]] D4) — `up:` 을 갖지 않고 그래프 노드도 아니다. 쓰기 대상이 되는 것과 계보에 드는 것은 다른 축이다.

### D5. 양식 원천을 만든다

`templates/context/current.md` 를 둔다. `career` 가 `templates/persona/career.md` 를 갖는 것과 같다 — 형식 규칙을 프롬프트에 복사하지 않는다.

## Rationale

- **판단 기준**: 커밋이 말할 수 있는 것만 기계가 쓴다. 나머지는 사람이 쓰되, **쓰지 않으면 죽는다는 사실을 문서가 드러내야** 한다.
- **대안 대비 이유**: A 는 사람의 판단을 매일 덮고, B 는 이미 두 달 실패했다.
- **리스크**: 섹션 경계를 문자열로 찾으므로 사람이 헤더 이름을 바꾸면 갱신이 멈춘다. **조용히 멈추지 않게** 헤더가 없으면 발행을 거부한다.

## 근거 개념

- [[immutability]] — 사람 소유 섹션을 **고쳐 쓰지 않고 그대로 이어 붙인다.** 값이 같으면 되는 것이 아니라 주석·순서·빈 칸까지 원본이어야 한다는 것이 `render_career` 의 교훈이다
- [[service-layer]] — 「무엇을 갱신할지」를 정하는 자리와 「어떻게 쓸지」를 아는 자리를 가른다. 게이트가 갱신안을 만들고 Apply Executor 가 파일을 쓴다

## Scope

- In: `KDEV-SPEC-012` 착지 표 · `ALLOWED_PREFIXES` · `templates/context/current.md` · 섹션 보호 규칙
- Out: 게이트가 실제로 갱신안을 내보내는 구현 — 후속 work

## Open Questions

없음. 둘 다 2026-08-12 에 닫았다.

### D6. 열 구성은 두 영역이 같다 (OQ-1 해소)

`Project | Work | Status | Blocker | Next` 하나다. company 의 `Experience` 열을 `Work` 로 바꾼다.

- **그 열은 한 번도 안 채워졌다.** 두 행 다 비어 있었다.
- **그 축은 이미 `persona/career/` 가 갖는다** — `## 챌린지` · `## 배운 점` · `## 대표 작업` 이고, 잔디가 그 문서를 이미 자동 갱신한다(D1). 여기 두면 같은 사실이 두 곳에 산다.
- 열이 갈리면 프롬프트도 area 별로 갈라야 하고 템플릿도 둘이 된다. 얻는 것 없이 분기만 는다.
- **지금 정하지 않으면 사고로 일어난다.** `templates/context/current.md` 는 이미 `Work` 하나로 선언돼 있어서, 게이트 첫 실행이 `Experience` 를 조용히 갈아치웠을 것이다.

### D7. 행의 수명은 `Status` 가 정한다 (OQ-2 해소)

표는 새로 쓰는 것이 아니라 **고쳐 쓴다**(D3 과 같은 규율이 행 단위로 내려온 것이다).

| Status | 그날 커밋이 없으면 |
|---|---|
| `todo` · `in_progress` · `blocked` | **남는다.** 안 건드렸다는 것이 끝났다는 뜻은 아니다 |
| `done` | **다음 갱신에서 뺀다.** 한 회차만 보이고 사라진다 |

- 「그날 커밋 있는 것만 남긴다」를 기각한 이유: 어제 남긴 `todo` 가 매일 사라졌다 나타난다. 하다 만 것을 잊는 표가 된다.
- 「전부 남긴다」를 기각한 이유: `done` 이 쌓여 제품 수만큼 늘고, 「지금 무엇을 하고 있나」가 아니게 된다.
- `done` 을 오래 안 두는 근거는 **그 기록을 이미 다른 문서가 갖는다**는 것이다 — 그날 끝낸 것은 `persona/daily/`, 이력으로 남을 것은 `persona/career/`.

**이 둘은 검증이 아니라 작성 규칙이다.** 섹션 소유(D2)처럼 발행을 막지 않는다 — 행 내용은 판단이라 「담기면 거부」로 다룰 수 없고, 어긋나면 표에서 바로 보인다. 대가로 그날 잔디를 통째로 실패시키지 않는다.

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| KDEV-SPEC-012 | update | 착지 경로에 `context/{company,studio}/current.md` 추가. 섹션 단위 replace 계약 |
