"""algorithm — 문제 풀이 (erd.md §algorithm). 원장은 para/resources/algorithms/.

「오늘의 문제」는 하나뿐이다 — 앱이 아니라 DB(partial unique index)가 강제한다.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Algorithm(Base, TimestampMixin):
    __tablename__ = "algorithm"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE")
    )

    slug: Mapped[str] = mapped_column(String(64), unique=True)          # a-001-two-sum (파일명 stem 소문자)
    title: Mapped[str] = mapped_column(String(128))                     # Two Sum
    difficulty: Mapped[str] = mapped_column(String(8))                  # easy / medium / hard
    summary: Mapped[str | None] = mapped_column(Text)

    # 출처. jsonb 로 접지 않는다 — 플랫폼·번호로 거르고 싶어진다.
    source_platform: Mapped[str] = mapped_column(String(32))            # leetcode
    source_number: Mapped[int | None] = mapped_column()
    source_url: Mapped[str | None] = mapped_column(String(255))
    curated_in: Mapped[list[str] | None] = mapped_column(ARRAY(Text))   # neetcode150 · blind75

    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    today: Mapped[bool] = mapped_column(default=False, server_default="false")
    detail_path: Mapped[str] = mapped_column(String(255))               # para/resources/algorithms/*.md
    published_on: Mapped[date | None] = mapped_column(Date)
    visible: Mapped[bool] = mapped_column(default=True, server_default="true")

    __table_args__ = (
        # 「오늘의 문제」는 하나뿐 — DB 가 강제한다.
        Index("uq_algorithm_today", today, unique=True, postgresql_where=text("today")),
        Index("ix_algorithm_published", published_on.desc()),
    )
