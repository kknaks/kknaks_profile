# 2루프 E-6 — AX 가 회의 생성 초안을 못 고친다 · **원인 확인 보고**

## 상태: 원인 확인 완료 · **구현하지 않음**(코디 지시 변경 — 방향은 사용자가 정한다)

- 워크트리: 제품 코드 변경 **없음**. 지시 변경 전에 고친 코드가 없어서 되돌릴 것도 없었다.
- 남긴 것: 재현 시험 `backend/tests/contract/test_e6_ax_draft_save_repro.py` 하나(새 파일 · 5 passed · **지금 동작을 고정**한다 — 고치면 기대가 바뀐다). `frontend/` 는 건드리지 않았다.
- 경로 약어: `B/` = `backend/src/ax_workspace/`

## ① 재현 방법

`make test-contract-serial FILES="tests/contract/test_e6_ax_draft_save_repro.py"`(또는 `uv run pytest … -n0`) — 운영과 같은 모양:

1. 대화 턴에서 AX 제안을 하나 세운다 — `meeting.reservation.create`(초안 1회차 · 카드의 `allowed_commands` 에 `save_draft` 있음). 비교용으로 `task.create_self` 도 하나 세운다.
2. **다른 대화 턴에 묶인**(`AX_MCP_CAUSATION_ID` = 그 턴의 execution id — 대화 워커가 MCP 에 거는 것과 같다) MCP 파사드로 `action_item_command(command="save_draft", expected_version=1, base_submission_version=1, draft=편집 계약 값 + 참석자 추가 · 시간 변경)` 을 부른다.
3. 결과:
   - **회의도 업무도** `McpDelegatedActionAccessDenied("AX 제안은 사람이 승인합니다")` 로 거절되고, 회차는 1 그대로다.
   - MCP 서버를 거쳐 부르면 `UnexpectedToolError("Error executing tool action_item_command")` — 모델이 받는 글자에 사유가 없다.
   - Codex 스트림에서 그 실패의 `error_summary` = 「실패: failed」.
   - 같은 초안을 **사람(HTTP `POST /api/action-items/{id}/commands/save_draft`)** 이 보내면 200 · 회차 2 · 참석자 반영 — 저장 경로 자체는 산다.

## ② 원인 (파일:줄)

| # | 원인 | 위치 |
|---|---|---|
| 1 | **위임 턴의 `action_item_command` 는 `ax.*` 항목에 어떤 명령도 못 한다.** `_propose_action_item_command` 는 위임 턴(`AX_MCP_CAUSATION_ID` 있음)에서 항목의 `kind` 가 `ax.` 로 시작하면 **명령 종류를 보지 않고** 막는다. 「AX 가 자기 제안을 승인하지 못하게」 하려는 문인데, 승인이 아닌 `save_draft`(새 회차 · 사람이 여전히 확정)까지 함께 막는다 | `B/entrypoints/mcp.py:460-461`(`if str(detail.get("kind", "")).startswith("ax."): raise McpDelegatedActionAccessDenied("AX 제안은 사람이 승인합니다")`) · 함수 `:444` · 호출 `:439`(`run_action_command`) |
| 2 | **거절 사유가 모델에 가지 않는다.** `McpDelegatedActionAccessDenied` 는 `RuntimeError` 다(`ToolError` 아님). MCP SDK 는 `ToolError` 가 아닌 예외를 「예상 못 한 실패」 로 보고 `UnexpectedToolError` 로 감싼다. 클라이언트에 가는 글자는 `Error executing tool action_item_command` 뿐이다(SDK `mcpserver/server.py:441` · `exceptions.py` 의 `UnexpectedToolError` 설명). 모델은 「무엇이 틀렸는지」 모른 채 같은 호출을 되풀이한다 — 운영 4회 | 예외 정의 `B/entrypoints/mcp.py:246` · 도구 `:1597`(`action_item_command` — 도메인 예외를 `ToolError` 로 바꾸는 자리가 없다. 같은 파일에서 바꾸는 곳은 자료 검색 `:1985-1989` 뿐) |
| 3 | **실행 rail 의 「실패: failed」.** Codex 가 실패한 `mcp_tool_call` 을 `status: failed` + `result.content` 로 넘기는데, 결과에 `isError`/`is_error` 표지가 없으면 결과 글자를 읽지 않는다. 그래서 `status` 글자(`failed`)로 요약한다. 설령 읽어도 ②의 글자(사유 없음)라 두 겹으로 가려진다 | `B/platform/codex_cli.py:807-820`(`carried = payload.get("isError") or payload.get("is_error")` `:816` → 없으면 `_summarize_tool_error(status)`) · `B/platform/tool_receipts.py:53-59`(`summarize_tool_error("failed")` → 「실패: failed」) |

**코디 가설(판정 `decide_ax_confirmation` 의 업무 모양 · 첨부 `"task"` 고정)은 원인이 아니다**:
- 요청이 그 자리까지 가지 않는다 — ②-1에서 먼저 막힌다.
- 같은 회의 draft(참석자 추가 · 시간 변경)를 HTTP 로 보내면 정규화(`B/platform/action_center.py:584` 이하) · 판정 · 회차 열기가 모두 통과한다(재현 ④).

## ③ 업무 경로와 갈라지는 지점

- **갈라지지 않는다.** 업무 초안(`task.create_self`)도 위임 턴의 `save_draft` 는 **같은 줄**(`mcp.py:460`)에서 같은 사유로 막힌다(재현 시험의 두 갈래가 같은 결과).
- E-6 이 「회의만의 문제」 로 보인 이유는 둘로 본다:
  - 운영에서 AX 가 기존 카드를 `save_draft` 로 고치려 한 첫 사례가 회의였다.
  - 업무는 보통 AX 가 새 턴에서 **새 제안(새 카드)** 을 내는 쪽으로 고쳐 왔다 — 코드상 기존 AX 카드를 고치는 다른 AX 경로는 없다.
- 사람 경로는 업무·회의 모두 산다: `DRAFT_SAVE_ACTION_TYPES` `B/modules/actions/policy.py:38`(셋 다 포함 · WP3) · HTTP `save_draft` → `action_center.normalize` `:574`.
- **고칠 때 함께 걸리는 것(지금은 가려져 있음)**:
  - **첨부 선택 유실**: `save_draft` 에 `draft` 만 주고 `attachment_draft_ids` 를 빼면 회차의 첨부 선택이 비워진다 — `action_center.py:626`(`attachment_source = (recovery_payload or {}).get("attachment_draft_ids")`). 사람 화면은 늘 함께 보내지만 AX 는 모를 수 있다.
  - **부분 draft**: 도구 설명은 「complete typed draft」 다(`B/modules/ax_execution/tool_catalog.py:292` — 그것도 `confirm` 만 말하고 `save_draft` 는 말하지 않는다). AX 가 바뀐 칸만 보내면 생성 모델 검증(제목·시각 필수)에서 실패한다.

## ④ 고칠 방향 후보 (정하지 않고 나열)

**A. AX 가 기존 초안을 고치는 길**

| 후보 | 내용 | 득 | 실 |
|---|---|---|---|
| A-1 | 위임 턴에서 `ax.*` 항목의 **`save_draft` 만** 통과(서버가 그 항목에 `save_draft` 를 열어 둔 경우만). `confirm`·`reject` 는 지금처럼 막는다 | 화면 [수정]→저장과 같은 결과 · 같은 카드에서 회차+1 · 사람이 여전히 확정 | AX 가 사람 확인 없이 카드 내용을 바꾼다(확정은 아님). 회차 기록에 「AX 가 저장」 이 남는지 정해야 한다 |
| A-2 | 위임 턴의 `save_draft` 를 지금의 다른 명령처럼 **확인 래퍼(`action_item.command` 제안)** 로 만든다 — 사람이 「이 수정 저장」 을 한 번 더 누른다 | 사람 문을 하나도 낮추지 않는다 | 카드가 둘(초안 + 「수정 저장」 래퍼) · 고치려다 확인을 두 번 누른다 |
| A-3 | `save_draft` 를 막은 채 두고, AX 정책·도구 설명이 「기존 카드를 고치지 말고 **새 제안**을 내라」 고 말한다. 서버가 같은 대화의 같은 종류 대기 카드를 새 제안으로 **대체**(옛 카드 닫기)할지도 함께 정한다 | 사람 문 그대로 | 회차 이력이 한 카드에 쌓이지 않는다. 대체 규칙이 새로 생긴다 |
| A-4 | AX 전용 「초안 수정」 도구(예: `ax_draft_revise(action_item_id, changes)`) — 서버가 지금 회차 값 위에 바뀐 칸만 겹쳐 새 회차를 연다(회의 수정 카드의 「바뀐 칸만」 규칙과 같은 모양) | 부분 draft · 첨부 유실 문제를 서버가 한 번에 푼다 · 도구 이름이 뜻을 말한다 | 새 도구 · 인벤토리 · 정책 문구 |

**B. A-1/A-2 를 고르면 함께 정할 것**
- B-1 부분 draft: 서버가 지금 회차 위에 겹치나(위임 경로만, 또는 모두), 아니면 「완전한 draft」 를 도구 설명·정책에 못 박나.
- B-2 첨부 선택: `attachment_draft_ids` 를 안 주면 지금 회차 것을 유지하나(위임 경로만, 또는 모두).

**C. 사유가 가려지지 않게(어느 A 를 골라도 필요)**
- C-1 MCP 의 `action_item_command`(또는 명령 도구 전반)가 도메인 예외(`McpDelegatedActionAccessDenied` · `ActionError` · `ActionCenterError` · 404 류 · 검증 오류)를 **`ToolError("<코드>: <한 줄>")`** 로 바꿔 낸다 → 모델이 사유를 읽고 같은 호출을 되풀이하지 않는다.
- C-2 Codex 요약: 실패한 `mcp_tool_call` 이면 `isError` 표지가 없어도 결과의 첫 글자 내용을 사유로 쓴다(`codex_cli.py:816`) → 실행 rail 에 「실패: AX 제안은 사람이 승인합니다」 류가 남는다. Claude 경로는 `tool_result.is_error` 를 이미 본다(`claude_cli.py:532-536`).
- C-3 거절 글자 자체: 「AX 제안은 사람이 승인합니다」 는 `save_draft` 에는 틀린 말이다 — 명령별 문구(예: 「AX 제안의 확정·거절은 사람이 합니다」 / A-3 이면 「기존 카드는 고치지 않고 새 제안을 내세요」).

## 검증

| 명령 | 파일 | 결과 |
|---|---|---|
| `uv run pytest tests/contract/test_e6_ax_draft_save_repro.py -n0` | 재현 시험(새) — 위임 `save_draft` 거절 ×2(회의·업무) · 모델이 받는 글자 · Codex 「실패: failed」 · 사람 HTTP 저장 성공 | **5 passed** |

- 제품 코드가 바뀌지 않아 다른 시험은 돌리지 않았다.
