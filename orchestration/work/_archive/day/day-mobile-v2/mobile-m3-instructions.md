# [mobile] M3 — 앱 호출 취소 알림(doctor_call_cancel) · 푸시 누르기 · 원래 푸시 지우기 (iOS)

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` 의 역할 · 규칙 · 검증 · 금지 그대로. 커밋됨: M2 b91d2fca · 서버 P3 9162ee18. ⚠ backend 가 `backend/` 에서 F1(FCM) 작업 중 · reviewer 가 M2 · P3 를 읽는 중 — `backend/` 읽기만 · git 읽기만(커밋은 코디). **Android 푸시(FCM)는 이번 아님**(F2 따로 · 서버 F1 뒤).

## 정본
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` U-14(알림) 보강 · §3 「호출 취소 푸시」(:447 근처) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-005-notifications.md` 2026-11-20 개정(OQ-N15 ~ N18)
- 서버 사실 커밋 `9162ee18`(`services/notification_cancel.py` · `services/notifications.py` 목록 · unread · APNs payload) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p3-report.md`
- 앱 코드 지도: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/research-current-state.md` A2 #8 ~ #10 · D2 — `app/lib/notify/notification_model.dart:13,16` · `app/lib/state/push_coordinator.dart:200-205` · `app/ios/Runner/AppDelegate.swift:109-130` · `AcceptLogic.swift:149-168`(tapKeys)

## 할 것
1. 알림 목록 · 종 배지에 `doctor_call_cancel` 을 그린다(제목 · 본문은 서버 행 그대로 — 글자 짓지 마라). 알림 설정 줄은 스펙대로(원장 호출 설정이 그대로 덮는지 스펙 확인 · 없으면 새 줄 안 만듦).
2. 푸시 누르면 원장 호출 푸시와 같이 그 방문 룸 상세(카드 없으면 같은 토스트) · [수락] 액션 없음.
3. 호출 취소 푸시를 받으면 OS 알림 센터에 남은 그 호출의 원장 호출 푸시를 지운다(iOS — `callId` 기준 · OQ-N17).
4. 테스트 · `flutter analyze` · `flutter test` · `flutter build ios --no-codesign` 1회씩 · iOS 네이티브 바뀌면 그 빌드로 확인.

## allowed_paths
- `app/lib/notify/` · `app/lib/state/push_coordinator.dart` · 알림 관련 `app/lib/ui/` · `app/ios/Runner/`(푸시 처리 부분만) · `app/test/`
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m3-report.md`

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 · push · PR 금지.
