# [mobile] TestFlight 준비 결과 보고 — 개발용 Bundle ID 등록 + 앱 아이콘

## 상태: done

- 워크트리 `CENTURION_DAY/fix` (브랜치 `kknaksss/fix`, base `origin/dev`). 커밋 · push · PR 안 함.
- 비밀값(Key ID · Issuer ID · Team ID · 키 내용 · 토큰 · bundle resource id)은 이 리포트 · 화면 · 로그에 적지 않았다.

## 수행 — 변경 파일

| 파일 | 내용 |
|---|---|
| `app/assets/brand/app-icon.svg` (새) | 아이콘 원본 1개. 원본 SVG 에서 도형 `fill` 만 `#6F21FF` → `#1D8BFF`, 도형 아래 흰 불투명 배경 `<rect 512x512 #FFFFFF>` 한 줄 추가. path 좌표 · viewBox 는 원본과 같다(원본 대비 diff = 색 1곳 + rect 1줄) |
| `app/ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json` | 선언된 19칸 모두에 `filename` 추가. 칸 구성은 그대로 |
| `app/ios/Runner/Assets.xcassets/AppIcon.appiconset/Icon-App-*.png` (새 15개) | 19칸용 PNG(아이폰 · 아이패드가 같은 크기 칸은 같은 파일 공유 — Flutter 템플릿과 같은 방식). 전부 RGB(알파 없음) · 합계 약 76KB |
| `app/README.md` | 「개발 / 정식 빌드(Bundle ID · 이름)」 표 · 넣는 법, 「앱 아이콘」 원본 위치 · 다시 만드는 명령 추가. 「사용자가 나중에 할 것」의 Bundle ID · 아이콘 줄을 지금 상태로 고침 |
| 레포 밖 `~/.config/day/apple/credentials.local.json` | `dev_app` 칸 추가(아래 A). 기존 칸 값 · 서식 동일(원본이 indent-2 JSON 이라 다시 써도 기존 줄 그대로), 권한 600 유지 |

xcconfig · Info.plist · project.pbxproj 는 **손대지 않았다** — 이미 `PRODUCT_BUNDLE_IDENTIFIER = $(DAY_BUNDLE_ID)` · `CFBundleDisplayName/CFBundleName = $(DAY_DISPLAY_NAME)` 로 빌드 설정에서 받는다. Dart(`app/lib` · `app/test`) 변경 없음.

## A. 개발용 Bundle ID — App Store Connect API

스크립트는 scratchpad 에만(레포 밖). JWT(ES256 · aud `appstoreconnect-v1` · 10분)는 프로세스 안에서만.

1. 사전 조회: `day.medisolveai.dev` **없음** 확인. 기존 `day.medisolveai` = platform `UNIVERSAL` · capability `IN_APP_PURCHASE` · `PUSH_NOTIFICATIONS`.
2. `POST /v1/bundleIds` (identifier `day.medisolveai.dev` · name `DAY Dev` · platform `UNIVERSAL`) → **201**.
3. capability: `IN_APP_PURCHASE` 는 Apple 이 새 App ID 에 기본으로 켜 둔 상태라 이미 켜져 있었다(POST 안 함). `POST /v1/bundleIdCapabilities PUSH_NOTIFICATIONS` → **201**. prod 에 없는 capability 는 0개.
4. 재조회 결과:

| | identifier | name | platform | capabilities |
|---|---|---|---|---|
| 정식(조회만) | `day.medisolveai` | `DAY` | UNIVERSAL | IN_APP_PURCHASE · PUSH_NOTIFICATIONS |
| 개발(새로) | `day.medisolveai.dev` | `DAY Dev` | UNIVERSAL | IN_APP_PURCHASE · PUSH_NOTIFICATIONS |

5. `credentials.local.json` 에 `dev_app = { bundle_id: "day.medisolveai.dev", app_name: "DAY Dev", bundle_resource_id: <설정됨>, push_notifications_enabled: true }`. 기존 칸 비교 = 동일.

`day.medisolveai` 수정 · 삭제 0. 앱 record · 인증서 · 프로파일 · 기기 등록 0.

## B. 앱 아이콘

- 원본 `app/assets/brand/app-icon.svg` → resvg(resvg-py)로 칸마다 렌더 → Pillow 로 RGB(알파 제거) 저장. 명령은 `app/README.md` 「앱 아이콘」에 있다. **README 명령을 그대로 다시 돌려 15개 PNG 의 md5 가 모두 같음**을 확인(재현 가능).
- 개발 / 정식 같은 아이콘. 띠 · 배지 · 그림자 · 그라데이션 · 글자 없음. 도형이 512 안에서 차지하는 비율 · 위치는 원본 그대로(약 x 69–443 / 512).
- 칸 구성: 기존 `Contents.json` 의 19칸(Flutter 템플릿 = 아이폰 20/29/40/60 · 아이패드 20/29/40/76/83.5 · ios-marketing 1024)을 **그대로** 썼다. Xcode 26.2 · 배포 대상 iOS 13.0 에서 경고 없이 컴파일되고 산출물에 phone · pad · marketing 모두 들어가 고칠 필요가 없었다(Xcode 14+ 의 「1024 한 장」 방식으로 줄이지 않음 — 변경 범위 최소).

| idiom | size | scale | 파일 | 기대 px | 실제 px | hasAlpha | 결과 |
|---|---|---|---|---|---|---|---|
| iphone | 20x20 | 2x | Icon-App-20x20@2x.png | 40 | 40x40 | no | OK |
| iphone | 20x20 | 3x | Icon-App-20x20@3x.png | 60 | 60x60 | no | OK |
| iphone | 29x29 | 1x | Icon-App-29x29@1x.png | 29 | 29x29 | no | OK |
| iphone | 29x29 | 2x | Icon-App-29x29@2x.png | 58 | 58x58 | no | OK |
| iphone | 29x29 | 3x | Icon-App-29x29@3x.png | 87 | 87x87 | no | OK |
| iphone | 40x40 | 2x | Icon-App-40x40@2x.png | 80 | 80x80 | no | OK |
| iphone | 40x40 | 3x | Icon-App-40x40@3x.png | 120 | 120x120 | no | OK |
| iphone | 60x60 | 2x | Icon-App-60x60@2x.png | 120 | 120x120 | no | OK |
| iphone | 60x60 | 3x | Icon-App-60x60@3x.png | 180 | 180x180 | no | OK |
| ipad | 20x20 | 1x | Icon-App-20x20@1x.png | 20 | 20x20 | no | OK |
| ipad | 20x20 | 2x | Icon-App-20x20@2x.png | 40 | 40x40 | no | OK |
| ipad | 29x29 | 1x | Icon-App-29x29@1x.png | 29 | 29x29 | no | OK |
| ipad | 29x29 | 2x | Icon-App-29x29@2x.png | 58 | 58x58 | no | OK |
| ipad | 40x40 | 1x | Icon-App-40x40@1x.png | 40 | 40x40 | no | OK |
| ipad | 40x40 | 2x | Icon-App-40x40@2x.png | 80 | 80x80 | no | OK |
| ipad | 76x76 | 1x | Icon-App-76x76@1x.png | 76 | 76x76 | no | OK |
| ipad | 76x76 | 2x | Icon-App-76x76@2x.png | 152 | 152x152 | no | OK |
| ipad | 83.5x83.5 | 2x | Icon-App-83.5x83.5@2x.png | 167 | 167x167 | no | OK |
| ios-marketing | 1024x1024 | 1x | Icon-App-1024x1024@1x.png | 1024 | 1024x1024 | **no** | OK |

19/19 칸 파일 있음 · 크기 일치 · 알파 없음(`sips -g pixelWidth -g pixelHeight -g hasAlpha`).

## C. 개발 빌드 인자 확인

`DAY_BUNDLE_ID` · `DAY_DISPLAY_NAME` 은 `--dart-define` 이 아니라 **Xcode 빌드 설정**이다(`ios/Flutter/Identity.xcconfig` 기본값 `com.example.day.placeholder` / `DAY`). `flutter build ios` 는 Xcode 빌드 설정을 넘기는 인자가 없어서, 검증 빌드는 README 가 이미 정한 비추적 `ios/Flutter/Identity.local.xcconfig`(`.gitignore` 됨)를 **빌드 동안만** 만들고 끝나자마자 지웠다(빌드 전 없음 확인 · 빌드 뒤 삭제 확인). 소스 기본값은 그대로.

- 아카이브 경로용으로 `xcodebuild -showBuildSettings DAY_BUNDLE_ID=day.medisolveai.dev 'DAY_DISPLAY_NAME=DAY Dev'` → `PRODUCT_BUNDLE_IDENTIFIER = day.medisolveai.dev` · `DAY_DISPLAY_NAME = DAY Dev`. 인자 없이 → `com.example.day.placeholder`(기본값 그대로). 즉 **명령줄 빌드 설정만으로 dev 가 된다** — 아래 업로드 명령은 이 방식.

산출물 `build/ios/iphoneos/Runner.app`(20.7MB, `--release --no-codesign`):

| 확인 | 값 |
|---|---|
| `CFBundleIdentifier` | `day.medisolveai.dev` |
| `CFBundleDisplayName` | `DAY Dev` |
| `CFBundleName` | `DAY Dev` |
| `CFBundleIcons` / `CFBundleIcons~ipad` | `CFBundlePrimaryIcon.CFBundleIconName = AppIcon` (files `AppIcon60x60` · `AppIcon76x76`) |
| `Assets.car` | 있음(64KB). `assetutil --info` 에 AppIcon phone(29–180) · pad(20–167) · marketing 1024 |
| 번들 안 PNG | `AppIcon60x60@2x.png` · `AppIcon76x76@2x~ipad.png` |

## 업로드에 쓸 명령 — **실행하지 않음**(서명 · 업로드는 사용자 승인 뒤)

`app/` 에서. Team ID · ASC 키 값은 파일에서 읽고 화면에 내지 않는다. 서버 주소는 자리표시.

```sh
cd app
CRED=~/.config/day/apple/credentials.local.json
TEAM_ID=$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('$CRED')))['team_id'])")
ASC_KEY_ID=$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('$CRED')))['app_store_connect']['key_id'])")
ASC_ISSUER=$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('$CRED')))['app_store_connect']['issuer_id'])")

# 1) Flutter 설정만 생성(dart-define · 빌드 번호는 TestFlight 마다 올린다)
fvm flutter build ios --release --config-only --build-number=<N> \
  --dart-define=DAY_LOGIN_ENTRY=https://<dev 공개 주소> \
  --dart-define=DAY_ALLOWED_ORIGINS=https://<dev 공개 주소> \
  --dart-define=DAY_APNS_ENV=production

# 2) 서명 아카이브 — Bundle ID · 이름 · Team 은 명령줄 빌드 설정(소스에 안 씀)
xcodebuild -workspace ios/Runner.xcworkspace -scheme Runner -configuration Release \
  -destination 'generic/platform=iOS' -archivePath build/DAYDev.xcarchive \
  DAY_BUNDLE_ID=day.medisolveai.dev 'DAY_DISPLAY_NAME=DAY Dev' \
  DEVELOPMENT_TEAM="$TEAM_ID" CODE_SIGN_STYLE=Automatic \
  -allowProvisioningUpdates \
  -authenticationKeyPath ~/.appstoreconnect/private_keys/AuthKey_$ASC_KEY_ID.p8 \
  -authenticationKeyID "$ASC_KEY_ID" -authenticationKeyIssuerID "$ASC_ISSUER" \
  archive

# 3) IPA 내보내기(app-store-connect 방식 — 배포 서명이 aps-environment 를 production 으로 바꾼다)
cat > build/ExportOptions.plist <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>method</key><string>app-store-connect</string>
  <key>teamID</key><string>$TEAM_ID</string>
  <key>signingStyle</key><string>automatic</string>
  <key>destination</key><string>export</string>
</dict></plist>
PLIST
xcodebuild -exportArchive -archivePath build/DAYDev.xcarchive -exportPath build/ipa-dev \
  -exportOptionsPlist build/ExportOptions.plist -allowProvisioningUpdates \
  -authenticationKeyPath ~/.appstoreconnect/private_keys/AuthKey_$ASC_KEY_ID.p8 \
  -authenticationKeyID "$ASC_KEY_ID" -authenticationKeyIssuerID "$ASC_ISSUER"

# 4) 업로드(altool · ~/.appstoreconnect/private_keys/ 의 같은 키 — cc-prototype 와 같은 방식)
xcrun altool --upload-app -t ios -f build/ipa-dev/*.ipa \
  --apiKey "$ASC_KEY_ID" --apiIssuer "$ASC_ISSUER"
```

정식은 같은 명령에서 `DAY_BUNDLE_ID=day.medisolveai` · `DAY_DISPLAY_NAME=DAY` · 정식 dart-define(README 「빌드 설정」 예)로 바꾼다.

## 정할 것 (코디 · 사용자)

1. **App Store Connect 앱 record** `DAY Dev`(Bundle ID `day.medisolveai.dev`) 생성 — 사용자 웹 작업. 없으면 4) 업로드가 거절된다.
2. **dev 앱의 `DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS`** — 개발 앱은 dev 주소 하나로 둘지(위 예), mobile-deployment 의 「정식 앱 하나로 심사」 결정과 별개로 dev 앱 연결 규칙을 SPEC 에 적을지. 지금 SPEC 은 정식 빌드만 정의한다.
3. **ASC 키 위치**: 위 명령은 `~/.appstoreconnect/private_keys/AuthKey_<Key ID>.p8` 를 가정(day.json `upload`). 지금 키는 `~/.config/day/apple/` 에 있으니 그 폴더로 복사(600)할지, `-authenticationKeyPath` 를 credentials 의 `private_key_path` 로 둘지(altool 은 `API_PRIVATE_KEYS_DIR` env 로도 지정 가능).
4. 서버 `DAY_APNS_ALLOWED_APP_IDS` 에 `day.medisolveai.dev` 추가 — dev 앱 푸시 topic(서버 몫).
5. `IN_APP_PURCHASE` 는 Apple 기본 켜짐이라 두 Bundle ID 모두에 있다(DAY 는 쓰지 않음 · 끌 수 없는 기본값). 그대로 둔다.

## 검증

| 명령 | 결과 |
|---|---|
| `cd app && fvm flutter analyze` | No issues found! (1회) |
| `cd app && fvm flutter build ios --no-codesign --release --dart-define=DAY_LOGIN_ENTRY=https://<dev> --dart-define=DAY_ALLOWED_ORIGINS=https://<dev> --dart-define=DAY_APNS_ENV=production` (+ 임시 Identity.local.xcconfig) | ✓ Built Runner.app 20.7MB · Xcode build 54.3s (1회). 경고: 플러그인 2개(flutter_pcm_sound · flutter_tts) SPM 미지원 안내 — 기존 상태 |
| A 재조회 | 위 표 |
| B 아이콘 표 · README 재생성 md5 동일 | 19/19 OK |
| `flutter test` | 돌리지 않음(Dart 변경 없음 — 브리프 §8) |

## 계약 대조

- 서버 · 화면 계약 변경 없음. 앱 이름은 `DAY Dev` · `DAY` 만. Team ID · 서명 값 레포에 없음(M-16). 소스 기본 Bundle ID 는 placeholder 그대로.

## 이슈 · 코디가 확인할 것

- 원본 SVG path 끝(오른쪽 아래 끝, `L399.725 440.004 L400.126 439.587Z`)에 아주 작은 꺾임이 있어 1024 에서 오른쪽 아래 둥근 끝 바깥에 1–2px 짜리 각이 보인다. 「모양 그대로」라 고치지 않았다 — 디자인에서 고칠지 확인.
- 아이폰 `29x29@1x` 칸은 요즘 기기에서 안 쓰지만 템플릿 그대로 두었다(해 없음).
- 검증 빌드 산출물 `app/build/` 은 `.gitignore` 대상(커밋 안 됨).

## pending

- 서명 아카이브 · IPA · 업로드 · 앱 record · 실기기 푸시 — 이번 범위 밖(명령만 위에).
