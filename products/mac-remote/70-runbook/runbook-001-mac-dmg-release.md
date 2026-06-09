---
type: runbook
id: MRT-RB-001
title: "Mac 헬퍼 DMG 배포"
status: active
product: mac-remote
area: deploy
created_at: 2026-05-25
updated_at: 2026-06-03
tags:
  - product/mac-remote
  - doc/runbook
  - status/active
links:
  baselines: []
  decisions: []
  specs: []
  works: []
  releases:
    - "[[release-001-v1-0-0|MRT-REL-001]]"
    - "[[release-002-v1-0-1|MRT-REL-002]]"
  related: []
---

# Mac 헬퍼 DMG 배포

DeskDeckHelper를 Developer ID 사인된 DMG로 패키징해 외부 배포한다.

> 배포 환경/타겟 정적 구조는 `40-architecture/deploy/back/README.md`에 있다. 이 문서는 실행 절차만 둔다.
> 원본: `mac-remote/doc/runbook/mac-dmg-release.md` (전체 트러블슈팅·CSR 발급 절차는 원본 참조).

## 목적

DeskDeckHelper를 Universal Binary(arm64 + x86_64) + Developer ID 사인 DMG로 만들어 외부에 배포한다.

> **공증 정책**: 외부 공개 배포(랜딩 페이지)로 전환하면서 **공증(notarization)을 적용**한다. 공증 후에는 받는 사람이 **더블클릭으로 바로 실행**할 수 있다(경고 없음). 절차는 아래 §공증 참조.

## 사전 준비 (최초 1회)

- Apple Developer Program 가입 ($99/년).
- **Developer ID Application** 인증서 발급 (App Store용 `Apple Distribution`과 다름, 외부 직접 배포 전용).
  - Keychain Access → 인증서 지원 → CSR 생성 → developer.apple.com에서 Developer ID Application 발급 → `.cer` 더블클릭 설치.
- 설치 확인:
  ```bash
  security find-identity -v -p codesigning | grep "Developer ID Application"
  ```

## 절차

```bash
cd /path/to/mac-remote
./scripts/build_dmg.sh                # 버전: Info.plist의 CFBundleShortVersionString
./scripts/build_dmg.sh 1.0.1          # 버전 명시
SIGN_ID="Developer ID Application: ... (TEAMID)" ./scripts/build_dmg.sh   # 인증서 명시
```

스크립트가 하는 일:

1. Clean & Universal Release 빌드 — `swift build -c release --arch arm64 --arch x86_64`
2. `.app` 번들 조립 (실행 바이너리, Info.plist, AppIcon.icns, 메뉴바 아이콘 리소스 번들)
3. Codesign — Developer ID + `--timestamp` + `--options runtime` (hardened runtime)
4. DMG 생성 — `hdiutil create` UDZO 압축, `/Applications` 심볼릭 링크 포함
5. DMG 사인 — DMG 파일 자체도 Developer ID로 사인

받는 사람 설치: DMG 더블클릭 → DeskDeckHelper.app을 Applications로 드래그 → **더블클릭 실행**(공증돼서 경고 없음) → 권한 허용(손쉬운 사용 필수, 화면 기록 선택) → 메뉴바 QR로 iPhone 연결.

## 공증 (Notarization)

외부 배포용 DMG는 공증해 Gatekeeper 경고를 없앤다. (DMG 빌드 후 실행)

### 1. 자격증명 저장 (최초 1회)

App 전용 암호를 https://appleid.apple.com → 로그인 → "앱 암호"에서 발급한 뒤:

```bash
xcrun notarytool store-credentials "AC_NOTARY" \
  --apple-id "<APPLE_ID 이메일>" \
  --team-id "<TEAM_ID>" \
  --password "xxxx-xxxx-xxxx-xxxx"
```

### 2. 공증 + staple

```bash
DMG="build/DeskDeckHelper-1.0.1.dmg"

# 업로드 → Apple 자동 스캔 → 결과 대기 (보통 수 분)
xcrun notarytool submit "$DMG" --keychain-profile "AC_NOTARY" --wait

# 통과하면 티켓을 DMG에 부착 (오프라인에서도 Gatekeeper 통과)
xcrun stapler staple "$DMG"
```

> 실패 시 `xcrun notarytool log <submission-id> --keychain-profile "AC_NOTARY"`로 사유 확인. 흔한 원인: hardened runtime 누락(`--options runtime`), 서명 안 된 바이너리 포함.
> 정식 채택 시 `scripts/notarize_dmg.sh`로 분리하거나 `build_dmg.sh` 마지막 단계에 추가한다.

## 검증

| Check | 기대값 | 방법 |
|---|---|---|
| 사인 정보 | `Developer ID Application: ... (TeamID)` | `codesign -dv --verbose=2 build/DeskDeckHelper.app` |
| 사인 검증 | 통과 | `codesign --verify --deep --strict --verbose=2 build/DeskDeckHelper.app` |
| 아키텍처 | `x86_64 arm64` | `lipo -info build/DeskDeckHelper.app/Contents/MacOS/DeskDeckHelper` |
| 공증 결과 | `accepted, source=Notarized Developer ID` | `spctl --assess --type open --context context:primary-signature -v build/DeskDeckHelper-<ver>.dmg` |

## 트러블슈팅

| 증상 | 원인 / 해결 |
|---|---|
| `'Developer ID Application' 인증서를 찾지 못했습니다` | 인증서 발급 누락 또는 다른 키체인. 로그인 키체인으로 옮기기. |
| `errSecInternalComponent` codesign 실패 | 키체인 잠김. `security unlock-keychain login.keychain` 후 재시도. |
| `MacHelper_MacHelperApp.bundle` 없음 | 메뉴바 아이콘 리소스 번들 미생성. `swift build -c release` 정상 완료/`Package.swift` resources 확인. |
| 받는 Mac에서 "손상되어 열 수 없음" | DMG 전송 중 손상. 다시 받기, 또는 `xattr -d com.apple.quarantine DeskDeckHelper.app`. |
| 공증했는데도 "확인되지 않은 개발자" 경고 | staple 누락. `xcrun stapler staple "$DMG"` 재실행 후 `xcrun stapler validate "$DMG"`로 확인. |

## 관련 파일

- `scripts/build_dmg.sh`, `scripts/install_machelper.sh` (로컬 ad-hoc 설치)
- `MacHelper/Sources/MacHelperApp/Info.plist`, `icon/AppIcon.icns`
- 배포 구조: `40-architecture/deploy/back/README.md`

## 다운로드 호스팅

공증+staple된 DMG는 `kknaks_profile` 백엔드(FastAPI)에서 정적 서빙한다.

- DMG 위치: repo 루트 `downloads/DeskDeckHelper-<ver>.dmg` (git 커밋 → 서버 git pull 배포)
- 마운트: `app/back/main.py` — `app.mount("/download", StaticFiles(directory=PERSONA_DIR.parent / "downloads"))` (기존 `/assets` 패턴)
- 공개 URL: `https://profile-api.kknaks.cloud/download/DeskDeckHelper-<ver>.dmg`
- ⚠️ 마운트는 import 시점에 등록되므로, 배포 후 **back 컨테이너 재시작** 필요 (`docker compose restart back`)
- 랜딩 페이지(`/macremote`) `CONFIG.DMG_URL`에 위 URL을 넣는다.
