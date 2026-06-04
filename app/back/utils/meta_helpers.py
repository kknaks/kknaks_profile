"""공통 가공 — _meta.yaml + items 자동 집계 (categories.count 등)."""

from __future__ import annotations

from collections import Counter
from typing import Any

from core.i18n import i18n


def build_meta_groups(
    meta_groups: list[dict],
    items: list[dict],
    item_field: str,
    lang: str,
) -> list[dict]:
    """`_meta` 내 categories/clusters list + items 자동 count → 응답 dict.

    Args:
        meta_groups: e.g. [{id, label, order, color?}, ...]
        items: e.g. projects[] 또는 notes 값
        item_field: 'category' (projects) 또는 'group' (notes)
        lang: ko/en

    Returns:
        [{"id": ..., "label": "...", "count": N, ...meta extras}]
    """
    counts = Counter(it.get(item_field) for it in items)
    sorted_groups = sorted(meta_groups, key=lambda g: g.get("order", 999))
    out = []
    for g in sorted_groups:
        entry: dict[str, Any] = {
            "id": g["id"],
            "label": i18n(g.get("label"), lang),
            "count": counts.get(g["id"], 0),
        }
        # color 같은 추가 메타 보존 (notes.clusters 용)
        if "color" in g:
            entry["color"] = g["color"]
        out.append(entry)
    return out
