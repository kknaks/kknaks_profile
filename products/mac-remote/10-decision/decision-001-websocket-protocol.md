---
type: decision
id: MRT-DEC-001
title: "WebSocket을 통신 프로토콜로 선택"
status: accepted
product: mac-remote
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-iphone-mac-remote-idea|MRT-BL-001]]"
  decisions:
    - "[[decision-005-swifter-ws-library|MRT-DEC-005]]"
  specs:
    - "[[spec-005-websocket-protocol|MRT-SPEC-005]]"
  works: []
  releases: []
  related: []
---

# WebSocket을 통신 프로토콜로 선택 (ADR-001)

iOS ↔ Mac 간 실시간 양방향 통신에 WebSocket(JSON payload)을 사용한다. Mac 헬퍼가 서버, iOS 앱이 클라이언트.

> 원본: `mac-remote/doc/Decision.md` ADR-001.

## Context

- 관련 baseline: [[baseline-001-iphone-mac-remote-idea|MRT-BL-001]]
- iOS ↔ Mac 간 실시간 양방향 통신이 필요하다.
- 창 목록 갱신을 서버에서 push 해야 한다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| WebSocket (JSON) | Mac 서버 / iOS 클라이언트 | 지연 낮음, push 자연스러움, 디버깅 쉬움, 프로토콜 단순 | 서버를 헬퍼에 내장해야 함 | 채택 |
| HTTP 폴링 | iOS가 주기적으로 GET | 구현 단순 | 지연 큼, push 불가 | 기각 |
| Bonjour / MultipeerConnectivity | Apple 프레임워크 | 자동 탐색 | 디버깅 어렵고 프로토콜 복잡 | 기각 |

## Decision

- 채택: WebSocket (JSON payload). Mac 헬퍼가 서버, iOS 앱이 클라이언트.
- 기각: HTTP 폴링, Bonjour/MultipeerConnectivity.
- 보류: 없음.

## Rationale

- 판단 기준: 실시간성, push 자연스러움, 디버깅 용이성.
- 대안 대비 이유: HTTP 폴링 대비 지연이 낮고 서버→클라이언트 push가 자연스럽다. Bonjour/Multipeer 대비 WebSocket이 디버깅이 쉽고 프로토콜이 단순하다.
- 리스크: Mac 헬퍼가 WebSocket 서버를 내장해야 한다.

## Scope

- In: WebSocket 기반 메시지 계약(Spec-05).
- Out: 인터넷 경유 원격(제약상 LAN 전용).
- 영향을 받는 spec 후보: [[spec-005-websocket-protocol|MRT-SPEC-005]].

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 | | |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| MRT-SPEC-005 | create | WebSocket 통신 프로토콜. iOS는 URLSessionWebSocketTask로 추가 라이브러리 없이 구현 가능 |
