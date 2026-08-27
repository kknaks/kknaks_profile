---
type: work
id: MRT-WORK-009
title: "I2: WebSocket 클라이언트"
status: archived
original_status: done
archived_version: v1.0.1
archived_at: 2026-06-08
product: mac-remote
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/work
  - status/archived
links:
  baselines: []
  decisions: []
  specs:
    - "[[v1_0_1-spec-005-websocket-protocol|MRT-SPEC-005]]"
  works:
    - "[[v1_0_1-work-008-ios-setup|MRT-WORK-008]]"
  releases:
    - "[[v1_0_1-release-001-v1-0-0|MRT-REL-001]]"
  related: []
---

# I2: WebSocket 클라이언트

URLSessionWebSocketTask로 Mac 헬퍼에 연결하고, Spec-05 프로토콜대로 메시지를 송수신한다. 자동 재연결과 하트비트를 구현한다.

> 원본: `mac-remote/doc/work/Work-09-ws-client.md`. 구현 계약은 [[v1_0_1-spec-005-websocket-protocol|MRT-SPEC-005]].

## Work Summary

| 항목 | 내용 |
|---|---|
| 상태 | done |
| 시작일 | 2026-05-24 |
| 완료일 | 2026-05-24 |
| 의존 | [[v1_0_1-work-008-ios-setup\|MRT-WORK-008]] |
| 관련 스펙 | [[v1_0_1-spec-005-websocket-protocol\|MRT-SPEC-005]] |

## 참조 스펙 체크리스트

| Spec 섹션 | 항목 | 반영 여부 |
|-----------|------|-----------|
| Spec-05 §데이터 모델 | ClientMessage, ServerMessage Codable 모델 | [x] |
| Spec-05 §계약 | 모든 action 전송 / type 수신 처리 | [x] |
| Spec-05 §상태 전이 | 미연결→연결 중→연결됨→재연결 중 | [x] |
| Spec-05 §에러 처리 | CONNECTION_LOST, HEARTBEAT_TIMEOUT 재연결 | [x] |

## 태스크

| # | 태스크 | 상태 | 커밋 | 비고 |
|---|--------|------|------|------|
| 1 | WebSocketManager 클래스 (ObservableObject) | [x] | 1a7892a | ConnectionState enum + 공유 상수 |
| 2 | 연결/해제 메서드 | [x] | 675028a | URLSessionWebSocketTask |
| 3 | 메시지 수신 루프 + type별 디코딩 | [x] | 5b8f7a6 | 재귀 receive + ServerMessageType 분기 |
| 4 | 메시지 송신 메서드 (action별) | [x] | 452c9dc | listWindows/focus/key/getPermissions |
| 5 | 자동 재연결 (최대 10회, 2초 간격) | [x] | 41b1676 | heartbeat ping/pong 포함 |
| 6 | 연결 상태 Published 프로퍼티 | [x] | aaf6aef | isConnected, connectionStatusText 헬퍼 |

## 기술 메모

- URLSessionWebSocketTask.receive()는 재귀 호출로 연속 수신
- @Published var connectionState로 UI 바인딩
- 외부 라이브러리 불필요

## 검증 방법 / Acceptance

| # | 검증 항목 | 방법 | 결과 |
|---|----------|------|------|
| 1 | 연결 | Mac 헬퍼 실행 + iOS 앱 실행 → 연결 성공 | 수동 검증 (Xcode 필요) |
| 2 | 메시지 수신 | windowList push 수신 확인 (디버그 로그) | 수동 검증 (Xcode 필요) |
| 3 | 재연결 | Mac 헬퍼 종료 → 재시작 → 자동 재연결 | 수동 검증 (Xcode 필요) |

### 로그 추적 포인트

| # | 위치 (파일/함수) | 로그 레벨 | 로그 내용 |
|---|-----------------|-----------|-----------|
| 1 | WebSocketManager.connect() | INFO | "Connecting to ws://{host}:{port}" |
| 2 | WebSocketManager.connect() | INFO | "Connected successfully" |
| 3 | WebSocketManager.receive() | ERROR | "Connection lost: {error}" |
| 4 | WebSocketManager.reconnect() | WARN | "Reconnecting attempt {n}/{max}" |
| 5 | WebSocketManager.receive() | ERROR | "JSON decode failed: {error}" |
| 6 | WebSocketManager.send() | INFO | "Sending action={action}" |

## 완료 기록

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-05-24 | 최초 작성 |
