# W1 operation inventory·제품 문서 동기화 결과 — 2026-09-16

## 상태: done

바꾼 파일은 allowed_paths 넷뿐이다. 제품 코드·테스트·다른 워커 파일은 건드리지 않았고, stash/checkout/reset 을 쓰지 않았다.

```
 README.md                              | 15 ++++---
 docs/domain-model.md                   | 26 +++++++-----
 docs/unified-operations-inventory.json | 73 +++++++++++++++++++++++++---------
 docs/unified-operations.md             |  6 ++-
```

---

## 1. `docs/unified-operations-inventory.json`

scratchpad 갱신본을 **그대로 쓰지 않고**, 현재 코드에서 다시 생성해 현 파일과 비교한 뒤 반영했다(재생성 결과는 11:20 본과 동일 — 그 사이 inventory 입력 파일이 바뀌지 않았다).

diff 는 19 hunk / 실질 73줄이고 **전부 W1 생성 표면 넷**이다. 무관한 churn(키 재정렬·공백·다른 라우트)은 없다.

| 무엇 | 어디 |
|---|---|
| `http_handler` `create_self_task` → `create_task` | `POST /api/tasks` |
| `http_application_calls` `create_self_task` → `create_task` | `POST /api/tasks` |
| `owning_calls` → `self._task_creation(session).create_or_receipt` | `POST /api/tasks` · `POST /api/tasks/assign` · `POST /api/work-requests` |
| `owning_calls` `self._work_requests(session).create` → `self._task_creation(session).create_work_request` | `POST /api/meetings/{id}/todos/{todoId}/promote` |
| `http_signature` 에 `idempotency_key: str \| None` 추가 | 위 네 라우트 |
| `input_schema` 에 필수 `idempotency_key` + description | 도구 `task_create_self` · `task_assign` · `work_request_create` · `meeting_todo_promote` |
| `input_schema` 에 `assignee_id`(optional, ≤100자) | 도구 `task_create_self` |
| 도구 `description` 갱신(키 규칙 · 수락 단계 없음 · 담당 지정) | 위 네 도구 |

`operation` · `baseline_tools` · `target_tools` · `acceptance_evidence` · `status` 는 건드리지 않았다. `tool_count`(120) · `http_count`(140) 도 그대로 — W1 은 라우트·도구를 더하거나 빼지 않았다.

**검증**: `json.load` 파싱 통과. `git diff --check` clean.
그리고 `docs/` 를 갈아끼운 격리 fakeroot 에서 inventory 테스트 셋을 직접 호출해 전부 PASS 했다 —
`test_inventory_schemas_match_the_actual_registered_tools` · `test_inventory_includes_each_declared_http_operation` ·
`test_final_inventory_has_no_implicit_or_unverified_product_surface`.
**`make test-unit` 전체를 돌리지는 않았다**(코디가 통합 실행). 위 셋 말고 다른 테스트의 통과를 주장하지 않는다.

---

## 2. `README.md` — 「업무 — 요청과 배정」 절과 후보 문장

바꾼 문장 다섯 자리.

| 자리 | 지금 뭐라고 쓰여 있나 |
|---|---|
| 「데이터 넣기」 마지막 문단 | `답할 수 없는 사람` → **`들어올 문이 없는 사람`**, `판단이 영영 기다리는 항목이 생기지 않는다` → **`아무도 손댈 수 없는 업무가 생기지 않는다`**. 후보 필터(로그인 가능)는 그대로인데 **이유**가 달라졌다 — 이제 받는 사람이 판단하지 않는다 |
| 절 첫 문단(신규) | 한 번의 생성 명령으로 업무가 실재한다 · 수락 없이 즉시 · `Idempotency-Key` 필수 · 영수증(돌려주기 전 열람 권한 재검사) · 같은 키 다른 내용은 충돌 · **서버가 키를 대신 만들지 않는다** |
| 할일 문단 | `업무 요청 · 업무 배정 · 업무 결과 확인 · AX 제안` 넷 나열 → **신규 생성은 아무것도 만들지 않는다**, 지금 쌓이는 것은 결과 확인과 AX 제안. **과거 수락 항목은 그대로 남아 계속 답할 수 있다** |
| 요청·배정 bullet | 요청: 판단 권한을 묻지 않으므로 배정 권한 없는 구성원도 보낼 수 있다 · 후보 셋(문·본인 제외·조직 범위) · 목록과 명령이 같은 판정 · 요청 행은 출처로 남고 `source_work_request_id` 로 **완료 승인 확인자가 거기서 나온다** · 출처 상태 `assigned`. 배정: `task.assign` 과 조직 범위 검사는 **그대로**, 달라진 것은 기다림이 없다는 것뿐 · 잘못 온 배정의 출구는 거절이 아니라 문의와 담당자 변경. **세 번째 bullet 신설** — 과거 `pending` 행에는 수락·거절·조정·재상신과 회차별 근거가 그대로 걸리고 여전히 `work_request.decide` 를 요구한다 |
| `task_assignments` 문단 | 셋 다 생성 시점에 `active` · 활성 담당은 0 또는 1 · **부분 unique 인덱스 `uq_task_assignments_active` 가 데이터베이스에서 지킨다** |

건드리지 않은 것: 완료 보고/완료 인정/보완 요청 문단, AX 「쓰기는 바로 일어나지 않는다」 문단, 담당자 변경·취소·업무 수정 문단. 전부 W1 이 바꾸지 않은 사실이다.

---

## 3. `docs/domain-model.md`

### § 판단 통합 (ActionItem) — 현재 상태

- 절 도입부: `사람 판단이 필요한 경로는 업무 요청, 직접 배정, AX 변경 제안 세 가지` → **신규 생성은 그 경로를 열지 않는다**, 지금 새로 열리는 판단은 완료 결과 확인과 AX 제안이며, 아래 계약은 그 둘과 **과거 수락 항목**에 그대로 적용된다.
- 「판단 API는 하나다」 bullet: 남은 kind별 endpoint 는 **과거 행을 위해 남아 있고**, `assigned` 요청·`active` 배정에 걸면 **정의된 거절이며 회차·첨부·감사에 side effect 가 없다**, 신규 경로에 거절 명령을 신설하지 않는다.
- 「Task는 자기가 만들어진 사실만 소유한다」 bullet: `요청 수락` → `요청에서 파생된 담당`. 활성 담당 유일성에 DB 인덱스 근거 추가. **담당자 변경은 생성이 아니므로 수락 단계가 그대로 남아 새 assignment 는 `pending`** 임을 명시(혼동 방지).
- 「회의에서 나온 일은 사람이 결정할 때 일이 된다」 bullet: `요청으로 만들면 담당자가 평소처럼 판단한다` → 승격도 **같은 명령·같은 권한·같은 멱등 계약**을 쓰므로 담당을 지정하면 수락 없이 그 사람의 업무가 된다.

### § 판단·요청 연속성·업무 (Work) 표

| 행 | 바꾼 것 |
|---|---|
| `WORK_REQUEST` | `state` 여섯 값 명시 + **신규는 `assigned`**(판단 없이 섰다는 사실만, 수락이 아니다) + 나머지 다섯은 과거 행 값이고 뜻 불변 + 요청 행이 출처로 남는다 |
| `ACTION_ITEM` | `kind` 목록에 `task.delivery.review`·`ax.*` 추가 + **수락 두 종류는 신규 생성이 더는 만들지 않는다**(과거 행은 읽히고 답해진다) |
| `TASK` | `origin_kind` 값 보정(`meeting`·`project_plan` 누락 → 코드와 일치) + `approver_id` (nullable, **열만 있고 값이 들어오지 않는다**) |
| **(신규 행)** 생성 멱등 원장 `task_creation_attempts` | 키 범위가 (행위자·명령 종류)인 이유 · 지문 · 같은 키/다른 키 규칙 · 업무·담당과 같은 transaction · 동시 실행에서 진 쪽이 영수증을 읽는 경로 · 기존 전역 `causation_key` 는 뜻이 달라 그대로 두었다 |
| `TASK_ASSIGNMENT` | `request_effect(요청 수락)` → `(요청에서 파생)` · **셋 다 생성 시점 `active`** · `pending` 은 담당자 변경과 과거 행에만 · `uq_task_assignments_active` 로 DB 가 지킨다 · 과거 `pending` 배정의 수락/거절은 그대로, 신규 `active` 에 걸면 정의된 거절이고 변화 없음 · API 에 `Idempotency-Key 필수` 표기, MCP 목록에서 discovery 에 없는 `task_assignment_inbox\|accept\|decline` 제거 |
| `WORK_REQUEST_REFERENCE` | `수락으로 Task가 만들어질 때` → `요청에서 Task가 설 때` |
| `TASK_CHECKLIST_ITEM` | `수락으로 만들어진 Task의 체크리스트` → `그 요청에서 선 Task의 체크리스트` |

### § ERD 밖 테이블

- `task_creation_attempts` 한 줄 추가(계약 본문은 Work 표가 갖고 여기서는 가리키기만).
- 후속업무 승격 bullet: `수락으로 업무가 설 때 tasks 로 옮겨지며` → **`요청과 같은 transaction 에서 업무가 설 때`**, 그리고 승격도 `Idempotency-Key`(MCP `idempotency_key`)가 필수이고 담당자가 수락 없이 든다는 문장 추가.

### § 완료·검수·알림 — 결정됨, 아직 구현하지 않음

내용은 그대로 두고 **인용 한 줄만** 덧붙였다: 아래에서 말하는 「최초 수락 ActionItem」은 신규 경로에서 더는 열리지 않으며, 여기 적힌 결정은 완료 결과 확인 쪽 경계라 수락 gate 제거와 무관하다. (미구현 설계 절이라 결정 자체를 고쳐 쓰지 않았다.)

---

## 4. `docs/unified-operations.md` — 최소 개입

이 문서는 **2026-09-11 일원화 작업의 날짜 박힌 기록**이다(고정 SHA, 통과 수치, `/tmp/...` 로그 경로). 과거형 R2·R3·Acceptance 절을 지금 동작에 맞춰 고쳐 쓰면 끝난 작업의 기록을 위조하는 것이고, 내가 돌리지 않은 테스트의 결과를 바꿔 적는 일이 된다. **그래서 그 절들은 한 글자도 바꾸지 않았다.**

바꾼 것은 셋뿐이다.

1. **문서 머리에 인용 한 단락 추가** — "그 뒤의 변경은 이 기록을 덮지 않는다": 아래 절은 그 시점 관찰 그대로이고 SHA·수치·로그를 나중 작업에 맞춰 고치지 않는다. 그리고 2026-09-16 W1 이 무엇을 바꿨는지(네 라우트의 `Idempotency-Key`, 네 MCP 도구의 `idempotency_key`, 신규 요청·배정의 수락 gate 제거, 요청·배정 수락 판단은 과거 행에만, **완료 결과 확인과 AX 실행 확인은 그대로**)를 요약하고 현재 동작의 정본이 README·domain-model 임을 가리킨다.
2. **§조회 목적 표 — `task_assignment_candidates`·`sent_task_assignments` 행**: `수신 판단함은 action_item_list로 연결` → 신규 배정은 수신 판단을 만들지 않아 거기 서지 않고, 과거 `pending` 배정만 거기서 답한다.
3. **§조회 목적 표 — `work_request_assignee_candidates`·`work_request_cc_candidates` 행**: `active/login 판단 가능 조건은 현행 owning query 유지` → 재직·로그인 가능·본인 제외·조직 범위 교집합으로 고르고, **받는 사람이 판단하지 않으므로 판단 capability 는 묻지 않으며**, 같은 owning query 를 생성 명령의 대상 검사도 쓴다.

§조회 목적 표는 과거 기록이 아니라 **살아 있는 계약 서술**이라 고쳤다.

---

## 5. 문서 문장을 코드로 확인한 것

보고서 §4 의 대체 문장 초안을 그대로 적용하지 않고, 아래를 실제로 읽어 맞춘 뒤 썼다.

| 주장 | 확인 |
|---|---|
| `uq_task_assignments_active` unique · `task_id` · `status='active'` | 모델 metadata 조회 |
| `task_creation_attempts` 열·unique 구성 | 모델 metadata 조회 |
| `tasks.approver_id` nullable | 모델 metadata 조회 |
| `origin_kind` 실제 값 다섯 | `work_tasks.py` 의 리터럴 전수(`direct`·`meeting`·`request_effect`·`project_plan`·`assignment`) — 기존 문서가 둘을 빠뜨리고 있었다 |
| `create_request` 가 `state="assigned"` 이고 `DecisionItemRecord` 를 만들지 않는다 | 소스 검사 |
| `create_assigned_task` 가 `status="active"` 이고 acceptance 를 열지 않는다 | 소스 검사 |
| **`reassign` 은 여전히 `pending` + acceptance 를 연다** | 소스 검사 — 그래서 「담당자 변경은 수락 단계가 남는다」를 명시했다 |
| 후보 판정이 재직·로그인·본인 제외·조직 범위만 본다 | `work_request_assignee_candidates` + `profile_for`(재직 검사) 소스 |
| 네 라우트가 `Idempotency-Key` 헤더를 받는다 | `http.py` 전수 grep |

---

## 6. 손대지 않고 보고하는 것 (사전 drift, W1 무관)

1. **`docs/domain-model.md` § 판단 통합** 의 회의 승격 bullet 이 `POST /api/meetings/{id}/summaries/{summary_id}/statements/{index}/promote` 와 `meeting_followup_promotions` 표를 가리키는데, **그 라우트는 `http.py` 에 없다**(실제 live 경로는 같은 문서 §ERD 밖 테이블이 적은 `POST /api/meetings/{id}/todos/{todoId}/promote` 하나). 앞 태스크에서 보고한 `modules/meetings/followups.py` 死코드와 같은 뿌리다. 이번엔 그 bullet 의 **수락 전제 문장만** 고치고 라우트·표 이름은 그대로 뒀다 — 범위 밖의 사실 정정이라 코디 판단이 필요하다.
2. **`docs/unified-operations.md` 의 `HTTP 137개`** 와 현재 inventory `http_count 140` 이 어긋난다. W1 이 만든 차이가 아니라 그 기록 이후 라우트가 늘어난 것이고, 날짜 박힌 기록이라 고치지 않았다.
3. `docs/work-code-db-audit-2026-09-16-*` 는 읽기 전용으로 두었다(열지도 않았다).
4. 워크트리의 `정의_v2.md`·`example.md`·`definition.md`·`lifecycle.md` 와 `frontend/` 변경은 내 것이 아니다.

## 7. 하지 않은 것

- 제품 코드·테스트 무수정. `tests/legacy_acceptance.py` 를 확대하지 않았고 그 파일을 열지도 않았다.
- stash·checkout·reset 없음. 기준선 비교는 **현재 코드에서 inventory 를 재생성해 현재 문서와 diff** 하는 방식으로만 했다.
- 커밋·push·PR 없음. `make test-unit`·`make test` 미실행(코디 통합 몫). E2E 미실행.
