# WP-APP-3 채팅 화면(8 · 9 · 10) — 결과 보고

## 상태: done (미커밋 · 브랜치 `kknaksss/fix-app-re1` · `app/lib` · `app/test` 만 · 정정 1 · 정정 2 반영)

근거: SPEC-004 개정 ④(U-2 하단 4메뉴 · 메시지별 읽음 표시 · U-4 「자리가 맞아야 한다」 · §3 `Member` · `chat_member_read` · C-A16 · C-A22 ~ C-A25 · OQ-C16 ~ C18) · SPEC-003 개정 ⑩ U-2 예외 · `wp-plan.md` WP-APP-3 · §3 읽음 계약 표 · **`correction-read-1.md`**(보낸 사람 읽음 · 합치기 max) · **`correction-read-2.md`**(W2 보고 있는 방 · W5 안전 영역 · W9 시험 갈래).

## 변경 파일(이번 판) — lib 8 · test 5 · 새 파일 0

| 파일 | 무엇 |
|---|---|
| `lib/chat/screens/chat_room_screen.dart` | (8) `_menu` — 누른 순간 한 번 잰 자리 대신 `_FollowBubble`(파일 끝 새 위젯 · 같은 파일)이 화면 크기 · 키보드 높이가 바뀔 때마다(`didChangeMetrics`) **레이아웃 뒤**(post-frame) 말풍선 자리를 다시 재서 복사본 · 메뉴를 옮김(같아지면 멈춤). 메뉴 = 아래 자리 모자라면 위(기존 규칙) + 안전 영역 안으로 가둠 · (10) `_content` 시각 칸 = 안 읽은 사람 수(시각 위 · `Ms.primary` · 0 이면 없음) — 복사본도 같은 `_content` · 숫자 따라 바뀜 · (9 · W5) 입력줄 · 비활성 줄 아래 = 안전 영역만큼(`_safeBottom` · 폰만 · 아이패드 칸 그대로) |
| `lib/ui/shell.dart` | (9) `_PageDepth`(채팅 탭 Navigator 관찰 — 루트 위 **페이지** 수 · 팝업 안 셈) · 폰 + 지금 메뉴 채팅 + 깊이 > 0 이면 `_TabBar` 숨김 · 그때 본문에 아래 안전 영역(padding)을 넘김(탭바가 없으니 안 뺌) · 키보드 규칙 · 아이패드 레일 · 다른 메뉴 그대로 · `chatTabActive` 그대로 |
| `lib/chat/chat_model.dart` | `Member.lastReadSeq`(오르기만 · 가변) · `fromSeq`(없으면 0) · **순수 함수 `unreadReaders`**(seq · 보낸 사람 · members · 내 읽음 → 수) |
| `lib/chat/chat_stream.dart` | `chatEvents` 7종 — `chat_member_read` |
| `lib/chat/chat_state.dart` | `chat_member_read` → 그 멤버 `lastReadSeq` 올림(작거나 같으면 무시) · `unreadOf(m)`(시스템 · 지운 = 0 · **보고 있는 방이면 그린 메시지까지 나 = 읽음** — 정정 2 W2) · **`_keepReads`**(어느 `Room` 이든 합치기 = max · 예외: 지금 줄에 없던 멤버 · `fromSeq` 바뀐 멤버 = 받은 값 — 정정 1 ②) · **`_senderRead`**(메시지를 받으면 보낸 사람 `lastReadSeq = max` — 실시간 · 보낸 응답 · 전달 결과 · 처음 50 · 위로 더 · since 메우기 · 목록 다시 읽기 뒤 — 정정 1 ① · 시스템 줄 제외) · `watching` 무변경 |
| `lib/chat/screens/chat_info_screen.dart` · `chat_media_screen.dart` · `chat_new_screen.dart` | (W5) 탭을 숨긴 폰 화면의 스크롤 끝에 아래 안전 영역만큼 더 — 방 정보 [나가기] · [목록에서 숨기기] · 모아보기 격자 끝 · 새 대화/초대 직원 목록 끝(아이패드 시트 · 가운데 창 그대로) |
| `test/support/chat_fake.dart` | `reads(member, lastReadSeq, fromSeq)` — 멤버 줄 새 칸 |
| `test/chat/chat_state_test.dart` · `chat_contract_test.dart` · `test/ui/chat_ui_test.dart` · `test/capture/chat_capture_test.dart` | 아래 표 |

`chat_list_screen.dart` 는 바꿀 것 없었다(목록 = 루트 → 탭 보임). 「크게 보기 · 재생」은 세션 Navigator 의 전체 화면이라 탭바를 원래 덮는다(셸 변경 없이 숨김).

## 8번 원인 — 확인한 사실

- `chat_room_screen.dart` `_menu`: `bubbleContext.findRenderObject()` → `localToGlobal` 로 **누른 순간 한 번** `rect` 를 재고 `showGeneralDialog` 의 `pageBuilder` 가 그 `rect` 로 `Positioned.fromRect`(복사본) · 메뉴를 놓았다(다시 재는 코드 없음).
- 이 창은 Navigator 에 올라가는 route 라 열리면서 포커스를 가져간다 → 입력칸 포커스가 빠져 키보드가 닫힌다 → 셸 Scaffold 가 키보드만큼 줄였던 본문을 되돌리고, 대화 목록은 `reverse: true`(아래 기준)라 말풍선들이 키보드 높이만큼 **아래로** 다시 잡힌다 → 복사본 · 메뉴는 옛 자리(위)에 남아 어긋남. 키보드를 닫은 채 누르면 다시 잡힐 일이 없어 괜찮음 = 사용자 관찰과 같다.
- 고친 방법: 「닫힌 뒤 다시 재기」(스펙이 고르라 한 둘 중). 이유 = 사용자 기준이 「키보드 닫힌 상태의 지금 모양」이고, 키보드를 열어 둔 채 띄우면 메뉴가 키보드 뒤로 갈 수 있어 자리 규칙을 따로 짜야 함.
- **시험이 실패할 수 있는가 확인**: `_FollowBubble` 의 다시 재기를 끄고 돌리면 「길게 누르기 자리」 6건이 **전부 실패**(+0 −6) → 되돌림.

## 9번 — 하단 탭을 찾는 기존 시험 전수(`grep tab-bar` 10곳 + 대화 안에서 다른 메뉴 누름)

| 자리 | 무엇 | 9 뒤 |
|---|---|---|
| `actions_test.dart:353` | 판 화면 폰/아이패드 탭바 | 그대로 통과 |
| `app_flow_test.dart:60 · 186 · 268` | 셸 4메뉴 · 판 권한 없음 · 로그인 전 | 그대로 |
| `chat_ui_test.dart:158` | board 권한 없는 직원 셸 | 그대로 |
| `chat_ui_test.dart:189 · 203` | `/me` 403 셸 없음 · 판 SSE forbidden | 그대로 |
| `notification_ui_test.dart:75` | 알림 목록이 탭바를 덮음 | 그대로 |
| `session_race_test.dart:24` | 셸 · 판 그대로 | 그대로 |
| `capture/chat_capture_test.dart:315` | 키보드 열린 대화 = 탭바 없음 | 그대로(이제 키보드와 무관하게 없음) |
| `chat_ui_test.dart` 「다른 탭에서 SSE 메시지 → 배너 [보기] …」 | 대화 안에서 `nav-board` 누름 | **깨짐 → 고침**: 대화에서 목록으로 돌아간 뒤 누름(`backToList`) + 「배너로 들어온 대화도 탭 없음」 단언 더함 |
| `chat_ui_test.dart` 「board 권한 없는 활성 직원 …」 | 대화 안에서 `nav-settings` 누름 | **깨짐 → 고침**: 같은 방식 |

## 10번 — 읽음 셈 표 시험

`chat_state_test` 「순수 함수 표」(11 갈래 — `unreadReaders` 하나): 3명 그룹 A 보냄 = 2 · B 읽음 = 1 · 나도 읽음 = 0 · 내 메시지(나 안 셈) · 1:1 = 1 → 0 · 초대된 D(`fromSeq`) 앞 메시지 안 셈 · 뒤 메시지는 셈 · 비활성 안 셈 · 나간 멤버(목록에 없음) −1 · seq 0 = 0.
상태 갈래(정정 1 · 2 포함 — 실제 이벤트 · 응답 길로):

| 시험 | 갈래 |
|---|---|
| 「A(2) 가 보냄 → 2 · chat_member_read B → 1 · 내 chat_read → 0 · 시스템 줄 · 지운 것 = 0」 | 기본 · 시스템 · 지운 |
| 「chat_member_read 순서 뒤바뀜 — 늦게 온 작은 값이 큰 값을 덮지 않음」 | 정정 1 ② |
| 「받은 뒤 읽음 요청 전에 답장(정정 1)」 | 정정 1 ① |
| 「전달(정정 1) — 다른 사람이 전달한 메시지도 보낸 사람 읽음으로 · 1:1 에서 1 → 0」 | 정정 1 ① |
| 「옛 Room 이 나중에 옴(chat_room · 목록) — 합치기는 늘 max · 다시 들어온 멤버(fromSeq 바뀜)는 받은 값」 | 정정 1 ② · 예외 |
| 「보고 있는 방(정정 2 W2) — 그린 메시지까지 나 = 읽음(읽음 요청 전에도) · 보고 있지 않으면 뜸」 | 정정 2 ① |
| 「초대된 새 멤버 · 나간 멤버 — chat_room 새 members[] 로 다시 셈 · 재연결 = 같은 수」 | 초대 · 나감 · 재연결 |
| `chat_ui_test` 「읽음 — 가짜 서버가 스트림으로 순서를 일부러 바꿔 보냄(큰 seq → 작은 seq → 옛 Room) · 받은 뒤 답장 · 보고 있지 않을 때만 …」 | 정정 2 W9(가짜 SSE 로 순서 뒤집음 · 화면 숫자 3 → 2 → 2 → 1) |
| `chat_ui_test` 「말풍선 시각 위 숫자(Ms.primary) · 읽을 때마다 줄고 0 이면 사라짐 · 시스템 줄 · 보내는 중 = 숫자 없음」 | 그리기 · 색 · 자리 · 갈래 |

## 수용 항목 ↔ 시험

| 항목 | 시험 |
|---|---|
| C-A22 | `chat_ui_test` group 「길게 누르기 자리 …」 6건(폰 · 아이패드 × 맨 아래(내 것) · 긴 글 · 맨 위): 키보드 inset 336 에서 누름 → inset 0 → **말풍선이 실제로 움직였는지 먼저 확인** · 복사본 rect = 말풍선 rect · 메뉴 화면 안 · 닫은 채 누른 모양과 같음 |
| C-A23 | group 「폰 하단 4메뉴 — 채팅 목록에서만」 4건: 목록 보임 · 대화 숨김(키보드 열림 · 닫힘) · 방 정보 · 모아보기 숨김 · 뒤로 → 보임 · 배지 값 유지 · 숨긴 채 읽음 요청(보고 있는 방) · **입력줄 = 홈 표시줄(34) 위** · 새 대화 숨김 · 다른 메뉴 보임 · 403 안내 = 탭 보임 · 아이패드 레일 그대로 · 배너 [보기]로 들어와도 숨김(위 고친 시험) · (W5) 방 정보 [나가기] · 새 대화 목록 끝 = 홈 표시줄 위 |
| C-A25 | 위 셈 표 · 상태 갈래 · UI 2건 |
| C-A16 | 새 글자 0(아래) · 기존 전체 시험 통과 |
| C-A11 | `chat_contract_test` 「Member — lastReadSeq · fromSeq … · 7종째 이벤트 chat_member_read」 |
| C-A12(회귀) | 기존 시험 그대로 통과 |

## §3 읽음 계약 표 ↔ 앱이 읽는 필드

| 계약 | 앱 |
|---|---|
| `Room.members[]` = `{id, name, role, active, me, lastReadSeq: int, fromSeq: int}` | `Member.fromJson` — 둘 다 없으면 0(옛 서버) · `Room` 이 나오는 모든 길(목록 · 만들기 · 1:1 열기 · 초대 · 이름 바꾸기 · `chat_room`)이 같은 `_upsert`/목록 대입 → 합치기 max |
| SSE `chat_member_read {roomId, accountId, lastReadSeq}` | 그 방 그 멤버만 · 오를 때만 · 모르는 방/멤버 무시 |
| 기존 `chat_read`(나) | 내 `Room.lastReadSeq` 그대로(셈의 「나」 = max(「나」 줄, Room.lastReadSeq, 보고 있으면 그린 끝 seq)) |
| 수 세기 | `unreadReaders` — 보낸 사람 아님 · `active` · `fromSeq < seq` · `lastReadSeq < seq` · 시스템 · 지운 · 보내는 중 · 실패 = 없음 · 서버에 수 요구 0 · 읽음 요청 횟수 변화 0 |
| 정정 1 | 메시지 받음 = 보낸 사람 max · 합치기 늘 max(다시 들어온 줄 예외) |

## 새 화면 글자

**0.** 숫자(`'$unread'`)만. 색 `Ms.primary`(기존 토큰) · 새 토큰 0.

## 명령 · 수치

- `fvm flutter analyze` → No issues found
- 고친 시험: `test/ui/chat_ui_test.dart test/chat/chat_state_test.dart` → +76 · `chat_contract_test` 포함 상태/계약 +59(중간) — 모두 통과
- **전체 `fvm flutter test` → +341 ~67(캡처 skip) All tests passed**(앞 판 +320 → +21)
- `fvm flutter build ios --no-codesign` → ✓ Built Runner.app 20.7MB

## 캡처 (`work/fix/app-captures/` — 새 이름 · 가짜 값만)

| 파일 | 장면 |
|---|---|
| `phone-fix3-list-tabs.png` · `ipad-…` | 채팅 목록(탭 있음 / 아이패드 레일) |
| `phone-fix3-room-reads.png` | 폰 대화 · 하단 4메뉴 없음 · **아래 inset 34 기기**(입력줄 홈 표시줄 위) · 숫자 2 · 3 인 말풍선과 0 이라 없는 말풍선 |
| `ipad-fix3-room-reads.png` | 아이패드 대화(레일 그대로) · 숫자 |
| `phone-fix3-room-keyboard.png` · `ipad-…` | 키보드 열린 대화 |
| `phone-fix3-longpress-after-keyboard.png` · `ipad-…` | 키보드 열고 누른 뒤 닫힘 — 복사본이 원래 말풍선 자리 · 메뉴 위쪽 화면 안 |

## 스펙과 다른 곳 · 물을 것

1. 숫자 자리 — 시각 위 한 줄 · `Typo.caption600`(시각 `caption400` 보다 굵게 — 눈에 띄게) · 크기는 같은 단계. 굵기는 구현 몫(OQ-C18 「픽셀 · 굵기는 구현 때」).
2. 탭 숨김 판정 = 채팅 탭 Navigator 의 **페이지** 깊이(팝업 · 시트는 안 셈). 목록에서 뜨는 확인 창 · 시트는 탭을 숨기지 않는다(스펙 범위 안 — 「화면」만 셈).
3. 아이패드: 입력줄 아래 안전 영역을 더하지 않았다(「아이패드 바꾸지 않는다」). 아이패드 홈 표시줄이 있는 기종에서 입력줄이 표시줄에 가까운 것은 지금과 같다.
4. 「보고 있는 방」에서 내가 읽은 것으로 보는 끝 = 그 방 메모리에 받은 메시지 중 가장 큰 seq(「화면에 그린」을 받은 것으로 해석 — 목록은 받은 것을 모두 그림).

## pending

- BE-3 뒤 로컬 두 계정 실물(C-A25) — 이번 발주 범위 밖(로컬 스택 금지).
- 실기기(그림 8 재현 · 두 계정 이상 읽음 · 홈 표시줄) — 사용자.
