# 리뷰 리포트 — android-app mobile 5판(F1 + AND-7) / code (2026-11-14 · 3회차)

대상: HEAD `fa2f0d9f` 위 미커밋 변경. 수정 파일은 `app/.gitignore` · `app/README.md` · `app/lib/chat/screens/chat_room_screen.dart` · `app/lib/ui/theme.dart`, 새 파일은 `app/android/play_upload.py` · `app/test/ui/pane_bottom_inset_test.dart` 다. 코드는 읽고 시험만 했고, 수정 · 커밋은 하지 않았다.
근거: `e2e-feedback.md` F1(사용자 2026-11-13 「정석 = 하단 inset 만큼 비우기 · 채팅 입력창 · 시트 · 하단 버튼 **전수** · iOS 화면 불변」) · `app-5-report.md` · `review-code-2-report.md` W-1.

## 판정: WARN

FAIL 은 없다. 채팅 입력칸 수정 · iOS 불변 · 업로드 스크립트 · 비밀 0 · 관문 수치는 모두 맞다. 다만 F1 「전수」에 **Android 태블릿 스크롤 목록 끝**이 빠졌고, 워커 스크린샷 09 가 그 빠진 자리를 ✓ 로 적었다(W-1).

## 관문
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found (exit 0) |
| `fvm flutter test` | **+347 ~73 All tests passed** (exit 0 · 워커 수치와 같음 · 전 345 + 새 2) |
| `python3 play_upload.py tracks --package day.medisolveai.dev`(읽기) | internal `2 (0.1.0)` vc 2 completed · 나머지 트랙은 출시 없음 · `edit 삭제(ok)` · exit 0 · 키 · 토큰 출력 0 |

## WARN

### W-1 (중) F1 전수에서 빠진 자리 — Android 태블릿 레일 셸의 스크롤 목록 끝이 3버튼 내비 · 태스크바에 깔린다
- 위치:
  - `app/lib/ui/board_screen.dart:181` (`ListView.separated` padding `fromLTRB(side, 0, side, 24)`)
  - `app/lib/ui/board_screen.dart:195` (`SingleChildScrollView` 같은 값)
  - `app/lib/ui/shell.dart:425-426` (설정 탭 `ListView(padding: EdgeInsets.all(16))`)
- 원인: 태블릿 셸(`shell.dart:268-283`)은 본문에 `padding.bottom`(= 내비 높이)을 그대로 넘긴다. 그런데 이 목록들은 **padding 을 직접 지정**했다. Flutter `BoxScrollView` 는 padding 을 직접 주면 MediaQuery 안전 영역을 자동으로 더하지 않는다. 그래서 끝까지 스크롤해도 마지막 24/16dp 가 내비 바 밑에 있다. 폰은 탭바가 `removePadding` 하고 자기가 그 자리를 먹어서 문제가 없다. iPad 는 홈 인디케이터만 겹치므로 의도한 대로다.
- 증거: 워커 `app-5-shots/09-android-tablet-3btn-board-scrollend.png`. 맨 아래 카드(A-룸6 서서연)의 「얼굴필러…」 줄과 카드 아래 테두리가 내비 바(◀ ● ■) 밑으로 잘려 있다. 워커 표 「09 · 마지막 카드 … 내비 바 위 ✓」는 화면과 다르다.
- 대비되는 정상 자리: 채팅 목록 `chat_list_screen.dart:138` 은 padding 이 없어 자동 inset 이 붙는다(08 정상). 시트 · 통역 바 · 입력줄도 정상이다.
- 영향: 마지막 카드의 아래 일부가 보이지 않고, 그 자리는 시스템이 터치를 가져간다. 카드 위쪽은 눌리므로 기능이 막히지는 않는다. 사용자가 F1 에서 정한 「정석 = inset 만큼 비우기 · 전수」에는 어긋난다.
- 고칠 방향: 두 목록의 아래 padding 을 `24 + (paneReservesBottomInset ? MediaQuery.paddingOf(context).bottom : 0)` 로 바꾼다. 설정은 `16 + 같은 값` 이다. iOS 와 폰(탭바가 padding 을 0으로 만듦)은 값이 그대로다. 테스트는 기존 `pane_bottom_inset_test` 꼴로 「Android 태블릿 판 끝 카드 bottom ≤ 화면 높이 − 48」 하나를 더한다. Dart 변경이지만 F1 범위 안이다(사용자 OK 기록).

### W-2 (낮음) `play_upload.py` 트랙 인자에 제한이 없다 — 오타 · `production` 을 막지 않는다
- 위치: `app/android/play_upload.py:189` (`--track` 자유 문자열 · help 에는 production 도 나열)
- 근거: README 와 Delivery 범위는 개발 앱 internal · 정식 앱 alpha 뿐이다(`README.md` 「트랙」 줄). 그런데 `--track production` 을 주면 `status: completed` 로 그대로 commit 된다. 트랙 이름 오타는 Play 가 `tracks.update` 에서 오류를 낼 것으로 보지만 실제로 확인하지는 않았다(쓰기 금지). 오류가 나면 edit 이 지워져 남는 것은 없다.
- 고칠 방향: `choices=["internal","alpha"]` 로 막거나 production · beta 에 `--yes-production` 같은 확인 플래그를 둔다. package ↔ track 짝(`day.medisolveai.dev`→internal · `day.medisolveai`→alpha)을 검사하는 표 하나도 같이 둔다.

### W-3 (낮음) commit 뒤 트랙 다시 읽기가 실패하면 「실패」 exit 1 로 끝난다
- 위치: `play_upload.py:169-173`
- 근거: commit 이 끝난 뒤 두 번째 `Edit`(읽기)에서 네트워크 · HTTP 오류가 나면 `main` 이 「실패: …」 · exit 1 을 낸다. 운영자는 업로드가 안 된 줄 알고 다시 돌릴 수 있고, 그러면 같은 versionCode 라 Play 가 거절한다. 혼란만 생기고 해는 없다.
- 고칠 방향: 커밋 뒤 읽기는 try 로 감싸고 「commit ok · 트랙 읽기만 실패」로 exit 0 을 낸다.

## 확인 — 맞음(PASS 근거)

### 1. F1 수정 자리 · 키보드
- `chat_room_screen.dart:621` `_safeBottom` 은 `pane && !paneReservesBottomInset ? 0 : paddingOf.bottom` 이다. 비활성 안내 줄도 같은 getter 를 쓴다(워커 :732).
- 키보드가 두 번 비지 않는다. Flutter 는 키보드가 열리면 `padding.bottom = max(0, viewPadding − viewInsets)` = 0 이다. 태블릿 셸은 `removeViewInsets` 만 한다(`shell.dart:277-278`).
- 직접 grep 한 태블릿 하단 요소: 오른쪽 시트(`chat_info_screen.dart:98` · `chat_media_screen.dart:137` · `notification_screen.dart:150`)는 `SafeArea`. 새 대화(`chat_new_screen.dart:154` 의 태블릿 0)는 `showCenterPanel` Dialog(가운데 · 높이 0.8)라 바닥이 아니다. 원장 고르기 팝오버(`doctor_picker.dart:227` wide 0)는 `_Popover._place` 가 `pad.bottom` 을 빼고 배치한다(`:88-91`). 시술 방 통역 바는 `interpret_widgets.dart:101` 에서 `10 + paddingOf.bottom` 이다. 표 밖에서 새로 찾은 하단 **고정** 요소는 없고, 빠진 것은 W-1 스크롤 목록 끝뿐이다.

### 2. iOS 불변 · 테스트 배선
- `theme.dart` `paneReservesBottomInset = defaultTargetPlatform == android` 다. iOS/iPad 에서는 false 라 `pane ? 0` 이 그대로이고, 폰은 `pane == false` 라 분기를 타지 않아 값이 바뀌지 않는다. 워커 iPhone/iPad 전후 픽셀 비교(동일)도 이와 맞다.
- `pane_bottom_inset_test.dart` 는 실제 앱 배선 `Harness().start` → `toChat` → 방 탭 → `ChatRoomView` 를 지나 `chat-input` Rect 를 잰다(가짜 위젯 아님). 아이패드: Android − iOS = 48 · iOS < 48. 폰: 두 플랫폼 같음 · ≥ 48.
- 작은 흠: 중간 expect 가 실패하면 `debugDefaultTargetPlatformOverride` 가 리셋되지 않아 2차 오류가 함께 난다. `addTearDown` 으로 리셋하는 편이 안전하다(통과에는 영향 없음).

### 3. `play_upload.py`
- **실패 시 edit 삭제**: `Edit.__exit__`(`:99-102`)는 commit 되지 않은 edit 을 예외든 dry-run 이든 지운다. commit 이 실패하면 `closed=False` 라 지워진다. `--expect-version-code` 불일치(`:160-161`)도 PlayError → 삭제다.
- **dry-run**: validate 뒤 return → `__exit__` 에서 삭제한다. 트랙 · 출시는 남지 않는다. 다만 dry-run 중 `bundles.upload` 한 AAB 가 Play 「App bundle explorer」 라이브러리에 남는지는 **확인 안 됨**이다(Play 문서 미확인). 워커가 dev vc 2 를 dry-run 한 뒤 실제 업로드 vc 2 가 받아졌으므로, 적어도 versionCode 를 소모하지는 않는다.
- **키 · 토큰 출력 0**: 오류 문구는 HTTP 상태 + Google `status/message` 뿐이다(`:63` · `:67-74` · `:92`). 네트워크 오류는 예외 타입 이름만 낸다(`:206-207`). 키 읽기 실패는 경로 + 예외 타입이다(`:51`). PEM 파싱 실패(`:55`)는 try 밖이라 traceback 이 나지만, 파이썬 traceback 은 지역 값을 출력하지 않아 키 본문은 나가지 않는다. 실행 확인: 잘못된 키 경로 → 「서비스 계정 키를 읽지 못함: /nonexistent (FileNotFoundError)」.
- **패키지 오타**: `--package day.medisolveai.devx` → 「edits.insert 실패: HTTP 404 NOT_FOUND Package not found」 · edit 이 만들어지지 않아 남는 것 0(실행 확인).
- AAB 경로가 없으면 edit 을 만들기 전에 멈춘다(실행 확인).

### 4. W-1(2회차) · `.gitignore` · git status
- `app/.gitignore` 가 `app/` 아래 어디서든 `*.jks` · `*.keystore` · `*.p12` · `*.aab` · `upload-key.properties` · `play-service-account*.json` 을 막는다. check-ignore 로 `app/x.jks` · `app/android/x.keystore` · `app/y.p12` · `app/z.aab` · `app/lib/x.aab` · `app/upload-key.properties` · `app/play-service-account.json` · `app/android/play-service-account-dev.json` 모두 ignored 를 확인했다.
- 남은 틈(참고): 레포 루트(`x.jks` · `x.aab` · `play-service-account.json`)와 이름이 다른 서비스 계정 파일(`app/android/sa.json`)은 NOT ignored 다. 키는 원래 `~/.config/day/android/` 에 있으니 위험은 낮다.
- `git status --untracked-files=all` 은 위 6개 파일뿐이고 비밀 파일은 0이다.
- 로컬 권한: `~/.config/day/android/` 700 · `play-service-account.json` · `upload-key.properties` · `upload-keystore.jks` 600 · `out/` 700. `store/`(스토어 그래픽 · 스크린샷 PNG)는 755/644 인데 비밀이 아니다.

### 5. 비밀 grep (값 비교 · 출력 없음)
- 비교한 값: 서비스 계정 `private_key_id` · `client_email` · `client_id` · 키 본문 줄, 업로드 키 properties 값, `~/.config/day/*` 파일(dev 로그인 · infra · prod 값)의 6자 이상 값 62개.
- 대상: `git diff` + 새 파일 2개 → 걸린 것은 `theme.dart` 1행 **기존 문맥 줄**의 공개 브랜드 단어 하나뿐이다(이미 HEAD 에 있음 · 비밀 아님). 비밀 0.
- 워커 리포트 `app-5-report.md` 에서는 공개 도메인 3개(dev · prod 공개 주소)만 걸렸다. 계정 · 비밀번호 · 키는 0이다.

## 고칠 것 목록
| # | 심각도 | 무엇 | 언제 |
|---|---|---|---|
| W-1 | 중 | Android 태블릿 판 목록(`board_screen.dart:181` · `:195`) · 설정 목록(`shell.dart:426`) 아래에 `paddingOf.bottom` 을 더한다(Android 만) · 테스트 1 · 스크린샷 09 다시 찍기 | 정식 앱 alpha 실제 업로드 **전**에 권장(같은 빌드 번호를 쓰면 다시 빌드) |
| W-2 | 낮음 | `play_upload.py --track` choices · production 확인 · package↔track 짝 검사 | 다음 업로드 전 |
| W-3 | 낮음 | commit 뒤 트랙 읽기 실패 → exit 0 + 안내 | 아무 때 |
| 참고 | 낮음 | 테스트 `debugDefaultTargetPlatformOverride` 를 `addTearDown` 으로 리셋 · 루트 `.gitignore` 보강 | 아무 때 |

## 사용자가 실물에서 만날 자리
- Fold3 펼침 · 3버튼: 채팅 「메시지 입력」은 바 위로 올라온다(08). 다만 **시술현황 판을 끝까지 내리면 마지막 카드 아래가 바 밑에 잘린다**(09 · W-1). 설정 탭도 목록이 길면 같다.
- 접은 화면(폰)은 그대로다(탭바가 inset 을 먹음).
