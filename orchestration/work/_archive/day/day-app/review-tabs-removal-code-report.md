# 리뷰 리포트 — day-app 시술현황 상단 3탭 제거(SPEC-003 개정 ⑤) / code + 시각 (2026-11-10)

- 대상: `CENTURION_DAY/day-app` HEAD `4ee33f95` 위 미커밋 변경.
- 기준: spec tree HEAD = `06239a1c7d45e95a02e5aab61b9d29bea6b7aca3`(개정 ⑤ — 직접 확인).
- 원천: `tabs-removal-code-brief.md` · `tabs-removal-code-report.md` · `review-tabs-removal-spec2-report.md`.
- 방식: read-only. 코드 · spec · 서버 · 시뮬레이터 조작 0, 하위 위임 0. 로그는 `review-tabs-removal-logs/`.

## 판정: **PASS (참고 2)**

FAIL 과 WARN 은 없다. 스펙 개정 ⑤(:43 · :81)의 「시술현황 = 연결 줄 + 칩 4개 + `cards[]` 카드만」이 코드와 PNG 에서 모두 지켜졌다. 이 범위 밖의 회귀도 보이지 않는다.

## 변경 범위 (`git diff 4ee33f95`)

- 바뀐 파일은 `app/lib/ui/board_screen.dart`(−208) · `app/test/ui/app_flow_test.dart` · `app/test/capture/visual_capture_test.dart` **3개뿐**이다.
- `lib/model` · `lib/state` · `lib/data` · `room_screen` · `accept` · `shell` · 서버 · native diff 는 0이다.

`board_screen.dart` 에서 지운 것:
- `_tab` 상태와 탭 UI(`_tabs`, `tab-0..2`).
- `IndexedStack`. 이제 본문은 `_nowTab(snap)` 하나다.
- 호출 탭(`_callsTab` · `_callCard` · `call-accept-*`).
- 시술 완료 탭(`_doneTab` · `_doneCard` · 검색 · `chart_sheet` import).

옮겨 붙인 곳이 없다. 숨은 라우트 · 새 메뉴 · 새 정렬도 없고, `doneTab` 을 카드 목록에 합치지도 않았다(`grep`: `lib/` 안에서 `doneTab` 을 쓰는 곳은 `board_controller.dart:126` 의 KOS 실패 토스트 이름 찾기뿐 — 기존 기능).

## 보존 확인 (코드)

| 항목 | 근거 | 판정 |
|---|---|---|
| 칩 4개 · 서버 `inbox.section` 으로 거르기 · 서버 순서 | `_nowTab` · `_chipSection` 무변경 | PASS |
| 폰 1열 / iPad 격자 · 빈 판 | `_nowTab` 무변경 · 빈 판 `board-empty`(:162) · 거른 결과 0장 「조건에 맞는 고객이 없어요」(:164) | PASS |
| 카드 2줄 상태 박스 · 카드에서 바로 수락 | `RoomCard` · `card-accept-*` 무변경 | PASS |
| 상세 수락 · 개정 ④ | `room_screen.dart` diff 0 | PASS |
| 푸시로 진입 | `_openRequested` · `openRoom` 유지 | PASS |
| 세션 race · `alive` | `PresenceAware` · `_alive` 유지(`acceptCall` 에 넘김) | PASS |
| API · 모델 수신 | `BoardSnapshot.calls` · `doneTab` 파싱 유지(`board.dart:292-315`) · 귀가 처리 무변경 | PASS |
| 하단 4메뉴 · DAY 머리 · 종 | `shell.dart` diff 0 | PASS |

**테스트 정정은 지운 UI 몫뿐이다.**
- `app_flow_test`: 「탭 있음」 단언을 「`tab-0..2` · `calls-tab` · `done-tab` · 「현황」 · 「호출 」 · 「시술 완료 」 없음 + 칩 4개 + `card-v1`」로 바꿨다.
- 보기만 직무 테스트: 호출 탭 확인 대신 「카드에 호출 상태 보임 · 카드 [수락] 없음」을 확인하고, 상세 수락 · 호출 없음 단언은 그대로 둔다.
- 수락 직무 분기 그룹: `card` · `room` 두 진입점은 그대로 남고 `calls` 만 빠졌다(원장 즉시 · 간호사 드로어 · 정확 body 검증 유지).
- `session_race_test` · `actions_test` · `detail_polish_test` · `status_box_test` 는 바뀌지 않았다.

## 실행 — 내가 직접 돌린 것 / 로그만 확인한 것

| 구분 | 명령 | 결과 |
|---|---|---|
| 직접 | `fvm flutter analyze` | No issues · exit 0 |
| 직접 | `fvm flutter test test/ui/{app_flow,actions,session_race,detail_polish,status_box}_test.dart`(좁은 관문 1회) | **+70 · 0 fail** · exit 0 |
| 로그 | mobile 전체 test | 198 pass · 27 skip(15:40:44) |
| 로그 | analyze · capture · unsigned build · sim build | 15:41:05 · 15:40:20 · ✓ 17.4MB(15:41:42) · ✓(15:42:09) |
| 로그 | sim 실행 인자(`simulator-build-args.txt`) | 표준 build · `--dart-define` DAY_LOGIN_ENTRY / DAY_DEV_LOCAL_ORIGIN = 로컬 · REQUIRE_ENVIRONMENT=false · APNS sandbox |
| 로그 | sim PID | 45830 |

시각 순서: 마지막 소스 · 테스트 수정(board_screen 15:39:01 · capture 15:39:54 · app_flow 15:40:35) **뒤에** 전체 test(15:40:44) · analyze · build 로그가 찍혔다. capture(15:40:20)는 app_flow 정정보다 앞이지만, app_flow 는 캡처 대상이 아니라 PNG 에는 영향이 없다.

## 시각 — 직접 연 PNG (`tabs-removal-evidence/screens/`)

fixture 렌더는 실데이터가 아니다. 실제 시뮬레이터 화면은 따로 적었다.

| PNG | 확인 |
|---|---|
| `phone-board-list` | 머리 DAY / 시술현황 / 종 → **바로 칩 4개**(전체 6 · 확인 필요 1 · 시작 가능 0 · 시술 대기…) → 카드. 「현황 / 호출 / 시술 완료」 탭 줄 없음. 2줄 상태 박스 · 하단 4메뉴 유지 |
| `ipad-call-wait-list-nurse` | 레일 4메뉴 · 머리 아래 바로 칩 · 격자 2열 · 카드 호출 줄 「원장 골라 수락 · 2건」 유지(수락 가능 카드) |
| `phone320-long-list` | 320 · 탭 줄 없음 · 칩 아래 바로 카드 · 긴 방 · 이름 말줄임 · 카드 수락 버튼 안 잘림 |
| `simulator-after-reinstall`(**실제 시뮬레이터 · 사용자 기존 세션 · 로컬 실데이터**) | 상단 탭 없음 · 칩(전체 12 · 확인 필요 9 · 시작 가능 0 …) 아래 바로 카드 · 2줄 박스(「시술 중 · 147:13」 누적 · 「마취 중 · 55:01」 빨강) · 4메뉴 |

빈 판 · 보기만 직무 · 상세 개정 ④ 장면은 이번 증거 목록에 따로 없다. 빈 판과 보기만 직무는 위 코드 · 테스트로 확인했다. 개정 ④ 상세는 `room_screen` diff 0 이고 직전 검수(`review-detail-polish-code-report.md`)에서 PNG 를 봤다.

## FAIL · WARN

없음.

## 참고 (결함 아님)

1. **테스트 제목에 옛 글이 남음**: `app_flow_test.dart:285` 의 테스트 이름이 아직 「보기만 직무(코디) — 판 · 호출 · 시술 완료는 보이고 …」다. 본문 단언은 개정 ⑤ 에 맞게 고쳐졌다. 다음에 손댈 때 제목만 고치면 된다.
2. 모델의 `waitingCallCount` · `homeCount` getter 는 이제 화면에서 쓰지 않는다. 남아 있어도 해가 없고, 모델 · 수신 계약을 보존하라는 스펙 :43 과도 맞는다.

## 직원이 실물에서 만날 자리

- 시술현황에서 호출 목록과 오늘 귀가 / 완료 고객 목록 · 검색이 사라진다. 귀가 대기로 넘긴 방문은 카드에서 빠지고 앱 안에서는 다시 찾아볼 곳이 없다(사용자 결정 「카드만」).
- 수락은 목록 카드 호출 줄 · 룸 상세 상단 상자 · 원장 푸시에서만 한다.

## 남은 의존

- 실제 로그인 입력 · 업무 쓰기는 아무도 하지 않았다. 시뮬레이터는 사용자 기존 세션의 목록 조회까지만 보인다.
- D-2 · D-3 · D-5 · D-6 서버 의존과 상세 마취 칸 글자(OQ-A31 남은 부분)는 그대로 남아 있다.
