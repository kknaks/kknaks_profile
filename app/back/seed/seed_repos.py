"""repo 시드 — 잔디가 커밋을 긁을 레포 목록. 2026-08-25 실 DB 상태 기준.

부모(product/project)는 slug 로 찾아 건다 — seed_products·seed_projects 가
먼저 돌아야 한다.

**git_token_id 는 시드에 넣지 않는다.** 토큰은 비밀(git_token 표, Fernet
암호문)이라 시드 대상이 아니고, 어느 레포가 어느 토큰을 쓰는지도 그 비밀에
딸린 연결이다. 시드 후 어드민(설정 → 토큰)에서 사람이 다시 연결한다.
같은 이유로 재실행이 기존 행의 git_token_id 를 건드리지 않는다.

수집 상태(last_fetched_at·last_error)도 시드가 만들지 않는다 — 수집기의
런타임 기록이라 재실행이 되돌리면 안 된다.

검증용 가짜 레포(kknaks/this-repo-does-not-exist-xyz)는 시드에서 뺐다 —
수집 에러 표시를 확인하려고 실 DB 에만 넣어 둔 행이다.

멱등 upsert(slug 기준): 없으면 넣고, 있으면 role·enabled·부모 연결만 덮어쓴다.

실행:  uv run python -m seed.seed_repos
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select

from core.db import SessionLocal
from models import Product, Project, Repo

# (slug, role, 부모 종류, 부모 slug) — 부모는 product/project 중 정확히 하나.
REPOS: list[tuple[str, str | None, str, str]] = [
    ("kknaks/mac-remote", "app", "project", "mac-remote"),
    ("kknaks/study_timelapse", "app", "project", "study-timelapse"),
    ("kknaks/open_kknaks", "app", "project", "open-kknaks"),
    ("kknaks/summer_star_company", None, "project", "summer-star-company"),
    ("MediSolveAIDev/mediness", None, "product", "mediness"),
    ("MediSolveAIDev/mediness-app", None, "product", "mediness"),
]


async def seed() -> None:
    async with SessionLocal() as session:
        for slug, role, parent_kind, parent_slug in REPOS:
            if parent_kind == "product":
                parent = (
                    await session.execute(
                        select(Product).where(Product.slug == parent_slug)
                    )
                ).scalar_one_or_none()
                parent_fields = {"product_id": parent.id if parent else None,
                                 "project_id": None}
            else:
                parent = (
                    await session.execute(
                        select(Project).where(Project.slug == parent_slug)
                    )
                ).scalar_one_or_none()
                parent_fields = {"product_id": None,
                                 "project_id": parent.id if parent else None}
            if parent is None:
                raise SystemExit(
                    f"{parent_kind} 가 없다 — {parent_slug}. "
                    "seed_products·seed_projects 를 먼저 돌린다"
                )

            fields = {"slug": slug, "role": role, "enabled": True, **parent_fields}

            row = (
                await session.execute(select(Repo).where(Repo.slug == slug))
            ).scalar_one_or_none()
            if row is None:
                # git_token_id·last_fetched_at·last_error 는 넣지 않는다(머리 주석).
                session.add(Repo(**fields))
                print(f"repo 생성 — {slug} → {parent_kind}:{parent_slug}")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"repo 갱신 — {slug} → {parent_kind}:{parent_slug}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
