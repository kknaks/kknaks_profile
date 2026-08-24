"""product 시드 — 원료는 para/projects/company/<slug>/showcase.md 의 frontmatter.

- title·summary 는 ko 값만 담는다(database.md 서두 — 한국어 하나).
- detail_path 는 그 제품의 showcase.md 를 리포 루트 기준 상대경로로 가리킨다 —
  본문을 복사하지 않는다(정보는 DB, 상세는 md).
- **visible 은 무조건 False 로 시드한다** — 사람이 검토 후 어드민에서 켠다(_RESUME 방침).
- 원료에 없는 필드(links 등)는 비워 둔다 — 추측으로 메우지 않는다.
- career 연결은 아래 CAREER_OF 명시 매핑 — 지금 medisolve-ai 의 career 행이
  「백엔드 개발자」 하나뿐이라 거기 건다. 역할이 나뉘면 어드민에서 재연결한다.

멱등 upsert(slug 기준): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
어드민에서 고치기 시작한 뒤에는 돌리지 않는다.

실행:  uv run python -m seed.seed_products
"""

from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path

import yaml
from sqlalchemy import select

from core.db import SessionLocal
from models import Career, Company, Product

# app/back/seed/ → 리뉴얼 루트
_ROOT = Path(__file__).resolve().parents[3]
_COMPANY_DIR = _ROOT / "para" / "projects" / "company"

# 제품 slug → (company slug, career title). 원료 frontmatter 에 역할 정보가 없어
# 여기 명시한다 — 추측이 아니라 현재 career 행이 하나뿐이라는 사실에 기댄 매핑.
CAREER_OF: dict[str, tuple[str, str]] = {
    "mediness": ("medisolve-ai", "백엔드 개발자"),
}


def _ko(value: object) -> str | None:
    """frontmatter 의 {ko, en} 또는 단일 문자열에서 ko 만 뽑는다."""
    if isinstance(value, dict):
        value = value.get("ko")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _month_to_date(value: object) -> date | None:
    """`"2026.05"` → date(2026, 5, 1). 월 단위라 1일로 박는다."""
    if not isinstance(value, str) or not value.strip():
        return None
    parts = value.strip().replace("-", ".").split(".")
    if len(parts) < 2:
        return None
    return date(int(parts[0]), int(parts[1]), 1)


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, fm, _ = text.split("---", 2)
    loaded = yaml.safe_load(fm)
    return loaded if isinstance(loaded, dict) else {}


def _fields_from(slug: str, showcase: Path) -> dict:
    fm = _frontmatter(showcase)
    links = fm.get("links")
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
        "links": links if isinstance(links, dict) and links else None,
        "visible": False,  # 사람이 검토 후 켠다 — frontmatter 값과 무관하게 강제
    }


async def seed() -> None:
    async with SessionLocal() as session:
        for showcase in sorted(_COMPANY_DIR.glob("*/showcase.md")):
            slug = showcase.parent.name
            if slug not in CAREER_OF:
                print(f"건너뜀 — {slug}: CAREER_OF 매핑이 없다. 매핑을 먼저 정한다")
                continue
            company_slug, career_title = CAREER_OF[slug]
            career = (
                await session.execute(
                    select(Career)
                    .join(Company, Company.id == Career.company_id)
                    .where(Company.slug == company_slug, Career.title == career_title)
                )
            ).scalar_one_or_none()
            if career is None:
                raise SystemExit(
                    f"career 가 없다 — {company_slug} · {career_title}. "
                    "seed_companies 를 먼저 돌린다"
                )

            fields = _fields_from(slug, showcase)
            fields["career_id"] = career.id

            row = (
                await session.execute(select(Product).where(Product.slug == slug))
            ).scalar_one_or_none()
            if row is None:
                session.add(Product(**fields))
                print(f"product 생성 — {slug} → {company_slug} · {career_title}")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"product 갱신 — {slug} → {company_slug} · {career_title}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
