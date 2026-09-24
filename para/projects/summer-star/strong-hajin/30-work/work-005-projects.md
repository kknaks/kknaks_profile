---
type: work
id: WORK-005
title: "W5 — 「프로젝트」 화면: 깊이를 자르지 않는 간트와, 일을 보내면 따라가는 사람"
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
updated_at: 2026-09-22
tags:
  - product/strong-hajin
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-004-projects|BASE-004]]"
  decisions:
    - "[[decision-004-projects|DEC-004]]"
  specs:
    - "[[spec-005-projects|SPEC-005]]"
    - "[[spec-004-calendar-scheduling|SPEC-004]]"
    - "[[spec-003-task-lifecycle-v2|SPEC-003]]"
    - "[[spec-001-work-management|SPEC-001]]"
  works:
    - "[[work-004-calendar-scheduling|WORK-004]]"
  releases: []
  related: []
---

# W5 — 「프로젝트」 화면: 깊이를 자르지 않는 간트와, 일을 보내면 따라가는 사람

업무는 **하나씩** 산다. 그 위에 **프로젝트 하나를 스코프로 잡는 읽기 화면** 하나를 얹는다 —
그 프로젝트의 업무들이 **어느 기간에 걸쳐 있고 무엇이 무엇보다 먼저인지**를 한 장으로 보이는 것이다.
그리고 그 화면이 드러낸 **도메인 버그 둘**을 같이 고친다 — 손자가 옛 프로젝트에 남는 것(어긋남 ③)과
업무는 프로젝트에 들어가는데 사람은 안 들어가는 것(어긋남 ④).

**만들지 않는 것**: 진행률 저장 컬럼 · 후행(역방향) 조회 API · 새 HTTP 라우트 · 새 MCP 도구 ·
새 오류 코드 · 프로젝트 상세의 필터·정렬·페이징 · 사이드바 변경 · `AppHeader` 슬롯 신설 ·
`ds/Empty` 글리프 크기 · `.design-sync/` 수정 · `member → lead` 승격 경로 · 프로젝트를 닫는 명령 ·
자료함 탭. **SPEC-005 §1 Scope Out 이 그 목록의 원장**이고, 여기서 다시 세지 않는다.
그 자리들은 **빠뜨린 것이 아니라 계약이 없거나 DEC-004 가 보류한 것**이다.

> 1 파일 = 1 work = **빌드 계획**. SPEC-005 의 외부 계약 본문은 복제하지 않고 절 이름으로 가리킨다.
> **이 work 는 계약을 다시 정하지 않는다** — 모순을 발견하면 고치지 않고 `Open Issues` 에 올린다.
> **저장 구조는 이 문서가 확정한다** — `20-spec/README.md` § Data / Domain Boundary 가
> column·index·FK·ORM·repository·migration 을 `30-work/` 의 `Domain / Schema` 절로 보냈다.

## Meta

- Spec reference: **SPEC-005**(**1730줄** — 2루프 개정 v0.2.0 · 2026-09-22 문서 검수 반영본.
  1루프 검수 시점은 1121줄이었다). 검수 1회(1루프) — **FAIL 4 · WARN 5** 가 나왔고
  **넷 다 반영된 뒤의 본문이 이 work 의 기준**이다(`review-spec-005-report.md`).
  반영 결과를 이 work 가 직접 확인했다: §2.9·§4 가 **외부 계약 넷 + `blocked` 는 M-6 승계**로 서 있고
  (FAIL-1), §4 에러 표가 **일곱 갈래**이며 이동 게이트가 **`WORK_PROJECT_LOCKED_BY_PREDECESSORS`** 이고
  (FAIL-2), 떼는 자리가 **넷**(`cancel_assignment` 포함)이며(FAIL-3 — 그 **넷째는 표면이 오늘
  없다.** 구현이 드러냈고 SPEC §4 가 그렇게 고쳐 적었다. **부를 수 있는 표면은 셋**이다),
  `(확정 — D-04/D-20/D-10)` 셋이 `(도출)`·`(제안)` 으로 내려와 있다(FAIL-4).
  WARN 다섯도 닫혀 있다 — OQ-601 은 §7 에서 닫혔고, §5 가 **「거는 자리는 application 메서드이지
  entrypoint 가 아니다」**를 박았고, `:878` 인수조건이 `may_manage` 로 관측 가능해졌고,
  §1 에 SPEC-003 과의 깊이 화해 문장이 섰고, `task_schedules` 표 이름이 빠졌다.
- Decision reference: **DEC-004** — 결정 **D-01 ~ D-39**(**39건** · 그중 **~~D-12~~ 는 D-28 로,
  ~~D-31~~ 은 D-39 로 대체** — **2026-09-22 정정 1건이 뒤에 붙었다**),
  **미결 4건**(OQ-604 ~ OQ-607). 철회 하나(「간트는 2단계까지」)는
  DEC-004 § 철회가 갖는다. **이 work 는 그것을 다시 세우지 않는다.**
- Baseline reference: **BASE-004** — 시안 관측 · 부품 재고 19항목 · DS 토큰 누락 0 · **어긋남 ①~⑤**.
- Covers spec: **SPEC-005 전절** — §2 UX 계약(2.1~2.9) · §3 S-1~S-12 ·
  §4 API/Request-Response/자동 초대/자동 해제/손자 종속/Validation/에러/Data Contract ·
  §5 Implementation Rules · §6 인수조건 **1루프 76줄 · 10묶음** + **2루프 52줄 · 7묶음**(**합 128줄**).
  **SPEC-003·SPEC-001·SPEC-004** 는 대체되지 않은 절이 **회귀 기준**이다 —
  상태 넷과 `blocked` 의 M-6 미결 · 전이표 · 상위/하위 · 중심 업무 판정 · 「진행률은 쓰지 않는다」 ·
  기한 경과일 `+N` · 기간을 읽는 네 경우와 `span_from`·`span_to` 라는 이름.
- Depends on work: **WORK-004(W4)** — 1루프 넷이 `DONE` 이고 **`modules/work/schedule.py` 의
  `task_span()` 이 그 판의 산물**이다. 이 work 는 그것을 **읽기만** 한다.
  W4 의 2루프(`BE-3`~`FE-4`)가 미완이어도 착수를 막지 않는다 — 겹치는 파일이 없다.
- Parallel work: **없다. 이 work 안에서도 BE 와 FE 가 병행하지 않는다** — §Execution 의 직렬 규칙.
- Follow-up work: `material_*` 병렬 격리의 **일반화**(Phase 0 가 그 자리다) · 어긋남 ②(필터·페이징) ·
  `member → lead` 승격 · 프로젝트를 닫는 명령 · `ds/GutterList` 개명 · 낡은 주석 정리(어긋남 ⑤-2·⑤-3).
- External dependency: **없다.** 외부 API·credential 을 새로 붙이지 않는다.
  격리 PostgreSQL(`POSTGRES_TEST_URL`)과 로컬 demo DB 만 쓴다.
- 루프 구조: **1루프는 코디네이터 자율(오늘) — BE-1 → BE-2 → FE-1 → FE-2 → FE-3.**
  **2루프는 사용자 동반(내일 오전) — Phase 0(`material_*` 병렬 격리)과 브라우저 E2E.**
  §Execution 이 그 경계를 그린다.
- **2026-09-22 · 2루프가 실제로 무엇이 됐나.** 위 서술은 **2루프를 열기 전의 계획**이다.
  **Phase 0 는 닫혔고**(`make verify` 가 **exit 0**, 코디 실측 2026-09-22),
  **브라우저 E2E 1차도 사용자가 돌렸다.** **그 1차가 지시 열한 건을 냈고** 그것이 2루프의 본체가 됐다 —
  원장은 `orchestration/work/strong-hajin-projects/loop2-backlog.md`(사용자 지시 11건 · B-9 는 코디 발견),
  **범위 판정과 비용 수치는 같은 폴더 `loop2-survey-report.md`**(다섯 질문 · 428줄)다.
  DEC-004 가 그것을 **D-28 ~ D-38** 로 내렸고 SPEC-005 가 **v0.2.0** 으로 받았다.
  **그래서 2루프의 Phase 는 셋이 더 붙는다 — BE-3 → FE-4 → FE-5.** §Execution — 2루프.
- **2루프의 계약 변경은 하나다** — **체크리스트·업무 내용의 읽기 범위**(SPEC-005 §4 「읽기 범위」 · D-29).
  나머지는 **게이트 한 줄 제거(D-28)와 화면 아홉**이다.
- **커밋은 아직 0건이다** — 1루프의 모든 변경이 **코드 워크트리에만** 있다(2026-09-22 확인).

### 착수를 막는 것과 막지 않는 것

| 무엇 | 착수를 막나 | 어디에 걸리나 |
|---|---|---|
| **`material_*` 계열이 병렬에서 흔들린다** — `make verify` 가 exit 0 를 못 볼 수 있다 | **아니다** | **§검증 계획의 기준선 분리 절차.** 원인 규명과 격리는 **Phase 0(2루프 · 사용자 동반)** 이다. 1루프는 **그 계열을 겨눈 테스트를 더하지도 고치지도 않고**, 회차별 기록만 남긴다 — **그 기록이 Phase 0 의 입력**이다 |
| **관리 모달의 시안이 없다** | **아니다** | **코디 자율로 정해졌다.** 지금 `ProjectPage.tsx:206-306` 의 참여자·이력·생성 UI 를 시안 `handoff/shell/js/work-modal.jsx` 의 **어휘**(`Modal`·`Field`·`TextField`·`AutoComplete`)로 옮긴다. **새로 발명하지 않는다** — §Phase FE-3 |
| **착수 전 기준선 측정** — `make test-contract` 1회와 실패 파일 집합 | **아니다** | **Phase BE-1 착수 전 한 줄.** 결정이 아니라 **확인 작업**이다 |
| **실행 PostgreSQL** | **아니다** | **Phase BE-2 의 검증**에 들어간다. 이번 판은 새 제약을 만들지 않으므로 **증명이 아니라 회귀**다 |
| **운영 대장의 어느 칸이 흔들리는가** | **아니다** | **테스트가 판정한다.** 이 work 가 미리 세어 둔 답은 §Domain / Schema 마지막 절에 있고, SPEC §5 와 갈리는 한 줄은 `Open Issues` 가 든다 |
| SPEC-003 의 `M-6`(`blocked` 미결) | **아니다** | **이 판이 열지 않는다.** 계약 넷을 승계하고 화면은 받은 값을 렌더한다 — SPEC-005 §2.9 |
| WORK-004 2루프(`K19`~`K24`) 미완 | **아니다** | 겹치는 파일이 없다. `task_schedules` 를 **읽지도 쓰지도 않는다** |

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | **1루프 다섯 DONE**(커밋 전 · 워크트리) · **Phase 0 DONE** · **브라우저 E2E 1차 DONE(사용자)** · **2루프 BE-3 · FE-4 · FE-5 TODO** |
| Branch/PR | `kknaksss/strong-hajin-projects` (코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`, base `origin/main` = `e46ce39`) |
| Blocker | 없음 — 위 표 |
| Next | **Phase BE-3 발주** — **BE 가 먼저다.** FE-4 · FE-5 는 **BE-3 의 실물 응답을 보고** 짠다 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위·보류 처분·사용자 질문 승격 | done |
| Design | kknaks | 시안 해석(레이아웃만) · 관리 모달 어휘 선택 | done |
| BE | `@sc-ax-be` | Phase BE-1 · BE-2 | todo |
| FE | `@sc-ax-fe` | Phase FE-1 · FE-2 · FE-3 | todo |
| QA | 코디네이터(자동) / 사용자(브라우저) | 자동 검증은 에이전트, 브라우저 E2E 는 사용자(2루프) | todo |
| Ops | kknaks | 스키마 적용 순서·rollback·배포 | todo |
| **Phase 0** | **사용자 + 에이전트(동반)** | **`material_*` 병렬 격리 — 원인 규명과 수정을 한 Phase 에** | **done (2026-09-22)** |
| **BE (2루프)** | `@sc-ax-be` | **Phase BE-3** — 게이트 제거(D-28) · 체크리스트 읽기 범위(D-29) | **todo** |
| **FE (2루프)** | `@sc-ax-fe` | **Phase FE-4**(간트 셋) → **Phase FE-5**(헤더·좌 레일·우 레일). **BE-3 뒤에 직렬** | **todo** |

## Scope

포함:

- **프로젝트 상세 `tasks[]` 의 확장** — 담당 · 체크리스트 집계 · 정규화 기간 · 기한 경과일 ·
  **외부 상태 투영** (SPEC §4 · 어긋남 ①)
- **자동 초대** — 요청 발송 · 담당 교체 제안이 받는 사람을 그 프로젝트에 `참여`로 붙인다
  (D-11 · ~~D-12~~ → D-28 · 어긋남 ④)
- **자동 해제** — 거절·철회면 **조건 둘을 모두 만족할 때만** 뗀다. **행을 지우지 않는다** (D-13~D-15)
- **손자 프로젝트 종속** — 상위를 옮기면 **자손 전체**가 따라가고 **이동 게이트도 자손 전체**에 걸린다
  (D-19 · 어긋남 ③). **화면이 아니라 도메인 버그 수정이다**
- **화면 재작성** — 3레일 등록 · 좌 레일(셀렉터 + 업무 카드 + 선택 상태) · 요약 스트립 5칸 ·
  **깊이 제한 없는 재귀 간트** · **접어도 안 사라지는 의존선** · 우 레일 · 관리 모달 · 빈 상태
  (D-05 · D-16~D-18 · D-20~D-23)
- **시안 CSS 이식** — `handoff/projects/css/projects.css` 를 화면 CSS 한 장으로.
  **`.scax-page-header__title-row` 한 줄은 버린다** (D-25)
- **기존 화면 테스트 단언 교체** — `ProjectPage.test.tsx` 7개 중 **6개**가 깨진다.
  기능이 모달로 옮겨가므로 **검사도 따라간다**
- **운영 대장 갱신** — 라우트 수·도구 수는 **불변**. 흔들리는 칸은 §Domain / Schema 가 센다
- **Phase 0 — `material_*` 병렬 격리** (**2루프 · 사용자 동반**)

제외:

- **진행률 저장 컬럼** — SPEC-001 이 배제한 이유를 뒤집지 않는다 (D-01)
- **후행(역방향) 조회 API·질의** — 프로젝트 범위에서 **역산이 완전**하다 (D-07)
- **새 HTTP 라우트 · 새 MCP 도구 · 새 오류 코드** — 전부 **0건** (SPEC §4)
- **업무 생명주기·상태 전이표** — SPEC-003 그대로. 이 화면은 상태를 **표시**만 한다
- **시간 배정** — SPEC-004 그대로. `task_schedules` 를 **읽지도 쓰지도 않는다**
- **프로젝트 상세의 필터·정렬·페이징** — 어긋남 ② (D-27). ⚠ D-16 이 여기에 전제를 건다
- **사이드바 · 내비 순서** — 건드리지 않는다 (D-26, 사용자 결정). 어긋남 ⑤-8 은 **기록만**
- **`AppHeader` 의 `titleEnd` 슬롯** — 더하지 않는다 (D-25). 등록만 하는 `actions` 는 포함이다(D-21)
- **`ds/Empty` 글리프 크기** — 20px 그대로 (D-24). 소비처 29곳을 흔들지 않는다
- **`ds/ProgressBar` 의 API 변경** — 소비처 1곳을 흔들지 않는다. 미터는 **화면 전용 클래스**로 만든다
- **`ds/GutterList` 개명** — 소비처 0건. 이름 충돌은 `Open Issues` 가 든다
- **`.design-sync/` 수정** — 거울이다 (D-10)
- **`member → lead` 승격 · 프로젝트를 닫는 명령 · 자료함 탭** — DEC-004 보류 / 시안 자신이 미룬 것
- **브라우저 E2E** — **사용자 담당(2루프).** 에이전트는 자동 검증까지

## Code Surface

- Repo / module: `toy_pr2/Strong_hajin` (SCAX modular monolith).
  워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`,
  브랜치 `kknaksss/strong-hajin-projects`, base `origin/main` = **`e46ce39`**.
  **조사 시점에 워크트리는 깨끗했다**(BE·FE 조사 2건 모두 `git status --porcelain` 공백 확인,
  이 work 작성 시점 재확인).
- 규약: `AGENTS.md` — 백엔드 테스트는 **Makefile 타겟으로만** · 프론트는 `make frontend-test` ·
  HTTP/MCP 시그니처를 바꾸면 `tests/architecture/test_operation_inventory.py` 가
  `docs/unified-operations-inventory.json` 과의 drift 를 잡는다
  (**전체 재작성 금지, diff 난 항목만 패치**).
- 경로는 워크트리 루트 기준 상대경로다. 줄 번호는 **조사 시점**의 것이고, 구현 전에 다시 연다.

### 이번에 만질 파일 — 조사 둘이 센 전수를 실행 목록으로

**백엔드**

| # | 파일 | 무엇을 | Phase |
|---|---|---|---|
| 1 | `backend/src/ax_workspace/modules/work/project_results.py` | **`ProjectTaskView` 에 필드를 더한다**(`:28-37`, 지금 6개). 「간트 연결선의 유일한 원천」 주석은 **그대로 둔다** | BE-1 |
| 2 | `backend/src/ax_workspace/modules/work/projects.py` | `get()` 의 `tasks` 조립(`:236-252`)이 새 값을 싣는다. `assign()`(`:145`)·`release()`(`:176`)는 **사람이 직접 쓰는 문이라 그대로** 두고, 자동 초대가 쓰는 **내부 경로**를 따로 세운다 | BE-1 · BE-2 |
| 3 | `backend/src/ax_workspace/platform/projects.py` | `tasks_in()`(`:204-209`) 곁에 **담당·체크리스트 집계를 한 번에 읽는 조회.** 업무마다 따로 묻지 않는다 | BE-1 |
| 4 | `backend/src/ax_workspace/modules/work/application.py` | `_external_state()`(`:2495-2506`)와 기한 경과일 계산(`:2521-2529`)을 **프로젝트 쪽도 지나게 한다.** `update()` 의 `children_of` 루프(`:532-536`)를 **자손 전체**로 | BE-1 · BE-2 |
| 5 | `backend/src/ax_workspace/modules/work/schedule.py` | **읽기만.** `task_span()`(`:40-62`)이 정규화 정본이다 — **다시 만들지 않는다** | BE-1 |
| 6 | `backend/src/ax_workspace/platform/work_tasks.py` | `children_of()`(`:475-482`)는 **직속만** 돈다. **자손 전체를 도는 조회를 곁에 세운다** — 기존 함수를 바꾸면 다른 소비처가 같이 움직인다 | BE-2 |
| 7 | `backend/src/ax_workspace/modules/work/assignments.py` | **붙는 자리 하나**(`reassign()` `:171`) · **떼는 자리 둘**(`decline()` `:276` · `cancel()` `:295`). **`assign()`(`:89`)에는 안 건다** — 그 경로의 업무에 프로젝트가 없다 | BE-2 |
| 8 | `backend/src/ax_workspace/modules/work/requests.py` | **붙는 자리 하나**(`create()` `:306`) · **떼는 자리 둘**(`reject()` `:466` · `withdraw()` `:657`) | BE-2 |
| 9 | `backend/src/ax_workspace/platform/persistence.py` | **자동 초대 흔적 한 칸씩** — `work_requests`(`:1636~`) · `task_assignments`(`:1752~`). 아래 §Domain / Schema | BE-2 |
| 10 | `backend/src/ax_workspace/bootstrap/application.py` | `_projects()`(`:4337-4340`) — **새 의존 조립은 여기서만.** `_assignments()`(`:3089`) · `_work_requests()`(`:4371`)도 같다 | BE-1 · BE-2 |
| 11 | `backend/src/ax_workspace/bootstrap/schema_sync.py` | **코드 수정 불필요.** `make sync-demo-schema` 가 **없는 컬럼만** 더한다 | — |
| 12 | `docs/unified-operations-inventory.json` | **`current_runtime.tools` 의 `get_project` 행 `output_schema` 한 칸.** `http_count` **159 불변** · `tool_count` **129 불변** · **`http_signature` 도 불변** — 근거는 §Domain / Schema 마지막 절 | BE-1 |
| 13 | `backend/tests/contract/` · `tests/unit/` | 계약·도메인 테스트. **RED 먼저.** 기존 파일 넷이 회귀 기준이다 — `test_projects.py` · `test_project_commands.py` · `test_task_predecessors.py` · `test_task_assignments.py` | BE-1 · BE-2 |
| 14 | `Makefile` | **`test-contract-serial` 타겟 한 줄** — 아래 §검증 계획. **격리 수단이 아니라 재실행 편의**다 | BE-1 |

**`backend/src/ax_workspace/entrypoints/http.py` 를 건드리지 않는다.**
**새 라우트가 0건**이고 핸들러 시그니처도 안 바뀐다 — `GET /api/projects/{project_id}` 는 여전히
`(project_id: UUID, principal: Principal) -> ProjectDetailResult` 다.
**`entrypoints/mcp.py` 와 `modules/ax_execution/tool_catalog.py` 도 그대로다** — 새 도구를 내지 않는다.

**프론트엔드**

| # | 파일 | 무엇을 | Phase |
|---|---|---|---|
| 15 | `frontend/src/App.tsx` | `pageProps`(`:352`)와 `<ProjectPage>`(`:515`)가 **`onRegisterRails` 를 넘기게** 고친다. 선례 `MyWorkPage.tsx:941-972` · `CalendarPage.tsx:460-477`. **셸은 이미 3칸 규약을 갖는다**(`AppShell.tsx:74-82`) | FE-1 |
| 16 | `frontend/src/features/project/ProjectPage.tsx` (333줄) | **재작성.** 좌 레일·본문·우 레일 등록과 **선택 축 하나**(`taskId`)를 든다 | FE-1 · FE-2 · FE-3 |
| 17 | `frontend/src/features/project/projectModel.ts` **(신규 · 순수 함수)** | **평면 `tasks[]` → 재귀 트리** · **후행 역산** · 요약 스트립 세기 · 하위 N. 선례 `features/work/workRows.ts` · `features/calendar/calendarModel.ts` | FE-1 · FE-2 |
| 18 | `frontend/src/features/project/` **(신규 부품들)** | 좌 레일 · 요약 스트립 · 간트 · 의존선 오버레이 · 우 레일 · 관리 모달 | FE-1 · FE-2 · FE-3 |
| 19 | `frontend/src/lib/viewModels.ts` | `ProjectDetail.tasks`(`:96-103`) 타입 확장. **`state: string` 을 `TaskState` 로 조인다** — 어긋남 ⑤-6 이 그 자리다 | FE-1 |
| 20 | `frontend/src/styles/projects.css` **(신규)** + `index.css:16-40` 에 `@import` 한 줄 | 시안 `handoff/projects/css/projects.css`(13,510바이트)를 옮긴다. **참조 토큰 중 저장소에 없는 것이 0개**다 | FE-1 · FE-2 · FE-3 |
| 21 | `frontend/src/features/project/ProjectPage.test.tsx` (179줄) | **7개 중 6개 단언 교체.** 관리 UI 검사는 **모달을 따라간다** | FE-3 |

**`frontend/src/lib/api.ts` 를 건드리지 않는다.** 이 화면이 쓰는 호출이 **전부 이미 있다** —
`listProjects`(`:793`) · `getProject`(`:797`) · `getProjectParticipationHistory`(`:801`) ·
`createProject`(`:805`) · `assignToProject`(`:814`) · `releaseFromProject`(`:818`) ·
`getTask`(`:158`) · `getMemberDirectory`(`:146`). **넓어지는 것은 응답 타입뿐**이고 그것은 #19 다.

**`src/ds/` 를 건드리지 않는다** — `Empty`(D-24) · `ProgressBar`(소비처 1곳) · `Select`(`trigger` prop 선례
`MyWorkPage.tsx:1410`) · `Badge` · `AppHeader`(D-25) 전부 **있는 그대로 쓴다.**
**미터는 화면 전용 클래스**(`.scax-pj-summary__track/__fill` · `.scax-pj-side__track/__fill`)로 만든다 —
시안이 그렇게 하고, `ds/ProgressBar` 는 `done`/`total` 을 받아 내부에서 % 를 계산해(`ProgressBar.tsx:18`)
**「% 를 그리지 않는다」(D-02)를 표현할 수 없다.**

### 2루프(D-28 ~ D-38)에서 만질 자리 *(2026-09-22)*

**1루프의 파일 목록을 다시 세지 않는다.** 아래는 **2루프가 새로 여는 자리**이고,
**줄 번호는 조사 시점(2026-09-22)** 의 것이다 — 구현 전에 다시 연다.

**백엔드 — Phase BE-3**

| # | 파일 | 무엇을 | 근거 |
|---|---|---|---|
| B1 | `backend/src/ax_workspace/modules/work/projects.py` | **자동 초대의 게이트 한 줄을 뺀다** — `join_for_assignment()` 첫 줄(`:230`). **`may_assign_in` 의 정의(`:494`)는 남긴다** — 다른 소비처가 쓴다 | **D-28** |
| B2 | `backend/src/ax_workspace/modules/work/assignments.py` | **`plan_project_work()`(`:171`)는 건드리지 않는다** — 「그 프로젝트에 업무를 올릴 자격」은 **다른 규칙**이다. **여기까지 빼면 문이 하나 더 열린다** | **D-28**(범위 경계) |
| B3 | `backend/src/ax_workspace/modules/work/application.py` | **체크리스트를 싣는 조건**(`:940-943` 부근) — 「활성 배정을 쥐었나」에 **「그 업무의 프로젝트에 붙어 있나」를 더한다.** **접근 값은 `owner`/`read_only` 그대로 둔다**(SPEC-005 §4 ⓑ). 프로젝트 판정은 **이미 있는 것**(`_may_read_beyond_holding()` `:1111-1118`)을 쓴다 — **새 질의를 만들지 않는다** | **D-29** |
| B4 | `backend/src/ax_workspace/modules/work/task_results.py` | **쓰지 않는다(확인만)** — `checklist`·`checklist_progress` 가 **선택 필드**인 것은 그대로다. **타입은 안 바뀌고 실리는 조건만 바뀐다** | **D-29** |
| B5 | `backend/tests/contract/test_project_membership_follows_work.py` | **`:121-159` 의 주장이 뒤집힌다** — **이름·docstring·`:148` 단언을 다시 쓴다.** **삭제·skip 금지.** 이웃 둘(`:460-476` · `:170-188`)은 **그대로 통과해야 한다**(회귀) | **D-28** |
| B6 | `backend/tests/contract/` (체크리스트 읽기) | **RED 먼저.** 같은 프로젝트의 남의 업무에서 **항목이 온다** · **쓰기는 여전히 거절된다** · **프로젝트 밖에서는 안 온다** | **D-29** |

**`entrypoints/http.py` · `mcp.py` · 운영 대장을 건드리지 않는다** —
**새 라우트 0건 · 새 도구 0건 · 시그니처 불변**이고 **응답 «타입»도 안 바뀐다**(선택 필드가
실리는 «조건»만 바뀐다). ⚠ **대장이 흔들리는지는 테스트가 판정한다** — 흔들리면 **그 항목만 패치**한다.

**프론트엔드 — Phase FE-4 · FE-5**

| # | 파일 | 무엇을 | Phase |
|---|---|---|---|
| F1 | `frontend/src/styles/projects.css` | **간트 쪽**: 라벨 칸 고정 선언 + **z-index · 배경**. **우 레일·헤더 쪽**: 제목·소제목 색 · 메타 표 정렬선·행 높이 · 버튼 시인성 · 완료 바 fill 투명도. **한 장이라 두 Phase 가 같이 만진다 — 그래서 직렬이다** | FE-4 · FE-5 |
| F2 | `frontend/src/features/project/ProjectGantt.tsx` | 머리줄 **축 스페이서 요소 하나** · 스크롤 컨테이너 **ref** 와 첫 진입 `scrollLeft`. **좌표계·의존선·행 위치·접힘은 안 건드린다** | FE-4 |
| F3 | `frontend/src/features/project/ProjectRail.tsx` | **헤더를 한 줄로**(아이콘 + 「프로젝트」 + 건수 배지 · 오른쪽 끝 셀렉터) · **선택된 카드로 스크롤**하는 자리 | FE-4(스크롤) · FE-5(헤더) |
| F4 | `frontend/src/features/project/ProjectPage.tsx` | 헤더 `actions` 에 **「프로젝트 추가」 등록**(**게이트가 없다** — 2026-09-22 정정 · ~~D-31~~ → **D-39**) · 생성 모달 상태 · **빈 상태 갈래에서도 헤더를 세운다** — 오늘 `noProjects` 갈래는 **레일을 안 세우고**(`:230-235`) **`Empty` 만 그리는 이른 반환**(`:292-298`)이라 **그 두 자리가 같이 바뀐다.** ⚠ **헤더 등록 `useEffect`(`:280-290`)는 훅이라 이른 반환보다 먼저 돈다** — 자리는 이미 있다. 상태 전이 뒤 **프로젝트 상세와 업무 상세를 다시 읽는 자리**도 여기다 | FE-5 |
| F5 | `frontend/src/features/project/` **(신규 — 생성 모달)** | **네 칸**(이름 필수 · 설명 · 시작일 · 종료일). **`external_key` 칸을 만들지 않는다 — API 가 못 받아서가 아니라 화면이 «안 내기로» 해서다**(SPEC-005 §2.10 · OQ-607). 어휘는 관리 모달과 같은 것 | FE-5 |
| F6 | `frontend/src/features/project/ProjectTaskPanel.tsx` | **블록 순서 넷** · **「업무 정보」 신설**(설명 + 체크리스트) · **상태 드롭다운** · 버튼 시인성 | FE-5 |
| F7 | `frontend/src/features/work/WorkModals.tsx` **(읽기만)** | **셋을 «가져다 쓴다»** — 허용 전이 계산(`allowedTaskTransitions`) · **막힘 사유(`BlockReasonPrompt`)** · 완료 보고(`CompletionReportModal`). 셋 다 이미 export 돼 있다. **그 파일을 고치지 않는다** — 고치면 업무 화면이 함께 움직인다. **diff 0줄이 완료 판정**이다 | FE-5 |
| F8 | `frontend/src/features/project/ProjectPage.test.tsx` | 2루프가 여는 단언을 **더한다.** 1루프 단언은 **회귀 기준**이다 | FE-4 · FE-5 |
| **F9** | **`frontend/src/App.tsx`** **(신규 — 2루프 검수가 잡은 자리)** | **게이트가 읽을 값을 화면에 넘긴다.** 오늘 `ProjectPage` 는 `pageProps`(`personaId` · `onError` · `onRegisterRefresh`)만 받고(`:363` · `:532-537`) **역량 값을 못 받는다.** 넘길 것은 **하나**다 — **`canManageOwnTasks`(`task.self_manage`)**(상태 드롭다운 게이트 · **D-32**). **2026-09-22 정정 — 전에는 둘이었다**: ~~**`project.manage`**(생성 버튼 게이트 · D-31)~~ 는 **안 넘긴다.** ~~D-31~~ 이 뒤집혀 **D-39** 가 **그 게이트를 없앴다**(SPEC-005 §2.10 · §5 — 「게이트가 읽는 세션 값은 «하나»다」). **FE 가 코드에서 먼저 걷어냈다** — `App.tsx` 의 `canCreateProjects={has("project.manage")}` 한 줄과 `ProjectPage.tsx` 의 prop·분기 전부(`loop2-final-fix-report.md` §A-2). ⚠ **상태 드롭다운의 게이트(`task.self_manage`)는 안 움직인다** — 뒤집힌 것은 **생성 버튼 쪽 하나**이고, 이 행이 남는 이유가 그것이다. **다른 화면에 넘기는 값을 바꾸지 마라** — `sharedWorkProps` 를 통째로 넘기면 `ProjectPage` 의 계약이 넓어진다. **새 조회를 만들지 마라** — 값은 이미 세션 봉투에 있다(`:71` `session?.capabilities` · `:354` `has()`) | FE-5 |

⚠ **`App.tsx` 는 다섯 화면이 공유한다** — 그래서 **더하는 것만 한다**: `ProjectPage` 호출부에
**역량 두 값을 넘기는 것**이 전부이고, **다른 화면에 넘기는 값도 `sharedWorkProps` 자체도 안 바꾼다.**
**이 파일이 2루프 목록에 없던 것이 검수 FAIL-6 였다** — 워커가 「발주서 밖 파일」을 만나
멈추거나 조용히 만지는 자리였다.

**`src/ds/` 를 여전히 한 줄도 안 고친다** — `Select` 의 트리거 교체는 **그 부품이 이미 가진 길**이고,
**완료 바 색은 화면 CSS 에서 낮춘다**(D-35 — 토큰을 고치면 다른 화면이 흔들린다).

**FE 를 둘로 쪼갠 이유 — 그리고 그래도 직렬인 이유**

- **쪼갠 이유**: **검수 축이 다르다.** FE-4 는 **CSS 고정과 스크롤 좌표**(눈으로 보는 것이 전부)이고,
  FE-5 는 **새 모달 · 새 블록 · 기존 전이 로직 재사용**(계약과 분기가 걸린다).
  한 Phase 로 묶으면 **「간트가 안 보인다」와 「드롭다운이 안 뜬다」가 한 리뷰에 섞인다.**
- **그래도 직렬인 이유**: **`projects.css` 는 한 장이고 `ProjectRail.tsx` 를 둘 다 만진다**
  (FE-4 는 **선택된 카드로 스크롤**하는 자리를, FE-5 는 **그 헤더**를).
  1루프가 세운 규칙(「같은 코드 워크트리를 공유하므로 병행하면 서로를 덮는다」)이 **그대로 산다.**
- **그리고 둘 다 BE-3 뒤다** — **사용자 지시**이자 **D-29 가 응답을 바꾸기 때문**이다(§Dependency).

### 공유 자산 — 건드리면 다른 화면이 흔들린다

**이 표의 자산을 고치지 않는다. 깨지면 우리가 규약을 어긴 것이다.**

| 자산 | 무엇이 걸리나 | 이 work 의 처분 |
|---|---|---|
| `.scax-inbox-card` (`components.css:111-121`) | 수신함(`InboxRail.tsx:59-71`)·캘린더(`ScheduleCard.tsx:42-99`)가 같이 쓴다 | **`--selected`·hover·focus 규칙을 화면 CSS 안에서 화면 범위로 한정한다** **(제안)**. 공유 파일에 무조건 규칙으로 얹으면 두 화면에 새 CSS 가 붙는다 |
| `.scax-gutter-list` (`components.css:105-108`) | 같은 둘이 쓴다. 헤더가 **32px 고정**(`:106`) | 시안이 `.scax-gutter-list__header--sub` 로 `min-height:auto` 를 더한다(`projects.css:3`) — **그 modifier 도 화면 CSS 에** 둔다 |
| `.project-layout` 반응형 (`components.css:692-693`) | **`.dashboard-columns`·`.report-grid` 와 같은 규칙에 묶여 있다** — 홈·보고가 같이 움직인다 | **그 줄을 손대지 않는다.** 옛 `.project-*` 클래스는 `screens-a.css:231-260` 에서 걷어내되 이 줄은 **선택자에서 이름만 뺀다** |
| `.screens-b-lead` | 조직(`OrgPage.tsx:352`)·관계 탐색·보고가 쓴다. 검사도 걸려 있다(`OrgPage.test.tsx:249-251`) | 프로젝트 화면에서 **쓰지 않게 될 뿐** 규칙을 고치지 않는다 |
| `api.listProjects` | 업무 만들기 모달의 프로젝트 셀렉터가 같은 호출을 쓴다(`WorkModals.tsx:3672,4538`) | **호출을 고치지 않는다** |
| `tests/architecture/test_architecture.py` · `test_operation_inventory.py` · `test_test_pyramid.py` | 도메인이 `fastapi`·`sqlalchemy` 를 import · `*Application` 을 `bootstrap/application.py` 밖에서 조립 · 대장 drift · 순수 도메인 등재 | **편집하지 않는다.** 새 순수 도메인 모듈을 만들면 `PURE_DOMAIN_MODULES` 에 **한 줄 등재**한다 |

### 계약이 닿는 입구 — 전수

| 표면 | 이번에 |
|---|---|
| `GET /api/projects/{project_id}` | **`tasks[]` 응답 필드가 는다.** 라우트·시그니처·상태 코드는 그대로 |
| `GET /api/projects` · `GET /api/tasks/{task_id}` · `/participation-history` · `POST /api/projects` · `POST|DELETE /api/projects/{project_id}/members` | **그대로.** 화면이 쓰기만 한다 |
| `POST /api/work-requests` | **자동 초대 한 겹** (붙는 자리 #1) |
| `POST /api/tasks/assign` | **안 바뀐다** — 그 경로로 태어난 업무에 **프로젝트가 없다**(아래 「세어서 뺀 자리」) |
| `POST /api/tasks/{task_id}/reassign` | **자동 초대 한 겹** (붙는 자리 #2) |
| `POST /api/work-requests/{request_id}/reject` · `/withdraw` | **자동 해제 한 겹** (떼는 자리 #1·#2) |
| `POST /api/task-assignments/{assignment_id}/decline` | **자동 해제 한 겹** (떼는 자리 #3) |
| `POST /api/action-items/{action_item_id}/commands/cancel_assignment` | **안 바뀐다 — 이 표면은 떼는 자리 #4 에 닿지 않는다.** 그 봉투는 AX `task.assign` 제안 위에만 서고(`platform/actions.py:539` · `modules/actions/policy.py:136`), 그 초안은 **`project_id` 가 언제나 `None`** 이다(`modules/work/drafts.py:33`). **자동 해제는 메서드(`cancel()`)에 건다** — 아래 「거는 자리」 |
| `PATCH /api/tasks/{task_id}` (프로젝트 이동) | **게이트와 전파가 자손 전체로** (D-19) |
| MCP | **도구 수 그대로.** `get_project` 의 **응답 스키마**만 넓어진다 |
| AX 실행 경로 | **없다.** 이 화면은 읽기 화면이다 |

### 거는 자리 — **라우트가 아니라 application 메서드다**

**SPEC §5 가 못 박은 자리다.** 같은 명령이 **세 입구**로 들어온다 —
HTTP(`entrypoints/http.py`) · **MCP**(`entrypoints/mcp.py` 의 `task.assign`·`task.reassign`) ·
**action-center 명령**(`POST /api/action-items/{id}/commands/{command}` → `platform/action_center.py`
가 `self._assignments.cancel(...)` 를 부른다).

> **HTTP 라우트에만 걸면 MCP 로 들어온 배정이 조용히 초대를 안 한다.**
> **어느 입구로 들어와도 같은 메서드를 지나므로, 거기 한 번 걸면 셋이 다 덮인다.**

| 붙는/떼는 | 거는 메서드 |
|---|---|
| 붙는 #1 요청 발송 | `modules/work/requests.py` `WorkRequestApplication.create()` (`:306`) |
| 붙는 #2 담당 교체 제안 | `modules/work/assignments.py` `TaskAssignmentApplication.reassign()` (`:171`) |
| 떼는 #1 요청 거절 | `requests.py` `reject()` (`:466`) |
| 떼는 #2 요청 철회 | `requests.py` `withdraw()` (`:657`) |
| 떼는 #3 배정 거절 | `assignments.py` `decline()` (`:276`) |
| 떼는 #4 배정 철회 | `assignments.py` `cancel()` (`:295`) — docstring 이 「Withdraw a direct assignment before the assignee answers it」다. ⚠ **이 메서드에 닿는 표면이 오늘 없다**(SPEC §4 넷째). **건다** — 표면이 생기면 그대로 돈다 |

**공통 지점에 걸지 않는다.** 거기 걸면 「배정인가」를 스스로 판정해야 하고 **틀리면 조용히 안 돈다** —
SPEC-004 §5 와 WORK-004 의 `touch()` 판단이 같은 결이다.

### 세어서 뺀 자리 — 일곱. 여기에는 안 건다

| 표면 | 왜 |
|---|---|
| **`POST /api/tasks/assign`** (직접 배정, `assign()` `:89`) | **그 업무에는 프로젝트가 없다.** `create_assigned_task()` 가 만드는 `TaskRecord` 에 **`project_id` 가 인자에도 본문에도 없고**(`platform/work_tasks.py:2413-2455`), 그것이 실수가 아니라 **의도**다 — `TaskAssignmentInput` 이 **non-null `project_id` 를 명시적으로 거부하고**(`modules/work/task_creation.py:118-126`) 주석이 「A non-null project is not owned by assignment creation and must not be silently ignored by the executor」라고 적는다. 부모의 프로젝트를 물려받는 `project_for()` 도 **지나지 않는다**(`application.py:360-367` · `assignments.py:121-135`). 그래서 **언제나 `project_id = NULL`** 이고, 「업무에 프로젝트가 없으면 아무 일도 일어나지 않는다」에 **항상** 걸린다 |
| `POST /api/projects/{project_id}/tasks` (`plan_project_work()` `assignments.py:138`) | docstring 이 **「사람은 아직 정하지 않는다」**라고 적는다 — 받는 사람이 없다 |
| `POST /api/tasks` | 자기 업무다. 지명되는 사람이 없다 |
| `POST /api/task-assignments/{assignment_id}/accept` (`accept()` `:228`) | **붙는 시점이 아니다.** 멱등이라 아무 일도 안 한다 |
| `POST /api/tasks/{task_id}/proposals` · `/respond` · `/withdraw` | **조건 변경 제안은 날짜·조건**이다. 담당이 아니다 |
| `POST /api/projects/{project_id}/members` | **사람이 직접 붙이는 기존 문**이다. 자동이 아니다 |
| `GET /api/task-assignment-candidates` (`candidates()` `:71`) · `GET /api/task-assignments/sent` (`sent()` `:224`) | 읽기다 |

## Domain / Schema

`20-spec/README.md` § Data / Domain Boundary 가 column·index·FK·ORM·repository·migration 을
**여기로 보냈다.** SPEC-005 는 밖으로 드러나는 것만 갖는다. **실제 모양은 이 절이 확정한다.**

### 지금 코드에 있는 것

- 표 **91개**(`persistence.py`, `__tablename__` 기준). 이 판이 닿는 것은 **다섯** —
  읽는 넷 `tasks`(`:907~`) · `projects`(`:838-861`) · `project_assignments`(`:864-894`) ·
  `task_checklist_items`(`:1097-1118`), 그리고 **흔적을 남길 한 곳** `task_assignments`(`:1752~`).
  **`work_requests` 는 안 건드린다**(아래).
- **마이그레이션 체계가 없다.** 스키마 정본은 `Base.metadata` 이고 `bootstrap/reset.py:20` 의
  `create_all()` 이 새로 만들며, `schema_sync`(= `make sync-demo-schema`)가
  **없는 표를 만들고 없는 컬럼만 더한다** — 지우지도 타입을 바꾸지도 않는다.
  손 `.sql` 은 **기존 표에 인덱스를 더할 때**만 필요하고, **이번엔 없다**.
- `project_assignments` 에 **떼는 데 필요한 것이 이미 다 있다** —
  `ended_at` · `ended_by_member_id` · `end_reason`, 그리고 부분 unique
  `uq_project_assignment_active (project_id, member_id) WHERE ended_at IS NULL`(`:871-880`).
- `tasks.parent_task_id` 가 **자기참조 FK 이고 `index=True`**(`:937`) — 자손 전체를 도는 반복 조회가
  그 인덱스를 탄다.

### 새로 필요한 것 — **컬럼 하나. 표는 하나도 안 는다**

**진행률도 후행도 하위 집계도 저장하지 않는다** (D-01·D-07 · SPEC §4 「싣지 않는 것」).
저장이 느는 것은 **D-14 조건 ① 을 세우기 위한 한 가지 사실**뿐이다.

```text
task_assignments                                ← 기존 표
  auto_project_join   Boolean  NULL             ← 이 배정이 받는 사람을 그 프로젝트에 새로 붙였나
```

**한 표로 족한 이유 — 요청 발송도 배정 행을 만든다.** 요청을 보내면 업무와 **함께**
`TaskAssignmentRecord` 가 선다 — `assignment_kind="request_effect"` · `status="pending"` ·
**`source_work_request_id=request.id`**(`platform/work_tasks.py:1938-1957`).
**붙는 자리 둘이 전부 배정 행을 세우므로 흔적도 그 한 곳에 선다**, 그리고
**요청 유래인지는 `source_work_request_id` 로 안다.**

**결정과 그 근거.**

| 무엇 | 결정 | 근거 |
|---|---|---|
| **왜 한 칸이 필요한가** | 붙이는 명령은 **이미 붙어 있으면 새 행을 만들지 않는다**(`projects.py:163-165`). 그래서 「이 요청이 붙였나」의 구분은 **붙이는 그 순간에만 설 수 있다** — 나중에 되돌아보면 원래 멤버와 구별할 수 없다 | **(확정 — D-14)** |
| **왜 한 표인가** | **붙는 자리 둘이 전부 배정 행을 만든다** — 요청 발송은 `request_effect`·`pending` 행을(`platform/work_tasks.py:1938-1957`), 담당 교체 제안은 `direct`·`pending` 행을(`:2327-2328`) 세운다. **떼는 자리 넷이 전부 그 행에 닿는다**: `decline()`·`cancel()` 은 그 행 자체를 받고, 요청 거절·철회는 **`source_work_request_id` 로 그 행을 찾는다.** 나누면 **한쪽 문으로 닫았을 때 흔적을 못 찾는다** — 실제로 요청 발송이 세운 `pending` 행은 `decline()` 로도 닫힌다(`assignments.py:318-350` 이 `assignment_kind` 를 안 가린다). **D-14 의 「한 칸이 는다」와 그대로 맞는다** | **(도출 — 코드 사실)** |
| **왜 nullable 인가** | `schema_sync` 는 **NOT NULL 인데 `server_default` 가 없는 열**을 「사람이 결정할 것」으로 `manual[]` 에 내놓는다. 기존 행은 **전부 이 판 이전**이라 「이 요청이 붙였다」가 **거짓인 것이 사실**이고, 비어 있음을 그대로 「아니다」로 읽으면 된다 — **`manual[]` 을 비운 채로 들어간다** | **(제안)** · WORK-004 §Migration 의 같은 판정 |
| **인덱스** | **만들지 않는다.** 이 칸은 **그 행을 이미 손에 쥔 뒤**에만 읽힌다(거절·철회는 대상 행을 잠그고 시작한다). 그리고 **기존 표에 인덱스를 더하면 `schema_sync` 가 못 만들어 손 migration 이 하나 는다** — `work_requests.project_id` 주석(`persistence.py:1651-1652`)이 그 이유를 이미 적는다 | **(도출)** |
| **CHECK** | **박지 않는다.** 불변식이 아니라 **한 순간의 사실 기록**이다 | **(제안)** |
| **`project_assignments` 변경** | **없다.** `ended_at`·`end_reason` 이 이미 있고 부분 unique 도 이미 있다 | **(도출 — D-13)** |
| **`tasks` 변경** | **없다.** 담당은 **조인**이고(D-08 이 「분류」를 뺐다), 진행률은 **저장하지 않는다**(D-01). **기간 정규화·기한 경과도 계산이지 열이 아니다** — 다만 **그것을 정한 결정은 없다** | 담당·진행률 **(확정 — D-01·D-08)** / 기간 정규화·기한 경과 **(도출 — SPEC-005 §4 Data Contract)** — SPEC 자신도 기한 경과일을 `(도출)` 로 적고 「D-04 는 이 값을 정한 적이 없다」고 명시한다 |
| **`projects` 변경** | **없다.** 집계를 저장하지 않는다 | **(도출)** |
| **새 표** | **0개** | **(도출)** |

### Aggregate 경계와 불변식

- **프로젝트 참여(`project_assignments`)는 프로젝트의 자식**이다. 자동 초대·자동 해제는 그 aggregate 를
  **업무 쪽 명령의 부수 효과로** 건드린다 — 그래서 **같은 트랜잭션**이어야 한다(아래).
- **`auto_project_join` 은 배정의 자식**이다. 그 행이 죽으면 같이 죽는다. 참여 쪽에 두지 않는 이유가
  그것이다 — 참여는 **여러 요청이 공유**할 수 있다.
- **불변식 넷**

  | # | 불변식 | 누가 답하나 | 동시 요청 둘이 오면 |
  |---|---|---|---|
  | 1 | **한 사람은 한 프로젝트에 활성 참여 하나** | **데이터베이스** — `uq_project_assignment_active` | **둘째가 거절된다.** 틈이 없다 |
  | 2 | **선행은 같은 프로젝트 안에서만 선다** | **application** — `_resolve_predecessors()`(`application.py:1116-1158`) + **이동 게이트** | 이동 게이트가 자손 전체를 보므로 **이 판이 틈을 좁힌다** |
  | 3 | **자동 해제는 조건 ①·② 가 둘 다 참일 때만** | **application** — 조건 ② 는 「다른 활성 업무」를 세는 조회다 | **둘이 동시에 거절되면 둘 다 「다른 활성 업무 있음」을 볼 수 있다** → 아무도 안 떼어진다. **틈이 남는다**(아래) |
  | 4 | **참여 이력의 행을 지우지 않는다** | **application** — 닫기만 있고 삭제 명령이 없다 | 해당 없음 |

- **⚠ 불변식 3 의 한계를 감추지 않는다.** 같은 사람에게 보낸 업무 둘이 **동시에** 거절되면,
  둘 다 상대의 활성 업무를 보고 **아무도 안 뗀다.** **결과는 「사람이 프로젝트에 남는 것」**이고,
  그것은 **참여가 잘못 사라지는 것보다 안전한 쪽**이다. **DB 제약으로 올릴 수 없다** —
  「다른 활성 업무가 있나」는 두 표(`tasks`·`task_assignments`)에 걸친 세기다.
  WORK-004 의 「겹침 금지」가 만난 것과 **같은 모양의 한계**다.
- **트랜잭션 경계는 요청 하나다.**
  - **붙이는 것과 그 명령이 한 트랜잭션** — 나뉘면 「업무는 갔는데 사람은 안 붙은」 상태가
    **복구 경로 없이** 남는다 (SPEC §5).
  - **떼는 것과 그 종결이 한 트랜잭션** — 나뉘면 「거절은 됐는데 참여는 남은」 상태가 남는다.
  - **자손 전체 이동도 한 트랜잭션** — 나뉘면 **지금의 버그를 다른 모양으로 다시 만드는 것**이다.

### 자손 전체를 도는 법 — **반복이다. 재귀 CTE 가 아니다**

| 무엇 | 결정 | 근거 |
|---|---|---|
| 방법 | **BFS 반복** — `children_of()` 를 깊이마다 부르고 **본 것을 다시 보지 않는다** | 저장소에 **선례가 있다** — `_require_no_predecessor_cycle()`(`application.py:1169-1187`)이 활성 변을 같은 방식으로 걷고, 그 주석이 「**본 것을 다시 보지 않는다** — 원장이 이미 어긋나 고리가 있어도 무한히 걷지 않는다」고 적는다 |
| 왜 재귀 CTE 가 아닌가 | SQLite 와 PostgreSQL 둘 다에서 도는 SQL 을 **이 저장소가 아직 한 번도 안 썼다.** 깊이가 실무에서 서너 층이라 **왕복 수가 문제가 아니다** | **(제안)** |
| 기존 `children_of()` | **고치지 않는다.** 다른 소비처가 「직속만」을 전제한다 — **자손 전체를 도는 조회를 곁에 세운다** | **(도출)** |
| 고리가 있으면 | **본 것을 다시 보지 않으므로 멈춘다.** 부모 순환은 `parent_for()` 가 이미 막지만(`:401-405`), **원장이 이미 어긋난 경우에도 무한히 걷지 않는다** | 위 선례와 같은 규율 |
| 게이트를 거는 순서 | **자손 전체를 먼저 다 모으고, 전부에 `_require_project_unlocked()` 를 건 뒤에 옮긴다.** 걸으면서 옮기면 **부분 이동**이 생긴다 | **(도출 — 게이트의 뜻 · SPEC-005 §4)** — D-19 에 그 문장은 없다. SPEC-005 도 같은 사실을 `(도출)` 로 적는다 |

### 담당·체크리스트 집계를 어떻게 싣나 — **업무마다 묻지 않는다**

| 무엇 | 어디서 오나 | 규칙 |
|---|---|---|
| **담당** | `task_assignments` 의 **활성 행** — `tasks` 의 열이 아니다(`persistence.py:911-913`) | **그 프로젝트의 업무 전부를 한 번에** 조인한다. 투영 규칙은 기존 `_assignment_view()`(`application.py:2532-2551`)와 **같은 말**이어야 한다 — `status=="active"` 를 먼저 찾고, 없으면 기다리는 행 |
| **체크리스트 집계** | `task_checklist_items` 를 `task_id` 로 묶어 **`done`/`total` 두 수**. 항목은 **안 싣는다** | 집계 계산이 **두 곳에 있으면 조용히 갈린다** — 업무 상세의 `checklist_progress` 와 **같은 규칙**을 쓴다 |
| **정규화 기간** | `modules/work/schedule.py` 의 **`task_span()`**(`:40-62`) | **이름도 SPEC-004 와 같다** — `span_from`·`span_to`. **새 함수를 만들지 않는다** |
| **기한 경과일** | `application.py:2521-2529` 의 계산 | **「오늘」이 두 곳에서 판정되면** 목록의 `+N` 과 요약 스트립의 「지연」이 다른 수를 낸다 |
| **외부 상태 투영** | `_external_state()`(`application.py:2495-2506`) | **어긋남 ① 의 뿌리는 `ProjectApplication` 이 `work.application` 을 import 하지 않는다는 것**이다. 그래서 **같은 판정을 두 번 쓰지 않는 자리로 내린다** — 순수 함수로 두든 공유 모듈로 두든, **투영이 두 벌이 되면 어긋남 ① 을 다른 모양으로 다시 만드는 것**이다. 새 순수 도메인 모듈을 만들면 `PURE_DOMAIN_MODULES` 에 한 줄 등재한다 |

> **N+1 을 만들지 마라.** `tasks_in()` 은 지금 필터도 페이징도 없이 그 프로젝트의 업무 **전부**를 낸다
> (어긋남 ②). 그 배열의 각 줄마다 담당·체크리스트를 따로 물으면 **업무 수만큼 질의**가 된다.
> 선행 배열이 이미 그 모양으로 한 번에 온다 — `predecessors_for([...])`(`projects.py:229-231`).
> **같은 결로 두 벌을 더한다.**

### 운영 대장 — **흔들리는 칸을 세어 두었다**

이 work 가 인벤토리와 그 drift 테스트를 직접 읽고 센 결과다. **테스트가 최종 판정자**이고,
아래는 **무엇이 흔들릴지 미리 아는 것**이다.

| 칸 | 이번에 | 근거 |
|---|---|---|
| `current_runtime.http_count` | **159 불변** | 새 라우트 0건 |
| `current_runtime.tool_count` | **129 불변** | 새 도구 0건 |
| `http` 행의 `http_signature` | **불변** | `test_inventory_includes_each_declared_http_operation` 이 비교하는 것은 **핸들러의 어노테이션 문자열**이다. `GET /api/projects/{project_id}` 는 여전히 `(project_id: UUID, principal: Principal) -> ProjectDetailResult` — **`ProjectTaskView` 안에 필드를 더해도 이 문자열이 안 바뀐다** |
| `http` 행의 `http_handler`·`http_application_calls` | **불변** | 핸들러 이름도 application 호출도 그대로 |
| **`current_runtime.tools` 의 `get_project` 행 `output_schema`** | **바뀐다** | `test_inventory_schemas_match_the_actual_registered_tools`(`tests/architecture/test_operation_inventory.py:104`, 비교 자리 `:122`)가 도구의 **`output_schema` 를 통째로 비교**한다. 현재 그 스키마 안에 **`ProjectTaskView` 와 `preceding_task_ids` 가 실재**한다 — 필드를 더하면 그 자리에서 깨진다 |
| 그 밖 도구 | **불변** | `list_projects`·`project_list` 의 스키마에는 `ProjectTaskView` 가 **없다** |

- **갱신 방법: 테스트 실패 diff 의 그 항목만 패치한다. 전체 재작성 금지**(`AGENTS.md`).
  `acceptance_evidence` 를 **보존**한다.
- ⚠ **SPEC §5 는 「프로젝트 상세 행의 서명이 바뀐다」고 적는다.** 실제로 바뀌는 것은
  **MCP `get_project` 의 응답 스키마**다. **계약은 안 갈린다 — 가리키는 자리만 다르다.**
  `Open Issues` 가 그것을 든다.

### Migration 기술안 — 이 레포에 실제로 있는 도구로만

1. `persistence.py` 의 `TaskAssignmentRecord` 에 `auto_project_join` 을 선언한다.
   **`WorkRequestRecord` 는 안 건드린다** — 흔적은 한 칸이다(§Domain / Schema).
2. `make sync-demo-schema`(= `python -m ax_workspace.entrypoints.reset_demo --sync`)를 돌린다.
   **기존 표에 없는 컬럼을 더하는 것**이라 `schema_sync` 가 그대로 처리한다.
3. `plan()` 의 **`manual[]` 출력이 비어 있어야 한다.** 비어 있지 않으면 그 열이 NOT NULL 인데
   기본값이 없다는 뜻이다 — **nullable 로 두기로 한 이유가 그것**이다.
4. **손 `.sql` 이 필요 없다.** 그것은 **기존 표에 인덱스를 더할 때**만 필요하고, 이번엔 없다.
5. **운영 적용**: 컬럼 추가라 `CONCURRENTLY` 가 필요 없다. 다만 **코드 배포 전에 컬럼이 먼저** 있어야 한다
   (§Pre-deploy Check).
6. **`reset_demo` 안전 장치를 우회하지 않는다** — `require_safe_demo_database()` 가
   host 와 db 이름을 **연결 전에** 본다.

### 2루프(D-28 ~ D-38)는 **저장 구조를 바꾸지 않는다** *(2026-09-22 · 확인 완료)*

**표도 컬럼도 인덱스도 안 는다. 마이그레이션도 없다.** 세 자리를 확인했다.

| 무엇 | 왜 저장이 안 바뀌나 |
|---|---|
| **체크리스트 읽기 범위**(D-29) | **응답 투영의 문제다.** 항목도 집계도 **이미 저장돼 있고**, 바뀌는 것은 **「누구에게 실어 보내나」** 하나다. 판정에 쓰는 프로젝트 소속도 **이미 있는 표**(`project_assignments`)와 **이미 있는 판정**을 쓴다 — **새 칸이 필요 없다** |
| **자동 초대 게이트 제거**(D-28) | **조건 한 줄이 사라지는 것**이다. 붙일 때 남기는 흔적(`task_assignments.auto_project_join`)은 **1루프가 세운 그 칸 그대로**이고, **붙는 사람이 늘어도 그 칸의 뜻이 안 바뀐다** |
| **프로젝트 만들기**(D-30 · ~~D-31~~ → **D-39**) | **기존 표면·기존 입력·기존 표**다. 화면이 **이미 받는 네 칸을 처음으로 다 쓰는 것**뿐이다 |
| **화면 아홉**(D-32 ~ D-38) | **CSS 와 컴포넌트**다. `tasks[]` 도 **안 넓힌다**(D-38) |

**그래서 `make sync-demo-schema` 도, 배포 직전 컬럼 실재 확인도 2루프에는 없다** —
**1루프의 그 절차가 커버하는 컬럼 하나가 마지막이다.**
⚠ **응답 «타입»도 안 바뀐다** — `checklist`·`checklist_progress` 는 원래 **선택 필드**이고,
**실리는 조건만** 넓어진다. 운영 대장이 흔들리는지는 **테스트가 판정한다.**

## Dependency

| 무엇 | 상태 |
|---|---|
| **WORK-004 (W4)** | 1루프 넷 `DONE`. **`task_span()` 이 그 판의 산물**이고 이 work 는 **읽기만** 한다. W4 2루프 미완이 착수를 막지 않는다 — 겹치는 파일이 없다 |
| **SPEC-005** | `status: draft`. 검수 FAIL 4 반영 완료. **계약 변경이 필요해지면 몰래 넣지 않고 환류로 올린다** |
| 실행 PostgreSQL | **Phase BE-2 검증에 필요.** `POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_projects` — **이번 작업 전용 DB** |
| Node 20 | `make frontend-test` 가 요구한다. Node 25 에서는 jsdom localStorage 오류가 난다(W2 기록) |
| 시안 | `reference/2026-09-10-sc-meeting/package 2/` 의 `Projects.html` + `handoff/projects/` — **레이아웃 정본.** 기능 정본이 아니다 |
| 관리 모달의 어휘 | `handoff/shell/js/work-modal.jsx` — `Modal`·`Field`·`TextField`·`AutoComplete`. **시안이 없는 화면에 어휘만 빌린다** |
| 디자이너 | **없다.** 간트·의존선은 우리가 만든다 (DEC-004 · BASE-004 § 부품 재고) |
| **`material_*` 병렬 격리** | ~~선행이 아니다 — 같은 slug 의 Phase 0 이고 2루프다~~ → **2026-09-22 닫혔다.** `make verify` 가 **exit 0** 를 낸다(코디 실측). **이제 기준선 분리가 아니라 「실패 0」이 조건이다**(§검증 계획) |

**2026-09-22 · 2루프의 의존 — BE 가 FE 의 선행이다.**

| 무엇 | 상태 |
|---|---|
| **Phase BE-3 → Phase FE-4 → Phase FE-5** | **직렬이다. 병렬로 두지 않는다.** **사용자 지시(2026-09-22)**: 「api 필요한 거는 백엔드 먼저 하고 fe 돌리자, **계약이 제대로 안 되서 서로 충돌 나더라**」 |
| **왜 BE 가 먼저인가** | **D-29(체크리스트·업무 내용의 읽기 범위)가 FE 가 받는 응답을 바꾼다.** 같은 프로젝트 사람이 남의 업무를 골랐을 때 **항목이 오느냐 안 오느냐**가 우 레일의 분기를 가른다 — **추정으로 짜면 그 분기가 틀린다.** **FE 는 BE-3 이 닫힌 뒤 실물 응답을 보고 짠다** |
| **BE-3 이 닫히면 무엇을 넘기나** | **실제 API 응답 예시**(같은 프로젝트의 남의 업무 1건 · 프로젝트 밖 읽기 1건)를 **FE 브리프에 박는다.** 1루프의 BE-2 → FE 규칙과 같다 |
| **FE-4 와 FE-5 도 직렬이다** | **같은 코드 워크트리를 공유한다** — 1루프가 세운 그 규칙(「병행하면 서로를 덮는다」)이 그대로 산다. 아래 「FE 를 둘로 쪼갠 이유」 |
| **D-29 의 실물 응답** | **FE-5 의 선행**이다. FE-4(간트)는 응답에 안 걸리지만 **순서를 앞당기지 않는다** — 워크트리가 하나다 |
| **Phase 0** | **닫혔다.** `make verify` exit 0 가 **2루프의 기준선**이다 |

## Internal Interface Contract

**BE 가 내는 것과 FE 가 쓰는 것을 같은 단위에서 닫는다.** 다만 **이 work 는 직렬**이라
FE 는 BE 가 닫힌 뒤에 소비를 붙인다 — 아래는 **무엇이 짝인지**를 못 박는 표다.

| # | BE 가 내는 것 | FE 가 쓰는 것 | 짝 |
|---|---|---|---|
| I-1 | `tasks[]` 의 **담당** — 사람 식별자 + 표시 이름. **담당 없는 업무가 정상**이라 **비어서 온다** | 좌 레일 카드 meta 의 **「분류」를 뺀 자리** · 간트 이름줄 · 우 레일 하위 카드. **비면 그 칸을 비운다 — 「미정」을 지어내지 않는다** | BE-1 ↔ FE-1·FE-2·FE-3 |
| I-2 | `tasks[]` 의 **체크리스트 집계** — 완료 수 · 전체 수 | 간트 바의 % · 우 레일 미터. **전체 수가 0 이면 fill 도 % 도 그리지 않는다** — **0% 가 아니다** | BE-1 ↔ FE-2·FE-3 |
| I-3 | `tasks[]` 의 **정규화 기간** — **`span_from`·`span_to`, SPEC-004 와 같은 이름·같은 규칙** | 간트 바의 양 끝. **화면이 정규화를 다시 하지 않는다** — 한쪽만/뒤집힘/없음을 서버가 이미 접었다 | BE-1 ↔ FE-2 |
| I-4 | `tasks[]` 의 **기한 경과일** — **끝난 업무에는 값이 안 온다**(`_overdue_days()` 가 `done`·`cancelled`·`completion_submitted` 에 `null` 을 낸다, `application.py:2521-2529`) | 요약 스트립 **「지연」** 칸. **화면이 「오늘」을 따로 판정하지 않는다** — **값이 온 업무만 센다** | BE-1 ↔ FE-1 |
| I-5 | `tasks[]` 의 **외부 상태 투영** — `completion_submitted` 가 **접혀서** 나간다 | 좌 레일 배지 · 간트 바 색 · 요약 스트립. **라벨·톤을 못 찾는 값을 안 만난다** | BE-1 ↔ FE-1·FE-2 |
| I-6 | `tasks[]` 의 **`preceding_task_ids`** — **서버는 이미 낸다**(`get_project` 도구 스키마에 실재). 깊이와 무관하게 **손자까지 평평하게 전부** | **의존선의 유일한 원천**이자 **후행 역산의 재료**. **후행을 서버에 묻는 호출이 0건**. ⚠ **FE 타입에는 없다** — `viewModels.ts:95-102` 의 `ProjectDetail.tasks` 는 여섯 필드뿐이고 `features/project` 에서 읽는 코드가 **0건**이다. **FE 타입은 새로 더한다**(FE-1 작업 8) | **서버 기존 ↔ FE 신규** · FE-1 → FE-2·FE-3 |
| I-7 | **`may_manage`**(기존) | 관리 모달 손잡이를 그릴지. **화면이 권한을 추측하지 않는다** | 기존 ↔ FE-3 |
| I-8 | **자동 초대·자동 해제의 관측면** — `GET /api/projects`(셀렉터에 뜬다/사라진다) · `/participation-history`(닫힌 줄이 남는다) | **새 화면 조작이 없다.** 관리 모달의 참여 이력이 그 결과를 **보여줄 뿐**이다 | BE-2 ↔ FE-3 · 사용자 E2E |
| I-9 | **프로젝트 이동의 거절** — **`WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409)**, 기존 코드 그대로 | **이 화면에는 이동 조작이 없다.** 드로어가 그 명령을 갖는다 — **화면이 내는 새 거절이 0건** | BE-2 ↔ (없음) |

> **I-3 이 특히 한 단위여야 한다.** WORK-004 의 3차 검수 FAIL 이 바로 그 자리였다 —
> 서버가 `[9/4, 9/6]` 으로 받는 날을 화면이 `[9/6, 9/6]` 으로 막았다.
> **같은 사실을 두 규칙으로 읽지 않는다** — 이 판도 같은 이름으로 같은 값을 받는다.

## Execution

각 Phase 의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나다.
Phase 별 `완료 판정`이 완료 조건이다.

### 단계 순서 — **직렬이다**

```text
1루프 (코디 자율 · 오늘)
   Phase BE-1 ──▶ Phase BE-2 ──▶ Phase FE-1 ──▶ Phase FE-2 ──▶ Phase FE-3
      │              │              │              │              │
      └ 리뷰·재수정   └ 리뷰·재수정   └ 리뷰·재수정   └ 리뷰·재수정   └ 리뷰·재수정

2루프 (사용자 동반 · 내일 오전)
   Phase 0 (`material_*` 병렬 격리)   +   브라우저 E2E
```

- **BE 가 닫히기 전에 FE 를 태우지 않는다.** 같은 코드 워크트리를 공유하므로 병행하면 서로를 덮는다.
- **BE 를 둘로 가른 이유** — **BE-1 이 FE 전부의 선행**이다. 화면의 모든 칸이 그 배열에서 나온다.
  **BE-2 는 화면이 없어도 서는 도메인 수정**이고, 거기서 막혀도 **BE-1 이 인질이 되지 않는다.**
- **FE 를 셋으로 가른 이유** — FE-2(간트·의존선)가 **이 판의 가장 어려운 자리**다.
  FE-1 이 틀과 데이터 배선을 닫아 두면 FE-2 가 **좌표 계산 하나에만** 집중한다.
- **백엔드 커밋이 들어가면 API 를 반드시 다시 띄운다**
  (config `rules.restart_api_after_backend_commit`). 옛 코드가 떠 있으면 **「프론트가 안 된다」로 보인다.**
- **BE-2 검수 통과 후 실제 API 계약(응답 예시)을 FE 브리프에 박는다** — 추정으로 쓰지 않는다.
- 워커가 못 정하는 것이 나오면 **코디가 결정**하고 `Open Issues` 에 남긴 뒤 루프에 복귀한다.
  **조용히 정하지 않는다.** **계약이 필요해지면 SPEC 환류로 올린다.**

---

### Phase BE-1 — 프로젝트 상세 `tasks[]` 확장 + 상태 투영

- **Status**: TODO
- **닫는 SPEC 인수조건**: **상태 어휘 2줄**(승인 대기가 `done` 으로 나온다 · 같은 업무가 두 표면에서
  같은 값) · **진행률 1줄**(진행률 저장 컬럼이 늘지 않았다) · **간트와 트리 중 BE 절반 2줄**
  (한쪽 날짜만 · 뒤집힌 기간). 자세한 배정은 §인수조건 추적.
- **근거 결정**: **D-01**(진행률은 체크리스트에서) · **D-02**(없으면 % 없음 — 서버가 0 을 낸다) ·
  **D-04**(전체 진행률의 재료) · **D-06**(상태는 백엔드가 정본) · **D-08**(담당은 활성 배정이 답한다) ·
  **D-09**(기간 정규화는 서버가) · **BASE-004 어긋남 ①**.
- **설명**: 화면의 모든 칸이 이 배열에서 나온다. **여기까지가 「그릴 재료가 다 왔다」**다.

**작업**

0. **착수 전 기준선 (읽기 전용)** — `make test-contract` 를 **한 번** 돌리고
   **통과/실패 수와 실패 «파일 집합»** 을 기록한다. 코드를 아직 한 줄도 안 고친 상태다.
   결과를 `orchestration/work/strong-hajin-projects/flaky-baseline-projects.md` 에 **회차 1** 로 남긴다.
   **여기서 아무것도 고치지 않는다.** ← 이 기록이 **내일 Phase 0 의 입력**이다.
1. `modules/work/project_results.py` 의 `ProjectTaskView` 에 필드를 더한다 —
   **담당 · 체크리스트 집계 · 정규화 기간 · 기한 경과일**. 실을 것과 안 실을 것은 SPEC §4 가 세어 두었다.
   **하위 집계·후행·「분류」·담당 여부 플래그·승인 값은 안 싣는다.**
2. **상태 투영을 지나게 한다** — `modules/work/projects.py:244` 의 `"state": task.state` 가
   원값을 그대로 낸다. `_external_state()` 와 **같은 판정**을 지나게 한다.
   **투영이 두 벌이 되면 어긋남 ① 을 다른 모양으로 다시 만드는 것**이다 (§Domain / Schema).
3. `platform/projects.py` 에 **담당·체크리스트 집계를 한 번에 읽는 조회** 둘을 더한다.
   `predecessors_for([...])` 와 **같은 결**이다. **업무마다 따로 묻지 않는다.**
4. **기간은 `task_span()` 을 부른다**(`modules/work/schedule.py:40-62`). **새 함수를 만들지 않는다.**
   **이름도 `span_from`·`span_to` 로 SPEC-004 와 같게 낸다.**
5. **기한 경과일도 서버가 낸다** — `application.py:2521-2529` 와 같은 값. 화면이 「오늘」을 재판정하지 않는다.
6. `bootstrap/application.py:4337-4340` `_projects()` — **새 의존 조립은 여기서만.**
7. **운영 대장** — `docs/unified-operations-inventory.json` 의 **`current_runtime.tools` 에서
   `get_project` 행의 `output_schema` 만** 패치한다. `http_count` **159**·`tool_count` **129**·
   `http_signature` **전부 불변**. **전체 재작성 금지.**
8. `Makefile` 에 **`test-contract-serial` 타겟**을 더한다 —
   `FILES` 로 받은 계약 테스트를 **`-n0`**(직렬)로 돈다.
   **`-p no:randomly` 는 넣지 않는다** — 이 저장소에 `pytest-randomly` 가 **설치돼 있지 않아서**
   (`backend/pyproject.toml` dev 그룹은 `httpx`·`pytest`·`pytest-xdist` 셋뿐 · `uv.lock` 0건)
   **무해한 무동작**이기 때문이다. 실효 스위치는 **`-n0` 하나**다.
   **격리 수단이 아니다** — `-n auto` 를 끄는 스위치이고, `material_*` 를 가르는 타겟이 **아니다.**
   그 결정은 **Phase 0 몫**이다.
9. 계약 테스트 — **RED 먼저.** `tests/contract/test_projects.py` 에 새 필드의 계약을 세운다.

**하지 말 것**

- **진행률을 저장하지 마라** (D-01). 응답 어디에도 저장된 % 가 없어야 한다.
- **하위 집계를 서버가 내지 마라** (SPEC §4). 화면이 센다 — 서버가 또 내면 **원천이 둘이 된다.**
- **후행 배열을 만들지 마라** (D-07).
- **`tasks_in()` 에 필터·페이징을 넣지 마라** (D-27). ⚠ **D-16 이 여기에 전제를 건다** —
  간트가 깊이 제한 없이 그리려면 **그 프로젝트의 업무가 전부 한 응답에 실려야 한다.**
- **`entrypoints/http.py` 를 건드리지 마라.** 라우트도 시그니처도 안 바뀐다.

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] **회차 0(기준선) 기록이 남았다** — 통과 수 · 실패 수 · **실패 파일 집합**.
- [ ] `make test-unit`(= `test_operation_inventory` 포함) **통과**.
- [ ] `make test-contract` 를 돌리고 **회차 1 기록**을 남겼다. **새로 든 실패 파일이
      기준선 밖에 없다** — 있으면 그것이 이번 변경 탓이고 고친다.
- [ ] **이번 판이 더한 계약 테스트를 직렬로 따로 돌려 전부 통과를 보였다**
      (`make test-contract-serial FILES="tests/contract/test_projects.py"`).
- [ ] `curl` 로 `GET /api/projects/{project_id}` 가 **실물 응답**을 낸다 —
      담당이 실리고(없는 업무는 비어 있고) · 체크리스트 집계 두 수가 실리고 ·
      `span_from`·`span_to` 가 정규화돼 있고 · 기한 경과일이 있고 ·
      **승인 대기 업무의 `state` 가 `done`** 이다.
- [ ] **같은 업무를 `GET /api/tasks/{task_id}` 로도 불러 `state` 가 같다.**
- [ ] `docs/unified-operations-inventory.json` 의 diff 가 **`get_project` 도구 한 행**이내다.
      `http_count` 159 · `tool_count` 129 · `acceptance_evidence` **보존**.
- [ ] **커밋 후 API 를 다시 띄웠다.**

---

### Phase BE-2 — 소속과 참여의 정합: 손자 이동 · 자동 초대 · 자동 해제

- **Status**: TODO
- **닫는 SPEC 인수조건**: **핵심 넷 중 3줄**(프로젝트 밖 사람 초대 · 거절하면 떼어짐 · 상위를 옮기면
  손자까지) · **자동 초대 7줄** · **자동 해제 10줄** · **손자 프로젝트 종속 5줄** = **25줄**.
- **근거 결정**: **D-11**(자동 초대, 사용자 결정) · ~~**D-12**(열쇠는 배정 권한)~~ →
  **D-28**(배정이 성립하면 붙는다 — **2026-09-22 뒤집힘**. 이 Phase 는 **1루프의 기록**이고,
  게이트를 빼는 일은 **Phase BE-3** 이 한다) ·
  **D-13**(거절·철회면 뗀다, 사용자 결정) · **D-14**(조건 둘) · **D-15**(수락 뒤엔 안 뗀다) ·
  **D-19**(손자도 프로젝트에 종속, 사용자 결정) · **BASE-004 어긋남 ③·④**.
- **설명**: **화면이 없어도 서는 도메인 수정**이다. 이 화면이 드러냈을 뿐 이미 일어나고 있는 일이다.
  **여기까지가 「일을 보내면 사람도 따라간다」**다.

**작업**

1. **저장 — 컬럼 하나** (`task_assignments.auto_project_join`, §Domain / Schema 그대로). `make sync-demo-schema` → **`manual[]` 이 비어 있는지** 확인.
2. **자손 전체를 도는 조회**를 `platform/work_tasks.py` 에 세운다 —
   **`children_of()` 를 고치지 않고 곁에.** **BFS 반복 · 본 것을 다시 보지 않는다.**
3. **프로젝트 이동을 자손 전체로** — `application.py:532-536` 의 루프를 바꾼다.
   **자손 전체를 먼저 다 모으고, 전부에 `_require_project_unlocked()` 를 건 뒤에 옮긴다.**
   **부분 이동이 없다.** 거절은 **`WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409), 기존 코드 그대로**다 —
   **`WORK_PREDECESSORS_UNFINISHED` 를 끌어오지 않는다.** 그것은 **전이 게이트**이고
   이 판이 **건드리지 않는다.**
4. **자동 초대를 붙는 자리 둘에** — `requests.py:306`(요청 발송) · `assignments.py:171`(담당 교체 제안).
   **application 메서드에 건다. entrypoint 가 아니다.**
   - **`assign()`(`:89`)에는 안 건다** — 그 경로로 태어난 업무에 **프로젝트가 없다**
     (§세어서 뺀 자리). 걸어도 **언제나 무동작**이고, 「붙는 셋」으로 세면 **닫을 수 없는 테스트**가 생긴다.
   - 열쇠는 **`may_assign_in`**(`projects.py:299-300`)이다. **`project.manage` 를 요구하지 않고
     넓히지도 않는다.**
   - 붙이는 관계는 **`member`**. **`lead` 로 붙이지 않고 승격도 하지 않는다.**
   - **이미 붙어 있으면 아무 일도 일어나지 않는다**(멱등). 그때 `auto_project_join` 은 **거짓**이다.
   - **업무에 프로젝트가 없으면 아무 일도 일어나지 않는다** — 오류가 아니다.
   - **새 거절 갈래 0건.** 배정 자체가 막히면 **기존 배정 거절이 먼저 난다.**
5. **자동 해제를 떼는 자리 넷에** — `requests.py:466`·`:657` · `assignments.py:276`·`:295`.
   ⚠ **넷 중 `cancel()`(`:295`) 에는 닿는 표면이 오늘 없다**(SPEC §4 넷째) —
   `cancel_assignment` 봉투가 서는 제안의 초안이 **`project_id` 를 언제나 `None`** 으로 박는다
   (`modules/work/drafts.py:33` · `modules/actions/policy.py:136` · `platform/actions.py:539`).
   **그래도 건다** — **부를 수 있는 표면은 셋**이고 넷째는 **메서드까지 서 있다가 문이 나는 날 돈다.**
   - **흔적은 `task_assignments.auto_project_join` 한 칸이다.** 요청 거절·철회는
     **`source_work_request_id` 로 그 배정 행을 찾아** 읽는다 — `work_requests` 에 칸을 두지 않는다.
   - **요청 발송이 세운 `pending` 행은 `decline()` 로도 닫힌다** —
     `pending_for()`·`_pending_target()` 이 `assignment_kind` 를 **안 가린다**
     (`work_tasks.py:2490-2497` · `assignments.py:318-350`). **그 길로 닫아도 같은 칸을 읽으므로 그대로 돈다.**
   - **조건 ①·② 가 둘 다 참일 때만.** 철회라고 느슨해지지 않는다.
   - **참여를 닫는다** — `ended_at` + `end_reason`. **행을 지우지 않는다.**
   - 사유는 **「요청 거절」·「요청 철회」 둘뿐**이다. **셋째를 만들지 않는다** —
     배정 쪽 거절은 「요청 거절」을, 배정 쪽 철회는 「요청 철회」를 **그대로 쓴다.**
   - **수락 뒤 취소·완료로는 안 뗀다** (D-15).
6. **붙이는 것·떼는 것과 그 명령을 한 트랜잭션**에 둔다.
7. **계약 테스트** — 붙는 자리 **둘** · 떼는 자리 **넷**(배정 거절은 **요청 유래 행과 담당 교체 제안 행
   둘 다**를 겨눈다) · 조건 ①·② 의 거짓 경우 둘 · 손자 이동 ·
   자손 잠김 거절. **RED 먼저.**
   - **재는 층이 갈린다** — 떼는 자리 **셋**(요청 거절 · 요청 철회 · 배정 거절)은 **실제 라우트를 지나고**,
     **넷째(배정 철회)는 `TaskAssignmentApplication.cancel()` 을 직접 부른다.** **표면이 없기 때문**이고,
     **없는 표면을 테스트가 증명할 수는 없다.**
   - 그 메서드 테스트의 docstring 에 **왜 메서드로 재는지와 표면이 없다는 사실**을 적는다 —
     **표면이 생기면 이 테스트가 그 표면으로 올라온다.**

**하지 말 것**

- **`project.manage` 를 넓히지 마라** (~~D-12~~ → **D-28** — 결론은 그대로다.
  D-28 은 **게이트를 뺀 것**이지 권한을 **준** 것이 아니다). 넓히면 **참여자 붙이기/떼기 전체가 열린다.**
- **참여 이력 행을 지우지 마라** (D-13). 「붙었다가 거절로 떨어졌다」도 **일어난 일**이다.
- **새 오류 코드를 만들지 마라.** 자동 초대·자동 해제 둘 다 **새 거절 갈래가 0건**이고,
  조건이 안 맞으면 **거절이 아니라 무동작**이다.
- **`children_of()` 자체를 자손 전체로 바꾸지 마라.** 다른 소비처가 「직속만」을 전제한다.
- **동시성 틈을 감추지 마라** — 조건 ② 는 application 이 답하고 **DB 제약으로 못 올린다**
  (§Domain / Schema 불변식 3). **「한 사람 한 참여」와 같은 세기의 보장이 아니다.**
- **자손 전체 이동을 여러 트랜잭션으로 쪼개지 마라** — 지금 버그를 다른 모양으로 다시 만드는 것이다.

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make sync-demo-schema` 의 **`manual[]` 출력이 비어 있다.**
- [ ] `make test-unit` · `make test-contract` — **회차 2 기록**을 남겼고 **새로 든 실패 파일이
      기준선 밖에 없다.**
- [ ] **이번 판이 더한 계약 테스트를 직렬로 따로 돌려 전부 통과**
      (`test_projects.py` · `test_task_assignments.py` · `test_task_predecessors.py` 등).
- [ ] **붙는 자리 둘 각각**에 테스트가 있다 — 요청 발송 · 담당 교체 제안.
      **하나라도 빠지면 실패다.** **직접 배정은 붙는 자리가 아니다.**
- [ ] **표면이 있는 떼는 자리 셋 각각**에 테스트가 있다 — 요청 거절 · 요청 철회 · 배정 거절.
      **셋 다 실제 라우트를 지난다.**
      요청 발송이 세운 배정을 **`decline()` 로 닫는 경우도 한 건 든다.**
- [ ] **넷째(배정 철회)는 메서드 수준에서 해제가 도는 것을 보였다** —
      `TaskAssignmentApplication.cancel()` 을 직접 부르는 테스트가
      **프로젝트가 걸린 pending 배정**에서 떼어지는 것을 잰다.
      그 테스트의 docstring 이 **왜 메서드로 재는지**를 적는다.
- [ ] **그 철회에 표면이 오늘 없다는 사실을 코드 자리로 보였다** — `modules/work/drafts.py:33`
      (`'project_id': None` 강제) · `modules/actions/policy.py:136` · `platform/actions.py:539`.
      **테스트로 증명하지 않는다 — 없는 표면은 테스트할 수 없다.** **Open Issues 에 남긴다.**
- [ ] **넷 다 같은 칸(`task_assignments.auto_project_join`)을 읽는다.**
- [ ] **조건 ① 거짓**(원래 멤버)과 **조건 ② 거짓**(다른 활성 업무 있음)에서 **안 떼어진다.**
- [ ] **관리 권한이 없는 참여자**가 배정해도 붙는다 — 열쇠가 **배정 권한**이다.
- [ ] 떼어진 뒤 **참여 이력에 닫힌 줄이 남는다** — 사유가 **둘 중 하나**다.
- [ ] **상위를 옮기면 자식·손자·증손자가 전부 새 프로젝트에 있다.** 옛 프로젝트에 **0건** 남는다.
- [ ] **자손 중 하나라도 잠겨 있으면 이동 전체가 거절**되고
      **`WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409)** 다. **아무것도 안 움직였다.**
- [ ] **새 오류 코드 0건 · 새 라우트 0건**임을 grep 으로 보였다.
- [ ] `make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_projects`
      **통과** — **이번 판은 새 제약을 만들지 않는다. 이것은 증명이 아니라 회귀**다.
      다만 **닫고 다시 붙이는 경로가 `uq_project_assignment_active` 와 부딪히지 않는다**를 한 건 남긴다.
- [ ] **커밋 후 API 를 다시 띄웠다. 실제 API 계약(응답 예시)을 FE 브리프에 박았다.**

---

### Phase FE-1 — 틀과 좌 레일: 3레일 등록 · 셀렉터 · 업무 카드 · 요약 스트립

- **Status**: TODO
- **닫는 SPEC 인수조건**: **진행률 5줄**(요약 스트립 계산 넷 + 평균 아님) · **상태 어휘 3줄**
  (라벨·톤을 못 찾는 값 안 만남 · 계약 넷 라벨 · 톤이 시안과 같다) · **좌 레일 3줄**
  (분류 없음 · 담당 · 클릭 = 선택) · **빈 상태 1줄**(프로젝트 0개) = **12줄**.
- **근거 결정**: **D-04**(요약 스트립의 모수) · **D-06**(상태 정본과 톤) · **D-08**(「분류」를 빼고
  담당을 세운다) · **D-10**(DS 정본은 우리 코드) · **D-20**(클릭 = 선택) · **D-22**(빈 상태 하나) ·
  **D-26**(사이드바 안 건드림).
- **설명**: 레이아웃과 데이터 배선. **아직 간트도 우 레일도 없다.**

**작업**

0. **선행 확인 (한 줄로 끝낸다)** — 시안 `projects.css` 가 참조하는 토큰이 저장소에 **전부 있다**는
   조사 결과(BASE-004 § DS 토큰, 누락 0개)를 **값까지** 확인한다.
   **결정이 아니라 확인 작업**이다. 다르면 **저장소 값이 정본**이고 그 사실만 기록한다.
1. `App.tsx:352·515` 가 `ProjectPage` 에 **`onRegisterRails` 를 넘기게** 고친다.
   선례 `MyWorkPage.tsx:941-972`. **셸은 이미 3칸 규약을 갖는다** — 새 셸 변경이 들지 않는다.
2. `styles/projects.css` 를 만들고 `index.css` 에 `@import` 한 줄. 시안 CSS 를 옮긴다.
   **`.scax-page-header__title-row` 한 줄은 버린다** (D-25) — 그것은 **없는 슬롯을 전제한 셸 규칙**이다.
3. **좌 레일** — 헤더 한 줄(아이콘 + 「업무」 + **건수 배지**) + **프로젝트 `Select`**.
   `Select` 는 **알약 트리거**를 `trigger` prop 으로 갈아끼운다(선례 `MyWorkPage.tsx:1410`,
   CSS `components.css:44-49`). 헤더가 32px 고정이라 `.scax-gutter-list__header--sub` 를 **화면 CSS 에** 둔다.
4. **업무 카드** — **기존 `scax-inbox-card` 를 그대로 재사용**한다. 조립 선례 `ScheduleCard.tsx:42-99`.
   상태 배지 → 제목 → meta 한 줄(**기간 · 담당**). **「분류」를 싣지 않는다.**
   **담당이 없으면 그 칸을 비운다** — 「미정」을 지어내지 않는다.
5. **선택 상태** — hover · selected · focus. **화면 범위로 한정한 CSS** (§공유 자산).
   **클릭의 뜻은 선택이고 여는 것이 아니다** — **드로어를 열지 않는다.**
6. **요약 스트립 5칸** — 값 24px/32px bold · `tabular-nums`.
   **모수는 「취소를 뺀 업무」 하나**다 — **1번 칸과 5번 분모가 같은 수**다.
   「지연」은 **서버가 기한 경과일을 낸 업무의 수**다 — **끝나지 않은 업무 중 기한이 지난 것**이고,
   **완료·취소·승인 대기에는 서버가 `null` 을 낸다**(`application.py:2521-2529`). 다른 칸과 **겹쳐 센다.**
   **전체 진행률 = 완료 칸 ÷ 전체 업무 칸** — **업무별 % 의 평균이 아니다.**
7. **빈 상태** — 읽을 수 있는 프로젝트가 **0개면 화면 전체를 한 문장으로 덮는다**
   (「담당 프로젝트가 없습니다」). **네 칸을 각각 비우지 않는다.**
8. `lib/viewModels.ts:96-103` 의 `ProjectDetail.tasks` 타입을 넓히고
   **`state: string` 을 `TaskState` 로 조인다** — `ProjectPage.tsx:321` 의 억지 캐스팅이 사라진다.
   ⚠ **`preceding_task_ids: string[]` 도 같이 세운다** — **서버는 이미 내지만 FE 타입에 없다.**
   `viewModels.ts:95-102` 는 여섯 필드뿐이고 `features/project` 에서 읽는 코드가 **0건**이다.
   **BE-1 이 새로 더한 것만 넓히면 FE-2 가 의존선의 재료 없이 시작한다**(I-6).
9. `features/project/projectModel.ts`(신규 · **순수 함수**) — 요약 세기와 트리 조립의 **재료 함수**를
   여기 둔다. 선례 `workRows.ts`·`calendarModel.ts`. **화면이 서버 응답을 JSX 에 바로 꽂지 않는다.**

**하지 말 것**

- **사이드바·내비 순서를 건드리지 마라** (D-26, 사용자 결정). 어긋남 ⑤-8 은 **기록만.**
- **`AppHeader` 에 슬롯을 더하지 마라** (D-25).
- **`.scax-inbox-card--selected` 를 공유 CSS 에 무조건 규칙으로 얹지 마라** — 수신함·캘린더가 흔들린다.
- **`components.css:692-693` 의 반응형 줄을 손대지 마라** — 홈·보고가 같이 움직인다.
- **요약 스트립에서 취소를 「전체」에만 빼지 마라** — 한쪽만 빼면 **D-04 의 근거가 깨진다.**
- **취소된 업무를 목록에서 감추지 마라** — **세지 않는 것과 감추는 것은 다르다.**
  좌 레일 카드에는 **남는다.**

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make frontend-test`(**Node 20**) · `cd frontend && npx tsc --noEmit` **통과**.
- [ ] 선행 확인 0 의 결과가 **한 줄로 기록**됐다.
- [ ] 화면이 **3레일**이다 — 좌 380px · 우 342px. **토큰 값을 새로 만들지 않았다.**
- [ ] 좌 레일 카드에 **「분류」가 없고** 그 자리에 **담당**이 있다. 담당 없는 업무는 **빈 칸**이다.
- [ ] 카드를 클릭하면 **선택**된다 — **드로어가 열리지 않는다.**
- [ ] 좌 레일 건수 배지와 **「전체 업무」 칸이 다를 수 있다** —
      **취소된 업무가 있으면 배지가 더 크다.** 둘은 다른 것을 센다.
- [ ] **「전체 업무」 칸과 진행률 분모가 같은 수**다.
      업무 10건 중 **2건 취소 · 8건 완료**면 「전체 업무」 **8** · 「완료」 **8** · 진행률 **100%** 다.
- [ ] 「지연」 칸이 **서버가 기한 경과일을 낸 업무**를 센다 — 진행 중이면서 기한을 넘긴 업무는 **세고**,
      **완료한 업무는 기한을 넘겼어도 안 센다**(서버가 `null` 을 낸다).
- [ ] 배지 라벨이 **「시작 전」·「진행 중」·「완료」·「취소」**다 — 시안의 「대기」가 아니다.
      **`blocked` 가 오면 「막힘 / `danger`」**로 그려진다.
- [ ] **라벨·톤을 못 찾는 값이 안 온다** — `completion_submitted` 가 화면에 닿지 않는다.
- [ ] 읽을 수 있는 프로젝트가 **0개인 사람에게 한 문장**이 뜬다 — 네 칸이 각각 비지 않는다.
- [ ] **`src/ds/` 파일을 한 줄도 안 고쳤다** — `git diff --stat frontend/src/ds/` 가 **비어 있다.**

---

### Phase FE-2 — 간트와 의존선: **이 판의 가장 어려운 자리**

- **Status**: TODO
- **닫는 SPEC 인수조건**: **핵심 넷 중 3줄**(손자 행 · 손자에 걸린 선 · 접어도 안 사라지는 선) ·
  **간트와 트리 6줄** · **의존선 4줄** · **진행률 5줄**(바의 % 규칙) = **18줄**
  (+ BE-1·FE-1 과 갈라지는 **5줄**).
  ⚠ **의존선의 「후행 목록이 우 레일에 나온다」 한 줄은 FE-3 이 닫는다** — **우 레일이 FE-3 이다.**
- **근거 결정**: **D-16**(깊이 제한 없는 재귀 트리, 사용자 결정) · **D-17**(접힌 가지의 의존선) ·
  **D-18**(들여쓰기 12px · 최대 5단) · **D-09**(기간 없는 업무는 간트에서 뺀다) ·
  **D-07**(후행은 클라이언트가 역산) · **D-01~D-03**(바 안의 %) · **D-23**(`cancelled` 바).
- **설명**: **화면이 거짓말하지 않게 만드는 Phase 다.** 여기서 자르면 선이 조용히 사라진다.

**작업**

1. **평평한 `tasks[]` 에서 재귀 트리를 만든다** — `projectModel.ts` 의 순수 함수.
   **깊이 제한이 없다.** 부모 참조가 이미 실려 있고 **손자까지 전부 실리므로
   자르는 쪽이 오히려 추가로 하는 일**이다.
2. **행 기하는 시안 그대로** — 행 40px · 하루 34px · 라벨 칸 200px 고정 · 바 22/14/18px.
   **바꾸는 것은 들여쓰기 한 값뿐**이다 — **깊이당 12px · 최대 5단.**
   **5단에서 멈추는 것은 들여쓰기이고 행이 아니다.** 6층 이하는 **5단과 같은 들여쓰기로 계속 쌓인다.**
3. **twisty 는 펼칠 것이 실제로 있을 때만 선다** — **간트에 자리가 선 자손이 있는 행**에.
   **기본은 모두 펼침.**
   **「펼칠 것이 있나」와 「하위가 있나」를 나눈다** — 앞의 것이 **twisty·펼침**을 맡고,
   뒤의 것이 **바 규격(상위 14px · % 없음)과 `하위 N`** 을 맡는다.
   하위가 **전부 기간 없는 업무**면 **간트에 설 행이 없어** twisty 를 세워도 **눌러도 안 움직인다** —
   **죽은 손잡이를 세우지 않는다.** 그때도 **바는 상위 규격이고 `하위 N` 은 그대로 난다.**
4. **축의 기간은 데이터가 정한다** — 시안의 `{days: 30, today: 17}` 과 legend 「2026년 9월」은
   **목데이터 하드코딩**이다. **「오늘」도 고정값이 아니다.**
5. **간트에 서는 업무** — **정규화 결과가 있는 것만.** 기간이 없으면 **간트에 안 서고 좌 레일에만 선다.**
   **정규화를 화면이 다시 하지 않는다** — `span_from`·`span_to` 를 그대로 읽는다.
6. **바 안의 %**
   - 체크리스트가 **있으면** 완료 ÷ 전체. 5개 중 2개면 **40%**.
   - **없으면 fill 도 % 텍스트도 그리지 않는다** — **0% 가 아니다.**
   - 외부 상태 `done` 은 **체크리스트가 없어도 100%**.
   - `cancelled` 는 **% 없음** + 배경 `fill-weak` + fill 없음 + **제목 취소선**.
   - **상위 업무 바는 % 텍스트를 내지 않는다** — 하위가 있는 **모든 깊이**에서.
7. **의존선 오버레이** — 간트 위에 겹치는 SVG. **직각 3구간 + 화살표가 후행을 가리킨다.**
   원천은 **`preceding_task_ids` 하나**다. **후행을 서버에 묻지 않는다** —
   그 프로젝트 업무 전부의 선행 배열을 **뒤집어서** 만든다.
8. **접힌 가지의 선을 접힌 부모 바에 끌어붙인다** (D-17).
   ⚠ **시안은 이 경우를 안 다룬다** — `DepLines` 가 `if (!a || !b) return` 으로 **말없이 빠져나간다**
   (`handoff/projects/js/projects.v1.jsx:85-106`). 목데이터가 1단계뿐이라 **생길 수 없었던 상황**이다.
   **그 `return` 을 그대로 옮기면 화면이 「선행 없음」이라고 거짓말한다.**
9. **읽을 수 없는 선행은 자리가 남는다** — 제목·상태가 비고 **건수는 난다**.
   프로젝트 범위에서는 드물지만 **계약이다.**
10. **강조** — 평소 `line-strong` 1.2px, **선택된 업무에 닿는 선만** `accent` 1.6px.
11. **`하위 N` 은 화면이 센다** — 서버가 안 낸다.

**하지 말 것**

- **깊이를 자르지 마라** (D-16, 사용자 결정). 자르면 손자 행의 좌표가 없고 **선이 조용히 사라진다.**
- **들여쓰기 한계에서 행을 멈추지 마라** (D-18). **멈추는 것은 들여쓰기다.**
- **양 끝 좌표를 못 찾았다고 조용히 빠져나가지 마라.** 접힘이면 **부모 바에 붙이고**,
  그 밖의 경우는 **왜 없는지가 드러나야 한다.**
- **후행 조회를 서버에 만들지 마라** (D-07).
- **`taskSpan()` 같은 클라이언트 정규화를 부르지 마라** — 서버가 준 값을 쓴다.
- **체크리스트 없는 업무를 0% 로 그리지 마라** — **「아무것도 안 한 일」이라는 허위**가 생긴다.

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make frontend-test` · `npx tsc --noEmit` **통과**.
- [ ] **3층 트리에서 세 행이 전부 선다** — 손자도 자기 행과 자기 바를 갖는다.
- [ ] **깊이 4·5 의 업무도 행을 갖는다** — 행이 사라지는 깊이가 **없다.**
- [ ] 들여쓰기가 **깊이당 12px** 이고 **5단에서 멈춘다.** 6층 이하도 **행은 계속 선다.**
- [ ] twisty 가 **펼칠 것이 실제로 있을 때만** 서고, 기본이 **모두 펼침**이다.
      **하위가 전부 기간 없는 업무면 twisty 가 서지 않는다** — **죽은 손잡이가 없다.**
      **그때도 그 행의 바는 상위 규격(14px · % 없음)이고 `하위 N` 은 그대로 난다.**
- [ ] **손자가 조부의 형제를 선행으로 가져도 화살표가 선다** — 깊이로 잘리지 않는다.
- [ ] **가지를 접어도 어떤 관계도 사라지지 않는다** — **선으로 남거나, 건수로 남는다**
      (SPEC §2.5 세 갈래 표). **말없이 버려지는 경로가 없다.**
      ① 한쪽만 접히면 **접힌 부모 바에 닻을 박아 선을 그린다** — 접기 전후 **선의 개수가 같고**
      **닻의 값**(접힌 부모 id)까지 잰다. ② **양 끝이 같은 접힌 가지 안**이면 **그 행이 건수로 들고**
      무엇이 접혔는지를 말한다 — **선 하나가 줄고 건수 하나가 는다.**
      ③ 한쪽이 **기간 없거나 볼 수 없는 업무**면 **머리줄이 그 건수로 말한다.**
      **콘솔 경고도, 빈 자리도, 말없이 버려진 관계도 없다.**
- [ ] **후행을 서버에 묻는 호출이 0건**이다 (네트워크 탭·mock 호출 수로 보인다).
- [ ] 기간이 없는 업무가 **간트에 안 서고 좌 레일에는 선다.**
- [ ] **한쪽 날짜만 있는 업무가 그 날 하루짜리 바**이고, **뒤집힌 기간이 정규화된 구간**으로 그려진다 —
      **화면이 그 규칙을 다시 계산하지 않는다.**
- [ ] 축의 기간이 **데이터에서 나온다** — 30일 고정도, 고정된 「오늘」도 없다.
- [ ] 체크리스트 5개 중 2개 완료가 **40%**, 없으면 **fill·% 없음**, `done` 은 **100%**,
      `cancelled` 는 **% 없음 + 취소선**, **상위 바는 % 텍스트 없음**.
- [ ] **취소된 업무가 간트에 그대로 선다** — 요약 스트립에서만 빠진다.
- [ ] 선택된 업무에 닿는 선만 강조된다.

---

### Phase FE-3 — 우 레일 · 관리 모달 · 빈 상태 · 기존 테스트 교체

- **Status**: TODO
- **닫는 SPEC 인수조건**: **우 레일 4줄** · **관리 모달과 빈 상태 6줄** · **진행률 1줄**
  (우 레일 미터 「—」) · **의존선 1줄**(**후행 목록이 우 레일에 나온다** — 우 레일이 여기다) = **12줄**.
- **근거 결정**: **D-05**(관리 기능은 별도 모달, 사용자 결정) · **D-20**(여는 것은 한 줄로) ·
  **D-21**(손잡이는 헤더 `actions`) · **D-22**(빈 상태) · **D-24**(`Empty` 글리프 안 고침) ·
  **D-02**(체크리스트 없으면 미터가 「—」).
- **설명**: 상세와 관리를 제자리에 놓는다. **여기까지가 「화면이 다 섰다」**다.

**작업**

1. **우 레일 — 선택 업무 상자.** 선택이 없으면 **빈 상태**(「업무를 선택하세요」).
   **글리프는 20px 그대로** — 시안의 24px 과의 4px 차이는 **기록으로 남긴다** (D-24).
2. 머리: 제목 + **진행률 미터 + %**. **체크리스트가 없으면 「—」** — 0% 가 아니다.
   미터는 **화면 전용 클래스**로 만든다 (`ds/ProgressBar` 를 건드리지 않는다).
3. 블록 다섯 — **메타**(상태 배지 · 기간 · 담당 · 요청 · 상위 업무. **「분류」 없음**) ·
   **관계**(선행 건수+목록 · **후행 건수+목록**. 줄을 누르면 **그 업무가 선택된다**) ·
   **체크리스트**(`완료/전체` + 항목. **읽기 전용**) · **하위 업무 카드 목록** ·
   **「업무 열기」 한 줄**(**기존 드로어를 부른다** — 편집은 거기서만).
4. **우 레일은 선택된 하나에만 업무 상세를 부른다.** 목록 전부를 상세로 긁으면
   **업무 수만큼 호출**이 된다.
5. **체크리스트 항목이 안 실릴 수 있다** — 읽기 전용 접근에는 항목이 안 온다.
   그때 **집계와 미터는 그리고 항목 자리를 비운다.**
6. **관리 모달** — 참여자 붙이기/떼기 · 참여 이력 · 새 프로젝트 셋을 본문에서 **모달로 옮긴다.**
   손잡이는 **헤더의 `actions`**(`App.tsx:127` `surfaceActions` seam).
   **`may_manage` 가 거짓이면 렌더하지 않는다** — 화면이 권한을 추측하지 않는다.
   **⚠ 시안이 없다 — 어휘를 빌린다.** 지금 `ProjectPage.tsx:206-306` 의 UI 를
   `handoff/shell/js/work-modal.jsx` 의 **`Modal`**(`scax-modal-overlay` / `__head` / `__body` /
   `__foot`) · **`Field`**(`scax-field` / `__label` / `__hint`) · **`TextField`**(`scax-textfield`) ·
   **`AutoComplete`** 로 **옮긴다. 새 부품을 발명하지 않고, 필드를 늘리지도 줄이지도 않는다.**
   구성원 고르기는 지금 `ds/Select` 인데 시안 어휘의 `AutoComplete` 가 그 자리다 —
   **`ds/Select` 를 고치지 않고** 화면 안에서 조립한다.
7. **선택 축은 하나다** — 좌 레일 카드 · 간트 행/바 · 의존선 · 우 레일이
   **어디서 골라도 나머지 셋이 같이 반응**한다.
8. **기존 테스트 단언 교체** — `ProjectPage.test.tsx` 7개 중 **6개**.
   **기능이 모달로 옮겨가므로 검사도 따라간다** — **지우는 것이 아니다.**
   `may_manage` 로 관리 UI 를 감추는 검사(#3)는 **모달 손잡이 렌더 여부**로 옮긴다.
   프로젝트 전환 시 열린 입력을 닫는 검사(#7)는 **`Select` 전환**으로 옮긴다.

**하지 말 것**

- **기존 테스트를 편의상 삭제·skip·단언 약화 하지 마라.** 깨지면 **계약이 바뀐 것인지
  구현이 틀린 것인지**를 먼저 가른다. 이 판에서 깨지는 여섯은 **전부 자리 옮김**이다.
- **`ds/Empty` 의 글리프 크기를 고치지 마라** (D-24) — **4px 때문에 29곳을 흔들지 않는다.**
- **`ds/ProgressBar` 의 API 를 바꾸지 마라** — 소비처 1곳이 같이 움직인다.
- **드로어를 버리지 마라** — 편집은 거기서만 된다. **제스처를 나누는 것으로 충돌을 푼다.**
- **`member → lead` 승격을 모달에 만들지 마라** (보류).
- **우 레일이 목록 전부를 상세로 긁지 마라.**

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make frontend-test` · `npx tsc --noEmit` **통과**.
- [ ] 우 레일 미터가 체크리스트 없는 업무에서 **「—」** 다.
- [ ] 우 레일 체크리스트가 **읽기 전용**이다 — 이 화면에서 항목을 끄고 켤 수 없다.
- [ ] 읽기 전용 접근이라 항목이 안 실려도 **집계와 미터는 그려진다.**
- [ ] 우 레일이 **선택된 하나에만** 상세를 부른다 — 호출 수가 업무 수에 비례하지 않는다.
- [ ] 우 레일 **관계 블록에 후행 건수와 목록이 뜨고**, 그 원천이 **클라이언트가 뒤집어 만든 것**이다 —
      **후행을 서버에 묻는 호출이 0건**이다.
- [ ] **「업무 열기」를 눌러야 드로어가 열린다.**
- [ ] **선택 하나가 좌 레일 · 간트 행 · 의존선 · 우 레일 넷을 동시에** 움직인다.
- [ ] 참여자 붙이기/떼기 · 참여 이력 · 새 프로젝트가 **모달 안에** 있다 — 본문에 없다.
- [ ] 모달 손잡이가 **헤더의 `actions`** 에 있고, **`may_manage` 가 거짓이면 렌더되지 않는다.**
      참이면 **렌더된다.** 화면이 그 판정을 **다시 계산하는 자리가 0개**다.
- [ ] 모달이 **시안 어휘**를 쓴다 — `scax-modal-*` · `scax-field*` · `scax-textfield*`.
      **새 부품을 발명하지 않았고 필드가 늘거나 줄지 않았다.**
- [ ] 업무 미선택 우 레일이 **프로젝트 0개 빈 상태와 다른 빈 상태**다.
- [ ] 빈 상태 글리프가 **20px 그대로**다 — **`src/ds/` diff 가 비어 있다.**
- [ ] `ProjectPage.test.tsx` 의 검사가 **삭제 0건 · 교체 6건**이고, 각 교체가
      **옮겨간 자리를 겨눈다.**
- [ ] **최종 검증** — §검증 계획의 3단 절차를 돌리고 **회차 5 기록**을 남겼다.

---

## Execution — 2루프 (사용자 동반)

**1루프가 전부 닫힌 뒤**, **사용자가 직접 검수하며** 진행한다.
**그 검수 결과가 2루프의 입력**이다.

> **2026-09-22 — 그 검수가 돌았고, 2루프의 본체가 정해졌다.**
> **Phase 0 는 닫혔고**(`make verify` **exit 0**, 코디 실측) **브라우저 E2E 1차도 사용자가 돌렸다.**
> 그 1차가 낸 **지시 열한 건**이 DEC-004 의 **D-28 ~ D-38** 로, SPEC-005 **v0.2.0** 의
> **§4 읽기 범위 · §2.10 · §6 L-01~L-52** 로 내려왔다.
> **그래서 2루프에 Phase 셋이 더 붙는다 — BE-3 → FE-4 → FE-5.**
> **1루프의 다섯 Phase 는 기록이다 — 건드리지 않는다.**

### 단계 순서 — **2루프도 직렬이다. BE 가 먼저다**

```text
2루프
   Phase 0 (DONE)  ·  브라우저 E2E 1차 (DONE · 사용자)
        │
        ▼
   Phase BE-3 ──▶ Phase FE-4 ──▶ Phase FE-5 ──▶ 브라우저 E2E 2차 (사용자)
      │              │              │
      └ 리뷰·재수정   └ 리뷰·재수정   └ 리뷰·재수정
```

- **BE 를 먼저 한다 — 사용자 지시(2026-09-22)**: 「api 필요한 거는 백엔드 먼저 하고 fe 돌리자,
  **계약이 제대로 안 되서 서로 충돌 나더라**」. **병렬로 두지 않는다.**
- **왜 그 순서가 맞나** — **D-29 가 FE 가 받는 응답을 바꾼다.** 같은 프로젝트 사람이 남의 업무를
  골랐을 때 **항목이 오느냐**가 우 레일 분기를 가른다. **FE 는 BE-3 이 닫힌 뒤 실물 응답을 보고 짠다** —
  **추정으로 짜면 그 분기가 틀린다.**
- **BE-3 이 닫히면 실제 응답 예시를 FE 브리프에 박는다** — 1루프의 BE-2 → FE 규칙 그대로.
- **FE-4 와 FE-5 도 직렬이다** — **`projects.css` 한 장과 `ProjectRail.tsx` 를 둘 다 만진다**
  (§Code Surface 「FE 를 둘로 쪼갠 이유」).
- **백엔드 커밋이 들어가면 API 를 반드시 다시 띄운다** — 1루프와 같은 규칙.
  **옛 코드가 떠 있으면 「프론트가 안 된다」로 보인다.**
- **워커가 못 정하는 것이 나오면 코디가 결정하고 `Open Issues` 에 남긴다.** 조용히 정하지 않는다.

### Phase 0 — `material_*` 병렬 격리

- **Status**: **DONE (2026-09-22)** — **2루프 · 사용자 동반.**
  **`make verify` 가 exit 0 를 낸다**(코디 실측 2026-09-22). 그 결과로 **§검증 계획의 기준선이
  바뀌었다** — 이제 **「기준선 밖 실패 0」이 아니라 「실패 0」**이다.
  ⚠ **아래 본문은 그 Phase 를 열 때의 계획이고 기록으로 남긴다** — 무엇을 왜 했는지가 같이 남아야 한다.
- **닫는 SPEC 인수조건**: **없다.** SPEC-005 §1 Scope Out 이
  「`material_*` 병렬 격리(Phase 0) — 같은 slug 의 선행 작업이지만 **이 계약의 범위가 아니다**」로
  명시적으로 뺐다. **이 Phase 는 계약이 아니라 검증 인프라를 고친다.**
- **근거 결정**: DEC-004 「프로젝트 화면(B)이 메인, `material_*` 병렬 격리(A)는 **같은 slug 의 Phase 0** 로
  선행한다」 — 사용자 지시. 그리고 **1루프 범위 제약**(사용자 지시 2026-09-21):
  **「Phase 0 는 내일 사용자 몫」**.
- **왜 번호가 0 인데 마지막에 서 있나** — **논리적으로는 선행**이다(`make verify` 가 여기서 막힌다).
  **일정상으로는 2루프**다(사용자가 동반해야 한다). **1루프는 그것을 우회하지 않고 기준선 분리로 지나간다.**
- **재료**: `reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md` ·
  `orchestration/work/_archive/strong-hajin/strong-hajin-calendar/flaky-baseline-evidence.md` ·
  **그리고 1루프가 남긴 `flaky-baseline-projects.md` 의 회차 0~5 기록.**

**⚠ 원인이 아직 규명되지 않았다.** 재료의 「다음에 볼 자리」 셋은 **가설**이다 —
공유 자원이 무엇인지도, 어느 격리 수단이 맞는지도 **정해지지 않았다.**
**그래서 조사와 수정을 한 Phase 에 묶는다.** 조사만 떼어 발주하면
「무엇이 공유되는가」의 답이 **수정 방법을 바꾸는데** 그 사이에 판이 갈린다.

**지금까지 관측된 사실 (재료가 갖는다 — 다시 재지 않는다)**

| 사실 | 근거 |
|---|---|
| **고정 실패가 아니다** — 실패 파일 집합이 회차마다 바뀐다 | 캘린더 작업 6회차 기록 (`2f → 2f → 2f → 3f → 5f → 2f/3f`) |
| **직렬로 돌리면 전부 통과한다** — 한 라운드의 실패 다섯 파일을 `-p no:randomly` 직렬로 → **44 passed / 0 failed** | 같은 기록 |
| **착수 전 기준선에 이미 2건 실패했다** — 캘린더 코드가 한 줄도 없을 때 | 같은 기록 |
| **실패 단언이 job 상태다** (`['failed','running']` vs `['failed','completed']`) — **시간에 민감한 경합** | 같은 기록 |
| **부하가 실제로 눌려 있었다** — `load average 19.39`, E2E 스택 동시 기동, 나중에 OOM 으로 두 번 죽음 | 같은 기록 |
| **테스트가 늘수록 빈도가 는다** — 계약 테스트 58건을 더하자 `2f → 3f → 5f` | 같은 기록 |

**작업 — 조사와 수정을 한 Phase 에**

1. **무엇이 공유되는가를 먼저 답한다.** 그 계열이 무엇을 두고 다투는지 — 파일? DB? 시계?
   **`durable_jobs` 원장과 lease 시각이 후보이고, 후보일 뿐이다.**
   **1루프의 회차 기록이 여기 쓰인다** — 어느 파일이 어느 회차에 흔들렸는지, 그리고
   **이번 판이 더한 테스트가 그 계열과 무관하다**는 것이 그 기록으로 선다.
2. **재현을 만든다.** 원인 가설이 맞으면 **원하는 때에 실패를 만들 수 있어야 한다.**
   재현이 없으면 「고쳤다」를 증명할 방법도 없다.
3. **격리 수단을 고른다 — 원인이 정해진 뒤에.** 후보 셋(전부 가설):
   ① `pytest-xdist` 의 `--dist loadgroup` 으로 그 파일들을 한 워커에 묶기 ·
   ② 그 계열에만 직렬 마커 · ③ lease·timeout 을 실시간이 아니라 **주입 시계**로.
   **③ 이 유일하게 원인을 고치는 쪽**이고 ①② 는 증상을 가린다 — **그 차이를 보고에 적는다.**
4. **`make verify` 의 계약을 정한다.** 지금은 한 명령이 전부를 돈다.
   그 계열만 갈라 도는 타겟이 필요한지, `test-contract-serial`(BE-1 이 더한 것)을
   일반화할지 **여기서 정한다.**
5. **수정하고 증명한다** — 격리 후 **연속 여러 회차 초록**.

**하지 말 것**

- **테스트를 지우거나 `skip` 하거나 단언을 약화해서 초록을 만들지 마라.**
  그것은 **원인 규명이 아니라 증거 인멸**이다.
- **원인을 모른 채 격리 수단부터 고르지 마라.** ①② 를 먼저 넣으면
  **원인이 영영 안 밝혀진다** — 증상이 사라지기 때문이다.
- **이 Phase 를 1루프로 끌어오지 마라.** **사용자 몫**이다.

**완료 판정 — 사용자와 함께 본다**

- [ ] **무엇이 공유되는지가 한 줄로 적혔다** — 「모르겠다」면 그것도 그렇게 적는다.
- [ ] **원하는 때에 실패를 재현할 수 있다.**
- [ ] 고른 격리 수단이 **증상을 가리는 것인지 원인을 고치는 것인지**가 적혀 있다.
- [ ] **`make verify` 가 exit 0** 이거나, 아니라면 **남은 실패의 이유가 적혀 있다.**
- [ ] **연속 여러 회차 초록**이 수치로 남았다.
- [ ] **테스트 삭제·skip·단언 약화 0건.**

### 브라우저 E2E — 사용자 담당

**Phase FE-3 뒤에 넘긴다.** 아래는 **눈으로 보는 것**이고 자동 검증이 닿지 않는 자리다.

> **1차는 돌았다 (2026-09-22 · 사용자).** 화면 `http://localhost:5173/`(viewport 1676x936) ·
> API `127.0.0.1:8100` · DB `54329/ax_demo`. **그 1차가 지시 열한 건을 냈고 그것이 2루프의 본체**다
> (`loop2-backlog.md`). **아래 E-1~E-19 의 관측 결과 자체는 그 기록이 갖는다.**
>
> **2차는 Phase FE-5 뒤다.** 2차가 볼 것은 **E-1~E-19 의 회귀 + 아래 2루프 항목**이다.

**2루프 E2E — Phase FE-5 뒤에 넘긴다 (2026-09-22 추가)**

| 시나리오 | 조작 | 기대 결과(눈으로) | 인수조건 |
|---|---|---|---|
| E-20 | **조직 축 권한만 있는 사람**(그 프로젝트에서 배정 자격 없음)으로 남에게 업무를 보낸다 | 받은 사람의 셀렉터에 **그 프로젝트가 뜬다** | L-01 |
| E-21 | **참여자**로 붙은 사람으로 **남의 업무**를 고른다 | 「업무 정보」에 **체크리스트 항목이 보인다** | L-07 |
| E-22 | 같은 화면에서 그 항목을 **켜 보려 한다** | **켜지지 않는다** — 읽기 전용이다 | L-11 · 우 레일 계약 |
| E-23 | **프로젝트가 0개인 사람**으로 연다 | 본문은 **한 문장**인데 헤더에 **「프로젝트 추가」가 있다** | L-15 |
| E-24 | 그 버튼으로 **프로젝트를 만든다** | **네 칸 모달** → 만들면 셀렉터에 뜨고 **내가 리드**다 | L-19 · L-22 |
| E-25 | **관리 권한 없는 프로젝트**를 고른다 | **관리 버튼은 없고 생성 버튼은 있다** | L-16 |
| E-26 | 간트를 **오른쪽으로 끝까지 민다** | **업무 이름이 남아 있고** 그 칸 위로 **막대·날짜가 비치지 않는다** | L-42~L-44 |
| E-27 | 화면을 **새로 연다** | 간트가 **오늘이 보이는 위치**에서 시작한다 | L-45 |
| E-28 | 간트 **아래쪽 업무**를 누른다 | 좌 레일이 **그 카드로 스크롤**한다 | L-46 |
| E-29 | **내 업무**를 골라 상태를 바꾼다 | **드롭다운**이 뜨고 바뀐다. **요청 업무의 완료는 완료 보고 모달**이 뜬다. **「막힘」을 고르면 사유 입력이 먼저 뜨고**, 바꾸고 나면 **좌 레일 카드와 간트 바도 새 상태**다 | L-27 · L-31 · **L-49 · L-52** |
| E-30 | **남의 업무**를 고른다 | 상태가 **읽기 배지**다 | L-28 |
| E-31 | 우 레일의 **상위 업무 버튼**과 **선행·후행 줄**을 본다(hover 없이) | **누를 수 있게 보인다.** 누르면 **그 업무가 선택된다** | L-40 · L-41 |
| E-32 | 완료된 업무의 바와 좌 레일 헤더를 본다 | 초록이 **혼자 쨍하지 않다** · 헤더가 **한 줄**이다 | L-36 · L-34 |

| 시나리오 | 조작 | 기대 결과(눈으로) |
|---|---|---|
| E-1 | 요청을 주고받아 만든 **3층 트리**의 프로젝트를 연다 | **세 행이 전부 선다.** 손자에도 바가 있다 |
| E-2 | 손자가 **조부의 형제**를 선행으로 갖게 하고 본다 | **화살표가 선다** — 깊이로 안 잘린다 |
| E-3 | 그 가지를 **접는다** | **선이 접힌 부모 바에 붙는다.** 사라지지 않는다. **콘솔 경고 0건** |
| E-4 | 깊이 5·6 의 업무를 만들어 본다 | **행이 계속 선다.** 들여쓰기만 5단에서 멈춘다 |
| E-5 | 체크리스트 없는 업무의 바와 우 레일을 본다 | **fill 도 % 도 없고** 미터가 **「—」** 다. **0% 가 아니다** |
| E-6 | 업무 10건 중 2건을 취소하고 나머지를 완료한다 | 「전체 업무」 **8** · 「완료」 **8** · 진행률 **100%**. **그런데 취소 2건이 간트에는 취소선 바로 선다** |
| E-7 | 카드를 클릭한다 | **선택된다. 드로어가 안 열린다.** 넷이 동시에 움직인다 |
| E-8 | 우 레일의 **「업무 열기」**를 누른다 | **기존 드로어가 열린다** |
| E-9 | **프로젝트 밖 사람**에게 업무를 보낸다 | 그 사람 셀렉터에 **그 프로젝트가 뜬다** |
| E-10 | 그 사람이 **거절**한다 | 셀렉터에서 **사라지고**, 참여 이력에 **「요청 거절」로 닫힌 줄**이 남는다 |
| E-11 | 같은 사람에게 **둘** 보내고 **하나만** 거절한다 | **안 떼어진다** |
| E-12 | **원래 멤버**에게 보내고 거절당한다 | **아무 일도 일어나지 않는다** |
| E-13 | 배정을 보내고 **받는 사람이 답하기 전에 거둔다** | **떼어진다** — 「보냈다 거뒀는데 사람은 남는」 자리가 없다 |
| E-14 | 수락 뒤 업무를 **완료**하고, 다시 **취소**한다 | **참여가 유지된다** |
| E-15 | 상위를 다른 프로젝트로 **옮긴다** | **손자까지 새 프로젝트에 있다.** 옛 프로젝트에 **0건** |
| E-16 | 자손 하나에 **남은 선행**을 두고 옮겨 본다 | **거절된다.** **아무것도 안 움직였다** |
| E-17 | **관리 권한이 없는 사람**으로 연다 | 헤더에 **관리 모달 손잡이가 없다** |
| E-18 | **프로젝트가 0개인 사람**으로 연다 | **한 문장**이 화면을 덮는다. 네 칸이 각각 비지 않는다 |
| E-19 | 시안을 띄워 나란히 본다 (`cd "reference/2026-09-10-sc-meeting/package 2" && python3 -m http.server`) | 배치·간격 차이를 **후속 목록**으로 적는다 |

---

### Phase BE-3 — 게이트 제거와 **체크리스트 읽기 범위** (`D-28` · `D-29`)

- **Status**: TODO — **2루프의 첫 자리이고 FE 전부의 선행이다**
- **닫는 SPEC 인수조건**: **L-01 ~ L-06**(게이트 제거 전부) · **L-07 · L-08 · L-09 · L-11 · L-12**
  (읽기 범위의 서버 절반) · **L-13**. **L-10 은 FE-5 와 갈린다**(§인수조건 추적).
- **근거 결정**: **D-28**(배정이 성립하면 붙는다 — 사용자 결정) ·
  **D-29**(체크리스트·업무 내용을 프로젝트 구성원이면 본다 — 사용자 결정) ·
  **SPEC-005 §4 「체크리스트·업무 내용의 읽기 범위」**(가르는 방식 ⓑ — 제안).
- **설명**: **여기까지가 「FE 가 볼 응답이 확정됐다」**다.

**작업**

1. **게이트 한 줄을 뺀다** — 자동 초대의 첫 줄(`modules/work/projects.py:230`).
   붙는 관계(`member`)도 붙는 자리(둘)도 **안 바뀐다.**
2. **`may_assign_in` 의 정의는 남긴다**(`projects.py:494`) — **다른 소비처가 쓴다.**
   **`plan_project_work()`(`assignments.py:171`)를 같이 빼지 마라** —
   「그 프로젝트에 업무를 **올릴** 자격」은 **다른 규칙**이고, 같이 빼면 **문이 하나 더 열린다.**
3. **체크리스트를 싣는 조건을 넓힌다** — 「활성 배정을 쥐었나」 **또는**
   「그 업무의 프로젝트에 붙어 있나」. **프로젝트 판정은 이미 있는 것을 쓴다**
   (`application.py:1111-1118` `_may_read_beyond_holding()`) — **새 질의를 만들지 않는다.**
4. **접근 값을 셋으로 늘리지 마라** — **`owner`/`read_only` 그대로**다(SPEC-005 §4 ⓑ 채택).
   **`read_only` 인데 항목이 실리는 조합이 정상**이고, 그 값은 이제 **쓰기 범위만** 뜻한다.
5. **집계도 같이 넓힌다** — 항목만 열고 집계를 닫으면 **같은 사실을 두 규칙으로 읽는 것**이 된다.
6. **쓰기 가드는 한 줄도 건드리지 마라** — 체크리스트 추가·체크·삭제·순서는 **담당자만** 그대로다.
7. **뒤집힌 테스트를 다시 쓴다** —
   `tests/contract/test_project_membership_follows_work.py:121-159`
   (`test_the_key_is_assigning_in_that_project_not_managing_it`)는 **주장이 뒤집혔다.**
   **이름·docstring·`:148` 단언**을 새 계약으로 다시 쓴다. **삭제·skip·단언 약화 금지.**
8. **RED 먼저.** 읽기 범위는 계약 테스트 셋으로 잰다 —
   **같은 프로젝트의 남의 업무에서 항목이 온다 / 쓰기는 여전히 거절된다 /
   프로젝트 밖에서는 안 온다.**
9. **실제 응답 예시를 뽑아 FE 브리프에 박는다** — **같은 프로젝트의 남의 업무 1건**과
   **프로젝트 밖 읽기 1건.** **추정으로 쓰지 않는다.**

**하지 말 것**

- **`tasks[]` 를 넓히지 마라** (D-38). 업무 내용도 체크리스트 항목도 **프로젝트 상세에 싣지 않는다.**
- **새 라우트·새 도구·새 오류 코드를 만들지 마라** — **2루프도 0건이다.**
- **저장 구조를 건드리지 마라** — **표도 컬럼도 안 는다**(§Domain / Schema).
- **`plan_project_work()` 의 게이트를 같이 빼지 마라** — 위 2.

**완료 판정 — 무엇이 돌면 끝인가**

- [ ] `make test-unit` · `make test-contract` **통과** — **실패 0** (§검증 계획).
- [ ] **L-01** 조직 축 권한으로 배정한 사람의 상대가 **그 프로젝트에 붙는다.**
- [ ] **L-02** 붙는 관계가 **`참여`** 다.
- [ ] **L-03** **프로젝트에 업무를 올리는 거절은 그대로 산다** — 그 테스트가 **여전히 초록**이다.
- [ ] **L-04** 배정이 막히는 사람은 **기존 배정 거절**을 받는다. **새 오류 코드 0건.**
- [ ] **L-05** **새로 붙은 사람도 거절하면 떼어진다**(조건 ①·② 충족 시)
      — 참여 이력에 **닫힌 줄**이 남는다.
- [ ] **L-06** **뒤집힌 테스트가 새 계약을 잰다** — 이름·설명·단언이 바뀌었고 **삭제가 아니다.**
      이웃 둘(`:460-476` · `:170-188`)이 **그대로 초록**이다.
- [ ] **L-07 · L-08** 같은 프로젝트의 **참여자**와 **리드** 둘 다 **남의 업무 항목**을 받는다.
- [ ] **L-09** 같은 응답에 **집계도 온다.**
- [ ] **L-11** 담당이 아닌 사람의 **체크리스트 쓰기가 전과 같이 거절**된다.
- [ ] **L-12** **프로젝트 밖** 읽기에서는 **항목이 안 오고** 집계만 온다.
- [ ] **L-13** **업무 내용(설명)이 전과 같이 온다.**
- [ ] **응답 타입이 안 바뀌었다** — 선택 필드의 **실리는 조건만** 바뀌었다.
      운영 대장 테스트가 **초록**이다(흔들리면 **그 항목만 패치**).
- [ ] **커밋 후 API 를 다시 띄웠다. 실제 응답 예시를 FE 브리프에 박았다.**

---

### Phase FE-4 — 간트 셋: **틀고정 · 첫 진입 오늘 · 좌 레일 자동 스크롤** (`D-35` 일부 · `D-36` · `D-37`)

- **Status**: TODO — **BE-3 이 닫힌 뒤**
- **닫는 SPEC 인수조건**: **L-36**(완료 바 색) · **L-42 ~ L-48**.
- **근거 결정**: **D-36**(틀고정 + 첫 진입 오늘 — 사용자 결정) · **D-37**(자동 스크롤 — 사용자 결정) ·
  **D-35 의 한 줄**(완료 바 투명 초록 — 사용자 결정).
- **설명**: **CSS 쪽이다. 간트를 다시 조립하지 않는다.**

**작업**

1. **라벨 칸을 가로 스크롤에 고정한다** — 조사 Q1 이 센 **①~③**(고정 선언 · **z-index** · **배경**).
   **배경이 없으면 막대가 비쳐 보여 고정 전보다 더 안 읽힌다.**
2. **머리줄에 축 스페이서 요소 하나**를 더한다(조사 Q1 ④) —
   지금 그 자리에 요소가 없어 **날짜 숫자가 라벨 칸 위로 올라온다.**
3. **첫 진입 스크롤** — 스크롤 컨테이너에 **ref** 를 달고 **「오늘」이 보이는 위치**로 맞춘다.
   **선례가 있다** — 캘린더 주 뷰가 같은 방식으로 첫 진입 위치를 잡고 **jsdom 이 그 값을 검사한다.**
   **두 값(라벨 폭 · 하루 폭)은 이미 계산돼 있다.**
4. **간트 → 좌 레일 자동 스크롤** — 선택이 바뀌면 **그 카드가 보이는 위치**로.
   **반대 방향(좌 레일 → 간트)도 같이 넣는다.**
5. **완료 바 fill 에 투명도를 얹는다** — **이 화면 CSS 에서.** **DS 토큰을 고치지 마라.**

**하지 말 것**

- **좌표계를 건드리지 마라** — 의존선 좌표 · 행 위치 · 막대 기하 · 접힘은 **안 움직인다.**
  **sticky 는 레이아웃 후 페인트 오프셋**이라 기존 값이 그대로 산다.
- **두 열로 가르지 마라** — **기각된 길**이다(D-36). 가르면 **의존선 좌표계 · 행 위치 ·
  접힘 배지 · 「행의 자손으로 막대를 찾는」 단언 11건**이 함께 깨진다.
- **DS 토큰 파일을 고치지 마라** (D-35).

**완료 판정**

- [ ] `make frontend-test`(**Node 20**) · `npx tsc --noEmit` **통과**.
- [ ] **L-42** 가로로 밀어도 **업무 이름이 남는다.**
- [ ] **L-43** 고정된 칸 위로 **막대·격자가 비치지 않는다.**
- [ ] **L-44** 머리줄의 그 칸 자리에 **날짜 숫자가 올라오지 않는다.**
- [ ] **L-45** 첫 진입에 **「오늘」이 보이는 위치**다 — 기간의 첫날이 아니다.
- [ ] **L-46** 간트 행을 고르면 **좌 레일이 그 카드로 스크롤**한다.
- [ ] **L-47** 좌 레일 카드를 고르면 **간트가 그 행이 보이는 위치**로 온다.
- [ ] **L-36** 완료 바가 다른 바와 톤이 맞고 **DS 토큰 파일이 한 줄도 안 바뀌었다.**
- [ ] **L-48** **1루프의 간트 계약이 그대로다**(회귀) — 손자 행 · 접어도 사라지지 않는 선 ·
      바의 % 규칙 · 들여쓰기. **간트 단언이 하나도 안 깨졌다.**

---

### Phase FE-5 — 헤더·좌 레일 헤더·우 레일: **생성 모달 · 업무 정보 · 상태 드롭다운 · 읽히게** (`D-30` ~ `D-35` · `D-38` · 정정 `D-39`)

- **Status**: TODO — **FE-4 뒤**
- **닫는 SPEC 인수조건**: **L-10** · **L-14 ~ L-22** · **L-24 ~ L-35** ·
  **L-37 ~ L-41** · **L-49 ~ L-52**(2루프 검수가 더한 상태 관문 넷).
  (**L-23 은 문서가 닫는다** — §인수조건 추적.)
- **근거 결정**: **D-30**(헤더 생성 버튼은 루프2 — 사용자 결정) · ~~**D-31**~~ → **D-39**(**2026-09-22 정정** — 게이트를 뺐다. 「빈 상태에서도 선다」는 그대로 산다 · 사용자 결정) ·
  **D-32**(상태 드롭다운 — 사용자 결정) · **D-33**(업무 정보 블록과 순서 — 사용자 결정) ·
  **D-34**(좌 레일 헤더 한 줄 — 사용자 결정) · **D-35**(제목·소제목 색 · 메타 표 셋 — 사용자 결정) ·
  **D-38**(설명·체크리스트는 업무 상세에서 — 코디 판단).
- **설명**: **2루프의 가장 넓은 자리**다. **BE-3 의 실물 응답을 보고 짠다.**

**작업**

0. **게이트가 읽을 값을 화면에 먼저 넘긴다 (`App.tsx` · 2루프 검수가 잡은 자리).**
   **`task.self_manage`** **하나**이고 **세션 봉투의 역량**이다.
   ⚠ **2026-09-22 정정 — 전에는 둘이었다.** ~~`project.manage`(생성 버튼 게이트 · D-31)~~ 는
   **안 넘긴다** — ~~D-31~~ 이 뒤집혀 **D-39** 가 **생성 버튼의 게이트를 없앴다.**
   **상태 드롭다운 쪽(`task.self_manage`)은 안 움직인다** — 이 배선이 없으면 **아래 7 의 게이트가 설 수 없다.**
   **다른 화면에 넘기는 값은 바꾸지 마라.**
1. **헤더에 「프로젝트 추가」를 등록한다** — **다른 탭과 같은 방식**(등록하고 **떠날 때 지운다**).
   ⚠ **게이트가 없다 (2026-09-22 정정 — ~~D-31~~ → D-39).** 전에는
   ~~「권한이 없으면 아무것도 등록하지 않는다 · 게이트는 만들 자격이고 「관리」의 `may_manage` 와
   다른 값이다」~~ 였다. **이제 이 버튼은 세션의 역량을 묻지 않고 누구에게나 선다** —
   **게이트가 붙는 것은 「관리」(`may_manage`) 하나뿐**이다.
   **만들 자격은 서버가 그대로 쥔다** — 역량 없는 사람이 실제로 만들려 하면
   `POST /api/projects` 가 거절하고 **그 문구는 모달 «안»에 선다**(생성 거절 넷 중 첫째 ·
   SPEC-005 §2.10 · §4 에러). **「버튼은 뜨고, 거절은 모달이 말한다」.**
2. **빈 상태 갈래에서도 헤더를 세운다** — 지금은 `Empty` 만 그리고 헤더도 레일도 안 선다.
   **본문은 한 문장 그대로 덮되(D-22) 헤더 버튼은 그 덮개 밖**이다.
3. **생성 전용 모달 — 네 칸.** 이름(필수) · 설명 · 시작일 · 종료일.
   **`external_key` 칸을 만들지 마라.** ⚠ **이유가 「API 가 안 받아서」가 아니다 (2026-09-22 정정)** —
   **표면은 그 값을 선택으로 받는다**(최대 200 · 중복이면 「이미 있는 프로젝트 key입니다」).
   **안 내는 이유는 그 값이 데이터셋 import 의 외부 식별자이고 사람이 손으로 채울 값이 아니기 때문**이다
   (SPEC-005 §2.10 · 미결 **OQ-607**). **FE api 래퍼도 지금 넷만 보낸다 — 그 래퍼를 넓히지 마라.**
   **다섯 밖의 필드를 보내면 거절**(422)되므로 칸을 더 만들면 **성공이 아니라 오류**다.
4. **관리 모달의 「새 프로젝트」 폼은 그대로 둔다** — **루프3 이 뗀다**(D-30).
5. **좌 레일 헤더를 한 줄로** — 아이콘 + **「프로젝트」** + **건수 배지**, **오른쪽 끝 셀렉터.**
   **배지는 기존 부품 그대로**(수신함·캘린더 레일이 쓰는 그것).
6. **우 레일 블록을 넷으로 재편** — **메타 정보 → 업무 정보 → 관계 → 하위 업무.**
   「업무 정보」가 **설명 + 체크리스트**를 든다.
7. **상태 드롭다운 — 「업무 화면 로직 그대로」는 «그 화면이 상태를 바꿀 때 지나는 모든 관문»이다.**
   ⚠ **2루프 검수 정정**: 이 항목은 처음에 **관문 둘**만 적었다. **전수는 SPEC-005 §2.6 ①②③** 이고
   아래가 그 요지다. **관문을 빼고 드롭다운만 옮기면 서버가 거절하는 전이를 화면이 보낸다.**
   선례 한 자리를 그대로 옮긴다 — `MyWorkPage.tsx` 의 `TaskStateCell`(`:1357-1444`).
   - **서는가 — 셋**: ① 세션에 **`task.self_manage`** 가 있나(위 작업 0) ② 업무 상세의
     **접근 값이 `owner`** 인가 ③ **갈 곳이 하나라도 있나**(`cancelled` · **승인 대기 중인 `done`**
     은 갈 곳이 없어 **글자**다 — `allowedTaskTransitions` 가 빈 배열을 준다).
     **게이트는 ①②로 둘이다** — ②만 보면 **역량 없는 담당자에게 드롭다운이 서고 서버가 매번 거절한다.**
     **수락 전 배정**은 접근 값이 이미 `read_only` 라 ②에서 걸린다.
   - **골랐을 때 — 넷**: ④ **지금 상태를 다시 고르면 무동작** ⑤ 허용 전이에 **없는 값이면 무동작**
     ⑥ **「막힘」은 `BlockReasonPrompt` 를 띄운다 — 사유 없이 전이를 보내지 마라**(**처음에 빠졌던 규칙**)
     ⑦ **요청 업무의 「완료」는 완료 보고 모달**로 간다(서버가 늘 거절한다). 그 모달 안에도 관문 둘이
     있다 — **결과 요약이 비면 못 보내고, 끝나지 않은 하위가 있으면 보고 자체가 막힌다.**
     ⚠ 그 모달에 `materials`·`subtasks` 를 **안 넘기면 스스로 읽는다** — 넘길지 말지를 정하고 짜라.
   - **보낼 때 — 셋**: ⑧ **보내는 중에는 트리거를 잠근다**(두 번 눌러 두 번 보내지 않는다)
     ⑨ **회차(`version`)를 동봉한다 — 「업무 상세로 읽은 그 업무」의 값**이다.
     **`tasks[]` 행의 값으로 보내지 마라 — 409 다.**
     ⑩ **낙관적 갱신 0건** — 성공하면 **다시 읽고**, 실패하면 **오류 문구만** 뜬다.
     **다시 읽는 범위는 업무 상세 하나가 아니라 프로젝트 상세까지**다(좌 레일 카드·간트 바가 같은 상태를 그린다).
   - **부품을 고치지 마라** — 허용 전이 계산 · `BlockReasonPrompt` · `CompletionReportModal` 셋 다
     `WorkModals.tsx` 가 export 한 것을 **가져다 쓴다.** 고치면 **업무 화면이 함께 움직인다.**
8. **읽히게 고치는 넷** — 제목·소제목 `ink-strong` · 메타 표 **값 정렬선** ·
   **행 높이 통일과 수직 가운데** · **버튼 시인성**(메타 표의 상위 업무 버튼 **과**
   관계 블록의 선행·후행 줄 **둘 다**). **누르면 그 업무로 가는 동작은 유지**한다.
9. **설명·체크리스트는 선택 업무의 업무 상세에서 읽는다** — **이미 걸려 있는 호출 그대로**다.
   **`tasks[]` 를 읽어서 그리지 마라.**
10. **접근 값으로 항목을 감추지 마라** — **`read_only` 인데 항목이 온 응답이 정상**이다.
    **화면은 「왔는가」로 그린다.**

**하지 말 것**

- **액션 버튼(재개·막힘·완료)을 옮기지 마라** — **상태 드롭다운만**이다(사용자 확정).
- **전이 규칙을 새로 쓰지 마라** — **업무 화면의 경로를 재사용**한다.
- **`src/ds/` 를 고치지 마라.**
- **관리 모달을 정리하지 마라** — 루프3 이다.

**완료 판정**

- [ ] `make frontend-test` · `npx tsc --noEmit` **통과**.
- [ ] **L-14 · L-18** 헤더에 「프로젝트 추가」가 서고 **떠나면 사라진다.**
- [ ] **L-15** **프로젝트 0개에서도 그 버튼이 선다** — 본문은 한 문장으로 덮여 있다.
- [ ] **L-16** **관리 권한 없는 프로젝트에서 관리 버튼은 없고 생성 버튼은 있다.**
- [ ] **L-17** **만들 자격이 없는 세션으로 열어도 버튼이 «선다»** — 헤더의 버튼이 **그 하나뿐**이고
      (관리 버튼만 빠진다), 거기서 실제로 만들려 하면 **서버의 거절 문구가 «모달 안»에 선다.**
      *(2026-09-22 정정 — 전에는 ~~「버튼 자체가 없다(비활성 버튼이 아니다)」~~ 를 쟀다. ~~D-31~~ → D-39)*
- [ ] **L-19 ~ L-21** 모달이 **네 칸**이고 `external_key` 칸이 없다(**계약은 다섯을 받는다** —
      화면이 안 내는 것이다) ·
      **공백만 넣으면 안 만들어진다** · **종료일이 앞서면 거절**된다.
- [ ] **L-22** 만든 사람이 **리드로 붙고** 셀렉터에 그 프로젝트가 뜬다.
- [ ] **L-24 ~ L-26** 블록 순서가 넷이고 **「업무 정보」가 설명+체크리스트**를 들며
      **설명이 없으면 그 자리를 비운다.**
- [ ] **L-27 ~ L-32** 내 업무면 **드롭다운**, 아니면 **읽기 배지** · 수락 전이면 **안 선다** ·
      **지금 상태가 목록에 있고** 다시 골라도 아무 일도 없다 ·
      **요청 업무의 완료는 완료 보고 모달**이 뜬다 · **액션 버튼이 없다.**
- [ ] **L-33** 우 레일이 **선택된 하나에만** 상세를 부르고
      **`tasks[]` 응답에 설명·체크리스트 항목 필드가 0건**이다.
- [ ] **L-34 · L-35** 좌 레일 헤더가 **한 줄**이고 배지가 **카드 수**와 같다.
- [ ] **L-37 ~ L-41** 제목·소제목이 `ink-strong` · 값 정렬선이 하나 · 행 높이 통일 ·
      **두 자리 버튼이 hover 없이도 보인다** · **누르면 여전히 선택된다.**
- [ ] **L-49 ~ L-52** **상태를 바꿀 때 지나는 관문이 전수로 산다** — 「막힘」이 **사유 입력**을 띄우고
      (사유 없이 전이가 안 나간다) · **게이트가 둘**이라 **역량 없는 세션에는 드롭다운이 안 서고** ·
      **갈 곳이 없는 업무**(취소 · 승인 대기 중인 `done`)는 **배지**이며 ·
      바꾼 뒤 **좌 레일 카드와 간트 바까지 새 상태**다(낙관적 갱신 0건).
      **`WorkModals.tsx` diff 가 0줄**인 것도 같이 본다.
- [ ] **L-17** **만들 자격이 없는 세션으로 열어도 버튼이 «선다»** — 봉투의 역량에 `project.manage` 가
      **없고** 그 프로젝트의 관리 권한도 **없는** 세션으로 이 화면을 렌더하면 **헤더에 「프로젝트 추가」가
      서고, 헤더의 버튼은 그 하나뿐이다**(관리 버튼만 빠진다). 그리고 **거기서 실제로 만들려 하면
      서버의 거절 문구가 «모달 안»에 선다.** 데모 페르소나에 기대지 않고 **코드 자리로** 잰다
      — 그 역량을 뺀 세션 값으로 렌더한 단언이다(SPEC-005 §6 **L-17** 과 같은 문장).
      > **2026-09-22 정정 — 이 줄은 «뒤집혔지 삭제되지 않았다».**
      > 전에는 ~~「`project.manage` 를 뺀 세션 값으로 렌더하면 헤더 등록 노드가 `null` 이다」~~ 를 쟀다.
      > **~~D-31~~ 이 뒤집혀 그 인수조건이 거짓이 됐고**(D-39), **같은 자리에서 반대 사실**을 잰다.
      > 재는 대상은 그대로 **「자격 없는 세션의 헤더」**다. **FE 가 코드에서 먼저 뒤집었다**
      > (`loop2-final-fix-report.md` §A-2 — 삭제·skip 0건, 새 계약을 재게 다시 썼다).
- [ ] **L-10** **접근 값이 `read_only` 인데 항목이 온 응답을 정상으로 그린다** —
      접근 값으로 감추는 자리가 **0건**이다.
- [ ] **1루프의 화면 계약이 그대로다**(회귀) — 선택 축 하나 · 빈 상태 · 관리 모달 손잡이 ·
      후행 역산 · 요약 스트립 셈.
- [ ] **최종 `make verify` 가 exit 0** (§검증 계획).

## 검증 계획

**백엔드는 Makefile 타겟으로만 실행한다. `uv run pytest` 직접 호출 금지**(`AGENTS.md`).

| 단계 | 명령 | 언제 |
|---|---|---|
| 도메인·구조 | `make test-unit` (= `tests/unit` + `tests/architecture`) | BE-1 · BE-2 |
| 외부 계약 | `make test-contract` | **착수 전(기준선)** · BE-1 · BE-2 |
| **이번 판 계약만 직렬** | `make test-contract-serial FILES="..."` (BE-1 이 더한 타겟, **`-n0`**) | BE-1 · BE-2 · FE-3(최종) |
| DB·제약·동시성 | `make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_projects` | **BE-2**(회귀) |
| 인벤토리 | `make test-unit` 안의 `tests/architecture/test_operation_inventory.py` | **BE-1** |
| 화면 | `make frontend-test` (**Node 20**) | FE-1 · FE-2 · FE-3 |
| 타입 | `cd frontend && npx tsc --noEmit` | FE-1 · FE-2 · FE-3 |
| 전체 | `make verify` | **FE-3 에서 한 번** — **exit code 를 통과 조건으로 삼지 않는다**(아래) |

**테스트 범위의 적정선** — Phase 마다 **그 Phase 가 바꾼 계약**을 돌린다.
**같은 스위트를 Phase 마다 반복하지 않는다.**

### **첨부(`material_*`)를 제외한 채로 초록을 증명하는 법 — 3단 절차**

**`make verify` 가 exit 0 를 못 볼 수 있다.** 그 계열이 `-n auto` 병렬에서 흔들리고
**원인이 아직 규명되지 않았다**(Phase 0). 그래서 **초록의 증명을 세 조각으로 나눈다.**

**① 이번 판이 더한 계약 테스트를 직렬로 따로 돌린다 — 전부 통과를 보인다**

```text
make test-contract-serial FILES="tests/contract/test_projects.py \
                                 tests/contract/test_project_commands.py \
                                 tests/contract/test_task_assignments.py \
                                 tests/contract/test_task_predecessors.py"
```

- **`-n0`** — **병렬을 끈다.** 캘린더 판의 결정적 관측이 그것이었다 — **직렬로 돌리면 전부 통과한다.**
  **`-p no:randomly` 는 뺐다** — 이 저장소에 랜덤 플러그인이 없어 **무동작**이고,
  「둘 다 끈다」는 말이 거짓이 된다(캘린더 재료가 적은 같은 플래그도 무해한 no-op 이었다).
- **이 목록이 「이번 판이 더한 것」의 전부여야 한다.** 파일을 더 만들면 이 줄도 같이 는다.
- **이것이 「우리가 더한 계약이 초록이다」의 증명**이다.

**② 기준선 실패를 분리 보고한다 — 착수 전에 먼저 재어 둔다**

- **회차 0(착수 전)**: 코드를 한 줄도 안 고친 상태에서 `make test-contract` 를 **한 번** 돌리고
  **통과 수 · 실패 수 · 실패 «파일 집합»** 을 기록한다.
- **회차 1~5**: Phase 끝마다 같은 명령을 돌리고 같은 세 값을 기록한다.
- 기록 자리: `orchestration/work/strong-hajin-projects/flaky-baseline-projects.md`.
  표 한 장이면 된다 — **회차 · 통과 · 실패 · 실패 파일 집합 · 그 회차에 우리가 바꾼 것.**
- **판정은 파일 집합으로 한다. 수로 하지 않는다.**

  | 무엇 | 뜻 |
  |---|---|
  | 실패 파일이 **기준선 ∪ `material_*` 계열** 안에 있다 | **이번 변경과 무관하다.** 그대로 보고한다 |
  | 실패 파일이 **그 밖에 있다** | **이번 변경 탓이다.** 고친다 |
  | 같은 계열이 **회차마다 들고 난다** | **flaky 의 증거**다 — 그 사실 자체를 기록한다 |

- **우리가 `material_*` 계열을 겨눈 테스트를 더하지도 고치지도 않는다.**
  다만 **스위트가 그 계열을 함께 도는 것은 막지 않는다** — 막으면 회차 기록이 안 생기고,
  **그 기록이 내일 Phase 0 의 입력**이다.

**③ 그 기록이 Phase 0 의 입력이다**

- **어느 파일이 어느 회차에 흔들렸는지**가 원인 규명의 재료다.
- **계약 테스트가 늘수록 빈도가 는다**는 가설을 이번 판이 **다시 한 번 재는 것**이기도 하다 —
  우리도 계약 테스트를 더한다.
- **1루프가 원인을 고치려 들지 않는다.** 재료만 남긴다.

**`make verify` 의 판정 (FE-3 에서 한 번)**

- [ ] 돌린다. **exit code 가 0 이 아니어도 그 자체로 실패가 아니다.**
- [ ] **실패 목록이 「기준선 ∪ `material_*` 계열」 안에 전부 든다.**
- [ ] **이번 판이 더한 파일이 그 목록에 0건**이다.
- [ ] 위 ①이 **통과**다.
- [ ] 셋이 다 참이면 **1루프의 초록으로 인정하고**, 남은 exit code 는 **Phase 0 으로 넘긴다.**
- [ ] `frontend-test`·`frontend-assets`·`frontend-build` 는 **exit 0 여야 한다** —
      그쪽은 flaky 와 무관하다.

**하지 않을 것**

- 기존 테스트를 **편의상 삭제·skip·단언 약화** 하지 않는다. 깨지면 **계약이 바뀐 것인지
  구현이 틀린 것인지**를 먼저 가른다.
- **`material_*` 을 겨눈 테스트를 더하거나 고치지 않는다** — 1루프 범위 밖이다.
- **`docs/unified-operations-inventory.json` 전체 재작성 금지** — diff 난 항목만.
- **과거 수치를 이번 통과 근거로 쓰지 않는다.** SPEC-005 스스로 「이번 작업에서 실행한 테스트는 0건」이라 적었다.
- **SQLite 선언을 제약의 증거로 쓰지 않는다.**
- **브라우저에서 눈으로 본 것을 에이전트가 「확인했다」고 쓰지 않는다** — 그 칸은 사용자 것이다.

### 2루프의 검증 — **기준선이 바뀌었다. 이제 「실패 0」이다** *(2026-09-22)*

**Phase 0 가 닫혔다.** `make verify` 가 **exit 0** 를 낸다(코디 실측 2026-09-22).
**그래서 1루프의 3단 절차(기준선 분리)는 2루프에 적용되지 않는다.**

| 무엇 | 1루프 | **2루프** |
|---|---|---|
| `make verify` | **exit code 를 통과 조건으로 삼지 않았다** — 실패가 「기준선 ∪ `material_*`」 안에 들면 초록으로 인정 | **exit 0 가 통과 조건이다** |
| 판정 | **실패 파일 «집합»** 으로 판정 | **실패 0** 으로 판정 |
| 회차 기록 | `flaky-baseline-projects.md` 회차 0~5 | **더 이상 필요 없다** — 기준선이 초록이다. ⚠ **다시 흔들리면 그때는 「이번 변경 탓」이 기본 가설**이다 |

- **Phase 마다 그 Phase 가 바꾼 계약을 돌린다** — 1루프와 같다.
  **BE-3**: `make test-unit` · `make test-contract`. **FE-4 · FE-5**: `make frontend-test`(Node 20) ·
  `npx tsc --noEmit`. **FE-5 끝에 `make verify` 한 번.**
- **`make test-postgres` 는 2루프에 필요 없다** — **표도 컬럼도 제약도 안 는다**(§Domain / Schema).
  ⚠ 다만 **BE-3 이 권한 분기를 건드리므로** 그 계열 계약 테스트는 **반드시 돈다.**

**`@pytest.mark.serial` 마커 규약 — 새 테스트를 만들 때 지킨다**

이 저장소는 **자식 프로세스를 띄우는 테스트**(IsolatedWork spawn · MCP stdio · subprocess)를
**병렬 패스에서 뺀다.** 그 부류는 **`@pytest.mark.serial` 을 달고 `Makefile` 이 `-m` 으로 갈라 돈다** —
병렬 패스는 `-m "… and not serial"`, 직렬 패스(`make test-serial`)는 `-m serial -n0` 이다
(`backend/pyproject.toml` 의 마커 선언 · `backend/tests/conftest.py` 의 걸개).

- **새로 만드는 테스트가 자식 프로세스를 띄우면 그 마커를 달아야 한다.**
- **안 달면 conftest 의 걸개가 즉시 실패시킨다** — 「`@pytest.mark.serial` 을 달아
  직렬 패스로 보내라」는 메시지와 함께다. **조용히 통과하는 길이 없다.**
- **2루프가 그런 테스트를 만들 이유는 없어 보인다** — BE-3 은 **권한 분기와 응답 투영**이다.
  **그래도 규약을 여기 적어 둔다** — 만들게 되면 **마커가 먼저**다.
- **파일 이름으로 가르지 않는다** — 가르는 것은 **마커**다. `make test-contract-serial FILES=…`
  은 **격리 수단이 아니라 재실행 편의**다(1루프가 더한 타겟).

**하지 않을 것 (2루프도 같다)**

- 테스트 **삭제·skip·단언 약화로 초록을 만들지 않는다.**
  ⚠ **BE-3 은 테스트 하나를 실제로 다시 쓴다** — **그것은 「주장이 뒤집혔기 때문」**이고,
  **이름·docstring·단언을 새 계약으로 다시 쓰는 것**이지 **약화가 아니다.** 그 차이를 보고에 적는다.
- **브라우저에서 눈으로 본 것을 에이전트가 「확인했다」고 쓰지 않는다** — 그 칸은 사용자 것이다.
- **운영 대장 전체 재작성 금지** — diff 난 항목만.

### 검증 책임의 경계

| 무엇 | 누가 |
|---|---|
| API 응답값·오류·권한·동시성·DB 회귀 | **에이전트(자동)** |
| FE 단위 테스트·타입·빌드 | **에이전트(자동)** |
| **브라우저에서 눈으로 보는 것** — 배치·간격·문구·읽히는가·선이 사라지지 않는가 | **사용자(E2E · 2루프)** |
| **`material_*` 병렬 격리** | **사용자 동반 (Phase 0 · 2루프)** |
| 통합 검증·PR | **코디네이터** |

**1루프는 계약을 세우는 판이다. 픽셀·간격·문구는 2루프가 잡는다** —
1루프에서 레이아웃을 완벽히 맞추려 시간을 쓰지 않는다.

## 인수조건 추적 — 어느 Phase 가 SPEC §6 의 어느 줄을 닫나

**SPEC-005 §6 인수조건은 10묶음 · 76줄이다. 전수 매핑한다 — 닫는 Phase 가 없는 줄은 없다.**
> **75 → 76.** **구현이 드러낸 사실**을 반영하면서 **자동 해제 묶음이 한 줄 늘었다** —
> 「배정 철회는 **메서드 수준**에서 돈다」와 「그 철회에 **표면이 오늘 없다**」를 **갈라 적었기 때문**이다.
> **없는 표면을 테스트가 증명할 수 없으므로 두 줄은 관측 방법이 다르다.**

| # | 묶음 | 줄 수 | 닫는 Phase | 확인 방법 |
|---|---|---|---|---|
| A | **핵심 넷** (D-16·D-17·D-11~D-14·D-19) | **6** | **BE-2**(3줄 — 프로젝트 밖 사람 초대 · 거절하면 떼어짐 · 상위 옮기면 손자까지) · **FE-2**(3줄 — 손자 행 · 손자에 걸린 선 · 접어도 안 사라짐) | `make test-contract` · `make frontend-test` · **E2E E-1~E-3·E-9·E-10·E-15** |
| B | 간트와 트리 (D-16·D-18·D-09) | **8** | **FE-2**(6줄) · **BE-1↔FE-2 갈라짐**(2줄 — 한쪽 날짜만 · 뒤집힌 기간) | `make frontend-test` · `npx tsc --noEmit` · E2E E-4 |
| C | 의존선 (D-07·D-16·D-17) | **5** | **FE-2**(4줄) · **FE-3**(1줄 — **후행 목록이 우 레일에 나온다**. 우 레일은 FE-3 이 만든다) | `make frontend-test` · **후행 호출 0건은 호출 수로 센다** |
| D | 진행률 (D-01~D-04) | **13** | **BE-1**(1줄 — 저장 컬럼이 늘지 않았다) · **FE-1**(5줄 — 요약 스트립) · **FE-2**(5줄 — 바의 %) · **FE-3**(1줄 — 우 레일 미터 「—」) · **FE-1↔FE-2 갈라짐**(1줄 — 취소가 간트와 좌 레일에 남는다) | `make test-contract` · `make frontend-test` · E2E E-5·E-6 |
| E | 상태 어휘 (D-06 · SPEC-003 M-6 승계 · 어긋남 ①) | **7** | **BE-1**(2줄) · **FE-1**(3줄) · **FE-1↔FE-2 갈라짐**(1줄 — `blocked` 를 배지와 바가 같이 그린다) · **문서**(1줄 — 「계약 어휘를 안 넓혔다」) | `make test-contract` · `make frontend-test` · **문서 줄은 SPEC §2.9 와 이 WP 가 닫는다** |
| F | 좌 레일과 우 레일 (D-08·D-20) | **8** | **FE-1**(3줄) · **FE-3**(4줄) · **FE-1↔FE-2↔FE-3 갈라짐**(1줄 — 선택 하나가 넷을 움직인다) | `make frontend-test` · E2E E-7·E-8 |
| G | 관리 모달과 빈 상태 (D-05·D-21·D-22·D-24) | **7** | **FE-1**(1줄 — 프로젝트 0개 빈 상태) · **FE-3**(6줄) | `make frontend-test` · E2E E-17·E-18 |
| H | 자동 초대 (D-11 · ~~D-12~~ → D-28) | **7** | **BE-2** | `make test-contract` · E2E E-9 |
| I | 자동 해제 (D-13·D-14·D-15) | **10** | **BE-2** | `make test-contract`(표면 셋은 라우트로 · **배정 철회는 메서드로**) · **표면이 없다는 한 줄은 코드 자리로** · E2E E-10~E-14 |
| J | 손자 프로젝트 종속 (D-19) | **5** | **BE-2** | `make test-contract` · `make test-postgres`(회귀) · E2E E-15·E-16 |
| | **합계** | **76** | | |

**Phase 별 부담**

| 루프 | Phase | 대략 |
|---|---|---|
| 1루프 | **BE-1** | D1 + E2 = **3** (+ B 의 갈라지는 2줄의 BE 절반) |
| 1루프 | **BE-2** | A3 + H7 + I10 + J5 = **25** |
| 1루프 | **FE-1** | D5 + E3 + F3 + G1 = **12** |
| 1루프 | **FE-2** | A3 + B6 + C4 + D5 = **18** |
| 1루프 | **FE-3** | C1 + D1 + F4 + G6 = **12** |
| — | **문서** | **1** (E 의 「계약 어휘를 안 넓혔다」) |
| — | **갈라지는 줄** | **5** (아래 표) |
| | | **합 76** |

> **「계약 어휘를 안 넓혔다」 한 줄은 구현이 닫지 않는다.** SPEC §2.9·§4 가 계약으로 적었고
> 이 WP 가 그 말을 따른다 — `blocked` 를 **계약 어휘로 올리는 문장이 이 문서 어디에도 없다.**
> **Phase 에 매달 자리가 없어 여기 명시한다** — 「닫는 Phase 가 없다」로 읽히지 않게.

### 갈라지는 줄 — 어느 절반이 어느 Phase 인가

**한 줄이 두 Phase 에 걸치는 자리만** 따로 적는다. 나머지는 위 표의 묶음 단위로 닫힌다.

| SPEC §6 의 줄 | BE / 앞쪽 절반 | FE / 뒤쪽 절반 |
|---|---|---|
| 「**한쪽 날짜만 있는 업무는 그 날 하루짜리 바**가 된다 — 화면이 그 규칙을 다시 계산하지 않는다」 | `span_from`·`span_to` 를 서버가 낸다 (BE-1) | 그 값으로 바를 그린다 (FE-2) |
| 「**뒤집힌 기간은 정규화된 구간**으로 그려진다 — 빈 바가 아니다」 | `task_span()` 의 `[min, max]` (BE-1) | 그리기 (FE-2) |
| 「그 취소 2건이 **간트에는 그대로 서고 좌 레일 카드에도 남는다**」 | — | 좌 레일 (FE-1) · 간트 취소선 바 (FE-2) |
| 「`blocked` 가 실제로 오면 **배지가 「막힘 / `danger`」이고 간트 바가 `danger-soft`/`danger`**」 | — | 배지 (FE-1) · 바 (FE-2) |
| 「선택 하나가 **좌 레일 · 간트 행 · 의존선 · 우 레일** 넷을 동시에 움직인다」 | — | 좌 레일 (FE-1) · 간트·의존선 (FE-2) · 우 레일 (FE-3) |

### 2루프 인수조건 배정 — **L-01 ~ L-52 전수. 누락 0** *(2026-09-22)*

**SPEC-005 §6 의 2루프 묶음 일곱(52줄)을 세 Phase 에 전수 배정한다.**
> **48 → 52.** 2루프 문서 검수가 **상태 드롭다운의 관문 넷**을 더했다(L-49 ~ L-52 · 마지막 묶음).
> **기존 48줄의 번호도 배정도 안 바뀌었다** — 새 묶음이 뒤에 붙었을 뿐이다.
**1루프의 76줄 표는 기록이라 건드리지 않는다** — 이 표가 그 뒤에 붙는다.

| 묶음 | 줄 | 줄 수 | 닫는 Phase | 확인 방법 |
|---|---|---|---|---|
| **게이트 제거** (D-28) | **L-01 ~ L-06** | **6** | **BE-3** | `make test-contract`(뒤집힌 테스트 재작성 포함) · E2E **E-20** |
| **읽기 범위 — 서버** (D-29) | **L-07 · L-08 · L-09 · L-11 · L-12 · L-13** | **6** | **BE-3** | `make test-contract` 셋(같은 프로젝트에서 온다 / 쓰기는 거절 / 밖에서는 안 온다) · E2E **E-21 · E-22** |
| **읽기 범위 — 화면** (D-29) | **L-10** | **1** | **FE-5** | `make frontend-test` — **접근 값으로 감추는 자리가 0건**임을 단언으로 |
| **프로젝트 만들기** (D-30 · ~~D-31~~ → **D-39**) | **L-14 ~ L-22** | **9** | **FE-5** | `make frontend-test` · E2E **E-23 ~ E-25** |
| **루프2 중복의 기록** (D-30) | **L-23** | **1** | **문서** | SPEC-005 §2.7 · §2.10 · 이 문서 `Open Issues` — **구현이 닫지 않는다** |
| **우 레일 재편과 상태 드롭다운** (D-32 · D-33 · D-38) | **L-24 ~ L-33** | **10** | **FE-5** | `make frontend-test` · `npx tsc --noEmit` · E2E **E-29 · E-30** |
| **좌 레일 헤더** (D-34) | **L-34 · L-35** | **2** | **FE-5** | `make frontend-test` · E2E **E-32** |
| **완료 바 색** (D-35) | **L-36** | **1** | **FE-4** | 눈 + **DS 토큰 파일 diff 0줄** · E2E **E-32** |
| **읽히게 — 우 레일** (D-35) | **L-37 ~ L-41** | **5** | **FE-5** | `make frontend-test`(선택 유지 단언) · E2E **E-31** |
| **간트** (D-36 · D-37) | **L-42 ~ L-48** | **7** | **FE-4** | `make frontend-test` · E2E **E-26 ~ E-28** · **L-48 은 1루프 간트 단언의 회귀** |
| **상태 드롭다운의 관문** (D-32 · 검수 보강) | **L-49 ~ L-52** | **4** | **FE-5** | `make frontend-test`(막힘 사유 · 역량 없는 세션 · 갈 곳 없는 업무 · 다시 읽기) · **`WorkModals.tsx` diff 0줄** · E2E **E-29 · E-30** |
| | **합계** | **52** | | |

**Phase 별 부담 (2루프)**

| Phase | 줄 수 | 무엇 |
|---|---|---|
| **BE-3** | **12** (L-01~L-09 · L-11~L-13) | 게이트 제거 + 읽기 범위의 서버 절반 |
| **FE-4** | **8** (L-36 · L-42~L-48) | 간트 셋 + 완료 바 색 |
| **FE-5** | **31** (L-10 · L-14~L-22 · L-24~L-35 · L-37~L-41 · **L-49~L-52**) | 헤더 · 생성 모달 · 좌 레일 헤더 · 우 레일 전부 · **상태 관문 넷** |
| **문서** | **1** (L-23) | 루프2 중복이 **적혀 있다** |
| | **합 52** | |

**절반이 갈리는 줄 — 둘**

| 줄 | 서버 절반 | 화면 절반 |
|---|---|---|
| **L-10** 「접근 값이 `read_only` 인데 항목이 실린 응답을 정상으로 그린다」 | **그 조합을 실제로 만드는 것**은 BE-3 이고 **L-07 이 그것을 잰다** | **감추지 않고 그리는 것**이 FE-5 다 — **이 줄의 배정은 FE-5** |
| **L-12** 「프로젝트 밖에서는 항목이 안 실리고 집계·미터만 그려진다」 | **안 싣는 것**이 BE-3 다 — **이 줄의 배정은 BE-3** | **집계·미터를 그리는 것**은 **1루프 FE-3 이 이미 닫았다**(회귀) |

> **L-23 은 구현이 닫지 않는다.** 「루프2 동안 생성 경로가 둘인 것이 적혀 있다」는
> **문서의 줄**이다 — **Phase 에 매달 자리가 없어 여기 명시한다**(1루프의
> 「계약 어휘를 안 넓혔다」와 같은 취급).

### SPEC 밖에서 이 work 가 여는 인수조건 — **셋**

**아래 셋은 SPEC-005 §6 의 (1루프) 76줄에 없다.** 위 합계에도 들어가지 않는다.
**여기서 정하고 여기서 증명한다.**

**M-1 — 관리 모달의 어휘** (시안이 없어 코디 자율로 정해진 자리) — **FE-3**

- [ ] 모달이 시안 `work-modal.jsx` 의 **`Modal`·`Field`·`TextField`·`AutoComplete` 어휘**로 서 있다
      (`scax-modal-*` · `scax-field*` · `scax-textfield*`).
- [ ] **새 부품을 발명하지 않았고**, 옮긴 기능의 **필드가 늘거나 줄지 않았다** —
      참여자 붙이기/떼기(사유 입력 포함) · 참여 이력 · 새 프로젝트 만들기 셋 그대로.
- [ ] **`src/ds/` 를 한 줄도 안 고쳤다.**

**M-2 — 기존 화면 테스트의 이사** — **FE-3**

- [ ] `ProjectPage.test.tsx` 의 검사가 **삭제 0건**이고, 깨진 여섯이 **옮겨간 자리를 겨눈다.**
- [ ] 특히 `may_manage` 검사(#3)가 **모달 손잡이 렌더 여부**로 살아 있다 —
      권한 검사가 이사 중에 사라지지 않았다.

**M-3 — 기준선 분리 기록** — **BE-1 ~ FE-3 전 회차**

- [ ] `flaky-baseline-projects.md` 에 **회차 0~5** 가 있고, 각 회차에
      **통과 수 · 실패 수 · 실패 파일 집합 · 그 회차에 바꾼 것**이 적혀 있다.
- [ ] **이번 판이 더한 파일이 그 실패 집합에 한 번도 안 들었다.**
- [ ] 그 기록이 **Phase 0 의 입력으로 인계됐다.**

> **왜 SPEC 에 없나.** M-1 은 **시안이 없는 자리**라 SPEC §1 Scope Out 이 그 층을 `30-work/` 로 보냈고,
> M-2 는 화면 테스트라 같은 자리이며, M-3 은 **검증 절차**이지 계약이 아니다.
> **SPEC 을 고치지 않는다** — 필요해지면 SPEC 환류로 올린다.

## Pre-deploy Check

- [ ] **배포 직전 실제 데이터 DB 에서 컬럼 실재를 확인한다.** Phase BE-2 의 격리 DB 통과는
      이 조건의 근거가 아니다 — `information_schema` 에 **다시 묻는다.**
- [ ] `task_assignments.auto_project_join` 이 **실재한다**(없으면 만들었다).
      **`work_requests` 에는 더한 열이 없다.**
- [ ] **`--sync` 의 `manual[]` 출력이 비어 있다** — NOT NULL 인데 기본값 없는 열이 남지 않았다.
- [ ] **코드 배포 전에 컬럼이 먼저** 있다(스키마 → 코드).
- [ ] **기존 서비스 영향 없음** — 업무 생성·수정·시작·제안 동의 · 요청 발송·거절·철회 ·
      배정·담당 교체·수락·거절·철회 · 프로젝트 관리 화면이 **그대로 돈다.**
- [ ] **`GET /api/projects/{project_id}` 의 기존 여섯 필드가 이름도 뜻도 안 바뀌었다** —
      **더해지기만 했다.**
- [ ] `docs/unified-operations-inventory.json` 의 `http_count` 가 **159**, `tool_count` 가 **129** 다.
      **`acceptance_evidence` 가 보존됐다.**
- [ ] credential·env 를 새로 노출하지 않는다 (**이번에 추가한 외부 의존이 없다**).
- [ ] **운영·사용자 DB 초기화가 절차에 없다.**
- [ ] 응답에 **읽을 수 없는 업무·프로젝트의 제목이나 건수**가 새지 않는다 —
      읽을 수 없는 선행은 **제목을 감추고 건수는 낸다**는 기존 결을 지킨다.
- [ ] **읽을 수 없는 프로젝트가 여전히 「없는 것처럼」 답한다** — 자동 초대가 그 규칙을 안 뚫었다.

## Rollback

- **코드 롤백** — 배포 단위를 **BE-1(읽기 확장)** 과 **BE-2(도메인 수정)** 로 갈라 두었으므로
  BE-2 만 되돌릴 수 있다. 되돌리면 **자동 초대·자동 해제가 안 돌고 손자가 다시 옛 프로젝트에 남는다** —
  **잘못된 상태가 아니라 옛 동작**이다(어긋남 ③·④ 가 돌아온다).
- **BE-1 만 되돌리면** 화면이 담당·진행률·기한 경과를 못 받는다 — **FE 와 같이 되돌려야 한다.**
  **FE 는 BE-1 없이 설 수 없다** (§Internal Interface Contract).
- **컬럼** — **되돌리지 않는 것이 기본이다.** nullable 이고 기존 코드가 모르므로 남아 있어도 무해하다.
  지우면 **그 사이에 「이 요청이 붙였다」로 기록된 사실이 사라진다** —
  그러면 이후 거절에서 **원래 멤버와 구별할 수 없어진다**(D-14 조건 ①).
- **인덱스** — **더한 것이 없다.** 되돌릴 것도 없다.
- **이미 붙은 참여를 소급해 떼지 않는다.** BE-2 를 되돌려도 **그 사람들은 프로젝트에 남는다** —
  **사람이 관리 모달에서 직접 뗄 수 있고**, 그것이 **원래 있던 문**이다.
- **이미 옮겨진 손자를 소급해 되돌리지 않는다.** 그 데이터는 **고쳐진 것**이지 망가진 것이 아니다.
- **운영 대장** — `get_project` 도구 스키마를 되돌린다. **전체 재작성이 아니라 그 항목만.**
- **화면 롤백** — 옛 `ProjectPage` 로 되돌리면 **관리 기능이 본문으로 돌아온다.**
  기능이 사라지지 않는다 — **자리만 돌아간다.**

## Done Criteria

- [ ] **1루프 다섯 Phase**(BE-1 · BE-2 · FE-1 · FE-2 · FE-3)가 전부 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-005 §6 인수조건 (1루프) 76줄 전항**이 「데이터: 에이전트」 칸까지 자동검증으로 확인됐다
      (「계약 어휘를 안 넓혔다」 한 줄은 **문서가 닫는다**).
- [ ] **핵심 넷이 실제로 선다** — 손자 행 · 접어도 안 사라지는 의존선 ·
      프로젝트 밖 사람 초대와 거절 시 해제 · 이동 시 손자 추종.
- [ ] **BASE-004 어긋남 ①·③·④ 가 고쳐졌고**, ②·⑤ 는 **기록으로 남았다.**
- [ ] **새 라우트 0건 · 새 MCP 도구 0건 · 새 오류 코드 0건**이 grep 으로 남았다.
- [ ] **진행률 저장 컬럼이 0개**다 — 응답 어디에도 저장된 % 가 없다.
- [ ] **후행을 서버에 묻는 경로가 0건**이다.
- [ ] **`src/ds/` 와 `.design-sync/` 가 한 줄도 안 바뀌었다.**
- [ ] **사이드바·내비 순서가 안 바뀌었다.**
- [ ] **§검증 계획의 3단 절차**가 돌았고, ①이 통과이며 ②의 회차 기록 **0~5** 가 남았다.
- [ ] **운영 대장이 `http_count` 159 · `tool_count` 129** 로 통과했고 `acceptance_evidence` 가 보존됐다.
      **diff 가 `get_project` 도구 한 행**이내다.
- [ ] **M-1 · M-2 · M-3** 이 각각 증명됐다.
- [ ] **SPEC 환류 후보가 「지도 한 줄」 하나로 유지됐다** — 구현 중 새 외부 계약이 필요해지면
      **몰래 넣지 않고** 환류로 올렸다(`Open Issues`).
- [ ] **Phase 0 가 사용자와 함께 닫혔다** (2루프) — 또는 **왜 안 닫혔는지가 적혔다.**
- [ ] **브라우저 E2E 는 사용자가 수행**했고 그 결과가 기록됐다(**시안 대조 포함**).
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

**2루프 (D-28 ~ D-38 · 2026-09-22)**

- [ ] **Phase BE-3 · FE-4 · FE-5 가 그 순서로 `DONE`** 이다 — **BE 가 FE 보다 먼저 닫혔다.**
- [ ] **SPEC-005 §6 의 L-01 ~ L-52 전항**이 배정된 Phase 에서 확인됐다
      (**L-23 은 문서가 닫는다**).
- [ ] **`make verify` 가 exit 0** 다 — **실패 0.** 기준선 분리 절차를 쓰지 않았다.
- [ ] **새 라우트 0건 · 새 MCP 도구 0건 · 새 오류 코드 0건**이 grep 으로 남았다 (2루프도).
- [ ] **표도 컬럼도 안 늘었다** — 스키마 diff 0.
- [ ] **체크리스트 쓰기 가드가 한 줄도 안 바뀌었다.**
- [ ] **`src/ds/` 와 `.design-sync/` 가 여전히 한 줄도 안 바뀌었다** — 완료 바 색도 화면 CSS 다.
- [ ] **`tasks[]` 에 업무 내용·체크리스트 항목이 실리지 않는다** — 응답 grep 0건.
- [ ] **뒤집힌 테스트가 재작성됐고 삭제·skip·약화가 0건**이다.
- [ ] **관리 모달의 「새 프로젝트」 폼이 그대로 있다** — 루프3 이 뗀다.
- [ ] **루프2 의 중복(생성 경로 둘)이 세 문서에 적혀 있다.**
- [ ] **브라우저 E2E 2차를 사용자가 수행**했고(E-1~E-19 회귀 + E-20~E-32) 그 결과가 기록됐다.
- [ ] **미결 넷(OQ-604 · OQ-605 · OQ-606 · OQ-607)이 닫혔거나 왜 안 닫혔는지가 적혔다.**

## Open Issues

### 2루프가 남긴 것 — **루프3 으로 미룬 셋 · 미결 넷** *(2026-09-22)*

**루프3 으로 미룬 것 — 셋. 보류가 아니라 순서다.**

- **관리 모달 정리(생성 폼 제거)** — 그 안의 「새 프로젝트」 폼(입력 칸이 **이름 하나**)을 **뗀다**
  **(확정 — D-30, 사용자 결정)**. ⚠ **그래서 루프2 동안 생성 경로가 두 자리에 있다** —
  헤더의 새 모달(네 칸)과 관리 모달의 옛 폼(한 칸). **둘 다 같은 표면을 부르므로 계약은 하나**이고,
  **이것은 감수하는 중복이지 조용한 중복이 아니다**(SPEC-005 §2.7 · §2.10 · 인수조건 **L-23**).
  **영구히 둘 다 두는 것은 DEC-004 § 기각이다.**
- **리드 권한 부여·교체 화면** — **프로젝트 설정 화면의 일이고 그 화면부터 없다**
  (D-28 범위 밖 · 백로그 A-1 「범위 밖」). `member → lead` 승격 경로가 **보류**인 것과 같은 자리다 —
  **붙이는 명령에 그 길이 없다.** 그 화면이 나는 판에서 **둘을 같이 연다.**
- **떼는 자리 #4(배정 철회)의 표면** — 1루프가 **메서드 수준까지 증명**했고
  **그 배정에 철회 명령이 서게 하는 일**은 그 판의 몫이다(아래 1루프 항목이 근거를 갖는다).
  **문이 나는 날 그 메서드 테스트가 표면 테스트로 올라온다.**

**미결 넷 — 추측으로 메우지 않았다.**

- **OQ-604 — 체크리스트 항목이 안 실리는 갈래의 문구.** 지금 문구는
  「항목은 이 업무를 맡은 사람에게만 보입니다」인데 **D-29 가 그 말을 틀리게 만든다.**
  남는 갈래는 **프로젝트 밖에서 그 업무를 읽는 경우**뿐이고, **그 갈래가 실제로 얼마나 있는지도
  이 판에서 세지 않았다.** ⚠ 함께 물을 것 — **B-9 의 재현 조건**(막대 40% 인 업무에서 사용자가 본
  문구가 **ⓐ「등록된 항목이 없습니다」였나 ⓑ「…맡은 사람에게만 보입니다」였나**).
  **ⓑ 면 버그가 아니라 문구다.** **사용자 한 줄 확인**이 답이다.
- **OQ-605 — 좌 레일 건수 배지가 「프로젝트」 문구 옆에 서는데 세는 것은 업무 수다.**
  「프로젝트 (11)」이 **프로젝트 11개로 읽힐 수 있다.** 자리는 사용자가 확정했고(D-34)
  **세는 값도 안 바꾼다** — 남은 것은 **읽히는 방식**이다. **계약은 안 걸린다.**
- **OQ-606 — 접근 값의 이름이 뜻과 어긋나게 된다.** SPEC-005 §4 가 「체크리스트를 싣는 조건만」
  가르기로 하면서 **그 값은 쓰기 범위만 뜻하게 됐다** — **`read_only` 인데 항목이 실리는 조합이
  정상**이 된다. **개명·정리는 이 판의 범위 밖**이다: 그 값은 **업무 상세 표면 전체의 계약**이고
  **읽는 곳을 이 판이 세지 않았다.** **필요한 것이 체크리스트 한 자리라 그만큼만 열었다.**
  ⚠ **구현 워커가 「이왕 고치는 김에」 그 값을 셋으로 늘리지 않게 한다** — SPEC-005 §4 가 ⓐ를 기각했다.

- **OQ-607 — `external_key` 칸을 화면에 «낼» 것인가.** **표면은 그 값을 받는다**(선택 · 최대 200 ·
  중복이면 「이미 있는 프로젝트 key입니다」) — **화면이 안 내기로 한 것**이고, 그 이유는
  **데이터셋 import 의 외부 식별자라 사람이 손으로 채울 값이 아니기 때문**이다(SPEC-005 §2.10).
  ⚠ **1루프 조사가 이것을 「API 가 안 받는다」로 잘못 접었고 2루프 검수가 바로잡았다** —
  **계약(받는다)과 화면(안 낸다)은 다른 층**이다. **나중에 낼지는 사용자 한 줄 확인**이고,
  내기로 하면 **FE api 래퍼도 같이 넓어진다**(지금 넷만 보낸다).
  ⚠ **구현 워커가 「이왕 보내는 김에」 래퍼에 그 칸을 더하지 않게 한다.**

**2루프가 뒤집은 것 — 기록으로 남긴다.**

- **~~D-12~~(자동 초대의 열쇠는 배정 권한이다) → D-28.** 코디 기본값이었고
  **브라우저 1차 E2E 에서 사용자 결정으로 뒤집혔다.** DEC-004 가 **취소선과 사유로** 남겼다.
  **남는 교훈은 미결 넷을 코디가 메우지 않은 이유이기도 하다** —
  **화면이 사용자에게 무엇을 말하는가는 사용자가 답할 자리**다.
- **~~「`external_key` 는 API 가 안 받는다」~~ → 받는다 (2026-09-22 문서 검수).**
  1루프 조사(`loop2-survey-report.md` Q4)의 API 입력 표는 맞았는데 **작성자가 FE api 래퍼의
  네 칸과 바꿔 읽었다.** 세 문서가 그 위에 「화면에 칸을 만들면 보낼 곳이 없다」를 세웠고,
  **검수가 코드로 잡았다**(`project_commands.py` · `entrypoints/http.py`).
  **결정은 안 바뀌고 근거만 바뀌었다** — 남은 것은 **OQ-607**.
- **B-1 과 B-9 의 전제가 코드와 달랐다.** 코디가 적은 「프로젝트 화면은 헤더에 등록하지 않는다」와
  「우 레일 체크리스트가 항목을 받을 길이 없다」는 **둘 다 틀렸고 발주 전 조사가 바로잡았다**
  (`loop2-survey-report.md` Q3 · Q4). **발주 전에 조사를 넣은 것이 그 두 건을 막았다.**

### 1루프가 남긴 것

- **운영 대장의 지도 한 줄이 SPEC 과 갈린다 — SPEC 환류 후보.**
  SPEC-005 §5 「표면 등록」이 「**프로젝트 상세 행의 서명이 바뀐다**(응답 필드가 늘었다)」라고 적는데,
  `test_inventory_includes_each_declared_http_operation` 이 비교하는 `http_signature` 는
  **핸들러의 어노테이션 문자열**이고 `-> ProjectDetailResult` 가 **안 바뀐다.**
  실제로 드리프트가 나는 곳은 **MCP `get_project` 의 `output_schema`** 다
  (`test_inventory_schemas_match_the_actual_registered_tools`(`test_operation_inventory.py:104`)가
  스키마를 통째로 비교하고, 현재 그 안에
  `ProjectTaskView`·`preceding_task_ids` 가 실재한다).
  **계약은 안 갈린다 — 「대장을 손봐야 한다」도, 「라우트 수가 그대로다」도 참이다.
  가리키는 자리만 다르다.** **이 WP 가 SPEC 을 고치지 않는다.** 그 표를 손댈 때 자리를 맞춘다.
- **자동 초대 흔적은 「한 칸」이다 — 「두 표에 한 칸씩」에서 다시 정정됐다.**
  이 WP 의 앞 판은 흔적을 `work_requests`·`task_assignments` **두 표에 한 칸씩** 두고
  「붙는 자리가 두 원장에 걸쳐 있다」를 이유로 들었다.
  **요청 발송도 배정 행을 만든다는 사실이 드러나 한 표로 좁혔다** —
  요청을 보내면 `assignment_kind="request_effect"` · `status="pending"` ·
  `source_work_request_id` 를 든 `TaskAssignmentRecord` 가 함께 선다(`platform/work_tasks.py:1938-1957`).
  그래서 흔적은 **`task_assignments.auto_project_join` 하나**이고 **요청 유래인지는
  `source_work_request_id` 로 안다.** **D-14 의 「한 칸이 는다」와 다시 맞는다.**
  SPEC-005 는 「**무엇에 어떻게 기억하는지는 `30-work/` 몫**」이라 적었으므로 **계약은 안 갈린다.**
- **붙는 자리가 셋이 아니라 둘이다 — 같은 판에서 정정됐다.**
  직접 배정(`POST /api/tasks/assign`)은 **그 경로로 태어난 업무에 프로젝트가 없어** 붙는 자리가 아니다
  (`work_tasks.py:2413-2455` · `task_creation.py:118-126`). **D-11 은 자리 수를 세지 않았다** —
  「배정·발송할 때」까지다. 세는 것은 SPEC 의 몫이고 **SPEC-005 §4 가 근거와 함께 둘로 적었다.**
  ⚠ **같은 뿌리의 기존 부채** — 직접 배정으로 만든 하위 업무는 **상위의 프로젝트를 안 물려받아
  어느 프로젝트 화면에도 안 선다.** BASE-004 어긋남 목록에 없는 자리다. **이 판의 범위 밖 — 기록만.**
- **`material_*` 병렬 격리 — 원인이 아직 규명되지 않았다.** Phase 0(2루프)이 그 자리이고,
  「다음에 볼 자리」 셋은 **가설**이다. 1루프는 **기준선 분리로 지나가고 고치려 들지 않는다.**
- **떼는 자리 #4(배정 철회)는 표면이 오늘 없다 — 후속이 필요한 자리다.**
  SPEC §4 가 적은 `POST /api/action-items/{action_item_id}/commands/cancel_assignment` 는
  **AX `task.assign` 제안 위에만 서고**(`platform/actions.py:539` · `modules/actions/policy.py:136`),
  그 제안의 초안은 **`project_id` 를 언제나 `None` 으로 박는다**
  (`normalize_assigned_task_draft()` — `modules/work/drafts.py:33` · `modules/work/task_creation.py:118-126`).
  그래서 **프로젝트가 걸린 유일한 pending 배정**(담당 교체 제안이 세우는 행)에는
  **철회 표면이 HTTP·MCP·판단함 어디에도 없다.**
  **계약은 안 갈린다** — SPEC §4 가 그 자리를 **「표면이 오늘 없다」**로 적었고
  **메서드(`cancel()`)에는 건다.** 이 판은 **메서드 수준에서 해제가 도는 것까지** 증명하고
  **표면이 없다는 사실은 코드 자리로** 남긴다.
  **후속**: 그 배정에도 철회 명령이 서게 하는 일은 **이 판의 범위 밖**이다.
  문이 나는 날 **그 메서드 테스트가 표면 테스트로 올라온다.**
- **요약 스트립의 모수가 0일 때 「—」다 — D-04 가 정하지 않은 자리를 SPEC 이 (제안) 으로 닫았다.**
  업무가 0건이거나 전부 취소면 나눌 것이 없다. **0% 로 두면 「아무것도 안 했다」는 거짓**이 되므로
  **D-02 와 같은 결**로 「—」를 낸다(SPEC §2.3 · Data Contract).
  **새 결정이 아니라 열려 있던 자리를 (제안) 으로 적은 것**이고, **DEC-004 로 올릴지는 코디 판단**이다.
- **자동 해제 조건 ② 에 동시성 틈이 남는다.** 같은 사람에게 보낸 업무 둘이 **동시에** 거절되면
  둘 다 상대의 활성 업무를 보고 **아무도 안 뗀다.** 결과는 **「사람이 남는 것」**이고
  참여가 잘못 사라지는 것보다 안전한 쪽이다. **DB 제약으로 못 올린다** —
  「다른 활성 업무가 있나」는 두 표에 걸친 세기다. **이 한계를 감추지 않는다.**
- **어긋남 ② — `tasks_in()` 에 필터·페이징이 없다.** D-27 이 범위 밖으로 닫았다.
  ⚠ **D-16 이 여기에 전제를 건다** — 간트를 깊이 제한 없이 그리려면 그 프로젝트의 업무가
  **전부 한 응답에** 실려야 한다. **나중에 필터·페이징을 넣을 때 이 전제를 같이 보지 않으면
  간트가 다시 「선행 없음」이라고 거짓말한다.**
- **`member` → `lead` 승격 경로가 없다** (`projects.py:163-165` — 기존 활성 배정이면 `kind` 가 달라도
  영수증을 돌려준다). DEC-004 **보류**. 관리 모달이 요구하면 그때 연다.
- **프로젝트를 닫는 명령이 없다** — `PROJECT_STATES = ("active","closed")` 인데 `"closed"` 를 세우는
  API·operation 이 없다. DEC-004 **보류**. 이 화면이 요구하지 않는다.
- **`ds/GutterList` 이름 충돌** — 우리 부품(`ds/GutterList.tsx:20-58`)은 소비처 **0건**이고
  시안·CSS 의 `.scax-gutter-list` 와 **다른 것**이다. **개명은 범위 밖**(선례 DEC-003 §J).
  이 work 는 **새 이름을 쓰지 않고 기존 마크업 선례**(`InboxRail.tsx:103-114`)를 따른다.
- **낡은 주석 셋을 고치지 않는다** — `persistence.py:935-936`(「One level only for now」) ·
  `task_results.py:69`(「넷뿐이다」인데 `blocked` 가 통과한다) ·
  `tool_catalog.py:80,83`(없는 도구 `project_get` 을 가리킨다). **기록만 남긴다** —
  고치면 이 판의 diff 가 관계없는 자리로 번진다.
- **`ProjectPage.tsx:325` 의 빈 `<li>`** (어긋남 ⑤-7) — 화면이 재작성되므로 **자연히 사라진다.**
  별도 작업이 아니다.
- **내비 순서가 주석과 다르다** (어긋남 ⑤-8) — **D-26 이 명시적으로 닫았다.** 기록만.

## Related

- SPEC / Decision / Baseline: (frontmatter `links` 참조)
- 검수 리포트: `orchestration/work/strong-hajin-projects/review-spec-005-report.md`
  (1차 — **FAIL 4 · WARN 5**, 전부 반영됨)
- 조사 리포트: `orchestration/work/strong-hajin-projects/research-be-domain.md`(726줄) ·
  `research-fe-structure.md`(500줄) — **둘 다 코드 변경 0건 · 테스트 미실행**
- Phase 0 재료: `reference/2026-09-21-strong-hajin-calendar/material-parallel-isolation.md` ·
  같은 폴더 `README.md`(운영 사고 일곱) ·
  `orchestration/work/_archive/strong-hajin/strong-hajin-calendar/flaky-baseline-evidence.md`
- 시안: `reference/2026-09-10-sc-meeting/package 2/` 의 `Projects.html` + `handoff/projects/` —
  **레이아웃 정본.** 관리 모달의 어휘는 `handoff/shell/js/work-modal.jsx`
- 선행 work: `work-004-calendar-scheduling.md` — `task_span()` 과 `span_from`·`span_to` 라는 이름이
  그 판의 산물이다
