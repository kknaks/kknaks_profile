# Frontend Deploy — iOS

규칙: `para/projects/project.md`

> iOS 앱(MacRemote)의 배포 *구조/환경*. 실행 *절차*(TestFlight·App Store 심사)는 [70-runbook/runbook-002](../../../70-runbook/v1_0_1-runbook-002-ios-testflight-appstore.md).

## Runtime / Target

| Item | Value |
|---|---|
| Framework | Swift + SwiftUI (iOS 17+) |
| Build | Xcode (Archive → Distribute App) |
| 서명 | Automatic (Apple Distribution) |
| Bundle ID | `com.macremote.MacRemote` |
| 배포 채널 | TestFlight 내부 테스트(심사 없음) → App Store 외부 출시(Apple 심사) |

## 배포 환경

| Environment | Target | 심사 | Notes |
|---|---|---|---|
| local | Xcode → Run (실기기) | — | Development 인증서/프로파일 |
| TestFlight | 내부 테스트 | 없음, 즉시 | 최대 100명 |
| App Store | 외부 출시 | Apple 심사 24~48h | 메타데이터·스크린샷·App Privacy 필요 |

## 절차

업로드 전 점검·TestFlight·App Store 심사 제출(반려 리스크 포함)은 런북에 둔다.

- [MRT-RB-002 — iOS TestFlight / App Store 심사](../../../70-runbook/v1_0_1-runbook-002-ios-testflight-appstore.md)

## 관련 파일

- `iOSApp/MacRemote.xcodeproj`
- `iOSApp/iOSApp/Assets.xcassets/AppIcon.appiconset/` (1024 알파 금지)
