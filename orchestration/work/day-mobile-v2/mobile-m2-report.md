# day-mobile-v2 M2 결과 보고 — 기기 선택(U-17) · 바로 시작(U-18) · 호출 취소(U-19) · 원장 바꾸기(U-22) + M1 정리

## 상태: done (커밋 · push · PR 없음 · 실기기 · dev 서버 확인 pending)

base = `e96b0718`(서버 P2) 위. `backend/` 읽기만 — 워크트리의 `backend/**` 변경(알림 · migration 0012 등)은 backend 워커 P3 몫, 내 것 아님.

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `app/lib/state/session_controller.dart` | `Phase.choosingDevice` · `DeviceChoice` · `devices` · 응답 갈래 공통 `_answer`(choose_hospital · choose_device · signed_in) · `chooseDevice()`(유지 대상으로만 · 응답 대상 · 환경 확인 = 병원 고르기와 같음) · 임시 토큰 오류 공통 `_pendingFailed`(session_expired = 입력 화면 + 그 문구) |
| `app/lib/data/day_api.dart` | `chooseDevice` → `POST /api/auth/device {pending_token, device_id, client:"app"}` |
| `app/lib/ui/login_screen.dart` · `app/lib/app.dart` | 기기 선택 단계(로그인 카드 자리 · 병원 고르기와 같은 틀) · 라디오 줄 · 처음 선택 = 첫 줄 · [계속하기] · 뒤로 = 입력 화면(PopScope) |
| `app/lib/model/board.dart` | `Task.canCancelCall` · `canQuickStart` · `canChangeDoctor`(관대한 읽기) |
| `app/lib/state/board_controller.dart` | `quickStart`(200 `rejected[]` 코드마다 실패 토스트) · `cancelCall` · `changeDoctor` · 실패 글자 = 웹 `message_of` 규칙 하나(`boardActionMessage`) · 앱이 만든 코드(network · timeout · unexpected)는 코드 그대로(OQ-A7) |
| `app/lib/ui/doctor_picker.dart` · `accept.dart` | `PickMode.quickStart`(시술만 · 원장 고르기 없음 · 한 칸) · `PickMode.doctor`(「모든 의사」 없음) · 제출 대상 nullable |
| `app/lib/ui/room_screen.dart` | [의사 호출] 옆 [바로 시작] · 호출 줄 ⋮ 「호출 취소」 · 담당의 자리 누름 → 원장 변경 |
| `app/lib/core/copy.dart` | 기기 선택 글자 · `deviceAgo` · `cancelCallLabel` · `task_not_assignable` 글자 · `boardActionMessage`(M1 `roomActionMessage` 를 넓혀 판 조작 전부로) |
| `app/lib/ui/room_move.dart` | 주석만 |
| 테스트 새: `test/state/device_choice_test.dart`(6) · `test/ui/m2_actions_test.dart`(13) · `test/core/board_messages_contract_test.dart`(2) · `test/capture/m2_capture_test.dart`(캡처 · 평소 skip) · 고침: `test/ui/room_move_test.dart`(W-3) |

## 동작 · 판단한 배치(시안 없음 — 사용자 결정 + 웹 배치)

- **기기 선택(U-17)**: 로그인 카드 안 — 머리 「이미 로그인 중인 기기가 있습니다」 → 설명 두 줄 → 기기 줄(라디오 + 「{label} · {ip}」 + 「n분 전」/「방금 전」 · 시각 없으면 안 그림) → [계속하기]. 「처음으로」 없음(웹 OQ-K10) · 비밀번호 다시 안 물음 · **뒤로 가기 = 입력 화면(임시 토큰 버림 — OQ-A53 기본값)**. 응답 갈래 = signed_in(→ /me → 저장) · choose_hospital(→ 병원 고르기) · choose_device(새 목록 · 새 토큰 · 처음 선택 다시 첫 줄). 응답 대상 · 환경이 유지 대상과 다르면 `environment_unavailable`(다른 주소로 안 옮김). 빈 목록 · id 없는 줄만 = `unexpected_response`.
- **바로 시작(U-18)**: 룸 상세 시술 상자 아래 [의사 호출] · [바로 시작] 두 버튼 한 줄(웹 액션바 순서) → 의사 호출과 같은 드로어(폰 바텀 시트 · 아이패드 팝오버) · 시술 체크 · [전체 선택] 그대로 · 체크 가능 = 서버 `canQuickStart` · 원장 고르기 없음 → [바로 시작 · N건](0건 꺼짐). [바로 시작] 버튼은 `canQuickStart` 줄이 하나도 없으면 꺼짐(웹 「0건」 꺼짐과 같은 뜻) · `board` edit 일 때만. 200 이면 닫힘 · `rejected[]` 코드마다 토스트 · 409 = 그 코드 토스트 · 시트 그대로.
- **호출 취소(U-19)**: 호출 줄 2줄 오른쪽 ⋮(기존 시작 취소 ⋮ 와 같은 모양) → 「호출 취소」 → 확인 창 없이 `POST /api/tasks/{id}/cancel-call` · 성공 토스트 없음 · `task_not_called` 토스트 없음. 조건 = `canCancelCall` + `board` edit.
- **원장 바꾸기(U-22)**: 진행중 · 수락 줄 담당의 글자(이름 · 「간호관리」 · 「담당의 미정」 모두)가 `canChangeDoctor` + edit 이면 주색 글자 + ▾ 로 눌림 → 원장 고르기(U-6 대리 수락과 같은 배치 · 「모든 의사」 없음 · 기본 선택 없음 = 웹 E51) → [원장 변경] → `POST /api/tasks/{id}/doctor {doctorStaffId}`. 누름이 줄 전체(차트 열기)보다 먼저 잡힘.
- 성공 토스트는 네 기능 모두 없음(OQ-A56).

## 글자 출처 (CENTURION_DAY `backend/day/...`)
| 글자 | 출처 |
|---|---|
| 「이미 로그인 중인 기기가 있습니다」 | `templates/partials/login_card.html:17` |
| 「최대 5개 기기에서만 동시 로그인이 가능합니다.」 · 「아래 목록 중 로그아웃 시킬 기기를 선택해주세요.」 | `login_card.html:18` |
| 「{label} · {ip_address}」 · 「방금 전」 · 「n분 전」 | `login_card.html:25-27` |
| 「계속하기」 | `login_card.html:32` |
| 「바로 시작 · N건」 · 「바로 시작」 | `partials/board_parts.html:194` |
| 「선택한 시술」(바로 시작 시트 칸 이름) | `board_parts.html:194` 액션바 `label` |
| 「호출 취소」 | `board_parts.html:123` |
| 「원장 변경」(창 머리 · 버튼) | `templates/ui.html:400` title · `:459` submit(mode `doctor`) |
| 「원장을 변경할 수 없습니다.」 | `routers/board_messages.py` `MESSAGES` |
| 그 밖 실패 글자 · 비우는 코드 | `routers/board_messages.py` · `routers/board.py` `message_of` |

## 비운 글자(원천 없음 — 짓지 않음)
- 네 기능의 **성공 토스트**(OQ-A56).
- `task_not_called` · `room_*` · `visit_not_on_board` 등 웹이 비운 거절 토스트(OQ-A57).
- 기기 선택 「처음으로」(웹에 없음) · 뒤로 가기 안내 글자 없음.
- 바로 시작 시트 머리 아래 설명 · 원장 변경 창 설명 — 없음.

## M1 정리
- **W-2**: 웹 표 복제에 출처 주석 + **동기화 테스트** `test/core/board_messages_contract_test.dart` — 웹 `board_messages.py` 를 읽어 `MESSAGES`(웹 전용 `chart_conflict` 뺌) · `UNSET_MESSAGES` 가 앱 `actionMessages` · `unsetActionCodes` 와 같은지 본다(서버가 코드를 더하면 이 테스트가 깨짐). 실패 글자 함수도 `roomActionMessage` → `boardActionMessage` 하나로 — 판 조작 전부가 웹 `message_of` 규칙(0.2.0 케이스 매트릭스 「새 오류 코드」). 알림 · 채팅 글자 규칙은 그대로.
- **W-3**: `room_move_test.dart` 거절 두 곳에 `find.byKey(Key('toast')) findsNothing` + 「요청이 올바르지 않습니다」 없음 단언.
- 바뀐 동작(주의): 판 조작의 **표 밖 서버 코드**는 전에는 코드 그대로였고 이제 「요청이 올바르지 않습니다」(스펙 OQ-A57 · 케이스 매트릭스대로) · 웹이 비운 코드는 토스트 없음. 앱이 만든 `network_error` · `timeout` · `unexpected_response` 는 전처럼 코드 그대로(OQ-A7 — 전체 테스트가 이 회귀를 잡아 고침).

## 검증
| 명령 | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **+403 ~79 All tests passed**(~79 = 캡처 · 평소 skip · P5 뒤 382 → 403 · 새 21) |
| `fvm flutter build ios --no-codesign` | ✓ Built `Runner.app` (20.7MB) — 마지막 한 줄 고침 뒤 다시 빌드 |
| 캡처 `DAY_CAPTURE_DIR=… flutter test test/capture/m2_capture_test.dart` | 4/4 · PNG 10장 |

실물 서버 · KOS · 시뮬레이터 · 기기 무접촉(테스트 더블 + 실제 `DayApp` 트리). **dev 서버 · 실기기(A-50) = pending**.

## 캡처 (`shots/`)
`m2-{phone,ipad}-device-choice.png` · `m2-{phone,ipad}-room.png`(바로 시작 버튼 · 간호관리 ▾ · 호출 줄 ⋮) · `m2-{phone,ipad}-quick-start-sheet.png` · `m2-{phone,ipad}-cancel-call-menu.png` · `m2-{phone,ipad}-doctor-change.png`

## 계약 대조
| 항목 | 결과 |
|---|---|
| `/api/auth/login` 200 `choose_device` · `/api/auth/device` 요청 칸 · 응답 갈래 · 오류(`session_expired` · `kos_unavailable`) | 같음(be-p2 표) |
| `signed_in_at: null` | 시각 글자 안 그림(웹 `minutes_ago is none`) |
| `/api/visits/{id}/quick-start {taskIds}` · 200 `rejected[]` · 409 첫 거절 코드 | 같음 |
| `/api/tasks/{id}/cancel-call` · `/api/tasks/{id}/doctor {doctorStaffId}` | 같음 |
| 스냅샷 `canCancelCall` · `canQuickStart` · `canChangeDoctor` — 앱 판정 없음 | 같음 |

## 이슈 · 코디가 확인할 것
1. **원장 변경 창 오른쪽 칸 「호출할 시술 · 1개」** — 앱 고르기 창 공통 칸이라 원장 변경에도 보인다. 웹 `_call_body` 도 mode 와 상관없이 같은 글자(`ui.html:500`)라 웹과 같음 — 어색하면 사용자 판단.
2. 아이패드 원장 변경 창은 앱 대리 수락 창과 같은 두 칸 팝오버(웹은 한 칸) — U-6 앱 배치를 따름.
3. 담당의 누름 표시 = 주색 글자 + ▾(글자 아님 · 시안 없음 · M1 방 이름 ▾ 와 같은 방식).
4. 바로 시작 버튼 글자는 「바로 시작」(웹 버튼 「바로 시작 · N건」의 앞부분 — 앱은 드로어에서 고르므로 N 은 드로어 버튼에만).
5. 기기 선택 뒤로 가기 = 입력 화면은 OQ-A53 기본값 — 사용자 확정 아님.
6. 워크트리 `backend/**` P3 변경은 내 것 아님 — 커밋 때 나눌 것.
