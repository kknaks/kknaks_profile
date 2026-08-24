"""algorithm 시드 — 원료는 para/resources/algorithms/*.md 의 frontmatter (94건).

매핑 (원료에 없는 필드는 비운다 — 추측으로 메우지 않는다):
- slug            = `id` (A-001)
- title           = `title.ko` (없으면 `title.en`)
- difficulty      = `difficulty`
- summary         = `summary` (frontmatter 에 있으면 — 현재 원료엔 없다)
- source_platform = `source.platform`
- source_number   = `source.number`
- source_url      = `source.url`
- curated_in      = `source.curated_in`
- tags            = `tags`
- today           = `today` — **원료에 둘 이상이면 최신 published_on 하나만 true**
                    (DB uq_algorithm_today 가 하나만 허용한다)
- visible         = `visible`
- published_on    = `date`
- detail_path     = "para/resources/algorithms/<파일명>" — 본문은 복사하지 않는다
                    (정보는 DB, 상세는 md)
- profile_id      = 첫 profile 행 — 1인 사이트다

멱등 upsert(slug 기준): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
today 는 두 단계로 얹는다 — 먼저 시드 대상 전 행을 false 로 upsert·flush 한 뒤
지정 한 행만 true 로 올린다. 중간 상태가 partial unique 를 밟지 않게 하기 위해서다.

실행:  uv run python -m seed.seed_algorithms
"""

from __future__ import annotations

import asyncio
from datetime import date, datetime
from pathlib import Path

import yaml
from sqlalchemy import select

from core.db import SessionLocal
from models import Algorithm, Profile

# app/back/seed/ → 리뉴얼 루트
_ROOT = Path(__file__).resolve().parents[3]
_ALGORITHMS_DIR = _ROOT / "para" / "resources" / "algorithms"


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, fm, _ = text.split("---", 2)
    loaded = yaml.safe_load(fm)
    return loaded if isinstance(loaded, dict) else {}


def _title(value: object) -> str | None:
    """`title.ko` 우선, 없으면 `title.en`."""
    if isinstance(value, dict):
        for key in ("ko", "en"):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _to_date(value: object) -> date | None:
    """yaml 이 따옴표 유무에 따라 date 또는 str 로 준다 — 둘 다 받는다."""
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value.strip():
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    return None


def _str_list(value: object) -> list[str] | None:
    if not isinstance(value, list):
        return None
    picked = [v.strip() for v in value if isinstance(v, str) and v.strip()]
    return picked or None


def _fields_from(md: Path) -> dict | None:
    fm = _frontmatter(md)
    slug = fm.get("id")
    if not isinstance(slug, str) or not slug.strip():
        print(f"건너뜀 — id 없음: {md.name}")
        return None
    source = fm.get("source") if isinstance(fm.get("source"), dict) else {}
    number = source.get("number")
    summary = fm.get("summary")
    return {
        "slug": slug.strip(),
        "title": _title(fm.get("title")) or slug.strip(),
        "difficulty": fm.get("difficulty"),
        "summary": summary.strip() if isinstance(summary, str) and summary.strip() else None,
        "source_platform": source.get("platform"),
        "source_number": number if isinstance(number, int) else None,
        "source_url": source.get("url") or None,
        "curated_in": _str_list(source.get("curated_in")),
        "tags": _str_list(fm.get("tags")),
        "today": bool(fm.get("today", False)),
        "detail_path": f"para/resources/algorithms/{md.name}",
        "published_on": _to_date(fm.get("date")),
        "visible": bool(fm.get("visible", True)),
    }


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            raise SystemExit("profile 이 없다 — seed_profile 을 먼저 돌린다")

        all_fields = [
            f for md in sorted(_ALGORITHMS_DIR.glob("*.md"))
            if (f := _fields_from(md)) is not None
        ]

        # today 지정 — 원료에 둘 이상이면 최신 published_on 하나만 남긴다.
        today_rows = [f for f in all_fields if f["today"]]
        today_slug: str | None = None
        if today_rows:
            chosen = max(
                today_rows, key=lambda f: (f["published_on"] or date.min, f["slug"])
            )
            today_slug = chosen["slug"]
            if len(today_rows) > 1:
                dropped = [f["slug"] for f in today_rows if f["slug"] != today_slug]
                print(
                    f"today=true 가 원료에 {len(today_rows)}건 — "
                    f"최신 published_on 인 {today_slug} 만 남기고 내림: {dropped}"
                )

        created = updated = 0
        rows_by_slug: dict[str, Algorithm] = {}
        for fields in all_fields:
            fields["today"] = False  # 1단계 — 전부 내리고 flush 후 한 행만 올린다
            fields["profile_id"] = profile.id
            row = (
                await session.execute(
                    select(Algorithm).where(Algorithm.slug == fields["slug"])
                )
            ).scalar_one_or_none()
            if row is None:
                row = Algorithm(**fields)
                session.add(row)
                created += 1
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                updated += 1
            rows_by_slug[fields["slug"]] = row

        await session.flush()

        # 2단계 — 지정 한 행만 today=true. 시드 대상 밖의 today 행이 있으면
        # partial unique 가 여기서 막는다 — 그건 시드가 덮을 대상이 아니다.
        if today_slug is not None:
            rows_by_slug[today_slug].today = True

        await session.commit()
        print(
            f"algorithm 시드 완료 — 생성 {created} · 갱신 {updated} · "
            f"today={today_slug or '없음'}"
        )


if __name__ == "__main__":
    asyncio.run(seed())
