# fix 앱 수정 3 — 리뷰 W1 + R1 · R2 (길게 누르기 메뉴) 결과 보고

## 상태: done (미커밋 · `app/lib` · `app/test` 만 · 새 화면 글자 0 · R3 · R4 · R5 손대지 않음)

근거: `review-app-3-report.md` W1 · R1 · R2 · SPEC-004 U-4 「자리가 맞아야 한다」 · C-A22.

## 항목별 고친 자리 (`app/lib/chat/screens/chat_room_screen.dart`)

| # | 자리 | 무엇 |
|---|---|---|
| W1 | `:486-491` `_menu` → `_FollowBubble(bubble: …, triggers: [_chat, _scroll, _chat.streamStatus], gone: …)` | 다시 재는 계기를 화면 크기 · 키보드에서 **말풍선 자리를 바꿀 수 있는 것 전부**로 넓힘(아래 표) |
| W1(찾은 원인 하나 더) | `:314-341` `_bubbles` · `_bubbleMsg`(Expando) · `_liveBubble(id)` · `:486` `bubble: () => _liveBubble(m.id)` | **누른 순간의 element 를 쥐고 재면 틀린다**: 대화 목록은 `ListView.builder` 가 줄 번호로 element 를 다시 쓰므로, 새 메시지가 0번에 끼면 그 element 가 **다른 메시지**를 그린다(시험에서 복사본이 다른 말풍선 자리 · 높이 40 으로 감 — 확인함). 그래서 메시지 id → 지금 그 메시지를 그리는 element 로 찾아 잰다(다른 메시지를 그리게 된 element 는 버림) |
| R1 | `:491` `gone: _chat.changes.stream.where(kind == 'deleted' && messageId == m.id)` · `:1027-1031` 구독 → `_closing = true` · 저장해 둔 `NavigatorState.maybePop()` · `:1050-1055` 닫는 중엔 더 재지 않음 | 그 메시지가 지워지면 메뉴 닫힘(다른 메시지가 지워지면 그대로) · 닫히는 0.12초 동안 줄어든 「삭제된 메시지」 자리에 옛 복사본을 끼우지 않음(시험에서 overflow 로 확인 → 막음) · 화면 밖으로 밀려 잴 수 없을 때 = 마지막 자리 그대로(바꾸지 않음) |
| R2 | `:1001` `_queued` · `:1050-1066` `_afterLayout` | 재기 체인 늘 하나(대기 중이면 새로 걸지 않음) · 계기만 오고 그릴 프레임이 없을 때 대비 `ensureVisualUpdate` |
| (같이) | `:1048` `didChangeTextScaleFactor` | 글자 크기 바뀜도 계기 |

## 다시 재는 계기 전수 (코드에서 센 것)

말풍선 자리 = 대화 칸(`Expanded` · 머리 · 연결 줄 · 입력줄 사이) 안 `reverse` 목록의 자리. 그 자리를 바꾸는 것:

| # | 계기 | 어디서 오나(코드) | 잡는 길 |
|---|---|---|---|
| 1 | 키보드 높이 · 화면 크기(회전 · 분할) | 셸 Scaffold 의 `viewInsets` | `didChangeMetrics` |
| 2 | 글자 크기(접근성) | 플랫폼 | `didChangeTextScaleFactor` |
| 3 | 새 메시지(실시간 · 보낸 응답 · 전달 결과) | `ChatState._onMessage` → `_notify` | `_chat` |
| 4 | 메시지 지워짐(높이 바뀜) | `_onDeleted` → `_notify` | `_chat` (그 메시지면 R1 로 닫힘) |
| 5 | 메시지 수정됨(글 길이 · 「수정됨」) | `_onEdited` · `edit` → `_notify` | `_chat` |
| 6 | 읽음 숫자 생김 · 사라짐(시각 칸 높이) | `chat_member_read` · `chat_read` · `_markRead` · 메시지 받음(보낸 사람 읽음) · 방 갱신 → `_notify` | `_chat` |
| 7 | 위로 더 불러옴 · 처음 50 · since 메우기 · 다시 읽기(목록 교체) | `loadOlder` · `loadLatest` · `catchUp` · `refreshRooms` → `_notify` | `_chat` |
| 8 | 보내는 중 · 실패 말풍선 · 「N개 보내는 중」 줄 · 진행률 | `sendText` · `sendMany` · `_deliver` · `_drop` · `batches` → `_notify` | `_chat` |
| 9 | 방 바뀜(`chat_room` — 이름 · 인원 · 머리) · 방 빠짐 | `onEvent('chat_room')` · `_remove` → `_notify` | `_chat`(방이 빠지면 대화 화면이 닫힘) |
| 10 | 목록 스크롤(새 메시지 따라 내림 · 위로 더 · 자리 지킴) | 대화 `_scroll`(ScrollController) | `_scroll` |
| 11 | 연결 줄 생김 · 사라짐(머리 아래 노란 줄 = 대화 칸 높이) | `ChatState.streamStatus`(ValueNotifier — `_notify` 밖) | `_chat.streamStatus` |
| 12 | 채팅 거절(403) | `denied` | 셸이 채팅 창 · 대화를 닫음(수정 1) — 메뉴도 세션 Navigator 에서 같이 닫힘 · 따로 잴 것 없음 |

`ChatState._notify()` 부르는 자리 31곳은 3 ~ 9 에 모두 들어간다(`ChatState` 가 `ChangeNotifier` 하나라 한 구독으로 잡힘). 사진 바이트가 늦게 와도 말풍선 크기는 `width · height` 로 미리 정해져(`_photoSize`) 자리를 바꾸지 않는다 — 계기 아님. 입력줄 높이는 메뉴가 떠 있는 동안 막(장벽) 때문에 바뀌지 않는다(입력 · 키보드 = 1 로 잡힘).

## 시험 (`test/ui/chat_ui_test.dart` group 「길게 누르기 자리 …」)

| 이름 | 항목 |
|---|---|
| 「메뉴를 연 채 새 메시지(chat_message)가 와서 목록이 밀려도 복사본 = 말풍선 자리 · 메뉴 화면 안(리뷰 W1)」 | W1 — 말풍선이 실제로 밀렸는지 먼저 확인 · 복사본 rect = 말풍선 rect · 메뉴 화면 안 |
| 「메뉴를 띄운 메시지가 지워지면(chat_message_deleted) 메뉴가 닫힘(리뷰 R1) · 다른 메시지가 지워지면 그대로」 | R1 — 다른 메시지 지움 = 메뉴 그대로 · 그 메시지 지움 = 메뉴 · 복사본 없음 · 대화 그대로 · overflow 0 |
| 기존 키보드 갈래 6건 | 그대로 통과 |

**실패할 수 있는가**: `_triggers.addListener(_afterLayout)` 을 끄고 돌리면 W1 시험 **실패**(+0 −1) → 되돌림. 또 누른 순간 element 를 쥐던 앞 방식에서는 W1 시험이 「다른 메시지 자리(높이 40)」로 실패했다(원인 확인 뒤 메시지 id 로 찾게 고침).

## 명령 · 수치

- `cd app && fvm flutter analyze` → No issues found
- 고친 시험: `fvm flutter test test/ui/chat_ui_test.dart` → +33 통과
- 전체 `fvm flutter test` → **+343 ~73 All tests passed**(skip 73 = 캡처 · 앞 판 캡처 장면 6 이 skip 수에 더해짐)

## 비고

- 바꾼 파일: `app/lib/chat/screens/chat_room_screen.dart` · `app/test/ui/chat_ui_test.dart` 2개뿐.
- 메시지 id 로 element 를 찾는 표(`_bubbles`)는 그 대화 화면 안에만 있고 화면이 닫히면 같이 사라진다(지운 · 밀려난 메시지는 `mounted` · 메시지 id 확인으로 걸러짐).
