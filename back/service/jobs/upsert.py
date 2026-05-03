"""daily/{date}.md 갱신 — auto:true frontmatter + body (spec-03 §4, ADR-06).

기존 `upsert_activity` (activity.yaml 1 entry upsert) 폐기. ADR-06: 그날 = daily/{date}.md
한 파일이 SoT, activity.yaml 폐지 (`/api/activity` 는 daily/*.md 집계 derive).
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

import frontmatter

import config

logger = logging.getLogger("kknaks-back.upsert")


def write_daily(
    target: date,
    counts: dict,
    summary: dict | None,
    body: str,
    *,
    persona_dir: Path = config.PERSONA_DIR,
) -> Path:
    """daily/{date}.md 박기. 기존 파일이 `auto: false` 면 overwrite skip (본인 작성 보호).

    Idempotent — 같은 입력으로 두 번 호출해도 결과 동일.
    """
    path = persona_dir / "daily" / f"{target.isoformat()}.md"

    # spec-03 §1.3 방어 — 본인 작성 보호 (잡 진입점에서도 검사하지만 이중 안전망)
    if path.exists():
        try:
            existing = frontmatter.load(path)
            if not existing.metadata.get("auto"):
                logger.warning(
                    "daily/%s auto=false (본인 작성) — overwrite skip", path.name
                )
                return path
        except Exception as e:  # noqa: BLE001
            logger.warning("existing daily parse fail %s: %s — overwrite", path.name, e)

    fm: dict = {
        "type": "daily",
        "date": target.strftime("%Y.%m.%d"),
        "auto": True,
        "counts": dict(counts),
    }
    if summary is not None:
        fm["summary"] = summary

    post = frontmatter.Post(content=body or "", **fm)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return path
