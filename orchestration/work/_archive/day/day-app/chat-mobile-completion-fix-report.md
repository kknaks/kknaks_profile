# 채팅 이식 누락 수정 보고 — task_d72999cc8bae / ctx_5cb263ead35d

- 근거: SPEC-004 @53adbd49 §3 케이스 매트릭스(:433 「스트림 끊김」) · SPEC-003 U-1 · 케이스 매트릭스 403 @`b0f71ec3`(코디 재검수 PASS 메시지 msg_6ebcc5e35aa3 받은 뒤 권한 수정 착수)
- 범위: `app/` 만 · commit/push/merge/하위위임 0 · backend 워커 dirty 손대지 않음 · 새 UI 글자 0
- 결과: **4항목 완료 · 검증 PASS** / 활성화 전제(로컬 11040 서버 `/api/chat/*` 404)는 그대로

## 1. 채팅 연결 줄(SPEC-004 §3 :433)

| 파일 | 변경 |
|---|---|
| `lib/chat/chat_kit.dart` | `ChatConnectionLine` — 기존 `ConnectionLine`(SPEC-003 U-12 노란 줄 · 원문 글자 「서버에 연결 중…」/「연결 끊김 · 다시 연결 중」)을 **`ChatState.streamStatus`(채팅 전용 스트림)** 에 이음. 판 스트림과 무관. `ChatTabScaffold` 머리 아래(목록 · 아이패드 두 칸 공통 한 줄) |
| `lib/chat/screens/chat_room_screen.dart` | 폰 대화 머리 아래 같은 줄(아이패드 오른쪽 칸은 목록 줄 하나만) |

- 처음 연결 전 = connecting · 한 번 붙은 뒤 끊김/뒤로 감 = reconnecting(ChatStream 기존 상태 그대로 — 새 계약 0).
- 시험 `test/ui/chat_ui_test.dart`「채팅 연결 줄」: 채팅 스트림 503 → 「서버에 연결 중…」 · 같은 때 판 탭은 줄 없음(판 스트림 붙음) · 복구 → 없음 · 대화 화면에서 끊김 → 「연결 끊김 · 다시 연결 중」 → 3초 뒤 복구 → 없음. board 없는 직원도 채팅 상태는 같은 경로(아래 §3 시험에서 채팅 스트림 동작).
- PNG `day-v2/{phone,ipad}-11-chat-connecting.png` · `-12-chat-reconnecting.png`.

## 2. SPM Package.resolved · README

- `ios/Runner.xcworkspace/xcshareddata/swiftpm/Package.resolved` · `ios/Runner.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved` — 두 파일 `cmp` 동일 · 로컬 경로 · 키 · 토큰 문자열 0 · 커밋 대상 유지(SDWebImage 5.21.7 · SDWebImageWebPCoder 0.15.0 · libwebp-Xcode 1.6.0 — flutter_image_compress 전이).
- `README.md` — 구조(lib/chat · day/video · 앞 채팅 → 앱 안 배너) · 서버 의존 D-4(채팅 API · 스트림 · 채팅 APNs, 없으면 목록 비고 연결 줄) · 「채팅 iOS 의존 · 권한」(버전 · SPM lock · Info.plist 글자 · ATS 예외 0 · day/video) · 알림 목록/공통 interface = 후속 SPEC · 채팅 캡처 명령.

## 3. 같은 viewport 원형 대조

- 원형 스크래치: `scratchpad/protoapp/procedure/app`(77173cf8 `git archive` — 원본 저장소 수정 0) · 캡처 시험 `test/zz_capture_test.dart`(스크래치 전용).
- 같은 viewport: 폰 390×844 · 아이패드 1024×1366(세로) · dpr 2 · 원형 main.dart builder 의 태블릿 글자 배율(`uiScale`)까지 같게(1차 재캡처에서 빠져 고친 뒤 다시 찍음).
- 출력: `chat-mobile-evidence/proto-same/`(18) · `day-v2/`(28 — 대조 18 + 연결 줄 4 + board 없음 4 + 보내기 실패 2) · `pairs-same/`(18 — 원형 | DAY, 같은 픽셀 크기 `assert` 통과).
- 장면: 목록 · 대화 · 새 대화 · 초대 · 방 정보 · 첨부 · 전달 · 크게 보기 · 오류(없는 방)/안 읽음.
- 대조 결과: 배치 · 크기 · 문구 같음. 차이 = DAY 토큰 색 · 「DAY」 · 4메뉴 · 직무 이름(원장/코디네이터/상담실장) · 원형 「서버에 연결 중…」 줄(원형 판 스트림 — DAY 는 채팅 스트림 live 라 줄 없음, 끊김 장면은 11 · 12).
- 원형 「오류」 장면 2건 시험 실패 표시는 캡처 뒤 원형 토스트 타이머가 남은 것(「A Timer is still pending」) — PNG 는 정상.

## 4. 권한 진입 수정(SPEC-003 U-1 @b0f71ec3)

| 파일 | 변경 |
|---|---|
| `lib/state/session_controller.dart` | `/me` 200 = 늘 `Phase.board`(셸) + `boardForbidden = !canViewBoard`. `showForbidden(of:)`(판 조회 · 판 SSE `forbidden`) = 지금 세션일 때만 `boardForbidden = true` — 세션 · 푸시 종료 없음(hooks.onSessionEnded 안 부름). 로그아웃/세션 끝 = 초기화. `/me` 자체 403 = 기존 `Phase.forbidden`(그대로) |
| `lib/app.dart` | 판(BoardController · 판 SSE) = `Phase.board && !boardForbidden` 일 때만. 채팅 = `Phase.board` 일 때만(`/me` 403 에선 시작 안 함 — 이전 v7 은 시작했음). 셸 key = 세션 묶음(권한 회수돼도 셸 · 채팅 유지) |
| `lib/ui/shell.dart` | `board` nullable · null 이면 「시술현황」 본문 자리에 `BoardForbiddenBody`(기존 권한 없음 글자 + [로그아웃] — 새 글자 0) · 판이 바뀌면 시술현황 칸 Navigator 만 새로(옛 룸 상세 · 통역 드로어 정리) |

- board 없음 = 판 API · 판 SSE · 고객 정보 · 통역 0 · 서버 권한 확대 0. 채팅 403(직원 비활성 · 멤버십 상실)은 v7 그대로 토스트 + 채팅 목록 비움(별도 경로 · 같이 취급하지 않음).
- 늦은 이전 세션 `showForbidden` · `endSession` = 무시(기존 `sameSession` 보호 · 시험 유지).

시험:
- `test/state/session_controller_test.dart`: /me 200 board 없음 → Phase.board + boardForbidden · 묶음 유지 / /me 403 → Phase.forbidden / 세션 도중 판 forbidden = 영역만 · ended hook 0 · 세션 끝에 초기화 / (기존) 이전 세션 늦은 showForbidden 무시.
- `test/ui/chat_ui_test.dart`: board 없는 활성 직원 — 탭바 · 시술현황 자리 안내 · 채팅 배지 · 방 열기 · **보내기 POST** · 설정 로그아웃 보임 · 판 SSE 0 · `/api/board`·`/api/interpret` 요청 0 / `/me` 403 — 안내 · 탭바 없음 · 채팅 요청 · 스트림 0 / 세션 도중 판 SSE forbidden — 영역 안내 · 탭바 유지 · 판 스트림 닫힘 · 세션 묶음 유지 · 채팅 스트림 열린 채 · 채팅 목록 보임.
- 기존 `app_flow_test`「권한 행 없는 직무 — 권한 없음 안내 + 로그아웃」 그대로 통과(이제 시술현황 자리).
- PNG `day-v2/{phone,ipad}-13-board-forbidden.png` · `-14-board-forbidden-chat.png`.

## 5. 최종 검증(각 1회 · 로그 `chat-mobile-evidence/logs2/`)

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues |
| `fvm flutter test` | **245 passed · 47 skipped**(캡처 장면) · 실패 0 — 이전 240 → −2(권한 시험 2건을 새 의미 시험으로 교체) +7(세션 3 · 위젯 4: 연결 줄 1 · 권한 3). skip +4 = 새 캡처 장면 |
| `sh tool/native_logic_test.sh` | 54 PASS / ALL PASS(네이티브 소스 이번 변경 0) |
| `fvm flutter build ios --release --no-codesign` | 성공 20.6MB |
| `fvm flutter build ios --simulator --debug` + 11040 defines 4개 | 성공 |
| 시뮬레이터 overwrite install + launch | PID 45031 → **70352** · uninstall/erase/logout/실제 채팅 조작 0 · 로그인 세션 유지(시술현황 화면) — `simulator-after-install-v2.png` |

## 6. 남은 것

- 활성화 전제: 로컬 11040 `/api/chat/rooms` · `/api/chat/stream` 404(무인증 탐침 · `/api/board/stream` 401) — 채팅 백엔드 배포 전. 시뮬레이터에선 채팅 목록 비고 채팅 연결 줄이 「서버에 연결 중…」로 보일 것(정상 동작).
- 실기기 pending(이전 보고 그대로): 카메라 · 사진첩 제한 접근 · 동영상 변환/재생 · APNs 채팅 푸시 · AVPlayer 리다이렉트.
- 커밋 대상: 이전 v7 파일 + 이번 `lib/chat/chat_kit.dart` · `chat_room_screen.dart` · `session_controller.dart` · `app.dart` · `shell.dart` · `README.md` · 시험 4개 · Package.resolved 2개.
