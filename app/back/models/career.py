"""career — 직장에서의 역할 (erd.md §career).

한 행 = 역할 하나. 같은 회사에서 직무가 바뀌면 행이 하나 더 생긴다.
detail_path 를 두지 않는다 — 역할 서술은 짧아서 컬럼(description)이 낫다.
is_current · period · display_order 는 컬럼이 아니다 — 각각 ended_on IS NULL,
두 날짜의 렌더, started_on DESC 다.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Career(Base, TimestampMixin):
    __tablename__ = "career"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE")
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE")
    )

    title: Mapped[str] = mapped_column(String(64))                      # 백엔드 개발자

    started_on: Mapped[date] = mapped_column(Date)                      # 월 단위라 1일로
    ended_on: Mapped[date | None] = mapped_column(Date)                 # NULL 이면 현재 역할

    summary: Mapped[str | None] = mapped_column(Text)                   # 카드에 뜨는 한 줄
    description: Mapped[str | None] = mapped_column(Text)               # 맡은 역할. 펼쳤을 때
    stack: Mapped[list[str] | None] = mapped_column(ARRAY(Text))

    __table_args__ = (Index("ix_career_started", started_on.desc()),)
