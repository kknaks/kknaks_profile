# [mobile] 1판 리뷰 반영 (짧음)

같은 역할 · 같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app` · 커밋 금지 그대로.
리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/review-code-1-report.md`

1. **W-1** `app/android/.gitignore` 에 `/build/` 추가 → `git ls-files --others --exclude-standard app/android` 에 build 산출물 0 확인.
2. **W-4** `SessionChannel.kt` `run` 에서 work 를 `runCatching` 으로 감싸 실패해도 답이 반드시 돌아오게(load → null · save → `keychain_save_failed` 와 같은 길 또는 false — iOS 와 맞는 쪽 · clear/clearIf → null). 동작 계약 불변.
3. W-2(사진 권한) · W-3(rebase)은 하지 마라 — 코디 · 사용자 몫.
4. 검증: `fvm flutter analyze` · `fvm flutter build apk --debug`(1판과 같은 인자) 각 1회. 에뮬레이터 재확인 불필요.

리포트 `app-2-report.md`(같은 폴더 · 짧게). 완료 보고는 1판 브리프 §9 두 명령(새 preamble 의 taskId · dispatchId).
