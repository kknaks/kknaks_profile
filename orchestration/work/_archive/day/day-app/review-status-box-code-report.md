# 리뷰 리포트 — day-app 목록 상태 박스 2줄 · 초 단위 시간 / code + 시각 (2026-11-10)

- 대상: `CENTURION_DAY/day-app` `app/` 미커밋 트리. 상태 박스 후속(mobile task_c8833050658d)과, 이전 `review-mobile-ui-report.md` WARN 4건 후속(mobile-ui-fix1)을 함께 본다.
- 원천: SPEC-003 `d6d961e9`(개정 ③ — spec worktree HEAD 확인) · `status-box-code-brief.md` · `status-box-code-report.md` · `status-box-before-manifest.json` · `status-box-evidence/before-*.dart.txt`.
- 방식: read-only. app · spec · 서버 · 시뮬레이터 조작 0, 하위 위임 0. 검증 로그는 `review-status-box-logs/`.

## 판정: **PASS (WARN 2 · 참고 2)**

개정 ③ 의 목록 `_nowBox` 4상태 2줄은 스펙 U-3 4번(:205-213) · A-28 · A-29 와 같다. 범위 밖 코드는 바뀌지 않았다. 이전 WARN 4건은 모두 고쳐졌다. FAIL 은 없다.

## 변경 범위 — manifest 대조 (직접 sha256 계산)

`status-box-before-manifest.json`(14:13) 39개 파일을 지금 파일과 비교했다.

- **바뀐 것 4개뿐**: `lib/ui/board_screen.dart` · `lib/ui/format.dart` · `test/ui/app_flow_test.dart` · `test/capture/visual_capture_test.dart`.
- **새 파일**: `test/ui/status_box_test.dart`(manifest 밖 · 14:27).
- **manifest 에 없는 수정 파일**: `README.md` · `pubspec.*`. 수정 시각이 13:26–13:42 로 manifest 보다 앞이라 이번 회차 변경이 아니다.
- `room_screen` · `doctor_picker` · `accept` · `shell` · `model` · `state` · `data` · `core` 의 해시는 같다. 호출 박스 · 수락 · 귀가 · 상세 · 룸 머리 · API · 세션은 바뀌지 않았다. 룸 머리 가운데 정렬도 손대지 않았다(OQ-A31 기록만).
- `before-format.dart.txt` → 지금: `elapsedMmss` · `StatusSummary` · `doingSummary` · `openSummary` 추가만.
- `before-board_screen.dart.txt` → 지금: `_line` 을 `_twoLines` 로 바꾸고 `_nowBox` 본문만 바뀌었다(diff 539-608 한 덩어리). `_callBox` 우선(`:524`)은 그대로다.

## 실행 — 내가 직접 돌린 것 / 보고만 본 것

| 구분 | 명령 | 결과 |
|---|---|---|
| 직접 | `fvm flutter analyze` | No issues · exit 0 |
| 직접 | `fvm flutter test test/ui/status_box_test.dart test/ui/app_flow_test.dart test/ui/actions_test.dart`(좁은 관문) | **+55 · 0 fail** · exit 0 |
| 직접 | `fvm flutter test test/capture/visual_capture_test.dart`(캡처 환경값 없이 = 컴파일 확인) | ~27 skip · exit 0 |
| 직접 | sha256 manifest 대조 · `grep http:// lib` · ATS 키 grep | 위 범위 · 하드코딩 0 · ATS 예외 0 |
| 보고만 | mobile 전체 `flutter test` | 190 pass · 27 skip(log 14:27:47) |
| 보고만 | unsigned build · simulator build · PID | ✓ 17.5MB · ✓ · PID 6458 |

전체 테스트를 다시 돌리지 않은 것은 브리프가 반복하지 말라고 했기 때문이다. 대신 로그 시각을 대조했다. 전체 테스트 로그(14:27:47)는 `board_screen`(14:26:35) · `format`(14:21:51) · `status_box_test`(14:27:33) 수정 뒤에 찍혔다. `visual_capture_test.dart` 만 14:27:54 로 그보다 7초 늦다(WARN-2 — 실영향 없음).

## 코드 대조 (개정 ③)

| 규칙 | 코드 | 판정 |
|---|---|---|
| 4상태만 2줄 · 호출 대기가 있으면 호출 박스 우선 | `board_screen.dart:524` 그대로 · `_nowBox` 만 변경 | PASS |
| 1줄 = 상태 · 시간(왼쪽) / 담당의(오른쪽) · 2줄 = 시술명 + 「 외 N개」 · 1개면 생략 · 화살표 없음 | `_twoLines` 539-573: `count = more>0 ? ' 외 N개' : ''` | PASS |
| 경과 mm:ss 초 단위 · 분 누적(75:03) · 음수는 0 | `format.dart` `elapsedMmss`: `inSeconds.clamp` · `~/60` 을 패딩, 시간 단위 변환 없음 | PASS |
| 마취 완료 = lastSeconds÷60 내림 | `lastAnesMinutes` = `~/ 60`(1259 → 20) · 글자 「시술 대기 · 마취 완료 N분」 | PASS |
| 시술 중 = 서버 순서 첫 doing 행 하나가 시간 · 담당의 · 제목을 같이 냄 · 나머지 doing 만 셈 | `doingSummary`: doing 만 모음 · `rows.first` · `length-1`. `_nowBox` 시간 · 담당의 · 제목 모두 `s.row` 에서 옴 | PASS |
| 대기 · 마취의 2줄 = done 이 아닌 줄 첫 값 + 나머지 수 · 담당의 = done 아닌 줄 첫 담당의 | `openSummary` · `cardDoctor`(done 제외) — 스펙 :211 그대로 | PASS |
| 빈 값 | 행이 없으면 제목 '' · 시간 ''(「시술 중」만) · 담당의 「담당의 미정」 · 2줄 높이는 빈 Text 로 유지 | PASS — 아래 참고 1 |
| doing 행 담당의가 빈 글자일 때 | `(doctorName ?? '').isEmpty ? '담당의 미정'` — msg_8ed594d80c62 반영 | PASS |
| 320 폭 · 「마취 완료 20분」 안 잘림 | 상태 글자가 먼저 폭을 가짐(최대 85%) · 담당의는 Expanded 로 말줄임 — msg_32e7595777ed 반영 | PASS |
| 「외 N개」 유지 | 제목은 Flexible 로 말줄임 · count 는 고정 Text | PASS |
| 1초 갱신 · 새 타이머 없음 | 기존 `Ticking` 의 `now` 사용 · 새 Timer 0 | PASS |
| 색 · 서버 판정 | 마취 = 연보라 · `a.long` 일 때만 빨강 · 시술 중 = primary · 우선순위 = 마취 진행 > 시술 중 > 대기(`state=='doing' && runningSince==null`) — 이전과 같음 | PASS |
| 목록 박스에서 시작 시각 · 기준 분 제거 | `limits.anesMin` · `hm()` 사용 줄 삭제 | PASS |
| 서버에 새 fallback 정책 추가 | 없음(서버 · API 파일 diff 0, 다른 행으로 메우지 않음) | PASS |

새 테스트 6건(`status_box_test.dart`)은 mm:ss · 누적 · 0 처리 · 대표 행 집계 · open 집계 · 2줄 높이 · 1초 갱신 · 320 폭 · 빈 담당의를 확인한다. 디자인을 그대로 베낀 단언은 없다.

## 시각 — 직접 연 PNG (`status-box-evidence/screens/`)

fixture PNG 는 실데이터가 아니다. 실제 시뮬레이터 화면은 따로 적었다.

| PNG | 확인 |
|---|---|
| `phone-status-4states` | 4행 카드 유지 · 시술 대기 / 담당의 미정 / 「울쎄라피… 외 1개」 · 마취 중 · 12:34(연보라) · 「시술 대기 · 마취 완료 20분」 / 이원장 / 써마지(1개라 외 N개 없음) · 시술 중 · 05:24 / 김원장(DAY blue) · 4탭 |
| `ipad-status-4states` | 위 4상태 + 마취 long 빨강 30:00(카드 빨강 테두리) + **75:03 누적** · 긴 이름 「스킨보톡스 … (2회차) 외 1개」 · 레일 4메뉴 |
| `phone320-status-long` | 「시술 대기 · 마취 완료 20분」 전체가 보이고 긴 담당의는 「아주 긴 이름의 …」로 말줄임 · 「시술 중 · 05:24」 + 「…FLX … 외 2개」 보존 · 겹침 0 |
| `phone-call-wait-list-nurse` | 이전 WARN-1 해소: **「호출 1」**(calls[] 정합) |
| `phone-doctor-call-sheet-empty` | 이전 WARN-2 해소: 머리 「A-룸1 · TEST CLAUDE」 · 4탭 보임 |
| `phone-calls-tab` · `phone-done-tab` | 이전 WARN-4 해소: 호출 탭(수락 대기 1 / 수락함 2 · 「원장 골라 수락 · 2건」) · 시술 완료 탭(검색 · 귀가 대기 / 귀가 배지) |
| `phone-startable-room` | 이전 WARN-4 해소: 켜진 [시작] = DAY blue 테두리(수락 줄) · 꺼진 [시작] = 회색 |
| `phone320-long-list` | 이전 WARN-3 해소: 320 긴 방 · 이름 · 시술명 말줄임 · 「원장 골라 수락 · 1건」 안 잘림 |
| `simulator-after-reinstall`(**실제 시뮬레이터 · 사용자 기존 세션 · 로컬 실데이터**) | 「시술 중 · 74:13」 / 구지윤 / 얼굴필러 셀레스텔라 1cc — 실데이터에서도 분이 누적된다. A-룸1 = 「시술 중」 · 「담당의 미정」 · 2줄 빈칸(참고 1) |

열지 않은 것: `short599-*` · `short600-*`(테스트 + 320 장면으로 대신함) · `ipad-*` 나머지 · `simulator-before-reinstall`.

## FAIL

없음.

## WARN

1. **보고서의 manifest 서술이 틀림**: `status-box-code-report.md` 「보존」 줄에 「manifest 파일은 폴더에 없었다」라고 썼다. 실제로는 `work/day-app/status-box-before-manifest.json`(14:13)이 있고 지워지지도 바뀌지도 않았다. 기록 정정만 하면 된다. 코드에는 영향이 없다.
2. **전체 테스트 로그보다 늦게 고친 파일 1개**: `test/capture/visual_capture_test.dart` 의 수정 시각(14:27:54)이 전체 test 로그(14:27:47)보다 7초 늦다. 이 파일은 평소 skip 되는 캡처 전용이다. 뒤이은 캡처 실행(14:28:07, 27 pass)과 내가 한 컴파일 실행(exit 0)이 이 판을 덮으므로 실영향은 없다.

## 참고

1. **실데이터 A-룸1 「시술 중」인데 시간 · 시술명이 비어 있음**: 카드 `state` 는 방문 흐름 단계에서 오고, 줄 상태(task_state)는 `startedAt` 이 있어야 doing 이 된다. 둘은 별개라서 서버가 이 조합을 낼 수 있다(mobile 이 인용한 backend `board_rules.py` 근거 — 나는 그 파일을 다시 열지 않았다). 앱은 스펙 :209 · :212 대로 다른 행으로 메우지 않고, 담당의만 「담당의 미정」으로 둔다. 스펙대로다. 다만 직원에게는 「시술 중인데 아무 정보 없음」으로 보인다. 표시를 바꿀지는 사용자 · 코디가 정한다(새 정책은 이번 범위 밖).
2. 호출 상태 박스는 개정 ③ 범위 밖이라 옛 모양(대상 · 수락 대기 / 시술들 · 오른쪽 큰 분)을 유지한다. 상태 박스(2줄 · mm:ss)와 호출 박스(분)가 한 목록에 섞여 보인다 — 스펙 :213 대로이고 결함 아님.

## 직원이 실물에서 만날 자리

- 실데이터 「시술 중」 카드 중 시작 시각이 있는 줄이 없으면 박스가 「시술 중 / 담당의 미정 / 빈 줄」로 보인다(참고 1).
- 오래 걸리는 시술은 「74:13」처럼 분이 60 을 넘어 쌓인다(사용자 확정 형식).
- 같은 목록에서 호출 박스만 분 단위다(참고 2).

## 미검증 · 남은 의존

- **로그인 입력 · 인증 통합 · 업무 쓰기는 이번에도 아무도 하지 않았다.** 시뮬레이터는 사용자가 이미 로그인해 둔 세션이 복원되어 로컬 판 조회까지만 보인다(PID 6458 · mobile 보고 + PNG). 조작 성공 토스트 · 수락 · 호출의 실서버 동작은 미확인이다.
- probe 200 · health 는 인증 통합 증거가 아니다. ATS 예외 0 · 소스 http 0 은 직접 확인했다. 시뮬레이터에서 로컬 http 조회가 된 것은 화면으로만 봤다.
- D-2 · D-3 · D-5 · D-6 서버 의존, OQ-A31(룸 머리 정렬 · 상세 마취 글자)은 그대로 남아 있다.
