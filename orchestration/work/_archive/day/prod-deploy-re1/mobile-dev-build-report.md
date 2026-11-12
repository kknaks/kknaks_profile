# [mobile] DAY Dev TestFlight 빌드 3 업로드 결과 보고

## 상태: done — 0.1.0 (3) 업로드 · `processingState = VALID` · 내부 `IN_BETA_TESTING`

- 워크트리 `CENTURION_DAY/prod-deploy-re1` · 브랜치 `kknaksss/prod-deploy-re1` · 커밋 **`1d4ccfba`**(A2 「정보」 · 그 앞 `01bbed49` A1 포함). 시작 때 tracked 변경 0(미추적 `app/store/` · `app/tool/store_capture/` 만 — 손대지 않음).
- 소스 · 프로젝트 파일 수정 0 · 커밋 · push 0 · 테스터 · 그룹 · 베타 심사 제출 0 · 정식 앱 `day.medisolveai` 변경 0.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰은 출력하지 않았다(`credentials.local.json` → 셸 변수 · ExportOptions.plist 의 teamID 는 `app/build/tf3/`(무시 폴더) 안에만).

## 단계별 결과

| 단계 | 결과 |
|---|---|
| ASC 사전 조회(API · DAY Dev) | 빌드 0.1.0 (1) · (2) 둘 다 VALID → **빌드 번호 3** |
| config(`flutter build ios --release --config-only --build-name=0.1.0 --build-number=3` + `DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = `https://day-dev.medisolveai.com` · `DAY_APNS_ENV=production`) | OK (flutter 3.44.8 fvm) |
| archive(서명 없이 · `DAY_BUNDLE_ID=day.medisolveai.dev` · `DAY_DISPLAY_NAME=DAY Dev` · `CODE_SIGNING_ALLOWED=NO`) | **ARCHIVE SUCCEEDED** (1회) |
| 앱만 `ios/Runner/Runner.entitlements` ad-hoc(`--generate-entitlement-der`) | OK |
| export(`app-store-connect` · automatic · `-allowProvisioningUpdates` · DAY API 키) | **EXPORT SUCCEEDED** · IPA **22,247,048 bytes** |
| `altool --validate-app` | **VERIFY SUCCEEDED** · 오류 0 · 경고 1(90068 iOS 13.0 배포 대상 — 빌드 1 · 2 와 같음) |
| `altool --upload-app` | **UPLOAD SUCCEEDED** · 22,247,048 bytes · 경고 1(90068) · **12:09 KST** · Delivery UUID `7a8d6f58-e161-4753-a3d4-ba1b05336381` |
| ASC 처리 | **12:12:59 KST 조회에서 VALID**(업로드 뒤 약 4분) |

## IPA 확인 — `app/build/tf3/ipa/DAY Dev.ipa`

| 항목 | 값 | 결과 |
|---|---|---|
| `CFBundleIdentifier` | `day.medisolveai.dev` | OK |
| `CFBundleDisplayName` | `DAY Dev` | OK |
| `CFBundleShortVersionString` | `0.1.0` | OK |
| `CFBundleVersion` | `3` | OK |
| `ITSAppUsesNonExemptEncryption` | `false` | OK |
| 아이콘 | `CFBundleIcons(~ipad).CFBundlePrimaryIcon.CFBundleIconName = AppIcon` · `Assets.car` AppIcon phone 29–180 · pad 20–167 · marketing 1024 · `AppIcon60x60@2x.png` · `AppIcon76x76@2x~ipad.png` | OK |
| entitlements `aps-environment` | `production` | OK |
| entitlements 그 밖 | `application-identifier = <team>.day.medisolveai.dev` · `beta-reports-active = true` · `get-task-allow = false` · team-identifier | OK |
| 서명 | `Apple Distribution: Medisolve AI Co., Ltd. (<가림>)` · `codesign --verify --deep --strict` 통과 · Frameworks 3개(App · Flutter · flutter_pcm_sound) 모두 배포 서명 | OK |
| 프로파일 | `iOS Team Store Provisioning Profile: day.medisolveai.dev` · `aps-environment = production` | OK |
| dart-define | `App.framework` 안 서버 주소 = `https://day-dev.medisolveai.com` 하나. 그 밖 `https://day.medisolveai.com/privacy` 는 A2 설정 「정보」 개인정보 링크(고정 · 서버 origin 아님) | OK |
| MinimumOSVersion | 13.0 | (경고 90068) |

## ASC 빌드 상태

| 항목 | 값 |
|---|---|
| 앱 | DAY Dev (`day.medisolveai.dev`) |
| 버전 · 빌드 | **0.1.0 · 3** |
| `processingState` | **VALID** (12:12:59 KST 확인 · uploadedDate 2026-11-11T19:10:40-08:00) |
| `usesNonExemptEncryption` | false |
| `internalBuildState` | **IN_BETA_TESTING** |
| `externalBuildState` | READY_FOR_BETA_SUBMISSION(제출 안 함) |
| expired | false |

## 새 서명 자산
0 — 이 Mac 프로파일 폴더 최신 파일 시각이 11-11(이번 작업 전). export 가 기존 Cloud Managed 배포 인증서 · App Store 프로파일을 다시 씀.

## git status (끝)
```
?? app/store/
?? app/tool/store_capture/
```
HEAD `1d4ccfba` 그대로. `ios/Flutter/Generated.xcconfig` 는 config 가 다시 썼지만 무시 파일. 임시 파일(ExportOptions · 로그 · archive · IPA)은 `app/build/tf3/`, 풀어 본 IPA 는 지움.

## 미결 · 주의
1. 경고 90068: iOS 13.0 → 2027-04 전에 15.0 이상(범위 밖).
2. 다음 업로드는 빌드 번호 4 이상.
3. day.json `apple.state` 에 「빌드 3」 줄 추가는 코디 몫(이번에 고치지 않음).
