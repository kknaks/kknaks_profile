---
type: concept
id: tool-allowlist-by-phase
title: 단계별 도구 허용 목록 (Tool Allowlist by Phase)
aliases:
  - enabled_tools
  - 도구 잠금은 설정으로
  - MCP allow list
up:
  - 2026-09-08-docs-v1
tags:
  - agent
  - mcp
  - codex
  - prompt
---

# 단계별 도구 허용 목록

에이전트가 「무엇을 볼 수 있나」는 프롬프트 문장이 아니라 **도구 목록 자체**로 고정한다. 같은 세션이라도 제출 단계마다 열리는 도구 집합을 다르게 준다 — 회의 중 배치에는 업무 참조용 셋, 종료 후 최종에는 일곱.

## 정의

1. 도구 서버(MCP)는 도구를 전부 노출한다. 잠그는 손은 **클라이언트 실행 옵션**(`-c mcp_servers.<n>.enabled_tools=[…]` + 도구별 `approval_mode`)이다.
2. 옵션 빌더는 `phase` 를 **기본값 없는** 인자로 받는다. 새 호출부가 생기면 어느 단계인지 반드시 고르게 된다.
3. 세션을 이어 쓰는 `resume` 에도 `-c` 가 살아 매 제출마다 목록이 다시 걸린다. 첫 제출(웜스타트)의 목록은 「알려 주는 자리」일 뿐 실제 잠금은 매 제출이 한다.
4. 프롬프트에서는 조회 순서 지시를 지운다 — 없는 도구를 부르라고 적어 두면 모델이 「도구를 못 찾겠다」고 흔들린다.

## 사용 예시

```python
_TOOLS_BY_PHASE = {
    "batch": ("list_tasks", "get_task", "list_work_types"),
    "final": ("list_agendas", "get_agenda", "get_meeting", "get_account", "list_tasks", "get_task", "list_work_types"),
}
def build_codex_options(*, session_id, output_schema, timeout_sec, meeting_token, phase: Literal["batch", "final"]): ...
```

## 왜 중요한가

실물 회의에서 AI 요약이 사람 노트의 톤을 그대로 따라갔다. 원인은 AI 가 `list_agendas`·`get_agenda` 로 사람 안건·줄을 읽고 미러 안건을 만드는 설계였다. 「보지 마라」는 프롬프트 지시는 모델이 어길 수 있지만, 도구가 없으면 물리적으로 못 본다. 「두 사람이 각자 쓰고 최종에 합친다」는 개념을 설정 한 줄로 강제할 수 있었다.

## 경계와 오해

- **프롬프트 지시 ≠ 잠금** — 지시는 확률이고 도구 목록은 사실이다. 정책은 목록에, 설명은 프롬프트에.
- **서버에서 잠그지 않는다** — MCP 서버가 단계를 알게 하면 서버가 세션 상태를 들고 있어야 한다. 클라이언트 옵션이 더 단순하다.
- **웜스타트의 목록은 결정이 필요한 자리** — 실제 잠금과 무관하지만, 프롬프트에 「쓸 수 있는 도구」를 적는다면 그 자리의 목록과 어긋나지 않게.

## 함께 보는 개념

- [[strict-json-schema-output]] — 같은 `-c` 옵션에 실리는 출력 스키마
- [[resource-scoped-token]] — 도구가 REST 를 부를 때 쓰는 토큰

## 출처

- 코드: `app/back/integrations/agent.py` `_TOOLS_BY_PHASE` · 커밋 `1ca243e`(kknaks/task_management)
- 결정: `reference/2026-09-06-task-management-app/Meeting flow.md` MF-71 · SPEC-007 v0.0.3 §4 도구 표
