"""Versioned structured output parser for capture-knowledge."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

SCHEMA_VERSION = "1.0"
KINDS = {"idea", "reference"}
SOURCE_TYPES = {"youtube", "blog", "paper", "other"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CaptureValidationError(ValueError):
    """Structured capture output violates the persistence contract."""


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CaptureValidationError(f"{field} must be a non-empty string")
    return value.strip()


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        raise CaptureValidationError(f"{field} must be a list of non-empty strings")
    return [v.strip() for v in value]


@dataclass(frozen=True)
class CaptureDocument:
    schema_version: str
    kind: str
    title: str
    slug: str
    summary: str
    tags: tuple[str, ...]
    intent: str | None
    source: dict[str, Any] | None
    idea: dict[str, Any] | None
    reference: dict[str, Any] | None
    connection_candidates: tuple[dict[str, Any], ...]


def parse_document(raw: str | dict[str, Any], *, known_stems: set[str] | None = None) -> CaptureDocument:
    """Parse and validate one complete capture snapshot."""
    try:
        data = json.loads(raw) if isinstance(raw, str) else dict(raw)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise CaptureValidationError(f"invalid JSON: {exc}") from exc

    if data.get("error"):
        error = data["error"]
        raise CaptureValidationError(f"skill error: {error}")

    version = _text(data.get("schema_version"), "schema_version")
    if version != SCHEMA_VERSION:
        raise CaptureValidationError(f"unsupported schema_version: {version}")
    kind = _text(data.get("kind"), "kind")
    if kind not in KINDS:
        raise CaptureValidationError(f"invalid kind: {kind}")
    title = _text(data.get("title"), "title")
    slug = _text(data.get("slug"), "slug")
    if not SLUG_RE.fullmatch(slug):
        raise CaptureValidationError("slug must be lowercase kebab-case")
    summary = _text(data.get("summary"), "summary")
    tags = _string_list(data.get("tags"), "tags")
    if not 1 <= len(tags) <= 10:
        raise CaptureValidationError("tags must contain 1..10 values")
    intent_raw = data.get("intent")
    intent = intent_raw.strip() if isinstance(intent_raw, str) and intent_raw.strip() else None

    source = data.get("source")
    idea = data.get("idea")
    reference = data.get("reference")
    if kind == "idea":
        _validate_idea(idea)
        if reference is not None:
            raise CaptureValidationError("reference must be null for idea")
    else:
        _validate_source(source)
        _validate_reference(reference)
        if idea is not None:
            raise CaptureValidationError("idea must be null for reference")

    candidates = _validate_candidates(data.get("connection_candidates", []), known_stems)
    return CaptureDocument(
        schema_version=version,
        kind=kind,
        title=title,
        slug=slug,
        summary=summary,
        tags=tuple(tags),
        intent=intent,
        source=dict(source) if isinstance(source, dict) else None,
        idea=dict(idea) if isinstance(idea, dict) else None,
        reference=dict(reference) if isinstance(reference, dict) else None,
        connection_candidates=tuple(candidates),
    )


def _validate_idea(value: Any) -> None:
    if not isinstance(value, dict):
        raise CaptureValidationError("idea must be an object")
    for field in ("original", "refined", "problem", "expected_value"):
        _text(value.get(field), f"idea.{field}")
    _string_list(value.get("open_questions"), "idea.open_questions")


def _validate_source(value: Any) -> None:
    if not isinstance(value, dict):
        raise CaptureValidationError("source must be an object")
    url = _text(value.get("url"), "source.url")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise CaptureValidationError("source.url must be an absolute HTTP(S) URL")
    source_type = _text(value.get("type"), "source.type")
    if source_type not in SOURCE_TYPES:
        raise CaptureValidationError(f"invalid source.type: {source_type}")
    _text(value.get("accessed_at"), "source.accessed_at")


def _validate_reference(value: Any) -> None:
    if not isinstance(value, dict):
        raise CaptureValidationError("reference must be an object")
    for field in ("overview", "context", "notes"):
        _text(value.get(field), f"reference.{field}")
    for field in ("key_claims", "evidence", "applications", "limitations"):
        _string_list(value.get(field), f"reference.{field}")
    concepts = value.get("concepts")
    if not isinstance(concepts, list):
        raise CaptureValidationError("reference.concepts must be a list")
    for index, concept in enumerate(concepts):
        if not isinstance(concept, dict):
            raise CaptureValidationError(f"reference.concepts[{index}] must be an object")
        _text(concept.get("name"), f"reference.concepts[{index}].name")
        _text(concept.get("description"), f"reference.concepts[{index}].description")


def _validate_candidates(value: Any, known_stems: set[str] | None) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise CaptureValidationError("connection_candidates must be a list")
    valid: list[dict[str, Any]] = []
    for index, candidate in enumerate(value):
        if not isinstance(candidate, dict):
            raise CaptureValidationError(f"connection_candidates[{index}] must be an object")
        target = _text(candidate.get("target"), f"connection_candidates[{index}].target")
        reason = _text(candidate.get("reason"), f"connection_candidates[{index}].reason")
        confidence = candidate.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            raise CaptureValidationError(f"connection_candidates[{index}].confidence must be numeric")
        if not 0 <= float(confidence) <= 1:
            raise CaptureValidationError(f"connection_candidates[{index}].confidence must be 0..1")
        if known_stems is not None and target not in known_stems:
            continue
        valid.append({"target": target, "reason": reason, "confidence": float(confidence)})
    return valid
