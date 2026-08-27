"""education 시드 — 원료는 _archive/persona/career/{bitcamp,likelion}.md frontmatter (ko 값만).

옛 스키마에선 career 로 앉아 있었지만 erd 기준 education 몫이라 여기서 넣는다.
detail_path 는 비워 둔다 — 상세 md 원장이 아직 없다. 추측으로 메우지 않는다.

멱등 upsert(키: org + title + started_on): 없으면 넣고, 있으면 시드 값으로 덮어쓴다.
어드민에서 고치기 시작한 뒤에는 돌리지 않는다.

실행:  uv run python -m seed.seed_education
"""

from __future__ import annotations

import asyncio
from datetime import date

from sqlalchemy import select

from core.db import SessionLocal
from models import Education, Profile

EDUCATIONS: list[dict] = [
    {
        "org": "멋쟁이사자처럼",
        "title": "풀스택 엔지니어 심화과정",
        "location": "서울",
        "started_on": date(2024, 12, 1),
        "ended_on": date(2025, 3, 1),
        "summary": "2개 프로젝트, 자바 및 인프라 심화과정",
        "detail_path": None,
        "stack": ["Spring", "ELK", "Postgres", "Kubernetes", "React"],
    },
    {
        "org": "비트캠프",
        "title": "풀스택 엔지니어 과정",
        "location": "서울",
        "started_on": date(2024, 6, 1),
        "ended_on": date(2024, 12, 1),
        "summary": "풀스택 클라우드 엔지니어 기초과정",
        "detail_path": None,
        "stack": ["Java", "Spring", "MyBatis", "MySQL", "NCP", "JavaScript"],
    },
]


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            raise SystemExit("profile 이 없다 — seed_profile 을 먼저 돌린다")

        for fields in EDUCATIONS:
            # 멱등 키: (org, title, started_on) — 같은 기관 같은 과정 같은 시작
            row = (
                await session.execute(
                    select(Education).where(
                        Education.org == fields["org"],
                        Education.title == fields["title"],
                        Education.started_on == fields["started_on"],
                    )
                )
            ).scalar_one_or_none()
            if row is None:
                session.add(Education(profile_id=profile.id, **fields))
                print(f"education 생성 — {fields['org']} · {fields['title']}")
            else:
                for key, value in fields.items():
                    setattr(row, key, value)
                print(f"education 갱신 — {fields['org']} · {fields['title']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
