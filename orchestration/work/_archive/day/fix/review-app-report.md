# 리뷰 리포트 — fix 앱 WP-APP-1 · WP-APP-2 / code (2026-11-11)

검수 대상: `CENTURION_DAY/fix`(`kknaksss/fix`) `app/` 미커밋 변경 29파일(`git diff -- app` · +1225 −133). 작성자 아님 · read-only.
계약 SoT: mediness `fix-spec` 미커밋 SPEC-003(개정 ⑧ · ⑨) · SPEC-004(2026-11-11 개정 ① ② ③) · SPEC-005 · `wp-plan.md` §2 · §3.

## 판정: WARN

FAIL 0 · WARN 1 · 참고 5.
사용자 피드백 1 · 2 · 3 · 4 · 6 · 7번과 후속 2건은 코드 경로로 따라가 보니 모두 풀렸다. 새 화면 글자는 0개이고(전부 기존 상수 재사용), 서버 #22 · 설정 계약과도 필드 단위로 같다.
WARN 하나는 채팅 403 이 일부 화면(새 대화 · 사진 모아보기)에서 거절 안내로 가지 않는 것이다.

## FAIL

없음.

## WARN

### W1. 채팅 403 이 「거절」로 가지 않는 경로 2곳 — 새 대화 직원 목록 · 사진 · 동영상 모아보기
- `app/lib/chat/screens/chat_new_screen.dart:58-63` — `people()` 가 403 이면 `_error = e.message` 로 새 대화 화면 안에 `forbidden` 글자를 띄운다. `ChatState.denied` 로 가지 않으니 채팅 메모리 비움 · 스트림 멈춤 · 열린 창 닫기가 일어나지 않는다.
- `app/lib/chat/screens/chat_media_screen.dart:80-82` — 403 이면 `_failed = true` 다. 그래서 「사진 · 동영상을 불러오지 못했어요」 + [다시 시도]가 뜨고, 「권한 없음」 안내와 다른 글자가 된다.
- (작음) `app/lib/chat/chat_state.dart:960-967` 사진 바이트 읽기 403 = 무시(빈 칸). 다른 호출이 곧 거절로 보내므로 영향은 작다.
- 근거: SPEC-004 U-1 `:155`(「방 목록 · 스트림 · **그 밖 채팅 HTTP** 가 403 `forbidden` 이면 … 채팅 탭 본문 자리에」) · `:156`(열린 대화 · 방 정보 닫음 · 메모리 비움) · 케이스 매트릭스 `:449` · C-A19.
- 실제로 마주칠 일: 직원이 비활성으로 바뀐 순간 새 대화 · 모아보기 화면에 있으면, 스트림이 아직 403 을 받기 전까지 안내 화면 대신 그 화면 안 글자가 남는다. 앞의 대부분 경로(`refreshRooms` · `loadLatest` · `loadOlder` · `since` 메우기 · 읽음 · 보내기 · 수정 · 이름 바꾸기 · `run()` 경유 조작)는 `_handleError → _forbidden` 으로 맞게 간다.
- 고칠 방향: 두 화면의 `on ApiError` 에서 `e.isForbidden` 이면 `_app.chat.handle(e, ChatOp.other)` 로 넘긴다(보내기 · 수정과 같은 방식). 시험은 `chat_ui_test` 에 403 1건씩.

## 사용자 피드백이 풀렸나 (코드 경로)

| # | 본 것 | 지금 코드 | 결과 |
|---|---|---|---|
| 1 · 4 | 모두 완료인데 목록은 「시술 대기」 · 카드에 [귀가 대기] 없음 | `board_screen.dart:396-413` `_nowBox` 맨 앞 `card.allDone` → `allDoneLabel` / `lastDoneLabel(card.lastCompletedAt)` · 오른쪽 `''` · 마취 열림 무시(OQ-A37) · `:326` `_homeLine` = `canSendHome(c, me)`(`room_screen.dart:28` = `card.canHome && me.canEditBoard`) · `sendHomeAction` → `BoardController.home` 잠금 `home:{visitId}` | 풀림 — 방 상세(`room_screen.dart:594-611`)와 **같은 함수** · 같은 글자 상수(`format.dart:61-68`) · 같은 계산(`board.dart:200-208` `lastCompletedAt` 한 곳). 복사본 없음 |
| 2 | 카드 빨간 굵은 테두리(B안) | `board_screen.dart:296` 테두리 = 상태색만 · `:334-354` `_box` = `needs` 있으면 바탕 `Ms.red100` + 왼쪽 3px `Ms.red` 띠(글자 자리 유지) · `_callBox` 도 같은 `_box`(`:453`) | 풀림 — 겹침 7자리 전부 `_box` 하나로 처리됨. iPad 캡처 1장에서 7자리 + `needs` 없는 카드(G-룸8 평소 회색)를 눈으로 확인 |
| 3 | 채팅 403 인데 「서버에 연결 중…」 + 로딩 | `chat_state.dart:237-245` `_forbidden` = 스트림 멈춤 · `idle` · `clear()` · `denied=true` · 토스트 없음 · `chat_kit.dart:479-490` 거절이면 연결 줄 없음 · `shell.dart:213-222` 채팅 탭 본문 = `ForbiddenBody`(기존 `forbiddenMessage` · [로그아웃]) · `:176-180` 열린 대화 · 시트 닫음 · `chat_stream.dart:98-106` 403 = `_running=false` 재연결 없음(기존) | 풀림(W1 의 2곳 빼고) |
| 6 | 방 정보에서 그룹 이름 못 바꿈 | `chat_info_screen.dart:163-259` `GroupTitleCard`(그룹만 · 누르면 편집 · ✓/✕ · 40자 · 같은 값 ✓ 꺼짐 · 보내는 중 꺼짐) · `chat_state.dart:916-938` `rename` · `chat_api.dart:111` `PUT …/title {title}` | 풀림 |
| 7 | 설정에 채팅 전체 스위치 없음 | `notification_model.dart:16` `'chat': menuChat` · `:19-24` `chatAlertsOf`(없으면 켜짐) · `notification_controller.dart:34 · 72-86 · 126` 로그인 · 자동 로그인(`start`) · 앞으로 올 때 다시 읽음 · `notification_settings.dart:38-40` 바꾼 뒤 `applySettings` · `chat_state.dart:684` 배너 억제 · `app.dart:171` 같은 세션 값 전달 | 풀림 |
| 후속 | `version` 같은 값 · `calls[].canRecall` | `board_stream.dart:213` `>=` · `board.dart:238 · 263 · 331` `CallItem.canRecall` · `callCanRecall` · `Task.canRecall` 제거 · `room_screen.dart:24` `canRecallCall(snap, oc, me)` | 풀림 |

## 업무 규칙을 앱이 다시 계산하나

- [귀가 대기] 노출 = 서버 `canHome` + `/me` board edit — 목록 · 방 상세가 `canSendHome` 하나를 쓴다. 잠금 키는 `homeLockKey`(`room_screen.dart:32`)이고, 실제 잠금을 거는 쪽은 `board_controller.dart:185` 의 같은 문자열 `'home:$visitId'` 다. 문자열이 두 곳에 있다(참고 R1). 다만 `actions_test` 「이중 탭 잠금 · 룸 상세 [귀가 대기]와 같은 잠금」이 끝에서 끝까지 확인한다.
- 「모두 완료」 = `BoardCard.allDone`(기존 표시 계산 · 스펙 U-3 「앱 표시 계산」) · 마지막 종료 = `lastCompletedAt` 한 곳.
- 확인 필요 = `needs.isNotEmpty` 그대로. `why` 를 앱이 다시 판정하지 않는다.
- 목록 [귀가 대기] 줄에 `waitingCalls.isEmpty` 가 더 붙어 있다(`board_screen.dart:326`). 스펙 U-3 겹침 ①(「모두 완료 ↔ 수락 대기 호출은 생기지 않는다」) 때문에 결과는 같다(참고 R2).

## 새 화면 글자 표 (`git diff -- app/lib` 의 `+` 줄 · 주석 제외 · 한글 리터럴 전부)

| 글자 | 자리 | 이미 있던 곳(origin/dev) | 스펙 |
|---|---|---|---|
| 시술 모두 완료 | `format.dart:62` | `room_screen.dart`(옮김) | SPEC-003 U-3 개정 ⑧ · U-4 5번 |
| 마지막 종료 {HH:MM} | `format.dart:65` | `room_screen.dart`(옮김) | 같음 |
| 귀가 대기 | `format.dart:68` | `room_screen.dart`(옮김) | U-3 「모두 완료 카드」 · U-9 |
| 외 {N}개 | `board_screen.dart:361` | 같은 줄(조건만 바뀜) | U-3 |
| 그룹 이름 ×2 | `chat_info_screen.dart:230 · 240` | `chat_info_screen.dart:105` · `chat_new_screen.dart` | SPEC-004 U-7 `:221` |
| 비우면 참여자 이름으로 보여요 | `chat_info_screen.dart:248` | `chat_new_screen.dart:135` | U-7 `:221` |
| 수정 취소 · 저장(접근성) | `chat_info_screen.dart:254-255` | `chat_room_screen.dart:588 · 638` | U-7 `:222` · OQ-C11 (가) |
| 원장 호출 | `notification_model.dart:16` | 같은 파일 `:13` | SPEC-005 |
| 1:1 은 나갈 수 없어요 … / 1:1 에는 참여자를 더할 수 없어요 | `chat_copy.dart:20-22` | 같은 파일(분기만) | SPEC-004 §3 오류 표 `:370` |
| 채팅(설정 줄) | `menuChat` 상수 | `core/copy.dart:60` | SPEC-005 U-3 |
| (채팅 403) 이 화면을 볼 권한이 없습니다 … · 로그아웃 | `forbiddenMessage` 상수 | `core/copy.dart:18` | SPEC-004 U-1 · OQ-C15 |

**새 글자 0.** #22 `chat_group_only` 는 `codeOnly(code)`(`chat_copy.dart:21`)로 처리한다. 스펙 §3 규칙 `:349` 「이 경로에서 화면 글자를 정하지 않음」과 같다.

## 서버 계약 대조 (wp-plan §3 ↔ 서버 코드 ↔ 앱)

| 무엇 | 서버(읽기) | 앱 | 같나 |
|---|---|---|---|
| #22 요청 | `routers/api/chat.py:199-209` `PUT /rooms/{room_id}/title` · `writable_session` · `schemas/chat.py:36-42` `TitleRequest.title: str \| None`(칸 필수 · 모르는 칸 400) | `chat_api.dart:111` 본문 `{'title': t\|null}` 한 칸 · Bearer | 같음 |
| #22 규칙 | `services/chat.py:651-653` 앞뒤 공백 뺌 · 빈 값 → None · `len > 40` 400 `invalid_request` `title` · `:659` 1:1 = 400 `chat_group_only` · `:660-663` 같은 이름 200 이벤트 없음 · `:664-670` `chat_room` 지금 멤버 전부 · 404 = `_room_for` | 앞뒤 공백 뺌 · 빈 값 null(`chat_state.dart:919-920`) · 40 코드포인트 입력 제한 · 404 · 403 · 4xx · 0/5xx 분기 · `chat_room` = 기존 `_upsert` | 같음(40자 셈만 미세 차이 — 작성자 5번) |
| 응답 | `_room_view`(요청 계정 기준 Room) | 기존 `Room.fromJson` | 같음 |
| 설정 읽기 | `services/notifications.py:225-258` 받는 종류 차례 `doctor_call` → `chat` · 저장 없으면 `True` | 차례 그대로 · `chat` 없으면 켜짐 · 모르는 kind 버림 | 같음 |
| 설정 쓰기 | `{kind, enabled}` | 기존 PUT · 바꾼 뒤 다시 읽기 → `applySettings` | 같음 |
| 채팅 403 | 모든 채팅 HTTP · 스트림 `forbidden` | W1 2곳 빼고 거절 | W1 |

## 상태 · 경합

- 403 → 스트림 멈춤(`_stream.stop` · `null`) · `onStatus` 는 거절 중 무시 · 재연결 0(`chat_state_test` 40ms · `chat_ui_test` 40초).
- 다시 보는 때: 새 세션 = 새 `ChatState`(`app.dart:166-172`) · 앞으로 올 때 `setForeground(true)` → `_recheck` 한 번(`_rechecking` 으로 겹침 막음) · 그 밖 재시도 없음.
- 세션이 바뀐 뒤 온 결과: `_disposed` 검사(`_recheck` · `rename` · `refreshRooms`). `NotificationController` 도 세션마다 새로 만들고 `_disposed` 를 본다.
- 조작 중 403 = `_handleError` 에서 토스트 없이 `_forbidden`(`chat_state.dart:224-233`).
- 그룹 이름: 저장 중 ✓ · ✕ 꺼짐 · 실패면 입력 그대로 `_editing` 유지 · 404 면 목록에서 빼고 아이패드 시트 닫음.
  - 편집 중 다른 사람이 바꿔 `chat_room` 이 오면 입력은 그대로 두고, ✓ 비교 기준(`_initial`)이 새 이름으로 바뀐다. 스펙에 정한 것이 없는 자리다. 이상한 결과(덮어쓰기 · 크래시)는 없고, 나중 저장이 남는다(서버 `:349` 와 같음).
- 「채팅」 스위치: 앞에서 받은 채팅 푸시도 같은 `offerBanner`(`app.dart:210`)를 지나므로 꺼짐이면 배너 0. 지금 떠 있는 배너는 그 배너 타이머까지 남는다(작음).
- 참고 R3 · R4 를 보라(늦게 온 설정 응답 · 뒤로 간 사이 연 스트림).

## 작성자 「스펙 · 계획과 다른 곳」 10건 판정

| # | 내용 | 판정 |
|---|---|---|
| app-1 ① | 「시술 모두 완료」 글자 색 = 주색 | **스펙 안**. 스펙은 바탕만 정하고 글자 색은 정하지 않았다. 방 상세 강조 상자 글자(`Ms.primary`)와 같다. 캡처에서 옅은 빨강 위 파랑 글자 — 코디 눈 확인으로 충분 |
| app-1 ② | 모두 완료 · `needs` 빔 = 회색 | **스펙 안**. 서버 규칙상 안 생긴다(U-3 겹침 ③). 무리 없는 기본값 |
| app-1 ③ | 띠 3px | **스펙 안**(OQ-A20 「구현 때 정함 · 리뷰 눈 확인」) — 캡처에서 잘 보임 |
| app-1 ④ | `session_race_test` 무변경 | 문제 없음(계획 표의 후보였을 뿐) |
| app-2 ① | 거절 안내를 셸에서 바꿈 | **스펙 안**. U-1 `:155-156` 결과(본문 자리 안내 · 열린 대화 · 방 정보 닫음)를 한 곳에서 지킨다. 시술현황 권한 없음과 같은 위젯 |
| app-2 ② | `push_coordinator.dart` 무변경 | **스펙 안**. OQ-C13 의 때(로그인 · 자동 로그인 · 앞으로 올 때 · 바꾼 뒤)가 `NotificationController.start` · `setForeground` · `applySettings` 로 다 채워짐 |
| app-2 ③ | 그룹 이름 줄에 「누를 수 있음」 표시 없음 | **스펙 안**(와이어 「누르면 바꾸기」 · 아이콘 미정). 실기기에서 「바꿀 수 있는 줄 몰랐다」가 나오면 사용자 결정 — 지금 물을 필요 없음 |
| app-2 ④ | 이름 바꾸기 네트워크 · 5xx = 토스트 없음 | 네트워크 = **스펙 안**(`:451` 「입력 그대로 두고 다시 저장 가능」). 5xx 는 스펙에 글자가 없다 — 글자를 짓지 않은 것이 문구 원칙과 맞음. 수정 실패의 「고치지 못했어요」 같은 글자를 쓰려면 사용자 결정(선택) |
| app-2 ⑤ | 40자에 앞뒤 공백 포함 | **스펙과 미세 차이**(`:221` 「앞뒤 공백 뺀 뒤 40자」). 붙여 넣은 40자 + 끝 공백이 잘리는 정도라 실사용 영향은 거의 없다. 참고 R5 |
| app-2 ⑥ | 거절 상태에서 채팅 푸시 배너 없음 | **스펙 안**(U-8 `:233` 괄호 「채팅 403 이면 어차피 … 안내」 · U-1 「채팅 메모리 비움」) |

사용자에게 꼭 물어야 할 것은 없다. ③ · ④ 는 실기기 반응을 보고 정해도 된다.

## 조용히 통과하는 자리

1. **W1 경로는 시험이 없다** — 새 대화 · 모아보기 403. 수용 항목 C-A19 시험은 목록 · 스트림 · 보내기 · 이름 바꾸기만 확인한다.
2. `chat_state_test` 「거절 상태에서는 배너 없음」 — 같은 시험 안에 「거절 아님 → 배너 있음」 대조가 없다. 다른 시험(「chatAlerts 를 주지 않으면 켜짐」)이 대조 역할을 해서 지금은 실패할 수 있는 시험이다. 시험을 옮기거나 나누면 대조가 사라질 수 있다.
3. 픽스처 `callsOf`(`test/support/fixtures.dart:262-285`)는 줄 상태 `called` 면 `canRecall=true` 를 기본으로 만든다. 서버 규칙을 흉내 낸 기본값이다. 앱은 값을 그대로 읽으므로 A-22 노출 시험은 「전달」만 본다. 「줄에 옛 `canRecall=true` + 호출 `false` → 안 보임」 반대 시험(`board_stream_test` 새 1건)이 있어 구현을 베낀 시험은 아니다.
4. 캡처 시험(`test/capture/*`)은 평소 skip 이다(`~67`). 캡처 12장은 작성자가 따로 돌린 결과라 이번 `flutter test` 수치에 들어 있지 않다.
5. 수용 항목별 시험은 있다 — A-9 · A-22 · A-28 · A-33 · A-37 · A-41 ~ A-43 · C-A19(W1 빼고) · C-A20(앱) · C-A21(앱) · N-A10 · N-A13(앱). 실물(로컬 day-local · 두 기기 · TestFlight)은 pending 이다(작성자 보고와 같음).

## 범위

- 변경은 `app/lib/` 15 · `app/test/` 14 뿐이다. `app/lib/interpret/` 0 · `pubspec.yaml` · `pubspec.lock` 0 · 새 파일 0 · `backend/` 은 읽기만 했다.
- 새 색 토큰 0(`Ms.red100` · `Ms.red` · `Ms.gray100` · `Ms.primary` 기존) · 새 상태값 0.

## 참고

- R1. 잠금 키 문자열이 둘이다 — `room_screen.dart:32` `homeLockKey` · `board_controller.dart:185` `'home:$visitId'`. 고칠 방향: 컨트롤러가 `homeLockKey` 를 쓰게(한 곳).
- R2. `board_screen.dart:326` `waitingCalls.isEmpty` 는 스펙 조건(canHome + edit) 밖의 앱 조건이다. 서버 규칙상 결과는 같다. 빼면 「방 상세와 같은 조건」이 글자 그대로 맞는다.
- R3. 늦게 온 설정 응답 순서 보장이 없다 — `notification_controller.dart:73-80`(앞으로 올 때 GET)이 설정 화면의 PUT → GET(`notification_settings.dart:38-40`)보다 늦게 오면 옛 값으로 덮인다. 다음 앞으로 올 때 맞춰지고, 서버 푸시는 바로 맞으므로 영향은 앱 안 배너뿐이다.
- R4. `_recheck`(`chat_state.dart:248-259`)가 풀린 뒤 스트림을 열 때 그 사이 앱이 뒤로 갔는지 보지 않는다. 뒤에서 스트림이 열린 채로 남을 수 있다(`foreground` 면 `resume`, 아니면 `pause` 한 줄).
- R5. 작성자 ⑤ — 40자 셈에 앞뒤 공백 포함(스펙은 뺀 뒤). 맞추려면 포매터 대신 저장 때 `trim` 후 셈 + ✓ 꺼짐.

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd app && fvm flutter analyze` | No issues found! |
| `cd app && fvm flutter test` | **+314 ~67 All tests passed!**(skip 67 = 캡처 · 평소 skip) · exit 0 |
| 캡처 눈 확인 | phone 4장(모두 완료 · 확인 필요 칩 · 채팅 403 · 그룹 이름 편집 · 설정 「채팅」) · iPad 1장(겹침 7자리 + 평소 카드) — 스펙 와이어(SPEC-003 `:158-178` · SPEC-004 U-7)와 같음 |
