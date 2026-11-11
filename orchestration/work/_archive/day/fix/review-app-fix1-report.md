# 리뷰 리포트 — fix 앱 수정 1 재확인 / code (2026-11-11)

대상: `CENTURION_DAY/fix` `app/` — 앞 검수(`review-app-report.md`) 뒤에 바뀐 것만. 근거: 작성자 `app-fix1-report.md` · SPEC-004 U-1 `:155-159` · C-A19 · U-7 `:221`. read-only.

## 판정: PASS

W1 · R1 ~ R5 · 「조용히 통과」 2 가 모두 풀렸다. 내가 직접 센 채팅 HTTP 호출 자리에서 403 이 거절로 가지 않는 곳은 0이다. 새 화면 글자 0 · 범위 `app/lib` · `app/test` 안.
참고 1건(작음 · 막지 않음).

## 항목별

| # | 결과 | 자리 |
|---|---|---|
| W1 | 풀림 | `chat_state.dart:269-277` `_guard`(403 → `_forbidden()` 뒤 다시 던짐) · 감싼 11개(`:856 · 863 · 870 · 888 · 891 · 899 · 907 · 915 · 922 · 953 · 960`) · 사진 · 썸네일 `_load` 403 → 거절 · `chat_new_screen.dart:62` 403 = 화면 글자 없이 끝 · `chat_media_screen.dart:71 · 82` 공통 호출 + 403 = `_failed` 아님 |
| W1+ 전달 시트 | 옳음 | `chat_forward_sheet.dart:86-91` — 401 · 403 만 `chat.handle` → `_handleError`: 401 = `onSessionEnd(code)`(다른 화면의 `onUnauthorized` 와 같은 결과 — 세션 끝 규칙 같음) · 403 = 거절. 그 밖 = 기존 시트 안 실패 |
| W1+ 동영상 재생 | 옳음 | `chat_video_screen.dart:120-129` — 재생 실패 → `refreshRooms()`. 네트워크 끊김이면 `refreshRooms` 는 status 0 → `_handleError` 를 부르지 않고 false → `denied` 그대로 false → 기존 「동영상을 찾을 수 없어요」 + 닫기(거절로 잘못 가지 않음). 403 일 때만 거절 · 401 이면 세션 끝 → `disposed` → 조용히 끝 |
| R1 | 풀림 | `board_controller.dart:35` `homeLockKey` 한 곳 · `:188` `home()` 와 `room_screen.dart:32` `sendHomeAction` 이 같은 함수 사용 |
| R2 | 풀림 | `board_screen.dart:326` `c.allDone && canSendHome(c, me)` — 방 상세와 같은 조건 |
| R3 | 풀림 | `notification_controller.dart:73-94` 순번(`beginSettingsRead` · `applySettings(l, seq)` 가 `seq != _settingsSeq` 면 버림) · 설정 화면 `_toggle` = PUT → `_load()`(`notification_settings.dart:36-40` 새 순번으로 GET) → 그보다 먼저 보낸 「앞으로 올 때」 GET 응답이 늦게 와도 버려진다. 시험 `notification_contract_test` 「늦게 온 옛 설정 응답은 새 값을 덮지 않는다」 |
| R4 | 풀림 | `chat_state.dart:256` 열자마자 `!foreground` 면 `pause` · 시험 있음 |
| R5 | 풀림 | `chat_info_screen.dart:185-188` `_canSave` = 앞뒤 공백 뺀 코드포인트 ≤ 40 · 포매터 제거 · `_save` 첫 줄이 `if (!_canSave) return` → 41자 이상은 저장 요청이 나가지 않는다(시험: 41자 ✓ 꺼짐 · 공백 붙은 40자 ✓ 켜짐) |
| 조용히 통과 2 | 풀림 | `chat_state_test` 「거절 상태에서는 배너 없음 — 같은 시험 안 대조」(거절 아님 = 배너 있음 → 거절 뒤 = 없음) |

## 「403 → 다시 던짐」 뒤 토스트가 또 나는 자리 (항목 3)

`_guard` 를 탄 호출의 화면 쪽 처리를 전부 따라갔다 — 토스트 0.

| 호출 | 화면 처리 | 403 때 |
|---|---|---|
| `delete` · `setMuted` · `leave` · `hide` · `openDirect` · `createGroup` · `addMembers` | `ChatApp.run()` → `chat.handle` → `_handleError` 의 `isForbidden` 갈래(토스트 없음) | 안내만 |
| `edit` | `chat_room_screen.dart:545-551` `isForbidden` → `handle` | 안내만 |
| `forward` | `chat_forward_sheet.dart` `_send` 4xx → `close()` + `handle` | 안내만 |
| `people` | 새 대화 `:62` return · 전달 시트 `:86-91` handle | 안내만 |
| `attachments` | 모아보기 `:82` return | 안내만 |

## 내가 센 채팅 HTTP 호출 자리

`ChatApi` 공개 메서드 21개(people · rooms · openDirect · createGroup · addMembers · leave · hide · mute · rename · messages · attachments · send · edit · delete · forward · read · uploadPhoto · uploadVideo · photo · videoThumb · videoUri) + 채팅 스트림.

`grep "api\.<메서드>(" lib` 결과 (`chat_api.dart` 밖):
- `chat_state.dart` **23곳**: 368 · 393 · 422 · 458 · 461 · 533 · 822 · 827 · 832 · 856 · 863 · 870 · 888 · 891 · 899 · 907 · 915 · 922 · 934 · 953 · 960 · 963 · 966
- 채팅 스트림 1곳: `chat_state.dart:339`
- 재생 주소 1곳: `chat_video_screen.dart:90`

**직접 호출 = 25.** 작성자의 26 은 여기에 「모아보기 → 공통 호출로 바꾼 자리」(24번)를 더해 센 것이라 같은 결과다. 화면에서 `ChatApi` 를 직접 부르는 자리는 이제 재생 주소 하나뿐이다(`grep "\.api\." lib/chat`). `notification_controller.dart:50` 의 `ChatStream` 은 알림 스트림이라 대상 밖이다. **빠진 자리 0 · 403 누락 0.**

## 새 문제

- 새 화면 글자 0 — `+` 줄 한글 리터럴 집합이 앞 검수와 같다.
- 범위: `app/lib` · `app/test` 만 · `app/lib/interpret/` · `pubspec` 무변경.
- 참고(작음): `chat_video_screen.dart:126-128` — `refreshRooms` 를 기다린 뒤 토스트는 `mounted` 를 보지 않고 띄운다. 그 사이 화면을 떠났으면 「동영상을 찾을 수 없어요」가 뒤늦게 한 번 뜰 수 있다(`nav.maybePop` 은 `mounted` 확인). 보통 재생 실패 때 목록 GET 이 하나 늘어나는 것은 작성자가 적은 대로다.

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd app && fvm flutter analyze` | No issues found! |
| `cd app && fvm flutter test` | **+320 ~67 All tests passed!**(앞 판 +314 → +6) · exit 0 |
