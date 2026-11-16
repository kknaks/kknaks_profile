# [reviewer] 2회차 — AND-5 release 서명 검수 (짧음)

같은 역할 · read-only · 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app`. 대상 = 커밋 `e13ea876..HEAD`(AND-5 서명 커밋 하나). 맥락: 이 폴더의 `app-3-instructions.md` · `app-3-report.md` · 네 `review-code-1-report.md`.

볼 것: ① release 가 debug 키 · 무서명으로 나가는 길 0(코드로) ② 키 경로 주입 우선순위(-P > identity.local.properties) · 값이 저장소에 0 ③ `.gitignore` 패턴이 키 · properties · aab 를 다 막는지(`git check-ignore`) ④ debug · flutter run 영향 없음 ⑤ README 변경이 추가 + 자기 줄 1개 수정뿐 ⑥ `~/.config/day/android/` 파일 권한 600/700(값은 열지 마라).
관문 1회: `fvm flutter analyze`. 빌드 재실행은 필요 없으면 생략(키 경로 없이 `build apk --release` 가 멈추는지 1회는 해도 좋다).

리포트 `review-code-2-report.md`(같은 폴더 · 짧게 · PASS/WARN/FAIL). 완료 보고는 1회차 브리프 §9 두 명령(새 preamble 의 taskId · dispatchId).
