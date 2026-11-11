# 리뷰 리포트 — fix 앱 수정 3 재확인: 길게 누르기 메뉴(W1 · R1 · R2) / code (2026-11-11)

대상: `CENTURION_DAY/fix` `app/` — 앞 검수(`review-app-3-report.md`) 뒤 바뀐 것 = `lib/chat/screens/chat_room_screen.dart` · `test/ui/chat_ui_test.dart`. 근거: SPEC-004 U-4 `:202` · C-A22. read-only.

## 판정: PASS

W1 · R1 · R2 모두 풀렸다. 내가 센 계기에서 빠진 것은 없다. 무한 고리 · 목록 전체 다시 그리기 · dispose 뒤 콜백도 없다. 새 화면 글자 0 · 범위 2 파일.
참고 3건(작음 · 막지 않음).

## 항목별

| # | 결과 | 자리 |
|---|---|---|
| W1 | 풀림 | `chat_room_screen.dart` `_menu` → `_FollowBubble(triggers: [_chat, _scroll, _chat.streamStatus])` · `_triggers.addListener(_afterLayout)`(initState) · **메시지 id 로 지금 그 말풍선을 그리는 element 를 찾음**(`:314-341` `_bubbles` · `_bubbleMsg` Expando · `_liveBubble`). 작성자가 더 찾은 원인 — `ListView.builder` 가 element 를 다시 써서, 누른 순간의 context 가 새 메시지가 끼면 **다른 메시지**를 그림 — 은 맞다. `_bubbleMsg[c] != id` 로 걸러진다 |
| R1 | 풀림 | `gone: _chat.changes.stream.where(kind == 'deleted' && messageId == m.id)`(`changes` 는 broadcast — `chat_state.dart:199` · 두 번째 구독 안전) → `_closing = true` · 미리 잡아 둔 `NavigatorState.maybePop()`. 다른 메시지 삭제 = `messageId` 가 달라 그대로(시험 있음). 닫히는 0.12초 동안 `_closing` 이라 다시 재지 않는다 |
| R1 하위 창 | 고아 없음 | [선택 복사] · [전달] · [삭제 확인] · [수정]은 모두 메뉴가 **닫혀** `pick` 을 돌려준 **뒤** 열린다(`_menu` 끝 `switch`). 메뉴가 떠 있는 동안 그 위에 하위 창이 없으므로 `maybePop` 은 메뉴 자신을 닫는다. 하위 창이 열린 뒤 그 메시지가 지워지는 경우(삭제 확인 창이 남음 등)는 앞 판부터 있던 동작이고, 이번 범위 밖이다 |
| R2 | 풀림 | `_queued` — 대기 중이면 새로 걸지 않아 체인이 늘 하나다. `ensureVisualUpdate` 는 계기만 오고 프레임이 없을 때 한 번 |
| 무한 고리 | 없음 | 체인은 「잰 rect 가 바뀌었을 때만」 다음 프레임에 다시 걸린다. 같아지면 멈춘다. `setState` 는 `_FollowBubble`(메뉴 막)만 다시 그리고 대화 목록은 건드리지 않는다. 복사본의 `ListenableBuilder(_chat)` 은 `_chat` 알림 때만 다시 그려진다 |
| dispose | 안전 | post-frame 첫 줄 `if (!mounted \|\| _closing) return` · `dispose` 에서 observer · `_triggers` 리스너 · `_gone` 구독을 해제한다 |
| 새 글자 · 범위 | 0 · 2 파일 | `git diff -- app/lib` `+` 줄 한글 리터럴 = 앞 판과 같은 12개 · `app/lib/interpret` · `pubspec` 무변경 |
| 시험 | 실패할 수 있음 | W1 시험은 「말풍선이 실제로 밀렸는지 먼저 확인」한 뒤 복사본 rect = 말풍선 rect 를 본다(리스너를 끄면 실패한다는 작성자 확인과 구조가 맞음). R1 시험은 「다른 메시지 지움 = 그대로 → 그 메시지 지움 = 메뉴 없음」 대조가 한 시험 안에 있다 |

## 내가 센 계기 — 말풍선 자리를 바꿀 수 있는 것

| 계기 | 잡는 길 | 확인 |
|---|---|---|
| 키보드 높이 · 화면 크기 · 회전 · 분할 | `didChangeMetrics` | ✓ |
| 글자 크기 | `didChangeTextScaleFactor` | ✓ |
| 새 메시지(실시간 · 보낸 응답 · 전달) | `_chat`(`_onMessage` 끝 `_notify` · `chat_state.dart:706`) | ✓ |
| 지워짐(자리 높이 바뀜) | `_chat`(`_onDeleted`) — 그 메시지면 R1 로 닫힘 | ✓ |
| 수정됨(길이 · 「수정됨」) | `_chat` | ✓ |
| 읽음 숫자 생김 · 사라짐 | `_chat`(`chat_member_read` · `chat_read` · `_senderRead` 뒤 `_notify`) | ✓ |
| 위로 더 · 처음 50 · since · 다시 읽기 | `_chat` | ✓ |
| 보내는 중 · 실패 · 묶음 줄 · 진행률 | `_chat` | ✓ |
| 방 바뀜 · 빠짐 | `_chat`(빠지면 대화 닫힘) | ✓ |
| 목록 스크롤 | `_scroll` | ✓ |
| 연결 줄 생김 · 사라짐 | `_chat.streamStatus`(`_notify` 밖 ValueNotifier) | ✓ |
| 채팅 거절 | 셸이 대화 · 창을 닫음(수정 1) | ✓ |

**12종 — 작성자 표와 같다.** 따로 본 것: 사진 바이트 늦게 옴 = `_photoSize` 로 크기가 미리 정해져 자리 불변 · 입력줄 = 막이 떠 있는 동안 바뀌지 않음(키보드는 metrics). 빠진 계기 0.

## 참고

- R1'. `_bubbles`(`:314`)는 메시지 id → context 를 지우지 않고 쌓는다. 화면 밖으로 나가 떨어진 element 도 대화 화면이 닫힐 때까지 참조로 남는다. 아주 긴 대화를 오래 스크롤하면 메모리가 조금 늘고, 화면을 닫으면 사라진다. 고칠 방향: `_liveBubble` 에서 null 이면 그 키 삭제, 또는 `Builder` 대신 `State.dispose` 에서 지움.
- R2'. `_nav?.maybePop()` 은 그 Navigator(세션 Navigator) **맨 위** route 를 닫는다. 메뉴가 떠 있는 동안 세션 Navigator 에 다른 route 가 올라올 수 있는 길(예: 배너 [보기]가 막 위에서 눌림)이 있다면 그 route 가 닫힌다. 막(barrier)이 화면을 덮어 실제로는 거의 없다. 고칠 방향: `Navigator.removeRoute(ModalRoute.of(context)!)` 또는 `route.isCurrent` 확인 뒤 pop.
- R3'. 하위 창(삭제 확인 · 수정 모드)이 열린 뒤 그 메시지가 지워지는 경우 — 앞 판부터 있던 동작(확인 → 서버 오류 글자). 이번 범위 밖.

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd app && fvm flutter analyze` | No issues found! |
| `cd app && fvm flutter test` | **+343 ~73 All tests passed!** · exit 0(앞 판 +341 → +2) |
