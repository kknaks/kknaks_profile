# inbox

**공부 노트의 입구**다([[decision-021-inbox-is-an-entry|KDEV-DEC-021]] D1). 목적지가 아니다.

## 어떻게 쓰나

1. 공부하며 쓴 노트를 `inbox/{slug}.md` 로 넣고 push 한다 (또는 로컬 스킬로 만든다)
2. 서버가 뜰 때(FastAPI lifespan) `inbox/` 를 스캔해 **DB 큐로 옮기고 파일을 지운다**
3. route 게이트에서 무엇을 만들지 고른다 — `resources/source/` · `resources/concept/` · `persona/posts/`
4. 승인하면 Apply Executor 가 발행한다

## 서버에서는 항상 비어 있다

접수할 때 본문을 DB 로 옮기고 파일을 지우므로 **파일이 있으면 곧 미처리**다. 「미처리」를 따로 판정하지 않는다.

접수 전에 **DB 큐를 조회해 이미 있으면 skip** 한다 — 승인이 늦어 큐에 머무는 동안 같은 파일이 다시 push 돼도 두 번 접수되지 않는다([[idempotency]]).

## 여기 두는 것

- 아직 정제하지 않은 공부 노트. 타입은 `idea` — **층에 속하지 않고 `up:` 대상이 될 수 없다.**

## 여기 두지 않는 것

- 자료 원본 정리 → `resources/source/`
- 재사용 가능한 개념 → `resources/concept/`
- 공개 글 → `persona/posts/`
- 안 쓰게 된 노트 → `archive/`

> 종전에는 「보류함(목적지)」이었다 — route 게이트에서 「지금은 정제 못 하겠지만 버리긴
> 아깝다」로 승인된 idea 가 들어오는 자리([[decision-011-approval-gate-chain|KDEV-DEC-011]] D1).
> **0건 쓰였고 KDEV-DEC-021 로 폐기됐다.** 배타 옵션은 `폐기` 하나만 남는다.

## 작성 규약

- 작성 규칙: `rules/knowledge-note-pipeline.md`
- 양식: `templates/knowledge/idea.md`
