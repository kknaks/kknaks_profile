---
type: release
id: MRT-REL-003
title: "DeskDeck App Store 출시 (1.0.1)"
status: released
product: mac-remote
version: "1.0.1"
released_at: 2026-06-10
summary: "App Store 첫 출시 — 5.2.5(IP) 거절 대응으로 MacRemote→DeskDeck 개명, iOS build 5 재제출·승인. 기능 변경 없음(브랜드/메타데이터 릴리스)."
details:
  - "iOS 앱 개명 MacRemote→DeskDeck — CFBundleDisplayName + CFBundleName 둘 다 지정(생성 plist가 타겟명을 쓰므로), build 4→5"
  - "Mac 헬퍼 개명 MacHelper→DeskDeckHelper — 표시 이름·실행파일·.app/DMG 파일명까지, CFBundleExecutable 일치, 새 DMG 공증(Notarized Developer ID)"
  - "Bundle ID(com.macremote.MacRemote / .machelper)·SPM product명·리소스번들명은 유지 — 5.2.5 대상 아님, 앱 레코드·심사 이력 보존"
  - "랜딩(/macremote) 표기 DeskDeck/DeskDeckHelper 갱신, DMG_URL·APP_STORE_URL 연결"
  - "App Store: https://apps.apple.com/app/id6772868137"
created_at: 2026-06-10
updated_at: 2026-06-10
tags:
  - product/mac-remote
  - doc/release
  - status/released
links:
  baselines: []
  decisions: []
  specs: []
  works: []
  releases:
    - "[[release-002-v1-0-1|MRT-REL-002]]"
  related:
    - "[[runbook-002-ios-testflight-appstore|MRT-RB-002]]"
---

# MRT-REL-003 DeskDeck App Store 출시 (1.0.1)

> App Store 첫 출시. 코드 기능 변경 없는 **브랜드/메타데이터 릴리스** — 1.0.1 기능은 [[release-002-v1-0-1|MRT-REL-002]] 참조.

## 요약

App Store 심사에서 **Guideline 5.2.5 (지식재산권)**으로 거절됐다 — 앱 이름·부제·기기 표시 이름이 Apple 상표(Mac/iPhone)를 부적절하게 사용. ASC 텍스트만으로는 같은 사유로 재거절되므로, **바이너리 표시 이름까지 바꾼 새 빌드**가 필수였다.

`MacRemote` → **`DeskDeck`**으로 개명(Apple 상표 0개), iOS build 5 재제출 후 승인·출시. Mac 헬퍼도 브랜드 일관성을 위해 `MacHelper` → `DeskDeckHelper`로 완전 개명하고 새 DMG를 공증해 교체했다.

## 상세 수정 사항

| Area | Change | Notes |
|---|---|---|
| iOS (Renamed) | 표시 이름 → `DeskDeck` (`CFBundleDisplayName`+`CFBundleName`) | 생성 plist가 `PRODUCT_NAME=$(TARGET_NAME)`=MacRemote를 써서 두 키 모두 명시, build 4→5 |
| Mac 헬퍼 (Renamed) | `DeskDeckHelper` — 표시 이름·실행파일·`.app`/DMG 파일명 | `CFBundleExecutable=DeskDeckHelper` 일치, `build_dmg.sh` APP_NAME 변경, build 2→3 |
| ASC (Updated) | 앱 이름 `DeskDeck`, 부제 "내 컴퓨터가 손안의 리모컨으로" (Mac/iPhone 제거) | — |
| 랜딩 (Updated) | `DeskDeck`/`DeskDeckHelper` 표기, `APP_STORE_URL`·`DMG_URL` 연결 | `public/macremote/index.html` |

## 유지 (변경 안 함)

- **Bundle ID** `com.macremote.MacRemote` / `com.macremote.machelper` — 5.2.5 대상 아님, 바꾸면 앱 레코드·심사 이력·TCC 권한 소멸
- **SPM** product명 `MacHelperApp`, 리소스번들 `MacHelper_MacHelperApp.bundle` — 내부 식별자, `Bundle.module` 안정성

## Breaking Changes

- 없음. 기능·프로토콜·데이터 변경 없음.

## 검증

| Check | Result | Evidence |
|---|---|---|
| iOS build 5 바이너리 표시명 | `DeskDeck` | ASC 빌드 메타데이터 "앱 이름=DeskDeck" |
| App Store 심사 | 승인·출시 | https://apps.apple.com/app/id6772868137 |
| DMG 공증 | `accepted, source=Notarized Developer ID` | `spctl --assess`, Submission `3a01477f-9d26-4fb2-8895-638f2eac97eb` |
| DMG staple | 유효 | `xcrun stapler validate downloads/DeskDeckHelper-1.0.1.dmg` |

## 배포 정보

| Item | Value |
|---|---|
| Version | 1.0.1 (iOS build 5, 헬퍼 build 3) |
| Released At | 2026-06-10 |
| App Store | https://apps.apple.com/app/id6772868137 |
| Artifact | `downloads/DeskDeckHelper-1.0.1.dmg` (공증), iOS App Store build 5 |
| Deployment Target | macOS 14+, iOS 17+ |

## Known Issues

- [[release-002-v1-0-1|REL-002]]의 Known Issues 승계 (핸드셰이크 확인 없는 즉시 `.connected` 전이, client isolation 우회 불가).

## Rollback

- App Store: 이전 승인 빌드가 없어 롤백 불가(첫 출시). 문제 시 새 빌드로 대응.
- DMG: 직전 공증 DMG로 교체.
