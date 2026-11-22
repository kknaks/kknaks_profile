# 코드 검수 — 앱 푸시: M3 iOS 호출 취소 알림(ecea81d4) + F2 Android FCM(b87925c6)

워크트리 `CENTURION_DAY/day-mobile-v2` · 읽기만(수정 · 커밋 없음). 서버 사실 = HEAD `c22b56bc`(apns-collapse-id = callId) + 워크트리의 backend 고침 2(fcm 토큰 공유 · 칸 이름 변경 없음).

## 판정: **PASS with WARN** — FAIL 0 · WARN 6 · PASS 나머지

검수 지시 6개 항목에 FAIL(계약 어긋남 · 비밀값 노출 · 빌드 깨짐)은 없다. WARN 은 고칠 만한 경합 · 운영 위험이다.

## 검증 실행(이번 검수에서 직접 돌림)

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test test/notify/call_cancel_test.dart test/state/push_coordinator_test.dart` | +22 All tests passed |
| `sh app/tool/native_logic_test.sh`(Swift 판단) | ALL PASS(M3 새 6건 포함) |
| `./gradlew :app:testDebugUnitTest --rerun`(openjdk@17) | `PushLogicTest` tests=6 failures=0 errors=0 |
| `git ls-files \| grep google-services` | 없음 · `git check-ignore` → `.gitignore:23` 이 `app/android/app/google-services.json` 을 무시함 · 워크트리에 파일 없음 |

apk · ios 빌드는 다시 돌리지 않았다(F2 리포트의 두 갈래 빌드 결과를 믿고 · 디스크 부족 이력).

## 1. iOS · Android 같은 동작

| 항목 | iOS | Android | 판정 |
|---|---|---|---|
| 원장 호출 [수락] | `category=CALL` 일 때만 · 액션 「수락」 | `PushLogic.kt:68` `hasAccept` = kind doctor_call + category CALL · `AcceptReceiver.kt:21` 「수락」 | PASS |
| 누름 → 룸 상세 | `PushPayload.tap` → Dart `_onTap` | `PushLogic.kt:29,36` 같은 `tapKeys` → `Notifier.tapIntent` → `MainActivity.kt:49-53` → `PushHub.tap`(준비 전이면 `ready` 때) | PASS |
| 채팅 · 앞에서 받음 | 시스템 배너 없이 Dart | `DayMessagingService.kt:18-22` · `foreground && dartReady` 일 때만 Dart · 아니면 로컬 알림 | PASS |
| 호출 취소 → 원래 알림 | 서버 `apns-collapse-id=callId`(`backend/day/adapters/apns.py:98-100`)로 대체 + 앱이 `removeDelivered` | tag `call:{callId}`(`PushLogic.kt:58-65`)로 같은 자리 덮음 · 앱이 뒤/꺼짐이어도 즉시(data 메시지 = 앱 코드) | PASS(아래 W-1) |
| 호출 취소 [수락] 없음 · 누름 = 룸 상세 | `push_coordinator.dart` `callPushKinds` | 같은 Dart 경로 · 취소에는 액션 없음 | PASS |
| 앞 · 뒤 · 꺼짐 | 꺼짐 누름 = `ready` | 꺼짐 누름 = `onCreate`(`savedInstanceState==null`) → `pendingTap` → `ready` · 뒤 = `singleTop` `onNewIntent` | PASS |
| 회전 · 엔진 교체 | — | `PushHub.detach` 가 `channel === ch` 일 때만 끊음(`PushHub.kt:55-60`) → 새 엔진 채널을 지우지 않음 | PASS |

## 2. FCM data 칸 · 채널 · 권한 · 토큰

- **data 칸 = 서버와 같음 — PASS.** 서버 `data_of`(`backend/day/adapters/fcm.py` `data_of`) = APNs 커스텀 칸 그대로 + `title` · `body` · `category`. 원장 호출(`services/notifications.py:510-518`: kind · environment · hospitalId · visitId · callId · category CALL) · 호출 취소(`services/notification_cancel.py:254-261`: category 없음) · 채팅(`services/chat_push.py:136-142`: roomId · messageId) 모두 `PushLogic.kt:29-30` 키와 일치. 워크트리 backend 고침 2 는 칸 이름을 바꾸지 않음(토큰 공유 · 오류 분류만).
- **채널 이름 = 앱 글자 — PASS.** `PushLogic.kt:24-25` 「원장 호출」 · 「채팅」 = `notification_model.dart` `notifKindName`(`doctor_call` 「원장 호출」 · `chat` = `menuChat`). 호출 취소 = `CHANNEL_CALL`(`PushLogic.kt:54`) — OQ-A59 대로.
- **Android 13+ 권한 — PASS.** Manifest `POST_NOTIFICATIONS` · `PushChannel.kt:66-79` 13+ 미허락이고 처음일 때만 요청 · 그 뒤는 지금 값 · `onResume` 이 다시 물어 설정 앱 변경 반영(`push_coordinator.dart` `onResume`). 13 미만은 `areNotificationsEnabled`.
- **토큰 갱신 → 재등록 — PASS.** `DayMessagingService.onNewToken` → `PushHub.token`(Dart 미준비 = 메모리에 들고 `ready` 때) → `_onToken` → `PUT /api/devices` (`platform: android` · `push_env` 없음 · `push_coordinator.dart:141-164`). 프로세스가 죽어 메모리 토큰이 사라져도 다음 로그인 · 앞으로 옴의 `fetchToken` 이 현재 토큰을 다시 받음.

## 3. [수락] — 엔진 없이 저장 세션으로

| 확인 | iOS `AcceptLogic.decide` | Android `AcceptLogic.decide`(`PushLogic.kt:162-173`) | 판정 |
|---|---|---|---|
| 세션 없음 | 「앱에서 다시 로그인해 주세요」 | 같음 | PASS |
| 환경(dev/prod) 다름 · 세션 env null | 아무것도 안 함 | 같음(`:165`) · Receiver 도 `Unit`(`AcceptReceiver.kt:52`) | PASS |
| 만료 | 보내지 않고 같은 세션이면 지움 | `clearIf(token, base)`(`AcceptReceiver.kt:49`) | PASS(W-2 경합) |
| origin · staffId · callId 검증 | https 정규화 · http 는 DEBUG | 같음 · http 는 `FLAG_DEBUGGABLE` | PASS |
| 병원 확인 | 앱이 하지 않음(서버가 토큰으로) | 같음 | PASS(동등) |
| 401 → 그 세션만 지움 · 리다이렉트 안 따라감 | 같음 | `endsSession` · `instanceFollowRedirects=false` | PASS |
| 비밀값 로그 | — | Kotlin 새 파일 전체에 `Log.` · `println` 없음 · 결과 알림에 토큰 없음 · 누름 intent 는 `tapKeys` 만 | PASS |

## 4. google-services.json · 빌드

- 커밋 안 됨 · `.gitignore:23` 한 줄 — PASS.
- `build.gradle.kts`: 파일이 있고 그 안 `package_name` 이 이 빌드의 `DAY_APPLICATION_ID` 일 때만 플러그인 적용 · 아니면 로그 한 줄 + 푸시 없이 빌드 — OQ-A60 대로 PASS. `firebase-messaging` 은 늘 들어가지만 `google_app_id` 리소스가 없으면 FirebaseApp 이 없고 `PushChannel.requestPermission` = false(`PushChannel.kt:67`) — 스텁과 같은 동작.
- W-5 참조(release 빌드도 조용히 푸시 없이 나갈 수 있음).

## 5. M3 `NativeLogicTests/main.swift` 범위 밖 수정 — PASS(타당)

수정은 시험 18줄 추가뿐(`main.swift:118-134`) · 기존 네이티브 판단 시험 파일이고 `tool/native_logic_test.sh` 가 컴파일한다. 새 순수 함수(`cancelledCallIds` · `callsToClear`)를 시험할 유일한 자리라 추가가 맞다. 앞으로 allowed_paths 에 `app/ios/NativeLogicTests/` 를 넣기 권함.

## WARN

**W-1 · iOS 앞에서 받은 호출 취소가 자기 자신을 지울 수 있음** — `app/ios/Runner/AppDelegate.swift:121-124,170-178`
M3 는 collapse-id 이전에 쓰였다. 지금 서버가 원장 호출 · 호출 취소에 같은 `apns-collapse-id = callId` 를 싣고(`backend/day/adapters/apns.py:98-100`), iOS 는 collapse-id 를 알림 요청 identifier 로 쓴다 → 원래 원장 호출과 호출 취소의 `request.identifier` 가 **같다**. `willPresent` 에서 `clearCancelledCalls(extra: callId)` 는 비동기 `getDeliveredNotifications` 를 부르고 곧바로 `completionHandler([.banner…])` 를 부른다. 콜백이 아직 원래 원장 호출(kind doctor_call · id = callId)을 보고 `removeDeliveredNotifications([callId])` 를 부를 때 그 사이 같은 id 의 호출 취소가 이미 표시돼 있으면 **취소 알림까지 지워진다**(경합). collapse 로 OS 가 이미 대체하므로 앱 지우기는 이제 중복이다. 제안: `willPresent` 의 지우기를 빼거나, 지울 대상을 `request.identifier != callId`(collapse 이전 옛 알림)로 한정. 실기기 A-50 에서 앞 수신 취소 배너가 알림 센터에 남는지 확인.

**W-2 · `AcceptReceiver` 가 세션 저장소의 직렬 실행기를 우회** — `AcceptReceiver.kt:42-57` vs `SessionChannel.kt:58-60,70-72,137`
`SessionStore` 문서 불변식 = 「모든 접근(load · save · clear · clearIf)은 단일 스레드 실행기 하나를 지난다 — 읽고 비교하고 지우기 사이에 새 로그인 저장이 끼어들 수 없다」. Receiver 는 자기 `day.accept` 스레드에서 `loadRaw()` · `clearIf()` 를 직접 부른다. [수락] 결과 401 처리 중 Dart 로그인이 `save` 하면 `clearIf` 의 비교와 `clear` 사이에 끼어 **새 세션이 지워질 수 있다**(좁지만 iOS 가 막은 바로 그 경합). 제안: `store.run(...)` 으로 감싸거나 `executor` 를 공유.

**W-3 · [수락] 결과 알림을 눌러도 아무 화면도 안 열림(iOS · Android 같음 · 기존 결함 복사)** — `PushHub.kt:124-130` · `AppDelegate.swift:356-363` · `push_coordinator.dart` `_onTap` → `_hospitalMatches`
결과 알림 payload = kind · visitId · environment 뿐 · `hospitalId` 없음. Dart `_onTap` 은 병원 일치를 요구하므로 조용히 버린다(주석 「누르면 그 방문 룸 상세」와 다름). 동작은 두 플랫폼이 같아 parity 는 PASS. 제안: 두 쪽 모두 원래 data 의 `hospitalId`(와 `callId`)를 실어 둔다 + Dart 시험 1건.

**W-4 · [수락] 요청 시간 상한이 리시버 창보다 길 수 있음** — `AcceptReceiver.kt:29-35,69-71`
`goAsync()` 후 connect 20s + read 20s(최대 ~40s+). 브로드캐스트 리시버 ANR 창은 foreground 10s / background 60s 이고 알림 액션 브로드캐스트가 어느 쪽으로 오는지는 기기 · 버전 의존. iOS 는 `timeoutInterval: 20`. 제안: 전체 상한을 ~9s 로(또는 connect 5s + read 5s) · 실패는 기존 「서버에 연결할 수 없어요」.

**W-5 · release 빌드가 json 없이도 조용히 푸시 없이 나감** — `app/build.gradle.kts`(FCM 블록)
OQ-A60 은 로컬 빌드 대상. 지금은 Play 업로드 AAB 도 파일이 없으면 로그 한 줄만 남기고 FCM 없이 빌드된다(업로드 키는 `preReleaseBuild` 에서 막는데 FCM 은 안 막음). 제안: `preReleaseBuild`/`bundleRelease` 에서 플러그인 미적용이면 실패(또는 `-PDAY_ALLOW_NO_PUSH=true` 일 때만 허용).

**W-6 · 소소한 것**
- `PushHub.dartReady` 는 메인에서 쓰고 FCM 스레드(`DayMessagingService.kt:18`)에서 읽는데 `@Volatile` 아님(`foreground` 만 volatile) — 늦게 보일 수 있음(결과는 알림이 하나 더 뜨는 정도).
- PendingIntent requestCode = `tag.hashCode()`(`PushHub.kt:102,117`) — 다른 tag 가 같은 해시면 `FLAG_UPDATE_CURRENT` 로 서로의 누름 칸을 덮음(확률 낮음).
- 작은 아이콘 = 런처 mipmap(`PushHub.kt:104,133`) — 상태 바에서 흰 네모 가능(F2 리포트 이슈 3 · 자산 필요).
- 채팅 tag = 메시지마다(`chat:{messageId}`) — iOS `thread-id` 묶음과 달리 대화방별로 쌓임(기능 차이 · 계약 위반 아님).
- `app/README.md` 「Android」 절의 푸시 = 스텁 서술 미갱신(F2 리포트 이슈 5).

## 남은 것(검수 범위 밖 · pending)

- 실기기 · 에뮬레이터 실푸시(F3 · A-50): 뒤/꺼짐에서 호출 취소가 원래 알림을 덮는지 · [수락] 결과 · 권한 거부 흐름 · W-1 경합 실물 확인.
