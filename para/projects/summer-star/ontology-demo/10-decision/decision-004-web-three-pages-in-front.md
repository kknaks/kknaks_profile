---
type: decision
id: DEC-004
title: "웹 = app/front 통합 3페이지 — 단일 페이지 안을 뒤집고 정식 프론트로 간다"
status: accepted
product: ontology-demo
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/ontology-demo
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-demo-agent-app|BASE-001]]"
  decisions:
    - "[[decision-003-llm-via-open-kknaks-mcp|DEC-003]]"
    - "[[decision-005-internal-demo-deploy|DEC-005]]"
  specs:
    - "[[spec-003-api-and-chat-contract|SPEC-003]]"
    - "[[spec-004-three-screens|SPEC-004]]"
  works: []
  releases: []
  related: []
up: []
---

# 웹 = app/front 통합 3페이지 — 단일 페이지 안을 뒤집고 정식 프론트로 간다

기록 09 가 미결로 남긴 「FastAPI 단일 페이지(또는 Streamlit)」를 뒤집는다. 화면은 기존
`app/front/`(Next.js 15 App Router) 안의 통합 3페이지 — **채팅 · 모니터링 · 데이터** — 로 가고,
`app/ontology-agent/` 는 API 서버로 역할을 좁힌다.

> baseline의 날것 입력을 spec으로 내리기 전에 적용 방향을 정하는 문서.
> 기능 계약 상세는 `20-spec/`, 실제 작업 순서는 `30-work/`에 둔다.

## Context

- 관련 baseline: [[baseline-001-demo-agent-app|BASE-001]] — 기록 09 §3 의 7단계 「웹 통합」이
  「FastAPI + 단일 페이지(또는 Streamlit — 착수 시 결정)」로 미결이었다.
- 그런데 이 앱이 내야 하는 화면은 7종이고(계층 탐색 ①②③ · KPI ④ · 그래프 ⑤ · 예보 ⑥ ·
  채팅 ⑦), 그래프 하이라이트처럼 상태를 공유하는 상호작용이 있다.
- 프론트는 이미 있다 — `app/front/`(Next.js 15 App Router)가 포트폴리오 사이트로 돌고 있고
  Vercel 배포 경로도 서 있다.
- 결정이 필요한 이유: 화면 형태가 정해져야 백엔드의 역할(템플릿 렌더 vs API)이 정해지고,
  디자인 세션이 무엇을 그릴지도 정해진다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | FastAPI + static 단일 페이지 (기록 09 원안) | 백 하나로 끝 · 배포 단순 | 화면 7종과 상태 공유 상호작용을 한 페이지에 밀어 넣게 된다 · 렌더링 자산이 재사용 안 됨 | 기각 |
| B | Streamlit (기록 09 원안의 대안) | 데이터 화면을 가장 빨리 만든다 | 채팅·그래프 상호작용과 디자인 자유도가 막힌다 · 기존 프론트와 스택이 갈린다 | 기각 |
| **C** | **기존 `app/front/`(Next.js) 안에 통합 3페이지** | 정식 프론트 자산·배포 경로 재사용 · 화면 7종을 성격별로 3면에 정리 · 디자인 세션이 붙을 자리가 생긴다 | 프론트↔백 계약(API)을 명시해야 한다 · 배포 표면이 둘(Vercel·홈서버)로 갈린다 | **채택** |

## Decision

### D1. 화면은 `app/front/` 통합 3페이지

- 기존 `app/front/`(Next.js 15 App Router) 안에 채팅 · 모니터링 · 데이터 3페이지를 둔다.
  별도 프론트 앱을 새로 만들지 않는다.

### D2. 화면 7종 → 3페이지 매핑

| 페이지 | 담는 화면 | 내용 |
|---|---|---|
| 데이터 | ① ② ③ | 계층 탐색 — 브론즈(마스킹) · 실버(변환 규칙) · 골드(계산식·게이트 이력) |
| 모니터링 | ④ ⑤ ⑥ | KPI 카드 · 원인 분석 그래프 · 예보 |
| 채팅 | ⑦ | AI 채팅 — 답변이 밟은 엣지를 ⑤ 그래프에 하이라이트 |

### D3. 백엔드는 API 서버로 역할 축소

- `app/ontology-agent/`(FastAPI)는 API 서버다. **static 단일 페이지 안은 폐기**한다 —
  화면 렌더는 프론트가 갖는다.

### 기각

- FastAPI static 단일 페이지(A) · Streamlit(B).

## Rationale

- **판단 기준**: 화면 7종이 성격대로 정리되는가, 이미 있는 자산(프론트·배포 경로)을 쓰는가,
  디자인이 붙을 표면이 되는가.
- **C 인 이유**: 기록 09 시점의 단일 페이지 안은 「데모니까 최소로」의 선택이었는데, 실제로
  내야 하는 것은 성격이 다른 세 면(원본을 파고드는 데이터 · 상태를 읽는 모니터링 · 대화)이다.
  한 페이지에 넣으면 셋 다 반쪽이 된다. 프론트가 이미 있으므로 「최소」의 이점도 크지 않다.
- **백을 API 로 좁힌 이유**: 렌더 책임이 둘로 갈리면 어느 쪽이 화면의 SoT 인지 흐려진다.
- **리스크**
  - 프론트↔백 계약이 명시되지 않으면 병렬 구현이 어긋난다 — spec 의 API 계약이 그 자리다.
  - 배포 표면이 둘로 갈린다([[decision-005-internal-demo-deploy|DEC-005]] 가 받는다).

## 근거 개념

- **없음** — `para/areas/concept/front/` 는 현재 `html-form` · `script-loading` 두 건뿐이라,
  이 결정이 기대는 것(App Router 라우팅 · 페이지 분할 · 상태 공유)에 대응하는 개념 노트가
  없다. 억지로 잇지 않는다. 필요한 개념은 코디네이터 질문 목록에 올렸다.

## Scope

- In: 3페이지 구성과 화면 7종 매핑, 백엔드의 API 서버 역할 축소
- Out: 화면별 레이아웃·컴포넌트 상세(디자인 세션 → spec), API 계약 상세(spec),
  채팅↔그래프 하이라이트의 구현 방식(OQ-2)
- 영향을 받는 spec 후보: 화면 spec 3건(채팅·모니터링·데이터), 프론트↔백 API 계약

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 화면 상세(레이아웃 · 컴포넌트 · 카피) | kknaks | **디자인 별도 세션 진행 중** — 귀환 후 spec 에서 확정 |
| ~~OQ-2~~ | 채팅 답변의 `used_edges` 를 그래프에 하이라이트하는 방식(페이지 간 상태 공유 · 이동 여부) | kknaks | **닫힘 (2026-09-02 확정)** — 채팅에는 그래프 패널을 두지 않는다. 답변 안 **칩** + 칩 클릭 시 `/ontology/monitoring?edge=<edge_id>` **점프**로 일원화. 게이트 5-③ 검증 대상 화면 = **모니터링 그래프 단일**. 페이지 간 상태 공유는 **URL 쿼리뿐**(전역 스토어 없음) — [[spec-004-three-screens\|SPEC-004]] U-11 · §4 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-004-three-screens\|SPEC-004]] | create — **작성됨 (2026-09-02, v0.0.1 draft)** | 화면 3페이지 · 라우트 `/ontology/*` · 토큰 레이어 · 파생 카운트 · 디자인 조정 대기 20건 |
| [[spec-003-api-and-chat-contract\|SPEC-003]] | create — **작성됨 (2026-09-02, v0.0.1)** | 프론트↔백 API 계약 · 화면 7종 ↔ 엔드포인트 매핑 |
