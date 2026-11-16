# 리뷰 — DAY 채팅 앱(app/) 독립검수 · read-only (2026-11-10)

- 대상: `CENTURION_DAY/day-app` 작업 tree 의 app/ 미커밋 변경 전체(44 파일 · sha256 = `chat-mobile-review-logs/app-changed-hashes.txt`).
- 근거: SPEC-004 @53adbd49 · SPEC-003 U-1 권한 명확화 @b0f71ec3 · 보고 `chat-mobile-code-report.md` · `chat-mobile-completion-fix-report.md` · 증거 `pairs-same/` · `day-v2/` · 원천 cc-prototype 77173cf8(git show 만).
- 하지 않은 것: 코드 수정 0 · 사용자 시뮬레이터 조작 0 · DB 테스트 · 서버 설정 · 기동 0 · backend 손대지 않음 · 하위 위임 0.
- 역할 공개: 나는 이 Delivery 의 backend 작성자다(app 작성에는 참여하지 않음). app ↔ server 계약 대조는 내 backend 코드를 기준으로 한 것이라, 통합 리뷰에서 한 번 더 보는 것을 권한다.

## 판정: **PASS with WARN (FAIL 0 · WARN 1)**

## 독립 재실행 (각 1회 · `chat-mobile-review-logs/`)

| 명령 | 결과 | 보고와 대조 |
|---|---|---|
| `fvm flutter analyze` | No issues | 같음 |
| `fvm flutter test` | **245 passed · 47 skipped**(캡처 장면) · 실패 0 | 같음 |
| `sh tool/native_logic_test.sh` | ALL PASS(PASS 줄 55 · 마지막 `doctor_call tap keys unchanged`) | 보고 「54 PASS」 — 줄 수 세는 방법 차이로 보이며 실패 0 은 같다 |
| unsigned · simulator 빌드 | 다시 돌리지 않음(보고 로그로만 대조) | — |

## 항목별 확인

| 항목 | 근거(파일:줄) | 판정 |
|---|---|---|
| SPEC-003 U-1 @b0f71ec3: `/me` 200 + board 없음 → 셸 · 채팅 · 설정 유지 · 판 API/SSE · 통역 0 | `lib/state/session_controller.dart:335`(`Phase.board`) · `lib/app.dart:107`(판 = `!boardForbidden` 일 때만) · `:131`(채팅 = `Phase.board`) · 위젯 시험 board 없는 직원 · `/api/board` · `/api/interpret` 요청 0 · 캡처 `day-v2/*-13/14` | PASS |
| `/me` 자체 403 = 기존 전역 차단 · 채팅 시작 0 | `app.dart:131` `live = phase == board` · 시험「/me 403 — 채팅 요청 · 스트림 0」 | PASS |
| 채팅 API/SSE 403(직원 비활성 · 멤버십 상실) = 토스트 + 목록 비움 · 세션 종료 아님 | `lib/chat/chat_state.dart:213-228`(HTTP) · `:303-309`(SSE `session_expired: forbidden`) · 앞으로 오면 `resume` 으로 다시 연결(`chat_stream.dart:64`) | PASS |
| 채팅 연결 줄 = 채팅 스트림 상태 · 판과 별개 · SPEC-003 U-12 글자 | `chat_kit.dart` `ChatConnectionLine` · 시험「채팅 연결 줄」 · 캡처 `*-11/12` | PASS |
| HTTP 20 + 첨부 계약(내 backend 대조) | `chat_api.dart`: 경로 · `beforeSeq`/`since`/`limit` 만(서버는 모르는 쿼리 400 — 맞음) · `{seq}` 읽음 · multipart 칸 이름(roomId · photo · video · thumb · width · height · durationMs) · Content-Length 고정(서버 bounded read 와 맞음) · 오류 `{detail,code,field}` | PASS |
| 1:1 「(비활성)」 두 번 붙음 여부 | 서버 `name` 은 접미사를 붙이지만 앱 `roomTitle`(`chat_view.dart:13`)은 1:1 에서 `peer.name` 을 쓰고 표시는 `peerInactive` 로 따로 → 한 번만 | PASS |
| 역할 `role: null`(직무 없음) | `ChatRole.parse` → 빈 이름이면 Badge 숨김(`chat_ui.dart:14`) | PASS |
| SSE: Bearer · 리다이렉트 안 따라감 · 머리(200)에서 onConnected → 목록 · since | `chat_stream.dart:94-115` — 서버 W1 수정(구독을 머리 전에 확인)과 맞물린다 | PASS |
| 세션 격리: 늦은 401/2xx · SSE · 픽커/변환 뒤 업로드 · 배너 · 토스트 | `_disposed` 가드(chat_state 전반) · 콜백 = 그 세션(`app.dart:146` `endSession(code, of: s)`) · `sendMany` dispose 시 변환 파일 삭제(`:708-715`) · 시험「dispose 뒤 늦은 401·2xx」 | PASS |
| 푸시 누름 · 앞 배너 = environment + hospitalId(현재 `/me`) | `push_coordinator.dart` `_chatScope` · `app.dart:76` `session.me?.hospitalId` · 로그인 전 누름 = `_waitingTap` | PASS |
| SSE + 앞 푸시 같은 messageId 배너 한 번 · 알림 끔 · 보고 있는 방 · 뒤 = 버림 | `chat_state.dart:650-661` | PASS |
| native willPresent · tap 의 환경/병원 | `AcceptLogic.swift` `PushPayload` · `AppDelegate.swift` willPresent: Dart 준비됨 + `kind=chat` 이면 시스템 배너 없이 Dart 로(환경 · 병원 판정은 Dart). 아래 「참고 1」 | PASS(참고) |
| 원장 호출 native category · Keychain · 통역 오디오 회귀 | native 시험 `doctor_call tap keys unchanged` 등 ALL PASS · VideoConverter 오디오는 `.playAndRecord`/`.record`(통역)일 때 손대지 않음 | PASS |
| 동영상 재생 = Bearer 헤더 · 세션 origin · 서명 URL 없음 | `chat_video_screen.dart:108` `networkUrl(httpHeaders)` · 서버는 리다이렉트를 하지 않음 | PASS(실기기 pending) |
| 권한 문구 · PHPhotoLibrary 키 · ATS 예외 0 | `Info.plist` diff — SPEC-004 §4 원문(카메라는 「여권…」만 삭제) · `PHPhotoLibraryPreventAutomaticLimitedAccessAlert=true` | PASS |
| SPM lock 2개 · README | 두 `Package.resolved` `cmp` 동일 · 원격 URL · 버전만 · 로컬 경로 · 토큰 0 · README 채팅 의존/권한 절 | PASS |
| 같은 viewport 원형 대조 | `pairs-same/` 18쌍 중 대화(폰) · 전달(아이패드) 등 직접 열람: 배치 · 크기 · 문구 같음 · 차이 = DAY 색 · 「DAY」 · 4메뉴 · 직무 이름 · 원형의 판 스트림 연결 줄 | PASS |
| 가로 · 긴 문자 · 키보드 · 잘림 증거 | 아래 W1 | **WARN** |

## WARN

### W1. 가로 방향 · 긴 이름/제목 · 키보드 열린 상태의 화면 증거가 없다

- 브리프가 요구한 「가로/긴문자/키보드/필수버튼잘림 · 레이아웃 오버플로우」를 보여 주는 캡처나 시험이 없다. `test/` 에서 landscape · viewInsets · 키보드 · overflow 를 찾았지만 채팅 시험에는 없다. 캡처는 모두 세로이고 지어낸 짧은 이름만 쓴다.
- 코드가 원형 그대로라 큰 위험은 낮다. 다만 DAY 직무 이름은 원형 다섯 역할보다 길다(「코디네이터」 · 「상담실장」). 실제로 아이패드 목록 행에서 「마관리 관리자 (비활…」이 잘린다(원형도 같은 자리에서 잘려 회귀는 아님).
- 최소 정정(앱 워커): 캡처 장면을 몇 개 더한다. 폰 가로(844×390) 목록 · 대화, 대화에서 키보드가 열린 상태(viewInsets) 입력줄 · 탭바, 긴 직원 이름 · 긴 그룹 제목 · 긴 직무 이름의 목록 행 · 대화 머리 · 공유 시트. 각 장면에서 RenderFlex overflow 가 0 인지 단언한다.

## 참고 (결함 아님 · 기록)

1. **native 에는 병원 값이 없다.** Keychain 세션 묶음에 hospital 칸이 없어 native 가 병원을 볼 수 없다. 그래서 다음 두 경우에는 iOS 시스템 배너가 그대로 보인다.
   - 앱이 뒤에 있거나 잠금 화면일 때(iOS 기본 동작).
   - Dart 가 준비되기 전 몇 초(`dartReady=false`).
   - 이 경우 다른 병원 메시지가 보이지 않는 근거는 서버 대상 선정이다. 기기의 결속 세션 병원이 방 병원과 같고 세션이 살아 있을 때만 보낸다(backend A37 · 실제 PG 테스트).
   - Dart 가 준비된 앞 상태에서는 채팅 알림을 늘 시스템 배너 없이 Dart 로 넘기므로, 환경 · 병원이 다르면 아무것도 보이지 않는다.
   - 누름은 Dart 가 환경 · 병원을 확인한 뒤에만 이동한다.
   - 서버 대상 선정이 틀리면 막을 길이 없다(SPEC 이 정한 방어선은 「앱은 무시」까지).
2. 실기기 pending(보고 그대로): 카메라 · 제한 접근 「더 고르기」 · HEVC 변환 · Range 재생 · AVPlayer 리다이렉트 헤더 · APNs 채팅 푸시. 시험 통과를 실기기 성공으로 볼 수 없다.
3. 활성화 전제: 로컬 11040 서버에 채팅 API 가 아직 없다(보고 기준). 통합 E2E(실서버 응답 샘플 · 오류 · SSE 조립)는 별도로 한다.
4. 보고의 native PASS 수(54)와 내 실행 출력의 PASS 줄 수(55)가 하나 다르다. 실패는 0 으로 같다(세는 방법 차이로 보임).

## 계약 차이 · 코디 질문

- 지금 발견된 app ↔ server 계약 차이는 없다.
  - 서버의 구현 선택(같은 clientId 를 다른 방에 보내면 404 · `role: null` · UTC 시각 · 1:1 이름 접미사)을 앱이 모두 받아들인다.
  - 다른 방 clientId 404 는 앱이 「보내는 중 말풍선 지움 + 오류 토스트」로 처리한다(4xx 규칙).
