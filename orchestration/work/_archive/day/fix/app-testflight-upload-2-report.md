# [mobile] DAY Dev TestFlight 빌드 2 업로드 결과 보고

## 상태: done — 0.1.0 (2) 업로드 · `processingState = VALID` · 수출 규정 누락 없음

- 워크트리 `CENTURION_DAY/fix` · 브랜치 `kknaksss/fix-app-re1` · 커밋 `87cf2dec` 그대로 빌드(시작 때 워크트리 깨끗). 소스 · 프로젝트 파일 수정 0 · 커밋 · push 0.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰 · 인증서 일련번호는 적지 않았다. 값은 `credentials.local.json` 에서 셸 변수로만 읽었다. `~/.appstoreconnect/private_keys/` 는 쓰지 않았다.
- 테스터 · 그룹 추가 · 베타 심사 제출 · 정식 앱 `day.medisolveai` 변경 0.

## 단계별 결과

| 단계 | 결과 |
|---|---|
| ASC 사전 조회 | DAY Dev 빌드 1개(0.1.0 (1)) → **빌드 번호 2** 그대로 씀 |
| config(`flutter build ios --release --config-only --build-name=0.1.0 --build-number=2` + dart-define 3개: `DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = `https://day-dev.medisolveai.com` · `DAY_APNS_ENV=production`) | OK |
| archive(서명 없이 · `DAY_BUNDLE_ID=day.medisolveai.dev` · `DAY_DISPLAY_NAME=DAY Dev` · `CODE_SIGNING_ALLOWED=NO`) | **ARCHIVE SUCCEEDED** (1회) |
| 앱만 `ios/Runner/Runner.entitlements` 로 ad-hoc 서명(`codesign --force --sign - --entitlements … --generate-entitlement-der`) | OK |
| export(`app-store-connect` · 자동 서명 · `-allowProvisioningUpdates` · DAY API 키) | **EXPORT SUCCEEDED** · IPA 22,244,730 bytes |
| IPA 확인 | 아래 표 전부 OK |
| `altool --validate-app` | **VERIFY SUCCEEDED** · 오류 0 · 경고 1(90068 — 배포 대상 iOS 13.0, 2027-04 부터 15.0 필요 · 빌드 1과 같음) |
| `altool --upload-app` | **UPLOAD SUCCEEDED** · 22,244,730 bytes · 경고 1(같은 90068) · 16:32 KST |
| ASC 처리 | 16:36 조회에서 **VALID**(약 4분) |

절차는 빌드 1 5차와 같다. 임시 파일은 전부 `app/build/tf2/`(ExportOptions.plist 는 빌드 1 것 복사 · 로그 · archive · IPA). 풀어 본 IPA 폴더는 지웠다.

## IPA 확인 — `app/build/tf2/ipa/DAY Dev.ipa`

| 항목 | 값 | 결과 |
|---|---|---|
| `CFBundleIdentifier` | `day.medisolveai.dev` | OK |
| `CFBundleDisplayName` | `DAY Dev` | OK |
| `CFBundleShortVersionString` | `0.1.0`(pubspec 그대로) | OK |
| `CFBundleVersion` | `2` | OK |
| **`ITSAppUsesNonExemptEncryption`** | `false` | OK |
| 아이콘 | `CFBundleIconName = AppIcon` · `Assets.car` AppIcon phone 29–180(8) · pad 20–167(8) · marketing 1024 · `AppIcon60x60@2x.png` · `AppIcon76x76@2x~ipad.png` | OK |
| entitlements `aps-environment` | `production` | OK |
| entitlements 그 밖 | `application-identifier = <team>.day.medisolveai.dev` · `beta-reports-active = true` · `get-task-allow = false` · team-identifier | OK |
| 서명 | `Apple Distribution: Medisolve AI Co., Ltd. (<가림>)` · `codesign --verify --deep --strict` 통과 · Frameworks 3개(App · Flutter · flutter_pcm_sound) 모두 배포 서명 | OK |
| 프로파일 | `iOS Team Store Provisioning Profile: day.medisolveai.dev` · 프로파일 `aps-environment = production` | OK |
| dart-define | `App.framework` 안 서버 주소 = `https://day-dev.medisolveai.com` 만 | OK |
| MinimumOSVersion | 13.0 | (경고 90068 원인 · 지금은 막지 않음) |

## ASC 빌드 상태

| 항목 | 값 |
|---|---|
| 앱 | DAY Dev (`day.medisolveai.dev`) |
| 버전 · 빌드 번호 | **0.1.0 · 2** |
| `processingState` | **VALID** |
| `usesNonExemptEncryption` | **false** (API 로 고치지 않음 — Info.plist 키로 들어감) |
| `buildBetaDetail.internalBuildState` | **`IN_BETA_TESTING`** — `MISSING_EXPORT_COMPLIANCE` 아님 |
| `buildBetaDetail.externalBuildState` | `READY_FOR_BETA_SUBMISSION`(외부 심사 제출 안 함) |
| expired | false |

→ 빌드 1 때 남긴 확인 항목(수출 규정이 누락으로 서지 않는가) **해결 확인**. 내부 테스트 상태가 바로 `IN_BETA_TESTING` 이라, 이미 있는 내부 테스터는 TestFlight 에서 빌드 2를 받을 수 있다(테스터 · 그룹은 손대지 않음).

## 새 서명 자산

**0** — export 가 빌드 1 때 만든 Cloud Managed Apple Distribution 인증서 · App Store 프로파일(`iOS Team Store Provisioning Profile: day.medisolveai.dev`)을 다시 썼다.
- ASC API 인증서 목록: 빌드 1 뒤와 같음(DEVELOPMENT 1).
- 이 Mac 의 프로파일 폴더: 이번 작업 시각 이후 새 파일 0.
- 키체인 서명 identity: 빌드 1 뒤와 같음(새 것 없음).

## git status

```
On branch kknaksss/fix-app-re1
Your branch is up to date with 'origin/kknaksss/fix-app-re1'.

nothing to commit, working tree clean
```

`ios/Flutter/Generated.xcconfig` 는 config 단계가 다시 썼지만 무시 파일(빌드 번호 2 · dev define 이 들어 있음 — 다음 `flutter build`/`run` 이 다시 씀).

## 미결 · 주의

1. 경고 90068: 배포 대상 iOS 13.0 → 2027-04 전에 15.0 이상으로 올려야 업로드 가능(소스 변경 · 범위 밖).
2. 서명 절차(서명 없이 archive → ad-hoc entitlements → 자동 export)는 아직 저장소 문서에 없다 — 빌드 1 보고 미결 1 그대로.
3. 다음 업로드는 빌드 번호 3 이상.
