# android-app 6판 — review-code-3 WARN 반영 · 빌드 3 결과 보고

## 상태: done — 미커밋(HEAD `fa2f0d9f` 위 · 5판 변경에 이어서)

## dev 최신 확인
| 시점 | `git log --oneline HEAD..origin/dev`(fetch 뒤) |
|---|---|
| 시작 | 0건 |
| 보고 직전 | 0건 |

## W-1 — padding 을 직접 준 스크롤 목록 끝

### 정정
5판 리포트의 스크린샷 09 「마지막 카드 내비 바 위 ✓」는 틀렸다. 리뷰 지적대로 A-룸6 끝 줄이 바 밑에 잘려 있었다.
이번 판 전 화면(01)에서도 같은 자리가 실제 태스크바 밑에 잘린다.

### 전수(`app/lib` 의 ListView · GridView · SingleChildScrollView · CustomScrollView · SliverPadding · ReorderableListView — 23개 · 스크립트로 생성자 맨 위 `padding:` 인자 추출)
padding 을 주지 않은 목록은 Flutter 가 MediaQuery 안전 영역을 스스로 더하므로 문제가 없다(표에 「-」).
「태블릿 본문」은 셸이 padding.bottom 을 넘기는 자리(레일 셸 오른쪽 · 바닥까지 닿음)다.

| 파일:줄 | 목록 | padding | 놓이는 곳 | 고침 |
|---|---|---|---|---|
| `ui/board_screen.dart:131` | 판 칩 줄(가로) | 10 | 높이 52 칸 · 바닥 아님 | 없음 |
| `ui/board_screen.dart:179` | 판 카드 목록(**폰만**) | 아래 24 | 폰 탭 화면 — 셸이 padding.bottom 을 지움(0) | **고침**(`+ listEndInset` — 폰은 0 이라 값 불변 · 리뷰 지목 자리) |
| `ui/board_screen.dart:193` | 판 카드 격자(**태블릿**) | 아래 24 | **태블릿 본문 · 바닥** | **고침** — Android 태블릿 `24 + inset` |
| `ui/shell.dart:425` | 설정 목록 | 16 | **태블릿 본문 · 바닥**(폰은 탭바가 먹음 → 0) | **고침** — Android 태블릿 `16 + inset` |
| `ui/chart_sheet.dart:67` | 차트 시트 노트 목록 | 16 | **폰 하단 시트(0.8 높이 · 화면 바닥까지)** · 태블릿은 가운데 다이얼로그 | **고침** — Android 폰 `16 + inset`(태블릿 다이얼로그는 0). 리뷰 표 밖 · 같은 F1 자리 |
| `ui/room_screen.dart:173` · `:179` | 시술 방 본문(폰 · 태블릿) | 아래 16 | 아래에 통역 바(`10 + padding.bottom`)가 있어 바닥 아님 | 없음 |
| `ui/doctor_picker.dart:258-262` | 원장 고르기 목록 3 | 12 | 아래 [호출] 줄(`:227` 폰 = padding.bottom) 위 · 태블릿 = 팝오버 | 없음 |
| `ui/interpret_widgets.dart:49` | 문장 칩(가로) | 오른쪽만 | 바닥 아님 | 없음 |
| `ui/interpret_widgets.dart:349` | 통역 서랍 말 목록 | 14 | 아래 마이크 줄(`:419` padding.bottom) 위 | 없음 |
| `ui/interpret_widgets.dart:167` | 언어 고르기 시트 | - | 내용 끝 `SizedBox(paddingOf.bottom + 8)`(`:181`) | 없음 |
| `ui/login_screen.dart:53` | 로그인 | 16 | `SafeArea` 안 | 없음 |
| `chat/screens/chat_room_screen.dart:254` | 대화 말풍선 목록 | 12 | 아래 입력줄(5판 고침) 위 | 없음 |
| `chat/screens/chat_list_screen.dart:138` | 채팅 목록(폰 · 태블릿 왼쪽 칸) | - | Flutter 자동 안전 영역(아이패드도 지금 그대로) | 없음 |
| `chat/screens/chat_new_screen.dart:152` | 새 대화 사람 목록 | 폰 `16 + padding.bottom` · 태블릿 0 | 태블릿 = 가운데 패널(바닥 아님) | 없음 |
| `chat/screens/chat_info_screen.dart:103` · `chat_media_screen.dart:155` | 방 정보 · 사진 격자 | 폰 `+ padding.bottom` · 시트 0 | 태블릿 오른쪽 시트 = `SafeArea` | 없음 |
| `chat/screens/chat_forward_sheet.dart:268` · `:280` | 전달 시트 | - · 아래 16 | 폰 = `SafeArea(top:false)` 시트 · 태블릿 = 가운데 패널 | 없음 |
| `chat/screens/chat_attach_sheet.dart:205` | 첨부 시트 최근 사진(가로) | - | `SafeArea(top:false)` 시트 | 없음(사진 줄 그대로) |
| `notify/notification_screen.dart:142` | 알림 목록 | - | `SafeArea`(폰 · 태블릿 시트) | 없음 |

### 고침
- `lib/ui/theme.dart`: `listEndInset(context) => paneReservesBottomInset ? MediaQuery.paddingOf(context).bottom : 0` 하나를 더했다.
  - iOS 는 늘 0 이다. 폰 탭 화면은 셸이 padding 을 지워 0 이다.
- 적용한 자리:
  - `lib/ui/board_screen.dart:179` · `:193`(아래 `24 + listEndInset`)
  - `lib/ui/shell.dart:425`(설정 `fromLTRB(16,16,16,16 + listEndInset)` · `SettingsBody._body` 에 context 를 넘김)
  - `lib/ui/chart_sheet.dart:67`(폰만 `16 + listEndInset` · `_notes` 에 context 를 넘김)

### 테스트 — `test/ui/pane_bottom_inset_test.dart`
5개 테스트 × `TargetPlatformVariant{android, iOS}` = 10회 실행이다.
| 테스트 | Android | iOS |
|---|---|---|
| 태블릿 대화 칸 입력칸 ~ 화면 바닥 | ≥ 48 | < 48(그대로) |
| 폰 대화 화면 | ≥ 48 | ≥ 48 |
| **태블릿 판 끝**(카드 24장 · 끝까지 jumpTo) 마지막 카드 ~ 화면 바닥 | **24 + 48** | 24(그대로) |
| 설정 목록 아래 padding — 태블릿 | 16 + 48 | 16 |
| 설정 목록 아래 padding — 폰 | 16 | 16 |

- `debugDefaultTargetPlatformOverride` 는 `addTearDown` 대신 **`TargetPlatformVariant`** 로 정하고 되돌린다.
  - 처음엔 지시대로 `addTearDown` 으로 했는데, 4개 모두 「The value of a foundation debug variable was changed by the test」로 실패했다. 프레임워크의 debug 변수 검사가 tearDown 보다 먼저 돈다.
  - Variant 는 검사 전에 되돌리고, 실패해도 2차 오류가 없다 — 리뷰가 말한 의도와 같다.
- 변이 확인: `listEndInset` 을 0 으로 바꾸면 Android 「판 끝」 · 「설정 태블릿」 2개가 실패한다. 원복 뒤 통과.

### 스크린샷(`app-6-shots/`)
- 에뮬레이터: `Medium_Phone_API_36.1` 을 내가 켜고 껐다.
  - `wm size 1768x2208 · density 420` + 3버튼으로 했다. 이번엔 런처 **태스크바**가 실제로 떴다(Fold3 와 같은 꼴).
  - 끝나고 제스처 · 크기 · 밀도를 원래대로 돌렸다.
- 전 = 5판 apk · 후 = 이번 apk.

| # | 화면 | 결과 |
|---|---|---|
| 01 · 02 | Android 태블릿 3버튼 + 태스크바 · 판 끝까지 스크롤 — 전 / 후 | 전 = A-룸6 끝 줄이 태스크바 밑에 잘림 · **후 = 마지막 카드 전체가 바 위** |
| 03 · 04 | 같은 · 설정 끝(아래쪽만 잘라 저장 — 계정 칸 없음) — 전 / 후 | dev 계정은 설정이 짧아 스크롤이 없어 끝이 바에 닿지 않는다 → 화면 차이 없음. padding 차이(16 → 64)는 테스트로 확인 |
| 05 | 같은 · 채팅 대화 칸(5판 고침 · 태스크바 실물) | 입력칸 바 위 ✓ |
| 06 · 07 | iPad Air 11 시뮬레이터 · 판 — 전(5판) / 후 | **픽셀 동일**(PIL difference bbox = None). dev 판 5장이 한 화면에 들어가 스크롤이 없다 → 판 끝 = 전체 화면. iPad 판 끝 값이 그대로(24)인 것은 테스트로 확인 |

- iPad 시뮬레이터를 내가 켜고 껐다. 로그인 값은 5판과 같은 방식으로 출력 · 스크린샷에 없다(Android 는 adb input · iPad 는 키체인에 남은 세션).

## W-2 · W-3 — `app/android/play_upload.py`
- `--track` 은 argparse `choices=[alpha, internal]` 로 받는다. 짝 표 `UPLOAD_TRACKS = {day.medisolveai.dev: internal, day.medisolveai: alpha}` 로 검사하고, 키 · 네트워크 전에 멈춘다.

| 인자 | 결과 |
|---|---|
| dev · production | exit 2 `invalid choice: 'production'` |
| prod · beta | exit 2 `invalid choice: 'beta'` |
| dev · alpha | exit 1 `day.medisolveai.dev 는 internal 트랙에만 올린다` |
| prod · internal | exit 1 `day.medisolveai 는 alpha 트랙에만 올린다` |
| com.other · internal | exit 1 `올릴 수 없는 패키지` |
| dev · internal(키 없음) | 짝 통과 → 키 읽기에서 exit 1(정상 경로) |

- W-3: commit 뒤 트랙 다시 읽기를 try 로 감쌌다. 실패하면 「edits.commit ok · 트랙 다시 읽기만 실패(…) — 다시 올리지 말고 `tracks` 로 확인」을 내고 **exit 0** 이다.
  - 가짜 Edit(두 번째 insert 에서 HTTP 503)로 오프라인 확인: 위 문구 · exit 0.
- README 트랙 줄에 「이 두 짝만 받는다」 한 문장을 더했다.

## 참고 — 루트 `.gitignore`
루트 관례(주석 머리 + 패턴 묶음)대로 「Android 서명 · Play 업로드 비밀」 묶음을 더했다: `*.jks` · `*.keystore` · `*.p12` · `*.aab` · `upload-key.properties` · `play-service-account*.json`.
- check-ignore: 루트 `x.jks` · `y.keystore` · `z.p12` · `x.aab` · `upload-key.properties` · `play-service-account.json` · `backend/play-service-account-x.json` ignored.
- `app/android/play_upload.py` · `deploy/config/dev.env` 는 추적된다. 이미 추적 중인 파일과 겹치는 것 0.
- 이름이 다른 서비스 계정 파일(`sa.json`)은 여전히 패턴 밖이다(키는 `~/.config/day/android/` 에 둔다).

## 수치
- `fvm flutter analyze` — No issues found
- `fvm flutter test` — **+355 ~73 All tests passed**(5판 347 − 옛 inset 2 + 새 10)

## 빌드 3(`~/.config/day/android/out/` · 둘 다 600)
| | `DAY-Dev-0.1.0-3.aab` | `DAY-0.1.0-3.aab` |
|---|---|---|
| sha256 | `f1ed2385191eb89c29d22f6913c0fc98c8f142a57a333d3791ed4f02b4f6ce34` | `84634745566afc0180deae6e7d4714ed7adb2e45caec21115f4e41b4eab37581` |
| package · label | `day.medisolveai.dev` · `DAY Dev` | `day.medisolveai` · `DAY` |
| versionCode · versionName · targetSdk · debuggable | 3 · 0.1.0 · 36 · 없음 | 3 · 0.1.0 · 36 · 없음 |
| 서명 | jar verified · `92:75:54:AE:…:F9:A9:69:AD` = 업로드 키 | 같음 |

## 업로드
| 앱 · 트랙 | 결과 |
|---|---|
| `day.medisolveai.dev` · internal · dry-run | upload vc 3 · tracks.update · **edits.validate ok** · edit 삭제 |
| `day.medisolveai.dev` · internal · 실제 | **edits.commit ok** → `internal: name='3 (0.1.0)' versionCodes=['3'] status=completed notes='ko-KR: 하단 내비게이션 바가 입력창과 목록 끝을 가리던 문제 수정'` · exit 0 |
| `day.medisolveai` · alpha · dry-run 만 | upload vc 3 · tracks.update · **edits.validate ok** · edit 삭제 · 트랙 읽기 `alpha: '1 (0.1.0)' vc 1`(바뀌지 않음) |

정식 alpha 실제 명령(지시 뒤):
`cd app/android && python3 play_upload.py upload --package day.medisolveai --track alpha --aab ~/.config/day/android/out/DAY-0.1.0-3.aab --expect-version-code 3 --release-name '3 (0.1.0)' --notes '하단 내비게이션 바가 입력창과 목록 끝을 가리던 문제 수정'`

## 변경 파일(미커밋 · 5판 포함 전체)
- `M .gitignore`(이번) · `M app/.gitignore`(5판)
- `M app/README.md`(5판 소절 + 이번 한 문장)
- `M app/lib/ui/theme.dart`(5판 `paneReservesBottomInset` + 이번 `listEndInset`)
- `M app/lib/chat/screens/chat_room_screen.dart`(5판)
- `M app/lib/ui/board_screen.dart` · `M app/lib/ui/shell.dart` · `M app/lib/ui/chart_sheet.dart`(이번)
- `?? app/android/play_upload.py`(5판 + 이번 W-2 · W-3) · `?? app/test/ui/pane_bottom_inset_test.dart`(5판 + 이번 고쳐 씀)
- `app/ios` · 채팅 최근 사진 줄 · 사진 권한 변경 0

## 비밀 grep
값 34개를 출력 없이 값 자체로 비교했다: 서비스 계정 `private_key_id` · `client_email` · `client_id` · 키 본문 줄들, 업로드 키 비밀번호, dev 데모 이메일 · 비밀번호.
대상은 `git diff` + 추적 안 된 새 파일 2개다 → **0건**. 이 리포트 · 스크린샷 03/04(아래쪽만 자름)에도 계정 값 없음.

## 사용자에게 넘길 것
1. Z Fold3 펼침(3버튼 + 태스크바)에서 DAY Dev vc 3 을 받는다. 다음이 바 위에 있는지 확인:
   - 채팅 입력칸
   - **시술현황을 끝까지 내렸을 때 마지막 카드**
   - (목록이 길면) 설정 끝
   - 폰 쪽 차트 시트 끝
2. 확인되면 코디가 정식 alpha 실제 업로드를 지시한다(위 명령 · vc 3 AAB 준비됨 · vc 2 는 올리지 않은 채로 건너뜀 — Play 는 더 큰 versionCode 만 받으면 된다).
3. 커밋 · PR 은 코디가 한다.
