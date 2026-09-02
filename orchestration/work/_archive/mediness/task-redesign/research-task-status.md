# 사전 조사 — mediness task 상태 정의·사용처

> task-redesign 발주 스펙의 근거 문서. 코디 측 read-only 에이전트 2기 조사 결과.
> §A = spec 레포(mediness-mediness) 문서 조사 (2026-08-31 완료)
> §B = app 레포(mediness-app) 코드 조사 (진행 중 — 완료 시 append)

---

## §A. spec 문서 조사 (레포: /Users/kknaks/git/harness_works/mediness-mediness)

### 핵심 결론

mediness 에는 **이름만 같고 서로 통합되지 않은 task 계열 엔티티가 4종** 존재한다. 재설계는 "task 를 하나 고치는 일"이 아니라 **4개 축을 어떻게 정리할지 결정하는 일**이다.

| # | 엔티티 | 소유 SPEC | 부모 | 상태 값 개수 | 도메인 문서 |
|---|---|---|---|---|---|
| A | `decision_execution_task` | SPEC-113 (앵커 110) | `decision_intake`(결정 원장) | 4 | 있음 ✅ |
| B | `runtime_task` (Action Runtime Task) | SPEC-152 / 150 / 153 | `workflow_run` + 승인 실행 | 6 | **없음** ❌ |
| C | `version_wbs_task` | SPEC-125 | `product_version` | 6 | **없음** ❌ |
| D | `meeting_todo` | SPEC-030 | `meeting` | 상태 없음(`is_final` bool) | 있음 ✅ |

또한 설계 원형(canonical model)으로 **inbox 미승격 문서 1건**이 별도 상태셋을 제안하고 있다(§A-2-E).

### A-1. 문서 지도

#### 핵심 문서 — task 를 **정의**하는 곳

| 파일 | 무엇이 있나 |
|---|---|
| `products/mediness/40-architecture/domains/decision_execution_task.md` | **A축 SoT.** 컬럼표·`decision_task_status` enum 4값·자식↔원장 연동 불변식·Open Questions(OQ-1~5) |
| `products/mediness/40-architecture/domains/decision_task_log.md` | A축 진행 로그·핸드오프 append-only 자식(`kind = log \| handoff`). actor 정규화(0028→0029) |
| `products/mediness/20-spec/spec-113-execution-arc.md` | **A축 행동 계약.** §3.2 기본 독립 병렬 · §3.3 순서 메타 = `depends_on` 단일 · §3.4 핸드오프 · §3.6 자식 가드 · §API/MCP 계약 · §6 봉합선 · AC-1~17 · OQ-1~6 |
| `products/mediness/20-spec/spec-110-decision-lifecycle.md` | **A축 앵커.** §3.3 실행 그래프 속성표(⚠ stale — 불일치⑦) · §4 원장 상태 9값 |
| `products/mediness/20-spec/spec-152-incident-response-workflow.md` | **B축 SoT(사실상).** §Task Contract(L1280~1400): task type 3종(TK-1/2/3) · 상태 전이 · 수락/거부 계약 · TaskEvent 12종 · §U-6 간이 칸반 · §U-7 태스크 상세 · API·응답 계약 |
| `products/mediness/20-spec/spec-125-version-wbs-gantt.md` | **C축 SoT.** §Resource 4테이블 · §상태 Lifecycle(L540~558) · §U-12 자동 캐스케이드 · §U-12b 상태 칩 · API 표 |
| `products/mediness/20-spec/spec-150-action-runtime-workflow.md` | **B축 상위 커널.** §3 용어 · §6 조각 라이브러리 `task_round`(라운드 태스크 전부 terminal 판정) |
| `products/mediness/40-architecture/domains/meeting_item.md` | **D축.** `meeting_todo` — `is_final` 만 있고 진행 상태 없음 |

#### 부수 문서 — task 를 **참조/소비**하는 곳

- `spec-112-decision-arc.md` §3.6 — **A축 태스크 생성·최초 배정의 소유자**(113 아님 — 봉합선 = 계획 vs 실행)
- `spec-115-personal-dashboard.md` §U-3 — "업무수행" 세그먼트 = 내 태스크 리스트 + 시작/완료/막힘/해소/로그/핸드오프
- `spec-100-portfolio-dashboard.md` — A축 status 집계 진행률 + `currentOwner` 서버 파생
- `spec-119-decision-notify-slack.md` — T2 태스크 배정 DM, T5 완료 게이트 발화 1회(개별 Done 무음)
- `spec-123-action-ledger.md` — 회의 발 `issue_raise` 승인 → A축 실행 태스크 생성 핸드오프
- `spec-153-action-runtime-admin-workflow-console.md` — B축 콘솔, `task_status` 필터 6값(L497)
- `spec-130-weekly-report.md` — **C축 소비.** 주간보고 매트릭스가 `version_wbs_task` 읽음
- `spec-052` §L121 — C축 부모(`product_version`) + phase seed 트리거 / `spec-101` — 간트 출처 DB 전환
- `spec-030-meeting.md` — D축 Todo 추출·박제
- `spec-020-chat.md`·`spec-021-agent-daemon.md` — ⚠ **동음이의**: `chat.task`/`task_id` 는 WS 페이로드 식별자, 업무 task 무관
- `40-architecture/erd.md` — A축만 존재(⚠ stale — 불일치⑥) / `40-architecture/README.md` L44-45 — A축 2개만 등재
- `inbox/2026-07-07-action-runtime-model/Action Runtime Canonical Model.md` — **미승격 설계 원형**(§A-2-E)
- `context/decision-process.md` L23-24 · `context/org.md` L89·L100 — 조직 원칙("지시 ≠ 완료된 TODO … 사람 확인 후 task 발행")

#### WP 문서

- `30-work/work-074-incident-workflow-console.md` — B축 전체 (task 언급 최다)
- `30-work/work-069-version-wbs-gantt.md` — C축
- `30-work/work-076~078` — B축 리팩토링(`runtime_task_repo` 신설·`task_round` 조각 추출)
- `90-archive/v0.0.1/30-work/work-037`(A축 migration 0028)·`work-039`(actor 정규화 0029)

### A-2. task 상태 정의

#### A-2-A. `decision_execution_task` — 4값 (PascalCase)

출처: `domains/decision_execution_task.md` §Enum (L55~60)

```
decision_task_status: Todo | InProgress | Blocked | Done      (Cancelled 미도입 — OQ-4 후속)
```

- **태스크 자체의 합법 전이 매트릭스는 어느 문서에도 없다** — `spec-113` L185 서술문(`Todo→InProgress→Done/Blocked`)뿐
- 초기 status 조건부 안착(spec-113 §3.3): 담당자 있고 선행 없음 → `InProgress` 자동 착수 / 아니면 `Todo`
- 선행 게이팅 OFF(MVP) — `depends_on` 이 있어도 후행 시작 비차단
- 자식 → 원장 가드: 첫 태스크 생성 → 원장 `Executing` 자동 / `is_required` 전부 `Done` → `Feedback` 자동 / `Blocked` 는 사람 신호
- 삭제: `Todo` 만 soft delete, 그 외 409
- `Blocked` 는 `blocker_reason`/`blocker_owner_id`/`blocker_condition`/`blocker_due_date` 4컬럼 동반

#### A-2-B. `runtime_task` — 6값 (snake_case, PG enum `runtime_task_status`)

출처: `spec-152` L1297·L1513~1525 / `spec-153` L497

```
accept_pending | todo | in_progress | blocked | done | canceled
```

```
accept_pending →(수락)→ todo →(시작)→ in_progress → done
accept_pending →(거부+사유)→ accept_pending 유지 → (재배정 시 스탬프 클리어)
todo/in_progress ⇄ blocked · todo/in_progress/blocked → canceled
```

- 예외: `incident.response_tracking`(round 0)은 수락 게이트 없이 생성 즉시 `in_progress`
- 스탬프 5종(created/accepted/started/completed/canceled_at) · `declined` 는 저장 컬럼 아닌 이벤트 파생
- TaskEvent 12종 append-only (L1419~1432) — `comment` 를 시스템 전이와 같은 타임라인에 혼합(별도 로그 테이블 없음이 명시적 선택)

#### A-2-C. `version_wbs_task` — 6값 (snake_case)

출처: `spec-125` §Resource L399 / §Lifecycle L540~558

```
todo | in_progress | blocked | issue | done | canceled
```

- **`issue`**: 이 축 고유값. `issue_note` 필수, `[이슈]` intake 경로로만 진입, 상태 칩 선택지 제외(§U-12b)
- 일정 기반 자동 전환: `todo` + 시작일 도래 → `in_progress`(§U-12)
- 캐스케이드/rollup: check_item → work_item → phase 자동 전파 · `done`/`canceled`/`issue` 는 보호 상태
- 2계층 고정: `phase`/`work_item`(`task_kind`), check_item 은 depth 미포함

#### A-2-D. `meeting_todo` — 상태 없음

`text` + `is_final`(bool)뿐. `assignee_id` 는 "향후 컬럼 추가 자유"(DEC-019).

#### A-2-E. Canonical Model 원형(inbox 미승격) — 5값

`inbox/2026-07-07-action-runtime-model/Action Runtime Canonical Model.md` L180~189:
`todo | in_progress | blocked | done | canceled` + `assignee_type: user|team|agent|system` + `execution_mode: human|agent|tool|mixed` + task_event 13종 + Action Inbox/Task Inbox 표면 분리. L206: "기존 `decision_execution_task` 가 이 역할을 맡을 수 있다" — **통합 의도는 있었으나 어느 SPEC 에도 미반영.**

### A-3. 불일치 목록 (재설계 쟁점)

1. **상태 어휘 3벌** — 표기(PascalCase vs snake_case)·값·개수 전부 다름. `blocked` 표현도 3벌(A: 4컬럼 / B: 값만 / C: 값+`issue_note`)
2. **취소 3중 분기** — A: 상태 없음(Todo 한정 soft delete) / B: `canceled` terminal(사유 조건 모호) / C: 어디서든 `canceled`
3. **착수 철학 상충** — A: 배정 시 자동 착수 / B: 명시 수락 게이트(`accept_pending`) / C: 일정 기반 자동 전환
4. **진행 로그 저장소 2벌+** — A: `decision_task_log` / B: TaskEvent 혼합 타임라인 / C: `version_wbs_task_log`
5. **핸드오프/재배정 계약 3벌** — A: PATCH assignee(status 유지) / B: 전용 reassign(accept_pending 리셋) / C: 로그 기록만
6. **ERD stale (심각)** — `erd.md`(2026-06-20)는 A축을 "미구현"으로 기술하나 실제 migration 0028 로 구현됨. `actor` text 잔존(0029 정규화 미반영). B·C축 테이블은 ERD·도메인 인벤토리에 전무
7. **SPEC-110 앵커 stale** — §3.3·AC-9 에 폐기된 `exec_type`(순차/병렬/독립)·선행 대기 서술 잔존. spec-113/도메인 문서는 삭제 확정
8. **`is_required` 상충** — A축: 완료 자동 게이트 핵심 / B축: 폐기(work-074 C16)
9. **표면 파편화** — "내 할 일"이 3개 화면(SPEC-115 §U-3 / SPEC-152 §U-6 / SPEC-125)에 흩어짐. 통합 인박스는 미승격 inbox 문서에만 존재

### A-4. API / 화면 목록

**A축 API** (spec-113 §API, spec-115, spec-112 §3.6): `POST/PATCH/DELETE /decisions/{id}/execution-tasks[/{tid}]` · logs append/edit · `POST /decisions/{id}/transition` · `GET /api/v1/decisions/me/tasks` · MCP 3종(`decision_task_update`/`decision_transition`/`decision_task_log`)

**B축 API** (spec-152 L314~331): `GET /{run_id}/tasks[/{task_id}]` · `PATCH`(전이+comment) · `POST .../decline`·`.../reassign`·`.../comment` · `GET /api/v1/action-runtime/tasks`(칸반 횡단). 응답 계약 `TaskOut`/`TaskDetailOut`/`MyTaskOut`

**C축 API** (spec-125 L452~458): `POST/PATCH/DELETE /api/v1/versions/{vid}/wbs/tasks[/{tid}]` · reorder · intake · check-items

**화면**: 개인 스페이스 업무수행(115 §U-3, 확정) · 태스크 간이 칸반(152 §U-6, 착지) · **태스크 상세 2컬럼(152 §U-7, 설계 확정·미착수 ⚠)** · WBS/간트(125, stable) · 관리자 콘솔(153, stable) · HTML 시안 4종(`21-html/`)

### A-5. 설계 변경 이력 요약

- **A축**: 2026-06-20 T-016 대개편(`exec_type` 삭제·독립 병렬 기본·`Waiting`→`Todo` 4상태 확정·`is_required` 도입) → T-019 WP-037 발주(migration 0028) → 06-24 자동 착수 확정. 도메인 문서는 v0.0.1 컷 이후 무변경
- **B축**: spec-152 개정 노트 6건 — 07-15 모델 개편, 07-20 §U-7 신설·`comment` 이벤트, T-063 **되돌림**(회고 직접 발행 폐기, `/review/revise·publish` deprecated 죽은 경로), T-079 revise 폐지, 07-27 코드 대조 정합, C16 `is_required` 폐기
- **C축**: v0.0.3(SPEC-113/123 핸드오프 Phase 2 defer = OQ-6 RESOLVED-defer) · v0.0.5(`link_kind` enum 재사용 — 마이그레이션 회피) · v0.0.7(상태 칩)
- **미승격**: `inbox/2026-07-07-action-runtime-model/` 4건. `spec-151` L283 "Task/칸반 1단계 제외"

### A-6. 재설계 시 주의 (문서 관점)

1. A축 SoT 는 SPEC 이 아니라 **도메인 문서** — 상태 변경은 `decision_execution_task.md` 를 고치고 SPEC-113 은 링크 유지
2. B·C축은 SoT 가 SPEC 본문에 갇혀 있음 — 통합 설계 전에 **도메인 문서 2건 신설**이 선행돼야 층위가 맞는다
3. **ERD 를 신뢰하지 마라** — 3개월 전 상태. 코드/migration 이 SoT
4. A↔C 통합은 이미 **명시적으로 defer** 됨(spec-125 OQ-6, spec-113 §6) — 통합 방향이면 이 결정을 뒤집는 문서가 필요
5. 상태 값 통일보다 **착수 시점 철학(자동/수락/일정) 통일이 먼저** — 어느 쪽이든 나머지 축의 AC·화면·알림(119 T2)이 흔들림
6. A축 태스크 전이 매트릭스가 문서에 없다 — 재설계 시 새로 그리고 코드와 대조 필요
7. 동음이의어 분리: `chat.task`(WS 페이로드)·"별건 태스크"(후속 작업 항목)·background task(인프라)
8. spec-110 앵커 정정이 선행 과제 — 폐기 모델을 인용할 위험
9. B축 미착수 부채: spec-152 §U-7 태스크 상세 — 재설계가 흡수할지 결정 필요
10. A축 OQ 4건(OQ-1 department FK · OQ-2 의존성 다대다+게이팅 · OQ-4 Cancelled · OQ-5 is_required 주체)이 재설계 입력. OQ-4↔불일치②, OQ-5↔불일치⑧이 짝

---

## §B. app 코드 조사 (레포: /Users/kknaks/git/harness_works/mediness-app) — 2026-08-31 완료

### 핵심 결론

코드에서 "task"는 **세 개의 서로 다른 원장**이다. **`RuntimeTask`(테이블 `tasks`)가 이미 canonical 정본**이고, WBS 는 `origin_task_id` 로 상태 소유권을 넘긴 미러, `DecisionExecutionTask` 는 레거시 병행 원장이다.

### B-1. 상태 정의 정본

#### ① `RuntimeTask` — canonical (테이블 `tasks`)

`back/app/models/action_runtime.py:63-71` — `RuntimeTaskStatus` (PG enum `runtime_task_status`):
`accept_pending | todo | in_progress | blocked | done | canceled`

- 모델 `action_runtime.py:373-480`. `status` NOT NULL, server_default 없음(항상 앱 지정)
- 스탬프: `accepted_at`/`started_at`/`completed_at`/`canceled_at` (:455-458) · soft delete `deleted_at`(:466)은 취소와 **직교**
- 자식: `TaskCheckItem`(CASCADE) · `TaskCc`(RESTRICT) · `TaskEvent`(RESTRICT)

#### ② `VersionWbsTask` — WBS 미러 (테이블 `version_wbs_task`)

`back/app/models/version_wbs.py:55-75` — `VersionWbsTaskStatus`: **①과 문자열까지 동일한 6값** ("6 = 6이 계약" docstring, 변환 함수 없음, 사람이 동기화 유지). `origin_task_id → tasks.id` RESTRICT(:160-162) — **work_item 상태 정본은 RuntimeTask 쪽**. 구 `issue` 값은 **migration 0108 에서 폐지**.

#### ③ `DecisionExecutionTask` — 레거시 (테이블 `decision_execution_task`)

`back/app/models/decision.py:272-282` — `DecisionTaskStatus`: `Todo | InProgress | Blocked | Done` (PascalCase 4값). 상태머신 없음 — `decision_execution.py:225-232` 직접 대입. `Blocked ⟹ blocker_reason` 앱 검증(:351-355). soft delete.

#### 마이그레이션 이력(주요)

- `0028` decision_task_status 생성(4값) · `0042` version_wbs_task_status 생성 · `0045` runtime_task_status 생성(**6값이 처음부터**)
- `0108_wbs_status_vocab_task_axis` — **어휘 cutover**: `issue` 제거 + `accept_pending` 추가 + `issue_note` drop + `origin_task_id` 추가 (PG enum 값 제거 불가 → rename→새 타입→USING 캐스트→drop 4단 + 사전 RAISE 가드)
- `0110_task_canonical_wbs_backfill` — 기존 WBS work_item → `tasks` 소급 생성(무변환 캐스트)
- `0107`(제품·버전 축 + CHECK 2개) · `0112`(done 체크리스트 교정, BUG-021) · `0087`(tasks soft delete)

### B-2. 상태 전이 지도

**정본 전이표** — `back/app/services/action_runtime/tasks/machine.py:41-54`:

```
accept_pending → {todo, canceled}
todo           → {in_progress, blocked, canceled}
in_progress    → {done, blocked, canceled}
blocked        → {todo, in_progress, canceled}
done / canceled → terminal
```
- `decline` 은 상태 무변경(`task_declined` 이벤트만, :119-132) · `reassign(reset_gate=True)` → `accept_pending` 리셋 + 스탬프 클리어(:134-174, terminal 가드 = BUG-023)

**단일 집행 seam** — `tasks/lifecycle.py`: `apply_user_transition`(:120, 사람 전이의 유일한 문 — 낙관적 잠금 + TaskMachine + done 시 체크리스트 강제완료) / `apply_derived_transition`(:201, 체크리스트 파생 — **TaskMachine 우회**, done→in_progress 재개방 허용) / `guard_stale_write`(:61, `expected_updated_at` 409)

**전이 호출부 23곳** (요약 — 전체 표는 코드 조사 원문):
- manual 표면: transition/decline/reassign/생성 (`manual_surface.py`, 라우터 `action_runtime_v2.py:509~546, 399`)
- run 하위(incident/decision): `workflow/tasks_surface.py:349-411, 457, 669-730`
- WBS 상태 칩 → canonical 위임: `version_wbs.py:1386-1440`(**합성 전이 `todo→in_progress→done`** 포함) · cancel `:1490-1503`
- 체크리스트 파생/rollup: `version_wbs.py:756-829` + `version_wbs_status.py:124-160`(phase 는 직접, work_item 은 fail-closed)
- **스케줄러**: `version_wbs_scheduler.py:92-134` — 일 1회 `todo→in_progress` 자동전환 + overdue Slack DM (`apply_derived_transition`, cause="wbs_schedule")
- 채팅/MCP 즉시형: `task_draft/surface.py` — ⚡시작(:559-576, `accept_pending→todo→in_progress` 합성)·⚡완료(:578-608)·⚡거절(:628-682)·재배정(:1020-1055)
- 시스템 대리 완료: `decision/task_service.py:92-110` `complete_as_system` · bootstrap 생성 즉시 `in_progress`(:155) · incident 예방/후속 `accept_pending` 생성 vs 추적 카드 `in_progress` 생성(`incident/definitions.py:105,141,310`) · run 종결 시 done(`runs_surface.py:162`)

FE 전이 계약: `projection.py:292-299` `allowed_transitions`(전이표 ∩ Policy)가 **FE가 소비하는 유일한 축**.

### B-3. 사용처 지도

**back 라우터**: `action_runtime_v2.py` — canonical CRUD·transition·decline·reassign·check-items(:368~585) + incident/decision 하위(:595~675, :2181~2500) + 채팅/MCP 즉시형 9종(:1296~1575). 레거시: `decisions.py:139` `GET /me/tasks`. WBS: `wbs.py`.

**mcp**: `task_start`/`task_done`/`task_check`/`task_wbs_request`(`task_lifecycle.py`) · `task_decline`·`task_reassign_request`·draft 계열 · `runtime_task_my`(status 필터) · `wbs_task_update`(`wbs_common.py:42-43` **STATUSES 6값 하드코딩**) · `wbs_task_create` 는 status 를 받지 않음(back 소유)

**front**: 상태 어휘·라벨 3벌 — `lib/tasks/canonical-task.ts:20-41`(타입+terminal) · `lib/incident.ts:143-153`(라벨) · `lib/wbs.ts:35-42,227-265`(별도 라벨) · `lib/decisions.ts:342-352`(레거시 4값+`wait`). 칸반 `ax/tasks/task-kanban.tsx`(5열, canceled 미노출) · 상세 `components/tasks/detail/*`(`TaskHeaderActions.tsx:29-43` TRANSITION_LABEL 하드코딩 6쌍, 서버 allowed_transitions 만 소비) · WBS 모달 · BFF 라우트 다수.

### B-4. 연결 도메인

- FK in → `tasks.id`: `task_check_items`(CASCADE) · `task_ccs`(RESTRICT) · `task_events`(RESTRICT) · `version_wbs_task.origin_task_id`(RESTRICT)
- FK out: organization · org_unit×2 · organization_member · `action_executions`(워크플로 계열 필수) · `product_version`. FK 없는 축: `assignee_id`/`assignee_member_id`/`product_slug`/`scope_slug`
- **회의록 v2**: `MeetingV2MinutesTask`(기존 task 갱신 항목, status 는 "회의 시점 박제") · `MeetingV2MinutesTaskIssuance`(신규 발행 후보) — **둘 다 FK 없음**
- 채팅: `landing_chat_turns.task_id` 는 chat job id — **이 task 아님**(동음이의). 실제 연결은 `task_draft/*` Action 카드 매개
- 알림: `version_wbs_scheduler.py:41` 이 `decision_notify._send_dm` 재사용(overdue DM)
- 레거시: `DecisionExecutionTask → decision_intake`(RESTRICT) · self-ref `depends_on_task_id`(SET NULL)

### B-5. 냄새 목록

1. **S1 (심각)** — 상태 enum 3벌, 그중 `RuntimeTaskStatus`↔`VersionWbsTaskStatus` 는 값이 동일한데 별개 PG enum. 서로 캐스팅 왕복(`version_wbs_status.py:85`, `lifecycle.py:220`), 동기화는 사람이 지킴. 값 추가 시 두 enum 동시 migration 필요
2. **S2 (심각)** — `DecisionTaskStatus` 는 완전히 다른 세계: 4값 PascalCase, 상태머신 없음(직접 대입), FE 별도 라벨맵. **같은 제품에 태스크 상태 규칙이 두 벌**
3. **S3** — 상태 어휘 하드코딩 4곳(mcp `wbs_common.py:42` · front `canonical-task.ts` · `wbs.ts` · `incident.ts`)
4. **S4** — 같은 값의 한글 라벨이 표면마다 다름: `todo`=대기/예정/할 일, `blocked`=중단/차단/막힘 (incident.ts / wbs.ts / back `task_draft/const.py:231`)
5. **S5** — terminal 집합 복제 1건(`task_draft/composition.py:320` — 나머지 8곳은 `machine.TERMINAL_STATUSES` import)
6. **S6** — 죽은/도달 불가 값: WBS 표면에서 `accept_pending` 지정 불가(400) · phase 는 rollup 상 `accept_pending`/`blocked` 도달 불가 · `RuntimeTaskStatus` docstring "1단계 미사용" 낡음 · **`meeting_v2_minutes_task.status` 기본값 `"open"` = 네 번째 상태 어휘**(`_ACTION_STATUSES = open/in_progress/done`)
7. **S7** — TaskMachine 우회 경로 2개(`apply_derived_transition` — 자격 검사 없음 / `write_status` phase 전용)
8. **S8** — 합성 전이 3곳 각자 구현(공유 헬퍼 없음): `_transition_steps` · `_advance_to_in_progress` · `apply_complete`
9. **S9** — `decline` 자체는 상태 검사 없음인데 표면 3곳이 `accept_pending` 조건을 제각각 재구현(run 하위는 조건 없음)
10. **S10** — 상태·삭제·취소 3축 직교, `delete_task` 한 함수에 4가지 정책

### B-6. 재설계 시 주의 (코드 관점)

1. **RuntimeTask 가 이미 정본** — 재설계는 `version_wbs_task.status` 를 제거하는 방향이 자연스럽다. 단 phase(구조 행)는 자체 status 유지 — **phase 와 work_item 이 같은 테이블·enum 을 쓰는 게 이중 소유의 뿌리**
2. PG enum 변경 비용 큼 — 0108 의 4단 캐스트 + RAISE 가드 선례를 따를 것. runtime/wbs enum 은 **동시에** 변경
3. `accept_pending` 을 건드리면 최소 6곳 연쇄(재배정 리셋·생성 초기값 4곳·decline 조건·cascade lane·집계·스케줄러·칸반 5열)
4. `allowed_transitions` 가 FE 유일 계약 — 전이표 변경은 FE 자동 추종하나 `TRANSITION_LABEL` 하드코딩 6쌍은 새 edge 시 상태명 폴백
5. 파생 전이엔 자격 검사가 없다 — 체크리스트 토글 = 사실상 상태 변경 권한
6. 삭제⟂취소 계약 유지 — 조회 배제 앵커(`_scoped()`·`wbs_origin_task_not_deleted()`)가 무효화되는 설계 금지
7. `task_type` 은 allowlist 판정축(`tasks/const.py:58-96`) — 새 종류는 조용히 모수에서 빠짐. kind 축 변경 시 4곳 동반 수정
8. **DecisionExecutionTask 는 별도 마이그레이션 계획 필요** — canonical 에 `decision.execution` task_type 으로 일부 병존, `/decisions/me/tasks` 와 `/action-runtime/tasks` 가 같은 사용자에게 **다른 목록**을 줌
9. 트랜잭션 규약: lifecycle 은 commit-free, 커밋은 라우터/채팅 턴 소유 — 새 seam 도 동일
10. 낙관적 잠금 기준 = `tasks.updated_at`, 합성 전이는 첫 걸음만 검사
11. 테스트 70+ 파일 — 정본: `test_task_machine.py` · `test_wp104_w10_bug020_task_lifecycle.py` · `test_wp104_w3_status_axis.py` · `test_0094_wbs_status_vocab.py` · `test_version_wbs_scheduler.py` · bug023 · mcp/front 테스트

---

## §C. 문서 ↔ 코드 대조 (코디 종합)

| # | 항목 | 문서(§A) | 코드(§B) | 판정 |
|---|---|---|---|---|
| 1 | C축(WBS) 상태 어휘 | `spec-125` §Lifecycle: `issue` 포함 6값, `accept_pending` 없음 | **0108 cutover**: `issue` 폐지·`accept_pending` 도입, runtime 과 동일 6값 | **spec-125 stale** — 코드가 앞서감. wp104 계열 작업이 spec 에 미반영된 것으로 보임 |
| 2 | A↔C 통합 | "통합하지 않는다"(spec-113 §6)·OQ-6 defer | `origin_task_id` 로 **WBS→canonical 상태 위임 이미 구현**(0108/0110) | defer 결정이 코드에서 사실상 뒤집힘 — **문서 정정 필요** |
| 3 | B축 도메인 문서 | 없음(SPEC 본문에만) | `RuntimeTask` 가 canonical 정본 | 정본 엔티티에 도메인 SoT 문서가 없다 — 신설 1순위 |
| 4 | A축(decision) | 도메인 문서 SoT 有, OQ-4(`Cancelled`) 등 열림 | 레거시 병행 원장, 상태머신 없음, canonical 에 일부 이관 | **마이그레이션/폐기 로드맵이 양쪽 다 없음** |
| 5 | 착수 철학 | 3벌 상충(자동/수락/일정) | 코드도 3벌 그대로: bootstrap 즉시 in_progress · accept 게이트 · 스케줄러 자동전환 | 재설계 1번 쟁점 |
| 6 | 전이 매트릭스 | A축은 문서에 없음 | canonical 은 `machine.py` 가 정본(테스트 포함) | canonical 전이표를 도메인 문서로 승격하면 됨 |
| 7 | ERD | 2026-06-20 stale(A축 "미구현", B·C 부재) | 0028~0114 구현 완료 | **ERD 전면 재작성 대상** |
| 8 | 라벨 | 문서에 라벨 SoT 없음 | 한글 라벨 3~4벌 상이(S4·S6) | 라벨 SoT 를 재설계 산출물에 포함할 것 |

### 재설계 후보 쟁점 (사용자와 확정할 것)

1. **원장 통합 범위** — RuntimeTask 로의 단일화가 이미 반쯤 진행됨. `DecisionExecutionTask` 완전 이관·폐기까지 갈 것인가, WBS `status` 컬럼 제거까지 갈 것인가
2. **착수 시점 철학 단일화** — 자동 착수 / 수락 게이트 / 일정 기반 중 무엇을 정본으로
3. **상태 어휘 확정** — `accept_pending` 유지 여부, `Cancelled`(A축 OQ-4) 정리, meeting `open` 어휘 흡수
4. **문서 층위 복구** — `runtime_task` 도메인 문서 신설 + ERD 재작성 + spec-110/125 stale 정정이 스펙 단계 선행 과제

