# day-mobile-v2 푸시 고침 결과 보고 — 검수 W-1 ~ W-6 (M3 iOS · F2 Android)

## 상태: done (커밋 · push · PR 없음 · 실기기 · 에뮬레이터 실푸시 = pending(F3 · A-50))

base = `b87925c6`. `backend/**` 읽기만.

## 항목별

| 검수 | 고친 것 | 파일 |
|---|---|---|
| **W-1** iOS 취소 알림이 자기 자신을 지울 수 있음(서버 `apns-collapse-id = callId` 뒤) | `PushPayload.callsToClear` 가 **요청 id = callId 인 것(collapse 묶음 — OS 가 이미 취소로 대체)** 과 **취소 알림과 같은 id** 는 지우지 않는다. 지우는 것은 collapse 없이 온 옛 원장 호출 알림만. `willPresent` · 누름 · 앞으로 옴의 부르는 자리는 그대로(이제 안전) | `app/ios/Runner/AcceptLogic.swift` |
| **W-2** Android `AcceptReceiver` 가 세션 저장소 직렬 실행기 우회 | `SessionStore.sync(fallback) { … }` — 같은 단일 스레드 실행기에 넣고 기다림. 리시버의 `loadRaw` · `clearIf`(만료 · 401) 모두 이것으로 → 읽고 비교하고 지우기 사이에 Dart 새 로그인 저장이 못 끼어든다 | `…/SessionChannel.kt` · `…/AcceptReceiver.kt` |
| **W-3** [수락] 결과 알림에 hospitalId 없어 누름이 버려짐(iOS · Android) | 결과 알림 누름 칸 = 원래 알림의 `kind(doctor_call)` · `environment` · `hospitalId` · `visitId` · `callId` — iOS `PushPayload.resultInfo` · Android `PushLogic.resultTap`. Dart 쪽은 그대로(병원 일치 → 그 방문 · callId 읽음) | `AcceptLogic.swift` · `AppDelegate.swift`(AcceptAction) · `PushLogic.kt` · `PushHub.kt`(Notifier.result) · `AcceptReceiver.kt` |
| **W-4** [수락] 요청 상한 20+20초 > 리시버 창 | 연결 4초 + 읽기 5초 = 9초(< 앞 창 10초) · 실패 글자는 기존 「서버에 연결할 수 없어요」 | `AcceptReceiver.kt` |
| **W-5** release 가 json 없이 조용히 FCM 없이 나감 | `:app:preReleaseBuild` 에서 Firebase 플러그인이 안 걸렸으면 **오류로 멈춤**(업로드 키 검사보다 먼저 돎) · debug · profile 은 그대로 통과 · 일부러 푸시 없는 release = `-PDAY_ALLOW_NO_PUSH=true` | `app/android/app/build.gradle.kts` |
| **W-6** volatile | `PushHub.dartReady` `@Volatile` | `PushHub.kt` |
| **W-6** requestCode 해시 충돌 | `tag.hashCode()` → 앱 전용 저장소의 늘어나는 번호(`Notifier.nextRequestCode` · 프로세스가 다시 떠도 안 겹침) | `PushHub.kt` |
| **W-6** 알림 작은 아이콘 | 새 `res/drawable/ic_stat_day.xml` — **앱 아이콘 `assets/brand/app-icon.svg` 의 모양 path 그대로**(흰색 · 바탕 없음 · 새 그림 아님) · 두 알림 모두 이것 | `res/drawable/ic_stat_day.xml` · `PushHub.kt` |
| **W-6** README | `app/README.md` 「Android」 표의 `day/push` = 구현 · 권한 줄에 알림 · 새 절 「Android 푸시(FCM)」(복사 방법 · 레포 밖 경로 `~/.config/day/android/` 만 · 값 없음 · debug/release 차이 · 단위 시험 명령) | `app/README.md` |
| (덤) 채팅 tag = 메시지마다 | 그대로 — 검수도 「기능 차이 · 계약 위반 아님」 | — |

## 테스트 추가
- Swift `ios/NativeLogicTests/main.swift` — collapse id(= callId) 안 지움 · 옛 것만 지움 · 취소와 같은 id 안 지움 · 결과 칸에 병원 · 호출(3건)
- Kotlin `PushLogicTest.kt` — 결과 누름 칸 · 요청 상한 < 10초(2건 · 총 8)
- Dart `push_coordinator_test.dart` — 결과 알림 누름: 병원 있으면 그 방문 + callId 읽음 · 옛(병원 없음)은 버림(1건)

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+415 ~81 All tests passed**(새 1) |
| Kotlin `./gradlew :app:testDebugUnitTest`(JDK 17) | **8 tests · 0 failures** |
| Swift `sh app/tool/native_logic_test.sh` | **ALL PASS**(새 3) |
| `build apk --debug` · json **없음** | ✓ 성공(푸시 없이) |
| `build apk --debug` · json **복사** · `day.medisolveai.dev` | ✓ 성공 · `google_app_id` 생성 확인 |
| `build apk --release` · json **없음** | ✗ **의도대로 실패** — 「release 빌드에 Firebase 설정이 없습니다 — …」 |
| (덤) `build apk --release` · json 복사 · dev 식별자 | ✗ 업로드 키 검사에서 멈춤 — Firebase 검사는 통과(업로드 키는 로컬에 없음 · 정상) |
| `fvm flutter build ios --no-codesign` | ✓ `Runner.app` (20.8MB) |

복사한 `google-services.json` 은 빌드 뒤 지웠다. 내 빌드 산출물 `app/build` 는 iOS 빌드 전에 지웠다(디스크).

## 코디가 볼 것
1. W-1 실물(앞에서 받은 취소 배너가 알림 센터에 남는지) · W-3 실물(결과 알림 누름 → 룸 상세)은 A-50 실기기에서.
2. 작은 아이콘은 앱 아이콘 모양을 단색으로 쓴 것 — 별도 알림 아이콘 시안이 생기면 그 파일만 바꾸면 된다.
3. 이번 범위에서 `app/ios/NativeLogicTests/` · `app/README.md` 를 고쳤다(브리프 W-6 · 검증 목록이 요구).
