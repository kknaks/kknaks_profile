# 리뷰 — DAY 알림 v8 앱(app/) 독립검수 · read-only (2026-11-10)

- 대상: base `3aaa9780` 위 app/ 미커밋 v8 변경(23 파일 · sha256 = `notification-mobile-review-logs/app-changed-hashes.txt`).
- 근거: SPEC-005 @`b0f71ec3` 전문 · SPEC-003 U-14/U-16 · 원형 cc-prototype `77173cf8`(git show) · `notification-mobile-code-report.md` · 증거 `notification-mobile-evidence/`.
- 하지 않은 것: 코드 수정 0 · 시뮬레이터 · 실서버 · 실키 · DB · 포트 조작 0 · backend 수정 · DB 시험 0.
- **편향 공개**: 나는 이 v8 서버(backend)의 작성자다(app 작성 참여 0). API 대조는 SPEC-005 §3 을 기준으로 했고 내 서버 코드는 보조로만 봤다. 앱 시험은 모두 테스트 더블이다 — 실서버 통합으로 주장하지 않는다.

## 판정: **PASS with WARN (FAIL 0 · WARN 1)**

## 독립 재실행 (`notification-mobile-review-logs/`)

| 명령 | 결과 | 보고 대조 |
|---|---|---|
| `fvm flutter analyze` | No issues | 같음 |
| 집중(`test/notify` · `test/ui/notification_ui_test` · `test/state` · `test/ui/chat_ui_test` · 알림 캡처/레이아웃) | 96 passed · 12 skipped | — |
| `fvm flutter test` 전체 1회 | **277 passed · 59 skipped** · 실패 0 | 같음 |
| `sh tool/native_logic_test.sh`(native 변경 있음) | ALL PASS · PASS 줄 57 | 같음 |
| build | 다시 돌리지 않음(보고 로그 대조만) | — |

## 항목별

| 항목 | 근거(파일) | 판정 |
|---|---|---|
| 종 = 서버 `unread` 만 · 99+ · 0 숨김 · 접근성 「알림 n개 안 읽음」/「알림」 · 모든 탭 · 채팅 배지와 따로 | `ui/widgets.dart` `Bell` · PNG pairs 01-03 · ui 시험 | PASS |
| 다시 읽는 때: 로그인 뒤 · 앞으로 옴 · 스트림 (재)연결 · 행 읽음 뒤 · 앞 원장 호출 푸시 | `notification_controller.dart` start · `onConnected` · `setForeground` · `readCall` · `push_coordinator._onForeground` | PASS |
| 알림 전용 SSE `/api/notifications/stream` · `notification {unread}` 만 · 끊김 줄 없음 · 재연결 재전송 기대 0 | 같은 파일 + `chat_stream.dart`(`path` · `events` 인자 · 채팅 기본값 그대로) | PASS |
| 목록이 열린 동안 unread 가 바뀌면 다시 읽기 · 무한 반복 없음 | `notification_screen.dart` `_load` — 다른 값일 때만 unread 를 고쳐 다시 한 번만 돈다(같으면 멈춤) | PASS |
| 읽음 구분: 행 = `ids:[id]`(안 읽은 행만) · 푸시 누름 = `callId` · 모두 읽음 = 빈 본문(두 칸 없음) · 중복 요청 0 | `notification_screen._open` · `_readAll` · `push_coordinator._onTap` → `onCallOpened` | PASS — 서버의 「칸에 null = 400」과도 맞다(앱은 칸을 뺀다) |
| 설정: 서버 받는 종류만 · 기본 true · 스위치 PUT → 다시 읽기 · 실패 = 글자 토스트 + 서버 값 · `setting_not_allowed` 글자 · OS 거부 「알림 꺼짐 · 설정에서 켜기」 · 「받는 알림이 없어요」 | `notification_settings.dart` · PNG 07-08 | PASS |
| 목록 모양: 폰 전체 화면(탭바 위) · 아이패드 오른쪽 420(‹ 없음) · 행(점 · 제목 · HH:MM · 본문 · 안 읽음 바탕 · 줄) · 빈 · 오류 · 로딩 · 당겨서 새로 고침 | `notification_screen.dart` · pairs 04-06 직접 대조 | PASS |
| 원형 동일성(같은 viewport) | `pairs/phone-04-list` 등 직접 열람 — 배치 · 크기 · 글자 같음 · 차이 = DAY 색 · 「DAY」 · 4메뉴 · 원형 「이 기기」 · 「앱 정보」 칸 없음(§1 뺌) | PASS(아래 W1 한 곳 제외) |
| 레이아웃: 긴 제목/본문 · 가로 844×390 · 50행 스크롤 · overflow 0 | 캡처 시험 레이아웃 3건 + `layout-*` PNG · 입력칸이 없어 키보드 해당 없음 | PASS |
| 세션 격리: 늦은 401 · 2xx · SSE · 읽음 · 설정 · 푸시가 새 세션 종 · 목록 · 이동 · 토스트를 바꾸지 않음 · 로그아웃 = 종 0 · 스트림 닫음 | `_disposed` 가드(컨트롤러 · 화면 · 설정) · 목록 · 시트 = 세션 Navigator · `app.dart` 세션마다 하나 · ui 시험「늦은 이전 세션」 | PASS |
| 원장 호출 푸시 누름 · 앞 수신 = environment **+ hospitalId** 일치만 · 다른 병원 = 이동 · 읽음 0 | `push_coordinator._hospitalMatches` · 시험(칸 없음 · 병원 다름 거절) | PASS |
| board 없는 활성 직원: 종 · 목록 · 설정 유지 · 행 누름 = 시술현황 자리 권한 없음 안내 · 판 네트워크 0 | `shell._toVisit` · ui 시험 | PASS |
| 이동 카드 없음 = 기존 토스트 | 판 `openVisitRequest` 기존 경로 재사용 | PASS |
| native: 앞 원장 호출 = 시스템 배너 · 소리 그대로 + Dart 로 넘김(종만) · [수락] · Keychain · 기기 등록 · 채팅 앞 배너 무변경 | `AcceptLogic.swift` `PushPayload.callForeground` · `AppDelegate` willPresent diff · native 57 PASS | PASS |
| OS 권한 재확인(앞으로 옴) — 거부 → 설정에서 켬 → 다시 허락되면 원격 등록 | `push_coordinator.onResume` → native `requestPermission` 이 허락이면 `registerForRemoteNotifications`(AppDelegate:67-74) | PASS |
| 채팅 · 시술현황 · 로그인 · 통역 회귀 | 전체 277 passed | PASS |

## WARN

### W1. 설정 탭에서 「알림」 칸이 [로그아웃] 아래에 놓인다 — SPEC 와이어프레임과 차례가 다르다

- 위치: `lib/ui/shell.dart:416-428` 설정 탭 조립 — [로그아웃](:416-421) 뒤에 `NotificationSettingsSection`(:428). 원형 `settings_screen.dart:97-128` 은 계정 → 알림 → … → [로그아웃](:128).
- 근거:
  - SPEC-005 §2 Wireframe(설정 탭) 차례 = 「계정 …」 → 「알림」 → 「[로그아웃]」.
  - 원형 `settings_screen.dart` 도 [로그아웃]이 맨 아래다(pairs `ipad-07-settings` 왼쪽).
  - DAY 캡처(오른쪽)는 계정 카드 안 [로그아웃] → 「알림」이다.
- 영향: 기능 영향 없음. 배치가 원형 · SPEC 와 다르다(새 글자는 없음).
- 최소 정정(앱 워커): 「알림」 칸을 계정 정보와 [로그아웃] 사이에 둔다. 또는 SPEC-003 U-16 계정 카드 모양을 지키는 쪽이 맞으면 코디가 SPEC 차례를 정한다.

## 참고 (결함 아님)

1. **시각 표시는 KST 고정이다.** 알림 「HH:MM」은 `+9h`(`notification_model.dart:79-83` · 원형 그대로)다. 서버 「오늘」은 `HOSPITAL_TIMEZONE`(기본 Asia/Seoul)이라 지금은 같다. 병원 시간대가 바뀌면 둘이 어긋날 수 있다.
2. **native 수락은 병원을 보지 않는다.** 원장 호출 [수락]은 기존 SPEC-003 그대로 environment 만 본다. 다른 병원 호출이 오지 않는 근거는 서버 대상 선정이다(세션 병원 = 호출 병원 기기만). 앱의 이동 · 읽음은 이번에 hospitalId 까지 본다.
3. **브리프 추가 포커스 — 채팅 이벤트 경계(백엔드 · 앱 검수 범위 밖 · 코드 읽기로만 판단):**
   - 채팅 이벤트는 커밋 시점의 지금 멤버(`from_seq < seq`)에게만 만들어 보낸다. 스트림은 보내기 직전에 세션 · 활성 직원만 다시 본다.
   - 그래서 「publish ~ 전달」 몇 ms 사이에 나감 → 재초대가 끝나면, 나가기 전 이미 볼 수 있었던 메시지 이벤트가 새 경계 뒤에 도착할 수는 있다.
   - 이는 받는 순간 권한이 있던 데이터다. 나간 뒤 생긴 메시지 · 수정 · 삭제 이벤트는 그 계정에 만들어지지 않는다. 새 경계 밖 데이터 유출로 보지 않는다.
   - 실제 재현(probe)은 하지 않았다 — 판단 근거는 코드 읽기다. 앱 쪽은 메시지 seq ≤ `fromSeq` 이벤트를 무시하는지 이번 범위에서 보지 않았다.
4. **브리프 추가 포커스 — 서버 선택 비밀 · 디스크 영속:** 이전 backend fix(`chat-backend-fix-report.md`)에서 이미 코드로 닫혔다. `day_vm.py` 선택 비밀 2개(없으면 빠짐 · 금지 키) · Dockerfile `/var/lib/day/chat` · 로컬 named volume 이다. 실 Vault · 배포는 미실행이다.
5. **실물 pending:** 실서버 11040 알림 API 배포 · 실 APNs 키 · Apple Push 서명 · 실기기 수신 · 잠금 화면 [수락] 뒤 종 동기화. 모든 앱 결과는 더블 기준이다.
