"""교안 형식이 한 곳에서만 정의되는지 (KDEV-WORK-015 P3 보정).

교안을 만드는 경로가 둘이다 — 승인 게이트의 `derived` 스테이지와 기존 `content_enrich`
잡. 처음에는 8개 섹션 명세를 **양쪽 프롬프트에 각각 적었는데**, 그건 `reference`·
`concept` 에서 없앤 이중 SoT 를 교안에서 다시 만드는 것이었다. 한쪽만 고치는 날 두
경로의 산출물이 조용히 갈라진다.

이 파일은 그 재발을 막는다 — **템플릿을 고치면 양쪽 프롬프트가 함께 바뀌어야 한다.**
"""

from __future__ import annotations

from pathlib import Path

import pytest

import config
from service.content_format import FALLBACK, TEMPLATE_PATH, content_format, reset_cache

SECTIONS = (
    "## 개요",
    "## 배경 / 사전 지식",
    "## 핵심 개념",
    "## 작동 원리",
    "## 코드 예시",
    "## 함정·실수",
    "## 베스트 프랙티스",
    "## 참고",
)


@pytest.fixture(autouse=True)
def _fresh_cache():
    reset_cache()
    yield
    reset_cache()


def _enrich_prompt() -> str:
    from service.jobs.content_enrich import _build_prompt

    return _build_prompt({"title": "T", "channel": "C", "duration_s": 60, "tags": []}, "자막", None)


class _CapturingClient:
    """실제로 전송되는 프롬프트를 가로챈다.

    프롬프트를 테스트가 직접 조립하면 **스테이지가 템플릿을 읽는지 검증하지 못한다** —
    처음 쓴 버전이 그랬고, 그래서 derived 를 인라인 명세로 되돌려도 통과했다.
    """

    def __init__(self) -> None:
        self.prompt = ""

    async def submit(self, prompt, **kwargs):
        self.prompt = prompt
        return "task-1"

    async def result(self, task_id, timeout=None):
        raise RuntimeError("프롬프트만 확인한다")


def _derived_prompt(repo_root: Path) -> str:
    """`DerivedStage` 가 **실제로 보내는** 프롬프트."""
    from types import SimpleNamespace

    import anyio

    from service.pipeline.gates import GenerationInput
    from service.pipeline.stages.derived import DerivedStage

    client = _CapturingClient()
    stage = DerivedStage(
        client, repo_root=repo_root, provider="p", model=None, work_dir=None
    )
    request = GenerationInput(
        item=SimpleNamespace(id=1, source_url=None, source_kind="youtube", note=None),
        gate=SimpleNamespace(item_id=1, stage_name="derived"),
        preparation=None,
        previous_payload=None,
        feedback=None,
        session_ref=None,
    )
    async def _run():
        with pytest.raises(RuntimeError):
            await stage(request)

    anyio.run(_run)
    return client.prompt


def test_template_file_exists():
    assert (config.repo_root() / TEMPLATE_PATH).is_file()


@pytest.mark.parametrize("section", SECTIONS)
def test_template_defines_all_sections(section):
    assert section in content_format()


@pytest.mark.parametrize("section", SECTIONS)
def test_both_prompts_carry_the_sections(section):
    assert section in _enrich_prompt()
    assert section in _derived_prompt(config.repo_root())


def test_editing_the_template_changes_both_prompts(tmp_path, monkeypatch):
    """SoT 가 하나임을 **실제로 바꿔서** 확인한다.

    양쪽이 각자 명세를 들고 있으면 이 테스트가 실패한다.
    """
    marker = "## 이 줄은 템플릿에서만 왔다"
    (tmp_path / "templates/persona").mkdir(parents=True)
    (tmp_path / "templates/persona/content.md").write_text(marker, encoding="utf-8")
    monkeypatch.setattr(config, "repo_root", lambda: tmp_path)
    reset_cache()

    assert marker in _enrich_prompt()
    assert marker in _derived_prompt(tmp_path)


def test_missing_template_falls_back_loudly(tmp_path, caplog):
    """파일을 못 읽어도 교안이 통째로 무너지지는 않되, **경고는 남는다.**"""
    reset_cache()
    with caplog.at_level("WARNING"):
        text = content_format(tmp_path)
    assert text == FALLBACK
    assert any("읽지 못해" in r.message for r in caplog.records)


def test_system_assigned_fields_are_documented():
    """AI 가 정하지 않는 값이 양식에 적혀 있어야 한다 — 안 적으면 AI 가 지어낸다."""
    text = content_format()
    for field in ("id", "day", "status"):
        assert field in text
    assert "published" in text and "pending" in text
