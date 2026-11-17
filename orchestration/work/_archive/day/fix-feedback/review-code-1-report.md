# 리뷰 리포트 — fix-feedback / code (2026-11-17)

대상: `CENTURION_DAY/fix-feedback` 미커밋 diff(15 파일 수정 + 새 테스트 2) · base dev `4f8316a7`.
기준: SPEC-002 개정 ㉑(규칙 34 · 35 · 36 · 37 · U-2 · U-3 · U-6 · U-9 · §3 API · 매트릭스 · KOS 쓰기 표 · OQ-58 ~ 66) ·
SPEC-005 2026-11-17 개정(U-5 · §3 웹 OS 알림 · OQ-N8 ~ N13) · fe 브리프 §3 「재검수 review-doc-2 반영」(D1 · sort GET 만 · D2 · D5) · 레포 `AGENTS.md`.
read-only — 리포 파일은 고치지 않았다.

## 판정: WARN

FAIL 없음. 계약 · 스펙 기본값과 코드는 맞는다. 다만 **infra 테스트 13개는 한 번도 돌지 않았다** —
F-3 의 outbox 순서 · event_log 1행 · 시스템 계정 경로, F-1 의 flow log · KOS 쓰기를 단언하는 것은 전부 이 13개뿐이다.
코디가 `scripts/test.sh` 로 한 번 돌려 초록을 확인하기 전까지는 F-1 · F-3 서버 경로가 「검증됨」이 아니다(W1).

## 테스트 수치 (직접 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **948 passed, 333 deselected**(15.3s) — be · fe 리포트 수치와 같음 |
| `uv run ruff check backend` | All checks passed |
| `node --check backend/day/static/day.js` | OK |
| `grep "<script" templates`(src 없는 것) | 0 — 인라인 스크립트 없음 |
| infra(`test_board_feedback_service.py` 13개) | **안 돌림**(브리프 — Docker · 로컬 스택 금지). 코디 몫 |

## 항목별 대조

### 1. F-3 바로 시작 (규칙 34 · 매트릭스 :720-726 · 검사 순서 :742 · KOS 쓰기 :823-824) — PASS(코드) · infra 미검증

| 계약 | 코드 | 판정 |
|---|---|---|
| 검사 순서: 형식 400 → 카드 · 줄 404 → `visit_home` 묶음 → 줄마다 | `services/board.py` `quick_start` — `InvalidRequest`(빈 · 겹침) → `_world`(advisory lock) · `_card` → 줄 404 → `is_home` → `BoardConflict("visit_home")` → `quick_start_block` | PASS |
| 줄 판정: 진행 · 완료 `task_not_waiting` · 호출 `call_not_accepted` · 수락 `task_not_waiting` · 준비중 시작 · `no_doctor` 로 안 막음 | `services/board_rules.py` `quick_start_block`(task_state `called` → call_not_accepted · `ready_wait` 아니면 task_not_waiting) | PASS — 결과 동치(`done`/`doing`/`accepted` 모두 task_not_waiting) |
| 담당의 = KOS 집도의 중 원장 목록 | `rules.kos_doctor(t)`(`board_rules.py:145`) | PASS |
| 시스템 계정 KOS id 없음 → 그 줄 `conflict` | `usable = system_staff and (vendor is None or system_ext)` → 아니면 `(t.id, "conflict")` | PASS (+ 연결 없는 병원은 DAY 만 — be 해석, 스펙에 없는 경우 · W6) |
| 전부 거절 409 첫 거절 코드(요청 순서) | `rejected.sort(key=task_ids.index)` → `BoardConflict(rejected[0][1])` | PASS |
| outbox 순서 `change-tasks-doctors` → `change-flow-step(PROCEDURE)`(첫 시작만) → 의사차트 글 | intents 리스트 순서 그대로 `_queue` | PASS(코드) — 확인 조건 `doctors_equal=[시스템]`(`emr/kos/writes.py:154-163` 재사용 · status 안 봄 OQ-66 ⓑ) |
| DAY 사본 집도의 = 시스템 계정 1명으로 덮음 | `_set_task_doctor`(원장 바꾸기와 같은 함수) | PASS |
| 호출 안 만듦 · 한 transaction · `event_log` `task.quick_start` 1행 | `_event` 1회 · `_finish` 1회 commit · `doctor_call` 없음 | PASS |
| 시술 전 의사차트 = 시스템 계정 줄은 글만(OQ-65 ⓐ) | `_prestart_doctor_chart(..., rules.kos_doctor(t)=None, ...)` | PASS |
| 단건 [시작] `no_doctor` 그대로 · 앱 API 회귀 없음 | `start` · `start_block` 무변경 · `routers/api/` 무변경(diff 없음) · DB 없는 테스트 `test_바로_시작_줄_판정` 이 `start_block(...)=="no_doctor"` 단언 | PASS |
| 웹: 하나라도 시작 = 200 + 카드 조각 + 거절 코드마다 토스트 | `routers/board.py` `quick_start` → `_after(..., toasts=)` · 코드 중복 제거 · `board_action.html` `ui.toast_oob` | PASS |
| N = 체크한 준비중 줄 · 0 이면 disabled | `ui.check_item(quick=p.status=="wait")` → `data-day-quick` · `day.js` `syncChecks` | PASS |

`hx-include="[data-day-quick='{방문}']"` 는 체크된 checkbox 만 실리고(htmx 규칙) 체크 칸 이름이 `taskIds`(`board_parts.html:79` `"field": "taskIds"`)라 `hx-params="taskIds"` 와 맞다 — 경로 추적상 OK.

### 2. F-1 귀가 대기 취소 (규칙 35 · 매트릭스 :724-726 · KOS 쓰기 :838 · D1) — PASS(코드) · infra 미검증

| 계약 | 코드 | 판정 |
|---|---|---|
| 세션 병원 아님 · 없는 방문 404 | `owner != current.hospital_id → NotFound` | PASS |
| 귀가 대기 아님(판 카드 · 귀가 · 다른 날) · 방 없음 → 409 `visit_not_home` | `v is None or not is_home(v) or v.room_id is None` (다른 날 = 오늘 world 에 없음 → None) | PASS |
| 직전 단계 = `visit_flow_log` 의 귀가 대기 바로 앞 | `_step_before_home` — 마지막 `procedure_done` 의 `changed_at` 이하 · 그 단계 아닌 가장 최근 · `procedure_waiting`/`procedure` 밖이면 `procedure` | PASS — 「판 단계로 고정」은 be 해석(W5) |
| `flow_step` + `visit_flow_log`(day · actor) + outbox `change-flow-step(그 단계)` | `_flow` · `_queue_simple(... flow_step)` · `KOS_STEPS` 에 `procedure_waiting` 도 있어 `WriteNotSupported` 안 남 | PASS |
| 마취 · 방 배정 · 시술 줄 · 호출 · 차트 안 건드림 · `visit.undo_home` 1행 · 잠금 | 해당 쓰기 없음 · `_world(visit_id)` advisory lock | PASS |
| D1: 판 전체 다시 받기 · `X-Day-Version` 없음 | 라우트 = 본문 없음 + `HX-Trigger: day:board-refresh` + `HX-Reswap: none` + `X-Day-Action: 1` · `board.html` `hx-trigger="sse:board, day:board-refresh from:body"` | PASS — 아래 경로 추적 |
| 확인 창 · 성공 토스트 없음 · `visit_not_home` 글자 비움 | 메뉴 줄이 바로 `hx-post` · `UNSET_MESSAGES` 에 `visit_not_home` | PASS (브리프 §6-5 문구는 모호했으나 SPEC U-9 · OQ-58 ⓔ 와 맞게 읽음) |
| 「귀가」 카드엔 ⋮ 없음 · edit 권한 | `undo = EDIT and item.state == "home"` · 라우트 `_allowed(EDIT)` | PASS |

**D1 `day.js` 경로 추적(카드가 실제로 다시 앉는가)**: htmx 는 `HX-Trigger` 를 `htmx:beforeSwap` 보다 **먼저** 요청 elt(메뉴 줄 — 아직 DOM 안)에 쏜다 → body 로 버블 → `#board-main` `hx-get` 발동 →
`htmx:beforeRequest`(day.js :555) — 신호 본문 없음 → `signalDecision` = fetch → 그러나 메뉴가 열려 있어 `busy()` = true → `refreshDeferred = true` · 취소 →
같은 응답의 `htmx:beforeSwap` 에서 `X-Day-Action` → `closePop(false)` → `flushRefresh()`(:111) → 50ms 뒤 `htmx.trigger(root, "sse:board")` → 판 전체 GET(`hx-get` 에 박힌 `?sort=room` 유지 · `hx-params="none"` 은 경로의 쿼리를 지우지 않음). **카드가 판에 다시 앉는다 · 방별순도 유지.** 뒤이어 오는 이 조작의 SSE `board` 신호는 version 이 `ownVersions` 에 없어 한 번 더 받을 수 있다(무해 · 중복 GET 1회).

### 3. F-2 정렬 탭 (규칙 36 · U-2 · §3 「정렬 탭」 · D2) — PASS

- `GET /board?sort=room` 만 sort 를 받는다(`board_page` `_sort`) · 조작 POST 는 sort 를 싣지 않음(`_fields` 400 그대로 — fe 테스트 단언). `_render_board` 호출처는 `board_page` 하나뿐 — 조작 응답은 전부 `_after`(OOB)라 판 순서 · 탭을 바꾸지 않는다.
- SSE `hx-get` 에 sort 박음(`board.html`) · 판 조각(`board_main.html`)이 탭 `aria-current` · 방별순이면 grid form 에 `data-day-sort` · `hx-put` 없음 → `day.js` 끌기 시작 안 함. OOB 로 다시 그린 카드의 손잡이는 CSS(`.day-board__grid:not([data-day-sort]) .day-grip`)로 숨김.
- 서버 정렬 `sorted_cards` = 안정 정렬 `(is_home, room_title)` · 기본값이면 `ordered_cards` 그대로 · `board_card_order` 안 씀 — DB 없는 테스트가 여러 카드로 단언(`test_board_feedback_rules.py:21-55`).
- `hx-boost` 없음 확인 — 탭 링크는 전체 페이지 이동이라 조각 오염 없음.

### 4. F-4 웹 OS 알림 (SPEC-005 U-5 · §3 :278-281 · OQ-N8 ~ N13 · D5) — PASS(경고 있음)

- 로그인 화면: `base.html` 은 `{% if session %}` 일 때만 `data-day-notify` → 로그인 화면 스트림 없음. 권한 없는 계정: `/api/notifications` · `/stream` 은 `current_session` 만(권한 키 없음) — 원장 아닌 계정은 원장 호출 행이 없어 조용히 아무것도 안 뜸. 오류 표시 경로 없음.
- `document.hidden` · `permission === "granted"` 일 때만 · `tag = 행 id` · 열릴 때(`open` — 재연결 포함) 목록을 「본 것」으로(N13) · 첫 클릭 1회 `requestPermission` · 클릭 → `window.focus()` + `/board` · 읽음 처리 없음 · `session_expired` 면 close — 모두 기본값과 같음.
- 인라인 스크립트 0 · CSP 문제 없음. `/board` 의 htmx SSE(`/board/stream`)와 별도 EventSource — 상태 공유 없음(충돌 없음 · 연결 2개 = D5).
- 재호출은 새 call id → 새 행(`services/notifications.py:14`)이라 `seen` 에 막히지 않음.

### 5. F-6 · F-7 — PASS

- F-6 `ui.chart_icons`: 작성된 것만 brand · 둘 다 없으면 `day-proc__icons` 칸 자체 없음 · `disabled` 아이콘 0. 호출처 = 완료 줄(`ui.html:284`) · 시술 완료 탭(`board_parts.html:255`) · 키트 견본(같은 매크로). 미완료 줄은 원래 아이콘 없음.
- F-7 `ME_LISTED` = `session.staff_id` ∈ `snapshot.doctors[].staffId`(`board_regions` 의 `me_listed` 와 같은 식) → 팝오버 없이 `hx-post …/accept` + `hx-vals doctorStaffId=본인` · `ACCEPT`(board.accept edit) 조건 유지 · `_after` OOB 도 `session=current` 를 넘겨 같은 판정.
- **간호 계정 팝오버 회귀 질문**: 사라진 「보는 사람이 원장이면 본인」 기본 선택 갈래는 **원장 계정일 때만** 쓰이던 갈래다. 이제 원장 계정은 팝오버 자체를 안 그리므로(`{% if not me_listed %}`) 그 갈래는 죽은 코드였다 — 간호 · 관리 계정의 기본 선택(지정 호출 = 지정 원장 · 전체 = 없음)은 그대로. **의도와 맞음 · 회귀 아님.**

## WARN

| # | 자리 | 지적 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| W1 | `backend/tests/day/board/test_board_feedback_service.py` 전체 | infra 13개가 **한 번도 실행되지 않음**(be 리포트 「처음 돌릴 때 테스트 쪽 오타가 나올 수 있음」). F-3 outbox 순서 · `doctors_equal` · event_log 1행 · `conflict` · F-1 flow log · KOS 쓰기를 단언하는 유일한 테스트 | AGENTS.md 「테스트」 · 리뷰 체크 「조용히 통과하는 자리」 — 지금 948 passed 는 이 경로를 하나도 안 거친다 | 코디가 compose PostgreSQL · Redis 로 `scripts/test.sh -q backend/tests/day/board/test_board_feedback_service.py` 1회 → 실패면 be 2루프 |
| W2 | `backend/day/static/day.js` `startNotify` `onSignal` (`grew` 판정) | ① 첫 `prime` 이 실패하면(`lastUnread === null`) 다음 신호에서 **오늘 안 읽은 원장 호출 전부**를 OS 알림으로 쏟아냄(N13 「끊긴 동안 것 안 띄움」과 어긋날 수 있음). ② 같은 순간 다른 기기(앱)에서 읽음 처리로 `unread` 가 줄면서 새 호출이 들어와 합이 같거나 줄면 새 알림을 놓침 | SPEC-005 OQ-N13 · §3 :278(㉠ 「늘었을 때」) | ① `prime` 실패면 첫 신호 때 목록을 「본 것」으로만 채우고 띄우지 않기 ② (선택) `grew` 대신 늘 목록을 받아 `seen` 으로만 거르기 — 요청 1번 더 · 2루프 판단 |
| W3 | `backend/day/routers/board.py` `message_of` · `web_errors.board_error_handler` | 시스템 계정 KOS id 없음(`conflict`) 거절 토스트가 「요청이 올바르지 않습니다」(invalid_request 글자)로 나온다 — 사용자는 원인을 알 수 없음. 같은 규칙이 두 군데(중복) | SPEC-002 :765 토스트 표에 `conflict` 행 없음 · OQ-66 ⓒ(새 코드 없음 기본값) | 글자는 사용자 결정(2루프) · 중복은 `web_errors` 가 `message_of` 를 쓰게 |
| W4 | `tests/architecture/test_screen_copy.py` | fe allowed_paths(`backend/tests/day/`) 밖 파일 수정. 단 fe 브리프 §4 가 이 파일(:126-127)을 이름으로 지목 — 브리프 안의 모순 | reviewer rules 「allowed_paths 이탈」 · fe 브리프 §4 · §5 | 코디가 수용 여부만 기록(내용은 근거 표 추가 · 문제없음) |
| W5 | `services/board.py` `_step_before_home` · `UNDO_HOME_STEPS` | 직전 단계가 판 단계(`procedure_waiting`/`procedure`)가 아니면 `procedure` 로 고정 — OQ-58 ⓐ 기본값에 없는 세부(be 해석). 같은 `changed_at` 동점이면 `id`(uuid) 로 갈려 사실상 임의 | SPEC-002 OQ-58 ⓐ | 스펙 OQ-58 ⓐ 에 이 해석을 적어 닫거나 사용자 확인 |
| W6 | `services/board.py` `quick_start` `usable` | 동기화 연결이 없는 병원(vendor None)은 시스템 계정 직원만 있으면 KOS 쓰기 없이 DAY 만 시작 — 스펙에 없는 경우(be 해석 · 기존 「연결 없으면 KOS 쓰기 안 만듦」 관례) | 규칙 34 · OQ-66 ⓒ | 스펙에 한 줄 |
| W7 | `templates/partials/board_main.html` 정렬 탭 `aria-label="정렬"` · done 카드 ⋮ `aria-label="{고객} 더보기"` | 브리프 허용 글자 밖의 새 숨은 글자(스크린 리더만). `test_screen_copy` HIDDEN 에 「보이지 않음」으로 등록 | fe 브리프 §7 「화면 글자 발명 금지」 | 2루프에서 스펙 글자 표에 올리거나 수용 |
| W8 | SPEC-002 §3 「귀가 대기 취소 응답 = 판 조각 + 시술 완료 탭 OOB」 · 「판 조각을 돌려주는 조작 응답도 같은 sort 를 실어」 | 코드는 코디 D1(판 다시 받기) · 「sort 는 GET 만」대로 — 스펙 글이 아직 옛 문장 | fe 브리프 §3 D1 「스펙은 뒤에 맞춘다」 | 스펙 개정 ㉑ 보충에 D1 · sort 문장 반영 |
| W9 | `routers/kit*.py`(무변경) · `board_main.html` `sort_base="/dev/kit/board"` | 키트 견본의 「방별순」 링크는 kit 라우트가 `sort` 를 안 받아 늘 시술순으로 보임 | 규칙 37 「키트 견본도 같은 규칙」(F-6 만 해당 — F-2 는 해당 문장 없음) | 개발 화면이라 무시 가능 · 원하면 kit 라우트에 sort 전달 |

## 조용히 통과하는 자리

1. **infra 13개 skip**(W1) — `pytest -m "not infra"` 948 passed 는 F-1 · F-3 서비스 경로를 한 줄도 실행하지 않는다. fe 라우트 테스트는 서비스를 가짜로 바꿔서(`monkeypatch services.board.quick_start` 등) 라우트 · 조각만 본다 — be 서비스와 fe 라우트를 **실제로 이은 테스트는 0개**.
2. `test_판_읽기_sort_기본값은_지금_순서`(infra) 는 카드 1장이라 순서를 사실상 단언하지 않는다 — 여러 카드 순서는 DB 없는 `test_board_feedback_rules.py:21` 이 맡는다(이건 OK).
3. D1 판 다시 받기는 `HX-Trigger` 헤더 · `hx-trigger` 속성 글자만 단언 — 「메뉴 열린 채 미뤘다가 closePop → flushRefresh 로 받는다」 브라우저 경로는 테스트 없음(위 §2 에서 코드로 추적해 OK 판정).
4. F-4 `startNotify` 는 JS 단위 테스트 없음 — `body[data-day-notify]` 렌더 여부만 단언.
5. 차트 아이콘 on 판정은 Jinja truthy — 공백만 있는 `assignee_note` 가 저장돼 있으면 아이콘이 그려진다(규칙 37 「공백 정리 뒤 빈 글 = 없음」). 저장 쪽 정규화에 기대는 기존 판정 그대로(참고 · 기존 부채).

## 사용자가 E2E 에서 만날 자리

1. **F-3 담당의 없는 줄**: KOS 에 `change-tasks-doctors[시스템 계정]` → (첫 시작이면) `change-flow-step PROCEDURE` 순. `sequences` 여러 개를 KOS 가 다 받는지 확인 안 됨(OQ-66 ⓐ). 시작된 줄의 원장 글자는 빈 칸(「 · 진행 mm:ss」 앞 원장 없음 · OQ-62).
2. **F-3 시스템 계정 KOS id 없음**이면 그 줄만 빨간 토스트 「요청이 올바르지 않습니다」(W3) — 원인 글자 아님.
3. **F-3 버튼**: 호출 줄만 체크하면 「바로 시작 · 0건」 꺼짐 · 성공(일부 거절 포함) 뒤 그 카드 체크가 풀린다 · 거절 코드마다 토스트 1장.
4. **F-1 KOS**: `change-flow-step PROCEDURE_DONE → PROCEDURE` 를 KOS 가 받는지 미확인(OQ-58 ⓑ). 거절되면 「KOS 반영 실패」 토스트 + 다음 동기화에 카드가 다시 「시술 완료」로 빠질 수 있다. 되돌린 카드엔 점유 표시 · 마취가 없다(OQ-58 ⓒ ⓓ).
5. **F-1 화면**: ⋮ → 「귀가 대기 취소」는 확인 창 없이 즉시 · 판 전체가 한 번(또는 SSE 로 두 번) 다시 그려짐 · 스크롤 · 체크는 기존 keepState 로 유지.
6. **F-2**: 방별순은 문자열 정렬 — 「룸10」 이 「룸2」 앞(OQ-59 ⓓ). `?sort=room` 이 URL 에 남아 새로 고침해도 방별순 · 사이드 메뉴로 `/board` 들어오면 시술순. 방별순에서 손잡이 없음 · 끌기 안 됨.
7. **F-4 (D5)**: `/board` 탭은 SSE 2개(`/board/stream` + `/api/notifications/stream`). 로컬 uvicorn(HTTP/1.1) 직접 접속이면 브라우저 origin 당 6연결 한도라 **DAY 탭 3개 이상**에서 요청이 멈출 수 있다(Caddy HTTP/2 뒤에선 해당 없음).
8. **F-4 권한 · 표시 조건**: 로그인 뒤 **아무 곳 첫 클릭**에 권한 창(간호 계정에도 뜸 — 원장만 물을지는 OQ-N8 미정). 알림은 원장 목록 계정 + DAY 탭이 **숨겨졌을 때(`document.hidden`)** 만 — 브라우저 창이 다른 프로그램에 **일부만** 가려져 있으면 hidden 이 아니라 안 뜬다(사용자 말 「다른 프로그램 위에도」와 차이 · OQ-N9). macOS 는 브라우저 자체 시스템 알림 허용도 필요. 눌러도 읽음 처리 안 됨.
9. **F-7**: 원장 계정 [수락] = 팝오버 없이 즉시 본인(다른 원장 지정 호출도 본인). 원장 직무 태그가 붙은 공용 PC 계정이면 그 계정이 집도의로 남는다(OQ-64).

## 참고(기존 부채)

- 차트 아이콘 공백 글 판정(위 「조용히」 5) — 기존 판정 그대로.
- 고객 검색 조각(`GET /board/search`)은 권한 값을 넘기지 않아 view 계정에도 ⋮ 가 그려짐(누르면 403 토스트) — fe 리포트가 적은 기존 동작과 같음.
