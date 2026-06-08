---
type: decision
id: MRT-DEC-005
title: "Swifter를 Mac WebSocket 서버 라이브러리로 선택"
status: archived
original_status: accepted
archived_version: v1.0.1
archived_at: 2026-06-08
product: mac-remote
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/decision
  - status/archived
links:
  baselines:
    - "[[v1_0_1-baseline-001-iphone-mac-remote-idea|MRT-BL-001]]"
  decisions:
    - "[[v1_0_1-decision-001-websocket-protocol|MRT-DEC-001]]"
  specs:
    - "[[v1_0_1-spec-005-websocket-protocol|MRT-SPEC-005]]"
  works: []
  releases: []
  related: []
---

# Swifter를 Mac WebSocket 서버 라이브러리로 선택 (ADR-005)

Mac 헬퍼의 WebSocket 서버로 Swifter(httpswift/swifter)를 사용한다.

> 원본: `mac-remote/doc/Decision.md` ADR-005.

## Context

- 관련 baseline: [[v1_0_1-baseline-001-iphone-mac-remote-idea|MRT-BL-001]]
- [[v1_0_1-decision-001-websocket-protocol|MRT-DEC-001]]에 따라 Mac 헬퍼에 WebSocket 서버가 필요하다.
- 핵심 제약: 외부 의존성 최소화.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| Swifter | 순수 Swift 경량 HTTP/WS 서버 | 경량, 외부 의존성 최소화 원칙 부합 | 기능 범위 좁음 | 채택 |
| Vapor | 풀스택 서버 프레임워크 | 풍부한 기능 | 이 용도에 과함 | 기각 |
| Perfect | 서버 프레임워크 | — | 이 용도에 과함 | 기각 |

## Decision

- 채택: Swifter(httpswift/swifter).
- 기각: Vapor, Perfect.
- 보류: 없음.

## Rationale

- 판단 기준: 경량성, 외부 의존성 최소화.
- 대안 대비 이유: 순수 Swift, 경량, 외부 의존성 최소화 원칙에 부합. Vapor/Perfect는 이 용도에 과하다.
- 리스크: Swift Package Manager로 의존성 추가. Mac 헬퍼의 유일한 외부 의존성.

## Scope

- In: Mac WebSocket 서버 구현(Spec-05).
- Out: iOS 클라이언트(URLSessionWebSocketTask, 외부 의존성 없음).
- 영향을 받는 spec 후보: [[v1_0_1-spec-005-websocket-protocol|MRT-SPEC-005]].

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| MRT-SPEC-005 | update | WebSocket 서버 구현 라이브러리로 Swifter 명시 |
