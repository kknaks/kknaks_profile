"""모니터링 API — KPI 카드 · 시계열 · 그래프 · 예보.

- GET /api/kpi/cards   — 카드 + 최근 창 상태 + 기간 스테퍼 근거
- GET /api/kpi/series  — 시계열. 도구 `query_kpi` 와 **같은 함수**를 지난다
- GET /api/graph       — 노드·엣지 + 판정 구분
- GET /api/forecast    — 확정 엣지 기반 예보 2건

`/api/kpi/series` 가 `query_kpi` 와 같은 구현을 부르므로 SPEC-003 AC-5(오차 0)는
대조가 아니라 **구조로** 성립한다 — 화면용 집계 로직이 따로 없다.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from api.deps import as_http, require_session
from service import monitoring
from service.db import open_serving_db
from service.errors import QueryError
from service.queries import query_kpi

kpi_router = APIRouter(
    prefix="/api/kpi", tags=["kpi"], dependencies=[Depends(require_session)]
)
graph_router = APIRouter(tags=["graph"], dependencies=[Depends(require_session)])


@kpi_router.get("/cards")
def get_cards(
    period: str | None = Query(default=None, description="YYYY-MM, 기본 최신"),
    window_days: int = Query(default=7),
) -> dict:
    try:
        with open_serving_db() as conn:
            return monitoring.kpi_cards(conn, period=period, window_days=window_days)
    except QueryError as exc:
        raise as_http(exc) from exc


@kpi_router.get("/series")
def get_series(
    metrics: list[str] = Query(...),
    grain: str = Query(default="daily"),
    start: str = Query(...),
    end: str = Query(...),
    include_status: bool = Query(default=True),
    include_deltas: bool = Query(default=False),
) -> dict:
    try:
        with open_serving_db() as conn:
            return query_kpi(
                conn, metrics=list(metrics), grain=grain, start=start, end=end,
                include_status=include_status, include_deltas=include_deltas,
            )
    except QueryError as exc:
        raise as_http(exc) from exc


def _split_verdicts(raw: list[str] | None) -> list[str] | None:
    """판정 목록을 평탄화한다.

    정본은 `verdicts=채택,자동 확정` 처럼 **콤마로 묶은 단일 파라미터**이고,
    `verdicts=채택&verdicts=자동 확정` 반복 파라미터도 같이 받는다. 두 형식이
    섞여 와도 같은 목록이 된다. 알 수 없는 판정값 판정은 `service.monitoring` 이 한다.
    """
    if not raw:
        return None
    items = [part.strip() for value in raw for part in value.split(",")]
    items = [item for item in items if item]
    return items or None


@graph_router.get("/api/graph")
def get_graph(
    verdicts: list[str] | None = Query(default=None),
    as_of: str | None = Query(default=None),
    window_days: int = Query(default=7),
) -> dict:
    try:
        with open_serving_db() as conn:
            return monitoring.graph(
                conn, verdicts=_split_verdicts(verdicts),
                as_of=as_of, window_days=window_days,
            )
    except QueryError as exc:
        raise as_http(exc) from exc


@graph_router.get("/api/forecast")
def get_forecast(window_days: int = Query(default=30)) -> dict:
    try:
        with open_serving_db() as conn:
            return monitoring.forecast(conn, window_days=window_days)
    except QueryError as exc:
        raise as_http(exc) from exc
