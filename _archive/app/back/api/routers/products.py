"""제품 레지스트리 admin API (KDEV-WORK-018 P3 / KDEV-SPEC-014 §4).

**HTTP 경계다.** 여기서 하는 일은 셋뿐 — 요청을 스키마로 받고, service 를 부르고,
도메인 예외를 상태코드로 바꾼다. `select()` 도 ORM 도 도메인 규칙도 없다
(`40-architecture/system` 「백엔드 계층 규약」).

예외 매핑은 `api/routers/queue.py:414 _gate_error()` 와 같은 형태다 — service 가
`HTTPException` 을 던지면 CLI·잡에서 같은 코드를 못 쓴다.
"""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import config
from api.routers.auth import require_admin
from api.schemas.products import (
    DiscoveredResponse,
    DiscoveredRow,
    OptionsResponse,
    PatchRequest,
    RegisterRequest,
    RegistryList,
    CardInput,
    RegistryRow,
    SyncResponse,
    VisibleRequest,
)
from core.db import get_db, new_session
from service.products import discover, registry, validate
from service.products.dto import TrackedRepoDTO
from service.products.errors import ProductError, ProductNotFound, ScaffoldError

logger = logging.getLogger("kknaks-back.products")

router = APIRouter(
    prefix="/api/admin/products",
    tags=["products"],
    dependencies=[Depends(require_admin)],
)


def _http_error(exc: ProductError | ScaffoldError) -> HTTPException:
    """도메인 예외 → HTTP.

    검증 실패는 **422**(입력이 계약을 어겼다), 파일·git 실패는 **500**(입력은 옳았고
    서버가 못 했다). 사람이 고칠 곳이 다르므로 코드를 나눈다.
    """
    if isinstance(exc, ProductError):
        return HTTPException(422, detail=exc.as_dict())
    return HTTPException(500, detail={"code": exc.code, "message": exc.message})


def _row(dto: TrackedRepoDTO, repo_root: Path) -> RegistryRow:
    """DTO + 파생 둘. **파생은 저장하지 않고 여기서 판정한다.**"""
    return RegistryRow(
        id=dto.id,
        slug=dto.slug,
        type=dto.type,
        detail=dto.detail,
        product_slug=dto.product_slug,
        account=dto.account,
        enabled=dto.enabled,
        last_fetched_at=dto.last_fetched_at,
        last_error=dto.last_error,
        product_exists=registry.product_exists(dto.product_slug, repo_root),
        card_visible=registry.card_visible(dto.product_slug, repo_root),
    )


@router.get("", response_model=RegistryList)
async def list_products(db: AsyncSession = Depends(get_db)) -> RegistryList:
    root = config.repo_root()
    rows = await registry.list_rows(db)
    return RegistryList(items=[_row(r, root) for r in rows])


@router.get("/options", response_model=OptionsResponse)
async def options() -> OptionsResponse:
    """폼 선택지. **분류를 자유입력으로 두면 사이트가 멈춘다.**"""
    root = config.repo_root()
    products = sorted(p.name for p in (root / "products").iterdir() if p.is_dir())
    careers = sorted(
        p.stem for p in (root / "persona" / "career").glob("*.md")
    )
    return OptionsResponse(
        products=products,
        categories=validate.load_categories(root),
        statuses=list(validate.CARD_STATUSES),
        careers=careers,
    )


@router.get("/undiscovered", response_model=DiscoveredResponse)
async def undiscovered(db: AsyncSession = Depends(get_db)) -> DiscoveredResponse:
    """추적에 없는 레포 (KDEV-DEC-017 D17).

    **실패해도 200 이다.** 배너 하나 때문에 레지스트리 표가 안 뜨면 안 된다 —
    오류를 본문에 실어 배너만 실패시킨다(SPEC-014 U-1).
    """
    known = {r.slug for r in await registry.list_rows(db)}
    try:
        found = await discover.list_undiscovered(known)
    except discover.DiscoveryError as exc:
        logger.warning("미등록 조회 실패 — %s", exc)
        return DiscoveredResponse(items=[], error=str(exc))
    return DiscoveredResponse(
        items=[
            DiscoveredRow(
                slug=r.slug, account=r.account, pushed_at=r.pushed_at, private=r.private
            )
            for r in found.items
        ],
        hidden_old=found.hidden_old,
        window_days=discover.DISCOVERY_WINDOW_DAYS,
    )


async def _sync_in_background(repo_id: int) -> None:
    """등록 직후 클론. **요청 안에서 기다리지 않는다** — 최초 클론은 수 분이 걸린다.

    결과는 행의 `last_fetched_at`·`last_error` 로 남고 화면이 목록 조회로 확인한다.
    세션을 새로 연다 — 요청 세션은 응답과 함께 닫힌다.
    """
    try:
        async with new_session() as db:
            await registry.resync(db, repo_id)
            await db.commit()
    except Exception:  # noqa: BLE001 — 백그라운드라 올릴 곳이 없다
        logger.exception("백그라운드 동기화 실패 — id=%s", repo_id)


@router.post("", response_model=RegistryRow, status_code=201)
async def register_product(
    body: RegisterRequest,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> RegistryRow:
    root = config.repo_root()
    try:
        row = await registry.register(
            db,
            repo=body.repo,
            kind=body.type,
            detail=body.detail,
            product_slug=body.product_slug,
            card=body.card.model_dump() if body.card else None,
            repo_root=root,
        )
    except (ProductError, ScaffoldError) as exc:
        raise _http_error(exc) from exc

    await db.commit()
    background.add_task(_sync_in_background, row.id)
    return _row(row, root)


@router.patch("/{repo_id}", response_model=RegistryRow)
async def patch_product(
    repo_id: int, body: PatchRequest, db: AsyncSession = Depends(get_db)
) -> RegistryRow:
    root = config.repo_root()
    try:
        row = await registry.update(
            db,
            repo_id,
            detail=body.detail,
            product_slug=body.product_slug,
            enabled=body.enabled,
            # **보낸 필드만 반영한다** — 안 보낸 것과 null 을 보낸 것은 다르다.
            fields_set=set(body.model_fields_set),
        )
    except ProductNotFound as exc:
        raise HTTPException(404, detail=str(exc)) from exc
    except ProductError as exc:
        raise _http_error(exc) from exc

    await db.commit()
    return _row(row, root)


@router.post("/{repo_id}/sync", response_model=SyncResponse)
async def sync_product(
    repo_id: int, db: AsyncSession = Depends(get_db)
) -> SyncResponse:
    """수동 재동기화. **실패도 200 이다** — 행에 사유가 남는 정상적인 상태다."""
    root = config.repo_root()
    try:
        row = await registry.resync(db, repo_id)
    except ProductNotFound as exc:
        raise HTTPException(404, detail=str(exc)) from exc

    await db.commit()
    ok = row.last_error is None
    code = None if ok else str(row.last_error).split(":", 1)[0]
    return SyncResponse(
        row=_row(row, root), ok=ok, code=code, message=row.last_error
    )


@router.post("/{repo_id}/visible", response_model=RegistryRow)
async def set_visible(
    repo_id: int, body: VisibleRequest, db: AsyncSession = Depends(get_db)
) -> RegistryRow:
    """카드 노출 토글 (KDEV-DEC-017 D18).

    DB 를 안 바꾸므로 응답의 `card_visible` 은 **다시 읽은 파일에서** 나온다 —
    쓰기가 실제로 반영됐는지가 응답으로 확인된다.
    """
    root = config.repo_root()
    try:
        row = await registry.set_visible(db, repo_id, body.value, repo_root=root)
    except ProductNotFound as exc:
        raise HTTPException(404, detail=str(exc)) from exc
    except (ProductError, ScaffoldError) as exc:
        raise _http_error(exc) from exc
    return _row(row, root)


@router.post("/{repo_id}/card", response_model=RegistryRow)
async def add_card(
    repo_id: int, body: CardInput, db: AsyncSession = Depends(get_db)
) -> RegistryRow:
    """이미 있는 제품에 공개 카드를 붙인다.

    등록(`POST ""`)과 나눠 둔 이유는 상황이 다르기 때문이다 — 등록은 제품 디렉토리가
    **없어야** 하고, 이쪽은 **있어야** 한다.
    """
    root = config.repo_root()
    try:
        row = await registry.add_card(db, repo_id, body.model_dump(), repo_root=root)
    except ProductNotFound as exc:
        raise HTTPException(404, detail=str(exc)) from exc
    except (ProductError, ScaffoldError) as exc:
        raise _http_error(exc) from exc
    return _row(row, root)

