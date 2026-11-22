# day-mobile-v2 M1 결과 보고 — 방 옮기기 · 복귀 · 점유 띠(U-21) · 「간호관리」(U-20)

## 상태: done (커밋 · push · PR 없음 — 워크트리 `CENTURION_DAY/day-mobile-v2` 에 변경만)

base `844eace4`(= origin/dev). 서버 · `backend/` 무수정 · 기존 API · 스냅샷 칸만 사용. 버전 · 빌드 번호 무수정.

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `app/lib/model/board.dart` | `Task.systemDoctor` · `BoardCard.roomId` · `holdRoom`(RoomRef) · `canMoveRoom` · `canHoldMove` · `canReturnRoom` · `BoardSnapshot.rooms`(RoomOption `{id,title,takenBy}`) · `moveRooms(card)` 재묶음 — 관대한 읽기(bool 아니면 false · 모양 다른 holdRoom = null · id 없는 방 · 문자열 아닌 takenBy 버림 · `rooms` 칸 없어도 판 읽음) |
| `app/lib/state/board_controller.dart` | `moveRoom(visitId, roomId, hold:)` → `POST /api/visits/{id}/room-move {mode: hold|all, roomId}` · `returnRoom` → `POST /api/visits/{id}/room-return {}` · 잠금 키 `room:{visitId}` 공유 · `run` 에 오류 글자 함수 선택 인자(빈 글자 = 토스트 없음) |
| `app/lib/core/copy.dart` | 웹 글자 상수 + `roomActionMessage`(웹 `message_of` 와 같은 규칙) |
| `app/lib/ui/room_move.dart`(새) | 방 옮기기 창(폰 바텀 시트 · 아이패드 팝오버) · 점유 띠 `HoldBand` · 조건 함수 |
| `app/lib/ui/doctor_picker.dart` | 시트/팝오버 자리 코드를 `showPickerSurface` 로 꺼내 공용(의사 호출 동작 그대로) · 호출 시트 줄 담당의도 `taskDoctorLabel` |
| `app/lib/ui/widgets.dart` | `DetailHeader.onTitleTap` — 방 이름 누름(제목 옆 ▾ 아이콘) |
| `app/lib/ui/room_screen.dart` | 머리 방 이름 → 방 옮기기 · 머리 위 점유 띠 · 담당의 자리 `taskDoctorLabel` |
| `app/lib/ui/board_screen.dart` | 카드 방 이름 줄 아래 점유 띠 · 상태 박스 담당의 `taskDoctorLabel` |
| `app/lib/ui/format.dart` | `taskDoctorLabel`(원장 이름 > 「간호관리」 > 「담당의 미정」) · `cardDoctor` 같은 규칙 |
| `app/lib/ui/theme.dart` | `Day.roomPopWidth = 320`(웹 `--day-pop-w` 240 · 터치 폭) |
| `app/test/ui/room_move_test.dart`(새) | 모델 · 재묶음 · 간호관리 · 이동 · 점유 이동 · 거절 토스트 · 권한 · 아이패드 · 점유 띠 · 복귀 — 17건 |
| `app/test/capture/room_move_capture_test.dart`(새) | 시각 캡처(`DAY_CAPTURE_DIR` 있을 때만 · 평소 skip) |

### 동작(웹 `board_parts.html` 배치 그대로)
- **방 옮기기 진입** = 룸 상세 머리 방 이름(웹 카드 방 이름 버튼 `:166-170`). 보이는 조건 = `board` edit && (`canMoveRoom` || `canReturnRoom`).
- **창** = 머리(지금 방 이름 · 닫기) · `canReturnRoom` 이면 [복귀하기]만(웹 `room_pop :279`) · 아니면 방 목록 + 「점유 이동」(outline · `canHoldMove` && 고름) · 「이동」(주색 · 고름). 처음 선택 없음. 성공 = 닫힘 · 실패 = 창 그대로.
- **방 목록 재묶음**(U-21 · 웹 `:283-287`): 지금 방(`room.id`) 빼기 → `takenBy` 에서 자기 visitId 빼고 「비어 있음」/「배정됨」 → 빈 방 먼저 · 묶음 안 서버 순서.
- **점유 띠**(웹 `:174-178` · `.day-card__hold`): `holdRoom` 있으면 목록 카드(방 이름 줄 아래) · 룸 상세(머리 위)에 옅은 주색 띠 · 원래 방 이름 + [복귀하기](`board` edit && `canReturnRoom`) · 확인 창 없이 바로.
- **「간호관리」**: 줄 `doctor` 없고 `systemDoctor` 면 룸 상세 진행중 · 완료 줄 · 목록 카드 상태 박스 담당의 자리(OQ-A58 확인 — 카드 담당의는 그 줄 값에서 옴 · `doingSummary` 대표 줄 / `cardDoctor` 첫 비완료 줄). **누르는 동작 없음.**
- 성공 토스트 없음(OQ-A56). 실패 토스트 = 웹 규칙(OQ-A57): `room_held` · `room_same` · `room_not_held` · `visit_not_on_board` 등 웹 `UNSET_MESSAGES` = 토스트 없음 · 표에 있는 코드 = 그 글자 · 그 밖(`conflict`) = 「요청이 올바르지 않습니다」 · 403 = 기존 권한 글자.

## 글자 출처 (CENTURION_DAY `backend/day/...`)
| 글자 | 출처 |
|---|---|
| 「복귀하기」 | `templates/partials/board_parts.html:178` · `:279` (스펙 U-21 「복귀」는 웹 글자 그대로 = 「복귀하기」) |
| 「점유 이동」 · 「이동」 | `board_parts.html:290` · `:291` |
| 「비어 있음」 · 「배정됨」 | `board_parts.html:286` |
| 「간호관리」 | `board_parts.html:83` |
| 「담당의 미정」 | 앱 기존 글자(`room_screen.dart` 0.1.0) |
| 「요청이 올바르지 않습니다」 · 토스트 비움 코드 목록 | `routers/board_messages.py` `MESSAGES` · `UNSET_MESSAGES` · `routers/board.py:599-607` `message_of` |

## 비운 글자(원천 없음 — 짓지 않음)
- 방 옮기기 · 복귀 **성공 토스트**(OQ-A56) — 없음.
- 거절 코드 `room_held` · `room_same` · `room_not_held` · `visit_not_on_board` 토스트(OQ-A57 · 웹도 비움) — 없음.
- 방 옮기기 창 머리 제목 — 웹 팝오버 제목 = 지금 방 이름 그대로(별도 「방 옮기기」 글자 없음).
- 점유 띠 앞 설명 글자(예: 「점유 중」) — 웹에 없어 방 이름만.

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+372 ~75 All tests passed**(~75 = 캡처 테스트 · 평소 skip — 새 테스트 17건 포함 · 기존 실패 없음) |
| `fvm flutter build ios --no-codesign` | ✓ Built `build/ios/iphoneos/Runner.app` (20.7MB) |
| `DAY_CAPTURE_DIR=… flutter test test/capture/room_move_capture_test.dart` | 2/2 통과 · PNG 10장 |

캡처가 아이패드 복귀 팝오버의 11px 넘침을 잡아 고침(높이 140 → 180) · 그 경우를 위젯 테스트에 넣음.
실제 시뮬레이터 · 기기 · 로컬 백엔드는 쓰지 않았다(사용자 포트 · 프로세스 · 기기 무접촉) — 캡처는 실제 `DayApp` 위젯 트리 + 테스트 더블 스냅샷. **실기기 · dev 서버 확인(A-50)은 pending(사용자 몫).**

## 캡처 (`orchestration/work/day-mobile-v2/shots/`)
`m1-{phone,ipad}-board-hold-band.png`(목록 · 점유 띠 · 「간호관리」 상태 박스) · `m1-{phone,ipad}-room-nurse-care.png`(룸 상세 진행중 · 완료 줄 「간호관리」) · `m1-{phone,ipad}-room-move-sheet.png`(방 목록 · 고름) · `m1-{phone,ipad}-room-hold-band.png`(룸 상세 점유 띠) · `m1-{phone,ipad}-room-return-sheet.png`(복귀만 창)

## 계약 대조
| 항목 | 같음/다름 |
|---|---|
| API `room-move {mode, roomId}` · `room-return {}`(`routers/api/board.py:284-322` · `schemas/board.py:75`) | 같음 |
| 스냅샷 칸 `canMoveRoom` · `canHoldMove` · `canReturnRoom` · `holdRoom` · `rooms[].takenBy` · `tasks[].systemDoctor`(`schemas/board_responses.py`) | 같음 · 앱 판정 없음 |
| 방 목록 재묶음(U-21 · W-2) | 같음 |
| 점유 띠 목록 카드 · 룸 상세(W-3) | 같음 |
| U-20 「간호관리」 누름 → 원장 바꾸기 | **이번 아님**(브리프 — `canChangeDoctor` 뒤 다음 M) |

## 이슈 · 코디가 확인할 것
1. **배치 결정(시안 없음 · OQ-A54)**: 방 옮기기 진입 = 룸 상세 머리 방 이름(웹과 같은 자리). 앱에는 hover 가 없어 눌리는 줄 보이게 **방 이름 옆 ▾ 아이콘**을 더했다(글자 아님). 목록 카드 방 이름은 누르면 룸 상세(기존 동작)라 진입을 두지 않았다 — 점유 띠 [복귀하기]만 카드에서 바로.
2. 점유 띠 모양 = 웹 `.day-card__hold` 색(옅은 주색 · 주색 글자 12px) · 앱은 카드 안 둥근 띠(웹은 카드 폭 가득).
3. 아이패드 팝오버 폭 320(웹 240) — 터치 버튼 두 개 폭.
4. 의사 호출 시트의 시술 줄 담당의 글자도 같은 `taskDoctorLabel` 을 쓴다(시스템 계정 줄이면 「간호관리」) — 범위 밖이라 보면 되돌릴 수 있음.
5. 기존 다른 조작의 표 밖 코드는 여전히 코드 그대로(`codeOnly`) — 방 조작만 웹 `message_of` 규칙을 따름(OQ-A57 을 전 조작에 넓히는 건 이번 아님).
