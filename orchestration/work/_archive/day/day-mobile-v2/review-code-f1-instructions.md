# [reviewer] 코드 검수 — backend F1 FCM(커밋 87cec04d)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(다른 워커 작업 중 — git 읽기만). 대상 = 커밋 `87cec04d`.
- 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-f1-instructions.md` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-f1-report.md`
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` §3 「Android 푸시 — FCM」 · OQ-A50 · A51 · A59 · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-000-data-model.md` device platform

## 볼 것
1. 기기 등록 android 규칙(push_env 없음 · 토큰 검사 · 허용 앱 id) · null push_env 잠금 키 — iOS 등록 회귀 없나
2. FCM 발송 — data 메시지 모양(앱 F2 가 이것으로 로컬 알림 · 채널 「원장 호출」 · 「채팅」 · 호출 취소 = 원장 호출 채널) · 키 없음 skipped · 죽은 토큰 · 재시도 · OAuth 토큰 캐시 · 키 내용 로그 노출 0
3. 원장 호출 · 호출 취소 · 채팅 세 갈래가 iOS 와 같은 받는 사람 · 같은 push_log
4. migration 0013 up/down · head
5. `/api/auth/device` web 400 · P2 시험 추가분
6. 관련 테스트 · ruff 1회

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-f1-report.md` · FAIL/WARN/PASS · 파일:줄. 수정 · 커밋 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
