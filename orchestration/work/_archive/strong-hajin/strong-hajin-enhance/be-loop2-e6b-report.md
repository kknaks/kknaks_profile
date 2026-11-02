# 2루프 E-6 — AX 도 사람과 같은 「수정」(save_draft → 같은 카드 다음 회차) · 결과 보고

## 상태: done (커밋하지 않음 · `frontend/` 손대지 않음)

- 사용자 결정(2026-10-07 · 대체형을 바꿈):
  - 누가 고치든 같은 수정이다. 사람과 AX 가 같은 `save_draft` 를 쓰고, 결과는 같은 카드의 다음 회차다.
  - AX 전용 도구와 새 상태값(superseded)은 만들지 않는다.
- 앞 판의 C(사유 노출)는 그대로 둔다. 다만 C-3 의 `AX_DRAFT_EDIT_REFUSED` 문구는 쓸 곳이 없어져 걷었다.
- 경로 약어: `B/` = `backend/src/ax_workspace/`

## 1. 할 일 5/5

| # | 한 것 | 위치 |
|---|---|---|
| 1 | **위임 턴의 `save_draft` 통과** — `ax.*` 항목이라도 `save_draft` 이고 **서버가 그 카드에 저장을 열어 둔 때만**(`allowed_commands` 에 `save_draft` — 봉투 규칙 그대로) 그대로 실행한다. 열려 있지 않으면 `AX_DRAFT_SAVE_UNAVAILABLE`. **확정·거절(그 밖 모든 명령)은 지금처럼 `AX_DECISION_REFUSED`** | `B/entrypoints/mcp.py:513`(`_propose_action_item_command`) · 상수 `:259,261` |
| 2 | **부분 수정 = 바뀐 칸만 지금 회차 위에 덮기** — `merge_creation_draft`:<br>— 보낸 칸만 바꾸고 안 보낸 칸은 유지<br>— `null` = 비우기. 비울 수 없는 칸(제목·시각·요청 담당자)은 생성 명령 검증이 422<br>— 목록 칸(체크리스트·참석자·안건 …)은 **목록 전체로 교체**(항목 단위 더하기·빼기 없음)<br>— **모르는 칸**(생성 모델 밖)과 **바꿀 수 없는 칸**(회의 `location` — 장소는 회의실로만 · W-r2-6)은 422. 사유는 C-1 로 AX 에게 간다<br>대상 = `task.create_self`·`work_request.create`·`meeting.reservation.create`.<br>**사람 저장도 같은 병합을 탄다** — `action_center.normalize` 에서 `save_draft` 와 `confirm` 둘 다(「저장은 확인과 같은 입력·같은 검증」 원칙). 화면의 전체 draft 는 「모든 칸을 보낸 부분 수정」 이라 결과가 같다(회귀 시험).<br>**첨부 선택**: `attachment_draft_ids` 를 안 보내면 지금 회차 것을 잇는다.<br>**고친 것이 없으면** 회차가 오르지 않는다(기존 `decide_ax_confirmation` 의 `revised` 판정 그대로) | `B/modules/actions/confirmation.py:187-213`(`PATCHABLE_DRAFT_ACTION_TYPES` · `_LOCKED_DRAFT_FIELDS` · `merge_creation_draft`) · `B/platform/action_center.py:603`(병합) · `:639`(첨부 유지) |
| 3 | **정책·도구 설명**: 「아직 등록 전인 AX 초안을 고치라고 하면 새 카드를 만들지 말고 `action_item_command(save_draft)` 로 **바뀐 칸만** · 등록은 사람이 한다 · 실패하면 사유(코드)를 읽고 고쳐 보내되 같은 호출을 되풀이하지 않는다」 — 업무 생성 지침과 회의 생성 지침 둘 다(Claude 는 같은 문장을 import). 도구 `action_item_command` 설명에도 같은 규칙 | `B/platform/codex_cli.py:112`(`AX_DRAFT_EDIT_RULE`) · `MEETING_CREATION_POLICY` · `WORK_AND_REPORT_ROUTING_POLICY` · `B/modules/ax_execution/tool_catalog.py`(`action_item_command`) |
| 4 | **누가 고쳤나** — 지금 기록에는 없었다: 회차(`submissions.submitted_by`)는 사람·AX 모두 같은 회원 id 이고, `save_draft` 는 감사 기록을 남기지 않았다. **새 칸 없이** 기존 표 `action_item_audit_events` 에 회차를 열 때마다 `event_type="draft_saved"` · `payload={submission_version, edited_by: "person"\|"ax", causation_ref?}` 를 남긴다. AX 여부는 MCP 가 위임 턴의 수정을 `causation_ref="ax_turn:<execution id>"` 로 응용에 넘기고(기존 `caused_by` 문맥 재사용), 기록이 그것을 읽는다. **응답(회차 목록)에는 아직 내지 않는다** — 화면에 「AX 수정」 표지가 필요하면 `rounds[]` 에 한 칸을 더하는 BE·FE 일이다(§4) | `B/platform/action_center.py:1086` · 접두 `B/modules/actions/domain.py:80` · `current_causation` `B/platform/work_tasks.py:112` · 응용 `run_action_command(…, causation_ref=)` `B/bootstrap/application.py:3983` · MCP `B/entrypoints/mcp.py:492` |
| — | **곁에서 고친 것**: 회의 초안 저장의 첨부 확인이 `"task"` 로 고정돼 있었다(`validate_claim(…, "task")`) — 확정 경로처럼 회의면 `"meeting"`. 회의 초안에 자료를 고른 채 저장하면 틀린 주인 종류로 검사하던 자리다 | `B/platform/action_center.py:1072` |

## 2. 시험

`backend/tests/contract/test_e6_ax_draft_save_repro.py` 를 새 동작으로 다시 썼다(12):
- **업무 체크리스트 줄이기**(AX · 바뀐 칸만): 2회차 · 목록 교체 · `null` 비우기 · 제목 유지 · 기록 `(2, ax)` · 여전히 확인 대기
- **회의 참석자 추가 + 시간 변경**(AX): 2회차 · 제목 유지
- **초안 → 사람 수정(전체 draft) → AX 수정(참석자만)** = 3회차 · 사람이 고친 제목·목적 유지 · 회차 이력 1·2·3 · 기록 `(2, person)`, `(3, ax)`
- **고친 것 없음** → 회차 그대로 · 기록 없음
- **사람 전체 draft 저장 회귀** — 보낸 값 그대로
- **모르는 칸**(`colour`) · **바꿀 수 없는 칸**(회의 `location`) · **비울 수 없는 칸**(`title: null`) → `ToolError("<코드>: …")`(예상한 거절) · 사람 경로도 422
- **AX 의 `confirm`·`reject`·`approve`** → `AX_DECISION_REFUSED` · 카드 그대로
- **이미 등록된 카드에 AX 수정** → `AX_DRAFT_SAVE_UNAVAILABLE`
- C-1 도메인 거절 사유 · 프로그램 오류는 그대로 「예상 못 한 실패」 · C-2 Codex 실패 사유

**계약이 바뀌어 고친 기존 시험 1**: `test_action_center.py::test_ax_drafts_refuse_only_what_new_task_creation_refuses`.
- 요청 초안을 `confirm` 하며 `draft={"title": …}` 만 보내 「담당자 없음 422」 를 보던 시험이다.
- 이제 안 보낸 칸은 「그대로」 라서, 담당자를 빼려면 `"assignee_id": null` 을 보내게 바꿨다(422 기대 그대로).

| 명령 | 파일 | 결과 |
|---|---|---|
| `make test-contract-serial FILES="…"` ① | `tests/architecture` · unit: `test_ax_work_lookup_policy.py` · `test_action_policy.py` · `test_codex_tool_summary.py` / contract: `test_e6_ax_draft_save_repro.py` · `test_action_center.py` · `test_mcp_action_items.py` · `test_unified_commands.py` · `test_mcp.py` · `test_mcp_command_result.py` · `test_meeting_creation_input.py` · `test_meeting_rooms.py` · `test_task_creation_contract.py` · `test_codex_cli.py` · `test_claude_cli.py` · `test_inbox_message_context.py` · `test_material_action_evidence.py` | **404 passed** · 0 failed |
| `make test-contract-serial FILES="…"` ② (초안·확인을 쓰는 나머지 contract 전부 — rg) | `test_action_material_command_tools.py` · `test_action_material_drafts.py` · `test_assignment_creation_input.py` · `test_batch_failure_receipts.py` · `test_browser_interactions.py` · `test_checklist_confirmation_contract.py` · `test_extended_confirmation.py` · `test_material_search.py` · `test_mcp_checklist.py` · `test_meeting_room_change.py` · `test_project_membership_follows_work.py` · `test_report_confirmation_contract.py` · `test_request_creation_input.py` · `test_request_revision_input.py` · `test_task_origin.py` · `test_task_transition_confirmation.py` · `test_task_update_contract.py` | **159 passed · 1 failed** → 실패 1건(`test_project_membership_follows_work.py::…old_project` — 프로젝트 생성 403)은 단독 실행 1 passed · 그 파일 재실행 **20 passed**. 병렬에서 한 번 흔들린 시험으로 본다(이번 변경과 무관한 프로젝트 생성 권한 경로) |
| `AX_POSTGRES_TEST_URL=… pytest -m integration -n0` | `test_postgres_extended_confirmation.py` · `test_inbox_message_origin_postgres.py` · `test_postgres_integration.py` | **51 passed** |

- 인벤토리: 도구 `action_item_command` 의 설명만 바뀌어 그 1항목을 패치했다(architecture 통과).

## 3. 남은 것 · 주의점

1. **확정(`confirm`)도 병합을 탄다** — 화면은 늘 전체 draft 를 보내 결과가 같다. 다만 확정 때 「칸을 빼서 비우기」 는 이제 안 된다 — 비우려면 `null`. 화면이 칸을 빼서 비우는 곳이 있는지 FE 확인 거리(시험상으로는 없음).
2. **화면의 「AX 가 고친 회차」 표지**: 기록은 감사 표에 있다. 회차 목록 응답(`rounds[]`)에 `edited_by` 를 내고 FE 가 표지를 다는 일은 하지 않았다 — 원하면 BE(응답 한 칸 · 인벤토리) + FE.
3. **AX 의 부분 draft 와 `base_submission_version`**: AX 는 `action_item_get` 의 지금 회차를 기준으로 보내야 한다. 사람이 그 사이 저장했으면 낡은 기준으로 거절되고, 사유가 C-1 로 가서 AX 가 다시 읽고 보낼 수 있다.
4. 실물 확인(코디 E2E): 운영과 같은 대화로 「참석자 추가해 줘」 → 같은 카드 2회차 · 실행 기록에 실패 없음.
