from __future__ import annotations

from datetime import datetime

import pytest
import yaml

from service.knowledge_capture import (
    CaptureValidationError,
    RenderContext,
    atomic_write,
    output_path,
    parse_document,
    render_document,
)
from service.knowledge_capture.source import detect_source_type, find_urls


def _idea() -> dict:
    return {
        "schema_version": "1.0",
        "kind": "idea",
        "title": "Slack 지식 수집",
        "slug": "slack-knowledge-capture",
        "summary": "Slack에서 아이디어를 수집한다.",
        "tags": ["slack", "knowledge"],
        "intent": None,
        "source": None,
        "idea": {
            "original": "슬랙에서 아이디어를 넣자",
            "refined": "Slack을 지식 수집 진입점으로 사용한다.",
            "problem": "생각을 기록하는 마찰이 크다.",
            "expected_value": "아이디어 유실을 줄일 수 있다.",
            "open_questions": ["어떤 채널을 사용할까?"],
        },
        "reference": None,
        "connection_candidates": [],
    }


def _reference() -> dict:
    data = _idea()
    data.update({
        "kind": "reference",
        "title": "에이전트 메모리 논문",
        "slug": "agent-memory-paper",
        "source": {
            "url": "https://example.com/paper",
            "type": "paper",
            "title": "Agent Memory",
            "author": "Kim",
            "publisher": None,
            "published_at": "2026-01-01",
            "accessed_at": "2026-07-02T12:00:00+09:00",
            "external_id": None,
        },
        "idea": None,
        "reference": {
            "overview": "에이전트 메모리 구조를 설명한다.",
            "context": "연구 논문이다.",
            "key_claims": ["계층적 메모리가 검색 비용을 줄인다."],
            "concepts": [{"name": "계층적 메모리", "description": "정보를 단계별로 저장한다."}],
            "evidence": ["실험군의 검색 비용이 감소했다."],
            "applications": ["개인 지식그래프에 적용할 수 있다."],
            "limitations": ["표본 범위가 제한적이다."],
            "notes": "추가 자료 없음",
        },
        "connection_candidates": [
            {"target": "known-note", "reason": "메모리 구조 관련", "confidence": 0.8},
            {"target": "missing-note", "reason": "없는 노트", "confidence": 0.5},
        ],
    })
    return data


def _context(tmp_path, *, group: str = "study") -> RenderContext:
    return RenderContext(
        repo_root=tmp_path,
        request_id="Ev123",
        root_thread_ts="123.456",
        captured_at=datetime.fromisoformat("2026-07-02T12:00:00+09:00"),
        group=group,
        allowed_groups=frozenset({"study", "ai_skills"}),
    )


def test_idea_render_contract(tmp_path):
    document = parse_document(_idea())
    rendered = render_document(document, _context(tmp_path))
    assert output_path(document, _context(tmp_path)).relative_to(tmp_path).as_posix() == (
        "inbox/2026-07-02-slack-knowledge-capture.md"
    )
    meta = yaml.safe_load(rendered.split("---", 2)[1])
    assert meta["type"] == "idea"
    assert meta["slack_thread_ts"] == "123.456"
    assert "## 정리된 아이디어" in rendered


def test_reference_render_contract_and_candidate_filter(tmp_path):
    document = parse_document(_reference(), known_stems={"known-note"})
    rendered = render_document(document, _context(tmp_path, group="ai_skills"))
    assert len(document.connection_candidates) == 1
    assert "reference/ai_skills/2026-07-02-agent-memory-paper.md" == (
        output_path(document, _context(tmp_path, group="ai_skills")).relative_to(tmp_path).as_posix()
    )
    headings = [
        "## 개요", "## 출처와 맥락", "## 핵심 주장", "## 주요 개념",
        "## 근거와 사례", "## 적용 가능성", "## 한계와 검증이 필요한 부분",
        "## 내 지식과의 연결 후보", "## 참고",
    ]
    assert [rendered.index(heading) for heading in headings] == sorted(
        rendered.index(heading) for heading in headings
    )
    assert "missing-note" not in rendered


@pytest.mark.parametrize(
    ("field", "value"),
    [("schema_version", "2.0"), ("kind", "permanent"), ("slug", "../escape")],
)
def test_invalid_document_rejected(field, value):
    data = _idea()
    data[field] = value
    with pytest.raises(CaptureValidationError):
        parse_document(data)


def test_unknown_reference_group_rejected(tmp_path):
    with pytest.raises(CaptureValidationError):
        output_path(parse_document(_reference()), _context(tmp_path, group="unknown"))


def test_atomic_write_refuses_replace_and_preserves_existing(tmp_path):
    path = tmp_path / "inbox" / "note.md"
    atomic_write(path, "first")
    with pytest.raises(FileExistsError):
        atomic_write(path, "second")
    assert path.read_text() == "first"
    atomic_write(path, "second", replace=True)
    assert path.read_text() == "second"


def test_source_detection():
    assert find_urls("이거 https://youtu.be/abc1234 봐줘") == ["https://youtu.be/abc1234"]
    assert detect_source_type("https://youtu.be/abc1234") == "youtube"
    assert detect_source_type("https://arxiv.org/abs/1234.5678") == "paper"
    assert detect_source_type("https://example.com/post") == "blog"
