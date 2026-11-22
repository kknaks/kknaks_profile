# [mobile] F2 — Android 푸시(FCM) 앱 쪽

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` 그대로. 서버 F1 커밋 `87cec04d`(`backend/day/adapters/fcm.py` · `services/push.py` — data 메시지 모양). ⚠ backend 가 `backend/` 고침 작업 중(푸시 묶음 ID = callId 를 FCM data 에 넣는 중 — 같은 키 이름은 커밋 뒤 확인) · reviewer 가 F1 을 읽는 중 — `backend/` 읽기만 · git 읽기만. Delivery #263.

## 정본
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` §3 「Android 푸시 — FCM」 · 「Android 개발 앱 — 네이티브 채널」(`day/push` 스텁을 구현으로) · OQ-A59(data 메시지 · 앱 로컬 알림 · 채널 「원장 호출」(수락 액션) · 「채팅」 · 호출 취소 = 원장 호출 채널) · OQ-A60(`google-services.json` 없는 빌드)
- iOS 쪽 같은 동작(원장 호출 [수락] · 누르면 룸 상세 · 채팅 · 호출 취소면 같은 callId 알림을 지움/덮음) — `app/ios/Runner/AppDelegate.swift` · `AcceptLogic.swift` · `app/lib/state/push_coordinator.dart`
- Android 지금: `app/android/app/src/main/kotlin/day/medisolveai/PushChannel.kt`(스텁) · 세션 채널 구현 참고

## Firebase 파일
- `~/.config/day/android/google-services.json`(두 앱 다 들어 있음) — **레포에 커밋하지 마라.** 빌드 때만 `app/android/app/google-services.json` 으로 복사하고 `.gitignore` 에 있는지 확인(없으면 한 줄 더함). 파일이 없으면 푸시 없이 빌드되게(OQ-A60).

## 할 것
1. Gradle 에 Google 서비스 플러그인 · firebase-messaging · 알림 채널 2개(이름 = 앱 글자 「원장 호출」 · 「채팅」 — `app/lib/notify/notification_model.dart:16`)
2. `day/push` 채널 Android 구현: 토큰 얻기 · 갱신 → 서버 등록(`platform: android` · push_env 없음) · data 메시지 → 로컬 알림(원장 호출은 [수락] 액션 · iOS 와 같은 서버 호출) · 누르면 iOS 와 같은 경로 · 호출 취소면 같은 callId 알림을 tag 로 덮음 · Android 13+ 알림 권한
3. 테스트 · `flutter analyze` · `flutter test` · **`flutter build apk --debug`**(google-services 복사 상태 · 없는 상태 둘 다) · `flutter build ios --no-codesign` 1회
4. 실기기 · 에뮬레이터 실푸시는 pending 가능(사용자 F3). 에뮬레이터를 띄워도 되나 사용자 에뮬레이터 · 기기는 건드리지 마라.

## allowed_paths
`app/android/` · `app/lib/`(푸시 · 기기 등록 부분) · `app/test/` · `.gitignore`(그 한 줄) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-f2-report.md`

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 금지.
