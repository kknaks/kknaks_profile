"""Deterministic Markdown rendering for capture documents."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .models import CaptureDocument, CaptureValidationError


@dataclass(frozen=True)
class RenderContext:
    repo_root: Path
    request_id: str
    root_thread_ts: str
    captured_at: datetime
    group: str = "study"
    allowed_groups: frozenset[str] = frozenset({"study"})
    output_override: Path | None = None


def output_path(document: CaptureDocument, context: RenderContext) -> Path:
    root = context.repo_root.resolve()
    if context.output_override is not None:
        path = (root / context.output_override).resolve()
        if not path.is_relative_to(root):
            raise CaptureValidationError("output path escapes repository")
        expected_parent = "inbox" if document.kind == "idea" else "reference"
        if path.relative_to(root).parts[0] != expected_parent:
            raise CaptureValidationError("existing output path does not match document kind")
        return path
    date = context.captured_at.strftime("%Y-%m-%d")
    if document.kind == "idea":
        relative = Path("inbox") / f"{date}-{document.slug}.md"
    else:
        if context.group not in context.allowed_groups:
            raise CaptureValidationError(f"unknown reference group: {context.group}")
        # **flat 이다.** 종전에는 `reference/{group}/` 이었는데 WORK-005/013 이 층을
        # flat 으로 바꾼 뒤로도 여기만 남아 있었다 — 로더가 `*.md` 를 **재귀 없이**
        # 훑으므로 하위 폴더에 쓰면 그 노트가 **아예 안 읽힌다.** 롤백 경로라 실행될
        # 일이 드물어 드러나지 않았다 (KDEV-WORK-019 에서 발견).
        #
        # `group` 검사는 남긴다 — 경로에는 안 쓰이지만 입력이 알려진 값인지 보는
        # 방어로는 여전히 쓸모가 있다.
        relative = Path("resources") / "source" / f"{date}-{document.slug}.md"
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise CaptureValidationError("output path escapes repository")
    return path


def render_document(document: CaptureDocument, context: RenderContext) -> str:
    stem = output_path(document, context).stem
    created = context.captured_at.isoformat(timespec="seconds")
    meta: dict[str, Any] = {
        "type": document.kind,
        "id": stem,
        "title": document.title,
    }
    if document.kind == "idea":
        meta.update({
            "created_at": created,
            "source": "slack",
            "slack_event_id": context.request_id,
            "slack_thread_ts": context.root_thread_ts,
            "tags": list(document.tags),
        })
        body = _render_idea(document)
    else:
        source = document.source or {}
        meta.update({
            "date": context.captured_at.strftime("%Y.%m.%d"),
            "group": context.group,
            "source": source["url"],
            "source_type": source["type"],
            "source_title": source.get("title"),
            "source_author": source.get("author"),
            "source_published_at": source.get("published_at"),
            "accessed_at": source["accessed_at"],
            "slack_event_id": context.request_id,
            "slack_thread_ts": context.root_thread_ts,
            "summary": document.summary,
            "tags": list(document.tags),
        })
        meta = {key: value for key, value in meta.items() if value is not None}
        body = _render_reference(document)
    frontmatter = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{frontmatter}\n---\n\n# {document.title}\n\n{body.strip()}\n"


def _render_idea(document: CaptureDocument) -> str:
    idea = document.idea or {}
    questions = _bullets(idea["open_questions"])
    return f"""## 원문

{idea["original"]}

## 정리된 아이디어

{idea["refined"]}

## 해결하려는 문제

{idea["problem"]}

## 기대 효과

{idea["expected_value"]}

## 열린 질문

{questions}"""


def _render_reference(document: CaptureDocument) -> str:
    ref = document.reference or {}
    concepts = "\n".join(
        f"### {item['name']}\n\n{item['description']}" for item in ref["concepts"]
    )
    candidates = (
        "\n".join(f"- {item['target']}: {item['reason']}" for item in document.connection_candidates)
        or "- 확인된 연결 후보 없음"
    )
    return f"""## 개요

{ref["overview"]}

## 출처와 맥락

{ref["context"]}

## 핵심 주장

{_bullets(ref["key_claims"])}

## 주요 개념

{concepts}

## 근거와 사례

{_bullets(ref["evidence"])}

## 적용 가능성

> 아래 내용은 원문 요약이 아니라 적용을 위한 해석이다.

{_bullets(ref["applications"])}

## 한계와 검증이 필요한 부분

{_bullets(ref["limitations"])}

## 내 지식과의 연결 후보

{candidates}

## 참고

{ref["notes"]}"""


def _bullets(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values)
