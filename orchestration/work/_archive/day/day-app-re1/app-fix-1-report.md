# day-app-re1 app-fix-1 결과 보고 (mobile)

## 상태: done

대상: 워크트리 `day-app-re1` · `43ba40a3` 위 · 변경은 `app/` 만(커밋 · push 없음). backend 워커 변경(`backend/`)은 건드리지 않았다.

## 수행 — 파일 · 화면 목록

| 항목 | 파일 | 내용 |
|---|---|---|
| W1 | `app/lib/state/chart_controller.dart` | 10초 tick 건너뜀 조건 = 고르는 중 · **올리기 · 삭제 · 다시 시도 중**(`_photoMutating`) · 읽는 중. 세대 번호 `_photoGen` 은 조작이 시작될 때 +1, 끝날 때(성공 · 실패 · 넘김 = `finally`) +1. GET 은 시작할 때 세대를 잡아 두고, 응답이 왔을 때 세대가 바뀌었거나 조작이 진행 중이면 버린다. 정본은 조작 응답 목록이다 |
| W2 | 같은 파일 | `file()` 실패 = future(null)를 캐시에 남긴다(같은 future → `FutureBuilder` 다시 그림 = 요청 0 · 깜빡임 없음). 목록 반영(`_setPhotos`) 때 **사진 id 줄이 바뀌면** 실패한 사진만 캐시에서 빼서 다음 그림 때 다시 받는다. `photos` 는 getter 로 바꿈(쓰기는 `_setPhotos` 하나) |
| Q1 | `app/lib/ui/session_nav.dart`(`LeaveGuard` · `LeaveGuards` · `LeaveGuardScope`) · `app/lib/ui/shell.dart` · `app/lib/ui/chart_sheet.dart` | 셸이 세션 Navigator 를 `LeaveGuardScope` 로 감싼다. 차트 창(`_ChartWindowState implements LeaveGuard`)은 열릴 때 등록하고, 닫힐 때(didPop · dispose) 지운다. `_toVisit`(알림 행 · 원장 호출 푸시) · `_toChat`(채팅 푸시 · 배너 [보기]) · `_onChatDenied`(채팅 탭일 때 세션 Navigator 비우기)는 `_leaveSession(go)` 를 거친다. 미저장이 없으면 지금처럼 바로 `go`. 있으면 ✕ 와 같은 확인 창(「저장하지 않고 닫을까요?」 · [계속 쓰기] · [버리고 닫기] — 기존 `chartDiscard*` 글자 · `showChartConfirm` 같은 함수)이 뜬다. [버리고 닫기] = `c.discard()` 뒤 원래 이동(popUntil), [계속 쓰기] = 이동 안 함. 채팅은 확인 전에 채팅 목록이 방을 먼저 열지 않도록 `openRequest` 를 거두고, [버리고 닫기] 때 `chat.openRoom(id)` 로 다시 건다. ✕ 확인 창과 확인 로직(`_askDiscard`)을 함께 쓴다 |
| Q2 | `session_nav.dart`(`SessionRoutes` · `track` · `closeAll`) · `room_screen.dart` · `doctor_picker.dart`(`showPickerSurface` · `showDoctorPicker` 에 `track:`) · `room_move.dart` · `accept.dart` | 룸 상세가 `SessionRoutes _sheets` 를 갖는다. 그 화면이 띄우는 시작/완료 취소 확인(`confirmUndo`) · 의사 호출 · 바로 시작 · 원장 바꾸기 · 대리 수락 고르기 · 방 옮기기의 내용을 `track` 으로 감싸 route 를 기억한다. 닫는 때는 셋이다. ① 카드가 판에서 빠짐(`_changed` → 다음 프레임 `closeAll` → 목록으로) ② 룸 route 가 탭 스택에서 빠짐(`RouteAware.didPop` — 뒤로 · 같은 탭 다시 · 카드 빠짐) ③ 판이 바뀌어 탭 스택째 버려짐(dispose → 다음 프레임). `closeAll` 은 맨 위 route 를 `pop`(닫는 움직임)하고 아래 route 는 `removeRoute` 한다. 기다리던 쪽은 null 을 받는다 = [닫기]와 같아 요청 0. **차트 창은 넣지 않았다**(OQ-A69 — 남음). 차트 안 담당자 고르기 · 사진 삭제 확인도 차트 소속이라 넣지 않았다 |
| 테스트 | `app/test/state/chart_controller_test.dart`(+2) · `app/test/ui/session_leave_test.dart`(새 파일 · 10) | 아래 |

새 화면 글자 없음 · 새 패키지 없음 · W3 · W4 손대지 않음.

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+472 ~81 −0**(app-1 기준 +460 → 새 테스트 12) |
| `fvm flutter build ios --no-codesign` | ✓ Built `build/ios/iphoneos/Runner.app`(20.8MB) |
| 새 테스트가 「조용히 통과」가 아닌지 | `app/lib` 변경 8파일을 `HEAD` 로 잠깐 되돌려 새 테스트를 돌렸다 → **W1 · W2 · Q1 ×2 · Q2 ×4 = 8개가 실패**했다. 되돌린 파일은 원래대로 돌려놓았다(diff 8파일 236+/26− 그대로 확인). W8 둘 · 「Q1 미저장 없음 = 바로 이동」 · 「Q2 차트 남음」은 지금 동작을 지키는 회귀 테스트라 고치기 전후 모두 통과한다 |

새 테스트 목록:
- W1 — 삭제 보내는 중 10초 = tick 0 · tick GET(지운 사진이 아직 있는 목록)이 다시 시도 응답보다 늦게 옴 = 버림 · 「KOS 미반영」으로 되돌아가지 않음 · 올리는 중 = 건너뜀 · 끝난 뒤 다음 회차는 다시 읽음
- W2 — 받기 실패 = 같은 future(`identical`) · 파일 GET 1회 · 같은 목록이 다시 와도 1회 · 사진 id 줄이 바뀌면 다시 받음(2회 · 성공 바이트)
- W8 — 룸 상세 · Android 뒤로 = 목록 / 차트 위 뒤로 = 차트만 → 한 번 더 = 목록
- Q1 — 원장 호출 푸시: [계속 쓰기] = 이동 안 함 · 쓴 글 · 룸 그대로 / [버리고 닫기] = 그 방문 룸 · 저장 POST 0 · 미저장 없음 = 확인 없이 바로 · 채팅 푸시: [계속 쓰기] = 채팅 방 안 열림(숨은 채팅 탭 포함) / [버리고 닫기] = 그 방
- Q2 — 폰 시작 취소 확인 시트 · 폰 의사 호출 시트 · 아이패드 원장 고르기 팝오버 · 아이패드 방 옮기기 팝오버: 카드가 빠지면 닫힘 + 목록으로 · POST 0 / 아이패드 팝오버가 뜬 채 룸 route pop = 팝오버 닫힘 / 차트는 카드가 빠져도 남고 쓴 글도 그대로

## 계약 대조

- API · 요청 모양 변경 없음(C0 ~ C3 그대로). 사진 GET 쿼리(`tick=1` · `poll=1` · 없음)도 그대로다.
- 닫기 표(D6′ · D12) 다섯 길은 그대로다. 기존 `chart_test.dart` 닫기 시험이 전부 통과한다. Q1 확인 창은 ✕ 와 같은 함수 · 같은 글자(SPEC U-23 · E59)다.
- OQ-A69 차트 남음은 유지했다(Q2 테스트로 지킴).

## 이슈 · 코디가 확인할 것

1. **채팅 배너 [보기]는 차트가 열린 동안 실제로는 누를 수 없다.** `ChatBannerLayer` 는 세션 Navigator 첫 route(`_frame`) 안에 있어서, 차트(폰 전체 화면 · 아이패드 덮개)에 덮인다. Q1 의 배너 길은 배선만 했다(`_openBanner` → `openRoom` → `_toChat` 같은 길). 시험은 채팅 푸시로 했다. 배너를 차트 위로 올릴지는 제품 결정이다(지금은 손대지 않음).
2. 확인 창이 이미 떠 있는데(✕ 확인 · 앞선 푸시 확인) 또 푸시를 누르면 그 이동은 하지 않는다. 확인 창을 두 개 쌓지 않으려는 것이다. 놓친 이동은 다시 누르면 된다.
3. 저장을 보내는 중에(미저장 + busy) 푸시를 누르면 확인 창이 뜬다(✕ 는 꺼져 있지만 이동은 사용자가 고른 것). [버리고 닫기]를 누르면 창이 닫히고, 보낸 저장은 서버에서 끝난다(응답은 버림). 지금 OQ-A70(보내는 중 닫기 꺼짐)과 다르니 SPEC 결정이 필요하면 알려 달라.
4. [계속 쓰기]를 골라도 알림 읽음 처리는 이미 나갔다(알림 컨트롤러가 openVisit 전에 읽음 처리 — 기존 동작). 채팅 [계속 쓰기]는 열기 요청을 거두므로 그 방은 열리지 않고, 배너도 지워진다.
5. W2 — 받기 실패한 썸네일은 사진 id 줄이 바뀌거나 차트를 다시 열 때까지 다시 받지 않는다(지시대로). 잠깐 끊겨서 실패한 경우에도 깨진 그림이 그대로 남는다.
6. W1 — 버린 GET 이 `reread=true` 였다면 5초 뒤 `poll=1` 을 걸지 않는다. 다음 10초 tick 이 다시 읽는다.
7. Q2 ③(판이 바뀌어 탭 스택째 버려짐 → dispose 다음 프레임 `closeAll`)은 배선만 하고 위젯 테스트는 없다. ① · ② 는 테스트가 있다.

### review-code-1 §9 — 싸게 고칠 수 있는 것(목록만 · 고치지 않음)

| §9 | 이번 처리 | 싸게 고칠 수 있나 |
|---|---|---|
| 1 배너 · 푸시가 차트를 경고 없이 닫음 | **고침**(Q1) — 배너는 위 이슈 1 | — |
| 3 지운 사진이 잠깐 다시 보임 | **고침**(W1) | — |
| 4 실패 썸네일 깜빡임 | **고침**(W2) | — |
| 11 카드가 빠진 뒤 남는 시트 | **고침**(Q2) | — |
| 8 담당자 고르기 = 서버 순서 | 그대로 | 싸다. `showStaffPicker` 에서 `options` 대신 이미 만든 `sorted` 로 그리면 된다(한 줄). 다만 이름순이 맞는지 SPEC(D5 「원장 고르기 드로어 재사용」) 확인이 필요하다 |
| 9 저장 200 뒤 커서가 끝으로 튐 | 그대로 | 싸다. `chart_sheet.dart` `_changed` 에서 `text` 를 바꿀 때 `selection` 을 새 길이 안으로 줄여 유지하면 된다(몇 줄 · 글자 없음) |
| 10 올리는 중 진행 표시 없음 | 그대로 | 싸다. 올리는 묶음의 ＋ 칸(`isUploading`)에 작은 원(`CircularProgressIndicator`)을 그리면 된다(글자 없음) |
| 12 꺼진 [시작] · 담당의 글자 누름 = 차트 열림 | 그대로 | 중간. 꺼진 버튼을 `AbsorbPointer` 로 감싸면 된다. 다만 SPEC 「여는 곳 = 시술 줄 누름」과 어긋나지 않는지 확인이 필요하다 |
| 2 · 5 · 6 · 7 · 13 | 그대로 | W4 · W3(2루프) · OQ-A78 · 웹과 같은 빈 값 · 설계대로 — 이번 범위 밖 |
