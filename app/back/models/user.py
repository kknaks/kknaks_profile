"""users — 로그인 계정. 표면에 절대 나가지 않는다. 인증 수단일 뿐 소유자가 아니다."""

from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE")
    )

    username: Mapped[str] = mapped_column(String(64), unique=True)      # 로그인 ID
    password_hash: Mapped[str] = mapped_column(String(255))
    system_role: Mapped[str] = mapped_column(
        String(32), default="admin", server_default="admin"             # 권한. 직함과 다르다
    )
