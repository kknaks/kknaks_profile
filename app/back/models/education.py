"""education — 교육과정 (erd.md §education).

career 와 모양이 같지만 커밋이 붙지 않는다 — 교육과정에서 만든 결과물은
project 로 가지 과정 자체에 커밋이 귀속되지 않는다.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Education(Base, TimestampMixin):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE")
    )

    org: Mapped[str] = mapped_column(String(64))                        # 멋쟁이사자처럼 / 비트캠프
    title: Mapped[str] = mapped_column(String(64))                      # 풀스택 엔지니어 심화과정
    location: Mapped[str | None] = mapped_column(String(64))

    started_on: Mapped[date] = mapped_column(Date)
    ended_on: Mapped[date | None] = mapped_column(Date)

    summary: Mapped[str | None] = mapped_column(Text)
    detail_path: Mapped[str | None] = mapped_column(String(255))        # 상세 md. NULL 이면 상세 없음
    stack: Mapped[list[str] | None] = mapped_column(ARRAY(Text))

    __table_args__ = (Index("ix_education_started", started_on.desc()),)
