# DAY 알림 v8 앱 구현 보고 — task_e7839883b642 / ctx_b014a64d2575

- 계약: DAY-SPEC-005 @ `b0f71ec3`(전문) · 인접 SPEC-003/004/000/001 · 승인 = delivery-v8-plan-approval / v8-approved-result(plan-approved) · request = delivery-request-v8-execution.json
- 원천: cc-prototype `77173cf8` `procedure/app/lib/{widgets/header.dart, screens/notifications_screen.dart, screens/settings_screen.dart, screens/shell.dart, model/notification.dart, app_state.dart, push/push.dart}` — `git show` · `git archive`(스크래치)로만 읽음 · 원본 수정 0
- 작업 tree: CENTURION_DAY/day-app · branch kknaksss/day-app · 시작 head `3aaa9780`(그대로 · commit/push/PR 0) · **app/ 만 변경**(backend dirty = 서버 writer 병렬 작업 — 손대지 않음)
- 결과: **코드 완료 · 검증 PASS** / 실서버 활성(11040 배포) · APNs 실키 · 실기기 수신 pending

## 1. 변경 파일 · sha256 앞 16자(전체 = `notification-mobile-evidence/logs/file-hashes.txt`)

| 파일 | 내용 | hash |
|---|---|---|
| `lib/notify/notification_model.dart` (신규) | §3 모양 — uuid · `target{visitId, callId}` · 모르는 kind(상담사 · chat) 버림 · 설정 이름 「원장 호출」 · 시각 KST `HH:MM` | `8b20ba3e1deda781` |
| `lib/notify/notification_api.dart` (신규) | #1 ~ #4 — 세션 origin · Bearer 만 · 리다이렉트 안 따라감 · `{ids?, callId?}` · 두 칸 없음 = 모두 읽음 · 오류 code | `b8bf414c9c4ce2c7` |
| `lib/notify/notification_controller.dart` (신규) | 종 unread(서버 값만) · 전용 SSE `/api/notifications/stream`(`notification {unread}` 만 · 끊김 줄 없음 · 재연결 = #1) · callId 읽음 · 앞/뒤 · 세션 격리(`_disposed`) · code 글자 | `851ec7cfb7194120` |
| `lib/notify/notification_screen.dart` (신규) | 원형 목록 이식 — [‹ 닫기] · 「알림」 정가운데 · [모두 읽음](안 읽음 있을 때만) · 행(점 · 제목 · HH:MM · 본문 · 안 읽음 바탕) · 「오늘 받은 알림이 없어요」 · 당겨서 새로 고침 · 열린 동안 unread 바뀌면 다시 읽기 · 폰 전체 화면 / 아이패드 오른쪽 420(‹ 없음) — **세션 Navigator** 에 올림 | `cd08981ffb1ac48d` |
| `lib/notify/notification_settings.dart` (신규) | 설정 「알림」 칸 — 원형 `_Section`/`_Row`/SwitchRow · 「알림 꺼짐 · 설정에서 켜기」 · 「받는 알림이 없어요」 · 「알림 설정」 + 글자 · 실패 = 글자 토스트 + 서버 값으로 원래대로 | `943afcf76e11ddd4` |
| `lib/ui/widgets.dart` | `Bell` = 원형 header.dart:107-137(빨간 배지 · 99+ · 0 숨김 · 접근성 「알림 n개 안 읽음」/「알림」 · 누르면 목록) · 셸 밖이면 종만 | `16c31d950a3e5a6b` |
| `lib/ui/shell.dart` | `NotifyScope` · 알림 행/푸시 → 「시술현황」 탭 그 방문(판 없으면 그 자리 권한 없음 안내) · 설정 계정 칸 아래 「알림」 칸 | `42d0cf939524dcc3` |
| `lib/app.dart` | 알림 컨트롤러 = `/me` 200 셸 세션 하나에 하나(채팅과 같은 때 · board/chat 권한 무관) · 로그아웃 · 401 · 병원/계정/환경 바뀜 = dispose(종 0 · 스트림 닫음) · 앞/뒤 · 푸시 콜백 · 테스트용 전송 칸 | `d168861672afa952` |
| `lib/state/push_coordinator.dart` | 원장 호출 누름 = 환경 **+ hospitalId** 일치만 → 그 방문 + `callId` 읽음 · 앞 수신 = 같은 환경 · 병원만 종 다시 · `osDenied`(기존 권한 결과 재사용 · 앞으로 올 때 다시 확인) | `f6d98c4f2a09cad7` |
| `lib/chat/chat_stream.dart` | `path` · `events` 인자(기본값 = 채팅 그대로) — 알림 스트림이 같은 SSE 규칙 재사용 | `bd6a5861acdcd785` |
| `ios/Runner/AcceptLogic.swift` · `AppDelegate.swift` | `PushPayload.callForeground` — 앞 원장 호출은 시스템 배너 · 소리 그대로 + Dart 로도 넘김(종 다시 읽기). 네이티브 [수락] · Keychain · 기기 등록 무변경 | `47def9bf6bb3741c` · `826674afe8fd0fcf` |
| `README.md` | 구조 · 종/목록/설정 구현 · 서버 활성 전제 | `6491aa34bcc8550d` |
| 시험 | `test/notify/notification_contract_test.dart`(7) · `test/ui/notification_ui_test.dart`(14) · `test/capture/notification_capture_test.dart`(장면 12 skip + 레이아웃 3) · `test/support/notify_fake.dart` · fixtures/ui_harness(알림 더블 분리) · `push_coordinator_test`(+1 · 원장 호출 payload 에 hospitalId) · `actions_test` · `app_flow_test`(payload 에 hospitalId) · native +3 | 위 해시 파일 |

## 2. 원형 → 구현 → 검증 매핑

| 원형(77173cf8) | 구현 | 검증 |
|---|---|---|
| widgets/header.dart:107-137 Bell | ui/widgets.dart `Bell` | ui「종 = 서버 unread · 0 숨김 · 99+ · 접근성 · 모든 탭」· PNG 01-03 |
| screens/notifications_screen.dart 전체 | notify/notification_screen.dart | ui 목록 · 행 누름 · 모두 읽음 · 열린 동안 SSE · 아이패드 420 · PNG 04-06 |
| screens/shell.dart:321-336 openNotifications | notification_screen.dart `openNotifications`(세션 Navigator) | ui「폰 전체 화면(탭바 덮음)」·「아이패드 오른쪽 420 · ‹ 없음 · 바깥 닫힘」 |
| screens/settings_screen.dart:102-117 · _Section/_Row | notify/notification_settings.dart(계정 칸 아래) | ui 설정 3건 · PNG 07-08 |
| model/notification.dart | notify/notification_model.dart | contract「모양」 |
| app_state.dart:102-108 · 178-199 · 466-476 unread | notification_controller.dart(전용 스트림 · 다시 읽기 때) | contract 상태 4건 · ui 앞 수신/앞으로 옴 |
| app_state.dart:201-226 알림 누름 · callId 읽음 | push_coordinator.dart + app.dart + shell `_toVisit` | ui「푸시 누름 = callId 읽음 · 다른 병원 무시」· push_coordinator_test |

## 3. 서버 계약 정합(SPEC-005 §3 고정 · 추측 0)

- 경로 · 메서드 · 본문 · 응답 칸 = §3 표 그대로(contract 시험이 고정). 같은 tree 서버 writer 의 진행 중 `backend/day/routers/api/notifications.py` · `services/notifications.py` 를 **읽기만** 해 대조: 4 경로 + `/api/notifications/stream` · 목록 `{unread, items[{id, kind, title, body, createdAt, readAt, target{visitId, callId}}]}` · 읽음 `{ok, read}` · 설정 `{items[{kind, enabled}]}` · `setting_not_allowed` · 원장 호출 푸시 `{aps{alert, sound, category?CALL}, kind, environment, hospitalId, visitId, callId}` — **앱 기대와 차이 없음**(질문 필요 없음).
- 원장 호출 푸시 `hospitalId` 를 필수로 봄(U-4 · §3 본문) — 기존 시험의 hospitalId 없는 payload 3건을 SPEC-005 모양으로 고침(병원 다름 · 칸 없음 = 이동 · 읽음 없음 시험 추가).

## 4. 검증(최종 각 1회 · 로그 `notification-mobile-evidence/logs/`)

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues |
| `fvm flutter test`(전체) | **277 passed · 59 skipped**(캡처 장면) · 실패 0 — 기존 시술현황 · 로그인 · 세션 · 통역 · 채팅 회귀 포함 |
| `sh tool/native_logic_test.sh` | **57 PASS / ALL PASS**(54 + 원장 호출 앞 수신 3) |
| `fvm flutter build ios --release --no-codesign` | 성공 20.6MB |

중간 개발 실행(부분)은 별도 · 시뮬레이터 빌드 · 설치 · 사용자 orca-mobile-iphone(PID 70352) 조작 **0**(브리프: 이번은 fixture · unsigned 만).

검증한 경우(시험 이름 요약): 종 0/1/99+ · 접근성 · 모든 탭 · 채팅은 종에 안 더함 · 목록 폰/아이패드 · 행 누름 ids 읽음(한 번) → 룸 상세 · 읽은 행 = 읽음 요청 없음 · 카드 없음 토스트 · 모두 읽음 = 빈 본문 · 버튼 꺼짐 · 빈 목록 · 열린 동안 SSE → 다시 읽기 · 푸시 누름 callId 읽음 · 다른 병원/칸 없음 거절 · 앞 수신 다시 읽기(같은 병원만) · 앞으로 옴 다시 읽기 · 설정 스위치 PUT · `setting_not_allowed` 토스트 + 원래대로 · OS 거부/허락 · 받는 종류 없음 · board 없는 직원(종 · 목록 · 설정 · 행 누름 = 권한 없음 안내 · 판 네트워크 0) · 로그아웃 = 종 0 · 스트림 닫음 · 늦은 이전 세션 응답 무시 · dispose 뒤 늦은 401/2xx 무시 · 401 세션 끝 한 번 · 네트워크 실패 조용히 · API Bearer/origin/리다이렉트/본문 모양 · 302 거절 · 레이아웃(폰 · 가로 844×390 · 아이패드: 긴 제목/본문 · 50행 스크롤 · 99+ · 당겨서 새로 고침 overflow 0 · [닫기]/[모두 읽음] 누름). 키보드: 알림 화면 · 설정 칸에 입력이 없어 해당 없음.

## 5. 시각 증거 — `notification-mobile-evidence/`

- `day/`(22) · `proto/`(16 — 스크래치 `protoapp/procedure/app/test/zz_notif_capture_test.dart` · 원형 FakeChat override 로 같은 지어낸 값) · `pairs/`(16 — 원형 | DAY · 같은 픽셀 크기)
- viewport 동일: 폰 390×844 · 아이패드 1024×1366 · dpr 2 · 원형 main.dart builder `uiScale` 와 DAY `tabletTextScale` 각자 앱 규칙.
- 장면: 01 종 2 · 02 종 0 · 03 종 99+ · 04 목록(안 읽음/읽음) · 05 모두 읽음 뒤 · 06 빈 목록 · 07 설정 스위치 · 08 설정 OS 거부 + 받는 종류 없음 / 레이아웃 `layout-{phone,land,ipad}-{long,scrolled}`.
- 직접 대조: 목록 머리 · 행(점 · 제목 · 시각 · 본문 · 안 읽음 바탕 · 구분선) · 아이패드 420 시트 · 99+ 배지 위치/모양 · 설정 「알림」 칸(빨간 안내 · 「받는 알림이 없어요」) **같음**. 차이(의도): DAY 주색 · 「DAY」 · 4메뉴 · 설정은 DAY 계정 칸(SPEC-003 U-16) 아래 「알림」 칸만(원형 「이 기기」 · 「앱 정보」 없음 — §1 뺌) · 원형 「서버에 연결 중…」은 원형 판 스트림 줄.

## 6. pending · 사용자 후속

- 서버: 알림 API 4 · 스트림 · 원장 호출 알림 행/푸시 = 서버 writer 진행 중 — 11040 에 배포되기 전엔 종 0 · 목록 「not_found」 코드 글자(정상 동작).
- APNs 키 · Apple Push/서명 · 실기기 수신(N-3) · 실제 앞/뒤 배너 · 잠금 화면 [수락]과 알림 읽음 연동 · 「설정에서 켜기」는 원형대로 글자만(OS 설정 열기 없음 — OQ-N2 기본값).
- 사용자 질문 「개발용 iOS 푸시 받을까」: 앱 쪽은 `DAY_APNS_ENV=sandbox` 빌드 · 기존 기기 등록으로 준비됨 — 실제 수신은 APNs 키(서버 Key Vault) · Push capability 서명 · 실기기 설치가 사용자 몫.
