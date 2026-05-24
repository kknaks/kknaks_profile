# mac-remote

iPhone을 리모컨으로 써서 MacBook의 창을 전환하고 단축키 매크로를 전송하는 앱.

```
┌────────────────────┐       Wi-Fi (LAN)        ┌─────────────────────────┐
│  iOS 앱 (리모컨)    │  ◄── WebSocket/JSON ──►  │  Mac 헬퍼 (실행기)       │
│  SwiftUI           │                           │  Swift, 메뉴바 앱        │
│  - 창 목록 UI      │                           │  - WebSocket 서버        │
│  - 매크로 버튼     │                           │  - 창 목록 수집          │
│  - 설정/페어링     │                           │  - 앱 아이콘 수집        │
└────────────────────┘                           │  - 창 활성화 / 키 입력   │
                                                  └─────────────────────────┘
```

## 구성요소

| 컴포넌트 | 플랫폼 | 역할 |
|----------|--------|------|
| **Mac 헬퍼** | macOS 14+ | WebSocket 서버, 창 목록 수집, 창 활성화, 키 입력 전송 |
| **iOS 앱** | iOS 17+ | WebSocket 클라이언트, 창 목록 표시, 매크로 버튼 UI |

## 통신

- Mac 헬퍼가 WebSocket **서버**, iOS 앱이 **클라이언트**
- 같은 Wi-Fi 필수 (LAN 전용)
- 페어링: QR 코드 스캔 또는 수동 IP 입력

## 기술 스택

- Swift (양쪽 모두)
- SwiftUI (iOS)
- MenuBarExtra (macOS)
- CGWindowListCopyWindowInfo (창 목록)
- CGEvent (키 입력)
- AXUIElement (창 활성화)
