"""profile 시드 — 내 개인 정보(신원·연락·스택)만. 문구는 seed_site_config 가 넣는다.

원료는 _archive/persona/profile.md (ko 값만, erd 컬럼만).

멱등 upsert: 첫 행이 없으면 만들고, 있으면 시드 값으로 덮어쓴다.
어드민에서 내용을 고치기 시작한 뒤에는 돌리지 않는다.

실행:  uv run python -m seed.seed_profile
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select

from core.db import SessionLocal
from models import Profile

SEED = {
    # 신원
    "handle": "kknaks",
    "name": "이건학",
    "role": "백엔드 엔지니어",
    "years": "1년차",
    "location": "서울, 대한민국",
    "focus": "AI · Python · Infra · mobile",
    "avatar_url": "/assets/profile/me.png",
    # 연락
    "email": "kknaks@gmail.com",
    "github": "github.com/kknaks",
    "linkedin": "linkedin.com/in/kknaks",
    # 스택
    "stack": [
        "Python",
        "FastAPI",
        "Postgres",
        "Next.js",
        "React Native",
        "Redis",
        "LangGraph",
        "Docker",
        "Linux",
    ],
}


async def seed() -> None:
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            session.add(Profile(**SEED))
            print("profile 생성")
        else:
            for key, value in SEED.items():
                setattr(profile, key, value)
            print(f"profile 갱신 — id={profile.id} (시드 값으로 덮어씀)")
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
