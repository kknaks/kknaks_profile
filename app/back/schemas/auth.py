"""auth — front ↔ back 계약. 프론트 lib/api.ts authApi 와 1:1 이다."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserOut(BaseModel):
    username: str
    role: str


class LoginResponse(BaseModel):
    user: UserOut


class LogoutResponse(BaseModel):
    ok: bool
