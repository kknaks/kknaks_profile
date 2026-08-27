"""repo — 커밋을 긁을 레포 (erd.md §repo).

부모가 둘(product / project)이지만 FK 를 살린다 — CHECK 가 정확히 하나만 허용한다.
수집 상태(last_fetched_at · last_error)를 행에 갖는다 — 레포마다 따로 막힌다.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Repo(Base, TimestampMixin):
    __tablename__ = "repo"
    __table_args__ = (
        # 둘 중 정확히 하나에만 속한다.
        CheckConstraint(
            "(product_id IS NULL) <> (project_id IS NULL)",
            name="ck_repo_one_parent",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE")
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE")
    )

    slug: Mapped[str] = mapped_column(String(160), unique=True)          # owner/name
    role: Mapped[str | None] = mapped_column(String(32))                 # spec / app / infra
    git_token_id: Mapped[int | None] = mapped_column(                    # 수집 토큰. NULL 무토큰(공개)
        ForeignKey("git_token.id", ondelete="SET NULL")
    )

    enabled: Mapped[bool] = mapped_column(default=True, server_default="true")  # 끄기. 지우지 않는다

    last_fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error: Mapped[str | None] = mapped_column(Text)                 # 성공하면 비운다
