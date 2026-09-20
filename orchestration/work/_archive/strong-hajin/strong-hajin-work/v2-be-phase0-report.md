# WORK-002 Phase 0 — 읽기 전용 관측 결과 (backend)

- 작성: `@sc-ax-be` / 2026-09-17
- 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`, 브랜치 `kknaksss/strong-hajin-work`
- 범위: **Phase 0 만.** 코드·DB·테스트·빌드 변경 0건. 실행한 것은 `git` 조회 · `grep`/`cat` · `psql`
  `BEGIN TRANSACTION READ ONLY` SELECT 뿐이다. Phase 1 이후는 이 보고서에서 다루지 않는다.

## 상태: done (관측만) — **단, U-1·U-2·U-6·F-5 는 「못 했다」에 가깝다.** 아래 §2 가 이유다.

---

## 1. 기준선 — W1 미커밋 상태 (했다)

| 항목 | 값 |
|---|---|
| HEAD | `8973791982228f9b5400c2bcaba7e1a9bdda97d7` — manifest 의 `head` 와 일치 |
| manifest 82 파일 sha256 | **82/82 일치. 누락 0, 불일치 0** |
| 워킹트리 | 추적 변경 80 + untracked 15 = 95 항목. 브리프 스냅샷과 같다 |
| 새 diff | **없다.** 다른 세션이 W1 을 건드린 흔적 없음 (U-4 닫힘) |

---

## 2. 실행 DB — **관측 못 했다. 스키마도 데이터도 없다** ⚠

프로젝트 설정으로 식별한 실행 DB:

- `Makefile:1` `DATABASE_URL ?= postgresql+psycopg://ax:ax@localhost:54329/ax_demo`
- 컨테이너 `strong-hajin-work-postgres-1` (postgres:16.6, `0.0.0.0:54329->5432`, up 29h, healthy),
  볼륨 `strong-hajin-work_ax_demo_postgres` — **이 워크트리 자신의 compose 프로젝트**다. 공유·운영 DB 아님.

| DB | public 테이블 수 | 크기 |
|---|---|---|
| **`ax_demo` (실행 DB)** | **0** | 7484 kB (빈 template 크기) |
| `ax_test` | 0 | 7484 kB |
| `ax_test_acceptance` | 0 | 7484 kB |
| `ax_test_w1` | 86 | 65 MB |

**`ax_demo` 에는 표가 하나도 없다.** 그래서 U-1(스키마 대조)·U-2(`assigned` 문자열)·U-6(예외 행)·
F-5(중복)를 **실행 DB 에서는 셀 수 없었다.** 브리프대로 DB 생성·리셋·DDL·스택 재시작은 하지 않았다.

> **SQLite 로 대신하지 않았다**(P-7). 아래 §3 은 `ax_test_w1` 관측이고, 그것이 무엇을 증명하고
> 무엇을 증명하지 못하는지 §4 에 적었다.

### 같이 본 것 — 기본 DATABASE_URL 이 남의 DB 를 가리킨다 ⚠

`bootstrap/settings.py:137-138` 의 기본값은 `postgresql+psycopg://ax:ax@localhost:**5432**/ax_demo` 다.
이 기기의 5432 는 **다른 프로젝트**(`task-management-local-db-1`, postgres:16-alpine, up 8d)가 물고 있다.
`DATABASE_URL` 없이 백엔드를 띄우면 남의 postgres 로 간다. Makefile 경로(54329)로만 뜨면 문제가 없고,
Phase 1 이후 격리 DB 를 세울 때 **env 를 명시적으로 넘기는 것이 전제**다.

---

## 3. 스키마·인덱스 관측 (`ax_test_w1`, READ ONLY)

`ax_test_w1` 은 W1 세션이 남긴 격리 테스트 DB다. 86 표, `members` 6행,
**`tasks`·`work_requests`·`task_assignments`·`action_items` 는 전부 0행.**

### 3-1. 컬럼 — ORM 과 **차이 0**

| 표 | 실제 컬럼 수 | ORM(`platform/persistence.py`) | 차이 |
|---|---|---|---|
| `tasks` | 27 | `TaskRecord` (`:897-948`) | 없음 |
| `work_requests` | 19 | `WorkRequestRecord` (`:1511-1544`) | 없음 |
| `task_assignments` | 15 | `TaskAssignmentRecord` (`:1558-1594`) | 없음 |

### 3-2. 인덱스 11개 — 전부 `indisvalid=t`, `indisready=t`

| 표 | 인덱스 | 정의 |
|---|---|---|
| `tasks` | **`uq_tasks_source_work_request`** | `UNIQUE btree(source_work_request_id) WHERE (source_work_request_id IS NOT NULL)` — **실재·valid** |
| `tasks` | `tasks_pkey` · `tasks_causation_key_key` · `ix_tasks_parent_task_id` · `ix_tasks_project_id` | — |
| `task_assignments` | **`uq_task_assignments_active`** | `UNIQUE btree(task_id) WHERE ((status)::text = 'active'::text)` — **실재·valid** |
| `task_assignments` | `task_assignments_pkey` · `ix_task_assignments_task_id` · `ix_task_assignments_assignee_status` | — |
| `work_requests` | `work_requests_pkey` · `work_requests_causation_key_key` | **`requester_id`·`assignee_id`·`state` 인덱스가 없다** |

두 부분 유일 인덱스의 predicate 를 `pg_index.indpred` 로 직접 읽었고 위 표가 그 원문이다.

### 3-3. 제약 — FK 25개 전부 `convalidated=true`. **CHECK 제약은 0개**

`tasks.state` · `work_requests.state` · `task_assignments.status` 에 **DB 차원의 값 제약이 없다.**
어떤 문자열이든 들어갈 수 있다 — `blocked`·`completion_submitted`·`assigned` 정리는 애플리케이션 몫이다.
`work_requests.requester_id`/`assignee_id`/`promoted_by_member_id` 는 의도대로 FK 가 없다.

---

## 4. 집계 SELECT — 전부 0건. **그러나 0건 추정 금지: 근거가 없는 0이다**

> **정정(코디 지적 반영, 2026-09-17).** 초판의 U-6 SQL 은 **요청 수락**(`work_request.acceptance`) 축을
> 보고 있었다. U-6 이 묻는 것은 **완료 승인**이다 — 둘은 다른 판단이고 다른 표 행이다.
> 아래는 `accept_delivery` → `record_delivery_decision` 경로로 다시 유도해 **실행·검증한** 쿼리다.

`ax_test_w1` 에서 READ ONLY 로 돌린 결과:

| 항목 | 결과 |
|---|---|
| **F-5 중복** `SELECT source_work_request_id,count(*) FROM tasks WHERE source_work_request_id IS NOT NULL GROUP BY 1 HAVING count(*)>1` | **0 그룹** |
| **U-6 예외 행** (아래 SQL) | **0 행** |
| **U-2 `assigned`** — `work_requests.state` 히스토그램 | **행 자체가 0 — 집계 불가** |
| 활성 담당 중복 — `task_assignments status='active'` GROUP BY task_id HAVING >1 | **0** |
| 참고: `decision_items(kind='task.delivery.review')` · `subjects(subject_type='task_delivery')` · `review_decisions` 전체 | **각 0** |

### U-6 정본 SQL — 완료 승인 축

```sql
SELECT count(*)
FROM tasks t
LEFT JOIN decision_items di
       ON di.kind = 'task.delivery.review'
      AND di.context_type = 'task'
      AND di.context_id = t.id::text
LEFT JOIN submissions s  ON s.decision_item_id = di.id
LEFT JOIN review_decisions rd
       ON rd.submission_id = s.id AND rd.decision = 'accept'
WHERE t.source_work_request_id IS NOT NULL
  AND t.state = 'done'
  AND rd.id IS NULL;
```

**유도 근거 (코드 경로)**

| 단계 | 코드 |
|---|---|
| U-6 모집단 = 완료 승인이 필요한 업무 | `requires_completion_review()`(`modules/work/application.py:513-515`) ⟺ `source_work_request_id IS NOT NULL` |
| 완료 보고가 delivery 라운드를 연다 | `submit_completion()`(`:517-552`) → `open_delivery_round()`(`platform/work_tasks.py:548-600`) |
| 그 라운드의 주제·판단 항목 | `subjects.subject_type='task_delivery'`(`:553-555`) · `decision_items.kind='task.delivery.review'`(`DELIVERY_KIND`, `:511`), `context_type='task'` · `context_id=str(task.id)` · `effect_identity='task.delivery.accept:<task_id>'`(`:558-567`) |
| 승인 행 | `accept_delivery()`(`application.py:554-565`) → `record_delivery_decision()`(`work_tasks.py:615-639`) 가 `ReviewDecisionRecord(submission_id=…, decision='accept')` 를 남긴다 |

> `decision_items.context_id` 는 `String(100)` 이므로 **`t.id::text` 캐스트가 필요하다.**
> 위 SQL 은 실제 스키마에 대해 READ ONLY 로 **실행해 통과시킨 것**이고, 구문상 실데이터에 그대로 쓸 수 있다.
> **다만 「예외 0건」의 근거로는 쓸 수 없다** — 아래가 이유다.

### 이 0 이 무엇을 뜻하지 않는가

**「예외가 없다」가 아니라 「셀 대상이 없다」다.**
`tasks`·`work_requests`·`task_assignments` 가 0행이고, delivery 축(`decision_items`·`subjects`·
`review_decisions`)도 전부 0행이다. `ax_test_w1` 은 `create_all` 로 만들어진 격리 DB라
**인덱스가 처음부터 다 있다.** 리뷰 F-5 가 지적한 위험(인덱스 없이 오래 산 DB 에 중복이 쌓였을 가능성)은
**이 관측으로 배제되지 않는다.** 배제하려면 실데이터가 있는 DB 가 있어야 하는데, 이 기기에는 없다.

### 비-0 이 나오면 무슨 뜻인가 (Phase 1 판독 기준)

현재 코드에서는 `transition_task()` 가 `target is DONE and requires_completion_review` 를
**거부한다**(`modules/work/lifecycle.py:81-83`). 즉 요청에서 난 업무가 `done` 에 이르는 경로는
`accept_delivery()` **하나뿐이고, 그 경로는 항상 `accept` 판단 행을 남긴다.**
따라서 실데이터에서 위 SQL 이 **0 이 아니면 그것은 현재 코드의 구멍이 아니라 이 가드 이전의 과거 데이터**이며,
**사용자 결정으로 올릴 대상**이다(옛 OQ-205).

### 참고 — 요청 **수락** 축 (U-6 아님, 혼동 방지용으로 남긴다)

요청 수락은 `requests.accept()`(`modules/work/requests.py:325`) → `record_decision()`(`work_tasks.py:1039-1064`)이
남기며, 연결은 `work_requests.subject_id` → `decision_items(kind='work_request.acceptance')`
(`:1015-1022`) → `submissions.decision_item_id`(`:1024-1030`) → `review_decisions.submission_id` 다.
**초판이 U-6 으로 잘못 쓴 경로가 이것이다.** 필요하면 별개 점검으로 쓰되 U-6 으로 쓰지 않는다.

## 5. 자료 읽기 권한 표면 (U-5) — 코드로 확인. **두 갈래가 실재한다**

판정이 **두 가족**으로 갈려 있고, 둘은 서로 다른 답을 낸다.

**A 가족 — `TaskApplication.get()` 경유. 요청 관계 읽기가 통한다**
`get()`(`modules/work/application.py:351-361`)이 실패하면 `_related_view()`(`:363-378`)로 떨어진다.

| 표면 | 관문 |
|---|---|
| `GET /api/tasks/{id}` | `get()` |
| `GET /api/tasks/{id}/history` · `/history/diff` | `TaskApplication._readable()`(`:761-763`) = `get()` |
| 상세의 `parent`·`children` | `_may_read()`(`:453-458`) = `get()` |
| 그래프 단건(`graph_neighbors` 등) | `_SessionGraphSource.readable_task()`(`bootstrap/application.py:679-683`) = `get()` |

**B 가족 — `readable_tasks()` = `_list()` 경유. 요청 관계 길이 아예 없다**
`_list()`(`application.py:303-349`)는 **자기가 든 것 + 조직 범위 + 참여 프로젝트** 셋뿐이다.

| 표면 | 관문 |
|---|---|
| `GET /api/tasks` · my_work | `_list()` |
| `GET /api/tasks/{id}/materials` (목록) | `materials._readable()`(`:290-297`) → `may_read_task()`(`bootstrap/application.py:658-660`) → `readable_task_ids()` → `_list()` |
| `GET /api/tasks/{id}/materials/{mid}/content` (다운로드) | 같은 `_readable()` (`materials.py:245`) |
| `GET /api/materials/search` · `GET /api/materials/{id}` (메타·미리보기) | `material_search.search()`(`:43-58`) → `SessionMaterialOwners.sources()`(`bootstrap/material_sources.py:57-59`) → `readable_tasks()` |
| 본문 추출·미리보기 | 같은 `sources()` 가 낸 후보에만 붙는다 |
| 그래프 목록·검색 | `_SessionGraphSource.readable_tasks()`(`:669-677`) → `_list()` |
| MCP `task_materials_list` · `open_task_material` · `material_search` · `material_metadata` · `task_list` | 같은 application 경유 → B |

> **결론**: WP 의 진단이 코드와 맞다. **task 축 자료 표면(목록·본문·다운로드·검색·미리보기)은 전부 B 가족**이고,
> 상세·이력만 A 다. 지금도 「요청자가 상세는 여는데 그 업무의 자료는 못 연다」가 성립한다.
> `work_request` 축 첨부(`GET /api/work-requests/{id}/attachments/{aid}/content`)는
> `requests.list(principal)` 로 따로 판정되므로(`material_sources.py:74-89`) 이 갈래에 걸리지 않는다.
>
> **Phase 4 함정 하나**: `_readable` 이라는 **같은 이름의 메서드가 두 클래스에 있고 서로 다른 관문**이다 —
> `TaskApplication._readable`(= A) 과 `TaskMaterialApplication._readable`(= B). grep 으로 고치면 섞인다.

---

## 6. 입구 전수 — 브리프 목록이 아니라 현재 코드를 직접 세었다

| 레지스트리 | 실측 | 근거 |
|---|---|---|
| HTTP 라우트 | **140** (업무·요청·배정·자료·판단 축 **75**) | `entrypoints/http.py` 데코레이터 |
| AX/MCP 도구 (`TOOL_CATALOG`) | **120** | `modules/ax_execution/tool_catalog.py` `ToolDefinition` |
| 위임 확인 대상 (`DELEGATED_ACTION_CAPABILITIES`) | **88** | `entrypoints/mcp.py:139-227` |
| `docs/unified-operations-inventory.json` `current_runtime` | `http_count 140` · `tool_count 120` | **실측과 일치 — drift 없다** |

### 과거 스펙 관측과 어긋난 지점 (전부 이번에 직접 확인)

1. **레지스트리가 둘이다.** WP 는 AX 도구를 `task.create_self`·`task.assign`·`work_request.create` 로 적었지만,
   `TOOL_CATALOG` 의 실제 id 는 **snake** — `task_create_self`(`:535`) · `task_assign`(`:447`) ·
   `work_request_create`(`:637`). 점 표기는 `DELEGATED_ACTION_CAPABILITIES` 의 **키**다(다른 물건).
   **Phase 6 은 두 레지스트리를 다 만져야 한다.**
2. **읽기 도구 이름도 다르다.** WP 의 `task_subtasks`·`task_material_list` → 실제는
   **`task_subtask_list`·`task_materials_list`**.
3. **`withdraw` — WP 진단이 정확하다.** HTTP 라우트 0, `TOOL_CATALOG` 0, 위임 map 0.
   **유일한 입구가 판단함 명령**(`platform/action_center.py:259-260`)이다.
4. **`resubmit` 은 반쪽이다.** HTTP `POST /api/work-requests/{id}/resubmit`(`http.py:1780`)는 있고
   어댑터 `resubmit_work_request`(`mcp.py:300`)도 있지만, **`TOOL_CATALOG` 에 묶인 도구가 없다** —
   MCP/AX 로는 안 열린다. 표면 일치(K-10)를 Phase 6 에서 판정할 때 이 칸이 비어 있다.
5. **AX 도구 설명문이 v1 을 못박고 있다** — 이번 work 가 뒤집는 문장이 그대로 들어 있다:
   - `work_request_create`(`:639`): *"The Task is created with the request and enters the recipient's work at once — **there is no acceptance step**."*
   - `task_assign`(`:449`): *"The Task enters the assignee's work at once — **there is no acceptance step**."*

   **Phase 6 의 실제 작업 항목이다.** 문구를 안 고치면 AX 가 계속 v1 을 안내한다.

---

## 7. 다음 구현용 실행 환경 (확인만)

| 항목 | 값 |
|---|---|
| Node | **v20.20.0 활성** (nvm 에 20.18.3 / 20.19.0 / 20.20.0). Node 25 문제 재현 조건 아님 — **FE 테스트 그대로 가능** |
| npm | 10.8.2 |
| uv | 0.9.28 · `requires-python >=3.12` |
| PostgreSQL | postgres:16.6, **127.0.0.1:54329** (compose `strong-hajin-work-postgres-1`) |
| 격리 DB 후보 | `ax_test`(0표) · `ax_test_acceptance`(0표) · `ax_test_w1`(86표) — Makefile `POSTGRES_TEST_URL` 은 `…:54329/ax_test` |
| Make 타겟 | `test` `test-unit` `test-contract` `test-scale` `test-release` `test-postgres` `frontend-test` `verify` `postgres-up` `sync-demo-schema` `reset-demo` `local-stack` 확인 |

**브리프 지시대로 테스트·빌드는 0회 실행했다.** WP Phase 0 의 「변경 전 테스트 4종 기록」 항목은
이번 발주에서 명시적으로 제외되었으므로 **미수행**이다 — Phase 1 발주에서 격리 DB 준비와 함께 가야 한다.

---

## 8. Phase 1 착수 전 조건 (BE 판단)

1. **실행/격리 DB 가 없다.** `ax_demo` 0표, `ax_test` 0표. Phase 1 의 `make sync-demo-schema` 격리 적용과
   `make test-postgres` 는 **DB 를 먼저 세워야** 돌아간다. Phase 0 은 파괴적 명령이 금지라 세우지 않았다 —
   **Phase 1 발주가 `reset-demo`/`sync-demo-schema` 실행 권한을 명시해야 한다.**
2. **F-5 의 위험은 여전히 열려 있다.** 이 기기에 데이터가 있는 DB 가 없어 중복 유무를 판정할 수 없다.
   §4 의 SELECT 두 벌은 **운영/실데이터 DB 에 접근 가능해진 시점에 그대로 다시 돌려야** 하고,
   `CREATE INDEX CONCURRENTLY` 를 운영에 걸기 전 **Pre-deploy 게이트로 남겨야 한다.**
3. `DATABASE_URL` 을 항상 명시할 것 — 기본값 5432 는 남의 postgres 다(§2).

## 9. 사용자 결정이 필요한 데이터 예외

**없다 — 「예외 0건」이어서가 아니라 판정할 데이터가 없어서다.**
U-6/F-5 를 근거로 사용자에게 올릴 것은 지금 시점에 없고, **실데이터 DB 가 생기는 시점에 다시 센 뒤에 판단한다.**
「예외 0건 확인」으로 §6 인수조건(`:951`)을 닫으면 **거짓이 된다.**

## 10. 이 Phase 에서 하지 않은 것

코드·테스트·마이그레이션 작성 0 · DB 쓰기/DDL/리셋 0 · 테스트·빌드 실행 0 ·
commit/push/PR/stash/reset/checkout 0 · Phase 1 이후 단계 읽기·구현 0 · 문서 리포 쓰기 0.
쓴 파일은 이 보고서 하나다.
