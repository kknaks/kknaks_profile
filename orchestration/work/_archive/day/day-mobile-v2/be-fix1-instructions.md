# [backend] 고침 1 — P3 검수 WARN · 푸시 묶음 ID · 배포 비밀 목록

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-be-brief.md` 그대로. 최신 커밋 87cec04d(F1). ⚠ mobile 이 `app/` 작업 · reviewer 가 F1 을 읽는 중 — `app/` 금지 · git 읽기만.

1. **실제 버그**(`/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p3-report.md` ①): 호출 취소 뒤 늦게 도는 `call_push` 가 원래 원장 호출 푸시를 보내거나 닫힌 호출에 안 읽은 행을 쓸 수 있음(`services/notifications.py:454-545` · `:325-`) — 보내기 직전 호출이 닫혔으면 보내지 않고 행도 안 씀. 경쟁 시험.
2. **푸시 묶음**(코디 결정 · 사용자 통보): 원장 호출 푸시와 호출 취소 푸시에 같은 묶음 ID = callId — APNs `apns-collapse-id` · FCM 은 Android 알림 tag 로 쓰도록 data 에 같은 값(앱 F2 가 tag 로 씀). 취소 푸시가 OS 알림 센터에서 원래 호출 푸시를 덮게. 재호출은 새 callId.
3. P3 ③ JS 픽스처 NOTIFY_KIND 를 실제 배열로 · 취소 닫기 동작 시험(`controllers.test.mjs:50`) · ④ 재호출 뒤 취소 시험.
4. `scripts/deploy/configuration.py` OPTIONAL_SECRETS 에 `DAY_FCM_SERVICE_ACCOUNT` 한 줄(F1 리포트 — 안 넣으면 키가 서버에 안 감).

allowed_paths: `backend/day/services/notifications.py` · `services/notification_cancel.py` · `services/push.py` · `adapters/apns.py` · `adapters/fcm.py` · `backend/day/static/` 의 JS 시험 · 관련 테스트 · `scripts/deploy/configuration.py`(그 한 줄). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-fix1-report.md`. 검증 관련 테스트 · ruff 1회. 완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 금지.
