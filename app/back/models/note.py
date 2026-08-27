"""note — 내가 쓴 글 (erd.md §note). 원장은 para/resources/note/.

모든 글이 자동으로 뜨지 않는다 — 공개할 것만 여기 등록한다 (케이스 4).
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Note(Base, TimestampMixin):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE")
    )

    slug: Mapped[str] = mapped_column(String(64), unique=True)
    title: Mapped[str] = mapped_column(String(128))
    summary: Mapped[str | None] = mapped_column(Text)                   # 카드에 뜨는 한 줄
    detail_path: Mapped[str] = mapped_column(String(255))               # para/resources/note/*.md

    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    published_on: Mapped[date | None] = mapped_column(Date)
    visible: Mapped[bool] = mapped_column(default=True, server_default="true")

    __table_args__ = (Index("ix_note_published", published_on.desc()),)
