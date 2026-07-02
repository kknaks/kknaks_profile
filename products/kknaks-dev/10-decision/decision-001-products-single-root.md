---
type: decision
id: KDEV-DEC-001
title: "제품·프로젝트를 products/ 단일 루트로 통합"
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
  specs:
    - "[[spec-001-directory-structure|KDEV-SPEC-001]]"
  works: []
  releases: []
  related: []
---

# 제품·프로젝트를 products/ 단일 루트로 통합 (ADR-001)

모든 제품·프로젝트(회사 업무 포함)를 `products/` 단일 루트로 모은다. 블로그 렌더용 showcase 카드는 `products/{제품}/showcase.md`로, 회사/개인 구분은 frontmatter `org`로.

## Context

- 관련 baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- 같은 제품이 두 곳에 흩어져 있었다: `persona/projects/{x}.md`(블로그 렌더용 showcase 카드)와 `products/{x}/`(실제 코드 작업용 개발 SSOT).
- showcase 카드: frontmatter `thumbnail`/`visible`/`problem`/`approach`/`impact`, 회고적, 블로그/PDF 렌더, 회사+개인 13개.
- products: 00-baseline~60-release 파이프라인, 능동적 개발, 개인 제품 8개.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 물리 병합 | persona/projects 폐기, 모두 products로 | 단일 트리 | 회사 프로젝트(코드 파이프라인 없음) 갈 곳 없음, 표현/개발 혼합 | 기각 |
| 분리 유지 + 링크 | 둘 다 두고 frontmatter로 연결 | 안전 | 중복 관리 지속 | 기각 |
| **단일 루트 통합** | products로 모으되 showcase는 별도 파일 | 한 곳 관리, SSOT | 마이그레이션 비용 | **채택** |

showcase 위치: (A) `showcase.md` 단일 파일 / (B) `50-showcase/` 스테이지 / (C) README 흡수 → **A**.
회사/개인 구분: (A) flat + frontmatter `org:company|studio` / (B) 폴더 분리 → **A**.

## Decision

- 채택: 모든 제품·프로젝트를 `products/{제품}/`로. showcase = `showcase.md` 단일 파일(A). flat + `org` frontmatter(A).
- 기각: 물리 병합, 분리 유지, showcase 스테이지화, 회사/개인 폴더 분리.
- 보류: products 파일명 `{ID}-{slug}` 일관 rename은 선택적 폴리시.

## Rationale

- 판단 기준: 같은 대상의 다른 층(개발 SSOT vs 렌더 카드)을 한 곳에서 관리.
- 회사 프로젝트(mediness·linky 등)는 코드가 회사 레포라 파이프라인 없이 `showcase.md`만 둔다.
- showcase 한 장이면 충분하니 단일 파일이 깔끔, 블로그는 파일 하나만 읽음.
- 회사/개인을 폴더로 쪼개면 category(web/backend/mobile)와 이중 분류 → frontmatter 한 필드가 나음.
- 리스크: persona/projects를 읽는 코드(블로그 라우트, `jobs/inputs.py` 활동추적 SoT) 이전 필요.

## Scope

- In: products 디렉토리 구조, showcase.md, org 필드.
- Out: 실제 마이그레이션(별도 work).
- 영향을 받는 spec 후보: 디렉토리 구조 spec.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 디렉토리 구조 spec | create | products/{제품}/ 레이아웃 + showcase + org |
