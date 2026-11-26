# DAY Dev 0.3.0 빌드 · 업로드 결과 보고 — iOS TestFlight 빌드 5 · Android internal vc5

## 상태: done — 둘 다 올라감 · TestFlight `0.3.0 (5)` VALID · 내부 `IN_BETA_TESTING` · Play internal `5 (0.3.0)` completed

- 빌드 커밋: `git fetch origin && git checkout --detach origin/dev` = **`a76496c4`**(#296 카메라 문구 · 부모 `8fe0095a` = #295). `app/ios/Runner/Info.plist` 에 「고객 여권의 정보면을 읽기 위해」 있음 확인 후 빌드. 소스 수정 0 · 커밋 0.
- 정식 앱(`day.medisolveai`) 빌드 · 업로드 0. 테스터 · 그룹 · 심사 제출 0. 사용자 기기 · 시뮬레이터 · 로컬 스택(11040) · 실행 중 `flutter run` 무접촉.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰은 적지 않았다(셸 변수로만 · altool 출력은 가려서 저장).

## iOS — DAY Dev `day.medisolveai.dev` 0.3.0 (5)

절차 = 지난 업로드와 같음(config-only → 서명 없이 archive → 앱만 `Runner.entitlements` ad-hoc 서명 → export 자동 서명 → validate → upload). 임시 파일 · 로그는 `app/build/tf5/`(무시 폴더).

| 단계 | 결과 |
|---|---|
| config(`--build-name=0.3.0 --build-number=5` + `DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = `https://day-dev.medisolveai.com` · `DAY_APNS_ENV=production`) | OK |
| archive(`DAY_BUNDLE_ID=day.medisolveai.dev` · `DAY_DISPLAY_NAME=DAY Dev` · `CODE_SIGNING_ALLOWED=NO`) | **ARCHIVE SUCCEEDED** · 경고만(아래) |
| ad-hoc entitlements 서명 | OK |
| export(app-store-connect · 자동 · `-allowProvisioningUpdates` · DAY API 키) | **EXPORT SUCCEEDED** · IPA 22,609,614 bytes |
| `altool --validate-app` | **VERIFY SUCCEEDED** · 오류 0 · 경고 2 |
| `altool --upload-app` | **UPLOAD SUCCEEDED** · 22,609,614 bytes · 20:20 KST |
| ASC 처리(20:26 조회) | **VALID** |

### archive 경고 전문(막지 않음 · 플러그인 · 도구 쪽)
- `appintentsmetadataprocessor … warning: Metadata extraction skipped. No AppIntents.framework dependency found.`
- `video_player_avfoundation-2.12.1/…/FVPAVFactory.h:38:4: warning: 'AVKeyValueStatus' is deprecated: first deprecated in iOS 16.0 - Use AVAsyncProperty.Status instead`
- `flutter_tts-4.2.5/ios/Classes/SwiftFlutterTtsPlugin.swift:10:7: warning: stored property 'synthesizer' of 'Sendable'-conforming class 'SwiftFlutterTtsPlugin' has non-Sendable type 'AVSpeechSynthesizer'`
- `flutter_tts-4.2.5/ios/Classes/AudioCategoryOptions.swift:25:15: warning: 'allowBluetooth' was deprecated in iOS 8.0: renamed to 'AVAudioSession.CategoryOptions.allowBluetoothHFP'`
- config 단계: `The following plugins do not support Swift Package Manager for ios: flutter_pcm_sound, flutter_tts`
- 여권 스캔(Vision) 관련 경고 · 오류 0.

### validate · upload 경고 전문(지난 빌드와 같은 2개)
- **90068** `Deployment target too low. Your app targets iOS 13.0. Starting in April 2027, iOS apps must target 15.0 or later to be uploaded to App Store Connect or submitted for distribution.`
- **90725** `SDK version issue. This app was built with the iOS 26.2 SDK. Starting April 2027, iOS and iPadOS apps must be built with the iOS 27 SDK or later, included in Xcode 27 or later, in order to be uploaded to App Store Connect or submitted for distribution.`

### IPA 확인
| 항목 | 값 | 결과 |
|---|---|---|
| `CFBundleIdentifier` · `CFBundleDisplayName` | `day.medisolveai.dev` · `DAY Dev` | OK |
| `CFBundleShortVersionString` · `CFBundleVersion` | `0.3.0` · `5` | OK |
| `ITSAppUsesNonExemptEncryption` | `false` | OK |
| `NSCameraUsageDescription` | 「채팅으로 보낼 사진과 차트에 올릴 시술 전후 사진을 찍고, 고객 여권의 정보면을 읽기 위해 카메라를 사용합니다. 찍은 사진은 사진첩에 저장하지 않습니다.」 | OK |
| 여권 스캔 네이티브 | `Runner` 가 `Vision.framework` · `AVFoundation.framework` 링크 | OK |
| 아이콘 | `AppIcon60x60@2x.png` · `AppIcon76x76@2x~ipad.png` · `Assets.car` | OK |
| entitlements | `aps-environment = production` · `beta-reports-active = true` · `get-task-allow = false` · application-identifier · team-identifier | OK |
| 서명 | `Apple Distribution: Medisolve AI Co., Ltd. (<가림>)` · `codesign --verify --deep --strict` 통과 · Frameworks(App · Flutter · flutter_pcm_sound) | OK |
| 프로파일 | `iOS Team Store Provisioning Profile: day.medisolveai.dev` | OK |
| 서버 주소(`App.framework`) | `https://day-dev.medisolveai.com` 만 + `https://day.medisolveai.com/privacy`(개인정보 처리방침 고정 링크 · 지난 빌드와 같음) · 그 밖은 flutter 문서 · pub.dev 링크 | OK |

### ASC 빌드 상태(DAY Dev)
| 버전 (빌드) | processingState | usesNonExemptEncryption | 내부 | 외부 |
|---|---|---|---|---|
| **0.3.0 (5)** | **VALID** | false | **IN_BETA_TESTING** | READY_FOR_BETA_SUBMISSION(제출 안 함) |
| 0.2.0 (4) | VALID | false | IN_BETA_TESTING | 〃 |

- 수출 규정 누락 없음 → 기존 내부 테스터는 바로 받을 수 있다(그룹 · 테스터 손대지 않음).
- 새 서명 자산: 프로비저닝 프로파일 폴더 새 파일 0 · 기존 클라우드 배포 인증서 · App Store 프로파일 재사용.

## Android — DAY Dev `day.medisolveai.dev` 0.3.0 (versionCode 5)

| 단계 | 결과 |
|---|---|
| `google-services.json` 복사 → 빌드 → 지움 | OK |
| `flutter build appbundle --release --build-name 0.3.0 --build-number 5` + `DAY_APPLICATION_ID=day.medisolveai.dev` · `DAY_APP_NAME=DAY Dev` · `DAY_UPLOAD_KEY_PROPERTIES` · dev dart-define 2개 | ✓ 72.3MB(지난 55.7MB → ML Kit OCR 번들 포함으로 증가) |
| 사본 `~/.config/day/android/out/DAY-Dev-0.3.0-5.aab`(600) | sha256 `1218f13eecf9a1ed1cb44d392ae32410a1e6fc78bde4d2e3ab4b4fd6ea3bb6c1` |
| `play_upload.py … --expect-version-code 5 --release-name '5 (0.3.0)' --dry-run` | bundles.upload vc 5 · tracks.update · **edits.validate ok** · edit 삭제 |
| 같은 명령 실제 | **edits.commit ok** → `internal: name='5 (0.3.0)' versionCodes=['5'] status=completed` · 20:26 KST |

출시 노트(ko-KR · 원천 = PR #295 제목): 「0.3.0 — 차트 웹 기능 · 예약현황 탭 · 문진 QR · 여권 스캔 · 태블릿에 보내기」.

### 빌드 경고 전문(막지 않음)
- `WARNING: Your app uses the following plugins that apply Kotlin Gradle Plugin (KGP): flutter_image_compress_common, flutter_tts, photo_manager — Future versions of Flutter will fail to build if your app uses plugins that apply KGP.`
- `Warning: SDK processing. This version only understands SDK XML versions up to 3 but an SDK XML file of version 4 was encountered.`(Android Studio · cmdline-tools 버전 차이)
- CameraX · ML Kit 관련 경고 · 오류 0.

### AAB 확인
| 항목 | 값 | 결과 |
|---|---|---|
| package · versionCode · versionName | `day.medisolveai.dev` · 5 · `0.3.0` | OK |
| Firebase | `google_app_id` 리소스 있음 · **dev 앱 id 있음 · 정식 앱 id 없음**(google-services.json 과 대조 · 값 미출력) | OK |
| CAMERA | `android.permission.CAMERA` · `uses-feature android.hardware.camera.any required=false` | OK |
| 여권 스캔 네이티브 | `day.medisolveai.PassportScanActivity` · ML Kit text(`TextRegistrar` · `MlKitInitProvider`) · 번들 so `libmlkit_google_ocr_pipeline.so` · CameraX `libimage_processing_util_jni.so` · `libsurface_util_jni.so` | OK |
| 푸시 | `DayMessagingService` · `AcceptReceiver` · `POST_NOTIFICATIONS` | OK |
| 그 밖 권한 | INTERNET · ACCESS_NETWORK_STATE · RECORD_AUDIO · READ_MEDIA_IMAGES/VIDEO/VISUAL_USER_SELECTED · READ_EXTERNAL_STORAGE · WAKE_LOCK · BIND_JOB_SERVICE · DUMP(= androidx profileinstaller 수신기 보호 속성 · 앱 요청 권한 아님) | 참고 |
| 서버 주소(`libapp.so`) | `https://day-dev.medisolveai.com` 만(+ 개인정보 처리방침 고정 링크 · pub.dev) | OK |
| 서명 | `jar verified` · SHA-256 `92:75:54:AE:…:F9:A9:69:AD` = 업로드 키(지난 빌드와 같음) | OK |

## 정리 · git
- `app/android/app/google-services.json` 지움 · 풀어 본 IPA · AAB 폴더 지움(산출물 · 로그는 `app/build/tf5/` 무시 폴더).
- 워크트리를 `kknaksss/app-camera-copy-re1` 로 되돌림:
```
On branch kknaksss/app-camera-copy-re1
Your branch is up to date with 'origin/kknaksss/app-camera-copy-re1'.

nothing to commit, working tree clean
```

## 다음
- 실기기 확인: TestFlight DAY Dev 0.3.0 (5) · Play 내부 테스트 5 (0.3.0) — 여권 스캔(iOS Vision · Android ML Kit) 실물 동작.
- 테스터 그룹 · 심사 제출은 코디 몫(손대지 않음).
- 2027-04 전: iOS 배포 대상 15.0 · Xcode 27(90068 · 90725) · KGP 플러그인 3개 갱신.
