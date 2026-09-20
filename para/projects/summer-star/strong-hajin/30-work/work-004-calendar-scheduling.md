---
type: work
id: WORK-004
title: "W4 — 캘린더 시간 배정: task_schedules 와 3분할 캘린더 화면"
status: todo
product: strong-hajin
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-09-21
updated_at: 2026-09-21
tags:
  - product/strong-hajin
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-003-calendar|BASE-003]]"
  decisions:
    - "[[decision-003-calendar|DEC-003]]"
  specs:
    - "[[spec-004-calendar-scheduling|SPEC-004]]"
    - "[[spec-003-task-lifecycle-v2|SPEC-003]]"
  works:
    - "[[work-002-task-lifecycle-v2|WORK-002]]"
  releases: []
  related: []
---

# W4 — 캘린더 시간 배정: `task_schedules` 와 3분할 캘린더 화면

업무는 **날짜 단위**로 산다. 그 위에 **시간 단위** 하나를 얹는다 — 월~수짜리 업무에
「월요일 오전 10시 · 화요일 오후 2시 · 수요일 오전 9시」처럼 **그 기간 안에서** 시간을 배분한다.
회의는 이미 시간 축을 갖고 있고, 없는 것은 **업무의 시간 배정** 하나다.
그리고 그 배분이 **확정 시안의 3분할 캘린더**(좌측 일정 레일 · 월/주 뷰 · 탭 셋)에서 실제로 불려지게 한다.

**만들지 않는 것**: 배정의 **명시적 삭제** · 시간 블록의 **날짜 이동** · 회의 도메인의 변경
(기간 파라미터 외) · 상태 변경 아홉 경로를 lifecycle 로 모으는 리팩터 · 저장소 DS `GutterList` 개명 ·
「더보기」 단추 · 반복 회의 · 근무 시간 · MCP 도구. **계약이 없거나 DEC-003 이 보류했다.**
그 자리들은 **빠뜨린 것이 아니라 후속으로 남긴 것**이고, 이 work 를 「캘린더 전체 완료」로 읽지 않는다.

> 1 파일 = 1 work = **빌드 계획**. SPEC-004 의 외부 계약 본문은 복제하지 않고 절 이름으로 가리킨다.
> **SPEC-004 는 검수 4회를 거쳐 PASS 다**(지적 13 → 3 → 1 → 0). **계약은 닫혔다.**
> 이 work 는 계약을 다시 정하지 않는다 — 모순을 발견하면 **고치지 않고 `Open Issues` 에 올린다.**

## Meta

- Baseline: **BASE-003** (시안 규칙 `R1`~`R9` · 사용자 원문 · 조사가 뒤집은 전제 둘)
- Decision: **DEC-003** — 채택 `§A`~`§J` · 증보 **`K1`~`K14`** · 기각 넷 · 보류 다섯
- Covers spec: **SPEC-004 전절** — §2 UX 계약 · §3 S-1~S-8(+S-1b·S-1c·S-4b) ·
  §4 API/Request-Response/Validation/Case Matrix/Flow/State/Data · §5 Implementation Rules ·
  §6 인수조건 **124줄**. **SPEC-003·SPEC-001** 은 대체되지 않은 절이 **회귀 기준**이다
  (상태 여섯 · 전이표 · 멱등 키 `K-1` · 낙관적 잠금 `K-4` · 영수증 `K-2` · 권한 재검사 ·
  `WORK_NOT_FOUND` 의 「없는 것과 못 읽는 것을 같은 말로」)
- Depends on work: **WORK-002(W2)** — 업무 생명주기 v2 가 기준선이다. **재구현하지 않는다.**
  이 work 는 그 위에 시간 축만 얹는다
- Parallel work: **없다. 이 work 안에서도 BE 와 FE 가 병행하지 않는다** — §Execution 의 직렬 규칙
- Follow-up work: 배정의 명시적 삭제 · 상태 변경 경로 통합 리팩터 · 저장소 DS `GutterList` 개명 ·
  「더보기」 단추 · 반복 회의 · 근무 시간(SPEC-003 M-23 의 남은 절반) · 배정의 MCP 표면
- External dependency: **없다.** 외부 API·credential 을 새로 붙이지 않는다.
  격리 PostgreSQL(`POSTGRES_TEST_URL`)과 로컬 demo DB 만 쓴다

### 착수를 막는 것과 막지 않는 것

| 무엇 | 착수를 막나 | 어디에 걸리나 |
|---|---|---|
| **WARN-A** — 뒤집힌 업무에서 「어느 화면 끝이 `start` 손잡이인가」와 R1 의 「길이」 | **아니다** | **Phase FE-2 의 한 줄.** 서버는 어느 매핑이든 **한 값**이고(K11 한 규칙) 할 수 있는 일도 같다. **FE 가 고르고 인수조건 한 줄을 단다** — §Phase FE-2 |
| **배정 삭제 없음의 구멍** (DEC-003 보류) | **아니다** | **이번 판에 열지 않는다.** `Open Issues` 가 들고 있다 |
| **착수 전 조사 ①** — `_ds_bundle` 토큰 **값** 대조 | **아니다** | **Phase FE-1 착수 전 한 줄.** 결정이 아니라 **확인 작업**이다 |
| **착수 전 조사 ②** — 실행 PostgreSQL 의 실제 제약 | **아니다** | **Phase BE-1 의 검증**에 들어간다. ORM 선언을 통과 근거로 쓰지 않는다 |
| SPEC-003 의 `OQ-203`·`OQ-206` | **아니다** | 이 work 와 무관하다. 시간 축은 완료 승인 경로를 건드리지 않는다 |

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | `kknaksss/strong-hajin-calendar` (코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`, base `origin/main` = `1b40f83`) |
| Blocker | 없음 — 위 표 |
| Next | Phase BE-1 발주 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위·보류 처분·사용자 질문 승격 | done |
| Design | kknaks | 시안 해석(레이아웃만) · DS-gaps 8건의 처분 | done |
| BE | `@sc-ax-be` | Phase BE-1 · BE-2 | todo |
| FE | `@sc-ax-fe` | Phase FE-1 · FE-2 | todo |
| QA | 코디네이터(자동) / 사용자(브라우저) | 자동 검증은 에이전트, 브라우저 E2E 는 사용자 | todo |
| Ops | kknaks | 스키마 적용 순서·rollback·배포 | todo |

## Scope

포함:

- **`task_schedules`** 한 표 — 업무에 완전히 종속. 범용 `schedules` 표를 만들지 않는다 (§A)
- 배정 **생성**(`POST`, 생성 전용) · **시각 변경**(`PATCH`) — 낙관적 잠금은 **배정 자신의 회차** (K8·K10)
- **합본 조회** — 업무 + 회의를 한 배열로, `kind` 로 가름. 「내 것만」 축 (§D · K2 · K13 · K14)
- `GET /api/meetings` 의 **기간 파라미터** — `from`/`to` 가 오면 구획도 커서도 쓰지 않는다 (§H · K2)
- **기간이 바뀔 때의 배정 검증** — 날짜가 바뀌는 **세 자리**에 명시적으로 (§B · §J)
- **소프트 딜리트** — `released_at` + 사유 둘. 되돌려도 복구하지 않는다 (§B · §J)
- **업무 종료는 읽기 필터** — 캘린더 조회가 내부 `DONE`·`CANCELLED` 를 거른다 (§B · §C)
- **닫힌 건수 응답** — `schedule_release{released_count, reason}` 을 세 자리 전부가 낸다 (K3)
- **캘린더 화면 재작성** — 3분할 · 월/주 뷰 · 탭 셋 · 상호작용 넷 · 금지 문구 (§E · §I)
- **DS-gaps** 중 필요한 것을 **우리가 만든다** (§J 정정 — 디자이너가 없다)
- **운영 대장 등록** · **local-stack 표지** · **도메인 모델 대조표** (§J)

제외:

- **배정의 명시적 삭제 경로** — 시안에 없고 DEC-003 이 **보류**했다. 덮어쓰기와 기간 조정으로만 바뀐다
- **시간 블록의 날짜 이동** — 시안에 길이 없다 (SPEC §2.3 R6)
- **회의 도메인의 변경** — `from`/`to` 외에는 손대지 않는다. 다만 **캘린더 경로가 「공유받은 회의는
  캘린더에 서지 않는다」는 기존 규칙을 뒤집는다**(K9) — 회의 도메인 **코드는 건드리지 않고**
  합본 조회가 자기 규칙으로 읽을 뿐이며, **회의 화면 경로는 기존 동작 그대로**다
- **MCP 도구** — 내지 않는다. `status: excluded` · `policy: E2` 로 사유를 단다 (§J)
- **상태 변경 아홉 경로 통합 리팩터** — 이번 판이 읽기 필터라 급하지 않다. **다음에 쓰기가
  필요해지면 이것이 선행조건**이 된다 (DEC-003 보류)
- **저장소 DS `GutterList` 개명** — 소비처 미집계. **새것에 다른 이름**을 준다 (§J)
- **반복 회의**(`repeat`) · **근무 시간** · 시안 목데이터의 `badge`·`actions`·`starred`·`unread`
- **브라우저 E2E** — **사용자 담당.** 에이전트는 자동 검증까지 (§검증 책임의 경계)

## Code Surface

- Repo / module: `toy_pr2/Strong_hajin` (SCAX modular monolith).
  워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`,
  브랜치 `kknaksss/strong-hajin-calendar`, base `origin/main` = **`1b40f83`**.
  **조사 시점에 워크트리는 깨끗했다**(조사 2건 · 검수 4회 모두 `git status --short` 공백 확인).
- 규약: `AGENTS.md` — 백엔드 테스트는 **Makefile 타겟으로만**(`uv run pytest` 직접 호출 금지) ·
  프론트는 `make frontend-test` · HTTP/MCP 시그니처를 바꾸면
  `tests/architecture/test_operation_inventory.py` 가 `docs/unified-operations-inventory.json` 과의
  drift 를 잡는다(**전체 재작성 금지, diff 난 항목만 패치** — `AGENTS.md:15`).

### 이번에 만질 파일 — `be-survey-report.md` §2 가 센 전수를 실행 목록으로

| # | 파일 | 무엇을 | Phase |
|---|---|---|---|
| 1 | `backend/src/ax_workspace/platform/persistence.py` | **`TaskScheduleRecord(Base)` 선언.** `__table_args__` 에 부분 unique + CHECK. 표 90개가 여기 산다 | BE-1 |
| 2 | `backend/src/ax_workspace/bootstrap/schema_sync.py` | **코드 수정 불필요.** 새 표면 `CreateTable` + **그 표의 인덱스 전부**를 함께 낸다(`:27-31`) | — |
| 3 | `backend/src/ax_workspace/entrypoints/reset_demo.py` · `bootstrap/reset.py` | **코드 수정 불필요.** `make sync-demo-schema` 가 표를 만든다 | — |
| 4 | `backend/src/ax_workspace/platform/task_schedules.py` **(신규)** | 배정 조회·쓰기 SQL. `work_tasks.py` 의 `SqlAlchemyTaskRepository` 와 같은 결 | BE-1 |
| 5 | `backend/src/ax_workspace/modules/work/schedule.py` **(신규 · 순수 도메인)** | 「기간을 읽는 법」 네 경우(K7·K11) · 기간 밖 판정 · 닫기 사유 결정 | BE-1 |
| 6 | `backend/src/ax_workspace/modules/work/application.py` | 배정 CRUD 유스케이스 + **D1 세 자리** (아래) | BE-1 · BE-2 |
| 7 | `backend/src/ax_workspace/bootstrap/application.py` | `:4222-4233` `_tasks()` — **새 repository 조립은 여기서만.** 합본 조회 facade | BE-1 |
| 8 | `backend/src/ax_workspace/entrypoints/http.py` | **새 라우트 셋** + `GET /api/meetings`(`:665-674`)에 `from`/`to` | BE-1 |
| 9 | `backend/src/ax_workspace/modules/meetings/application.py` | `board()`(`:211-226`)가 기간 인자를 받는 갈래. **`_is_past`·`my_meetings` 는 건드리지 않는다** | BE-1 |
| 10 | `backend/src/ax_workspace/platform/meetings.py` | `meetings_visible_to`(`:144-170`)에 시각 조건 추가(또는 호출부 필터) | BE-1 |
| 11 | **`docs/unified-operations-inventory.json`** | **행 3 추가 + `http_count` 156→159 + `GET /api/meetings` 행의 `http_signature` 갱신.** `tool_count` **129 불변** | BE-2 |
| 12 | `Makefile:170` + `backend/tests/architecture/test_local_stack_targets.py:28-40` | local-stack preflight 표지에 **`task_schedules` 추가 — 둘을 동시에** | BE-2 |
| 13 | `backend/tests/architecture/test_test_pyramid.py` `PURE_DOMAIN_MODULES` | **#5 를 만들면 여기 한 줄 등재** — 안 하면 순수성이 안 지켜진다 | BE-1 |
| 14 | `docs/domain-model.md` | ERD 대조표에 **한 줄** (선례 `TASK_REFERENCE` — `:110`) | BE-2 |
| 15 | `backend/tests/integration/postgres/` | **부분 unique 가 실제로 선다**를 증명하는 새 파일. 선례 `test_task_lifecycle_v2_schema_postgres.py` | BE-1 |
| 16 | `backend/tests/contract/` · `tests/unit/` | 계약·도메인 테스트. **RED 먼저** | BE-1 · BE-2 |
| 17 | `frontend/src/features/calendar/CalendarPage.tsx` | **재작성.** `:106` 주석 「이 화면은 업무만 낸다」가 뒤집힌다 | FE-1 |
| 18 | `frontend/src/App.tsx` | `:468` 이 `onRegisterRails` 를 **안 넘긴다** — 넘기게 고친다. 선례 `MyWorkPage.tsx:899-921` | FE-1 |
| 19 | `frontend/src/features/calendar/` **(신규 부품들)** | 레일·카드·월 격자·주 격자·일정 조각 — §DS-gaps | FE-1 · FE-2 |
| 20 | `frontend/src/lib/api.ts` | 배정 CRUD · 합본 조회 · `listMeetings` 에 기간 인자 | FE-1 |
| 21 | `frontend/src/lib/viewModels.ts` | 배정·합본 행 타입. **`TaskState` 5종은 그대로** — `completion_submitted` 를 들이지 않는다 | FE-1 |
| 22 | `frontend/src/ds/Empty.tsx` | **`icon` prop 추가 — additive.** 기존 `variant` 경로는 그대로이고 **소비처 19곳을 고치지 않는다.** 그 파일 docstring 이 「props 는 우리 것을 그대로 지켰다(D-4) — 소비처를 고치지 않는다」를 규율로 적어 뒀다. **props 를 더하는 것이 그 규율이 닿는 자리다** (G-CAL-02) | FE-1 |
| 23 | `frontend/src/styles/` | 시안 `calendar.css` 103줄 중 **89줄이 값 수정 없이** 옮겨진다. 토큰 `--scax-*` 51종은 저장소에 **전부 있다** | FE-1 |

**고치지 않지만 걸리는 회귀 가드** (`be-survey-report.md` §2 「여기 없던 자리」) —
**이 파일들을 편집하지 않는다. 깨지면 우리가 규약을 어긴 것이다.**

| 가드 | 무엇을 막나 |
|---|---|
| `tests/architecture/test_architecture.py:67-74` | **API startup 경로에 스키마 생성이 끼는 것.** `create_all` 을 monkeypatch 로 막고 `create_app()` 을 띄운다 |
| `tests/architecture/test_architecture.py:139-148`·`:158-162`·`:172-194` | 도메인이 `fastapi`·`mcp`·`sqlalchemy` 를 import · `entrypoints/` 에 영속 계층 **문자열**이 뜸 · `*Application` 을 `bootstrap/application.py` 밖에서 조립 |
| `tests/architecture/test_operation_inventory.py:119-141`·`:144-198`·`:201-249` | 대장 drift. `http.py` 를 **AST 로 파싱**해 라우트마다 비교한다 |

**`entrypoints/mcp.py` · `modules/ax_execution/tool_catalog.py` 는 건드리지 않는다** —
MCP 도구를 내지 않으므로 `tool_count` 가 **129 그대로**다(§J).

**`TaskCalendar`(`WorkViews.tsx:257-270`)는 고치지 않고 새로 세운다** — 실 소비처가
`CalendarPage` 하나뿐이지만 시그니처·앵커·주 뷰 성격이 전부 다르다(`fe-survey-report.md` §2-1).
**`taskSpan` 은 `TaskTimeline` 이 같이 쓰므로 읽기만** 한다 — **캘린더는 그것을 쓰지 않고
서버가 준 `span_from`·`span_to` 를 쓴다**(K14).

### D1 — 날짜가 바뀌는 **세 자리**. 한 자리로 모으지 않는다

| # | 자리 | 무엇이 바뀌나 | 진입 표면 |
|---|---|---|---|
| ① | `modules/work/application.py:518-520` `update` | `start_date`·`due_date` 둘 다. `validate_schedule` 을 **바로 앞(`:518`)에서** 부른다 | `PATCH /api/tasks/{task_id}` · MCP `task_update` |
| ② | `modules/work/application.py:1443` `transition` | `start_date` 만. 순수 도메인 `lifecycle.py:165-172` 가 `open → in_progress` 이고 `start_date` 가 비었을 때 `command.today` 를 넣는다. **`validate_schedule` 을 안 지난다** | `POST /api/tasks/{task_id}/start` · MCP `task_start` |
| ③ | `modules/work/application.py:1679` `_apply_proposal` | `due_date` 만. 제안 payload 를 `date.fromisoformat()` 으로 바로 대입. **`validate_schedule` 을 안 지난다** | `POST /api/tasks/{id}/proposals/{pid}/respond` |

- **공통 지점 `repository.touch()` 에 걸지 않는다.** 날짜와 무관한 변경에도 아홉 번 불리므로
  「날짜가 바뀌었나」를 스스로 판정해야 하고 **틀리면 조용히 안 돈다** (§J).
- **②·③ 이 `validate_schedule` 을 안 지나므로 뒤집힌 기간이 실재한다**(`be-survey-report.md` §8-5).
  그래서 **K11 정규화**가 계약이 됐다. **이 work 는 그 두 자리를 고치지 않는다** — 계약으로 덮는다.
- **생성 시점은 대상이 아니다** — 새 업무에는 배정이 없다.

### 상태가 바뀌는 **아홉 경로** — 여기에는 걸지 않는다

`be-survey-report.md` §4 가 셌다. `lifecycle.transition_task()` 를 지나는 것은 **하나뿐**이고,
`CANCELLED` 로 가는 길이 **다섯**(그중 셋이 영속 계층), `DONE` 으로 가는 길이 **둘**이다.
**그래서 §B 가 업무 종료를 읽기 필터로 옮겼다.** 이 work 는 **그 아홉 자리에 아무것도 더하지 않는다.**
캘린더 조회 한 자리에서 `tasks.state` 를 조인해 거른다.

### 계약이 닿는 입구 — 전수

| 표면 | 이번에 |
|---|---|
| `POST /api/tasks/{task_id}/schedules` | **신규** |
| `PATCH /api/task-schedules/{schedule_id}` | **신규** |
| `GET /api/calendar?from=&to=` | **신규** |
| `GET /api/meetings` | **인자 추가** — 행 모양은 `from`/`to` 없을 때 그대로 |
| `PATCH /api/tasks/{task_id}` | **응답에 `schedule_release` 추가** (K3) |
| `POST /api/tasks/{task_id}/start` | 같음 (② 자리) |
| `POST /api/tasks/{id}/proposals/{pid}/respond` | 같음 (③ 자리) |
| MCP | **없다.** `target_tools` 를 비우므로 `tool_count` 불변 |
| AX 실행 경로 | **없다.** 배정은 격자 위의 직접 조작이다 (§J) |

## Domain / Schema

`20-spec/README.md` § Data / Domain Boundary 가 column·index·FK·ORM·repository 를 **여기로 보냈다.**
SPEC-004 는 외부에 드러나는 것만 갖는다. **실제 모양은 이 절이 확정한다.**

### 지금 코드에 있는 것

- 표 **90개**(`persistence.py`). 예정 시각을 담는 것은 **`meetings.starts_at`/`ends_at` 뿐**이다.
- 마이그레이션 체계는 **없다**(`backend/migrations/manual/2026-09-17-w2-indexes.sql:8-12`).
  `schema_sync` 는 **없는 표를 만들고 없는 컬럼을 더할 뿐**, 기존 표에 인덱스를 더하지 않는다.
  **새 표는 `--sync` 가 인덱스까지 함께 만든다**(`:14-15` · `schema_sync.py:27-31`).
- `released_at` + 부분 unique 선례가 **둘** — `task_predecessors`(`persistence.py:995-1042`,
  인덱스 `:1015-1022`) · `task_references`(`:1497-1526`, 인덱스 `:1506-1515`).

### 새로 필요한 것 — 표 하나. **additive 만**

```text
task_schedules                                  ← 새 표
  id                String   PK (uuid)
  task_id           String   FK → tasks.id  NOT NULL
  on_date           Date     NOT NULL              배정된 날
  starts_at         Time     NOT NULL              시작 시각
  ends_at           Time     NOT NULL              종료 시각
  version           Integer  NOT NULL  default 1   ← 증보 K8. 배정 자신의 회차
  released_at       DateTime NULL                  소프트 딜리트 — 비어 있으면 살아 있다
  released_reason   String   NULL                  out_of_range | task_dates_cleared
  created_at        DateTime NOT NULL
  updated_at        DateTime NOT NULL

  Index  uq_task_schedules_active  UNIQUE (task_id, on_date)
         sqlite_where / postgresql_where = released_at IS NULL     ← 하루 한 칸
  CHECK  ck_task_schedules_time_order  (ends_at > starts_at)
```

**결정과 그 근거.**

| 무엇 | 결정 | 근거 |
|---|---|---|
| 표 이름·컬럼 | 위 그대로 | DEC-003 **§A** |
| `released_by` | **두지 않는다.** nullable 도 안 만든다 | **§J** — 닫기는 시스템 판정이라 member id 가 없다. 왜는 `released_reason` 이 말한다. **선례(`task_predecessors`)에는 있지만 여기서는 뺀다** |
| 부분 unique | `(task_id, on_date) WHERE released_at IS NULL` | **§A · §J.** `uq_task_predecessors_active`(`:1015-1022`)와 **글자 그대로 같은 구조**. 닫힌 행이 유일성에서 빠진다 |
| 30분 눈금 CHECK | **박지 않는다** | **§J** — 나중에 15분으로 바꿀 때 마이그레이션이 필요해진다. 화면 편의로 둔다 |
| `ends_at > starts_at` CHECK | **둔다** | 저장소의 결 — `TaskPredecessorRecord` docstring(`:1000-1011`)이 「자기 자신 금지는 CHECK 이 답한다」로 **값 수준 불변식을 DB 로 내리는 선례**를 세웠다. **사용자 계약은 안 바뀐다** — 표면은 여전히 `TASK_SCHEDULE_INVALID_RANGE` 422 다(SPEC §4) |
| `version` | `Integer NOT NULL default 1`, 쓰기마다 +1 | **증보 K8** — 회차의 주인은 배정이다. **업무 회차를 올리지 않는다**(다른 화면의 낙관적 잠금이 깨진다) |
| 추가 조회 인덱스 | **이번에 만들지 않는다** | 부분 unique 가 `(task_id, on_date)` 를 이미 덮고, 합본 조회는 **내 업무 집합 + 날짜 범위**로 들어온다. 필요해지면 **기존 표가 아니라 새 표**라 `--sync` 가 함께 만든다 |
| `meetings` 변경 | **없다** | **§A** — `task_id` 를 뚫으면 거기 FK 를 건 표 다섯(`meeting_agendas`·`meeting_lines`·`meeting_attendees`·`meeting_transcripts`·`meeting_recording_files`)에 **빈 가지**가 생긴다 |
| `tasks` 변경 | **없다** | 1업무 : N배정이라 시각 컬럼이 애초에 안 된다(DEC-003 기각) |

### Aggregate 경계와 불변식

- **배정은 업무의 자식이다.** 독립 aggregate 가 아니고 **자기 가시성 규칙을 갖지 않는다** —
  업무를 읽을 수 있으면 배정도 읽을 수 있다(선례 `task_references` · `docs/domain-model.md:110`).
- **불변식 셋**
  1. **하루 한 칸** — `(task_id, on_date)` 당 살아 있는 행은 **0 또는 1**.
     **데이터베이스가 답한다**(부분 unique). application 검사만으로 낮추지 않는다 —
     두 명령이 동시에 들어오면 **둘 다 「없다」를 보는 틈**이 남는다.
  2. **기간 안** — `span_from <= on_date <= span_to`. 「기간을 읽는 법」은 **네 경우**(아래).
     **application 이 답한다** — 업무의 날짜를 읽어야 해서 DB 제약으로 못 내린다.
  3. **닫힘은 끝** — `released_at` 이 찍히면 되살아나는 전이가 없다.
- **기간을 읽는 법 — 네 경우** (SPEC §4 Validation · 순수 도메인 `modules/work/schedule.py` 가 갖는다)

  | 경우 | 구간 |
  |---|---|
  | ① 둘 다 있고 순서가 맞음 | `[start_date, due_date]` |
  | ② 한쪽만 있음 | 남은 한쪽의 **그 날 하루** (K7) |
  | ③ 둘 다 없음 | **기간 없음** — 배정을 만들 수 없다 |
  | ④ `start_date > due_date` | **`[min, max]` 로 정규화** (K11). **빈 구간으로 보지 않는다** |

  **이 함수의 결과가 곧 응답의 `span_from`·`span_to`** 다(K14). **화면이 다시 계산하지 않는다.**
- **닫기 사유는 둘뿐이다** — `out_of_range` · `task_dates_cleared`.
  **셋째가 생기는 경로가 없다**: 같은 날 재배정은 **`PATCH` 가 같은 행을 갱신**하므로 닫지 않고(K1·K10),
  업무 종료는 **읽기 필터**라 쓰기가 아니다(§B).

### Migration 기술안 — 이 레포에 실제로 있는 도구로만

1. `persistence.py` 에 `TaskScheduleRecord` 를 선언한다.
2. `make sync-demo-schema`(= `python -m ax_workspace.entrypoints.reset_demo --sync`)를 돌린다.
   **새 표라서 `CreateTable` + 인덱스 전부**가 한 트랜잭션에 나간다(`schema_sync.py:27-31`·`:64-70`).
3. `plan()` 의 `manual[]` 출력이 **비어 있어야 한다** — NOT NULL 인데 `server_default` 가 없는 열이
   있으면 거기 뜬다(`schema_sync.py:33-41`). **뜨면 그 열을 고친다.**
4. **손 `.sql` 이 필요 없다.** 그것은 **기존 표에 인덱스를 더할 때**만 필요하고, 이번엔 없다.
5. **운영 적용**: 새 표라 `CONCURRENTLY` 가 필요 없다. 다만 **코드 배포 전에 표가 먼저** 있어야 한다
   (§Pre-deploy Check).
6. **`reset_demo` 안전 장치를 우회하지 않는다** — `require_safe_demo_database()` 가
   host `localhost|127.0.0.1|::1` + db 이름 `^ax_(demo|test)(_[a-z0-9_]+)?$` 를 **연결 전에** 본다.

## Dependency

| 무엇 | 상태 |
|---|---|
| **WORK-002 (W2)** | 업무 생명주기 v2 가 `review`. **이 work 는 그 상태·전이표를 읽기만** 한다. W2 가 미완이어도 착수를 막지 않는다 |
| 실행 PostgreSQL | **Phase BE-1 검증에 필요.** `POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar` — **이번 작업 전용 DB** |
| Node 20 | `make frontend-test` 가 요구한다. Node 25 에서는 jsdom localStorage 오류가 난다(W2 기록) |
| 시안 | `reference/2026-09-10-sc-meeting/package 2/` — **레이아웃 정본.** 기능 정본이 아니다 |
| 디자이너 | **없다.** DS-gaps 는 우리가 만든다 (DEC-003 §J 정정) |

## Internal Interface Contract

**BE 가 내는 것과 FE 가 쓰는 것을 같은 단위에서 닫는다.** 다만 **이 work 는 직렬**이라
FE 는 BE 가 닫힌 뒤에 소비를 붙인다 — 아래는 **무엇이 짝인지**를 못 박는 표다.

| # | BE 가 내는 것 | FE 가 쓰는 것 | 짝 |
|---|---|---|---|
| I-1 | `GET /api/calendar` 의 한 배열 + `kind` | 격자·레일의 데이터 원천. **두 번 부르지 않는다** | BE-1 ↔ FE-1 |
| I-2 | 업무 행의 **`span_from`·`span_to`** (K14) | **띠를 그리는 구간**과 **시간 격자 드롭 가드**가 **같은 값**을 쓴다. `taskSpan()` 을 쓰지 않는다 | BE-1 ↔ FE-1·FE-2 |
| I-3 | `schedules[]` 원소의 **`schedule_id`·`version`** (K8·W-9) | **시각 변경을 부를 값.** 없으면 FE 가 `PATCH` 를 못 부른다 | BE-1 ↔ FE-2 |
| I-4 | `POST` 는 **생성 전용**, 그 날이 차 있으면 **409**; **영수증이 먼저** (K10·K12) | 같은 날 재배정은 **`PATCH`** 로 보낸다. 연타는 **같은 멱등 키**로 보낸다 | BE-1 ↔ FE-2 |
| I-5 | `PATCH /api/tasks` 응답의 **`schedule_release{released_count, reason}`** (K3) | 「N건의 시간 배정이 기간 밖이라 해제되었습니다.」 문구. **0건이면 말하지 않는다** | BE-2 ↔ FE-2 |
| I-6 | 회의 행의 **`created_by_display_name`** (K4) | 회의 카드의 주최자 이름. member id 를 그리지 않는다 | BE-1 ↔ FE-1 |
| I-7 | `from`/`to` 가 오면 **구획도 커서도 없는 한 배열** (K2) | 한 화면 = 한 요청. **공유받은 다음 주 회의가 제자리에** 선다 | BE-1 ↔ FE-1 |
| I-8 | 거절의 **에러 코드 열 종**과 그 「언제」 | **문구를 낸다.** 조용한 거절 0개 (§I) | BE-1·BE-2 ↔ FE-2 |

> **I-2 가 특히 한 단위여야 한다.** 3차 검수의 FAIL(F-8)이 바로 그 자리였다 —
> 서버가 `[9/4, 9/6]` 으로 받는 날을 화면이 `[9/6, 9/6]` 으로 막았다.
> **K14 가 필드로 닫았으므로 FE 는 계산하지 않고 받는다.**

## Execution

각 Phase 의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나다.
Phase 별 `완료 판정`이 완료 조건이다.

### 단계 순서 — **직렬이다**

```text
Phase BE-1 ──▶ Phase BE-2 ──▶ Phase FE-1 ──▶ Phase FE-2
```

- **BE 가 닫히기 전에 FE 를 태우지 않는다.** 같은 코드 워크트리를 공유하므로 병행하면 서로를 덮는다.
- **BE-2 검수 통과 후 실제 API 계약을 FE 브리프에 박는다** — 추정으로 쓰지 않는다.
- **백엔드 커밋이 들어가면 API 를 반드시 다시 띄운다**
  (config `rules.restart_api_after_backend_commit`). 옛 코드가 떠 있으면 **「프론트가 안 된다」로 보인다.**
- 워커가 못 정하는 것이 나오면 **코디가 결정**하고 DEC-003 에 증보로 남긴 뒤 루프에 복귀한다.
  **조용히 정하지 않는다.**

---

### Phase BE-1 — 스키마 + 배정 CRUD + 합본 조회

- **Status**: TODO
- **설명**: `task_schedules` 를 세우고, 배정 생성·시각 변경·합본 조회 셋을 연다.
  **여기까지가 「배정이라는 것이 존재한다」**다.

**작업**

1. **선행 점검 (읽기 전용)** — 실행 PostgreSQL 에 접속해 `information_schema`·`pg_index` 로
   **지금 있는 제약**을 센다. **ORM 선언과 같다고 전제하지 않는다.**
   결과를 한 줄로 남긴다. **여기서 코드를 고치지 않는다.** ← 착수 전 조사 ②
2. `persistence.py` 에 `TaskScheduleRecord` 선언 (§Domain / Schema 의 표 그대로).
3. `make sync-demo-schema` → **`manual[]` 출력이 비어 있는지** 확인.
4. `modules/work/schedule.py`(신규 · **순수 도메인**) — 「기간을 읽는 법」 네 경우 · 기간 밖 판정.
   **`tests/architecture/test_test_pyramid.py` 의 `PURE_DOMAIN_MODULES` 에 등재**한다.
5. `platform/task_schedules.py`(신규) — 조회·쓰기. **조회는 기본으로 `released_at IS NULL`** 을 건다
   (선례 `work_tasks.py:679-684` `references_for(..., include_released=False)`).
6. `modules/work/application.py` 에 유스케이스 셋:
   - **생성** — 멱등 키 조회 → (같은 키면 **영수증 `200`**) → 담당 관계 검사 →
     업무 상태 검사 → 기간 검사 → **그 날이 차 있으면 `409`** → 생성 `201`.
     **`expected_version` 을 받지 않는다** (K10·K12).
   - **시각 변경** — `expected_version` **무조건 필수**. `on_date` 를 받지 않는다.
     **닫힌 배정은 존재를 숨긴다**(404).
   - **합본 조회** — 업무는 `my_work` 축, 회의는 `board` 축. **기존 조회를 재사용**한다 —
     새 질의를 직접 쓰면 「이 사람이 그 업무를 열 수 있는가는 **한 자리에서만 답한다**」가 깨진다
     (`be-survey-report.md` §7 해석 1). 업무 행에 **`span_from`·`span_to`**(K14)와 `version`,
     회의 행에 **`created_by_display_name`**(K4, member 조인)을 싣는다.
     **끝난 업무(`DONE`·`CANCELLED`)를 거른다** — `COMPLETION_SUBMITTED` 는 **남긴다**(§C).
7. `GET /api/meetings` 에 `from`/`to`. **둘이 오면 구획도 커서도 쓰지 않고 한 배열**,
   **없으면 기존 동작 그대로**(K2). **`_is_past`·`my_meetings` 를 건드리지 않는다.**
8. `entrypoints/http.py` 에 새 라우트 셋. `bootstrap/application.py` 에서만 조립한다.
9. `tests/integration/postgres/` 에 **부분 unique 증명** 파일 추가.

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make test-unit` · `make test-contract` **통과**.
- [ ] **`make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar`
      통과**, 그 안에 다음 넷이 **각각 한 건씩** 남는다:
      ① `information_schema`·`pg_index` 에 부분 unique 가 **있고 valid** ·
      ② 그 술어가 **「닫히지 않은 행만」** ·
      ③ 같은 (업무, 날)에 살아 있는 배정 둘을 넣으면 **거절** ·
      ④ **닫힌 행이 있는 날에 새 배정이 받아들여진다.**
      **SQLite 선언은 아무것도 증명하지 않는다.**
- [ ] 선행 점검 ②의 결과가 **한 줄로 기록**됐다.
- [ ] `curl` 로 세 라우트가 **실물 응답**을 낸다 — 생성 `201` · 같은 날 두 번째 `409` ·
      같은 키 재전송 `200` · 시각 변경 `200` · 합본 조회가 `kind` 두 종을 낸다.
- [ ] **커밋 후 API 를 다시 띄웠다.**

---

### Phase BE-2 — D1 세 자리 + K3 `released_count` + 운영 대장

- **Status**: TODO
- **설명**: 배정이 **사라지는 두 경로**를 실제로 걸고, 닫힌 건수를 응답에 싣고,
  표면 등록을 마친다. **여기까지가 「배정이 업무를 따라간다」**다.

**작업**

1. **D1 세 자리에 명시적으로** 검증을 건다 — `application.py:518-520` · `:1443` · `:1679`.
   각 자리에서 **날짜가 실제로 바뀌었을 때만** 돈다. **`touch()` 에 걸지 않는다.**
2. 닫기 — 정규화 구간 밖이면 `released_at` + `out_of_range`,
   날짜를 **전부 지웠으면** 전부 닫고 `task_dates_cleared`.
   **검증과 저장이 한 transaction 에 있다** — 나뉘면 「닫혔는데 업무 날짜는 안 바뀐」 상태가
   **복구 경로 없이** 남는다.
3. **세 자리 전부**가 응답에 `schedule_release{released_count, reason}` 를 싣는다 (K3).
   **0건이면 `released_count=0`·`reason=null`.** **문구는 서버가 만들지 않는다.**
4. **업무 종료는 쓰기가 아니다** — 아홉 경로에 아무것도 더하지 않고, **합본 조회의 필터**만 확인한다.
5. **운영 대장** — `docs/unified-operations-inventory.json` 에 **행 3 추가**,
   `http_count` **156 → 159**, `tool_count` **129 불변**.
   각 행에 `status: excluded` · `policy: E2` ·
   `exclusion.reason`(「업무 시간 배분은 캘린더 격자 위의 직접 조작이다. 에이전트가 대신 잡을 근거가
   지금은 없다」) · `reconsider_when`(「AX 가 일정 제안을 하게 될 때」).
   `GET /api/meetings` 행의 **`http_signature` 갱신**(인자가 늘었다) +
   합본 조회 행의 응답 필드 증가도 그 행에 든다.
   **전체 재작성 금지 — 테스트 실패 diff 의 그 항목만 패치.** 선례 — excluded 6건
   (`GET /api/auth/providers` 등)이 같은 모양.
6. **local-stack 표지** — `Makefile:170` 의 `to_regclass(...)` 목록에 `task_schedules` 추가 +
   `tests/architecture/test_local_stack_targets.py:28-40` 을 **동시에** 고친다.
   한쪽만 고치면 깨진다.
7. `docs/domain-model.md` 대조표에 **한 줄**.

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make test-unit`(= `test_operation_inventory` 포함) · `make test-contract` **통과**.
- [ ] **세 자리 각각**에 대한 테스트가 있다 — 업무 수정 · **시작 전이** · 조건 변경 제안 동의.
      **시작 전이 자리는 「닫을 것이 없음」을 증명한다**(`released_count = 0`) —
      K11 이후 그 자리에서 닫히는 배정은 **구조적으로 나올 수 없다**(§인수조건 추적 F 참조).
      **검증 훅과 `schedule_release` 묶음은 그래도 있다** — K3 이 세 자리 전부에 요구한다.
- [ ] 기간을 줄였다 되돌리면 **빈 채로 돌아온다**(복구 없음), 그 날에 **다시 배정할 수 있다**(부분 unique).
- [ ] `make test-postgres` **재통과**(동시성·제약 회귀).
- [ ] `docs/unified-operations-inventory.json` 의 diff 가 **행 3 + count 1줄 + `http_signature` 2줄**
      이내다. `acceptance_evidence` 가 **보존**됐다.
- [ ] `make local-stack` preflight 가 `task_schedules` 를 **본다**.
- [ ] **커밋 후 API 를 다시 띄웠다.** **실제 API 계약(응답 예시)을 FE 브리프에 박았다.**

---

### Phase FE-1 — 화면 골격: 3분할 · 좌측 레일 · 월/주 뷰

- **Status**: TODO
- **설명**: 레이아웃과 데이터 배선. **아직 쓰기는 없다.**

**작업**

0. **선행 확인 (한 줄로 끝낸다)** — `_ds_bundle.css`(4069줄)·`_ds_bundle.js`(1862줄)의
   **토큰 값**이 저장소 `styles/scax.css` 의 정의와 같은지 대조한다. 참조 이름은 이미 맞췄고
   **값은 안 봤다**(BASE-003 § 안 본 것). **결정이 아니라 확인 작업**이다.
   다르면 **저장소 값이 정본**이고 그 사실만 기록한다. ← 착수 전 조사 ①
1. `App.tsx:468` 이 `CalendarPage` 에 **`onRegisterRails` 를 넘기게** 고친다.
   선례 `MyWorkPage.tsx:899-921`. 셸은 이미 3칸 규약을 갖는다(`AppShell.tsx:74-82`).
2. **오른쪽 레일은 비운다** — `railLeft` 만 (§J).
3. 본문 스크롤 — 시안 캘린더는 **칸을 꽉 채워 자기 안에서 스크롤**한다.
   회의 화면이 같은 충돌을 `--fixed` 변종으로 풀었다(`shell.css:182` · `App.tsx:458`).
4. `lib/api.ts` 에 합본 조회 · 배정 CRUD · `listMeetings(from, to)`.
   `lib/viewModels.ts` 에 그 타입. **`TaskState` 5종 유지.**
5. **부품 신설** — 아래 DS-gaps 표의 **만든다** 칸.
6. 월 뷰 · 주 뷰 렌더링 — **읽기만.** 띠는 **`span_from`·`span_to`** 로 그린다(K14).
7. 탭 셋 · 날짜 선택 · lane 상한 · 「오늘」(`seoulToday()`).
8. **격자는 상태를 말하지 않는다** — 유형 둘로만. **좌측 카드·상세는 기존 상태 어휘**를 쓴다.

**DS-gaps 8건의 처분 — 전부 배치한다** (만든다 **다섯**: 01·02·04·05·06 · 만들지 않는다 **셋**: 03·07·08)

| ID | 없는 것 | 처분 | 어디에 | Phase |
|---|---|---|---|---|
| G-CAL-01 | 레일형 `GutterList` 부품 | **만든다.** 저장소 DS 의 같은 이름과 **다른 이름**을 준다(§J) — 제안 `ScheduleRail`. 마크업은 `InboxRail.tsx:103-114` 에 인라인으로 이미 있다 | `features/calendar/ScheduleRail.tsx` | FE-1 |
| G-CAL-02 | `Empty` 의 `icon` prop | **만든다** — `ds/Empty.tsx` 에 `icon` 을 **추가**한다(기존 `variant` 경로는 그대로) | `ds/Empty.tsx` | FE-1 |
| G-CAL-03 | `TaskCreateModal` | **만들지 않는다.** 업무 만들기는 **기존 모달**을 쓴다(§J 정정). 시안의 필드 구성을 따라가지 않는다 | — | — |
| G-CAL-04 | `ItemCard` / `InboxCard` 부품 | **만든다.** `.scax-inbox-card` 클래스는 저장소에 **전부 있고**(`components.css:111-121`) 시안이 더하는 것은 `--draggable` 한 종뿐이다 | `features/calendar/ScheduleCard.tsx` | FE-1 |
| G-CAL-05 | 일정 조각(`Event`) 부품 일체 — 띠·손잡이·고스트·`+N건` | **만든다.** 스타일은 시안 `calendar.css:34-57`·`95-103` 에서 옮긴다 | `features/calendar/EventBar.tsx` 등 | FE-1(띠·`+N건`) · FE-2(손잡이·고스트) |
| G-CAL-06 | `MonthGrid` · `WeekGrid` | **만든다.** 기존 `TaskCalendar` 를 고치지 않고 **새로 세운다** | `features/calendar/MonthGrid.tsx` · `WeekGrid.tsx` | FE-1 |
| G-CAL-07 | `AppHeader` 의 `titleEnd` | **만들지 않는다.** 캘린더는 `title`+`actions` 만 쓴다(SPEC §2.8) | — | — |
| G-CAL-08 | 상태 색 tint | **격자에는 만들지 않는다**(§J — 유형 둘로만). **좌측 카드는 기존 상태 톤**을 쓴다 | — | FE-1(기존 톤 재사용) |

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make frontend-test`(**Node 20**) · `cd frontend && npx tsc --noEmit` **통과**.
- [ ] **`ds/Empty.tsx` 의 기존 소비처가 전부 그대로 컴파일된다** — `npx tsc --noEmit` 에서
      **19곳 중 한 곳도 고치지 않았다.** `icon` 은 **additive** 이고 계약을 바꾸지 않는다.
- [ ] 선행 확인 ①의 결과가 **한 줄로 기록**됐다.
- [ ] 화면이 **3분할**이고 오른쪽 레일이 비어 있다. 탭 셋이 **레일과 격자를 동시에** 가른다.
- [ ] 주 뷰가 **종일 칸 + 0~24시**이고 **8시에 맞춰 열린다.** 월 뷰가 **완전히 달 밖인 마지막 주를 지운다.**
- [ ] **한 화면 = 한 요청**이다 — 주 뷰 7일·월 뷰 42일이 각각 한 번의 합본 조회로 그려진다.
- [ ] **뒤집힌 업무의 띠가 `[9/4, 9/6]` 으로 그려진다**(서버가 준 구간 그대로). `taskSpan()` 을 쓰지 않는다.
- [ ] 회의 카드에 **주최자 이름**이 뜨고 member id 가 안 보인다.
- [ ] **공유받은 다음 주 회의가 그 주에 제자리로** 선다.
- [ ] 격자에 **상태 색이 없다.** 새 레일 부품이 **저장소 DS 의 `GutterList` 와 다른 이름**을 쓴다.

---

### Phase FE-2 — 상호작용 넷: 드롭 · 손잡이 · 시간 배정 · 금지 문구

- **Status**: TODO
- **설명**: 쓰기를 붙인다. **여기까지가 「시간을 배분할 수 있다」**다.

**작업**

1. **R1 · 날짜 칸 드롭** = 기간 이동 → `PATCH /api/tasks`. 회의는 못 끈다(`draggable: false`).
2. **R3 · 좌우 손잡이** = 시작·마감일 조정 → 같은 명령.
3. **R4 · 마감만 있던 업무**가 손잡이로 기간을 갖는다.
4. **R5 · 시간 격자 드롭** = 배정 생성 → `POST`. 기본 1시간 · 30분 눈금 · 고스트.
   **가드는 `span_from`·`span_to`** 로 판정한다(K14).
   **같은 날에 이미 배정이 있으면 `POST` 가 아니라 `PATCH`** 를 보낸다(K10) —
   `schedules[]` 가 `schedule_id`·`version` 을 이미 주었다.
   **연타는 같은 멱등 키**로 보낸다 — 그래야 `409` 가 아니라 영수증이다(K12).
5. **R6 · 세로 손잡이** = 시각 조정 → `PATCH`. **놓을 때 한 번만** 부른다.
   **회의 블록에는 손잡이를 붙이지 않는다**(§F).
6. **금지는 말로** (§I) — 거절 전부에 문구. 선례는 칸반의 `onInvalidMove`
   (`fe-survey-report.md` §7-3). **조용한 거절 0개.**
   기간 밖 문구에 **그 업무의 실제 기간**(= `span_from`~`span_to`)을 넣는다.
7. **K3 알림** — `schedule_release.released_count` 로
   「N건의 시간 배정이 기간 밖이라 해제되었습니다.」 **0건이면 아무 말도 하지 않는다.**
8. **WARN-A 를 닫는다 — 한 줄로 정한다.**

   > **뒤집힌 업무에서도 `start` 손잡이는 `start_date` 를, `end` 손잡이는 `due_date` 를 쓴다.
   > 띠 위에서 그 둘의 좌우가 바뀌어 보일 수 있다.**
   > **R1 의 「길이」는 span 길이**(`span_to - span_from`)다 — raw 차이가 아니다.

   **왜 이 쪽인가** — 손잡이의 **정체가 필드**여야 「왼쪽을 끌었는데 마감이 바뀐다」가
   **예측 가능**해진다. 화면 위치에 물리면 같은 손잡이가 업무마다 다른 필드를 바꾼다.
   **어느 쪽을 골라도 서버 계약은 한 값이고 할 수 있는 일도 같다**(검수 4차 WARN-A) —
   **고른다는 것 자체가 이 work 의 일**이다.

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make frontend-test` · `npx tsc --noEmit` **통과**.
- [ ] 상호작용 넷이 **실제 API 를 부른다**(목데이터가 아니다).
- [ ] **조용히 거절되는 자리가 0개**다 — 기간 밖 · 기한 없음 · 역전 · 담당 아님 전부 문구가 난다.
- [ ] 같은 날 재배정이 **`PATCH` 로 나간다** — `POST` 로 나가 `409` 를 보는 자리가 없다.
- [ ] 드래그 연타가 **`409` 를 띄우지 않는다**(같은 멱등 키 → 영수증).
- [ ] 기간을 줄이면 **「N건 … 해제되었습니다」**가 뜨고, 0건이면 **아무 말도 없다.**
- [ ] **WARN-A 의 한 줄이 코드와 테스트에 같이 있다** — 뒤집힌 업무에서
      `start` 손잡이를 끌면 **`start_date` 가** 바뀐다.
- [ ] **최종 `make verify` 통과** + `make test-postgres` 재통과.

## 검증 계획

**백엔드는 Makefile 타겟으로만 실행한다. `uv run pytest` 직접 호출 금지**(`AGENTS.md`).

| 단계 | 명령 | 언제 |
|---|---|---|
| 도메인·구조 | `make test-unit` | BE-1 · BE-2 |
| 외부 계약 | `make test-contract` | BE-1 · BE-2 |
| DB·제약·동시성 | `make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar` | **BE-1**(부분 unique 증명) · BE-2(회귀) · FE-2(최종) |
| 인벤토리 | `make test-unit` 안의 `tests/architecture/test_operation_inventory.py` | **BE-2** |
| 화면 | `make frontend-test` (**Node 20**) | FE-1 · FE-2 |
| 타입 | `cd frontend && npx tsc --noEmit` | FE-1 · FE-2 |
| 전체 | `make verify` | **FE-2 에서 한 번** |

**테스트 범위의 적정선** — Phase 마다 **그 Phase 가 바꾼 계약**을 돌린다.
**전량(`make verify`)은 FE-2 에서 한 번이다. 같은 스위트를 Phase 마다 반복하지 않는다.**

**하지 않을 것**

- 기존 테스트를 **편의상 삭제·skip·단언 약화** 하지 않는다. 깨지면 **계약이 바뀐 것인지
  구현이 틀린 것인지**를 먼저 가른다.
- `docs/unified-operations-inventory.json` **전체 재작성 금지** — diff 난 항목만.
- **과거 수치를 이번 통과 근거로 쓰지 않는다.** SPEC-004 는 스스로 「이번 작업에서 실행한
  테스트는 0건」이라고 적었다.
- **SQLite 선언을 제약의 증거로 쓰지 않는다.**

### 검증 책임의 경계

| 무엇 | 누가 |
|---|---|
| API 응답값·오류·권한·동시성·DB 제약 | **에이전트(자동)** |
| FE 단위 테스트·타입·빌드 | **에이전트(자동)** |
| **브라우저에서 눈으로 보는 것** — 배치·간격·문구·읽히는가 | **사용자(E2E)** |
| 통합 검증·PR | **코디네이터** |

**1루프는 계약을 세우는 판이다. 픽셀·간격·문구는 2루프가 잡는다** —
1루프에서 레이아웃을 완벽히 맞추려 시간을 쓰지 않는다.

### 사용자 E2E 인계 — FE-2 뒤에 넘길 것

| 시나리오 | 조작 | 기대 결과(눈으로) |
|---|---|---|
| E-1 | 월~수 업무를 월 10시 · 화 14시 · 수 9시에 배정 | 세 칸이 서고 **업무 기간이 안 바뀐다** |
| E-2 | 같은 업무를 **목요일**에 놓아 본다 | 「이 업무의 기간(…) 안에만 시간을 배정할 수 있습니다.」 — **조용하지 않다** |
| E-3 | 기한 없는 업무를 **시간 격자**에 놓아 본다 | 「먼저 업무 기간을 정해 주세요.」 |
| E-4 | 손잡이로 기간을 줄인다 | **「N건 … 해제되었습니다」**가 뜨고 그 배정이 사라진다 |
| E-5 | 기간을 **되돌린다** | 그 날이 **빈 채로** 돌아온다. **사람이 새로 넣는다** |
| E-6 | 그 업무를 **완료** → **재개** | 완료하면 통째로 빠지고, **재개하면 시간표가 통째로 돌아온다** |
| E-7 | 회의 카드를 끌어 본다 · 회의 블록의 세로 손잡이를 찾아본다 | **둘 다 안 된다 / 없다** |
| E-8 | 9/30~10/1 로 띠를 끈다 | **달 경계를 넘는다** |
| E-9 | 마감이 지난 업무를 **시작**한다 | **시간표가 사라지지 않는다**(K11 정규화) |
| E-10 | 드래그를 **연타**한다 | **오류 문구가 안 뜨고** 배정이 하나만 선다 |
| E-11 | 시안을 띄워 나란히 본다 (`cd "reference/2026-09-10-sc-meeting/package 2" && python3 -m http.server`) | 배치·간격 차이를 **2루프 목록**으로 적는다 |

## 인수조건 추적 — 어느 Phase 가 SPEC §6 의 어느 줄을 닫나

**SPEC-004 §6 인수조건은 14묶음 · 124줄이다. 전수 매핑한다 — 닫는 Phase 가 없는 줄은 없다.**

| # | 묶음 | 줄 수 | 닫는 Phase | 확인 방법 |
|---|---|---|---|---|
| A | 배정 만들기 (R1·R2·R5) | **13** | **BE-1**(서버 11줄) · **FE-2**(문구 2줄 — 기간 밖·기한 없음 안내) | `make test-contract` · FE-2 의 문구 테스트 |
| B | 하루 한 칸 (R5 · K1·K10) | **10** | **BE-1**(9줄) · **FE-2**(「정상 흐름에서 화면이 `409` 를 보지 않는다」 1줄) | `make test-contract` · `make test-postgres` · FE-2 |
| C | 회차 (K8) | **10** | **BE-1** | `make test-contract` · `make test-postgres`(동시성 2줄) |
| D | 시각 조정 (R6) | **5** | **BE-1**(`on_date` 거부 1줄) · **FE-2**(4줄 — 손잡이·역전 문구·자정·회의 손잡이 없음) | `make test-contract` · `make frontend-test` |
| E | 기간 이동·조정 (R1·R3·R4) | **7** | **FE-2** (서버는 기존 `PATCH /api/tasks` 계약 — 회귀) | `make frontend-test` · E2E |
| F | 사라지는 두 경로 — (가) 기간 밖 | **20** | **BE-2**(18줄) · **FE-2**(알림 문구 2줄) | `make test-contract` · `make test-postgres` |
| G | 사라지는 두 경로 — (나) 업무 종료 | **7** | **BE-1**(조회 필터 6줄) · **FE-2**(「이쪽은 알리지 않는다」 1줄) | `make test-contract` |
| H | 합본 조회 | **13** | **BE-1**(11줄) · **FE-1**(「서버 구간 = 화면 구간」·「띠와 드롭 가드가 같은 구간」 2줄) | `make test-contract` · `make frontend-test` |
| I | 회의 | **9** | **BE-1**(7줄) · **FE-1**(「캘린더에서 회의를 끌 수 없고 늘릴 수 없다」·「쓰기 명령을 안 보낸다」 2줄) | `make test-contract` · `make frontend-test` |
| J | 금지는 말로 (§I) | **2** | **FE-2** | `make frontend-test` · E2E |
| K | 화면 (§E·§J) | **12** | **FE-1**(10줄) · **FE-2**(「업무 만들기가 기존 모달」·「시안 목데이터 필드가 안 올라왔다」 2줄) | `make frontend-test` · `npx tsc --noEmit` · E2E |
| L | 표면 등록 (§J) | **8** | **BE-2** | `make test-unit`(`test_operation_inventory`·`test_local_stack_targets`) |
| M | 「선언했다」가 아니라 「선다」 | **7** | **BE-1** | **`make test-postgres`** — 이 줄들은 **다른 명령으로 닫히지 않는다** |
| N | 계층 (새 모듈을 만들 경우) | **1** | **BE-1** | `make test-unit`(`test_architecture`·`test_test_pyramid`) |
| | **합계** | **124** | | |

**Phase 별 부담**: BE-1 **약 60줄** · BE-2 **약 26줄** · FE-1 **약 14줄** · FE-2 **약 24줄**.

### 갈라지는 줄 — 어느 절반이 어느 Phase 인가

**한 줄이 두 Phase 에 걸치는 자리만** 따로 적는다. 나머지는 위 표의 묶음 단위로 닫힌다.

| SPEC §6 의 줄 | BE 절반 | FE 절반 |
|---|---|---|
| 「기간 밖 … **기간을 문구에 넣은 안내**가 나온다」 | 422 + 에러 코드 (BE-1) | 문구와 기간 표시 (FE-2) |
| 「**정상 흐름에서 화면이 `409` 를 보지 않는다**」 | `409` 를 내는 것 (BE-1) | `PATCH` 로 가는 것 (FE-2) |
| 「**서버가 낸 구간과 화면이 그리는 구간이 같다**」 | `span_from`·`span_to` (BE-1) | 그것으로 그리기 (FE-1) |
| 「그 구간이 **띠와 드롭 가드 양쪽에** 같이 쓰인다」 | — | 둘 다 (FE-1 띠 · FE-2 가드) |
| 「화면이 그 값으로 **「N건 …」** 를 내고 **0건이면 아무 말도 하지 않는다**」 | `released_count` (BE-2) | 문구 (FE-2) |
| 「**이쪽은 알리지 않는다**」 | 쓰기가 없음 (BE-1) | 문구를 안 냄 (FE-2) |

### WARN-A 가 더하는 인수조건 — **SPEC 밖에서 이 work 가 여는 한 줄**

- [ ] **뒤집힌 업무**(`start 9/6 · due 9/4`)에서 **`start` 손잡이를 끌면 `start_date` 가 바뀐다.**
      띠 위에서 그 손잡이가 **오른쪽 끝에 그려져도** 그렇다.
- [ ] R1 의 「길이 유지」가 **span 길이**(`span_to - span_from`)를 유지한다 — raw 차이가 아니다.

> **이 둘은 SPEC-004 §6 에 없다.** 검수 4차가 **WP 로 넘긴 WARN-A** 이고,
> **계약이 갈리지 않아 FAIL 이 아니었다**(서버는 한 값). 여기서 정하고 여기서 증명한다.
> **SPEC 을 고치지 않는다** — 필요해지면 SPEC 환류로 올린다.

## Pre-deploy Check

- [ ] **배포 직전 실제 데이터 DB 에서 제약 실재를 다시 확인한다.** Phase BE-1 의 격리 DB 통과는
      이 조건의 근거가 아니다 — `information_schema`·`pg_index` 에 **다시 묻는다.**
- [ ] `task_schedules` 표와 **부분 unique 가 실재**한다(없으면 만들었다).
- [ ] **`--sync` 의 `manual[]` 출력이 비어 있다** — NOT NULL 인데 기본값 없는 열이 남지 않았다.
- [ ] **코드 배포 전에 표가 먼저** 있다(스키마 → 코드).
- [ ] **기존 서비스 영향 없음** — 업무 생성·수정·시작·제안 동의·회의 화면이 그대로 돈다.
      **`GET /api/meetings` 가 `from`/`to` 없이 불리면 기존 응답 그대로**다.
- [ ] `docs/unified-operations-inventory.json` 의 `http_count` 가 **159**, `tool_count` 가 **129** 다.
- [ ] credential·env 를 새로 노출하지 않는다 (**이번에 추가한 외부 의존이 없다**).
- [ ] **운영·사용자 DB 초기화가 절차에 없다.**
- [ ] 응답에 **읽을 수 없는 업무·회의의 이름이나 건수**가 새지 않는다.

## Rollback

- **코드 롤백** — 배포 단위를 **BE-1(읽기·생성)** 과 **BE-2(닫기·대장)** 로 갈라 두었으므로
  BE-2 만 되돌릴 수 있다. 되돌리면 **기간이 바뀌어도 배정이 안 닫힌다** —
  **잘못된 상태가 아니라 옛 동작**이다.
- **표** — **되돌리지 않는 것이 기본이다.** 새 표이고 기존 코드가 모르므로 남아 있어도 무해하다.
  지우면 그 사이 사람이 짠 시간표가 **사라진다.**
- **인덱스** — 새 표와 함께 만들어졌다. 표를 남기면 인덱스도 남는다.
- **부분 revert 의 영향 범위** — BE-2 를 되돌리면 **정규화 구간 밖에 있는 배정이 화면에 남는다.**
  사람이 그것을 보고 **직접 지울 길이 없다**(삭제 경로가 없으므로 — `Open Issues`).
  **그 상태로 오래 두지 않는다.**
- **운영 대장** — 라우트를 되돌리면 `http_count` 도 되돌린다. **전체 재작성이 아니라 그 항목만.**

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-004 §6 인수조건 124줄 전항**이 「데이터: 에이전트」 칸까지 자동검증으로 확인됐다.
- [ ] **WARN-A 의 두 줄**이 코드와 테스트에 같이 있다.
- [ ] **부분 unique 가 살아 있는 PostgreSQL 에서 선다**가 **네 건**(있음·술어·거절·재배정)으로 남았다.
- [ ] `make verify` 와 `make test-postgres` 가 **수치와 로그**로 남았다.
- [ ] **운영 대장이 `http_count` 159 · `tool_count` 129** 로 통과했고 `acceptance_evidence` 가 보존됐다.
- [ ] **DS-gaps 8건 전부**가 「만들었다 / 만들지 않기로 했다」로 처분됐다.
- [ ] **브라우저 E2E 는 사용자가 수행**했고 그 결과가 기록됐다(**2루프의 시안 대조 포함**).
- [ ] **SPEC 환류 후보가 0건**임이 유지됐다 — 구현 중 새 외부 계약이 필요해지면
      **몰래 넣지 않고** SPEC 환류로 올렸다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **배정의 명시적 삭제가 없다** (DEC-003 보류 · SPEC-004 §7 의 「판단을 깔고 간 자리」).
  **월요일 배정만 빼고 업무 기간은 유지하고 싶을 때 길이 없다.**
  덮어쓰기(같은 날 재배정)와 기간 조정으로만 바뀐다. **이번 판에 열지 않는다** —
  **2루프의 사용자 E2E 에서 그 불편이 실제로 나오면 그때 연다.**
  ⚠ Rollback 이 BE-2 를 되돌리는 경우에도 이 구멍이 드러난다(위 §Rollback).
- **`_apply_proposal` 이 `validate_schedule` 을 안 지난다** (`be-survey-report.md` §8-5,
  「고치지 않고 보고한다」). **이 work 는 그 자리를 고치지 않고 K11 정규화로 덮는다.**
  고칠지는 별건이다 — 고쳐도 **시작 전이 경로(②)는 남는다**(전이 시점의 `today` 는 막을 값이 아니다).
- **상태 변경 아홉 경로가 흩어져 있다.** 이번 판은 읽기 필터라 안 걸리지만,
  **다음에 배정 쪽에 쓰기가 필요해지면 그 통합이 선행조건**이 된다 (DEC-003 보류).
- **회의 규칙을 뒤집는다** — 「공유받은 회의는 캘린더에 서지 않는다」가 **다른 SPEC 의 계약**인데
  그 원문이 우리에게 없다(K9). **회의 도메인 코드는 건드리지 않지만 관찰 가능한 동작 변경**이다.
  회의 화면 경로는 그대로다.
- **SPEC 환류 후보는 없다** — 구현 중 새 외부 계약이 필요해지면 **몰래 넣지 않고 환류로 올린다.**
  WARN-A 의 두 줄은 **SPEC 밖의 FE 층**이라 환류 대상이 아니다(SPEC §1 Scope Out 이 그 층을 WORK 로 보냈다).

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Decision / Baseline: (frontmatter 참조)
- 조사 리포트: `orchestration/work/strong-hajin-calendar/be-survey-report.md`(764줄) ·
  `fe-survey-report.md`(727줄) — **둘 다 코드 변경 0건**
- 검수 리포트: `orchestration/work/strong-hajin-calendar/review-spec-004-report.md`
  (1~4차 · 최종 **PASS**)
- 시안: `reference/2026-09-10-sc-meeting/package 2/` — **레이아웃 정본**
