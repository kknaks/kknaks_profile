"""content — 영상 + 교안 (erd.md §content). 원장은 para/resources/youtube/.

note 와 표면 모양이 같고 영상 세 필드만 다르다.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Content(Base, TimestampMixin):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE")
    )

    slug: Mapped[str] = mapped_column(String(64), unique=True)          # C-025
    title: Mapped[str] = mapped_column(String(128))
    summary: Mapped[str | None] = mapped_column(Text)
    detail_path: Mapped[str] = mapped_column(String(255))               # para/resources/youtube/*.md

    youtube_id: Mapped[str] = mapped_column(String(16))
    duration: Mapped[str | None] = mapped_column(String(16))            # 3:58
    speaker: Mapped[str | None] = mapped_column(String(64))             # 출처 채널

    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    published_on: Mapped[date | None] = mapped_column(Date)
    visible: Mapped[bool] = mapped_column(default=True, server_default="true")

    __table_args__ = (Index("ix_content_published", published_on.desc()),)
