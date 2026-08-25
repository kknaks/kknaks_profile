"""company — 어디에 있었나 (erd.md §company).

career 에서 뗀다 — 회사 소개와 제품은 회사 속성이지 역할 속성이 아니다.
재직 기간은 컬럼이 아니다: 그 회사 career 행들의 최소·최대다.
"""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)

    slug: Mapped[str] = mapped_column(String(64), unique=True)          # medisolve-ai
    name: Mapped[str] = mapped_column(String(64))                       # 메디솔브 AI
    description: Mapped[str | None] = mapped_column(Text)               # 회사 소개
    location: Mapped[str | None] = mapped_column(String(64))            # 서울
    site: Mapped[str | None] = mapped_column(String(255))
    logo_url: Mapped[str | None] = mapped_column(String(255))
    github_org: Mapped[str | None] = mapped_column(String(64))          # GitHub 조직(owner) — 레포 owner 드롭다운 후보
