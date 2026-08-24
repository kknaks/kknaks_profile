"""사용자 DTO — 내부 계층 이동용. ORM 은 repository 를 넘지 않는다."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    id: int
    profile_id: int
    username: str
    password_hash: str
    system_role: str
