"""admin 계정 시드 — 멱등. 몇 번을 돌려도 같은 상태가 된다.

- 계정은 .env 의 ADMIN_USERNAME / ADMIN_PASSWORD 로 만든다
- users.profile_id 가 NOT NULL 이라 profile 이 없으면 최소 스텁을 먼저 만든다.
  스텁 내용은 어드민 프로필 화면에서 고친다 — 여기는 FK 를 세울 뿐이다
- 이미 있으면 비밀번호 해시만 갱신한다 (.env 비번을 바꾸고 다시 돌리면 반영)

실행:  uv run python -m seed.seed_users
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select

from config import get_settings
from core.db import SessionLocal
from core.security import hash_password
from models import Profile, User


async def seed() -> None:
    settings = get_settings()
    async with SessionLocal() as session:
        profile = (
            await session.execute(select(Profile).order_by(Profile.id).limit(1))
        ).scalar_one_or_none()
        if profile is None:
            profile = Profile(
                handle="kknaks",
                name="이건학",
                role="백엔드 엔지니어",
                email="kknaks@kknaks.dev",  # 스텁 — 어드민에서 고친다
            )
            session.add(profile)
            await session.flush()
            print(f"profile 스텁 생성 — id={profile.id}")

        user = (
            await session.execute(
                select(User).where(User.username == settings.admin_username)
            )
        ).scalar_one_or_none()
        if user is None:
            session.add(
                User(
                    profile_id=profile.id,
                    username=settings.admin_username,
                    password_hash=hash_password(settings.admin_password),
                )
            )
            print(f"admin 생성 — username={settings.admin_username}")
        else:
            user.password_hash = hash_password(settings.admin_password)
            print(f"admin 비밀번호 갱신 — username={settings.admin_username}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
