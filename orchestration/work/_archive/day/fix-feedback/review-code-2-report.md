# 리뷰 리포트 — fix-feedback / code 2루프 (2026-11-17)

대상: `CENTURION_DAY/fix-feedback` 미커밋 diff 전체(1루프 + 2루프 · 17 파일 수정 + 새 테스트 2) · base dev `4f8316a7`.
기준: e2e-feedback.md(F-5 · E2 · E3 · E5 · E6) · `_RESUME.md` §2 · SPEC-002 개정 ㉒(U-3 :225-229 · :275 · :547 · :578 · :595 · 매트릭스 :740 · 검사 순서 :756 · KOS 표 :847 · 규칙 38 :953 · event 이름 :1008) · SPEC-005 2차 개정 · 고정 사용자 결정(호출 취소 알림 · 새 알림 종류 · migration · KOS 쓰기 없음).
read-only — 리포 파일 고치지 않음 · Docker · 로컬 스택 안 건드림.

## 판정: WARN

FAIL 없음. 2루프 결정 7개(F-5 · 규칙 38 · E3 · E6 · E5 · W2 · E2)는 코드와 맞고, 고정 결정(알림 · migration · KOS 쓰기 0)도 지켜졌다.
다만 **새 표시 버그 1건(N1)** — 「바로 시작」 줄을 [시작 취소]한 뒤 의사 호출하면 호출 줄 원장 칸이 「간호관리」로 나온다(호출 대상 원장 · 「전체」가 가려짐). E2E 2회차에서 만날 수 있는 경로라 고치고 가는 것을 권한다(템플릿 1줄 또는 서버 판정 1줄).

## 테스트 수치 (직접 1회)

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **958 passed, 339 deselected**(17.9s) — fe-2 리포트 수치와 같음 |
| `uv run ruff check backend` | All checks passed |
| `node --check backend/day/static/day.js` | OK |
| infra | 안 돌림(지시 — 코디 몫). be-2 리포트: infra 19 passed(1루프 13 + 새 6) |

## 1. 2루프 결정 대조

| 결정 | 코드 | 판정 |
|---|---|---|
| F-5 ⋮ — 준비중 · 수락 줄 없음 · 호출 → 「호출 취소」 · 진행중 · 완료 그대로 | `board_parts.html:112`(조건 `called and c` · `doing` · `done and canUndoFinish`) · `:122`(메뉴 「호출 취소」 바로 `hx-post …/cancel-call` · 확인 창 없음) · 진행중 · 완료 갈래는 그대로 | PASS |
| 라우트 · 응답 = 다른 줄 조작과 같은 `_after` | `routers/board.py:690` `TASK_ACTIONS["cancel-call"] = board.cancel_call` → 기존 `task_action`(edit 권한 · `_after` OOB + `X-Day-Version`) · 판 전체 다시 받기 없음(:595) | PASS |
| 규칙 38 검사 순서(:756) 404 → `visit_home` → `call_already_accepted` → `task_not_called` | `services/board.py:789-794` `_visit_of` → `_world`(방문 advisory lock — accept 와 같은 잠금) → `_task` → `board_rules.py:293` `cancel_call_block` | PASS |
| 저장 — 그 줄이 든 **열린 호출 전부** `deleted_at` · 받을 시술이 안 남으면 `closed_at` | `services/board.py:797-814`. 유효 호출(`_effective`)은 「가장 최근 호출 · 닫힘이면 없음」(`board_rules.py:64-69`)이라 열린 호출에서 모두 빼면 앞 호출로 되살아나지 않음(닫힌 앞 호출은 effective 에서 걸러짐) | PASS |
| 다른 곳이 빠진 줄을 다시 읽지 않나 | `doctor_call_task` 를 읽는 곳 = `queries/board.py:230` · `services/notifications.py:364` — 둘 다 `deleted_at IS NULL`. 동기화(`emr/`)는 호출 테이블을 안 건드림 → 「다음 동기화가 되돌리지 않음」(:1032) 코드상 맞음. PK `(call_id, task_id)` — 다시 호출은 새 call id 라 충돌 없음 | PASS |
| event_log `call.cancel` 1행 · 한 transaction | `services/board.py:815-829`(`_event` 1 · `_finish` 1 commit) · 이름 = 스펙 :1008 제안 그대로 | PASS |
| KOS outbox 0 · 알림 행 0 · migration 없음 | `cancel_call` 에 `_queue*` · `notifications.*` 호출 없음 · `migrations/` diff 없음 · `NotificationKind` 무변경. infra 테스트가 outbox · 알림 행 증가 0 단언(`test_board_feedback_service.py:360-376`) | PASS |
| 거절 글자 — `task_not_called` 비움 · `call_already_accepted` 기존 | `routers/board.py:145` `UNSET_MESSAGES` · `web_errors.py:113-116` 가 같은 규칙 | PASS |
| E3 「간호관리」 · 원장 변경 똑같이 | 서버 `board_rules.py:149` `system_doctor` + 스냅샷 `:799` `systemDoctor` · `BStaff.is_system`(`dtos/board.py` · `queries/board.py:341`). 화면 `board_parts.html:82-83` 글자 · `doctor_pop` 조건 `t.doctor or t.systemDoctor` · `proc_menu` 원장 변경 창도 같은 조건. 서버 `doctor_change_block` 은 원래 진행중이면 받음(infra 테스트 `:477` 변경 뒤 false) | PASS — 단 N1 |
| E6 차트 = 이름 글자만 · 호버 「차트 작성」 · 나머지 클릭 안 열림 | 줄 `row_attrs` 에서 `data-day-row-get` 제거 · `ui.html` `chart_name`(버튼 · `tip("차트 작성")` · `data-day-row-get`) · 판 줄 두 갈래 + 시술 완료 탭(`board_parts.html:262` 줄 `button` → `span`) · `day.js:852` 는 `[data-day-row-get]` 가 이름 버튼에만 있어 체크 · 버튼 · ⋮ · 시간 칸 클릭은 안 엶. settling 막기 유지 | PASS |
| E5 늘 띄움 | `day.js:1007` `show` = `permission === "granted"` 만(`document.hidden` 없음) | PASS |
| W2 고침(① prime 실패 시 쏟아짐 ② unread 합 상쇄) | `day.js:996-1060` — `lastUnread/grew` 제거 · 신호마다 목록 → `seen` 으로만 거름 · `ready` 플래그(`:1039` 붙을 때 목록 실패면 다음 목록은 `markSeen` 만) · 재연결(open)마다 다시 prime | PASS — review-code-1 W2 해소 |
| E2 원인 · 수정 | `app.css:594` `.day-opt { position: relative }` · `:573` `.day-pick { overflow: hidden; overflow: clip }`. fe 원인 설명(라디오 `absolute` 의 containing block 이 `.day-opt` 가 아니라 팝오버 → 목록 스크롤 밖 · 라벨 클릭 포커스가 hidden 팝오버 자체를 스크롤) 이 CSS 사실과 맞음(`.day-opt__radio` `:598` absolute · 목록은 positioned 아님). dev `4f8316a7` 에도 같은 규칙 — 1루프 회귀 아님 | PASS(코드) · 브라우저 실측 없음 |
| E2 다른 팝오버 회귀 | `.day-opt` 안 absolute 자식은 라디오뿐 · `.day-pick` 은 원래 hidden 이라 clip 으로 바뀌어도 잘리는 범위 같음 · JS 가 `.day-pick` scrollTop 을 쓰는 곳 없음(`day.js` scrollTop 은 keep-scroll 만). 차트 담당자 · 방 옮기기 · 수락 · 원장 변경 팝오버 모두 같은 고침을 받음 · 깨질 자리 못 찾음. `overflow: clip` 미지원 브라우저는 앞 선언 hidden 으로 떨어짐(옛 동작) | PASS |

## 2. 1루프 W 해소 상태

| W | 상태 |
|---|---|
| W1 infra 미실행 | **해소** — be-2 가 `scripts/test.sh` 로 infra 19 passed(1루프 13 포함). 이번 리뷰는 안 돌림(코디 몫) |
| W2 알림 prime · grew | **해소**(위) |
| W3 `conflict` 토스트 = 「요청이 올바르지 않습니다」 | **남음** — 스펙 OQ-66 ⓓ 「정해지지 않음」으로 올라감(spec-3). 코드 그대로 · `message_of` / `web_errors` 중복도 그대로 |
| W7 숨은 aria 글자 | **남음 · 늘었음** — 새 숨은 글자 「{시술} 차트 작성」 · 「간호관리 원장 변경」(fe 리포트 · 기존 틀). 보이는 새 글자는 허용 3개(「호출 취소」 「간호관리」 「차트 작성」)뿐 |
| W9 kit 방별순 | **남음**(개발 화면 · 무시 가능) — kit 라우트 무변경 |

## 3. 앱 영향

- `routers/api/` · `schemas/` · `app/` 워킹트리 diff 없음. 앱 `GET /api/board` 는 같은 `task_view` 를 쓰므로 **더한 칸 `systemDoctor` 하나뿐**(기존 칸 · 값 변화 없음 — 시스템 계정 줄의 `doctor` 는 원래 null).
- 앱에는 호출 취소 경로 없음(스펙 :578 「이번엔 웹만」 그대로). 앱 원장이 받은 호출 알림 행은 남음(결정대로).

## 지적

| # | 등급 | 자리 | 지적 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| N1 | **WARN** | `templates/partials/board_parts.html:82` · `services/board_rules.py:149` | `systemDoctor` 는 **줄 상태와 상관없이** 참이 된다(담당 원장 없음 + KOS 집도의 = 시스템 계정). [시작 취소](`services/board.py:1099` `undo_start`)는 집도의를 안 지우므로 「바로 시작」 → 「시작 취소」 줄은 준비중인데 `systemDoctor = true` → 화면 ① 준비중 줄 「**간호관리** 준비중」 ② 그 줄을 의사 호출하면 원장 칸 우선순위가 `t.doctor → 간호관리 → 전체/지정 원장` 이라 「**간호관리** 호출」 — 호출 대상(「전체」 · 지정 원장 이름)이 가려진다. 수락하면 담당 원장이 생겨 정상으로 돌아옴 | SPEC-002 U-3 :225 — 「간호관리」 는 진행중 「간호관리 · 진행 mm:ss」 · 완료 「간호관리 · n분」 자리만 정함. 호출 줄 글자는 호출 대상(U-3 기존) | 둘 중 하나: (a) 서버 `system_doctor` 에 `self.task_state(t) in ("doing", "done")` 조건(스냅샷 뜻이 스펙 조건과 같아짐 · 앱도 같은 값) (b) 템플릿 `board_parts.html:82` 에서 `t.systemDoctor and t.state in ("doing", "done")`. (a) 권장 + DB 없는 테스트 1개(준비중 · 호출 줄 false) |
| N2 | 참고 | `services/board.py:797-814` | 그 줄을 뺀 **앞 열린 호출**(유효 호출이 아닌 쪽)에 받을 시술이 하나도 안 남아도 그 호출은 닫지 않는다(유효 호출만 닫음) | 규칙 38 「그 호출을 유효 호출로 갖는 시술이 하나도 안 남으면 닫힌다」 — 앞 호출은 이미 다른 줄의 유효 호출이 아니었으면 `calls_view` 가 안 보여주므로(`board_rules.py:903-915` open_tasks 없음 → skip) 화면 영향 없음 | 손댈 필요 없음 · 기록만 |
| N3 | 참고 | `board_parts.html:112` | 호출 줄 ⋮ 는 상태만 본다 — 동시에 다른 탭에서 수락돼도 판이 다시 그려지기 전엔 ⋮ 가 남고 누르면 409 「다른 원장이 먼저 받았습니다」. 서버가 막으므로 안전 | fe 판단(스냅샷에 `canCancelCall` 없음) | 그대로 |

W3 · W7 · W9 는 위 §2 대로 1루프에서 이어짐.

## 조용히 통과하는 자리

1. **N1 은 어느 테스트도 안 잡는다** — `systemDoctor` 테스트는 진행중 줄(바로 시작 직후) · 원장 변경 뒤만 본다(`test_board_feedback_rules.py:159` · `test_board_feedback_service.py:477` · 화면 `test_시스템_계정_집도의_줄은_간호관리…`). 「시작 취소 뒤」 · 「호출 줄」 조합 없음.
2. E2 팝오버 · E6 이름 호버 툴팁 · E5 OS 알림은 **CSS · 속성 글자 단언뿐** — 브라우저 동작 테스트 없음(fe 도 실측 못 함). E2E 에서 눈으로 확인해야 함.
3. 호출 취소 라우트 화면 테스트는 서비스를 가짜로 바꿔 본다 — 서비스 ↔ 라우트를 실제로 이은 것은 없음(infra 서비스 테스트 + 가짜 라우트 테스트 조합 · 1루프와 같은 모양).
4. 웹 `startNotify` JS 단위 테스트 없음 — 문자열 단언(`test_웹_OS_알림은_신호마다…`)만.

## 사용자가 E2E 2회차에서 만날 자리

1. **F-5 호출 취소**: 호출 줄 ⋮ → 「호출 취소」 즉시 · 토스트 없음 · 줄 「준비중」. KOS 데스크엔 그 작업이 「호출(WAITING)」로 남음(감수). 원장 앱 · 웹 알림함의 그 호출 알림은 남음 — 원장이 눌러 들어오면 이미 준비중. 같은 호출의 다른 줄이 남아 있으면 「수락 대기」에 그 호출이 남고 수락하면 남은 줄만 받음.
2. **호출 취소 뒤 다시 호출**: KOS 에는 이미 WAITING 인 작업에 「처음 호출」 쓰기(`call-tasks-doctors`)가 다시 감 — 같은 경로 · 같은 본문이라 KOS 가 받을 것으로 보이나 실물 확인 거리.
3. **N1**: 「바로 시작」 → ⋮ 「시작 취소」 → 그 줄이 「간호관리 준비중」 · 다시 의사 호출하면 「간호관리 호출」(대상 원장 · 「전체」 안 보임).
4. **E3**: 바로 시작 줄 「간호관리 · 진행 mm:ss」 · 「간호관리」 호버 「원장 변경」 · 고르면 KOS `change-tasks-doctors [그 원장]` 1건 · 완료 「간호관리 · n분」(누를 수 없음).
5. **E6**: 차트는 시술 이름 글자만 · 시술 완료 탭 줄은 이제 줄 전체 호버 배경 없음.
6. **E5**: DAY 탭이 앞이어도 OS 알림. 권한 창은 로그인 뒤 첫 클릭(간호 계정에도 뜸 — 1루프 그대로). 신호마다 `GET /api/notifications` 1번(읽음 신호 포함).
7. **E2**: 의사 호출 팝오버에서 맨 아래 원장을 골라도 제목 · 검색 · 추천 · 「선택됨」이 그대로인지 + 수락 · 원장 변경 · 차트 담당자 · 방 옮기기 팝오버도 같은지.
8. (1루프 그대로) `conflict` 토스트 글자(W3) · `/board` 탭 SSE 2개(D5).
