# day-mobile-v2 M2 고침 결과 보고 — 검수 FAIL 1 · WARN 3

## 상태: done (커밋 · push · PR 없음)

base = M3 `ecea81d4` 위. `backend/**` 는 읽기만(F1 변경은 내 것 아님).

## 항목별

| 검수 | 고친 것 | 파일 |
|---|---|---|
| **F-1 FAIL** 원장 변경 창 「호출할 시술 · 1개」 | `procs: const []` — 웹 원장 변경 창(`ui.html:406` single)처럼 시술 칸 안 그림. 아이패드 오른쪽 칸엔 「선택됨」만 | `app/lib/ui/room_screen.dart:528` |
| **W-1** 바로 시작 `rejected[]` 토스트 | 웹 `routers/board.py:628-629` 와 같게 — 코드 **중복 없이 처음 나온 순서** · 글자 미정 코드 뺌 · **한 장씩 차례로**(앱 토스트 칸이 하나라 `ToastBus.showAll` 큐 — 지금 장이 2.6초 뒤 사라지면 다음 장). 새 `show` 는 기다리는 장을 버림(새 일이 앞 일을 덮음 — 기존 동작 그대로) | `app/lib/core/toast.dart` · `app/lib/state/board_controller.dart` |
| **W-2** 캡처 메뉴 검은 테두리 | 캡처 테스트에서 `debugDisableShadows = false`(끝에 되돌림) → `shots/m2-*.png` 10장 다시 찍음(덮어씀). ⋮ 메뉴 · 시트 · 팝오버가 실기기처럼 옅은 그림자로 보임 | `app/test/capture/m2_capture_test.dart` |
| **W-3** 호출 취소 ⋮ `state == 'called'` | 조건 = `board` edit && 서버 `canCancelCall` 만 | `app/lib/ui/room_screen.dart:578` |

## 테스트
- `app/test/core/toast_queue_test.dart`(새 · 2) — 차례 · 다른 id 무시 · 새 show 가 큐 버림 · 빈 목록
- `app/test/ui/m2_actions_test.dart` — 원장 변경 창에 「호출할 시술」 없음 단언 · 새 1건: `rejected[]` = call_not_accepted · task_not_called(미정) · call_not_accepted(중복) · task_not_waiting → 「호출이 아직 수락되지 않았습니다」 → 2.6초 뒤 「이미 시작했거나 끝난 시술입니다」 → 끝(두 장)

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+412 ~79 All tests passed**(M3 뒤 409 → 412) |
| `fvm flutter build ios --no-codesign` | ✓ Built `Runner.app` (20.8MB) |
| 캡처 `DAY_CAPTURE_DIR=… flutter test test/capture/m2_capture_test.dart` | 4/4 · `m2-*.png` 10장 다시 |

## 코디가 볼 것
1. 검수 「참고」(범위 밖): 앱 U-6 대리 수락 창(`accept.dart`)도 「호출할 시술 · N개」 칸을 그린다(웹 수락 창 = single · 칸 없음). 0.1.0 부터의 배치라 이번엔 안 건드림 — 사용자 · 코디 판단.
2. M1 캡처(`m1-*.png`)도 같은 하네스 영향(그림자 → 검은 선)이 있을 수 있다 — 이번 범위(m2)만 다시 찍음.
3. 아이패드 원장 변경 창은 여전히 두 칸 팝오버(오른쪽 「선택됨」) — 웹 single 은 한 칸. 내용은 같고 배치만 앱 U-6 꼴.
