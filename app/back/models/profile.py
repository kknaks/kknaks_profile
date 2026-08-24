"""profile — 루트 테이블. 신원·연락만 갖는다 (erd.md §profile).

1인 사이트라 표면에 뜨는 문구(히어로·소개·카드)는 전부 site_config 로 갔다.
"""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Profile(Base, TimestampMixin):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)

    # 신원. /about 상단.
    handle: Mapped[str] = mapped_column(String(64))                     # kknaks
    name: Mapped[str] = mapped_column(String(64))                       # 이건학
    role: Mapped[str] = mapped_column(String(64))                       # 백엔드 엔지니어 — 직함
    years: Mapped[str | None] = mapped_column(String(32))               # 1년차
    location: Mapped[str | None] = mapped_column(String(64))            # 서울, 대한민국
    focus: Mapped[str | None] = mapped_column(String(128))              # AI · Python · Infra
    avatar_url: Mapped[str | None] = mapped_column(String(255))

    # 연락. /about + footer.
    email: Mapped[str] = mapped_column(String(255))
    github: Mapped[str | None] = mapped_column(String(255))
    linkedin: Mapped[str | None] = mapped_column(String(255))

    stack: Mapped[list[str] | None] = mapped_column(ARRAY(Text))        # 기술 뱃지 — 내 스택
