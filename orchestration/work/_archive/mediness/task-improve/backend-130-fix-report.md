# backend — WP-130 검수 FAIL 정정 리포트

- 일시: 2026-09-01
- 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (branch `kknaksss/task-improve`, 미커밋 위)
- 근거: `review-code130-report.md` (F-1 · F-3 · W-3 · W-4 · W-9 + §요약조치 7)
- 범위: `back/` 만. `front/` 무수정.

---

## 1. 위반 ① — 「깨진 테스트 26건」의 실체는 **둘로 갈린다**

리포트는 26건 전부를 「이 diff 가 깨뜨린 것」으로 봤다. 실측은 다르다.

| 갈래 | 건수 | 원인 | 조치 |
|---|---|---|---|
| (a) 선행 실패 | **20** | `POST /versions/{v}/wbs/tasks` (work_item) 가 **부모 phase 의 execution 조직**을 요구한다(`version_wbs.create_task:1153`). 테스트가 `VersionAssignment.department_org_unit_id` 를 안 세워 phase 가 조직 없이 서고 **400** 이 난다. | 파일 안에서 `_assign` 을 계약에 맞추고 각 케이스에 배정을 세웠다 |
| (b) 이 diff 가 깨뜨린 것 | **6** | 새 근거 검사(`lifecycle.guard_completion_evidence`)가 사람 액터의 `→ done` 전부에 걸리는데 WBS 칩이 `completionNote` 를 안 보낸다 → **422** | 헬퍼 한 곳에서 `completionNote` 를 싣도록 갱신 + **422 계약 자체를 고정하는 테스트 신설** |

### (a) 가 선행 실패라는 근거 세 가지

1. 실패 지점은 **생성**(`create_task`)이고, 이 diff 의 `version_wbs.py` 변경은 `patch_task`·
   `_transition_linked_task` **둘뿐**이다(`git diff` 로 확인 — 생성 경로 0줄).
2. 그 400 을 내는 줄은 커밋 `9578e714`(2026-08-10, WP-103~104 「조직·Task 정본 기반 WBS 전환」)가
   넣었다.
3. **이 diff 가 전혀 건드리지 않은** `tests/api/test_version_wbs_crud.py` 도 같은 이유로 15건
   실패한다(이 라운드 범위 밖이라 손대지 않았다 — 좌표 밖 금지).

⇒ 「선행 실패 재분류」로 넘기지 않고 **두 파일 안에서 전부 고쳤다**. 다만 위 사실은 그대로 보고한다:
BE 의 「447 passed / 0 failed」가 부분 실행이었다는 리포트 판정은 맞고, **「26건이 이 diff 의
신규 실패」라는 부분은 6건이 맞다**.

### 갱신 내용

**`back/tests/api/test_version_wbs_checkitem.py`**
- `_assign` 이 `department_org_unit_id=unit.id` 를 명시로 채운다 — `repo.list_assignment_org_units`
  가 **그 컬럼으로 join** 하므로 legacy `department` slug 만으로는 phase 가 조직을 못 받는다.
  (같은 파일의 `test_wp104_w3_status_axis._assign` 과 **같은 모양**으로 맞췄다.)
- 업무를 만드는 케이스마다 `await _assign(db, v.id, admin.id)` — 형제 파일이 이미 쓰는 관용.
- `_status_body(status)` 헬퍼 신설: `done` 이면 `completionNote` 를 **한 곳에서** 싣는다.
  `_create_then_status`·`_patch_status`·직접 PATCH 세 자리가 그 헬퍼를 지난다.
- 삭제·취소 응답 shape 정정(`data.tree` — `WbsTaskDeleteResult`). 같은 파일
  `test_work_delete_recomputes_phase` 가 이미 쓰던 모양이고, 선행 실패에 가려져 있었다.
- **신설** `test_done_without_evidence_is_422_and_changes_nothing` — 근거 없는 `→ done` 이 422 이고
  `detail.code == TASK_COMPLETION_EVIDENCE_REQUIRED` 이며 **상태·부모 rollup 이 하나도 안 바뀐다**를
  고정한다(422 술어 자체는 손대지 않았다).

**`back/tests/services/test_version_progress.py`**
- `_DONE_BODY = {"status": "done", "completionNote": ...}` — done PATCH 3자리(:226·:270·:304).
  이 파일은 이미 `_assign` 을 쓰고 있어 (a) 갈래가 없다 — 실패 2건 전부 (b) 였다.

### 수치

```
tests/api/test_version_wbs_checkitem.py + tests/services/test_version_progress.py
  전:  28 failed, 13 passed, 1 skipped
  후:  43 passed, 1 skipped          (신설 1건 포함)
```

---

## 2. 위반 ③ — 첨부 바인딩 오소비 차단

### 무엇이 문제였나

`landing_chat/turns.py:170` 이 발화 접수 때 Redis 바인딩을 심는데 **사람 축 하나**였고, 소비자는
`POST /task-drafts` **하나뿐**이었다. 그래서:

> 파일 첨부 → 「이 태스크 **수정**해줘」(모델이 `task_update` 호출 — 소비자가 아니다)
> → 바인딩 생존 → **30분 안의 다음 «생성» 발화**가 그 파일들을 **엉뚱한 새 태스크에** 붙인다.

### 정정 — 세 겹

**① 소유자 대조** (`attachment_binding.claim_owner` / `owner_of` / `owns`)
- 스테이징 발급·추가 업로드가 `task_draft_staging_owner:{draft_id} → member_id` 를 남긴다(TTL 30분).
- `remember` 는 **소유가 확인된 `draft_id` 만** 바인딩으로 세운다 — 기록이 없으면(만료·Redis 부재)
  **fail-closed**(첨부 0 이 남의 파일보다 낫다).
- `POST /task-draft-attachments` 는 **다른 사람 것**인 `draft_id` 를 **404**(존재 은닉)로 막는다.
  기록이 없는 것은 「남의 것」이 아니라 통과다(정상 사용자의 두 번째 파일을 막지 않는다).
- ⇒ `attachments.py` 모듈 docstring 의 「클라이언트가 지어낸 id 를 받지 않는다」가 **사실이 됐다**
  (검수 W-4 — 「실효 방어는 UUID4 추측 불가 하나」였던 상태를 정정).

**② 방 대조 + 1발화 1바인딩**
- 바인딩 값이 `{"draft_id": ..., "room_id": ...}` JSON 이 됐다.
- `remember` 를 **방 확정 뒤**로 옮겼다(403 참조로 접수가 막힌 발화는 바인딩도 안 남긴다).
- **첨부 없는 발화가 앞선 바인딩을 지운다** → 오소비 창이 「30분」에서 **「한 발화」**로 줄었다.
- ⚠ **대기 조각(queued)은 지우지 않는다**(`clear_if_absent=False`) — 그 조각은 앞 발화와 **같은
  turn 으로 합쳐져** 나가므로, 지우면 사용자가 방금 붙인 파일이 자기 발화에서 사라진다.

**③ 생성 발화 흐름에서만 소비 + 즉시 삭제**
- `consume(redis, *, member_id, room_id)` — `room_id` 가 없으면 **소비하지 않는다**.
- 방은 `POST /task-drafts` 에서 **MCP 토큰의 turn** 으로 얻는다
  (`landing_chat.taint.turn_for_token_jti` — 「그 토큰이 곧 turn 식별자」인 D19 계약 재사용,
  새 식별 축 0). turn 이 없으면(웹·데스크톱 직접 호출) 소비 대상이 아니다 — 그 경로는 body 로
  `draft_id` 를 명시한다(「명시가 이긴다」 그대로).
- 방이 **맞을 때만** 지운다(1회성). 방이 다르면 소비도 삭제도 하지 않는다 — 그 바인딩은 아직
  자기 방에서 쓰일 자격이 있다.

### 수정 카드 첨부 = **v1 미지원**으로 봉인 (반쪽 잔재 제거)

- `schemas/action_runtime.py` `TaskUpdateCreateRequest.draft_id` **제거** + 왜 없는지·v2 에서 열 때
  무엇을 함께 세워야 하는지를 docstring 에 남겼다.
- `definitions.py` `UPDATE_DEFINITION.on_reject=_discard_staged_attachments` **제거**(죽은 훅).
  `DRAFT_DEFINITION` 의 같은 훅은 **그대로**다(그쪽은 실제로 payload 에 `draft_id` 가 실린다).
- MCP `task_update_request` 는 애초에 `draft_id` 를 안 보낸다(확인함) — 호출자 영향 0.
- **신설** `test_task_update_request_has_no_attachment_field` 가 이 봉인을 고정한다.

### 신설 테스트 (`tests/services/engine_v2/test_ax_task_draft.py`)

| 테스트 | 고정하는 사실 |
|---|---|
| `..._refuses_a_draft_owned_by_someone_else` | 남의(또는 기록 없는) `draft_id` 는 바인딩이 **안 선다** |
| `..._is_not_consumed_across_rooms` | 다른 방·방 없음에서 소비 0, 자기 방에서는 그대로 산다 |
| `test_attachment_free_utterance_clears_a_stale_binding` | 첨부 없는 발화가 잔재를 치운다 / **대기 조각은 안 치운다** |
| `..._is_remembered_then_consumed_once` (갱신) | 소비 즉시 삭제 — 1회성 |
| `test_task_update_request_has_no_attachment_field` | 수정 축에 반쪽 배선이 없다 |

---

## 3. WARN 처리

**W-3 · 25MB 를 전량 수신 전에 본다**
- `task_reference_storage.guard_declared_size(content_length)` 신설 — `Content-Length` 로 선검사.
  ⚠ **상한을 대체하지 않는다**: 값이 없거나 거짓이면 통과하고 실제 바이트는 `guard_size` 가
  종전대로 잡는다. multipart 봉투 여유(64KB)를 둬서 **정확히 25MB 인 파일이 boundary 때문에
  거절되는** 일이 없다.
- `add_task_reference_ep` · `stage_task_draft_attachment_ep` 두 문이 `request.form()` **앞에서**
  부른다(라우터 헬퍼 `_guard_declared_upload_size` 한 곳 — 상한 숫자는 storage 만 안다).
- 신설 `test_declared_size_is_checked_before_the_body_is_read`.

**W-9 · 주석 오타** — `task_reference_storage.py:51` 「마지막 확장자만 **보지 않는다**」→
「마지막 확장자만 **본다**」. 이어지는 설명(`a.exe.txt` 통과 / `a.txt.exe` 차단)·코드
(`os.path.splitext(...)[1]`)와 이제 일치한다.

**§요약조치 7 · stale 주석** — `tasks_surface.create_task` docstring 의 「수락 게이트가 있는
상태로 태어난다」(WP-126 이 2026-08-31 에 폐기한 어휘)를 걷고 「게이트 없음 · 초기 상태는 예외 없이
`todo`」로 정정했다.

---

## 4. 재검증 수치 — **영향 파일 1회**(전체 회귀는 CI 몫)

```
pytest tests/api/test_version_wbs_checkitem.py \
       tests/services/test_version_progress.py \
       tests/services/engine_v2/test_ax_task_draft.py \
       tests/api/test_wp130_task_detail_unification.py \
       tests/api/test_wp129_task_request_axis.py

→ 163 passed, 1 skipped (86.9s)
```

| 대상 | 전 | 후 |
|---|---|---|
| `test_version_wbs_checkitem.py` + `test_version_progress.py` | 28 failed / 13 passed / 1 skipped | **43 passed / 1 skipped** (신설 1 포함) |
| `test_ax_task_draft.py` (바인딩 신설 4 + 봉인 1) | 63 passed | **67 passed** |
| `test_wp130_task_detail_unification.py` (선검사 신설 1) | 37 passed | **38 passed** |
| `test_wp129_task_request_axis.py` | passed | **passed**(회귀 0) |
| ruff (수정 파일 전량) | — | 신규 0 |

---

## 5. 지나가며 본 선행 실패 (이 라운드 좌표 밖 — **손대지 않았다**)

§1 판정 근거를 세우다 본 것들이다. 전부 **이 diff 와 무관**하고 내 수정 전후로 같다.

| 대상 | 건수 | 원인 |
|---|---|---|
| `tests/api/test_version_wbs_crud.py` | 15 | 위 §1(a) 와 같은 phase execution 조직 선행 실패 |
| `tests/api/test_landing_chat_refs.py` | 10 | 테스트 mother 가 만든 task 가 `ck_tasks_execution_required_for_workflow`(migration **0107**) 를 위반 — 픽스처 대 제약의 어긋남 |
| `tests/api/test_meeting_v2_test_inject.py` | 수집 오류 | 모듈 import 단계 |
| `tests/schema/test_version_wbs_schema.py` | 수집 오류 | `VersionWbsLinkKind` 가 `app.models.version_wbs` 에 없다 |

⇒ 다음 라운드 좌표 후보로 올린다. (특히 `test_version_wbs_crud.py` 는 이번에 고친 것과 **같은 한 줄
패턴**이라 기계적으로 닫힌다.)

---

## 6. 손댄 파일

```
back/app/routers/action_runtime_v2.py
back/app/schemas/action_runtime.py
back/app/services/action_runtime/workflow/task_draft/attachment_binding.py
back/app/services/action_runtime/workflow/task_draft/attachments.py        (docstring)
back/app/services/action_runtime/workflow/task_draft/definitions.py
back/app/services/action_runtime/workflow/tasks_surface.py                 (docstring)
back/app/services/landing_chat/turns.py
back/app/services/task_reference_storage.py
back/tests/api/test_version_wbs_checkitem.py
back/tests/api/test_wp130_task_detail_unification.py
back/tests/services/engine_v2/test_ax_task_draft.py
back/tests/services/test_version_progress.py
```

**하지 않은 것**: `front/` 0 · 422 술어 변경 0 · migration 0 · 새 상태/이벤트 0 · 새 leaf 0.
