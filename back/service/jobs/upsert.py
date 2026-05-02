"""activity.yaml upsert — rolling 365 + idempotent (spec-03 §4)."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import yaml

import config

DEFAULT_PATH = config.PERSONA_DIR / "activity.yaml"
WINDOW_DAYS = 365


def upsert_activity(entry: dict, path: Path = DEFAULT_PATH) -> dict:
    """오늘 entry를 activity.yaml에 upsert. rolling 365 트림.

    Idempotent — 같은 entry 두 번 박아도 결과 동일.
    Returns the full data dict written.
    """
    data: dict
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or _empty(entry["date"])
    else:
        data = _empty(entry["date"])

    # 같은 date entry 제거 후 추가
    data["items"] = [e for e in data.get("items", []) if e["date"] != entry["date"]]
    data["items"].append(entry)
    data["items"].sort(key=lambda e: e["date"])

    # rolling 365 트림
    today = date.fromisoformat(entry["date"].replace(".", "-"))
    cutoff = today - timedelta(days=WINDOW_DAYS - 1)
    cutoff_str = cutoff.strftime("%Y.%m.%d")
    data["items"] = [e for e in data["items"] if e["date"] >= cutoff_str]

    data["since"] = data["items"][0]["date"]
    data["until"] = data["items"][-1]["date"]
    data["totalCount"] = sum(e.get("count", 0) for e in data["items"])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    return data


def _empty(seed_date: str) -> dict:
    return {"since": seed_date, "until": seed_date, "totalCount": 0, "items": []}
