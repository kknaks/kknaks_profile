# day-app mobile — 사용자 UI 교정 + 로컬 API 소비 구현 결과 (task_5d4fa3a01700 · ctx_0a53366d9755)

## 상태: done — 앱 구현 · 더블 테스트 · 시각 증거 완료. authenticated 통합(로그인 뒤 실데이터)은 미실행(사용자 몫)

- 기준: SPEC-003 exact `cdde456af1e38a988470b5144278cbb04360341f`(로컬 API 정합 리뷰 PASS판). 소비 원천 = 옆 SPEC-002 `e421b77b` · backend `day-procedure-board-2` `a1c90b9d`(read-only 대조).
- 코드 트리 `CENTURION_DAY/day-app` · `kknaksss/day-app` · 시작 HEAD `0b776e90`. **변경은 `app/**` 만 · 미커밋**(커밋 · push · PR · merge 0). 백엔드 · 웹 · 스펙 · 배포 · 실 env · 서버 · DB · 포트 변경 0. 하위 워커 · 위임 0.
- 시각 원천: profile `ui-reference/*.png` 13장 + cc-prototype `procedure/app/lib` (board_screen · room_screen · widgets/ui · call_sheet · interpret_bar · interpret_drawer · header · screens/shell · theme/tokens) 직접 읽음. 프로토 모양(둥근 14 카드 · 지금 상자 · Boxed · 시술 카드형 · 큰 경과 · 알약 칩 · 원형 마이크 · 셸 탭바/레일 92)에 **DAY 색 · 브랜드 · 서버 값**만 바꿈.

## 변경 파일 (app/ 아래)

| 파일 | 변경 |
|---|---|
| `lib/model/board.dart` | `needs[]`(Need: why · since · limitMin · callId · doctorName) · `anesthesia.lastSeconds` · `tasks[].canRecall` · `limits`(anesMin · callMin) 파싱 · 옛 `need`/`lastMinutes` 안 읽음 · `isDoctor(staffId)` · `needsCheck` · `allDone`(표시) |
| `lib/state/board_controller.dart` | `run` 반환 = **2xx 일 때만 true**(이전: 요청 보냄) · 성공 토스트 `ok` 글자 · `alive` 판단 · 닫힌 판/떠난 화면 응답 토스트 없음 · 401 은 그 판 세션에만 |
| `lib/core/copy.dart` | `call_already_accepted` 글자 · `OkToast`(U-13 표 원문) · 취소 확인 창 원문 · 메뉴 이름 · 「곧 출시 예정」 · 브랜드 |
| `lib/ui/shell.dart`(신규) | 셸 4메뉴(폰 탭바 · 아이패드 레일) · 탭마다 Navigator · 같은 탭 다시 = 맨 위 · 설정 탭(이름 · 병원 · 로그아웃) · `ScreenPresence`/`PresenceAware`(탭 보임 + PageRoute 덮임) |
| `lib/ui/accept.dart`(신규) | 직무별 수락 — 원장(`doctors[]` 에 staff.id) 즉시 본인 · 그 밖 「원장 골라 수락」 드로어 대리 · 글자 「수락 · N건」/「원장 골라 수락 · N건」 |
| `lib/ui/board_screen.dart` | 공통 머리 · 인박스 탭 · 알약 칩 4개(서버 section) · 카드 네 줄 · 지금 상자(대기 · 마취 한 줄 · 마취 완료 N분 · 시술 중) · 호출 상자 + 호출 줄 + 카드에서 수락 · 호출 탭 수락 |
| `lib/ui/room_screen.dart` | 「< 시술현황 · {방}」 · 머리(상태 배지 · 시각 · needs 원문 · 모두 완료 합성 글자) · 호출 강조 상자(큰 경과 · 재호출 = canRecall · 큰 수락) · 오더 메모 위 여백 축소 · 마취 칸 · 시술 카드형 · 세로 ⋮ → 확인 창 · [의사 호출] · 모두 완료 상자 · 통역 드로어 숨김 시 닫기 |
| `lib/ui/doctor_picker.dart` | 호출 시트 한 장(① 시술 체크 · 전체 선택(pickable) ② 검색 · 추천 모든 의사 · 원장 줄 · 선택됨 · 호출할 시술 N개) · footer [취소] + 확인 · 시트가 보내고 실패면 다시 켬 · 아이패드 팝오버(레일 오프셋 보정) |
| `lib/ui/interpret_widgets.dart` | 통역 바(스피커 아이콘 알약 칩 · 가로 스크롤 · 끝 흐림 · [통역하기]) · 드로어(손잡이 · 「통역 · 언어」 드롭다운 · 방 · 경과 · [종료] · 가운데 자막 · 칩 · 큰 원형 마이크 · 상태) |
| `lib/interpret/langs.dart` · `lib/state/interpret_controller.dart` · `lib/main.dart` | `natLang`(TW→zh-Hant · CN · JP · TH · US · PH · IN · 그 밖 en) · zh-Hant 한국어 이름 「중국어(번체)」 · 첫 언어 = 고객 국적(전역 기억 제거) · 직접 바꾸기 유지 · `followCustomer` |
| `lib/ui/widgets.dart` · `lib/ui/theme.dart` · `lib/ui/format.dart` | 프로토 모양 조각(MsButton · Boxed · Tag · PillBadge · SheetHandle · AppHeader · Bell · DetailHeader) · 토스트 원형(어두운 둥근 · 2.6초 · 덮어쓰기 · 터치 통과) · Typo · 마취 보라(--day-st-consult-wait) · 표시 함수(needText · elapsedMin · clock · lastAnesMinutes · openCalls · callTargetLabel · vitals 순서 나이 \| 국적 \| 성별) |
| `lib/app.dart` | 판 묶음 → `AppShell` |
| `pubspec.yaml` · `pubspec.lock` | `shared_preferences` 제거(전역 마지막 언어 기억을 없앴으므로) — Podfile.lock 변화 없음 · native 코드 변경 없음 |
| `test/support/fixtures.dart` · `ui_harness.dart` | a1c90b9d 실제 모양 fixture(needs · lastSeconds · canRecall · limits 4칸) · `openCard` · `logoutViaSettings` · 캡처용 wrap |
| `test/ui/app_flow_test.dart` · `actions_test.dart` · `session_race_test.dart` · `test/data/board_stream_test.dart` · `test/interpret/interpret_test.dart` | 계약 변경분 정정 + 새 회귀(아래) |
| `test/capture/visual_capture_test.dart`(신규) | **검증 전용** — `DAY_CAPTURE_DIR` 있을 때만 실행(평소 skip 18건) · 실제 DayApp 위젯 + fixture · macOS 시스템 글꼴 |
| `README.md` | 셸 · 소비 기준 · 캡처 명령 · 국적 언어 · 종 배지 D-5 |

## 검증 — 실명령 · 수치 (증거 `mobile-ui-evidence/logs/`)

| 명령(cd app · FVM 3.44.8 · 전역 설정 변경 0) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **184 passed · 18 skipped(캡처 전용) · 0 failed**(이전 155) |
| `fvm flutter build ios --no-codesign` | ✓ Built Runner.app 17.5MB(최종 수정 뒤 1회) |
| `tool/native_logic_test.sh` | PASS 47 · FAIL 0 · ALL PASS(native 변경 없음 · 빠른 회귀) |
| `DAY_CAPTURE_DIR=… fvm flutter test test/capture/visual_capture_test.dart` | 18 passed → PNG 46장 |
| `fvm flutter build ios --simulator --debug --dart-define=…`(아래 로컬 값) | ✓ Built(시뮬레이터용) |

기존 155 테스트는 지우거나 느슨하게 하지 않았다. 바뀐 것은 계약이 바뀐 자리뿐: 머리 계정 버튼 → 설정 탭 로그아웃 · 상시 체크박스 → 호출 시트 · 「늘 원장 고르기 창」 → 직무별 · `need.why=call` 재호출 → `canRecall` · ⋮ 즉시 → 확인 창 · 마취 칩 → 마취 칸 버튼 · 「성공 토스트 없음」 → 원문 토스트 · 언어 기억 → 국적.

새 회귀(주요): 새 API shape 파서 · 옛 칸 무시 · limits 없음 · 원장 picker 안 뜸/간호 picker 뜸 × 목록 카드 · 상세 · 호출 탭 + 정확 body(`doctorStaffId`) · 지정 호출 기본 선택 · 원장 A→B 지정 즉시 본인 · 원장 즉시 수락 거절 토스트(창 안 엶) · 재호출 canRecall true/false/수락됨/보기만 · 확인 창 [닫기]=요청 0/[시작 취소]·[완료 취소] · 아이패드 모달 · 성공 토스트 글자 · 2.6초 · 덮어쓰기 · 이전 타이머 · SSE 남의 조작 토스트 0 · 떠난 화면(뒤로 · **다른 탭** · **상세가 덮음**) 늦은 2xx/409 토스트 0 · 닫힌 판 늦은 성공 0 · 시트는 덮은 것 아님 · 호출 시트 한 장 · pickable 줄만 · 409 task_not_pickable 시트 다시 켬 · 모두 완료 상자 · home 중복 없음 · canHome 없음 · TW→zh-Hant · 앞 고객 언어가 덮지 않음 · 드로어 언어 바꾸면 WS 재시작 · **드로어 연 채 탭 전환 / 푸시로 다른 방문 → 녹음 멈춤 · WS 닫힘** · 4메뉴 · 예약 · 채팅 · 알림 API 요청 0 · 320 · 599/600 · iPad 레일 · overflow 0.

## 구현 대조표 — UI 13항목 (SPEC-003 cdde456a)

| # | 항목 | 구현 | 근거(테스트 · PNG) |
|---|---|---|---|
| 1 | 셸 4메뉴 · 폰 탭바/아이패드 레일 · 예약 「곧 출시 예정」 · 채팅 자리 · 공통 머리 DAY/제목/종(배지 · 탭 동작 없음) · 계정은 설정 | 같음 | 셸 테스트 · `*-board-list` `*-tab-*` |
| 2 | 필터 4개 = 서버 `inbox.section` · 서버 순서 · 확인 필요 빨강 | 같음(프로토 알약 칩 모양) | 칩 테스트 · `*-board-filter-need` |
| 3 | 카드 4행(방–수납 / 이름·발음 / 나이·국적·성별 / 상자·담당의) · 진행 0/2 줄 없음 | 같음 · 둥근 14 · 프로토 여백 | 카드 테스트 · `phone-board-list` |
| 4 | 마취 중 한 줄 · 연보라 · 서버 long 만 빨강 · 「시술 대기 - 마취 완료 N분」(lastSeconds ÷60 내림) | 같음 | 마취 테스트 · `*-anesthesia-*` |
| 5 | 호출 뒤 카드(대상 · 수락 대기 · 시술 · 경과 · 건수 · 수락) · 상세 강조 상자 · 원장 즉시 / 간호 드로어 · 목록·상세·호출 탭 공통 · A→B 지정 즉시 성공 | 같음 | 수락 그룹 6+5건 · `*-call-wait-*` `*-nurse-accept-*` |
| 6 | 「< 시술현황 · {방}」 · 오더 메모 위 여백 축소 · 시술 카드(제목·담당의·상태·버튼) · 진행중 연한 DAY 배경·테두리·큰 경과 · 완료 아래 회색 · 시작/종료 DAY 주색 · 세로 ⋮(canUndo*) · 확인 원문 창 · 토스트 되돌리기 없음 | 같음(메모 위 패딩 12→8 · 크게 보기 버튼 높이 제거) | 진행·완료·확인 테스트 · `*-doing-room` `*-done-room` `*-undo-confirm` |
| 7 | 상시 체크박스 없음 · [의사 호출] → 한 시트(시술 체크/전체 선택 + 원장) · 마법사 없음 · pickable/canCall 서버 · 재호출 canRecall · 원장 고르기 유지 | 같음 · footer [취소]+확인(프로토) | 호출 시트 테스트 · `*-doctor-call-sheet-*` |
| 8 | 모두 완료 강조 상자(「시술 모두 완료」 · 「마지막 종료」 · [귀가 대기] canHome) · 머리 「시술 모두 완료 · 귀가 대기 전」 · 이탈은 서버 | 같음 | 모두 완료 테스트 · `*-all-done-room` |
| 9 | 통역 드로어 원형 · 칩 스피커 아이콘 · 알약 · 가로 스크롤 · [통역하기] | 같음(드로어 칩은 원본 PNG 대로 아이콘 없음) | 통역 테스트 · `*-interpret-drawer*` · `*-waiting-room` |
| 10 | TW → 중국어(번체) zh-Hant 첫 선택 · 앞 고객 언어가 덮지 않음 · 수동 변경 → 칩 · WS 같이 · 7언어 · vi/yue 칩 없음 · 보기 권한 통역 | 같음 | 국적 · 고객 전환 테스트 |
| 11 | 성공 토스트 어두운 둥근 상단 · 2.6초 · 덮어쓰기 · 원문만 · 본인 2xx 만 · 이전 세션/떠난 화면/SSE 없음 · 되돌리기 없음 · 오류는 DAY 코드 글자 | 같음 | 토스트 테스트 · `*-success-toast-*` |
| 12 | API 파서/fixture(아래 6차이) · 판정은 서버 · 환경 격리 · 세션 race · 로그 · 타임아웃 · redirect 차단 보존 · 원장 변경/방 이동/차트 쓰기 추가 없음 | 같음 · 세션 · 네트워크 코드 무변경 | session_race 7건 · 기존 세션/WS/네이티브 테스트 그대로 통과 |
| 13 | (UI 전반) 원형 디자인 + DAY 색 · 320/폰/iPad/599·600 overflow 0 | 같음 | 320 · 599/600 · iPad 테스트 |

## API 6차이 (dev 91728737 → 로컬 a1c90b9d)

| # | 차이 | 앱 |
|---|---|---|
| ① | 카드 `need` → `needs[]` 5상황 | 테두리 · 상세 원문(「대기/마취/호출 n분째」 · 「{doctorName} 수락 n분째」 · 「귀가 대기 전」) · 모두 완료면 home 글자는 합성 머리가 대신 · 칩 집계는 section |
| ② | `tasks[].canRecall` | [재호출] = 그 호출 줄 중 canRecall + board edit · 5분 조건 제거 · 기본 선택 = firstKind/firstTargetStaffId |
| ③ | 취소 확인 창 | 「{시술} 시작을/완료를 취소할까요?」 · [시작 취소]/[완료 취소] · [닫기] · 폰 시트/iPad 모달 |
| ④ | `lastMinutes` → `lastSeconds` | ÷60 내림 표시만 · [마취 시작]=새 회차 · 귀가 대기 뒤 서버 닫힘 그대로 |
| ⑤ | `pickable` 준비중만 | 시트 체크 가능 = 서버 값 그대로 |
| ⑥ | 원장 바꾸기 API · 검색 · 차트 API | 부르지 않음 · `call_already_accepted` 「다른 원장이 먼저 받았습니다」 · `task_not_pickable` 글자 추가 |

옛 칸 호환 분기는 만들지 않았다 — dev(91728737)에 붙이면 확인 필요 · 마취 완료 · 재호출이 비어 보일 수 있음(D-6 · 테스트로 「옛 칸 안 읽음」 고정).

## 스크린샷 (`mobile-ui-evidence/screens/` · 46 + 1)

- **전부 fixture 렌더**(테스트 더블 스냅샷 · 실제 backend 데이터 아님). 실제 `DayApp` 위젯 트리 · 실제 셸/Navigator · 글꼴 = macOS Apple SD Gothic Neo + SDK Material Icons(iOS 기기 SF 와 글꼴 차이 있음).
- phone(390×844) · ipad(1024×1366) 각 23장: `board-list` · `board-filter-need` · `tab-reservations` · `tab-chat` · `tab-settings` · `waiting-room` · `anesthesia-room` · `anesthesia-long-room` · `call-wait-list-doctor` · `call-wait-room-doctor` · `success-toast-accept` · `call-wait-list-nurse` · `nurse-accept-room` · `nurse-accept-drawer` · `doing-room` · `done-room` · `undo-confirm` · `success-toast-undo` · `all-done-room` · `doctor-call-sheet-empty` · `doctor-call-sheet-picked` · `interpret-drawer` · `interpret-drawer-lang`.
- `simulator-iphone-local-login.png` — **실제 시뮬레이터** 로컬 빌드 로그인 화면.
- 원본 13장과 눈으로 대조 · 고친 것: iPad 팝오버 위치(레일만큼 밀림) · 팝오버 검은 그림자 테두리 → 연회색 테두리 · 검색 칸 크기 · 원장 상태 글자 오른쪽 정렬 · 호출 시트 footer [취소]. 남는 차이(의도): 호출 상자 · 카드 대상 글자 「전체 의사」(OQ-A8 DAY 웹 글자 · 원본 「전체 호출」) · 헤더 상태 배지 글자 DAY(「시술 대기/시술 중/확인 필요」) · 국적 · 재내원 · 입실 칩 없음(DAY 결정) · 원본 진행 0/2 줄 없음(사용자) · 상세 머리에 방 이름 대신 내비게이션 오른쪽 방(사용자) · 원본 「호출할 대기 시술 없음」 글자 대신 꺼진 [의사 호출] · 드로어 아이패드 옆 빠른 말하기 목록 대신 같은 칩 줄(SPEC 배치) · 마취 「안 함」 글자 없음.

## 로컬 연결 · 시뮬레이터

- 읽기 전용 확인: `GET http://127.0.0.1:11040/health/ready` = 200 · 토큰 없이 `GET /api/board` = 401 `unauthorized`.
- 빌드 값(debug 만 · 소스 하드코딩 0): `DAY_LOGIN_ENTRY` · `DAY_DEV_LOCAL_ORIGIN` = `http://127.0.0.1:11040` · `DAY_REQUIRE_ENVIRONMENT=false` · `DAY_APNS_ENV=sandbox` · `DAY_ALLOWED_ORIGINS` 비움. release 규칙(https · 허용 목록 · 환경 필수) 그대로.
- 기기: 기존 `orca-mobile-iphone` 5C9E05C7-7171-455E-97CE-2AD2EA097F88(Booted 확인 · 재사용 · 다른 기기 0). 같은 번들 `com.example.day.placeholder` 재설치 · 실행 **PID 66626** · 로그인 화면 대기(켜 둠). iPad 시뮬레이터는 쓰지 않음(위젯 렌더로 대체).
- 이전 day-dev 세션: Keychain 을 읽지 않았다. 앱 복원 로직이 「빌드 허용 목록 밖 대상 묶음은 요청 없이 지움」(`session_controller.dart:115-120`, 기존 코드)이라 로컬 빌드에서 day-dev 토큰은 어디에도 보내지지 않는다.
- ATS: 저장소 · 빌드 산출물 Info.plist 에 ATS 예외 키 0(device · simulator 둘 다). 로그인 전에는 앱이 요청을 보내지 않아 **http://127.0.0.1 이 ATS 에 막히는지는 확인 못 함** — 사용자가 로그인할 때 막히면 개발자 로컬 ignore 설정으로만 다룰 것(README 기존 문장).
- **로그인 · authenticated 통합 미실행**(자격증명 찾기 · 토큰 추출 · 로그인 시도 0). live API 정합은 소스(a1c90b9d board_rules.py · board_parts.html · routers/board.py MESSAGES) + fixture 대조까지.

## 남은 실물 의존 · 주의

- 사용자 로그인 뒤 실데이터 확인(로컬 day-local) · ATS · 실제 needs/canRecall 표시.
- D-2(기기 등록 · APNs) · D-3(통역 WS · Soniox) · D-5(알림 미읽음 API — 종만) · D-6(옆 #920 · #236 머지 전 dev 는 옛 칸) 서버 pending 그대로.
- OQ 기본값 진행: A8(「전체 의사」) · A20(마취 보라 = consult-wait 토큰) · A21(시술 중 상자 · 겹치면 호출 상자 우선 · 첫 담당의) · A22 · A23 · A24(오류도 같은 어두운 토스트) · A26 · A27(성별) · A28 · A29 · A30 — 리뷰 확인 대상.
- 「떠난 화면」 정의 = 탭이 보이고 그 화면 위를 다른 PageRoute 가 덮지 않음(시트 · 창은 그 화면에서 연 것이라 덮은 것 아님) — 코디 지적 반영.
- 시술 중 카드의 상자 색(연한 주색)은 프로토 원형을 따름(OQ-A21 장식 최소 기본값과 긴장 — 리뷰 확인).
