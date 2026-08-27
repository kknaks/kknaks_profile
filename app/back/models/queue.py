"""queue — 인박스 파이프라인 한 건 (erd.md §queue).

표면에 안 뜬다. 모달에서 넣은 것(종류·URL·메모)과 처리 상태가 전부다 —
파이프라인 상태는 문서가 아니라 DB 가 갖는다(리뉴얼 결정). 행은 done 이 돼도
안 지운다 — 넣은 URL 의 기록이 여기 영구히 남는다.
"""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Queue(Base, TimestampMixin):
    __tablename__ = "queue"

    id: Mapped[int] = mapped_column(primary_key=True)

    kind: Mapped[str] = mapped_column(String(16))                # youtube / docs / article / blog
    source_url: Mapped[str | None] = mapped_column(String(512))  # book·session 은 NULL
    note: Mapped[str | None] = mapped_column(Text)               # 모달 메모

    # queued → processing → review → done. 실패는 failed(재시도 가능)
    status: Mapped[str] = mapped_column(
        String(16), default="queued", server_default="queued"
    )
    error: Mapped[str | None] = mapped_column(Text)              # 실패 사유. 성공하면 비운다

    # codex 세션 — 문서 생성이 남기고 개념 생성이 resume 으로 이어받는다
    ai_session_id: Mapped[str | None] = mapped_column(String(64))
