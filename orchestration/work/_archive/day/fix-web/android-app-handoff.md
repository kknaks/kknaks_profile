# 인수인계 — DAY 직원 앱 Android 로컬 실행 (다음 slug `android-app`)

작성 2026-11-12 · fix-web 코디 세션에서 사용자와 범위를 닫음. **발주는 아직 안 했다.**
다음 세션은 이 문서를 읽고 `scripts/new-work.sh day android-app` 부터 시작한다.

## 1. 목표

DAY 개발 앱(`DAY Dev`)을 **로컬 Android 에뮬레이터**에서 띄워 **dev 서버에 로그인 → 화면 확인**까지.
스토어 출시 · 푸시는 범위 밖이다.

## 2. 사용자와 정한 것 (2026-11-12)

| 항목 | 결정 |
|---|---|
| 범위 | ① `app/android/` 생성 ② `day/session` Kotlin 구현 ③ 권한 · 설정 |
| 푸시 `day/push` | Kotlin 에서 **스텁**(권한 false · 토큰 없음 · installId/appId/appName 정도만 값). Firebase(FCM)는 **다음 작업** — 회사 Google 계정을 아직 몰라서(사용자) |
| 동영상 · 오디오 `day/video` | 스텁. Android 에선 채팅 동영상 첨부 · 통역 오디오 전환만 빠진다 |
| 알림 [수락](`AcceptLogic.swift`) | 안 함(푸시 뒤) |
| 앱 id · 이름 | `day.medisolveai.dev` / `DAY Dev` (iOS 개발판과 같게) |
| iOS | **안 건드린다** — 정식 0.1.0 (2) 심사 중 |
| Play Console · Firebase | 나중. 계정 생기면 별도 slug |

## 3. 지금 상태 (확인한 사실)

- 코드 `~/git/CENTURION_DAY`(dev `c5045a99`) `app/` = Flutter, `.fvmrc` 3.44.8 · `fvm` 에 3.44.8 있음
- **`app/android/` 없음** — iOS 전용으로만 지어 왔다
- 네이티브 채널 3개가 `ios/Runner/AppDelegate.swift`(445줄)에만 있다:
  - `day/session` — load · save · clear · clearIf(token · api_base_url 비교 후 삭제, 직렬 큐 하나로 원자적). Dart `lib/data/session_store.dart` `KeychainSessionStore`. **없으면 로그인 직후 터진다**
  - `day/push` — ready · requestPermission · register · installId · appId · appName / 역방향 onToken · onTap · onForeground. Dart `lib/data/push_bridge.dart`, `lib/main.dart` 에서 바로 생성
  - `day/video` — audioSave · audioFollowSilent · audioRestore · probe · convert. Dart `lib/chat/video_pick.dart` · `chat_video_screen.dart`
- 플러그인 권한 필요: `record`(마이크) · `image_picker` · `photo_manager`(사진 · 동영상) · `flutter_tts` · `url_launcher` · 인터넷
- 로컬 Android: SDK `~/Library/Android/sdk`(emulator · platform-tools · ndk) · AVD `Medium_Phone_API_36.1` · `mediness_api36` · `emulator` 는 PATH 에 없음(절대경로로)

## 4. 빌드 값

`--dart-define` — 정의는 `app/README.md` 「빌드 설정」.

- **dev 서버로**: `DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS` = dev 공개 주소(`https://day-dev.medisolveai.com`, 3차 TestFlight 개발판과 같은 값 — `_archive/day/fix/app-testflight-upload-2-report.md`). `DAY_APNS_ENV` 는 푸시 스텁이라 의미 없음
- **로컬 day-local 로** 붙일 땐: 에뮬레이터에서 호스트는 `127.0.0.1` 이 아니라 **`10.0.2.2`**, http 라 cleartext 허용이 필요 — 이건 iOS ATS 처럼 **저장소에 넣지 말고 개발자 로컬에서만**(README 원칙). 기본은 dev 서버로 간다
- 로그인 계정 = dev 데모 테넌트 계정(이미 쓰는 것)

## 5. 발주 때 주의

- 계약이 닿는 곳 전수조사: `grep -rn "MethodChannel(" app/lib` 로 채널 전부 세고 시작(3개로 확인됐지만 워커가 다시 센다)
- Dart 쪽 동작은 바꾸지 않는 게 기본 — Android 에서 막을 건 Kotlin 스텁으로. Dart 를 고쳐야 하면 코디에게 묻는다
- 문서: `app/README.md` 에 Android 실행법 한 절 · 스펙(mediness `products/day/` mobile-deployment)에 「Android = 로컬 실행만, 푸시 없음」 반영 여부는 발주 전 사용자와 닫는다(문서 파이프라인)
- 완료 조건 = **에뮬레이터에서 실제 dev 로그인 → 시술 현황 · 채팅 목록이 뜨는 것**(실물 e2e). 워커는 사용자 에뮬레이터 · 프로세스 함부로 끄지 않는다
- iOS 빌드 깨지지 않는지 `fvm flutter build ios --no-codesign` 한 번

## 6. 다음 작업 (이번 범위 밖)

- FCM 푸시: Firebase 프로젝트(회사 계정) · `google-services.json` · 서버 기기 등록에 FCM 발송 · 알림 [수락] Android 판
- `day/video` Kotlin 구현
- Play Console 등록 · 서명 키 · 내부 테스트 트랙
