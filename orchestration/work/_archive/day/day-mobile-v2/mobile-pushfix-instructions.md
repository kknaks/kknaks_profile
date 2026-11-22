# [mobile] 푸시 고침 — 검수 WARN 6 (M3 iOS · F2 Android)

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` 그대로. 최신 커밋 b87925c6. ⚠ backend 가 `backend/` 고침 2 중 — 읽기만 · git 읽기만.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-push-report.md` W-1 ~ W-6 전부:
- W-1 iOS: 서버가 `apns-collapse-id`=callId 를 붙여 원장 호출 · 호출 취소 알림 identifier 가 같아졌다 → `willPresent` 지우기가 취소 알림 자신을 지울 수 있음(`AppDelegate.swift:121-124 · 170-178`) — 취소 알림은 남기고 원래만 지우게(또는 collapse 로 이미 덮였으면 지우지 않게)
- W-2 Android `AcceptReceiver` 가 SessionStore 직렬 실행기를 우회 — 같은 실행기로
- W-3 수락 결과 알림에 hospitalId 없음 → 누름이 버려짐(iOS · Android 둘 다)
- W-4 수락 타임아웃 20s+20s 가 receiver 창보다 김 — goAsync 창 안으로
- W-5 release 빌드가 `google-services.json` 없이 조용히 FCM 없이 나감 → release 빌드에서는 없으면 빌드 실패(debug 는 지금처럼 통과)
- W-6 작은 것: volatile · requestCode 해시 충돌 · **알림 작은 아이콘**(흰 단색 아이콘 — 기존 앱 아이콘 자산에서 만들 수 있으면 · 새 그림 짓지 마라 · 못 하면 리포트) · `app/README.md` Android 절(google-services 넣는 법 · 레포 밖 경로 `~/.config/day/android/` 만 · 값 없이)

검증 analyze · flutter test · Kotlin 단위 · Swift NativeLogicTests · build apk(debug json 유/무 · release json 무 = 실패 확인) · build ios --no-codesign 각 1회. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-pushfix-report.md`. 완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 금지.
