"""P1 — 제출 조립과 시스템 프롬프트. SPEC-005 AC-보조 2 · WORK-003 P1 검증.

제출 옵션은 **큐 없이** 단언한다(순수 함수). 프롬프트 검사는 S-001 의 검증 명제를
지키는 자리다 — 관계 지식이 프롬프트로 새면 「도구로만 답한다」가 증명되지 않는다.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from agent import prompt as prompt_mod
from agent.submission import (
    TOOL_ALLOWLIST,
    build_config_overrides,
    build_submission,
    redact_config_overrides,
)
from config import settings

APP = Path(__file__).resolve().parents[1]


# --- 제출 옵션 ---------------------------------------------------------------


def test_도구_allowlist_가_SPEC_002_4종_그대로다():
    assert TOOL_ALLOWLIST == ("query_kpi", "query_layer", "trace_ontology", "get_definition")


def test_승인_축이_둘이고_per_tool_approve_가_실린다():
    """`approval_policy="never"` 는 「안 물어보고 **실패 처리**」이지 허용이 아니다.

    허용은 `tools.<name>.approval_mode="approve"` 다. 이 둘을 헷갈리면 MCP 툴 호출이
    「user cancelled」로 죽는다 — 조사 리포트 §3.2 의 실측 함정.
    """
    overrides = build_config_overrides(
        mcp_url="http://ontology-mcp:28081/mcp", server_key="ontology", effort="low")

    assert 'approval_policy="never"' in overrides
    for name in TOOL_ALLOWLIST:
        assert f'mcp_servers.ontology.tools.{name}.approval_mode="approve"' in overrides
    # 서버 기본으로 걸지 않는다 — 나중에 도구가 늘면 그것까지 자동으로 열린다
    assert not any(
        line.startswith("mcp_servers.ontology.approval_mode") for line in overrides)


def test_codex_가_스스로_붙이는_표면을_끈다():
    """`features.apps=false` 가 없으면 allowlist 로 못 막는 MCP surface 가 붙는다."""
    overrides = build_config_overrides(
        mcp_url="http://x/mcp", server_key="ontology", effort="low")
    assert "features.apps=false" in overrides
    assert "features.shell_tool=false" in overrides
    assert 'web_search="disabled"' in overrides
    assert "features.image_generation=false" in overrides


def test_enabled_tools_가_비지_않는다():
    """빈 배열이면 그 서버 툴이 하나도 안 열린다 — fail-closed 계약이다."""
    overrides = build_config_overrides(
        mcp_url="http://x/mcp", server_key="ontology", effort="low")
    line = next(x for x in overrides if x.startswith("mcp_servers.ontology.enabled_tools="))
    assert line == (
        'mcp_servers.ontology.enabled_tools=["query_kpi", "query_layer", '
        '"trace_ontology", "get_definition"]')


def test_server_key_가_url_과_allowlist_에서_같다():
    """갈리면 에러가 아니라 **조용히 툴 0개**다(조사 리포트 §5.6-2)."""
    overrides = build_config_overrides(
        mcp_url="http://x/mcp", server_key="mykey", effort="low")
    keys = {m.group(1) for line in overrides
            if (m := re.match(r"mcp_servers\.([A-Za-z0-9_]+)\.", line))}
    assert keys == {"mykey"}


def test_제출_계획이_모델_큐_상한_sandbox_를_싣는다():
    plan = build_submission(prompt="질문", conversation_id="c1", message_id="m1")

    assert plan.provider == "codex"
    assert plan.queue == settings.ai_queue == "ontology"
    assert plan.model == "gpt-5.6-terra"
    assert plan.options["timeout_sec"] == 180
    assert plan.provider_options["sandbox"] == "read-only"
    # resume 에도 반드시 — 없으면 「Not inside a trusted directory」로 막힌다
    assert plan.provider_options["skip_git_repo_check"] is True
    assert plan.metadata == {"ontology_conversation_id": "c1", "ontology_message_id": "m1"}
    assert "resume" not in plan.options


def test_모델과_effort_가_레퍼런스_실측_조합이다():
    """`gpt-5.6-terra` + `low` — 조사 리포트 §5.6-3. `none` 은 툴 연결 판단이 죽는다."""
    assert settings.ai_model == "gpt-5.6-terra"
    assert settings.ai_reasoning_effort == "low"
    overrides = build_config_overrides(
        mcp_url="http://x/mcp", server_key="ontology",
        effort=settings.ai_reasoning_effort)
    assert "model_reasoning_effort=low" in overrides


def test_세션이_있으면_resume_가_실린다():
    plan = build_submission(prompt="질문", resume_session_id="sess-1")
    assert plan.options["resume"] == {"mode": "session", "session_id": "sess-1"}


def test_빈_모델은_None_으로_나간다(monkeypatch):
    """`""` 를 넘기면 `codex exec --model ""` 이 된다."""
    monkeypatch.setattr(settings, "ai_model", "")
    assert build_submission(prompt="q").model is None


def test_로그_위생_함수가_헤더_줄을_가린다():
    redacted = redact_config_overrides([
        'mcp_servers.ontology.url="http://x/mcp"',
        'mcp_servers.ontology.http_headers={Authorization="Bearer secret-token"}',
    ])
    assert "secret-token" not in " ".join(redacted)
    assert redacted[0].startswith("mcp_servers.ontology.url=")


# --- S-001 · ADR-04 ----------------------------------------------------------

#: 프롬프트에 있으면 안 되는 것 — 노드 id · 판정 · 관계 서술 · 계산식.
#: 하나라도 새면 「관계 지식 없이 답한다」는 검증 명제가 무효가 된다.
_BANNED_IN_PROMPT = (
    "sales_total", "cancel_rate", "reservations", "noshow_rate", "new_patients",
    "gu_reviews", "naver_reviews", "payment_visits", "promo_event", "avg_ticket",
    "채택", "자동 확정", "기각", "보류", "선언",
    "취소율", "노쇼율", "객단가", "신환", "재진", "결제 내원", "매출",
    "부도 ÷", "→",
)


@pytest.mark.parametrize("needle", _BANNED_IN_PROMPT)
def test_AC보조2_시스템_프롬프트에_관계_도메인_지식이_없다(needle):
    assert needle not in prompt_mod.SYSTEM_PROMPT, (
        f"프롬프트에 도메인·관계 문자열이 있다: {needle!r} — "
        "관계는 trace_ontology 가, 계산식은 get_definition 이 준다(S-001)")


def test_프롬프트가_도구_이름과_형식_지시는_담는다():
    """금지는 관계 지식이지 도구 사용 규칙이 아니다 — 빈 프롬프트로 통과하면 안 된다."""
    for tool in TOOL_ALLOWLIST:
        assert tool in prompt_mod.SYSTEM_PROMPT
    for field in ("used_edges", "citations", "premise_correction", "excluded_edges"):
        assert field in prompt_mod.SYSTEM_PROMPT


def test_프롬프트_블록_순서가_시스템_질문_이다():
    built = prompt_mod.build_prompt("최근 4주 노쇼율 추이는?")
    assert built.startswith(prompt_mod.SYSTEM_PROMPT)
    assert built.endswith("최근 4주 노쇼율 추이는?")
    assert "\n\n---\n\n" in built


def test_ADR04_LLM_SDK_직접_import_가_0건이다():
    """실행은 open-kknaks 경유다 — SDK 를 직접 붙이지 않는다."""
    banned = {"anthropic", "openai", "google.generativeai", "cohere", "mistralai"}
    offenders: list[str] = []
    for path in sorted(APP.rglob("*.py")):
        if "__pycache__" in path.parts or ".venv" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                if name.split(".")[0] in banned:
                    offenders.append(f"{path.name}:{node.lineno} {name}")
    assert offenders == [], f"LLM SDK 직접 import: {offenders}"


def test_open_kknaks_는_lazy_import_다():
    """의존 미설치 환경에서도 모듈이 로드돼야 한다 — 단위 테스트가 큐 없이 돈다."""
    source = (APP / "agent" / "runtime.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    top_level = {
        a.name for node in tree.body if isinstance(node, ast.Import) for a in node.names
    } | {
        node.module for node in tree.body if isinstance(node, ast.ImportFrom)
    }
    assert "open_kknaks" not in top_level
    assert "from open_kknaks import" in source     # 함수 안에는 있다
