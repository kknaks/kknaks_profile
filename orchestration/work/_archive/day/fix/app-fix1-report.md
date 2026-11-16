# fix 앱 수정 1 — 리뷰 W1 + 참고 R1 ~ R5 결과 보고

## 상태: done (미커밋 · `app/lib` · `app/test` 만 · 통역 폴더 · `pubspec` 무변경 · 새 화면 글자 0 · 새 의존성 0)

근거: `review-app-report.md`(WARN 1 · 참고 5 · 조용히 통과 2) · SPEC-004 U-1 `:155-159` · C-A19 · U-7 `:221`.

## 항목별

| # | 고친 자리 | 무엇 |
|---|---|---|
| W1 | `lib/chat/chat_state.dart:269` `_guard` | **채팅 HTTP 공통 403** — 감싼 호출이 403 `forbidden` 이면 `_forbidden()`(거절 상태 · 메모리 비움 · 스트림 멈춤 · 토스트 없음) 뒤 오류를 다시 던짐. 감쌈: `delete:856` · `edit:863` · `forward:870` · `people:888` · `openDirect:891` · `createGroup:899` · `addMembers:907` · `leave:915` · `hide:922` · `mute:953` · `attachments:960` |
| W1 | `lib/chat/chat_state.dart` `_load`(사진 · 썸네일 바이트 `photo:963` · `thumb:966`) | 403 = `_forbidden()`(전엔 조용히 빈 칸) |
| W1 | `lib/chat/screens/chat_new_screen.dart:58-63` | 직원 목록 403 = 화면 안 글자(`_error`) 없이 끝 — 거절 안내는 ChatState → 셸 |
| W1 | `lib/chat/screens/chat_media_screen.dart:71 · 80-82` | `_app.api.attachments` 직접 호출 → `_chat.attachments`(감싼 것) · 403 = `_failed`(「불러오지 못했어요」) 아님 |
| W1 (리뷰가 못 본 자리) | `lib/chat/screens/chat_forward_sheet.dart:84-93` | 전달 시트 직원 목록 `onError` 가 모든 오류를 `_peopleFailed` 로 삼켰다(403 · **401 도**) → 401 · 403 은 `chat.handle`(세션 끝 · 거절) |
| W1 (리뷰가 못 본 자리) | `lib/chat/screens/chat_video_screen.dart:113-124` | 재생기(`VideoPlayerController.networkUrl`)는 HTTP 상태를 주지 않아 403 을 「동영상을 찾을 수 없어요」 토스트로 냈다 → 재생 실패 때 목록을 한 번 읽어(`refreshRooms` — 403 이면 거절) 거절이면 토스트 없이 안내로 · 아니면 기존대로 토스트 + 닫기 |
| R1 | `lib/state/board_controller.dart:35` `homeLockKey` · `:188` `home()` 가 그 함수 사용 · `room_screen.dart` 의 정의 지움 | 잠금 키 문자열 한 곳 |
| R2 | `lib/ui/board_screen.dart:326` | `c.allDone && canSendHome(c, me)` — `waitingCalls.isEmpty` 뺌(방 상세와 글자 그대로 같은 조건) |
| R3 | `lib/notify/notification_controller.dart:75 · 85-94` `beginSettingsRead` · `applySettings(settings, seq)` · `lib/notify/notification_settings.dart:36-40` | 설정 읽기 순번 — **가장 나중에 보낸** 읽기의 응답만 적용(늦게 온 옛 응답 버림) |
| R4 | `lib/chat/chat_state.dart:256` | `_recheck` 가 풀려 스트림을 연 뒤 그 사이 앱이 뒤면 바로 `pause`(다음 앞으로 올 때 `resume`) |
| R5 | `lib/chat/screens/chat_info_screen.dart:185-188` `_canSave` · 입력 포매터 뺌 | 40자 = 앞뒤 공백 뺀 뒤 셈 · 넘으면 [✓] 꺼짐(새 글자 없음) |
| 조용히 통과 2 | `test/chat/chat_state_test.dart` 「거절 상태에서는 배너 없음 — 같은 시험 안 대조 …」 | 같은 시험 안에서 거절 아님 = 배너 있음 → 거절 뒤 = 없음 |

## 채팅 HTTP 호출 자리 전수 (`app/lib/chat/` grep — `api.<메서드>(` · `_app.api.` · 재생 주소)

`ChatApi` 메서드 22개(`chat_api.dart`) · 호출 자리 26곳. 403 이 거절로 가지 않는 자리 **0**.

| # | 자리 | 호출 | 403 처리 |
|---|---|---|---|
| 1 | `chat_state.dart:368` `refreshRooms` | `GET /rooms` | catch → `_handleError` → `_forbidden`(기존) |
| 2 | `:393` `loadLatest` | `GET …/messages` | catch → `_handleError`(기존) |
| 3 | `:422` `loadOlder` | `GET …/messages?beforeSeq` | catch → `_handleError`(기존) |
| 4 · 5 | `:458 · :461` `catchUp` | `GET …/messages?since` · 최근 50 | catch → `_handleError`(기존) |
| 6 | `:533` `_markRead` | `POST …/read` | catch → `_handleError`(기존) |
| 7 · 8 · 9 | `:822 · :827 · :832` `_deliver` | 사진 · 동영상 올리기 · `POST …/messages` | 4xx → `_handleError`(기존) |
| 10 | `:856` `delete` | `DELETE /messages/{id}` | `_guard`(새) + 화면 `run()` → `handle` |
| 11 | `:863` `edit` | `PATCH /messages/{id}` | `_guard`(새) + 화면 `handle`(기존) |
| 12 | `:870` `forward` | `POST …/forward` | `_guard`(새) + 시트 4xx → `handle`(기존) |
| 13 | `:888` `people` | `GET /people` | `_guard`(새) — 새 대화 · 전달 시트 두 화면이 씀 |
| 14 | `:891` `openDirect` | `POST /rooms/direct` | `_guard`(새) + `run()` |
| 15 | `:899` `createGroup` | `POST /rooms` | `_guard`(새) + `run()` |
| 16 | `:907` `addMembers` | `POST …/members` | `_guard`(새) + `run()` |
| 17 | `:915` `leave` | `POST …/leave` | `_guard`(새) + `run()` |
| 18 | `:922` `hide` | `POST …/hide` | `_guard`(새) + `run()` |
| 19 | `:934` `rename` | `PUT …/title` | catch → `_handleError`(앞 판) |
| 20 | `:953` `setMuted` | `PUT …/mute` | `_guard`(새) + `run()` |
| 21 | `:960` `attachments` | `GET …/attachments` | `_guard`(새) — 모아보기가 이제 이것을 씀 |
| 22 | `:963` `photo` → `_load` | `GET /photos/{id}` | `_load` catch → `_forbidden`(새) |
| 23 | `:966` `thumb` → `_load` | `GET /videos/{id}/thumbnail` | 같음(새) |
| 24 | `chat_media_screen.dart:71`(전 `_app.api.attachments` 직접) | → 21 로 바꿈 | 거절(새) · 화면 `_failed` 안 됨 |
| 25 | `chat_video_screen.dart:90` `videoUri` + `authHeaders` → 재생기 | `GET /videos/{id}` | 재생기는 상태 코드 없음 → 실패 때 `refreshRooms`(1번)로 판정(새) |
| 26 | `chat_stream.dart:88` 채팅 스트림 | `GET /api/chat/stream` | 403 = `_running=false` · `onSessionEnd('forbidden')` → `_forbidden`(기존) |

(알림 API `notify/` 는 채팅 HTTP 가 아니다 — 대상 밖.)

## 시험 (새 · 바뀐 것)

| 파일 | 이름 | 항목 |
|---|---|---|
| `test/ui/chat_ui_test.dart` | 「새 대화 — 직원 목록 403 = 화면 안 글자 없이 닫히고 채팅 탭 = 권한 없음 안내 · 토스트 0」 | W1 |
| 〃 | 「사진 · 동영상 모아보기 403 = 「불러오지 못했어요」 아님 · 열린 대화 · 방 정보 닫고 권한 없음 안내」 | W1 |
| 〃 | 「아이패드 — 방 정보 시트(세션 Navigator 위)에서 모아보기 403 = 시트도 닫힘」 | W1 |
| 〃 | 「그룹 — … 바꿈 → PUT …」 안 40자 부분(41자 ✓ 꺼짐 · 앞뒤 공백 붙은 40자 ✓ 켜짐) | R5 |
| `test/chat/chat_state_test.dart` | 「그 밖 채팅 HTTP 403 도 거절로(W1) — 직원 목록 · 모아보기 · 사진 바이트 · 알림 · 초대 · 나가기 · 숨기기 · 삭제 · 수정 · 전달 · 1:1 · 그룹」(11 호출 + 사진 · 썸네일 — 각 거절 · 토스트 0) | W1 |
| 〃 | 「풀린 뒤 스트림을 여는 사이 앱이 뒤로 갔으면 열어 두지 않는다 · 다음에 앞으로 오면 붙음(R4)」 | R4 |
| 〃 | 「거절 상태에서는 배너 없음 — 같은 시험 안 대조: 거절 아님 = 배너 있음」 | 조용히 통과 2 |
| `test/notify/notification_contract_test.dart` | 「늦게 온 옛 설정 응답은 새 값을 덮지 않는다 — 가장 나중에 보낸 읽기의 응답만(R3)」(앞으로 옴 GET 을 붙잡고 → 끔 PUT 뒤 읽기 먼저 → 옛 응답 늦게 도착 = 버림) | R3 |
| 〃 | 기존 「start 에 읽음 …」 — `applySettings(l, c.beginSettingsRead())` 로 맞춤 | R3 |

R1 · R2 는 기존 `actions_test` 「이중 탭 잠금 · 룸 상세 [귀가 대기]와 같은 잠금」 · 「보기만 직무 · 서버 canHome false → 줄 없음」이 그대로 지킨다(통과).

## 명령 · 수치

- `cd app && fvm flutter analyze` → No issues found
- 고친 시험만: `test/notify/notification_contract_test.dart` +10 · `test/chat/chat_state_test.dart` +37 · `test/ui/chat_ui_test.dart` +19 — 모두 통과
- 전체 `fvm flutter test` → **+320 ~67(캡처 skip) All tests passed**(앞 판 +314 → +6)

## 비고

- 모아보기 403 UI 시험은 대화 · 방 정보 · 모아보기 세 화면이 한꺼번에 닫히는 전환이라 2초 더 흘린 뒤 확인한다(동작 문제 아님 — 전환 시간).
- 재생기 403(25번)은 재생 실패 때 목록을 한 번 더 읽는 방식이다. 비활성이 아닌 보통 재생 실패(지워진 동영상)는 기존 그대로 「동영상을 찾을 수 없어요」 + 닫기이고, 그때 목록 GET 이 한 번 늘어난다.
