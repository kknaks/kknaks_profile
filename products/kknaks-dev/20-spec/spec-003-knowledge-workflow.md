---
type: spec
id: KDEV-SPEC-003
title: "지식 워크플로 — 분류·연결·망각 생명주기"
status: draft
product: kknaks-dev
version: 0.0.1
created_at: 2026-06-29
updated_at: 2026-06-29
tags:
  - product/kknaks-dev
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-005-classification-workflow|KDEV-DEC-005]]"
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works: []
  releases: []
  related: []
---

# 지식 워크플로 — 분류·연결·망각 생명주기

노트가 생성→분류→연결→망각으로 흐르는 규약. SSOT는 종착지이며, 분류는 *승격/이동*이 아니라 성격에 따른 배치다.

## 1. Context

### Meta

- Decision reference: [[decision-005-classification-workflow|KDEV-DEC-005]]
- Baseline reference: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Domain note: permanent·product·post는 평행한 독립 SSOT. idea는 휘발.
- Open questions: §7

### Business Requirement

생각·자료가 휘발되지 않고 적절한 종착지에 쌓이며, 종착지 간 중복 없이 계보로 연결되어야 한다.

### Scope

In scope: 노트 생명주기(수집·분류·연결·망각), SSOT 귀속 규칙.
Out of scope: 검증 규칙([[spec-004-graph-validation|KDEV-SPEC-004]]), 디렉토리 정의([[spec-001-directory-structure|KDEV-SPEC-001]]).

## 2. UX Contract

해당 없음 (작성자/에이전트 규약).

## 3. User Scenario

### S-1. 수집 — 아이디어 던지기

1. 떠오른 생각을 `inbox/`에 빠르게 적는다 (type: idea, 정제 안 함).

### S-2. 분류 — 종착지로 배치

1. inbox의 idea를 검토해 성격을 판단한다.
2. 제품 스펙감 → `products/{x}/00-baseline`로 옮겨 적는다.
3. 연구/고찰 → `permanent/`로.
4. 글감 → `persona/posts/`로.
5. **원본 idea는 폐기** (휘발). 내용은 종착지에 존재.

### S-3. 연결 — 기반/연상

1. reference 자료를 읽고 permanent/product/post 작성 시 본문에 `[[reference-stem]]` 인용.
2. 계보(기반)면 `up:`에도 stem을 넣는다.
3. permanent끼리 관련되면 본문 `[[]]`로 연상 연결.
4. permanent와 product는 별개 SSOT로 살아있고, `up:`은 인용일 뿐 중복 아님.

### S-4. 망각 — 아카이브

1. 안 쓰게 된 permanent는 `permanent/archive/`로 옮긴다 (파일명 stem 유지 → 링크 보존).
2. 다시 필요하면 상위로 폴더 한 칸 이동(부활).

## 4. Interface Contract

### State / Lifecycle

```mermaid
stateDiagram-v2
    [*] --> idea : inbox 수집
    idea --> product : 제품 스펙감 (분류)
    idea --> permanent : 연구/고찰 (분류)
    idea --> post : 글감 (분류)
    idea --> [*] : 분류 후 원본 폐기
    permanent --> archived : 안 씀
    archived --> permanent : 부활
    reference --> permanent : 인용(up)
    reference --> product : 인용(up)
```

## 5. Implementation Rules

- 분류 후 inbox 원본은 폐기 (inbox는 항상 미분류만 보유).
- idea는 `up:` 대상 금지 (휘발). 상류는 reference·permanent만 — 검증 L4.
- 종착지 간 동일 stem 중복 금지 = SSOT 단일 — 검증 L2.
- 아카이브 내림은 폴더 이동, 링크는 stem 기반이라 보존.

## 6. Verification

### Acceptance Criteria

- [ ] inbox에는 미분류 idea만 남는다 (분류된 것 폐기).
- [ ] permanent와 product가 같은 내용을 중복 보유하지 않는다.
- [ ] archive로 옮겨도 inbound 링크가 깨지지 않는다.
- [ ] idea를 `up:`으로 가리키는 노트가 없다.

## 7. Open Questions

- 아카이브로 내리는 트리거 기준(수동 판단 vs 미참조 기간). 운영하며 정함.
