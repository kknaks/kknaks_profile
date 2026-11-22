# day-mobile-v2 F2 결과 보고 — Android 푸시(FCM) 앱 쪽

## 상태: done (커밋 · push · PR 없음 · 실기기 · 에뮬레이터 실푸시 = pending(F3))

base = 서버 F1 `87cec04d`. `backend/**` 는 읽기만(워크트리의 backend 변경 — 푸시 묶음 = callId 고침 — 은 backend 몫).

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `app/android/settings.gradle.kts` | Google 서비스 플러그인 `com.google.gms.google-services` 4.4.4(`apply false`) |
| `app/android/app/build.gradle.kts` | `app/google-services.json` 이 있고 **그 안에 이 빌드의 applicationId 가 있을 때만** 플러그인 적용(없거나 임시 기본값 식별자 = 푸시 없이 빌드 · OQ-A60) · `firebase-bom` 34.19.0 · `firebase-messaging` · `androidx.core` 1.17.0 · 단위 시험 의존(junit · org.json) |
| `app/android/app/src/main/AndroidManifest.xml` | `POST_NOTIFICATIONS` 권한 · `DayMessagingService`(MESSAGING_EVENT · exported false) · `AcceptReceiver`(exported false) |
| `…/PushChannel.kt` | 스텁 → 구현: `ready`(눌러서 연 알림 · 들고 있던 토큰) · `requestPermission`(Android 13+ 한 번만 묻고 그 뒤는 지금 값 — iOS 처럼 다시 안 물음 · 허락이면 FCM 토큰 → onToken · Firebase 없는 빌드 = false) · `register`(토큰 다시) · installId · appId · appName 그대로 |
| `…/PushHub.kt`(새) | 프로세스 공용 자리(채널 · dartReady · 대기 토큰 · 대기 누름 · 앞에 있음) + `Notifier`(채널 2개 · 로컬 알림 · 누름 intent · [수락] 액션 · 결과 알림) |
| `…/DayMessagingService.kt`(새) | `onNewToken` → Dart 다시 등록 · `onMessageReceived`(data) → 앞에서 받은 채팅 = 시스템 알림 없이 Dart 앱 안 배너 · 원장 호출 · 호출 취소 = 알림 + Dart 종 다시 읽기 · 그 밖 = 로컬 알림 |
| `…/AcceptReceiver.kt`(새) | 알림 [수락] — 엔진 없이 저장된 세션 묶음(`SessionStore`)으로 `POST {api_base_url}/api/calls/{callId}/accept {doctorStaffId}` · 리다이렉트 안 따라감 · 20초 · 결과 알림 · 401 = 그 세션만 지움 · 만료 = 보내지 않고 지움 · 다른 환경 = 아무것도 · 누른 알림 닫음 |
| `…/PushLogic.kt`(새) | 순수 판단(iOS `AcceptLogic.swift` 의 `PushPayload` · `AcceptLogic` · `DaySession` 와 같은 규칙 · 같은 글자) |
| `…/MainActivity.kt` | day/push 를 구현으로 · 알림 누름 intent → Dart onTap(꺼진 상태 = ready 때) · 앞/뒤 표시 · 권한 결과 전달 |
| `app/android/app/src/test/kotlin/day/medisolveai/PushLogicTest.kt`(새 · 6) | 세션 묶음 · 수락 판단 · origin · 결과 글자 · 채널 · tag · 액션 · Dart 칸 |
| `app/lib/data/push_bridge.dart` | `PushBridge.platform`(Android = `android`) |
| `app/lib/state/push_coordinator.dart` | Android 등록 = `platform: android` · **`push_env` 안 보냄**(OQ-A51) · APNs 환경 설정 없어도 등록 |
| `app/test/state/push_coordinator_test.dart` | 새 2건(Android 등록 본문 · iOS 는 그대로 APNs 설정 필요) |
| `.gitignore`(루트) | `google-services.json` 한 줄(Android 비밀 줄 옆) — `git check-ignore` 로 `app/android/app/google-services.json` 무시 확인 |

## 동작 — 스펙 대조(DAY-SPEC-003 §3 「Android 푸시 — FCM」 · OQ-A59 · OQ-A60 · iOS 와 같게)

| 항목 | Android |
|---|---|
| 메시지 | 서버 data 메시지(`adapters/fcm.py` `data_of` — kind · environment · hospitalId · visitId · callId · roomId · messageId · title · body · category) → 앱이 로컬 알림(앞 · 뒤 · 꺼짐) |
| 알림 채널 | 둘 — `doctor_call` 「원장 호출」 · `chat` 「채팅」(글자 = `notification_model.dart:16` `notifKindName` · 새 글자 없음) · 중요도 높음 · **호출 취소 = 「원장 호출」 채널** |
| [수락] | 원장 호출 + `category = CALL` 일 때만(호출 취소 · 채팅 없음) · 글자 「수락」(iOS 액션 글자 그대로) · 결과 글자 iOS 와 같음 |
| 누름 | iOS 와 같은 칸(`tapKeys`)으로 Dart `onTap` → 원장 호출 · 호출 취소 = 룸 상세 + callId 읽음 · 채팅 = 대화방(환경 · 병원 판정은 Dart · 기존 코드) |
| 호출 취소 → 원래 알림 | 원장 호출 · 호출 취소 tag = `call:{callId}` → **취소 알림이 같은 자리의 원래 원장 호출 알림을 덮는다**(앱이 뒤 · 꺼짐이어도 바로 — data 메시지는 앱 코드가 받으므로). 서버 backend 고침의 설명(`test_push_collapse.py` — 「Android 는 앱이 data `callId` 를 tag 로 쓴다 · 서버 칸 추가 없음」)과 같은 키 |
| 앞에서 받음 | 채팅 = 시스템 알림 없이 앱 안 배너(Dart 준비 뒤) · 원장 호출 · 호출 취소 = 알림 그대로 + 종 다시 읽기 |
| 권한(Android 13+) | 로그인 뒤 한 번 묻고 그 뒤는 지금 값만(설정 앱에서 켜고 돌아오면 앞으로 올 때 반영) · 거부 = 푸시 없이(U-14) |
| 기기 등록 | `PUT /api/devices/{install_id}` · `platform: android` · `app_id` = applicationId · `push_env` 없음 · `kind` 그대로 · 토큰 바뀜(onNewToken) = 다시 |
| google-services.json 없음(OQ-A60) | 플러그인 안 걸림 · FirebaseApp 없음 → `requestPermission` = false(스텁과 같음) · 앱은 그대로 돈다 |
| 모르는 kind | 알림을 띄우지 않음(관대한 읽기 — iOS 는 OS 가 alert 를 그대로 띄우므로 이 점만 다름) |

## 검증

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+414 ~81 All tests passed**(새 2) |
| `fvm flutter build apk --debug`(google-services.json **없음** · 기본 식별자) | ✓ `app-debug.apk` — 플러그인 없이 빌드 |
| `fvm flutter build apk --debug --android-project-arg=DAY_APPLICATION_ID=day.medisolveai.dev …`(json **복사**) | ✓ `app-debug.apk` — 생성 리소스에 `google_app_id` · `project_id` 확인(플러그인 적용됨) |
| `./gradlew :app:testDebugUnitTest`(JAVA_HOME = Homebrew openjdk@17) | **6 tests · 0 failures** |
| `fvm flutter build ios --no-codesign` | ✓ `Runner.app` (20.8MB) |

- 복사한 `app/android/app/google-services.json` 은 빌드 뒤 지웠다(빌드 때만 · 무시 확인됨). 다시 빌드: `cp ~/.config/day/android/google-services.json app/android/app/` + `--android-project-arg=DAY_APPLICATION_ID=day.medisolveai.dev`(또는 `day.medisolveai`).
- **실푸시(에뮬레이터 · 실기기) = pending(F3)** — 에뮬레이터 · 기기 무접촉.

## 이슈 · 코디가 확인할 것
1. **맥 디스크가 거의 꽉 참** — 첫 apk 빌드가 `No space left on device` 로 실패. 내 빌드 산출물 `app/build`(gitignore)만 지우고 다시 돌렸다(그 뒤 다른 쪽에서 공간이 풀려 27GB). 사용자 파일은 건드리지 않음.
2. `./gradlew` 는 셸의 `JAVA_HOME`(없는 Android Studio JBR 경로)을 그대로 쓰면 실패 — Homebrew openjdk@17 로 돌렸다(flutter 빌드는 flutter 가 고른 JDK 라 영향 없음).
3. 작은 아이콘 = 앱 런처 아이콘(`mipmap/ic_launcher`) — Android 알림 아이콘은 단색이 권장이라 상태 바에서 흰 네모처럼 보일 수 있다(시안 · 자산 없음 — 사용자 판단).
4. 기본 식별자(`com.example.day.placeholder`)로 json 을 넣고 빌드하면 json 에 그 앱이 없어 **푸시 없이** 빌드된다(빌드 로그 「DAY: … 푸시(FCM) 없이 빌드」) — 의도된 동작(빌드가 멈추지 않음).
5. `app/README.md` 「Android」 절(푸시 = 스텁 서술)은 allowed_paths 밖이라 고치지 않음 — 문서 갱신 필요.
6. 워크트리 `backend/**` · `scripts/**` 변경은 내 것 아님.
