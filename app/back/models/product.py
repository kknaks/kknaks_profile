"""product — 회사에서 만든 것 (erd.md §product).

**company 가 아니라 career 에 속한다.** 회사의 제품 카탈로그가 아니라
「내가 그 역할에서 만든 것」의 기록이다 — 회사는 career.company_id 를 거쳐 닿는다.
상세 본문은 DB 에 없다 — detail_path 가 md 를 가리킨다(정보는 DB, 상세는 md).
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_id: Mapped[int] = mapped_column(
        ForeignKey("career.id", ondelete="CASCADE")
    )                                                                   # 어느 역할에서 만들었나

    slug: Mapped[str] = mapped_column(String(64), unique=True)          # mediness
    title: Mapped[str] = mapped_column(String(64))
    summary: Mapped[str | None] = mapped_column(Text)                   # 카드에 뜨는 한 줄
    detail_path: Mapped[str | None] = mapped_column(String(255))        # 상세 md. NULL 이면 상세 없음

    category: Mapped[str | None] = mapped_column(String(32))
    status: Mapped[str | None] = mapped_column(String(16))              # live / wip / archived
    started_on: Mapped[date | None] = mapped_column(Date)

    stack: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    thumbnail: Mapped[str | None] = mapped_column(String(255))
    links: Mapped[dict[str, Any] | None] = mapped_column(JSONB)         # {site, docs}
    visible: Mapped[bool] = mapped_column(default=True, server_default="true")
