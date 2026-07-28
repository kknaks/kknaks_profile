"""발행 전 가상 그래프 검증 (KDEV-WORK-015 P4 / KDEV-SPEC-004 §3 S-3).

계획을 **적용했다고 가정한** 그래프에 L1~L6 를 돌린다. ERROR 가 하나라도 있으면
파일을 쓰기 전에 발행 전체를 거부한다.

부팅 검증으로는 늦다 — 그때는 이미 `origin/main` 에 나간 뒤다.

전체 재조립(406노드)이 비싸지 않아 증분 계산을 하지 않는다(SPEC-010 §7 OQ). 발행은
승인 한 번에 한 번 일어나는 일이고, 잘못 나가는 비용이 훨씬 크다.
"""

from __future__ import annotations

import logging
from typing import Any

import frontmatter

from core.graph import validate_graph

from .plan import FileAction, Violation

logger = logging.getLogger("kknaks-back.apply.graph")


def _node_from(action: FileAction) -> dict[str, Any]:
    """계획된 파일 하나 → 그래프 노드. 로더가 만드는 것과 같은 모양이어야 한다."""
    post = frontmatter.loads(action.content)
    meta = post.metadata
    aliases = meta.get("aliases") or []
    if isinstance(aliases, str):
        aliases = [aliases]
    return {
        "type": meta.get("type") or action.note_type,
        "id": action.stem,
        "title": meta.get("title") or action.stem,
        "up": meta.get("up"),
        "aliases": list(aliases),
        "body": post.content,
        "archived": False,
    }


def virtual_nodes(
    current: dict[str, dict], actions: list[FileAction]
) -> dict[str, dict]:
    """현재 노드 맵 위에 계획을 얹은 사본. **원본을 건드리지 않는다.**"""
    merged = dict(current)
    for action in actions:
        try:
            merged[action.stem] = _node_from(action)
        except Exception as exc:  # noqa: BLE001
            logger.warning("계획 노드 파싱 실패 %s — %s", action.path, exc)
    return merged


def check_graph(
    current: dict[str, dict], actions: list[FileAction]
) -> list[Violation]:
    """가상 그래프의 **ERROR** 만 발행 차단 사유로 삼는다.

    WARN·INFO 는 막지 않는다 — `synthesis` orphan(WARN)이나 미소화 큐(INFO)는
    정상 상태이고, 그것 때문에 발행을 막으면 아무것도 못 내보낸다.
    """
    nodes = virtual_nodes(current, actions)
    by_stem = {a.stem: a.path for a in actions}
    violations: list[Violation] = []
    for item in validate_graph(nodes):
        if item.get("level") != "ERROR":
            continue
        stem = str(item.get("node") or "")
        violations.append(
            Violation(
                rule=f"GRAPH_{item.get('rule')}",
                path=by_stem.get(stem, stem),
                detail=str(item.get("detail") or ""),
            )
        )
    return violations
