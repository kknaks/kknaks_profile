"""content 시드 — 원료는 para/resources/youtube/*.md 의 frontmatter.

- slug 는 frontmatter `id`(C-002 …) — 파일명이 아니라 문서가 자기 이름을 안다.
- title·summary 는 ko 값만 담는다(database.md 서두 — 한국어 하나).
- tags 는 `#` 접두를 뗀다 — 표시용 장식이지 값이 아니다.
- published_on 은 `date`("2026.05.02") 를 date 로 바꾼다.
- visible 은 전부 true — frontmatter 에 없고, 옛 사이트에서 전부 공개였다.
- detail_path 는 그 md 를 리포 루트 기준 상대경로로 가리킨다 — 본문을 복사하지
  않는다(정보는 DB, 상세는 md).
- 원료에 없는 필드는 비워 둔다 — 추측으로 메우지 않는다.
- profile_id 는 첫 profile 행 — 1인 사이트다.

멱등 upsert(slug 기준): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
어드민에서 고치기 시작한 뒤에는 돌리지 않는다.

실행:  uv run python -m seed.seed_contents
"""

from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path

import yaml
from sqlalchemy import select

from core.db import SessionLocal
from models import Content, Profile

# app/back/seed/ → 리뉴얼 루트
_ROOT = Path(__file__).resolve().parents[3]
_CONTENTS_DIR = _ROOT / "para" / "resources" / "youtube"


def _ko(value: object) -> str | None:
    """frontmatter 의 {ko, en} 또는 단일 문자열에서 ko 만 뽑는다."""
    if isinstance(value, dict):
        value = value.get("ko")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _to_date(value: object) -> date | None:
    """`"2026.05.02"` → date(2026, 5, 2). yaml 이 date 로 읽었으면 그대로."""
    if isinstance(value, date):
        return value
    if not isinstance(value, str) or not value.strip():
        return None
    parts = value.strip().replace("-", ".").split(".")
    if len(parts) != 3:
        return None
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def _tags(value: object) -> list[str] | None:
    """['#modulo-bias', …] → ['modulo-bias', …]. 다 비면 None."""
    if not isinstance(value, list):
        return None
    picked = [
        tag.lstrip("#").strip()
        for tag in value
        if isinstance(tag, str) and tag.lstrip("#").strip()
    ]
    return picked or None


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, fm, _ = text.split("---", 2)
    loaded = yaml.safe_load(fm)
    return loaded if isinstance(loaded, dict) else {}


def _fields_from(md: Path) -> dict | None:
    fm = _frontmatter(md)
    slug = fm.get("id")
    title = _ko(fm.get("title"))
    youtube_id = fm.get("youtubeId")
    if not (isinstance(slug, str) and slug and title and isinstance(youtube_id, str)):
        print(f"건너뜀 — id·title.ko·youtubeId 없음: {md.name}")
        return None
    duration = fm.get("duration")
    speaker = fm.get("speaker")
    return {
        "slug": slug,
        "title": title,
        "summary": _ko(fm.get("summary")),
        "detail_path": str(md.relative_to(_ROOT)),
        "youtube_id": youtube_id,
        "duration": str(duration) if duration else None,
        "speaker": str(speaker) if speaker else None,
        "tags": _tags(fm.get("tags")),
        "published_on": _to_date(fm.get("date")),
        "visible": True,  # frontmatter 에 없음 — 옛 사이트에서 전부 공개였다
    }


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            raise SystemExit("profile 이 없다 — seed_profile 을 먼저 돌린다")

        count = 0
        for md in sorted(_CONTENTS_DIR.glob("*.md")):
            fields = _fields_from(md)
            if fields is None:
                continue
            fields["profile_id"] = profile.id

            row = (
                await session.execute(
                    select(Content).where(Content.slug == fields["slug"])
                )
            ).scalar_one_or_none()
            if row is None:
                session.add(Content(**fields))
                print(f"content 생성 — {fields['slug']} ({fields['title']})")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"content 갱신 — {fields['slug']} ({fields['title']})")
            count += 1

        await session.commit()
        print(f"완료 — {count}건")


if __name__ == "__main__":
    asyncio.run(seed())
