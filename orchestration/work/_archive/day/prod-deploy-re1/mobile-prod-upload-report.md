# [mobile] 정식 DAY 배포 빌드 · App Store Connect 업로드 결과 보고

## 상태: done — 0.1.0 (1) 업로드 · ASC `processingState = VALID` · 앱 버전 0.1.0 연결 검사 통과(연결은 안 함)

- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` · `kknaksss/prod-deploy-re1` · HEAD `5f7806d3`. 진입점 **`lib/main.dart`**.
- 커밋 · push · PR · 심사 제출 · 공개 출시 · 테스터/그룹 변경 · 빌드 연결 PATCH 0. 인증서 · 기기 삭제 0.
- Team ID · Key ID · Issuer · 키 · 토큰 · 인증서 일련번호는 적지 않았다. 값은 `~/.config/day/apple/credentials.local.json` 에서 셸 변수로만 읽었다. `~/.appstoreconnect/private_keys/` 는 쓰지 않았다.

## 단계별 결과

| 단계 | 결과 |
|---|---|
| ASC 사전 조회(앱 6833456680 · bundleId `day.medisolveai` 일치 확인) | 빌드 **0개** → build-number **1**. 앱 버전 1개 `0.1.0` · `PREPARE_FOR_SUBMISSION` · 빌드 연결 없음. DAY Dev 는 조회 안 함 |
| `fvm flutter build ios --release --config-only --target=lib/main.dart --build-name=0.1.0 --build-number=1` + define 4개 | OK. `Generated.xcconfig` = `FLUTTER_TARGET=lib/main.dart` · 0.1.0 · 1 · DART_DEFINES 디코드 = `DAY_LOGIN_ENTRY=https://day.medisolveai.com` · `DAY_ALLOWED_ORIGINS=https://day.medisolveai.com,https://day-dev.medisolveai.com` · `DAY_REQUIRE_ENVIRONMENT=true` · `DAY_APNS_ENV=production`(촬영 task 의 store_capture 값 덮어씀) |
| archive(서명 없이 · `DAY_BUNDLE_ID=day.medisolveai` · `DAY_DISPLAY_NAME=DAY` · `CODE_SIGNING_ALLOWED=NO`) | **ARCHIVE SUCCEEDED**(56s · 1회) |
| archive 의 앱만 `ios/Runner/Runner.entitlements` 로 ad-hoc 서명 | OK |
| export(`app-store-connect` · automatic · `-allowProvisioningUpdates` · DAY API 키) | **EXPORT SUCCEEDED** · `DAY.ipa` 22,245,069 bytes |
| IPA 검사 | 아래 표 전부 OK |
| `altool --validate-app` | **VERIFY SUCCEEDED with no errors, 1 warning**(90068) |
| `altool --upload-app` | **UPLOAD SUCCEEDED with no errors, 1 warning**(90068) · 22,245,069 bytes · 21:24:34 KST · Delivery UUID `9c4cd151-eee6-4f50-bcdf-7207d38a50ba` |
| ASC 처리(45초 간격 조회) | 21:27:02 **VALID**(업로드 뒤 약 2.5분) |
| 빌드 연결 검사(`~/.config/day/apple/asc_link_build.py <id>` · `--apply` 없음 = dry-run) | `processingState VALID` · `expired False` · preReleaseVersion `0.1.0` · `IOS` · `app_ok True` · 현재 연결 빌드 없음 → **연결 가능**. PATCH 는 하지 않음 |

과거 5차 절차 그대로(실패한 1~4차 방식 재시도 0). 모든 단계 1회.

## 산출물 — `app/build/store-prod/`(무시 경로)

| 파일 | 값 |
|---|---|
| `ipa/DAY.ipa` | 22,245,069 bytes · sha256 `dc96e1f74779e686311b3606fc4c3ed28533d93448babfb7539e47f203ca75d1` |
| `DAY.xcarchive` | 181M(dSYM 포함) |
| 로그 | `config.log` · `archive.log` · `export.log` · `validate.log` · `upload.log` · `poll.log` · `link-dryrun.log` — validate/upload 로그에 Key ID · Issuer 문자열 0건 확인. `config.log` 에는 Flutter 가 고른 로컬 개발 서명 identity 이름이 한 줄 있다(무시 경로 · 커밋 대상 아님) |
| 조회 스크립트 | `asc_builds.py` · `asc_assets.py` · `asc_poll.py`(GET 만) |
| `ExportOptions.plist` | 권한 600 · teamID 포함(무시 경로) |

풀어 본 IPA 폴더(`unzip/`)는 검사 뒤 지웠다.

## IPA 검사

| 항목 | 값 | 판정 |
|---|---|---|
| `CFBundleIdentifier` | `day.medisolveai` | OK |
| `CFBundleDisplayName` · `CFBundleName` | `DAY` · `DAY` | OK |
| `CFBundleShortVersionString` · `CFBundleVersion` | `0.1.0` · `1` | OK |
| `ITSAppUsesNonExemptEncryption` | `false` | OK |
| `MinimumOSVersion` | `13.0` | 경고 90068(2027-04 부터 15.0 필요) |
| 아이콘 | `CFBundleIconName = AppIcon`(직전 빌드 리포트의 Assets.car 검사와 같은 소스) | OK |
| 서명 | `Apple Distribution: Medisolve AI Co., Ltd. (<가림>)` · `codesign --verify --deep --strict` 통과 · Frameworks 3개(App · Flutter · flutter_pcm_sound) 모두 배포 서명 | OK |
| entitlements | `application-identifier = <team>.day.medisolveai` · **`aps-environment = production`** · `beta-reports-active = 1` · `get-task-allow = 0` · team-identifier `<가림>` | OK |
| 프로파일 | `iOS Team Store Provisioning Profile: day.medisolveai` · AppIDName `DAY` · `aps-environment production` · ProvisionedDevices 없음(App Store) · 만료 2027-11-11 | OK |
| 서버 주소(`App.framework` strings) | `https://day.medisolveai.com` 2 · `https://day-dev.medisolveai.com` 1 · 그 밖은 Flutter 프레임워크 문자열(api.flutter.dev · docs.flutter.dev · pub.dev · github.com) | OK |
| **촬영 진입점 · fixture 혼입** | 바이트 검색(UTF-8 · UTF-16LE): 양성 대조 `로그아웃` 2 · `통역하기` 1 · `시술현황` 1 · `interpret-open` 2 · `day/push` 2 → 검색 유효. 표지 `store_capture` · `prod.day.test` · `dev.day.test` · `keepalive` · `가간호` · `나의사` · `다코디` · `오전 시술팀` · `10분 뒤에 들어갈게요` · `마취 크림을 바르고` · `療程前` · `會痛嗎` · `린 메이` · `스즈키 하나` · `LIN MEI` · `SUZUKI` · `데모 병원` 및 ASCII `FakeServer` · `FakeChat` · `FakeNotify` · `FakeSse` · `InterpDouble` · `FakePushBridge` · `MockClient` · `package:http/testing` · `test/support` **모두 0** | OK — 업로드 진행 |

## ASC 빌드 상태(업로드 뒤 GET)

| 항목 | 값 |
|---|---|
| 앱 | DAY (`day.medisolveai` · 6833456680) |
| **build resource id** | **`9c4cd151-eee6-4f50-bcdf-7207d38a50ba`** |
| 버전 · 빌드 번호 | 0.1.0 · 1 |
| `processingState` | **VALID** |
| `usesNonExemptEncryption` | **false**(Info.plist 키 · API 로 고치지 않음) |
| expired | false |
| minOsVersion | 13.0 |
| buildBetaDetail | internal `READY_FOR_BETA_TESTING` · external `READY_FOR_BETA_SUBMISSION`(외부 심사 제출 · 테스터 변경 안 함) |
| 앱 버전 0.1.0 연결 | **안 함** — dry-run 검사 통과. 코디/ASC 워커가 `asc_link_build.py 9c4cd151-eee6-4f50-bcdf-7207d38a50ba --apply` 로 연결 가능 |

## 새 서명 자산

| 종류 | 개수 | 근거 |
|---|---|---|
| App Store 배포 프로파일(`iOS Team Store Provisioning Profile: day.medisolveai`) | **1**(이번 export 가 자동 생성 · 2026-11-11 21:21:59) | 로컬 프로파일 폴더에 export 시작 뒤 새 파일 1 · IPA embedded 프로파일 생성 시각 |
| 인증서 | **0 추가로 보임** | ASC API 인증서 목록 = DEVELOPMENT 1(이전과 같음 — 클라우드 관리 배포 인증서는 API 목록에 나오지 않음) · 키체인 코드서명 identity 4 → 4 |
| 기기 · App ID 변경 | 0 | |

## 소스 변화

- `git status --short app` = `?? app/store/` · `?? app/tool/store_capture/` 뿐 — **둘 다 앞 사진 task 의 새 파일**(되돌리거나 지우지 않음). `git diff --stat -- app` = 빈 결과(추적 파일 변경 0 — lib/ · ios/ · pubspec · test/ · Info.plist · entitlements 그대로).
- `ios/Flutter/Identity.local.xcconfig` 를 쓰지 않았고 없다(Bundle ID · 이름은 xcodebuild 명령줄 설정).
- `ios/Flutter/Generated.xcconfig`(무시 파일)는 지금 `lib/main.dart` · prod define · 0.1.0 (1).
- backend/ 변경 12줄은 다른 워커 것 — 건드리지 않음.

## 경고(원문 요약)

- altool 90068: `Deployment target too low. Your app targets iOS 13.0. Starting in April 2027, iOS apps must target 15.0 or later …` — validate · upload 둘 다 1건. 지금 막지 않음.
- archive 컴파일 경고 5(플러그인 · SDK 사용 중단 안내): `AVKeyValueStatus` deprecated(video_player) · `allowBluetooth` deprecated(audio_session) · flutter_tts `Sendable` · appintents metadata 건너뜀. 앱 코드 경고 0.

## 실물 pending(이번에 확인하지 않음 · 업로드는 심사 제출 · 승인이 아님)

1. prod 서버 미배포(502) — 정식 앱 로그인 · 데모 → dev 연결 · 푸시 · 통역 실물 미확인.
2. 개인정보처리방침 · 지원 URL 페이지(502) · 앱 내부 개인정보 링크 · Soniox 고지/허가 흐름 없음(mobile-build-report 의 제출 차단 항목 그대로).
3. 심사 정보(데모 계정 · 연락처 · 메모) · App Privacy · 연령 등급 · 가격/지역 · 빌드 연결 · 스크린샷 업로드는 코디/ASC 워커 몫.
4. 업로드 뒤 Apple 메일(ITMS-91053/91061 privacy manifest 등) 여부는 사용자 메일함 확인 필요.
5. 예약현황 「곧 출시 예정」 placeholder 는 그대로 바이너리에 있다(소스 변경 금지).
6. 다음 업로드는 빌드 번호 2 이상.
