# 리뷰 리포트 — day-mobile-v2 M1(방 옮기기 · 복귀 · 점유 띠 · 「간호관리」) / code (2026-11-20)

대상: 워크트리 `CENTURION_DAY/day-mobile-v2` `app/` 미커밋 변경 전부(9개 수정 + 새 파일 3개). `backend/` 는 읽기만(대조용).
근거: DAY-SPEC-003 U-20 · U-21 · §「오류」 표(:845-853) · OQ-A56 · A57 · A58 · 웹 `backend/day/templates/partials/board_parts.html` · `routers/board_messages.py` · `routers/board.py:599-607` · `routers/api/board.py:284-322` · `schemas/board.py:75` · `schemas/board_responses.py`.

## 판정: PASS (WARN 4 · FAIL 0)

## FAIL

없음.

## WARN

1. **W-1 · 스펙 글자 「복귀」 vs 구현 「복귀하기」(문서 쪽 정정 권고)** — `app/lib/core/copy.dart:94` 는 `'복귀하기'`. 스펙 U-21(spec-003 :507)은 「버튼 글자 = 웹 「복귀」 글자 그대로」라고 썼지만 실제 웹 글자는 `board_parts.html:178` · `:279` 「복귀하기」다. 구현이 웹 원천을 따른 것은 맞다(M-9 「원천에 있는 것만」). 스펙 문장을 「복귀하기」로 고치지 않으면 다음 검수자가 오해할 수 있다. → 스펙 정정(코드 그대로).
2. **W-2 · 웹 거절 글자 표 복제의 동기화 장치 없음** — `app/lib/core/copy.dart:105-119` `unsetActionCodes` · `roomActionMessage` 는 지금 웹 `board_messages.py` `UNSET_MESSAGES`(8개)와 `message_of` 규칙과 정확히 같다(대조 확인). 다만 손으로 복제한 값이라 서버가 코드를 더하거나 빼면 앱은 모른다. 「서버 계산 값만」 원칙상 판정이 아닌 글자 표라 FAIL 은 아님. 기존 `actionMessages` 도 같은 방식이라 기존 부채와 같은 성격.
3. **W-3 · 거절 위젯 테스트의 「토스트 없음」 단언이 약함** — `app/test/ui/room_move_test.dart:190` · `:250` 은 `find.text('room_held')` · `find.text('room_not_held')` 가 없는지만 본다. 앱이 잘못해서 「요청이 올바르지 않습니다」를 띄워도 이 줄은 통과한다. 같은 파일 `:270-274` 단위 테스트(`roomActionMessage('room_held') == ''`)가 실제 계약을 지키고, `:195` 의 `findsOneWidget` 이 간접 방어라 실질 위험은 낮다. 보강 권고: `:190` 에 `expect(find.text('요청이 올바르지 않습니다'), findsNothing)`, `:250` 에도 같은 단언.
4. **W-4 · 시안 없이 정한 배치 3건(OQ-A54 — 사용자 판단 몫)** — 사용자 결정(시안 없음 · 기존 컴포넌트 + 웹 배치)에 맞지만 웹과 다른 점이 있다. 실물에서 확인할 것:
   - 방 이름 옆 ▾ 아이콘 `app/lib/ui/widgets.dart:493` — 글자가 아니라 지은 글자에는 해당하지 않음. 웹에는 없음.
   - 아이패드 팝오버 폭 320 `app/lib/ui/theme.dart`(`Day.roomPopWidth`) — 웹 `--day-pop-w` 240.
   - 목록 카드 방 이름에서는 방 옮기기로 들어가지 않음(누르면 기존처럼 룸 상세). 카드에서는 점유 띠 [복귀하기]만 바로 된다. 웹은 카드 방 이름이 곧 진입점(`board_parts.html:166-170`). 스펙 U-21 「자리 = 룸 상세 머리」와는 맞다.

## 항목별 대조

### 1. 스펙 U-20 · U-21 · 서버 칸만 쓰는지 · API — PASS
| 항목 | 근거 | 판정 |
|---|---|---|
| 메뉴 보임 = `board` edit && (`canMoveRoom` \|\| `canReturnRoom`) | `app/lib/ui/room_move.dart:18` = 웹 `board_parts.html:166` | 같음 |
| [복귀하기] = edit && `canReturnRoom` | `room_move.dart:21` · `:249` = 웹 `:178` | 같음 |
| 점유 중이면 [복귀하기]만 | `room_move.dart:114-126` = 웹 `:279` | 같음 |
| 「점유 이동」 = `canHoldMove` && 고름 · 「이동」 = 고름 | `room_move.dart:141` · `:151` = 웹 `:290-291`(`data-day-room-submit` 조건) | 같음 |
| 재묶음: 지금 방 빼기 → takenBy 에서 자기 빼기 → 빈 방 먼저 · 묶음 안 서버 순서 | `app/lib/model/board.dart:380-389` = 웹 `:283-287` · 스펙 U-21 ①②③ | 같음(판정 아닌 목록 묶기 — 스펙이 허용한 표시 예외) |
| 점유 띠 = `holdRoom` 있으면 목록 카드 · 룸 상세 | `board_screen.dart:310-313` · `room_screen.dart:154-160` · `room_move.dart:217-256` = 웹 `:174-178` | 같음 |
| `POST /api/visits/{id}/room-move {mode: hold\|all, roomId}` | `board_controller.dart:179-185` = `routers/api/board.py:284-301` · `schemas/board.py:75`(`RoomMoveBody` forbid · mode Literal) | 같음 |
| `POST /api/visits/{id}/room-return {}` | `board_controller.dart:188-189` = `routers/api/board.py:304-322`(빈 본문 또는 `EmptyBody`) | 같음 |
| 스냅샷 칸 이름(`canMoveRoom` · `canHoldMove` · `canReturnRoom` · `holdRoom` · `rooms[].takenBy` · `tasks[].systemDoctor`) | `schemas/board_responses.py:142 · 249-252 · 433 · 485` | 같음 |
| 「간호관리」 = 원장 이름 없고 `systemDoctor` | `app/lib/ui/format.dart:152-157` = 웹 `board_parts.html:83` 순서(doctor.name > 간호관리) · 스펙 U-20 | 같음 |
| 목록 카드 상태 상자도 같은 규칙(OQ-A58) | `board_screen.dart:430` · `format.dart:159-166` | 같음 |
| 「간호관리」 누름 → 원장 바꾸기(U-20 3번째 줄 · U-22) | 이번 M 범위 밖(브리프 · 리포트) — 누름 없음 테스트 `room_move_test.dart:128` | 범위 밖(다음 M) |
| 성공 토스트 없음(OQ-A56) | `moveRoom` · `returnRoom` 이 `ok` 에 null 을 넘김 | 같음 |
| 실패 토스트 = 웹 `message_of`(OQ-A57 · 스펙 :853) | `copy.dart:118-119` = `routers/board.py:599-607` | 같음 |

앱이 새로 판정하는 곳: 없음. `HoldBand` · 패널에서 쓰는 조건은 모두 서버 `can*` 와 `/me` `board` edit 뿐이다.

### 2. 글자 출처 — PASS (지은 글자 0)
| 글자 | 앱 | 원천 |
|---|---|---|
| 복귀하기 | `copy.dart:94` | `board_parts.html:178` · `:279` |
| 점유 이동 · 이동 | `copy.dart` roomHoldMoveLabel · roomMoveLabel | `board_parts.html:290` · `:291` |
| 비어 있음 · 배정됨 | `copy.dart` roomFree/TakenLabel | `board_parts.html:286` |
| 간호관리 | `copy.dart:101` | `board_parts.html:83` |
| 담당의 미정 | `copy.dart:102` | 앱 0.1.0 기존 글자(스펙 U-20 `room_screen.dart:484`) |
| 요청이 올바르지 않습니다 · 대상을 찾을 수 없습니다… | 기존 `actionMessages` | `board_messages.py` `MESSAGES` |
| 창 머리 = 지금 방 이름 · 닫기 | `room_move.dart:96` · 기존 `closeLabel` | 웹 팝오버 제목 = 방 이름(`:278`) |

### 3. 관대한 읽기 — PASS
- `_b(v) => v == true` (`board.dart:7`): `can*` · `systemDoctor` 칸이 없거나 bool 이 아니면 false.
- `RoomRef.parse` 는 id 가 없거나 문자열이 아니면 null이고, 그러면 띠를 그리지 않는다. `RoomOption.parse` 는 id 가 없으면 버리고, takenBy 에서 문자열이 아닌 값을 버린다. `rooms` 칸이 없으면 `const []`(`board.dart:373` — `_list` 는 Map 이 아닌 원소를 버림).
- `roomId == null` 이면 모든 방이 목록에 나온다(웹 `here = ""` 와 같음).
- 패널을 열어 둔 사이 카드가 판에서 빠지거나 조건이 꺼지면 머리만 그린다(`room_move.dart:109-111`). 고른 방이 목록에서 빠지면 선택을 풀어 버튼이 꺼진다(`:129`).
- 위 동작은 테스트 `room_move_test.dart:64-80` 이 확인한다.
- 정의 쪽 null-aware 원소 `?RoomOption.parse(r)` 는 SDK `^3.12.2`(pubspec)에서 문법상 허용된다. analyze 통과.

### 4. 회귀 — PASS
- **의사 호출 시트**: `showPickerSurface` 로 꺼냈다(`doctor_picker.dart:49-85`). 의사 호출 기본값 phoneHeight 0.88 · popWidth `callPopWidth` 는 그대로다. 높이식 `:109-110` 은 cap=560 일 때 `max(280, min(560, x))` 로 예전 식과 같다. `actions_test.dart`(60건, 320 폭 고르기 창 overflow 포함)가 통과한다.
- **카드 누름**: 점유 띠 [복귀하기]를 눌러도 룸 상세를 열지 않는다(테스트 `:232`). 띠의 나머지 자리나 보기 권한일 때는 기존처럼 카드 누름 그대로다.
- **DetailHeader**: `onTitleTap == null` 이면 위젯 트리가 예전과 같다(`widgets.dart` 분기). 쓰는 곳은 룸 상세(centerTitle) 하나다.
- **리포트 이슈 4(`taskDoctorLabel` 을 호출 시트 줄에도 씀, `doctor_picker.dart:339`)**: 웹 호출 목록도 같은 `proc` 매크로(`board_parts.html:83`)로 「간호관리」를 보이므로 웹 배치와 맞다. `systemDoctor` 는 진행중 · 완료 줄에서만 오고, 호출 시트에서 그 줄은 이미 잠긴 줄이라 동작은 바뀌지 않는다. 되돌릴 필요 없음.
- **`cardDoctor` 변경**(`format.dart:159-166`): 비완료 줄 중 원장 이름 또는 「간호관리」가 있는 첫 줄을 고른다. 원장 이름만 있을 때는 예전과 같은 결과다(테스트 `:101-105`).
- **`run` 시그니처**(`board_controller.dart:123-145`): 끝에 위치 인자 하나를 더했다. 기존 호출부는 그대로이고, `message` 가 없으면 `actionMessage` 를 쓰므로 기존 갈래가 같다. 빈 글자면 토스트를 띄우지 않는 갈래는 방 조작에서만 생긴다.
- **잠금 키 `room:{visitId}`**: 이동 · 복귀 · 띠 · 패널이 같은 키를 써서 이중 탭을 막는다(A-11).

### 5. 테스트 · 정적 검사 — PASS (W-3 참고)
- 테스트는 실제 `DayApp` 트리와 테스트 더블 서버로 보낸 경로와 본문을 단언한다(`expectSent` — `:162` all · `:177` hold · `:230` · `:243` return `{}`). 버튼 꺼짐은 요청 수가 그대로인지로 확인한다(`:153` · `:160`). 보기 권한, 아이패드 팝오버, 넘침 경우도 덮는다. 빈 단언이나 「조용히 통과」하는 자리는 W-3 외에 없다.
- `fvm flutter analyze` → **No issues found!**
- `fvm flutter test test/ui/room_move_test.dart test/ui/actions_test.dart test/ui/status_box_test.dart test/ui/detail_polish_test.dart test/capture/room_move_capture_test.dart` → **+60 ~2 All tests passed!**(~2 = 캡처 · `DAY_CAPTURE_DIR` 없으면 skip)
- 캡처 `shots/m1-phone-room-move-sheet.png` · `m1-phone-board-hold-band.png` 를 보고 확인했다: 빈 방이 먼저 나오고, 지금 방이 빠졌고, 띠에 원래 방과 [복귀하기]가 있고, 상태 상자에 「간호관리」가 보인다.

### 계층 · 금지 사항 — PASS
- 하드코딩 주소 · 비밀값 · 가짜 계정 없음(경로는 상대 `/api/...` + 세션 `apiBaseUrl`).
- `backend/` 무수정(이번 M1 변경 기준). 버전 · 빌드 번호 무수정.

## 직원이 실물에서 만날 자리
- 룸 상세 머리 방 이름 ▾ 를 눌러야 방 옮기기가 열린다. 목록 카드 방 이름을 누르면 룸 상세로 간다(웹과 다름, W-4).
- 거절 코드 `room_held` · `room_same` · `room_not_held` · `visit_not_on_board` 는 아무 토스트 없이 시트가 그대로 남는다. 직원은 「눌렀는데 아무 일도 없다」로 느낄 수 있다(OQ-A57 · 웹과 같음 — 글자는 사용자 몫).
- 「점유 이동」은 병원 설정에 「방 배정」 id 가 없으면 늘 꺼져 있다(`canHoldMove` · 웹 리뷰 W2).
- 「간호관리」는 아직 누를 수 없다. 원장 바꾸기(U-22)는 다음 M이다.
- 실기기 · dev 서버 확인(A-50)은 아직 하지 않았다(사용자 몫).

## 참고(기존 부채)
- 기존 조작은 표 밖 코드를 여전히 코드 그대로 보인다(`copy.dart:52` `actionMessage` → `codeOnly`). 방 조작만 스펙 :853 규칙(「요청이 올바르지 않습니다」)을 따른다. :853 은 0.2.0 전체의 「새 오류 코드」 기준이라, 다른 조작에 넓히는 일은 후속 M에서 확인이 필요하다(리포트 이슈 5).
- 웹은 원장이 없는 호출 중 줄의 원장 칸을 「전체」 또는 호출 대상 이름으로 채운다(`board_parts.html:83`). 앱 호출 시트는 0.1.0 부터 「담당의 미정」이다. 이번 변경 범위 밖이다.
