"""계층 조회 API — 데이터 화면이 딛는 표면.

- GET /api/layers/{layer}/tables          — 테이블 목록 + 행수 + 근거 기록 + flows_to
- GET /api/layers/{layer}/{table}         — 행 조회(브론즈·실버는 마스킹 뷰 경유)
- GET /api/layers/{layer}/{table}/lineage — 컬럼별 변환 규칙·계산식·근거 기록

행 조회는 도구 `query_layer` 와 **같은 함수**를 지난다 — API 전용 우회 경로를 만들지
않는다(DEC-002).
"""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Query

from api.deps import as_http, require_session
from service import allowlist as al
from service import lineage as lineage_service
from service.db import open_serving_db
from service.errors import QueryError, UnknownField
from service.queries import query_layer

router = APIRouter(
    prefix="/api/layers", tags=["layers"], dependencies=[Depends(require_session)]
)


def _parse_filters(raw: str | None) -> list[dict]:
    """`filters` 는 JSON 배열 문자열이다 — `{field, op, value}` 최대 5개."""
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise as_http(UnknownField(f"filters 가 JSON 이 아니다: {exc}")) from exc
    if not isinstance(parsed, list):
        raise as_http(UnknownField("filters 는 배열이어야 한다"))
    return parsed


def _parse_order(field: str | None, direction: str) -> dict | None:
    return {"field": field, "direction": direction} if field else None


@router.get("/{layer}/tables")
def get_tables(layer: str) -> dict:
    try:
        with open_serving_db() as conn:
            return lineage_service.layer_tables(conn, layer)
    except QueryError as exc:
        raise as_http(exc) from exc


@router.get("/{layer}/{table}")
def get_rows(
    layer: str,
    table: str,
    filters: str | None = Query(default=None),
    order_by: str | None = Query(default=None),
    direction: str = Query(default="asc"),
    limit: int = Query(default=al.DEFAULT_API_LIMIT),
    offset: int = Query(default=0),
) -> dict:
    try:
        with open_serving_db() as conn:
            return query_layer(
                conn, layer=layer, table=table,
                filters=_parse_filters(filters),
                order_by=_parse_order(order_by, direction),
                limit=limit, offset=offset,
            )
    except QueryError as exc:
        raise as_http(exc) from exc


@router.get("/{layer}/{table}/lineage")
def get_lineage(layer: str, table: str) -> dict:
    try:
        with open_serving_db() as conn:
            return lineage_service.lineage(conn, layer, table)
    except QueryError as exc:
        raise as_http(exc) from exc
