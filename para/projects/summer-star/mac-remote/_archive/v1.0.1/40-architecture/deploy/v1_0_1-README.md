# Deploy Architecture

규칙: `para/projects/project.md`

> mac-remote는 두 artifact를 따로 배포한다 — Mac 헬퍼는 Developer ID 사인 DMG, iOS 앱은 TestFlight.
> 원본: `mac-remote/doc/Architecture.md` §8, `mac-remote/doc/runbook/`.

## Environments

| Environment | Target | Purpose | Notes |
|---|---|---|---|
| local (Mac) | `swift run MacHelper` | 개발 | 사인 불필요 |
| local (iOS) | Xcode → Run (실기기) | 개발 | Development 인증서/프로파일 |
| dist (Mac) | Developer ID 사인 + 공증 DMG | 외부 배포 | 더블클릭 실행 (RB-001 §공증) |
| dist (iOS) | TestFlight 내부 테스트 | 내부 배포 | 심사 없음, 즉시 배포 |

## 실행 / 권한 요구사항

| 컴포넌트 | 플랫폼 | 최소 버전 | 권한 / 설정 |
|----------|--------|-----------|-------------|
| Mac 헬퍼 | macOS | 14.0+ | Accessibility (필수), Screen Recording (창 제목에 필요) |
| iOS 앱 | iOS | 17.0+ | 카메라 (QR 스캔, 선택), 로컬 네트워크 |
| 네트워크 | Wi-Fi LAN | — | 같은 네트워크 필수, 포트 8765 |

## Deploy Map

| Area | Index |
|---|---|
| Backend (Mac 헬퍼 DMG) | `back/README.md` |
| Frontend (iOS TestFlight) | `front/README.md` |

## Release Flow

실행 절차는 런북에 있다.

1. Mac: [MRT-RB-001 DMG 배포](../../70-runbook/v1_0_1-runbook-001-mac-dmg-release.md).
2. iOS: [MRT-RB-002 TestFlight / App Store 심사](../../70-runbook/v1_0_1-runbook-002-ios-testflight-appstore.md).
3. 출시 후 release note 작성: `60-release/release-*.md`.
