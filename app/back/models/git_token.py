"""git_token — 커밋 수집용 GitHub 토큰 (erd.md §git_token).

토큰은 **암호문**으로만 저장한다 — 복호 키는 .env 의 GIT_TOKEN_KEY 가 갖는다.
개인 n개·회사 n개 전부 행이다. 이직하면 회사 토큰 행만 갈아끼운다 — repo 는 안 바뀐다.
users 에 붙이지 않는다 — users 는 로그인 계정(1행)이고 토큰은 n개라 자리가 다르다.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, TimestampMixin


class GitToken(Base, TimestampMixin):
    __tablename__ = "git_token"

    id: Mapped[int] = mapped_column(primary_key=True)

    kind: Mapped[str] = mapped_column(String(16))        # 구분 — personal / company
    account: Mapped[str] = mapped_column(String(64))     # 깃 계정 id — kknaks / kknaksss
    email: Mapped[str] = mapped_column(String(255))      # 착지 커밋의 git 신원(user.email)에 쓴다
    token_cipher: Mapped[str] = mapped_column(Text)      # Fernet 암호문. 원문은 저장 안 함

    company_id: Mapped[int | None] = mapped_column(      # kind=company 토큰의 소속. personal 은 NULL
        ForeignKey("company.id", ondelete="SET NULL")
    )

    enabled: Mapped[bool] = mapped_column(default=True, server_default="true")  # 끄면 무토큰 취급. 지우지 않는다
