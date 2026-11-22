# [reviewer] 코드 검수 — 앱 푸시: M3 iOS 호출 취소 알림(ecea81d4) + F2 Android FCM(b87925c6)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(backend 가 고침 2 작업 중 — git 읽기만). 대상 = 커밋 `ecea81d4` · `b87925c6`.
- 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m3-instructions.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-f2-instructions.md` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m3-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-f2-report.md`
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` U-14 · §3 푸시 · 「Android 푸시 — FCM」 · OQ-A59 · A60 · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-005-notifications.md` 2026-11-20 개정
- 서버 사실: `backend/day/adapters/fcm.py` · `services/push.py` · `adapters/apns.py`(apns-collapse-id) · 결정: Android tag = data.callId

## 볼 것
1. iOS · Android 같은 동작 — 원장 호출 [수락] · 누름 → 룸 상세 · 채팅 · 호출 취소(원래 알림 덮기/지우기) · 앞/뒤/꺼짐 상태별
2. FCM data 칸 이름이 서버와 맞나 · 채널 이름 = 앱 글자 · Android 13+ 권한 · 토큰 갱신 → 재등록
3. [수락] 이 엔진 없이 저장 세션으로 서버 호출 — 세션 만료 · 환경(dev/prod) · 병원 확인이 iOS 와 같나 · 비밀값 로그 노출 0
4. `google-services.json` 커밋 안 됨 · 없으면 푸시 없이 빌드 · 플러그인 조건
5. M3 의 `NativeLogicTests/main.swift` 범위 밖 수정 타당성
6. `flutter analyze` · 관련 `flutter test` · Kotlin 단위 시험 1회

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-push-report.md` · FAIL/WARN/PASS · 파일:줄. 수정 · 커밋 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
