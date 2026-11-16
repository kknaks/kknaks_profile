# 리뷰 리포트 — fix 앱 검수 3: WP-APP-3 채팅 화면(8 · 9 · 10 + 정정 1 · 2) / code (2026-11-11)

대상: `CENTURION_DAY/fix`(브랜치 `kknaksss/fix-app-re1`) `app/` — 앞 앱 검수(수정 1 재확인) 뒤 바뀐 것: `chat_room_screen.dart` · `shell.dart` · `chat_model.dart` · `chat_stream.dart` · `chat_state.dart` · `chat_info/media/new_screen.dart` + 시험. read-only.
SoT: SPEC-004 개정 ④ + 정정 1 · 2(`:183-188` 읽음 표시 · `:202` 자리가 맞아야 · `:438` `chat_member_read` · C-A16 · C-A22 ~ C-A25) · 서버 `queries/chat.py` `room_views` · `services/chat.py` `read`(앞 서버 검수 PASS).

## 판정: WARN

FAIL 0 · WARN 1 · 참고 5.
- 9(탭 숨김) · 10(읽음 셈) · 정정 1 · 2 · 서버 계약 · 새 글자 0 은 스펙과 같다.
- 8(길게 누르기 자리)은 버그 그림의 원인(키보드 닫힘)은 풀었다. 다만 메뉴가 떠 있는 동안 **새 메시지로 목록이 밀리면** 다시 재지 않는다(W1).

## FAIL

없음.

## WARN

### W1. 길게 누르기 메뉴가 떠 있는 동안 새 메시지가 오면 복사본 · 메뉴가 옛 자리에 남는다
- 자리: `app/lib/chat/screens/chat_room_screen.dart` `_FollowBubbleState`(파일 끝 · `didChangeMetrics` → `_afterLayout`).
- 다시 재는 계기는 **화면 크기 · 키보드 높이 바뀜(`didChangeMetrics`)과 그 뒤 자리가 멈출 때까지뿐**이다. 대화 목록은 `reverse: true`(아래 기준)라, 맨 아래를 보고 있을 때 새 메시지가 들어오면 기존 말풍선들이 그 높이만큼 **위로** 밀린다. 그때는 metrics 변화가 없어 `_FollowBubble` 이 다시 재지 않는다 → 복사본 · 메뉴가 원래 말풍선과 어긋난다. 버그 8 과 같은 모양이고, 계기만 다르다.
- 근거: SPEC-004 U-4 `:202` 「떠오른 말풍선(복사본)과 메뉴는 **화면이 자리를 다시 잡은 뒤(키보드가 닫힌 뒤 등)** 그 말풍선이 실제로 있는 자리에 붙는다 — 복사본이 원래 말풍선과 겹쳐 보이고 … 어긋나지 않는다」. 그룹 채팅에서 메뉴를 연 채 상대 메시지가 오는 것은 흔하다. C-A22 시험 갈래(키보드)에는 없지만 규칙 문장에 걸린다.
- 고칠 방향: 메뉴가 떠 있는 동안 `ChatState`(또는 그 방 `changes`) 변경에도 `_afterLayout()` 을 부르게 한다(`_chat` 리스너 하나 — 복사본 `ListenableBuilder` 가 이미 `_chat` 을 듣고 있음). 시험: 메뉴를 연 채 `chat_message` 이벤트 → 복사본 rect = 말풍선 rect.
- 같은 자리의 작은 것(참고 R1): 그 메시지가 지워지거나(`chat_message_deleted`) 화면 밖으로 밀리면 `_measure()` 가 null 을 주고 **마지막 자리를 그대로 둔다**(주석대로). 지운 메시지 메뉴가 계속 떠 있고 [수정] · [삭제]가 남는다 — 누르면 서버가 404 를 돌려준다. 이것은 앞 판에도 있던 동작이다.

## 8번 — 원인 · 다시 재기

- 작성자가 적은 원인은 코드로 맞다.
  - 앞 코드는 `_menu` 에서 `findRenderObject` → `localToGlobal` 로 누른 순간 한 번 잰 `rect` 를 `pageBuilder` 에 고정했다(diff `-` 줄).
  - `showGeneralDialog` 의 route 가 포커스를 가져가 입력칸 포커스가 빠지면 키보드가 닫히고, 셸이 키보드만큼 줄였던 본문이 되돌아온다. 목록이 `reverse` 라 말풍선이 아래로 다시 잡힌다.
- 고친 방법:
  - `_FollowBubble` 이 `initState` · `didChangeMetrics` 마다 post-frame 에 다시 잰다. 바뀌었으면 `setState` 를 하고 다음 프레임에도 다시 재며, 같아지면 멈춘다.
  - post-frame 은 `if (!mounted) return` 으로 dispose 뒤 안전하다 · `dispose` 에서 observer 를 뗀다.
- 메뉴 자리: 아래가 모자라면 위로 간다(기존 규칙) + `clamp(pad.top + 8, screen.height − pad.bottom − 8 − h)` 로 안전 영역 안에 가둔다. 캡처 `phone-fix3-longpress-after-keyboard.png` 에서 복사본이 원래 말풍선에 겹치고 메뉴가 위쪽 화면 안에 있다.
- 작성자의 「다시 재기를 끄면 6건 실패」: 시험이 「inset 336 → 0 뒤 말풍선이 실제로 움직였는지 먼저 확인」하므로 구조상 실패할 수 있는 시험이다(내가 끄고 돌려 보지는 않음 — 수정 금지).
- 참고 R2: 키보드 애니메이션 동안 `didChangeMetrics` 가 프레임마다 오면 `_afterLayout` 체인이 겹쳐 생긴다. 각 체인은 자리가 같아지면 멈추므로 기능 문제는 없다(작은 낭비).

## 9번 — 탭 보임/숨김 표(폰)

판정: `shell.dart` `chatDeep = _cur == chat && _chatStack.depth > 0` · `tabs = !keyboard && !chatDeep`. `_PageDepth` 는 채팅 탭 Navigator 의 **PageRoute** 만 센다(첫 route · 팝업 · 시트 제외 · push/pop/remove/replace 모두 반영).

| 화면 | 탭 | 근거 |
|---|---|---|
| 채팅 목록(루트) | 보임 | depth 0 |
| 대화(키보드 닫힘 · 열림) | 숨김 | depth ≥ 1(열림은 원래도 숨김) |
| 방 정보 · 모아보기 · 새 대화 · 초대 | 숨김 | 채팅 탭 PageRoute |
| 크게 보기 · 재생 | 숨김 | 세션 Navigator 전체 화면이 탭바를 덮음(기존) |
| 목록 위 확인 창 · 시트 | 보임 | PopupRoute 는 안 셈(작성자 2 · 스펙 「화면」 범위) |
| 채팅 거절 안내 | 보임 | `_onChatDenied` 가 `popUntil(first)` → didPop 으로 depth 0 · 본문은 루트 자리 |
| 다른 메뉴(시술현황 · 설정 · 예약) | 보임 | `_cur != chat` |
| 대화에서 다른 메뉴로 | 그 메뉴는 보임 · 채팅으로 돌아오면 숨김 | depth 는 채팅 Navigator 상태 그대로 |
| 배너 · 푸시로 대화에 바로 | 숨김 | 시험 「배너 [보기]로 들어와도 숨김」 |
| 아이패드 | 레일 그대로 | 폰 분기만 |

- 뒤로 제스처 도중: `didStartUserGesture` 를 보지 않아 pop 이 끝난 뒤에 탭이 나타난다(자연스러움).
- 세션이 바뀔 때: `AppShell(key: ValueKey(session.session))`(`app.dart:258-259`)로 셸 · `_chatStack` 이 새로 생겨 어긋남이 없다.
- `chatTabActive` · `watching` · 탭 배지 · 배너 코드는 무변경이다(지금 메뉴는 그대로 「채팅」).
- **아래 안전 영역**:
  - 탭이 숨은 화면은 셸이 `mq`(padding 포함)를 그대로 넘기고, 입력줄 · 비활성 줄이 `6/14 + paddingOf.bottom` 을 더한다(`chat_room_screen.dart:599-605 · 711`). 대화 Scaffold 는 `SafeArea(bottom: false)`(`:244`)라 두 번 들어가지 않는다.
  - 키보드가 열리면 셸이 `removePadding(bottom)` 을 해서 0 이 된다 → inset 을 두 번 빼지 않는다.
  - 탭이 보이면 `removePadding(bottom)` → 0(탭바가 `bottom` 을 가짐).
  - 방 정보 · 모아보기 · 새 대화 끝 여백도 같은 방식이다(새 대화는 `SafeArea` 안이라 `paddingOf` = 0 → 이중 없음).
  - 캡처 `phone-fix3-room-reads.png`(inset 34)에서 입력줄이 홈 표시줄 위에 있다.

## 10번 — 읽음 셈 손 계산 표

`unreadReaders`(`chat_model.dart`)는 스펙 `:183` 의 ①~④를 줄 단위로 같게 구현했다: 보낸 사람 제외 · `!active` 제외 · `fromSeq >= seq` 제외 · 「나」 = max(「나」 줄, `myLastRead`) · `read < seq` 셈. `unreadOf`(`chat_state.dart:658-668`)는 시스템 · 지운 = 0, 방 모름 = 0, 보고 있는 방이면 `myLastRead = max(Room.lastReadSeq, 받은 최대 seq)` 이다.

그룹 = 나(C) · A · B · D(나중 초대). 손 계산과 코드 결과가 모두 같다.

| 갈래 | 설정 | 손 계산 | 코드 |
|---|---|---|---|
| A 가 보냄(seq 5) · 나 안 봄 | A=5(senderRead) · B=4 · C=4 | B · C = 2 | 2 |
| B 읽음 | B=5 | C = 1 | 1 |
| 나 읽음(chat_read) / 보고 있음 | C=5 / drawn 5 | 0 | 0(숫자 없음) |
| 내 메시지(seq 6) | 나 제외 · A=5 · B=5 | A · B = 2 | 2 |
| 초대된 D: from=6 · 앞 메시지(seq ≤ 6) | `fromSeq >= seq` | D 안 셈 | 안 셈 |
| 초대 뒤 메시지(seq 8) | D last=6 | D 셈 | 셈 |
| 나간 멤버 | `chat_room` 새 members[] 에 없음 | −1 | −1 |
| 비활성 | `active=false` | 안 셈 | 안 셈 |
| 지운 · 시스템 줄 | — | 숫자 없음 | 0 |
| 1:1 | 상대 1 → 읽으면 0 | 1 → 0 | 1 → 0 |
| **그룹 만든 직후 첫 메시지** | 서버 `_join`: 모두 last = from = 0 · 시스템 줄 seq 1 · 첫 메시지 seq 2(만든 사람 = 보낸 사람 → senderRead 2) | 나머지 N−1 · 읽으면 #15 `least(2, last_seq)` 로 2 → 줄어듦 | 같음 — 영원히 남지 않음 |
| 숨겼다 다시 봄(1:1) | 숨긴 방은 목록에 없음 → `room()` null → 0 · 다시 열면 `_upsert` 로 members 들어옴 | 다시 셈 | 같음 |
| 재연결 | `GET /rooms` → `_keepReads`(max) + `_senderRead`(받은 메시지) | 같은 수 | 같은 수(시험 있음) |

## 정정 1 — `_senderRead` 걸린 길 표(직접 grep: `.merge(` · `_onMessage(` · `rooms =`)

| 길 | 자리 | 걸림 |
|---|---|---|
| 실시간 `chat_message` | `chat_state.dart:605` → `_onMessage` → `:672` | ✓ |
| 보낸 응답 | `:888` `_onMessage(m)` | ✓ |
| 전달 결과 | `:931` `_onMessage(msg)` | ✓ |
| 처음 읽기(최근 50) | `:422` merge · `:423` | ✓ |
| 위로 더 | `:451` · `:452` | ✓ |
| since 메우기 · 최근 50 다시 | `:492-497` | ✓(둘 다) |
| 목록 다시 읽기 | `:393-396` 새 members[] 에 이미 받은 thread 전부 | ✓ |

merge 4곳 · `_onMessage` 3곳 · 목록 1곳 → **빠진 길 0**. 시스템 줄은 제외된다(`:316`).

- `_keepReads`(`:304-311`)는 fresh 의 멤버마다 「옛 줄이 있고 `fromSeq` 가 같고 옛 값이 크면 옛 값」 → max. 지금 줄에 없던 멤버 · `fromSeq` 가 바뀐 멤버는 받은 값이다(스펙 `:186` ② 예외). 숫자를 **되살리는** 경우는 다시 들어온 멤버뿐이고, 그 멤버는 새 경계(`fromSeq`) 뒤 메시지만 세므로 의도대로다. 나간 멤버는 fresh 에 없어 빠진다.
- 가변 `Member.lastReadSeq` 공유: 방 정보 · 목록 화면이 같은 `Room.members` 객체를 쓴다. 바뀌는 값은 숫자 칸 하나이고 그 화면들은 그 칸을 그리지 않는다. 바꾼 뒤 `_notify()` 를 부르므로 부작용은 없다. `Member` 의 `const` 생성자가 없어졌지만 사용처는 컴파일된다(analyze 0).

## 정정 2 — 보고 있는 방

- `unreadOf` 는 기존 `watching` getter(`:516` · 무변경)를 그대로 쓴다. 보고 있지 않으면(앱이 뒤 · 다른 메뉴 · 목록 · 방 정보를 위에 띄움 = `watching` null) `Room.lastReadSeq` 로 센다 → 숫자가 뜬다(시험 「보고 있지 않으면 뜸」).
- 「그린 메시지」 = 그 방 thread 의 최대 seq(작성자 4 — 목록이 받은 것을 모두 그림). 받아들인다.
- 읽음 요청이 실패하면 화면(보고 있는 동안 0)과 서버가 어긋난다. 실패하면 `_readSent` 를 지워 다음 새 메시지 · 다시 열기 때 다시 보낸다. 보고 있지 않게 되면 화면도 서버 값으로 돌아오므로 **계속** 어긋나지는 않는다(참고 R3).

## 서버 계약

| 앱이 읽음 | 서버 | 같나 |
|---|---|---|
| `members[].id` | `person()` `str(account_id)`(`queries/chat.py:44-45`) | ✓ — `chat_member_read.accountId` 와 같은 id |
| `members[].lastReadSeq` · `fromSeq`(int · 없으면 0) | `queries/chat.py:297-306` int | ✓ · 옛 서버 = 0 → 「모두 안 읽음」으로 셈(옛 서버와는 짝이 아님 — 같은 PR 로 나감) |
| `chat_member_read {roomId, accountId, lastReadSeq}` | `services/chat.py:991-995` str · str · int | ✓ · 모르는 방 · 멤버 무시 · 작거나 같으면 무시 |
| 7종 구독 | `chat_events.EVENTS` 7종 | ✓(`chat_stream.dart:9-18`) |

## 표시 · 새 글자

- 숫자 = 시각 칸 위 · `Typo.caption600` · `Ms.primary` · 0 이면 없음 · 내 것 오른쪽 정렬 / 남의 것 왼쪽 정렬 · `tabularFigures`. 시스템 · 지운 = 0. 보내는 중 · 실패 말풍선은 `ChatMessage` 가 아니라 pending 이라 숫자가 없다(시험 있음). 사진 · 동영상 · 「수정됨」도 같은 칸이다. 복사본은 `ListenableBuilder(_chat)` 로 숫자를 따라간다.
- 캡처: `phone-fix3-room-reads.png` 에서 사진(다코디 보냄) 2 · 내 메시지 3 · 앞 메시지 없음 — 4명 방 손 계산과 맞는다. `phone-fix3-longpress-after-keyboard.png` 는 복사본이 겹치고 숫자 3 이 유지된다. 스펙 와이어(시각 위 숫자)와 같다.
- **새 화면 글자 0** — `git diff -- app/lib` `+` 줄 한글 리터럴 집합 = 앞 판과 같다(「수정됨」은 기존 줄을 `Column` 안으로 옮긴 것). 숫자는 `'$unread'` 뿐이다.

## 성능

- `unreadOf` 는 말풍선 build 마다 멤버(≤ 20)를 훑는다. `ListView.builder` 라 보이는 말풍선만 build 되므로, 한 번 다시 그릴 때 보이는 말풍선 × 20 정도다(메시지 수백과 무관). 멤버 줄 찾기는 `where().firstOrNull` 선형이지만 20명이라 작다.
- `chat_member_read` 하나 → `_notify()` → ChatState 를 듣는 화면(목록 · 열린 대화)이 다시 그려진다. 목록 행은 읽음 숫자를 그리지 않으니 낭비이지만 작다(참고 R4). 같은 값이면 `_notify` 하지 않는다.

## 조용히 통과하는 자리

1. W1(새 메시지로 밀림) · R1(지워진 메시지)에는 시험이 없다 — 「길게 누르기 자리」 6건은 키보드 갈래만 본다.
2. 「그룹 만든 직후 첫 메시지」는 순수 함수 표에 따로 이름 붙은 갈래가 없다(일반 갈래가 같은 계산을 덮음 · 서버 `_join` 시작값 0 을 쓴 앱 시험은 없음).
3. skip 수: 내 실행 `~73` · 작성자 보고 `~67`. 새 캡처 시험(skip 기본)이 늘어난 몫으로 보인다 — 통과 수 +341 은 같다.
4. C-A22 실기기 · C-A25 두 계정 실물은 pending(사용자 · 로컬 스택 금지).

## 수용 항목 ↔ 시험

C-A16(새 글자 0 · 탭 4메뉴 시험) · C-A22(`chat_ui_test.dart:652` group 6건) · C-A23(`:465` group 4건 + 배너 · 403 갈래) · C-A24(서버 · 앞 검수) · C-A25(`chat_state_test.dart:618-` 순수 함수 11 + 상태 갈래 7 · `chat_ui_test.dart:602 · 636` UI 2) · C-A11(`chat_contract_test.dart:165`) — 모두 있음. W1 갈래만 빠짐.

## 범위

`app/lib` · `app/test` 만. `app/lib/interpret/` · `pubspec.*` · `app/ios` 무변경. 새 의존성 0. (같은 워크트리의 `backend/` 변경은 서버 몫 — 대상 아님.)

## 참고

- R1. 지워진 · 화면 밖 말풍선 → 마지막 자리 유지 · 메뉴가 남음(앞 판과 같은 동작). `chat_message_deleted` 를 받으면 메뉴를 닫는 편이 낫다(새 글자 없음).
- R2. `_afterLayout` 체인이 키보드 애니메이션 동안 겹쳐 생김 — 하나만 돌게 플래그 하나.
- R3. 읽음 요청 실패 시 보고 있는 동안만 화면이 서버보다 앞선다(계속은 아님).
- R4. `chat_member_read` 가 목록까지 다시 그림 — 방 단위 알림으로 나누면 줄일 수 있다(지금 규모에선 불필요).
- R5. 옛 서버(칸 없음)와 짝이 되면 `lastReadSeq = 0` 이라 모든 메시지에 숫자가 뜬다 — 같은 PR 로 서버 · 앱이 함께 나가므로 문제 없음. 배포 순서가 갈리면(앱 먼저) 생긴다.

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd app && fvm flutter analyze` | No issues found! |
| `cd app && fvm flutter test` | **+341 ~73 All tests passed!** · exit 0 |
