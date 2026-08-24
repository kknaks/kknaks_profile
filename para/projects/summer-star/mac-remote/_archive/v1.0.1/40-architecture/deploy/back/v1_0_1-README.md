# Backend Deploy — Mac 헬퍼

규칙: `para/projects/project.md`

> Mac 헬퍼(MacHelper)의 배포 *구조/환경*. 실행 *절차*는 [70-runbook/runbook-001](../../../70-runbook/v1_0_1-runbook-001-mac-dmg-release.md).

## Runtime / Target

| Item | Value |
|---|---|
| Language | Swift 5.9+ / macOS 14+ |
| Build | Swift Package Manager (`swift build -c release`) |
| Artifact | `build/MacHelper-<버전>.dmg` (Universal: arm64 + x86_64) |
| 서명 주체 | Developer ID Application (외부 직접 배포용) |
| 공증 | 적용 (notarytool + stapler) — 더블클릭 실행 |
| 배포 채널 | Developer ID 사인 DMG 직접 배포 |

## 절차

빌드·서명·DMG 생성·검증·트러블슈팅은 런북에 둔다.

- [MRT-RB-001 — Mac 헬퍼 DMG 배포](../../../70-runbook/v1_0_1-runbook-001-mac-dmg-release.md)

## 관련 파일

- `scripts/build_dmg.sh`, `scripts/install_machelper.sh`
- `MacHelper/Sources/MacHelperApp/Info.plist`, `icon/AppIcon.icns`
