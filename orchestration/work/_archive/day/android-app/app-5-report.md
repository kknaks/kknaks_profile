# android-app 5판 — F1(하단 시스템 바 가림) + AND-7(Play API 업로드) · 빌드 2 결과 보고

## 상태: done — 미커밋(HEAD `fa2f0d9f` 위)

## 0. dev 최신 확인
| 시점 | `git fetch origin` → `git log --oneline HEAD..origin/dev` |
|---|---|
| 시작 | 0건 — rebase 안 함 |
| 보고 직전 | 0건 |

## A. F1

### 원인
폰은 이미 맞다. 탭바는 `mq.padding.bottom` 을 먹고, 탭바를 숨긴 대화 화면은 셸이 아래 안전 영역을 넘겨 입력줄이 그만큼 띄운다. 시트는 `SafeArea(top:false)` 를 쓴다.
**태블릿 폭(짧은 변 ≥ 600 — Fold3 펼침)** 은 레일 셸이고 채팅 대화가 오른쪽 칸(`ChatRoomView(pane: true)`)이다.
여기서 `_safeBottom` 이 `pane ? 0` 이라 아래 안전 영역을 비우지 않았다. 아이패드는 홈 인디케이터가 내용 위에 겹쳐 그려져도 되는 자리라 의도된 0 이었다.
Android(targetSdk 36 edge-to-edge)에서는 3버튼 내비 · 태스크바가 그 자리를 덮고, 터치도 시스템이 가져간다 → 입력칸이 깔림.

### 전수조사(`app/lib` grep: bottomNavigationBar · bottomSheet · showModalBottomSheet · Positioned bottom · Alignment.bottom · SafeArea · MediaQuery padding/viewPadding/viewInsets · resizeToAvoidBottomInset)
`bottomNavigationBar` · `bottomSheet` · `BottomAppBar` · `persistentFooterButtons` · `Positioned(bottom:)` · `SystemChrome` 사용처는 0. 하단 탭바는 셸의 자체 위젯이다.

| 파일:줄 | 요소 | 지금 inset 처리 | 고침 |
|---|---|---|---|
| `ui/shell.dart:268-283` | 태블릿 셸(레일 + 본문) | 본문에 padding 그대로 넘김 · 키보드는 Padding(viewInsets) + removeViewInsets | 없음 |
| `ui/shell.dart:290-305` | 폰 셸 · 하단 3메뉴 `_TabBar(bottom: mq.padding.bottom)` | 탭바가 안전 영역을 먹음 · 탭 없는 채팅 화면엔 padding 넘김 · 키보드면 제거 | 없음 |
| `ui/shell.dart:548-` | 레일 `_Rail` | 위 정렬 · 아래 24 — 하단 요소 없음 | 없음 |
| `ui/shell.dart:401` · `:632` · `chat/chat_kit.dart:469` | 탭 루트 `SafeArea(bottom:false)` | 스크롤 목록(아래 고정 요소 없음) | 없음 |
| **`chat/screens/chat_room_screen.dart:620`** | **대화 입력줄 · 비활성 안내 줄(`:732`) `_safeBottom`** | **폰 = padding.bottom · 태블릿 칸 = 0** | **고침 — Android 태블릿 칸도 padding.bottom** |
| `chat/screens/chat_room_screen.dart:494` | 말풍선 메뉴 위치 | padding 으로 가둠 | 없음 |
| `chat/screens/chat_room_screen.dart:886` · `chat_attach_sheet.dart:56` · `chat_forward_sheet.dart:50` · `ui/room_screen.dart:657` | 하단 시트 | `SafeArea(top:false)` | 없음 |
| `chat/chat_kit.dart:428` · `ui/chart_sheet.dart:26` · `ui/doctor_picker.dart:63` · `ui/interpret_widgets.dart:160` · `:194` | `showModalBottomSheet(useSafeArea)` | 내용이 `SafeArea` · `paddingOf.bottom`(`interpret_widgets.dart:181` · `:419` · `doctor_picker.dart:227`)로 비움. 태블릿은 다이얼로그 · 팝오버 | 없음 |
| `ui/interpret_widgets.dart:101-120` | 시술 방 하단 통역 바(폰 · 태블릿) | 둘 다 `10 + paddingOf.bottom` | 없음 |
| `chat/screens/chat_new_screen.dart:154` | 새 대화 [만들기] | 폰 = padding.bottom · 태블릿 = 가운데 패널(바닥 아님) | 없음 |
| `chat/screens/chat_media_screen.dart:137-159` · `chat_info_screen.dart:98-104` | 사진 · 방 정보(폰 화면 · 태블릿 오른쪽 시트) | 폰 = 목록 padding.bottom · 시트 = `SafeArea` | 없음 |
| `notify/notification_screen.dart:150` | 알림(태블릿 오른쪽 시트) | `SafeArea` | 없음 |
| `ui/login_screen.dart:51` · `:167` · `:195` · `chat/screens/chat_video_screen.dart:66` · `chat_photo_screen.dart:26` · `chat_new_screen.dart:112` · `ui/room_screen.dart:132` | 전체 화면 | `SafeArea` | 없음 |

### 고침(Dart 2파일 · 새 테스트 1)
- `lib/ui/theme.dart` — `paneReservesBottomInset`(= `defaultTargetPlatform == TargetPlatform.android`)를 하나 둔다. 이유는 주석에.
- `lib/chat/screens/chat_room_screen.dart:620` — `_safeBottom => widget.pane && !paneReservesBottomInset ? 0 : MediaQuery.paddingOf(context).bottom`.
- 플랫폼 분기를 쓴 이유: 같은 `padding.bottom` 이어도 아이패드(홈 인디케이터 · 겹쳐 그려도 됨 · 지금 0)와 Android(내비 · 태스크바 · 덮고 터치를 가져감)의 맞는 답이 다르다. iOS 화면을 그대로 두려면 iOS 값은 0 이어야 한다.
  `dart:io Platform` 대신 `defaultTargetPlatform` 을 써서 테스트로 두 플랫폼을 다 돌린다.
- 키보드: Flutter 의 `padding.bottom` 은 이미 키보드만큼 줄어든다(키보드가 열리면 0). 태블릿 셸은 `removeViewInsets` 만 하고 padding 은 그대로라 두 번 비지 않는다.
- `test/ui/pane_bottom_inset_test.dart`(새 파일 · 실제 앱 배선 Harness):
  - 아이패드 크기 · 아래 안전 영역 48 에서 Android 입력칸은 iOS 보다 정확히 48 위다.
  - iOS 는 48 미만(지금 그대로)이다.
  - 폰은 두 플랫폼이 같고 48 이상이다.

### 스크린샷(`app-5-shots/`)
Android = `Medium_Phone_API_36.1` 에뮬레이터를 내가 띄웠고 끝나고 껐다. 태블릿은 `wm size 1768x2208 · density 420`(Fold3 펼침 · 짧은 변 673dp → 레일 셸)로 했고 끝나고 reset 했다.
3버튼 ↔ 제스처는 `cmd overlay` 로 바꿨고, 원래대로 제스처로 돌려놨다.
| # | 화면 | 결과 |
|---|---|---|
| 01 · 02 | 폰 제스처 · 현황판 탭바 / 대화 입력줄 | 막대 위 ✓(퇴행 없음) |
| 03 · 04 · 05 · 06 | 폰 3버튼 · 탭바 / 대화 입력줄 / 첨부 시트(최근 사진 줄 · 사진 권한은 「허용 안 함」) / 시술 방 통역 바 · [통역하기] | 모두 내비 바 위 ✓ |
| **07 · 08** | **태블릿 3버튼 · 채팅 대화 칸 — 고치기 전 / 후** | **전 = 입력칸이 내비 바 아래 깔림(F1 재현) · 후 = 내비 바 위 ✓** |
| 09 · 10 | 태블릿 3버튼 · 현황판 끝까지 스크롤 / 시술 방 통역 바 | 마지막 카드 · 통역 바 내비 바 위 ✓ |
| 11 | 태블릿 제스처 · 채팅 대화 칸(고친 뒤) | 막대 위 ✓ |
| 12-15 | iPhone 17 · 채팅 목록(탭바) · 대화 입력줄 — 전 / 후 | **픽셀 동일**(PIL difference bbox = None) |
| 16-19 | iPad Air 11 · 현황판 · 시술 방(통역 바) — 전 / 후 | 현황판 픽셀 동일. 시술 방은 머리 줄 시계 · 「대기 N분째」만 다르고 아래쪽 동일 |

- 에뮬레이터 Gboard 는 소프트 키보드 대신 스타일러스 도구 막대만 떠서, 키보드가 열린 태블릿 칸은 화면으로 확인하지 못했다. 위 「키보드」 설명이 근거다.
- iPad 시뮬레이터에서 레일 [채팅]이 macOS 합성 클릭에 반응하지 않았다(뒤로 · 카드 · 알림 버튼은 됨). 그래서 iPad 전/후는 현황판 · 시술 방(하단 통역 바)으로 찍었다. iPad 대화 칸이 그대로인 것은 위 테스트(iOS = 0)로 확인했다.
  - Android 태블릿에서는 같은 레일 [채팅]이 탭으로 된다(07 · 08) — 시뮬레이터 입력 문제로 본다.
- 로그인: dev 데모 계정을 adb input · 시뮬레이터 키 코드로 넣었다. 값은 출력 · 스크린샷에 없다(설정 화면은 열지 않음).
  - 시뮬레이터 첫 시도 때 Option 키가 붙어 이메일이 깨진 글자로 찍힌 스크린샷이 생겼다. 바로 지웠다(스크래치 폴더 · 여기엔 없음).
  - 깨진 이메일로 dev 로그인 1회 실패가 서버에 남았다.
- 시뮬레이터 2대(iPhone 17 · iPad Air 11 — 앱 없던 것)를 내가 켰고 끝나고 껐다. 사용자 시뮬레이터(iPhone 17 Pro Max · iPad Pro 13)는 손대지 않음.
- Android 에뮬레이터에서 Back 두 번에 DAY 가 닫혀, 이미 깔려 있던 다른 개발 앱(Expo) 오류 화면이 잠깐 앞에 왔다. 탭 1-2번이 그 위에 떨어졌을 수 있다(오류 로그 Dismiss 자리). 그 앱은 더 만지지 않고 DAY 를 다시 띄웠다.

### analyze · test
- `fvm flutter analyze` — No issues found
- `fvm flutter test` — **+347 ~73 All tests passed**(전 345 + 새 2)

## B. AND-7 — `app/android/play_upload.py`

### 위치를 고른 이유
저장소 스크립트는 루트 `scripts/*.py`(python3 · 표준 + 의존 최소)이고, `app/tool/` 은 테스트 · 캡처 도우미다.
업로드는 Android 전용이고 `-P` 서명 · id 주입(`app/android/`)과 짝이라 `app/android/` 에 둔다.

### 하는 일
- `upload`: 서비스 계정 JWT(RS256 · `cryptography`) → 토큰 → `edits.insert` → `bundles.upload`(AAB) → `tracks.update`(트랙 · 출시명 · ko-KR 노트 · `status: completed`) → `edits.commit`.
  - 커밋 뒤 그 트랙을 다시 읽어 출력한다.
  - 어느 단계든 실패하면 edit 을 삭제한다.
- `--dry-run`: commit 대신 `edits.validate` 를 하고 edit 을 삭제한다(Play 에 남는 것 없음).
- `--expect-version-code`: 올린 AAB versionCode 가 다르면 멈춘다(edit 삭제).
- `--changes-not-sent-for-review`: Play 가 요구할 때만 쓴다.
- `tracks`: 읽기만(insert → list → delete).
- 키 경로: `--key` > env `DAY_PLAY_SERVICE_ACCOUNT` > `~/.config/day/android/play-service-account.json`. 키 · 토큰은 출력하지 않는다. 오류는 HTTP 상태와 Google 오류 문구만 낸다.
- 의존성: python3 + `requests` · `cryptography`(이 맥에 있음 — 2.32.5 · 46.0.5). 설치법은 README 에.

### W-1 · README
- `app/.gitignore`: `*.jks` · `*.keystore` · `*.p12` · `*.aab` · `upload-key.properties` · `play-service-account*.json` 추가.
  - `git check-ignore` 확인: `app/x.jks` · `app/android/x.keystore` · `app/y.p12` · `app/z.aab` · `app/upload-key.properties` · `app/play-service-account.json` · `app/android/play-service-account-dev.json` 모두 ignored.
  - `app/android/play_upload.py` 는 추적된다.
- `app/README.md` Android 절에 「Play 업로드(API)」 소절을 **추가만**(키 위치 · 의존성 · `tracks` · dry-run → 실제 · 트랙 표).

## C. 빌드 2 · 업로드

### AAB(둘 다 600 · `~/.config/day/android/out/`)
| | 개발 `DAY-Dev-0.1.0-2.aab` | 정식 `DAY-0.1.0-2.aab` |
|---|---|---|
| sha256 | `082d5f21008afac9565a9f4a578197dcad40e4bf75ddb138e281626ed968e94e` | `adcc3a834494bab7f6c50f26e03521c23fa402e88b3c19270a55e80f17fcb2f3` |
| package · label | `day.medisolveai.dev` · `DAY Dev` | `day.medisolveai` · `DAY` |
| versionCode · versionName · targetSdk · debuggable | 2 · 0.1.0 · 36 · 없음 | 2 · 0.1.0 · 36 · 없음 |
| `jarsigner -verify` · 지문 | jar verified · `92:75:54:AE:…:F9:A9:69:AD` = 업로드 키 | 같음 |
| libapp.so 주소 | `https://day-dev.medisolveai.com` | `https://day.medisolveai.com` · `https://day.medisolveai.com,https://day-dev.medisolveai.com` |

정정: `production` 문자열은 `lib/core/build_config.dart:68` 의 코드 리터럴이라 개발 AAB 에도 있다. 4판 리포트가 이 문자열을 `DAY_APNS_ENV` 확인 근거로 든 것은 틀렸다. 정식 빌드에 `--dart-define=DAY_APNS_ENV=production` 을 넣은 것은 명령으로만 확인된다.

### 업로드 결과
| 앱 · 트랙 | 명령 | 결과 |
|---|---|---|
| `day.medisolveai.dev` · internal | `--dry-run` | upload ok(vc 2) · tracks.update ok · **edits.validate ok** · edit 삭제 |
| `day.medisolveai.dev` · internal | 실제 | **edits.commit ok** → 트랙 읽기: `internal: name='2 (0.1.0)' versionCodes=['2'] status=completed notes='ko-KR: 하단 내비게이션 바가 입력창을 가리던 문제 수정'` |
| `day.medisolveai` · alpha | `--dry-run` 만 | upload ok(vc 2) · tracks.update ok · **edits.validate ok** · edit 삭제 |
| `day.medisolveai` · alpha | (실제 안 함 — 지시) | 트랙 읽기: `alpha: name='1 (0.1.0)' versionCodes=['1'] status=completed`(바뀌지 않음) |

정식 앱 실제 업로드 명령(코디 지시 뒤):
`cd app/android && python3 play_upload.py upload --package day.medisolveai --track alpha --aab ~/.config/day/android/out/DAY-0.1.0-2.aab --expect-version-code 2 --release-name '2 (0.1.0)' --notes '하단 내비게이션 바가 입력창을 가리던 문제 수정'`

## 변경 파일(미커밋)
- `M app/lib/ui/theme.dart` · `M app/lib/chat/screens/chat_room_screen.dart`(F1)
- `?? app/test/ui/pane_bottom_inset_test.dart`(새 테스트)
- `?? app/android/play_upload.py`(AND-7)
- `M app/.gitignore`(W-1) · `M app/README.md`(소절 추가만)
- `app/ios` · 채팅 최근 사진 줄 · 사진 권한 변경 0

## 비밀 grep
값 자체로 비교했다(출력 없이): 서비스 계정 `private_key_id` · 키 본문 줄 · `client_email` · 업로드 키 비밀번호 · dev 데모 이메일 · 비밀번호.
대상은 `git diff` + 새 파일 2개다 → 모두 **0건**. 이 리포트도 같은 방식으로 0건.

## 사용자에게 넘길 것
1. **실기기(Z Fold3) 확인** — Play 내부 테스트에서 DAY Dev 업데이트(vc 2)를 받는다.
   - 펼친 화면 · 3버튼 내비 + 태스크바에서 채팅 대화 칸의 「메시지 입력」이 바 위에 보이는지 본다.
   - 접은 화면(폰)도 그대로인지 본다.
2. 확인되면 코디가 정식 앱 alpha 실제 업로드를 지시한다(위 명령 · AAB 준비됨).
3. 커밋 · PR 은 코디가 한다.
