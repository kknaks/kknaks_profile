# [mobile] DAY 정식 앱 prod release 빌드 검증 결과 보고

## 상태: done — analyze · test · release(no-codesign) 빌드 통과 · 소스 변화 0 · 제출 전 미완 항목 있음(통역 동의의 보편적 필수 판정은 아래 코디 정정 참고)

- 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` · 브랜치 `kknaksss/prod-deploy-re1` · HEAD `5f7806d3`(feat: prod 첫 배포 준비 … Delivery #243).
- 시작 · 끝 모두 `git status --short app` = 빈 결과(app/ 변경 0). 워크트리의 backend/ 변경 11개는 다른 워커 것 — 건드리지 않음.
- 도구: Flutter **3.44.8**(Dart 3.12.2 · `app/.fvmrc` 고정 · fvm) · Xcode **26.2**(17C52 · SDK iphoneos26.2) · macOS 15.6.1.
- 커밋 · push · PR · 서명 · ASC 변경 · 업로드 · 심사 제출 · 실제 로그인/푸시 0. Team ID · 키 · 계정 값은 읽거나 적지 않았다.
- 자격 위치(`day.json` `apple`): `credentials` 파일 있음 · `key_files` 는 적힌 글롭으로 찾지 못함(이번 작업에 쓰지 않아 더 보지 않음). 값은 열지 않았다.

## 검증 — 명령과 결과 (각 1회)

| 명령(`app/`) | 결과 |
|---|---|
| `fvm flutter pub get` | OK(lock 그대로 · "13 packages have newer versions incompatible…" 안내만) |
| `fvm flutter analyze` | **No issues found!** (0 error · 0 warning · 0 info · 1.9s) |
| `fvm flutter test --reporter compact` | **+343 통과 · ~73 skip · 0 실패**(24s). skip 73 = 전부 `test/capture/*`(`skip: _dir == null` — `DAY_CAPTURE_DIR` 없을 때 시각 캡처 끔 · 정상) |
| `fvm flutter build ios --release --no-codesign` + 정식 identity + prod define(아래) | **✓ Built build/ios/iphoneos/Runner.app (20.7MB)** · 70s · exit 0 |

빌드 인자(버전은 pubspec `0.1.0+1` 그대로 — 바꾸지 않음):

```
--dart-define=DAY_LOGIN_ENTRY=https://day.medisolveai.com
--dart-define=DAY_ALLOWED_ORIGINS=https://day.medisolveai.com,https://day-dev.medisolveai.com
--dart-define=DAY_APNS_ENV=production
--dart-define=DAY_REQUIRE_ENVIRONMENT=true
```

정식 identity: `ios/Flutter/Identity.local.xcconfig` 가 **없음을 확인한 뒤** `DAY_BUNDLE_ID = day.medisolveai` · `DAY_DISPLAY_NAME = DAY` 두 줄로 만들고 빌드 직후 **삭제**(삭제 후 `ls` = No such file). 무시 파일(`app/ios/.gitignore:37`)이라 git 에는 처음부터 보이지 않음.

### 빌드 경고(원문)

```
Warning: Building for device with codesigning disabled. You will have to manually codesign before deploying to device.
The following plugins do not support Swift Package Manager for ios:
  - flutter_pcm_sound
  - flutter_tts
This will become an error in a future version of Flutter. Please contact the plugin maintainers to request Swift Package Manager adoption.
```

- 첫 줄은 `--no-codesign` 의 당연한 결과. 둘째는 Flutter 미래 경고(지금 빌드 · 제출 영향 없음 — CocoaPods 로 들어감).
- Xcode 컴파일 경고는 로그에 없음(flutter 는 xcodebuild 상세를 숨김 · 오류 0).
- 업로드 때 알려진 경고(직전 DAY Dev 빌드 1·2 의 altool): **90068 — 배포 대상 iOS 13.0, 2027-04 부터 15.0 필요**. 같은 설정이라 정식 앱도 같을 것(이번엔 altool 을 돌리지 않음 · 실물 미확인).

## 산출물

- 앱 번들: **`/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1/app/build/ios/iphoneos/Runner.app`**(20M · arm64 · 서명 없음 — 업로드 불가 상태 그대로)
- `App.framework/App` sha256 앞 16자 `ea0292c4b83ae20b`
- 빌드 · 테스트 로그(임시): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-prod-deploy-re1/a16a6bd4-a673-4b57-8139-6d20a0d533b2/scratchpad/{analyze,test,build}.log`
- 부산물: `app/build/ios/SourcePackages`(SPM 체크아웃) · `ios/Flutter/Generated.xcconfig`(무시 파일 — prod define 이 base64 로 들어 있음 · 다음 `flutter build/run` 이 다시 씀) · `ios/Pods` 갱신(무시 파일 · `Podfile.lock` 변화 없음).

## bundle 검증 표 — `Runner.app/Info.plist` 외

| 항목 | 값 | 판정 |
|---|---|---|
| `CFBundleIdentifier` | `day.medisolveai` | OK(정식) |
| `CFBundleDisplayName` · `CFBundleName` | `DAY` · `DAY` | OK |
| `CFBundleShortVersionString` · `CFBundleVersion` | `0.1.0` · `1` | pubspec 그대로 — 첫 제출 버전은 사용자 판단 |
| `MinimumOSVersion` | `13.0` | 직전 dev 업로드는 경고 90068로 통과. 이번 정식 빌드의 업로드 가능 여부는 미확인 |
| `UIDeviceFamily` | `[1, 2]`(iPhone · iPad) | OK — ASC 에 iPad 스크린샷도 필요 |
| `ITSAppUsesNonExemptEncryption` | `false` | OK(README 「수출 규정」 근거와 맞음) |
| 빌드 SDK | `DTSDKName iphoneos26.2` · `DTXcode 2620` | OK(최신 SDK) |
| 아이콘 | `CFBundleIcons(~ipad).CFBundlePrimaryIcon.CFBundleIconName = AppIcon` · `Assets.car` phone 8종(29–180) · pad 10종(20–167) · marketing 1024 · 번들 PNG `AppIcon60x60@2x`(120) · `AppIcon76x76@2x~ipad`(152) | OK |
| 아이콘 알파 · 크기 | 원본 15개 PNG 전부 `hasAlpha: no` · 크기 = 파일 이름과 일치(1024 포함) · Assets.car 렌더 전부 `Opaque: True` | OK |
| 런치 화면 | `UILaunchStoryboardName = LaunchScreen`(storyboardc 있음 · 이미지 비움) | OK |
| 방향 | iPhone 세로 · 가로 2 / iPad 4방향 · `UIRequiresFullScreen` 없음 | OK(iPad 멀티태스킹 조건 충족) |
| 권한 설명 | 카메라 · 사진 보관함 · 마이크 3개(한국어 문장 있음) · `PHPhotoLibraryPreventAutomaticLimitedAccessAlert = true` | OK(쓰는 기능과 일치 — 아래 「권한」) |
| 없는 키(정상) | `NSPhotoLibraryAddUsageDescription`(사진 저장 기능 없음) · `NSSpeechRecognitionUsageDescription`(기기 STT 없음) · `UIBackgroundModes` · `NSAppTransportSecurity`(ATS 예외 없음) | OK |
| entitlements | 서명 없는 빌드라 없음. 소스 `Runner.entitlements` = `aps-environment development` 하나 — 배포 서명 export 때 `production` 으로 바뀜(DAY Dev 빌드 2 IPA 에서 확인된 동작 · 정식 앱은 실물 미확인) | 서명 단계 확인 필요 |
| Frameworks | `App` · `Flutter` · `flutter_pcm_sound`(나머지 플러그인 · SPM 은 Runner 에 정적 링크) | — |

### 바이너리 안 서버 주소 · debug 혼입 (`strings App.framework/App`)

| 확인 | 결과 |
|---|---|
| `https://day.medisolveai.com` | 2회(진입점 + 허용 목록) |
| `https://day-dev.medisolveai.com` | 1회(허용 목록) |
| 그 밖 URL | `api.flutter.dev` · `docs.flutter.dev` · `pub.dev` · `github.com`(Flutter/Dart 프레임워크 오류 문자열) — 앱 서버 주소 아님 |
| `localhost` | 1회 — `lib/` 에 없음(`grep` 0). Dart SDK(dart:io) 내부 문자열 |
| `127.0.0.1` · `192.168` · `day-local` · `ngrok` · `.local` | 0 |
| `DAY_DEV_LOCAL_ORIGIN` 값 | 빌드에 주지 않음 · 코드도 release 에서 무시(`lib/core/build_config.dart:114 release: kReleaseMode`) |
| `DAY_REQUIRE_ENVIRONMENT` | `true` 로 줌 · release 는 코드상 늘 켜짐 |
| Runner 바이너리 · Info.plist 의 URL | `https://github.com`(라이브러리 문자열) 뿐 |

→ prod + dev 두 허용 origin 만 들어갔고 debug 로컬 설정 혼입 없음.

### privacy manifest · required reason API

| 위치 | manifest | 선언 내용 |
|---|---|---|
| **앱 자신(Runner)** | **없음**(`ios/Runner/PrivacyInfo.xcprivacy` 없음) | — |
| Flutter.framework | 있음 | FileTimestamp `0A2A.1 · C617.1` · SystemBootTime `35F9.1` · 추적 없음 |
| photo_manager | 있음 | 수집 `PhotosorVideos` · FileTimestamp `C617.1` |
| SDWebImage | 있음 | FileTimestamp `C617.1` |
| image_picker_ios · record_ios · url_launcher_ios · video_player_avfoundation | 있음 | API 선언 없음 · 추적 없음 |
| flutter_tts · flutter_pcm_sound · audio_session · flutter_image_compress_common | 없음 | 플러그인 iOS 소스에 required reason API 호출 0(grep) |
| **libwebp-Xcode 1.6.0 · SDWebImageWebPCoder 0.15.0**(SPM · flutter_image_compress 전이 의존) | **없음** | Apple 목록에는 SDWebImage가 명시돼 있으나 libwebp·SDWebImageWebPCoder는 이름으로 명시되지 않음. 재패키징 해당 여부는 별도 확인. 여기서는 소스로 Runner 에 정적 링크(코디 정정) |

Runner 바이너리 심볼: `stat/fstat/lstat/getattrlist/mach_absolute_time/statfs` import 0 · `NSUserDefaults` 0 · `systemUptime` 0. `attributesOfItemAtPath:` 1곳 = `AppDelegate.swift:437`(변환한 동영상 **크기** `.size` 만 읽음 — 타임스탬프 아님). `creationDate` 문자열 5 = photo_manager 의 `PHAsset.creationDate`(사진 라이브러리 속성 · 파일 타임스탬프 API 아님).

→ 앱 자체 코드는 required reason API 를 쓰지 않는 것으로 보인다. 다만 **앱 manifest 부재 · libwebp/WebPCoder manifest 부재**가 Apple 업로드 뒤 메일(ITMS-91053/91061)을 부를지는 **실물 미확인** — DAY Dev 빌드 1·2 는 같은 의존으로 altool 검증 · 처리 VALID 였으나, 업로드 뒤 Apple 메일 내용은 기록에 없다(사용자 메일함 확인 필요).

## 데이터 목록 — Apple App Privacy 작성 초안 근거(코드 기준)

앱은 DAY 서버(세션의 `api_base_url` — prod 또는 데모면 dev)만 부른다. 분석 · 광고 · crash SDK 없음(`pubspec.lock` 에 firebase · sentry · crashlytics · analytics 류 0) · `print/debugPrint/NSLog` 0 · 추적(ATT) 없음.

| 데이터 | 어디서 | 어디로 · 보관 | App Privacy 분류 초안 |
|---|---|---|---|
| 이메일 · 비밀번호 | 로그인 입력 | `POST /api/auth/login {email,password,client:"app"}`(`lib/data/day_api.dart:112`) · 기기에 저장 안 함 | 연락처 정보 › 이메일 주소 · 앱 기능 · 사용자와 연결 |
| 세션 묶음(api_base_url · environment · token · expires_at · staff_id) | 로그인 응답 · `/me` | iOS Keychain 항목 하나(`day.session` · 이 기기만 · 첫 잠금 해제 뒤) | 식별자 › 사용자 ID(staff_id) · 앱 기능 |
| 설치 id(UUID) · APNs 기기 토큰 · `platform:ios` · `app_id`(Bundle ID) · `push_env` · `kind`(phone/tablet) | 앱 생성 UUID(Keychain `day.install`) · iOS | `PUT /api/devices/{install_id}`(`lib/state/push_coordinator.dart:156`) | 식별자 › 기기 ID · 앱 기능(푸시) · 사용자와 연결 |
| 채팅 글 | 사용자 입력 | `/api/chat/*` → 서버 DB | 사용자 콘텐츠 › 기타(메시지) · 앱 기능 · 연결. **환자 정보가 들어갈 수 있음**(건강 정보 분류 여부 사용자 판단) |
| 채팅 사진 · 동영상 | 카메라(사진만) · 사진 보관함(photo_manager 목록 · image_picker) | 기기에서 줄이거나 변환(앱 임시 폴더 · 보낸 뒤 삭제 `video_pick.dart:94`) → `/api/chat/photos` · `/api/chat/videos` → 서버 파일 저장소(Blob) | 사용자 콘텐츠 › 사진 또는 비디오 · 앱 기능 · 연결 |
| 통역 음성 | 마이크(`record` · PCM 16kHz mono · 파일 저장 없음 · 스트림만) | `WS /api/interpret`(DAY 서버) → **서버가 Soniox(STT · 번역 · TTS)로 실시간 중계**(DAY-SPEC-003 §3 「통역」 · 서버 「통역 기록 없음」) | 사용자 콘텐츠 › 오디오 데이터 — **실시간 처리만 · 보관 없음**이면 Apple 정의상 「수집」에서 빠질 수 있음. Soniox 쪽 보관 · 학습 사용 여부는 **실물 미확인**(계약 · 설정 확인 필요) |
| 업무 조작(호출 · 수락 · 시술 시작/종료 · 알림 읽음 · 알림 설정) | 사용자 조작 | `/api/calls/*` · `/api/tasks/*` · `/api/visits/*` · `/api/notifications/*` · `/api/me/notification-settings` | 업무 기능 조작 — 분석용 「제품 상호작용」 아님(앱 기능 데이터). 분류는 사용자 판단 |
| 화면에 보이는 환자 정보(판 · 차트 읽기) | 서버가 내려줌 | 메모리 · 화면만(기기 저장 없음) | 앱 사용자에게서 수집하는 값 아님 |
| 빠른 말하기 TTS | `flutter_tts`(iOS 기기 음성 합성) | 기기 안 | 수집 아님 |
| 채팅 안 링크 | 메시지 글자 | `url_launcher` 외부 앱으로 열기(`chat_link.dart:10`) | 수집 아님 |

## 계정 · 로그인 흐름

- 앱에 **회원가입 · 계정 삭제 · 비밀번호 찾기 없음**(grep 0). 계정은 병원 KOS 직원 계정 — 앱 밖에서 만들어짐. 로그인(이메일 · 비밀번호) → 병원 여럿이면 병원 고르기 → `/me` 확인 뒤 Keychain 저장 → 설정 탭 [로그아웃](세션 · 기기 등록 해제).
- 가이드 5.1.1(v)(계정 삭제)은 「앱에서 계정 생성을 지원할 때」 적용 — 지금 코드엔 생성이 없음. 심사 노트에 「계정은 병원이 발급 · 앱에서 생성 없음」을 적는 것은 사용자 판단.
- 심사 계정 = 데모 계정 → prod 서버가 dev 로 연결(D-1). **prod 서버에 D-1 · 데모 env 가 배포돼 있어야 심사관 로그인이 됨**(서버 · 코디 몫 · 이번에 확인 안 함).

## 권한 사용(코드 근거)

| 권한 | 쓰는 곳 | 비고 |
|---|---|---|
| 카메라 | 채팅 사진 찍기(`photo_pick.dart:42` `ImageSource.camera`) | 동영상 촬영 없음 |
| 사진 보관함 | 채팅 최근 사진 목록 · 고르기 · 제한 접근 추가(`photo_pick.dart:179–212` photo_manager) | 쓰기(저장) 없음 → Add 권한 키 없음 정상 |
| 마이크 | 통역(`audio_io.dart:64` `record.startStream` · `interpret_controller.dart:135` 권한 확인) | 권한 문장은 「의료진과 고객의 말을 듣기 위해」 — **외부(서버 · Soniox) 전달은 문장에 없음** |
| 알림 | 원장 호출 · 채팅 푸시(`day/push` 채널) | Info.plist 키 불필요 |

## 코디 추가 확인(msg_2330558b8c3c) — 개인정보 링크 · 통역 외부 전달 고지

코드 근거로 **둘 다 없음**(소스 수정 안 함):

1. **앱 안 개인정보처리방침 링크 없음** — `lib/` 전체에 `개인정보` · `privacy` · `약관` · `terms` 0. 로그인 화면 · 설정 탭(`lib/ui/shell.dart:418` 「이름 · 병원 · [로그아웃]만」 · 알림 칸) 어디에도 링크 없음. → 5.1.1(i) 충족 안 됨.
2. **Soniox 외부 전달 안내 · 허가 흐름 없음** — `soniox` · `동의` · `consent` · `외부` · `제3자` 0. 통역 드로어를 열면(`interpret_controller.dart:110 openDrawer` → `_start`) **마이크 권한 확인 → 바로 `WS /api/interpret` 연결**. 고지 화면 · 동의 저장 · 첫 사용 확인 없음. 마이크 권한 문장도 외부 전달을 말하지 않음. → 개인정보가 실제 공유되는 경우의 5.1.2(i) 조건 확인 필요. 통역이라는 이유만으로 개인정보 포함·동의 팝업 필수를 단정하지 않는다(코디 정정).

최소 변경안(보고만 · 글자는 SPEC 원천이 필요 — 앱 규칙 「원천 글자만」):
- (a) 개인정보처리방침 URL 을 빌드 설정 `--dart-define=DAY_PRIVACY_URL`(이름 제안)로 받고, 로그인 화면 아래 · 설정 탭에 링크 1줄(`url_launcher` 이미 의존 · 외부 브라우저). URL 없으면 release 에서 숨기지 말고 빌드 실패/경고로 드러내는 편이 안전.
- (b) 통역 드로어 첫 사용 때 고지 시트 1개: 「말한 음성이 DAY 서버를 거쳐 음성 인식 · 번역 업체(Soniox)로 전달됨」(보관 기간·학습 사용은 공급자 정책을 확인한 뒤 실제 내용으로 고지) + [동의] / [취소]. 동의 상태는 Keychain(기존 `SessionKeychain` 방식 · UserDefaults 를 쓰면 required reason `CA92.1` manifest 필요) 또는 서버 `/me` 칸. 거절이면 연결하지 않음.
- (c) `NSMicrophoneUsageDescription` 에 「통역 업체로 전달」 한 구절 추가.
- 세 가지 모두 DAY-SPEC-003(통역 · 설정) 개정 → 앱 구현 → 재빌드 순서. 서버 동의 기록이 필요한지는 사용자 판단.

## 소스 변화

**없음.** `git status --short app` = 빈 결과 · `git diff --stat -- app` = 빈 결과(마지막 확인). 생성물은 `app/build/` 와 무시 파일(`ios/Flutter/Generated.xcconfig` · `ios/Pods` · `.dart_tool`)뿐. 임시 `Identity.local.xcconfig` 는 만들고 지움.

## 제출 전 예약 탭 처리 필요(코디 추가)

예약현황 탭이 `lib/ui/shell.dart`에서 자리표시 화면을 열고 `lib/core/copy.dart:62`의 ‘곧 출시 예정’을 표시한다. 정식 제출 전에 탭을 숨길지 기능을 완성할지 결정해야 한다. Apple 심사 가이드 2.1의 완성도 기준과 Unlisted의 정식 배포 준비 조건에 맞춰 확인한다. 이번에는 소스 변경 없이 누락 사항으로 기록했다. `mobile-submission-draft.md`에도 같은 항목을 기록했다.

## 제출을 막는 항목 (확인됨)

1. **앱 안 개인정보처리방침 링크 없음**(5.1.1(i)) — 소스 변경 필요 · 위 (a). ASC 의 Privacy Policy URL 도 필요(사용자 답변: 미정).
2. **통역 외부 전달 안내·별도 허가 흐름 없음은 코드 관찰 사실**. 다만 모든 단순 통역에 별도 동의 팝업이 반드시 필요하다고 단정한 판정은 철회. 실제 개인정보 공유가 있다면 5.1.2(i) 적용 조건을 확인한다. 동의 팝업·권한 문구를 이번 작업에서 임의 변경하지 않는다(사용자 지적 반영).
3. **App Store Connect 정식 「DAY」 앱 record 생성 여부 미확인** — 사용자 담당(mobile-deployment §1-1). 이번에는 ASC 조회를 하지 않았다(코디 정정).
4. **배포 서명 방법 미정**(M-16) — 지금 빌드는 서명 없음. DAY Dev 에서 쓴 우회(서명 없는 archive → ad-hoc entitlements → 자동 export)는 저장소 문서에 없음. 사용자 결정.
5. **prod 서버 준비**(코디 몫) — D-1 데모 → dev 연결 · 데모 env · prod APNs 설정 · M-20(dev 서버 APNs 허용 앱에 `day.medisolveai` 추가). 없으면 심사관 로그인 · 데모 푸시 실패.
6. **ASC 메타데이터**(사용자) — App Privacy 설문(위 데이터 표 근거) · iPhone + iPad 스크린샷 · 심사 노트(데모 계정 · 「데모는 테스트 데이터로 같은 기능」) · 연령 등급 등. Unlisted 는 정식 배포 준비를 끝내 심사에 제출한 뒤 별도 신청한다. 심사 통과·공개 출시까지 기다릴 필요는 없다(Apple 공식 Unlisted 안내 · 코디 정정).

7. **예약현황 탭 자리표시** — 정식 제출 전에 숨기거나 기능을 완성할지 결정 · 위 코디 추가 항목 참조.

## 실물 미확인 (이번 범위 밖 · 막는지 모름)

- 정식 번들로 서명 · export 한 IPA 의 entitlements(`aps-environment = production`) · 프로파일 — 서명 금지라 확인 못 함.
- altool 검증 · 업로드 결과(90068 외 경고 유무) · 업로드 뒤 Apple 메일(ITMS-91053 앱 manifest · ITMS-91061 libwebp/SDWebImageWebPCoder manifest).
- Soniox 의 음성 · 문장 보관 · 학습 사용 여부(App Privacy 「수집」 판단 근거).
- 실기기 prod 로그인 · 데모 → dev 연결 · 푸시 도착 · 통역(이번엔 하지 않기로 함).
- 버전 `0.1.0 (1)` 을 첫 정식 제출 버전으로 쓸지(사용자 판단 · 바꾸지 않음).

## 주의(막지 않음)

- 최소 iOS 13.0 → 2027-04 전 15.0 이상 필요(경고 90068 · M-7).
- flutter_pcm_sound · flutter_tts 의 SPM 미지원 — 미래 Flutter 에서 오류 예정.
- 앱 자체 `PrivacyInfo.xcprivacy` 추가(추적 false · 수집 유형 선언)는 막는 항목이 아니어도 위 (b) 에서 UserDefaults 를 쓰면 함께 필요.

## 사용자 지적 반영 정정

단순 대화 통역이라는 기능만으로 음성에 개인정보가 포함된다고 단정할 수 없다. 위 외부 전달/별도 허가 단계 부재는 코드 관찰이고, 이를 무조건적인 심사 차단으로 분류한 초기 판단은 철회한다. 별도 동의 팝업 추가 지시도 하지 않았다. 현재 권한 문구는 한국어 원문 그대로다. 최신 제출 자료 원천은 mediness products/day/60-release/app-store-preparation.md.
