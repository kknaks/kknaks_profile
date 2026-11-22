# 코드 검수 — mobile M2 (커밋 `b91d2fca`)

대상: `b91d2fca` app/ 16파일 · 대조: 서버 계약 `e96b0718`(`routers/api/auth.py` · `routers/api/board.py` · `schemas/auth.py` · `schemas/board.py` · `schemas/responses.py`) · 웹 `templates/ui.html` · `partials/board_parts.html` · `routers/board.py` · `routers/board_messages.py` · `web_errors.py` · 스펙 SPEC-003 U-17 · U-18 · U-19 · U-22 · OQ-A57. 읽기만 했다(수정 · 커밋 없음 · 워크트리 `app/` 은 HEAD 와 같음).

## 결론: **FAIL 1 · WARN 3 · 나머지 PASS**

| # | 등급 | 요약 |
|---|---|---|
| F-1 | **FAIL** | 원장 변경 창의 「호출할 시술 · 1개」 칸은 웹에 없는 글자. 리포트의 원천 주장(`ui.html:500`)이 틀렸다 |
| W-1 | WARN | 바로 시작 `rejected[]` 토스트: 웹은 코드를 중복 없이 한 장씩 쌓고, 앱은 토스트 칸이 하나라 마지막 것만 남는다 |
| W-2 | WARN | 캡처의 ⋮ 메뉴 굵은 검은 테두리 = 캡처 렌더 탓(실제 모양 아님). 캡처 하네스는 고쳐야 한다 |
| W-3 | WARN(낮음) | 호출 취소 ⋮ 에 앱이 `t.state == 'called'` 조건을 덧붙였다(서버 값만으로 그린다는 원칙에서 조금 벗어남. 지금은 결과가 같다) |

---

## 1. 서버 계약 — PASS

| 항목 | 앱 | 서버 | 판정 |
|---|---|---|---|
| 기기 선택 요청 | `day_api.dart:126` `POST {target}/api/auth/device {pending_token, device_id, client:"app"}` | `schemas/auth.py:82-99` `DeviceRequest`(`pending_token` · alias `device_id` · `client`, forbid) | 같음 |
| 기기 선택 응답 | `session_controller.dart:207` `_answer`: `choose_hospital` · `choose_device` · `signed_in`. `devices[].{id,label,ip_address,signed_in_at}` | `routers/api/auth.py:141-159` `SignedIn \| ChooseHospital \| ChooseDevice` · `schemas/auth.py:204-245` | 같음. `signed_in_at: null` 이면 시각 글자 없음(`copy.dart` `deviceAgo`) |
| 기기 선택 오류 | `session_controller.dart:275` `_pendingFailed`: `session_expired` = 입력 화면 + 문구. 그 밖 = 로그인 오류 칸 | `auth.py:154` 401 `session_expired` | 같음(U-17 「실패」) |
| 연결 대상 검증 | `session_controller.dart:247-` 응답 origin · 환경이 다르면 `environment_unavailable` | 병원 고르기와 같은 규칙(A-20) | 같음 |
| 바로 시작 | `board_controller.dart:198` `POST /api/visits/{id}/quick-start {taskIds}` · 200 `rejected[].code` 마다 토스트 · 409 = `run` 의 그 코드 토스트 | `routers/api/board.py:287-302` · `schemas/board.py:48` `QuickStartBody.taskIds` · `schemas/responses.py:26-56` `{startedTaskIds, rejected[{taskId,code}], flowStepChanged}` | 같음(토스트 개수는 W-1) |
| 호출 취소 | `board_controller.dart:211` `POST /api/tasks/{id}/cancel-call`(본문 없음) | `routers/api/board.py:346-363` `/tasks/{task_id}/{action}` · `TASK_ACTIONS["cancel-call"]`(`routers/board.py:545`) | 같음 |
| 원장 바꾸기 | `board_controller.dart:215` `POST /api/tasks/{id}/doctor {doctorStaffId}` | `routers/api/board.py:246-263` `AcceptBody.doctorStaffId`(`schemas/board.py:41`) | 같음 |
| 스냅샷 칸 | `model/board.dart` `canCancelCall` · `canQuickStart` · `canChangeDoctor`(관대한 읽기 `_b`) | `presentation/board.py:172-174` | 같음 |

## 2. 서버 값만으로 그리나 — PASS(W-3 하나)

- 바로 시작: 버튼은 `card.tasks.any(canQuickStart)` + edit(`room_screen.dart:480`). 시트에서 체크할 수 있는 줄은 `_can(t) = t.canQuickStart`(`doctor_picker.dart` `_can`). 앱이 따로 판정하지 않는다. PASS.
- 원장 바꾸기: `me.canEditBoard && t.canChangeDoctor` 만 본다(`room_screen.dart:614-`). 이름 · 「간호관리」 · 「담당의 미정」이 모두 같은 조건이다(U-22). PASS.
- **W-3** 호출 취소: `room_screen.dart:578` `if (edit && t.state == 'called' && t.canCancelCall)`. 서버 `cancel_call_block`(`policies/board_rules.py:641-`)이 이미 `task_not_called` 를 거르므로 지금은 결과가 같다. 다만 상태 조건은 앱 판정이 덧붙은 것이다(U-19 「보이는 조건 = canCancelCall + board edit」). 제안: `t.state == 'called'` 를 빼거나, 왜 두는지(예: 진행중 ⋮ 와 겹치지 않게) 주석을 단다.

## 3. 글자 원천

### F-1 FAIL — 원장 변경 창 「호출할 시술 · 1개」

- 앱: `room_screen.dart:528` 이 `_openDoctorChange` 에 `procs: [t.title]` 를 넘긴다. 그러면 `doctor_picker.dart:416-433` `_chosenSection` 이 「선택됨」 아래에 **「호출할 시술 · 1개」 + 「· {시술명}」** 를 그린다(폰 = 같은 시트 아래, 아이패드 = 오른쪽 칸. 캡처 `m2-*-doctor-change.png`).
- 웹 원장 변경 창에는 이 칸이 **없다**:
  - `partials/board_parts.html:135` 원장 변경 = `call_dialog("doctor-…", "doctor", "", [t.title], …)` → `:54` `doctor_call_modal(…, as_popover=true)`
  - `ui.html:406` `{%- set layout = "wide" if mode == "call" else "single" -%}`. 즉 doctor 는 늘 `single` 이다.
  - `ui.html:496-502` 「호출할 시술 · N개」는 `{%- if layout != "single" %}` 안에만 있다. 그래서 웹 원장 변경 · 수락 창에는 「선택됨 → 전체 → 원장 목록」(`ui.html:472-476`)만 있고 시술 칸이 없다. (`ui.html:465` 도 같다. single 이면 `where` 글자도 비운다.)
- 그러니 mobile 리포트 「이슈 1」의 「웹 `_call_body` 도 mode 와 상관없이 같은 글자(`ui.html:500`)라 웹과 같음」은 **틀린 원천 주장**이다. 원장 바꾸기는 호출이 아닌데 「호출할 시술」이 뜬다. 원천에 없는 글자를 쓴 것이다(M-9 · 글자 짓기 금지).
- 고칠 방향(가장 작게): `room_screen.dart:528` 를 `procs: const []` 로 바꾼다. `_chosenSection` 은 `titles.isNotEmpty` 일 때만 칸을 그리므로 이것만으로 칸이 사라진다. 아이패드 오른쪽 칸에는 「선택됨」만 남는다.
- 참고(같은 계열, 이번 범위 밖): 앱 U-6 대리 수락(`accept.dart` · `PickMode.accept`)도 같은 칸을 그린다면 웹 수락 창(single)과 다르다. 0.1.0 부터 그랬던 배치라 사용자 · 코디가 판단할 일이다.

### 그 밖 글자 — PASS
| 글자 | 원천 | 확인 |
|---|---|---|
| 기기 선택 4줄 · 「계속하기」 · 「방금 전」/「n분 전」 | `login_card.html:17-32` | 리포트 표와 같음 |
| 「바로 시작 · N건」 · 「선택한 시술」 | `board_parts.html:194` 버튼 · 액션바 `label` | 같음 |
| 「호출 취소」 | `board_parts.html:123` `menu_row` | 같음 |
| 「원장 변경」(머리 · 버튼) | `ui.html:400` title · `:459` submit | 같음 |
| 「원장을 변경할 수 없습니다.」 | `board_messages.py` `MESSAGES.task_not_assignable` | 같음(계약 테스트가 지킴) |
| 바로 시작 시트 머리 「바로 시작」 | 웹에는 창이 없어 버튼 글자를 빌림 | 원천 글자 재사용. 사용자 결정(드로어) 안이라 허용 |

### W-2 WARN — ⋮ 메뉴 굵은 검은 테두리 = 캡처 렌더 탓(실제 모양 아님)
- 위젯은 기존 시작 · 완료 취소 ⋮ `_more`(`room_screen.dart:662-676`)와 **글자 하나까지 같다**(`PopupMenuButton` · `padding: zero` · 32×32 `more_vert_rounded` 20 · `Ms.gray600`). 테마에 `popupMenuTheme` 은 없다(`theme.dart:120-` M3 기본값).
- 원인: flutter_test 는 `debugDisableShadows = true` 가 기본이다. 이때 `RenderPhysicalShape` 는 그림자 대신 `shadowColor`(검정)로 **`elevation × 2` 굵기의 선**을 그린다(fvm 3.44.8 `packages/flutter/lib/src/rendering/proxy_box.dart:2216-2224 · :2321-2329`). M3 팝업 메뉴는 elevation 3 이라 6px 검은 테두리가 된다. 실기기에서는 M3 기본(옅은 그림자 · 둥근 4 · surfaceContainer 바탕)이다.
- `test/capture/m2_capture_test.dart` 에는 `debugDisableShadows` 를 끄는 줄이 없다. 그래서 이 캡처로는 메뉴 모양을 판단할 수 없다. 제안: 캡처 테스트 앞에서 `debugDisableShadows = false`(끝에 되돌림)로 다시 찍는다. 다른 캡처의 바텀 시트 · 팝오버도 같은 영향을 받는다.

## 4. 실패 글자 통합(OQ-A57) — PASS(W-1 하나)

- `boardActionMessage`(`copy.dart`)의 규칙은 웹 `message_of`(`routers/board.py:600-607`) · `web_errors.py:113-116` 과 같다. 미정 = 빈 값, 표 = 글자, 그 밖 = 「요청이 올바르지 않습니다」. 표 동기화 테스트 `test/core/board_messages_contract_test.dart` 는 웹 파일을 읽어 `MESSAGES`(chart_conflict 뺌) · `UNSET_MESSAGES` 를 비교한다. 좋다.
- 회귀:
  - `BoardController.run` 의 6번째 인자(`message`)를 지우고 `onOk` 로 바꿨다. `flutter analyze` 가 통과하므로 다른 호출부도 함께 바뀌었다.
  - 앱이 만든 코드(`network_error` · `timeout` · `unexpected_response`)는 코드 그대로 둔다(`board_controller.dart:147`). OQ-A7 이 유지된다.
  - 알림(`notification_controller.dart:19`) · 채팅(`chat_copy.dart:40`)은 그대로 `actionMessage` 를 쓴다.
  - 동작이 바뀐 곳: 판 조작에서 서버가 준 **표 밖 코드**가 전에는 코드 그대로였고 이제 「요청이 올바르지 않습니다」다. `UNSET` 코드(`chart_staff_required` · `staff_not_listed` 등)는 토스트가 없어졌다. 스펙 케이스 매트릭스 `:853` · OQ-A57 과 같다. 참고: 서버가 5xx 에 코드를 실어 보내면 그것도 「요청이 올바르지 않습니다」가 된다. 웹 `board_error_handler` 는 400/404/409 `ServiceError` 만 다루므로 5xx 글자는 웹에도 원천이 없다. 막을 일은 아니고 알아만 둘 것.
- **W-1** 바로 시작 `rejected[]`(`board_controller.dart:198-207`):
  - 웹: `routers/board.py:628-629` `codes = list(dict.fromkeys(...))` 로 **중복을 뺀 코드마다 토스트 한 장씩, 여러 장**을 띄운다.
  - 앱: 거절 **줄마다** `toasts.show` 를 부른다. 그런데 `ToastController.show`(`core/toast.dart:14-17`)는 `current` 하나를 갈아 끼우므로 화면에는 **마지막 코드 한 장만** 남는다. 거절 코드가 둘 이상(예: `call_not_accepted` + `task_not_waiting`)이면 앞 글자를 잃는다. 같은 코드가 여러 번이면 같은 토스트를 갈아 끼울 뿐이라 겉으로는 티가 안 난다.
  - 스펙 U-18 「거절 코드마다 실패 토스트 하나」를 앱 토스트 구조로는 다 보여 줄 수 없다. 사용자 · 코디가 정할 것: (a) 지금처럼 마지막 하나 (b) 코드를 중복 없이 모아 한 장에 줄바꿈 (c) 토스트 줄 세우기. 적어도 웹처럼 코드 중복은 빼는 편이 좋다. 테스트(`m2_actions_test.dart:101-105`)는 거절 한 줄만 본다.

## 5. 정적 검사 · 테스트 — PASS
| 명령(app/) | 결과 |
|---|---|
| `fvm flutter analyze` | No issues found! |
| `fvm flutter test test/ui/m2_actions_test.dart test/state/device_choice_test.dart test/core/board_messages_contract_test.dart test/ui/room_move_test.dart` | +38 All tests passed! |

## 그 밖 확인(PASS)
- 기기 선택 뒤로 가기: `PopScope(canPop:false)` → `backToStart()`(OQ-A53 기본값 · 사용자 확정 아님. 리포트 이슈 5 그대로).
- 새 목록이 오면 처음 선택을 첫 줄로 되돌림: `identical(_deviceList, s.devices)`(`login_screen.dart`). `_answer` 가 늘 새 리스트를 만들므로 다시 막혀도 첫 줄로 돌아간다.
- 바로 시작 시트 아이패드: `widget.wide && !_quick` 이라 한 칸이다. 오른쪽 칸 없음(F-1 과 다름).
- 원장 바꾸기 기본 선택 없음 · 「모든 의사」 없음: `_withAll` 은 call/recall 에만 있다. 웹 E51 과 같다.
