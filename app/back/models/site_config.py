"""site_config — 사이트에 뜨는 문구 전부. key-value (erd.md §site_config).

value 는 jsonb — 문자열은 JSON string, 구조(hero_headline·cards)는 배열/객체.
created_at 이 없다 — key 가 곧 정체성이라 갱신만 있다.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class SiteConfig(Base):
    __tablename__ = "site_config"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)      # home.hero_headline
    value: Mapped[Any] = mapped_column(JSONB)
    note: Mapped[str | None] = mapped_column(Text)                      # 어디에 쓰이는지

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
