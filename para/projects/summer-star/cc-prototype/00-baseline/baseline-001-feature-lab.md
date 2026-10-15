---
type: baseline
id: BASE-001
title: "기능별 front/back 실험을 한 레포에, 고객 데모까지"
status: raw
product: cc-prototype
source:
  type: conversation
  ref: "사용자 대화 2026-10-10"
links:
  baselines: []
  decisions:
    - "[[decision-001-feature-lab|DEC-001]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-10-10
updated_at: 2026-10-10
tags:
  - product/cc-prototype
  - doc/baseline
  - status/raw
---

# 기능별 front/back 실험을 한 레포에, 고객 데모까지

> 아직 결정하지 않은 입력이다. 무엇을 정했는지는 DEC-001 이 갖는다.

## Raw

### 입력 1 — 사용자 원문 (2026-10-10)

> summerstar에 프로토 탑입 프로젝트 시작할거야
>
> https://github.com/kknaksss/cc-prototype.git 빈레포에서 시작할거야
>
> 아래 여러가지 기능을 시작할거야
>
> ```
> sts
> |-front
> |-back
> cc
> |-front
> |-back
> ```
>
> 이런식으로 여러 기능별 실험을 할거야
> 고객 한테 보여줘야 해서 배포 까지 생각할거야

### 입력 2 — 코디 질문에 대한 답 (2026-10-10)

| 질문 | 답 |
|---|---|
| sts · cc 는 각각 어떤 실험인가 | 지금은 이름만 — 내용은 기능별 작업에서 받는다 |
| 기능별 front/back 기본 스택 | FastAPI + Next.js |
| 고객 데모 배포 위치 | 아직 미정 |
| 기능끼리 무엇을 공유하나 | 완전 독립 — 기능마다 자체 compose · DB · env |

### 입력 3 — 레포 관측 (2026-10-10)

`git ls-remote https://github.com/kknaksss/cc-prototype.git` 결과 ref 없음 — 커밋 0 인 빈 레포.
