# day-app mobile — 목록 상태 박스 2줄 · 초 단위 시간 (task_c8833050658d · ctx_8915491d7e90)

## 상태: done — 구현 · 테스트 · 캡처 · 빌드 · 시뮬레이터 재설치 완료

- 기준: SPEC-003 `d6d961e9402dc4dbae69aa1c407b5a37f5571882`(개정 ③ — 카드 상태 박스 2줄). 사용자 「응 일단 이거 부터 바꾸고 오자」.
- 코드: `day-app` 기존 미커밋 UI 위에 좁게 고침. `app/` 만 · 커밋 · push · merge 0 · 하위 위임 0. 서버 · 포트 · DB · env · 네이티브 · 서명 · 다른 기기 0.
- 보존: `status-box-evidence/before-board_screen.dart.txt` · `before-format.dart.txt`(기존) 그대로. manifest는 상위 work/day-app/status-box-before-manifest.json에 보존되어 있다(코디 기록 정정; 독립 리뷰에서 해시 대조 완료).

## 변경 (app/)

| 파일 | 변경 |
|---|---|
| `lib/ui/board_screen.dart` | `RoomCard._nowBox` 4상태를 2줄로 · 옛 한 줄 `_line` 제거 · 새 `_twoLines`(1줄 = 상태 · 시간 / 담당의 · 2줄 = 「첫 시술명」 + 「 외 N개」). 호출 `_callBox` · `_callLine` · 수락 · 귀가 · 카드 밖 줄 · 상세 · 룸 머리 무변경 |
| `lib/ui/format.dart` | `elapsedMmss`(초 단위 mm:ss · 분 누적 75:03) · `StatusSummary` · `doingSummary`(서버 순서 첫 doing 대표 + 나머지 doing 수) · `openSummary`(완료 아닌 줄 첫 값 + 나머지 수) |
| `test/ui/status_box_test.dart`(신규) | 불변식: mm:ss · 75:03 누적 · 음수 0 · lastSeconds 1259 → 20 · doing 대표 집계(대기 · 완료 안 셈) · open 집계 · 하나면 외 N개 없음 · 빈 목록 2줄 높이 · 1초 뒤 글자 바뀜 · 320 긴 담당의/시술명에서 상태 칸 폭 유지 · 「외 2개」 박스 안 · 상태 글자가 제 폭을 줄이지 않음 · 진행 줄 담당의 빈 글자 = 미정. (테스트 기본 글꼴은 글자마다 글자 크기만큼 넓어 긴 한글 전체 폭 검사는 실글꼴 캡처로 확인) |
| `test/ui/app_flow_test.dart` | 마취 테스트 1건만 새 글자로(「마취 중 · 19:0x」 · 「기준」 없음 · 「시술 대기 · 마취 완료 2분」) |
| `test/capture/visual_capture_test.dart` | fixture 시간을 예시값으로(마취 중 12:34 · 마취 완료 1234초 = 20분 · 시술 중 05:24 + doing 2줄) · 4상태 장면 · 320/599/600 긴 상태 장면 |

## 구현 대조 (개정 ③)

| 항목 | 구현 |
|---|---|
| 시술 대기 | 「시술 대기」 / 첫 담당의 또는 「담당의 미정」 · 2줄 = 완료 아닌 줄 첫 제목 외 N개 |
| 마취 중 | 「마취 중 · mm:ss」(지금 − runningSince) · 연보라 · `long` 이면 빨강(서버) · 시작 시각 · 기준 분은 목록 박스에서 안 그림 |
| 마취 완료 대기 | 「시술 대기 · 마취 완료 {lastSeconds÷60 내림}분」 |
| 시술 중 | 대표 = 서버 순서 첫 `doing` 줄 → 「시술 중 · mm:ss」(그 줄 startedAt) / 그 줄 담당의(null · 빈 글자 = 「담당의 미정」 — 코디 지적 반영) / 그 줄 제목 + 나머지 doing 「외 N개」 · DAY 주색 |
| 시간 | 초 단위 · 분 누적 · 기존 `Ticking`(1초 · 서버 시각 보정) 그대로 — 새 timer 0 |
| 폭 | 1줄 = 상태 · 시간이 제 폭을 먼저 가짐(최대 85%) · 담당의는 남는 폭에서 오른쪽 정렬 · 말줄임(코디 지적: 3:2 상한이면 「마취 완료 20분」 이 잘릴 수 있음 → 고침) · 2줄 제목 Flexible 말줄임 + 「 외 N개」 고정 · 화살표 · 펼침 없음 |
| 빈 시술 목록 | 2줄 비움(글자 안 지음) · 높이 2줄 유지 |
| 우선순위 | 호출 대기 있으면 호출 박스(기존 OQ-A21) · 마취 진행 > 시술 중 > 대기(기존 순서) |

## 검증 (`status-box-evidence/logs/`)

| 명령(cd app · FVM 3.44.8) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **190 passed · 27 skipped(캡처 전용) · 0 failed**(+6 새 상태 박스 테스트) · fix1 회귀(320 호출 버튼 · 시트 고객 · 호출 카운트) 포함 통과 |
| `DAY_CAPTURE_DIR=…/screens fvm flutter test test/capture/visual_capture_test.dart` | 27 passed → PNG 71장(+ 시뮬레이터 2장) |
| `fvm flutter build ios --no-codesign` | ✓ 17.5MB · ATS 키 0 |
| `fvm flutter build ios --simulator --debug`(표준 `lib/main.dart` · 브리프 4개 `--dart-define`) | ✓ Built |

## 스크린샷 (`status-box-evidence/screens/`)

- **fixture 렌더(실데이터 아님)**: `phone-status-4states` · `ipad-status-4states`(시술 대기 / 마취 중 · 12:34 / 시술 대기 · 마취 완료 20분 / 시술 중 · 05:24 / 마취 중 long 빨강 30:00 / 마취 중 75:03 누적) · `phone320-status-long`(「시술 대기 · 마취 완료 20분」 전체 + 긴 담당의 말줄임) · `short599-status-long` · `short600-status-long`(긴 담당의 「아주 긴 이름의 …」 · 긴 시술명 「…  외 2개」) · 그 밖 기존 장면 재캡처. 실제 DayApp 위젯 · macOS 실글꼴. 시각은 fixture `now` + 실행 지연이라 ±1초 날 수 있다.
- **실 시뮬레이터**: `simulator-before-reinstall.png` · `simulator-after-reinstall.png`.

## 시뮬레이터

- 기존 `orca-mobile-iphone` 5C9E05C7-7171-455E-97CE-2AD2EA097F88 에 `simctl install` 로 덮어 설치(uninstall · erase · 로그아웃 · 토큰 삭제 0) → 실행 — 최종 수정 뒤 다시 덮어 설치 · **최종 PID 6458**.
- 사용자가 이미 로그인해 둔 세션이 그대로 복원되어 **로컬 day-local 현황 화면**이 떠 있다(나는 로그인 · 자격증명 · 업무 조작을 하지 않았다). 화면에서 새 2줄 박스 확인: 예) A-룸3 「시술 중 · 74:13」 / 담당 원장 / 얼굴필러 셀레스텔라 1cc — 분 누적 표시가 실데이터에서도 보임.
- **실데이터 관찰(수정 안 함 · 한계)**: 첫 카드 A-룸1 은 「시술 중」 · 시간 없음 · 「담당의 미정」 · 2줄 빈칸. 코드 근거(읽기 전용 · 옆 backend `a1c90b9d`): 카드 `state` 는 방문 흐름 단계에서 온다(`board_rules.py:27-31` `VISIT_STATES` · `:80-81` `visit_state` — `FlowStep.PROCEDURE → doing`), 줄 상태는 줄마다 따로 정한다(`:102-110` `task_state` — `started_at` 이 있어야 `doing`). 그래서 방문은 시술 단계(doing)인데 시작 시각이 있는 줄이 하나도 없는 조합이 서버에서 나올 수 있다. 앱은 개정 ③ 대로 대표 `doing` 줄이 없으면 시간 · 담당의 · 시술명을 다른 줄로 채우지 않는다(빈 2줄 높이 유지). 새 대체 규칙 · 서버 수정은 하지 않았다 — 그 화면의 실제 줄 값은 자격증명 · API 조회 없이 확인하지 않았다(추정). 표시를 바꿀지는 사용자 · 코디 판단.

## 남은 것

- 룸 머리 방 이름 가운데 정렬 · 상세 마취 칸 글자(OQ-A31)는 이번 범위 밖 — 손대지 않음.
- 개정 ③ 은 목록 박스만. 호출 박스 · 상세는 그대로.
