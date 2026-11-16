# 리뷰 리포트 — android-app mobile 6판(review-code-3 W-1~3 반영) / code (2026-11-14 · 4회차)

대상: HEAD `fa2f0d9f` 위의 미커밋 변경 전체다(5판 + 6판). 바뀐 파일은 `.gitignore`(루트) · `app/.gitignore` · `app/README.md` · `app/lib/{ui/theme.dart, ui/board_screen.dart, ui/shell.dart, ui/chart_sheet.dart, chat/screens/chat_room_screen.dart}` 이고, 새 파일은 `app/android/play_upload.py` · `app/test/ui/pane_bottom_inset_test.dart` 다. 코드는 읽고 시험만 했고 수정 · 커밋은 하지 않았다.

## 판정: PASS

3회차 W-1~3 은 모두 해소됐다. 새 FAIL · WARN 은 없고 참고 2건만 있다.

## 관문
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found (exit 0) |
| `fvm flutter test` | **+355 ~73 All tests passed** (exit 0 · 워커 수치와 같음 · 347 − 옛 2 + 새 10) |
| `python3 play_upload.py tracks --package day.medisolveai`(읽기) | alpha `1 (0.1.0)` vc 1 completed 그대로 · `edit 삭제(ok)` · 키 · 토큰 출력 0 |

## 1. W-1 — 해소

### 전수 재집계
`app/lib` 를 직접 grep 했다(`ListView` · `GridView` · `SingleChildScrollView` · `CustomScrollView` · `SliverPadding` · `ReorderableListView` · `PageView`). 25자리가 나왔고, 워커 표가 모두 덮는다. 표는 `doctor_picker` 3개를 한 줄로, `room_screen` 2개를 한 줄로 묶었다. 표 밖에서 바닥에 닿으면서 padding 을 직접 지정한 목록은 없다.
- 바닥에 닿는 목록의 판정:
  - padding 없음 → Flutter 가 안전 영역을 자동으로 더한다: `chat_list_screen.dart:138` · `notification_screen.dart:142`(SafeArea 안).
  - 폰 / 시트 분기가 있는 목록: `chat_new_screen.dart:152` · `chat_info_screen.dart:103` · `chat_media_screen.dart:155`.
  - 아래에 고정 줄이 있는 목록: `room_screen.dart:173/179` → 통역 바 · `chat_room_screen.dart:254` → 입력줄 · `interpret_widgets.dart:349` → 마이크 줄 · `doctor_picker.dart:258-262` → [호출] 줄.
  - 남은 3자리(판 격자 · 설정 · 차트 시트)는 이번에 고쳤다.

### `listEndInset` 값 (`theme.dart`)
`paneReservesBottomInset ? paddingOf.bottom : 0` 이다.
- **iOS 는 늘 0** 이라 iOS 화면은 바뀌지 않는다.
- 폰 탭 화면 판 목록(`board_screen.dart:181`) · 설정(`shell.dart:426`)은 Android 여도 셸이 `removePadding(removeBottom)` 을 한다(`shell.dart:304` · 탭이 있을 때). 그래서 `paddingOf.bottom = 0` 이고, 탭바가 그 자리를 먹는다 → 값 불변. 테스트 「설정 목록 끝 — 폰 = 16(두 플랫폼)」이 이를 확인한다.
- 이중 여백은 없다. 태블릿 본문은 셸이 padding 을 그대로 넘기고 이 목록들은 padding 을 직접 지정하므로, 자동 inset 이 붙지 않은 상태에서 한 번만 더해진다.

### `chart_sheet.dart` 추가 고침 — 맞음
폰 경로는 `showModalBottomSheet(useSafeArea: true)`(`chart_sheet.dart:26-32` · heightFactor 0.8 · 화면 바닥에 붙음)다. Flutter 3.44.8 `bottom_sheet.dart:1167-1168` 을 보면 `useSafeArea` 는 `SafeArea(bottom: false)` 라 아래 안전 영역이 내용으로 남는다. 그래서 padding 을 직접 준 `_notes` 목록 끝은 Android 내비 바 밑에 깔린다. 고친 식 `16 + (isTablet ? 0 : listEndInset)` 이 맞다. 태블릿은 가운데 Dialog(`:16-20`)라 0 이다.
- iPhone 차트 시트 끝은 원래대로 홈 인디케이터에 겹친다. iOS 불변 원칙대로이고 이번 범위 밖이다.

### 새 테스트 — 실제 배선을 지난다
`pane_bottom_inset_test.dart` 의 5개 테스트 × `TargetPlatformVariant{android, iOS}` 는 모두 `Harness().start` 로 실제 앱 셸을 띄운다. 판은 `snapshot` 카드 24장 → `card-grid` Scrollable 을 끝까지 `jumpTo` → 마지막 카드 Rect 를 잰다. 설정은 `nav-settings` 를 탭 → `SettingsBody` 안 `ListView.padding` 을 본다. 입력칸은 실제 채팅방 진입이다.
- 기대값이 정확하다. 판 끝 gap 은 Android 24+48 · iOS 24, 설정은 태블릿 Android 64 · iOS 16 · 폰 16.
- 워커는 `listEndInset → 0` 변이로 2개가 실패하는 것도 확인했다(테스트가 실제로 잡는다는 근거).
- Variant 로 바꾼 이유(addTearDown 이 foundation debug 변수 검사보다 늦음)는 Flutter 동작과 맞다. 3회차 참고 「2차 오류」도 해소됐다.

### 스크린샷 02 — 맞음
`app-6-shots/02-android-tablet-3btn-board-end-AFTER.png` 에서 A-룸6 카드 전체(아래 테두리 포함)가 태스크바 · 3버튼 위에 있고 아래 여백도 보인다. 01(전)과 비교하면 고쳐진 것이 분명하다.

## 2. W-2 · W-3 — 해소 (오프라인 실행 확인 · Play 쓰기 없음)

| 인자(`--key /nonexistent`) | 결과 |
|---|---|
| dev · production | rc 2 `invalid choice: 'production' (choose from alpha, internal)` |
| prod · internal | rc 1 `day.medisolveai 는 alpha 트랙에만 올린다` |
| dev · alpha | rc 1 `day.medisolveai.dev 는 internal 트랙에만 올린다` |
| com.other · internal | rc 1 `올릴 수 없는 패키지` |
| dev · internal | 짝 검사 통과 → 키 읽기 실패 rc 1 (`check_target` 이 키 · 네트워크보다 먼저 돈다 — `play_upload.py:220`) |

- choices 는 짝 표 값에서 만든다(`:206` · `UPLOAD_TRACKS` `:38`). 짝 검사는 `:156-161` 이다.
- W-3(`:183-190`): commit 뒤 다시 읽기를 `try` 로 감쌌다. PlayError · RequestException 이면 「edits.commit ok · 트랙 다시 읽기만 실패(HTTP 상태/예외 타입) — 다시 올리지 말고 `tracks` 로 확인」을 내고 정상 반환해 exit 0 이다. 출력에는 HTTP 상태 · Google 문구 · 예외 이름만 있다(키 · 토큰 0).
- README 트랙 줄에 「두 짝만 받는다」 한 문장이 더해졌고, 실제 동작과 같다.

## 3. 루트 `.gitignore` — 이미 추적 중인 파일을 숨기지 않음
- `git ls-files -ci --exclude-standard` = **0건**.
- check-ignore 결과:
  - 루트 `x.jks` · `y.keystore` · `z.p12` · `x.aab` · `upload-key.properties` · `play-service-account.json` · `backend/play-service-account-x.json` → ignored.
  - `app/android/play_upload.py` · `deploy/config/dev.env` → 추적 유지.
- `git status --untracked-files=all` 은 위 대상 파일뿐이고 비밀 파일은 0이다.

## 4. 비밀 grep (값 비교 · 출력 없음)
- 비교한 값 80개: 서비스 계정 `private_key_id` · `client_email` · `client_id` · 키 본문 줄, 업로드 키 properties 값, `~/.config/day/*` 파일 값(dev 로그인 · infra · prod 값).
- 대상: `git diff` + 새 파일 2개 + 워커 `app-6-report.md`.
- 걸린 것은 `theme.dart` 머리 주석의 **기존 문맥 줄**(HEAD 에 이미 있는 공개 브랜드 단어) 1건뿐이다. 비밀 0.

## 참고 (막는 사유 아님)
1. iPhone 하단 시트 중 padding 을 직접 준 목록(차트 시트 `_notes`)은 홈 인디케이터에 조금 겹친다. 원래 그랬고, iOS 불변 원칙이라 이번에 바꾸지 않았다. iOS 를 손볼 기회가 생기면 같은 식으로 맞출 수 있다.
2. 정식 앱 alpha 는 지금 vc 1 이다. 다음 실제 업로드는 vc 3 AAB(`DAY-0.1.0-3.aab`)이고, 정식 앱에 vc 2 를 건너뛰는 것은 문제없다(Play 는 더 큰 versionCode 만 요구). 실제 업로드는 코디네이터 지시 뒤에 한다.

## 사용자가 실물에서 만날 자리
- Fold3 펼침(3버튼 + 태스크바)에서 채팅 입력칸 · 시술현황 판 마지막 카드 · (길면) 설정 끝이 바 위에 있다. 접은 폰 화면은 그대로다.
- Android 폰 차트 시트 끝도 내비 바 위로 올라온다.
- iPhone · iPad 화면은 바뀌지 않는다(워커 iPad 전후 픽셀 동일 · 테스트 iOS 값 그대로).
