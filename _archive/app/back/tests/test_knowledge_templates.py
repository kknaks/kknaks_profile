"""`templates/knowledge/` 가 그래프 검증과 어긋나지 않는지 (KDEV-WORK-013).

템플릿은 **형식의 SoT** 다 — 사람도 AI 에이전트도 여기를 읽고 노트를 쓴다
(`CLAUDE.md → agent.md → rules/knowledge-note-pipeline.md → templates/knowledge/`).
프롬프트에 복사해 넣지 않으므로, 템플릿이 틀리면 그대로 산출물이 틀린다.

따라서 템플릿은 두 가지를 만족해야 한다.
1. frontmatter 가 **파싱된다** — 플레이스홀더에 콜론 하나만 들어가도 YAML 이 깨진다.
2. 채워 넣으면 **L1~L6 를 통과한다** — 템플릿대로 썼는데 검증에 걸리면 규칙과 양식이 갈라진 것이다.
"""

from __future__ import annotations

import re
from pathlib import Path

import frontmatter
import pytest

from core.graph import validate_graph

TEMPLATE_DIR = Path(__file__).resolve().parents[3] / "templates" / "knowledge"
# KDEV-DEC-019 — 판단층 폐기로 `permanent.md` 템플릿이 사라졌다.
LAYER_TEMPLATES = ("idea.md", "reference.md", "concept.md")

REFERENCE_STEM = "2026-07-28-sample-source"
CONCEPT_STEM = "sample-concept"
IDEA_STEM = "2026-07-28-sample-idea"


def _strip_placeholders(value):
    """`<...>` 안내문을 그럴듯한 값으로 치환한다."""
    if isinstance(value, str):
        return re.sub(r"<[^>]*>", "x", value)
    if isinstance(value, list):
        return [_strip_placeholders(v) for v in value]
    return value


def _load(name: str, stem: str) -> tuple[dict, str]:
    post = frontmatter.loads(TEMPLATE_DIR.joinpath(name).read_text(encoding="utf-8"))
    meta = {k: _strip_placeholders(v) for k, v in post.metadata.items()}
    meta["id"] = stem
    body = re.sub(r"<!--.*?-->", "", post.content, flags=re.S)   # 주석 제거
    body = re.sub(r"<[^>]*>", "설명", body)                       # 본문 플레이스홀더
    return meta, body


def _node(meta: dict, body: str) -> dict:
    return {
        **meta,
        "body": body,
        "up": meta.get("up"),
        "aliases": meta.get("aliases"),
        "archived": False,
    }


@pytest.mark.parametrize("name", LAYER_TEMPLATES + ("README.md",))
def test_template_frontmatter_parses(name):
    """플레이스홀더에 콜론이 섞이면 여기서 걸린다 (실제로 한 번 깨졌다)."""
    frontmatter.loads(TEMPLATE_DIR.joinpath(name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", LAYER_TEMPLATES)
def test_template_declares_expected_type(name):
    """`reference` 는 로더가 type 을 주입하므로 frontmatter 에 없어도 된다."""
    post = frontmatter.loads(TEMPLATE_DIR.joinpath(name).read_text(encoding="utf-8"))
    expected = {"idea.md": "idea", "concept.md": "concept"}
    if name in expected:
        assert post.metadata.get("type") == expected[name]


def _filled_graph() -> dict:
    """세 템플릿을 채워 층 체인을 만든다 — reference ← concept."""
    ref_meta, ref_body = _load("reference.md", REFERENCE_STEM)
    ref_meta["type"] = "reference"          # 로더가 주입하는 값
    ref_body += f"\n- [[{CONCEPT_STEM}]] — 개념 위임\n"

    con_meta, con_body = _load("concept.md", CONCEPT_STEM)
    con_meta["aliases"] = ["샘플개념", "sample"]
    con_meta["up"] = [REFERENCE_STEM]
    con_body += f"\n- [[{REFERENCE_STEM}]] — 출처\n"

    idea_meta, idea_body = _load("idea.md", IDEA_STEM)
    idea_meta.pop("up", None)

    return {
        REFERENCE_STEM: _node(ref_meta, ref_body),
        CONCEPT_STEM: _node(con_meta, con_body),
        IDEA_STEM: _node(idea_meta, idea_body),
    }


def test_filled_templates_pass_validation():
    """템플릿대로 쓴 노트는 ERROR·WARN 없이 통과해야 한다.

    걸린다면 템플릿과 `core/graph.py` 규칙이 갈라진 것이다 — 둘 중 하나를 고쳐야 한다.
    """
    violations = validate_graph(_filled_graph())
    blocking = [v for v in violations if v["level"] in ("ERROR", "WARN")]
    assert blocking == [], [f"{v['rule']} {v['node']}: {v['detail']}" for v in blocking]


def test_filled_templates_form_the_layer_chain():
    """계보가 실제로 발현되는지 — 템플릿이 `up:` 을 제대로 안내하는가."""
    from core.graph import build_knowledge_graph

    graph = build_knowledge_graph(_filled_graph())
    lineage = {
        (e["source"], e["target"])
        for e in graph["edges"] if e["type"] == "lineage"
    }
    assert (CONCEPT_STEM, REFERENCE_STEM) in lineage      # 개념 → 출처

    layers = {n["id"]: n["layer"] for n in graph["nodes"]}
    assert layers[REFERENCE_STEM] == "source"
    assert layers[CONCEPT_STEM] == "concept"
    assert layers[IDEA_STEM] is None                      # 노드이되 층 없음
