# 채팅 앱 구현 보고 — task_33cf78b10d47 / ctx_34c5e69ffee4

- 계약: DAY-SPEC-004 @ `53adbd49`(+ SPEC-003 셸·세션·푸시·테마, SPEC-000 device, SPEC-001 인증) · WPv7 승인본
- 원천: cc-prototype `77173cf8b62f0b27ec54ec4ee22e9d308b7f701e` — `git show`/`git archive` 로만 읽음(로컬 checkout 미사용·수정 0)
- 범위: `app/` 만. commit/push/merge 0 · 하위 위임 0 · backend/루트/deploy/스펙/GitHub 변경 0 · 다른 dirty(backend 워커 파일) 손대지 않음
- 결과: **코드 완료 · 검증 PASS / 활성화 전제 미충족(로컬 서버에 채팅 API 없음 — §6)**

## 1. 앱 변경 목록

| 구분 | 파일 | 내용 |
|---|---|---|
| 신규 data | `lib/chat/chat_model.dart` | SPEC-004 §3 모양 — id = uuid 문자열 · `seq` · `fromSeq` · `lastReadSeq` · 직무 `{key,name}`(OQ-C3) |
| 신규 data | `lib/chat/chat_api.dart` | 20개 경로 + 첨부 바이트. **세션 `api_base_url` 만 · Bearer 헤더만 · `followRedirects=false`** · 오류 `{detail,code,field}`→ApiError(code) · multipart 진행률(contentLength 고정) |
| 신규 data | `lib/chat/chat_stream.dart` | `GET /api/chat/stream` 전용 SSE(판 스트림과 같은 parser/opener·백오프 3→30s·45s idle·session_expired) · 연결/재연결마다 onConnected → 목록+since 메우기 |
| 신규 state | `lib/chat/chat_state.dart` | 프로토 ChatState 이식 — 이벤트 6종 · 읽음 `{seq}` · 서버 unreadRooms 정본 · 배너 messageId 1회 · 보내기/다시보내기(같은 clientId) · 세션 격리(`_disposed` 가드) |
| 신규 copy | `lib/chat/chat_copy.dart` | §3 오류 code→글자 표(경로별 글자는 ChatOp) · 모르는 code = 코드만 |
| 신규 UI kit | `lib/chat/chat_kit.dart` | DAY 에 없던 프로토 위젯(MsBadge·MsInput·MsCheckbox·MsCard·MsBanner·StatusChip·MiniChip·HeaderBack·DetailHeader→ChatDetailHeader·showAppSheet·SwitchRow·MsLabel) · `ChatScope`/`ChatApp`(프로토 AppScope 의 채팅 몫) · 세션 Navigator 입구 |
| 이식(거의 그대로) | `lib/chat/chat_view.dart` · `chat_search.dart` · `chat_link.dart` · `photo_pick.dart` · `video_pick.dart`(채널 `day/video`) · `chat_ui.dart`(역할 Badge = DAY 직무) | 원천 파일 첫 줄에 출처 |
| 이식 화면 9 | `lib/chat/screens/chat_{list,room,new,info,attach_sheet,forward_sheet,media,photo,video}_screen/sheet.dart` | 배치·문구 원문 그대로 · id→String · 정렬 seq · 오류 글자 code 표 · 대화상자/창/뷰어 → 세션 Navigator |
| 셸 | `lib/ui/shell.dart` | 「채팅」 자리 활성(ChatScreen) · 탭/레일 빨간 배지(서버 unreadRooms·99+) · 앱 안 배너 층(폰 위/아이패드 520 가운데) · 키보드 열리면 탭바 숨김 · **셸 전체를 감싸는 세션 Navigator**(세션 끝 = 대화상자·뷰어·동영상 함께 사라짐) · 4메뉴 유지 |
| 조립 | `lib/app.dart` | ChatState = 로그인 확정 세션 하나에 하나(Phase.board **및 forbidden** — board 권한 무관) · 세션 바뀜/세션 끝 = dispose · 생명주기 앞/뒤 · 채팅 전송을 `AppDeps.chatClient/chatSseOpener` 로 분리 가능 |
| 푸시 | `lib/state/push_coordinator.dart` · `lib/data/push_bridge.dart` | `kind: chat` 누름 = environment **및 hospitalId** 일치일 때만 그 방 · 앞에서 받음(`onForeground`) = 같은 조건으로 앱 안 배너 · 원장 호출 규칙 그대로 |
| 테마 | `lib/ui/theme.dart` | `Ms.cons/cons100`(상담사 Badge 색 — 프로토 tokens.dart:36-37) |
| 네이티브 | `ios/Runner/AppDelegate.swift` | `day/video` 채널(VideoConverter — 프로토 :343-446 그대로, 채널명만) · 채팅 willPresent → 시스템 배너 대신 Dart · 누름 칸에 hospitalId/roomId/messageId |
| 네이티브 | `ios/Runner/AcceptLogic.swift` | `PushPayload.tap/chatForeground` 순수 함수(시험 가능) |
| 네이티브 | `ios/Runner/Info.plist` | `NSCameraUsageDescription`(여권 부분만 삭제) · `NSPhotoLibraryUsageDescription` · `PHPhotoLibraryPreventAutomaticLimitedAccessAlert=true` · ATS 예외 0 |
| 의존 | `pubspec.yaml/lock` | image_picker 1.2.4 · flutter_image_compress 2.5.1 · photo_manager 3.12.0 · video_player 2.14.1 · url_launcher 6.3.3 — **프로토 lock 과 정확히 같은 버전** |
| 의존 lock(빌드 생성) | `ios/Runner.xcworkspace/.../swiftpm/Package.resolved` · `ios/Runner.xcodeproj/project.xcworkspace/.../swiftpm/Package.resolved` | flutter_image_compress 의 SPM 전이 의존 고정(SDWebImage 5.21.7 · SDWebImageWebPCoder 0.15.0 · libwebp-Xcode 1.6.0) — 커밋 여부는 코디 판단 |
| 시험 | `test/chat/chat_state_test.dart`(25) · `test/chat/chat_contract_test.dart`(11) · `test/ui/chat_ui_test.dart`(6) · `test/capture/chat_capture_test.dart`(16 장면, DAY_CAPTURE_DIR 없으면 skip) · `test/support/chat_fake.dart` · fixtures/ui_harness(채팅 더블 분리) · `ios/NativeLogicTests/main.swift`(+7) | |

## 2. 원천 기능 → 구현 → 검증 매핑 (누락 0)

| 기능 | 원천(77173cf8) | 구현 | 검증 |
|---|---|---|---|
| 목록 · 정렬 · 행 | screens/chat_list_screen.dart · chat/chat_ui.dart | screens/chat_list_screen.dart · chat_ui.dart | chat_ui_test 폰/아이패드 · capture 01 |
| 탭 배지(서버 unreadRooms) | screens/shell.dart:244-261 | ui/shell.dart `_TabIcon` | state「GET rooms」· ui「폰」 |
| 1:1 · 그룹 만들기(새 대화) | screens/chat_new_screen.dart | 같은 이름 | capture 03 · fake rooms/direct·rooms |
| 초대 | chat_info_screen → chat_new_screen(addTo) | 같음 | capture 04 |
| 나가기 · 숨기기 | chat_info_screen · chat_state leave/hide | 같음(op 별 오류 글자) | chat_copy 경로별 글자 test |
| 알림 끔(음소거) | chat_info_screen SwitchRow · setMuted | 같음 · 배너 억제 | state「알림 끈 방」 |
| 읽음(보고 있는 방 · 1초 묶음) | chat_state _markRead/_readSoon | `{seq}` · 응답 unreadRooms 정본 | state 읽음 2건 · ui 폰 `{"seq":2}` |
| 다기기 읽음 · 6 이벤트 | chat_state onEvent | 같음 + lastReadSeq | state 실시간 6종 7건 |
| 재연결 since · hasMore · 묘비 · from_seq 경계 | chat_state catchUp · _onDeleted | 같음 + memberKey(fromSeq) | state「놓친 것」·「chat_room 경계」·「deleted」 |
| 수정 · 삭제 | chat_room_screen 메뉴 · chat_state edit/delete | 같음 | state edited · copy test |
| 전달 | chat_forward_sheet · chat_state forward | 같음 · 실패 code 글자 | capture 07 · contract 전달결과 |
| 검색(초성) | chat/chat_search.dart | 그대로 | capture 07(검색칸) |
| 사진 · 동영상 보내기 · 진행 · 취소/다시 | photo_pick · video_pick · chat_attach_sheet · sendMany | 그대로(채널 day/video) | state 사진 multipart · 다시보내기 같은 clientId · capture 06·10 |
| 모아보기 | chat_media_screen | beforeSeq · seq 정렬 | 화면 이식 · fake attachments |
| 크게 보기 · 재생(Range) | chat_photo_screen · chat_video_screen | 세션 Navigator · Bearer 헤더 | capture 08 · contract videoUri origin |
| 푸시 누름 진입 | app_state _onTap · push.dart | push_coordinator(environment+hospitalId) | contract 푸시 3건 · ui 푸시 누름 |
| 앱 안 배너(SSE·앞 푸시 messageId 1회) | chat_state offerBanner · shell ChatBannerLayer · AppDelegate willPresent | 같음 | state 배너 4건 · ui 배너 · native 7건 |
| 없는 방 → 글자 → 목록 | chat_list_screen _onOpenRequest | 같음 | ui 푸시 누름 · capture 09 |
| phone/iPad 분기 | 화면 전반 isTabletWidth | 그대로 | capture phone/ipad 전 장면 · ui 아이패드 |

## 3. 격리 · 보안 확인

- 세션 묶음: ChatState·스트림·ChatApi 는 세션 하나에 묶이고 바뀌면 dispose(메모리·실패 말풍선·변환 임시파일 `deleteTemp`·배너/읽음 타이머·SSE). 늦은 401/2xx 무영향 → `chat_state_test「dispose 뒤 늦은 401·2xx」`, 로그아웃 후 재로그인 새 토큰만 → `chat_ui_test「로그아웃」`.
- 콜백은 `session.endSession(code, of: s)` 로 그 세션에 묶음(기존 epoch 보호 재사용).
- 토큰: 세션 origin 만 · 리다이렉트 안 따라감(302 시험) · 쿠키/`?token=` 없음. 동영상은 서버가 바이트 직접(§3·C-A10, 서명URL 없음) — AVPlayer 의 리다이렉트 헤더 동작은 실기기 pending.
- 대화상자·뷰어를 세션 Navigator 에 올려 세션 끝에 함께 사라짐(프로토는 루트).
- board 권한 없는 직원: Phase.forbidden 에서도 채팅 상태/스트림 시작(ui 시험). **단 SPEC-003 의 권한 화면에는 셸이 없어 채팅 탭 UI 로 들어갈 길이 없다** — 셸 정책 변경은 범위 밖이라 그대로 둠(코디 질문 1).
- 로그·보고에 토큰/실키/실사람 본문 0(시험 이름은 지어낸 값).

## 4. 검증 명령 · 실제 수

| 명령 | 결과 | 로그 |
|---|---|---|
| `fvm flutter test`(전체 · 최종 1회) | **240 passed · 43 skipped**(캡처 27+16) · 실패 0 — 기존 198 그대로 + 신규 42 | `chat-mobile-evidence/logs/flutter-test.txt` |
| `fvm flutter analyze` | No issues(1차 실행에서 캡처 시험 info 2건 → 고친 뒤 재실행 1회 — 정직 기록) | `logs/analyze.txt` |
| `sh tool/native_logic_test.sh` | **54 PASS / ALL PASS**(기존 47 + 채팅 푸시 7) | `logs/native-logic.txt` |
| `fvm flutter build ios --release --no-codesign` | 성공 · Runner.app 20.6MB | `logs/build-ios-unsigned.txt` |
| `fvm flutter build ios --simulator --debug` + 11040 defines 4개 | 성공 · Info.plist 권한 글자 · PHPhoto…=true · ATS 키 없음 확인 | `logs/build-ios-simulator.txt` |
| 시뮬레이터 overwrite install + launch | 이전 PID 45830 → **새 PID 45031** · uninstall/erase/logout 0 · 세션 유지(시술현황 로그인 상태 화면) | `logs/simulator-install.txt` · `simulator-after-install.png` |

## 5. 시각 증거(원형 대조)

- `chat-mobile-evidence/day/`(DAY 20장) · `proto/`(원형 18장 — 스크래치에 77173cf8 `git archive` 후 원형 FakeChat 으로 같은 지어낸 값·같은 장면, 프로토 저장소 수정 0) · `pairs/`(왼쪽 원형 | 오른쪽 DAY, 18쌍)
- 장면: 01 목록 · 02 대화 · 03 새 대화 · 04 초대 · 05 방 정보 · 06 첨부 · 07 전달 · 08 크게 보기 · 09 오류(없는 방)·안 읽음 · 10 보내기 실패(DAY 만)
- 차이(의도): 색 = DAY 토큰(주색 #1D8BFF) · 머리 「DAY」 · 4메뉴 · 역할 글자 = DAY 직무 이름(예 원장/코디네이터/상담실장). 배치·문구·크기 동일. 원형 아이패드 캡처는 가로(2388×1668), DAY 는 세로(1024×1366)라 쌍의 비율이 다름. 원형 「서버에 연결 중…」 줄은 원형 판 스트림 연결 줄(DAY 채팅 탭엔 없음 — SPEC-003 셸 그대로).

## 6. 제약 · pending

- **활성화 전제**: 지금 로컬 서버(127.0.0.1:11040)는 `/api/chat/rooms`·`/api/chat/stream` 404(무인증 탐침, `/api/board/stream` 401 로 서버 살아 있음 확인). 앱은 404 를 조용히 넘기고 스트림은 백오프 재시도 — 깨짐 없음. 채팅 백엔드가 그 서버에 배포/재시작돼야 실제 동작(서버 재시작·env·DB 손대지 않음).
- 실기기 pending: 사진첩 제한 접근 「더 고르기」·카메라·HEVC→H.264 변환·Range 재생·무음 스위치·APNs 채팅 푸시(앞/뒤/누름)·AVPlayer 리다이렉트 헤더. 위젯 시험은 API 성공을 실기기 성공으로 주장하지 않음.
- 네이티브 VideoConverter 는 컴파일(두 빌드)만 확인 — 변환 실행은 실기기 pending.
- 시뮬레이터 채팅 탭은 실제 조작하지 않음(사용자 세션·업무 데이터 보존).

## 7. 서버 요구 · 코디 질문

1. board 권한 없는 직원의 채팅 UI 진입: SPEC-003 Phase.forbidden(셸 없음) 유지가 맞는지, 셸+채팅 탭을 보여야 하는지(앱은 상태·푸시는 이미 시작).
2. 서버가 SPEC-004 그대로여야 하는 칸: `Room.fromSeq/lastReadSeq` · `Message.seq` · 읽음 응답 `lastReadSeq/unreadRooms` · `chat_read.lastReadSeq` · 푸시 `environment/hospitalId` · `/me` 의 `hospital.id`(푸시 병원 비교에 사용) · 첨부 리다이렉트 없음.
3. Package.resolved 2개(SPM 전이 고정)를 커밋에 포함할지.
