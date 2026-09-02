"""chat-tool — 1층. **MCP 서버만 부른다** (SPEC-017 §4 Tool Contract / DEC-027 D5).

전 엔드포인트 read-only 이고 인자는 slug · query · limit 뿐이다 — 경로 인자가 없다(D3).
노출 판정은 매 호출 DB 에서 돈다.

## 인증 = turn 전용 Bearer

이 표면은 「지금 도는 turn」만 부를 수 있다. 토큰이 없거나 만료·폐기면 401 이다 —
chat-tool 이 공개 데이터만 준다는 것과는 별개 축이다(DEC-027 D5).

응답은 얇은 봉투 하나로 통일한다: 목록은 `{items, count}`, 상세는 `{item}`. MCP 가
유형마다 다른 모양을 외우지 않아도 되게 — tool 사슬이 흔들리지 않는 조건이다.
"""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from core.chat_slugs import public_url
from core.exceptions import UnauthorizedError
from dto.chat_tool import ChatDocDTO
from service.chat.tool_service import chat_tool_service
from service.chat.turn_token import turn_token_service

router = APIRouter(prefix="/api/chat-tool", tags=["chat-tool"])


async def require_turn(request: Request, db: AsyncSession = Depends(get_db)) -> int:
    """`Authorization: Bearer <turn token>` 검증. 반환 = 그 turn 의 메시지 id.

    ⚠ 실패 사유(없음 · 만료 · 폐기)를 구분해 말하지 않는다 — 부르는 쪽은 코드가
    아니라 모델이고, 구분이 알려 주는 것은 우리 수명 관리뿐이다.
    """
    header = request.headers.get("authorization", "")
    token = header[7:].strip() if header.lower().startswith("bearer ") else None
    message = await turn_token_service.verify(db, token)
    if message is None:
        raise UnauthorizedError("invalid turn token")
    return message.id


def _item(doc: ChatDocDTO) -> dict:
    """DTO → 응답 dict. 근거 카드가 쓸 `url` 을 여기서 붙인다(§4 source)."""
    payload = asdict(doc)
    payload["url"] = public_url(doc.type, doc.slug)
    # body 가 None 이면 키를 두지 않는다 — 목록과 상세가 같은 모양이면서도
    # 「본문이 비었다」와 「본문 자리가 없다」가 섞이지 않는다.
    if payload.get("body") is None:
        payload.pop("body", None)
    if not payload.get("meta"):
        payload.pop("meta", None)
    return payload


def _items(docs: list[ChatDocDTO]) -> dict:
    return {"items": [_item(d) for d in docs], "count": len(docs)}


@router.get("/profile", dependencies=[Depends(require_turn)])
async def get_profile(db: AsyncSession = Depends(get_db)) -> dict:
    return {"item": asdict(await chat_tool_service.get_profile(db))}


@router.get("/careers", dependencies=[Depends(require_turn)])
async def list_careers(
    limit: int | None = Query(default=None), db: AsyncSession = Depends(get_db)
) -> dict:
    return _items(await chat_tool_service.list_careers(db, limit))


@router.get("/careers/{slug}", dependencies=[Depends(require_turn)])
async def get_career(slug: str, db: AsyncSession = Depends(get_db)) -> dict:
    return {"item": _item(await chat_tool_service.get_career(db, slug))}


@router.get("/projects", dependencies=[Depends(require_turn)])
async def list_projects(
    limit: int | None = Query(default=None), db: AsyncSession = Depends(get_db)
) -> dict:
    return _items(await chat_tool_service.list_projects(db, limit))


@router.get("/projects/{slug}", dependencies=[Depends(require_turn)])
async def get_project(slug: str, db: AsyncSession = Depends(get_db)) -> dict:
    return {"item": _item(await chat_tool_service.get_project(db, slug))}


@router.get("/problems", dependencies=[Depends(require_turn)])
async def list_problems(
    limit: int | None = Query(default=None), db: AsyncSession = Depends(get_db)
) -> dict:
    return _items(await chat_tool_service.list_problems(db, limit))


@router.get("/problems/{slug}", dependencies=[Depends(require_turn)])
async def get_problem(slug: str, db: AsyncSession = Depends(get_db)) -> dict:
    return {"item": _item(await chat_tool_service.get_problem(db, slug))}


@router.get("/company-products", dependencies=[Depends(require_turn)])
async def list_company_products(
    limit: int | None = Query(default=None), db: AsyncSession = Depends(get_db)
) -> dict:
    return _items(await chat_tool_service.list_company_products(db, limit))


@router.get("/company-products/{slug}", dependencies=[Depends(require_turn)])
async def get_company_product(slug: str, db: AsyncSession = Depends(get_db)) -> dict:
    return {"item": _item(await chat_tool_service.get_company_product(db, slug))}


@router.get("/notes", dependencies=[Depends(require_turn)])
async def search_notes(
    query: str | None = Query(default=None),
    limit: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return _items(await chat_tool_service.search_notes(db, query, limit))


@router.get("/notes/{slug}", dependencies=[Depends(require_turn)])
async def get_note(slug: str, db: AsyncSession = Depends(get_db)) -> dict:
    return {"item": _item(await chat_tool_service.get_note(db, slug))}


@router.get("/contents", dependencies=[Depends(require_turn)])
async def list_contents(
    limit: int | None = Query(default=None), db: AsyncSession = Depends(get_db)
) -> dict:
    return _items(await chat_tool_service.list_contents(db, limit))


@router.get("/algorithms", dependencies=[Depends(require_turn)])
async def list_algorithms(
    limit: int | None = Query(default=None), db: AsyncSession = Depends(get_db)
) -> dict:
    return _items(await chat_tool_service.list_algorithms(db, limit))
