# 리뷰 리포트 — internal-chat / doc r5 (2026-10-29)

대상: SPEC-007 0.5.0 `(r5)` · WORK-011 r5(BE5 ∥ APP7) · `spec-r5-report.md` · DEC-009 D-67 ~ D-69
코드 기준: 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` `git rev-parse --short HEAD` = **`3ed1089`**(읽기만 · 미커밋 변경 0)
OQ-962 ~ 969 = 코디 기본값으로 받음(브리프) → FAIL 대상 아님

## 판정: FAIL (1건 — 한 줄로 고칠 수 있음)

| 대조 | 결과 |
|---|---|
| D-69 읽기 길 V1 ~ V12 (`3ed1089` 직접) | 12 / 12 자리 있음 · **V10(푸시) 근거가 틀림 → F-1** |
| §12.4 전수 grep G1 ~ G10 수 | 10 / 10 같음(7 · 23 · 9 · 19 · 3 · 14 · 4 · 8 · 5 · 8) |
| §12.4 R5-B1 ~ B17 · R5-A1 ~ A10 · W1 줄 번호 | 전부 확인 — 어긋남 0(아래 「§12.4 확인」) |
| #20 모아보기(모양 · 페이지 · 정렬 · 권한 · D-69 · 화면) | PASS(W-3 하나) |
| D-68 초대 — 1:1 [초대] = #4 그대로 | PASS — `create_group` 동작으로 다 됨(아래 3) |
| 처분 4문서 동기(부록 D.4 ~ D.7 = 7 + 2 + 1 + 4) | 14 / 14 들어감 |
| public grep(SPEC-007 · WORK-011) | 0 |

## FAIL

### F-1 푸시 본문이 D-69 경계를 넘을 수 있다 — V10 「안 바꿈」 근거가 푸시에서는 성립하지 않음
- **자리**: SPEC-007 §4.6 V10(`spec-007-internal-chat.md:313`) · §12.4 R5-B14(`spec-007:959` 「`push.py:167-221` … **안 바꿈** — 새 메시지 id 는 모든 지금 멤버의 경계보다 큼」) · §7 `chat_message` 줄(「새 메시지는 늘 … 경계 뒤라 거르지 않는다」)
- **근거(코드 `3ed1089`)**:
  - SSE `chat_message` 는 받는 사람을 **보내기 트랜잭션 안에서** 정한다(`service/chat.py:352` `members = tx.chat_members(room_id)` → `:368`) → V10 말이 맞다
  - 그러나 푸시는 **커밋 뒤 이벤트 루프 태스크**로 돌고(`push.py:239` `loop.create_task(self._notify(...))` → `:272` `prepare()`), 받는 사람을 **그때 다시 읽는다**(`push.py:174-181` `tx.chat_message(message_id)` · `members = tx.chat_members(room["id"])` — 지금 멤버 전원). 그 사이에 다른 요청(초대 #5 · 다시 초대 · 1:1 [초대]는 새 방이라 무관)이 먼저 처리될 수 있다(핸들러는 `async def` · 서비스는 동기라 요청은 한 번에 하나지만, 태스크는 다음 루프 차례)
  - 순서: A 가 그룹에 글 M 보냄(커밋 · 푸시 태스크 예약) → 태스크보다 먼저 B 초대(B `from_message_id` = M.id 이상) → 푸시 태스크가 멤버를 다시 읽음 → **B 기기에 M 의 제목 · 본문 앞 100자(`chat_body`) 푸시** → B 는 앱에서 M 을 못 본다(D-69 위반 · 잠금 화면에 남음). 다시 초대(나갔다 온 사람)도 같다
- **왜 FAIL**: 브리프 볼 것 1 「빠진 길(푸시 본문 …)」. SPEC 이 「안 바꿈」으로 적어 코드 워커는 `push.py` 를 건드리지 않는다 → 시험(§13.1 r5 SSE 줄)도 푸시를 안 본다 = 조용히 통과
- **고칠 것(제안)**: R5-B14 의 `push.py` 부분을 「바뀜」으로 — `chat_message` 의 `to` 에 `r["from_message_id"] < m["id"]` 한 조건(지금 멤버 · 안 끔 · 활성 조건 옆). §4.6 V10 · §7 은 「SSE = 안 바꿈(tx 안에서 받는 사람) · 푸시 = 받는 사람을 커밋 뒤 다시 읽으므로 경계 조건 더함」으로 나눠 적는다. §13.1 r5 에 한 줄: 「A 글 M(푸시 태스크 아직) → B 초대 → `PushService.chat_message(M)` 받는 사람에 B 없음」(가짜 APNs · 태스크 대신 `chat_message(mid)` 를 바로 불러 단언). §12.4 R5-B14 를 R5-B14a(SSE 안 바꿈) · R5-B14b(푸시 바뀜)로

## WARN

### W-1 옛 DB 채우기 뒤 `last_read_message_id ≥ from_message_id` 를 시험이 안 본다
- 자리: §3 r5 `_backfill_chat_from`(`spec-007:161`) · §13.1 「안 읽음 불변식 (r5)」(「모든 길 … 뒤」 — 채우기는 목록에 없음)
- 근거: §4.6 「안 읽음 · 읽음」은 V4 를 **이 불변식 하나**로 「안 바꿈」 처리한다. 새 행은 `_join` 이 같은 값을 넣어 성립하지만, 옛 행은 채우기 SQL(`created_at < joined_at` 의 MAX id)과 옛 `last_read_message_id` 가 따로 정해진다. 1판 이후 `_join`(`3ed1089` `service/chat.py:160-169`)이 늘 들어올 때 마지막 id 를 넣었으므로 지금 데이터로는 성립할 것으로 보이나, 깨지면 안 읽음 배지가 보이지 않는 메시지를 센다(사용자 표면)
- 권장: §13.1 「옛 DB (r5)」 줄에 「채운 뒤 모든 행 `last_read_message_id ≥ from_message_id`」 단언 한 줄(또는 채우기에서 `last_read_message_id = MAX(last_read_message_id, from_message_id)`)

### W-2 나가기 문구 옛 단언 시험이 G10 · R5-A9 목록 밖
- 자리: §12.4 G10(`grep "초대했어요\|참여자 추가"`) · R5-A9
- 근거: `app/test/chat_app3_test.dart:446` `expect(find.text('내 목록에서 이 방이 사라져요. 다시 초대받으면 다시 볼 수 있어요.'), findsOneWidget)` — G10 패턴에 안 걸린다. R5-A2 를 고치면 빨갛게 깨지므로 조용히 통과는 아님
- 권장: R5-A9 에 `chat_app3_test.dart:446` 추가 · G10 에 `다시 초대받으면` 더함

### W-3 아이패드 모아보기 = 「방 정보 시트 안 다음 화면」 의 길이 안 적힘
- 자리: §10.16 「틀」 · R5-A6
- 근거: 아이패드 방 정보는 `showRightSheet`(`app/lib/chat/chat_ui.dart:151` · `useRootNavigator: true` · `showGeneralDialog`)로 열리고(`chat_room_screen.dart:187`) 시트 안에 Navigator 가 없다. 「[‹ 방 정보]로 돌아감」을 하려면 시트 안 Navigator 를 새로 두거나 `ChatInfoScreen` 안 상태로 화면을 바꿔야 한다 — 어느 쪽이든 되지만 SPEC 이 고르지 않았다. 지금 시트 머리는 `back: sheet ? '닫기' : '대화'`(`chat_info_screen.dart:67`)
- 권장: 「워커 선택(시트 안 `Navigator` 또는 `ChatInfoScreen` 안 상태 교체) · 머리 왼쪽 = 「‹ 방 정보」」 한 줄

### W-4 나간 사이 꺼져 있던 다른 기기 — 열린 대화의 옛 메시지가 메모리에 남음
- 자리: §4.6 「다시 초대」 · R5-A8(「`chat_room_removed` 처리로 메모리 지움 — 안 바꿈」)
- 근거: R5-A8 은 그 기기가 SSE 로 `chat_room_removed` 를 받는 경우만이다. 같은 계정 기기 2 가 **그 방 대화를 연 채** 연결이 끊긴 동안 기기 1 에서 나가기 → 다시 초대되면, 기기 2 의 `catchUp`(`app/lib/chat/chat_state.dart:262-289`)은 열린 방을 `since` 로 메우기만 해(`:276-283` `merge`) 옛 메시지(id ≤ 경계)가 화면에 남는다. 열려 있지 않은 방은 `t.reset()`(`:266-268`)이라 괜찮다. 드문 경우이고 이미 본 내용이지만 C23 실기기에서 만날 수 있다
- 권장: 「경계 밖으로 밀린 메시지는 앱이 버린다」 같은 규칙을 둘지는 코디 판단 — 최소한 §4.6 에 「알려진 한계」 한 줄

## 볼 것별 결과

### 1. D-69 읽기 길 V1 ~ V12 — `3ed1089` 직접 전수
| V | 코드에서 본 자리 | 판정 |
|---|---|---|
| V1 · V2 | `repo.py:746-761` `chat_messages`(방 조건만) · `service/chat.py:332` — `id > ?` 를 더하면 `limit+1` 꼴로 `hasMore:false` 가 자연히 남 | PASS |
| V3 | `_room` `service/chat.py:122-129` `last_chat_message` 그대로 미리보기 · `_room_events :154` 는 받는 사람마다 `_room` → R5-B4 로 충분 | PASS |
| V4 | `chat_unread` `repo.py:763-767` (`id > last_read`) · `_join :167-169` 가 같은 값으로 시작 · `read :570-573` `max` | PASS(W-1) |
| V5 | `_attachment :616-625` — #14 · #17 · #18 셋 다 이 함수 | PASS |
| V6 | `forward :430-434`(`lock_write` 뒤) · 원본 첨부 `:440` 은 그 뒤 | PASS |
| V7 | 새 #20 | PASS |
| V8 | `delete :505-508` · `edit :542-545` — 404 를 403 · 400 · 「이미 지움 return」 · 「같은 글 return」 보다 먼저 두면 됨(SPEC 그대로) | PASS |
| V9 | `delete :518` · `edit :555` `members` → `:527` · `:557` | PASS |
| **V10** | SSE `:352` → `:368` = tx 안 · **푸시 `push.py:174-181` = 커밋 뒤 다시 읽음** | **FAIL → F-1** |
| V11 | `chat_message_by_client :390` · `:469` — `account_id = actor` | PASS |
| V12 | `read` · `rooms` · `hide` · `mute` · `leave` · `open_direct` — 본문 없음(`chat_room` 은 V3 로 거름) | PASS |
| 그 밖 | 검색 = 앱 안 이름 검색만(`chat_search.dart` — 메시지 검색 없음) · 알림 목록 = 채팅 안 들어감(D9-30 · `notifications.py KINDS`) · 썸네일 = V5 · 업로드 전 첨부(`message_id` null)는 올린 사람만 = 경계 무관 | 빠진 길 없음 |

`from_message_id` 정의: 만들 때(`create_group :239-240` · `_open_direct :201-202`) · 처음 추가 · 다시 초대(`add_members :265-266`) 모두 `_join` 한 곳(`:160-169`) → R5-B2 한 자리로 전부 됨. 옛 DB 채우기: 새 DB 는 `CREATE TABLE` 에 열이 있어 `MIGRATIONS` 루프(`db.py:259-262`)가 더하지 않음 → 채우기 안 부름 · 옛 DB 만 부름 — 「열이 새로 생길 때만」이 지금 루프 꼴로 구현 가능. 시각 열 = 둘 다 `to_db_ms` 폭 → `created_at < joined_at` 문자열 비교 성립. 같은 밀리초: 새 행 = id 로 정확 · 옛 행 = 같은 밀리초 보임(SPEC 에 명시 · OQ-962). **구현 가능하게 적혔다.**

### 2. #20 모아보기
- 모양 `MessageList`(`schemas/chat.py:125`) 재사용 · 커서 = 메시지 id · `ORDER BY m.id DESC` · `limit` 1 ~ 60 — 기존 #9 꼴 `Query(PAGE, ge=1, le=PAGE)`(`api/chat.py:92-93`)로 범위 밖 = `invalid_request` · 권한 = `_member`(404 `chat_room_not_found`) · 경계 `m.id > ?` · 전달본 = 대상 방 새 행이라 `JOIN` 으로 그대로 나옴 → PASS
- 화면 §10.16: 틀 · 격자 · 읽기 · 빈 상태 · 누르면 · 메뉴 없음 · 저장 없음 · SSE 반영 · 보고 있는 방 · 나감 다 있음 → PASS(아이패드 길 = W-3)

### 3. D-68 초대
- 1:1 [초대] = #4: `create_group`(`service/chat.py:224-248`) — `accountIds` = [상대, …고른] ≥ 2(`GROUP_MIN`) · ≤ 19 · 비활성 상대 = `candidate` 실패 400 `chat_person_invalid` · 1:1 방 안 건드림 · 매번 `add_chat_room` 새 방(같은 묶음이어도) → **새 경로 없이 됨**. 시스템 줄은 R5-B5 로 `create_group` 에 더함(`add_members :273-275` 꼴 SSE)
- 앱: `_cap`(`chat_new_screen.dart:38`) = 20 − `memberCount`(1:1 = 2) = 18 그대로 · `_members` 에 상대가 들어 「이미 참여 중」 그대로 · `_submit :80-94` 분기만 더함 → R5-A3 대로 됨. 문구 바뀜 시험 = §13.1 「초대 문구 · 그룹 만들기 줄」 · §13.2 r5 · C22. 앱 쪽 글자 자리 = G6 앱 11줄 전부 R5-A1 ~ A3 · 주석으로 분류(W-2 시험 1줄만 빠짐)
- 옛 「초대했어요」 행 = 그대로(OQ-964) · 앱은 시스템 줄 본문을 그대로 그림(문구 파싱 없음 — `grep "초대" app/lib` 에 판단 코드 0)

### 4. 처분 4문서 동기
- `r4-dispositions.md` 7줄 → 부록 D.4 7 · §15 OQ-959 · 960 · 961 「닫힘」(`spec-007:1143-1145`)
- `app-fix-r4`(W3-1 · W3-3) → §10.0 「공용 바텀 시트」(`:541` · `showAppSheet` = `3ed1089` `app/lib/widgets/sheet.dart:13` 확인) · §10.14
- `be-fix-r4`(W3-2) → §5 「전달」 ① · §13.1 「전달 — 잠금」(코드 `service/chat.py:430` `lock_write` 확인)
- `app-fix-r5`(F10) → §10.0 「머리 · 줄 정렬」 · 부록 D.7 4줄
→ 14 / 14 PASS

### 5. §12.4 확인(`3ed1089` grep)
- G1 ~ G10 수 10 / 10 같음
- 줄: `db.py:202` · `:233-246` · `:259-263` · `:282` / `repo.py:731` · `:735` · `:742-744` · `:746-761` · `:763-767` · `:773` · `:781` / `service/chat.py:109` · `:111-136`(`:122`) · `:134` · `:144-145` · `:147-150` · `:152-154` · `:160-169` · `:162` · `:224-248` · `:268` · `:273` · `:275` · `:293` · `:296` · `:320-334`(`:332`) · `:344-369`(`:366` · `:368`) · `:390` · `:394` · `:409-495`(`:431-434` · `:440`) · `:469` · `:497-527`(`:505-508` · `:514` · `:527`) · `:529-558`(`:542-545` · `:554` · `:557`) · `:571` · `:579` · `:610-629`(`:616`) / `push.py:174` · `:224` · `:227` / `test_order.py:248-279` · `test_chat.py:136-137` / `chat_info_screen.dart:32-44` · `:48` · `:88-91` · `:97` · `:125` / `chat_new_screen.dart:19-20` · `:35-38` · `:71` · `:75` · `:80-94` · `:110` / `chat_list_screen.dart:88-94` / `chat_state.dart:186-197` · `:192` · `:385-390` · `:436` · `:490-494` · `:671-672` / `api.dart:217` · `:223-231` / `board_stream.dart:158` / `api/chat.py:91-96` / `schemas/chat.py:125` / `front/lib/hooks.ts:77` — 어긋남 0
- 빠진 자리: `push.py:174-181` 받는 사람(F-1) · `chat_app3_test.dart:446`(W-2)

### WORK-011 r5
BE5 ∥ APP7 병렬 근거(계약 고정점 r5 4줄) · 대상 파일 · 완료 조건(C1 ~ C23 실기기 = 사용자 표면) · SIM3 옛 볼륨 채우기 확인 · infra 변경 없음(열 = 부팅 MIGRATIONS · 새 env · 경로 0) · 빌드 13 호환(빈 `lastMessage` 는 기존에도 있던 꼴) — SPEC 과 맞음. F-1 을 고치면 WP-BE5 대상 파일에 `back/app/service/push.py` 와 시험 한 줄을 더한다.

## 고객이 실물에서 만날 자리
- F-1: 초대된 직원 잠금 화면에 들어오기 전 대화 한 줄이 푸시로 뜸(앱에는 없음) — 초대와 글이 거의 동시일 때
- W-4: 두 번째 기기에 옛 대화가 남아 보임(나가기 · 다시 초대 사이 그 기기가 꺼져 있고 대화를 연 채였을 때)
- W-1: 옛 DB 에서 안 읽음 배지가 보이지 않는 메시지를 세는 경우(불변식이 깨졌을 때만)

## 조용히 통과하는 자리
- F-1: §13.1 r5 SSE 시험은 초록인데 푸시 경계는 아무 시험도 안 봄

## 사용자 판단 후보
없음(OQ-962 ~ 969 는 코디 기본값으로 받음. W-4 는 코디 판단 범위)

## 참고(기존 부채)
- `scripts/lint-pipeline.py` 이 워크트리에 없음(planner 리포트와 같음 · r3 · r4 부터)

```text
$ git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short
 M orchestration/config/projects/cc-prototype.json
 M para/projects/summer-star/cc-prototype/00-baseline/README.md
 M para/projects/summer-star/cc-prototype/10-decision/README.md
 M para/projects/summer-star/cc-prototype/20-spec/README.md
 M para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md
 M para/projects/summer-star/cc-prototype/30-work/README.md
 M para/projects/summer-star/cc-prototype/deploy.md
 M para/projects/summer-star/cc-prototype/log.md
?? orchestration/roles/cc-prototype/designer/
?? orchestration/work/internal-chat/
?? para/projects/summer-star/cc-prototype/00-baseline/baseline-010-internal-chat.md
?? para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md
?? para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md
?? para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md
```
(이 판에서 만든 파일 = `orchestration/work/internal-chat/review-doc-r5.md` 하나 — 미추적 폴더 안)
