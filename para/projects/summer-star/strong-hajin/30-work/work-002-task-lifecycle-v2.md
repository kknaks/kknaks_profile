---
type: work
id: WORK-002
title: "W2 — 업무 구조·생명주기 v2 와 확정 시안 화면 통합"
status: review
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
created_at: 2026-09-17
updated_at: 2026-09-17
tags:
  - product/strong-hajin
  - doc/work
  - status/in_progress
links:
  baselines:
    - "[[baseline-002-task-lifecycle-v2|BASE-002]]"
  decisions:
    - "[[decision-002-task-lifecycle-v2|DEC-002]]"
  specs:
    - "[[spec-003-task-lifecycle-v2|SPEC-003]]"
    - "[[spec-001-work-management|SPEC-001]]"
    - "[[spec-002-action-item-review|SPEC-002]]"
  works:
    - "[[work-001-task-creation|WORK-001]]"
  releases: []
  related: []
---

# W2 — 업무 구조·생명주기 v2 와 확정 시안 화면 통합

요청을 **보내고 수락해야 담당이 서는 축**을 되돌리고, 업무를 **재귀 하위**로 나누며,
담당 변경에 **책임 공백이 없게** 하고, 완료를 **사람이 내는 끝**으로 만든다.
그 흐름이 **확정 시안의 화면**(세 탭·표 세 벌·칩·모달·두 레일)에서 실제로 불려지게 한다.

**만들지 않는 것**: 업무 분배(배정)의 수락 정책 · 체크리스트 강제 · 막힘/공동 담당/복수 부모/상위 취소
전파 · 메일·메신저 통합과 시안 내비의 새 페이지(수신함·진행 현황·자료) · 별표 · 근무 시간 ·
**캘린더의 회의 일정** · 수신함 카드의 아바타·미읽음. **승인이 없거나 계약이 없다.**
그 자리들은 **빠뜨린 것이 아니라 후속 계약으로 남긴 것**이고, 이 work 를 「확정 시안 전체 완료」로
읽지 않는다.

> 1 파일 = 1 work = **빌드 계획**. SPEC 의 외부 계약 본문은 복제하지 않고 절 이름으로 가리킨다.
> **2026-09-17 구현 착수.** WORK 재검수의 차단 결함 0건 확인 후 BE Phase 1~6 · FE Phase 7을 발주했다.
> 변경 전 자동검증 4종은 통과했다. 실행 DB가 비어 있어 실데이터 점검은 배포 전까지 미충족으로 남는다.
> 브라우저 E2E는 사용자 담당이며, 구현·자동검증 완료와 구분한다.

## Meta

- Baseline: BASE-002 (원문 V-*·L-*·P-*·E-*·EU-* 와 현재 관측 O-1~O-34 · 미확인 **BASE U-1~U-7**)
- Covers spec: **SPEC-003 전절** — §2 UX 계약 · §3 S-1~S-16 · §4 API/Request-Response/Validation/
  Case Matrix/State/Data · §5 Implementation Rules · §6 인수조건과 A1~C2·10단계 추적.
  **SPEC-001·SPEC-002** 는 대체되지 않은 절이 **회귀 기준**이다(멱등 키 · 활성 담당 유일성 ·
  권한 재검사 · actor 기록 · 관리자 배정의 조직 범위 검사 ·
  진행 기록 append-only · 기한 두 값 · 완료 승인 회차 · 종류 칩 · AX 사람 확인 · 표면 일치)
- Depends on work: **WORK-001(W1)** — 기준선이다. **재구현하지 않는다.** W1 이 세운 일곱 보장을
  이 work 가 그대로 이어받는다(§ W1 유지 회귀)
- Parallel work: 없음. 이 work 안에서 BE/FE 가 병행한다(§ 병행 가능 지점)
- Follow-up work: 배정 정책(M-1~M-3) · 체크리스트 강제(M-4) · 중간 검토(M-5) ·
  막힘/공동 담당/복수 부모/상위 취소 전파(M-6) · 자동 수락 트리거(M-7) ·
  시안 내비의 새 화면 3종 · 별표(M-21) · 수신함 카드 메타(M-22) ·
  **근무 시간·캘린더의 회의 일정(M-23)** ·
  `blocked`·`completion_submitted` enum 정리
- External dependency: **없다.** 외부 API·credential 을 새로 붙이지 않는다.
  격리 PostgreSQL(`POSTGRES_TEST_URL`)과 로컬 demo DB 만 쓴다

### 착수를 막는 것과 막지 않는 것

| 무엇 | 착수를 막나 | 어디에 걸리나 |
|---|---|---|
| **OQ-203** — 완료 보고 제출도 하위로 막을 것인가 | **아니다** | Phase 5 의 작업 한 줄과 §6 인수조건 한 줄. **답 대기 중이다** — 제출을 여는 것은 **현행 보존**이고(SPEC-003 §4·§6·§7 의 기본값과 같다) **새 선택의 확정이 아니다. 답 전에는 정책 확정으로 표시하지 않는다.** 답이 「막는다」면 `completion-report` 에 검사 한 줄 + 인수조건 한 줄 (조건별 검증 계획은 Phase 5) |
| **OQ-206** — 승격 요청(요청자=`system:meeting`)의 완료 확인자 | **아니다** | Phase 5 의 **승격 경로 완료 승인 한 조각만.** 답 전까지 **구현 대상이 아니다**(SPEC-003 §4·§7). 일반 요청 축 A1~C2 는 전부 선다. 승격 요청의 **수정·재상신·철회**는 미정이 아니다(O-31, 기존 동작 보존) |
| **BASE U-6** — 실행 DB 예외 행 | **아니다** | Phase 0 의 읽기 전용 SELECT. **0건이 아니면 그때 사용자에게 올린다** |
| M-1~M-7 · M-11~M-24 | **아니다** | 현행 동작을 회귀로 지키거나 화면 조각만 비운다 |

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | review |
| Progress | 자동검증 완료 |
| Branch/PR | `kknaksss/strong-hajin-work` (워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`, HEAD `8973791` + W1 미커밋) |
| Blocker | 없음 — 위 표 |
| Next | 사용자 브라우저 E2E · OQ-203/OQ-206 답변 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위·미정 처분·사용자 질문 승격 | done |
| Design | kknaks | 확정 시안 해석과 미설계 자리의 배치 결정 | done |
| FE | `@sc-ax-fe` | Phase 7 전부 + Phase 2~6 의 FE 소비 절반 | done |
| BE | `@sc-ax-be` | Phase 0~6 + Phase 8 의 API·DB 회귀 | done |
| QA | 코디네이터(자동) / 사용자(브라우저) | 자동 검증은 에이전트, 브라우저 E2E 는 사용자 | done (브라우저는 사용자 대기) |
| Ops | kknaks | migration 순서·rollback·배포 | review |

## Scope

포함:

- 요청 발송 · 수락 · 거절 · 협의 · 철회 · 재요청 과 **상위 Task 연결**
- **재귀 하위 저장**(깊이 제한 제거) · 직속 하위 조회 · 중심 업무 판정 · 순환 차단
- 담당 변경의 **제안–수락–거절**과 책임 공백 제거
- 완료 보고 · 보완 · 승인 · **취소 제외 미완결 하위의 최종 완료·승인 차단** · 자동 완료 없음
- 수락 후 **합의 취소** · 수락 후 **조건 변경 동의** · **재개**(완료된 상위 선재개 포함)
- **요청 관계 읽기 권한**과 그 권한이 닿는 표면 전수(상세·하위 트리·자료 목록·본문·다운로드·검색·미리보기)
- 무응답·기한 초과의 **자동 전이 없음**
- 새 명령 전부의 멱등성·회차·권한 재검사
- **REST · MCP · AX · 회의 승격 · seed/시나리오 · operation inventory** 의 표면 일치
- **확정 시안 기준 FE** — 세 탭 · 표 세 벌 · 필터 칩 · 업무 만들기 모달 · 좌/우 레일 ·
  그리고 **v2 흐름이 설 자리**(상세·직속 하위·수락/거절·승인/보완·담당 변경·취소 제안/동의·재개)
- 기존 데이터 호환: **읽기 전용 점검 → additive migration → rollout → rollback**

제외:

- **배정 정책** — ① 신규 관리자 배정(즉시 `active`, O-28) ② 담당 없는 업무의 첫 지정(`pending`, O-14)은
  **현행 유지 회귀**다. ③ **담당 교체만** v2 를 적용한다(DEC-002 § 범위 기록)
- 체크리스트 전체 체크 강제·결과 필수 입력(M-4) · 중간 검토(M-5) ·
  막힘·공동 담당·복수 부모·상위 취소 전파(M-6) · 자동 수락(M-7)
- `blocked` · `completion_submitted` **enum 자체의 정리** — 이 work 는 두 값을 **없애지 않는다.**
  `completion_submitted` 는 **내부에 유지하고 외부 투영에서만 `done` + `awaiting_review` 로 매핑**한다
  (Phase 5). enum 을 지우는 것은 후속이다
- 시안 내비의 새 페이지 3종 · 메일/메신저 통합 · 별표 · 근무 시간 · **캘린더의 회의 일정** ·
  수신함 카드 아바타·미읽음
- **브라우저 E2E** — 사용자 담당. 에이전트는 자동 검증까지(§ 검증 책임의 경계)
- `.design-sync/` 재싱크와 DS 부품 신설의 **디자인 작업 자체** — 이 work 는 **있는 DS 로 조립**하고
  모자란 글리프 9종만 더한다(§ Phase 7)

## Code Surface

- Repo / module: `toy_pr2/Strong_hajin` (SCAX modular monolith).
  워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`, 브랜치 `kknaksss/strong-hajin-work`.
  **HEAD `8973791` 위에 W1 미커밋 변경이 살아 있다** — 기준선은 HEAD 가 아니라
  `orchestration/work/strong-hajin-work/v2-code-baseline/`(manifest·working-files.zip·tracked.patch)이다.
  **HEAD 만으로 v2 diff 를 판정하지 않는다.**
- 규약: `AGENTS.md` — 백엔드 테스트는 **Makefile 타겟으로만**(`uv run pytest` 직접 호출 금지) ·
  프론트는 `make frontend-test` · MCP/HTTP 시그니처를 바꾸면
  `tests/architecture/test_operation_inventory.py` 가 `docs/unified-operations-inventory.json` 과의
  drift 를 잡는다(**전체 재작성 금지, diff 난 항목만 패치**).

### 이번에 만질 파일 — 직접 찾은 전수

경로는 `backend/src/ax_workspace/` 기준. **소유자를 한 칸에 하나만** 적는다 —
공유 파일을 둘이 만지면 통합 단위에서 충돌한다.

| 경로 후보 | 역할 | 소유 | Phase |
|---|---|---|---|
| `modules/work/requests.py` | 요청 발송·수락·거절·협의·철회·수정. `create()` 가 요청+Task+활성 담당을 한 transaction 에 세운다(O-1) | BE | 2 |
| `modules/work/request_lifecycle.py` | 순수 층 — 요청 생성 판정·수정·철회. `SYSTEM_MEETING_REQUESTER` 와 `promoted_by_member_id` 대행이 여기 있다(O-30·O-31) | BE | 2·6 |
| `modules/work/request_commands.py` · `request_results.py` · `request_errors.py` | 요청 입력 모델·결과 투영·오류 | BE | 2 |
| `modules/work/creation.py` | `decide_task_creation()` — `self`/`horizontal`/`managed` 세 갈래(O-26)와 멱등 키 필수(`require_idempotency_key`) | BE | 2 |
| `modules/work/creation_commands.py` | `POST /api/tasks` 의 두 갈래 실행부. `_refuse_unsupported_horizontal_fields` 가 `start_date`·`parent_task_id`·`project_id` 를 거절한다(O-27, `:157-173`) | BE | 2 |
| `modules/work/application.py` | 중심 축. `parent_for()` 한 단계 제한(O-6, `:212-230`) · `_hierarchy_view`/`_related_view` 의 `children` 비움(O-8, `:390`·`:467`) · `_may_read`/`_may_read_beyond_holding`/`_manages`(O-21·O-22) · `_readable_children`(O-9) · `_require_children_finished`(`:506-511`) · `requires_completion_review`(`:513-515`) · `submit_completion`(`:517-552`) · `accept_delivery`(`:556-562`) · `_requester_of`(`:649-653`, 대행 없음 — O-29·O-31) · `readable_tasks`/`_list`(`:299-349`) | BE | 2·4·5 |
| `modules/work/lifecycle.py` | 순수 상태 전이. `TaskState` 에 `BLOCKED`·`COMPLETION_SUBMITTED` 가 남아 있다(O-5) · `_ALLOWED_TRANSITIONS` · `DONE` 전이의 요청 Task 거부(`:81-83`) | BE | 2·5 |
| `modules/work/assignments.py` | 배정·재배정 application. `reassign()`(`:166-198`) · `accept`/`decline`/`cancel`/`inbox`/`sent`(O-15) · `plan_project_work` | BE | 3 |
| `modules/work/assignment_commands.py` · `task_commands.py` · `task_values.py` · `task_results.py` | 입력 모델·결과 투영 | BE | 2·3·5 |
| `modules/work/materials.py` | 자료 목록·업로드·`open`(다운로드)·`detach`. 읽기 판정은 `_readable()`(`:290-297`)이 `ReadableWorkPort` 에 위임 | BE | 4 |
| `modules/work/material_search.py` · `material_search_policy.py` | 자료 검색. 후보 집합은 `MaterialOwnerPort.sources` 가 정한다 | BE | 4 |
| `modules/work/material_extraction.py` · `material_results.py` · `material_query_results.py` | 미리보기·본문 추출 투영 | BE | 4 |
| `modules/work/graph.py` | 관계 그래프 — `readable_tasks`/`readable_task` 를 통해 같은 판정을 쓴다 | BE | 4 |
| `platform/work_tasks.py` | 저장소. `create_task_for_request()`(`:1260-1340`, 활성 담당을 즉시 `active`+`accepted_at` 으로 세운다) · `create_accepted_task()`(O-3, `:1252-1258`) · `active_assignment_for()`(O-11, `:1816-1824`) · `reassign()`(O-12, `:1825-1861`) · `decide()` 거절이 Task 를 `CANCELLED` 로(O-13, `:1903-1911`) · `hand_to()`(O-14) · `cancel()`(O-16) · `create_assigned_task()`(O-28) · `open_children_of()`(O-17·O-20, `:473-475`) · `children_of()` · `withdraw()`(`:1091-1105`) | BE | 1~5 |
| `platform/persistence.py` | ORM. `tasks`(`:897-948`) · `work_requests`(`:1511-1544`) · `task_assignments`(`:1558-1594`) · `TaskCreationAttemptRecord` | BE | 1 |
| `platform/action_center.py` | 판단함 — 요청/배정/완료 확인/AX 제안 네 종류의 봉투와 명령 실행. `withdraw` 분기(`:259-260`) · 완료 확인자 본인 제한(`:1320-1323`, O-32) | BE | 2·3·5·6 |
| `modules/actions/policy.py` | 판단 항목이 내주는 **허용 명령** — `available_assignment_commands` · `available_delivery_commands`(`reviewer_id == principal.id`, O-32) · `available_work_request_commands` | BE | 2·3·5 |
| `modules/actions/replay.py` · `domain.py` · `commands.py` · `results.py` | 재전송 영수증·회차 | BE | 2·5 |
| `entrypoints/http.py` | REST. 기존 업무·요청 경로 전수는 아래 § 입구 전수 | BE | 6 |
| `entrypoints/mcp.py` | MCP 도구와 역량 맵(`:140-202`) | BE | 6 |
| `modules/ax_execution/tool_catalog.py` · `command_contracts.py` | AX 도구 정의와 확인 payload | BE | 6 |
| `modules/meetings/followups.py` | 회의 후속 승격 — 요청 발송 계약을 그대로 쓴다(우회 adapter 없음) | BE | 6 |
| `bootstrap/application.py` | 조립. `_SessionReadableWork`(`:640-659`)가 `readable_task_ids`/`may_read_task` 를 낸다 · 승격 호출부(`:1858`·`:3573`) | BE | 4·6 |
| `bootstrap/material_sources.py` | 자료 소유자 판정 — `sources()` 가 task/work_request/folder/meeting/report 축의 후보를 모은다 | BE | 4 |
| `bootstrap/schema_sync.py` | 로컬 스키마 동기화. **기존 테이블에 인덱스를 더하지 않는다**(O-24, `:18-47`) · NOT NULL + server_default 없음이면 `manual` (O-25) | BE | 1 |
| `bootstrap/scenario.py` · `bootstrap/operation_inventory.py` | seed 시나리오 · 운영 인벤토리 | BE | 6 |
| `docs/unified-operations-inventory.json` | HTTP·MCP 스키마 스냅샷. **diff 난 항목만 패치** | BE | 6 |
| `frontend/src/lib/api.ts` | REST 클라이언트 — 새 명령 8종이 여기 선다 | FE | 2~7 |
| `frontend/src/lib/viewModels.ts` | 타입 — `DirectTask` · `ActionItemEnvelope`(`:502-528`) · `TaskAssignment` · `WorkRequest` · `MeetingRow`(`:843-854`) | FE | 2~7 |
| `frontend/src/lib/labels.ts` | 상태·필터 라벨과 옵션(`taskFilterOptions` 등) | FE | 7 |
| `frontend/src/features/work/MyWorkPage.tsx` | 화면 본체 — 현재 탭 `mine`/`sent`/`organization`(`:429-440`) · 칩 바 · 보기 방식(`:454-461`) · 표 | FE | 7 |
| `frontend/src/features/work/WorkModals.tsx` | 생성 모달·상세 드로어·요청 상세 드로어·빠른 액션 | FE | 2~7 |
| `frontend/src/features/work/WorkViews.tsx` | 카드·칸반·타임라인 | FE | 7 |
| `frontend/src/shell/InboxRail.tsx` · `CalendarRail.tsx` · `AppShell.tsx` · `SideNav.tsx` | 좌·우 레일과 셸 | FE | 7 |
| `frontend/src/ds/icons/glyphs.tsx` | 글리프 40종 — 시안이 부르는 9종이 없다 | FE | 7 |
| `frontend/src/ds/*` | DS 부품 35종 — **이번에 신설하지 않고 조립한다** | FE | 7 |

### 계약이 닿는 입구 — 전수 (직접 grep 으로 셌다)

「목록 N개」를 받고 시작하면 목록 밖에서 FAIL 한다. 아래는 이번 계약이 지나는 **실제 입구 전부**다.

**업무·요청을 만드는 입구 (생성 축)**

| 입구 | 무엇 | v2 에서 |
|---|---|---|
| `POST /api/tasks` | 한 명령 두 갈래 — 담당 없음/본인 = 본인 업무, 타인 = **수평 요청**(O-26) | 타인 갈래가 `open` Task + 수락 대기. **입구·응답 묶음·거절 필드는 그대로** |
| `POST /api/work-requests` | 요청 발송 표면 | **`parent_task_id` 신규** · `supersedes_request_id` 신규 |
| `POST /api/projects/{id}/tasks` | 프로젝트 계획 업무(`plan_project_work`) — 담당 없음 | 변경 없음. 첫 지정은 M-2 |
| `POST /api/tasks/assign` | 관리자 배정(`managed`) — 즉시 `active`(O-28) | **현행 유지 회귀** |
| MCP `task.create_self` · `task.assign` · `work_request.create` | 같은 판정 | 같은 계약(K-10) |
| AX `tool_catalog` 의 `task.create_self`·`task.assign`·`work_request.create` 확인 payload | 사람 확인 뒤 실행 | 같은 계약 · **확인 전 effect 없음(K-5)** |
| 회의 승격 — `modules/meetings/followups.py` → `bootstrap/application.py:1858`·`:3573` | `allow_self_assignment=True` 를 켜는 **유일한 두 호출부**(O-30) | v2 에서도 **수락 대기**. 자동 수락 신설 없음 |
| `bootstrap/scenario.py` seed | demo 데이터 | 새 상태에 맞춰 갱신 |

**응답·회신 명령 (판단 축)**

| 입구 | 무엇 |
|---|---|
| `POST /api/work-requests/{id}/accept` · `/reject` · `/negotiate` · `/resubmit` · `/amend` | 요청 판단·재상신·수정 |
| `POST /api/tasks/{id}/reassign` · `POST /api/task-assignments/{id}/accept` · `/decline` | 담당 변경과 그 응답 |
| `POST /api/actions/{action_id}/decide` · `POST /api/action-items/{id}/commands/{command}` | **판단함 경유의 같은 명령** — 요청 `accept`/`adjust`/`reject`/`revise`/`withdraw`, 배정 `accept`/`decline`/`cancel_assignment`, 완료 `accept`/`request_changes` |
| `POST /api/tasks/{id}/start` · `/complete` · `/cancel` · `/block` · `/resume` | 수행 상태 전이 |
| `POST /api/tasks/{id}/completion-report` | **완료 보고 제출** — `complete` 와 이미 다른 명령이다(O-34) |
| MCP `work_request.accept`·`reject`·`negotiate`·`amend` · `task.assignment.accept`·`decline` · `task.transition` · `task.completion.submit` · `task.reassign` | 같은 계약 |

> **`withdraw` 는 HTTP 라우트가 없다.** 순수 층(`request_lifecycle.withdraw_work_request`)과
> application(`requests.withdraw`, `:514-529`)은 있고, **판단함 명령으로만 열려 있다**
> (`action_center.py:259-260` · `policy.py:97`). v2 는 이것을 **요청자의 일반 명령**으로 올린다.

**읽기·자료 표면 (BASE U-5 의 전수)**

요청 관계 읽기 권한(V-21)이 닿아야 하는 자리. **한 곳만 열면 다른 곳에서 샌다.**

| 표면 | 판정이 지나는 자리 |
|---|---|
| `GET /api/tasks/{id}` | `TaskApplication.get()` → 실패 시 `_related_view()` |
| `GET /api/tasks` · `/api/tasks` (my_work) | `readable_tasks()`/`my_work()` → `_list()` |
| `GET /api/tasks/{id}/materials` | `TaskMaterialApplication.list()` → `_readable()` → `ReadableWorkPort.may_read_task` |
| `GET /api/tasks/{id}/materials/{material_id}/content` | 같은 `_readable()` (`open()`) |
| `GET /api/materials/search` · `GET /api/materials/{id}` | `MaterialSearchApplication.search()` → `SessionMaterialOwners.sources()` → `readable_tasks()` |
| 미리보기·본문 추출 | 같은 `sources()` 가 낸 후보에만 붙는다 |
| `GET /api/work-requests/{id}/attachments/{id}/content` | `work_request` 축 — 요청자는 이미 읽는다 |
| `GET /api/tasks/{id}/history` · `/history/diff` | `_readable(principal, task_id)` |
| 관계 그래프 `graph.py` | `_SessionGraphSource.readable_tasks/readable_task` |
| MCP `task_get` · `task_subtasks` · `material_search` · `task_material_list` | 같은 application 을 부른다 |

> **여기서 한 가지가 이미 어긋나 있다 — 이 work 가 닫아야 하는 자리다.**
> `_may_read()` 는 `get()` 을 불러 **`_related_view` 성공까지 True** 로 치는데(`application.py:453-458`),
> 자료 쪽이 쓰는 `may_read_task()` 는 **`readable_task_ids()`(= `_list()`)** 로 답한다
> (`bootstrap/application.py:653-659`). `_list()` 에는 **요청 관계 길이 아예 없다.**
> 그래서 지금도 「요청자가 상세는 여는데 그 업무의 자료는 못 연다」가 성립한다.
> **두 답을 한 자리에서 나오게 하는 것이 Phase 4 의 핵심**이다.

## Domain / Schema

**schema 정본은 코드와 migration 이다.** 아래는 **구현 중 가정**이고 전문을 복사하지 않는다.

| Entity | 역할 |
|---|---|
| `work_requests` | 요청 관계와 과정 (L-3) |
| `tasks` | 수행 본체 (L-3) |
| `task_assignments` | 담당 관계와 변경 이력. **권한 배분 전용이 아니다** (L-4) |
| `task_proposals` **(신규 후보)** | 수락 후 취소·조건 변경 제안 (`kind` = `cancellation` \| `terms_change`) |
| `work_request_list_entries` **(신규 후보)** | 요청자 목록에서의 취소 항목 정리 (L-6 · P-12) |

### 코드에서 확인한 현재 스키마 — 무엇이 이미 있나

**중요: 하위 관계와 담당 교체는 새 컬럼이 거의 필요 없다.**

- `tasks.parent_task_id` 가 **이미 있고 인덱스도 있다**(`persistence.py:937`).
  재귀 저장은 **스키마 변경이 아니라 애플리케이션 제한 제거**다(O-6).
- `tasks` 의 유일 인덱스 `uq_tasks_source_work_request`(부분 유일, `:900-908`) — 요청 하나에 Task 하나.
  재요청이 새 요청·새 Task 이므로 이 제약과 부딪히지 않는다.
- `task_assignments` 에 `status` · `accepted_at` · `declined_at` · `superseded_at` ·
  `decline_reason` · `supersedes_assignment_id` 가 **이미 있다**(`:1578-1594`).
  담당 변경 v2 는 **행동 변경**이지 컬럼 추가가 아니다.
- `work_requests` 에 `promoted_by_member_id` · `causation_key`(unique) 가 있다.

### 새로 필요한 것 — additive 만

| 대상 | 무엇 | 왜 additive 인가 |
|---|---|---|
| `work_requests.parent_task_id` | 하위 요청의 상위 연결 (V-9) | **nullable FK** — `schema_sync` 가 `ADD COLUMN` 으로 더한다 |
| `work_requests.supersedes_request_id` | 재요청 연결 (V-12, 제안) | 같음 |
| `tasks.cancel_reason` | `direct`/`request_rejected`/`request_withdrawn`/`cancellation_agreed` (F-3) | **nullable** |
| `tasks.started_at` | `open → in_progress` 시각 (V-13 · L-10) | **nullable timestamp.** 현재는 `start_date`(Date, 계획 시작)에 오늘을 덮어쓴다(`lifecycle.py` 의 `start_date` 대입) — **계획과 실제가 한 칸에 섞여 있다.** 새 칸으로 가른다 |
| `tasks.completed_at` · `tasks.reopened_at` | 완료·재개 시각 (제안) | nullable |
| `task_proposals`(신규 표) | 제안·응답·회차 | **없는 표는 `schema_sync` 가 인덱스까지 함께 만든다**(O-24 의 예외가 아니라 그 규칙 그대로) |
| `work_request_list_entries`(신규 표) | 요청자 목록 정리 | 같음 |

**상태/invariant**

- 활성 담당은 **언제나 0 또는 1**(K-3). `pending` 은 그 수에 들어가지 않는다.
  같은 Task 에 `active` 1 + `pending` 1 이 **공존한다**(V-18).
- 하위 「완결」 = 취소가 아니고 · `state=done` 이며 · **요청 Task 면 `approval=approved`** (V-15·V-16).
- 저장 깊이 제한 없음, 표시 두 단계, 자기·조상 부모 금지(순환 차단).
- 한 덩어리로 처리 — (발송: 요청+Task+상위 연결) · (수락: 담당 확정) · (거절: 요청 거절+Task 취소) ·
  (담당 교체: 종료+활성화) · (완료: 완료 확정+확인 요청).

**Migration 필요 여부: 필요하다. 단일 기술안은 아래 § Migration 기술안.**

**SPEC 에 환류해야 하는 외부 resource/status/enum 변경: 없다 — 아래 § SPEC 환류 후보.**

### Migration 기술안 — 이 레포에 실제로 있는 도구로만

**있는 것과 없는 것을 먼저 가른다 (직접 확인).**

| 도구 | 실제 능력 |
|---|---|
| `make sync-demo-schema` → `reset_demo --sync` → `schema_sync.apply()` | **모델에 있고 DB 에 없는 표를 만들고**(그 표의 인덱스 포함), **없는 컬럼을 더한다.** 지우거나 타입을 바꾸지 않는다. NOT NULL + `server_default` 없음이면 실행하지 않고 **`manual` 로 사람에게 올린다**(O-25) |
| `make reset-demo` | **파괴적 초기화.** `ax_demo`/`ax_test*` 이름과 로컬 호스트로 **guard 되어 있다**(`reset_demo.require_safe_demo_database`) |
| **없는 것** | **alembic 도 migrations 디렉토리도 없다** — 레포 전체 검색 결과 0건. 버전 관리되는 migration 체계가 **없다** |
| **못 하는 것** | **기존 테이블에 인덱스를 더하는 경로가 없다**(O-24). `manual` 에도 올리지 않아 **조용히 지나간다** |

**그래서 기술안은 하나다 — 「additive 모델 변경 + `--sync` 적용 + 인덱스는 손으로, 순서를 지켜서」.**

1. **Phase 0 에서 실행 DB 를 읽기 전용으로 센다.** `information_schema` 로 `tasks`·`work_requests`·
   `task_assignments` 의 컬럼·FK·**인덱스**를 뽑아 ORM 과 대조한다(**BASE U-1**).
   **여기서 `uq_tasks_source_work_request` 가 실제 DB 에 있는지 반드시 본다** — W1 이 이 유일 인덱스를
   `tasks` **기존 표**에 더했고, `schema_sync` 는 기존 표의 인덱스를 만들지 않는다.
   **없으면 이번 작업의 선행 항목**이고, 있으면 그대로 간다.
2. **모델 변경은 전부 additive 로 쓴다.** 위 표의 새 컬럼은 **전부 nullable** 이고,
   새 표는 **새 표**다. `NOT NULL` 을 새로 쓰지 않는다 — 쓰면 `schema_sync` 가 멈추고
   사람이 기존 행의 값을 정해야 한다(O-25).
3. **격리 PG 에서 먼저 돌린다.** `POSTGRES_TEST_URL` 의 `ax_test` 에 `--sync` 를 적용하고
   `make test-postgres` 로 FK·유일성·잠금·경합을 본다. **운영·사용자 DB 에는 아직 손대지 않는다.**
4. **인덱스는 별도 명시 단계이고, 적용 단위는 레포 안의 `.sql` 파일 둘이다.** 새 표의 인덱스는
   `--sync` 가 만든다. **기존 표에 더할 인덱스**(`work_requests.parent_task_id` ·
   `work_requests.supersedes_request_id`. `tasks.parent_task_id` 는 이미 있다)는 `--sync` 가
   만들지 않으므로(O-24) **DDL 을 파일로 남긴다** — Phase 1 이 만든다.
   - `backend/migrations/manual/2026-09-17-w2-indexes.sql` — **격리 검증용.**
     `CREATE INDEX IF NOT EXISTS`. 트랜잭션 안에서 돈다.
   - `backend/migrations/manual/2026-09-17-w2-indexes.concurrent.sql` — **운영 적용용.**
     `CREATE INDEX CONCURRENTLY IF NOT EXISTS` — 쓰기를 막지 않는 대신 **트랜잭션 블록 안에서
     돌 수 없다.** autocommit 으로 실행하고, 실패하면 **INVALID 인덱스가 남으므로** 그것을
     `DROP INDEX` 한 뒤 다시 시작한다.
   **두 판을 한 파일에 나란히 두지 않는다**(통째로 돌리면 중복 생성이거나 트랜잭션 안에서 죽는다).
   **정의는 두 파일에서 같고**, 머리에 어느 쪽을 언제 쓰는지 적는다.
   **이것은 migration 체계가 아니다** — alembic 도 migrations 디렉토리도 이 레포에 없고,
   이 둘은 **손으로 적용하는 `.sql`** 이다. **「새 migration 이 이미 있다」고 쓰지 않는다.**
5. **데이터 변환은 하지 않는다.** 기존 `active` 를 `pending` 으로 되돌리지 않고(P-8),
   수락 이력을 만들지 않으며(P-8), 부모를 추정해 채우지 않고(P-9), 취소된 재배정을 복원하지 않는다(P-10).
   **새 완결 판정은 기존 `accept` 판단 행을 읽는다** — 없던 승인을 만드는 것이 아니다(O-33 · 호환 매핑).
6. **운영 DB 초기화를 대안으로 쓰지 않는다**(P-11). `reset-demo` 는 **demo/test 이름에만** 걸린다.

**Rollout 순서 (앞이 뒤를 막지 않게)**

```text
① 읽기 전용 점검(Phase 0)          → 예외 행 0건 확인. 0건이 아니면 사용자에게 올린다
② 스키마 추가(컬럼·표)              → --sync. 전부 nullable/새 표라 기존 행이 그대로 산다
③-a 인덱스 — 격리 검증(에이전트)     → 2026-09-17-w2-indexes.sql(비-CONCURRENTLY) 적용 + pg_indexes 확인
③-b 인덱스 — 운영 적용(사람)         → 같은 정의의 .concurrent.sql, 트랜잭션 밖(autocommit)에서 실행.
                                      실패 시 INVALID 인덱스(indisvalid=false)를 DROP INDEX 하고 다시 시작
④ 코드 배포 — 읽기 쪽 먼저          → 새 컬럼을 「있으면 읽는다」로만 쓴다
⑤ 코드 배포 — 쓰기·새 규칙          → 수락 대기·완결 판정·재귀 하위·읽기 권한이 함께 켜진다
⑥ 관측                              → 완료가 새로 거부되는 행이 있는지 본다
```

**Rollback**

| 되돌리는 것 | 어떻게 |
|---|---|
| ⑤ 새 규칙 | **코드 롤백.** 추가된 컬럼·표는 **그대로 둔다** — nullable 이라 옛 코드가 무시한다 |
| ④ 읽기 | 같음 |
| ③ 인덱스 | `DROP INDEX CONCURRENTLY`(트랜잭션 밖). 데이터에 영향 없다. INVALID 로 남은 것도 같은 명령으로 지운다 |
| ② 컬럼·표 | **되돌리지 않는 것이 기본이다.** 지우면 ⑤ 사이에 쌓인 값(수락 시각·취소 사유·제안 행)이 사라진다 |
| 데이터 | **되돌릴 데이터 변환이 없다** — ⑤ 이후 새로 쓴 행만 있고 기존 행은 변환하지 않았다 |

> **코드 롤백만으로 데이터까지 복구된다고 가정하지 않는다**(P-11).
> ⑤ 이후에 생긴 「수락 대기 상태의 요청 Task」는 옛 코드에서 **활성 담당이 없는 Task** 로 보인다.
> 그것은 **잘못된 상태가 아니라 새 사실**이고, 롤백은 그 사실을 지우지 않는다. 그 구간이
> 얼마나 되는지는 ⑥ 관측이 답한다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| FE 화면(Phase 7) | `GET /api/tasks/{id}` 의 `derived` · `children` · `child_progress` · `blocking_children` | 시안의 배지·행 액션·두 단계 표시가 전부 이 값 위에 선다 |
| FE 「보낸 업무」 표 | 요청 상태 여섯 + `origin.kind` | 요청과 배정을 **행에서 구분**하려면 둘 다 필요하다. `origin.kind` 는 **이미 나온다**(`work_request`/`direct_assignment`/`self_created`) |
| FE 필터 칩 | `derived.assignment` · `derived.approval` · `overdue_days` | 칩은 상태 나열이 아니라 파생 조건이다 |
| MCP · AX | 같은 application 메서드 | 새 명령이 REST 에만 서면 K-10 이 깨진다 |
| 후속 배정 정책(M-1~M-3) | `task_assignments` 의 `pending`/`active` 분리 조회 | 이 work 가 `active_assignment_for()` 를 두 조회로 가른다(P-3) |
| 후속 W2 enum 정리 | `TaskState` | 이 work 는 `completion_submitted` 를 **없애지 않고 읽기만** 한다 |

## Internal Interface Contract

SPEC-003 §4 의 외부 계약을 복제하지 않는다. **내부 층 사이의 약속만** 고정한다.

- **`active_assignment_for()` 를 둘로 가른다** (P-3 · O-11):
  `current_assignment_for(task_id)` → `status="active"` 한 행(0 또는 1) ·
  `pending_assignment_for(task_id)` → `status="pending"` 한 행(0 또는 1).
  **기존 호출부를 전수로 옮긴다** — 섞어 쓰던 자리가 남으면 담당 변경 대기에서 조용히 어긋난다(DEC-002 리스크).
- **읽기 판정은 한 함수에서 나온다**: `TaskApplication` 이 `may_read_task(principal, task_id)` 와
  `readable_task_ids(principal)` 를 **같은 규칙으로** 답한다. `_list()` 에 요청 관계 길을 더하고
  `_may_read()` 가 그 길을 쓴다. `bootstrap/application.py:_SessionReadableWork` 는 그 둘을 **그대로 위임**한다.
- **완결 판정은 한 함수다**: `is_child_settled(task) -> bool` — 취소 제외 · `state` · 요청 Task 면 승인까지.
  `_require_children_finished()` 와 `child_progress`/`blocking_children` 투영이 **같은 함수**를 쓴다.
- **제안–응답의 공통 규칙 넷**(DEC-002 D-6)을 코드에서도 한 곳에 둔다 —
  제안만으로 안 바뀐다 · 상태 넷 · 응답자 한정 · 이력과 회차 필수.
  **저장 표면은 둘로 남는다**: 담당 변경은 `task_assignments`, 취소·조건 변경은 `task_proposals`.
- **멱등 원장은 W1 것 그대로**: `(행위자 · 명령 종류 · 키)`. 새 명령이 생성 명령이면 같은 원장을 쓴다.

## Execution

각 Phase 의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나다.
Phase 별 `검증` + `완료 증거`가 완료 조건이다.

### 단계 순서와 병행 가능 지점

```text
Phase 0 ──▶ Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ Phase 4 ──▶ Phase 5 ──▶ Phase 6 ──▶ Phase 8
                          │           │           │           │           │
                          └───────────┴───────────┴───────────┴───────────┴──▶ Phase 7 (FE)
```

- **Phase 0·1 은 BE 단독이다.** 이 동안 FE 는 **시안 대조와 글리프 9종 추가**(Phase 7-A)를
  병행할 수 있다 — API 를 소비하지 않는 조각이다.
- **Phase 2~6 의 BE 절반과 Phase 7 의 FE 절반이 통합 단위로 짝을 이룬다**(아래 표).
  FE 는 짝이 되는 BE 가 끝나야 **소비**를 붙이지만, **화면 뼈대와 목데이터 렌더링은 먼저 할 수 있다.**
- **Phase 8 은 둘 다 끝나야 시작한다.**

### 통합 단위 — API 생산과 FE 소비를 함께 닫는다

**「API 는 냈는데 화면이 무시하는 창」과 「화면이 부르는데 API 가 없는 창」을 만들지 않는다.**
아래 한 줄이 한 통합 단위이고, **BE 절반과 FE 절반이 같은 단위에서 닫힌다.**

| # | BE 가 내는 것 | FE 가 쓰는 것 | 닫히는 Phase |
|---|---|---|---|
| I-1 | `POST /api/work-requests` 의 `parent_task_id` · 발송 후 `derived.assignment=awaiting_acceptance` | 업무 만들기 모달의 **담당자 지정 자리** · 하위에서 「요청 보내기」 | 2 ↔ 7 |
| I-2 | `accept`/`reject`/`negotiate`/`withdraw` 의 REST 명령과 요청 상태 여섯 | 내 업무 행의 **수락/거절** · 보낸 업무 배지 · 「다시 요청」 | 2 ↔ 7 |
| I-3 | **멱등 키 서버 필수화**(발송·본인 업무 생성) | **FE 가 `Idempotency-Key` 를 보내기 시작** | 2 ↔ 7 |
| I-4 | `reassign` 이 기존 담당을 닫지 않음 · `GET /api/tasks/{id}/assignments` 가 현재/대기를 **각각** | **담당 변경 대기** 표시(기존 담당 + 새 제안 둘 다) | 3 ↔ 7 |
| I-5 | 재귀 하위 저장 · `children` 이 언제나 직속 하위 · `child_progress` | **중심 업무 + 직속 하위 두 단계** 표시와 하위 생성 자리 | 4 ↔ 7 |
| I-6 | 요청 관계 읽기 권한이 상세·자료·검색에 함께 | 요청자 화면에서 하위·자료 열기 | 4 ↔ 7 |
| I-7 | `blocking_children` 과 `WORK_CHILDREN_UNFINISHED` 본문의 **하위 이름** | 거부 사유와 막는 하위를 보여 주는 자리 | 5 ↔ 7 |
| I-8 | `proposals`(취소·조건 변경) · `reopen` · `DELETE …/list-entry` | **취소 제안·동의·재개·목록 정리**를 여는 자리 | 5 ↔ 7 |

> **I-3 이 특히 한 단위여야 한다.** 서버가 멱등 키를 필수로 만드는 커밋과 FE 가 키를 싣기
> 시작하는 커밋이 갈리면, 그 사이의 화면에서 **생성이 전부 422 로 막히거나**(서버가 먼저) —
> **재시도가 새 업무가 된다**(FE 가 먼저). 둘을 같은 통합 단위에서 닫는다.
> (W1 이 이미 키를 필수로 만들었으므로 이번에 확인할 것은 **새로 여는 발송 표면**이다.)

---

### Phase 0 — 기준선과 읽기 전용 점검

- **Status**: DONE
- **설명**: 무엇을 고칠지 정하기 전에 **지금 무엇이 있는지**를 센다. 작업본과 실행 DB 를 가르고,
  계약이 닿는 입구를 **목록이 아니라 직접 검색으로** 다시 센다. **이 Phase 에서 코드를 고치지 않는다.**
- **작업**:
  - [ ] `git status`·HEAD 를 확인하고 `v2-code-baseline/manifest.json` 의 **82 파일 sha256** 과 대조한다.
        **코디네이터가 발주 직전 82 파일 일치를 확인했다** — 착수 시 다시 대조해
        **다르면 그 파일을 먼저 보고한다**(다른 세션이 W1 을 계속 건드리고 있다 · **BASE U-4**).
  - [ ] 위 § 입구 전수의 검색을 **다시 돌린다**(HTTP 라우트 · MCP 도구맵 · AX 도구 · 판단함 명령 ·
        자료 읽기 표면). **브리프의 목록을 믿지 않고 grep 결과를 원장으로 삼는다.**
  - [ ] 실행 DB 에 **읽기 전용**으로 붙어 `information_schema.columns` · `table_constraints` ·
        `pg_indexes` 로 `tasks`·`work_requests`·`task_assignments` 를 뽑아 ORM 과 대조한다(**BASE U-1**).
        **`uq_tasks_source_work_request` 인덱스의 실재를 따로 확인한다.**
  - [ ] **BASE U-6 점검 SELECT 한 번** — 「`source_work_request_id` 가 있고 `state='done'` 인데
        그 요청의 `accept` 판단 행이 없는 Task」를 **센다**. 읽기만 한다.
  - [ ] **부분 유일 인덱스가 만들어질 수 있는지 중복을 센다** — `uq_tasks_source_work_request` 가
        실행 DB 에 **없었다면 그동안 중복이 들어갈 수 있었다는 뜻**이고, 만들려는 순간 실패한다.
        `SELECT source_work_request_id, count(*) FROM tasks WHERE source_work_request_id IS NOT NULL
        GROUP BY 1 HAVING count(*) > 1;` — **존재 여부만 세지 않고 중복까지 센다.
        0건이 아니면 인덱스를 만들 수 없다 — 사용자에게 올린다.**
  - [ ] `assigned` 요청 상태 문자열이 실제 행에 실려 있는지 센다(**BASE U-2**).
  - [ ] 격리 PG(`ax_test`)를 준비하고 **변경 전** `make test-unit` · `make test-contract` ·
        `make test-postgres` · `make frontend-test` 를 돌려 **변경 전 기준선 수치**를 기록한다.
        **이 넷은 2026-09-17 코드 변경 전에 코디네이터가 이미 현재 코드에서 직접 돌렸다.**
        `make test-unit` **322 passed** · `make test-contract` **976 passed** ·
        `make frontend-test` **645 passed** · `make test-postgres` **65 passed** — **넷 다 exit 0**
        (Node 20.20.0 · `PYTEST_XDIST_AUTO_NUM_WORKERS=4` · 격리 `localhost:54329/ax_test`).
        **증거**: `orchestration/work/strong-hajin-work/v2-phase0-verification.md` 와
        `v2-phase0-test-unit` · `v2-phase0-test-contract` · `v2-phase0-frontend-test` ·
        `v2-phase0-test-postgres` 의 `.log`/`.exit`. **착수 시 그 증거를 완료 증거로 참조할 수 있다** —
        **baseline 82 파일 sha 가 일치하는 동안만** 유효하고, 어긋나면 넷을 다시 돌린다.
        **과거 W1 수치가 아니라 현재 코드의 수치다.**
  - [ ] `node -v` 로 **Node 20** 을 확인한다(W1 검증에서 Node 25 가 `localStorage` 로 깨졌다).
  - [ ] **위 넷은 「현재 코드가 초록」이라는 기준선일 뿐 v2 통과가 아니다** — Phase 1~8 의 모든 통과 수치는
        **이번 판에서 새로 실행한 것**이어야 한다. **과거 수치를 v2 통과 근거로 쓰지 않는다**(P-7).
        **실제 업무 데이터(`ax_demo`)는 빈 DB 이므로 데이터 이관 검사를 했다고 쓰지 않는다.**
- **검증**:
  - [ ] 수정 대상 파일과 W1 미커밋 변경의 **경계**가 기록돼 있다.
  - [ ] 실행 DB 확인 여부가 **했다/못 했다**로 기록돼 있다. 못 했으면 그렇게 적는다 —
        SQLite 로 대신했다고 쓰지 않는다(P-7).
  - [ ] **BASE U-6** SELECT 의 **건수**가 기록돼 있다. **0건이 아니면 사용자 결정으로 올린다**(옛 OQ-205).
  - [ ] **변경 전 4종의 수치와 exit 코드가 로그와 함께** 남아 있다(위 `v2-phase0-*` 참조 가능).
        **그 수치를 v2 통과로 쓰지 않는다** — 기준선과 v2 검증을 갈라서 적는다.
- **완료 증거**: `v2-phase0-verification.md` 4종 exit0(322/976/645/65), `v2-be-phase0-report.md` 읽기전용 관측 및 U-6 정정, 발주 직전 manifest 82/82 일치. 실데이터 DB가 없어 U-1/U-2/U-6 및 운영 인덱스 실재 판정은 배포 전 이월; 빈 DB 0건으로 완료 처리하지 않는다.

---

### Phase 1 — 관계·저장 구조와 migration 기술안을 격리 DB 에서 닫는다

- **Status**: DONE
- **설명**: 위 § Domain/Schema 의 additive 안을 **실제 모델에 넣고 격리 PG 에서 돌려** 본다.
  컬럼·FK·인덱스·트랜잭션 경계가 말이 되는지 여기서 판정한다.
- **작업**:
  - [ ] `work_requests.parent_task_id`(nullable FK → `tasks.id`) ·
        `work_requests.supersedes_request_id`(nullable FK → `work_requests.id`) 를 모델에 더한다.
  - [ ] `tasks.cancel_reason`(nullable) · `tasks.started_at` · `completed_at` · `reopened_at`(nullable) 을 더한다.
  - [ ] `task_proposals` 표를 정의한다 — `task_id` · `kind` · `state` · `proposed_by` · `responder_id` ·
        `payload` · `reason` · `version` · 시각들. **한 Task 에 같은 종류의 `pending` 은 하나**(부분 유일 인덱스).
  - [ ] `work_request_list_entries` 표를 정의한다 — 요청자 목록에서만 빼고 **행은 지우지 않는다**.
  - [ ] `active_assignment_for()` 를 `current_assignment_for()`/`pending_assignment_for()` 로 가르고
        **호출부를 전수로 옮긴다**(grep 으로 세고 시작한다).
  - [ ] `make sync-demo-schema` 를 **격리 DB 에** 적용하고 **이번에 더한 컬럼·표가 `manual` 출력에
        없는지** 본다. 있으면 그 컬럼을 nullable 로 고쳐 다시 돌린다.
  - [ ] **기존 표에 더할 인덱스의 DDL 을 레포 안 파일 둘로 남긴다 — 그 파일이 적용 단위이자 증거다.**
        - `backend/migrations/manual/2026-09-17-w2-indexes.sql` — **격리 검증용.**
          `CREATE INDEX IF NOT EXISTS`. 트랜잭션 안에서 돈다.
        - `backend/migrations/manual/2026-09-17-w2-indexes.concurrent.sql` — **운영 적용용.**
          `CREATE INDEX CONCURRENTLY IF NOT EXISTS`. **트랜잭션 블록 안에서 돌 수 없으므로**
          `BEGIN`/`psql -1` 없이 **autocommit 으로** 실행한다.
        **두 판을 한 파일에 나란히 두지 않는다** — 한 파일을 통째로 돌리면 같은 인덱스를 두 번 만들거나
        `CONCURRENTLY` 가 트랜잭션 안에서 죽는다. **인덱스 정의는 두 파일에서 같아야 하고**, 각 파일
        머리에 **어느 쪽을 언제 쓰는지**를 적는다.
        대상은 **기존 표에 더하는 인덱스뿐**이다 — `work_requests.parent_task_id` ·
        `work_requests.supersedes_request_id`. (새 표의 인덱스는 `--sync` 가 만들고,
        `tasks.parent_task_id` 는 **이미 있다** `persistence.py:937`.)
        **`schema_sync` 가 만들 것이라고 쓰지 않는다**(O-24). **alembic 도 migrations 체계도 이 레포에
        없다** — 이 둘은 **손으로 적용하는 `.sql`** 이고, **「migration 체계를 세웠다」고 쓰지 않는다.**
- **검증**:
  - [ ] 격리 PG 에서 `make test-postgres` 가 **변경 전과 같은 수치**로 통과한다(회귀).
  - [ ] **이번에 더한 컬럼·표가 `--sync` 의 `manual` 에 없다** — 기존 행의 값을 사람이 정할 자리가 없다.
        (`plan()` 은 **모델에 없는 기존 컬럼**도 `manual` 에 넣으므로 `manual` 목록 전체가 비기를
        기대하지 않는다 — `schema_sync.py:44-45`.)
  - [ ] 새 표의 인덱스가 실제로 생겼는지 `pg_indexes` 로 확인한다.
  - [ ] **격리 PG 에서 기존 표의 인덱스 결손을 인위로 재현해 닫는다** — 대상 인덱스를 `DROP INDEX` 하고
        **`make sync-demo-schema` 를 다시 돌려도 생기지 않는 것**을 먼저 확인한다(그것이 O-24 의 재현이다).
        그 다음 `2026-09-17-w2-indexes.sql`(비-CONCURRENTLY 판)을 적용하고 `pg_indexes` 로 재확인한다.
        **한 번 더 적용해도 실패하지 않는다**(`IF NOT EXISTS` — 재적용 가능).
  - [ ] **`CONCURRENTLY` 판은 격리 PG 에서 「트랜잭션 밖에서 돈다」만 확인한다.** 실패하면
        **INVALID 인덱스가 남아 다음 시도를 막는다** — `pg_index.indisvalid = false` 로 찾아
        `DROP INDEX` 하고 다시 시작하는 **회복 절차를 기록한다.**
        **격리 검증을 운영 적용으로 쓰지 않는다** — 운영 적용은 Rollout ③-b 에서 사람이 한다.
  - [ ] `active_assignment_for` 를 부르던 자리가 **0건** 남아 있다(grep).
- **완료 증거**: 미작성

---

### Phase 2 — 요청: 발송 · 수락 · 거절 · 협의 · 철회 · 재요청

- **Status**: DONE
- **설명**: 발송이 `open` Task 와 **수락 대기**를 만들고, 수락이 **같은 Task** 의 담당을 확정한다.
  W1 이 「수락 없이 즉시 활성 담당」으로 세운 자리를 **응답 단계만** 되돌린다.
- **작업**:
  - [ ] `create_task_for_request()` 가 담당 행을 **`status="pending"`, `accepted_at=None`** 으로 세운다.
        Task 는 `state=open` 그대로다. **주석의 「수락 없이」 설명을 함께 고친다** — 낡은 주석이
        다음 사람을 오도한다.
  - [ ] `accept()` 가 **새 Task 를 만들지 않는다**. `create_accepted_task()`(O-3) 경로를 걷고,
        대신 **그 요청의 기존 Task 의 담당 행을 `active` 로 확정**한다(`accepted_at` 기록).
        `task_id` 와 `parent_task_id` 가 그대로다.
  - [ ] `reject()` 가 요청을 `rejected` 로 두고 **그 Task 를 `cancelled`**,
        `cancel_reason=request_rejected` 로 만든다. **상위 연결과 로그는 남긴다.**
  - [ ] `withdraw()` 를 **요청자의 일반 명령으로 올린다** — `POST /api/work-requests/{id}/withdraw`.
        Task 를 `cancelled`, `cancel_reason=request_withdrawn`. 판단함 경유 명령도 같은 결과를 낸다.
  - [ ] `POST /api/work-requests` 가 `parent_task_id` 와 `supersedes_request_id` 를 받는다.
        `parent_task_id` 검증은 Phase 4 의 판정(중심 업무·순환·수락 전 부모 금지)을 쓴다.
  - [ ] `POST /api/tasks` 의 `horizontal` 갈래는 **입구·응답 묶음·거절 필드를 그대로 둔다**(O-26·O-27).
        바뀌는 것은 **그 Task 의 값**뿐이다 — `assignee=null` · `derived.assignment=awaiting_acceptance`.
  - [ ] 재요청은 **새 요청·새 Task** 다. 거절된 Task 를 재사용하는 경로를 만들지 않는다.
        `supersedes_request_id` 로 잇는다.
  - [ ] 요청 상태·담당 상태·수행 상태가 섞이지 않게 **판단함 봉투와 목록 응답**을 고친다
        (`action_center.py` · `policy.py` · `request_results.py`).
  - [ ] `PATCH /api/work-requests/{id}` 가 **수락 후 거부**한다 — `WORK_REQUEST_LOCKED_AFTER_ACCEPT`.
  - [ ] 새 오류 코드를 Case Matrix 대로 낸다 — `WORK_REQUEST_NOT_PENDING` ·
        `WORK_REQUEST_RESPONDER_ONLY` · `WORK_REJECT_REASON_REQUIRED` ·
        `WORK_CANCEL_REQUIRES_AGREEMENT`(Phase 5 와 함께).
  - [ ] **`derived` 묶음을 응답 투영에 신설한다 — 서버가 만든다.**
        `TaskApplication._view()`(`application.py:1085-1112`) · 목록 투영(`_list()` `:299-349`) ·
        `_hierarchy_view`/`_related_view` · `task_results.py` 의 결과 타입에 함께 싣는다.
        **지금 코드에는 `derived` 키가 0건이고 `overdue_days` 도 0건이다**(직접 grep) —
        **없는 것을 있다고 전제하지 않는다.** **FE 가 `state`·`origin_kind` 로 추론하지 않는다**
        (SPEC-003 §2.11 「API 가 내야 하는 데이터 … 이 SPEC 의 몫이다」).
  - [ ] **묶음의 키는 SPEC-003 §4 Data Contract 의 「파생 표시」 전부**다 — `assignment` ·
        `approval` · `proposal` · `blocking_children` · `reply` · `status_note` · `overdue_days`.
        **어느 값도 `state` 에서 읽지 않고 각 원장에서 계산한다**(SPEC-001 §4).
        **어느 단계가 어느 값을 내는지 못 박는다**:
        - **Phase 2** — `assignment`(담당 행의 `pending`/`active`: `awaiting_acceptance` ·
          `awaiting_handover` · `null`) · `overdue_days`(`due_date` 에서 계산. 표시값이다)
        - **Phase 4** — `blocking_children`·`child_progress`(같은 `is_child_settled()` 를 쓴다)
        - **Phase 5** — `approval`(완료 확인 **판단 행**에서) · `proposal`(`task_proposals` 의 `pending`)
        - **이 work 가 값을 만들지 않는 둘** — `reply`·`status_note` 는 SPEC-001 계승인데
          **그 원장(문의·회신 대기·상태 메모)이 코드에 0건이다**(`inquir`·`status_note`·`reminder` grep 0건).
          **키는 묶음에 두고 값은 `null` 고정**이며, 값을 내는 것은 **SPEC-001 문의·메모 구현(후속)** 이다.
          **「이미 나온다」고 쓰지 않는다.**
  - [ ] **FE 타입을 같은 통합 단위에서 맞춘다** — `viewModels.ts` 의 Task 타입에 `derived` 를 더하고
        Phase 2 가 내는 두 값부터 읽는다. **API 는 내는데 화면이 무시하는 창을 만들지 않는다**(I-1).
- **검증**:
  - [ ] `make test-contract` — 발송/수락/거절/철회/재요청 계약. **A2·A3·B1·B5 의 기대 결과**.
  - [ ] `make test-unit` — 요청 순수 층(`request_lifecycle`) 회귀.
  - [ ] **회귀**: `POST /api/tasks` 의 `parent_task_id`·`start_date`·`project_id` 거절이 그대로다.
  - [ ] **회귀**: 멱등 키 없는 발송·본인 업무 생성이 거부되고, 재전송은 한 건이며 영수증 전에
        권한을 다시 검사한다(K-1·K-2).
  - [ ] **회귀**: 관리자 배정(`POST /api/tasks/assign`)이 **여전히 즉시 `active`** 다(O-28).
  - [ ] `GET /api/tasks/{id}` · `GET /api/tasks` 응답에 **`derived` 묶음이 실린다.**
        발송 직후 `derived.assignment == "awaiting_acceptance"` 이고 `overdue_days` 가 `due_date` 에서 나온다.
        **이 Phase 에서 값이 서는 키는 그 둘이고 나머지는 `null`** 이다 — 나머지는 Phase 4·5 가 채운다.
        `reply`·`status_note` 는 **끝까지 `null`** 이고 그것이 정상이다.
- **완료 증거**: 미작성

---

### Phase 3 — 담당 변경: 책임 공백 제거

- **Status**: DONE
- **설명**: 제안이 **기존 담당을 닫지 않는다.** 교체는 수락 한 덩어리에서만 일어나고,
  거절은 제안만 닫는다.
- **작업**:
  - [ ] `reassign()`(`work_tasks.py:1825-1861`)이 기존 `active` 를 **그대로 두고** 새 담당을
        `pending` 으로 **덧붙인다**. `supersedes_assignment_id` 로 잇는다.
  - [ ] `decide()` 의 **거절 분기가 Task 를 취소하지 않게** 가른다(O-13).
        **최초 배정 거절**(첫 지정 `hand_to()` 뒤)은 **현행 그대로 유지**하고,
        **담당 교체 제안의 거절**만 「제안만 닫는다」로 간다. 두 사건을 **각각** 기록한다(L-12).
  - [ ] 수락은 **기존 담당 `superseded` + 새 담당 `active`** 를 **한 transaction** 에서 한다.
        활성 담당 0명·2명인 중간 상태가 관찰되지 않는다.
  - [ ] 대기 중 기존 담당의 **수행·기록·완료 보고 권한과 「내 업무」 등재**가 유지된다.
  - [ ] `GET /api/tasks/{id}/assignments` 를 열어 **현재 담당과 대기 제안을 각각** 낸다.
  - [ ] 한 Task 에 대기 제안은 하나 — `WORK_ASSIGNMENT_PROPOSAL_EXISTS`.
        응답은 수신자만 — `WORK_ASSIGNMENT_RESPONDER_ONLY`.
  - [ ] 제안·수락·거절·실제 교체를 **각각** 이력으로 남긴다(L-9).
- **검증**:
  - [ ] `make test-contract` — **B3·B4** 의 기대 결과.
  - [ ] `make test-postgres` — 담당 교체와 거절의 **동시 실행**에서 활성 담당이 0·2가 되지 않는다.
  - [ ] **회귀**: 담당 없는 업무의 **첫 지정**(`hand_to()`)은 여전히 `pending` + 수락 판단 항목이다(O-14, M-2).
  - [ ] **회귀**: 배정 철회(`cancel`)의 현행 동작이 그대로다(O-16).
- **완료 증거**: 미작성

---

### Phase 4 — 재귀 하위 · 중심 업무 · 순환 차단 · 요청 관계 읽기 권한과 자료 표면

- **Status**: DONE
- **설명**: 저장 깊이를 열고 표시 깊이만 둘로 둔다. 그리고 **요청자가 자기가 부탁한 것까지만** 읽게 한다.
  **이 Phase 가 이 work 에서 가장 새는 자리다** — 한 경로만 열면 다른 경로에서 실패한다.
- **작업**:
  - [ ] `parent_for()` 의 **한 단계 제한을 걷는다**(O-6). 끝난 업무에 하위를 붙이는 금지는
        **현행 계승**으로 남긴다 — `WORK_PARENT_CLOSED`(O-7).
  - [ ] **중심 업무 판정**을 넣는다 — 부모가 없거나 **부모의 활성 담당자가 이 Task 의 담당자와 다르면**
        중심 업무다. 같은 담당자의 **직접 작업 아래 직접 작업**은 `WORK_DIRECT_NESTING`.
        **「부모가 없으면 중심 업무」로 판정하지 않는다**(V-7 · P-3).
  - [ ] **자기·조상을 부모로** 지정하면 `WORK_PARENT_CYCLE`. 작업계획서 §4.5 가 우선한다
        (example §7.8 의 미정보다).
  - [ ] **수락 전 요청 Task 아래에 하위를 만들 수 없다** — `WORK_PARENT_UNASSIGNED`.
        새 규칙이 아니라 중심 업무 판정과 「활성 담당자가 만든다」에서 그대로 나온다.
  - [ ] `_hierarchy_view`/`_related_view` 의 `children` 비우기(O-8, `:390`·`:467`)를 걷고
        **어느 Task 에서도 직속 하위**를 낸다. 읽을 수 없는 하위는 **목록에도 건수에도** 없다(O-9 유지).
  - [ ] `child_progress` 를 `{done, blocking, cancelled, total}` 로 넓히고 `blocking_children` 을
        **Phase 2 가 세운 같은 `derived` 묶음에 실어** 낸다. 둘 다 `is_child_settled()` 를 쓴다.
  - [ ] **요청 관계를 읽기의 세 번째 길로 연다** — `_list()`(= `readable_tasks`)에
        「내가 요청자인 Task 와 **그 하위 트리 전체**」를 더한다. 깊이 제한이 없다(V-21).
  - [ ] `_may_read()` 와 `readable_task_ids()` 가 **같은 규칙**을 쓰게 한다.
        `bootstrap/application.py:_SessionReadableWork` 는 **위임만** 한다.
        **이 한 줄이 「상세는 보이는데 파일은 못 연다」를 없앤다.**
  - [ ] 같은 판정이 **자료 목록 · 본문/다운로드(`open`) · 검색(`sources()`) · 미리보기** 에서
        동일한지 **Phase 0 의 표면 전수를 다시 밟아** 확인한다.
  - [ ] **수행자의 다른 업무와 미연결 자료는 `WORK_NOT_FOUND`** 다. 넓히지 않는다.
  - [ ] **조회 권한이 수정·시작·완료·배정 권한을 넓히지 않는다** — mutating 경로의 가드를 그대로 둔다.
  - [ ] **상위 관계 이동 명령을 만들지 않는다**(EU-15 · M-13).
  - [ ] **EU-6·EU-7 은 미정이다 — 이번에 넓히지도 막지도 않는다(현행 보존).**
        **새 담당자가 수락하기 전의 자료 접근 범위**(EU-6)와 **재분해·재요청을 원 요청자에게 알리는
        방식**(EU-7)은 SPEC-003 §5 가 둘 다 미정으로 남겼다. 읽기 판정을 **한 함수로 모으는 이 Phase 가
        그 둘을 무심코 정하기 쉬운 자리**이므로, 합치는 대상은 **기존 두 답의 불일치**뿐이고
        **미정 축의 값은 현행 그대로** 둔다.
- **검증**:
  - [ ] `make test-contract` — **A1·A4·A5** 와 두 단계 표시.
  - [ ] **두 단계 이상 깊이 저장**이 되고, 부모가 있는 Task 도 자기 하위를 낸다.
  - [ ] **역검증**: 요청자가 **수행자의 다른 업무**를 읽으려 하면 `WORK_NOT_FOUND` 다.
        **미연결 자료**도 같다. 검색 결과와 **건수**에도 들어가지 않는다.
  - [ ] **역검증**: 조회만 되는 사람이 `start`·`complete`·`reassign` 을 부르면 거부된다.
  - [ ] `make test-unit` — 중심 업무 판정과 순환 차단의 순수 층.
- **완료 증거**: 미작성

---

### Phase 5 — 완료 보고 · 승인 · 보완 · 합의 취소 · 조건 변경 · 재개

- **Status**: DONE
- **설명**: **끝은 사람이 낸다.** 그리고 **최종 완료와 완료 보고를 섞지 않는다.**
- **작업**:
  - [ ] **`complete` 와 `completion-report` 를 통합하지 않는다.** 새 endpoint 도 만들지 않는다(O-34).
        - `complete` — **본인·배정 업무의 최종 완료.** 하위 완결 검사가 걸린다.
        - `complete` on **요청 Task** — **거부**(「요청자의 확인이 필요합니다. 완료 보고로 제출하세요」).
          **현행 그대로**(`lifecycle.py:81-83`).
        - `completion-report` — **요청 Task 의 완료 보고 제출.** 기본값에서 하위 검사를 **걸지 않는다**.
        - **요청자 승인** — **요청 Task 의 최종 완료.** 하위 검사는 **이미 걸려 있다**(O-34).
  - [ ] **`_ALLOWED_TRANSITIONS[TaskState.OPEN]` 에 `DONE` 을 더한다**(`lifecycle.py:67`) —
        **SPEC-001 §4 State 와 SPEC-003 §4 State 가 둘 다 그린 전이다.** 환류 후보가 아니라
        **이번 판의 구현 대상**이다. **요청 Task 는 그대로 거부된다**(`requires_completion_review`
        가드 `lifecycle.py:82-83` 가 먼저 걸린다) · **하위 완결 검사도 그대로 걸린다**(`:84-86`).
        `started_at` 은 **비어 있는 채로 둔다** — 시작하지 않은 일이 끝난 것이고 V-13 과 어긋나지 않는다.
  - [ ] **내부 `TaskState.COMPLETION_SUBMITTED` 는 유지하고 외부 투영에서만 매핑한다** —
        `_view()`(`application.py:1089`)와 목록 투영이 그 값을 **`state="done"` +
        `derived.approval="awaiting_review"`** 로 낸다(SPEC-003 §4 State 「이 계약에 없다」 · §6 · §3 S-7).
        **SPEC 환류가 아니다.** 승인 가드(`accept_delivery` `:556-558`)와 제출 가드(`:536`)는
        **내부 값을 그대로 읽으므로 손대지 않는다.** enum 자체의 정리는 후속이다.
  - [ ] **완결·권한 판정을 투영 묶음에서 읽지 않는다.** `is_child_settled()` 와 읽기 권한 판정은
        **내부 원장(판단 행·담당 행)** 에서 답한다 — `state` 문자열이나 `derived.*` 를 읽어
        완결·권한을 추론하는 경로를 만들지 않는다(투영은 표시용이다).
  - [ ] **요청 Task 의 완결 판정은 「지금 완료 회차에 유효한 `accept` 판단 행」의 존재다**(O-33 · V-15).
        **아무 과거 승인 하나로 충분하지 않다** — 보완(`request_changes`)으로 회차가 올라갔거나
        `reopen` 이 있었으면 **그 이전 승인은 무효**다. 판정은 **현재 회차 번호(또는 `reopened_at`)
        이후의 승인 행**만 센다. **승인이 없으면 미완결로 확실히 판정한다** — 모르면 완결로 치지 않는다.
  - [ ] **FE 소비를 같은 단위에서 맞춘다** — `TaskState` 에서 `completion_submitted` 를 뺀다
        (`viewModels.ts:110` · `labels.ts:7,16` · `MyWorkPage.tsx:85,757` · `WorkViews.tsx:475` ·
        `WorkModals.tsx:635`). 「완료 확인 대기」는 **`derived.approval` 로 읽는다.**
        (Phase 7 의 같은 통합 단위에서 닫는다 — 투영만 바꾸고 FE 를 두면 화면이 값을 잃는다.)
  - [ ] **새로 닫는 것은 「완결」 판정 하나다**(O-20). `open_children_of()` 가 `state` 만 보던 것을
        `is_child_settled()` 로 바꾼다 — **요청 Task 면 승인까지**여야 완결이다.
        **「승인에서 막는다」를 신규 구현으로 적지 않는다.**
  - [ ] `WORK_CHILDREN_UNFINISHED` 본문이 **막는 하위의 이름**을 낸다(현행 `_require_children_finished`
        가 이미 이름 3개까지 낸다 — 그 모양을 유지하고 `blocking_children` 과 짝을 맞춘다).
  - [ ] **보완은 같은 Task 의 다음 회차**다. **하위 Task 를 자동으로 만들지 않는다**(E-3).
        **별도 검토 Task 를 만들지 않고**(V-14), **역승인 경로를 만들지 않는다**(E-12).
  - [ ] **수락된 요청 Task 의 직접 `cancel` 을 거부한다** — 요청자·담당자·관리자 **모두**
        `WORK_CANCEL_REQUIRES_AGREEMENT`. **수락 전 요청 Task·본인 업무·배정 업무의 직접 취소는 현행 그대로다.**
  - [ ] `POST /api/tasks/{id}/proposals`(`kind`=`cancellation`|`terms_change`) · `/respond` · `/withdraw` ·
        `GET …/proposals` 를 연다. **제안만으로는 아무것도 바뀌지 않는다.**
        동의 시 `cancellation` 은 `cancelled` + `cancel_reason=cancellation_agreed`,
        `terms_change` 는 새 조건 적용.
  - [ ] 제안의 「요청자」 판정은 **요청자 전용 조작과 같은 모양**을 쓴다 —
        `requester_id` **또는** `promoted_by_member_id`(O-31). 응답자는 **담당자만**.
  - [ ] `POST /api/tasks/{id}/reopen` 을 연다 — **완료된 상위가 있으면 `WORK_REOPEN_PARENT_DONE`**.
        본인 업무는 담당자, 요청 업무는 요청자(+담당자 알림). **배정 업무는 열지 않는다**(M-3).
        **이전 완료 이력·회차·결과를 지우지 않는다**(E-5).
  - [ ] `DELETE /api/work-requests/{id}/list-entry` — 요청자 목록에서만 빼고 **로그는 남긴다**.
        **전역 삭제·상대방 자료 삭제로 넓히지 않는다**(P-12).
  - [ ] **무응답·기한 초과는 아무것도 바꾸지 않는다.** 자동 전이 코드를 만들지 않는다.
        `overdue_days` 는 표시값이다.
  - [ ] **OQ-203 은 답 대기다 — 제출에 하위 검사를 더하지 않는 것은 「현행 보존」이고 새 선택의
        확정이 아니다.** 답이 오기 전에는 **정책이 정해졌다고 표시하지 않는다**(문구·주석·테스트 이름에도).
        **조건별 검증 계획**: 답이 「막지 않는다」면 지금 계획대로 — 미완결 하위가 있어도 제출은 통과하고
        **승인에서 막힌다**(A7). 답이 「막는다」면 `submit_completion()` 에 `is_child_settled` 검사 한 줄 +
        `WORK_CHILDREN_UNFINISHED` 회귀 한 줄을 더하고 §6 인수조건 한 줄을 바꾼다 —
        **바뀌는 자리는 그 둘뿐이고 나머지 Phase 는 그대로다.**
  - [ ] **OQ-206 의 승격 요청 완료 승인은 구현하지 않는다.** 그 경로에 **새 자동 승인을 만들지 않고**(E-4),
        확인자를 임의로 바꾸지도 않는다. 답이 오면 **그 한 조각만** 연다.
        **의존은 좁다** — 「요청자가 `system:meeting` 인 요청 Task 의 완료 승인을 누가 부르는가」 하나이고,
        일반 요청 축(A1~C2)과 승격의 **수정·재상신·철회**(O-31)는 이 미정과 무관하게 선다.
- **검증**:
  - [ ] `make test-contract` — **A6·A7·A8·A9·B2·B6·B7·B8·B9·B10**.
  - [ ] **`open` 상태의 본인·배정 업무를 `complete` 로 직접 완료할 수 있다.**
        **A9 를 `open` 경로로 한 번, `in_progress` 경로로 한 번 각각 돌린다** —
        **`in_progress` 를 거치게 고쳐 우회하지 않는다.**
  - [ ] **회귀**: 요청 Task 의 `open → done` 직접 완료는 **여전히 거부**된다(확인 필요 가드).
        하위가 남은 `open` 업무의 직접 완료도 **하위 완결 검사에서 거부**된다.
  - [ ] 제출 직후 응답이 **`state="done"` · `derived.approval="awaiting_review"`** 다.
        **응답 어디에도 `completion_submitted` 문자열이 없다**(REST·MCP·AX 전 표면 grep).
  - [ ] **역검증**: 제출됐으나 승인 전인 요청 하위를 둔 상위의 완료가 **거부**된다.
  - [ ] **역검증**: **보완으로 회차가 오른 뒤**·**재개한 뒤**의 요청 하위는, 이전 회차의 승인 행이
        남아 있어도 **미완결**로 세어진다.
  - [ ] `done` + 승인 전인 요청 하위가 **상위 완료 검사에서 미완결로 세어진다**.
  - [ ] **회귀**: 요청 Task 에 `complete` 를 부르면 거부된다(기존 동작).
  - [ ] **회귀**: 승인에 하위 완결 검사가 걸린다(**이미 있다** — 새로 만든 것이 아니다).
  - [ ] **역검증**: 취소된 하위는 검사에서 **제외**되고 로그는 남는다. 취소가 완료로 바뀌지 않는다.
  - [ ] **역검증**: 하위가 전부 끝나도 상위가 **자동 완료되지 않는다**.
  - [ ] **역검증**: 참고 연결(`reference_task_ids`)이 하위 완결 검사에 **들어가지 않는다**(E-6).
- **완료 증거**: 미작성

---

### Phase 6 — 표면 일치: REST · MCP · AX · 회의 승격 · seed · 인벤토리

- **Status**: DONE
- **설명**: **같은 행위 → 같은 결과**(K-10). 새 명령이 REST 에만 서면 계약이 갈린다.
- **작업**:
  - [ ] 새 명령(`withdraw` · `reopen` · `proposals` 3종 · `assignments` 조회 · `list-entry`)을
        **MCP 도구맵**(`entrypoints/mcp.py:140-202`)에 필요한 것만 올린다.
        **역량(capability)은 REST 와 같은 것을 건다.**
  - [ ] **AX `tool_catalog`** 에 올릴 것과 올리지 않을 것을 가른다.
        올리는 것은 **`requires_confirmation=True`** 다 — 확인 전 effect 없음(K-5).
  - [ ] **판단함 명령**(`modules/actions/policy.py`)이 새 상태에서 옳은 명령만 낸다.
        요청 `pending` → 수락/조정/거절, `negotiating` → 재상신/철회,
        담당 제안 `pending` → 수락/거절, 완료 `awaiting_review` → 완료 인정/보완 요청.
        **완료 확인 명령은 확인자 본인에게만**(O-32) — 그대로 둔다.
  - [ ] **회의 후속 승격**이 발송 계약을 그대로 쓴다. **우회 adapter 를 두지 않는다.**
        승격 요청도 **수락 대기**로 선다. `allow_self_assignment` 는 **그 두 호출부에만** 남긴다(O-30).
        **출처(회의)와 actor(누른 사람)는 둘 다 보존**한다(K-6).
  - [ ] `bootstrap/scenario.py` seed 를 새 상태에 맞춘다 — **하지 않은 수락을 만들지 않는다.**
  - [ ] **승격 요청 seed 를 빼서 미답 경로를 감추지 않는다.** OQ-206 이 미답이라 승격 요청 Task 의
        **완료 승인을 부를 사람이 정해지지 않는다** — 그 Task 가 완결 판정 대상이 되면 상위 완료가 막힌다.
        **seed 에서 그 경로를 제거하지 말고, 「미답으로 막히는 경로」라고 seed 주석과 Phase 8 인계 문서에
        적는다.** 막히는 것은 **미답의 결과이지 제품 버그가 아니고**, 없애면 실제 경로 결함이 숨는다.
  - [ ] `bootstrap/operation_inventory.py` 와 `docs/unified-operations-inventory.json` 의
        **차이 난 항목만 패치**한다. **전체 재작성 금지**(AGENTS.md).
- **검증**:
  - [ ] `make test-unit` — `tests/architecture/test_operation_inventory.py` 가 drift 를 잡지 않는다.
  - [ ] `make test-contract` — MCP 계약 테스트(`test_mcp*.py`)가 REST 와 **같은 결과**를 낸다.
  - [ ] **역검증**: AX 확인 전에는 effect 가 없다(K-5).
  - [ ] **역검증**: 유입 경로(회의 승격)만으로 자동 수락되지 않는다(L-15·L-16).
- **완료 증거**: 미작성

---

### Phase 7 — FE: 확정 시안 + v2 흐름

- **Status**: DONE
- **설명**: 시안이 그린 것을 그리고, **시안이 그리지 않았지만 계약이 요구하는 자리**를 만든다.
  「시안에 없다」는 **미설계**이지 **정책 부정이 아니다**.
- **먼저 가른다 — 무엇이 실물이고 무엇이 없나** (직접 확인):
  - **DS 는 거의 다 있다.** 시안 CSS 클래스 179종 중 **차집합 1종**(`.scax-select__caret`),
    토큰 **차집합 0종**. 「부품으로 안 묶였다」이지 「스타일이 없다」가 아니다.
  - **없는 것은 글리프 9종**이다 — `mail` · `message` · `external-link` · `circle-close` ·
    `circle-check` · `chevron-left-small` · `chevron-right-small` · `chat` · `image`.
    (`chevron-left` 자체가 없다.)
  - **`StateSwitch` 는 시안 스스로 dev 전용이라 적었다** — 제품에 넣지 않는다.
  - **시안 화면 파일은 `MyWork.html` 하나다.** `nav.js` 가 가리키는 `Calendar.html`·
    `MeetingWorkspace.html` 은 `.design-sync/screens/` 에 **없다**.
  - **시안 모달에 담당자 지정 자리가 없다** — 직접 읽어 확인했다(업무 명·기한·내용·
    확인받을 사람·체크리스트·첨부파일 여섯). **이것이 §2.7 이 말한 미설계다.**

- **작업 — 7-A. 병행 가능(BE 를 기다리지 않는다)**:
  - [ ] 글리프 9종을 `ds/icons/glyphs.tsx` 에 더한다.
  - [ ] `.scax-select__caret` 과 `<Icon name="chevron-down">` 중 **하나로 정한다**(둘이 공존한다).
  - [ ] 시안 표 세 벌의 **뼈대**를 목데이터로 세운다 — `TaskTable` · `SentTaskTable` ·
        `DoneTaskTable`(그룹 둘 · 접이식). 4상태(default/empty/loading/error)를 각각 그린다.
        **`TaskTable` 은 기존 `.scax-task-table--nostar` 5열을 유지한다** — 시안 6열에서 **별표만 빠진다**
        (M-21. 이미 `MyWorkPage.tsx:593-601` · `styles/components.css:401-405` 에 결정과 이유가 있다:
        「`starred` 필드도 저장 엔드포인트도 없어서 눌러도 아무 데도 안 남는다」). **별표 열을 되살리지 않는다.**
  - [ ] 업무 만들기 모달을 시안 모양(2열 격자 + 가운데 세로선 · 내용 Composer 200자 · 첨부 DropZone ·
        체크리스트 · Toast)으로 옮긴다.
        **구현 해석(2026-09-17)**: SPEC-003 §2가 기존 본문 계약을 보존하므로 Composer의 200자는 표시 눈금이며 입력을 잘라내는 새 상한으로 만들지 않는다. 첨부 DropZone은 범위에 유지한다. 기존 생성·자료 연결 API를 순서대로 사용하고, 생성 후 첨부 실패 시 업무를 중복 생성하지 않는 재시도 경로까지 검증한다. 이 검증 전 7-A 전체 완료로 세지 않는다. 기존 자료 쓰기는 활성 담당자에게만 열리므로 생성 모달의 첨부는 본인 업무 경로에 제공한다. 관리자 배정·요청 발송·회의 승격에서는 담당자가 상세에서 첨부한다(요청은 수락 후). 이 갈래를 요청 근거 원장으로 우회하거나 발송자에게 새 자료 쓰기 권한을 열지 않는다.
- **작업 — 7-B. 탭·칩(통합 단위 I-1·I-2)**:
  - [ ] 탭을 시안 셋으로 바꾼다 — **내 업무 / 보낸 업무 / 완료 업무**.
  - [ ] **「보낸 업무」는 요청과 배정을 함께 담되 행에서 구분한다** — `origin.kind` 가
        `work_request`/`direct_assignment` 로 **이미 나온다**. 요청 행에만 수락 대기가 선다.
  - [ ] **「받은 요청」은 탭이 아니라 「내 업무」의 필터 칩**이다. 그 칩은
        `derived.assignment=awaiting_acceptance` 를 건다.
  - [ ] **「참조된 업무」·「조직 업무」를 지우지 않는다** — M-20 이 미정이므로 **화면에서 없애는 것은
        제품 결정**이다. **이번 판의 기본값**: 「보낸 업무」 탭 안의 **별도 구획**으로 남기고,
        「조직 업무」는 `canReadOrganizationWork` 인 사람에게만 **네 번째 탭 없이 같은 구획**으로 둔다.
        (뒤집히면 그 구획만 옮긴다.)
  - [ ] 칩 라벨의 **건수는 그 칩이 거는 필터의 건수**다. **읽을 수 없는 것은 건수에도 넣지 않는다.**
  - [ ] **「막힘」 칩은 그리지 않는다** — 계약에 `blocked` 상태가 없다(M-6). 계약이 생기면 그때 켠다.
  - [ ] **칩 바 오른쪽 끝**: M-24 가 미정이다. **이번 판의 기본값**은 **보기 방식(목록/칸반/타임라인)을
        유지**하고 「WBS 보기」는 **두지 않는다** — 여는 화면이 시안에 없다. (뒤집히면 단추만 바꾼다.)
- **작업 — 7-C. v2 흐름의 자리(통합 단위 I-1·I-2·I-4·I-5·I-7·I-8)**:
  - [ ] **상태 매핑**: 시안 `progress` → `in_progress`, `not-started` → `open`, `done`/`cancelled` 그대로.
        **「시작」을 부를 자리가 있어야 한다**(V-13) — 상태 Select 에 「시작 전」을 넣든 「시작」 단추를
        두든 화면이 고르되, **전이를 부를 길이 있어야 한다.**
  - [ ] **상세 상단에 `[시작]` 과 `[완료]` 를 함께 낸다** — `open` 에서도 `[완료]` 가 선다
        (SPEC-001 §4 State 주석 「`open → done` 은 상세 상단의 `[완료]` 로만 간다. 행 액션에는 없다」).
        **행 액션에는 `open` 행의 다음 한 걸음(`[시작]`)만** 둔다. Phase 5 가 전이를 열어 둔 것이 전제다.
  - [ ] **수락 대기 행과 내가 맡은 행을 구분**해 그린다(`derived.assignment`).
        받은 요청 행에 **수락/거절**을 둔다.
  - [ ] **보낸 업무 표의 상태 표시를 넓힌다** — 요청 상태 여섯(`pending`·`negotiating`·`accepted`·
        `rejected`·`withdrawn`·`cancelled_by_agreement`)이 **서로 다르게 읽혀야** 한다.
        시안 배지 둘로는 자리가 없다.
  - [ ] **「다시 요청」이 어느 명령인지 정한다** — **재요청**(`supersedes_request_id` 를 실은 새 요청)과
        **독촉**(`reminders`)은 다른 것이다. **이번 판의 기본값: 재요청.**
  - [ ] **업무 상세**를 연다 — 시안에 **상세 화면 자체가 없다**(미설계).
        기존 `TaskDetailDrawer` 를 v2 로 넓힌다: **중심 업무 + 직속 하위 두 단계** ·
        하위 생성(직접 작업 / 하위 요청) · **담당 변경 대기(기존 담당 + 새 제안 둘 다)** ·
        **철회 · 취소 제안 · 동의 · 재개** · 완료 보고/보완/승인 **회차** · 취소·재요청·담당 변경 **이력**.
  - [ ] **명령 노출은 서버 봉투와 `derived.approval`로 판단한다.** 외부 `done`만으로 재개를 노출하지 않는다 — 승인 대기와 최종 완료가 같은 상태값으로 투영된다.
  - [ ] **완료 거부 시 막는 하위를 이름으로** 보여 준다(`blocking_children`).
  - [ ] **거절한 행은 「완료 업무」 탭의 취소로 간다.** 상위에서는 **「취소됨 — 요청 거절」**로 읽힌다
        (`cancel_reason=request_rejected`).
  - [ ] **완료 업무 탭**에서 `done` 과 `cancelled` 를 다르게, **요청 Task 의 승인 전 `done` 은
        「확인 대기」**로 낸다.
  - [ ] **업무 만들기 모달에 담당자 지정 자리를 둔다** — 없으면 **요청을 보낼 길이 화면에서 사라진다**(V-2).
        비었거나 본인이면 본인 업무, 다른 사람이면 요청 발송. **시안에 없어도 계약이 요구한다.**
  - [ ] **「확인받을 사람」은 승인자(`approver_id` 0..1)** 다. **요청 Task 에서는 확인자가 요청자로
        고정**되므로 그 자리는 본인·배정 업무에서만 쓴다.
  - [ ] **시작일·참조자·참고 업무·담당자 모드**를 **계약에서 지우지 않는다**. 시안에 없다는 이유로
        없애면 기능이 사라진다. **이번 판의 기본값**: 모달의 「추가 입력」 영역으로 접어 둔다.
  - [ ] **체크리스트는 하위 Task 로 바뀌지 않는다** — 둘이 각각 읽힌다.
  - [ ] **목록 정리(OQ-202)의 화면 선택** — 백엔드 계약은 정해졌다(목록에서 빠지고 로그는 남는다).
        **이번 판의 기본값: 「숨기기」** — 행을 목록에서 감추고 **「숨긴 항목 보기」 토글**로 되돌린다.
        「삭제」로 부르면 로그가 남는 사실과 어긋나고, 「보관」은 새 보관함 화면을 요구한다.
        **기존 BE 계약 안의 기술 UX 선택이므로 사용자 질문으로 올리지 않는다.**
- **작업 — 7-D. 레일**:
  - [ ] **수신함 좌 레일**: 시안의 분류 축은 「전체/업무/참고」인데 **계약의 축은 종류 칩 둘**
        (`inquiry`·`approval`·`none`)이고 **현재 코드의 축은 상태(판단 대기·조정 필요)** 다.
        **셋이 대응하지 않는다.** → **이번 판은 현재의 상태 축을 유지**하고 종류 축은 만들지 않는다.
        그 축을 세우는 것은 **새 계약**이다(후속. 이 work 가 만들지 않는다).
  - [ ] **카드 단추**: 「내 업무로」는 M-7 에 걸린다 — **사람이 누른다는 것까지가 계약**이다.
        **「답장」·「원문 확인하기」는 계약이 없다** — 이번에 만들지 않는다.
        없는 명령을 부르는 단추를 그리지 않는다.
  - [ ] **아바타·미읽음은 그리지 않는다** — 데이터가 없다(직접 grep: `avatar` 0건, 액션 항목의
        읽음 상태 0건. `notifications.read_at` 은 **다른 도메인**이다).
  - [ ] **수신 시각은 그릴 수 있다** — 판단 항목 레코드에 `created_at` 이 **이미 있다**
        (`action_center.py` 가 정렬에 쓰고 회차에 `submitted_at` 으로 낸다). 봉투에 **없을 뿐**이다.
        **봉투에 한 줄 더하는 것은 새 외부 계약**이고, SPEC §7 **M-22 가 「계약을 만들지 않는다」로
        이미 파킹했다 — 환류가 아니라 후속이다.** **이번 판에서 그리지 않는다.**
  - [ ] **캘린더 우 레일은 업무 기한만 싣는다 — 회의 일정은 이번에 싣지 않는다.**
        M-23 미정이고 **SPEC-003 §2.9·§6·§7 이 이번 인수조건에서 뺐다**
        (「다른 도메인의 데이터를 업무 캘린더로 끌어오는 일이므로 **새 계약이 필요하다**」).
        **기술 가능성은 기록으로 남긴다** — `GET /api/meetings` 가
        `MeetingRow{title, starts_at, ends_at, location, status}` 를 **이미 내므로 새 BE 계약은
        필요 없다**(직접 확인: `http.py:614` · `viewModels.ts:843`). **넣을지는 제품 결정**이고
        **후속 계약**이다. 기술적으로 가능하다는 사실을 **범위 승인으로 바꿔 읽지 않는다.**
  - [ ] **근무 시간은 그리지 않는다** — 백엔드·프론트 어디에도 그 개념이 **없다**(직접 grep 0건).
        만들면 **새 계약**이다(M-23).
  - [ ] 주/월 뷰는 시안 모양(`CalendarNav` + 요일 스트립 + 접이식 날짜 섹션 / 7×N 그리드)으로 옮긴다.
- **작업 — 7-E. 내비**:
  - [ ] **시안 내비 10항목을 그대로 만들지 않는다.** 「수신함·진행 현황·자료」는 **갈 화면이 없고
        승인이 없다**. 현재 8항목을 유지한다. **시안이 정본이라는 원칙과 부딪히는 자리이고,
        「승인이 없다」가 이긴다**(DEC-002 § 시안 반영).
- **검증**:
  - [ ] `make frontend-test` — **Node 20 에서** 돌린다.
  - [ ] `npx tsc --noEmit`(또는 `make frontend-build` 의 `tsc -b`)로 타입이 깨지지 않는다.
  - [ ] **UX-U1~UX-U15(SPEC-003 §6) 중 「데이터: 에이전트」 칸**이 응답값으로 확인된다.
  - [ ] **역검증**: **없는 API 를 부르는 단추가 하나도 없다**(답장·원문 확인하기·별표·근무 시간).
  - [ ] **역검증**: **API 가 내는데 화면이 무시하는 값이 없다** — `derived.assignment` ·
        `derived.approval` · `derived.proposal` · `blocking_children` · `cancel_reason` ·
        `origin.kind` 가 전부 어딘가에서 읽힌다.
  - [ ] **역검증**: 읽을 수 없는 하위·자료가 목록에도 **칩 건수에도** 없다.
- **완료 증거**: 미작성

---

### Phase 8 — 자동 통합 회귀와 사용자 E2E 인계

- **Status**: DONE
- **설명**: **에이전트가 하는 것과 사용자가 하는 것을 가른다.**
  **E2E 미실행을 통과라고 쓰지 않는다.**
- **작업**:
  - [x] `make verify` 를 끝까지 돌린다(`test` → `test-scale` → `test-release` → `frontend-test` →
        `frontend-assets` → `frontend-build`). **Node 20 에서 FE 구간을 돌린다.**
  - [x] `make test-postgres` 를 격리 DB 에서 돌려 **FK·유일성·잠금·경합**을 본다 —
        C1·C2 의 동시 실행이 여기서 판정된다.
  - [ ] **A1~C2 21건 전수**의 통과/실패를 표로 남긴다. **빠진 줄이 없다.**
  - [ ] **example §10 의 10단계**를 API 로 한 번 끝까지 밟고 실제 행·연결·활동 이력을 증거로 남긴다.
  - [ ] **W1 유지 회귀 7종(K-1~K-6 · K-11)** 을 별도 절로 확인한다(아래 § W1 유지 회귀).
  - [ ] **사용자 E2E 인계 문서**를 쓴다 — 시나리오·조작 순서·기대 결과·확인할 화면 자리.
        `make local-stack` 으로 띄우는 방법과 **스키마가 최신이 아니면 시작하지 않는다**는 조건을 적는다.
  - [ ] **워커는 사용자 포트·프로세스를 건드리지 않는다.** 스택 기동은 사용자 몫이다.
- **검증**:
  - [ ] **W1 유지 회귀와 v2 새 계약 검증을 가른 표**가 있다. 섞어서 「전부 통과」로 적지 않는다.
  - [ ] **자료 worker 의 3초 lease 시간 전제 테스트**가 실패하면 **제품 버그와 가른다** —
        W1 검증에서 이미 「높은 CPU 부하에서 불안정 · 병렬 4 는 완화이지 해결이 아니다」로 기록됐다.
        **skip 하거나 단언을 약화하지 않는다.** 실패 시 병렬 4 로 재실행하고 **환경 조건을 함께 적는다.**
  - [ ] **브라우저 E2E 는 실행하지 않았다**고 명시한다. 사용자 확인 전에 「화면 경로가 검증됐다」로 쓰지 않는다.
  - [ ] SQLite 계약 테스트로 PostgreSQL 을 대신했다고 쓰지 않는다(P-7).
- **완료 증거**: 미작성

---

### 구현 누락 정정 — 직접 취소 사유 (2026-09-17)

SPEC-003 §4 API·Validation 및 SPEC-001의 확정 계약에 따라 Phase 5 BE와 Phase 7 FE를 같은 통합 단위로 보완한다. 취소 권한·허용 대상은 보존한다.

- [ ] BE: 직접 취소 REST/MCP/AX의 `reason`을 필수로 받고 공백을 거부한다. 실제 입력 사유를 취소 이력에 보존하며 `blocked`의 사유 계약도 유지한다.
- [ ] FE: 직접 취소를 제공하는 상세·오늘·캘린더 등 모든 호출 경로에서 사유 입력 후 `{expected_version, reason}`을 보낸다. 입력 누락을 고정 문구로 메우지 않는다.
- [ ] 검증: 빈 사유 거부·유효 사유 저장·기존 권한·수락된 요청 직접취소 거부 및 FE 입력/오류 회귀를 확인한다. BE만 먼저 배포하여 기존 FE 취소를 막지 않고 두 변경을 함께 인수한다.

## W1 유지 회귀 — 걷어내지 않는다

v2 는 **응답 단계만** 되돌린다. 아래 **일곱(K-1~K-6 · K-11)** 은 v2 가 건드리지 않았고,
이 work 가 **그대로 보존**한다.
새로 생기는 명령(수락·거절·철회·제안·응답·재개)에는 **회차·권한 재검사·중복 effect 방지 규칙을 건다.**
**멱등 키 필수 입력은 발송·본인 업무 생성에 한정한다**(SPEC-003 §4 Validation·§5). 나머지 명령에 새 키 입력을 요구하지 않는다.

| # | 보장 | 어떻게 확인하나 |
|---|---|---|
| K-1 | **멱등 원장** — 키 필수, 유효 범위 (행위자 · 명령 종류 · 키). 같은 키·다른 내용 = 충돌, 다른 키·같은 내용 = 둘 다 생성 | 발송·본인 업무 생성의 키 누락 거부 + 재전송 1건 |
| K-2 | **영수증 전 권한 재검사** — 잃었으면 존재를 숨긴다 | 권한을 뺀 뒤 재전송 |
| K-3 | **활성 담당 최대 1** — `pending` 은 세지 않는다 | 담당 변경 대기 중 `active` 1 + `pending` 1 공존, 교체 시 중간 상태 없음 |
| K-4 | **회차 필수** — 상태·값을 바꾸는 **모든** 명령 | 새 명령 전부에 `expected_version` |
| K-5 | **AX 사람 확인** — 확인 전 effect 없음 | AX 도구의 `requires_confirmation` |
| K-6 | **출처와 actor** — 실제로 명령을 부른 사람 | 회의 승격에서 출처=회의, actor=누른 사람 |
| K-11 | **관리자 직접 배정의 조직 범위 검사** | `POST /api/tasks/assign` 회귀 |

**그리고 배정 축의 현행 둘** — ① 신규 관리자 배정은 **즉시 `active`**(O-28) ·
② 담당 없는 업무의 **첫 지정은 `pending`**(O-14). **이번에 손대지 않는다.**

## 검증 계획

**백엔드는 Makefile 타겟으로만 실행한다. `uv run pytest` 직접 호출 금지**(AGENTS.md · P-6).
`PYTEST_ADDOPTS` 로 범위를 좁히더라도 **실행은 `make test-contract` 를 통해** 한다.

| 단계 | 명령 | 언제 |
|---|---|---|
| 도메인·구조 | `make test-unit` | Phase 1·2·4·5·6 |
| 외부 계약 | `make test-contract` | Phase 2~6 |
| DB·동시성 | `make test-postgres` (격리 `POSTGRES_TEST_URL`, `DATABASE_URL` 과 **달라야 한다**) | Phase 1·3·5·8 |
| 화면 | `make frontend-test` (**Node 20**) | Phase 7 |
| 타입 | `npx tsc --noEmit` — `frontend/` 에서. `make frontend-build` 의 `tsc -b` 가 같은 일을 한다 | Phase 7 |
| 전체 | `make verify` | Phase 8 **한 번** |
| 인벤토리 | `make test-unit` 안의 `tests/architecture/test_operation_inventory.py` | Phase 6 |

**테스트 범위의 적정선** — Phase 마다 **그 Phase 가 바꾼 계약**을 돌린다.
전량(`make verify`)은 **Phase 8 에서 한 번**이다. 같은 스위트를 Phase 마다 반복하지 않는다.

**하지 않을 것**

- 기존 테스트를 **편의상 삭제·skip·단언 약화** 하지 않는다. 깨지면 **계약이 바뀐 것인지
  구현이 틀린 것인지**를 먼저 가른다.
- **문구만 확인하는 테스트를 늘리지 않는다.** 의미 있는 회귀만 더한다.
- `docs/unified-operations-inventory.json` **전체 재작성 금지** — diff 난 항목만.
- **47 / 1297 같은 과거 수치를 v2 통과 근거로 쓰지 않는다**(작업계획서 §3 마지막 줄 · P-7).

### 검증 책임의 경계

| 무엇 | 누가 |
|---|---|
| API 응답값·오류·권한·동시성·DB 제약 | **에이전트(자동)** |
| FE 단위 테스트·타입·빌드 | **에이전트(자동)** |
| **브라우저에서 눈으로 보는 것** — 배치·문구·읽히는가 | **사용자(E2E)** |
| 통합 검증·PR | **코디네이터** |

**SPEC-003 §6 UX 인수조건(이 문서에서 `UX-U1`~`UX-U15`)의 두 칸이 이 경계다.**
「데이터: 에이전트 / 표시: 사용자」로 나뉜 항목은 **데이터 칸만 자동으로 닫힌다.**

### 사용자 E2E 인계 — Phase 8 에서 넘길 것

| 시나리오 | 조작 | 기대 결과(눈으로) |
|---|---|---|
| E-1 | 보고서 만들고 그 아래 디자인을 **다른 사람에게 요청** | 보고서 하위에 「수락 대기」 행이 선다. 상대의 **내 업무에는 서지 않는다** |
| E-2 | 상대가 **수락** → **시작** | 같은 행이 담당 확정으로 바뀌고, 수락과 시작이 **다른 시각**으로 읽힌다 |
| E-3 | 상대가 **거절**(사유) | 그 행이 **「취소됨 — 요청 거절」**로 읽히고 「완료 업무」의 취소로 간다 |
| E-4 | **재요청** | 같은 상위 아래 **새 행**이 서고 이전 취소 로그가 남아 있다 |
| E-5 | 하위가 남은 채 **최종 완료** 시도 | 거부되고 **막는 하위의 이름**이 보인다 |
| E-6 | **완료 보고 → 보완 → 재보고 → 승인** | 같은 업무에서 **회차**가 쌓이고 별도 검토 업무가 생기지 않는다 |
| E-7 | **담당 변경 제안 → 거절** | 기존 담당이 그대로이고 업무가 취소되지 않는다 |
| E-8 | **담당 변경 제안 → 수락** | 담당이 바뀌고 중간에 담당 없는 구간이 보이지 않는다 |
| E-9 | 수락 후 **취소 제안 → 동의** | 동의 전에는 아무것도 안 바뀌고, 동의하면 취소된다 |
| E-10 | 완료된 상위 아래 **하위 재개** 시도 | 거부되고 **상위를 먼저 재개하라**고 읽힌다 |
| E-11 | **요청자가 하위와 연결 자료 열기** | 열린다. **수행자의 다른 업무·미연결 자료는 없는 것처럼** 보인다 |
| E-12 | 취소 항목 **목록 정리** | 목록에서 빠지고 이력에는 남는다 |

## SPEC 환류 후보 — 없다

**WORK 가 몰래 제품 정책을 확정하지 않는다.** 검수에서 셋을 다시 대조한 결과
**SPEC 으로 되돌릴 것이 남지 않았다** — 셋 다 SPEC 이 이미 답을 적었거나 후속으로 파킹된 자리다.

| 한때 후보였던 것 | 왜 환류가 아닌가 | 어디서 닫나 |
|---|---|---|
| 요청 Task 제출 직후의 표면 상태값 | SPEC-003 §4 State 가 「`completion_submitted` 는 이 계약에 없다」 · §6·§3 S-7 이 「`done` + `awaiting_review`」를 적었다. **내부 enum 유지 + 외부 투영 매핑**으로 닫힌다 | **Phase 5** 작업·검증 |
| `open → done` 전이 | SPEC-001 §4 State · SPEC-003 §4 State 가 **둘 다 그린 전이**다. 판정을 받을 열린 질문이 아니라 **구현 대상**이다 | **Phase 5** 작업·검증 · **Phase 7-C** |
| 판단 항목 봉투의 수신 시각 | SPEC §7 **M-22 가 「계약을 만들지 않는다」로 이미 파킹**했다. 환류가 아니라 **후속(M-22)** 이다. 근거만 정정한다 — 「값이 없다」가 아니라 **「계약에 싣지 않았다」** | **아래 M-22 행** |

**환류가 아닌 것 — 기술 UX 선택이라 이 work 가 닫는다**: 목록 정리의 표시 방식(숨기기) ·
「다시 요청」이 재요청이라는 것 · 칩 바 오른쪽 끝 · 「참조된 업무/조직 업무」의 자리.
**캘린더의 회의 일정은 여기 없다** — 기술 가능성과 범위 승인은 다른 축이고, SPEC 이 **이번 범위에서 뺐다**
(§2.9·§6·§7 M-23). 넣으려면 **새 계약**이다.

## 미설계·미정의 화면 처분 — 「후행」 한 마디로 숨기지 않는다

| # | 시안이 요구 | 계약 | 이번 판 | 의존 |
|---|---|---|---|---|
| M-20 | 3탭에 「받은 요청」·「참조된 업무」·「조직 업무」 | 셋 다 **계약에 있다** | 받은 요청 = **내 업무의 칩** · 나머지 둘 = **보낸 업무 탭의 구획** | 없음. 제품 결정이 오면 자리만 옮긴다 |
| M-21 | 별표 | **필드도 저장 경로도 없다**(직접 grep 0건) | **그리지 않는다** | 새 계약 필요 |
| M-22 | 수신함 카드 아바타·수신 시각·출처·미읽음 | **아바타·미읽음 = 데이터 없음** · **수신 시각 = 데이터는 있고 계약에 싣지 않았다**(`DecisionItemRecord.created_at`·`ActionItemRecord.created_at` 이 정렬에 쓰이고 회차가 `submitted_at` 으로 낸다. **봉투 `ActionItemEnvelope` 에 없을 뿐**) · **출처(메일/메신저) = 개념도 데이터도 없음** — 메일·메신저 통합이 **승인 밖** | **넷 다 그리지 않는다.** 부재의 종류를 가른 것이 위 칸이다 | **환류가 아니라 후속 M-22** — 봉투에 한 줄 싣는 것은 새 외부 계약이고 SPEC 이 파킹했다 |
| M-23 | 근무 시간 · 캘린더의 회의 일정 | **둘 다 「계약을 만들지 않는다」**(§2.9·§6·§7) · 회의 일정은 **BE 계약이 필요 없다는 사실만** 확인됨(`GET /api/meetings` 실재) | **둘 다 안 그린다.** 회의 일정은 **「BE 계약 불필요」만 기록**하고 싣는 것은 **후속 계약** | 새 계약 필요(제품 결정) |
| M-24 | 「WBS 보기」 자리 | 두 단계 표시는 **정책**, 그 단추의 **자리만** 미정 | 보기 방식 유지, WBS 단추 **없음** | 여는 화면이 시안에 없다 |
| 수신함 분류 축 | 「전체/업무/참고」 | 계약 축은 **종류 칩 둘**, 코드 축은 **상태** — **대응하지 않는다** | **현재 상태 축 유지** | 새 계약 필요(이 work 가 만들지 않는다) |
| 「답장」·「원문 확인하기」 | 카드 단추 둘 | **계약이 없다** | **그리지 않는다** — 없는 명령을 부르는 단추를 만들지 않는다 | 새 계약 필요 |
| 내비 3항목 | 수신함·진행 현황·자료 | **승인이 없다** | **만들지 않는다** | 별도 발주 |

## 인수조건 추적 — 어느 Phase 가 어느 줄을 닫나

**SPEC-003 §6 의 인수 시나리오 21건 전수.** 빠진 줄이 없다.
「닫는 Phase」가 구현이고, **판정은 전부 Phase 8 에서 한 번 더 전수로** 확인한다.

| ID | 시나리오 | 닫는 Phase | 확인 방법 |
|---|---|---|---|
| A1 | 보고서와 내용 작성 하위 생성 | **4** | `make test-contract` — 담당·상위 관계, 생성과 시작 구분 |
| A2 | 보고서에서 디자인 요청 발송 | **2** | Task 즉시 생성 · `parent` = 보고서 · 활성 담당 없음 |
| A3 | 수락 후 시작 | **2** | 같은 `task_id` · 수락 시각과 시작 시각이 각각 |
| A4 | 디자이너의 조사·시안 + 타인 요청 | **4** | 중심 업무 재분해 허용 · `WORK_DIRECT_NESTING` |
| A5 | 요청자가 상세와 연결 자료 조회 | **4** | 하위·자료 허용 · 무관 자료 `WORK_NOT_FOUND` |
| A6 | 완료 보고 후 보완·재보고 | **5** | 같은 Task 의 회차 · 별도 검토 Task 0건 |
| A7 | 미완료 하위가 있는데 최종 완료 시도 | **5** | 본인·배정은 `complete` 에서, 요청 Task 는 **승인**에서 차단 |
| A8 | 승인 전 상위 완료 시도 | **5** | 상위 완료 차단(완결 판정이 승인까지 본다) |
| A9 | 하위 전부 완료 후 상위 완료 | **5** | 직접 완료 성공 · 자동 완료 없음. **`open`·`in_progress` 두 경로를 각각** 돌린다 |
| B1 | 거절 후 재요청 | **2** | 기존 Task `cancelled`·로그 유지 · 새 요청·Task |
| B2 | 취소된 A 와 완료된 B 공존 | **5** | A 가 상위 완료를 막지 않는다 |
| B3 | 담당 변경 제안 후 거절 | **3** | A 책임 유지 · Task 취소 안 됨 |
| B4 | 담당 변경 제안 후 수락 | **3** | 원자적 교체 · 활성 담당 최대 1 |
| B5 | 수락 전 철회 | **2** | Task 취소 · 로그 유지 |
| B6 | 수락 후 취소 제안과 동의 | **5** | 동의 전 기존 상태 · 동의 후 취소 |
| B7 | 무응답·기한 초과 | **5** | 지연 표시만 · 상태·담당·기한 그대로 |
| B8 | 완료된 상위 아래 하위 재개 | **5** | `WORK_REOPEN_PARENT_DONE` · 상위 재개 후 가능 |
| B9 | 수락 후 조건 변경 | **5** | 동의 전 기존 조건 · 동의 후 변경 |
| B10 | 취소 항목 목록 정리 | **5**(BE) · **7**(화면) | 목록에서 빠지고 로그 유지 |
| C1 | 발송·수락·승인 재시도 | **2**(발송) · **3**(담당) · **5**(승인) | 중복 생성 0 · 영수증 전 권한 재검사 |
| C2 | 동시 실행 셋 | **3**·**5** 구현 · **8** 판정 | `make test-postgres` — 모순 상태·책임 공백·잘못된 상위 완료 없음 |

**UX 인수조건 — SPEC-003 §6 의 U-1~U-15** — §6 이 각 줄의 확인 주체를 이미 갈랐다.

> **라벨 주의 — 이 문서 안에 U 번호 체계가 둘이다.** SPEC-003 §6 의 UX 인수조건 U-1~U-15 와
> BASE-002 의 미확인 항목 U-1~U-7 은 **다른 목록인데 글자가 같다**(예: SPEC 의 U-5 = 완료 업무 표시 /
> BASE 의 U-5 = 자료 표면 전수). **SPEC 의 번호를 고치지 않는다** — 대신 **이 work 안에서 가리킬 때만**
> `UX-U1`~`UX-U15`(SPEC-003 §6)와 `BASE U-1`~`BASE U-7`(BASE-002)로 **접두를 붙여 참조한다.**
> 「U-5 전수」처럼 접두 없이 쓰지 않는다.

| ID (SPEC-003 §6 의 U-*) | 닫는 Phase | 에이전트(데이터) | 사용자(표시·자리) |
|---|---|---|---|
| UX-U1 수락 대기/내가 맡은 행 구분 | 2·7 | `derived.assignment` | 구분되어 보이는가 |
| UX-U2 수락·거절과 거절 행의 행선지 | 2·7 | 명령·`cancel_reason` | 행이 취소로 가는가 |
| UX-U3 시작 자리와 `started_at` | 2·7 | `started_at`·`accepted_at` 각각 | 시작을 부를 자리 |
| UX-U4 보낸 업무의 대기·협의·거절 | 2·7 | 요청 상태 여섯 | 다르게 읽히는가 |
| UX-U5 완료 업무의 `done`/`cancelled`/확인 대기 | 5·7 | 상태 + `derived.approval` | 다르게 읽히는가 |
| UX-U6 두 단계 표시 | 4·7 | `children` 직속만 | 두 단계가 보이는가 |
| UX-U7 막는 하위를 이름으로 | 5·7 | 오류 본문 · `blocking_children` | 이름이 보이는가 |
| UX-U8 담당 변경 대기 | 3·7 | `assignments` 가 각각 | 둘 다 보이는가 |
| UX-U9 철회·취소 제안·동의·재개·담당 제안 응답 | 2·3·5·7 | 명령 존재 | 부를 자리 |
| UX-U10 담당자 지정이 요청 발송이 된다 | 2·7 | 두 갈래 결과 | 모달의 담당자 자리 |
| UX-U11 확인받을 사람 = 승인자 0..1 | 5·7 | 저장·요청 Task 고정 | — (데이터만) |
| UX-U12 체크리스트 ≠ 하위 Task | 4·7 | 각각 읽힌다 | — (데이터만) |
| UX-U13 유입 경로만으로 담당 안 선다 | 6·7 | 사람이 누른 뒤에만 생성 | — (데이터만) |
| UX-U14 기한 초과는 표시만 | 5·7 | 상태·담당·기한 불변 | — (데이터만) |
| UX-U15 읽을 수 없는 것은 건수에도 없다 | 4·7 | 목록·칩 건수 | — (데이터만) |

**이번 인수조건이 아닌 것** — 별표(M-21) · 수신함 카드 메타(M-22) · **근무 시간·회의 일정(M-23)** ·
「WBS 보기」 자리(M-24) · 시안 내비의 새 페이지. **계약이 없거나 승인이 없다.**
**없는 계약을 인수조건으로 세우지 않는다**(SPEC-003 §6). 위 목록은 **빠진 것이 아니라 후속 계약으로
남은 것**이고, 이 work 를 「확정 시안 전체 완료」로 읽지 않는다 — **원문 시안의 요구 중 여기 적힌 것들은
이번 판 밖이다.**

## Pre-deploy Check

- [ ] **배포 직전 실제 데이터 DB에서 BASE U-1·U-2·U-6 및 인덱스 실재를 다시 확인한다.** Phase 0의 빈 DB·0행 조회는 이 조건의 통과 근거가 아니다. U-6 예외가 0건이거나, 0건이 아니면 사용자 결정을 받았다.
- [ ] 실행 DB 의 `uq_tasks_source_work_request` 인덱스가 **실재한다**(없으면 만들었다).
- [ ] 추가한 컬럼이 **전부 nullable** 이고 **이번에 더한 컬럼·표가 `--sync` 의 `manual` 에 없다.**
- [ ] 기존 표의 인덱스는 **`backend/migrations/manual/2026-09-17-w2-indexes.concurrent.sql` 이
      운영에 적용됐고 `pg_indexes` 로 확인**됐다(사람이 실행 · 트랜잭션 밖).
      **INVALID 로 남은 인덱스가 0건**이다.
- [ ] **기존 서비스 영향 없음** — 관리자 배정·첫 지정·배정 철회·
      기한 두 값·AX 확인이 그대로 돈다.
- [ ] credential·env 를 새로 노출하지 않는다 (**이번에 추가한 외부 의존이 없다**).
- [ ] 응답에 **읽을 수 없는 하위·자료의 이름이나 건수**가 새지 않는다.
- [ ] **운영·사용자 DB 초기화가 절차에 없다.**
- [ ] 코드 배포 전에 **스키마 추가가 먼저** 끝났다(Rollout ②③ → ④⑤).

## Rollback

- **코드 롤백** — 배포 단위를 ④(읽기)와 ⑤(쓰기·새 규칙)로 갈라 두었으므로 ⑤만 되돌릴 수 있다.
- **인덱스** — `DROP INDEX CONCURRENTLY`(트랜잭션 밖). 데이터 영향 없음.
  **실패로 남은 INVALID 인덱스**(`pg_index.indisvalid = false`)도 같은 명령으로 지우고 다시 만든다.
- **컬럼·표** — **되돌리지 않는 것이 기본이다.** nullable 이라 옛 코드가 무시하고,
  지우면 ⑤ 구간에 쌓인 수락 시각·취소 사유·제안 행이 사라진다.
- **부분 revert 의 영향 범위** — ⑤ 를 되돌리면 그 사이 **수락 대기로 선 요청 Task** 가
  옛 코드에서 **활성 담당 없는 Task** 로 보인다. 목록에 서지 않고 담당자가 시작할 수 없다.
  **잘못된 상태가 아니라 새 사실**이고, 되살리려면 그 행들의 담당을 **사람이 수락**하게 한다 —
  **일괄 `active` 전환을 하지 않는다**(P-8 의 반대 방향도 같은 금지다).

## Done Criteria

- [x] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [x] **SPEC-003 §6 인수조건 전항**이 「데이터: 에이전트」 칸까지 자동검증으로 확인됐다.
- [x] **A1~C2 21건 전수**와 **example §10 의 10단계**가 통과/미통과로 **각각** 기록됐다.
- [x] **W1 유지 회귀 7종(K-1~K-6·K-11) + 배정 축 현행 둘**이 통과했다.
- [x] `make verify` 와 `make test-postgres` 가 **수치와 로그**로 남았다.
- [ ] **브라우저 E2E 는 사용자가 수행**했고 그 결과가 기록됐다. 현재는 **미실행**이며 사용자 확인으로 이관했다.
- [ ] **SPEC 환류 후보가 0건**임이 유지됐다 — 구현 중에 새 외부 계약이 필요해지면
      **몰래 넣지 않고** SPEC 환류로 올렸다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **OQ-203**(제출도 막을 것인가) — **답 대기.** 제출을 여는 것은 **현행 보존**이지 새 선택의 확정이 아니다.
  **답 전에 정책 확정으로 표시하지 않는다.** 뒤집히면 **Phase 5 의 작업 한 줄 + §6 인수조건 한 줄**만 바뀐다
  (조건별 검증 계획은 Phase 5 에 있다).
- **OQ-206**(승격 요청의 완료 확인자) — **그 조각은 구현 대상이 아니다.** 답이 오면 Phase 5 에 한 조각을 연다.
  **미답으로 남는 경로를 숨기지 않는다**: 승격 요청 Task 의 **완료 승인 경로는 이 판에서 미검증**이고,
  seed·E2E 에서 그 Task 가 완결 판정 대상이 되면 **승인을 부를 사람이 정해지지 않아 상위 완료가 막힌다.**
  **그것은 미답의 결과이지 제품 버그가 아니다** — seed 에서 승격 경로를 **빼서 감추지 않는다**(Phase 6).
- **SPEC 환류 후보는 없다** — 제출 직후 표면값과 `open → done` 은 **SPEC 이 이미 답을 적었으므로
  Phase 5 가 구현한다**. **「완결 판정이 두 state 값을 다 읽게 쓴다」로 흡수하지 않는다**(제출·미승인이
  완결로 새어 V-15 를 깬다) · **「A9 를 `in_progress` 로 거쳐 가게 쓴다」로 우회하지 않는다**(계약 위반을
  초록으로 덮는다). 판정은 **승인 판단 행**, 경로는 **`open`·`in_progress` 각각**이다.
- **BASE U-1 실행 스키마 미확인** — Phase 0 에서 닫는다. **ORM = 실행 DB 를 전제한 설계는 인덱스·FK 에서 깨진다.**
- **자료 worker 3초 lease** — 시간 전제 부채다. **제품 버그와 가른다.** 영구 해결은 이 work 밖이다.
- **`blocked`·`completion_submitted` enum** — 이 work 는 **읽기만** 한다. 정리는 후속이다.

## Automated Completion Evidence

- 최종 `make verify`: Node 20.20.0, `PYTEST_XDIST_AUTO_NUM_WORKERS=1`, exit 0. 로그: `orchestration/work/strong-hajin-work/v2-final-verification/make-verify-node20.log`.
- 백엔드 본체 1338 passed, scale 13 passed, release 1 passed. FE 53 files / 713 tests passed, assets와 build exit 0.
- 격리 PostgreSQL `make test-postgres`: 77 passed, 0 failed, 0 skipped, exit 0. 로그: `v2-postgres-verification/final-full-03.*`.
- 신규 v2 계약 테스트 33건과 example §10·K 회귀는 `v2-contract-tests-report.md` 및 최종 백엔드 실행에 포함됐다.
- 최초 기본 Node 25 실행에서 FE jsdom localStorage 오류가 난 기록은 검증 증거로 사용하지 않았다. 저장소가 요구하는 Node 20 환경에서 재실행해 통과했다.

## Related

- SPEC: (frontmatter `links.specs` 참조)
- Work: (frontmatter `links.works` 참조)
- 원문: `reference/2026-09-10-sc-meeting/` 의 정의·생명주기·작업계획서 v2 와 `example.md`
- 확정 시안: 코드 레포 `.design-sync/screens/` (정본) · `design-change-2026-09-17/` 분석 3종(보고서)
