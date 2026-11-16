# WP-APP-1 시술현황 카드 + 앱 후속 2 — 결과 보고

## 상태: done (미커밋 · 워크트리 `CENTURION_DAY/fix` `kknaksss/fix` · `app/` 만)

근거 스펙: mediness `fix-spec` 미커밋 SPEC-003 개정 ⑧ · U-3(5상태 · 모두 완료 카드 [귀가 대기] · 확인 필요 표시 · 겹침 표) · U-4 5번 · U-9 · U-12 · A-9 · A-22 · A-28 · A-33 · A-37 · A-41 ~ A-43 · OQ-A33 · A37 · A38 · A44.
서버 변경 없음 — 서버 값(`needs[]` · `canHome` · `calls[].canRecall` · `version`) 소비만.

## 수행 — 변경 파일 (새 파일 없음)

| 파일 | 무엇 |
|---|---|
| `app/lib/ui/board_screen.dart` | 카드 테두리 빨강 · 굵기 제거(평소 테두리 그대로 — 시술 중 주색 · 그 밖 회색) · `_box` = 확인 필요면 바탕 `Ms.red100` + 왼쪽 띠 `Ms.red`(3px · 글자 자리 그대로) — 호출 상태 상자도 같은 `_box` · `_nowBox` 맨 앞 `card.allDone` → 1줄 「시술 모두 완료」 / 2줄 「마지막 종료 HH:MM」(없으면 비움) · 오른쪽 비움 · 마취가 열려 있어도 이 상태 · 모두 완료 카드 맨 아래 `_homeLine`(위 구분선 · 오른쪽 [귀가 대기] · 왼쪽 글자 없음) |
| `app/lib/ui/room_screen.dart` | `canRecallCall(snap, oc, me)` = 그 호출의 `calls[].canRecall` + `board` edit · 공용 `canSendHome` · `homeLockKey` · `sendHomeAction`(노출 조건 · 잠금 키 `home:{visitId}` · 요청 · 토스트 하나 — 룸 상세 · 목록 카드가 같이 씀) · 모두 완료 상자는 공용 글자 · `lastCompletedAt` 사용 |
| `app/lib/model/board.dart` | `CallItem.canRecall` 읽기 · `BoardSnapshot.callCanRecall(callId)` · `Task.canRecall` 소비 제거(OQ-A33) · `BoardCard.lastCompletedAt`(가장 늦은 `completedAt` — 계산 한 곳) |
| `app/lib/data/board_stream.dart` | `snap.version > current` → `>=`(같은 값 받음 · 미만만 버림) · 머리 주석 |
| `app/lib/ui/format.dart` | 공용 글자 `allDoneLabel` · `lastDoneLabel(DateTime)` · `homeLabel`(룸 상세에 이미 있던 글자를 한 곳으로 옮김 — 새 글자 아님) |
| `app/test/support/fixtures.dart` | `callsOf(cards)` — 서버 calls_view 모양(`canRecall` 포함)을 카드에서 만듦 · `snapshot(calls:)` 생략 시 자동 · 줄에서는 `canRecall` 칸을 지움(서버 줄에 없는 칸) |
| `app/test/ui/status_box_test.dart` · `actions_test.dart` · `data/board_stream_test.dart` · `ui/app_flow_test.dart` · `capture/visual_capture_test.dart` | 아래 표 |

## 수용 항목 ↔ 시험

| 항목 | 시험(파일 · 이름) |
|---|---|
| A-9 같은 version 받음 · 미만 버림 · 새 연결 첫 board | `board_stream_test` 「세션 대상 · Bearer · 첫 board · 미만 version 만 버림 · 같은 version 받음 · 새 연결 첫 board 는 늘 받음(A-9)」 |
| A-22 [재호출] = `calls[].canRecall` · `board` edit | `board_stream_test` 「needs[] 5상황 · lastSeconds · calls[].canRecall …」 · 「[재호출] 근거 = calls[].canRecall 만 — 줄의 옛 tasks[].canRecall 은 읽지 않음 …」 · `app_flow_test` 「[재호출] 노출 = 서버 canRecall · board edit(A-22)」 3건(픽스처가 calls[] 로 실어 줌) |
| A-28 · A-41 모두 완료 = 다섯째 상태 · 같은 글자 · 같은 값 · 오른쪽 비움 · 마취 열림도 모두 완료 | `status_box_test` 「마지막 종료 = 가장 늦은 completedAt …」 · 「목록 상자 = 1줄 「시술 모두 완료」 · 2줄 …· 룸 상세와 같은 글자」 · 「모두 완료 + 마취 열림(초과 포함) = 「시술 모두 완료」 …」 |
| A-42 목록 [귀가 대기] | `actions_test` group 「목록 카드 [귀가 대기](개정 ⑧ · A-42)」 — 노출 · 왼쪽 글자 없음 · 확인 창 없이 POST · 토스트 · 다음 스냅샷 빠짐 / 보기만 직무 · canHome false = 줄 없음 / `tasks_not_done` · `visit_home` · 403 `forbidden` DAY 글자 / 이중 탭 잠금 · 룸 상세와 같은 잠금 · 버튼 밖 = 룸 상세 |
| A-33 룸 상세 모두 완료(회귀) | `actions_test` 「모두 완료 — 강조 상자 …(A-33)」 · 「모두 완료 · canHome 없음(서버) → 상자 글자만」 |
| A-37 · A-43 확인 필요 = 상자 표시 · 테두리 없음 · 겹침 7자리 | `status_box_test` 「겹침 7자리 — 바탕 Ms.red100 + 왼쪽 띠 Ms.red · 상태 글자 색 유지 · 카드 테두리는 평소」 · `app_flow_test` 「확인 필요 = 서버 needs 소비 — 상자 표시(테두리 아님 · 개정 ⑧) …(A-37)」 |

겹침 7자리 적용(OQ-A37 (가)): 1 시술 대기 · 2 마취 끝난 대기 · 3 마취 중(글자 보라) · 4 마취 초과(바탕 이미 빨강 → 띠만 더해짐 · 글자 빨강) · 5 시술 중(글자 주색) · 6 호출 상태(호출 글자 색 그대로) · 7 모두 완료 — 전부 바탕 `Ms.red100` + 왼쪽 `Ms.red` 띠. `needs` 가 비면 표시 없음.

## 새 화면 글자

**없음.** 쓰인 글자 = 「시술 모두 완료」 · 「마지막 종료 {HH:MM}」 · 「귀가 대기」 — 모두 룸 상세 `room_screen.dart` 에 있던 글자(SPEC-003 U-4 5번 · U-9 · DAY 웹 E46)를 `format.dart` 상수 하나로 옮겨 두 곳이 같이 씀. 토스트 「{방} {고객} 귀가 대기」 = 기존 `OkToast.home`(U-13).

## 계약

서버 계약 변경 없음. 앱이 읽는 칸: `cards[].tasks[].state · completedAt` · `cards[].canHome` · `cards[].needs[]` · `calls[].callId · canRecall`(서버 `board_rules.py:861`) · `version`. 보내는 것: `POST /api/visits/{visitId}/home`(본문 없음 — 룸 상세와 같음).

## 명령 · 수치

- `cd app && fvm flutter analyze` → No issues found
- `fvm flutter test test/ui/status_box_test.dart test/ui/actions_test.dart test/data/board_stream_test.dart test/ui/app_flow_test.dart test/ui/session_race_test.dart` → **+95 All tests passed**
- 전체 테스트 · 빌드는 WP-APP-2 끝에 한 번(app-2-report).

## 캡처 (`work/fix/app-captures/`)

- `phone-board-all-done-need-overlap.png` · `ipad-board-all-done-need-overlap.png` — 모두 완료 + [귀가 대기] · 겹침 7자리 + 확인 필요 없는 카드 1장
- `phone-board-need-overlap-filtered.png` · `ipad-board-need-overlap-filtered.png` — 「확인 필요」 칩

## 스펙 · 계획과 다른 곳 · 물을 것

- 「시술 모두 완료」 1줄 글자 색 = 주색(`Ms.primary`) — 룸 상세 강조 상자 글자 색과 맞춤. 스펙은 바탕만 정함(겹침 표 7). 다르게 원하면 한 줄.
- 모두 완료인데 `needs` 가 빈 경우(서버 규칙상 생기지 않음 — U-3 겹침 ③)의 바탕 = 평소 회색(`Ms.gray100`) — 자기 색 미정이라 시술 대기와 같은 회색.
- 띠 굵기 3px(사용자 미정 · OQ-A20 — 구현 값).
- 계획 표의 `session_race_test` 는 기대 변경이 필요 없었다(그대로 통과).

## pending

- 시뮬레이터 · 실기기 확인(이번 발주 금지) — 사용자 TestFlight(wp-plan §7 #1).
