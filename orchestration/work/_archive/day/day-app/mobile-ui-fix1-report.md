# day-app mobile — UI 독립리뷰 WARN1~4 보완 + iOS 로컬 읽기전용 연결 probe (task_783997f3df7d · ctx_5e453fa0cd95)

## 상태: done — 코드 · 증거 보완 완료 · 앱 프로세스 → 로컬 public health 200 확인. 로그인 · 인증 통합은 미실행(사용자)

- 입력: `review-mobile-ui-report.md`(PASS · WARN 4) · `mobile-ui-code-report.md` · `mobile-ui-code-brief.md`. 코드 트리 `day-app` 시작 `0b776e90` 위 미커밋 UI. 변경 `app/**` 만 · 커밋 · push · merge 0. 서버 · 스펙 · 실 env · 서명 · 계정 · 포트 · DB 0. 하위 위임 0.
- 이전 증거 보존: `mobile-ui-evidence/screens/` · `logs/`(1차) 그대로. 이번 것 = `screens-fix1/` · `logs-fix1/` · `probe/`.

## 변경 (app/)

| 파일 | 변경 | 이유 |
|---|---|---|
| `lib/ui/room_screen.dart` `_openCallSheet` | `where` = 늘 `'{방} · {고객}'`(폰도) — 1줄 | WARN-2 · SPEC U-5 머리 「방 · 고객 이름」 · 폰 수락 드로어 · iPad 와 같음 · 새 글자 없음(서버 값) |
| `lib/ui/doctor_picker.dart` 머리 `where` | `maxLines 1 → 2` | 320 에서 긴 방 이름이 고객 이름을 가리던 것(눈 검수에서 드러남) |
| `lib/ui/widgets.dart` `CustomerName` | `maxLines 1 → 2` | 320 긴 영문 이름이면 한글 발음이 말줄임으로 통째로 사라짐 → 다음 줄로 |
| `lib/ui/room_screen.dart` 호출 상자 | [재호출]+[수락] 둘 다일 때 폭 < 300×배율이면 위아래로 쌓음 · 넓으면 [재호출] 96 고정 + [수락] 나머지 | 320 · iPad 600 경계(글자 1.15 배)에서 「원장 골라 수락 · N건」이 「원장 골라 수락 · …」로 잘림(드러난 결함) |
| `test/capture/visual_capture_test.dart` | `_callsOf(cards)` — 카드의 열린 호출(called · accepted 줄의 유효 호출)을 서버 `calls_view` 와 같은 모양으로 `calls[]` 에 늘 실음 · `doneTab` fixture · 켜진 [시작](`canStart: true`) · 320/599/600 긴 이름 시나리오 · 호출 탭/시술 완료 탭 | WARN-1 · 3 · 4 |
| `test/ui/actions_test.dart` 320 테스트 | 쌓인 [재호출] · [수락]을 `ensureVisible` 뒤 누름 | 위 배치 변경에 맞춤(검사 내용 같음) |

기능 확대 · 새 API · 새 글자 · 원형/4행/4탭 변경 없음. native 변경 0.

## 검증 — 실명령 · 수치(`logs-fix1/`)

| 명령(cd app · FVM 3.44.8) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **184 passed · 25 skipped(캡처 전용 · 평소 skip) · 0 failed** |
| `DAY_CAPTURE_DIR=…/screens-fix1 fvm flutter test test/capture/visual_capture_test.dart` | 25 passed → PNG 66장 |
| `fvm flutter build ios --no-codesign` | ✓ Runner.app 17.5MB(마지막 lib 수정 뒤) |
| `fvm flutter build ios --simulator --debug --dart-define=DAY_LOGIN_ENTRY/DAY_DEV_LOCAL_ORIGIN=http://127.0.0.1:11040 · DAY_REQUIRE_ENVIRONMENT=false · DAY_APNS_ENV=sandbox`(표준 `lib/main.dart`) | ✓ Built |
| Info.plist ATS 키(`NSAppTransportSecurity`) — device · simulator 산출물 | 0 · 0 |
| native Swift 47 | 재실행 안 함(native 변경 0 · 1차 47 PASS) |

## WARN 대조

| WARN | 해소 | 증거(`screens-fix1/` · 전부 fixture 렌더) |
|---|---|---|
| 1 「호출 0」인데 수락 대기 카드 | 캡처 fixture 가 카드 호출을 `calls[]` 에도 실음(서버 `calls_view` 모양: callId · visitId · room · customer(이름 · 발음 · 국적) · kind · targetStaffId · createdAt(= 그 호출 created) · acceptedBy · acceptedAt · tasks) | `phone-board-list`(호출 1 — 수락 대기 1 · 수락된 c5 · c9 는 「수락함」) · `phone-call-wait-list-*`(호출 1) · `phone320-long-list`(호출 2) · `*-calls-tab` |
| 2 폰 호출 시트 머리 고객 없음 | 폰도 「방 · 고객」 | `phone-doctor-call-sheet-*`(「A-룸1 · TEST CLAUDE」) · `phone320-long-call-sheet`(긴 방 · 고객 2줄) |
| 3 320 긴 이름 · 599/600 | 목록 · 상세 · 시술 목록 · 호출 시트 각 1장 × 320 · 599 · 600 | `phone320-long-*` · `short599-long-*` · `short600-long-*`(599 = 폰 탭바 · 600 = 레일 · 두 열) |
| 4 켜진 [시작] · 호출 탭 · 시술 완료 탭 | 서버 canStart true 줄 = DAY 주색 테두리 [시작] · 호출 탭 수락 대기/수락함 · 시술 완료 탭 귀가 대기/귀가 | `*-startable-list` · `*-startable-room` · `*-calls-tab` · `*-done-tab`(phone · iPad) |

눈 검수: 66장 중 위 새 장면과 1차 장면을 다시 열어 잘림 · 겹침 확인 → 드러난 3건(발음 사라짐 · 수락 버튼 글자 잘림 · 시트 머리 고객 가림)을 위처럼 고친 뒤 다시 캡처. 남는 것(의도): 320 룸 상세는 머리 + 통역 바가 고정이라 본문 보이는 높이가 작다(스크롤 · 기존 배치 · 재설계 안 함) · 600 경계 두 열의 긴 시술명은 여러 줄로 감김.

스크린샷 표시: **모두 테스트 더블 fixture**(실제 backend 데이터 아님) · 실제 DayApp 위젯 트리 · macOS Apple SD Gothic Neo + SDK Material Icons(테스트 기본 네모 글꼴 아님) · cards/calls/doneTab 서로 맞춤.

## §4 iOS 로컬 network probe — 읽기 전용 · 자격증명 없음

- 검증 전용 entrypoint: `mobile-ui-evidence/probe/health_probe.dart`(profile 증거 · 제품 코드 아님 · `app/lib/main.dart` 무수정 · 새 production flag/화면/route 0 · 새 패키지 0). 앱이 쓰는 `package:http` Client(DayApi 와 같은 것) + `dart:io HttpClient` 로 `GET {PROBE_ORIGIN}/health/ready` 한 번씩 · 리다이렉트 안 따라감 · 상태/바이트 수만.
- 명령: `fvm flutter run -t <probe> --no-resident -d 5C9E05C7-7171-455E-97CE-2AD2EA097F88 --debug --dart-define=PROBE_ORIGIN=http://127.0.0.1:11040`(같은 번들 · 같은 Runner Info.plist · ATS 예외 0).
- 결과(`probe/flutter-run-probe.txt` · 앱 sandbox 파일 사본 `probe/sandbox-day-health-probe.txt` · 화면 `probe/probe-screen.png` · probe PID 83644):
  ```
  GET http://127.0.0.1:11040/health/ready
  package:http status=200 bytes=73
  dart:io HttpClient status=200 bytes=73
  ```
- 뜻: **시뮬레이터 앱 프로세스 → 로컬 public health 실제 통신 200**(ATS 예외 없이). 로그인 · 인증 · 판 API 통합 성공이 아니다. 자격증명 · Keychain · 로그인 · 업무 쓰기 · 서버 재시작 0.
- 그 뒤 **표준 `lib/main.dart` 로컬 debug 빌드로 재설치 · 실행** → probe 화면 남지 않음 · DAY 로그인 화면(`screens-fix1/simulator-iphone-local-login.png`) · **최종 앱 PID 86372**(`orca-mobile-iphone` 켜 둠). 다른 기기 0.

## 남은 것 · 주의

- 로그인 · authenticated 통합(로컬 day-local) 미실행 — 사용자.
- D-2 · D-3 · D-5 · D-6 서버 pending 그대로. OQ 기본값(A8 「전체 의사」 등)은 1차 보고 그대로.
- 폰 시트 머리를 「방 · 고객」으로 바꿔 원본 PNG(방만)와 글자가 다르다 — SPEC U-5 정본을 따른 결과(코디 지시).
