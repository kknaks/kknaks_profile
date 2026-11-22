# day-mobile-v2 M3 결과 보고 — 앱 호출 취소 알림(doctor_call_cancel) · 푸시 누르기 · 원래 푸시 지우기(iOS)

## 상태: done (커밋 · push · PR 없음 · 실기기 APNs 확인 pending · Android FCM 은 범위 밖)

base = `9162ee18`(서버 P3) 위. `backend/**` 변경(fcm 등)은 backend F1 몫 — 내 것 아님.

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `app/lib/notify/notification_model.dart` | `notifKinds` 에 `doctor_call_cancel` · `callPushKinds = {doctor_call, doctor_call_cancel}` · 설정 줄은 그대로(새 줄 없음) |
| `app/lib/state/push_coordinator.dart` | 푸시 누름 · 앞 수신 판정을 `callPushKinds` 로 — 호출 취소도 환경 · 병원 확인 뒤 그 방문 룸 상세 + `callId` 읽음 · 앞 수신 = 종 다시 읽기 |
| `app/ios/Runner/AcceptLogic.swift` | `PushPayload.callForeground` 가 호출 취소도 Dart 로 · 순수 함수 `cancelledCallIds` · `callsToClear`(지울 원래 원장 호출 푸시 고르기) |
| `app/ios/Runner/AppDelegate.swift` | `clearCancelledCalls` — 알림 센터의 호출 취소 푸시(+ 방금 받은 것)의 `callId` 와 같은 `doctor_call` 푸시를 `removeDeliveredNotifications` · 부르는 때 = 앞에서 받음(`willPresent`) · 누름(`didReceive`) · 앱이 앞으로 옴(`didBecomeActive`) |
| `app/test/notify/call_cancel_test.dart`(새 · 6) | 모델 · 설정 · 목록 행 · 종 배지 · 행 누름 · 푸시 누름(환경 · 병원 격리 · 카드 없음 토스트) · 앞 수신 |
| `app/ios/NativeLogicTests/main.swift` | 네이티브 판단 시험 6건 추가 — **allowed_paths(`app/ios/Runner/` · `app/test/`) 밖이지만 기존 네이티브 시험 파일**(`tool/native_logic_test.sh` 가 컴파일) · 코디 확인 바람 |

## 동작 — 스펙 대조(DAY-SPEC-005 2026-11-20 · DAY-SPEC-003 §3 「호출 취소 푸시」)

| 항목 | 앱 |
|---|---|
| 목록 · 종 배지 | 원장 호출 행과 같은 모양(점 · 제목 · HH:MM · 본문 · 안 읽음 바탕) · **제목 · 본문 = 서버 행 그대로**(「호출 취소」 · 「{방} · 호출 취소」 — 앱이 짓지 않음) · 종 = 서버 `unread`(종류 안 거름) |
| 설정 | 새 줄 없음 — 서버가 「원장 호출」 스위치를 따름(OQ-N18). 서버가 `doctor_call_cancel` 설정 줄을 보내도 그리지 않음 |
| 행 누름 | 원장 호출과 같음 — `ids` 읽음 → 그 방문 룸 상세 · 카드 없으면 기존 토스트 |
| 푸시 누름 | 원장 호출과 같음 — 환경 · 병원이 같을 때만 그 방문 룸 상세 + `POST /api/notifications/read {callId}`(그 호출의 행 읽음) · 카드 없으면 「호출이 끝났거나 방이 비었어요」 · **[수락] 액션 없음**(서버가 카테고리를 안 실음 · 앱은 `CALL` 카테고리에만 액션) |
| 앞에서 받음 | 시스템 배너 · 소리 그대로 + Dart 종 다시 읽기 + 원래 원장 호출 푸시 지움 |
| 원래 푸시 지우기(OQ-N17 ②) | `callId` 같은 `kind = doctor_call` 알림만 지움 · 호출 취소 푸시 자체 · 다른 호출 · 채팅은 남김 |

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+409 ~79 All tests passed**(M2 뒤 403 → 409 · 새 6) |
| `fvm flutter build ios --no-codesign` | ✓ Built `Runner.app` (20.8MB) — 바뀐 Swift 포함 컴파일 |
| `sh app/tool/native_logic_test.sh` | ALL PASS(새 6건: 앞 수신 Dart 넘김 · 누름 칸 · 취소 callId 모으기 · 그 호출 원장 호출 푸시만 지움 · 취소 없으면 0 · 방금 받은 callId) |

실기기 APNs 수신 · 알림 센터 지우기 실물 = **pending(A-50 · 사용자 실기기)** — 시뮬레이터 · 기기 무접촉.

## 이슈 · 코디가 확인할 것
1. **뒤에 있을 때(백그라운드 · 꺼짐) 받은 호출 취소는 그 순간 원래 푸시를 못 지운다** — 서버 본문은 일반 alert(`content-available` · `mutable-content` 없음)라 iOS 가 앱을 깨우지 않는다. 그래서 원래 원장 호출 푸시는 **앱이 앞으로 올 때 · 취소(또는 아무) 알림을 누를 때** 지워진다(그 사이 잠금 화면엔 둘 다 보임). 받는 즉시 지우려면 셋 중 하나가 필요: ⓐ 서버가 두 푸시에 같은 `apns-collapse-id`(= callId)를 실어 취소가 원래 것을 **대체**(서버 변경 · 가장 단순 · 원래 알림이 「호출 취소」로 바뀜) ⓑ Notification Service Extension(새 타깃 · `mutable-content: 1` · 서버 + Xcode 프로젝트 변경) ⓒ `content-available` 조용한 푸시(전달 보장 없음). 이번 범위(앱 · `ios/Runner/` 만)에서는 고르지 않음 — 사용자 · 코디 판단.
2. 호출 취소 푸시를 누르면 `{callId}` 읽음이라 그 호출의 원래 원장 호출 행도 같이 읽음(서버가 이미 닫았으므로 차이 없음).
3. `app/ios/NativeLogicTests/main.swift` 수정은 allowed_paths 밖(기존 네이티브 시험 파일).
4. 워크트리 `backend/**` F1 변경은 내 것 아님.
