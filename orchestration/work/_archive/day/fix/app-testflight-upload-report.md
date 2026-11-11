# [mobile] DAY Dev 첫 TestFlight 업로드 결과 보고

## 상태: done (업로드 · 처리 VALID) — TestFlight 배포는 수출 규정 답 대기

- 워크트리 `CENTURION_DAY/fix` (`kknaksss/fix`) — 앞 판 미커밋 변경(아이콘 · README) 위에서 빌드. 소스 수정 0 · 커밋 · push · PR 0.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰 · 인증서 일련번호는 적지 않았다(명령 출력은 가려서 봤다). 값은 `credentials.local.json` 에서 셸 변수로만 읽었다.

## 요약

| 단계 | 결과 |
|---|---|
| ASC 사전 조회 | 앱 「DAY Dev」(`day.medisolveai.dev`) 있음 · 빌드 0개 → **빌드 번호 1** 그대로 |
| config(`flutter build ios --config-only`) | OK — 0.1.0 (1) · dart-define 3개만 |
| archive 1차(자동 서명) | **실패** — 아래 「겪은 오류」 ① |
| archive 2차(자동 + `CODE_SIGN_IDENTITY=Apple Distribution`) | **실패** — ② |
| archive 3차(서명 없이) → export | 성공했지만 IPA 에 `aps-environment` **없음** → 버림 — ③ |
| archive 4차(수동 · ad-hoc) | **실패** — ④ |
| **archive 5차(서명 없이) + 앱만 저장소 entitlements 로 ad-hoc 서명 → export(자동 · app-store-connect)** | **성공** — IPA 확인 표 통과 |
| `altool --validate-app` | **VERIFY SUCCEEDED** · 오류 0 · 경고 1(90068 배포 대상 낮음) |
| `altool --upload-app` | **성공** · 22,228,271 bytes · 경고 1(같은 90068) |
| ASC 처리 | **VALID**(업로드 11:14 → 11:20 조회에서 VALID · 약 6분) |

## 실제로 돌린 명령(값은 가림 · `app/` 에서)

```sh
# 값은 credentials.local.json 에서 셸 변수로 — 화면에 내지 않음
eval "$(python3 -c '... TEAM_ID · ASC_KEY_ID · ASC_ISSUER · ASC_KEY_PATH(= app_store_connect.private_key_path) ...')"

fvm flutter build ios --release --config-only --build-name=0.1.0 --build-number=1 \
  --dart-define=DAY_LOGIN_ENTRY=https://day-dev.medisolveai.com \
  --dart-define=DAY_ALLOWED_ORIGINS=https://day-dev.medisolveai.com \
  --dart-define=DAY_APNS_ENV=production

# 최종 archive(5차) — 서명 없이 빌드, Bundle ID · 이름은 명령줄 빌드 설정
xcodebuild -workspace ios/Runner.xcworkspace -scheme Runner -configuration Release \
  -destination 'generic/platform=iOS' -archivePath build/tf/DAYDev.xcarchive \
  DAY_BUNDLE_ID=day.medisolveai.dev 'DAY_DISPLAY_NAME=DAY Dev' CODE_SIGNING_ALLOWED=NO archive
# 앱 번들에 저장소 entitlements(aps-environment)를 ad-hoc 으로 실어 둔다 — export 가 이것을 보고 production 으로 바꿔 서명
codesign --force --sign - --entitlements ios/Runner/Runner.entitlements --generate-entitlement-der \
  build/tf/DAYDev.xcarchive/Products/Applications/Runner.app

# export — build/tf/ExportOptions.plist: method app-store-connect · teamID $TEAM_ID · signingStyle automatic · destination export
xcodebuild -exportArchive -archivePath build/tf/DAYDev.xcarchive -exportPath build/tf/ipa \
  -exportOptionsPlist build/tf/ExportOptions.plist -allowProvisioningUpdates \
  -authenticationKeyPath "$ASC_KEY_PATH" -authenticationKeyID "$ASC_KEY_ID" -authenticationKeyIssuerID "$ASC_ISSUER"

API_PRIVATE_KEYS_DIR=~/.config/day/apple xcrun altool --validate-app -t ios -f "build/tf/ipa/DAY Dev.ipa" --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER"
API_PRIVATE_KEYS_DIR=~/.config/day/apple xcrun altool --upload-app   -t ios -f "build/tf/ipa/DAY Dev.ipa" --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER"
```

`~/.appstoreconnect/private_keys/` 는 쓰지 않았다. 키 복사 · 이동 0.

## 겪은 오류(원문 · 가림)와 원인

① 자동 서명 archive:
```
error: Communication with Apple failed: Your team has no devices from which to generate a provisioning profile. Connect a device to use or manually add device IDs in Certificates, Identifiers & Profiles.
error: No profiles for 'day.medisolveai.dev' were found: Xcode couldn't find any iOS App Development provisioning profiles matching 'day.medisolveai.dev'.
```
원인: 자동 서명은 archive 를 **개발** 서명으로 하고, 팀에 등록 기기가 0개라 개발 프로파일을 못 만든다. 기기 등록은 금지라 우회.
이 시도에서 Xcode 가 DAY 팀 **Apple Development 인증서 1개**를 만들었다(아래 「새 서명 자산」).

② `CODE_SIGN_IDENTITY=Apple Distribution` 명령줄 덮어쓰기: `Runner has conflicting provisioning settings. Runner is automatically signed for development, but a conflicting code signing identity Apple Distribution has been manually specified.` (Pods · SPM 타깃 전부 같은 오류)

③ 서명 없는 archive → export 는 성공했지만 앱 entitlements 가 `application-identifier · beta-reports-active · team-identifier · get-task-allow` 뿐, **`aps-environment` 없음**(서명 없이 빌드하면 `Runner.entitlements` 가 실리지 않아 export 가 넣을 근거가 없다). 푸시가 안 되므로 올리지 않고 버렸다.

④ `CODE_SIGN_STYLE=Manual CODE_SIGN_IDENTITY=-`: `"Runner" requires a provisioning profile.`

→ 5차: 서명 없이 archive 한 뒤 **빌드 산출물(app/build 안)의 앱만** `Runner.entitlements` 로 ad-hoc 서명. 소스 · 프로젝트 파일은 그대로. export 가 클라우드 배포 인증서로 다시 서명하며 `aps-environment` 를 production 으로 바꿨다(아래 표).

## IPA 확인(§2-4) — `build/tf/ipa/DAY Dev.ipa`

| 항목 | 값 | 결과 |
|---|---|---|
| `CFBundleIdentifier` | `day.medisolveai.dev` | OK |
| `CFBundleDisplayName` | `DAY Dev` | OK |
| `CFBundleShortVersionString` | `0.1.0` | OK |
| `CFBundleVersion` | `1` | OK |
| 아이콘 | `CFBundleIcons…CFBundleIconName = AppIcon` · `Assets.car` AppIcon phone 29–180 · pad 20–167 · marketing 1024 · `AppIcon60x60@2x.png` · `AppIcon76x76@2x~ipad.png` | OK |
| entitlements `aps-environment` | `production` | OK |
| entitlements `application-identifier` | `<team>.day.medisolveai.dev` | OK |
| 그 밖 entitlements | `beta-reports-active = true` · `get-task-allow = false` · `com.apple.developer.team-identifier` | OK |
| 서명 | `Apple Distribution: Medisolve AI Co., Ltd. (<가림>)` · `codesign --verify --deep --strict` 통과 · Frameworks 3개(App · Flutter · flutter_pcm_sound) 모두 배포 서명 | OK |
| 프로파일 | `iOS Team Store Provisioning Profile: day.medisolveai.dev` · 프로파일 entitlements `aps-environment = production` · 기기 목록 없음 | OK |
| dart-define | `App.framework` 안 서버 주소 문자열 = `https://day-dev.medisolveai.com` 만 | OK |

## ASC 빌드 상태

ASC API 조회(1~2분 간격 · 5회째에 확정):

| 항목 | 값 |
|---|---|
| 앱 | DAY Dev (`day.medisolveai.dev`) |
| 버전 · 빌드 번호 | 0.1.0 · 1 (ASC 에 기존 빌드 0개 — 번호 올리지 않음) |
| `processingState` | **VALID** |
| `usesNonExemptEncryption` | 없음(null) |
| `buildBetaDetail` internal · external | **`MISSING_EXPORT_COMPLIANCE`** — 수출 규정 준수 정보 누락 |
| expired | false |

## 새로 생긴 서명 자산(종류 · 개수만)

| 종류 | 개수 | 어디서 |
|---|---|---|
| Apple Development 인증서(DAY 팀) | 1 | archive 1차의 자동 서명이 만듦 · 이 Mac 키체인에 개인키 · 만료 2027-11-11. **브리프 허용 범위(배포 인증서 · 프로파일) 밖의 부산물** — 지울지 코디 · 사용자 판단 |
| Cloud Managed Apple Distribution 인증서 | 1 | export 의 자동 서명(Apple 클라우드 관리 · 이 Mac 에 개인키 없음 · ASC API 인증서 목록에는 안 보임) · 만료 2027-11-11 |
| App Store 프로파일 `iOS Team Store Provisioning Profile: day.medisolveai.dev` | 1 | export 의 자동 서명(Xcode 관리 · 이 Mac 에 받아 둠 · ASC API 프로파일 목록에는 안 보임) |

기기 등록 · 다른 App ID · capability 변경 0. 정식 앱 `day.medisolveai` 손대지 않음. 테스터 · 그룹 · 베타 심사 · 앱 정보 입력 0.

## git status

`git status --short` = 앞 판과 같다(18줄 · diff 0). `Identity.local.xcconfig` 를 쓰지 않았고 없다. 임시 파일(ExportOptions.plist · 로그 · archive · IPA · 풀어 본 IPA)은 전부 `app/build/tf/` 안(`.gitignore`). `ios/Flutter/Generated.xcconfig` 는 config 단계가 다시 썼지만 원래 무시 파일이고 지금 dev define 이 들어 있다 — 다음 `flutter build`/`run` 이 다시 쓴다.

## 미결 · 주의

1. **다음 업로드부터의 서명 방법** — 기기 0개인 팀에서 자동 서명 archive 는 실패한다. 이번 우회(서명 없이 archive → 앱만 entitlements ad-hoc 서명 → export 자동 서명)는 저장소에 적혀 있지 않다. 정식화하려면 (가) 이 절차를 README 에 적기, (나) 기기 1대를 등록해 표준 자동 서명 archive, (다) Release 를 수동 서명(배포 인증서 · 프로파일 고정) 중 하나를 사용자가 정한다.
2. **경고 90068**: 배포 대상 iOS 13.0 — 2027-04 부터 15.0 이상이어야 업로드 가능. 지금은 업로드 막지 않음.
3. **수출 규정(암호화)**: `ITSAppUsesNonExemptEncryption` 이 Info.plist 에 없다 — 지어 넣지 않았다. 빌드는 지금 internal · external 모두 **`MISSING_EXPORT_COMPLIANCE`** — 사용자가 App Store Connect 웹(TestFlight → 빌드 1 → 수출 규정)에서 답해야 테스터에게 배포된다. 다음 빌드부터 묻지 않게 하려면 Info.plist 에 키를 넣을지 정해야 한다(소스 변경 · 이번 범위 밖).
4. 빌드 번호: 다음 업로드는 2 이상.
5. 사용자가 실기기에서 받으려면 TestFlight 내부 테스터 추가가 필요(이번 범위 밖 · 사용자 몫).
