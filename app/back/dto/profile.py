"""프로필 DTO — 내부 계층 이동용. 신원·연락만 — 문구는 site_config."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileDTO:
    id: int

    handle: str
    name: str
    role: str
    years: str | None
    location: str | None
    focus: str | None
    avatar_url: str | None

    email: str
    github: str | None
    linkedin: str | None

    stack: list[str] | None
