"""제출 계약 — back → open-kknaks (SPEC-017 §5 · DEC-027 D5).

조립만 한다. 제출은 `runtime.py` 가 하고, 여기는 **테스트가 닫히게** 순수 함수로 둔다.

## 기존 파이프라인과 섞이지 않는다

`service/ai_service.py` 의 `_build_run_options` 는 **자료 캡처 파이프라인의 계약**이다 —
`sandbox="danger-full-access"` 에 `/ledger` 마운트. 입력이 owner 라 성립하는 값이다.
채팅은 **익명 방문자의 입력**이 들어오므로 그 옵션을 재사용할 수 없다. 그래서 이 파일이
따로 있고, 저쪽은 한 줄도 건드리지 않는다.

## 모델 표기 (DEC-027 OQ-5, 레퍼런스 실측)

⚠ 유효한 값은 계정 모델 피커의 **정식 표기**뿐이다(`gpt-5.6-terra`). 축약형(`terra`)은
metadata 조회 실패로 **400** 이 나는데, 에러 문구가 «ChatGPT account 에서 지원 안 함» 이라
인증 문제로 읽힌다 — 아니다. 같은 인증에서 정식 표기는 정상 동작한다.

⚠ 모델과 `model_reasoning_effort` 는 **짝**이다. 허용 effort 목록이 CLI 가 아니라 모델별로
갈린다 — 모델을 바꾸면 effort 도 그 모델이 받는 값인지 다시 잰다.

## resume 이 못 받는 옵션

`codex exec resume` 은 `--sandbox`·`--cd` 를 안 받는다. 그런데 open-kknaks 어댑터가
`CODEX_RESUME_UNSUPPORTED_OPTIONS` 로 제출 전에 그 키를 **먼저 떨궈** 준다(설치본 확인).
그래서 앱은 신규·resume 에 **같은 값**을 넘기고, 분기는 어댑터 한 곳이 소유한다.

`skip_git_repo_check` 는 resume 에도 반드시 실어야 한다 — 없으면 「Not inside a trusted
directory」로 막힌다.

## 손을 MCP 하나로 좁힌다 (D5)

`features.shell_tool=false` + `web_search="disabled"` + `features.apps=false` +
`sandbox="read-only"`. 쉘이 없으니 컨테이너 bwrap 문제 자체가 없고(파이프라인 워커가
겪은 그 사고), 인젝션이 부릴 손이 MCP tool 뿐이다.

⚠ `features.apps=false` 가 필요한 이유: codex 가 **우리가 설정하지 않은** MCP surface 를
붙인다(레퍼런스 실측에서 `mcp__codex_apps__` 27종). allowlist 는 우리 서버만 가리키므로
그 밖의 surface 를 막지 못한다.

⚠ 승인 축은 둘이 **다르다**. `approval_policy="never"` 는 「안 물어보고 **실패 처리**」이지
허용이 아니다. 허용은 `mcp_servers.<id>.tools.<tool>.approval_mode="approve"` 다.
툴별로 거는 이유 = 서버 기본으로 걸면 나중에 tool 이 늘 때 그것까지 자동으로 열린다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config import get_settings

#: 파일을 쓰지 않는다 — 일은 MCP tool 로만 한다. 신규·resume 공통 단일값이다.
_SANDBOX = "read-only"

#: MCP 툴 승인 모드. bypass 를 대체하는 정식 손잡이다(위 머리 주석).
_MCP_APPROVAL_MODE = "approve"

#: 이 채팅이 부를 수 있는 tool 전부 — SPEC-017 §4 Tool Contract 의 열 줄이 그대로다.
#: **여기 없는 이름은 열리지 않는다**(fail-closed). MCP 서버가 tool 을 하나 늘려도
#: 이 목록에 적기 전까지는 codex 에 보이지 않는다.
TOOL_ALLOWLIST: tuple[str, ...] = (
    "get_profile",
    "list_career",
    "get_career",
    "list_projects",
    "get_project",
    "list_problems",
    "get_problem",
    # 회사 제품 — `list_projects`(개인)와 **다른 표·다른 tool** 이다(spec v0.0.8).
    "list_company_products",
    "get_company_product",
    "search_notes",
    "get_note",
    "list_contents",
    "list_algorithms",
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
    *, mcp_token: str, mcp_url: str, server_key: str, effort: str
) -> list[str]:
    """반복 `-c` 오버라이드 — 태스크별 설정 **파일이 없다**.

    값은 TOML 로 파싱되므로 문자열은 따옴표로 감싼다. 토큰은 프로세스 인자로만 흐르고
    디스크에 남지 않는다.
    """
    tools_toml = "[" + ", ".join(f'"{name}"' for name in TOOL_ALLOWLIST) + "]"
    overrides = [
        f"model_reasoning_effort={effort}",
        # 승인 «요청» 축은 끈다 — headless 라 물어볼 사람이 없다. 실제 허용은 아래
        # per-tool approval_mode 가 준다(둘은 다른 축이다).
        'approval_policy="never"',
        f'mcp_servers.{server_key}.url="{mcp_url}"',
        f'mcp_servers.{server_key}.http_headers={{Authorization="Bearer {mcp_token}"}}',
        f"mcp_servers.{server_key}.enabled_tools={tools_toml}",
    ]
    overrides += [
        f'mcp_servers.{server_key}.tools.{name}.approval_mode="{_MCP_APPROVAL_MODE}"'
        for name in TOOL_ALLOWLIST
    ]
    overrides += [
        "features.shell_tool=false",
        'web_search="disabled"',
        "features.apps=false",
    ]
    return overrides


def build_submission(
    *,
    system_prompt: str,
    question_block: str,
    mcp_token: str,
    recent_context: str = "",
    resume_session_id: str | None = None,
    conversation_id: int | None = None,
    message_id: int | None = None,
) -> SubmissionPlan:
    """제출 한 벌.

    시스템 프롬프트를 `provider_options.system_prompt` 가 아니라 **프롬프트 본문 앞에
    붙이는** 이유 = codex 어댑터가 그 provider option 을 지원하지 않아 제출 자체가
    거부되기 때문이다(허용 목록에 없다). 계약이 요구하는 것은 「함께 싣는다」이고
    전달 수단은 코드가 정한다.

    지난 기록은 **시스템 프롬프트 아래·질문 위**에 온다 — 「그거 말인데요」의 「그거」가
    질문 바로 앞에 있어야 한다. 없으면 그 자리는 아예 비어 있다(「기록 없음」 같은
    문장을 넣지 않는다).
    """
    settings = get_settings()
    blocks = [system_prompt]
    if recent_context:
        blocks.append(recent_context)
    blocks.append(question_block)

    overrides = build_config_overrides(
        mcp_token=mcp_token,
        mcp_url=settings.chat_mcp_url,
        server_key=settings.chat_mcp_server_key,
        effort=settings.chat_reasoning_effort,
    )

    options: dict[str, Any] = {"timeout_sec": settings.chat_timeout_sec}
    if resume_session_id:
        # 대화 하나 = 세션 하나. 다른 대화의 세션 id 가 여기 실릴 경로를 만들지 않는다.
        options["resume"] = {"mode": "session", "session_id": resume_session_id}

    return SubmissionPlan(
        prompt="\n\n---\n\n".join(blocks),
        queue=settings.chat_queue,
        provider="codex",
        model=settings.chat_model or None,
        provider_options={
            "sandbox": _SANDBOX,
            # resume 에도 반드시 — 없으면 trusted-directory 검사에 막힌다.
            "skip_git_repo_check": True,
            "config": overrides,
        },
        options=options,
        # 관측용 — 브로커에 남아 「이 태스크가 어느 대화/메시지인가」를 되짚게 한다.
        metadata={
            "chat_conversation_id": conversation_id,
            "chat_message_id": message_id,
        },
    )
