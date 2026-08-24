---
type: concept
id: mrtr
title: MRTR (Multi-Round Trip Request)
aliases:
  - MRTR
  - Multi-Round Trip Request
  - 멀티라운드 트립 리퀘스트
  - 다회 왕복 요청
up:
  - C-025-mcp-s-new-spec-from-stateful-sessions-to-stateless
tags:
  - protocol-design
  - request-response
  - mcp
---

# MRTR (Multi-Round Trip Request)

MRTR은 서버가 요청 처리 중 클라이언트로부터 추가 정보가 필요할 때, 서버가 클라이언트를 역으로 호출하는 대신 "정보가 더 필요하다"는 응답으로 요청을 일단 종료하고, 클라이언트가 필요한 정보를 얻어 다시 요청을 보내게 하는 상호작용 패턴이다.

## 정의

1. 서버가 요청을 처리하다 추가 정보(예: 사용자 입력)가 필요한 지점에 도달한다.
2. 서버는 클라이언트를 향해 별도의 요청을 만들어 보내지 않고, "정보 필요"라는 응답을 돌려주며 현재 요청을 종료한다.
3. 클라이언트가 필요한 정보를 확보한다.
4. 클라이언트가 그 정보를 담아 서버에 다시 요청을 보낸다.

## 사용 예시

MCP의 2026-07-28 신규 스펙에서 도입됐다. 기존 MCP는 서버가 실행 중 추가 정보가 필요하면 클라이언트에게 "사용자에게 이 내용을 물어봐 달라"고 역으로 요청을 보낼 수 있었다(서버가 클라이언트를 호출). 신규 스펙은 이 구조를 MRTR로 바꿔, 서버가 클라이언트를 역호출하지 않고 "정보 필요" 응답으로 요청을 끝내면 클라이언트가 정보를 얻어 다시 요청하도록 했다.

## 왜 중요한가

서버가 클라이언트를 역으로 호출하는 구조는 웹에서 일반적으로 쓰이는 HTTP request-response 방식과 맞지 않는다. MRTR로 바꾸면 서버는 항상 요청에 응답만 하면 되므로, [[stateless-protocol]] 위에서 표준적인 HTTP 요청-응답 모델과 자연스럽게 맞물린다.

## 경계와 오해

- **MRTR ≠ 서버가 클라이언트를 호출하는 콜백 구조** — 기존 MCP의 "서버가 클라이언트에게 되물어봐 달라 요청"하던 방식과 반대다. MRTR에서는 서버가 클라이언트를 향해 새 요청을 만들지 않는다.
- **[[remote-procedure-call]]과의 차이** — RPC는 원격 노드가 서로를 직접 호출하는 모델이다. MRTR은 그 반대로, 서버가 클라이언트를 직접 호출하지 않고 응답-재요청으로 정보를 주고받는 모델이다.

## 함께 보는 개념

- [[stateless-protocol]] — MRTR이 성립하는 배경이 되는 프로토콜 구조
- [[remote-procedure-call]] — 대조되는 역호출 기반 원격 호출 모델
- [[ai-agent]] — MRTR이 도입된 MCP가 AI 에이전트와 툴을 연결하는 프로토콜

## 출처

- [[C-025-mcp-s-new-spec-from-stateful-sessions-to-stateless]] — MCP 신규 스펙이 서버의 클라이언트 역호출 대신 MRTR 구조를 도입했다고 설명
