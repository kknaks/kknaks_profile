# W1 통합 리뷰 수정 1차 — 결과 보고 (2026-09-16)

## 상태: done · 담당 지적 8건 전부 처리 · 자료 worker 실패 2건 원인 규명 완료

---

## 0. 검증 수치 (명령·exit code)

| 명령 | exit | 결과 |
|---|---|---|
| `make test-unit` | **0** | **322 passed**, 1 deselected (operation inventory 4건 포함 green) |
| `make test-contract` | **0** | **975 passed** (1차 974 + 1 failed → W-2 낡은 단언 수정 후 재실행) |
| `make reset-demo DATABASE_URL=…/ax_test_w1` | **0** | 격리 DB 스키마 갱신 |
| `make test-postgres POSTGRES_TEST_URL=…/ax_test_w1` | **0** | **65 passed**, 1311 deselected |
| `git diff --check` | 0 | clean |

`ax_demo` 무접촉. E2E 미실행(사용자 담당). 전량 `make verify` 는 코디 몫.
로그: `scratchpad/r1-unit.txt` · `r1-contract.txt`(1차) · `r1-contract2.txt` · `r1-pgreset.txt` · `r1-pg.txt`.

---

## 1. 지적별 처리

### F-1 (BE 몫) — horizontal 이 못 받는 필드의 명시 422 + 부수효과 0 테스트

- **추가**: `tests/contract/test_task_creation_contract.py::test_a_recipient_creation_refuses_each_field_it_cannot_carry_and_leaves_nothing_behind`
  — `start_date`·`parent_task_id`·`project_id` **각각**을 parametrize 해 3건.
- 각 건이 단언하는 것: **422** · detail 에 **그 필드 이름**과 「쓸 수 없는 항목」이 실림 ·
  `TaskRecord` 0건 · `TaskCreationAttemptRecord` 에 그 키 없음 · **`WorkRequestRecord` 0건**(출처 행도 안 섬) ·
  받는 사람 `my_work` 비어 있음 · **같은 값을 본인 업무로 만드는 길은 201 로 그대로 산다**.
- `project_id` 건은 지호가 만든 프로젝트에 민아를 붙여 **읽을 수 있는 프로젝트**로 세웠다 — 거절 사유가
  「읽을 수 없는 프로젝트(404)」가 아니라 **담당 지정 갈래가 받지 않는 값(422)** 임을 분리하기 위해서다.
- 계약은 브리프대로 **유지**했다: horizontal 은 여전히 세 필드를 지원하지 않고, self/managed 지원은 그대로다.
  FE 쪽 수정은 FE 워커 몫(사용자 회신으로 완료 확인).

### W-1 — AX 확정 실행이 horizontal 에서 `source_*` 계보를 버리던 것 → 전달·보존

계보를 **거절이 아니라 전달**로 풀었다. 사용자에게 열어 둔 AX 담당 지정 기능을 축소하지 않는다.

- `platform/work_tasks.py::create_task_for_request` 가 네 계보를 인자로 받는다. 요청 자신의 판단 회차가
  있으면 그것이 출처고(과거 행), 없으면 호출자가 준 계보를 싣는다. `tasks.source_action_item_id` 도 이제 채운다.
- `modules/work/requests.py::WorkRequestApplication.create` 가 네 인자를 받아 그대로 흘려보낸다.
- `modules/work/creation_commands.py` — `create_task` horizontal 갈래와 `create_work_request` 둘 다 전달.
- `bootstrap/application.py::create_work_request` · `platform/actions.py` 의 `work_request.create` 확정 실행도 전달
  (`source_action_item_id=action.id`).
- **담당(assignment) 행의 source refs 는 회차에서만 채운다** — 신규 경로엔 그 사람을 앉힌 판단이 없으므로
  하지 않은 판단을 담당 관계가 가리키지 않는다. `create_assigned_task`(managed)와 같은 기준이다.
- **테스트**: `…::test_an_ax_confirmation_that_names_a_recipient_keeps_the_action_it_came_from`
  — 확인 전 `TaskRecord`·`WorkRequestRecord`·`TaskCreationAttemptRecord` **0건** → 확인 후 담당은 지호이고
  `lineage.source_action_item_id == action_id` · `source_work_request_id` · `source_decision_item_id` ·
  `source_submission_id` 가 모두 실림 → **재실행(replay)** 시 업무·요청 각 1건, 원장 key 는 action id.

### W-2 — 요청 출신 업무의 `created_by_actor_id`·최초 회차 actor

「전부 requester 로 치환」하지 않고 **실제 caller 를 전달**하는 방식으로 고쳤다.

- `create_task_for_request(request, *, actor_id, …)` 로 행위자를 명시 인자로 받는다.
  - 신규 경로: `WorkRequestApplication.create` 가 `str(principal.id)` — **명령을 실제로 부른 사람**.
  - **회의 승격**: principal 이 누른 사람이므로 그 사람이 남는다. `system:meeting`(requester_id)도, 받는 사람도 아니다.
  - **과거 pending 행의 수락**: `create_accepted_task` 가 `actor_id=request.assignee_id` 를 그대로 넘긴다 —
    그 시절엔 담당자의 수락이 업무를 있게 한 것이 맞다. 두 뜻을 한 값으로 뭉개지 않았다.
- `capture_version(task, actor_id, "task.created")` 도 같은 값을 쓴다 → `GET /api/tasks/{id}/history` 첫 회차 actor 교정.
- **권한 회귀 확인**: 읽기는 전부 활성 담당으로 스코프된다(`_held_by`), `created_by_actor_id` fallback
  (`application.py:433`)은 담당이 없을 때만 쓰이는데 이 경로는 언제나 담당이 있다. 테스트로 고정했다.
- **테스트**: `…::test_the_creating_actor_is_the_one_who_ran_the_command_on_every_path`
  — 신규는 `mina`(칼럼 + history 첫 회차) · **과거 모양 수락은 `jiho` 그대로** ·
  보낸 사람은 남의 `my_work` 를 얻지 못하고 · 관계 없는 구성원(minseok, `task.read` 보유)에게는 **404 존재 은닉** ·
  보낸 사람은 출처로 계속 200 으로 읽는다.
- **낡은 단언 교정**: `test_task_actor.py` 의 `test_an_accepted_request_keeps_the_sender_where_the_request_is`
  → `test_a_sent_request_keeps_…` 로 이름과 단언(`"jiho"` → `"mina"`), 주석
  「The acceptance created the Task」를 지금 뜻으로 교체. (1차 contract run 이 정확히 이 1건으로 실패했고,
  그것이 W-2 가 지적한 「낡은 뜻을 못 박은 테스트」다.)

### W-3 — README 권한을 명령별로 정확히 구분

소스에서 8개 명령의 `_require` 를 전수 확인하고 다시 적었다.

| 명령 | 실제 역량 (확인한 자리) |
|---|---|
| 요청 수락·거절·조정 | `work_request.decide` (`requests.py:316·331·353`) |
| 요청 재상신·거두기 | `work_request.create` (`requests.py:392·474·516`) |
| 배정 수락·거절 | `task.self_manage` (`assignments.py:221·232`) |
| 배정 취소 | `task.assign` (`assignments.py:251`) |

README 해당 bullet 을 위 네 갈래로 갈라 적고, 거절 모양도 실측대로 적었다 —
**받는 사람 422 / 관계 없는 사람 404(존재 은닉)**.

### W-4 — domain-model 「판단 API」 bullet 에서 살아 있는 AX 경로 분리

한 묶음이던 endpoint 셋을 **처지별 세 갈래**로 나눴다.

1. `work-requests/{id}/accept|reject|negotiate` · `task-assignments/{id}/accept|decline` → **과거 행 전용**(422/404 · side effect 0).
2. `work-requests/{id}/resubmit` → 판단이 아니라 **요청자의 재상신**(`work_request.create`, 행위자가 다름).
3. `POST /api/actions/{id}/decide` → **신규 AX 확인의 현행 경로이고 지금도 살아 있다**(SPEC-001 §6).

### W-5 — 없는 회의 route/table 을 실제 todo 경로·잠금으로 정정

- API: `POST /api/meetings/{id}/summaries/{summary_id}/statements/{index}/promote` → **`POST /api/meetings/{id}/todos/{todoId}/promote`**(`Idempotency-Key` 필수).
- 중복 방지 근거: 없는 `meeting_followup_promotions` unique → **실재하는 후보 잠금**
  `MeetingApplication.todo_for_promotion` 의 `_readable(lock=True)` + `todo(lock=True)` +
  `ensure_todo_actionable(linked_work_request_id=…)`(`meetings/application.py:848-861` 확인), 그 위에 생성 층 멱등 키 — **두 층**.
- 회의 상세의 표시는 `linked.work_request_id`(`meetings/application.py:1788` 확인).

### W-6 — 신규 `assigned` 의 근거 경계를 정확히 기술 (참조 API·권한 실재 확인)

`docs/domain-model.md` EVIDENCE 행에 한 문단을 더했다. **주장마다 돌려서 확인했다**:

| 주장 | 실측 |
|---|---|
| 신규 요청의 `POST …/evidence` 는 영구 422, 첨부·감사 0 | 422 (`store_file` 앞) ✔ |
| 업무 자료 기능은 남는다 | `POST /api/tasks/{id}/materials` **201**(담당자) ✔ · `/materials/links` **201** ✔ |
| 그 길은 **담당자**의 것이다 | 보낸 사람(민아) **404** — `task.self_manage` + 활성 담당이 조건(`materials.py:212-214`) ✔ |
| 논의 첨부는 신규에서도 산다 | `POST …/comments/{id}/attachments` **201** ✔ |

### W-7 — 잡음·낡은 주석·얕은 단언·키 커버리지

| 항목 | 조치 |
|---|---|
| `== "` → `=="` 172줄 잡음 | 4개 파일에서 **188곳 복원**(`test_action_center` 100 · `test_mcp_action_items` 50 · `test_request_amendment` 23 · `test_evidence_continuity` 15). 남은 diff 는 legacy fixture 전환뿐임을 확인 |
| SAVEPOINT 자기모순 주석 | `work_tasks.py` 클래스 docstring 의 「SAVEPOINT 안에서 받는다」를 지우고 실제 동작(commit 시점 unique 위반 → 조립 층 재시도)으로 교체. 근거는 `claim` 주석이 갖는다 |
| `command_kind` 오기 | `persistence.py` 주석 `meeting.followup.promote` → **`work_request.create`**(+ 상수 위치 `modules/work/creation.py`) |
| no-op accept 호출 | `test_task_origin.py` 두 자리에서 제거하고 「수락 단계가 없다」주석으로 대체 |
| `in {403, 404, 422}` 얕은 단언 | `test_action_center.py` 에서 **404(받는 쪽 존재 은닉) / 422(보낸 쪽 명령 불가)** 두 값으로 각각 고정 |
| 키 누락 미검 4자리 | `…::test_the_manager_assignment_and_meeting_promotion_surfaces_also_refuse_a_missing_key` 신설 — `/api/tasks/assign`(헤더 누락·빈·공백) · `…/todos/{id}/promote`(누락·빈·공백) · MCP `assign_task` · `promote_current_meeting_todo`. 거절 뒤 Task·원장·WorkRequest 0건과 **후보가 승격되지 않은 채로 남는 것**까지 단언 |
| 「잃은 단언 1건」(리뷰 ② P3) | `test_task_assignments.py` 에 복원 — 신규 배정에 **남이** 수락/거절을 걸면 **404**(배정한 사람에게도) |

---

## 2. 자료 worker 실패 2건 — 원인·조치·검증

### 결론: **제품 race 가 아니라 fixture 의 시간 의존**이다. 제품 fencing 은 정확히 동작했다.

**재현**: CPU hog 24개를 띄우고 두 테스트만 돌려 `verify-2026-09-16.log` 와 **같은 두 단언**을 재현했다.

```
test_long_parse_heartbeats…  : assert job["state"] == "completed"  →  'running'
test_stage_timeout_fences…   : ['failed','completed']              →  ['failed','running']
```

**계측**(worker 의 `_heartbeat`·`_extend_transport` 를 감싸 시각·소요·반환을 기록):

| 부하 | 박동 간격 | 마지막 구간 | 결과 |
|---|---|---|---|
| 유휴 | 1.01 · 1.00 · 1.00 · 1.00 · 1.01 · 1.01 | 박동 1.117s 소요, 간격 2.12s | `extend_transport` **True** → completed |
| hog 24 | 1.01 · 1.00 · 1.00 · 1.00 · 1.00 | **박동 하나가 2.62s 블록**(t=7.01 시작 → 9.63 종료) | `extend_transport` **False** → running |

메커니즘: `material_queue_visibility_timeout=3`(테스트가 고정), 박동 간격 `lease/3 = 1s`.
7.01 에 갱신된 lease 는 10.01 에 만료된다. 그런데 그 박동 호출 자체가 2.62s 블록되고, 이어서
자식 결과 게시(`asyncio.to_thread(_extend_transport)`)가 스레드 배정을 기다려 **10.43** 에 실행됐다 —
만료 0.42s 뒤다. `extend_lease` 가 False 를 돌려주자 worker 는 **결과를 게시하지 않고** 반환하고,
`run_once` 가 「attempt ended without a result」로 job 을 정리한다.

즉 **lease 를 잃은 worker 가 결과를 쓰지 않는 것은 설계대로 옳은 동작**이다. 깨진 것은
「3초 안에 반드시 한 번은 CPU 를 받는다」는 **테스트의 전제**이고, `-n auto` 최대 병렬 + `spawn` 자식
프로세스(이 기계에서 기동만 4~5초)가 그 전제를 깬다. 자식이 「active」로 올라오기 전 박동이
`waiting` 을 돌려주는 구간도 유휴에서 3~5초다.

**시도했다가 되돌린 것 (근거 포함)**: 박동 예약을 고정 지연(`완료시각 + interval`) → 고정 주기
(`직전 예정시각 + interval`)로 바꾸면 한 번 느린 박동이 다음 박동을 밀어내는 drift 가 사라진다
(계측에서 4.029/5.034/6.039 → 4.015/5.015/6.015 로 정확해짐). 그러나 **hog 24 에서 두 테스트는 여전히 실패**했다 —
지배적 요인이 drift 가 아니라 호출 자체의 2.6초 블록과 스레드 배정 지연이기 때문이다.
증상을 고치지 못하는 제품 변경을 durable-job lease 경로에 남기는 것은 범위 밖이라 **원복했다**
(`git diff --stat -- bootstrap/material_worker.py` 빈 출력 = 무변경).

**권고**(코디/planner 판단 필요 — 내가 코드로 정하지 않았다): 셋 중 하나다.
1. 이 두 테스트를 최대 병렬에서 빼고 직렬로 돌린다(`scale` 처럼 마커 분리). 단언은 그대로 산다.
2. 박동 예약을 고정 주기로 바꾼다(위 계측 근거). 완화가 아니라 개선이지만 이 실패는 못 막는다.
3. 그대로 둔다 — 이 기계의 `-n auto` 부하에서만 나는 환경 flake 임을 알고 넘어간다.

**sleep 늘리기·단언 약화·skip 은 쓰지 않았다.** 두 테스트 파일도 worker 도 이번 작업에서 **무변경**이다
(`git diff HEAD --stat` 로 확인).

---

## 3. 계약 준수

- horizontal 의 `start_date`/`parent`/`project` **미지원 계약 유지** — 받아 주지 않고 각각 422. self/managed 지원 보존(테스트로 고정).
- **자료·출처·actor 를 조용히 버리지 않는다** — W-1 이 버리던 계보를 전달로 바꿨고, W-2 가 거짓이던 actor 를 실제 caller 로 고쳤다.
- API 공개 shape·도구 schema **무변경**: `http.py` 무수정, MCP 도구 인자 무변경, inventory 테스트 4 passed(변경 불필요).
- legacy fixture **현행 유지, 확대 없음**(`tests/legacy_acceptance.py` 무수정).
- 공유 트리 stash/checkout/reset **미사용** — baseline 비교는 `git show HEAD:<file>` 와 `git diff HEAD --stat` 읽기 전용만.
- `frontend/` 무수정(13개 FE 변경은 FE 워커 것 그대로). 커밋·push·PR 없음. `ax_demo` 무접촉.

---

## 4. 남은 항목 / 주의점

1. **inventory 변경 필요 없음.** `WorkflowApplication.create_work_request` 에 인자 넷이 늘었지만 HTTP 라우트
   시그니처·도구 schema·`owning_calls` 는 그대로라 drift 가 없다 — `test_operation_inventory.py` **4 passed** 로 확인.
2. **리뷰 ② 의 `_erase_task` 메모**: legacy fixture 가 tasks FK 를 가진 모든 행을 지우므로
   `task_creation_attempts` 행도 함께 지운다. 리뷰가 기록만 권했고 이번에 바꾸지 않았다.
3. **인수조건 #8(권한 밖 담당 지정)**: 데모 조직이 회사 하나라 조직 범위 교집합이 늘 겹쳐
   `WORK_RECIPIENT_NOT_ALLOWED` 가 실재 구성원에게는 도달 불가라는 리뷰 판정은 그대로다 — SPEC 결정 사항이라 손대지 않았다.
4. **기존 부채 3건**(리뷰 §기존 부채 1·3·4)은 이번 범위 밖이라 그대로다:
   `meeting.followup.*` AX action 의 AttributeError, FE 의 죽은 import, `unified-operations.md` 의 `HTTP 137개` ↔ inventory 140.
5. `make verify` 전량은 코디 몫. E2E 사용자 담당.
