"""commit — 수집한 커밋 (erd.md §commit).

리베이스가 같은 작업을 새 sha 로 되풀이하므로 중복 제거 키가 sha 가 아니라
(repo_id, tree) 다. authored_at 이 커미터 날짜가 아닌 것도 같은 이유다.
message 는 원문이라 공개하지 않는다 — 잔디에 뜨는 것은 summary 다.
updated_at 이 없다 — 수집된 커밋은 고치지 않는다(erd 가 created_at 만 갖는다).
예외는 AI 요약 하나 — summary 를 AI 한 줄로 덮고 summarized_at 을 찍는다.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Commit(Base):
    __tablename__ = "commit"
    __table_args__ = (
        UniqueConstraint("repo_id", "tree", name="uq_commit_repo_tree"),
        Index("ix_commit_authored", text("authored_at DESC")),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    repo_id: Mapped[int] = mapped_column(ForeignKey("repo.id", ondelete="CASCADE"))

    sha: Mapped[str] = mapped_column(String(40))
    tree: Mapped[str] = mapped_column(String(40))                        # 중복 제거의 진짜 키
    author: Mapped[str | None] = mapped_column(String(128))
    authored_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # author 날짜
    message: Mapped[str | None] = mapped_column(Text)                    # 원문. 공개하지 않는다
    summary: Mapped[str | None] = mapped_column(Text)                    # 한 줄 요약. 잔디에 뜬다
    summarized_at: Mapped[datetime | None] = mapped_column(              # AI 요약 시각. NULL = 미요약
        DateTime(timezone=True)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
