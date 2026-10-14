---
type: decision
id: DEC-001
title: "기능별 독립 front/back 한 레포 · FastAPI + Next.js"
status: proposed
product: cc-prototype
created_at: 2026-10-10
updated_at: 2026-10-12
tags:
  - product/cc-prototype
  - doc/decision
  - status/proposed
links:
  baselines:
    - "[[baseline-001-feature-lab|BASE-001]]"
    - "[[baseline-002-sts-idea|BASE-002]]"
    - "[[baseline-003-cc-idea|BASE-003]]"
  decisions: []
  specs: []
  works: []
  releases: []
  related: []
up: []
---

# 기능별 독립 front/back 한 레포 · FastAPI + Next.js

> 기능 계약은 `20-spec/`, 작업 순서는 `30-work/` 가 갖는다. 이 문서는 무엇을 정했고
> 무엇이 열려 있는지만 갖는다.

## Context

고객에게 보여줄 실험이 여러 개 생긴다(BASE-001 입력 1). 실험은 생겼다 사라지고, 고객마다
다른 것을 보여줄 수 있어야 한다.

## Options

| Option | Description | 판단 |
|---|---|---|
| A | **한 레포, 기능 폴더마다 front/back 한 쌍, 기능끼리 공유 없음** | **채택** |
| B | 한 레포, 공통 인프라(DB · 인증 · 프록시) 위에 기능을 얹음 | 기각 — 사용자 답 「완전 독립」. 실험 하나를 지우거나 따로 띄울 때 공통부가 걸린다 |
| C | 기능마다 레포 | 기각 — 사용자가 레포 하나(`kknaksss/cc-prototype`)를 지정 |

## Decision

| ID | 결정 | 근거 |
|---|---|---|
| D-01 | 코드는 `kknaksss/cc-prototype` 한 레포. 로컬 `/Users/kknaks/git/toy_pr2/cc-prototype`. 문서는 `para/projects/summer-star/cc-prototype/`(이 레포) | 사용자 원문 「빈레포에서 시작할거야」 · sc-rank 와 같은 분리형 |
| D-02 | 레포 루트에 **기능 폴더**를 두고 그 아래 `front/` · `back/` 한 쌍. 첫 기능은 ~~`sts` · `cc`~~ → **`cc`** (2026-10-12 뒤집음 — D-06) | 사용자 원문의 트리 |
| D-03 | **기능은 완전 독립.** 기능 폴더 하나가 자기 compose · DB · env · 의존성 파일을 전부 갖는다. 기능 폴더 밖의 코드를 import 하지 않는다. 기능 폴더를 통째로 지워도 다른 기능이 그대로 돈다 | 사용자 답 「완전 독립」 |
| D-04 | 기본 스택은 **back = FastAPI(Python, uv) · front = Next.js**. 기능이 다른 스택을 원하면 그 기능의 DEC 에서 바꾼다 | 사용자 답 「FastAPI + Next.js」 |
| D-05 | 기능의 내용은 **기능별 BASE · DEC** 로 받는다. 이 DEC 는 레포 구조만 정한다 | 사용자 답 「지금은 이름만」 |
| D-06 | **sts 는 기능 폴더가 아니다 — `cc` 안의 통역 기능이다.** cc 직원용 화면에서 통역을 연다. Soniox 연결(STT+번역 · TTS)은 `cc/back` 이 갖는다. D-03(기능끼리 공유 없음)은 그대로 — sts 가 별도 기능이 아니므로 공유가 생기지 않는다 (2026-10-12) | 사용자 원문 「cc 에 다 통합 될거 같은데」(BASE-003) · 「직원용 뷰에 통역 기능 넣으면 될거 같아서 Sts 로」 · 「dec 바꾸자」(2026-10-12) |

## Scope

- In: 레포 구조, 기능 독립 규칙, 기본 스택.
- Out: 각 기능의 내용, 배포 대상(OQ-001).

## Open Questions

| ID | 질문 | 언제 닫나 |
|---|---|---|
| OQ-001 | 고객 데모를 어디에 배포하나 — 홈서버 일체(docker + NPM) / front Vercel + back 홈서버 / 기타. 도메인 규칙(기능별 서브도메인 등) 포함 | 첫 기능을 고객에게 보여주기 전 |
| OQ-002 | 고객이 데모에 들어올 때 접근 제한(비밀번호 · 링크 토큰 등)이 필요한가 | OQ-001 과 같이 |
| OQ-003 | 로컬 개발 포트 배정 규칙(기능끼리 안 겹치게) | 레포 뼈대 SPEC 에서 |
| OQ-004 | 통역을 넣을 cc 화면 — 사용자는 「직원용 뷰」, 받은 시안 파일명은 「Ceramique 의사 모바일」. 둘이 같은 화면인가 | cc 통역 SPEC 전 |
| OQ-005 | 코드 레포에 이미 만든 `sts/` 뼈대(front/back `.gitkeep`)를 지우나 | 다음 코드 발주 때 |
