"""i18n helper — frontmatter `{ko, en}` 객체 → lang에 따라 한쪽 추출 (ADR-02 + spec-02 §4.1)."""

from __future__ import annotations

from typing import Any


def i18n(node: Any, lang: str = "ko") -> Any:
    """Extract one language from a `{ko, en}` dict; pass through scalars/lists.

    ADR-02 §2.4: ko가 마스터 언어 — 요청 lang 누락 시 ko로 fallback.
    """
    if isinstance(node, dict) and lang in node:
        return node[lang]
    if isinstance(node, dict) and "ko" in node:
        return node["ko"]
    return node


def apply_i18n(obj: Any, lang: str = "ko") -> Any:
    """Recursively apply `i18n` to all `{ko, en}` shaped dicts in an arbitrary nested object."""
    if isinstance(obj, dict):
        if _is_i18n_object(obj):
            return i18n(obj, lang)
        return {k: apply_i18n(v, lang) for k, v in obj.items()}
    if isinstance(obj, list):
        return [apply_i18n(x, lang) for x in obj]
    return obj


def _is_i18n_object(d: dict) -> bool:
    """`{ko, en}` 또는 `{ko}`만 있는 dict인지 검사. 다른 키 섞여있으면 i18n 객체 아님."""
    keys = set(d.keys())
    return keys <= {"ko", "en"} and "ko" in keys
