# 리뷰 리포트 — strong-hajin-calendar / Phase BE-1 코드 검수 (2026-09-21)

## 판정: **PASS**

**BE-2 로 넘어가도 된다.**

검수 네 판이 닫은 **열 자리가 코드에서 전부 지켜졌다.** 특히 코디가 짚은 **K12 는 호출 순서**라
코드를 열어야 아는 자리인데, `claim` → (같은 키면 **영수증 반환**) → 아니면 `create_schedule`
(그 안에 `409`) 로 **영수증이 409 보다 확실히 앞선다.**

**Phase 경계가 깨끗하다** — D1 세 자리(`update`·`transition`·`_apply_proposal`)를 **한 줄도
건드리지 않았고**, `schedule_release`·운영 대장·`Makefile`·local-stack 표지에 손대지 않았다.
BE-2 를 당겨 하지 않았다.

**부분 unique 증명 넷이 각각 한 건씩** 살아 있는 PostgreSQL 에 남았고, 「선언했다」를 근거로 쓴
자리가 없다. 오히려 **선행 점검이 실제 drift 를 찾아냈다.**

**조용히 통과하는 자리를 찾지 못했다.** 기존 테스트가 하나도 약화되지 않았고(수정된 테스트 파일은
`test_test_pyramid.py` **한 줄 등재**뿐), 새 코드에 빈 단언·폴백·삼킨 `except` 가 없다.

남은 것은 **WARN 하나** — 새 조회가 sibling 들이 전부 지나는 capability 문을 안 지난다.
**SPEC 을 어긴 것은 아니라서**(SPEC `:1105` 이 「로그인 구성원」이라고 적었다) FAIL 로 세지 않는다.

---

## 검수 범위

`git status --short` · `git diff` 로 확정했다 — **수정 13 · 신규 5, 전부 `backend/`.**

| 신규 | 무엇 |
|---|---|
| `modules/work/schedule.py` | 순수 도메인 — 기간 네 경우 · 기간 밖 판정 · 닫기 사유 |
| `platform/task_schedules.py` | 배정 조회·쓰기 |
| `tests/unit/test_task_schedule_span.py` | 네 경우 단위 |
| `tests/contract/test_task_schedules.py` | 계약 (35 함수) |
| `tests/integration/postgres/test_task_schedules_postgres.py` | 제약 실물 증명 |

**테스트는 돌리지 않았다** — 지시대로 읽기만 했다. 코드도 한 줄 고치지 않았다.
코디가 이미 판정한 둘(`VERSION_CONFLICT` 409 · `COMPLETION_SUBMITTED` 투영 → K15)과
`test_operation_inventory` 의 대장 drift 는 **지적에 넣지 않았다.**

---

## ① allowed_paths — **지켰다**

18개 전부 `backend/` 아래다. `frontend/`·`para/`·`orchestration/` **0건**. 코디 확인과 일치한다.

---

## ② Phase 경계 — **BE-2 도 FE 도 당겨 하지 않았다**

`git diff -U0` 의 hunk 머리를 세어 확인했다 — `modules/work/application.py` 의 변경은
**import · Protocol(`:143`) · 생성자(`:202`·`:205`) · 새 블록(`:564`) · 말미 헬퍼(`:2458`)** 뿐이다.

| BE-2 의 것 | 손댔나 |
|---|---|
| D1 세 자리 (`update:518-520` · `transition:1443` · `_apply_proposal:1679`) | **아니다** — 세 함수가 diff 에 없다 |
| `schedule_release{released_count, reason}` | **아니다** — `src/` 에 0건. 유일한 언급이 `tests/contract/test_task_schedules.py:10` 의 「**Phase BE-2 의 몫이라 여기 없다**」 |
| `docs/unified-operations-inventory.json` | **아니다** — `git status` 에 없다 |
| `Makefile:170` · `test_local_stack_targets.py` | **아니다** |
| `docs/domain-model.md` | **아니다** |
| FE | **아니다** |

`task_schedules.py:103` `release()` 와 `:67` `active_for()` 는 **선언만 되고 BE-1 에서 안 쓰인다** —
BE-2 의 D1 이 쓸 자리다. Protocol 을 미리 세운 것이지 **경계를 넘은 것이 아니다.**

---

## ③ 검수 네 판이 닫은 열 자리 — **코드에서 전부 지켜졌다**

### K12 — **영수증이 409 보다 먼저다.** 순서를 코드에서 확인했다 ★

`modules/work/creation_commands.py:202-262` `create_task_schedule` 의 실행 순서:

1. `:238` `key = require_idempotency_key(...)` · `fingerprint = ...`
2. `:239` **`attempt = self._ledger.claim(actor, CREATE_TASK_SCHEDULE_COMMAND, key, fingerprint)`**
3. `:240` **`if attempt is None:`** → `return self._schedule_receipt(...), False`
   — **여기서 반환한다. `create_schedule` 을 부르지 않는다.**
4. 그 아래에서만 `self._tasks.create_schedule(...)` 를 부르고, `409 TaskScheduleDayTaken` 은
   **그 안**(`modules/work/application.py:612`)에서 난다.

**따라서 같은 키의 재전송은 409 검사에 도달하지 않는다.** 표면이 그것을 `200` 으로 낸다
(`http.py` `response.status_code = 201 if created else 200`).
계약 테스트 `test_task_schedules.py:113` 이 그대로 증명한다 — 같은 키 두 번 → `201` then **`200`**,
`again.json() == created.json()`.

**영수증도 권한을 다시 검사한다** (K-2 계승) — `_schedule_receipt` → `schedule_receipt` →
`_assignable_task`(`application.py:571`).

### 나머지 아홉

| 자리 | 코드 | 확인 |
|---|---|---|
| **K10** `POST` 가 회차를 안 받나 · 그 날이 차면 409 | `task_commands.py` `TaskScheduleCreateInput` 에 `expected_version` **없음** + `extra="forbid"` · `application.py:611-613` `active_on` → `TaskScheduleDayTaken` | **✔** |
| **K8** 회차가 배정의 것인가 | `application.py:632` `if schedule.version != expected_version` · `task_schedules.py:98` `schedule.version += 1`. **업무 `version` 을 건드리는 줄이 없다** | **✔** |
| **K7·K11** 네 경우가 한 함수 · 뒤집힘이 `[min,max]` | `schedule.py:40-60` `task_span` **한 함수**. `:58-59` `if start_date > due_date: return TaskSpan(due_date, start_date)` | **✔** |
| **K14** span 이 그 함수의 출력인가 | `application.py:666` `span = task_span(task.start_date, task.due_date)` → `:673-674` `"span_from"/"span_to": _span_end(span, ...)`. **따로 계산하는 자리가 없다** | **✔** |
| **K5** 판정이 활성 담당 관계인가 | `application.py:578` `self.repository.task(task_id, str(principal.id), lock=lock)` → `work_tasks.py:1064` `_held_by(owner_id)`, docstring 「**only while they hold an active TaskAssignment**」. **capability 로 판정하는 줄이 없다** | **✔** |
| **K6** 403 / 404 | `application.py:579-582` — `TaskNotFound` 를 잡아 `may_read_task` 면 `TaskScheduleForbidden`(→`TaskAccessDenied`→**403**), 아니면 그대로 **404** | **✔** |
| **K13** `is_active_assignee` 를 안 싣나 | `task_results.py` `CalendarTaskRow` 에 **없음** · `application.py:667-677` 행 조립에 **없음**. 테스트 `:353` `assert "is_active_assignee" not in task_row` | **✔** |
| **§C** `COMPLETION_SUBMITTED` 를 남기나 | `application.py:664` `tasks_for(include_closed=False)` → `work_tasks.py:1073-1075` 가 거르는 것은 **`[DONE, CANCELLED]` 둘뿐**. 테스트 `:377` | **✔** |
| **K2** 기간이 오면 구획·커서 없음 / 없으면 기존 그대로 | `meetings/application.py:240` `window = _day_window(...)` → `:243-251` 기간 갈래는 **한 배열**(`_page` 안 탐) · `:252-263` 은 **기존 코드 그대로**. 테스트 `:425`·`:438` | **✔** |

**Case Matrix 의 상태 코드도 전수 확인했다** — `TaskScheduleForbidden(TaskAccessDenied)`→403 ·
`TaskClosed`/`DayTaken`/`VersionConflict` 는 `http.py` 409 튜플에 **명시적으로** 들어가 일반 `TaskError`
분기(422)보다 먼저 잡히고 · `OutOfRange`/`TaskUnscheduled`/`InvalidRange`/`CalendarRangeInvalid` 는
`TaskError`→**422** · `MeetingRangeIncomplete(MeetingError)`→**422** · `TaskNotFound`→**404**.
**SPEC §4 Case Matrix 와 전부 맞는다.**

`OUT_OF_RANGE` 문구도 계약대로다 — `application.py:606-609` 가 **`span.span_from`~`span.span_to`**
(정규화 구간)를 적는다. raw 날짜가 아니다.

---

## ④ `meetings_visible_to` 소비처 셋 — **둘이 안 바뀐다. 증명도 있다**

- `platform/meetings.py:145-151` — `overlapping` 이 **keyword-only 이고 기본 `None`** 이다.
  `:177-181` 이 `if overlapping is not None:` 일 때만 조건을 더한다.
- 소비처 셋(`meetings/application.py:180` `my_meetings` · `:198` `readable_rows` · `:218` `board`)
  중 **인자를 넘기는 것은 `board` 하나**다. 나머지 둘의 질의는 **글자 그대로 그대로**다.
- **불변을 증명하는 테스트가 있다** — `test_task_schedules.py:460`
  「the range argument does not reach the other two readers of the same query」.
  좁은 기간 조회는 near 하나만 내는데 `my_meetings` 와 `readable_rows` 는 **near·far 둘 다** 본다고
  단언한다. WORK 검수에서 WARN-1 로 낸 자리가 **그대로 닫혔다.**
- `_is_past` · `my_meetings` 본문은 diff 에 **없다** ✔

---

## ⑤ 부분 unique 증명 넷 — **각각 한 건씩 있다. 「선언했다」로 지나간 자리 없음**

`tests/integration/postgres/test_task_schedules_postgres.py`:

| # | 요구 | 테스트 | 무엇으로 |
|---|---|---|---|
| ① | 있고 valid | `:69` | `information_schema.tables` + `pg_index.indisvalid` + `pg_get_indexdef` 에 `UNIQUE`·`task_id`·`on_date` |
| ② | 술어가 「닫히지 않은 행만」 | `:93` | 정의 문자열에 `WHERE` · **`released_at IS NULL`** |
| ③ | 살아 있는 중복 거절 | `:104` | 같은 (업무,날) 두 번째 행 → `IntegrityError`. **다른 날은 안 막힌다**는 대조까지 |
| ④ | 닫힌 날 재배정 | `:139` | 닫고 다시 → `201`, `schedule_id` 가 다르고, 행 2 중 **살아 있는 것 1**, 그리고 **합본 조회에 닫힌 것이 안 실린다** |

**덤으로 CHECK 증명 하나 더** — `:174` `ends_at < starts_at` 행이 `IntegrityError` 로 거절된다.

**「선언했다」를 근거로 쓴 자리가 없다.** 모듈 docstring `:3-6` 이 「모델 선언이나 `create_all`
성공을 근거로 삼지 않는다」·「SQLite 는 여기와 같은 모양으로 답하지 않는다」를 먼저 적는다.

**선행 점검(WP BE-1 작업 1)이 기록됐고, 실제 drift 를 찾았다** — docstring `:10-14`:
실행 PG 의 부분 unique 가 **여덟**(모델 아홉), `task_predecessors` 표 자체가 없었다(표 88 / 모델 90).
**「ORM 선언과 살아 있는 스키마는 같지 않았다」** — 이 파일이 존재하는 이유를 실물로 증명했다.

---

## ⑥ 조용히 통과하는 자리 — **찾지 못했다**

- **빈 단언·`pass`·`assert True`·`skip`·`xfail`** — 새 소스·새 테스트에 **0건**(grep).
- **삼킨 `except`** — 새 코드에 `except Exception` **0건**. 유일한 `except` 는
  `bootstrap/application.py` `create_task_schedule` 의 `except IntegrityError` 인데
  **삼키지 않는다**: 영수증이면 반환, 그 날이 실제로 찼으면 `409 TaskScheduleDayTaken`,
  **둘 다 아니면 `raise`** 로 다시 올린다. 부분 unique 경합을 사람 말로 바꾸는 자리다.
- **폴백으로 지나간 곳** — 새 모듈에 `or None`·`.get(` 기본값이 없다.
  `creation_commands.py` 의 그 패턴들은 전부 **기존 줄**이다.
- **개명으로 지나간 곳** — 없다. 새 이름 `task_schedules`·`TaskScheduleRecord`·`schedule.py` 가
  기존 것과 충돌하지 않는다.
- **테스트가 계약을 실제로 밟는가** — 표본을 열어 확인했다. 특히 K11 테스트(`:182`)는
  **진짜 `POST /api/tasks/{id}/start` 를 태워** `start_date > due_date` 를 만들고
  (`assert detail["start_date"] > detail["due_date"]`), 그 위에서 정규화 구간을 단언한다.
  **목으로 흉내 낸 것이 아니다.**
- `schedules[]` 원소 모양도 **집합 동등**으로 박혔다(`:352`) — 필드가 늘거나 줄면 깨진다.

---

## ⑦ 기존 실패와 새 실패의 분리 — **기존 테스트가 하나도 약화되지 않았다**

`git status --short backend/tests` 가 내는 것은 넷뿐이다 —
**수정은 `test_test_pyramid.py` 하나이고 그 내용은 `"work/schedule.py"` 한 줄 등재**다.
나머지 셋은 신규다. **삭제·skip·단언 약화가 0건**이라는 뜻이고, 이것이 워커의 「무관」 분리를
문서 밖에서 뒷받침한다.

`test_operation_inventory` 1건 실패는 코디가 확인한 대로 **의도된 대장 drift**(BE-2)다 — 지적에서 뺐다.

---

## WARN — 구현 중에 닫아도 되는 것

### WARN-1 → **Phase BE-2 브리프** (또는 코디 판단)

새 읽기·쓰기가 **capability 문을 안 지난다.**

- `modules/work/application.py:664` `calendar_tasks` 는 `self.repository.tasks_for(...)` 를
  **직접** 부른다. 같은 행 집합을 쓰는 `my_work` 는 `_list` 를 거치고 **그 첫 줄이
  `self._require(principal, TASK_READ)`** 다. `application.py` 안에서 `TASK_READ` 를 요구하는
  자리가 **열둘**인데 새 조회만 그 문을 안 지난다.
- 쓰기 쪽 `_assignable_task`(`:571`)도 `_require(principal, TASK_SELF_MANAGE)` 를 부르지 않는다.
  기존 업무 수정 경로(`:491`)는 부른다.
- `be-survey-report.md` §7 해석 1 이 「새 조회는 **`_require(principal, TASK_READ)` 를 지나야 하고**,
  행 집합은 `my_work`/`readable_tasks` 중 하나를 **재사용**해야 한다」로 **둘**을 요구했는데
  **행 집합 재사용만** 지켜졌다.

**FAIL 이 아닌 이유 — SPEC 을 어기지 않았다.** SPEC-004 §5 권한 표 `:1105` 가
「**캘린더 조회 | 로그인 구성원.** 행 집합은 `my_work` + `board`」라고 적었다. 구현이 그대로다.
쓰기 쪽도 K5 가 「판정은 **활성 담당 관계**이고 봉투가 아니다」라고 못 박았고 구현이 그대로다.
**실질 영향도 지금은 없다** — `task.read`·`task.self_manage` 가 `_MEMBER_CAPABILITIES`·
`_LEAD_CAPABILITIES` 양쪽에 다 들어 있어 그 문을 못 지나는 역할이 **현재 없다**
(`modules/organization_access/catalog.py:77-100`).

**그래도 남기는 이유** — 역량 문은 「누가 이 기능 자체를 쓰는가」이고 관계 검사는 「그중 이 행을
만질 수 있는가」다. **둘은 대체재가 아니라 겹겹**이고, 새 표면만 한 겹이 얇다. 나중에 역량을
빼는 역할이 생기면 그때 조용히 새는 자리가 된다.

**브리프에 실을 한 줄**: 「`calendar_tasks` 에 `self._require(principal, TASK_READ)` 를,
배정 쓰기에 `TASK_SELF_MANAGE` 를 더할지 정한다. **더해도 K5 는 안 깨진다** — 판정은 여전히
담당 관계이고 역량은 그 앞의 문일 뿐이다. 안 더하기로 하면 **그 사실을 SPEC §5 권한 표 옆에
한 줄로 남긴다**(「캘린더 조회는 역량 문을 두지 않는다 — 행 집합이 이미 `my_work` 다」).」

---

## 확인한 것 (근거)

- **①** `git status --short` 18건 전수 — `backend/` 밖 0건.
- **②** `git diff -U0` hunk 머리로 `update`·`transition`·`_apply_proposal` 무변경 확인 ·
  `schedule_release` src 0건 · 대장/Makefile/local-stack 무변경.
- **③** 열 자리를 **각각 코드 줄로** 확인했다. K12 는 `creation_commands.py:238-247` 의
  실행 순서를 따라 읽어 **영수증이 `create_schedule` 앞에서 반환되는 것**을 확인했다.
  Case Matrix 상태 코드 10종의 매핑도 `_runtime_error` 분기 순서로 전수 확인했다.
- **④** `meetings_visible_to` 소비처 셋을 `grep` 으로 세고, 선택적 인자임과 불변 테스트(`:460`)를 확인했다.
- **⑤** postgres 증명 넷 + CHECK 하나를 각각 읽었다. 선행 점검 기록도 확인했다.
- **⑥** 빈 단언·삼킴·폴백·개명을 grep + 표본 열람으로 훑었다. **없다.**
  테스트가 실제 경로를 밟는지 K11·K12·K13·item4 네 건을 본문까지 읽어 확인했다.
- **⑦** `git status backend/tests` — 수정된 테스트가 **한 파일 한 줄**뿐임을 확인했다.
- **테스트를 돌리지 않았다** (지시). **코드를 한 줄도 고치지 않았다.** 산출물은 이 리포트 하나.

---

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
 M backend/src/ax_workspace/bootstrap/application.py
 M backend/src/ax_workspace/entrypoints/http.py
 M backend/src/ax_workspace/modules/meetings/application.py
 M backend/src/ax_workspace/modules/meetings/domain.py
 M backend/src/ax_workspace/modules/work/application.py
 M backend/src/ax_workspace/modules/work/creation.py
 M backend/src/ax_workspace/modules/work/creation_commands.py
 M backend/src/ax_workspace/modules/work/errors.py
 M backend/src/ax_workspace/modules/work/task_commands.py
 M backend/src/ax_workspace/modules/work/task_results.py
 M backend/src/ax_workspace/platform/meetings.py
 M backend/src/ax_workspace/platform/persistence.py
 M backend/tests/architecture/test_test_pyramid.py
?? backend/src/ax_workspace/modules/work/schedule.py
?? backend/src/ax_workspace/platform/task_schedules.py
?? backend/tests/contract/test_task_schedules.py
?? backend/tests/integration/postgres/test_task_schedules_postgres.py
?? backend/tests/unit/test_task_schedule_span.py
```
