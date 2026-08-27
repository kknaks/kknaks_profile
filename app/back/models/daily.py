"""daily — 하루 요약 (커밋 AI 요약 파이프라인).

commit 을 KST 날짜로 묶은 하루치 AI 요약이 앉는 표다. date 가 PK — 날짜당
정확히 한 행. summary 는 레포 단위 불릿을 줄바꿈으로 이은 텍스트고, 공개
표면(/api/activity)의 잔디 툴팁이 이것만 읽는다(커밋 원문 fallback 없음).

error 는 요약 실패 사유 — repo.last_error 규약과 같다: 성공하면 비운다.
실패한 날짜는 다음 판(최근 7일 창)이 자동 재시도한다.
"""

from __future__ import annotations

from datetime import date as date_

from sqlalchemy import Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class Daily(Base, TimestampMixin):
    __tablename__ = "daily"

    date: Mapped[date_] = mapped_column(Date, primary_key=True)  # KST 날짜
    summary: Mapped[str | None] = mapped_column(Text)  # 불릿 — 줄바꿈 구분
    error: Mapped[str | None] = mapped_column(Text)    # 실패 사유. 성공하면 비운다
