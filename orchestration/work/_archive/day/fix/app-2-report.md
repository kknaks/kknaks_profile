# WP-APP-2 채팅 · 설정 — 결과 보고

## 상태: done (미커밋 · `app/` 만 · 서버 BE-1 은 계약 표 + 테스트 더블로 — 실물 로컬 확인은 pending)

근거 스펙: mediness `fix-spec` 미커밋 SPEC-004 2026-11-11 개정 ① ② ③(U-1 「채팅 거절」 · U-7 「그룹 이름 바꾸기」 · U-8 「채팅 전체 알림 끔」 · 케이스 매트릭스 · OQ-C11 ~ C15 · C-A19 ~ C-A21) · SPEC-005 2026-11-11 개정(U-3 「채팅」 스위치 · S-5 · N-A13) · wp-plan §3 계약 표.

## 수행 — 변경 파일 (새 파일 없음)

| 파일 | 무엇 |
|---|---|
| `app/lib/chat/chat_state.dart` | `denied`(채팅 거절) — 403 = 메모리 비움(`clear`) · 스트림 멈춤 · 상태 idle · **토스트 없음**(조작 중 403 포함 — `_handleError`) · 세션은 그대로 · 다시 보는 때 = 새 세션(다시 로그인 · 앱 다시 열기 = 새 ChatState) + **앱이 앞으로 올 때 한 번**(`setForeground(true)` → `_recheck` = 목록 → 되면 스트림) · 거절 중 배너 없음 · `chatAlerts`(채팅 전체 알림) false 면 배너 없음(방별 `muted` 그대로) · `rename()`(#22 — 성공 Room 으로 갱신 · 404 = 「대화방을 찾을 수 없어요」 + 목록에서 뺌 · 403 = 거절 · 그 밖 4xx = code 글자 · 네트워크/5xx = 조용히) |
| `app/lib/chat/chat_api.dart` | `rename(roomId, title)` = `PUT /api/chat/rooms/{id}/title` `{title: string \| null}` |
| `app/lib/chat/chat_copy.dart` | `ChatOp.rename` · #22 의 `chat_group_only` = 코드만(스펙: 이 경로에서 화면 글자를 정하지 않음) |
| `app/lib/chat/chat_kit.dart` | `ChatConnectionLine` — 거절 상태면 줄 없음(「서버에 연결 중…」이 남지 않음) |
| `app/lib/chat/screens/chat_info_screen.dart` | `GroupTitleCard` — 그룹만 · 누르면 편집 · 이름표 「그룹 이름」 · 힌트 「비우면 참여자 이름으로 보여요」 · 40자(`RuneLimitFormatter(40)`) · [✕] 「수정 취소」 · [✓] 「저장」(같은 값 · 보내는 중 꺼짐) · 성공 토스트 없음 · 실패면 입력 그대로 · 404 면 아이패드 시트 닫음 |
| `app/lib/ui/shell.dart` | `BoardForbiddenBody` → `ForbiddenBody`(이름만 · 글자 · [로그아웃] 그대로 · 글자 키 인자) · 채팅 탭 본문 = 거절이면 `ForbiddenBody`(키 `chat-forbidden`) · 거절되면 채팅 탭 스택을 목록까지 닫고(채팅 탭이 지금이면 세션 Navigator 위 채팅 창 · 시트도) |
| `app/lib/notify/notification_model.dart` | `notifKindName['chat'] = menuChat`(「채팅」) · `chatAlertsOf(settings)`(없으면 켜짐) |
| `app/lib/notify/notification_controller.dart` | `chatAlerts` 값 · `refreshSettings()`(start = 로그인 · 자동 로그인 뒤 · 앞으로 올 때) · `applySettings()` |
| `app/lib/notify/notification_settings.dart` | 설정 읽기(바꾼 뒤 다시 읽기 포함) 결과를 `applySettings` 로 넘김 — 줄 차례 = 서버 `items` 차례 그대로 |
| `app/lib/app.dart` | `ChatState(chatAlerts: notify.chatAlerts)` — 같은 세션의 알림 상태 값 |
| 시험 | `test/support/chat_fake.dart`(#22 경로 · `forbidden` 스위치) · `chat/chat_state_test.dart` · `chat/chat_contract_test.dart` · `notify/notification_contract_test.dart` · `ui/chat_ui_test.dart` · `ui/notification_ui_test.dart` · `capture/chat_capture_test.dart` · `capture/notification_capture_test.dart` |

`chat_stream.dart` 는 고치지 않았다 — 이미 403 이면 `_running=false` 로 다시 붙지 않고 `onSessionEnd('forbidden')` 한 번(연결 실패 · 끊김은 재시도) — 시험으로 고정. `chat_list_screen.dart` · `push_coordinator.dart` 도 고치지 않았다(아래 「계획과 다른 곳」).

## 수용 항목 ↔ 시험

| 항목 | 시험 |
|---|---|
| C-A19 403 = 본문 안내 · 연결 중/로딩 없음 · 재연결 0 · 메모리 비움 · 세션 · 시술현황 그대로 · 토스트 0 | `chat_ui_test` 「채팅 거절 403 …」 폰 · 아이패드 2건(글자 · [로그아웃] · 「서버에 연결 중…」 0 · 로딩 0 · 토스트 0 · 탭 배지 0 · 40초 뒤에도 연결 1 · 세션 묶음 · 시술현황 카드 · [로그아웃] → 로그인) · `chat_state_test` 「스트림 403 = 재연결 0 · idle · 메모리 · 배지 비움 · 토스트 0 · 세션 그대로」 · `chat_contract_test` 「403 forbidden = 거절로 끝 … 다시 붙지 않음」 · 기존 「401 … · 403 forbidden = 목록 비움 · 거절 상태 · 토스트 없음」(기대 갱신) |
| C-A19 조작 중 403 · 다시 보는 때 | `chat_state_test` 「조작 중 403(보내기 · 이름 바꾸기) = 같은 거절 상태 · 토스트 0」 · 「다시 보는 때 = 앱이 앞으로 올 때 한 번 …」 · `chat_ui_test` 「대화 중 403(보내기) = 열린 대화를 닫고 같은 안내 · 토스트 0 · 앱이 앞으로 올 때 한 번 다시 읽어 풀리면 목록」 |
| C-A20 (앱) 그룹 이름 | `chat_contract_test` 「#22 그룹 이름 — PUT … 본문 {title} 만 · 응답 Room」 · 「#22 가짜 서버 계약 — 1:1 · 41자 · 404 · 같은 이름」 · `chat_state_test` group 「그룹 이름 바꾸기」 4건(공백 뺌 · 순서 · 안 읽음 · 줄 0 · 토스트 0 / 빈 값 null / 404 · 400 · 네트워크 / `chat_room` 이벤트) · `chat_ui_test` group 「그룹 이름 바꾸기」 4건(✓ 꺼짐 · 공백 비교 · PUT · 40자 · ✕ 요청 없음 / 이벤트 반영 / 1:1 줄 없음 · 404 → 목록 / 아이패드 시트) |
| C-A21 (앱 — 배너) · N-A13 (앱) | `chat_state_test` 「chatAlerts false = 모든 방 배너 0 · 방별 muted 그대로 · 다시 켜면 방별대로 · 안 읽음은 셈」 · 「chatAlerts 를 주지 않으면 켜짐」 · `notification_contract_test` 「설정 — chat = 「채팅」 줄 · 차례 · chat 없으면 켜짐」 · 「start 에 읽음 · 앞으로 올 때 다시 · 읽기 실패 = 마지막 값 · PUT {kind: chat, enabled}」(두 기기 = 다른 기기는 다음 앞으로 올 때부터) · `notification_ui_test` 「설정 「채팅」 스위치 …」 · 「설정 응답에 chat 이 없으면 「채팅」 줄 없음 · 배너는 켜짐」 |
| N-A10 | (기존 · 바뀜 없음 — 설정 칸 받는 종류만 · 기존 시험 통과) |

## 새 화면 글자

**새 문자열 상수 0.** 쓰인 글자는 전부 기존 상수 · 기존 글자 재사용:

| 글자 | 코드 자리 | 스펙 줄 |
|---|---|---|
| 「이 화면을 볼 권한이 없습니다. 관리자에게 문의해 주세요」 · [로그아웃] | `shell.dart` `ForbiddenBody`(기존 `forbiddenMessage` · 기존 버튼) | SPEC-004 U-1 「채팅 거절」 · OQ-C15 |
| 「그룹 이름」 · 「비우면 참여자 이름으로 보여요」 | `chat_info_screen.dart` `GroupTitleCard`(새 대화 `chat_new_screen.dart:133-135` 와 같은 글자) | SPEC-004 U-7 「입력」 |
| 「저장」 · 「수정 취소」(아이콘 접근성 이름) | `GroupTitleCard`(`chat_room_screen.dart` 수정 모드와 같은 아이콘 `check_rounded` · `close_rounded`) | SPEC-004 U-7 「저장 · 취소」 · OQ-C11 (가) |
| 「대화방을 찾을 수 없어요」 | `chatErrorText('chat_room_not_found')` | SPEC-004 §3 오류 표 |
| 「채팅」(설정 줄) | `notifKindName['chat'] = menuChat`(기존 메뉴 상수) | SPEC-005 U-3 |

## 계약 대조 (wp-plan §3 ↔ 앱)

| 무엇 | 앱이 보냄 | 앱이 읽음 | 같나 |
|---|---|---|---|
| #22 | `PUT {origin}/api/chat/rooms/{roomId}/title` · `Authorization: Bearer` · 리다이렉트 안 따라감 · 본문 `{"title": string\|null}` 한 칸(앞뒤 공백 뺌 · 비면 null) | 200 `Room`(기존 `Room.fromJson` — id · kind · title · name · members · memberCount · muted · unread · lastMessage · lastMessageAt · createdAt · fromSeq · lastReadSeq) · 오류 `{detail, code, field}` → `code` 만(`detail` 안 보임) | 같음 · backend 워커 진행 중 diff(`routers/api/chat.py` `PUT /rooms/{room_id}/title` · `TitleRequest.title: str \| None`)도 같은 모양(읽기만 함) |
| 이름 바뀜 | — | SSE `chat_room` `{room}` → 기존 `_upsert`(목록 · 대화 머리 · 방 정보) | 같음 · 새 이벤트 없음 |
| 설정 읽기 | `GET /api/me/notification-settings` | `items[].kind · enabled` · 차례 그대로 · `chat` 없으면 켜짐 · 모르는 kind 버림 | 같음 · backend diff 의 받는 종류 `doctor_call` → `chat` 과 같음 |
| 설정 쓰기 | `PUT /api/me/notification-settings` `{"kind": "chat", "enabled": bool}` | `{items}` → 다시 읽기 · 400 `setting_not_allowed` = 기존 글자 토스트 | 같음 |
| 채팅 403 | — | 모든 채팅 HTTP · 스트림 403 `forbidden` → 거절 안내 | 같음 |
| 채팅 푸시 | (서버) | 앞에서 받은 채팅 푸시 → 같은 배너 길(`offerBanner`) → `chatAlerts` false 면 없음 | 같음 |

## 명령 · 수치

- `cd app && fvm flutter analyze` → No issues found
- WP 시험: `fvm flutter test test/chat/chat_state_test.dart` → +35 · `test/chat/chat_contract_test.dart test/notify/notification_contract_test.dart` → +23 · `test/ui/chat_ui_test.dart test/ui/notification_ui_test.dart` → +34 — 모두 통과
- **전체** `fvm flutter test` → **+314 ~67(skip = 캡처 · 평소 skip) All tests passed**
- `fvm flutter build ios --no-codesign` → ✓ Built `build/ios/iphoneos/Runner.app` (20.7MB) · Xcode 29.9s (서명 · 아카이브 · 업로드 없음)

## 캡처 (`work/fix/app-captures/` — 가짜 값만)

| 파일 | 장면 |
|---|---|
| `phone-board-all-done-need-overlap.png` · `ipad-…` | (APP-1) 모두 완료 + [귀가 대기] · 확인 필요 겹침 7자리 |
| `phone-board-need-overlap-filtered.png` · `ipad-…` | (APP-1) 「확인 필요」 칩 |
| `phone-fix-chat-forbidden.png` · `ipad-…` | 채팅 403 안내 |
| `phone-fix-group-title-edit.png` · `ipad-…` | 방 정보 그룹 이름 편집([✕] · [✓]) |
| `phone-fix-group-title-saved.png` · `ipad-…` | 바꾼 뒤 |
| `phone-fix-settings-chat-switch.png` · `ipad-…` | 설정 「알림」 원장 호출 + 채팅 |

## 스펙 · 계획과 다른 곳 · 물을 것

1. **거절 안내 위치** — 계획은 `chat_list_screen.dart` 본문에서 바꾸라 했지만, 셸(`shell.dart` `_root`)에서 채팅 탭 본문을 `ForbiddenBody` 로 바꿨다. 시술현황 권한 없음과 같은 자리 · 같은 위젯이고, 열린 대화(폰 스택) · 아이패드 오른쪽 칸이 함께 사라져 「열린 대화 · 방 정보는 닫는다」를 한 곳에서 지킨다. 화면 결과는 스펙과 같다.
2. **`push_coordinator.dart` 무변경** — 설정 다시 읽기를 `NotificationController`(세션마다 새로 만듦 = 로그인 · 자동 로그인 뒤 `start` · `setForeground(true)`)에 붙였다. 계획이 적은 「이미 있는 갱신 자리」가 거기다. `push_coordinator_test` 도 그대로 통과.
3. **그룹 이름 줄 누름 표시** — 보기 상태 줄은 카드 전체를 누르면 편집(와이어 「누르면 바꾸기」). 연필 아이콘 등 표시는 넣지 않았다(스펙에 없음). 눌러 바꿀 수 있다는 게 안 보인다고 하면 사용자 결정.
4. **이름 바꾸기 네트워크 실패 · 5xx** — 스펙 「입력 그대로 두고 다시 저장 가능」 그대로 · 토스트 없음(원천 글자 없음). 코드만 토스트를 원하면 한 줄.
5. **40자 막기** — 입력에서 40자(코드포인트)까지만 받는다. 앞뒤 공백도 40자 안에 센다(서버는 공백을 뺀 뒤 셈 — 앱이 더 엄격 · 실사용 영향 없음).
6. 거절 상태에서 앞에서 받은 채팅 푸시 배너도 띄우지 않는다(채팅 탭이 안내 화면 — U-8 「채팅 403 이면 어차피 안내」).

## pending

- **로컬 day-local 실물 확인**(wp-plan §4 「BE-1 끝난 뒤 C-A20 · C-A21」) — 이번 발주는 로컬 스택 · 포트 금지라 하지 않았다. 앱은 계약 표 + 더블로만 검증.
- 실기기(두 기기 · TestFlight 빌드 2 이상) — 사용자(wp-plan §7 #2 ~ #4).
