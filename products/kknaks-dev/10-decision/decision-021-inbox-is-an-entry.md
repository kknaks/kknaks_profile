---
type: decision
id: KDEV-DEC-021
title: "inbox 는 입구다 — 보류 목적지를 없앤다"
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
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
  decisions:
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
  specs:
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
  works: []
  releases: []
  related: []
up: []
---

# inbox 는 입구다 — 보류 목적지를 없앤다

[[decision-011-approval-gate-chain|KDEV-DEC-011]] D1 의 `inbox/` 규정을 뒤집는다. 「보류함(목적지)」에서 **공부 노트의 입구**로 바꾸고, route 게이트의 배타 옵션에서 `inbox_hold` 를 뺀다.

> DEC-011 D1 의 나머지(**승인 큐는 DB에 둔다** · 승인 전에는 레포에 파일이 생기지 않는다)는 그대로다. 바뀌는 것은 `inbox/` 디렉토리의 역할 하나다.

## Context

- 관련 baseline: [[baseline-007-update-lines-by-case|KDEV-BL-007]] 케이스 5(공부 노트)
- **DEC-011 D1 이 정한 것**: 「`inbox/` 도 **하나의 목적지**이지 대기열이 아니다」. 근거는 둘이었다 —
  ① 미커밋 md 는 `git reset --hard origin/main` 에 사라지므로 대기열을 작업트리에 둘 수 없다
  ② 노트북에서 옵시디언을 열었을 때 「이런 것도 있었지」가 보여야 한다
- **①은 입구에 적용되지 않는다.** `reset --hard` 가 지우는 것은 **미커밋** 파일이다. 사람이 `inbox/` 에 넣고 **push 한 파일은 이미 커밋돼 있어** 날아가지 않는다. 그 위험은 **AI 가 만든 미커밋 초안**의 것이고, 그래서 초안은 DB 에 둔다([[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D1).
- **②는 입구여도 성립한다.** 옵시디언에서 보이는 것은 같고, **처리되면 사라진다**는 점만 다르다.
- **결정적으로, 보류 목적지는 한 번도 쓰이지 않았다.** `inbox_hold` 로 들어온 파일이 0건이다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 목적지 유지 + 입구 역할을 얹는다 | 기존 결정을 안 건드림 | **한 디렉토리가 두 역할**을 갖는다 — 비어 있어야 하는지 쌓여야 하는지 정할 수 없다 | 기각 |
| B | 입구는 새 디렉토리(`intake/` 등)에 둔다 | 역할이 갈린다 | 디렉토리가 하나 늘고, 쓰인 적 없는 목적지를 위해 이름을 비켜 준다 | 기각 |
| **C** | **입구 하나로 하고 보류 목적지를 없앤다** | 역할이 하나. **쓰인 적 없는 기능을 지우는 것**이라 잃는 것이 없다 | 「버리긴 아깝다」를 담을 자리가 사라진다 | **채택** |

## Decision

### D1. `inbox/` 는 입구다

- **공부 노트의 입구**다([[baseline-007-update-lines-by-case|KDEV-BL-007]] 케이스 5). 사람이 노트를 넣고 push 하거나 로컬 스킬로 만든다.
- **서버에서는 항상 비어 있는 상태**를 유지한다. 접수할 때 본문을 DB 큐로 옮기고 파일을 지운다 — **파일이 있으면 곧 미처리**다.
- 접수 전에 **DB 큐를 조회해 이미 있으면 skip** 한다. 승인이 늦어 큐에 머무는 동안 같은 파일이 다시 push 돼도 두 번 접수되지 않는다.
- 트리거는 **FastAPI 시작 프로세스(lifespan) 스캔**이다.

### D2. route 게이트의 `inbox_hold` 를 없앤다

- 배타 옵션이 **`discard`(폐기) 하나만** 남는다.
- 「버리긴 아깝지만 지금 정제 못 하겠다」는 **폐기하거나, 산출물을 하나 켜서 만들거나** 둘 중 하나다. 중간 상태를 두지 않는다.
- 쓰인 적이 없으므로 마이그레이션 대상 데이터가 없다.

### D3. `inbox/` 는 `type: idea` 를 갖는다

입구에 놓인 파일은 여전히 `idea` 다 — 층에 속하지 않고 `up:` 대상이 될 수 없다. 접수되면 사라지므로 **그래프에 오래 남지 않는다.**

## Rationale

- **판단 기준**: 한 디렉토리가 두 역할을 가지면 「비어 있어야 하나」에 답할 수 없다. 그리고 **쓰인 적 없는 기능을 지키느라 쓸 기능을 비틀지 않는다.**
- **대안 대비 이유**: A 는 역할 충돌을 그대로 남기고, B 는 0건짜리 목적지를 위해 디렉토리를 하나 더 만든다.
- **리스크**: 「버리긴 아깝다」를 담을 자리가 없어진다. 다만 그것이 필요했다면 `inbox_hold` 가 한 번은 쓰였을 것이다 — 0건이라는 사실이 그 필요가 아직 없다는 증거다. 필요해지면 그때 다시 만든다.

## 근거 개념

- [[idempotency]] — 접수의 큐 조회 skip 이 이 성질이다. 같은 파일이 여러 번 push 돼도 큐 항목은 하나여야 한다. 잔디의 「email 기준 멱등」·Drive 의 `drive_file_id` unique 와 같은 자리다

## Scope

- In: `inbox/` 역할 · route 배타 옵션 · `KDEV-SPEC-008`
- Out: 공부 노트 파이프라인 구현(`source_kind` 정의·collect·게이트) — 후속 work

## Open Questions

없음.

**접수 멱등의 자연키는 파일명(slug)이다.** `inbox/` 는 접수 때 비워지므로(D1) 같은 경로가 다시 나타난다는 것은 **같은 노트를 다시 넣었다**는 뜻이다 — 내용 해시를 쓸 이유가 없다. 오탈자를 고쳐 다시 넣어도 같은 항목으로 잡힌다.

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| KDEV-SPEC-008 | update | 배타 옵션에서 `inbox 보류` 제거. `discard` 만 남는다 |
