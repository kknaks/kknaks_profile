"""project 시드 — 원료는 para/projects/summer-star/<slug>/showcase.md 의 frontmatter.

- slug 는 **디렉토리명**이다 — frontmatter 의 P-NN id·org 는 쓰지 않는다.
- title·summary 는 ko 값만 담는다(database.md 서두 — 한국어 하나).
- links 는 {repo, site, store} 만 담는다(erd.md §project) — 그 외 키(live 등)는 버린다.
- visible 은 frontmatter 값 그대로 — showcase.md 가 원장이다.
- detail_path 는 그 프로젝트의 showcase.md 를 리포 루트 기준 상대경로로 가리킨다 —
  본문을 복사하지 않는다(정보는 DB, 상세는 md).
- 원료에 없는 필드는 비워 둔다 — 추측으로 메우지 않는다.
- profile_id 는 첫 profile 행 — 1인 사이트다.

멱등 upsert(slug 기준): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
어드민에서 고치기 시작한 뒤에는 돌리지 않는다.

실행:  uv run python -m seed.seed_projects
"""

from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path

import yaml
from sqlalchemy import select

from core.db import SessionLocal
from models import Profile, Project

# app/back/seed/ → 리뉴얼 루트
_ROOT = Path(__file__).resolve().parents[3]
_PROJECTS_DIR = _ROOT / "para" / "projects" / "summer-star"

# links jsonb 에 담는 키 — erd.md §project 의 {repo, site, store}.
_LINK_KEYS = ("repo", "site", "store")


def _ko(value: object) -> str | None:
    """frontmatter 의 {ko, en} 또는 단일 문자열에서 ko 만 뽑는다."""
    if isinstance(value, dict):
        value = value.get("ko")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _month_to_date(value: object) -> date | None:
    """`"2026.03"` → date(2026, 3, 1). 월 단위라 1일로 박는다."""
    if not isinstance(value, str) or not value.strip():
        return None
    parts = value.strip().replace("-", ".").split(".")
    if len(parts) < 2:
        return None
    return date(int(parts[0]), int(parts[1]), 1)


def _links(value: object) -> dict | None:
    """{repo, site, store} 만 남긴다. 빈 값 키는 버리고, 다 비면 None."""
    if not isinstance(value, dict):
        return None
    picked = {
        key: value[key].strip()
        for key in _LINK_KEYS
        if isinstance(value.get(key), str) and value[key].strip()
    }
    return picked or None


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, fm, _ = text.split("---", 2)
    loaded = yaml.safe_load(fm)
    return loaded if isinstance(loaded, dict) else {}


def _fields_from(slug: str, showcase: Path) -> dict:
    fm = _frontmatter(showcase)
    return {
        "slug": slug,
        "title": _ko(fm.get("title")) or slug,
        "summary": _ko(fm.get("summary")),
        "detail_path": str(showcase.relative_to(_ROOT)),
        "category": fm.get("category") or None,
        "status": fm.get("status") or None,
        "started_on": _month_to_date(fm.get("date")),
        "stack": fm.get("stack") or None,
        "thumbnail": fm.get("thumbnail") or None,
        "links": _links(fm.get("links")),
        "visible": bool(fm.get("visible", True)),
    }


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            raise SystemExit("profile 이 없다 — seed_profile 을 먼저 돌린다")

        for showcase in sorted(_PROJECTS_DIR.glob("*/showcase.md")):
            slug = showcase.parent.name
            fields = _fields_from(slug, showcase)
            fields["profile_id"] = profile.id

            row = (
                await session.execute(select(Project).where(Project.slug == slug))
            ).scalar_one_or_none()
            if row is None:
                session.add(Project(**fields))
                print(f"project 생성 — {slug} (visible={fields['visible']})")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"project 갱신 — {slug} (visible={fields['visible']})")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
