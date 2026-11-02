"""제출 계약 — ontology-agent → open-kknaks(codex).

**조립만 한다.** 제출은 `runtime.py` 가 하고 여기는 순수 함수로 둬서 큐 없이 테스트가 닫힌다.

## 승인 축이 둘이라는 것이 이 파일의 핵심 함정

- `approval_policy="never"` 는 「안 물어보고 **실패 처리**」이지 허용이 아니다.
  비대화(exec)에서 MCP 툴 호출이 「user cancelled」로 죽던 원인이 이것이다.
- 허용하는 축은 **`mcp_servers.<key>.tools.<tool>.approval_mode="approve"`** 다.
  우선순위는 툴별 > 서버 기본 > auto. **툴별로 거는 이유**: 서버 기본으로 걸면 나중에
  도구가 늘 때 그것까지 자동으로 열린다.

## `features.apps=false` 가 필요한 이유

codex 가 **우리가 설정하지 않은** MCP surface 를 붙인다(레퍼런스 실측 `mcp__codex_apps__`
27종). allowlist 는 우리 서버만 가리키므로 그 밖의 surface 를 아예 못 막는다.

## 손을 MCP 넷으로 좁힌다

`features.shell_tool=false` + `web_search="disabled"` + `features.apps=false` +
`sandbox="read-only"`. 쉘이 없으니 인젝션이 부릴 손이 도구 4종뿐이다.

⚠ `enabled_tools` 가 **빈 배열이면 그 서버 툴이 하나도 안 열린다** — 버그가 아니라
fail-closed 계약이다.
⚠ `mcp_server_key` 는 `-c mcp_servers.<key>` 와 allowlist 표기 **두 곳이 같아야** 한다.
   갈리면 에러가 아니라 **조용히 툴 0개**다 — env 하나(`ONTOLOGY_MCP_SERVER_KEY`)가 SoT 다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config import settings

#: 파일을 쓰지 않는다 — 일은 MCP 도구로만 한다. 신규·resume 공통 단일값.
_SANDBOX = "read-only"

#: MCP 툴 승인 모드. `approval_policy` 를 대체하는 정식 손잡이다(위 머리 주석).
_MCP_APPROVAL_MODE = "approve"

#: 이 에이전트가 부를 수 있는 도구 전부 — SPEC-002 의 4종이 그대로다.
#: **여기 없는 이름은 열리지 않는다**(fail-closed). MCP 서버가 도구를 늘려도
#: 이 목록에 적기 전까지는 codex 에 보이지 않는다.
TOOL_ALLOWLIST: tuple[str, ...] = (
    "query_kpi",
    "query_layer",
    "trace_ontology",
    "get_definition",
)


@dataclass(frozen=True)
class SubmissionPlan:
    """`AgentClient.submit()` 에 그대로 펼칠 인자 묶음."""

    prompt: str
    queue: str
    provider: str
    provider_options: dict[str, Any]
    options: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    #: 빈 값이면 **None** 이어야 한다 — `""` 를 넘기면 `codex exec --model ""` 이 된다.
    model: str | None = None


def build_config_overrides(
    *, mcp_url: str, server_key: str, effort: str,
    tools: tuple[str, ...] = TOOL_ALLOWLIST,
) -> list[str]:
    """반복 `-c` 오버라이드 — 태스크별 설정 **파일이 없다**.

    값은 TOML 로 파싱되므로 문자열은 따옴표로 감싼다.
    """
    tools_toml = "[" + ", ".join(f'"{name}"' for name in tools) + "]"
    overrides = [
        f"model_reasoning_effort={effort}",
        # 승인 «요청» 축은 끈다 — headless 라 물어볼 사람이 없다.
        # 실제 «허용» 은 아래 per-tool approval_mode 가 준다(둘은 다른 축이다).
        'approval_policy="never"',
        f'mcp_servers.{server_key}.url="{mcp_url}"',
        f"mcp_servers.{server_key}.enabled_tools={tools_toml}",
    ]
    # 툴별 승인 — 서버 기본으로 걸지 않는다(나중에 도구가 늘면 자동으로 열린다)
    overrides += [
        f'mcp_servers.{server_key}.tools.{name}.approval_mode="{_MCP_APPROVAL_MODE}"'
        for name in tools
    ]
    overrides += [
        "features.shell_tool=false",
        'web_search="disabled"',
        "features.image_generation=false",
        # codex 가 스스로 붙이는 MCP surface 를 끈다 — allowlist 로는 못 막는다
        "features.apps=false",
    ]
    return overrides


def build_submission(
    *,
    prompt: str,
    resume_session_id: str | None = None,
    conversation_id: str | None = None,
    message_id: str | None = None,
) -> SubmissionPlan:
    """제출 한 벌. 큐·모델·상한·allowlist 를 **한 곳에서** 조립한다."""
    overrides = build_config_overrides(
        mcp_url=settings.mcp_url,
        server_key=settings.mcp_server_key,
        effort=settings.ai_reasoning_effort,
    )
    options: dict[str, Any] = {"timeout_sec": settings.ai_timeout_sec}
    if resume_session_id:
        # 대화 하나 = 세션 하나. 다른 대화의 세션 id 가 여기 실릴 경로를 만들지 않는다.
        options["resume"] = {"mode": "session", "session_id": resume_session_id}

    return SubmissionPlan(
        prompt=prompt,
        queue=settings.ai_queue,
        provider=settings.ai_provider,
        model=settings.ai_model or None,
        provider_options={
            "sandbox": _SANDBOX,
            # resume 에도 반드시 — 없으면 「Not inside a trusted directory」로 막힌다
            "skip_git_repo_check": True,
            "config": overrides,
        },
        options=options,
        # 관측용 — 브로커에 남아 「이 태스크가 어느 대화/메시지인가」를 되짚게 한다
        metadata={
            "ontology_conversation_id": conversation_id,
            "ontology_message_id": message_id,
        },
    )


def redact_config_overrides(overrides: list[str]) -> list[str]:
    """로그 위생 — 헤더 줄에 토큰이 실릴 수 있다.

    지금 우리 MCP 는 토큰을 받지 않아 `http_headers` 를 안 싣지만, 배포에서 붙는 순간
    이 함수가 없으면 Bearer 원문이 로그로 나간다. 미리 둔다.
    """
    return [
        "<redacted>" if line.startswith(("mcp_servers.",)) and "http_headers" in line else line
        for line in overrides
    ]
