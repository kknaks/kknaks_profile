# [mobile] 6판 — review-code-3 WARN 반영 · 빌드 3

같은 역할 · 같은 워크트리(5판 미커밋 변경 위에 이어서). 커밋 · push 금지 그대로.
근거: 이 폴더의 `review-code-3-report.md`(W-1 · W-2 · W-3 · 참고) · `app-5-instructions.md`(규칙 그대로 — 시작/끝 dev 확인 · iOS 불변 · 사진 줄 유지 · 사용자 기기 · 프로세스 손대지 않기).

## 할 것
1. **W-1(중)** — Android 태블릿(레일 셸)에서 padding 을 직접 준 스크롤 목록 끝이 내비 밑에 깔림. 리뷰가 찾은 `board_screen.dart:181` · `:195` · `shell.dart:426` 만이 아니라 **`app/lib` 에서 `padding:` 을 직접 준 ListView · GridView · SingleChildScrollView · CustomScrollView 를 전부 grep** 해서 태블릿 본문(셸이 padding.bottom 을 넘기는 자리)에 놓이는 것을 센다. 표(파일:줄 · 고침 여부)를 리포트에. 고침 = 아래 padding 에 `paneReservesBottomInset ? paddingOf.bottom : 0` 더하기(iOS · 폰 값 불변).
   - 테스트 1+(기존 `pane_bottom_inset_test` 꼴 · Android 태블릿 판 끝 카드가 하단 inset 위).
   - 같은 테스트의 `debugDefaultTargetPlatformOverride` 는 `addTearDown` 으로 리셋.
   - 스크린샷: Android 태블릿 3버튼 판 끝 · 설정 끝(전/후) · iOS iPad 판 끝 전/후 픽셀 비교. `app-6-shots/`.
2. **W-2** — `play_upload.py`: `--track` 은 `internal` · `alpha` 만 허용, package↔track 짝 검사(`day.medisolveai.dev`→internal · `day.medisolveai`→alpha). 그 밖은 멈춤.
3. **W-3** — commit 뒤 트랙 다시 읽기 실패는 「commit ok · 읽기만 실패」 exit 0.
4. 참고: 루트 `.gitignore` 에도 `*.jks` · `*.aab` · `play-service-account*.json` 같은 패턴이 없으면 더하기(레포 관례 보고).
5. analyze · test.
6. **빌드 3**(versionCode 3 · 0.1.0) 개발 · 정식 둘 다 → `~/.config/day/android/out/DAY-Dev-0.1.0-3.aab` · `DAY-0.1.0-3.aab`(600 · 지문 · vc 확인).
7. 업로드: **개발 앱 internal 실제**(출시명 `3 (0.1.0)` · 노트 「하단 내비게이션 바가 입력창과 목록 끝을 가리던 문제 수정」) · **정식 alpha 는 dry-run 만**.

## 산출물
`app-6-report.md` — 전수 표 · 변경 파일 · 스크린샷 · 수치 · 업로드 결과 · 비밀 grep 0. 완료 보고는 1판 브리프 §9 두 명령(새 preamble 값).
