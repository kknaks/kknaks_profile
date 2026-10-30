# 리뷰 리포트 — internal-chat / code r4 (2026-10-29)

대상: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` `kknaksss/internal-chat-invite` · `git diff 3ed1089` 미커밋(20 파일 변경 + 새 3: `chat_media_screen.dart` · `chat_app7_test.dart` · `test_chat_r5.py`)
SSOT: `r5-dispositions.md`(SPEC 보다 이김) → SPEC-007 0.5.0 §4.6 V1 ~ V12 · §4.7 · #20 · DEC-009 D-67 ~ D-69 · OQ-962 ~ 969 → `review-doc-r5.md`
읽기 목적 실행: `uv run pytest -q tests/test_chat_r5.py` = **10 passed**(전체 532 · 앱 248 은 코디 수치). 검사 grep: 법적 주석 = 5 · `@router.` = 20 · 라우트 뒤 `def ` = 0 · 변경 전부 `procedure/` 안(기능 독립 OK).

## 판정: WARN

FAIL 0 · WARN 3 · 참고 2. D-69 경계는 back 의 읽기 길 전부에 있다(V1 ~ V12 + 표 밖 grep 전수). 처분 FAIL-1 · W-1 · W-2 · W-3 은 코드와 시험에 있다. W-4(앱이 다시 받기)는 **가장 흔한 경우를 못 잡는다** — 아래 WARN-1.

---

## 1. D-69 경계 — back 읽기 길 전수

grep(`FROM chat_message|FROM chat_photo|JOIN …` · `.chat_messages(|.last_chat_message(|.chat_unread(|.chat_message(|.chat_photo(|.chat_message_by_client(|.chat_attachments(|.chat_members(`)으로 나온 줄 전부를 봤다.

| V | 길 | 코드 | 판정 |
|---|---|---|---|
| V1 · V2 | 목록 처음 · `before` · `since` | `repo.py` `chat_messages(after_id=)` — `where` 머리에 `id > ?` 를 넣어 세 꼴 모두 걸림 · `service/chat.py:368` 이 내 `from_message_id` 를 넘김 · `hasMore` = `limit+1` 이라 경계에서 false | PASS |
| V3 | 미리보기 · SSE `chat_room` | `_room` `chat.py:138` `last.id > me.from_message_id` 아니면 `lastMessage` null · `_room_events` 가 받는 사람마다 `_room` 을 불러 SSE 도 같이 걸림 | PASS |
| V4 | 안 읽음 · `unreadRooms` | 안 바꿈 · `_join` 이 `last_read = from = last_id` 로 시작 · `read` 는 `max` · `test_chat_unread_invariant`(7가지 길) | PASS |
| V5 | #14 · #17 · #18 | `_attachment` → `_sees(member, p.message_id)` `chat.py:90` · 전달본은 대상마다 새 `chat_photo` 행이라 `message_id` 가 그 방 것 | PASS |
| V6 | 전달 원본 #19 | `lock_write` 뒤 `_sees(me, m.id)` → 404 `chat_message_not_found` · 원본 첨부 `:490` 은 그 뒤 | PASS |
| V7 | 모아보기 #20 | `repo.chat_attachments` `m.id > ?` · 지운 메시지 · 지운 첨부 빠짐 · `limit` `Query(ge=1, le=60)` → 400 `invalid_request`(`main.py:108` 핸들러 · 시험 `{0, 61, "x", "a"}`) · `async def` | PASS |
| V8 | 고치기 · 지우기 | `_sees` 가 403 · 400 보다 먼저(404) | PASS |
| V9 | SSE edited · deleted | `_seers(chat_members, message_id)` `chat.py:568` · `:606` · `test_chat_boundary_sse` | PASS |
| V10 · FAIL-1 | SSE `chat_message` · 푸시 | SSE = `_insert` · `add_members` · `create_group` · `leave` 네 곳 모두 `_seers` · 푸시 = `push.py:184` `from_message_id < m.id`(커밋 뒤 다시 읽어도 그 사이 초대된 사람은 경계 ≥ mid 라 빠짐) · `test_chat_boundary_push_race` 가 태스크를 잡아 두고 초대 뒤 보냄 → 새 멤버 APNs 0 · SSE 0 | PASS |
| V11 | 같은 `clientId` | 안 바꿈(내 메시지) | PASS(SPEC 그대로) |
| V12 | 읽음 · 이름 · 멤버 · 숨기기 · 알림 · 나가기 | 내용 없음 · `read` 는 `last_chat_message` 의 id 만 | PASS |

**표 밖**: `chat_rooms_of`(`me_last_read` 만 · 내용 없음) · `chat_photo_live_refs`(파일 지우기 셈) · `open_direct` · `_check_peer` — 내용을 내보내지 않는다. 빠진 길 0.

### `from_message_id` 정의 · 옛 DB · 불변식

- 방 만들 때(만든 사람 · 처음 멤버) · 1:1 · 추가 · 다시 초대가 모두 `_join` 한 곳(`chat.py:175-185`) — 새 행 · 덮기 둘 다 `from_message_id = last_read_message_id = 마지막 id`. 그룹 만들기는 `_join` 들 **뒤**에 초대 줄을 써서 줄이 경계 밖(보임). PASS
- 옛 DB: `MIGRATIONS` 한 줄 + 그 부팅에 열을 **새로 더했을 때만** `_backfill_chat_from`(`db.py:269` · 같은 `connect()` 커밋). SQL = `MAX(id) … created_at < joined_at` 이고 SPEC §3 r5 와 같다. 시험은 같은 밀리초 · 나간 행 · 두 번째 부팅은 손대지 않음 · **채우기 전 · 뒤 `unread` 같음**(처분 W-1)을 본다. PASS
- 새 DB 는 `CREATE TABLE` 에 열이 있어 채우기를 부르지 않는다. 맞다.

## 2. #20 back ↔ app 대조

| 칸 | back | app | |
|---|---|---|---|
| 경로 | `GET /api/chat/rooms/{room_id}/attachments` | `api.dart` `chatAttachments` 같은 경로 | 같음 |
| 쿼리 | `before?` · `limit?`(1 ~ 60 · 기본 60) | `before` · `limit`(`mediaPage = 60`) | 같음 |
| 응답 | `MessageList {items, hasMore}` · id 내림차순 | `items` → `ChatMessage.fromJson` · `hasMore == true` · `_merge` 가 id 내림차순으로 다시 맞춤 | 같음 |
| 다음 쪽 | `id < before` | `before = _items.last.id`(가장 오래된 것) | 같음 |
| 오류 | 404 `chat_room_not_found` · 400 | 401 → `onUnauthorized` · 그 밖 = 실패 + [다시 시도] | 같음 |

## 3. 초대(D-68)

- 문구: back `_invited` `chat.py:188-191` = `"{A}님이 {B}님, {C}님을 초대했습니다"` · `create_group` · `add_members` 같은 함수. 옛 「…초대했어요」 행은 그대로(시험 `:346-353` · OQ-964). grep `참여자 추가|초대했어요|다시 초대받으면|그룹을 만들어요`(lib · app) = **0**(남은 것은 `chat.py:280` 독스트링의 「= 참여자 추가」와 시험의 옛 행 · 「없음」 단언뿐). PASS
- 그룹 만들기 줄 1 · SSE `chat_message` 멤버 전원(`_seers` · 모두 경계 0) · **푸시 0**(시스템 줄 · `self.push` 안 부름). PASS
- 1:1 [초대]: `chat_new_screen.dart` `_fromDirect` → `createGroup([peer, …고른 차례])` 제목 없음 · `_cap` = 20 − 2 = 18 · 안내 「N명 선택 · 나 포함 N+2명 · 최대 20명」 · 상대 = 「이미 참여 중」(`_members`). `chat_info_screen.dart:49-63` — 1:1 이면 `openRoom(made.id)` → `ChatListScreen._onOpenRequest` → `open`(폰 = `popUntil(isFirst)` + 새 방 / 아이패드 = 시트를 루트에서 닫고 `_select`). 1:1 방은 손대지 않음. 비활성 상대 = `peerInactive` 로 버튼 숨김. PASS
- 나가기 문구 OQ-968 · `chat_app3_test` 옛 기대도 고침(처분 W-2). PASS

## 4. 회귀

- 전달: `forward` 원본 확인이 `lock_write` 뒤 같은 자리 · 대상 SSE 는 `_insert` 의 `_seers`(새 id 라 모두 받음). `test_chat_r4` 기대는 「만듦 줄 +1」(메시지 수 4 → 5)만 바뀌었다. 단언이 약해지지 않았다.
- 공용 시트 · F10: `showRightSheet` · `showCenterPanel` · `DetailHeader` 그대로. 방 정보 시트 머리만 `onBack` 을 루트 pop 으로 바꿨다(시트 안 Navigator 때문 · 맞음).
- 1판 ~ 3판 시험: 옛 「옛 메시지 보임」 단언(`test_chat.py:136-137`)은 D-69 로 뒤집혔다. 처음 멤버는 그대로 전부 보는지 새 단언을 더했다. 경로 수 71 · `CHAT_ROUTES` 20 · 채팅 밖 51 그대로.

---

## WARN

### WARN-1 — W-4 「경계가 바뀐 방은 처음부터」: 멤버 구성 비교로는 **나갔다 다시 초대된 가장 흔한 경우를 못 잡는다**
- 자리: `app/lib/chat/chat_state.dart:214` `_memberKey` · `:292-300` `catchUp` · `:421` `chat_room`
- 근거: r5-dispositions W-4(「내 `chat_room` 이벤트를 받았거나 방 목록의 내 경계가 바뀐 방은 다시 들어갈 때 처음부터」) · SPEC §4.6 「다시 초대」
- 무엇이 일어나나: 기기 2 가 꺼져(또는 SSE 끊김) 있는 동안 B 가 기기 1 에서 나가고 → 다시 초대된다. 그 사이 다른 사람의 들고 남이 없으면 멤버 id 묶음은 나가기 전과 **같다**(나 포함 · 나간 사람은 목록에 없지만 다시 들어왔음). 그래서 `_memberKey` 가 같고 reset 이 안 된다. 열려 있던 대화는 `since` 메우기로 가고, 서버는 경계 밖만 주므로 옛 메시지가 기기 2 화면에 그대로 남는다. 열려 있지 않은 방은 원래 `catchUp` 이 reset 하므로 상관없다. 결국 문제는 「그 방 대화를 띄운 채 꺼진 기기」 하나다.
- 시험: `chat_app7_test.dart:271` 은 **멤버가 늘어난** `chat_room` 만 본다. 같은 구성으로 다시 초대되는 경우는 시험이 없다.
- 처분은 이것을 PoC 의 알려진 한계로 받았고 앱 보완도 「작으면 하고 크면 보고」였다. 그래서 FAIL 은 아니다. 다만 지금 구현은 그 보완이 **된 것처럼 보이면서** 핵심 경우를 비운다. 고칠 길(앱만): 앞으로 올 때 **열린 방**은 `since` 대신 늘 처음 50 을 다시 읽는다(열린 방은 보통 1개라 싸다). 또는 `refreshRooms` 뒤 그 방 `lastMessage` 가 null 로 바뀐 것까지 조건에 넣는다(이것만으로는 불충분). 코디가 정한다.

### WARN-2 — 모아보기 칸 누름의 404 확인이 메모리 캐시에 막혀 거의 안 돈다
- 자리: `app/lib/screens/chat_media_screen.dart:118-127` `_open` → `ChatState.photo` · `thumb`(`chat_state.dart:740-755` — 캐시가 맞으면 서버를 안 부름)
- 근거: SPEC §10.16 「못 열면(그새 지워짐 · 404) 토스트 … + 그 칸 뺌」
- 칸이 그려질 때 이미 같은 키로 캐시에 들어가므로, `_open` 은 늘 `ok = true` 다. SSE `chat_message_deleted` 를 놓친 채 지워진 사진을 누르면 캐시 바이트로 크게 보기가 열린다. 동영상은 썸네일만 확인하므로 재생 화면이 404 를 따로 처리한다. SSE 가 살아 있으면 칸이 먼저 빠지고, 다시 연결되면 `resync` 로 다시 읽으므로 보이는 범위는 작다. `chat_app7_test.dart:109` 는 캐시가 빈 칸으로 404 를 만들어 통과한다(**조용히 통과하는 자리**). 경계 문제는 아니다(경계 안 사진은 목록에 없어 캐시에 들어오지 않음).

### WARN-3 — 아이패드: 다른 기기에서 나가면 오른쪽 시트(방 정보 · 모아보기)가 남는다
- 자리: `app/lib/screens/chat_info_screen.dart:20-28` `ChatInfoSheet` · `chat_room_screen.dart:107` `_onRemoved`(`!widget.pane` 이면 아무것도 안 함) · `chat_list_screen.dart` `_onRemoved`(오른쪽 칸만 비움)
- 근거: SPEC §10.16 「나감 · 숨김 = 방 정보와 함께 닫힘」
- 폰은 대화 화면이 `popUntil(isFirst)` 로 모아보기까지 닫는다. 아이패드는 루트 위 시트를 아무도 닫지 않는다. 방 정보는 `room == null` 이라 빈 칸이 되지만 **모아보기 격자는 받아 둔 칸을 계속 보여 준다**. 서버가 404 를 주므로 새로 새는 것은 없고 화면에 남는 것뿐이다. 방 정보 시트가 안 닫히는 것은 3판부터 있던 부채이고, r5 가 그 시트 안에 격자를 얹어 눈에 띄게 됐다. 고칠 길: `ChatInfoSheet` 가 `removed` 를 듣고 루트 pop.

---

## 사용자가 실물에서 만날 자리

1. **배포 첫 부팅 = 옛 대화가 갑자기 안 보이는 사람이 생긴다**: 옛 판에서 나갔다 다시 초대된 사람은 `joined_at` 이 다시 초대된 시각이다. 채우기가 그 앞 메시지를 숨기므로, 어제까지 보이던 대화가 업데이트 뒤 사라진다. D-69 를 그대로 옛 데이터에 쓴 결과라 맞는 동작이지만, 사용자에게 미리 말해 둘 자리다.
2. **새 그룹 첫 줄**: [새 대화]로 만들어도 1:1 [초대]로 만들어도 첫 줄이 「가람님이 나래님, 다솜님을 초대했습니다」이고, 방 목록 미리보기도 그 줄이다(전에는 비어 있었음).
3. **한 방 안에 두 문구**: 옛 「가람 님이 나래 님을 초대했어요」(띄움 · 해요체)와 새 「가람님이 나래님을 초대했습니다」가 섞여 보인다(OQ-964 · 의도).
4. **다시 초대된 사람의 대화 = 초대 줄부터**: 위로 끌어도 더 없다(`hasMore:false`). 나가기 전에 내가 쓴 글도 없다(OQ-969).
5. **1:1 [초대] 뒤**: 새 그룹이 열리고 1:1 은 목록에 그대로 있다. 같은 세 사람으로 또 누르면 그룹이 또 생긴다(D9-08).
6. **대화를 띄운 채 꺼둔 두 번째 기기**: 그 사이 나갔다 다시 초대됐으면 옛 메시지가 남아 보일 수 있다(WARN-1). 앱을 다시 열거나 방을 다시 들어가면 사라진다.
7. **아이패드**: 방 정보 → 「사진 · 동영상」은 시트 안에서 넘어가고 [‹ 방 정보]로 돌아온다. 크게 보기 · 재생은 전체 화면이다. 다른 기기에서 나가면 시트가 남는다(WARN-3).
8. 모아보기 격자: 날짜 묶음 · 개수 없음 · 길게 누르기 메뉴 없음. 이것을 「안 된다」로 볼 수 있다(의도 · OQ-966).

## 참고(기존 부채 · 판정 밖)

- `chat_media_screen.dart:67` `_load` 는 `_loading` 중이면 그냥 돌아간다. 그래서 다음 쪽을 받는 도중에 온 `resync`(다시 연결 · 앞으로 옴)는 버려진다. 다음 `resync` 나 다시 열기에서 맞춰진다.
- V11(같은 `clientId` 로 다시 보내면 경계 안의 내 옛 메시지를 돌려줌)은 SPEC 이 「길 없음」으로 받은 그대로다. 실패 말풍선은 나갈 때 `_remove` 가 지운다.
