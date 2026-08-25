"""company + career 시드 — 원료는 _archive/persona/career/ (ko 값만).

bitcamp·likelion 은 여기 없다 — erd 기준 education 몫이라 교육 시드에서 넣는다.
회사 소개·site·로고는 원료에 없던 것은 비워 둔다 — 추측으로 메우지 않는다.
어드민에서 채운다.

멱등 upsert(slug 기준): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
2026-08-25 실 DB 상태로 동기 — 어드민에서 고친 값(medisolve-ai github_org,
백엔드 개발자 ended_on, AX 리더 신설)을 반영했다. 재실행이 값을 안 되돌린다.

실행:  uv run python -m seed.seed_companies
"""

from __future__ import annotations

import asyncio
from datetime import date

from sqlalchemy import select

from core.db import SessionLocal
from models import Career, Company, Profile

COMPANIES = [
    {
        "slug": "medisolve-ai",
        "name": "메디솔브 AI",
        "description": "피부과 의료 ai 솔루션",
        "location": "서울",
        "github_org": "MediSolveAIDev",  # 어드민 입력(2026-08-25) — 레포 owner 후보
    },
    {
        "slug": "quantus",
        "name": "퀀터스",
        "description": None,
        "location": "서울",
        "github_org": None,
    },
    {
        "slug": "dowha-eng",
        "name": "도화 엔지니어링",
        "description": None,
        "location": "서울",
        "github_org": None,
    },
]

# (company_slug, career 필드) — 기간은 월 단위라 1일로 박는다.
CAREERS: list[tuple[str, dict]] = [
    (
        "medisolve-ai",
        {
            "title": "백엔드 개발자",
            "started_on": date(2026, 2, 1),
            "ended_on": date(2026, 6, 1),  # 어드민 입력 — 6월부터 AX 리더로 역할 전환
            "summary": "피부과 전용 CRM, MSO 제작, 사내 하네스 엔지니어링",
            "description": (
                "피부과 전용 CRM과 MSO(Multi-Site Operation) 백엔드를 맡고 있으며, "
                "레거시 의사결정 흐름을 Action Runtime의 정식 도메인으로 이식하는 "
                "워크플로 엔진과 그 워크플로가 노출하는 MCP tool 표면의 스펙·구현을 "
                "함께 주도하고 있다."
            ),
            "stack": ["Python", "FastAPI", "Postgres", "Vite", "LangChain"],
        },
    ),
    (
        # 어드민 입력(2026-08-25) — 같은 회사 두 번째 역할. product 시드가 이 행에 건다.
        "medisolve-ai",
        {
            "title": "AX 리더",
            "started_on": date(2026, 6, 1),
            "ended_on": None,
            "summary": "사내 AX 전환 프로젝트 리더, B2B AX 솔루션 개발",
            "description": None,
            "stack": ["FastAPI", "NextJS", "AI"],
        },
    ),
    (
        "quantus",
        {
            "title": "백엔드 개발자",
            "started_on": date(2025, 8, 1),
            "ended_on": date(2026, 2, 1),
            "summary": "퀀트시스템 개발, 뉴스공시 수집파이프라인 개발",
            "description": None,
            "stack": ["Python", "FastAPI", "MySQL", "Azure", "AWS", "ELK", "Airflow"],
        },
    ),
    (
        "dowha-eng",
        {
            "title": "토목 설계",
            "started_on": date(2020, 1, 1),
            "ended_on": date(2023, 12, 1),
            "summary": "상하수도분야 토목 설계",
            "description": None,
            "stack": ["AutoCAD", "Civil 3D"],
        },
    ),
]


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            raise SystemExit("profile 이 없다 — seed_profile 을 먼저 돌린다")

        companies: dict[str, Company] = {}
        for fields in COMPANIES:
            row = (
                await session.execute(
                    select(Company).where(Company.slug == fields["slug"])
                )
            ).scalar_one_or_none()
            if row is None:
                row = Company(**fields)
                session.add(row)
                await session.flush()
                print(f"company 생성 — {fields['slug']}")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"company 갱신 — {fields['slug']}")
            companies[fields["slug"]] = row

        for company_slug, fields in CAREERS:
            company = companies[company_slug]
            # 멱등 키: (company, title, started_on) — 같은 회사 같은 역할 같은 시작
            row = (
                await session.execute(
                    select(Career).where(
                        Career.company_id == company.id,
                        Career.title == fields["title"],
                        Career.started_on == fields["started_on"],
                    )
                )
            ).scalar_one_or_none()
            if row is None:
                session.add(
                    Career(profile_id=profile.id, company_id=company.id, **fields)
                )
                print(f"career 생성 — {company_slug} · {fields['title']}")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"career 갱신 — {company_slug} · {fields['title']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
