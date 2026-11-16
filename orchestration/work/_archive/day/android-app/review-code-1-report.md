# 리뷰 리포트 — android-app AND-1~4 / code (2026-11-13)

검수 대상: 워크트리 `CENTURION_DAY/android-app` · 브랜치 `kknaksss/android-app` (HEAD `0106654e`) 의 **미커밋** 변경 — `app/android/**`(새로) · `app/.metadata` · `app/README.md`.
근거: Delivery #251(v2 · AND-1~4 · A1~A5 · A7) · DAY-SPEC-003 §3 「세션 보관」 · 「Android 개발 앱 — 네이티브 채널」 · A-48 · mobile-deployment §3 · §7-0 · §7-2 · iOS `app/ios/Runner/AppDelegate.swift` · `AcceptLogic.swift`.
A5 음성 입력(말하기 → 자막 → 번역 음성)은 사용자 결정(2026-11-13)대로 A6 실기기 몫이라 FAIL 로 보지 않았다.

## 판정: WARN

FAIL 은 없다. 채널 계약 · 세션 저장 보안 · id 주입 · Dart/iOS 무변경 · 비밀 0 은 모두 맞다. 커밋 전에 W-1(빌드 산출물이 커밋될 수 있음)을 고쳐야 하고, W-2(Play 사진 권한 정책)는 Play 단계(AND-5~7)에 들어가기 전에 정해야 한다.

## 관문 명령 (리뷰어가 1회씩 실행)

| 명령 | 결과 |
|---|---|
| `cd app && fvm flutter analyze` | No issues found (exit 0) |
| `fvm flutter test` | All tests passed — +345 ~73 (exit 0, 워커 수치와 같음) |
| `fvm flutter build apk --debug --android-project-arg=DAY_APPLICATION_ID=day.medisolveai.dev '--android-project-arg=DAY_APP_NAME=DAY Dev' --dart-define=DAY_LOGIN_ENTRY=… --dart-define=DAY_ALLOWED_ORIGINS=…` | ✓ Built (exit 0). `aapt dump badging`: package `day.medisolveai.dev` · label `DAY Dev` · sdkVersion 24 · targetSdkVersion 36 · compileSdk 36 · `allowBackup=false` · cleartext 속성 없음 |
| 병합된 권한(aapt) | INTERNET · RECORD_AUDIO · READ_MEDIA_IMAGES · READ_MEDIA_VIDEO · READ_MEDIA_VISUAL_USER_SELECTED · READ_EXTERNAL_STORAGE(max 32) · ACCESS_NETWORK_STATE · WAKE_LOCK · `<pkg>.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION` |
| iOS `build ios --no-codesign` | 다시 돌리지 않았다. 워커 결과(✓ Runner.app)를 인용한다. `app/ios` 변경이 0이라 이번 변경으로 iOS 빌드 결과가 달라질 수 없다 |

빌드 경고: 플러그인 3개(flutter_image_compress_common · flutter_tts · photo_manager)에서 KGP / Built-in Kotlin 경고가 나온다. 빌드 실패는 아니다(워커 이슈 4와 같음).

## FAIL

없음.

## WARN

### W-1 `app/android/build/` 가 무시되지 않는다 — `git add app/android` 를 하면 Gradle 산출물이 커밋된다
- 위치: `app/android/.gitignore:1-17`(`/build/` 줄이 없음). 실제 파일은 `app/android/build/reports/problems/problems-report.html`.
- 근거: `git ls-files --others --exclude-standard app/android` 에 이 파일이 나오고, `git check-ignore` 로 확인해도 무시되지 않는다. Flutter 템플릿은 빌드 폴더를 `app/build/` 로 옮기지만(`android/build.gradle.kts:8-17`), Gradle 9 의 problems report 는 루트 프로젝트 자리에 따로 써진다. 레포 `AGENTS.md` 「작업 규칙」 기준으로 생성물이 커밋되면 안 된다. 경로 · 비밀 값은 들어 있지 않다(`/Users/` 0건 · 경고 1건뿐).
- 고칠 방향: `app/android/.gitignore` 에 `/build/` 한 줄을 더한다. 커밋할 때는 `git add app/android` 결과에 `build/` 가 없는지 확인한다.

### W-2 READ_MEDIA_IMAGES · READ_MEDIA_VIDEO — Play 내부 테스트(A6) 게시를 막을 수 있다
- 위치: `app/android/app/src/main/AndroidManifest.xml:8-10`
- 근거: Delivery A6(Play 내부 테스트 업로드 → 설치) · mobile-deployment §7-3-1(「그 밖의 앱 콘텐츠 … 확인 안 됨」). Google Play 「사진 및 동영상 권한」 정책은 이 권한을 선언한 앱에 Play Console 신고서를 요구한다. 핵심 기능이 아니면 시스템 사진 선택기를 쓰라고 하고, 신고 전에는 출시 게시가 막힐 수 있다. 다만 내부 테스트 트랙에도 같은 기준이 걸리는지는 이번에 공식 문서로 확인하지 않았다.
- 지금 필요한 이유는 맞다. `lib/chat/photo_pick.dart:179` `PhotoManager.requestPermissionExtend()` 와 `:192` `getAssetListPaged`(채팅 [+] 최근 줄)에 이 권한이 있어야 한다. photo_manager 3.12.0 매니페스트는 READ_EXTERNAL_STORAGE 만 합쳐 넣기 때문에, 이 권한을 빼면 Android 13+ 에서 최근 줄이 늘 「권한 없음」이 된다. 이번 판(로컬 에뮬레이터) 범위에서는 위반이 아니다.
- 고칠 방향: AND-5 전에 코디네이터 · 사용자가 둘 중 하나를 고른다. (a) Play Console 에 「핵심 기능」으로 신고한다(근거: 채팅 최근 사진 줄). (b) Android 에서 최근 줄을 끄고 「사진」 메뉴(`pickMultipleMedia` = 시스템 선택기)만 쓴다. (b)는 Dart 변경이라 SPEC-003 §3 「Dart 바꾸면 코디 · 사용자 확인」에 걸린다. 근거로 쓸 수 있게 워커 이슈 2를 그대로 안건으로 올린다.

### W-3 base 가 `origin/dev` 보다 한 커밋 뒤다 — rebase 하면 하단 메뉴가 3개로 바뀐다
- 위치: HEAD `0106654e` · `origin/dev` `ca72fd1d`(#252 「예약현황 탭 숨김 — 하단 3메뉴」).
- 근거: `git diff origin/dev HEAD -- app/README.md` 에서 2줄(3메뉴 ↔ 4메뉴)이 다르다. 워커의 README 변경은 파일 끝에 덧붙인 것이라 hunk 가 겹치지 않고, rebase 충돌도 예상되지 않는다. 다만 A1 스크린샷(`app-1-shots/02-board.png`)은 4메뉴(예약현황 포함) 화면이다.
- 고칠 방향: PR 전에 `origin/dev` 로 rebase 한다. Android 코드는 Dart 와 무관해서 다시 검증할 것은 analyze · test 정도다. 스크린샷을 다시 찍을지는 코디네이터가 정한다. 계약 위반은 아니고 증거 화면이 옛 base 라는 점만 알린다.

### W-4 (낮음) `SessionStore.run` 이 예외를 막지 않는다 — 막히면 Dart `await` 가 끝나지 않는다
- 위치: `SessionChannel.kt:67-69`(`executor.execute { done(this.work()) }`)
- 근거: `loadRaw` · `save` 는 try/catch 로 감쌌지만, `clear()`(`:86-88`)와 그것을 부르는 `clearIf`(`:91-95`)는 감싸지 않았다. 여기서 RuntimeException 이 나면 실행기 스레드에서 삼켜지고 `result` 는 끝까지 답하지 않는다. 그러면 Dart 의 `clear()` · `clearIf()` future 가 영원히 기다린다(로그아웃 · 401 처리 멈춤). iOS 는 `queue.sync` 라 같은 일이 생기지 않는다. `SharedPreferences.commit()` 이 던지는 일은 드물어서 실제 위험은 낮다.
- 고칠 방향: `run` 안에서 `runCatching { work() }` 로 감싼다. 실패하면 load → null · save → false · clear/clearIf → null 로 답해 결과가 반드시 돌아오게 한다. 동작 계약은 바뀌지 않는다.

## 판정 축별 확인 (PASS 근거)

### 1. 채널 계약 — 같음
| 항목 | iOS | Android | 판정 |
|---|---|---|---|
| 채널 이름 3개 | `AppDelegate.swift:46,50,54(351)` | `MainActivity.kt:18-20` | 같음 |
| session `load` | `:159-160` raw JSON 또는 nil | `SessionChannel.kt:31` · `:71-78` raw 또는 null(복호화 실패도 null) | 같음 |
| session `save` | `:161-166` 인자가 String 이 아니거나 저장 실패 → `keychain_save_failed` | `:32-41` 같은 코드 · 같은 두 갈래 | 같음 |
| session `clear` | `:167-169` → nil | `:42` → null | 같음 |
| session `clearIf` | `:170-176` 인자가 틀리면 지우지 않고 nil · `:208-214` `queue.sync{ storedMatches → clearLocked }` | `:43-51` 인자가 틀리면 null · `:91-95` 실행기 한 작업 안에서 읽기 → 비교 → 삭제 | 같음 |
| 비교 칸 | `AcceptLogic.swift:127-131` JSON 객체의 `token` · `api_base_url` 이 String 으로 같을 때 | `SessionChannel.kt:140-148` `opt("token") as? String` · `opt("api_base_url") as? String` | 같음(JSON null · 숫자 → 불일치 · 파싱 실패 → false 도 같음) |
| 직렬화 | `:188` 직렬 큐 하나 · 모든 접근 `sync` | `:134` 프로세스 전역(companion) `newSingleThreadExecutor` · 4 메서드 모두 `store.run` 을 지남 · 엔진이 다시 붙어도 같은 줄 | 같음 — save 가 clearIf 의 읽기와 삭제 사이에 끼어들 수 없다. 메인 스레드에서 제출한 순서 = 실행 순서 = 답 순서 |
| push `ready`/`requestPermission`/`register` | `:59-83` | `PushChannel.kt:22-24` null/false/null · 역방향 호출 없음 | 스텁(SPEC-003 §3 표 그대로) |
| push `installId`/`appId`/`appName` | `:84-89` | `:25-27` · `:32-39` 소문자 uuid · packageName · label | 같은 모양 |
| video `audio*`/`probe`/`convert` | `:364-398` | `VideoChannel.kt:16-19` null/false/null/`convert_failed` | 스텁. Dart `video_pick.dart:25-53` 이 모두 try/catch → 「동영상을 보내지 못했어요」(SPEC-004 U-6 기존 문구) |
- Dart 소비 쪽(`session_store.dart:79-109` · `push_bridge.dart:35-74` · `video_pick.dart:22-58`)도 확인했다. 반환 타입이 모두 Dart 기대와 맞는다(`invokeMethod<String>` · `<bool>` · `invokeMapMethod` → null 허용).
- 다른 점(문서화됨 · 해롭지 않음): iOS 는 인자가 없는 `probe` 를 `bad_args` 로 답하고 Android 스텁은 null 로 답한다. 둘 다 Dart 에서 null 로 끝난다. 설치 id 는 앱을 지우면 Android 에서 새 값이 된다(워커 표 기재).

### 2. 세션 저장 보안 — 같음(§7-2 [제안] 을 따름)
- 키: AndroidKeyStore · alias `day.session.key` · AES-256 · GCM/NoPadding · ENCRYPT|DECRYPT 만 쓴다(`:97-109`). 키를 꺼낼 수 없다.
- IV: `init(ENCRYPT_MODE, key)` 에 IV 를 넘기지 않는다(`:113`). Keystore 키는 기본값이 randomizedEncryptionRequired=true 라서 IV 를 Keystore 가 무작위로 만들고 호출자가 지정할 수도 없다 → **IV 재사용 0**. 태그는 128bit 로 암 · 복호가 같다(`:122`).
- 평문 0: prefs 값은 `b64(iv):b64(ct)` 하나뿐이다(`:80-81`). 워커가 `run-as cat` 로 평문 칸이 없음을 실기에서 확인했다. `Log.`/`println` 은 0건이다(grep).
- 백업 · 기기 이전 제외: `AndroidManifest.xml:19-21` allowBackup=false · fullBackupContent=false · `data_extraction_rules.xml` 이 cloud-backup 과 device-transfer 의 5개 domain 을 모두 exclude 한다. Android 12+ 에서는 allowBackup=false 만으로 기기 이전이 막히지 않는데, 그 빈자리를 device-transfer 규칙이 메운다. 맞다.
- 예외 처리: 복호화 실패 → null(`:73-77`). 키를 잃은 경우 `key()` 가 새 키를 만들고 복호화가 실패해 null → 다음 save 가 새 키로 덮는다. 저장 실패 → `keychain_save_failed`. 남은 구멍은 W-4 뿐이다.

### 3. id 주입 — 같음
- `app/build.gradle.kts:11-22`: `identity.properties` → `identity.local.properties` 순으로 같은 Properties 에 load 해서 local 이 키 단위로 덮는다. 그 위에 `project.findProperty(key)`(-P)가 먼저 온다. 그래서 **-P > local > 기본** 순서가 맞다. 빈 값은 `require` 로 빌드를 실패시킨다(조용한 폴백 없음).
- 실제 빌드에서 -P 로 `day.medisolveai.dev` · `DAY Dev` 가 들어간 것을 aapt 로 확인했다.
- 소스의 id 는 `com.example.day.placeholder` · `DAY` 뿐이다(`identity.properties:6-7`). 실제 id 는 README 예시 명령에만 있고, 이 값은 스펙 §3 의 [확정] 공개 값이라 비밀이 아니다.
- `.gitignore:17` `/identity.local.properties` → check-ignore 로 확인했다.
- 참고: `findProperty` 는 `~/.gradle/gradle.properties` · `ORG_GRADLE_PROJECT_DAY_*` 환경 변수도 -P 와 같은 자리로 읽는다. 개발자 PC 전역 설정에 이 키가 있으면 local 파일보다 앞선다. 스펙에 적을 때 한 줄로 남기면 된다.

### 4. 권한 · 매니페스트
- 필요한 권한은 빠짐없이 있다. RECORD_AUDIO(`record_android` 매니페스트도 합쳐 넣음) · INTERNET · 사진 권한(W-2 참고). CAMERA 를 선언하지 않은 것도 맞다(image_picker 카메라는 시스템 카메라 intent 라 선언하면 오히려 런타임 권한이 필요해짐).
- cleartext 0: main · debug · profile 매니페스트에 `usesCleartextTraffic` · networkSecurityConfig 가 없다. debug 매니페스트(`src/debug/AndroidManifest.xml`)는 템플릿 그대로다.
- queries: PROCESS_TEXT(템플릿) · TTS_SERVICE(flutter_tts · Android 11+) · https VIEW(`chat_link.dart:10` `launchUrl` externalApplication). 맞다.
- edge-to-edge(targetSdk 36 강제): 스크린샷 02-board 에서 상태 막대 · 제스처 막대 아래에 겹침이 없다.

### 5. Dart · iOS 무변경 — 같음
- `git diff HEAD --stat` = `app/.metadata` +3 · `app/README.md` +43뿐이다. `app/lib` · `app/ios` · `app/test` 변경은 0이다.
- README 는 **추가만** 했다. 기존 줄 수정은 0이고 `@@ -169,3 +169,46 @@` 끝에 덧붙였다. `.metadata` 는 `platform: android` 3줄만 더했다.

### 6. 빌드 설정
- targetSdk 36(`build.gradle.kts:45`)은 mobile-deployment §7-3-1 의 Play 기준과 맞다.
- minSdk 24(`:43`)의 근거는 플러그인 최소값 중 최대값이다. pub-cache 로 일부를 확인했다(flutter_pcm_sound 19 · 나머지는 워커 표). Flutter 3.44.8 기본값과 같다.
- `flutter_pcm_sound` 덮어쓰기(`android/build.gradle.kts:29-35`)는 `name == "flutter_pcm_sound"` 인 subproject 한 곳에만, compileSdk 하나만 36 으로 바꾼다. 범위가 맞고, 원래 값 33(`pub-cache/.../flutter_pcm_sound-3.3.3/android/build.gradle:7`)도 확인했다.
- release 서명 = debug 키(`app/build.gradle.kts:50-56`)는 다음 판 전까지 위험이 없다. 저장소에 키를 두지 않고, Play Console 은 debug 서명 AAB 를 거절한다. 조용히 통과할 수 없는 자리다. AND-5 에서 업로드 키 서명으로 바꾸는 것만 잊지 않으면 된다.

### 7. A7 비밀 0 — PASS
- 새 파일 전체(png 제외)와 README diff 를 password · secret · api key · private key · BEGIN · token · 이메일 · `storePassword` · `keyAlias` · `AIza` · `ghp_` · URL 로 grep 했다. 걸린 것은 `SecretKey` 타입 이름과 `token` 변수 · 주석, Gradle report 의 공개 CDN URL 뿐이다. 이메일 · 키 · 비밀번호는 0이다. README 의 dev 주소는 `<dev 공개 주소>` placeholder 다.

## 조용히 통과하는 자리
1. **clearIf 원자성은 자동 시험이 없다.** Dart `MemorySessionStore` 시험은 네이티브를 거치지 않고, Kotlin 단위 시험도 없다. 지금의 원자성은 「실행기가 하나」라는 구조로만 보장된다. 누군가 `store.run` 을 거치지 않는 경로(예: 네이티브 수락이 생길 때 메인 스레드에서 직접 `loadRaw`)를 더하면 시험은 초록인 채로 깨진다. FCM · 네이티브 수락을 넣을 때 「모든 접근은 `run`」을 지켜야 한다. 순수 함수 `storedMatches` 는 Robolectric 같은 JVM 시험으로 붙일 수 있다(다음 판 제안).
2. **스텁이 없어도 화면이 같다.** push · video 채널이 없어 MissingPluginException 이 나도 Dart 가 삼켜 같은 화면이 된다. 스텁이 실제로 불렸는지는 `appName`(마이크 거부 문구의 「DAY Dev」)으로만 보인다(워커 기재와 같음).
3. **W-4** — `clear` 가 던지면 Dart future 가 답 없이 멈춘다(오류 화면 없이 로그아웃이 진행되지 않음).
4. **로그아웃 `DELETE /api/devices/{install_id}`** 는 등록한 적이 없어도 나간다 → 서버 404 를 Dart 가 무시한다. 서버 로그에 Android 설치 id 의 404 가 쌓인다(워커 기재).
5. **복호화 실패 = 로그인 화면** · 오류 문구가 없다. Keystore 키를 잃었는지 사용자는 구분할 수 없다(의도한 동작).

## 사용자가 실물에서 만날 자리 (Android 개발 앱)
- 설정 「알림」 칸은 늘 「알림 꺼짐」이다. OS 설정에서 켜도 사라지지 않는다(SPEC-003 §3 문서화).
- 원장 호출 · 채팅 푸시 · 알림 [수락]이 없다. 앱이 앞에 있을 때만 SSE 로 바뀐다.
- 채팅 동영상 보내기는 항상 「동영상을 보내지 못했어요」다. 최근 줄에서 동영상 썸네일은 보이지만 보낼 수 없다.
- 채팅 [+] 최근 사진 줄은 Android 13+ 에서 사진 권한 창이 뜨고, 14+ 에서는 「일부 허용」 갈래가 있다. Play 정책 결정(W-2)에 따라 바뀔 수 있다.
- 시스템 뒤로 가기(제스처 · 버튼): iOS 에는 없는 입력이다. targetSdk 36 에서는 predictive back 이 기본으로 켜진다. `lib` 에서 PopScope 를 쓰는 곳은 `chat_kit.dart` · `chat_forward_sheet.dart` 둘뿐이라, 루트 화면에서 뒤로 가면 앱이 백그라운드로 간다. 시트 · 드로어 · 룸 상세는 Flutter 기본 pop 동작을 따른다. 이번 실물 확인(A1~A5)에 뒤로 가기는 들어 있지 않았다. A6 실기기에서 한 번 눌러 보기를 권한다.
- 로컬 빌드와 Play 빌드는 서명이 달라 한 기기에 같이 깔 수 없다. 바꿀 때 지우고 깔아야 하고, 그때 세션도 지워진다(SPEC-003 §3 문서화).
- 통역 음성 입력 → 자막 · 번역 음성(flutter_pcm_sound 재생)은 아직 실물로 보지 못했다 → A6(사용자 결정).

## 스펙에 반영할 것 (mediness — 코디네이터 → spec 워커)
1. **id 주입**(mobile-deployment §3 끝 줄 「정하지 않았다」 → 정함): `-P`(`--android-project-arg=DAY_APPLICATION_ID=…` · `DAY_APP_NAME=…`) > `android/identity.local.properties`(커밋 안 함) > `android/identity.properties`(placeholder `com.example.day.placeholder` · `DAY`). iOS `DAY_BUNDLE_ID` · `Identity.local.xcconfig` 와 같은 3단이다. flavor 는 아직 만들지 않았다(§4 [제안] 그대로). 「-P 자리 = Gradle 프로젝트 속성(~/.gradle/gradle.properties · ORG_GRADLE_PROJECT_* 포함)」 한 줄도 덧붙인다.
2. **세션 저장**(§7-0 · §7-2 [제안] · SPEC-003 §3 「세션 보관」 저장소 칸): Android Keystore AES-256-GCM 키(alias `day.session.key`) + 앱 전용 SharedPreferences 값 하나(`day.session`) · 무작위 IV · 클라우드 백업 · 기기 이전 제외(dataExtractionRules) · 사용자 인증 요구 없음 · 단일 직렬 실행기. 사용자가 확정할지는 그대로 열어 둔다([제안] → 「구현됨 · 확정 대기」).
3. **minSdk 24**(M-7): 근거는 플러그인 최소값 중 최대(record · audio_session · flutter_tts · image_picker · url_launcher · video_player = 24)이고 Flutter 3.44.8 기본값이다. targetSdk · compileSdk 36. `flutter_pcm_sound` compileSdk 덮어쓰기 1건.
4. (안건) W-2 Play 사진 권한 — §7-3-1 표에 「사진 및 동영상 권한 신고 — 확인 안 됨」 줄을 더하고 결정은 사용자 몫으로 둔다.

## 참고(기존 부채 · 이번 범위 밖)
- KGP / Built-in Kotlin 경고(플러그인 3개) — 플러그인을 올릴 때 다시 본다. `gradle.properties:4-6` 은 템플릿 기본값이다.
- `PushChannel.installId` 는 메인 스레드에서 `commit()` 한다(최초 1회 · 아주 작은 디스크 I/O). 실제 영향은 없다.
- iOS 빌드를 리뷰어가 다시 돌리지는 않았다(워커 결과 인용 · iOS 변경 0).
