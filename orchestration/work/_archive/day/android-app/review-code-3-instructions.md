# [reviewer] 3회 — mobile 5판(F1 + AND-7) 코드 검수

같은 역할 · 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app`(HEAD `fa2f0d9f` 위 **미커밋** 변경). 읽기 · 시험만 — 코드 수정 · 커밋 금지.
맥락(이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`): `app-5-instructions.md`(발주) · `app-5-report.md`(워커 보고) · `app-5-shots/` · `e2e-feedback.md` F1 · `review-code-2-report.md`(W-1).

## 볼 것

1. **F1 범위 누락** — 워커 전수조사 표를 믿지 말고 `app/lib` 를 직접 grep 해서 화면 하단에 붙는 요소가 표 밖에 있는지 센다. 특히 태블릿(레일 셸 · 짧은 변 ≥ 600) 쪽 하단 요소 · 키보드 열림 때 두 번 비는지.
2. **iOS 불변** — `paneReservesBottomInset` 분기가 iOS · iPad 값(0)을 그대로 두는지 · 폰 경로 무변경인지. 새 테스트(`test/ui/pane_bottom_inset_test.dart`)가 실제 앱 배선을 지나는지(가짜 위젯만 재는지).
3. **`app/android/play_upload.py`** — 실패 시 edit 삭제 · dry-run 이 Play 에 남기는 것 0 · 키/토큰 출력 0(오류 경로 포함) · `--expect-version-code` · 트랙/패키지 인자 오타 시 동작. 실제 Play 쓰기는 하지 마라(읽기 `tracks` 명령은 해도 됨).
4. **W-1** `app/.gitignore` 패턴 · `git check-ignore` 로 키 · aab · 서비스 계정 파일이 무시되는지 · `git status` 에 비밀 파일 0.
5. 비밀 grep(키 · 업로드 키 비밀번호 · dev 계정 값 — `~/.config/day/` 의 값과 비교하되 출력 금지).
6. `fvm flutter analyze` · `fvm flutter test` 수치.

## 산출물

`review-code-3-report.md`(같은 폴더) — PASS / WARN / FAIL · 항목별 근거(파일:줄) · 고칠 것 목록(심각도).
완료 보고는 1판 리뷰 브리프(`android-app-review-brief.md`) 의 완료 보고 두 명령(새 preamble 의 taskId · dispatchId).
