---
type: spec
id: KDEV-SPEC-001
title: "지식그래프 디렉토리 구조"
status: draft
product: kknaks-dev
version: 0.0.3
created_at: 2026-06-29
updated_at: 2026-06-30
tags:
  - product/kknaks-dev
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions:
    - "[[decision-001-products-single-root|KDEV-DEC-001]]"
    - "[[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]"
  specs:
    - "[[spec-002-graph-schema|KDEV-SPEC-002]]"
  works: []
  releases: []
  related: []
---

# 지식그래프 디렉토리 구조

레포의 모든 노트가 어느 디렉토리에 사는지, 각 디렉토리가 그래프에서 어떤 노드 타입을 담는지에 대한 계약. 작성자·에이전트·빌더가 이 문서만으로 노트 위치를 판단할 수 있어야 한다.

## 1. Context

### Meta

- Decision reference: [[decision-001-products-single-root|KDEV-DEC-001]], [[decision-002-knowledge-pipeline-layers|KDEV-DEC-002]]
- Baseline reference: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Domain note: 노드 타입 enum = `idea`/`reference`/`permanent`/`post`/`product`. 내부 스키마 상세는 [[spec-002-graph-schema|KDEV-SPEC-002]].
- Open questions: §7

### Business Requirement

흩어진 생각·자료·제품 문서가 일관된 위치 규칙을 가져야, 작성 시 "어디 둘지" 고민이 없고 빌더가 디렉토리로 노드 타입을 결정할 수 있다.

### Scope

In scope:
- 루트 레벨 지식 파이프라인 층(inbox/reference/permanent)
- products 제품 레이아웃(showcase + 파이프라인)
- persona 재편(posts 신설, projects/notes/contents 이동 결과)

Out of scope:
- 실제 파일 이동·코드 정합(work)
- 노드/엣지 스키마([[spec-002-graph-schema|KDEV-SPEC-002]])

## 2. UX Contract

해당 없음 (디렉토리 구조 계약, 화면 없음).

## 3. User Scenario

### S-1. 작성자 — 새 노트를 둘 위치 결정

1. 정제 안 된 생각이면 → `inbox/` (type: idea, 휘발).
2. 외부 자료를 읽고 정리한 것이면 → `reference/` (type: reference).
3. 정제된 영구 생각(제품화 전 연구·고찰)이면 → `permanent/` (type: permanent).
4. 제품 스펙감이면 → `products/{제품}/00-baseline` (type: product 계열, 00→20 파이프라인).
5. 발행할 글이면 → `persona/posts/` (type: post).
6. 안 쓰게 된 영구노트는 → `permanent/archive/` (cold).

## 4. Interface Contract

### API Contract

해당 없음.

### Data Contract — 디렉토리 레이아웃

```text
inbox/                 # type: idea (휘발)
reference/             # type: reference (자료 정리)
permanent/             # type: permanent (영구노트)
└── archive/           # 장기기억 (cold)
products/              # type: product 계열
└── {제품}/
    ├── README.md
    ├── showcase.md    # 블로그 카드 (frontmatter: org, category, status …)
    ├── 00-baseline/ … 60-release/   # 개인 제품만 채움
    └── log.md
persona/
├── posts/             # type: post (발행물)
├── career/ · profile.md · daily/ · assets/   # 정체성(그래프 주변 노드)
├── algorithms/        # 그래프 무관, 잔류
└── contents/          # type: content — YouTube 요약 파이프라인, 그래프 무관, 잔류 (DEC-008)
```

- `products/{제품}/showcase.md` frontmatter: `org: company | studio`, `category`, `status`, `visible`, `thumbnail`.
- 회사 프로젝트 = `showcase.md`만, 개인 제품 = showcase + 파이프라인.

### State / Lifecycle

노트 위치 전이는 [[spec-003-knowledge-workflow|KDEV-SPEC-003]] 참조.

## 5. Implementation Rules

- 노드 타입은 디렉토리가 1차 결정, frontmatter `type`이 명시(불일치 시 검증 ERROR — [[spec-004-graph-validation|KDEV-SPEC-004]]).
- 파일명 stem 전역 유일(식별자 — [[spec-002-graph-schema|KDEV-SPEC-002]]).
- 실제 디렉토리 이동·라우트/로더 코드 정합은 work에 둔다.
- showcase-only 제품(회사/일부 개인, S1)은 stage 디렉토리(00~30) 없이 `showcase.md`만 둔다. product-doc-pipeline은 **showcase.md 有 + stage 디렉토리 無**를 showcase-only로 추론해 stage README 강제를 면제한다(D-001/D-003 파생).

## 6. Verification

### Acceptance Criteria

- [ ] inbox/reference/permanent(+archive) 루트 층 존재.
- [ ] products/{제품}/에 showcase.md 규약 적용, org 필드로 회사/개인 구분.
- [ ] persona/posts 신설, projects→products·notes→reference 재편 완료 (contents 잔류 — DEC-008).
- [ ] 각 디렉토리의 노드 타입이 frontmatter `type`과 일치.

## 7. Open Questions

- 없음 (구현 세부는 work).
