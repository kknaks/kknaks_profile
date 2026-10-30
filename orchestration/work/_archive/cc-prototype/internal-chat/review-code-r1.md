# 리뷰 리포트 — internal-chat / code (2026-10-29)

- 대상: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` 미커밋 변경(base `origin/main` `dbf0b53`) — `procedure/back` 수정 10 · 새 6 / `procedure/app` 수정 16 · 새 15 (+ ios swiftpm 미추적 2)
- 기준: SPEC-007 0.2.0 + be-brief §0(W2-1 ~ W2-6 · D-45) · WORK-011 WP-REVIEW · DEC-009 D-01 ~ D-45 · 시안 r2(헤더 = D-38) · review-doc r1 · r2
- 읽기로 돌린 시험: `uv run pytest -q -k "chat or route_count"` = **27 passed** · `flutter test test/chat_app{1,2,3}_test.dart` = **45 passed** (전체 pytest 500 · flutter test 184 · analyze 0 · ruff 는 코디가 확인한 값을 그대로 씀)
- 서버 · 시뮬레이터 · compose 는 띄우지 않았다 → 화면 픽셀 비교 · 실 APNs 는 이 리포트 범위 밖(코디 시뮬레이터 · E2E 몫)

## 판정: FAIL (FAIL 1 · WARN 1)

FAIL 은 한 군데다. 나머지 계약(API 14 · SSE 5 · 푸시 payload · §0 W2-1 ~ 6 · WP-REVIEW 17항목 · 기능 독립)은 back · app 양쪽 모두 맞다. **FAIL-1 은 한 줄 수정**(앱이 삭제 응답 뒤 로컬 시각을 쓰지 않게)이면 닫힌다.

## FAIL

### FAIL-1 내가 지운 메시지에 기기 로컬 시각(오프셋 없음)을 `updatedAt` 으로 넣는다 → 다음 `since` 가 9시간 미래가 돼 놓친 메시지가 안 메워진다 (조용히 통과 · 시뮬레이터에서 만남)

- **코드**: `procedure/app/lib/chat/chat_state.dart:516` — `delete()` 가 `api.chatDelete` 뒤 `_onDeleted(m.roomId, m.id, DateTime.now().toIso8601String())`. Dart `DateTime.now().toIso8601String()` = **오프셋 없는 로컬 시각**(예 `2026-10-29T14:03:07.215123`). `_onDeleted`(`chat_state.dart:421-426`)는 늘 `byId[id] = m.asDeleted(at)` 로 덮어쓴다 — SSE `chat_message_deleted` 가 서버 `updatedAt` 을 먼저 넣었어도 HTTP 응답 뒤 이 줄이 다시 덮는다(두 신호 순서는 경합)
- `ChatThread.latestUpdatedAt`(`chat_state.dart:96-107`)은 시각이 가장 늦은 메시지의 **원래 문자열**을 고른다 → 방금 지운 그 메시지(지금 시각)가 뽑히고 오프셋 없는 문자열이 그대로 `since` 로 나간다(`chat_state.dart:260-266` `catchUp`)
- **서버**: `clock.parse`(`back/app/domain/clock.py:43-51`)는 「오프셋 없음 = UTC」 → 확인: `parse('2026-10-29T14:03:07.215123')` → `14:03:07.215+00:00`(실제는 `05:03:07.215+00:00`). KST 기기(시뮬레이터 = Mac 시간대)에서 `since` 가 **9시간 미래** → `updated_at >= since` 빈 목록 · `hasMore:false` → 앱은 「다 받았다」로 안다
- **깨지는 곳(실물)**: 대화방에서 내 메시지를 지움 → 앱을 백그라운드(또는 SSE 끊김) → 그동안 상대가 보냄 → 돌아오면 `catchUp` 의 `since` 메우기가 0 건 → **열린 대화에 그 메시지들이 안 보인다**(방 목록 미리보기 · 배지는 `GET rooms` 라 바뀜 → 「목록엔 있는데 대화엔 없음」). SSE 로 새 메시지가 하나 더 오면 그 뒤부터만 정상
- **근거**: SPEC-007 §5 「다시 연결 = `since=<받은 것 중 가장 늦은 updatedAt>`」(서버가 준 값) · §6.1 시각 꼴(KST 오프셋 · 밀리초) · §11 「앞으로 옴 · 다시 연결 = since 메우기」 · D9-19 · review-doc-r1 F-2(시각 경계 · 조용히 통과)
- **시험이 못 잡는 이유**: `test/chat_app2_test.dart:297` 은 SSE `chat_message_deleted`(서버 꼴 `+09:00`) 길만 본다 · `ChatState.delete` 뒤 `latestUpdatedAt` 꼴을 단언하는 시험이 없다
- **고칠 것(한 가지면 됨)**: `delete()` 에서 로컬 시각으로 `_onDeleted` 를 부르지 않고 SSE `chat_message_deleted`(서버 `updatedAt`)에 맡기거나, 로컬 표시만 바꾸고 `updatedAt` 은 원래 값 유지. 아울러 `latestUpdatedAt` 이 오프셋 없는 문자열을 고르지 않게(또는 서버 값만 쓰게) + 시험 1개: 「`delete()` 뒤 `thread.latestUpdatedAt` 이 `+09:00` 꼴」

## WARN

### WARN-1 로그아웃 상태에서 채팅 푸시를 눌러 앱을 열면, 로그인 뒤 그 방이 안 열린다

- **코드**: `procedure/app/lib/app_state.dart:214-217`(`_onTap` chat → `chat.openRoom(roomId)` = `openRequest` 에 방 id) → 로그인 `app_state.dart:289-291` 「계정 바뀜」 분기는 `session` 이 null 이면 늘 참 → `chat.clear()` → `chat_state.dart:589` `openRequest.value = null` 로 지움 → `ChatScreen._onOpenRequest`(`chat_list_screen.dart:97-110`)가 받을 값이 없다
- **근거**: SPEC-007 §8 「누르면 … 로그인 안 됐으면 로그인 뒤 그 방」 · DS:S12
- 실물: 토큰이 풀린 기기(12시간)에서 잠금 화면 채팅 푸시를 누름 → 로그인 → 채팅 탭은 열리지만(탭 값은 남음) 방 목록에서 멈춤. 저장된 세션이 살아 있는 보통 경우(C3)는 정상
- 고칠 것: `clear()` 가 `openRequest` 를 비우지 않게(로그아웃에서만 비움) 또는 로그인 분기에서 값 보존

## 고객이 실물에서 만날 자리 (코디 시뮬레이터 2대 · 실기기)

1. **FAIL-1** — 내 메시지를 지운 뒤 백그라운드 → 돌아오면 그사이 온 메시지가 열린 대화에 없음(목록 미리보기에는 있음). 시뮬레이터에서 바로 재현된다(시뮬레이터 시간대 = Mac = KST)
2. **WARN-1** — 로그인 풀린 상태에서 채팅 푸시 누름 → 로그인 뒤 방 목록에서 멈춤(실기기 · TestFlight 에서만 — 시뮬레이터는 푸시 없음)
3. 시뮬레이터 [사진] → [카메라로 찍기] = 카메라가 없어 토스트 「사진을 불러오지 못했어요」(`chat_room_screen.dart:142` 일반 catch — 권한 문구가 아님). 앨범은 됨. 결함 아님(카메라는 C5 실기기)
4. 아이패드: 방 정보 시트 · 가운데 창(새 대화 · 사진 시트) · 대화상자가 떠 있을 때 온 다른 방 배너는 **어두운 막 아래**(셸 안 층) — review-doc-r2 실물 #2 · OQ-933 · §0 W2-4 로 받은 값
5. 폰: 사진 크게 보기 · 알림 목록(루트 전체 화면) 중에 온 채팅은 배너 없이 지나감 · 탭 배지 · 방 목록만 바뀜(OQ-933 그대로)
6. 막 켠 직후(Dart 준비 전) 앞에서 받은 채팅 푸시는 iOS 배너 + 소리(`AppDelegate.swift` `dartReady` 아니면 기존 꼴 — review-doc-r2 실물 #4 · A11)
7. 비활성 상대 1:1 = 입력줄 대신 「비활성 계정이에요」(D9-42 · 서버도 409) — 시험 계정을 비활성으로 돌리면 바로 보임
8. 처음 초대받은 그룹 = 옛 메시지 안 읽음 0(D-45 처리됨 — r2 실물 #1 은 닫힘)

## 조용히 통과하는 자리 (review-doc r1 · r2 목록 → 코드에서 막혔나)

| # | 자리 | 코드 | 시험 | 결과 |
|---|---|---|---|---|
| r1-1 | 동기 핸들러 → 푸시 0 | `back/app/api/chat.py` 14 경로 모두 `async def` · W2-6 grep = 0 | `test_chat_push.py:82` `test_chat_push_targets_http` — TestClient HTTP → 가짜 APNs 요청 수 · 「이벤트 루프 없음」 0 | 막힘 |
| r1-2 | 같은 초 메시지 유실 · 안 읽음 누락 | `clock.py:33-40` `iso_ms` · `to_db_ms` · `repo.py` `chat_messages` `updated_at >= ?` · `chat_unread` `id > ?` | `test_chat.py` `test_chat_time_boundary`(같은 밀리초 고정) | 서버는 막힘 — **앱 삭제 경로가 다시 엶 → FAIL-1** |
| r1-3 | `_showing` 만 보는 배너 거름 | `chat_state.dart:15-26` `openDisplayScreens` · `qr_show_screen.dart` · `scan_screen.dart` 두 함수가 올리고 `finally` 로 내림 · 배너 = `shell.dart` `ChatBannerLayer`(셸 `Stack` 맨 위) · `main.dart` 는 observer 만 | `chat_app3_test.dart:187-265` 세 길(대기열 · 예약 상세 QR · 여권 스캔) | 막힘 |
| r1-4 | 2001자 → `invalid_request` | `service/chat.py:323-324` 서비스가 `len` 으로 `chat_message_too_long` · 스키마엔 `text` 길이 없음 | `test_chat_message_rules` 코드까지 단언 | 막힘 |
| r1-5 | 시스템 줄이 탭 배지 올림 | `chat_state.dart:404` `m.kind != MsgKind.system` | app1 시험 | 막힘 |
| r1-6 | PNG 스크린샷 400 | `photo_pick.dart:47-65` 늘 `flutter_image_compress` JPEG 85 | 픽커는 가짜(시험 불가) | 코드 막힘 · 실물 = C5 |
| r2-1 | 처음 추가된 사람 안 읽음 99+ | `service/chat.py:147-156` `_join` = 그 순간 마지막 id(D-45) | `test_chat_new_member_unread_zero` | 막힘 |
| r2-2 | 세 길 배너 시험을 가짜 위에 | 시험이 실제 `ReservationDetailScreen` push(`chat_app3_test.dart:215`) | — | 막힘 |
| r2-3 | 보고 있는 방 = 채팅 Navigator 맨 위만 | `chat_state.dart:28-56` `RootRoutes`(루트 Navigator observer · `main.dart` `navigatorObservers`) · `watching` 에 `rootRoutes.count == 0` | app3 | 막힘 |
| 새 | 삭제 뒤 `since` 가 로컬 시각 | `chat_state.dart:516` | 없음 | **FAIL-1** |

## WP-REVIEW 항목별 결과 (WORK-011 L77 · 17 + 머리)

| # | 항목 | 판정 | 근거(파일:줄) |
|---|---|---|---|
| 0 | SPEC §2 ~ §14 ↔ 코드 · 부록 A · B | PASS(FAIL-1 · WARN-1 빼고) | 아래 표들 |
| 1 | 경로 65 | PASS | `back/tests/test_order.py:247-277` `test_route_count_65` · 채팅 14 집합 단언 · 51 + 14 |
| 2 | 채팅 핸들러 `async def` | PASS | `api/chat.py:45-134` 14개 모두 `async def`. WP-REVIEW 문구의 `grep -n "^def "` = 1(도우미 `_int` `api/chat.py:38`) → §0 W2-6 이 이 grep 을 라우트만 보는 명령으로 바꿈 = **0** |
| 3 | 채팅 시각 밀리초 | PASS | `domain/clock.py:33-40` `iso_ms` · `to_db_ms` 새 함수(기존 `iso` · `to_db` 그대로) · 채팅 표 · API 만 사용(`service/chat.py` 전부 `to_db_ms` · `iso_ms`) |
| 4 | `since >=` | PASS(서버) · 앱 FAIL-1 | `service/chat.py:305-310` parse → `to_db_ms` · 못 읽음 400 · `repo.py` `chat_messages` `updated_at >= ?` · 앱 `api.dart` `Uri(queryParameters:)`(`+` → `%2B`) · 겹침은 `ChatThread.merge` id 키 |
| 5 | 안 읽음 id 기준 | PASS | `repo.py` `chat_unread`(`id > ? · account_id != ? · kind != 'system' · deleted_at IS NULL`) · `service/chat.py:389-409` read = `max(지금, min(messageId, 마지막 id))` · 0 = 안 바꿈(W2-2) |
| 6 | 배너 층(셸 안 · `main.dart` 아님) | PASS | `shell.dart` `ChatBannerLayer` 를 폰 · 태블릿 `Scaffold` 안 `Stack` 맨 위에 · `main.dart:32-33` 는 `navigatorObservers` 만(배너 없음 · `ToastLayer` 그대로) |
| 7 | 멤버 아닌 404 | PASS | `service/chat.py:71-77` `_member`(없음 · 나감 = `chat_room_not_found`) · 삭제 `:367-371` · 사진 `:439-452` · 시험 `test_chat_permission` |
| 8 | 붙기 전 사진 | PASS | `service/chat.py:446-448` `message_id` null = 올린 사람만 · 보내기 `:333-337` 남이 올림 · 다른 방 · 이미 붙음 · 지움 = `chat_photo_invalid` |
| 9 | `clientId` | PASS | 스키마 8 ~ 64(`schemas/chat.py:122`) · UNIQUE(`db.py` `chat_message`) · 처음 것 200 · SSE · 푸시 다시 안 함(`service/chat.py:330-332`) · 앱 UUID v4(`chat_view.dart:101-109`) · 다시 보내기 = 같은 `clientId`(`chat_state.dart:481`) |
| 10 | 푸시 대상 | PASS | `service/push.py` `chat_message()` — 지금 멤버 − 보낸 사람 − muted − 비활성 · 숨긴 1:1 받음 · 시스템 줄 · 지운 것 0 · `devices_of` 재사용 |
| 11 | 만료(호출 0 회귀) | PASS | `push/apns.py:48-52` `expiration: int = 0` · `Delivery.expiration` → `_send_with_retry` → `_send` → `client.send`(B9) · 채팅만 `now + 86400` · 시험 `test_chat_push_expiration` |
| 12 | `notification` 0 | PASS | `push.py` 채팅 경로는 `notification` 행 안 씀 · `notifications.py` · `NotificationKind` 변경 0 · 시험이 `notification` 0 · 종 unread 그대로 단언 |
| 13 | SSE 받는 연결 | PASS | `service/chat.py` — `chat_message` · `chat_message_deleted` = 지금 멤버 전원 · `chat_room` = 계정마다 `_room(…, i)` · `chat_room_removed` · `chat_read` = 내 계정만 · 허브 `send_to_account`(`container.py` 배선) · `id:` 없음(`test_chat_sse_frames_have_no_id`) |
| 14 | 사진 Bearer | PASS | `api/chat.py:129-134` `Actor`(헤더만 — `deps.py:17-21`) · `no-store` · `inline` · 시험 `?token=` = 401(`test_chat_push.py:316-319`) · 앱 `api.dart` `chatPhoto` 헤더만 |
| 15 | 사진첩 저장 0 | PASS | `image_picker` 카메라 = 저장 안 함 · 저장 · 공유 버튼 없음(`chat_photo_screen.dart:60-90`) · 저장 패키지 0(grep) |
| 16 | 디스크 캐시 0 | PASS | `chat_state.dart:58-80` 메모리 LRU 100 · `Image.memory` 만(`Image.network` · `path_provider` · `writeAsBytes` grep 0) · 고른 임시 파일 삭제(`photo_pick.dart:57-61`) · 로그아웃 · 계정 바뀜 `clear()` |
| 17 | 주석 4곳 | PASS | `grep -rn "법적 검토 필요: 직원 채팅" procedure/back` = 4 — `repository/db.py:194` · `service/chat.py:3` · `api/chat.py:132` · `service/push.py:37` |
| 18 | 실명 · 키 grep | PASS | 시험 이름 = 지어낸 두 글자(`tests/chat_env.py` 머리 「모두 지어낸 가짜」) · 비밀번호 칸 = `test-only-not-a-hash` · 도메인 · 키 · 전화 · 메일 grep 0 |

## API 14 · SSE 5 · 푸시 payload — back 구현 ↔ app 소비 양쪽 대조

**API 14 / 14 일치** (경로 · 메서드 · 요청 키 · 응답 키 · 타입)

| # | 경로 | back | app | 결과 |
|---|---|---|---|---|
| 1 | GET people | `PeopleList{items:[Person{id,name,role}]}` | `Api.chatPeople` → `Person.fromJson` | 같음 |
| 2 | GET rooms | `RoomList{items:[Room], unreadRooms}` · Room 11키 · Member 5키 · Preview 8키 | `chatRooms` → `Room.fromJson`(11) · `Member`(5) · `Preview`(8) | 같음 |
| 3 | POST rooms/direct | `{accountId: StrictInt}` → Room | `chatOpenDirect({'accountId'})` | 같음 |
| 4 | POST rooms | `{accountIds, title?}` → Room | `chatCreateGroup`(빈 제목은 안 보냄 · 서버도 빈 = null) | 같음 |
| 5 | POST rooms/{id}/members | `{accountIds}`(1명 이상) → Room | `chatAddMembers` | 같음 |
| 6 | POST …/leave | `{ok}` | `chatLeave` | 같음 |
| 7 | POST …/hide | `{ok}` | `chatHide` | 같음 |
| 8 | PUT …/mute | `{muted: StrictBool}` → `{ok, muted}` | `chatMute` PUT `{'muted'}` | 같음 |
| 9 | GET …/messages | `before · since · limit(1~50)` → `{items:[Message], hasMore}` · Message 10키 · sender 4키 · photo 3키 | `chatMessages`(`Uri(queryParameters:)`) → `ChatMessage.fromJson`(10 · 4 · 3) | 같음 |
| 10 | POST …/messages | `{clientId, text?}` \| `{clientId, photoId}` → Message | `chatSend`(null 키는 빠짐 · 사진이면 `text` 안 보냄 `chat_state.dart:494`) | 같음 |
| 11 | DELETE messages/{id} | `{ok}` | `chatDelete` | 같음(뒤처리 = FAIL-1) |
| 12 | POST …/read | `{messageId ≥ 0}` → `{ok, lastViewedAt, lastReadMessageId, unreadRooms}` | `chatRead` · `unreadRooms` 읽음 | 같음 |
| 13 | POST photos | multipart `roomId · photo · width · height` → `{photoId}` | `chatUploadPhoto` `StreamedRequest`(진행률 · 40초 · 같은 네 칸) | 같음 |
| 14 | GET photos/{id} | `image/jpeg` · `no-store` · Bearer | `chatPhoto` Bearer 헤더 · `bodyBytes` | 같음 |

오류 코드: back 14 새 코드 + 재사용 4 — 앱은 `{error:{code,message}}` 의 `message` 를 토스트(4xx) · 401 로그아웃(`chat_state.dart:498-509`) = §10.5 · OQ-934.

**SSE 5 / 5 일치**

| 이벤트 | back 페이로드 | app 소비(`chat_state.dart:357-385` · 파서 `board_stream.dart` `otherEvents`) | 결과 |
|---|---|---|---|
| `chat_message` | `{roomId, message}` | `data['message']` → `ChatMessage`(roomId 는 메시지 안 값) | 같음 |
| `chat_message_deleted` | `{roomId, messageId, updatedAt}` | 세 키 모두 | 같음 |
| `chat_room` | `{room}`(받는 계정 기준) | `Room.fromJson(data['room'])` | 같음 |
| `chat_room_removed` | `{roomId}` | `roomId` | 같음 |
| `chat_read` | `{roomId, lastViewedAt, lastReadMessageId, unreadRooms}` | `roomId` · `lastReadMessageId`(배지는 로컬 목록으로 다시 셈 — 같은 집합이라 같은 값) | 같음 |

**푸시 payload 6 / 6 키 일치** — back `push.py` `chat_message()`: `{aps:{alert:{title, body}, sound:"default", "thread-id":"chat-<roomId>"}, kind:"chat", roomId, messageId}` · `category` · `badge` 없음 · 만료 +86400 / app: `AppDelegate.swift` `willPresent` 가 `kind · roomId · messageId` + `content.title · body` 를 넘김 · 누름 키 목록에 `roomId · messageId` 더함 · `push.dart` `PushKind.chat`(roomId 없으면 버림) · 앞 = `onChatForeground` → 앱 안 배너(눌러 열기 아님) · 누름 = 채팅 탭 그 방 · 알림 읽음 호출 없음.

## §0 W2-1 ~ W2-6

| # | 처분 | 판정 | 근거 |
|---|---|---|---|
| W2-1 · D-45 | 만들기 · 처음 추가 · 다시 초대 = 그 순간 마지막 id | PASS | `service/chat.py:147-156` `_join` · 시험 `test_chat_new_member_unread_zero` |
| W2-2 | 빈 방 since 없음 · read 0 = 200 안 바꿈 | PASS | 서버 `service/chat.py:399-408` · 앱 `chat_state.dart:261`(받은 것 없으면 `loadLatest`) · `:326`(0 이면 read 안 보냄) · 시험 `test_chat_empty_room` |
| W2-3 | 예약 상세 실제 호출 자리 · 실제 화면 push | PASS | `qr_show_screen.dart` · `scan_screen.dart` 두 함수가 `whileDisplayScreen` · 시험 `chat_app3_test.dart:204-242` 실제 `ReservationDetailScreen` |
| W2-4 | 루트 위 화면에서는 배너 안 보여도 됨 | PASS | 셸 안 층 + `RootRoutes` 로 보고 있는 방도 아님 |
| W2-5 | `flutter_image_compress` | PASS | `pubspec.yaml:46` · `photo_pick.dart:64-65` `CompressFormat.jpeg` |
| W2-6 | 라우트 핸들러 `def` grep = 0 | PASS | 실행 결과 0 |

## 시안 24 장면 → 화면 코드 (헤더 = D-38)

24 / 24 자리 있음(구조 · 문구 대조 — 픽셀 비교는 코디 시뮬레이터 스크린샷 몫).

| 장면 | 코드 |
|---|---|
| S1 · S2 | `chat_list_screen.dart` — `TabScaffold(tab: AppTab.chat)` = `AppHeader` [Céramique][채팅][종] → 제목 없는 [새 대화] 줄 → `RoomRow`(`chat_ui.dart:24-84`) · 빈 안내 문구 시안과 같음 |
| S3a ~ S3c | `chat_new_screen.dart` — [대화 시작] / [만들기] · 그룹 이름 · 안내 줄 · 19명 상한 · 검색 「찾는 직원이 없어요」 · 칩 = `StatusChip`(+ `onRemove` ✕) |
| S4 · S5 | `chat_room_screen.dart` — 폰 `DetailHeader(back: '채팅', titleWidget: 이름 + 역할 Badge / N명)` · 날짜 구분선 · 시스템 줄 · 연달아 이름 숨김(`chat_view.dart:80-85`) · 입력 `RuneLimitFormatter`(코드 포인트 2000) · 비활성 1:1 안내 |
| S6 | `_pendingRow` 「보내는 중…」 · 빨간 ! · 「보내지 못했어요」 · [다시 보내기] |
| S7a · S7b · S8 | `chat_photo_screen.dart` 시트(1장씩) · 「올리는 중 N%」 + `MsProgress` · 크게 보기(검정 · 닫기 · 보낸 사람 · 시각 · 버튼 없음) |
| S9a · S9b | `_deleteMenu`(내 것만 · 말풍선 떠오름 · [삭제]) · `confirmChat` 문구 시안과 같음 |
| S10a ~ S10e | `chat_info_screen.dart` — 그룹 이름 · 알림 `SwitchRow`(= `Switch.adaptive` · 설정과 공용) · 참여자(「나」 맨 위) · [+ 참여자 추가](이미 참여 중 = `MiniChip`) · [나가기] 확인 · 1:1 안내 · [목록에서 숨기기] |
| S11 · S13d | `shell.dart` `ChatBannerLayer` — 폰 위 · 아이패드 위 가운데 520 · [보기] · 4초 |
| S12 | iOS 시스템(payload 만) |
| S13a ~ S13c | 아이패드 — 같은 `AppHeader` · 목록 칸 360 위 [새 대화] · 대화 칸 `DetailHeader(back: null)` · 「왼쪽에서 대화를 골라 주세요」 · 방 정보 = `showRightSheet` 420 |

## 기능 독립 · 회귀

- 바뀐 파일은 모두 `procedure/back/**` · `procedure/app/**` — 다른 기능 폴더 · 레포 루트 · `procedure/front` 변경 0(`git status`) → PASS
- import: back 새 파일은 `app.*` + 표준 · fastapi · pydantic · starlette 만 · app 새 파일은 상대 경로 + `flutter` · `image_picker` · `flutter_image_compress` 만 → procedure 밖 import 0 → PASS
- 회귀: 원장 · 상담사 호출 · 띄우기 푸시 = 만료 0 그대로(apns 기본값 0 · `Delivery.expiration` 기본 0) · 알림 목록 종류 둘 그대로 · 여권 사진 multipart 한도 = 같은 전역 값(주석만 더함 `api/photos.py:21`) · `showQrScreen` · `showPassportScan` 은 감싸기만(반환 그대로) · 설정 `_SwitchRow` → 공용 `SwitchRow`(같은 꼴) · `StatusChip` 선택 인자만 더함 · 기존 시험 파일 수정 0 · pytest 500 · flutter test 184 통과(코디 확인값) → PASS

## 참고 (기존 부채 · 정리할 것)

- `procedure/app/ios/Runner.xcworkspace/xcshareddata/swiftpm/` · `Runner.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/` 미추적 — `flutter_image_compress` iOS 가 SwiftPM 으로 끌어온 SDWebImage · libwebp `Package.resolved`(+ `configuration`). 커밋해 재현 빌드를 고정할지 코디가 정한다(내용은 공개 패키지 버전뿐 · 비밀 없음). SDWebImage 는 인코더로만 쓰이고 이미지 로딩 · 디스크 캐시 경로로는 안 쓰인다(D9-24 영향 없음)
- WP-REVIEW 문구의 `grep -n "^def "` 는 W2-6 이전 문구 — WORK-011 을 W2-6 명령으로 고치면 다음 리뷰에서 거짓 FAIL 이 안 난다(planner 몫)
- `main.dart:62` 주석 「공통 틀(탭 4)」 · `shell.dart` `TabScaffold` 주석은 고쳐짐 — `_Home` 주석 한 줄만 낡음(코드 영향 없음)
