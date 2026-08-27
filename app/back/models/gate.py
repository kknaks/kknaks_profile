"""gate — 승인 지점 (erd.md §gate).

한 행 = 게이트 하나. 케이스 1 은 건마다 둘이다 — document(문서 초안) 승인 후
concept(개념 보강안). 초안은 payload(jsonb)에만 산다 — md 는 승인 시점에 착지하고,
푸시 성공(commit_ref)이 DB 확정의 증거다.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Gate(Base, TimestampMixin):
    __tablename__ = "gate"

    id: Mapped[int] = mapped_column(primary_key=True)
    queue_id: Mapped[int] = mapped_column(
        ForeignKey("queue.id", ondelete="CASCADE")
    )

    stage: Mapped[str] = mapped_column(String(16))               # document / concept
    payload: Mapped[dict] = mapped_column(JSONB)                 # 초안. 승인 때 다듬은 것으로 덮인다
    status: Mapped[str] = mapped_column(
        String(16), default="open", server_default="open"        # open / approved / rejected
    )
    commit_ref: Mapped[str | None] = mapped_column(String(40))   # 푸시 성공의 증거
    result: Mapped[dict | None] = mapped_column(JSONB)           # content_id · 파일 경로
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (UniqueConstraint("queue_id", "stage", name="uq_gate_queue_stage"),)
