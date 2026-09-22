# 캘린더 시간 배정 — `task_schedules` 를 세울 때 걸리는 표면 전수조사 (backend, read-only)

- 태스크: `task_9f39aaed8cb9` · dispatch `ctx_fc6a3f4db557`
- 조사 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar` (브랜치 `kknaksss/strong-hajin-calendar`)
- 조사일: 2026-09-20
- **코드는 한 줄도 고치지 않았다.** 증거는 §9.
- 줄 번호는 모두 이 워크트리의 `1b40f83` 시점 기준이다. `backend/` 상대 경로로 적는다.

## 0. 이 리포트를 읽는 법

- 각 절은 **사실(근거) / 해석 / 모르는 것** 으로 갈라져 있다. 「사실」에는 `파일:줄` 이 붙는다.
- 「전부 세라」고 한 4-1·4-2·4-3·4-4 는 **실제로 돌린 검색 명령**을 그대로 적었다. 모두 저장소 루트
  (`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`) 에서 돌린 것이다.
- 설계를 정하지 않았다. 갈리는 자리는 §10 Open Questions 로 남겼다.
- D1~D8 과 **어긋나 보이는 것**은 고치지 않고 §8 에 모았다.

---

## 1. 시안이 요구하는 것 (SSOT 읽기 결과 — 저장 구조가 아니라 「무엇을 할 수 있나」)

### 사실

- 시안은 표 둘을 가정한다: `CAL_TASKS`(날짜 단위) · `CAL_SCHEDULE`(시간 단위).
  `shared/js/work-data.js:4` 주석이 「실제 구현에서는 두 테이블(tasks · schedules) 조회 결과가
  이 꼴로 들어온다」고 쓴다.
- `CAL_SCHEDULE` 한 행은 `kind: 'meeting' | 'task'` 로 갈린다. `kind==='task'` 인 행만 `taskId` 를 갖는다
  (`shared/js/work-data.js:51` — 유일한 예 `s9`).
- **업무 기간 밖에는 배정할 수 없다** — `calendar/js/week.jsx:101-105` `canDrop(day)`:
  `day >= taskFrom(t) && day <= taskTo(t)`. `taskFrom`/`taskTo` 는 `t.from || t.due` · `t.to || t.due`
  (`week.jsx:20-21`) 라서 **기한이 전혀 없는 업무는 시간 배정 자체가 불가**하다(`!taskFrom(t)` → false).
- **같은 업무는 하루에 한 칸** — `calendar/js/calendar.v1.jsx:222-226` `addSlot`:
  `const keep = list.filter((s) => !(s.taskId === taskId && s.day === day));` 로 기존 행을 버리고 새로 붙인다.
  D8 이 말하는 그 동작이 여기 있다.
- 시각 눈금은 **30분**(`week.jsx:9` `WEEK_SNAP = 30`), 드롭 기본 길이는 60분(`week.jsx:212`),
  격자는 0시~24시(`week.jsx:10` `WEEK_SPAN = 24*60`), 블록 최소 높이 30분(`week.jsx:227`).
- 배정 블록의 시각은 세로 드래그로 **30분 단위**로 조정된다(`calendar.v1.jsx:229-233` `resizeSlot`; 눈금은 `week.jsx:85-86`).
  시작은 종료보다 앞, 종료는 시작보다 뒤여야 한다는 것 말고 다른 검사가 없다.
- 시간 배정을 만들어도 **업무의 기간은 그대로다**(`calendar.v1.jsx:221` 주석 「업무의 기간은 그대로 남는다」).
- 좌측 목록은 업무 카드에 배정 시각을 `"{day}일 {start}"` 문자열로 덧붙인다(`calendar.v1.jsx:261`·`:268`).
  → 업무 목록 조회가 **그 업무의 배정 목록**을 함께 내야 한다는 뜻이다.
- 회의는 `place`(장소)·`repeat`(반복) 를 카드 meta 로 쓴다(`calendar.v1.jsx:283`).

### 해석

- `task_schedules` 가 답해야 하는 조회는 최소 둘이다 — ① 기간(주/월) 안의 배정 전부, ② 업무 하나의 배정 전부.
- 시안의 `repeat`(매주 월) 은 **목데이터에만 있는 문자열**이고 백엔드 `meetings` 표에 대응 열이 없다(§5 참고).

### 모르는 것

- 30분 눈금이 **저장 제약**인지 화면 편의인지 시안만으로는 갈리지 않는다. 시안은 `wkClock()`(`week.jsx:17`) 으로
  `HH:MM` 문자열을 만들 뿐이라 30분 아닌 값을 저장할 수 없다고 말하지 않는다.
- 자정을 넘는 배정(23:30–00:30)을 시안이 허용하는지 — `week.jsx` 의 격자는 하루 안에서만 그린다.

---

## 2. 4-1. 새 표 하나를 세울 때 손대는 자리 전부

### 사실 — 이 레포에 마이그레이션 체계는 **없다**

- `backend/migrations/manual/2026-09-17-w2-indexes.sql:8-12` 가 규약의 정본이다:
  > 이 저장소에는 alembic 도 migrations 체계도 없다. `schema_sync`(= `make sync-demo-schema`)는
  > **없는 표를 만들고 없는 컬럼을 더할 뿐, 기존 표에 인덱스를 더하지 않는다**(BASE-002 O-24).
- 같은 파일 `:14-15`:
  > 새 표(`task_proposals` · `work_request_list_entries`)의 인덱스는 여기 없다 —
  > **새 표는 `--sync` 가 인덱스까지 함께 만든다.**
- 실제로 `schema_sync.plan()` 이 그렇게 한다 — `bootstrap/schema_sync.py:27-31`:
  살아 있는 표에 없는 이름이면 `CreateTable` + **그 표의 `table.indexes` 전부**를 `CreateIndex` 로 낸다.
  이미 있는 표에는 `ALTER TABLE ... ADD COLUMN` 만 낸다(`:38`), 인덱스는 손대지 않는다.
- 운영 적용용 판은 별도 파일이다(`2026-09-17-w2-indexes.concurrent.sql`) — `CONCURRENTLY` 라 트랜잭션
  밖에서 **사람이** 돌린다(`:3-9`). 두 판의 정의가 같아야 한다는 것도 그 파일이 못 박는다(`:22`).

### 사실 — `task_schedules` 를 세울 때 **반드시** 닿는 자리

| # | 자리 | 근거 | 무엇을 한다 |
|---|---|---|---|
| 1 | `src/ax_workspace/platform/persistence.py` | `persistence.py:11-12` `Base` · 90개 표가 여기 산다 | `TaskScheduleRecord(Base)` 선언. `__table_args__` 에 인덱스·부분 unique·CHECK |
| 2 | `bootstrap/schema_sync.py` | `:27-31` | **코드 수정 불필요.** 새 표면 자동으로 `CreateTable` + 인덱스를 낸다 |
| 3 | `entrypoints/reset_demo.py` | `:55-66` (`--sync`), `:68` (파괴적 reset) | **코드 수정 불필요.** `make sync-demo-schema` 가 표를 만든다 |
| 4 | `bootstrap/reset.py` | `:11-22` — `Base.metadata.create_all(engine)` | **코드 수정 불필요** |
| 5 | `docs/domain-model.md` | 역할 `rules.md`: 「새 모듈·새 표는 `docs/domain-model.md` 대조표에 한 줄 추가한다」. 선례: `TASK_REFERENCE` 행 (`docs/domain-model.md:110`) | ERD 항목 ↔ 표 ↔ 비고 한 줄 |
| 6 | `bootstrap/application.py` | `:4222-4233` `_tasks()` 가 `TaskApplication` 에 repository 들을 물린다 | 새 repository / application 을 **여기서만** 조립한다 |
| 7 | `platform/work_tasks.py` 또는 새 `platform/task_schedules.py` | `work_tasks.py` 가 `SqlAlchemyTaskRepository` 를 갖는다 | 조회·쓰기 SQL |
| 8 | `modules/work/…` | `modules/work/application.py` · `lifecycle.py` 등 | 도메인 규칙(D1·D5 검증)이 사는 자리 |
| 9 | `entrypoints/http.py` | 156개 라우트 (§4-1 inventory) | 새 엔드포인트 |
| 10 | `entrypoints/mcp.py` + `modules/ax_execution/tool_catalog.py` | `tool_catalog.py:430` 등 | MCP 도구를 낼 경우 |
| 11 | **`docs/unified-operations-inventory.json`** | `tests/architecture/test_operation_inventory.py` (§ 아래) | 새 HTTP·MCP 표면마다 행 추가 + count 갱신 |
| 12 | `backend/tests/contract/` · `tests/unit/` | 역할 `rules.md` TDD | RED 먼저 |

### 사실 — **여기 없던 자리** (이 조사의 성과)

1. **`docs/unified-operations-inventory.json` 은 2.1MB 짜리 캡처 파일이고, 세 테스트가 이것을 drift 로 잡는다.**
   - `tests/architecture/test_operation_inventory.py:119-141` — 실제로 등록된 MCP 도구의 `input_schema`·
     `output_schema`·`annotations` 까지 통째로 비교하고, `tool_count` 도 센다(현재 **129**).
   - `:144-198` — `http.py` 를 **AST 로 파싱해서** 라우트마다
     `http_handler` · `http_application_calls`(handler 가 부르는 `workflow_application.*` 이름 집합, 로컬
     호출까지 재귀로 따라간다) · **`http_signature`(인자 타입 + 반환 타입 문자열)** 를 뽑아 캡처와 비교한다.
     `http_count` 는 현재 **156**.
   - `:201-249` — verified 행은 `http_handler`·`http_application_calls`·**`owning_calls`**·`target_tools`·
     `policy`·`acceptance_evidence` 를 **모두** 가져야 한다. `owning_calls` 는 `_workflow_owner_calls()`
     (`:26-105`) 가 `bootstrap/application.py` 의 `WorkflowApplication` 을 AST 로 걸어 **그 operation 이
     실제로 부르는 소유 호출**을 뽑은 것과 정확히 같아야 한다.
   - `target_tools` 는 `bootstrap/operation_inventory.py:tool_targets_for_http()` 가 `adapter_operation`
     으로 자동 매칭한 결과와 같아야 한다. 라우트와 도구가 **다른 facade 이름**을 지나면
     `HTTP_TOOL_TARGET_OVERRIDES`(`operation_inventory.py:12-82`) 에 한 줄 박아야 한다.
   - → **새 엔드포인트 하나가 inventory json 에 행 하나 + 두 count 증가를 요구한다.** 전체 재작성 금지
     (브리프 §AGENTS.md). 캡처 갱신 스크립트는 레포에서 **찾지 못했다** (아래 「모르는 것」).
2. **`Makefile` 의 `local-stack` preflight 가 표 이름을 하드코딩한다** (`Makefile:170`):
   `to_regclass('durable_jobs')`, `daily_report_generations`, `task_checklist_items`,
   `meeting_transcripts`, `assistant_character_preferences`, `action_material_drafts`, `notifications` …
   이 목록이 스키마가 최신인지 가르는 표지다. `tests/architecture/test_local_stack_targets.py:28-40` 이
   **그 문자열 하나하나를 assert** 한다.
   → `task_schedules` 를 표지에 넣을지는 선택이지만, **넣으면 그 테스트도 같이 고쳐야 한다.**
   넣지 않으면 스키마가 뒤처진 로컬 DB 에서 local-stack 이 통과하고 런타임에 터진다.
3. **실제 PostgreSQL 에서 제약이 서 있는지 세는 통합 테스트 선례가 있다** —
   `tests/integration/postgres/test_task_lifecycle_v2_schema_postgres.py:1-15`:
   > 모델 선언이나 `create_all` 이 성공했다는 사실을 근거로 삼지 않는다 — 살아 있는 PostgreSQL 의
   > `information_schema` · `pg_constraint` · `pg_index` 에 **그 제약이 실제로 서 있고 valid 한지**를 묻고,
   > **잘못된 행이 거절되는 것**을 한 건씩 남긴다. SQLite 선언은 여기서 아무것도 증명하지 않는다.
   → 부분 unique 인덱스를 쓰는 새 표는 이 선례를 따라야 「선언했다」가 아니라 「선다」가 증명된다.
   `make test-postgres` (`POSTGRES_TEST_URL` 필요) 로 돈다.
4. **`tests/architecture/test_architecture.py:67-74`** — `test_application_startup_never_mutates_schema`:
   `Base.metadata.create_all` 을 monkeypatch 로 막고 `create_app()` 을 띄운다. 즉 **새 표를 어디서
   만들든 API startup 경로에 스키마 생성이 끼면 이 테스트가 즉시 깨진다.**
5. **계층 테스트 셋** — 새 모듈을 만들 경우 자동으로 걸린다:
   - `test_architecture.py:139-148` — `modules/*/domain.py`·`application.py` 는 `fastapi`·`mcp`·`sqlalchemy`
     를 import 하면 안 된다.
   - `test_architecture.py:158-162` — `entrypoints/` 는 `ax_workspace.platform` 이라는 **문자열조차**
     들어가면 안 된다.
   - `test_architecture.py:172-194` — `*Application` 생성자를 `platform/`·`entrypoints/` 에서 부르면 안 된다.
     조립은 `bootstrap/application.py` 뿐이다.
   - `tests/architecture/test_test_pyramid.py:11-26` — `PURE_DOMAIN_MODULES` 목록에 든 파일은 순수해야
     한다. 새 순수 도메인 파일(예: `work/schedule.py`)을 만들면 **이 목록에 한 줄 더해야** 그 순수성이 지켜진다.
6. **reset_demo 경로의 정확한 모양** (브리프가 물은 것):
   - 문 하나다 — `python -m ax_workspace.entrypoints.reset_demo`. `Makefile:102-111` 에 세 타겟이
     같은 모듈을 부른다: `reset-demo`(무플래그·파괴적) · `sync-demo-schema`(`--sync`) · `reset-catalog`(`--catalog-only`).
   - `reset_demo.py:47-52` — 안전 장치 셋: `require_safe_demo_database()` 가 **연결 전에** URL 을 본다.
     postgres 는 host 가 `localhost|127.0.0.1|::1` 이고 db 이름이 `^ax_(demo|test)(_[a-z0-9_]+)?$`,
     sqlite 는 `:memory:` 이거나 `^(ax_)?(demo|test)[-_a-z0-9]*\.db$` 일 때만 통과.
   - `reset_demo.py:53-54` — `settings.developer_auth_enabled` 가 아니면 `RuntimeError`.
   - 파괴적 경로는 `bootstrap/reset.py:14-19` — postgres 면 **`DROP SCHEMA public CASCADE` → `CREATE SCHEMA public`**,
     그 밖이면 `drop_all`. 그다음 `create_all` + `seed_catalog`.
   - `--sync` 경로는 `schema_sync.apply()` → `plan()` 의 statement 를 **한 transaction** 에 실행(`schema_sync.py:64-70`).
     `plan()` 이 내는 `manual[]` 은 **실행하지 않고 사람에게 출력**한다(`reset_demo.py:60-61`):
     NOT NULL 인데 `server_default` 가 없는 열(`schema_sync.py:33-41`), 모델에 없는 살아 있는 열(`:44-45`).
   - `_column_spec()`(`schema_sync.py:49-62`) 이 **SQLAlchemy 자신의 `CreateColumn` 컴파일러**를 써서
     `DEFAULT`·`NOT NULL` 을 그대로 싣는다 — 실물에서 안건 52건이 NULL 이 될 뻔한 사고의 대응이라고 주석이 적는다.

### 실제로 돌린 명령 (4-1)

```bash
# 표 개수
grep -c '__tablename__' backend/src/ax_workspace/platform/persistence.py      # -> 90

# 표·제약 목록
grep -n "__tablename__\|^class \|UniqueConstraint\|Index(" \
  backend/src/ax_workspace/platform/persistence.py

# 마이그레이션이 존재하는가
find backend/migrations -type f
# -> manual/2026-09-17-w2-indexes.sql, manual/2026-09-17-w2-indexes.concurrent.sql  (그게 전부)

# 마이그레이션을 언급하는 파일 전부
rg -n 'migration' --glob '!*.lock' -l .
# -> docs/domain-model.md
#    backend/tests/integration/postgres/test_task_lifecycle_v2_schema_postgres.py
#    backend/migrations/manual/2026-09-17-w2-indexes.sql
#    backend/src/ax_workspace/platform/persistence.py

# inventory 규모
python3 -c "import json;d=json.load(open('docs/unified-operations-inventory.json'));\
print(len(d['http']), len(d['current_runtime']['added_operations']),\
d['current_runtime']['tool_count'], d['current_runtime']['http_count'])"
# -> 112 44 129 156
```

### 해석

- **새 표만 놓고 보면 마이그레이션 작업은 사실상 없다** — `--sync` 가 표와 인덱스를 함께 만든다.
  손 `.sql` 이 필요해지는 경우는 **기존 표(`tasks`·`meetings`)에 인덱스나 열을 더할 때**다.
- 비용의 무게중심은 스키마가 아니라 **inventory drift + 계층 테스트 + PostgreSQL 제약 증명** 셋이다.

### 모르는 것

- `docs/unified-operations-inventory.json` 을 **자동 갱신하는 스크립트를 찾지 못했다.**
  찾아본 방법: `rg -n 'unified-operations-inventory' .` (히트는 테스트 3곳과 json 자신뿐),
  `grep -n '^[a-z-]*:' Makefile` 로 타겟 40개 확인 — 캡처용 타겟 없음.
  테스트가 `actual == captured` 로 비교하므로 **실패 메시지의 diff 를 보고 손으로 패치**하는 것이
  현재 유일한 길로 보인다(AGENTS.md 도 「diff 난 항목만 패치」라고 쓴다).
- 「운영 migration(Alembic baseline)과 배포는 별도 gate」(`docs/domain-model.md:96`) 라는 문장의
  그 gate 가 이 저장소 밖 어디인지는 코드에서 확인할 수 없었다.

---

## 3. 4-2. 업무 날짜가 바뀌는 경로 전부 (D1 을 걸 자리)

### 실제로 돌린 명령

```bash
# ① 기존 행의 날짜를 바꾸는 자리
rg -n --no-heading '\btask\.(start_date|due_date)\s*=[^=]' backend/src/

# ② 넓게 — 어떤 객체든 날짜 속성 대입
rg -n --no-heading '\.(start_date|due_date)\s*=[^=]' backend/src/

# ③ 새 행을 세울 때 날짜가 들어오는 자리
rg -n --no-heading '^\s+(start_date|due_date)=' backend/src/ax_workspace/platform/work_tasks.py
rg -n --no-heading -B2 'TaskRecord\(' backend/src/

# ④ 표면(HTTP·MCP)에서 날짜를 받는 자리
rg -n 'start_date|due_date' backend/src/ax_workspace/entrypoints/http.py
rg -n 'start_date|due_date' backend/src/ax_workspace/entrypoints/mcp.py

# ⑤ 검증 함수의 호출자
rg -n 'validate_schedule' backend/src/

# ⑥ 전체 분포
rg -c --no-heading 'start_date|due_date' backend/src/ | sort -t: -k2 -rn   # 270 히트 / 29 파일
```

### 사실 — **이미 선 업무의 날짜를 바꾸는 자리는 셋** (①의 출력 전부)

| # | 자리 | 무엇이 바뀌나 | 진입 표면 |
|---|---|---|---|
| A | `modules/work/application.py:518-520` (`TaskApplication.update`, 정의 `:458`) | `start_date`·`due_date` 둘 다. `validate_schedule(start_date, due_date)` 를 **바로 앞에서** 부른다(`:518`) | `PATCH /api/tasks/{task_id}` (`entrypoints/http.py:1489-1494`) → `bootstrap/application.py:2335-2339` → `TaskApplication.update`. MCP `task_update` (`entrypoints/mcp.py:2016-2032`) 가 **같은 operation** 으로 들어온다 |
| B | `modules/work/application.py:1443` (`TaskApplication.transition`, 정의 `:1392`) | `start_date` 만. 순수 도메인 `modules/work/lifecycle.py:165-170` 이 **`open → in_progress` 이고 `start_date` 가 비어 있을 때 `command.today` 를 넣는다** | `POST /api/tasks/{task_id}/start` (`http.py:2411`), MCP `task_start`, 그리고 `_walk_to` 를 지나는 시드 |
| C | `modules/work/application.py:1679` (`TaskApplication._apply_proposal`, 정의 `:1658`) | `due_date` 만. 제안(`task_proposals.payload`)에 `due_date` 가 있으면 `date.fromisoformat()` 으로 덮어쓴다 | `POST /api/tasks/{task_id}/proposals/{proposal_id}/respond` (`http.py:1772`) — 「조건 변경 제안」에 **동의**할 때 |

②의 출력에는 위 넷 말고 `modules/work/requests.py:591` 하나가 더 있는데, 이것은
`work_requests.due_date`(요청 행)이지 `tasks.due_date` 가 아니다.

### 사실 — **생성 시점에도 날짜가 들어온다** — 다섯 자리 (③의 출력)

전부 `platform/work_tasks.py` 의 `TaskRecord(...)` 생성자다.

| 줄 | 함수 | 진입 |
|---|---|---|
| `work_tasks.py:400-401` | `create_self_task` (정의 `:365`) | `POST /api/tasks` (`http.py:1320`), `POST /api/projects/{project_id}/tasks` (`http.py:1390`), MCP `task_create_self` |
| `work_tasks.py:1318-1319` | `create_request` (정의 `:1276`) | **`work_requests` 행**의 날짜다 — Task 가 아니다 |
| `work_tasks.py:1906-1907` | `create_task_for_request` (정의 `:1869`) | 요청이 만드는 업무 — `start_date=getattr(request, "start_date", None)`, `due_date=request.due_date` 로 **요청 행에서 복사**한다 |
| `work_tasks.py:2298-2299` | `create_unheld_task` (정의 `:2275`) | 아직 아무도 들지 않은 업무 |
| `work_tasks.py:2443-2444` | `create_assigned_task` (정의 `:2413`) | `POST /api/tasks/assign` (`http.py:1446`), MCP `task_assign` |

그 밖에 날짜를 실어 보내는 표면: `POST /api/work-requests` (`http.py:1902`),
`POST /api/work-requests/{id}/resubmit` (`:2003`), `POST /api/work-requests/{id}/amend` (`:2017`),
`POST /api/meetings/{id}/todos/{todo_id}/promote` (`:789`) — 모두 **요청 행**의 날짜를 받고,
그 요청이 수락될 때 `create_task_for_request` 가 Task 로 복사한다.

### 사실 — 검증은 한 함수인데 호출이 **셋뿐**이다

`modules/work/task_values.py:29-31`:

```python
def validate_schedule(start_date: date | None, due_date: date | None) -> None:
    if start_date is not None and due_date is not None and start_date > due_date:
        raise TaskError("start date cannot be later than the due date")
```

호출자(⑤ 출력): `modules/work/application.py:518`(update) · `modules/work/assignments.py:160` ·
`modules/work/task_creation.py:35`. **B(lifecycle) 와 C(제안 동의) 는 부르지 않는다.**

### 해석 — D1 을 한 자리에 걸 수 있는가

- **없다. 최소 세 자리다.** A·B·C 는 서로 다른 계층에 있고 공통 조상이 없다:
  - A 와 C 는 같은 클래스(`TaskApplication`)지만 `update()` 와 `_apply_proposal()` 은 서로를 부르지 않는다.
  - B 는 **순수 도메인**(`lifecycle.py`)이 날짜를 정하고 application 이 옮겨 적는 모양이다. `lifecycle.py` 는
    `tests/architecture/test_test_pyramid.py:22` 가 순수로 못 박은 파일이라 **거기서 DB 를 볼 수 없다.**
    즉 D1 검증은 `application.py:1443` 직후에 걸어야 한다.
- **한 자리로 모으고 싶다면** `self.repository.touch(task)` 가 A·B·C 모두에서 불린다
  (`:522`, `:1456`, `:1665`) — 다만 같은 호출이 날짜와 무관한 자리에도 여섯 번 더 있다(`:1282`,`:1298`,`:1316`,`:1522`,`:1690`,`:1786`) — 다만 `touch` 는 상태 전이·제목 수정 등 **날짜와 무관한 변경에도**
  불리므로, 거기 거는 것은 「날짜가 바뀌었을 때만」을 스스로 판정해야 한다. 이건 설계 선택이라 §10 으로 넘긴다.
- **생성 시점은 D1 대상이 아니다** — 새 업무에는 배정이 없다. 다만 `create_task_for_request` 는
  요청의 날짜를 복사하므로, 요청의 날짜가 바뀐 뒤 수락되는 순서에서는 이미 만들어진 배정이 없다.

### 모르는 것

- `update()` 의 `changes` 딕셔너리는 `TaskEditFields.model_validate(values).changes()` 를 지난다
  (`modules/work/task_commands.py:129`). `clear_start_date`/`clear_due_date` 가 오면 값이 `None` 이 된다
  (`task_commands.py:120-122`). **날짜를 전부 지운 업무의 기존 배정을 어떻게 할지**는 D1~D3 어디에도 없다 → §10.

---

## 4. 4-3. 업무가 `done`·`cancelled` 로 가는 경로 전부 (D5 를 걸 자리)

### 실제로 돌린 명령

```bash
# ① Task 행의 state 를 바꾸는 자리 — 이것이 답이다
rg -n --no-heading '\btask\.state\s*=[^=]' backend/src/

# ② 넓게 — 어떤 객체든 state 대입 (오탐 많음, 교차 확인용)
rg -n --no-heading '\.state\s*=[^=]' backend/src/

# ③ DONE/CANCELLED 상수가 쓰이는 자리 전부
rg -n --no-heading 'TaskState\.(DONE|CANCELLED)' backend/src/

# ④ 시드·배치·관리 스크립트가 직접 쓰는가
rg -n 'TaskRecord|state\s*=|start_date|due_date' \
  backend/src/ax_workspace/bootstrap/{demo_work,seed,scenario,dataset_import,isolated_work}.py
```

### 사실 — `transition_task`(lifecycle) 를 **지나지 않는** 경로가 여덟 개다

①의 출력 9줄 중 `application.py:1442` 하나만 lifecycle 을 지난다. 나머지 여덟:

| # | 자리 | 목표 상태 | 표면 | lifecycle 을 지나나 |
|---|---|---|---|---|
| 1 | `modules/work/application.py:1277` `submit_completion` (정의 `:1247`) | `COMPLETION_SUBMITTED` | `POST /api/tasks/{id}/completion-report` (`http.py:1634`) | **아니오** |
| 2 | `modules/work/application.py:1296` `accept_delivery` (정의 `:1288`) | **`DONE`** | 요청자의 결과 확인 (판단 경로 `action_item_command`) | **아니오** |
| 3 | `modules/work/application.py:1311` `request_delivery_changes` (정의 `:1301`) | `IN_PROGRESS` (되돌림) | 보완 요청 | **아니오** |
| 4 | `modules/work/application.py:1442` `transition` (정의 `:1392`) | 6종 전부 | `POST /api/tasks/{id}/{start,block,resume,complete,cancel}` (`http.py:2411-2433`) | **예 — 유일** |
| 5 | `modules/work/application.py:1518` `reopen` (정의 `:1487`) | `IN_PROGRESS` | `POST /api/tasks/{id}/reopen` (`http.py:1733`) | **아니오** |
| 6 | `modules/work/application.py:1662` `_apply_proposal` (정의 `:1658`) | **`CANCELLED`** (`cancel_reason="cancellation_agreed"`) | `POST /api/tasks/{id}/proposals/{pid}/respond` (`http.py:1772`) | **아니오** |
| 7 | **`platform/work_tasks.py:1855`** `close_request_task` (정의 `:1834`) | **`CANCELLED`** | 요청 거절·철회·합의 취소가 부른다 | **아니오 — 영속 계층** |
| 8 | **`platform/work_tasks.py:2658`** `decide` (정의 `:2595`) | **`CANCELLED`** (`cancel_reason="direct"`) | 직접 배정을 **거절**했고 교체 대상이 없을 때 | **아니오 — 영속 계층** |
| 9 | **`platform/work_tasks.py:2715`** `cancel` (정의 `:2684`) | **`CANCELLED`** | 답 없는 직접 배정을 보낸 사람이 거둘 때 | **아니오 — 영속 계층** |

- 7·8·9 는 `platform/work_tasks.py` 안에 있다. 그 안에서 `TaskActivityRecord` 를 직접 add 하고
  `ActivityLedger(...).record(...)` 를 직접 부른다 (`work_tasks.py:1860-1866`, `:2666-2670`, `:2719-2727`).
  즉 **도메인 규칙을 application 층에 걸면 이 셋은 그 밑으로 빠져나간다.**
- 4(`transition`)는 `lifecycle.transition_task()` 를 부르고(`application.py:1418-1441`),
  `_ALLOWED_TRANSITIONS`(`lifecycle.py:93-104`)가 전이를 가른다.
- 취소 3·6·7·8·9 를 합치면 **`CANCELLED` 로 가는 길이 다섯**이고, `DONE` 으로 가는 길이 **둘**
  (4 의 `TaskState.DONE` 과 2 의 `accept_delivery`)이다.

### 사실 — 시드·배치·관리 스크립트는 **깨끗하다**

- ④의 출력: `bootstrap/` 어디에서도 `TaskRecord` 를 직접 세우거나 `state` 를 직접 대입하지 않는다.
- `bootstrap/scenario.py:278-294` `_walk_to()` 주석이 그 규약을 적는다:
  > 상태는 옮겨 적는 것이 아니라 그 사람이 실제로 옮긴다. 이력도 그렇게 남는다.
  실제로 `application.transition_task(...)` 를 순서대로 부른다(`:290`).
- `bootstrap/demo_work.py:46`·`:60` 도 같은 facade 를 쓴다.
- `bootstrap/dataset_import.py` 의 `state=` 히트(`:206`,`:216`,`:224`,`:237`,`:438`)는 전부
  **구성원 재직 상태**(`employment_state`)·조직 행이고 Task 가 아니다.
- 워커(`entrypoints/*_worker.py`)에서는 `task.state` 대입이 ① 출력에 전혀 없다.

### 해석

- **D5 를 `transition_task` 한 자리에만 걸면 구멍이 다섯 난다** — 2(정상 완료!), 6, 7, 8, 9.
  특히 2(`accept_delivery`)는 **요청 업무의 정상적인 완료 경로**다. 여기를 빠뜨리면
  「요청받아 한 일은 완료돼도 배정이 살아 있다」가 된다.
- 7·8·9 가 영속 계층에 있으므로, D5 를 도메인 규칙으로만 표현하면 닿지 않는다.
  **실행 가능한 선택지 두 가지** (어느 쪽인지는 §10):
  - (가) 다섯 자리 각각에 「배정도 접는다」 호출을 넣는다 — 지금 구조 그대로, 자리가 늘면 또 빠뜨린다.
  - (나) `task_schedules` 를 읽는 **조회 쪽에서** Task 의 현재 상태를 조인해 거른다 — 행은 남고
    화면에 안 선다. 배정을 「접는」 쓰기가 아예 없어지지만, D2 의 소프트 딜리트와 뜻이 섞인다
    (기간 밖으로 나간 것 vs 업무가 끝난 것).

### 모르는 것

- `COMPLETION_SUBMITTED` 가 D5 의 「`done`」에 드는지. §8-2 참조 — **외부 계약에서는 `done` 으로 보인다.**

---

## 5. 4-4. 소프트 딜리트 선례 (D2 가 따를 모양)

### 실제로 돌린 명령

```bash
# ① 종료 시각류 열 전부
rg -n '(removed_at|archived_at|superseded_at|revoked_at|discarded_at|deleted_at|detached_at\
|cancelled_at|closed_at|purged_at|ended_at|retired_at|abandoned_at|withdrawn_at|released_at)' \
  backend/src/ax_workspace/platform/persistence.py

# ② 부분 unique 인덱스 전부
rg -n 'sqlite_where|postgresql_where' backend/src/ax_workspace/platform/persistence.py

# ③ 조회에서 어떻게 걸러지나
rg -n 'include_archived|include_released|released_at.is_\(None\)|removed_at.is_\(None\)' backend/src/
```

### 사실 — 소프트 딜리트 패턴은 **네 종류**다

**(1) `released_at` / `released_by` — 「뗀 시각」. task 의 자식 관계 표가 쓴다.**

| 표 | 선언 | 부분 unique |
|---|---|---|
| `task_predecessors` | `persistence.py:995-1042` | `uq_task_predecessors_active` on (`task_id`,`predecessor_task_id`) **WHERE `released_at IS NULL`** (`:1015-1022`) |
| `task_references` | `persistence.py:1497-1526` | `uq_task_reference_active` on (`task_id`,`referenced_task_id`) **WHERE `released_at IS NULL`** (`:1506-1515`) |

`TaskPredecessorRecord` 의 docstring(`persistence.py:1000-1011`)이 이 레포의 **결**을 그대로 말한다:

> **행을 지우지 않고 닫는다** (`released_at`). 참고 연결 해제가 같은 이유로 같은 모양을 쓴다 —
> 놓아준 것도 거기 있었다는 사실은 이력에 남는다 (§5 보존).
> 데이터베이스가 답하는 것과 application 이 답하는 것을 가른다.
> - **활성 행 유일성**은 부분 unique 가 답한다 … application 검사만으로는 둘 다 「없다」를 보는 틈이 남는다.
> - **자기 자신 금지**는 CHECK 이 답한다 …
> - **순환 금지는 DB 가 못 한다.** … **검사와 저장이 한 transaction** 에 있다.

조회 필터: `platform/work_tasks.py:679-684` —
`references_for(task_id, *, include_released: bool = False)` 가 기본으로
`.where(TaskReferenceRecord.released_at.is_(None))` 를 건다. 단건 조회(`:687-693`)도 같다.
`docs/domain-model.md:110` 이 API 계약으로도 그것을 적는다:
> 해제는 삭제가 아니라 `released_at`·`released_by`를 남겨 과거 snapshot에서 복원된다.

**(2) `state` 문자열 + `archived_at`/`archived_by` — 목록에서 감추기.**

- `task_checklist_items` (`persistence.py:1043-1066`): `state` 는 `active|archived`(`:1055`),
  `archived_by`·`archived_at`(`:1061-1062`). **부분 unique 없음.**
- 쓰기: `work_tasks.py:860-862`. 조회: `work_tasks.py:437-441`
  `checklist_for(task_id, *, include_archived: bool = False)`.
- 이력 조회는 일부러 `include_archived=True` 로 부른다(`work_tasks.py:1003-1004`):
  > History keeps the steps a current screen hides, so an archived one is part of what the Task then was.

**(3) `ended_at` / `superseded_at` + status 문자열 — 「활성은 0 또는 1」.**

- `project_assignments` (`persistence.py:864-894`): `uq_project_assignment_active`
  on (`project_id`,`member_id`) **WHERE `ended_at IS NULL`** (`:872-880`).
  `docs/domain-model.md:39` 가 이 표의 **이행 절차**까지 적어 뒀다 — nullable 종료 열 추가 → backfill →
  기존 무조건 unique 제거 → partial unique 생성, 그리고
  > `sync-demo-schema`는 nullable 컬럼 추가까지만 가능한 개발 helper라 constraint 교체·backfill을 대신하지 않으며…
- `task_assignments` (`persistence.py:1692-1729`): `uq_task_assignments_active` on (`task_id`)
  **WHERE `status = 'active'`** (`:1701-1710`) + `superseded_at`(`:1728`).
  주석(`:1699-1701`): 「application 검사로 낮추지 않는다 — 두 명령이 동시에 들어와도 데이터베이스가 둘째를 거절한다.」
- `access_grants.revoked_at`(`:261`), `auth_sessions.revoked_at`(`:1927`),
  `meeting_attendees.removed_at`(`:480`), `material_extractions.archived_at`/`superseded_at`(`:1296`,`:1315`),
  `action_material_drafts.discarded_at`(`:821`), `employment_periods.ended_at`(`:111`).

**(4) 별도 「감춤」 표 — 행을 지우는 대신 다른 표에 한 줄.**

- `work_request_list_entries` (`persistence.py:1664-1679`). docstring:
  > **행을 지우지 않는다.** 거절·취소·재요청 로그는 그대로 남고, 이 표는 「요청자의 목록에서만 감춘다」는
  > 한 가지 사실만 갖는다. 전역 삭제도 상대방 자료 삭제도 아니다.

### 사실 — 부분 unique 인덱스 선례는 **아홉 개**다 (②의 출력)

| 줄 | 인덱스 | WHERE |
|---|---|---|
| `:659-660` | conversation_turns | `state IN ('pending','running')` |
| `:877-878` | `uq_project_assignment_active` | `ended_at IS NULL` |
| `:905-906` | `uq_tasks_source_work_request` | `source_work_request_id IS NOT NULL` |
| `:1020-1021` | `uq_task_predecessors_active` | `released_at IS NULL` |
| `:1512-1513` | `uq_task_reference_active` | `released_at IS NULL` |
| `:1707-1708` | `uq_task_assignments_active` | `status = 'active'` |
| `:1749-1750` | `uq_task_proposals_pending_kind` | `state = 'pending'` |
| `:1826-1827`, `:1894-1895` | report generations / durable jobs | `state IN ('queued','running')` |

세 가지 술어 모양이 있다 — `<열> IS NULL`(닫힘 표시) · `<열> IS NOT NULL` · `state = '<값>'`.

### 해석 — **무엇을 따르는 것이 이 레포의 결인가**

**`task_predecessors` · `task_references` 의 `released_at` 모양을 따르는 것이 결대로다.** 근거 넷:

1. **자리가 같다.** 둘 다 `tasks.id` 를 FK 로 물고, 업무에 완전히 종속하며, 제목 같은 것을 복사하지 않는
   **task 의 자식 관계 표**다. `task_schedules` 가 D7 에서 정확히 그 모양이다.
2. **뜻이 같다.** D2 의 「배정을 소프트 딜리트」와 `released_at` 의 「놓아준 것도 거기 있었다는 사실은
   이력에 남는다」가 같은 말이다. `archived_at`(체크리스트)은 「사람이 목록에서 치웠다」는 **사람의 의도**이고,
   D2 는 **시스템이 기간 밖이라고 판정한 것**이라 뜻이 다르다.
3. **D8 이 요구하는 유일성 모양이 이미 거기 있다.** 「소프트 딜리트된 행은 유일성에서 빠져야 한다」는
   `uq_task_predecessors_active ... WHERE released_at IS NULL` 과 **글자 그대로 같은 구조**다.
   `task_schedules` 는 (`task_id`, `scheduled_date`) unique WHERE `released_at IS NULL` 이 된다.
4. **행위자를 남기는 열이 짝으로 있다** — `released_by`. D2 는 시스템 판정이라 여기에 무엇을 넣을지가
   갈리지만(§10), **열의 존재 자체는 선례가 요구하는 모양**이다.

`task_assignments` 의 `status='active'` 모양은 **상태값이 넷 이상**일 때 쓴 것이고
(`active|pending|ended|declined|superseded|cancelled`), 배정에 상태 기계가 필요하지 않다면 과하다.

### 모르는 것

- D2 의 소프트 딜리트와 D5 의 「업무가 끝나서 접는 것」을 **같은 열로 표현할지 다른 열로 가를지**.
  선례가 둘 다 있다: `task_assignments` 는 `status` 로 사유를 가르고(`declined`/`superseded`/`cancelled`),
  `task_references` 는 사유를 안 가른다. → §10.

---

## 6. 4-5. 회의 목록 API 의 실제 계약

### 사실 — 라우트

`entrypoints/http.py:665-674`:

```python
@app.get("/api/meetings")
def list_meetings(
    cursor: str | None = None,
    principal: Principal = Depends(developer_principal),
) -> dict[str, object]:
    """예정·지난 두 구획. 「지난」은 20건씩 커서로 잇는다."""
    return app.state.workflow_application.meeting_board(principal, cursor=cursor)
```

→ `bootstrap/application.py:1401-1406` → `modules/meetings/application.py:211-226` `MeetingApplication.board()`.

### 사실 — 응답 모양

```jsonc
{
  "upcoming": [ MeetingRow, ... ],          // 전부. 페이징 없음
  "past": { "items": [ MeetingRow, ... ],   // 20건 (PAST_PAGE_SIZE, application.py:61)
            "next_cursor": "<base64>" | null }
}
```

`MeetingRow` = `_row()` (`modules/meetings/application.py:1610-1621`) — **정확히 9개 필드**:

| 필드 | 값 |
|---|---|
| `meeting_id` | `str(uuid)` |
| `title` | `str | null` — 「바로 시작」 회의는 제목이 없다 (`persistence.py:299`, docstring `:287-291`) |
| `starts_at` | **ISO8601 datetime** (`_iso`) |
| `ends_at` | **ISO8601 datetime** |
| `location` | `str | null` |
| `status` | `str` — 6종 (`meetings.status`, `persistence.py:315`) |
| `viewer_relation` | `"attendee" | "shared"` (`policy.py:195`) |
| `created_by` | `owner_id` |
| `attendee_count` | `int` |

**→ `starts_at`·`ends_at`·`location` 셋 다 나온다.** `title_candidate`·`purpose`·`room_reservation`·
`attendees[]` 는 **나오지 않는다** (그것들은 `_calendar_row`(`:1623-1635`) 와 `_detail`(`:1637-1684`) 에만 있다).

### 사실 — 기간(from~to) 필터는 **없다**

- 라우트 인자는 `cursor` 하나뿐이다(`http.py:666-669`).
- `board()` 는 `meetings_visible_to(...)` 로 **범위 안 회의를 전부 메모리에 올린 뒤** 파이썬에서 가른다
  (`modules/meetings/application.py:216-225`).
- 저장소 질의(`platform/meetings.py:144-170`)에도 시각 조건이 없다.
  `.order_by(MeetingRecord.starts_at, MeetingRecord.id)` 만 있다.
- 구획을 가르는 기준은 `policy.py:269-277` `is_meeting_past()`:
  `relation == "shared" or status in PAST_STATUSES or ends_at <= now`.
- 커서는 **마지막으로 낸 행의 자리를 base64 로 싼 것**이고, 매 호출마다 전체 목록을 다시 만든 뒤
  그 자리를 **선형 탐색**한다(`application.py:1870-1883` `_page`). 즉 DB 커서가 아니다.

### 사실 — 권한 envelope

- **목록 행에는 `viewer_relation` 하나뿐이다.** `can_*` 불리언이 없다.
- 「열 수 있는가」는 **필터로 답한다** — 못 여는 회의는 목록에 아예 서지 않는다
  (`application.py:214-216`; docstring `:213`: 「열 수 없는 회의는 여기 아예 서지 않는다 — 목록도 없는
  것처럼 응답하는 자리다 (§3.2-1)」).
- `can_*` 들은 **상세**(`GET /api/meetings/{id}` → `_detail`)에만 있다(`:1660-1669`):
  `can_edit_info`(bool) · `can_edit_note`(bool) · `can_edit_agendas`(`{memo,ai,final}`) ·
  `can_add_agenda`(`{memo,ai,final}`) · `can_write_memo`(bool). 정의는 `modules/meetings/policy.py:192-205`
  `MeetingView`, 판정은 `project_meeting_view()`(`policy.py:208`) — **순수 도메인**이다.

### 사실 — 캘린더용 투영이 따로 있는데 **HTTP 로 안 나온다**

`modules/meetings/application.py:162-175` `MeetingApplication.list()` docstring:

> **Calendar-safe projection**: a meeting this person may not open contributes only a busy block.
> This stays as it was for the calendar and the MCP tools. The meeting screen reads `board` instead,
> which never mentions a meeting the viewer cannot open at all.

- 못 여는 회의를 `{"kind":"busy","starts_at":…,"ends_at":…}` 로 낸다(`:174`).
- 열 수 있으면 `_calendar_row()` — `_row()` + `kind:"meeting"` + `owner_id` + `attendees[{member_id,display_name}]`.
- **호출자**(`rg -n 'list_meetings|my_meetings' backend/src/`): `bootstrap/application.py:1393`,
  `entrypoints/mcp.py:773-776`(MCP 도구 `meeting_list`, `tool_catalog.py:430`), `bootstrap/scenario.py:248`.
  **`entrypoints/http.py` 에는 없다.**
- `my_meetings()`(`:177-189`)도 마찬가지로 MCP 전용(`mcp.py:778-781`, 도구 `my_meeting_list`,
  `tool_catalog.py:445`)이고, `viewer_relation == "shared"` 인 것을 뺀다(`:188`).

### 해석 — **캘린더가 쓰려면 모자란 것**

1. **기간 필터가 없다.** 9월을 그리려면 지금은 전체를 받아 클라이언트가 걸러야 한다. 「지난」 구획은
   20건 커서라, 과거 달로 이동하려면 **여러 번 왕복**해야 한다. 캘린더의 한 화면 = 한 요청이 안 된다.
2. **`upcoming`/`past` 분류가 캘린더의 축이 아니다.** 캘린더는 「이 주」를 묻는데 API 는 「지났나」로 답한다.
   더욱이 `is_meeting_past()` 는 **공유받은 회의를 무조건 `past` 로 보낸다**(`policy.py:277`) —
   다음 주 회의도 공유받은 것이면 `past` 에 들어간다. 시안대로 캘린더에 그리면 자리가 틀린다.
3. **busy block 투영이 HTTP 에 없다.** 시안의 캘린더는 조직 일정을 보는 화면인데, 현재 HTTP 목록은
   「내가 열 수 있는 회의」만 낸다. `list()` 의 busy block 은 MCP 에만 열려 있다.
4. **행 단위 권한 envelope 이 없다.** 시안은 회의 카드를 읽기 전용으로만 그리므로(`draggable: false`, `calendar.v1.jsx:285`) 당장은 안 막힐 수 있다. 다만 「이 회의를 고칠 수 있나」를 캘린더에서 물으면
   상세를 한 번 더 부르거나 목록 행에 envelope 을 실어야 한다 — 역할 `rules.md` 는
   「envelope 은 server 가 만든다. client 가 kind 로 추론하게 만들지 않는다」고 못 박는다.
5. **`attendees[]`·`purpose` 가 없다.** 시안은 `owner` 를 카드 meta 로 쓴다(`calendar.v1.jsx:283`).
   `created_by` 는 member id 라서 **표시 이름이 없다** — `_calendar_row` 에만 `display_name` 이 있다.
6. **시안의 `repeat`(「매주 월」)에 대응하는 열이 `meetings` 에 없다.**
   `rg -n 'recur|repeat|rrule' backend/src/ax_workspace/platform/persistence.py` → 히트 0.
   반복 회의는 현재 모델에 없는 개념이다.

### 모르는 것

- 캘린더가 회의를 **어느 문으로** 읽을 계획인지(기존 `GET /api/meetings` 확장 vs 새 엔드포인트)는
  이 조사로 정할 일이 아니다 → §10.

---

## 7. 4-6. 가시성 — 캘린더에 무엇이 보이나

### 사실 — 판단의 뿌리는 `Principal` 이다

`modules/organization_access/domain.py:27-67`:

```python
@dataclass
class Principal:
    id: str
    display_name: str
    organization_scope: frozenset[str]   # 어느 조직 단위까지 닿나
    capabilities: frozenset[str]         # 무엇을 할 수 있나 (어디서인지는 모름)
    grants: tuple[Grant, ...] = ()       # 그 역량이 어느 unit·project 에 닿나
```

- `scope_for(capability)` (`:43-49`) · `projects_for(capability)` (`:51-57`) · `allows(cap, unit=, project=)` (`:59-67`).
- docstring(`:33-34`): 「`capabilities` says what this person may do *somewhere*; `grants` says where.
  A check that has a place to name should ask `allows(capability, unit=...)`」.

### 사실 — **업무**: 「내 것」과 「읽을 수 있는 것」이 다른 질문이다

| 조회 | 자리 | 무엇을 내나 |
|---|---|---|
| `my_work()` | `modules/work/application.py:539-544` | **지금 활성 담당으로 들고 있는 것만.** `_list(include_organization=False)` |
| `readable_tasks()` | `:546-558` | 조직 범위 + 프로젝트 범위 + 요청 관계 + CC. 「자료 검색·그래프·권한 판정이 이 답을 쓴다」 |

- 둘 다 `_list()` (`:560-`) 를 지나고, **첫 줄이 가드**다 — `:574` `self._require(principal, TASK_READ)`.
  `_require` 는 `:1733-1736`: 역량이 없으면 `TaskAccessDenied`.
- 세 번째 길(요청 관계, 정책 V-21)은 `WORK_REQUEST_READ` 역량이 있을 때만 열린다(`:585-589`)
  — 그리고 **그 업무 아래 전부**를 깊이 제한 없이 따라간다(`:592-601`, `work_tasks.py:641-654`
  `descendant_ids_of`).
- `my_work()` 의 기본 질의는 `work_tasks.py:1072-1076` `tasks_for(owner_id)` →
  `_held_by(owner_id)` + `state NOT IN (done, cancelled)` (`include_closed=False` 일 때).
- **한 자리에서만 답한다는 규약이 명문화돼 있다** — `application.py:1047-1058` `may_read_task()`:
  > 이 사람이 그 업무를 열 수 있는가 — **한 자리에서만 답한다.**
  > `readable_task_ids()` 와 이 답이 같은 규칙에서 나와야 한다. 예전에는 갈라져 있었다: … **요청자가
  > 상세는 여는데 그 업무의 자료는 못 여는** 모양이 성립했다.
- HTTP: `GET /api/my-work` (`http.py:658-663`) · `GET /api/tasks` (`:1885-1893`, `list_tasks`).

### 사실 — **회의**: 축이 둘이고 조직 범위는 셋째 축이 **아니다**

`modules/meetings/application.py:1478-1484` `_can_read_detail()` docstring:

> 회의를 여는 사람은 그 회의의 참석자다. 공유가 유일한 예외다 (SPEC §3.2-1·2 · §10-1).
> 축은 둘뿐이다 — **조직 범위로 남의 회의를 여는 셋째 축은 두지 않는다. 대표라도 참석하거나 공유받지
> 않은 회의는 없는 것처럼 응답한다.** 캘린더의 시간 덩어리는 회의를 여는 것이 아니므로 `list`가 따로 판정한다.

- 캘린더 전용 판정은 따로다 — `:1486-1493` `_can_read_calendar_detail()`:
  > 전체 조회 권한(`meeting.read.private`)이 **조직 범위 안에서만** 닿는 자리는 여기 하나로 남긴다 —
  > 회의 화면의 열람 경계(§3.2)와 캘린더의 투영은 다른 물음이다.
- 저장소 질의 둘:
  - `platform/meetings.py:133-142` `meetings_in_organizations(organization_ids)` — `list()` 가 쓴다.
    조직 범위 **전부**.
  - `:144-170` `meetings_visible_to(organization_ids, member_id)` — `board()`·`my_meetings()`·
    `readable_rows()` 가 쓴다. `OR` 넷: 참석자 행(`removed_at IS NULL`) · 소유자 · 조직 범위 ·
    유효한 공유 관계(`resource_relationships`, `valid_from <= now < valid_until`).
- 판정은 전부 순수 도메인 `modules/meetings/policy.py` 의 `project_meeting_view()` 한 함수에서 나온다
  (`application.py:1509-` `_view_plan` 이 그것을 부른다).

### 해석 — 캘린더가 **반드시 통과해야 하는 가드**

1. **업무 쪽**: 새 조회는 `TaskApplication._require(principal, TASK_READ)` 를 지나야 하고,
   행 집합은 `my_work`/`readable_tasks` 중 **하나를 재사용**해야 한다. 새 질의를 직접 쓰면
   `may_read_task()` 가 못 박은 「한 자리에서만 답한다」가 깨진다.
   `platform/work_tasks.py` 에 `tasks_held_by_members`(`:1078-1089`)·`tasks_in_projects`(`:1091-1098`)
   같은 조각이 이미 있고, `tasks_held_by_members` docstring 이
   「Used only for an organization-wide read, **never to act on them**」이라고 못 박는다.
2. **회의 쪽**: 캘린더는 `_can_read_calendar_detail`(조직 범위 + `meeting.read.private`)을 쓰는
   축이고, 회의 화면은 `_can_read_detail`(참석·공유)을 쓴다. **둘을 섞으면 안 된다** —
   코드가 일부러 두 함수로 갈라 놓았다.
3. **배정 쪽(새로 만들 것)**: `task_schedules` 는 D5 에 따라 업무에 완전히 종속하므로
   **자기 가시성 규칙을 갖지 않는 것**이 결대로다 — 업무를 읽을 수 있으면 그 배정도 읽을 수 있다.
   `task_references` 가 같은 모양이다(`docs/domain-model.md:110`:
   「**연결은 권한을 주지 않는다** — 매 조회마다 대상 Task를 읽을 수 있는지 다시 확인하고…」).

### 사실 — 캘린더는 「내 것」인가 「조직」인가

- **시안은 답하지 않는다.** `calendar.v1.jsx` 는 사이드바 사용자 하나(`유하람님`)로 그리고,
  좌측 목록은 `CAL_TASKS` 전부를 그대로 쓴다 — 목데이터에는 `group: 'sent'`(내가 남에게 보낸 것)도
  섞여 있다(`work-data.js:30-33`).
- **백엔드는 두 답을 다 갖고 있다** — 업무는 `my_work` vs `readable_tasks`,
  회의는 `board`(참석·공유) vs `list`(조직 범위 + busy block).
→ 조합이 네 가지라 §10 으로 남긴다.

---

## 8. D1~D8 과 어긋나 보이는 것 (고치지 않고 적는다)

### 8-1. D5 의 「`transition_task` 하나」 전제가 사실이 아니다

§4 참조. `tasks.state` 를 `DONE`/`CANCELLED` 로 옮기는 자리가 lifecycle 밖에 **다섯** 있고,
그중 셋이 **영속 계층**(`platform/work_tasks.py`)이다. 가장 무거운 것은
`accept_delivery`(`application.py:1296`) — **요청 업무의 정상 완료 경로**가 lifecycle 을 안 지난다.

### 8-2. D4 의 「`TaskState` 6종이 정본」이 **API 계약에서는 5종**이다

- 내부 enum 은 6종(`modules/work/lifecycle.py:20-26`).
- 그런데 `modules/work/application.py:2218` `_external_state()` 가
  `completion_submitted` → **`done`** 으로 접어서 내보낸다. docstring(`:2210-2216`):
  > 계약은 그 사실을 **`state=done` + `derived.approval=awaiting_review`** 로 말한다.
  > **enum 자체를 없애지 않는다** — 제출 가드와 승인 가드가 그 내부 값을 읽고 있고, 정리는 후속이다.
- 같은 docstring 이 `blocked` 도 「계약에 없지만 이 work 는 그 값을 발행하지도 없애지도 않는다」고 적는다.
- **D5 에 직결된다**: 「업무가 `done` 으로 가면 배정도 접는다」에서 `done` 이
  (가) 내부 `TaskState.DONE` 인지 (나) 외부 계약의 `done`(= `DONE` + `COMPLETION_SUBMITTED`) 인지가
  갈린다. (나)라면 `submit_completion`(`:1277`) 도 D5 의 자리가 되고,
  **`request_delivery_changes`(`:1311`)가 되돌리는 경우**를 D3(복구하지 않는다)과 함께 생각해야 한다.

### 8-3. D1 의 「기간이 바뀌면」에 **상태 전이가 기간을 바꾸는 경우**가 빠져 있다

`modules/work/lifecycle.py:165-170` — `open → in_progress` 이고 `start_date` 가 비어 있으면
`command.today` 를 넣는다. 즉 **「시작」 버튼 하나가 업무 기간을 만든다.**
D1 을 「날짜를 바꾸는 명령」에만 걸면 이 경로가 새고, 하필 **기간이 없다가 생기는** 경우라
「기간 밖」 판정이 처음으로 의미를 갖는 순간이다.

### 8-4. D1 이 전제하는 「기간」이 없을 수 있다

- `tasks.start_date`·`due_date` 는 둘 다 nullable(`persistence.py:918-919`).
- 표면이 **비우는 것**을 명시적으로 지원한다 — `TaskUpdateInput.clear_start_date`·`clear_due_date`
  (`modules/work/task_commands.py:109-110`), `changes()` 가 `None` 으로 접는다(`:120-122`).
- 시안은 기간 없는 업무에 배정을 **못 만들게** 한다(`week.jsx:103` `if (!t || !taskFrom(t)) return false`).
- → **기간을 지운 업무의 기존 배정**을 D1~D3 이 말하지 않는다.

### 8-5. `due_date` 를 바꾸는 한 경로가 `validate_schedule` 을 지나지 않는다

`_apply_proposal`(`application.py:1679`)은 `task.due_date` 를 덮어쓰면서 `validate_schedule` 을 부르지
않는다(§3 ⑤). 그래서 **`due_date < start_date` 인 업무가 성립할 수 있다.**
D1 의 「기간 밖」 판정은 `start_date <= d <= due_date` 를 전제하는데, 이 경우 구간이 비어
**그 업무의 모든 배정이 기간 밖**이 된다. 고치지 않고 보고한다.

### 8-6. D6 의 「`meetings`(그대로)」가 캘린더 요구와 어긋난다

§6 해석 1·2·6 — 기간 필터 없음, `upcoming`/`past` 축이 캘린더 축과 다름(공유 회의가 항상 `past`),
반복(`repeat`) 개념 없음. 「표를 그대로 둔다」는 지켜지지만 **조회를 그대로 둘 수는 없다.**

### 8-7. D7 의 「담당자는 담지 않는다 — 조인으로 끌어온다」가 조회 한 번을 추가한다

시안 좌측 카드가 배정 시각을 업무 카드에 붙인다(`calendar.v1.jsx:261`·`:268`). D7 대로면 그 조인은
`tasks` × `task_schedules` 이고, 「담당자」는 `task_assignments` 까지 3단 조인이다
(`my_work` 가 이미 `_held_by` 로 그 조인을 한다 — `work_tasks.py:1072-1076`). 모순은 아니지만
**배정 조회가 `my_work` 의 투영을 재사용해야 하는 이유**다.

---

## 9. 검증 — 아무것도 고치지 않았다

```
$ git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short
$ echo "[exit=$?]"
[exit=0]
```

출력이 **비어 있다.** (브랜치 `kknaksss/strong-hajin-calendar`, HEAD `1b40f83`)
테스트는 돌리지 않았다 — 브리프 §7 대로 고친 것이 없어 돌릴 이유가 없다.
쓴 파일은 이 리포트 하나뿐이다.

---

## 10. Open Questions — 정하지 못한 것 (임의로 정하지 않았다)

| # | 질문 | 선택지와 대가 |
|---|---|---|
| Q1 | **D5 의 「`done`」은 내부 6종의 `DONE` 인가, 외부 계약의 `done`(= `DONE` + `COMPLETION_SUBMITTED`)인가?** | (가) 내부 `DONE` 만 — 자리가 적다. 대신 「완료 보고 냈고 승인 대기」인 업무의 배정이 캘린더에 계속 선다. (나) 외부 `done` — 화면과 일치한다. 대신 `request_delivery_changes`(`:1311`)가 되돌리는 경우가 생기고, D3(되돌려도 복구 안 함)과 부딪힌다: 보완 요청 한 번에 배정이 영구히 사라진다. §8-2 |
| Q2 | **D5 를 「쓰기(배정을 접는다)」로 걸 것인가 「읽기(조회에서 거른다)」로 걸 것인가?** | (가) 쓰기 — 다섯 자리(§4 의 2·6·7·8·9)에 각각 건다. 그중 셋은 `platform/work_tasks.py` 안이라 계층이 뒤집힌다. 새 취소 경로가 생기면 또 빠뜨린다. (나) 읽기 — 조회에서 `tasks.state` 를 조인해 거른다. 한 자리로 끝나지만 D2(기간 밖)와 D5(업무 종료)가 **다른 메커니즘**이 되어, 「왜 안 보이나」의 답이 둘이 된다 |
| Q3 | **D1 검증을 A·B·C 세 자리에 각각 걸 것인가, `repository.touch(task)` 같은 공통 지점에 걸 것인가?** | 공통 지점은 셋 다 지나지만(§3 해석) 날짜와 무관한 변경에도 불린다 — 「날짜가 바뀌었나」를 스스로 판정해야 하고, 그 판정이 틀리면 조용히 안 돈다. 세 자리에 거는 쪽은 명시적이지만 §8-3 처럼 **새 경로가 생기면 빠뜨린다** |
| Q4 | **기간을 전부 지운 업무(`start_date`·`due_date` 둘 다 `null`)의 기존 배정은?** | (가) 전부 소프트 딜리트 — 시안의 `canDrop` 과 일관(기간 없으면 배정 불가). (나) 그대로 둔다 — 기간이 없으니 「기간 밖」도 없다는 해석. D2 의 문언은 「바뀐 기간 밖으로 나간 배정」이라 빈 기간을 말하지 않는다. §8-4 |
| Q5 | **D2 의 소프트 딜리트 열에 `released_by`(누가/무엇이 닫았나)를 둘 것인가?** | 선례(`task_predecessors`·`task_references`)는 `released_by` 를 짝으로 둔다. 다만 D1 의 닫기는 **시스템 판정**이라 member id 가 없다. (가) 기간을 바꾼 그 사람의 id (나) nullable 로 두고 비운다 (다) `released_reason` 을 따로 둔다 |
| Q6 | **D2(기간 밖)와 D5(업무 종료)를 같은 열로 표현할 것인가?** | (가) 한 열(`released_at`) — 단순하다. 왜 닫혔는지는 모른다. (나) `released_at` + `released_reason`(`out_of_range`/`task_closed`) — 선례는 `task_assignments` 가 `status` 로 사유를 가르는 쪽이고, `task_references` 는 안 가르는 쪽이다. §5 모르는 것 |
| Q7 | **캘린더가 회의를 어느 문으로 읽는가?** | (가) `GET /api/meetings` 에 `from`/`to` 쿼리를 더한다 — 기존 라우트의 `http_signature` 가 바뀌므로 inventory 행을 고쳐야 한다(§2 성과 1). `upcoming`/`past` 축은 그대로라 캘린더가 다시 갈라야 한다. (나) 새 라우트 — inventory 행 + count 증가. `MeetingApplication.list()`(busy block 투영)를 HTTP 로 처음 여는 일이 된다 |
| Q8 | **캘린더의 가시성 축은 「내 것」인가 「조직」인가?** (업무·회의 각각) | 업무: `my_work`(활성 담당만) vs `readable_tasks`(조직·프로젝트·요청 관계). 회의: `board`(참석·공유) vs `list`(조직 범위 + 못 여는 것은 busy block). 조합 넷. 시안은 답하지 않는다(§7 마지막). 조직 축을 고르면 **타인의 업무 배정이 내 캘린더에 선다** — 그러면 D7 의 「담당자는 조인으로」가 표시 요구가 된다 |
| Q9 | **시각 저장 타입.** `meetings` 는 `starts_at`/`ends_at` 가 `DateTime(timezone=True)` 이다(`persistence.py:314-315`). D7 은 「날짜 · 시작시각 · 종료시각」 셋으로 나누라고 한다 | (가) `Date` + `Time` + `Time` — D7 문언 그대로. 업무 기간(`Date`)과 같은 축이라 「기간 밖」 판정이 단순한 날짜 비교가 된다. 자정 넘는 배정이 불가능하다. (나) `Date` + `DateTime`×2 — 회의와 같은 모양이지만 날짜가 중복 저장된다. **이 조사는 정하지 않았다** |
| Q10 | **30분 눈금이 저장 제약인가?** | 시안은 30분 단위로만 만든다(`week.jsx:9`·`:85-86`·`:94-98`). CHECK 제약으로 못 박을지, 화면 편의로 둘지. §1 모르는 것 |
| Q11 | **`task_schedules` 를 `local-stack` preflight 표지에 넣을 것인가?** | 넣으면 `Makefile:170` + `tests/architecture/test_local_stack_targets.py:28-40` 을 같이 고친다. 안 넣으면 스키마가 뒤처진 로컬에서 local-stack 이 통과하고 런타임에 터진다. §2 성과 2 |
| Q12 | **`docs/unified-operations-inventory.json` 갱신 방법.** 자동 갱신 스크립트를 찾지 못했다(§2 모르는 것). 테스트 실패 diff 를 손으로 패치하는 것이 맞는지 확인이 필요하다 | — |

---

## 11. 요약 — 다음 판의 spec·WP 가 알아야 할 것 다섯

1. **스키마 작업은 거의 없다.** `persistence.py` 에 `TaskScheduleRecord` 한 클래스를 더하면
   `make sync-demo-schema` 가 표와 인덱스를 함께 만든다. 손 `.sql` 은 **기존 표에 인덱스를 더할 때만** 필요하다.
2. **비용은 `docs/unified-operations-inventory.json` 에 있다.** 새 엔드포인트 하나가 `http_signature`·
   `owning_calls`·`target_tools`·`policy`·`acceptance_evidence` 를 갖춘 행 하나와 두 count 갱신을 요구하고,
   세 개의 architecture 테스트가 AST 수준으로 그것을 강제한다.
3. **D1 은 세 자리다** — `update`(application.py:518-520) · `transition`(`:1443`, 실제 결정은 순수
   `lifecycle.py:165-170`) · `_apply_proposal`(`:1679`). 공통 조상이 없다.
4. **D5 는 다섯 자리다** — `transition_task` 하나가 아니다. 셋(`work_tasks.py:1855`,`:2658`,`:2715`)은
   **영속 계층**이고, 하나(`accept_delivery`, `application.py:1296`)는 **요청 업무의 정상 완료 경로**다.
5. **D2 가 따를 모양은 `released_at`/`released_by` + 부분 unique `WHERE released_at IS NULL` 이다** —
   `task_predecessors`(`persistence.py:1015-1022`)·`task_references`(`:1506-1515`)가 같은 자리의 같은 뜻으로
   이미 쓰고 있고, D8 이 요구하는 유일성 모양과 글자 그대로 같다.
