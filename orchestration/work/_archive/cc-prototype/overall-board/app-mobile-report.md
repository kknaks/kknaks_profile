# WORK-009 앱(mobile) 결과 보고 — WP-APP1 → APP6

## 상태: done — APP1 ~ APP4 · APP6 완료 · APP5 보류(코드 둠) · 실기기 확인(카메라 · 푸시 · KOS 쓰기)은 WP-E2E

공통
- 워크트리 `overall-board` · branch `kknaksss/overall-board-2` · 범위 `procedure/app/**` 만 · 커밋 없음
- 확인 back = **레포 밖 복사본**(scratchpad · `.env` 없음 → KOS 끔) · `PROC_FAKE_BOARD=1` · 임시 포트 **8791** · 지어낸 계정(`demo-*`). 사용자 8700 · 프로세스 안 건드림. back 코드는 backend 워커 진행 중(작업 트리 스냅샷)
- 스크린샷 = `flutter drive` + `integration_test/app_shots_test.dart`(WP · SHOT 인자) → `app-shots/APPn-{phone|tablet}-NN_*.png` · 시뮬레이터 iPhone 17 · iPad Pro 11"(M5)
- flutter = `~/fvm/versions/3.44.8`

## APP1 — 새 틀 (done)

### 수행
| 파일 | 내용 |
|---|---|
| `lib/screens/shell.dart`(새) | 폰 아래 탭바 4칸(예약 현황 · 내원 현황 · 시술 현황 · 설정) · 태블릿 왼쪽 레일 92px(「Céramique」 + 메뉴 4) · 탭마다 자기 Navigator(IndexedStack · 바꿔도 유지 · 같은 탭 다시 = 맨 위로) · `TabScaffold`(폰 = 공통 헤더 + 연결 줄 + 탭 머리) · `openNotifications`(폰 전체 화면 · 태블릿 오른쪽 시트) |
| `lib/widgets/header.dart` | `AppHeader`(가운데 Céramique · 종) · `Bell`(안 읽은 수 · 99+ · 0 이면 없음) · `TabHead`(태블릿은 끝에 종) · 시술 현황 탭 머리 = 「시술실 현황」 · 확인 N · 시계(로고 · 계정 ▾ 없앰 — D7-57) · `ConnectionLine` 그대로 |
| `lib/screens/settings_screen.dart`(새) | 계정(이름 · 역할 이름 · 아이디) · 알림(그 역할 받는 종류만 스위치 · 없으면 「받는 알림이 없어요」 · iOS 권한 거부면 「알림 꺼짐 · 설정에서 켜기」) · 이 기기(이름 고치기 → `POST /api/devices {token,name}` · 기기 행 없으면 안내 문구) · 앱 정보(버전 · 빌드 · debug 만 서버 주소) · [로그아웃] 빨강 |
| `lib/screens/notifications_screen.dart` · `lib/model/notification.dart`(새) | §6.13 목록(두 종류만 · 점 색 primary/cons · 안 읽음 파란 바탕 · [모두 읽음] · 빈 상태 문구) — 푸시 받기는 APP4 |
| `lib/screens/reservations_screen.dart` · `visits_screen.dart`(새) | 자리만(본문 APP3) · 첫 화면 = 예약 현황 |
| `lib/model/account.dart` | 역할 5(`coordinator` · `counselor` 더함) · 역할 이름 · 수락 묶음 `isAdmin` = admin \| coordinator \| counselor(§3.4) |
| `lib/app_state.dart` | 탭 상태 · `unread` · `deviceId`(응답 저장 · SharedPreferences · 로그아웃 · 계정 바뀜 때 지움 · SSE 쿼리) · 기기 이름 · `kind`(짧은 변 600) · 알림 누름 분기(원장 호출 → 시술 현황 탭 룸 · 상담사 호출 → 예약 현황 탭 그 예약) · SSE 붙을 때 · 앞으로 올 때 배지 다시 읽기 |
| `lib/api/api.dart` | `registerDevice(token,{name,kind}) → deviceId` · 알림 4(목록 · 읽음 · 설정 GET/PUT) · `streamUri(deviceId:)` |
| `lib/sse/board_stream.dart` | `board` 밖 `display` · `notification` 을 version 규칙 없이 `onEvent` 로(§7.1 r2) |
| `lib/push/push.dart` · `ios/Runner/AppDelegate.swift` | `PushTap`(kind 없음 = doctor_call · counselor_call · display) · onTap 에 payload 키 5개 전달 · 채널 `deviceName` · `appVersion` |
| `lib/main.dart` · `login_screen.dart` · `Info.plist` | 로그인 뒤 = Shell · 로그인 제목 「예약 · 시술 현황」 · 앱 이름 「Céramique」(`CFBundleDisplayName` · MaterialApp title) |
| `lib/theme/tokens.dart` | `cons` #15803D · `cons100` #E7F4EC(웹 globals.css 값) |
| `integration_test/app_shots_test.dart`(새) · `screens_test.dart` | 스크린샷 순회 · 기존 순회는 로그인 뒤 시술 현황 탭을 눌러 들어감 |

### 검증
- `flutter analyze` → No issues found
- `flutter test` → **63 passed**(기존 62 + payload 종류 1 · 기기 시험 고침: deviceId 저장 · SSE 쿼리 · 로그아웃 때 지움)
- 시뮬레이터: `APP1-phone-01..06` · `APP1-tablet-01..06`(로그인 · 4탭 · 설정 · 알림 목록). 시술 현황 탭 = 기존 카드 · 필터 · [수락] 그대로(회귀 없음)

### 계약 대조
- §6.8 탭바 · 레일 · 공통 헤더 · 종 배지 · 탭 스택 · 연결 줄 · 첫 화면 = 같음. 아이콘은 시안이 빈 네모라 Material 아이콘(DS 기본값)
- §6.14 = 같음(지점 · 구역 · 언어 없음)
- §5-1.3 / §5-2 누르면 탭 바꾸기 = 같음(예약 상세 열기는 APP3 에서 `openReservation` 을 받음)
- 태블릿 레일 글자는 배율 없이 고정(92px 폭 넘침 방지)

### 이슈
- 시뮬레이터에서도 APNs 토큰이 오는 경우가 있어(iPad) 태블릿 설정은 「기기 이름」 줄이 보임 · 폰은 안내 문구

## APP2 — 웹 따라잡기 (done)

### 수행
| 파일 | 내용 |
|---|---|
| `lib/view/state.dart`(새) | 2계층 표 한 곳 — 웹 `reservations/view.tsx` `MAIN_NAME` · `SUB_NAME` · `MAIN_TONE` · `phaseStyle` · `barStyle` · `headOf` · `LEGEND` · `stateText` + `procedures/view.ts` `STATE_2` · `stateBadge` · `procChip` 를 Dart 로(값 새로 안 정함 · 예약 · 내원 현황(APP3)도 이것을 씀) |
| `lib/view/view.dart` | 카드 순서 = 스냅샷 배열 그대로(정렬 제거) · 보이는 작업 = `isRoomTask` 만 뺌(ETCETERA 도 시술 줄 · n/m · 막대도) · 시술 차례 = 진행 → 대기 → 완료(웹 `orderedProcs`) · 카드 배지 = 확인 필요(danger 점) > 마취 중(purple 점) > 2계층 칩(점 없음) · **「시술 완료」 배지 없앰** → 웹 글자 「시술 모두 완료 · 귀가 대기 전」 · 필터 점(웹 `FILTERS` — 대기 ○ · 진행 ● · 귀가 = 귀가 대기 ○ · 수락 대기 점 없음) |
| `lib/model/board.dart` | `isRoomTask` · `canUndoStart` · `canUndoFinish`(없으면 꺼짐) |
| `lib/widgets/undo_sheet.dart`(새) | 되돌리기 아이콘 · 확인 시트(폰 바텀 · 태블릿 가운데 · 웹 `UNDO_TITLE` 글자 · [취소] / [되돌리기]) · [시작] · [종료] 성공 토스트 [되돌리기](5초) · 되돌린 토스트 = 웹 `UNDONE` 글자 |
| `lib/widgets/ui.dart` | `MsBadge.of` · `MsBadge.chip`(2계층 색) · `Toaster` 버튼(있을 때만 누를 수 있음 · 5초 / 없으면 2.6초) |
| `lib/screens/room_screen.dart` | 시술 줄 오른쪽 = 「호출함」 → 부상태 칩 → 되돌리기 아이콘 → 버튼(완료 줄 = 아이콘 → 「완료」 칩 · 웹 OrderCard 차례) |
| `lib/screens/board_screen.dart` | 카드 이름 + 한글 발음(회색 · 발음 먼저 말줄임 · 없으면 안 그림) · 필터 칸 점 |
| `lib/api/api.dart` | `undoStart` · `undoFinish` |

### 검증
- `flutter analyze` 0 · `flutter test` **69 passed**(새: `state_test.dart` 5 — 2계층 글자 · 색 · 머리 · 막대 · 범례 · 시술 매핑 · 토스트 버튼 / `view_test` 고침 — 배열 순서 · `isRoomTask` 만 숨김 · ETCETERA 줄 · 배지 2계층 · 「시술 완료」 없음 · 되돌리기 = 스냅샷 값)
- 시뮬레이터 `APP2-{phone,tablet}-01_board · 02_room_doing · 03_undo_confirm · 04_room_done` — 가짜 판(웹과 같은 스냅샷 값)

### 계약 대조
- 부록 D #1 ~ #5 = 같음. §6.9 시술 현황 칸 = 같음
- 웹과 다름: 아이콘 = Material `undo_rounded`(웹 medikit ResetIcon 뒤집기와 모양 비슷 · 36pt 누름 칸) · 웹 호버 툴팁 없음(D7-65)

### 이슈
- 가짜 판은 조작 403(`fake_board`)이라 토스트 [되돌리기] 는 단위 시험으로만 봄 — 실제 [시작] → [되돌리기] 는 WP-E2E 데모 back 에서
- 웹과 나란히 둔 스크린샷(완료 조건 문구)은 앱 쪽만 찍음 — 웹은 같은 가짜 판(`PROC_FAKE_BOARD`) 화면이라 E2E 때 나란히 보면 됨

## APP3 — 예약 현황 · 내원 현황 · 예약 상세 (done · 쓰기 실제 반영은 E2E)

### 수행
| 파일 | 내용 |
|---|---|
| `lib/model/reservation.dart`(새) | SPEC-005 §7.2 · §7.3 응답(back `schemas/reservations.py` 이름 그대로 · 모르는 키 무시) · 띄우기 대상 |
| `lib/view/resv_view.dart`(새) | 웹 `view.tsx` 의 KST 시각 · 날짜 · 정원 글자 · 금액 · 국가 표(67개 그대로) · 국기(iOS 국기 글자 — 웹 flag-icons 대신) · 폰 30분 시간대 · 지금 시간대 |
| `lib/widgets/resv_ui.dart`(새) | 예약 카드(막대 · 성별 · 초진/재진 · 부상태 칩 · 국기 · 발음 · 수납 필요 · 취소/부도 흐림+줄) · 범례 7(개수) · 상태 칩 · 원내 카드(전체 · 결제 · 수납 필요) |
| `lib/screens/reservations_screen.dart` | ‹ 날짜 › · [오늘] · 범례 · 총 예약 N건 / 폰 = 칩 줄(전체 + KOS 그룹 · 구역 칩 없음) + 30분 목록(지금 줄 파란 바탕) / 태블릿 = 시간 × 칸 표(가로 스크롤 · 시각 열 · 열 머리 고정 · 1시간 같은 높이 · 칸마다 간격 · 운영 밖 회색 · 지금 선 · 칸 머리 「{정원} / {간격}분」) · 첫 렌더 지금 시각 스크롤 · 10초 폴링(앱 앞 + 이 탭) · 상담사 호출 푸시 → 그 예약 상세(상담 카드로 스크롤). [+] · 드래그 · 등록 · 공지 · 요청 없음 |
| `lib/screens/visits_screen.dart` | 웹 원내 현황 그대로 — 필터 5(점 · 수) · 구역 order 묶음 · 0 명 구역 안 그림 · 「귀가 대기」 수납 필요 먼저 · 오늘만 · 태블릿 = 카드 격자 · 10초 폴링 |
| `lib/screens/reservation_detail_screen.dart`(새) | 위 막대 = 상태 색(웹 `headOf`) · 머리 줄(국적 · 성별 · 만 n세 · No. · 날짜 시각 · 구역 · 칸 · 방) · 접수(진행 경로 · 시술실 시트 — 사용 중 위 회색 · 「{구역} · 빈 방 N개」 · [접수 완료 · 방]) · 내원 현황 단계 카드(지난 회색 · 지금만 그 색 · [+ 상담 추가] · 상담사 시트 비어있음 먼저 → [○○ 실장 호출] · 「실장 호출됨 · HH:MM」 · [시술 현황 ›] → 시술 현황 탭 그 방) · 귀가 대기 정산 **글자만**(전체 · 결제 · 수납 필요 N건 · 처방전 N건 / 오늘 처방전 없음) · [귀가 완료] → 닫고 토스트 · 신분 확인([확인 완료] / [미확인으로] · 앱 스캔 · 손 입력 줄 · **[여권 스캔]**) · 고객 기본 정보(웹 칸 · 연락처 보임 · [수정] = 바꾼 키만 PUT) · 예약 메모 · 주의사항 [저장] · 건강 정보(빈 = 「고객이 문진을 작성하면 채워집니다」) · 이전 방문 · [예약 취소](취소 / 부도) · **[태블릿에 띄우기]**(targets 시트 · 접속 중 점 · 오늘 제출 안내) · **[이 기기에서 열기]** · 5초 폴링(맨 위 화면일 때) · 409 · 403 = 토스트 + 다시 부름. 켜짐 = `can.*` 그대로. 수납 · 처방전 · 리포트 버튼 · [스캔할 기기] 없음 |
| `lib/screens/launchers.dart`(새) | [태블릿에 띄우기] 시트 · 문진 · 스캔 여는 자리(APP5 · APP6 에서 채움) |
| `lib/api/api.dart` | 예약 GET 2 · 쓰기 9(cancel · reception · counselor-call · consultation-add · discharge · memo · remark · personal · identity) · `devices/targets` · `display-requests` |

### 검증
- `flutter analyze` 0 · `flutter test` **75 passed**(새 `resv_test.dart` 6 — KST · 날짜 · 금액 · 정원 글자 · 국가 · 국기 · 30분 목록 · 그룹 거르기 · 지금 줄 · 2계층 읽기 · 원내 묶음 · 귀가 대기 수납 먼저 · `can` 그대로)
- 시뮬레이터(back 실제 코드 · 임시 포트 8791 · `PROC_FAKE_BOARD=1` 가짜 KOS 판): `APP3-phone-01..08`(예약 현황 · 상세 접수 전 · 접수 상자 · 시술실 시트 · 내원 현황 · 상세 접수 뒤 · 고객 정보 · 귀가 대기 정산) · `APP3-tablet-01..06`(시간 × 칸 표 · 두 열 상세)

### 계약 대조
- §6.10 · §6.11 표 · §6.12 = 같음. 상세 버튼 켜짐 = `can.*` · 접수 상자 보임 = 웹 `showReceiveBtn`(receiveMode · 예약 · 부도)과 같음
- 웹과 다름(꼴만): 국기 = iOS 국기 글자 · 폰 상세 차례 = 접수 · 내원 현황 먼저(지금 할 일) · 고객 정보 고치기 = 시트(주소 · SNS · 국적 칸은 웹에서 — 앱 시트엔 이름 · 발음 · 생년월일 · 이메일 · 여권 4칸 · 휴대폰)

### 이슈 · 코디가 확인할 것
- **쓰기 1회씩(웹 반영 확인)은 못 함** — 가짜 판(`PROC_FAKE_BOARD`)은 쓰기가 403 `fake_board` · 실제 KOS 데모 쓰기는 사용자 허가 · `.env` 가 필요해 WP-E2E 로 넘김(앱은 응답 `message` 토스트 + 다시 부름까지 확인)
- 시뮬레이터 알림 권한 창이 앱 위에 남으면 캡처가 흰 화면 — 스크린샷 순회는 푸시 채널 없이(`--dart-define=PUSH` 없음) 찍음

## APP4 — 알림 목록 · 상담사 푸시 받기 · 띄우기 받기 (done · 실제 배너는 실기기)

### 수행
| 파일 | 내용 |
|---|---|
| `lib/screens/notifications_screen.dart` · `lib/model/notification.dart` | (APP1) 목록 + `target.callId`(후속 #4) · 누르면 읽음(ids) → 원장 호출 = 시술 현황 탭 룸 · 상담사 호출 = 예약 현황 탭 예약 상세 · SSE 배지 바뀌면 다시 읽음 |
| `lib/model/display.dart`(새) | pending · claim 항목(코디 확정 모양 #1) · `ccc://display?t=` 만 받기 · SSE `display` 자기 `deviceId` 만 |
| `lib/app_state.dart` | SSE `display`(자기 기기) → `GET pending?deviceId=` · 띄우기 푸시 누름 · 로그인 · 앞으로 올 때 · 기기 등록 직후 pending · 열 차례(중복 · 닫힌 것 빼고 오래된 것 먼저) · [QR 읽기] → `claim {qrToken, deviceId?}` · 푸시 누름 → `POST /api/notifications/read {callId | reservationId}`(후속 #3) + 배지 다시 · 로그아웃 때 차례 비움 |
| `lib/screens/shell.dart` | 띄우기 차례를 하나씩 연다(문진 / 스캔 — 그 화면이 끝날 때까지 다음은 기다림 · OQ-621) |
| `lib/screens/launchers.dart` | `openDisplay` — 문진 = §6.15 · 스캔 = 예약 상세를 읽어 §6.16 |
| `lib/screens/reservations_screen.dart` | 머리 오른쪽 **[QR 읽기]**(카메라 → claim) |
| `lib/scan/scan_channel.dart` · `ios/Runner/TextScanner.swift`(새 · pbxproj 등록) · `AppDelegate.swift` | 채널 `procedure/scan` — `scanQr`(AVFoundation QR) · `takePassportPhoto`(APP6) · `recognizeText`(APP6) · 카메라 없음 = `no_camera` |
| `Info.plist` | `NSCameraUsageDescription`(QR · 여권 · 사진첩 저장 안 함) |
| `lib/api/api.dart` | pending · claim · close · 읽음 `callId` / `reservationId` |

### 검증
- `flutter analyze` 0 · `flutter test` **83 passed**(새 `display_test.dart` 7 — 자기 기기만 · QR 꼴 · pending 모양 · 차례 · **SSE `board` 만 version · `id:` 없는 `display` · `notification` 받음 · version 안 건드림** · 배지 · 알림 둘만 / `push_test` +1 — 누름 → 탭 · 읽음 본문 · 상담사 = 수락 관리자 묶음)
- 시뮬레이터(back 실제 코드 8791): `APP4-phone-01..04`(종 배지 · 목록 둘(점 primary / cons) · 상담사 호출 누름 → 예약 현황 탭 그 예약 상세 · 읽은 뒤 배지)

### 이슈
- **`xcrun simctl push` 배너 확인 못 함** — 스크린샷 순회는 알림 권한 창을 피하려고 푸시 채널을 끄고 돌림 · 시뮬레이터에 알림 권한을 미리 줄 방법(simctl privacy 에 알림 없음)이 없어 배너가 안 뜸. 누름 길은 `push_test` 로 · 실제 배너 · 소리 · 알림 [수락]은 WP-E2E 실기기
- [QR 읽기] · 띄우기 SSE 실제 열림은 카메라 · 두 기기가 필요해 E2E(시뮬레이터 = 「카메라를 쓸 수 없어요」 토스트)

## APP5 — 문진 화면 (done · 데모 제출은 BE4 가 함 · 앱 화면 제출은 가짜 KOS)

### 수행
| 파일 | 내용 |
|---|---|
| `lib/screens/questionnaire_screen.dart`(새) | 루트 내비게이터 전체 화면(탭바 · 레일 · 공통 헤더 가림) · `PopScope(canPop:false)`(뒤로 · 가장자리 밀기 막음) · 토스트(앱 안 배너) 끔 · 언어 칩 6(back 이 정한 언어 고른 채 · 바꾸면 다시 부르지 않고 받은 번역 안에서) · 「{이름} 님」 [시작] → 기본 정보(미리 채움: 이름 · 생년월일 `yyyyMMdd`(후속 #2) · 성별 · 휴대폰 `{countryCode, phoneNumber}`(후속 #5) · 주소 · 상세) → KOS 양식 쪽마다(CHECK_BOX 여럿 · SELECT_BOX 하나 · INPUT_BOX 글 · `isSubText` 고르면 글칸 · 필수 = KOS 값) → 동의(약관 키 ja · en · zh · 필수 안 하면 [제출] 꺼짐) → 제출 → 「감사합니다」 → 3초 뒤 **잠긴 대기 화면**(다음 문진 요청이 오면 바로 연다) · 실패 = 그 언어 「제출하지 못했어요 · 직원에게…」 + [다시 제출] · 입력 유지 · **[직원] 1.5초 길게 → 비밀번호 → `POST /api/auth/unlock {password, deviceId?}`** · 401 · 429 = back 문구 그대로 · 나가면 제출 전 띄우기 요청 `canceled` |
| `lib/model/questionnaire.dart`(새) | 양식 · 번역(`translsMap.title.translation[lang]` · 없으면 원문) · 답 모음 → 제출 `answers[]`(고른 선택지 한 줄씩 · 키 7개 · `title` · `parentQuestionTitle` 원문 한국어) |
| `lib/l10n/questionnaire_text.dart`(새) | 화면 틀 고정 문구 6개 언어(ko · ja · zh-Hans · zh-Hant · en · id) |
| `lib/api/api.dart` | 문진 GET(`?deviceId=` · 기기 없으면 뺌) · POST · unlock |
| `lib/widgets/ui.dart` | `Toaster.muted`(잠금 동안) |
| `lib/screens/launchers.dart` | [이 기기에서 열기] · 띄우기(문진) → 이 화면 |

제출 본문 = `{displayRequestId?, deviceId?, language, name, dateOfBirth(yyyyMMdd), gender, phone, address, addressDetail, agreements[{…, agreed}], answers[]}` — **`registrationNumber` · `phoneticName` 없음**(주민번호 칸 없음 · D7-16 Q-152)

### 검증
- `flutter analyze` 0 · `flutter test` **87 passed**(새 `questionnaire_test.dart` 4 — answers 키 7개 · 원문 title · subText · inputText · SELECT 하나 · 약관 키 / **잠금: 뒤로 가기 막힘 · 대기 화면도 막힘** · 언어 칩 바꿔도 다시 안 부름 · 토스트 끔 / 제출 본문(언어 · yyyyMMdd · displayRequestId · 주민번호 · 발음 없음 · agreed) / **[직원] 0.5초 = 안 열림 · 1.6초 = 열림 · unlock 429 문구 그대로**)
- 시뮬레이터 `APP5-phone-01..13`: 시작 ja · ko · en(언어 3가지) · 기본 정보 · 4쪽 · 동의 · 감사 · 잠긴 대기 · 틀린 비밀번호(실제 back unlock 401 문구) · 맞는 비밀번호 → 나감(예약 상세로)

### 계약 대조 · 이슈
- §6.15 ① ~ ⑦ · 잠금 = 같음. 양식은 scratch back 의 **가짜 문진 응답**(KOS 꺼짐 — 지어낸 4쪽 · 6개 언어 · 레포 밖)으로 그림 — 실제 KOS 양식(4쪽 15질문)은 키가 같다고 보고(BE4 · app-kos-report §4) E2E 에서 확인
- 질문 「필수」 키 이름이 KOS 응답에 무엇인지 문서에 없음 → `required` · `isRequired` · `essential` 셋 중 하나면 필수로(없으면 모두 선택). 실제 양식에서 다르면 알려 주세요
- 시뮬레이터는 기기 행이 없어(알림 권한 없음) `deviceId` 없이 보냄 — back 「기기 없음」 칸 길

## APP5 보류 — 어디까지 했나 (코디 지시 2026-10-27 · 사용자: 「문진은 고객이 웹에서 한다(앱 아님)」)
- 상태: **보류** · 코드는 지우지 않고 그대로 둠(위 APP5 절의 파일 전부 · 시험 4 포함 · analyze 0 · test 87)
- 된 것: 문진 화면 전체(잠금 · 언어 칩 6 · 기본 정보 미리 채움 · KOS 양식 쪽 · 동의 · 제출 · 실패 · 감사 · 잠긴 대기 · [직원] unlock) · 시뮬레이터 13장 — 가짜 문진 응답(scratch)
- 안 한 것: 실제 KOS 양식으로 앱 화면 제출(E2E) · 필수 키 이름 확인
- 그대로 둔 길(손대지 않음 · 지시 기다림): 앱 예약 상세 [태블릿에 띄우기] → 기기 시트 → `POST /api/display-requests {kind:"questionnaire"}` · 띄우기(SSE · 푸시 · pending · QR)로 문진 요청이 오면 이 화면이 열리는 길 · [이 기기에서 열기]

## APP6 — 여권 스캔 · 스캔 확인 (done · 카메라 · 저장 실반영은 실기기 E2E)

### 수행
| 파일 | 내용 |
|---|---|
| `lib/scan/mrz.dart`(새) | TD3(두 줄 · 44자) · ICAO 9303 검사 숫자(여권번호 · 생년월일 · 만료일 · 종합) · 날짜 칸 글자 헷갈림 고침(O→0 등) · **세기: 생년월일 20YY 가 오늘 뒤면 19YY · 만료일 늘 20YY**(r2) · 이름 `<` → 공백 · alpha-3 → alpha-2 표(모르는 코드 = 빈 값) · 줄 쪼개짐 · 88자 한 덩어리 · 첫 줄 끝 `<` 덜 읽힘 처리 · **법적 검토 주석 ⑤**(여권 TD3 만 · 주민번호 신분증 = 마스킹 자리) |
| `lib/scan/scan_channel.dart`(새) · `ios/Runner/TextScanner.swift`(APP4 에서 등록) | 카메라 = `UIImagePickerController` + **가이드 틀 오버레이**(사진면 125 × 88 · 아래 MRZ 점선 · 「여권 사진면을 틀에 맞춰 주세요」 · 빛 반사 안내) · JPEG 긴 변 2000 · 0.8 · **기기 안 Vision `VNRecognizeTextRequest`**(외부 서비스 0) · 사진은 메모리로만 Dart 에 · **법적 검토 주석** |
| `lib/screens/scan_screen.dart`(새) | 찍기 → 읽기 → 틀리면 「읽지 못했어요 · 다시 찍어 주세요」(n / 3) → **3번 실패 → [손으로 입력]**(빈 확인) · 카메라 없음 = 바로 [손으로 입력] · 확인 = 「읽은 값」(고침) ↔ 「KOS 지금 값」(예약 상세 `personal`) 나란히 · 다른 칸 강조 · **name 칸 없음**(D7-53) · 사진 작게 · [다시 찍기] · [저장] → 바꾼 칸만 multipart(`fields` · `photo` · `reservationId` · `displayRequestId?` · `deviceId?` · `manual`) · 실패 = 「저장하지 못했어요 · {message}」 + [다시 저장] · 결과 = 고객 정보 · **ccc 사진 · KOS 사진 따로 한 줄**(ok · disabled / ok · failed · skipped — 후속 #6) · KOS 실패 → **[사진 다시 올리기]**(kos-retry) · 원본 = 저장 성공 · [다시 찍기] · [닫기] 때 버림(사진첩 · 파일 0) · **법적 검토 주석 ④** · 띄우기로 열렸는데 저장 전 [닫기] = 요청 `canceled` |
| `lib/api/api.dart` | `passportScan`(multipart · `http_parser` 로 `image/jpeg`) · `photoKosRetry` |
| `pubspec.yaml` · `pubspec.lock` | `http_parser ^4.1.2` 직접 의존(이미 http 가 쓰던 판 · lock 은 「transitive → direct main」 한 줄) |
| `lib/screens/launchers.dart` | 예약 상세 [여권 스캔] · 띄우기(scan) → 이 화면 |

### 검증
- `flutter analyze` 0 · `flutter test` **97 passed**(새 `mrz_test.dart` 6 — ICAO 견본(L898902C3 · ERIKSSON ANNA MARIA · UTO = 빈 국적) · 지어낸 견본 · 검사 숫자 틀림 = null · 세기 규칙 · 글자 인식 잡음 / `scan_test.dart` 4 — 바꾼 칸만 · **3번 실패 → [손으로 입력] → manual=true multipart** · MRZ 읽힘 → 바꾼 칸만 · 카메라 없음 길)
- `grep "법적 검토 필요"` 앱 = **6곳**(scan_screen 2 · mrz 1 · scan_channel 1 · api 1 · TextScanner.swift 1) ≥ 2
- `flutter build ios --no-codesign` → **Runner.app 빌드됨**(25.2MB · 서명 없음)
- 시뮬레이터 `APP6-phone-01..04`: 카메라 없음 → 손 입력(빈) → 지어낸 값 입력(다른 칸 강조) → 저장 = 가짜 판 403 문구 + [다시 저장]

### 이슈 · 코디가 확인할 것
- **카메라 취소 = 스캔 닫기**(§6.16 ① [닫기] 그대로 → 예약 상세). 손 입력은 3번 실패 · 카메라 없음에서만 — 「취소 → 손 입력」 으로 바꿀지 결정 필요하면 알려 주세요
- iPhone 17 시뮬레이터는 카메라 「있음」으로 열려 시스템 카메라에서 멈춤 → 스크린샷 순회만 **시험 스위치**(`integration_test` 에서 `openPassportScan` 을 카메라 없는 채널로 바꿔 열기 · 앱 코드 그대로)
- 카메라 · Vision 실제 읽기 · 저장 실반영(KOS 고객 수정 · ccc 사진 · KOS 이미지)은 실기기 · 데모 back 에서(WP-E2E). back BE5 데모 1회는 이미 함(지어낸 TEST 그림)
- 손 입력은 사진이 없으면 back 이 400(`photo` 필수) — 실기기는 3번 찍은 마지막 사진이 붙고, 카메라 없는 기기에서만 해당

---

## 전체 요약
- 바뀐 파일: `procedure/app/**` 만(수정 23 · 새 28 — `git status` 그대로) · 커밋 없음
- 검증: analyze 0 · test **97 passed**(시작 62) · `flutter build ios --no-codesign` 됨 · 스크린샷 `app-shots/APP1 ~ APP6-*`(APP1 · 2 · 3 폰 + 태블릿 · APP4 · 5 · 6 폰)
- 확인 back: 레포 밖 복사본 · 임시 포트 8791(끝나고 내림) · KOS 끔 + 가짜 판 · 지어낸 계정 · 사용자 8700 · 프로세스 안 건드림
- 데모 흔적(앱 쪽): **없음**(KOS 쓰기 0 — 모든 쓰기는 가짜 판 403 또는 scratch DB). scratch DB 에 지어낸 알림 3행 · 가짜 문진 제출 1건(레포 밖)
- 미결(WP-E2E 실기기): 예약 쓰기 1회씩 웹 반영 · 푸시 배너 · 알림 [수락] · 띄우기 SSE 두 기기 · [QR 읽기] · 카메라 + Vision 실제 MRZ · 스캔 저장 실반영 · APP5 보류 결정

## 리뷰 r1 수정 (mobile 몫 — FAIL-2 짝 · W1 · W3 · 2026-10-27)

| # | 고친 곳 | 내용 |
|---|---|---|
| FAIL-2 짝 | `lib/screens/scan_screen.dart` | **손 입력 = 사진 없이 저장** — [손으로 입력]을 누르면 읽지 못한 사진을 그 자리에서 버리고(메모리) 저장 multipart 에 `photo` 칸을 **보내지 않는다**(`manual=true`). 카메라로 읽은 길은 그대로 사진 필수. 응답 `photo: null` 이면 결과 = 「사진 없음 · 손으로 입력」(ccc · KOS 사진 줄 · [사진 다시 올리기] 없음) — 전엔 null 을 「KOS 사진 · 실패」로 잘못 그렸을 길을 막음 |
| W1 | `lib/app_state.dart` · `lib/screens/questionnaire_screen.dart`(한 줄) | 이미 연 띄우기 요청 id 를 기억(`_openedDisplays`) — 앞으로 올 때(`resumed`) · SSE · 로그인 때 `pending` 이 opened 를 다시 돌려줘도 차례에 안 넣는다 · 문진 대기 화면이 직접 연 것도 같은 기억에 넣음(`markDisplayOpened` · APP5 보류 코드는 이 한 줄만) · 로그아웃 때 비움 |
| W3 | `lib/app_state.dart` | 알림 목록 항목 누름 = 목록이 그 항목 **`ids`** 로 읽음(그대로) · 이어지는 화면 열기(`openNotification`)는 `callId` · `reservationId` 로 **또 읽지 않는다**(`markRead:false`). 푸시를 눌러 연 때만 발송 단위 읽음 |

### 검증
- `flutter analyze` 0 · `flutter test` **98 passed**(+1 · 고침: `scan_test` 손 입력 multipart 에 `photo` 없음 · 카메라 길은 `photo` 있음 · 새 「photo: null → 사진 없음」 / `display_test` 연 요청 다시 안 넣음 · 대기 화면이 연 것도 / `push_test` 목록 누름 = 읽음 요청 0 · 화면은 열림)
- 시뮬레이터 1회(임시 back · scratch 8791 · 끝나고 내림): 예약 상세 [여권 스캔] → 카메라 없음 → [손으로 입력] → 지어낸 값 → [저장] → back 이 받은 것 = `manual: true` · **`photo` 없음** · `fields` = 바꾼 4칸 · `reservationId` → 화면 「저장했어요 · 사진 없음 · 손으로 입력」(`APP6-phone-04_scan_save_result.png` 새로 찍음)
- 단, back FAIL-2(사진 없이 받기)는 아직 작업 트리에 없어 scratch 쪽 `passport-scan` 은 **받은 multipart 를 기록하는 가짜**(KOS 꺼짐 · 레포 밖)로 받음 — 실제 back 고친 뒤 E2E 에서 한 번 더

---

## E2E batch 1 (2026-10-28 · branch `kknaksss/overall-board-3` · base `f8a3751`) — mobile #1 · #2 · #3 · #5 · #6 done(실기기 확인 남음) · #4 되돌림

공통: 범위 `procedure/app/**` 만 · 커밋 · push · 업로드 없음. 확인용 back = 레포 밖 복사본(scratchpad · `.env` 없음 → KOS 꺼짐 · `PROC_FAKE_BOARD=1` · 지어낸 계정 `demo-coord` · 임시 포트 **8791** · 끝나고 내리고 복사본 지움). 사용자 8700 · 프로세스는 건드리지 않음.

### 수행
| # | 파일 | 내용 |
|---|---|---|
| 1 installId | `ios/Runner/AppDelegate.swift` · `lib/push/push.dart` · `lib/api/api.dart` · `lib/app_state.dart` | 채널 `installId` = 키체인(`procedure.install` · 이 기기만 · 첫 잠금 해제 뒤)에 둔 값 · 없으면 `identifierForVendor`(없으면 UUID)를 처음 한 번 저장. back 확정 모양 그대로 `POST /api/devices {token, name?, kind?, installId?}` — 못 얻으면 키를 뺌. 토큰 등록 · 이름 시트 · 설정 이름 고치기 모두 실음 |
| 1/3 등록 순서 | `lib/app_state.dart` | **등록을 한 번에 하나씩**. 로그인 때 저장된 옛 토큰 등록과 새 토큰 등록이 겹치면, 늦게 온 옛 응답이 `deviceId` 를 옛 행으로 되돌리고 SSE 를 그 id 로 다시 열 수 있었음(시험으로 막음). 같은 원인으로, 기다리는 동안 사용자가 정한 이름을 `UIDevice.name`(「iPhone」)으로 덮던 `deviceName ??= await …` 도 고침 |
| 2 기기 이름 | `lib/screens/shell.dart` · `lib/app_state.dart` · `lib/screens/settings_screen.dart` | 로그인 뒤(이미 로그인한 옛 설치도 한 번) **이름을 정한 적이 없으면 「이 기기 이름」 창**(예: 데스크 태블릿 · 코디 폰 · 40자) — [저장] = 이 기기에 저장 + 토큰이 있으면 바로 등록 · [나중에] = 기본 이름 그대로 · 둘 다 다시 묻지 않음(`device.nameAsked`). 띄우기 화면이 열려 있으면 그게 끝난 뒤 뜸. 설정 「이 기기」 = 이름 줄 늘 보임(기기 행이 없으면 「알림을 켜면 웹 기기 목록에 보여요」 한 줄 더). entitlement 신청은 하지 않음 |
| 3 SSE display | `lib/app_state.dart` | ① 받은 `display` 프레임(`{requestId, deviceId, kind, reservationId}`)으로 **바로 차례에 넣음** — 전에는 pending GET 이 성공해야만 열렸음. 이어서 pending 도 읽음(opened 표시 · 놓친 것) · 같은 요청 두 번 안 엶 ② SSE 가 다시 붙을 때도 pending 읽기 ③ 위 등록 순서 고침 |
| 5 ccc 딥링크 | `ios/Runner/Info.plist` · `AppDelegate.swift` · `lib/push/push.dart` · `lib/app_state.dart` | `CFBundleURLTypes` 스킴 `ccc` · `FlutterDeepLinkingEnabled=false`(Flutter 가 링크를 화면 경로로 밀지 않게). 장면 생명주기 플러그인 대리자(`registrar.addSceneDelegate` — `willConnectTo` 의 urlContexts(꺼진 상태) · `openURLContexts`(켜진 상태)) + `application(_:open:)` → Dart `onLink` / 준비 전이면 `takeLink`. Dart: `ccc://display?t=` 만 받음 → 로그인 돼 있으면 `claim {qrToken, deviceId}` · 아니면 토스트 「로그인하면 고객 입력 화면을 열어요」 후 로그인 뒤 claim(기기 등록 뒤 — deviceId 실음) |
| 6 여권 연속 스캔 | `ios/Runner/TextScanner.swift` · `lib/scan/scan_channel.dart` · `lib/screens/scan_screen.dart` | `UIImagePickerController` 한 장 촬영 → **`PassportScanController`(AVCaptureSession)**. 카메라 = `builtInTripleCamera` → `builtInDualWideCamera` → `builtInWideAngleCamera`. 가상 기기는 첫 전환 배율(광각 「1x」)에 두고 전환 동작 `.auto` → 가까우면 iOS 가 초광각(매크로)으로 바꿈. 광각만 있는 기기는 최소 초점거리에 맞춰 조금 확대(최대 2.5) · 연속 AF · `.near`. 1080p 프레임마다(앞 것이 끝난 뒤 · 0.12초 이상 간격) **가이드 틀 아래 MRZ 자리만** `regionOfInterest` 로 Vision `.accurate` 인식 → '<' 든 긴 줄 둘 이상이면 Dart `checkMrz`(= `mrz.dart` `findMrz` · 검사 숫자 규칙 한 곳) → 맞으면 진동 + **그 프레임의 틀 영역만 JPEG**(품질 0.8 · 긴 변 2000 이하 · 메모리만)으로 자동 촬영 → 확인 화면. **8초씩 3번** 못 읽으면(또는 1번 실패 뒤 보이는 [손으로 입력]) → 「읽지 못했어요 (3 / 3)」 + [손으로 입력] · [다시 찍기]. 틀 = 화면 폭 80%(가로 iPad 는 높이 기준) · 바깥 어둡게 · 안내 「맞으면 자동으로 찍혀요」. 카메라 권한 꺼짐 = `no_camera` → 손 입력 길. 사진첩 · 파일 저장 0 · **법적 검토 주석 유지**(`grep "법적 검토 필요"` = 7곳). `takePassportPhoto` · `recognizeText` · 피커 · `PassportGuide` 는 지움 |
| 4 | — | 코디가 「KOS 그대로」로 바꿈 → `Phone.display` · 상세 표시 변경을 **되돌림**(`model/reservation.dart` · `reservation_detail_screen.dart` = base 와 같음). 앱은 `number` 그대로 |
| 시험 | `test/e2e_batch1_test.dart`(새) · `test/scan_test.dart` · `integration_test/app_shots_test.dart` | 아래 |

### 검증
- `flutter analyze` → **No issues found**
- `flutter test` → **106 passed**(이전 98 · 두 번 돌려 둘 다 통과). 새 `e2e_batch1_test` 7: installId 실음(등록 · 이름 고치기) · 못 얻으면 키 뺌 · **등록이 겹쳐도 deviceId = 마지막 토큰 행** · 첫 로그인 창 → 저장 = 이름 등록(installId 포함) · 다시 안 물음 · **SSE `display` → 다른 탭(설정)에 있어도 스캔 화면이 열림 · pending 이 500 이어도 · 같은 요청 두 번 안 엶 · 다른 기기 것 안 엶** · 링크: 로그인 전 = 기다렸다가 로그인 뒤 claim(deviceId 실음) · 켜진 상태 링크 claim · 다른 링크 무시. `scan_test` 고침: 연속 스캔 실패 → (3/3) [손으로 입력] → `manual=true` · 사진 없음 / MRZ 자동 촬영 → 바꾼 칸만 · 사진 있음 / `checkMrz` = 검사 숫자 틀리면 false / 인자 `{windows:3, windowSec:8}` · [닫기] = 스캔 닫기
- `flutter build ios --no-codesign` → Runner.app 빌드됨(25.2MB). Swift 경고 = `contentEdgeInsets` 지원 중단 1개뿐 · 장면 대리자 메서드 시그니처 불일치 경고 없음
- 시뮬레이터(iPhone 17 · scratch back 8791): `app-shots/B1-phone-01_device_name_sheet` · `02_device_name_typed` · `03_settings_after_name`. 카메라 · 딥링크 · 푸시는 시뮬레이터로 확인 불가 → 실기기

### 계약 대조
- §5-1.1 기기 등록 + installId(backend 확정 모양) = 같음 · §5-3 띄우기(SSE · pending · QR claim) = 같음 + 딥링크 길이 더해짐(웹 QR 을 기본 카메라로) · §6.14 기기 이름 = 같음 + 첫 로그인 창 · §6.16 ① 촬영 방식만 바뀜(한 장 → 연속 자동) · 3번 실패 → 손 입력 · 원본 메모리만 = 같음

### #3 원인 — 확인한 것 · 남은 것
- 앱 코드로 찾은 실제 결함: (a) **pending GET 하나에만 기대 열기** — 그 요청이 실패하면(타임아웃 · 404) 프레임을 받고도 아무것도 안 열림 → 고침 (b) **로그인 때 기기 등록 경쟁** — 늦게 온 옛 토큰 응답이 deviceId 를 옛 행으로 되돌림(그러면 이 기기 것이 아니라며 `display` 를 버림) → 고침. 운영 #10 에서 둘 중 무엇이었는지는 로그가 없어 단정 못 함
- **back 쪽 참고(코디 판단)**: hub 는 끊긴 연결을 다음 쓰기(ping 15초 · 프록시를 거치면 더 길 수 있음) 때에야 알아챔. 폰이 뒤로 가거나 잠기면 앱은 스트림을 닫지만, 그 사이 `online(deviceId)` 가 참으로 남아 `reach()` 가 SSE 를 고르고 **푸시를 건너뜀** → 폰은 아무것도 못 받음(앞으로 와야 pending 으로 열림). 「뒤 · 잠김」 확인에서 알림이 안 오면 이 길 — 예: SSE 로 보낸 뒤 N초 안에 opened 가 안 되면 푸시도 보내기

### 이슈 · 실기기에서 볼 것(코디 · 사용자)
1. **#6 여권 스캔**(지어낸 견본 · 실제 여권 · 사람 사진 쓰지 말 것): 가까이 댈 때 매크로 전환 · 초점 · 자동 촬영까지 걸리는 시간 · 8초 × 3 이 적당한지 · 찍힌 틀 영역 사진 품질(KOS 사진)
2. **#5 딥링크**: 웹 QR → iOS 기본 카메라 → 「Céramique 에서 열기」 → (켜진 상태 · **꺼진 상태(콜드 스타트)** · 로그아웃 상태) 각각 claim → 스캔 화면. 콜드 스타트 urlContexts 는 Flutter 장면 플러그인 대리자로 받는데, 늦게 등록된 대리자에 Flutter 가 그것을 넘겨 주는지는 실기기에서만 확인 가능 — 안 되면 알려 주세요(SceneDelegate 에서 받는 길로 바꿈)
3. **#3**: 앞(다른 탭) · 뒤 · 잠김 상태에서 웹 [스캔할 기기] → 열림. 뒤 · 잠김은 위 back 참고 사항 영향
4. **#1**: 새 빌드 설치 뒤 웹 기기 목록이 이 폰 한 줄인지(옛 행 8 은 24시간 뒤 빠짐 — backend 보고)
5. **#2**: 이미 로그인한 TestFlight 설치에도 다음 실행 때 이름 창이 한 번 뜸(의도 — 「iPhone」 두 줄을 이름으로 가르려고)
6. 새 Swift 파일 없음(pbxproj 수정 없음) · Info.plist 에 URL 스킴 · `FlutterDeepLinkingEnabled` 두 키 추가

---

## E2E batch 2 (2026-10-28 · branch `kknaksss/overall-board-4` · base `333f30f`) — mobile #3 · #4 done(실기기 확인 남음) · #2 변경 없음

공통: 범위 `procedure/app/**` 만 · 커밋 · push · 업로드 없음. 확인용 back = 레포 밖 복사본(scratchpad · `.env` 없음 → KOS 꺼짐 · `PROC_FAKE_BOARD=1` · 지어낸 계정 · 임시 포트 8791 · 끝나고 내리고 지움). 사용자 8700 · 프로세스는 건드리지 않음.

### 수행
| # | 파일 | 내용 |
|---|---|---|
| 3 이름 창 뺌 | `lib/screens/shell.dart` · `lib/app_state.dart` · `integration_test/app_shots_test.dart` · `test/e2e_batch1_test.dart` | batch 1 의 첫 로그인 「이 기기 이름」 창 · 상태(`askDeviceName` · `device.nameAsked`) · 시험을 모두 지움 |
| 3 기종 이름 자동 | `ios/Runner/AppDelegate.swift`(채널 `deviceModel` = `utsname.machine` · 시뮬레이터는 `SIMULATOR_MODEL_IDENTIFIER`) · `lib/push/push.dart`(`modelName()` 표 — iPhone X ~ 17 · Air · 16e · iPad 9th ~ A16 · mini 6 · A17 Pro · Air 4 ~ M3 · Pro 11/12.9/13 3rd ~ M4) · `lib/app_state.dart` | 기본 이름 = 기종 이름(예 `iPhone16,1` → 「iPhone 15 Pro」). 모르는 코드 = 「iPhone (iPhone19,1)」 꼴(코드를 남겨 구분). 시작 때 바로 정해 설정에 보임. **이미 이름을 정한 기기(설정 저장 · batch 1 창)는 그 이름 그대로** |
| 3 name 싣는 때(코디 전달) | `lib/app_state.dart` | `POST /api/devices` 의 `name` = **처음 등록 · 설정에서 저장할 때만**(`device.nameSent` 기록). 그 밖 등록(토큰 바뀜 · 앱 시작)은 `name` 키를 뺌 → back 의 이름을 덮지 않음. batch 1 빌드에서 넘어온 기기는 기록이 없어 **처음 한 번** 기종 이름을 실음(운영의 「iPhone」 이름이 기종 이름으로 바뀜) |
| 4 MRZ 보정 | `lib/scan/mrz.dart` | ① 채움 문자: `« ‹ く 〈 ＜ ≤` → `<` · **`K` 는 왼쪽이 `<` 이고 오른쪽이 `<`/`K`/줄 끝일 때만 `<`**(이름 속 K — `PARK<<` · `<KIM` — 는 그대로) · 공백은 「지움」 · 「`<` 로」 두 후보 ② 칸 종류별: 날짜 · 검사 숫자 칸 `O Q D U→0 · I L T→1 · Z→2 · S→5 · B→8 · G→6 · A→4` · 국적 · 이름 칸 숫자 → 글자(`0→O` 등) · 여권번호(글자 · 숫자 섞임)는 그대로 안 맞으면 헷갈리는 자리(0/O · 1/I · 5/S · 8/B · 2/Z · 6/G · 최대 6자리)를 **적게 바꾼 것부터** 바꿔 검사 숫자가 맞는 쪽 ③ 통과 = **여권번호 · 생년월일 · 만료일 검사 숫자 셋**(종합 검사 숫자 실패는 허용) ④ 길이: 첫 줄 끝 채움이 덜 · 더 읽힘(짧은 이름 · `P..<<` 꼴이면 8자부터) · 둘째 줄 끝(옵션 칸)이 덜 읽힘(30 ~ 43자 → `<` 채움) · 한 자 더 ⑤ `MrzConfirm` — **같은 판독(여권번호 · 생년월일 · 만료일 · 이름 · 국적 · 성별)이 연속 두 번이면 확정** · 다른 판독 · 못 읽음 · 빈 프레임이 끼면 처음부터 |
| 4 판정 · [촬영] | `lib/scan/scan_channel.dart` · `lib/screens/scan_screen.dart` | `checkMrz` 답 = `none` · `lines`(두 줄 읽음 · 검사 숫자 안 맞음) · `pending`(확인 중) · `confirmed` → 자동 촬영. 인자에 `debug: kDebugMode`. **[촬영] 사진(shutter)에서도 못 읽으면 바로 손 입력**(사진 버림 — r1 그대로) · 읽히면 확인 화면 |
| 4 네이티브 | `ios/Runner/TextScanner.swift` | ① **[촬영] 버튼 늘 보임**(흰 원 72pt · 「촬영」) — 지금 프레임의 틀 영역 사진 + 그 사진 전체 글자(Vision accurate) → `{photo, lines, shutter: true}` ② 상태 글자 = 「판독 줄 찾는 중」 · 「두 줄 읽음 — 맞추는 중」 · 「확인 중 — 그대로 들고 있어 주세요」 · 「확인됨」 · 「사진에서 읽는 중」(+ 실패 창 지나면 「못 읽음 n / 3」) ③ **틀 ↔ 영상 좌표 = `preview.metadataOutputRectConverted(fromLayerRect:)`**(aspect fill · 회전 · 크기를 레이어가 계산한 센서 좌표) → 버퍼에서 그 영역을 잘라(CI 원점 아래 → y 뒤집음) 화면 방향(세로 `.right`)으로 세운 그림을 Vision 에 넘김 — batch 1 의 손 계산 · `regionOfInterest`(방향 뒤 좌표인지 애매)를 버림. 세션이 돌기 시작한 뒤 다시 계산 ④ MRZ 자리 = 틀 아래 30%(+14pt 여유) · 틀 = 화면 폭 80%(높이 50% 이내) ⑤ **debug 빌드만 인식 글자 오버레이**(노란 고정폭 · 화면에만 · 저장 · 로그 없음) — Swift `DEBUG` 플래그는 Runner 에 없어 Dart `kDebugMode` 를 인자로 받음 · TestFlight(release) 에는 안 보임 ⑥ 빈 프레임도 판정에 넘겨 「연속」이 끊김을 앎 · 사진 · 프레임 메모리만 · 법적 검토 주석 유지(7곳) |
| 2 | — | 변경 없음(빌드 6 의 `ccc` 스킴). **딥링크 처리 시험 있음**: `test/e2e_batch1_test.dart` 「#5 ccc 링크 — 로그인 돼 있으면 claim · 아니면 로그인 뒤 claim · 다른 링크는 무시」(꺼진 상태 `takeLink` · 켜진 상태 `onLink` · deviceId 실음) — 그대로 통과 |

### 검증
- `flutter analyze` → **No issues found**
- `flutter test` → **118 passed**(batch 1 끝 106 · 이름 창 시험 −1 · 두 번 돌려 둘 다 통과). 새 · 고친 시험: `mrz_test` +6(오인식 섞은 지어낸 견본 — K · « 채움 · 이름 속 K 그대로 · 공백 · 숫자 칸 O/I/S/B · 국적 0→O · 이름 칸 1→I · 여권번호 0↔O · 줄 끝 덜 · 더 · **종합 검사 숫자만 틀림 = 통과 · 생년월일 검사 숫자 틀림 = 실패** · 연속 두 번 확정 · 끊기면 처음부터) / 새 `e2e_batch2_test` 8(기종 표 · 기본 이름 = 기종 · **name 은 처음 등록만 · 설정 저장은 실음** · 정한 이름 유지 · 옛 빌드 기기 첫 한 번 · [촬영] 못 읽음 → 손 입력 · [촬영] 읽힘 → 확인 · `checkMrz` none → pending → confirmed) / `scan_test` 인자에 `debug` · `e2e_batch1_test` name 기대 고침
- `flutter build ios --no-codesign` → Runner.app 빌드됨(25.3MB) · Runner Swift 경고 0
- 시뮬레이터(iPhone 17 · scratch back): `app-shots/B2-phone-01_after_login_no_name_sheet`(로그인 뒤 창 없음) · `B2-phone-02_settings_model_name`(설정 「기기 이름 = iPhone 17」 — 시뮬레이터 모델 코드 iPhone18,3 → 표). 카메라 · MRZ 는 실기기

### 계약 대조
- §6.14 이름 고치기 = 같음 · 기본 이름 = 기종(UIDevice.name 대신) · §5-1.1 등록 = name 은 처음 · 저장 때만(backend 전달) · §6.16 ① 자동 촬영 기준(연속 두 번 · 종합 검사 숫자 허용) + [촬영] · ②~⑤ 같음

### 이슈 · 실기기에서 볼 것(코디 · 사용자 · 실제 여권 · 사람 사진은 시험 자료로 쓰지 않음)
1. **#4 자동 촬영**: debug 빌드(Xcode 실행)로 오버레이를 켜고 MRZ 두 줄이 어떻게 읽히는지 · 상태 글자가 「두 줄 읽음」에서 멈추면 오버레이 글자를 알려 주세요(보정 표에 더함). TestFlight(release)엔 오버레이 없음
2. **#4 [촬영]**: 흔들림 없이 찍었을 때 사진에서 읽히는지 · 못 읽으면 바로 손 입력으로 가는지
3. **#3**: 새 빌드 첫 실행 뒤 웹 [스캔할 기기] 이름이 「iPhone 15 Pro」 꼴로 바뀌는지(기록 없는 기기 첫 한 번) · 설정에서 바꾼 이름이 다음 실행 · 토큰 바뀜에도 유지되는지. 같은 기종 두 대 구분(「계정 이름」 등)은 지시서에 없어 넣지 않음 — 필요하면 알려 주세요
4. 기종 표에 없는 새 모델은 「iPhone (모델 코드)」로 보임

---

## WORK-010 WP-APP (2026-10-28 · branch `kknaksss/overall-board-6` · base `fad8b56`) — done(가짜 응답) · 데모 back 붙여 보기는 WP-BE 뒤

계약 SPEC-006 0.1.0 §6.6 · §8.2 · §10.2 · SPEC-004 0.4.2. 범위 `procedure/app/**` 만 · 커밋 · push 없음. **back 에 `qrUrl` 이 아직 없어**(작업 시점 `grep qrUrl procedure/back` = 0) 지시대로 화면부터 — 응답 모양은 SPEC-006 §6.6 그대로(가짜 응답 · 시험).

### 수행
| 파일 | 내용 |
|---|---|
| `lib/screens/qr_show_screen.dart`(새) | 문진 QR 화면 — 흰 바탕 전체 화면 · 가운데 QR(짧은 변 60%) · 「휴대폰 카메라로 QR 을 찍어 주세요」 + 「Scan with your phone camera」 · 남은 시간 mm:ss(`expiresAt` · 서버 시각 보정 skew) · 0 이면 「시간이 지났어요」 · 오른쪽 위 [닫기] = **화면만**(요청 그대로 · close 안 부름) · 고객 이름 · 예약 정보 없음 · 떠 있는 동안 화면 꺼짐 막기 · **5초마다 `GET /api/reservations/{id}` `displays[]`** 에서 그 요청이 `pending` 이 아니면 한 줄(「고객 폰에서 열렸어요」 · 「제출됐어요」 · 「시간이 지났어요」 · 「닫혔어요」) → 1.5초 뒤 저절로 닫힘 · 읽기 실패 · 목록에 없음 = 다음 폴링. `qrUrl` 은 로그 · 저장 · 토스트에 쓰지 않음 |
| `ios/Runner/TextScanner.swift` · `lib/scan/scan_channel.dart` | 채널 `procedure/scan` 에 `qrImage({text, size})`(CoreImage `CIQRCodeGenerator` · 오류 정정 M · 정수 배 확대 PNG · 기기 안) · `keepAwake(bool)`(`isIdleTimerDisabled`) — **새 패키지 없음**(qr_flutter · wakelock 안 넣음 · pubspec 그대로) |
| `lib/model/display.dart` | `DisplayReq.qrUrl`(pending 응답 · SSE 프레임 · 빈 문자열 = null) · `isCustomerQr()`(https/http) |
| `lib/model/reservation.dart` | 상세 `displays[]` 에 `qrUrl` · `openedAt` |
| `lib/app_state.dart` | 차례 넣기: **문진 = `status == pending` 만**(opened · done 은 안 엶) · 스캔 = 지금 그대로(pending · opened) · 같은 requestId 한 번 · 다른 화면이 떠 있으면 기다림(OQ-621 그대로). **[QR 읽기] = `ccc://` 만** — https 를 찍으면 claim 안 부르고 「고객 폰으로 찍는 QR 이에요」 · `markDisplayOpened`(문진 대기 화면용) 지움 |
| `lib/screens/launchers.dart` | 띄우기(문진) → `qrUrl` 로 QR 화면(없으면 「문진 QR 을 받지 못했어요」) · **[이 기기에 QR 보이기]** = `POST /api/display-requests {reservationId, kind:"questionnaire"}`(**deviceId 없이**) → 응답 `{id, qrUrl, expiresAt}` → QR 화면 · 시험 · 스크린샷용 `openQrScreen` 자리 |
| `lib/screens/reservation_detail_screen.dart` | [이 기기에서 열기] → **[이 기기에 QR 보이기]** · [태블릿에 띄우기] 그대로 · 단계 글 = pending 「{기기} QR 표시 중」 · opened 「고객이 입력 중 · HH:MM」(`openedAt`) |
| `lib/api/api.dart` | 문진 GET · 제출 · `unlock` 호출 지움(문진 API 0) |
| `lib/widgets/ui.dart` | 문진 잠금용 `Toaster.muted` 지움 |
| **지움** | `lib/screens/questionnaire_screen.dart` · `lib/l10n/questionnaire_text.dart` · `lib/model/questionnaire.dart` · `test/questionnaire_test.dart` · 잠금 · [직원] · unlock · `integration_test` APP5 순회 |
| 시험 | `test/qr_show_test.dart`(새 · 7) · `test/display_test.dart`(문진 = pending 만 · qrUrl 받기 · [QR 읽기] https 거절) · `integration_test/qr_shots_test.dart`(새 · back 없이 가짜 응답 · 지어낸 링크) |

### 검증
- `flutter analyze` → **No issues found**
- `flutter test` → **122 passed**(두 번). QR 화면: `qrUrl` 로 그림(`qrImage` 인자) · 안내 두 줄 · 남은 시간 · 고객 이름 없음 · `keepAwake(true)` / 폴링 pending → 그대로 · opened → 「고객 폰에서 열렸어요」 → 1.5초 뒤 닫힘 · 쓰기 요청 0 · `keepAwake(false)` / [닫기] = 화면만(POST 0) / 띄우기(문진) = QR 화면 · qrUrl 없으면 토스트 / [이 기기에 QR 보이기] 본문 = `{reservationId, kind}`(deviceId 있어도 안 실음) → 응답 qrUrl
- `flutter build ios --no-codesign` → Runner.app 빌드됨 · Swift 경고 0
- 시뮬레이터: `app-shots/W10-phone-01_qr_screen` · `W10-phone-02_qr_opened_closing` · `W10-tablet-01..02`(iPad Pro 11 M5). QR 은 **지어낸 `https://example.invalid/q#…` 주소**(토큰 아님 · 쓸 수 없는 주소)라 가릴 것 없음 — 실제 데모 back 링크로 찍을 때는 SPEC-006 §7.5 대로 가림

### 계약 대조(SPEC-006 §8.2)
- 받기(SSE · 푸시 → pending · 앞으로 올 때) = 같음 · QR 화면 = 같음 · 닫힘(5초 상세 폴링 · 1.5초) = 같음 · [닫기] = 화면만 = 같음 · 문진 pending 만 = 같음 · [이 기기에 QR 보이기] = 같음 · [QR 읽기] https 거절 = 같음 · 지움 = 같음. 띄우기 푸시 payload 는 그대로(`{kind:"display", requestId}` → 누르면 pending 에서 qrUrl)

### 남은 것 · 코디가 볼 것
1. **WP-BE 뒤**: 데모 back 으로 시뮬레이터 [태블릿에 띄우기] → QR 화면 · 데스크 브라우저에서 그 주소 열면 화면이 닫히는지(지시서 WP-APP 확인 줄) — back 에 `qrUrl` · `displays[].qrUrl/openedAt` 가 생기면 바로 한 번 돌림. 응답 키가 §6.6 과 다르면 알려 주세요
2. 띄우기 푸시를 눌러 연 경우 `pending` 항목에 `qrUrl` 이 있어야 열린다(§6.6 「pending 일 때만」) — 이미 opened 면 열지 않음(의도)
3. 옛 TestFlight 빌드의 문진 화면은 배포 뒤 404(SPEC-006 OQ-812) — 새 빌드 같이 올리기

### WP-APP 실제 back 확인 (WP-BE 뒤 · 2026-10-28)
- **실제 back 으로 한 번 됨** — `procedure/back` 레포 밖 복사본 · 임시 포트 8791 · `.env` 없음(KOS 꺼짐) · 가짜 판 · 지어낸 계정. 복사본에만: 가짜 판 상세에 실제 `displays[]` 붙임 · KOS 양식 읽기 1줄 가짜 · 지어낸 예약 · 고객 행(끝나고 내리고 지움 · 레포 코드 그대로). 응답 모양 = WP-BE 보고 · SPEC-006 §6.6 과 같음(만들기 `qrToken: null` · `qrUrl` 43자 토큰 · pending · SSE · `displays[].qrUrl`(pending 만) · `openedAt`)
- 흐름(`integration_test/qweb_e2e_test.dart` · 시뮬레이터 iPhone 17 · 통과): 앱 로그인 → 기기 등록(지어낸 토큰을 앱의 `onToken` 길로) → 데스크 로그인이 이 기기로 문진 띄우기(= [태블릿에 띄우기]) → **SSE → QR 화면(남은 시간 있음)** → 데스크 쪽에서 그 링크 공개 `GET` 200 → **5초 폴링 opened → 「고객 폰에서 열렸어요」 → 저절로 닫힘** · 상세 `opened` / 예약 상세 **[이 기기에 QR 보이기] → QR 화면 → [닫기] = 화면만**(요청 `pending` 그대로 · `deviceName` 없음)
- **고친 것 1**: SSE `display` 프레임엔 `expiresAt` 이 없어 SSE 로 연 QR 화면에 남은 시간이 비었음 → SSE 를 받으면 **`pending` 응답(만료 · qrUrl 다 있음)으로 열고**, pending 읽기가 실패할 때만 프레임으로(batch 1 #3 그대로) · `refreshDisplays()` 가 성공 여부를 돌려줌 · 시험 +1
- 검증 `flutter analyze` 0 · `flutter test` **123 passed** · 스크린샷 `app-shots/W10E-phone-01..04`(**QR 은 저장 뒤 회색으로 가림** · 파일 이름에 토큰 없음)

---

## 띄우기 실기기 안 열림 (2026-10-28 · branch `kknaksss/overall-board-7` · base `00853e1` · TestFlight 빌드 8)

범위 `procedure/app/**` 만 · 커밋 없음. 확인 back = 레포 밖 복사본 · 임시 포트 8791 · KOS 꺼짐 · 가짜 판 · 지어낸 계정 · 지어낸 예약 행(끝나고 내리고 지움).

### 원인 (코드로 찾은 것 · 코디 단서 「다시 로그인하니까 된다」와 맞춤)
1. **저장된 로그인으로 시작(업데이트 · 콜드 스타트) — SSE 가 확인 안 된 deviceId 로 붙고 다시 안 붙음.** 시작 때 `_enter()` 가 SSE 를 **저장된 deviceId 로 먼저** 연다(등록 전). 그 순간 back 이 그 id 를 이 계정 기기로 못 알아보면(`devices.own` = None — 옛 행 · 다른 계정 소유 · 등록 전) 연결은 **기기 없이** 붙고(`online(9)` = 거짓 · `display` 프레임 안 옴 · `last_seen` 안 바뀜) 앱엔 아무 신호가 없다. 뒤이은 등록(installId → 행 9)이 **같은 id 를 돌려주면 「바뀜 없음」이라 SSE 를 다시 안 열었다** → 그 세션 내내 display 를 못 받음. 다시 로그인 = `deviceId` 를 지우고 등록 → id 가 「바뀜」 → SSE 다시 → 됨(사용자 관찰 그대로). 앞으로 올 때는 다시 등록조차 안 했다
2. **앞에서 받은 띄우기 푸시가 배너만** — `willPresent` 가 배너 · 소리만 띄우고 Dart 로 안 넘겼다. SSE 가 안 붙은 상태(1)에선 푸시가 와도 **눌러야만** 열렸다(눌러야 pending 을 읽음 · 운영 `last_seen` 이 안 바뀐 것 = pending 도 안 불림 = 안 눌림과 맞음)
3. 뒤 · 잠김: iOS 는 앱을 저절로 앞으로 못 올린다 — 알림을 누르거나 앱을 열면 `resumed` → pending 으로 연다(지금도 됨 · 이번에 등록 · SSE 다시 붙임도 더함). 콜드 스타트 알림 누름 = `ready()` 의 pendingTap → 로그인 뒤 pending(지금도 됨)
4. 세 길(SSE · 푸시 · pending) 모두 같은 함수(`enqueueDisplays` → Shell `_next` → `openDisplay` → 문진 = QR 화면)로 간다 — 그 쪽 결함 없음

### 고침
| 파일 | 내용 |
|---|---|
| `lib/app_state.dart` | **시작(저장된 로그인 · 로그인) · 앞으로 올 때 = 기기 다시 등록 → 등록 응답 id 로 SSE 를 한 번 다시 연다(id 가 같아도 · `reconnect`)** — `_refreshPush({reconnect})` · `_registerDevice(token, reconnect:)` · 로그인 상태일 때만 다시 엶 · 앞으로 올 때 `_refreshPush(reconnect: true)` 더함(판은 바로 열고, 등록 뒤 확인된 id 로 다시) |
| `ios/Runner/AppDelegate.swift` | `willPresent`: `kind = "display"` 면 **배너 대신 바로 Dart(`onForeground` {kind, requestId})** → 누른 것과 같은 길(pending 읽어 엶) · 그 밖 푸시는 지금 그대로(배너 + 소리) |
| `lib/push/push.dart` | `onForeground` 받기 → `onTap` 과 같은 처리 |
| 시험 | `test/boot_device_test.dart`(새 2 — 저장된 옛 id 8 → 시작 등록 9 → SSE · pending 이 9 / **등록 응답이 같은 9 여도 SSE 순서 `sse:9 → register → sse:9`** · 앞으로 올 때 다시 등록 → 마지막 SSE 가 등록 뒤) · `integration_test/display_push_e2e_test.dart`(새 · 실제 back) |

### 검증
- `flutter analyze` 0 · `flutter test` **125 passed**(두 번) · `flutter build ios --no-codesign` 됨(Swift 경고 0)
- **시뮬레이터 · 실제 back(임시) 세 경우 통과** — `xcrun simctl push` 는 시뮬레이터 알림 허용을 명령으로 줄 수 없어(simctl privacy 에 알림 없음) 대신: 기기 등록 = 앱 토큰 길(`onToken`)에 지어낸 토큰 · 앞 푸시 = 네이티브 `willPresent` 가 보내는 채널 메시지 그대로 · 뒤 · 콜드 = 실제 앱 생명주기(`simctl launch` 다른 앱 → 이 앱)
  - ① **앞 · SSE 끊김 → 데스크 띄우기(back = 푸시만) → 앞 푸시로 QR 화면 열림** `app-shots/BUG-phone-01_fg_push_opened`
  - ② **뒤(다른 앱) → 데스크 띄우기(curl) → 이 앱을 앞으로 → QR 화면 열림** `BUG-phone-02_bg_resume_opened`
  - ③ **콜드 스타트 + 버그 상태 재현**(시작 전 기기 행을 다른 계정으로 돌려 둠 = 시작 SSE 가 기기 없이 붙음) → 시작 등록이 행을 되찾고 SSE 다시 → **데스크 띄우기가 SSE 로 와서 QR 화면** · 기기 행 계정 복구 확인 `BUG-phone-03_cold_start_sse_opened`(화면 넘어가는 프레임 · QR 안 그려짐 → 토큰 없음)
  - 덤으로 확인: 알림 상태가 「허용」이 아니면 앱은 시작 때 등록을 안 한다(r2 설계 — 알림 거부 기기 = 띄우기 대상 아님) → 그 경우 SSE 는 기기 없이 붙는다

### 코디 · backend 가 볼 것
1. 운영에서 정확히 어느 순간 back 이 저장된 id 를 못 알아봤는지는 로그가 없어 단정 못 함(코드 · 재현으로 같은 증상 확인). **back 제안**: `reach()` 결과(`sse+push` / `push`)와 SSE 연결이 `deviceId` 를 받았는데 `own()` = None 이었을 때를 로그 한 줄로 — 다음엔 바로 보인다. `last_seen` 은 SSE 연결 · pending · 등록 때만 바뀜(프레임마다 아님)
2. 실기기(TestFlight 다음 빌드): 업데이트 뒤 다시 로그인 **없이** 앞 · 다른 탭 · 뒤(알림 누름 / 앱 열기) · 잠김 · 콜드 스타트에서 웹 [폰 · 태블릿에 띄우기] → QR 화면
3. 앱이 앞일 때 띄우기 푸시는 배너가 안 뜬다(바로 화면이 열리므로) — 원장 · 상담사 호출 푸시는 그대로 배너

---

## 헤더 · QR 읽기 (2026-10-28 · branch `kknaksss/overall-board-8` · app 만)

### 1. 헤더 한 줄 `[메뉴명] [Céramique] [알림]`
| 파일 | 내용 |
|---|---|
| `lib/widgets/header.dart` | `AppHeader(title)` = 한 줄 56 — 왼쪽 지금 탭 이름 · 가운데 Céramique(좌우 여백 같게 → 본문 가운데) · 오른쪽 종 + 안 읽은 수. **폰 · 태블릿 같음**(태블릿도 레일 오른쪽 본문 위에 이 한 줄). 탭 머리 큰 제목 줄(`TabHead`) · 「시술실 현황」 머리(`ListHeader`) 지움 → 시술 현황 「확인 N」(태블릿 「확인 필요 N」) · 시계는 **본문 첫 줄 `BoardBar`(40)** 로 |
| `lib/screens/shell.dart` | `TabScaffold(tab:, body:)` = 헤더 한 줄 + 연결 줄 + 본문(탭 이름은 `tabName` 그대로: 예약 현황 · 내원 현황 · 시술 현황 · 설정) |
| `lib/screens/{reservations,visits,board,settings}_screen.dart` | 새 `TabScaffold` · 예약 현황 날짜 이동 줄 · 범례 · 필터는 원래 본문 첫 줄이라 그대로 |

### 2. 예약 현황 [QR 읽기] 뺌 — 지운 것 · 남긴 것
- **지움**: 예약 현황 머리 [QR 읽기] 버튼 · `_readQr` · `ScanChannel.scanQr` · 네이티브 `scanQr` 와 QR 카메라 화면 `QrViewController`(`TextScanner.swift`) · 문진 https QR 을 거절하던 토스트 · `isCustomerQr()` · 그 시험 · 카메라 권한 문구에서 「QR 을 읽고」(이제 여권 사진면만)
- **남김(쓰는 곳 있음)**: `ccc://` 딥링크(`CFBundleURLTypes` · `LinkHandler` · `openLink`) · `claimQr` · `api.claimDisplay` — 웹이 아직 **스캔 종류에 `ccc://display?t=` QR 을 그린다**(`front/components/reservations/Display.tsx` `displayQrText` · [스캔할 기기]를 고르지 않으면 QR 단계). 그 QR 을 iOS 기본 카메라로 찍으면 앱이 열려 claim 한다(batch 1 #5). 웹에서 스캔 QR 단계를 없애면 이 길도 지울 수 있음 — 코디 판단
- 앱이 QR 을 읽는 곳 = 0(여권 MRZ 인식은 그대로)

### 검증
- `flutter analyze` 0 · `flutter test` **127 passed**(새 `header_test` 2 — 폰 · 태블릿: 탭 이름 · Céramique · 종이 같은 줄 · 높이 56 · Céramique 가운데 · 안 읽은 수 / `display_test` claim 시험 = 딥링크 길로 고침) · `flutter build ios --no-codesign` 됨(Swift 경고 0)
- 시뮬레이터(임시 back 8791 · 가짜 판 · 지어낸 계정 · 끝나고 내림): `app-shots/H-phone-01..04` · `H-tablet-01..04`(예약 현황 · 내원 현황 · 시술 현황 · 설정)

### 코디가 볼 것
- 태블릿은 레일 위 「Céramique」 글자와 헤더 가운데 「Céramique」가 둘 보인다 — 레일 글자를 뺄지 알려 주세요(지시대로 헤더는 폰 · 태블릿 같게 둠)

---

## 헤더 2 · 예약 상세 자동 저장 · 칩 · 입력 칸 (2026-10-28 · branch `kknaksss/overall-board-9` · base `4d48421` · app 만)

한 판에 받은 지시 전부(코디 · 사용자). 커밋 없음.

| # | 지시 | 고친 것 |
|---|---|---|
| 1 | 헤더 자리 바꿈 | `AppHeader` = **[Céramique 왼쪽][메뉴명 가운데][알림 오른쪽]** · 메뉴명이 본문 정가운데(좌우 여백 같게) · 폰 · 태블릿 |
| 2 | 헤더 높이 · 아래 여백 | 모든 머리 `headerHeight` = **56 → 48**(공통 헤더 · 상세 머리 · 알림) |
| 3 | 상세 헤더(확정안) | 새 `DetailHeader` — 흰 바탕 · **[‹ 들어온 탭 이름]**(예약 현황 / 내원 현황 · 룸 = 시술 현황) · **제목 = 화면 이름 정가운데**(예약 상세 · 룸 상세 · 알림 — 왼쪽 버튼 폭과 상관없이 Stack 가운데) · 시각 · 상태 제목 없음. 상태 색 머리(`headOf` · 보라 등) 지움 → 상태는 본문 `StateChip`(2계층)만 · iOS 상태 바 어두운 글자. 뒤로 버튼 = 공통 `HeaderBack`(‹ + 16pt 500 · 모든 화면 같은 크기). 룸 상세: 옛 「← 현황」 버튼 없앰 · 「다른 룸 확인 N」은 룸 정보 줄로. 중간 지시(상태 제목 · 처음부터 상태)는 확정안으로 바뀌어 넣었다 뺌 |
| 4 | 예약 현황 날짜 줄(최종) | 1줄 **[‹ 날짜 ›] [오늘] [총 예약 N건]** 붙여서 · 2줄 **상태 칩 7개 한 줄**(넘치면 가로 스크롤). 원인: 날짜가 `Flexible`(남는 자리의 반)이라 「(요일)」이 숨은 줄로 넘어가며 날짜와 › 사이가 벌어졌음 → 글자 폭 그대로 |
| 5 | 공통 칩 | 새 `StatusChip` · `ChipRow`(`widgets/resv_ui.dart`) — 기준 = 예약 현황 범례 칩(알약 · caption 600 · 웹 2계층 색 · 「이름 개수」). 필터 = 안 고름 흰 바탕 · gray-300 테두리(점 = 상태 색) / 고름 primary-100 · primary. 한 줄 · 넘치면 가로 스크롤 · 왼쪽부터. **바뀐 곳(전수 grep `Chip|Pill|Filter|circular(999)`)**: ① 예약 현황 범례 `ResvLegend` ② 예약 현황 그룹 필터 `_chips`(옛 32px 큰 알약) ③ 내원 현황 필터 `_FilterCell` 격자 → 지움 ④ 시술 현황 필터 `FilterChipButton`(옛 각진 8px) → 지움. **그대로 둔 것(필터 · 범례 아님)**: 카드 · 상세 안 상태 배지 `StateChip` · `MsBadge`(룸 · 시술 줄) · `MiniChip`(초진 · 재진 · 신분 칸) · 종 배지 · 통역 문구 칩(`PhraseChips` · 누르면 말하는 버튼) |
| 6 | 시술 현황 시계 | 탭 첫 줄에서 시계 뺌 · 「확인 N」만(없으면 줄 없음). 룸 상세 시계는 그대로 |
| 7 | 입력 칸 테두리 | 앱 테마 `inputDecorationTheme` 한 곳 — 흰 바탕 · gray-300 테두리 · 둥근 8 · gray-400 placeholder · 포커스 때만 primary · 못 고침 = gray-200 테두리 · 오류 red. 모든 TextField(로그인은 원래 같은 값). 웹 textarea 는 둥근 6 — 코디 지시대로 8 |
| 8 | 예약 상세 자동 저장(웹 batch 3 와 같게) | 새 `AutoSaveField`(`widgets/autosave.dart`) — **입력 멈춤 1초 · 칸 벗어날 때 · 화면 나갈 때(남은 것)** 저장 · 칸 옆 「저장 중… / 저장됨 / 저장 못 함 · 다시」 · 실패 = 글자 그대로 · 같은 값이면 안 부름 · 고치는 중이 아니면 5초 폴링 새 값으로. **예약 메모 · 주의사항 [저장] 없앰 · 고객 기본 정보 [수정] · 편집 시트 없앰 → 늘 편집 · 칸마다 저장**(이름 · 한글 발음 · 생년월일 · 휴대폰 · 이메일 · 여권 영문 성 · 이름 · 여권번호 · 만료일 — `PUT …/personal` 에 그 칸 하나만 · 성별 · 국적 · SNS 는 원래도 고칠 칸 없음 = 보기). **유입 채널** = 드롭다운(`funnelCodes` · 지금 값 `customer.funnel`) · 고르면 바로 `PUT /api/customers/{id}/funnel {funnelId}`(비움 = null) · 머리의 옛 「유입 채널 · 예약 유입」 줄 지움. **여권 사진 [사진 삭제]**(사진 있을 때) → 확인 창 → `DELETE /api/id-photos/{id}` → 「KOS 사진도 지움 / KOS 에는 없었어요」 · 실패 = 메시지(다시 누르면 됨) |

### 검증
- `flutter analyze` 0 · `flutter test` **138 passed**(새 `autosave_test` 9 — 1초 · 칸 벗어남 · 같은 값 0 · 실패 글자 유지 + 다시 · 화면 나감 저장 · 폴링 새 값 / 예약 상세 [저장] · [수정] 없음 · 메모 · 고객 칸 하나만 · 유입 채널 PUT · 사진 삭제 DELETE · 사진 없으면 버튼 없음 · `chip_test` 1 · `header_test` 3) · `flutter build ios --no-codesign` 됨
- 고치는 길에 찾은 결함 1: 자동 저장 칸 「마지막 저장 값」이 늦게 초기화돼 첫 폴링 새 값이 막혔음 → initState 에서(시험으로 잡음)
- 시뮬레이터(임시 back · 가짜 판 · 끝나고 내림): `app-shots/H2-phone-01..07` · `H2-tablet-01..07`(예약 현황 · 예약 상세 · 상세 입력 칸(자동 저장 · 테두리 · 유입 채널) · 내원 현황 · 시술 현황 · 룸 상세 · 설정)

### 실기기에서 볼 것
- 자동 저장 실제 KOS 반영(같은 값 0 · 칸 하나씩) · 유입 채널 · 사진 삭제(KOS 이미지) — 데모 back 에서 · 키보드가 올라온 채 다른 칸 누름 · 화면 나감

### 시뮬레이터 피드백 batch 4 (2026-10-28 · `kknaksss/overall-board-9` · app 만 · 시뮬레이터 · 앱 · integration test 안 돌림)
- **#1** 예약 현황 날짜 줄 `[‹ 날짜 ›] [오늘] ……… [총 예약 N건]`(오른쪽 끝 · Spacer) — `reservations_screen.dart`
- **#2** 칩 줄 위 · 아래 여백을 `ChipRow` 가 정함(`chipRowVertical` 2 + 필터 칩 누르는 자리 6 = 예약 현황 그룹 필터 줄 기준) · 화면은 좌우(`left` · `right`)만 — 걷어 낸 화면별 여백: 시술 현황 칩 줄 위 4 · 카드 목록 위 10(폰) · 12(태블릿 격자) / 내원 현황 목록 위 12 · 칩 아래 8 · 첫 「N층 N명」 머리 위 4 / 예약 현황 그룹 필터 아래 2
- 검증 `flutter analyze` 0 · `flutter test` **139 passed**(chip_test + 여백 1). 스크린샷 없음(지시대로)
