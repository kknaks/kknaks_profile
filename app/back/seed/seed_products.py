"""product 시드 — 2026-08-25 실 DB 상태를 값으로 박는다.

원래는 para/projects/company/<slug>/showcase.md frontmatter 를 파싱했지만,
메타 SoT 는 DB 로 갔다(templates/projects/showcase.md — frontmatter 를 두지
않는다). 원료는 이제 어드민이 관리하는 DB 그 자체이고, 시드는 그 시점 상태의
스냅샷이다. 상세 본문은 detail_path 의 md 가 갖는다(정보는 DB, 상세는 md).

- career 연결은 CAREER_OF 명시 매핑 — mediness 는 「AX 리더」 역할의 산출물이다
  (어드민에서 재연결한 실값, 2026-08-25).
- visible 도 어드민에서 정한 실값 그대로 — 첫 시드의 「무조건 False」는
  검토 전 상태였고, 검토가 끝나 켜졌다.

멱등 upsert(slug 기준): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
재실행이 값을 안 되돌린다 — 시드 값이 곧 현 DB 값이라서다.

실행:  uv run python -m seed.seed_products
"""

from __future__ import annotations

import asyncio
from datetime import date

from sqlalchemy import select

from core.db import SessionLocal
from models import Career, Company, Product

# 제품 slug → (company slug, career title). seed_companies 가 먼저 돌아야 한다.
CAREER_OF: dict[str, tuple[str, str]] = {
    "mediness": ("medisolve-ai", "AX 리더"),
}

PRODUCTS: list[dict] = [
    {
        "slug": "mediness",
        "title": "Mediness",
        "summary": "문서·회의·의사결정·업무를 한 자리에 모은 사내 AX 워크스페이스",
        "detail_path": "para/projects/company/mediness/showcase.md",
        "category": "web",
        "status": "live",
        "started_on": date(2026, 5, 1),
        "stack": [
            "FastAPI", "PostgreSQL", "Redis", "SQLAlchemy", "Alembic",
            "Next.js", "TypeScript", "Tailwind CSS", "WebSocket", "MCP",
            "Docker Compose", "Prometheus", "Grafana", "Tauri",
        ],
        "thumbnail": None,
        "links": None,
        "visible": True,
    },
]


async def seed() -> None:
    async with SessionLocal() as session:
        for fields in PRODUCTS:
            slug = fields["slug"]
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

            fields = {**fields, "career_id": career.id}

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
