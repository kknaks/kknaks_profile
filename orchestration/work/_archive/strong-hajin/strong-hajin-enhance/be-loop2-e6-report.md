# 2루프 E-6 — AX 초안 수정 = 옛 초안 닫고 새 초안 (사용자 결정 A-3) · 결과 보고

## 상태
- **확인 결과: 「대체됨」 은 기존 값으로 안 된다.** 새 상태값이 필요하다 → **대체형은 구현하지 않음**(지시대로 · 사용자 답 대기).
- **C(C-1·C-2·C-3)만 구현**(코디 답 「C만 지금 구현」).
- 커밋하지 않았다 · `frontend/` 는 건드리지 않았다.
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/`

## 1. 먼저 확인 — 테이블이 받는가

| 질문 | 답 | 근거 |
|---|---|---|
| ① 「대체됨/닫힘」 으로 쓸 기존 값이 있나 | **없다**(쓸 만한 것이 반쪽만 있다) | 아래 표 |
| ② 「같은 대화의 같은 종류 대기 초안」 을 찾을 수 있나 | **찾을 수 있다**(새 칸 없이) | `ActionItemRecord.turn_id` → `conversation_turns.conversation_id` · `action_type` · `state == "pending"` (`B/platform/persistence.py:810,815,819`) — WP4 출처 판정이 이미 같은 조인을 쓴다(`B/platform/actions.py` `_record_message_origin`) |
| ③ 새 상태값·칸·마이그레이션 | **새 상태값 1** — 마이그레이션은 불필요(아래) | |

**표마다 지금 값**

| 표·칸 | 지금 쓰는 값 | 「대체됨」 으로 쓸 수 있나 |
|---|---|---|
| `action_items.state` `String(40)` · CHECK 없음 | `pending` · `approved` · `rejected` 셋뿐 — `B/platform/actions.py:287`(생성) · `:483`(판단) | **없다.** `rejected` 로 닫으면 사람이 안 한 거절이 된다 |
| `decision_items.status` `String(30)` | `open` · `resolved`(`B/platform/action_center.py:915` · `actions.py:540`) | `resolved` 는 「끝났다」 일 뿐 — 쓸 수 있으나 이유를 말하지 않는다 |
| `review_assignments.status` / `resolution_kind` | `pending` · `decided` · **`superseded`**(+`resolution_kind="revised"` — 사람이 고쳐 다음 회차를 열 때 앞 배정을 닫는 값 · `action_center.py:956-957`) · `cancelled` · `declined` | **배정 쪽에는 `superseded` 가 이미 있다.** 다만 같은 카드 안의 「다음 회차」 뜻이고, 카드(제안) 자체의 상태가 아니다 |
| `review_decisions` | 사람의 확정·거절 기록(`actor_member_id` 필수) | 쓰면 안 된다 — 아무도 판단하지 않았다 |

**화면이 그 상태를 어떻게 그리나**
- 응답의 카드 상태는 `awaiting_review` · `resolved` 둘뿐이다(`B/platform/action_center.py:750` · `B/modules/actions/domain.py:20,24`).
- 화면 카드의 `state` 타입은 `"pending" | "approved" | "rejected"` 셋이다(`F/lib/viewModels.ts:773` · `F/features/action/AxDraftCard.tsx:68`).
- 화면은 「`resolved` 인데 만들어진 업무가 없으면 `rejected`」 로 읽고(`AxDraftCard.tsx:125`) 「거절됨」 표지를 단다(`:489`). 회의 수정 카드도 같다(`ActionMeetingUpdateCard.tsx:199`).
- **기존 값으로 닫으면 옛 카드는 「거절됨」 으로 보인다.** 카드가 사라지지는 않는다(대기 목록에서는 빠진다 — `pending=false`).

**충실하게 하려면 필요한 것(사용자 판단 거리)**

| 몫 | 내용 |
|---|---|
| BE 상태값 | `action_items.state = "superseded"`. CHECK 가 없어 **마이그레이션은 불필요**. 같은 트랜잭션에서 `decision_items.status="resolved"` · 대기 배정 `status="superseded"`·`resolution_kind="replaced"`(기존 값 재사용 + 새 resolution 글자 하나)로 닫는다. 판단 기록(`review_decisions`)은 남기지 않는다. 대체한 새 제안 id 는 기존 JSON 칸 `action_items.result` 에 `{"superseded_by": "<새 id>"}` 로 남긴다(새 칸 없음) |
| BE 응답 | 카드 `status` 가 `resolved` 인 채 이유를 실을 자리 — 예: `state="superseded"` 를 그대로 내고 `superseded_by_action_id` 를 더한다(응답 모양이 바뀌므로 인벤토리 drift 패치). 대화 응답의 `actions[].state` 에도 같은 값 |
| BE 정책 | 정책·도구 설명에 「고치라고 하면 고친 **전체** 내용으로 새 초안」(체크리스트 100개면 줄인 결과 전체) |
| **FE 몫** | 카드 `state` 타입에 `"superseded"` 를 더하고 「새 초안으로 대체됨」 표지(라벨 · `labels.ts`). `AxDraftCard.tsx:125` 의 「업무 없으면 rejected」 추론이 `superseded` 를 먼저 보게 한다. 회의 생성·업무·요청 카드 모두 |
| 대안(상태값 없이) | `rejected` 로 닫고 `result.superseded_by` 로 FE 가 「대체됨」 을 그린다 — 상태 글자는 「거절」 로 남아 다른 화면·통계가 거절로 센다. **권하지 않는다** |

## 2. 구현 — C 전부

| # | 고친 것 | 위치 |
|---|---|---|
| **C-3** 명령별 거절 문구 | 위임 턴의 `ax.*` 항목은 지금처럼 막는다(`save_draft` 포함 — 고치는 길은 새 제안). 문구와 코드가 명령에 맞는다:<br>— `save_draft` → **`AX_DRAFT_EDIT_REFUSED`** 「기존 초안은 고치지 않고 새 초안을 내세요 — 고친 전체 내용으로 같은 생성 도구를 다시 부르면 사람이 새 카드를 확인합니다」<br>— `confirm`·`reject`·`approve` 등 → **`AX_DECISION_REFUSED`** 「AX 제안의 등록(확정)·거절은 사람이 합니다 — 카드에서 사람이 고르게 두세요」<br>예외 `McpDelegatedActionAccessDenied` 에 `code` 를 실었다 | `B/entrypoints/mcp.py:248`(예외) · `:257,261`(문구) · `:506`(고르는 자리) |
| **C-1** 도메인 예외 → `ToolError("<코드>: <한 줄>")` | `action_item_command` 도구가 **예상한 거절**을 모델이 읽는 `ToolError` 로 바꾼다 — `anticipated_tool_error`:<br>— 도메인 모듈(`ax_workspace.modules.*`)의 예외 · 위임 거절 · `ResourceNotFound` · 입력 검증(`INVALID_INPUT` + 칸 이름)이 대상이다<br>— 코드 = 예외의 `code`/`reason`, 없으면 404 류 `NOT_FOUND`, 그것도 없으면 클래스 이름(`ACTION_CAPABILITY_DENIED` 식)<br>— 한 줄 = 메시지 200자<br>**프로그램 오류(그 밖의 예외)는 그대로 「예상 못 한 실패」**(서버가 traceback 을 남긴다).<br>모델이 받는 글자: `Error executing tool action_item_command: AX_DRAFT_EDIT_REFUSED: 기존 초안은 …` — 머리는 MCP SDK 가 붙인다 | `B/entrypoints/mcp.py:265`(`_error_code`) · `:275`(`anticipated_tool_error`) · `:1666`(도구) |
| **C-2** Codex 실행 기록 사유 | 실패한 `mcp_tool_call` 의 결과에 `isError` 표지가 없어도(Codex 가 실패를 `status` 로 옮긴 경우) **결과의 글자 조각**을 사유로 쓴다 → `error_summary` = 「실패: AX_DRAFT_EDIT_REFUSED: …」(80자). 구조화 결과(정상 결과 모양)는 사유 자리에 쓰지 않는다. 글자가 정말 없을 때만 「실패: failed」. Claude 경로는 `tool_result.is_error` 를 이미 본다(변경 없음) | `B/platform/codex_cli.py:816-832` |

- 도구 설명(`tool_catalog`)·HTTP·MCP 시그니처는 바꾸지 않았다 → 인벤토리 변경 없음(architecture 통과).
- **C-1 범위**: 이번에는 `action_item_command` 하나에 걸었다(E-6 의 도구). `anticipated_tool_error` 는 모듈 함수라 다른 명령 도구에도 같은 줄로 걸 수 있다 — 넓힐지는 코디 판정 거리.

## 3. 시험

재현 시험 `backend/tests/contract/test_e6_ax_draft_save_repro.py` 를 새 동작에 맞게 고쳤다(9). 다루는 것:
- 위임 `save_draft` 거절 = 회의·업무 둘 다 `AX_DRAFT_EDIT_REFUSED` + 「새 초안을 내세요」 · 회차 1 그대로
- 위임 `confirm`·`reject`·`approve` = `AX_DECISION_REFUSED`
- MCP 를 거친 모델 글자에 코드·사유가 있다(`UnexpectedToolError` 아님)
- 위임 밖 도메인 거절(낡은 판)도 코드·한 줄 · 프로그램 오류(`KeyError`)는 여전히 `UnexpectedToolError`
- Codex 실패 결과: 표지 없음 → 사유 · 표지 있음 → 같은 사유 · 글자 없음 → 「실패: failed」
- 사람 HTTP `save_draft` 는 회의 초안 회차 2(그대로)

| 명령 | 파일 | 결과 |
|---|---|---|
| `make test-contract-serial FILES="…"` | `tests/architecture` · `tests/unit/test_codex_tool_summary.py` · `tests/unit/test_codex_stream_adapter.py` · contract: `test_e6_ax_draft_save_repro.py` · `test_mcp_action_items.py`(기존 「사람」 거절 시험 통과 — 새 문구에도 「사람」) · `test_mcp.py` · `test_mcp_command_result.py` · `test_codex_stream_ingest.py` · `test_codex_cli.py` · `test_unified_commands.py` · `test_action_center.py` | **214 passed** · 0 failed |

## 4. 남은 것 (사용자 답 뒤)

- 대체형(A-3 본체) — §1 「충실하게 하려면」 의 BE 넷 + FE 몫.
- 대체형 없이 지금 AX 가 새 초안을 내면 **옛 카드는 대기로 남는다**(카드 둘).
  - C-3 문구가 AX 에게 「새 초안을 내라」 고 하므로, 대체가 들어오기 전에는 사용자가 옛 카드를 직접 거절해야 한다.
  - 대체형 답이 늦어지면 문구에서 「새 초안을 내세요」 를 빼는 선택지도 있다 — 코디 판정 거리.
