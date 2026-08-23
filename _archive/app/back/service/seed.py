"""관리자 유저 시드 (auth-01 §유저 시드).

부팅 시 .env 의 ADMIN_USERNAME/ADMIN_PASSWORD 로 users 행을 멱등 upsert 한다.
- 없으면 생성, 있으면 비밀번호 해시를 현재 .env 값으로 갱신(비번 로테이션 지원).
- DB 미가용(마이그레이션 전/DB 다운)이면 로그만 남기고 부팅은 계속 — 콘텐츠 API 는 DB 무관.
"""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import config
from core.db import get_engine
from core.models import User
from core.security import hash_password

logger = logging.getLogger("kknaks-back.seed")


async def seed_admin() -> bool:
    """.env admin 계정을 upsert. 성공 True, DB 미가용 등 실패 False (부팅 비차단)."""
    username = config.admin_username()
    password = config.admin_password()
    try:
        async with AsyncSession(get_engine()) as db:
            user = (
                await db.execute(select(User).where(User.username == username))
            ).scalar_one_or_none()
            if user is None:
                db.add(User(username=username, password_hash=hash_password(password), role="admin"))
                logger.info("seeded admin user %r", username)
            else:
                user.password_hash = hash_password(password)
                logger.info("refreshed admin user %r password from env", username)
            await db.commit()
        return True
    except SQLAlchemyError as e:
        logger.warning("admin seed skipped — DB unavailable (%s)", e.__class__.__name__)
        return False
