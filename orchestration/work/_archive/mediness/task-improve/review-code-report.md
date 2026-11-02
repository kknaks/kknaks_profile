# 리뷰 리포트 — WP-129 업무 요청 축 + 지시 입구 차단 / code (BE+FE) (2026-09-01)

## 판정: **WARN**

**계약 위반(FAIL 사유) 0건.** 브리프 §2 의 계약 항목 8개(게이트 재도입·판정 술어 한 곳·migration 인덱스 1건·자동 cc 0·DM graceful·입구 차단 주석 수준·FE 금지선·allowed_paths)가 **전부 코드로 확인**됐다.
다만 **정합·품질 WARN 7건**이 남고, 그중 **W1(계층 방향 역전)** 과 **W2(은퇴 어휘 3벌 · 「재활성 한 줄」 주장 부정확)** 는 코디네이터가 재발주 여부를 판단할 만한 무게다.

---

## 검수 범위

- base `origin/dev` — **`git diff origin/dev...HEAD` 는 비어 있다**(커밋 0). 실검수 대상 = **워킹트리 전량**:
  - modified 38파일 (`back/` 33 · `front/` 5)
  - untracked 6파일 (`back/alembic/versions/0137_*` · `back/app/services/action_runtime/tasks/request_axis.py` · 신규 테스트 4)
  - 합계 **44파일 / +1013 −152**
- 실행한 검사: `git diff` 전문 정독 · `git status --porcelain` · 위치 기반 grep(판정 술어 중복 · `register_decision` 호출부 전수 · `RETIRED_*` 상수 소비처 · `repositories/`→`services/` import · leaf · alembic 체인) · SSOT 대조(WP-129 · SPEC-154 §4.8 · SPEC-155 §6.1 · SPEC-111/115/156)
- **테스트 미실행**(reviewer tools.md 금지). 워커가 보고한 수치는 검증하지 않았고, 대신 **테스트 코드의 내용**을 읽어 계약을 고정하는지 판정했다.

---

## 위반 (FAIL 사유)

**없음.**

---

## 계약 항목별 판정 근거 (브리프 §2 1~8)

### ① 게이트 재도입 0 — **PASS**
- diff 추가줄 전량에 `accept_pending` · `task_accepted` · `task_declined` · `accepted_at` 이 **0건**(`git diff -U0 | grep '^+'`).
- `back/app/models/action_runtime.py` diff 는 **`Index(...)` 한 블록뿐**(:683–692) — 상태 enum·TaskEvent 어휘 무변경.
- `request_axis.py:20–24` 모듈 docstring 이 「게이트가 없다 / 거부 동선은 재배정 요청」을 명시.

### ② 판정 술어 한 곳 — **PASS**
- 정본 = `back/app/services/action_runtime/tasks/request_axis.py:55 is_request_task` + `:79 request_predicate`(SQL 짝, **같은 모듈·같은 docstring**).
- 소비처 전수: `manual_surface.py:599`(상세) · `manual_surface.py:1090`(목록 행) · `projection.py:295`(표시명) · `runtime_task_repo.py:363`(조회) — **전부 술어를 호출**하고 조건을 인라인하지 않는다.
- grep: `created_by_member_id != ` 은 **`request_axis.py:91` 한 줄뿐**(app/ 전역).
- FE 는 판정을 재유도하지 않는다 — `front/lib/tasks/canonical-task.ts:367 is_request: t.is_request === true`(fail-closed) · `front/components/tasks/detail/TaskMetaPanel.tsx:288 {task.is_request && ...}`. `assignee_id`/`task_type` 조합 재조립 **0**.

### ③ migration = 인덱스 1건뿐 — **PASS**
- `back/alembic/versions/0137_tasks_created_by_index.py:55` — 함수 본문이 `op.create_index` **한 호출**. `add_column`·`create_table`·`alter` 0.
- 체인 선형: `0137.down_revision = "0136_task_status_5v"`, 같은 down_revision 을 쓰는 다른 파일 없음(head 분기 0).
- 테스트가 총계를 센다 — `back/tests/migrations/test_0137_tasks_created_by_index.py:79–81`(인덱스 델타 == {1개} · 컬럼 집합 불변 · 테이블 집합 불변).

### ④ 자동 cc 0 — **PASS**
- `manual_surface.py:209 cc_member_ids=req.cc` — 요청자 주입 없음. `factory.create_task_with_cc` 는 호출부가 준 목록만 쓴다(`factory.py:159`).
- 채팅 발도 같다 — `task_draft/definitions.py:78–81` 이 `create_task_in_txn(member=creator, ...)` 만 바꾸고 cc 축을 건드리지 않는다.
- `back/tests/api/test_wp129_task_request_axis.py:283 test_request_does_not_auto_add_the_requester_to_cc`.

### ⑤ DM graceful · spec-119 재사용(신설 0) — **PASS**
- `request_axis.py:180 notify_task_requested` → `workflow/decision/notify.send_dm`(:162) + `decision/surface.notifier()`(:971) **기존 인프라 그대로**. 새 클라이언트·새 발송 원장·새 알림 종 **0**.
- graceful 2겹: 요청자 이름 해소 실패도(`:190–195`), 발송 실패도(`:204–206`) `logger.warning` 후 `[]` 반환. 호출부(`manual_surface.py:249`)는 **commit 이후**에 부르고 반환값을 판정에 쓰지 않는다.
- fail-loud 혼입 없음 — `incident/surface.py` diff 는 `requested_by_me` **패스스루 한 인자**뿐(:234·:247).

### ⑥ 입구 차단 = 주석/상수 수준 — **PASS**(단 W2 참조)
- 강제 지점 **한 곳**: `workflow/decision/surface.py:239 if flow_type in C.RETIRED_FLOW_TYPES: raise wf.err_retired_flow_type()`.
- `register_decision` 호출부 전수 = `routers/decisions.py:231`(REST·웹 모달·MCP 공용) · `routers/slack.py:671`(슬랙 폼) · `services/version_wbs.py:1753`(WBS 발) · `decision_draft/definitions.py:121`(채팅 승인 실행) — **네 곳 모두 그 한 문을 지난다**. 표면별 가드 누락 구멍 없음.
- **삭제 0**: `FLOW_TYPES` 3종 유지(`decision/const.py:118`) · `FLOW_LABELS["instruction"]` 유지(:249) · `FLOW_FIELD_SETS["instruction"]` 유지 · `accept_instruction` 함수 유지 · leaf `decision.execution_task.read` 유지(`policies/decision.py:70`) · `POST /decisions/{id}/execution-tasks` 유지.
- **부트스트랩 축**: 끈 것은 `surface.py:293 if not deduped and flow_type == FLOW_INSTRUCTION: accept_instruction(...)` **한 줄의 도달 가능성**뿐. `open_round_bootstrap`(결정 승인 발 · [후속 실행] 발)은 **diff 에 없다** — 유지 축 보존.
- 기존 run 회귀를 테스트가 고정 — `test_wp129_instruction_entrance_closed.py:202 test_existing_instruction_run_keeps_running`(라우팅·자동 승인 DONE·부트스트랩 태스크 존재까지 단언).

### ⑦ FE 금지선 — **PASS**
- `front/` diff 4파일: `components/tasks/detail/TaskMetaPanel.tsx`(메타 「담당·조직」 그룹 한 곳 +18줄) · `lib/tasks/canonical-task.ts`(타입·매퍼 additive) · 테스트 2.
- **목록·칸반 diff 0** — `front/app/(authenticated)/ax/tasks/*` · 카드 컴포넌트 무변경.
- **본문 존 diff 0** — `TaskMetaPanel.tsx` 변경은 `②담당·조직` 섹션(`:230–290`) 안에만 있고 6블록 본문 컴포넌트는 손대지 않았다.
- **CTA 코드 diff 0** — 요청자 상태 칩 미노출을 **서버 `allowed_transitions=['canceled']` 소비**로 달성. 헤더/CTA 컴포넌트 파일 무변경, 새 FE 분기 0.

### ⑧ allowed_paths — **PASS**
- BE diff = `back/` **전량**. `mcp/` 파일 **0건**(MCP `task_draft_request` 스키마 diff 0 — 테스트 `test_wp129_chat_assignee.py:246` 가 고정).
- FE diff = `front/` 전량.
- `back/`·`front/` 밖 파일 **0건**. 문서 레포 무변경.

---

## 정합·품질 판정 (브리프 §2 9~13)

### ⑨ 채팅 담당자 해소 ↔ SPEC-155 §6.1 — **일치**
| SPEC-155 §6.1 「담당자」 행 | 코드 |
|---|---|
| 발화 명시 시 그 사람 | `task_draft/provider.py:202–214`(완전 일치 → 접미사 일치) |
| 명시 없으면 요청자 본인 | `provider.py:186–189` |
| 해소 범위 = 같은 조직 활성 구성원 | `provider.py:196`(`list_active_members_with_primary_unit` — **배정 picker 와 같은 쿼리**) |
| tenant 미상 = 아무도 해소 안 함 | `provider.py:191` fail-closed |
| 동명이인·불일치 → **미해소 + 사유**, 요청자로 눕히지 않음 | `provider.py:210·212` + 카드 표기 `workflow.py:362 _assignee_fact` + 실행 거절 `definitions.py:136` |
| 승인 실행이 재검증(이중 그물) | `definitions.py:97–103 get_active_member` |
| 부서 = **담당자** 소속 파생 | `workflow.py:471 _primary_org_unit(session, content.get("assignee_member_id"))` — 요청자가 아니다 |
| fallback 에서도 담당자 채움(미해소면 요청자) | `provider.py:318 "assignee_name": ""` → 요청자로 떨어짐 |
- 3케이스 테스트 존재 — `test_wp129_chat_assignee.py:40·58·75`(+ 모호 `:93` · 비활성 `:111` · tenant 미상 `:130`).
- ⚠ **표기 불일치 1건은 SPEC 쪽 문제** → W4.

### ⑩ `scope=requested` — **PASS**
- 신규 endpoint **0**: `routers/action_runtime_v2.py:414 list_my_tasks_ep` 의 `scope` 패턴을 `_TASK_SCOPE_PATTERN`(:252)으로 넓힌 것이 전부. 신규 leaf 0.
- `read_all` 미요구 — `:435–439` 가 요청 축일 때 `_resolve_scope`(자격 판정)를 **아예 지나지 않고** `AppliedScope(requested/applied='requested', degraded=False)` 를 직접 만든다. 본인 축이라 강등 대상이 없다.
- `actor_override` 와 배타 — `:441` `(not requested_axis) and applied.applied == _SCOPE_ALL` + `tasks_surface.py:898` 가 요청 축을 먼저 본다(fail-closed 방향).
- 응답 shape 불변 — 모집단만 `list_requested_by`(`runtime_task_repo.py:339`)로 갈리고 정렬·행 조립은 같은 코드.

### ⑪ 6번째 입구(버전 WBS 태스크 발) — **계약 위반 아님. WP 환류 대상.**
- 실체 = `back/app/services/version_wbs.py:1730 register_decision_from_wbs_task` → `:1753 register_decision`. **같은 seam** 이라 별도 코드 없이 함께 닫혔다.
- **프로덕션 호출자 0** — grep 결과 호출부는 `tests/api/test_wp104_w6_task_surface.py:638` **테스트 하나뿐**이고, 함수 docstring 자체가 「사용자-facing WBS 제출 endpoint 는 W6 에서 제거됐고 시스템 내부 등록 경로만 남는다」로 적고 있다.
- 즉 **지시 흐름 발 「휴면 seam」** 이고, 닫힘은 「어느 경로로도 새 `instruction` run 이 서지 않는다」는 P5 검증 항목과 **정합**한다. 유지 축(결정 승인 발·[후속 실행] 발 부트스트랩)과 무관.
- 워커가 테스트의 흐름 예시를 `FLOW_INSTRUCTION` → `FLOW_REQUEST` 로 바꿨다(`test_wp104_w6_task_surface.py:644`) — 그 테스트의 대상은 「공용 seam 을 지나는가」라 대상 계약은 보존된다.
- **환류 필요**: WP-129 P0 「지시 흐름 입구 전수 목록」에 이 자리를 추가(휴면·호출자 0 명시).

### ⑫ 테스트가 계약을 고정하나 — **대체로 예**
- **재활성 증명**: `test_wp129_instruction_entrance_closed.py:32 reopen_instruction()` 이 `C.RETIRED_FLOW_TYPES = frozenset()` 한 줄로 등록을 되열고, `:202 test_existing_instruction_run_keeps_running` 이 그 상태에서 실제로 run 이 서는 것을 확인한다 — **런타임 재활성이 동작함을 증명**. (다만 그 「한 줄」이 등록 seam 한정 → W2.)
- **금지선 테스트**: `:249`(저장 값·어휘·라벨 보존) · `:261`(정의·라우팅·자동 승인·검토 방향 미삭제, `inspect.getsource` 로 확인) · `:282`(leaf 미회수) · `:289`(`/decisions/me/tasks` 등록 해제 + 핸들러 생존) · `:302`(`execution-tasks` 계약 보존).
- **요청자 취소 축**: `test_wp129_task_request_axis.py:190`(취소 허용 · 그 밖 전이 거절) · `:215`(담당자 전이표 불변) · `:236`(terminal 은 열지 않음) · `:260`(수정 자격은 기존 축) · `:283`(cc 0) · `:306`(DM 폭발해도 태스크 생성) · `:334`(본인 태스크는 발송 0) · `:353`(본문 = 요청자·제목·딥링크 1).
- **기존 테스트를 삭제하지 않고 이관**: `test_decision_register.py` 는 지시 시나리오를 지우는 대신 `reopen_instruction()` 로 「이미 선 run」을 재현하고 **닫힘 단언을 같은 자리에 추가**(:277–282). `test_decision_form.py` 는 삭제한 `test_modal_dynamic_labels_instruction` 을 **라벨 표 보존 단언**(`:402–405 FIELD_LABELS_BY_FLOW[...]["instruction"]`)으로 대체 — 커버리지 손실 없음.
- ⚠ 술어 중복 grep 테스트는 **리터럴 문자열 의존** → W7.

### ⑬ 기존 실패 2건(워커 주장: 선행 실패) — **diff 무관 판정(코드 근거)**
- `tests/services/test_decision_legacy_migrate.py` 2건 — 원인 `Runner._run_signal() missing 'origin'`. `app/services/action_runtime/engine/runner.py` 는 **이번 diff 에 없다**(`:196` 시그니처 기존). 그 테스트 파일도 미수정. → **무관**.
- `tests/api/test_wp113_decision_draft_after_approval.py::TestLatestExecutionResult` 2건 — 원인 `actions.subject_id` NOT NULL(픽스처 축). 그 파일은 **미수정**이고(수정된 것은 동명 유사 파일 `test_wp113_decision_draft.py`), 파일 안에 `instruction` 사용이 **0건**(`flow_type="request"` 만) 이라 신규 `RETIRED_FLOW_TYPES` 가드에 걸리지 않는다. → **무관**.
- ⚠ **실행으로 확인하지 않았다**(reviewer 테스트 실행 금지). 위는 **코드 근거 판정**이다.

---

## 경미 (WARN)

### W1. 계층 방향 역전 — repository 가 service 를 import 한다 *(가장 무거운 WARN)*
- `back/app/repositories/action_runtime/runtime_task_repo.py:357`
  `from app.services.action_runtime.tasks.request_axis import request_predicate`
- **`app/repositories/` 전체에서 유일한 `from app.services` import** 다(grep 전수 확인).
- 동시에 `request_axis.request_predicate()`(`services/.../request_axis.py:79`)는 **service 계층에서 SQLAlchemy WHERE 절을 조립**한다.
- 근거: `roles/mediness/backend/rules.md`(reviewer `rules.md` backend 절 인용) — 「계층 = routers/ → services/ → repositories/ → models/」 · 「쿼리는 `repositories/` 에만. Service 에서 raw 쿼리 조립이 나오면 위반」.
- ⚠ 「판정 술어 한 곳」 계약과 **충돌하지 않는다** — 술어를 `repositories/action_runtime/`(또는 `models/` 인접 공용 자리)에 두고 `request_axis` 가 **아래로** import 하면 한 곳 유지 + 계층 정방향이 동시에 성립한다.
- 권장 수정: `request_predicate` 를 `repositories/action_runtime/` 로 옮기고, service 는 그것을 import(방향 역전 해소 · 함수 본문 무변경). 순환 회피용 함수 내부 지연 import(:357)도 함께 사라진다.

### W2. 은퇴 어휘가 **3벌** — 「재활성 = 한 줄」은 등록 seam 한정
- 세 자리가 **서로 독립된 상수**로 은퇴를 표현한다:
  - `back/app/services/action_runtime/workflow/decision/const.py:135 RETIRED_FLOW_TYPES`(강제)
  - `back/app/services/decision_form.py:125 RETIRED_FLOW_VALUES`(슬랙 폼 select)
  - `back/app/services/decision_gate.py:526 _FLOW_FORM_VALUES`(AI gate — `INSTRUCTION` 을 **줄 삭제**로 뺐다)
- 따라서 `RETIRED_FLOW_TYPES` 만 비우면 **등록은 열리지만 폼 옵션과 gate 추천은 계속 닫혀 있다.** 워커 리포트의 「재활성 = 그 frozenset 을 비우는 한 줄」과 `test_reactivation_is_one_line` 의 이름은 **범위를 과장**한다(테스트 본문은 상수 존재만 단언하므로 거짓 단언은 아니다).
- 더해 `const.py:139 REGISTRABLE_FLOW_TYPES` 는 **프로덕션 소비처 0** 이다(grep — 유일한 참조가 `test_wp129_instruction_entrance_closed.py:258`). 그런데 `const.py:138` 주석은 「폼 select 옵션·AI gate 산출·채팅 intake 산출이 **전부 이 목록에서 나온다**(어휘가 세 벌이 되지 않게)」로 적혀 있어 **코드 사실과 반대**다.
- 근거: reviewer `rules.md` 「재사용 — 있는 것을 놔두고 같은 기능을 재구현하지 않았나」 + WP-129 P5 「비활성 자리에 **재활성 방법을 아는 주석**을 남긴다」(각 자리에 🔁 주석은 있으므로 P5 작업 항목 자체는 충족).
- 권장 수정: ⓐ `const.py:138` 주석을 사실에 맞게 정정하거나, ⓑ `decision_form` / `decision_gate` 가 `REGISTRABLE_FLOW_TYPES`(또는 `RETIRED_FLOW_TYPES`)를 **실제로 소비**하게 해 어휘를 한 벌로 접는다. ⓑ 를 택하면 「재활성 한 줄」이 사실이 된다.

### W3. 채팅 승인 경로의 DM 이 **pre-commit** 이다 *(워커 자진 신고 — 확인됨)*
- `task_draft/definitions.py:87 await notify_task_requested(ctx.session, task, ...)` 가 `complete_execution` 직후에 있고, 커널은 실행 핸들러 **뒤**에 커밋한다. REST 경로(`manual_surface.py:249`)는 `db.commit()` **이후**라 두 경로의 발화 시점이 갈린다.
- 실패 방향이 「DM 은 갔는데 태스크가 없다」로 기운다. graceful 이라 태스크 생성을 막지는 않는다.
- 근거: SPEC-154 §4.8 「DM 은 보조」 — 계약 위반은 아니나 **두 표면의 순서가 다르다**는 것이 정합 흠이다.
- 권장: 이번 라운드 밖으로 두더라도 **OQ 로 기록**(워커 리포트 §미결 3 과 같은 내용).

### W4. SPEC-155 §6.1 「산출 필드」 표기와 구현 필드명이 다르다 — **SPEC 환류 대상**
- SPEC-155 §6.1 산출 필드 행: `**assignee_member_id**(옵셔널·발화 명시 시 — 2026-09-01)`
- 구현: 모델 산출은 **`assignee_name`**(`provider.py:246`)이고 id 해소는 서버(`resolve_assignee`)가 한다.
- 같은 절의 「담당자」 행·「지어낼 자리를 만들지 않는다」 행은 **이름 해소**를 서술하므로 **SPEC 내부가 서로 어긋나 있고**, 구현은 서술부(의도)를 따랐다 — 이 판단이 옳다(모델에게 id 를 내게 하면 지어내기 금지가 무너진다).
- 근거: WP-129 「구현 중 어긋나는 사실이 나오면 코드를 고치지 말고 SPEC 으로 되돌린다」.
- 권장: SPEC-155 §6.1 산출 필드 표기를 `assignee_name`(이름·서버 해소)으로 정정.

### W5. P0 실측 3건이 비어 있다 — Pre-deploy 이월
- 미측정: ① `created_by_member_id` 빈 행 수 ② `slack_id` 미매핑 비율(OI-4 백필 판단 근거) ③ 살아 있는 `instruction` run 건수.
- 사유(워커): 이 머신에서 도달 가능한 dev/prod DB 없음. **코드는 그 행을 안전하게 다룬다**(`request_axis.py:69–72` 두 값 NOT NULL 요구 · 마이그레이션 테스트 `:112` 가 nullable 을 고정).
- 권장: WP-129 §Pre-deploy Check 에 미측정 3건을 **명시적 blocker 로 남긴다**(「완료 증거: 미작성」인 채 P0 을 DONE 으로 올리지 않는다).

### W6. `EXPLAIN` 미확인 — 인덱스 실효성 미검증
- WP-129 P1 검증 3번(「`EXPLAIN` 으로 요청자 필터 조회가 새 인덱스를 타는지」)이 **미수행**. 대신 구조 일치(선행 컬럼 `organization_id, created_by_member_id` + 부분 조건 `deleted_at IS NULL`)를 테스트로 고정했다(`test_0137_*.py:63–65`).
- 조회는 `_scoped()` 에 `deleted_at IS NULL` 이 항상 붙고(`runtime_task_repo.py:361`) 선행 컬럼이 `organization_id` 라 **정의상 정합**하나, planner 선택은 데이터 있는 환경에서 확인이 필요.

### W7. 술어 중복 grep 테스트가 리터럴 의존이라 취약
- `back/tests/api/test_wp129_task_request_axis.py:83` 는 `grep -rln "created_by_member_id != "` 결과 파일이 `request_axis.py` 하나임을 단언한다.
- 공백·줄바꿈·`!=` 대신 `.isnot()`/`is_not` 같은 다른 표기로 조건을 복제하면 **테스트를 통과한 채 중복이 생긴다**.
- 근거: reviewer `rules.md` 「테스트 — 커버리지 수치가 아니라 존재·의미」.
- 권장(선택): 소비처가 `request_axis` 를 import 하는지(모듈 의존 기준)로 바꾸거나, 정규식을 `created_by_member_id\s*!=` 로 넓힌다. **이번 판정에 영향 없음.**

---

## 기존 부채 (이번 판정 제외)

- `app/services/decision_gate.py` 의 프롬프트가 **파이썬 모듈 상수**로 인라인돼 있다(SPEC-117 프롬프트 스토어 이관 미완) — 이번 diff 는 그 상수 안 문장만 고쳤고 구조는 기존 그대로다. SPEC-155 §6.1 이 이관을 「이번 범위 밖」으로 명시.
- `register_decision_from_wbs_task`(`version_wbs.py:1730`)가 **프로덕션 호출자 없이** 남아 있다(테스트만 호출). WP-129 §Scope 「죽은 코드 정리 → OQ-20」에 해당 — 이번 라운드가 건드릴 자리가 아니다.

---

## 확인한 것 (PASS 근거 요약 · 「확인 안 함」 포함)

| 항목 | 확인 방법 | 결과 |
|---|---|---|
| 게이트 재도입 0 | diff 추가줄 grep | ✅ 0건 |
| 판정 술어 한 곳 | grep + 소비처 4곳 대조 | ✅ `request_axis.py` 단일 |
| FE 판정 재유도 0 | `canonical-task.ts` · `TaskMetaPanel.tsx` 정독 | ✅ fail-closed 소비만 |
| migration 객체 1 | 파일 본문 + 테스트 단언 | ✅ 인덱스 1 |
| alembic 체인 | `down_revision` grep | ✅ 선형, head 분기 0 |
| 자동 cc 0 | 생성 seam 2경로 인자 대조 | ✅ |
| DM graceful · 신설 0 | `send_dm`/`notifier` 재사용 확인 | ✅ |
| 입구 = 한 seam | `register_decision` 호출부 전수(4곳) | ✅ 전부 가드 통과 |
| 삭제 0 · leaf 유지 | 상수·함수·라우트·leaf 개별 확인 | ✅ |
| 유지 축 부트스트랩 | `open_round_bootstrap` diff 부재 | ✅ 무변경 |
| FE 금지선(목록·칸반·본문·CTA) | `front/` diff 전량 정독 | ✅ 메타 존 한정 |
| allowed_paths | `git status` 전량 | ✅ `back/`·`front/` 만 |
| 배정 후보 = 같은 조직 활성 구성원 | `TaskFormFields.tsx:18 fetchAssignableMembers` → org-directory | ✅ **기존 동작으로 이미 충족**(diff 0 이 정상) |
| 채팅 해소 ↔ SPEC-155 | 조항별 대조표(위 ⑨) | ✅ 일치(W4 표기 제외) |
| `scope=requested` | 라우터·surface·repo 3층 정독 | ✅ 신규 endpoint 0 · read_all 미요구 |
| 계층 방향 | `repositories/`→`services/` import grep | ⚠ **W1** |
| 은퇴 어휘 단일성 | `RETIRED_*` 소비처 grep | ⚠ **W2** |
| 테스트 실행 결과 | — | ❌ **확인 안 함**(reviewer 금지 — 워커 수치 미검증) |
| DB 실측 3건 | — | ❌ **확인 안 함**(DB 도달 불가 — W5) |
| `EXPLAIN` | — | ❌ **확인 안 함**(W6) |

---

## 코디네이터 조치 제안

1. **재발주 없이 진행 가능**(계약 위반 0). 다만 **W1(계층 역전)** 은 한 파일 이동으로 끝나므로 PR 전에 처리 권장 — 리포에서 유일한 방향 역전이라 선례가 된다.
2. **W2** 는 ⓐ 주석 정정(1분) 만으로도 「문서가 코드보다 앞서 있다」를 해소한다.
3. **문서 환류 3건** — ⑪ 6번째 입구(WP-129 P0 목록) · W4(SPEC-155 §6.1 필드명) · W5(Pre-deploy 미측정 3건). 전부 planner 몫.
