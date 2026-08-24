"""problem — 해결한 문제. 이력서의 알맹이다 (erd.md §problem).

한 행 = 푼 문제 하나. 원료는 para/projects/company/<제품>/log/ 의 SUMMARY.md §3 —
행이면 하나씩 옮길 수 있고 어느 제품에서 나온 것인지도 잇는다(케이스 6 게이트).
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Problem(Base, TimestampMixin):
    __tablename__ = "problem"

    id: Mapped[int] = mapped_column(primary_key=True)
    career_id: Mapped[int] = mapped_column(
        ForeignKey("career.id", ondelete="CASCADE")
    )
    # 제품에 매이지 않는 문제(조직·프로세스)도 있다 — NULL 허용.
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("product.id", ondelete="SET NULL")
    )

    title: Mapped[str] = mapped_column(String(128))                     # 무엇을 풀었나
    body: Mapped[str | None] = mapped_column(Text)                      # 어떻게 풀었나
    display_order: Mapped[int] = mapped_column(default=0, server_default="0")
