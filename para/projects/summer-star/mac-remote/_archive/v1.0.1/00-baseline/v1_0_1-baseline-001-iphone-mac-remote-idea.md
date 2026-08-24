---
type: baseline
id: MRT-BL-001
title: "iPhone을 Mac 리모컨으로 쓰기"
status: archived
original_status: accepted
archived_version: v1.0.1
archived_at: 2026-06-08
product: mac-remote
source:
  type: idea
  ref: "mac-remote/doc/Decision.md (Project Overview)"
links:
  baselines: []
  decisions:
    - "[[v1_0_1-decision-001-websocket-protocol|MRT-DEC-001]]"
    - "[[v1_0_1-decision-002-cgwindowlist-window-source|MRT-DEC-002]]"
    - "[[v1_0_1-decision-003-app-icon-only-no-capture|MRT-DEC-003]]"
    - "[[v1_0_1-decision-004-mac-helper-first|MRT-DEC-004]]"
    - "[[v1_0_1-decision-005-swifter-ws-library|MRT-DEC-005]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-05-24
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/baseline
  - status/archived
---

# iPhone을 Mac 리모컨으로 쓰기

iPhone을 물리 리모컨처럼 써서 Mac의 창 전환과 자주 쓰는 단축키 매크로를 한 손으로 실행하고 싶다.

> 이 제품을 시작하게 된 날것의 동기와 핵심 제약을 보존한다. 실제 결정은 `10-decision/`에 있다.

## Raw

> Mac에서 여러 창을 전환할 때 키보드/트랙패드 조작이 번거롭다.
> iPhone을 물리 리모컨처럼 써서 한 탭에 원하는 창으로 이동하고,
> 자주 쓰는 단축키를 버튼 하나로 실행하고 싶다.

## Context

- 프로젝트명: 매크로 키보드 (mac-remote)
- 한줄 요약: iPhone을 리모컨으로 써서 Mac의 창 전환 + 단축키 매크로 전송
- 시작일: 2026-05-24
- 두 컴포넌트로 구성: iOS 앱(리모컨) + Mac 헬퍼(실행기). 실제 창 제어/키 입력은 100% Mac 헬퍼가 담당한다.

## Why It Matters

여러 창을 오가는 작업에서 키보드 단축키를 외우거나 트랙패드 제스처를 반복하는 대신, 손에 든 iPhone에서 창을 직접 보고 누르는 편이 빠르다. 자주 쓰는 단축키도 버튼 하나로 묶을 수 있다.

## Core Constraints

이번 제품이 지켜야 하는 날것의 제약. decision 단계에서 각각이 어떻게 반영됐는지는 `10-decision/` 참조.

- LAN 전용 — 인터넷 경유 원격 접속 불가, 같은 Wi-Fi 필수
- 화면 캡처/썸네일 금지 — 앱 아이콘만 표시, ScreenCaptureKit 미사용
- iOS 앱 단독 동작 불가 — 실제 창 제어/키 입력은 100% Mac 헬퍼가 담당
- DB 미사용 — 영속 저장은 UserDefaults 수준으로 충분
- 멀티 Mac 동시 연결 불가 — 1:1 연결만 지원

## Possible Direction

- 통신: 실시간 양방향 + 서버→클라이언트 push가 필요 → WebSocket 후보 ([[v1_0_1-decision-001-websocket-protocol|MRT-DEC-001]])
- 창 목록: macOS 네이티브 API로 수집 ([[v1_0_1-decision-002-cgwindowlist-window-source|MRT-DEC-002]])
- 창 식별: 캡처 대신 앱 아이콘 ([[v1_0_1-decision-003-app-icon-only-no-capture|MRT-DEC-003]])
- 개발 순서: Mac 헬퍼 CLI 먼저 검증 후 iOS ([[v1_0_1-decision-004-mac-helper-first|MRT-DEC-004]])
