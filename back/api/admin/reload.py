"""POST /admin/reload — 페르소나 git push 후 webhook 트리거 (ADR-03 §4.2).

토큰 인증은 단순 화이트리스트 (env `RELOAD_TOKEN`).
M8에서 GitHub webhook HMAC-SHA256 검증으로 강화 예정 (advisor §4.3 nit).
"""

from fastapi import APIRouter, Header, HTTPException

import config

router = APIRouter()


@router.post("/admin/reload")
def reload(x_reload_token: str | None = Header(default=None)):
    expected = config.reload_token()
    if not expected:
        raise HTTPException(500, "RELOAD_TOKEN not configured")
    if x_reload_token != expected:
        raise HTTPException(403, "invalid token")

    from main import load_all

    load_all()
    return {"status": "reloaded"}
