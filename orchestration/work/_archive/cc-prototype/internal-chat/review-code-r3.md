# 리뷰 리포트 — internal-chat / code r3 (2026-10-29)

대상: `kknaksss/internal-chat-forward` · `git diff a6c4123` 미커밋 변경(back BE4 · app APP6) — 18 파일 수정 · 6 새 파일
SSOT: `r4-dispositions.md`(이김) → SPEC-007 0.4.0 `(r4)` · WORK-011 WP-REVIEW3 · DEC-009 D-62 ~ D-66 → `review-doc-r4.md` 「조용히 통과하는 자리」

## 판정: WARN (FAIL 0 · WARN 3)

읽기용으로 돌린 것: `uv run pytest -q tests/test_chat_r4.py` = 6 passed · `flutter test test/chat_app6_test.dart test/interpret_drawer_test.dart` = 17 passed. 전체 수치(pytest 521 · 경로 70 · test 229)는 코디 확인값을 그대로 받았다(다시 돌리지 않음).

## FAIL

없음.

## WARN

### W3-1 폰 전달 시트 머리(손잡이 · [✕] · [전송])가 상태 표시줄 밑으로 들어간다 — F9 와 같은 꼴
- `app/lib/screens/chat_forward_sheet.dart:40-48` — `showModalBottomSheet`(기본 `useRootNavigator: false` → **채팅 탭 Navigator**, 곧 탭바 위 칸)에 `SizedBox(height: MediaQuery.sizeOf(ctx).height * 0.88)`를 넣었다. 높이를 **화면 전체** 기준으로 잡고 `SafeArea(top: false)`라서, 시트 위가 상태 표시줄 아래에 머문다는 보장이 없다.
  - 키보드 닫힘 · iPhone 15 꼴(852 · 상태 표시줄 59 · 탭바 약 82): 시트 0.88×852 ≈ 750 · 칸 ≈ 770 → 시트 위 y ≈ 20. 손잡이가 Dynamic Island 밑에 있고 머리 줄도 일부 걸친다.
  - **검색칸을 누르면**(키보드 열림 · `shell.dart:139-147` 이 탭바를 숨기고 본문을 키보드만큼 줄임): 칸 ≈ 852 − 336 = 516 < 750. 시트가 칸 전체로 잘려 **위 y = 0**에 붙는다 → [✕] 「공유」 [전송 N] 줄이 상태 표시줄 · 노치와 겹친다. 사용자는 검색 중에 [전송]을 누르러 손이 가는데, 그 자리가 노치 밑이다.
- 근거: SPEC-007 §10.14 「틀」(폰 = 바텀 시트 · 손잡이 · 머리 [✕] 「공유」 [전송]) · §10.15 · D9-65(F9 — 「높이를 화면 전체로 잡아 탭 본문보다 커져 머리가 상태 표시줄 밑」, 같은 판에서 드로어만 고침).
- 조용히 통과: `chat_app6_test.dart` 는 기본 시험 화면(상태 표시줄 0 · 탭바 없음 · 키보드 없음)이라 잡지 못한다. `interpret_drawer_test.dart:76` 처럼 상태 표시줄 · 탭바 칸 · (키보드) 를 넣은 시험이 없다.
- 고칠 꼴(제안): 드로어와 같이 놓인 칸 기준(LayoutBuilder · `min(칸 × 0.88, 칸 − 위 padding)`) 또는 `useSafeArea: true` · 키보드 열림 시험 1개.

### W3-2 D-66 셈은 맞지만 「전달 ↔ 마지막 참조 삭제」가 동시에 오면 깨진 전달본이 생긴다
- `back/app/service/chat.py:436-442` — 전달이 원본 첨부 행(`deleted_at`)과 파일(`is_file`)을 확인하는 SELECT 는 **쓰기 잠금을 잡기 전**에 돈다. Python `sqlite3` 기본(`db.py:269` · isolation 기본)은 INSERT/UPDATE 바로 앞에서만 `BEGIN`(DEFERRED)을 걸고, journal 은 WAL 이 아니다(grep 0). 그래서 첫 쓰기(`:473` `add_chat_photo` 또는 사람 대상 `_open_direct`) 전까지는 확인이 커밋된 남의 쓰기와 직렬화되지 않는다.
- 이렇게 깨진다: ① B 가 원본(작성자 A)을 전달 — 첨부 행 살아 있음 · 파일 있음 확인 ② 그 사이 A 가 같은 메시지를 지움 — `delete` tx 에서 셈 = 0(`:513`) → 커밋 → 파일 unlink(`:515-520`) ③ B 의 전달 tx 가 같은 `file_name` 새 행을 넣고 커밋. 결과: 전달본 메시지는 있는데 파일이 없다(사진 · 동영상 열기 404 · 그 뒤 그 전달본을 다시 전달하면 `chat_not_forwardable`).
- 두 삭제가 동시에 오는 경우(같은 파일 마지막 참조 둘)는 안전하다: `delete` 는 UPDATE(쓰기 잠금) 뒤에 셈해 직렬화된다 → 파일이 남아 새는 일도 없다. 썸네일은 `file_name` 셈 하나로 본 파일과 같이 움직이고, 동영상 전달본 시험(`test_chat_forward_attachments_delete` — 본 파일 + 썸네일 둘 다 남음 · 다 지우면 0)이 있다.
- 근거: r4 처분 D-66(「tx 안에서 남은 참조 셈 · tx 밖 unlink」) · SPEC §5 「전달」 ①(첨부 행 지움 · 파일 없음 = 400). 창은 ms 단위라 실물에서 드물다 → WARN.
- 고칠 꼴(제안): 전달 tx 첫머리에서 쓰기 잠금을 먼저 잡거나(`BEGIN IMMEDIATE`), 첫 쓰기 뒤에 `src["deleted_at"]`를 다시 읽어 지워졌으면 `chat_not_forwardable`.

### W3-3 [전송] 뒤 응답을 기다리는 동안 시트를 닫을 수 있다 — 닫으면 결과를 알 수 없다
- `chat_forward_sheet.dart:188` [✕] 는 `_sending` 중에도 켜져 있고, 바텀 시트 끌어 내리기 · 바깥 누름도 그대로다. 닫으면 `:132` `if (!mounted) return;` 이라 토스트(「보냈어요」 · 「N곳에 보내지 못했어요」 · 「보내지 못했어요」)가 하나도 안 뜬다. 서버는 이미 보냈을 수 있다.
- 근거: SPEC-007 §10.14 「[전송]」 — 「누르면 [전송] 자리에 도는 표시 · **시트는 응답까지 열려 있다**」 · 처분 OQ-959(결과마다 토스트).
- 고칠 꼴(제안): 보내는 중에는 [✕] 끔 · `enableDrag` · `isDismissible` 끔(아이패드 `barrierDismissible`도), 또는 닫혀도 토스트는 띄움.

## 항목별 대조 (WP-REVIEW3 · 코디 「볼 것」)

| 항목 | 판정 | 근거 |
|---|---|---|
| #19 요청 모양 back ↔ app | PASS | back `schemas/chat.py` `ForwardTarget{roomId?, accountId?, clientId 8~64}` · 둘 중 하나 · 모르는 키 400(`_Req`) ↔ app `chat_model.dart` `ForwardTarget.room/person` `toJson` = `{roomId?, accountId?, clientId}` |
| #19 결과 모양 | PASS | back `ForwardOk{ok:true, roomId, message}` / `ForwardFail{ok:false, roomId\|null, error{code, message}}` · 대상 차례 그대로 ↔ app `ForwardResult.fromJson`(ok · roomId · message · error.code · error.message) · 시트가 `results[i]` ↔ `picks[i]` 차례로 짝지음 |
| 오류 차례(처분 W-4) | PASS | 401 → 400(pydantic 모양 · 0 · 11 · 같은 roomId/accountId/clientId) → 404 `chat_message_not_found`(없음 · 지금 멤버 아님 · 나간 사람) → 400 `chat_not_forwardable`(시스템 · 지움 · 첨부 행 · 파일) · 409 `photo_disabled` — 시험 `test_chat_forward_auth_shape`(「모양 400 이 404 보다 먼저」 포함) |
| 대상별 실패 = 200 + 결과 | PASS | `DomainError` 를 대상마다 잡음 · 비활성 1:1 = 그것만 409 · 멤버 아님 404 · 후보 아님 400 — 실패 대상은 쓰기 전에 걸러짐(부분 쓰기 없음) |
| 같은 방 두 번 = 1개(§5 ⑤) | PASS | `done[room_id]` — 1:1 방 + 그 사람 → 뒤 대상은 같은 결과 · 앱은 키 `p:<id>` 로 애초에 하나로 합침 |
| clientId 다시 보내기(D9-16) | PASS | back 대상마다 `chat_message_by_client` → 처음 것(SSE · 푸시 없음) · app `_clientIds.putIfAbsent(key)` — 네트워크 실패 · 일부 실패 뒤 다시 [전송] = 같은 clientId(시험 있음) |
| SSE · 푸시 · async def | PASS | `forward_message` `async def` · 커밋 뒤 `_emit` + 만든 것만 `push` · 시험이 HTTP 경로로(조용히 통과 #3 막힘) · 라우트 def 0 = 19개 모두 async(`test_chat_r3.py:498`) |
| 경로 70 | PASS | `test_route_count_70`(HTTP 69 + WS 1 · 채팅 19) |
| D-66 셈 · tx 경계 · 썸네일 | PASS + W3-2 | 셈 tx 안(`:513`) · unlink 커밋 뒤(`:515`) · 동영상 전달본 시험(조용히 통과 #1 막힘) · 동시 전달 경합 = W3-2 |
| 인덱스(옛 DB) | PASS | `db.py` `CREATE INDEX IF NOT EXISTS chat_photo_file` · `test_chat_forward_index_migration` |
| 전달 시트 OQ-959 | PASS(+W3-3) | 전부 됨 = 닫힘 「보냈어요」 · 일부 실패 = 시트 남김 · 실패한 곳만 고른 채 · 성공 고름 풂 · 「N곳에 보내지 못했어요」 · 전부 실패 = 닫힘 + 첫 문구 · 4xx = 닫힘 + message · 네트워크 · 5xx = 남김 |
| OQ-960 같은 사람 한 번 | PASS | [전체] = 1:1 방이 있는 직원은 「직원」에서 숨김(`:179`) · [사람] = 직원 한 번씩 · 1:1 있으면 `ForwardTarget.room` |
| OQ-961 초성 세 곳 | PASS | `chat_search.dart` `nameMatches` 하나 — 전달 시트(방 · 사람) · `ChatPeopleScreen`(새 대화 · `addTo` 참여자 추가 같은 화면) · 겹자음 · 이어지는 자리 · 대소문자 · 공백 시험 |
| 비활성 1:1 | PASS | `forwardRooms` = 방 − `peerInactive` · 직원 목록은 active 만(#1) · 서버도 대상별 409 |
| 10곳 | PASS | 찬 뒤 흐림 0.35 + 토스트 「한 번에 10곳까지 보낼 수 있어요」 · 서버 11 이상 400 |
| 아이패드 | PASS | `isTabletWidth` → 가운데 `Dialog`(최대 520 × 화면 0.8) · 시험 있음 |
| W-5 FakeChat `/forward` | PASS | `chat_fixture.dart` 에 자리 더함 — 본문(차례 · 대상마다 clientId · 같은 clientId)을 진짜 요청에서 단언(조용히 통과 #2 막힘) |
| share_plus 걷어냄 | PASS | pubspec · lock · `chat_share.dart` · `chatVideoDownload` · 임시 파일 코드 0(grep · lib/test/ios) · 링크 열기는 `chat_link.dart` 로 옮겨 그대로 · grep 시험 있음 |
| 1판 · 2판 회귀 | PASS | 지운 시험 = 공유 그룹 2개(시스템 시트 · 동영상 받기 · [취소])뿐 — 보내기 · 수정 · 삭제 · 동영상 · 링크 · 키보드 · 알약 시험은 손대지 않음 · `post` 는 `_check_peer` · `_insert` 로 나눴을 뿐 같은 순서(r3 · 1판 pytest 초록) |
| 통역 드로어 높이 · 손잡이 | PASS | `interpret_drawer.dart` LayoutBuilder — 높이 = 놓인 칸 × 0.92 · 상태 표시줄 아래로 자름 · 손잡이 누름 · 끌어 내림(25% 또는 빠름) · 폰 · 아주 낮은 칸 · 아이패드 시험 |
| 탭바 유무 | PASS | 드로어는 `room_screen.dart:84` Scaffold 본문 Stack 칸 기준이라 탭바가 있든(폰) 없든(아이패드 레일) 칸을 따른다 |
| 통역 세션 정리 | PASS(참고 1) | 닫기 · 끌어 내림 모두 `_close` → `_teardown`(마이크 stop → WS close → 재생기 flush) · dispose 도 같음 — 참고 R-1 |
| 기능 독립 | PASS | `procedure/` 밖 변경 0 · 새 import 는 기능 안 |
| 비밀값 · 실명 · 키 | PASS | 새 코드에 하드코딩 주소 · 계정 0 · 시험 이름 = 가짜(c-amy …) |

## 고객(사용자)이 실물에서 만날 자리

1. **폰에서 [공유] → 검색칸 누름** → 키보드가 올라오면 시트 머리([✕] · 「공유」 · [전송 N])가 노치 · 상태 표시줄 밑으로 들어간다. 키보드가 없어도 큰 아이폰에서는 손잡이가 Dynamic Island 밑이다(W3-1). SE 꼴(667)은 키보드 없을 때 겨우 들어온다.
2. 검색 중 키보드가 목록 아래쪽을 덮는다. 시트 높이를 줄이지 않아서 마지막 몇 줄은 키보드를 내려야 고를 수 있다(시트가 칸에 맞게 줄어도 같음).
3. [전송]을 누르고 도는 동안 끌어 내리거나 [✕]를 누르면 시트가 닫히고 아무 토스트도 없다. 실제로는 보내졌을 수 있다(W3-3).
4. 일부 실패면 시트가 남고 **실패한 곳만 고른 채** 남는다(처분 OQ-959 — review-doc-r4 의 「닫힌다」 기대는 처분으로 바뀜). 비활성 1:1 이 섞여 실패했으면 그곳을 직접 빼야 다시 [전송]이 「전부 됨」이 된다.
5. 같은 사람: [전체] 탭에서는 1:1 방 줄(방 이름 = 그 사람 이름)로만 보이고, [사람] 탭에서는 직원 줄로 보인다. 둘은 같은 고름(키 `p:<id>`)이라 칩 줄은 하나다.
6. 남의 메시지를 전달하면 받는 쪽에는 보낸 사람 = 전달한 나로 보이고 「전달됨」 표시가 없다(D-64). 원본을 지워도 전달본이 남아 있으면 사진 · 동영상 파일은 서버에 남는다(D-66).
7. 통역 드로어는 이제 손잡이를 끌어 내려 닫을 수 있다. 25% 미만으로 천천히 끌면 제자리로 돌아온다.
8. 빌드 12 사용자는 back 배포 뒤에도 [공유] = 옛 iOS 시스템 시트다(앱 빌드 13 전까지).

## 참고(기존 부채 · 이번 판정 밖)

- R-1 `interpret_drawer.dart` `_teardown`: `_mic.stop()` → `c?.close()` 차례라서, `_mic.stop` 이 던지면 WS close 가 건너뛰어진다. 이번에 더한 try/catch 는 드로어를 닫히게만 한다. `_client` 는 이미 null 이라 dispose 에서도 다시 닫지 않는다. 지금 `Mic.stop`(`audio_io.dart:71-77`)은 `_rec.stop` 예외를 삼켜서 실제로 던질 길은 `_sub.cancel` 뿐이라 WARN 으로 올리지 않는다. 드로어 시험은 로그인 없이 돌아 마이크 · WS 가 열리지 않으므로 「닫힐 때 마이크 stop · WS close」 자체는 단언하지 않는다(통역 기존 시험에 맡김).
- R-2 `_close` 재진입: 끌어 내려 닫히는 220ms 사이에 손잡이를 또 누르면 `onClose` 가 두 번 불린다(부모 setState 두 번 · 해 없음 · 누름 닫기는 전부터 같음).
- R-3 back `forward` 다시 보내기: 같은 clientId 의 처음 메시지가 다른 방에 있으면 결과 `roomId` 는 처음 메시지 방이고 `done` 키는 요청 방이다. 앱은 키마다 clientId 를 고정해 이 꼴을 만들지 않는다.
