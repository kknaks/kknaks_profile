"""para 자산 서빙 — 1층.

- GET /api/assets/{path} — 공개. para/** 하위의 이미지 파일만 내려준다

원장(md)이 자기 옆 assets/ 에 이미지를 갖는다 — showcase.md 의 상대참조와
DB thumbnail(para 상대경로)이 전부 여기로 온다. md 를 read_detail 이 읽어주듯
이미지는 이 라우터가 읽어준다(정보는 DB, 상세·자산은 para).

경로는 para/ 밖을 못 나간다 — resolve 후 포함 검사로 탈출(..)을 막는다.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from config import get_settings
from core.exceptions import NotFoundError

router = APIRouter(prefix="/api/assets", tags=["assets"])

# 이미지만 — md 본문은 body 로 나가고, 그 외 파일을 뚫어줄 이유가 없다.
_ALLOWED_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"})


@router.get("/{path:path}")
async def get_asset(path: str) -> FileResponse:
    root = (Path(get_settings().repo_root) / "para").resolve()
    target = (Path(get_settings().repo_root) / path).resolve()
    if not target.is_relative_to(root):
        raise NotFoundError("asset not found")
    if target.suffix.lower() not in _ALLOWED_SUFFIXES:
        raise NotFoundError("asset not found")
    if not target.is_file():
        raise NotFoundError("asset not found")
    return FileResponse(target)
