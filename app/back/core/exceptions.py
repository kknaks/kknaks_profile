"""도메인 예외 — service · repository 는 HTTPException 을 모른다.

계층 규약: 아래 층은 이 예외를 던지고, HTTP 상태로 바꾸는 것은
main.py 에 등록하는 핸들러 하나뿐이다. 응답 형태는 FastAPI 기본과 같은
{"detail": ...} 로 맞춘다 — 프론트 authFetch 가 detail 을 읽는다.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """도메인 예외 루트. status 는 HTTP 매핑 힌트일 뿐 아래 층은 의미를 모른다."""

    status = 500

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class NotFoundError(AppError):
    status = 404


class UnauthorizedError(AppError):
    status = 401


class ConflictError(AppError):
    status = 409


class ValidationError(AppError):
    status = 422


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status, content={"detail": exc.detail})
