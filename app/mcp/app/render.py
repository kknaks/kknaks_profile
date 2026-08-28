"""tool 응답의 표기 — 모델이 읽을 md + 화면이 쓸 structured.

## 왜 md 를 따로 만드나

모델은 JSON 보다 문장을 잘 읽고, 특히 **다음에 무엇을 할지**를 목록의 생김새에서 고른다.
목록마다 `slug` 를 눈에 띄게 두는 이유가 그것이다 — 상세 tool 의 인자가 그 값이라는 것을
설명 없이 알게 된다.

## structured 는 소비자가 읽는다

근거 카드(§3 S-9 2항)는 back 의 소비자가 `structured.item` 에서 뽑는다. 그래서 **상세
tool 은 반드시 `item` 을 실어야 한다** — 목록은 `items` 라 카드가 만들어지지 않는다
(훑기만 한 것을 「읽었다」고 말하지 않는다).
"""

from __future__ import annotations

from typing import Any

#: 목록 한 줄의 요약 길이 상한 — 목록 하나가 컨텍스트를 다 먹지 않게.
_SUMMARY_MAX = 200


def _clip(text: str | None, limit: int = _SUMMARY_MAX) -> str:
    if not text:
        return ""
    flat = " ".join(str(text).split())
    return flat if len(flat) <= limit else flat[:limit] + "…"


def _meta_line(meta: dict[str, Any] | None) -> str:
    if not meta:
        return ""
    parts = []
    for key, value in meta.items():
        rendered = " · ".join(str(v) for v in value) if isinstance(value, list) else str(value)
        parts.append(f"{key}: {rendered}")
    return "  \n  ".join(parts)


def render_list(title: str, payload: dict[str, Any]) -> dict[str, Any]:
    """목록 tool 의 반환. `items` 를 준다 — 근거 카드는 만들어지지 않는다."""
    items = payload.get("items") or []
    lines = [f"## {title} ({len(items)}건)", ""]
    if not items:
        lines.append("_노출 승인된 항목이 없습니다. 기록에 없다고 답하세요._")
    for item in items:
        head = f"- **{item.get('title', '')}** — `{item.get('slug', '')}`"
        if item.get("subtitle"):
            head += f"  \n  {item['subtitle']}"
        if item.get("summary"):
            head += f"  \n  {_clip(item['summary'])}"
        lines.append(head)
    return {
        "content": [{"type": "text", "text": "\n".join(lines)}],
        "structured": {"items": items, "count": len(items)},
    }


def render_doc(payload: dict[str, Any]) -> dict[str, Any]:
    """상세 tool 의 반환. `item` 을 실어야 근거 카드가 만들어진다(머리 주석)."""
    item = payload.get("item") or {}
    lines = [f"## {item.get('title', '')}"]
    if item.get("subtitle"):
        lines.append(f"_{item['subtitle']}_")
    if item.get("summary"):
        lines += ["", item["summary"]]
    meta = _meta_line(item.get("meta"))
    if meta:
        lines += ["", meta]
    body = item.get("body")
    if body:
        lines += ["", "---", "", str(body)]
    else:
        lines += ["", "_상세 본문이 없습니다 — 위 요약이 기록의 전부입니다._"]
    return {
        "content": [{"type": "text", "text": "\n".join(lines)}],
        "structured": {"item": item},
    }


def render_profile(payload: dict[str, Any]) -> dict[str, Any]:
    item = payload.get("item") or {}
    lines = [
        f"## {item.get('name', '')} — {item.get('role', '')}",
        "",
        f"- 연차: {item.get('years') or '(기록 없음)'}",
        f"- 위치: {item.get('location') or '(기록 없음)'}",
        f"- focus: {item.get('focus') or '(기록 없음)'}",
        f"- 스택: {' · '.join(item.get('stack') or []) or '(기록 없음)'}",
        f"- 이메일: {item.get('email', '')}",
    ]
    # 프로필은 문서가 아니다 — 근거 카드로 올리지 않는다(`item` 대신 `profile`).
    return {
        "content": [{"type": "text", "text": "\n".join(lines)}],
        "structured": {"profile": item},
    }
