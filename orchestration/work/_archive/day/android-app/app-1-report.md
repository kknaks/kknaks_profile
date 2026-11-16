# android-app AND-1~4 결과 보고 — Android 개발 앱 1판

## 상태: done — A5 음성 입력(말하기 → 자막 → 번역 음성)만 Play 내부 테스트 실기기(A6)로 넘김(사용자 결정 2026-11-13 · 호스트 마이크 사유)

워크트리 `CENTURION_DAY/android-app` · 브랜치 `kknaksss/android-app`(base `origin/dev` 0106654e) · 커밋 · push 없음.

## 수행 — 변경 파일

| 파일 | 무엇 |
|---|---|
| `app/android/**`(새로) | `flutter create --platforms android --org day.medisolveai`(fvm 3.44.8 · 임시 폴더에서 만들어 `android/` 만 복사 — ios/ · lib/ · test/ 덮어쓰기 없음) |
| `app/android/app/build.gradle.kts` | namespace `day.medisolveai` · applicationId · 앱 이름 = 빌드 값(아래 「id 주입」) · minSdk 24 · targetSdk 36 · compileSdk 36 |
| `app/android/build.gradle.kts` | `flutter_pcm_sound` 모듈만 compileSdk 36 으로(그 플러그인 33 · 의존 exifinterface 1.4.1 이 34+ 요구 → checkAarMetadata 실패) |
| `app/android/identity.properties` | 임시 기본값 `com.example.day.placeholder` · `DAY`(iOS `Identity.xcconfig` 와 같은 값) |
| `app/android/.gitignore` | 생성물 + `/identity.local.properties` |
| `app/android/app/src/main/AndroidManifest.xml` | 권한 · 백업 제외 · queries(TTS_SERVICE · https VIEW) · `@string/app_name` |
| `app/android/app/src/main/res/xml/data_extraction_rules.xml` | 클라우드 백업 · 기기 이전 모두 제외 |
| `app/android/app/src/main/kotlin/day/medisolveai/{MainActivity,SessionChannel,PushChannel,VideoChannel}.kt` | 채널 3개 |
| `app/android/app/src/main/res/mipmap-*/ic_launcher.png` | `assets/brand/app-icon.svg` 에서 만든 48~192px(README 「앱 아이콘」 과 같은 resvg 방식 · 알파 없음) |
| `app/.metadata` | `platform: android` 줄 추가(flutter create 산물) |
| `app/README.md` | 「Android(개발 앱 · 로컬 에뮬레이터)」 절 **추가만**(기존 줄 수정 0) |

`app/lib/**` · `app/ios/**` · `app/test/**` 변경 0. Dart 변경 0 — 코디 질문 필요한 자리 없었다.

## 채널 대조표 (`grep -rn "MethodChannel(" app/lib` = 3개 — video_pick.dart:22 · session_store.dart:79 · push_bridge.dart:35)

| 채널 · 메서드 | iOS `AppDelegate.swift` | Android Kotlin | 같음/다름 |
|---|---|---|---|
| 등록 | :45-54 `registrar(forPlugin:)` | `MainActivity.kt` `configureFlutterEngine` | 같음(이름 그대로) |
| session `load` | :159-160 → `SessionKeychain.loadRaw` :196 · :230 | `SessionChannel.kt:31` → `SessionStore.loadRaw` :71 | 같음 — JSON 문자열 · 없으면 null(복호화 실패도 null) |
| session `save` | :161-166 · 실패 `keychain_save_failed` · :216 update-or-add | `:32-41` · 같은 오류 코드 · `:80` `commit()` 한 번에 통째 | 같음 |
| session `clear` | :167-169 · :239 | `:42` · `:86` | 같음 |
| session `clearIf` | :170-176 · :208-214 `queue.sync{ storedMatches → clearLocked }` · AcceptLogic.swift:127 | `:43-51` · `:91-95` · `storedMatches` `:140`(JSON 의 token · api_base_url 두 칸만) | 같음 — 인자 틀리면 지우지 않고 null |
| 직렬화 | :188 `DispatchQueue("day.session.keychain")` + 모든 접근 `queue.sync` | `:134` 프로세스 하나의 `newSingleThreadExecutor` — load · save · clear · clearIf 전부 그 줄로 · 결과만 메인 스레드 | 같음 |
| push `ready` | :59-66 pendingTap · pendingToken | `PushChannel.kt:22` null | 스텁 |
| push `requestPermission` | :67-74 OS 권한 | `:23` false | 스텁 |
| push `register` | :75-83 | `:24` null(onToken 안 부름) | 스텁 |
| push `installId` | :84-85 · :246-274 Keychain uuid 소문자 | `:25` · `:33` 앱 전용 prefs `day.install` uuid 소문자 · 로그아웃해도 유지 | 같음(앱 삭제 시 새 값 — iOS Keychain 은 남을 수 있음) |
| push `appId` · `appName` | :86-89 bundleIdentifier · CFBundleDisplayName | `:26-27` packageName · application label | 같음 — 실기 확인 `day.medisolveai.dev` · `DAY Dev`(마이크 권한 창 「Allow DAY Dev…」) |
| push 역방향 onToken · onTap · onForeground | :65 · :98 · :119 · :124 · :146 | 부르지 않음 | 스텁 |
| video `audioSave` · `audioRestore` | :364-367 · :375-381 | `VideoChannel.kt:16` null | 스텁(Android 무음 스위치 없음) |
| video `audioFollowSilent` | :368-374 Bool | `:17` false | 스텁 |
| video `probe` | :391-396 `{durationMs}` | `:18` null | 스텁 — Dart `durationMs` = null(길이 검사는 변환 뒤 값) |
| video `convert` | :397-398 · 실패 `convert_failed` | `:19` `convert_failed`(message `android_stub`) | 스텁 — Dart `convert` catch → null → 「동영상을 보내지 못했어요」(SPEC-004 U-6 기존 문구) |
| 알림 [수락] | :133-142 · :287-339 | 없음 | 범위 밖(푸시 스텁 — 알림이 안 옴) |

Dart 가 실패를 삼키는지: `video_pick.dart` 의 probe · convert · audio* 는 모두 try/catch(→ null · 무시). `push_coordinator.dart` 는 ready · requestPermission · register · appId · installId 모두 try/catch. `session_store.dart` 는 save 실패(PlatformException)만 위로 — 로그인 화면 `keychain_save_failed`(iOS 와 같은 길).

## 세션 저장 방식 (스펙 mobile-deployment §7-2 [제안] 「Android Keystore 로 보호되는 암호화 저장소」를 따름)

- **AES-256-GCM** · 키 = **Android Keystore**(`AndroidKeyStore` · alias `day.session.key` · 기기 밖으로 못 꺼냄) · 무작위 IV · 암호문 `base64(iv):base64(ct)` 를 앱 전용 SharedPreferences `day.session` 의 값 하나에 `commit()`.
- 왜 Jetpack `EncryptedSharedPreferences` 가 아닌가: `androidx.security:security-crypto` 는 deprecated(1.1.0 · 2025) — 새 의존 없이 플랫폼 API 만으로 같은 구조(Keystore 키로 암호화한 prefs)를 직접 쓴다. 코드가 80줄 남짓이라 대조 · 검토가 쉽다.
- 이 기기에서만: `allowBackup=false` · `fullBackupContent=false` · `dataExtractionRules` 로 클라우드 백업 · 기기 이전 모두 제외(iOS `ThisDeviceOnly`). 키도 Keystore 밖으로 안 나가 암호문만 옮겨져도 못 읽는다(→ load null → 로그인 화면).
- 사용자 인증(지문 등) 요구 없음 — credential-encrypted 저장소라 부팅 뒤 첫 잠금 해제 이후 읽힘(iOS `AfterFirstUnlock` 자리). Android 는 알림 [수락]이 없어 잠금 화면 읽기는 필요 없다.
- 실기 확인: 로그인 뒤 `run-as … cat shared_prefs/day.session.xml` — 평문 칸(api_base_url · staff_id · expires_at · https://) **없음** · 값 모양 `iv:ct` 확인(값은 출력하지 않음).

## id 주입 방식 (스펙 미정 자리 — iOS 방식에 맞춤)

iOS = 소스 기본값(`Identity.xcconfig` placeholder) + 명령줄 빌드 설정 > `Identity.local.xcconfig`(커밋 안 함). Android 도 같은 3단:
`-P`(`--android-project-arg=DAY_APPLICATION_ID=…` · `DAY_APP_NAME=…` — `flutter run` · `build apk` 둘 다 받음) > `android/identity.local.properties`(커밋 안 함) > `android/identity.properties`(placeholder · `DAY`).
이유: 소스에 실제 id 를 두지 않는 iOS 원칙과 같고, 다음 판 Play 업로드 스크립트가 같은 `-P` 로 넣으면 된다. flavor(`dev` · `prod` — §4 [제안])는 정식 앱 id 가 [미결]이라 이번엔 만들지 않음 — 나중에 flavor 로 가도 이 두 값만 옮기면 된다.

## minSdk (M-7)

**24** — 플러그인 Android 최소값 중 최대: record_android · audio_session · flutter_tts · image_picker_android · url_launcher_android · video_player_android · flutter_plugin_android_lifecycle = 24(나머지 photo_manager 16 · flutter_pcm_sound 19 · flutter_image_compress 21). Flutter 3.44.8 기본값과 같다. targetSdk 36 · compileSdk 36.

## 권한 (매니페스트 — 문구 없음 · 지어 넣지 않음)

INTERNET · RECORD_AUDIO(통역) · READ_MEDIA_IMAGES · READ_MEDIA_VIDEO · READ_MEDIA_VISUAL_USER_SELECTED(채팅 최근 줄 photo_manager · 13+/14+) · READ_EXTERNAL_STORAGE maxSdk 32. 플러그인이 합쳐 넣는 것: ACCESS_NETWORK_STATE · WAKE_LOCK · (androidx) DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION. CAMERA 는 선언 안 함(image_picker 카메라 = 시스템 카메라 앱 intent — 선언하면 오히려 런타임 권한이 필요해짐). cleartext 허용 없음(저장소) — 로컬 day-local 은 README 대로 개발자 로컬만.

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | All tests passed — +345 ~73(skip = 기존 capture 등) |
| `fvm flutter build ios --no-codesign` | ✓ Built Runner.app (20.7MB) · `git status ios lib` 변경 0 |
| `fvm flutter build apk --debug -P… --dart-define=DAY_LOGIN_ENTRY/DAY_ALLOWED_ORIGINS=https://day-dev.medisolveai.com` | ✓ app-debug.apk · aapt: package `day.medisolveai.dev` · label `DAY Dev` · sdkVersion 24 · targetSdk 36 |
| 비밀 grep(`git diff` + 새 파일) | 키 · 토큰 · 비밀번호 · 계정 0(걸린 것은 `SecretKey` 타입 이름 · `token` 변수명뿐) |

에뮬레이터: AVD `Medium_Phone_API_36.1`(Android 16 · arm64) — 떠 있는 것이 없어 내가 새로 띄움(`-allow-host-audio`). 로그인 = 코디가 준 dev 데모 계정 파일(값은 adb input 으로만 · 출력 없음).

## A1~A5

| | 확인 | 결과 | 스크린샷 |
|---|---|---|---|
| A1 | dev 실제 로그인 → 시술 현황 · 채팅 목록 | **PASS** — 판(처음 cards 0 = 서버 값 그대로 · 뒤에 카드 1 → 그대로 표시) · 채팅 목록(「아직 대화가 없어요」 = 서버 빈 목록 · 오류 없음) | 01-login · 02-board · 03-chat · 06-relaunch-autologin |
| A2 | 다시 켜면 자동 로그인 · 로그아웃 뒤 다시 켜면 로그인 화면 | **PASS** — 자동 로그인(force-stop → 실행 → 바로 판) · 로그아웃 → `day.session` 레코드 0 → force-stop → 실행 = 로그인 화면 | 06 · 07 |
| 푸시 없음 | 오류 화면 없음 · 설정 「알림 꺼짐 · 설정에서 켜기」 | **PASS** | 05-settings(계정 이메일 칸은 회색으로 가림) |
| A3 | iOS `ios/` 변경 0 · build ios --no-codesign | **PASS** | — |
| A4 | `app/lib` 변경 0 · 저장소 비밀 0 | **PASS** | — |
| A5 | [통역하기] → 드로어 → 마이크 권한 → 말하기 → 자막 · 번역 음성 · 칩 TTS | 드로어 · Android 마이크 권한 창(「Allow DAY Dev to record audio?」) · dev 통역 WS 연결 「듣는 중」 **PASS** · 칩 TTS 소리 **PASS**(en · ja — `dumpsys audio` CONTENT_TYPE_SPEECH started) · **음성 입력(말하기 → 자막 · 번역 음성) = 실기기로 넘김**(사용자 결정 — Play 내부 테스트 실기기 A6): 에뮬레이터 로그 `coreaudio: Could not initialize record` — macOS 가 에뮬레이터 프로세스에 맥 마이크를 주지 않음(호스트 권한 · 앱 문제 아님). 에뮬레이터 마이크 설정은 건드리지 않음 | 04a-mic-permission · 04b-drawer · 04c-ja-tts |

화면에 보이는 사람 이름 「이선호」(A-룸2 · 만 21세 · KR) = dev **데모 지점(「KOS 데모 지점」) 시드 데이터**(seed 스크립트 한국어 이름 · 오더 메모 상담 양식). 전화번호는 화면에 없음.

## 조용히 통과하는 자리

- **clearIf 원자성**: 단일 스레드 실행기라 「읽기 · 비교 · 삭제」 사이에 save 가 끼지 않는다 — 그러나 이를 직접 찌르는 시험(동시 save + clearIf)은 없다. Dart 쪽 `MemorySessionStore` 시험은 네이티브를 거치지 않는다. Kotlin 단위 시험(JVM)은 org.json · Keystore 가 안드로이드 스텁이라 이번에 두지 않음.
- **스텁이 없어도 화면이 같은 곳**: push 채널이 아예 없었어도 Dart 는 MissingPluginException 을 삼켜 같은 「알림 꺼짐」 화면이 된다 — 스텁이 실제로 불리는지는 화면으로 구분 안 됨(appName 은 마이크 거부 문구 「설정 → DAY Dev → 마이크」 에서만 보임). video 스텁도 같다(모두 try/catch).
- **로그아웃 때 `DELETE /api/devices/{install_id}`**: 등록한 적 없어도 Dart 가 보낸다(iOS 와 같은 코드) — 서버 404 를 Dart 가 무시. 서버 로그에 Android 설치 id 404 가 남는다.
- **복호화 실패 = 없음**: 앱 데이터 백업 복원 · Keystore 키 손실이면 load null → 로그인 화면(오류 문구 없음). 깨진 암호문은 다음 save · clear 때 덮인다.
- **flutter_pcm_sound compileSdk 덮어쓰기**: 플러그인을 올리면(compileSdk 34+) 이 줄은 필요 없어진다 — 남아도 해 없음.

## 이슈 · 코디가 확인할 것 · 정할 것

1. **A5 음성 입력** → A6(Play 내부 테스트 실기기)에서 말하기 → 자막 원문 · 번역 → 번역 음성(flutter_pcm_sound 재생) 확인 필요. 번역 음성 PCM 재생 경로는 이번에 실물로 못 봄.
2. **Play 정책(다음 판)**: `READ_MEDIA_IMAGES` · `READ_MEDIA_VIDEO` 는 Play 가 「핵심 기능」 신고를 요구할 수 있다(사진 선택기로 대체 권장). 채팅 최근 사진 줄(photo_manager)을 위해 넣었다 — 업로드 때 Play Console 신고 또는 Android 에서 최근 줄 끄기(Dart 변경) 중 정해야 함.
3. **스펙 반영**: id 주입 방식(`-P` > identity.local.properties > identity.properties) · 세션 저장 방식(Keystore AES-GCM + prefs · 백업 제외) · minSdk 24 → mobile-deployment §3 끝 줄 · §7-2 · M-7.
4. Built-in Kotlin 경고: Flutter 3.44.8 이 일부 플러그인(Built-in Kotlin 미이행)에 경고만 냄 — 빌드 실패 아님 · `android.builtInKotlin=false`(템플릿 기본) 유지.
5. release 빌드는 지금 SDK debug 키 서명(템플릿 그대로) — 업로드 키는 다음 판.

## 정리

- 내가 띄운 에뮬레이터(`Medium_Phone_API_36.1` · emulator-5554)는 끝나고 껐다. 앱(`day.medisolveai.dev`)은 설치된 채 로그아웃 상태. 다른 에뮬레이터 · 프로세스는 건드리지 않음.
- 스크린샷: `app-1-shots/` 01-login · 02-board(cards 0) · 03-chat · 04a-interpret-mic-permission · 04b-interpret-drawer · 04c-interpret-ja-tts · 05-settings(이메일 가림) · 06-relaunch-autologin(데모 카드) · 07-relaunch-after-logout.
