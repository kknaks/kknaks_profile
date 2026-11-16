# [mobile] 정식 DAY 0.1.0 (2) 업로드 · 버전 연결 결과 보고

## 상태: done — 0.1.0 (2) 업로드 · `VALID` · App Store 버전 0.1.0 에 빌드 2 연결(빌드 1 대체) · 내부 그룹에 들어 있음

- 워크트리 `CENTURION_DAY/prod-deploy-re1` · `kknaksss/prod-deploy-re1` · HEAD **`79e730b5`** — `git diff 79e730b5 382827d5` 빈 결과(dev 머지와 같은 tree) · tracked 변경 0(미추적 `app/store/` · `app/tool/store_capture/` 만 · 손대지 않음). 진입점 **`lib/main.dart`**.
- 소스 수정 · 커밋 · push 0 · 심사 제출 0 · 메타데이터 변경 0 · 외부 테스터 0 · 그룹 생성 0 · 그룹에 빌드 POST 0.
- Key ID · Issuer · Team ID · 키 · 토큰은 출력하지 않음(validate/upload 로그에 Key ID · Issuer 문자열 0건 확인).

## 단계별 결과

| 단계 | 결과 |
|---|---|
| ASC 사전 조회(앱 6833456680 · bundleId `day.medisolveai` 일치) | 빌드 1개 0.1.0 (1) `9c4cd151…` VALID → **build-number 2**. 같은 때 betaGroups 조회 = **0개** |
| config `--target=lib/main.dart --build-name=0.1.0 --build-number=2` + define 4 | OK · `Generated.xcconfig` 디코드 = `DAY_LOGIN_ENTRY=https://day.medisolveai.com` · `DAY_ALLOWED_ORIGINS=https://day.medisolveai.com,https://day-dev.medisolveai.com` · `DAY_REQUIRE_ENVIRONMENT=true` · `DAY_APNS_ENV=production` |
| archive(서명 없이 · `DAY_BUNDLE_ID=day.medisolveai` · `DAY_DISPLAY_NAME=DAY` · `CODE_SIGNING_ALLOWED=NO`) | **ARCHIVE SUCCEEDED**(1회) |
| 앱만 `Runner.entitlements` ad-hoc | OK |
| export(빌드 1 의 `ExportOptions.plist` 복사 · app-store-connect · automatic · `-allowProvisioningUpdates`) | **EXPORT SUCCEEDED** · `DAY.ipa` **22,247,103 bytes** · sha256 `c1f84f1edf238e1eb44e02c67688cdc42bf2d31dcc889e4de1d063b99dc44944` |
| `altool --validate-app` | **VERIFY SUCCEEDED** · 오류 0 · 경고 1(90068) |
| `altool --upload-app` | **UPLOAD SUCCEEDED** · 22,247,103 bytes · **13:19:24 KST** · Delivery UUID `21071da9-aa6f-44ec-924f-219400ac0d58` |
| ASC 처리 | **13:22:42 KST VALID**(약 3분) |
| 버전 연결 `~/.config/day/apple/asc_link_build.py 21071da9-… ` dry-run → `--apply` | 검사 통과(VALID · not expired · 0.1.0 · IOS · app_ok) · 이전 연결 `9c4cd151…`(빌드 1) → **readback `21071da9…`(빌드 2)** |

## IPA 확인 — `app/build/store-prod-2/ipa/DAY.ipa`

| 항목 | 값 | 판정 |
|---|---|---|
| `CFBundleIdentifier` | `day.medisolveai` | OK |
| `CFBundleDisplayName` · `CFBundleName` | `DAY` · `DAY` | OK |
| `CFBundleShortVersionString` · `CFBundleVersion` | `0.1.0` · `2` | OK |
| `ITSAppUsesNonExemptEncryption` | `false` | OK |
| `MinimumOSVersion` | 13.0 | 경고 90068 |
| 아이콘 | `CFBundleIconName = AppIcon` · Assets.car AppIcon phone 29–180 · pad 20–167 · marketing 1024 | OK |
| 서명 | `Apple Distribution: Medisolve AI Co., Ltd. (<가림>)` · `codesign --verify --deep --strict` 통과 · Frameworks 3개 모두 배포 서명 | OK |
| entitlements | `<team>.day.medisolveai` · **`aps-environment = production`** · `beta-reports-active = true` · `get-task-allow = false` | OK |
| 프로파일 | `iOS Team Store Provisioning Profile: day.medisolveai` · AppIDName `DAY` · aps production · ProvisionedDevices 없음 · 생성 2026-11-11 21:21:59(빌드 1 것 재사용) · 만료 2027-11-11 | OK |
| 주소(`App.framework` strings) | `https://day.medisolveai.com` 2 · `https://day-dev.medisolveai.com` 1 · `https://day.medisolveai.com/privacy` 1(A2 설정 「정보」 링크) | OK |
| 촬영 진입점 · fixture 혼입(UTF-8 · UTF-16LE 바이트 검색) | 양성 대조: `로그아웃` 2 · `통역하기` 1 · `시술현황` 1 · `interpret-open` 1 · `day/push` 1 · `개인정보 처리 안내` 1 · `정보` 3. 빌드 1 과 같은 표지 26개(`store_capture` · `prod.day.test` · `dev.day.test` · `keepalive` · 가짜 인물 · 대화 · `FakeServer` · `MockClient` · `test/support` 등) **모두 0** | OK |

## ASC 상태(끝)

| 항목 | 값 |
|---|---|
| 빌드 2 id | **`21071da9-aa6f-44ec-924f-219400ac0d58`** · VALID · expired false |
| `usesNonExemptEncryption` | **false** 확인(API 로 고치지 않음) |
| App Store 버전 0.1.0 | `PREPARE_FOR_SUBMISSION` · 연결 빌드 = **빌드 2** |
| 빌드 2 internal / external | **IN_BETA_TESTING** / READY_FOR_BETA_SUBMISSION(외부 제출 안 함) |

## TestFlight 내부 그룹 — 주의

- 작업 시작 사전 조회(업로드 전) 때 정식 앱 betaGroups = **0개**.
- 끝 조회(13:23 쯤) 때 내부 그룹 **`medisolveai`**(`876f34d9-…` · `isInternalGroup = true` · `hasAccessToAllBuilds = true` · 테스터 1) 가 **있었다** — 그 사이 다른 쪽(사용자 · 코디 · ASC 워커)이 만든 것으로 보인다. 이 워커는 만들지 않았다.
- 그 그룹은 「모든 빌드 접근」이라 빌드 2 · 빌드 1 이 **이미 그룹 빌드 목록에 들어 있다**. 그래서 빌드 넣기 POST 는 하지 않았다(할 필요 없음). 빌드 2 내부 상태 `IN_BETA_TESTING` → 그룹 테스터가 TestFlight 에서 받을 수 있음.

## 새 서명 자산
0 — 프로파일 폴더에 이번 작업 뒤 새 파일 0 · IPA 프로파일은 빌드 1 때 만든 것.

## 산출물 — `app/build/store-prod-2/`(무시 경로)
`config.log` · `archive.log` · `export.log` · `validate.log` · `upload.log` · `link-dryrun.log` · `link-apply.log` · `ExportOptions.plist`(600 · teamID) · `DAY.xcarchive` · `ipa/DAY.ipa` · `profile.plist`. 풀어 본 IPA 는 지움.

## git status (끝)
```
?? app/store/
?? app/tool/store_capture/
```
HEAD `79e730b5` 그대로. `ios/Flutter/Generated.xcconfig`(무시 파일) = `lib/main.dart` · prod define · 0.1.0 (2).

## 미결 · 주의
1. 경고 90068(iOS 13.0 → 2027-04 전 15.0).
2. 다음 정식 업로드는 빌드 번호 3 이상.
3. 내부 그룹 `medisolveai` 는 이번 작업 중 생겼다 — 누가 만들었는지 코디 확인. day.json `apple.state` 갱신(빌드 2 · 연결)은 코디 몫.
