---
type: runbook
id: MRT-RB-002
title: "iOS TestFlight / App Store 심사"
status: active
product: mac-remote
area: deploy
created_at: 2026-05-25
updated_at: 2026-06-01
tags:
  - product/mac-remote
  - doc/runbook
  - status/active
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-007-pairing|MRT-SPEC-007]]"
  works: []
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
    - "[[release-002-v1-0-1|MRT-REL-002]]"
  related: []
---

# iOS TestFlight / App Store 심사

iOSApp(MacRemote)을 TestFlight 내부 테스트로 배포하고, App Store 외부 출시(Apple 심사)로 제출한다.

> 배포 환경/타겟 정적 구조는 `40-architecture/deploy/front/README.md`에 있다. 이 문서는 실행 절차만 둔다.
> 원본: `mac-remote/doc/runbook/ios-testflight-release.md` (전체 절차·트러블슈팅은 원본 참조).

## 목적

iOS 앱을 (1) TestFlight 내부 테스트(심사 없음, 즉시)로 배포하고, (2) App Store 외부 출시(Apple 심사 24~48시간)로 제출한다.

## 사전 준비 (최초 1회)

- Apple Developer Program 가입, **Apple Distribution** 인증서.
- Bundle ID 등록(`com.macremote.MacRemote`, Explicit), App Store Connect 앱 레코드 생성.

## 절차

### 1. 업로드 전 코드/리소스 점검 (누락 시 validation 거부)

| # | 항목 | 확인 |
|---|------|------|
| 2-1 | App Icon 1024 **알파 채널 금지** | `sips -g hasAlpha .../AppIcon-1024.png` → `no` |
| 2-2 | `NSLocalNetworkUsageDescription` | `grep -c NSLocalNetworkUsageDescription .../project.pbxproj` → `2` (Debug+Release) |
| 2-3 | ATS | 사설 IP/`.local`은 자동 예외 — 설정 불필요 |
| 2-4 | `ITSAppUsesNonExemptEncryption = NO` | `grep -c ITSAppUsesNonExemptEncryption .../project.pbxproj` → `2` |
| 2-5 | 서명 | `CODE_SIGN_STYLE=Automatic`, `DEVELOPMENT_TEAM` 설정, Signing & Capabilities 에러 없음 |

### 2. TestFlight 내부 테스트

1. Destination을 **Any iOS Device (arm64)**로 선택 (시뮬레이터로는 Archive 불가).
2. **Product → Archive** → Organizer 열림.
3. **Distribute App** → App Store Connect → Upload → 기본값 → Automatically manage signing → Upload.
4. App Store Connect → TestFlight → 처리 대기(5~30분) → 내부 테스터 그룹에 빌드 할당(즉시 배포).
5. iPhone에서 TestFlight 앱 → 설치 → 첫 실행 시 **로컬 네트워크 권한 허용** → Mac 메뉴바 QR 스캔.

후속 빌드: Build number(`CURRENT_PROJECT_VERSION`)는 매 업로드마다 +1. Marketing version은 큰 변경 때만.

### 3. App Store 심사 제출 (외부 출시)

내부 테스트와 달리 추가로 필요한 것:

| # | 항목 | 비고 |
|---|------|------|
| 1 | App Store 메타데이터 | 이름·부제·설명·키워드·카테고리·프로모션 텍스트 |
| 2 | 스크린샷 | **iPhone + iPad 세트 필수** (Universal 타겟 `1,2,7`). 기기 크기별, 자세한 규격은 [assets/README.md](assets/README.md) |
| 3 | App Privacy | 데이터 수집 항목 선언. 이 앱은 LAN-only·수집 없음 → "데이터를 수집하지 않음" |
| 4 | 연령 등급 | 설문 응답 |
| 5 | 개인정보 처리방침 URL | 항목에 따라 요구될 수 있음 |
| 6 | Export compliance | 프로덕션도 `ITSAppUsesNonExemptEncryption=NO` 유지 (ws:// 평문, 표준/자체 암호화 없음) |
| 7 | App Review 정보 + 심사 노트 | ⚠️ 아래 reviewability 주의 |

> #### ⚠️ Reviewability — companion Mac 의존
> 이 앱은 **같은 Wi-Fi의 Mac 헬퍼가 켜져 있어야** 동작한다. 심사자는 Mac 헬퍼가 없으므로 앱을 켜면 "연결 안 됨"만 보고 **"기능이 동작하지 않는다"로 반려**할 수 있다. 완화책:
> - App Review 노트에 companion Mac 필요·연결 절차를 명시한다.
> - 전체 플로우(QR 페어링 → 창 전환 → 매크로) **데모 영상**을 첨부하거나 노트에 링크한다. ([[spec-007-pairing\|MRT-SPEC-007]])

#### App Store Connect 입력 체크리스트

App Store Connect를 위→아래로 따라가며 입력한다. **상태 칸**에 `✅완료 / ⬜미입력 / ⛔막힘·확인불가`로 표시하고, 막히거나 빠진 게 나오면 이 표를 갱신한다. (ASC UI 라벨은 수시로 바뀌니 항목명은 근사값.)

**A. App 정보** (앱 단위, 버전 무관 — 좌측 `App 정보`)

| 필드 | 입력값 / 지침 | 상태 | 메모 |
|---|---|---|---|
| 이름 | **DeskDeck** | ⬜ | 5.2.5 거절로 개명 (구 MacRemote). ASC 텍스트 수정 + 기기 표시 이름은 §4 새 빌드 필요 |
| 부제 | "내 컴퓨터가 손안의 리모컨으로" | ⬜ | 맥·아이폰 제거 (구 "아이폰이 맥 리모컨이 된다"). 대안: "창 전환·단축키 매크로 리모컨" |
| 카테고리 | 기본: 유틸리티 | ✅ |  |
| 콘텐츠 권한 | 자체 콘텐츠 → 해당 없음 | ✅ |  |

**B. 가격 및 사용 가능 여부**

| 필드 | 입력값 / 지침 | 상태 | 메모 |
|---|---|---|---|
| 가격 | 무료 ($0) | ✅ | 완료 |
| 배포 국가/지역 | 모든 국가 또는 지역 | ✅ | EU는 DSA 비거래자라 자동 제외 |

**C. 앱 개인정보 보호 (App Privacy)**

| 필드 | 입력값 / 지침 | 상태 | 메모 |
|---|---|---|---|
| 데이터 수집 | "데이터를 수집하지 않습니다" (LAN-only, 수집 없음) | ✅ | 게시 완료 |
| 개인정보 처리방침 URL | https://profile.kknaks.cloud/macremote#privacy | ✅ | 2026-06-08 입력 |

**D. 이번 버전** (좌측 `App Store` → iOS 버전)

| 필드 | 입력값 / 지침 | 상태 | 메모 |
|---|---|---|---|
| 미리보기·스크린샷 | iPhone 3장 받음 (1284×2778 6.5", 알파X) → `assets/screenshots/`. iPad 불필요 | ✅ | ASC 업로드 시 6.5" 슬롯 확인 (6.9" 요구하면 1320×2868로 재요청) |
| 프로모션 텍스트 | 작성 제공 | ✅ |  |
| 설명 | 작성 제공 | ✅ |  |
| 키워드 | 작성 제공 | ✅ |  |
| 지원 URL | https://profile.kknaks.cloud/macremote | ✅ | 2026-06-08 입력 (필수 필드) |
| 마케팅 URL | https://profile.kknaks.cloud/macremote | ✅ | 랜딩 (선택) |
| 빌드 | 업로드된 빌드 선택 (build +1) | ✅ | 2026-06-08 선택 |
| 저작권 | 2026 keonhak lee | ✅ |  |
| 연령 등급 | 4+ | ✅ |  |
| App 심사 정보 — 연락처 | 이름/전화/이메일 | ✅ |  |
| App 심사 정보 — 로그인 | 로그인 없음 → 데모 계정 불필요 | ✅ |  |
| **App 심사 정보 — 메모** | companion Mac 필요·연결 절차 명시 (위 Reviewability) | ✅ | 붙여넣음 |
| **App 심사 정보 — 첨부(데모 영상)** | 📹 녹화·업로드 완료 (QR→창전환→매크로) | ✅ | 2026-06-08 업로드. ⚠️ 반려 방지 핵심 |
| 버전 출시 | 수동 / 자동 (택) | ✅ | 2026-06-08 선택 |

**E. 제출**

| 필드 | 입력값 / 지침 | 상태 | 메모 |
|---|---|---|---|
| Export Compliance | `ITSAppUsesNonExemptEncryption=NO` → 자동 통과(다이얼로그 안 뜸) | ✅ | 자동 통과 |
| 심사를 위해 제출 | Submit for Review → Apple 심사 24~48h | ⛔ | 2026-06-08 제출 → **2026-06-08 거절 (5.2.5)**. 대응은 §4 |
| 출시 후 | 승인·출시되면 `60-release/release-003-*.md` 작성 | ⬜ | 재제출·통과 대기 |
| 출시 후 | App Store 정식 URL(`apps.apple.com/app/id…`)을 랜딩 다운로드 버튼에 연결 | ⬜ | ⚠️ 출시 전엔 앱 페이지 404 → URL 발급 후 연결 |

> 입력하다 막히거나(⛔) 빠진 항목이 나오면 이 표에 행을 추가/갱신한다. 빌드 업로드 절차 자체는 위 §2(TestFlight) Deploy Steps와 동일(build number +1).

### 4. 심사 반려 대응 — Guideline 5.2.5 (지식재산권)

**반려 이력**

| 일자 | 버전(빌드) | Submission ID | 가이드라인 | 사유 |
|---|---|---|---|---|
| 2026-06-08 | 1.0.1 (4) | 7289e983-49ae-467e-86d6-52ba8d835210 | 5.2.5 IP | 메타데이터의 앱 이름·부제가 Apple 상표(Mac/iPhone)를 부적절하게 사용. **기기 표시 이름**에도 "Mac" 포함 지적 (QA1823 링크) |

> **핵심:** 이건 텍스트 두 줄만이 아니라 **기기 표시 이름**(`CFBundleDisplayName`)까지 지적됐다. ASC 텍스트만 고치면 같은 가이드라인으로 재거절된다. → **새 빌드 필수.**

**개명 결정:** `MacRemote` → **`DeskDeck`** (Apple 상표 0개, 5.2.5 재거절 리스크 사실상 0). Bundle ID `com.macremote.MacRemote`는 **변경하지 않는다** (5.2.5 대상 아님, 바꾸면 앱 레코드·심사 이력 소멸).

> Mac 헬퍼 앱 `MacHelper`는 DMG 배포라 5.2.5 대상은 아니지만 **브랜드 일관성**을 위해 `DeskDeckHelper`로 **완전 개명**한다 — 표시 이름(CFBundle*Name) + 실행파일명 + `.app`/DMG 파일명(`DeskDeckHelper-1.0.1.dmg`)까지. `CFBundleExecutable`을 실행파일명(`DeskDeckHelper`)과 일치시켜 실행 보장. **Bundle ID(`com.macremote.machelper`)와 SPM product명(`MacHelperApp`)·리소스번들(`MacHelper_MacHelperApp.bundle`)은 유지**(내부 식별자, 안 바꿔도 무방·빌드 안정). DMG 파일명이 바뀌므로 `downloads/`의 구파일 교체 + 랜딩 `DMG_URL` 갱신 필요.

**대응 체크리스트**

> ✅ = 이 작업 세션에서 코드 레포(`~/git/toy_pr2/mac-remote`)에 적용 완료. ⬜ = 사용자가 Xcode/ASC에서 수동 진행.

| # | 작업 | 위치 | 상태 |
|---|---|---|---|
| 1 | 표시 이름 `CFBundleDisplayName` + `CFBundleName` → `DeskDeck` (생성 plist가 `PRODUCT_NAME=$(TARGET_NAME)`=MacRemote를 쓰므로 **두 키 모두** 명시해야 바이너리 이름 필드에 MacRemote가 안 남음) | Swift 레포 `iOSApp` pbxproj Debug+Release | ✅ |
| 2 | 앱 내 "MacRemote" UI 노출 문자열 점검 → 프로덕션 UI 0건(프리뷰 목업/주석만) | Swift 레포 | ✅ |
| 3 | Build number +1 → **Archive → Upload** | Xcode | ⬜ `CURRENT_PROJECT_VERSION 4→5` 설정 완료, Archive/Upload만 수동 |
| 4 | ASC **앱 이름** `DeskDeck`로 수정 | ASC → App 정보 | ⬜ |
| 5 | ASC **부제** "내 컴퓨터가 손안의 리모컨으로"로 수정 | ASC → App 정보 | ⬜ |
| 6 | 새 빌드 선택 (이번 버전) | ASC → 빌드 | ⬜ |
| 7 | Resolution Center에 회신 (아래 회신문) | ASC → 메시지 | ⬜ |
| 8 | Submit for Review 재제출 | ASC | ⬜ |
| 9 | 지원/개인정보 페이지 앱 이름 `DeskDeck`·헬퍼 `DeskDeckHelper`로 갱신 | `assets/appstore/pages/*.md` | ✅ |
| 10 | (헬퍼) MacHelper Info.plist 표시 이름 → `DeskDeckHelper`, `CFBundleExecutable=MacHelper` 고정, `CFBundleVersion 2→3` | Swift 레포 `MacHelper` | ✅ |
| 11 | (헬퍼) 새 DMG 빌드 → 공증·staple → `downloads/`에 `DeskDeckHelper-1.0.1.dmg` 배치(구 `MacHelper-1.0.1.dmg` 제거) | `scripts/build_dmg.sh` | ✅ 공증 통과 (Submission `3a01477f-9d26-4fb2-8895-638f2eac97eb`, source=Notarized Developer ID) |
| 12 | 랜딩(`/macremote`) 표기 `DeskDeck`/`DeskDeckHelper` + `DMG_URL` 파일명 갱신 | front `public/macremote/index.html` + 소스 | ✅ 배포 필요 |
| 13 | RB-001 / 백엔드 deploy README 산출물명·다운로드 URL 갱신 (SPM 내부명 유지) | `runbook-001`, `40-architecture/deploy/back` | ✅ |

**Resolution Center 회신문 (초안)**

```
Thank you for the review.

We have addressed Guideline 5.2.5:
- The app name has been changed from "MacRemote" to "DeskDeck",
  removing the Apple trademark from both the App Store name and the
  on-device display name (CFBundleDisplayName) in a new build.
- The subtitle no longer references "Mac" or "iPhone" and now
  describes the app's function generically.

The new build (build +1) with the updated display name has been
uploaded and selected for this version. Please re-review.
```

## 검증

| Check | 기대값 | 방법 |
|---|---|---|
| 아이콘 알파 | `hasAlpha: no` | `sips -g hasAlpha .../AppIcon-1024.png` |
| 로컬 네트워크 권한 키 | `2` | `grep -c NSLocalNetworkUsageDescription .../project.pbxproj` |
| Export compliance 키 | `2` | `grep -c ITSAppUsesNonExemptEncryption .../project.pbxproj` |
| TestFlight 설치 후 연결 | Mac 페어링 성공 | 실기기 + 로컬 네트워크 권한 허용 |

## 트러블슈팅

| 증상 | 원인 / 해결 |
|---|---|
| `Invalid large app icon … alpha channel` | 1024 아이콘 알파 채널. 평탄화. |
| `Missing … NSLocalNetworkUsageDescription` | 권한 키 누락. project.pbxproj에 추가. |
| TestFlight 후 "Missing Compliance" | `ITSAppUsesNonExemptEncryption = NO` 누락. 추가하면 다음 빌드부터 안 뜸. |
| iPhone 설치 후 연결 안 됨(조용히 실패) | 로컬 네트워크 권한 거부. 설정 → MacRemote → 허용. |
| Archive 메뉴 회색 | Destination이 시뮬레이터. "Any iOS Device (arm64)"로 변경. |
| **심사 반려: 앱이 동작하지 않음** | companion Mac 미설명. App Review 노트 + 데모 영상으로 Mac 헬퍼 필요를 설명 후 재제출. |

## 관련 파일

- `iOSApp/MacRemote.xcodeproj`
- `iOSApp/iOSApp/Assets.xcassets/AppIcon.appiconset/` (1024 알파 금지)
- 배포 구조: `40-architecture/deploy/front/README.md`
- **제출 자산(스크린샷·아이콘) manifest**: [assets/README.md](assets/README.md)
- 짝 런북: [runbook-001-mac-dmg-release.md](runbook-001-mac-dmg-release.md)
