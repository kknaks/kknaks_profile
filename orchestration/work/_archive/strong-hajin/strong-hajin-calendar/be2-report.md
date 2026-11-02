# WORK-004 Phase BE-2 결과 보고 — D1 세 자리 · `schedule_release` · 운영 대장

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar` · BE-1 은 `1c15d02` 로 커밋돼 있고
**이번 변경은 전부 uncommitted** 다. **커밋·push 하지 않았다.**

---

## 1. 변경 파일 (수정 8 · 신규 1)

| 파일 | 무엇 |
|---|---|
| `backend/src/ax_workspace/modules/work/application.py` | D1 훅(`_release_schedules_outside`·`_schedule_release_for`) + **세 자리**에 명시적으로 걸기 · K16 역량 문 둘 |
| `backend/src/ax_workspace/modules/work/task_results.py` | `TaskScheduleReleaseView` · `TaskDateMutationResult` |
| `backend/src/ax_workspace/bootstrap/application.py` | `update_task`·`transition_task` 반환 타입 |
| `backend/src/ax_workspace/entrypoints/http.py` | `PATCH /api/tasks/{id}` · `POST /api/tasks/{id}/start` 응답 타입 |
| `docs/unified-operations-inventory.json` | **행 3 + `http_count` 1줄 + `http_signature` 3줄** |
| `docs/domain-model.md` | `task_schedules` 대조표 **한 줄** |
| `Makefile` | local-stack preflight 표지에 `task_schedules` |
| `backend/tests/architecture/test_local_stack_targets.py` | 그 표지를 **함께** 세는 두 줄 |
| `backend/tests/contract/test_task_schedule_release.py` **(신규)** | D1 세 자리 · 복구 없음 · 재배정 · K16 (13건) |

`frontend/`·`para/`·`orchestration/`·그 밖의 `docs/` 는 건드리지 않았다.

---

## 2. 구현 요약

### D1 — **세 자리에 명시적으로**. 공통 조상에 걸지 않았다

`_schedule_release_for(task, dates_before)` 가 **날짜가 실제로 바뀌었을 때만** 검증을 돌린다.
안 바뀌면 저장소를 아예 건드리지 않고 `{0, null}` 을 낸다.

| # | 자리 | 트리거 | 표면 |
|---|---|---|---|
| ① | `update` | `start_date`·`due_date` 를 실은 새 값으로 바꾼 직후 | `PATCH /api/tasks/{id}` · MCP `task_update` |
| ② | `transition` | `open → in_progress` 가 **비어 있던 시작일을 오늘로 채운** 직후 | `POST /api/tasks/{id}/start` · MCP `task_start` |
| ③ | `_apply_proposal` | 제안 payload 가 `due_date` 를 덮어쓴 직후 | `POST /api/tasks/{id}/proposals/{pid}/respond` |

- **`repository.touch()` 에 걸지 않았다** — 날짜와 무관한 변경에도 아홉 번 불린다.
- **검증과 저장이 한 transaction** 이다: 세 자리 모두 조립 층이 명령 하나를 한 session 에 싣고,
  닫기는 그 session 안에서 일어난다.
- **사유는 둘뿐이다.** 날짜를 전부 지우면 `task_dates_cleared`, 그 밖은 `out_of_range`.
  한쪽만 지우는 것은 남은 한쪽을 그 날 하루로 읽으므로 **여전히 `out_of_range`** 다 (K7) —
  셋째 사유가 생기는 경로가 없다.
- **업무 종료는 쓰기가 아니다.** 합의 취소(`_apply_proposal` 의 `cancellation` 갈래)는 `{0, null}` 을 내고
  배정을 닫지 않는다. **상태 변경 아홉 경로에 아무것도 더하지 않았다.**

### K3 — `schedule_release` 를 **어디에 싣고 어디에 안 싣는가**

새 타입 **`TaskDateMutationResult(TaskMutationResult)`** 하나를 더했다 — `schedule_release` 가 붙은 투영이다.
**공유 타입 `TaskMutationResult` 는 건드리지 않았다.** 처음에 거기 `NotRequired` 로 넣어 봤더니
**MCP 도구 16개의 `output_schema` 가 함께 변했다**(`task_list`·`task_get`·`my_task_list` 같은 **읽기**
표면까지). 목록 한 줄이 「배정을 닫았다」를 광고할 이유가 없어 되돌렸다.

| 표면 | `schedule_release` | 왜 |
|---|---|---|
| `PATCH /api/tasks/{task_id}` | **낸다** | D1 ① |
| `POST /api/tasks/{task_id}/start` | **낸다** | D1 ② |
| `POST /api/tasks/{id}/proposals/{pid}/respond` | **낸다** (동의·거절·영수증 전부) | D1 ③ |
| `POST .../block`·`/resume`·`/complete`·`/cancel` | **안 낸다** | 날짜를 바꾸지 않는 표면이다. 같은 operation 을 지나지만 **표면이 약속하는 것**이 다르다 — 기존 계약 그대로 |

결과: **MCP 도구 129개의 스키마가 하나도 바뀌지 않았다** (`tool_count` 129 불변, 드리프트 0건).

### K16 — 역량 문 둘 (DEC-003 증보 6)

- `calendar_tasks` 앞에 `self._require(principal, TASK_READ)`
- `_assignable_task` 앞에 `self._require(principal, TASK_SELF_MANAGE)` — 생성·시각 변경·영수증 셋이 이 문을 지난다

**기존 동작은 바뀌지 않는다**: 구성원(mina)·팀장(jiho) 둘 다 두 역량을 갖고 있어 그대로 통과하는 것을
테스트로 남겼다(`test_the_two_capability_gates_do_not_change_what_a_member_or_a_lead_can_do`).
역량을 뺀 `Principal` 로 부르면 둘 다 `TaskAccessDenied` 다.

---

## 3. 운영 대장 — diff 를 실제로 쟀다

```
docs/unified-operations-inventory.json | 75 insertions(+), 4 deletions(-)   (hunk 5개)
```

| 무엇 | 줄 |
|---|---|
| 새 행 | **3** — `POST /api/tasks/{task_id}/schedules` · `PATCH /api/task-schedules/{schedule_id}` · `GET /api/calendar` (전부 `status: excluded` · `policy: E2` · `target_tools: []`) |
| `http_count` | **1줄** — 156 → 159 |
| `http_signature` | **3줄** — `GET /api/meetings`(인자 증가) · `PATCH /api/tasks/{task_id}`·`POST /api/tasks/{task_id}/start`(응답 타입이 `TaskDateMutationResult` 로) |
| `tool_count` | **불변 129** · 도구 스키마 변경 **0건** |

> **브리프의 「`http_signature` 2줄 이내」보다 한 줄 많다.** 그 한 줄은 K3 이 **기존 두 표면의 응답에**
> 묶음을 더하기 때문에 생긴다 — WP 는 BE-1 이 만든 2줄만 셈에 넣었다. 계약을 바꾼 것이 아니라
> **계약이 이미 말한 것을 대장이 받아 적은 것**이다. 줄일 방법은 응답 타입을 느슨하게(`dict`) 두는
> 것뿐인데 그러면 대장이 실제 계약을 더 적게 말하게 된다.

- **전체 재작성하지 않았다.** `json.load` → 그 항목만 수정 → `indent=2` 로 다시 씀. 나머지는 바이트 동일
  (diff hunk 가 5개뿐인 것이 증거).
- **`acceptance_evidence` 보존 확인** — 변경 전 141건 / 변경 후 **141건**(새 3행은 `excluded` 라 요구되지 않는다).
- `exclusion.reason`·`reconsider_when` 은 WORK-004 작업 5 문구 그대로.
  `alternative` 는 **테스트가 요구하는 필수 항목**인데 WP 가 주지 않아 각 행의 화면 경로를 적었다.

---

## 4. 검증 결과 (수치)

| 명령 | 결과 |
|---|---|
| `make test-unit` | **356 passed / 0 failed** — **`test_operation_inventory` 통과**. 이 Phase 의 관문이 닫혔다 |
| `make test-contract` | **1117 passed / 2 failed** (BE-1 직후 1104 + 신규 13). 실패 둘은 `test_material_worker_recovery`(lease·timeout) — **기존 flaky**. 그 파일들만 직렬로 다시 돌리면 **36 passed** |
| `make test-postgres POSTGRES_TEST_URL=…/ax_test_calendar` | **89 passed / 0 failed** (동시성·제약 회귀 재통과) |
| local-stack preflight | 실행 PostgreSQL 에 같은 SQL 을 돌려 `…|task_checklist_items|task_schedules|meeting_transcripts|…` 를 grep 패턴이 **매치**하는 것 확인 |

**세 자리 각각의 테스트** (`tests/contract/test_task_schedule_release.py`, 13건):

- ① 업무 수정 — 축소 시 `{1, out_of_range}` · 전부 지움 `{2, task_dates_cleared}` ·
  한쪽만 지움 `{1, out_of_range}`(셋째 사유 없음) · 제목만 바꿈 `{0, null}`
- ② 시작 전이 — **`released_count = 0`**. 마감이 지난 업무를 시작해 `start_date > due_date` 를 실제로 만든 뒤에도
  그 안의 배정이 **그대로 산다**(K11). 시작일이 이미 있던 업무도 `{0, null}`
- ③ 제안 동의 — 마감을 당기면 `{1, out_of_range}` · 거절은 `{0, null}` · 제목만 바꾸는 제안도 `{0, null}`
- **되돌려도 복구되지 않는다** — 줄였다 늘리면 `schedules[]` 가 **빈 채로** 돌아오고, 그 날에 **다시 배정하면
  새 `schedule_id` 로 `version: 1`** 이 선다
- `/block`·`/cancel` 응답에 `schedule_release` **키가 없다**

---

## 5. 실제 API 계약 — **FE-1·FE-2 가 이것을 쓴다**

**전부 돌려 본 실물이다.** `ax_demo` 위에 API 를 띄워(127.0.0.1:8124) curl 로 받은 본문이고,
확인 뒤 만든 데모 행은 지웠다(`task_schedules` 0행).

### `GET /api/calendar?from=&to=` → `200` · **한 배열**, `kind` 로 가름

```json
[
  {
    "kind": "task",
    "task_id": "fcc4b3c2-2bac-4155-8470-bfd575432746",
    "title": "BE-2 계약 캡처",
    "state": "open",
    "start_date": "2027-03-01",
    "due_date": "2027-03-05",
    "span_from": "2027-03-01",
    "span_to": "2027-03-05",
    "version": 1,
    "schedules": [
      {
        "schedule_id": "f80eef3a-5278-448c-8627-34b422827881",
        "on_date": "2027-03-03",
        "starts_at": "10:00",
        "ends_at": "11:30",
        "version": 1
      }
    ]
  },
  {
    "kind": "meeting",
    "meeting_id": "1716af53-748e-48b3-8e7a-b694778c5981",
    "title": "BE-2 합본 확인 회의",
    "starts_at": "2027-03-04T01:00:00+00:00",
    "ends_at": "2027-03-04T02:00:00+00:00",
    "location": null,
    "status": "scheduled",
    "viewer_relation": "attendee",
    "created_by": "mina",
    "attendee_count": 1,
    "created_by_display_name": "민아 (구성원)"
  }
]
```

**타입과 함정**

| 필드 | 타입 | FE 가 알아야 할 것 |
|---|---|---|
| `kind` | `'task'` \| `'meeting'` | 한 배열에 섞여 온다. **순서는 업무 전부 → 회의 전부** |
| `span_from`·`span_to` | `string \| null` (ISO 날짜) | **서버가 정규화한 구간.** 기간 없는 업무는 **둘 다 `null`**. `taskSpan()` 을 쓰지 말고 이 값을 띠와 드롭 가드에 **똑같이** 쓴다 (I-2) |
| `start_date`·`due_date` | `string \| null` | **원본 그대로.** 뒤집힌 업무면 `start_date > due_date` 가 실제로 온다 — 그릴 때 쓰지 않는다 |
| `schedules[]` | 배열 | **요청한 기간과 겹치는 살아 있는 배정만.** 기간 밖 배정은 **안 실린다**. 원소에 `task_id` 는 **없다** |
| `state` | `'open'\|'in_progress'\|'blocked'\|'done'\|'cancelled'` | 5종 그대로. **`completion_submitted` 는 `'done'` 으로 투영돼 캘린더에 선다**(§C) — 합본 행에 `derived` 가 없어 승인 대기인지 여기서는 가려지지 않는다 |
| `version` | `number` | **업무** 회차. 날짜 조정(`PATCH /api/tasks`)에 쓴다 |
| 회의 `starts_at`·`ends_at` | ISO datetime **UTC(`+00:00`)** | **날짜 문자열이 아니다.** 사무실 시간대(Asia/Seoul)로 변환해 격자에 놓는다 |
| `created_by_display_name` | `string` | 주최자 이름. 없으면 member id 로 채워진다 |
| 없는 것 | — | `is_active_assignee`(K13) · 회의의 `attendees[]`·`purpose`·`repeat` |

- 끝난 업무(`done`·`cancelled`)는 **애초에 실리지 않는다.**
- **기간으로 업무를 거르지 않는다** — 기간 없는 업무도 행으로 온다(좌측 레일이 R2 를 하려면 필요).
  기간이 거르는 것은 `schedules[]` 뿐이다.
- `from`·`to` **둘 다 필수**. 역전이면 `422`.

### `POST /api/tasks/{task_id}/schedules`

요청: 헤더 `Idempotency-Key` **필수**, 본문 `{"on_date":"YYYY-MM-DD","starts_at":"HH:MM","ends_at":"HH:MM"}`.
**`expected_version` 을 받지 않는다**(보내면 `422` — `extra=forbid`).

```json
// 201 (생성)
{"schedule_id":"f80eef3a-…","task_id":"fcc4b3c2-…","on_date":"2027-03-03","starts_at":"10:00","ends_at":"11:30","version":1}

// 200 (같은 멱등 키 재전송 = 영수증 · 본문이 201 과 동일하고 version 도 그대로)
{"schedule_id":"f80eef3a-…","task_id":"fcc4b3c2-…","on_date":"2027-03-03","starts_at":"10:00","ends_at":"11:30","version":1}

// 409 (다른 키인데 그 날이 이미 참)
{"detail":"이 날에는 이미 시간 배정이 있습니다"}
```

> **상태 코드로 가른다** — `201` 은 새로 생겼고 `200` 은 영수증이다. **본문으로는 구분되지 않는다.**
> 정상 흐름에서 `409` 는 보이지 않는다: 그 날에 배정이 있으면 화면은 `schedules[]` 의 `schedule_id` 로
> 곧바로 `PATCH` 를 부른다.

### `PATCH /api/task-schedules/{schedule_id}`

요청: `{"expected_version": <그 배정의 version>, "starts_at":"HH:MM", "ends_at":"HH:MM"}`.
**`on_date` 를 받지 않는다**(보내면 `422`). `expected_version` **무조건 필수**(빠지면 `422`).

```json
// 200
{"schedule_id":"f80eef3a-…","task_id":"fcc4b3c2-…","on_date":"2027-03-03","starts_at":"14:00","ends_at":"15:30","version":2}

// 409 (낡은 회차)
{"detail":"다른 곳에서 먼저 바뀌었습니다"}
```

### 업무 날짜 수정의 `schedule_release`

```json
// PATCH /api/tasks/{task_id}  (기간을 2027-03-05 → 2027-03-02 로 줄임)  200
{ "task_id":"fcc4b3c2-…", "start_date":"2027-03-01", "due_date":"2027-03-02", "version":2,
  "schedule_release": {"released_count": 1, "reason": "out_of_range"} }

// PATCH /api/tasks/{task_id}  (제목만 바꿈)  200
{"released_count": 0, "reason": null}

// POST /api/tasks/{task_id}/start  200
{"state":"in_progress","start_date":"2027-03-01","due_date":"2027-03-02",
 "schedule_release":{"released_count":0,"reason":null}}
```

`reason` ∈ `"out_of_range"` | `"task_dates_cleared"` | `null`.
**`released_count` 가 0 이면 화면은 아무 말도 하지 않는다.** 문구는 FE 가 만든다 —
서버는 건수와 사유만 낸다. `POST .../proposals/{pid}/respond` 도 같은 칸을 `{task_id, proposal, task_version, schedule_release}` 에 싣는다.

### `GET /api/meetings` — 두 모양

```
GET /api/meetings?from=2027-03-01&to=2027-03-05   → 200, 배열 (구획 없음 · 커서 없음)
   [{meeting_id, title, starts_at, ends_at, location, status, viewer_relation, created_by, attendee_count}]
GET /api/meetings                                  → 200, {upcoming: [...], past: {items, next_cursor}}  (기존 그대로)
```

**기간 갈래에는 `created_by_display_name` 이 없다** — 그 필드는 **합본 조회에만** 있다(K4).

### 에러 — **실제 본문 10종**

| 코드(SPEC) | HTTP | 실제 `detail` |
|---|---|---|
| `TASK_SCHEDULE_OUT_OF_RANGE` | 422 | `"이 업무의 기간(2027-03-01~2027-03-05) 안에만 시간을 배정할 수 있습니다"` — **정규화 구간**이 들어간다 |
| `TASK_SCHEDULE_TASK_UNSCHEDULED` | 422 | `"먼저 업무 기간을 정해 주세요. 기간이 있어야 시간을 배정할 수 있습니다"` |
| `TASK_SCHEDULE_INVALID_RANGE` | 422 | `"종료 시각은 시작 시각보다 뒤여야 합니다"` |
| `TASK_SCHEDULE_TASK_CLOSED` | **409** | `"끝난 업무에는 시간을 배정할 수 없습니다"` |
| `TASK_SCHEDULE_DAY_TAKEN` | **409** | `"이 날에는 이미 시간 배정이 있습니다"` |
| `TASK_SCHEDULE_FORBIDDEN` | **403** | `"내가 맡은 업무에만 시간을 배정할 수 있습니다"` |
| `WORK_NOT_FOUND` | 404 | 업무: `"task was not found"` · 배정: `"task schedule was not found"` |
| `VERSION_CONFLICT` | **409** | `"다른 곳에서 먼저 바뀌었습니다"` |
| `WORK_SCHEDULE_START_AFTER_DUE` | 422 | `"start date cannot be later than the due date"` **(영문 — 기존 `validate_schedule` 문구 그대로)** |
| `CALENDAR_RANGE_REQUIRED` | 422 | 역전: `"조회 기간의 시작이 끝보다 뒤일 수 없습니다"` · 누락: FastAPI 표준 `[{"type":"missing","loc":["query","to"],…}]` |
| `MEETING_RANGE_INCOMPLETE` | 422 | `"회의 기간 조회에는 from 과 to 가 함께 필요합니다"` |

> **에러 본문은 `{"detail": "<문장>"}` 이고 `code` 필드가 없다.** 저장소의 결이 그렇다 — 오류 코드는
> 예외 클래스가 갖고, HTTP 상태가 매핑이며, 본문은 **사람이 읽는 문장**이다. **FE 는 상태 코드 +
> 호출한 명령으로 갈라야 하고, 문구는 FE 가 자기 것을 낸다**(§I 「조용한 거절 0개」).
> 위 문장은 **그대로 화면에 뿌리라고 준 것이 아니라** 무엇이 오는지 알려 주는 것이다.

---

## 6. 미결 · 주의점

1. **대장 `http_signature` 가 3줄 바뀌었다** (브리프 기대치 2줄). 이유는 §3 의 인용 박스. 계약 변경이 아니다.
2. **`WORK_SCHEDULE_START_AFTER_DUE` 문구가 영문**이다(`"start date cannot be later than the due date"`).
   기존 `validate_schedule` 의 것이고 **이 work 가 바꾸지 않았다.** SPEC §4 Case Matrix 가 적은
   한국어 문구(「시작일은 마감일보다 뒤일 수 없습니다」)는 **화면 문구**이므로 FE 가 만든다.
3. **`schedule_release` 는 날짜를 바꾸지 않는 전이 넷에는 없다**(`/block`·`/resume`·`/complete`·`/cancel`).
   FE 가 그 응답에서 이 칸을 읽으면 `undefined` 다.
4. **합본 조회 업무 행에 `derived` 가 없다.** `completion_submitted` 인 업무는 `state: "done"` 으로 서고
   「승인 대기」인지 캘린더 행만으로는 알 수 없다 — 좌측 카드가 그 구분을 내야 하면 상세/목록을 따로 읽어야 한다.
   **BE-1 보고에서 올린 것과 같은 자리**이고 계약을 바꾸지 않았다.
5. **실패한 명령은 멱등 원장에 남지 않는다.** 같은 키로 먼저 `422` 가 났던 요청을 다른 내용으로 다시 보내면
   `409` 가 아니라 **새 생성**이 된다(그 transaction 이 통째로 버려졌으므로). 성공한 키의 재사용만 영수증/충돌로 갈린다.
6. **`ax_demo` 스키마는 BE-1 에서 이미 맞춰 뒀다.** 이번 Phase 는 스키마를 바꾸지 않았다.
7. FE 로 남은 것 — `Phase FE-1`·`FE-2`. 위 §5 가 그 브리프에 그대로 들어가면 된다.
