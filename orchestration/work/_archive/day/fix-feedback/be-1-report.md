# fix-feedback backend 1루프 결과 보고 — F-1 귀가 대기 취소 · F-2 정렬 · F-3 바로 시작

## 상태: done (infra 테스트 실행은 pending — 아래 「검증」)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` · 브랜치 `kknaksss/fix-feedback` · 커밋 · push 안 함.

## 수행 — 변경 파일

| 파일 | 무엇 |
|---|---|
| `backend/day/services/board_rules.py` | `BoardSort = Literal["procedure", "room"]` · `BoardRules(world, *, sort="procedure")` · `sorted_cards()`(방별순 = `room_title` 문자열 오름차순 · 안정 정렬 → 같은 이름은 시술순) · `snapshot()` 의 `cards[]` 가 `sorted_cards()` 를 씀 · `quick_start_block(t)`(줄 판정) |
| `backend/day/services/board.py` | `QuickStartResult` · `quick_start(...)` · `undo_home(...)` · `_step_before_home` · `_system_staff`(`_system_account` 에서 떼어 냄 — 동작 같음) · `board(..., sort=)` |
| `backend/tests/day/board/test_board_feedback_rules.py` (새) | DB 없음 4개 — 정렬 기본값 = 지금 순서 · 방별순 순서 · 순서 목록 안 바꿈 · 줄 판정 · 단건 `no_doctor` 그대로 · 시스템 계정은 담당의 아님 |
| `backend/tests/day/board/test_board_feedback_service.py` (새 · `infra`) | 13개 — 아래 |

migration 없음 · 라우터 · 템플릿 · static · styles · 앱 API 안 건드림.

## 계약 대조 (브리프 §3)

| 계약 | 구현 | 같음/다름 |
|---|---|---|
| `quick_start(session, current, visit_id, task_ids) -> QuickStartResult` | `quick_start(session, current, visit_id, task_ids, now=None)` — `now` 는 **선택 인자**(없으면 `datetime.now(UTC)`). 다른 조작처럼 `_now()` 를 넘겨도 되고 안 넘겨도 된다 | 같음(+선택 인자) |
| `QuickStartResult` = `started: list[UUID]` · `rejected: list[tuple[UUID, str]]` | 그대로 · **`services/board.py` 에 `ActionResult` 하위 클래스로 둠**(dtos 아님). 이유: fe 가 바로 시작 응답에 기존 `_after(request, session, current, result)` 를 그대로 쓰려면 `version` · `visit_id` 가 있어야 함. dtos 에 두면 dtos → services import(역방향)가 생김. `result.body` = `{startedTaskIds, rejected:[{taskId, code}], flowStepChanged}` | 위치만 다름 |
| 전부 거절 → 409 첫 거절 코드 | `BoardConflict(rejected[0][1])` · 거절 순서 = 요청 `taskIds` 순서 | 같음 |
| 귀가 대기 방문 → 묶음 전체 409 `visit_home` · 줄 판정 전 | 형식(400) → 카드 · 줄(404) → `visit_home` → 줄마다 | 같음(스펙 §3 「401 · 403 · 404 · 400 · 409 visit_home 묶음 전체」 순서) |
| 검증 실패 = 기존 Validation | 빈 목록 · 겹침 `InvalidRequest`(400) · 다른 카드 · 없는 줄 · 「방 배정」 · KOS 취소 줄 `NotFound`(404) — `call` 과 같은 방식 | 같음 |
| `undo_home(session, current, visit_id) -> None` | `undo_home(session, current, visit_id, now=None) -> ActionResult` — **`None` 대신 `ActionResult`**(`version` · `visit_id` — fe 가 쓰거나 무시하면 됨) | 반환만 다름(더 줌) |
| `visit_not_home` · 방 없음도 `visit_not_home` | 다른 병원 · 없는 방문 404 `not_found` · 판 카드 · 귀가(`completed`) · 다른 날 · 방 없음 409 `visit_not_home` | 같음(매트릭스) |
| 정렬 `sort` 인자 | **`services/board.py` `board(session, current, now, *, version=None, sort="procedure")`** 에 더함 → `BoardRules(world, sort=sort)` → `snapshot()["cards"]`. 기본값이면 지금과 같은 결과. 앱 API(`routers/api/board.py`)는 넘기지 않으므로 그대로 | 같음 |

규칙 대조:

- **규칙 34(바로 시작)**: 준비중만 시작 · 호출 `call_not_accepted` · 수락 · 진행 · 완료 `task_not_waiting` · 담당의(원장 목록 집도의) 있으면 단건 [시작]과 같은 쓰기 · 없으면 DAY 사본 집도의를 시스템 계정 1명으로 덮음(`_set_task_doctor` — 원장 바꾸기와 같은 함수) + outbox `change-tasks-doctors`(같은 카드 그런 줄 한 요청 · `doctorIds=[시스템 KOS id]` · 확인 `doctors_equal=[시스템]` — 기존 `change_doctor` 쓰기 계획 재사용 · status 안 봄 OQ-66 ⓑ). outbox 순서 = `change-tasks-doctors` → `change-flow-step(PROCEDURE)`(첫 시작일 때) → 의사차트 글(OQ-65 ⓐ — 담당의 없으면 `actual=None` 로 글만). 호출(`doctor_call`) 안 만듦. 한 transaction · `event_log` `task.quick_start` 1행(payload `taskIds` · `systemDoctorTaskIds` · `rejected` · `flowStepChanged`) — 줄마다 `task.start` 안 쌓음.
- 시스템 계정 직원이 없거나(동기화 연결이 있는데) 그 KOS id 가 없으면 그 줄만 `conflict`(OQ-66 ⓒ). **동기화 연결이 없는 병원**(KOS 쓰기 자체가 없는 병원)은 시스템 계정 직원만 있으면 DAY 쪽만 하고 시작 — 스펙에 없는 경우라 기존 「연결 없으면 KOS 쓰기 안 만듦」 관례를 따름.
- **규칙 35(귀가 대기 취소)**: 직전 단계 = `visit_flow_log` 의 마지막 `procedure_done` 이전 가장 최근 단계 — `procedure_waiting` · `procedure` 가 아니거나 이력이 없으면 `procedure`(판에 앉을 수 있는 단계로 고정 — **스펙 OQ-58 ⓐ 에 없는 세부 · 코디 확인 거리**). `flow_step` + `visit_flow_log`(source day · actor = 누른 직원) + outbox `change-flow-step(그 단계)` · 마취 · 「방 배정」 · 시술 줄 · 호출 · 차트 안 건드림 · 카드 자리는 규칙 18 그대로(순서 행이 살아 있으면 그 자리 · 없으면 판을 읽을 때 맨 뒤 — 코드 변경 없음) · `event_log` `visit.undo_home` 1행(payload `flowStep`).
- **규칙 36(정렬)**: 방별순은 `board_card_order` 를 읽기만 함 · 귀가 대기는 원래 판 카드가 아님(BOARD_STEPS) · 인박스 · 「시술 완료」 탭 순서 안 바뀜(`inbox()` 는 시각 정렬).
- 단건 [시작] · 앱 API 동작 변경 없음 — 단건 `no_doctor` 회귀 테스트 있음(DB 없는 것 · infra 둘 다).

## 검증 — 명령과 수치

```
uv run pytest -q backend/tests/day/board/test_board_feedback_rules.py backend/tests/day/board/test_board_feedback_service.py
  → 4 passed, 13 skipped (skipped = infra — 이 머신에 PostgreSQL · Docker 데몬이 안 떠 있음)
uv run pytest -q backend/tests/day/board/test_board_rules.py  → 함께 돌려 60 passed(기존 규칙 회귀 없음)
uv run pytest -q -m "not infra"  → 936 passed, 4 failed (무관 — 아래)
uv run ruff check backend/day/services/ backend/tests/day/board/test_board_feedback_*.py → All checks passed
uv run ruff format --check → 통과
```

- **pending — infra 13개**(`test_board_feedback_service.py`: 바로 시작 시스템 계정 경로 · outbox 순서 · 확인 조건 · event_log 1행 · 일부 거절 · 전부 거절 409 · `visit_home` · 400/404 · 시스템 KOS id 없음 `conflict` · 시스템 계정 없음 · 단건 `no_doctor` 회귀 · 귀가 대기 취소 성공/409/404/방 없음 · `sort` 기본값). 사유: Docker 데몬 꺼짐 · 5432 응답 없음 — 사용자 로컬 스택은 띄우지 말라는 브리프라 띄우지 않음. 코디가 `docker compose -f deploy/compose.local.yaml --env-file deploy/local.env up -d --wait postgres redis` 뒤 `scripts/test.sh -q backend/tests/day/board/test_board_feedback_service.py` 로 확인해야 함 — **한 번도 실제로 돌지 않았으니 처음 돌릴 때 테스트 쪽 오타가 나올 수 있음**.
- **무관한 실패 4개(frontend 작업 중 파일)**: `test_screen_copy`(새 문구 「바로 시작 ·」 · 「귀가 대기 취소」 · 「시술순」 · 「방별순」 · 「간호관리차트 있음」 … 근거 표에 없음) · `test_web_rules` 빌드 CSS sha(app.css 바뀜 → `scripts/build-css.sh` 필요) · `day/web/test_board_page.py` 2개. 모두 fe 의 templates · styles 변경에서 나옴 — 내 파일과 무관.

## 상대(frontend) 몫으로 넘긴 것

- 웹 라우트 `POST /board/visits/{id}/quick-start`(폼 `taskIds` 여러 개) → `board.quick_start(session, current, visit_id, ids, _now())` → `_after(..., result)` 그대로 + `result.rejected` 마다(코드별 1장) 토스트 OOB. 전부 거절은 `BoardConflict` 로 올라오므로 기존 409 토스트 경로.
- `POST /board/visits/{id}/undo-home` → `board.undo_home(...)` → 판 다시 받기(D1 — `X-Day-Version` 안 실음).
- `GET /board?sort=room` → `board.board(session, current, _now(), sort=...)`(`room` 아니면 `"procedure"`) · `hx-get` 에 sort 박기(D2).
- 토스트 글자: 새 코드 없음 — `task_not_waiting` · `call_not_accepted` · `conflict`(기존 일반 거절 글자) · `visit_not_home` 글자는 비워 둠(스펙).
- `test_screen_copy` 근거 표 · CSS 빌드 · `test_board_page` 2개 실패 정리.

## 사용자가 E2E 에서 만날 자리

1. **바로 시작 — 담당의 없는 줄**: KOS 에 `change-tasks-doctors [시스템 계정]` 이 먼저, 첫 시작이면 `change-flow-step PROCEDURE` 가 뒤에 감. 확인은 `doctors_equal`(status 안 봄). 여러 sequence 한 요청을 KOS 가 다 받는지는 데모 실물(OQ-66 ⓐ). 판 줄에서 그 줄의 원장 글자는 비어 보임(시스템 계정은 원장 목록 밖 · OQ-62).
2. **귀가 대기 취소 KOS 쓰기**: `change-flow-step PROCEDURE_DONE → PROCEDURE` 를 KOS 가 받는지 확인 안 됨(OQ-58 ⓑ). 안 받으면 outbox 실패 토스트 + 다음 동기화에 카드가 다시 빠짐.
3. 귀가 대기 때 KOS 에서 취소된 「방 배정」은 안 되살림 → 되돌린 카드에 점유 표시가 없음(OQ-58 ⓒ). 닫힌 마취도 안 열림.
4. 귀가 대기 직전 단계가 이력상 판 단계가 아니면 `procedure` 로 되돌림(내 해석 — 위 규칙 35 줄).
5. 방별순은 문자열 정렬 — 「룸10」 이 「룸2」 앞(OQ-59 ⓓ 기본값).
6. (D5 · fe 쪽) 공통 틀 알림 스트림 때문에 `/board` 탭은 SSE 를 둘 연다 — 탭 여러 개면 연결 수가 늘어남.

## 이슈 · 코디가 확인할 것

- `QuickStartResult` 위치(services · `ActionResult` 하위) · `undo_home` 반환(`ActionResult`) · 두 함수의 선택 인자 `now` — 계약과 모양이 조금 다름(위 표). fe 가 계약대로 `now` 없이 불러도 동작.
- infra 테스트 13개 실행 필요(pending).
