# 리뷰 리포트 — day-app 룸 상세 다듬기(SPEC-003 개정 ④) / code + 시각 (2026-11-10)

- 대상: `CENTURION_DAY/day-app` HEAD `47be2cb0` 위 미커밋 변경.
- 기준: spec tree HEAD = `4a5d4a4705b07fd66272867d85115376b1289400`(개정 ④ — 직접 확인).
- 원천: `detail-polish-code-brief.md` · `detail-polish-code-report.md` · `review-detail-polish-spec-report.md`.
- 방식: read-only. 코드 · spec · 서버 · 시뮬레이터 조작 0, 하위 위임 0. 로그는 `review-detail-polish-logs/`.

## 판정: **PASS**

FAIL 과 WARN 은 없다. 개정 ④ 의 세 항목(① 머리 전체 폭 정가운데 ② 미수락 호출만 상자 ③ 시술 행 5상태)은 코드와 최종 PNG 모두 스펙 U-4 :227 · :231 · :236, U-6 :256, A-31, A-39 와 같다.

## 변경 범위

- `git status`: 바뀐 파일은 `app/lib/ui/room_screen.dart` · `app/lib/ui/widgets.dart` · `app/test/capture/visual_capture_test.dart` 와 새 `app/test/ui/detail_polish_test.dart` 4개뿐이다(app/ 만).
- 서버 · env · native · 서명 · 목록(`board_screen`) · 호출 시트 · 수락(`accept.dart`) · 셸 · 세션은 바뀌지 않았다.
- 수정 시각: 소스 15:03:05–15:06:08 → mobile 의 analyze 15:06:35 · 전체 test 15:06:45 · capture 15:06:58 · build 15:07:33 / 15:07:58 · PID 15:08:14. **모든 로그가 마지막 소스 수정 뒤에 찍혔다.**

## 실행 — 내가 직접 돌린 것 / 보고만 본 것

| 구분 | 명령 | 결과 |
|---|---|---|
| 직접 | `fvm flutter analyze` | No issues · exit 0 |
| 직접 | `fvm flutter test test/ui/detail_polish_test.dart test/ui/actions_test.dart test/ui/app_flow_test.dart test/ui/status_box_test.dart`(좁은 관문 1회) | **+65 · 0 fail** · exit 0 |
| 직접 | backend `day-procedure-board-2@a1c90b9d` `board_rules.py:268-280` `start_block` 읽기 | 호출 중(`effective_call` 있는데 accepted 아님) → `call_not_accepted` = **canStart false** · 준비중 + KOS 담당의 → **true** · 담당의 없음 → false |
| 보고만 | mobile 전체 test · unsigned build · sim build | 200 pass · 29 skip(로그 확인) · ✓ 17.5MB · ✓ Built |
| 보고만 | 표준 `lib/main.dart` · 로컬 dart-define | build 로그에 dart-define 줄이 없어 보고서 서술로만 확인 |
| 보고만 | sim PID | 28681(`simulator-pid.txt`) |

## 코드 대조

### ① 머리 — 방 이름을 머리 전체 폭 정가운데에

- 방식: `widgets.dart` 의 `DetailHeader` 에 `centerTitle` 옵션을 더했다. 이 값을 켜는 곳은 `room_screen.dart:134` 하나뿐이다. 기본값 false 일 때는 이전 Row 모양 그대로다(그 밖의 화면은 기본값 보존).
- 가운데 계산: `_CenteredTitleLayout` 이 뒤로 버튼을 왼쪽에 둔다. 제목 최대 폭은 `width − 2×(뒤로 폭+8)`, x 는 `(width − 제목폭)/2` 다. Container 좌우 padding 이 4/4 로 대칭이라 결과가 머리 전체 폭의 가운데가 된다(뒤로 버튼을 뺀 나머지의 가운데가 아니다).
- 긴 이름은 말줄임된다. 뒤로 버튼 InkWell · Semantics(label = 「시술현황」 · excludeSemantics)는 이전과 같아서 겹침이 없다.

### ② 호출 강조 상자 — 미수락 줄이 남은 호출만

- `room_screen.dart:156`: `if (oc.waiting)`. `waiting` = 그 호출에 `called` 줄이 남았는지다.
- 전부 수락된 호출은 숨긴다. 부분 수락이거나 여러 호출 중 미수락 호출이면 상자를 그대로 보인다.
- 상자 내용(대상 · 건수 · 기준 · 큰 경과 · 재호출 = canRecall · 직무별 수락 `acceptCall`)과 목록 · 호출 탭은 바뀌지 않았다.

### ③ 시술 행 5상태 (`_taskCard`)

| 항목 | 코드 | 판정 |
|---|---|---|
| 1줄 = 제목 왼쪽 · 시간 오른쪽 | 진행중 = `elapsedMmss`(기존 함수 · 분 누적 · 22pt) / 완료 = 「완료 {spanMin}」 · 값이 없으면 「완료」 / 그 밖 없음 | PASS |
| 2줄 = 담당의 왼쪽 + 조작 오른쪽 | 진행중 「담당의 · HH:MM 시작」 · 빈 값이면 「담당의 미정」 | PASS |
| [시작] — 준비중 · 호출 중 · 수락 뒤 | `edit && !doing && !done` · 켜짐 = `!busy && t.canStart`(서버 값). 준비중 `canStart=true` 를 앱이 막지 않는다. 호출 중은 서버가 false 를 줘서 꺼진다 | PASS |
| 진행중 = [종료][⋮] · 완료 = [⋮] | `canFinish` · `canUndoStart` · `canUndoFinish` · board edit 그대로 · ⋮ 는 기존 `_more` → `confirmUndo` → API | PASS |
| 행 [수락] · 상태 Pill · 호출 대상 · 호출 경과 글자 제거 | 이 위젯들을 만드는 코드가 없어짐(`PillBadge` · `acceptCall` · `callTargetLabel` · `shortElapsed` 호출 0) | PASS |
| 보기만 직무 | `edit=false` 면 조작 0 · 새 동작 없음 | PASS |
| 그 행 값만 · 새 타이머 0 · spanMin 변경 0 | `t.*` 만 사용 · 기존 `Ticking` 의 `now` 사용 · `format.dart` diff 0 | PASS |
| 행을 누르면 차트 | `GestureDetector onTap: showChart` 유지 | PASS |
| 회색 톤 · 진행중 강조 | done = gray500 · doing = primary100 배경 + primary 테두리 | PASS |

새 테스트 `detail_polish_test.dart` 10건이 다루는 것: 전부 수락 숨김, 부분 / 복수 호출, 행 [수락] 없음, 회색 [시작] 요청 0, 준비중 canStart true → POST start, 조작이 2줄째, 진행 · 완료 글자, 보기만 직무 조작 0, 머리 중심 = 머리 중심(폰 · 320 · iPad), 뒤로 버튼과 겹침 0. 디자인 복제 단언은 없다.

## 시각 — 직접 연 PNG (`detail-polish-evidence/screens/`)

fixture 렌더는 실데이터가 아니다.

| PNG | 확인 |
|---|---|
| `phone-detail-5states` · `-scrolled` | 「F-룸1」이 화면 가운데(x≈390/780). 진행중: 큰 05:24 + 「KOS-DEMO · 13:54 시작」 + [종료][⋮]. 준비중 KOS-DEMO: **켜진 [시작]**(server true). 호출 중 리쥬란: 담당의 미정 + 회색 [시작]. 수락 뒤 포텐자 김원장: 켜진 [시작]. 완료: 회색 「완료 11분」 + ⋮. 배지 · 행 [수락] 없음. 상단 상자는 미수락 호출만. 4탭 · 통역 바 유지 |
| `ipad-detail-5states` | 같은 5상태 · 2열(마취 / 호출 상자 + 시술). 「F-룸1」은 레일을 뺀 머리 폭의 가운데(머리가 레일 오른쪽에 있음) |
| `phone-detail-partial-accept` | 상자 남음 · 「원장 골라 수락 · 1건」 · 김원장 줄 켜진 [시작] · 담당의 미정 줄 회색 [시작] |
| `phone-detail-all-accepted` | 호출 상자 없음 · 두 줄 모두 김원장 + [시작] |
| `phone320-detail-long-rows` · `-scrolled` · `-done` | 머리 「A-레이저 시술…」 가운데 말줄임 · 뒤로와 겹침 0. 75:03 이 2줄 제목 옆에 남음. 긴 담당의 「아주 긴 이름의 담당 원장 KOS-DEMO-…」 말줄임 + [시작] 잘림 0. 완료 「완료 11분」 + ⋮ 잘림 0 |
| `simulator-after-reinstall`(**실제 시뮬레이터 · 사용자 기존 세션 · 로컬 실데이터**) | 목록 화면. 개정 ③ 2줄 상태 박스 회귀 0(「시술 중 · 26:20 / 마취용 / 울쎄라피… 외 1개」 · 「113:04」 누적). 상세 화면은 열려 있지 않다 |

열지 않은 것: `short599-*` · `short600-*` · `ipad-*-scrolled` · `ipad-detail-partial/all` · `simulator-before-reinstall`.

## FAIL · WARN

없음.

## 참고 (결함 아님)

- 같은 줄의 상태가 호출 중이든 수락 뒤든 행 모양은 같고, [시작]이 켜졌는지만 다르다(브리프 의도). 호출 대상 · 경과는 상단 상자에서만 보인다.
- 부분 수락 상자의 부제 「시술 2건」은 그 호출의 전체 줄 수이고, 버튼 「· 1건」은 미수락 줄 수다. 기존 U-4 정의 그대로이며 이번 변경 밖이다.
- 320 높이(568)에서는 통역 바가 화면 아래를 크게 차지해 시술 목록이 짧게 보인다. 개정 ④ 전부터 있던 배치다.

## 직원이 실물에서 만날 자리

- 호출이 전부 수락되면 상세의 큰 호출 상자가 사라진다. 담당의는 시술 줄에서 보인다.
- 호출 중 시술의 [시작]은 회색이다. 수락은 상단 상자 · 목록 카드 · 호출 탭에서만 한다.
- 진행 시간이 60분을 넘으면 「75:03」처럼 분이 쌓인다.

## 미검증

- 로그인 입력 · 실제 업무 쓰기 · 실데이터 상세 5상태는 아무도 보지 않았다. 시뮬레이터는 사용자의 기존 세션으로 목록 조회까지만 보인다. 실 backend 가 준비중 줄에 canStart true 를 주는 실제 사례는 코드(`start_block`)로만 확인했다.
- 표준 main · 로컬 dart-define 으로 빌드했다는 것은 mobile 보고서 서술로만 확인했다(로그에 인자가 남아 있지 않음).
