"""잔디 — 1층.

- GET /api/activity — 공개 조회. /about 의 ContribGrass 가 읽는다

테이블이 없다 — commit 을 날짜로 묶은 파생이다(erd.md §잔디). 커밋을 채우는
것은 수집 파이프라인(케이스 6·7) 몫이라, 그것이 서기 전에는 빈 잔디가 내려간다.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from schemas.activity import ActivityResponse
from service.activity_service import activity_service

router = APIRouter(prefix="/api/activity", tags=["activity"])


@router.get("", response_model=ActivityResponse, response_model_by_alias=True)
async def get_activity(db: AsyncSession = Depends(get_db)) -> ActivityResponse:
    dto = await activity_service.get_activity(db)
    return ActivityResponse.from_dto(dto)
