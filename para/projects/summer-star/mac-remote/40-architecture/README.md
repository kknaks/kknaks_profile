# Architecture Index

규칙: `para/projects/project.md`

> mac-remote는 **Mac 헬퍼(실행기)** + **iOS 앱(리모컨)** 두 컴포넌트가 LAN WebSocket으로 통신하는 구조다. 여러 spec/work가 공유하는 장기 구조를 여기에 둔다.
> 원본: `mac-remote/doc/Architecture.md`.

## 문서 맵

| Area | Purpose | Index |
|---|---|---|
| system | 컴포넌트, 통신 인터페이스, 데이터 흐름 | `system/README.md` |
| database | 런타임 엔티티와 영속 저장(UserDefaults) | `database/README.md` |
| deploy | Mac DMG / iOS TestFlight 배포 프로세스 | `deploy/README.md` |

## 기술 스택

| 계층 | 기술 | 버전 | 선택 근거 |
|------|------|------|-----------|
| Mac 헬퍼 | Swift + AppKit | Swift 5.9+ / macOS 14+ | 네이티브 API 필수 (CGEvent, AXUIElement, CGWindowList) |
| iOS 앱 | Swift + SwiftUI | Swift 5.9+ / iOS 17+ | 선언형 UI, URLSessionWebSocketTask 내장 |
| 통신 | WebSocket (JSON) | RFC 6455 | 실시간 양방향, 서버→클라이언트 push |
| Mac WS 서버 | Swifter | latest | 경량, 순수 Swift ([[decision-005-swifter-ws-library\|MRT-DEC-005]]) |

### 외부 의존성

| 이름 | 용도 | 라이선스 | 비고 |
|------|------|----------|------|
| Swifter (httpswift/swifter) | Mac WebSocket 서버 | BSD-3 | Mac 헬퍼의 유일한 외부 의존성 |

## 원칙

- 코드와 schema 전문을 복사하지 않는다.
- 오래 유지되는 구조, 경계, invariant만 둔다.
- 관련 결정: [[decision-001-websocket-protocol\|MRT-DEC-001]], [[decision-005-swifter-ws-library\|MRT-DEC-005]].
