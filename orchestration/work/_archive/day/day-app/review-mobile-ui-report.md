# 리뷰 리포트 — day-app mobile UI 교정 + 로컬 API 소비 / code + 시각 (2026-11-10)

- 대상: `CENTURION_DAY/day-app` · `kknaksss/day-app` · 기준 `0b776e90` 위 미커밋 `app/**` 변경(24 수정 + `accept.dart` · `shell.dart` · `test/capture/` 신규).
- 원천: SPEC-003 exact `cdde456a`(로컬 확인 HEAD 일치) · `mobile-ui-code-brief.md` · `mobile-ui-code-report.md` · ui-reference 13장 · 프로토 `cc-prototype/procedure/app`(read-only).
- 방식: read-only. 앱 · 서버 · 기기 · 포트 조작 0. app 파일 수정 0. 증거 PNG 를 직접 열어 대조.
- 검증 로그: `review-mobile-ui-logs/`(analyze.txt · test.txt)

## 판정: **PASS (WARN 4)**

FAIL 은 없다. 13 UI 항목과 API 6차이는 코드와 최종 PNG 모두 스펙과 맞는다. 코디가 따로 짚은 점(최종 `phone-doctor-call-sheet-empty` 에 4탭이 안 보인다는 것)은 **최종 PNG 기준으로 사실이 아니다** — 아래 「시각 검수」 참고. WARN 은 증거 픽스처 정합 1건, 스펙 문구 1건, 시각 증거 빈칸 2건이다. 출시를 막지 않으며 mobile 에게 돌려 고칠 수 있다.

## 직접 실행 (mobile 수치 재현)

| 명령 (cd app · FVM) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found · exit 0 |
| `fvm flutter test` | **+184 · ~18 skip(캡처 전용) · 0 fail** · exit 0 — mobile 보고와 같음 |
| `git diff --name-only 0b776e90` · `git status` | 변경은 `app/**` 뿐(allowed_paths 준수) |
| `grep http:// lib ios/Runner/*.plist` | 소스 하드코딩 0(Info.plist DTD URL 뿐) |
| `grep NSAppTransportSecurity\|NSAllows* ios/` | ATS 예외 0 |
| `git diff 0b776e90 -- lib/core lib/data lib/state/session_controller.dart ios` | `copy.dart` 글자 추가뿐 · origin · 세션 · 네트워크 · native 변경 0 |
| `ios/Podfile.lock` | shared_preferences 흔적 없음 → 의존성 제거가 native 를 바꾸지 않음 |

unsigned build · 시뮬레이터 build 는 다시 돌리지 않았다(native · 빌드 설정 변경 0, mobile 로그 `flutter-build-ios*.txt` 확인).

## FAIL

없음.

## WARN

1. **캡처 픽스처 정합 — 「호출 0」 인데 수락 대기 호출이 보임** — `app/test/capture/visual_capture_test.dart:175-188`(`_snap([_called(), …])` 에 `calls:` 를 넘기지 않음).
   - 재현: `phone-call-wait-list-doctor.png` · `phone-call-wait-list-nurse.png` · `ipad-board-list.png` — 카드에는 「전체 의사 · 수락 대기 3분」이 있는데 인박스 탭은 「호출 0」.
   - 앱 코드는 맞다: `board.dart` `waitingCallCount` = `calls[]` 중 `acceptedBy == null`(SPEC-003 U-2 :174). 서버는 `cards` 와 `calls` 를 같이 싣기 때문에 실물에서는 생기지 않는 조합이다. 다만 증거 PNG 가 실물 모습을 잘못 보여 준다.
   - 고칠 것: 캡처 fixture 에 그 호출의 `calls[]` 항목을 넣고 다시 캡처.
2. **폰 호출 시트 머리에 고객 이름이 빠짐** — `app/lib/ui/room_screen.dart:453`: `where: isTablet(btn) ? '방 · 고객' : card.roomTitle`.
   - 스펙: SPEC-003 U-5 :56 머리 = 「의사 호출」 + 「방 · 고객 이름」, :58 「문구 · 칸 · 규칙은 같다」(플랫폼은 배치만 다름).
   - 재현: `phone-doctor-call-sheet-*.png` = 「의사 호출 A-룸1」, `ipad-doctor-call-sheet-picked.png` = 「A-룸1 · TEST CLAUDE」. 폰 수락 드로어는 「C-룸1 · CHEN WEI」라서 폰 안에서도 서로 다르다.
   - 원본 PNG(`doctor-call-sheet.png`)가 방만 보이므로 원본을 따른 선택이다. 그래도 스펙 문구와 다르다. 폰도 「방 · 고객」으로 할지, 스펙을 고칠지는 코디가 정한다(정책 발명 아님 · 문구 대조).
3. **긴 이름 · 320 · 599/600 시각 증거 없음** — overflow 0 은 테스트로만 확인된다(`app_flow_test.dart:220` · `actions_test.dart:262,281` — 내가 돌린 184 통과에 포함).
   - 이 테스트는 RenderFlex overflow 예외만 잡는다. 글자 잘림이나 말줄임은 보지 않는다.
   - 브리프 §3 「목록 · 상세 긴 시술명 320 폭」의 **눈 검수는 PNG 가 없어 하지 못했다.** 캡처 목록(390 · 1024)에 320 긴 이름 1장(목록 + 상세)과 599/600 1장씩을 더할 것을 권한다.
4. **활성 [시작] · 호출 탭 · 시술 완료 탭 캡처 없음**.
   - 모든 상세 PNG 에서 [시작]이 꺼진 회색 테두리다(fixture `canStart:false`). 켜진 [시작]의 DAY 주색 테두리(U-7 「버튼 색 = DAY 주색」)는 코드(`room_screen.dart:519-525` outlined primary)로만 확인했다.
   - U-10 호출 탭과 U-11 시술 완료 탭 화면도 증거가 없다. 브리프 캡처 목록에 없으니 결함은 아니다. 실물에서 처음 보게 되는 화면이다.

## 코디 중간 피드백 반영 확인

| 메일 | 확인 | 근거 |
|---|---|---|
| msg_e7a53096d7c3 run bool 오용 | 반영 | `board_controller.dart` `run` = 2xx 일 때만 `!_disposed`, 실패 · 닫힌 판이면 false. `doctor_picker.dart:193-200` 시트는 true 일 때만 닫고 false 면 다시 켬 |
| msg_85a0f1c0bf92 숨은 탭 / route 늦은 응답 | 반영 | `shell.dart:61` `present()` = mounted · 탭 보임 · route active · PageRoute 가 덮지 않음. 모든 조작이 `alive: _alive` 를 넘김(room 405-645, board 212 · 326 · 632). 늦은 2xx · 오류 토스트 없음, 401 만 세션으로 전달 |
| msg_839ac2566c65 숨은 드로어 mic stop | 반영 | `room_screen.dart:81-89` 탭이 숨으면 `_closeDrawer` · `AppLifecycleListener(onHide)` · dispose 에서 `_interp.dispose` |
| msg_ecc006fe5ddf 통역 드로어 하단 탭 | 반영 | `phone-interpret-drawer.png` 4탭 보임 |
| msg_3e1abad18a7e 호출 시트 하단 탭 · 취소 footer | 반영 | `phone-doctor-call-sheet-empty.png` · `-picked.png`(780×1688 · 13:44 · 마지막 코드 수정 13:43:38 뒤). [취소]+「의사를 선택하세요」 footer 아래에 **예약현황 · 시술현황 · 채팅 · 설정 4탭이 보인다**. `phone-nurse-accept-drawer.png` · `phone-undo-confirm.png` 도 같다. 코드: `showModalBottomSheet` 기본 `useRootNavigator:false` → 탭 Navigator 안이고, 탭바는 Navigator 밖 Column(`shell.dart:173-184`) |

코디가 「4탭이 안 보인다」고 한 것은 이전 중간판으로 보인다. 최종 파일은 위와 같다.

## 13 UI 항목 대조

| # | 항목 (SPEC-003) | 코드 | 시각 (직접 연 PNG) | 판정 |
|---|---|---|---|---|
| 1 | 셸 4메뉴 · 폰 탭바 / iPad 레일 · 5번째 메뉴 없음 · 예약 「곧 출시 예정」 · 채팅 빈 자리 · 머리 DAY/제목/종(배지 · 동작 없음) · 계정은 설정 | `shell.dart` 전체 · `copy.dart` 메뉴 상수 | `phone-tab-*` · `ipad-board-list`(레일 4개 · 내원현황 없음) | PASS (iPad 의 레일 + 머리 DAY 두 번은 프로토 `header.dart:1` 「폰 · 태블릿 같음」과 같음) |
| 2 | 인박스 탭 「현황/호출 n/시술 완료 n」 + 칩 4개 = 서버 section · 서버 순서 | `board_screen.dart:28-30,132` | `phone-board-filter-need` · `phone-board-list` | PASS (증거 「호출 0」은 WARN-1) |
| 3 | 카드 4행 방/수납 → 이름·발음 → 바이탈 → 상태 상자 · 둥근 · 0/2 줄 없음 | `board_screen.dart` | `phone-board-list` · `ipad-board-list` — 사용자 ASCII 순서 그대로 · 진행 0/2 줄 없음 | PASS |
| 4 | 마취 한 줄 · 연보라 · long 빨강 · 「시술 대기 - 마취 완료 N분」(lastSeconds ÷60) | `format.dart` `lastAnesMinutes` | 같은 PNG(14분 보라 · 30분 빨강 테두리 · 마취 완료 21분) | PASS |
| 5 | 호출 뒤 카드 · 상세 강조 상자 · 원장 즉시 / 간호사 드로어 · 3진입점 | `accept.dart` · board 316/622 · room 278-292 · 498-516 | `*-call-wait-list-doctor`(「수락 · 2건」) · `*-nurse`(「원장 골라 수락 · 2건」) · `*-nurse-accept-drawer`(머리 「수락할 원장」 · 「모든 의사」 줄 없음) | PASS |
| 6 | 「< 시술현황 · {방}」 · 시술 카드 · 진행중 연한 DAY · 큰 경과 · 완료 아래 회색 · 세로 ⋮ · 확인 창 원문 | `room_screen.dart` | `phone-doing-room` · `phone-done-room` · `phone-undo-confirm`(「…완료를 취소할까요?」 [닫기]/[완료 취소]) · 원본 `procedure-doing/done.png` 와 구조 같고 teal→DAY blue | PASS (활성 [시작]은 WARN-4) |
| 7 | 상시 체크박스 없음 · 한 시트(시술 체크/전체 선택 + 원장) · pickable · 재호출 canRecall · 기본 선택 firstKind | `doctor_picker.dart:186,271-296` · room 22-29 | `*-doctor-call-sheet-empty/picked` — 원본 `doctor-call-sheet.png` 구조 같음 · 마법사 없음 | PASS (머리 문구는 WARN-2) |
| 8 | 모두 완료 상자 · 마지막 종료 · [귀가 대기] canHome · 머리 합성 글자 · home 중복 없음 | room 620-650 | `phone-all-done-room` vs `home-ready.png` 같음 · 머리 「시술 모두 완료 · 귀가 대기 전」 한 번 | PASS |
| 9 | 통역 드로어 원형 · 바 칩 스피커 아이콘 · 알약 · 가로 스크롤 · [통역하기] | `interpret_widgets.dart` | `phone-interpret-drawer` vs `interpret-drawer.png`(손잡이 · 드롭다운 · 방 · 경과 · [종료] · 가운데 안내 · 칩 · 큰 원형 마이크 · 4탭) · `quick-speech` ↔ `phone-doing-room` 아래 바 | PASS (iPad [종료] 글자가 「통역 종료」 — 프로토 태블릿 글자인지 따로 확인하지 않음, 참고) |
| 10 | TW→zh-Hant 「중국어(번체)」 · 앞 고객/전역 언어 덮지 않음 · 수동 변경 WS 같이 · 7언어 · vi/yue 칩 없음 | `langs.dart` `natLang` · `interpret_controller.dart` `_manual` · `followCustomer` · RoomScreen 마다 새 컨트롤러 | 바 · 드로어 「중국어(번체)」 | PASS |
| 11 | 토스트 어두운 둥근 상단 · 2.6초 · 덮어쓰기 · 원문 · 본인 2xx 만 · 되돌리기 없음 | `copy.dart` `OkToast` = U-13 표 글자 그대로 · `widgets.dart` 토스트 | `phone-success-toast-accept` 「C-룸1 수락」 · `-undo` · [되돌리기] 없음 | PASS |
| 12 | API 정합 · 세션 race · origin · redirect · 로그 무변경 | 아래 API 표 · session/origin/data diff 0 | — | PASS |
| 13 | 원형 디자인 + DAY 색 · overflow 0 | 테스트 | 390/1024 PNG 46장 | PASS (320 눈 검수는 WARN-3) |

## API 6차이 대조 (dev 91728737 → 로컬 a1c90b9d)

| # | 차이 | 앱 | 판정 |
|---|---|---|---|
| ① | `need` → `needs[]` 5상황 | `Need.parse`(why · since · limitMin · callId · doctorName) · `needsCheck` 테두리 · 판정 재계산 없음 · 옛 `need` 안 읽음 | PASS |
| ② | `tasks[].canRecall` | `canRecallCall` = board edit && 서버 값 · 5분 조건 제거 | PASS |
| ③ | 취소 확인 창 | `confirmUndo`: 폰 시트 / iPad 모달 · [닫기] = 요청 0 · 경로 `undo-start\|undo-finish` | PASS |
| ④ | `lastMinutes` → `lastSeconds` | `_i(lastSeconds)` · ÷60 표시만 | PASS |
| ⑤ | `pickable` 준비중만 | `_pickedNow` = 서버 pickable 만 · 전체 선택 = pickable 전부 | PASS |
| ⑥ | 원장 변경 · 검색 · 차트 API | 부르지 않음 · `call_already_accepted` 글자 추가(SPEC U-6 원문) | PASS |

원장 본인 수락 `doctorStaffId = me.staffId`(`accept.dart:37`) · 간호사는 고른 원장 · 드로어 기본 선택 = 지정 호출이면 지정 원장(`proxyDefault`) — U-6 그대로다. A→B 지정 호출을 원장이 본인 수락하는 경로도 새 차단 없이 서버 판정에 맡긴다(U-6 :74).

## 보안 · 세션 회귀

- 셸이 `ValueKey(board)` 로 세션에 묶여 있다(`app.dart:142`). 로그아웃 · 세션 교체 때 탭 Navigator 4개와 그 위 시트 · 팝오버 · 확인 창이 같이 사라진다. 시트 · 팝오버는 모두 `useRootNavigator:false` 다.
- 닫힌 판의 늦은 응답(성공 · 오류 · 401)은 `_disposed` 에서 끊기고 토스트 · 콜백이 없다 → 이전 세션의 늦은 401 이 새 세션을 지우지 않는다(`session_race_test` 7건 통과).
- origin · redirect · release https · 허용 목록 · 환경 필수 코드는 바뀌지 않았다. 소스 http 하드코딩 0, ATS 예외 0. 로컬 http 는 `--dart-define` debug 값으로만 들어간다.
- D-2(푸시 · 기기) · D-3(통역 WS) · D-5(알림 배지) 는 서버에 없고 앱은 종만 그린다. 배지 · 데모 흐름 · 가짜 값 0(`grep` 과 PNG 로 확인).

## 직접 열어 본 PNG

- 원본(ui-reference): `doctor-call-sheet` · `nurse-accept` · `procedure-list` · `procedure-doing` · `procedure-done` · `waiting-card` · `called-board-card` · `tab-header` · `home-ready` · `interpret-drawer` · `success-toast` (11/13. `doctor-accept` · `quick-speech` 는 열지 않았다. `quick-speech` 는 `procedure-done` 아래쪽과 통역 바 PNG 로 대신 확인)
- 결과(mobile-ui-evidence/screens, **모두 fixture 렌더**): `phone-doctor-call-sheet-empty` · `phone-doctor-call-sheet-picked` · `phone-nurse-accept-drawer` · `phone-board-list` · `phone-call-wait-list-doctor` · `phone-call-wait-list-nurse` · `phone-doing-room` · `phone-done-room` · `phone-interpret-drawer` · `phone-all-done-room` · `phone-nurse-accept-room` · `phone-undo-confirm` · `phone-success-toast-accept` · `ipad-doctor-call-sheet-picked` · `ipad-board-list` · `ipad-nurse-accept-drawer` · `ipad-interpret-drawer` (17/46장. 나머지 `*-tab-*` · `waiting` · `anesthesia*` · `call-wait-room` · `success-toast-undo` · `interpret-drawer-lang` · ipad 나머지는 열지 않았다)
- `simulator-iphone-local-login.png`(실제 시뮬레이터)는 열지 않았다. mobile 보고 기준 로그인 화면 증거일 뿐이고, 인증 통합 증거가 아니다.

## 직원이 실물에서 만날 자리

- **로그인 뒤 실데이터는 아직 아무도 보지 못했다**(로그인 · 인증 통합 미실행). 실제 `needs` · `canRecall` · `lastSeconds` · `calls[]` 카운트가 화면에 어떻게 나오는지는 로컬 로그인 뒤 처음 확인된다. 로컬 `http://127.0.0.1:11040` 이 ATS 에 막히는지도 확인되지 않았다.
- dev(91728737)에 붙이면 옛 칸이라 확인 필요 · 마취 완료 · 재호출이 비어 보인다(D-6 — 의도된 비호환).
- 탭을 바꾸면 통역 드로어가 닫히고 대화가 지워진다(의도된 마이크 보호). 호출 시트 · 확인 창은 숨은 탭에 남아 있다가 돌아오면 다시 보인다.
- 폰 호출 시트 머리에 고객 이름이 없다(WARN-2).
- 호출 탭 · 시술 완료 탭 · 켜진 [시작]은 증거 없이 실물에서 처음 보인다(WARN-4).

## 남은 통합 의존

사용자 로컬 로그인 → 실데이터 눈 확인 · ATS · D-2 / D-3 / D-5 서버 · D-6(#920 · #236 머지 전 dev 옛 칸) · OQ-A8/A21/A24/A28 기본값 확인 · Apple 서명 · TestFlight(사용자).

## 수정 요청 (mobile 에게)

1. WARN-1: 캡처 fixture 의 `calls[]` 를 카드와 맞추고 다시 캡처.
2. WARN-2: 폰 호출 시트 `where` 를 「방 · 고객」으로(또는 코디가 원본 유지를 정하면 스펙 쪽을 정정).
3. WARN-3/4: 320 긴 이름(목록 + 상세) · 599/600 · 켜진 [시작] 캡처를 더한다. 선택: 호출 탭 · 시술 완료 탭.
