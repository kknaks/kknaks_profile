---
type: decision
id: KDEV-DEC-003
title: "노드 타입(frontmatter type) + 식별자(파일명 stem)"
status: accepted
product: kknaks-dev
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
    - "[[decision-004-edge-model-and-schema|KDEV-DEC-004]]"
  specs:
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
  works: []
  releases: []
  related: []
up:
  - primary-key
  - unique-key
---

# 노드 타입 + 식별자 (ADR-003)

그래프 노드 타입은 frontmatter `type`으로 선언하고, 노드 식별자는 **파일명 stem**으로 한다(옵시디언 기준, 빌더가 따라감). id는 `aliases`에 박는다.

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- 그래프 인프라 `app/back/core/wikilinks.py`는 노드를 `id`로 키잉. 그런데 검증 결과:
  - 실제 본문 링크 = `[[파일명-stem|ID-별칭]]` (옵시디언 alias). 타겟이 id가 아니라 파일명.
  - persona 링크 = 경로형 `[[notes/...]]`. 빌더 regex가 `|`·`/`·대문자 미파싱 → 현재 그래프 거의 안 그려짐.
  - 파일명 stem은 ~99% 전역 유일(충돌 3개: Day01·copy·v1_0_1-README). frontmatter `id`는 prefix로 전역 유일.
- 옵시디언은 순정(community 플러그인 0). `[[X]]`를 파일명/`aliases`로만 resolve.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[primary-key]] — **파일명 stem 이 노드의 식별자**라는 결정. 값을 새로 만들지 않고 이미 있는 것(파일명)을 키로 삼은 선택이라, 자연키를 쓸 때의 이점과 대가가 그대로 따라온다
- [[unique-key]] — 그 stem 이 **전역 유일**이어야 그래프가 성립한다 — L2 가 검사하는 제약이 곧 이 결정의 전제다

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| frontmatter id 식별자 | `[[KDEV-SPEC-001]]` | 전역유일 | 기존 링크 전부 변환, 옵시디언 자동완성 불편 | 기각 |
| **파일명 stem 식별자** | `[[spec-001-window-list]]`, id는 aliases | 옵시디언 네이티브, 기존 유지, 이동 안전 | 충돌 3개·alias regex 필요 | **채택** |
| 파일명=id 일치 | 대량 rename | 단순 | 비용 큼 | 기각 |

## Decision

- 노드 타입(frontmatter `type`): `idea`(inbox) · `reference` · `permanent` · `post`(persona/posts) · `product`(products).
- 식별자 = **파일명 stem**. 전역 유일 `id`(예: `KDEV-SPEC-001`)는 frontmatter `aliases`에 등록 → `[[id]]`로도 resolve.
- 빌더가 옵시디언 동작에 맞춘다(파일명 stem 키 + alias 인덱스).
- products 파일명을 `{ID}-{slug}`로 통일하는 건 선택적 폴리시(그래프 요구사항 아님).

## Rationale

- 옵시디언은 못 바꾸는 제약 → 빌더가 거기 맞춘다.
- 파일명 stem이 이미 99% 유일하고, id는 prefix로 유일 → 둘 다 활용(파일명=링크, id=안정 참조).
- 폴더를 옮겨도 옵시디언이 파일명으로 자동 추적 + 빌더도 stem 키 → 승격·아카이브 이동에도 그래프 보존.
- 리스크: 빌더 regex가 alias/경로형 미파싱(수술 필요), 충돌 3개 수정 시 stem 변경 → inbound 링크 확인 후 rename.

## Scope

- In: type 체계, 파일명 stem 식별자, aliases 규약.
- Out: 빌더 regex 구현(work), 충돌 수정(work).
- 영향을 받는 spec 후보: 스키마 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 스키마 spec | create | 노드 타입 + 식별자 + aliases |
