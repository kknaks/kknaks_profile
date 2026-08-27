"""project — 혼자 만든 것 (erd.md §project).

**career 가 아니라 profile 에 바로 붙는다.** 혼자 하는 것이라 소속이 없어서지
비어 있는 게 아니다. 상세 본문은 DB 에 없다 — detail_path 가
para/projects/summer-star/<slug>/showcase.md 를 가리킨다(정보는 DB, 상세는 md).
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profile.id", ondelete="CASCADE")
    )                                                                   # 1인 사이트 — 첫 profile, 서버가 채운다

    slug: Mapped[str] = mapped_column(String(64), unique=True)          # wine-log — 디렉토리명
    title: Mapped[str] = mapped_column(String(64))
    summary: Mapped[str | None] = mapped_column(Text)                   # 카드에 뜨는 한 줄
    detail_path: Mapped[str | None] = mapped_column(String(255))        # 상세 md. NULL 이면 상세 없음

    category: Mapped[str | None] = mapped_column(String(32))            # mobile / web / cli
    status: Mapped[str | None] = mapped_column(String(16))              # live / wip / archived
    started_on: Mapped[date | None] = mapped_column(Date)

    stack: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    thumbnail: Mapped[str | None] = mapped_column(String(255))
    links: Mapped[dict[str, Any] | None] = mapped_column(JSONB)         # {repo, site, store}
    visible: Mapped[bool] = mapped_column(default=True, server_default="true")
